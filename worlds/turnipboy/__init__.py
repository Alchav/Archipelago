from BaseClasses import Item, MultiWorld, Region, Location, Tutorial, ItemClassification, CollectionState
from worlds.AutoWorld import World, WebWorld
from worlds.turnipboy.Options import TurnipBoyOptions
from .Items import item_table
from .Locations import get_location_table
from .Regions import get_region_table
from .Types import RegionData
from typing import Optional, Callable


class TurnipBoyWebWorld(WebWorld):
    theme = 'partyTime'
    tutorials = [
        Tutorial(
            tutorial_name='Setup Guide',
            description='A guide to playing Archipidle',
            language='English',
            file_name='guide_en.md',
            link='guide/en',
            authors=['Farrak Kilhn']
        )
    ]


class TurnipBoyWorld(World):
    """
    Turnip Boy Commits Tax Evasion
    """
    game = "TurnipBoy"
    item_name_to_id = {name: data.id for name, data in item_table.items()}
    location_name_to_id = {name: data.id for name, data in get_location_table(-1).items()}
    topology_present = False
    hidden = False
    web = TurnipBoyWebWorld()
    options_dataclass = TurnipBoyOptions
    options: TurnipBoyOptions

    def set_rules(self):
        self.multiworld.completion_condition[self.player] =\
            lambda state: state.has("Defeat Corrupt Onion", self.player)

    def create_item(self, name: str) -> Item:
        item_data = item_table[name]
        return Item(name, item_data.classification, item_data.index, self.player)

    def create_items(self):
        item_pool = []
        for (name, data) in item_table.items():
            for i in range(data.count):
                item_pool.append(TurnipBoyItem(
                    name,
                    data.classification,
                    data.id,
                    self.player
                ))

        self.multiworld.itempool += item_pool

    def create_regions(self):
        # Create the menu region
        menu_region = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions += [menu_region]

        # Now add the Turnip Boy regions
        for (region, data) in get_region_table(self.player).items():
            self.multiworld.regions += [create_region(self.multiworld, self.player, region, data)]

        # Connect Menu to Veggieville, then add all other connections
        menu_region.connect(self.multiworld.get_region("Veggieville", self.player))
        connect_regions(self.multiworld, self.player)

    def generate_early(self):
        quick_start = self.options.quick_start
        if (quick_start > 0):
            quick_start_items = self.multiworld.random.sample(["Progressive Weapon", "Watering Can", "Fertilizer"], quick_start)
            for item in quick_start_items:
                self.multiworld.local_early_items[self.player][item] = 1

    def post_fill(self):
        return

def create_region(world: MultiWorld, player: int, region_name: str, region_data: RegionData):
    region = Region(region_name, player, world)
    # Add locations
    for (location_name, location_data) in get_location_table(player).items():
        # TODO: Group locations by region
        if location_data.region == region_name:
            location = TurnipBoyLocation(player, location_name, location_data.id, region)
            region.locations.append(location)

            # Add an access rule for the location
            if location_data.rule:
                location.access_rule = location_data.rule

            # Handle "event" checks by adding a fixed item
            if location_data.event_name:
                location.place_locked_item(TurnipBoyItem(
                    location_data.event_name,
                    ItemClassification.progression,
                    None,
                    player
                ))
    return region

def connect_regions(world: MultiWorld, player: int):
    for (region_name, region_data) in get_region_table(player).items():
        for exit in region_data.exits:
            connect(world, player, region_name, exit.destination, exit.rule)

# Connect two regions
def connect(world: MultiWorld, player: int, source: str, target: str, rule: Optional[Callable[[CollectionState], bool]] = None):
    sourceRegion = world.get_region(source, player)
    targetRegion = world.get_region(target, player)
    sourceRegion.connect(targetRegion, rule=rule)

class TurnipBoyItem(Item):
    game: str = "TurnipBoy"

class TurnipBoyLocation(Location):
    game: str = "TurnipBoy"