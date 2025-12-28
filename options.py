from dataclasses import dataclass
from Options import OptionGroup, PerGameCommonOptions, Toggle

class OOTxMMHardMode(Toggle):
    """
    Docstring for OOTxMMHardMode
    """
    display_name = "Hard Mode"
    
class OOTxMMSecretTest(Toggle):
    """
    Enable secret testing features
    """
    display_name = "Secret Testing Data"
    
@dataclass
class OOTxMMOptions(PerGameCommonOptions):
    hard_mode: OOTxMMHardMode
    secret_testing_data: OOTxMMSecretTest
    
option_groups = [
    OptionGroup(
        "Template Options",
        [OOTxMMHardMode, OOTxMMSecretTest],
    ),
]

option_presets = {
    "Womp Womp": {
        "hard_mode": False,
        "secret_testing_data": False,
    },
    "Thwom Womp": {
        "hard_mode": True,
        "secret_testing_data": False,
    },
}