import unittest

from test.bases import WorldTestBase

from ..options import OOTxMM_tricks


class OOTxMMTestBase(WorldTestBase):
    game = "OOTxMM"


def door_of_time_conditions(test: WorldTestBase) -> list:
    return [cond for _, _, cond in test.world.logic.events["OOT_DOOR_OF_TIME_OPEN"]]


class TestDefaults(OOTxMMTestBase):
    def test_song_age_change_disabled(self) -> None:
        from .. import logic
        self.assertFalse(self.world.logic.age_changes)
        self.assertNotIn(logic.AGE_CHANGE_EVENT, self.world.logic.events)

    def test_door_of_time_needs_song(self) -> None:
        self.assertNotIn(True, door_of_time_conditions(self))

    def test_settings_for_the_patch(self) -> None:
        settings = self.world.fill_slot_data()["settings"]
        self.assertEqual(settings["doorOfTime"], "closed")
        self.assertEqual(settings["tricks"], sorted(OOTxMM_tricks.default))


class TestOpenWithEveryTrick(OOTxMMTestBase):
    # Settings and tricks that loosen conditions: the seed must still be beatable, and the logic must change.
    options = {
        "doorOfTime": "open",
        "dekuTree": "open",
        "openMaskShop": True,
        "agelessSwords": True,
        "agelessHookshot": True,
        "climbMostSurfacesOot": "logical",
        "tricks": OOTxMM_tricks.valid_keys,
    }

    def test_door_of_time_needs_nothing(self) -> None:
        self.assertIn(True, door_of_time_conditions(self))

    def test_settings_for_the_patch(self) -> None:
        settings = self.world.fill_slot_data()["settings"]
        self.assertEqual(settings["doorOfTime"], "open")
        self.assertTrue(settings["openMaskShop"])
        self.assertEqual(settings["tricks"], sorted(OOTxMM_tricks.valid_keys))


class TestAgeChangeAlways(OOTxMMTestBase):
    options = {"ageChange": "always"}

    def test_song_age_change_prerequisites(self) -> None:
        from collections import Counter
        from .. import items, logic, time_logic
        self.assertEqual(self.world.fill_slot_data()["settings"]["ageChange"], self.options["ageChange"])
        parents = self.world.logic.events[logic.AGE_CHANGE_EVENT]
        self.assertTrue(self.world.logic.age_changes)
        self.assertTrue(all(logic.can_change_age(area) for area, _ in self.world.logic.age_changes))
        data = time_logic.ANY_TIME
        ocarina = items.ITEM_BY_SYMBOLIC_ID["OOT_OCARINA"].display_name
        song = items.ITEM_BY_SYMBOLIC_ID["OOT_SONG_TIME"].display_name
        def unlocked(counts):
            return any(time_logic.evaluate(cond, data, counts) is not None for _, _, cond in parents)
        counts = Counter({ocarina: 1, song: 1, "OOT_TIME_TRAVEL": 1})
        self.assertEqual(unlocked(counts), self.options["ageChange"] == "always")
        counts[ocarina] = 2
        self.assertTrue(unlocked(counts))
        for missing in (song, "OOT_TIME_TRAVEL", ocarina):
            incomplete = counts.copy()
            del incomplete[missing]
            self.assertFalse(unlocked(incomplete), missing)
        for area, age in self.world.logic.age_changes:
            region = self.world.get_region(logic.region_name(area, age))
            self.assertTrue(any(e.connected_region.name == logic.region_name(area, "adult" if age == "child" else "child")
                                for e in region.exits))


class TestAgeChangeOcarinaOfTime(TestAgeChangeAlways):
    options = {"ageChange": "oot"}


class TestGoalBoth(OOTxMMTestBase):
    # The default goal: Ganon and Majora.
    def test_needs_both_bosses(self) -> None:
        state = self.multiworld.state.copy()
        state.collect(self.multiworld.get_location("MM_MAJORA", self.player).item, True)
        self.assertFalse(self.multiworld.completion_condition[self.player](state))
        state.collect(self.multiworld.get_location("OOT_GANON", self.player).item, True)
        self.assertTrue(self.multiworld.completion_condition[self.player](state))


class TestGoalGanon(OOTxMMTestBase):
    options = {"goal": "ganon"}

    def test_needs_ganon_only(self) -> None:
        state = self.multiworld.state.copy()
        state.collect(self.multiworld.get_location("MM_MAJORA", self.player).item, True)
        self.assertFalse(self.multiworld.completion_condition[self.player](state))
        state.collect(self.multiworld.get_location("OOT_GANON", self.player).item, True)
        self.assertTrue(self.multiworld.completion_condition[self.player](state))


class SkeletonKeyTests(OOTxMMTestBase):
    def test_key_doors(self) -> None:
        from collections import Counter
        from .. import items, time_logic
        for prefix, source, target, setting in (("OOT", "Forest Temple Main", "Forest Temple Maze", "skeletonKeyOot"),
                                                ("MM", "Woodfall Temple Main Entrance Ledge", "Woodfall Temple Maze", "skeletonKeyMm")):
            conditions = [cond for (parent, _), exits in self.world.logic.exits.items()
                          if parent == f"{prefix} {source}"
                          for area, cond in exits if area == f"{prefix} {target}"]
            self.assertTrue(conditions)
            data = (time_logic.OOT_ALL, time_logic.MM_ALL, 0, 0)
            for cond in conditions:
                self.assertIsNone(time_logic.evaluate(cond, data, Counter()))
                for key_prefix in ("OOT", "MM"):
                    counts = Counter({items.ITEM_BY_SYMBOLIC_ID[f"{key_prefix}_SKELETON_KEY"].display_name: 1})
                    succeeds = time_logic.evaluate(cond, data, counts) is not None
                    self.assertEqual(succeeds, bool(self.world.ootmm_settings[setting]) and prefix == key_prefix)

    def test_optional_keys(self) -> None:
        from collections import Counter
        from .. import items, logic
        pool = Counter(items.ITEM_BY_NAME[item.name].symbolic_id
                       for item in self.multiworld.itempool if item.player == self.player)
        for key, symbolic in logic.POOL_SETTINGS.items():
            enabled = bool(self.world.ootmm_settings[key])
            self.assertEqual(pool[symbolic], int(enabled))
            self.assertEqual(symbolic in self.world.logic.items, enabled)
            self.assertEqual(self.world.fill_slot_data()["settings"][key], enabled)
            if enabled:
                self.assertTrue(self.world.create_item(items.ITEM_BY_SYMBOLIC_ID[symbolic].display_name).advancement)
        alternate = {**self.world.ootmm_settings, "skeletonKeyOot": not self.world.ootmm_settings["skeletonKeyOot"]}
        other_graph = logic.build(alternate)
        self.assertIsNot(other_graph, self.world.logic)
        self.assertEqual("OOT_SKELETON_KEY" in other_graph.items, alternate["skeletonKeyOot"])
        self.assertIs(logic.build(self.world.ootmm_settings), self.world.logic)
        # Skeleton keys supplement ordinary keys, rather than replacing them.
        placed = [location.item for location in self.multiworld.get_locations(self.player)
                  if location.item and location.item.name in items.ITEM_BY_NAME]
        inventory = Counter(items.ITEM_BY_NAME[item.name].symbolic_id for item in placed + [item for item in self.multiworld.itempool if item.player == self.player])
        self.assertEqual(inventory["OOT_SMALL_KEY_FOREST"], 5)
        self.assertEqual(inventory["MM_SMALL_KEY_WF"], 1)


class TestSkeletonKeyOot(SkeletonKeyTests):
    options = {"skeletonKeyOot": True}


class TestSkeletonKeyMm(SkeletonKeyTests):
    options = {"skeletonKeyMm": True}


class TestSkeletonKeysBoth(SkeletonKeyTests):
    options = {"skeletonKeyOot": True, "skeletonKeyMm": True,
               "smallKeyShuffleOot": "anywhere", "smallKeyShuffleMm": "anywhere",
               "smallKeyShuffleHideout": "anywhere", "smallKeyShuffleChestGame": "anywhere"}


class KeyRingTests(OOTxMMTestBase):
    options = {"smallKeyRingOot": ["Forest"], "smallKeyRingMm": ["WF"]}
    def test_ring_pool_and_placement(self) -> None:
        from collections import Counter
        from .. import items, logic, prefill
        inventory = [loc.item for loc in self.multiworld.get_locations(self.player) if loc.item]
        inventory += [item for item in self.multiworld.itempool if item.player == self.player]
        counts = Counter(items.ITEM_BY_NAME[item.name].symbolic_id for item in inventory
                         if item.name in items.ITEM_BY_NAME)
        selected = logic.key_rings(self.world.ootmm_settings)
        for setting, members in logic.KEY_RING_SETTINGS.items():
            self.assertEqual(self.world.fill_slot_data()["settings"][setting], sorted(self.options[setting]))
            for key in members.values():
                ring = key.replace("SMALL_KEY", "KEY_RING")
                removed = prefill.removed_item(self.world, key)
                self.assertEqual(counts[ring], int(key in selected and not removed), ring)
                if key in selected:
                    self.assertEqual(counts[key], 0, key)
                elif not removed:
                    self.assertGreater(counts[key], 0, key)
                if counts[ring]:
                    placement = ("smallKeyShuffleHideout" if key == "OOT_SMALL_KEY_GF" else
                                 "smallKeyShuffleChestGame" if key == "OOT_SMALL_KEY_TCG" else
                                 "smallKeyShuffleOot" if key.startswith("OOT") else "smallKeyShuffleMm")
                    main_count = sum(item.name == items.ITEM_BY_SYMBOLIC_ID[ring].display_name
                                     and item.player == self.player for item in self.multiworld.itempool)
                    self.assertEqual(main_count, int(self.world.ootmm_settings[placement] == "anywhere"), ring)
                    self.assertTrue(self.world.create_item(items.ITEM_BY_SYMBOLIC_ID[ring].display_name).advancement)
                    if self.world.ootmm_settings["smallKeyShuffleOot" if key.startswith("OOT") else "smallKeyShuffleMm"] == "ownDungeon":
                        locations = set().union(*(names for members, names in prefill.DUNGEON_GROUPS if ring in members))
                        location = next(loc for loc in self.multiworld.get_locations(self.player)
                                        if loc.item and loc.item.name == items.ITEM_BY_SYMBOLIC_ID[ring].display_name)
                        self.assertIn(location.name, locations)
        alternate = {**self.world.ootmm_settings, "smallKeyRingOot": []}
        graph = logic.build(alternate)
        self.assertIsNot(graph, self.world.logic)
        self.assertIs(logic.build(self.world.ootmm_settings), self.world.logic)
        hideout = {**self.world.ootmm_settings, "smallKeyRingOot": ["GF"], "smallKeyShuffleHideout": "vanilla"}
        shuffled = {**hideout, "smallKeyShuffleHideout": "anywhere"}
        self.assertNotIn("OOT_KEY_RING_GF", logic.build(hideout).items)
        self.assertIn("OOT_KEY_RING_GF", logic.build(shuffled).items)
        self.assertIsNot(logic.build(hideout), logic.build(shuffled))
        native = {**self.world.ootmm_settings, **{key: {"type": "specific", "values": self.world.ootmm_settings[key]}
                                                for key in logic.KEY_RING_SETTINGS}}
        self.assertIs(logic.build(native), self.world.logic)

    def test_ring_opens_key_door(self) -> None:
        from collections import Counter
        from .. import items, time_logic
        for prefix, source, target, suffix in (("OOT", "Forest Temple Main", "Forest Temple Maze", "FOREST"),
                                                ("MM", "Woodfall Temple Main Entrance Ledge", "Woodfall Temple Maze", "WF")):
            conditions = [cond for (parent, _), exits in self.world.logic.exits.items()
                          if parent == f"{prefix} {source}" for area, cond in exits if area == f"{prefix} {target}"]
            self.assertTrue(conditions)
            data = (time_logic.OOT_ALL, time_logic.MM_ALL, 0, 0)
            for cond in conditions:
                if self.world.ootmm_settings[f"smallKeyShuffle{'Oot' if prefix == 'OOT' else 'Mm'}"] == "removed":
                    continue
                self.assertIsNone(time_logic.evaluate(cond, data, Counter()))
                ring = items.ITEM_BY_SYMBOLIC_ID[f"{prefix}_KEY_RING_{suffix}"].display_name
                self.assertIsNotNone(time_logic.evaluate(cond, data, Counter({ring: 1})))
                key = items.ITEM_BY_SYMBOLIC_ID[f"{prefix}_SMALL_KEY_{suffix}"].display_name
                self.assertIsNone(time_logic.evaluate(cond, data, Counter({key: 99})))


class TestKeyRingsOwnDungeon(KeyRingTests):
    options = {"smallKeyRingOot": ["Forest", "Fire", "Water", "Shadow", "Spirit", "BotW", "GTG", "Ganon", "GF", "TCG"],
               "smallKeyRingMm": ["WF", "SH", "GB", "ST"], "smallKeyShuffleChestGame": "ownDungeon"}


class TestKeyRingsAnywhere(KeyRingTests):
    options = {**TestKeyRingsOwnDungeon.options, "smallKeyShuffleOot": "anywhere", "smallKeyShuffleMm": "anywhere",
               "smallKeyShuffleHideout": "anywhere", "smallKeyShuffleChestGame": "anywhere"}


class TestKeyRingsVanillaSpecial(KeyRingTests):
    options = {**TestKeyRingsOwnDungeon.options, "smallKeyShuffleHideout": "vanilla", "smallKeyShuffleChestGame": "vanilla"}


class TestKeyRingsRemoved(KeyRingTests):
    options = {**TestKeyRingsOwnDungeon.options, "smallKeyShuffleOot": "removed", "smallKeyShuffleMm": "removed"}


class SoulTests(OOTxMMTestBase):
    def test_soul_requirements(self) -> None:
        from collections import Counter
        from .. import items, logic, time_logic
        conditions = [cond for parents in (*self.world.logic.checks.values(), *self.world.logic.events.values())
                      for _, _, cond in parents]
        conditions += [cond for exits in self.world.logic.exits.values() for _, cond in exits]
        counts = Counter({item.display_name: 999 for item in items.ITEM_BY_NAME.values()})
        counts.update({event: 999 for event in self.world.logic.events})
        data = (time_logic.OOT_ALL, time_logic.MM_ALL, 0, 0)
        replacements = {d[game]: d["shared"] for key, defs in logic.SHARED_SOUL_SETTINGS.items()
                        if self.world.ootmm_settings[key] for d in defs for game in ("oot", "mm")}
        for key, group in logic.SOUL_SETTINGS.items():
            group = [replacements.get(item, item) for item in group]
            without = counts.copy()
            for symbolic in group:
                without[items.ITEM_BY_SYMBOLIC_ID[symbolic].display_name] = 0
            gated = [cond for cond in conditions if time_logic.evaluate(cond, data, counts) is not None
                     and time_logic.evaluate(cond, data, without) is None]
            self.assertEqual(bool(gated), bool(self.world.ootmm_settings[key]))
            if key.startswith("soulsBoss") and self.world.ootmm_settings[key]:
                for symbolic in group:
                    without_one = counts.copy()
                    without_one[items.ITEM_BY_SYMBOLIC_ID[symbolic].display_name] = 0
                    self.assertTrue(any(time_logic.evaluate(cond, data, counts) is not None
                                        and time_logic.evaluate(cond, data, without_one) is None
                                        for cond in conditions), symbolic)

    def test_souls_pool_and_logic(self) -> None:
        from collections import Counter
        from .. import items, logic
        pool = Counter(items.ITEM_BY_NAME[item.name].symbolic_id
                       for item in self.multiworld.itempool if item.player == self.player)
        replacements = {d[game]: d["shared"] for key, defs in logic.SHARED_SOUL_SETTINGS.items()
                        if self.world.ootmm_settings[key] for d in defs for game in ("oot", "mm")}
        for key, group in logic.SOUL_SETTINGS.items():
            group = [replacements.get(item, item) for item in group]
            enabled = bool(self.world.ootmm_settings[key])
            self.assertEqual(self.world.fill_slot_data()["settings"][key], enabled)
            self.assertTrue(group)
            for symbolic in group:
                self.assertEqual(pool[symbolic], int(symbolic in logic.extra_items(self.world.ootmm_settings)))
            required = set(group) & self.world.logic.items
            self.assertEqual(bool(required), enabled)
            for symbolic in required:
                self.assertTrue(self.world.create_item(items.ITEM_BY_SYMBOLIC_ID[symbolic].display_name).advancement)
            alternate = {**self.world.ootmm_settings, key: not enabled}
            other = logic.build(alternate)
            self.assertIsNot(other, self.world.logic)
            if not any(item in replacements.values() for item in group):
                self.assertEqual(bool(set(group) & other.items), not enabled)
        self.assertIs(logic.build(self.world.ootmm_settings), self.world.logic)


class TestEnemySoulsOot(SoulTests):
    options = {"soulsEnemyOot": True}


class TestEnemySoulsMm(SoulTests):
    options = {"soulsEnemyMm": True}


class TestEnemySoulsBoth(SoulTests):
    options = {"soulsEnemyOot": True, "soulsEnemyMm": True, "shufflePotsOot": "all", "shufflePotsMm": "all"}


class TestBossSoulsOot(SoulTests):
    options = {"soulsBossOot": True}


class TestBossSoulsMm(SoulTests):
    options = {"soulsBossMm": True}


class TestBossSoulsBoth(SoulTests):
    options = {"soulsBossOot": True, "soulsBossMm": True}


class TestEnemyAndBossSouls(SoulTests):
    options = {**TestEnemySoulsBoth.options, **TestBossSoulsBoth.options}


class TestNpcSoulsOot(SoulTests):
    options = {"soulsNpcOot": True, "shufflePotsOot": "all"}


class TestNpcSoulsMm(SoulTests):
    options = {"soulsNpcMm": True, "shufflePotsMm": "all"}


class TestNpcSoulsBoth(SoulTests):
    options = {"soulsNpcOot": True, "soulsNpcMm": True,
               "shufflePotsOot": "all", "shufflePotsMm": "all"}


class TestEnemyBossAndNpcSouls(SoulTests):
    options = {**TestEnemyAndBossSouls.options, **TestNpcSoulsBoth.options}


class TestAnimalSoulsOot(SoulTests):
    options = {"soulsAnimalOot": True}


class TestAnimalSoulsMm(SoulTests):
    options = {"soulsAnimalMm": True}


class TestMiscSoulsOot(SoulTests):
    options = {"soulsMiscOot": True}


class TestMiscSoulsMm(SoulTests):
    options = {"soulsMiscMm": True}


class TestAnimalAndMiscSouls(SoulTests):
    options = {"soulsAnimalOot": True, "soulsAnimalMm": True,
               "soulsMiscOot": True, "soulsMiscMm": True}


class TestAllSouls(SoulTests):
    options = {**TestEnemyBossAndNpcSouls.options, **TestAnimalAndMiscSouls.options}


class TestSharedSouls(SoulTests):
    options = {**TestAllSouls.options, "sharedSoulsEnemy": True, "sharedSoulsNpc": True,
               "sharedSoulsAnimal": True, "sharedSoulsMisc": True}

    def test_shared_soul_merging(self) -> None:
        from collections import Counter
        from .. import items, logic
        pool = Counter(items.ITEM_BY_NAME[item.name].symbolic_id
                       for item in self.multiworld.itempool if item.player == self.player)
        for key, definitions in logic.SHARED_SOUL_SETTINGS.items():
            self.assertTrue(self.world.fill_slot_data()["settings"][key])
            separate = logic.build({**self.world.ootmm_settings, key: False})
            self.assertIsNot(separate, self.world.logic)
            for definition in definitions:
                shared, oot, mm = (definition[name] for name in ("shared", "oot", "mm"))
                self.assertEqual(pool[shared], 1)
                self.assertEqual(pool[oot] + pool[mm], 0)
                self.assertNotIn(oot, self.world.logic.items)
                self.assertNotIn(mm, self.world.logic.items)
                self.assertNotIn(shared, separate.items)
                self.assertEqual(shared in self.world.logic.items, bool({oot, mm} & separate.items), shared)
            self.assertTrue({d["shared"] for d in definitions} & self.world.logic.items)

    def test_shared_soul_pool_combinations(self) -> None:
        from .. import logic
        for key, definitions in logic.SHARED_SOUL_SETTINGS.items():
            family = key.removeprefix("sharedSouls")
            for oot_enabled, mm_enabled in ((False, False), (True, False), (False, True), (True, True)):
                settings = {key: True, f"souls{family}Oot": oot_enabled, f"souls{family}Mm": mm_enabled}
                additions = logic.extra_items(settings)
                for definition in definitions:
                    shared = oot_enabled and mm_enabled
                    self.assertEqual(additions.count(definition["shared"]), int(shared))
                    self.assertEqual(additions.count(definition["oot"]), int(oot_enabled and not shared))
                    self.assertEqual(additions.count(definition["mm"]), int(mm_enabled and not shared))


class TestSharedSoulsDisabled(SoulTests):
    options = {"sharedSoulsEnemy": True, "sharedSoulsNpc": True,
               "sharedSoulsAnimal": True, "sharedSoulsMisc": True}


class TestSharedSkeletonKey(OOTxMMTestBase):
    options = {"skeletonKeyOot": True, "skeletonKeyMm": True, "sharedSkeletonKey": True}

    def test_shared_key_pool_and_doors(self) -> None:
        from collections import Counter
        from .. import items, logic, time_logic
        pool = Counter(items.ITEM_BY_NAME[item.name].symbolic_id for item in self.multiworld.itempool)
        self.assertEqual(pool["SHARED_SKELETON_KEY"], 1)
        for prefix in ("OOT", "MM"):
            self.assertEqual(pool[f"{prefix}_SKELETON_KEY"], 0)
            self.assertNotIn(f"{prefix}_SKELETON_KEY", self.world.logic.items)
        shared = items.ITEM_BY_SYMBOLIC_ID["SHARED_SKELETON_KEY"].display_name
        self.assertTrue(self.world.create_item(shared).advancement)
        for prefix, source, target in (("OOT", "Forest Temple Main", "Forest Temple Maze"),
                                       ("MM", "Woodfall Temple Main Entrance Ledge", "Woodfall Temple Maze")):
            conditions = [cond for (parent, _), exits in self.world.logic.exits.items()
                          if parent == f"{prefix} {source}"
                          for area, cond in exits if area == f"{prefix} {target}"]
            self.assertTrue(conditions)
            for cond in conditions:
                data = (time_logic.OOT_ALL, time_logic.MM_ALL, 0, 0)
                self.assertIsNone(time_logic.evaluate(cond, data, Counter()))
                self.assertIsNotNone(time_logic.evaluate(cond, data, Counter({shared: 1})))
        self.assertTrue(self.world.fill_slot_data()["settings"]["sharedSkeletonKey"])
        separate = logic.build({**self.world.ootmm_settings, "sharedSkeletonKey": False})
        self.assertIsNot(separate, self.world.logic)
        self.assertNotIn("SHARED_SKELETON_KEY", separate.items)
        self.assertIn("OOT_SKELETON_KEY", separate.items)
        self.assertIn("MM_SKELETON_KEY", separate.items)

    def test_sharing_requires_both_keys(self) -> None:
        from .. import logic
        for oot in (False, True):
            for mm in (False, True):
                settings = {**self.world.ootmm_settings, "skeletonKeyOot": oot, "skeletonKeyMm": mm}
                normalized = logic.normalize_shared_items(settings)
                self.assertEqual(normalized["sharedSkeletonKey"], oot and mm)
                additions = logic.extra_items(settings)
                self.assertEqual("SHARED_SKELETON_KEY" in additions, oot and mm)
                self.assertEqual("OOT_SKELETON_KEY" in additions, oot and not mm)
                self.assertEqual("MM_SKELETON_KEY" in additions, mm and not oot)


class TestSharedSkeletonKeyDisabled(SkeletonKeyTests):
    options = {"skeletonKeyOot": True, "sharedSkeletonKey": True}

    def test_patch_disables_sharing(self) -> None:
        self.assertFalse(self.world.fill_slot_data()["settings"]["sharedSkeletonKey"])


class OcarinaButtonTests(OOTxMMTestBase):
    __test__ = False

    def test_button_pool_and_logic(self) -> None:
        from collections import Counter
        from .. import items, logic
        settings = self.world.fill_slot_data()["settings"]
        shared = settings["sharedOcarinaButtons"]
        pool = Counter(items.ITEM_BY_NAME[item.name].symbolic_id for item in self.multiworld.itempool)
        for definition in logic.SHARED_ITEM_SETTINGS["sharedOcarinaButtons"]:
            for game, suffix in (("oot", "Oot"), ("mm", "Mm")):
                enabled = settings[f"ocarinaButtonsShuffle{suffix}"]
                self.assertEqual(pool[definition[game]], int(enabled and not shared))
                self.assertEqual(definition[game] in self.world.logic.items, enabled and not shared)
            self.assertEqual(pool[definition["shared"]], int(shared))
            self.assertEqual(definition["shared"] in self.world.logic.items, shared)
            for symbolic in (definition["oot"], definition["mm"], definition["shared"]):
                if pool[symbolic]:
                    self.assertTrue(self.world.create_item(items.ITEM_BY_SYMBOLIC_ID[symbolic].display_name).advancement)

    def test_song_requires_its_buttons(self) -> None:
        from collections import Counter
        from .. import items, time_logic
        inventory = Counter({items.ITEM_BY_SYMBOLIC_ID[symbolic].display_name: 99
                             for symbolic in self.world.logic.items})
        data = (time_logic.OOT_ALL, time_logic.MM_ALL, 0, 0)
        conditions = [cond for _, _, cond in self.world.logic.checks["OOT Zora River Frogs Zeldas Lullaby"]]
        self.assertTrue(any(time_logic.evaluate(cond, data, inventory) is not None for cond in conditions))
        prefix = "SHARED" if self.world.ootmm_settings["sharedOcarinaButtons"] else "OOT"
        for button in ("C_UP", "C_RIGHT", "C_LEFT"):
            missing = inventory.copy()
            missing.pop(items.ITEM_BY_SYMBOLIC_ID[f"{prefix}_BUTTON_{button}"].display_name, None)
            self.assertEqual(any(time_logic.evaluate(cond, data, missing) is not None for cond in conditions),
                             not self.world.ootmm_settings["ocarinaButtonsShuffleOot"])

    def test_sharing_normalization(self) -> None:
        from .. import logic
        for oot in (False, True):
            for mm in (False, True):
                settings = {**self.world.ootmm_settings, "ocarinaButtonsShuffleOot": oot,
                            "ocarinaButtonsShuffleMm": mm, "sharedOcarinaButtons": True}
                self.assertEqual(logic.normalize_shared_items(settings)["sharedOcarinaButtons"], oot and mm)
                additions = logic.extra_items(settings)
                for definition in logic.SHARED_ITEM_SETTINGS["sharedOcarinaButtons"]:
                    self.assertEqual(definition["shared"] in additions, oot and mm)
                    self.assertEqual(definition["oot"] in additions, oot and not mm)
                    self.assertEqual(definition["mm"] in additions, mm and not oot)


class TestOcarinaButtonsOot(OcarinaButtonTests):
    __test__ = True
    options = {"ocarinaButtonsShuffleOot": True, "sharedOcarinaButtons": True}


class TestOcarinaButtonsMm(OcarinaButtonTests):
    __test__ = True
    options = {"ocarinaButtonsShuffleMm": True}


class TestOcarinaButtonsSeparate(OcarinaButtonTests):
    __test__ = True
    options = {"ocarinaButtonsShuffleOot": True, "ocarinaButtonsShuffleMm": True}


class TestOcarinaButtonsShared(OcarinaButtonTests):
    __test__ = True
    options = {"ocarinaButtonsShuffleOot": True, "ocarinaButtonsShuffleMm": True,
               "sharedOcarinaButtons": True}


SHARED_EQUIPMENT = (
    ("sharedBows", "BOW", 3, 3, 3),
    ("sharedBombBags", "BOMB_BAG", 3, 3, 3),
    ("sharedMagic", "MAGIC_UPGRADE", 2, 2, 2),
    ("sharedMagicArrowFire", "ARROW_FIRE", 1, 1, 1),
    ("sharedMagicArrowIce", "ARROW_ICE", 1, 1, 1),
    ("sharedMagicArrowLight", "ARROW_LIGHT", 1, 1, 1),
    ("sharedHookshot", "HOOKSHOT", 2, 2, 1),
    ("sharedLens", "LENS", 1, 1, 1),
    ("sharedSongEpona", "SONG_EPONA", 1, 1, 1),
    ("sharedSongStorms", "SONG_STORMS", 1, 1, 1),
    ("sharedSongTime", "SONG_TIME", 1, 1, 1),
    ("sharedMaskGoron", "MASK_GORON", 1, 1, 1),
    ("sharedMaskZora", "MASK_ZORA", 1, 1, 1),
    ("sharedMaskTruth", "MASK_TRUTH", 1, 1, 1),
    ("sharedMaskBunny", "MASK_BUNNY", 1, 1, 1),
    ("sharedMaskKeaton", "MASK_KEATON", 1, 1, 1),
    ("sharedWallets", "WALLET", 2, 2, 2),
)


class SharedEquipmentTests(OOTxMMTestBase):
    __test__ = False

    def test_pool_counts_and_patch_settings(self) -> None:
        from collections import Counter
        from .. import items, logic
        settings = self.world.fill_slot_data()["settings"]
        pool = Counter(items.ITEM_BY_NAME[item.name].symbolic_id
                       for item in self.multiworld.get_items() if item.player == self.player and item.code)
        for key, suffix, count, oot_count, mm_count in SHARED_EQUIPMENT:
            shared = settings[key]
            self.assertEqual(pool[f"SHARED_{suffix}"], count if shared else 0)
            for game, separate_count in (("OOT", oot_count), ("MM", mm_count)):
                self.assertEqual(pool[f"{game}_{suffix}"], 0 if shared else separate_count)
                if shared:
                    self.assertNotIn(f"{game}_{suffix}", self.world.logic.items)
            if shared:
                self.assertIn(f"SHARED_{suffix}", self.world.logic.items)
                self.assertTrue(self.world.create_item(items.ITEM_BY_SYMBOLIC_ID[f"SHARED_{suffix}"].display_name).advancement)
            self.assertEqual(shared, bool(self.options.get(key, False)))

    def test_both_games_require_shared_equipment(self) -> None:
        from collections import Counter
        from .. import items, time_logic
        inventory = Counter({items.ITEM_BY_SYMBOLIC_ID[symbol].display_name: 99
                             for symbol in self.world.logic.items})
        # Isolate mask requirements from the dog-race funding and guard-gate prerequisites.
        inventory.update({"OOT_RUPEES": 1, "MM_RUPEES": 1, "OOT_KAKARIKO_GATE_OPEN": 1})
        data = (time_logic.OOT_ALL, time_logic.MM_ALL, 0, 0)
        for key, suffix, *_ in SHARED_EQUIPMENT:
            if not self.options.get(key):
                continue
            shared = items.ITEM_BY_SYMBOLIC_ID[f"SHARED_{suffix}"].display_name
            usable = inventory.copy()
            if suffix == "BOMB_BAG":
                # Blast Mask and bombchus are valid alternatives to bombs in MM's conditions.
                for symbol in self.world.logic.items:
                    if "BOMBCHU" in symbol or symbol.endswith("MASK_BLAST"):
                        usable.pop(items.ITEM_BY_SYMBOLIC_ID[symbol].display_name, None)
            if suffix == "ARROW_FIRE":
                # Din's Fire can light the same OoT torches as Fire Arrows.
                for symbol in self.world.logic.items:
                    if symbol.endswith("SPELL_FIRE"):
                        usable.pop(items.ITEM_BY_SYMBOLIC_ID[symbol].display_name, None)
            missing = usable.copy()
            missing.pop(shared)
            for game in ("OOT", "MM"):
                if game == "OOT" and suffix == "ARROW_ICE":
                    # Ice Arrows are optional in OoT's default rules.
                    continue
                if game == "OOT" and suffix in ("MASK_GORON", "MASK_ZORA"):
                    # These are cosmetic masks in OoT; their transformation gates are in MM.
                    continue
                conditions = [cond for parents in (*self.world.logic.checks.values(), *self.world.logic.events.values())
                              for area, _, cond in parents if area.startswith(game + " ")]
                conditions += [cond for (area, _), exits in self.world.logic.exits.items()
                               if area.startswith(game + " ") for _, cond in exits]
                affected = [cond for cond in conditions
                            if time_logic.evaluate(cond, data, usable) is not None
                            and time_logic.evaluate(cond, data, missing) is None]
                self.assertTrue(affected, (game, suffix))

    def test_filler_uses_shared_ammunition(self) -> None:
        from .. import items, logic
        items.get_random_filler_item(self.world)
        for name in self.world.filler_item_names:
            symbol = items.ITEM_BY_NAME[name].symbolic_id
            self.assertEqual(logic.shared_item(symbol, self.world.ootmm_settings), symbol)
        for location in self.multiworld.get_locations(self.player):
            if location.item and location.item.code:
                symbol = items.ITEM_BY_NAME[location.item.name].symbolic_id
                self.assertEqual(logic.shared_item(symbol, self.world.ootmm_settings), symbol)

    def test_shared_song_placement(self) -> None:
        from .. import items, prefill
        for key, suffix, *_ in SHARED_EQUIPMENT:
            if not suffix.startswith("SONG_") or not self.options.get(key):
                continue
            name = items.ITEM_BY_SYMBOLIC_ID[f"SHARED_{suffix}"].display_name
            locations = self.multiworld.find_item_locations(name, self.player)
            if self.options.get("songs", "songLocations") == "songLocations":
                self.assertEqual(len(locations), 1)
                self.assertIn(locations[0].name, prefill.SONG_LOCATIONS)
                self.assertEqual(locations[0].player, self.player)
            else:
                self.assertEqual(sum(item.name == name and item.player == self.player
                                     for item in self.multiworld.itempool), 1)
                self.assertFalse(locations)


class TestSharedBows(SharedEquipmentTests):
    __test__ = True
    options = {"sharedBows": True}


class TestSharedBombBags(SharedEquipmentTests):
    __test__ = True
    options = {"sharedBombBags": True}


class TestSharedMagic(SharedEquipmentTests):
    __test__ = True
    options = {"sharedMagic": True}


class TestSharedWallets(SharedEquipmentTests):
    __test__ = True
    options = {"sharedWallets": True}


class TestSharedEquipment(SharedEquipmentTests):
    __test__ = True
    options = {**{key: True for key, *_ in SHARED_EQUIPMENT}, "shuffleMaskTrades": True}


class TestSharedArrows(SharedEquipmentTests):
    __test__ = True
    options = {"sharedMagicArrowFire": True, "sharedMagicArrowIce": True, "sharedMagicArrowLight": True}


class TestSharedTools(SharedEquipmentTests):
    __test__ = True
    options = {"sharedHookshot": True, "sharedLens": True}


class TestSharedMasks(SharedEquipmentTests):
    __test__ = True
    options = {**{key: True for key, suffix, *_ in SHARED_EQUIPMENT if suffix.startswith("MASK_")},
               "shuffleMaskTrades": True}


class TestSharedSongs(SharedEquipmentTests):
    __test__ = True
    options = {"sharedSongEpona": True, "sharedSongStorms": True, "sharedSongTime": True}


class TestSharedSongsAnywhere(TestSharedSongs):
    options = {**TestSharedSongs.options, "songs": "anywhere"}


class TestCrossGameEquipment(OOTxMMTestBase):
    options = {
        "hammerMm": True, "sharedHammer": True, "boomerangMm": True,
        "bootsIronMm": True, "sharedBootsIron": True, "tunicGoronMm": True,
        "tunicZoraMm": True, "sharedTunicZora": True,
        "spellWindMm": True, "sharedSpellWind": True, "sharedSpellLove": True,
        "shuffleRocksMm": "all",
    }

    def test_equipment_in_generated_pool(self) -> None:
        from collections import Counter
        from ..items import ITEM_BY_NAME

        pool = Counter(ITEM_BY_NAME[item.name].symbolic_id
                       for item in self.multiworld.get_items() if item.player == self.player and item.code)
        for symbol in ("SHARED_HAMMER", "OOT_BOOMERANG", "MM_BOOMERANG",
                       "SHARED_BOOTS_IRON", "MM_TUNIC_GORON",
                       "SHARED_SPELL_WIND", "OOT_SPELL_LOVE"):
            self.assertEqual(pool[symbol], 1)
        self.assertEqual(pool["OOT_TUNIC_GORON"], 2)
        self.assertEqual(pool["SHARED_TUNIC_ZORA"], 2)
        for symbol in ("OOT_HAMMER", "MM_HAMMER", "SHARED_BOOMERANG",
                       "OOT_BOOTS_IRON", "MM_BOOTS_IRON", "SHARED_TUNIC_GORON",
                       "OOT_TUNIC_ZORA", "MM_TUNIC_ZORA",
                       "OOT_SPELL_WIND", "MM_SPELL_WIND", "SHARED_SPELL_LOVE", "MM_SPELL_LOVE"):
            self.assertEqual(pool[symbol], 0)
        settings = self.world.fill_slot_data()["settings"]
        for key, value in {**self.options, "sharedSpellLove": False}.items():
            self.assertEqual(settings[key], value)


class TestSharedEquipmentReference(unittest.TestCase):
    def test_same_pool_as_ootmm(self) -> None:
        import json
        import pkgutil
        from collections import Counter
        from .. import logic
        samples = json.loads(pkgutil.get_data(__name__, "shared_equipment_samples.json"))
        base = Counter(samples[0]["pool"])
        # Reconstruct the two vanilla Lullaby sources before the default progressive transform.
        for game in ("OOT", "MM", "SHARED"):
            for suffix in ("GORON", "GORON_HALF"):
                base.pop(game + "_SONG_" + suffix, None)
        base.update(item for item in logic.ootxmm_staticdata.OOTxMMCheckItems.values()
                    if item in ("MM_SONG_GORON", "MM_SONG_GORON_HALF"))
        additions = {item for _, item in logic.CROSS_GAME_ITEMS.values()}
        additions.update(item for key in ("sharedShovel", "sharedPlatinumToken")
                         for definition in logic.SHARED_ITEM_SETTINGS[key] for item in definition.values())
        additions.update(("OOT_SONG_GORON", "OOT_SONG_GORON_HALF", "MM_OCARINA"))
        vanilla = logic.ootxmm_staticdata.OOTxMMCheckItems
        equipment = logic.EQUIPMENT_ITEMS
        consumables = {"OOT_RECOVERY_HEART", "MM_RECOVERY_HEART", "OOT_FAIRY_BIG", "MM_FAIRY_BIG"}
        for sample in samples:
            with self.subTest(settings=sample["settings"]):
                settings = logic.normalize_shared_items(sample["settings"])
                pool = base.copy()
                if "healthChecks" in sample:
                    for item in consumables:
                        pool.pop(item, None)
                    pool.update(vanilla[name] for name in sample["healthChecks"])
                pool.update(item for item in logic.extra_items(settings) if item in additions)
                if "equipmentChecks" in sample:
                    for item in equipment:
                        pool.pop(item, None)
                    pool.update(vanilla[name] for name in sample["equipmentChecks"])
                    pool.update(item for item in logic.extra_items(settings) if item in equipment)
                    self.assertEqual({name: logic.shared_item(vanilla[name], settings)
                                      for name in sample["fixedEquipment"]}, sample["fixedEquipment"])
                transformed = logic.transform_pool(pool.elements(), settings)
                transformed.subtract(logic.shared_item(vanilla[name], settings)
                                     for name in sample.get("fixedOcarinas", ()))
                expected = Counter(sample["pool"])
                if "equipmentChecks" in sample and sample["settings"].get("shopShuffleOot") == "full":
                    # Shuffled shops also add unrelated vanilla stock to the reference pool.
                    transformed = Counter({item: transformed[item] for item in equipment if transformed[item]})
                    expected = Counter({item: expected[item] for item in equipment if expected[item]})
                self.assertEqual(+transformed, expected)
                from .. import prefill
                self.assertEqual(prefill.song_locations(settings), set(sample["songLocations"]))


class TestSharedOcarinaAndHealth(OOTxMMTestBase):
    options = {"sharedOcarina": True, "sharedHealth": True, "sharedMagic": True,
               "fairyOcarinaMm": True, "shuffleFreeHeartsMm": True, "shuffleGossipBigFairiesMm": "all"}

    def test_shared_items_in_pool_and_patch_settings(self) -> None:
        from collections import Counter
        from .. import items
        pool = Counter(items.ITEM_BY_NAME[item.name].symbolic_id
                       for item in self.multiworld.get_items() if item.player == self.player and item.code)
        for suffix, count in (("OCARINA", 2), ("HEART_CONTAINER", 6), ("HEART_PIECE", 44), ("DEFENSE_UPGRADE", 1)):
            self.assertEqual(pool["SHARED_" + suffix], count)
            self.assertEqual(pool["OOT_" + suffix] + pool["MM_" + suffix], 0)
        for suffix in ("RECOVERY_HEART", "FAIRY_BIG"):
            self.assertGreater(pool["SHARED_" + suffix], 0)
            self.assertEqual(pool["OOT_" + suffix] + pool["MM_" + suffix], 0)
        settings = self.world.fill_slot_data()["settings"]
        for key, value in self.options.items():
            self.assertEqual(settings[key], value)
        self.assertIn("SHARED_OCARINA", self.world.logic.items)
        self.assertTrue({"OOT_OCARINA", "MM_OCARINA"}.isdisjoint(self.world.logic.items))


class TestSharedFixedOcarinas(OOTxMMTestBase):
    options = {"sharedOcarina": True, "shuffleOcarinasOot": False}

    def test_only_fixed_shared_ocarinas(self) -> None:
        from .. import items, prefill
        name = items.ITEM_BY_SYMBOLIC_ID["SHARED_OCARINA"].display_name
        sources = prefill.FIXED_SETTINGS["shuffleOcarinasOot"]
        self.assertEqual(len(sources), 2)
        for source in sources:
            location = self.multiworld.get_location(source, self.player)
            self.assertTrue(location.locked)
            self.assertEqual(location.item.name, name)
        self.assertFalse(any(item.name == name for item in self.multiworld.itempool))


class TestSharedSwordsShieldsAndNutsSticks(OOTxMMTestBase):
    options = {
        "extraChildSwordsOot": True, "sharedSwords": True,
        "progressiveShieldsOot": "progressive", "progressiveShieldsMm": "progressive", "sharedShields": True,
        "sticksNutsUpgradesMm": True, "sticksNutsUpgradesInitial": True, "sharedNutsSticks": True,
    }

    def test_shared_progression_and_fixed_stock(self) -> None:
        from collections import Counter
        from .. import items
        pool = Counter(items.ITEM_BY_NAME[item.name].symbolic_id for item in self.multiworld.itempool
                       if item.player == self.player)
        for suffix in ("SWORD", "SHIELD", "STICK_UPGRADE", "NUT_UPGRADE"):
            self.assertEqual(pool["SHARED_" + suffix], 3)
            self.assertEqual(pool["OOT_" + suffix] + pool["MM_" + suffix], 0)
            self.assertIn("SHARED_" + suffix, self.world.logic.items)
        for check, symbol in (
            ("MM Trading Post Item 3", "SHARED_SHIELD_HYLIAN"),
            ("MM Trading Post Item 5", "SHARED_STICK"),
            ("OOT Kokiri Shop Item 5", "SHARED_NUTS_5"),
        ):
            location = self.multiworld.get_location(check, self.player)
            self.assertTrue(location.locked)
            self.assertEqual(items.ITEM_BY_NAME[location.item.name].symbolic_id, symbol)
        settings = self.world.fill_slot_data()["settings"]
        for key, value in self.options.items():
            self.assertEqual(settings[key], value)


class TestSharedSeparateShields(OOTxMMTestBase):
    options = {"sharedShields": True, "dekuShieldMm": True,
               "shopShuffleOot": "full", "shopShuffleMm": "full"}

    def test_shield_additions_fit_pool(self) -> None:
        from collections import Counter
        from .. import items
        pool = self.multiworld.itempool
        self.assertEqual(sum(item.player == self.player for item in pool) + len(self.world.get_pre_fill_items()),
                         len(self.multiworld.get_unfilled_locations(self.player)))
        counts = Counter(items.ITEM_BY_NAME[item.name].symbolic_id for item in pool if item.player == self.player)
        for suffix, count in (("SHIELD_DEKU", 8), ("SHIELD_HYLIAN", 6), ("SHIELD_MIRROR", 1)):
            self.assertEqual(counts["SHARED_" + suffix], count)
