"""Package one generated seed and its built patches without ROMs or player spoilers.

python tools/package_playtest.py --seed <AP_seed.zip> --patches <folder> --out dist/playtest
Build the patches from this checkout before packaging. The output directory must be new.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import zipfile


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def file_hashes(folder):
    return {path.relative_to(folder).as_posix(): sha256(path)
            for path in sorted(folder.rglob("*")) if path.is_file()}

ROOT = Path(__file__).resolve().parent.parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=Path, required=True)
    parser.add_argument("--patches", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--require-build-receipts", action="store_true",
                        help="require each patch to match its placement and current patch sources")
    args = parser.parse_args()
    if args.out.exists():
        parser.error("output directory already exists; choose a new directory to preserve frozen builds")
    with zipfile.ZipFile(args.seed) as seed:
        members = seed.namelist()
        player_files = sorted(name for name in members if name.endswith(".ootxmm.json"))
        server_files = [name for name in members if name.endswith(".archipelago")]
        if not player_files or len(server_files) != 1:
            parser.error("seed must contain player JSON files and exactly one .archipelago file")
        # Everything in the seed: other games' players get their patch files from the host.
        host_members = [name for name in members if not name.endswith("/")]
        flattened = [Path(name).name for name in host_members]
        if len(flattened) != len(set(flattened)):
            parser.error("seed contains duplicate host filenames")
        patch_inputs = {path.relative_to(ROOT).as_posix(): sha256(path)
                        for folder in ("ootmm-ap", "ootmm-patches")
                        for path in (ROOT / folder).rglob("*") if path.is_file()}
        slots = []
        for name in player_files:
            data = json.loads(seed.read(name))
            patch = args.patches / (Path(name).name.removesuffix(".json") + ".ootmm")
            if not patch.is_file():
                parser.error(f"missing patch: {patch}")
            receipt_path = patch.with_suffix(".build.json")
            receipt = None
            if receipt_path.exists():
                receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
                expected_placement = hashlib.sha256(seed.read(name)).hexdigest()
                if (receipt.get("schema_version") != 1 or receipt.get("seed") != data["seed"]
                    or receipt.get("placement") != {"name": Path(name).name, "sha256": expected_placement}
                    or receipt.get("patch") != {"name": patch.name, "sha256": sha256(patch)}
                    or receipt.get("builder_sha256") != patch_inputs["ootmm-ap/ap-patch.ts"]
                    or receipt.get("patch_inputs") != patch_inputs):
                    parser.error(f"patch build receipt does not match seed, patch or current sources: {receipt_path}")
            elif args.require_build_receipts:
                parser.error(f"missing patch build receipt: {receipt_path}")
            slots.append({"receipt": receipt_path if receipt else None, "file": name, "seed": data["seed"], "goal": data["settings"]["goal"], "patch": patch})
        share = args.out / "share"
        host = args.out / "host"
        (share / "patches").mkdir(parents=True)
        host.mkdir()
        # Flatten names so ZIP paths never escape the output.
        for name in host_members:
            (host / Path(name).name).write_bytes(seed.read(name))
        for slot in slots:
            if slot["receipt"]:
                shutil.copyfile(slot["receipt"], host / slot["receipt"].name)
            shutil.copyfile(slot["patch"], share / "patches" / slot["patch"].name)
    subprocess.run([sys.executable, str(ROOT / "tools/build_apworld.py"), str(share / "ootxmm.apworld")], check=True)
    for source, target in [("setup_en.md", "setup_en.md"), ("playtest_en.md", "PLAYTEST.md"), ("en_OOTxMM.md", "ABOUT.md")]:
        shutil.copyfile(ROOT / "docs" / source, share / target)
    slot_list = "\n".join(f"- `{slot['patch'].name}` — goal `{slot['goal']}`" for slot in slots)
    (share / "README.md").write_text(
        "# OOTxMM group playtest\n\n"
        "Use Archipelago 0.6.8, BizHawk 2.11.1 and OoTMM v33.0.\n\n"
        "Install `ootxmm.apworld` in Archipelago's `custom_worlds` folder and restart the launcher. "
        "Apply only your matching patch with OoTMM v33.0 and your own ROMs. "
        "The patch filename includes the player number and slot name.\n\n"
        f"{slot_list}\n\n"
        "The host provides the server address, port and slot name. "
        "Follow [setup](setup_en.md), then [the playtest checklist](PLAYTEST.md). "
        "This is a development build awaiting a full gameplay session. "
        "Read [testing scope and remaining limits](ABOUT.md#current-status). "
        "Keep client logs when reporting problems.\n", encoding="utf-8")
    (host / "README.md").write_text(
        "# Host files\n\n"
        f"Host `{Path(server_files[0]).name}` with Archipelago 0.6.8. Keep its server save. "
        "Give players `../players.zip` and their slot names and connection details. "
        "Keep this folder private: it contains the spoiler and placements.\n", encoding="utf-8")
    manifest = []
    for path in sorted(share.rglob("*")):
        if path.is_file():
            manifest.append(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.relative_to(share).as_posix()}")
    (share / "SHA256SUMS.txt").write_text("\n".join(manifest) + "\n", encoding="utf-8")
    with zipfile.ZipFile(args.out / "players.zip", "w", zipfile.ZIP_DEFLATED) as bundle:
        for path in sorted(share.rglob("*")):
            if path.is_file():
                bundle.write(path, path.relative_to(share).as_posix())
    # Keep source and host identities private; only player artifacts enter players.zip.
    with zipfile.ZipFile(share / "ootxmm.apworld") as world:
        world_members = {name: hashlib.sha256(world.read(name)).hexdigest()
                         for name in sorted(world.namelist())}
    revision = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT,
                              check=True, capture_output=True, text=True).stdout.strip()
    status = subprocess.run(["git", "status", "--porcelain", "--untracked-files=normal"],
                            cwd=ROOT, check=True, capture_output=True, text=True).stdout
    inputs = [ROOT / "tools" / name for name in ("package_playtest.py", "build_apworld.py", "verify_playtest.py", "ootmm-build.sh", "ootmm-build.ps1")]
    for folder in ("ootmm-ap", "ootmm-patches"):
        inputs.extend(path for path in (ROOT / folder).rglob("*") if path.is_file())
    provenance = {
        "schema_version": 1,
        "source_revision": revision,
        "source_status": status.splitlines(),
        "seed_archive": {"name": args.seed.name, "sha256": sha256(args.seed)},
        "players_zip_sha256": sha256(args.out / "players.zip"),
        "player_files": file_hashes(share),
        "host_files": file_hashes(host),
        "packaged_world_members": world_members,
        "packaging_and_patch_inputs": {
            path.relative_to(ROOT).as_posix(): sha256(path) for path in sorted(inputs)},
        "slots": [{"placement": Path(slot["file"]).name, "seed": slot["seed"],
                   "goal": slot["goal"], "patch": slot["patch"].name} for slot in slots],
        "validation": {
            "patch_build_receipts_verified": all(slot["receipt"] is not None for slot in slots),
        },
    }
    (host / "PROVENANCE.json").write_text(
        json.dumps(provenance, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(args.out.resolve() / "players.zip")


if __name__ == "__main__":
    main()
