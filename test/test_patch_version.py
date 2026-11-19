import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


@unittest.skipUnless((ROOT / "ootmm-ap").is_dir(), "needs the repository checkout")
class TestPatchVersion(unittest.TestCase):
    def test_builder_matches_world_version(self) -> None:
        """The ROM builder refuses seeds from other releases, so it must name this release."""
        manifest = json.loads((ROOT / "archipelago.json").read_text(encoding="utf-8"))
        source = (ROOT / "ootmm-ap" / "ap-patch.ts").read_text(encoding="utf-8")
        match = re.search(r"^const WORLD_VERSION = '([^']+)';", source, re.M)
        self.assertIsNotNone(match)
        self.assertEqual(match.group(1), manifest["world_version"])
