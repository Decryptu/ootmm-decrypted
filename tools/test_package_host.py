"""Release bundle boundaries and argument handling without downloading a toolchain."""
import hashlib
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
import zipfile

from package_host import ROOT, package


class HostBundleTests(unittest.TestCase):
    def test_bundle_is_self_contained_and_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "host.zip"
            package(output)
            with zipfile.ZipFile(output) as archive:
                names = archive.namelist()
                self.assertIn("ootxmm-host/Host Setup.cmd", names)
                self.assertIn("ootxmm-host/ootmm-ap/ap-patch.ts", names)
                self.assertTrue(any("/ootmm-patches/" in name for name in names))
                self.assertFalse(any(name.endswith((".z64", ".ootxmm.json")) for name in names))
                self.assertNotIn(b"\r", archive.read("ootxmm-host/tools/ootmm-build.sh"))
                for name in names:
                    self.assertFalse(".." in Path(name).parts)
            self.assertEqual(output.with_suffix(".zip.sha256").read_text().split()[0],
                             hashlib.sha256(output.read_bytes()).hexdigest())
            with self.assertRaises(FileExistsError):
                package(output)

    def test_patch_mode_preserves_paths_and_propagates_failure(self):
        bash = shutil.which("bash") if os.name != "nt" else r"C:\Program Files\Git\bin\bash.exe"
        if not bash or not Path(bash).is_file():
            self.skipTest("Bash unavailable")
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            # Bash accepts forward-slash Windows drive paths under Git for Windows.
            base = folder.as_posix()
            if os.name == "nt":
                base = "/" + base[0].lower() + base[2:]
            (folder / "bin").mkdir()
            (folder / "src").mkdir()
            (folder / "repo/ootmm-patches").mkdir(parents=True)
            (folder / "repo/ootmm-ap").mkdir()
            (folder / "repo/ootmm-ap/ap-patch.ts").write_text("test")
            (folder / "oot rom.z64").write_bytes(b"oot")
            (folder / "mm rom.z64").write_bytes(b"mm")
            for name, body in {
                "git": "exit 0",
                "podman": 'printf \'%s\\n\' "$@" > "$HOST_TEST_LOG"; exit "$HOST_TEST_EXIT"',
            }.items():
                mock = folder / "bin" / name
                mock.write_text("#!/bin/sh\n" + body + "\n")
                mock.chmod(0o755)
            script = folder / "build.sh"
            script.write_text((ROOT / "tools/ootmm-build.sh").read_text().replace(
                "SRC=/root/ootmm", 'SRC="' + base + '/src"'))
            seed = base + "/seed space ' quote $literal; text"
            output = base + "/output space ' quote $literal; text"
            env = dict(os.environ, HOST_TEST_LOG=base + "/args", HOST_TEST_EXIT="0")
            command = [bash, "-c", 'export PATH="$1/bin:$PATH"; shift; exec sh "$@"',
                       "test", base, base + "/build.sh", base + "/repo", "--patch-seed",
                       seed, base + "/oot rom.z64", base + "/mm rom.z64", output]
            result = subprocess.run(command, env=env, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            args = (folder / "args").read_text().splitlines()
            self.assertEqual(args[-3:], ["sh", seed, output])
            self.assertEqual((folder / "src/roms/oot.z64").read_bytes(), b"oot")
            env["HOST_TEST_EXIT"] = "23"
            self.assertEqual(subprocess.run(command, env=env, capture_output=True).returncode, 23)


if __name__ == "__main__":
    unittest.main()
