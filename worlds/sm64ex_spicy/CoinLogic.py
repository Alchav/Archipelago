from __future__ import annotations

import dataclasses
from collections.abc import Callable
from dataclasses import dataclass
from types import ModuleType

from BaseClasses import CollectionState

from .RuleBuilder import CoinEvaluation, CoinSourceTrace


CoinTraceEvaluator = Callable[[CollectionState, int, int], CoinEvaluation]
RedCoinEvaluator = Callable[[CollectionState, int], bool]


class CoinTraceBuilder:
    def __init__(self) -> None:
        self.reachable_coins = 0
        self.children: list[CoinSourceTrace] = []

    def add(
            self,
            source_id: str,
            label: str,
            coins: int,
            available: bool,
            *,
            counted: bool | None = None,
            children: tuple[CoinSourceTrace, ...] = (),
    ) -> None:
        if counted is None:
            counted = available
        self.children.append(CoinSourceTrace(
            source_id, label, coins, counted, available, children))
        if counted:
            self.reachable_coins += coins

    def add_source(
            self,
            source_id: str,
            label: str,
            coins: int,
            available: bool,
            *,
            counted: bool | None = None,
    ) -> None:
        self.add(source_id, label, coins, available, counted=counted)

    def add_route(
            self,
            route_id: str,
            label: str,
            available: bool,
            sources: tuple[CoinSourceTrace, ...],
            *,
            selected: bool = True,
    ) -> None:
        counted = available and selected
        source_traces = tuple(
            CoinSourceTrace(
                source.source_id,
                source.label,
                source.coins,
                counted and source.available,
                available and source.available,
                source.children,
            )
            for source in sources
        )
        route_coins = sum(
            source.coins for source in sources
            if counted and source.available
        )
        if counted:
            self.reachable_coins += route_coins

        displayed_coins = sum(
            source.coins for source in sources
            if source.available or not available
        )
        self.children.append(CoinSourceTrace(
            route_id,
            label,
            displayed_coins,
            counted,
            available,
            source_traces,
        ))

    def evaluation(self, reachable_coins: int | None = None) -> CoinEvaluation:
        if reachable_coins is None:
            reachable_coins = self.reachable_coins
        return CoinEvaluation(reachable_coins, tuple(self.children))


def _has_red_coins(state: CollectionState, player: int, level_name: str) -> bool:
    from . import Rules

    return Rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Red Coins", f"{level_name} - Red Coins")


def _can_collect_all_bob_red_coins(state: CollectionState, player: int) -> bool:
    from . import Rules

    level = "Bob-omb Battlefield"
    target = f"{level} - Find the 8 Red Coins"
    return (
        _has_red_coins(state, player, level)
        and state.can_reach(f"{level} - Island", "Region", player)
        and (
            any(Rules.has_action(state, player, action, level)
                for action in ("Climb", "Side Flip", "Backflip", "Triple Jump"))
            or Rules.can_use_logic_trick(
                state, player, "logic_bob_island_red_coin_with_ground_pound", target)
            or Rules.can_use_logic_trick(
                state, player, "logic_bob_island_koopa_shell", target)
            or Rules.can_use_logic_trick(
                state, player, "logic_bob_mario_wings_to_the_sky_without_cannon", target)
            or (
                state.has(f"{level} - Cannon Unlock", player)
                and state.can_reach(f"{level} - Mario Wings to the Sky", "Location", player)
            )
        )
    )


def _can_collect_all_wf_red_coins(state: CollectionState, player: int) -> bool:
    from . import Rules

    level = "Whomp's Fortress"
    return (
        _has_red_coins(state, player, level)
        and state.can_reach(f"{level} - Top", "Region", player)
        and Rules.has_unlock(
            state, player, "enemy_unlocks", "Thwomp", f"{level} - Thwomp")
    )


def _can_collect_all_jrb_red_coins(state: CollectionState, player: int) -> bool:
    from . import Rules

    level = "Jolly Roger Bay"
    target = f"{level} - Red Coins on the Ship Afloat"
    pillar = (
        Rules.has_action(state, player, "Climb", level)
        or Rules.can_use_logic_trick(state, player, "logic_jrb_pillar_red_coin_moves", target)
        or Rules.can_use_logic_trick(state, player, "logic_jrb_pillar_red_coin_cannon", target)
    )
    return (
        _has_red_coins(state, player, level)
        and state.can_reach(f"{level} - Upper", "Region", player)
        and Rules.has_per_act_feature(state, player, f"{level} - Raised Ship")
        and pillar
    )


def _red_coins_and_region(
        state: CollectionState, player: int, level: str, region: str | None = None,
) -> bool:
    return (
        _has_red_coins(state, player, level)
        and (region is None or state.can_reach(region, "Region", player))
    )


def _can_collect_all_hmc_red_coins(state: CollectionState, player: int) -> bool:
    from . import Rules

    level = "Hazy Maze Cave"
    return (
        _red_coins_and_region(state, player, level, f"{level} - Red Coin Area")
        and Rules.has_checkerboard_platforms(state, player, level)
    )


def _can_collect_all_lll_red_coins(state: CollectionState, player: int) -> bool:
    from . import Rules

    return (
        _has_red_coins(state, player, "Lethal Lava Land")
        and Rules.can_collect_all_lethal_lava_land_red_coins(
            state, player, "Lethal Lava Land - 8-Coin Puzzle with 15 Pieces")
    )


def _can_collect_all_ssl_red_coins(state: CollectionState, player: int) -> bool:
    from . import Rules

    level = "Shifting Sand Land"
    target = f"{level} - Free Flying for 8 Red Coins"
    normal = (
        Rules.has_wing_cap(state, player, level)
        and (
            Rules.has_action(state, player, "Triple Jump", level)
            or state.has(f"{level} - Cannon Unlock", player)
        )
    )
    trick = (
        Rules.can_use_logic_trick(
            state, player, "logic_ssl_three_red_coins_with_tweesters", target)
        and Rules.can_use_logic_trick(
            state, player, "logic_ssl_one_red_coin_with_shy_guy_spin_jump", target)
        and bool(state.multiworld.worlds[player].options.no_despawns.value)
    )
    return _has_red_coins(state, player, level) and (normal or trick)


def _can_collect_all_ddd_red_coins(state: CollectionState, player: int) -> bool:
    from . import Rules

    level = "Dire, Dire Docks"
    poles = (
        Rules.has_per_act_feature(state, player, f"{level} - Poles")
        and Rules.has_action(state, player, "Climb", level)
    )
    first = (
        Rules.has_purple_switches(state, player, level)
        or (
            Rules.has_per_act_feature(state, player, f"{level} - Bowser's Sub")
            and poles
            and Rules.has_action(state, player, "Triple Jump", level)
        )
    )
    return _has_red_coins(state, player, level) and first and poles


def _can_collect_all_wdw_red_coins(state: CollectionState, player: int) -> bool:
    from . import Rules

    level = "Wet-Dry World"
    return (
        _red_coins_and_region(state, player, level, f"{level} - Downtown")
        and Rules.has_simple_arbitrary_feature(
            state, player, "WDW_WATER_LEVEL_DIAMOND")
        and (
            Rules.has_action(state, player, "Wall Kick", level)
            or Rules.can_use_logic_trick(
                state, player, "logic_wdw_high_red_coins_triple_jump",
                f"{level} - Go to Town for Red Coins")
        )
    )


def _can_collect_all_thi_red_coins(state: CollectionState, player: int) -> bool:
    from . import Rules

    level = "Tiny-Huge Island"
    return (
        _red_coins_and_region(state, player, level, f"{level} - Red Coins Area")
        and Rules.has_action(state, player, "Wall Kick", level)
    )


def _can_collect_all_ttc_red_coins(state: CollectionState, player: int) -> bool:
    from . import Rules

    return (
        _red_coins_and_region(
            state, player, "Tick Tock Clock",
            "Tick Tock Clock - First Clock Hand Area")
        and Rules.has_simple_arbitrary_feature(state, player, "TTC_SPINNERS")
    )


def _can_collect_all_rr_red_coins(state: CollectionState, player: int) -> bool:
    from . import Rules

    level = "Rainbow Ride"
    target = f"{level} - Coins Amassed in a Maze"
    route = (
        Rules.has_action(state, player, "Wall Kick", level)
        or (
            Rules.has_action(state, player, "Long Jump", level)
            and any(Rules.has_action(state, player, action, level)
                    for action in ("Side Flip", "Backflip", "Triple Jump"))
        )
        or Rules.can_use_logic_trick(
            state, player, "logic_rr_maze_coins_ledge_grab_and_carpets", target)
    )
    return (
        _red_coins_and_region(state, player, level, f"{level} - Maze")
        and route
    )


def _can_collect_all_wmotr_red_coins(state: CollectionState, player: int) -> bool:
    from . import Rules

    level = "Wing Mario Over the Rainbow"
    cannon = state.can_reach(f"{level} - Cannon", "Region", player)
    flight = (
        cannon
        or (
            Rules.has_wing_cap(state, player, level)
            and Rules.has_action(state, player, "Triple Jump", level)
        )
    )
    return _has_red_coins(state, player, level) and cannon and flight


def _can_collect_all_vcutm_red_coins(state: CollectionState, player: int) -> bool:
    from . import Rules

    level = "Vanish Cap Under the Moat"
    target = f"{level} - Red Coins"
    combines_routes = (
        any(Rules.has_action(state, player, action, level)
            for action in ("Triple Jump", "Ledge Grab", "Side Flip", "Backflip", "Wall Kick"))
        or Rules.can_use_logic_trick(
            state, player,
            "logic_vcutm_drop_to_checkerboard_platforms_after_crawling_back_up", target)
    )
    can_cross_grate = (
        Rules.has_vanish_cap(state, player, level)
        or Rules.can_use_logic_trick(
            state, player, "logic_vcutm_wall_kick_over_vanish_cap_grate", target)
    )
    return (
        _has_red_coins(state, player, level)
        and Rules.has_checkerboard_platforms(state, player, level)
        and combines_routes
        and can_cross_grate
    )


def _can_collect_all_cotmc_red_coins(state: CollectionState, player: int) -> bool:
    from . import Rules

    level = "Cavern of the Metal Cap"
    return (
        _has_red_coins(state, player, level)
        and (
            Rules.has_metal_cap(state, player, level)
            or Rules.can_use_logic_trick(
                state, player, "logic_cotmc_deep_underwater_coins_without_metal_cap",
                f"{level} - Red Coins")
        )
    )


def _can_collect_all_bitdw_red_coins(state: CollectionState, player: int) -> bool:
    from . import Rules

    level = "Bowser in the Dark World"
    return (
        _has_red_coins(state, player, level)
        and Rules.has_purple_switches(state, player, level)
    )


def _can_collect_all_bitfs_red_coins(state: CollectionState, player: int) -> bool:
    level = "Bowser in the Fire Sea"
    return _red_coins_and_region(state, player, level, f"{level} - Upper")


def coin_source(
        source_id: str,
        label: str,
        coins: int,
        available: bool,
        *,
        counted: bool | None = None,
        children: tuple[CoinSourceTrace, ...] = (),
) -> CoinSourceTrace:
    if counted is None:
        counted = available
    return CoinSourceTrace(source_id, label, coins, counted, available, children)


def coin_route(
        source_id: str,
        label: str,
        available: bool,
        selected: bool,
        children: tuple[CoinSourceTrace, ...],
) -> CoinSourceTrace:
    route_coins = sum(
        child.coins
        for child in children
        if (child.counted if selected else child.available)
    )
    return coin_source(
        source_id,
        label,
        route_coins,
        available,
        counted=available and selected,
        children=children,
    )


def coin_evaluation(
        traces: list[CoinSourceTrace],
        maximum: int,
) -> CoinEvaluation:
    reachable_coins = sum(trace.coins for trace in traces if trace.counted)
    assert reachable_coins <= maximum
    return CoinEvaluation(reachable_coins, tuple(traces))


def evaluate_bob_omb_battlefield_coins(
        state: CollectionState,
        player: int,
        _required_coins: int,
) -> CoinEvaluation:
    from . import Rules

    level_name = "Bob-omb Battlefield"
    target_name = f"{level_name} - Coins Star"
    has_cannon = state.has(f"{level_name} - Cannon Unlock", player)
    has_single_yellow_coins = Rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Single Yellow Coins", f"{level_name} - Single Yellow Coins")
    has_red_coins = Rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Red Coins", f"{level_name} - Red Coins")
    has_horizontal_coin_lines = Rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Horizontal Coin Lines", f"{level_name} - Horizontal Coin Lines")
    has_horizontal_coin_rings = Rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Horizontal Coin Rings", f"{level_name} - Horizontal Coin Rings")
    has_vertical_coin_rings = Rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Vertical Coin Rings", f"{level_name} - Vertical Coin Rings")
    has_breakable_coin_box = Rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Breakable Coin Boxes", f"{level_name} - Breakable Coin Box")
    has_throwable_cork_boxes = Rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Throwable Cork Boxes", f"{level_name} - Throwable Cork Boxes")
    has_wooden_posts = Rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Wooden Posts", f"{level_name} - Wooden Posts")
    has_bob_ombs = Rules.has_unlock(
        state, player, "enemy_unlocks",
        "Bob-ombs", f"{level_name} - Bob-ombs")
    has_goombas = Rules.has_unlock(
        state, player, "enemy_unlocks",
        "Goombas", f"{level_name} - Goombas")
    has_koopa_troopa = Rules.has_unlock(
        state, player, "enemy_unlocks",
        "Koopa Troopas", f"{level_name} - Koopa Troopa")

    traces = [
        coin_source("start_breakable_coin_box", "Large breakable coin box near the start", 3,
                has_breakable_coin_box),
        coin_source("start_throwable_cork_boxes", "Two throwable cork boxes near the start", 6,
                has_throwable_cork_boxes),
        coin_source("main_horizontal_coin_lines", "Three horizontal coin lines", 15,
                has_horizontal_coin_lines),
        coin_source("main_wooden_posts", "Five wooden posts", 25, has_wooden_posts),
        coin_source("flowerbed_coin_ring", "Coin ring around the flowerbed", 8,
                has_horizontal_coin_rings),
        coin_source("main_bob_ombs", "Twelve Bob-ombs", 12, has_bob_ombs),
        coin_source("main_goombas", "Eleven Goombas", 11, has_goombas),
        coin_source("main_red_coins", "Seven Red Coins outside the island", 14, has_red_coins),
        coin_source("main_koopa_troopa", "Koopa Troopa", 5, has_koopa_troopa),
    ]

    has_island = state.can_reach(f"{level_name} - Island", "Region", player)
    traces.append(coin_source(
        "island_first_ring_easy_coins",
        "First three coins from the island's first vertical ring",
        3,
        has_island and has_vertical_coin_rings,
    ))

    has_full_trick_route = has_island and Rules.can_use_logic_trick(
        state, player, "logic_bob_mario_wings_to_the_sky_without_cannon", target_name)
    has_cannon_route = (
        has_island
        and has_cannon
        and state.can_reach(f"{level_name} - Mario Wings to the Sky", "Location", player)
    )
    selected_route = (
        "without_cannon" if has_full_trick_route
        else "cannon" if has_cannon_route
        else "partial"
    )

    full_trick_children = (
        coin_source(
            "island_full_trick_vertical_ring_coins",
            "Remaining vertical-ring coins above the island",
            37,
            has_full_trick_route and has_vertical_coin_rings,
            counted=selected_route == "without_cannon" and has_full_trick_route and has_vertical_coin_rings,
        ),
        coin_source(
            "island_full_trick_ring_center_coins",
            "Yellow coins in the centers of the island rings",
            5,
            has_full_trick_route and has_single_yellow_coins,
            counted=selected_route == "without_cannon" and has_full_trick_route and has_single_yellow_coins,
        ),
        coin_source(
            "island_full_trick_red_coin",
            "Island Red Coin",
            2,
            has_full_trick_route and has_red_coins,
            counted=selected_route == "without_cannon" and has_full_trick_route and has_red_coins,
        ),
    )
    traces.append(coin_route(
        "island_without_cannon_route",
        "Mario Wings to the Sky without Cannon route",
        has_full_trick_route,
        selected_route == "without_cannon",
        full_trick_children,
    ))

    cannon_children = (
        coin_source(
            "island_cannon_vertical_ring_coins",
            "Remaining vertical-ring coins reached with the cannon",
            37,
            has_cannon_route and has_vertical_coin_rings,
            counted=selected_route == "cannon" and has_cannon_route and has_vertical_coin_rings,
        ),
        coin_source(
            "island_cannon_ring_center_coins",
            "Yellow coins in the centers of the island rings",
            5,
            has_cannon_route and has_single_yellow_coins,
            counted=selected_route == "cannon" and has_cannon_route and has_single_yellow_coins,
        ),
        coin_source(
            "island_cannon_red_coin",
            "Island Red Coin reached while flying from the cannon",
            2,
            has_cannon_route and has_red_coins,
            counted=selected_route == "cannon" and has_cannon_route and has_red_coins,
        ),
    )
    traces.append(coin_route(
        "island_cannon_route",
        "Mario Wings to the Sky cannon route",
        has_cannon_route,
        selected_route == "cannon",
        cannon_children,
    ))

    has_island_red_coin_movement = any(
        Rules.has_action(state, player, action, level_name)
        for action in ("Climb", "Side Flip", "Backflip", "Triple Jump")
    )
    has_island_red_coin_ground_pound = Rules.can_use_logic_trick(
        state, player, "logic_bob_island_red_coin_with_ground_pound", target_name)
    has_island_koopa_shell = Rules.can_use_logic_trick(
        state, player, "logic_bob_island_koopa_shell", target_name)
    has_first_ring_jump = any(
        Rules.has_action(state, player, action, level_name)
        for action in ("Side Flip", "Backflip", "Triple Jump")
    )
    has_wing_cap_flight = (
        Rules.has_wing_cap(state, player, level_name)
        and Rules.has_action(state, player, "Triple Jump", level_name)
    )
    partial_route_available = has_island and selected_route == "partial"
    partial_children = (
        coin_source(
            "island_partial_flight_ring_coins",
            "Four complete vertical rings reached with Wing Cap and Triple Jump",
            32,
            partial_route_available and has_wing_cap_flight and has_vertical_coin_rings,
        ),
        coin_source(
            "island_partial_flight_center_coins",
            "Four ring-center coins reached with Wing Cap and Triple Jump",
            4,
            partial_route_available and has_wing_cap_flight and has_single_yellow_coins,
        ),
        coin_source(
            "island_partial_red_coin",
            "Island Red Coin reached with movement, Ground Pound trick, or Koopa Shell trick",
            2,
            partial_route_available and has_red_coins and (
                has_island_red_coin_movement
                or has_island_red_coin_ground_pound
                or has_island_koopa_shell
            ),
        ),
        coin_source(
            "island_partial_first_ring_three_coins",
            "Three additional first-ring coins reached by jumping",
            3,
            partial_route_available and has_vertical_coin_rings and (
                has_first_ring_jump or has_island_red_coin_ground_pound
            ),
        ),
        coin_source(
            "island_partial_first_ring_two_coins",
            "Two additional first-ring coins requiring a movement jump",
            2,
            partial_route_available and has_vertical_coin_rings and has_first_ring_jump,
        ),
        coin_source(
            "island_partial_triple_jump_coin",
            "Single island coin reached with Triple Jump",
            1,
            partial_route_available and has_single_yellow_coins
            and Rules.has_action(state, player, "Triple Jump", level_name),
        ),
    )
    traces.append(coin_route(
        "island_partial_route",
        "Partial island coin routes",
        has_island,
        selected_route == "partial" and has_island,
        partial_children,
    ))
    return coin_evaluation(traces, 146)


def evaluate_whomps_fortress_coins(
        state: CollectionState,
        player: int,
        _required_coins: int,
) -> CoinEvaluation:
    from . import Rules

    level_name = "Whomp's Fortress"
    target_name = f"{level_name} - Coins Star"
    has_single_yellow_coins = Rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Single Yellow Coins", f"{level_name} - Single Yellow Coins")
    has_red_coins = Rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Red Coins", f"{level_name} - Red Coins")
    has_blue_coin_block = Rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Blue Coin Blocks", f"{level_name} - Blue Coin Block")
    has_horizontal_coin_lines = Rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Horizontal Coin Lines", f"{level_name} - Horizontal Coin Lines")
    has_horizontal_coin_rings = Rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Horizontal Coin Rings", f"{level_name} - Horizontal Coin Rings")
    has_coin_arrows = Rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Coin Arrows", f"{level_name} - Coin Arrows")
    has_throwable_cork_boxes = Rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Throwable Cork Boxes", f"{level_name} - Throwable Cork Boxes")
    has_piranha_plants = Rules.has_unlock(
        state, player, "enemy_unlocks",
        f"{level_name} - Piranha Plants", f"{level_name} - Piranha Plants")
    has_whomps = Rules.has_unlock(
        state, player, "enemy_unlocks",
        "Whomps", f"{level_name} - Whomps")
    has_thwomp = Rules.has_unlock(
        state, player, "enemy_unlocks",
        "Thwomp", f"{level_name} - Thwomp")

    traces = [
        coin_source("start_throwable_cork_boxes", "Two throwable cork boxes", 6,
                has_throwable_cork_boxes),
        coin_source("start_flower_coin_ring", "Coin ring around the starting flower", 8,
                has_horizontal_coin_rings),
        coin_source("start_coin_line", "Coin line near the beginning", 5,
                has_horizontal_coin_lines),
        coin_source("falling_bridge_coin_line", "Coin line past the falling bridge", 5,
                has_horizontal_coin_lines),
        coin_source("rotating_plank_coins", "Coins around the rotating plank", 4,
                has_single_yellow_coins),
        coin_source("water_slope_coin_line", "Coin line on the slope from the water", 5,
                has_horizontal_coin_lines),
        coin_source("water_coin_ring", "Coin ring in the water", 8, has_horizontal_coin_rings),
        coin_source("buddy_coin_line", "Coin line near the Bob-omb Buddy", 5,
                has_horizontal_coin_lines),
        coin_source("whomp_jump_coins", "Coins from jumping on two Whomps", 10, has_whomps),
        coin_source("piranha_plant_coins", "Three Piranha Plants", 15, has_piranha_plants),
        coin_source("initial_red_coins", "Five initially reachable Red Coins", 10, has_red_coins),
        coin_source("thwomp_red_coin", "Red Coin on the Thwomp", 2,
                has_red_coins and has_thwomp),
    ]

    has_moveless_wild_blue_route = (
        Rules.can_use_logic_trick(
            state, player, "logic_wf_into_the_wild_blue_yonder_moveless", target_name)
        and (
            Rules.has_action(state, player, "Climb", level_name)
            or Rules.has_action(state, player, "Side Flip", level_name)
            or (
                Rules.has_action(state, player, "Triple Jump", level_name)
                and Rules.has_action(state, player, "Ledge Grab", level_name)
            )
        )
    )
    can_reach_wild_blue_coins = (
        state.has(f"{level_name} - Cannon Unlock", player)
        or Rules.can_use_logic_trick(
            state, player, "logic_wf_into_the_wild_blue_yonder_wall_kick", target_name)
        or Rules.can_use_logic_trick(
            state, player, "logic_wf_into_the_wild_blue_yonder_long_jump", target_name)
        or has_moveless_wild_blue_route
    )
    wild_blue_children = (
        coin_source(
            "wild_blue_coin_ring",
            "Coin ring above Shoot into the Wild Blue",
            8,
            can_reach_wild_blue_coins and has_horizontal_coin_rings,
        ),
    )
    traces.append(coin_route(
        "wild_blue_route",
        "Shoot into the Wild Blue coin route",
        can_reach_wild_blue_coins,
        can_reach_wild_blue_coins,
        wild_blue_children,
    ))

    has_ground_pound = Rules.has_action(state, player, "Ground Pound", level_name)
    ground_pound_children = (
        coin_source("whomp_ground_pound_coins", "Ground Pound bonus from two Whomps", 10,
                has_ground_pound and has_whomps),
        coin_source("blue_coin_block", "Blue Coin Block", 20,
                has_ground_pound and has_blue_coin_block),
    )
    traces.append(coin_route(
        "ground_pound_sources",
        "Ground Pound coin sources",
        has_ground_pound,
        has_ground_pound,
        ground_pound_children,
    ))

    has_top = state.can_reach(f"{level_name} - Top", "Region", player)
    top_children = (
        coin_source("top_floating_isle_ring", "Coin ring on the floating isle", 8,
                has_top and has_horizontal_coin_rings),
        coin_source("top_floating_arrow", "Coin arrow above the fortress", 8,
                has_top and has_coin_arrows),
        coin_source("top_red_coins", "Two Red Coins at the top", 4,
                has_top and has_red_coins),
    )
    traces.append(coin_route(
        "top_region_sources",
        "Whomp's Fortress Top sources",
        has_top,
        has_top,
        top_children,
    ))
    return coin_evaluation(traces, 141)


def evaluate_jolly_roger_bay_coins(
        state: CollectionState,
        player: int,
        _required_coins: int,
) -> CoinEvaluation:
    from . import Rules

    level_name = "Jolly Roger Bay"
    target_name = f"{level_name} - Coins Star"
    has_red_coins = Rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Red Coins", f"{level_name} - Red Coins")
    has_blue_coin_block = Rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Blue Coin Blocks", f"{level_name} - Blue Coin Block")
    has_horizontal_coin_lines = Rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Horizontal Coin Lines", f"{level_name} - Horizontal Coin Lines")
    has_horizontal_coin_rings = Rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Horizontal Coin Rings", f"{level_name} - Horizontal Coin Rings")
    has_vertical_coin_lines = Rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Vertical Coin Lines", f"{level_name} - Vertical Coin Lines")
    has_vertical_coin_rings = Rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Vertical Coin Rings", f"{level_name} - Vertical Coin Rings")
    has_three_coin_block = Rules.has_unlock(
        state, player, "coin_object_unlocks",
        "3-Coin Blocks", f"{level_name} - 3-Coin Block")
    has_goombas = Rules.has_unlock(
        state, player, "enemy_unlocks",
        "Goombas", f"{level_name} - Goombas")
    has_pillar_red_coin_moves = Rules.can_use_logic_trick(
        state, player, "logic_jrb_pillar_red_coin_moves", target_name)
    has_pillar_red_coin_cannon = Rules.can_use_logic_trick(
        state, player, "logic_jrb_pillar_red_coin_cannon", target_name)
    has_upper = state.can_reach(f"{level_name} - Upper", "Region", player)
    has_raised_ship = Rules.has_per_act_feature(
        state, player, f"{level_name} - Raised Ship")

    traces = [
        coin_source("start_three_coin_block", "Three-Coin Block near the start", 3,
                has_three_coin_block),
        coin_source("clam_vertical_coin_ring", "Vertical coin ring near the clams", 8,
                has_vertical_coin_rings),
        coin_source("tall_spike_coin_ring", "Coin ring around the tall spike", 8,
                has_horizontal_coin_rings),
        coin_source("purple_switch_lower_coin_line", "Lower part of the Purple Switch coin line", 3,
                has_vertical_coin_lines),
        coin_source("jet_stream_coin_ring", "Coin ring near the jet stream", 8,
                has_horizontal_coin_rings),
        coin_source("cave_chest_coin_ring", "Coin ring near the cave treasure chests", 8,
                has_horizontal_coin_rings),
        coin_source("main_goombas", "Three Goombas", 3, has_goombas),
        coin_source("lower_red_coins", "Four initially reachable Red Coins", 8, has_red_coins),
    ]

    has_pillar_route = (
        Rules.has_action(state, player, "Climb", level_name)
        or has_pillar_red_coin_moves
        or has_pillar_red_coin_cannon
    )
    pillar_children = (
        coin_source("pillar_red_coin", "Red Coin on the stone pillar", 2,
                has_pillar_route and has_red_coins),
    )
    traces.append(coin_route(
        "pillar_red_coin_route",
        "Stone pillar Red Coin route",
        has_pillar_route,
        has_pillar_route,
        pillar_children,
    ))

    has_ship_red_coin_alternative = (
        Rules.can_use_logic_trick(
            state, player, "logic_jrb_ship_red_coin_with_long_jump", target_name)
        or Rules.has_purple_switches(state, player, level_name)
    )
    upper_children = (
        coin_source(
            "purple_switch_upper_coin_line",
            "Upper part of the Purple Switch coin line",
            2,
            has_upper and has_vertical_coin_lines,
        ),
        coin_source(
            "raised_ship_approach_coin_lines",
            "Coin lines leading to the raised ship",
            15,
            has_upper and has_horizontal_coin_lines,
        ),
        coin_source(
            "raised_ship_red_coins",
            "Three Red Coins on the raised ship",
            6,
            has_upper and has_red_coins and has_raised_ship,
        ),
        coin_source(
            "ship_alternative_red_coin",
            "Single ship Red Coin reached without raising the ship",
            2,
            has_upper and has_red_coins and not has_raised_ship
            and has_ship_red_coin_alternative,
        ),
    )
    traces.append(coin_route(
        "upper_region_sources",
        "Jolly Roger Bay Upper sources",
        has_upper,
        has_upper,
        upper_children,
    ))

    has_ground_pound = Rules.has_action(state, player, "Ground Pound", level_name)
    traces.append(coin_source(
        "blue_coin_block",
        "Blue Coin Block",
        30,
        has_blue_coin_block and has_ground_pound,
    ))
    return coin_evaluation(traces, 104)


def evaluate_cool_cool_mountain_coins(
        state: CollectionState,
        player: int,
        _required_coins: int,
) -> CoinEvaluation:
    from . import Rules

    level_name = "Cool, Cool Mountain"
    target_name = f"{level_name} - Coins Star"
    has_single_yellow_coins = Rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Single Yellow Coins", f"{level_name} - Single Yellow Coins")
    has_red_coins = Rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Red Coins", f"{level_name} - Red Coins")
    has_single_blue_coin = Rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Single Blue Coins", f"{level_name} - Single Blue Coin")
    has_blue_coin_block = Rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Blue Coin Blocks", f"{level_name} - Blue Coin Block")
    has_horizontal_coin_lines = Rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Horizontal Coin Lines", f"{level_name} - Horizontal Coin Lines")
    has_coin_arrows = Rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Coin Arrows", f"{level_name} - Coin Arrows")
    has_vertical_coin_lines = Rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Vertical Coin Lines", f"{level_name} - Vertical Coin Lines")
    has_mr_blizzards = Rules.has_unlock(
        state, player, "enemy_unlocks",
        "Mr Blizzards", f"{level_name} - Mr Blizzards")
    has_spindrifts = Rules.has_unlock(
        state, player, "enemy_unlocks",
        "Spindrifts", f"{level_name} - Spindrifts")

    traces = [
        coin_source("penguin_slide_yellow_coins", "Individual coins on the Penguin Slide", 27,
                has_single_yellow_coins),
        coin_source("penguin_slide_coin_lines", "Nine coin lines on the Penguin Slide", 45,
                has_horizontal_coin_lines),
        coin_source("chimney_vertical_coin_line", "Vertical coin line into the chimney", 5,
                has_vertical_coin_lines),
        coin_source("main_mountain_coin_lines", "Four coin lines on the main mountain route", 20,
                has_horizontal_coin_lines),
        coin_source("standard_mr_blizzard", "Defeatable Mr. Blizzard", 3, has_mr_blizzards),
        coin_source("main_spindrifts", "Three Spindrifts on the main route", 9, has_spindrifts),
        coin_source("red_coins", "Eight Red Coins", 16, has_red_coins),
        coin_source("slide_blue_coin", "Blue Coin at the start of the slide", 5,
                has_single_blue_coin),
    ]

    has_cannon = state.has(f"{level_name} - Cannon Unlock", player)
    has_spin_jump_route = Rules.can_use_logic_trick(
        state, player, "logic_ccm_wall_kicks_will_work_spin_jump", target_name)
    has_wall_kicks_route = has_cannon or has_spin_jump_route
    route_children: list[CoinSourceTrace] = [
        coin_source(
            "wall_kicks_coin_arrow",
            "Coin arrow near Wall Kicks Will Work",
            8,
            has_wall_kicks_route and has_coin_arrows,
        ),
        coin_source(
            "wall_kicks_spindrifts",
            "Two Spindrifts near Wall Kicks Will Work",
            6,
            has_wall_kicks_route and has_spindrifts,
        ),
    ]
    route_total = sum(child.coins for child in route_children if child.counted)
    loses_spindrift_coins = (
        has_wall_kicks_route
        and has_spindrifts
        and not has_cannon
        and not Rules.permanent_coin_collection_enabled(state, player)
    )
    if loses_spindrift_coins:
        route_total -= 3
        route_children.append(coin_source(
            "wall_kicks_spindrift_route_loss",
            "Three Spindrift coins left behind when using the Spin Jump route",
            3,
            False,
            counted=False,
        ))
    traces.append(coin_source(
        "wall_kicks_route",
        "Wall Kicks Will Work coin route"
        + (" after its three-coin route loss" if loses_spindrift_coins else ""),
        route_total,
        has_wall_kicks_route,
        counted=has_wall_kicks_route,
        children=tuple(route_children),
    ))

    has_ground_pound = Rules.has_action(state, player, "Ground Pound", level_name)
    traces.append(coin_source(
        "blue_coin_block",
        "Blue Coin Block",
        10,
        has_blue_coin_block and has_ground_pound,
    ))
    return coin_evaluation(traces, 154)


def evaluate_big_boos_haunt_coins(
        state: CollectionState,
        player: int,
        _required_coins: int,
) -> CoinEvaluation:
    from . import Rules

    level_name = "Big Boo's Haunt"
    target_name = f"{level_name} - Coins Star"
    has_red_coins = Rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Red Coins", f"{level_name} - Red Coins")
    has_blue_coin_block = Rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Blue Coin Blocks", f"{level_name} - Blue Coin Block")
    has_breakable_coin_boxes = Rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Breakable Coin Boxes", f"{level_name} - Breakable Coin Boxes")
    has_crazy_box = Rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Crazy Boxes", f"{level_name} - Crazy Box")
    has_ten_coin_block = Rules.has_unlock(
        state, player, "coin_object_unlocks",
        "10-Coin Blocks", f"{level_name} - 10-Coin Block")
    has_boos = Rules.has_unlock(
        state, player, "enemy_unlocks",
        "Boos", f"{level_name} - Boos")
    has_flying_bookends = Rules.has_unlock(
        state, player, "enemy_unlocks",
        f"{level_name} - Flying Bookends", f"{level_name} - Flying Bookends")
    has_mr_is = Rules.has_unlock(
        state, player, "enemy_unlocks",
        "Mr. Is", f"{level_name} - Mr. Is")
    has_scuttlebugs = Rules.has_unlock(
        state, player, "enemy_unlocks",
        "Scuttlebugs", f"{level_name} - Scuttlebugs")
    has_normal_third_floor_route = (
        Rules.has_action(state, player, "Wall Kick", level_name)
        and Rules.has_action(state, player, "Ledge Grab", level_name)
    )
    has_wall_kick_third_floor_trick = Rules.can_use_logic_trick(
        state, player, "logic_bbh_third_floor_wall_kick", target_name)
    has_bookend_third_floor_trick = Rules.can_use_logic_trick(
        state, player, "logic_bbh_third_floor_side_flip", target_name)

    traces = [
        coin_source("mansion_ten_coin_block", "Ten-Coin Block behind the mansion", 10,
                has_ten_coin_block),
        coin_source("shed_breakable_coin_boxes", "Two breakable coin boxes near the shed", 6,
                has_breakable_coin_boxes),
        coin_source("outside_crazy_box", "Crazy Box outside the mansion", 5, has_crazy_box),
        coin_source("outside_scuttlebugs", "Three Scuttlebugs outside", 9, has_scuttlebugs),
        coin_source("main_boos", "Five Boos in the mansion", 25, has_boos),
        coin_source("main_mr_is", "Two Mr. Is", 10, has_mr_is),
        coin_source("main_bookend", "Flying Bookend on the first floor", 5,
                has_flying_bookends),
        coin_source("first_floor_red_coins", "Four first-floor Red Coins", 8, has_red_coins),
    ]

    has_second_floor = state.can_reach(f"{level_name} - Second Floor", "Region", player)
    second_floor_children = (
        coin_source("second_floor_bookends", "Two Flying Bookends on the second floor", 10,
                has_second_floor and has_flying_bookends),
        coin_source("second_floor_mr_i", "Mr. I on the second floor", 5,
                has_second_floor and has_mr_is),
        coin_source("second_floor_red_coins", "Four second-floor Red Coins", 8,
                has_second_floor and has_red_coins),
    )
    traces.append(coin_route(
        "second_floor_sources",
        "Big Boo's Haunt Second Floor sources",
        has_second_floor,
        has_second_floor,
        second_floor_children,
    ))

    has_third_floor = state.can_reach(f"{level_name} - Third Floor", "Region", player)
    third_floor_children: list[CoinSourceTrace] = [
        coin_source(
            "third_floor_boo",
            "Boo behind the third-floor Vanish Cap barrier",
            5,
            has_third_floor and has_boos,
        ),
        coin_source(
            "attic_blue_coin_block",
            "Blue Coin Block in the attic",
            20,
            has_third_floor and has_blue_coin_block
            and Rules.has_action(state, player, "Ground Pound", level_name),
        ),
    ]
    third_floor_total = sum(child.coins for child in third_floor_children if child.counted)
    loses_bookend_coins = (
        has_third_floor
        and has_flying_bookends
        and has_bookend_third_floor_trick
        and not has_normal_third_floor_route
        and not has_wall_kick_third_floor_trick
        and not state.multiworld.worlds[player].options.no_despawns.value
        and not Rules.permanent_coin_collection_enabled(state, player)
    )
    if loses_bookend_coins:
        lost_coins = min(10, third_floor_total)
        third_floor_total -= lost_coins
        third_floor_children.append(coin_source(
            "bookend_third_floor_route_loss",
            "Third-floor coins offset by Bookend coins left behind below",
            lost_coins,
            False,
            counted=False,
        ))
    traces.append(coin_source(
        "third_floor_sources",
        "Big Boo's Haunt Third Floor sources"
        + (" after the Bookend route loss" if loses_bookend_coins else ""),
        third_floor_total,
        has_third_floor,
        counted=has_third_floor,
        children=tuple(third_floor_children),
    ))

    traces.append(coin_source(
        "merry_go_round_boos",
        "Five Merry-Go-Round Boos",
        25,
        has_boos and Rules.has_per_act_feature(
            state, player, f"{level_name} - Merry-go-round"),
    ))
    return coin_evaluation(traces, 151)


def evaluate_hazy_maze_cave_coins(
        state: CollectionState,
        player: int,
        _required_coins: int,
) -> CoinEvaluation:
    from . import Rules

    level_name = "Hazy Maze Cave"
    has_single_yellow_coins = Rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Single Yellow Coins", f"{level_name} - Single Yellow Coins")
    has_red_coins = Rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Red Coins", f"{level_name} - Red Coins")
    has_blue_coin_block = Rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Blue Coin Blocks", f"{level_name} - Blue Coin Block")
    has_horizontal_coin_lines = Rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Horizontal Coin Lines", f"{level_name} - Horizontal Coin Lines")
    has_horizontal_coin_rings = Rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Horizontal Coin Rings", f"{level_name} - Horizontal Coin Rings")
    has_mr_is = Rules.has_unlock(
        state, player, "enemy_unlocks",
        "Mr. Is", f"{level_name} - Mr. Is")
    has_scuttlebugs = Rules.has_unlock(
        state, player, "enemy_unlocks",
        "Scuttlebugs", f"{level_name} - Scuttlebugs")
    has_snufits = Rules.has_unlock(
        state, player, "enemy_unlocks",
        "Snufits", f"{level_name} - Snufits")
    has_swoops = Rules.has_unlock(
        state, player, "enemy_unlocks",
        "Swoops", f"{level_name} - Swoops")
    has_basic_movement = any(
        Rules.has_action(state, player, action, level_name)
        for action in ("Wall Kick", "Ledge Grab", "Backflip", "Side Flip", "Triple Jump")
    )
    has_long_jump = Rules.has_action(state, player, "Long Jump", level_name)
    has_climb = Rules.has_action(state, player, "Climb", level_name)
    has_checkerboards = Rules.has_checkerboard_platforms(state, player, level_name)
    has_platform_route = has_basic_movement and (
        has_basic_movement and has_climb
        or Rules.can_use_logic_trick(
            state, player, "logic_hmc_upper_red_coin_area_wall_kick", level_name)
    )

    traces = [
        coin_source("start_coin_line", "Coin line right of the start", 5,
                has_horizontal_coin_lines),
        coin_source("maze_entrance_coin_line", "Coin line before the maze", 5,
                has_horizontal_coin_lines),
        coin_source("rolling_rocks_coins", "Coins beside the rolling rocks", 5,
                has_single_yellow_coins),
        coin_source("lake_approach_coin_ring", "Coin ring before the underground lake", 8,
                has_horizontal_coin_rings),
        coin_source("first_room_scuttlebugs", "Two Scuttlebugs in the first room", 6,
                has_scuttlebugs),
        coin_source("pit_room_scuttlebug", "Scuttlebug in the pit room", 3, has_scuttlebugs),
        coin_source("pit_room_swoop", "Swoop in the pit room", 1, has_swoops),
        coin_source("red_coin_room_scuttlebugs", "Two Scuttlebugs in the Red Coin room", 6,
                has_scuttlebugs),
        coin_source("toxic_maze_snufits", "Four Snufits in the toxic maze", 8, has_snufits),
        coin_source("toxic_maze_swoops", "Four Swoops in the toxic maze", 4, has_swoops),
    ]

    basic_movement_children = (
        coin_source("lower_red_coin_room_coins", "Four lower Red Coins in the Red Coin room", 8,
                has_basic_movement and has_red_coins),
        coin_source("red_coin_room_mr_is", "Two Mr. Is in the Red Coin room", 10,
                has_basic_movement and has_mr_is),
        coin_source("pit_island_room_swoops", "Two Swoops in the Pit Island elevator room", 2,
                has_basic_movement and has_swoops),
    )
    traces.append(coin_route(
        "basic_movement_sources",
        "Sources reached with basic vertical movement",
        has_basic_movement,
        has_basic_movement,
        basic_movement_children,
    ))

    first_upper_red_coin_route = (
        has_red_coins and has_platform_route and (has_long_jump or has_checkerboards)
    )
    traces.append(coin_source(
        "upper_red_coin_pair_first",
        "First pair of upper Red Coins",
        4,
        first_upper_red_coin_route,
    ))
    traces.append(coin_source(
        "upper_red_coin_pair_checkerboards",
        "Second pair of upper Red Coins",
        4,
        has_red_coins and has_platform_route and has_checkerboards,
    ))
    traces.append(coin_source(
        "upper_red_coin_swoops",
        "Two Swoops in the upper Red Coin area",
        2,
        has_swoops and has_platform_route and has_checkerboards,
    ))
    traces.append(coin_source(
        "pit_islands_ceiling_coin_line",
        "Coin line on the hangable ceiling above Pit Islands",
        5,
        state.can_reach(f"{level_name} - Pit Islands", "Region", player)
        and has_climb and has_horizontal_coin_lines,
    ))
    traces.append(coin_source(
        "swimming_beast_coin_ring",
        "Coin ring around Swimming Beast in the Cavern",
        8,
        (
            Rules.has_simple_arbitrary_feature(state, player, "HMC_SWIMMING_BEAST")
            or Rules.can_use_logic_trick(state, player, "logic_hmc_elevator_clip", level_name)
        )
        and has_horizontal_coin_rings,
    ))

    has_toxic_maze_location = state.can_reach(
        f"{level_name} - Navigating the Toxic Maze", "Location", player)
    toxic_maze_children = (
        coin_source("toxic_maze_star_coin_line", "Coin line leading to the toxic maze star", 5,
                has_toxic_maze_location and has_horizontal_coin_lines),
        coin_source("toxic_maze_exit_swoops", "Two additional Swoops on the toxic maze route", 2,
                has_toxic_maze_location and has_swoops),
    )
    traces.append(coin_route(
        "navigating_toxic_maze_sources",
        "Navigating the Toxic Maze sources",
        has_toxic_maze_location,
        has_toxic_maze_location,
        toxic_maze_children,
    ))

    has_metal_head_route = (
        Rules.has_purple_switches(state, player, level_name)
        and (
            Rules.has_metal_cap(state, player, level_name)
            or Rules.can_use_logic_trick(
                state, player, "logic_hmc_metal_head_coin_route_capless", level_name)
        )
    )
    traces.append(coin_source(
        "metal_head_scuttlebug",
        "Scuttlebug on the Metal-Head Mario Can Move route",
        3,
        has_metal_head_route and has_scuttlebugs,
    ))
    traces.append(coin_source(
        "toxic_maze_blue_coin_block",
        "Blue Coin Block in the toxic maze",
        35,
        has_blue_coin_block and Rules.has_action(state, player, "Ground Pound", level_name),
    ))
    return coin_evaluation(traces, 139)


def coin_condition(
        source_id: str,
        label: str,
        available: bool,
        *,
        counted: bool | None = None,
) -> CoinSourceTrace:
    if counted is None:
        counted = available
    return CoinSourceTrace(source_id, label, 0, counted, available)


def lethal_lava_land_coins(
        state: CollectionState,
        player: int,
        _required_coins: int,
) -> CoinEvaluation:
    from . import Rules

    level_name = "Lethal Lava Land"
    target_name = f"{level_name} - Coins Star"
    has_single_yellow_coins = Rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Single Yellow Coins", f"{level_name} - Single Yellow Coins")
    has_red_coins = Rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Red Coins", f"{level_name} - Red Coins")
    has_horizontal_coin_lines = Rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Horizontal Coin Lines", f"{level_name} - Horizontal Coin Lines")
    has_horizontal_coin_rings = Rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Horizontal Coin Rings", f"{level_name} - Horizontal Coin Rings")
    has_crazy_box = Rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Crazy Boxes", f"{level_name} - Crazy Box")
    has_bowser_puzzle = Rules.has_unlock(
        state, player, "coin_object_unlocks",
        f"{level_name} - Bowser Puzzle", f"{level_name} - Bowser Puzzle")
    has_bullies = Rules.has_unlock(
        state, player, "enemy_unlocks",
        "Bullies", f"{level_name} - Bullies")
    has_mr_is = Rules.has_unlock(
        state, player, "enemy_unlocks",
        "Mr. Is", f"{level_name} - Mr. Is")

    has_koopa_shell = Rules.has_per_act_feature(
        state, player, f"{level_name} - Koopa Shell")
    has_lava_damage_boosting = Rules.can_use_logic_trick(
        state, player, "logic_lava_damage_boosting", target_name)
    can_reach_red_coins = Rules.can_reach_lethal_lava_land_red_coins(
        state, player, target_name)
    has_healing_coins = Rules.has_lethal_lava_land_healing_coins(state, player)
    can_collect_all_red_coins = Rules.can_collect_all_lethal_lava_land_red_coins(
        state, player, target_name)

    builder = CoinTraceBuilder()
    builder.add(
        "lll_tilting_platform_coin_line",
        "Coin line on the tilting platform past the first Mr. I",
        5,
        has_horizontal_coin_lines,
    )
    builder.add(
        "lll_grey_ramp_coins",
        "Coins on the grey ramp near the tilting platform",
        3,
        has_single_yellow_coins,
    )
    builder.add(
        "lll_bowser_puzzle_coins",
        "Bowser Puzzle reward",
        5,
        has_bowser_puzzle,
    )
    builder.add(
        "lll_first_big_bully_coin_line",
        "Coin line before the first Big Bully",
        5,
        has_horizontal_coin_lines,
    )
    builder.add(
        "lll_second_big_bully_coin_ring",
        "Coin ring on the second Big Bully platform",
        8,
        has_horizontal_coin_rings,
    )
    builder.add(
        "lll_northwest_ramp_coin_line",
        "Coin line on the northwest brown ramp",
        5,
        has_horizontal_coin_lines,
    )
    builder.add(
        "lll_sinking_platform_coins",
        "Coins on the sinking platforms near the Crazy Box",
        4,
        has_single_yellow_coins,
    )
    builder.add(
        "lll_north_volcano_coin_line",
        "Coin line north of the volcano",
        5,
        has_horizontal_coin_lines,
    )
    builder.add(
        "lll_two_bullies_coin_ring",
        "Coin ring on the platform with two Bullies",
        8,
        has_horizontal_coin_rings,
    )
    builder.add(
        "lll_spinning_volcano_platform_coins",
        "Coins on the spinning platform around the volcano",
        3,
        has_single_yellow_coins,
    )
    builder.add(
        "lll_southeast_grey_ramp_coins",
        "Coins on the southeast grey ramp",
        4,
        has_single_yellow_coins,
    )
    builder.add(
        "lll_second_mr_i_coin_ring",
        "Coin ring by the second Mr. I",
        8,
        has_horizontal_coin_rings,
    )
    builder.add(
        "lll_crazy_box_coins",
        "Crazy Box",
        5,
        has_crazy_box,
    )

    red_coin_route_children = (
        coin_condition(
            "lll_red_coin_unlock",
            "Red Coins are unlocked",
            has_red_coins,
        ),
        coin_condition(
            "lll_red_coin_bowser_puzzle_route",
            "Bowser Puzzle route",
            has_bowser_puzzle,
        ),
        coin_condition(
            "lll_red_coin_koopa_shell_route",
            "Koopa Shell route",
            has_koopa_shell,
        ),
        coin_condition(
            "lll_red_coin_lava_damage_boosting_route",
            "Lava Damage Boosting trick route",
            has_lava_damage_boosting,
        ),
    )
    builder.add(
        "lll_first_five_red_coins",
        "First five Red Coins",
        10,
        has_red_coins and can_reach_red_coins,
        children=red_coin_route_children,
    )
    all_red_coin_route_children = red_coin_route_children + (
        coin_condition(
            "lll_red_coin_healing_source",
            "A non-puzzle healing coin source is unlocked",
            has_healing_coins,
        ),
    )
    builder.add(
        "lll_remaining_three_red_coins",
        "Remaining three Red Coins",
        6,
        has_red_coins and can_collect_all_red_coins,
        children=all_red_coin_route_children,
    )

    builder.add(
        "lll_outside_bullies",
        "Eight Bullies outside the volcano",
        8,
        has_bullies,
    )
    builder.add(
        "lll_mr_is",
        "Two Mr. Is",
        10,
        has_mr_is,
    )
    builder.add(
        "lll_under_bridge_coin_line",
        "Coin line under the bridge",
        5,
        has_single_yellow_coins and (has_koopa_shell or has_lava_damage_boosting),
        children=(
            coin_condition(
                "lll_under_bridge_koopa_shell_route",
                "Koopa Shell route",
                has_koopa_shell,
            ),
            coin_condition(
                "lll_under_bridge_lava_damage_boosting_route",
                "Lava Damage Boosting trick route",
                has_lava_damage_boosting,
            ),
        ),
    )
    builder.add(
        "lll_volcano_s_island_coins",
        "Volcano S-shaped island coins",
        3,
        has_single_yellow_coins,
    )
    builder.add(
        "lll_volcano_first_ridge_coin_line",
        "Volcano first ridge coin line",
        5,
        has_horizontal_coin_lines,
    )
    builder.add(
        "lll_volcano_second_ridge_coins",
        "Volcano second ridge coins",
        2,
        has_single_yellow_coins,
    )
    builder.add(
        "lll_volcano_floating_platform_coins",
        "Volcano floating platform coins",
        4,
        has_single_yellow_coins,
    )
    builder.add(
        "lll_volcano_post_platform_coin",
        "Volcano coin after the floating platforms",
        1,
        has_single_yellow_coins,
    )
    builder.add(
        "lll_volcano_second_bully_coin_line",
        "Volcano second Bully coin line",
        5,
        has_horizontal_coin_lines,
    )
    builder.add(
        "lll_volcano_checkerboard_lift_coin",
        "Volcano coin by the checkerboard lift",
        1,
        has_single_yellow_coins,
    )
    builder.add(
        "lll_volcano_bullies",
        "Bullies inside the volcano",
        2,
        has_bullies,
    )
    can_reach_elevator_tour = state.can_reach(
        "Lethal Lava Land - Elevator Tour in the Volcano", "Location", player)
    builder.add(
        "lll_elevator_tour_platform_coins",
        "Tiny platforms by Elevator Tour in the Volcano",
        3,
        has_single_yellow_coins and can_reach_elevator_tour,
        children=(
            coin_condition(
                "lll_elevator_tour_location_access",
                "Elevator Tour in the Volcano is reachable",
                can_reach_elevator_tour,
            ),
        ),
    )

    assert builder.reachable_coins <= 133
    return builder.evaluation()


def shifting_sand_land_coins(
        state: CollectionState,
        player: int,
        _required_coins: int,
) -> CoinEvaluation:
    from . import Rules

    level_name = "Shifting Sand Land"
    target_name = f"{level_name} - Coins Star"
    has_single_yellow_coins = Rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Single Yellow Coins", f"{level_name} - Single Yellow Coins")
    has_red_coins = Rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Red Coins", f"{level_name} - Red Coins")
    has_blue_coin_block = Rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Blue Coin Blocks", f"{level_name} - Blue Coin Block")
    has_horizontal_coin_lines = Rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Horizontal Coin Lines", f"{level_name} - Horizontal Coin Lines")
    has_horizontal_coin_ring = Rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Horizontal Coin Rings", f"{level_name} - Horizontal Coin Rings")
    has_vertical_coin_line = Rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Vertical Coin Lines", f"{level_name} - Vertical Coin Lines")
    has_throwable_cork_box = Rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Throwable Cork Boxes", f"{level_name} - Throwable Cork Box")
    has_crazy_boxes = Rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Crazy Boxes", f"{level_name} - Crazy Boxes")
    has_bob_ombs = Rules.has_unlock(
        state, player, "enemy_unlocks",
        "Bob-ombs", f"{level_name} - Bob-ombs")
    has_fly_guys = Rules.has_unlock(
        state, player, "enemy_unlocks",
        "Fly Guys", f"{level_name} - Fly Guy")
    has_goombas = Rules.has_unlock(
        state, player, "enemy_unlocks",
        "Goombas", f"{level_name} - Goombas")
    has_pokeys = Rules.has_unlock(
        state, player, "enemy_unlocks",
        "Pokeys", f"{level_name} - Pokeys")

    builder = CoinTraceBuilder()
    builder.add(
        "ssl_throwable_cork_box",
        "Throwable cork box under the stone structure",
        3,
        has_throwable_cork_box,
    )
    builder.add(
        "ssl_pillar_and_pyramid_coins",
        "Coins on the pillars and inside the pyramid",
        6,
        has_single_yellow_coins,
    )
    builder.add(
        "ssl_behind_pyramid_coin_line",
        "Coin line between the pillars behind the pyramid",
        5,
        has_horizontal_coin_lines,
    )
    builder.add(
        "ssl_pyramid_side_coin_line",
        "Vertical coin line up the side of the pyramid",
        5,
        has_vertical_coin_line,
    )
    builder.add(
        "ssl_fly_guys",
        "Fly Guys",
        6,
        has_fly_guys,
    )
    builder.add(
        "ssl_crazy_boxes",
        "Crazy Boxes",
        10,
        has_crazy_boxes,
    )
    builder.add(
        "ssl_bob_ombs",
        "Bob-ombs",
        2,
        has_bob_ombs,
    )
    builder.add(
        "ssl_pokeys",
        "Pokeys",
        20,
        has_pokeys,
    )
    builder.add(
        "ssl_goombas",
        "Goombas inside and outside the pyramid",
        12,
        has_goombas,
    )
    builder.add(
        "ssl_low_red_coins",
        "Four low Red Coins",
        8,
        has_red_coins,
    )

    has_climb = Rules.has_action(state, player, "Climb", level_name)
    builder.add(
        "ssl_first_wire_grid_coin_ring",
        "Coin ring under the first pyramid wire grid",
        8,
        has_horizontal_coin_ring and has_climb,
        children=(
            coin_condition("ssl_first_wire_grid_climb", "Climb", has_climb),
        ),
    )

    has_wing_cap = Rules.has_wing_cap(state, player, level_name)
    has_triple_jump = Rules.has_action(state, player, "Triple Jump", level_name)
    has_cannon = state.has(f"{level_name} - Cannon Unlock", player)
    has_normal_red_coin_route = has_wing_cap and (has_triple_jump or has_cannon)
    has_tweester_trick = Rules.can_use_logic_trick(
        state, player, "logic_ssl_three_red_coins_with_tweesters", target_name)
    has_shy_guy_trick = Rules.can_use_logic_trick(
        state, player, "logic_ssl_one_red_coin_with_shy_guy_spin_jump", target_name)
    no_despawns = bool(state.multiworld.worlds[player].options.no_despawns.value)

    builder.add(
        "ssl_normal_high_red_coin_route",
        "Four high Red Coins via Wing Cap",
        8,
        has_red_coins and has_normal_red_coin_route,
        children=(
            coin_condition("ssl_high_red_coin_wing_cap", "Wing Cap", has_wing_cap),
            coin_condition("ssl_high_red_coin_triple_jump", "Triple Jump route", has_triple_jump),
            coin_condition("ssl_high_red_coin_cannon", "Cannon route", has_cannon),
        ),
    )
    tweester_route_available = has_red_coins and has_tweester_trick
    builder.add(
        "ssl_tweester_red_coin_route",
        "Three high Red Coins with the Tweester trick",
        6,
        tweester_route_available,
        counted=tweester_route_available and not has_normal_red_coin_route,
        children=(
            coin_condition(
                "ssl_tweester_red_coin_trick",
                "Tweesters to Reach 3 Red Coins trick",
                has_tweester_trick,
            ),
        ),
    )
    shy_guy_route_available = has_red_coins and has_shy_guy_trick and no_despawns
    builder.add(
        "ssl_shy_guy_red_coin_route",
        "One high Red Coin with the Shy Guy spin-jump trick",
        2,
        shy_guy_route_available,
        counted=shy_guy_route_available and not has_normal_red_coin_route,
        children=(
            coin_condition(
                "ssl_shy_guy_red_coin_trick",
                "Spin Jump Off a Shy Guy to Reach 1 Red Coin trick",
                has_shy_guy_trick,
            ),
            coin_condition(
                "ssl_shy_guy_red_coin_no_despawns",
                "No Despawns",
                no_despawns,
            ),
        ),
    )

    can_reach_upper_pyramid = state.can_reach(
        "Shifting Sand Land - Upper Pyramid", "Region", player)
    builder.add(
        "ssl_upper_pyramid_coin_lines",
        "Coin lines under the second wire grid and at the pyramid top",
        15,
        can_reach_upper_pyramid and has_horizontal_coin_lines,
        children=(
            coin_condition(
                "ssl_upper_pyramid_access_for_lines",
                "Upper Pyramid is reachable",
                can_reach_upper_pyramid,
            ),
        ),
    )
    builder.add(
        "ssl_upper_pyramid_single_coins",
        "Moving-step and Pyramid Puzzle secret coins",
        13,
        can_reach_upper_pyramid and has_single_yellow_coins,
        children=(
            coin_condition(
                "ssl_upper_pyramid_access_for_singles",
                "Upper Pyramid is reachable",
                can_reach_upper_pyramid,
            ),
        ),
    )

    has_ground_pound = Rules.has_action(state, player, "Ground Pound", level_name)
    builder.add(
        "ssl_blue_coin_block",
        "Blue Coin Block",
        15,
        has_blue_coin_block and has_ground_pound,
        children=(
            coin_condition("ssl_blue_coin_block_ground_pound", "Ground Pound", has_ground_pound),
        ),
    )

    assert builder.reachable_coins <= 136
    return builder.evaluation()


def dire_dire_docks_coins(
        state: CollectionState,
        player: int,
        _required_coins: int,
) -> CoinEvaluation:
    from . import Rules

    level_name = "Dire, Dire Docks"
    has_single_yellow_coins = Rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Single Yellow Coins", f"{level_name} - Single Yellow Coins")
    has_red_coins = Rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Red Coins", f"{level_name} - Red Coins")
    has_blue_coin_block = Rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Blue Coin Blocks", f"{level_name} - Blue Coin Block")
    has_horizontal_coin_lines = Rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Horizontal Coin Lines", f"{level_name} - Horizontal Coin Lines")
    has_horizontal_coin_rings = Rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Horizontal Coin Rings", f"{level_name} - Horizontal Coin Rings")
    has_vertical_coin_lines = Rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Vertical Coin Lines", f"{level_name} - Vertical Coin Lines")
    has_vertical_coin_rings = Rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Vertical Coin Rings", f"{level_name} - Vertical Coin Rings")

    has_climb = Rules.has_action(state, player, "Climb", level_name)
    has_poles_item = Rules.has_per_act_feature(
        state, player, f"{level_name} - Poles")
    has_poles = has_poles_item and has_climb
    has_purple_switch_route = Rules.has_purple_switches(state, player, level_name)
    has_sub = Rules.has_per_act_feature(
        state, player, f"{level_name} - Bowser's Sub")
    has_triple_jump = Rules.has_action(state, player, "Triple Jump", level_name)
    has_sub_poles_movement_route = has_sub and has_poles and has_triple_jump

    builder = CoinTraceBuilder()
    builder.add(
        "ddd_start_wall_coin_line",
        "Sloped underwater coin line near the start",
        5,
        has_horizontal_coin_lines,
    )
    builder.add(
        "ddd_chest_and_current_coin_lines",
        "Vertical coin lines by the chests and first current",
        10,
        has_vertical_coin_lines,
    )
    builder.add(
        "ddd_seafloor_chest_coins",
        "Coins surrounding the sea-floor chest",
        3,
        has_single_yellow_coins,
    )
    builder.add(
        "ddd_sub_area_coin_rings",
        "Coin rings leading to the Bowser's Sub area",
        24,
        has_vertical_coin_rings,
    )
    builder.add(
        "ddd_seafloor_clam_coin_ring",
        "Sea-floor coin ring by the Koopa Shell clam",
        8,
        has_horizontal_coin_rings,
    )
    builder.add(
        "ddd_moat_exit_coin_line",
        "Vertical coin line by the moat exit",
        5,
        has_vertical_coin_lines,
    )
    builder.add(
        "ddd_sub_area_dock_coin_line",
        "Coin line on the Bowser's Sub area dock",
        5,
        has_horizontal_coin_lines,
    )

    can_reach_first_red_coin = has_purple_switch_route or has_sub_poles_movement_route
    red_route_children = (
        coin_condition(
            "ddd_red_coin_purple_switch_route",
            "Purple Switch route",
            has_purple_switch_route,
        ),
        coin_condition(
            "ddd_red_coin_sub_poles_movement_route",
            "Bowser's Sub, Poles, Climb, and Triple Jump route",
            has_sub_poles_movement_route,
        ),
    )
    builder.add(
        "ddd_first_red_coin",
        "First Red Coin",
        2,
        has_red_coins and can_reach_first_red_coin,
        children=red_route_children,
    )
    builder.add(
        "ddd_remaining_red_coins",
        "Remaining seven Red Coins",
        14,
        has_red_coins and can_reach_first_red_coin and has_poles,
        children=red_route_children + (
            coin_condition("ddd_remaining_red_coin_poles", "Poles item", has_poles_item),
            coin_condition("ddd_remaining_red_coin_climb", "Climb", has_climb),
        ),
    )

    has_ground_pound = Rules.has_action(state, player, "Ground Pound", level_name)
    builder.add(
        "ddd_blue_coin_block",
        "Blue Coin Block",
        30,
        has_blue_coin_block and has_purple_switch_route and has_poles and has_ground_pound,
        children=(
            coin_condition(
                "ddd_blue_coin_block_purple_switches",
                "Purple Switch route",
                has_purple_switch_route,
            ),
            coin_condition("ddd_blue_coin_block_poles", "Poles item", has_poles_item),
            coin_condition("ddd_blue_coin_block_climb", "Climb", has_climb),
            coin_condition("ddd_blue_coin_block_ground_pound", "Ground Pound", has_ground_pound),
        ),
    )

    assert builder.reachable_coins <= 106
    return builder.evaluation()


def snowmans_land_coins(
        state: CollectionState,
        player: int,
        _required_coins: int,
) -> CoinEvaluation:
    from . import Rules

    level_name = "Snowman's Land"
    target_name = f"{level_name} - Coins Star"
    has_single_yellow_coins = Rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Single Yellow Coins", f"{level_name} - Single Yellow Coins")
    has_red_coins = Rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Red Coins", f"{level_name} - Red Coins")
    has_horizontal_coin_lines = Rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Horizontal Coin Lines", f"{level_name} - Horizontal Coin Lines")
    has_three_coin_block = Rules.has_unlock(
        state, player, "coin_object_unlocks",
        "3-Coin Blocks", f"{level_name} - 3-Coin Block")
    has_fly_guy = Rules.has_unlock(
        state, player, "enemy_unlocks",
        "Fly Guys", f"{level_name} - Fly Guy")
    has_goombas = Rules.has_unlock(
        state, player, "enemy_unlocks",
        "Goombas", f"{level_name} - Goombas")
    has_moneybags = Rules.has_unlock(
        state, player, "enemy_unlocks",
        f"{level_name} - Moneybags", f"{level_name} - Moneybags")
    has_mr_blizzards = Rules.has_unlock(
        state, player, "enemy_unlocks",
        "Mr Blizzards", f"{level_name} - Mr Blizzards")
    has_spindrifts = Rules.has_unlock(
        state, player, "enemy_unlocks",
        "Spindrifts", f"{level_name} - Spindrifts")

    builder = CoinTraceBuilder()
    builder.add(
        "sl_start_coins",
        "Coins to the left of the start",
        2,
        has_single_yellow_coins,
    )
    builder.add(
        "sl_spindrifts",
        "Eleven Spindrifts",
        33,
        has_spindrifts,
    )
    builder.add(
        "sl_start_mr_blizzards",
        "Three Mr. Blizzards",
        9,
        has_mr_blizzards,
    )
    builder.add(
        "sl_moneybags",
        "Two Moneybags",
        10,
        has_moneybags,
    )
    builder.add(
        "sl_fly_guy",
        "Fly Guy",
        2,
        has_fly_guy,
    )

    can_reach_whirl = state.can_reach(
        "Snowman's Land - Whirl from the Freezing Pond", "Region", player)
    builder.add(
        "sl_whirl_red_coins",
        "Three Red Coins in the Whirl from the Freezing Pond area",
        6,
        can_reach_whirl and has_red_coins,
        children=(
            coin_condition(
                "sl_whirl_region_access_for_red_coins",
                "Whirl from the Freezing Pond is reachable",
                can_reach_whirl,
            ),
        ),
    )
    has_cannon = state.has(f"{level_name} - Cannon Unlock", player)
    no_despawns = bool(state.multiworld.worlds[player].options.no_despawns.value)
    builder.add(
        "sl_whirl_mr_blizzard",
        "Mr. Blizzard in the Whirl from the Freezing Pond area",
        3,
        can_reach_whirl and has_mr_blizzards and (has_cannon or no_despawns),
        children=(
            coin_condition(
                "sl_whirl_region_access_for_mr_blizzard",
                "Whirl from the Freezing Pond is reachable",
                can_reach_whirl,
            ),
            coin_condition(
                "sl_whirl_mr_blizzard_cannon_route",
                "Cannon route",
                has_cannon,
            ),
            coin_condition(
                "sl_whirl_mr_blizzard_no_despawns_route",
                "No Despawns route",
                no_despawns,
            ),
        ),
    )

    can_reach_upper = state.can_reach(f"{level_name} - Upper", "Region", player)
    builder.add(
        "sl_upper_slope_coin_line",
        "Coin line on the slope toward the Igloo",
        5,
        can_reach_upper and has_horizontal_coin_lines,
    )
    builder.add(
        "sl_upper_slope_single_coins",
        "Single coins on the slope toward the Igloo",
        3,
        can_reach_upper and has_single_yellow_coins,
    )
    builder.add(
        "sl_penguin_and_face_coins",
        "Coins by the penguin and snowman's face",
        3,
        can_reach_upper and has_single_yellow_coins,
    )
    builder.add(
        "sl_upper_spindrifts",
        "Three Spindrifts in the Upper area",
        9,
        can_reach_upper and has_spindrifts,
    )
    builder.add(
        "sl_upper_goombas",
        "Three Goombas in the Upper area",
        3,
        can_reach_upper and has_goombas,
    )
    builder.add(
        "sl_upper_red_coins",
        "Five Red Coins in the Upper area",
        10,
        can_reach_upper and has_red_coins,
    )

    can_reach_snowman_top = state.can_reach(
        f"{level_name} - Top of Snowman's Head", "Region", player)
    builder.add(
        "sl_snowman_head_plank_coins",
        "Coins on the wooden plank near the top of the snowman",
        2,
        can_reach_snowman_top and has_single_yellow_coins,
        children=(
            coin_condition(
                "sl_snowman_head_region_access",
                "Top of Snowman's Head is reachable",
                can_reach_snowman_top,
            ),
        ),
    )

    can_reach_igloo = state.can_reach(f"{level_name} - Igloo", "Region", player)
    has_vanish_cap = Rules.has_vanish_cap(state, player, level_name)
    igloo_source_data = (
        (
            "sl_igloo_frozen_coin_lines",
            "Frozen coin lines inside the Igloo",
            20,
            has_horizontal_coin_lines and has_vanish_cap,
        ),
        (
            "sl_igloo_single_coins",
            "Single coins inside the Igloo",
            3,
            has_single_yellow_coins,
        ),
        (
            "sl_igloo_three_coin_block",
            "3-Coin Block inside the Igloo",
            3,
            has_three_coin_block,
        ),
    )
    igloo_children = [
        CoinSourceTrace(source_id, label, coins, available, available)
        for source_id, label, coins, available in igloo_source_data
    ]
    igloo_coins = sum(
        coins for _source_id, _label, coins, available in igloo_source_data if available)
    loses_spindrift_coins = (
        can_reach_igloo
        and has_spindrifts
        and not can_reach_snowman_top
        and not has_cannon
        and not Rules.permanent_coin_collection_enabled(state, player)
    )
    transition_loss = min(3, igloo_coins) if loses_spindrift_coins else 0
    if loses_spindrift_coins:
        igloo_children.append(CoinSourceTrace(
            "sl_igloo_transition_loss",
            (
                "Spindrift coins lost during the forced Igloo transition"
                if transition_loss
                else "Forced Igloo transition has no Igloo coins to deduct"
            ),
            transition_loss,
            False,
            True,
        ))
    else:
        igloo_children.append(CoinSourceTrace(
            "sl_igloo_transition_loss",
            "No Spindrift coin loss during the Igloo transition",
            3,
            False,
            False,
        ))
    net_igloo_coins = igloo_coins - transition_loss
    builder.add(
        "sl_igloo_route",
        "Igloo coin route after transition losses",
        net_igloo_coins,
        can_reach_igloo,
        children=tuple(igloo_children),
    )

    has_impossible_coin_trick = Rules.can_use_logic_trick(
        state, player, "logic_sl_impossible_coin", target_name)
    builder.add(
        "sl_impossible_coin",
        "Impossible Coin trick",
        1,
        has_single_yellow_coins and has_impossible_coin_trick,
        children=(
            coin_condition(
                "sl_impossible_coin_trick",
                "Snowman's Land Impossible Coin trick",
                has_impossible_coin_trick,
            ),
        ),
    )

    assert builder.reachable_coins <= 127
    return builder.evaluation()


def tall_tall_mountain_coins(
        state: CollectionState,
        player: int,
        _required_coins: int,
) -> CoinEvaluation:
    from . import Rules

    level_name = "Tall, Tall Mountain"
    has_single_yellow_coins = Rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Single Yellow Coins", f"{level_name} - Single Yellow Coins")
    has_red_coins = Rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Red Coins", f"{level_name} - Red Coins")
    has_single_blue_coins = Rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Single Blue Coins", f"{level_name} - Single Blue Coins")
    has_horizontal_coin_lines = Rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Horizontal Coin Lines", f"{level_name} - Horizontal Coin Lines")
    has_horizontal_coin_ring = Rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Horizontal Coin Rings", f"{level_name} - Horizontal Coin Rings")
    has_vertical_coin_line = Rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Vertical Coin Lines", f"{level_name} - Vertical Coin Lines")
    has_crazy_box = Rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Crazy Boxes", f"{level_name} - Crazy Box")
    has_bob_ombs = Rules.has_unlock(
        state, player, "enemy_unlocks",
        "Bob-ombs", f"{level_name} - Bob-ombs")
    has_chuckya = Rules.has_unlock(
        state, player, "enemy_unlocks",
        "Chuckyas", f"{level_name} - Chuckya")
    has_fly_guy = Rules.has_unlock(
        state, player, "enemy_unlocks",
        "Fly Guys", f"{level_name} - Fly Guy")
    has_goombas = Rules.has_unlock(
        state, player, "enemy_unlocks",
        "Goombas", f"{level_name} - Goombas")

    builder = CoinTraceBuilder()
    builder.add(
        "ttm_start_coin_ring",
        "Coin ring at the start",
        8,
        has_horizontal_coin_ring,
    )
    builder.add(
        "ttm_crazy_box",
        "Crazy Box",
        5,
        has_crazy_box,
    )
    builder.add(
        "ttm_start_goombas",
        "Three Goombas in the starting area",
        2,
        has_goombas,
    )

    can_reach_middle = state.can_reach(f"{level_name} - Middle", "Region", player)
    builder.add(
        "ttm_middle_goomba",
        "Goomba above the starting area",
        1,
        can_reach_middle and has_goombas,
    )
    builder.add(
        "ttm_middle_red_coins",
        "Six Red Coins in the Middle area",
        12,
        can_reach_middle and has_red_coins,
    )
    builder.add(
        "ttm_middle_bob_ombs",
        "Three Bob-ombs in the Middle area",
        3,
        can_reach_middle and has_bob_ombs,
    )
    builder.add(
        "ttm_middle_chuckya",
        "Chuckya in the Middle area",
        5,
        can_reach_middle and has_chuckya,
    )
    builder.add(
        "ttm_middle_bridge_coin_line",
        "Coin line on the bridge from Chuckya to the Bob-omb Buddy",
        5,
        can_reach_middle and has_horizontal_coin_lines,
    )
    builder.add(
        "ttm_middle_fly_guy",
        "Fly Guy in the Middle area",
        2,
        can_reach_middle and has_fly_guy,
    )

    can_reach_upper = state.can_reach(f"{level_name} - Upper", "Region", player)
    builder.add(
        "ttm_upper_red_coins",
        "Two Red Coins in the Upper area",
        4,
        can_reach_upper and has_red_coins,
    )
    builder.add(
        "ttm_upper_goombas",
        "Six Goombas in the Upper area",
        6,
        can_reach_upper and has_goombas,
    )
    builder.add(
        "ttm_upper_bob_ombs",
        "Two Bob-ombs in the Upper area",
        2,
        can_reach_upper and has_bob_ombs,
    )
    has_climb = Rules.has_action(state, player, "Climb", level_name)
    has_moveless = Rules.can_use_logic_trick(
        state, player, "logic_ttm_coins_without_climb", level_name)
    builder.add(
        "ttm_upper_leaf_coin_line",
        "Coin line by the Upper Monty Moles",
        5,
        can_reach_upper and has_horizontal_coin_lines and (has_climb or has_moveless),
        children=(
            coin_condition("ttm_upper_leaf_climb_route", "Climb route", has_climb),
            coin_condition(
                "ttm_upper_leaf_moveless_route",
                "No-Climb coin route",
                has_moveless,
            ),
        ),
    )

    can_reach_top = state.can_reach(f"{level_name} - Top", "Region", player)
    builder.add(
        "ttm_slide_single_coins",
        "Single yellow coins on the slide",
        27,
        can_reach_top and has_single_yellow_coins,
    )
    builder.add(
        "ttm_slide_coin_lines",
        "Four coin lines on the slide",
        20,
        can_reach_top and has_horizontal_coin_lines,
    )
    builder.add(
        "ttm_slide_blue_coins",
        "Single blue coins on the slide",
        15,
        can_reach_top and has_single_blue_coins,
    )
    builder.add(
        "ttm_slide_entrance_coin_line",
        "Coin line by the slide entrance",
        5,
        can_reach_top and has_horizontal_coin_lines,
    )
    builder.add(
        "ttm_top_switch_base_coins",
        "Lower coins by the Purple Switch near the mountain top",
        2,
        can_reach_top and has_vertical_coin_line,
    )
    builder.add(
        "ttm_waterfall_bridge_coin_line",
        "Coin line on the rock bridge beside the waterfall",
        5,
        can_reach_top and has_horizontal_coin_lines,
    )

    has_purple_switches = Rules.has_purple_switches(state, player, level_name)
    has_triple_jump = Rules.has_action(state, player, "Triple Jump", level_name)
    has_backflip = Rules.has_action(state, player, "Backflip", level_name)
    has_side_flip = Rules.has_action(state, player, "Side Flip", level_name)
    has_first_upper_switch_route = (
        has_purple_switches or has_triple_jump or has_backflip or has_side_flip)
    builder.add(
        "ttm_top_switch_middle_coins",
        "Middle coins by the Purple Switch near the mountain top",
        2,
        can_reach_top and has_vertical_coin_line and has_first_upper_switch_route,
        children=(
            coin_condition(
                "ttm_top_switch_middle_purple_switch_route",
                "Purple Switch route",
                has_purple_switches,
            ),
            coin_condition(
                "ttm_top_switch_middle_triple_jump_route",
                "Triple Jump route",
                has_triple_jump,
            ),
            coin_condition(
                "ttm_top_switch_middle_backflip_route",
                "Backflip route",
                has_backflip,
            ),
            coin_condition(
                "ttm_top_switch_middle_side_flip_route",
                "Side Flip route",
                has_side_flip,
            ),
        ),
    )
    has_final_upper_switch_route = has_purple_switches or has_triple_jump
    builder.add(
        "ttm_top_switch_highest_coin",
        "Highest coin by the Purple Switch near the mountain top",
        1,
        can_reach_top and has_vertical_coin_line and has_final_upper_switch_route,
        children=(
            coin_condition(
                "ttm_top_switch_highest_purple_switch_route",
                "Purple Switch route",
                has_purple_switches,
            ),
            coin_condition(
                "ttm_top_switch_highest_triple_jump_route",
                "Triple Jump route",
                has_triple_jump,
            ),
        ),
    )

    return builder.evaluation()


@dataclasses.dataclass
class _route_trace_node_type:
    source_id: str
    label: str
    coins: int
    available: bool
    selected: bool
    children: list[_route_trace_node_type] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class _route_type:
    source_id: str
    label: str
    available: bool
    sources: dict[str, int]
    children: list[_route_trace_node_type]


def _route_source(
        source_id: str,
        label: str,
        coins: int,
        available: bool,
        *,
        selected: bool | None = None,
) -> _route_trace_node_type:
    return _route_trace_node_type(
        source_id,
        label,
        coins,
        available,
        available if selected is None else selected,
    )


def _build_route_trace_node(
        node: _route_trace_node_type,
        *,
        route_available: bool,
        route_counted: bool,
        route_id: str,
        source_owners: dict[str, str] | None,
) -> CoinSourceTrace:
    available = route_available and node.available
    children = tuple(
        _build_route_trace_node(
            child,
            route_available=available,
            route_counted=route_counted and node.selected,
            route_id=route_id,
            source_owners=source_owners,
        )
        for child in node.children
    )
    if children:
        counted = route_counted and node.selected and available
        coins = sum(child.coins for child in children if child.counted)
        if not counted:
            coins = sum(child.coins for child in children if child.available)
        return CoinSourceTrace(
            node.source_id,
            node.label,
            coins,
            counted,
            available,
            children,
        )

    owned = source_owners is None or source_owners.get(node.source_id) == route_id
    counted = route_counted and node.selected and available and owned
    return CoinSourceTrace(
        node.source_id,
        node.label,
        node.coins,
        counted,
        available,
    )


def _build_route_trace(
        route: _route_type,
        *,
        counted: bool,
        source_owners: dict[str, str] | None = None,
) -> CoinSourceTrace:
    children = tuple(
        _build_route_trace_node(
            child,
            route_available=route.available,
            route_counted=counted,
            route_id=route.source_id,
            source_owners=source_owners,
        )
        for child in route.children
    )
    if counted:
        coins = sum(child.coins for child in children if child.counted)
    else:
        coins = sum(route.sources.values())
    return CoinSourceTrace(
        route.source_id,
        route.label,
        coins,
        counted,
        route.available,
        children,
    )


def _evaluate_route_set(
        routes: list[_route_type],
        *,
        permanent: bool,
        maximum: int | None = None,
) -> CoinEvaluation:
    if permanent:
        source_owners: dict[str, str] = {}
        reachable_sources: dict[str, int] = {}
        for route in routes:
            if not route.available:
                continue
            for source_id, value in route.sources.items():
                source_owners.setdefault(source_id, route.source_id)
                reachable_sources[source_id] = value
        reachable_coins = sum(reachable_sources.values())
        traces = tuple(
            _build_route_trace(
                route,
                counted=route.available,
                source_owners=source_owners,
            )
            for route in routes
        )
    else:
        selected_index = max(
            (index for index, route in enumerate(routes) if route.available),
            key=lambda index: sum(routes[index].sources.values()),
            default=None,
        )
        reachable_coins = (
            sum(routes[selected_index].sources.values())
            if selected_index is not None
            else 0
        )
        traces = tuple(
            _build_route_trace(route, counted=index == selected_index)
            for index, route in enumerate(routes)
        )

    if maximum is not None:
        reachable_coins = min(reachable_coins, maximum)
    return CoinEvaluation(reachable_coins, traces)


def wet_dry_world_coin_evaluation(
        state: CollectionState,
        player: int,
        required_coins: int,
) -> CoinEvaluation:
    # Import lazily so Rules can register these evaluators without an import cycle.
    from . import Rules as rules

    level_name = "Wet-Dry World"
    has_red_coins = rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Red Coins", f"{level_name} - Red Coins")
    has_blue_coin_block = rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Blue Coin Blocks", f"{level_name} - Blue Coin Block")
    has_horizontal_coin_lines = rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Horizontal Coin Lines", f"{level_name} - Horizontal Coin Lines")
    has_horizontal_coin_rings = rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Horizontal Coin Rings", f"{level_name} - Horizontal Coin Rings")
    has_breakable_coin_boxes = rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Breakable Coin Boxes", f"{level_name} - Breakable Coin Boxes")
    has_three_coin_blocks = rules.has_unlock(
        state, player, "coin_object_unlocks",
        "3-Coin Blocks", f"{level_name} - 3-Coin Blocks")
    has_ten_coin_blocks = rules.has_unlock(
        state, player, "coin_object_unlocks",
        "10-Coin Blocks", f"{level_name} - 10-Coin Blocks")
    has_chuckya = rules.has_unlock(
        state, player, "enemy_unlocks",
        "Chuckyas", f"{level_name} - Chuckya")
    has_skeeters = rules.has_unlock(
        state, player, "enemy_unlocks",
        f"{level_name} - Skeeters", f"{level_name} - Skeeters")
    has_ground_pound = rules.has_action(state, player, "Ground Pound", level_name)
    has_wdw_purple_switches = rules.has_purple_switches(state, player, level_name)
    has_water_level_diamond = rules.has_simple_arbitrary_feature(
        state, player, "WDW_WATER_LEVEL_DIAMOND")
    has_long_jump = rules.has_action(state, player, "Long Jump", level_name)
    has_triple_jump = rules.has_action(state, player, "Triple Jump", level_name)
    has_dive = rules.has_action(state, player, "Dive", level_name)
    has_wall_kick = rules.has_action(state, player, "Wall Kick", level_name)
    can_reach_high_red_coins = has_wall_kick or rules.can_use_logic_trick(
        state, player, "logic_wdw_high_red_coins_triple_jump", level_name)
    can_reach_top_of_express_elevator = state.can_reach(
        "Wet-Dry World - Top of the Express Elevator", "Region", player)
    has_movement_top_route = (
        any(
            rules.has_action(state, player, action, level_name)
            for action in ("Wall Kick", "Triple Jump", "Side Flip", "Backflip")
        )
    )
    can_reach_top_from_express_elevator = can_reach_top_of_express_elevator and (
        has_long_jump or rules.can_use_logic_trick(
            state, player, "logic_wdw_express_elevator_to_top_no_movement", level_name))
    can_reach_mid_high_from_mid = has_water_level_diamond and (
        can_reach_top_of_express_elevator or has_triple_jump and has_dive)

    def route_has_top(water_levels: set[str]) -> bool:
        return (
            has_movement_top_route
            or can_reach_top_from_express_elevator
            or "highest" in water_levels
        )

    def route_water_levels(start_water_level: str) -> set[str]:
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

    def route_has_downtown(water_levels: set[str]) -> bool:
        return (
            "highest" in water_levels
            and rules.has_action(state, player, "Ledge Grab", level_name)
            or state.has("Wet-Dry World - Cannon Unlock", player)
            or route_has_top(water_levels)
            and rules.can_use_logic_trick(
                state, player, "logic_wdw_downtown_triple_jump", level_name)
        )

    def make_route(
            variant_region: str,
            start_water_level: str,
            label: str,
    ) -> _route_type:
        route_available = state.can_reach(variant_region, "Region", player)
        water_levels = route_water_levels(start_water_level)
        has_top = route_has_top(water_levels)
        has_downtown = route_has_downtown(water_levels)
        children = [
            _route_source("main_skeeters", "Two Skeeters in the main area", 6, has_skeeters),
            _route_source("amp_ring", "Coin ring around the Amp pillar", 8, has_horizontal_coin_rings),
            _route_source(
                "pillar_ten_coin_block",
                "10-Coin Block on the pillar",
                10,
                has_ten_coin_blocks,
            ),
            _route_source(
                "push_block_three_coin_block",
                "3-Coin Block below the Chuckya platform",
                3,
                has_three_coin_blocks,
            ),
            _route_source(
                "low_breakable_boxes",
                "Breakable coin boxes at low water",
                12,
                "low" in water_levels and has_breakable_coin_boxes,
            ),
            _route_source(
                "low_ten_coin_block",
                "10-Coin Block below the cannon",
                10,
                "low" in water_levels and has_ten_coin_blocks,
            ),
            _route_source(
                "low_blue_coins",
                "Blue coins at low water",
                30,
                "low" in water_levels and has_ground_pound and has_blue_coin_block,
            ),
            _route_source(
                "wooden_structure_three_coin_block",
                "3-Coin Block on the wooden structure",
                3,
                "mid" in water_levels and has_three_coin_blocks,
            ),
            _route_source(
                "fourth_diamond_coin_line",
                "Coin line by the fourth water-level diamond",
                5,
                has_horizontal_coin_lines and bool(
                    water_levels.intersection({"mid", "highest"})
                    or has_wdw_purple_switches
                    or has_triple_jump and has_dive
                ),
            ),
            _route_source(
                "top_coin_line",
                "Coin line at the highest water-level diamond",
                5,
                has_top and has_horizontal_coin_lines,
            ),
            _route_source("top_chuckya", "Chuckya at the top", 5, has_top and has_chuckya),
            _route_source(
                "express_elevator_ten_coin_block",
                "10-Coin Block above the Express Elevator",
                10,
                can_reach_top_of_express_elevator and has_ten_coin_blocks,
            ),
            _route_source(
                "downtown_ring",
                "Downtown statue coin ring",
                8,
                has_downtown and has_horizontal_coin_rings,
            ),
            _route_source(
                "downtown_metal_cap_line",
                "Downtown metal-cap coin line",
                5,
                has_downtown and has_horizontal_coin_lines,
            ),
            _route_source(
                "downtown_first_building_line",
                "Downtown first-building coin line",
                5,
                has_downtown and has_horizontal_coin_lines,
            ),
            _route_source(
                "downtown_second_building_line",
                "Downtown second-building coin line",
                5,
                has_downtown and has_horizontal_coin_lines,
            ),
            _route_source(
                "downtown_skeeters",
                "Two Skeeters Downtown",
                6,
                has_downtown and has_skeeters,
            ),
            _route_source(
                "downtown_initial_red_coin",
                "First Downtown red coin",
                2,
                has_downtown and has_red_coins,
            ),
            _route_source(
                "downtown_diamond_red_coins",
                "Five Downtown red coins beyond water-level diamonds",
                10,
                has_downtown and has_water_level_diamond and has_red_coins,
            ),
            _route_source(
                "downtown_high_red_coins",
                "Two high Downtown red coins",
                4,
                has_downtown and has_water_level_diamond and has_red_coins
                and can_reach_high_red_coins,
            ),
        ]
        sources = {
            child.source_id: child.coins
            for child in children
            if child.available
        }
        water_label = ", ".join(sorted(water_levels))
        return _route_type(
            f"wdw_{start_water_level}_variant",
            f"{label} ({water_label} water reachable)",
            route_available,
            sources,
            children,
        )

    routes = [
        make_route("Wet-Dry World Low", "low", "Low entrance variant"),
        make_route("Wet-Dry World Middle", "mid", "Middle entrance variant"),
        make_route("Wet-Dry World High", "highest", "High entrance variant"),
    ]
    return _evaluate_route_set(
        routes,
        permanent=rules.permanent_coin_collection_enabled(state, player),
        maximum=152,
    )


def tiny_huge_island_coin_evaluation(
        state: CollectionState,
        player: int,
        required_coins: int,
) -> CoinEvaluation:
    # Import lazily so Rules can register these evaluators without an import cycle.
    from . import Rules as rules

    level_name = "Tiny-Huge Island"
    has_single_yellow_coins = rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Single Yellow Coins", f"{level_name} - Single Yellow Coins")
    has_red_coins = rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Red Coins", f"{level_name} - Red Coins")
    has_blue_coin_block = rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Blue Coin Blocks", f"{level_name} - Blue Coin Block")
    has_horizontal_coin_lines = rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Horizontal Coin Lines", f"{level_name} - Horizontal Coin Lines")
    has_three_coin_block = rules.has_unlock(
        state, player, "coin_object_unlocks",
        "3-Coin Blocks", f"{level_name} - 3-Coin Block")
    has_wooden_posts = rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Wooden Posts", f"{level_name} - Wooden Posts")
    has_chuckya = rules.has_unlock(
        state, player, "enemy_unlocks",
        "Chuckyas", f"{level_name} - Chuckya")
    has_lakitu = rules.has_unlock(
        state, player, "enemy_unlocks",
        "Lakitus", f"{level_name} - Lakitu")
    has_fire_piranha_plants = rules.has_unlock(
        state, player, "enemy_unlocks",
        "Fire Piranha Plants", f"{level_name} - Fire Piranha Plants")
    has_fly_guy = rules.has_unlock(
        state, player, "enemy_unlocks",
        "Fly Guys", f"{level_name} - Fly Guy")
    has_goombas = rules.has_unlock(
        state, player, "enemy_unlocks",
        "Goombas", f"{level_name} - Goombas")
    has_koopa_troopa = rules.has_unlock(
        state, player, "enemy_unlocks",
        "Koopa Troopas", f"{level_name} - Koopa Troopa")
    has_warp_pipes = rules.has_simple_arbitrary_feature(state, player, "THI_WARP_PIPES")
    has_thi_purple_switches = rules.has_purple_switches(state, player, level_name)
    has_triple_jump = rules.has_action(state, player, "Triple Jump", level_name)
    has_long_jump = rules.has_action(state, player, "Long Jump", level_name)
    has_backflip = rules.has_action(state, player, "Backflip", level_name)
    has_side_flip = rules.has_action(state, player, "Side Flip", level_name)
    has_ledge_grab = rules.has_action(state, player, "Ledge Grab", level_name)
    has_dive = rules.has_action(state, player, "Dive", level_name)
    has_ground_pound = rules.has_action(state, player, "Ground Pound", level_name)
    has_cannon = state.has("Tiny-Huge Island - Cannon Unlock", player)
    can_enter_tiny = state.can_reach("Tiny-Huge Island (Tiny)", "Region", player)
    can_enter_huge = state.can_reach("Tiny-Huge Island (Huge)", "Region", player)
    has_tiny_piranha_movement = has_triple_jump or has_long_jump or has_ledge_grab
    has_cannonball_movement = has_ledge_grab or has_side_flip or has_backflip or has_triple_jump
    has_upper_movement = has_side_flip or has_backflip or has_triple_jump
    has_fly_guy_ascent = rules.can_use_logic_trick(
        state,
        player,
        "logic_thi_windswept_valley_fly_guy_spin_jump",
        f"{level_name} - Coins Star",
    )
    has_koopa_shell_ascent = rules.can_use_logic_trick(
        state,
        player,
        "logic_thi_scale_huge_mountain_koopa_shell",
        f"{level_name} - Coins Star",
    )
    has_impossible_coin = rules.can_use_logic_trick(
        state,
        player,
        "logic_thi_impossible_coin",
        f"{level_name} - Coins Star",
    )
    permanent = rules.permanent_coin_collection_enabled(state, player)

    def giant_goomba_coins(count: int) -> int:
        return count * (5 if has_ground_pound else 1)

    def make_route(start_tiny: bool, route_available: bool) -> _route_type:
        sources: dict[str, int] = {}
        children: list[_route_trace_node_type] = []

        def add_source(
                source_id: str,
                label: str,
                value: int,
                available: bool,
        ) -> None:
            children.append(_route_source(source_id, label, value, available))
            if available and value:
                sources[source_id] = value

        has_tiny_piranha = start_tiny and has_tiny_piranha_movement
        has_tiny_main_from_tiny = has_tiny_piranha and has_thi_purple_switches
        has_huge_start = not start_tiny
        has_huge_piranha_from_pipe = has_tiny_piranha and has_warp_pipes
        has_koopa_from_pipe = has_tiny_main_from_tiny and has_warp_pipes

        repeatable_windswept = has_huge_start and (
            has_long_jump or has_triple_jump and has_dive)
        fly_windswept = has_huge_start and has_fly_guy_ascent
        has_windswept = repeatable_windswept or fly_windswept
        has_cannonball = has_windswept and has_cannonball_movement
        has_koopa_from_mountain = has_cannonball and has_upper_movement
        has_koopa_region = (
            has_koopa_from_pipe
            or has_koopa_from_mountain
            or has_koopa_shell_ascent and has_huge_start
        )
        has_top_from_mountain = has_koopa_region and has_upper_movement
        has_top = has_top_from_mountain or has_koopa_shell_ascent and has_huge_start
        has_tiny_main = has_tiny_main_from_tiny or has_koopa_region and has_warp_pipes

        normal_repeatable_top = (
            repeatable_windswept and has_cannonball_movement and has_upper_movement)
        pipe_repeatable_top = has_koopa_from_pipe and has_upper_movement
        repeatable_top = normal_repeatable_top or pipe_repeatable_top
        if has_top and has_warp_pipes and has_upper_movement:
            repeatable_top = True

        one_use_ascents = 0
        if not repeatable_top:
            if has_koopa_shell_ascent and has_huge_start:
                one_use_ascents += 1
            if fly_windswept and has_cannonball_movement and has_upper_movement:
                one_use_ascents += 1

        add_source(
            "tiny_start_goomba",
            "Small Goomba at Tiny Island start",
            1,
            start_tiny and has_goombas,
        )
        add_source(
            "tiny_piranha_area_plant",
            "Piranha Plant in the Tiny Piranha Area",
            1,
            start_tiny and has_tiny_piranha and has_fire_piranha_plants,
        )
        add_source(
            "tiny_main_individual_coins",
            "Individual coins in Tiny Main",
            8,
            start_tiny and has_tiny_main and has_single_yellow_coins,
        )
        add_source(
            "tiny_main_coin_line",
            "Coin line on the Tiny Main wooden plank",
            5,
            start_tiny and has_tiny_main and has_horizontal_coin_lines,
        )
        add_source(
            "tiny_main_three_coin_block",
            "3-Coin Block in Tiny Main",
            3,
            start_tiny and has_tiny_main and has_three_coin_block,
        )
        add_source(
            "tiny_main_goombas",
            "Nine Small Goombas in Tiny Main",
            9,
            start_tiny and has_tiny_main and has_goombas,
        )
        add_source(
            "tiny_main_koopa",
            "Small Koopa in Tiny Main",
            5,
            start_tiny and has_tiny_main and has_koopa_troopa,
        )
        add_source(
            "tiny_impossible_coin",
            "Impossible underground coin on Tiny Island",
            1,
            start_tiny and has_tiny_main and has_single_yellow_coins and has_impossible_coin,
        )
        add_source(
            "tiny_purple_switch_coin",
            "Separated Tiny Island coin",
            1,
            start_tiny
            and has_tiny_main
            and has_thi_purple_switches
            and has_single_yellow_coins,
        )

        has_huge_context = has_huge_start or has_koopa_region
        add_source(
            "huge_lower_giant_goombas",
            "Four Giant Goombas on lower Huge Island",
            giant_goomba_coins(4),
            has_huge_context and has_goombas,
        )
        add_source(
            "huge_start_post",
            "Wooden post at Huge Island start",
            5,
            has_huge_context and has_wooden_posts,
        )
        add_source(
            "huge_beach_coins",
            "Two coins above the Huge Island beach",
            2,
            has_huge_context and has_single_yellow_coins,
        )
        add_source(
            "huge_lower_fly_guys",
            "Two Fly Guys on lower Huge Island",
            4,
            has_huge_context and has_fly_guy,
        )
        add_source(
            "huge_lakitu",
            "Lakitu on Huge Island",
            5,
            has_huge_context and has_lakitu,
        )
        add_source(
            "huge_koopa_troopa",
            "Koopa Troopa on Huge Island",
            5,
            has_huge_context and has_koopa_troopa,
        )
        add_source(
            "huge_lakitu_island_post",
            "Wooden post on Lakitu's island",
            5,
            has_huge_context
            and has_wooden_posts
            and (has_cannon and has_huge_start or has_top and has_long_jump),
        )
        add_source(
            "huge_windswept_line",
            "Coin line in Windswept Valley",
            5,
            has_huge_context and has_windswept and has_horizontal_coin_lines,
        )
        add_source(
            "huge_windswept_giant_goombas",
            "Two Giant Goombas in Windswept Valley",
            giant_goomba_coins(2),
            has_huge_context and has_windswept and has_goombas,
        )
        add_source(
            "huge_cannonball_line",
            "Coin line in the Cannonball area",
            5,
            has_huge_context and has_cannonball and has_horizontal_coin_lines,
        )
        add_source(
            "huge_cannonball_fly_guy",
            "Fly Guy in the Cannonball area",
            2,
            has_huge_context and has_cannonball and has_fly_guy,
        )
        add_source(
            "huge_koopa_region_line",
            "Slanted coin line in Koopa the Quick's area",
            4,
            has_huge_context and has_koopa_region and has_horizontal_coin_lines,
        )
        add_source(
            "huge_koopa_region_giant_goombas",
            "Three Giant Goombas in Koopa the Quick's area",
            giant_goomba_coins(3),
            has_huge_context and has_koopa_region and has_goombas,
        )
        add_source(
            "huge_top_wooden_plank_line",
            "Coin line on the mountaintop wooden plank",
            5,
            has_huge_context and has_top and has_horizontal_coin_lines,
        )
        add_source(
            "huge_top_curved_plank_line",
            "Coin line on the curved Wiggler's Cave plank",
            5,
            has_huge_context and has_top and has_horizontal_coin_lines,
        )
        add_source(
            "huge_top_chuckya",
            "Chuckya at the Huge Island top",
            5,
            has_huge_context and has_top and has_chuckya,
        )

        red_area_children = [
            _route_source(
                "red_area_giant_goombas",
                "Two Giant Goombas in the Red Coins Area",
                giant_goomba_coins(2),
                has_goombas,
            ),
            _route_source(
                "red_area_red_coins",
                "Seven red coins in the Red Coins Area",
                14,
                has_red_coins,
            ),
            _route_source(
                "red_area_wall_kick_red_coin",
                "Wall-kick red coin in the Red Coins Area",
                2,
                has_red_coins and rules.has_action(
                    state, player, "Wall Kick", level_name),
            ),
            _route_source(
                "red_area_blue_coins",
                "Blue coins in the Red Coins Area",
                10,
                has_ground_pound and has_blue_coin_block,
            ),
        ]
        wiggler_children = [
            _route_source(
                "wiggler_cave_coin_lines",
                "Coin lines in Wiggler's Cave",
                10,
                has_horizontal_coin_lines,
            ),
        ]
        piranha_children = [
            _route_source(
                "huge_piranha_area_plants",
                "Fire Piranha Plants in the Huge Piranha Area",
                10,
                has_fire_piranha_plants,
            ),
        ]

        red_area_direct = has_huge_context and has_cannon and has_huge_start
        red_area_terminal = has_huge_context and not red_area_direct and has_top
        wiggler_available = (
            has_huge_context and has_tiny_main and has_warp_pipes and has_ground_pound)
        piranha_direct = has_huge_piranha_from_pipe or (
            has_koopa_region and has_warp_pipes and has_thi_purple_switches)
        piranha_terminal = not has_huge_piranha_from_pipe and has_koopa_region and not piranha_direct

        terminal_groups: list[_route_trace_node_type] = []
        if red_area_terminal:
            terminal_groups.append(_route_trace_node_type(
                "thi_red_coins_area",
                "Red Coins Area dead end",
                sum(child.coins for child in red_area_children if child.available),
                True,
                False,
                red_area_children,
            ))
        if has_huge_context:
            terminal_groups.append(_route_trace_node_type(
                "thi_wiggler_cave",
                "Wiggler's Cave dead end",
                sum(child.coins for child in wiggler_children if child.available)
                if wiggler_available
                else 0,
                wiggler_available,
                False,
                wiggler_children,
            ))
        if piranha_terminal:
            terminal_groups.append(_route_trace_node_type(
                "thi_huge_piranha_area",
                "Huge Piranha Area dead end",
                sum(child.coins for child in piranha_children if child.available),
                True,
                False,
                piranha_children,
            ))

        if permanent or repeatable_top:
            selected_terminal_groups = terminal_groups
        elif has_top:
            selected_terminal_groups = sorted(
                terminal_groups,
                key=lambda group: group.coins,
                reverse=True,
            )[:one_use_ascents]
        else:
            selected_terminal_groups = []
        selected_terminal_ids = {group.source_id for group in selected_terminal_groups}

        def append_group(
                source_id: str,
                label: str,
                available: bool,
                selected: bool,
                group_children: list[_route_trace_node_type],
        ) -> None:
            group = _route_trace_node_type(
                source_id,
                label,
                sum(child.coins for child in group_children if child.available),
                available,
                selected,
                group_children,
            )
            children.append(group)
            if selected and available:
                for child in group_children:
                    if child.available and child.coins:
                        sources[child.source_id] = child.coins

        append_group(
            "thi_red_coins_area",
            "Red Coins Area",
            red_area_direct or red_area_terminal,
            red_area_direct or "thi_red_coins_area" in selected_terminal_ids,
            red_area_children,
        )
        append_group(
            "thi_wiggler_cave",
            "Wiggler's Cave dead end",
            wiggler_available,
            "thi_wiggler_cave" in selected_terminal_ids,
            wiggler_children,
        )
        append_group(
            "thi_huge_piranha_area",
            "Huge Piranha Area",
            has_huge_piranha_from_pipe or has_koopa_region,
            piranha_direct or "thi_huge_piranha_area" in selected_terminal_ids,
            piranha_children,
        )

        route_name = "Tiny entrance route" if start_tiny else "Huge entrance route"
        route_id = "thi_tiny_variant" if start_tiny else "thi_huge_variant"
        return _route_type(route_id, route_name, route_available, sources, children)

    routes = [
        make_route(True, can_enter_tiny),
        make_route(False, can_enter_huge),
    ]
    return _evaluate_route_set(routes, permanent=permanent)


def _rules() -> ModuleType:
    # The lazy import keeps this evaluator free of a Rules <-> CoinLogic cycle.
    from . import Rules
    return Rules


def tick_tock_clock_coins(
        state: CollectionState, player: int, coins: int) -> CoinEvaluation:
    rules = _rules()
    level_name = "Tick Tock Clock"
    has_single_yellow_coins = rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Single Yellow Coins", f"{level_name} - Single Yellow Coins")
    has_red_coins = rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Red Coins", f"{level_name} - Red Coins")
    has_blue_coin_block = rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Blue Coin Blocks", f"{level_name} - Blue Coin Block")
    has_horizontal_coin_lines = rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Horizontal Coin Lines", f"{level_name} - Horizontal Coin Lines")
    has_three_coin_blocks = rules.has_unlock(
        state, player, "coin_object_unlocks",
        "3-Coin Blocks", f"{level_name} - 3-Coin Blocks")
    has_ten_coin_blocks = rules.has_unlock(
        state, player, "coin_object_unlocks",
        "10-Coin Blocks", f"{level_name} - 10-Coin Blocks")
    has_bob_ombs = rules.has_unlock(
        state, player, "enemy_unlocks",
        "Bob-ombs", f"{level_name} - Bob-ombs")

    trace = CoinTraceBuilder()
    trace.add_route("ttc_start", "Starting region", True, (
        coin_source("ttc_start_ten_coin_block",
                "10-Coin Block behind the start", 10, has_ten_coin_blocks),
        coin_source("ttc_start_bob_ombs", "Two Bob-ombs", 2, has_bob_ombs),
        coin_source("ttc_start_cube_coins",
                "Coins above the first turning cube", 2, has_single_yellow_coins),
        coin_source("ttc_second_pendulum_block",
                "3-Coin Block behind the second pendulum", 3, has_three_coin_blocks),
    ))

    has_lower = state.can_reach(
        "Tick Tock Clock - First Clock Hand Area", "Region", player)
    moving_line_route = (
        state.can_reach("Tick Tock Clock Moving", "Region", player)
        or (
            state.can_reach("Tick Tock Clock Stopped", "Region", player)
            and any(rules.has_action(state, player, action, level_name)
                    for action in ("Ledge Grab", "Backflip", "Triple Jump", "Wall Kick"))
        )
    )
    trace.add_route("ttc_lower", "Lower region", has_lower, (
        coin_source("ttc_first_hand_block",
                "3-Coin Block by the first moving hand", 3, has_three_coin_blocks),
        coin_source("ttc_lower_red_coins", "Five lower Red Coins", 10, has_red_coins),
        coin_source(
            "ttc_spinner_red_coins",
            "Three Red Coins reached with the Spinners",
            6,
            has_red_coins
            and rules.has_simple_arbitrary_feature(state, player, "TTC_SPINNERS"),
        ),
        coin_source(
            "ttc_first_pole_coin_line",
            "Slanted coin line by the first pole (moving time, or stopped-time movement)",
            5,
            has_horizontal_coin_lines and moving_line_route,
        ),
    ))

    has_upper = state.can_reach(
        "Tick Tock Clock - Moving Bars Area", "Region", player)
    trace.add_route("ttc_upper", "Upper region", has_upper, (
        coin_source("ttc_heave_ho_blocks",
                "Two 3-Coin Blocks by the Heave-Hos", 6, has_three_coin_blocks),
        coin_source(
            "ttc_blue_coin_block",
            "Blue Coin Block by The Pit and the Pendulums",
            35,
            has_blue_coin_block
            and rules.has_action(state, player, "Ground Pound", level_name),
        ),
    ))

    has_top = state.can_reach("Tick Tock Clock - Top", "Region", player)
    trace.add_route("ttc_top", "Top region", has_top, (
        coin_source("ttc_timed_jumps_block",
                "3-Coin Block above Timed Jumps on Moving Bars",
                3, has_three_coin_blocks),
        coin_source("ttc_four_moving_bars_block",
                "10-Coin Block above Four Moving Bars",
                10, has_ten_coin_blocks),
    ))

    has_top_past_spinners = state.can_reach(
        "Tick Tock Clock - Top Past Spinners", "Region", player)
    trace.add_route(
        "ttc_top_past_spinners", "Top Past Spinners region",
        has_top_past_spinners, (
            coin_source("ttc_past_three_spinners_block",
                    "3-Coin Block past the three spinners",
                    3, has_three_coin_blocks),
            coin_source("ttc_beneath_thwomp_block",
                    "10-Coin Block beneath the Thwomp",
                    10, has_ten_coin_blocks),
            coin_source("ttc_top_clock_hand_block",
                    "10-Coin Block at the top clock hand",
                    10, has_ten_coin_blocks),
            coin_source("ttc_top_central_platform_block",
                    "10-Coin Block on the top central platform",
                    10, has_ten_coin_blocks),
        ))

    assert trace.reachable_coins <= 128
    return trace.evaluation()


def rainbow_ride_coins(
        state: CollectionState, player: int, coins: int) -> CoinEvaluation:
    rules = _rules()
    level_name = "Rainbow Ride"
    has_single_yellow_coins = rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Single Yellow Coins", f"{level_name} - Single Yellow Coins")
    has_red_coins = rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Red Coins", f"{level_name} - Red Coins")
    has_blue_coin_block = rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Blue Coin Blocks", f"{level_name} - Blue Coin Block")
    has_horizontal_coin_lines = rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Horizontal Coin Lines", f"{level_name} - Horizontal Coin Lines")
    has_horizontal_coin_rings = rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Horizontal Coin Rings", f"{level_name} - Horizontal Coin Rings")
    has_vertical_coin_lines = rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Vertical Coin Lines", f"{level_name} - Vertical Coin Lines")
    has_bob_ombs = rules.has_unlock(
        state, player, "enemy_unlocks",
        "Bob-ombs", f"{level_name} - Bob-ombs")
    has_chuckya = rules.has_unlock(
        state, player, "enemy_unlocks",
        "Chuckyas", f"{level_name} - Chuckya")
    has_lakitus = rules.has_unlock(
        state, player, "enemy_unlocks",
        "Lakitus", f"{level_name} - Lakitus")
    has_fly_guy = rules.has_unlock(
        state, player, "enemy_unlocks",
        "Fly Guys", f"{level_name} - Fly Guy")
    has_goomba = rules.has_unlock(
        state, player, "enemy_unlocks",
        "Goombas", f"{level_name} - Goomba")

    trace = CoinTraceBuilder()
    has_carpets = rules.has_simple_arbitrary_feature(
        state, player, "RR_CARPETS")
    has_first_ring_route = has_carpets or (
        rules.can_use_logic_trick(
            state, player, "logic_rr_initial_coins_without_carpets", level_name)
    )
    trace.add_route("rr_initial", "Starting region", True, (
        coin_source(
            "rr_first_platform_ring",
            "Coin ring at the first carpet platform",
            8,
            has_horizontal_coin_rings and has_first_ring_route,
        ),
    ))

    has_beneath_pole = state.can_reach(
        "Rainbow Ride - Beneath the Pole", "Region", player)
    trace.add_route("rr_beneath_pole", "Beneath the Pole region",
                    has_beneath_pole, (
        coin_source("rr_fly_guy_line", "Coin line by the Fly Guy",
                5, has_horizontal_coin_lines),
        coin_source("rr_fly_guy", "Fly Guy", 2, has_fly_guy),
        coin_source("rr_first_swing_line",
                "Vertical coin line by the first swing",
                5, has_vertical_coin_lines),
        coin_source("rr_first_donut_lift_coins",
                "Coins on the first Donut Lifts",
                4, has_single_yellow_coins),
        coin_source("rr_second_swing_line",
                "Coin line before the second swing",
                5, has_horizontal_coin_lines),
        coin_source("rr_tricky_triangles_line",
                "Slanted coin line before Tricky Triangles",
                5, has_horizontal_coin_lines),
        coin_source("rr_beneath_pole_goomba", "Goomba", 1, has_goomba),
    ))

    has_maze = state.can_reach("Rainbow Ride - Maze", "Region", player)
    has_ground_pound = rules.has_action(
        state, player, "Ground Pound", level_name)
    has_wall_kick = rules.has_action(state, player, "Wall Kick", level_name)
    has_maze_red_coin_trick = rules.can_use_logic_trick(
        state, player, "logic_rr_maze_coins_ledge_grab_and_carpets",
        "Rainbow Ride - Coins Amassed in a Maze")
    trace.add_route("rr_maze", "Maze region", has_maze, (
        coin_source("rr_maze_coin_rings",
                "Two coin rings at the spinning platforms",
                16, has_horizontal_coin_rings),
        coin_source("rr_maze_lakitus", "Two Lakitus", 10, has_lakitus),
        coin_source("rr_maze_bob_ombs", "Two Bob-ombs", 2, has_bob_ombs),
        coin_source("rr_maze_blue_coin",
                "First Blue Coin from the Maze block",
                5, has_blue_coin_block and has_ground_pound),
        coin_source("rr_maze_wall_kick_blue_coins",
                "Remaining Maze Blue Coins with Wall Kick",
                25, has_blue_coin_block and has_ground_pound and has_wall_kick),
        coin_source(
            "rr_maze_movement_red_coin",
            "Maze Red Coin reached with Long Jump or Wall Kick",
            2,
            has_red_coins and (
                rules.has_action(state, player, "Long Jump", level_name)
                or has_wall_kick
                or has_maze_red_coin_trick),
        ),
    ))

    trace.add_route(
        "rr_red_coin_star_route",
        "All Red Coins route",
        _can_collect_all_rr_red_coins(state, player),
        (coin_source("rr_other_red_coins", "Seven remaining Red Coins",
                 14, has_red_coins),),
    )
    trace.add_route(
        "rr_carpets", "Carpets region",
        state.can_reach("Rainbow Ride - Carpets", "Region", player), (
            coin_source("rr_second_carpet_platform_coin",
                    "Coin on the second carpet's grey platform",
                    1, has_single_yellow_coins),
            coin_source("rr_second_carpet_air_coin",
                    "Coin in the air along the second carpet",
                    1, has_single_yellow_coins),
        ))
    trace.add_route(
        "rr_house", "House region",
        state.can_reach("Rainbow Ride - House", "Region", player), (
            coin_source("rr_house_donut_lift_line",
                    "Vertical coin line on the House-path Donut Lifts",
                    5, has_vertical_coin_lines),
            coin_source("rr_house_floor_line",
                    "Coin line on the Big House floor",
                    5, has_horizontal_coin_lines),
            coin_source("rr_house_glass_platform_line",
                    "Coin line on the second glass platform",
                    5, has_horizontal_coin_lines),
            coin_source("rr_house_return_line",
                    "Airborne coin line before returning to the House",
                    5, has_horizontal_coin_lines),
        ))
    trace.add_route(
        "rr_cruiser", "Cruiser region",
        state.can_reach("Rainbow Ride - Cruiser", "Region", player), (
            coin_source("rr_cruiser_bob_ombs", "Two Cruiser Bob-ombs",
                    2, has_bob_ombs),
            coin_source("rr_ship_pole_ring", "Coin ring around the ship pole",
                    8, has_horizontal_coin_rings),
        ))
    trace.add_route(
        "rr_somewhere_over_the_rainbow",
        "Somewhere Over the Rainbow location route",
        state.can_reach(
            "Rainbow Ride - Somewhere Over the Rainbow", "Location", player),
        (coin_source("rr_somewhere_chuckya", "Chuckya", 5, has_chuckya),),
    )

    assert coins <= 146
    return trace.evaluation()


def princess_secret_slide_coins(
        state: CollectionState, player: int, coins: int) -> CoinEvaluation:
    rules = _rules()
    level_name = "The Princess's Secret Slide"
    trace = CoinTraceBuilder()
    trace.add_route("pss_course", "Secret Slide", True, (
        coin_source(
            "pss_single_yellow_coins",
            "Single Yellow Coins",
            20,
            rules.has_unlock(
                state, player, "coin_object_unlocks",
                "Single Yellow Coins",
                "Princess's Secret Slide - Single Yellow Coins"),
        ),
        coin_source(
            "pss_horizontal_coin_lines",
            "Horizontal Coin Lines",
            30,
            rules.has_unlock(
                state, player, "coin_object_unlocks",
                "Horizontal Coin Lines",
                "Princess's Secret Slide - Horizontal Coin Lines"),
        ),
        coin_source(
            "pss_blue_coin_block",
            "Blue Coin Block with Ground Pound",
            30,
            rules.has_action(state, player, "Ground Pound", level_name)
            and rules.has_unlock(
                state, player, "coin_object_unlocks",
                "Blue Coin Blocks",
                "Princess's Secret Slide - Blue Coin Block"),
        ),
    ))
    assert trace.reachable_coins <= 80
    return trace.evaluation()


def secret_aquarium_coins(
        state: CollectionState, player: int, coins: int) -> CoinEvaluation:
    rules = _rules()
    trace = CoinTraceBuilder()
    trace.add_route("sa_course", "Secret Aquarium", True, (
        coin_source(
            "sa_red_coins", "Eight Red Coins", 16,
            rules.has_unlock(
                state, player, "coin_object_unlocks",
                "Red Coins", "Secret Aquarium - Red Coins"),
        ),
        coin_source(
            "sa_horizontal_coin_ring", "Horizontal Coin Ring", 8,
            rules.has_unlock(
                state, player, "coin_object_unlocks",
                "Horizontal Coin Rings",
                "Secret Aquarium - Horizontal Coin Rings"),
        ),
        coin_source(
            "sa_vertical_coin_rings", "Vertical Coin Rings", 32,
            rules.has_unlock(
                state, player, "coin_object_unlocks",
                "Vertical Coin Rings",
                "Secret Aquarium - Vertical Coin Rings"),
        ),
    ))
    assert trace.reachable_coins <= 56
    return trace.evaluation()


def wing_mario_over_the_rainbow_coins(
        state: CollectionState, player: int, coins: int) -> CoinEvaluation:
    rules = _rules()
    level_name = "Wing Mario Over the Rainbow"
    has_wing_cap_item = rules.has_wing_cap(state, player, level_name)
    has_red_coins = rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Red Coins", f"{level_name} - Red Coins")
    has_horizontal_coin_rings = rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Horizontal Coin Rings", f"{level_name} - Horizontal Coin Rings")
    has_vertical_coin_rings = rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Vertical Coin Rings", f"{level_name} - Vertical Coin Rings")
    has_leap_of_faith = rules.has_logic_trick(
        state, player, "logic_wmotr_leap_of_faith")
    has_leap_without_ledge_grab = rules.has_logic_trick(
        state, player, "logic_wmotr_leap_of_faith_without_ledge_grab")
    can_long_jump_leap = (
        rules.has_action(state, player, "Long Jump", level_name)
        and (has_leap_of_faith or has_leap_without_ledge_grab)
    )
    has_cannon_region = state.can_reach(
        "Wing Mario Over the Rainbow - Cannon", "Region", player)
    has_flight_route = (
        has_cannon_region
        or (
            has_wing_cap_item
            and rules.has_action(state, player, "Triple Jump", level_name)
        )
    )

    trace = CoinTraceBuilder()
    trace.add_route("wmotr_initial", "Starting cloud", True, (
        coin_source("wmotr_initial_red_coin", "Initial Red Coin", 2, has_red_coins),
    ))
    trace.add_route("wmotr_cannon_only", "Cannon region", has_cannon_region, (
        coin_source("wmotr_cannon_red_coins",
                "Four Red Coins requiring the Cannon region",
                8, has_red_coins),
    ))

    trace.add_route("wmotr_flight_route", "Flight route", has_flight_route, (
        coin_source("wmotr_flight_red_coins", "Three flight-path Red Coins",
                6, has_red_coins),
        coin_source("wmotr_rainbow_coin_rings",
                "Four vertical coin rings around the rainbows",
                32, has_vertical_coin_rings),
        coin_source("wmotr_cloud_coin_ring",
                "Horizontal coin ring below the pole cloud",
                8, has_horizontal_coin_rings),
    ))

    fallback_selected = not has_flight_route
    long_jump_first_coin = has_red_coins and can_long_jump_leap
    long_jump_second_coin = (
        long_jump_first_coin
        and (
            has_leap_without_ledge_grab
            or rules.has_action(state, player, "Ledge Grab", level_name)
        )
    )
    wing_cap_fallback_coin = (
        not long_jump_first_coin
        and has_red_coins
        and has_wing_cap_item
        and (has_leap_of_faith or has_leap_without_ledge_grab)
    )
    trace.add_route(
        "wmotr_leap_fallback",
        "Leap of Faith fallback (used only when the flight route is unavailable)",
        True,
        (
            coin_source("wmotr_long_jump_first_red_coin",
                    "First Long Jump Leap of Faith Red Coin",
                    2, long_jump_first_coin),
            coin_source("wmotr_long_jump_second_red_coin",
                    "Second Long Jump Leap of Faith Red Coin",
                    2, long_jump_second_coin),
            coin_source("wmotr_wing_cap_fallback_red_coin",
                    "Wing Cap slow-fall Leap of Faith Red Coin",
                    2, wing_cap_fallback_coin),
        ),
        selected=fallback_selected,
    )

    assert trace.reachable_coins <= 56
    return trace.evaluation()


def tower_of_the_wing_cap_coins(
        state: CollectionState, player: int, coins: int) -> CoinEvaluation:
    rules = _rules()
    level_name = "Tower of the Wing Cap"
    has_coin_mastery = rules.has_logic_trick(
        state, player, "logic_totwc_coin_mastery")
    has_single_yellow_coins = rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Single Yellow Coins", f"{level_name} - Single Yellow Coins")
    has_red_coins = rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Red Coins", f"{level_name} - Red Coins")
    has_vertical_coin_rings = rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Vertical Coin Rings", f"{level_name} - Vertical Coin Rings")
    has_wing_cap_item = rules.has_wing_cap(state, player, level_name)

    trace = CoinTraceBuilder()
    trace.add_route("totwc_course", "Course coin objects", True, (
        coin_source("totwc_single_yellow_coins",
                "Single Yellow Coins", 15, has_single_yellow_coins),
        coin_source("totwc_red_coins", "Eight Red Coins", 16, has_red_coins),
    ))
    trace.add_route(
        "totwc_standard_ring_route",
        "Coin rings without Coin Mastery",
        not has_coin_mastery,
        (coin_source("totwc_standard_ring_coins",
                 "Reachable vertical Coin Ring coins",
                 16, has_vertical_coin_rings),),
        selected=not has_coin_mastery,
    )
    trace.add_route(
        "totwc_mastery_ring_route",
        "Coin Mastery route",
        has_coin_mastery,
        (
            coin_source("totwc_mastery_ring_coins",
                    "Coin Ring coins reachable with Coin Mastery",
                    20, has_vertical_coin_rings),
            coin_source("totwc_mastery_wing_cap_ring_coins",
                    "Additional Coin Ring coins with Wing Cap",
                    12, has_vertical_coin_rings and has_wing_cap_item),
        ),
        selected=has_coin_mastery,
    )

    uncapped_coins = trace.reachable_coins
    assert uncapped_coins <= 63
    logic_cap = 63 if has_coin_mastery else 31
    option_cap = state.multiworld.worlds[
        player].options.tower_of_the_wing_cap_coinsanity_max_coins.value
    reachable_coins = min(uncapped_coins, logic_cap, option_cap)
    if reachable_coins < uncapped_coins:
        trace.add_source(
            "totwc_coin_cap",
            f"Coins excluded by the {min(logic_cap, option_cap)}-coin logic/option cap",
            uncapped_coins - reachable_coins,
            True,
            counted=False,
        )
    return trace.evaluation(reachable_coins)


def vanish_cap_under_the_moat_coins(
        state: CollectionState, player: int, coins: int) -> CoinEvaluation:
    rules = _rules()
    level_name = "Vanish Cap Under the Moat"
    has_single_yellow_coins = rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Single Yellow Coins", f"{level_name} - Single Yellow Coins")
    has_red_coins = rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Red Coins", f"{level_name} - Red Coins")
    has_horizontal_coin_lines = rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Horizontal Coin Lines", f"{level_name} - Horizontal Coin Lines")
    has_three_coin_block = rules.has_unlock(
        state, player, "coin_object_unlocks",
        "3-Coin Blocks", f"{level_name} - 3-Coin Block")
    has_movement = any(
        rules.has_action(state, player, action, level_name)
        for action in ("Triple Jump", "Ledge Grab", "Side Flip", "Backflip", "Wall Kick")
    )
    has_checkerboards = rules.has_checkerboard_platforms(
        state, player, level_name)
    can_drop_to_checkerboards = rules.can_use_logic_trick(
        state, player, "logic_vcutm_drop_to_checkerboard_platforms",
        "Vanish Cap Under the Moat - Coins Star")
    can_crawl_back_then_drop = rules.can_use_logic_trick(
        state, player,
        "logic_vcutm_drop_to_checkerboard_platforms_after_crawling_back_up",
        "Vanish Cap Under the Moat - Coins Star")

    earlier_sources = (
        coin_source("vcutm_bottom_slide_line",
                "Coin line at the bottom of the slide",
                5, has_horizontal_coin_lines),
        coin_source("vcutm_earlier_red_coins",
                "Four Red Coins before the checkerboards",
                8, has_red_coins),
    )
    later_route = (
        has_movement or can_drop_to_checkerboards or can_crawl_back_then_drop)
    later_sources = (
        coin_source("vcutm_turning_lifts_block",
                "3-Coin Block before the turning lifts",
                3, has_three_coin_block),
        coin_source("vcutm_checkerboard_red_coins",
                "Four Red Coins at the checkerboards",
                8, has_checkerboards and has_red_coins),
        coin_source("vcutm_end_marker_coins",
                "Coins by the final star marker",
                3,
                has_checkerboards
                and has_single_yellow_coins
                and rules.has_vanish_cap(state, player, level_name)),
    )
    earlier_total = sum(source.coins for source in earlier_sources
                        if source.available)
    later_total = sum(source.coins for source in later_sources
                      if source.available) if later_route else 0

    combines_routes = has_movement or can_crawl_back_then_drop
    drop_only = (
        can_drop_to_checkerboards
        and not combines_routes
    )
    earlier_selected = combines_routes or not drop_only or earlier_total >= later_total
    later_selected = combines_routes or (drop_only and later_total > earlier_total)

    trace = CoinTraceBuilder()
    trace.add_route(
        "vcutm_earlier_slide_route",
        "Earlier slide route",
        True,
        earlier_sources,
        selected=earlier_selected,
    )
    trace.add_route(
        "vcutm_later_checkerboard_route",
        (
            "Later checkerboard route "
            "(combined after crawling back, otherwise compared with the earlier route)"
        ),
        later_route,
        later_sources,
        selected=later_selected,
    )

    assert trace.reachable_coins <= 27
    return trace.evaluation()


def cavern_of_the_metal_cap_coins(
        state: CollectionState, player: int, coins: int) -> CoinEvaluation:
    rules = _rules()
    level_name = "Cavern of the Metal Cap"
    has_red_coins = rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Red Coins", f"{level_name} - Red Coins")
    has_horizontal_coin_lines = rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Horizontal Coin Lines", f"{level_name} - Horizontal Coin Lines")
    has_horizontal_coin_rings = rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Horizontal Coin Rings", f"{level_name} - Horizontal Coin Rings")
    has_snufits = rules.has_unlock(
        state, player, "enemy_unlocks",
        "Snufits", f"{level_name} - Snufits")
    has_deep_water_route = (
        rules.has_metal_cap(state, player, level_name)
        or rules.can_use_logic_trick(
            state, player,
            "logic_cotmc_deep_underwater_coins_without_metal_cap",
            "Cavern of the Metal Cap - Coins Star")
    )

    trace = CoinTraceBuilder()
    trace.add_route("cotmc_course", "Course route", True, (
        coin_source("cotmc_underwater_slope_line",
                "Coin line under the water after the first Metal Cap Block",
                5, has_horizontal_coin_lines),
        coin_source("cotmc_rock_bridge_line",
                "Coin line after the rock bridge",
                5, has_horizontal_coin_lines),
        coin_source("cotmc_snufits", "Four Snufits", 8, has_snufits),
        coin_source("cotmc_initial_red_coins", "Four initial Red Coins",
                8, has_red_coins),
    ))
    trace.add_route(
        "cotmc_deep_water",
        "Deep underwater route (Metal Cap or Deep Underwater Coins trick)",
        has_deep_water_route,
        (
            coin_source("cotmc_underwater_ring",
                    "Coin ring around the underwater star marker",
                    8, has_horizontal_coin_rings),
            coin_source("cotmc_stream_bottom_line",
                    "Coin line on the stream bottom",
                    5, has_horizontal_coin_lines),
            coin_source("cotmc_deep_red_coins",
                    "Four deep-water Red Coins",
                    8, has_red_coins),
        ))
    assert trace.reachable_coins <= 47
    return trace.evaluation()


def bowser_in_the_dark_world_coins(
        state: CollectionState, player: int, coins: int) -> CoinEvaluation:
    rules = _rules()
    level_name = "Bowser in the Dark World"
    has_single_yellow_coins = rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Single Yellow Coins", f"{level_name} - Single Yellow Coins")
    has_red_coins = rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Red Coins", f"{level_name} - Red Coins")
    has_horizontal_coin_lines = rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Horizontal Coin Lines", f"{level_name} - Horizontal Coin Lines")
    has_horizontal_coin_rings = rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Horizontal Coin Rings", f"{level_name} - Horizontal Coin Rings")
    has_three_coin_block = rules.has_unlock(
        state, player, "coin_object_unlocks",
        "3-Coin Blocks", f"{level_name} - 3-Coin Block")
    has_goombas = rules.has_unlock(
        state, player, "enemy_unlocks",
        "Goombas", f"{level_name} - Goombas")
    has_purple_switches = rules.has_purple_switches(
        state, player, level_name)
    has_slope_access = (
        has_purple_switches
        or rules.can_use_logic_trick(
            state, player, "logic_bitdw_purple_switch_bypass", level_name)
    )

    trace = CoinTraceBuilder()
    trace.add_route("bitdw_before_slope", "Before the Purple Switch slope", True, (
        coin_source("bitdw_coin_rings", "Three rings of eight coins",
                24, has_horizontal_coin_rings),
        coin_source("bitdw_coin_lines", "Two lines of five coins",
                10, has_horizontal_coin_lines),
        coin_source("bitdw_single_coins_before_slope",
                "Single Yellow Coins before the slope",
                18, has_single_yellow_coins),
        coin_source("bitdw_three_coin_block", "3-Coin Block",
                3, has_three_coin_block),
        coin_source("bitdw_goombas", "Six Goombas", 6, has_goombas),
        coin_source("bitdw_red_coins_before_slope",
                "Six Red Coins before the slope", 12, has_red_coins),
    ))
    trace.add_route(
        "bitdw_slope",
        "Purple Switch slope (Purple Switches or bypass trick)",
        has_slope_access,
        (coin_source("bitdw_slope_single_coins",
                 "Three coins on the slope",
                 3, has_single_yellow_coins),),
    )
    trace.add_route(
        "bitdw_slope_red_coins",
        "Final slope Red Coins (Purple Switches only)",
        has_purple_switches,
        (coin_source("bitdw_final_red_coins",
                 "Final two Red Coins", 4, has_red_coins),),
    )
    assert trace.reachable_coins <= 80
    return trace.evaluation()


def bowser_in_the_fire_sea_coins(
        state: CollectionState, player: int, coins: int) -> CoinEvaluation:
    rules = _rules()
    level_name = "Bowser in the Fire Sea"
    has_single_yellow_coins = rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Single Yellow Coins", f"{level_name} - Single Yellow Coins")
    has_red_coins = rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Red Coins", f"{level_name} - Red Coins")
    has_horizontal_coin_lines = rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Horizontal Coin Lines", f"{level_name} - Horizontal Coin Lines")
    has_horizontal_coin_rings = rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Horizontal Coin Rings", f"{level_name} - Horizontal Coin Rings")
    has_vertical_coin_lines = rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Vertical Coin Lines", f"{level_name} - Vertical Coin Lines")
    has_three_coin_block = rules.has_unlock(
        state, player, "coin_object_unlocks",
        "3-Coin Blocks", f"{level_name} - 3-Coin Block")
    has_ten_coin_block = rules.has_unlock(
        state, player, "coin_object_unlocks",
        "10-Coin Blocks", f"{level_name} - 10-Coin Block")
    has_bob_omb = rules.has_unlock(
        state, player, "enemy_unlocks",
        "Bob-ombs", f"{level_name} - Bob-omb")
    has_bullies = rules.has_unlock(
        state, player, "enemy_unlocks",
        "Bullies", f"{level_name} - Bullies")
    has_goombas = rules.has_unlock(
        state, player, "enemy_unlocks",
        "Goombas", f"{level_name} - Goombas")
    has_climb = rules.has_action(state, player, "Climb", level_name)
    has_lava_damage_boosting = rules.can_use_logic_trick(
        state, player, "logic_lava_damage_boosting",
        "Bowser in the Fire Sea - Coins Star")

    trace = CoinTraceBuilder()
    trace.add_route("bitfs_start", "Starting section", True, (
        coin_source("bitfs_start_single_coins",
                "Coins on the first lava platforms",
                2, has_single_yellow_coins),
        coin_source("bitfs_second_sinking_platform_line",
                "Coin line on the second sinking platform",
                5, has_horizontal_coin_lines),
        coin_source("bitfs_first_ring", "Coin ring by the first Bully",
                8, has_horizontal_coin_rings),
        coin_source("bitfs_first_bully", "First Bully", 1, has_bullies),
        coin_source("bitfs_start_goombas", "Three Goombas", 3, has_goombas),
        coin_source("bitfs_start_red_coins", "Two initial Red Coins",
                4, has_red_coins),
    ))
    trace.add_route(
        "bitfs_rising_platform_block",
        "3-Coin Block after the rising pole platform (Climb or Lava Damage Boosting)",
        has_climb or has_lava_damage_boosting,
        (coin_source("bitfs_three_coin_block",
                 "3-Coin Block", 3, has_three_coin_block),),
    )
    trace.add_route("bitfs_climb", "Upper course reached with Climb", has_climb, (
        coin_source("bitfs_elevator_line",
                "Coin line after the elevator",
                5, has_horizontal_coin_lines),
        coin_source("bitfs_wire_grid_ring",
                "Coin ring beneath the wire grid",
                8, has_horizontal_coin_rings),
        coin_source("bitfs_vertical_drop_line",
                "Vertical coin line after the second block",
                5, has_vertical_coin_lines),
        coin_source("bitfs_bob_omb_slope_line",
                "Sloped coin line before the Bob-omb",
                5, has_horizontal_coin_lines),
        coin_source("bitfs_ten_coin_block",
                "10-Coin Block by the Bob-omb",
                10, has_ten_coin_block),
        coin_source("bitfs_third_sinking_platform_line",
                "Coin line on the third sinking platform",
                5, has_horizontal_coin_lines),
        coin_source("bitfs_bob_omb", "Bob-omb", 1, has_bob_omb),
        coin_source("bitfs_upper_bullies", "Three upper Bullies",
                3, has_bullies),
        coin_source("bitfs_upper_red_coins", "Six upper Red Coins",
                12, has_red_coins),
    ))
    assert trace.reachable_coins <= 80
    return trace.evaluation()


def bowser_in_the_sky_coins(
        state: CollectionState, player: int, coins: int) -> CoinEvaluation:
    rules = _rules()
    level_name = "Bowser in the Sky"
    has_single_yellow_coins = rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Single Yellow Coins", f"{level_name} - Single Yellow Coins")
    has_red_coins = rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Red Coins", f"{level_name} - Red Coins")
    has_horizontal_coin_lines = rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Horizontal Coin Lines", f"{level_name} - Horizontal Coin Lines")
    has_bob_ombs = rules.has_unlock(
        state, player, "enemy_unlocks",
        "Bob-ombs", f"{level_name} - Bob-ombs")
    has_chuckya = rules.has_unlock(
        state, player, "enemy_unlocks",
        "Chuckyas", f"{level_name} - Chuckya")
    has_fire_piranha_plants = rules.has_unlock(
        state, player, "enemy_unlocks",
        "Fire Piranha Plants", f"{level_name} - Fire Piranha Plants")
    has_goombas = rules.has_unlock(
        state, player, "enemy_unlocks",
        "Goombas", f"{level_name} - Goombas")
    has_whomp = rules.has_unlock(
        state, player, "enemy_unlocks",
        "Whomps", f"{level_name} - Whomp")
    has_ground_pound = rules.has_action(
        state, player, "Ground Pound", level_name)

    trace = CoinTraceBuilder()
    trace.add_route("bits_start", "Starting region", True, (
        coin_source("bits_tilting_w_coins",
                "Coins on the tilting W platform",
                3, has_single_yellow_coins),
        coin_source("bits_start_goombas", "Two Goombas", 2, has_goombas),
        coin_source("bits_start_red_coins", "Three initial Red Coins",
                6, has_red_coins),
        coin_source("bits_start_fire_piranha",
                "Initial Fire Piranha Plant",
                1, has_fire_piranha_plants),
        coin_source("bits_whomp_platform_lines",
                "Two coin lines beneath the Whomp",
                10, has_horizontal_coin_lines),
        coin_source("bits_whomp_jump_coins",
                "Whomp coins available without Ground Pound",
                5, has_whomp),
        coin_source("bits_whomp_ground_pound_coins",
                "Additional Whomp coins with Ground Pound",
                5, has_whomp and has_ground_pound),
    ))
    trace.add_route(
        "bits_chuckya",
        "Chuckya region",
        state.can_reach("Bowser in the Sky - Chuckya", "Region", player),
        (
            coin_source("bits_chuckya_enemy", "Chuckya", 5, has_chuckya),
            coin_source("bits_chuckya_goomba", "Goomba", 1, has_goombas),
            coin_source("bits_raised_steps_coins",
                    "Coins on the raised steps",
                    6, has_single_yellow_coins),
        ))
    trace.add_route(
        "bits_arrow_ride",
        "Arrow Ride region",
        state.can_reach(
            "Bowser in the Sky - Arrow Ride", "Region", player),
        (
            coin_source("bits_suction_platform_line",
                    "Coin line on the suction-cup platform",
                    5, has_horizontal_coin_lines),
            coin_source("bits_arrow_ride_red_coins",
                    "Three Arrow Ride Red Coins",
                    6, has_red_coins),
            coin_source("bits_spinning_platform_coins",
                    "Coins on the spinning platform after the fifth Red Coin",
                    3, has_single_yellow_coins),
            coin_source("bits_arrow_ride_bob_ombs",
                    "Two Arrow Ride Bob-ombs", 2, has_bob_ombs),
            coin_source("bits_arrow_ride_fire_piranha",
                    "Arrow Ride Fire Piranha Plant",
                    1, has_fire_piranha_plants),
        ))
    trace.add_route(
        "bits_top",
        "Top region",
        state.can_reach("Bowser in the Sky - Top", "Region", player),
        (
            coin_source("bits_top_goombas", "Four top Goombas", 4, has_goombas),
            coin_source("bits_top_bob_ombs", "Two top Bob-ombs", 2, has_bob_ombs),
            coin_source("bits_top_red_coins", "Two top Red Coins",
                    4, has_red_coins),
            coin_source("bits_final_rotating_platform_line",
                    "Coin line before the final rotating platforms",
                    5, has_horizontal_coin_lines),
        ))
    assert trace.reachable_coins <= 76
    return trace.evaluation()


COIN_EVALUATORS: dict[str, CoinTraceEvaluator] = {
    "Bob-omb Battlefield": evaluate_bob_omb_battlefield_coins,
    "Whomp's Fortress": evaluate_whomps_fortress_coins,
    "Jolly Roger Bay": evaluate_jolly_roger_bay_coins,
    "Cool, Cool Mountain": evaluate_cool_cool_mountain_coins,
    "Big Boo's Haunt": evaluate_big_boos_haunt_coins,
    "Hazy Maze Cave": evaluate_hazy_maze_cave_coins,
    "Lethal Lava Land": lethal_lava_land_coins,
    "Shifting Sand Land": shifting_sand_land_coins,
    "Dire, Dire Docks": dire_dire_docks_coins,
    "Snowman's Land": snowmans_land_coins,
    "Wet-Dry World": wet_dry_world_coin_evaluation,
    "Tall, Tall Mountain": tall_tall_mountain_coins,
    "Tiny-Huge Island": tiny_huge_island_coin_evaluation,
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


RED_COIN_EVALUATORS: dict[str, RedCoinEvaluator] = {
    "Bob-omb Battlefield": _can_collect_all_bob_red_coins,
    "Whomp's Fortress": _can_collect_all_wf_red_coins,
    "Jolly Roger Bay": _can_collect_all_jrb_red_coins,
    "Cool, Cool Mountain": lambda state, player: _has_red_coins(
        state, player, "Cool, Cool Mountain"),
    "Big Boo's Haunt": lambda state, player: _red_coins_and_region(
        state, player, "Big Boo's Haunt", "Big Boo's Haunt - Second Floor"),
    "Hazy Maze Cave": _can_collect_all_hmc_red_coins,
    "Lethal Lava Land": _can_collect_all_lll_red_coins,
    "Shifting Sand Land": _can_collect_all_ssl_red_coins,
    "Dire, Dire Docks": _can_collect_all_ddd_red_coins,
    "Snowman's Land": lambda state, player: _red_coins_and_region(
        state, player, "Snowman's Land", "Snowman's Land - Upper"),
    "Wet-Dry World": _can_collect_all_wdw_red_coins,
    "Tall, Tall Mountain": lambda state, player: _red_coins_and_region(
        state, player, "Tall, Tall Mountain", "Tall, Tall Mountain - Upper"),
    "Tiny-Huge Island": _can_collect_all_thi_red_coins,
    "Tick Tock Clock": _can_collect_all_ttc_red_coins,
    "Rainbow Ride": _can_collect_all_rr_red_coins,
    "The Secret Aquarium": lambda state, player: _has_red_coins(
        state, player, "Secret Aquarium"),
    "Wing Mario Over the Rainbow": _can_collect_all_wmotr_red_coins,
    "Tower of the Wing Cap": lambda state, player: _has_red_coins(
        state, player, "Tower of the Wing Cap"),
    "Vanish Cap Under the Moat": _can_collect_all_vcutm_red_coins,
    "Cavern of the Metal Cap": _can_collect_all_cotmc_red_coins,
    "Bowser in the Dark World": _can_collect_all_bitdw_red_coins,
    "Bowser in the Fire Sea": _can_collect_all_bitfs_red_coins,
    "Bowser in the Sky": lambda state, player: _red_coins_and_region(
        state, player, "Bowser in the Sky", "Bowser in the Sky - Top"),
}
