import re
from typing import Callable, Union, Dict, Set

from BaseClasses import CollectionState, Entrance, MultiWorld
from ..generic.Rules import add_rule, set_rule
from .Locations import locFreestanding1Up_table, location_table, parse_coinsanity_location_name
from .Options import SM64Options, move_randomizer_option_name_by_action
from .Regions import connect_regions, SM64Levels, sm64_entrance_to_region, sm64_level_to_paintings, \
    sm64_level_to_secrets, sm64_secrets_to_level, sm64_entrances_to_level, sm64_level_to_entrances, \
    sm64_ttc_entrances, sm64_wdw_entrances
from .Items import action_item_data_table, cap_item_data_table, per_level_move_area_names, ut_glitch_item_name


initial_reachable_entrances = (
    "Bob-omb Battlefield",
    "Whomp's Fortress",
    "Jolly Roger Bay",
    "Cool, Cool Mountain",
    "The Princess's Secret Slide",
)
minimum_starting_check_count = 2

simple_arbitrary_feature_options = {
    "HMC_SWIMMING_BEAST": ("Hazy Maze Cave - Swimming Beast", "hazy_maze_cave_swimming_beast"),
    "RR_CARPETS": ("Rainbow Ride - Carpets", "rainbow_ride_carpets"),
    "THI_WARP_PIPES": ("Tiny-Huge Island - Warp Pipes", "tiny_huge_island_warp_pipes"),
    "CCM_BABY_PENGUINS": ("Cool, Cool Mountain - Baby Penguins", "cool_cool_mountain_baby_penguins"),
    "SL_PENGUIN": ("Snowman's Land - Penguin", "snowmans_land_penguin"),
    "SSL_PYRAMID_ELEVATOR": ("Shifting Sand Land - Pyramid Elevator", "shifting_sand_land_pyramid_elevator"),
    "WDW_WATER_LEVEL_DIAMOND": ("Wet-Dry World - Water Level Diamond", "wet_dry_world_water_level_diamond"),
    "TTC_SPINNERS": ("Tick Tock Clock - Spinners", "tick_tock_clock_spinners"),
}

checkerboard_item_name_by_level = {
    "Bob-omb Battlefield": "Bob-omb Battlefield - Checkerboard Platforms",
    "Whomp's Fortress": "Whomp's Fortress - Checkerboard Platforms",
    "Lethal Lava Land": "Lethal Lava Land - Checkerboard Platforms",
    "Hazy Maze Cave": "Hazy Maze Cave - Checkerboard Platform",
    "Vanish Cap Under the Moat": "Vanish Cap Under the Moat - Checkerboard Platforms",
}

rolling_log_item_name_by_level = {
    "Lethal Lava Land": "Lethal Lava Land - Rolling Log",
    "Tall, Tall Mountain": "Tall, Tall Mountain - Rolling Log",
}

purple_switch_item_name_by_level = {
    "Bob-omb Battlefield": "Bob-omb Battlefield - Purple Switch",
    "Jolly Roger Bay": "Jolly Roger Bay - Purple Switch",
    "Hazy Maze Cave": "Hazy Maze Cave - Purple Switch",
    "Dire, Dire Docks": "Dire, Dire Docks - Purple Switch",
    "Wet-Dry World": "Wet-Dry World - Purple Switch",
    "Tall, Tall Mountain": "Tall, Tall Mountain - Purple Switch",
    "Tiny-Huge Island": "Tiny-Huge Island - Purple Switch",
    "Rainbow Ride": "Rainbow Ride - Purple Switch",
    "Bowser in the Dark World": "Bowser in the Dark World - Purple Switch",
    "Bowser in the Sky": "Bowser in the Sky - Purple Switch",
}


move_area_name_aliases = {
    "Castle Grounds": "Castle",
    "Castle Courtyard": "Castle",
    "The Princess's Secret Slide": "Castle",
    "The Secret Aquarium": "Castle",
    "Wing Mario Over the Rainbow": "Castle",
    "Tower of the Wing Cap": "Castle",
    "Cavern of the Metal Cap": "Castle",
    "Vanish Cap Under the Moat": "Castle",
    "Bowser in the Dark World": "Castle",
    "Bowser in the Fire Sea": "Castle",
    "Bowser in the Sky": "Castle",
}


def get_move_area_name(level_name: str) -> str:
    return move_area_name_aliases.get(level_name, level_name)


def get_per_level_action_item_name(level_name: str, action: str) -> str | None:
    move_area_name = get_move_area_name(level_name)
    if move_area_name not in per_level_move_area_names:
        return None
    return f"{move_area_name} - {action}"


def has_action(state: CollectionState, player: int, action: str, level_name: str = "Castle") -> bool:
    option_name = move_randomizer_option_name_by_action.get(action)
    if option_name is None:
        return True
    options = state.multiworld.worlds[player].options
    option = getattr(options, option_name)
    if option.value == option.option_not_shuffled:
        return True
    if option.value == option.option_global:
        return state.has(action, player)
    item_name = get_per_level_action_item_name(level_name, action)
    return item_name is None or state.has(item_name, player)


def allows_moveless(state: CollectionState, player: int) -> bool:
    return not state.multiworld.worlds[player].options.strict_move_requirements or state.has(ut_glitch_item_name, player)


def allows_capless(state: CollectionState, player: int) -> bool:
    return not state.multiworld.worlds[player].options.strict_cap_requirements or state.has(ut_glitch_item_name, player)


def has_metal_cap(state: CollectionState, player: int, level_name: str) -> bool:
    options = state.multiworld.worlds[player].options
    item_name = f"{level_name} - Metal Cap" if options.per_level_cap_items else "Metal Cap"
    return state.has(item_name, player)


def has_simple_arbitrary_feature(state: CollectionState, player: int, token: str) -> bool:
    item_name, option_name = simple_arbitrary_feature_options[token]
    options = state.multiworld.worlds[player].options
    return not getattr(options, option_name).value or state.has(item_name, player)


def has_purple_switches(state: CollectionState, player: int, level_name: str) -> bool:
    options = state.multiworld.worlds[player].options
    if options.purple_switches.value == options.purple_switches.option_not_shuffled:
        return True
    if options.purple_switches.value == options.purple_switches.option_global:
        return state.has("Purple Switches", player)
    item_name = purple_switch_item_name_by_level.get(level_name)
    return item_name is None or state.has(item_name, player)


def has_tiny_huge_island_top_return_movement(state: CollectionState, player: int) -> bool:
    level_name = "Tiny-Huge Island"
    return (
        has_action(state, player, "Triple Jump", level_name)
        or has_action(state, player, "Long Jump", level_name) and (
            has_action(state, player, "Side Flip", level_name)
            or has_action(state, player, "Ledge Grab", level_name)
        )
    )


def has_checkerboard_platforms(state: CollectionState, player: int, level_name: str) -> bool:
    options = state.multiworld.worlds[player].options
    if options.checkerboard_platforms.value == options.checkerboard_platforms.option_not_shuffled:
        return True
    if options.checkerboard_platforms.value == options.checkerboard_platforms.option_global:
        return state.has("Checkerboard Platforms", player)
    item_name = checkerboard_item_name_by_level.get(level_name)
    return item_name is None or state.has(item_name, player)


def bob_omb_battlefield_coins(state: CollectionState, player: int, coins: int) -> bool:
    level_name = "Bob-omb Battlefield"
    reachable_coins = 109
    if state.can_reach("Bob-omb Battlefield - Island", "Region", player):
        reachable_coins += 3
        if has_action(state, player, "Climb", level_name):
            reachable_coins += 2
        if any(has_action(state, player, action, level_name) for action in ("Side Flip", "Backflip", "Triple Jump")):
            reachable_coins += 5
        if has_action(state, player, "Triple Jump", level_name):
            reachable_coins += 1
    if state.can_reach("Bob-omb Battlefield - Mario Wings to the Sky", "Location", player):
        reachable_coins += 36
    return coins <= min(reachable_coins, 146)


def whomps_fortress_coins(state: CollectionState, player: int, coins: int) -> bool:
    level_name = "Whomp's Fortress"
    reachable_coins = 73
    if state.can_reach("Whomp's Fortress - Shoot into the Wild Blue", "Location", player):
        reachable_coins += 8
    if has_action(state, player, "Ground Pound", level_name):
        reachable_coins += 40
    if state.can_reach("Whomp's Fortress - Top", "Region", player):
        reachable_coins += 20
    return coins <= reachable_coins


def cool_cool_mountain_coins(state: CollectionState, player: int, coins: int) -> bool:
    level_name = "Cool, Cool Mountain"
    reachable_coins = 130
    has_cannon = state.has("Cannon Unlock - Cool, Cool Mountain", player)
    if has_cannon or allows_moveless(state, player):
        reachable_coins += 11
    if has_cannon:
        reachable_coins += 3
    if has_action(state, player, "Ground Pound", level_name):
        reachable_coins += 10
    return coins <= reachable_coins


def big_boos_haunt_coins(state: CollectionState, player: int, coins: int) -> bool:
    level_name = "Big Boo's Haunt"
    reachable_coins = 88
    if state.can_reach("Big Boo's Haunt - Second Floor", "Region", player):
        reachable_coins += 13
    if state.can_reach("Big Boo's Haunt - Third Floor", "Region", player):
        reachable_coins += 5
        if has_action(state, player, "Ground Pound", level_name):
            reachable_coins += 20
    if state.has("Big Boo's Haunt - Merry-go-round", player):
        reachable_coins += 25
    return coins <= reachable_coins


def hazy_maze_cave_coins(state: CollectionState, player: int, coins: int) -> bool:
    level_name = "Hazy Maze Cave"
    has_basic_movement = any(has_action(state, player, action, level_name)
                             for action in ("Wall Kick", "Ledge Grab", "Backflip", "Side Flip", "Triple Jump"))
    has_long_jump = has_action(state, player, "Long Jump", level_name)
    has_climb = has_action(state, player, "Climb", level_name)
    has_checkerboards = has_checkerboard_platforms(state, player, level_name)
    has_platform_route = has_basic_movement and (
            has_basic_movement and has_climb
            or allows_moveless(state, player) and has_action(state, player, "Wall Kick", level_name))

    reachable_coins = 75
    if has_basic_movement:
        reachable_coins += 4
    if has_platform_route and (has_long_jump or has_checkerboards):
        reachable_coins += 2
    if has_platform_route and has_checkerboards:
        reachable_coins += 2
    if state.can_reach("Hazy Maze Cave - Pit Islands", "Region", player) and has_action(
            state, player, "Climb", level_name):
        reachable_coins += 5
    if has_simple_arbitrary_feature(state, player, "HMC_SWIMMING_BEAST"):
        reachable_coins += 8
    if state.can_reach("Hazy Maze Cave - Navigating the Toxic Maze", "Location", player):
        reachable_coins += 5
    if has_metal_cap(state, player, "Hazy Maze Cave") or (
            allows_capless(state, player) and has_action(state, player, "Triple Jump", level_name)):
        reachable_coins += 3
    if has_action(state, player, "Ground Pound", level_name):
        reachable_coins += 35
    return coins <= reachable_coins


def lethal_lava_land_coins(state: CollectionState, player: int, coins: int) -> bool:
    reachable_coins = 125
    if state.has("Lethal Lava Land - Koopa Shell", player):
        # Technically possible without the shell, but no current option fits that logic.
        reachable_coins += 5
    if state.can_reach("Lethal Lava Land - Elevator Tour in the Volcano", "Location", player):
        reachable_coins += 3
    return coins <= reachable_coins


def shifting_sand_land_coins(state: CollectionState, player: int, coins: int) -> bool:
    level_name = "Shifting Sand Land"
    reachable_coins = 89
    if state.can_reach("Shifting Sand Land - Free Flying for 8 Red Coins", "Location", player):
        reachable_coins += 4
    if has_action(state, player, "Ground Pound", level_name):
        reachable_coins += 15
    if state.can_reach("Shifting Sand Land - Upper Pyramid", "Region", player):
        reachable_coins += 28
    return coins <= reachable_coins


def jolly_roger_bay_coins(state: CollectionState, player: int, coins: int) -> bool:
    level_name = "Jolly Roger Bay"
    reachable_coins = 50
    if (
            has_action(state, player, "Climb", level_name)
            or has_action(state, player, "Triple Jump", level_name)
            or state.has("Cannon Unlock - Jolly Roger Bay", player)
            or allows_moveless(state, player) and (
                has_action(state, player, "Backflip", level_name)
                or has_action(state, player, "Wall Kick", level_name)
            )):
        reachable_coins += 2
    has_upper = state.can_reach("Jolly Roger Bay - Upper", "Region", player)
    has_raised_ship = state.has("Jolly Roger Bay - Raised Ship", player)
    if has_upper:
        reachable_coins += 16
        if has_action(state, player, "Long Jump", level_name) or has_purple_switches(
                state, player, level_name) or has_raised_ship:
            reachable_coins += 2
        if has_raised_ship:
            reachable_coins += 4
    if has_action(state, player, "Ground Pound", level_name):
        reachable_coins += 30
    return coins <= reachable_coins


def dire_dire_docks_coins(state: CollectionState, player: int, coins: int) -> bool:
    level_name = "Dire, Dire Docks"
    reachable_coins = 60
    has_poles = state.has("Dire, Dire Docks - Poles", player)
    has_purple_switch_route = has_purple_switches(state, player, "Dire, Dire Docks")
    has_sub_poles_movement_route = (
            state.has("Dire, Dire Docks - Bowser's Sub", player)
            and has_poles
            and has_action(state, player, "Triple Jump", level_name)
            and has_action(state, player, "Climb", level_name)
    )
    if has_purple_switch_route or has_sub_poles_movement_route:
        reachable_coins += 2
        if has_poles:
            reachable_coins += 14
            if has_purple_switch_route and has_action(state, player, "Ground Pound", level_name):
                reachable_coins += 30
    return coins <= reachable_coins


def snowmans_land_coins(state: CollectionState, player: int, coins: int) -> bool:
    reachable_coins = 102
    if state.has("Cannon Unlock - Snowman's Land", player):
        reachable_coins += 3
    if state.can_reach("Snowman's Land - Snowman's Big Head", "Location", player):
        reachable_coins += 2
    if state.can_reach("Snowman's Land - Into the Igloo", "Location", player):
        reachable_coins += 20
    return coins <= reachable_coins


def wet_dry_world_coins(state: CollectionState, player: int, coins: int) -> bool:
    level_name = "Wet-Dry World"
    has_ground_pound = has_action(state, player, "Ground Pound", level_name)
    has_wdw_purple_switches = has_purple_switches(state, player, "Wet-Dry World")
    has_water_level_diamond = has_simple_arbitrary_feature(state, player, "WDW_WATER_LEVEL_DIAMOND")
    has_triple_jump = has_action(state, player, "Triple Jump", level_name)
    has_dive = has_action(state, player, "Dive", level_name)
    has_movement_top_route = (
        any(has_action(state, player, action, level_name)
            for action in ("Wall Kick", "Triple Jump", "Side Flip", "Backflip"))
        or allows_moveless(state, player)
        or has_wdw_purple_switches and has_action(state, player, "Long Jump", level_name)
    )
    can_reach_mid_high_from_mid = has_water_level_diamond and (has_wdw_purple_switches or has_triple_jump and has_dive)

    def route_water_levels(start_water_level: str) -> Set[str]:
        water_levels = {start_water_level}
        while True:
            previous_count = len(water_levels)
            if has_water_level_diamond:
                if "low" in water_levels:
                    water_levels.add("mid")
                if "mid" in water_levels:
                    water_levels.add("low")
                    if can_reach_mid_high_from_mid:
                        water_levels.add("mid-high")
                if "mid-high" in water_levels:
                    water_levels.add("mid")
                if "high" in water_levels:
                    water_levels.add("mid-high")
                if "highest" in water_levels:
                    water_levels.add("high")
            if "mid-high" in water_levels and route_has_top(water_levels):
                water_levels.add("high")
            if len(water_levels) == previous_count:
                return water_levels

    def route_has_top(water_levels: Set[str]) -> bool:
        return has_movement_top_route or "highest" in water_levels

    def route_has_downtown(water_levels: Set[str]) -> bool:
        return (
            "highest" in water_levels
            or state.has("Cannon Unlock - Wet-Dry World", player)
            or route_has_top(water_levels) and allows_moveless(state, player) and has_triple_jump and has_dive
        )

    def route_coins(start_water_level: str) -> int:
        water_levels = route_water_levels(start_water_level)
        route_total = 0
        if "low" in water_levels:
            route_total += 22
            if has_ground_pound:
                route_total += 30
        if "high" in water_levels:
            route_total += 22
        if water_levels.intersection({"low", "mid"}):
            route_total += 3
        if water_levels.intersection({"mid", "highest"}) or has_wdw_purple_switches or (has_triple_jump and has_dive):
            route_total += 5
        if route_has_top(water_levels):
            route_total += 15
        if has_wdw_purple_switches or (has_movement_top_route and any(has_action(state, player, action, level_name)
                                                                      for action in ("Long Jump", "Triple Jump",
                                                                                     "Ledge Grab"))):
            route_total += 10
        if route_has_downtown(water_levels):
            route_total += 31
            if has_water_level_diamond:
                route_total += 14
        return route_total

    reachable_variant_starts = (
        ("Wet-Dry World Low", "low"),
        ("Wet-Dry World Middle", "mid"),
        ("Wet-Dry World High", "highest"),
    )
    reachable_totals = [route_coins(start_water_level)
                        for variant_region, start_water_level in reachable_variant_starts
                        if state.can_reach(variant_region, "Region", player)]
    return coins <= min(max(reachable_totals, default=0), 152)


def tall_tall_mountain_coins(state: CollectionState, player: int, coins: int) -> bool:
    level_name = "Tall, Tall Mountain"
    reachable_coins = 15
    if state.can_reach("Tall, Tall Mountain - Middle", "Region", player):
        reachable_coins += 55
    if has_action(state, player, "Climb", level_name) or allows_moveless(state, player):
        reachable_coins += 5
    if state.can_reach("Tall, Tall Mountain - Top", "Region", player):
        reachable_coins += 59
        if has_purple_switches(state, player, "Tall, Tall Mountain") or any(
                has_action(state, player, action, level_name) for action in ("Triple Jump", "Backflip", "Side Flip")):
            reachable_coins += 2
        if has_purple_switches(state, player, "Tall, Tall Mountain") or has_action(
                state, player, "Triple Jump", level_name):
            reachable_coins += 1
    return coins <= reachable_coins


def tiny_huge_island_coins(state: CollectionState, player: int, coins: int) -> bool:
    level_name = "Tiny-Huge Island"
    has_warp_pipes = has_simple_arbitrary_feature(state, player, "THI_WARP_PIPES")
    has_thi_purple_switches = has_purple_switches(state, player, "Tiny-Huge Island")
    has_long_jump = has_action(state, player, "Long Jump", level_name)
    has_top_return_movement = has_tiny_huge_island_top_return_movement(state, player)
    has_huge_piranha_area_reentry = (has_warp_pipes and has_thi_purple_switches) or has_top_return_movement
    has_huge_top_gate = state.has("Cannon Unlock - Tiny-Huge Island", player) or has_top_return_movement
    has_ground_pound = has_action(state, player, "Ground Pound", level_name)
    can_enter_tiny = state.can_reach("Tiny-Huge Island (Tiny)", "Region", player)
    can_enter_huge = state.can_reach("Tiny-Huge Island (Huge)", "Region", player)
    can_reach_tiny_piranha_area = state.can_reach("Tiny-Huge Island - Tiny Piranha Area", "Region", player)
    can_reach_tiny_main = state.can_reach("Tiny-Huge Island - Tiny Main", "Region", player)
    can_reach_huge_piranha_area = state.can_reach("Tiny-Huge Island - Huge Piranha Area", "Region", player)
    can_reach_wiggler = state.can_reach("Tiny-Huge Island - Make Wiggler Squirm", "Location", player)

    def route_coins(has_tiny_side: bool, has_huge_side: bool) -> int:
        route_total = 0
        if has_tiny_side:
            route_total += 1
            if can_reach_tiny_piranha_area:
                route_total += 1
            if can_reach_tiny_main:
                route_total += 31
        if has_huge_side:
            route_total += 54
            if has_huge_top_gate:
                route_total += 21
            if has_ground_pound:
                route_total += 46
                if has_huge_top_gate:
                    route_total += 8
            if has_action(state, player, "Wall Kick", level_name) and has_huge_top_gate:
                route_total += 4
            if can_reach_wiggler:
                route_total += 10
            if state.has("Cannon Unlock - Tiny-Huge Island", player) or has_long_jump:
                route_total += 5
        if can_reach_huge_piranha_area and (not has_huge_side or has_huge_piranha_area_reentry):
            route_total += 10
        return route_total

    reachable_totals = []
    if can_enter_tiny:
        reachable_totals.append(route_coins(True, False))
    if can_enter_huge:
        reachable_totals.append(route_coins(has_warp_pipes, True))
    return coins <= max(reachable_totals, default=0)


def tick_tock_clock_coins(state: CollectionState, player: int, coins: int) -> bool:
    level_name = "Tick Tock Clock"
    reachable_coins = 17
    if state.can_reach("Tick Tock Clock - Lower", "Region", player):
        reachable_coins += 13
        if has_simple_arbitrary_feature(state, player, "TTC_SPINNERS"):
            reachable_coins += 6
        if state.can_reach("Tick Tock Clock Moving", "Region", player) or (
                state.can_reach("Tick Tock Clock Stopped", "Region", player) and any(
                    has_action(state, player, action, level_name)
                    for action in ("Ledge Grab", "Backflip", "Triple Jump", "Wall Kick")
                )):
            reachable_coins += 5
    if state.can_reach("Tick Tock Clock - Upper", "Region", player):
        reachable_coins += 6
        if has_action(state, player, "Ground Pound", level_name):
            reachable_coins += 35
    if state.can_reach("Tick Tock Clock - Top", "Region", player):
        reachable_coins += 16
    if state.can_reach("Tick Tock Clock - Top Past Spinners", "Region", player):
        reachable_coins += 30
    return coins <= min(reachable_coins, 128)


def rainbow_ride_coins(state: CollectionState, player: int, coins: int) -> bool:
    level_name = "Rainbow Ride"
    reachable_coins = 0
    has_carpets = has_simple_arbitrary_feature(state, player, "RR_CARPETS")
    if has_carpets or (
            allows_moveless(state, player) and has_action(state, player, "Long Jump", level_name) and
            has_action(state, player, "Triple Jump", level_name) and
            has_action(state, player, "Ledge Grab", level_name)):
        reachable_coins += 8
    if state.can_reach("Rainbow Ride - Beneath the Pole", "Region", player):
        reachable_coins += 27
    if state.can_reach("Rainbow Ride - Maze", "Region", player):
        reachable_coins += 23
        if has_action(state, player, "Ground Pound", level_name):
            reachable_coins += 5
        if has_action(state, player, "Long Jump", level_name) or has_action(state, player, "Wall Kick", level_name):
            reachable_coins += 2
    if has_action(state, player, "Ground Pound", level_name) and has_action(state, player, "Wall Kick", level_name):
        reachable_coins += 25
    if state.can_reach("Rainbow Ride - Coins Amassed in a Maze", "Location", player):
        reachable_coins += 14
    if state.can_reach("Rainbow Ride - Carpets", "Region", player):
        reachable_coins += 2
    if state.can_reach("Rainbow Ride - House", "Region", player):
        reachable_coins += 20
    if state.can_reach("Rainbow Ride - Cruiser", "Region", player):
        reachable_coins += 15
    if state.can_reach("Rainbow Ride - Somewhere Over the Rainbow", "Location", player):
        reachable_coins += 5
    return coins <= min(reachable_coins, 146)


def shuffle_dict_keys(multiworld: MultiWorld, dictionary: dict) -> dict:
    keys = list(dictionary.keys())
    values = list(dictionary.values())
    multiworld.random.shuffle(keys)
    return dict(zip(keys, values))

def fix_reg(entrance_map: Dict[SM64Levels, str], entrance: SM64Levels, invalid_regions: Set[str],
            swapdict: Dict[SM64Levels, str], multiworld: MultiWorld):
    if entrance_map[entrance] in invalid_regions: # Unlucky :C
        replacement_regions = [(rand_entrance, rand_region) for rand_entrance, rand_region in swapdict.items()
                               if rand_region not in invalid_regions]
        rand_entrance, rand_region = multiworld.random.choice(replacement_regions)
        old_dest = entrance_map[entrance]
        entrance_map[entrance], entrance_map[rand_entrance] = rand_region, old_dest
        swapdict[entrance], swapdict[rand_entrance] = rand_region, old_dest
    swapdict.pop(entrance)


def is_starting_check_location(location_name: str, options: SM64Options) -> bool:
    if not options.exclamation_boxes and "1Up Block" in location_name:
        return False
    if not options.buddy_checks and location_name.endswith(" - Bob-omb Buddy"):
        return False
    return True


def get_starting_check_sources(options: SM64Options) -> tuple[str, ...]:
    if options.enable_locked_paintings:
        return ("Bob-omb Battlefield", "The Princess's Secret Slide")
    return initial_reachable_entrances


def get_randomized_entrance_connections(multiworld: MultiWorld, player: int) -> Dict[str, Entrance]:
    return {
        entrance.name.split(" -> ", 1)[1]: entrance
        for entrance in multiworld.get_entrances(player)
        if " -> " in entrance.name and entrance.name.split(" -> ", 1)[1] in sm64_entrances_to_level
        and entrance.parent_region.name not in sm64_wdw_entrances
    }


def has_reachable_starting_check(
        multiworld: MultiWorld, options: SM64Options, player: int,
        allowed_source_entrances: tuple[str, ...] | None = None,
        randomized_entrance_connections: Dict[str, Entrance] | None = None) -> bool:
    if allowed_source_entrances is None:
        allowed_source_entrances = get_starting_check_sources(options)
    if randomized_entrance_connections is None:
        randomized_entrance_connections = get_randomized_entrance_connections(multiworld, player)

    allowed_source_entrance_set = set(allowed_source_entrances)
    disabled_connections = {}
    for source_entrance, entrance in randomized_entrance_connections.items():
        if source_entrance not in allowed_source_entrance_set:
            disabled_connections[entrance] = entrance.access_rule
            entrance.access_rule = lambda state: False

    try:
        state = CollectionState(multiworld)
        reachable_check_count = 0
        for location in multiworld.get_locations(player):
            if is_starting_check_location(location.name, options) and location.can_reach(state):
                reachable_check_count += 1
                if reachable_check_count >= minimum_starting_check_count:
                    return True
        return False
    finally:
        for entrance, access_rule in disabled_connections.items():
            entrance.access_rule = access_rule


def retarget_entrance(entrance: Entrance, target_region_name: str, multiworld: MultiWorld, player: int) -> None:
    target_region = multiworld.get_region(target_region_name, player)
    if entrance.connected_region is target_region:
        return
    if entrance.connected_region:
        entrance.connected_region.entrances.remove(entrance)
    entrance.connected_region = target_region
    target_region.entrances.append(entrance)


def sources_share_entrance_pool(source: str, donor: str, options: SM64Options) -> bool:
    source_is_course = sm64_entrances_to_level[source] in sm64_level_to_paintings
    donor_is_course = sm64_entrances_to_level[donor] in sm64_level_to_paintings
    if options.area_rando == options.area_rando.option_Courses_Only:
        return source_is_course and donor_is_course
    if options.area_rando == options.area_rando.option_Courses_and_Secrets:
        return True
    return source_is_course == donor_is_course


def has_valid_fixed_assignments(entrance_map: Dict[SM64Levels, str]) -> bool:
    if entrance_map[SM64Levels.BOWSER_IN_THE_FIRE_SEA] == "Dire, Dire Docks":
        return False
    invalid_cotmc_destinations = {"Hazy Maze Cave"}
    if entrance_map[SM64Levels.BOWSER_IN_THE_FIRE_SEA] == "Hazy Maze Cave":
        invalid_cotmc_destinations.add("Dire, Dire Docks")
    return entrance_map[SM64Levels.CAVERN_OF_THE_METAL_CAP] not in invalid_cotmc_destinations


def ensure_reachable_starting_check(
        multiworld: MultiWorld, options: SM64Options, player: int,
        randomized_entrances: Dict[SM64Levels, str], randomized_entrances_s: Dict[str, str],
        randomized_entrance_connections: Dict[str, Entrance]) -> None:
    starting_check_sources = get_starting_check_sources(options)
    if has_reachable_starting_check(
            multiworld, options, player, starting_check_sources, randomized_entrance_connections):
        return

    for source in starting_check_sources:
        source_connection = randomized_entrance_connections[source]
        old_source_destination = randomized_entrances_s[source]
        old_source_region = sm64_entrance_to_region[old_source_destination]

        for donor, donor_destination in randomized_entrances_s.items():
            if donor == source or not sources_share_entrance_pool(source, donor, options):
                continue

            source_level = sm64_entrances_to_level[source]
            donor_level = sm64_entrances_to_level[donor]
            swapped_entrances = randomized_entrances.copy()
            swapped_entrances[source_level], swapped_entrances[donor_level] = \
                donor_destination, old_source_destination
            if not has_valid_fixed_assignments(swapped_entrances):
                continue

            donor_connection = randomized_entrance_connections[donor]
            old_donor_region = sm64_entrance_to_region[donor_destination]
            retarget_entrance(source_connection, old_donor_region, multiworld, player)
            retarget_entrance(donor_connection, old_source_region, multiworld, player)

            if has_reachable_starting_check(
                    multiworld, options, player, starting_check_sources, randomized_entrance_connections):
                randomized_entrances[source_level], randomized_entrances[donor_level] = \
                    donor_destination, old_source_destination
                randomized_entrances_s[source], randomized_entrances_s[donor] = \
                    donor_destination, old_source_destination
                return

            retarget_entrance(source_connection, old_source_region, multiworld, player)
            retarget_entrance(donor_connection, old_donor_region, multiworld, player)

    raise Exception("Unable to place enough reachable starting checks in initially accessible SM64 entrances.")

def set_rules(multiworld: MultiWorld, options: SM64Options, player: int, area_connections: dict, move_rando_bitvec: int):
    using_slot_area_connections = bool(area_connections)
    if using_slot_area_connections:
        randomized_entrances = {
            int(entrance_lvl): sm64_level_to_entrances[int(destination_lvl)]
            for entrance_lvl, destination_lvl in area_connections.items()
        }
    else:
        randomized_level_to_paintings = sm64_level_to_paintings.copy()
        randomized_level_to_secrets = sm64_level_to_secrets.copy()

        if options.area_rando > options.area_rando.option_Off:  # Some randomization is happening, randomize Courses
            randomized_level_to_paintings = shuffle_dict_keys(multiworld, sm64_level_to_paintings)

        if options.area_rando == options.area_rando.option_Courses_and_Secrets_Separate:  # Randomize Secrets as well
            randomized_level_to_secrets = shuffle_dict_keys(multiworld, sm64_level_to_secrets)

        randomized_entrances = {**randomized_level_to_paintings, **randomized_level_to_secrets} # Concatenate courses and secrets for rest

        if options.area_rando == options.area_rando.option_Courses_and_Secrets:  # Randomize Courses and Secrets in one pool
            randomized_entrances = shuffle_dict_keys(multiworld, randomized_entrances)

        if options.area_rando > options.area_rando.option_Off:
            # Now, fix assignment if necessary
            swapdict = randomized_entrances.copy()
            # Guarantee BITFS is not mapped to DDD
            fix_reg(randomized_entrances, SM64Levels.BOWSER_IN_THE_FIRE_SEA, {"Dire, Dire Docks"}, swapdict, multiworld)
            # Guarantee COTMC is not mapped to HMC, cuz thats impossible. If BitFS -> HMC, also no COTMC -> DDD.
            if randomized_entrances[SM64Levels.BOWSER_IN_THE_FIRE_SEA] == "Hazy Maze Cave":
                fix_reg(randomized_entrances, SM64Levels.CAVERN_OF_THE_METAL_CAP,
                        {"Hazy Maze Cave", "Dire, Dire Docks"}, swapdict, multiworld)
            else:
                fix_reg(randomized_entrances, SM64Levels.CAVERN_OF_THE_METAL_CAP, {"Hazy Maze Cave"}, swapdict,
                        multiworld)

    randomized_entrances_s = {sm64_level_to_entrances[entrance_lvl]: destination for (entrance_lvl,destination) in randomized_entrances.items()}
    randomized_entrance_connections = {}

    rf = RuleFactory(multiworld, options, player, move_rando_bitvec)

    def connect_randomized_entrance(source: str, source_entrance: str, rule=None):
        destination_entrance = randomized_entrances_s[source_entrance]
        target_region = sm64_entrance_to_region[destination_entrance]
        entrance = connect_regions(
            multiworld, player, source, target_region, rule,
            name=f"{source} -> {source_entrance}"
        )
        randomized_entrance_connections[source_entrance] = entrance
        return entrance

    def has_first_floor_key(state):
        return state.has("Dark World Key", player) or state.has("Progressive Key", player, 1)

    def has_basement_key(state):
        return state.has("Basement Key", player) or state.has("Progressive Basement Key", player, 1) or \
            state.has("Progressive Key", player, 2)

    def has_thirty_star_key(state):
        return state.has("Progressive Basement Key", player, 2) or state.has("Progressive Key", player, 3)

    def has_second_floor_key(state):
        return state.has("Second Floor Key", player) or state.has("Progressive Upstairs Key", player, 1) or \
            state.has("Progressive Key", player, 4)

    def has_third_floor_key(state):
        return state.has("Progressive Upstairs Key", player, 2) or state.has("Progressive Key", player, 5)

    def has_endless_stairs_key(state):
        return state.has("Progressive Upstairs Key", player, 3) or state.has("Progressive Key", player, 6)

    def has_bowser_stage_1up_unlock(state, stage_item_name: str, vanilla_key_rule: Callable) -> bool:
        option = options.bowser_stage_1ups
        if option.value == option.option_always_spawn:
            return True
        if option.value == option.option_vanilla:
            return vanilla_key_rule(state)
        if option.value == option.option_global:
            return state.has("Bowser Stage Extra 1-Ups", player)
        return state.has(stage_item_name, player)

    connect_randomized_entrance("Menu", "Bob-omb Battlefield")
    connect_randomized_entrance("Menu", "Whomp's Fortress",
                                rf.build_rule("", painting_lvl_name="Whomp's Fortress"))
    # JRB door is separated from JRB itself because the secret aquarium can be accessed without entering the painting
    connect_regions(multiworld, player, "Menu", "Jolly Roger Bay Door")
    connect_randomized_entrance("Jolly Roger Bay Door", "Jolly Roger Bay",
                                rf.build_rule("", painting_lvl_name="Jolly Roger Bay"))
    connect_randomized_entrance("Menu", "Cool, Cool Mountain",
                                rf.build_rule("", painting_lvl_name="Cool, Cool Mountain"))
    connect_randomized_entrance("Menu", "Big Boo's Haunt",
                                lambda state: state.has("Courtyard Boos", player))
    connect_randomized_entrance("Menu", "The Princess's Secret Slide")
    connect_randomized_entrance("Jolly Roger Bay Door", "The Secret Aquarium",
                                rf.build_rule("SF/BF | TJ & LG | MOVELESS & TJ"))
    connect_randomized_entrance("Menu", "Tower of the Wing Cap",
                                lambda state: state.has("Wing Cap Light", player))
    connect_randomized_entrance("Menu", "Bowser in the Dark World", has_first_floor_key)

    connect_regions(multiworld, player, "Menu", "Basement", has_basement_key)

    connect_randomized_entrance("Basement", "Hazy Maze Cave")
    connect_randomized_entrance("Basement", "Lethal Lava Land",
                                rf.build_rule("", painting_lvl_name="Lethal Lava Land"))
    connect_randomized_entrance("Basement", "Shifting Sand Land",
                                rf.build_rule("", painting_lvl_name="Shifting Sand Land"))
    ddd_entry_rule = rf.build_rule("", painting_lvl_name="Dire, Dire Docks")
    connect_randomized_entrance("Basement", "Dire, Dire Docks",
                                lambda state: has_thirty_star_key(state) and ddd_entry_rule(state))
    connect_randomized_entrance("Hazy Maze Cave", "Cavern of the Metal Cap",
                                rf.build_rule("HMC_SWIMMING_BEAST"))
    connect_randomized_entrance("Menu", "Vanish Cap Under the Moat",
                                lambda state: state.has("Unlock Vanish Cap Under the Moat", player))
    connect_randomized_entrance("Basement", "Bowser in the Fire Sea",
                                lambda state: has_thirty_star_key(state) and
                                state.has("Unlock Bowser in the Fire Sea", player))

    connect_regions(multiworld, player, "Menu", "Second Floor", has_second_floor_key)

    connect_randomized_entrance("Second Floor", "Snowman's Land",
                                rf.build_rule("", painting_lvl_name="Snowman's Land"))
    for wdw_entrance in sm64_wdw_entrances:
        wdw_entrance_rule = "LG & TJ/SF/BF" if wdw_entrance == "Wet-Dry World High" else ""
        connect_randomized_entrance("Second Floor", wdw_entrance,
                                    rf.build_rule(wdw_entrance_rule, painting_lvl_name="Wet-Dry World"))
    connect_randomized_entrance("Second Floor", "Tall, Tall Mountain",
                                rf.build_rule("", painting_lvl_name="Tall, Tall Mountain"))
    connect_randomized_entrance("Second Floor", "Tiny-Huge Island (Tiny)",
                                rf.build_rule("", painting_lvl_name="Tiny-Huge Island"))
    connect_randomized_entrance("Second Floor", "Tiny-Huge Island (Huge)",
                                rf.build_rule("", painting_lvl_name="Tiny-Huge Island"))
    connect_regions(multiworld, player, "Tiny-Huge Island - Tiny Piranha Area", "Tiny-Huge Island - Huge Piranha Area",
                    name="Tiny-Huge Island - Tiny Piranha Area to Huge Piranha Area")
    connect_regions(multiworld, player, "Tiny-Huge Island (Huge)", "Tiny-Huge Island (Tiny)",
                    name="Tiny-Huge Island - Huge Island to Tiny Island")

    connect_regions(multiworld, player, "Second Floor", "Third Floor", has_third_floor_key)

    for ttc_entrance in sm64_ttc_entrances:
        connect_randomized_entrance("Third Floor", ttc_entrance,
                                    rf.build_rule("LG/TJ/SF/BF/WK", painting_lvl_name="Tick Tock Clock"))
    connect_randomized_entrance("Third Floor", "Rainbow Ride", rf.build_rule("TJ/SF/BF"))
    connect_randomized_entrance("Third Floor", "Wing Mario Over the Rainbow",
                                rf.build_rule("TJ/SF/BF"))
    connect_regions(multiworld, player, "Third Floor", "Bowser in the Sky", has_endless_stairs_key)

    # Course Rules
    # Bob-omb Battlefield
    rf.assign_rule("Bob-omb Battlefield - Big Bob-Omb on the Summit", "BOB_KING")
    rf.assign_rule("Bob-omb Battlefield - Footrace with Koopa The Quick", "BOB_KOOPA")
    rf.assign_rule("Bob-omb Battlefield - Island", "CANN | CANNLESS & WC & TJ | CAPLESS & CANNLESS & LJ")
    rf.assign_rule("Bob-omb Battlefield - Mario Wings to the Sky",  "CANN & WC | CAPLESS & CANN")
    rf.assign_rule("Bob-omb Battlefield - Behind Chain Chomp's Gate", "GP | MOVELESS")
    rf.assign_rule("Bob-omb Battlefield - Bob-omb Buddy", "BOB_BUDDY")
    rf.assign_rule("Bob-omb Battlefield - Cannon Tree 1-Up", "CL/TJ/BF/SF")
    # Whomp's Fortress
    rf.assign_rule("Whomp's Fortress - To the Top of the Fortress", "WF_FORTRESS")
    rf.assign_rule("Whomp's Fortress - Chip Off Whomp's Block", "WF_KING & GP")
    rf.assign_rule("Whomp's Fortress - Top", "CHECKERBOARD_PLATFORMS | WF_HOOT | WK & SF/TJ")
    rf.assign_rule("Whomp's Fortress - Shoot into the Wild Blue", "WK & TJ/SF | CANN")
    rf.assign_rule("Whomp's Fortress - Red Coins on the Floating Isle", "WF_FORTRESS")
    rf.assign_rule("Whomp's Fortress - Fall onto the Caged Island",
                   "WF_HOOT | CL & WF_FORTRESS & {Whomp's Fortress - Top} | "
                   "MOVELESS & TJ & WF_FORTRESS & {Whomp's Fortress - Top} | "
                   "MOVELESS & LJ & WF_FORTRESS & {Whomp's Fortress - Top} | MOVELESS & CANN")
    rf.assign_rule("Whomp's Fortress - Blast Away the Wall", "CANN | CANNLESS & LG")
    rf.assign_rule("Whomp's Fortress - Bob-omb Buddy", "WF_BUDDY")
    rf.assign_rule("Whomp's Fortress - Flagpole 1-Up", "CL")
    rf.assign_rule("Whomp's Fortress - Tower Alcove 1-Up", "WF_FORTRESS")
    # Jolly Roger Bay
    rf.assign_rule("Jolly Roger Bay - Plunder in the Sunken Ship", "JRB_SUNKEN_SHIP")
    rf.assign_rule("Jolly Roger Bay - Can the Eel Come Out to Play?", "JRB_UNAGI")
    rf.assign_rule("Jolly Roger Bay - Upper", "TJ/BF/SF/WK | MOVELESS & LG")
    rf.assign_rule("Jolly Roger Bay - Red Coins on the Ship Afloat",
                   "JRB_RAISED_SHIP & CL/TJ | JRB_RAISED_SHIP & CANN | "
                   "JRB_RAISED_SHIP & MOVELESS & BF/WK")
    rf.assign_rule("Jolly Roger Bay - Blast to the Stone Pillar",
                   "CANN+CL | CANNLESS & MOVELESS | CANN & MOVELESS")
    rf.assign_rule("Jolly Roger Bay - Through the Jet Stream", "JRB_JET_STREAM & MC/CAPLESS")
    rf.assign_rule("Jolly Roger Bay - Bob-omb Buddy", "JRB_BUDDY")
    rf.assign_rule("Jolly Roger Bay - Stone Pillar 1-Up", "CANN")
    # Cool, Cool Mountain
    rf.assign_rule("Cool, Cool Mountain - Big Penguin Race", "CCM_BIG_PENGUIN")
    rf.assign_rule("Cool, Cool Mountain - Snowman's Lost His Head", "CCM_SNOWMAN_HEAD")
    rf.assign_rule("Cool, Cool Mountain - Li'l Penguin Lost", "CCM_BABY_PENGUINS")
    rf.assign_rule("Cool, Cool Mountain - Wall Kicks Will Work", "TJ/WK & CANN | CANNLESS & TJ/WK | MOVELESS")
    rf.assign_rule("Cool, Cool Mountain - Snowman Tree 1-Up", "CL/TJ/BF/SF")
    # Big Boo's Haunt
    rf.assign_rule("Big Boo's Haunt - Ride Big Boo's Merry-Go-Round", "BBH_MERRY_GO_ROUND")
    rf.assign_rule("Big Boo's Haunt - Second Floor", "BBH_STAIRCASE | WK & TJ/SF")
    rf.assign_rule("Big Boo's Haunt - Third Floor", "WK+LG | MOVELESS & WK")
    rf.assign_rule("Big Boo's Haunt - Roof", "LJ | MOVELESS")
    rf.assign_rule("Big Boo's Haunt - Secret of the Haunted Books", "KK | MOVELESS")
    rf.assign_rule("Big Boo's Haunt - Seek the 8 Red Coins", "BF/WK/TJ/SF")
    rf.assign_rule("Big Boo's Haunt - Eye to Eye in the Secret Room", "VC")
    rf.assign_rule("Big Boo's Haunt - Shed Roof 1-Up", "TJ/SF/WK")
    # Haze Maze Cave
    rf.assign_rule("Hazy Maze Cave - Swimming Beast in the Cavern", "HMC_SWIMMING_BEAST")
    rf.assign_rule("Hazy Maze Cave - Red Coin Area",
                   "CHECKERBOARD_PLATFORMS & CL & WK/LG/BF/SF/TJ | CHECKERBOARD_PLATFORMS & MOVELESS & WK")
    rf.assign_rule("Hazy Maze Cave - Pit Islands", "TJ+CL | MOVELESS & WK & TJ/LJ | MOVELESS & WK+SF+LG")
    rf.assign_rule("Hazy Maze Cave - Metal-Head Mario Can Move!",
                   "PURPLE_SWITCHES & LJ+MC | CAPLESS & LJ+TJ | "
                   "CAPLESS & MOVELESS & LJ/TJ/WK")
    rf.assign_rule("Hazy Maze Cave - Navigating the Toxic Maze", "WK/SF/BF/TJ")
    rf.assign_rule("Hazy Maze Cave - Watch for Rolling Rocks", "WK")
    rf.assign_rule("Hazy Maze Cave - Blue Coin Trail Monty Moles", "WK/SF/BF/TJ")
    rf.assign_rule("Hazy Maze Cave - Twin Hole Monty Moles", "WK/SF/BF/TJ")
    # Lethal Lava Land
    rf.assign_rule("Lethal Lava Land - Red-Hot Log Rolling", "WC | LLL_ROLLING_LOG | LLL_KOOPA_SHELL | MOVELESS+CAPLESS")
    rf.assign_rule("Lethal Lava Land - Upper Volcano", "CL")
    rf.assign_rule("Lethal Lava Land - Elevator Tour in the Volcano", "CHECKERBOARD_PLATFORMS/DV/TJ/LJ")
    rf.assign_rule("Lethal Lava Land - Northeast Platform 1-Up", "LLL_KOOPA_SHELL | WC | LJ")
    rf.assign_rule("Lethal Lava Land - Southern Curve 1-Up", "LLL_KOOPA_SHELL | WC | LJ")
    rf.assign_rule("Lethal Lava Land - Raised Brown Platform 1-Up", "LLL_KOOPA_SHELL | WC | LJ")
    rf.assign_rule("Lethal Lava Land - Volcano Curve 1-Up", "LLL_KOOPA_SHELL | WC | LJ")
    rf.assign_rule("Lethal Lava Land - Northwest Curve 1-Up", "LLL_KOOPA_SHELL | WC | LJ")
    # Shifting Sand Land
    rf.assign_rule("Shifting Sand Land - In the Talons of the Big Bird", "SSL_KLEPTO")
    rf.assign_rule("Shifting Sand Land - Upper Pyramid", "CL & TJ/BF/SF/LG | SSL_PYRAMID_ELEVATOR")
    rf.assign_rule("Shifting Sand Land - Stand Tall on the Four Pillars",
                   "SSL_PYRAMID_ELEVATOR & TJ+WC+GP | SSL_PYRAMID_ELEVATOR & CANN+WC+GP | "
                   "SSL_PYRAMID_ELEVATOR & TJ/SF/BF & CAPLESS | MOVELESS & LG/KK")
    rf.assign_rule("Shifting Sand Land - Free Flying for 8 Red Coins", "TJ+WC | CANN+WC | TJ/SF/BF & CAPLESS | MOVELESS & CAPLESS")
    rf.assign_rule("Shifting Sand Land - Oasis Tree 1-Up", "CL/TJ/BF/SF")
    rf.assign_rule("Shifting Sand Land - Above Quicksand Pit 1-Up", "WC | LJ")
    rf.assign_rule("Shifting Sand Land - Pyramid Mummified Thwomp 1-Up", "TJ/LG/BF/SF")
    rf.assign_rule("Shifting Sand Land - Pyramid Right Path 1-Up", "TJ/LG/BF/SF")
    # Dire, Dire Docks
    rf.assign_rule("Dire, Dire Docks - Board Bowser's Sub", "PURPLE_SWITCHES/TJ & DDD_BOWSER_SUB")
    rf.assign_rule("Dire, Dire Docks - Pole-Jumping for Red Coins",
                   "PURPLE_SWITCHES & DDD_POLES & CL | "
                   # "PURPLE_SWITCHES & DDD_POLES & TJ+DV+LG+WK & MOVELESS |"  # I don't understand this and don't know if it is supposed to involve the sub
                   "TJ & DDD_BOWSER_SUB & DDD_POLES & CL")
    rf.assign_rule("Dire, Dire Docks - Through the Jet Stream", "MC | CAPLESS")
    rf.assign_rule("Dire, Dire Docks - The Manta Ray's Reward", "DDD_MANTA_RAY")
    rf.assign_rule("Dire, Dire Docks - Collect the Caps...", "VC")
    # Snowman's Land
    rf.assign_rule("Snowman's Land - Top of Snowman's Head", "SL_PENGUIN & BF/SF/TJ | CANN")
    rf.assign_rule("Snowman's Land - In the Deep Freeze", "WK/SF/LG/BF/CANN/TJ")
    rf.assign_rule("Snowman's Land - Into the Igloo", "VC & TJ/SF/BF/WK/LG | MOVELESS & VC")
    rf.assign_rule("Snowman's Land - Snowman Tree 1-Up", "CL/TJ/BF/SF")
    rf.assign_rule("Snowman's Land - Igloo Ice Block 1-Up", "VC & TJ/SF/BF/WK/LG | MOVELESS & VC")
    # Wet-Dry World
    rf.assign_rule("Wet-Dry World - Low Water to Mid Water", "WDW_WATER_LEVEL_DIAMOND")
    rf.assign_rule("Wet-Dry World - Mid Water to Low Water", "WDW_WATER_LEVEL_DIAMOND")
    rf.assign_rule("Wet-Dry World - Mid Water to Mid-High Water",
                   "WDW_WATER_LEVEL_DIAMOND & PURPLE_SWITCHES | WDW_WATER_LEVEL_DIAMOND & TJ+DV")
    rf.assign_rule("Wet-Dry World - Mid-High Water to Mid Water", "WDW_WATER_LEVEL_DIAMOND")
    rf.assign_rule("Wet-Dry World - Mid-High Water to High Water", "{Wet-Dry World - Top}")
    rf.assign_rule("Wet-Dry World - High Water to Mid-High Water", "WDW_WATER_LEVEL_DIAMOND")
    rf.assign_rule("Wet-Dry World - Highest Water to High Water", "WDW_WATER_LEVEL_DIAMOND")
    rf.assign_rule("Wet-Dry World - Top", "WK/TJ/SF/BF | MOVELESS | PURPLE_SWITCHES & LJ | {Wet-Dry World - Highest Water}")
    rf.assign_rule("Wet-Dry World - Downtown", "{Wet-Dry World - Highest Water} | CANN | {Wet-Dry World - Top} & MOVELESS & TJ+DV")
    rf.assign_rule("Wet-Dry World - Go to Town for Red Coins",
                   "WDW_WATER_LEVEL_DIAMOND & WK | WDW_WATER_LEVEL_DIAMOND & MOVELESS & TJ")
    rf.assign_rule("Wet-Dry World - Shocking Arrow Lifts!",
                   "{Wet-Dry World - Low Water} | {Wet-Dry World - Mid-High Water} | "
                   "{Wet-Dry World - High Water} | {Wet-Dry World - Top} & TJ/LG/LJ")
    rf.assign_rule("Wet-Dry World - Express Elevator--Hurry Up!", "PURPLE_SWITCHES | {Wet-Dry World - Top} & LG/TJ/LJ")
    rf.assign_rule("Wet-Dry World - Quick Race Through Downtown!",
                   "WDW_WATER_LEVEL_DIAMOND & VC & WK/BF | "
                   "WDW_WATER_LEVEL_DIAMOND & VC & TJ+LG+PURPLE_SWITCHES | "
                   "WDW_WATER_LEVEL_DIAMOND & MOVELESS & VC & TJ | "
                   "WDW_WATER_LEVEL_DIAMOND & MOVELESS & DJ/SF/BF & KK")
    rf.assign_rule("Wet-Dry World - 1Up Block in Downtown", "WDW_WATER_LEVEL_DIAMOND")
    rf.assign_rule("Wet-Dry World - Downtown Center Coin Ring 1-Up", "WDW_WATER_LEVEL_DIAMOND")
    rf.assign_rule("Wet-Dry World - Bob-omb Buddy",
                   "{Wet-Dry World - High Water} & TJ | {Wet-Dry World - High Water} & SF+LG | "
                   "{Wet-Dry World - Highest Water} & BF/SF")
    # Tall, Tall Mountain
    rf.assign_rule("Tall, Tall Mountain - Top", "MOVELESS & TJ | LJ/DV & LG/KK | MOVELESS & WK & SF/LG | MOVELESS & KK/DV")
    rf.assign_rule("Tall, Tall Mountain - Mystery of the Monkey Cage", "TTM_UKIKI")
    rf.assign_rule("Tall, Tall Mountain - Breathtaking View from Bridge", "TJ/DV/LG/PURPLE_SWITCHES")
    rf.assign_rule("Tall, Tall Mountain - Blast to the Lonely Mushroom", "CANN | CANNLESS & LJ | MOVELESS & CANNLESS")
    # Tiny-Huge Island
    rf.assign_rule("Tiny-Huge Island - Tiny Piranha Area", "TJ/LJ/LG")
    rf.assign_rule("Tiny-Huge Island - Tiny Main", "PURPLE_SWITCHES")
    rf.assign_rule("Tiny-Huge Island - Tiny Piranha Area to Huge Piranha Area", "THI_WARP_PIPES")
    rf.assign_rule("Tiny-Huge Island - Huge Island to Tiny Island", "THI_WARP_PIPES")
    rf.assign_rule("Tiny-Huge Island - Huge Piranha Area", "THI_WARP_PIPES & PURPLE_SWITCHES | TJ | LJ+SF | LJ+LG")
    rf.assign_rule("Tiny-Huge Island - Rematch with Koopa the Quick", "THI_KOOPA")
    rf.assign_rule("Tiny-Huge Island - Wiggler's Red Coins", "WK")
    rf.assign_rule("Tiny-Huge Island - Make Wiggler Squirm", "{Tiny-Huge Island - Tiny Main} & GP")
    rf.assign_rule("Tiny-Huge Island - Cannon Tree 1-Up", "CANN")
    rf.assign_rule("Tiny-Huge Island - Cannon Tree Butterfly 1-Up", "CANN")
    rf.assign_rule("Tiny-Huge Island - Red Coin Cave 1-Up", "WK")
    # Tick Tock Clock
    rf.assign_rule("Tick Tock Clock - Lower", "LG/TJ/SF/BF/WK | {Tick Tock Clock Stopped} & TTC_SPINNERS")
    rf.assign_rule("Tick Tock Clock - Upper", "CL | MOVELESS & WK")
    rf.assign_rule("Tick Tock Clock - Top", "TJ+LG | MOVELESS & WK/TJ")
    rf.assign_rule("Tick Tock Clock - Top Past Spinners", "TTC_SPINNERS | SF+LG | TJ")
    rf.assign_rule("Tick Tock Clock - 1Up Block Midway Up", "TTC_SPINNERS | LJ+LG")
    rf.assign_rule("Tick Tock Clock - Timed Jumps on Moving Bars", "{Tick Tock Clock Moving} | WK")
    rf.assign_rule("Tick Tock Clock - Stomp on the Thwomp", "{Tick Tock Clock Moving}")
    rf.assign_rule("Tick Tock Clock - Moving Bars Platform 1-Up", "{Tick Tock Clock Moving} | WK")
    # Rainbow Ride
    rf.assign_rule("Rainbow Ride - Beneath the Pole", "LJ/TJ/DV")
    rf.assign_rule("Rainbow Ride - Maze", "CL")
    rf.assign_rule("Rainbow Ride - Initial to Maze", "RR_CARPETS")
    rf.assign_rule("Rainbow Ride - Carpets", "RR_CARPETS")
    rf.assign_rule("Rainbow Ride - Coins Amassed in a Maze", "WK | LJ & SF/BF/TJ | MOVELESS & LG/TJ")
    rf.assign_rule("Rainbow Ride - Bob-omb Buddy", "WK | MOVELESS & LG")
    rf.assign_rule("Rainbow Ride - Swingin' in the Breeze", "LG/TJ/BF/SF | MOVELESS")
    rf.assign_rule("Rainbow Ride - Tricky Triangles!",
                   "PURPLE_SWITCHES & LG/TJ/BF/SF | PURPLE_SWITCHES & MOVELESS")
    rf.assign_rule("Rainbow Ride - Tricky Triangles 1-Up",
                   "PURPLE_SWITCHES & LG/TJ/BF/SF | PURPLE_SWITCHES & MOVELESS")
    rf.assign_rule("Rainbow Ride - Cruiser", "RR_CARPETS & WK/SF/BF/LG/TJ")
    rf.assign_rule("Rainbow Ride - Ship Pole 1-Up", "CL")
    rf.assign_rule("Rainbow Ride - House", "RR_CARPETS & TJ/SF/BF/LG")
    rf.assign_rule("Rainbow Ride - Somewhere Over the Rainbow", "CANN")
    # Tower of the Wing Cap
    # rf.assign_rule("Tower of the Wing Cap Red Coins", "WC") # ridiculous
    # Cavern of the Metal Cap
    rf.assign_rule("Cavern of the Metal Cap Red Coins", "MC | CAPLESS")
    rf.assign_rule("Cavern of the Metal Cap - Alcove 1-Up", "MC | CAPLESS")
    # Vanish Cap Under the Moat
    rf.assign_rule("Vanish Cap Under the Moat Switch",
                   "CHECKERBOARD_PLATFORMS & WK/TJ/BF/SF/LG | CHECKERBOARD_PLATFORMS & MOVELESS")
    rf.assign_rule("Vanish Cap Under the Moat Red Coins",
                   "CHECKERBOARD_PLATFORMS & TJ/BF/SF/LG/WK & VC | CHECKERBOARD_PLATFORMS & CAPLESS & WK")
    rf.assign_rule("Vanish Cap Under the Moat - Upper Platform 1-Up",
                   "CHECKERBOARD_PLATFORMS & WK/TJ/BF/SF/LG | CHECKERBOARD_PLATFORMS & MOVELESS")
    rf.assign_rule("Vanish Cap Under the Moat - Lower Platform 1-Up",
                   "CHECKERBOARD_PLATFORMS & WK/TJ/BF/SF/LG | CHECKERBOARD_PLATFORMS & MOVELESS")
    rf.assign_rule("Vanish Cap Under the Moat - Red Coin Platform 1-Up",
                   "CHECKERBOARD_PLATFORMS & TJ/BF/SF/LG/WK & VC | CHECKERBOARD_PLATFORMS & CAPLESS & WK")
    # Bowser in the Dark World
    rf.assign_rule("Bowser in the Dark World Red Coins", "PURPLE_SWITCHES")
    rf.assign_rule("Bowser in the Dark World Key", "PURPLE_SWITCHES")
    rf.assign_rule("Bowser in the Dark World - Center Overhang 1-Up", "PURPLE_SWITCHES")
    rf.assign_rule("Bowser in the Dark World - Right Tilting Platform Base 1-Up", "PURPLE_SWITCHES")
    rf.assign_rule("Bowser in the Dark World - Left Tilting Platform Base 1-Up", "PURPLE_SWITCHES")
    rf.assign_rule("Bowser in the Dark World - Far Overhang 1-Up", "PURPLE_SWITCHES")
    if options.freestanding_1ups:
        for location_name in (
                "Bowser in the Dark World - Center Overhang 1-Up",
                "Bowser in the Dark World - Left Tilting Platform Base 1-Up",
        ):
            add_rule(multiworld.get_location(location_name, player),
                     lambda state: has_bowser_stage_1up_unlock(
                         state, "Bowser in the Dark World - Extra 1-Ups", has_basement_key))
        add_rule(multiworld.get_location("Bowser in the Dark World - Far Overhang 1-Up", player),
                 lambda state: has_bowser_stage_1up_unlock(
                     state, "Bowser in the Dark World - Extra 1-Ups", has_second_floor_key))
    # Bowser in the Fire Sea
    rf.assign_rule("Bowser in the Fire Sea - Upper", "CL")
    rf.assign_rule("Bowser in the Fire Sea Red Coins", "LG/WK")
    rf.assign_rule("Bowser in the Fire Sea 1Up Block Near Poles", "LG/WK")
    rf.assign_rule("Bowser in the Fire Sea - Near Poles 1-Up", "LG/WK")
    if options.freestanding_1ups:
        for location_name in (
                "Bowser in the Fire Sea - Near Poles 1-Up",
                "Bowser in the Fire Sea - Second Stone Structure 1-Up",
        ):
            add_rule(multiworld.get_location(location_name, player),
                     lambda state: has_bowser_stage_1up_unlock(
                         state, "Bowser in the Fire Sea - Extra 1-Ups", has_second_floor_key))
    # Wing Mario Over the Rainbow
    rf.assign_rule("Wing Mario Over the Rainbow Red Coins", "WC+CANN")
    rf.assign_rule("Wing Mario Over the Rainbow 1Up Block", "WC+CANN")
    rf.assign_rule("Wing Mario Over the Rainbow - Bob-omb Buddy", "WC | LJ+CAPLESS")
    rf.assign_rule("Wing Mario Over the Rainbow - Bob-omb Buddy Platform 1-Up", "CL & WC | CL & LJ+CAPLESS")
    # Probably possible with cannon alone, but keep this gated until the route is modeled.
    rf.assign_rule("Wing Mario Over the Rainbow - Cloud 1-Up", "WC")
    rf.assign_rule("Wing Mario Over the Rainbow - Hanging Pole 1-Up", "WC+CANN")
    # Bowser in the Sky
    rf.assign_rule("Bowser in the Sky - Top",
                   "PURPLE_SWITCHES")
    rf.assign_rule("Bowser in the Sky - Middle",
                   "CL+TJ | CL+SF+LG | MOVELESS & TJ+WK+LG")
    # Coin Stars
    set_rule(
        multiworld.get_location("Bob-omb Battlefield - Coins Star", player),
        lambda state: bob_omb_battlefield_coins(
            state, player, options.bob_omb_battlefield_coin_star_requirement.value)
    )
    set_rule(
        multiworld.get_location("Whomp's Fortress - Coins Star", player),
        lambda state: whomps_fortress_coins(state, player, options.whomps_fortress_coin_star_requirement.value)
    )
    set_rule(
        multiworld.get_location("Jolly Roger Bay - Coins Star", player),
        lambda state: jolly_roger_bay_coins(state, player, options.jolly_roger_bay_coin_star_requirement.value)
    )
    set_rule(
        multiworld.get_location("Cool, Cool Mountain - Coins Star", player),
        lambda state: cool_cool_mountain_coins(
            state, player, options.cool_cool_mountain_coin_star_requirement.value)
    )
    set_rule(
        multiworld.get_location("Big Boo's Haunt - Coins Star", player),
        lambda state: big_boos_haunt_coins(state, player, options.big_boos_haunt_coin_star_requirement.value)
    )
    set_rule(
        multiworld.get_location("Hazy Maze Cave - Coins Star", player),
        lambda state: hazy_maze_cave_coins(state, player, options.hazy_maze_cave_coin_star_requirement.value)
    )
    set_rule(
        multiworld.get_location("Lethal Lava Land - Coins Star", player),
        lambda state: lethal_lava_land_coins(state, player, options.lethal_lava_land_coin_star_requirement.value)
    )
    set_rule(
        multiworld.get_location("Shifting Sand Land - Coins Star", player),
        lambda state: shifting_sand_land_coins(
            state, player, options.shifting_sand_land_coin_star_requirement.value)
    )
    set_rule(
        multiworld.get_location("Dire, Dire Docks - Coins Star", player),
        lambda state: dire_dire_docks_coins(state, player, options.dire_dire_docks_coin_star_requirement.value)
    )
    set_rule(
        multiworld.get_location("Snowman's Land - Coins Star", player),
        lambda state: snowmans_land_coins(state, player, options.snowmans_land_coin_star_requirement.value)
    )
    set_rule(
        multiworld.get_location("Wet-Dry World - Coins Star", player),
        lambda state: wet_dry_world_coins(state, player, options.wet_dry_world_coin_star_requirement.value)
    )
    set_rule(
        multiworld.get_location("Tall, Tall Mountain - Coins Star", player),
        lambda state: tall_tall_mountain_coins(
            state, player, options.tall_tall_mountain_coin_star_requirement.value)
    )
    set_rule(
        multiworld.get_location("Tiny-Huge Island - Coins Star", player),
        lambda state: tiny_huge_island_coins(state, player, options.tiny_huge_island_coin_star_requirement.value)
    )
    set_rule(
        multiworld.get_location("Tick Tock Clock - Coins Star", player),
        lambda state: tick_tock_clock_coins(
            state, player, options.tick_tock_clock_coin_star_requirement.value)
    )
    set_rule(
        multiworld.get_location("Rainbow Ride - Coins Star", player),
        lambda state: rainbow_ride_coins(state, player, options.rainbow_ride_coin_star_requirement.value)
    )
    coinsanity_coin_rules = {
        "Bob-omb Battlefield": bob_omb_battlefield_coins,
        "Whomp's Fortress": whomps_fortress_coins,
        "Jolly Roger Bay": jolly_roger_bay_coins,
        "Cool, Cool Mountain": cool_cool_mountain_coins,
        "Big Boo's Haunt": big_boos_haunt_coins,
        "Hazy Maze Cave": hazy_maze_cave_coins,
        "Lethal Lava Land": lethal_lava_land_coins,
        "Shifting Sand Land": shifting_sand_land_coins,
        "Dire, Dire Docks": dire_dire_docks_coins,
        "Snowman's Land": snowmans_land_coins,
        "Wet-Dry World": wet_dry_world_coins,
        "Tall, Tall Mountain": tall_tall_mountain_coins,
        "Tiny-Huge Island": tiny_huge_island_coins,
        "Tick Tock Clock": tick_tock_clock_coins,
        "Rainbow Ride": rainbow_ride_coins,
    }
    for location in multiworld.get_locations(player):
        coinsanity_location = parse_coinsanity_location_name(location.name)
        if coinsanity_location is None:
            continue
        course_name, coin_count = coinsanity_location
        coin_rule = coinsanity_coin_rules[course_name]
        set_rule(location, lambda state, rule=coin_rule, count=coin_count: rule(state, player, count))

    # Castle Stars
    rf.assign_rule("Castle - Roof", "CANN")
    add_rule(multiworld.get_location("Castle - Toad (Basement)", player),
             lambda state: state.can_reach("Basement", 'Region', player) and state.has("Castle Toads", player))
    add_rule(multiworld.get_location("Castle - Toad (Second Floor)", player),
             lambda state: state.can_reach("Second Floor", 'Region', player) and state.has("Castle Toads", player))
    add_rule(multiworld.get_location("Castle - Toad (Third Floor)", player),
             lambda state: state.can_reach("Third Floor", 'Region', player) and state.has("Castle Toads", player))
    add_rule(multiworld.get_location("Castle - Yoshi", player),
             lambda state: state.has("Yoshi", player))

    rf.assign_rule("Castle - Third Tree From Waterfall 1-Up", "CL/TJ/BF/SF")
    rf.assign_rule("Castle - Bridge Coins 1-Up", "{{Castle - Drain the Moat}} & WK & TJ/SF")
    rf.assign_rule("Castle - Jolly Roger Bay Lobby 1-Up", "SF/BF | TJ & LG | MOVELESS & TJ")
    rf.assign_rule("Castle - Drain the Moat", "GP")
    rf.assign_rule("Castle - MIPS 1", "DV | MOVELESS")
    rf.assign_rule("Castle - MIPS 2", "DV | MOVELESS")
    add_rule(multiworld.get_location("Castle - MIPS 1", player),
             lambda state: state.can_reach("Basement", 'Region', player) and state.has("Progressive MIPS", player))
    add_rule(multiworld.get_location("Castle - MIPS 2", player),
             lambda state: state.can_reach("Basement", 'Region', player) and
             state.has("Progressive MIPS", player, 2))

    if options.area_rando > options.area_rando.option_Off and not using_slot_area_connections:
        ensure_reachable_starting_check(
            multiworld, options, player, randomized_entrances, randomized_entrances_s,
            randomized_entrance_connections)

    # Destination Format: LVL | AREA with LVL = LEVEL_x, AREA = Area as used in sm64 code
    # Cast to int to not rely on availability of SM64Levels enum. Will cause crash in MultiServer otherwise
    area_connections.update({int(entrance_lvl): int(sm64_entrances_to_level[destination])
                             for (entrance_lvl, destination) in randomized_entrances.items()})

    multiworld.completion_condition[player] = lambda state: state.can_reach("Bowser in the Sky - Top", 'Region', player)

    if options.completion_type == options.completion_type.option_Last_Bowser_Stage:
        multiworld.completion_condition[player] = lambda state: state.can_reach("Bowser in the Sky - Top", 'Region', player)
    elif options.completion_type == options.completion_type.option_All_Bowser_Stages:
        multiworld.completion_condition[player] = lambda state: state.can_reach("Bowser in the Dark World", 'Region', player) and \
                                                           state.can_reach("Bowser in the Fire Sea - Upper", 'Region', player) and \
                                                           state.can_reach("Bowser in the Sky - Top", 'Region', player)


class RuleFactory:

    multiworld: MultiWorld
    player: int
    move_rando_bitvec: bool
    area_randomizer: bool
    capless: bool
    cannonless: bool
    moveless: bool

    global_cap_item_name_by_token = {
        "WC": "Wing Cap",
        "MC": "Metal Cap",
        "VC": "Vanish Cap",
    }
    token_table = {
        "TJ": "Triple Jump",
        "DJ": "Double Jump",
        "LJ": "Long Jump",
        "BF": "Backflip",
        "SF": "Side Flip",
        "WK": "Wall Kick",
        "DV": "Dive",
        "GP": "Ground Pound",
        "KK": "Kick",
        "CL": "Climb",
        "LG": "Ledge Grab",
        "BOB_KING": "Bob-omb Battlefield - King Bob-omb",
        "BOB_KOOPA": "Bob-omb Battlefield - Koopa the Quick",
        "BOB_BUDDY": "Bob-omb Battlefield - Bob-omb Buddy",
        "WF_KING": "Whomp's Fortress - Whomp King",
        "WF_FORTRESS": "Whomp's Fortress - Fortress",
        "WF_BUDDY": "Whomp's Fortress - Bob-omb Buddy",
        "WF_HOOT": "Whomp's Fortress - Hoot",
        "CCM_SNOWMAN_HEAD": "Cool, Cool Mountain - Snowman's Head",
        "CCM_BIG_PENGUIN": "Cool, Cool Mountain - Big Penguin",
        "JRB_SUNKEN_SHIP": "Jolly Roger Bay - Sunken Ship",
        "JRB_RAISED_SHIP": "Jolly Roger Bay - Raised Ship",
        "JRB_BUDDY": "Jolly Roger Bay - Bob-omb Buddy",
        "JRB_JET_STREAM": "Jolly Roger Bay - Jet Stream",
        "JRB_UNAGI": "Jolly Roger Bay - Unagi",
        "LLL_KOOPA_SHELL": "Lethal Lava Land - Koopa Shell",
        "SSL_KLEPTO": "Shifting Sand Land - Klepto Star",
        "THI_KOOPA": "Tiny-Huge Island - Koopa the Quick",
        "TTM_UKIKI": "Tall, Tall Mountain - Ukiki",
        "DDD_MANTA_RAY": "Dire, Dire Docks - Manta Ray",
        "DDD_BOWSER_SUB": "Dire, Dire Docks - Bowser's Sub",
        "DDD_POLES": "Dire, Dire Docks - Poles",
        "BBH_STAIRCASE": "Big Boo's Haunt - Staircase",
        "BBH_MERRY_GO_ROUND": "Big Boo's Haunt - Merry-go-round",
        "HMC_SWIMMING_BEAST": "Hazy Maze Cave - Swimming Beast",
        "RR_CARPETS": "Rainbow Ride - Carpets",
        "CHECKERBOARD_PLATFORMS": "Checkerboard Platforms",
        "THI_WARP_PIPES": "Tiny-Huge Island - Warp Pipes",
        "CCM_BABY_PENGUINS": "Cool, Cool Mountain - Baby Penguins",
        "SL_PENGUIN": "Snowman's Land - Penguin",
        "SSL_PYRAMID_ELEVATOR": "Shifting Sand Land - Pyramid Elevator",
        "LLL_ROLLING_LOG": "Rolling Logs",
        "PURPLE_SWITCHES": "Purple Switches",
        "WDW_WATER_LEVEL_DIAMOND": "Wet-Dry World - Water Level Diamond",
        "TTC_SPINNERS": "Tick Tock Clock - Spinners",
    }
    cap_item_name_by_token_and_level = {
        "WC": {
            "Bob-omb Battlefield": "Bob-omb Battlefield - Wing Cap",
            "Castle": "Castle - Wing Cap",
            "Lethal Lava Land": "Lethal Lava Land - Wing Cap",
            "Shifting Sand Land": "Shifting Sand Land - Wing Cap",
            "Tower of the Wing Cap": "Tower of the Wing Cap - Wing Cap",
            "Wing Mario Over the Rainbow": "Wing Mario Over the Rainbow - Wing Cap",
        },
        "MC": {
            "Whomp's Fortress": "Whomp's Fortress - Metal Cap",
            "Jolly Roger Bay": "Jolly Roger Bay - Metal Cap",
            "Hazy Maze Cave": "Hazy Maze Cave - Metal Cap",
            "Dire, Dire Docks": "Dire, Dire Docks - Metal Cap",
            "Wet-Dry World": "Wet-Dry World - Metal Cap",
            "Cavern of the Metal Cap": "Cavern of the Metal Cap - Metal Cap",
            "Bowser in the Dark World": "Bowser in the Dark World - Metal Cap",
        },
        "VC": {
            "Big Boo's Haunt": "Big Boo's Haunt - Vanish Cap",
            "Dire, Dire Docks": "Dire, Dire Docks - Vanish Cap",
            "Snowman's Land": "Snowman's Land - Vanish Cap",
            "Vanish Cap Under the Moat": "Vanish Cap Under the Moat - Vanish Cap",
            "Wet-Dry World": "Wet-Dry World - Vanish Cap",
        },
    }
    cannon_item_name_by_level = {
        "Wing Mario Over the Rainbow": "Cannon Unlock - Wing Mario Over the Rainbow",
    }

    class SM64LogicException(Exception):
        pass

    def __init__(self, multiworld, options: SM64Options, player: int, move_rando_bitvec: int):
        self.multiworld = multiworld
        self.options = options
        self.player = player
        self.move_rando_bitvec = move_rando_bitvec
        self.area_randomizer = options.area_rando > 0
        self.painting_randomizer = options.enable_locked_paintings
        self.capless = not options.strict_cap_requirements
        self.cannonless = not options.strict_cannon_requirements
        self.moveless = not options.strict_move_requirements
        self.per_level_caps = options.per_level_cap_items

    def assign_rule(self, target_name: str, rule_expr: str):
        if target_name in locFreestanding1Up_table and not self.options.freestanding_1ups:
            return
        target = self.multiworld.get_location(target_name, self.player) if target_name in location_table else self.multiworld.get_entrance(target_name, self.player)
        cannon_name = self.get_cannon_item_name(target_name)
        try:
            rule = self.build_rule(
                rule_expr, cannon_name, self.get_cap_item_names(target_name),
                self.get_arbitrary_item_names(target_name), self.get_action_item_names(target_name))
        except RuleFactory.SM64LogicException as exception:
            raise RuleFactory.SM64LogicException(
                f"Error generating rule for {target_name} using rule expression {rule_expr}: {exception}")
        if rule:
            set_rule(target, rule)
        if isinstance(target, Entrance):
            for region_name in re.findall(r"(?<!\{)\{([^{}]+)\}(?!\})", rule_expr):
                self.multiworld.register_indirect_condition(
                    self.multiworld.get_region(region_name, self.player), target)

    def build_rule(
            self, rule_expr: str, cannon_name: str = '', cap_item_names: dict[str, str] | None = None,
            arbitrary_item_names: dict[str, str | bool] | None = None,
            action_item_names: dict[str, str | bool] | None = None,
            painting_lvl_name: str = None, star_num_req: int = None) -> Callable:
        # Star/painting requirements are outer and'd requirements, logically (painting? star? and (rule_expr))
        base_rule = self.build_star_painting_entry_requirements(painting_lvl_name, star_num_req)
        if cap_item_names is None:
            cap_item_names = {}
        if arbitrary_item_names is None:
            arbitrary_item_names = self.get_arbitrary_item_names("")
        if action_item_names is None:
            action_item_names = self.get_action_item_names("Castle")
        expressions = rule_expr.split(" | ") if len(rule_expr) > 0 else []
        rules = []
        for expression in expressions:
            or_clause = self.combine_and_clauses(
                expression, cannon_name, cap_item_names, arbitrary_item_names, action_item_names)
            if or_clause is True:
                return base_rule
            if or_clause is not False:
                rules.append(or_clause)
        if rules:
            if len(rules) == 1:
                return lambda state: base_rule(state) and rules[0](state)
            else:
                return lambda state: base_rule(state) and any(rule(state) for rule in rules)
        else:
            return base_rule

    def build_star_painting_entry_requirements(self, painting_lvl_name: str = None, star_num_req: int = None) -> Callable:
        nop_condition = lambda state: True
        star_rule = nop_condition
        painting_rule = nop_condition
        if painting_lvl_name is not None and self.painting_randomizer:
            painting_item_name = f"Painting Unlock - {painting_lvl_name}"
            painting_rule = lambda state: state.has(painting_item_name, self.player)
        return lambda state: star_rule(state) and painting_rule(state)

    def get_level_name_from_target(self, target_name: str) -> str:
        if " - " in target_name:
            return target_name.split(" - ", 1)[0]
        for level_name in (
                "Tower of the Wing Cap",
                "Cavern of the Metal Cap",
                "Vanish Cap Under the Moat",
                "Wing Mario Over the Rainbow",
                "Bowser in the Dark World",
                "Bowser in the Fire Sea",
                "Bowser in the Sky",
                "The Princess's Secret Slide",
                "The Secret Aquarium",
        ):
            if target_name.startswith(level_name):
                return level_name
        return "Castle"

    def get_cannon_item_name(self, target_name: str) -> str:
        level_name = self.get_level_name_from_target(target_name)
        return self.cannon_item_name_by_level.get(level_name, "Cannon Unlock - " + target_name.split(" - ", 1)[0])

    def get_cap_item_names(self, target_name: str) -> dict[str, str]:
        level_name = self.get_level_name_from_target(target_name)
        return {
            token: item_name_by_level[level_name]
            for token, item_name_by_level in self.cap_item_name_by_token_and_level.items()
            if level_name in item_name_by_level
        }

    def get_arbitrary_item_names(self, target_name: str) -> dict[str, str | bool]:
        level_name = self.get_level_name_from_target(target_name)
        item_names = {
            token: True if not getattr(self.options, option_name).value else item_name
            for token, (item_name, option_name) in simple_arbitrary_feature_options.items()
        }
        item_names["CHECKERBOARD_PLATFORMS"] = self.get_feature_family_item_name(
            self.options.checkerboard_platforms.value,
            self.options.checkerboard_platforms.option_not_shuffled,
            self.options.checkerboard_platforms.option_global,
            "Checkerboard Platforms",
            checkerboard_item_name_by_level,
            level_name)
        item_names["LLL_ROLLING_LOG"] = self.get_feature_family_item_name(
            self.options.rolling_logs.value,
            self.options.rolling_logs.option_not_shuffled,
            self.options.rolling_logs.option_global,
            "Rolling Logs",
            rolling_log_item_name_by_level,
            level_name)
        item_names["PURPLE_SWITCHES"] = self.get_feature_family_item_name(
            self.options.purple_switches.value,
            self.options.purple_switches.option_not_shuffled,
            self.options.purple_switches.option_global,
            "Purple Switches",
            purple_switch_item_name_by_level,
            level_name)
        return item_names

    def get_action_item_names(self, target_name: str) -> dict[str, str | bool]:
        level_name = self.get_level_name_from_target(target_name)
        item_names = {}
        for action in action_item_data_table:
            option_name = move_randomizer_option_name_by_action.get(action)
            if option_name is None:
                item_names[action] = True
                continue
            option = getattr(self.options, option_name)
            if option.value == option.option_not_shuffled:
                item_names[action] = True
            elif option.value == option.option_global:
                item_names[action] = action
            else:
                item_names[action] = get_per_level_action_item_name(level_name, action) or True
        return item_names

    @staticmethod
    def get_feature_family_item_name(
            option_value: int, not_shuffled_value: int, global_value: int, global_item_name: str,
            item_name_by_level: dict[str, str], level_name: str) -> str | bool:
        if option_value == not_shuffled_value:
            return True
        if option_value == global_value:
            return global_item_name
        return item_name_by_level.get(level_name, True)

    def combine_and_clauses(
            self, rule_expr: str, cannon_name: str, cap_item_names: dict[str, str],
            arbitrary_item_names: dict[str, str | bool],
            action_item_names: dict[str, str | bool]) -> Union[Callable, bool]:
        expressions = rule_expr.split(" & ")
        rules = []
        for expression in expressions:
            and_clause = self.make_lambda(
                expression, cannon_name, cap_item_names, arbitrary_item_names, action_item_names)
            if and_clause is False:
                return False
            if and_clause is not True:
                rules.append(and_clause)
        if rules:
            if len(rules) == 1:
                return rules[0]
            return lambda state: all(rule(state) for rule in rules)
        else:
            return True

    def make_lambda(
            self, expression: str, cannon_name: str, cap_item_names: dict[str, str],
            arbitrary_item_names: dict[str, str | bool],
            action_item_names: dict[str, str | bool]) -> Union[Callable, bool]:
        if '+' in expression:
            tokens = expression.split('+')
            items = set()
            for token in tokens:
                item = self.parse_token(token, cannon_name, cap_item_names, arbitrary_item_names, action_item_names)
                if item is True:
                    continue
                if item is False:
                    return False
                items.add(item)
            if items:
                return lambda state: state.has_all(items, self.player)
            else:
                return True
        if '/' in expression:
            tokens = expression.split('/')
            items = set()
            for token in tokens:
                item = self.parse_token(token, cannon_name, cap_item_names, arbitrary_item_names, action_item_names)
                if item is True:
                    return True
                if item is False:
                    continue
                items.add(item)
            if items:
                return lambda state: state.has_any(items, self.player)
            else:
                return False
        if '{{' in expression:
            return lambda state: state.can_reach(expression[2:-2], "Location", self.player)
        if '{' in expression:
            return lambda state: state.can_reach(expression[1:-1], "Region", self.player)
        item = self.parse_token(expression, cannon_name, cap_item_names, arbitrary_item_names, action_item_names)
        if item in (True, False):
            return item
        return lambda state: state.has(item, self.player)

    def parse_token(
            self, token: str, cannon_name: str, cap_item_names: dict[str, str],
            arbitrary_item_names: dict[str, str | bool],
            action_item_names: dict[str, str | bool]) -> Union[str, bool]:
        if token == "CANN":
            return cannon_name
        if token in self.global_cap_item_name_by_token:
            if not self.per_level_caps:
                return self.global_cap_item_name_by_token[token]
            item = cap_item_names.get(token)
            if not item:
                raise RuleFactory.SM64LogicException(f"No per-level cap item for token '{token}' in this target.")
            return item
        if token == "CAPLESS":
            return True if self.capless else ut_glitch_item_name
        if token == "CANNLESS":
            return True if self.cannonless else ut_glitch_item_name
        if token == "MOVELESS":
            return True if self.moveless else ut_glitch_item_name
        if token in arbitrary_item_names:
            return arbitrary_item_names[token]
        item = self.token_table.get(token, None)
        if not item:
            raise Exception(f"Invalid token: '{item}'")
        if item in action_item_data_table:
            return action_item_names[item]
        elif item in cap_item_data_table:
            return item
        return item
