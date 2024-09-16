from typing import List
from typing import Dict

from BaseClasses import Region, Tutorial
from worlds.AutoWorld import WebWorld, World
from .Items import MMRItem, item_data_table, item_table, code_to_item_table
from .Locations import MMRLocation, location_data_table, location_table, code_to_location_table, locked_locations
from .Options import mmr_options
from .Regions import region_data_table, get_exit
from .Rules import *


class MMRWebWorld(WebWorld):
    theme = "partyTime"
    
    setup_en = Tutorial(
        tutorial_name="Start Guide",
        description="A guide to playing Majora's Mask Recompiled in Archipelago.",
        language="English",
        file_name="guide_en.md",
        link="guide/en",
        authors=["LittleCube"]
    )
    
    tutorials = [setup_en]


class MMRWorld(World):
    """A Zelda game we're not completely burnt out on."""

    game = "Majora's Mask Recompiled"
    data_version = 1
    web = MMRWebWorld()
    option_definitions = mmr_options
    location_name_to_id = location_table
    item_name_to_id = item_table

    def generate_early(self):
        pass
    
    def create_item(self, name: str) -> MMRItem:
        return MMRItem(name, item_data_table[name].type, item_data_table[name].code, self.player)

    def create_items(self) -> None:
        mw = self.multiworld

        item_pool: List[MMRItem] = []
        item_pool_count: Dict[str, int] = {}
        for name, item in item_data_table.items():
            item_pool_count[name] = 0
            if item.code and item.can_create(self.options):
                while item_pool_count[name] < item.num_exist:
                    item_pool.append(self.create_item(name))
                    item_pool_count[name] += 1

        mw.itempool += item_pool

        mw.push_precollected(self.create_item("Ocarina of Time"))
        mw.push_precollected(self.create_item("Song of Time"))
        mw.push_precollected(self.create_item("Progressive Sword"))

    def create_regions(self) -> None:
        player = self.player
        mw = self.multiworld

        # Create regions.
        for region_name in region_data_table.keys():
            region = Region(region_name, player, mw)
            mw.regions.append(region)

        # Create locations.
        for region_name, region_data in region_data_table.items():
            region = mw.get_region(region_name, player)
            region.add_locations({
                location_name: location_data.address for location_name, location_data in location_data_table.items()
                if location_data.region == region_name and location_data.can_create(self.options)
            }, MMRLocation)
            region.add_exits(region_data.connecting_regions)

        # Place locked locations.
        for location_name, location_data in locked_locations.items():
            # Ignore locations we never created.
            if not location_data.can_create(self.options):
                continue

            locked_item = self.create_item(location_data_table[location_name].locked_item)
            mw.get_location(location_name, player).place_locked_item(locked_item)

        if not self.options.shuffle_swamphouse_reward.value:
            mw.get_location("Swamphouse Reward", player).place_locked_item(self.create_item("Mask of Truth"))

        if self.options.skullsanity.value == 0:
            for i in range(0, 31):
                if i == 3:
                    continue
                mw.get_location(code_to_location_table[0x34769420062700 | i], player).place_locked_item(self.create_item("Swamp Skulltula Token"))
                

        if not self.options.shuffle_great_fairy_rewards.value:
            mw.get_location("North Clock Town Great Fairy Reward", player).place_locked_item(self.create_item("Progressive Magic Upgrade"))
            mw.get_location("North Clock Town Great Fairy Reward (Has Transformation Mask)", player).place_locked_item(self.create_item("Great Fairy Mask"))
            mw.get_location("Woodfall Great Fairy Reward", player).place_locked_item(self.create_item("Great Spin Attack"))

        if not self.options.fairysanity.value:
            mw.get_location("Laundry Pool Stray Fairy (Clock Town)", player).place_locked_item(self.create_item("Stray Fairy (Clock Town)"))

            mw.get_location("Woodfall Temple Entrance Chest", player).place_locked_item(self.create_item("Stray Fairy (Woodfall)"))
            mw.get_location("Woodfall Temple Wooden Flower Switch Chest", player).place_locked_item(self.create_item("Stray Fairy (Woodfall)"))
            mw.get_location("Woodfall Temple Black Boe Room Chest", player).place_locked_item(self.create_item("Stray Fairy (Woodfall)"))
            mw.get_location("Woodfall Temple Entrance Freestanding SF", player).place_locked_item(self.create_item("Stray Fairy (Woodfall)"))
            mw.get_location("Woodfall Temple Wooden Flower Deku Baba SF", player).place_locked_item(self.create_item("Stray Fairy (Woodfall)"))
            mw.get_location("Woodfall Temple Wooden Flower Pot SF", player).place_locked_item(self.create_item("Stray Fairy (Woodfall)"))
            mw.get_location("Woodfall Temple Moving Flower Platform Room Beehive SF", player).place_locked_item(self.create_item("Stray Fairy (Woodfall)"))
            mw.get_location("Woodfall Temple Wooden Flower Bubble SF", player).place_locked_item(self.create_item("Stray Fairy (Woodfall)"))
            mw.get_location("Woodfall Temple Push Block Skulltula SF", player).place_locked_item(self.create_item("Stray Fairy (Woodfall)"))
            mw.get_location("Woodfall Temple Push Block Bubble SF", player).place_locked_item(self.create_item("Stray Fairy (Woodfall)"))
            mw.get_location("Woodfall Temple Push Block Beehive SF", player).place_locked_item(self.create_item("Stray Fairy (Woodfall)"))
            mw.get_location("Woodfall Temple Final Room Right Lower Platform SF", player).place_locked_item(self.create_item("Stray Fairy (Woodfall)"))
            mw.get_location("Woodfall Temple Final Room Right Upper Platform SF", player).place_locked_item(self.create_item("Stray Fairy (Woodfall)"))
            mw.get_location("Woodfall Temple Final Room Left Upper Platform SF", player).place_locked_item(self.create_item("Stray Fairy (Woodfall)"))
            mw.get_location("Woodfall Temple Final Room Bubble SF", player).place_locked_item(self.create_item("Stray Fairy (Woodfall)"))

        # TODO: check options to see what player starts with
        mw.get_location("Top of Clock Tower (Ocarina of Time)", player).place_locked_item(self.create_item(self.get_filler_item_name()))
        mw.get_location("Top of Clock Tower (Song of Time)", player).place_locked_item(self.create_item(self.get_filler_item_name()))

    def get_filler_item_name(self) -> str:
        return "Purple Rupee"

    def set_rules(self) -> None:
        player = self.player
        mw = self.multiworld

        # Completion condition.
        mw.completion_condition[player] = lambda state: state.has("Victory", player)

        if (self.options.logic_difficulty == 4):
            return

        region_rules = get_region_rules(player)
        for entrance_name, rule in region_rules.items():
            entrance = mw.get_entrance(entrance_name, player)
            entrance.access_rule = rule

        location_rules = get_location_rules(player)
        for location in mw.get_locations(player):
            name = location.name
            if name in location_rules and location_data_table[name].can_create(self.options):
                location.access_rule = location_rules[name]

    def fill_slot_data(self):
        return {
            "skullsanity": self.options.skullsanity.value,
            "death_link": self.options.death_link.value
        }
