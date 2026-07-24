import re
from typing import Callable, Union, Dict, Set

from BaseClasses import CollectionState, Entrance, MultiWorld
from ..generic.Rules import add_rule, set_rule
from .Locations import locOneUp_table, location_table, parse_coinsanity_location_name
from .Options import SM64Options, move_randomizer_option_name_by_action
from .Regions import connect_regions, SM64Levels, sm64_entrance_to_region, sm64_level_to_paintings, \
    sm64_level_to_secrets, sm64_secrets_to_level, sm64_entrances_to_level, sm64_level_to_entrances, \
    sm64_ttc_entrances, sm64_wdw_entrances
from .Items import action_item_data_table, cap_item_data_table, per_level_move_area_names, ut_glitch_item_name
from .LogicTricks import logic_tricks


logic_tricks_by_name = {data["name"]: data for data in logic_tricks.values()}


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
    "Bob-omb Battlefield": "Bob-omb Battlefield - Checkerboard Platform",
    "Whomp's Fortress": "Whomp's Fortress - Checkerboard Platform",
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


def has_logic_trick(state: CollectionState, player: int, trick_name: str) -> bool:
    world = state.multiworld.worlds[player]
    return (
        getattr(world, trick_name, False)
        or getattr(world, f"{trick_name}_ut_glitch", False) and state.has(ut_glitch_item_name, player)
    )


def can_use_logic_trick(
        state: CollectionState, player: int, trick_name: str, target_name: str) -> bool:
    if not has_logic_trick(state, player, trick_name):
        return False
    world = state.multiworld.worlds[player]
    rule_factory = RuleFactory(state.multiworld, world.options, player, world.move_rando_bitvec)
    return rule_factory.build_rule(
        trick_name,
        rule_factory.get_cannon_item_name(target_name),
        rule_factory.get_cap_item_names(target_name),
        rule_factory.get_arbitrary_item_names(target_name),
        rule_factory.get_action_item_names(target_name),
    )(state)


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


def has_tiny_huge_island_rematch_movement(state: CollectionState, player: int) -> bool:
    level_name = "Tiny-Huge Island"
    return (
        has_action(state, player, "Long Jump", level_name)
        or has_action(state, player, "Dive", level_name)
        or allows_moveless(state, player) and (
            has_tiny_huge_island_top_return_movement(state, player)
            or has_simple_arbitrary_feature(state, player, "THI_WARP_PIPES")
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


def get_unlock_item_name(options, option_name: str, global_item_name: str, per_level_item_name: str) -> str | bool:
    option = getattr(options, option_name)
    if option.value == option.option_not_shuffled:
        return True
    if option.value == option.option_global:
        return global_item_name
    return per_level_item_name


def has_unlock(
        state: CollectionState, player: int, option_name: str,
        global_item_name: str, per_level_item_name: str) -> bool:
    item_name = get_unlock_item_name(
        state.multiworld.worlds[player].options, option_name, global_item_name, per_level_item_name)
    return item_name is True or state.has(item_name, player)


def bob_omb_battlefield_coins(state: CollectionState, player: int, coins: int) -> bool:
    level_name = "Bob-omb Battlefield"
    has_cannon = state.has(f"{level_name} - Cannon Unlock", player)
    has_single_yellow_coins = has_unlock(
        state, player, "coin_object_unlocks",
        "Single Yellow Coins", f"{level_name} - Single Yellow Coins")
    has_red_coins = has_unlock(
        state, player, "coin_object_unlocks",
        "Red Coins", f"{level_name} - Red Coins")
    has_horizontal_coin_lines = has_unlock(
        state, player, "coin_object_unlocks",
        "Horizontal Coin Lines", f"{level_name} - Horizontal Coin Lines")
    has_horizontal_coin_rings = has_unlock(
        state, player, "coin_object_unlocks",
        "Horizontal Coin Rings", f"{level_name} - Horizontal Coin Rings")
    has_vertical_coin_rings = has_unlock(
        state, player, "coin_object_unlocks",
        "Vertical Coin Rings", f"{level_name} - Vertical Coin Rings")
    has_breakable_coin_box = has_unlock(
        state, player, "coin_object_unlocks",
        "Breakable Coin Boxes", f"{level_name} - Breakable Coin Box")
    has_throwable_cork_boxes = has_unlock(
        state, player, "coin_object_unlocks",
        "Throwable Cork Boxes", f"{level_name} - Throwable Cork Boxes")
    has_wooden_posts = has_unlock(
        state, player, "coin_object_unlocks",
        "Wooden Posts", f"{level_name} - Wooden Posts")
    has_bob_ombs = has_unlock(
        state, player, "enemy_unlocks",
        "Bob-ombs", f"{level_name} - Bob-ombs")
    has_goombas = has_unlock(
        state, player, "enemy_unlocks",
        "Goombas", f"{level_name} - Goombas")
    has_koopa_troopa = has_unlock(
        state, player, "enemy_unlocks",
        "Koopa Troopas", f"{level_name} - Koopa Troopa")
    # https://ukikipedia.net/mediawiki/index.php?title=Bob-omb_Battlefield&oldid=19916

    # Inside the large breakable block near start
    reachable_coins = 3 if has_breakable_coin_box else 0
    # Inside the two throwable cork boxes
    if has_throwable_cork_boxes:
        reachable_coins += 6
    # Three horizontal coin lines
    if has_horizontal_coin_lines:
        reachable_coins += 15
    # 5 Posts (Run around them)
    if has_wooden_posts:
        reachable_coins += 25
    # Coins around flowerbed
    if has_horizontal_coin_rings:
        reachable_coins += 8
    # 12 Bob-ombs
    if has_bob_ombs:
        reachable_coins += 12
    # 11 Goombas
    if has_goombas:
        reachable_coins += 11
    # 7 red coins, excluding the Island one
    if has_red_coins:
        reachable_coins += 14
    # 1 Koopa
    if has_koopa_troopa:
        reachable_coins += 5

    if state.can_reach("Bob-omb Battlefield - Island", "Region", player):
        # 3 coins from the first coin ring are easily reachable.
        if has_vertical_coin_rings:
            reachable_coins += 3
        if can_use_logic_trick(
                state, player, "logic_bob_mario_wings_to_the_sky_without_cannon",
                "Bob-omb Battlefield - Coins Star"):
            # This route collects every coin on and above the island without using the cannon.
            if has_vertical_coin_rings:
                reachable_coins += 37
            if has_single_yellow_coins:
                reachable_coins += 5
            if has_red_coins:
                reachable_coins += 2
        elif has_cannon and state.can_reach(
                "Bob-omb Battlefield - Mario Wings to the Sky", "Location", player):
            if has_vertical_coin_rings:
                reachable_coins += 37
            if has_single_yellow_coins:
                reachable_coins += 5
            # Flying from the cannon can also reach the 8th red coin.
            if has_red_coins:
                reachable_coins += 2
        else:
            if has_wing_cap(state, player, level_name) and has_action(state, player, "Triple Jump", level_name):
                # 4 rings of 8 coins, plus the coin in the middle of each ring.
                if has_vertical_coin_rings:
                    reachable_coins += 32
                if has_single_yellow_coins:
                    reachable_coins += 4

            has_island_red_coin_movement = any(
                has_action(state, player, action, level_name)
                for action in ("Climb", "Side Flip", "Backflip", "Triple Jump")
            )
            has_island_red_coin_ground_pound = (
                can_use_logic_trick(
                    state, player, "logic_bob_island_red_coin_with_ground_pound",
                    "Bob-omb Battlefield - Coins Star")
            )
            if has_red_coins and (has_island_red_coin_movement
                    or has_island_red_coin_ground_pound
                    or can_use_logic_trick(
                        state, player, "logic_bob_island_koopa_shell",
                        "Bob-omb Battlefield - Coins Star")):
                reachable_coins += 2

            has_first_ring_jump = any(
                has_action(state, player, action, level_name)
                for action in ("Side Flip", "Backflip", "Triple Jump")
            )
            if has_vertical_coin_rings and (has_first_ring_jump or has_island_red_coin_ground_pound):
                reachable_coins += 3
            if has_vertical_coin_rings and has_first_ring_jump:
                reachable_coins += 2  # Ground Pound does not reach these two.
            if has_single_yellow_coins and has_action(state, player, "Triple Jump", level_name):
                reachable_coins += 1

    assert reachable_coins <= 146
    return coins <= reachable_coins


def whomps_fortress_coins(state: CollectionState, player: int, coins: int) -> bool:
    level_name = "Whomp's Fortress"
    has_single_yellow_coins = has_unlock(
        state, player, "coin_object_unlocks",
        "Single Yellow Coins", f"{level_name} - Single Yellow Coins")
    has_red_coins = has_unlock(
        state, player, "coin_object_unlocks",
        "Red Coins", f"{level_name} - Red Coins")
    has_blue_coin_switches = has_unlock(
        state, player, "coin_object_unlocks",
        "Blue Coin Blocks", f"{level_name} - Blue Coin Block")
    has_horizontal_coin_lines = has_unlock(
        state, player, "coin_object_unlocks",
        "Horizontal Coin Lines", f"{level_name} - Horizontal Coin Lines")
    has_horizontal_coin_rings = has_unlock(
        state, player, "coin_object_unlocks",
        "Horizontal Coin Rings", f"{level_name} - Horizontal Coin Rings")
    has_coin_arrows = has_unlock(
        state, player, "coin_object_unlocks",
        "Coin Arrows", f"{level_name} - Coin Arrows")
    has_throwable_cork_boxes = has_unlock(
        state, player, "coin_object_unlocks",
        "Throwable Cork Boxes", f"{level_name} - Throwable Cork Boxes")
    has_piranha_plants = has_unlock(
        state, player, "enemy_unlocks",
        f"{level_name} - Piranha Plants", f"{level_name} - Piranha Plants")
    has_whomps = has_unlock(
        state, player, "enemy_unlocks",
        "Whomps", f"{level_name} - Whomps")
    has_thwomp = has_unlock(
        state, player, "enemy_unlocks",
        "Thwomp", f"{level_name} - Thwomp")

    # https://ukikipedia.net/mediawiki/index.php?title=Whomp%27s_Fortress&oldid=19913

    # The two throwable cork boxes (near start/blue coin block)
    reachable_coins = 6 if has_throwable_cork_boxes else 0
    # Coins around the flower near the start
    if has_horizontal_coin_rings:
        reachable_coins += 8
    # Line of coins near the beginning
    if has_horizontal_coin_lines:
        reachable_coins += 5
    # Line of coins on bridge past the falling bridge
    if has_horizontal_coin_lines:
        reachable_coins += 5
    # Coins around the rotating plank
    if has_single_yellow_coins:
        reachable_coins += 4
    # Line of coins on slope leading from the water
    if has_horizontal_coin_lines:
        reachable_coins += 5
    # Ring of coins in water
    if has_horizontal_coin_rings:
        reachable_coins += 8
    # Line of coins near the bob-omb buddy
    if has_horizontal_coin_lines:
        reachable_coins += 5
    # 2 Whomps (jump on back)
    if has_whomps:
        reachable_coins += 10
    # 3 Piranha Plants
    if has_piranha_plants:
        reachable_coins += 15
    # 5 initially reachable Red Coins
    if has_red_coins:
        reachable_coins += 10
    # Red Coin on a Thwomp
    if has_red_coins and has_thwomp:
        reachable_coins += 2

    can_reach_wild_blue_coins = (
        state.has("Whomp's Fortress - Cannon Unlock", player)
        or can_use_logic_trick(
            state, player, "logic_wf_into_the_wild_blue_yonder_wall_kick",
            "Whomp's Fortress - Coins Star")
        or can_use_logic_trick(
            state, player, "logic_wf_into_the_wild_blue_yonder_long_jump",
            "Whomp's Fortress - Coins Star")
        or (
            can_use_logic_trick(
                state, player, "logic_wf_into_the_wild_blue_yonder_moveless",
                "Whomp's Fortress - Coins Star")
            and (
                has_action(state, player, "Climb", level_name)
                or has_action(state, player, "Side Flip", level_name)
                or (
                    has_action(state, player, "Triple Jump", level_name)
                    and has_action(state, player, "Ledge Grab", level_name)
                )
            )
        )
    )
    if can_reach_wild_blue_coins and has_horizontal_coin_rings:
        # Ring of coins above the "Shoot into the Blue" Star
        reachable_coins += 8
    if has_action(state, player, "Ground Pound", level_name):
        # 2 Whomps (ground pound)
        if has_whomps:
            reachable_coins += 10
        # Blue Coin Block
        if has_blue_coin_switches:
            reachable_coins += 20
    if state.can_reach("Whomp's Fortress - Top", "Region", player):
        # Ring of coins on the floating isle
        if has_horizontal_coin_rings:
            reachable_coins += 8
        # Arrow of coins on the floating arrow
        if has_coin_arrows:
            reachable_coins += 8
        # 2 Red Coins
        if has_red_coins:
            reachable_coins += 4
    assert reachable_coins <= 141
    return coins <= reachable_coins


def cool_cool_mountain_coins(state: CollectionState, player: int, coins: int) -> bool:
    level_name = "Cool, Cool Mountain"
    has_single_yellow_coins = has_unlock(
        state, player, "coin_object_unlocks",
        "Single Yellow Coins", f"{level_name} - Single Yellow Coins")
    has_red_coins = has_unlock(
        state, player, "coin_object_unlocks",
        "Red Coins", f"{level_name} - Red Coins")
    has_single_blue_coin = has_unlock(
        state, player, "coin_object_unlocks",
        "Single Blue Coins", f"{level_name} - Single Blue Coin")
    has_blue_coin_switches = has_unlock(
        state, player, "coin_object_unlocks",
        "Blue Coin Blocks", f"{level_name} - Blue Coin Block")
    has_horizontal_coin_lines = has_unlock(
        state, player, "coin_object_unlocks",
        "Horizontal Coin Lines", f"{level_name} - Horizontal Coin Lines")
    has_coin_arrows = has_unlock(
        state, player, "coin_object_unlocks",
        "Coin Arrows", f"{level_name} - Coin Arrows")
    has_vertical_coin_lines = has_unlock(
        state, player, "coin_object_unlocks",
        "Vertical Coin Lines", f"{level_name} - Vertical Coin Lines")
    has_mr_blizzards = has_unlock(
        state, player, "enemy_unlocks",
        "Mr Blizzards", f"{level_name} - Mr Blizzards")
    has_spindrifts = has_unlock(
        state, player, "enemy_unlocks",
        "Spindrifts", f"{level_name} - Spindrifts")

    # https://ukikipedia.net/mediawiki/index.php?title=Cool,_Cool_Mountain&oldid=19915

    # 27 individual coins and 9 lines of coins on the Penguin Slide
    reachable_coins = 27 if has_single_yellow_coins else 0
    if has_horizontal_coin_lines:
        reachable_coins += 45
    # Vertical line of coins into chimney
    if has_vertical_coin_lines:
        reachable_coins += 5
    if has_horizontal_coin_lines:
        # Four lines along the main mountain route
        reachable_coins += 20
    if has_mr_blizzards:
        # Only the standard Mr. Blizzard is normally defeatable. The two
        # jumping Mr. Blizzards on the bridge require Metal Cap.
        reachable_coins += 3
    if has_spindrifts:
        # 3 Spindrifts
        reachable_coins += 9
    if has_red_coins:
        # 8 Red Coins
        reachable_coins += 16
    # Blue Coin at the start of the slide
    if has_single_blue_coin:
        reachable_coins += 5

    has_cannon = state.has("Cool, Cool Mountain - Cannon Unlock", player)
    has_spin_jump_route = can_use_logic_trick(
        state, player, "logic_ccm_wall_kicks_will_work_spin_jump",
        "Cool, Cool Mountain - Coins Star")
    if has_cannon or has_spin_jump_route:
        # Arrow of coins near "Wall Kicks will Work"
        if has_coin_arrows:
            reachable_coins += 8
        if has_spindrifts:
            # 2 Spindrifts
            reachable_coins += 6
        if has_spindrifts and not has_cannon:
            # If you use a spindrift to get down, you must leave its 3 coins behind.
            reachable_coins -= 3
    if has_blue_coin_switches and has_action(state, player, "Ground Pound", level_name):
        # Blue Coin Block
        reachable_coins += 10
    assert reachable_coins <= 154
    return coins <= reachable_coins


def big_boos_haunt_coins(state: CollectionState, player: int, coins: int) -> bool:
    level_name = "Big Boo's Haunt"
    has_red_coins = has_unlock(
        state, player, "coin_object_unlocks",
        "Red Coins", f"{level_name} - Red Coins")
    has_blue_coin_switches = has_unlock(
        state, player, "coin_object_unlocks",
        "Blue Coin Blocks", f"{level_name} - Blue Coin Block")
    has_breakable_coin_boxes = has_unlock(
        state, player, "coin_object_unlocks",
        "Breakable Coin Boxes", f"{level_name} - Breakable Coin Boxes")
    has_crazy_box = has_unlock(
        state, player, "coin_object_unlocks",
        "Crazy Boxes", f"{level_name} - Crazy Box")
    has_ten_coin_block = has_unlock(
        state, player, "coin_object_unlocks",
        "Ten-Coin Blocks", f"{level_name} - Ten-Coin Block")
    has_boos = has_unlock(
        state, player, "enemy_unlocks",
        "Boos", f"{level_name} - Boos")
    has_flying_bookends = has_unlock(
        state, player, "enemy_unlocks",
        f"{level_name} - Flying Bookends", f"{level_name} - Flying Bookends")
    has_mr_is = has_unlock(
        state, player, "enemy_unlocks",
        "Mr. Is", f"{level_name} - Mr. Is")
    has_scuttlebugs = has_unlock(
        state, player, "enemy_unlocks",
        "Scuttlebugs", f"{level_name} - Scuttlebugs")
    has_normal_third_floor_route = (
        has_action(state, player, "Wall Kick", level_name)
        and has_action(state, player, "Ledge Grab", level_name)
    )
    has_wall_kick_third_floor_trick = can_use_logic_trick(
        state, player, "logic_bbh_third_floor_wall_kick",
        "Big Boo's Haunt - Coins Star")
    has_bookend_third_floor_trick = can_use_logic_trick(
        state, player, "logic_bbh_third_floor_side_flip",
        "Big Boo's Haunt - Coins Star")

    # https://ukikipedia.net/mediawiki/index.php?title=Big_Boo%27s_Haunt&oldid=20246

    # Yellow [!] behind mansion
    reachable_coins = 10 if has_ten_coin_block else 0
    # Two cork boxes near shed
    if has_breakable_coin_boxes:
        reachable_coins += 6
    # Crazy Box outside
    if has_crazy_box:
        reachable_coins += 5
    # 3 Scuttlebugs (outside)
    if has_scuttlebugs:
        reachable_coins += 9
    # 5 Boos
    if has_boos:
        reachable_coins += 25
    # 2 Mr. Is
    if has_mr_is:
        reachable_coins += 10
    # 1 Bookend
    if has_flying_bookends:
        reachable_coins += 5
    # 4 Red Coins
    if has_red_coins:
        reachable_coins += 8

    if state.can_reach("Big Boo's Haunt - Second Floor", "Region", player):
        # 2 Bookends
        if has_flying_bookends:
            reachable_coins += 10
        # 1 Mr. I
        if has_mr_is:
            reachable_coins += 5
        # 4 Red Coins
        if has_red_coins:
            reachable_coins += 8
    if state.can_reach("Big Boo's Haunt - Third Floor", "Region", player):
        third_floor_coins = 0
        # 1 Boo, spawns behind vanish cap barrier but can follow Mario out
        if has_boos:
            third_floor_coins += 5
        if has_blue_coin_switches and has_action(state, player, "Ground Pound", level_name):
            # Blue coin block (attic)
            third_floor_coins += 20
        if (
                has_flying_bookends
                and has_bookend_third_floor_trick
                and not has_normal_third_floor_route
                and not has_wall_kick_third_floor_trick
                and not state.multiworld.worlds[player].options.no_despawns.value):
            # Taking this route leaves the two Bookends' 10 coins below to
            # despawn.
            third_floor_coins = max(0, third_floor_coins - 10)
        reachable_coins += third_floor_coins
    if has_boos and state.has("Big Boo's Haunt - Merry-go-round", player):
        # 5 Boos
        reachable_coins += 25
    assert reachable_coins <= 151
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

    # https://ukikipedia.net/mediawiki/index.php?title=Hazy_Maze_Cave&oldid=19918

    # Line of coins right of start
    reachable_coins = 5
    # Line of coins before the maze
    reachable_coins += 5
    # Line of coins next to rolling rocks
    reachable_coins += 5
    # Ring of coins around exclamation block, before lake
    reachable_coins += 8
    # 2 Scuttlebugs in first room
    reachable_coins += 6
    # Scuttlebug in pit room
    reachable_coins += 3
    # Swooper in pit room
    reachable_coins += 1
    # 2 Scuttlebugs in Red Coin room
    reachable_coins += 6
    # 4 Snufits in Hazy Maze
    reachable_coins += 8
    # 4 Swoopers in Hazy Maze
    reachable_coins += 4

    if has_basic_movement:
        ## Red Coin room
        # 4 Red Coins
        reachable_coins += 8
        #2 Mr Is
        reachable_coins += 10
        ## Pit Island elevator room
        # 2 Swoopers
        reachable_coins += 2
    if has_platform_route and (has_long_jump or has_checkerboards):
        # 2 Red Coins
        reachable_coins += 4
    if has_platform_route and has_checkerboards:
        # 2 Red Coins
        reachable_coins += 4
        # 2 Swoopers
        reachable_coins += 2
    if (state.can_reach("Hazy Maze Cave - Pit Islands", "Region", player)
            and has_action(state, player, "Climb", level_name)):
            # Line of coins on the hangable ceiling
            reachable_coins += 5
    if has_simple_arbitrary_feature(state, player, "HMC_SWIMMING_BEAST"):
        # Ring of coins around the "Swimming Beast in the Cavern" star
        reachable_coins += 8
    if state.can_reach("Hazy Maze Cave - Navigating the Toxic Maze", "Location", player):
        # Line of coins to "Navigating the Toxic Maze" Star
        reachable_coins += 5
        # 2 Swoopers
        reachable_coins += 2
    if has_purple_switches(state, player, level_name) and (
            has_metal_cap(state, player, "Hazy Maze Cave")
            or allows_capless(state, player) and has_action(state, player, "Triple Jump", level_name)):
        reachable_coins += 3
    if has_action(state, player, "Ground Pound", level_name):
        # Blue coin block (in maze)
        reachable_coins += 35
    assert reachable_coins <= 139
    return coins <= reachable_coins


def has_lethal_lava_land_healing_coins(state: CollectionState, player: int) -> bool:
    level_name = "Lethal Lava Land"
    return any((
        has_unlock(
            state, player, "coin_object_unlocks",
            "Single Yellow Coins", f"{level_name} - Single Yellow Coins"),
        has_unlock(
            state, player, "coin_object_unlocks",
            "Horizontal Coin Lines", f"{level_name} - Horizontal Coin Lines"),
        has_unlock(
            state, player, "coin_object_unlocks",
            "Horizontal Coin Rings", f"{level_name} - Horizontal Coin Rings"),
        has_unlock(
            state, player, "enemy_unlocks",
            "Bullies", f"{level_name} - Bullies"),
        has_unlock(
            state, player, "enemy_unlocks",
            "Mr. Is", f"{level_name} - Mr. Is"),
    ))


def can_collect_all_lethal_lava_land_red_coins(
        state: CollectionState, player: int, target_name: str) -> bool:
    if has_unlock(
            state, player, "coin_object_unlocks",
            "Lethal Lava Land - Bowser Puzzle", "Lethal Lava Land - Bowser Puzzle"):
        return True
    has_lava_crossing = (
        state.has("Lethal Lava Land - Koopa Shell", player)
        or can_use_logic_trick(state, player, "logic_jump_in_lava", target_name)
    )
    return has_lava_crossing and has_lethal_lava_land_healing_coins(state, player)


def can_reach_lethal_lava_land_red_coins(
        state: CollectionState, player: int, target_name: str) -> bool:
    return (
        has_unlock(
            state, player, "coin_object_unlocks",
            "Lethal Lava Land - Bowser Puzzle", "Lethal Lava Land - Bowser Puzzle")
        or state.has("Lethal Lava Land - Koopa Shell", player)
        or can_use_logic_trick(state, player, "logic_jump_in_lava", target_name)
    )


def lethal_lava_land_coins(state: CollectionState, player: int, coins: int) -> bool:
    level_name = "Lethal Lava Land"
    has_single_yellow_coins = has_unlock(
        state, player, "coin_object_unlocks",
        "Single Yellow Coins", f"{level_name} - Single Yellow Coins")
    has_red_coins = has_unlock(
        state, player, "coin_object_unlocks",
        "Red Coins", f"{level_name} - Red Coins")
    has_horizontal_coin_lines = has_unlock(
        state, player, "coin_object_unlocks",
        "Horizontal Coin Lines", f"{level_name} - Horizontal Coin Lines")
    has_horizontal_coin_rings = has_unlock(
        state, player, "coin_object_unlocks",
        "Horizontal Coin Rings", f"{level_name} - Horizontal Coin Rings")
    has_crazy_box = has_unlock(
        state, player, "coin_object_unlocks",
        "Crazy Boxes", f"{level_name} - Crazy Box")
    has_bowser_puzzle = has_unlock(
        state, player, "coin_object_unlocks",
        f"{level_name} - Bowser Puzzle", f"{level_name} - Bowser Puzzle")
    has_bullies = has_unlock(
        state, player, "enemy_unlocks",
        "Bullies", f"{level_name} - Bullies")
    has_mr_is = has_unlock(
        state, player, "enemy_unlocks",
        "Mr. Is", f"{level_name} - Mr. Is")

    # https://ukikipedia.net/mediawiki/index.php?title=Lethal_Lava_Land&oldid=19919

    # Line of coins on tilting platform past first Mr. I
    reachable_coins = 5 if has_horizontal_coin_lines else 0
    # Three coins on grey ramp near tilting platform
    if has_single_yellow_coins:
        reachable_coins += 3
    # Five coins for completing Bowser puzzle
    if has_bowser_puzzle:
        reachable_coins += 5
    # Line of coins on sinking platform right before first Big Bully
    if has_horizontal_coin_lines:
        reachable_coins += 5
    # Ring of coins on second Big Bully platform
    if has_horizontal_coin_rings:
        reachable_coins += 8
    # Five coins on high brown ramp in north-west corner
    if has_horizontal_coin_lines:
        reachable_coins += 5
    # Four coins on sinking platforms, between crazy box & second Big Bully
    if has_single_yellow_coins:
        reachable_coins += 4
    # Line of coins on sinking platform, north of volcano
    if has_horizontal_coin_lines:
        reachable_coins += 5
    # "Four Ring of coins on platform with 2 bullies" (it's just one ring?)
    if has_horizontal_coin_rings:
        reachable_coins += 8
    # Three coins on spinning platform around volcano
    if has_single_yellow_coins:
        reachable_coins += 3
    # Four coins on small grey ramp, south-east from volcano (with 1UP)
    if has_single_yellow_coins:
        reachable_coins += 4
    # Ring of coins with second Mr. I
    if has_horizontal_coin_rings:
        reachable_coins += 8
    # Crazy Box
    if has_crazy_box:
        reachable_coins += 5
    # 8 Red Coins
    if (has_red_coins
            and can_reach_lethal_lava_land_red_coins(
                state, player, "Lethal Lava Land - Coins Star")):
        # Five do not require additional healing once the lava area is reachable.
        reachable_coins += 10
        if can_collect_all_lethal_lava_land_red_coins(
                state, player, "Lethal Lava Land - Coins Star"):
            reachable_coins += 6
    # 8 Bullies outside
    if has_bullies:
        reachable_coins += 8
    # 2 Mr Is
    if has_mr_is:
        reachable_coins += 10

    if (has_single_yellow_coins
            and (state.has("Lethal Lava Land - Koopa Shell", player)
                 or can_use_logic_trick(
                    state, player, "logic_jump_in_lava", "Lethal Lava Land - Coins Star"))):
        # Line of coins under bridge
        reachable_coins += 5

    # (Inside the Volcano) Three coins on S-shaped island at bottom of volcano, by lavafall
    if has_single_yellow_coins:
        reachable_coins += 3
    # (Inside the Volcano) Five coins on first ridge going up
    if has_horizontal_coin_lines:
        reachable_coins += 5
    # (Inside the Volcano) Two coins on second ridge going up (with first bully)
    if has_single_yellow_coins:
        reachable_coins += 2
    # (Inside the Volcano) Four coins on floating platforms (with the spinning heart)
    if has_single_yellow_coins:
        reachable_coins += 4
    # (Inside the Volcano) Singular coin after the floating platforms (from above line)
    if has_single_yellow_coins:
        reachable_coins += 1
    # (Inside the Volcano) Line of coins, with the second bully, on platform beside waterfall
    if has_horizontal_coin_lines:
        reachable_coins += 5
    # (Inside the Volcano) Singular coin by checker-board lift, left from beginning
    if has_single_yellow_coins:
        reachable_coins += 1
    # Bullies inside
    if has_bullies:
        reachable_coins += 2
    if (has_single_yellow_coins
            and state.can_reach("Lethal Lava Land - Elevator Tour in the Volcano", "Location", player)):
        # (Inside the Volcano) Three coins on tiny floating platforms, by "Elevator Tour in the Volcano"
        reachable_coins += 3
    assert reachable_coins <= 133
    return coins <= reachable_coins


def shifting_sand_land_coins(state: CollectionState, player: int, coins: int) -> bool:
    level_name = "Shifting Sand Land"
    has_single_yellow_coins = has_unlock(
        state, player, "coin_object_unlocks",
        "Single Yellow Coins", f"{level_name} - Single Yellow Coins")
    has_red_coins = has_unlock(
        state, player, "coin_object_unlocks",
        "Red Coins", f"{level_name} - Red Coins")
    has_blue_coin_block = has_unlock(
        state, player, "coin_object_unlocks",
        "Blue Coin Blocks", f"{level_name} - Blue Coin Block")
    has_horizontal_coin_lines = has_unlock(
        state, player, "coin_object_unlocks",
        "Horizontal Coin Lines", f"{level_name} - Horizontal Coin Lines")
    has_horizontal_coin_ring = has_unlock(
        state, player, "coin_object_unlocks",
        "Horizontal Coin Rings", f"{level_name} - Horizontal Coin Rings")
    has_vertical_coin_line = has_unlock(
        state, player, "coin_object_unlocks",
        "Vertical Coin Lines", f"{level_name} - Vertical Coin Lines")
    has_throwable_cork_box = has_unlock(
        state, player, "coin_object_unlocks",
        "Throwable Cork Boxes", f"{level_name} - Throwable Cork Box")
    has_crazy_boxes = has_unlock(
        state, player, "coin_object_unlocks",
        "Crazy Boxes", f"{level_name} - Crazy Boxes")
    has_bob_ombs = has_unlock(
        state, player, "enemy_unlocks",
        "Bob-ombs", f"{level_name} - Bob-ombs")
    has_fly_guys = has_unlock(
        state, player, "enemy_unlocks",
        "Fly Guys", f"{level_name} - Fly Guy")
    has_goombas = has_unlock(
        state, player, "enemy_unlocks",
        "Goombas", f"{level_name} - Goombas")
    has_pokeys = has_unlock(
        state, player, "enemy_unlocks",
        "Pokeys", f"{level_name} - Pokeys")

    reachable_coins = 0
    if has_throwable_cork_box:
        # Inside the throwing box under the stone building
        reachable_coins += 3
    if has_single_yellow_coins:
        # One coin on top of each pillar and two inside the pyramid
        reachable_coins += 6
    if has_horizontal_coin_lines:
        # Line between the two pillars behind the pyramid
        reachable_coins += 5
    if has_vertical_coin_line:
        # Line up the side of the pyramid
        reachable_coins += 5
    if has_fly_guys:
        # One normal Fly Guy and two fire Fly Guys
        reachable_coins += 6
    if has_crazy_boxes:
        reachable_coins += 10
    if has_bob_ombs:
        reachable_coins += 2
    if has_pokeys:
        reachable_coins += 20
    if has_goombas:
        # Eight inside the pyramid and four outside
        reachable_coins += 12
    if has_red_coins:
        # Four low Red Coins
        reachable_coins += 8

    if has_horizontal_coin_ring and has_action(state, player, "Climb", level_name):
        # (In the Pyramid) Ring of coins under the first wire grid
        reachable_coins += 8

    has_normal_red_coin_route = (
        has_wing_cap(state, player, level_name)
        and (
            has_action(state, player, "Triple Jump", level_name)
            or state.has("Shifting Sand Land - Cannon Unlock", player)
        )
    )
    if has_red_coins and has_normal_red_coin_route:
        # 4 Red Coins
        reachable_coins += 8
    elif has_red_coins:
        if can_use_logic_trick(
                state, player, "logic_ssl_three_red_coins_with_tweesters",
                "Shifting Sand Land - Coins Star"):
            # 3 Red Coins
            reachable_coins += 6
        if (can_use_logic_trick(
                state, player, "logic_ssl_one_red_coin_with_shy_guy_spin_jump",
                "Shifting Sand Land - Coins Star")
                and state.multiworld.worlds[player].options.no_despawns.value):
            # 1 Red Coin
            reachable_coins += 2

    if state.can_reach("Shifting Sand Land - Upper Pyramid", "Region", player):
        if has_horizontal_coin_lines:
            # One line under the second wire grid and two at the top
            reachable_coins += 15
        if has_single_yellow_coins:
            # Coins on moving steps and the Pyramid Puzzle secrets
            reachable_coins += 13

    if has_blue_coin_block and has_action(state, player, "Ground Pound", level_name):
        # (In the Pyramid) Blue coin block
        reachable_coins += 15

    assert reachable_coins <= 136
    return coins <= reachable_coins


def jolly_roger_bay_coins(state: CollectionState, player: int, coins: int) -> bool:
    level_name = "Jolly Roger Bay"
    has_red_coins = has_unlock(
        state, player, "coin_object_unlocks",
        "Red Coins", f"{level_name} - Red Coins")
    has_blue_coin_switches = has_unlock(
        state, player, "coin_object_unlocks",
        "Blue Coin Blocks", f"{level_name} - Blue Coin Block")
    has_horizontal_coin_lines = has_unlock(
        state, player, "coin_object_unlocks",
        "Horizontal Coin Lines", f"{level_name} - Horizontal Coin Lines")
    has_horizontal_coin_rings = has_unlock(
        state, player, "coin_object_unlocks",
        "Horizontal Coin Rings", f"{level_name} - Horizontal Coin Rings")
    has_vertical_coin_lines = has_unlock(
        state, player, "coin_object_unlocks",
        "Vertical Coin Lines", f"{level_name} - Vertical Coin Lines")
    has_vertical_coin_rings = has_unlock(
        state, player, "coin_object_unlocks",
        "Vertical Coin Rings", f"{level_name} - Vertical Coin Rings")
    has_three_coin_block = has_unlock(
        state, player, "coin_object_unlocks",
        "Three-Coin Blocks", f"{level_name} - Three-Coin Block")
    has_goombas = has_unlock(
        state, player, "enemy_unlocks",
        "Goombas", f"{level_name} - Goombas")
    has_pillar_red_coin_moves = (
        can_use_logic_trick(
            state, player, "logic_jrb_pillar_red_coin_moves",
            "Jolly Roger Bay - Coins Star")
    )
    has_pillar_red_coin_cannon = (
        can_use_logic_trick(
            state, player, "logic_jrb_pillar_red_coin_cannon",
            "Jolly Roger Bay - Coins Star")
    )
    has_upper = state.can_reach("Jolly Roger Bay - Upper", "Region", player)
    has_raised_ship = state.has("Jolly Roger Bay - Raised Ship", player)

    # https://ukikipedia.net/mediawiki/index.php?title=Jolly_Roger_Bay&oldid=20489

    # The yellow [!] block near start
    reachable_coins = 3 if has_three_coin_block else 0
    # Ring of underwater coins near clams
    if has_vertical_coin_rings:
        reachable_coins += 8
    # Ring of coins around the tall spike
    if has_horizontal_coin_rings:
        reachable_coins += 8
    # Vertical line of coins before the purple switch (3 of them)
    if has_vertical_coin_lines:
        reachable_coins += 3
    # Ring of coins near jet stream
    if has_horizontal_coin_rings:
        reachable_coins += 8
    # Ring of coins near cave treasure chests
    if has_horizontal_coin_rings:
        reachable_coins += 8
    # 3 Goombas
    if has_goombas:
        reachable_coins += 3
    # 4 Red Coins
    if has_red_coins:
        reachable_coins += 8


    if has_red_coins and (
            has_action(state, player, "Climb", level_name)
            or has_pillar_red_coin_moves
            or has_pillar_red_coin_cannon):
        # Pillar Red Coin
        reachable_coins += 2
    if has_upper:
        # Vertical line of coins before the purple switch (2 of them)
        if has_vertical_coin_lines:
            reachable_coins += 2
        # The lines of coins before the ship
        if has_horizontal_coin_lines:
            reachable_coins += 15
        if has_red_coins and has_raised_ship:
            # 3 Red Coins
            reachable_coins += 6
        elif has_red_coins and (
                can_use_logic_trick(state, player, "logic_jrb_ship_red_coin_with_long_jump",
                                    "Jolly Roger Bay - Coins Star")
                or has_purple_switches(state, player, level_name)):
            # 1 Red Coin
            reachable_coins += 2
    if has_blue_coin_switches and has_action(state, player, "Ground Pound", level_name):
        # Blue coin block
        reachable_coins += 30
    assert reachable_coins <= 104
    return coins <= reachable_coins


def dire_dire_docks_coins(state: CollectionState, player: int, coins: int) -> bool:
    level_name = "Dire, Dire Docks"
    reachable_coins = 60
    has_poles = state.has("Dire, Dire Docks - Poles", player) and has_action(state, player, "Climb", level_name)
    has_purple_switch_route = has_purple_switches(state, player, "Dire, Dire Docks")
    has_sub_poles_movement_route = (
            state.has("Dire, Dire Docks - Bowser's Sub", player)
            and has_poles
            and has_action(state, player, "Triple Jump", level_name)
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
    if state.has("Snowman's Land - Cannon Unlock", player) or \
            state.multiworld.worlds[player].options.no_despawns.value:
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
    has_long_jump = has_action(state, player, "Long Jump", level_name)
    has_triple_jump = has_action(state, player, "Triple Jump", level_name)
    has_dive = has_action(state, player, "Dive", level_name)
    can_reach_top_of_express_elevator = state.can_reach(
        "Wet-Dry World - Top of the Express Elevator", "Region", player)
    has_movement_top_route = (
        any(has_action(state, player, action, level_name)
            for action in ("Wall Kick", "Triple Jump", "Side Flip", "Backflip"))
        or allows_moveless(state, player)
    )
    can_reach_top_from_express_elevator = can_reach_top_of_express_elevator and (
        has_long_jump or allows_moveless(state, player))
    can_reach_mid_high_from_mid = has_water_level_diamond and (
        can_reach_top_of_express_elevator or has_triple_jump and has_dive)

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
        return has_movement_top_route or can_reach_top_from_express_elevator or "highest" in water_levels

    def route_has_downtown(water_levels: Set[str]) -> bool:
        return (
            "highest" in water_levels
            or state.has("Wet-Dry World - Cannon Unlock", player)
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
        if can_reach_top_of_express_elevator:
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
    has_huge_top_gate = state.has("Tiny-Huge Island - Cannon Unlock", player) or has_top_return_movement
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
                route_total += 30
                if has_thi_purple_switches:
                    route_total += 1
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
            if state.has("Tiny-Huge Island - Cannon Unlock", player) or has_long_jump:
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


def has_wing_cap(state: CollectionState, player: int, level_name: str) -> bool:
    options = state.multiworld.worlds[player].options
    item_name = f"{level_name} - Wing Cap" if options.per_level_cap_items else "Wing Cap"
    return state.has(item_name, player)


def has_vanish_cap(state: CollectionState, player: int, level_name: str) -> bool:
    options = state.multiworld.worlds[player].options
    item_name = f"{level_name} - Vanish Cap" if options.per_level_cap_items else "Vanish Cap"
    return state.has(item_name, player)


def princess_secret_slide_coins(state: CollectionState, player: int, coins: int) -> bool:
    level_name = "The Princess's Secret Slide"
    reachable_coins = 0
    if has_unlock(
            state, player, "coin_object_unlocks",
            "Single Yellow Coins", "Princess's Secret Slide - Single Yellow Coins"):
        reachable_coins += 20
    if has_unlock(
            state, player, "coin_object_unlocks",
            "Horizontal Coin Lines", "Princess's Secret Slide - Horizontal Coin Lines"):
        reachable_coins += 30
    if has_action(state, player, "Ground Pound", level_name) and has_unlock(
            state, player, "coin_object_unlocks",
            "Blue Coin Blocks", "Princess's Secret Slide - Blue Coin Block"):
        reachable_coins += 30
    assert reachable_coins <= 80
    return coins <= reachable_coins


def secret_aquarium_coins(state: CollectionState, player: int, coins: int) -> bool:
    reachable_coins = 0
    if has_unlock(
            state, player, "coin_object_unlocks",
            "Red Coins", "Secret Aquarium - Red Coins"):
        reachable_coins += 16
    if has_unlock(
            state, player, "coin_object_unlocks",
            "Horizontal Coin Rings", "Secret Aquarium - Horizontal Coin Rings"):
        reachable_coins += 8
    if has_unlock(
            state, player, "coin_object_unlocks",
            "Vertical Coin Rings", "Secret Aquarium - Vertical Coin Rings"):
        reachable_coins += 32
    assert reachable_coins <= 56
    return coins <= reachable_coins


def wing_mario_over_the_rainbow_coins(state: CollectionState, player: int, coins: int) -> bool:
    level_name = "Wing Mario Over the Rainbow"
    reachable_coins = 2
    has_wing_cap_item = has_wing_cap(state, player, level_name)
    has_long_jump_capless = has_action(state, player, "Long Jump", level_name) and allows_capless(state, player)

    if state.can_reach("Wing Mario Over the Rainbow - Cannon", "Region", player):
        reachable_coins += 54
    elif has_wing_cap_item and has_action(state, player, "Triple Jump", level_name):
        reachable_coins += 46
    else:
        if has_long_jump_capless:
            reachable_coins += 4
        elif has_wing_cap_item and allows_moveless(state, player):
            reachable_coins += 2
    return coins <= reachable_coins


def tower_of_the_wing_cap_coins(state: CollectionState, player: int, coins: int) -> bool:
    return coins <= state.multiworld.worlds[player].options.tower_of_the_wing_cap_coinsanity_max_coins.value


def vanish_cap_under_the_moat_coins(state: CollectionState, player: int, coins: int) -> bool:
    level_name = "Vanish Cap Under the Moat"
    has_single_yellow_coins = has_unlock(
        state, player, "coin_object_unlocks",
        "Single Yellow Coins", f"{level_name} - Single Yellow Coins")
    has_red_coins = has_unlock(
        state, player, "coin_object_unlocks",
        "Red Coins", f"{level_name} - Red Coins")
    has_horizontal_coin_lines = has_unlock(
        state, player, "coin_object_unlocks",
        "Horizontal Coin Lines", f"{level_name} - Horizontal Coin Lines")
    has_three_coin_block = has_unlock(
        state, player, "coin_object_unlocks",
        "Three-Coin Blocks", f"{level_name} - Three-Coin Block")
    has_movement = any(has_action(state, player, action, level_name)
                       for action in ("Triple Jump", "Ledge Grab", "Side Flip", "Backflip", "Wall Kick"))
    has_checkerboards = has_checkerboard_platforms(state, player, level_name)
    can_drop_to_checkerboards = can_use_logic_trick(
        state, player, "logic_vcutm_drop_to_checkerboard_platforms", "Vanish Cap Under the Moat - Coins Star")
    can_crawl_back_then_drop = can_use_logic_trick(
        state, player, "logic_vcutm_drop_to_checkerboard_platforms_after_crawling_back_up",
        "Vanish Cap Under the Moat - Coins Star")

    # https://ukikipedia.net/mediawiki/index.php?title=Vanish_Cap_under_the_Moat&oldid=19286

    # Line of coins at bottom of slide, around the corner to left
    earlier_coins = 5 if has_horizontal_coin_lines else 0
    # 4 Red Coins
    if has_red_coins:
        earlier_coins += 8

    later_coins = 0
    if has_movement or can_drop_to_checkerboards or can_crawl_back_then_drop:
        # 3 coins in an ! block right before all the turning lifts
        if has_three_coin_block:
            later_coins += 3
        if has_checkerboards and has_red_coins:
            # 4 Red Coins
            later_coins += 8
        if has_checkerboards and has_single_yellow_coins and has_vanish_cap(state, player, level_name):
            # 3 coins by star marker at very end
            later_coins += 3

    if has_movement or can_crawl_back_then_drop:
        reachable_coins = earlier_coins + later_coins
    elif can_drop_to_checkerboards:
        reachable_coins = max(earlier_coins, later_coins)
    else:
        reachable_coins = earlier_coins
    assert reachable_coins <= 27
    return coins <= reachable_coins


def cavern_of_the_metal_cap_coins(state: CollectionState, player: int, coins: int) -> bool:
    level_name = "Cavern of the Metal Cap"
    has_red_coins = has_unlock(
        state, player, "coin_object_unlocks",
        "Red Coins", f"{level_name} - Red Coins")
    has_horizontal_coin_lines = has_unlock(
        state, player, "coin_object_unlocks",
        "Horizontal Coin Lines", f"{level_name} - Horizontal Coin Lines")
    has_horizontal_coin_rings = has_unlock(
        state, player, "coin_object_unlocks",
        "Horizontal Coin Rings", f"{level_name} - Horizontal Coin Rings")
    has_snufits = has_unlock(
        state, player, "enemy_unlocks",
        "Snufits", f"{level_name} - Snufits")

    # Sloped line of coins under the water after first metal cap block
    reachable_coins = 5 if has_horizontal_coin_lines else 0
    # Line of coins after rock bridge over the water
    if has_horizontal_coin_lines:
        reachable_coins += 5
    # 4 Snufits
    if has_snufits:
        reachable_coins += 8
    # 4 Red Coins
    if has_red_coins:
        reachable_coins += 8

    if (has_metal_cap(state, player, level_name)
            or can_use_logic_trick(
                state, player,
                "logic_cotmc_deep_underwater_coins_without_metal_cap",
                "Cavern of the Metal Cap - Coins Star")):
        # Ring of coins around star marker under the water
        if has_horizontal_coin_rings:
            reachable_coins += 8
        # Line of coins on bottom of stream under bridge
        if has_horizontal_coin_lines:
            reachable_coins += 5
        # 4 Red Coins
        if has_red_coins:
            reachable_coins += 8
    assert reachable_coins <= 47
    return coins <= reachable_coins


def bowser_in_the_dark_world_coins(state: CollectionState, player: int, coins: int) -> bool:
    level_name = "Bowser in the Dark World"
    has_single_yellow_coins = has_unlock(
        state, player, "coin_object_unlocks",
        "Single Yellow Coins", f"{level_name} - Single Yellow Coins")
    has_red_coins = has_unlock(
        state, player, "coin_object_unlocks",
        "Red Coins", f"{level_name} - Red Coins")
    has_horizontal_coin_lines = has_unlock(
        state, player, "coin_object_unlocks",
        "Horizontal Coin Lines", f"{level_name} - Horizontal Coin Lines")
    has_horizontal_coin_rings = has_unlock(
        state, player, "coin_object_unlocks",
        "Horizontal Coin Rings", f"{level_name} - Horizontal Coin Rings")
    has_three_coin_block = has_unlock(
        state, player, "coin_object_unlocks",
        "Three-Coin Blocks", f"{level_name} - Three-Coin Block")
    has_goombas = has_unlock(
        state, player, "enemy_unlocks",
        "Goombas", f"{level_name} - Goombas")
    has_slope_access = (
        has_purple_switches(state, player, level_name)
        or can_use_logic_trick(state, player, "logic_bitdw_purple_switch_bypass", level_name)
    )

    # https://ukikipedia.net/mediawiki/index.php?title=Bowser_in_the_Dark_World&oldid=18919

    # Three rings of eight coins.
    reachable_coins = 24 if has_horizontal_coin_rings else 0
    # Two lines of five coins.
    if has_horizontal_coin_lines:
        reachable_coins += 10
    if has_single_yellow_coins:
        # Eighteen are before the Purple Switch slope.
        reachable_coins += 18
        # The final three are on the slope leading to Bowser.
        if has_slope_access:
            reachable_coins += 3
    if has_three_coin_block:
        reachable_coins += 3
    if has_goombas:
        reachable_coins += 6
    if has_red_coins:
        # Six Red Coins are reachable before the Purple Switch slope.
        reachable_coins += 12
        # The final two Red Coins cannot be collected with the slope trick.
        if has_purple_switches(state, player, level_name):
            reachable_coins += 4
    assert reachable_coins <= 80
    return coins <= reachable_coins


def bowser_in_the_fire_sea_coins(state: CollectionState, player: int, coins: int) -> bool:
    level_name = "Bowser in the Fire Sea"
    has_single_yellow_coins = has_unlock(
        state, player, "coin_object_unlocks",
        "Single Yellow Coins", f"{level_name} - Single Yellow Coins")
    has_red_coins = has_unlock(
        state, player, "coin_object_unlocks",
        "Red Coins", f"{level_name} - Red Coins")
    has_horizontal_coin_lines = has_unlock(
        state, player, "coin_object_unlocks",
        "Horizontal Coin Lines", f"{level_name} - Horizontal Coin Lines")
    has_horizontal_coin_rings = has_unlock(
        state, player, "coin_object_unlocks",
        "Horizontal Coin Rings", f"{level_name} - Horizontal Coin Rings")
    has_vertical_coin_lines = has_unlock(
        state, player, "coin_object_unlocks",
        "Vertical Coin Lines", f"{level_name} - Vertical Coin Lines")
    has_three_coin_block = has_unlock(
        state, player, "coin_object_unlocks",
        "Three-Coin Blocks", f"{level_name} - Three-Coin Block")
    has_ten_coin_block = has_unlock(
        state, player, "coin_object_unlocks",
        "Ten-Coin Blocks", f"{level_name} - Ten-Coin Block")
    has_bob_omb = has_unlock(
        state, player, "enemy_unlocks",
        "Bob-ombs", f"{level_name} - Bob-omb")
    has_bullies = has_unlock(
        state, player, "enemy_unlocks",
        "Bullies", f"{level_name} - Bullies")
    has_goombas = has_unlock(
        state, player, "enemy_unlocks",
        "Goombas", f"{level_name} - Goombas")
    has_climb = has_action(state, player, "Climb", level_name)

    # https://ukikipedia.net/mediawiki/index.php?title=Bowser_in_the_Fire_Sea&oldid=18920

    # 2 coins on the 2 platforms floating in lava at the very beginning
    reachable_coins = 2 if has_single_yellow_coins else 0
    # Line of coins on the second sinking platform at beginning
    if has_horizontal_coin_lines:
        reachable_coins += 5
    # Ring of coins (along with red coin) up a platform to left of bully
    if has_horizontal_coin_rings:
        reachable_coins += 8
    # 1 Bully
    if has_bullies:
        reachable_coins += 1
    # 3 Goombas
    if has_goombas:
        reachable_coins += 3
    # 2 Red Coins
    if has_red_coins:
        reachable_coins += 4

    if ((has_climb
            or can_use_logic_trick(
                state, player, "logic_jump_in_lava", "Bowser in the Fire Sea - Coins Star"))
            and has_three_coin_block):
        # 3 coins in an ! block after rising platform with the poll
        reachable_coins += 3

    if has_climb:
        # Line of coins after elevator (on big grey triangle platform)
        if has_horizontal_coin_lines:
            reachable_coins += 5
        # Ring of coins under wire grid (hang on it to get them)
        if has_horizontal_coin_rings:
            reachable_coins += 8
        # Vertical line of coins, past 2nd ! block (fall through hole to get)
        if has_vertical_coin_lines:
            reachable_coins += 5
        # Sloped line of coins, just before the bob-omb
        if has_horizontal_coin_lines:
            reachable_coins += 5
        # 10 coins in an ! block with the bob-omb
        if has_ten_coin_block:
            reachable_coins += 10
        # Line of coins on third sinking platform after bob-omb
        if has_horizontal_coin_lines:
            reachable_coins += 5
        # 1 Bob-omb
        if has_bob_omb:
            reachable_coins += 1
        # 3 Bullies
        if has_bullies:
            reachable_coins += 3
        # 6 Red Coins
        if has_red_coins:
            reachable_coins += 12

    assert reachable_coins <= 80
    return coins <= reachable_coins


def bowser_in_the_sky_coins(state: CollectionState, player: int, coins: int) -> bool:
    level_name = "Bowser in the Sky"
    reachable_coins = 23
    if has_action(state, player, "Ground Pound", level_name):
        reachable_coins += 10
    if state.can_reach("Bowser in the Sky - Chuckya", "Region", player):
        reachable_coins += 9
    if state.can_reach("Bowser in the Sky - Arrow Ride", "Region", player):
        reachable_coins += 18
    if state.can_reach("Bowser in the Sky - Top", "Region", player):
        reachable_coins += 16
    return coins <= reachable_coins


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
    if not options.one_up_checks and location_name in locOneUp_table:
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

    def can_mips_skip_thirty_star_door(state):
        return can_use_logic_trick(
            state, player, "logic_castle_30_star_door_mips_skip", "Castle")

    def can_bypass_thirty_star_door(state):
        return (
            has_thirty_star_key(state)
            or can_use_logic_trick(state, player, "logic_castle_30_star_door_sblj", "Castle")
            or can_use_logic_trick(state, player, "logic_castle_30_star_door_crackslide", "Castle")
            or can_use_logic_trick(
                state, player, "logic_castle_30_star_door_crackslide_double_jump", "Castle")
            or can_use_logic_trick(state, player, "logic_castle_30_star_door_crackslide_yolo", "Castle")
            or can_mips_skip_thirty_star_door(state)
        )

    def can_bypass_fifty_star_door(state):
        return (
            has_third_floor_key(state)
            or can_use_logic_trick(state, player, "logic_castle_50_star_door_blj", "Castle")
        )

    def can_bypass_seventy_star_door(state):
        return (
            has_endless_stairs_key(state)
            or can_use_logic_trick(state, player, "logic_castle_70_star_door_blj", "Castle")
        )

    def has_bowser_stage_1up_unlock(state, stage_item_name: str, vanilla_key_rule: Callable) -> bool:
        option = options.bowser_stage_1ups
        if option.value == option.option_always_spawn:
            return True
        if option.value == option.option_vanilla:
            return vanilla_key_rule(state)
        if option.value == option.option_global:
            return state.has("Bowser Stage Extra 1-Ups", player)
        return state.has(stage_item_name, player)

    def has_bowser_arena_bombs(state, stage_name: str, required_hits: int) -> bool:
        if options.bowser_bombs.value == options.bowser_bombs.option_not_shuffled:
            return True
        if options.bowser_bombs.value == options.bowser_bombs.option_global:
            bomb_count = state.count("Progressive Bowser Arena Bomb", player)
            if stage_name == "Bowser in the Sky":
                bomb_count += state.count("Bowser in the Sky - Progressive Bowser Arena Bomb", player)
            return bomb_count >= required_hits
        return state.has(f"{stage_name} - Progressive Bowser Arena Bomb", player, required_hits)

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
                                lambda state: state.has("Unlock Big Boo's Haunt", player))
    connect_randomized_entrance("Menu", "The Princess's Secret Slide")
    connect_randomized_entrance("Jolly Roger Bay Door", "The Secret Aquarium",
                                rf.build_rule(
                                    "SF/BF | TJ & LG | logic_secret_aquarium_triple_jump | "
                                    "logic_secret_aquarium_wall_kick_and_ledge_grab | "
                                    "logic_secret_aquarium_wall_kick | logic_secret_aquarium_ledge_grab"))
    connect_randomized_entrance("Menu", "Tower of the Wing Cap",
                                lambda state: state.has("Unlock Tower of the Wing Cap", player))
    connect_randomized_entrance("Menu", "Bowser in the Dark World", has_first_floor_key)

    connect_regions(multiworld, player, "Menu", "Basement", has_basement_key)

    connect_randomized_entrance("Basement", "Hazy Maze Cave",
                                rf.build_rule("", painting_lvl_name="Hazy Maze Cave"))
    connect_randomized_entrance("Basement", "Lethal Lava Land",
                                rf.build_rule("", painting_lvl_name="Lethal Lava Land"))
    connect_randomized_entrance("Basement", "Shifting Sand Land",
                                rf.build_rule("", painting_lvl_name="Shifting Sand Land"))
    ddd_entry_rule = rf.build_rule("", painting_lvl_name="Dire, Dire Docks")
    connect_randomized_entrance("Basement", "Dire, Dire Docks",
                                lambda state: can_bypass_thirty_star_door(state) and ddd_entry_rule(state))
    connect_randomized_entrance("Hazy Maze Cave", "Cavern of the Metal Cap",
                                rf.build_rule("HMC_SWIMMING_BEAST"))
    connect_randomized_entrance("Menu", "Vanish Cap Under the Moat",
                                lambda state: state.has("Unlock Vanish Cap Under the Moat", player))
    connect_randomized_entrance("Basement", "Bowser in the Fire Sea",
                                lambda state: can_bypass_thirty_star_door(state) and
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
                                rf.build_rule("", painting_lvl_name="Tiny Island"))
    connect_randomized_entrance("Second Floor", "Tiny-Huge Island (Huge)",
                                rf.build_rule("", painting_lvl_name="Huge Island"))
    connect_regions(multiworld, player, "Tiny-Huge Island - Tiny Piranha Area", "Tiny-Huge Island - Huge Piranha Area",
                    name="Tiny-Huge Island - Tiny Piranha Area to Huge Piranha Area")
    connect_regions(multiworld, player, "Tiny-Huge Island - Huge Piranha Area", "Tiny-Huge Island - Tiny Piranha Area",
                    name="Tiny-Huge Island - Huge Piranha Area to Tiny Piranha Area")
    connect_regions(multiworld, player, "Tiny-Huge Island - Huge Piranha Area", "Tiny-Huge Island (Huge)",
                    name="Tiny-Huge Island - Huge Piranha Area to Huge Island")
    connect_regions(multiworld, player, "Tiny-Huge Island - Tiny Piranha Area", "Tiny-Huge Island (Tiny)",
                    name="Tiny-Huge Island - Tiny Piranha Area to Tiny Island")
    connect_regions(multiworld, player, "Tiny-Huge Island - Tiny Main", "Tiny-Huge Island (Huge)",
                    name="Tiny-Huge Island - Tiny Main to Huge Island")
    connect_regions(multiworld, player, "Tiny-Huge Island (Huge)", "Tiny-Huge Island - Tiny Main",
                    name="Tiny-Huge Island - Huge Island to Tiny Main")

    connect_regions(multiworld, player, "Second Floor", "Third Floor", can_bypass_fifty_star_door)

    ttc_entrance_rule = rf.build_rule(
        "LG/TJ/SF/BF | logic_castle_ttc_with_wall_kick | "
        "logic_castle_ttc_with_long_jump_and_kick | logic_castle_ttc_with_dive_and_kick",
        painting_lvl_name="Tick Tock Clock")
    for ttc_entrance in sm64_ttc_entrances:
        connect_randomized_entrance("Third Floor", ttc_entrance, ttc_entrance_rule)
    third_floor_alcove_rule = rf.build_rule(
        "TJ/SF/BF | logic_castle_3f_alcoves_with_wall_kick | "
        "logic_castle_3f_alcoves_with_dive_and_kick | "
        "logic_castle_3f_alcoves_with_dive_and_ledge_grab | "
        "logic_castle_3f_alcoves_with_long_jump_and_ledge_grab")
    connect_randomized_entrance("Third Floor", "Rainbow Ride", third_floor_alcove_rule)
    connect_randomized_entrance("Third Floor", "Wing Mario Over the Rainbow",
                                third_floor_alcove_rule)
    connect_regions(multiworld, player, "Third Floor", "Bowser in the Sky", can_bypass_seventy_star_door)

    # Course Rules
    # Bob-omb Battlefield
    rf.assign_rule("Bob-omb Battlefield - Big Bob-Omb on the Summit", "BOB_KING")
    rf.assign_rule("Bob-omb Battlefield - Footrace with Koopa The Quick", "BOB_KOOPA")
    rf.assign_rule("Bob-omb Battlefield - Island",
                   "CANN | logic_bob_island_without_cannon | logic_bob_island_long_jump | "
                   "logic_bob_island_koopa_shell | "
                   "logic_bob_mario_wings_to_the_sky_without_cannon")
    rf.assign_rule("Bob-omb Battlefield - Mario Wings to the Sky",
                   "CANN & WC | logic_bob_mario_wings_capless | "
                   "logic_bob_mario_wings_to_the_sky_without_cannon")
    rf.assign_rule("Bob-omb Battlefield - Behind Chain Chomp's Gate",
                   "WOODEN_POSTS & GP | logic_bob_chain_chomp_gate_without_ground_pound")
    rf.assign_rule("Bob-omb Battlefield - Bob-omb Buddy", "BOB_BUDDY")
    rf.assign_rule("Bob-omb Battlefield - Cannon Tree 1-Up", "CL/TJ/BF/SF")
    add_rule(
        multiworld.get_location("Bob-omb Battlefield - Mario Wings to the Sky", player),
        lambda state: (
            has_unlock(
                state, player, "coin_object_unlocks",
                "Single Yellow Coins", "Bob-omb Battlefield - Single Yellow Coins")
            or has_unlock(
                state, player, "coin_object_unlocks",
                "Vertical Coin Rings", "Bob-omb Battlefield - Vertical Coin Rings")
            or can_use_logic_trick(
                state, player, "logic_bob_mario_wings_without_coin_markers",
                "Bob-omb Battlefield - Mario Wings to the Sky")))
    rf.assign_rule("Bob-omb Battlefield - Find the 8 Red Coins", "RED_COINS")
    # Whomp's Fortress
    rf.assign_rule("Whomp's Fortress - To the Top of the Fortress", "WF_FORTRESS")
    rf.assign_rule("Whomp's Fortress - Chip Off Whomp's Block", "WF_KING & GP")
    rf.assign_rule(
        "Whomp's Fortress - Top",
        "CHECKERBOARD_PLATFORMS | WF_HOOT | WK & SF/TJ | CL & DV/LG | "
        "logic_wf_caged_top_access_with_cannon | logic_wf_caged_top_access_with_sf_lg | "
        "logic_wf_caged_top_access_with_tj")
    rf.assign_rule(
        "Whomp's Fortress - Shoot into the Wild Blue",
        "CANN | logic_wf_into_the_wild_blue_yonder_wall_kick | "
        "logic_wf_into_the_wild_blue_yonder_long_jump | logic_wf_into_the_wild_blue_yonder_moveless")
    rf.assign_rule("Whomp's Fortress - Fall onto the Caged Island",
                   "WF_HOOT & CL | "
                   "logic_wf_caged_island_cage_triple_jump | "
                   "logic_wf_caged_island_cage_wk_long_jump | "
                   "logic_wf_caged_island_cage_wk_jump | "
                   "logic_wf_caged_island_top_fortress_long_jump")
    rf.assign_rule(
        "Whomp's Fortress - Blast Away the Wall",
        "CANN | logic_wf_blast_away_wall_cannonless_backflip | logic_wf_blast_away_wall_cannonless")
    rf.assign_rule("Whomp's Fortress - Bob-omb Buddy", "WF_BUDDY")
    rf.assign_rule("Whomp's Fortress - Red Coins on the Floating Isle", "RED_COINS")
    rf.assign_rule("Whomp's Fortress - Flagpole 1-Up", "CL")
    rf.assign_rule("Whomp's Fortress - Tower Alcove 1-Up", "WF_FORTRESS")
    # Jolly Roger Bay
    rf.assign_rule("Jolly Roger Bay - Plunder in the Sunken Ship", "JRB_SUNKEN_SHIP")
    rf.assign_rule("Jolly Roger Bay - Can the Eel Come Out to Play?", "JRB_UNAGI")
    rf.assign_rule(
        "Jolly Roger Bay - Upper",
        "TJ/BF/SF/WK | logic_jrb_upper_ledge_grab | "
        "logic_jrb_upper_dive_and_kick | logic_jrb_upper_cannon")
    rf.assign_rule("Jolly Roger Bay - Red Coins on the Ship Afloat",
                   "RED_COINS & JRB_RAISED_SHIP & CL | "
                   "RED_COINS & JRB_RAISED_SHIP & logic_jrb_pillar_red_coin_moves | "
                   "RED_COINS & JRB_RAISED_SHIP & logic_jrb_pillar_red_coin_cannon")
    rf.assign_rule("Jolly Roger Bay - Blast to the Stone Pillar",
                   "CANN+CL | logic_jrb_stone_pillar_cannonless | "
                   "logic_jrb_stone_pillar_cannon_no_climb")
    rf.assign_rule(
        "Jolly Roger Bay - Through the Jet Stream",
        "JRB_JET_STREAM & MC | JRB_JET_STREAM & logic_jrb_jet_stream_capless")
    rf.assign_rule("Jolly Roger Bay - Bob-omb Buddy", "JRB_BUDDY")
    rf.assign_rule("Jolly Roger Bay - Stone Pillar 1-Up", "CANN")
    # Cool, Cool Mountain
    rf.assign_rule("Cool, Cool Mountain - Big Penguin Race", "CCM_BIG_PENGUIN")
    rf.assign_rule("Cool, Cool Mountain - Snowman's Lost His Head", "CCM_SNOWMAN_HEAD")
    rf.assign_rule("Cool, Cool Mountain - Li'l Penguin Lost", "CCM_BABY_PENGUINS")
    rf.assign_rule("Cool, Cool Mountain - Frosty Slide for 8 Red Coins", "RED_COINS")
    rf.assign_rule(
        "Cool, Cool Mountain - Wall Kicks Will Work",
        "TJ/WK | logic_ccm_wall_kicks_will_work_spin_jump")
    # Big Boo's Haunt
    rf.assign_rule("Big Boo's Haunt - Go on a Ghost Hunt", "BOOS & BIG_BOO")
    rf.assign_rule(
        "Big Boo's Haunt - Ride Big Boo's Merry-Go-Round",
        "BBH_MERRY_GO_ROUND & BOOS & BIG_BOO")
    rf.assign_rule(
        "Big Boo's Haunt - Second Floor",
        "BBH_STAIRCASE | logic_bbh_third_floor_triple_jump_wall_kick | "
        "logic_bbh_third_floor_side_flip_wall_kick")
    rf.assign_rule(
        "Big Boo's Haunt - Third Floor",
        "WK+LG | logic_bbh_third_floor_wall_kick | logic_bbh_third_floor_side_flip")
    rf.assign_rule("Big Boo's Haunt - Roof", "LJ | logic_bbh_roof_without_long_jump")
    rf.assign_rule("Big Boo's Haunt - Big Boo's Balcony", "BIG_BOO")
    rf.assign_rule("Big Boo's Haunt - Secret of the Haunted Books", "KK")
    rf.assign_rule("Big Boo's Haunt - Seek the 8 Red Coins", "RED_COINS & BF/WK/TJ/SF")
    rf.assign_rule("Big Boo's Haunt - Eye to Eye in the Secret Room", "VC & MR_IS")
    rf.assign_rule("Big Boo's Haunt - Shed Roof 1-Up", "TJ/SF/WK")
    # Haze Maze Cave
    rf.assign_rule("Hazy Maze Cave - Swimming Beast in the Cavern", "HMC_SWIMMING_BEAST")
    rf.assign_rule("Hazy Maze Cave - Red Coin Area",
                   "CHECKERBOARD_PLATFORMS & CL & WK/LG/BF/SF/TJ | CHECKERBOARD_PLATFORMS & MOVELESS & WK")
    rf.assign_rule("Hazy Maze Cave - Pit Islands", "TJ+CL | MOVELESS & WK & TJ/LJ | MOVELESS & WK+SF+LG")
    rf.assign_rule("Hazy Maze Cave - Metal-Head Mario Can Move!",
                   "PURPLE_SWITCHES & LJ+MC | PURPLE_SWITCHES & CAPLESS & LJ+TJ | "
                   "PURPLE_SWITCHES & CAPLESS & MOVELESS & LJ/TJ/WK")
    rf.assign_rule("Hazy Maze Cave - Navigating the Toxic Maze", "WK/SF/BF/TJ")
    rf.assign_rule("Hazy Maze Cave - Watch for Rolling Rocks", "WK")
    # Lethal Lava Land
    add_rule(
        multiworld.get_location("Lethal Lava Land - Boil the Big Bully", player),
        lambda state: has_unlock(
            state, player, "enemy_unlocks",
            "Big Bully", "Lethal Lava Land - Big Bullies"))
    add_rule(
        multiworld.get_location("Lethal Lava Land - Bully the Bullies", player),
        lambda state: (
            has_unlock(state, player, "enemy_unlocks", "Bullies", "Lethal Lava Land - Bullies")
            and has_unlock(state, player, "enemy_unlocks", "Big Bully", "Lethal Lava Land - Big Bullies")
        ))
    add_rule(
        multiworld.get_location("Lethal Lava Land - 8-Coin Puzzle with 15 Pieces", player),
        lambda state: (
            has_unlock(
                state, player, "coin_object_unlocks",
                "Red Coins", "Lethal Lava Land - Red Coins")
            and can_collect_all_lethal_lava_land_red_coins(
                state, player, "Lethal Lava Land - 8-Coin Puzzle with 15 Pieces")
        ))
    rf.assign_rule(
        "Lethal Lava Land - Red-Hot Log Rolling",
        "WC+TJ | LLL_ROLLING_LOG | LLL_KOOPA_SHELL | logic_jump_in_lava")
    for location_name in (
            "Lethal Lava Land - Northeast Brown Platform 1-Up",
            "Lethal Lava Land - Boil the Big Bully Star Lava 1-Up",
            "Lethal Lava Land - Northwest Curve 1-Up",
    ):
        rf.assign_rule(location_name, "LLL_KOOPA_SHELL | logic_jump_in_lava")
    rf.assign_rule(
        "Lethal Lava Land - Hot-Foot-It Ledge",
        "CL | logic_lll_hot_foot_it_with_wall_kick | logic_lll_hot_foot_it_with_triple_jump | "
        "logic_lll_hot_foot_it_with_side_flip | logic_lll_hot_foot_it_with_backflip | "
        "logic_lll_hot_foot_it_with_no_movement")
    rf.assign_rule("Lethal Lava Land - Upper Volcano", "CL")
    connect_regions(
        multiworld, player, "Lethal Lava Land - Upper Volcano", "Lethal Lava Land - Elevator Tour",
        rf.build_rule(
            "CHECKERBOARD_PLATFORMS",
            arbitrary_item_names=rf.get_arbitrary_item_names("Lethal Lava Land"),
            action_item_names=rf.get_action_item_names("Lethal Lava Land")),
        name="Lethal Lava Land - Upper Volcano to Elevator Tour")
    connect_regions(
        multiworld, player, "Lethal Lava Land - Hot-Foot-It Ledge", "Lethal Lava Land - Elevator Tour",
        rf.build_rule(
            "logic_lll_elevator_tour_long_jump | CL & logic_lll_elevator_tour_triple_jump_or_dive",
            arbitrary_item_names=rf.get_arbitrary_item_names("Lethal Lava Land"),
            action_item_names=rf.get_action_item_names("Lethal Lava Land")),
        name="Lethal Lava Land - Hot-Foot-It Ledge to Elevator Tour")
    # Shifting Sand Land
    rf.assign_rule("Shifting Sand Land - In the Talons of the Big Bird", "SSL_KLEPTO")
    rf.assign_rule(
        "Shifting Sand Land - Stone Structure",
        "TJ/SF/BF | logic_ssl_stone_structure_shy_guy_bounce")
    rf.assign_rule(
        "Shifting Sand Land - Upper Pyramid",
        "SSL_PYRAMID_ELEVATOR & TJ+WC+GP | SSL_PYRAMID_ELEVATOR & CANN+WC+GP | "
        "SSL_PYRAMID_ELEVATOR & logic_ssl_pillars_shell | "
        "SSL_PYRAMID_ELEVATOR & logic_ssl_pillars_side_flip_or_kick | CL")
    rf.assign_rule("Shifting Sand Land - Stand Tall on the Four Pillars",
                   "{Shifting Sand Land - Upper Pyramid} & SSL_PYRAMID_ELEVATOR & EYEROK | "
                   "logic_ssl_stand_tall_without_pyramid_elevator & EYEROK & LG/KK")
    # TODO: Verify what the old "TJ/SF/BF & CAPLESS" route represents before restoring it.
    rf.assign_rule(
        "Shifting Sand Land - Free Flying for 8 Red Coins",
        "RED_COINS & TJ+WC | RED_COINS & CANN+WC | "
        "RED_COINS & logic_ssl_three_red_coins_with_tweesters & "
        "logic_ssl_one_red_coin_with_shy_guy_spin_jump")
    rf.assign_rule("Shifting Sand Land - Oasis Tree 1-Up", "CL/TJ/BF/SF")
    rf.assign_rule("Shifting Sand Land - Above Quicksand Pit 1-Up", "WC & TJ/CANN | LJ")
    rf.assign_rule("Shifting Sand Land - Pyramid Mummified Thwomp 1-Up", "THWOMP")
    rf.assign_rule(
        "Shifting Sand Land - Pyramid Right Path 1-Up",
        "{Shifting Sand Land - Upper Pyramid} | CL/TJ/SF/BF")
    # Dire, Dire Docks
    rf.assign_rule("Dire, Dire Docks - Board Bowser's Sub",
                   "PURPLE_SWITCHES & DDD_BOWSER_SUB | TJ & MOVELESS & DDD_BOWSER_SUB")
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
    rf.assign_rule("Snowman's Land - Inside Igloo Block 1-Up", "VC & TJ/SF/BF/WK/LG | MOVELESS & VC")
    # Wet-Dry World
    rf.assign_rule("Wet-Dry World - Low Water to Mid Water", "WDW_WATER_LEVEL_DIAMOND")
    rf.assign_rule("Wet-Dry World - Mid Water to Low Water", "WDW_WATER_LEVEL_DIAMOND")
    rf.assign_rule("Wet-Dry World - Mid Water to Mid-High Water",
                   "WDW_WATER_LEVEL_DIAMOND & {Wet-Dry World - Top of the Express Elevator} | "
                   "WDW_WATER_LEVEL_DIAMOND & TJ+DV")
    rf.assign_rule("Wet-Dry World - Mid-High Water to Mid Water", "WDW_WATER_LEVEL_DIAMOND")
    rf.assign_rule("Wet-Dry World - Mid-High Water to High Water", "{Wet-Dry World - Top}")
    rf.assign_rule("Wet-Dry World - High Water to Mid-High Water", "WDW_WATER_LEVEL_DIAMOND")
    rf.assign_rule("Wet-Dry World - Highest Water to High Water", "WDW_WATER_LEVEL_DIAMOND")
    rf.assign_rule("Wet-Dry World - Top of the Express Elevator",
                   "PURPLE_SWITCHES | WK/TJ/SF/BF/MOVELESS & LJ/TJ/LG/MOVELESS")
    rf.assign_rule("Wet-Dry World - Top",
                   "WK/TJ/SF/BF | MOVELESS | {Wet-Dry World - Top of the Express Elevator} & LJ/MOVELESS | "
                   "{Wet-Dry World - Highest Water}")
    rf.assign_rule("Wet-Dry World - Downtown",
                   "{Wet-Dry World - Highest Water} & LG | CANN | {Wet-Dry World - Top} & MOVELESS & TJ+DV")
    rf.assign_rule("Wet-Dry World - Go to Town for Red Coins",
                   "WDW_WATER_LEVEL_DIAMOND & WK | WDW_WATER_LEVEL_DIAMOND & MOVELESS & TJ")
    rf.assign_rule("Wet-Dry World - Shocking Arrow Lifts!",
                   "{Wet-Dry World - Low Water} | {Wet-Dry World - Mid-High Water} | "
                   "{Wet-Dry World - High Water} | {Wet-Dry World - Top} & TJ/LG/LJ")
    rf.assign_rule("Wet-Dry World - Express Elevator--Hurry Up!",
                   "{Wet-Dry World - Low Water} & BF/SF/WK | "
                   "{Wet-Dry World - Low Water} & WDW_WATER_LEVEL_DIAMOND")
    rf.assign_rule("Wet-Dry World - Secrets in the Shallows & Sky",
                   "{Wet-Dry World - Top of the Express Elevator} & LJ | "
                   "{Wet-Dry World - Top of the Express Elevator} & {Wet-Dry World - Top} | "
                   "{Wet-Dry World - Top of the Express Elevator} & WDW_WATER_LEVEL_DIAMOND")
    rf.assign_rule("Wet-Dry World - Quick Race Through Downtown!",
                   "WDW_WATER_LEVEL_DIAMOND & VC & WK/BF | "
                   "WDW_WATER_LEVEL_DIAMOND & VC & TJ+LG+PURPLE_SWITCHES | "
                   "WDW_WATER_LEVEL_DIAMOND & MOVELESS & VC & TJ | "
                   "WDW_WATER_LEVEL_DIAMOND & MOVELESS & DJ/SF/BF & KK")
    rf.assign_rule("Wet-Dry World - Downtown Block 1-Up", "WDW_WATER_LEVEL_DIAMOND")
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
    rf.assign_rule("Tiny-Huge Island - Huge Piranha Area to Tiny Piranha Area", "THI_WARP_PIPES")
    rf.assign_rule("Tiny-Huge Island - Tiny Main to Huge Island", "THI_WARP_PIPES")
    rf.assign_rule("Tiny-Huge Island - Huge Island to Tiny Main", "THI_WARP_PIPES")
    rf.assign_rule("Tiny-Huge Island - Huge Piranha Area", "THI_WARP_PIPES & PURPLE_SWITCHES | TJ | LJ+SF | LJ+LG")
    rf.assign_rule("Tiny-Huge Island - Five Itty Bitty Secrets", "PURPLE_SWITCHES")
    rf.assign_rule("Tiny-Huge Island - Rematch with Koopa the Quick", "THI_KOOPA")
    add_rule(multiworld.get_location("Tiny-Huge Island - Rematch with Koopa the Quick", player),
             lambda state: has_tiny_huge_island_rematch_movement(state, player))
    rf.assign_rule("Tiny-Huge Island - Wiggler's Red Coins", "WK")
    rf.assign_rule("Tiny-Huge Island - Make Wiggler Squirm",
                   "{Tiny-Huge Island - Tiny Main} & GP & THI_WARP_PIPES")
    rf.assign_rule("Tiny-Huge Island - Cannon Tree 1-Up", "CANN | CANNLESS")
    rf.assign_rule("Tiny-Huge Island - Cannon Tree Butterfly 1-Up", "CANN | CANNLESS")
    rf.assign_rule("Tiny-Huge Island - Red Coin Cave 1-Up", "WK")
    # Tick Tock Clock
    rf.assign_rule("Tick Tock Clock - Lower", "LG/TJ/SF/BF | MOVELESS & WK | {Tick Tock Clock Stopped} & TTC_SPINNERS")
    rf.assign_rule("Tick Tock Clock - Mid", "CL | MOVELESS & WK")
    rf.assign_rule("Tick Tock Clock - Upper", "{Tick Tock Clock Moving} | WK")
    rf.assign_rule("Tick Tock Clock - Top", "TJ+LG | MOVELESS & WK/TJ")
    rf.assign_rule("Tick Tock Clock - Top Past Spinners", "TTC_SPINNERS | SF+LG | TJ")
    rf.assign_rule("Tick Tock Clock - Midway Up Block 1-Up", "TTC_SPINNERS | LJ+LG")
    rf.assign_rule("Tick Tock Clock - Stop Time for Red Coins", "TTC_SPINNERS")
    rf.assign_rule("Tick Tock Clock - Stomp on the Thwomp", "{Tick Tock Clock Moving} & THWOMP")
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
    # rf.assign_rule("Tower of the Wing Cap - Red Coins", "WC") # ridiculous
    # Cavern of the Metal Cap
    rf.assign_rule("Cavern of the Metal Cap - Red Coins",
                   "MC | logic_cotmc_deep_underwater_coins_without_metal_cap")
    # Vanish Cap Under the Moat
    rf.assign_rule("Vanish Cap Under the Moat - Switch",
                   "CHECKERBOARD_PLATFORMS & WK/TJ/BF/SF/LG | CHECKERBOARD_PLATFORMS & MOVELESS")
    rf.assign_rule("Vanish Cap Under the Moat - Red Coins",
                   "CHECKERBOARD_PLATFORMS & TJ/BF/SF/LG/WK & VC | "
                   "CHECKERBOARD_PLATFORMS & TJ/BF/SF/LG/WK & "
                   "logic_vcutm_wall_kick_over_vanish_cap_grate | "
                   "CHECKERBOARD_PLATFORMS & logic_vcutm_drop_to_checkerboard_platforms & VC | "
                   "CHECKERBOARD_PLATFORMS & logic_vcutm_drop_to_checkerboard_platforms & "
                   "logic_vcutm_wall_kick_over_vanish_cap_grate | "
                   "CHECKERBOARD_PLATFORMS & "
                   "logic_vcutm_drop_to_checkerboard_platforms_after_crawling_back_up & VC | "
                   "CHECKERBOARD_PLATFORMS & "
                   "logic_vcutm_drop_to_checkerboard_platforms_after_crawling_back_up & "
                   "logic_vcutm_wall_kick_over_vanish_cap_grate")
    rf.assign_rule("Vanish Cap Under the Moat - Red Coin Platform 1-Up",
                   "CHECKERBOARD_PLATFORMS & TJ/BF/SF/LG/WK & VC | "
                   "CHECKERBOARD_PLATFORMS & TJ/BF/SF/LG/WK & "
                   "logic_vcutm_wall_kick_over_vanish_cap_grate | "
                   "CHECKERBOARD_PLATFORMS & logic_vcutm_drop_to_checkerboard_platforms & VC | "
                   "CHECKERBOARD_PLATFORMS & logic_vcutm_drop_to_checkerboard_platforms & "
                   "logic_vcutm_wall_kick_over_vanish_cap_grate | "
                   "CHECKERBOARD_PLATFORMS & "
                   "logic_vcutm_drop_to_checkerboard_platforms_after_crawling_back_up & VC | "
                   "CHECKERBOARD_PLATFORMS & "
                   "logic_vcutm_drop_to_checkerboard_platforms_after_crawling_back_up & "
                   "logic_vcutm_wall_kick_over_vanish_cap_grate")
    # Bowser in the Dark World
    rf.assign_rule("Bowser in the Dark World - Red Coins", "RED_COINS & PURPLE_SWITCHES")
    rf.assign_rule("Bowser in the Dark World - Key",
                   "PURPLE_SWITCHES | logic_bitdw_purple_switch_bypass")
    add_rule(
        multiworld.get_location("Bowser in the Dark World - Key", player),
        lambda state: has_bowser_arena_bombs(
            state, "Bowser in the Dark World", options.bowser_in_the_dark_world_hits.value))
    if options.one_up_checks:
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
    rf.assign_rule("Bowser in the Fire Sea - Red Coins", "LG/WK")
    rf.assign_rule("Bowser in the Fire Sea - Near Poles Block 1-Up", "LG/WK")
    rf.assign_rule("Bowser in the Fire Sea - Near Poles 1-Up", "LG/WK")
    add_rule(
        multiworld.get_location("Bowser in the Fire Sea - Key", player),
        lambda state: has_bowser_arena_bombs(
            state, "Bowser in the Fire Sea", options.bowser_in_the_fire_sea_hits.value))
    if options.one_up_checks:
        for location_name in (
                "Bowser in the Fire Sea - Near Poles 1-Up",
                "Bowser in the Fire Sea - Second Stone Structure 1-Up",
        ):
            add_rule(multiworld.get_location(location_name, player),
                     lambda state: has_bowser_stage_1up_unlock(
                         state, "Bowser in the Fire Sea - Extra 1-Ups", has_second_floor_key))
    # Wing Mario Over the Rainbow
    wmotr_flight_rule = "WC & TJ | WC & {Wing Mario Over the Rainbow - Bob-omb Buddy Platform} & CANN"
    rf.assign_rule("Wing Mario Over the Rainbow - Bob-omb Buddy Platform", "WC+TJ | LJ+CAPLESS")
    rf.assign_rule("Wing Mario Over the Rainbow - Cannon", "WC+CANN")
    rf.assign_rule("Wing Mario Over the Rainbow - Block 1-Up", "WC & TJ/CANN")
    # Probably possible with cannon alone, but keep this gated until the route is modeled.
    rf.assign_rule("Wing Mario Over the Rainbow - Cloud 1-Up", wmotr_flight_rule)
    # Bowser in the Sky
    rf.assign_rule("Bowser in the Sky - Chuckya",
                   "TJ/SF/LG/BF/MOVELESS")
    rf.assign_rule("Bowser in the Sky - Arrow Ride",
                   "PURPLE_SWITCHES | MOVELESS")
    rf.assign_rule("Bowser in the Sky - Top",
                   "CL | MOVELESS & TJ+WK+LG")
    if options.blocksanity:
        blocksanity_rules = {
            "Big Boo's Haunt - Back Entrance Vanish Cap Block": "VC",
            "Big Boo's Haunt - Second Floor Vanish Cap Block": "VC",
            "Big Boo's Haunt - Secret Room Vanish Cap Block": "VC",
            "Bowser in the Dark World - Metal Cap Block": "MC",
            "Bob-omb Battlefield - Near Flower Patches Wing Cap Block": "WC",
            "Bob-omb Battlefield - Wooden Ramp Wing Cap Block": "WC",
            "Bob-omb Battlefield - Island Wing Cap Block": "WC",
            "Castle - Roof Wing Cap Block": "WC",
            "Cavern of the Metal Cap - First Metal Cap Block": "MC",
            "Cavern of the Metal Cap - Near Switch Metal Cap Block": "MC",
            "Dire, Dire Docks - Metal Cap Block": "MC",
            "Dire, Dire Docks - Vanish Cap Block": "VC",
            "Hazy Maze Cave - Beginning Metal Cap Block": "MC",
            "Hazy Maze Cave - Metal-Head Mario Can Move Metal Cap Block": "MC",
            "Hazy Maze Cave - Toxic Maze Near Empty Alcove Metal Cap Block": "MC",
            "Hazy Maze Cave - Toxic Maze Near Bats Metal Cap Block": "MC",
            "Hazy Maze Cave - Toxic Maze Near Twin Monty Mole Holes Metal Cap Block": "MC",
            "Jolly Roger Bay - Beginning Metal Cap Block": "MC",
            "Jolly Roger Bay - Ocean Cave Metal Cap Block": "MC",
            "Jolly Roger Bay - Blast to the Stone Pillar Star Block":
                "CANN+CL | logic_jrb_stone_pillar_cannonless | "
                "logic_jrb_stone_pillar_cannon_no_climb",
            "Jolly Roger Bay - Purple Switch Metal Cap Block": "MC",
            "Jolly Roger Bay - Plunder in the Sunken Ship Star Block": "JRB_SUNKEN_SHIP",
            "Lethal Lava Land - Wing Cap Block": "WC",
            "Lethal Lava Land - Koopa Shell Block": "LLL_KOOPA_SHELL",
            "Rainbow Ride - Somewhere Over the Rainbow Star Block": "CANN",
            "Snowman's Land - Inside Igloo 1-Up Block": "VC & TJ/SF/BF/WK/LG | MOVELESS & VC",
            "Snowman's Land - Vanish Cap Block": "VC",
            "Shifting Sand Land - Outside Pyramid Wing Cap Block": "WC",
            "Shifting Sand Land - Stone Structure Wing Cap Block": "WC",
            "Shifting Sand Land - Cannon Wing Cap Block": "WC",
            "Tower of the Wing Cap - Wing Cap Block": "WC",
            "Tick Tock Clock - Midway Up 1-Up Block": "TTC_SPINNERS | LJ+LG",
            "Vanish Cap Under the Moat - Bottom of Slide Vanish Cap Block": "VC",
            "Vanish Cap Under the Moat - 3 Coins Block": "LG/TJ/BF/SF",
            "Vanish Cap Under the Moat - Near Switch Vanish Cap Block":
                "VC & CHECKERBOARD_PLATFORMS & WK/TJ/BF/SF/LG | "
                "VC & CHECKERBOARD_PLATFORMS & MOVELESS",
            "Wet-Dry World - Shocking Arrow Lifts Star Block":
                "{Wet-Dry World - Low Water} | {Wet-Dry World - Mid-High Water} | "
                "{Wet-Dry World - High Water} | {Wet-Dry World - Top} & TJ/LG/LJ",
            "Wet-Dry World - Wooden Structure 3 Coins Block":
                "{Wet-Dry World - Mid Water} | {Wet-Dry World - Top} | PURPLE_SWITCHES & LJ",
            "Wet-Dry World - Downtown Vanish Cap Block": "WDW_WATER_LEVEL_DIAMOND & VC",
            "Wet-Dry World - Metal Cap Block": "MC",
            "Wet-Dry World - Quick Race Through Downtown Star Vanish Cap Block": "WDW_WATER_LEVEL_DIAMOND & VC",
            "Wet-Dry World - Downtown 1-Up Block": "WDW_WATER_LEVEL_DIAMOND",
            "Whomp's Fortress - Metal Cap Block": "MC",
            "Wing Mario Over the Rainbow - Highest Cloud Wing Cap Block": "WC",
            "Wing Mario Over the Rainbow - Cloud Across From Starting Cloud Wing Cap Block":
                wmotr_flight_rule,
            "Wing Mario Over the Rainbow - Starting Cloud Wing Cap Block": "WC",
            "Wing Mario Over the Rainbow - Lowest Cloud Wing Cap Block": "WC+TJ | WC+MOVELESS | WC+LJ+CAPLESS",
            "Wing Mario Over the Rainbow - Bob-omb Buddy Platform Wing Cap Block": "WC",
            "Wing Mario Over the Rainbow - Overlooking Bob-omb Buddy Cloud Wing Cap Block": wmotr_flight_rule,
        }
        for location_name, rule in blocksanity_rules.items():
            rf.assign_rule(location_name, rule)
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
        "The Princess's Secret Slide": princess_secret_slide_coins,
        "The Secret Aquarium": secret_aquarium_coins,
        "Wing Mario Over the Rainbow": wing_mario_over_the_rainbow_coins,
        "Tower of the Wing Cap": tower_of_the_wing_cap_coins,
        "Vanish Cap Under the Moat": vanish_cap_under_the_moat_coins,
        "Cavern of the Metal Cap": cavern_of_the_metal_cap_coins,
        "Bowser in the Dark World": bowser_in_the_dark_world_coins,
        "Bowser in the Fire Sea": bowser_in_the_fire_sea_coins,
        "Bowser in the Sky": bowser_in_the_sky_coins,
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
             lambda state: state.can_reach("Basement", 'Region', player) and state.has("Castle - Toads", player))
    add_rule(multiworld.get_location("Castle - Toad (Second Floor)", player),
             lambda state: state.can_reach("Second Floor", 'Region', player) and state.has("Castle - Toads", player))
    add_rule(multiworld.get_location("Castle - Toad (Third Floor)", player),
             lambda state: state.can_reach("Third Floor", 'Region', player) and state.has("Castle - Toads", player))
    add_rule(multiworld.get_location("Castle - Yoshi", player),
             lambda state: state.has("Castle - Yoshi", player))

    rf.assign_rule("Castle - Third Tree From Waterfall 1-Up",
                   "CL/TJ/BF/SF | logic_castle_waterfall_tree_1up_with_no_movement")
    rf.assign_rule("Castle - Bridge Coins 1-Up", "{{Castle - Drain the Moat}} & WK & TJ/SF")
    rf.assign_rule("Castle - Jolly Roger Bay Lobby 1-Up",
                   "SF/BF | TJ & LG | logic_secret_aquarium_triple_jump | "
                   "logic_secret_aquarium_wall_kick_and_ledge_grab | "
                   "logic_secret_aquarium_wall_kick | logic_secret_aquarium_ledge_grab")
    rf.assign_rule("Castle - Drain the Moat", "GP")
    rf.assign_rule("Castle - MIPS 1", "DV | logic_castle_mips_without_dive")
    rf.assign_rule("Castle - MIPS 2", "DV | logic_castle_mips_without_dive")
    add_rule(multiworld.get_location("Castle - MIPS 1", player),
             lambda state: state.can_reach("Basement", 'Region', player) and state.has("Castle - Progressive MIPS", player))
    add_rule(multiworld.get_location("Castle - MIPS 2", player),
             lambda state: state.can_reach("Basement", 'Region', player) and
             state.has("Castle - Progressive MIPS", player, 2))

    if options.area_rando > options.area_rando.option_Off and not using_slot_area_connections:
        ensure_reachable_starting_check(
            multiworld, options, player, randomized_entrances, randomized_entrances_s,
            randomized_entrance_connections)

    # Destination Format: LVL | AREA with LVL = LEVEL_x, AREA = Area as used in sm64 code
    # Cast to int to not rely on availability of SM64Levels enum. Will cause crash in MultiServer otherwise
    area_connections.update({int(entrance_lvl): int(sm64_entrances_to_level[destination])
                             for (entrance_lvl, destination) in randomized_entrances.items()})

    can_defeat_bowser_in_the_sky = lambda state: (
        state.can_reach("Bowser in the Sky - Top", 'Region', player)
        and has_bowser_arena_bombs(state, "Bowser in the Sky", options.bowser_in_the_sky_hits.value)
    )
    multiworld.completion_condition[player] = can_defeat_bowser_in_the_sky

    if options.completion_type == options.completion_type.option_Last_Bowser_Stage:
        multiworld.completion_condition[player] = can_defeat_bowser_in_the_sky
    elif options.completion_type == options.completion_type.option_All_Bowser_Stages:
        multiworld.completion_condition[player] = lambda state: (
            state.can_reach("Bowser in the Dark World - Key", 'Location', player)
            and state.can_reach("Bowser in the Fire Sea - Key", 'Location', player)
            and can_defeat_bowser_in_the_sky(state)
        )


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
        "MIPS1": "Castle - Progressive MIPS",
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
        "Wing Mario Over the Rainbow": "Wing Mario Over the Rainbow - Cannon Unlock",
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
        if target_name in locOneUp_table and not self.options.one_up_checks:
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
            for region_name in self.get_indirect_condition_region_names(rule_expr):
                self.multiworld.register_indirect_condition(
                    self.multiworld.get_region(region_name, self.player), target)

    def get_indirect_condition_region_names(
            self, rule_expr: str, seen_tricks: set[str] | None = None) -> set[str]:
        region_names = set(re.findall(r"(?<!\{)\{([^{}]+)\}(?!\})", rule_expr))
        seen_tricks = set() if seen_tricks is None else seen_tricks
        for trick_name in re.findall(r"\blogic_[a-z0-9_]+\b", rule_expr):
            if trick_name in logic_tricks_by_name and trick_name not in seen_tricks:
                seen_tricks.add(trick_name)
                region_names.update(self.get_indirect_condition_region_names(
                    logic_tricks_by_name[trick_name].get("rule", ""), seen_tricks))
        return region_names

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
        if expressions:
            return lambda state: False
        return base_rule

    def build_star_painting_entry_requirements(self, painting_lvl_name: str = None, star_num_req: int = None) -> Callable:
        nop_condition = lambda state: True
        star_rule = nop_condition
        painting_rule = nop_condition
        if painting_lvl_name is not None and self.painting_randomizer:
            painting_item_name = f"Unlock {painting_lvl_name}"
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
        return self.cannon_item_name_by_level.get(level_name, f"{level_name} - Cannon Unlock")

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
        item_names["SINGLE_YELLOW_COINS"] = get_unlock_item_name(
            self.options, "coin_object_unlocks",
            "Single Yellow Coins", f"{level_name} - Single Yellow Coins")
        item_names["VERTICAL_COIN_RINGS"] = get_unlock_item_name(
            self.options, "coin_object_unlocks",
            "Vertical Coin Rings", f"{level_name} - Vertical Coin Rings")
        item_names["RED_COINS"] = get_unlock_item_name(
            self.options, "coin_object_unlocks",
            "Red Coins", f"{level_name} - Red Coins")
        item_names["WOODEN_POSTS"] = get_unlock_item_name(
            self.options, "coin_object_unlocks",
            "Wooden Posts", f"{level_name} - Wooden Posts")
        item_names["BOBOMBS"] = get_unlock_item_name(
            self.options, "enemy_unlocks",
            "Bob-ombs", f"{level_name} - Bob-ombs")
        item_names["KOOPA_TROOPA"] = get_unlock_item_name(
            self.options, "enemy_unlocks",
            "Koopa Troopas", f"{level_name} - Koopa Troopa")
        item_names["WHOMPS"] = get_unlock_item_name(
            self.options, "enemy_unlocks",
            "Whomps", f"{level_name} - Whomps")
        item_names["SPINDRIFTS"] = get_unlock_item_name(
            self.options, "enemy_unlocks",
            "Spindrifts", f"{level_name} - Spindrifts")
        item_names["FLY_GUY"] = get_unlock_item_name(
            self.options, "enemy_unlocks",
            "Fly Guys", f"{level_name} - Fly Guy")
        item_names["EYEROK"] = get_unlock_item_name(
            self.options, "enemy_unlocks",
            "Shifting Sand Land - Eyerok", "Shifting Sand Land - Eyerok")
        item_names["BIG_BOO"] = get_unlock_item_name(
            self.options, "enemy_unlocks",
            "Big Boo's Haunt - Big Boo", "Big Boo's Haunt - Big Boo")
        item_names["THWOMP"] = get_unlock_item_name(
            self.options, "enemy_unlocks",
            "Thwomp", f"{level_name} - Thwomp")
        item_names["BOOS"] = get_unlock_item_name(
            self.options, "enemy_unlocks",
            "Boos", f"{level_name} - Boos")
        item_names["MR_IS"] = get_unlock_item_name(
            self.options, "enemy_unlocks",
            "Mr. Is", f"{level_name} - Mr. Is")
        item_names["FLYING_BOOKENDS"] = get_unlock_item_name(
            self.options, "enemy_unlocks",
            f"{level_name} - Flying Bookends", f"{level_name} - Flying Bookends")
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
        if expression in logic_tricks_by_name:
            world = self.multiworld.worlds[self.player]
            enabled = getattr(world, expression, False)
            enabled_for_ut = getattr(world, f"{expression}_ut_glitch", False)
            if not enabled and not enabled_for_ut:
                return False
            trick_rule = self.build_rule(
                logic_tricks_by_name[expression].get("rule", ""),
                cannon_name, cap_item_names, arbitrary_item_names, action_item_names)
            if enabled:
                return trick_rule
            return lambda state: state.has(ut_glitch_item_name, self.player) and trick_rule(state)
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
