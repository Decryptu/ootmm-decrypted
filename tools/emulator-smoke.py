"""Deliver remote items through the real BizHawk connector into a disposable gameplay state.

Run with AP's Python, --archipelago <checkout> --seed <two-player .archipelago>.
Open slot 1's matching ROM and connector first. Use a fresh test save, never a player's live save.
The other player's pickups are simulated on a temporary loopback server. Server persistence is opt-in and uses disposable files.
"""
import argparse
import asyncio
import functools
import json
import os
from pathlib import Path
import sys
import zlib

from mailbox_timing import MailboxTiming
from mailbox_load import MailboxLoad
from gameplay_connection import wait_for_rom


async def wait_for_scenario_result(path, timeout):
    """Wait for the scenario's complete result, without polling a closing core."""
    async with asyncio.timeout(timeout):
        while True:
            try:
                result = json.loads(path.read_text(encoding="utf-8"))
            except (FileNotFoundError, json.JSONDecodeError):
                await asyncio.sleep(0.125)
                continue
            if result.get("passed") is not True:
                raise AssertionError("Offline save scenario failed")
            return result


async def disconnect_game(peer, poll_game, bizhawk):
    mailbox, received_index = peer.handler.mailbox, peer.handler.last_query
    assert mailbox is not None, "Disconnect requires a live game mailbox"
    await peer.disconnect()
    await poll_game()
    # The disconnected watcher clears its cached address after notifying the game.
    header = await bizhawk.read(peer.bizhawk_ctx, [(mailbox + 16, 4, "RDRAM")])
    assert header[0] == bytes(4), "Game must see disconnected server"
    return received_index


class PickupInterruption:
    """Abort the real socket at one selected check's send boundary, once."""

    def __init__(self, peer, locations, accepted, boundary):
        self.peer, self.locations = peer, locations
        self.accepted, self.boundary = accepted, boundary
        self.evidence = None
        self.send = peer.send_msgs

    async def send_msgs(self, messages):
        checks = {loc for message in messages if message.get("cmd") == "LocationChecks"
                  for loc in message["locations"]} & self.locations
        if self.evidence is not None or not checks:
            return await self.send(messages)
        assert checks <= self.peer.locations_checked, "Pickup must be retained before its send"
        assert not checks & self.accepted(), "Interruption requires a new pickup"
        self.evidence = {"boundary": self.boundary, "locations": sorted(checks),
                         "retained_before_send": True}
        if self.boundary == "after-accept":
            await self.send(messages)
            async with asyncio.timeout(10):
                while not checks <= self.accepted():
                    await asyncio.sleep(0.01)
        socket = self.peer.server.socket
        # Suppress automatic retries until the observer has notified the game.
        self.peer.disconnected_intentionally = True
        socket.transport.abort()
        async with asyncio.timeout(10):
            await socket.wait_closed()
            await self.peer.disconnect()
        self.evidence["server_accepted_at_abort"] = checks <= self.accepted()
        assert self.evidence["server_accepted_at_abort"] == (self.boundary == "after-accept")
        if self.boundary == "before-send":
            # Exercise CommonClient's silent return when its socket has disappeared.
            await self.send(messages)


async def run(args):
    import CommonClient
    import MultiServer
    import Utils
    import websockets
    from NetUtils import ClientStatus, NetworkItem
    import worlds._bizhawk as bizhawk
    from worlds.ootxmm.client import OOTxMMClient
    if args.connector_port is not None:
        bizhawk.BIZHAWK_SOCKET_PORT_RANGE_START = args.connector_port

    class Peer(CommonClient.CommonContext):
        game = "OOTxMM"
        items_handling = 0b101
        want_slot_data = True

        def __init__(self, address, name):
            super().__init__(address, None)
            self.slot_name = name
            self.bizhawk_ctx = bizhawk.BizHawkContext()
            self.handler = OOTxMMClient()
            self.slot_data = None

        async def server_auth(self, password_requested=False):
            self.auth = self.slot_name
            await self.send_connect()

        def on_package(self, cmd, data):
            if cmd == "Connected":
                self.slot_data = data["slot_data"]
            self.handler.on_package(self, cmd, data)

    context = MultiServer.Context("127.0.0.1", 0, "", "", 1, 10, False)
    context.load(str(args.seed))
    if args.server_save_input:
        context.set_save(Utils.restricted_loads(zlib.decompress(args.server_save_input.read_bytes())))
    if args.server_save_output:
        if args.server_save_output.exists():
            raise ValueError("Refusing to overwrite a server save")
        context.save_filename = str(args.server_save_output)
    server = await websockets.serve(functools.partial(MultiServer.server, ctx=context), "127.0.0.1", 0)
    peer = Peer(f"ws://127.0.0.1:{server.sockets[0].getsockname()[1]}", context.player_names[0, 1])
    initial_checks = set(context.location_checks[0, 1])
    setup_grants = []
    last_goal_snapshot = None
    timing = MailboxTiming()
    load = MailboxLoad()
    mailbox_history = timing.history
    active_mailboxes = []
    verified_rom_sha1 = None
    pickup_interruption = None
    interruption_reconnected = False

    async def poll_game():
        nonlocal last_goal_snapshot, interruption_reconnected
        if peer.bizhawk_ctx.streams is None:
            if not await bizhawk.connect(peer.bizhawk_ctx):
                return
            print("Reconnected to BizHawk connector", flush=True)
        poll_started = timing.clock()
        try:
            await load.sample(peer, bizhawk)
            await peer.handler.game_watcher(peer)
            await load.sample(peer, bizhawk)
        except bizhawk.NotConnectedError:
            event = timing.observe(None, peer.handler.last_query, poll_started)
            if event is not None:
                print("Mailbox discovery:", event, flush=True)
            return
        if pickup_interruption and pickup_interruption.evidence and not interruption_reconnected:
            # The interrupted watcher may acknowledge its retained local check. Notify
            # the game of the closed socket before letting normal login resend it.
            mailbox = peer.handler.mailbox
            assert mailbox is not None
            await peer.handler.game_watcher(peer)
            flag = await bizhawk.read(peer.bizhawk_ctx, [(mailbox + 16, 4, "RDRAM")])
            assert flag[0] == bytes(4), "Game must observe the interrupted socket"
            pickup_interruption.evidence["connected_flag_cleared"] = True
            interruption_reconnected = True
            peer.server_task = asyncio.create_task(CommonClient.server_loop(peer))
        if args.expect_boss:
            snapshot = {"key": peer.handler.goal_key, "client_goals": sorted(peer.handler.goals),
                        "stored_goals": context.stored_data.get(peer.handler.goal_key, {}),
                        "server_finished": context.client_game_state[0, 1] == ClientStatus.CLIENT_GOAL}
            if snapshot != last_goal_snapshot:
                print("Goal observation:", snapshot, flush=True)
                last_goal_snapshot = snapshot
        mailbox = peer.handler.mailbox
        event = timing.observe(mailbox, peer.handler.last_query, poll_started)
        if event is not None:
            print("Mailbox discovery:", event, flush=True)
        if mailbox is not None and (not active_mailboxes or active_mailboxes[-1] != mailbox):
            active_mailboxes.append(mailbox)
        if (args.ready_file and not args.ready_file.exists()
                and mailbox is not None and peer.handler.last_query is not None):
            args.ready_file.write_text(json.dumps({"mailbox": mailbox,
                                                  "received_index": peer.handler.last_query,
                                                  "verified_connector_rom_sha1": verified_rom_sha1}), encoding="utf-8")

    try:
        async with asyncio.timeout(args.timeout):
            while not await bizhawk.connect(peer.bizhawk_ctx):
                await asyncio.sleep(0.25)
        verified_rom_sha1 = await wait_for_rom(peer, bizhawk, args.expected_rom_sha1)
        print("Connected to BizHawk N64 core:", (await bizhawk.get_cores(peer.bizhawk_ctx)).get("N64"), flush=True)
        peer.server_task = asyncio.create_task(CommonClient.server_loop(peer))
        async with asyncio.timeout(60):
            while peer.slot is None:
                await asyncio.sleep(0.05)
            while peer.handler.last_query is None:
                await poll_game()
                await asyncio.sleep(0.125)
        if args.grant_item:
            item_ids = context.item_names_for_game("OOTxMM")
            for name in args.grant_item:
                if name not in item_ids:
                    raise ValueError(f"Unknown setup item: {name}")
            for name in args.grant_item:
                MultiServer.send_items_to(context, 0, 1, NetworkItem(item_ids[name], -1, 0))
                setup_grants.append(name)
            MultiServer.send_new_items(context)
        if args.expect_check or args.expect_boss or args.grant_item:
            names = context.location_names["OOTxMM"]
            wanted = {loc for loc in context.locations[1] if names[loc] in args.expect_check}
            assert len(wanted) == len(set(args.expect_check)), "Unknown or inactive expected check"
            injected_checks = []

            def inject_remote_checks():
                checks = [loc for loc, item in context.locations[2].items()
                          if item[1] == 1 and loc not in context.location_checks[0, 2]][:args.inject_remote_count]
                assert len(checks) == args.inject_remote_count, "Not enough unused remote checks"
                MultiServer.register_location_checks(context, 0, 2, checks)
                return checks

            interruption = None
            if args.interrupt_pickup:
                assert not wanted & initial_checks, "Interrupted checks must be new"
                pickup_interruption = PickupInterruption(
                    peer, wanted, lambda: set(context.location_checks[0, 1]), args.interrupt_pickup)
                peer.send_msgs = pickup_interruption.send_msgs
            if args.save_offline:
                assert not wanted & initial_checks, "Pending checks must be absent from the restored server"
                if args.expect_received_index is not None:
                    assert peer.handler.last_query == args.expect_received_index, "Unexpected pre-disconnect receipt index"
                received_index_before = await disconnect_game(peer, poll_game, bizhawk)
                received_before = len(peer.items_received)
                await wait_for_scenario_result(args.ready_file.parent / "result.json", args.timeout)
                assert set(context.location_checks[0, 1]) == initial_checks, "Offline checks reached the server"
                assert len(peer.items_received) == received_before, "Offline client received items"
                if args.server_save_output:
                    assert context._save(), "Disposable server save failed"
                report = {"coverage": "assisted-gameplay", "passed": True,
                          "phase": "offline-save", "server_reloaded": bool(args.server_save_input),
                          "pending_checks_to_verify_after_cold_boot": args.expect_check,
                          "no_checks_reported_while_offline": True, "connected_flag_cleared": True,
                          "restored_checks": [names[loc] for loc in sorted(initial_checks)],
                          "new_checks": [], "setup_grants": [], "simulated_remote_checks": [],
                          "received_index_before_disconnect": received_index_before,
                          "verified_connector_rom_sha1": verified_rom_sha1}
                args.report.write_text(json.dumps(report, indent=2), encoding="utf-8")
                print("PASS: offline save phase; pending recovery requires a separate cold boot", flush=True)
                return
            if args.disconnect_seconds:
                before_disconnect = set(context.location_checks[0, 1])
                await disconnect_game(peer, poll_game, bizhawk)
                received_before = len(peer.items_received)
                if args.inject_remote_count:
                    injected_checks = inject_remote_checks()
                    assert len(MultiServer.get_received_items(context, 0, 1, False)) >= args.inject_remote_count, "Remote backlog was not queued"
                started = asyncio.get_running_loop().time()
                while asyncio.get_running_loop().time() - started < args.disconnect_seconds:
                    await poll_game()
                    await asyncio.sleep(0.125)
                assert set(context.location_checks[0, 1]) == before_disconnect, "Offline checks reached the server"
                assert len(peer.items_received) == received_before, "Disconnected client received server items"
                interruption = {"queued_remote_items": len(injected_checks),
                                "client_received_nothing_while_offline": True, "seconds": args.disconnect_seconds, "connected_flag_cleared": True,
                                "no_checks_reported_while_offline": True}
                peer.server_task = asyncio.create_task(CommonClient.server_loop(peer))
                async with asyncio.timeout(60):
                    while peer.slot is None:
                        await asyncio.sleep(0.05)
            if args.inject_remote_count and not injected_checks:
                injected_checks = inject_remote_checks()
            def goals_verified():
                stored = context.stored_data.get(peer.handler.goal_key, {})
                return all(stored.get(boss) is True and boss in peer.handler.goals for boss in args.expect_boss)

            async with asyncio.timeout(args.timeout):
                previous = set()
                while (not wanted <= context.location_checks[0, 1]
                       or not goals_verified()
                       or len(active_mailboxes) - 1 < args.min_game_switches
                       or (args.expect_received_index is not None and peer.handler.last_query != args.expect_received_index)):
                    await poll_game()
                    current = set(context.location_checks[0, 1])
                    if current != previous:
                        print("Observed game checks:", [names[loc] for loc in sorted(current)], flush=True)
                        previous = current
                    await asyncio.sleep(0.125)
                for _ in range(16):
                    await poll_game()
                    if args.interrupt_pickup:
                        assert set(context.location_checks[0, 1]) == initial_checks | wanted, "Unexpected check during recovery"
                        if args.expect_received_index is not None:
                            assert peer.handler.last_query == args.expect_received_index, "Receipt index changed after recovery"
                    await asyncio.sleep(0.125)
            assert goals_verified(), "Boss progress was not confirmed by server storage"
            if args.interrupt_pickup:
                assert pickup_interruption.evidence and interruption_reconnected, "Pickup interruption did not run"
                assert peer.slot == 1 and peer.handler.last_query is not None, "Client did not recover"
                interruption = pickup_interruption.evidence
                interruption["reconnected"] = True
                interruption["stable_polls"] = 16
            if args.expect_boss:
                expected_finished = peer.handler.goal_reached(peer)
                assert (context.client_game_state[0, 1] == ClientStatus.CLIENT_GOAL) == expected_finished, "Server completion disagrees with configured goal"
            if args.expect_received_index is not None:
                assert peer.handler.last_query == args.expect_received_index, "Unexpected received index"
            if args.server_save_output:
                assert context._save(), "Disposable server save failed"
            observed = sorted(context.location_checks[0, 1])
            for loc in wanted:
                item, recipient, _flags = context.locations[1][loc]
                queued = MultiServer.get_received_items(context, 0, recipient, True)
                assert sum(entry.location == loc and entry.player == 1 and entry.item == item
                           for entry in queued) == 1, "Pickup must queue exactly one award"
            report = {"coverage": "assisted-gameplay", "seed": str(args.seed), "slot": 1,
                      "server_reloaded": bool(args.server_save_input),
                      "interruption": interruption,
                      "setup_grants": setup_grants,
                      "simulated_remote_checks": [{"location": context.location_names["OOTxMM"][loc],
                                                   "item": context.item_names["OOTxMM"][context.locations[2][loc][0]]}
                                                  for loc in injected_checks],
                      "restored_checks": [names[loc] for loc in sorted(initial_checks)],
                      "new_checks": [names[loc] for loc in observed if loc not in initial_checks],
                      "expected_bosses": args.expect_boss,
                      "stored_goals": context.stored_data.get(peer.handler.goal_key, {}),
                      "server_finished": context.client_game_state[0, 1] == ClientStatus.CLIENT_GOAL,
                      "expected": args.expect_check, "observed": [names[loc] for loc in observed],
                      "awards": [{"location": names[loc], "recipient": context.locations[1][loc][1],
                                  "item": context.item_names["OOTxMM"][context.locations[1][loc][0]]}
                                 for loc in observed], "received_index": peer.handler.last_query,
                      "mailbox_history": mailbox_history, "active_mailboxes": active_mailboxes,
                      "mailbox_timing": timing.report(), "mailbox_load": load.report(),
                      "rom_mailbox_directory": peer.handler.rom_mailboxes,
                      "verified_connector_rom_sha1": verified_rom_sha1,
                      "game_switches": max(0, len(active_mailboxes) - 1), "award_count_verified": True, "passed": wanted <= set(observed)}
            if args.report:
                args.report.write_text(json.dumps(report, indent=2), encoding="utf-8")
            print("PASS: server checks and game assertions verified:", report, flush=True)
            return
        assert peer.handler.last_query == 0, "Use a fresh disposable save with no received items"
        checks = [loc for loc, item in context.locations[2].items() if item[1] == 1][:3]
        assert len(checks) == 3, "Seed must have at least three remote items for slot 1 in slot 2"
        MultiServer.register_location_checks(context, 0, 2, checks)
        async with asyncio.timeout(90):
            while peer.handler.last_query < len(checks):
                await poll_game()
                await asyncio.sleep(0.125)
        print(f"PASS: real game consumed {peer.handler.last_query} remote items through the RAM mailbox.", flush=True)
        for item in peer.items_received:
            print("Received:", context.item_names["OOTxMM"][item.item], flush=True)
        await peer.disconnect()
        await poll_game()  # Let the game see the lost server connection.
        await asyncio.sleep(0.5)
        peer.server_task = asyncio.create_task(CommonClient.server_loop(peer))
        async with asyncio.timeout(60):
            while peer.slot is None:
                await asyncio.sleep(0.05)
            peer.handler.last_query = None
            while peer.handler.last_query is None:
                await poll_game()
                await asyncio.sleep(0.125)
            for _ in range(8):
                await poll_game()
                await asyncio.sleep(0.125)
        assert peer.handler.last_query == len(checks), "Reconnect duplicated a received item"
        print("PASS: server reconnect resumed at the same received index without duplicates.", flush=True)
    except Exception as error:
        if args.report:
            names = context.location_names["OOTxMM"]
            report = {
                "coverage": "assisted-gameplay" if args.expect_check or args.expect_boss or args.grant_item else "protocol",
                "passed": False,
                "interruption": pickup_interruption.evidence if pickup_interruption else None,
                "setup_grants": setup_grants,
                "error": {"type": type(error).__name__, "message": str(error)},
                "seed": str(args.seed), "slot": 1,
                "expected": args.expect_check, "expected_bosses": args.expect_boss,
                "observed": [names[loc] for loc in sorted(context.location_checks[0, 1])],
                "stored_goals": context.stored_data.get(peer.handler.goal_key, {}),
                "server_finished": context.client_game_state[0, 1] == ClientStatus.CLIENT_GOAL,
                "received_index": peer.handler.last_query,
                "server_item_count": len(peer.items_received),
                "mailbox_history": mailbox_history, "active_mailboxes": active_mailboxes,
                "mailbox_timing": timing.report(), "mailbox_load": load.report(),
                "rom_mailbox_directory": peer.handler.rom_mailboxes,
                "verified_connector_rom_sha1": verified_rom_sha1,
                "server_reloaded": bool(args.server_save_input),
            }
            args.report.write_text(json.dumps(report, indent=2), encoding="utf-8")
        raise
    finally:
        print("Final received index:", peer.handler.last_query, "server items:", len(peer.items_received), flush=True)
        if peer.handler.mailbox is not None and peer.bizhawk_ctx.streams is not None:
            try:
                await bizhawk.write(peer.bizhawk_ctx, [(peer.handler.mailbox + 16, [0, 0, 0, 0], "RDRAM")])
            except (bizhawk.NotConnectedError, bizhawk.RequestFailedError):
                print("Emulator connector already closed during cleanup", flush=True)
        bizhawk.disconnect(peer.bizhawk_ctx)
        await peer.shutdown()
        server.close()
        await server.wait_closed()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archipelago", type=Path, required=True)
    parser.add_argument("--seed", type=Path, required=True)
    parser.add_argument("--expect-check", action="append", default=[], help="Observe actual pickups; do not inject remote checks")
    parser.add_argument("--expect-boss", action="append", default=[], choices=("OOT_GANON", "MM_MAJORA"), help="Observe real boss packets and confirmed server storage")
    parser.add_argument("--min-game-switches", type=int, default=0)
    parser.add_argument("--disconnect-seconds", type=float, default=0)
    parser.add_argument("--interrupt-pickup", choices=("before-send", "after-accept"))
    parser.add_argument("--save-offline", action="store_true", help="Disconnect after attachment until the scenario exits; verify pending checks in a separate cold boot")
    parser.add_argument("--grant-item", action="append", default=[], help="Explicit diagnostic item grant through the temporary server; no source pickup coverage")
    parser.add_argument("--inject-remote-count", type=int, default=0)
    parser.add_argument("--expect-received-index", type=int)
    parser.add_argument("--server-save-input", type=Path)
    parser.add_argument("--server-save-output", type=Path)
    parser.add_argument("--report", type=Path)
    parser.add_argument("--connector-port", type=int)
    parser.add_argument("--timeout", type=float, default=90)
    parser.add_argument("--expected-rom-sha1", help="Require the connector to expose this exact ROM")
    parser.add_argument("--ready-file", type=Path, help="Signal the first live mailbox query to the scenario")
    args = parser.parse_args()
    if args.interrupt_pickup and (not args.expect_check or args.save_offline or args.disconnect_seconds
                                  or args.inject_remote_count or args.grant_item or args.expect_boss):
        parser.error("Pickup interruption requires real pickup assertions and no other stimuli")
    if args.save_offline and (not args.expect_check or not args.ready_file or not args.report
                             or args.disconnect_seconds or args.inject_remote_count or args.grant_item or args.expect_boss):
        parser.error("Offline save requires pickup assertions, ready/report files and no other stimuli")
    if args.min_game_switches < 0 or (args.min_game_switches and not args.expect_check):
        parser.error("--min-game-switches requires nonnegative count and pickup assertions")
    if args.inject_remote_count < 0 or (args.expect_received_index is not None and args.expect_received_index < 0):
        parser.error("Receipt counts must be nonnegative")
    if (args.inject_remote_count or args.expect_received_index is not None) and not (args.expect_check or args.expect_boss or args.grant_item):
        parser.error("Receipt assertions require observer mode")
    if args.inject_remote_count and args.expect_received_index is None:
        parser.error("Simulated remote checks require an expected received index")
    if not 0 <= args.disconnect_seconds <= 60 or (args.disconnect_seconds and not args.expect_check):
        parser.error("Disconnect duration must be 0-60 seconds and requires pickup assertions")
    if args.grant_item and args.expect_received_index is None:
        parser.error("Diagnostic grants require --expect-received-index")
    if args.connector_port is not None and not 1024 <= args.connector_port <= 65530:
        parser.error("Connector range start must be between 1024 and 65530")
    args.seed = args.seed.resolve()
    sys.path.insert(0, str(args.archipelago.resolve()))
    os.environ["SKIP_REQUIREMENTS_UPDATE"] = "1"
    asyncio.run(run(args))
