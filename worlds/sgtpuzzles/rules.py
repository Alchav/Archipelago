from math import ceil
from worlds.generic.Rules import set_rule
from BaseClasses import LocationProgressType, MultiWorld
from .items import max_puzzles
from .options import SimonTathamPuzzlesOptions


# Sets rules on entrances and advancements that are always applied
def set_rules(multiworld: MultiWorld, player: int, puzzles: list[str]):
    for i in range(max_puzzles):
        if i < len(puzzles):
            set_rule(multiworld.get_location(f"Puzzle {i+1} Reward", player), lambda state, i=i: state.has(f"Puzzle {i+1}", player, 1))


# Sets rules on completion condition
def set_completion_rules(multiworld: MultiWorld, player: int, target_puzzles: int):
    multiworld.completion_condition[player] = lambda state: state.has_from_list_unique(
        [f"Puzzle {i+1}" for i in range(max_puzzles)], player, target_puzzles)
