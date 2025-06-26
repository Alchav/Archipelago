from worlds.AutoWorld import World
from BaseClasses import ItemClassification, Item
from NetUtils import SlotType
from Options import PerGameCommonOptions, OptionList
from dataclasses import dataclass

allowed_filler_games = {
    "Secret of Evermore", "Super Mario 64", "Crystalis", "DOOM 1993", "DOOM II", "Final Fantasy Mystic Quest",
    "A Hat in Time", "Pokemon Red and Blue", "The Sims 4", "Jigsaw", "Majora's Mask Recompiled",
    "A Link to the Past", "Super Mario World", "Final Fantasy V", "AlchapelaBot"
}

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
        self.item_name_to_id["Nothing"] = 100000
        self.multiworld.player_types[self.player] = SlotType.spectator  # mark as spectator
        for player, player_name in self.multiworld.player_name.items():
            self.item_name_to_id[f"Unlock {player_name}"] = player
            self.item_id_to_name[player] = f"Unlock {player_name}"
            self.item_name_to_id[f"{player_name} Hint Point"] = player + 1000
            self.item_id_to_name[player + 1000] = f"{player_name} Hint Point"
            self.options.start_hints.value.add(f"Unlock {player_name}")
        for starting_game in self.options.start_games.value:
            self.multiworld.push_precollected(self.create_item(f"Unlock {starting_game}"))
        self.item_name_groups["Everything"] = set(self.item_name_to_id.keys())

    def post_fill(self) -> None:
        allowed_filler_slots = [player for player in self.multiworld.player_ids if self.multiworld.worlds[player].game in allowed_filler_games]
        for location in self.multiworld.get_unfilled_locations():
            player = self.random.choice(allowed_filler_slots)
            self.multiworld.push_item(location, self.multiworld.worlds[player].create_filler())

    def create_item(self, name):
        return UnlockItem(name, ItemClassification.filler if name == "Nothing" else ItemClassification.progression if "Unlock" in name else ItemClassification.useful, self.item_name_to_id[name], self.player)

    def get_filler_item_name(self) -> str:
        return "Nothing"

class UnlockItem(Item):
    game = "AlchapelaBot"
