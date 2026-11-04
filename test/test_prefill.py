from types import SimpleNamespace
from unittest import TestCase
from unittest.mock import patch

from Fill import FillError

from .. import items, ootxmm_staticdata, prefill
from .test_options import OOTxMMTestBase


def symbolic(item) -> str:
    return items.ITEM_BY_NAME[item.name].symbolic_id


class TestPreFillRetry(TestCase):
    def test_reward_failure_retries_local_placements(self) -> None:
        local_item = SimpleNamespace(location=None)
        reward = SimpleNamespace(location=None)
        local = SimpleNamespace(item=None, locked=False)
        reward_location = SimpleNamespace(item=None, locked=False)
        world = SimpleNamespace(player=1, pre_fill_pending=[local_item, reward])
        multiworld = SimpleNamespace(get_game_worlds=lambda game: [world],
                                     get_unfilled_locations=lambda: [local, reward_location])
        calls = 0

        def local_fill(world):
            self.assertIsNone(local.item)
            self.assertIsNone(local_item.location)
            self.assertIsNone(reward_location.item)
            self.assertIsNone(reward.location)
            self.assertFalse(local.locked)
            self.assertEqual(world.pre_fill_pending, [local_item, reward])
            local.item = local_item
            local_item.location = local
            local.locked = True
            world.pre_fill_pending = [reward]

        def reward_fill(multiworld):
            nonlocal calls
            calls += 1
            reward_location.item = reward
            reward.location = reward_location
            reward_location.locked = True
            world.pre_fill_pending.clear()
            if calls == 1:
                raise FillError("Local placements blocked rewards")

        with patch.object(prefill, "pre_fill", side_effect=local_fill), \
                patch.object(prefill, "place_dungeon_rewards", side_effect=reward_fill):
            prefill.pre_fill_all(multiworld)
        self.assertEqual(calls, 2)
        self.assertEqual(world.pre_fill_pending, [])
        self.assertIs(local.item, local_item)
        self.assertIs(reward_location.item, reward)

    def test_partial_placement_is_cleared_before_retry(self) -> None:
        item = SimpleNamespace(location=None)
        filled = SimpleNamespace(item=item, locked=True)
        empty = SimpleNamespace(item=None, locked=False)
        world = SimpleNamespace(pre_fill_pending=[item])
        calls = 0

        def place_group(world, items, names, placed):
            nonlocal calls
            calls += 1
            self.assertEqual(world.pre_fill_pending, [item])
            if calls == 1:
                world.pre_fill_pending.clear()
                item.location = filled
                placed.extend([filled, empty])
                raise FillError("Partial placement")
            self.assertIsNone(item.location)
            self.assertIsNone(filled.item)
            self.assertFalse(filled.locked)
            self.assertIsNone(empty.item)
            world.pre_fill_pending.clear()

        with patch.object(prefill, "_groups", return_value=[(set(), set())]), \
                patch.object(prefill, "_place_group", side_effect=place_group):
            prefill.pre_fill(world)
        self.assertEqual(calls, 2)
        self.assertEqual(world.pre_fill_pending, [])


class TestPreFill(OOTxMMTestBase):
    # Where OoTMM's defaults put items, which the ROM relies on (prefill.py).
    def test_fixed_checks_keep_their_vanilla_item(self) -> None:
        for location in self.multiworld.get_locations(self.player):
            if location.name in prefill.fixed_checks(self.world):
                self.assertEqual(symbolic(location.item), ootxmm_staticdata.OOTxMMCheckItems[location.name], location.name)

    def test_items_stay_where_ootmm_puts_them(self) -> None:
        for location in self.multiworld.get_locations(self.player):
            if location.address is None or location.item is None or location.item.player != self.player or location.name in prefill.fixed_checks(self.world):
                continue
            for group_items, group_locations in prefill._groups(self.world):
                if symbolic(location.item) in group_items - prefill.FAIRY_ITEMS:
                    self.assertIn(location.name, group_locations, f"{location.item.name} at {location.name}")

    def test_no_item_left_unplaced(self) -> None:
        self.assertEqual(self.world.get_pre_fill_items(), [])


class TestDungeonAnywhere(TestPreFill):
    options = {key: "anywhere" for key in prefill.DUNGEON_SETTINGS}

    def test_dungeon_items_enter_main_fill(self) -> None:
        shuffled = set().union(*prefill.DUNGEON_SETTINGS.values())
        found = {symbolic(item) for item in self.multiworld.itempool if item.player == self.player}
        # WorldTestBase runs pre-fill, leaving unrestricted items in the main pool.
        self.assertTrue(shuffled <= found)
        self.assertFalse(any(shuffled & group for group, _ in prefill._groups(self.world)))


class TestDungeonRemoved(TestPreFill):
    options = {key: "removed" for key in prefill.DUNGEON_SETTINGS}

    def test_removed_items_are_absent(self) -> None:
        removed = set().union(*prefill.DUNGEON_SETTINGS.values())
        placed = {symbolic(item) for item in self.multiworld.get_items() if item.name in items.ITEM_BY_NAME}
        self.assertFalse(placed & removed)
        self.assertIn("OOT_SMALL_KEY_GF", placed)


class TestStartingMaps(TestPreFill):
    options = {"mapCompassShuffle": "starting"}

    def test_maps_are_granted_by_rom_instead_of_pickups(self) -> None:
        maps = prefill.DUNGEON_SETTINGS["mapCompassShuffle"]
        placed = {symbolic(item) for item in self.multiworld.get_items() if item.name in items.ITEM_BY_NAME}
        self.assertFalse(placed & maps)
        self.assertEqual(self.world.fill_slot_data()["settings"]["mapCompassShuffle"], "starting")
        self.assertFalse(any(maps & group for group, _ in prefill._groups(self.world)))
        # The ROM grants these directly; server delivery would grant a duplicate on connection.
        self.assertFalse(any(symbolic(item) in maps for item in self.multiworld.precollected_items[self.player]))


class TestDungeonMixed(TestPreFill):
    options = {"mapCompassShuffle": "removed", "bossKeyShuffleOot": "anywhere", "bossKeyShuffleMm": "ownDungeon"}

    def test_games_keep_independent_settings(self) -> None:
        placed = {symbolic(item) for item in self.multiworld.get_items() if item.name in items.ITEM_BY_NAME}
        self.assertFalse(placed & prefill.DUNGEON_SETTINGS["mapCompassShuffle"])
        self.assertTrue(prefill.DUNGEON_SETTINGS["bossKeyShuffleOot"] <= placed)
        self.assertTrue(prefill.DUNGEON_SETTINGS["bossKeyShuffleMm"] <= placed)
        self.assertEqual(self.world.fill_slot_data()["settings"]["bossKeyShuffleOot"], "anywhere")


class TestSmallKeyCounts(TestPreFill):
    expected_fire_keys = 7

    def test_fire_key_count(self) -> None:
        keys = [item for item in self.multiworld.get_items()
                if item.name in items.ITEM_BY_NAME and symbolic(item) == "OOT_SMALL_KEY_FIRE"]
        self.assertEqual(len(keys), self.expected_fire_keys)


class TestSmallKeyAnywhereCounts(TestSmallKeyCounts):
    options = {"smallKeyShuffleOot": "anywhere", "smallKeyShuffleMm": "anywhere"}
    expected_fire_keys = 8


class FairyPlacementTests(TestPreFill):
    def test_fairy_counts_and_restrictions(self) -> None:
        from collections import Counter
        fixed = prefill.fixed_checks(self.world)
        expected = Counter(ootxmm_staticdata.OOTxMMCheckItems[name] for name in prefill.FAIRY_LOCATIONS)
        found = Counter(symbolic(item) for item in self.multiworld.get_items()
                        if item.name in items.ITEM_BY_NAME and symbolic(item) in prefill.FAIRY_ITEMS)
        self.assertEqual(found, expected)
        unrestricted = Counter(ootxmm_staticdata.OOTxMMCheckItems[name]
                               for key, names in prefill.FAIRY_SETTINGS.items()
                               if self.world.ootmm_settings[key] == "anywhere" for name in names)
        main_pool = Counter(symbolic(item) for item in self.multiworld.itempool
                            if item.player == self.player and symbolic(item) in prefill.FAIRY_ITEMS)
        self.assertEqual(main_pool, unrestricted)
        for group, locations in prefill.DUNGEON_GROUPS:
            for location in self.multiworld.get_locations(self.player):
                if location.item and location.item.name in items.ITEM_BY_NAME and symbolic(location.item) in group & prefill.FAIRY_ITEMS and location.locked and location.name not in fixed:
                    self.assertIn(location.name, locations)


class TestFairiesVanilla(FairyPlacementTests):
    options = {key: "vanilla" for key in prefill.FAIRY_SETTINGS}


class TestFairiesOwnDungeon(FairyPlacementTests):
    options = {key: "ownDungeon" for key in prefill.FAIRY_SETTINGS}


class TestFairiesAnywhere(FairyPlacementTests):
    options = {key: "anywhere" for key in prefill.FAIRY_SETTINGS}


class TestFairiesChestAnywhere(FairyPlacementTests):
    options = {"strayFairyChestShuffle": "anywhere", "strayFairyOtherShuffle": "ownDungeon"}


class TestFairiesOtherAnywhere(FairyPlacementTests):
    options = {"strayFairyChestShuffle": "ownDungeon", "strayFairyOtherShuffle": "anywhere"}


class TestFairiesChestVanilla(FairyPlacementTests):
    options = {"strayFairyChestShuffle": "vanilla", "strayFairyOtherShuffle": "anywhere"}


class TestFairiesChestOwnOtherVanilla(FairyPlacementTests):
    options = {"strayFairyChestShuffle": "ownDungeon", "strayFairyOtherShuffle": "vanilla"}


class TestFairiesChestVanillaOtherOwn(FairyPlacementTests):
    options = {"strayFairyChestShuffle": "vanilla", "strayFairyOtherShuffle": "ownDungeon"}


class TestFairiesChestAnywhereOtherVanilla(FairyPlacementTests):
    options = {"strayFairyChestShuffle": "anywhere", "strayFairyOtherShuffle": "vanilla"}


class TestSongsOnSongLocations(TestPreFill):
    options = {"songs": "songLocations"}

    def test_songs_are_local_and_restricted(self) -> None:
        from collections import Counter
        available = {location.name for location in self.multiworld.get_locations(self.player)}
        expected = Counter(item for name, item in ootxmm_staticdata.OOTxMMCheckItems.items()
                           if name in available and item in prefill.SONG_ITEMS)
        found = Counter()
        for location in self.multiworld.get_locations(self.player):
            if location.item and location.item.name in items.ITEM_BY_NAME and symbolic(location.item) in prefill.SONG_ITEMS:
                found[symbolic(location.item)] += 1
                self.assertIn(location.name, prefill.SONG_LOCATIONS)
                self.assertEqual(location.item.player, self.player)
                self.assertTrue(location.locked)
        self.assertEqual(found, expected)
        self.assertTrue(found)
        self.assertFalse(any(symbolic(item) in prefill.SONG_ITEMS
                             for item in self.multiworld.itempool if item.player == self.player))


class TestSongsAnywhere(TestPreFill):
    options = {"songs": "anywhere"}

    def test_all_songs_enter_main_fill(self) -> None:
        from collections import Counter
        available = {location.name for location in self.multiworld.get_locations(self.player)}
        expected = Counter(item for name, item in ootxmm_staticdata.OOTxMMCheckItems.items()
                           if name in available and item in prefill.SONG_ITEMS)
        found = Counter(symbolic(item) for item in self.multiworld.itempool
                        if item.player == self.player and symbolic(item) in prefill.SONG_ITEMS)
        self.assertEqual(found, expected)
        self.assertTrue(found)
        self.assertFalse(any(group & prefill.SONG_ITEMS for group, _ in prefill._groups(self.world)))
        self.assertEqual(self.world.fill_slot_data()["settings"]["songs"], "anywhere")


class TestSongsAnywhereWithDungeonShuffle(TestSongsAnywhere):
    options = {"songs": "anywhere", **{key: "anywhere" for key in prefill.DUNGEON_SETTINGS},
               **{key: "anywhere" for key in prefill.FAIRY_SETTINGS}}


class TestRewardsBlueWarps(TestPreFill):
    options = {"dungeonRewardShuffle": "dungeonBlueWarps"}

    def test_all_rewards_are_local_on_warps(self) -> None:
        from collections import Counter
        expected = Counter(item for item in ootxmm_staticdata.OOTxMMCheckItems.values()
                           if item in prefill.REWARD_ITEMS)
        found = Counter()
        for location in self.multiworld.get_locations(self.player):
            if location.item and location.item.name in items.ITEM_BY_NAME and symbolic(location.item) in prefill.REWARD_ITEMS:
                found[symbolic(location.item)] += 1
                self.assertIn(location.name, prefill.WARP_LOCATIONS)
                self.assertEqual(location.item.player, self.player)
                self.assertTrue(location.locked)
        self.assertEqual(found, expected)
        self.assertEqual(sum(found.values()), 13)


class TestRewardsAnywhere(TestPreFill):
    options = {"dungeonRewardShuffle": "anywhere"}

    def test_all_rewards_enter_main_fill(self) -> None:
        from collections import Counter
        expected = Counter(item for item in ootxmm_staticdata.OOTxMMCheckItems.values()
                           if item in prefill.REWARD_ITEMS)
        found = Counter(symbolic(item) for item in self.multiworld.itempool
                        if item.player == self.player and symbolic(item) in prefill.REWARD_ITEMS)
        self.assertEqual(found, expected)
        self.assertEqual(sum(found.values()), 13)
        self.assertFalse(any(group & prefill.REWARD_ITEMS for group, _ in prefill._groups(self.world)))
        self.assertEqual(self.world.fill_slot_data()["settings"]["dungeonRewardShuffle"], "anywhere")


class TestRewardsAnywhereWithOtherShuffles(TestRewardsAnywhere):
    options = {"dungeonRewardShuffle": "anywhere", "songs": "anywhere",
               **{key: "anywhere" for key in prefill.DUNGEON_SETTINGS},
               **{key: "anywhere" for key in prefill.FAIRY_SETTINGS}}


class TestRewardsDungeons(TestPreFill):
    options = {"dungeonRewardShuffle": "dungeons"}

    def test_rewards_stay_in_eligible_dungeons(self) -> None:
        from collections import Counter
        expected = Counter(item for item in ootxmm_staticdata.OOTxMMCheckItems.values()
                           if item in prefill.REWARD_ITEMS)
        found = Counter()
        eligible = prefill.reward_locations(self.world)
        for location in self.multiworld.get_locations():
            if location.item and location.item.name in items.ITEM_BY_NAME and symbolic(location.item) in prefill.REWARD_ITEMS:
                found[symbolic(location.item)] += 1
                self.assertIn(location.name, eligible)
                self.assertTrue(location.locked)
        self.assertEqual(found, expected)
        self.assertEqual(sum(found.values()), 13)
        self.assertFalse(any(symbolic(item) in prefill.REWARD_ITEMS for item in self.multiworld.itempool))


class TestRewardsDungeonsWithOtherShuffles(TestRewardsDungeons):
    options = {"dungeonRewardShuffle": "dungeons", "songs": "anywhere",
               **{key: "anywhere" for key in prefill.DUNGEON_SETTINGS},
               **{key: "anywhere" for key in prefill.FAIRY_SETTINGS}}


class TestRewardsDungeonsLimited(TestRewardsDungeons):
    options = {"dungeonRewardShuffle": "dungeonsLimited"}

    def test_one_reward_per_dungeon(self) -> None:
        for dungeon in prefill._fill["rewardDungeons"]:
            names = set(prefill._fill["dungeons"][dungeon])
            if dungeon == "ST":
                names |= set(prefill._fill["dungeons"]["IST"])
            locations = [location for location in self.multiworld.get_locations(self.player)
                         if location.name in names]
            rewards = [location for location in locations if location.item
                       and location.item.game == "OOTxMM" and symbolic(location.item) in prefill.REWARD_ITEMS]
            self.assertLessEqual(len(rewards), 1, dungeon)
            if rewards:
                for location in locations:
                    if location is not rewards[0]:
                        self.assertFalse(location.item_rule(rewards[0].item), location.name)

    def test_mixed_rewards_cannot_share_stone_tower(self) -> None:
        from copy import copy
        normal = next(location for location in self.multiworld.get_locations(self.player)
                      if location.name in prefill._fill["dungeons"]["ST"])
        inverted = next(location for location in self.multiworld.get_locations(self.player)
                        if location.name in prefill._fill["dungeons"]["IST"])
        reward = next(location.item for location in self.multiworld.get_locations()
                      if location.item and location.item.game == "OOTxMM"
                      and symbolic(location.item) in prefill.REWARD_ITEMS)
        unrestricted = copy(reward)
        unrestricted.player = self.player + 1000
        dungeon_locations = [location for location in self.multiworld.get_locations(self.player)
                             if location.name in set(prefill._fill["dungeons"]["ST"])
                             | set(prefill._fill["dungeons"]["IST"])]
        saved = [(location, location.item) for location in dungeon_locations]
        try:
            for location in dungeon_locations:
                location.item = None
            normal.item = reward
            self.assertFalse(inverted.item_rule(unrestricted))
            normal.item = unrestricted
            self.assertFalse(inverted.item_rule(reward))
            self.assertTrue(inverted.item_rule(unrestricted))
        finally:
            for location, item in saved:
                location.item = item


class TestRewardsDungeonsLimitedWithOtherShuffles(TestRewardsDungeonsLimited):
    options = {"dungeonRewardShuffle": "dungeonsLimited", "songs": "anywhere",
               **{key: "anywhere" for key in prefill.DUNGEON_SETTINGS},
               **{key: "anywhere" for key in prefill.FAIRY_SETTINGS}}


class StartingFairyTests(TestPreFill):
    expected_starting = 0
    def test_native_grants_and_remaining_pool(self) -> None:
        from collections import Counter
        from ..time_logic import evaluate, INITIAL
        expected = prefill.starting_fairies(self.world.ootmm_settings)
        self.assertEqual(sum(expected.values()), self.expected_starting)
        found = Counter(symbolic(item) for item in self.multiworld.get_items()
                        if item.name in items.ITEM_BY_NAME and symbolic(item) in prefill.FAIRY_ITEMS)
        original = Counter(ootxmm_staticdata.OOTxMMCheckItems[name] for name in prefill.FAIRY_LOCATIONS)
        self.assertEqual(found, original - expected)
        self.assertFalse(any(symbolic(item) in prefill.FAIRY_ITEMS
                             for item in self.multiworld.precollected_items[self.player]))
        _, counts = self.world.time_logic.solve(Counter())
        for item, count in expected.items():
            name = items.ITEM_BY_SYMBOLIC_ID[item].display_name
            self.assertEqual(counts[name], count)
            self.assertIsNotNone(evaluate(("item", item, count), INITIAL, counts))
            self.assertIsNone(evaluate(("item", item, count + 1), INITIAL, counts))
        available = {loc.name for loc in self.multiworld.get_locations(self.player)}
        other = prefill.FAIRY_SETTINGS["strayFairyOtherShuffle"]
        self.assertEqual(len(other & available), 0 if self.world.ootmm_settings["strayFairyOtherShuffle"] == "removed" else len(other))


class TestStartingChestFairies(StartingFairyTests):
    options = {"strayFairyChestShuffle": "starting", "strayFairyOtherShuffle": "anywhere"}
    expected_starting = 31


class TestStartingOtherFairies(StartingFairyTests):
    options = {"strayFairyChestShuffle": "ownDungeon", "strayFairyOtherShuffle": "starting"}
    expected_starting = 29


class TestStartingAllFairies(StartingFairyTests):
    options = {"strayFairyChestShuffle": "starting", "strayFairyOtherShuffle": "starting"}
    expected_starting = 60


class TestRemovedOtherFairies(StartingFairyTests):
    options = {"strayFairyChestShuffle": "anywhere", "strayFairyOtherShuffle": "removed"}
    expected_starting = 29


class TestStartingChestRemovedOtherFairies(StartingFairyTests):
    options = {"strayFairyChestShuffle": "starting", "strayFairyOtherShuffle": "removed"}
    expected_starting = 60


class TestTingleVanilla(TestPreFill):
    def test_tingle_map_pool(self) -> None:
        mode = self.world.ootmm_settings["tingleShuffle"]
        locations = {loc.name: loc for loc in self.multiworld.get_locations(self.player)}
        self.assertEqual(len(prefill.TINGLE_ITEMS), 6)
        self.assertTrue(prefill.TINGLE_LOCATIONS <= locations.keys())
        maps = [item for item in self.multiworld.get_items()
                if item.name in items.ITEM_BY_NAME and symbolic(item) in prefill.TINGLE_ITEMS]
        self.assertEqual(len(maps), 6 if mode in ("vanilla", "anywhere") else 0)
        self.assertFalse(any(symbolic(item) in prefill.TINGLE_ITEMS
                             for item in self.multiworld.precollected_items[self.player]))
        self.assertFalse(any(symbolic(item) in prefill.TINGLE_ITEMS
                             for item in self.world.get_pre_fill_items()))
        for name in prefill.TINGLE_LOCATIONS:
            self.assertEqual(name in prefill.fixed_checks(self.world), mode == "vanilla")
            self.assertEqual(locations[name].locked, mode == "vanilla")


class TestTingleAnywhere(TestTingleVanilla):
    options = {"tingleShuffle": "anywhere"}


class TestTingleStarting(TestTingleVanilla):
    options = {"tingleShuffle": "starting"}


class TestTingleRemoved(TestTingleVanilla):
    options = {"tingleShuffle": "removed"}

class TestGanonKeyRemoved(TestPreFill):
    options = {"ganonBossKey": "removed"}

    def test_ganon_key_pool_and_lock(self):
        mode = self.world.ootmm_settings["ganonBossKey"]
        key = "OOT_BOSS_KEY_GANON"
        found = [item for item in self.multiworld.get_items()
                 if item.name in items.ITEM_BY_NAME and symbolic(item) == key]
        self.assertEqual(len(found), int(mode != "removed"))
        fixed = prefill.fixed_checks(self.world)
        self.assertEqual("OOT Ganon Castle Boss Key" in fixed, mode == "vanilla")
        groups = [names for group, names in prefill._groups(self.world) if key in group]
        self.assertEqual(bool(groups), mode == "ganon")
        if mode == "ganon":
            self.assertIn(found[0].location.name, groups[0])
            self.assertTrue(found[0].location.locked)
        if mode == "anywhere":
            self.assertIn(found[0], self.multiworld.itempool)
        from collections import Counter
        from ..time_logic import evaluate, OOT_ALL, MM_ALL
        source = ("OOT Ganon Castle Tower Staircase Before Boss Door", "adult")
        cond = next(cond for target, cond in self.world.logic.exits[source]
                    if target == "OOT Ganon Castle Tower Lower Arena")
        data = (OOT_ALL, MM_ALL, 0, 0)
        self.assertEqual(evaluate(cond, data, Counter()) is not None, mode == "removed")
        display = items.ITEM_BY_SYMBOLIC_ID[key].display_name
        self.assertIsNotNone(evaluate(cond, data, Counter({display: 1})))


class TestGanonKeyVanilla(TestGanonKeyRemoved):
    options = {"ganonBossKey": "vanilla"}


class TestGanonKeyCastle(TestGanonKeyRemoved):
    options = {"ganonBossKey": "ganon"}


class TestGanonKeyAnywhere(TestGanonKeyRemoved):
    options = {"ganonBossKey": "anywhere"}
