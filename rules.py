from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import CollectionState
from worlds.generic.Rules import add_rule, set_rule

if TYPE_CHECKING:
    from .world import OOTxMM


def set_all_rules(world: OOTxMM) -> None:
    #set_all_entrance_rules(world)
    #set_all_location_rules(world)
    set_completion_condition(world)


def set_all_entrance_rules(world: OOTxMM) -> None:
    overworld_to_bottom_right_room = world.get_entrance("Overworld to Bottom Right Room")
    overworld_to_top_left_room = world.get_entrance("Overworld to Top Left Room")
    overworld_to_secret_room = world.get_entrance("Overworld to Secret Room")
    right_room_to_final_boss_room = world.get_entrance("Right Room to Final Boss Room")

    def can_destroy_bush(state: CollectionState) -> bool:
        return state.has("Sword", world.player)
    
    set_rule(overworld_to_secret_room, can_destroy_bush)

    set_rule(overworld_to_bottom_right_room, can_destroy_bush)

    set_rule(overworld_to_top_left_room, lambda state: state.has("Key", world.player))

    set_rule(right_room_to_final_boss_room, lambda state: state.has("Top Left Room Button Pressed", world.player))


def set_all_location_rules(world: OOTxMM) -> None:
    
    right_room_enemy = world.get_location("Right Room Enemy Drop")

    if world.options.hard_mode:
        set_rule(
            right_room_enemy,
            lambda state: (
                state.has("Sword", world.player) and state.has_any(("Shield", "Health Upgrade"), world.player)
            ),
        )
    else:
        set_rule(right_room_enemy, lambda state: state.has("Sword", world.player))

    # Another way to chain multiple conditions is via the add_rule function.
    # This makes the access rules a bit slower though, so it should only be used if your structure justifies it.
    # In our case, it's pretty useful because hard mode and easy mode have different requirements.
    final_boss = world.get_location("Final Boss Defeated")

    # For the "known" requirements, it's still better to chain them using a normal "and" condition.
    add_rule(final_boss, lambda state: state.has_all(("Sword", "Shield"), world.player))

    if world.options.hard_mode:
        # You can check for multiple copies of an item by using the optional count parameter of state.has().
        add_rule(final_boss, lambda state: state.has("Health Upgrade", world.player, 2))


def set_completion_condition(world: OOTxMM) -> None:
    # In our case, we went for the Victory event design pattern (see create_events() in locations.py).
    # So lets undo what we just did, and instead set the completion condition to:
    world.multiworld.completion_condition[world.player] = lambda state: state.has("Victory", world.player)
