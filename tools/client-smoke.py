"""Exercise the client against a loopback AP server and simulated game mailboxes.

Run with Archipelago's Python: client-smoke.py --archipelago <checkout> --seed <two-player .archipelago>.
Uses a temporary server save, never the group's live save. Both slots must use goal: both.
"""
import argparse
import asyncio
import functools
import logging
import os
from pathlib import Path
import struct
import sys
import tempfile
from unittest import mock
import zlib


async def run(args):
    import websockets
    import CommonClient
    import MultiServer
    import Utils
    from NetUtils import ClientStatus
    from worlds.ootxmm import client
    from worlds.ootxmm.test.test_client import FakeGame, MAILBOX

    class Peer(CommonClient.CommonContext):
        game = "OOTxMM"
        items_handling = 0b101
        want_slot_data = True

        def __init__(self, address, name):
            super().__init__(address, None)
            self.auth = name
            self.slot_name = name
            self.bizhawk_ctx = None
            self.handler = client.OOTxMMClient()
            self.handler.mailbox = MAILBOX
            self.mail = FakeGame()
            self.mail.set_u32(16, 1)

        async def server_auth(self, password_requested=False):
            self.auth = self.slot_name
            await self.send_connect()

        def on_package(self, cmd, data):
            if cmd == "Connected":
                self.slot_data = data["slot_data"]
            self.handler.on_package(self, cmd, data)

        async def poll(self):
            with mock.patch.object(client.bizhawk, "read", self.mail.read), \
                    mock.patch.object(client.bizhawk, "guarded_write", self.mail.guarded_write):
                await self.handler.exchange(self)
            return self.mail.receive()

        async def pickup(self, location=None, boss=None):
            key = key_by_location[location] if location is not None else 0
            gi = goal_gi[boss] if boss else 0x12
            self.mail.send(struct.pack(">IBIBBBhhI", 1, client.OP_WAL, 42, client.WAL_ITEM,
                client.OUR_WORLD if boss else client.OTHER_WORLD, 0, gi, 0, key))
            await self.poll()
            if boss:
                async with asyncio.timeout(15):
                    while boss not in self.handler.goals:
                        await asyncio.sleep(0.01)
                await self.poll()

    async def until(predicate, label):
        async with asyncio.timeout(15):
            while not predicate():
                await asyncio.sleep(0.01)
        logging.info("PASS: %s", label)

    key_by_location = {location: key for key, location in client.LOCATION_BY_KEY.items()}
    goal_gi = {event: gi for gi, event in client.GOAL_GI.items()}
    peers = []
    server = None
    context = None
    with tempfile.TemporaryDirectory(prefix="ootxmm-smoke-") as scratch:
        def load_server(saved=False):
            ctx = MultiServer.Context("127.0.0.1", 0, "", "", 1, 10, False)
            ctx.load(str(args.seed))
            ctx.save_filename = str(Path(scratch) / "test.apsave")
            if saved:
                ctx.set_save(Utils.restricted_loads(zlib.decompress(Path(ctx.save_filename).read_bytes())))
            return ctx

        async def listen(ctx):
            return await websockets.serve(functools.partial(MultiServer.server, ctx=ctx), "127.0.0.1", 0)

        async def connect(slot):
            port = server.sockets[0].getsockname()[1]
            peer = Peer(f"ws://127.0.0.1:{port}", context.player_names[0, slot])
            peers.append(peer)
            peer.server_task = asyncio.create_task(CommonClient.server_loop(peer))
            await until(lambda: peer.slot == slot, f"slot {slot} login")
            assert peer.slot_data["settings"]["goal"] == "both", "Use goal: both for both slots"
            peer.mail.send(struct.pack(">IB", 0, client.OP_HELLO) + client.HELLO_MAGIC + bytes(49))
            await peer.poll()
            return peer

        try:
            context = load_server()
            server = await listen(context)
            one, two = await connect(1), await connect(2)
            for sender, receiver in [(one, two), (two, one)]:
                check, placement = next((loc, item) for loc, item in context.locations[sender.slot].items()
                                        if item[1] == receiver.slot and loc in key_by_location)
                await sender.pickup(location=check)
                await until(lambda: check in context.location_checks[0, sender.slot], "server records pickup")
                await until(lambda: any(i.location == check and i.player == sender.slot
                                       for i in receiver.items_received), "remote item delivered")
                index = next(i for i, item in enumerate(receiver.items_received)
                             if item.location == check and item.player == sender.slot)
                receiver.mail.send(struct.pack(">IBI", 1, client.OP_WAL_QUERY, index))
                replies = await receiver.poll()
                packet = next(p for p in replies if p[4] == client.OP_WAL)
                assert struct.unpack_from(">h", packet, 21)[0] == client.GI_BY_ITEM_ID[placement[0]]
                count = len(receiver.items_received)
                await sender.pickup(location=check)
                await sender.send_msgs([{"cmd": "Sync"}])
                await asyncio.sleep(0.1)
                assert len(receiver.items_received) == count, "Repeated check duplicated an item"
            # CommonClient must replay a check acknowledged while its socket was closed.
            pending = next(loc for loc in context.locations[1]
                           if loc in key_by_location and loc not in context.location_checks[0, 1])
            async def dropped_send(_msgs):
                pass
            with mock.patch.object(one, "send_msgs", dropped_send):
                await one.pickup(location=pending)
            assert pending in one.locations_checked
            assert pending not in context.location_checks[0, 1]
            await one.disconnect()
            one.server_task = asyncio.create_task(CommonClient.server_loop(one))
            await until(lambda: pending in context.location_checks[0, 1], "reconnect replays pending check")
            for peer, boss in [(one, "OOT_GANON"), (two, "MM_MAJORA")]:
                await peer.pickup(boss=boss)
                await until(lambda: context.stored_data.get(peer.handler.goal_key, {}).get(boss), "first boss stored")
                assert context.client_game_state[0, peer.slot] != ClientStatus.CLIENT_GOAL
            for peer in peers:
                await peer.shutdown()
            peers.clear()
            server.close()
            await server.wait_closed()
            assert context._save(), "Server save failed"
            context = load_server(saved=True)
            server = await listen(context)
            one, two = await connect(1), await connect(2)
            for peer, first, second in [(one, "OOT_GANON", "MM_MAJORA"), (two, "MM_MAJORA", "OOT_GANON")]:
                await until(lambda: first in peer.handler.goals, "boss restored after server/client restart")
                assert second not in peer.handler.goals, "Boss progress leaked between slots"
                peer.handler.reset()
                peer.handler.mailbox = MAILBOX
                peer.mail.send(struct.pack(">IB", 0, client.OP_HELLO) + client.HELLO_MAGIC + bytes(49))
                await peer.poll()
                await peer.pickup(boss=second)
                await until(lambda: context.client_game_state[0, peer.slot] == ClientStatus.CLIENT_GOAL,
                            "both-boss goal completed after restart and mailbox reset")
            print("PASS: bidirectional checks/items, duplicate checks, reconnect replay, disk-save reload, "
                  "slot isolation and both boss orders (simulated mailboxes).")
        finally:
            for peer in peers:
                await peer.shutdown()
            if server:
                server.close()
                await server.wait_closed()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archipelago", type=Path, required=True)
    parser.add_argument("--seed", type=Path, required=True)
    args = parser.parse_args()
    args.seed = args.seed.resolve()
    sys.path.insert(0, str(args.archipelago.resolve()))
    os.environ["SKIP_REQUIREMENTS_UPDATE"] = "1"
    logging.basicConfig(level=logging.INFO)
    asyncio.run(run(args))
