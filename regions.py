from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Region

from . import logic

if TYPE_CHECKING:
    from .world import OOTxMM

def create_and_connect_regions(world: OOTxMM) -> None:
    create_all_regions(world)
    connect_regions(world)

def create_all_regions(world: OOTxMM) -> None:
    regions = [Region(logic.ORIGIN, world.player, world.multiworld)]
    regions += [Region(logic.region_name(area, age), world.player, world.multiworld) for area, age in world.logic.regions]
    world.multiworld.regions += regions

def connect_regions(world: OOTxMM) -> None:
    # Both ages start at the spawn: the origin leads to each age's copy of it.
    origin = world.get_region(logic.ORIGIN)
    for age in logic.AGES:
        origin.connect(world.get_region(logic.region_name(logic.ORIGIN, age)))
    for (area, age), exits in world.logic.exits.items():
        region = world.get_region(logic.region_name(area, age))
        for target, cond in exits:
            target_name = logic.region_name(target, age)
            region.connect(world.get_region(target_name), f"{region.name} to {target_name}",
                           world.time_logic.rule(area, age, cond))
