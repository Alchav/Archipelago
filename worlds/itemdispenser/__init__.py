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
    item_name_to_id = {f"{n} Token{'s' if n != 1 else ''}": n for n in range(1, 10000)}
    location_name_to_id = {"1 Token": 1}

    def __init__(self, multiworld, player: int):
        super().__init__(multiworld, player)
        self.displaced_items = {}

    def post_fill(self):
        token_rates = {player: (len({loc for loc in self.multiworld.get_locations(player) if swappable(self.multiworld, loc)})
                                * self.multiworld.worlds[player].options.token_percentage.value / 100) for player in self.multiworld.player_ids}
        highest_token_rate = max(token_rates.values())
        token_rates = {player: int(101 - ((100 / highest_token_rate) * token_rate)) for player, token_rate in token_rates.items()}
        # all_state = self.multiworld.get_all_state(use_cache=False)
        state = self.multiworld.state.copy()
        state.sweep_for_advancements()
        i = 0
        menu = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu)
        active_games = set()
        extra_items_to_place = []

        def last_available_loc(n):
            for i in range(n, 1, -1):
                loc_name = f"{i} Token{'s' if i != 1 else ''}"
                if loc_name not in self.multiworld.regions.location_cache[self.player]:
                    return i
            else:
                raise Exception("No possible open item dispenser locations")

        beaten_game_spheres = {}
        unreachable = False
        for sphere_num, sphere in enumerate(list(get_item_spheres(self.multiworld, beaten_game_spheres)), start=1):
            extra_items_to_place += [item for item in self.multiworld.extra_items if item.player in active_games]
            self.multiworld.extra_items = [item for item in self.multiworld.extra_items if item not in extra_items_to_place]
            self.random.shuffle(extra_items_to_place)
            sphere = sorted(sphere)
            self.random.shuffle(sphere)
            if not sphere:
                unreachable = True
                break # no unreachable
            for location in sphere:
                active_games.add(location.player)
                if location.item and location.item.player != 1:
                    if location.player == location.item.player and location.item.name in self.multiworld.worlds[location.item.player].options.non_local_items.value:
                        pass
                    else:
                        if beaten_game_spheres[location.player] < sphere_num:
                            continue
                        if location.progress_type != LocationProgressType.DEFAULT:
                            continue
                        if not swappable(self.multiworld, location):
                            continue
                        elif self.multiworld.worlds[location.player].options.token_percentage < self.random.randint(1, 100):
                            continue
                increment = max(1, int(self.random.triangular((token_rates[location.player] * 0.75),
                                                              int(token_rates[location.player] * 1.25),
                                                              token_rates[location.player])))

                i += increment
                if location.item:
                    loc_name = f"{i} Token{'s' if i != 1 else ''}"
                    # print(f"{i} Token{'s' if i != 1 else ''}")
                    self.location_name_to_id[loc_name] = i
                    new_location = IDLocation(self.player, loc_name, i, menu)
                    menu.locations.append(new_location)
                    new_location.item = location.item
                    new_location.item.location = new_location
                    new_location.access_rule = lambda state, count=i: token_logic(state, self, count)
                    new_location.parent_region = menu
                    location.item = None
                    new_item = IDItem(f"{increment} Token{'s' if i != 1 else ''}", ItemClassification.progression_skip_balancing, increment, self.player)
                    location.place_locked_item(new_item)
                    if location.item.game == "AlchapelaBot":
                        i2 = last_available_loc(i-1)
                        loc_name_2 = f"{i2} Token{'s' if i2 != 1 else ''}"
                        new_location_2 = IDLocation(self.player, loc_name_2, i2, menu)
                        new_location_2.place_locked_item(self.displaced_items[sphere_num].pop())
                        new_location_2.access_rule = lambda state, count=i2: token_logic(state, self, count)
                        new_location_2.parent_region = menu
                        menu.locations.append(new_location_2)
                        self.location_name_to_id[loc_name_2] = i2
                    elif extra_items_to_place:
                        i2 = last_available_loc(i-1)
                        loc_name_2 = f"{i2} Token{'s' if i2 != 1 else ''}"
                        new_location_2 = IDLocation(self.player, loc_name_2, i2, menu)
                        new_location_2.place_locked_item(extra_items_to_place.pop())
                        new_location_2.access_rule = lambda state, count=i2: token_logic(state, self, count)
                        new_location_2.parent_region = menu
                        menu.locations.append(new_location_2)
                        self.location_name_to_id[loc_name_2] = i2
                elif extra_items_to_place:
                    loc_name = f"{i} Token{'s' if i != 1 else ''}"
                    new_location = IDLocation(self.player, loc_name, i, menu)
                    new_location.place_locked_item(extra_items_to_place.pop())
                    new_location.access_rule = lambda state, count=i: token_logic(state, self, count)
                    new_location.parent_region = menu
                    menu.locations.append(new_location)
                    self.location_name_to_id[loc_name] = i
        assert not any(self.displaced_items.values())


class IDLocation(Location):
    game = "Item Dispenser"


class IDItem(Item):
    game = "Item Dispenser"
