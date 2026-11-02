"""The world graph with OoTMM's conditions, built once at import from raw/GreatLogicJSONdump.json.

OoTMM explores every area once per age, so each region exists as a child and an adult copy, and each
condition is specialized to the copy's age. A condition on an item the pool never holds, or on an event
nothing can trigger, is false, as it is for OoTMM. Copies no exit can reach with every pool item, and
exits, checks and events whose condition is then false, are left out.
"""
from __future__ import annotations

from typing import Union

from . import ootxmm_staticdata

AGES = ("child", "adult")
ORIGIN = "OOT SPAWN"

# Items OoTMM adds to the pool on top of the checks' vanilla items (EXTRA_ITEMS_OOT and EXTRA_ITEMS_MM in
# packages/logic/src/world/transform.ts): their vanilla sources are not checks.
EXTRA_ITEMS = [
    "OOT_MASK_SKULL", "OOT_MASK_SPOOKY", "OOT_MASK_GERUDO", "OOT_MASK_KEATON",
    "OOT_MASK_TRUTH", "OOT_MASK_BUNNY", "OOT_MASK_GORON", "OOT_MASK_ZORA",
    "MM_MASK_DEKU", "MM_SWORD",
]

# A condition is True, False, or a tuple: ("item", OoTMM item ID, count), ("event", event),
# ("unique", item IDs, count), ("and", conditions) or ("or", conditions).
Condition = Union[bool, tuple]

_nodes = ootxmm_staticdata.OOTxMMLogic["nodes"]
_areas = ootxmm_staticdata.OOTxMMLogic["areas"]

class _Specializer:
    """Conditions specialized to an age, with the items and events that can't happen folded to false."""
    def __init__(self, items: set[str], events: set[str] | None):
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
            for target, node in _areas[area]["exits"].items():
                if target in areas and (target, age) not in regions and _met(specialize(node, age), events):
                    regions.add((target, age))
                    changed = True
            for event, node in _areas[area]["events"].items():
                if event not in events and _met(specialize(node, age), events):
                    events.add(event)
                    changed = True
    return regions, events

def _build():
    # Start from every check's item and drop those whose check turns out unreachable, until it settles.
    items = set(ootxmm_staticdata.OOTxMMCheckItems.values()) | set(EXTRA_ITEMS)
    while True:
        regions, events = _explore(_Specializer(items, None))
        specialize = _Specializer(items, events)
        exits = {
            (area, age): [
                (target, cond) for target, node in _areas[area]["exits"].items()
                if (target, age) in regions and (cond := specialize(node, age)) is not False
            ]
            for area, age in sorted(regions)
        }
        # Checks and events can be reached from several regions: name -> [(area, age, condition)].
        checks: dict[str, list[tuple[str, str, Condition]]] = {}
        event_parents: dict[str, list[tuple[str, str, Condition]]] = {}
        for area, age in sorted(regions):
            for kind, targets in (("locations", checks), ("events", event_parents)):
                for name, node in _areas[area][kind].items():
                    if (cond := specialize(node, age)) is not False:
                        targets.setdefault(name, []).append((area, age, cond))
        # The pool is the vanilla items of the checks that exist, so it depends on which can be reached.
        pool = {ootxmm_staticdata.OOTxMMCheckItems[name] for name in checks} | set(EXTRA_ITEMS)
        if pool == items:
            return exits, checks, event_parents
        items = pool

EXITS, CHECKS, EVENTS = _build()
REGIONS = list(EXITS)

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

def _logic_items() -> set[str]:
    found: set[str] = set()
    for targets in EXITS.values():
        for _, cond in targets:
            _items(cond, found)
    for parents in (*CHECKS.values(), *EVENTS.values()):
        for _, _, cond in parents:
            _items(cond, found)
    return found

# The OoTMM item IDs some condition asks for: these are the progression items.
LOGIC_ITEMS = _logic_items()
