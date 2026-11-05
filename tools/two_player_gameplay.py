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
import os
from pathlib import Path
import subprocess
import sys


async def run(args):
    import CommonClient
    import MultiServer
    import websockets
    import worlds._bizhawk as bizhawk
    from worlds.ootxmm.client import OOTxMMClient

    plan = json.loads(args.plan.read_text(encoding="utf-8"))
    players = plan["players"]
    if sorted(p["slot"] for p in players) != [1, 2]:
        raise ValueError("Plan must contain slots 1 and 2 exactly once")
    for p in players:
        if not p["checks"] or type(p["received_index"]) is not int or p["received_index"] < 1:
            raise ValueError("Each slot needs actual source checks and a positive receipt target")
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
            self.history = []
            self.slot_data = None

        async def server_auth(self, password_requested=False):
            self.auth = context.player_names[0, self.player["slot"]]
            await self.send_connect()

        def on_package(self, cmd, data):
            if cmd == "Connected":
                self.slot_data = data["slot_data"]
            self.handler.on_package(self, cmd, data)

    peers, processes, logs = [], [], []
    report = {"passed": False, "coverage": "assisted-gameplay", "simulated_remote_checks": [], "players": [],
              "coordinator_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "seed_sha256": hashlib.sha256(Path(plan["seed"]).read_bytes()).hexdigest()}
    startup = subprocess.STARTUPINFO()
    startup.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startup.wShowWindow = 0

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
            return
        try:
            await peer.handler.game_watcher(peer)
        except (bizhawk.NotConnectedError, bizhawk.RequestFailedError):
            return
        value = {"mailbox": peer.handler.mailbox, "received_index": peer.handler.last_query}
        if not peer.history or peer.history[-1] != value:
            peer.history.append(value)
            print(f"Slot {peer.player['slot']}: {value}", flush=True)

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
                peers.append(peer)
                while peer.bizhawk_ctx.streams is None:
                    if processes[-1].poll() is not None:
                        raise RuntimeError(f"Slot {slot} runner exited before connector attachment")
                    if not await connect(peer):
                        await asyncio.sleep(0.25)
                peer.bizhawk_ctx.connection_status = bizhawk.ConnectionStatus.TENTATIVE
                peer.bizhawk_ctx._port = port
                expected_hash = hashlib.sha1(Path(player["rom"]).read_bytes()).hexdigest().upper()
                for attempt in range(4):
                    try:
                        actual_hash = (await bizhawk.get_hash(peer.bizhawk_ctx)).upper()
                        break
                    except bizhawk.RequestFailedError:
                        if attempt == 3:
                            raise
                        await asyncio.sleep(0.5)
                        while not await connect(peer):
                            await asyncio.sleep(0.25)
                assert actual_hash == expected_hash, f"Slot {slot} connector ROM hash mismatch: {actual_hash}"
                player["verified_connector_rom_sha1"] = actual_hash
                assert await peer.handler.validate_rom(peer), "Expected patched OoTMM ROM"
                peer.server_task = asyncio.create_task(CommonClient.server_loop(peer))
                print(f"Slot {slot}: attached to verified ROM on port {port}", flush=True)

            names = context.location_names["OOTxMM"]
            wanted = {}
            for peer in peers:
                slot = peer.player["slot"]
                wanted[slot] = {loc for loc in context.locations[slot] if names[loc] in peer.player["checks"]}
                assert len(wanted[slot]) == len(set(peer.player["checks"])), "Unknown expected source check"
                assert any(context.locations[slot][loc][1] == 3 - slot for loc in wanted[slot]), "Each source must award the other player"
            stable = 0
            while stable < 16:
                for peer, process in zip(peers, processes):
                    if process.poll() is not None:
                        raise RuntimeError(f"Slot {peer.player['slot']} exited before exchange assertions")
                await asyncio.gather(*(poll(peer) for peer in peers))
                ready = all(p.bizhawk_ctx.streams is not None and p.slot is not None
                            and wanted[p.player["slot"]] <= context.location_checks[0, p.player["slot"]]
                            and p.handler.last_query == p.player["received_index"] for p in peers)
                stable = stable + 1 if ready else 0
                await asyncio.sleep(0.125)
            for peer in peers:
                slot = peer.player["slot"]
                received = MultiServer.get_received_items(context, 0, slot, False)
                assert len(received) == peer.player["received_index"], "Unexpected extra remote awards"
                awards = []
                for loc in sorted(wanted[slot]):
                    item, recipient, _flags = context.locations[slot][loc]
                    queued = MultiServer.get_received_items(context, 0, recipient, True)
                    assert sum(i.location == loc and i.player == slot and i.item == item for i in queued) == 1, "Award duplicated"
                    awards.append({"location": names[loc], "recipient": recipient,
                                   "item": context.item_names["OOTxMM"][item]})
                report["players"].append({"slot": slot, "awards": awards, "received_index": peer.handler.last_query,
                                          "history": peer.history, "stable_polls": stable,
                                          "verified_connector_rom_sha1": peer.player["verified_connector_rom_sha1"]})
            assert context._save(), "Disposable server save failed"
            # Continue servicing both games while their inventory assertions and captures finish.
            while any(p.poll() is None for p in processes):
                await asyncio.gather(*(poll(peer) for peer, process in zip(peers, processes) if process.poll() is None))
                await asyncio.sleep(0.125)
            for peer, process in zip(peers, processes):
                result = json.loads((out / f"slot-{peer.player['slot']}" / "result.json").read_text(encoding="utf-8"))
                assert process.returncode == 0 and result["passed"], "Game scenario failed"
                assert peer.handler.last_query == peer.player["received_index"], "Receipt index changed after stability check"
            report["passed"] = True
    except Exception as exc:
        report["reason"] = f"{type(exc).__name__}: {exc}"
        raise
    finally:
        report["final_observations"] = [{"slot": peer.player["slot"], "received_index": peer.handler.last_query,
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
    asyncio.run(run(args))
