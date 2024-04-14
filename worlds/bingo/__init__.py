from typing import Dict, Any, List

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
    hint_blacklist = {item for item in item_name_to_id}
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

    def generate_early(self) -> None:
        # self.multiworld.start_location_hints[self.player].value.update({loc for loc in self.location_name_to_id})
        self.multiworld.start_hints[self.player].value.update({item for item in self.item_name_to_id})
        self.multiworld.non_local_items[self.player].value.update({item for item in self.item_name_to_id})

    # def create_regions(self) -> None:
    #

    # def set_rules(self) -> None:
    #

    def create_item(self, name):
        return BingoItem(name, ItemClassification.progression, self.item_name_to_id[name], self.player)

    # def create_items(self):
    #     for item in self.item_name_to_id.keys():
    #         self.multiworld.itempool.append(self.create_item(item))
    #     self.multiworld.itempool += [self.create_item(item) for item in self.multiworld.random.sample(list(self.item_name_to_id.keys()), 21)]

    def post_fill(self):
        menu = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu)
        menu.locations = [Location(self.player, location_name, location_id, menu) for location_name, location_id in
                          self.location_name_to_id.items()]
        self.cards = [[self.multiworld.random.sample(r, 5) for r in
                       (range(1, 16), range(16, 31), range(31, 46), range(46, 61), range(61, 76))] for _ in range(1, 9)]
        for card in self.cards:
            card[2][2] = 0
        for location in self.multiworld.get_region("Menu", self.player).locations:
            location.progress_type = LocationProgressType.PRIORITY
            location.item_rule = lambda item: item.game != "Bingo" and item.classification == ItemClassification.progression
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
            bingo_calls = [f"{bingo_letter(self.cards[n][c[0]][c[1]])}-{self.cards[n][c[0]][c[1]]}" for c in coords if self.cards[n][c[0]][c[1]] != 0]
            location.access_rule = lambda state, b=bingo_calls: state.has_all(b, self.player)
            location.calls_needed = bingo_calls

        from BaseClasses import CollectionState
        multiworld = self.multiworld
        def get_item_spheres():
            state = CollectionState(multiworld)
            locations = set(multiworld.get_filled_locations())
            locations = {loc for loc in locations if loc.progress_type != LocationProgressType.EXCLUDED}
            beaten_games = set()
            while locations:
                reachable_locations = {location for location in locations if location.can_reach(state)}
                old_reachable_locations = None
                while old_reachable_locations != reachable_locations:
                    old_reachable_locations = reachable_locations.copy()
                    reachable_events = {location for location in reachable_locations if location.address is None}
                    for location in reachable_events:
                        state.collect(location.item, True, location)
                    locations -= reachable_events
                    reachable_locations = {location for location in locations if location.can_reach(state)}
                if not reachable_locations:
                    break  # don't swap unreachables
                    if locations:
                        yield locations  # unreachable locations
                    break
                else:
                    yield {loc for loc in reachable_locations if loc.player not in beaten_games and not loc.locked}
                    beaten_games = {player for player in multiworld.player_ids if multiworld.has_beaten_game(state)}

                for location in reachable_locations:
                    if location.item.advancement:
                        state.collect(location.item, True, location)
                locations -= reachable_locations
        item_pool = []
        for item in self.item_name_to_id.keys():
            item_pool.append(self.create_item(item))
        item_pool += [self.create_item(item) for item in self.multiworld.random.sample(list(self.item_name_to_id.keys()), 21)]
        spheres = [s for s in get_item_spheres() if len(s) >= 96]
        spheres.sort(key=lambda s: len(s))
        sphere = spheres[0]
        sphere = list(sphere)
        sphere.sort(key=lambda l: l.name)
        self.random.shuffle(sphere)
        for a, b in zip([loc for loc in self.multiworld.get_unfilled_locations(self.player) if not loc.progress_type == LocationProgressType.EXCLUDED], sphere):
            a.item = b.item
            b.item = item_pool.pop()
        pass
        # for i, s in enumerate(spheres):
        #     spheres[i] = [l for l in s if l.item.advancement]

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

    def extend_hint_information(self, hint_data: Dict[int, Dict[int, str]]):
        hint_data[self.player] = {}
        for location in self.multiworld.get_region("Menu", self.player).locations:
            hint_data[self.player][location.address] = ", ".join(location.calls_needed)


class BingoItem(Item):
    game = "Bingo"
