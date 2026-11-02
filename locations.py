from __future__ import annotations
from typing import TYPE_CHECKING

from BaseClasses import Location, Region

from . import items, ootxmm_staticdata

if TYPE_CHECKING:
    from .world import OOTxMM

class OOTxMMLocation(Location):
    game = "OOTxMM"

class OOTxMMLocationData:
    def __init__(
        self,
        id: int | None,
        display_name: str,
        core_name: str,
        parents: list[str],
    ):
        self.id = id
        self.display_name = display_name
        self.core_name = core_name
        # OoTMM lists some checks under several regions: the check is reachable from any of them.
        self.parents = parents

LocationParents: dict[str, list[str]] = {}
for region, regiondata in ootxmm_staticdata.OOTxMMRegionData.items():
    for regionlocation in regiondata.get("locations") or {}:
        LocationParents.setdefault(regionlocation, []).append(region)

OOTxMMLocationList = [
    OOTxMMLocationData(LocationID, name, name, parents)
    for LocationID, (name, parents) in enumerate(LocationParents.items(), start=1)
]

LOCATION_NAME_TO_ID = {item.display_name: item.id for item in OOTxMMLocationList}

def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return {location_name: LOCATION_NAME_TO_ID[location_name] for location_name in location_names}

def create_all_locations(world: OOTxMM) -> None:
    create_regular_locations(world)
    create_events(world)

def create_regular_locations(world: OOTxMM) -> None:
    for location in OOTxMMLocationList:
        loc = get_location_names_with_ids([location.display_name])
        if len(location.parents) == 1:
            world.get_region(location.parents[0]).add_locations(loc, OOTxMMLocation)
            continue
        # A location can only have one region, so a check with several parents gets its own region,
        # entered from each parent. The access rule for each parent goes on that entrance.
        check_region = Region(f"{location.display_name} (check)", world.player, world.multiworld)
        world.multiworld.regions.append(check_region)
        check_region.add_locations(loc, OOTxMMLocation)
        for parent in location.parents:
            world.get_region(parent).connect(check_region, f"{parent} to {location.display_name}")

def create_events(world: OOTxMM) -> None:
    final_boss_room = world.get_region("MM Moon")

    final_boss_room.add_event(
        "BEAT MAJORA", "Victory", location_type=OOTxMMLocation, item_type=items.OOTxMMItem
    )
