from collections.abc import Mapping
from typing import Any

from Options import Choice, OptionSet, Toggle
from worlds.AutoWorld import World

from . import web_world, options, items, locations, logic, regions, rules

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
        # Compiled access rules, shared by every entrance and location with the same condition.
        self.rule_cache = {}
        regions.create_and_connect_regions(self)
        locations.create_all_locations(self)

    def set_rules(self) -> None:
        rules.set_all_rules(self)

    def create_items(self) -> None:
        items.create_all_items(self)

    def create_item(self, name: str) -> items.OOTxMMItem:
        return items.create_item_with_correct_classification(self, name)

    def get_filler_item_name(self) -> str:
        return items.get_random_filler_item(self)

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
    return settings
