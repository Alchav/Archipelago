import re
from typing import Union

from BaseClasses import CollectionState, DEFAULT_COLLECTION_RULE, Entrance, MultiWorld
from rule_builder.rules import And, CanReachLocation, CanReachRegion, False_, Has, HasAll, HasAny, \
    Or, Rule, True_
from .Locations import SM64Location, locOneUp_table, location_table, one_up_unlock_category_by_location, \
    parse_coin_count_check_location_name, parse_global_coin_count_check_location_name, global_coin_count_course_data
from .CoinChecks import coin_output_by_name
from .Options import SM64Options, move_randomizer_option_name_by_action
from .Regions import connect_regions, create_region, SM64Levels, sm64_entrance_to_region, sm64_level_to_paintings, \
    sm64_level_to_secrets, sm64_secrets_to_level, sm64_entrances_to_level, sm64_level_to_entrances, \
    sm64_ttc_entrances, sm64_wdw_entrances
from .Items import action_item_data_table, cap_item_data_table, feature_item_data_table, \
    per_level_move_area_names, ut_glitch_item_name, freestanding_star_item_data_table, \
    star_block_item_data_table, koopa_shell_block_item_data_table, star_secret_item_data_table
from .LogicTricks import logic_tricks
from .RuleBuilder import CanCollectAllRedCoins, CanCollectCoinOutput, CanCollectCoins, CanCollectGlobalCoins, HasUnlock, LogicTrick, \
    register_coin_evaluator
from .CoinLogic import COIN_EVALUATORS, SSL_UPPER_PYRAMID_ENTRANCE_RULE
from .Signs import sign_data, sign_item_name_for_area
from .SubAreas import CASTLE_RETURN_DESTINATIONS, CASTLE_RETURN_SOURCES, RETURN_DESTINATIONS, RETURN_SOURCES, \
    SUB_AREA_DESTINATIONS, SUB_AREA_SOURCES, build_mixed_connections, build_separate_connections, \
    destination_slot_data, normal_source_id, pack_warp_destination, SUB_AREA_SOURCE_NAMES


logic_tricks_by_internal_id = {
    data["internal_id"]: (option_key, data)
    for option_key, data in logic_tricks.items()
}


initial_reachable_entrances = (
    "Bob-omb Battlefield",
    "Whomp's Fortress",
    "Jolly Roger Bay",
    "Cool, Cool Mountain",
    "The Princess's Secret Slide",
)
simple_level_feature_items = {
    "HMC_SWIMMING_BEAST": "Hazy Maze Cave - Swimming Beast",
    "RR_CARPETS": "Rainbow Ride - Carpets",
    "CCM_BABY_PENGUINS": "Cool, Cool Mountain - Baby Penguins",
    "SL_PENGUIN": "Snowman's Land - Penguin",
    "SSL_PYRAMID_ELEVATOR": "Shifting Sand Land - Pyramid Elevator",
    "WDW_WATER_LEVEL_DIAMOND": "Wet-Dry World - Water Level Diamond",
    "TTC_SPINNERS": "Tick Tock Clock - Spinners",
}

warp_pipe_item_name_by_level = {
    "Tiny-Huge Island": "Tiny-Huge Island - Warp Pipes",
    "Bowser in the Dark World": "Bowser in the Dark World - Warp Pipe",
    "Bowser in the Sky": "Bowser in the Sky - Warp Pipe",
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

bobomb_buddy_item_name_by_level = {
    level_name: f"{level_name} - Bob-omb Buddy"
    for level_name in (
        "Bob-omb Battlefield",
        "Whomp's Fortress",
        "Jolly Roger Bay",
        "Cool, Cool Mountain",
        "Shifting Sand Land",
        "Snowman's Land",
        "Wet-Dry World",
        "Tall, Tall Mountain",
        "Tiny-Huge Island",
        "Rainbow Ride",
        "Wing Mario Over the Rainbow",
    )
}

treasure_chest_item_name_by_level = {
    "Jolly Roger Bay": "Jolly Roger Bay - Treasure Chests",
    "Dire, Dire Docks": "Dire, Dire Docks - Treasure Chests",
}

per_act_feature_tokens = {
    "BOB_KING",
    "BOB_KOOPA",
    "BOB_BUDDY",
    "WF_KING",
    "WF_FORTRESS",
    "WF_BUDDY",
    "WF_HOOT",
    "CCM_SNOWMAN_BODY",
    "CCM_BIG_PENGUIN",
    "JRB_SUNKEN_SHIP",
    "JRB_RAISED_SHIP",
    "JRB_BUDDY",
    "JRB_JET_STREAM",
    "JRB_UNAGI",
    "LLL_KOOPA_SHELL",
    "SSL_KLEPTO",
    "THI_KOOPA",
    "TTM_UKIKI",
    "DDD_MANTA_RAY",
    "DDD_BOWSER_SUB",
    "DDD_POLES",
    "BBH_STAIRCASE",
    "BBH_MERRY_GO_ROUND",
}


move_area_name_aliases = {
    "Castle Grounds": "Castle",
    "Castle First Floor": "Castle",
    "Castle Courtyard": "Castle",
    "Castle Basement": "Castle",
    "Castle Second Floor": "Castle",
    "Castle Third Floor": "Castle",
    "The Princess's Secret Slide": "Castle",
    "The Secret Aquarium": "Castle",
}


misc_move_area_names = {
    "Castle",
    "Bowser in the Dark World",
    "Bowser in the Fire Sea",
    "Bowser in the Sky",
    "Vanish Cap Under the Moat",
    "Cavern of the Metal Cap",
    "Tower of the Wing Cap",
    "Wing Mario Over the Rainbow",
}


def get_move_area_name(level_name: str, combined_castle_and_secret_stage_move_items: bool = True) -> str:
    move_area_name = move_area_name_aliases.get(level_name, level_name)
    if combined_castle_and_secret_stage_move_items and move_area_name in misc_move_area_names:
        return "Misc"
    return move_area_name


def get_per_level_action_item_name(
        level_name: str, action: str, combined_castle_and_secret_stage_move_items: bool = True) -> str | None:
    move_area_name = get_move_area_name(level_name, combined_castle_and_secret_stage_move_items)
    if move_area_name not in per_level_move_area_names:
        return None
    return f"{move_area_name} - {action}"


def get_compatible_per_level_action_item_names(level_name: str, action: str) -> tuple[str, ...]:
    exact_item_name = get_per_level_action_item_name(level_name, action, False)
    if exact_item_name is None:
        return ()
    if get_move_area_name(level_name, False) in misc_move_area_names:
        return exact_item_name, f"Misc - {action}"
    return (exact_item_name,)


def has_action(state: CollectionState, player: int, action: str, level_name: str = "Castle") -> bool:
    option_name = move_randomizer_option_name_by_action.get(action)
    if option_name is None:
        return True
    options = state.multiworld.worlds[player].options
    option = getattr(options, option_name)
    if option.value == option.option_not_shuffled:
        return True
    per_level_item_names = get_compatible_per_level_action_item_names(level_name, action)
    if not per_level_item_names:
        return state.has(action, player)
    return state.has(action, player) or any(state.has(item_name, player) for item_name in per_level_item_names)


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
    ).resolve(world)(state)


def has_metal_cap(state: CollectionState, player: int, level_name: str) -> bool:
    return state.has("Metal Cap", player) or state.has(f"{level_name} - Metal Cap", player)


def has_simple_arbitrary_feature(state: CollectionState, player: int, token: str) -> bool:
    item_name = simple_level_feature_items[token]
    return has_unlock(state, player, "level_features", item_name, item_name)


def has_warp_pipes(state: CollectionState, player: int, level_name: str) -> bool:
    return has_level_feature(
        state, player, "level_features", "Warp Pipes", warp_pipe_item_name_by_level[level_name])


def get_level_feature_item_name(
        option, global_item_name: str | None, per_level_item_name: str) -> HasUnlock:
    return HasUnlock(global_item_name or per_level_item_name, per_level_item_name)


def has_level_feature(
        state: CollectionState, player: int, option_name: str,
        global_item_name: str | None, per_level_item_name: str) -> bool:
    return has_unlock(
        state, player, option_name, global_item_name or per_level_item_name, per_level_item_name)


def has_per_act_feature(
        state: CollectionState, player: int, per_level_item_name: str) -> bool:
    return has_unlock(state, player, "level_features", per_level_item_name, per_level_item_name)


def has_purple_switches(state: CollectionState, player: int, level_name: str) -> bool:
    item_name = purple_switch_item_name_by_level.get(level_name)
    return item_name is None or has_level_feature(
        state, player, "level_features", "Purple Switches", item_name)


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
    item_name = checkerboard_item_name_by_level.get(level_name)
    return item_name is None or has_level_feature(
        state, player, "level_features", "Checkerboard Platforms", item_name)


def get_unlock_item_name(options, option_name: str, global_item_name: str, per_level_item_name: str) -> HasUnlock:
    return HasUnlock(global_item_name, per_level_item_name)


def has_unlock(
        state: CollectionState, player: int, option_name: str,
        global_item_name: str, per_level_item_name: str) -> bool:
    world = state.multiworld.worlds[player]
    item_names = {
        item_name for item_name in (global_item_name, per_level_item_name)
        if item_name in world.item_name_to_id
    }
    return (
        any(state.has(item_name, player) for item_name in item_names)
        or any(world.item_name_to_id[item_name] in world.start_inventory_item_ids for item_name in item_names)
    )


def has_wing_cap(state: CollectionState, player: int, level_name: str) -> bool:
    return state.has("Wing Cap", player) or state.has(f"{level_name} - Wing Cap", player)


def has_vanish_cap(state: CollectionState, player: int, level_name: str) -> bool:
    return state.has("Vanish Cap", player) or state.has(f"{level_name} - Vanish Cap", player)


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
        has_level_feature(
            state, player, "level_features", "Koopa Shell Blocks", "Lethal Lava Land - Koopa Shell")
        or can_use_logic_trick(state, player, "logic_lava_damage_boosting", target_name)
    )
    return has_lava_crossing and has_lethal_lava_land_healing_coins(state, player)


def can_reach_lethal_lava_land_red_coins(
        state: CollectionState, player: int, target_name: str) -> bool:
    return (
        has_unlock(
            state, player, "coin_object_unlocks",
            "Lethal Lava Land - Bowser Puzzle", "Lethal Lava Land - Bowser Puzzle")
        or has_level_feature(
            state, player, "level_features", "Koopa Shell Blocks", "Lethal Lava Land - Koopa Shell")
        or can_use_logic_trick(state, player, "logic_lava_damage_boosting", target_name)
    )


def shuffle_dict_keys(multiworld: MultiWorld, dictionary: dict) -> dict:
    keys = list(dictionary.keys())
    values = list(dictionary.values())
    multiworld.random.shuffle(keys)
    return dict(zip(keys, values))

def is_starting_check_location(location_name: str, options: SM64Options) -> bool:
    if not options.one_up_checks and location_name in locOneUp_table:
        return False
    if not options.buddy_checks and location_name.endswith(" - Bob-omb Buddy"):
        return False
    return True


def set_rules(multiworld: MultiWorld, options: SM64Options, player: int, area_connections: dict, move_rando_bitvec: int):
    world = multiworld.worlds[player]
    sub_area_mode = options.sub_area_shuffle.value
    castle_return_mode = options.castle_return_shuffle.value
    using_slot_area_connections = bool(area_connections)
    if using_slot_area_connections:
        randomized_entrances = {
            int(entrance_lvl): sm64_level_to_entrances[int(destination_lvl)]
            for entrance_lvl, destination_lvl in area_connections.items()
            if isinstance(entrance_lvl, int) and isinstance(destination_lvl, int)
        }
    else:
        randomized_level_to_paintings = sm64_level_to_paintings.copy()
        randomized_level_to_secrets = sm64_level_to_secrets.copy()

        if options.main_course_shuffle.value == options.main_course_shuffle.option_separate:
            randomized_level_to_paintings = shuffle_dict_keys(multiworld, sm64_level_to_paintings)
        if options.secret_course_shuffle.value == options.secret_course_shuffle.option_separate:
            randomized_level_to_secrets = shuffle_dict_keys(multiworld, randomized_level_to_secrets)
        randomized_entrances = {**randomized_level_to_paintings, **randomized_level_to_secrets}

    randomized_entrances_s = {sm64_level_to_entrances[entrance_lvl]: destination for (entrance_lvl,destination) in randomized_entrances.items()}
    randomized_entrance_connections = {}
    normal_destination_ids = {
        name: int(entrance_id)
        for entrance_id, name in sm64_level_to_entrances.items()
    }
    normal_destination_ids["Bowser in the Sky"] = int(SM64Levels.BOWSER_IN_THE_SKY)
    normal_source_ids = {
        entrance_id: normal_source_id(entrance_id)
        for entrance_id in normal_destination_ids.values()
    }
    world.shuffled_entrance_source_ids = world.get_shuffled_entrance_source_ids()

    def packed_normal_destination(entrance_id: int) -> int:
        level = entrance_id // 10
        variant = entrance_id % 10
        area = variant if level == 13 else 1
        entrance_variant = variant if level in {11, 14} else 0
        return pack_warp_destination(level, area, 0x0A, entrance_variant)

    normal_destination_slot_data = {
        entrance_id: packed_normal_destination(entrance_id)
        for entrance_id in normal_destination_ids.values()
    }

    if not using_slot_area_connections:
        mixed_normal_ids = []
        if options.main_course_shuffle.value == options.main_course_shuffle.option_mixed:
            mixed_normal_ids.extend(int(entrance_id) for entrance_id in sm64_level_to_paintings)
        if options.secret_course_shuffle.value == options.secret_course_shuffle.option_mixed:
            mixed_normal_ids.extend(int(entrance_id) for entrance_id in sm64_level_to_secrets)
        include_mixed_sub_areas = sub_area_mode in {
            options.sub_area_shuffle.option_mixed,
            options.sub_area_shuffle.option_mixed_decoupled,
        }
        include_mixed_castle_returns = (
            castle_return_mode == options.castle_return_shuffle.option_mixed)
        if mixed_normal_ids or include_mixed_sub_areas or include_mixed_castle_returns:
            mixed_names = {
                sm64_level_to_entrances[entrance_id]: entrance_id
                for entrance_id in mixed_normal_ids
            }
            if int(SM64Levels.BOWSER_IN_THE_SKY) in mixed_normal_ids:
                mixed_names["Bowser in the Sky"] = int(SM64Levels.BOWSER_IN_THE_SKY)
            mixed_connections = build_mixed_connections(
                world.random,
                {f"normal:{name}": source_id for name, source_id in mixed_names.items()},
                tuple(mixed_names),
                include_mixed_castle_returns,
                include_mixed_sub_areas,
                decoupled=sub_area_mode == options.sub_area_shuffle.option_mixed_decoupled,
                allow_castle_return_bits_branch=(
                    options.main_course_shuffle.value == options.main_course_shuffle.option_mixed
                    and sub_area_mode == options.sub_area_shuffle.option_mixed
                    and include_mixed_castle_returns
                ),
            )
            area_connections.update({
                mixed_names[source.removeprefix("normal:")]
                if source.startswith("normal:") else source:
                mixed_names.get(destination, destination)
                for source, destination in mixed_connections.items()
            })

            # These physical entrance/destination pairs cannot work. Swap only
            # ordinary mixed roots so the forced Bowser in the Sky branch and
            # the sub-area graph remain intact.
            protected_sources = {
                int(SM64Levels.BOWSER_IN_THE_SKY),
                int(SM64Levels.BOWSER_IN_THE_FIRE_SEA),
                int(SM64Levels.CAVERN_OF_THE_METAL_CAP),
            }

            def fix_invalid_mixed_destination(source_id: int, invalid_destinations: set[int]):
                if area_connections.get(source_id) not in invalid_destinations:
                    return
                replacements = [
                    candidate for candidate, destination in area_connections.items()
                    if isinstance(candidate, int)
                    and candidate not in protected_sources
                    and destination not in invalid_destinations
                ]
                replacement = world.random.choice(replacements)
                area_connections[source_id], area_connections[replacement] = (
                    area_connections[replacement], area_connections[source_id])

            fix_invalid_mixed_destination(
                int(SM64Levels.BOWSER_IN_THE_FIRE_SEA),
                {int(SM64Levels.DIRE_DIRE_DOCKS)},
            )
            cotmc_invalid_destinations = {int(SM64Levels.HAZY_MAZE_CAVE)}
            if area_connections.get(int(SM64Levels.BOWSER_IN_THE_FIRE_SEA)) \
                    == int(SM64Levels.HAZY_MAZE_CAVE):
                cotmc_invalid_destinations.add(int(SM64Levels.DIRE_DIRE_DOCKS))
            fix_invalid_mixed_destination(
                int(SM64Levels.CAVERN_OF_THE_METAL_CAP),
                cotmc_invalid_destinations,
            )

        if sub_area_mode == options.sub_area_shuffle.option_separate:
            area_connections.update(build_separate_connections(world.random))

    if sub_area_mode != options.sub_area_shuffle.option_vanilla \
            or castle_return_mode == options.castle_return_shuffle.option_mixed:
        source_ids = {
            **normal_source_ids,
        }
        if sub_area_mode != options.sub_area_shuffle.option_vanilla:
            source_ids.update({key: source.source_id for key, source in SUB_AREA_SOURCES.items()})
            source_ids.update({key: source.source_id for key, source in RETURN_SOURCES.items()})
        if castle_return_mode == options.castle_return_shuffle.option_mixed:
            source_ids.update({key: source.source_id for key, source in CASTLE_RETURN_SOURCES.items()})
        world.sub_area_slot_data = {
            source_ids[source_key]: destination_slot_data(destination_key, normal_destination_slot_data)
            for source_key, destination_key in area_connections.items()
            if source_key in source_ids
        }

    def sub_area_target_region(destination_key: int | str) -> str:
        if isinstance(destination_key, int):
            if destination_key == int(SM64Levels.BOWSER_IN_THE_SKY):
                return "Bowser in the Sky"
            return sm64_entrance_to_region[sm64_level_to_entrances[destination_key]]
        for table in (SUB_AREA_DESTINATIONS, RETURN_DESTINATIONS, CASTLE_RETURN_DESTINATIONS):
            destination = table.get(destination_key)
            if destination is not None:
                return destination.region
        raise KeyError(destination_key)
    defer_randomized_entrances = (
        bool(getattr(multiworld, "generation_is_fake", False))
        and getattr(multiworld, "enforce_deferred_connections", "default") != "off"
        and bool(world.shuffled_entrance_source_ids)
    )

    rf = RuleFactory(multiworld, options, player, move_rando_bitvec)

    if defer_randomized_entrances:
        create_region("Bypassing Logic", player, multiworld)
        connect_regions(
            multiworld, player, world.origin_region_name, "Bypassing Logic", Has(ut_glitch_item_name))

    def connect_randomized_entrance(source: str, source_entrance: str, rule=None):
        entrance_id = int(sm64_entrances_to_level[source_entrance])
        if entrance_id in area_connections:
            destination_entrance = area_connections[entrance_id]
            target_region = (
                sub_area_target_region(destination_entrance)
                if not isinstance(destination_entrance, int)
                else sm64_entrance_to_region[sm64_level_to_entrances[destination_entrance]]
            )
        else:
            destination_entrance = randomized_entrances_s[source_entrance]
            target_region = sm64_entrance_to_region[destination_entrance]
        entrance = connect_regions(
            multiworld, player, source, target_region, rule,
            name=f"{source} -> {source_entrance}"
        )
        randomized_entrance_connections[source_entrance] = entrance
        world.randomized_entrance_connections[entrance_id] = entrance
        return entrance

    first_floor_key_rule = Has("Dark World Key") | Has("Progressive Key")
    basement_key_rule = (
        Has("Basement Key") | Has("Progressive Basement Key") | Has("Progressive Key", 2)
    )
    thirty_star_key_rule = Has("Progressive Basement Key", 2) | Has("Progressive Key", 3)
    second_floor_key_rule = (
        Has("Second Floor Key") | Has("Progressive Upstairs Key") | Has("Progressive Key", 4)
    )
    third_floor_key_rule = Has("Progressive Upstairs Key", 2) | Has("Progressive Key", 5)
    endless_stairs_key_rule = Has("Progressive Upstairs Key", 3) | Has("Progressive Key", 6)
    thirty_star_door_bypass_rule = thirty_star_key_rule | rf.build_rule(
        "logic_castle_30_star_door_sblj | logic_castle_30_star_door_crackslide | "
        "logic_castle_30_star_door_crackslide_double_jump | "
        "logic_castle_30_star_door_crackslide_yolo | logic_castle_30_star_door_mips_skip"
    )
    fifty_star_door_bypass_rule = third_floor_key_rule | rf.build_rule("logic_castle_50_star_door_blj")
    seventy_star_door_bypass_rule = endless_stairs_key_rule | rf.build_rule("logic_castle_70_star_door_blj")

    def bowser_stage_one_up_rule(stage_item_name: str, vanilla_key_rule: Rule) -> Rule:
        option = options.bowser_stage_1ups
        if option.value == option.option_vanilla:
            return vanilla_key_rule
        return HasUnlock("Bowser Stage Extra 1-Ups", stage_item_name)

    def bowser_arena_bomb_rule(stage_name: str, required_hits: int) -> Rule:
        required_bombs = []
        for bomb in range(1, required_hits + 1):
            stage_item_name = f"{stage_name} - Bowser Arena Bomb {bomb}"
            if bomb == 5:
                required_bombs.append(HasUnlock(stage_item_name, stage_item_name))
            else:
                global_item_name = f"Bowser Arena Bomb {bomb}"
                required_bombs.append(
                    HasUnlock(global_item_name, global_item_name)
                    | HasUnlock(stage_item_name, stage_item_name))
        return And(*required_bombs)

    def level_unlock_rule(item_name: str) -> Rule:
        return HasUnlock(item_name, item_name)

    def full_level_unlock_rule(item_name: str) -> Rule:
        return HasUnlock(item_name, item_name)

    connect_regions(multiworld, player, "Castle Grounds", "Castle First Floor")
    connect_regions(multiworld, player, "Castle First Floor", "Castle Courtyard")
    connect_randomized_entrance(
        "Castle First Floor", "Bob-omb Battlefield", level_unlock_rule("Unlock Bob-omb Battlefield"))
    connect_randomized_entrance("Castle First Floor", "Whomp's Fortress",
                                rf.build_rule("", painting_lvl_name="Whomp's Fortress"))
    connect_randomized_entrance("Castle First Floor", "Jolly Roger Bay",
                                rf.build_rule("", painting_lvl_name="Jolly Roger Bay"))
    connect_randomized_entrance("Castle First Floor", "Cool, Cool Mountain",
                                rf.build_rule("", painting_lvl_name="Cool, Cool Mountain"))
    connect_randomized_entrance("Castle Courtyard", "Big Boo's Haunt",
                                level_unlock_rule("Unlock Big Boo's Haunt"))
    connect_randomized_entrance(
        "Castle First Floor", "The Princess's Secret Slide",
        level_unlock_rule("Unlock The Princess's Secret Slide"))
    connect_randomized_entrance("Castle First Floor", "The Secret Aquarium",
                                level_unlock_rule("Unlock The Secret Aquarium") & rf.build_rule(
                                    "SF/BF | TJ & LG | logic_secret_aquarium_triple_jump | "
                                    "logic_secret_aquarium_wall_kick_and_ledge_grab | "
                                    "logic_secret_aquarium_wall_kick | logic_secret_aquarium_ledge_grab"))
    connect_randomized_entrance("Castle First Floor", "Tower of the Wing Cap",
                                level_unlock_rule("Unlock Tower of the Wing Cap"))
    connect_randomized_entrance(
        "Castle First Floor", "Bowser in the Dark World",
        first_floor_key_rule | rf.build_rule("logic_castle_lobby_8_star_door_blj"))

    connect_regions(multiworld, player, "Castle First Floor", "Castle Basement", basement_key_rule)

    connect_randomized_entrance("Castle Basement", "Hazy Maze Cave",
                                rf.build_rule("", painting_lvl_name="Hazy Maze Cave"))
    connect_randomized_entrance("Castle Basement", "Lethal Lava Land",
                                rf.build_rule("", painting_lvl_name="Lethal Lava Land"))
    connect_randomized_entrance("Castle Basement", "Shifting Sand Land",
                                rf.build_rule("", painting_lvl_name="Shifting Sand Land"))
    ddd_entry_rule = rf.build_rule("", painting_lvl_name="Dire, Dire Docks")
    connect_randomized_entrance("Castle Basement", "Dire, Dire Docks",
                                thirty_star_door_bypass_rule & ddd_entry_rule)
    connect_randomized_entrance(
        "Hazy Maze Cave", "Cavern of the Metal Cap",
        level_unlock_rule("Unlock Cavern of the Metal Cap")
        & rf.build_rule(
            "HMC_SWIMMING_BEAST | logic_hmc_elevator_clip",
            arbitrary_item_names=rf.get_arbitrary_item_names("Hazy Maze Cave"),
            action_item_names=rf.get_action_item_names("Hazy Maze Cave")))
    connect_randomized_entrance("Castle Grounds", "Vanish Cap Under the Moat",
                                level_unlock_rule("Unlock Vanish Cap Under the Moat"))
    connect_randomized_entrance("Castle Basement", "Bowser in the Fire Sea",
                                thirty_star_door_bypass_rule & level_unlock_rule("Unlock Bowser in the Fire Sea"))

    connect_regions(multiworld, player, "Castle First Floor", "Castle Second Floor", second_floor_key_rule)

    connect_randomized_entrance("Castle Second Floor", "Snowman's Land",
                                rf.build_rule("", painting_lvl_name="Snowman's Land"))
    for wdw_entrance in sm64_wdw_entrances:
        wdw_entrance_rule = "TJ/SF/BF" if wdw_entrance == "Wet-Dry World High" else ""
        connect_randomized_entrance("Castle Second Floor", wdw_entrance,
                                    rf.build_rule(wdw_entrance_rule, painting_lvl_name="Wet-Dry World"))
    connect_randomized_entrance("Castle Second Floor", "Tall, Tall Mountain",
                                rf.build_rule("", painting_lvl_name="Tall, Tall Mountain"))
    connect_randomized_entrance("Castle Second Floor", "Tiny-Huge Island (Tiny)",
                                rf.build_rule("", painting_lvl_name="Tiny Island"))
    connect_randomized_entrance("Castle Second Floor", "Tiny-Huge Island (Huge)",
                                rf.build_rule("", painting_lvl_name="Huge Island"))

    connect_regions(multiworld, player, "Castle Second Floor", "Castle Third Floor", fifty_star_door_bypass_rule)

    ttc_entrance_rule = rf.build_rule(
        "LG/TJ/SF/BF | logic_castle_ttc_with_wall_kick | "
        "logic_castle_ttc_with_long_jump_and_kick | logic_castle_ttc_with_dive_and_kick",
        painting_lvl_name="Tick Tock Clock")
    for ttc_entrance in sm64_ttc_entrances:
        connect_randomized_entrance("Castle Third Floor", ttc_entrance, ttc_entrance_rule)
    third_floor_alcove_rule = rf.build_rule(
        "TJ/SF/BF | logic_castle_3f_alcoves_with_wall_kick | "
        "logic_castle_3f_alcoves_with_dive_and_kick | "
        "logic_castle_3f_alcoves_with_dive_and_ledge_grab | "
        "logic_castle_3f_alcoves_with_long_jump_and_ledge_grab")
    connect_randomized_entrance(
        "Castle Third Floor", "Rainbow Ride",
        third_floor_alcove_rule & full_level_unlock_rule("Unlock Rainbow Ride"))
    connect_randomized_entrance("Castle Third Floor", "Wing Mario Over the Rainbow",
                                third_floor_alcove_rule
                                & full_level_unlock_rule("Unlock Wing Mario Over the Rainbow"))
    if int(SM64Levels.BOWSER_IN_THE_SKY) in area_connections:
        bits_target_region = sub_area_target_region(area_connections[int(SM64Levels.BOWSER_IN_THE_SKY)])
    elif options.secret_course_shuffle.value != options.secret_course_shuffle.option_vanilla:
        bits_target_region = sm64_entrance_to_region[randomized_entrances_s["Bowser in the Sky"]]
    else:
        bits_target_region = None
    if bits_target_region is not None:
        bits_entrance = connect_regions(
            multiworld, player, "Castle Third Floor",
            bits_target_region,
            seventy_star_door_bypass_rule,
            name="Castle Third Floor -> Bowser in the Sky",
        )
        world.randomized_entrance_connections[int(SM64Levels.BOWSER_IN_THE_SKY)] = bits_entrance
    else:
        connect_regions(
            multiworld, player, "Castle Third Floor", "Bowser in the Sky", seventy_star_door_bypass_rule)

    def connect_sub_area_source(source_key: str, rule: Rule | None = None) -> None:
        source = SUB_AREA_SOURCES[source_key]
        destination_key = area_connections.get(source_key, source.vanilla_destination)
        entrance = connect_regions(
            multiworld, player, source.region, sub_area_target_region(destination_key), rule,
            name=SUB_AREA_SOURCE_NAMES[source_key],
        )
        if sub_area_mode:
            world.randomized_entrance_connections[source.source_id] = entrance

    # Portal approach regions and alternate approaches are independent of the
    # destination assigned to the physical warp.
    connect_regions(
        multiworld, player, "Snowman's Land", "Snowman's Land - Igloo Entrance",
        rf.build_rule(
            "{Snowman's Land - Whirl from the Freezing Pond} & SL_KOOPA_SHELL",
            arbitrary_item_names=rf.get_arbitrary_item_names("Snowman's Land"),
            action_item_names=rf.get_action_item_names("Snowman's Land")),
        name="Snowman's Land - Igloo Approach")
    connect_regions(
        multiworld, player, "Cool, Cool Mountain - Slide Exit", "Cool, Cool Mountain",
        name="Cool, Cool Mountain - Slide Exit to Main Area")
    connect_regions(multiworld, player, "Lethal Lava Land", "Lethal Lava Land - Volcano Entrance")
    ssl_upper_pyramid_entrance_rule = rf.build_rule(
        SSL_UPPER_PYRAMID_ENTRANCE_RULE,
        cannon_name=rf.get_cannon_item_name("Shifting Sand Land"),
        cap_item_names=rf.get_cap_item_names("Shifting Sand Land"),
        arbitrary_item_names=rf.get_arbitrary_item_names("Shifting Sand Land"),
        action_item_names=rf.get_action_item_names("Shifting Sand Land"))
    connect_regions(
        multiworld, player, "Shifting Sand Land",
        "Shifting Sand Land - Upper Pyramid Entrance", ssl_upper_pyramid_entrance_rule)
    connect_regions(
        multiworld, player, "Bowser in the Dark World", "Bowser in the Dark World - Bowser Pipe")

    connect_sub_area_source("ccm_slide")
    connect_sub_area_source("sl_igloo")
    connect_sub_area_source("ttm_slide")
    connect_sub_area_source("thi_red_cave")
    connect_sub_area_source(
        "jrb_ship",
        rf.build_rule(
            "JRB_SUNKEN_SHIP",
            arbitrary_item_names=rf.get_arbitrary_item_names("Jolly Roger Bay")))
    connect_sub_area_source("lll_volcano")
    connect_sub_area_source("ssl_pyramid_side")
    connect_sub_area_source("ssl_pyramid_top")
    connect_sub_area_source(
        "thi_wiggler",
        rf.build_rule(
            "GP & WARP_PIPES",
            arbitrary_item_names=rf.get_arbitrary_item_names("Tiny-Huge Island"),
            action_item_names=rf.get_action_item_names("Tiny-Huge Island")))
    connect_sub_area_source(
        "bitdw_bowser",
        rf.build_rule(
            "WARP_PIPES & PURPLE_SWITCHES | WARP_PIPES & logic_bitdw_purple_switch_bypass",
            arbitrary_item_names=rf.get_arbitrary_item_names("Bowser in the Dark World"),
            action_item_names=rf.get_action_item_names("Bowser in the Dark World")))
    connect_sub_area_source("bitfs_bowser")
    connect_sub_area_source(
        "bits_bowser",
        rf.build_rule(
            "WARP_PIPES", arbitrary_item_names=rf.get_arbitrary_item_names("Bowser in the Sky")))

    if sub_area_mode:
        for source_key, source in RETURN_SOURCES.items():
            destination_key = area_connections[source_key]
            entrance = connect_regions(
                multiworld, player, source.region, sub_area_target_region(destination_key),
                name=SUB_AREA_SOURCE_NAMES[source_key])
            world.randomized_entrance_connections[source.source_id] = entrance

    else:
        for source in RETURN_SOURCES.values():
            connect_regions(
                multiworld, player, source.region,
                sub_area_target_region(source.vanilla_destination),
                name=SUB_AREA_SOURCE_NAMES[source.key])

    if castle_return_mode == options.castle_return_shuffle.option_mixed:
        for source_key, source in CASTLE_RETURN_SOURCES.items():
            destination_key = area_connections[source_key]
            source_rule = HasUnlock("Dire, Dire Docks - Moat Exit", "Dire, Dire Docks - Moat Exit") \
                if source_key == "ddd_fall" else None
            entrance = connect_regions(
                multiworld, player, source.region, sub_area_target_region(destination_key),
                source_rule,
                name=SUB_AREA_SOURCE_NAMES[source_key])
            world.randomized_entrance_connections[source.source_id] = entrance

    # Course Rules
    # Bob-omb Battlefield
    rf.assign_rule("Bob-omb Battlefield - Big Bob-Omb on the Summit", "BOB_KING")
    rf.assign_rule("Bob-omb Battlefield - Footrace with Koopa The Quick", "BOB_KOOPA")
    rf.assign_rule("Bob-omb Battlefield - Island",
                   "CANN | logic_bob_island_without_cannon | logic_bob_island_long_jump | "
                   "logic_bob_island_koopa_shell | logic_bob_island_koopa_shell_wing_cap | "
                   "logic_bob_mario_wings_to_the_sky_without_cannon")
    rf.assign_rule_object(
        "Bob-omb Battlefield - Mario Wings to the Sky",
        rf.build_rule(
            "CANN & WC | logic_bob_mario_wings_capless | "
            "logic_bob_mario_wings_to_the_sky_without_cannon",
            cannon_name=rf.get_cannon_item_name("Bob-omb Battlefield"),
            cap_item_names=rf.get_cap_item_names("Bob-omb Battlefield"),
            arbitrary_item_names=rf.get_arbitrary_item_names("Bob-omb Battlefield"),
            action_item_names=rf.get_action_item_names("Bob-omb Battlefield"))
        & (True_() if options.trigger_sparkles else rf.build_rule(
            "SINGLE_YELLOW_COINS | VERTICAL_COIN_RINGS | logic_bob_mario_wings_without_coin_markers",
            cannon_name=rf.get_cannon_item_name("Bob-omb Battlefield"),
            cap_item_names=rf.get_cap_item_names("Bob-omb Battlefield"),
            arbitrary_item_names=rf.get_arbitrary_item_names("Bob-omb Battlefield"),
            action_item_names=rf.get_action_item_names("Bob-omb Battlefield"))))
    rf.assign_rule(
        "The Princess's Secret Slide - Coin Triggers 1-Up",
        "" if options.trigger_sparkles else
        "HORIZONTAL_COIN_LINES | logic_pss_coin_triggers_1up_without_coin_markers")
    rf.assign_rule("Bob-omb Battlefield - Behind Chain Chomp's Gate",
                   "CHAIN_CHOMP & WOODEN_POSTS & GP | "
                   "CHAIN_CHOMP & logic_bob_chain_chomp_gate_without_ground_pound | "
                   "CHAIN_CHOMP & logic_bob_chain_chomp_gate_with_cork_box")
    rf.assign_rule("Bob-omb Battlefield - Bob-omb Buddy", "BOB_BUDDY")
    rf.assign_rule("Bob-omb Battlefield - Cannon Tree 1-Up", "CL/TJ/BF/SF")
    # Whomp's Fortress
    rf.assign_rule("Whomp's Fortress - To the Top of the Fortress", "WF_FORTRESS")
    rf.assign_rule("Whomp's Fortress - Chip Off Whomp's Block", "WF_KING & GP")
    rf.assign_rule(
        "Whomp's Fortress - Top",
        "CHECKERBOARD_PLATFORMS | WF_HOOT & CL | WK & SF/TJ | CL & DV/LG | "
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
                   "logic_wf_caged_island_top_fortress_long_jump | "
                   "logic_wf_caged_island_cannon")
    rf.assign_rule(
        "Whomp's Fortress - Blast Away the Wall",
        "CANN | logic_wf_blast_away_wall_cannonless_backflip | logic_wf_blast_away_wall_cannonless")
    rf.assign_rule("Whomp's Fortress - Bob-omb Buddy", "WF_BUDDY")
    rf.assign_rule("Whomp's Fortress - Flagpole 1-Up", "CL")
    rf.assign_rule("Whomp's Fortress - Tower Alcove 1-Up", "WF_FORTRESS")
    # Jolly Roger Bay
    rf.assign_rule("Jolly Roger Bay - Plunder in the Sunken Ship", "TREASURE_CHESTS")
    rf.assign_rule("Jolly Roger Bay - Treasure of the Ocean Cave", "TREASURE_CHESTS")
    rf.assign_rule("Jolly Roger Bay - Can the Eel Come Out to Play?", "JRB_UNAGI")
    rf.assign_rule(
        "Jolly Roger Bay - Upper",
        "TJ/BF/SF/WK | logic_jrb_upper_ledge_grab | "
        "logic_jrb_upper_dive_and_kick | logic_jrb_upper_cannon")
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
    rf.assign_rule("Cool, Cool Mountain - Snowman's Lost His Head", "CCM_SNOWMAN_BODY")
    rf.assign_rule("Cool, Cool Mountain - Li'l Penguin Lost", "CCM_BABY_PENGUINS")
    rf.assign_rule("Cool, Cool Mountain - Bob-omb Buddy", "BOBOMB_BUDDY")
    rf.assign_rule(
        "Cool, Cool Mountain - Wall Kicks Will Work",
        "CANN+TJ+WK | logic_ccm_wall_kicks_will_work_spin_jump")
    # Big Boo's Haunt
    rf.assign_rule("Big Boo's Haunt - Go on a Ghost Hunt", "BOOS & BIG_BOO")
    rf.assign_rule(
        "Big Boo's Haunt - Ride Big Boo's Merry-Go-Round",
        "BBH_MERRY_GO_ROUND & BOOS & BIG_BOO")
    rf.assign_rule(
        "Big Boo's Haunt - Second Floor",
        "BBH_STAIRCASE | logic_bbh_second_floor_wall_kick")
    rf.assign_rule(
        "Big Boo's Haunt - Third Floor",
        "WK+LG | logic_bbh_third_floor_wall_kick | logic_bbh_third_floor_side_flip")
    rf.assign_rule("Big Boo's Haunt - Roof", "LJ | logic_bbh_roof_without_long_jump")
    rf.assign_rule("Big Boo's Haunt - Big Boo's Balcony", "BIG_BOO")
    rf.assign_rule("Big Boo's Haunt - Eye to Eye in the Secret Room", "VC & MR_IS")
    rf.assign_rule("Big Boo's Haunt - Shed Roof 1-Up", "TJ & BREAKABLE_COIN_BOXES")
    # Haze Maze Cave
    rf.assign_rule(
        "Hazy Maze Cave - Swimming Beast in the Cavern",
        "HMC_SWIMMING_BEAST | logic_hmc_elevator_clip")
    rf.assign_rule("Hazy Maze Cave - Mid Red Coin Room", "WK/LG/BF/SF/TJ")
    rf.assign_rule(
        "Hazy Maze Cave - Upper Red Coin Room",
        "{Hazy Maze Cave - Mid Red Coin Room} & CL | logic_hmc_upper_red_coin_area_wall_kick")
    rf.assign_rule("Hazy Maze Cave - Pit Islands", "TJ+CL | logic_hmc_pit_islands_wall_kick")
    rf.assign_rule("Hazy Maze Cave - Metal-Head Mario Can Move Room",
                   "PURPLE_SWITCHES & MC | PURPLE_SWITCHES & logic_hmc_metal_head_capless")
    rf.assign_rule("Hazy Maze Cave - Metal-Head Mario Can Move!",
                   "LJ | logic_hmc_metal_head_coin_route_capless")
    rf.assign_rule("Hazy Maze Cave - Navigating the Toxic Maze", "WK/SF/BF/TJ")
    rf.assign_rule("Hazy Maze Cave - Watch for Rolling Rocks", "WK")
    for sign in sign_data:
        target_name = sign.area
        rule = HasUnlock("Signs", sign_item_name_for_area(sign.area))
        if sign.rule:
            rule &= rf.build_rule(
                sign.rule,
                rf.get_cannon_item_name(target_name),
                rf.get_cap_item_names(target_name),
                rf.get_arbitrary_item_names(target_name),
                rf.get_action_item_names(target_name),
            )
        rf.world.set_rule(multiworld.get_location(sign.location_name, player), rule)

    if options.one_up_checks:
        rf.add_rule("Hazy Maze Cave - Blue Coin Trail Monty Moles",
                    HasUnlock("Monty Moles", "Hazy Maze Cave - Monty Moles"))
        rf.add_rule("Hazy Maze Cave - Twin Hole Monty Moles",
                    HasUnlock("Monty Moles", "Hazy Maze Cave - Monty Moles"))
    # Lethal Lava Land
    rf.assign_rule("Lethal Lava Land - Boil the Big Bully", "BIG_BULLY")
    rf.assign_rule("Lethal Lava Land - Bully the Bullies", "BULLIES & BIG_BULLY")
    rf.assign_rule(
        "Lethal Lava Land - Red-Hot Log Rolling",
        "WC+TJ | LLL_ROLLING_LOG | LLL_KOOPA_SHELL | logic_lava_damage_boosting")
    for location_name in (
            "Lethal Lava Land - Northeast Brown Platform 1-Up",
            "Lethal Lava Land - Boil the Big Bully Star Lava 1-Up",
            "Lethal Lava Land - Northwest Curve 1-Up",
    ):
        rf.assign_rule(location_name, "LLL_KOOPA_SHELL | logic_lava_damage_boosting")
    rf.assign_rule(
        "Lethal Lava Land - Central Gray Crescent 1-Up",
        "LLL_KOOPA_SHELL | WC+TJ | LJ | logic_lava_damage_boosting")
    rf.assign_rule(
        "Lethal Lava Land - Volcano Brown Platform 1-Up",
        "LLL_KOOPA_SHELL | TJ | LJ | logic_lava_damage_boosting")
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
        "TJ/SF/BF | logic_ssl_top_of_stone_structure_spin_jump_or_tweesters")
    rf.assign_rule(
        "Shifting Sand Land - Upper Pyramid",
        "CL")
    rf.assign_rule(
        "Shifting Sand Land - Pyramid Top Entry Elevator Route",
        "SSL_PYRAMID_ELEVATOR")
    rf.assign_rule(
        "Shifting Sand Land - Inside the Ancient Pyramid",
        "SF/BF/TJ/WK/LG | "
        "{Shifting Sand Land - Pyramid Top Entry} & SSL_PYRAMID_ELEVATOR")
    rf.assign_rule("Shifting Sand Land - Eyerok Arena",
                   "{Shifting Sand Land - Pyramid Top Entry} & SSL_PYRAMID_ELEVATOR & EYEROK | "
                   "logic_ssl_stand_tall_without_pyramid_elevator & EYEROK & LG/KK")
    rf.assign_rule("Shifting Sand Land - Oasis Tree 1-Up", "CL/TJ/BF/SF")
    rf.assign_rule("Shifting Sand Land - Above Quicksand Pit 1-Up", "WC & TJ/CANN | LJ")
    rf.assign_rule("Shifting Sand Land - Pyramid Grindel 1-Up", "THWOMP & TJ/SF/BF/LG")
    rf.assign_rule("Shifting Sand Land - Bob-omb Buddy", "BOBOMB_BUDDY")
    rf.assign_rule(
        "Shifting Sand Land - Pyramid Above the First Wire Grid 1-Up",
        "{Shifting Sand Land - Upper Pyramid} | CL/TJ/SF/BF")
    # Dire, Dire Docks
    rf.assign_rule("Dire, Dire Docks - Board Bowser's Sub",
                   "PURPLE_SWITCHES & DDD_BOWSER_SUB | logic_ddd_board_bowsers_sub_triple_jump")
    rf.assign_rule(
        "Dire, Dire Docks - Through the Jet Stream",
        "DDD_JET_STREAM & MC | DDD_JET_STREAM & logic_ddd_jet_stream_capless")
    rf.assign_rule("Dire, Dire Docks - The Manta Ray's Reward", "DDD_MANTA_RAY")
    rf.assign_rule("Dire, Dire Docks - Collect the Caps...", "VC")
    rf.assign_rule("Dire, Dire Docks - Chests in the Current", "TREASURE_CHESTS")
    # Snowman's Land
    rf.world.set_rule(
        multiworld.get_region("Snowman's Land - Whirl from the Freezing Pond", player).entrances[0],
        rf.build_rule(
            "SPINDRIFTS | CANN",
            cannon_name=rf.get_cannon_item_name("Snowman's Land - Whirl from the Freezing Pond"),
            cap_item_names=rf.get_cap_item_names("Snowman's Land - Whirl from the Freezing Pond"),
            arbitrary_item_names=rf.get_arbitrary_item_names("Snowman's Land - Whirl from the Freezing Pond"),
            action_item_names=rf.get_action_item_names("Snowman's Land - Whirl from the Freezing Pond")))
    rf.assign_rule(
        "Snowman's Land - Upper",
        "{Snowman's Land - Whirl from the Freezing Pond} & SL_KOOPA_SHELL | TJ/SF/BF | CANN")
    rf.assign_rule("Snowman's Land - Top of Snowman's Head", "SL_PENGUIN & BF/SF/TJ | CANN")
    rf.assign_rule("Snowman's Land - Chill with the Bully", "BIG_BULLY")
    rf.assign_rule("Snowman's Land - In the Deep Freeze", "WK/SF/LG/BF/CANN/TJ")
    rf.assign_rule("Snowman's Land - Into the Igloo", "VC & TJ/SF/BF/WK/LG")
    rf.assign_rule("Snowman's Land - Snowman Tree 1-Up", "CL/TJ/BF/SF")
    rf.assign_rule("Snowman's Land - Igloo Ice Block 1-Up", "VC")
    rf.assign_rule("Snowman's Land - Bob-omb Buddy", "BOBOMB_BUDDY")
    # Wet-Dry World
    wdw_pedestal_block_route = (
        "{Wet-Dry World - Low Water} & HEAVE_HOS & logic_wdw_pedestal_heave_ho | "
        "{Wet-Dry World - Low Water} & SF/BF/TJ | "
        "{Wet-Dry World - Mid Water} & HEAVE_HOS & logic_wdw_pedestal_heave_ho | "
        "{Wet-Dry World - Mid Water} & SF/BF/TJ | "
        "{Wet-Dry World - High Water} & LG | "
        "{Wet-Dry World - Highest Water} | {Wet-Dry World - Top}"
    )
    wdw_non_highest_near_top_routes = (
        "{Wet-Dry World - Mid Water}",
        "{Wet-Dry World - Low Water} & HEAVE_HOS",
        "{Wet-Dry World - Mid-High Water} & HEAVE_HOS",
        "{Wet-Dry World - High Water} & HEAVE_HOS",
    )
    wdw_top_without_highest_water = " | ".join(
        [f"{route} & WK/TJ/SF/BF" for route in wdw_non_highest_near_top_routes]
        + [f"{route} & PURPLE_SWITCHES & LJ" for route in wdw_non_highest_near_top_routes]
        + [f"{route} & PURPLE_SWITCHES & logic_wdw_express_elevator_to_top_no_movement"
           for route in wdw_non_highest_near_top_routes]
    )
    wdw_shocking_arrow_lifts_rule = (
        "{Wet-Dry World - Cannon} & {Wet-Dry World - Low Water} | "
        "{Wet-Dry World - Cannon} & {Wet-Dry World - High Water} | "
        "{Wet-Dry World - Cannon} & {Wet-Dry World - Highest Water} & "
        "logic_wdw_shocking_arrow_lifts_underwater_ground_pound | "
        f"{wdw_top_without_highest_water} | "
        "{Wet-Dry World - Mid-High Water} & LG/SF/TJ/BF"
    )
    wdw_wooden_structure_block_rule = (
        "{Wet-Dry World - Mid Water} | "
        f"{wdw_top_without_highest_water}"
    )
    wdw_secrets_target = "Wet-Dry World - Secrets in the Shallows & Sky"
    wdw_secrets_cannon = rf.get_cannon_item_name(wdw_secrets_target)
    wdw_secrets_cap_items = rf.get_cap_item_names(wdw_secrets_target)
    wdw_secrets_arbitrary_items = rf.get_arbitrary_item_names(wdw_secrets_target)
    wdw_secrets_action_items = rf.get_action_item_names(wdw_secrets_target)

    def build_wdw_secrets_rule(rule_expr: str) -> Rule:
        return rf.build_rule(
            rule_expr, wdw_secrets_cannon, wdw_secrets_cap_items,
            wdw_secrets_arbitrary_items, wdw_secrets_action_items)

    wdw_secrets_route = And(
        build_wdw_secrets_rule("CANN/HEAVE_HOS"),
        Or(
            build_wdw_secrets_rule("PURPLE_SWITCHES"),
            And(
                build_wdw_secrets_rule("logic_wdw_top_platforms_to_express_elevator_no_movement"),
                build_wdw_secrets_rule("CANN/SF/BF/WK/TJ"),
            ),
        ),
        Or(
            build_wdw_secrets_rule("logic_wdw_pedestal_heave_ho"),
            build_wdw_secrets_rule("CANN/SF/BF/WK/TJ"),
        ),
        build_wdw_secrets_rule("SF/BF/WK/TJ/LJ/CANN/WDW_WATER_LEVEL_DIAMOND"),
    )
    wdw_express_elevator_target = "Wet-Dry World - Express Elevator--Hurry Up!"
    wdw_express_elevator_cannon = rf.get_cannon_item_name(wdw_express_elevator_target)
    wdw_express_elevator_cap_items = rf.get_cap_item_names(wdw_express_elevator_target)
    wdw_express_elevator_arbitrary_items = rf.get_arbitrary_item_names(wdw_express_elevator_target)
    wdw_express_elevator_action_items = rf.get_action_item_names(wdw_express_elevator_target)

    def build_wdw_express_elevator_rule(rule_expr: str) -> Rule:
        return rf.build_rule(
            rule_expr, wdw_express_elevator_cannon, wdw_express_elevator_cap_items,
            wdw_express_elevator_arbitrary_items, wdw_express_elevator_action_items)

    wdw_express_elevator_route = And(
        build_wdw_express_elevator_rule("CANN/HEAVE_HOS"),
        Or(
            build_wdw_express_elevator_rule("PURPLE_SWITCHES"),
            And(
                build_wdw_express_elevator_rule("logic_wdw_top_platforms_to_express_elevator_no_movement"),
                build_wdw_express_elevator_rule("CANN/SF/BF/WK/TJ"),
            ),
        ),
        build_wdw_express_elevator_rule("SF/BF/WK/WDW_WATER_LEVEL_DIAMOND"),
    )
    rf.assign_rule("Wet-Dry World - Low Water to Mid Water", "WDW_WATER_LEVEL_DIAMOND")
    rf.assign_rule("Wet-Dry World - Mid Water to Low Water", "WDW_WATER_LEVEL_DIAMOND")
    wdw_water_level_diamond_route = (
        "WDW_WATER_LEVEL_DIAMOND & {Wet-Dry World - Top} | "
        "WDW_WATER_LEVEL_DIAMOND & TJ+DV | "
        "WDW_WATER_LEVEL_DIAMOND & {Wet-Dry World - Cannon} & LJ | "
        "WDW_WATER_LEVEL_DIAMOND & PURPLE_SWITCHES"
    )
    rf.assign_rule(
        "Wet-Dry World - Low Water to Mid-High Water",
        "WDW_WATER_LEVEL_DIAMOND & LJ")
    rf.assign_rule(
        "Wet-Dry World - Mid Water to Mid-High Water",
        wdw_water_level_diamond_route)
    rf.assign_rule("Wet-Dry World - Mid-High Water to Mid Water", "WDW_WATER_LEVEL_DIAMOND")
    rf.assign_rule(
        "Wet-Dry World - Mid-High Water to High Water",
        "HEAVE_HOS & WK/TJ/SF/BF | "
        "HEAVE_HOS & PURPLE_SWITCHES & LJ | "
        "HEAVE_HOS & PURPLE_SWITCHES & logic_wdw_express_elevator_to_top_no_movement")
    rf.assign_rule("Wet-Dry World - High Water to Mid-High Water", "WDW_WATER_LEVEL_DIAMOND")
    rf.assign_rule("Wet-Dry World - Highest Water to High Water", "WDW_WATER_LEVEL_DIAMOND")
    rf.assign_rule("Wet-Dry World - Near the Top",
                   "{Wet-Dry World - Highest Water} | {Wet-Dry World - Mid Water} | HEAVE_HOS")
    rf.assign_rule("Wet-Dry World - Top of the Express Elevator", "PURPLE_SWITCHES")
    rf.assign_rule("Wet-Dry World - Top", "WK/TJ/SF/BF")
    rf.assign_rule("Wet-Dry World - Top of the Express Elevator to Top",
                   "LJ | logic_wdw_express_elevator_to_top_no_movement")
    rf.assign_rule("Wet-Dry World - Top to Top of the Express Elevator",
                   "logic_wdw_top_platforms_to_express_elevator_no_movement")
    rf.assign_rule("Wet-Dry World - Cannon to Near the Top", "CANN")
    rf.assign_rule("Wet-Dry World - Cannon to Top", "CANN")
    rf.assign_rule("Wet-Dry World - Downtown",
                   "{Wet-Dry World - Highest Water} & LG | "
                   "{Wet-Dry World - Top} & logic_wdw_downtown_triple_jump")
    rf.assign_rule("Wet-Dry World - Cannon to Downtown", "CANN")
    rf.assign_rule("Wet-Dry World - Shocking Arrow Lifts!", wdw_shocking_arrow_lifts_rule)
    rf.assign_rule_object("Wet-Dry World - Express Elevator--Hurry Up!", wdw_express_elevator_route)
    rf.assign_rule_object("Wet-Dry World - Secrets in the Shallows & Sky", wdw_secrets_route)
    rf.assign_rule("Wet-Dry World - Quick Race Through Downtown!",
                   "WDW_WATER_LEVEL_DIAMOND & VC & WK/BF | "
                   "WDW_WATER_LEVEL_DIAMOND & VC & TJ+LG+PURPLE_SWITCHES | "
                   "logic_wdw_quick_race_triple_jump")
    rf.assign_rule("Wet-Dry World - Downtown Block 1-Up", "WDW_WATER_LEVEL_DIAMOND")
    rf.assign_rule("Wet-Dry World - Bob-omb Buddy",
                   "BOBOMB_BUDDY & {Wet-Dry World - High Water} & TJ | "
                   "BOBOMB_BUDDY & {Wet-Dry World - High Water} & SF+LG | "
                   "BOBOMB_BUDDY & {Wet-Dry World - Highest Water} & TJ/BF/SF")
    # Tall, Tall Mountain
    rf.assign_rule("Tall, Tall Mountain - Upper",
                   "TJ+LG | BF/SF/ROLLING_LOG | logic_ttm_upper_fly_guy_spin_jump")
    rf.assign_rule("Tall, Tall Mountain - Top",
                   "LJ | logic_ttm_top_triple_jump | "
                   "logic_ttm_top_wall_kick | logic_ttm_top_kick | logic_ttm_top_dive")
    rf.assign_rule("Tall, Tall Mountain - Mystery of the Monkey Cage", "TTM_UKIKI")
    rf.assign_rule("Tall, Tall Mountain - Breathtaking View from Bridge",
                   "{Tall, Tall Mountain - Top} & PURPLE_SWITCHES | "
                   "logic_ttm_breathtaking_view_triple_jump_from_below")
    rf.assign_rule("Tall, Tall Mountain - Middle", "VERTICAL_WIND/TJ/LJ")
    rf.assign_rule("Tall, Tall Mountain - Blast to the Lonely Mushroom",
                   "CANN | logic_ttm_lonely_mushroom_cannonless | "
                   "logic_ttm_lonely_mushroom_fly_guy_spin_jump")
    if options.one_up_checks:
        rf.add_rule("Tall, Tall Mountain - Upper Monty Moles",
                    HasUnlock("Monty Moles", "Tall, Tall Mountain - Monty Moles"))
        rf.add_rule("Tall, Tall Mountain - Lower Monty Moles",
                    HasUnlock("Monty Moles", "Tall, Tall Mountain - Monty Moles"))
    rf.assign_rule("Tall, Tall Mountain - Bob-omb Buddy", "BOBOMB_BUDDY")
    # Tiny-Huge Island
    rf.assign_rule("Tiny-Huge Island - Tiny Piranha Area", "TJ/LJ/LG")
    rf.assign_rule("Tiny-Huge Island - Tiny Main", "PURPLE_SWITCHES")
    rf.assign_rule("Tiny-Huge Island - Tiny Piranha Area to Huge Piranha Area", "WARP_PIPES")
    rf.assign_rule("Tiny-Huge Island - Huge Piranha Area to Tiny Piranha Area", "WARP_PIPES")
    rf.assign_rule("Tiny-Huge Island - Tiny Main to Koopa the Quick", "WARP_PIPES")
    rf.assign_rule("Tiny-Huge Island - Koopa the Quick to Tiny Main", "WARP_PIPES")
    rf.assign_rule("Tiny-Huge Island - Windswept Valley to Tiny Main", "WARP_PIPES")
    rf.assign_rule("Tiny-Huge Island - Tiny Main to Windswept Valley", "WARP_PIPES")
    rf.assign_rule(
        "Tiny-Huge Island - Windswept Valley",
        "TJ+DV | LJ+VERTICAL_WIND | LJ+TJ | "
        "logic_thi_windswept_valley_fly_guy_spin_jump")
    rf.assign_rule("Tiny-Huge Island - Cannonball", "LG/SF/BF/TJ/WK")
    rf.assign_rule("Tiny-Huge Island - Koopa the Quick", "SF/BF/TJ/WK")
    rf.assign_rule("Tiny-Huge Island - Huge Top", "SF/BF/TJ")
    rf.assign_rule(
        "Tiny-Huge Island - Huge Island to Huge Top with Koopa Shell",
        "logic_thi_scale_huge_mountain_koopa_shell")
    rf.assign_rule("Tiny-Huge Island - Huge Island to Huge Tree Area", "CANN")
    rf.assign_rule("Tiny-Huge Island - Make Wiggler Squirm", "WIGGLER")
    rf.assign_rule("Tiny-Huge Island - Five Itty Bitty Secrets", "PURPLE_SWITCHES")
    rf.assign_rule("Tiny-Huge Island - Rematch with Koopa the Quick", "THI_KOOPA")
    rf.assign_rule("Tiny-Huge Island - Bob-omb Buddy", "BOBOMB_BUDDY")
    rf.assign_rule("Tiny-Huge Island - Pluck the Piranha Flower", "FIRE_PIRANHA_PLANTS")
    rf.assign_rule("Tiny-Huge Island - Red Coin Cave 1-Up", "WK")
    # Tick Tock Clock
    rf.assign_rule("Tick Tock Clock - First Clock Hand Area",
                   "LG/TJ/SF/BF | logic_ttc_first_clock_hand_area_wall_kick | "
                   "{Tick Tock Clock Stopped} & TTC_SPINNERS")
    rf.assign_rule(
        "Tick Tock Clock - The Pit and the Pendulums Area",
        "CL | logic_ttc_pit_and_pendulums_area_wall_kick")
    rf.assign_rule("Tick Tock Clock - Moving Bars Area", "{Tick Tock Clock Moving} | WK")
    rf.assign_rule(
        "Tick Tock Clock - Upper Moving Bars Area",
        "TJ+LG | {Tick Tock Clock Moving} & SF")
    rf.assign_rule(
        "Tick Tock Clock - More Moving Bars Area", "WK/TJ/LG/SF")
    rf.assign_rule(
        "Tick Tock Clock - Top", "TJ/LG/BF/SF")
    rf.assign_rule(
        "Tick Tock Clock - Top Past Spinners",
        "TTC_SPINNERS | SF | TJ")
    rf.assign_rule(
        "Tick Tock Clock - Moving Bars Area to Top with Wall Kick",
        "logic_ttc_top_past_spinners_wall_kick")
    rf.assign_rule(
        "Tick Tock Clock - Moving Bars Area to Top Past Spinners with Wall Kick",
        "logic_ttc_top_past_spinners_wall_kick")
    rf.assign_rule(
        "Tick Tock Clock - Stomp on the Thwomp",
        "{Tick Tock Clock Moving} & THWOMP | "
        "{Tick Tock Clock Moving} & logic_ttc_stomp_thwomp_triple_jump_wall_kick | "
        "THWOMP & logic_ttc_stomp_thwomp_wall_kick | "
        "logic_ttc_stomp_thwomp_triple_jump_wall_kick & logic_ttc_stomp_thwomp_wall_kick")
    # Rainbow Ride
    rf.assign_rule("Rainbow Ride - Beneath the Pole", "LJ/TJ/DV")
    rf.assign_rule("Rainbow Ride - Maze", "CL")
    rf.assign_rule("Rainbow Ride - Initial to Maze", "RR_CARPETS")
    rf.assign_rule("Rainbow Ride - Carpets", "RR_CARPETS")
    rf.assign_rule(
        "Rainbow Ride - Bob-omb Buddy",
        "BOBOMB_BUDDY & WK | BOBOMB_BUDDY & logic_rr_buddy_ledge_grab")
    rf.assign_rule("Rainbow Ride - Swingin' in the Breeze",
                   "LG/TJ/BF/SF | logic_rr_swingin_no_movement")
    rf.assign_rule("Rainbow Ride - Tricky Triangles!",
                   "PURPLE_SWITCHES & LG/TJ/BF/SF | logic_rr_tricky_triangles_no_movement | "
                   "logic_rr_fall_to_tricky_triangles_from_somewhere_over_the_rainbow")
    rf.assign_rule("Rainbow Ride - Tricky Triangles 1-Up",
                   "PURPLE_SWITCHES & LG/TJ/BF/SF | logic_rr_tricky_triangles_no_movement | "
                   "logic_rr_fall_to_tricky_triangles_one_up_from_somewhere_over_the_rainbow")
    rf.assign_rule(
        "Rainbow Ride - Cruiser to Tricky Triangles",
        "logic_rr_fall_to_tricky_triangles_from_somewhere_over_the_rainbow | "
        "logic_rr_fall_to_tricky_triangles_one_up_from_somewhere_over_the_rainbow")
    rf.assign_rule("Rainbow Ride - Cruiser", "RR_CARPETS & WK/SF/BF/LG/TJ")
    rf.assign_rule("Rainbow Ride - Cruiser Pole 1-Up", "CL")
    rf.assign_rule("Rainbow Ride - House", "RR_CARPETS & TJ/SF/BF/LG")
    rf.assign_rule("Rainbow Ride - Somewhere Over the Rainbow", "CANN")
    # Vanish Cap Under the Moat
    rf.assign_rule("Vanish Cap Under the Moat - Switch",
                   "CHECKERBOARD_PLATFORMS & WK/TJ/BF/SF/LG | logic_vcutm_switch_no_movement")
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
    rf.assign_rule_object(
        "Bowser in the Dark World - Key",
        rf.build_rule(
            "BOWSER",
            arbitrary_item_names=rf.get_arbitrary_item_names("Bowser in the Dark World"),
            action_item_names=rf.get_action_item_names("Bowser in the Dark World"))
        & bowser_arena_bomb_rule(
            "Bowser in the Dark World", options.bowser_in_the_dark_world_health.value))
    if options.one_up_checks:
        for location_name in (
                "Bowser in the Dark World - Center Overhang 1-Up",
                "Bowser in the Dark World - Left Tilting Platform Base 1-Up",
        ):
            rf.assign_rule_object(
                location_name,
                bowser_stage_one_up_rule(
                    "Bowser in the Dark World - Extra 1-Ups", basement_key_rule))
        rf.assign_rule_object(
            "Bowser in the Dark World - Far Overhang 1-Up",
            bowser_stage_one_up_rule(
                "Bowser in the Dark World - Extra 1-Ups", second_floor_key_rule))
    # Bowser in the Fire Sea
    rf.assign_rule("Bowser in the Fire Sea - Upper", "CL")
    rf.assign_rule("Bowser in the Fire Sea - Near Final Poles Block 1-Up", "WK/TJ")
    rf.assign_rule("Bowser in the Fire Sea - Near Final Poles 1-Up", "TJ/WK")
    rf.assign_rule_object(
        "Bowser in the Fire Sea - Key",
        rf.build_rule(
            "BOWSER", arbitrary_item_names=rf.get_arbitrary_item_names("Bowser in the Fire Sea"))
        & bowser_arena_bomb_rule(
            "Bowser in the Fire Sea", options.bowser_in_the_fire_sea_health.value))
    if options.one_up_checks:
        for location_name in (
                "Bowser in the Fire Sea - Near Final Poles 1-Up",
                "Bowser in the Fire Sea - Second Stone Structure 1-Up",
        ):
            existing_rule = rf.build_rule("TJ/WK") if location_name.endswith("Near Final Poles 1-Up") else True_()
            rf.assign_rule_object(
                location_name,
                existing_rule & bowser_stage_one_up_rule(
                    "Bowser in the Fire Sea - Extra 1-Ups", second_floor_key_rule))
    # Wing Mario Over the Rainbow
    wmotr_flight_rule = "WC & TJ | WC & {Wing Mario Over the Rainbow - Bob-omb Buddy Platform} & CANN"
    rf.assign_rule(
        "Wing Mario Over the Rainbow - Bob-omb Buddy Platform",
        "WC+TJ | LG & logic_wmotr_leap_of_faith | logic_wmotr_leap_of_faith_without_ledge_grab")
    rf.assign_rule("Wing Mario Over the Rainbow - Bob-omb Buddy", "BOBOMB_BUDDY")
    rf.assign_rule("Wing Mario Over the Rainbow - Upper", "WC+CANN")
    rf.assign_rule("Wing Mario Over the Rainbow - Block 1-Up", "WC & TJ/CANN")
    # Probably possible with cannon alone, but keep this gated until the route is modeled.
    rf.assign_rule("Wing Mario Over the Rainbow - Cloud 1-Up", wmotr_flight_rule)
    # Bowser in the Sky
    rf.assign_rule("Bowser in the Sky - Chuckya",
                   "TJ/SF/LG/BF | logic_bits_chuckya_no_movement")
    rf.assign_rule("Bowser in the Sky - Arrow Ride",
                   "PURPLE_SWITCHES | logic_bits_arrow_ride_no_purple_switch")
    rf.assign_rule("Bowser in the Sky - Top", "CL | logic_bits_top_without_climb")
    if options.blocksanity:
        blocksanity_rules = {
            "Big Boo's Haunt - Back Entrance Vanish Cap Block": "VC",
            "Big Boo's Haunt - Second Floor Vanish Cap Block": "VC",
            "Big Boo's Haunt - Secret Room Vanish Cap Block": "VC",
            "Bowser in the Dark World - Metal Cap Block": "MC",
            "Bob-omb Battlefield - Near Flower Patches Wing Cap Block": "WC",
            "Bob-omb Battlefield - Wooden Ramp Wing Cap Block": "WC",
            "Bob-omb Battlefield - Island Wing Cap Block": "WC",
            "Castle Grounds - Roof Wing Cap Block": "WC",
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
            "Jolly Roger Bay - Plunder in the Sunken Ship Star Block": "TREASURE_CHESTS",
            "Lethal Lava Land - Wing Cap Block": "WC",
            "Lethal Lava Land - Koopa Shell Block": "LLL_KOOPA_SHELL",
            "Bowser in the Fire Sea - 3 Coins Block": "CL | WK | logic_lava_damage_boosting",
            "Bowser in the Fire Sea - Near Final Poles 1-Up Block": "WK/TJ",
            "Rainbow Ride - Somewhere Over the Rainbow Star Block": "CANN",
            "Snowman's Land - Vanish Cap Block": "VC & TJ/SF/BF/LG | logic_sl_igloo_vanish_block_with_spindrift",
            "Shifting Sand Land - Outside Pyramid Wing Cap Block": "WC",
            "Shifting Sand Land - Stone Structure Wing Cap Block": "WC",
            "Shifting Sand Land - Cannon Wing Cap Block": "WC",
            "Tower of the Wing Cap - Wing Cap Block": "WC",
            "Tick Tock Clock - Below Red Coin Spinners 10 Coins Block": "TEN_COIN_BLOCKS",
            "Tick Tock Clock - First Pendulum 3 Coins Block": "THREE_COIN_BLOCKS",
            "Tick Tock Clock - Above Red Coin Spinners 3 Coins Block": "THREE_COIN_BLOCKS",
            "Tick Tock Clock - Heave-ho First 3 Coins Block": "THREE_COIN_BLOCKS",
            "Tick Tock Clock - Heave-ho Second 3 Coins Block": "THREE_COIN_BLOCKS",
            "Tick Tock Clock - Above Timed Jumps on Moving Bars 3 Coins Block": "THREE_COIN_BLOCKS",
            "Tick Tock Clock - Above Four Moving Bars 10 Coins Block": "TEN_COIN_BLOCKS",
            "Tick Tock Clock - Past Three Spinners 3 Coins Block": "THREE_COIN_BLOCKS",
            "Tick Tock Clock - Top Clock Hand 10 Coins Block": "TEN_COIN_BLOCKS",
            "Tick Tock Clock - Top Central Platform 10 Coins Block": "TEN_COIN_BLOCKS",
            "Tick Tock Clock - Beneath the Thwomp 10 Coins Block": "TEN_COIN_BLOCKS",
            "Vanish Cap Under the Moat - Bottom of Slide Vanish Cap Block": "VC",
            "Vanish Cap Under the Moat - 3 Coins Block": "LG/TJ/BF/SF",
            "Vanish Cap Under the Moat - Near Switch Vanish Cap Block":
                "VC & CHECKERBOARD_PLATFORMS & WK/TJ/BF/SF/LG | "
                "VC & logic_vcutm_switch_no_movement",
            "Wet-Dry World - Shocking Arrow Lifts Star Block": wdw_shocking_arrow_lifts_rule,
            "Wet-Dry World - Pedestal 10 Coins Block": wdw_pedestal_block_route,
            "Wet-Dry World - Wooden Structure 3 Coins Block": wdw_wooden_structure_block_rule,
            "Wet-Dry World - Downtown Vanish Cap Block": "WDW_WATER_LEVEL_DIAMOND & VC",
            "Wet-Dry World - Metal Cap Block": "MC",
            "Wet-Dry World - Quick Race Through Downtown Star Vanish Cap Block": "WDW_WATER_LEVEL_DIAMOND & VC",
            "Wet-Dry World - Downtown 1-Up Block": "WDW_WATER_LEVEL_DIAMOND",
            "Whomp's Fortress - Metal Cap Block": "MC",
            "Wing Mario Over the Rainbow - Highest Cloud Wing Cap Block": "WC",
            "Wing Mario Over the Rainbow - Below the Pole Cloud Wing Cap Block":
                wmotr_flight_rule,
            "Wing Mario Over the Rainbow - Starting Cloud Wing Cap Block": "WC",
            "Wing Mario Over the Rainbow - Lowest Cloud Wing Cap Block":
                "WC+TJ | WC & logic_wmotr_leap_of_faith | "
                "WC & logic_wmotr_leap_of_faith_without_ledge_grab",
            "Wing Mario Over the Rainbow - Bob-omb Buddy Platform Wing Cap Block": "WC",
            "Wing Mario Over the Rainbow - Overlooking Bob-omb Buddy Cloud Wing Cap Block": wmotr_flight_rule,
        }
        for location_name, rule in blocksanity_rules.items():
            rf.assign_rule(location_name, rule)
        coin_block_unlock_locations = {
            ("3-Coin Blocks", "Bowser in the Dark World - 3-Coin Block"): (
                "Bowser in the Dark World - 3 Coins Block",
            ),
            ("3-Coin Blocks", "Bowser in the Fire Sea - 3-Coin Block"): (
                "Bowser in the Fire Sea - 3 Coins Block",
            ),
            ("3-Coin Blocks", "Jolly Roger Bay - 3-Coin Block"): (
                "Jolly Roger Bay - 3 Coins Block",
            ),
            ("3-Coin Blocks", "Snowman's Land - 3-Coin Block"): (
                "Snowman's Land - 3 Coins Block",
            ),
            ("3-Coin Blocks", "Tiny-Huge Island - 3-Coin Block"): (
                "Tiny-Huge Island - 3 Coins Block",
            ),
            ("3-Coin Blocks", "Tick Tock Clock - 3-Coin Blocks"): (
                "Tick Tock Clock - Above Timed Jumps on Moving Bars 3 Coins Block",
                "Tick Tock Clock - First Pendulum 3 Coins Block",
                "Tick Tock Clock - Past Three Spinners 3 Coins Block",
                "Tick Tock Clock - Heave-ho First 3 Coins Block",
                "Tick Tock Clock - Above Red Coin Spinners 3 Coins Block",
                "Tick Tock Clock - Heave-ho Second 3 Coins Block",
            ),
            ("3-Coin Blocks", "Vanish Cap Under the Moat - 3-Coin Block"): (
                "Vanish Cap Under the Moat - 3 Coins Block",
            ),
            ("3-Coin Blocks", "Wet-Dry World - 3-Coin Blocks"): (
                "Wet-Dry World - Push Block 3 Coins Block",
                "Wet-Dry World - Wooden Structure 3 Coins Block",
            ),
            ("10-Coin Blocks", "Big Boo's Haunt - 10-Coin Block"): (
                "Big Boo's Haunt - 10 Coins Block",
            ),
            ("10-Coin Blocks", "Bowser in the Fire Sea - 10-Coin Block"): (
                "Bowser in the Fire Sea - 10 Coins Block",
            ),
            ("10-Coin Blocks", "Tick Tock Clock - 10-Coin Blocks"): (
                "Tick Tock Clock - Top Clock Hand 10 Coins Block",
                "Tick Tock Clock - Above Four Moving Bars 10 Coins Block",
                "Tick Tock Clock - Top Central Platform 10 Coins Block",
                "Tick Tock Clock - Below Red Coin Spinners 10 Coins Block",
                "Tick Tock Clock - Beneath the Thwomp 10 Coins Block",
            ),
            ("10-Coin Blocks", "Wet-Dry World - 10-Coin Blocks"): (
                "Wet-Dry World - Push Block 10 Coins Block",
                "Wet-Dry World - Pedestal 10 Coins Block",
                "Wet-Dry World - Top of Express Elevator 10 Coins Block",
            ),
        }
        for (global_item_name, per_level_item_name), location_names in coin_block_unlock_locations.items():
            required_item = get_unlock_item_name(
                options, "coin_object_unlocks", global_item_name, per_level_item_name)
            for location_name in location_names:
                rf.add_rule(location_name, required_item)
    for course_name, evaluator in COIN_EVALUATORS.items():
        register_coin_evaluator(course_name, evaluator)
    red_coin_star_by_course = {
        "Bob-omb Battlefield": "Bob-omb Battlefield - Find the 8 Red Coins",
        "Whomp's Fortress": "Whomp's Fortress - Red Coins on the Floating Isle",
        "Jolly Roger Bay": "Jolly Roger Bay - Red Coins on the Ship Afloat",
        "Cool, Cool Mountain": "Cool, Cool Mountain - Frosty Slide for 8 Red Coins",
        "Big Boo's Haunt": "Big Boo's Haunt - Seek the 8 Red Coins",
        "Hazy Maze Cave": "Hazy Maze Cave - Elevate for 8 Red Coins",
        "Lethal Lava Land": "Lethal Lava Land - 8-Coin Puzzle with 15 Pieces",
        "Shifting Sand Land": "Shifting Sand Land - Free Flying for 8 Red Coins",
        "Dire, Dire Docks": "Dire, Dire Docks - Pole-Jumping for Red Coins",
        "Snowman's Land": "Snowman's Land - Shell Shreddin' for Red Coins",
        "Wet-Dry World": "Wet-Dry World - Go to Town for Red Coins",
        "Tall, Tall Mountain": "Tall, Tall Mountain - Scary 'Shrooms, Red Coins",
        "Tiny-Huge Island": "Tiny-Huge Island - Wiggler's Red Coins",
        "Tick Tock Clock": "Tick Tock Clock - Stop Time for Red Coins",
        "Rainbow Ride": "Rainbow Ride - Coins Amassed in a Maze",
        "The Secret Aquarium": "The Secret Aquarium - Red Coins",
        "Wing Mario Over the Rainbow": "Wing Mario Over the Rainbow - Red Coins",
        "Tower of the Wing Cap": "Tower of the Wing Cap - Red Coins",
        "Vanish Cap Under the Moat": "Vanish Cap Under the Moat - Red Coins",
        "Cavern of the Metal Cap": "Cavern of the Metal Cap - Red Coins",
        "Bowser in the Dark World": "Bowser in the Dark World - Red Coins",
        "Bowser in the Fire Sea": "Bowser in the Fire Sea - Red Coins",
        "Bowser in the Sky": "Bowser in the Sky - Red Coins",
    }
    for course_name, location_name in red_coin_star_by_course.items():
        rf.assign_rule_object(location_name, CanCollectAllRedCoins(course_name))
    rf.add_rule("Bowser in the Fire Sea - Red Coins", rf.build_rule("WK/TJ"))
    vcutm_red_coin_star = "Vanish Cap Under the Moat - Red Coins"
    rf.add_rule(vcutm_red_coin_star, rf.build_rule(
        "VC | logic_vcutm_wall_kick_over_vanish_cap_grate",
        rf.get_cannon_item_name(vcutm_red_coin_star),
        rf.get_cap_item_names(vcutm_red_coin_star),
        rf.get_arbitrary_item_names(vcutm_red_coin_star),
        rf.get_action_item_names(vcutm_red_coin_star),
    ))

    coin_star_requirements = {
        "Bob-omb Battlefield": options.bob_omb_battlefield_coin_star_requirement.value,
        "Whomp's Fortress": options.whomps_fortress_coin_star_requirement.value,
        "Jolly Roger Bay": options.jolly_roger_bay_coin_star_requirement.value,
        "Cool, Cool Mountain": options.cool_cool_mountain_coin_star_requirement.value,
        "Big Boo's Haunt": options.big_boos_haunt_coin_star_requirement.value,
        "Hazy Maze Cave": options.hazy_maze_cave_coin_star_requirement.value,
        "Lethal Lava Land": options.lethal_lava_land_coin_star_requirement.value,
        "Shifting Sand Land": options.shifting_sand_land_coin_star_requirement.value,
        "Dire, Dire Docks": options.dire_dire_docks_coin_star_requirement.value,
        "Snowman's Land": options.snowmans_land_coin_star_requirement.value,
        "Wet-Dry World": options.wet_dry_world_coin_star_requirement.value,
        "Tall, Tall Mountain": options.tall_tall_mountain_coin_star_requirement.value,
        "Tiny-Huge Island": options.tiny_huge_island_coin_star_requirement.value,
        "Tick Tock Clock": options.tick_tock_clock_coin_star_requirement.value,
        "Rainbow Ride": options.rainbow_ride_coin_star_requirement.value,
    }
    for course_name, required_coins in coin_star_requirements.items():
        rf.assign_rule_object(
            f"{course_name} - Coins Star",
            CanCollectCoins(course_name, required_coins))

    for location in multiworld.get_locations(player):
        coin_output = coin_output_by_name.get(location.name)
        if coin_output is not None:
            rf.assign_rule_object(
                location.name,
                CanCollectCoinOutput(
                    coin_output.output_id.course_name,
                    coin_output.source_methods,
                ),
            )
            continue
        coin_count_check_location = parse_coin_count_check_location_name(location.name)
        if coin_count_check_location is not None:
            course_name, coin_count = coin_count_check_location
            rf.assign_rule_object(location.name, CanCollectCoins(course_name, coin_count))
            continue
        global_coin_count = parse_global_coin_count_check_location_name(location.name)
        if global_coin_count is not None:
            course_caps = tuple(
                (course_name, cap)
                for (course_name, _offset, _option_name, _maximum), cap
                in zip(global_coin_count_course_data, world.get_global_coin_count_caps())
            )
            rf.assign_rule_object(location.name, CanCollectGlobalCoins(course_caps, global_coin_count))

    # Castle Stars
    rf.assign_rule("Castle Grounds - Roof", "CANN")
    rf.add_rule("Castle Basement - Toad", CanReachRegion("Castle Basement") & Has("Castle - Toads"))
    rf.add_rule("Castle Second Floor - Toad", CanReachRegion("Castle Second Floor") & Has("Castle - Toads"))
    rf.add_rule("Castle Third Floor - Toad", CanReachRegion("Castle Third Floor") & Has("Castle - Toads"))
    rf.add_rule("Castle Grounds - Yoshi", Has("Castle - Yoshi"))

    rf.assign_rule("Castle Grounds - Third Tree From Waterfall 1-Up",
                   "CL/TJ/BF/SF | logic_castle_waterfall_tree_1up_with_no_movement")
    rf.assign_rule("Castle Grounds - Bridge Coins 1-Up", "{{Castle Basement - Drain the Moat}} & WK & TJ/SF")
    rf.assign_rule("Castle First Floor - Jolly Roger Bay Room 1-Up",
                   "SF/BF | TJ & LG | logic_secret_aquarium_triple_jump | "
                   "logic_secret_aquarium_wall_kick_and_ledge_grab | "
                   "logic_secret_aquarium_wall_kick | logic_secret_aquarium_ledge_grab")
    rf.assign_rule("Castle Basement - Drain the Moat", "GP")
    rf.assign_rule("Castle Basement - MIPS 1", "DV | logic_castle_mips_without_dive")
    rf.assign_rule("Castle Basement - MIPS 2", "DV | logic_castle_mips_without_dive")
    rf.add_rule(
        "Castle Basement - MIPS 1",
        CanReachRegion("Castle Basement") & Has("Castle - Progressive MIPS"))
    rf.add_rule(
        "Castle Basement - MIPS 2",
        CanReachRegion("Castle Basement") & Has("Castle - Progressive MIPS", 2))

    active_location_names = {location.name for location in multiworld.get_locations(player)}
    freestanding_star_locations = {
        "Bob-omb Battlefield": {"Bob-omb Battlefield - Behind Chain Chomp's Gate"},
        "Whomp's Fortress": {
            "Whomp's Fortress - To the Top of the Fortress",
            "Whomp's Fortress - Shoot into the Wild Blue",
            "Whomp's Fortress - Fall onto the Caged Island",
            "Whomp's Fortress - Blast Away the Wall",
        },
        "Jolly Roger Bay": {
            "Jolly Roger Bay - Through the Jet Stream",
        },
        "Cool, Cool Mountain": {"Cool, Cool Mountain - Wall Kicks Will Work"},
        "Big Boo's Haunt": {"Big Boo's Haunt - Secret of the Haunted Books"},
        "Hazy Maze Cave": {
            "Hazy Maze Cave - Swimming Beast in the Cavern",
            "Hazy Maze Cave - Metal-Head Mario Can Move!",
            "Hazy Maze Cave - Navigating the Toxic Maze",
            "Hazy Maze Cave - A-Maze-Ing Emergency Exit",
            "Hazy Maze Cave - Watch for Rolling Rocks",
        },
        "Lethal Lava Land": {
            "Lethal Lava Land - Red-Hot Log Rolling",
            "Lethal Lava Land - Hot-Foot-It into the Volcano",
            "Lethal Lava Land - Elevator Tour in the Volcano",
        },
        "Shifting Sand Land": {
            "Shifting Sand Land - Shining Atop the Pyramid",
            "Shifting Sand Land - Inside the Ancient Pyramid",
        },
        "Dire, Dire Docks": {
            "Dire, Dire Docks - Board Bowser's Sub",
            "Dire, Dire Docks - Collect the Caps...",
        },
        "Snowman's Land": {
            "Snowman's Land - Snowman's Big Head",
            "Snowman's Land - In the Deep Freeze",
            "Snowman's Land - Into the Igloo",
        },
        "Wet-Dry World": {
            "Wet-Dry World - Express Elevator--Hurry Up!",
            "Wet-Dry World - Quick Race Through Downtown!",
        },
        "Tall, Tall Mountain": {
            "Tall, Tall Mountain - Scale the Mountain",
            "Tall, Tall Mountain - Mysterious Mountainside",
            "Tall, Tall Mountain - Breathtaking View from Bridge",
            "Tall, Tall Mountain - Blast to the Lonely Mushroom",
        },
        "Tick Tock Clock": {
            "Tick Tock Clock - Roll into the Cage",
            "Tick Tock Clock - The Pit and the Pendulums",
            "Tick Tock Clock - Get a Hand",
            "Tick Tock Clock - Stomp on the Thwomp",
            "Tick Tock Clock - Timed Jumps on Moving Bars",
        },
        "Rainbow Ride": {
            "Rainbow Ride - Cruiser Crossing the Rainbow",
            "Rainbow Ride - The Big House in the Sky",
            "Rainbow Ride - Swingin' in the Breeze",
            "Rainbow Ride - Tricky Triangles!",
        },
    }
    for level_name, location_names in freestanding_star_locations.items():
        per_level_name = next(name for name in freestanding_star_item_data_table if name.startswith(f"{level_name} -"))
        for location_name in location_names & active_location_names:
            rf.add_rule(location_name, HasUnlock("Freestanding Stars", per_level_name))

    star_block_location_names = {
        location_name for location_name in active_location_names if location_name.endswith("Star Block")
    }
    for location_name in star_block_location_names:
        level_name = location_name.split(" - ", 1)[0]
        per_level_name = next(name for name in star_block_item_data_table if name.startswith(f"{level_name} -"))
        rf.add_rule(location_name, HasUnlock("Star Blocks", per_level_name))

    for location_name, per_level_name in {
        "Bob-omb Battlefield - Shoot to the Island in the Sky": "Bob-omb Battlefield - Star Block",
        "Jolly Roger Bay - Blast to the Stone Pillar": "Jolly Roger Bay - Star Blocks",
        "Jolly Roger Bay - Plunder in the Sunken Ship": "Jolly Roger Bay - Star Blocks",
        "The Princess's Secret Slide - Block Star": "The Princess's Secret Slide - Star Block",
        "Rainbow Ride - Somewhere Over the Rainbow": "Rainbow Ride - Star Block",
        "Snowman's Land - Whirl from the Freezing Pond": "Snowman's Land - Star Block",
        "Tiny-Huge Island - The Tip Top of the Huge Island": "Tiny-Huge Island - Star Block",
        "Wet-Dry World - Shocking Arrow Lifts!": "Wet-Dry World - Star Blocks",
        "Wet-Dry World - Top o' the Town": "Wet-Dry World - Star Blocks",
    }.items():
        rf.add_rule(location_name, HasUnlock("Star Blocks", per_level_name))

    for location_name, per_level_name in {
        "Lethal Lava Land - Koopa Shell Block": "Lethal Lava Land - Koopa Shell",
        "Shifting Sand Land - Stone Structure Koopa Shell Block": "Shifting Sand Land - Koopa Shell Block",
        "Snowman's Land - Koopa Shell Block": "Snowman's Land - Koopa Shell Block",
    }.items():
        if location_name in active_location_names:
            rf.add_rule(location_name, HasUnlock("Koopa Shell Blocks", per_level_name))

    for location_name, per_level_name in {
        "Bob-omb Battlefield - Mario Wings to the Sky": "Bob-omb Battlefield - Star Secrets",
        "Shifting Sand Land - Pyramid Puzzle": "Shifting Sand Land - Star Secrets",
        "Wet-Dry World - Secrets in the Shallows & Sky": "Wet-Dry World - Star Secrets",
        "Tiny-Huge Island - Five Itty Bitty Secrets": "Tiny-Huge Island - Star Secrets",
    }.items():
        rf.add_rule(location_name, HasUnlock("Star Secrets", per_level_name))

    for location_name in (
            "Tower of the Wing Cap - Switch",
            "Cavern of the Metal Cap - Switch",
            "Vanish Cap Under the Moat - Switch"):
        level_name = location_name.rsplit(" - ", 1)[0]
        rf.add_rule(location_name, HasUnlock("Cap Switches", f"{level_name} - Cap Switch"))

    if options.one_up_checks:
        for location_name, category_name in one_up_unlock_category_by_location.items():
            if location_name not in active_location_names:
                continue
            if location_name.endswith("Monty Moles"):
                continue
            level_name = rf.get_level_name_from_target(location_name)
            per_level_item_name = f"{level_name} - {category_name}"
            rf.add_rule(location_name, HasUnlock(category_name, per_level_item_name))

    starting_state = CollectionState(multiworld)
    reachable_starting_checks = sum(
        location.address is not None
        and is_starting_check_location(location.name, options)
        and location.can_reach(starting_state)
        for location in multiworld.get_locations(player)
    )
    if reachable_starting_checks < 2:
        castle_lobby = multiworld.get_region("Castle First Floor", player)
        fallback_names = ("Castle First Floor - Free Item", "Castle First Floor - Another Free Item")
        for location_name in fallback_names[:2 - reachable_starting_checks]:
            castle_lobby.locations.append(
                SM64Location(player, location_name, location_table[location_name], castle_lobby))
            multiworld.itempool.append(world.create_filler())

    for spot in (*multiworld.get_entrances(player), *multiworld.get_locations(player)):
        if spot.access_rule is DEFAULT_COLLECTION_RULE.__func__:
            rf.world.set_rule(spot, True_())

    # Destination Format: LVL | AREA with LVL = LEVEL_x, AREA = Area as used in sm64 code
    # Cast to int to not rely on availability of SM64Levels enum. Will cause crash in MultiServer otherwise
    for entrance_lvl, destination in randomized_entrances.items():
        area_connections.setdefault(int(entrance_lvl), int(sm64_entrances_to_level[destination]))

    can_defeat_bowser_in_the_sky = (
        CanReachRegion("Bowser in the Sky - Bowser Arena")
        & rf.build_rule("BOWSER", arbitrary_item_names=rf.get_arbitrary_item_names("Bowser in the Sky"))
        & bowser_arena_bomb_rule("Bowser in the Sky", options.bowser_in_the_sky_health.value)
    )
    if options.completion_type == options.completion_type.option_Last_Bowser_Stage:
        rf.world.set_completion_rule(can_defeat_bowser_in_the_sky)
    elif options.completion_type == options.completion_type.option_All_Bowser_Stages:
        all_bowser_stages = (
            CanReachLocation("Bowser in the Dark World - Key")
            & CanReachLocation("Bowser in the Fire Sea - Key")
            & can_defeat_bowser_in_the_sky
        )
        rf.assign_rule_object("Bowser in the Sky - Grand Star", all_bowser_stages)
        rf.world.set_completion_rule(CanReachLocation("Bowser in the Sky - Grand Star"))

    if defer_randomized_entrances:
        for entrance_id in world.shuffled_entrance_source_ids:
            entrance = world.randomized_entrance_connections[entrance_id]
            target = entrance.connected_region
            if target is None:
                continue
            target.entrances.remove(entrance)
            entrance.connected_region = None
            world.deferred_entrance_targets[entrance_id] = target


class RuleFactory:

    multiworld: MultiWorld
    player: int
    move_rando_bitvec: bool
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
        "MARIOS_HAT": "Mario's Hat",
        "MIPS1": "Castle - Progressive MIPS",
        "BOB_KING": "Bob-omb Battlefield - King Bob-omb",
        "BOB_KOOPA": "Bob-omb Battlefield - Koopa the Quick",
        "BOB_BUDDY": "Bob-omb Battlefield - Bob-omb Buddy",
        "WF_KING": "Whomp's Fortress - Whomp King",
        "WF_FORTRESS": "Whomp's Fortress - Fortress",
        "WF_BUDDY": "Whomp's Fortress - Bob-omb Buddy",
        "WF_HOOT": "Whomp's Fortress - Hoot",
        "CCM_SNOWMAN_BODY": "Cool, Cool Mountain - Snowman's Body",
        "CCM_BIG_PENGUIN": "Cool, Cool Mountain - Big Penguin",
        "JRB_SUNKEN_SHIP": "Jolly Roger Bay - Sunken Ship",
        "JRB_RAISED_SHIP": "Jolly Roger Bay - Raised Ship",
        "JRB_BUDDY": "Jolly Roger Bay - Bob-omb Buddy",
        "JRB_JET_STREAM": "Jolly Roger Bay - Jet Stream",
        "DDD_JET_STREAM": "Dire, Dire Docks - Jet Stream",
        "JRB_UNAGI": "Jolly Roger Bay - Unagi",
        "LLL_KOOPA_SHELL": "Lethal Lava Land - Koopa Shell",
        "SSL_KOOPA_SHELL": "Shifting Sand Land - Koopa Shell Block",
        "SL_KOOPA_SHELL": "Snowman's Land - Koopa Shell Block",
        "SSL_KLEPTO": "Shifting Sand Land - Klepto with Star",
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
        "CCM_BABY_PENGUINS": "Cool, Cool Mountain - Baby Penguins",
        "SL_PENGUIN": "Snowman's Land - Penguin",
        "SSL_PYRAMID_ELEVATOR": "Shifting Sand Land - Pyramid Elevator",
        "LLL_ROLLING_LOG": "Rolling Logs",
        "PURPLE_SWITCHES": "Purple Switches",
        "WDW_WATER_LEVEL_DIAMOND": "Wet-Dry World - Water Level Diamond",
        "TTC_SPINNERS": "Tick Tock Clock - Spinners",
        "VERTICAL_WIND": "Vertical Wind",
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
        self.world = multiworld.worlds[player]
        self.options = options
        self.player = player
        self.move_rando_bitvec = move_rando_bitvec
        self.assigned_rules: dict[str, Rule] = {}

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
        self.assigned_rules[target_name] = rule
        self.world.set_rule(target, rule)

    def add_rule(self, target_name: str, rule: Rule) -> None:
        combined_rule = self.assigned_rules.get(target_name, True_()) & rule
        self.assigned_rules[target_name] = combined_rule
        target = (
            self.multiworld.get_location(target_name, self.player)
            if target_name in location_table
            else self.multiworld.get_entrance(target_name, self.player)
        )
        self.world.set_rule(target, combined_rule)

    def assign_rule_object(self, target_name: str, rule: Rule) -> None:
        self.assigned_rules[target_name] = rule
        target = (
            self.multiworld.get_location(target_name, self.player)
            if target_name in location_table
            else self.multiworld.get_entrance(target_name, self.player)
        )
        self.world.set_rule(target, rule)

    def get_indirect_condition_region_names(
            self, rule_expr: str, seen_tricks: set[str] | None = None) -> set[str]:
        region_names = set(re.findall(r"(?<!\{)\{([^{}]+)\}(?!\})", rule_expr))
        seen_tricks = set() if seen_tricks is None else seen_tricks
        for trick_name in re.findall(r"\blogic_[a-z0-9_]+\b", rule_expr):
            if trick_name in logic_tricks_by_internal_id and trick_name not in seen_tricks:
                seen_tricks.add(trick_name)
                region_names.update(self.get_indirect_condition_region_names(
                    logic_tricks_by_internal_id[trick_name][1].get("rule", ""), seen_tricks))
        return region_names

    def build_rule(
            self, rule_expr: str, cannon_name: str = '', cap_item_names: dict[str, str | Rule] | None = None,
            arbitrary_item_names: dict[str, str | bool] | None = None,
            action_item_names: dict[str, str | bool] | None = None,
            painting_lvl_name: str = None, star_num_req: int = None) -> Rule:
        # Star/painting requirements are outer and'd requirements, logically (painting? star? and (rule_expr))
        base_rule = self.build_star_painting_entry_requirements(painting_lvl_name, star_num_req)
        if cap_item_names is None:
            cap_item_names = {}
        if arbitrary_item_names is None:
            arbitrary_item_names = self.get_arbitrary_item_names("")
        if action_item_names is None:
            action_item_names = self.get_action_item_names("Castle")
        expressions = rule_expr.split(" | ") if len(rule_expr) > 0 else []
        rules: list[Rule] = []
        for expression in expressions:
            or_clause = self.combine_and_clauses(
                expression, cannon_name, cap_item_names, arbitrary_item_names, action_item_names)
            if or_clause is True:
                return base_rule
            if or_clause is not False:
                rules.append(or_clause)
        if rules:
            return base_rule & Or(*rules)
        if expressions:
            return False_()
        return base_rule

    def build_star_painting_entry_requirements(
            self, painting_lvl_name: str = None, star_num_req: int = None) -> Rule:
        star_rule: Rule = True_()
        painting_rule: Rule = True_()
        if painting_lvl_name is not None:
            painting_item_name = f"Unlock {painting_lvl_name}"
            painting_rule = HasUnlock(painting_item_name, painting_item_name)
        return star_rule & painting_rule

    def get_level_name_from_target(self, target_name: str) -> str:
        if " - " in target_name:
            level_name = target_name.split(" - ", 1)[0]
            if level_name in {
                    "Castle Grounds", "Castle First Floor", "Castle Courtyard",
                    "Castle Basement", "Castle Second Floor", "Castle Third Floor"}:
                return "Castle"
            return level_name
        if target_name in per_level_move_area_names:
            return target_name
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

    def get_cap_item_names(self, target_name: str) -> dict[str, Rule]:
        level_name = self.get_level_name_from_target(target_name)
        return {
            token: HasUnlock(self.global_cap_item_name_by_token[token], item_name_by_level[level_name])
            for token, item_name_by_level in self.cap_item_name_by_token_and_level.items()
            if level_name in item_name_by_level
        }

    def get_arbitrary_item_names(self, target_name: str) -> dict[str, str | bool]:
        level_name = self.get_level_name_from_target(target_name)
        unlock_level_name = {
            "The Secret Aquarium": "Secret Aquarium",
            "The Princess's Secret Slide": "Princess's Secret Slide",
        }.get(level_name, level_name)
        item_names = {
            token: HasUnlock(item_name, item_name)
            for token, item_name in simple_level_feature_items.items()
        }
        for token in per_act_feature_tokens:
            per_level_item_name = self.token_table[token]
            if token in {"BOB_BUDDY", "WF_BUDDY", "JRB_BUDDY"}:
                item_names[token] = HasUnlock("Bob-omb Buddies", per_level_item_name)
            else:
                item_names[token] = HasUnlock(per_level_item_name, per_level_item_name)
        if level_name in {"Jolly Roger Bay", "Dire, Dire Docks"}:
            item_names[f"{'JRB' if level_name == 'Jolly Roger Bay' else 'DDD'}_JET_STREAM"] = HasUnlock(
                "Jet Streams", f"{level_name} - Jet Stream")
        item_names["CHECKERBOARD_PLATFORMS"] = (
            get_level_feature_item_name(
                self.options.level_features,
                "Checkerboard Platforms", checkerboard_item_name_by_level[level_name])
            if level_name in checkerboard_item_name_by_level else True
        )
        item_names["LLL_ROLLING_LOG"] = (
            get_level_feature_item_name(
                self.options.level_features,
                "Rolling Logs", rolling_log_item_name_by_level[level_name])
            if level_name in rolling_log_item_name_by_level else True
        )
        item_names["ROLLING_LOG"] = item_names["LLL_ROLLING_LOG"]
        item_names["PURPLE_SWITCHES"] = (
            get_level_feature_item_name(
                self.options.level_features,
                "Purple Switches", purple_switch_item_name_by_level[level_name])
            if level_name in purple_switch_item_name_by_level else True
        )
        koopa_shell_block_item_name_by_level = {
            "Lethal Lava Land": "Lethal Lava Land - Koopa Shell",
            "Shifting Sand Land": "Shifting Sand Land - Koopa Shell Block",
            "Snowman's Land": "Snowman's Land - Koopa Shell Block",
        }
        koopa_shell_item_name = koopa_shell_block_item_name_by_level.get(level_name)
        if koopa_shell_item_name:
            token = {
                "Lethal Lava Land": "LLL_KOOPA_SHELL",
                "Shifting Sand Land": "SSL_KOOPA_SHELL",
                "Snowman's Land": "SL_KOOPA_SHELL",
            }[level_name]
            item_names[token] = HasUnlock("Koopa Shell Blocks", koopa_shell_item_name)
        vertical_wind_item_name_by_level = {
            "Cool, Cool Mountain": "Cool, Cool Mountain - Vertical Wind",
            "Tall, Tall Mountain": "Tall, Tall Mountain - Vertical Wind",
            "Tiny-Huge Island": "Tiny-Huge Island - Vertical Wind",
        }
        item_names["VERTICAL_WIND"] = (
            HasUnlock("Vertical Wind", vertical_wind_item_name_by_level[level_name])
            if level_name in vertical_wind_item_name_by_level else True
        )
        warp_pipe_item_name = warp_pipe_item_name_by_level.get(level_name)
        if warp_pipe_item_name:
            item_names["WARP_PIPES"] = get_level_feature_item_name(
                self.options.level_features, "Warp Pipes", warp_pipe_item_name)
        buddy_item_name = bobomb_buddy_item_name_by_level.get(level_name)
        if buddy_item_name:
            item_names["BOBOMB_BUDDY"] = HasUnlock("Bob-omb Buddies", buddy_item_name)
        chest_item_name = treasure_chest_item_name_by_level.get(level_name)
        if chest_item_name:
            item_names["TREASURE_CHESTS"] = get_level_feature_item_name(
                self.options.level_features, "Treasure Chests", chest_item_name)
        item_names["SINGLE_YELLOW_COINS"] = get_unlock_item_name(
            self.options, "coin_object_unlocks",
            "Single Yellow Coins", f"{unlock_level_name} - Single Yellow Coins")
        item_names["VERTICAL_COIN_RINGS"] = get_unlock_item_name(
            self.options, "coin_object_unlocks",
            "Vertical Coin Rings", f"{unlock_level_name} - Vertical Coin Rings")
        item_names["HORIZONTAL_COIN_LINES"] = get_unlock_item_name(
            self.options, "coin_object_unlocks",
            "Horizontal Coin Lines", f"{unlock_level_name} - Horizontal Coin Lines")
        item_names["HORIZONTAL_COIN_RINGS"] = get_unlock_item_name(
            self.options, "coin_object_unlocks",
            "Horizontal Coin Rings", f"{unlock_level_name} - Horizontal Coin Rings")
        item_names["RED_COINS"] = get_unlock_item_name(
            self.options, "coin_object_unlocks",
            "Red Coins", f"{unlock_level_name} - Red Coins")
        item_names["THREE_COIN_BLOCKS"] = get_unlock_item_name(
            self.options, "coin_object_unlocks",
            "3-Coin Blocks", f"{level_name} - 3-Coin Blocks")
        item_names["TEN_COIN_BLOCKS"] = get_unlock_item_name(
            self.options, "coin_object_unlocks",
            "10-Coin Blocks", f"{level_name} - 10-Coin Blocks")
        item_names["BREAKABLE_COIN_BOXES"] = get_unlock_item_name(
            self.options, "coin_object_unlocks",
            "Breakable Coin Boxes", f"{level_name} - Breakable Coin Boxes")
        item_names["WOODEN_POSTS"] = get_unlock_item_name(
            self.options, "coin_object_unlocks",
            "Wooden Posts", f"{level_name} - Wooden Posts")
        item_names["BOWSER_PUZZLE"] = get_unlock_item_name(
            self.options, "coin_object_unlocks",
            "Lethal Lava Land - Bowser Puzzle", "Lethal Lava Land - Bowser Puzzle")
        item_names["BOBOMBS"] = get_unlock_item_name(
            self.options, "enemy_unlocks",
            "Bob-ombs", f"{level_name} - Bob-ombs")
        item_names["KOOPA_TROOPA"] = get_unlock_item_name(
            self.options, "enemy_unlocks",
            "Koopa Troopas",
            f"{level_name} - {'Koopa Troopas' if level_name == 'Tiny-Huge Island' else 'Koopa Troopa'}")
        item_names["WHOMPS"] = get_unlock_item_name(
            self.options, "enemy_unlocks",
            "Whomps", f"{level_name} - Whomps")
        item_names["SPINDRIFTS"] = get_unlock_item_name(
            self.options, "enemy_unlocks",
            "Spindrifts", f"{level_name} - Spindrifts")
        item_names["BIG_BULLY"] = get_unlock_item_name(
            self.options, "enemy_unlocks",
            "Big Bullies",
            "Lethal Lava Land - Big Bullies" if level_name == "Lethal Lava Land"
            else f"{level_name} - Chill Bully")
        item_names["BULLIES"] = get_unlock_item_name(
            self.options, "enemy_unlocks",
            "Bullies", f"{level_name} - Bullies")
        item_names["FLY_GUY"] = get_unlock_item_name(
            self.options, "enemy_unlocks",
            "Fly Guys",
            f"{level_name} - {'Fly Guys' if level_name in {'Shifting Sand Land', 'Tiny-Huge Island'} else 'Fly Guy'}")
        item_names["FIRE_PIRANHA_PLANTS"] = get_unlock_item_name(
            self.options, "enemy_unlocks",
            "Fire Piranha Plants", f"{level_name} - Fire Piranha Plants")
        item_names["EYEROK"] = get_unlock_item_name(
            self.options, "enemy_unlocks",
            "Shifting Sand Land - Eyerok", "Shifting Sand Land - Eyerok")
        item_names["BIG_BOO"] = get_unlock_item_name(
            self.options, "enemy_unlocks",
            "Big Boo's Haunt - Big Boos", "Big Boo's Haunt - Big Boos")
        if level_name == "Shifting Sand Land":
            thwomp_item_name = "Shifting Sand Land - Grindel"
        elif level_name == "Whomp's Fortress":
            thwomp_item_name = "Whomp's Fortress - Thwomps"
        else:
            thwomp_item_name = f"{level_name} - Thwomp"
        item_names["THWOMP"] = get_unlock_item_name(
            self.options, "enemy_unlocks", "Thwomps and Grindels", thwomp_item_name)
        item_names["BOWSER"] = get_unlock_item_name(
            self.options, "enemy_unlocks", "Bowsers", f"{level_name} - Bowser")
        item_names["CHAIN_CHOMP"] = get_unlock_item_name(
            self.options, "enemy_unlocks",
            "Bob-omb Battlefield - Chain Chomp", "Bob-omb Battlefield - Chain Chomp")
        item_names["WIGGLER"] = get_unlock_item_name(
            self.options, "enemy_unlocks",
            "Tiny-Huge Island - Wiggler", "Tiny-Huge Island - Wiggler")
        item_names["TWEESTERS"] = get_unlock_item_name(
            self.options, "enemy_unlocks",
            "Shifting Sand Land - Tweesters", "Shifting Sand Land - Tweesters")
        item_names["HEAVE_HOS"] = get_unlock_item_name(
            self.options, "enemy_unlocks",
            "Heave-Hos",
            f"{level_name} - {'Heave-Ho' if level_name == 'Tick Tock Clock' else 'Heave-Hos'}")
        item_names["BOOS"] = get_unlock_item_name(
            self.options, "enemy_unlocks",
            "Boos", f"{level_name} - Boos")
        item_names["MR_IS"] = get_unlock_item_name(
            self.options, "enemy_unlocks",
            "Mr. Is", f"{level_name} - Mr. Is")
        item_names["MONTY_MOLES"] = get_unlock_item_name(
            self.options, "one_up_unlocks",
            "Monty Moles", f"{level_name} - Monty Moles")
        item_names["FLYING_BOOKENDS"] = get_unlock_item_name(
            self.options, "enemy_unlocks",
            f"{level_name} - Flying Bookends", f"{level_name} - Flying Bookends")
        item_names["JRB_SIGNS"] = HasUnlock("Signs", "Jolly Roger Bay - Signs")
        item_names["BOB_CORKBOXES"] = HasUnlock("Throwable Cork Boxes", "Bob-omb Battlefield - Throwable Cork Boxes")
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
            else:
                per_level_item_name = get_per_level_action_item_name(
                    level_name, action, bool(self.options.combined_castle_and_secret_stage_move_items))
                if per_level_item_name is None:
                    item_names[action] = action
                    continue
                compatible_item_names = get_compatible_per_level_action_item_names(level_name, action)
                item_names[action] = Or(
                    HasUnlock(action, per_level_item_name),
                    *(Has(name) for name in compatible_item_names if name != per_level_item_name),
                )
        return item_names

    def combine_and_clauses(
            self, rule_expr: str, cannon_name: str, cap_item_names: dict[str, str | Rule],
            arbitrary_item_names: dict[str, str | bool],
            action_item_names: dict[str, str | bool]) -> Union[Rule, bool]:
        expressions = rule_expr.split(" & ")
        rules = []
        for expression in expressions:
            and_clause = self.make_rule(
                expression, cannon_name, cap_item_names, arbitrary_item_names, action_item_names)
            if and_clause is False:
                return False
            if and_clause is not True:
                rules.append(and_clause)
        if rules:
            return And(*rules)
        else:
            return True

    def make_rule(
            self, expression: str, cannon_name: str, cap_item_names: dict[str, str | Rule],
            arbitrary_item_names: dict[str, str | bool],
            action_item_names: dict[str, str | bool]) -> Union[Rule, bool]:
        if expression in logic_tricks_by_internal_id:
            option_key, trick_data = logic_tricks_by_internal_id[expression]
            world = self.multiworld.worlds[self.player]
            enabled = getattr(world, expression, False)
            enabled_for_ut = getattr(world, f"{expression}_ut_glitch", False)
            if not enabled and not enabled_for_ut:
                return False
            trick_rule = self.build_rule(
                trick_data.get("rule", ""),
                cannon_name, cap_item_names, arbitrary_item_names, action_item_names)
            if enabled:
                return LogicTrick(option_key, trick_rule)
            return LogicTrick(option_key, trick_rule, ut_glitched=True)
        if '+' in expression:
            tokens = expression.split('+')
            rules = []
            for token in tokens:
                item = self.parse_token(token, cannon_name, cap_item_names, arbitrary_item_names, action_item_names)
                if item is True:
                    continue
                if item is False:
                    return False
                rules.append(item if isinstance(item, Rule) else Has(item))
            if rules:
                return And(*rules)
            else:
                return True
        if '/' in expression:
            tokens = expression.split('/')
            rules = []
            for token in tokens:
                item = self.parse_token(token, cannon_name, cap_item_names, arbitrary_item_names, action_item_names)
                if item is True:
                    return True
                if item is False:
                    continue
                rules.append(item if isinstance(item, Rule) else Has(item))
            if rules:
                return Or(*rules)
            else:
                return False
        if '{{' in expression:
            return CanReachLocation(expression[2:-2])
        if '{' in expression:
            return CanReachRegion(expression[1:-1])
        item = self.parse_token(expression, cannon_name, cap_item_names, arbitrary_item_names, action_item_names)
        if item in (True, False):
            return item
        if isinstance(item, Rule):
            return item
        return Has(item)

    def parse_token(
            self, token: str, cannon_name: str, cap_item_names: dict[str, str | Rule],
            arbitrary_item_names: dict[str, str | bool],
            action_item_names: dict[str, str | bool]) -> Union[str, bool, Rule]:
        if token == "CANN":
            return cannon_name
        if token in self.global_cap_item_name_by_token:
            item = cap_item_names.get(token)
            return item if item is not None else self.global_cap_item_name_by_token[token]
        if token in arbitrary_item_names:
            return arbitrary_item_names[token]
        item = self.token_table.get(token, None)
        if not item:
            raise Exception(f"Invalid token: '{token}'")
        if item in action_item_data_table:
            return action_item_names[item]
        elif item in cap_item_data_table:
            return item
        return item
