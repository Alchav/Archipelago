from dataclasses import dataclass
from Options import Range, NamedRange, PerGameCommonOptions


class LocationCount(Range):
    """The number of location checks. More locations means more trap items for you!"""
    range_start = 150
    range_end = 1500
    default = 300


class SpeedOption(NamedRange):
    range_start = 3
    range_end = 53
    special_range_names = {
        "level_0": 53,
        "level_1": 49,
        "level_2": 45,
        "level_3": 41,
        "level_4": 37,
        "level_5": 33,
        "level_6": 28,
        "level_7": 22,
        "level_8": 17,
        "level_9": 11,
        "level_10": 10,
        "level_11": 9,
        "level_12": 8,
        "level_13": 7,
        "level_14": 6,
        "level_15": 6,
        "level_16": 5,
        "level_17": 5,
        "level_18": 4,
        "level_19": 4,
        "level_20": 3
    }


class StartingSpeed(SpeedOption):
    """Starting speed level. You can set this value numerically, in which case the value chosen is the number of frames
    between the piece falling one line, so a lower number is faster."""
    default = 33


class MaximumSpeed(SpeedOption):
    """The maximum possible speed level. You can set this value numerically, in which case the value chosen is the
    number of frames between the piece falling one line, so a lower number is faster."""
    default = 10


class TargetSpeed(SpeedOption):
    """The final speed level you will end up at after all speed modification items are obtained. This can be lower or
    higher than Starting Speed, but if it is higher than Maximum Speed, it will be set to the same as Maximum Speed.
    You can set this value numerically, in which case the value chosen is thenumber of frames between the piece falling
    one line, so a lower number is faster."""
    default = 53


class ScoreMultipliers(Range):
    """Number of score multipliers for line clears in the item pool. In the vanilla game, line clear scores are
    multiplied by your current level. Here, it will be increased only by these items."""
    range_start = 10
    range_end = 40
    default = 30


@dataclass
class TetrisOptions(PerGameCommonOptions):
    location_count: LocationCount
    starting_speed: StartingSpeed
    maximum_speed: MaximumSpeed
    target_speed: TargetSpeed
    score_multipliers: ScoreMultipliers
