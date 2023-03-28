from ..AutoWorld import World, WebWorld
from Fill import remaining_fill
from .Regions import rooms, create_regions, location_table, set_rules
from .Items import item_table, item_groups, create_items, FFMQItem
from .Output import generate_output
from .Options import option_definitions
from BaseClasses import LocationProgressType
import base64
import threading

class FFMQWorld(World):
    """ffmq description here"""
    game = "Final Fantasy Mystic Quest"

    item_name_to_id = {name: data.id for name, data in item_table.items() if data.id is not None}
    location_name_to_id = location_table
    option_definitions = option_definitions

    topology_present = True

    item_name_groups = item_groups

    generate_output = generate_output
    create_items = create_items
    create_regions = create_regions
    set_rules = set_rules

    # def __init__(self, world, player: int):
    #     self.rom_name_available_event = threading.Event()
    #     super().__init__(world, player)

    def generate_early(self):
        if self.multiworld.sky_coin_mode[self.player] == "shattered":
            self.multiworld.brown_boxes[self.player] = self.multiworld.brown_boxes[self.player].from_text("include")
        if self.multiworld.enemies_scaling_lower[self.player].value > \
                self.multiworld.enemies_scaling_upper[self.player].value:
            (self.multiworld.enemies_scaling_lower[self.player].value,
             self.multiworld.enemies_scaling_upper[self.player].value) =\
                (self.multiworld.enemies_scaling_upper[self.player].value,
                 self.multiworld.enemies_scaling_lower[self.player].value)
        if self.multiworld.bosses_scaling_lower[self.player].value > \
                self.multiworld.bosses_scaling_upper[self.player].value:
            (self.multiworld.bosses_scaling_lower[self.player].value,
             self.multiworld.bosses_scaling_upper[self.player].value) =\
                (self.multiworld.bosses_scaling_upper[self.player].value,
                 self.multiworld.bosses_scaling_lower[self.player].value)

    @classmethod
    def stage_generate_early(cls, multiworld):
        multiworld.ffmq_useful_locations = []

    @classmethod
    def stage_fill_hook(cls, multiworld, progitempool, usefulitempool, filleritempool, fill_locations):
        # this is the only real safe way to ensure a location has a 'useful' item in it. Attempting to accomplish
        # this with an item rule could cause a very long swap loop
        remaining_fill(multiworld, multiworld.ffmq_useful_locations.copy(), usefulitempool)
        for location in multiworld.ffmq_useful_locations:
            if location.item:
                fill_locations.remove(location)
                location.locked = True
            else:
                # not enough useful items. This shouldn't happen unless other games are also pulling items from the
                # pool early
                location.progress_type = LocationProgressType.PRIORITY

    # def modify_multidata(self, multidata) -> None:
    #     b64_name: str = base64.b64encode(bytes(self.rom_name)).decode()
    #     multidata["connect_names"][b64_name] = multidata["connect_names"][self.multiworld.player_name[self.player]]

    def create_item(self, name: str):
        return FFMQItem(name, self.player)

    def collect_item(self, state, item, remove=False):
        if "Progressive" in item.name:
            i = item.code - 256
            if state.has(self.item_id_to_name[i], self.player):
                if state.has(self.item_id_to_name[i+1], self.player):
                    return self.item_id_to_name[i+2]
                return self.item_id_to_name[i+1]
            return self.item_id_to_name[i]
        return item.name if item.advancement else None







