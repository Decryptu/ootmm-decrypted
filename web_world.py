from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld

from .options import option_groups, option_presets

class OOTxMMWebWorld(WebWorld):
    game = "OOTxMM"
    theme = "partyTime"

    setup_en = Tutorial(
        "OOTxMM AP Setup Guide",
        "A guide to setting up OOTxMM for Archipelago.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Quasky"],
    )
    
    tutorials = [setup_en]
    
    option_groups = option_groups
    options_presets = option_presets