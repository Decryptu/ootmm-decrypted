import json
import os
from collections.abc import Mapping
from typing import Any

from BaseClasses import ItemClassification

from Options import Choice, OptionSet, Toggle
from worlds.AutoWorld import World

from . import web_world, options, prefill, items, locations, logic, regions, rules, time_logic

class OOTxMM(World):
    """
    OOTxMM is an Archipelago implementation that hooks into the OOTMM randomizer already
    combining TLoZ: Ocarina of Time and TLoZ: Majora's Mask
    into a the Archipelago MultiWorld.
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
        self.logic = logic.build(self.ootmm_settings)

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
            "seed": f"{self.multiworld.seed_name}-{self.player}",
            "settings": self.ootmm_settings,
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
        return {"settings": self.ootmm_settings}

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
