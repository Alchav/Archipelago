from dataclasses import dataclass
from Options import Toggle, Range, Choice, PerGameCommonOptions


class TextSpeed(Choice):
    """
    Text Speed.
    Instant: Text renders an entire window at a time.
    Fast: Text renders a character at a time at the same speed as the JP version.
    """

    display_name = "Text Speed"
    option_fast = 0
    option_instant = 1
    default = 1


class Goal(Choice):
    """
    How you beat the game.
    Deathtoll: Defeat Deathtoll.
    Emblem Hunt: Collect all 8 master's emblems and turn them in at the Gem Fairy in Greenwood.
    """

    display_name = "Goal"
    option_deathtoll = 0
    option_emblem_hunt = 1
    default = 0


class StonesPlacement(Choice):
    """
    Determines the placement of the 6 stones needed to enter the World of Evil.
    Vanilla: Stones are given by the town leader of each act.
    Bosses: Stones are rewarded from the boss lair of each act.
    Random: Stones are randomized with everything else.
    """

    display_name = "Stones Placement"
    option_vanilla = 0
    option_bosses = 1
    option_random = 2
    default = 0


class StonesCount(Range):
    """
    Number of Stones needed to open the World of Evil.
    """

    display_name = "Stones Count"
    range_start = 0
    range_end = 6
    default = 6


class StartingSword(Choice):
    """
    Determines the sword you will get in the first chest.
    Vanilla: You will get the Sword of Life.
    Randomized: You will get a random sword.
    """

    display_name = "Starting Sword"
    option_vanilla = 0
    option_randomized = 1
    default = 0


class EquipmentStats(Choice):
    """
    Determines equipment power & defense.
    Vanilla: No change to the way Weapons/Armor work.
    Semi-progressive: Equipment strength/defense scales with the number of swords/armors obtained.
    Shuffle: Shuffles the stats of all swords and armor.
    """

    display_name = "Equipment Stats"
    option_vanilla = 0
    option_semi_progressive = 1
    option_shuffle = 2
    default = 1


class EquipmentScaling(Choice):
    """
    Determines the stat progression for swords/armor.
    Vanilla: Swords/Armor follow the vanilla 1/2/3/4/6/8/10/12 strength/defense progression.
    Improved: Swords/Armor follow an improved 1/3/5/7/9/12/12/12 strength/defense progression.
    Strong: Swords/Armor follow a strong 1/3/6/9/12/12/12/12 strength/defense progression.
    """

    display_name = "Equipment Scaling"
    option_vanilla = 0
    option_improved = 1
    option_strong = 2
    default = 0


class MagicianItem(Choice):
    """
    Determines the item the Magician gives you at the start of the game.
    Vanilla: The vanilla reward (Fireball).
    Random Spell: A random castable magic spell.
    Totally Random: Any reward in the item pool.
    """

    display_name = "Magician's Item"
    option_vanilla = 0
    option_random_spell = 1
    option_totally_random = 2
    default = 1


class MagicianSoul(Choice):
    """
    Determines what reward you will get in place of the Magician's Soul at the start of the game.
    Vanilla: You get the Soul of Magician.
    Random Soul: Any progression soul. (Soul of Magician, Soul of Light, Soul of Detection)
    Totally Random: Any reward in the item pool.
    """

    display_name = "Magician's Soul"
    option_vanilla = 0
    option_random_soul = 1
    option_totally_random = 2
    default = 0


class GemExpPool(Choice):
    """
    Modifies the Gem/Exp rewards in the item pool.
    Vanilla: The same Gem/Exp values as the vanilla game.
    Improved: Gem rewards in the item pool are multiplied by 2, and Exp rewards by 10.
    Random: Gem rewards in the pool are randomized in the range of 1-999, and Exp rewards in the range of 1-9999.
    """

    display_name = "GEM/Exp Pool"
    option_vanilla = 0
    option_improved = 1
    option_random = 2


# By convention, we call the options dataclass `<world>Options`.
# It has to be derived from 'PerGameCommonOptions'.
@dataclass
class SoulBlazerOptions(PerGameCommonOptions):
    text_speed: TextSpeed
    goal: Goal
    stones_placement: StonesPlacement
    stones_count: StonesCount
    starting_sword: StartingSword
    equipment_Stats: EquipmentStats
    equipment_scaling: EquipmentScaling
    magician_item: MagicianItem
    magician_soul: MagicianSoul
    gem_exp_pool: GemExpPool
