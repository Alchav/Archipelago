from dataclasses import dataclass

from typing import Dict

from Options import Choice, Option, DefaultOnToggle, Toggle, Range, OptionList, StartInventoryPool, DeathLink, PerGameCommonOptions


class LogicDifficulty(Choice):
    """Set the logic difficulty used when generating."""
    display_name = "Logic Difficulty"
    option_easy = 0
    option_normal = 1
    #option_obscure_glitchless = 2
    #option_glitched = 3
    option_no_logic = 4
    default = 0


class CAMC(DefaultOnToggle):
    """Set whether chest appearance matches contents."""
    display_name = "CAMC"


class Swordless(Toggle):
    """Start the game without a sword, and shuffle an extra Progressive Sword into the pool."""
    display_name = "Swordless"


class Shieldless(Toggle):
    """Start the game without a shield, and shuffle an extra Progressive Shield into the pool."""
    display_name = "Shieldless"


class StartWithSoaring(DefaultOnToggle):
    """Start the game with Song of Soaring."""
    display_name = "Start With Soaring"


class StartingHeartQuarters(Range):
    """The number of heart quarters Link starts with.
    If less than 12, extra heart items will be shuffled into the pool to accommodate."""
    display_name = "Starting Hearts"
    range_start = 4
    range_end = 12
    default = 12


class StartingHeartsAreContainersOrPieces(Choice):
    """Choose whether Link's starting hearts are shuffled into the pool as Heart Containers (plus the remainder as Heart Pieces) or as all Heart Pieces."""
    display_name = "Starting Hearts are Containers or Pieces"
    option_containers = 0
    option_pieces = 1
    default = 0

class ShuffleRegionalMaps(Choice):
    """Choose whether to shuffle every regional map from Tingle."""
    display_name = "Shuffle Regional Maps"
    option_vanilla = 0
    option_starting = 1
    option_anywhere = 2
    default = 1


class ShuffleBossRemains(Choice):
    """Choose whether to shuffle the Boss Remains received after beating a boss at the end of a dungeon.
    
    vanilla: Boss Remains are placed in their vanilla locations.
    anything: Any item can be given by any of the Boss Remains, and Boss Remains can be found anywhere in any world.
    bosses: Boss Remains are shuffled amongst themselves as the rewards for defeating bosses."""
    display_name = "Shuffle Boss Remains"
    option_vanilla = 0
    option_anywhere = 1
    option_bosses = 2
    default = 0


class ShuffleSwamphouseReward(Toggle):
    """Choose whether to shuffle the Mask of Truth given at the end of the Southern Swamphouse."""
    display_name = "Shuffle Swamphouse Reward"


class Skullsanity(Choice):
    """Choose what items gold skulltulas can give.
    
    vanilla: Keep the swamphouse in generation, but only place Skulltula tokens there.
    anything: Any item can be given by any Skulltula, and tokens can be found anywhere in any world.
    ignore: Remove the swamphouse from generation entirely, lowering the hint percentage."""
    display_name = "Skullsanity"
    option_vanilla = 0
    option_anything = 1
    option_ignore = 2
    default = 0


class Shopsanity(Choice):
    """Choose whether shops and their items are shuffled into the pool.
    This includes Trading Post, Bomb Shop, Goron Shop, and Zora Shop, along with the Gorman Ranch and Milk Bar purchases.
    
    vanilla: Shop items are not shuffled.
    enabled: Every item in shops are shuffled, with alternate shops sharing the same items.
    advanced: Every single item in shops are shuffled, including the alternate Night Trading Post and Spring Goron Shop. Also adds an extra Heart Piece to Spring Goron Village."""
    display_name = "Shopsanity"
    option_vanilla = 0
    option_enabled = 1
    option_advanced = 2
    default = 0


class Scrubsanity(Toggle):
    """Choose whether to shuffle Business Scrub purchases."""
    display_name = "Shuffle Business Scrub Purchases"

class Cowsanity(Toggle):
    """Choose whether to shuffle Cows."""
    display_name = "Shuffle Cows"


class ShuffleGreatFairyRewards(Toggle):
    """Choose whether to shuffle Great Fairy rewards."""
    display_name = "Shuffle Great Fairy Rewards"


class Fairysanity(Toggle):
    """Choose whether Stray Fairies are shuffled into the pool."""
    display_name = "Fairysanity"


class StartWithConsumables(DefaultOnToggle):
    """Choose whether to start with basic consumables (99 rupees, 10 deku sticks, 20 deku nuts)."""
    display_name = "Start With Consumables"


class PermanentChateauRomani(DefaultOnToggle):
    """Choose whether the Chateau Romani stays even after a reset."""
    display_name = "Permanent Chateau Romani"


class StartWithInvertedTime(Toggle):
    """Choose whether time starts out inverted at Day 1, even after a reset."""
    display_name = "Reset With Inverted Time"


class ReceiveFilledWallets(DefaultOnToggle):
    """Choose whether you receive wallets pre-filled (not including the starting wallet)."""
    display_name = "Receive Filled Wallets"


class DamageMultiplier(Choice):
    """Adjust the amount of damage taken."""
    display_name = "Damage Multiplier"
    option_half = 0
    option_normal = 1
    option_double = 2
    option_quad = 3
    option_ohko = 4
    default = 1

class DeathBehavior(Choice):
    """Change what happens when you die.
    
    vanilla: The normal death cutscene plays when you die.
    fast: The death cutscene is massively sped up.
    moon_crash: Triggers a moon crash and restarts the current cycle."""
    display_name = "Death Behavior"
    option_vanilla = 0
    option_fast = 1
    option_moon_crash = 2
    default = 0


class LinkTunicColor(OptionList):
    """Choose a color for Link's tunic."""
    display_name = "Link Tunic Color"
    default = [30, 105, 27]


@dataclass
class MMROptions(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    logic_difficulty: LogicDifficulty
    camc: CAMC
    swordless: Swordless
    shieldless: Shieldless
    start_with_soaring: StartWithSoaring
    starting_hearts: StartingHeartQuarters
    starting_hearts_are_containers_or_pieces: StartingHeartsAreContainersOrPieces
    shuffle_regional_maps: ShuffleRegionalMaps
    shuffle_boss_remains: ShuffleBossRemains
    shuffle_swamphouse_reward: ShuffleSwamphouseReward
    skullsanity: Skullsanity
    shopsanity: Shopsanity
    scrubsanity: Scrubsanity
    cowsanity: Cowsanity
    shuffle_great_fairy_rewards: ShuffleGreatFairyRewards
    fairysanity: Fairysanity
    start_with_consumables: StartWithConsumables
    permanent_chateau_romani: PermanentChateauRomani
    start_with_inverted_time: StartWithInvertedTime
    receive_filled_wallets: ReceiveFilledWallets
    damage_multiplier: DamageMultiplier
    death_behavior: DeathBehavior
    death_link: DeathLink
    link_tunic_color: LinkTunicColor
