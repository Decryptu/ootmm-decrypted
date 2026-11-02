"""Remove every game but OOTxMM from an Archipelago checkout used for testing.

Archipelago's generic tests run against every installed world, so another game's random
fill failure would fail our checks. Kept: `generic` (Archipelago's own world), `apquest`
(test/general/test_options.py uses it by name), `ootxmm`, and the shared libraries whose
folder starts with `_`.

    python tools/prune_worlds.py <archipelago checkout>
"""
import shutil
import sys
from pathlib import Path

KEEP = {"generic", "apquest", "ootxmm"}

worlds = Path(sys.argv[1]) / "worlds"
if not (worlds / "ootxmm").is_dir():
    sys.exit(f"{worlds / 'ootxmm'} is missing: copy the world in first")
for entry in worlds.iterdir():
    if entry.name in KEEP or entry.name.startswith(("_", ".")):
        continue
    if entry.is_dir():
        shutil.rmtree(entry)
    elif entry.suffix == ".apworld":
        entry.unlink()
