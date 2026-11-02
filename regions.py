from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Region

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
    for region, regiondata in ootxmm_staticdata.OOTxMMRegionData.items():
        worldregion = world.get_region(region)
        for connectedregion in regiondata.get("exits") or {}:
            worldregion.connect(world.get_region(connectedregion), f"{region} to {connectedregion}")
