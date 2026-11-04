"""Packs the world into ootxmm.apworld, or copies it into a folder.

The repository root is the world package, next to files that are not part of it (tools, repo
docs, the metadata generator's inputs and intermediates). WORLD_FILES lists what goes in; anything
else stays out, so a new world file must be added here.

    python tools/build_apworld.py dist/ootxmm.apworld
    python tools/build_apworld.py --dir <archipelago>/worlds/ootxmm
"""
import argparse
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = "ootxmm"
WORLD_FILES = [
    "__init__.py",
    "archipelago.json",
    "client.py",
    "items.py",
    "locations.py",
    "logic.py",
    "time_logic.py",
    "ootxmm_staticdata.py",
    "options.py",
    "prefill.py",
    "regions.py",
    "rules.py",
    "web_world.py",
    "world.py",
    "LICENSE",
    "docs/en_OOTxMM.md",
    "docs/setup_en.md",
    # The only metadata the world reads at runtime (ootxmm_staticdata.py).
    "raw/GreatWorldJSONdump.json",
    "raw/GreatLogicJSONdump.json",
    "raw/LocationIDs.json",
    "raw/GreatCheckItemJSONdump.json",
    "raw/GreatCheckInfoJSONdump.json",
    "raw/GreatFillJSONdump.json",
    "raw/GreatSettingsJSONdump.json",
    "raw/GreatItemJSONdump.json",
    "raw/ItemIDs.json",
]
WORLD_DIRS = ["test"]


def world_files():
    files = [ROOT / name for name in WORLD_FILES]
    for name in WORLD_DIRS:
        folder = ROOT / name
        if folder.is_dir():
            files += [p for p in folder.rglob("*") if p.is_file() and "__pycache__" not in p.parts]
    missing = [str(p) for p in files if not p.is_file()]
    if missing:
        raise SystemExit("missing world files: " + ", ".join(missing))
    return sorted(files)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("out", nargs="?", help="the .apworld to write")
    parser.add_argument("--dir", help="copy the world into this folder instead")
    args = parser.parse_args()
    if bool(args.out) == bool(args.dir):
        parser.error("give either an .apworld path or --dir")

    if args.dir:
        dest = Path(args.dir)
        if dest.exists():
            shutil.rmtree(dest)
        for src in world_files():
            target = dest / src.relative_to(ROOT)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, target)
        return

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
        for src in world_files():
            zf.write(src, f"{PACKAGE}/{src.relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
    main()
