from collections.abc import Mapping
from typing import Any

from worlds.AutoWorld import World

from . import web_world, options, items, locations, regions, rules

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
    
    origin_region_name = "TEST_Overworld"
    
    def create_regions(self) -> None:
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

    # There may be data that the game client will need to modify the behavior of the game.
    # This is what slot_data exists for. Upon every client connection, the slot's slot_data is sent to the client.
    # slot_data is just a dictionary using basic types, that will be converted to json when sent to the client.
    def fill_slot_data(self) -> Mapping[str, Any]:
        # If you need access to the player's chosen options on the client side, there is a helper for that.
        return self.options.as_dict(
            "hard_mode", "secret_testing_data"
        )
