from __future__ import annotations

import dataclasses
import random
import re
from collections import defaultdict
from collections.abc import Iterable, Mapping, Sequence
from enum import Enum

from .CoinCheckData import SOURCE_LAYOUTS


INDIVIDUAL_COIN_LOCATION_BASE_ID = 4_000_000
INDIVIDUAL_COIN_COURSE_STRIDE = 1_000


class CoinOutputKind(Enum):
    YELLOW = "yellow"
    RED = "red"
    BLUE = "blue"


@dataclasses.dataclass(frozen=True, order=True)
class CoinOutputID:
    course_name: str
    source_id: str
    output_index: int


@dataclasses.dataclass(frozen=True)
class CoinOutputDefinition:
    output_id: CoinOutputID
    location_id: int
    location_name: str
    kind: CoinOutputKind
    coin_value: int
    source_methods: tuple[str, ...]


@dataclasses.dataclass(frozen=True)
class CoinSourceDefinition:
    """One physical producer or formation and its canonical outputs."""

    course_name: str
    source_id: str
    label: str
    outputs: tuple[CoinOutputDefinition, ...]
    maximum_coin_value: int


COURSE_ORDER = tuple(SOURCE_LAYOUTS)
_COURSE_INDEX = {course_name: index for index, course_name in enumerate(COURSE_ORDER)}

COURSE_MAXIMUM_COIN_VALUES = {
    "Bob-omb Battlefield": 146, "Whomp's Fortress": 141, "Jolly Roger Bay": 104,
    "Cool, Cool Mountain": 154, "Big Boo's Haunt": 151, "Hazy Maze Cave": 139,
    "Lethal Lava Land": 133, "Shifting Sand Land": 136, "Dire, Dire Docks": 106,
    "Snowman's Land": 127, "Wet-Dry World": 152, "Tall, Tall Mountain": 137,
    "Tiny-Huge Island": 193, "Tick Tock Clock": 128, "Rainbow Ride": 146,
    "The Princess's Secret Slide": 80, "The Secret Aquarium": 56,
    "Wing Mario Over the Rainbow": 56, "Tower of the Wing Cap": 63,
    "Vanish Cap Under the Moat": 27, "Cavern of the Metal Cap": 47,
    "Bowser in the Dark World": 80, "Bowser in the Fire Sea": 80, "Bowser in the Sky": 76,
    "Castle": 15,
}


# Coin outputs in independently shuffled sub-areas belong to the physical
# region containing their source. Course-wide count checks remain course-wide
# because permanent coin totals span every area in a course.
COIN_SOURCE_METHOD_REGION_NAMES: Mapping[str, str] = {
    "lower_red_coin_room_coins": "Hazy Maze Cave - Mid Red Coin Room",
    "red_coin_room_mr_is": "Hazy Maze Cave - Mid Red Coin Room",
    "upper_red_coin_pair_first": "Hazy Maze Cave - Upper Red Coin Room",
    "upper_red_coin_pair_checkerboards": "Hazy Maze Cave - Upper Red Coin Room",
    "upper_red_coin_swoops": "Hazy Maze Cave - Upper Red Coin Room",
    "toxic_maze_star_coin_line": "Hazy Maze Cave - Pit Islands",

    "penguin_slide_yellow_coins": "Cool, Cool Mountain - Secret Slide",
    "penguin_slide_coin_lines": "Cool, Cool Mountain - Secret Slide",
    "slide_blue_coin": "Cool, Cool Mountain - Secret Slide",

    "lll_volcano_s_island_coins": "Lethal Lava Land - Volcano",
    "lll_volcano_first_ridge_coin_line": "Lethal Lava Land - Volcano",
    "lll_volcano_second_ridge_coins": "Lethal Lava Land - Volcano",
    "lll_volcano_floating_platform_coins": "Lethal Lava Land - Volcano",
    "lll_volcano_post_platform_coin": "Lethal Lava Land - Volcano",
    "lll_volcano_second_bully_coin_line": "Lethal Lava Land - Volcano",
    "lll_volcano_checkerboard_lift_coin": "Lethal Lava Land - Volcano",
    "lll_volcano_bullies": "Lethal Lava Land - Volcano",
    "lll_elevator_tour_platform_coins": "Lethal Lava Land - Elevator Tour",

    "ssl_throwable_cork_box": "Shifting Sand Land",
    "ssl_pillar_coins": "Shifting Sand Land",
    "ssl_quicksand_pillar_coin": "Shifting Sand Land",
    "ssl_behind_pyramid_coin_line": "Shifting Sand Land",
    "ssl_pyramid_side_coin_line": "Shifting Sand Land",
    "ssl_fly_guys": "Shifting Sand Land",
    "ssl_crazy_boxes": "Shifting Sand Land",
    "ssl_bob_ombs": "Shifting Sand Land",
    "ssl_pokeys": "Shifting Sand Land",
    "ssl_outside_goombas": "Shifting Sand Land",
    "ssl_low_red_coins": "Shifting Sand Land",
    "ssl_high_red_coins": "Shifting Sand Land",
    "ssl_inside_pyramid_coins": "Shifting Sand Land - Pyramid",
    "ssl_pyramid_goombas": "Shifting Sand Land - Pyramid",
    "ssl_first_wire_grid_coin_ring": "Shifting Sand Land - Pyramid",
    "ssl_blue_coin_block": "Shifting Sand Land - Pyramid",
    "ssl_second_wire_grid_coin_line": "Shifting Sand Land - Upper Pyramid",
    "ssl_pyramid_top_horizontal_coin_line": "Shifting Sand Land - Upper Pyramid",
    "ssl_pyramid_top_vertical_coin_line": "Shifting Sand Land - Upper Pyramid",
    "ssl_pyramid_top_vertical_coin_line_top_coin": "Shifting Sand Land - Upper Pyramid",
    "ssl_upper_pyramid_single_coins": "Shifting Sand Land - Upper Pyramid",

    "sl_igloo_frozen_coin_lines": "Snowman's Land - Igloo",
    "sl_igloo_single_coins": "Snowman's Land - Igloo",
    "sl_igloo_three_coin_block": "Snowman's Land - Igloo",
    "sl_igloo_goombas": "Snowman's Land - Igloo",
    "sl_igloo_spindrifts": "Snowman's Land - Igloo",
    "sl_upper_slope_coin_line": "Snowman's Land - Igloo Entrance",
    "sl_highest_slope_single_coin": "Snowman's Land - Igloo Entrance",

    "ttm_hidden_coin_before_slide": "Tall, Tall Mountain - Secret Slide",
    "ttm_slide_single_coins": "Tall, Tall Mountain - Secret Slide",
    "ttm_slide_coin_lines": "Tall, Tall Mountain - Secret Slide",
    "ttm_slide_blue_coins": "Tall, Tall Mountain - Secret Slide",

    "red_area_red_coins": "Tiny-Huge Island - Red Coin Cave",
    "red_area_wall_kick_red_coin": "Tiny-Huge Island - Red Coin Cave",
    "red_area_blue_coins": "Tiny-Huge Island - Red Coin Cave",
    "red_area_giant_goombas_yellow": "Tiny-Huge Island - Red Coins Area",
    "red_area_giant_goombas_blue": "Tiny-Huge Island - Red Coins Area",
    "red_area_plank_line": "Tiny-Huge Island - Red Coins Area",
    "wiggler_cave_coin_lines": "Tiny-Huge Island - Wiggler's Cave",
}


def coin_output_region_name(output: CoinOutputDefinition) -> str | None:
    """Return the physical region for an output in an independently shuffled sub-area."""
    regions = {
        COIN_SOURCE_METHOD_REGION_NAMES[method]
        for method in output.source_methods
        if method in COIN_SOURCE_METHOD_REGION_NAMES
    }
    if len(regions) > 1:
        raise ValueError(f"Coin output {output.output_id} maps to multiple physical regions: {regions}")
    return next(iter(regions), None)


COIN_OUTPUT_SOURCE_METHOD_OVERRIDES: Mapping[tuple[str, str, int], tuple[str, ...]] = {
    ("Tall, Tall Mountain", "ttm_upper_leaf_coin_line", 1):
        ("ttm_upper_leaf_first_coin",),
    **{
        ("Shifting Sand Land", "ssl_goombas", index):
            (("ssl_pyramid_goombas",) if index <= 9 else ("ssl_outside_goombas",))
        for index in range(1, 13)
    },
    **{
        ("Shifting Sand Land", "ssl_pillar_and_pyramid_coins", index):
            (("ssl_inside_pyramid_coins",) if index <= 2 else
             ("ssl_quicksand_pillar_coin",) if index == 6 else ("ssl_pillar_coins",))
        for index in range(1, 7)
    },
    (
        "Shifting Sand Land",
        "ssl_pyramid_top_vertical_coin_line",
        5,
    ): ("ssl_pyramid_top_vertical_coin_line_top_coin",),
    (
        "Snowman's Land",
        "sl_upper_slope_single_coins",
        3,
    ): ("sl_highest_slope_single_coin",),
    **{
        ("Bowser in the Dark World", "bitdw_single_coins_before_slope", index):
            ("bitdw_slope_single_coins",)
        for index in (6, 7, 16)
    },
    **{
        ("Bowser in the Dark World", "bitdw_slope_single_coins", index):
            ("bitdw_single_coins_before_slope",)
        for index in range(1, 4)
    },
}


COIN_OUTPUT_NAME_OVERRIDES: Mapping[tuple[str, str, int], str] = {
    **{
        ("Bob-omb Battlefield", "main_wooden_posts", index):
            f"Chain Chomp's Wooden Post Coin {index}"
        for index in range(1, 6)
    },
    **{
        ("Bob-omb Battlefield", "main_wooden_posts", index):
            f"Wooden Post {(index - 6) // 5 + 1} Coin {(index - 6) % 5 + 1}"
        for index in range(6, 26)
    },
    **{
        ("Cool, Cool Mountain", "main_spindrifts", index):
            f"Snowman Head Spindrift Coin {index}"
        for index in range(1, 4)
    },
    **{
        ("Cool, Cool Mountain", "main_spindrifts", index):
            f"Snowman Body Spindrift Coin {index - 3}"
        for index in range(4, 7)
    },
    **{
        ("Cool, Cool Mountain", "main_mountain_coin_lines", index):
            f"Snowman Slide Coin Line {(index - 1) // 5 + 1} Coin {(index - 1) % 5 + 1}"
        for index in range(1, 21)
    },
    **{
        ("Tall, Tall Mountain", "ttm_upper_leaf_coin_line", index):
            f"Upper Vine Wall Hangable Ceiling Coin Line Coin {index}"
        for index in range(1, 6)
    },
    **{
        ("Tall, Tall Mountain", "ttm_middle_bridge_coin_line", index):
            f"Bob-omb Buddy Bridge Coin {index}"
        for index in range(1, 6)
    },
    **{
        ("Tall, Tall Mountain", "ttm_middle_chuckya", index):
            f"Chuckya Coin {index}"
        for index in range(1, 6)
    },
    **{
        ("Tall, Tall Mountain", "ttm_middle_bob_ombs", index):
            f"Past Vine Wall Bob-omb {index} Coin"
        for index in range(1, 4)
    },
    **{
        ("Cool, Cool Mountain", "penguin_slide_yellow_coins", old_index):
            f"Penguin Slide Coin {new_index}"
        for new_index, old_index in enumerate(
            (6, 7, 12, 1, 2, 3, 4, 5, 22, 23, 24, 25, 26, 27,
             9, 8, 10, 11, 13, 14, 15, 16, 17, 18, 19, 20, 21),
            1,
        )
    },
    **{
        ("Cool, Cool Mountain", "penguin_slide_coin_lines", old_line * 5 + old_coin):
            f"Penguin Slide Coin Line {new_line} Coin {new_coin}"
        for new_line, old_line, reverse_coins in (
            (1, 8, True),
            (2, 0, False),
            (3, 1, False),
            (4, 2, False),
            (5, 3, False),
            (6, 4, False),
            (7, 5, True),
            (8, 6, True),
            (9, 7, True),
        )
        for old_coin in range(1, 6)
        for new_coin in (6 - old_coin if reverse_coins else old_coin,)
    },
    ("Cool, Cool Mountain", "slide_blue_coin", 1): "Penguin Slide Blue Coin",
    **{
        ("Bowser in the Sky", "bits_whomp_platform_lines", index):
            f"Coin Line Beneath the Whomp Coin {index}"
        for index in range(1, 6)
    },
    **{
        ("Bowser in the Sky", "bits_whomp_platform_lines", index):
            f"Coin Line Beneath the Tilting Platform Coin {index - 5}"
        for index in range(6, 11)
    },
    **{
        ("Tall, Tall Mountain", "ttm_slide_single_coins", old_index):
            f"Coin on the Slide {new_index}"
        for new_index, old_index in enumerate(
            (1, 10, 11, 12, 25, 13, 15, 16, 17, 14, 26, 18, 19,
             20, 21, 23, 22, 24, 5, 6, 7, 2, 3, 4, 8, 9),
            1,
        )
    },
    **{
        ("Tall, Tall Mountain", "ttm_slide_coin_lines", index):
            f"Coin Line on the Slide {(index - 1) // 5 + 1} Coin "
            f"{6 - ((index - 1) % 5 + 1) if (index - 1) // 5 + 1 in (1, 2, 4) else (index - 1) % 5 + 1}"
        for index in range(1, 21)
    },
    **{
        ("Tall, Tall Mountain", "ttm_slide_blue_coins", old_index):
            f"Slide Blue Coin {new_index}"
        for old_index, new_index in ((1, 3), (2, 2), (3, 1))
    },
    **{
        ("Wet-Dry World", "amp_ring", index): f"Pedestal Coin Ring Coin {index}"
        for index in range(1, 9)
    },
    **{
        ("Wet-Dry World", "fourth_diamond_coin_line", index):
            f"Second Highest Water Level Diamond Coin Line Coin {index}"
        for index in range(1, 6)
    },
    ("Bowser in the Fire Sea", "bitfs_start_single_coins", 1): "First Lava Platforms Coin 2",
    ("Bowser in the Fire Sea", "bitfs_start_single_coins", 2): "First Lava Platforms Coin 1",
    **{
        ("Bowser in the Fire Sea", "bitfs_second_sinking_platform_line", index):
            f"Sinking Platform Coin {index}"
        for index in range(1, 6)
    },
    **{
        ("Bowser in the Fire Sea", "bitfs_wire_grid_ring", index):
            f"Wire Platform Coin Ring Coin {index}"
        for index in range(1, 9)
    },
    **{
        ("Bowser in the Dark World", "bitdw_coin_lines", index):
            f"Coin Line 2 Coin {index}"
        for index in range(1, 6)
    },
    **{
        ("Bowser in the Dark World", "bitdw_coin_lines", index):
            f"Coin Line 1 Coin {index - 5}"
        for index in range(6, 11)
    },
    **{
        ("Bowser in the Dark World", "bitdw_coin_rings", index):
            f"Moving Platforms Coin Ring Coin {index - 8}"
        for index in range(9, 17)
    },
    **{
        ("Bowser in the Dark World", "bitdw_coin_rings", index):
            f"Spike Platform Coin Ring Coin {index - 16}"
        for index in range(17, 25)
    },
    **{
        ("Bowser in the Dark World", "bitdw_goombas", index): f"Goomba {display_index} Coin"
        for index, display_index in enumerate((5, 4, 3, 1, 2, 6), 1)
    },
    **{
        ("Bowser in the Dark World", "bitdw_single_coins_before_slope", index): name
        for index, name in {
            1: "Tilting Platforms Coin 3",
            2: "Tilting Platforms Coin 1",
            3: "Tilting Platforms Coin 6",
            4: "Tilting Platforms Coin 4",
            5: "Bottom of the Slope Coin 2",
            6: "Upper Slope Coin 3",
            7: "Upper Slope Coin 2",
            8: "Above Tilting Platforms Coin 1",
            9: "Above Tilting Platforms Coin 2",
            10: "Spike Platform Coin 1",
            11: "Spike Platform Coin 2",
            12: "Spike Platform Coin 3",
            13: "Spike Platform Coin 4",
            14: "Ferris Wheel Coin",
            15: "Bottom of the Slope Coin 1",
            16: "Upper Slope Coin 1",
            17: "Tilting Platforms Coin 2",
            18: "Tilting Platforms Coin 5",
        }.items()
    },
    **{
        ("Bowser in the Dark World", "bitdw_slope_single_coins", index):
            f"Moving Platform Coin {index}"
        for index in range(1, 4)
    },
    **{
        ("Bob-omb Battlefield", "flowerbed_coin_ring", index): f"Flowerbed Coin Ring Coin {index}"
        for index in range(1, 9)
    },
    **{
        ("Bob-omb Battlefield", "main_horizontal_coin_lines", index):
            f"Bubble Cannon Coin Line Coin {index - 5}"
        for index in range(6, 11)
    },
    ("Bob-omb Battlefield", "main_bob_ombs", 1): "Switch Tunnel Bob-omb Coin",
    ("Bob-omb Battlefield", "main_bob_ombs", 12): "Bubble Cannon Bob-omb Coin",
    **{
        ("Castle", "castle_courtyard_boos", index): f"Courtyard Boo {index} Coin"
        for index in range(1, 10)
    },
    **{
        ("Dire, Dire Docks", "ddd_sub_area_coin_rings", index):
            f"Coin Ring Leading to the Tunnel 2 Coin {index}"
        for index in range(1, 9)
    },
    **{
        ("Dire, Dire Docks", "ddd_sub_area_coin_rings", index):
            f"Tunnel Coin Ring Coin {index - 8}"
        for index in range(9, 17)
    },
    **{
        ("Dire, Dire Docks", "ddd_sub_area_coin_rings", index):
            f"Coin Ring Leading to the Tunnel 1 Coin {index - 16}"
        for index in range(17, 25)
    },
    **{
        ("Dire, Dire Docks", "ddd_chest_and_current_coin_lines", index):
            f"Vertical Coin Line by the Whirlpool Coin {index}"
        for index in range(1, 6)
    },
    **{
        ("Dire, Dire Docks", "ddd_chest_and_current_coin_lines", index):
            f"Vertical Coin Line by the Chest Coin {index - 5}"
        for index in range(6, 11)
    },
    **{
        ("Whomp's Fortress", "whomp_jump_coins", index):
            f"Whomp {((index - 1) // 5) + 1}, Coin {((index - 1) % 5) + 1}"
        for index in range(1, 11)
    },
    **{
        ("Whomp's Fortress", "whomp_ground_pound_coins", index):
            f"Whomp {((index - 1) // 5) + 1}, Coin {((index - 1) % 5) + 6}"
        for index in range(1, 11)
    },
    **{
        ("Whomp's Fortress", "start_throwable_cork_boxes", index): f"Grass Cork Box Coin {index}"
        for index in range(1, 4)
    },
    **{
        ("Whomp's Fortress", "start_throwable_cork_boxes", index):
            f"Below Shoot into the Wild Blue Cork Box Coin {index - 3}"
        for index in range(4, 7)
    },
    **{
        ("Whomp's Fortress", "start_coin_line", index): f"Dirt Ramp Coin Line Coin {index}"
        for index in range(1, 6)
    },
    **{
        ("Whomp's Fortress", "falling_bridge_coin_line", index): f"Cannon Coin Line Coin {index}"
        for index in range(1, 6)
    },
    **{
        ("Whomp's Fortress", "water_slope_coin_line", index): f"Narrow Plank Coin Line Coin {index}"
        for index in range(1, 6)
    },
    **{
        ("Whomp's Fortress", "buddy_coin_line", index): f"Stone Ramp Coin Line Coin {index}"
        for index in range(1, 6)
    },
    ("Whomp's Fortress", "piranha_plant_coins", 1): "Staircase Piranha Plant Blue Coin",
    ("Whomp's Fortress", "piranha_plant_coins", 2): "Flower Patch Piranha Plant Blue Coin",
    ("Whomp's Fortress", "piranha_plant_coins", 3): "Rotating Plank Piranha Plant Blue Coin",
    **{
        ("Whomp's Fortress", "top_floating_arrow", index): f"Coin Arrow Coin {index}"
        for index in range(1, 9)
    },
    **{
        ("Whomp's Fortress", "top_floating_isle_ring", index): f"Floating Isle Coin Ring Coin {index}"
        for index in range(1, 9)
    },
    **{
        ("Big Boo's Haunt", "outside_scuttlebugs", index):
            f"Scuttlebug Behind the Mansion 1, Coin {index}"
        for index in range(1, 4)
    },
    **{
        ("Big Boo's Haunt", "outside_scuttlebugs", index):
            f"Scuttlebug Behind the Mansion 2, Coin {index - 3}"
        for index in range(4, 7)
    },
    **{
        ("Big Boo's Haunt", "outside_scuttlebugs", index):
            f"Starting Area Scuttlebug, Coin {index - 6}"
        for index in range(7, 10)
    },
    ("Big Boo's Haunt", "main_boos", 3): "Back Entrance Room Boo 1 Blue Coin",
    ("Big Boo's Haunt", "main_boos", 5): "Back Entrance Room Boo 2 Blue Coin",
    ("Big Boo's Haunt", "main_boos", 1): "First Floor Boo 1 Blue Coin",
    ("Big Boo's Haunt", "main_boos", 2): "First Floor Boo 2 Blue Coin",
    ("Big Boo's Haunt", "main_boos", 4): "First Floor Boo 3 Blue Coin",
    ("Big Boo's Haunt", "main_mr_is", 1): "First Floor Mr. I Blue Coin",
    ("Big Boo's Haunt", "main_mr_is", 2): "Shed Mr. I Blue Coin",
    ("Big Boo's Haunt", "main_bookend", 1): "First Floor Flying Bookend Blue Coin",
    ("Lethal Lava Land", "lll_outside_bullies", 1): "Bully the Bullies Bully 1 Coin",
    ("Lethal Lava Land", "lll_outside_bullies", 2): "Bully the Bullies Bully 3 Coin",
    ("Lethal Lava Land", "lll_outside_bullies", 3): "Bully the Bullies Bully 2 Coin",
    ("Lethal Lava Land", "lll_outside_bullies", 4): "After Bowser Puzzle Bully 2 Coin",
    ("Lethal Lava Land", "lll_outside_bullies", 5): "First Bully Coin",
    ("Lethal Lava Land", "lll_outside_bullies", 6): "Beige Platform Bully 2 Coin",
    ("Lethal Lava Land", "lll_outside_bullies", 7): "Beige Platform Bully 1 Coin",
    ("Lethal Lava Land", "lll_outside_bullies", 8): "After Bowser Puzzle Bully 1 Coin",
    ("Lethal Lava Land", "lll_mr_is", 1): "Grate Platform Mr. I Blue Coin",
    ("Lethal Lava Land", "lll_mr_is", 2): "Island Mr. I Blue Coin",
    ("Shifting Sand Land", "ssl_pillar_and_pyramid_coins", 1): "Inside Pyramid Coin 1",
    ("Shifting Sand Land", "ssl_pillar_and_pyramid_coins", 2): "Inside Pyramid Coin 2",
    **{
        ("Shifting Sand Land", "ssl_pillar_and_pyramid_coins", index): f"Pillar Coin {index - 2}"
        for index in range(3, 7)
    },
    ("Shifting Sand Land", "ssl_pillar_and_pyramid_coins", 6): "Quicksand Pillar Coin",
    **{
        ("Shifting Sand Land", "ssl_upper_pyramid_single_coins", old_index):
            f"Pyramid Moving-Step Coin {new_index}"
        for new_index, old_index in enumerate((12, 13, 10, 11), 1)
    },
    **{
        ("Shifting Sand Land", "ssl_upper_pyramid_single_coins", old_index):
            f"Pyramid Puzzle Coin {new_index}"
        for new_index, old_index in enumerate((4, 3, 5, 1, 2), 1)
    },
    **{
        ("Shifting Sand Land", "ssl_upper_pyramid_single_coins", old_index):
            f"Pyramid Steps to the Spindel Coin {new_index}"
        for new_index, old_index in enumerate((9, 7, 6, 8), 1)
    },
    **{
        ("Wet-Dry World", source_id, index): f"{block_name} Coin {index}"
        for source_id, block_name, count in (
            ("pillar_ten_coin_block", "Pedestal 10-Coin Block", 10),
            ("push_block_three_coin_block", "Push Block 3-Coin Block", 3),
            ("low_ten_coin_block", "Push Block 10-Coin Block", 10),
            ("wooden_structure_three_coin_block", "Wooden Structure 3-Coin Block", 3),
            ("express_elevator_ten_coin_block", "Top of Express Elevator 10-Coin Block", 10),
        )
        for index in range(1, count + 1)
    },
}


# Each tuple identifies alternate CoinLogic methods for the same physical Red Coin.
RED_COIN_SOURCE_METHODS: Mapping[str, Mapping[int, tuple[str, ...]]] = {
    "Bob-omb Battlefield": {
        **{i: ("main_red_coins",) for i in range(1, 8)},
        8: ("island_full_trick_red_coin", "island_cannon_red_coin", "island_partial_red_coin"),
    },
    "Whomp's Fortress": {
        **{i: ("initial_red_coins",) for i in range(1, 6)}, 6: ("thwomp_red_coin",),
        7: ("top_red_coins",), 8: ("top_red_coins",),
    },
    "Jolly Roger Bay": {
        **{i: ("lower_red_coins",) for i in range(1, 5)}, 5: ("pillar_red_coin",),
        6: ("raised_ship_red_coins", "ship_alternative_red_coin"),
        7: ("raised_ship_red_coins",), 8: ("raised_ship_red_coins",),
    },
    "Cool, Cool Mountain": {i: ("red_coins",) for i in range(1, 9)},
    "Big Boo's Haunt": {
        1: ("first_floor_red_coins",),
        2: ("first_floor_red_coins",),
        3: ("first_floor_movement_red_coin",),
        4: ("first_floor_red_coins",),
        **{i: ("second_floor_red_coins",) for i in range(5, 8)},
        8: ("second_floor_movement_red_coin",),
    },
    "Hazy Maze Cave": {
        **{i: ("lower_red_coin_room_coins",) for i in range(1, 5)},
        5: ("upper_red_coin_pair_first",), 6: ("upper_red_coin_pair_first",),
        7: ("upper_red_coin_pair_checkerboards",), 8: ("upper_red_coin_pair_checkerboards",),
    },
    "Lethal Lava Land": {
        **{i: ("lll_first_five_red_coins",) for i in range(1, 6)},
        **{i: ("lll_remaining_three_red_coins",) for i in range(6, 9)},
    },
    "Shifting Sand Land": {
        **{i: ("ssl_low_red_coins",) for i in range(1, 5)},
        5: ("ssl_normal_high_red_coin_route", "ssl_tweester_red_coin_route"),
        6: ("ssl_normal_high_red_coin_route", "ssl_tweester_red_coin_route"),
        7: ("ssl_normal_high_red_coin_route", "ssl_tweester_red_coin_route"),
        8: ("ssl_normal_high_red_coin_route", "ssl_shy_guy_red_coin_route"),
    },
    "Dire, Dire Docks": {1: ("ddd_first_red_coin",), **{i: ("ddd_remaining_red_coins",) for i in range(2, 9)}},
    "Snowman's Land": {
        1: ("sl_start_red_coins",),
        2: ("sl_whirl_red_coins",),
        3: ("sl_whirl_red_coins",),
        4: ("sl_whirl_red_coins",),
        5: ("sl_whirl_red_coins",),
        6: ("sl_start_red_coins",),
        7: ("sl_whirl_red_coins",),
        8: ("sl_whirl_red_coins",),
    },
    "Wet-Dry World": {
        1: ("downtown_diamond_red_coins",),
        2: ("downtown_brown_brick_red_coin",),
        3: ("downtown_diamond_red_coins",),
        4: ("downtown_beige_building_red_coin",),
        5: ("downtown_diamond_red_coins",),
        6: ("downtown_diamond_red_coins",),
        7: ("downtown_diamond_red_coins",),
        8: ("downtown_chapel_roof_red_coin",),
    },
    "Tall, Tall Mountain": {
        **{i: ("ttm_middle_red_coins",) for i in range(1, 7)},
        7: ("ttm_upper_red_coins",), 8: ("ttm_upper_red_coins",),
    },
    "Tiny-Huge Island": {
        **{i: ("red_area_red_coins",) for i in range(1, 8)}, 8: ("red_area_wall_kick_red_coin",),
    },
    "Tick Tock Clock": {
        **{i: ("ttc_lower_red_coins",) for i in range(1, 6)},
        **{i: ("ttc_spinner_red_coins",) for i in range(6, 9)},
    },
    "Rainbow Ride": {1: ("rr_maze_movement_red_coin",), **{i: ("rr_other_red_coins",) for i in range(2, 9)}},
    "The Secret Aquarium": {i: ("sa_red_coins",) for i in range(1, 9)},
    "Tower of the Wing Cap": {i: ("totwc_red_coins",) for i in range(1, 9)},
    "Vanish Cap Under the Moat": {
        **{i: ("vcutm_earlier_red_coins",) for i in range(1, 5)},
        **{i: ("vcutm_checkerboard_red_coins",) for i in range(5, 9)},
    },
    "Cavern of the Metal Cap": {
        **{i: ("cotmc_initial_red_coins",) for i in range(1, 5)},
        **{i: ("cotmc_deep_red_coins",) for i in range(5, 9)},
    },
    "Wing Mario Over the Rainbow": {
        # Macro order does not follow the flight route or physical elevation.
        1: ("wmotr_cannon_red_coins",),
        2: ("wmotr_cannon_red_coins",),
        3: ("wmotr_cannon_red_coins",),
        4: ("wmotr_flight_red_coins",),
        5: ("wmotr_flight_red_coins", "wmotr_long_jump_second_red_coin"),
        6: ("wmotr_flight_red_coins", "wmotr_long_jump_first_red_coin", "wmotr_wing_cap_fallback_red_coin"),
        7: ("wmotr_initial_red_coin",),
        8: ("wmotr_cannon_red_coins",),
    },
    "Bowser in the Dark World": {
        1: ("bitdw_purple_switch_red_coins",),
        **{i: ("bitdw_other_red_coins",) for i in range(2, 7)},
        7: ("bitdw_purple_switch_red_coins",),
        8: ("bitdw_other_red_coins",),
    },
    "Bowser in the Fire Sea": {
        1: ("bitfs_upper_red_coins",),
        2: ("bitfs_start_red_coins",),
        3: ("bitfs_second_red_coin",),
        **{i: ("bitfs_upper_red_coins",) for i in range(4, 9)},
    },
    "Bowser in the Sky": {
        **{i: ("bits_start_red_coins",) for i in range(1, 4)},
        **{i: ("bits_arrow_ride_red_coins",) for i in range(4, 7)},
        7: ("bits_top_red_coins",), 8: ("bits_top_red_coins",),
    },
}


def _repeat_names(base: str, count: int) -> tuple[str, ...]:
    return tuple(base if count == 1 else f"{base} {index}" for index in range(1, count + 1))


RED_COIN_NAMES: Mapping[str, tuple[str, ...]] = {
    "Bob-omb Battlefield": (
        "Wooden Posts Red Coin 1",
        "Wooden Posts Red Coin 2",
        "Grass Ramp Red Coin",
        "Chain Chomp Red Coin",
        "Checkerboard Platform Red Coin",
        "Switch Tunnel Red Coin",
        "Below the Island Red Coin",
        "Island Red Coin",
    ),
    "Whomp's Fortress": (
        "Rotating Plank Red Coin",
        "Narrow Ledge Red Coin",
        "Piranha Plant Red Coin",
        "Bomp Red Coin",
        "Slide Beneath Rotating Plank Red Coin",
        "Thwomp Red Coin",
        "Floating Isle Red Coin 1",
        "Floating Isle Red Coin 2",
    ),
    "Jolly Roger Bay": (*_repeat_names("Initially Reachable Red Coin", 4), "Red Coin on the Stone Pillar", *_repeat_names("Red Coin on the Raised Ship", 3)),
    "Cool, Cool Mountain": (
        "First Tree Red Coin",
        "Bottom of Snowman Slide Red Coin",
        "Bridge Out Red Coin",
        "Ice Pillar Red Coin",
        "Top of Buddy Lift Red Coin",
        "Bottom Bridge Island Red Coin",
        "Bottom Tree Red Coin",
        "Bottom Corner Red Coin",
    ),
    "Big Boo's Haunt": (
        "Mad Piano Red Coin",
        "Bookshelf Red Coin 1",
        "Bookshelf Red Coin 2",
        "Hole Room Red Coin",
        *_repeat_names("Second Floor Red Coin", 4),
    ),
    "Hazy Maze Cave": (
        *_repeat_names("Lower Red Coin", 4),
        *_repeat_names("Checkerboard Platform Arrival Platform Red Coin", 2),
        *_repeat_names("Checkerboard Platform Ride Red Coin", 2),
    ),
    "Lethal Lava Land": _repeat_names("Bowser Puzzle Red Coin", 8),
    "Shifting Sand Land": (*_repeat_names("Low Red Coin", 4), *_repeat_names("High Red Coin", 4)),
    "Dire, Dire Docks": ("First Red Coin", *_repeat_names("Pole Red Coin", 7)),
    "Snowman's Land": (
        "Starting Area Red Coin 2",
        "Under the Bully Red Coin 2",
        "Whirl from the Freezing Pond Red Coin 4",
        "Whirl from the Freezing Pond Red Coin 3",
        "Whirl from the Freezing Pond Red Coin 2",
        "Starting Area Red Coin 1",
        "Whirl from the Freezing Pond Red Coin 1",
        "Under the Bully Red Coin 1",
    ),
    "Wet-Dry World": (
        "Gray Building with Orange Roof Red Coin",
        "Brown Brick Building Red Coin",
        "Gray Building Red Coin",
        "Beige Building Red Coin",
        "Statue Wall Red Coin 2",
        "Statue Wall Red Coin 1",
        "Chapel Alcove Red Coin",
        "Chapel Roof Red Coin",
    ),
    "Tall, Tall Mountain": (
        "Scary Shrooms Red Coin 4",
        "Scary Shrooms Red Coin 2",
        "Scary Shrooms Red Coin 1",
        "Vine Wall Lower Red Coin 1",
        "Vine Wall Lower Red Coin 2",
        "Scary Shrooms Red Coin 3",
        *_repeat_names("Upper Area Red Coin", 2),
    ),
    "Tiny-Huge Island": _repeat_names("Red Coin", 8),
    "Tick Tock Clock": _repeat_names("Red Coin", 8),
    "Rainbow Ride": ("Red Coin Requiring Maze Movement", *_repeat_names("Other Maze Red Coin", 7)),
    "The Secret Aquarium": _repeat_names("Aquarium Red Coin", 8),
    "Tower of the Wing Cap": _repeat_names("Tower Red Coin", 8),
    "Vanish Cap Under the Moat": (
        *_repeat_names("Slide Red Coin", 4),
        *_repeat_names("Tilting Platform Red Coin", 2),
        "Checkerboard Platform Red Coin",
        "Cap Switch Red Coin",
    ),
    "Cavern of the Metal Cap": (*_repeat_names("Initial Red Coin", 4), *_repeat_names("Deep-Water Red Coin", 4)),
    "Wing Mario Over the Rainbow": (
        "Cannon Region Red Coin 1",
        "Cannon Region Red Coin 2",
        "Cannon Region Red Coin 3",
        "Flight Path Red Coin 1",
        "Flight Path Red Coin 2",
        "Flight Path Red Coin 3",
        "Initial Red Coin",
        "Cannon Region Red Coin 4",
    ),
    "Bowser in the Dark World": (
        "Purple Switch Red Coin 2",
        "Moving Yellow Bar Red Coin",
        "Moving Platforms Red Coin",
        "Spike Platform Red Coin",
        "Above Tilting Platforms Red Coin",
        "Crystal Path Red Coin",
        "Purple Switch Red Coin 1",
        "Near Tilting Platforms Red Coin",
    ),
    "Bowser in the Fire Sea": (
        "Below the Lift Red Coin",
        "Wire Platform Red Coin",
        "Seesaw Platform Red Coin",
        "Upper Course Red Coin 2",
        "Upper Course Red Coin 3",
        "Upper Course Red Coin 4",
        "Upper Course Red Coin 5",
        "Lift Cage Corner Red Coin",
    ),
    "Bowser in the Sky": (
        "Piranha Plant Red Coin",
        "Push Block Red Coin",
        "Beneath the Tilting Platform Hidden Red Coin",
        *_repeat_names("Arrow Ride Red Coin", 3),
        *_repeat_names("Top Red Coin", 2),
    ),
}


def _output_names(label: str, kind: CoinOutputKind, count: int) -> tuple[str, ...]:
    source_name = _title_source_label(label)
    coin_name = "Blue Coin" if kind is CoinOutputKind.BLUE else "Coin"
    group_size = _formation_group_size(source_name, count)
    group_count = count // group_size
    source_name = _singularize_source_name(source_name, group_count > 1)
    names = []
    for group_index in range(1, group_count + 1):
        source = f"{source_name} {group_index}" if group_count > 1 else source_name
        for coin_index in range(1, group_size + 1):
            names.append(f"{source}, {coin_name} {coin_index}" if group_size > 1 else f"{source}, {coin_name}")
    return tuple(names)


def _formation_group_size(source_name: str, count: int) -> int:
    lower_name = source_name.lower()
    if "coin ring" in lower_name or "rings of eight coins" in lower_name:
        return 8 if count % 8 == 0 else count
    if "coin line" in lower_name or "lines of five coins" in lower_name:
        return 5 if count % 5 == 0 else count
    if any(term in lower_name for term in ("breakable coin box", "throwable cork box")):
        return 3 if count % 3 == 0 else count
    if "crazy box" in lower_name:
        return 5 if count % 5 == 0 else count
    if "wooden post" in lower_name:
        return 5 if count % 5 == 0 else count
    if "3-coin block" in lower_name:
        return 3 if count % 3 == 0 else count
    if "10-coin block" in lower_name:
        return 10 if count % 10 == 0 else count
    return count


def _singularize_source_name(source_name: str, numbered: bool) -> str:
    source_name = re.sub(r"^(Two|Three|Four|Five|Nine) ", "", source_name)
    source_name = re.sub(r"^Rings of Eight Coins$", "Coin Ring", source_name)
    source_name = re.sub(r"^Lines of Five Coins$", "Coin Line", source_name)
    if numbered:
        source_name = re.sub(r"\bCoin Rings\b", "Coin Ring", source_name)
        source_name = re.sub(r"\bCoin Lines\b", "Coin Line", source_name)
        source_name = re.sub(r"\bBreakable Coin Boxes\b", "Breakable Coin Box", source_name)
        source_name = re.sub(r"\bThrowable Cork Boxes\b", "Throwable Cork Box", source_name)
        source_name = re.sub(r"\bCrazy Boxes\b", "Crazy Box", source_name)
        source_name = re.sub(r"\bWooden Posts\b", "Wooden Post", source_name)
        source_name = re.sub(r"\b3-Coin Blocks\b", "3-Coin Block", source_name)
        source_name = re.sub(r"\b10-Coin Blocks\b", "10-Coin Block", source_name)
    return source_name


def _title_source_label(label: str) -> str:
    label = label.replace("second-building", "second building").replace("first-building", "first building") \
        .replace("metal-cap", "metal cap")
    label = re.sub(r"\bLine of coins\b", "Coin line", label, flags=re.IGNORECASE)
    label = re.sub(r"\bLines of coins\b", "Coin lines", label, flags=re.IGNORECASE)
    label = re.sub(r"\bHorizontal (?=Coin (?:Line|Ring)s?\b)", "", label, flags=re.IGNORECASE)
    titled = label.title()
    titled = re.sub(
        r"(?<!^)\b(A|An|And|Or|The|Of|In|On|At|To|From|By|Near|After|Before|Around|Above|Below|"
        r"Behind|Beside|Under|With|Without|Past|Into|Toward|Through)\b",
        lambda match: match.group(0).lower(),
        titled,
    )
    replacements = {
        "Bob-Omb": "Bob-omb", "Bob-Ombs": "Bob-ombs", "Whomp'S": "Whomp's",
        "Bowser'S": "Bowser's", "Wiggler'S": "Wiggler's", "Koopa the Quick'S": "Koopa the Quick's",
        "Lakitu'S": "Lakitu's", "Snowman'S": "Snowman's",
        "Mr. Is": "Mr. Is", "Mr. I": "Mr. I", "10-Coin": "10-Coin", "3-Coin": "3-Coin",
        "S-Shaped": "S-Shaped", "Red Coin": "Red Coin", "Purple Switch": "Purple Switch",
        "Vanish Cap": "Vanish Cap", "Wall Kicks Will Work": "Wall Kicks Will Work",
        "Tiny Main": "Tiny Main", "Huge Island": "Huge Island", "Tiny Island": "Tiny Island",
    }
    for old, new in replacements.items():
        titled = titled.replace(old, new)
    return titled


_ENEMY_TYPES = (
    ("fire_piranha", "Fire Piranha Plant", 1), ("piranha", "Piranha Plant", 1),
    ("mr_blizzard", "Mr. Blizzard", 3), ("scuttlebug", "Scuttlebug", 3),
    ("spindrift", "Spindrift", 3), ("skeeter", "Skeeter", 3), ("snufit", "Snufit", 2),
    ("fly_guy", "Fly Guy", 2), ("chuckya", "Chuckya", 5), ("lakitu", "Lakitu", 5),
    ("moneybag", "Moneybag", 5), ("bookend", "Flying Bookend", 1),
    ("bob_omb", "Bob-omb", 1), ("goomba", "Goomba", 1), ("koopa", "Koopa Troopa", 1),
    ("mr_i", "Mr. I", 1), ("swoop", "Swoop", 1), ("bully", "Bully", 1),
    ("boo", "Boo", 1), ("pokey", "Pokey", 1), ("whomp", "Whomp", 5),
)
_LEVEL_SOURCE_PREFIXES = {
    "lll", "ssl", "sl", "ttm", "ttc", "rr", "cotmc", "bitdw", "bitfs", "bits",
}
_QUALIFIER_REPLACEMENTS = {
    "main": "Main Area", "start": "Starting Area", "standard": "Defeatable",
    "bob": "", "ombs": "", "enemy": "", "plant": "", "plants": "", "troopa": "", "guys": "",
    "goombas": "", "boos": "", "bullies": "", "bookends": "", "spindrifts": "",
    "scuttlebugs": "", "skeeters": "", "snufits": "", "swoops": "", "pokeys": "",
    "blizzards": "", "moneybags": "", "is": "",
    "coins": "",
}
_ENEMY_OUTPUT_GROUP_OVERRIDES = {
    "whomp_jump_coins": (5, 5),
    "whomp_ground_pound_coins": (5, 5),
    "bits_whomp_jump_coins": (5,),
    "bits_whomp_ground_pound_coins": (5,),
    "huge_piranha_area_plants": (2, 2, 2, 2, 2),
}
_ENEMY_DESCRIPTOR_OVERRIDES = {
    "whomp_jump_coins": "Whomp (Jump)",
    "whomp_ground_pound_coins": "Whomp (Ground Pound)",
    "bits_whomp_jump_coins": "Whomp (Jump)",
    "bits_whomp_ground_pound_coins": "Whomp (Ground Pound)",
    "main_mr_is": "Main Area Mr. I",
    "merry_go_round_boos": "Merry-Go-Round Boo",
    "tiny_piranha_area_plant": "Tiny Island Fire Piranha Plant",
    "tiny_start_goomba": "Tiny Start Goomba",
    "huge_beach_fly_guy": "Beach Fly Guy",
    "huge_near_cannon_fly_guy": "Near Cannon Fly Guy",
    "huge_lakitu": "Huge Island Lakitu",
    "huge_koopa_troopa": "Huge Island Koopa Troopa",
    "huge_cannonball_fly_guy": "Cannonball Area Fly Guy",
    "huge_piranha_area_plants": "Huge Island Fire Piranha Plant",
    "tiny_main_goombas": "Tiny Island Goomba",
    "huge_top_chuckya": "Chuckya",
    "castle_courtyard_boos": "Courtyard Boo",
    "sl_upper_spindrifts": "Additional Outdoor Spindrift",
    "standard_mr_blizzard": "Mr. Blizzard",
    "amazing_emergency_exit_swoop_1": "A-Maze-Ing Emergency Exit Swoop 1",
    "amazing_emergency_exit_swoop_2": "A-Maze-Ing Emergency Exit Swoop 2",
    "upper_red_coin_swoops": "Checkerboard Platform Ride Swoop",
}
_GIANT_GOOMBA_DESCRIPTORS = {
    "huge_start_giant_goombas": "Huge Starting Area Goomba",
    "near_cannon_giant_goomba": "Near Cannon Goomba",
    "huge_windswept_giant_goombas": "Windswept Valley Giant Goomba",
    "huge_koopa_region_giant_goombas": "Koopa the Quick Area Giant Goomba",
    "red_area_giant_goombas": "Red Coins Area Giant Goomba",
}


def _enemy_output_names(
        source_id: str, kind: CoinOutputKind, count: int,
) -> tuple[str, ...] | None:
    if any(marker in source_id for marker in ("_line", "_ring", "_post")) \
            and source_id not in _ENEMY_OUTPUT_GROUP_OVERRIDES:
        return None
    matched = next((entry for entry in _ENEMY_TYPES if entry[0] in source_id), None)
    if matched is None:
        return None
    token, enemy_name, default_outputs = matched
    qualifier_tokens = source_id.split("_")
    if qualifier_tokens and qualifier_tokens[0] in _LEVEL_SOURCE_PREFIXES:
        qualifier_tokens.pop(0)
    enemy_tokens = set(token.split("_"))
    qualifier_tokens = [
        _QUALIFIER_REPLACEMENTS.get(part, part)
        for part in qualifier_tokens
        if part not in enemy_tokens
    ]
    qualifier = " ".join(part for part in qualifier_tokens if part)
    descriptor = _ENEMY_DESCRIPTOR_OVERRIDES.get(
        source_id,
        f"{_title_source_label(qualifier)} {enemy_name}" if qualifier else enemy_name,
    )

    group_sizes = _ENEMY_OUTPUT_GROUP_OVERRIDES.get(source_id)
    if group_sizes is None:
        if count % default_outputs:
            return None
        group_sizes = (default_outputs,) * (count // default_outputs)

    coin_name = "Blue Coin" if kind is CoinOutputKind.BLUE else "Coin"
    names = []
    multiple_enemies = len(group_sizes) > 1
    for enemy_index, output_count in enumerate(group_sizes, 1):
        enemy = f"{descriptor} {enemy_index}" if multiple_enemies else descriptor
        for output_index in range(1, output_count + 1):
            suffix = f"{coin_name} {output_index}" if output_count > 1 else coin_name
            names.append(f"{enemy}, {suffix}")
    return tuple(names) if len(names) == count else None


STANDALONE_YELLOW_COIN_SOURCE_IDS = frozenset({
    "rotating_plank_coins", "penguin_slide_yellow_coins", "rolling_rocks_coins",
    "lll_grey_ramp_coins", "lll_sinking_platform_coins", "lll_spinning_volcano_platform_coins",
    "lll_southeast_grey_ramp_coins", "lll_volcano_s_island_coins",
    "lll_volcano_first_ridge_coin_line", "lll_volcano_second_ridge_coins",
    "lll_volcano_floating_platform_coins", "lll_volcano_post_platform_coin",
    "lll_volcano_checkerboard_lift_coin", "lll_elevator_tour_platform_coins",
    "ssl_pillar_and_pyramid_coins", "ssl_upper_pyramid_single_coins", "ddd_seafloor_chest_coins",
    "sl_start_coins", "sl_upper_slope_single_coins", "sl_penguin_and_face_coins",
    "sl_snowman_head_plank_coins", "sl_igloo_single_coins", "sl_impossible_coin",
    "ttm_hidden_coin_before_slide", "ttm_slide_single_coins", "tiny_main_individual_coins",
    "tiny_impossible_coin", "tiny_purple_switch_coin", "huge_beach_coins", "ttc_start_cube_coins",
    "rr_first_donut_lift_coins", "rr_second_carpet_platform_coin", "rr_second_carpet_air_coin",
    "pss_single_yellow_coins", "totwc_single_yellow_coins", "vcutm_end_marker_coins",
    "bitdw_single_coins_before_slope", "bitdw_slope_single_coins", "bitfs_start_single_coins",
    "bits_tilting_w_coins", "bits_raised_steps_coins", "bits_spinning_platform_coins",
    "castle_grounds_bridge_coins", "castle_lobby_coins",
})


STANDALONE_YELLOW_COIN_NAME_OVERRIDES = {
    "rotating_plank_coins": "Rotating Plank Coin",
    "lll_volcano_s_island_coins": "Coin on the Volcano S-Shaped Island",
    "lll_volcano_first_ridge_coin_line": "Coin on the Volcano First Ridge",
    "lll_volcano_second_ridge_coins": "Coin on the Volcano Second Ridge",
    "lll_volcano_floating_platform_coins": "Coin on a Volcano Floating Platform",
    "lll_volcano_post_platform_coin": "Coin After the Volcano Floating Platforms",
    "lll_volcano_checkerboard_lift_coin": "Coin by the Volcano Checkerboard Lift",
    "lll_elevator_tour_platform_coins": "Coin on a Tiny Elevator Tour Platform",
    "sl_impossible_coin": "Impossible Coin",
    "sl_penguin_and_face_coins": "Coin Leading to Snowman's Big Head",
    "ttm_hidden_coin_before_slide": "Hidden Coin Before the Slide",
    "tiny_impossible_coin": "Impossible Coin",
    "tiny_purple_switch_coin": "Five Itty Bitty Secrets Island Coin",
    "vcutm_end_marker_coins": "Star Cage Coin",
    "rr_second_carpet_platform_coin": "Coin on the Second Carpet's Grey Platform",
    "rr_second_carpet_air_coin": "Coin in the Air Along the Second Carpet",
    "castle_grounds_bridge_coins": "Coin Under the Bridge",
    "castle_lobby_coins": "Lobby Coin",
}


def _standalone_yellow_names(source_id: str, label: str, count: int) -> tuple[str, ...]:
    base = STANDALONE_YELLOW_COIN_NAME_OVERRIDES.get(source_id)
    has_curated_name = base is not None
    if base is None:
        base = label
        for prefix in ("Individual coins", "Single yellow coins", "Single Yellow Coins", "Single coins",
                       "Three coins", "Two coins", "Coins"):
            if base.startswith(prefix):
                base = "Coin" + base[len(prefix):]
                break
        else:
            if " coin" in base.lower():
                start = base.lower().index(" coin") + 1
                end = start + (5 if base[start:start + 5].lower() == "coins" else 4)
                base = base[:start] + "Coin" + base[end:]
            else:
                base = f"{base} Coin"
    return _repeat_names(base if has_curated_name else _title_source_label(base), count)


def _without_coin_separator(name: str) -> str:
    """Keep producer and formation coin names readable without comma-separated suffixes."""
    return name.replace(", Blue Coin", " Blue Coin").replace(", Coin", " Coin") \
        .replace(", Center Coin", " Center Coin")


def _build_catalog() -> tuple[CoinSourceDefinition, ...]:
    sources: list[CoinSourceDefinition] = []
    for course_name in COURSE_ORDER:
        course_base = INDIVIDUAL_COIN_LOCATION_BASE_ID + _COURSE_INDEX[course_name] * INDIVIDUAL_COIN_COURSE_STRIDE
        offset = 0

        red_methods = RED_COIN_SOURCE_METHODS.get(course_name)
        if red_methods:
            outputs = tuple(
                CoinOutputDefinition(
                    CoinOutputID(course_name, "red_coin", index), course_base + offset + index - 1,
                    f"{course_name} - {RED_COIN_NAMES[course_name][index - 1]}", CoinOutputKind.RED, 2,
                    red_methods[index],
                )
                for index in range(1, 9)
            )
            sources.append(CoinSourceDefinition(course_name, "red_coin", "Red Coins", outputs, 16))
            offset += 8

        for source_id, label, kind_name, count in SOURCE_LAYOUTS[course_name]:
            if kind_name == "giant":
                names = _repeat_names(_GIANT_GOOMBA_DESCRIPTORS[source_id], count)
                outputs = []
                for index, producer_name in enumerate(names, 1):
                    outputs.extend((
                        CoinOutputDefinition(
                            CoinOutputID(course_name, source_id, index * 2 - 1), course_base + offset,
                            f"{course_name} - {producer_name} Coin", CoinOutputKind.YELLOW, 1,
                            (f"{source_id}_yellow",),
                        ),
                        CoinOutputDefinition(
                            CoinOutputID(course_name, source_id, index * 2), course_base + offset + 1,
                            f"{course_name} - {producer_name} Blue Coin", CoinOutputKind.BLUE, 5,
                            (f"{source_id}_blue",),
                        ),
                    ))
                    offset += 2
                sources.append(CoinSourceDefinition(course_name, source_id, label, tuple(outputs), count * 5))
                continue

            kind = CoinOutputKind(kind_name)
            names = _enemy_output_names(source_id, kind, count) or (
                _standalone_yellow_names(source_id, label, count)
                if kind is CoinOutputKind.YELLOW and source_id in STANDALONE_YELLOW_COIN_SOURCE_IDS
                else _output_names(label, kind, count)
            )
            value = 5 if kind is CoinOutputKind.BLUE else 1
            outputs = tuple(
                CoinOutputDefinition(
                    CoinOutputID(course_name, source_id, index), course_base + offset + index - 1,
                    f"{course_name} - {_without_coin_separator(COIN_OUTPUT_NAME_OVERRIDES.get(
                        (course_name, source_id, index), name))}",
                    kind, value,
                    COIN_OUTPUT_SOURCE_METHOD_OVERRIDES.get(
                        (course_name, source_id, index), (source_id,)),
                )
                for index, name in enumerate(names, 1)
            )
            sources.append(CoinSourceDefinition(course_name, source_id, label, outputs, count * value))
            offset += count

        if course_name == "Bob-omb Battlefield":
            # The physical object order runs furthest-to-nearest in places. Keep the stable output IDs,
            # but display and logically treat the rings from closest to the island to furthest.
            ring_display_order = {4: 1, 3: 2, 2: 3, 5: 4, 1: 5}
            closest_ring_indices = range(25, 33)
            partial_flight_ring_indices = set(range(1, 41)) - set(closest_ring_indices)
            partial_flight_center_indices = {2, 3, 4, 5}
            custom = (
                ("island_vertical_ring", "Vertical Ring Coin Above the Island", 40, tuple(
                    ("island_first_ring_easy_coins",) if i in range(25, 28) else
                    ("island_partial_first_ring_three_coins", "island_full_trick_vertical_ring_coins", "island_cannon_vertical_ring_coins") if i in range(28, 31) else
                    ("island_partial_first_ring_two_coins", "island_full_trick_vertical_ring_coins", "island_cannon_vertical_ring_coins") if i in range(31, 33) else
                    ("island_partial_flight_ring_coins", "island_full_trick_vertical_ring_coins", "island_cannon_vertical_ring_coins") if i in partial_flight_ring_indices else
                    ("island_full_trick_vertical_ring_coins", "island_cannon_vertical_ring_coins")
                    for i in range(1, 41))),
                ("island_ring_center", "Yellow Coin in the Center of an Island Ring", 5, tuple(
                    ("island_partial_flight_center_coins", "island_full_trick_ring_center_coins", "island_cannon_ring_center_coins") if i in partial_flight_center_indices else
                    ("island_full_trick_ring_center_coins", "island_cannon_ring_center_coins",)
                    for i in range(1, 6))),
            )
            for source_id, label, count, methods in custom:
                if source_id == "island_vertical_ring":
                    names = tuple(
                        f"Island Vertical Coin Ring {ring_display_order[((index - 1) // 8) + 1]} "
                        f"Coin {((index - 1) % 8) + 1}"
                        for index in range(1, count + 1)
                    )
                else:
                    names = tuple(
                        f"Island Coin Ring {ring_display_order[index]} Center Coin"
                        for index in range(1, count + 1)
                    )
                outputs = tuple(
                    CoinOutputDefinition(
                        CoinOutputID(course_name, source_id, index), course_base + offset + index - 1,
                        f"{course_name} - {names[index - 1]}", CoinOutputKind.YELLOW, 1, methods[index - 1],
                    ) for index in range(1, count + 1)
                )
                sources.append(CoinSourceDefinition(course_name, source_id, label, outputs, count))
                offset += count

        if course_name == "Tower of the Wing Cap":
            outputs = tuple(
                CoinOutputDefinition(
                    CoinOutputID(course_name, "coin_ring", index), course_base + offset + index - 1,
                    f"{course_name} - Coin Ring {((index - 1) // 8) + 1} Coin {((index - 1) % 8) + 1}",
                    CoinOutputKind.YELLOW, 1,
                    ("totwc_mastery_ring_coins",) if index <= 20 else ("totwc_mastery_wing_cap_ring_coins",),
                ) for index in range(1, 33)
            )
            sources.append(CoinSourceDefinition(course_name, "coin_ring", "Coin Ring Coins", outputs, 32))

    return tuple(sources)


coin_source_catalog = _build_catalog()
coin_output_catalog = tuple(output for source in coin_source_catalog for output in source.outputs)
coin_output_by_name = {output.location_name: output for output in coin_output_catalog}
coin_output_by_id = {output.output_id: output for output in coin_output_catalog}
individual_coin_location_table = {output.location_name: output.location_id for output in coin_output_catalog}

if len(coin_output_by_name) != len(coin_output_catalog):
    raise ValueError("Individual Coin Check names must be unique")
if len({output.location_id for output in coin_output_catalog}) != len(coin_output_catalog):
    raise ValueError("Individual Coin Check IDs must be unique")


def select_individual_coin_outputs(
        percentage: int, rng: random.Random,
        catalog: Iterable[CoinOutputDefinition] = coin_output_catalog,
        excluded_output_ids: frozenset[CoinOutputID] = frozenset(),
) -> tuple[CoinOutputDefinition, ...]:
    """Select the requested percentage independently within each course."""
    if not 0 <= percentage <= 100:
        raise ValueError("Coin Checks percentage must be between 0 and 100")
    by_course: dict[str, list[CoinOutputDefinition]] = defaultdict(list)
    for output in catalog:
        if output.output_id in excluded_output_ids:
            continue
        by_course[output.output_id.course_name].append(output)
    selected = []
    for course_name in COURSE_ORDER:
        outputs = sorted(by_course[course_name], key=lambda output: output.output_id)
        count = (len(outputs) * percentage + 99) // 100
        selected.extend(rng.sample(outputs, count))
    return tuple(sorted(selected, key=lambda output: output.location_id))
