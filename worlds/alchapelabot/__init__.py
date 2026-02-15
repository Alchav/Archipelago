from worlds.AutoWorld import World
from BaseClasses import ItemClassification, Item
from NetUtils import SlotType
from Options import PerGameCommonOptions, OptionList, Owner, OptionDict
from dataclasses import dataclass

allowed_filler_games = {
    "Secret of Evermore", "Super Mario 64", "Crystalis", "DOOM 1993", "DOOM II", "Final Fantasy Mystic Quest",
    "A Hat in Time", "Pokemon Red and Blue", "The Sims 4", "Jigsaw", "Majora's Mask Recompiled",
    "A Link to the Past", "Super Mario World", "Final Fantasy V", "AlchapelaBot"
}


class StartGames(OptionList):
    """Starting games"""
    default = []


class HintCount(OptionDict):
    default = {}


@dataclass
class AlchapelaOptions(PerGameCommonOptions):
    start_games: StartGames
    hint_count: HintCount


class AlchapelaBotWorld(World):
    game = "AlchapelaBot"
    topology_present = False
    item_name_to_id = {
        "Alchav Hint Point": 1000,
        "Alchav Alt Hint Point": 1001,
        "AvBW Hint Point": 1002,
        "AvBW Jigsaw Hint Point": 1003,
        "Jack Hint Point": 1004,
        "Jack Jigsaw Hint Point": 1005,
        "Alyssa Hint Point": 1006,
        "Alyssa Jigsaw Hint Point": 1007,
        "Auto Hint Point": 1008,
        "Ophilla Hint Point": 1010,
        "Alchav Valley Hint Point": 1011,
        "Alchav Hint Location Point": 10000,
        "Alchav Alt Hint Location Point": 10001,
        "AvBW Hint Location Point": 10002,
        "AvBW Jigsaw Hint Location Point": 10003,
        "Jack Hint Location Point": 10004,
        "Jack Jigsaw Hint Location Point": 10005,
        "Alyssa Hint Location Point": 10006,
        "Alyssa Jigsaw Hint Location Point": 10007,
        "Auto Hint Location Point": 10008,
        "Ophilla Hint Location Point": 10010,
        "Alchav Valley Hint Location Point": 10011,
        "Nothing": 100000
    }

    location_name_to_id = {}
    options_dataclass = AlchapelaOptions
    options: AlchapelaOptions

    def generate_early(self):
        self.multiworld.player_types[self.player] = SlotType.spectator  # mark as spectator
        for player, player_name in self.multiworld.player_name.items():
            self.item_name_to_id[f"Unlock {player_name}"] = player
            self.item_id_to_name[player] = f"Unlock {player_name}"
            # self.item_name_to_id[f"{player_name} Hint Point"] = player + 1000
            # self.item_name_to_id[f"{player_name} Hint Location Point"] = player + 10000
            # self.item_id_to_name[player + 1000] = f"{player_name} Hint Point"
            # self.item_id_to_name[player + 10000] = f"{player_name} Hint Location Point"
            # self.options.start_hints.value.add(f"Unlock {player_name}")
        for starting_game in self.options.start_games.value:
            try:
                self.multiworld.push_precollected(self.create_item(f"Unlock {starting_game}"))
            except Exception:
                pass
        self.item_name_groups["Everything"] = set(self.item_name_to_id.keys())

    def post_fill(self) -> None:
        allowed_filler_slots = [player for player in self.multiworld.player_ids if self.multiworld.worlds[player].game in allowed_filler_games]
        for location in self.multiworld.get_unfilled_locations():
            player = self.random.choice(allowed_filler_slots)
            self.multiworld.push_item(location, self.multiworld.worlds[player].create_filler())

    def create_item(self, name):
        return UnlockItem(name, ItemClassification.progression if "Unlock" in name else ItemClassification.filler, self.item_name_to_id[name], self.player)

    def get_filler_item_name(self) -> str:
        return "Nothing"

class UnlockItem(Item):
    game = "AlchapelaBot"
