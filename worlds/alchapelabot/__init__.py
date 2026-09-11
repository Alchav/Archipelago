from worlds.AutoWorld import World
from BaseClasses import ItemClassification, Item
from NetUtils import SlotType
from Options import PerGameCommonOptions, OptionList, Owner, OptionDict
from dataclasses import dataclass


HINT_POINT_ITEM_ID_BASE = 1_000_000
HINT_POINT_ITEM_ID_OWNER_STRIDE = 100

allowed_filler_games = {
    "Secret of Evermore", "Super Mario 64", "Crystalis", "DOOM 1993", "DOOM II", "Final Fantasy Mystic Quest",
    "A Hat in Time", "Pokemon Red and Blue", "The Sims 4", "Jigsaw", "Majora's Mask Recompiled",
    "A Link to the Past", "Super Mario World", "Final Fantasy V", "AlchapelaBot"
}


class StartGames(OptionList):
    """Starting games"""
    default = []


class HintCount(OptionDict):
    """Number of purchasable hints for each owner (for example, ``Ophilla Hint: 50``).

    Point items are divided among the spheres containing that owner's locations.
    Legacy ``Hint Location`` entries are folded into the corresponding owner's total.
    """
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
        "Factorio Hint Point": 1011,
        "Alchav64 Hint Point": 1012,
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
        pass

    def create_item(self, name):
        return UnlockItem(name, ItemClassification.progression if "Unlock" in name else ItemClassification.filler, self.item_name_to_id[name], self.player)

    def create_hint_point_item(self, owner: int, amount: int):
        """Create an owner hint item whose value is carried by its name and ID."""
        base_name = self.item_id_to_name[owner + 1000].removesuffix(" Point")
        name = f"{amount} {base_name} Point{'s' if amount != 1 else ''}"
        item_id = HINT_POINT_ITEM_ID_BASE + amount * HINT_POINT_ITEM_ID_OWNER_STRIDE + owner
        existing_name = self.item_id_to_name.get(item_id)
        if existing_name is not None and existing_name != name:
            raise ValueError(f"Hint point item ID collision between {existing_name!r} and {name!r}")
        self.item_name_to_id[name] = item_id
        self.item_id_to_name[item_id] = name
        return self.create_item(name)

    def get_filler_item_name(self) -> str:
        return "Nothing"

class UnlockItem(Item):
    game = "AlchapelaBot"
