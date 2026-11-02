from __future__ import annotations
from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification

from . import ootxmm_staticdata

if TYPE_CHECKING:
    from .world import OOTxMM

class OOTxMMItem(Item):
    game = "OOTxMM"

class OOTxMMItemData:
    def __init__(self, id: int, symbolic_id: str, display_name: str, type: ItemClassification):
        self.id = id
        self.symbolic_id = symbolic_id
        self.display_name = display_name
        self.type = type

def classify(item: dict) -> ItemClassification:
    # OoTMM's TRAPS and JUNK groups (logic/src/items/groups.ts). Everything else counts as progression
    # until the logic tells which items it needs.
    if item["trap"]:
        return ItemClassification.trap
    if item["junk"]:
        return ItemClassification.filler
    return ItemClassification.progression

# Built from OoTMM's item list by raw/GenerateMetadata.py. NOTHING is OoTMM's empty check, not an item.
OOTxMMItemList: list[OOTxMMItemData] = [
    OOTxMMItemData(ootxmm_staticdata.OOTxMMItemIDs[item["id"]], item["id"], item["name"], classify(item))
    for item in ootxmm_staticdata.OOTxMMItemData
    if item["id"] != "NOTHING"
]

ITEM_NAME_TO_ID = {item.display_name: item.id for item in OOTxMMItemList}
ITEM_NAME_TO_CLASS = {item.display_name: item.type for item in OOTxMMItemList}
FILLER_ITEM_NAMES = sorted(item.display_name for item in OOTxMMItemList if item.type == ItemClassification.filler)

def get_random_filler_item(world: OOTxMM) -> str:
    return world.random.choice(FILLER_ITEM_NAMES)

def create_item_with_correct_classification(world: OOTxMM, item_name: str) -> OOTxMMItem:
    return OOTxMMItem(item_name, ITEM_NAME_TO_CLASS[item_name], ITEM_NAME_TO_ID[item_name], world.player)

def create_all_items(world: OOTxMM) -> None:
    # Placeholder pool until OoTMM's pool rules are ported: one of every non-junk item, then filler.
    itempool: list[Item] = [
        create_item_with_correct_classification(world, item.display_name)
        for item in OOTxMMItemList
        if item.type == ItemClassification.progression
    ]
    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))
    itempool += [world.create_filler() for _ in range(number_of_unfilled_locations - len(itempool))]
    world.multiworld.itempool += itempool
