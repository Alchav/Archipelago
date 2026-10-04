from worlds.AutoWorld import World, data_package_checksum
import copy

from BaseClasses import ItemClassification, Item, Location, Region
from NetUtils import SlotType
from Options import PerGameCommonOptions, OptionList, Owner, OptionDict
from dataclasses import dataclass


HINT_POINT_ITEM_ID_BASE = 1_000_000
HINT_POINT_ITEM_ID_OWNER_STRIDE = 100
CUSTOM_ITEM_ID_BASE = 2_000_000
CUSTOM_LOCATION_ID_BASE = 2_000_000

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
        "Leigh Hint Point": 1014,
        "Leigh SDV Hint Point": 1015,
        "Nothing": 100000
    }

    location_name_to_id = {}
    options_dataclass = AlchapelaOptions
    options: AlchapelaOptions

    def generate_early(self):
        # This world has seed-specific items and locations. Never leak them into a
        # later generation through the class-level datapackage dictionaries.
        self.item_name_to_id = type(self).item_name_to_id.copy()
        self.item_id_to_name = {item_id: name for name, item_id in self.item_name_to_id.items()}
        self.location_name_to_id = {}
        self.location_id_to_name = {}
        self.item_name_groups = {
            name: set(items) for name, items in type(self).item_name_groups.items()
        }
        self.custom_item_triggers = {}
        self.custom_item_aliases = {}
        self.custom_item_owners = {}
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

    def create_regions(self):
        self.multiworld.regions.append(Region(self.origin_region_name, self.player, self.multiworld))

    def post_fill(self) -> None:
        pass

    def create_item(self, name):
        return UnlockItem(name, ItemClassification.progression if "Unlock" in name else ItemClassification.filler, self.item_name_to_id[name], self.player)

    def create_custom_item(self, name: str, classification: ItemClassification):
        # Triggers participate in logic even when every bundled item is filler or
        # useful, so they must always be collected into CollectionState.
        return UnlockItem(name, classification | ItemClassification.progression,
                          self.item_name_to_id[name], self.player)

    def register_custom_item(self, name: str, item_id: int, native_game: str, owner: int) -> None:
        self.item_name_to_id[name] = item_id
        self.item_id_to_name[item_id] = name
        self.item_name_groups.setdefault("Everything", set()).add(name)
        self.custom_item_aliases.setdefault(native_game, {})[name] = item_id
        self.custom_item_owners[item_id] = owner

    def register_custom_location(self, name: str, location_id: int) -> None:
        self.location_name_to_id[name] = location_id
        self.location_id_to_name[location_id] = name

    def fill_slot_data(self):
        return {"custom_item_triggers": self.custom_item_triggers}

    def modify_multidata(self, multidata):
        packages = multidata["datapackage"]
        bot_package = {
            "item_name_groups": {
                name: sorted(items) for name, items in sorted(self.item_name_groups.items())
            },
            "item_name_to_id": dict(self.item_name_to_id),
            "location_name_groups": {},
            "location_name_to_id": dict(self.location_name_to_id),
        }
        bot_package["checksum"] = data_package_checksum(bot_package)
        packages[self.game] = bot_package

        for game, aliases in self.custom_item_aliases.items():
            package = copy.deepcopy(packages[game])
            package["item_name_to_id"].update(aliases)
            package.pop("checksum", None)
            package["checksum"] = data_package_checksum(package)
            packages[game] = package

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
