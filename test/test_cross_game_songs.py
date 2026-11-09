import unittest
from collections import Counter

from .test_options import OOTxMMTestBase
from .. import items, logic, prefill


ENABLE = {enable: True for enable, _ in logic.CROSS_GAME_SONGS.values()}
SHARE = {key: True for key in logic.CROSS_GAME_SONGS}
DUNGEON_ENABLE = {key: True for key in ("songAwakeningOot", "songZoraOot", "songOrderOot")}
DUNGEON_SHARE = {key: True for key in ("sharedSongAwakening", "sharedSongZora", "sharedSongOrder")}


class TestSeparateCrossGameSongs(OOTxMMTestBase):
    options = {**ENABLE, "songs": "anywhere"}

    def test_song_pool_and_placement(self):
        settings = self.world.ootmm_settings
        pool = Counter(items.ITEM_BY_NAME[item.name].symbolic_id
                       for item in self.multiworld.get_items() if item.player == self.player and item.code)
        for shared, (enable, added) in logic.CROSS_GAME_SONGS.items():
            game, suffix = added.split("_", 1)
            native = ("MM_" if game == "OOT" else "OOT_") + suffix
            combined = settings[shared]
            self.assertEqual(pool[added], int(settings[enable] and not combined))
            self.assertEqual(pool[native], int(not combined))
            self.assertEqual(pool["SHARED_" + suffix], int(combined))
            for symbol in (added, native, "SHARED_" + suffix):
                if not pool[symbol]:
                    self.assertNotIn(symbol, self.world.logic.items)
                    continue
                name = items.ITEM_BY_SYMBOLIC_ID[symbol].display_name
                locations = self.multiworld.find_item_locations(name, self.player)
                if settings["songs"] == "songLocations":
                    self.assertEqual(len(locations), 1)
                    self.assertIn(locations[0].name, prefill.SONG_LOCATIONS)
                else:
                    self.assertFalse(locations)
                    self.assertEqual(sum(i.name == name for i in self.multiworld.itempool), 1)
        self.assertEqual(self.world.fill_slot_data()["settings"], settings)


    def test_dungeon_song_logic_uses_correct_game(self):
        from .. import time_logic
        inventory = Counter({items.ITEM_BY_SYMBOLIC_ID[symbol].display_name: 99
                             for symbol in self.world.logic.items})
        inventory.update({event: 1 for event in self.world.logic.events})
        for enable, symbol in logic.CROSS_GAME_SONGS.values():
            if self.world.ootmm_settings[enable]:
                inventory[items.ITEM_BY_SYMBOLIC_ID[symbol].display_name] = 1
        for song, event in (("AWAKENING", "MM_OPEN_WOODFALL_TEMPLE"),
                            ("ZORA", "MM_TURTLE_WOKEN"),
                            ("ORDER", "MM_MOON_OPEN")):
            with self.subTest(song=song):
                missing = inventory.copy()
                shared = {"AWAKENING": "sharedSongAwakening", "ZORA": "sharedSongZora",
                          "ORDER": "sharedSongOrder"}[song]
                prefix = "SHARED_" if self.world.ootmm_settings[shared] else "MM_"
                missing.pop(items.ITEM_BY_SYMBOLIC_ID[prefix + "SONG_" + song].display_name)
                conditions = [cond for _, _, cond in self.world.logic.events[event]]
                self.assertTrue(any(time_logic.evaluate(cond, time_logic.ANY_TIME, inventory) is not None
                                    for cond in conditions))
                self.assertTrue(all(time_logic.evaluate(cond, time_logic.ANY_TIME, missing) is None
                                    for cond in conditions))


class TestSharedCrossGameSongs(TestSeparateCrossGameSongs):
    options = {**ENABLE, **SHARE}

    def test_shared_elegy_opens_mm_logic(self):
        from .. import time_logic
        inventory = Counter({items.ITEM_BY_SYMBOLIC_ID[symbol].display_name: 99
                             for symbol in self.world.logic.items})
        inventory.update({event: 1 for event in self.world.logic.events})
        missing = inventory.copy()
        missing.pop(items.ITEM_BY_SYMBOLIC_ID["SHARED_SONG_EMPTINESS"].display_name)
        data = (time_logic.OOT_ALL, time_logic.MM_ALL, 0, 0)
        conditions = [cond for parents in self.world.logic.checks.values()
                      for area, _, cond in parents if area.startswith("MM ")]
        self.assertTrue(any(time_logic.evaluate(cond, data, inventory) is not None
                            and time_logic.evaluate(cond, data, missing) is None
                            for cond in conditions))


class TestSharedCrossGameSongsAnywhere(TestSeparateCrossGameSongs):
    options = {**ENABLE, **SHARE, "songs": "anywhere"}


class TestDisabledCrossGameSongs(TestSeparateCrossGameSongs):
    options = SHARE

    def test_disabled_sharing(self):
        for key in SHARE:
            self.assertFalse(self.world.ootmm_settings[key])


class TestSeparateSunSong(TestSeparateCrossGameSongs):
    options = {"songSunMm": True, "songs": "anywhere"}


class TestSharedSunSong(TestSeparateCrossGameSongs):
    options = {"songSunMm": True, "sharedSongSun": True}


class TestSeparateDungeonSongs(TestSeparateCrossGameSongs):
    options = {**DUNGEON_ENABLE, "songs": "anywhere"}


class TestSharedDungeonSongs(TestSeparateCrossGameSongs):
    options = {**DUNGEON_ENABLE, **DUNGEON_SHARE}


class TestSongCapacity(unittest.TestCase):
    def test_overfull_song_locations_explain_options(self):
        from types import SimpleNamespace
        from unittest.mock import Mock, patch
        from Fill import FillError
        world = SimpleNamespace(player=1, ootmm_settings={"songs": "songLocations"},
                                multiworld=Mock())
        world.multiworld.get_unfilled_locations.return_value = []
        with patch.object(prefill, "_symbolic", return_value="OOT_SONG_TIME"):
            with self.assertRaisesRegex(FillError, "Use songs: anywhere or share more songs"):
                prefill.split_pool(world, [object()])
        self.assertFalse(hasattr(world, "pre_fill_pending"))
