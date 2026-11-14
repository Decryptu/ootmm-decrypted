"""Run two isolated gameplay scenarios against one disposable Archipelago server.

Use Archipelago's Python. The JSON plan supplies seed, emulator, config, connector,
and two players (slot, rom, placements, scenario, state or save_ram or fresh_boot,
checks, received_index). Paths are relative to the working directory.
Only actual game packets report checks; this tool never injects awards.
"""
import argparse
import asyncio
import functools
import hashlib
import json
import logging
import os
from pathlib import Path
import subprocess
import sys
import time
import zlib

from gameplay_connection import verify_pickup_award, wait_for_rom
from mailbox_load import MailboxLoad


def validate_backlog(backlog, players, stage_names):
    if backlog is None:
        return
    if (type(backlog.get("slot")) is not int or backlog["slot"] not in (1, 2)
            or backlog.get("disconnect_stage") not in stage_names
            or not isinstance(backlog.get("checks"), list) or not backlog["checks"]
            or any(not isinstance(check, str) for check in backlog["checks"])
            or len(set(backlog["checks"])) != len(backlog["checks"])):
        raise ValueError("Backlog requires a recipient, disconnect stage and unique source checks")
    source = next(p for p in players if p["slot"] == 3 - backlog["slot"])
    if not set(backlog["checks"]) <= set(source["checks"]):
        raise ValueError("Backlog sources must be expected checks from the other slot")


def stage_ready(stage, observations):
    """Require every explicit condition from the latest successful live queries."""
    return all(condition["capture"] in observations[condition["slot"]]["captures"]
               and observations[condition["slot"]]["game"] == condition["game"]
               and observations[condition["slot"]]["received_index"] == condition["received_index"]
               and set(condition.get("checks", [])) <= set(observations[condition["slot"]]["checks"])
               for condition in stage["players"])


def validate_restart(stage, stage_names, backlog):
    if stage is not None and (not isinstance(stage, str) or stage not in stage_names or backlog):
        raise ValueError("Server restart requires a declared stage and no backlog outage")


def expected_sources(players, locations, names, slot_set):
    wanted = {}
    remote_targets = set()
    for player in players:
        slot = player["slot"]
        wanted[slot] = {loc for loc in locations[slot] if names[loc] in player["checks"]}
        assert len(wanted[slot]) == len(set(player["checks"])), "Unknown expected source check"
        for loc in wanted[slot]:
            _, recipient, _ = locations[slot][loc]
            if recipient != slot:
                remote_targets.update(slot_set(recipient))
    for player in players:
        if player["received_index"] > 0:
            assert player["slot"] in remote_targets, "Receipt target needs an expected remote source"
    return wanted


def completed_captures(path):
    if not path.exists():
        return []
    captures = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        if '"capture"' not in line:
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue  # The emulator may be flushing the final line concurrently.
        if event.get("event") == "capture":
            captures.add(event["name"])
    return sorted(captures)


def verify_receipt_count(starting_items, received_items, expected_index):
    """Match the client's starting-inventory prefix plus remote delivery queue."""
    assert len(starting_items) + len(received_items) == expected_index, "Unexpected starting/remote item total"


async def run(args):
    import CommonClient
    import MultiServer
    import websockets
    import Utils
    import worlds._bizhawk as bizhawk
    from worlds.ootxmm.client import MAGIC, OOTxMMClient

    plan = json.loads(args.plan.read_text(encoding="utf-8"))
    players = plan["players"]
    if sorted(p["slot"] for p in players) != [1, 2]:
        raise ValueError("Plan must contain slots 1 and 2 exactly once")
    stages = plan.get("stages", [])
    backlog = plan.get("backlog")
    stage_names = set()
    for stage in stages:
        name = stage["name"]
        if not name or any(c not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_" for c in name) or name in stage_names:
            raise ValueError("Stages require unique simple names")
        stage_names.add(name)
        if sorted(p["slot"] for p in stage["players"]) != [1, 2]:
            raise ValueError("Each stage requires conditions for both slots")
        for condition in stage["players"]:
            if condition["game"] not in ("oot", "mm") or type(condition["received_index"]) is not int or condition["received_index"] < 0:
                raise ValueError("Stage conditions require a game and nonnegative receipt index")
            player = next(p for p in players if p["slot"] == condition["slot"])
            scenario = json.loads(Path(player["scenario"]).read_text(encoding="utf-8"))
            if not any(s["action"] == "capture" and s["name"] == condition["capture"] for s in scenario["steps"]):
                raise ValueError("Stage capture is absent from its scenario")
    validate_backlog(backlog, players, stage_names)
    restart_stage = plan.get("restart_stage")
    validate_restart(restart_stage, stage_names, backlog)
    for p in players:
        if type(p["received_index"]) is not int or p["received_index"] < 0:
            raise ValueError("Each slot needs a nonnegative receipt target")
    if not any(p["checks"] for p in players):
        raise ValueError("At least one slot needs actual source checks")
    if not any(p["received_index"] > 0 for p in players):
        raise ValueError("At least one slot needs a positive receipt target")
    # Resolve every input before launching either emulator, so a missing second-slot
    # checkpoint cannot interrupt an otherwise valid first-slot run.
    for key in ("seed", "emulator", "config", "connector"):
        Path(plan[key]).resolve(strict=True)
    for player in players:
        for key in ("rom", "placements", "scenario"):
            Path(player[key]).resolve(strict=True)
        modes = sum(bool(player.get(key)) for key in ("fresh_boot", "state", "save_ram"))
        if modes != 1:
            raise ValueError("Each slot requires exactly one boot mode")
        for key in ("state", "save_ram"):
            if player.get(key):
                Path(player[key]).resolve(strict=True)
        scenario = json.loads(Path(player["scenario"]).read_text(encoding="utf-8"))
        if any(s["action"] == "wait_signal" and s["name"] not in stage_names for s in scenario["steps"]):
            raise ValueError("Scenario waits for an undeclared stage")
        if stages:
            with Path(player["rom"]).open("rb") as rom:
                header = rom.read(0x40)
            if header[0x18:0x20] != b"APIPC001":
                raise ValueError("Staged game assertions require the ROM mailbox directory")
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=False)
    (out / "plan.json").write_text(json.dumps(plan, indent=2), encoding="utf-8")
    context = MultiServer.Context("127.0.0.1", 0, "", "", 1, 10, False)
    context.load(str(Path(plan["seed"]).resolve(strict=True)))
    context.save_filename = str(out / "server.apsave")
    server = await websockets.serve(functools.partial(MultiServer.server, ctx=context), "127.0.0.1", 0)
    address = f"ws://127.0.0.1:{server.sockets[0].getsockname()[1]}"

    class Peer(CommonClient.CommonContext):
        game = "OOTxMM"
        items_handling = 0b101
        want_slot_data = True

        def __init__(self, player):
            super().__init__(address, None)
            self.player = player
            self.bizhawk_ctx = bizhawk.BizHawkContext()
            self.handler = OOTxMMClient()
            self.last_observed_receipt = None
            self.history = []
            self.load = MailboxLoad()
            self.slot_data = None

        async def server_auth(self, password_requested=False):
            self.auth = context.player_names[0, self.player["slot"]]
            await self.send_connect()

        def on_package(self, cmd, data):
            if cmd == "Connected":
                self.slot_data = data["slot_data"]
            self.handler.on_package(self, cmd, data)

    peers, processes, logs, workers = [], [], [], []
    report = {"passed": False, "coverage": "assisted-gameplay", "simulated_remote_checks": [], "players": [],
              "stages": [],
              "backlog": None,
              "server_restart": None,
              "coordinator_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "seed_sha256": hashlib.sha256(Path(plan["seed"]).read_bytes()).hexdigest()}
    startup = subprocess.STARTUPINFO()
    startup.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startup.wShowWindow = 0
    started = time.monotonic()

    async def connect(peer):
        if peer.bizhawk_ctx.streams is None:
            first = args.port + (peer.player["slot"] - 1) * 10
            for port in range(first, first + 6):
                try:
                    peer.bizhawk_ctx.streams = await asyncio.open_connection("127.0.0.1", port)
                    peer.bizhawk_ctx.connection_status = bizhawk.ConnectionStatus.TENTATIVE
                    peer.bizhawk_ctx._port = port
                    break
                except ConnectionRefusedError:
                    continue
            else:
                return False
        return True

    async def poll(peer):
        if not await connect(peer):
            peer.live = False
            return
        try:
            await peer.load.sample(peer, bizhawk)
            await peer.handler.game_watcher(peer)
            await peer.load.sample(peer, bizhawk)
        except (bizhawk.NotConnectedError, bizhawk.RequestFailedError):
            peer.live = False
            return
        if peer.handler.mailbox is not None and peer.handler.last_query is not None:
            try:
                header, = await bizhawk.read(peer.bizhawk_ctx, [(peer.handler.mailbox, 24, "RDRAM")])
                sample = (peer.handler.mailbox, header[20:24])
                peer.live = (header[:16] == MAGIC and header[16:20] == b"\x00\x00\x00\x01"
                             and getattr(peer, "alive_sample", None) is not None
                             and peer.alive_sample[0] == sample[0] and peer.alive_sample[1] != sample[1])
                peer.alive_sample = sample
                peer.sample_at = time.monotonic()
                ready_file = out / f"slot-{peer.player['slot']}" / "client-ready.json"
                if peer.live and not ready_file.exists():
                    ready_file.write_text(
                        json.dumps({"verified_connector_rom_sha1": peer.player["verified_connector_rom_sha1"]}), encoding="utf-8")
            except (bizhawk.NotConnectedError, bizhawk.RequestFailedError):
                peer.live = False
                return
        else:
            peer.live = False
        peer.poll_count += 1
        if peer.handler.last_query is not None:
            peer.last_observed_receipt = peer.handler.last_query
        value = {"mailbox": peer.handler.mailbox, "received_index": peer.handler.last_query}
        if not peer.history or peer.history[-1] != value:
            peer.history.append(value)
            print(f"Slot {peer.player['slot']}: {value}", flush=True)

    async def watch(peer, process):
        while process.poll() is None:
            async with peer.poll_lock:
                if not peer.offline:
                    await poll(peer)
            await asyncio.sleep(0.125)

    def check_workers():
        for worker in workers:
            if worker.done() and not worker.cancelled():
                worker.result()

    def observations():
        result = {}
        for peer in peers:
            slot = peer.player["slot"]
            captures = completed_captures(out / f"slot-{slot}" / "events.jsonl")
            directory = peer.handler.rom_mailboxes
            game = None
            if peer.live and time.monotonic() - peer.sample_at <= 1 and len(directory) == 2 and peer.handler.mailbox in directory:
                game = ("oot", "mm")[directory.index(peer.handler.mailbox)]
            result[slot] = {"captures": sorted(captures), "game": game,
                            "mailbox": peer.handler.mailbox, "rom_mailboxes": directory,
                            "received_index": peer.handler.last_query,
                            "checks": [context.location_names["OOTxMM"][loc]
                                       for loc in sorted(context.location_checks[0, slot])]}
        return result

    async def advance_stages():
        nonlocal context, server
        if len(report["stages"]) >= len(stages):
            return
        stage = stages[len(report["stages"])]
        observed = observations()
        if stage_ready(stage, observed):
            if stage["name"] == restart_stage:
                before = {str(p.player["slot"]): {
                    "checks": sorted(context.location_checks[0, p.player["slot"]]),
                    "received_index": p.handler.last_query,
                    "queued": len(MultiServer.get_received_items(context, 0, p.player["slot"], False))}
                    for p in peers}
                for peer in peers:
                    async with peer.poll_lock:
                        mailbox = peer.handler.mailbox
                        await peer.disconnect()
                        await poll(peer)
                        flag, = await bizhawk.read(peer.bizhawk_ctx, [(mailbox + 16, 4, "RDRAM")])
                        assert flag == bytes(4), "Game must observe server outage"
                        peer.offline = True
                        peer.live = False
                server_port = server.sockets[0].getsockname()[1]
                server.close()
                await server.wait_closed()
                assert context._save(), "Pre-restart server save failed"
                saved = (out / "server.apsave").read_bytes()
                (out / "before-restart.apsave").write_bytes(saved)
                replacement = MultiServer.Context("127.0.0.1", 0, "", "", 1, 10, False)
                replacement.load(str(Path(plan["seed"]).resolve(strict=True)))
                replacement.save_filename = str(out / "server.apsave")
                replacement.set_save(Utils.restricted_loads(zlib.decompress(saved)))
                assert replacement is not context
                context = replacement
                for peer in peers:
                    baseline = before[str(peer.player["slot"])]
                    assert sorted(context.location_checks[0, peer.player["slot"]]) == baseline["checks"]
                    assert len(MultiServer.get_received_items(context, 0, peer.player["slot"], False)) == baseline["queued"]
                server = await websockets.serve(functools.partial(MultiServer.server, ctx=context), "127.0.0.1", server_port)
                for peer in peers:
                    peer.server_task = asyncio.create_task(CommonClient.server_loop(peer))
                    peer.offline = False
                async with asyncio.timeout(30):
                    while not all(p.live and p.slot == p.player["slot"] for p in peers):
                        check_workers()
                        await asyncio.sleep(0.125)
                for peer in peers:
                    assert peer.handler.last_query == before[str(peer.player["slot"])]["received_index"], "Restart replayed receipts"
                report["server_restart"] = {"stage": restart_stage, "before": before,
                    "save_sha256": hashlib.sha256(saved).hexdigest(), "restored": True,
                    "elapsed_seconds": time.monotonic() - started,
                    "limits": "Orderly listener/context replacement in the coordinator; not a server process crash"}
            if backlog and stage["name"] == backlog["disconnect_stage"]:
                peer = next(p for p in peers if p.player["slot"] == backlog["slot"])
                async with peer.poll_lock:
                    mailbox = peer.handler.mailbox
                    index = peer.handler.last_query
                    await peer.disconnect()
                    await poll(peer)
                    flag, = await bizhawk.read(peer.bizhawk_ctx, [(mailbox + 16, 4, "RDRAM")])
                    assert flag == bytes(4), "Recipient game must see the disconnect"
                    peer.offline = True
                    peer.live = False
                    peer.offline_mailbox = mailbox
                    report["backlog"] = {"slot": backlog["slot"], "received_index_before": index,
                                         "queued_before": len(MultiServer.get_received_items(context, 0, backlog["slot"], False)),
                                         "game_flag_cleared": True, "offline_samples": 0,
                                         "reconnected": False}
            report["stages"].append({"name": stage["name"], "elapsed_seconds": time.monotonic() - started,
                                     "observations": observed})
            for slot in (1, 2):
                (out / f"slot-{slot}" / f"signal-{stage['name']}").touch()
            print(f"Stage passed: {stage['name']}", flush=True)

    async def recover_backlog():
        evidence = report["backlog"]
        if not evidence or evidence["reconnected"]:
            return
        peer = next(p for p in peers if p.player["slot"] == backlog["slot"])
        assert peer.server is None and peer.slot is None, "Offline recipient unexpectedly reconnected"
        flag, = await bizhawk.read(peer.bizhawk_ctx, [(peer.offline_mailbox + 16, 4, "RDRAM")])
        assert flag == bytes(4), "Recipient must stay disconnected while sources queue"
        evidence["offline_samples"] += 1
        source = 3 - backlog["slot"]
        checks = {context.location_names["OOTxMM"][loc] for loc in context.location_checks[0, source]}
        if not set(backlog["checks"]) <= checks:
            return
        queued = MultiServer.get_received_items(context, 0, backlog["slot"], False)
        assert len(queued) == evidence["queued_before"] + len(backlog["checks"]), "Unexpected backlog size"
        evidence.update(queued_while_offline=len(queued), source_checks=sorted(checks),
                        elapsed_seconds=time.monotonic() - started)
        peer.server_task = asyncio.create_task(CommonClient.server_loop(peer))
        peer.offline = False
        evidence["reconnected"] = True

    try:
        async with asyncio.timeout(args.timeout):
            for player in players:
                slot = player["slot"]
                port = args.port + (slot - 1) * 10
                # Refuse occupied ports rather than attach to another running game.
                for candidate in range(port, port + 6):
                    try:
                        reader, writer = await asyncio.open_connection("127.0.0.1", candidate)
                    except ConnectionRefusedError:
                        continue
                    writer.close()
                    await writer.wait_closed()
                    raise ValueError(f"Connector port {candidate} is already occupied")
                command = [sys.executable, str(Path(__file__).with_name("gameplay_test.py")),
                           "--slot", str(slot), "--out", str(out / f"slot-{slot}"),
                           "--stop-file", str(out / "stop"),
                           "--connector-port", str(port), "--timeout", str(args.timeout)]
                for name in ("seed", "emulator", "config", "connector"):
                    command.extend(["--" + name, str(Path(plan[name]).resolve(strict=True))])
                for name in ("rom", "placements", "scenario"):
                    command.extend(["--" + name, str(Path(player[name]).resolve(strict=True))])
                if player.get("fresh_boot"):
                    command.append("--fresh-boot")
                else:
                    boot = "state" if player.get("state") else "save_ram"
                    command.extend(["--" + boot.replace("_", "-"), str(Path(player[boot]).resolve(strict=True))])
                log = (out / f"slot-{slot}.txt").open("w", encoding="utf-8")
                logs.append(log)
                processes.append(subprocess.Popen(command, stdout=log, stderr=subprocess.STDOUT, startupinfo=startup))
                peer = Peer(player)
                peer.poll_count = 0
                peer.live = False
                peer.offline = False
                peer.poll_lock = asyncio.Lock()
                peers.append(peer)
                while peer.bizhawk_ctx.streams is None:
                    if processes[-1].poll() is not None:
                        raise RuntimeError(f"Slot {slot} runner exited before connector attachment")
                    if not await connect(peer):
                        await asyncio.sleep(0.25)
                peer.bizhawk_ctx.connection_status = bizhawk.ConnectionStatus.TENTATIVE
                peer.bizhawk_ctx._port = port
                expected_hash = hashlib.sha1(Path(player["rom"]).read_bytes()).hexdigest().upper()
                actual_hash = await wait_for_rom(peer, bizhawk, expected_hash, connect=lambda: connect(peer))
                player["verified_connector_rom_sha1"] = actual_hash
                if stages and len(peer.handler.rom_mailboxes) != 2:
                    raise ValueError("Staged game assertions require a valid mailbox directory")
                peer.server_task = asyncio.create_task(CommonClient.server_loop(peer))
                workers.append(asyncio.create_task(watch(peer, processes[-1])))
                print(f"Slot {slot}: attached to verified ROM on port {port}", flush=True)

            names = context.location_names["OOTxMM"]
            wanted = expected_sources(players, context.locations, names, context.slot_set)
            for stage in stages:
                for condition in stage["players"]:
                    valid_checks = {names[loc] for loc in context.locations[condition["slot"]]}
                    if not set(condition.get("checks", [])) <= valid_checks:
                        raise ValueError("Stage refers to an unknown source check")
            if backlog:
                source = 3 - backlog["slot"]
                source_peer = next(p for p in peers if p.player["slot"] == source)
                assert set(backlog["checks"]) <= set(source_peer.player["checks"]), "Backlog sources must be expected real checks"
                for loc in wanted[source]:
                    if names[loc] in backlog["checks"]:
                        assert context.locations[source][loc][1] == backlog["slot"], "Backlog source must award recipient"
            stable = 0
            last_counts = [0, 0]
            while stable < 16:
                check_workers()
                for peer, process in zip(peers, processes):
                    if process.poll() is not None:
                        raise RuntimeError(f"Slot {peer.player['slot']} exited before exchange assertions")
                await advance_stages()
                await recover_backlog()
                ready = all(p.live and p.bizhawk_ctx.streams is not None and p.slot is not None
                            and wanted[p.player["slot"]] <= context.location_checks[0, p.player["slot"]]
                            and p.handler.last_query == p.player["received_index"] for p in peers)
                counts = [peer.poll_count for peer in peers]
                if not ready:
                    stable = 0
                elif all(current > previous for current, previous in zip(counts, last_counts)):
                    stable += 1
                    last_counts = counts
                await asyncio.sleep(0.125)
            for peer in peers:
                slot = peer.player["slot"]
                received = MultiServer.get_received_items(context, 0, slot, False)
                starting = MultiServer.get_start_inventory(context, slot, True)
                verify_receipt_count(starting, received, peer.player["received_index"])
                awards = []
                for loc in sorted(wanted[slot]):
                    item, recipient = verify_pickup_award(context, MultiServer.get_received_items, slot, loc)
                    awards.append({"location": names[loc], "recipient": recipient,
                                   "item": context.item_names["OOTxMM"][item]})
                report["players"].append({"slot": slot, "awards": awards, "received_index": peer.handler.last_query,
                                          "starting_items": [context.item_names["OOTxMM"][item.item] for item in starting],
                                          "remote_item_count": len(received),
                                          "history": peer.history, "stable_polls": stable,
                                          "verified_connector_rom_sha1": peer.player["verified_connector_rom_sha1"]})
            assert context._save(), "Disposable server save failed"
            # Continue servicing both games while their inventory assertions and captures finish.
            while any(p.poll() is None for p in processes):
                check_workers()
                await advance_stages()
                await asyncio.sleep(0.125)
            for peer, process in zip(peers, processes):
                result = json.loads((out / f"slot-{peer.player['slot']}" / "result.json").read_text(encoding="utf-8"))
                assert process.returncode == 0 and result["passed"], "Game scenario failed"
                # The credits transition or emulator shutdown can clear the active mailbox.
                assert peer.last_observed_receipt == peer.player["received_index"], "Receipt index changed after stability check"
            assert len(report["stages"]) == len(stages), "Not all gameplay stages completed"
            if backlog:
                assert report["backlog"] and report["backlog"]["reconnected"], "Backlog recovery did not run"
            if restart_stage:
                assert report["server_restart"] and report["server_restart"]["restored"], "Server restart did not run"
                for peer in peers:
                    baseline = report["server_restart"]["before"][str(peer.player["slot"]) ]
                    assert wanted[peer.player["slot"]] - set(baseline["checks"]), "No new source pickup after restart"
                    assert peer.last_observed_receipt > baseline["received_index"], "No new remote delivery after restart"
            report["passed"] = True
    except Exception as exc:
        report["reason"] = f"{type(exc).__name__}: {exc}"
        raise
    finally:
        report["final_observations"] = [{"slot": peer.player["slot"], "received_index": peer.last_observed_receipt,
                                         "mailbox_load": peer.load.report(),
                                         "history": peer.history,
                                         "checks": [context.location_names["OOTxMM"][loc]
                                                    for loc in sorted(context.location_checks[0, peer.player["slot"]])]}
                                        for peer in peers]
        (out / "result.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
        (out / "stop").touch()
        for process in processes:
            if process.poll() is None:
                # The stop file asks the runner to clean up its own emulator.
                try:
                    await asyncio.to_thread(process.wait, timeout=15)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait()
        for log in logs:
            log.close()
        for worker in workers:
            worker.cancel()
        await asyncio.gather(*workers, return_exceptions=True)
        for peer in peers:
            bizhawk.disconnect(peer.bizhawk_ctx)
            await peer.shutdown()
        server.close()
        await server.wait_closed()
    print(json.dumps(report), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--archipelago", type=Path, required=True)
    parser.add_argument("--timeout", type=float, default=180)
    parser.add_argument("--port", type=int, default=43055)
    args = parser.parse_args()
    if not 1024 <= args.port <= 65520 or not 0 < args.timeout <= 3600:
        parser.error("Use two valid connector ranges and a timeout between 0 and 3600 seconds")
    sys.path.insert(0, str(args.archipelago.resolve(strict=True)))
    os.environ["SKIP_REQUIREMENTS_UPDATE"] = "1"
    logging.basicConfig(level=logging.INFO)
    asyncio.run(run(args))
