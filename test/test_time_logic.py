from collections import Counter
import json
import pkgutil
from types import SimpleNamespace
from unittest import TestCase
from unittest.mock import patch

from .. import logic
from ..items import ITEM_BY_SYMBOLIC_ID
from ..time_logic import TimeLogic, evaluate, MM_ALL, OOT_ALL, MM_SLICES
from .test_options import OOTxMMTestBase


class TestTimeConditions(TestCase):
    def test_contradictory_times_are_false(self):
        data = (OOT_ALL, MM_ALL, 0, 0)
        for kind in ("time-oot", "time-mm"):
            self.assertIsNone(evaluate(("and", ((kind, 1), (kind, 2))), data, Counter()))

    def test_or_keeps_only_successful_routes(self):
        cond = ("or", (("and", (False, ("time-mm", 1))), ("time-mm", 4)))
        self.assertEqual(evaluate(cond, (OOT_ALL, MM_ALL, 0, 0), Counter())[1], 4)

    def test_incompatible_regional_flags(self):
        self.assertIsNone(evaluate(("flag-on", 0), (OOT_ALL, MM_ALL, 0, 1), Counter()))
        self.assertIsNone(evaluate(("and", (("flag-on", 0), ("flag-off", 0))),
                                   (OOT_ALL, MM_ALL, 0, 0), Counter()))

    def graph(self, areas, exits, stay=None):
        self.patch = patch.dict(logic._areas, areas)
        self.patch.start()
        self.addCleanup(self.patch.stop)
        graph = SimpleNamespace(exits=exits, stay={key: None for key in exits})
        graph.stay.update(stay or {})
        return TimeLogic(graph, 1)

    def test_late_entry_cannot_reach_early_check(self):
        areas = {"OOT SPAWN": {"game": "oot", "time": "flow"},
                 "MM Late": {"game": "mm"}, "MM Room": {"game": "mm"}}
        exits = {(logic.ORIGIN, age): [("MM Late", True)] for age in logic.AGES}
        for age in logic.AGES:
            exits[("MM Late", age)] = [("MM Room", ("time-mm", 1 << 32))]
            exits[("MM Room", age)] = []
        engine = self.graph(areas, exits)
        reached = engine.explore(Counter())
        data = reached[("MM Room", "child")]
        self.assertIsNone(evaluate(("time-mm", 1), data, Counter()))
        self.assertIsNotNone(evaluate(("time-mm", 1 << 45), data, Counter()))

    def test_conditional_wait_and_day_one_return(self):
        areas = {"OOT SPAWN": {"game": "oot", "time": "flow"},
                 "MM Wait": {"game": "mm"}, "OOT Return": {"game": "oot", "time": "still"},
                 "MM Reset": {"game": "mm"}}
        exits = {(logic.ORIGIN, age): [("MM Wait", True)] for age in logic.AGES}
        stay = {}
        for age in logic.AGES:
            exits[("MM Wait", age)] = [("OOT Return", ("time-mm", 4))]
            exits[("OOT Return", age)] = [("MM Reset", True)]
            exits[("MM Reset", age)] = []
            stay[("MM Wait", age)] = (True, ("event", "WAIT_ALLOWED"), True) + (False,) * (MM_SLICES - 3)
        engine = self.graph(areas, exits, stay)
        self.assertEqual(engine.explore(Counter())[("MM Wait", "child")][1], 1)
        reached = engine.explore(Counter(WAIT_ALLOWED=1))
        self.assertEqual(reached[("MM Wait", "child")][1], 7)
        self.assertTrue(reached[("MM Reset", "child")][1] & 1)

    def test_native_grants_survive_inventory_changes_without_duplication(self):
        areas = {"OOT SPAWN": {"game": "oot", "time": "flow"}}
        exits = {(logic.ORIGIN, age): [] for age in logic.AGES}
        base = self.graph(areas, exits)
        name = ITEM_BY_SYMBOLIC_ID["MM_STRAY_FAIRY_WF"].display_name
        engine = TimeLogic(base.graph, 1, {name: 3})
        class State:
            prog_items = {1: Counter()}
        state = State()
        enough = engine.rule(logic.ORIGIN, "child", ("item", "MM_STRAY_FAIRY_WF", 4))
        self.assertFalse(enough(state))
        state.prog_items[1][name] += 1
        self.assertTrue(enough(state))
        self.assertTrue(enough(state))
        state.prog_items[1][name] -= 1
        self.assertFalse(enough(state))
        self.assertEqual(engine.starting[name], 3)
        self.assertFalse(base.rule(logic.ORIGIN, "child", ("item", "MM_STRAY_FAIRY_WF", 1))(state))

    def test_player_inventories_are_isolated(self):
        areas = {"OOT SPAWN": {"game": "oot", "time": "flow"}}
        exits = {(logic.ORIGIN, age): [] for age in logic.AGES}
        first = self.graph(areas, exits)
        second = TimeLogic(first.graph, 2)
        class State:
            prog_items = {1: Counter(TEST_CLOCK_EVENT=1), 2: Counter()}
        state = State()
        condition = ("event", "TEST_CLOCK_EVENT")
        self.assertTrue(first.rule(logic.ORIGIN, "child", condition)(state))
        self.assertFalse(second.rule(logic.ORIGIN, "child", condition)(state))


class TestTimeState(OOTxMMTestBase):
    def test_empty_terminal_areas_are_pruned(self):
        self.assertNotIn(("MM Gorman Track Trees", "child"), self.world.logic.regions)
        self.assertNotIn(("MM Gorman Track Trees", "adult"), self.world.logic.regions)

    def test_cache_tracks_removal_and_copies(self):
        engine = self.world.time_logic
        rule = engine.rule(logic.ORIGIN, "child", ("item", "OOT_OCARINA", 1))
        item = self.world.create_item(ITEM_BY_SYMBOLIC_ID["OOT_OCARINA"].display_name)
        state = self.multiworld.state.copy()
        self.assertFalse(rule(state))
        state.collect(item, True)
        self.assertTrue(rule(state))
        copy = state.copy()
        state.remove(item)
        self.assertFalse(rule(state))
        self.assertTrue(rule(copy))


class TestOoTMMClocks(TestCase):
    def test_derives_events_without_archipelago_sweep(self):
        samples = json.loads(pkgutil.get_data(__name__, "time_samples.json").decode())
        graph = logic.build(logic.ootxmm_staticdata.OOTxMMSettingDefaults)
        counts = Counter({ITEM_BY_SYMBOLIC_ID[s].display_name: n for s, n in samples[0]["counts"].items()})
        engine = TimeLogic(graph, 1)
        reached, derived = engine.solve(counts)
        self.assertTrue(derived["OOT_GANON"])
        self.assertTrue(derived["MM_MAJORA"])
        empty = engine.solve(Counter())
        self.assertEqual(engine.solve(counts, (Counter(), empty)), (reached, derived))
        reduced = counts.copy()
        del reduced[ITEM_BY_SYMBOLIC_ID["MM_OCARINA"].display_name]
        self.assertEqual(engine.solve(reduced, (counts, (reached, derived))), engine.solve(reduced))

    def test_matches_upstream_area_clocks(self):
        samples = json.loads(pkgutil.get_data(__name__, "time_samples.json").decode())
        graph = logic.build(logic.ootxmm_staticdata.OOTxMMSettingDefaults)
        engine = TimeLogic(graph, 1)
        for sample in samples:
            counts = Counter({ITEM_BY_SYMBOLIC_ID[s].display_name: n for s, n in sample["counts"].items()})
            # Supply upstream's events to isolate clock propagation from other logic approximations.
            counts.update(sample["events"])
            reached = engine.explore(counts)
            for i, age in enumerate(logic.AGES):
                for area, expected in sample["areas"][i].items():
                    if (area, age) in graph.exits:
                        with self.subTest(removed=sample["removed"], area=area, age=age):
                            self.assertEqual(reached.get((area, age)), tuple(expected))
