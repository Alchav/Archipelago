from dataclasses import dataclass
from Options import DefaultOnToggle, Range, Toggle, DeathLink, Choice, PerGameCommonOptions, NamedRange, OptionGroup, \
    OptionSet, ItemsAccessibility

from .LogicTricks import logic_trick_option_keys


class CoinStarRequirement(Range):
    range_start = 1
    range_end = 100
    default = 100


class CoinCountChecks(Range):
    """
    Adds extra location checks for collecting coins.

    The value is a percentage from 0 to 100. For each main course, the game looks at every possible coin count below
    that course's Coin Star requirement, then creates that percentage of them as checks, rounded up. The checks are
    spread evenly below the Coin Star requirement and never duplicate the Coin Star check itself.

    Number of checks per main course:
    ceil((Coin Star Requirement - 1) * Coin Count Checks / 100)

    Example: if Bob-omb Battlefield requires 50 coins for its Coin Star, there are 49 possible count checks
    from 1 to 49 coins. A value of 2 creates 1 check, at 25 coins. A value of 50 creates 25 checks. A value of 100
    creates all 49 checks.

    Secret stages use the same percentage based on their Coin Count Max Coins option. At 100, every coin count
    from 1 through that stage's maximum is a check.

    Some Coin Count Check locations may be created regardless of this option if there are too many items in the item
    pool.
    """
    display_name = "Coin Count Checks"
    range_start = 0
    range_end = 100
    default = 0


class CoinChecks(Range):
    """Adds checks to individual physical coins. The percentage is applied independently to every level's complete
    set of coin objects and enemy/object coin outputs. Zero disables individual coin checks; 100 makes every coin
    output a check."""
    display_name = "Coin Checks"
    range_start = 0
    range_end = 100
    default = 0


class SM64Accessibility(ItemsAccessibility):
    default = ItemsAccessibility.option_full


class PrincessSecretSlideCoinCountMaxCoins(Range):
    """Maximum coin threshold used for The Princess's Secret Slide Coin Count Checks."""
    display_name = "The Princess's Secret Slide Coin Count Max Coins"
    range_start = 0
    range_end = 80
    default = 80


class SecretAquariumCoinCountMaxCoins(Range):
    """Maximum coin threshold used for The Secret Aquarium Coin Count Checks."""
    display_name = "The Secret Aquarium Coin Count Max Coins"
    range_start = 0
    range_end = 56
    default = 56


class WingMarioOverTheRainbowCoinCountMaxCoins(Range):
    """Maximum coin threshold used for Wing Mario Over the Rainbow Coin Count Checks."""
    display_name = "Wing Mario Over the Rainbow Coin Count Max Coins"
    range_start = 0
    range_end = 56
    default = 56


class TowerOfTheWingCapCoinCountMaxCoins(Range):
    """
    Maximum coin threshold used for Tower of the Wing Cap Coin Count Checks.
    """
    display_name = "Tower of the Wing Cap Coin Count Max Coins"
    range_start = 0
    range_end = 63
    default = 63


class VanishCapUnderTheMoatCoinCountMaxCoins(Range):
    """Maximum coin threshold used for Vanish Cap Under the Moat Coin Count Checks."""
    display_name = "Vanish Cap Under the Moat Coin Count Max Coins"
    range_start = 0
    range_end = 27
    default = 27


class CavernOfTheMetalCapCoinCountMaxCoins(Range):
    """Maximum coin threshold used for Cavern of the Metal Cap Coin Count Checks."""
    display_name = "Cavern of the Metal Cap Coin Count Max Coins"
    range_start = 0
    range_end = 47
    default = 47


class BowserInTheDarkWorldCoinCountMaxCoins(Range):
    """Maximum coin threshold used for Bowser in the Dark World Coin Count Checks."""
    display_name = "Bowser in the Dark World Coin Count Max Coins"
    range_start = 0
    range_end = 80
    default = 80


class BowserInTheFireSeaCoinCountMaxCoins(Range):
    """Maximum coin threshold used for Bowser in the Fire Sea Coin Count Checks."""
    display_name = "Bowser in the Fire Sea Coin Count Max Coins"
    range_start = 0
    range_end = 80
    default = 80


class BowserInTheSkyCoinCountMaxCoins(Range):
    """Maximum coin threshold used for Bowser in the Sky Coin Count Checks."""
    display_name = "Bowser in the Sky Coin Count Max Coins"
    range_start = 0
    range_end = 76
    default = 76


secret_stage_coin_count_max_coin_options = (
    PrincessSecretSlideCoinCountMaxCoins,
    SecretAquariumCoinCountMaxCoins,
    WingMarioOverTheRainbowCoinCountMaxCoins,
    TowerOfTheWingCapCoinCountMaxCoins,
    VanishCapUnderTheMoatCoinCountMaxCoins,
    CavernOfTheMetalCapCoinCountMaxCoins,
    BowserInTheDarkWorldCoinCountMaxCoins,
    BowserInTheFireSeaCoinCountMaxCoins,
    BowserInTheSkyCoinCountMaxCoins,
)

secret_stage_coin_count_max_coin_option_names = (
    "princess_secret_slide_coin_count_max_coins",
    "secret_aquarium_coin_count_max_coins",
    "wing_mario_over_the_rainbow_coin_count_max_coins",
    "tower_of_the_wing_cap_coin_count_max_coins",
    "vanish_cap_under_the_moat_coin_count_max_coins",
    "cavern_of_the_metal_cap_coin_count_max_coins",
    "bowser_in_the_dark_world_coin_count_max_coins",
    "bowser_in_the_fire_sea_coin_count_max_coins",
    "bowser_in_the_sky_coin_count_max_coins",
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
    """
    Coins needed for the Coin Star in Snowman's Land. With Full Accessibility, this is capped at 126 unless the
    Snowman's Land Impossible Coin trick is enabled.
    """
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
    """
    Coins needed for the Coin Star in Tiny-Huge Island. With Full Accessibility, this is capped at 192 unless the
    Tiny-Huge Island Impossible Coin trick is enabled.
    """
    display_name = "Tiny-Huge Island Coin Star Requirement"
    range_end = 193


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

class LevelUnlocks(Choice):
    """
    Choose which level entrances require unlock items.

    Disabled - Start with every level entrance unlocked.

    Special Only - Shuffle level unlocks for Tower of the Wing Cap, Big Boo's Haunt, Bowser in the Fire Sea,
    and Vanish Cap Under the Moat.

    Full - Also shuffle the course painting unlocks, Rainbow Ride, and Wing Mario Over the Rainbow.

    A locked entrance will reject Mario. Entrance Randomization may change the level reached through that entrance.
    """
    display_name = "Level Unlocks"
    option_disabled = 0
    option_special_only = 1
    option_full = 2
    alias_default = option_special_only
    alias_false = option_special_only
    alias_true = option_full
    default = 1


class CapItems(Choice):
    """
    Choose how cap items are handled.

    Global - Shuffle one item for each cap type that unlocks that cap everywhere.

    Per Level - Shuffle separate cap items for each level that can require a cap.

    Both - Shuffle both the global cap items and every applicable level-specific cap item.
    """
    display_name = "Cap Items"
    option_global = 0
    option_per_level = 1
    alias_individual = 1
    option_both = 2
    alias_false = 0
    alias_true = 1


class MariosHat(Toggle):
    """Add Mario's Hat as a useful item. If disabled, the game starts with it unlocked."""
    display_name = "Include Mario's Hat"


class LevelFeatureItemMode(Choice):
    option_not_shuffled = 0
    option_global = 1
    option_per_level = 2
    alias_individual = 2
    option_both = 3



class LevelFeatures(Choice):
    """
    Choose how level features are handled.

    Not Shuffled - Start with every level feature unlocked.

    Per Act Only - Shuffle only features that were tied to specific selected Stars in vanilla Super Mario 64.

    Global - Shuffle the full suite of Spicy Mycena 64 level feature items. Checkerboard Platforms, Rolling Logs, Purple
    Switches, Treasure Chests, and Warp Pipes use global items.

    Per Level - Shuffle the full suite of Spicy Mycena 64 level feature items. Checkerboard Platforms, Rolling Logs,
    Purple Switches, Treasure Chests, and Warp Pipes use separate level-specific items.

    Both - Shuffle both global and level-specific items for features that support both forms.
    """
    display_name = "Level Features"
    option_not_shuffled = 0
    option_per_act_only = 1
    option_global = 2
    option_per_level = 3
    option_both = 4
    default = 1


class BobombBuddies(Choice):
    """
    Choose how all Bob-omb Buddy spawns are handled.

    Not Shuffled - Start with every Bob-omb Buddy unlocked.

    Per Act Only - Shuffle the Bob-omb Battlefield, Whomp's Fortress, and Jolly Roger Bay buddies. Start with the
    remaining buddies unlocked.

    Global - Shuffle one Bob-omb Buddies item that unlocks every buddy.

    Per Level - Shuffle a separate item for every level's Bob-omb Buddy.

    Both - Shuffle the global Bob-omb Buddies item and every level-specific Bob-omb Buddy item.
    """
    display_name = "Bob-omb Buddy Items"
    option_not_shuffled = 0
    option_per_act_only = 1
    option_global = 2
    option_per_level = 3
    option_both = 4
    default = 1


class CoinObjectUnlocks(LevelFeatureItemMode):
    """
    Choose how placed coins, coin formations, and coin-producing object unlocks are handled.

    Not Shuffled - The game starts with every coin object unlocked.

    Global - Shuffle one item for each object type. Object types without a global item use their level-specific item.

    Per Level - Shuffle separate level-specific items for every applicable coin object type.

    Both - Shuffle both global and level-specific items for every applicable coin object type.
    """
    display_name = "Coin Object Unlocks"


class EnemyUnlocks(LevelFeatureItemMode):
    """
    Choose how unlocks are handled for most enemies.

    Not Shuffled - The game starts with every affected enemy unlocked.

    Global - Shuffle one item for each enemy type. Enemy types without a global item use their level-specific item.

    Per Level - Shuffle separate level-specific items for every applicable enemy type.

    Both - Shuffle both global and level-specific items for every applicable enemy type.
    """
    display_name = "Enemy Unlocks"


class OneUpUnlocks(LevelFeatureItemMode):
    """
    Choose how 1-Up source unlocks and Monty Moles are handled.

    Not Shuffled - Start with freestanding, triggered, block-spawned, butterfly 1-Ups and Monty Moles unlocked.

    Global - Shuffle one global item for each of those five 1-Up source types.

    Per Level - Shuffle separate source-type unlock items for each level that contains matching 1-Up checks.

    Both - Shuffle both global and level-specific items for every applicable 1-Up source type.
    """
    display_name = "1-Up Unlocks"


class SignUnlocks(LevelFeatureItemMode):
    """
    Choose how signposts and wall-mounted signs are unlocked. Signs may contain hints.

    Not Shuffled - Start with every sign unlocked.

    Global - Shuffle one Signs item that unlocks every sign.

    Per Level - Shuffle separate Signs items for each area containing signs. Castle - Signs controls all signs in the
    Castle Grounds, castle interior, and courtyard.

    Both - Shuffle the global Signs item and every level-specific Signs item.
    """
    display_name = "Sign Unlocks"


class BowserBombs(LevelFeatureItemMode):
    """
    Choose how Progressive Bowser Arena Bombs are handled.

    Not Shuffled - The game starts with all Bower Arena Bombs available.

    Global - Shuffle five Progressive Bowser Arena Bomb items that each add one bomb to each Bowser Arena.
    Bowser in the Dark World and Bowser in the Fire Sea cap at four bombs.

    Per Level - Shuffle separate bombs for each arena: four each for Bowser in the Dark World and Bowser in the
    Fire Sea, and five for Bowser in the Sky.

    Both - Shuffle five global bombs in addition to all thirteen level-specific bombs.
    """
    display_name = "Progressive Bowser Arena Bomb Items"


class BowserInTheDarkWorldHits(Range):
    """Number of Bowser Bomb hits required to defeat Bowser in the Dark World."""
    display_name = "Bowser in the Dark World Health"
    range_start = 1
    range_end = 4
    default = 1


class BowserInTheFireSeaHits(Range):
    """Number of Bowser Bomb hits required to defeat Bowser in the Fire Sea."""
    display_name = "Bowser in the Fire Sea Health"
    range_start = 1
    range_end = 4
    default = 1


class BowserInTheSkyHits(Range):
    """Number of Bowser Bomb hits required to defeat Bowser in the Sky."""
    display_name = "Bowser in the Sky Health"
    range_start = 1
    range_end = 5
    default = 3


class BowserInTheSkyStageCollapseHits(Range):
    """
    Number of hits Bowser must take before parts of the Bowser in the Sky arena fall off.
    """
    display_name = "Bowser in the Sky Stage Collapse Hits"
    range_start = 1
    range_end = 5
    default = 2


class BowserStage1Ups(Choice):
    """
    Choose how Bowser stage 1-Up objects that normally depend on Bowser key flags are handled.

    Vanilla - Two 1-Ups in Bowser in the Dark World require the Basement Key, and one 1-Up in Bowser in the Dark World
    plus two in Bowser in the Fire Sea require the Second Floor Key.

    Global - Shuffle one Bowser Stage Extra 1-Ups item that spawns all affected Bowser in the Dark World and Bowser in the
    Fire Sea 1-Ups.

    Per Level - Shuffle separate Bowser in the Dark World - Extra 1-Ups and Bowser in the Fire Sea - Extra 1-Ups items.

    Both - Shuffle the global Bowser Stage Extra 1-Ups item and both level-specific items.

    Always Spawn - All 1-Ups always spawn in the Bowser stages.
    """
    display_name = "Bowser Stage 1-Up Behavior"
    option_vanilla = 0
    option_global = 1
    option_per_level = 2
    alias_individual = 2
    option_always_spawn = 3
    option_both = 4
    default = 0


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


class UncollectRandomCoinTrapWeight(Range):
    """
    Relative weight for Uncollect Random Coin Traps.

    This trap randomly selects one previously collected coin and makes it collectible again. The reduced course total
    takes effect the next time the course is entered.

    Higher values make this trap appear more often.
    A weight of 0 disables this trap.
    """
    range_start = 0
    range_end = 100
    default = 0
    display_name = "Uncollect Random Coin Trap Weight"


trap_weight_options = (
    BonkTrapWeight,
    FireTrapWeight,
    ElectricTrapWeight,
    ChuckyaTrapWeight,
    SpinTrapWeight,
    GustTrapWeight,
    UncollectRandomCoinTrapWeight,
)

trap_weight_option_names = (
    "bonk_trap_weight",
    "fire_trap_weight",
    "electric_trap_weight",
    "chuckya_trap_weight",
    "spin_trap_weight",
    "gust_trap_weight",
    "uncollect_random_coin_trap_weight",
)

trap_item_name_by_option_name = {
    "bonk_trap_weight": "Bonk Trap",
    "fire_trap_weight": "Burn Trap",
    "electric_trap_weight": "Shock Trap",
    "chuckya_trap_weight": "Chuckya Trap",
    "spin_trap_weight": "Spin Trap",
    "gust_trap_weight": "Gust Trap",
    "uncollect_random_coin_trap_weight": "Uncollect Random Coin Trap",
}
class LogicTricks(OptionSet):
    """Choose specific advanced techniques to include in logic. The All Easy, All Medium, and All Hard entries
    include every trick at that difficulty and below. Details for each trick are documented in
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
    alias_individual = 2
    option_both = 3



class TripleJump(MoveRandomizerMode):
    """
    Choose how Triple Jump is handled.

    Not Shuffled - The game starts with Triple Jump unlocked.

    Global - Shuffle one Triple Jump item that unlocks the move everywhere.

    Per Level - Shuffle separate Triple Jump items for each main course. Castle, castle grounds, secret courses,
    cap stages, and Bowser stages use the Castle - Triple Jump item.

    Both - Shuffle the global Triple Jump item and every applicable level-specific Triple Jump item.
    """
    display_name = "Triple Jump"


class LongJump(MoveRandomizerMode):
    """
    Choose how Long Jump is handled.

    Not Shuffled - The game starts with Long Jump unlocked.

    Global - Shuffle one Long Jump item that unlocks the move everywhere.

    Per Level - Shuffle separate Long Jump items for each main course. Castle, castle grounds, secret courses,
    cap stages, and Bowser stages use the Castle - Long Jump item.

    Both - Shuffle the global Long Jump item and every applicable level-specific Long Jump item.
    """
    display_name = "Long Jump"


class Backflip(MoveRandomizerMode):
    """
    Choose how Backflip is handled.

    Not Shuffled - The game starts with Backflip unlocked.

    Global - Shuffle one Backflip item that unlocks the move everywhere.

    Per Level - Shuffle separate Backflip items for each main course. Castle, castle grounds, secret courses,
    cap stages, and Bowser stages use the Castle - Backflip item.

    Both - Shuffle the global Backflip item and every applicable level-specific Backflip item.
    """
    display_name = "Backflip"


class SideFlip(MoveRandomizerMode):
    """
    Choose how Side Flip is handled.

    Not Shuffled - The game starts with Side Flip unlocked.

    Global - Shuffle one Side Flip item that unlocks the move everywhere.

    Per Level - Shuffle separate Side Flip items for each main course. Castle, castle grounds, secret courses,
    cap stages, and Bowser stages use the Castle - Side Flip item.

    Both - Shuffle the global Side Flip item and every applicable level-specific Side Flip item.
    """
    display_name = "Side Flip"


class WallKick(MoveRandomizerMode):
    """
    Choose how Wall Kick is handled.

    Not Shuffled - The game starts with Wall Kick unlocked.

    Global - Shuffle one Wall Kick item that unlocks the move everywhere.

    Per Level - Shuffle separate Wall Kick items for each main course. Castle, castle grounds, secret courses,
    cap stages, and Bowser stages use the Castle - Wall Kick item.

    Both - Shuffle the global Wall Kick item and every applicable level-specific Wall Kick item.
    """
    display_name = "Wall Kick"


class Dive(MoveRandomizerMode):
    """
    Choose how Dive is handled.

    Not Shuffled - The game starts with Dive unlocked.

    Global - Shuffle one Dive item that unlocks the move everywhere.

    Per Level - Shuffle separate Dive items for each main course. Castle, castle grounds, secret courses,
    cap stages, and Bowser stages use the Castle - Dive item.

    Both - Shuffle the global Dive item and every applicable level-specific Dive item.
    """
    display_name = "Dive"


class GroundPound(MoveRandomizerMode):
    """
    Choose how Ground Pound is handled.

    Not Shuffled - The game starts with Ground Pound unlocked.

    Global - Shuffle one Ground Pound item that unlocks the move everywhere.

    Per Level - Shuffle separate Ground Pound items for each main course. Castle, castle grounds, secret courses,
    cap stages, and Bowser stages use the Castle - Ground Pound item.

    Both - Shuffle the global Ground Pound item and every applicable level-specific Ground Pound item.
    """
    display_name = "Ground Pound"


class Kick(MoveRandomizerMode):
    """
    Choose how Kick is handled.

    Not Shuffled - The game starts with Kick unlocked.

    Global - Shuffle one Kick item that unlocks the move everywhere.

    Per Level - Shuffle separate Kick items for each main course. Castle, castle grounds, secret courses,
    cap stages, and Bowser stages use the Castle - Kick item.

    Both - Shuffle the global Kick item and every applicable level-specific Kick item.
    """
    display_name = "Kick"


class Climb(MoveRandomizerMode):
    """
    Choose how Climb is handled.

    Not Shuffled - The game starts with Climb unlocked.

    Global - Shuffle one Climb item that unlocks the move everywhere.

    Per Level - Shuffle separate Climb items for each main course (Except Big Boo's Haunt which has no climbable objects).
    Castle, castle grounds, secret courses, cap stages, and Bowser stages use the Castle - Climb item.

    Both - Shuffle the global Climb item and every applicable level-specific Climb item.
    """
    display_name = "Climb"


class LedgeGrab(MoveRandomizerMode):
    """
    Choose how Ledge Grab is handled.

    Not Shuffled - The game starts with Ledge Grab unlocked.

    Global - Shuffle one Ledge Grab item that unlocks the move everywhere.

    Per Level - Shuffle separate Ledge Grab items for each main course. Castle, castle grounds, secret courses,
    cap stages, and Bowser stages use the Castle - Ledge Grab item.

    Both - Shuffle the global Ledge Grab item and every applicable level-specific Ledge Grab item.
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


class SkyboxShuffle(Choice):
    """
    Control the textured skybox used by each outdoor area.

    Off - Use vanilla skyboxes.

    Shuffle - Archipelago sends a deterministic per-area skybox map.

    Random on Load - The game picks a random skybox each time an area loads.
    """
    display_name = "Skybox Shuffle"
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
        LevelUnlocks,
        CapItems,
        LogicTricks,
        UniversalTrackerGlitchedLogic,
    ]),
    OptionGroup("Level Feature Unlocks", [
        LevelFeatures,
        BobombBuddies,
        CoinObjectUnlocks,
        EnemyUnlocks,
        OneUpUnlocks,
        SignUnlocks,
        BowserBombs,
        BowserStage1Ups,
    ]),
    OptionGroup("Coin Options", [
        CoinChecks,
        CoinCountChecks,
        *secret_stage_coin_count_max_coin_options,
        *coin_star_requirement_options,
    ]),
    OptionGroup("Gameplay Options", [
        MariosHat,
        BowserInTheDarkWorldHits,
        BowserInTheFireSeaHits,
        BowserInTheSkyHits,
        BowserInTheSkyStageCollapseHits,
    ]),
    OptionGroup("Ability Options", [
        *move_randomizer_options,
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
        SkyboxShuffle,
    ]),

]

@dataclass
class SM64Options(PerGameCommonOptions):
    accessibility: SM64Accessibility
    area_rando: AreaRandomizer
    buddy_checks: BuddyChecks
    one_up_checks: OneUpChecks
    blocksanity: Blocksanity
    easy_butterflies: EasyButterflies
    no_despawns: NoDespawns
    combined_progressive_keys: CombinedProgressiveKeys
    level_unlocks: LevelUnlocks
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
    cap_items: CapItems
    level_features: LevelFeatures
    bobomb_buddies: BobombBuddies
    coin_object_unlocks: CoinObjectUnlocks
    enemy_unlocks: EnemyUnlocks
    one_up_unlocks: OneUpUnlocks
    sign_unlocks: SignUnlocks
    bowser_bombs: BowserBombs
    bowser_in_the_dark_world_health: BowserInTheDarkWorldHits
    bowser_in_the_fire_sea_health: BowserInTheFireSeaHits
    bowser_in_the_sky_health: BowserInTheSkyHits
    bowser_in_the_sky_stage_collapse_hits: BowserInTheSkyStageCollapseHits
    bowser_stage_1ups: BowserStage1Ups
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
    skybox_shuffle: SkyboxShuffle
    coin_checks: CoinChecks
    coin_count_checks: CoinCountChecks
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
    princess_secret_slide_coin_count_max_coins: PrincessSecretSlideCoinCountMaxCoins
    secret_aquarium_coin_count_max_coins: SecretAquariumCoinCountMaxCoins
    wing_mario_over_the_rainbow_coin_count_max_coins: WingMarioOverTheRainbowCoinCountMaxCoins
    tower_of_the_wing_cap_coin_count_max_coins: TowerOfTheWingCapCoinCountMaxCoins
    vanish_cap_under_the_moat_coin_count_max_coins: VanishCapUnderTheMoatCoinCountMaxCoins
    cavern_of_the_metal_cap_coin_count_max_coins: CavernOfTheMetalCapCoinCountMaxCoins
    bowser_in_the_dark_world_coin_count_max_coins: BowserInTheDarkWorldCoinCountMaxCoins
    bowser_in_the_fire_sea_coin_count_max_coins: BowserInTheFireSeaCoinCountMaxCoins
    bowser_in_the_sky_coin_count_max_coins: BowserInTheSkyCoinCountMaxCoins
    traps_filler_percentage: TrapsFillerPercentage
    bonk_trap_weight: BonkTrapWeight
    fire_trap_weight: FireTrapWeight
    electric_trap_weight: ElectricTrapWeight
    chuckya_trap_weight: ChuckyaTrapWeight
    spin_trap_weight: SpinTrapWeight
    gust_trap_weight: GustTrapWeight
    uncollect_random_coin_trap_weight: UncollectRandomCoinTrapWeight
    death_link: DeathLink
    completion_type: CompletionType
