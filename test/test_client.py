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

    async def write(self, _ctx, write_list):
        for address, data, _ in write_list:
            self.ram[address:address + len(data)] = bytes(data)


class TestClientProtocol(unittest.TestCase):
    def setUp(self) -> None:
        self.game = FakeGame()
        self.game.set_u32(16, 1)
        self.client = client.OOTxMMClient()
        self.client.mailbox = MAILBOX
        self.sent: list[dict] = []

        async def send_msgs(msgs):
            self.sent += msgs
        self.ctx = SimpleNamespace(
            bizhawk_ctx=None, items_received=[], checked_locations=set(), finished_game=False,
            player_names={2: "Zelda"}, slot_data={"settings": {"goal": "ganon"}}, send_msgs=send_msgs)

    def exchange(self) -> list[bytes]:
        with mock.patch.object(client.bizhawk, "read", self.game.read), \
                mock.patch.object(client.bizhawk, "write", self.game.write):
            asyncio.run(self.client.exchange(self.ctx))
        return self.game.receive()

    def test_hello(self) -> None:
        self.game.send(struct.pack(">IB", 0, client.OP_HELLO) + client.HELLO_MAGIC + bytes(49))
        (reply,) = self.exchange()
        self.assertEqual(reply, struct.pack(">IB8sII", 0, client.OP_HELLO, client.HELLO_MAGIC, 0, 1))
        self.assertEqual(self.game.u32(28), self.game.u32(24), "the client consumed the game's packets")

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
