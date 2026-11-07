import unittest

from gameplay_test import validate


class TestGameplayValidation(unittest.TestCase):
    def scenario(self, **step):
        return {"coverage": "assisted-gameplay", "description": "Native return",
                "limitations": "No item receipt asserted", "max_frames": 100,
                "required_rom_sha256": "0" * 64,
                "oot_layout": {"play_pointer": 0x1000, "main": 0x80002000, "source": "Matching payload symbols"},
                "steps": [{"action": "wait_game", "game": "oot", "scene": 32,
                           "timeout_frames": 100, **step}]}

    def test_wait_game_requires_matching_layout_and_bounded_timeout(self):
        validate(self.scenario())
        for step in ({"game": "mm"}, {"game": "other"}, {"timeout_frames": 0},
                     {"timeout_frames": 101}, {"scene": -1}):
            with self.subTest(step=step), self.assertRaises(ValueError):
                validate(self.scenario(**step))

    def test_wait_client_is_bounded(self):
        scenario = self.scenario()
        scenario["steps"] = [{"action": "wait_client", "timeout_frames": 100}]
        validate(scenario)
        scenario["steps"][0]["timeout_frames"] = 101
        with self.assertRaises(ValueError):
            validate(scenario)


if __name__ == "__main__":
    unittest.main()
