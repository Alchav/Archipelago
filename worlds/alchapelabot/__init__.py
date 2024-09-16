from worlds.AutoWorld import World
from BaseClasses import ItemClassification, Item
from NetUtils import SlotType
from Options import PerGameCommonOptions, OptionList
from dataclasses import dataclass


class StartGames(OptionList):
    """Starting games"""
    default = []


@dataclass
class AlchapelaOptions(PerGameCommonOptions):
    start_games: StartGames


class AlchapelaBotWorld(World):
    game = "AlchapelaBot"
    topology_present = False
    item_name_to_id = {}
    location_name_to_id = {}
    options_dataclass = AlchapelaOptions
    options: AlchapelaOptions

    def generate_early(self):
        self.multiworld.player_types[self.player] = SlotType.spectator  # mark as spectator
        for player, player_name in self.multiworld.player_name.items():
            self.item_name_to_id[f"Unlock {player_name}"] = player
            self.item_id_to_name[player] = f"Unlock {player_name}"
        for starting_game in self.options.start_games.value:
            self.multiworld.push_precollected(self.create_item(f"Unlock {starting_game}"))

    def create_item(self, name):
        return Item(name, ItemClassification.progression, self.item_name_to_id[name], self.player)
