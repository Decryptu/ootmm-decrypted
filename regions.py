from __future__ import annotations

import pkgutil
import json
from typing import TYPE_CHECKING

from BaseClasses import Entrance, Region

if TYPE_CHECKING:
    from .world import OOTxMM

OOTxMMRegionData = json.loads((pkgutil.get_data(__name__, 'raw/GreatWorldJSONdump.json')).decode('utf-8'))
OOTxMMRegionList = OOTxMMRegionData.keys()

def create_and_connect_regions(world: OOTxMM) -> None:
    create_all_regions(world)
    connect_regions(world)
    
def create_all_regions(world: OOTxMM) -> None:
    regions = [Region(name, world.player, world.multiworld) for name in OOTxMMRegionData.keys()]
    world.multiworld.regions += regions

def connect_regions(world: OOTxMM) -> None:
    for region in OOTxMMRegionData.keys():
        print("== Connecting region: " + region)
        worldregion = world.get_region(region)
        try:
            for connectedregion in OOTxMMRegionData[region]["exits"].keys():
                try:
                    print("==== "+ region + " => " + connectedregion)
                    ExitRegion = world.get_region(connectedregion)
                    worldregion.connect(ExitRegion, f"{region} to {connectedregion}")
                except Exception as e:
                    print("Connection Error: " + region + " => " + connectedregion + " ~~ " + str(e))
                    pass
        except Exception as e:
            print("Connection Error: " + region + " ~~ " + str(e))
            pass