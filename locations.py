from __future__ import annotations
from typing import TYPE_CHECKING

from BaseClasses import Location, Region

from . import items, logic, ootxmm_staticdata, rules

if TYPE_CHECKING:
    from .world import OOTxMM

class OOTxMMLocation(Location):
    game = "OOTxMM"

# Every check in the world dump has an ID, from the registry raw/GenerateMetadata.py keeps, so IDs stay
# the same across OoTMM releases. Checks no region can reach at either age are not created.
LOCATION_NAME_TO_ID = {
    name: ootxmm_staticdata.OOTxMMLocationIDs[name]
    for regiondata in ootxmm_staticdata.OOTxMMRegionData.values()
    for name in regiondata.get("locations") or {}
}

def create_all_locations(world: OOTxMM) -> None:
    for name, parents in world.logic.checks.items():
        location = OOTxMMLocation(world.player, name, LOCATION_NAME_TO_ID[name])
        place(world, location, parents, "check")
    # OoTMM's events become event items on locations of the same name.
    for event, parents in world.logic.events.items():
        location = OOTxMMLocation(world.player, event, None)
        location.place_locked_item(items.OOTxMMItem(event, items.ItemClassification.progression, None, world.player))
        place(world, location, parents, "event")

def place(world: OOTxMM, location: OOTxMMLocation, parents: list, kind: str) -> None:
    # A location has one region. OoTMM can list it under several regions and ages, meaning reachable from
    # any of them: it then gets its own region, entered from each parent with that parent's condition.
    if len(parents) == 1:
        area, age, cond = parents[0]
        region = world.get_region(logic.region_name(area, age))
        rule = rules.compile_rule(world, cond, world.rule_cache)
        if rule:
            location.access_rule = rule
    else:
        region = Region(f"{location.name} ({kind})", world.player, world.multiworld)
        world.multiworld.regions.append(region)
        for area, age, cond in parents:
            parent = world.get_region(logic.region_name(area, age))
            parent.connect(region, f"{parent.name} to {location.name}", rules.compile_rule(world, cond, world.rule_cache))
    location.parent_region = region
    region.locations.append(location)
