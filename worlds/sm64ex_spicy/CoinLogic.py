from __future__ import annotations

import dataclasses
from contextvars import ContextVar
from collections.abc import Callable
from dataclasses import dataclass
from functools import cache
from types import ModuleType
from typing import TYPE_CHECKING, Any

from BaseClasses import CollectionState
from rule_builder.rules import And, False_, Or, Rule, True_

from .RuleBuilder import CoinEvaluation, CoinSourceTrace, HasUnlock, LogicTrick

if TYPE_CHECKING:
    from . import SM64World


CoinTraceEvaluator = Callable[[CollectionState, int, int], CoinEvaluation]
_coin_rule_context: ContextVar[tuple[CollectionState, int, str] | None] = ContextVar(
    "sm64_coin_rule_context", default=None)


def _coin_trace(
        source_id: str,
        label: str,
        coins: int,
        available: bool,
        *,
        counted: bool | None = None,
        children: tuple[CoinSourceTrace, ...] = (),
        red_coin_ids: frozenset[int] = frozenset(),
        max_coins: int | None = None,
        reachable_red_coin_ids_when_uncounted: frozenset[int] = frozenset(),
) -> CoinSourceTrace:
    requirement_rule = None
    original_available = available
    context = _coin_rule_context.get()
    if context is not None:
        state, player, course_name = context
        requirement_rule = get_coin_requirement_rule(course_name, source_id, state, player)
        if requirement_rule is not None:
            rule_available = requirement_rule(state)
            available = rule_available
    if counted is None:
        counted = available and original_available
    return CoinSourceTrace(
        source_id, label, coins, counted, available, children, red_coin_ids,
        max_coins, reachable_red_coin_ids_when_uncounted, requirement_rule)


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
            red_coin_ids: frozenset[int] = frozenset(),
            max_coins: int | None = None,
    ) -> None:
        source = _coin_trace(
            source_id, label, coins, available, counted=counted, children=children,
            red_coin_ids=red_coin_ids, max_coins=max_coins)
        self.children.append(source)
        if source.counted:
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
            _coin_trace(
                source.source_id,
                source.label,
                source.coins,
                available and source.available,
                counted=counted and source.available,
                children=source.children,
                red_coin_ids=source.red_coin_ids,
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
        self.children.append(_coin_trace(
            route_id, label, displayed_coins, available,
            counted=counted, children=source_traces))

    def evaluation(self, reachable_coins: int | None = None) -> CoinEvaluation:
        if reachable_coins is None:
            reachable_coins = self.reachable_coins
        return CoinEvaluation(reachable_coins, tuple(self.children))


def _has_red_coins(state: CollectionState, player: int, level_name: str) -> bool:
    from . import Rules

    return Rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Red Coins", f"{level_name} - Red Coins")



def coin_source(
        source_id: str,
        label: str,
        coins: int,
        available: bool,
        *,
        counted: bool | None = None,
        children: tuple[CoinSourceTrace, ...] = (),
        red_coin_ids: frozenset[int] = frozenset(),
) -> CoinSourceTrace:
    return _coin_trace(
        source_id, label, coins, available, counted=counted,
        children=children, red_coin_ids=red_coin_ids)


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
    assert reachable_coins <= maximum, [
        (trace.source_id, trace.coins) for trace in traces if trace.counted]
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
        coin_source("main_red_coins", "Seven Red Coins outside the island", 14, has_red_coins,
                    red_coin_ids=frozenset(range(1, 8))),
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
            red_coin_ids=frozenset({8}),
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
            red_coin_ids=frozenset({8}),
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
            red_coin_ids=frozenset({8}),
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
        "Thwomps and Grindels", f"{level_name} - Thwomps")

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
        coin_source("initial_red_coins", "Five initially reachable Red Coins", 10, has_red_coins,
                    red_coin_ids=frozenset(range(1, 6))),
        coin_source("thwomp_red_coin", "Red Coin on the Thwomp", 2,
                has_red_coins and has_thwomp, red_coin_ids=frozenset({6})),
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
                has_top and has_red_coins, red_coin_ids=frozenset({7, 8})),
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
        coin_source("lower_red_coins", "Four initially reachable Red Coins", 8, has_red_coins,
                    red_coin_ids=frozenset(range(1, 5))),
    ]

    has_pillar_route = (
        Rules.has_action(state, player, "Climb", level_name)
        or has_pillar_red_coin_moves
        or has_pillar_red_coin_cannon
    )
    pillar_children = (
        coin_source("pillar_red_coin", "Red Coin on the stone pillar", 2,
                has_pillar_route and has_red_coins, red_coin_ids=frozenset({5})),
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
            red_coin_ids=frozenset({6, 7, 8}),
        ),
        coin_source(
            "ship_alternative_red_coin",
            "Single ship Red Coin reached without raising the ship",
            2,
            has_upper and has_red_coins and not has_raised_ship
            and has_ship_red_coin_alternative,
            red_coin_ids=frozenset({6}),
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
        coin_source("red_coins", "Eight Red Coins", 16, has_red_coins,
                    red_coin_ids=frozenset(range(1, 9))),
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
    traces.append(coin_source(
        "wall_kicks_route",
        "Wall Kicks Will Work coin sources",
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
        coin_source("first_floor_red_coins", "Four first-floor Red Coins", 8, has_red_coins,
                    red_coin_ids=frozenset(range(1, 5))),
    ]

    has_second_floor = state.can_reach(f"{level_name} - Second Floor", "Region", player)
    second_floor_children = (
        coin_source("second_floor_bookends", "Two Flying Bookends on the second floor", 10,
                has_second_floor and has_flying_bookends),
        coin_source("second_floor_mr_i", "Mr. I on the second floor", 5,
                has_second_floor and has_mr_is),
        coin_source("second_floor_red_coins", "Three readily reachable second-floor Red Coins", 6,
                has_second_floor and has_red_coins, red_coin_ids=frozenset({5, 6, 7})),
        coin_source(
            "second_floor_movement_red_coin",
            "Second-floor Red Coin requiring Triple Jump, Wall Kick, Backflip, or Side Flip",
            2,
            has_second_floor and has_red_coins and any(
                Rules.has_action(state, player, action, level_name)
                for action in ("Triple Jump", "Wall Kick", "Backflip", "Side Flip")
            ),
            red_coin_ids=frozenset({8}),
        ),
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
    traces.append(coin_source(
        "third_floor_sources",
        "Big Boo's Haunt Third Floor sources",
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
                has_basic_movement and has_red_coins, red_coin_ids=frozenset(range(1, 5))),
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
        red_coin_ids=frozenset({5, 6}),
    ))
    traces.append(coin_source(
        "upper_red_coin_pair_checkerboards",
        "Second pair of upper Red Coins",
        4,
        has_red_coins and has_platform_route and has_checkerboards,
        red_coin_ids=frozenset({7, 8}),
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
    return _coin_trace(source_id, label, 0, available, counted=counted)


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
        red_coin_ids=frozenset(range(1, 6)),
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
        red_coin_ids=frozenset({6, 7, 8}),
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
        "Fly Guys", f"{level_name} - Fly Guys")
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
        "Line of coins between the two pillars behind the pyramid",
        5,
        has_horizontal_coin_lines,
    )
    builder.add(
        "ssl_pyramid_side_coin_line",
        "Line of coins on the pyramid",
        5,
        has_horizontal_coin_lines,
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
        red_coin_ids=frozenset(range(1, 5)),
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
    tweester_route_available = has_red_coins and has_tweester_trick
    shy_guy_route_available = has_red_coins and has_shy_guy_trick
    normal_route_available = has_red_coins and has_normal_red_coin_route
    use_tweester_route = tweester_route_available and not normal_route_available
    use_shy_guy_coins = shy_guy_route_available and not normal_route_available
    reachable_high_red_coin_value = (
        8 if normal_route_available
        else (6 if use_tweester_route else 0) + (2 if use_shy_guy_coins else 0)
    )
    builder.add(
        "ssl_high_red_coins",
        "Four high Red Coins",
        reachable_high_red_coin_value,
        normal_route_available or tweester_route_available or shy_guy_route_available,
        max_coins=8,
        children=(
            _coin_trace(
                "ssl_normal_high_red_coin_route",
                "Wing Cap with Triple Jump or Cannon",
                8,
                normal_route_available,
                counted=normal_route_available,
                red_coin_ids=frozenset({5, 6, 7, 8}),
            ),
            _coin_trace(
                "ssl_tweester_red_coin_route",
                "Three Red Coins with the Tweester trick",
                6,
                tweester_route_available,
                counted=use_tweester_route,
                red_coin_ids=frozenset({5, 6, 7}),
            ),
            _coin_trace(
                "ssl_shy_guy_red_coin_route",
                "One Red Coin with the Shy Guy spin-jump trick",
                2,
                shy_guy_route_available,
                counted=use_shy_guy_coins,
                red_coin_ids=frozenset({8}),
                reachable_red_coin_ids_when_uncounted=frozenset({8}),
            ),
        ),
    )

    can_reach_upper_pyramid = state.can_reach(
        "Shifting Sand Land - Upper Pyramid", "Region", player)
    upper_pyramid_access = coin_condition(
        "ssl_upper_pyramid_access_for_lines",
        "Upper Pyramid is reachable",
        can_reach_upper_pyramid,
    )
    builder.add(
        "ssl_second_wire_grid_coin_line",
        "Line of coins under the second wire grid",
        5,
        can_reach_upper_pyramid and has_horizontal_coin_lines,
        children=(upper_pyramid_access,),
    )
    builder.add(
        "ssl_pyramid_top_horizontal_coin_line",
        "Horizontal coin line at the top of the pyramid",
        5,
        can_reach_upper_pyramid and has_horizontal_coin_lines,
        children=(upper_pyramid_access,),
    )
    builder.add(
        "ssl_pyramid_top_vertical_coin_line",
        "Vertical coin line at the top of the pyramid",
        5,
        can_reach_upper_pyramid and has_vertical_coin_line,
        children=(upper_pyramid_access,),
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
        red_coin_ids=frozenset({1}),
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
        red_coin_ids=frozenset(range(2, 9)),
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
        "Eight Spindrifts outside the Upper area",
        24,
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
        red_coin_ids=frozenset({1, 2, 3}),
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
        "sl_upper_red_coins",
        "Five Red Coins in the Upper area",
        10,
        can_reach_upper and has_red_coins,
        red_coin_ids=frozenset({4, 5, 6, 7, 8}),
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
        (
            "sl_igloo_goombas",
            "Three Goombas inside the Igloo",
            3,
            has_goombas,
        ),
        (
            "sl_igloo_spindrifts",
            "Three Spindrifts inside the Igloo",
            9,
            has_spindrifts,
        ),
    )
    igloo_children = [
        _coin_trace(source_id, label, coins, available)
        for source_id, label, coins, available in igloo_source_data
    ]
    igloo_coins = sum(
        coins for _source_id, _label, coins, available in igloo_source_data if available)
    builder.add(
        "sl_igloo_route",
        "Igloo coin sources",
        igloo_coins,
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
        3,
        has_goombas,
    )

    can_reach_middle = state.can_reach(f"{level_name} - Middle", "Region", player)
    builder.add(
        "ttm_middle_red_coins",
        "Six Red Coins in the Middle area",
        12,
        can_reach_middle and has_red_coins,
        red_coin_ids=frozenset(range(1, 7)),
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
        red_coin_ids=frozenset({7, 8}),
    )
    builder.add(
        "ttm_upper_goombas",
        "Three Goombas in the Upper area",
        3,
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
        "ttm_top_goombas",
        "Three Goombas in the Top area",
        3,
        can_reach_top and has_goombas,
    )
    builder.add(
        "ttm_hidden_coin_before_slide",
        "Hidden single yellow coin before the slide",
        1,
        can_reach_top and has_single_yellow_coins,
    )
    builder.add(
        "ttm_slide_single_coins",
        "Single yellow coins on the slide",
        26,
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
    red_coin_ids: frozenset[int] = frozenset()


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
        red_coin_ids: frozenset[int] = frozenset(),
) -> _route_trace_node_type:
    return _route_trace_node_type(
        source_id,
        label,
        coins,
        available,
        available if selected is None else selected,
        red_coin_ids=red_coin_ids,
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
        return _coin_trace(
            node.source_id, node.label, coins, available,
            counted=counted, children=children)

    owned = source_owners is None or source_owners.get(node.source_id) == route_id
    counted = route_counted and node.selected and available and owned
    return _coin_trace(
        node.source_id, node.label, node.coins, available,
        counted=counted, red_coin_ids=node.red_coin_ids)


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
    return _coin_trace(
        route.source_id, route.label, coins, route.available,
        counted=counted, children=children)


def _evaluate_route_set(
        routes: list[_route_type],
        *,
        maximum: int | None = None,
) -> CoinEvaluation:
    merged: dict[str, CoinSourceTrace] = {}

    def merge_node(node: _route_trace_node_type, parent_available: bool) -> None:
        available = parent_available and node.available
        if node.children:
            # Some producers, notably Giant Goombas, keep their coin value on
            # the parent while zero-value children explain alternate physical
            # outcomes. Preserve that value instead of treating the producer
            # as a route-only container.
            if node.coins and not any(child.coins for child in node.children):
                previous = merged.get(node.source_id)
                merged[node.source_id] = _coin_trace(
                    node.source_id,
                    node.label,
                    node.coins,
                    available or bool(previous and previous.available),
                    red_coin_ids=node.red_coin_ids | (previous.red_coin_ids if previous else frozenset()),
                )
            for child in node.children:
                merge_node(child, available)
            return

        previous = merged.get(node.source_id)
        merged[node.source_id] = _coin_trace(
            node.source_id,
            node.label,
            node.coins,
            available or bool(previous and previous.available),
            red_coin_ids=node.red_coin_ids | (previous.red_coin_ids if previous else frozenset()),
        )

    for route in routes:
        for child in route.children:
            merge_node(child, route.available)

    traces = tuple(merged.values())
    reachable_coins = sum(trace.coins for trace in traces if trace.counted)

    if maximum is not None:
        reachable_coins = min(reachable_coins, maximum)
    return CoinEvaluation(reachable_coins, traces)


def wet_dry_world_coin_evaluation(
        state: CollectionState,
        player: int,
        required_coins: int,
) -> CoinEvaluation:
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
    has_heave_hos = rules.has_unlock(
        state, player, "enemy_unlocks",
        "Heave-Hos", f"{level_name} - Heave-Hos")
    has_ground_pound = rules.has_action(state, player, "Ground Pound", level_name)
    has_water_level_diamond = rules.has_simple_arbitrary_feature(
        state, player, "WDW_WATER_LEVEL_DIAMOND")
    has_long_jump = rules.has_action(state, player, "Long Jump", level_name)
    has_triple_jump = rules.has_action(state, player, "Triple Jump", level_name)
    has_backflip = rules.has_action(state, player, "Backflip", level_name)
    has_side_flip = rules.has_action(state, player, "Side Flip", level_name)
    has_wall_kick = rules.has_action(state, player, "Wall Kick", level_name)
    has_ledge_grab = rules.has_action(state, player, "Ledge Grab", level_name)
    can_reach_high_red_coins = has_wall_kick or rules.can_use_logic_trick(
        state, player, "logic_wdw_high_red_coins_triple_jump", level_name)
    can_reach_main = state.can_reach(level_name, "Region", player)
    can_reach_low = state.can_reach(f"{level_name} - Low Water", "Region", player)
    can_reach_mid = state.can_reach(f"{level_name} - Mid Water", "Region", player)
    can_reach_high = state.can_reach(f"{level_name} - High Water", "Region", player)
    can_reach_highest = state.can_reach(f"{level_name} - Highest Water", "Region", player)
    can_reach_near_top = state.can_reach(f"{level_name} - Near the Top", "Region", player)
    can_reach_top = state.can_reach(f"{level_name} - Top", "Region", player)
    can_reach_top_of_express = state.can_reach(
        f"{level_name} - Top of the Express Elevator", "Region", player)
    can_reach_downtown = state.can_reach(f"{level_name} - Downtown", "Region", player)
    near_top_block_route = (
        can_reach_low
        or can_reach_mid and (has_heave_hos or has_side_flip or has_backflip or has_triple_jump)
        or can_reach_high and has_ledge_grab
        or can_reach_highest
        or can_reach_top
    )
    wooden_structure_route = (
        can_reach_mid or can_reach_top or can_reach_top_of_express and has_long_jump)
    fourth_diamond_route = (
        can_reach_mid or can_reach_highest or can_reach_top
        or can_reach_top_of_express and has_long_jump)

    traces = [
        coin_source("main_skeeters", "Two Skeeters in the main area", 6,
                    can_reach_main and has_skeeters),
        coin_source("amp_ring", "Coin ring around the Amp pillar", 8,
                    can_reach_near_top and has_horizontal_coin_rings),
        coin_source("pillar_ten_coin_block", "10-Coin Block on the pillar", 10,
                    can_reach_near_top and near_top_block_route and has_ten_coin_blocks),
        coin_source("push_block_three_coin_block", "3-Coin Block below the Chuckya platform", 3,
                    can_reach_near_top and has_three_coin_blocks),
        coin_source("low_breakable_boxes", "Breakable coin boxes at low water", 12,
                    can_reach_low and has_breakable_coin_boxes),
        coin_source("low_ten_coin_block", "10-Coin Block below the cannon", 10,
                    can_reach_low and has_ten_coin_blocks),
        coin_source("low_blue_coins", "Blue coins at low water", 30,
                    can_reach_low and has_ground_pound and has_blue_coin_block),
        coin_source("wooden_structure_three_coin_block", "3-Coin Block on the wooden structure", 3,
                    wooden_structure_route and has_three_coin_blocks),
        coin_source("fourth_diamond_coin_line", "Coin line by the fourth water-level diamond", 5,
                    fourth_diamond_route and has_horizontal_coin_lines),
        coin_source("top_coin_line", "Coin line at the highest water-level diamond", 5,
                    can_reach_top and has_horizontal_coin_lines),
        coin_source("top_chuckya", "Chuckya at the top", 5,
                    can_reach_top and has_chuckya),
        coin_source("express_elevator_ten_coin_block", "10-Coin Block above the Express Elevator", 10,
                    can_reach_top_of_express and has_ten_coin_blocks),
        coin_source("downtown_ring", "Downtown statue coin ring", 8,
                    can_reach_downtown and has_horizontal_coin_rings),
        coin_source("downtown_metal_cap_line", "Downtown metal-cap coin line", 5,
                    can_reach_downtown and has_horizontal_coin_lines),
        coin_source("downtown_first_building_line", "Downtown first-building coin line", 5,
                    can_reach_downtown and has_horizontal_coin_lines),
        coin_source("downtown_second_building_line", "Downtown second-building coin line", 5,
                    can_reach_downtown and has_horizontal_coin_lines),
        coin_source("downtown_skeeters", "Two Skeeters Downtown", 6,
                    can_reach_downtown and has_skeeters),
        coin_source("downtown_initial_red_coin", "First Downtown red coin", 2,
                    can_reach_downtown and has_red_coins,
                    red_coin_ids=frozenset({1})),
        coin_source("downtown_diamond_red_coins", "Five Downtown red coins beyond water-level diamonds", 10,
                    can_reach_downtown and has_water_level_diamond and has_red_coins,
                    red_coin_ids=frozenset({2, 3, 4, 5, 6})),
        coin_source("downtown_high_red_coins", "Two high Downtown red coins", 4,
                    can_reach_downtown and has_water_level_diamond
                    and has_red_coins and can_reach_high_red_coins,
                    red_coin_ids=frozenset({7, 8})),
    ]
    return coin_evaluation(traces, 152)


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
        "Fly Guys", f"{level_name} - Fly Guys")
    has_goombas = rules.has_unlock(
        state, player, "enemy_unlocks",
        "Goombas", f"{level_name} - Goombas")
    has_koopa_troopa = rules.has_unlock(
        state, player, "enemy_unlocks",
        "Koopa Troopas", f"{level_name} - Koopa Troopas")
    has_warp_pipes = rules.has_warp_pipes(state, player, "Tiny-Huge Island")
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
    def giant_goomba_coins(count: int, blue_coin_available: bool | None = None) -> int:
        if blue_coin_available is None:
            blue_coin_available = has_ground_pound
        return count * (5 if blue_coin_available else 1)

    def make_route(start_tiny: bool, route_available: bool) -> _route_type:
        sources: dict[str, int] = {}
        children: list[_route_trace_node_type] = []

        def add_source(
                source_id: str,
                label: str,
                value: int,
                available: bool,
                red_coin_ids: frozenset[int] = frozenset(),
                giant_blue_available: bool | None = None,
        ) -> None:
            source = _route_source(source_id, label, value, available, red_coin_ids=red_coin_ids)
            if source_id in {
                    "huge_start_giant_goombas", "near_cannon_giant_goomba",
                    "huge_windswept_giant_goombas",
                    "huge_koopa_region_giant_goombas", "red_area_giant_goombas"}:
                if giant_blue_available is None:
                    giant_blue_available = has_ground_pound
                source.children.extend((
                    _route_source(f"{source_id}_yellow", f"{label} yellow outputs", 0, available),
                    _route_source(
                        f"{source_id}_blue", f"{label} blue outputs",
                        0, available and giant_blue_available),
                ))
            children.append(source)
            if available and value:
                sources[source_id] = value

        has_initial_tiny_piranha = start_tiny and has_tiny_piranha_movement
        has_tiny_main_from_tiny = has_initial_tiny_piranha and has_thi_purple_switches
        has_huge_piranha_from_pipe = has_initial_tiny_piranha and has_warp_pipes
        has_huge_start = not start_tiny or has_huge_piranha_from_pipe
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
        has_tiny_piranha = has_initial_tiny_piranha or has_koopa_region and has_warp_pipes
        has_tiny_start = start_tiny or has_tiny_piranha
        has_tiny_main = has_tiny_main_from_tiny or has_koopa_region and has_warp_pipes

        add_source(
            "tiny_start_goomba",
            "Small Goomba in the starting Tiny region",
            1,
            start_tiny and has_tiny_start and has_goombas,
        )
        add_source(
            "tiny_piranha_area_plant",
            "Piranha Plant in the Tiny Piranha Area",
            1,
            start_tiny and has_tiny_piranha and has_fire_piranha_plants,
        )
        add_source(
            "tiny_main_individual_coins",
            "Tiny Island coins",
            9,
            has_tiny_main and has_single_yellow_coins,
        )
        add_source(
            "tiny_main_coin_line",
            "Coin line on the Tiny Island wooden plank",
            5,
            has_tiny_main and has_horizontal_coin_lines,
        )
        add_source(
            "tiny_main_three_coin_block",
            "3-Coin Block on Tiny Island",
            3,
            has_tiny_main and has_three_coin_block,
        )
        add_source(
            "tiny_main_goombas",
            "Nine Tiny Island Goombas",
            9,
            has_tiny_main and has_goombas,
        )
        add_source(
            "tiny_main_koopa",
            "Tiny Island Koopa Troopa",
            5,
            has_tiny_main and has_koopa_troopa,
        )
        add_source(
            "tiny_purple_switch_coin",
            "Five Itty Bitty Secrets Island coin",
            1,
            has_tiny_main
            and has_thi_purple_switches
            and has_single_yellow_coins,
        )

        has_huge_context = has_huge_start or has_koopa_region
        add_source(
            "huge_start_giant_goombas",
            "Three Huge Starting Area Goombas",
            giant_goomba_coins(3),
            has_huge_context and has_goombas,
        )
        near_cannon_blue_available = has_ground_pound or has_fly_guy
        add_source(
            "near_cannon_giant_goomba",
            "Near Cannon Goomba",
            giant_goomba_coins(1, near_cannon_blue_available),
            has_huge_context and has_goombas,
            giant_blue_available=near_cannon_blue_available,
        )
        add_source(
            "huge_start_post",
            "Wooden post at Huge Island start",
            5,
            has_huge_context and has_wooden_posts,
        )
        add_source(
            "huge_beach_coins",
            "Huge Island beach coins",
            2,
            has_huge_context and has_single_yellow_coins,
        )
        add_source(
            "huge_beach_fly_guy",
            "Beach Fly Guy",
            2,
            has_huge_context and has_fly_guy,
        )
        add_source(
            "huge_near_cannon_fly_guy",
            "Near Cannon Fly Guy",
            2,
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
            and (has_cannon and has_huge_start or has_koopa_region and has_long_jump),
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
            "Coin line in Koopa the Quick's area",
            4,
            has_huge_context and has_koopa_region and has_horizontal_coin_lines,
        )
        add_source(
            "tiny_impossible_coin",
            "Impossible Coin",
            1,
            has_huge_context and has_koopa_region and has_horizontal_coin_lines and has_impossible_coin,
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
            "huge_top_chuckya",
            "Chuckya",
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
                red_coin_ids=frozenset(range(1, 8)),
            ),
            _route_source(
                "red_area_wall_kick_red_coin",
                "Wall-kick red coin in the Red Coins Area",
                2,
                has_red_coins and rules.has_action(
                    state, player, "Wall Kick", level_name),
                red_coin_ids=frozenset({8}),
            ),
            _route_source(
                "red_area_blue_coins",
                "Blue coins in the Red Coins Area",
                10,
                has_ground_pound and has_blue_coin_block,
            ),
            _route_source(
                "red_area_plank_line",
                "Coin line on the Red Coins Area plank",
                5,
                has_horizontal_coin_lines,
            ),
        ]
        red_area_children[0].children.extend((
            _route_source(
                "red_area_giant_goombas_yellow", "Two Giant Goombas yellow outputs",
                0, has_goombas),
            _route_source(
                "red_area_giant_goombas_blue", "Two Giant Goombas blue outputs",
                0, has_goombas and has_ground_pound),
        ))
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
            _route_source(
                "tiny_piranha_area_plant",
                "Piranha Plant beyond the Warp Pipe in the Tiny Piranha Area",
                1,
                not start_tiny and has_warp_pipes and has_fire_piranha_plants,
            ),
            _route_source(
                "tiny_start_goomba",
                "Small Goomba in the starting Tiny region",
                1,
                not start_tiny and has_warp_pipes and has_goombas,
            ),
        ]

        red_area_direct = has_huge_context and has_cannon and has_huge_start
        red_area_terminal = has_huge_context and not red_area_direct and has_top
        wiggler_available = (
            has_huge_context and has_tiny_main and has_warp_pipes and has_ground_pound)
        piranha_direct = has_huge_piranha_from_pipe or (
            has_koopa_region and has_warp_pipes and has_thi_purple_switches)
        piranha_terminal = not has_huge_piranha_from_pipe and has_koopa_region and not piranha_direct

        def append_group(
                source_id: str,
                label: str,
                available: bool,
                group_children: list[_route_trace_node_type],
        ) -> None:
            group = _route_trace_node_type(
                source_id,
                label,
                sum(child.coins for child in group_children if child.available),
                available,
                available,
                group_children,
            )
            children.append(group)
            if available:
                for child in group_children:
                    if child.available and child.coins:
                        sources[child.source_id] = child.coins

        append_group(
            "thi_red_coins_area",
            "Red Coins Area",
            red_area_direct or red_area_terminal,
            red_area_children,
        )
        append_group(
            "thi_wiggler_cave",
            "Wiggler's Cave",
            wiggler_available,
            wiggler_children,
        )
        append_group(
            "thi_huge_piranha_area",
            "Huge Piranha Area",
            piranha_direct or piranha_terminal,
            piranha_children,
        )

        route_name = "Tiny entrance route" if start_tiny else "Huge entrance route"
        route_id = "thi_tiny_variant" if start_tiny else "thi_huge_variant"
        return _route_type(route_id, route_name, route_available, sources, children)

    routes = [
        make_route(True, can_enter_tiny),
        make_route(False, can_enter_huge),
    ]
    return _evaluate_route_set(routes)


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
        coin_source("ttc_lower_red_coins", "Five lower Red Coins", 10, has_red_coins,
                    red_coin_ids=frozenset(range(1, 6))),
        coin_source(
            "ttc_spinner_red_coins",
            "Three Red Coins reached with the Spinners",
            6,
            has_red_coins
            and rules.has_simple_arbitrary_feature(state, player, "TTC_SPINNERS"),
            red_coin_ids=frozenset({6, 7, 8}),
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
        coin_source("rr_maze_lakitu", "Lakitu in the Maze", 5, has_lakitus),
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
            red_coin_ids=frozenset({1}),
        ),
        coin_source(
            "rr_other_red_coins",
            "Seven remaining Red Coins",
            14,
            has_red_coins and (
                has_wall_kick
                or (
                    rules.has_action(state, player, "Long Jump", level_name)
                    and any(rules.has_action(state, player, action, level_name)
                            for action in ("Side Flip", "Backflip", "Triple Jump"))
                )
                or has_maze_red_coin_trick
            ),
            red_coin_ids=frozenset(range(2, 9)),
        ),
    ))
    trace.add_route(
        "rr_carpets", "Carpets region",
        state.can_reach("Rainbow Ride - Carpets", "Region", player), (
            coin_source("rr_carpets_lakitu", "Lakitu in the Carpets region", 5, has_lakitus),
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
            red_coin_ids=frozenset(range(1, 9)),
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
    has_leap_of_faith = rules.can_use_logic_trick(
        state, player, "logic_wmotr_leap_of_faith", level_name)
    has_leap_without_ledge_grab = rules.can_use_logic_trick(
        state, player, "logic_wmotr_leap_of_faith_without_ledge_grab", level_name)
    leap_of_faith_selected = rules.has_logic_trick(
        state, player, "logic_wmotr_leap_of_faith")
    leap_without_ledge_grab_selected = rules.has_logic_trick(
        state, player, "logic_wmotr_leap_of_faith_without_ledge_grab")
    can_long_jump_leap = has_leap_of_faith or has_leap_without_ledge_grab
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
        coin_source("wmotr_initial_red_coin", "Initial Red Coin", 2, has_red_coins,
                    red_coin_ids=frozenset({1})),
    ))
    trace.add_route("wmotr_cannon_only", "Cannon region", has_cannon_region, (
        coin_source("wmotr_cannon_red_coins",
                "Four Red Coins requiring the Cannon region",
                8, has_red_coins, red_coin_ids=frozenset({2, 3, 4, 5})),
    ))

    trace.add_route("wmotr_flight_route", "Flight route", has_flight_route, (
        coin_source("wmotr_flight_red_coins", "Three flight-path Red Coins",
                6, has_red_coins, red_coin_ids=frozenset({6, 7, 8})),
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
            or has_leap_of_faith
            and rules.has_action(state, player, "Ledge Grab", level_name)
        )
    )
    wing_cap_fallback_coin = (
        not long_jump_first_coin
        and has_red_coins
        and has_wing_cap_item
        and (leap_of_faith_selected or leap_without_ledge_grab_selected)
    )
    trace.add_route(
        "wmotr_leap_fallback",
        "Leap of Faith fallback (used only when the flight route is unavailable)",
        True,
        (
            coin_source("wmotr_long_jump_first_red_coin",
                    "First Long Jump Leap of Faith Red Coin",
                    2, long_jump_first_coin, red_coin_ids=frozenset({6})),
            coin_source("wmotr_long_jump_second_red_coin",
                    "Second Long Jump Leap of Faith Red Coin",
                    2, long_jump_second_coin, red_coin_ids=frozenset({7})),
            coin_source("wmotr_wing_cap_fallback_red_coin",
                    "Wing Cap slow-fall Leap of Faith Red Coin",
                    2, wing_cap_fallback_coin, red_coin_ids=frozenset({6})),
        ),
        selected=fallback_selected,
    )

    assert trace.reachable_coins <= 56
    return trace.evaluation()


def tower_of_the_wing_cap_coins(
        state: CollectionState, player: int, coins: int) -> CoinEvaluation:
    rules = _rules()
    level_name = "Tower of the Wing Cap"
    # Permanent collection allows the ring coins to be accumulated over
    # repeated attempts, so the former single-visit mastery cap does not apply.
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
        coin_source("totwc_red_coins", "Eight Red Coins", 16, has_red_coins,
                    red_coin_ids=frozenset(range(1, 9))),
    ))
    trace.add_route(
        "totwc_mastery_ring_route",
        "Coin ring sources across repeated attempts",
        True,
        (
            coin_source("totwc_mastery_ring_coins",
                    "Coin Ring coins reachable across repeated attempts",
                    20, has_vertical_coin_rings),
            coin_source("totwc_mastery_wing_cap_ring_coins",
                    "Additional Coin Ring coins with Wing Cap",
                    12, has_vertical_coin_rings and has_wing_cap_item),
        ),
        selected=True,
    )

    uncapped_coins = trace.reachable_coins
    assert uncapped_coins <= 63
    option_cap = state.multiworld.worlds[
        player].options.tower_of_the_wing_cap_coin_count_max_coins.value
    reachable_coins = min(uncapped_coins, option_cap)
    if reachable_coins < uncapped_coins:
        trace.add_source(
            "totwc_coin_cap",
            f"Coins excluded by the {option_cap}-coin option cap",
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
                8, has_red_coins, red_coin_ids=frozenset(range(1, 5))),
    )
    later_route = (
        has_movement or can_drop_to_checkerboards or can_crawl_back_then_drop)
    later_sources = (
        coin_source("vcutm_turning_lifts_block",
                "3-Coin Block before the turning lifts",
                3, has_three_coin_block),
        coin_source("vcutm_checkerboard_red_coins",
                "Four Red Coins at the checkerboards",
                8, has_checkerboards and has_red_coins,
                red_coin_ids=frozenset({5, 6, 7, 8})),
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
                8, has_red_coins, red_coin_ids=frozenset(range(1, 5))),
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
                    8, has_red_coins, red_coin_ids=frozenset({5, 6, 7, 8})),
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
                "Six Red Coins before the slope", 12, has_red_coins,
                red_coin_ids=frozenset(range(1, 7))),
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
                 "Final two Red Coins", 4, has_red_coins,
                 red_coin_ids=frozenset({7, 8})),),
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
                4, has_red_coins, red_coin_ids=frozenset({1, 2})),
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
                12, has_red_coins, red_coin_ids=frozenset(range(3, 9))),
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
                6, has_red_coins, red_coin_ids=frozenset({1, 2, 3})),
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
                    6, has_red_coins, red_coin_ids=frozenset({4, 5, 6})),
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
                    4, has_red_coins, red_coin_ids=frozenset({7, 8})),
            coin_source("bits_final_rotating_platform_line",
                    "Coin line before the final rotating platforms",
                    5, has_horizontal_coin_lines),
        ))
    assert trace.reachable_coins <= 76
    return trace.evaluation()


def _with_coin_rule_context(
        course_name: str,
        evaluator: CoinTraceEvaluator,
) -> CoinTraceEvaluator:
    def evaluate(
            state: CollectionState,
            player: int,
            required_coins: int,
    ) -> CoinEvaluation:
        token = _coin_rule_context.set((state, player, course_name))
        try:
            return evaluator(state, player, required_coins)
        finally:
            _coin_rule_context.reset(token)

    return evaluate


def castle_coins(
        state: CollectionState,
        player: int,
        _required_coins: int,
) -> CoinEvaluation:
    from . import Rules

    level_name = "Castle"
    has_single_yellow_coins = Rules.has_unlock(
        state, player, "coin_object_unlocks",
        "Single Yellow Coins", "Castle - Single Yellow Coins")
    can_reach_bridge_coins = (
        state.can_reach("Castle - Drain the Moat", "Location", player)
        and Rules.has_action(state, player, "Wall Kick", level_name)
        and any(Rules.has_action(state, player, action, level_name)
                for action in ("Triple Jump", "Side Flip"))
    )
    has_castle_boos = Rules.has_unlock(
        state, player, "enemy_unlocks", "Boos", "Castle - Boos")

    trace = CoinTraceBuilder()
    trace.add_source(
        "castle_grounds_bridge_coins", "Two coins under the Castle Grounds bridge", 2,
        has_single_yellow_coins and can_reach_bridge_coins)
    trace.add_source(
        "castle_lobby_coins", "Four coins in the Castle Lobby", 4,
        has_single_yellow_coins)
    trace.add_source(
        "castle_courtyard_boos", "Nine Boos in the Castle Courtyard", 45,
        has_castle_boos)
    assert trace.reachable_coins <= 51
    return trace.evaluation()


_RAW_COIN_EVALUATORS: dict[str, CoinTraceEvaluator] = {
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
    "Castle": castle_coins,
}

COIN_EVALUATORS: dict[str, CoinTraceEvaluator] = {
    course_name: _with_coin_rule_context(course_name, evaluator)
    for course_name, evaluator in _RAW_COIN_EVALUATORS.items()
}


CoinSourceRuleSpec = dict[str, Any]


_TOKEN_ALIASES = {
    "BOB_OMBS": "BOBOMBS",
    "THI_PURPLE_SWITCHES": "PURPLE_SWITCHES",
    "THI_WARP_PIPES": "WARP_PIPES",
    "TTM_PURPLE_SWITCHES": "PURPLE_SWITCHES",
    "WDW_PURPLE_SWITCHES": "PURPLE_SWITCHES",
}

_EXPLANATION_ONLY_UNLOCKS = {
    "BLUE_COIN_BLOCKS": ("Blue Coin Blocks", "Blue Coin Block"),
    "BREAKABLE_COIN_BOXES": ("Breakable Coin Boxes", "Breakable Coin Box"),
    "CHUCKYA": ("Chuckyas", "Chuckya"),
    "CRAZY_BOXES": ("Crazy Boxes", "Crazy Box"),
    "GOOMBAS": ("Goombas", "Goombas"),
    "LAKITU": ("Lakitus", "Lakitu"),
    "SINGLE_BLUE_COINS": ("Single Blue Coins", "Single Blue Coins"),
    "SKEETERS": ("Skeeters", "Skeeters"),
}


def _early_requirement_specs():
    """Rule Builder requirement specifications for the first five course coin evaluators.

    This is intentionally data-only scaffolding.  ``rule`` contains the non-object
    requirements from CoinLogic, while ``unlocks`` contains the object/enemy unlock
    families that must be resolved with HasUnlock.
    """



    UnlockPair = tuple[str, str]
    RequirementSpec = dict[str, str | tuple[UnlockPair, ...]]


    def _spec(target: str, rule: str = "", *unlocks: UnlockPair) -> RequirementSpec:
        return {"rule": rule, "target": target, "unlocks": unlocks}


    BOB = "Bob-omb Battlefield"
    BOB_TARGET = f"{BOB} - Coins Star"
    WF = "Whomp's Fortress"
    WF_TARGET = f"{WF} - Coins Star"
    JRB = "Jolly Roger Bay"
    JRB_TARGET = f"{JRB} - Coins Star"
    CCM = "Cool, Cool Mountain"
    CCM_TARGET = f"{CCM} - Coins Star"
    BBH = "Big Boo's Haunt"
    BBH_TARGET = f"{BBH} - Coins Star"


    COIN_REQUIREMENT_SPECS: dict[tuple[str, str], RequirementSpec] = {
        # Bob-omb Battlefield
        (BOB, "start_breakable_coin_box"): _spec(
            BOB_TARGET, "", ("Breakable Coin Boxes", f"{BOB} - Breakable Coin Box")),
        (BOB, "start_throwable_cork_boxes"): _spec(
            BOB_TARGET, "", ("Throwable Cork Boxes", f"{BOB} - Throwable Cork Boxes")),
        (BOB, "main_horizontal_coin_lines"): _spec(
            BOB_TARGET, "", ("Horizontal Coin Lines", f"{BOB} - Horizontal Coin Lines")),
        (BOB, "main_wooden_posts"): _spec(
            BOB_TARGET, "", ("Wooden Posts", f"{BOB} - Wooden Posts")),
        (BOB, "flowerbed_coin_ring"): _spec(
            BOB_TARGET, "", ("Horizontal Coin Rings", f"{BOB} - Horizontal Coin Rings")),
        (BOB, "main_bob_ombs"): _spec(
            BOB_TARGET, "", ("Bob-ombs", f"{BOB} - Bob-ombs")),
        (BOB, "main_goombas"): _spec(BOB_TARGET, "", ("Goombas", f"{BOB} - Goombas")),
        (BOB, "main_red_coins"): _spec(BOB_TARGET, "", ("Red Coins", f"{BOB} - Red Coins")),
        (BOB, "main_koopa_troopa"): _spec(
            BOB_TARGET, "", ("Koopa Troopas", f"{BOB} - Koopa Troopa")),
        (BOB, "island_first_ring_easy_coins"): _spec(
            BOB_TARGET, f"{{{BOB} - Island}}",
            ("Vertical Coin Rings", f"{BOB} - Vertical Coin Rings")),

        (BOB, "island_without_cannon_route"): _spec(
            BOB_TARGET, f"{{{BOB} - Island}} & logic_bob_mario_wings_to_the_sky_without_cannon"),
        (BOB, "island_full_trick_vertical_ring_coins"): _spec(
            BOB_TARGET, f"{{{BOB} - Island}} & logic_bob_mario_wings_to_the_sky_without_cannon",
            ("Vertical Coin Rings", f"{BOB} - Vertical Coin Rings")),
        (BOB, "island_full_trick_ring_center_coins"): _spec(
            BOB_TARGET, f"{{{BOB} - Island}} & logic_bob_mario_wings_to_the_sky_without_cannon",
            ("Single Yellow Coins", f"{BOB} - Single Yellow Coins")),
        (BOB, "island_full_trick_red_coin"): _spec(
            BOB_TARGET, f"{{{BOB} - Island}} & logic_bob_mario_wings_to_the_sky_without_cannon",
            ("Red Coins", f"{BOB} - Red Coins")),

        (BOB, "island_cannon_route"): _spec(
            BOB_TARGET, f"{{{BOB} - Island}} & CANN & {{{{{BOB} - Mario Wings to the Sky}}}}"),
        (BOB, "island_cannon_vertical_ring_coins"): _spec(
            BOB_TARGET, f"{{{BOB} - Island}} & CANN & {{{{{BOB} - Mario Wings to the Sky}}}}",
            ("Vertical Coin Rings", f"{BOB} - Vertical Coin Rings")),
        (BOB, "island_cannon_ring_center_coins"): _spec(
            BOB_TARGET, f"{{{BOB} - Island}} & CANN & {{{{{BOB} - Mario Wings to the Sky}}}}",
            ("Single Yellow Coins", f"{BOB} - Single Yellow Coins")),
        (BOB, "island_cannon_red_coin"): _spec(
            BOB_TARGET, f"{{{BOB} - Island}} & CANN & {{{{{BOB} - Mario Wings to the Sky}}}}",
            ("Red Coins", f"{BOB} - Red Coins")),

        # Partial methods expose only the outputs that their individual rules reach.
        (BOB, "island_partial_route"): _spec(BOB_TARGET, f"{{{BOB} - Island}}"),
        (BOB, "island_partial_flight_ring_coins"): _spec(
            BOB_TARGET, f"{{{BOB} - Island}} & WC & TJ",
            ("Vertical Coin Rings", f"{BOB} - Vertical Coin Rings")),
        (BOB, "island_partial_flight_center_coins"): _spec(
            BOB_TARGET, f"{{{BOB} - Island}} & WC & TJ",
            ("Single Yellow Coins", f"{BOB} - Single Yellow Coins")),
        (BOB, "island_partial_red_coin"): _spec(
            BOB_TARGET,
            f"{{{BOB} - Island}} & CL/SF/BF/TJ | "
            f"{{{BOB} - Island}} & logic_bob_island_red_coin_with_ground_pound | "
            f"{{{BOB} - Island}} & logic_bob_island_koopa_shell",
            ("Red Coins", f"{BOB} - Red Coins")),
        (BOB, "island_partial_first_ring_three_coins"): _spec(
            BOB_TARGET,
            f"{{{BOB} - Island}} & SF/BF/TJ | "
            f"{{{BOB} - Island}} & logic_bob_island_red_coin_with_ground_pound",
            ("Vertical Coin Rings", f"{BOB} - Vertical Coin Rings")),
        (BOB, "island_partial_first_ring_two_coins"): _spec(
            BOB_TARGET, f"{{{BOB} - Island}} & SF/BF/TJ",
            ("Vertical Coin Rings", f"{BOB} - Vertical Coin Rings")),
        (BOB, "island_partial_triple_jump_coin"): _spec(
            BOB_TARGET, f"{{{BOB} - Island}} & TJ",
            ("Single Yellow Coins", f"{BOB} - Single Yellow Coins")),

        # Whomp's Fortress
        (WF, "start_throwable_cork_boxes"): _spec(
            WF_TARGET, "", ("Throwable Cork Boxes", f"{WF} - Throwable Cork Boxes")),
        (WF, "start_flower_coin_ring"): _spec(
            WF_TARGET, "", ("Horizontal Coin Rings", f"{WF} - Horizontal Coin Rings")),
        (WF, "start_coin_line"): _spec(
            WF_TARGET, "", ("Horizontal Coin Lines", f"{WF} - Horizontal Coin Lines")),
        (WF, "falling_bridge_coin_line"): _spec(
            WF_TARGET, "", ("Horizontal Coin Lines", f"{WF} - Horizontal Coin Lines")),
        (WF, "rotating_plank_coins"): _spec(
            WF_TARGET, "", ("Single Yellow Coins", f"{WF} - Single Yellow Coins")),
        (WF, "water_slope_coin_line"): _spec(
            WF_TARGET, "", ("Horizontal Coin Lines", f"{WF} - Horizontal Coin Lines")),
        (WF, "water_coin_ring"): _spec(
            WF_TARGET, "", ("Horizontal Coin Rings", f"{WF} - Horizontal Coin Rings")),
        (WF, "buddy_coin_line"): _spec(
            WF_TARGET, "", ("Horizontal Coin Lines", f"{WF} - Horizontal Coin Lines")),
        (WF, "whomp_jump_coins"): _spec(WF_TARGET, "", ("Whomps", f"{WF} - Whomps")),
        (WF, "piranha_plant_coins"): _spec(
            WF_TARGET, "", (f"{WF} - Piranha Plants", f"{WF} - Piranha Plants")),
        (WF, "initial_red_coins"): _spec(WF_TARGET, "", ("Red Coins", f"{WF} - Red Coins")),
        (WF, "thwomp_red_coin"): _spec(
            WF_TARGET, "", ("Red Coins", f"{WF} - Red Coins"),
            ("Thwomps and Grindels", f"{WF} - Thwomps")),
        (WF, "wild_blue_route"): _spec(
            WF_TARGET,
            "CANN | logic_wf_into_the_wild_blue_yonder_wall_kick | "
            "logic_wf_into_the_wild_blue_yonder_long_jump | "
            "logic_wf_into_the_wild_blue_yonder_moveless & CL | "
            "logic_wf_into_the_wild_blue_yonder_moveless & SF | "
            "logic_wf_into_the_wild_blue_yonder_moveless & TJ+LG"),
        (WF, "wild_blue_coin_ring"): _spec(
            WF_TARGET,
            "CANN | logic_wf_into_the_wild_blue_yonder_wall_kick | "
            "logic_wf_into_the_wild_blue_yonder_long_jump | "
            "logic_wf_into_the_wild_blue_yonder_moveless & CL | "
            "logic_wf_into_the_wild_blue_yonder_moveless & SF | "
            "logic_wf_into_the_wild_blue_yonder_moveless & TJ+LG",
            ("Horizontal Coin Rings", f"{WF} - Horizontal Coin Rings")),
        (WF, "ground_pound_sources"): _spec(WF_TARGET, "GP"),
        (WF, "whomp_ground_pound_coins"): _spec(
            WF_TARGET, "GP", ("Whomps", f"{WF} - Whomps")),
        (WF, "blue_coin_block"): _spec(
            WF_TARGET, "GP", ("Blue Coin Blocks", f"{WF} - Blue Coin Block")),
        (WF, "top_region_sources"): _spec(WF_TARGET, f"{{{WF} - Top}}"),
        (WF, "top_floating_isle_ring"): _spec(
            WF_TARGET, f"{{{WF} - Top}}", ("Horizontal Coin Rings", f"{WF} - Horizontal Coin Rings")),
        (WF, "top_floating_arrow"): _spec(
            WF_TARGET, f"{{{WF} - Top}}", ("Coin Arrows", f"{WF} - Coin Arrows")),
        (WF, "top_red_coins"): _spec(
            WF_TARGET, f"{{{WF} - Top}}", ("Red Coins", f"{WF} - Red Coins")),

        # Jolly Roger Bay
        (JRB, "start_three_coin_block"): _spec(
            JRB_TARGET, "", ("3-Coin Blocks", f"{JRB} - 3-Coin Block")),
        (JRB, "clam_vertical_coin_ring"): _spec(
            JRB_TARGET, "", ("Vertical Coin Rings", f"{JRB} - Vertical Coin Rings")),
        (JRB, "tall_spike_coin_ring"): _spec(
            JRB_TARGET, "", ("Horizontal Coin Rings", f"{JRB} - Horizontal Coin Rings")),
        (JRB, "purple_switch_lower_coin_line"): _spec(
            JRB_TARGET, "", ("Vertical Coin Lines", f"{JRB} - Vertical Coin Lines")),
        (JRB, "jet_stream_coin_ring"): _spec(
            JRB_TARGET, "", ("Horizontal Coin Rings", f"{JRB} - Horizontal Coin Rings")),
        (JRB, "cave_chest_coin_ring"): _spec(
            JRB_TARGET, "", ("Horizontal Coin Rings", f"{JRB} - Horizontal Coin Rings")),
        (JRB, "main_goombas"): _spec(JRB_TARGET, "", ("Goombas", f"{JRB} - Goombas")),
        (JRB, "lower_red_coins"): _spec(JRB_TARGET, "", ("Red Coins", f"{JRB} - Red Coins")),
        (JRB, "pillar_red_coin_route"): _spec(
            JRB_TARGET, "CL | logic_jrb_pillar_red_coin_moves | logic_jrb_pillar_red_coin_cannon"),
        (JRB, "pillar_red_coin"): _spec(
            JRB_TARGET, "CL | logic_jrb_pillar_red_coin_moves | logic_jrb_pillar_red_coin_cannon",
            ("Red Coins", f"{JRB} - Red Coins")),
        (JRB, "upper_region_sources"): _spec(JRB_TARGET, f"{{{JRB} - Upper}}"),
        (JRB, "purple_switch_upper_coin_line"): _spec(
            JRB_TARGET, f"{{{JRB} - Upper}}", ("Vertical Coin Lines", f"{JRB} - Vertical Coin Lines")),
        (JRB, "raised_ship_approach_coin_lines"): _spec(
            JRB_TARGET, f"{{{JRB} - Upper}}",
            ("Horizontal Coin Lines", f"{JRB} - Horizontal Coin Lines")),
        (JRB, "raised_ship_red_coins"): _spec(
            JRB_TARGET, f"{{{JRB} - Upper}} & JRB_RAISED_SHIP",
            ("Red Coins", f"{JRB} - Red Coins")),
        # This source additionally requires Raised Ship to be absent. RuleFactory cannot express NOT.
        (JRB, "ship_alternative_red_coin"): _spec(
            JRB_TARGET,
            f"{{{JRB} - Upper}} & logic_jrb_ship_red_coin_with_long_jump | "
            f"{{{JRB} - Upper}} & PURPLE_SWITCHES",
            ("Red Coins", f"{JRB} - Red Coins")),
        (JRB, "blue_coin_block"): _spec(
            JRB_TARGET, "GP", ("Blue Coin Blocks", f"{JRB} - Blue Coin Block")),

        # Cool, Cool Mountain
        (CCM, "penguin_slide_yellow_coins"): _spec(
            CCM_TARGET, "", ("Single Yellow Coins", f"{CCM} - Single Yellow Coins")),
        (CCM, "penguin_slide_coin_lines"): _spec(
            CCM_TARGET, "", ("Horizontal Coin Lines", f"{CCM} - Horizontal Coin Lines")),
        (CCM, "chimney_vertical_coin_line"): _spec(
            CCM_TARGET, "", ("Vertical Coin Lines", f"{CCM} - Vertical Coin Lines")),
        (CCM, "main_mountain_coin_lines"): _spec(
            CCM_TARGET, "", ("Horizontal Coin Lines", f"{CCM} - Horizontal Coin Lines")),
        (CCM, "standard_mr_blizzard"): _spec(
            CCM_TARGET, "", ("Mr Blizzards", f"{CCM} - Mr Blizzards")),
        (CCM, "main_spindrifts"): _spec(CCM_TARGET, "", ("Spindrifts", f"{CCM} - Spindrifts")),
        (CCM, "red_coins"): _spec(CCM_TARGET, "", ("Red Coins", f"{CCM} - Red Coins")),
        (CCM, "slide_blue_coin"): _spec(
            CCM_TARGET, "", ("Single Blue Coins", f"{CCM} - Single Blue Coin")),
        (CCM, "wall_kicks_route"): _spec(
            CCM_TARGET, "CANN | logic_ccm_wall_kicks_will_work_spin_jump"),
        (CCM, "wall_kicks_coin_arrow"): _spec(
            CCM_TARGET, "CANN | logic_ccm_wall_kicks_will_work_spin_jump",
            ("Coin Arrows", f"{CCM} - Coin Arrows")),
        (CCM, "wall_kicks_spindrifts"): _spec(
            CCM_TARGET, "CANN | logic_ccm_wall_kicks_will_work_spin_jump",
            ("Spindrifts", f"{CCM} - Spindrifts")),
        (CCM, "blue_coin_block"): _spec(
            CCM_TARGET, "GP", ("Blue Coin Blocks", f"{CCM} - Blue Coin Block")),

        # Big Boo's Haunt
        (BBH, "mansion_ten_coin_block"): _spec(
            BBH_TARGET, "", ("10-Coin Blocks", f"{BBH} - 10-Coin Block")),
        (BBH, "shed_breakable_coin_boxes"): _spec(
            BBH_TARGET, "", ("Breakable Coin Boxes", f"{BBH} - Breakable Coin Boxes")),
        (BBH, "outside_crazy_box"): _spec(BBH_TARGET, "", ("Crazy Boxes", f"{BBH} - Crazy Box")),
        (BBH, "outside_scuttlebugs"): _spec(
            BBH_TARGET, "", ("Scuttlebugs", f"{BBH} - Scuttlebugs")),
        (BBH, "main_boos"): _spec(BBH_TARGET, "", ("Boos", f"{BBH} - Boos")),
        (BBH, "main_mr_is"): _spec(BBH_TARGET, "", ("Mr. Is", f"{BBH} - Mr. Is")),
        (BBH, "main_bookend"): _spec(
            BBH_TARGET, "", (f"{BBH} - Flying Bookends", f"{BBH} - Flying Bookends")),
        (BBH, "first_floor_red_coins"): _spec(
            BBH_TARGET, "", ("Red Coins", f"{BBH} - Red Coins")),
        (BBH, "second_floor_sources"): _spec(BBH_TARGET, f"{{{BBH} - Second Floor}}"),
        (BBH, "second_floor_bookends"): _spec(
            BBH_TARGET, f"{{{BBH} - Second Floor}}",
            (f"{BBH} - Flying Bookends", f"{BBH} - Flying Bookends")),
        (BBH, "second_floor_mr_i"): _spec(
            BBH_TARGET, f"{{{BBH} - Second Floor}}", ("Mr. Is", f"{BBH} - Mr. Is")),
        (BBH, "second_floor_red_coins"): _spec(
            BBH_TARGET, f"{{{BBH} - Second Floor}}", ("Red Coins", f"{BBH} - Red Coins")),
        (BBH, "second_floor_movement_red_coin"): _spec(
            BBH_TARGET, f"{{{BBH} - Second Floor}} & TJ/WK/BF/SF",
            ("Red Coins", f"{BBH} - Red Coins")),
        (BBH, "third_floor_sources"): _spec(BBH_TARGET, f"{{{BBH} - Third Floor}}"),
        (BBH, "third_floor_boo"): _spec(
            BBH_TARGET, f"{{{BBH} - Third Floor}}", ("Boos", f"{BBH} - Boos")),
        (BBH, "attic_blue_coin_block"): _spec(
            BBH_TARGET, f"{{{BBH} - Third Floor}} & GP",
            ("Blue Coin Blocks", f"{BBH} - Blue Coin Block")),
        (BBH, "merry_go_round_boos"): _spec(
            BBH_TARGET, "BBH_MERRY_GO_ROUND", ("Boos", f"{BBH} - Boos")),
    }
    return COIN_REQUIREMENT_SPECS


def _middle_requirement_specs():
    """RuleBuilder requirements for the middle group of course coin evaluators.

    This module is intentionally data-only.  ``unlocks`` contains global/per-level
    item-name pairs which are ANDed with ``rule`` by the eventual consumer.
    """



    UnlockPair = tuple[str, str]
    CoinRequirementSpec = dict[str, str | tuple[UnlockPair, ...]]

    COIN_REQUIREMENT_SPECS: dict[tuple[str, str], CoinRequirementSpec] = {}


    def _add(
            course: str,
            source_ids: str | tuple[str, ...],
            rule: str = "",
            unlocks: tuple[UnlockPair, ...] = (),
    ) -> None:
        if isinstance(source_ids, str):
            source_ids = (source_ids,)
        target = f"{course} - Coins Star"
        for source_id in source_ids:
            COIN_REQUIREMENT_SPECS[(course, source_id)] = {
                "rule": rule,
                "target": target,
                "unlocks": unlocks,
            }


    def _unlock(global_name: str, course: str, per_level_name: str | None = None) -> UnlockPair:
        return global_name, per_level_name or f"{course} - {global_name}"


    # Hazy Maze Cave
    HMC = "Hazy Maze Cave"
    HMC_BASIC = "WK/LG/BF/SF/TJ"
    HMC_PLATFORM = (
        f"{HMC_BASIC} & CL | "
        "logic_hmc_upper_red_coin_area_wall_kick"
    )
    HMC_PLATFORM_CHECKERBOARDS = (
        f"{HMC_BASIC} & CL & CHECKERBOARD_PLATFORMS | "
        "logic_hmc_upper_red_coin_area_wall_kick"
    )

    _add(HMC, ("start_coin_line", "maze_entrance_coin_line"),
         unlocks=(_unlock("Horizontal Coin Lines", HMC),))
    _add(HMC, "rolling_rocks_coins", unlocks=(_unlock("Single Yellow Coins", HMC),))
    _add(HMC, ("lake_approach_coin_ring",),
         unlocks=(_unlock("Horizontal Coin Rings", HMC),))
    _add(HMC, ("first_room_scuttlebugs", "pit_room_scuttlebug", "red_coin_room_scuttlebugs"),
         unlocks=(_unlock("Scuttlebugs", HMC),))
    _add(HMC, ("pit_room_swoop", "toxic_maze_swoops"),
         unlocks=(_unlock("Swoops", HMC),))
    _add(HMC, "toxic_maze_snufits", unlocks=(_unlock("Snufits", HMC),))
    _add(HMC, "basic_movement_sources", HMC_BASIC)
    _add(HMC, "lower_red_coin_room_coins", HMC_BASIC,
         (_unlock("Red Coins", HMC),))
    _add(HMC, "red_coin_room_mr_is", HMC_BASIC, (_unlock("Mr. Is", HMC),))
    _add(HMC, "pit_island_room_swoops", HMC_BASIC, (_unlock("Swoops", HMC),))
    _add(HMC, "upper_red_coin_pair_first",
         f"{HMC_BASIC} & CL & LJ/CHECKERBOARD_PLATFORMS | "
         "logic_hmc_upper_red_coin_area_wall_kick",
         (_unlock("Red Coins", HMC),))
    _add(HMC, "upper_red_coin_pair_checkerboards",
         HMC_PLATFORM_CHECKERBOARDS,
         (_unlock("Red Coins", HMC),))
    _add(HMC, "upper_red_coin_swoops",
         HMC_PLATFORM_CHECKERBOARDS,
         (_unlock("Swoops", HMC),))
    _add(HMC, "pit_islands_ceiling_coin_line", f"{{{HMC} - Pit Islands}} & CL",
         (_unlock("Horizontal Coin Lines", HMC),))
    _add(HMC, "swimming_beast_coin_ring", "HMC_SWIMMING_BEAST | logic_hmc_elevator_clip",
         (_unlock("Horizontal Coin Rings", HMC),))
    _add(HMC, "navigating_toxic_maze_sources", f"{{{{{HMC} - Navigating the Toxic Maze}}}}")
    _add(HMC, "toxic_maze_star_coin_line", f"{{{{{HMC} - Navigating the Toxic Maze}}}}",
         (_unlock("Horizontal Coin Lines", HMC),))
    _add(HMC, "toxic_maze_exit_swoops", f"{{{{{HMC} - Navigating the Toxic Maze}}}}",
         (_unlock("Swoops", HMC),))
    _add(HMC, "metal_head_scuttlebug",
         "PURPLE_SWITCHES & MC | PURPLE_SWITCHES & logic_hmc_metal_head_coin_route_capless",
         (_unlock("Scuttlebugs", HMC),))
    _add(HMC, "toxic_maze_blue_coin_block", "GP",
         (_unlock("Blue Coin Blocks", HMC, f"{HMC} - Blue Coin Block"),))


    # Lethal Lava Land
    LLL = "Lethal Lava Land"
    LLL_RED_ROUTE = "BOWSER_PUZZLE | LLL_KOOPA_SHELL | logic_lava_damage_boosting"
    LLL_HEALING = "SINGLE_YELLOW_COINS/HORIZONTAL_COIN_LINES/HORIZONTAL_COIN_RINGS/BULLIES/MR_IS"

    _add(LLL, (
        "lll_tilting_platform_coin_line", "lll_first_big_bully_coin_line",
        "lll_northwest_ramp_coin_line", "lll_north_volcano_coin_line",
        "lll_volcano_first_ridge_coin_line", "lll_volcano_second_bully_coin_line",
    ), unlocks=(_unlock("Horizontal Coin Lines", LLL),))
    _add(LLL, (
        "lll_grey_ramp_coins", "lll_sinking_platform_coins",
        "lll_spinning_volcano_platform_coins", "lll_southeast_grey_ramp_coins",
        "lll_volcano_s_island_coins", "lll_volcano_second_ridge_coins",
        "lll_volcano_floating_platform_coins", "lll_volcano_post_platform_coin",
        "lll_volcano_checkerboard_lift_coin",
    ), unlocks=(_unlock("Single Yellow Coins", LLL),))
    _add(LLL, "lll_bowser_puzzle_coins",
         unlocks=((f"{LLL} - Bowser Puzzle", f"{LLL} - Bowser Puzzle"),))
    _add(LLL, (
        "lll_second_big_bully_coin_ring", "lll_two_bullies_coin_ring",
        "lll_second_mr_i_coin_ring",
    ), unlocks=(_unlock("Horizontal Coin Rings", LLL),))
    _add(LLL, "lll_crazy_box_coins", unlocks=(_unlock("Crazy Boxes", LLL, f"{LLL} - Crazy Box"),))
    _add(LLL, "lll_first_five_red_coins", LLL_RED_ROUTE, (_unlock("Red Coins", LLL),))
    _add(LLL, "lll_remaining_three_red_coins",
         f"BOWSER_PUZZLE | LLL_KOOPA_SHELL & {LLL_HEALING} | "
         f"logic_lava_damage_boosting & {LLL_HEALING}",
         (_unlock("Red Coins", LLL),))
    _add(LLL, "lll_outside_bullies", unlocks=(_unlock("Bullies", LLL),))
    _add(LLL, "lll_mr_is", unlocks=(_unlock("Mr. Is", LLL),))
    _add(LLL, "lll_under_bridge_coin_line", "LLL_KOOPA_SHELL | logic_lava_damage_boosting",
         (_unlock("Single Yellow Coins", LLL),))
    _add(LLL, "lll_volcano_bullies", unlocks=(_unlock("Bullies", LLL),))
    _add(LLL, "lll_elevator_tour_platform_coins",
         f"{{{{{LLL} - Elevator Tour in the Volcano}}}}",
         (_unlock("Single Yellow Coins", LLL),))

    # Zero-coin route/group traces used as nested explanation nodes.
    _add(LLL, "lll_red_coin_unlock", unlocks=(_unlock("Red Coins", LLL),))
    _add(LLL, "lll_red_coin_bowser_puzzle_route",
         unlocks=((f"{LLL} - Bowser Puzzle", f"{LLL} - Bowser Puzzle"),))
    _add(LLL, "lll_red_coin_koopa_shell_route", "LLL_KOOPA_SHELL")
    _add(LLL, ("lll_red_coin_lava_damage_boosting_route",
               "lll_under_bridge_lava_damage_boosting_route"), "logic_lava_damage_boosting")
    _add(LLL, "lll_red_coin_healing_source", LLL_HEALING)
    _add(LLL, "lll_under_bridge_koopa_shell_route", "LLL_KOOPA_SHELL")
    _add(LLL, "lll_elevator_tour_location_access",
         f"{{{{{LLL} - Elevator Tour in the Volcano}}}}")


    # Shifting Sand Land
    SSL = "Shifting Sand Land"
    _add(SSL, "ssl_throwable_cork_box",
         unlocks=(_unlock("Throwable Cork Boxes", SSL, f"{SSL} - Throwable Cork Box"),))
    _add(SSL, "ssl_pillar_and_pyramid_coins", unlocks=(_unlock("Single Yellow Coins", SSL),))
    _add(SSL, ("ssl_behind_pyramid_coin_line", "ssl_pyramid_side_coin_line"),
         unlocks=(_unlock("Horizontal Coin Lines", SSL),))
    _add(SSL, "ssl_fly_guys", unlocks=(_unlock("Fly Guys", SSL, f"{SSL} - Fly Guys"),))
    _add(SSL, "ssl_crazy_boxes", unlocks=(_unlock("Crazy Boxes", SSL),))
    _add(SSL, "ssl_bob_ombs", unlocks=(_unlock("Bob-ombs", SSL),))
    _add(SSL, "ssl_pokeys", unlocks=(_unlock("Pokeys", SSL),))
    _add(SSL, "ssl_goombas", unlocks=(_unlock("Goombas", SSL),))
    _add(SSL, "ssl_low_red_coins", unlocks=(_unlock("Red Coins", SSL),))
    _add(SSL, "ssl_first_wire_grid_coin_ring", "CL",
         (_unlock("Horizontal Coin Rings", SSL),))
    _add(SSL, "ssl_first_wire_grid_climb", "CL")

    SSL_NORMAL_HIGH = "WC & TJ/CANN"
    SSL_TWEESTER = "logic_ssl_three_red_coins_with_tweesters"
    SSL_SHY_GUY = "logic_ssl_one_red_coin_with_shy_guy_spin_jump"
    _add(SSL, "ssl_high_red_coins",
         f"{SSL_NORMAL_HIGH} | {SSL_TWEESTER} | {SSL_SHY_GUY}",
         (_unlock("Red Coins", SSL),))
    _add(SSL, "ssl_normal_high_red_coin_route", SSL_NORMAL_HIGH,
         (_unlock("Red Coins", SSL),))
    _add(SSL, "ssl_tweester_red_coin_route", SSL_TWEESTER,
         (_unlock("Red Coins", SSL),))
    _add(SSL, "ssl_shy_guy_red_coin_route", SSL_SHY_GUY,
         (_unlock("Red Coins", SSL),))
    # No Despawns controls whether this reachable Red Coin contributes its two coins;
    # it is an option predicate and cannot be represented by a RuleFactory expression.
    _add(SSL, "ssl_shy_guy_red_coin_no_despawns")

    _add(SSL, "ssl_upper_pyramid_access_for_lines", f"{{{SSL} - Upper Pyramid}}")
    _add(SSL, ("ssl_second_wire_grid_coin_line", "ssl_pyramid_top_horizontal_coin_line"),
         f"{{{SSL} - Upper Pyramid}}", (_unlock("Horizontal Coin Lines", SSL),))
    _add(SSL, "ssl_pyramid_top_vertical_coin_line", f"{{{SSL} - Upper Pyramid}}",
         (_unlock("Vertical Coin Lines", SSL),))
    _add(SSL, "ssl_upper_pyramid_single_coins", f"{{{SSL} - Upper Pyramid}}",
         (_unlock("Single Yellow Coins", SSL),))
    _add(SSL, "ssl_upper_pyramid_access_for_singles", f"{{{SSL} - Upper Pyramid}}")
    _add(SSL, "ssl_blue_coin_block", "GP",
         (_unlock("Blue Coin Blocks", SSL, f"{SSL} - Blue Coin Block"),))
    _add(SSL, "ssl_blue_coin_block_ground_pound", "GP")


    # Dire, Dire Docks
    DDD = "Dire, Dire Docks"
    _add(DDD, ("ddd_start_wall_coin_line", "ddd_sub_area_dock_coin_line"),
         unlocks=(_unlock("Horizontal Coin Lines", DDD),))
    _add(DDD, ("ddd_chest_and_current_coin_lines", "ddd_moat_exit_coin_line"),
         unlocks=(_unlock("Vertical Coin Lines", DDD),))
    _add(DDD, "ddd_seafloor_chest_coins", unlocks=(_unlock("Single Yellow Coins", DDD),))
    _add(DDD, "ddd_sub_area_coin_rings", unlocks=(_unlock("Vertical Coin Rings", DDD),))
    _add(DDD, "ddd_seafloor_clam_coin_ring", unlocks=(_unlock("Horizontal Coin Rings", DDD),))

    DDD_FIRST_RED_ROUTE = "PURPLE_SWITCHES | DDD_BOWSER_SUB & DDD_POLES & CL & TJ"
    _add(DDD, "ddd_first_red_coin", DDD_FIRST_RED_ROUTE, (_unlock("Red Coins", DDD),))
    _add(DDD, "ddd_remaining_red_coins",
         "PURPLE_SWITCHES & DDD_POLES & CL | DDD_BOWSER_SUB & DDD_POLES & CL & TJ",
         (_unlock("Red Coins", DDD),))
    _add(DDD, "ddd_red_coin_purple_switch_route", "PURPLE_SWITCHES")
    _add(DDD, "ddd_red_coin_sub_poles_movement_route", "DDD_BOWSER_SUB & DDD_POLES & CL & TJ")
    _add(DDD, "ddd_remaining_red_coin_poles", "DDD_POLES")
    _add(DDD, "ddd_remaining_red_coin_climb", "CL")
    _add(DDD, "ddd_blue_coin_block", "PURPLE_SWITCHES & DDD_POLES & CL & GP",
         (_unlock("Blue Coin Blocks", DDD, f"{DDD} - Blue Coin Block"),))
    _add(DDD, "ddd_blue_coin_block_purple_switches", "PURPLE_SWITCHES")
    _add(DDD, "ddd_blue_coin_block_poles", "DDD_POLES")
    _add(DDD, "ddd_blue_coin_block_climb", "CL")
    _add(DDD, "ddd_blue_coin_block_ground_pound", "GP")


    # Snowman's Land
    SL = "Snowman's Land"
    _add(SL, "sl_start_coins", unlocks=(_unlock("Single Yellow Coins", SL),))
    _add(SL, "sl_spindrifts", unlocks=(_unlock("Spindrifts", SL),))
    _add(SL, "sl_start_mr_blizzards", unlocks=(_unlock("Mr Blizzards", SL),))
    _add(SL, "sl_moneybags",
         unlocks=((f"{SL} - Moneybags", f"{SL} - Moneybags"),))
    _add(SL, "sl_fly_guy", unlocks=(_unlock("Fly Guys", SL, f"{SL} - Fly Guy"),))
    _add(SL, "sl_whirl_red_coins", f"{{{SL} - Whirl from the Freezing Pond}}",
         (_unlock("Red Coins", SL),))
    _add(SL, "sl_whirl_region_access_for_red_coins", f"{{{SL} - Whirl from the Freezing Pond}}")

    # Exact evaluator condition is Whirl & Mr. Blizzard & (Cannon | No Despawns).
    # RuleFactory cannot express the No Despawns option predicate.  Requiring Cannon
    # here would produce a false missing requirement when No Despawns is the route,
    # so the shared portion is represented and the option-aware branch is left to
    # the consumer.
    _add(SL, "sl_whirl_mr_blizzard",
         f"{{{SL} - Whirl from the Freezing Pond}}",
         (_unlock("Mr Blizzards", SL),))
    _add(SL, "sl_whirl_region_access_for_mr_blizzard", f"{{{SL} - Whirl from the Freezing Pond}}")
    _add(SL, "sl_whirl_mr_blizzard_cannon_route", "CANN")
    _add(SL, "sl_whirl_mr_blizzard_no_despawns_route")

    _add(SL, "sl_upper_slope_coin_line", f"{{{SL} - Upper}}",
         (_unlock("Horizontal Coin Lines", SL),))
    _add(SL, ("sl_upper_slope_single_coins", "sl_penguin_and_face_coins"),
         f"{{{SL} - Upper}}", (_unlock("Single Yellow Coins", SL),))
    _add(SL, "sl_upper_spindrifts", f"{{{SL} - Upper}}", (_unlock("Spindrifts", SL),))
    _add(SL, "sl_upper_red_coins", f"{{{SL} - Upper}}", (_unlock("Red Coins", SL),))
    _add(SL, "sl_snowman_head_plank_coins", f"{{{SL} - Top of Snowman's Head}}",
         (_unlock("Single Yellow Coins", SL),))
    _add(SL, "sl_snowman_head_region_access", f"{{{SL} - Top of Snowman's Head}}")

    _add(SL, "sl_igloo_frozen_coin_lines", f"{{{SL} - Igloo}} & VC",
         (_unlock("Horizontal Coin Lines", SL),))
    _add(SL, "sl_igloo_single_coins", f"{{{SL} - Igloo}}",
         unlocks=(_unlock("Single Yellow Coins", SL),))
    _add(SL, "sl_igloo_three_coin_block", f"{{{SL} - Igloo}}",
         unlocks=(_unlock("3-Coin Blocks", SL, f"{SL} - 3-Coin Block"),))
    _add(SL, "sl_igloo_goombas", f"{{{SL} - Igloo}}", (_unlock("Goombas", SL),))
    _add(SL, "sl_igloo_spindrifts", f"{{{SL} - Igloo}}", (_unlock("Spindrifts", SL),))
    _add(SL, "sl_igloo_route", f"{{{SL} - Igloo}}")
    _add(SL, "sl_impossible_coin", "logic_sl_impossible_coin",
         (_unlock("Single Yellow Coins", SL),))
    _add(SL, "sl_impossible_coin_trick", "logic_sl_impossible_coin")


    del HMC, HMC_BASIC, HMC_PLATFORM, HMC_PLATFORM_CHECKERBOARDS
    del LLL, LLL_RED_ROUTE, LLL_HEALING
    del SSL, SSL_NORMAL_HIGH, SSL_TWEESTER, SSL_SHY_GUY
    del DDD, DDD_FIRST_RED_ROUTE, SL
    return COIN_REQUIREMENT_SPECS


def _late_requirement_specs():
    """Late coin-source requirements for structured CoinLogic explanations.

    This module is intentionally data-only.  Rules are RuleFactory expressions and
    ``unlocks`` contains the global/per-level item pair represented by each unlock
    token.
    """


    from typing import TypedDict


    UnlockPair = tuple[str, str]


    class CoinRequirementSpec(TypedDict):
        rule: str
        target: str
        unlocks: tuple[UnlockPair, ...]


    COIN_REQUIREMENT_SPECS: dict[tuple[str, str], CoinRequirementSpec] = {}


    _UNLOCK_RULE_TOKENS = {
        "Single Yellow Coins": "SINGLE_YELLOW_COINS",
        "Red Coins": "RED_COINS",
        "Single Blue Coins": "SINGLE_BLUE_COINS",
        "Horizontal Coin Lines": "HORIZONTAL_COIN_LINES",
        "Horizontal Coin Rings": "HORIZONTAL_COIN_RINGS",
        "Vertical Coin Lines": "VERTICAL_COIN_LINES",
        "Crazy Boxes": "CRAZY_BOXES",
        "Breakable Coin Boxes": "BREAKABLE_COIN_BOXES",
        "3-Coin Blocks": "THREE_COIN_BLOCKS",
        "10-Coin Blocks": "TEN_COIN_BLOCKS",
        "Blue Coin Blocks": "BLUE_COIN_BLOCKS",
        "Wooden Posts": "WOODEN_POSTS",
        "Bob-ombs": "BOB_OMBS",
        "Chuckyas": "CHUCKYA",
        "Fire Piranha Plants": "FIRE_PIRANHA_PLANTS",
        "Fly Guys": "FLY_GUY",
        "Goombas": "GOOMBAS",
        "Koopa Troopas": "KOOPA_TROOPA",
        "Lakitus": "LAKITU",
        "Skeeters": "SKEETERS",
    }


    def _remove_unlock_tokens(rule: str, unlocks: tuple[UnlockPair, ...]) -> str:
        """Keep object/enemy requirements in HasUnlock rather than RuleFactory."""
        for global_name, _per_level_name in unlocks:
            token = _UNLOCK_RULE_TOKENS[global_name]
            if rule == token:
                rule = ""
            else:
                rule = rule.replace(f"{token} & ", "").replace(f" & {token}", "")
        return rule


    def _add(course: str, source_id: str, rule: str, *unlocks: UnlockPair) -> None:
        COIN_REQUIREMENT_SPECS[course, source_id] = {
            "rule": _remove_unlock_tokens(rule, unlocks),
            "target": f"{course} - Coins Star",
            "unlocks": unlocks,
        }


    def _unlock(global_name: str, course: str, local_name: str | None = None) -> UnlockPair:
        return global_name, f"{course} - {local_name or global_name}"


    # Wet-Dry World
    WDW = "Wet-Dry World"
    _add(WDW, "main_skeeters", "{Wet-Dry World} & SKEETERS", _unlock("Skeeters", WDW))
    _add(WDW, "amp_ring", "{Wet-Dry World - Near the Top} & HORIZONTAL_COIN_RINGS",
         _unlock("Horizontal Coin Rings", WDW))
    _add(WDW, "pillar_ten_coin_block",
         "{Wet-Dry World - Near the Top} & {Wet-Dry World - Low Water} | "
         "{Wet-Dry World - Near the Top} & {Wet-Dry World - Mid Water} & HEAVE_HOS/SF/BF/TJ | "
         "{Wet-Dry World - Near the Top} & {Wet-Dry World - High Water} & LG | "
         "{Wet-Dry World - Near the Top} & {Wet-Dry World - Highest Water} | "
         "{Wet-Dry World - Near the Top} & {Wet-Dry World - Top}",
         _unlock("10-Coin Blocks", WDW))
    _add(WDW, "push_block_three_coin_block",
         "{Wet-Dry World - Near the Top} & THREE_COIN_BLOCKS", _unlock("3-Coin Blocks", WDW))
    _add(WDW, "low_breakable_boxes", "{Wet-Dry World - Low Water} & BREAKABLE_COIN_BOXES",
         _unlock("Breakable Coin Boxes", WDW))
    _add(WDW, "low_ten_coin_block", "{Wet-Dry World - Low Water} & TEN_COIN_BLOCKS",
         _unlock("10-Coin Blocks", WDW))
    _add(WDW, "low_blue_coins", "{Wet-Dry World - Low Water} & GP & BLUE_COIN_BLOCKS",
         _unlock("Blue Coin Blocks", WDW, "Blue Coin Block"))
    _add(WDW, "wooden_structure_three_coin_block",
         "{Wet-Dry World - Mid Water} | {Wet-Dry World - Top} | "
         "{Wet-Dry World - Top of the Express Elevator} & LJ",
         _unlock("3-Coin Blocks", WDW))
    _add(WDW, "fourth_diamond_coin_line",
         "{Wet-Dry World - Mid Water} | {Wet-Dry World - Highest Water} | "
         "{Wet-Dry World - Top} | {Wet-Dry World - Top of the Express Elevator} & LJ",
         _unlock("Horizontal Coin Lines", WDW))
    _add(WDW, "top_coin_line", "{Wet-Dry World - Top} & HORIZONTAL_COIN_LINES",
         _unlock("Horizontal Coin Lines", WDW))
    _add(WDW, "top_chuckya", "{Wet-Dry World - Top} & CHUCKYA", _unlock("Chuckyas", WDW, "Chuckya"))
    _add(WDW, "express_elevator_ten_coin_block",
         "{Wet-Dry World - Top of the Express Elevator} & TEN_COIN_BLOCKS",
         _unlock("10-Coin Blocks", WDW))
    _add(WDW, "downtown_ring", "{Wet-Dry World - Downtown} & HORIZONTAL_COIN_RINGS",
         _unlock("Horizontal Coin Rings", WDW))
    for _source in ("downtown_metal_cap_line", "downtown_first_building_line", "downtown_second_building_line"):
        _add(WDW, _source, "{Wet-Dry World - Downtown} & HORIZONTAL_COIN_LINES",
             _unlock("Horizontal Coin Lines", WDW))
    _add(WDW, "downtown_skeeters", "{Wet-Dry World - Downtown} & SKEETERS", _unlock("Skeeters", WDW))
    _add(WDW, "downtown_initial_red_coin", "{Wet-Dry World - Downtown} & RED_COINS",
         _unlock("Red Coins", WDW))
    _add(WDW, "downtown_diamond_red_coins", "{Wet-Dry World - Downtown} & WDW_WATER_LEVEL_DIAMOND & RED_COINS",
         _unlock("Red Coins", WDW))
    _add(WDW, "downtown_high_red_coins",
         "{Wet-Dry World - Downtown} & WDW_WATER_LEVEL_DIAMOND & WK | "
         "{Wet-Dry World - Downtown} & WDW_WATER_LEVEL_DIAMOND & logic_wdw_high_red_coins_triple_jump",
         _unlock("Red Coins", WDW))
    _add(WDW, "wdw_all_red_coins_reachable",
         "{Wet-Dry World - Downtown} & WDW_WATER_LEVEL_DIAMOND & WK | "
         "{Wet-Dry World - Downtown} & WDW_WATER_LEVEL_DIAMOND & logic_wdw_high_red_coins_triple_jump",
         _unlock("Red Coins", WDW))


    # Tall, Tall Mountain
    TTM = "Tall, Tall Mountain"
    _add(TTM, "ttm_start_coin_ring", "HORIZONTAL_COIN_RINGS", _unlock("Horizontal Coin Rings", TTM))
    _add(TTM, "ttm_crazy_box", "CRAZY_BOXES", _unlock("Crazy Boxes", TTM, "Crazy Box"))
    _add(TTM, "ttm_start_goombas", "GOOMBAS", _unlock("Goombas", TTM))
    _add(TTM, "ttm_middle_goomba", "{Tall, Tall Mountain - Middle} & GOOMBAS", _unlock("Goombas", TTM))
    _add(TTM, "ttm_middle_red_coins", "{Tall, Tall Mountain - Middle} & RED_COINS", _unlock("Red Coins", TTM))
    _add(TTM, "ttm_middle_bob_ombs", "{Tall, Tall Mountain - Middle} & BOB_OMBS", _unlock("Bob-ombs", TTM))
    _add(TTM, "ttm_middle_chuckya", "{Tall, Tall Mountain - Middle} & CHUCKYA", _unlock("Chuckyas", TTM, "Chuckya"))
    _add(TTM, "ttm_middle_bridge_coin_line", "{Tall, Tall Mountain - Middle} & HORIZONTAL_COIN_LINES",
         _unlock("Horizontal Coin Lines", TTM))
    _add(TTM, "ttm_middle_fly_guy", "{Tall, Tall Mountain - Middle} & FLY_GUY", _unlock("Fly Guys", TTM, "Fly Guy"))
    _add(TTM, "ttm_upper_red_coins", "{Tall, Tall Mountain - Upper} & RED_COINS", _unlock("Red Coins", TTM))
    _add(TTM, "ttm_upper_goombas", "{Tall, Tall Mountain - Upper} & GOOMBAS", _unlock("Goombas", TTM))
    _add(TTM, "ttm_upper_bob_ombs", "{Tall, Tall Mountain - Upper} & BOB_OMBS", _unlock("Bob-ombs", TTM))
    _add(TTM, "ttm_upper_leaf_climb_route", "CL")
    _add(TTM, "ttm_upper_leaf_moveless_route", "logic_ttm_coins_without_climb")
    _add(TTM, "ttm_upper_leaf_coin_line",
         "{Tall, Tall Mountain - Upper} & CL | "
         "{Tall, Tall Mountain - Upper} & logic_ttm_coins_without_climb",
         _unlock("Horizontal Coin Lines", TTM))
    _add(TTM, "ttm_top_goombas", "{Tall, Tall Mountain - Top} & GOOMBAS", _unlock("Goombas", TTM))
    _add(TTM, "ttm_hidden_coin_before_slide", "{Tall, Tall Mountain - Top} & SINGLE_YELLOW_COINS",
         _unlock("Single Yellow Coins", TTM))
    _add(TTM, "ttm_slide_single_coins", "{Tall, Tall Mountain - Top} & SINGLE_YELLOW_COINS",
         _unlock("Single Yellow Coins", TTM))
    for _source in ("ttm_slide_coin_lines", "ttm_slide_entrance_coin_line", "ttm_waterfall_bridge_coin_line"):
        _add(TTM, _source, "{Tall, Tall Mountain - Top} & HORIZONTAL_COIN_LINES",
             _unlock("Horizontal Coin Lines", TTM))
    _add(TTM, "ttm_slide_blue_coins", "{Tall, Tall Mountain - Top} & SINGLE_BLUE_COINS",
         _unlock("Single Blue Coins", TTM))
    _add(TTM, "ttm_top_switch_base_coins", "{Tall, Tall Mountain - Top} & VERTICAL_COIN_LINES",
         _unlock("Vertical Coin Lines", TTM))
    for _source, _rule in (
            ("ttm_top_switch_middle_purple_switch_route", "PURPLE_SWITCHES"),
            ("ttm_top_switch_middle_triple_jump_route", "TJ"),
            ("ttm_top_switch_middle_backflip_route", "BF"),
            ("ttm_top_switch_middle_side_flip_route", "SF")):
        _add(TTM, _source, _rule)
    _add(TTM, "ttm_top_switch_middle_coins",
         "{Tall, Tall Mountain - Top} & PURPLE_SWITCHES | "
         "{Tall, Tall Mountain - Top} & TJ/BF/SF",
         _unlock("Vertical Coin Lines", TTM))
    _add(TTM, "ttm_top_switch_highest_purple_switch_route", "PURPLE_SWITCHES")
    _add(TTM, "ttm_top_switch_highest_triple_jump_route", "TJ")
    _add(TTM, "ttm_top_switch_highest_coin",
         "{Tall, Tall Mountain - Top} & PURPLE_SWITCHES | {Tall, Tall Mountain - Top} & TJ",
         _unlock("Vertical Coin Lines", TTM))


    # Tiny-Huge Island physical source access.
    THI = "Tiny-Huge Island"
    _add(THI, "thi_tiny_variant", "{Tiny-Huge Island (Tiny)}")
    _add(THI, "thi_huge_variant", "{Tiny-Huge Island (Huge)}")
    _add(THI, "tiny_start_goomba", "{Tiny-Huge Island (Tiny)} & GOOMBAS", _unlock("Goombas", THI))
    _add(THI, "tiny_piranha_area_plant", "{Tiny-Huge Island - Tiny Piranha Area} & FIRE_PIRANHA_PLANTS",
         _unlock("Fire Piranha Plants", THI))
    _add(THI, "tiny_main_individual_coins", "{Tiny-Huge Island - Tiny Main} & SINGLE_YELLOW_COINS",
         _unlock("Single Yellow Coins", THI))
    _add(THI, "tiny_main_coin_line", "{Tiny-Huge Island - Tiny Main} & HORIZONTAL_COIN_LINES",
         _unlock("Horizontal Coin Lines", THI))
    _add(THI, "tiny_main_three_coin_block", "{Tiny-Huge Island - Tiny Main} & THREE_COIN_BLOCKS",
         _unlock("3-Coin Blocks", THI, "3-Coin Block"))
    _add(THI, "tiny_main_goombas", "{Tiny-Huge Island - Tiny Main} & GOOMBAS", _unlock("Goombas", THI))
    _add(THI, "tiny_main_koopa", "{Tiny-Huge Island - Tiny Main} & KOOPA_TROOPA",
         _unlock("Koopa Troopas", THI, "Koopa Troopas"))
    _add(THI, "tiny_impossible_coin",
         "{Tiny-Huge Island - Koopa the Quick} & HORIZONTAL_COIN_LINES & logic_thi_impossible_coin",
         _unlock("Horizontal Coin Lines", THI))
    _add(THI, "tiny_purple_switch_coin",
         "{Tiny-Huge Island - Tiny Main} & PURPLE_SWITCHES & SINGLE_YELLOW_COINS",
         _unlock("Single Yellow Coins", THI))

    _thi_huge_main = "{Tiny-Huge Island (Huge)}"
    for _source, _token, _global, _local in (
            ("huge_start_giant_goombas", "GOOMBAS", "Goombas", None),
            ("near_cannon_giant_goomba", "GOOMBAS", "Goombas", None),
            ("huge_start_post", "WOODEN_POSTS", "Wooden Posts", None),
            ("huge_beach_coins", "SINGLE_YELLOW_COINS", "Single Yellow Coins", None),
            ("huge_beach_fly_guy", "FLY_GUY", "Fly Guys", "Fly Guys"),
            ("huge_near_cannon_fly_guy", "FLY_GUY", "Fly Guys", "Fly Guys"),
            ("huge_lakitu", "LAKITU", "Lakitus", "Lakitu"),
            ("huge_koopa_troopa", "KOOPA_TROOPA", "Koopa Troopas", "Koopa Troopas")):
        _add(THI, _source, f"{_thi_huge_main} & {_token}", _unlock(_global, THI, _local))
    _add(THI, "huge_lakitu_island_post",
         "{Tiny-Huge Island (Huge)} & CANN | {Tiny-Huge Island - Koopa the Quick} & LJ",
         _unlock("Wooden Posts", THI))
    _add(THI, "huge_windswept_line", "{Tiny-Huge Island - Windswept Valley} & HORIZONTAL_COIN_LINES",
         _unlock("Horizontal Coin Lines", THI))
    _add(THI, "huge_windswept_giant_goombas", "{Tiny-Huge Island - Windswept Valley} & GOOMBAS",
         _unlock("Goombas", THI))
    _add(THI, "huge_cannonball_line", "{Tiny-Huge Island - Cannonball} & HORIZONTAL_COIN_LINES",
         _unlock("Horizontal Coin Lines", THI))
    _add(THI, "huge_cannonball_fly_guy", "{Tiny-Huge Island - Cannonball} & FLY_GUY",
         _unlock("Fly Guys", THI, "Fly Guys"))
    _add(THI, "huge_koopa_region_line", "{Tiny-Huge Island - Koopa the Quick} & HORIZONTAL_COIN_LINES",
         _unlock("Horizontal Coin Lines", THI))
    _add(THI, "huge_koopa_region_giant_goombas", "{Tiny-Huge Island - Koopa the Quick} & GOOMBAS",
         _unlock("Goombas", THI))
    _add(THI, "huge_top_wooden_plank_line", "{Tiny-Huge Island - Huge Top} & HORIZONTAL_COIN_LINES",
         _unlock("Horizontal Coin Lines", THI))
    _add(THI, "huge_top_chuckya", "{Tiny-Huge Island - Huge Top} & CHUCKYA", _unlock("Chuckyas", THI, "Chuckya"))

    _add(THI, "thi_red_coins_area", "{Tiny-Huge Island - Red Coins Area}")
    _add(THI, "red_area_giant_goombas", "{Tiny-Huge Island - Red Coins Area} & GOOMBAS", _unlock("Goombas", THI))
    _add(THI, "red_area_red_coins", "{Tiny-Huge Island - Red Coins Area} & RED_COINS", _unlock("Red Coins", THI))
    _add(THI, "red_area_wall_kick_red_coin", "{Tiny-Huge Island - Red Coins Area} & RED_COINS & WK",
         _unlock("Red Coins", THI))
    _add(THI, "red_area_blue_coins", "{Tiny-Huge Island - Red Coins Area} & GP & BLUE_COIN_BLOCKS",
         _unlock("Blue Coin Blocks", THI, "Blue Coin Block"))
    _add(THI, "red_area_plank_line", "{Tiny-Huge Island - Red Coins Area} & HORIZONTAL_COIN_LINES",
         _unlock("Horizontal Coin Lines", THI))
    _add(THI, "thi_wiggler_cave", "{Tiny-Huge Island - Tiny Main} & WARP_PIPES & GP")
    _add(THI, "wiggler_cave_coin_lines",
         "{Tiny-Huge Island - Tiny Main} & WARP_PIPES & GP & HORIZONTAL_COIN_LINES",
         _unlock("Horizontal Coin Lines", THI))
    _add(THI, "thi_huge_piranha_area", "{Tiny-Huge Island - Huge Piranha Area}")
    _add(THI, "huge_piranha_area_plants", "{Tiny-Huge Island - Huge Piranha Area} & FIRE_PIRANHA_PLANTS",
         _unlock("Fire Piranha Plants", THI))

    for _source in (
            "huge_start_giant_goombas", "near_cannon_giant_goomba", "huge_windswept_giant_goombas",
            "huge_koopa_region_giant_goombas", "red_area_giant_goombas"):
        _base = COIN_REQUIREMENT_SPECS[THI, _source]
        COIN_REQUIREMENT_SPECS[THI, f"{_source}_yellow"] = dict(_base)
        COIN_REQUIREMENT_SPECS[THI, f"{_source}_blue"] = {
            **_base,
            "rule": f"{_base['rule']} & GP",
        }
    COIN_REQUIREMENT_SPECS[THI, "near_cannon_giant_goomba_blue"] = {
        **COIN_REQUIREMENT_SPECS[THI, "near_cannon_giant_goomba"],
        "rule": f"{_thi_huge_main} & GOOMBAS & GP/FLY_GUY",
    }


    # Tick Tock Clock
    TTC = "Tick Tock Clock"
    _add(TTC, "ttc_start", "")
    _add(TTC, "ttc_start_ten_coin_block", "TEN_COIN_BLOCKS", _unlock("10-Coin Blocks", TTC))
    _add(TTC, "ttc_start_bob_ombs", "BOB_OMBS", _unlock("Bob-ombs", TTC))
    _add(TTC, "ttc_start_cube_coins", "SINGLE_YELLOW_COINS", _unlock("Single Yellow Coins", TTC))
    _add(TTC, "ttc_second_pendulum_block", "THREE_COIN_BLOCKS", _unlock("3-Coin Blocks", TTC))
    _add(TTC, "ttc_lower", "{Tick Tock Clock - First Clock Hand Area}")
    _add(TTC, "ttc_first_hand_block", "{Tick Tock Clock - First Clock Hand Area} & THREE_COIN_BLOCKS",
         _unlock("3-Coin Blocks", TTC))
    _add(TTC, "ttc_lower_red_coins", "{Tick Tock Clock - First Clock Hand Area} & RED_COINS", _unlock("Red Coins", TTC))
    _add(TTC, "ttc_spinner_red_coins", "{Tick Tock Clock - First Clock Hand Area} & RED_COINS & TTC_SPINNERS",
         _unlock("Red Coins", TTC))
    _add(TTC, "ttc_first_pole_coin_line",
         "{Tick Tock Clock - First Clock Hand Area} & {Tick Tock Clock Moving} | "
         "{Tick Tock Clock - First Clock Hand Area} & {Tick Tock Clock Stopped} & LG/BF/TJ/WK",
         _unlock("Horizontal Coin Lines", TTC))
    _add(TTC, "ttc_upper", "{Tick Tock Clock - Moving Bars Area}")
    _add(TTC, "ttc_heave_ho_blocks", "{Tick Tock Clock - Moving Bars Area} & THREE_COIN_BLOCKS",
         _unlock("3-Coin Blocks", TTC))
    _add(TTC, "ttc_blue_coin_block", "{Tick Tock Clock - Moving Bars Area} & GP & BLUE_COIN_BLOCKS",
         _unlock("Blue Coin Blocks", TTC, "Blue Coin Block"))
    _add(TTC, "ttc_top", "{Tick Tock Clock - Top}")
    _add(TTC, "ttc_timed_jumps_block", "{Tick Tock Clock - Top} & THREE_COIN_BLOCKS",
         _unlock("3-Coin Blocks", TTC))
    _add(TTC, "ttc_four_moving_bars_block", "{Tick Tock Clock - Top} & TEN_COIN_BLOCKS",
         _unlock("10-Coin Blocks", TTC))
    _add(TTC, "ttc_top_past_spinners", "{Tick Tock Clock - Top Past Spinners}")
    _add(TTC, "ttc_past_three_spinners_block", "{Tick Tock Clock - Top Past Spinners} & THREE_COIN_BLOCKS",
         _unlock("3-Coin Blocks", TTC))
    for _source in ("ttc_beneath_thwomp_block", "ttc_top_clock_hand_block", "ttc_top_central_platform_block"):
        _add(TTC, _source, "{Tick Tock Clock - Top Past Spinners} & TEN_COIN_BLOCKS",
             _unlock("10-Coin Blocks", TTC))


    # Rainbow Ride
    RR = "Rainbow Ride"
    _add(RR, "rr_initial", "")
    _add(RR, "rr_first_platform_ring",
         "RR_CARPETS | logic_rr_initial_coins_without_carpets",
         _unlock("Horizontal Coin Rings", RR))
    _add(RR, "rr_beneath_pole", "{Rainbow Ride - Beneath the Pole}")
    for _source in ("rr_fly_guy_line", "rr_second_swing_line", "rr_tricky_triangles_line"):
        _add(RR, _source, "{Rainbow Ride - Beneath the Pole} & HORIZONTAL_COIN_LINES",
             _unlock("Horizontal Coin Lines", RR))
    _add(RR, "rr_fly_guy", "{Rainbow Ride - Beneath the Pole} & FLY_GUY", _unlock("Fly Guys", RR, "Fly Guy"))
    _add(RR, "rr_first_swing_line", "{Rainbow Ride - Beneath the Pole} & VERTICAL_COIN_LINES",
         _unlock("Vertical Coin Lines", RR))
    _add(RR, "rr_first_donut_lift_coins", "{Rainbow Ride - Beneath the Pole} & SINGLE_YELLOW_COINS",
         _unlock("Single Yellow Coins", RR))
    _add(RR, "rr_beneath_pole_goomba", "{Rainbow Ride - Beneath the Pole} & GOOMBAS", _unlock("Goombas", RR, "Goomba"))
    _add(RR, "rr_maze", "{Rainbow Ride - Maze}")
    _add(RR, "rr_maze_coin_rings", "{Rainbow Ride - Maze} & HORIZONTAL_COIN_RINGS",
         _unlock("Horizontal Coin Rings", RR))
    _add(RR, "rr_maze_lakitu", "{Rainbow Ride - Maze} & LAKITU", _unlock("Lakitus", RR))
    _add(RR, "rr_carpets_lakitu", "{Rainbow Ride - Carpets} & LAKITU", _unlock("Lakitus", RR))
    _add(RR, "rr_maze_bob_ombs", "{Rainbow Ride - Maze} & BOB_OMBS", _unlock("Bob-ombs", RR))
    _add(RR, "rr_maze_blue_coin", "{Rainbow Ride - Maze} & BLUE_COIN_BLOCKS & GP",
         _unlock("Blue Coin Blocks", RR, "Blue Coin Block"))
    _add(RR, "rr_maze_wall_kick_blue_coins", "{Rainbow Ride - Maze} & BLUE_COIN_BLOCKS & GP & WK",
         _unlock("Blue Coin Blocks", RR, "Blue Coin Block"))
    _add(RR, "rr_maze_movement_red_coin",
         "{Rainbow Ride - Maze} & LJ/WK | "
         "{Rainbow Ride - Maze} & logic_rr_maze_coins_ledge_grab_and_carpets",
         _unlock("Red Coins", RR))
    _add(RR, "rr_other_red_coins",
         "{Rainbow Ride - Maze} & WK | {Rainbow Ride - Maze} & LJ & SF/BF/TJ | "
         "{Rainbow Ride - Maze} & logic_rr_maze_coins_ledge_grab_and_carpets",
         _unlock("Red Coins", RR))
    _add(RR, "rr_carpets", "{Rainbow Ride - Carpets}")
    for _source in ("rr_second_carpet_platform_coin", "rr_second_carpet_air_coin"):
        _add(RR, _source, "{Rainbow Ride - Carpets} & SINGLE_YELLOW_COINS", _unlock("Single Yellow Coins", RR))
    _add(RR, "rr_house", "{Rainbow Ride - House}")
    _add(RR, "rr_house_donut_lift_line", "{Rainbow Ride - House} & VERTICAL_COIN_LINES",
         _unlock("Vertical Coin Lines", RR))
    for _source in ("rr_house_floor_line", "rr_house_glass_platform_line", "rr_house_return_line"):
        _add(RR, _source, "{Rainbow Ride - House} & HORIZONTAL_COIN_LINES",
             _unlock("Horizontal Coin Lines", RR))
    _add(RR, "rr_cruiser", "{Rainbow Ride - Cruiser}")
    _add(RR, "rr_cruiser_bob_ombs", "{Rainbow Ride - Cruiser} & BOB_OMBS", _unlock("Bob-ombs", RR))
    _add(RR, "rr_ship_pole_ring", "{Rainbow Ride - Cruiser} & HORIZONTAL_COIN_RINGS",
         _unlock("Horizontal Coin Rings", RR))
    _add(RR, "rr_somewhere_over_the_rainbow", "{{Rainbow Ride - Somewhere Over the Rainbow}}")
    _add(RR, "rr_somewhere_chuckya", "{Rainbow Ride - Cruiser} & CHUCKYA",
         _unlock("Chuckyas", RR, "Chuckya"))
    return COIN_REQUIREMENT_SPECS


def _secrets_requirement_specs():
    """RuleBuilder requirement specifications for secret-stage coin sources.

    This is intentionally data-only groundwork.  ``rule`` contains the non-unlock
    portion of a complete source requirement.  ``unlocks`` contains global and
    per-level item alternatives that should be instantiated as ``HasUnlock`` rules.
    """



    def _spec(
            target: str,
            rule: str = "",
            *unlocks: tuple[str, str],
    ) -> dict[str, str | tuple[tuple[str, str], ...]]:
        return {"rule": rule, "target": target, "unlocks": unlocks}


    PSS = "The Princess's Secret Slide"
    SA = "The Secret Aquarium"
    WMOTR = "Wing Mario Over the Rainbow"
    TOTWC = "Tower of the Wing Cap"
    VCUTM = "Vanish Cap Under the Moat"
    COTMC = "Cavern of the Metal Cap"
    BITDW = "Bowser in the Dark World"
    BITFS = "Bowser in the Fire Sea"
    BITS = "Bowser in the Sky"
    CASTLE = "Castle"


    def _target(course: str) -> str:
        return f"{course} - Coins Star"


    COIN_REQUIREMENT_SPECS: dict[
        tuple[str, str], dict[str, str | tuple[tuple[str, str], ...]]
    ] = {
        # The Princess's Secret Slide
        (PSS, "pss_course"): _spec(_target(PSS)),
        (PSS, "pss_single_yellow_coins"): _spec(
            _target(PSS), "", ("Single Yellow Coins", "Princess's Secret Slide - Single Yellow Coins")),
        (PSS, "pss_horizontal_coin_lines"): _spec(
            _target(PSS), "", ("Horizontal Coin Lines", "Princess's Secret Slide - Horizontal Coin Lines")),
        (PSS, "pss_blue_coin_block"): _spec(
            _target(PSS), "GP", ("Blue Coin Blocks", "Princess's Secret Slide - Blue Coin Block")),

        # The Secret Aquarium
        (SA, "sa_course"): _spec(_target(SA)),
        (SA, "sa_red_coins"): _spec(
            _target(SA), "", ("Red Coins", "Secret Aquarium - Red Coins")),
        (SA, "sa_horizontal_coin_ring"): _spec(
            _target(SA), "", ("Horizontal Coin Rings", "Secret Aquarium - Horizontal Coin Rings")),
        (SA, "sa_vertical_coin_rings"): _spec(
            _target(SA), "", ("Vertical Coin Rings", "Secret Aquarium - Vertical Coin Rings")),

        # Wing Mario Over the Rainbow
        (WMOTR, "wmotr_initial"): _spec(_target(WMOTR)),
        (WMOTR, "wmotr_initial_red_coin"): _spec(
            _target(WMOTR), "", ("Red Coins", f"{WMOTR} - Red Coins")),
        (WMOTR, "wmotr_cannon_only"): _spec(_target(WMOTR), f"{{{WMOTR} - Cannon}}"),
        (WMOTR, "wmotr_cannon_red_coins"): _spec(
            _target(WMOTR), f"{{{WMOTR} - Cannon}}", ("Red Coins", f"{WMOTR} - Red Coins")),
        (WMOTR, "wmotr_flight_route"): _spec(
            _target(WMOTR), f"{{{WMOTR} - Cannon}} | WC+TJ"),
        (WMOTR, "wmotr_flight_red_coins"): _spec(
            _target(WMOTR), f"{{{WMOTR} - Cannon}} | WC+TJ", ("Red Coins", f"{WMOTR} - Red Coins")),
        (WMOTR, "wmotr_rainbow_coin_rings"): _spec(
            _target(WMOTR), f"{{{WMOTR} - Cannon}} | WC+TJ",
            ("Vertical Coin Rings", f"{WMOTR} - Vertical Coin Rings")),
        (WMOTR, "wmotr_cloud_coin_ring"): _spec(
            _target(WMOTR), f"{{{WMOTR} - Cannon}} | WC+TJ",
            ("Horizontal Coin Rings", f"{WMOTR} - Horizontal Coin Rings")),
        # This route is selected only while the flight route is unavailable. RuleFactory expressions
        # cannot represent that non-monotonic selection condition.
        (WMOTR, "wmotr_leap_fallback"): _spec(_target(WMOTR)),
        (WMOTR, "wmotr_long_jump_first_red_coin"): _spec(
            _target(WMOTR),
            "logic_wmotr_leap_of_faith | logic_wmotr_leap_of_faith_without_ledge_grab",
            ("Red Coins", f"{WMOTR} - Red Coins")),
        (WMOTR, "wmotr_long_jump_second_red_coin"): _spec(
            _target(WMOTR),
            "logic_wmotr_leap_of_faith_without_ledge_grab | LG & logic_wmotr_leap_of_faith",
            ("Red Coins", f"{WMOTR} - Red Coins")),
        # The evaluator additionally suppresses this source when the Long Jump fallback is available.
        (WMOTR, "wmotr_wing_cap_fallback_red_coin"): _spec(
            _target(WMOTR),
            "WC & SELECTED_TRICK:logic_wmotr_leap_of_faith | "
            "WC & SELECTED_TRICK:logic_wmotr_leap_of_faith_without_ledge_grab",
            ("Red Coins", f"{WMOTR} - Red Coins")),

        # Tower of the Wing Cap
        (TOTWC, "totwc_course"): _spec(_target(TOTWC)),
        (TOTWC, "totwc_single_yellow_coins"): _spec(
            _target(TOTWC), "", ("Single Yellow Coins", f"{TOTWC} - Single Yellow Coins")),
        (TOTWC, "totwc_red_coins"): _spec(
            _target(TOTWC), "", ("Red Coins", f"{TOTWC} - Red Coins")),
        (TOTWC, "totwc_mastery_ring_route"): _spec(_target(TOTWC)),
        (TOTWC, "totwc_mastery_ring_coins"): _spec(
            _target(TOTWC), "",
            ("Vertical Coin Rings", f"{TOTWC} - Vertical Coin Rings")),
        (TOTWC, "totwc_mastery_wing_cap_ring_coins"): _spec(
            _target(TOTWC), "WC",
            ("Vertical Coin Rings", f"{TOTWC} - Vertical Coin Rings"),
            ("Wing Cap", f"{TOTWC} - Wing Cap")),
        # This synthetic trace is present only when the dynamic logic/option cap removes coins.
        (TOTWC, "totwc_coin_cap"): _spec(_target(TOTWC)),

        # Vanish Cap Under the Moat
        (VCUTM, "vcutm_earlier_slide_route"): _spec(_target(VCUTM)),
        (VCUTM, "vcutm_bottom_slide_line"): _spec(
            _target(VCUTM), "", ("Horizontal Coin Lines", f"{VCUTM} - Horizontal Coin Lines")),
        (VCUTM, "vcutm_earlier_red_coins"): _spec(
            _target(VCUTM), "", ("Red Coins", f"{VCUTM} - Red Coins")),
        (VCUTM, "vcutm_later_checkerboard_route"): _spec(
            _target(VCUTM),
            "TJ/LG/SF/BF/WK | logic_vcutm_drop_to_checkerboard_platforms | "
            "logic_vcutm_drop_to_checkerboard_platforms_after_crawling_back_up"),
        (VCUTM, "vcutm_turning_lifts_block"): _spec(
            _target(VCUTM),
            "TJ/LG/SF/BF/WK | logic_vcutm_drop_to_checkerboard_platforms | "
            "logic_vcutm_drop_to_checkerboard_platforms_after_crawling_back_up",
            ("3-Coin Blocks", f"{VCUTM} - 3-Coin Block")),
        (VCUTM, "vcutm_checkerboard_red_coins"): _spec(
            _target(VCUTM),
            "CHECKERBOARD_PLATFORMS & TJ/LG/SF/BF/WK | "
            "CHECKERBOARD_PLATFORMS & logic_vcutm_drop_to_checkerboard_platforms | "
            "CHECKERBOARD_PLATFORMS & logic_vcutm_drop_to_checkerboard_platforms_after_crawling_back_up",
            ("Red Coins", f"{VCUTM} - Red Coins"),
            ("Checkerboard Platforms", f"{VCUTM} - Checkerboard Platforms")),
        (VCUTM, "vcutm_end_marker_coins"): _spec(
            _target(VCUTM),
            "CHECKERBOARD_PLATFORMS & VC & TJ/LG/SF/BF/WK | "
            "CHECKERBOARD_PLATFORMS & VC & logic_vcutm_drop_to_checkerboard_platforms | "
            "CHECKERBOARD_PLATFORMS & VC & logic_vcutm_drop_to_checkerboard_platforms_after_crawling_back_up",
            ("Single Yellow Coins", f"{VCUTM} - Single Yellow Coins"),
            ("Checkerboard Platforms", f"{VCUTM} - Checkerboard Platforms"),
            ("Vanish Cap", f"{VCUTM} - Vanish Cap")),
        # Route selection also compares the reachable earlier/later totals. The positive access rules
        # above are exact, but that total-dependent selection is not expressible by RuleFactory.

        # Cavern of the Metal Cap
        (COTMC, "cotmc_course"): _spec(_target(COTMC)),
        (COTMC, "cotmc_underwater_slope_line"): _spec(
            _target(COTMC), "", ("Horizontal Coin Lines", f"{COTMC} - Horizontal Coin Lines")),
        (COTMC, "cotmc_rock_bridge_line"): _spec(
            _target(COTMC), "", ("Horizontal Coin Lines", f"{COTMC} - Horizontal Coin Lines")),
        (COTMC, "cotmc_snufits"): _spec(
            _target(COTMC), "", ("Snufits", f"{COTMC} - Snufits")),
        (COTMC, "cotmc_initial_red_coins"): _spec(
            _target(COTMC), "", ("Red Coins", f"{COTMC} - Red Coins")),
        (COTMC, "cotmc_deep_water"): _spec(
            _target(COTMC), "MC | logic_cotmc_deep_underwater_coins_without_metal_cap"),
        (COTMC, "cotmc_underwater_ring"): _spec(
            _target(COTMC), "MC | logic_cotmc_deep_underwater_coins_without_metal_cap",
            ("Horizontal Coin Rings", f"{COTMC} - Horizontal Coin Rings")),
        (COTMC, "cotmc_stream_bottom_line"): _spec(
            _target(COTMC), "MC | logic_cotmc_deep_underwater_coins_without_metal_cap",
            ("Horizontal Coin Lines", f"{COTMC} - Horizontal Coin Lines")),
        (COTMC, "cotmc_deep_red_coins"): _spec(
            _target(COTMC), "MC | logic_cotmc_deep_underwater_coins_without_metal_cap",
            ("Red Coins", f"{COTMC} - Red Coins")),

        # Bowser in the Dark World
        (BITDW, "bitdw_before_slope"): _spec(_target(BITDW)),
        (BITDW, "bitdw_coin_rings"): _spec(
            _target(BITDW), "", ("Horizontal Coin Rings", f"{BITDW} - Horizontal Coin Rings")),
        (BITDW, "bitdw_coin_lines"): _spec(
            _target(BITDW), "", ("Horizontal Coin Lines", f"{BITDW} - Horizontal Coin Lines")),
        (BITDW, "bitdw_single_coins_before_slope"): _spec(
            _target(BITDW), "", ("Single Yellow Coins", f"{BITDW} - Single Yellow Coins")),
        (BITDW, "bitdw_three_coin_block"): _spec(
            _target(BITDW), "", ("3-Coin Blocks", f"{BITDW} - 3-Coin Block")),
        (BITDW, "bitdw_goombas"): _spec(
            _target(BITDW), "", ("Goombas", f"{BITDW} - Goombas")),
        (BITDW, "bitdw_red_coins_before_slope"): _spec(
            _target(BITDW), "", ("Red Coins", f"{BITDW} - Red Coins")),
        (BITDW, "bitdw_slope"): _spec(
            _target(BITDW), "PURPLE_SWITCHES | logic_bitdw_purple_switch_bypass"),
        (BITDW, "bitdw_slope_single_coins"): _spec(
            _target(BITDW), "PURPLE_SWITCHES | logic_bitdw_purple_switch_bypass",
            ("Single Yellow Coins", f"{BITDW} - Single Yellow Coins")),
        (BITDW, "bitdw_slope_red_coins"): _spec(_target(BITDW), "PURPLE_SWITCHES"),
        (BITDW, "bitdw_final_red_coins"): _spec(
            _target(BITDW), "PURPLE_SWITCHES", ("Red Coins", f"{BITDW} - Red Coins")),

        # Bowser in the Fire Sea
        (BITFS, "bitfs_start"): _spec(_target(BITFS)),
        (BITFS, "bitfs_start_single_coins"): _spec(
            _target(BITFS), "", ("Single Yellow Coins", f"{BITFS} - Single Yellow Coins")),
        (BITFS, "bitfs_second_sinking_platform_line"): _spec(
            _target(BITFS), "", ("Horizontal Coin Lines", f"{BITFS} - Horizontal Coin Lines")),
        (BITFS, "bitfs_first_ring"): _spec(
            _target(BITFS), "", ("Horizontal Coin Rings", f"{BITFS} - Horizontal Coin Rings")),
        (BITFS, "bitfs_first_bully"): _spec(
            _target(BITFS), "", ("Bullies", f"{BITFS} - Bullies")),
        (BITFS, "bitfs_start_goombas"): _spec(
            _target(BITFS), "", ("Goombas", f"{BITFS} - Goombas")),
        (BITFS, "bitfs_start_red_coins"): _spec(
            _target(BITFS), "", ("Red Coins", f"{BITFS} - Red Coins")),
        (BITFS, "bitfs_rising_platform_block"): _spec(
            _target(BITFS), "CL | logic_lava_damage_boosting"),
        (BITFS, "bitfs_three_coin_block"): _spec(
            _target(BITFS), "CL | logic_lava_damage_boosting",
            ("3-Coin Blocks", f"{BITFS} - 3-Coin Block")),
        (BITFS, "bitfs_climb"): _spec(_target(BITFS), "CL"),
        (BITFS, "bitfs_elevator_line"): _spec(
            _target(BITFS), "CL", ("Horizontal Coin Lines", f"{BITFS} - Horizontal Coin Lines")),
        (BITFS, "bitfs_wire_grid_ring"): _spec(
            _target(BITFS), "CL", ("Horizontal Coin Rings", f"{BITFS} - Horizontal Coin Rings")),
        (BITFS, "bitfs_vertical_drop_line"): _spec(
            _target(BITFS), "CL", ("Vertical Coin Lines", f"{BITFS} - Vertical Coin Lines")),
        (BITFS, "bitfs_bob_omb_slope_line"): _spec(
            _target(BITFS), "CL", ("Horizontal Coin Lines", f"{BITFS} - Horizontal Coin Lines")),
        (BITFS, "bitfs_ten_coin_block"): _spec(
            _target(BITFS), "CL", ("10-Coin Blocks", f"{BITFS} - 10-Coin Block")),
        (BITFS, "bitfs_third_sinking_platform_line"): _spec(
            _target(BITFS), "CL", ("Horizontal Coin Lines", f"{BITFS} - Horizontal Coin Lines")),
        (BITFS, "bitfs_bob_omb"): _spec(
            _target(BITFS), "CL", ("Bob-ombs", f"{BITFS} - Bob-omb")),
        (BITFS, "bitfs_upper_bullies"): _spec(
            _target(BITFS), "CL", ("Bullies", f"{BITFS} - Bullies")),
        (BITFS, "bitfs_upper_red_coins"): _spec(
            _target(BITFS), "CL", ("Red Coins", f"{BITFS} - Red Coins")),

        # Bowser in the Sky
        (BITS, "bits_start"): _spec(_target(BITS)),
        (BITS, "bits_tilting_w_coins"): _spec(
            _target(BITS), "", ("Single Yellow Coins", f"{BITS} - Single Yellow Coins")),
        (BITS, "bits_start_goombas"): _spec(
            _target(BITS), "", ("Goombas", f"{BITS} - Goombas")),
        (BITS, "bits_start_red_coins"): _spec(
            _target(BITS), "", ("Red Coins", f"{BITS} - Red Coins")),
        (BITS, "bits_start_fire_piranha"): _spec(
            _target(BITS), "", ("Fire Piranha Plants", f"{BITS} - Fire Piranha Plants")),
        (BITS, "bits_whomp_platform_lines"): _spec(
            _target(BITS), "", ("Horizontal Coin Lines", f"{BITS} - Horizontal Coin Lines")),
        (BITS, "bits_whomp_jump_coins"): _spec(
            _target(BITS), "", ("Whomps", f"{BITS} - Whomp")),
        (BITS, "bits_whomp_ground_pound_coins"): _spec(
            _target(BITS), "GP", ("Whomps", f"{BITS} - Whomp")),
        (BITS, "bits_chuckya"): _spec(_target(BITS), f"{{{BITS} - Chuckya}}"),
        (BITS, "bits_chuckya_enemy"): _spec(
            _target(BITS), f"{{{BITS} - Chuckya}}", ("Chuckyas", f"{BITS} - Chuckya")),
        (BITS, "bits_chuckya_goomba"): _spec(
            _target(BITS), f"{{{BITS} - Chuckya}}", ("Goombas", f"{BITS} - Goombas")),
        (BITS, "bits_raised_steps_coins"): _spec(
            _target(BITS), f"{{{BITS} - Chuckya}}",
            ("Single Yellow Coins", f"{BITS} - Single Yellow Coins")),
        (BITS, "bits_arrow_ride"): _spec(_target(BITS), f"{{{BITS} - Arrow Ride}}"),
        (BITS, "bits_suction_platform_line"): _spec(
            _target(BITS), f"{{{BITS} - Arrow Ride}}",
            ("Horizontal Coin Lines", f"{BITS} - Horizontal Coin Lines")),
        (BITS, "bits_arrow_ride_red_coins"): _spec(
            _target(BITS), f"{{{BITS} - Arrow Ride}}", ("Red Coins", f"{BITS} - Red Coins")),
        (BITS, "bits_spinning_platform_coins"): _spec(
            _target(BITS), f"{{{BITS} - Arrow Ride}}",
            ("Single Yellow Coins", f"{BITS} - Single Yellow Coins")),
        (BITS, "bits_arrow_ride_bob_ombs"): _spec(
            _target(BITS), f"{{{BITS} - Arrow Ride}}", ("Bob-ombs", f"{BITS} - Bob-ombs")),
        (BITS, "bits_arrow_ride_fire_piranha"): _spec(
            _target(BITS), f"{{{BITS} - Arrow Ride}}",
            ("Fire Piranha Plants", f"{BITS} - Fire Piranha Plants")),
        (BITS, "bits_top"): _spec(_target(BITS), f"{{{BITS} - Top}}"),
        (BITS, "bits_top_goombas"): _spec(
            _target(BITS), f"{{{BITS} - Top}}", ("Goombas", f"{BITS} - Goombas")),
        (BITS, "bits_top_bob_ombs"): _spec(
            _target(BITS), f"{{{BITS} - Top}}", ("Bob-ombs", f"{BITS} - Bob-ombs")),
        (BITS, "bits_top_red_coins"): _spec(
            _target(BITS), f"{{{BITS} - Top}}", ("Red Coins", f"{BITS} - Red Coins")),
        (BITS, "bits_final_rotating_platform_line"): _spec(
            _target(BITS), f"{{{BITS} - Top}}",
            ("Horizontal Coin Lines", f"{BITS} - Horizontal Coin Lines")),

        # Castle Grounds, interior, and courtyard. These have no Coin Count Checks.
        (CASTLE, "castle_grounds_bridge_coins"): _spec(
            "Castle - Bridge Coins 1-Up", "{{Castle - Drain the Moat}} & WK & TJ/SF",
            ("Single Yellow Coins", "Castle - Single Yellow Coins")),
        (CASTLE, "castle_lobby_coins"): _spec(
            "Castle", "", ("Single Yellow Coins", "Castle - Single Yellow Coins")),
        (CASTLE, "castle_courtyard_boos"): _spec(
            "Castle", "", ("Boos", "Castle - Boos")),
    }
    return COIN_REQUIREMENT_SPECS


@cache
def _coin_source_rule_specs() -> dict[tuple[str, str], CoinSourceRuleSpec]:
    combined: dict[tuple[str, str], CoinSourceRuleSpec] = {}
    for group in (
            _early_requirement_specs(),
            _middle_requirement_specs(),
            _late_requirement_specs(),
            _secrets_requirement_specs(),
    ):
        duplicates = combined.keys() & group.keys()
        if duplicates:
            raise ValueError(f"Duplicate coin requirement specs: {sorted(duplicates)}")
        combined.update(group)
    return combined

def _split_top_level(expression: str, operators: str) -> list[str]:
    depth = 0
    brace_depth = 0
    pieces: list[str] = []
    start = 0
    for index, character in enumerate(expression):
        if character == "{":
            brace_depth += 1
        elif character == "}":
            brace_depth -= 1
        elif not brace_depth:
            if character == "(":
                depth += 1
            elif character == ")":
                depth -= 1
            elif depth == 0 and character in operators:
                pieces.append(expression[start:index].strip())
                start = index + 1
    if pieces:
        pieces.append(expression[start:].strip())
    return pieces


def _strip_outer_parentheses(expression: str) -> str:
    expression = expression.strip()
    while expression.startswith("(") and expression.endswith(")"):
        depth = 0
        encloses_all = True
        for index, character in enumerate(expression):
            if character == "(":
                depth += 1
            elif character == ")":
                depth -= 1
                if depth == 0 and index != len(expression) - 1:
                    encloses_all = False
                    break
        if not encloses_all:
            break
        expression = expression[1:-1].strip()
    return expression


def _build_expression_rule(rf, expression: str, target_name: str, arbitrary_item_names) -> Rule:
    expression = _strip_outer_parentheses(expression)
    if not expression:
        return True_()

    alternatives = _split_top_level(expression, "|/")
    if alternatives:
        return Or(*(_build_expression_rule(rf, part, target_name, arbitrary_item_names)
                    for part in alternatives))

    requirements = _split_top_level(expression, "&+")
    if requirements:
        return And(*(_build_expression_rule(rf, part, target_name, arbitrary_item_names)
                     for part in requirements))

    atom = _TOKEN_ALIASES.get(expression, expression)
    selected_trick_prefix = "SELECTED_TRICK:"
    if atom.startswith(selected_trick_prefix):
        from .LogicTricks import logic_tricks

        internal_id = atom[len(selected_trick_prefix):]
        option_key = next(
            key for key, data in logic_tricks.items()
            if data["internal_id"] == internal_id
        )
        world = rf.multiworld.worlds[rf.player]
        if getattr(world, internal_id, False):
            return LogicTrick(option_key, True_())
        if getattr(world, f"{internal_id}_ut_glitch", False):
            return LogicTrick(option_key, True_(), ut_glitched=True)
        return False_()
    result = rf.make_rule(
        atom,
        rf.get_cannon_item_name(target_name),
        rf.get_cap_item_names(target_name),
        arbitrary_item_names,
        rf.get_action_item_names(target_name),
    )
    if result is True:
        return True_()
    if result is False:
        return False_()
    if isinstance(result, Rule):
        return result
    from rule_builder.rules import Has
    return Has(result)


def get_coin_requirement_rule(
        course_name: str,
        source_id: str,
        state: CollectionState,
        player: int,
) -> Rule.Resolved | None:
    """Build the Rule Builder rule explaining one structured coin source."""
    spec = _coin_source_rule_specs().get((course_name, source_id))
    if spec is None:
        return None

    world: SM64World = state.multiworld.worlds[player]
    cache = getattr(world, "coin_requirement_rule_cache", None)
    if cache is None:
        cache = {}
        world.coin_requirement_rule_cache = cache
    cache_key = (course_name, source_id)
    if cache_key in cache:
        return cache[cache_key]

    from .Rules import RuleFactory

    target_name = spec.get("target", course_name)
    rule_expression = spec.get("rule", "")
    unlocks = spec.get("unlocks", ())
    if not rule_expression and not unlocks:
        cache[cache_key] = None
        return None

    rf = RuleFactory(world.multiworld, world.options, player, world.move_rando_bitvec)
    arbitrary_item_names = rf.get_arbitrary_item_names(target_name)
    level_name = rf.get_level_name_from_target(target_name)
    for token, (global_name, local_suffix) in _EXPLANATION_ONLY_UNLOCKS.items():
        arbitrary_item_names[token] = HasUnlock(
            global_name, f"{level_name} - {local_suffix}")
    rule = _build_expression_rule(
        rf, rule_expression, target_name, arbitrary_item_names)
    for global_item_name, per_level_item_name in unlocks:
        rule &= HasUnlock(global_item_name, per_level_item_name)

    resolved = rule.resolve(world)
    cache[cache_key] = resolved
    return resolved
