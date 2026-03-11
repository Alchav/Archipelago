import typing
from dataclasses import dataclass
from Options import Choice, Option, Toggle, DefaultOnToggle, Range, OptionList, DeathLink, PerGameCommonOptions

class Goal(Range):
    """Achievement Goal"""
    display_name = "Achievement Goal"
    range_start = 1
    range_end = 639
    default = 100

class Traps(Range):
    """Traps Percentage"""
    display_name = "Traps Percentage"
    range_start = 1
    range_end = 70
    default = 50

@dataclass
class CCOptions(PerGameCommonOptions):
    advancement_goal: Goal
    traps_percentage: Traps