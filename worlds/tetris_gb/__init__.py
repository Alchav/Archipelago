from typing import Mapping, Any

from BaseClasses import Item, Tutorial, ItemClassification, Region, Location, Item
from ..AutoWorld import World, WebWorld
from . import client
from .locations import score_locations, location_name_to_id
from .items import items, item_name_to_id
from .options import TetrisOptions


class TetrisGBWorld(World):
    game = "Tetris"
    location_name_to_id = location_name_to_id
    item_name_to_id = item_name_to_id

    origin_region_name: str = "Sphere 1"

    options_dataclass = TetrisOptions
    options: TetrisOptions

    def __init__(self, multiworld, player: int):
        super().__init__(multiworld, player)
        self.speed_decreases = 0
        self.speed_increases = 0

    def generate_early(self):
        starting_speed = self.options.starting_speed.value
        maximum_speed = self.options.maximum_speed.value
        target_speed = max(self.options.target_speed.value, maximum_speed)
        self.speed_increases = starting_speed - maximum_speed
        self.speed_decreases = target_speed - maximum_speed

    def create_regions(self):

        locs = list(range(1, len(location_name_to_id) + 1))

        locations_used = [int(i * len(locs) / self.options.location_count.value) for i in range(1, self.options.location_count.value + 1)]

        regions = []
        total_spheres = max(self.speed_decreases, self.options.score_multipliers.value) + 1

        locs_per_sphere = len(locations_used) / total_spheres
        for n in range(1, total_spheres + 1):
            sphere_region = Region(f"Sphere {n}", self.player, self.multiworld)
            for i in range(int(locs_per_sphere * (n - 1)), int(locs_per_sphere * n)):
                if i > len(locations_used) - 1:
                    break
                sphere_region.locations.append(TetrisLocation(self.player, self.location_id_to_name[locations_used[i]], locations_used[i], sphere_region))
            regions.append(sphere_region)
        for i, region in enumerate(regions):
            if i < len(regions) - 1:
                region.connect(regions[i + 1], f"Sphere {i} to {i + 1}",
                               rule=lambda state, sphere=i + 1: state.has("Decrease Speed", self.player, int((self.speed_decreases / total_spheres) * sphere))
                               and state.has("Score Multiplier", self.player, int((self.options.score_multipliers.value / total_spheres) * sphere))
                               )
        self.multiworld.regions += regions

    def set_rules(self):
        self.multiworld.completion_condition[self.player] = lambda state: (
                state.has("Decrease Speed", self.player, self.speed_decreases)
                and state.has("Score Multiplier", self.player, self.options.score_multipliers.value)
        )

    def create_items(self):
        item_pool = [self.create_item("Hide Next Piece")]
        item_pool += [self.create_item("Score Multiplier") for _ in range(self.options.score_multipliers.value)]
        item_pool += [self.create_item("Decrease Speed") for _ in range(self.speed_decreases)]
        item_pool += [self.create_item("Increase Speed") for _ in range(self.speed_increases)]
        item_pool += [self.create_item(item) for item in self.random.choices(["Garbage Line", "Shuffle Garbage Line Hole"], weights=[50, 1], k=len(self.multiworld.get_unfilled_locations(self.player)) - len(item_pool))]
        self.multiworld.itempool += item_pool

    def create_item(self, item):
        return TetrisItem(item, items[item], self.item_name_to_id[item], self.player)

    def fill_slot_data(self):
        return {"starting_speed": self.options.starting_speed.value}


class TetrisLocation(Location):
    game = "Tetris"


class TetrisItem(Item):
    game = "Tetris"
