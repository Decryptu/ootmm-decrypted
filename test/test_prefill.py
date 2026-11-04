from types import SimpleNamespace
from unittest import TestCase
from unittest.mock import patch

from Fill import FillError

from .. import items, ootxmm_staticdata, prefill
from .test_options import OOTxMMTestBase


def symbolic(item) -> str:
    return items.ITEM_BY_NAME[item.name].symbolic_id


class TestPreFillRetry(TestCase):
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
            if location.name in prefill.FIXED:
                self.assertEqual(symbolic(location.item), ootxmm_staticdata.OOTxMMCheckItems[location.name], location.name)

    def test_items_stay_where_ootmm_puts_them(self) -> None:
        for location in self.multiworld.get_locations(self.player):
            if location.address is None or location.item is None or location.item.player != self.player or location.name in prefill.FIXED:
                continue
            for group_items, group_locations in prefill._groups(self.world):
                if symbolic(location.item) in group_items:
                    self.assertIn(location.name, group_locations, f"{location.item.name} at {location.name}")

    def test_no_item_left_unplaced(self) -> None:
        self.assertEqual(self.world.get_pre_fill_items(), [])
