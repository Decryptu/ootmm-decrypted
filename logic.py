"""The world graph with OoTMM's conditions, built per player's settings from raw/GreatLogicJSONdump.json.

OoTMM explores every area once per age, so each region exists as a child and an adult copy, and each
condition is specialized to the copy's age and the player's settings and tricks. A condition on an item the
pool never holds, or on an event nothing can trigger, is false, as it is for OoTMM. Checks the settings leave
out (removed_checks) don't exist. Copies no exit can reach
with every pool item, and exits, checks and events whose condition is then false, are left out.
"""
from __future__ import annotations

from typing import Any, Union

from . import ootxmm_staticdata

AGES = ("child", "adult")
TRAVERSAL_SETTINGS = {"ageChange"}
AGE_CHANGE_EVENT = "OOT_TIME_TRAVEL_AT_WILL"
ORIGIN = "OOT SPAWN"

# Items OoTMM adds to the pool on top of the checks' vanilla items (EXTRA_ITEMS_OOT and EXTRA_ITEMS_MM in
# packages/logic/src/world/transform.ts): their vanilla sources are not checks.
EXTRA_ITEMS = [
    "OOT_MASK_SKULL", "OOT_MASK_SPOOKY", "OOT_MASK_GERUDO", "OOT_MASK_KEATON",
    "OOT_MASK_TRUTH", "OOT_MASK_BUNNY", "OOT_MASK_GORON", "OOT_MASK_ZORA",
    "MM_MASK_DEKU", "MM_SWORD",
]

OPTIONAL_ITEM_SETTINGS = ootxmm_staticdata.OOTxMMFill["optionalItems"]
SOUL_SETTINGS = {key: group for key, group in OPTIONAL_ITEM_SETTINGS.items() if key.startswith("souls")}
SHARED_ITEM_SETTINGS = ootxmm_staticdata.OOTxMMFill["sharedItems"]
SHARED_SOUL_SETTINGS = {key: defs for key, defs in SHARED_ITEM_SETTINGS.items() if key.startswith("sharedSouls")}

POOL_TRANSFORMS = ootxmm_staticdata.OOTxMMFill["poolTransforms"]
CROSS_GAME_SONGS = ootxmm_staticdata.OOTxMMFill["crossGameSongs"]
CROSS_GAME_ITEMS = CROSS_GAME_SONGS | ootxmm_staticdata.OOTxMMFill["crossGameEquipment"]
LULLABY_SETTINGS = {"songGoronOot", "sharedSongGoron", "progressiveGoronLullabyOot", "progressiveGoronLullabyMm"}

POOL_SETTINGS = {"skeletonKeyOot": "OOT_SKELETON_KEY", "skeletonKeyMm": "MM_SKELETON_KEY"}


def normalize_shared_items(settings: Settings) -> Settings:
    """OoTMM enables sharing only when both games' corresponding items are enabled."""
    settings = dict(settings)
    for key in SHARED_SOUL_SETTINGS:
        family = key.removeprefix("sharedSouls")
        settings[key] = bool(_value(settings, key) and _value(settings, f"souls{family}Oot")
                             and _value(settings, f"souls{family}Mm"))
    settings["sharedSkeletonKey"] = bool(_value(settings, "sharedSkeletonKey")
                                         and _value(settings, "skeletonKeyOot")
                                         and _value(settings, "skeletonKeyMm"))
    settings["sharedOcarinaButtons"] = bool(_value(settings, "sharedOcarinaButtons")
                                           and _value(settings, "ocarinaButtonsShuffleOot")
                                           and _value(settings, "ocarinaButtonsShuffleMm"))
    for key, (enable, _) in CROSS_GAME_ITEMS.items():
        settings[key] = bool(_value(settings, key) and _value(settings, enable))
    settings["sharedSongGoron"] = bool(_value(settings, "sharedSongGoron") and _value(settings, "songGoronOot")
                                      and _value(settings, "progressiveGoronLullabyOot")
                                      == _value(settings, "progressiveGoronLullabyMm"))
    return settings


def extra_items(settings: Settings) -> list[str]:
    """Base additions and optional items from OoTMM's world/transform.ts."""
    settings = normalize_shared_items(settings)
    additions = (EXTRA_ITEMS + [item for key, item in POOL_SETTINGS.items() if _value(settings, key)]
            + [item for key, group in OPTIONAL_ITEM_SETTINGS.items() if _value(settings, key)
               and not any(enable == key and _value(settings, shared)
                           for shared, (enable, _) in CROSS_GAME_ITEMS.items()) for item in group])
    # OoTMM shareItems(..., 'max'): these optional items have at most one copy per game.
    present = set(additions)
    if _value(settings, "songGoronOot") and not _value(settings, "sharedSongGoron"):
        present.update(("OOT_SONG_GORON", "OOT_SONG_GORON_HALF"))
    for key, definitions in SHARED_ITEM_SETTINGS.items():
        if not _value(settings, key):
            continue
        for definition in definitions:
            originals = {definition["oot"], definition["mm"]}
            if present & originals:
                present.difference_update(originals)
                present.add(definition["shared"])
    return sorted(present)


# OoTMM world/transform.ts keyRing: collapse all copies to one ring, except vanilla special keys.
KEY_RING_SETTINGS = {
    "smallKeyRingOot": {name: f"OOT_SMALL_KEY_{suffix}" for name, suffix in (
        ("Forest", "FOREST"), ("Fire", "FIRE"), ("Water", "WATER"), ("Spirit", "SPIRIT"),
        ("Shadow", "SHADOW"), ("BotW", "BOTW"), ("GTG", "GTG"), ("Ganon", "GANON"),
        ("GF", "GF"), ("TCG", "TCG"))},
    "smallKeyRingMm": {name: f"MM_SMALL_KEY_{name}" for name in ("WF", "SH", "GB", "ST")},
}


def key_rings(settings: Settings) -> dict[str, str]:
    selected = {item: item.replace("SMALL_KEY", "KEY_RING")
                for key, members in KEY_RING_SETTINGS.items() for name, item in members.items()
                if _set_has(_value(settings, key), name)}
    for suffix, key in (("GF", "smallKeyShuffleHideout"), ("TCG", "smallKeyShuffleChestGame")):
        if _value(settings, key) == "vanilla":
            selected.pop(f"OOT_SMALL_KEY_{suffix}", None)
    return selected


def transform_pool(items, settings: Settings):
    """Apply OoTMM's ordered sharing replacements, copy reductions and Lullaby modes."""
    from collections import Counter
    settings = normalize_shared_items(settings)
    pool = Counter(items)
    for key, operations in POOL_TRANSFORMS.items():
        if not _value(settings, key):
            continue
        for op, source, target in operations:
            if op == "replaceItem":
                count = pool.pop(source, 0)
                if count:
                    pool[target] += count
            elif op == "removeItem":
                pool[source] = max(0, pool[source] - target)
            elif op == "divideItem":
                pool[source] //= target
            else:
                raise ValueError(f"Unknown pool operation: {op}")
    def replace(source, target):
        count = pool.pop(source, 0)
        if count:
            pool[target] += count
    if _value(settings, "sharedSongGoron"):
        for suffix in ("GORON", "GORON_HALF"):
            replace("MM_SONG_" + suffix, "SHARED_SONG_" + suffix)
        games = ("SHARED",)
    else:
        games = ("OOT", "MM")
    for game in games:
        full, half = game + "_SONG_GORON", game + "_SONG_GORON_HALF"
        mode_game = "Mm" if game in ("MM", "SHARED") else "Oot"
        if _value(settings, "progressiveGoronLullaby" + mode_game) == "progressive":
            replace(full, half)
        else:
            pool.pop(half, None)
    return +pool


def shared_item(item: str, settings: Settings) -> str:
    # Fixed pickups also use the transformed vanilla item, without pool copy reductions.
    for key, operations in POOL_TRANSFORMS.items():
        if _value(settings, key):
            for op, source, target in operations:
                if op == "replaceItem" and item == source:
                    item = target
    if item in ("OOT_SONG_GORON", "MM_SONG_GORON", "OOT_SONG_GORON_HALF", "MM_SONG_GORON_HALF"):
        settings = normalize_shared_items(settings)
        game, suffix = item.split("_", 1)
        if game == "MM" and _value(settings, "sharedSongGoron"):
            game = "SHARED"
        mode_game = "Mm" if game in ("MM", "SHARED") else "Oot"
        if suffix == "SONG_GORON" and _value(settings, "progressiveGoronLullaby" + mode_game) == "progressive":
            suffix += "_HALF"
        item = game + "_" + suffix
    return item


def pool_items(items, settings: Settings) -> set[str]:
    rings = key_rings(settings)
    return {rings.get(item, item) for item in transform_pool([*items, *extra_items(settings)], settings)}


# A condition is True, False, or a tuple: ("item", OoTMM item ID, count), ("event", event),
# ("unique", item IDs, count), ("and", conditions), ("or", conditions),
# ("time-oot" or "time-mm", allowed mask), or ("flag-on" or "flag-off", flag index).
Condition = Union[bool, tuple]

# Settings are OoTMM's: {setting key: value, "tricks": [trick keys]}.
Settings = dict[str, Any]

_nodes = ootxmm_staticdata.OOTxMMLogic["nodes"]
_areas = ootxmm_staticdata.OOTxMMLogic["areas"]
_check_info = ootxmm_staticdata.OOTxMMCheckInfo

# The check filters of run() in OoTMM's packages/logic/src/world/transform.ts (filterChecks*): setting key ->
# the check type it shuffles in its game. A setting is a toggle or none, all, overworld or dungeons.
CHECK_FILTERS = {
    "shufflePotsOot": "pot", "shufflePotsMm": "pot", "shuffleCratesOot": "crate", "shuffleCratesMm": "crate",
    "shuffleBarrelsMm": "barrel", "pondFishShuffle": "fish",
    "shuffleFreeRupeesOot": "rupee", "shuffleFreeRupeesMm": "rupee",
    "shuffleFreeHeartsOot": "heart", "shuffleFreeHeartsMm": "heart",
    "shuffleHivesOot": "hive", "shuffleHivesMm": "hive", "shuffleGrassOot": "grass", "shuffleGrassMm": "grass",
    "shuffleRocksOot": "rock", "shuffleRocksMm": "rock", "shuffleTreesOot": "tree", "shuffleTreesMm": "tree",
    "shuffleBushOot": "bush", "shuffleBushMm": "bush", "shuffleSoilOot": "soil", "shuffleSoilMm": "soil",
    "shuffleGossipFairiesOot": "gossip", "shuffleGossipBigFairiesOot": "gossip-big",
    "shuffleGossipFairiesMm": "gossip", "shuffleGossipBigFairiesMm": "gossip-big",
    "shuffleWonderItemsOot": "wonder", "shuffleWonderItemsMm": "wonder",
    "shuffleButterfliesOot": "butterfly", "shuffleButterfliesMm": "butterfly",
    "shuffleBouldersOot": "boulder", "shuffleBouldersMm": "boulder",
    "shuffleRedBouldersOot": "boulder-red", "shuffleRedBouldersMm": "boulder-red",
    "shuffleSilverBouldersOot": "boulder-silver", "shuffleSnowballsMm": "snowball",
    "shuffleIciclesOot": "icicle", "shuffleIciclesMm": "icicle", "shuffleRedIceOot": "redice",
    "fairyFountainFairyShuffleOot": "fairy", "fairyFountainFairyShuffleMm": "fairy",
    "fairySpotShuffleOot": "fairy-spot",
}

# The check settings removed_checks follows: test/test_checks.py checks that every setting raw/Meta_Options.py
# lists as ported (PORTED_SETTINGS in options.py) is one. A setting the world doesn't offer keeps OoTMM's default.
CHECK_SETTINGS = [
    *CHECK_FILTERS, "restoreBrokenActors", "shuffleMaskTrades", "divingGameRupeeShuffle",
    "shuffleSkulltulaFinalReward", "shuffleTFGrassMm", "eggShuffle",
]

def _value(settings: Settings, key: str) -> Any:
    # Settings the world doesn't offer keep OoTMM's default.
    return settings[key] if key in settings else ootxmm_staticdata.OOTxMMSettingDefaults[key]

def _set_has(value: Any, member: str) -> bool:
    # An offered set setting is a list; OoTMM's default is {type: all, none or specific, values}.
    if isinstance(value, dict):
        return value.get("type") == "all" or member in value.get("values", [])
    return member in value

def removed_checks(settings: Settings) -> set[str]:
    """The checks OoTMM leaves out with these settings, as run() in its world/transform.ts removes them."""
    removed: set[str] = set()
    if _value(settings, "strayFairyOtherShuffle") == "removed":
        removed.update(ootxmm_staticdata.OOTxMMFill["fairyLocations"]["strayFairyOtherShuffle"])
    def checks(type_: str, scene: str | None = None) -> list[str]:
        return [name for name, (t, s, _) in _check_info["checks"].items() if t == type_ and scene in (None, s)]
    for key, type_ in CHECK_FILTERS.items():
        value = _value(settings, key)
        prefix = "MM " if key.endswith("Mm") else "OOT "
        for name in checks(type_):
            in_dungeon = _check_info["checks"][name][2]
            if name.startswith(prefix) and (value in (False, "none") or (value == "overworld" and in_dungeon)
                                            or (value == "dungeons" and not in_dungeon)):
                removed.add(name)
    if not _value(settings, "restoreBrokenActors"):
        removed.update(_check_info["brokenActors"])
    if not _value(settings, "shuffleMaskTrades"):
        removed.update(_check_info["sellMasks"])
    if _value(settings, "goal") in ("triforce", "triforce3"):
        removed.update(checks("pot", "OOT_GANON_TOWER") + checks("pot", "MM_LAIR_MAJORA"))
    if not _value(settings, "shuffleTFGrassMm"):
        removed.update(checks("grass", "MM_TERMINA_FIELD"))
    # Water rocks need the Iron Boots and the Blast Mask at one age.
    blast = (_value(settings, "mmAgeReqChildMaskBlast"), _value(settings, "mmAgeReqAdultMaskBlast"))
    boots = (_value(settings, "mmAgeReqChildBootsIron"), _value(settings, "mmAgeReqAdultBootsIron"))
    if not _value(settings, "bootsIronMm") or (blast[0] and boots[1]) or (blast[1] and boots[0]):
        removed.update(_check_info["mmWaterRocks"])
    if not _value(settings, "stoneMaskOot"):
        removed.add("OOT Hyrule Castle Tree Guarded")
    if (_value(settings, "logic") == "allLocations" and "MM_GORON_BOMB_JUMP" not in _value(settings, "tricks")
            and _value(settings, "hookshotAnywhereMm") != "logical"):
        removed.update(checks("tree", "MM_GORMAN_TRACK"))
    if not _value(settings, "agelessStrength") or _set_has(_value(settings, "openDungeonsOot"), "fireChild"):
        removed.update(f"OOT Death Mountain Crater Silver Boulder {i}" for i in (1, 2, 3))
    if not _value(settings, "divingGameRupeeShuffle"):
        removed.update(f"OOT Zora Domain Diving Game {color} Rupee" for color in ("Green", "Blue", "Red", "Purple", "Huge"))
    if not _value(settings, "shuffleSkulltulaFinalReward"):
        removed.add("OOT Skulltula House 100 Tokens")
    if not _value(settings, "eggShuffle"):
        removed.update(("OOT Hatch Chicken", "OOT Hatch Pocket Cucco"))
    return removed

class _Specializer:
    """Conditions specialized to an age and the settings, with the items and events that can't happen folded to false."""
    def __init__(self, settings: Settings, items: set[str], events: set[str] | None):
        self.settings = settings
        self.tricks = set(settings["tricks"])
        self.items = items
        self.events = events  # None: every event is still possible
        self.memo: dict[tuple[int, str], Condition] = {}

    def __call__(self, node_id: int, age: str) -> Condition:
        key = (node_id, age)
        if key not in self.memo:
            self.memo[key] = self.build(_nodes[node_id], age)
        return self.memo[key]

    def build(self, node, age: str) -> Condition:
        if isinstance(node, bool):
            return node
        if node[0] == "age":
            return node[1] == age
        if node[0] == "price":
            return self.settings.get("_prices", ootxmm_staticdata.OOTxMMLogic["prices"])[node[1]] <= node[2]
        if node[0] in ("time-oot", "time-mm", "flag-on", "flag-off"):
            return tuple(node)
        if node[0] == "setting":
            # setting(key) for a toggle, setting(key, value) for the others.
            value = self.settings[node[1]]
            return bool(value) if node[2] is None else (_set_has(value, node[2]) if node[1] in KEY_RING_SETTINGS else value == node[2])
        if node[0] == "trick":
            return node[1] in self.tricks
        if node[0] == "not":
            # Only settings and tricks are negated, so the child is already true or false.
            return not self(node[1], age)
        if node[0] == "item":
            return node[1] in self.items and ("item", node[1], node[2])
        if node[0] == "event":
            return (self.events is None or node[1] in self.events) and ("event", node[1])
        if node[0] == "count_unique":
            possible = tuple(i for i in node[1] if i in self.items)
            return len(possible) >= node[2] and ("unique", possible, node[2])
        is_and = node[0] == "and"
        children = []
        for child in (self(c, age) for c in node[1]):
            if child is (not is_and):
                return child
            if child is not is_and and child not in children:
                children.append(child)
        if not children:
            return is_and
        return children[0] if len(children) == 1 else (node[0], tuple(children))

def _met(cond: Condition, events: set[str]) -> bool:
    # With every pool item: only events can still be missing.
    if isinstance(cond, bool):
        return cond
    if cond[0] == "event":
        return cond[1] in events
    if cond[0] == "and":
        return all(_met(c, events) for c in cond[1])
    if cond[0] == "or":
        return any(_met(c, events) for c in cond[1])
    return True

def region_name(area: str, age: str) -> str:
    return f"{area} ({age.capitalize()})"


def can_change_age(area: str) -> bool:
    return _areas[area]["game"] == "oot" and _areas[area].get("age_change", False)

def _explore(specialize: _Specializer):
    """Regions and events reachable from the spawn with every pool item."""
    areas = ootxmm_staticdata.OOTxMMRegionData.keys()
    # Both ages start at the spawn, as in OoTMM's pathfinder.
    regions = {(ORIGIN, age) for age in AGES}
    events: set[str] = set()
    changed = True
    while changed:
        changed = False
        for area, age in list(regions):
            other = (area, "adult" if age == "child" else "child")
            if AGE_CHANGE_EVENT in events and can_change_age(area) and other not in regions:
                regions.add(other)
                changed = True
            for target, node in _areas[area]["exits"].items():
                if target in areas and (target, age) not in regions and _met(specialize(node, age), events):
                    regions.add((target, age))
                    changed = True
            for event, node in _areas[area]["events"].items():
                if event not in events and _met(specialize(node, age), events):
                    events.add(event)
                    changed = True
    return regions, events

def _items(cond: Condition, found: set[str]) -> None:
    if not isinstance(cond, tuple):
        return
    if cond[0] == "item":
        found.add(cond[1])
    elif cond[0] == "unique":
        found.update(cond[1])
    elif cond[0] in ("and", "or"):
        for child in cond[1]:
            _items(child, found)

class Logic:
    """The graph for one set of settings.

    exits: (area, age) -> [(target area, condition)], for every region copy that exists.
    checks, events: name -> [(area, age, condition)]: the parents a check or event can be reached from.
    items: the OoTMM item IDs some condition asks for, which are the progression items.
    """
    def __init__(self, settings: Settings, removed: set[str]):
        # Start from every check's item and drop those whose check turns out unreachable, until it settles.
        items = pool_items((item for name, item in ootxmm_staticdata.OOTxMMCheckItems.items() if name not in removed), settings)
        while True:
            regions, events = _explore(_Specializer(settings, items, None))
            specialize = _Specializer(settings, items, events)
            exits = {
                (area, age): [
                    (target, cond) for target, node in _areas[area]["exits"].items()
                    if (target, age) in regions and (cond := specialize(node, age)) is not False
                ]
                for area, age in sorted(regions)
            }
            checks: dict[str, list[tuple[str, str, Condition]]] = {}
            event_parents: dict[str, list[tuple[str, str, Condition]]] = {}
            for area, age in sorted(regions):
                for kind, targets in (("locations", checks), ("events", event_parents)):
                    for name, node in _areas[area][kind].items():
                        if kind == "locations" and name in removed:
                            continue
                        if (cond := specialize(node, age)) is not False:
                            targets.setdefault(name, []).append((area, age, cond))
            # The pool is the vanilla items of the checks that exist, so it depends on which can be reached.
            pool = pool_items((ootxmm_staticdata.OOTxMMCheckItems[name] for name in checks), settings)
            if pool == items:
                break
            items = pool
        # Check filters can leave empty terminal areas, including time-limited subareas
        # reachable at only one age. They cannot contribute checks, events or a return route.
        occupied = {(area, age) for parents in (*checks.values(), *event_parents.values())
                    for area, age, _ in parents}
        age_changes = {key for key in exits if can_change_age(key[0])
                       and (key[0], "adult" if key[1] == "child" else "child") in exits
                       and AGE_CHANGE_EVENT in event_parents}
        occupied.update(age_changes)
        while empty := {key for key, targets in exits.items() if not targets and key not in occupied
                       and key[0] != ORIGIN}:
            exits = {key: [(target, cond) for target, cond in targets if (target, key[1]) not in empty]
                     for key, targets in exits.items() if key not in empty}
        self.exits = exits
        self.age_changes = age_changes
        self.regions = list(exits)
        self.checks = checks
        self.events = event_parents
        self.stay = {
            (area, age): None if _areas[area]["stay"] is None else tuple(specialize(n, age) for n in _areas[area]["stay"])
            for area, age in self.regions
        }
        self.items: set[str] = set()
        for targets in exits.values():
            for _, cond in targets:
                _items(cond, self.items)
        for parents in (*checks.values(), *event_parents.values()):
            for _, _, cond in parents:
                _items(cond, self.items)
        for conditions in self.stay.values():
            for cond in conditions or ():
                _items(cond, self.items)

# Conditions and optional pool items both change the specialized graph.
LOGIC_SETTINGS = sorted({node[1] for node in _nodes if isinstance(node, list) and node[0] == "setting"} | set(POOL_TRANSFORMS) | set(POOL_SETTINGS) | set(OPTIONAL_ITEM_SETTINGS) | set(SHARED_ITEM_SETTINGS) | set(KEY_RING_SETTINGS) | LULLABY_SETTINGS | {"smallKeyShuffleHideout"})

_cache: dict[tuple, Logic] = {}

def build(settings: Settings) -> Logic:
    """The graph for these settings. Players with the same logic settings, tricks and checks share one."""
    settings = normalize_shared_items(settings)
    removed = removed_checks(settings)
    key = (tuple(settings.get("_prices", ootxmm_staticdata.OOTxMMLogic["prices"])), tuple(tuple(name for name in KEY_RING_SETTINGS[k] if _set_has(_value(settings, k), name))
                 if k in KEY_RING_SETTINGS else _value(settings, k) for k in LOGIC_SETTINGS), tuple(sorted(settings["tricks"])), frozenset(removed))
    if key not in _cache:
        _cache[key] = Logic(settings, removed)
    return _cache[key]
