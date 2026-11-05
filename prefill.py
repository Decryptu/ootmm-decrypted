from __future__ import annotations
from collections import Counter
from typing import TYPE_CHECKING

from BaseClasses import Item, Location
from Fill import FillError, fill_restrictive

from . import logic, ootxmm_staticdata

if TYPE_CHECKING:
    from .world import OOTxMM

# What OoTMM's solver (packages/logic/src/solver/solve.ts) does before its main fill, exported by
# raw/GenerateMetadata.py (GenerateFillFile) for OoTMM's defaults of the item placement settings.
# The ROM relies on it: under ownDungeon a check in a dungeon gives a key for
# that dungeon, whichever key was placed there, and shops, scrubs and cows keep their vanilla items.
_fill = ootxmm_staticdata.OOTxMMFill
FIXED = set(_fill["fixed"])
FAIRY_SETTINGS = {key: set(names) for key, names in _fill["fairyLocations"].items()}
FAIRY_LOCATIONS = set().union(*FAIRY_SETTINGS.values())
FAIRY_ITEMS = {ootxmm_staticdata.OOTxMMCheckItems[name] for name in FAIRY_LOCATIONS}
TINGLE_LOCATIONS = {name for name, item in ootxmm_staticdata.OOTxMMCheckItems.items()
                    if item.startswith("MM_WORLD_MAP_")}
TINGLE_ITEMS = {ootxmm_staticdata.OOTxMMCheckItems[name] for name in TINGLE_LOCATIONS}
MAP_SETTINGS = {"tingleShuffle"}
SONG_SETTINGS = {"songs"}
SONG_LOCATIONS = set(_fill["songLocations"])
SONG_ITEMS = set(_fill["songItems"])
WARP_LOCATIONS = set(_fill["warpLocations"])
REWARD_SETTINGS = {"dungeonRewardShuffle"}
REWARD_ITEMS = set(_fill["rewardItems"])
DUNGEON_SETTINGS = {key: set(items) for key, items in _fill["dungeonShuffleItems"].items()}
DUNGEON_SETTINGS["ganonBossKey"] = {"OOT_BOSS_KEY_GANON"}
SPECIAL_KEY_LOCATIONS = {
    "smallKeyShuffleHideout": {name for name, item in ootxmm_staticdata.OOTxMMCheckItems.items()
                              if item == "OOT_SMALL_KEY_GF"},
    "smallKeyShuffleChestGame": {name for name, (_, scene, _) in logic._check_info["checks"].items()
                                if scene == "OOT_TREASURE_SHOP"
                                and ootxmm_staticdata.OOTxMMCheckItems[name] != "OOT_HEART_PIECE"},
}

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

def fixed_checks(world: OOTxMM) -> set[str]:
    fixed = FIXED - FAIRY_LOCATIONS - TINGLE_LOCATIONS - set().union(*SPECIAL_KEY_LOCATIONS.values())
    for key, names in SPECIAL_KEY_LOCATIONS.items():
        if logic._value(world.ootmm_settings, key) == "vanilla":
            fixed |= names
    if logic._value(world.ootmm_settings, "ganonBossKey") == "vanilla":
        fixed.add("OOT Ganon Castle Boss Key")
    if logic._value(world.ootmm_settings, "tingleShuffle") == "vanilla":
        fixed |= TINGLE_LOCATIONS
    for key, names in FAIRY_SETTINGS.items():
        if logic._value(world.ootmm_settings, key) == "vanilla":
            fixed |= names
    return fixed


def place_fixed(world: OOTxMM) -> None:
    """The checks that keep their vanilla item (OoTMM's fixer, packages/logic/src/misc/fixer.ts)."""
    from .items import ITEM_BY_SYMBOLIC_ID, create_item_with_correct_classification
    fixed = fixed_checks(world)
    for location in world.multiworld.get_unfilled_locations(world.player):
        if location.name in fixed:
            vanilla = logic.shared_item(ootxmm_staticdata.OOTxMMCheckItems[location.name], world.ootmm_settings)
            location.place_locked_item(create_item_with_correct_classification(world, ITEM_BY_SYMBOLIC_ID[vanilla].display_name))

def starting_fairies(settings) -> Counter:
    """Native ROM grants from OoTMM's misc/config.ts, counted independently of AP deliveries."""
    return Counter(ootxmm_staticdata.OOTxMMCheckItems[name]
                   for key, names in FAIRY_SETTINGS.items()
                   if logic._value(settings, key) in ("starting", "removed")
                   for name in names)


def removed_item(world: OOTxMM, item: str) -> bool:
    """Items OoTMM takes out of the pool (run() in its world/transform.ts); their checks get filler."""
    return (item == "OOT_BOSS_KEY_GANON" and logic._value(world.ootmm_settings, "ganonBossKey") in ("removed", "custom")
            or item in TINGLE_ITEMS and logic._value(world.ootmm_settings, "tingleShuffle") in ("starting", "removed")
            or any(item in items and (logic._value(world.ootmm_settings, key) == "removed"
                                     or key == "mapCompassShuffle" and logic._value(world.ootmm_settings, key) == "starting")
                   for key, items in DUNGEON_SETTINGS.items()))

def _groups(world: OOTxMM) -> list[tuple[set[str], set[str]]]:
    """(OoTMM items, checks they must go to), in placing order."""
    # OoTMM places songs first. Here the rewards go first: 13 rewards for 13 bosses is the tighter fit, and
    # the songs then have 23 checks to spread over, which the greedy fill copes with far better.
    groups = []
    if logic._value(world.ootmm_settings, "dungeonRewardShuffle") == "dungeonBlueWarps":
        groups.append((REWARD_ITEMS, WARP_LOCATIONS))
    if logic._value(world.ootmm_settings, "songs") == "songLocations":
        groups.append((SONG_ITEMS, SONG_LOCATIONS))
    unrestricted = set().union(*(items for key, items in DUNGEON_SETTINGS.items()
                                 if logic._value(world.ootmm_settings, key) != ("ganon" if key == "ganonBossKey" else "ownDungeon")))
    return groups + [(items - unrestricted, locations) for items, locations in DUNGEON_GROUPS]

def _symbolic(item: Item) -> str:
    from .items import ITEM_BY_NAME
    return ITEM_BY_NAME[item.name].symbolic_id

def split_pool(world: OOTxMM, pool: list[Item]) -> list[Item]:
    """Keeps the items pre_fill places out of the pool (in world.pre_fill_pending), returns the rest."""
    restricted = set().union(*(items for items, _ in _groups(world)))
    if logic._value(world.ootmm_settings, "dungeonRewardShuffle") in ("dungeons", "dungeonsLimited"):
        restricted |= REWARD_ITEMS
    # A temple has one fairy item type, but chest and freestanding sources can have different rules.
    # Restrict only the copies contributed by ownDungeon sources, as OoTMM fixDungeon does.
    available = {location.name for location in world.multiworld.get_unfilled_locations(world.player)}
    fairy_counts = Counter(ootxmm_staticdata.OOTxMMCheckItems[name]
                           for key, names in FAIRY_SETTINGS.items()
                           if logic._value(world.ootmm_settings, key) == "ownDungeon"
                           for name in names & available)
    world.pre_fill_pending = []
    remaining = []
    for item in pool:
        symbolic = _symbolic(item)
        keep = symbolic in restricted
        if symbolic in FAIRY_ITEMS:
            keep = fairy_counts[symbolic] > 0
            if keep:
                fairy_counts[symbolic] -= 1
        (world.pre_fill_pending if keep else remaining).append(item)
    return remaining

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
                if location.item is not None:
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


def reward_locations(world: OOTxMM) -> set[str]:
    """OoTMM's eligible reward dungeons; Stone Tower includes its inverted layout."""
    names = set().union(*(set(_fill["dungeons"][dungeon]) for dungeon in _fill["rewardDungeons"]))
    names |= set(_fill["dungeons"]["IST"])
    if logic._value(world.ootmm_settings, "songs") == "songLocations":
        names -= SONG_LOCATIONS
    return names


def pre_fill_all(multiworld) -> None:
    """Retry local groups too when their placements leave no valid reward distribution."""
    worlds = list(multiworld.get_game_worlds("OOTxMM"))
    pending = {world.player: list(world.pre_fill_pending) for world in worlds}
    candidates = list(multiworld.get_unfilled_locations())
    reserve_limited_dungeons(multiworld)
    for attempt in range(ATTEMPTS):
        try:
            for world in worlds:
                pre_fill(world)
            place_dungeon_rewards(multiworld)
            return
        except FillError:
            for location in candidates:
                if location.item is not None:
                    location.item.location = None
                    location.item = None
                    location.locked = False
            for world in worlds:
                world.pre_fill_pending = list(pending[world.player])
            if attempt == ATTEMPTS - 1:
                raise


def reserve_limited_dungeons(multiworld) -> None:
    """A limited reward reserves its host dungeon against all other rewards, including main-fill items."""
    worlds = list(multiworld.get_game_worlds("OOTxMM"))
    limited = {world.player for world in worlds
               if logic._value(world.ootmm_settings, "dungeonRewardShuffle") == "dungeonsLimited"}
    if not limited:
        return
    for world in worlds:
        for dungeon in _fill["rewardDungeons"]:
            names = set(_fill["dungeons"][dungeon])
            if dungeon == "ST":
                names |= set(_fill["dungeons"]["IST"])
            locations = [location for location in multiworld.get_locations(world.player)
                         if location.name in names]
            for location in locations:
                original = location.item_rule

                def reward_rule(item, original=original, locations=locations, location=location):
                    if not original(item):
                        return False
                    if item.game != "OOTxMM" or _symbolic(item) not in REWARD_ITEMS:
                        return True
                    return not any(other is not location and other.item is not None
                                   and other.item.game == "OOTxMM"
                                   and _symbolic(other.item) in REWARD_ITEMS
                                   and (item.player in limited or other.item.player in limited)
                                   for other in locations)

                location.item_rule = reward_rule


def place_dungeon_rewards(multiworld) -> None:
    """Fill dungeon-only rewards across OoTMM players after their local pre-fills."""
    worlds = list(multiworld.get_game_worlds("OOTxMM"))
    owners = [world for world in worlds
              if logic._value(world.ootmm_settings, "dungeonRewardShuffle") in ("dungeons", "dungeonsLimited")]
    pending = {world.player: list(world.pre_fill_pending) for world in owners}
    if not any(pending.values()):
        return
    eligible = {world.player: reward_locations(world) for world in worlds}
    candidates = [location for location in multiworld.get_unfilled_locations()
                  if location.player in eligible and location.name in eligible[location.player]]
    for attempt in range(ATTEMPTS):
        group = [item for items in pending.values() for item in items]
        for world in owners:
            world.pre_fill_pending = []
        locations = list(candidates)
        multiworld.random.shuffle(locations)
        multiworld.random.shuffle(group)
        try:
            fill_restrictive(multiworld, multiworld.get_all_state(), locations, group,
                             lock=True, allow_excluded=True, name="OOTxMM dungeon rewards")
            return
        except FillError:
            for location in candidates:
                if location.item is not None:
                    location.item.location = None
                    location.item = None
                    location.locked = False
            for world in owners:
                world.pre_fill_pending = list(pending[world.player])
            if attempt == ATTEMPTS - 1:
                raise
