import typing
import os
import json
from .Items import item_data_table, action_item_data_table, cannon_item_data_table, cap_item_data_table, \
    castle_progression_item_data_table, feature_item_data_table, global_cap_item_names, \
    painting_unlock_item_data_table, item_table, SM64Item, global_checkerboard_item_names, \
    global_rolling_log_item_names, global_purple_switch_item_names, checkerboard_item_data_table, \
    rolling_log_item_data_table, purple_switch_item_data_table, optional_item_data_table, \
    bowser_stage_1up_item_data_table, randomized_action_item_names, per_level_move_area_names, ut_glitch_item_name, \
    item_name_groups, global_coin_object_item_data_table, per_level_coin_object_item_data_table, \
    global_enemy_item_data_table, per_level_enemy_item_data_table, global_mode_coin_object_item_names, \
    global_mode_enemy_item_names, bowser_bomb_item_data_table
from .Locations import location_table, SM64Location, coinsanity_course_data, get_coinsanity_location_name, \
    get_coinsanity_location_names, get_secret_stage_coinsanity_location_names, location_name_groups
from .Music import build_music_slot_data
from .Options import sm64_options_groups, SM64Options, coin_star_requirement_option_names, \
    move_randomizer_option_name_by_action, secret_stage_coinsanity_max_coin_option_names, \
    trap_weight_option_names, trap_item_name_by_option_name
from .Rules import set_rules
from .LogicTricks import get_enabled_logic_tricks, logic_tricks
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
    item_name_groups = item_name_groups
    location_name_groups = location_name_groups

    required_client_version = (0, 3, 5)

    ut_can_gen_without_yaml = True
    glitches_item_name = ut_glitch_item_name

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
        "one_up_checks",
        "blocksanity",
        "easy_butterflies",
        "no_despawns",
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
        "coin_object_unlocks",
        "enemy_unlocks",
        "bowser_bombs",
        "bowser_in_the_dark_world_hits",
        "bowser_in_the_fire_sea_hits",
        "bowser_in_the_sky_hits",
        "bowser_in_the_sky_stage_collapse_hits",
        "bowser_stage_1ups",
        "wet_dry_world_water_level_diamond",
        "tick_tock_clock_spinners",
        "strict_cannon_requirements",
        "strict_move_requirements",
        "logic_tricks",
        "universal_tracker_glitched_logic",
        "marios_hat",
        "mario_hat_color",
        "mario_shirt_color",
        "mario_overalls_color",
        "mario_gloves_color",
        "mario_shoes_color",
        "mario_skin_color",
        "mario_hair_color",
        "music_shuffle",
        "coinsanity",
        "secret_stage_coinsanity",
        *secret_stage_coinsanity_max_coin_option_names,
        *coin_star_requirement_option_names,
        "traps_filler_percentage",
        *trap_weight_option_names,
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

        enabled_logic_tricks = get_enabled_logic_tricks(self.options.logic_tricks.value)
        tracker_logic_tricks = get_enabled_logic_tricks(self.options.universal_tracker_glitched_logic.value)
        for trick, data in logic_tricks.items():
            setattr(self, data["name"], trick in enabled_logic_tricks)
            setattr(self, f"{data['name']}_ut_glitch", trick in tracker_logic_tricks)

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
            if self.options.secret_stage_coinsanity:
                secret_stage_coin_maxes = {
                    option_name: getattr(self.options, option_name).value
                    for option_name in secret_stage_coinsanity_max_coin_option_names
                }
                if (
                        self.options.accessibility == self.options.accessibility.option_full
                        and not self.logic_totwc_coin_mastery
                ):
                    secret_stage_coin_maxes["tower_of_the_wing_cap_coinsanity_max_coins"] = min(
                        secret_stage_coin_maxes["tower_of_the_wing_cap_coinsanity_max_coins"], 31)
                self.coinsanity_location_names += get_secret_stage_coinsanity_location_names(
                    secret_stage_coin_maxes, self.options.coinsanity.value)
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
        item = SM64Item(name, self.get_item_classification(data), data.code, self.player)

        return item

    def get_item_classification(self, item_data):
        if callable(item_data.classification):
            return item_data.classification(self.options)
        return item_data.classification

    def create_event_item(self, name: str) -> Item:
        data = item_data_table[name]
        return SM64Item(name, self.get_item_classification(data), None, self.player)

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
        elif self.options.checkerboard_platforms.value == self.options.checkerboard_platforms.option_per_level:
            item_names += list(checkerboard_item_data_table)

        if self.options.rolling_logs.value == self.options.rolling_logs.option_global:
            item_names += list(global_rolling_log_item_names)
        elif self.options.rolling_logs.value == self.options.rolling_logs.option_per_level:
            item_names += list(rolling_log_item_data_table)

        if self.options.purple_switches.value == self.options.purple_switches.option_global:
            item_names += list(global_purple_switch_item_names)
        elif self.options.purple_switches.value == self.options.purple_switches.option_per_level:
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

    @staticmethod
    def get_unlock_item_names(option, global_mode_item_names, per_level_item_data_table) -> typing.List[str]:
        if option.value == option.option_global:
            return list(global_mode_item_names)
        if option.value == option.option_per_level:
            return list(per_level_item_data_table)
        return []

    def get_coin_object_unlock_item_names(self) -> typing.List[str]:
        return self.get_unlock_item_names(
            self.options.coin_object_unlocks,
            global_mode_coin_object_item_names,
            per_level_coin_object_item_data_table)

    def get_enemy_unlock_item_names(self) -> typing.List[str]:
        return self.get_unlock_item_names(
            self.options.enemy_unlocks,
            global_mode_enemy_item_names,
            per_level_enemy_item_data_table)

    def get_bowser_arena_bomb_item_names(self) -> typing.List[str]:
        if self.options.bowser_bombs.value == self.options.bowser_bombs.option_global:
            return ["Progressive Bowser Arena Bomb"] * 4 + [
                "Bowser in the Sky - Progressive Bowser Arena Bomb"]
        if self.options.bowser_bombs.value == self.options.bowser_bombs.option_per_level:
            return (
                ["Bowser in the Dark World - Progressive Bowser Arena Bomb"] * 4
                + ["Bowser in the Fire Sea - Progressive Bowser Arena Bomb"] * 4
                + ["Bowser in the Sky - Progressive Bowser Arena Bomb"] * 5
            )
        return []

    def get_unrandomized_bowser_arena_bomb_item_names(self) -> typing.List[str]:
        if self.options.bowser_bombs.value == self.options.bowser_bombs.option_not_shuffled:
            return ["Progressive Bowser Arena Bomb"] * 4 + [
                "Bowser in the Sky - Progressive Bowser Arena Bomb"]
        return []

    def get_unrandomized_unlock_item_names(self) -> typing.List[str]:
        item_names = []
        if self.options.coin_object_unlocks.value == self.options.coin_object_unlocks.option_not_shuffled:
            item_names += list(global_coin_object_item_data_table)
            item_names += list(per_level_coin_object_item_data_table)
        if self.options.enemy_unlocks.value == self.options.enemy_unlocks.option_not_shuffled:
            item_names += list(global_enemy_item_data_table)
            item_names += list(per_level_enemy_item_data_table)
        return item_names

    def get_bowser_stage_1up_item_names(self) -> typing.List[str]:
        if self.options.bowser_stage_1ups.value == self.options.bowser_stage_1ups.option_global:
            return ["Bowser Stage Extra 1-Ups"]
        if self.options.bowser_stage_1ups.value == self.options.bowser_stage_1ups.option_per_level:
            return [
                "Bowser in the Dark World - Extra 1-Ups",
                "Bowser in the Fire Sea - Extra 1-Ups",
            ]
        return []

    def get_unrandomized_bowser_stage_1up_item_names(self) -> typing.List[str]:
        if self.options.bowser_stage_1ups.value == self.options.bowser_stage_1ups.option_always_spawn:
            return ["Bowser Stage Extra 1-Ups"]
        return []

    def get_action_item_names(self) -> typing.List[str]:
        item_names = []
        for action in randomized_action_item_names:
            option = getattr(self.options, move_randomizer_option_name_by_action[action])
            if option.value == option.option_global:
                item_names.append(action)
            elif option.value == option.option_per_level:
                item_names += [
                    f"{area_name} - {action}" for area_name in per_level_move_area_names
                    if not (area_name == "Big Boo's Haunt" and action == "Climb")
                ]
        return item_names

    def get_progression_item_names(self) -> typing.List[str]:
        item_names = list(feature_item_data_table)
        item_names += self.get_arbitrary_item_names()
        item_names += self.get_castle_key_item_names()
        item_names += ["Castle - Progressive MIPS"] * 2
        item_names += [
            item_name for item_name in castle_progression_item_data_table
            if item_name != "Castle - Progressive MIPS"
        ]
        item_names += self.get_cap_item_names()
        item_names += self.get_bowser_stage_1up_item_names()

        if self.options.buddy_checks:
            item_names += list(cannon_item_data_table)
        if self.options.enable_locked_paintings:
            item_names += list(painting_unlock_item_data_table)

        item_names += self.get_action_item_names()
        item_names += self.get_coin_object_unlock_item_names()
        item_names += self.get_enemy_unlock_item_names()
        item_names += self.get_bowser_arena_bomb_item_names()

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
        return locked_count
        
    def get_filler_replacements(self, filler_count: int) -> typing.List[str]:
        replacement_names: typing.List[str] = []

        trap_items = []
        trap_weights = []
        for option_name in trap_weight_option_names:
            weight = getattr(self.options, option_name).value
            if weight > 0:
                trap_items.append(trap_item_name_by_option_name[option_name])
                trap_weights.append(weight)

        trap_count = (filler_count * self.options.traps_filler_percentage.value) // 100
        if trap_items: replacement_names.extend(self.random.choices(trap_items, weights=trap_weights, k=trap_count,))
        self.random.shuffle(replacement_names)
        return replacement_names

    def create_items(self):
        item_names = self.get_progression_item_names()
        item_names += self.get_optional_item_names()
        fillable_location_count = len(self.multiworld.get_unfilled_locations(self.player)) - self.get_future_locked_location_count()
        self.filler_count = fillable_location_count - len(item_names)
        if self.filler_count < 0:
            raise OptionError(f"{self.player_name}'s Spicy Mycena 64 world has {abs(self.filler_count)} more "
                              f"required items than randomized locations.")

        replacement_item_names = self.get_filler_replacements(self.filler_count)
        plain_filler_count = self.filler_count - len(replacement_item_names)
        self.multiworld.itempool += [self.create_item(item_name) for item_name in item_names]
        self.multiworld.itempool += [self.create_item(item_name) for item_name in replacement_item_names]
        self.multiworld.itempool += [self.create_item("1-Up Mushroom") for i in range(plain_filler_count)]

    def generate_basic(self):
        if not self.options.buddy_checks:
            for location_name, item_name in (
                    ("Bob-omb Battlefield - Bob-omb Buddy", "Bob-omb Battlefield - Cannon Unlock"),
                    ("Whomp's Fortress - Bob-omb Buddy", "Whomp's Fortress - Cannon Unlock"),
                    ("Jolly Roger Bay - Bob-omb Buddy", "Jolly Roger Bay - Cannon Unlock"),
                    ("Cool, Cool Mountain - Bob-omb Buddy", "Cool, Cool Mountain - Cannon Unlock"),
                    ("Shifting Sand Land - Bob-omb Buddy", "Shifting Sand Land - Cannon Unlock"),
                    ("Snowman's Land - Bob-omb Buddy", "Snowman's Land - Cannon Unlock"),
                    ("Wet-Dry World - Bob-omb Buddy", "Wet-Dry World - Cannon Unlock"),
                    ("Tall, Tall Mountain - Bob-omb Buddy", "Tall, Tall Mountain - Cannon Unlock"),
                    ("Tiny-Huge Island - Bob-omb Buddy", "Tiny-Huge Island - Cannon Unlock"),
                    ("Rainbow Ride - Bob-omb Buddy", "Rainbow Ride - Cannon Unlock"),
                    ("Wing Mario Over the Rainbow - Bob-omb Buddy",
                     "Wing Mario Over the Rainbow - Cannon Unlock"),
            ):
                location = self.multiworld.get_location(location_name, self.player)
                location.address = None
                location.place_locked_item(self.create_event_item(item_name))

    def get_filler_item_name(self) -> str:
        return "1-Up Mushroom"

    @staticmethod
    def get_rgb_color(value: int) -> typing.List[int]:
        return [(value >> 16) & 0xFF, (value >> 8) & 0xFF, value & 0xFF]

    def get_mario_colors_slot_data(self) -> typing.Dict[str, typing.List[int]]:
        return {
            "hat": self.get_rgb_color(self.options.mario_hat_color.value),
            "shirt": self.get_rgb_color(self.options.mario_shirt_color.value),
            "overalls": self.get_rgb_color(self.options.mario_overalls_color.value),
            "gloves": self.get_rgb_color(self.options.mario_gloves_color.value),
            "shoes": self.get_rgb_color(self.options.mario_shoes_color.value),
            "skin": self.get_rgb_color(self.options.mario_skin_color.value),
            "hair": self.get_rgb_color(self.options.mario_hair_color.value),
        }

    def get_coin_star_requirements_slot_data(self) -> typing.List[int]:
        return [
            getattr(self.options, option_name).value
            for option_name in coin_star_requirement_option_names
        ]

    def get_start_inventory_slot_data(self) -> typing.Dict[int, int]:
        start_inventory = {}
        for item_name in (
                self.get_unrandomized_arbitrary_item_names()
                + self.get_unrandomized_optional_item_names()
                + self.get_unrandomized_bowser_stage_1up_item_names()
                + self.get_unrandomized_bowser_arena_bomb_item_names()
                + self.get_unrandomized_unlock_item_names()):
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
            "BowserStage1UpBehavior": self.options.bowser_stage_1ups.value != self.options.bowser_stage_1ups.option_vanilla,
            "OneUpChecks": self.options.one_up_checks.value,
            "Blocksanity": self.options.blocksanity.value,
            "BuddyChecks": self.options.buddy_checks.value,
            "EasyButterflies": self.options.easy_butterflies.value,
            "NoDespawn": self.options.no_despawns.value,
            "BowserInTheDarkWorldHits": self.options.bowser_in_the_dark_world_hits.value,
            "BowserInTheFireSeaHits": self.options.bowser_in_the_fire_sea_hits.value,
            "BowserInTheSkyHits": self.options.bowser_in_the_sky_hits.value,
            "BowserInTheSkyStageCollapseHits": self.options.bowser_in_the_sky_stage_collapse_hits.value,
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
            "location_to_item": {
                location.address: location.item.code
                for location in self.multiworld.get_locations()
                if location.address is not None and location.item is not None and location.item.code is not None
            },
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
                        if location.address is None:
                            continue
                        er_hint_data[location.address] = entrance_name
            hint_data[self.player] = er_hint_data
