from typing import Dict, Any

from BaseClasses import Location, Region, Item, ItemClassification, LocationProgressType
from worlds.AutoWorld import World, WebWorld

start_ids = 9990000

from worlds.LauncherComponents import Component, SuffixIdentifier, Type, components, launch_subprocess
def launch_client(*args) -> None:
    from .client import launch
    launch_subprocess(launch, name="BingoClient")

component = Component("Bingo Client", "BingoClient", component_type=Type.CLIENT, func=launch_client,
                      file_identifier=SuffixIdentifier())
components.append(component)


def bingo_letter(i):
    return 'B' if i <= 15 else 'I' if i <= 30 else 'N' if i <= 45 else 'G' if i <= 60 else 'O'

class Bingo(World):
    game = "Bingo"
    item_name_to_id = {f"{bingo_letter(i)}-{i}": (start_ids + i) for i in range(1, 76)}
    location_name_to_id = {}
    id = start_ids
    for card in range(1, 9):
        for i in range(1, 6):
            location_name_to_id[f"Bingo Card {card} - Horizontal {i}"] = id
            id += 1
        for i in range(1, 6):
            location_name_to_id[f"Bingo Card {card} - Vertical {i}"] = id
            id += 1
        for i in range(1, 3):
            location_name_to_id[f"Bingo Card {card} - Diagonal {i}"] = id
            id += 1

    def __init__(self, multiworld, player):
        self.cards = None
        super().__init__(multiworld, player)

    def create_regions(self) -> None:
        menu = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu)
        menu.locations = [Location(self.player, location_name, location_id, menu) for location_name, location_id in self.location_name_to_id.items()]
        self.cards = [[self.multiworld.random.sample(r, 5) for r in (range(1, 16), range(16, 31), range(31, 46), range(46, 61), range(61, 76))] for _ in range(1, 9)]
        for card in self.cards:
            card[2][2] = 0

    def set_rules(self) -> None:
        for location in self.multiworld.get_region("Menu", self.player).locations:
            location.progress_type = LocationProgressType.PRIORITY
            location.item_rule = lambda item: item.game != "Bingo"
            card = int(location.name.split(" ")[2]) - 1
            n = int(location.name.split(" ")[5]) - 1
            line_type = location.name.split(" ")[4]
            if line_type == "Horizontal":
                coords = [(i, n) for i in range(5)]
                # location.access_rule = lambda state: state.has_all([f"Bingo Call {bingo_letter(self.cards[card][r][n])}-{self.cards[card][r][n]}" for r in range(1, 6)], self.player)
            elif line_type == "Vertical":
                coords = [(n, i) for i in range(5)]
                # location.access_rule = lambda state: state.has_all([f"Bingo Call {bingo_letter(self.cards[card][n][r])}-{self.cards[card][n][r]}" for r in range(1, 6)], self.player)
            elif line_type == "Diagonal":
                if n == 0:
                    coords = [(i, i) for i in range(5)]
                else:
                    coords = [(i, 4-i) for i in range(5)]
            location.access_rule = lambda state, card=card, coords=coords: state.has_all([f"{bingo_letter(self.cards[card][c[0]][c[1]])}-{self.cards[card][c[0]][c[1]]}" for c in coords if self.cards[card][c[0]][c[1]] != 0], self.player)

    def create_item(self, name):
        return BingoItem(name, ItemClassification.progression, self.item_name_to_id[name], self.player)

    def create_items(self):
        for item in self.item_name_to_id.keys():
            self.multiworld.itempool.append(self.create_item(item))
        self.multiworld.itempool += [self.create_item(item) for item in self.multiworld.random.sample(list(self.item_name_to_id.keys()), 21)]

    def write_spoiler(self, spoiler_handle) -> None:
        spoiler_handle.write(f'\n\nBingo Cards ({self.multiworld.player_name[self.player]}):\n')
        for card in self.cards:
            spoiler_handle.write(f"Card {card}:\n")
            for row in range(5):
                spoiler_handle.write(f"\n")
                for column in range(5):
                    if card[column][row] == 0:
                        spoiler_handle.write("   ")
                    else:
                        spoiler_handle.write(f"{card[column][row]}".zfill(2) + " ")
            spoiler_handle.write(f"\n")

    def fill_slot_data(self):
        return {"cards": self.cards}

    # def extend_hint_information(self, hint_data: Dict[int, Dict[int, str]]):
    #     for location in self.multiworld.get_region("Menu", self.player).locations:



class BingoItem(Item):
    game = "Bingo"
