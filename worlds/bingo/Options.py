import typing
from Options import Choice, Option, Toggle, Range, OptionList, DeathLink


class CardPairs(Range):
    """How many pairs of Bingo cards."""
    display_name = "Card Pairs"
    range_start = 1
    range_end = 4
    default = 4


class RevealRewards(Toggle):
    """Start with all Bingo rewards hinted."""
    display_name = "Reveal Rewards"
    default = 1


bingo_options: typing.Dict[str, type(Option)] = {
    "card_pairs": CardPairs,
    "reveal_rewards": RevealRewards
}