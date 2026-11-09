import json
import os
import pkgutil
import random
import tempfile
from collections import Counter
from unittest import TestCase
from unittest.mock import patch

from .. import logic, ootxmm_staticdata, prefill, prices
from ..time_logic import TimeLogic, evaluate
from ..items import ITEM_BY_SYMBOLIC_ID
from .test_options import OOTxMMTestBase


class TestPriceTables(TestCase):
    def test_shop_reachability_matches_upstream(self):
        samples = json.loads(pkgutil.get_data(__name__, "time_samples.json").decode())
        for sample in samples:
            if "priceOotShops" not in sample["settings"]:
                continue
            graph = logic.build({**ootxmm_staticdata.OOTxMMSettingDefaults, **sample["settings"]})
            counts = Counter({ITEM_BY_SYMBOLIC_ID[s].display_name: n for s, n in sample["counts"].items()})
            counts.update(sample["events"])
            reached = TimeLogic(graph, 1).explore(counts)
            expected = set(sample["locations"])
            for name, parents in graph.checks.items():
                if logic._check_info["checks"][name][0] != "shop":
                    continue
                actual = any((data := reached.get((area, age))) is not None
                             and evaluate(cond, data, counts) is not None for area, age, cond in parents)
                with self.subTest(settings=sample["settings"], removed=sample["removed"], shop=name):
                    self.assertEqual(actual, name in expected)

    def test_modes_preserve_other_ranges(self):
        data = ootxmm_staticdata.OOTxMMLogic
        defaults = ootxmm_staticdata.OOTxMMSettingDefaults
        self.assertEqual(prices.generate(defaults, random.Random(1)), data["prices"])
        for mode in ("affordable", "random", "weighted"):
            settings = {**defaults, "priceOotShops": mode, "priceMmShops": mode}
            table = prices.generate(settings, random.Random(123))
            self.assertEqual(table, prices.generate(settings, random.Random(123)))
            slots = {i for group in ("OOT_SHOPS", "MM_SHOPS", "MM_SHOPS_EX")
                     for i in range(data["priceRanges"][group], data["priceRanges"][group] + data["priceCounts"][group])}
            for i, value in enumerate(table):
                if i not in slots:
                    self.assertEqual(value, data["prices"][i])
                elif mode == "affordable":
                    self.assertEqual(value, 10)
                else:
                    self.assertEqual(value % 5, 0)
                    self.assertTrue(0 <= value <= 500)

    def test_price_threshold_and_graph_cache(self):
        defaults = ootxmm_staticdata.OOTxMMSettingDefaults
        node = next(n for n in ootxmm_staticdata.OOTxMMLogic["nodes"] if isinstance(n, list) and n[0] == "price")
        table = list(ootxmm_staticdata.OOTxMMLogic["prices"])
        table[node[1]] = node[2]
        settings = {**defaults, "_prices": table}
        self.assertTrue(logic._Specializer(settings, set(), None).build(node, "child"))
        graph = logic.build(settings)
        table = table.copy()
        table[node[1]] += 1
        settings = {**defaults, "_prices": table}
        self.assertFalse(logic._Specializer(settings, set(), None).build(node, "adult"))
        self.assertIsNot(graph, logic.build(settings))

    def test_wallet_limits_and_weighted_draws(self):
        class HighestDraw:
            def randrange(self, stop):
                return stop - 1

        for colossal, bottomless, maximum in ((False, False, 500), (True, False, 995), (True, True, 4995)):
            for mode in ("random", "weighted"):
                settings = {"priceOotShops": mode, "colossalWallets": colossal, "bottomlessWallets": bottomless}
                self.assertEqual(prices.generate(settings, HighestDraw())[0], maximum)

        class Draws:
            values = iter([90, 10, 70, 30, 50, 20])

            def randrange(self, stop):
                return next(self.values, 0)

        self.assertEqual(prices.generate({"priceOotShops": "weighted"}, Draws())[0], 100)


class TestShuffledShops(OOTxMMTestBase):
    options = {"shopShuffleOot": "full", "shopShuffleMm": "full",
               "priceOotShops": "uniform", "priceMmShops": "weighted"}

    def test_shops_are_unlocked(self):
        fixed = prefill.fixed_checks(self.world)
        for names in prefill.SHOP_SETTINGS.values():
            self.assertTrue(names)
            self.assertFalse(names & fixed)
        self.assertEqual(self.world.ootmm_settings["priceOotShops"], "random")

    def test_output_carries_exact_prices(self):
        with tempfile.TemporaryDirectory() as directory:
            with patch(f"{self.world.__module__}.display_item", return_value=["OOT_RUPEE_GREEN", True]):
                self.world.generate_output(directory)
            with open(os.path.join(directory, os.listdir(directory)[0])) as file:
                output = json.load(file)
        self.assertEqual(output["prices"], self.world.prices)
        self.assertIs(self.world.logic, logic.build({**self.world.ootmm_settings, "_prices": self.world.prices}))


class TestAffordableShops(TestShuffledShops):
    options = {"shopShuffleOot": "full", "shopShuffleMm": "full",
               "priceOotShops": "affordable", "priceMmShops": "affordable"}

    def test_shops_are_unlocked(self):
        self.assertFalse(set().union(*prefill.SHOP_SETTINGS.values()) & prefill.fixed_checks(self.world))
