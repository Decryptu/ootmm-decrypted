import unittest
from collections import Counter

from .test_options import OOTxMMTestBase
from .. import items, logic, prefill, time_logic


class LullabyTestBase(OOTxMMTestBase):
    def test_pool_and_song_locations(self):
        settings = self.world.ootmm_settings
        pool = Counter(items.ITEM_BY_NAME[i.name].symbolic_id for i in self.multiworld.get_items()
                       if i.player == self.player and i.code)
        shared = settings["sharedSongGoron"]
        for game, enabled, mode in (("MM", not shared, settings["progressiveGoronLullabyMm"]),
                                    ("OOT", settings["songGoronOot"] and not shared,
                                     settings["progressiveGoronLullabyOot"]),
                                    ("SHARED", shared, settings["progressiveGoronLullabyMm"])):
            self.assertEqual(pool[game + "_SONG_GORON"], int(enabled and mode == "single"))
            self.assertEqual(pool[game + "_SONG_GORON_HALF"], 2 if enabled and mode == "progressive" else 0)
        self.assertEqual("MM Goron Baby" in prefill.song_locations(settings),
                         settings["progressiveGoronLullabyMm"] == "progressive")
        if settings["songs"] == "songLocations":
            for location in self.multiworld.get_filled_locations(self.player):
                if location.item.code and items.ITEM_BY_NAME[location.item.name].symbolic_id in prefill.SONG_ITEMS:
                    self.assertIn(location.name, prefill.song_locations(settings))
        self.assertIn("MM Goron Baby", self.world.logic.checks)
        self.assertEqual(self.world.fill_slot_data()["settings"], settings)

    def test_snowhead_needs_full_lullaby(self):
        settings = self.world.ootmm_settings
        inventory = Counter({items.ITEM_BY_SYMBOLIC_ID[symbol].display_name: 99
                             for symbol in self.world.logic.items})
        inventory.update({event: 1 for event in self.world.logic.events})
        for game in ("MM", "SHARED"):
            for suffix in ("GORON", "GORON_HALF"):
                inventory.pop(items.ITEM_BY_SYMBOLIC_ID[game + "_SONG_" + suffix].display_name, None)
        conditions = [cond for _, _, cond in self.world.logic.events["MM_OPEN_SNOWHEAD_TEMPLE"]]
        def unlocked():
            return any(time_logic.evaluate(c, time_logic.ANY_TIME, inventory) is not None for c in conditions)
        self.assertFalse(unlocked())
        prefix = "SHARED_" if settings["sharedSongGoron"] else "MM_"
        progressive = settings["progressiveGoronLullabyMm"] == "progressive"
        name = items.ITEM_BY_SYMBOLIC_ID[prefix + "SONG_GORON" + ("_HALF" if progressive else "")].display_name
        inventory[name] = 1
        self.assertEqual(unlocked(), not progressive)
        inventory[name] = 2
        self.assertTrue(unlocked())


class TestDefaultLullaby(LullabyTestBase):
    options = {}


class TestSingleLullaby(LullabyTestBase):
    options = {"progressiveGoronLullabyMm": "single"}


class TestSeparateProgressiveLullabies(LullabyTestBase):
    options = {"songGoronOot": True, "songs": "anywhere"}


class TestSeparateSingleLullabies(LullabyTestBase):
    options = {"songGoronOot": True, "progressiveGoronLullabyMm": "single",
               "progressiveGoronLullabyOot": "single", "songs": "anywhere"}


class TestSharedProgressiveLullaby(LullabyTestBase):
    options = {"songGoronOot": True, "sharedSongGoron": True}


class TestSharedSingleLullaby(LullabyTestBase):
    options = {"songGoronOot": True, "sharedSongGoron": True,
               "progressiveGoronLullabyMm": "single", "progressiveGoronLullabyOot": "single"}


class TestMismatchedLullabies(LullabyTestBase):
    options = {"songGoronOot": True, "sharedSongGoron": True,
               "progressiveGoronLullabyOot": "single", "songs": "anywhere"}

    def test_sharing_is_disabled(self):
        self.assertFalse(self.world.ootmm_settings["sharedSongGoron"])


class TestLullabyCache(unittest.TestCase):
    def test_sharing_has_its_own_graph(self):
        settings = dict(logic.ootxmm_staticdata.OOTxMMSettingDefaults)
        settings.update(songGoronOot=True, sharedSongGoron=False)
        separate = logic.build(settings)
        shared = logic.build({**settings, "sharedSongGoron": True})
        self.assertIsNot(separate, shared)
        self.assertIn("MM_SONG_GORON_HALF", separate.items)
        self.assertNotIn("MM_SONG_GORON_HALF", shared.items)
        self.assertIn("SHARED_SONG_GORON_HALF", shared.items)
        self.assertIs(separate, logic.build(settings))
