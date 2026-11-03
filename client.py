"""BizHawk client: speaks OoTMM's multiworld protocol through the RAM mailbox of our OoTMM patch.

See "Client" in DEVELOPMENT.md. The game sends a WAL item packet, with the check's key, for every check the
player gets (their own items too), and asks for the items it should receive by index (WAL query). The client
reports the checks to the server and answers the queries with the items the server sent, in order.
"""
from __future__ import annotations

import struct
from typing import TYPE_CHECKING

from NetUtils import ClientStatus
import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient

from . import items, locations, ootxmm_staticdata

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext

RDRAM = "RDRAM"
MAGIC = b"OoTMM-IPC-RAM-1\x00"
RING = 0x800
HEADER = 0x28  # magic (16), connected, alive, outHead, outTail, inHead, inTail (u32 each)
HELLO_MAGIC = b"OoTMM\x7f\x01\x00"

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
        self.reset()

    def reset(self) -> None:
        self.mailbox: int | None = None
        self.candidates: dict[int, int] = {}  # mailbox address -> alive counter last seen
        self.seq_net = 0
        self.goals: set[str] = set()

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        try:
            name = (await bizhawk.read(ctx.bizhawk_ctx, [(0x20, 20, "ROM")]))[0]
        except bizhawk.RequestFailedError:
            return False
        if not name.startswith(b"OOT+MM COMBO"):
            return False
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
        if not self.candidates:
            size = await bizhawk.get_memory_size(ctx.bizhawk_ctx, RDRAM)
            chunk = 0x10000
            reads = await bizhawk.read(ctx.bizhawk_ctx, [(base, chunk, RDRAM) for base in range(0, size, chunk)])
            data = b"".join(reads)
            start = data.find(MAGIC)
            while start != -1:
                if start % 16 == 0:
                    self.candidates[start] = struct.unpack_from(">I", data, start + 20)[0]
                start = data.find(MAGIC, start + 1)
            return
        reads = await bizhawk.read(ctx.bizhawk_ctx, [(address, 24, RDRAM) for address in self.candidates])
        for address, raw in zip(list(self.candidates), reads):
            if raw[:16] != MAGIC:
                del self.candidates[address]
                continue
            alive = struct.unpack_from(">I", raw, 20)[0]
            if alive != self.candidates[address]:
                self.mailbox = address
                self.seq_net = 0
                return
            self.candidates[address] = alive

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        if ctx.server is None or ctx.slot is None:
            if self.mailbox is not None:
                # Without a server, the game must keep what it sends: it waits for an ack that never comes.
                await bizhawk.write(ctx.bizhawk_ctx, [(self.mailbox + 16, [0, 0, 0, 0], RDRAM)])
            return
        try:
            if self.mailbox is None:
                await self.find_mailbox(ctx)
                if self.mailbox is None:
                    return
                await bizhawk.write(ctx.bizhawk_ctx, [(self.mailbox + 16, [0, 0, 0, 1], RDRAM)])
            await self.exchange(ctx)
        except bizhawk.RequestFailedError:
            pass

    async def exchange(self, ctx: "BizHawkClientContext") -> None:
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

        packets = []
        tail = out_tail
        while tail != out_head:
            size = (ring[tail] << 8) | ring[(tail + 1) % RING]
            tail = (tail + 2) % RING
            packets.append(bytes(ring[(tail + i) % RING] for i in range(size)))
            tail = (tail + size) % RING

        replies: list[bytes] = []
        checked: set[int] = set()
        query: int | None = None
        for packet in packets:
            if len(packet) < 5:
                continue
            op = packet[4]
            if op == OP_HELLO:
                # The game says hello every 30 frames until it reads an answer; answer the latest only, as a
                # second answer after it connected would break its sequence check. Our packets are numbered
                # from 1 after the hello; the game's numbering is its own business.
                self.seq_net = 1
                replies = [struct.pack(">IB8sII", 0, OP_HELLO, HELLO_MAGIC, 0, 1)]
                query = None
            elif op == OP_WAL and len(packet) >= 10:
                token, kind = struct.unpack_from(">IB", packet, 5)
                if kind == WAL_ITEM and len(packet) >= 20:
                    to, _, gi, flags, key = struct.unpack_from(">BBhhI", packet, 10)
                    if key in LOCATION_BY_KEY:
                        checked.add(LOCATION_BY_KEY[key])
                    if gi in GOAL_GI and to == OUR_WORLD:
                        self.goals.add(GOAL_GI[gi])
                replies.append(self.packet(OP_WAL_ACK, struct.pack(">I", token)))
            elif op == OP_WAL_QUERY and len(packet) >= 9:
                query = struct.unpack_from(">I", packet, 5)[0]

        if query is not None and query < len(ctx.items_received):
            replies.append(self.wal_item(ctx, query))

        writes = [(mailbox + 28, list(struct.pack(">I", tail)), RDRAM)]
        if replies:
            data = b"".join(struct.pack(">H", len(reply)) + reply for reply in replies)
            free = (in_tail - in_head - 1) % RING
            if len(data) <= free:
                first = min(len(data), RING - in_head)
                writes.append((mailbox + HEADER + RING + in_head, list(data[:first]), RDRAM))
                if first < len(data):
                    writes.append((mailbox + HEADER + RING, list(data[first:]), RDRAM))
                writes.append((mailbox + 32, list(struct.pack(">I", (in_head + len(data)) % RING)), RDRAM))
        await bizhawk.write(ctx.bizhawk_ctx, writes)

        new = checked - ctx.checked_locations
        if new:
            await ctx.send_msgs([{"cmd": "LocationChecks", "locations": sorted(new)}])
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
        goal = ctx.slot_data.get("settings", {}).get("goal") if ctx.slot_data else None
        if goal == "ganon":
            return "OOT_GANON" in self.goals
        if goal == "majora":
            return "MM_MAJORA" in self.goals
        if goal == "any":
            return bool(self.goals)
        return {"OOT_GANON", "MM_MAJORA"} <= self.goals
