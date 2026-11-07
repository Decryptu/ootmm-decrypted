import asyncio
import struct
import unittest
from types import SimpleNamespace
from unittest import mock

from NetUtils import NetworkItem

from .. import client, locations, ootxmm_staticdata

MAILBOX = 0x1000


class FakeGame:
    """The game's side of the RAM mailbox (ram.c in our OoTMM patch), in a bytearray."""
    def __init__(self) -> None:
        self.ram = bytearray(0x4000)
        self.ram[MAILBOX:MAILBOX + 16] = client.MAGIC
        self.seq = 0

    def u32(self, offset: int) -> int:
        return struct.unpack_from(">I", self.ram, MAILBOX + offset)[0]

    def set_u32(self, offset: int, value: int) -> None:
        struct.pack_into(">I", self.ram, MAILBOX + offset, value)

    def send(self, packet: bytes) -> None:
        head = self.u32(24)
        for byte in struct.pack(">H", len(packet)) + packet:
            self.ram[MAILBOX + client.HEADER + head] = byte
            head = (head + 1) % client.RING
        self.set_u32(24, head)

    def receive(self) -> list[bytes]:
        packets, tail, head = [], self.u32(36), self.u32(32)
        base = MAILBOX + client.HEADER + client.RING
        while tail != head:
            size = (self.ram[base + tail] << 8) | self.ram[base + (tail + 1) % client.RING]
            tail = (tail + 2) % client.RING
            packets.append(bytes(self.ram[base + (tail + i) % client.RING] for i in range(size)))
            tail = (tail + size) % client.RING
        self.set_u32(36, tail)
        return packets

    async def read(self, _ctx, read_list):
        return [bytes(self.ram[address:address + size]) for address, size, _ in read_list]

    async def guarded_write(self, _ctx, write_list, guard_list):
        if any(self.ram[address:address + len(data)] != data for address, data, _ in guard_list):
            return False
        for address, data, _ in write_list:
            self.ram[address:address + len(data)] = bytes(data)
        return True


class TestClientProtocol(unittest.TestCase):
    def setUp(self) -> None:
        self.game = FakeGame()
        self.game.set_u32(16, 1)
        self.client = client.OOTxMMClient()
        self.client.mailbox = MAILBOX
        self.sent: list[dict] = []

        async def send_msgs(msgs):
            self.sent += msgs
            for msg in msgs:
                if msg["cmd"] == "Set":
                    self.client.on_package(self.ctx, "SetReply", {
                        "key": msg["key"], "value": msg["operations"][0]["value"]})
        self.ctx = SimpleNamespace(
            bizhawk_ctx=None, items_received=[], checked_locations=set(), locations_checked=set(), finished_game=False,
            server_seed_name="test-seed", team=0, slot=1,
            player_names={2: "Zelda"}, slot_data={"settings": {"goal": "ganon"}}, send_msgs=send_msgs)
        asyncio.run(self.client.sync_goals(self.ctx))
        self.sent.clear()

    def exchange(self) -> list[bytes]:
        with mock.patch.object(client.bizhawk, "read", self.game.read), \
                mock.patch.object(client.bizhawk, "guarded_write", self.game.guarded_write):
            asyncio.run(self.client.exchange(self.ctx))
        return self.game.receive()

    def test_hello(self) -> None:
        self.game.send(struct.pack(">IB", 0, client.OP_HELLO) + client.HELLO_MAGIC + bytes(49))
        (reply,) = self.exchange()
        self.assertEqual(reply, struct.pack(">IB8sII", 0, client.OP_HELLO, client.HELLO_MAGIC, 0, 1))
        self.assertEqual(self.game.u32(28), self.game.u32(24), "the client consumed the game's packets")

    def test_invalid_ring_offsets_restart_discovery_without_writing(self) -> None:
        for offset in (24, 28, 32, 36):
            with self.subTest(offset=offset):
                self.setUp()
                self.game.set_u32(offset, client.RING)
                self.assert_corrupt_mailbox_is_untouched()

    def test_invalid_packet_lengths_restart_discovery_without_writing(self) -> None:
        # Include a valid check first: an invalid suffix must not acknowledge it.
        for raw in (b"\x00", b"\x00\x00", b"\x00\x04abcd", b"\x00\x20abc", b"\x07\xfe"):
            with self.subTest(raw=raw):
                self.setUp()
                self.send_check()
                head = self.game.u32(24)
                start = MAILBOX + client.HEADER + head
                self.game.ram[start:start + len(raw)] = raw
                self.game.set_u32(24, head + len(raw))
                self.assert_corrupt_mailbox_is_untouched()

    def assert_corrupt_mailbox_is_untouched(self) -> None:
        self.client.goals.add("OOT_GANON")
        before = bytes(self.game.ram)
        with mock.patch.object(client.bizhawk, "read", self.game.read), \
                mock.patch.object(client.bizhawk, "guarded_write", self.game.guarded_write):
            asyncio.run(self.client.exchange(self.ctx))
        self.assertEqual(bytes(self.game.ram), before)
        self.assertIsNone(self.client.mailbox)
        self.assertEqual(self.client.goals, {"OOT_GANON"})
        self.assertEqual(self.ctx.locations_checked, set())
        self.assertEqual(self.sent, [])

    def test_check_is_reported_and_acked(self) -> None:
        name = "OOT Kokiri Forest Kokiri Sword Chest"
        key = ootxmm_staticdata.OOTxMMCheckInfo["keys"][name]
        self.client.seq_net = 1
        self.game.send(struct.pack(">IBIBBBhhI", 7, client.OP_WAL, 42, client.WAL_ITEM, 2, 0, 0x12, 0, key))
        (ack,) = self.exchange()
        self.assertEqual(ack, struct.pack(">IBI", 1, client.OP_WAL_ACK, 42))
        self.assertEqual(self.sent, [{"cmd": "LocationChecks", "locations": [locations.LOCATION_NAME_TO_ID[name]]}])

    def test_query_gets_the_received_item(self) -> None:
        item_id = ootxmm_staticdata.OOTxMMItemIDs["OOT_HOOKSHOT"]
        self.ctx.items_received = [NetworkItem(item_id, 1, 2, 0)]
        self.client.seq_net = 1
        self.game.send(struct.pack(">IBI", 3, client.OP_WAL_QUERY, 0))
        (item,) = self.exchange()
        gi = client.GI_BY_ITEM_ID[item_id]
        self.assertEqual(item, struct.pack(">IBIBB8sBBhhI", 1, client.OP_WAL, 0, client.WAL_ITEM, client.OTHER_WORLD,
                                           b"Zelda\0\0\0", client.OUR_WORLD, 0, gi, 0, 0))

    def send_check(self) -> int:
        name = "OOT Kokiri Forest Kokiri Sword Chest"
        key = ootxmm_staticdata.OOTxMMCheckInfo["keys"][name]
        self.game.send(struct.pack(">IBIBBBhhI", 7, client.OP_WAL, 42,
                                   client.WAL_ITEM, 2, 0, 0x12, 0, key))
        return locations.LOCATION_NAME_TO_ID[name]

    def test_check_is_retained_when_socket_drops_before_send(self) -> None:
        location = self.send_check()

        async def disconnected_send(_msgs):
            pass  # CommonClient silently returns when its socket is closed.

        self.ctx.send_msgs = disconnected_send
        self.exchange()
        self.assertEqual(self.ctx.locations_checked, {location})

    def test_failed_send_keeps_packet_and_sequence_for_retry(self) -> None:
        location = self.send_check()
        self.client.seq_net = 1
        send_msgs = self.ctx.send_msgs

        async def failed_send(_msgs):
            raise ConnectionError("socket closed during send")

        self.ctx.send_msgs = failed_send
        with self.assertRaises(ConnectionError):
            self.exchange()
        self.assertEqual(self.game.u32(28), 0)
        self.assertEqual(self.client.seq_net, 1)
        self.assertEqual(self.ctx.locations_checked, {location})
        self.ctx.send_msgs = send_msgs
        (ack,) = self.exchange()
        self.assertEqual(ack, struct.pack(">IBI", 1, client.OP_WAL_ACK, 42))

    def test_full_ring_retries_without_losing_ack_or_sequence(self) -> None:
        self.send_check()
        self.client.seq_net = 1
        # Ring has only two free bytes: not enough for the framed WAL acknowledgement.
        self.game.set_u32(32, client.RING - 3)
        with mock.patch.object(client.bizhawk, "read", self.game.read), \
                mock.patch.object(client.bizhawk, "guarded_write", self.game.guarded_write):
            asyncio.run(self.client.exchange(self.ctx))
        self.assertEqual(self.game.u32(28), 0)
        self.assertEqual(self.client.seq_net, 1)
        self.assertEqual(self.sent, [])
        self.game.set_u32(36, client.RING - 3)
        (ack,) = self.exchange()  # Also exercises a reply wrapping around the ring boundary.
        self.assertEqual(ack, struct.pack(">IBI", 1, client.OP_WAL_ACK, 42))
        self.assertEqual(self.game.u32(28), self.game.u32(24))

    def test_boss_waits_for_server_confirmation_before_ack(self) -> None:
        async def unconfirmed_send(msgs):
            self.sent += msgs

        self.ctx.send_msgs = unconfirmed_send
        self.client.seq_net = 1
        self.defeat("OOT_GANON")
        self.assertEqual(self.game.u32(28), 0)
        self.assertEqual(self.client.seq_net, 1)
        self.assertFalse(self.ctx.finished_game)
        saved = next(msg for msg in self.sent if msg["cmd"] == "Set")
        self.client.on_package(self.ctx, "Connected", {})
        self.exchange()
        self.assertEqual(self.game.u32(28), 0, "reconnect still must not acknowledge an unconfirmed boss")
        self.client.on_package(self.ctx, "SetReply", {"key": saved["key"], "value": {"OOT_GANON": True}})
        (ack,) = self.exchange()
        self.assertEqual(ack, struct.pack(">IBI", 1, client.OP_WAL_ACK, 1))
        self.assertTrue(self.ctx.finished_game)

    def test_query_past_the_end_gets_nothing(self) -> None:
        self.game.send(struct.pack(">IBI", 3, client.OP_WAL_QUERY, 0))
        self.assertEqual(self.exchange(), [])

    def test_ganon_is_the_goal(self) -> None:
        self.client.seq_net = 1
        gi = ootxmm_staticdata.OOTxMMCheckInfo["goalGi"]["OOT_GANON"]
        self.game.send(struct.pack(">IBIBBBhhI", 7, client.OP_WAL, 1, client.WAL_ITEM, client.OUR_WORLD, 0, gi, 0, 0))
        self.exchange()
        self.assertTrue(self.ctx.finished_game)
        self.assertEqual(self.sent[-1]["cmd"], "StatusUpdate")

    def defeat(self, event: str) -> None:
        gi = ootxmm_staticdata.OOTxMMCheckInfo["goalGi"][event]
        self.game.send(struct.pack(">IBIBBBhhI", 7, client.OP_WAL, 1, client.WAL_ITEM,
                                   client.OUR_WORLD, 0, gi, 0, 0))
        self.exchange()

    def test_both_survives_client_restart_in_either_order(self) -> None:
        for first, second in [("OOT_GANON", "MM_MAJORA"), ("MM_MAJORA", "OOT_GANON")]:
            with self.subTest(first=first):
                self.setUp()
                self.ctx.slot_data["settings"]["goal"] = "both"
                self.defeat(first)
                self.assertFalse(self.ctx.finished_game)
                saved = next(msg for msg in self.sent if msg["cmd"] == "Set")
                self.assertEqual(saved["operations"], [{"operation": "update", "value": {first: True}}])
                self.client = client.OOTxMMClient()
                self.client.mailbox = MAILBOX
                self.exchange()
                self.client.on_package(self.ctx, "Retrieved", {"keys": {saved["key"]: {first: True}}})
                self.defeat(second)
                self.assertTrue(self.ctx.finished_game)

    def test_game_switch_preserves_goals(self) -> None:
        self.ctx.slot_data["settings"]["goal"] = "both"
        self.defeat("OOT_GANON")
        self.client.reset()
        self.client.mailbox = MAILBOX
        self.defeat("MM_MAJORA")
        self.assertTrue(self.ctx.finished_game)

    def test_stale_mailbox_restarts_discovery_and_preserves_goals(self) -> None:
        self.client.goals.add("OOT_GANON")
        with mock.patch.object(client.time, "monotonic", return_value=10):
            self.exchange()
        with mock.patch.object(client.time, "monotonic", return_value=14):
            self.exchange()
        self.assertIsNone(self.client.mailbox)
        self.assertEqual(self.client.scan_pos, 0)
        self.assertEqual(self.client.goals, {"OOT_GANON"})
        self.assertEqual(self.game.u32(16), 1, "the stale mailbox stays intact")
        other = 0x8000
        self.game.ram.extend(bytes(0x10000 - len(self.game.ram)))
        self.game.ram[other:other + 16] = client.MAGIC
        with mock.patch.object(client.bizhawk, "read", self.game.read), \
                mock.patch.object(client.bizhawk, "get_memory_size", mock.AsyncMock(return_value=0x10000)):
            asyncio.run(self.client.find_mailbox(self.ctx))
            asyncio.run(self.client.find_mailbox(self.ctx))
            struct.pack_into(">I", self.game.ram, other + 20, 1)
            asyncio.run(self.client.find_mailbox(self.ctx))
        self.assertEqual(self.client.mailbox, other, "discovery selects the new game's moving mailbox")

    def discover(self, polls: int, size: int = 0x10000) -> None:
        self.game.ram.extend(bytes(size - len(self.game.ram)))
        with mock.patch.object(client.bizhawk, "read", self.game.read), \
                mock.patch.object(client.bizhawk, "get_memory_size", mock.AsyncMock(return_value=size)):
            for _ in range(polls):
                asyncio.run(self.client.find_mailbox(self.ctx))

    def test_mailbox_at_the_end_of_a_scan_read_is_found(self) -> None:
        self.client.reset()
        address = client.SCAN_CHUNK - 16
        self.game.ram.extend(bytes(0x10000 - len(self.game.ram)))
        self.game.ram[address:address + 16] = client.MAGIC
        self.discover(2)
        struct.pack_into(">I", self.game.ram, address + 20, 1)
        self.discover(1)
        self.assertEqual(self.client.mailbox, address)

    def test_known_mailbox_is_found_again_without_a_scan(self) -> None:
        self.client.known_mailboxes = [0x8000, MAILBOX]
        self.client.reset()
        size = mock.AsyncMock(return_value=0x10000)
        self.game.ram.extend(bytes(0x10000 - len(self.game.ram)))
        with mock.patch.object(client.bizhawk, "read", self.game.read), \
                mock.patch.object(client.bizhawk, "get_memory_size", size), \
                mock.patch.object(client.time, "monotonic", return_value=10):
            for _ in range(2):  # finds the copy, then reads its alive counter
                asyncio.run(self.client.find_mailbox(self.ctx))
            self.game.set_u32(20, 7)
            asyncio.run(self.client.find_mailbox(self.ctx))
        self.assertEqual(self.client.mailbox, MAILBOX)
        size.assert_not_called()

    def test_waits_at_known_addresses_while_a_game_loads_then_scans(self) -> None:
        self.client.known_mailboxes = [0x8000]
        self.client.reset()
        size = mock.AsyncMock(return_value=0x10000)
        self.game.ram.extend(bytes(0x10000 - len(self.game.ram)))
        with mock.patch.object(client.bizhawk, "read", self.game.read), \
                mock.patch.object(client.bizhawk, "get_memory_size", size):
            for now in (0, 5, 19):
                with mock.patch.object(client.time, "monotonic", return_value=now):
                    asyncio.run(self.client.find_mailbox(self.ctx))
            size.assert_not_called()
            self.assertEqual(self.client.scan_pos, 0)
            with mock.patch.object(client.time, "monotonic", return_value=client.KNOWN_MAILBOX_WAIT_SECONDS):
                asyncio.run(self.client.find_mailbox(self.ctx))
        size.assert_called()
        self.assertIn(MAILBOX, self.client.candidates, "the full scan found the mailbox elsewhere")

    def test_found_mailbox_is_remembered(self) -> None:
        self.client.reset()
        self.discover(2)
        self.game.set_u32(20, 3)
        self.discover(1)
        self.assertEqual(self.client.mailbox, MAILBOX)
        self.client.reset()
        self.assertEqual(self.client.known_mailboxes, [MAILBOX])

    def test_rom_without_mailbox_warns_once(self) -> None:
        self.client.reset()
        self.game.ram[MAILBOX:MAILBOX + 16] = bytes(16)
        polls_per_scan = 0x10000 // (client.SCAN_CHUNK * client.SCAN_READS_PER_POLL) + 2  # scan, then restart
        with self.assertLogs(client.logger, "WARNING") as logs:
            self.discover(polls_per_scan * (client.EMPTY_SCANS_BEFORE_WARNING + 2))
        self.assertEqual(logs.output, [f"WARNING:Client:{client.NO_MAILBOX_WARNING}"])

    def test_patched_rom_does_not_warn(self) -> None:
        self.client.reset()
        polls_per_scan = 0x10000 // (client.SCAN_CHUNK * client.SCAN_READS_PER_POLL) + 2
        with mock.patch.object(client.logger, "warning") as warning, \
                mock.patch.object(client.time, "monotonic", side_effect=range(0, 1000, 10)):
            self.discover(polls_per_scan * (client.EMPTY_SCANS_BEFORE_WARNING + 2))
        warning.assert_not_called()

    def test_scan_repeats_when_every_copy_found_is_stale(self) -> None:
        self.client.reset()
        with mock.patch.object(client.time, "monotonic", return_value=10):
            self.discover(2)
        self.assertEqual(list(self.client.candidates), [MAILBOX])
        with mock.patch.object(client.time, "monotonic", return_value=11):
            self.discover(1)
        self.assertIsNone(self.client.scan_pos, "still watching the copy it found")
        with mock.patch.object(client.time, "monotonic", return_value=14):
            self.discover(1)
        self.assertEqual(self.client.scan_pos, 0)

        live = 0x8000
        self.game.ram[live:live + 16] = client.MAGIC
        with mock.patch.object(client.time, "monotonic", return_value=14):
            self.discover(2)
        struct.pack_into(">I", self.game.ram, live + 20, 1)
        with mock.patch.object(client.time, "monotonic", return_value=15):
            self.discover(1)
        self.assertEqual(self.client.mailbox, live)

    def test_mailbox_replaced_between_read_and_write_is_left_alone(self) -> None:
        self.game.send(struct.pack(">IB", 0, client.OP_HELLO) + client.HELLO_MAGIC + bytes(49))
        real_read = self.game.read

        async def read_then_switch(ctx, read_list):
            result = await real_read(ctx, read_list)
            self.game.ram[MAILBOX:MAILBOX + 0x40] = bytes(0x40)
            return result

        self.game.read = read_then_switch
        self.exchange_without_receive()
        self.assertEqual(bytes(self.game.ram[MAILBOX:MAILBOX + 0x40]), bytes(0x40))
        self.assertIsNone(self.client.mailbox)

    def exchange_without_receive(self) -> None:
        with mock.patch.object(client.bizhawk, "read", self.game.read), \
                mock.patch.object(client.bizhawk, "guarded_write", self.game.guarded_write):
            asyncio.run(self.client.exchange(self.ctx))

    def test_server_loss_detaches_once_and_only_from_the_mailbox(self) -> None:
        self.ctx.server = None
        with mock.patch.object(client.bizhawk, "guarded_write", self.game.guarded_write):
            asyncio.run(self.client.game_watcher(self.ctx))
        self.assertEqual(self.game.u32(16), 0)
        self.assertIsNone(self.client.mailbox)

        self.client.mailbox = MAILBOX
        self.game.set_u32(16, 1)
        self.game.ram[MAILBOX:MAILBOX + 16] = bytes(16)
        with mock.patch.object(client.bizhawk, "guarded_write", self.game.guarded_write):
            asyncio.run(self.client.game_watcher(self.ctx))
        self.assertEqual(self.game.u32(16), 1, "another game's data at the old address stays intact")

    def test_lost_emulator_does_not_end_the_watcher(self) -> None:
        self.ctx.server = None
        for error in (client.bizhawk.RequestFailedError("reset"), client.bizhawk.NotConnectedError()):
            self.client.mailbox = MAILBOX
            with mock.patch.object(client.bizhawk, "guarded_write", mock.AsyncMock(side_effect=error)):
                asyncio.run(self.client.game_watcher(self.ctx))

    def test_advancing_mailbox_keeps_connection(self) -> None:
        for now, alive in [(10, 0), (12, 1), (14, 2), (16, 0)]:
            self.game.set_u32(20, alive)
            with mock.patch.object(client.time, "monotonic", return_value=now):
                self.exchange()
            self.assertEqual(self.client.mailbox, MAILBOX)

    def test_other_slot_or_seed_does_not_inherit_goals(self) -> None:
        self.defeat("OOT_GANON")
        old_key = self.client.goal_key
        self.ctx.slot = 2
        self.exchange()
        self.client.on_package(self.ctx, "Retrieved", {"keys": {old_key: {"OOT_GANON": True}}})
        self.assertEqual(self.client.goals, set())
        self.client.goals.add("MM_MAJORA")
        self.ctx.server_seed_name = "another-seed"
        self.exchange()
        self.assertEqual(self.client.goals, set())

    def test_delayed_restore_merges_with_new_boss(self) -> None:
        self.ctx.slot_data["settings"]["goal"] = "both"
        self.defeat("MM_MAJORA")
        self.client.on_package(self.ctx, "Retrieved", {
            "keys": {self.client.goal_key: {"OOT_GANON": True}}})
        self.exchange()
        self.assertTrue(self.ctx.finished_game)

    def test_reconnect_reloads_and_rejects_other_slot_reply(self) -> None:
        self.defeat("OOT_GANON")
        self.client.on_package(self.ctx, "Connected", {})
        self.exchange()
        self.assertEqual(self.client.goals, set())
        self.client.on_package(self.ctx, "SetReply", {"key": "other-slot", "value": {"OOT_GANON": True}})
        self.assertEqual(self.client.goals, set())
        self.client.on_package(self.ctx, "SetReply", {
            "key": self.client.goal_key, "value": {"OOT_GANON": True}})
        self.assertEqual(self.client.goals, {"OOT_GANON"})
