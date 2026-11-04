from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .world import OOTxMM

def set_all_rules(world: OOTxMM) -> None:
    # Entrance and location rules are set where regions.py and locations.py create them.
    set_completion_condition(world)

# Settings set_completion_condition ports (raw/Meta_Options.py).
GOAL_SETTINGS = ["goal"]

def set_completion_condition(world: OOTxMM) -> None:
    # OoTMM's goal check (isGoalReached in packages/logic/src/pathfind/pathfind.ts): OOT_GANON and MM_MAJORA
    # are its events for beating Ganon and Majora. The Triforce goals are not offered yet.
    player = world.player
    goal = world.ootmm_settings["goal"]
    if goal == "any":
        rule = lambda state: state.has_any(("OOT_GANON", "MM_MAJORA"), player)
    elif goal == "ganon":
        rule = lambda state: state.has("OOT_GANON", player)
    elif goal == "majora":
        rule = lambda state: state.has("MM_MAJORA", player)
    else:
        rule = lambda state: state.has_all(("OOT_GANON", "MM_MAJORA"), player)
    world.multiworld.completion_condition[player] = rule
