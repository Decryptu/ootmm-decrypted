from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .world import OOTxMM

def set_all_rules(world: OOTxMM) -> None:
    # Entrance and location rules are set where regions.py and locations.py create them.
    set_completion_condition(world)

# Settings set_completion_condition ports (raw/Meta_Options.py).
GOAL_SETTINGS = ["goal", "triforceGoal", "triforcePieces"]
TRIFORCE_PIECE = "SHARED_TRIFORCE"
TRIFORCE_ASPECTS = ("SHARED_TRIFORCE_POWER", "SHARED_TRIFORCE_COURAGE", "SHARED_TRIFORCE_WISDOM")


def triforce_items(settings) -> dict[str, int]:
    if settings["goal"] == "triforce":
        return {TRIFORCE_PIECE: settings["triforcePieces"]}
    if settings["goal"] == "triforce3":
        return dict.fromkeys(TRIFORCE_ASPECTS, 1)
    return {}

def set_completion_condition(world: OOTxMM) -> None:
    # OoTMM's goal check (isGoalReached in packages/logic/src/pathfind/pathfind.ts): OOT_GANON and MM_MAJORA
    # are its events for beating Ganon and Majora.
    player = world.player
    goal = world.ootmm_settings["goal"]
    if goal == "any":
        rule = lambda state: state.has_any(("OOT_GANON", "MM_MAJORA"), player)
    elif goal == "ganon":
        rule = lambda state: state.has("OOT_GANON", player)
    elif goal == "majora":
        rule = lambda state: state.has("MM_MAJORA", player)
    elif goal == "triforce":
        from .items import ITEM_BY_SYMBOLIC_ID
        name = ITEM_BY_SYMBOLIC_ID[TRIFORCE_PIECE].display_name
        rule = lambda state: state.has(name, player, world.ootmm_settings["triforceGoal"])
    elif goal == "triforce3":
        from .items import ITEM_BY_SYMBOLIC_ID
        names = tuple(ITEM_BY_SYMBOLIC_ID[item].display_name for item in TRIFORCE_ASPECTS)
        rule = lambda state: state.has_all(names, player)
    else:
        rule = lambda state: state.has_all(("OOT_GANON", "MM_MAJORA"), player)
    world.multiworld.completion_condition[player] = rule
