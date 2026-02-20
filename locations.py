from __future__ import annotations
import pkgutil
import json
from typing import TYPE_CHECKING

from BaseClasses import ItemClassification, Location

from . import items

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
        parent: str,
    ):
        self.id = id
        self.display_name = display_name
        self.core_name = core_name
        self.parent = parent

LocationIDCounter = 1
OOTxMMLocationList = []

OOTxMMRegionData = json.loads((pkgutil.get_data(__name__, 'raw/GreatWorldJSONdump.json')).decode('utf-8'))

for region in OOTxMMRegionData.keys():
    print("== Adding locations for region: " + region)
    try:
        for regionlocation in OOTxMMRegionData[region]["locations"].keys():
            try:
                print("==== + " + regionlocation)
                OOTxMMLocationList.append(OOTxMMLocationData(LocationIDCounter, regionlocation, regionlocation, region))
                LocationIDCounter += 1
            except Exception as e:
                print("==== ! Location add error: " + LocationIDCounter + " " + regionlocation + " " + regionlocation + " " + region + " ~~ " + str(e))
                pass
    except Exception as e:
        print("Locations Error: " + region + " ~~ " + str(e))
        pass

LOCATION_NAME_TO_ID = {item.display_name: item.id for item in OOTxMMLocationList}

def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return {location_name: LOCATION_NAME_TO_ID[location_name] for location_name in location_names}

def create_all_locations(world: OOTxMM) -> None:
    create_regular_locations(world)
    create_events(world)

def create_regular_locations(world: OOTxMM) -> None:
    # Finally, we need to put the Locations ("checks") into their regions.
    # Once again, before we do anything, we can grab our regions we created by using world.get_region()
    
    for location in OOTxMMLocationList:
        loc = get_location_names_with_ids([location.display_name])
        parent = world.get_region(location.parent)
        parent.add_locations(loc, OOTxMMLocation)

def create_events(world: OOTxMM) -> None:
    final_boss_room = world.get_region("Moon Boss")

    final_boss_room.add_event(
        "Final Boss Defeated", "Victory", location_type=OOTxMMLocation, item_type=items.OOTxMMItem
    )

