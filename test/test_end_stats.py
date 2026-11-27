import asyncio
import struct
import unittest
from types import SimpleNamespace
from unittest import mock

from NetUtils import NetworkItem

from .. import client, end_stats, locations, ootxmm_staticdata
from .test_client import FakeGame, MAILBOX


class TestEndStats(unittest.TestCase):
    def _sample_locations(self):
        oot_dungeon = [
            (name, locations.LOCATION_NAME_TO_ID[name])
            for name, info in ootxmm_staticdata.OOTxMMCheckInfo["checks"].items()
            if name.startswith("OOT ") and info[2] and name in locations.LOCATION_NAME_TO_ID
        ]
        oot_overworld = [
            (name, locations.LOCATION_NAME_TO_ID[name])
            for name, info in ootxmm_staticdata.OOTxMMCheckInfo["checks"].items()
            if name.startswith("OOT ") and not info[2] and name in locations.LOCATION_NAME_TO_ID
        ]
        mm_overworld = [
            (name, locations.LOCATION_NAME_TO_ID[name])
            for name, info in ootxmm_staticdata.OOTxMMCheckInfo["checks"].items()
            if name.startswith("MM ") and not info[2] and name in locations.LOCATION_NAME_TO_ID
        ]
        return oot_dungeon, oot_overworld, mm_overworld

    def test_collect_stats_breakdowns_and_senders(self) -> None:
        oot_dungeon, oot_overworld, mm_overworld = self._sample_locations()
        checked = {oot_dungeon[0][1], oot_overworld[0][1], mm_overworld[0][1]}
        missing = {oot_dungeon[1][1], mm_overworld[1][1]}

        ids = ootxmm_staticdata.OOTxMMItemIDs
        received = [
            NetworkItem(ids["OOT_HOOKSHOT"], 1, 2, end_stats.FLAG_PROGRESSION),
            NetworkItem(ids["MM_MASK_BUNNY"], 2, 2, end_stats.FLAG_PROGRESSION),
            NetworkItem(ids["SHARED_BOW"], 3, 3, end_stats.FLAG_USEFUL),
            NetworkItem(ids["OOT_RUPEE_GREEN"], 4, 3, 0),
            NetworkItem(ids["OOT_TRAP_ICE"], 5, 4, end_stats.FLAG_TRAP),
            NetworkItem(ids["OOT_TRAP_ICE"], 6, 4, end_stats.FLAG_TRAP),
        ]

        ctx = SimpleNamespace(
            slot=1,
            server_seed_name="seed-123",
            player_names={1: "Link", 2: "Zelda", 3: "Saria", 4: "SkullKid"},
            checked_locations=checked,
            missing_locations=missing,
            items_received=received,
            slot_data={"settings": {"goal": "both", "itemPool": "normal"}},
        )
        run_stats = {
            "started_at": 1000.0,
            "finished_at": 4600.0,
            "active_seconds": 3600.0,
            "game_switches": 7,
            "boss_order": ["MM_MAJORA", "OOT_GANON"],
        }

        stats = end_stats.collect_stats(ctx, {"OOT_GANON", "MM_MAJORA"}, last_query=6, run_stats=run_stats)
        self.assertEqual(stats.player_name, "Link")
        self.assertEqual(stats.goal_label, "Defeat Ganon & Majora")
        self.assertEqual(stats.goal_detail, "Defeated: Majora -> Ganon")
        self.assertEqual(stats.overall.checked, 3)
        self.assertEqual(stats.overall.total, 5)
        self.assertEqual(stats.oot.checked, 2)
        self.assertEqual(stats.oot.total, 3)
        self.assertEqual(stats.mm.checked, 1)
        self.assertEqual(stats.mm.total, 2)
        self.assertEqual(stats.dungeons.checked, 1)
        self.assertEqual(stats.overworld.checked, 2)
        self.assertEqual(stats.items_received_total, 6)
        self.assertEqual(stats.items_progression, 2)
        self.assertEqual(stats.items_useful, 1)
        self.assertEqual(stats.items_filler, 1)
        self.assertEqual(stats.items_trap, 2)
        self.assertEqual(stats.items_oot, 4)
        self.assertEqual(stats.items_mm, 1)
        self.assertEqual(stats.items_shared, 1)
        self.assertEqual(stats.top_senders[0].name, "Zelda")
        self.assertEqual(stats.top_senders[0].progression, 2)
        self.assertIsNotNone(stats.top_trickster)
        self.assertEqual(stats.top_trickster.name, "SkullKid")
        self.assertEqual(stats.top_trickster.traps, 2)
        self.assertEqual(stats.game_switches, 7)
        self.assertAlmostEqual(stats.elapsed_seconds, 3600.0)
        self.assertAlmostEqual(stats.checks_per_hour, 3.0)

        report = end_stats.format_text_report(stats)
        self.assertIn("OOTxMM VICTORY — END STATS", report)
        self.assertIn("Defeated: Majora -> Ganon", report)
        self.assertIn("SkullKid (2 traps)", report)
        self.assertIn("OoT<->MM Switches: 7", report)

    def test_all_goal_targets_format_cleanly(self) -> None:
        ids = ootxmm_staticdata.OOTxMMItemIDs
        piece = ids["SHARED_TRIFORCE"]
        power = ids["SHARED_TRIFORCE_POWER"]
        courage = ids["SHARED_TRIFORCE_COURAGE"]
        wisdom = ids["SHARED_TRIFORCE_WISDOM"]

        cases = [
            ("ganon", {"OOT_GANON"}, {}, [], "Ganon defeated"),
            ("majora", {"MM_MAJORA"}, {}, [], "Majora defeated"),
            ("any", {"MM_MAJORA"}, {}, [], "Cleared via: Majora"),
            ("both", {"OOT_GANON", "MM_MAJORA"}, {}, [], "Defeated:"),
            (
                "triforce",
                set(),
                {"triforceGoal": 3, "triforcePieces": 5},
                [NetworkItem(piece, 1, 2, 1), NetworkItem(piece, 2, 2, 1)],
                "3/3 Triforce Pieces collected (1 local, 2 received; 5 in pool)",
            ),
            (
                "triforce3",
                set(),
                {},
                [NetworkItem(courage, 1, 2, 1), NetworkItem(wisdom, 2, 2, 1)],
                "Power: Yes | Courage: Yes | Wisdom: Yes",
            ),
        ]

        for goal_key, goals, extra_settings, received, expected_snippet in cases:
            with self.subTest(goal=goal_key):
                local_triforce = {}
                checked = set()
                if goal_key == "triforce":
                    local_triforce = {"100001": piece}
                    checked = {100001}
                elif goal_key == "triforce3":
                    local_triforce = {"100001": power}
                    checked = {100001}
                ctx = SimpleNamespace(
                    slot=1,
                    server_seed_name="seed",
                    player_names={1: "Hero", 2: "Ally"},
                    checked_locations=checked,
                    missing_locations=set(),
                    items_received=received,
                    slot_data={
                        "settings": {"goal": goal_key, **extra_settings},
                        "local_triforce": local_triforce,
                    },
                )
                stats = end_stats.collect_stats(ctx, goals, last_query=len(received))
                self.assertIn(expected_snippet, stats.goal_detail)
                self.assertIn(stats.goal_label, end_stats.format_text_report(stats))

    def test_client_shows_end_stats_on_goal_and_tracks_game_switches(self) -> None:
        game = FakeGame()
        game.set_u32(16, 1)
        cli = client.OOTxMMClient()
        cli.mailbox = MAILBOX
        cli.last_mailbox = MAILBOX
        cli.seq_net = 1
        sent: list[dict] = []

        async def send_msgs(msgs):
            sent.extend(msgs)
            for msg in msgs:
                if msg["cmd"] == "Set" and msg.get("want_reply", True):
                    cli.on_package(ctx, "SetReply", {
                        "key": msg["key"], "value": msg["operations"][0]["value"]})

        tabs_added = []
        fake_tab = SimpleNamespace(released=False)
        fake_tab.on_release = lambda: setattr(fake_tab, "released", True)
        fake_ui = SimpleNamespace(
            add_client_tab=lambda title, widget: (tabs_added.append((title, widget)), fake_tab)[1],
            remove_client_tab=lambda tab: None,
        )

        ctx = SimpleNamespace(
            bizhawk_ctx=None,
            items_received=[],
            checked_locations=set(),
            missing_locations=set(),
            locations_checked=set(),
            finished_game=False,
            server_seed_name="test-seed",
            team=0,
            slot=1,
            player_names={1: "Link"},
            slot_data={"settings": {"goal": "ganon"}},
            send_msgs=send_msgs,
            ui=fake_ui,
        )
        asyncio.run(cli.sync_goals(ctx))
        sent.clear()

        # Simulate switching to another game's mailbox address.
        other = 0x2000
        game.ram[other:other + 16] = client.MAGIC
        cli.candidates = {other: 0}
        struct.pack_into(">I", game.ram, other + 20, 1)
        with mock.patch.object(client.bizhawk, "read", game.read):
            asyncio.run(cli.check_candidates(ctx, [other]))
        self.assertEqual(cli.run_stats.get("game_switches"), 1)

        # Switch back to MAILBOX and defeat Ganon.
        cli.mailbox = MAILBOX
        cli.seq_net = 1
        gi = ootxmm_staticdata.OOTxMMCheckInfo["goalGi"]["OOT_GANON"]
        game.send(struct.pack(">IBIBBBhhI", 7, client.OP_WAL, 1, client.WAL_ITEM, client.OUR_WORLD, 0, gi, 0, 0))

        with mock.patch.object(client.bizhawk, "read", game.read), \
                mock.patch.object(client.bizhawk, "guarded_write", game.guarded_write), \
                mock.patch.object(end_stats, "_build_kivy_widget", return_value=object()), \
                mock.patch("kivy.clock.Clock.schedule_once", side_effect=lambda fn, _dt=0: fn(0)):
            asyncio.run(cli.exchange(ctx))

        self.assertTrue(ctx.finished_game)
        self.assertEqual(sent[-1]["cmd"], "StatusUpdate")
        self.assertTrue(cli.end_stats_shown)
        self.assertIsNotNone(cli.last_end_stats)
        self.assertEqual(cli.last_end_stats.game_switches, 1)
        self.assertEqual(len(tabs_added), 1)
        self.assertEqual(tabs_added[0][0], end_stats.END_STATS_TAB_TITLE)
        self.assertTrue(fake_tab.released)
