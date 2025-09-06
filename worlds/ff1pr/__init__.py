from dataclasses import fields
from typing import Dict, List, Any, Tuple, Type, TypedDict, ClassVar, Union, Set, TextIO
from logging import warning
from BaseClasses import Region, Location, Item, Tutorial, ItemClassification, MultiWorld, CollectionState
from .items import item_name_to_id, item_table, item_name_groups
from .locations import location_table, standard_location_name_to_id, event_table, location_name_groups
from .rules import set_location_rules, set_region_rules
from .regions import ff1pr_regions
from .options import FF1pixelOptions, grouped_options, presets
from worlds.AutoWorld import WebWorld, World
from Options import PerGameCommonOptions

GAME_NAME: str = "FF1 Pixel Remaster"

class FF1pixelWeb(WebWorld):
    tutorials = [
        Tutorial(
            tutorial_name="Multiworld Setup Guide",
            description="A guide to setting up the FF1 Pixel Remaster Randomizer for Archipelago multiworld games.",
            language="English",
            file_name="setup_en.md",
            link="setup/en",
            authors=["wildham"]
        )
    ]
    theme = "grassFlowers"
    game = GAME_NAME
    option_groups = grouped_options
    options_presets = presets
    bug_report_page = "https://github.com/wildham0/FF1PRAP/issues"

class FF1pixelItem(Item):
    game: str = GAME_NAME

class FF1pixelLocation(Location):
    game: str = GAME_NAME

class FF1pixelWorld(World):
    """
    Explore the world of Final Fantasy from its origins.
    """
    game = GAME_NAME
    web = FF1pixelWeb()

    options: FF1pixelOptions
    options_dataclass = FF1pixelOptions

    item_name_groups = item_name_groups
    location_name_groups = location_name_groups
    item_name_to_id = item_name_to_id
    location_name_to_id = standard_location_name_to_id.copy()

    items_to_ignore: List[int] = []

    spawn_airship = False
    spawn_ship = False

    def generate_early(self) -> None:
        if self.options.start_inventory.value.get("Airship", 0) > 0:
            self.spawn_airship = True
            self.items_to_ignore.append(507)

        if self.options.start_inventory_from_pool.value.get("Airship", 0) > 0:
            self.spawn_airship = True
            self.items_to_ignore.append(507)

        if self.options.start_inventory.value.get("Ship",0) > 0:
            self.spawn_ship = True
            self.items_to_ignore.append(44)

        if self.options.start_inventory_from_pool.value.get("Ship",0) > 0:
            self.spawn_ship = True
            self.items_to_ignore.append(44)

        if self.options.job_promotion.value == 0:
            self.items_to_ignore.append(500)

        if self.options.lute_tablatures.value > 0:
            self.options.start_inventory.value["Lute"] = 1

    def create_event(self, event: str) -> FF1pixelItem:
        # while we are at it, we can also add a helper to create events
        return FF1pixelItem(event, ItemClassification.progression, None, self.player)

    def create_item(self, name: str) -> FF1pixelItem:
        return FF1pixelItem(name, item_table[name].classification, self.item_name_to_id[name], self.player)

    def create_items(self) -> None:
        ff1pr_items: List[FF1pixelItem] = []
        items_made: int = 0

        items_to_create: Dict[str, int] = {item: data.quantity_in_item_pool for item, data in item_table.items()}
        available_filler: List[str] = [filler for filler in items_to_create if items_to_create[filler] > 0 and
                                       item_table[filler].classification == ItemClassification.filler]

        def remove_filler(qty: int) -> None:
            for i in range(qty):
                filler_item = self.random.choice(available_filler)
                #if items_to_create[filler_item] == 0:
                # screw up message
                items_to_create[filler_item] -= 1
                if items_to_create[filler_item] == 0:
                    available_filler.remove(filler_item)

        # Early Progression Ship
        if self.options.early_progression.value == 1 and not self.spawn_ship:
            items_to_create["Ship"] = 1
        elif self.spawn_ship:
            items_to_create[self.get_filler_item_name()] += 1

        # Job Items
        if self.options.job_promotion == 1:
            items_to_create["All Promotion Jobs"] = 1
        elif self.options.job_promotion == 2:
            remove_filler(5)
            for item in item_name_groups["Jobs"]:
                items_to_create[item] = 1

        # Lute Tablatures Mode
        if self.options.lute_tablatures > 0:
            items_to_create["Lute"] = 0
            items_to_create["Lute Tablature"] = 40
            remove_filler(39)

        for item, quantity in items_to_create.items():
            for _ in range(quantity):
                ff1pr_items.append(self.create_item(item))
            items_made += quantity

        self.multiworld.itempool += ff1pr_items

    def create_regions(self) -> None:
        for region_name in ff1pr_regions:
            region = Region(region_name, self.player, self.multiworld)
            self.multiworld.regions.append(region)

        for region_name, exits in ff1pr_regions.items():
            region = self.get_region(region_name)
            #print(region_name)
            region.add_exits(exits)

        for location_name, location_id in self.location_name_to_id.items():
            #print(location_name)
            region = self.get_region(location_table[location_name].region)
            location = FF1pixelLocation(self.player, location_name, location_id, region)
            region.locations.append(location)

        for location_name, location_data in event_table.items():
            #print(location_name)
            region = self.get_region(location_data.region)
            location = FF1pixelLocation(self.player, location_name, None, region)
            region.locations.append(location)

    def set_rules(self) -> None:
        set_region_rules(self)
        set_location_rules(self)

    def get_filler_item_name(self) -> str:
        filler_list = list(self.item_name_groups["Fillers"])
        return self.random.choice(filler_list)

    def fill_slot_data(self) -> Dict[str, Any]:
        options_list = options.presets["Starter"].keys()
        slot_data: Dict[str, Any] = {
            "items_to_ignore": self.items_to_ignore,
            "spawn_airship": self.spawn_airship,
            "spawn_ship": self.spawn_ship,
            **self.options.as_dict(*options_list)
        }

        dummy_slot_data: Dict[str, Any] = {
            "shuffle_gear_shops": self.options.shuffle_gear_shops.value,
            "shuffle_spells": self.options.shuffle_spells.value,
            "job_promotion": self.options.job_promotion.value,
            "lute_tablatures": self.options.lute_tablatures.value,
            "crystals_required": self.options.crystals_required.value,
            "shuffle_trials_maze": self.options.shuffle_trials_maze.value,
            "early_progression": self.options.early_progression.value,
            "northern_docks": self.options.northern_docks.value,
            "nerf_chaos": self.options.nerf_chaos.value,
            "boss_minions": self.options.boss_minions.value,
            "monster_parties": self.options.monster_parties.value,
            "monsters_cap": self.options.monsters_cap.value,
            "dungeon_encounter_rate": self.options.dungeon_encounter_rate.value,
            "overworld_encounter_rate": self.options.overworld_encounter_rate.value,
            "xp_boost": self.options.xp_boost.value,
            "gil_boost": self.options.gil_boost.value,
            "boost_menu": self.options.boost_menu.value,
            "spawn_airship": self.spawn_airship,
            "spawn_ship": self.spawn_ship,
            "items_to_ignore": self.items_to_ignore
        }

        return slot_data