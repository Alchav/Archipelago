from dataclasses import dataclass

from Options import Range, PerGameCommonOptions

class QuickStart(Range):
    """
    Force up to two early-game progression items (Soil Sword, Watering Can,
    Fertilizer) to be in sphere 1 locally.
    """
    display_name = "Quick Start Items"
    range_start = 0
    range_end = 2
    default = 0

@dataclass
class TurnipBoyOptions(PerGameCommonOptions):
    quick_start: QuickStart
