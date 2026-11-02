from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from BaseClasses import CollectionState

from .items import ITEM_BY_SYMBOLIC_ID
from .logic import Condition

if TYPE_CHECKING:
    from .world import OOTxMM

Rule = Callable[[CollectionState], bool]

def compile_rule(world: OOTxMM, cond: Condition, cache: dict) -> Rule | None:
    """Turn a condition from logic.py into an access rule. None means always met."""
    if cond is True:
        return None
    if cond in cache:
        return cache[cond]
    player = world.player
    rule: Rule
    if cond is False:
        rule = lambda state: False
    elif cond[0] == "item":
        name, count = ITEM_BY_SYMBOLIC_ID[cond[1]].display_name, cond[2]
        rule = lambda state: state.has(name, player, count)
    elif cond[0] == "event":
        event = cond[1]
        rule = lambda state: state.has(event, player)
    elif cond[0] == "unique":
        names, count = [ITEM_BY_SYMBOLIC_ID[i].display_name for i in cond[1]], cond[2]
        rule = lambda state: state.has_from_list_unique(names, player, count)
    else:
        children = tuple(compile_rule(world, c, cache) for c in cond[1])
        if cond[0] == "and":
            def rule(state: CollectionState) -> bool:
                for child in children:
                    if not child(state):
                        return False
                return True
        else:
            def rule(state: CollectionState) -> bool:
                for child in children:
                    if child(state):
                        return True
                return False
    cache[cond] = rule
    return rule

def set_all_rules(world: OOTxMM) -> None:
    # Entrance and location rules are set where regions.py and locations.py create them.
    set_completion_condition(world)

def set_completion_condition(world: OOTxMM) -> None:
    # MM_MAJORA is OoTMM's event for beating Majora.
    world.multiworld.completion_condition[world.player] = lambda state: state.has("MM_MAJORA", world.player)
