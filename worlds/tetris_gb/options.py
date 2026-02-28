from dataclasses import dataclass
from Options import Range, NamedRange, Choice, PerGameCommonOptions, NonLocalItems


class GoalScore(Range):
    """The score you must reach to trigger the rocket launch sequence upon game over,
    which completes the game in Archipelago."""
    display_name = "Goal Score"
    range_start = 100000
    default = 200000
    range_end = 999999


class LocationCount(Range):
    """The number of location checks. More locations means more filler items, including your chosen traps!
    Each check requires reaching a specific score.
    The score thresholds for each check will be spread out up to your end goal of 200,000 points."""
    display_name = "Location Count"
    range_start = 200
    range_end = 2000
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
    display_name = "Starting Speed"
    default = 33


class TargetSpeed(SpeedOption):
    """The final speed level you will end up at after all speed modification items are obtained. This can be lower or
    higher than Starting Speed, but if it is higher than Maximum Speed, it will be set to the same as Maximum Speed.
    You can set this value numerically, in which case the value chosen is thenumber of frames between the piece falling
    one line, so a lower number is faster."""
    display_name = "Target Speed"
    default = 10


class MaximumSpeed(SpeedOption):
    """The maximum possible speed level. You can set this value numerically, in which case the value chosen is the
    number of frames between the piece falling one line, so a lower number is faster."""
    display_name = "Maximum Speed"
    default = 7


class ScoreMultipliers(Range):
    """Number of score multipliers for line clears in the item pool. In the vanilla game, line clear scores are
    multiplied by your current level. Here, it will be increased only by these items."""
    display_name = "Score Multipliers"
    range_start = 15
    range_end = 99
    default = 40


class NextPieceDisplay(Choice):
    """Enable or Disable displaying the next piece.
    Enabled to Disabled: A single trap item permanently hides the next piece display.
    Disabled to Enabled: The next piece display starts disabled but is enabled permanently by a single item.
    Toggles: A number of items are added to the item pool that toggle the next piece display."""
    display_name = "Next Piece Display"
    option_enabled = 0
    option_disabled = 1
    option_enabled_to_disabled = 2
    option_disabled_to_enabled = 3
    option_toggles = 4
    default = 0


class FillerWeights(Range):
    range_start = 0
    range_end = 100


class RowClearWeight(FillerWeights):
    """Weight of "Clear Random Row" items in the item pool.
    These cause a random row to clear as if it had been filled in completely, the next time you connect a piece."""
    display_name = "Clear Random Row Weight"
    default = 32

    @staticmethod
    def get_item(random):
        return "Clear Random Row"


class GarbageLineWeight(FillerWeights):
    """Weight of Garbage Line traps in the item pool.
    These create a line of 9 blocks and one empty tile that come up from the bottom of the screen and push all existing
    pieces upward, the next time you connect a piece."""
    display_name = "Garbage Line Weight"
    default = 64

    @staticmethod
    def get_item(random):
        return "Garbage Line"


class ShuffleGarbageLineHoleWeight(FillerWeights):
    """Weight of Shuffle Garbage Line Hole traps in the item pool.
    These randomly change which tile will be empty when Garbage Lines are generated."""
    display_name = "Shuffle Garbage Line Hole Weight"
    default = 8

    @staticmethod
    def get_item(random):
        return "Shuffle Garbage Line Hole"


class RandomInputsWeight(FillerWeights):
    """Weight of Random Input traps in the item pool.
    These cause a loss of control of the game as random buttons register every frame.
    Trap lengths range from 1 frame to 4 seconds."""
    display_name = "Random Inputs Weight"
    default = 16

    @staticmethod
    def get_item(random):
        return random.choices(["1 Frame of Random Inputs", "1 Second of Random Inputs", "2 Seconds of Random Inputs",
                               "3 Seconds of Random Inputs", "4 Seconds of Random Inputs"],
                              k=1, weights=[16, 8, 4, 2, 1])[0]


class WallTrapWeight(FillerWeights):
    """Weight of Wall Trap items in the item pool.
    These warp your active piece into the left or right wall and instantly connect them, which may or may not result
    in tiles hanging out into the game area."""
    display_name = "Wall Trap Weight"
    default = 32

    @staticmethod
    def get_item(random):
        return random.choice(["Active Piece Gets Stuck in the Left Wall", "Active Piece Gets Stuck in the Right Wall"])


class InstantlyLockActivePieceWeight(FillerWeights):
    """Weight of "Instantly Lock Active Piece" items in the item pool.
    These cause your active piece to instantly lock in piece as if there are blocks underneath it, whether there are
    or not."""
    display_name = "Instantl Lock Weight"
    default = 4

    @staticmethod
    def get_item(random):
        return "Instantly Lock Active Piece"


class IllusoryPieceWeight(FillerWeights):
    """Weight of Illusory Piece trap items in the item pool.
    These trap items cause the next piece you connect to be an illusion. Future pieces will fall right through it.
    They will disappear the next time you clear a line. These will be more troublesome if you are paying less attention
    to your incoming items!"""
    display_name = "Illusory Piece Weight"
    default = 4

    @staticmethod
    def get_item(random):
        return "Active Piece is an Illusion"


class ToggleNextPieceWeight(FillerWeights):
    """Weight of Toggle Next Piece trap items in the item pool. Only in effect if Next Piece Display is set to Toggles.
    These toggle the visibility of the next piece display. Pressing select does not toggle it in Archipelago."""
    display_name = "Toggle Next Piece Weight"
    default = 4

    @staticmethod
    def get_item(random):
        return "Toggle Next Piece"


class TetrisNonLocalItems(NonLocalItems):
    __doc__ = NonLocalItems.__doc__
    default = frozenset({"Garbage Line", "1 Frame of Random Inputs", "1 Second of Random Inputs",
                         "2 Seconds of Random Inputs", "3 Seconds of Random Inputs", "4 Seconds of Random Inputs",
                         "Instantly Lock Active Piece", "Active Piece Gets Stuck in the Left Wall",
                         "Active Piece Gets Stuck in the Right Wall", "Clear Random Row"})

@dataclass
class TetrisOptions(PerGameCommonOptions):
    goal_score: GoalScore
    location_count: LocationCount
    starting_speed: StartingSpeed
    target_speed: TargetSpeed
    maximum_speed: MaximumSpeed
    score_multipliers: ScoreMultipliers
    next_piece_display: NextPieceDisplay
    clear_random_row_weight: RowClearWeight
    garbage_line_weight: GarbageLineWeight
    shuffle_garbage_line_hole_weight: ShuffleGarbageLineHoleWeight
    random_inputs_weight: RandomInputsWeight
    instant_lock_weight: InstantlyLockActivePieceWeight
    wall_trap_weight: WallTrapWeight
    illusory_piece_weight: IllusoryPieceWeight
    toggle_next_piece_weight: ToggleNextPieceWeight
    non_local_items: TetrisNonLocalItems
