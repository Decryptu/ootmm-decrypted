from __future__ import annotations
from collections import Counter
import logging
from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification

from . import logic, prefill, ootxmm_staticdata

if TYPE_CHECKING:
    from BaseClasses import Location, MultiWorld
    from .world import OOTxMM


def minimize_barren(multiworld: MultiWorld, worlds: list[OOTxMM]) -> None:
    """Replace optional OOTxMM placements while preserving all slots' accessibility."""
    from Fill import FillError
    from .rules import TRIFORCE_ASPECTS, TRIFORCE_PIECE

    protected = {ITEM_BY_SYMBOLIC_ID[item].id for item in (*TRIFORCE_ASPECTS, TRIFORCE_PIECE)}
    candidates = [
        location for world in worlds for location in multiworld.get_filled_locations(world.player)
        if location.address is not None and not location.locked and not location.item.trap
        and location.item.game == world.game and location.item.code not in protected
    ]
    if not candidates:
        return
    if not multiworld.fulfills_accessibility():
        raise FillError("Barren requires a beatable seed that satisfies accessibility before item removal.")
    multiworld.random.shuffle(candidates)

    def try_remove(locations: list[Location]) -> int:
        originals = [location.item for location in locations]
        for location in locations:
            world = multiworld.worlds[location.player]
            item = world.create_item(ITEM_BY_SYMBOLIC_ID["NOTHING"].display_name)
            location.item = item
            item.location = location
        valid = False
        try:
            valid = multiworld.fulfills_accessibility()
        except FillError:
            valid = False
        finally:
            if not valid:
                for location, item in zip(locations, originals):
                    location.item.location = None
                    location.item = item
        if valid:
            for item in originals:
                item.location = None
            return len(locations)
        if len(locations) == 1:
            return 0
        middle = len(locations) // 2
        return try_remove(locations[:middle]) + try_remove(locations[middle:])

    optional = [location for location in candidates if not location.advancement]
    progression = [location for location in candidates if location.advancement]
    removed = (try_remove(optional) if optional else 0) + (try_remove(progression) if progression else 0)
    logging.info("Barren replaced %d optional placements with Nothing.", removed)

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
        return world.progression_items
    # An item link group's world, for which generate_early doesn't run: its items are its members'.
    members = world.multiworld.groups[world.player]["players"]
    return set().union(*(progression_items(world.multiworld.worlds[player]) for player in members))

def classification(world: OOTxMM, item: OOTxMMItemData) -> ItemClassification:
    if item.type != ItemClassification.trap and item.symbolic_id in progression_items(world):
        return ItemClassification.progression
    return item.type

def get_random_filler_item(world: OOTxMM) -> str:
    if not hasattr(world, "filler_item_names"):
        settings = getattr(world, "ootmm_settings", {})
        world.filler_item_names = sorted(
            item.display_name for item in OOTxMMItemList if classification(world, item) == ItemClassification.filler
            and item.symbolic_id not in logic.EQUIPMENT_ITEMS
            and logic.shared_item(item.symbolic_id, settings) == item.symbolic_id)
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
    # Source classes share fairy item IDs; replace only copies from starting sources.
    starting_sources = set().union(*(names for key, names in prefill.FAIRY_SETTINGS.items()
                                    if logic._value(world.ootmm_settings, key) == "starting"))
    pool = [ITEM_BY_NAME[get_random_filler_item(world)] if location.name in starting_sources else item
            for location, item in zip(unfilled, pool)]
    pool = [ITEM_BY_NAME[get_random_filler_item(world)] if prefill.removed_item(world, item.symbolic_id) else item for item in pool]
    filler = [i for i, item in enumerate(pool) if classification(world, item) == ItemClassification.filler
              and item.symbolic_id not in logic.EQUIPMENT_ITEMS]
    extras = logic.extra_items(world.ootmm_settings)
    if len(filler) < len(extras):
        raise ValueError(f"Not enough junk slots for optional items: {len(filler)} slots for {len(extras)} items. Enable more check shuffles.")
    for i, extra in zip(world.random.sample(filler, len(extras)), extras):
        pool[i] = ITEM_BY_SYMBOLIC_ID[extra]
    symbols = [item.symbolic_id for item in pool]
    fixed_ocarinas = 0
    if logic._value(world.ootmm_settings, "sharedOcarina"):
        # OoTMM merges all three ocarinas before removing the two fixed OoT pickups, if any.
        fixed_ocarinas = sum(location.locked and location.item is not None
                             and location.item.name == ITEM_BY_SYMBOLIC_ID["SHARED_OCARINA"].display_name
                             for location in world.multiworld.get_filled_locations(world.player))
        symbols.extend(["OOT_OCARINA"] * fixed_ocarinas)
    transformed = logic.transform_pool(symbols, world.ootmm_settings)
    if fixed_ocarinas:
        transformed["SHARED_OCARINA"] = max(0, transformed["SHARED_OCARINA"] - fixed_ocarinas)
    mode = logic._value(world.ootmm_settings, "itemPool")
    if mode != "normal":
        fixed = Counter(ITEM_BY_NAME[location.item.name].symbolic_id
                        for location in world.multiworld.get_filled_locations(world.player)
                        if location.locked and location.item and location.item.name in ITEM_BY_NAME)
        transformed.update(fixed)
        # OoTMM applies pool modes after making key rings and adding spare bottles afterwards.
        spare_bottles = 2 if (logic._value(world.ootmm_settings, "extraBottlesOot")
                              and not logic._value(world.ootmm_settings, "sharedBottles")) else 0
        transformed["OOT_BOTTLE_EMPTY"] -= spare_bottles
        if logic._value(world.ootmm_settings, "smallKeyShuffleOot") == "ownDungeon":
            transformed["OOT_SMALL_KEY_FIRE"] = max(0, transformed["OOT_SMALL_KEY_FIRE"] - 1)
        rings = logic.key_rings(world.ootmm_settings)
        for key, ring in rings.items():
            if transformed.pop(key, 0):
                transformed[ring] = 1
        logic.apply_item_pool_mode(transformed, world.ootmm_settings)
        transformed["OOT_BOTTLE_EMPTY"] += spare_bottles
        transformed = +(transformed - fixed)
    if logic._value(world.ootmm_settings, "pondFishShuffle"):
        logic.pond_fish_pool(transformed, world.random)
    transformed.update(world.goal_items)
    capacity = len(pool)
    pool = [ITEM_BY_SYMBOLIC_ID[symbolic] for symbolic, count in transformed.items() for _ in range(count)]
    excess = len(pool) - capacity
    if excess > 0:
        filler = [i for i, item in enumerate(pool) if classification(world, item) == ItemClassification.filler
                  and item.symbolic_id not in logic.EQUIPMENT_ITEMS]
        if excess > len(filler):
            raise ValueError(f"Not enough junk slots for pool additions: {len(filler)} slots for {excess} items. "
                             "Enable more check shuffles or reduce the Triforce piece count.")
        replaced = set(world.random.sample(filler, excess))
        pool = [item for i, item in enumerate(pool) if i not in replaced]
    pool += [ITEM_BY_NAME[get_random_filler_item(world)] for _ in range(capacity - len(pool))]
    # Vanilla Fire Temple uses one fewer key unless keys are shuffled anywhere (OoTMM transform.ts).
    if mode == "normal" and logic._value(world.ootmm_settings, "smallKeyShuffleOot") == "ownDungeon":
        index = next(i for i, item in enumerate(pool) if item.symbolic_id == "OOT_SMALL_KEY_FIRE")
        pool[index] = ITEM_BY_NAME[get_random_filler_item(world)]
    for key, ring in (logic.key_rings(world.ootmm_settings).items() if mode == "normal" else ()):
        indices = [i for i, item in enumerate(pool) if item.symbolic_id == key]
        for i in indices:
            pool[i] = ITEM_BY_NAME[get_random_filler_item(world)]
        if indices:
            pool[indices[0]] = ITEM_BY_SYMBOLIC_ID[ring]
    created = [create_item_with_correct_classification(world, item.display_name) for item in pool]
    world.multiworld.itempool += prefill.split_pool(world, created)
