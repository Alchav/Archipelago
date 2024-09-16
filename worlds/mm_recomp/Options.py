from typing import Dict

from Options import Choice, Option, Toggle, StartInventoryPool, DeathLink


#class HardMode(Toggle):
#    """Only for the most masochistically inclined... Requires button activation!"""
#    display_name = "Hard Mode"


#class ButtonColor(Choice):
#    """Customize your button! Now available in 12 unique colors."""
#    display_name = "Button Color"
#    option_red = 0
#    option_orange = 1
#    option_yellow = 2
#    option_green = 3
#    option_cyan = 4
#    option_blue = 5
#    option_magenta = 6
#    option_purple = 7
#    option_pink = 8
#    option_brown = 9
#    option_white = 10
#    option_black = 11


class LogicDifficulty(Choice):
    """Set the logic difficulty used when generating."""
    display_name = "Logic Difficulty"
    option_easy = 0
    option_no_logic = 4
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


class ShuffleGreatFairyRewards(Toggle):
    """Choose whether to shuffle Great Fairy rewards."""
    display_name = "Shuffle Great Fairy Rewards"


class Fairysanity(Toggle):
    """Choose whether Stray Fairies are shuffled into the pool."""
    display_name = "Fairysanity"


mmr_options: Dict[str, type(Option)] = {
    "start_inventory_from_pool": StartInventoryPool,
    "logic_difficulty": LogicDifficulty,
    "shuffle_swamphouse_reward": ShuffleSwamphouseReward,
    "skullsanity": Skullsanity,
    "shuffle_great_fairy_rewards": ShuffleGreatFairyRewards,
    "fairysanity": Fairysanity,
    "death_link": DeathLink
}
