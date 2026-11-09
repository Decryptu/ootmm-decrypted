import hashlib
import json
import pkgutil
import unittest

from .test_options import OOTxMMTestBase
from .. import logic, rules, prefill
from .. import options as options_module
from ..options import PORTED_SETTINGS


class TestPortedSettings(unittest.TestCase):
    def test_ported_settings_are_handled(self) -> None:
        from .. import prices
        self.assertLessEqual(set(PORTED_SETTINGS), prices.SETTINGS | set(prefill.SHOP_SETTINGS) | logic.TRAVERSAL_SETTINGS | set(logic.POOL_TRANSFORMS) | set(logic.POOL_SETTINGS) | set(logic.OPTIONAL_ITEM_SETTINGS) | set(logic.SHARED_ITEM_SETTINGS) | set(logic.KEY_RING_SETTINGS) | set(logic.CHECK_SETTINGS) | set(rules.GOAL_SETTINGS) | set(prefill.DUNGEON_SETTINGS) | set(prefill.FAIRY_SETTINGS) | set(prefill.FIXED_SETTINGS) | prefill.MAP_SETTINGS | prefill.SONG_SETTINGS | prefill.REWARD_SETTINGS)


class TestOoTMMCheckSets(unittest.TestCase):
    # check_samples.json holds OoTMM's own check set for some settings (GenerateCheckSamples in
    # raw/GenerateMetadata.py): removed_checks must leave the same checks.
    def test_same_checks_as_ootmm(self) -> None:
        samples = json.loads(pkgutil.get_data(__name__, "check_samples.json").decode("utf-8"))
        names = set(logic.ootxmm_staticdata.OOTxMMCheckItems)
        for sample in samples:
            with self.subTest(settings=sample["settings"]):
                checks = names - logic.removed_checks({**logic.ootxmm_staticdata.OOTxMMSettingDefaults, **sample["settings"]})
                self.assertEqual(len(checks), sample["count"])
                self.assertEqual(hashlib.sha256("\n".join(sorted(checks)).encode("utf-8")).hexdigest(), sample["sha256"])


class TestDefaultChecks(OOTxMMTestBase):
    # OoTMM's defaults shuffle no pots or grass, and no Hyrule Castle tree without the Stone Mask.
    def test_unshuffled_checks_are_absent(self) -> None:
        names = {location.name for location in self.multiworld.get_locations(self.player)}
        self.assertNotIn("OOT Hyrule Castle Tree Guarded", names)
        info = logic._check_info["checks"]
        self.assertFalse([name for name in names if name in info and info[name][0] in ("pot", "grass")])
        self.assertIn("OOT Deku Tree Slingshot Chest", names)


class TestShuffledPotsAndGrass(OOTxMMTestBase):
    options = {
        "shufflePotsOot": "dungeons",
        "shuffleGrassMm": "all",
        "shuffleTFGrassMm": True,
    }

    def test_shuffled_checks_exist(self) -> None:
        names = {location.name for location in self.multiworld.get_locations(self.player)}
        info = logic._check_info["checks"]
        pots = {name for name, (t, _, dungeon) in info.items() if name.startswith("OOT ") and t == "pot"}
        self.assertTrue(any(name in names for name in pots if info[name][2]))
        self.assertFalse(any(name in names for name in pots if not info[name][2]))
        termina_grass = {name for name, (t, scene, _) in info.items() if t == "grass" and scene == "MM_TERMINA_FIELD"}
        self.assertTrue(termina_grass & names)


class TestEverythingShuffled(OOTxMMTestBase):
    # Every check filter on: the largest pool must still generate and be beatable.
    options = {key: "all" if hasattr(getattr(options_module, f"OOTxMM_{key}"), "option_all") else True
               for key in PORTED_SETTINGS if key in logic.CHECK_SETTINGS}
