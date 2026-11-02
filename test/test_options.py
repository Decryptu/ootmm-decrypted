from test.bases import WorldTestBase

from ..options import OOTxMM_tricks


class OOTxMMTestBase(WorldTestBase):
    game = "OOTxMM"


def door_of_time_conditions(test: WorldTestBase) -> list:
    return [cond for _, _, cond in test.world.logic.events["OOT_DOOR_OF_TIME_OPEN"]]


class TestDefaults(OOTxMMTestBase):
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
