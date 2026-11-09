import copy
from pathlib import Path
import tempfile
import unittest

from two_player_gameplay import completed_captures, expected_sources, stage_ready, validate_backlog, validate_restart


class TestGameplayStages(unittest.TestCase):
    def test_one_way_delivery_requires_the_expected_remote_source(self):
        players = [{"slot": 1, "checks": ["Local chest"], "received_index": 1},
                   {"slot": 2, "checks": ["Key chest"], "received_index": 0}]
        names = {10: "Local chest", 20: "Key chest", 21: "Other chest"}
        locations = {1: {10: (100, 1, 0)}, 2: {20: (200, 1, 0), 21: (201, 1, 0)}}
        self.assertEqual(expected_sources(players, locations, names), {1: {10}, 2: {20}})
        # An unrelated remote placement cannot satisfy a local-only expected source.
        locations[2][20] = (200, 2, 0)
        with self.assertRaisesRegex(AssertionError, "expected remote source"):
            expected_sources(players, locations, names)
        locations[2][20] = (200, 1, 0)
        players[1]["received_index"] = 1
        with self.assertRaisesRegex(AssertionError, "expected remote source"):
            expected_sources(players, locations, names)
        locations[1][10] = (100, 2, 0)
        self.assertEqual(expected_sources(players, locations, names), {1: {10}, 2: {20}})

    def test_restart_requires_a_stage_and_excludes_overlapping_outages(self):
        validate_restart(None, {"ready"}, None)
        validate_restart("ready", {"ready"}, None)
        for stage, backlog in (("absent", None), ([], None), (True, None),
                               ("ready", {"slot": 1})):
            with self.subTest(stage=stage, backlog=backlog), self.assertRaises(ValueError):
                validate_restart(stage, {"ready"}, backlog)

    def test_backlog_requires_other_players_real_expected_sources(self):
        players = [{"slot": 1, "checks": ["Own source"]},
                   {"slot": 2, "checks": ["First", "Second"]}]
        valid = {"slot": 1, "disconnect_stage": "ready", "checks": ["First", "Second"]}
        validate_backlog(None, players, {"ready"})
        validate_backlog(valid, players, {"ready"})
        for field, value in (("slot", 0), ("slot", True), ("disconnect_stage", "missing"),
                             ("checks", []), ("checks", ["First", "First"]),
                             ("checks", ["Own source"]), ("checks", "First"), ("checks", [1])):
            changed = dict(valid, **{field: value})
            with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                validate_backlog(changed, players, {"ready"})

    def test_only_completed_capture_events_release_a_stage(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "events.jsonl"
            self.assertEqual(completed_captures(path), [])
            path.write_text('{"event":"step","action":"capture"}\n'
                            '{"event":"capture","name":"ready"}\n'
                            '{"event":"capture","name":', encoding="utf-8")
            self.assertEqual(completed_captures(path), ["ready"])

    def test_all_conditions_must_hold_for_both_players(self):
        stage = {"players": [
            {"slot": 1, "capture": "mm-ready", "game": "mm", "received_index": 1, "checks": ["Chest"]},
            {"slot": 2, "capture": "oot-ready", "game": "oot", "received_index": 1}]}
        observations = {
            1: {"captures": ["mm-ready"], "game": "mm", "received_index": 1, "checks": ["Chest", "Song"]},
            2: {"captures": ["oot-ready"], "game": "oot", "received_index": 1, "checks": []}}
        self.assertTrue(stage_ready(stage, observations))
        for slot, field, value in ((1, "captures", []), (1, "game", "oot"), (1, "game", None),
                                   (1, "received_index", 0), (1, "received_index", 2), (1, "checks", []),
                                   (2, "captures", []), (2, "game", None), (2, "received_index", None)):
            changed = copy.deepcopy(observations)
            changed[slot][field] = value
            with self.subTest(slot=slot, field=field, value=value):
                self.assertFalse(stage_ready(stage, changed))


if __name__ == "__main__":
    unittest.main()
