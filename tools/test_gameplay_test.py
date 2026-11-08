import unittest

from gameplay_test import validate


class TestGameplayValidation(unittest.TestCase):
    def test_signal_message_dismissal_requires_boolean(self):
        scenario = self.scenario()
        for value in (False, True):
            scenario["steps"] = [{"action": "wait_signal", "name": "ready", "timeout_frames": 100,
                                  "dismiss_messages": value}]
            validate(scenario)
        for value in (1, "true", None):
            scenario["steps"][0]["dismiss_messages"] = value
            with self.subTest(value=value), self.assertRaises(ValueError):
                validate(scenario)

    def test_native_exit_requires_both_layouts_and_assisted_coverage(self):
        scenario = self.scenario()
        scenario["mm_layout"] = dict(scenario["oot_layout"])
        scenario["steps"] = [{"action": "native_exit", "game": "mm", "scene": 111,
                              "target_game": "oot", "target_scene": 32, "x": -278,
                              "y": 0, "z": -775, "timeout_frames": 100}]
        validate(scenario)
        for changes in ({"target_game": "mm"}, {"timeout_frames": 101}, {"x": float("nan")}):
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                validate({**scenario, "steps": [{**scenario["steps"][0], **changes}]})
        scenario["coverage"] = "unmodified-gameplay"
        with self.assertRaises(ValueError):
            validate(scenario)
        scenario["coverage"] = "assisted-gameplay"
        del scenario["mm_layout"]
        with self.assertRaises(ValueError):
            validate(scenario)

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

    def test_signal_health_support_requires_assisted_sourced_scene(self):
        scenario = self.scenario()
        scenario["steps"] = [{"action": "wait_signal", "name": "ready", "timeout_frames": 100,
                              "keep_health": True, "game": "oot", "scene": 62}]
        validate(scenario)
        scenario["coverage"] = "unmodified-gameplay"
        with self.assertRaises(ValueError):
            validate(scenario)
        scenario["coverage"] = "assisted-gameplay"
        scenario["steps"][0]["game"] = "mm"
        with self.assertRaises(ValueError):
            validate(scenario)

    def test_signal_rejects_paths_and_unbounded_waits(self):
        scenario = self.scenario()
        for name in ("arrived-mm", "stage_2"):
            scenario["steps"] = [{"action": "wait_signal", "name": name, "timeout_frames": 100}]
            validate(scenario)
        for name in ("", "../ready", "a/b", "a\\b"):
            scenario["steps"][0]["name"] = name
            with self.subTest(name=name), self.assertRaises(ValueError):
                validate(scenario)
        scenario["steps"][0].update(name="ready", timeout_frames=101)
        with self.assertRaises(ValueError):
            validate(scenario)


if __name__ == "__main__":
    unittest.main()
