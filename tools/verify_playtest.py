"""Verify a packaged playtest against its private host/PROVENANCE.json receipt."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import zipfile


def digest(data):
    return hashlib.sha256(data).hexdigest()


def verify(folder):
    receipt = json.loads((folder / "host/PROVENANCE.json").read_text(encoding="utf-8"))
    if receipt["schema_version"] != 1:
        raise ValueError("unsupported provenance schema")
    bundle = folder / "players.zip"
    if digest(bundle.read_bytes()) != receipt["players_zip_sha256"]:
        raise ValueError("player ZIP hash mismatch")
    with zipfile.ZipFile(bundle) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)):
            raise ValueError("duplicate player ZIP members")
        actual = {name: digest(archive.read(name)) for name in names}
        if actual != receipt["player_files"]:
            raise ValueError("player ZIP members differ from provenance")
        with zipfile.ZipFile(io.BytesIO(archive.read("ootxmm.apworld"))) as world:
            names = world.namelist()
            if len(names) != len(set(names)):
                raise ValueError("duplicate world package members")
            actual = {name: digest(world.read(name)) for name in names}
            if actual != receipt["packaged_world_members"]:
                raise ValueError("world source members differ from provenance")
    for subfolder, expected in (("share", receipt["player_files"]),
                                ("host", receipt["host_files"])):
        actual = {path.relative_to(folder / subfolder).as_posix(): digest(path.read_bytes())
                  for path in (folder / subfolder).rglob("*")
                  if path.is_file() and path != folder / "host/PROVENANCE.json"}
        if actual != expected:
            raise ValueError(f"{subfolder} files differ from provenance")
    return receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folder", type=Path)
    args = parser.parse_args()
    try:
        receipt = verify(args.folder)
    except (ValueError, OSError, KeyError, zipfile.BadZipFile) as error:
        parser.exit(1, f"Verification failed: {error}\n")
    bound = receipt["validation"].get("patch_build_receipts_verified", False)
    print(f"Artifact integrity verified for {len(receipt['slots'])} slots; "
          f"patch build receipts verified at packaging: {bound}. "
          "Gameplay readiness requires separate validation.")


if __name__ == "__main__":
    main()
