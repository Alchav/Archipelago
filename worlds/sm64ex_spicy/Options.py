from dataclasses import dataclass
from Options import DefaultOnToggle, Range, Toggle, DeathLink, Choice, PerGameCommonOptions, NamedRange, OptionGroup, \
    OptionSet

from .LogicTricks import logic_trick_option_keys


class CoinStarRequirement(Range):
    range_start = 1
    range_end = 100
    default = 100


class Coinsanity(Range):
    """
    Adds extra location checks for collecting coins.

    The value is a percentage from 0 to 100. For each main course, the game looks at every possible coin count below
    that course's Coin Star requirement, then creates that percentage of them as checks, rounded up. The checks are
    spread evenly below the Coin Star requirement and never duplicate the Coin Star check itself.

    Number of checks per main course:
    ceil((Coin Star Requirement - 1) * Coinsanity / 100)

    Example: if Bob-omb Battlefield requires 50 coins for its Coin Star, there are 49 possible Coinsanity checks
    from 1 to 49 coins. Coinsanity 2 creates 1 check, at 25 coins. Coinsanity 50 creates 25 checks. Coinsanity 100
    creates all 49 checks.

    If Secret Stage Coinsanity is enabled, secret stages use the same percentage based on their Coinsanity Max Coins
    option. At 100, every coin count from 1 through that stage's max is a check.

    Some Coinsanity locations may be created regardless of this option if there are too many items in the item pool.
    """
    display_name = "Coinsanity"
    range_start = 0
    range_end = 100
    default = 0


class SecretStageCoinsanity(Toggle):
    """Include Coinsanity checks for secret stages and Bowser stages."""
    display_name = "Secret Stage Coinsanity"


class PrincessSecretSlideCoinsanityMaxCoins(Range):
    """Maximum coin threshold used for The Princess's Secret Slide Coinsanity."""
    display_name = "The Princess's Secret Slide Coinsanity Max Coins"
    range_start = 0
    range_end = 80
    default = 80


class SecretAquariumCoinsanityMaxCoins(Range):
    """Maximum coin threshold used for The Secret Aquarium Coinsanity."""
    display_name = "The Secret Aquarium Coinsanity Max Coins"
    range_start = 0
    range_end = 56
    default = 56


class WingMarioOverTheRainbowCoinsanityMaxCoins(Range):
    """Maximum coin threshold used for Wing Mario Over the Rainbow Coinsanity."""
    display_name = "Wing Mario Over the Rainbow Coinsanity Max Coins"
    range_start = 0
    range_end = 56
    default = 56


class TowerOfTheWingCapCoinsanityMaxCoins(Range):
    """
    Maximum coin threshold used for Tower of the Wing Cap Coinsanity.

    Collecting all Tower of the Wing Cap coins is very difficult.
    """
    display_name = "Tower of the Wing Cap Coinsanity Max Coins"
    range_start = 0
    range_end = 63
    default = 31


class VanishCapUnderTheMoatCoinsanityMaxCoins(Range):
    """Maximum coin threshold used for Vanish Cap Under the Moat Coinsanity."""
    display_name = "Vanish Cap Under the Moat Coinsanity Max Coins"
    range_start = 0
    range_end = 27
    default = 27


class CavernOfTheMetalCapCoinsanityMaxCoins(Range):
    """Maximum coin threshold used for Cavern of the Metal Cap Coinsanity."""
    display_name = "Cavern of the Metal Cap Coinsanity Max Coins"
    range_start = 0
    range_end = 47
    default = 47


class BowserInTheDarkWorldCoinsanityMaxCoins(Range):
    """Maximum coin threshold used for Bowser in the Dark World Coinsanity."""
    display_name = "Bowser in the Dark World Coinsanity Max Coins"
    range_start = 0
    range_end = 80
    default = 80


class BowserInTheFireSeaCoinsanityMaxCoins(Range):
    """Maximum coin threshold used for Bowser in the Fire Sea Coinsanity."""
    display_name = "Bowser in the Fire Sea Coinsanity Max Coins"
    range_start = 0
    range_end = 80
    default = 80


class BowserInTheSkyCoinsanityMaxCoins(Range):
    """Maximum coin threshold used for Bowser in the Sky Coinsanity."""
    display_name = "Bowser in the Sky Coinsanity Max Coins"
    range_start = 0
    range_end = 76
    default = 76


secret_stage_coinsanity_max_coin_options = (
    PrincessSecretSlideCoinsanityMaxCoins,
    SecretAquariumCoinsanityMaxCoins,
    WingMarioOverTheRainbowCoinsanityMaxCoins,
    TowerOfTheWingCapCoinsanityMaxCoins,
    VanishCapUnderTheMoatCoinsanityMaxCoins,
    CavernOfTheMetalCapCoinsanityMaxCoins,
    BowserInTheDarkWorldCoinsanityMaxCoins,
    BowserInTheFireSeaCoinsanityMaxCoins,
    BowserInTheSkyCoinsanityMaxCoins,
)

secret_stage_coinsanity_max_coin_option_names = (
    "princess_secret_slide_coinsanity_max_coins",
    "secret_aquarium_coinsanity_max_coins",
    "wing_mario_over_the_rainbow_coinsanity_max_coins",
    "tower_of_the_wing_cap_coinsanity_max_coins",
    "vanish_cap_under_the_moat_coinsanity_max_coins",
    "cavern_of_the_metal_cap_coinsanity_max_coins",
    "bowser_in_the_dark_world_coinsanity_max_coins",
    "bowser_in_the_fire_sea_coinsanity_max_coins",
    "bowser_in_the_sky_coinsanity_max_coins",
)


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
    Does not affect secrets and levels that don't have a painting (Big Boo's Haunt, Rainbow Ride).
    This only affects the ability for Mario to enter a painting, the destination of the painting may change due to
    Entrance Randomization, if it is enabled.
    """
    display_name = "Enable Locked Paintings"


class StrictCapRequirements(DefaultOnToggle):
    """If disabled, Stars that expect special caps may have to be acquired without the caps.
    Bob-omb Battlefield cap tricks are instead controlled by Logic Tricks."""
    display_name = "Strict Cap Requirements"


class PerLevelCapItems(Toggle):
    """
    Generate separate cap items for each level that can require a cap instead of one global item per cap type.
    """
    display_name = "Per-Level Cap Items"


class MariosHat(Toggle):
    """Add Mario's Hat as a useful item. If disabled, the game starts with it unlocked."""
    display_name = "Include Mario's Hat"


class HazyMazeCaveSwimmingBeast(Toggle):
    """Shuffle Hazy Maze Cave - Swimming Beast as an item. If disabled, the game starts with it unlocked."""
    display_name = "Shuffle Hazy Maze Cave - Swimming Beast"


class RainbowRideCarpets(Toggle):
    """Shuffle Rainbow Ride - Carpets as an item. If disabled, the game starts with them unlocked."""
    display_name = "Shuffle Rainbow Ride - Carpets"


class TinyHugeIslandWarpPipes(Toggle):
    """Shuffle Tiny-Huge Island - Warp Pipes as an item. If disabled, the game starts with them unlocked."""
    display_name = "Shuffle Tiny-Huge Island - Warp Pipes"


class CoolCoolMountainBabyPenguins(Toggle):
    """Shuffle Cool, Cool Mountain - Baby Penguins as an item. If disabled, the game starts with them unlocked."""
    display_name = "Shuffle Cool, Cool Mountain - Baby Penguins"


class SnowmansLandPenguin(Toggle):
    """Shuffle Snowman's Land - Penguin as an item. If disabled, the game starts with it unlocked."""
    display_name = "Shuffle Snowman's Land - Penguin"


class ShiftingSandLandPyramidElevator(Toggle):
    """Shuffle Shifting Sand Land - Pyramid Elevator as an item. If disabled, the game starts with it unlocked."""
    display_name = "Shuffle Shifting Sand Land - Pyramid Elevator"


class WetDryWorldWaterLevelDiamond(Toggle):
    """Shuffle Wet-Dry World - Water Level Diamond as an item. If disabled, the game starts with it unlocked."""
    display_name = "Shuffle Wet-Dry World - Water Level Diamond"


class TickTockClockSpinners(Toggle):
    """Shuffle Tick Tock Clock - Spinners as an item. If disabled, the game starts with them unlocked."""
    display_name = "Shuffle Tick Tock Clock - Spinners"



class LevelFeatureItemMode(Choice):
    option_not_shuffled = 0
    option_global = 1
    option_individual = 2



class CheckerboardPlatforms(LevelFeatureItemMode):
    """
    Choose how Checkerboard Platform unlocks are handled.

    Not Shuffled - The game starts with all Checkerboard Platforms unlocked.

    Global - Shuffle one Checkerboard Platforms item that unlocks every applicable platform.

    Individual - Shuffle separate level-specific Checkerboard Platforms items.
    """
    display_name = "Checkerboard Platform Items"


class RollingLogs(LevelFeatureItemMode):
    """
    Choose how Rolling Log unlocks are handled.

    Not Shuffled - The game starts with all Rolling Logs unlocked.

    Global - Shuffle one Rolling Logs item that unlocks every applicable log.

    Individual - Shuffle separate level-specific Rolling Log items.
    """
    display_name = "Rolling Log Items"


class PurpleSwitches(LevelFeatureItemMode):
    """
    Choose how Purple Switch unlocks are handled.

    Not Shuffled - The game starts with all Purple Switches unlocked.

    Global - Shuffle one Purple Switches item that unlocks every applicable switch.

    Individual - Shuffle separate level-specific Purple Switch items.
    """
    display_name = "Purple Switch Items"


class BowserStage1Ups(Choice):
    """
    Choose how Bowser stage 1-Up objects that normally depend on Bowser key flags are handled.

    Vanilla - Two 1-Ups in Bowser in the Dark World require the Basement Key, and one 1-Up in Bowser in the Dark World
    plus two in Bowser in the Fire Sea require the Second Floor Key.

    Global - Shuffle one Bowser Stage Extra 1-Ups item that spawns all affected Bowser in the Dark World and Bowser in the
    Fire Sea 1-Ups.

    Individual - Shuffle separate Bowser in the Dark World - Extra 1-Ups and Bowser in the Fire Sea - Extra 1-Ups items.

    Always Spawn - All 1-Ups always spawn in the Bowser stages.
    """
    display_name = "Bowser Stage 1-Up Behavior"
    option_vanilla = 0
    option_global = 1
    option_individual = 2
    option_always_spawn = 3
    default = 0


class StrictCannonRequirements(DefaultOnToggle):
    """If disabled, Stars that expect cannons may have to be acquired without them.
    Has no effect if Buddy Checks are disabled and all movement abilities are not shuffled.
    Bob-omb Battlefield cannon tricks are instead controlled by Logic Tricks."""
    display_name = "Strict Cannon Requirements"


class AreaRandomizer(Choice):
    """Randomize Entrances"""
    display_name = "Entrance Randomizer"
    option_Off = 0
    option_Courses_Only = 1
    option_Courses_and_Secrets_Separate = 2
    option_Courses_and_Secrets = 3


class BuddyChecks(Toggle):
    """Bob-omb Buddies are checks, cannon unlocks are items"""
    display_name = "Bob-omb Buddy Checks"


class OneUpChecks(Toggle):
    """Include 1-Up mushrooms, including 1-Ups spawned from blocks, as Archipelago location checks."""
    display_name = "1-Up Checks"


class Blocksanity(Toggle):
    """Include coin blocks, cap blocks, shell blocks, and star blocks as Archipelago location checks."""
    display_name = "Blocksanity"


class EasyButterflies(Toggle):
    """Butterflies turn into 1-Up mushrooms regardless of Mario's distance from the butterfly, and one of the three
    always has a 1-Up."""
    display_name = "Easy Butterflies"


class NoDespawns(Toggle):
    """
    Prevent coins and 1-Ups from despawning over time. Coins and 1-Ups that fall into a void, quicksand, or lava are
    granted automatically. Bookends and small goombas drop their coins when they attack.
    """
    display_name = "No Despawns"


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

class TrapsFillerPercentage(NamedRange):
    """
    Replaces this percentage of filler items with trap items.
    Trap types are selected according to their configured weights.
    It is recommended to keep this at a low percentage so the majority of the pool aren't all traps.
    """
    default = 0
    range_start = 0
    range_end = 100
    display_name = "Replace Filler With Traps"
    special_range_names = {
        "disabled": 0,
        "light": 10,
        "normal": 25,
        "extreme": 50,
    }


class BonkTrapWeight(Range):
    """
    Relative weight for Bonk Traps.

    Higher values make this trap appear more often.
    A weight of 0 disables this trap.
    """
    range_start = 0
    range_end = 100
    default = 100
    display_name = "Bonk Trap Weight"


class FireTrapWeight(Range):
    """
    Relative weight for Burn Traps.

    Higher values make this trap appear more often.
    A weight of 0 disables this trap.
    """
    range_start = 0
    range_end = 100
    default = 100
    display_name = "Burn Trap Weight"


class ElectricTrapWeight(Range):
    """
    Relative weight for Shock Traps.

    Higher values make this trap appear more often.
    A weight of 0 disables this trap.
    """
    range_start = 0
    range_end = 100
    default = 100
    display_name = "Shock Trap Weight"


class ChuckyaTrapWeight(Range):
    """
    Relative weight for Chuckya Traps.

    Higher values make this trap appear more often.
    A weight of 0 disables this trap.
    """
    range_start = 0
    range_end = 100
    default = 100
    display_name = "Chuckya Trap Weight"


class SpinTrapWeight(Range):
    """
    Relative weight for Spin Traps.

    Higher values make this trap appear more often.
    A weight of 0 disables this trap.
    """
    range_start = 0
    range_end = 100
    default = 100
    display_name = "Spin Trap Weight"


class GustTrapWeight(Range):
    """
    Relative weight for Gust Traps.

    Higher values make this trap appear more often.
    A weight of 0 disables this trap.
    """
    range_start = 0
    range_end = 100
    default = 100
    display_name = "Gust Trap Weight"


trap_weight_options = (
    BonkTrapWeight,
    FireTrapWeight,
    ElectricTrapWeight,
    ChuckyaTrapWeight,
    SpinTrapWeight,
    GustTrapWeight,
)

trap_weight_option_names = (
    "bonk_trap_weight",
    "fire_trap_weight",
    "electric_trap_weight",
    "chuckya_trap_weight",
    "spin_trap_weight",
    "gust_trap_weight",
)

trap_item_name_by_option_name = {
    "bonk_trap_weight": "Bonk Trap",
    "fire_trap_weight": "Burn Trap",
    "electric_trap_weight": "Shock Trap",
    "chuckya_trap_weight": "Chuckya Trap",
    "spin_trap_weight": "Spin Trap",
    "gust_trap_weight": "Gust Trap",
}
class StrictMoveRequirements(DefaultOnToggle):
    """If disabled, Stars that expect certain moves may have to be acquired without them.
    Only makes a difference for movement abilities that are shuffled.
    Bob-omb Battlefield movement tricks are instead controlled by Logic Tricks."""
    display_name = "Strict Move Requirements"


class LogicTricks(OptionSet):
    """Choose specific advanced techniques to include in logic. The All Easy, All Medium, and All Hard entries
    include every trick at that difficulty and below. Details and videos for each trick are documented in
    LogicTricks.py."""
    display_name = "Logic Tricks"
    valid_keys = logic_trick_option_keys


class UniversalTrackerGlitchedLogic(OptionSet):
    """Choose tricks that the Universal Tracker should show as glitched logic.
    The All Easy, All Medium, and All Hard entries include every trick at that difficulty and below.
    """
    display_name = "Universal Tracker Glitched Logic"
    valid_keys = logic_trick_option_keys


class MoveRandomizerMode(Choice):
    option_not_shuffled = 0
    option_global = 1
    option_per_level = 2



class TripleJump(MoveRandomizerMode):
    """
    Choose how Triple Jump is handled.

    Not Shuffled - The game starts with Triple Jump unlocked.

    Global - Shuffle one Triple Jump item that unlocks the move everywhere.

    Per Level - Shuffle separate Triple Jump items for each main course. Castle, castle grounds, secret courses,
    cap stages, and Bowser stages use the Castle - Triple Jump item.
    """
    display_name = "Triple Jump"


class LongJump(MoveRandomizerMode):
    """
    Choose how Long Jump is handled.

    Not Shuffled - The game starts with Long Jump unlocked.

    Global - Shuffle one Long Jump item that unlocks the move everywhere.

    Per Level - Shuffle separate Long Jump items for each main course. Castle, castle grounds, secret courses,
    cap stages, and Bowser stages use the Castle - Long Jump item.
    """
    display_name = "Long Jump"


class Backflip(MoveRandomizerMode):
    """
    Choose how Backflip is handled.

    Not Shuffled - The game starts with Backflip unlocked.

    Global - Shuffle one Backflip item that unlocks the move everywhere.

    Per Level - Shuffle separate Backflip items for each main course. Castle, castle grounds, secret courses,
    cap stages, and Bowser stages use the Castle - Backflip item.
    """
    display_name = "Backflip"


class SideFlip(MoveRandomizerMode):
    """
    Choose how Side Flip is handled.

    Not Shuffled - The game starts with Side Flip unlocked.

    Global - Shuffle one Side Flip item that unlocks the move everywhere.

    Per Level - Shuffle separate Side Flip items for each main course. Castle, castle grounds, secret courses,
    cap stages, and Bowser stages use the Castle - Side Flip item.
    """
    display_name = "Side Flip"


class WallKick(MoveRandomizerMode):
    """
    Choose how Wall Kick is handled.

    Not Shuffled - The game starts with Wall Kick unlocked.

    Global - Shuffle one Wall Kick item that unlocks the move everywhere.

    Per Level - Shuffle separate Wall Kick items for each main course. Castle, castle grounds, secret courses,
    cap stages, and Bowser stages use the Castle - Wall Kick item.
    """
    display_name = "Wall Kick"


class Dive(MoveRandomizerMode):
    """
    Choose how Dive is handled.

    Not Shuffled - The game starts with Dive unlocked.

    Global - Shuffle one Dive item that unlocks the move everywhere.

    Per Level - Shuffle separate Dive items for each main course. Castle, castle grounds, secret courses,
    cap stages, and Bowser stages use the Castle - Dive item.
    """
    display_name = "Dive"


class GroundPound(MoveRandomizerMode):
    """
    Choose how Ground Pound is handled.

    Not Shuffled - The game starts with Ground Pound unlocked.

    Global - Shuffle one Ground Pound item that unlocks the move everywhere.

    Per Level - Shuffle separate Ground Pound items for each main course. Castle, castle grounds, secret courses,
    cap stages, and Bowser stages use the Castle - Ground Pound item.
    """
    display_name = "Ground Pound"


class Kick(MoveRandomizerMode):
    """
    Choose how Kick is handled.

    Not Shuffled - The game starts with Kick unlocked.

    Global - Shuffle one Kick item that unlocks the move everywhere.

    Per Level - Shuffle separate Kick items for each main course. Castle, castle grounds, secret courses,
    cap stages, and Bowser stages use the Castle - Kick item.
    """
    display_name = "Kick"


class Climb(MoveRandomizerMode):
    """
    Choose how Climb is handled.

    Not Shuffled - The game starts with Climb unlocked.

    Global - Shuffle one Climb item that unlocks the move everywhere.

    Per Level - Shuffle separate Climb items for each main course (Except Big Boo's Haunt which has no climbable objects).
    Castle, castle grounds, secret courses, cap stages, and Bowser stages use the Castle - Climb item.
    """
    display_name = "Climb"


class LedgeGrab(MoveRandomizerMode):
    """
    Choose how Ledge Grab is handled.

    Not Shuffled - The game starts with Ledge Grab unlocked.

    Global - Shuffle one Ledge Grab item that unlocks the move everywhere.

    Per Level - Shuffle separate Ledge Grab items for each main course. Castle, castle grounds, secret courses,
    cap stages, and Bowser stages use the Castle - Ledge Grab item.
    """
    display_name = "Ledge Grab"


move_randomizer_options = (
    TripleJump,
    LongJump,
    Backflip,
    SideFlip,
    WallKick,
    Dive,
    GroundPound,
    Kick,
    Climb,
    LedgeGrab,
)

move_randomizer_option_name_by_action = {
    "Triple Jump": "triple_jump",
    "Long Jump": "long_jump",
    "Backflip": "backflip",
    "Side Flip": "side_flip",
    "Wall Kick": "wall_kick",
    "Dive": "dive",
    "Ground Pound": "ground_pound",
    "Kick": "kick",
    "Climb": "climb",
    "Ledge Grab": "ledge_grab",
}


class MarioColor(NamedRange):
    """
    Cosmetic Mario palette color. Use a named color or a decimal RGB value from 0 through 16777215.

    To use an exact hex color, convert it to decimal first. For example, FF0000 is 16711680.
    """
    range_start = 0
    range_end = 16777215
    special_range_names = {
        "black": 0,
        "white": 16777215,
        "gray": 8421504,
        "red": 16711680,
        "green": 65280,
        "blue": 255,
        "yellow": 16776960,
        "cyan": 65535,
        "magenta": 16711935,
        "purple": 16711935,
        "orange": 16753920,
        "pink": 16761035,
        "brown": 10824234,
    }


class MarioHatColor(MarioColor):
    """Mario's hat color."""
    display_name = "Mario Hat Color"
    default = 16711680


class MarioShirtColor(MarioColor):
    """Mario's shirt color."""
    display_name = "Mario Shirt Color"
    default = 16711680


class MarioOverallsColor(MarioColor):
    """Mario's overalls color."""
    display_name = "Mario Overalls Color"
    default = 255


class MarioGlovesColor(MarioColor):
    """Mario's gloves color."""
    display_name = "Mario Gloves Color"
    default = 16777215


class MarioShoesColor(MarioColor):
    """Mario's shoes color."""
    display_name = "Mario Shoes Color"
    default = 7478286
    special_range_names = {**MarioColor.special_range_names, "default_brown": 7478286}


class MarioSkinColor(MarioColor):
    """Mario's skin color."""
    display_name = "Mario Skin Color"
    default = 16695673
    special_range_names = {**MarioColor.special_range_names, "default_skin": 16695673}


class MarioHairColor(MarioColor):
    """Mario's hair color."""
    display_name = "Mario Hair Color"
    default = 7538176
    special_range_names = {**MarioColor.special_range_names, "default_brown": 7538176}


class MusicShuffle(Choice):
    """
    Control in-game background music.

    Off - Use vanilla music.

    Shuffle - Archipelago sends a deterministic per-area music map.

    Random on Load - The game picks a random song each time an area loads.
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
        OneUpChecks,
        Blocksanity,
        EasyButterflies,
        NoDespawns,
        CombinedProgressiveKeys,
        EnableLockedPaintings,
        StrictCapRequirements,
        PerLevelCapItems,
        StrictCannonRequirements,
        LogicTricks,
        UniversalTrackerGlitchedLogic,
    ]),
    OptionGroup("Level Feature Unlocks", [
        HazyMazeCaveSwimmingBeast,
        RainbowRideCarpets,
        CheckerboardPlatforms,
        TinyHugeIslandWarpPipes,
        CoolCoolMountainBabyPenguins,
        SnowmansLandPenguin,
        ShiftingSandLandPyramidElevator,
        RollingLogs,
        PurpleSwitches,
        BowserStage1Ups,
        WetDryWorldWaterLevelDiamond,
        TickTockClockSpinners,
    ]),
    OptionGroup("Coin Options", [
        Coinsanity,
        SecretStageCoinsanity,
        *secret_stage_coinsanity_max_coin_options,
        *coin_star_requirement_options,
    ]),
    OptionGroup("Gameplay Options", [
        MariosHat,
    ]),
    OptionGroup("Ability Options", [
        *move_randomizer_options,
        StrictMoveRequirements,
    ]),
    OptionGroup("Trap Options", [
        TrapsFillerPercentage,
        *trap_weight_options,
    ]),
    OptionGroup("Cosmetic Options", [
        MarioHatColor,
        MarioShirtColor,
        MarioOverallsColor,
        MarioGlovesColor,
        MarioShoesColor,
        MarioSkinColor,
        MarioHairColor,
        MusicShuffle,
    ]),

]

@dataclass
class SM64Options(PerGameCommonOptions):
    area_rando: AreaRandomizer
    buddy_checks: BuddyChecks
    one_up_checks: OneUpChecks
    blocksanity: Blocksanity
    easy_butterflies: EasyButterflies
    no_despawns: NoDespawns
    combined_progressive_keys: CombinedProgressiveKeys
    enable_locked_paintings: EnableLockedPaintings
    triple_jump: TripleJump
    long_jump: LongJump
    backflip: Backflip
    side_flip: SideFlip
    wall_kick: WallKick
    dive: Dive
    ground_pound: GroundPound
    kick: Kick
    climb: Climb
    ledge_grab: LedgeGrab
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
    bowser_stage_1ups: BowserStage1Ups
    wet_dry_world_water_level_diamond: WetDryWorldWaterLevelDiamond
    tick_tock_clock_spinners: TickTockClockSpinners
    strict_cannon_requirements: StrictCannonRequirements
    strict_move_requirements: StrictMoveRequirements
    logic_tricks: LogicTricks
    universal_tracker_glitched_logic: UniversalTrackerGlitchedLogic
    marios_hat: MariosHat
    mario_hat_color: MarioHatColor
    mario_shirt_color: MarioShirtColor
    mario_overalls_color: MarioOverallsColor
    mario_gloves_color: MarioGlovesColor
    mario_shoes_color: MarioShoesColor
    mario_skin_color: MarioSkinColor
    mario_hair_color: MarioHairColor
    music_shuffle: MusicShuffle
    coinsanity: Coinsanity
    secret_stage_coinsanity: SecretStageCoinsanity
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
    princess_secret_slide_coinsanity_max_coins: PrincessSecretSlideCoinsanityMaxCoins
    secret_aquarium_coinsanity_max_coins: SecretAquariumCoinsanityMaxCoins
    wing_mario_over_the_rainbow_coinsanity_max_coins: WingMarioOverTheRainbowCoinsanityMaxCoins
    tower_of_the_wing_cap_coinsanity_max_coins: TowerOfTheWingCapCoinsanityMaxCoins
    vanish_cap_under_the_moat_coinsanity_max_coins: VanishCapUnderTheMoatCoinsanityMaxCoins
    cavern_of_the_metal_cap_coinsanity_max_coins: CavernOfTheMetalCapCoinsanityMaxCoins
    bowser_in_the_dark_world_coinsanity_max_coins: BowserInTheDarkWorldCoinsanityMaxCoins
    bowser_in_the_fire_sea_coinsanity_max_coins: BowserInTheFireSeaCoinsanityMaxCoins
    bowser_in_the_sky_coinsanity_max_coins: BowserInTheSkyCoinsanityMaxCoins
    traps_filler_percentage: TrapsFillerPercentage
    bonk_trap_weight: BonkTrapWeight
    fire_trap_weight: FireTrapWeight
    electric_trap_weight: ElectricTrapWeight
    chuckya_trap_weight: ChuckyaTrapWeight
    spin_trap_weight: SpinTrapWeight
    gust_trap_weight: GustTrapWeight
    death_link: DeathLink
    completion_type: CompletionType
