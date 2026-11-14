"""BizHawk client: speaks OoTMM's multiworld protocol through the RAM mailbox of our OoTMM patch.

See "Client" in DEVELOPMENT.md. The game sends a WAL item packet, with the check's key, for every check the
player gets (their own items too), and asks for the items it should receive by index (WAL query). The client
reports the checks to the server and answers the queries with the items the server sent, in order.
"""
from __future__ import annotations

import logging
import struct
import time
from typing import TYPE_CHECKING

from NetUtils import ClientStatus
import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient

from . import items, locations, ootxmm_staticdata

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext

logger = logging.getLogger("Client")

RDRAM = "RDRAM"
MAGIC = b"OoTMM-IPC-RAM-1\x00"
RING = 0x800
HEADER = 0x28  # magic (16), connected, alive, outHead, outTail, inHead, inTail (u32 each)
HELLO_MAGIC = b"OoTMM\x7f\x01\x00"
DIRECTORY_MAGIC = b"APIPC001"
SCAN_CHUNK = 0x8000
# Each read stalls the emulator while the connector copies it, so a full scan is spread over many polls: a game
# switch was 30 seconds slower with 16 reads per poll.
SCAN_READS_PER_POLL = 4
# How long the client only rechecks the addresses where it found a mailbox before, while a game switch loads,
# before it scans all of RAM. Each game's mailbox is at the same address every time it loads.
KNOWN_MAILBOX_WAIT_SECONDS = 20.0
MAILBOX_STALL_SECONDS = 3.0
# Full RAM scans without any copy of the magic before the client warns that the ROM has no mailbox. The magic
# is a string constant in our patch's code, so a patched game has a copy as soon as its code is loaded.
EMPTY_SCANS_BEFORE_WARNING = 3
NO_MAILBOX_WARNING = (
    "This game has no Archipelago mailbox: the ROM was not built from an OOTxMM .ootmm patch, so no item can "
    "be sent or received. A seed generated directly on ootmm.com, or a patch from another seed, does not work. "
    "Apply your slot's .ootmm patch in the OoTMM website's Patch mode and open that ROM.")

OP_HELLO, OP_WAL, OP_WAL_QUERY, OP_WAL_ACK = 0x01, 0x02, 0x03, 0x04
WAL_ITEM = 0x01

# The game is world 1; items it receives come from world 2, so it doesn't take them for its own pickups.
OUR_WORLD = 1
OTHER_WORLD = 2

_info = ootxmm_staticdata.OOTxMMCheckInfo
LOCATION_BY_KEY = {key: locations.LOCATION_NAME_TO_ID[name] for name, key in _info["keys"].items()
                   if name in locations.LOCATION_NAME_TO_ID}
GOAL_GI = {gi: event for event, gi in _info["goalGi"].items()}
GI_NOTHING = next(item["gi"] for item in ootxmm_staticdata.OOTxMMItemData if item["id"] == "NOTHING")
GI_BY_ITEM_ID = {ootxmm_staticdata.OOTxMMItemIDs[item["id"]]: item["gi"] for item in ootxmm_staticdata.OOTxMMItemData}


class OOTxMMClient(BizHawkClient):
    game = "OOTxMM"
    system = "N64"
    patch_suffix = None

    def __init__(self) -> None:
        super().__init__()
        self.known_mailboxes: list[int] = []  # where mailboxes were found, kept across resets
        self.rom_mailboxes: list[int] = []  # exact payload addresses from this ROM's versioned header
        self.reset()
        self.goals: set[str] = set()
        self.goal_key: str | None = None

    def reset(self) -> None:
        self.mailbox: int | None = None
        self.candidates: dict[int, int | None] = {}  # mailbox address -> alive counter last seen
        self.scan_pos: int | None = 0  # next RAM address to scan, None when the scan is done
        self.scan_done_at = 0.0
        self.empty_scans = 0
        self.known_since: float | None = None  # when the client started waiting at the known addresses
        self.seq_net = 0
        self.last_query: int | None = None
        self.last_alive: int | None = None
        self.alive_changed_at = 0.0
        self.attach_alive: int | None = None
        self.attach_started = 0.0

    def on_package(self, ctx: "BizHawkClientContext", cmd: str, args: dict) -> None:
        if cmd == "Connected":
            # Re-read on every login, including reconnects to the same slot.
            self.goal_key = None
            self.goals.clear()
        elif self.goal_key is not None:
            value = None
            if cmd == "Retrieved":
                value = args["keys"].get(self.goal_key)
            elif cmd == "SetReply" and args["key"] == self.goal_key:
                value = args["value"]
            if isinstance(value, dict):
                self.goals.update(event for event in GOAL_GI.values() if value.get(event) is True)

    async def sync_goals(self, ctx: "BizHawkClientContext") -> None:
        key = f"ootxmm_goals_{ctx.server_seed_name}_{ctx.team}_{ctx.slot}"
        if key != self.goal_key:
            self.goals.clear()
            self.goal_key = key
            await ctx.send_msgs([{"cmd": "Get", "keys": [key]}])

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        try:
            header = (await bizhawk.read(ctx.bizhawk_ctx, [(0, 0x40, "ROM")]))[0]
        except bizhawk.RequestFailedError:
            return False
        if not header[0x20:0x34].startswith(b"OOT+MM COMBO"):
            return False
        self.known_mailboxes.clear()
        self.rom_mailboxes = []
        if header[0x18:0x20] == DIRECTORY_MAGIC:
            addresses = [int.from_bytes(header[offset:offset + 3], "big") for offset in (0x34, 0x37)]
            if all(0 < address <= 0x800000 - HEADER - 2 * RING and address % 16 == 0
                   for address in addresses) and len(set(addresses)) == 2:
                self.rom_mailboxes = addresses
            else:
                logger.warning("Invalid ROM mailbox directory; using RAM discovery")
        ctx.game = self.game
        # Items from other worlds and the starting inventory: the game gives the player's own pickups itself.
        ctx.items_handling = 0b101
        ctx.want_slot_data = True  # the goal setting
        # The game drops the connection when its 2 KB outgoing ring is full (about a second of queries and
        # positions), and waits for an ack before each pickup after the first: poll often.
        ctx.watcher_timeout = 0.125
        self.reset()
        return True

    async def find_mailbox(self, ctx: "BizHawkClientContext") -> None:
        # The magic is also in the game's code as a string constant, and after a game switch the other game's
        # mailbox stays in RAM: the live mailbox is the 16-aligned one whose alive counter moves. It only moves
        # in gameplay, not on the title screen or the file select.
        # The connector's replies are capped at 64 KB, so RAM is scanned a few small reads per poll. The mailbox
        # is 16-aligned and the reads are too, so the magic is never split between two, but the alive counter
        # after it can be in the next read, so candidates get their first value from the polls below.
        if self.rom_mailboxes:
            # A directory is only a hint: still require the magic and a moving alive counter before writing.
            # Read both games together, so a stale old-game copy never delays first arrival in the other game.
            await self.check_candidates(ctx, self.rom_mailboxes)
            return
        if self.scan_pos == 0 and await self.check_known_mailboxes(ctx):
            return
        if self.scan_pos is not None:
            size = await bizhawk.get_memory_size(ctx.bizhawk_ctx, RDRAM)
            for _ in range(SCAN_READS_PER_POLL):
                if self.scan_pos >= size:
                    self.scan_pos = None
                    self.scan_done_at = time.monotonic()
                    if self.candidates:
                        self.empty_scans = 0
                    else:
                        self.empty_scans += 1
                        if self.empty_scans == EMPTY_SCANS_BEFORE_WARNING:
                            logger.warning(NO_MAILBOX_WARNING)
                    break
                data = (await bizhawk.read(ctx.bizhawk_ctx, [(self.scan_pos, SCAN_CHUNK, RDRAM)]))[0]
                start = data.find(MAGIC)
                while start != -1:
                    if start % 16 == 0:
                        self.candidates.setdefault(self.scan_pos + start, None)
                    start = data.find(MAGIC, start + 1)
                self.scan_pos += SCAN_CHUNK
            return
        if not self.candidates:
            self.scan_pos = 0
            return
        await self.check_candidates(ctx, list(self.candidates))
        if self.mailbox is not None:
            return
        if time.monotonic() - self.scan_done_at >= MAILBOX_STALL_SECONDS:
            # Every copy found is stale: the live mailbox was written after the scan passed it, as during a
            # game switch. Scan again, or the client would watch the stale copies forever.
            self.scan_pos = 0

    async def check_candidates(self, ctx: "BizHawkClientContext", addresses: list[int]) -> None:
        reads = await bizhawk.read(ctx.bizhawk_ctx, [(address, 24, RDRAM) for address in addresses])
        for address, raw in zip(addresses, reads):
            if raw[:16] != MAGIC:
                self.candidates.pop(address, None)
                continue
            alive = struct.unpack_from(">I", raw, 20)[0]
            previous = self.candidates.get(address)
            if previous is not None and alive != previous:
                self.mailbox = address
                self.seq_net = 0
                if address not in self.known_mailboxes:
                    self.known_mailboxes.append(address)
                logger.info(f"Found the game's mailbox at 0x{address:X}")
                return
            self.candidates[address] = alive

    async def check_known_mailboxes(self, ctx: "BizHawkClientContext") -> bool:
        """Before a full scan, wait at the addresses where mailboxes were found: one small read per poll instead
        of hundreds while the other game loads. Returns False when the full scan should run."""
        if not self.known_mailboxes:
            return False
        now = time.monotonic()
        if self.known_since is None:
            self.known_since = now
        elif now - self.known_since >= KNOWN_MAILBOX_WAIT_SECONDS:
            return False
        reads = await bizhawk.read(ctx.bizhawk_ctx, [(address, 16, RDRAM) for address in self.known_mailboxes])
        found = [address for address, raw in zip(self.known_mailboxes, reads) if raw == MAGIC]
        if found:
            # Watch them as a scan's candidates; if none comes alive, this runs again until the wait ends.
            for address in found:
                self.candidates.setdefault(address, None)
            self.scan_pos = None
            self.scan_done_at = now
        return True

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        # An exception out of here ends Archipelago's watcher loop, and the client with it.
        try:
            if ctx.server is None or ctx.slot is None:
                if self.mailbox is not None:
                    # Without a server, the game must keep what it sends: it waits for an ack that never comes.
                    await self.write_mailbox(ctx, [(self.mailbox + 16, [0, 0, 0, 0], RDRAM)])
                    self.reset()
                return
            if self.mailbox is None:
                await self.find_mailbox(ctx)
                if self.mailbox is None:
                    return
                # A restored game or an unclean client exit can retain another session's
                # connected flag and packet sequence. Let the game observe a disconnect
                # before starting a new handshake; a paused counter is not acknowledgement.
                if not await self.write_mailbox(ctx, [(self.mailbox + 16, [0, 0, 0, 0], RDRAM)]):
                    self.reset()
                    return
                header, = await bizhawk.read(ctx.bizhawk_ctx, [(self.mailbox, 24, RDRAM)])
                if header[:16] != MAGIC:
                    self.reset()
                    return
                self.attach_alive = struct.unpack_from(">I", header, 20)[0]
                self.attach_started = time.monotonic()
                return
            if self.attach_alive is not None:
                header, = await bizhawk.read(ctx.bizhawk_ctx, [(self.mailbox, 24, RDRAM)])
                if header[:16] != MAGIC:
                    self.reset()
                    return
                if struct.unpack_from(">I", header, 20)[0] == self.attach_alive:
                    if time.monotonic() - self.attach_started >= MAILBOX_STALL_SECONDS:
                        self.reset()
                    return
                if not await self.write_mailbox(ctx, [(self.mailbox + 16, [0, 0, 0, 1], RDRAM)]):
                    self.reset()
                    return
                self.attach_alive = None
            await self.exchange(ctx)
        except (bizhawk.RequestFailedError, bizhawk.NotConnectedError):
            pass

    async def write_mailbox(self, ctx: "BizHawkClientContext", writes: list) -> bool:
        # Only while the mailbox is still there: a game switch can put other data at this address between polls.
        return await bizhawk.guarded_write(ctx.bizhawk_ctx, writes, [(self.mailbox, MAGIC, RDRAM)])

    async def exchange(self, ctx: "BizHawkClientContext") -> None:
        await self.sync_goals(ctx)
        mailbox = self.mailbox
        header, ring = await bizhawk.read(ctx.bizhawk_ctx, [(mailbox, HEADER, RDRAM), (mailbox + HEADER, RING, RDRAM)])
        if header[:16] != MAGIC:
            # A reset or a game switch: the mailbox is gone or moved.
            self.reset()
            return
        connected, alive, out_head, out_tail, in_head, in_tail = struct.unpack_from(">6I", header, 16)
        if connected == 0:
            # The game reinitialized its mailbox (a game switch reloads it): attach again.
            self.reset()
            return

        now = time.monotonic()
        if alive != self.last_alive:
            self.last_alive = alive
            self.alive_changed_at = now
        elif now - self.alive_changed_at >= MAILBOX_STALL_SECONDS:
            # A game switch can leave the old mailbox intact, including connected=1.
            # Rescan for a moving counter. Paused emulation reattaches when it resumes.
            self.reset()
            return

        if any(offset >= RING for offset in (out_head, out_tail, in_head, in_tail)):
            logger.warning("Invalid mailbox ring offsets; restarting discovery")
            self.reset()
            return

        packets = []
        tail = out_tail
        remaining = (out_head - out_tail) % RING
        while remaining:
            if remaining < 2:
                logger.warning("Incomplete mailbox packet header; restarting discovery")
                self.reset()
                return
            size = (ring[tail] << 8) | ring[(tail + 1) % RING]
            if size < 5 or size + 2 > remaining:
                logger.warning("Invalid mailbox packet length; restarting discovery")
                self.reset()
                return
            tail = (tail + 2) % RING
            packets.append(bytes(ring[(tail + i) % RING] for i in range(size)))
            tail = (tail + size) % RING
            remaining -= size + 2

        seq_before = self.seq_net
        replies: list[bytes] = []
        checked: set[int] = set()
        goals: set[str] = set()
        query: int | None = None
        for packet in packets:
            op = packet[4]
            if op == OP_HELLO:
                # The game says hello every 30 frames until it reads an answer; answer the latest only, as a
                # second answer after it connected would break its sequence check. Our packets are numbered
                # from 1 after the hello; the game's numbering is its own business.
                self.seq_net = 1
                replies = [struct.pack(">IB8sII", 0, OP_HELLO, HELLO_MAGIC, 0, 1)]
                logger.info("Connected to the game")
                query = None
            elif self.seq_net == 0:
                # The old session's queued queries cannot establish a new connection.
                # Reliable checks will be resent after the game completes its hello.
                continue
            elif op == OP_WAL and len(packet) >= 10:
                token, kind = struct.unpack_from(">IB", packet, 5)
                if kind == WAL_ITEM and len(packet) >= 20:
                    to, _, gi, flags, key = struct.unpack_from(">BBhhI", packet, 10)
                    if key in LOCATION_BY_KEY:
                        checked.add(LOCATION_BY_KEY[key])
                    if gi in GOAL_GI and to == OUR_WORLD:
                        goals.add(GOAL_GI[gi])
                replies.append(self.packet(OP_WAL_ACK, struct.pack(">I", token)))
            elif op == OP_WAL_QUERY and len(packet) >= 9:
                query = struct.unpack_from(">I", packet, 5)[0]

        if query is not None and query != self.last_query:
            # The game has taken every item before this index.
            logger.info(f"The game has {query} of {len(ctx.items_received)} received items")
            self.last_query = query
        if query is not None and query < len(ctx.items_received):
            replies.append(self.wal_item(ctx, query))

        data = b"".join(struct.pack(">H", len(reply)) + reply for reply in replies)
        free = (in_tail - in_head - 1) % RING
        seq_after = self.seq_net
        self.seq_net = seq_before
        if len(data) > free:
            # Retry this batch after the game drains its ring. Consuming it or advancing the
            # sequence here would lose acknowledgements and disconnect the game's protocol.
            return

        # CommonClient resends this local set on login. Retain checks before acknowledging
        # their WAL packets, including when send_msgs returns during a socket disconnect.
        ctx.locations_checked.update(checked)
        new = checked - ctx.checked_locations
        if new:
            await ctx.send_msgs([{"cmd": "LocationChecks", "locations": sorted(new)}])

        unsaved_goals = goals - self.goals
        if unsaved_goals:
            # Persist before acknowledging the pickup. Updating individual keys preserves the other boss,
            # even if its stored result has not arrived yet or another client is connected to this slot.
            await ctx.send_msgs([{"cmd": "Set", "key": self.goal_key, "default": {}, "want_reply": True,
                                  "operations": [{"operation": "update", "value": dict.fromkeys(unsaved_goals, True)}]}])
            # A socket can close while send_msgs silently returns. Keep the game's reliable
            # pickup pending until Retrieved/SetReply confirms the server has stored it.
            if not goals <= self.goals:
                return

        writes = [(mailbox + 28, list(struct.pack(">I", tail)), RDRAM)]
        if replies:
            first = min(len(data), RING - in_head)
            writes.append((mailbox + HEADER + RING + in_head, list(data[:first]), RDRAM))
            if first < len(data):
                writes.append((mailbox + HEADER + RING, list(data[first:]), RDRAM))
            writes.append((mailbox + 32, list(struct.pack(">I", (in_head + len(data)) % RING)), RDRAM))
        if not await self.write_mailbox(ctx, writes):
            self.reset()
            return
        self.seq_net = seq_after

        if not ctx.finished_game and self.goal_reached(ctx):
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            ctx.finished_game = True

    def packet(self, op: int, body: bytes) -> bytes:
        packet = struct.pack(">IB", self.seq_net, op) + body
        self.seq_net += 1
        return packet

    def wal_item(self, ctx: "BizHawkClientContext", index: int) -> bytes:
        item = ctx.items_received[index]
        gi = GI_BY_ITEM_ID.get(item.item) or GI_NOTHING
        name = ctx.player_names.get(item.player, "")
        sender = name.encode("ascii", "replace")[:8].ljust(8, b"\x00")
        # GI_NOTHING: the game gives nothing and moves on to the next index.
        body = struct.pack(">IBB8sBBhhI", index, WAL_ITEM, OTHER_WORLD, sender, OUR_WORLD, 0, gi, 0, 0)
        return self.packet(OP_WAL, body)

    def goal_reached(self, ctx: "BizHawkClientContext") -> bool:
        slot = ctx.slot_data or {}
        settings = slot.get("settings", {})
        goal = settings.get("goal")
        if goal in ("triforce", "triforce3"):
            ids = ootxmm_staticdata.OOTxMMItemIDs
            local = [item for location, item in slot.get("local_triforce", {}).items()
                     if int(location) in ctx.checked_locations]
            delivered = [item.item for item in ctx.items_received[:self.last_query or 0]]
            if goal == "triforce":
                piece = ids["SHARED_TRIFORCE"]
                return local.count(piece) + delivered.count(piece) >= settings["triforceGoal"]
            return {ids["SHARED_TRIFORCE_" + aspect] for aspect in ("POWER", "COURAGE", "WISDOM")} <= set(local + delivered)
        if goal == "ganon":
            return "OOT_GANON" in self.goals
        if goal == "majora":
            return "MM_MAJORA" in self.goals
        if goal == "any":
            return bool(self.goals)
        return {"OOT_GANON", "MM_MAJORA"} <= self.goals
