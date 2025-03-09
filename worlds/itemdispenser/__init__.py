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
    tokens = sum((state.count(item, world.player) * i) for item, i in world.item_name_to_id.items())
    return tokens >= count


allowed_filler_games = {
    "Secret of Evermore", "Super Mario 64", "Crystalis", "DOOM 1993", "DOOM II", "Final Fantasy Mystic Quest",
    "A Hat in Time", "Pokemon Red and Blue", "The Sims 4", "Jigsaw", "Majora's Mask Recompiled", "Paper Mario",
    "A Link to the Past", "Final Fantasy IV Free Enterprise", "Mega Man X3", "Super Mario World"
}


class ItemDispenser(World):
    game = "Item Dispenser"
    item_name_to_id = {f"{n} Token{'s' if n != 1 else ''}": n for n in range(1, 100)}
    location_name_to_id = {"1 Token": 1}

    def __init__(self, multiworld, player: int):
        super().__init__(multiworld, player)
        self.displaced_items = {}

    def post_fill(self):
        state = self.multiworld.state.copy()
        state.sweep_for_advancements()
        i = 0
        menu = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu)
        active_games = set()
        extra_items_to_place = []

        old_skipped_sphere_locs = []

        beaten_game_spheres = {}
        unreachable = False
        for sphere_num, sphere in enumerate(list(get_item_spheres(self.multiworld, beaten_game_spheres)), start=1):
            extra_items_to_place += [item for item in self.multiworld.extra_items if item.player in active_games]
            self.multiworld.extra_items = [item for item in self.multiworld.extra_items if item not in extra_items_to_place]
            if sphere_num in self.displaced_items:
                extra_items_to_place += self.displaced_items[sphere_num]

            sphere_slots = sorted({location.player for location in sphere})

            for player in sphere_slots:
                active_games.add(player)
                extra_items_to_place.append(self.multiworld.worlds[1].create_item(f"{self.multiworld.player_name[player]} Hint Points"))

            self.random.shuffle(extra_items_to_place)

            sphere = sorted(sphere)
            self.random.shuffle(sphere)
            sphere_locations = []
            sphere_num_locations = {}
            skipped_sphere_locs = []
            if not sphere:
                unreachable = True
                break # no unreachable
            for location in sphere:
                if location.item and location.item.player != 1:
                    if location.player == location.item.player and location.item.name in self.multiworld.worlds[location.item.player].options.non_local_items.value:
                        pass
                    elif location.item.name == "Nothing":
                        pass
                    else:
                        # if beaten_game_spheres[location.player] < sphere_num:
                        #     continue
                        if location.progress_type != LocationProgressType.DEFAULT:
                            continue
                        if not swappable(self.multiworld, location):
                            continue
                        elif self.multiworld.worlds[location.player].options.token_percentage * (100 if location.item.advancement else 5) < self.random.randint(1, 10000):
                            continue
                sphere_locations.append(location)
                if location.player not in sphere_num_locations:
                    sphere_num_locations[location.player] = 1
                else:
                    sphere_num_locations[location.player] += 1

            def add_location(item, i):
                loc_name = f"{i} Token{'s' if i != 1 else ''}"
                self.location_name_to_id[loc_name] = i
                new_location = IDLocation(self.player, loc_name, i, menu)
                menu.locations.append(new_location)
                new_location.item = item
                item.location = new_location
                new_location.access_rule = lambda state, count=i: token_logic(state, self, count)
                new_location.parent_region = menu
                new_location.locked = True
            if sphere_locations:
                highest_count = max(sphere_num_locations.values())
                token_rates = {player: 10 - ((10 / highest_count) * value) for player, value in sphere_num_locations.items()}
                self.random.shuffle(sphere_locations)
                for location in sphere_locations:
                    increment = max(min(round(self.random.triangular(1, 100, token_rates[location.player])), 10), 1)
                    skipped_sphere_locs += list(range(i+1, i+increment))
                    i += increment
                    if location.item and location.item.name != "Nothing":
                        add_location(location.item, i)
                    else:
                        skipped_sphere_locs.append(i)
                    location.item = None
                    new_item = IDItem(f"{increment} Token{'s' if increment != 1 else ''}", ItemClassification.progression_skip_balancing, increment, self.player)
                    location.place_locked_item(new_item)
            self.random.shuffle(skipped_sphere_locs)
            while skipped_sphere_locs and extra_items_to_place:
                add_location(extra_items_to_place.pop(), skipped_sphere_locs.pop())
            old_skipped_sphere_locs += skipped_sphere_locs
            old_skipped_sphere_locs.sort(key=lambda i: -i)
            while old_skipped_sphere_locs and extra_items_to_place:
                add_location(extra_items_to_place.pop(), old_skipped_sphere_locs.pop())

            allowed_games = [player for player in active_games if
                             self.multiworld.worlds[player].game in allowed_filler_games]
            if allowed_games:
                while len(old_skipped_sphere_locs) > 50:
                    game = self.random.choice(allowed_games)
                    add_location(self.multiworld.worlds[game].create_filler(), old_skipped_sphere_locs.pop())

        assert not extra_items_to_place
        del skipped_sphere_locs
        del old_skipped_sphere_locs


class IDLocation(Location):
    game = "Item Dispenser"


class IDItem(Item):
    game = "Item Dispenser"
