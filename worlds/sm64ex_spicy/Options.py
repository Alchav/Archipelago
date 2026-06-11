from dataclasses import dataclass
from Options import DefaultOnToggle, Range, Toggle, DeathLink, Choice, OptionError, PerGameCommonOptions, OptionDict, \
    OptionSet, OptionGroup
from .Items import action_item_data_table


class CoinStarRequirement(Range):
    range_start = 1
    range_end = 100
    default = 100


class BobOmbBattlefieldCoinStarRequirement(CoinStarRequirement):
    """Coins needed for the Coin Star in Bob-omb Battlefield."""
    display_name = "Bob-omb Battlefield Coin Star Requirement"
    range_end = 146


class WhompsFortressCoinStarRequirement(CoinStarRequirement):
    """Coins needed for the Coin Star in Whomp's Fortress."""
    display_name = "Whomp's Fortress Coin Star Requirement"
    range_end = 141


class JollyRogerBayCoinStarRequirement(CoinStarRequirement):
    """Coins needed for the Coin Star in Jolly Roger Bay."""
    display_name = "Jolly Roger Bay Coin Star Requirement"
    range_end = 104


class CoolCoolMountainCoinStarRequirement(CoinStarRequirement):
    """Coins needed for the Coin Star in Cool, Cool Mountain."""
    display_name = "Cool, Cool Mountain Coin Star Requirement"
    range_end = 154


class BigBoosHauntCoinStarRequirement(CoinStarRequirement):
    """Coins needed for the Coin Star in Big Boo's Haunt."""
    display_name = "Big Boo's Haunt Coin Star Requirement"
    range_end = 151


class HazyMazeCaveCoinStarRequirement(CoinStarRequirement):
    """Coins needed for the Coin Star in Hazy Maze Cave."""
    display_name = "Hazy Maze Cave Coin Star Requirement"
    range_end = 139


class LethalLavaLandCoinStarRequirement(CoinStarRequirement):
    """Coins needed for the Coin Star in Lethal Lava Land."""
    display_name = "Lethal Lava Land Coin Star Requirement"
    range_end = 133


class ShiftingSandLandCoinStarRequirement(CoinStarRequirement):
    """Coins needed for the Coin Star in Shifting Sand Land."""
    display_name = "Shifting Sand Land Coin Star Requirement"
    range_end = 136


class DireDireDocksCoinStarRequirement(CoinStarRequirement):
    """Coins needed for the Coin Star in Dire, Dire Docks."""
    display_name = "Dire, Dire Docks Coin Star Requirement"
    range_end = 106


class SnowmansLandCoinStarRequirement(CoinStarRequirement):
    """Coins needed for the Coin Star in Snowman's Land."""
    display_name = "Snowman's Land Coin Star Requirement"
    range_end = 127


class WetDryWorldCoinStarRequirement(CoinStarRequirement):
    """Coins needed for the Coin Star in Wet-Dry World."""
    display_name = "Wet-Dry World Coin Star Requirement"
    range_end = 152


class TallTallMountainCoinStarRequirement(CoinStarRequirement):
    """Coins needed for the Coin Star in Tall, Tall Mountain."""
    display_name = "Tall, Tall Mountain Coin Star Requirement"
    range_end = 137


class TinyHugeIslandCoinStarRequirement(CoinStarRequirement):
    """Coins needed for the Coin Star in Tiny-Huge Island."""
    display_name = "Tiny-Huge Island Coin Star Requirement"
    range_end = 191


class TickTockClockCoinStarRequirement(CoinStarRequirement):
    """Coins needed for the Coin Star in Tick Tock Clock."""
    display_name = "Tick Tock Clock Coin Star Requirement"
    range_end = 128


class RainbowRideCoinStarRequirement(CoinStarRequirement):
    """Coins needed for the Coin Star in Rainbow Ride."""
    display_name = "Rainbow Ride Coin Star Requirement"
    range_end = 146


coin_star_requirement_options = (
    BobOmbBattlefieldCoinStarRequirement,
    WhompsFortressCoinStarRequirement,
    JollyRogerBayCoinStarRequirement,
    CoolCoolMountainCoinStarRequirement,
    BigBoosHauntCoinStarRequirement,
    HazyMazeCaveCoinStarRequirement,
    LethalLavaLandCoinStarRequirement,
    ShiftingSandLandCoinStarRequirement,
    DireDireDocksCoinStarRequirement,
    SnowmansLandCoinStarRequirement,
    WetDryWorldCoinStarRequirement,
    TallTallMountainCoinStarRequirement,
    TinyHugeIslandCoinStarRequirement,
    TickTockClockCoinStarRequirement,
    RainbowRideCoinStarRequirement,
)

coin_star_requirement_option_names = (
    "bob_omb_battlefield_coin_star_requirement",
    "whomps_fortress_coin_star_requirement",
    "jolly_roger_bay_coin_star_requirement",
    "cool_cool_mountain_coin_star_requirement",
    "big_boos_haunt_coin_star_requirement",
    "hazy_maze_cave_coin_star_requirement",
    "lethal_lava_land_coin_star_requirement",
    "shifting_sand_land_coin_star_requirement",
    "dire_dire_docks_coin_star_requirement",
    "snowmans_land_coin_star_requirement",
    "wet_dry_world_coin_star_requirement",
    "tall_tall_mountain_coin_star_requirement",
    "tiny_huge_island_coin_star_requirement",
    "tick_tock_clock_coin_star_requirement",
    "rainbow_ride_coin_star_requirement",
)

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


class MariosHat(Toggle):
    """Add Mario's Hat as a useful item. If disabled, the client starts with it unlocked."""
    display_name = "Include Mario's Hat"


class ArbitraryFeatureToggle(DefaultOnToggle):
    """Shuffle this level feature as an Archipelago item. If disabled, the client starts with it unlocked."""


class HazyMazeCaveSwimmingBeast(ArbitraryFeatureToggle):
    display_name = "Shuffle Hazy Maze Cave - Swimming Beast"


class RainbowRideCarpets(ArbitraryFeatureToggle):
    display_name = "Shuffle Rainbow Ride - Carpets"


class TinyHugeIslandWarpPipes(ArbitraryFeatureToggle):
    display_name = "Shuffle Tiny-Huge Island - Warp Pipes"


class CoolCoolMountainBabyPenguins(ArbitraryFeatureToggle):
    display_name = "Shuffle Cool, Cool Mountain - Baby Penguins"


class SnowmansLandPenguin(ArbitraryFeatureToggle):
    display_name = "Shuffle Snowman's Land - Penguin"


class ShiftingSandLandPyramidElevator(ArbitraryFeatureToggle):
    display_name = "Shuffle Shifting Sand Land - Pyramid Elevator"


class WetDryWorldWaterLevelDiamond(ArbitraryFeatureToggle):
    display_name = "Shuffle Wet-Dry World - Water Level Diamond"


class TickTockClockSpinners(ArbitraryFeatureToggle):
    display_name = "Shuffle Tick Tock Clock - Spinners"


class ArbitraryFeatureItemMode(Choice):
    """
    Not Shuffled - The client starts with this feature family unlocked.

    Global - Shuffle one item that unlocks every use of this feature family.

    Individual - Shuffle separate level-specific items where supported by the client.
    """
    option_not_shuffled = 0
    option_global = 1
    option_individual = 2
    default = 1


class CheckerboardPlatforms(ArbitraryFeatureItemMode):
    display_name = "Checkerboard Platform Items"


class RollingLogs(ArbitraryFeatureItemMode):
    display_name = "Rolling Log Items"


class PurpleSwitches(ArbitraryFeatureItemMode):
    display_name = "Purple Switch Items"


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


class MusicShuffle(Choice):
    """
    Control in-game background music.

    Off - Use vanilla music.

    Shuffle - Archipelago sends a deterministic per-area music map.

    Random on Load - The client picks a random song each time an area loads.
    """
    display_name = "Music Shuffle"
    option_off = 0
    option_shuffle = 1
    option_random_on_load = 2
    alias_on = 1


sm64_options_groups = [
    OptionGroup("Logic Options", [
        AreaRandomizer,
        BuddyChecks,
        ExclamationBoxes,
        CombinedProgressiveKeys,
        EnableLockedPaintings,
        StrictCapRequirements,
        PerLevelCapItems,
        StrictCannonRequirements,
    ]),
    OptionGroup("Arbitrary Feature Unlocks", [
        HazyMazeCaveSwimmingBeast,
        RainbowRideCarpets,
        CheckerboardPlatforms,
        TinyHugeIslandWarpPipes,
        CoolCoolMountainBabyPenguins,
        SnowmansLandPenguin,
        ShiftingSandLandPyramidElevator,
        RollingLogs,
        PurpleSwitches,
        WetDryWorldWaterLevelDiamond,
        TickTockClockSpinners,
    ]),
    OptionGroup("Coin Star Requirements", [
        *coin_star_requirement_options,
    ]),
    OptionGroup("Ability Options", [
        EnableMoveRandomizer,
        MoveRandomizerActions,
        StrictMoveRequirements,
    ]),
    OptionGroup("Cosmetic Options", [
        MariosHat,
        MarioColors,
        MusicShuffle,
    ]),

]

@dataclass
class SM64Options(PerGameCommonOptions):
    area_rando: AreaRandomizer
    buddy_checks: BuddyChecks
    exclamation_boxes: ExclamationBoxes
    combined_progressive_keys: CombinedProgressiveKeys
    enable_locked_paintings: EnableLockedPaintings
    enable_move_rando: EnableMoveRandomizer
    move_rando_actions: MoveRandomizerActions
    strict_cap_requirements: StrictCapRequirements
    per_level_cap_items: PerLevelCapItems
    hazy_maze_cave_swimming_beast: HazyMazeCaveSwimmingBeast
    rainbow_ride_carpets: RainbowRideCarpets
    checkerboard_platforms: CheckerboardPlatforms
    tiny_huge_island_warp_pipes: TinyHugeIslandWarpPipes
    cool_cool_mountain_baby_penguins: CoolCoolMountainBabyPenguins
    snowmans_land_penguin: SnowmansLandPenguin
    shifting_sand_land_pyramid_elevator: ShiftingSandLandPyramidElevator
    rolling_logs: RollingLogs
    purple_switches: PurpleSwitches
    wet_dry_world_water_level_diamond: WetDryWorldWaterLevelDiamond
    tick_tock_clock_spinners: TickTockClockSpinners
    strict_cannon_requirements: StrictCannonRequirements
    strict_move_requirements: StrictMoveRequirements
    marios_hat: MariosHat
    mario_colors: MarioColors
    music_shuffle: MusicShuffle
    bob_omb_battlefield_coin_star_requirement: BobOmbBattlefieldCoinStarRequirement
    whomps_fortress_coin_star_requirement: WhompsFortressCoinStarRequirement
    jolly_roger_bay_coin_star_requirement: JollyRogerBayCoinStarRequirement
    cool_cool_mountain_coin_star_requirement: CoolCoolMountainCoinStarRequirement
    big_boos_haunt_coin_star_requirement: BigBoosHauntCoinStarRequirement
    hazy_maze_cave_coin_star_requirement: HazyMazeCaveCoinStarRequirement
    lethal_lava_land_coin_star_requirement: LethalLavaLandCoinStarRequirement
    shifting_sand_land_coin_star_requirement: ShiftingSandLandCoinStarRequirement
    dire_dire_docks_coin_star_requirement: DireDireDocksCoinStarRequirement
    snowmans_land_coin_star_requirement: SnowmansLandCoinStarRequirement
    wet_dry_world_coin_star_requirement: WetDryWorldCoinStarRequirement
    tall_tall_mountain_coin_star_requirement: TallTallMountainCoinStarRequirement
    tiny_huge_island_coin_star_requirement: TinyHugeIslandCoinStarRequirement
    tick_tock_clock_coin_star_requirement: TickTockClockCoinStarRequirement
    rainbow_ride_coin_star_requirement: RainbowRideCoinStarRequirement
    death_link: DeathLink
    completion_type: CompletionType
