from dataclasses import dataclass
from Options import OptionGroup, PerGameCommonOptions, Toggle, Choice, Range

# Main Options
class OOTxMMGoal(Choice):
    """
    The objective of the seed. The game will end when the specified goal is reached.
    - **Any**: You can beat either Ganon or Majora.
    - **Ganon**: You must beat Ganon.
    - **Majora**: You must beat Majora.
    - **Both**: You must beat Ganon AND Majora. You can do so in any order.
    - **Triforce**: You must collect Triforce Pieces to win.
    - **Triforce3**: You must collect the three parts of the Triforce (Power, Courage and Wisdom) to win. Specific hints will guide you.
    """
    display_name = "Goal"
    option_any_goal = 0
    option_ganon = 1
    option_majora = 2
    option_both = 3
    option_triforce = 4
    option_triforce3 = 5
    default = option_both
    
class OOTxMMTriforceGoal(Range):
    """
    The amount of Triforce Pieces that are required to win.
    """
    display_name = "Triforce Goal"
    range_start = 1
    range_end = 10
    default = 5
    
    
    
    
    
    
    
    
    
    
class OOTxMMSecretTest(Toggle):
    """
    Enable secret testing features
    """
    display_name = "Secret Testing Data"
    
@dataclass
class OOTxMMOptions(PerGameCommonOptions):
    goal: OOTxMMGoal
    triforce_goal: OOTxMMTriforceGoal
    secret_testing_data: OOTxMMSecretTest
    
option_groups = [
    OptionGroup(
        "Template Options",
        [OOTxMMGoal, OOTxMMTriforceGoal,OOTxMMSecretTest],
    ),
]

option_presets = {
    "Womp Womp": {
        "goal": OOTxMMGoal.option_both,
        "triforce_goal": 5,
        "secret_testing_data": False,
    },
    "Thwom Womp": {
        "goal": OOTxMMGoal.option_ganon,
        "triforce_goal": 5,
        "secret_testing_data": False,
    },
}