from unittest import TestCase

from BaseClasses import Item, ItemClassification, MultiWorld, Region
from worlds.AutoWorld import World

from ..world import assign_gossip_hints


class TestGossip(TestCase):
    def test_cross_world_progression_and_foolish_region(self):
        multiworld = MultiWorld(2)
        multiworld.set_seed(42)
        multiworld.player_name = {1: "Link", 2: "Zelda"}
        multiworld.worlds = {player: World(multiworld, player) for player in (1, 2)}

        local = Region("Menu", 1, multiworld)
        remote = Region("Menu", 2, multiworld)
        empty = Region("Empty Cave", 1, multiworld)
        inaccessible = Region("Unreachable Cave", 1, multiworld)
        multiworld.regions.extend([local, remote, empty, inaccessible])
        local.connect(empty)
        local.add_locations({"Chest": 1, "Optional Chest": 2})
        remote.add_locations({"Remote Chest": 1, "Remote Optional Chest": 2})
        empty.add_locations({"Pot": 3, "Other Pot": 4})
        inaccessible.add_locations({"Unreachable Chest": 5})

        for player, check, item, recipient in [
            (1, "Chest", "Zelda's Key", 2),
            (2, "Remote Chest", "Link's Key", 1),
            (1, "Optional Chest", "Map", 2),
            (2, "Remote Optional Chest", "Compass", 1),
            (1, "Unreachable Chest", "Hidden Key", 1),
        ]:
            location = multiworld.get_location(check, player)
            location.place_locked_item(Item(item, ItemClassification.progression, 1, recipient))
        for check in ("Pot", "Other Pot"):
            multiworld.get_location(check, 1).place_locked_item(Item("Rupee", ItemClassification.filler, 2, 1))
        multiworld.completion_condition = {
            1: lambda state: state.has("Link's Key", 1),
            2: lambda state: state.has("Zelda's Key", 2),
        }

        world = multiworld.worlds[1]
        assign_gossip_hints(multiworld, [world])
        self.assertCountEqual(world.gossip_hints, [
            "Chest is on the Way of the Hero",
            "Remote Chest (P2) is on the Way of the Hero",
            "plundering Empty Cave is a foolish choice",
            "Optional Chest holds Map for Zelda",
            "Remote Optional Chest (P2) holds Compass",
        ])
