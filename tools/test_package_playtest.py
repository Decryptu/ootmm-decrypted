"""Packaging integrity checks; run: python -m unittest discover -s tools -p test_package_playtest.py."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

import package_playtest
import verify_playtest


class PackageTest(unittest.TestCase):
    def test_archive_manifest_loads_with_archipelago(self):
        try:
            from worlds.Files import APWorldContainer
        except ModuleNotFoundError as error:
            if error.name == "worlds":
                self.skipTest("Requires Archipelago on PYTHONPATH")
            raise
        scratch = package_playtest.ROOT / "dist"
        scratch.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=scratch) as temporary:
            package = Path(temporary) / "ootxmm.apworld"
            subprocess.run([sys.executable, str(package_playtest.ROOT / "tools/build_apworld.py"),
                            str(package)], check=True)
            container = APWorldContainer(str(package))
            container.read()
            self.assertEqual(container.game, "OOTxMM")
            self.assertEqual(container.minimum_ap_version, (0, 6, 8))
            self.assertEqual(container.world_version, (0, 0, 1))

    def test_receipt_binding_and_private_files(self):
        scratch = package_playtest.ROOT / "dist"
        scratch.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=scratch) as temporary:
            root = Path(temporary)
            patches = root / "patches"
            patches.mkdir()
            placement = json.dumps({"version": 1, "seed": "123-1", "settings": {"goal": "both"}}).encode()
            validation = root / "validation.json"
            validation.write_text('{"pending": ["gameplay"]}', encoding="utf-8")
            seed = root / "AP_123.zip"
            with zipfile.ZipFile(seed, "w") as archive:
                archive.writestr("AP_123_P1_Link.ootxmm.json", placement)
                archive.writestr("AP_123.archipelago", b"private server")
                archive.writestr("AP_123_Spoiler.txt", b"private spoiler")
            patch = patches / "AP_123_P1_Link.ootxmm.ootmm"
            patch.write_bytes(b"diagnostic patch")
            inputs = {path.relative_to(package_playtest.ROOT).as_posix(): package_playtest.sha256(path)
                      for folder in ("ootmm-ap", "ootmm-patches")
                      for path in (package_playtest.ROOT / folder).rglob("*") if path.is_file()}
            receipt = {"schema_version": 1, "seed": "123-1",
                       "placement": {"name": "AP_123_P1_Link.ootxmm.json", "sha256": hashlib.sha256(placement).hexdigest()},
                       "patch": {"name": patch.name, "sha256": package_playtest.sha256(patch)},
                       "builder_sha256": inputs["ootmm-ap/ap-patch.ts"], "patch_inputs": inputs}
            receipt_path = patch.with_suffix(".build.json")

            def package(name):
                out = root / name
                result = subprocess.run([sys.executable, str(package_playtest.ROOT / "tools/package_playtest.py"),
                                         "--seed", str(seed), "--patches", str(patches), "--out", str(out),
                                         "--require-build-receipts", "--validation-report", str(validation)], capture_output=True, text=True)
                return result, out

            result, out = package("missing")
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(out.exists())
            for field in ("seed", "placement", "patch", "builder_sha256", "patch_inputs"):
                with self.subTest(field=field):
                    changed = dict(receipt)
                    changed[field] = "mismatch"
                    receipt_path.write_text(json.dumps(changed), encoding="utf-8")
                    result, out = package(field)
                    self.assertNotEqual(result.returncode, 0, result.stdout)
                    self.assertIn("receipt does not match", result.stderr)
                    self.assertFalse(out.exists())
            receipt_path.write_text(json.dumps(receipt), encoding="utf-8")
            result, out = package("valid")
            self.assertEqual(result.returncode, 0, result.stderr)
            report = verify_playtest.verify(out)
            self.assertTrue(report["validation"]["patch_build_receipts_verified"])
            self.assertEqual((out / "host/VALIDATION.json").read_bytes(), validation.read_bytes())
            with zipfile.ZipFile(out / "players.zip") as archive:
                self.assertNotIn("VALIDATION.json", archive.namelist())
                self.assertFalse(any(name.endswith((".build.json", ".archipelago", "_Spoiler.txt", ".z64"))
                                     for name in archive.namelist()))
            for relative in ("share/PLAYTEST.md", "host/AP_123.archipelago", "players.zip"):
                with self.subTest(tampered=relative):
                    artifact = out / relative
                    original = artifact.read_bytes()
                    artifact.write_bytes(original + b"changed")
                    with self.assertRaises(ValueError):
                        verify_playtest.verify(out)
                    artifact.write_bytes(original)
            result, _ = package("valid")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("output directory already exists", result.stderr)


if __name__ == "__main__":
    unittest.main()
