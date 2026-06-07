from dataclasses import dataclass
from Options import DefaultOnToggle, Toggle, DeathLink, Choice, OptionError, PerGameCommonOptions, OptionDict, \
    OptionSet, OptionGroup
from .Items import action_item_data_table

class EnableCoinStars(Toggle):
    """
    Add 100 Coin Stars as checks.
    """
    display_name = "Enable 100 Coin Stars"
    default = 0

class EnableLockedPaintings(Toggle):
    """
    Determine how paintings are treated.

    Off - Paintings are not locked, as long as you can access them you can enter them (Vanilla behavior).

    On - Paintings (other than Bob-omb Battlefield) are replaced in the pool with items to allow access to them.
    Attempting to enter a locked painting will simply kick Mario out.
    Does not affect secrets and levels that don't have a painting (Big Boo's Haunt, Hazy Maze Cave, Rainbow Ride).
    This only affects the ability for Mario to enter a painting, the destination of the painting may change due to Entrance Randomization, if it is enabled.
    """
    display_name = "Enable Locked Paintings"


class StrictCapRequirements(DefaultOnToggle):
    """If disabled, Stars that expect special caps may have to be acquired without the caps"""
    display_name = "Strict Cap Requirements"


class PerLevelCapItems(Toggle):
    """
    Generate separate cap items for each level that can require a cap instead of one global item per cap
    type.
    """
    display_name = "Per-Level Cap Items"


class StrictCannonRequirements(DefaultOnToggle):
    """If disabled, Stars that expect cannons may have to be acquired without them.
    Has no effect if Buddy Checks and Move Randomizer are disabled"""
    display_name = "Strict Cannon Requirements"


class AreaRandomizer(Choice):
    """Randomize Entrances"""
    display_name = "Entrance Randomizer"
    option_Off = 0
    option_Courses_Only = 1
    option_Courses_and_Secrets_Separate = 2
    option_Courses_and_Secrets = 3


class BuddyChecks(Toggle):
    """Bob-omb Buddies are checks, Cannon Unlocks are items"""
    display_name = "Bob-omb Buddy Checks"


class ExclamationBoxes(Toggle):
    """Include 1Up Exclamation Boxes during randomization.
    Adds 29 locations to the pool."""
    display_name = "Randomize 1Up !-Blocks"
    alias_1Ups_Only = 1


class CompletionType(Choice):
    """Set goal for game completion"""
    display_name = "Completion Goal"
    option_Last_Bowser_Stage = 0
    option_All_Bowser_Stages = 1


class CombinedProgressiveKeys(DefaultOnToggle):
    """
    Off - Use grouped castle keys: Dark World Key, Progressive Basement Key x2, Progressive Upstairs Key x3.

    On - Use a single combined Progressive Key with six tiers for all castle key doors.
    """
    display_name = "Combined Progressive Castle Keys"

class StrictMoveRequirements(DefaultOnToggle):
    """If disabled, Stars that expect certain moves may have to be acquired without them. Only makes a difference
    if Move Randomization is enabled"""
    display_name = "Strict Move Requirements"

class EnableMoveRandomizer(Toggle):
    """Mario is unable to perform some actions until a corresponding item is picked up.
    This option is incompatible with builds using a 'nomoverando' branch.
    Specific actions to randomize can be specified in the YAML."""
    display_name = "Enable Move Randomizer"

class MoveRandomizerActions(OptionSet):
    """Which actions to randomize when Move Randomizer is enabled"""
    display_name = "Randomized Moves"
    # HACK: Disable randomization for double jump
    valid_keys = [action for action in action_item_data_table if action != 'Double Jump']
    default = valid_keys


class MarioColors(OptionDict):
    """
    Cosmetic Mario palette. Keys may be shirt, overalls, gloves, shoes, skin, or hair, with each value being
    an RGB array.
    """
    display_name = "Mario Colors"
    valid_keys = {"shirt", "overalls", "gloves", "shoes", "skin", "hair"}
    default = {
        "shirt": [255, 0, 0],
        "overalls": [0, 0, 255],
        "gloves": [255, 255, 255],
        "shoes": [114, 28, 14],
        "skin": [254, 193, 121],
        "hair": [115, 6, 0]
    }

    def verify(self, world, player_name: str, plando_options) -> None:
        super().verify(world, player_name, plando_options)
        errors = []
        if self.value.keys() != self.valid_keys:
            errors.append(f"Color keys must be {self.valid_keys}. Keys used: {set(self.value.keys())}")
        for color_name, channels in self.value.items():
            if not isinstance(channels, (list, tuple)) or len(channels) != 3:
                errors.append(f"{color_name} must be an RGB array with exactly three channels.")
                continue
            invalid_channels = [
                channel for channel in channels
                if isinstance(channel, bool) or not isinstance(channel, int) or channel < 0 or channel > 255
            ]
            if invalid_channels:
                errors.append(f"{color_name} channels must be integers from 0 through 255.")
        if errors:
            raise OptionError(f"Player {player_name} has invalid Mario Colors:\n" + "\n".join(errors))

sm64_options_groups = [
    OptionGroup("Logic Options", [
        AreaRandomizer,
        BuddyChecks,
        ExclamationBoxes,
        CombinedProgressiveKeys,
        EnableCoinStars,
        EnableLockedPaintings,
        StrictCapRequirements,
        PerLevelCapItems,
        StrictCannonRequirements,
    ]),
    OptionGroup("Ability Options", [
        EnableMoveRandomizer,
        MoveRandomizerActions,
        StrictMoveRequirements,
    ]),
    OptionGroup("Cosmetic Options", [
        MarioColors,
    ]),

]

@dataclass
class SM64Options(PerGameCommonOptions):
    area_rando: AreaRandomizer
    buddy_checks: BuddyChecks
    exclamation_boxes: ExclamationBoxes
    combined_progressive_keys: CombinedProgressiveKeys
    enable_coin_stars: EnableCoinStars
    enable_locked_paintings: EnableLockedPaintings
    enable_move_rando: EnableMoveRandomizer
    move_rando_actions: MoveRandomizerActions
    strict_cap_requirements: StrictCapRequirements
    per_level_cap_items: PerLevelCapItems
    strict_cannon_requirements: StrictCannonRequirements
    strict_move_requirements: StrictMoveRequirements
    mario_colors: MarioColors
    death_link: DeathLink
    completion_type: CompletionType
