from BaseClasses import Location, Region, Item, ItemClassification, LocationProgressType
from worlds.AutoWorld import World, WebWorld
import random

seeded_random = random.Random(172)
regions = [f"Region {i}" for i in range(1, 173)]
region_locations = {r: [] for r in regions}
all_locations = []
for region_name, location_list in region_locations.items():
    for i in range(1, seeded_random.randint(11, 26)):
        loc_name = region_name + f" - Location {i}"
        location_list.append(loc_name)
        all_locations.append(loc_name)


class Game(World):
    game = "Game"
    item_name_to_id = {f"Item {i}": i for i in range(1, 101)}
    location_name_to_id = {a: b for a, b in zip(all_locations, range(1, len(all_locations) + 1))}

    origin_region_name = "Region 1"

    def create_regions(self):
        self.random = seeded_random

        def rule_factory(n):
            n = self.random.randint(1, n)
            items_needed = self.random.choices(list(self.item_name_to_id.keys()), k=n)
            print(items_needed)
            return lambda state: state.has_all(items_needed, self.player)
        regions = list(range(2, 173))
        self.random.shuffle(regions)
        regions = [1] + regions
        regions2 = regions.copy()
        self.random.shuffle(regions2)
        for i in regions:
            region = Region(f"Region {i}", self.player, self.multiworld)
            self.multiworld.regions.append(region)
            for location_name in region_locations[f"Region {i}"]:
                print(location_name)
                location = Location(self.player, location_name, self.location_name_to_id[location_name], region)
                region.locations.append(location)
                if self.random.randint(0, 2) == 0:
                    if self.random.randint(0, 2) == 0:
                        location.access_rule = rule_factory(2)
                    else:
                        location.access_rule = rule_factory(1)
        for r1, r2 in zip(regions[:len(regions) - 1], regions[1:]):
            print(f"{r1} - {r2} - 1")
            rule = rule_factory(2)
            self.multiworld.get_region(f"Region {r1}", self.player).connect(self.multiworld.get_region(f"Region {r2}", self.player), f"{r1} to {r2} - 1", rule=rule)
            self.multiworld.get_region(f"Region {r2}", self.player).connect(self.multiworld.get_region(f"Region {r1}", self.player), f"{r1} to {r2} - 1", rule=rule)
        victory_region = self.multiworld.get_region(f"Region {r2}", self.player)
        victory_location = Location(self.player, "Win Game", None, victory_region)
        self.multiworld.get_region(f"Region {r2}", self.player).locations.append(victory_location)
        victory_location.access_rule = rule_factory(6)
        victory_location.item = GameItem("Win Game", ItemClassification.progression, None, self.player)

        for r1, r2 in zip(regions, regions2):
            print(f"{r1} - {r2} - 2")
            self.multiworld.get_region(f"Region {r1}", self.player).connect(self.multiworld.get_region(f"Region {r2}", self.player), f"{r1} to {r2} - 2", rule=rule_factory(4))

    def set_rules(self):
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Win Game", self.player)

    def create_items(self):
        self.multiworld.itempool += [GameItem(item, ItemClassification.progression, i, self.player) for item, i in self.item_name_to_id.items()]


class GameItem(Item):
    game = "Byte"
