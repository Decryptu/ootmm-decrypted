"""Run a bounded BizHawk scenario with isolated configuration, saves and evidence.

Requires BizHawk 2.11.1, a matching ROM/state/seed and AP's generic Lua connector.
Passing steps proves only their explicit assertions. Setup helpers never write check flags or packets.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import time


def digest(path):
    with path.open("rb") as source:
        return hashlib.file_digest(source, "sha256").hexdigest()


def validate(scenario):
    def integer(value, low, high):
        if type(value) is not int or not low <= value <= high:
            raise ValueError(f"Expected integer between {low} and {high}: {value!r}")

    def probe(value):
        integer(value["size"], 1, 4)
        integer(value["address"], 0, 0x800000 - value["size"])
        if "pointer" in value:
            integer(value["pointer"], 0, 0x7ffffc)
        if not isinstance(value["name"], str) or not value["name"]:
            raise ValueError("Probes require a name")

    integer(scenario["max_frames"], 1, 1000000)
    if scenario["coverage"] not in ("unmodified-gameplay", "assisted-gameplay", "protocol"):
        raise ValueError("Declare the coverage category")
    if not scenario.get("description") or not scenario.get("limitations"):
        raise ValueError("Describe the scenario and its limits")
    for game in ("oot", "mm"):
        layout = scenario.get(f"{game}_layout")
        if layout is not None:
            integer(layout["play_pointer"], 0, 0x7ffffc)
            integer(layout["main"], 0x80000000, 0x807fffff)
            if not layout.get("source"):
                raise ValueError("Record the source of compiled layout addresses")
            if len(scenario.get("required_rom_sha256", "")) != 64:
                raise ValueError("Pin the ROM hash before using compiled layout addresses")
    for value in scenario.get("probes", []):
        probe(value)
    for step in scenario["steps"]:
        action = step["action"]
        if action == "wait_signal":
            if not step.get("name") or any(c not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_" for c in step["name"]):
                raise ValueError("Signal names must be simple filenames")
            integer(step["timeout_frames"], 1, scenario["max_frames"])
            if "dismiss_messages" in step and type(step["dismiss_messages"]) is not bool:
                raise ValueError("Message dismissal must be a boolean")
            if step.get("keep_health"):
                if step.get("game") not in ("oot", "mm") or f"{step['game']}_layout" not in scenario or scenario["coverage"] != "assisted-gameplay":
                    raise ValueError("Health support requires a sourced game layout and assisted gameplay")
                integer(step["scene"], 0, 0xffff)
        elif action == "wait_client":
            integer(step["timeout_frames"], 1, scenario["max_frames"])
        elif action == "native_exit":
            if scenario["coverage"] != "assisted-gameplay":
                raise ValueError("Native exit positioning requires assisted gameplay")
            for key in ("game", "target_game"):
                if step.get(key) not in ("oot", "mm") or f"{step[key]}_layout" not in scenario:
                    raise ValueError("Native exits require both sourced layouts")
            if step["game"] == step["target_game"]:
                raise ValueError("Native exit must change games")
            for key in ("scene", "target_scene"):
                integer(step[key], 0, 0xffff)
            integer(step["timeout_frames"], 1, scenario["max_frames"])
            for axis in ("x", "y", "z"):
                if not isinstance(step[axis], (int, float)) or not -100000 <= step[axis] <= 100000:
                    raise ValueError("Invalid player coordinate")
        elif action == "wait_game":
            if step.get("game") not in ("oot", "mm") or f"{step['game']}_layout" not in scenario:
                raise ValueError("Waiting for gameplay requires a sourced game layout")
            integer(step["scene"], 0, 0xffff)
            integer(step["timeout_frames"], 1, scenario["max_frames"])
        elif action == "boot_file":
            if "oot_layout" not in scenario:
                raise ValueError("Automated file boot requires a sourced OoT layout")
            integer(step["scene"], 0, 0xffff)
            integer(step["timeout_frames"], 1, scenario["max_frames"])
        elif action == "speed":
            integer(step["percent"], 100, 400)
        elif action in ("input", "wait"):
            integer(step["frames"], 1, scenario["max_frames"])
            if action == "input":
                if any(type(v) is not bool for v in step.get("buttons", {}).values()):
                    raise ValueError("Digital buttons must be booleans")
                for value in step.get("analog", {}).values():
                    integer(value, -128, 127)
        elif action == "expect_player_item":
            if step["game"] not in ("oot", "mm") or step["game"] + "_layout" not in scenario:
                raise ValueError("Player item assertion requires a sourced game layout")
            integer(step["scene"], 0, 0xffff)
            integer(step["value"], 0, 255)
            integer(step["timeout_frames"], 1, scenario["max_frames"])
        elif action == "expect":
            probe(step)
            integer(step["value"], 0, 256 ** step["size"] - 1)
            if "mask" in step:
                integer(step["mask"], 1, 256 ** step["size"] - 1)
                if step["value"] & ~step["mask"]:
                    raise ValueError("Expected value contains bits outside the assertion mask")
            integer(step["timeout_frames"], 1, scenario["max_frames"])
        elif action == "capture":
            if not step["name"] or any(c not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_" for c in step["name"]):
                raise ValueError("Capture names must be simple filenames")
        elif action in ("mm_boss_support", "mm_boss_approach", "oot_boss_support", "oot_boss_approach", "oot_boss_weapon", "oot_boss_arm"):
            if f"{action.split('_')[0]}_layout" not in scenario or scenario["coverage"] != "assisted-gameplay":
                raise ValueError("Boss support requires a sourced game layout and assisted-gameplay coverage")
            if action == "oot_boss_arm" and step.get("sword") not in ("master", "biggoron"):
                raise ValueError("Choose an acquired master or biggoron sword")
            if action.endswith("_support"):
                integer(step["frames"], 1, scenario["max_frames"])
        elif action == "mm_fairy_approach":
            if "mm_layout" not in scenario or scenario["coverage"] != "assisted-gameplay":
                raise ValueError("Fairy positioning requires a sourced MM layout and assisted gameplay")
            integer(step["scene"], 0, 0xffff)
            if step["scene"] not in (0x16, 0x18, 0x1b, 0x21, 0x49):
                raise ValueError("Fairy positioning requires a temple scene")
            integer(step["flag"], 0, 0x7f)
            integer(step["frames"], 1, min(60, scenario["max_frames"]))
        elif action in ("oot_gohma_prepare", "oot_gohma_approach"):
            if "oot_layout" not in scenario or scenario["coverage"] != "assisted-gameplay":
                raise ValueError("Gohma setup requires a sourced OoT layout and assisted gameplay")
        elif action in ("mm_boss_loadout", "oot_boss_loadout"):
            if f"{action.split('_')[0]}_layout" not in scenario or scenario["coverage"] != "assisted-gameplay":
                raise ValueError("Boss loadout requires a sourced game layout and assisted-gameplay coverage")
            integer(step["scene"], 0, 0xffff)
        elif action in ("oot_transition", "oot_position", "mm_transition", "mm_position"):
            game, operation = action.split("_")
            if f"{game}_layout" not in scenario or scenario["coverage"] != "assisted-gameplay":
                raise ValueError("Setup helpers require a sourced layout and assisted-gameplay coverage")
            if operation == "transition":
                integer(step["from_scene"], 0, 0xffff)
                integer(step["entrance"], 0, 0xffff)
            else:
                integer(step["scene"], 0, 0xffff)
                integer(step.get("frames", 1), 1, 60)
                if "yaw" in step:
                    integer(step["yaw"], 0, 0xffff)
                for axis in ("x", "y", "z"):
                    if not isinstance(step[axis], (int, float)) or not -100000 <= step[axis] <= 100000:
                        raise ValueError("Invalid player coordinate")
        else:
            raise ValueError(f"Unsupported action: {action}")


def validate_grant_capture(scenario, name, grants):
    if name is None:
        return
    if not grants or not name or any(c not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_" for c in name):
        raise ValueError("Grant capture requires diagnostic grants and a simple capture name")
    if not any(step["action"] == "capture" and step["name"] == name for step in scenario["steps"]):
        raise ValueError("Grant capture is absent from the scenario")


def run(args):
    scenario = json.loads(args.scenario.read_text(encoding="utf-8"))
    validate(scenario)
    validate_grant_capture(scenario, args.grant_after_capture, args.grant_item)
    paths = {name: getattr(args, name).resolve(strict=True)
             for name in ("rom", "seed", "placements", "config", "connector", "emulator", "scenario")}
    for name in ("state", "save_ram", "server_save_input"):
        if getattr(args, name) is not None:
            paths[name] = getattr(args, name).resolve(strict=True)
    if scenario.get("required_rom_sha256", digest(paths["rom"])) != digest(paths["rom"]):
        raise ValueError("Scenario layout belongs to a different ROM")
    if args.connector_port is not None and not 1024 <= args.connector_port <= 65530:
        raise ValueError("Connector range start must be between 1024 and 65530")
    placements = json.loads(paths["placements"].read_text(encoding="utf-8"))
    observe = bool(args.expect_check or args.expect_boss or args.grant_item)
    if args.interrupt_pickup and (not args.expect_check or args.save_offline or args.disconnect_seconds
                                  or args.inject_remote_count or args.grant_item or args.expect_boss):
        raise ValueError("Pickup interruption requires real pickup assertions and no other stimuli")
    if args.save_offline and (not args.expect_check or args.disconnect_seconds or args.inject_remote_count
                             or args.grant_item or args.expect_boss):
        raise ValueError("Offline save requires pickup assertions and no other stimuli")
    if observe and not (args.ap_python and args.archipelago):
        raise ValueError("Server assertions require --ap-python and --archipelago")
    if not observe and not args.stop_file and any(step["action"] == "wait_client" for step in scenario["steps"]):
        raise ValueError("wait_client requires a server observer or external coordinator")
    if args.min_game_switches < 0 or (args.min_game_switches and not args.expect_check):
        raise ValueError("--min-game-switches requires nonnegative count and pickup assertions")
    if args.inject_remote_count < 0 or (args.expect_received_index is not None and args.expect_received_index < 0):
        raise ValueError("Receipt counts must be nonnegative")
    if (args.save_server or args.server_save_input or args.inject_remote_count or args.expect_received_index is not None) and not observe:
        raise ValueError("Server persistence requires pickup or boss assertions")
    if args.inject_remote_count and args.expect_received_index is None:
        raise ValueError("Simulated remote checks require an expected received index")
    if args.grant_item and args.expect_received_index is None:
        raise ValueError("Diagnostic grants require an expected received index")
    if not 0 <= args.disconnect_seconds <= 60 or (args.disconnect_seconds and not args.expect_check):
        raise ValueError("Disconnect duration must be 0-60 seconds and requires pickup assertions")
    expected_seed = paths["seed"].stem.removeprefix("AP_") + f"-{args.slot}"
    if placements["seed"] != expected_seed:
        raise ValueError("Placements do not match the supplied seed and slot")
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=False)
    config = json.loads(paths["config"].read_text(encoding="utf-8-sig"))
    for entry in config["PathEntries"]["Paths"]:
        if entry["System"] == "Global_NULL" and entry["Type"] == "Base":
            entry["Path"] = out.as_posix()
        elif Path(entry["Path"]).is_absolute() or ".." in Path(entry["Path"]).parts:
            entry["Path"] = "./" + entry["Type"]
    config["RecentRoms"] = {"recentlist": []}
    config["StartPaused"] = False
    if any(step["action"] == "speed" for step in scenario["steps"]):
        config["ClockThrottle"] = True
        config["Unthrottled"] = False
    (out / "config.ini").write_text(json.dumps(config, indent=2), encoding="utf-8")
    if args.save_ram:
        save_dir = out / "N64" / "SaveRAM"
        save_dir.mkdir(parents=True)
        shutil.copy2(paths["save_ram"], save_dir / paths["save_ram"].name)
    shutil.copytree(paths["connector"].parent, out / "lua")
    if args.connector_port is not None:
        connector_copy = out / "lua" / paths["connector"].name
        source = connector_copy.read_text(encoding="utf-8")
        first, size = "local SOCKET_PORT_FIRST = 43055", "local SOCKET_PORT_RANGE_SIZE = 5"
        if source.count(first) != 1 or source.count(size) != 1:
            raise ValueError("Unsupported connector port configuration")
        connector_copy.write_text(source.replace(first, f"local SOCKET_PORT_FIRST = {args.connector_port}"), encoding="utf-8")
    shutil.copy2(Path(__file__).with_name("bizhawk_scenario.lua"), out / "lua" / "scenario.lua")
    (out / "scenario.json").write_text(json.dumps(scenario, indent=2), encoding="utf-8")
    manifest = {"inputs": {name: {"path": str(path), "sha256": digest(path)}
                           for name, path in paths.items()},
                "coverage": scenario["coverage"], "description": scenario["description"],
                "limitations": scenario["limitations"], "slot": args.slot,
                "ootmm_seed": placements["seed"], "settings": placements["settings"],
                "setup_modifications": args.setup_note,
                "harness_sha256": digest(Path(__file__).with_name("bizhawk_scenario.lua")),
                "runner_sha256": digest(Path(__file__)),
                "observer_sha256": digest(Path(__file__).with_name("emulator-smoke.py")),
                "boot_mode": "savestate" if args.state else "native-save" if args.save_ram else "fresh-file",
                "connector_port": args.connector_port,
                "assertions": {"checks": args.expect_check, "bosses": args.expect_boss, "min_game_switches": args.min_game_switches,
                               "received_index": args.expect_received_index,
                               "disconnect_seconds": args.disconnect_seconds,
                               "save_offline": args.save_offline,
                               "interrupt_pickup": args.interrupt_pickup,
                               "simulated_remote_count": args.inject_remote_count, "setup_grants": args.grant_item,
                               "grant_after_capture": args.grant_after_capture}}
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    command = [str(paths["emulator"]), "--gdi", f"--config={out / 'config.ini'}",
               *([f"--load-state={paths['state']}"] if args.state else []), f"--lua={out / 'lua' / 'scenario.lua'}",
               f"--userdata=out:{out};connector:{out / 'lua' / paths['connector'].name}",
               str(paths["rom"])]
    startup = subprocess.STARTUPINFO()
    startup.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startup.wShowWindow = 0
    with (out / "stdout.txt").open("w") as stdout, (out / "stderr.txt").open("w") as stderr:
        process = subprocess.Popen(command, cwd=out / "lua", stdout=stdout, stderr=stderr, startupinfo=startup)
        observer = None
        observer_log = None
        print(f"BizHawk PID {process.pid}; evidence: {out}", flush=True)
        deadline = time.monotonic() + args.timeout
        try:
            if observe:
                observer_command = [str(args.ap_python.resolve(strict=True)),
                                    str(Path(__file__).with_name("emulator-smoke.py").resolve()),
                                    "--archipelago", str(args.archipelago.resolve(strict=True)),
                                    "--seed", str(paths["seed"]), "--slot", str(args.slot), "--report", str(out / "server-result.json"),
                                    "--expected-rom-sha1", hashlib.sha1(paths["rom"].read_bytes()).hexdigest(),
                                    "--ready-file", str(out / "client-ready.json"),
                                    "--timeout", str(args.timeout), "--min-game-switches", str(args.min_game_switches)]
                if args.connector_port is not None:
                    observer_command.extend(["--connector-port", str(args.connector_port)])
                if args.disconnect_seconds:
                    observer_command.extend(["--disconnect-seconds", str(args.disconnect_seconds)])
                if args.save_offline:
                    observer_command.append("--save-offline")
                if args.interrupt_pickup:
                    observer_command.extend(["--interrupt-pickup", args.interrupt_pickup])
                if args.inject_remote_count:
                    observer_command.extend(["--inject-remote-count", str(args.inject_remote_count)])
                if args.expect_received_index is not None:
                    observer_command.extend(["--expect-received-index", str(args.expect_received_index)])
                if args.server_save_input:
                    observer_command.extend(["--server-save-input", str(paths["server_save_input"])])
                if args.save_server:
                    observer_command.extend(["--server-save-output", str(out / "server.apsave")])
                for item in args.grant_item:
                    observer_command.extend(["--grant-item", item])
                if args.grant_after_capture:
                    observer_command.extend(["--grant-ready-file", str(out / (args.grant_after_capture + ".png"))])
                for boss in args.expect_boss:
                    observer_command.extend(["--expect-boss", boss])
                for name in args.expect_check:
                    observer_command.extend(["--expect-check", name])
                observer_log = (out / "server.txt").open("w")
                observer = subprocess.Popen(observer_command, stdout=observer_log, stderr=subprocess.STDOUT, startupinfo=startup)
            while (process.poll() is None and time.monotonic() < deadline
                   and not (args.stop_file and args.stop_file.exists())):
                time.sleep(0.25)
            if process.poll() is None:
                result = {"passed": False, "scenario_passed": False,
                          "reason": "Scenario stopped by coordinator" if args.stop_file and args.stop_file.exists()
                                    else "Emulator exceeded wall-clock timeout",
                          "wall_timeout": not bool(args.stop_file and args.stop_file.exists())}
                # Frame callbacks cannot write a result when the core is blocked.
                events = out / "events.jsonl"
                if events.exists():
                    lines = events.read_text(encoding="utf-8").splitlines()
                    if lines:
                        try:
                            result["last_event"] = json.loads(lines[-1])
                        except json.JSONDecodeError:
                            result["last_event_incomplete"] = True
                (out / "result.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
                print(json.dumps(result), flush=True)
                return 1
            result_path = out / "result.json"
            if not result_path.exists():
                raise RuntimeError(f"Emulator exited {process.returncode} without a scenario result; inspect logs")
            result = json.loads(result_path.read_text())
            if args.save_offline and not any(path.stat().st_size for path in (out / "N64" / "SaveRAM").glob("*.SaveRAM")):
                result["passed"] = False
                result["reason"] = "Offline save produced no native SaveRAM"
            if observer is not None:
                try:
                    observer.wait(timeout=max(1, min(10, deadline - time.monotonic())))
                except subprocess.TimeoutExpired:
                    result["reason"] = "Server assertion exceeded wall-clock timeout"
                result["scenario_passed"] = result["passed"]
                result["server_passed"] = observer.returncode == 0 and (out / "server-result.json").exists()
                result["passed"] = result["passed"] and result["server_passed"]
                if not result["server_passed"]:
                    result["server_reason"] = "Server assertion failed; inspect server.txt"
                    if result["scenario_passed"]:
                        result["reason"] = result["server_reason"]
                result_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
            print(json.dumps(result), flush=True)
            return 0 if result["passed"] and process.returncode == 0 else 1
        finally:
            if process.poll() is None:
                process.kill()
                process.wait()
            if observer is not None and observer.poll() is None:
                observer.kill()
                observer.wait()
            if observer_log is not None:
                observer_log.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("rom", "seed", "placements", "config", "connector", "emulator", "scenario", "out"):
        parser.add_argument(f"--{name}", type=Path, required=True)
    boot = parser.add_mutually_exclusive_group(required=True)
    boot.add_argument("--state", type=Path)
    boot.add_argument("--save-ram", type=Path, help="Cold boot using a disposable native SaveRAM file")
    boot.add_argument("--fresh-boot", action="store_true", help="Boot a new isolated file without any existing save")
    parser.add_argument("--connector-port", type=int, help="Set the disposable connector's six-port loopback range start")
    parser.add_argument("--stop-file", type=Path, help="Stop and clean up this runner when the coordinator creates this file")
    parser.add_argument("--disconnect-seconds", type=float, default=0)
    parser.add_argument("--interrupt-pickup", choices=("before-send", "after-accept"))
    parser.add_argument("--save-offline", action="store_true", help="Save a real pending pickup while disconnected; pair with a separate cold boot")
    parser.add_argument("--grant-item", action="append", default=[])
    parser.add_argument("--grant-after-capture", help="Delay diagnostic grants until this scenario capture completes")
    parser.add_argument("--inject-remote-count", type=int, default=0)
    parser.add_argument("--expect-received-index", type=int)
    parser.add_argument("--server-save-input", type=Path)
    parser.add_argument("--save-server", action="store_true")
    parser.add_argument("--slot", type=int, required=True)
    parser.add_argument("--setup-note", action="append", default=[])
    parser.add_argument("--timeout", type=float, default=180)
    parser.add_argument("--ap-python", type=Path)
    parser.add_argument("--archipelago", type=Path)
    parser.add_argument("--min-game-switches", type=int, default=0)
    parser.add_argument("--expect-boss", action="append", default=[], choices=("OOT_GANON", "MM_MAJORA"))
    parser.add_argument("--expect-check", action="append", default=[])
    args = parser.parse_args()
    raise SystemExit(run(args))
