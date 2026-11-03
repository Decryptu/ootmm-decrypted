from .. import items, ootxmm_staticdata, prefill
from .test_options import OOTxMMTestBase


def symbolic(item) -> str:
    return items.ITEM_BY_NAME[item.name].symbolic_id


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
