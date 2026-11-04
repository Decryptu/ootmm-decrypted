"""Per-area clock ranges and constraints, following OoTMM's pathfinder and expression evaluator."""
from collections import Counter, OrderedDict, deque
from weakref import WeakKeyDictionary

from . import logic, ootxmm_staticdata
from .items import ITEM_BY_SYMBOLIC_ID

OOT_ALL = ootxmm_staticdata.OOTxMMLogic["ootTimeAll"]
MM_SLICES = len(ootxmm_staticdata.OOTxMMLogic["mmTimeSlices"])
MM_ALL = (1 << MM_SLICES) - 1
# Area data: OoT times, MM times, required-on flags, required-off flags.
INITIAL = (0, 1, 0, 0)


def evaluate(cond, data, counts):
    """Return the allowed clock masks and required flags, or None if the condition fails.

    Like OoTMM, OR merges successful alternatives and AND intersects their time ranges.
    Flags represent constraints on the route, not inventory events.
    """
    if isinstance(cond, bool):
        return (OOT_ALL, MM_ALL, 0, 0) if cond else None
    kind = cond[0]
    if kind == "time-oot":
        return (cond[1], MM_ALL, 0, 0) if data[0] & cond[1] else None
    if kind == "time-mm":
        return (OOT_ALL, cond[1], 0, 0) if data[1] & cond[1] else None
    if kind in ("flag-on", "flag-off"):
        bit = 1 << cond[1]
        on = kind == "flag-on"
        if data[3 if on else 2] & bit:
            return None
        return (OOT_ALL, MM_ALL, bit if on else 0, 0 if on else bit)
    if kind == "item":
        met = counts[ITEM_BY_SYMBOLIC_ID[cond[1]].display_name] >= cond[2]
    elif kind == "event":
        met = bool(counts[cond[1]])
    elif kind == "unique":
        met = sum(bool(counts[ITEM_BY_SYMBOLIC_ID[i].display_name]) for i in cond[1]) >= cond[2]
    else:
        is_and = kind == "and"
        result = (OOT_ALL, MM_ALL, 0, 0) if is_and else (0, 0, -1, -1)
        found = False
        for child in cond[1]:
            value = evaluate(child, data, counts)
            if value is None:
                if is_and:
                    return None
                continue
            found = True
            a, b, c, d = result
            x, y, z, w = value
            result = (a & x, b & y, c | z, d | w) if is_and else (a | x, b | y, c & z, d & w)
        if not found or not result[0] or not result[1] or result[2] & result[3]:
            return None
        return result
    return (OOT_ALL, MM_ALL, 0, 0) if met else None


def merge(a, b):
    return (a[0] | b[0], a[1] | b[1], a[2] & b[2], a[3] & b[3])


class TimeLogic:
    def __init__(self, graph, player, starting=None):
        self.starting = Counter(starting or {})
        self.graph = graph
        self.player = player
        self.cache = WeakKeyDictionary()
        self.inventories = OrderedDict()
        self.last_inventory = None
        self.last_result = None
        self.events = set(getattr(graph, "events", {}))
        self.events_by_area = {}
        for event, parents in getattr(graph, "events", {}).items():
            for area, age, cond in parents:
                self.events_by_area.setdefault((area, age), []).append((event, cond))
        self.dependencies = {}
        def track(cond, key):
            if isinstance(cond, tuple):
                if cond[0] == "event":
                    self.dependencies.setdefault(cond[1], set()).add(key)
                elif cond[0] == "item":
                    self.dependencies.setdefault(ITEM_BY_SYMBOLIC_ID[cond[1]].display_name, set()).add(key)
                elif cond[0] == "unique":
                    for item in cond[1]:
                        self.dependencies.setdefault(ITEM_BY_SYMBOLIC_ID[item].display_name, set()).add(key)
                elif cond[0] in ("and", "or"):
                    for child in cond[1]:
                        track(child, key)
        for key, exits in graph.exits.items():
            for _, cond in exits:
                track(cond, key)
            for _, cond in self.events_by_area.get(key, ()):
                track(cond, key)
            for cond in graph.stay[key] or ():
                track(cond, key)

    def expand(self, key, data, counts):
        area = logic._areas[key[0]]
        oot, mm, on, off = data
        if area["game"] == "oot":
            oot |= {"day": 1, "night": 2, "flow": OOT_ALL, "still": 0}[area["time"]]
        else:
            if not mm:
                return None
            stay = self.graph.stay[key]
            if stay is None:
                mm |= MM_ALL ^ ((mm & -mm) - 1)
            else:
                waiting = False
                for i, cond in enumerate(stay):
                    if mm & (1 << i):
                        waiting = True
                    elif waiting:
                        waiting = evaluate(cond, (oot, mm, on, off), counts) is not None
                        if waiting:
                            mm |= 1 << i
        return (oot, mm, on, off)

    def explore(self, counts):
        return self.solve(counts)[0]

    def solve(self, counts, previous=None):
        # Derive events together with the clock ranges, rather than relying on AP's
        # separate event sweep to repeatedly restart the same traversal.
        inventory = counts
        counts = counts.copy()
        counts.update(self.starting)
        incremental = previous is not None and inventory >= previous[0]
        if incremental:
            counts.update({event: count for event, count in previous[1][1].items() if event in self.events})
        prepared = {}
        def prepare(cond):
            if isinstance(cond, bool):
                return cond
            if cond in prepared:
                return prepared[cond]
            kind = cond[0]
            result = cond
            if kind in ("item", "unique"):
                result = evaluate(cond, INITIAL, counts) is not None
            elif kind in ("and", "or"):
                is_and = kind == "and"
                children = []
                for child in cond[1]:
                    value = prepare(child)
                    if value is not is_and:
                        if value is (not is_and):
                            result = value
                            break
                        children.append(value)
                else:
                    result = is_and if not children else children[0] if len(children) == 1 else (kind, tuple(children))
            prepared[cond] = result
            return result
        reached = previous[1][0].copy() if incremental else {}
        queue = deque()
        queued = set()

        def enqueue(key):
            if key not in queued:
                queued.add(key)
                queue.append(key)

        def enter(key, data):
            old = reached.get(key)
            value = self.expand(key, merge(old, data) if old is not None else data, counts)
            if value is not None and value != old:
                reached[key] = value
                enqueue(key)

        if incremental:
            for name, count in inventory.items():
                if count != previous[0][name]:
                    for dependent in self.dependencies.get(name, ()):
                        if dependent in reached:
                            enqueue(dependent)
        else:
            for age in logic.AGES:
                enter((logic.ORIGIN, age), INITIAL)
        while queue:
            key = queue.popleft()
            queued.remove(key)
            expanded = self.expand(key, reached[key], counts)
            reached[key] = expanded
            data = reached[key]
            for event, cond in self.events_by_area.get(key, ()):
                if not counts[event] and evaluate(prepare(cond), data, counts) is not None:
                    counts[event] = 1
                    for dependent in self.dependencies.get(event, ()):
                        if dependent in reached:
                            enqueue(dependent)
            for target, cond in self.graph.exits[key]:
                allowed = evaluate(prepare(cond), data, counts)
                if allowed is None:
                    continue
                oot, mm, on, off = allowed
                value = (data[0] & oot, data[1] & mm, data[2] | on, data[3] | off)
                if logic._areas[key[0]]["game"] == "oot" and logic._areas[target]["game"] == "mm":
                    value = (value[0], value[1] | 1, value[2], value[3])
                enter((target, key[1]), value)
        return reached, counts

    def rule(self, area, age, cond):
        key = (area, age)
        def access(state):
            counts = Counter({name: count for name, count in state.prog_items[self.player].items()
                              if count and name not in self.events})
            cached = self.cache.get(state)
            if cached is None or cached[0] != counts:
                inventory = frozenset(counts.items())
                result = self.inventories.get(inventory)
                if result is None:
                    previous = None if self.last_inventory is None else (self.last_inventory, self.last_result)
                    result = self.solve(counts, previous)
                    self.inventories[inventory] = result
                    if len(self.inventories) > 16:
                        self.inventories.popitem(last=False)
                else:
                    self.inventories.move_to_end(inventory)
                self.last_inventory, self.last_result = counts, result
                reached, derived = result
                cached = (counts, reached, derived)
                self.cache[state] = cached
            data = cached[1].get(key)
            return data is not None and evaluate(cond, data, cached[2]) is not None
        return access
