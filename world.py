import json
import os
from collections import Counter, defaultdict
from collections.abc import Mapping
from itertools import takewhile
from typing import Any

from BaseClasses import ItemClassification

from Options import Choice, OptionSet, Toggle
from worlds.AutoWorld import World

from . import web_world, options, prefill, items, locations, logic, regions, rules, time_logic, prices

class OOTxMM(World):
    """
    OOTxMM is an Archipelago implementation that hooks into the OOTMM randomizer already
    combining TLoZ: Ocarina of Time and TLoZ: Majora's Mask
    into the Archipelago MultiWorld.
    """
    
    game = "OOTxMM"
    web = web_world.OOTxMMWebWorld()
    options_dataclass = options.OOTxMMOptions
    options: options.OOTxMMOptions
    
    
    location_name_to_id = locations.LOCATION_NAME_TO_ID
    item_name_to_id = items.ITEM_NAME_TO_ID
    
    origin_region_name = "OOT SPAWN"

    def generate_early(self) -> None:
        self.ootmm_settings = ootmm_settings(self.options)
        if self.ootmm_settings["goal"] == "triforce":
            self.ootmm_settings["triforceGoal"] = min(self.ootmm_settings["triforceGoal"],
                                                     self.ootmm_settings["triforcePieces"])
        self.prices = prices.generate(self.ootmm_settings, self.random)
        self.logic = logic.build({**self.ootmm_settings, "_prices": self.prices})
        self.goal_items = rules.triforce_items(self.ootmm_settings)
        self.progression_items = self.logic.items | self.goal_items.keys()

    def create_regions(self) -> None:
        self.time_logic = time_logic.TimeLogic(self.logic, self.player, {
            items.ITEM_BY_SYMBOLIC_ID[item].display_name: count
            for item, count in prefill.starting_fairies(self.ootmm_settings).items()})
        regions.create_and_connect_regions(self)
        locations.create_all_locations(self)

    def set_rules(self) -> None:
        rules.set_all_rules(self)

    def create_items(self) -> None:
        items.create_all_items(self)

    @classmethod
    def stage_pre_fill(cls, multiworld) -> None:
        prefill.pre_fill_all(multiworld)

    @classmethod
    def stage_pre_output(cls, multiworld) -> None:
        worlds = multiworld.get_game_worlds(cls.game)
        barren = [world for world in worlds if world.ootmm_settings["itemPool"] == "barren"]
        if barren:
            items.minimize_barren(multiworld, barren)
        assign_gossip_hints(multiworld, worlds)

    def get_pre_fill_items(self) -> list:
        # Restricted items kept out of the main pool until coordinated pre-fill places them.
        return getattr(self, "pre_fill_pending", [])

    def create_item(self, name: str) -> items.OOTxMMItem:
        return items.create_item_with_correct_classification(self, name)

    def get_filler_item_name(self) -> str:
        return items.get_random_filler_item(self)

    def generate_output(self, output_directory: str) -> None:
        # The player's file for the ROM patch (ootmm-ap/ap-patch.ts): settings and what is at each check.
        data = {
            "version": 1,
            # ap-patch.ts refuses files from another release: an older world drops settings it does not know.
            "world_version": self.world_version.as_simple_string(),
            "seed": f"{self.multiworld.seed_name}-{self.player}",
            "settings": self.ootmm_settings,
            "prices": self.prices,
            "gossip": getattr(self, "gossip_hints", []),
            "locations": {
                location.name: display_item(self, location.item)
                for location in self.multiworld.get_locations(self.player)
                if location.address is not None
            },
        }
        name = f"{self.multiworld.get_out_file_name_base(self.player)}.ootxmm.json"
        with open(os.path.join(output_directory, name), "w", encoding="utf-8") as f:
            json.dump(data, f)

    def fill_slot_data(self) -> Mapping[str, Any]:
        # The player's OoTMM settings, for the patch.
        data = {"settings": self.ootmm_settings}
        if self.goal_items:
            data["local_triforce"] = {
                str(location.address): location.item.code
                for location in self.multiworld.get_filled_locations(self.player)
                if location.address is not None and location.item.player == self.player
                and items.ITEM_BY_NAME[location.item.name].symbolic_id in self.goal_items
            }
        return data


def assign_gossip_hints(multiworld, worlds) -> None:
    """Analyze the final placements once, before player output runs in parallel."""
    reachable = [
        location
        for sphere in takewhile(bool, multiworld.get_spheres())
        for location in sorted(sphere)
    ]
    progression = [location for location in multiworld.get_filled_locations() if location.advancement]
    progression_regions = {location.parent_region for location in progression}
    copies = Counter((location.item.player, location.item.name) for location in progression)
    checks_by_region = defaultdict(list)
    for location in reachable:
        if location.address is not None:
            checks_by_region[location.parent_region].append(location)
    required = {}
    beatable = multiworld.can_beat_game(locations=progression)

    for world in worlds:
        player = world.player
        recipients = {player} | multiworld.get_player_groups(player)
        candidates = [
            location for location in reachable
            if location.address is not None and location.advancement
            and (location.player == player or location.item.player in recipients)
        ]
        world.random.shuffle(candidates)
        # Prefer scarcer progression over repeated ammo and currency placements.
        candidates.sort(key=lambda location: copies[location.item.player, location.item.name])

        def where(location):
            if location.player == player:
                return location.name
            return f"{location.name} (P{location.player})"

        paths = []
        path_checks = set()
        if beatable:
            # Bound the number of full multiworld replays per slot.
            for location in candidates[:16]:
                if location not in required:
                    required[location] = not multiworld.can_beat_game(
                        locations=[check for check in progression if check != location]
                    )
                if required[location]:
                    paths.append(f"{where(location)} is on the Way of the Hero")
                    path_checks.add(location)
                    if len(paths) == 4:
                        break

        foolish = [
            region.name for region, checks in checks_by_region.items()
            if region.player == player and region not in progression_regions and len(checks) >= 2
        ]
        world.random.shuffle(foolish)
        item_hints = []
        hinted_items = set()
        for location in candidates:
            item = location.item
            item_key = (item.player, item.name)
            if location in path_checks or item_key in hinted_items:
                continue
            hinted_items.add(item_key)
            recipient = "" if item.player == player else f" for {multiworld.get_player_name(item.player)}"
            item_hints.append(f"{where(location)} holds {item.name}{recipient}")
            if len(item_hints) == 6:
                break
        world.gossip_hints = paths + [f"plundering {name} is a foolish choice" for name in foolish[:4]] + item_hints


def ootmm_settings(opts: options.OOTxMMOptions) -> logic.Settings:
    """The OoTMM settings the options set, keyed and valued as OoTMM's settings."""
    settings: logic.Settings = {}
    for key in options.OOTMM_SETTINGS:
        option = getattr(opts, key)
        if isinstance(option, Choice):
            settings[key] = option.ootmm_values[option.value]
        elif isinstance(option, Toggle):
            settings[key] = bool(option.value)
        elif isinstance(option, OptionSet):
            settings[key] = sorted(option.value)
        else:
            settings[key] = int(option.value)
    return logic.normalize_shared_items(settings)

# What the game shows for another player's item: the item itself when it is an OoTMM one, else a stand-in
# for how much it matters.
FOREIGN_STAND_INS = {
    ItemClassification.progression: "SHARED_TRIFORCE",
    ItemClassification.useful: "OOT_HEART_PIECE",
}

def display_item(world: OOTxMM, item) -> list:
    """[OoTMM item, own] for a location's item, as the ROM patch reads it."""
    if item.game == world.game:
        return [items.ITEM_BY_NAME[item.name].symbolic_id, item.player == world.player]
    for classification, stand_in in FOREIGN_STAND_INS.items():
        if item.classification & classification:
            return [stand_in, False]
    return ["OOT_RUPEE_GREEN", False]
