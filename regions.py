from __future__ import annotations

import pkgutil
import json
from typing import TYPE_CHECKING

from BaseClasses import Entrance, Region

if TYPE_CHECKING:
    from .world import OOTxMM

from . import ootxmm_staticdata

OOTxMMRegionList = ootxmm_staticdata.OOTxMMRegionData.keys()

def create_and_connect_regions(world: OOTxMM) -> None:
    create_all_regions(world)
    connect_regions(world)
    
def create_all_regions(world: OOTxMM) -> None:
    regions = [Region(name, world.player, world.multiworld) for name in ootxmm_staticdata.OOTxMMRegionData.keys()]
    world.multiworld.regions += regions

def connect_regions(world: OOTxMM) -> None:
    for region in ootxmm_staticdata.OOTxMMRegionData.keys():
        print("== Connecting region: " + region)
        worldregion = world.get_region(region)
        try:
            for connectedregion in ootxmm_staticdata.OOTxMMRegionData[region]["exits"].keys():
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