from BaseClasses import Location, Item, ItemClassification, Region, LocationProgressType
from worlds.AutoWorld import World
from Fill import get_item_spheres, swappable

from worlds.LauncherComponents import Component, SuffixIdentifier, Type, components, launch_subprocess


def launch_client(*args) -> None:
    from .client import launch
    launch_subprocess(launch, name="IDClient")


component = Component("Item Dispenser Client", "IDClient", component_type=Type.CLIENT, func=launch_client,
                      file_identifier=SuffixIdentifier())
components.append(component)


class ItemDispenser(World):
    game = "Item Dispenser"
    item_name_to_id = {"Token": 1}
    location_name_to_id = {"Item 1": 1}

    def post_fill(self):
        i = 0
        menu = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu)
        for sphere in list(get_item_spheres(self.multiworld)):
            sphere = sorted(sphere)
            self.random.shuffle(sphere)
            for location in sphere:
                if location.progress_type == LocationProgressType.PRIORITY:
                    continue
                if not swappable(self.multiworld, location):
                    continue
                if location.progress_type == LocationProgressType.DEFAULT and self.multiworld.worlds[location.player].options.token_percentage < self.random.randint(1, 100):
                    continue
                i += 1
                loc_name = f"Item {i}"
                self.location_name_to_id[loc_name] = i
                new_location = IDLocation(self.player, loc_name, i, menu)
                menu.locations.append(new_location)
                new_location.item = location.item
                new_location.item.location = new_location
                new_item = IDItem("Token", ItemClassification.progression_skip_balancing, 1, self.player)
                location.item = None
                location.place_locked_item(new_item)
                new_location.access_rule = lambda state, count=i: state.has("Token", self.player, count)
                new_location.parent_region = menu


class IDLocation(Location):
    game = "Item Dispenser"


class IDItem(Item):
    game = "Item Dispenser"
