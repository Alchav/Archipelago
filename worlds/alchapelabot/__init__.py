from worlds.AutoWorld import World
from BaseClasses import ItemClassification, Item
from NetUtils import SlotType


class AlchapelaBotWorld(World):
    game = "AlchapelaBot"
    topology_present = False

    def generate_early(self):
        self.multiworld.player_types[self.player] = SlotType.spectator  # mark as spectator
        for player, player_name in self.multiworld.player_name.items():
            self.item_name_to_id[f"Unlock {player_name}"] = player
            self.item_id_to_name[player] = f"Unlock {player_name}"

    def create_item(self, name):
        return Item(name, ItemClassification.progression, self.item_name_to_id[name], self.player)