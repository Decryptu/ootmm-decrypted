from __future__ import annotations
from typing import TYPE_CHECKING

from BaseClasses import Item, Location
from Fill import FillError, fill_restrictive

from . import logic, ootxmm_staticdata

if TYPE_CHECKING:
    from .world import OOTxMM

# What OoTMM's solver (packages/logic/src/solver/solve.ts) does before its main fill, exported by
# raw/GenerateMetadata.py (GenerateFillFile) for OoTMM's defaults of the item placement settings, none of
# which the world offers yet. The ROM relies on it: under these defaults a check in a dungeon gives a key for
# that dungeon, whichever key was placed there, and shops, scrubs and cows keep their vanilla items.
_fill = ootxmm_staticdata.OOTxMMFill
FIXED = set(_fill["fixed"])
SONG_LOCATIONS = set(_fill["songLocations"])
SONG_ITEMS = set(_fill["songItems"])
WARP_LOCATIONS = set(_fill["warpLocations"])
REWARD_ITEMS = set(_fill["rewardItems"])

def _dungeon_groups() -> list[tuple[set[str], set[str]]]:
    # fixDungeon: Stone Tower's items also go to Inverted Stone Tower, Ganon's Castle's to Ganon's Tower.
    groups = []
    for dungeon, items in _fill["dungeonItems"].items():
        locations = set(_fill["dungeons"][dungeon])
        if dungeon == "ST":
            locations |= set(_fill["dungeons"]["IST"])
        if dungeon == "Ganon":
            locations |= set(_fill["dungeons"]["Tower"])
        if items:
            groups.append((set(items), locations))
    return groups

DUNGEON_GROUPS = _dungeon_groups()
ATTEMPTS = 10

def place_fixed(world: OOTxMM) -> None:
    """The checks that keep their vanilla item (OoTMM's fixer, packages/logic/src/misc/fixer.ts)."""
    from .items import ITEM_BY_SYMBOLIC_ID, create_item_with_correct_classification
    for location in world.multiworld.get_unfilled_locations(world.player):
        if location.name in FIXED:
            vanilla = ootxmm_staticdata.OOTxMMCheckItems[location.name]
            location.place_locked_item(create_item_with_correct_classification(world, ITEM_BY_SYMBOLIC_ID[vanilla].display_name))

def removed_item(world: OOTxMM, item: str) -> bool:
    """Items OoTMM takes out of the pool (run() in its world/transform.ts); their checks get filler."""
    return item == "OOT_BOSS_KEY_GANON" and logic._value(world.ootmm_settings, "ganonBossKey") in ("removed", "custom")

def _groups(world: OOTxMM) -> list[tuple[set[str], set[str]]]:
    """(OoTMM items, checks they must go to), in placing order."""
    # OoTMM places songs first. Here the rewards go first: 13 rewards for 13 bosses is the tighter fit, and
    # the songs then have 23 checks to spread over, which the greedy fill copes with far better.
    groups = []
    if logic._value(world.ootmm_settings, "dungeonRewardShuffle") == "dungeonBlueWarps":
        groups.append((REWARD_ITEMS, WARP_LOCATIONS))
    if logic._value(world.ootmm_settings, "songs") == "songLocations":
        groups.append((SONG_ITEMS, SONG_LOCATIONS))
    return groups + DUNGEON_GROUPS

def _symbolic(item: Item) -> str:
    from .items import ITEM_BY_NAME
    return ITEM_BY_NAME[item.name].symbolic_id

def split_pool(world: OOTxMM, pool: list[Item]) -> list[Item]:
    """Keeps the items pre_fill places out of the pool (in world.pre_fill_pending), returns the rest."""
    restricted = set().union(*(items for items, _ in _groups(world)))
    world.pre_fill_pending = [item for item in pool if _symbolic(item) in restricted]
    return [item for item in pool if _symbolic(item) not in restricted]

def pre_fill(world: OOTxMM) -> None:
    # The fill is greedy and can corner itself: songs placed first can sit at checks that need the spiritual
    # stones while the bosses holding the stones need those songs. Like OoTMM's solver (retry), start over.
    pending = list(world.pre_fill_pending)
    for attempt in range(ATTEMPTS):
        world.pre_fill_pending = list(pending)
        placed: list[Location] = []
        try:
            for items, names in _groups(world):
                _place_group(world, items, names, placed)
            return
        except FillError:
            if attempt == ATTEMPTS - 1:
                raise
            for location in placed:
                location.item.location = None
                location.item = None
                location.locked = False

def _place_group(world: OOTxMM, items: set[str], names: set[str], placed: list[Location]) -> None:
    multiworld = world.multiworld
    group = [item for item in world.pre_fill_pending if _symbolic(item) in items]
    if not group:
        return
    for item in group:
        world.pre_fill_pending.remove(item)
    locations = [location for location in multiworld.get_unfilled_locations(world.player) if location.name in names]
    placed += locations
    world.random.shuffle(locations)
    world.random.shuffle(group)
    # Everything but this group: the pool, the groups still to place (get_pre_fill_items) and what is placed.
    fill_restrictive(multiworld, multiworld.get_all_state(), locations, group, single_player_placement=True,
                     lock=True, allow_excluded=True, name=f"OOTxMM pre-fill {world.player}")
