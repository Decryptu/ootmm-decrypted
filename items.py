from __future__ import annotations
from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification

from . import logic, ootxmm_staticdata

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
    # Items some condition asks for are progression. Of the rest, OoTMM's TRAPS and JUNK groups
    # (logic/src/items/groups.ts) are traps and filler, and everything else is useful.
    if item["trap"]:
        return ItemClassification.trap
    if item["id"] in logic.LOGIC_ITEMS:
        return ItemClassification.progression
    if item["junk"]:
        return ItemClassification.filler
    return ItemClassification.useful

# Built from OoTMM's item list by raw/GenerateMetadata.py.
OOTxMMItemList: list[OOTxMMItemData] = [
    OOTxMMItemData(ootxmm_staticdata.OOTxMMItemIDs[item["id"]], item["id"], item["name"], classify(item))
    for item in ootxmm_staticdata.OOTxMMItemData
]
ITEM_BY_SYMBOLIC_ID = {item.symbolic_id: item for item in OOTxMMItemList}

ITEM_NAME_TO_ID = {item.display_name: item.id for item in OOTxMMItemList}
ITEM_NAME_TO_CLASS = {item.display_name: item.type for item in OOTxMMItemList}
FILLER_ITEM_NAMES = sorted(item.display_name for item in OOTxMMItemList if item.type == ItemClassification.filler)

def get_random_filler_item(world: OOTxMM) -> str:
    return world.random.choice(FILLER_ITEM_NAMES)

def create_item_with_correct_classification(world: OOTxMM, item_name: str) -> OOTxMMItem:
    return OOTxMMItem(item_name, ITEM_NAME_TO_CLASS[item_name], ITEM_NAME_TO_ID[item_name], world.player)

def create_all_items(world: OOTxMM) -> None:
    # OoTMM's base pool (makePools in packages/logic/src/world/transform.ts): the vanilla item of every
    # check, plus the extra items. The pool must match the number of locations, so the extra items
    # replace random filler.
    unfilled = world.multiworld.get_unfilled_locations(world.player)
    pool = [ITEM_BY_SYMBOLIC_ID[ootxmm_staticdata.OOTxMMCheckItems[location.name]] for location in unfilled]
    filler = [i for i, item in enumerate(pool) if item.type == ItemClassification.filler]
    for i, extra in zip(world.random.sample(filler, len(logic.EXTRA_ITEMS)), logic.EXTRA_ITEMS):
        pool[i] = ITEM_BY_SYMBOLIC_ID[extra]
    world.multiworld.itempool += [create_item_with_correct_classification(world, item.display_name) for item in pool]
