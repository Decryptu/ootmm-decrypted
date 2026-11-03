from __future__ import annotations
from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification

from . import logic, prefill, ootxmm_staticdata

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
    # OoTMM's TRAPS and JUNK groups (logic/src/items/groups.ts) are traps and filler, and everything else
    # is useful. Items some condition of the player's logic asks for are progression instead (classification).
    if item["trap"]:
        return ItemClassification.trap
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
ITEM_BY_NAME = {item.display_name: item for item in OOTxMMItemList}

def progression_items(world: OOTxMM) -> set[str]:
    if hasattr(world, "logic"):
        return world.logic.items
    # An item link group's world, for which generate_early doesn't run: its items are its members'.
    members = world.multiworld.groups[world.player]["players"]
    return set().union(*(world.multiworld.worlds[player].logic.items for player in members))

def classification(world: OOTxMM, item: OOTxMMItemData) -> ItemClassification:
    if item.type != ItemClassification.trap and item.symbolic_id in progression_items(world):
        return ItemClassification.progression
    return item.type

def get_random_filler_item(world: OOTxMM) -> str:
    if not hasattr(world, "filler_item_names"):
        world.filler_item_names = sorted(
            item.display_name for item in OOTxMMItemList if classification(world, item) == ItemClassification.filler)
    return world.random.choice(world.filler_item_names)

def create_item_with_correct_classification(world: OOTxMM, item_name: str) -> OOTxMMItem:
    item = ITEM_BY_NAME[item_name]
    return OOTxMMItem(item_name, classification(world, item), item.id, world.player)

def create_all_items(world: OOTxMM) -> None:
    # OoTMM's base pool (makePools in packages/logic/src/world/transform.ts): the vanilla item of every
    # check, plus the extra items. The pool must match the number of locations, so the extra items
    # replace random filler.
    prefill.place_fixed(world)
    unfilled = world.multiworld.get_unfilled_locations(world.player)
    pool = [ITEM_BY_SYMBOLIC_ID[ootxmm_staticdata.OOTxMMCheckItems[location.name]] for location in unfilled]
    pool = [ITEM_BY_NAME[get_random_filler_item(world)] if prefill.removed_item(world, item.symbolic_id) else item for item in pool]
    filler = [i for i, item in enumerate(pool) if classification(world, item) == ItemClassification.filler]
    for i, extra in zip(world.random.sample(filler, len(logic.EXTRA_ITEMS)), logic.EXTRA_ITEMS):
        pool[i] = ITEM_BY_SYMBOLIC_ID[extra]
    created = [create_item_with_correct_classification(world, item.display_name) for item in pool]
    world.multiworld.itempool += prefill.split_pool(world, created)
