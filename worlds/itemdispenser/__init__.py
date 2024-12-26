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


def token_logic(state, world, count):
    # tokens = 0
    # for item, i in world.item_name_to_id.items():
    #     tokens += (state.count(item, world.player) * i)
    tokens = sum((state.count(item, world.player) * i) for item, i in world.item_name_to_id.items())
    return tokens >= count


class ItemDispenser(World):
    game = "Item Dispenser"
    item_name_to_id = {f"{n} Token{'s' if n != 1 else ''}": n for n in range(1, 11)}
    location_name_to_id = {"1 Token": 1}

    def __init__(self, multiworld, player: int):
        super().__init__(multiworld, player)
        self.displaced_items = {}

    def post_fill(self):
        # all_state = self.multiworld.get_all_state(use_cache=False)
        state = self.multiworld.state.copy()
        state.sweep_for_advancements()
        i = 0
        menu = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu)
        active_games = set()
        extra_items_to_place = []
        for sphere_num, sphere in enumerate(list(get_item_spheres(self.multiworld))):
            extra_items_to_place += [item for item in self.multiworld.extra_items if item.player in active_games]
            self.multiworld.extra_items = [item for item in self.multiworld.extra_items if item not in extra_items_to_place]
            self.random.shuffle(extra_items_to_place)
            sphere = sorted(sphere)
            self.random.shuffle(sphere)
            for location in sphere:
                active_games.add(location.player)
                unreachable = False
                if location.item.player != 1:
                    if location.progress_type == LocationProgressType.PRIORITY:
                        continue
                    if not swappable(self.multiworld, location):
                        continue
                    if not location.can_reach(state):
                        unreachable = True
                    elif location.progress_type == LocationProgressType.DEFAULT and self.multiworld.worlds[location.player].options.token_percentage < self.random.randint(1, 100):
                        continue
                if unreachable:
                    increment = 1
                elif location.item.excludable:
                    increment = int(self.random.triangular(2, 5, 2))
                elif location.item.classification in (ItemClassification.progression_skip_balancing, ItemClassification.useful):
                    increment = int(self.random.triangular(2, 7, 2))
                else:
                    increment = int(self.random.triangular(2, 10, 2))
                i += increment
                loc_name = f"{i} Token{'s' if i != 1 else ''}"
                print(f"{i} Token{'s' if i != 1 else ''}")
                self.location_name_to_id[loc_name] = i
                new_location = IDLocation(self.player, loc_name, i, menu)
                menu.locations.append(new_location)
                new_location.item = location.item
                new_location.item.location = new_location
                if location.item.game == "AlchapelaBot":
                    new_location_2 = IDLocation(self.player, f"{i-1} Token{'s' if i != 1 else ''}", i-1, menu)
                    new_location_2.place_locked_item(self.displaced_items[sphere_num].pop())
                    new_location_2.access_rule = lambda state, count=i-1: token_logic(state, self, count)
                    new_location_2.parent_region = menu
                    menu.locations.append(new_location_2)
                elif extra_items_to_place:
                    new_location_2 = IDLocation(self.player, f"{i-1} Token{'s' if i != 1 else ''}", i-1, menu)
                    new_location_2.place_locked_item(extra_items_to_place.pop())
                    new_location_2.access_rule = lambda state, count=i-1: token_logic(state, self, count)
                    new_location_2.parent_region = menu
                    menu.locations.append(new_location_2)
                new_item = IDItem(f"{increment} Token{'s' if i != 1 else ''}", ItemClassification.progression_skip_balancing, increment, self.player)
                location.item = None
                location.place_locked_item(new_item)
                new_location.access_rule = lambda state, count=i: token_logic(state, self, count)
                new_location.parent_region = menu
        assert not any(self.displaced_items.values())


class IDLocation(Location):
    game = "Item Dispenser"


class IDItem(Item):
    game = "Item Dispenser"
