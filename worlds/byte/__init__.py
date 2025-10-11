from BaseClasses import Location, Region, Item, ItemClassification, LocationProgressType
from worlds.AutoWorld import World, WebWorld
num_bytes = 1
import logging
# logging.getLogger().setLevel(logging.DEBUG)
# logging.basicConfig(level=logging.DEBUG)
def get_set_bits(value: int) -> list[str]:
    result = []
    bit = 1
    while value:
        if value & 1:
            result.append(f"0x{bit:02X}")
        value >>= 1
        bit <<= 1
    return result


class Byte(World):
    game = "Byte"
    item_name_to_id = {name: item_id for name, item_id in zip([f"0x{1 << i:02X}" for i in range(9)], range(1, 9))}
    location_name_to_id = {f"0x{i:02X}": i + 1 for i in range(256)}

    def create_regions(self):
        menu = Region("Menu", self.player, self.multiworld)
        for i in range(0, 0x100):
            location = Location(self.player, f"0x{i:02X}", i+1, menu)
            menu.locations.append(location)
        self.multiworld.regions.append(menu)

    def set_rules(self):
        def make_access_rule(items):
            return lambda state: state.has_all(items, self.player)
        for i in range(0, 0x100):
            location = self.multiworld.get_location(f"0x{i:02X}", self.player)
            items = get_set_bits(i)
            location.access_rule = make_access_rule(items)
        self.multiworld.completion_condition[self.player] = lambda state: state.has_all(list(self.item_name_to_id), self.player)

    def create_items(self):
        self.multiworld.itempool += [ByteItem(item, ItemClassification.progression, i, self.player) for item, i in self.item_name_to_id.items()]

    def create_item(self, name: str) -> Item:
        return ByteItem(name, ItemClassification.progression, int(name, 16), self.player)

class ByteItem(Item):
    game = "Byte"
