from dataclasses import dataclass

from typing import Dict

from Options import Choice, Option, DefaultOnToggle, Toggle, Range, OptionList, StartInventoryPool, DeathLink, PerGameCommonOptions


class LogicDifficulty(Choice):
    """Set the logic difficulty used when generating."""
    display_name = "Logic Difficulty"
    option_easy = 0
    #option_normal = 1
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


class ShuffleBossRemains(Choice):
    """Choose whether to shuffle the Boss Remains received after beating a boss at the end of a dungeon.
    
    vanilla: Boss Remains are placed in their vanilla locations.
    anything: Any item can be given by any of the Boss Remains, and Boss Remains can be found anywhere in any world.
    bosses: Boss Remains are shuffled amongst themselves as the rewards for defeating bosses."""
    display_name = "Shuffle Boss Remains"
    option_vanila = 0
    option_anywhere = 1
    option_bosses = 2
    default = 1


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


class ShuffleGreatFairyRewards(Toggle):
    """Choose whether to shuffle Great Fairy rewards."""
    display_name = "Shuffle Great Fairy Rewards"


class Fairysanity(Toggle):
    """Choose whether Stray Fairies are shuffled into the pool."""
    display_name = "Fairysanity"


class StartWithConsumables(Toggle):
    """Choose whether to start with basic consumables (99 rupees, 10 deku sticks, 20 deku nuts)."""
    display_name = "Start With Consumables"


class PermanentChateauRomani(Toggle):
    """Choose whether the Chateau Romani stays even after a reset."""
    display_name = "Permanent Chateau Romani"


class ResetWithInvertedTime(Toggle):
    """Choose whether time starts out inverted at Day 1, even after a reset."""
    display_name = "Reset With Inverted Time"


class ReceiveFilledWallets(Toggle):
    """Choose whether you receive wallets pre-filled (not including the starting wallet)."""
    display_name = "Receive Filled Wallets"


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
    starting_hearts: StartingHeartQuarters
    starting_hearts_are_containers_or_pieces: StartingHeartsAreContainersOrPieces
    shuffle_boss_remains: ShuffleBossRemains
    shuffle_swamphouse_reward: ShuffleSwamphouseReward
    skullsanity: Skullsanity
    shuffle_great_fairy_rewards: ShuffleGreatFairyRewards
    fairysanity: Fairysanity
    start_with_consumables: StartWithConsumables
    permanent_chateau_romani: PermanentChateauRomani
    reset_with_inverted_time: ResetWithInvertedTime
    receive_filled_wallets: ReceiveFilledWallets
    death_link: DeathLink
    link_tunic_color: LinkTunicColor
