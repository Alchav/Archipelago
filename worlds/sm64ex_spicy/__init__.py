import typing
import os
import json
from .Items import item_data_table, action_item_data_table, cannon_item_data_table, cap_item_data_table, \
    castle_progression_item_data_table, feature_item_data_table, global_cap_item_names, \
    painting_unlock_item_data_table, item_table, SM64Item, global_checkerboard_item_names, \
    global_rolling_log_item_names, global_purple_switch_item_names, checkerboard_item_data_table, \
    rolling_log_item_data_table, purple_switch_item_data_table, optional_item_data_table, \
    randomized_action_item_names, per_level_move_area_names
from .Locations import location_table, SM64Location, coinsanity_course_data, get_coinsanity_location_name, \
    get_coinsanity_location_names
from .Music import build_music_slot_data
from .Options import sm64_options_groups, SM64Options, coin_star_requirement_option_names, \
    move_randomizer_option_name_by_action
from .Rules import set_rules
from .Regions import create_regions, sm64_entrance_to_region, sm64_level_to_entrances, SM64Levels
from BaseClasses import Item, Tutorial
from Options import OptionError
from ..AutoWorld import World, WebWorld


class SM64Web(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up SM64EX for MultiWorld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["N00byKing", "Alchav"]
    )]

    option_groups = sm64_options_groups


class SM64World(World):
    """ 
    The first Super Mario game to feature 3D gameplay, it features freedom of movement within a large open world based on polygons,
    combined with traditional Mario gameplay, visual style, and characters.
    """

    game: str = "SM64: Spicy Mycena 64"
    topology_present = False

    web = SM64Web()

    item_name_to_id = item_table
    location_name_to_id = location_table

    required_client_version = (0, 3, 5)

    ut_can_gen_without_yaml = True

    area_connections: typing.Dict[int, int]

    options_dataclass = SM64Options
    options: SM64Options

    number_of_stars: int
    move_rando_bitvec: int
    filler_count: int
    star_costs: typing.Dict[str, int]
    coinsanity_location_names: typing.Tuple[str, ...]
    music_slot_data: typing.Dict[str, typing.Any] | None
    using_slot_coinsanity_locations: bool

    slot_option_names = (
        "area_rando",
        "buddy_checks",
        "exclamation_boxes",
        "combined_progressive_keys",
        "enable_locked_paintings",
        "triple_jump",
        "long_jump",
        "backflip",
        "side_flip",
        "wall_kick",
        "dive",
        "ground_pound",
        "kick",
        "climb",
        "ledge_grab",
        "strict_cap_requirements",
        "per_level_cap_items",
        "hazy_maze_cave_swimming_beast",
        "rainbow_ride_carpets",
        "checkerboard_platforms",
        "tiny_huge_island_warp_pipes",
        "cool_cool_mountain_baby_penguins",
        "snowmans_land_penguin",
        "shifting_sand_land_pyramid_elevator",
        "rolling_logs",
        "purple_switches",
        "wet_dry_world_water_level_diamond",
        "tick_tock_clock_spinners",
        "strict_cannon_requirements",
        "strict_move_requirements",
        "marios_hat",
        "mario_colors",
        "music_shuffle",
        "coinsanity",
        *coin_star_requirement_option_names,
        "death_link",
        "completion_type",
    )

    def generate_early(self):
        slot_data = self.get_re_gen_slot_data()
        self.area_connections = {}
        self.music_slot_data = None
        self.using_slot_coinsanity_locations = False
        if slot_data:
            self.restore_options_from_slot_data(slot_data)
            self.area_connections = {
                int(entrance): int(destination)
                for entrance, destination in slot_data.get("AreaRando", {}).items()
            }
            self.music_slot_data = self.get_music_slot_data_from_slot_data(slot_data)

        self.move_rando_bitvec = 0
        double_jump_bitvec_offset = action_item_data_table['Double Jump'].code
        for action in randomized_action_item_names:
            option = getattr(self.options, move_randomizer_option_name_by_action[action])
            if option.value != option.option_not_shuffled:
                self.move_rando_bitvec |= (1 << (action_item_data_table[action].code - double_jump_bitvec_offset))

        self.filler_count = 0
        self.topology_present = self.options.area_rando
        coin_star_requirements = {
            option_name: getattr(self.options, option_name).value
            for option_name in coin_star_requirement_option_names
        }
        if "CoinsanityLocations" in slot_data:
            self.coinsanity_location_names = tuple(slot_data["CoinsanityLocations"])
            self.using_slot_coinsanity_locations = True
        else:
            self.coinsanity_location_names = get_coinsanity_location_names(
                coin_star_requirements, self.options.coinsanity.value)
        if "MoveRandoVec" in slot_data:
            self.move_rando_bitvec = slot_data["MoveRandoVec"]

    def create_regions(self):
        create_regions(self.multiworld, self.options, self.player)
        if not self.using_slot_coinsanity_locations:
            self.add_overflow_coinsanity_locations()
        coin_check_region_names = {
            "Tiny-Huge Island": "Tiny-Huge Island - Coins",
        }
        for location_name in self.coinsanity_location_names:
            region_name = location_name.rsplit(" - ", 1)[0]
            region_name = coin_check_region_names.get(region_name, region_name)
            region = self.multiworld.get_region(region_name, self.player)
            region.locations.append(SM64Location(self.player, location_name, location_table[location_name], region))

    def set_rules(self):
        set_rules(self.multiworld, self.options, self.player, self.area_connections, self.move_rando_bitvec)
        if self.topology_present:
            # Write area_connections to spoiler log
            for entrance, destination in self.area_connections.items():
                self.multiworld.spoiler.set_entrance(
                    sm64_level_to_entrances[entrance] + " Entrance",
                    sm64_level_to_entrances[destination],
                    'entrance', self.player)

    def create_item(self, name: str) -> Item:
        data = item_data_table[name]
        item = SM64Item(name, data.classification, data.code, self.player)

        return item

    def get_castle_key_item_names(self) -> typing.List[str]:
        if self.options.combined_progressive_keys:
            return ["Progressive Key"] * 6
        return ["Dark World Key"] + ["Progressive Basement Key"] * 2 + ["Progressive Upstairs Key"] * 3

    def get_cap_item_names(self) -> typing.List[str]:
        if self.options.per_level_cap_items:
            return list(cap_item_data_table)
        return list(global_cap_item_names)

    def get_arbitrary_item_names(self) -> typing.List[str]:
        item_names = [
            item_name
            for item_name, option_name in (
                ("Hazy Maze Cave - Swimming Beast", "hazy_maze_cave_swimming_beast"),
                ("Rainbow Ride - Carpets", "rainbow_ride_carpets"),
                ("Tiny-Huge Island - Warp Pipes", "tiny_huge_island_warp_pipes"),
                ("Cool, Cool Mountain - Baby Penguins", "cool_cool_mountain_baby_penguins"),
                ("Snowman's Land - Penguin", "snowmans_land_penguin"),
                ("Shifting Sand Land - Pyramid Elevator", "shifting_sand_land_pyramid_elevator"),
                ("Wet-Dry World - Water Level Diamond", "wet_dry_world_water_level_diamond"),
                ("Tick Tock Clock - Spinners", "tick_tock_clock_spinners"),
            )
            if getattr(self.options, option_name).value
        ]

        if self.options.checkerboard_platforms.value == self.options.checkerboard_platforms.option_global:
            item_names += list(global_checkerboard_item_names)
        elif self.options.checkerboard_platforms.value == self.options.checkerboard_platforms.option_individual:
            item_names += list(checkerboard_item_data_table)

        if self.options.rolling_logs.value == self.options.rolling_logs.option_global:
            item_names += list(global_rolling_log_item_names)
        elif self.options.rolling_logs.value == self.options.rolling_logs.option_individual:
            item_names += list(rolling_log_item_data_table)

        if self.options.purple_switches.value == self.options.purple_switches.option_global:
            item_names += list(global_purple_switch_item_names)
        elif self.options.purple_switches.value == self.options.purple_switches.option_individual:
            item_names += list(purple_switch_item_data_table)

        return item_names

    def get_unrandomized_arbitrary_item_names(self) -> typing.List[str]:
        item_names = [
            item_name
            for item_name, option_name in (
                ("Hazy Maze Cave - Swimming Beast", "hazy_maze_cave_swimming_beast"),
                ("Rainbow Ride - Carpets", "rainbow_ride_carpets"),
                ("Tiny-Huge Island - Warp Pipes", "tiny_huge_island_warp_pipes"),
                ("Cool, Cool Mountain - Baby Penguins", "cool_cool_mountain_baby_penguins"),
                ("Snowman's Land - Penguin", "snowmans_land_penguin"),
                ("Shifting Sand Land - Pyramid Elevator", "shifting_sand_land_pyramid_elevator"),
                ("Wet-Dry World - Water Level Diamond", "wet_dry_world_water_level_diamond"),
                ("Tick Tock Clock - Spinners", "tick_tock_clock_spinners"),
            )
            if not getattr(self.options, option_name).value
        ]

        if self.options.checkerboard_platforms.value == self.options.checkerboard_platforms.option_not_shuffled:
            item_names += list(global_checkerboard_item_names)
            item_names += list(checkerboard_item_data_table)
        if self.options.rolling_logs.value == self.options.rolling_logs.option_not_shuffled:
            item_names += list(global_rolling_log_item_names)
            item_names += list(rolling_log_item_data_table)
        if self.options.purple_switches.value == self.options.purple_switches.option_not_shuffled:
            item_names += list(global_purple_switch_item_names)
            item_names += list(purple_switch_item_data_table)

        return item_names

    def get_optional_item_names(self) -> typing.List[str]:
        if self.options.marios_hat:
            return list(optional_item_data_table)
        return []

    def get_unrandomized_optional_item_names(self) -> typing.List[str]:
        if self.options.marios_hat:
            return []
        return list(optional_item_data_table)

    def get_action_item_names(self) -> typing.List[str]:
        item_names = []
        for action in randomized_action_item_names:
            option = getattr(self.options, move_randomizer_option_name_by_action[action])
            if option.value == option.option_global:
                item_names.append(action)
            elif option.value == option.option_per_level:
                item_names += [f"{area_name} - {action}" for area_name in per_level_move_area_names]
        return item_names

    def get_progression_item_names(self) -> typing.List[str]:
        item_names = list(feature_item_data_table)
        item_names += self.get_arbitrary_item_names()
        item_names += self.get_castle_key_item_names()
        item_names += ["Progressive MIPS"] * 2
        item_names += [
            item_name for item_name in castle_progression_item_data_table
            if item_name != "Progressive MIPS"
        ]
        item_names += self.get_cap_item_names()

        if self.options.buddy_checks:
            item_names += list(cannon_item_data_table)
        if self.options.enable_locked_paintings:
            item_names += list(painting_unlock_item_data_table)

        item_names += self.get_action_item_names()

        return item_names

    def get_item_pool_item_count(self) -> int:
        return len(self.get_progression_item_names()) + len(self.get_optional_item_names())

    def get_coin_star_requirements_by_option(self) -> typing.Dict[str, int]:
        return {
            option_name: getattr(self.options, option_name).value
            for option_name in coin_star_requirement_option_names
        }

    def add_overflow_coinsanity_locations(self) -> None:
        item_count = self.get_item_pool_item_count()
        fillable_location_count = (
            len(self.multiworld.get_unfilled_locations(self.player))
            + len(self.coinsanity_location_names)
            - self.get_future_locked_location_count()
        )
        extra_location_count = item_count - fillable_location_count
        if extra_location_count <= 0:
            return

        coin_star_requirements = self.get_coin_star_requirements_by_option()
        selected_locations = set(self.coinsanity_location_names)
        extra_locations: list[str] = []

        below_threshold_pool = [
            get_coinsanity_location_name(course_name, coin_count)
            for course_name, _course_offset, option_name, _max_coins in coinsanity_course_data
            for coin_count in range(1, coin_star_requirements[option_name])
            if get_coinsanity_location_name(course_name, coin_count) not in selected_locations
        ]
        self.random.shuffle(below_threshold_pool)
        for location_name in below_threshold_pool[:extra_location_count]:
            selected_locations.add(location_name)
            extra_locations.append(location_name)

        remaining_location_count = extra_location_count - len(extra_locations)
        coin_offset = 0
        while remaining_location_count > 0:
            added_this_round = False
            for course_name, _course_offset, option_name, max_coin_star_requirement in coinsanity_course_data:
                coin_count = coin_star_requirements[option_name] + coin_offset
                if coin_count >= max_coin_star_requirement:
                    continue
                location_name = get_coinsanity_location_name(course_name, coin_count)
                if location_name in selected_locations:
                    continue
                selected_locations.add(location_name)
                extra_locations.append(location_name)
                remaining_location_count -= 1
                added_this_round = True
                if remaining_location_count <= 0:
                    break
            if not added_this_round:
                break
            coin_offset += 1

        self.coinsanity_location_names = (*self.coinsanity_location_names, *extra_locations)

    def get_future_locked_location_count(self) -> int:
        locked_count = 0
        if not self.options.buddy_checks:
            locked_count += len(cannon_item_data_table)
        if not self.options.exclamation_boxes:
            locked_count += sum(1 for loc_name in location_table if "1Up Block" in loc_name)
        return locked_count

    def create_items(self):
        item_names = self.get_progression_item_names()
        item_names += self.get_optional_item_names()
        fillable_location_count = len(self.multiworld.get_unfilled_locations(self.player)) - self.get_future_locked_location_count()
        self.filler_count = fillable_location_count - len(item_names)
        if self.filler_count < 0:
            raise OptionError(f"{self.player_name}'s Spicy Mycena 64 world has {abs(self.filler_count)} more "
                              f"required items than randomized locations.")

        self.multiworld.itempool += [self.create_item(item_name) for item_name in item_names]
        self.multiworld.itempool += [self.create_item("1Up Mushroom") for i in range(0, self.filler_count)]

    def generate_basic(self):
        if not self.options.buddy_checks:
            self.multiworld.get_location("Bob-omb Battlefield - Bob-omb Buddy", self.player).place_locked_item(self.create_item("Cannon Unlock - Bob-omb Battlefield"))
            self.multiworld.get_location("Whomp's Fortress - Bob-omb Buddy", self.player).place_locked_item(self.create_item("Cannon Unlock - Whomp's Fortress"))
            self.multiworld.get_location("Jolly Roger Bay - Bob-omb Buddy", self.player).place_locked_item(self.create_item("Cannon Unlock - Jolly Roger Bay"))
            self.multiworld.get_location("Cool, Cool Mountain - Bob-omb Buddy", self.player).place_locked_item(self.create_item("Cannon Unlock - Cool, Cool Mountain"))
            self.multiworld.get_location("Shifting Sand Land - Bob-omb Buddy", self.player).place_locked_item(self.create_item("Cannon Unlock - Shifting Sand Land"))
            self.multiworld.get_location("Snowman's Land - Bob-omb Buddy", self.player).place_locked_item(self.create_item("Cannon Unlock - Snowman's Land"))
            self.multiworld.get_location("Wet-Dry World - Bob-omb Buddy", self.player).place_locked_item(self.create_item("Cannon Unlock - Wet-Dry World"))
            self.multiworld.get_location("Tall, Tall Mountain - Bob-omb Buddy", self.player).place_locked_item(self.create_item("Cannon Unlock - Tall, Tall Mountain"))
            self.multiworld.get_location("Tiny-Huge Island - Bob-omb Buddy", self.player).place_locked_item(self.create_item("Cannon Unlock - Tiny-Huge Island"))
            self.multiworld.get_location("Rainbow Ride - Bob-omb Buddy", self.player).place_locked_item(self.create_item("Cannon Unlock - Rainbow Ride"))
            self.multiworld.get_location("Wing Mario Over the Rainbow - Bob-omb Buddy", self.player).place_locked_item(self.create_item("Cannon Unlock - Wing Mario Over the Rainbow"))

        if not self.options.exclamation_boxes:
            self.multiworld.get_location("Cool, Cool Mountain - 1Up Block Near Snowman", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.multiworld.get_location("Cool, Cool Mountain - 1Up Block Ice Pillar", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.multiworld.get_location("Cool, Cool Mountain - 1Up Block Secret Slide", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.multiworld.get_location("Big Boo's Haunt - 1Up Block Top of Mansion", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.multiworld.get_location("Hazy Maze Cave - 1Up Block above Pit", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.multiworld.get_location("Hazy Maze Cave - 1Up Block Past Rolling Rocks", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.multiworld.get_location("Shifting Sand Land - 1Up Block Outside Pyramid", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.multiworld.get_location("Shifting Sand Land - 1Up Block Pyramid Left Path", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.multiworld.get_location("Shifting Sand Land - 1Up Block Pyramid Back", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.multiworld.get_location("Snowman's Land - 1Up Block Near Moneybags", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.multiworld.get_location("Snowman's Land - 1Up Block inside Igloo", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.multiworld.get_location("Wet-Dry World - 1Up Block in Downtown", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.multiworld.get_location("Tall, Tall Mountain - 1Up Block on Red Mushroom", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.multiworld.get_location("Tiny-Huge Island - 1Up Block THI Small near Start", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.multiworld.get_location("Tiny-Huge Island - 1Up Block THI Large near Start", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.multiworld.get_location("Tiny-Huge Island - 1Up Block Windy Area", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.multiworld.get_location("Tick Tock Clock - 1Up Block Midway Up", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.multiworld.get_location("Tick Tock Clock - 1Up Block at the Top", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.multiworld.get_location("Rainbow Ride - 1Up Block Top of Red Coin Maze", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.multiworld.get_location("Rainbow Ride - 1Up Block Under Fly Guy", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.multiworld.get_location("Rainbow Ride - 1Up Block On House in the Sky", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.multiworld.get_location("Bowser in the Dark World 1Up Block on Tower", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.multiworld.get_location("Bowser in the Dark World 1Up Block near Goombas", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.multiworld.get_location("Cavern of the Metal Cap 1Up Block", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.multiworld.get_location("Vanish Cap Under the Moat 1Up Block", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.multiworld.get_location("Bowser in the Fire Sea 1Up Block Swaying Stairs", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.multiworld.get_location("Bowser in the Fire Sea 1Up Block Near Poles", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.multiworld.get_location("Wing Mario Over the Rainbow 1Up Block", self.player).place_locked_item(self.create_item("1Up Mushroom"))
            self.multiworld.get_location("Bowser in the Sky 1Up Block", self.player).place_locked_item(self.create_item("1Up Mushroom"))

    def get_filler_item_name(self) -> str:
        return "1Up Mushroom"

    def get_mario_colors_slot_data(self) -> typing.Dict[str, typing.List[int]]:
        return {color_name: list(channels) for color_name, channels in self.options.mario_colors.value.items()}

    def get_coin_star_requirements_slot_data(self) -> typing.List[int]:
        return [
            getattr(self.options, option_name).value
            for option_name in coin_star_requirement_option_names
        ]

    def get_start_inventory_slot_data(self) -> typing.Dict[int, int]:
        start_inventory = {}
        for item_name in self.get_unrandomized_arbitrary_item_names() + self.get_unrandomized_optional_item_names():
            item_id = item_table[item_name]
            start_inventory[item_id] = start_inventory.get(item_id, 0) + 1
        return start_inventory

    def get_re_gen_slot_data(self) -> typing.Dict[str, typing.Any]:
        return getattr(self.multiworld, "re_gen_passthrough", {}).get(self.game, {})

    def restore_options_from_slot_data(self, slot_data: typing.Dict[str, typing.Any]) -> None:
        for option_name, value in slot_data.get("Options", {}).items():
            if hasattr(self.options, option_name):
                getattr(self.options, option_name).value = value
        for option_name, value in zip(coin_star_requirement_option_names, slot_data.get("CoinStarRequirements", [])):
            getattr(self.options, option_name).value = value
        if "MusicShuffleMode" in slot_data:
            self.options.music_shuffle.value = slot_data["MusicShuffleMode"]

    def get_music_slot_data_from_slot_data(
            self, slot_data: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any] | None:
        if "MusicShuffleMode" not in slot_data:
            return None
        music_slot_data = {"MusicShuffleMode": slot_data["MusicShuffleMode"]}
        if "MusicMap" in slot_data:
            music_slot_data["MusicMap"] = slot_data["MusicMap"]
        return music_slot_data

    def get_music_slot_data(self) -> typing.Dict[str, typing.Any]:
        if self.music_slot_data is None:
            self.music_slot_data = build_music_slot_data(
                self.options.music_shuffle.value, self.random)
        return self.music_slot_data.copy()

    def fill_slot_data(self):
        slot_data = {
            "Options": self.options.as_dict(*self.slot_option_names),
            "AreaRando": self.area_connections,
            "MoveRandoVec": self.move_rando_bitvec,
            "PaintingRando": self.options.enable_locked_paintings.value,
            "DeathLink": self.options.death_link.value,
            "CompletionType": self.options.completion_type.value,
            "CoinStarRequirements": self.get_coin_star_requirements_slot_data(),
            "CoinsanityLocations": list(self.coinsanity_location_names),
            "StartInventory": self.get_start_inventory_slot_data(),
        }
        slot_data.update(self.get_music_slot_data())
        mario_colors = self.get_mario_colors_slot_data()
        if mario_colors:
            slot_data["MarioColors"] = mario_colors
        return slot_data

    @staticmethod
    def interpret_slot_data(slot_data: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any]:
        return slot_data

    def get_apsm64ex_slot_data(self):
        slot_data = self.fill_slot_data()
        slot_data["StartInventory"] = slot_data["StartInventory"].copy()
        for item in self.multiworld.precollected_items[self.player]:
            if item.code is None:
                continue
            slot_data["StartInventory"][item.code] = slot_data["StartInventory"].get(item.code, 0) + 1
        return slot_data

    def generate_output(self, output_directory: str):
        if self.multiworld.players != 1:
            return
        data = {
            "slot_data": self.get_apsm64ex_slot_data(),
            "location_to_item": {self.location_name_to_id[i.name] : item_table[i.item.name] for i in self.multiworld.get_locations()},
            "data_package": {
                "data": {
                    "games": {
                        self.game: {
                            "item_name_to_id": self.item_name_to_id,
                            "location_name_to_id": self.location_name_to_id
                        }
                    }
                }
            }
        }
        filename = f"{self.multiworld.get_out_file_name_base(self.player)}.apsm64ex"
        with open(os.path.join(output_directory, filename), 'w') as f:
            json.dump(data, f)

    def extend_hint_information(self, hint_data: typing.Dict[int, typing.Dict[int, str]]):
        if self.topology_present:
            er_hint_data = {}
            for entrance, destination in self.area_connections.items():
                destination_name = sm64_level_to_entrances[destination]
                region_name = sm64_entrance_to_region[destination_name]
                if destination_name == "Tiny-Huge Island (Tiny)":
                    continue
                if region_name == "Tick Tock Clock Moving":
                    region_name = "Tick Tock Clock"
                if destination_name == "Tiny-Huge Island (Huge)":
                    # Special rules for Tiny-Huge Island's dual entrances
                    reverse_area_connections = {destination: entrance for entrance, destination in self.area_connections.items()}
                    entrance_name = sm64_level_to_entrances[reverse_area_connections[SM64Levels.TINY_HUGE_ISLAND_HUGE]] \
                                    + ' or ' + sm64_level_to_entrances[reverse_area_connections[SM64Levels.TINY_HUGE_ISLAND_TINY]]
                    regions = [
                        self.multiworld.get_region("Tiny-Huge Island (Huge)", self.player),
                        self.multiworld.get_region("Tiny-Huge Island (Tiny)", self.player),
                    ]
                else:
                    entrance_name = sm64_level_to_entrances[entrance]
                    regions = [self.multiworld.get_region(region_name, self.player)]
                for region in regions[:]:
                    regions += region.subregions
                for region in regions:
                    for location in region.locations:
                        er_hint_data[location.address] = entrance_name
            hint_data[self.player] = er_hint_data
