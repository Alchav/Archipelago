import random
import unittest

from BaseClasses import CollectionState, ItemClassification

from .bases import SM64TestBase
from ..CoinChecks import (
    COIN_SOURCE_METHOD_REGION_NAMES,
    COURSE_MAXIMUM_COIN_VALUES,
    CoinOutputKind,
    CoinOutputID,
    STANDALONE_YELLOW_COIN_SOURCE_IDS,
    coin_output_by_id,
    coin_output_by_name,
    coin_output_catalog,
    coin_output_region_name,
    coin_source_catalog,
    select_individual_coin_outputs,
)
from ..CoinLogic import COIN_EVALUATORS
from ..RuleBuilder import CanCollectCoinOutput


class CoinCheckCatalogTest(unittest.TestCase):
    def test_wmotr_red_coins_match_physical_elevation_and_routes(self):
        course_name = "Wing Mario Over the Rainbow"
        expected = (
            ("Cannon Region Red Coin 1", ("wmotr_cannon_red_coins",)),
            ("Cannon Region Red Coin 2", ("wmotr_cannon_red_coins",)),
            ("Cannon Region Red Coin 3", ("wmotr_cannon_red_coins",)),
            ("Flight Path Red Coin 1", ("wmotr_flight_red_coins",)),
            ("Flight Path Red Coin 2", ("wmotr_flight_red_coins", "wmotr_long_jump_second_red_coin")),
            ("Flight Path Red Coin 3", (
                "wmotr_flight_red_coins",
                "wmotr_long_jump_first_red_coin",
                "wmotr_wing_cap_fallback_red_coin",
            )),
            ("Initial Red Coin", ("wmotr_initial_red_coin",)),
            ("Cannon Region Red Coin 4", ("wmotr_cannon_red_coins",)),
        )
        for output_index, (expected_name, expected_methods) in enumerate(expected, 1):
            with self.subTest(output_index=output_index):
                output = coin_output_by_id[CoinOutputID(course_name, "red_coin", output_index)]
                self.assertEqual(output.location_name, f"{course_name} - {expected_name}")
                self.assertEqual(output.source_methods, expected_methods)

    def test_ttm_reported_coin_names_match_their_physical_sources(self):
        course_name = "Tall, Tall Mountain"
        expected_red_names = (
            "Scary Shrooms Red Coin 4",
            "Scary Shrooms Red Coin 2",
            "Scary Shrooms Red Coin 1",
            "Vine Wall Lower Red Coin 1",
            "Vine Wall Lower Red Coin 2",
            "Scary Shrooms Red Coin 3",
        )
        for output_index, expected_name in enumerate(expected_red_names, 1):
            with self.subTest(kind="red", output_index=output_index):
                self.assertEqual(
                    coin_output_by_id[CoinOutputID(course_name, "red_coin", output_index)].location_name,
                    f"{course_name} - {expected_name}",
                )

        expected_source_names = {
            "ttm_middle_bridge_coin_line": tuple(
                f"{course_name} - Bob-omb Buddy Bridge Coin {index}" for index in range(1, 6)),
            "ttm_middle_chuckya": tuple(
                f"{course_name} - Chuckya Coin {index}" for index in range(1, 6)),
            "ttm_middle_bob_ombs": tuple(
                f"{course_name} - Past Vine Wall Bob-omb {index} Coin" for index in range(1, 4)),
        }
        for source_id, expected_names in expected_source_names.items():
            with self.subTest(source_id=source_id):
                source = next(source for source in coin_source_catalog
                              if source.course_name == course_name and source.source_id == source_id)
                self.assertEqual(tuple(output.location_name for output in source.outputs), expected_names)

        upper_line = next(source for source in coin_source_catalog
                          if source.course_name == course_name
                          and source.source_id == "ttm_upper_leaf_coin_line")
        self.assertEqual(
            tuple(output.location_name for output in upper_line.outputs),
            tuple(f"{course_name} - Upper Vine Wall Hangable Ceiling Coin Line Coin {index}"
                  for index in range(1, 6)),
        )
        self.assertEqual(
            tuple(output.source_methods for output in upper_line.outputs),
            (("ttm_upper_leaf_first_coin",),) + (("ttm_upper_leaf_coin_line",),) * 4,
        )

    def test_ttc_red_coin_names_are_plain_numbered_names(self):
        course_name = "Tick Tock Clock"
        self.assertEqual(
            tuple(coin_output_by_id[CoinOutputID(course_name, "red_coin", index)].location_name
                  for index in range(1, 9)),
            tuple(f"{course_name} - Red Coin {index}" for index in range(1, 9)),
        )

    def test_ccm_penguin_slide_names_follow_descent_order(self):
        course_name = "Cool, Cool Mountain"
        single_coin_order = (
            6, 7, 12, 1, 2, 3, 4, 5, 22, 23, 24, 25, 26, 27,
            9, 8, 10, 11, 13, 14, 15, 16, 17, 18, 19, 20, 21,
        )
        for display_index, output_index in enumerate(single_coin_order, 1):
            with self.subTest(kind="single", display_index=display_index):
                self.assertEqual(
                    coin_output_by_id[CoinOutputID(
                        course_name, "penguin_slide_yellow_coins", output_index)].location_name,
                    f"{course_name} - Penguin Slide Coin {display_index}",
                )

        line_order = (
            (9, range(5, 0, -1)),
            (1, range(1, 6)),
            (2, range(1, 6)),
            (3, range(1, 6)),
            (4, range(1, 6)),
            (5, range(1, 6)),
            (6, range(5, 0, -1)),
            (7, range(5, 0, -1)),
            (8, range(5, 0, -1)),
        )
        for display_line, (source_line, source_coins) in enumerate(line_order, 1):
            for display_coin, source_coin in enumerate(source_coins, 1):
                with self.subTest(kind="line", line=display_line, coin=display_coin):
                    output_index = (source_line - 1) * 5 + source_coin
                    self.assertEqual(
                        coin_output_by_id[CoinOutputID(
                            course_name, "penguin_slide_coin_lines", output_index)].location_name,
                        f"{course_name} - Penguin Slide Coin Line {display_line} Coin {display_coin}",
                    )

        self.assertEqual(
            coin_output_by_id[CoinOutputID(course_name, "slide_blue_coin", 1)].location_name,
            f"{course_name} - Penguin Slide Blue Coin",
        )

    def test_ttc_block_coin_sources_match_their_physical_blocks(self):
        expected_first_outputs = {
            "ttc_past_three_spinners_block": (
                4_013_046, "Tick Tock Clock - Past Three Spinners 3-Coin Block Coin 1"),
            "ttc_top_central_platform_block": (
                4_013_049, "Tick Tock Clock - Top Central Platform 10-Coin Block Coin 1"),
            "ttc_timed_jumps_block": (
                4_013_059, "Tick Tock Clock - Above Timed Jumps on Moving Bars 3-Coin Block Coin 1"),
            "ttc_four_moving_bars_block": (
                4_013_072, "Tick Tock Clock - Above Four Moving Bars 10-Coin Block Coin 1"),
            "ttc_top_clock_hand_block": (
                4_013_082, "Tick Tock Clock - Top Clock Hand 10-Coin Block Coin 1"),
        }
        sources = {
            source.source_id: source
            for source in coin_source_catalog
            if source.course_name == "Tick Tock Clock"
        }
        for source_id, (location_id, location_name) in expected_first_outputs.items():
            with self.subTest(source_id=source_id):
                first_output = sources[source_id].outputs[0]
                self.assertEqual(first_output.location_id, location_id)
                self.assertEqual(first_output.location_name, location_name)

    def test_atomic_output_denominations(self):
        self.assertEqual(
            {output.kind: output.coin_value for output in coin_output_catalog},
            {CoinOutputKind.YELLOW: 1, CoinOutputKind.RED: 2, CoinOutputKind.BLUE: 5},
        )

    def test_source_maximums_match_every_course_evaluator_maximum(self):
        totals = {course_name: 0 for course_name in COURSE_MAXIMUM_COIN_VALUES}
        for source in coin_source_catalog:
            totals[source.course_name] += source.maximum_coin_value
        self.assertEqual(totals, COURSE_MAXIMUM_COIN_VALUES)

    def test_names_and_ids_are_unique_and_stable(self):
        self.assertEqual(len(coin_output_catalog), 2080)
        self.assertEqual(len(coin_output_by_name), len(coin_output_catalog))
        self.assertEqual(
            len({output.location_id for output in coin_output_catalog}),
            len(coin_output_catalog),
        )
        self.assertEqual(
            coin_output_by_name["Jolly Roger Bay - Red Coin on the Raised Ship 1"].location_id,
            4_002_005,
        )
        self.assertIn("Tiny-Huge Island - Impossible Coin", coin_output_by_name)
        self.assertIn(
            "Wet-Dry World - Downtown Skeeter 1 Coin 1",
            coin_output_by_name,
        )
        self.assertIn(
            "Wet-Dry World - Gray Building Coin Line Coin 5",
            coin_output_by_name,
        )
        self.assertIn(
            "Wet-Dry World - Downtown Narrow Plank Coin Line Coin 4",
            coin_output_by_name,
        )
        self.assertIn("The Secret Aquarium - Vertical Coin Ring 1 Coin 3", coin_output_by_name)
        self.assertIn("Castle - Coin Under the Bridge 1", coin_output_by_name)
        self.assertIn("Castle - Lobby Coin 4", coin_output_by_name)
        self.assertIn("Castle - Courtyard Boo 9 Coin", coin_output_by_name)
        self.assertIn("Rainbow Ride - First Swing Vertical Coin Line Coin 4", coin_output_by_name)
        self.assertIn("Rainbow Ride - Swingin' in the Breeze Coin Line Coin 5", coin_output_by_name)
        self.assertIn("Rainbow Ride - Tricky Triangles Coin Line Coin 1", coin_output_by_name)
        self.assertIn(
            "Lethal Lava Land - First Sinking Platform Coin Line Coin 5",
            coin_output_by_name,
        )
        self.assertIn(
            "Lethal Lava Land - Sinking Platform near the Volcano Coin Line Coin 5",
            coin_output_by_name,
        )
        self.assertIn(
            "Dire, Dire Docks - Coin Ring Leading to the Tunnel 1 Coin 2",
            coin_output_by_name,
        )
        self.assertIn(
            "Dire, Dire Docks - Coin Ring Leading to the Tunnel 2 Coin 1",
            coin_output_by_name,
        )
        self.assertIn("Dire, Dire Docks - Tunnel Coin Ring Coin 1", coin_output_by_name)
        self.assertIn(
            "Dire, Dire Docks - Vertical Coin Line by the Chest Coin 3",
            coin_output_by_name,
        )
        self.assertIn(
            "Dire, Dire Docks - Vertical Coin Line by the Whirlpool Coin 1",
            coin_output_by_name,
        )
        self.assertEqual(
            tuple(
                coin_output_by_name[f"Whomp's Fortress - Rotating Plank Coin {index}"].location_id
                for index in range(1, 5)
            ),
            (4_001_032, 4_001_033, 4_001_034, 4_001_035),
        )
        self.assertEqual(
            tuple(
                output.location_name.removeprefix("Whomp's Fortress - ")
                for output in coin_output_catalog
                if output.output_id.course_name == "Whomp's Fortress"
                and output.output_id.source_id == "red_coin"
            ),
            (
                "Rotating Plank Red Coin",
                "Narrow Ledge Red Coin",
                "Piranha Plant Red Coin",
                "Bomp Red Coin",
                "Slide Beneath Rotating Plank Red Coin",
                "Thwomp Red Coin",
                "Floating Isle Red Coin 1",
                "Floating Isle Red Coin 2",
            ),
        )
        self.assertFalse(any(
            "Horizontal Coin Line" in output.location_name
            or "Horizontal Coin Ring" in output.location_name
            or ", Coin" in output.location_name
            or ", Blue Coin" in output.location_name
            for output in coin_output_catalog
        ))
        self.assertEqual(
            tuple(
                name.removeprefix("Cool, Cool Mountain - ")
                for name in coin_output_by_name
                if name.startswith("Cool, Cool Mountain - ")
                and name.endswith("Red Coin")
            ),
            (
                "First Tree Red Coin",
                "Bottom of Snowman Slide Red Coin",
                "Bridge Out Red Coin",
                "Ice Pillar Red Coin",
                "Top of Buddy Lift Red Coin",
                "Bottom Bridge Island Red Coin",
                "Bottom Tree Red Coin",
                "Bottom Corner Red Coin",
            ),
        )
        ccm_sources = {
            source.source_id: source
            for source in coin_source_catalog
            if source.course_name == "Cool, Cool Mountain"
        }
        self.assertEqual(
            tuple(output.location_name for output in ccm_sources["main_spindrifts"].outputs[:6]),
            (
                *(f"Cool, Cool Mountain - Snowman Head Spindrift Coin {index}"
                  for index in range(1, 4)),
                *(f"Cool, Cool Mountain - Snowman Body Spindrift Coin {index}"
                  for index in range(1, 4)),
            ),
        )
        self.assertEqual(
            tuple(output.location_name
                  for output in ccm_sources["standard_mr_blizzard"].outputs),
            tuple(f"Cool, Cool Mountain - Mr. Blizzard Coin {index}"
                  for index in range(1, 4)),
        )
        self.assertEqual(
            tuple(output.location_name
                  for output in ccm_sources["main_mountain_coin_lines"].outputs),
            tuple(
                f"Cool, Cool Mountain - Snowman Slide Coin Line {line} Coin {coin}"
                for line in range(1, 5)
                for coin in range(1, 6)
            ),
        )
        self.assertEqual(
            tuple(
                output.location_name.removeprefix("Vanish Cap Under the Moat - ")
                for output in coin_output_catalog
                if output.output_id.course_name == "Vanish Cap Under the Moat"
                and output.output_id.source_id == "red_coin"
            ),
            (
                "Slide Red Coin 1",
                "Slide Red Coin 2",
                "Slide Red Coin 3",
                "Slide Red Coin 4",
                "Tilting Platform Red Coin 1",
                "Tilting Platform Red Coin 2",
                "Checkerboard Platform Red Coin",
                "Cap Switch Red Coin",
            ),
        )
        self.assertEqual(
            tuple(
                output.location_name.removeprefix("Vanish Cap Under the Moat - ")
                for output in coin_output_catalog
                if output.output_id.course_name == "Vanish Cap Under the Moat"
                and output.output_id.source_id == "vcutm_end_marker_coins"
            ),
            ("Star Cage Coin 1", "Star Cage Coin 2", "Star Cage Coin 3"),
        )
        self.assertEqual(
            tuple(
                output.location_name.removeprefix("Bob-omb Battlefield - ")
                for output in coin_output_catalog
                if output.output_id.course_name == "Bob-omb Battlefield"
                and output.output_id.source_id == "red_coin"
            ),
            (
                "Wooden Posts Red Coin 1",
                "Wooden Posts Red Coin 2",
                "Grass Ramp Red Coin",
                "Chain Chomp Red Coin",
                "Checkerboard Platform Red Coin",
                "Switch Tunnel Red Coin",
                "Below the Island Red Coin",
                "Island Red Coin",
            ),
        )
        closest_ring = tuple(
            output for output in coin_output_catalog
            if output.output_id.course_name == "Bob-omb Battlefield"
            and output.output_id.source_id == "island_vertical_ring"
            and "Island Vertical Coin Ring 1 " in output.location_name
        )
        self.assertEqual(tuple(output.output_id.output_index for output in closest_ring), tuple(range(25, 33)))
        self.assertEqual(closest_ring[0].source_methods, ("island_first_ring_easy_coins",))
        self.assertIn("island_partial_first_ring_two_coins", closest_ring[-1].source_methods)
        self.assertEqual(
            coin_output_by_name["Hazy Maze Cave - First Room Coin 1"].output_id.source_id,
            "rolling_rocks_coins",
        )
        self.assertEqual(
            coin_output_by_name[
                "Hazy Maze Cave - Swimming Beast in the Cavern Star Coin Ring Coin 1"
            ].output_id.source_id,
            "lake_approach_coin_ring",
        )
        self.assertEqual(
            coin_output_by_name[
                "Hazy Maze Cave - Past Rolling Rocks 1-Up Block Coin Ring Coin 1"
            ].output_id.source_id,
            "swimming_beast_coin_ring",
        )
        self.assertEqual(
            {
                name: coin_output_by_name[name].location_id
                for name in (
                    "Hazy Maze Cave - A-Maze-Ing Emergency Exit Swoop 1 Coin",
                    "Hazy Maze Cave - Pit Island Room Swoop Coin",
                    "Hazy Maze Cave - A-Maze-Ing Emergency Exit Swoop 2 Coin",
                )
            },
            {
                "Hazy Maze Cave - A-Maze-Ing Emergency Exit Swoop 1 Coin": 4005040,
                "Hazy Maze Cave - Pit Island Room Swoop Coin": 4005061,
                "Hazy Maze Cave - A-Maze-Ing Emergency Exit Swoop 2 Coin": 4005062,
            },
        )
        self.assertEqual(
            tuple(
                output.location_name.removeprefix("Hazy Maze Cave - ")
                for output in coin_output_catalog
                if output.output_id.course_name == "Hazy Maze Cave"
                and output.output_id.source_id == "red_coin"
            ),
            (
                "Lower Red Coin 1",
                "Lower Red Coin 2",
                "Lower Red Coin 3",
                "Lower Red Coin 4",
                "Checkerboard Platform Arrival Platform Red Coin 1",
                "Checkerboard Platform Arrival Platform Red Coin 2",
                "Checkerboard Platform Ride Red Coin 1",
                "Checkerboard Platform Ride Red Coin 2",
            ),
        )
        self.assertEqual(
            coin_output_by_name[
                "Hazy Maze Cave - Coin Line Leading to the Toxic Maze Star Coin 1"
            ].output_id.source_id,
            "pit_islands_ceiling_coin_line",
        )
        self.assertEqual(
            coin_output_by_name[
                "Hazy Maze Cave - Coin Line on the Hangable Ceiling above Pit Islands Coin 1"
            ].output_id.source_id,
            "toxic_maze_star_coin_line",
        )
        self.assertIn(
            "Hazy Maze Cave - Checkerboard Platform Ride Swoop 1 Coin",
            coin_output_by_name,
        )
        self.assertEqual(
            tuple(
                output.location_name.removeprefix("Bowser in the Sky - ")
                for output in coin_output_catalog
                if output.output_id.course_name == "Bowser in the Sky"
                and output.output_id.source_id == "red_coin"
            )[:3],
            (
                "Piranha Plant Red Coin",
                "Push Block Red Coin",
                "Beneath the Tilting Platform Hidden Red Coin",
            ),
        )
        self.assertEqual(
            tuple(
                output.location_name.removeprefix("Bowser in the Sky - ")
                for output in coin_output_catalog
                if output.output_id.course_name == "Bowser in the Sky"
                and output.output_id.source_id == "bits_whomp_platform_lines"
            ),
            (
                *(f"Coin Line Beneath the Whomp Coin {index}" for index in range(1, 6)),
                *(f"Coin Line Beneath the Tilting Platform Coin {index}" for index in range(1, 6)),
            ),
        )

    def test_standalone_yellow_coins_are_not_named_as_outputs_from_coins(self):
        standalone_outputs = (
            output
            for source in coin_source_catalog
            if source.source_id in STANDALONE_YELLOW_COIN_SOURCE_IDS
            for output in source.outputs
        )
        self.assertTrue(all("Yellow Coin" not in output.location_name
                            for output in standalone_outputs))

    def test_yellow_coin_checks_omit_the_color(self):
        self.assertTrue(all("Yellow Coin" not in output.location_name for output in coin_output_catalog))

    def test_percentage_is_applied_independently_per_catalogued_course(self):
        selected = select_individual_coin_outputs(
            50, random.Random(0))
        selected_counts = {}
        catalog_counts = {}
        for output in selected:
            selected_counts[output.output_id.course_name] = \
                selected_counts.get(output.output_id.course_name, 0) + 1
        for output in coin_output_catalog:
            catalog_counts[output.output_id.course_name] = \
                catalog_counts.get(output.output_id.course_name, 0) + 1
        self.assertEqual(
            selected_counts,
            {course: (count * 50 + 99) // 100 for course, count in catalog_counts.items()},
        )

    def test_full_selection_contains_every_physical_output(self):
        self.assertEqual(
            set(select_individual_coin_outputs(100, random.Random(0))),
            set(coin_output_catalog),
        )

    def test_giant_goomba_has_separate_yellow_and_blue_logical_outputs(self):
        source = next(source for source in coin_source_catalog
                      if source.source_id == "huge_start_giant_goombas")
        self.assertEqual(source.maximum_coin_value, 15)
        self.assertEqual(len(source.outputs), 6)
        for yellow, blue in zip(source.outputs[::2], source.outputs[1::2]):
            self.assertEqual((yellow.kind, yellow.coin_value), (CoinOutputKind.YELLOW, 1))
            self.assertEqual((blue.kind, blue.coin_value), (CoinOutputKind.BLUE, 5))
            self.assertEqual(yellow.output_id.source_id, blue.output_id.source_id)
            self.assertEqual(yellow.source_methods, ("huge_start_giant_goombas_yellow",))
            self.assertEqual(blue.source_methods, ("huge_start_giant_goombas_blue",))

    def test_tiny_huge_island_sources_preserve_physical_object_boundaries(self):
        sources = {
            source.source_id: source
            for source in coin_source_catalog
            if source.course_name == "Tiny-Huge Island"
        }
        self.assertEqual(sum(source.maximum_coin_value for source in sources.values()), 193)
        self.assertEqual(len(sources["tiny_main_three_coin_block"].outputs), 3)
        self.assertEqual(len(sources["huge_windswept_line"].outputs), 5)
        self.assertEqual(len(sources["huge_koopa_region_line"].outputs), 4)
        self.assertEqual(len(sources["tiny_impossible_coin"].outputs), 1)
        self.assertEqual(len(sources["huge_top_wooden_plank_line"].outputs), 5)
        self.assertEqual(len(sources["red_area_plank_line"].outputs), 5)
        self.assertEqual(len(sources["wiggler_cave_coin_lines"].outputs), 10)
        self.assertEqual(len(sources["huge_piranha_area_plants"].outputs), 10)

    def test_ssl_top_vertical_line_uses_stricter_logic_for_its_highest_coin(self):
        source = next(
            source for source in coin_source_catalog
            if source.course_name == "Shifting Sand Land"
            and source.source_id == "ssl_pyramid_top_vertical_coin_line"
        )
        self.assertEqual(
            tuple(output.source_methods for output in source.outputs),
            (
                ("ssl_pyramid_top_vertical_coin_line",),
                ("ssl_pyramid_top_vertical_coin_line",),
                ("ssl_pyramid_top_vertical_coin_line",),
                ("ssl_pyramid_top_vertical_coin_line",),
                ("ssl_pyramid_top_vertical_coin_line_top_coin",),
            ),
        )

    def test_ssl_pyramid_and_pillar_coins_have_distinct_names_and_rules(self):
        source = next(
            source for source in coin_source_catalog
            if source.course_name == "Shifting Sand Land"
            and source.source_id == "ssl_pillar_and_pyramid_coins"
        )
        self.assertEqual(
            tuple(output.location_name for output in source.outputs),
            (
                "Shifting Sand Land - Inside Pyramid Coin 1",
                "Shifting Sand Land - Inside Pyramid Coin 2",
                "Shifting Sand Land - Pillar Coin 1",
                "Shifting Sand Land - Pillar Coin 2",
                "Shifting Sand Land - Pillar Coin 3",
                "Shifting Sand Land - Quicksand Pillar Coin",
            ),
        )
        self.assertEqual(
            tuple(output.source_methods for output in source.outputs),
            (("ssl_inside_pyramid_coins",),) * 2
            + (("ssl_pillar_coins",),) * 3
            + (("ssl_quicksand_pillar_coin",),),
        )

    def test_ssl_goombas_are_split_between_the_pyramid_and_outside(self):
        source = next(
            source for source in coin_source_catalog
            if source.course_name == "Shifting Sand Land"
            and source.source_id == "ssl_goombas"
        )
        self.assertEqual(
            tuple(output.source_methods for output in source.outputs),
            (("ssl_pyramid_goombas",),) * 9
            + (("ssl_outside_goombas",),) * 3,
        )

    def test_ssl_upper_pyramid_single_coin_names_follow_physical_order(self):
        source = next(
            source for source in coin_source_catalog
            if source.course_name == "Shifting Sand Land"
            and source.source_id == "ssl_upper_pyramid_single_coins"
        )
        names_by_physical_index = {
            12: "Pyramid Moving-Step Coin 1",
            13: "Pyramid Moving-Step Coin 2",
            10: "Pyramid Moving-Step Coin 3",
            11: "Pyramid Moving-Step Coin 4",
            4: "Pyramid Puzzle Coin 1",
            3: "Pyramid Puzzle Coin 2",
            5: "Pyramid Puzzle Coin 3",
            1: "Pyramid Puzzle Coin 4",
            2: "Pyramid Puzzle Coin 5",
            9: "Pyramid Steps to the Spindel Coin 1",
            7: "Pyramid Steps to the Spindel Coin 2",
            6: "Pyramid Steps to the Spindel Coin 3",
            8: "Pyramid Steps to the Spindel Coin 4",
        }
        for physical_index, expected_name in names_by_physical_index.items():
            with self.subTest(physical_index=physical_index):
                self.assertEqual(
                    source.outputs[physical_index - 1].location_name,
                    f"Shifting Sand Land - {expected_name}",
                )

    def test_ssl_outdoor_and_pyramid_sources_use_distinct_physical_regions(self):
        outdoor_methods = {
            "ssl_throwable_cork_box",
            "ssl_pillar_coins",
            "ssl_quicksand_pillar_coin",
            "ssl_behind_pyramid_coin_line",
            "ssl_pyramid_side_coin_line",
            "ssl_fly_guys",
            "ssl_crazy_boxes",
            "ssl_bob_ombs",
            "ssl_pokeys",
            "ssl_outside_goombas",
            "ssl_low_red_coins",
            "ssl_high_red_coins",
        }
        self.assertEqual(
            {method: COIN_SOURCE_METHOD_REGION_NAMES[method] for method in outdoor_methods},
            {method: "Shifting Sand Land" for method in outdoor_methods},
        )

    def test_snowmans_land_slope_singles_split_the_highest_coin(self):
        source = next(
            source for source in coin_source_catalog
            if source.course_name == "Snowman's Land"
            and source.source_id == "sl_upper_slope_single_coins"
        )
        self.assertEqual(
            tuple(output.source_methods for output in source.outputs),
            (("sl_upper_slope_single_coins",),) * 2
            + (("sl_highest_slope_single_coin",),),
        )

    def test_snowmans_land_red_coins_match_their_physical_regions(self):
        source = next(
            source for source in coin_source_catalog
            if source.course_name == "Snowman's Land" and source.source_id == "red_coin"
        )
        self.assertEqual(
            tuple(output.location_name.removeprefix("Snowman's Land - ") for output in source.outputs),
            (
                "Starting Area Red Coin 2",
                "Under the Bully Red Coin 2",
                "Whirl from the Freezing Pond Red Coin 4",
                "Whirl from the Freezing Pond Red Coin 3",
                "Whirl from the Freezing Pond Red Coin 2",
                "Starting Area Red Coin 1",
                "Whirl from the Freezing Pond Red Coin 1",
                "Under the Bully Red Coin 1",
            ),
        )
        self.assertEqual(
            tuple(output.source_methods for output in source.outputs),
            (
                ("sl_start_red_coins",),
                ("sl_whirl_red_coins",),
                ("sl_whirl_red_coins",),
                ("sl_whirl_red_coins",),
                ("sl_whirl_red_coins",),
                ("sl_start_red_coins",),
                ("sl_whirl_red_coins",),
                ("sl_whirl_red_coins",),
            ),
        )

    def test_snowmans_land_additional_spindrifts_are_not_upper_gated(self):
        source = next(
            source for source in coin_source_catalog
            if source.course_name == "Snowman's Land" and source.source_id == "sl_upper_spindrifts"
        )
        self.assertEqual(
            tuple(output.source_methods for output in source.outputs),
            (("sl_upper_spindrifts",),) * 9,
        )

    def test_shuffled_sub_area_coin_outputs_use_their_physical_regions(self):
        expected_regions = {
            ("Cool, Cool Mountain", "penguin_slide_yellow_coins", 1):
                "Cool, Cool Mountain - Secret Slide",
            ("Snowman's Land", "sl_igloo_goombas", 1): "Snowman's Land - Igloo",
            ("Snowman's Land", "sl_upper_slope_coin_line", 1):
                "Snowman's Land - Igloo Entrance",
            ("Snowman's Land", "sl_upper_slope_single_coins", 3):
                "Snowman's Land - Igloo Entrance",
            ("Tall, Tall Mountain", "ttm_slide_coin_lines", 1):
                "Tall, Tall Mountain - Secret Slide",
            ("Lethal Lava Land", "lll_volcano_s_island_coins", 1):
                "Lethal Lava Land - Volcano",
            ("Shifting Sand Land", "ssl_goombas", 1): "Shifting Sand Land - Pyramid",
            ("Shifting Sand Land", "ssl_goombas", 10): "Shifting Sand Land",
            ("Tiny-Huge Island", "red_coin", 1): "Tiny-Huge Island - Red Coin Cave",
            ("Tiny-Huge Island", "red_area_giant_goombas", 1):
                "Tiny-Huge Island - Red Coins Area",
            ("Tiny-Huge Island", "wiggler_cave_coin_lines", 1):
                "Tiny-Huge Island - Wiggler's Cave",
        }
        for output_key, expected_region in expected_regions.items():
            with self.subTest(output_key=output_key):
                output = coin_output_by_id[CoinOutputID(*output_key)]
                self.assertEqual(coin_output_region_name(output), expected_region)

    def test_bitdw_red_coin_names_and_purple_switch_rules_match_physical_coins(self):
        source = next(
            source for source in coin_source_catalog
            if source.course_name == "Bowser in the Dark World"
            and source.source_id == "red_coin"
        )
        self.assertEqual(
            tuple(output.location_name.removeprefix("Bowser in the Dark World - ")
                  for output in source.outputs),
            (
                "Purple Switch Red Coin 2",
                "Moving Yellow Bar Red Coin",
                "Moving Platforms Red Coin",
                "Spike Platform Red Coin",
                "Above Tilting Platforms Red Coin",
                "Crystal Path Red Coin",
                "Purple Switch Red Coin 1",
                "Near Tilting Platforms Red Coin",
            ),
        )
        self.assertEqual(
            tuple(output.source_methods for output in source.outputs),
            (
                ("bitdw_purple_switch_red_coins",),
                ("bitdw_other_red_coins",),
                ("bitdw_other_red_coins",),
                ("bitdw_other_red_coins",),
                ("bitdw_other_red_coins",),
                ("bitdw_other_red_coins",),
                ("bitdw_purple_switch_red_coins",),
                ("bitdw_other_red_coins",),
            ),
        )

    def test_bitdw_yellow_coin_names_and_slope_rules_match_physical_coins(self):
        sources = {
            source.source_id: source
            for source in coin_source_catalog
            if source.course_name == "Bowser in the Dark World"
        }
        prefix = "Bowser in the Dark World - "

        self.assertEqual(
            tuple(output.location_name.removeprefix(prefix)
                  for output in sources["bitdw_coin_lines"].outputs),
            tuple(f"Coin Line 2 Coin {index}" for index in range(1, 6))
            + tuple(f"Coin Line 1 Coin {index}" for index in range(1, 6)),
        )
        self.assertEqual(
            tuple(output.location_name.removeprefix(prefix)
                  for output in sources["bitdw_coin_rings"].outputs[8:]),
            tuple(f"Moving Platforms Coin Ring Coin {index}" for index in range(1, 9))
            + tuple(f"Spike Platform Coin Ring Coin {index}" for index in range(1, 9)),
        )
        self.assertEqual(
            tuple(output.location_name.removeprefix(prefix)
                  for output in sources["bitdw_goombas"].outputs),
            tuple(f"Goomba {index} Coin" for index in (5, 4, 3, 1, 2, 6)),
        )
        self.assertEqual(
            tuple(output.location_name.removeprefix(prefix)
                  for output in sources["bitdw_single_coins_before_slope"].outputs),
            (
                "Tilting Platforms Coin 3",
                "Tilting Platforms Coin 1",
                "Tilting Platforms Coin 6",
                "Tilting Platforms Coin 4",
                "Bottom of the Slope Coin 2",
                "Upper Slope Coin 3",
                "Upper Slope Coin 2",
                "Above Tilting Platforms Coin 1",
                "Above Tilting Platforms Coin 2",
                "Spike Platform Coin 1",
                "Spike Platform Coin 2",
                "Spike Platform Coin 3",
                "Spike Platform Coin 4",
                "Ferris Wheel Coin",
                "Bottom of the Slope Coin 1",
                "Upper Slope Coin 1",
                "Tilting Platforms Coin 2",
                "Tilting Platforms Coin 5",
            ),
        )
        self.assertEqual(
            tuple(output.source_methods
                  for output in sources["bitdw_single_coins_before_slope"].outputs),
            tuple(
                ("bitdw_slope_single_coins",)
                if index in (6, 7, 16) else ("bitdw_single_coins_before_slope",)
                for index in range(1, 19)
            ),
        )
        self.assertEqual(
            tuple(output.location_name.removeprefix(prefix)
                  for output in sources["bitdw_slope_single_coins"].outputs),
            tuple(f"Moving Platform Coin {index}" for index in range(1, 4)),
        )
        self.assertEqual(
            tuple(output.source_methods
                  for output in sources["bitdw_slope_single_coins"].outputs),
            (("bitdw_single_coins_before_slope",),) * 3,
        )

    def test_bitfs_names_and_rules_match_physical_coins(self):
        sources = {
            source.source_id: source
            for source in coin_source_catalog
            if source.course_name == "Bowser in the Fire Sea"
        }
        prefix = "Bowser in the Fire Sea - "

        self.assertEqual(
            tuple(output.location_name.removeprefix(prefix)
                  for output in sources["bitfs_start_single_coins"].outputs),
            ("First Lava Platforms Coin 2", "First Lava Platforms Coin 1"),
        )
        self.assertEqual(
            tuple(output.location_name.removeprefix(prefix)
                  for output in sources["bitfs_second_sinking_platform_line"].outputs),
            tuple(f"Sinking Platform Coin {index}" for index in range(1, 6)),
        )
        self.assertEqual(
            tuple(output.location_name.removeprefix(prefix)
                  for output in sources["bitfs_wire_grid_ring"].outputs),
            tuple(f"Wire Platform Coin Ring Coin {index}" for index in range(1, 9)),
        )
        self.assertEqual(
            tuple(output.location_name.removeprefix(prefix)
                  for output in sources["red_coin"].outputs),
            (
                "Below the Lift Red Coin",
                "Wire Platform Red Coin",
                "Seesaw Platform Red Coin",
                "Upper Course Red Coin 2",
                "Upper Course Red Coin 3",
                "Upper Course Red Coin 4",
                "Upper Course Red Coin 5",
                "Lift Cage Corner Red Coin",
            ),
        )
        self.assertEqual(
            tuple(output.source_methods for output in sources["red_coin"].outputs),
            (
                ("bitfs_upper_red_coins",),
                ("bitfs_start_red_coins",),
                ("bitfs_second_red_coin",),
                ("bitfs_upper_red_coins",),
                ("bitfs_upper_red_coins",),
                ("bitfs_upper_red_coins",),
                ("bitfs_upper_red_coins",),
                ("bitfs_upper_red_coins",),
            ),
        )

    def test_ttm_slide_coins_are_numbered_from_top_to_bottom(self):
        sources = {
            source.source_id: source
            for source in coin_source_catalog
            if source.course_name == "Tall, Tall Mountain"
        }
        prefix = "Tall, Tall Mountain - "
        single_coin_old_indices = (
            1, 10, 11, 12, 25, 13, 15, 16, 17, 14, 26, 18, 19,
            20, 21, 23, 22, 24, 5, 6, 7, 2, 3, 4, 8, 9,
        )
        single_names = tuple(
            output.location_name.removeprefix(prefix)
            for output in sources["ttm_slide_single_coins"].outputs
        )
        for new_index, old_index in enumerate(single_coin_old_indices, 1):
            self.assertEqual(single_names[old_index - 1], f"Coin on the Slide {new_index}")

        line_names = tuple(
            output.location_name.removeprefix(prefix)
            for output in sources["ttm_slide_coin_lines"].outputs
        )
        for line_index in range(1, 5):
            expected_coin_indices = range(5, 0, -1) if line_index in (1, 2, 4) else range(1, 6)
            self.assertEqual(
                line_names[(line_index - 1) * 5:line_index * 5],
                tuple(
                    f"Coin Line on the Slide {line_index} Coin {coin_index}"
                    for coin_index in expected_coin_indices
                ),
            )

        self.assertEqual(
            tuple(output.location_name.removeprefix(prefix)
                  for output in sources["ttm_slide_blue_coins"].outputs),
            ("Slide Blue Coin 3", "Slide Blue Coin 2", "Slide Blue Coin 1"),
        )

    def test_bbh_first_floor_red_coin_names_and_rules_match_physical_coins(self):
        source = next(
            source for source in coin_source_catalog
            if source.course_name == "Big Boo's Haunt"
            and source.source_id == "red_coin"
        )
        self.assertEqual(
            tuple(output.location_name.removeprefix("Big Boo's Haunt - ")
                  for output in source.outputs[:4]),
            (
                "Mad Piano Red Coin",
                "Bookshelf Red Coin 1",
                "Bookshelf Red Coin 2",
                "Hole Room Red Coin",
            ),
        )
        self.assertEqual(
            tuple(output.source_methods for output in source.outputs[:4]),
            (
                ("first_floor_red_coins",),
                ("first_floor_red_coins",),
                ("first_floor_movement_red_coin",),
                ("first_floor_red_coins",),
            ),
        )


class DisabledCoinChecksTest(SM64TestBase):
    run_default_tests = False
    options = {"coin_checks": 0}

    def test_no_individual_coin_locations_are_created(self):
        self.assertEqual(self.world.coin_check_location_names, ())
        self.assertFalse(
            coin_output_by_name.keys()
            & {location.name for location in self.multiworld.get_locations(self.player)})


class FullCataloguedCoinChecksTest(SM64TestBase):
    run_default_tests = False
    options = {"coin_checks": 100, "accessibility": "minimal"}

    def test_every_currently_catalogued_output_is_created(self):
        self.assertEqual(
            set(self.world.coin_check_location_names),
            set(coin_output_by_name),
        )
        for location_name in self.world.coin_check_location_names:
            location = self.multiworld.get_location(location_name, self.player)
            self.assertIsInstance(location.access_rule, CanCollectCoinOutput.Resolved)

    def test_every_output_rule_uses_a_coinlogic_trace_source(self):
        state = self.multiworld.get_all_state(False)
        def visit(sources, method_ids):
            for source in sources:
                method_ids.add(source.source_id)
                visit(source.children, method_ids)

        available_method_ids = {}
        for course_name, evaluator in COIN_EVALUATORS.items():
            available_method_ids[course_name] = set()
            visit(evaluator(state, self.player, 1).children, available_method_ids[course_name])

        missing = {
            (output.output_id.course_name, method)
            for output in coin_output_catalog
            for method in output.source_methods
            if method not in available_method_ids[output.output_id.course_name]
        }
        self.assertEqual(missing, set())

    def test_dire_dire_docks_seafloor_clam_ring_has_a_coinlogic_explanation(self):
        location = self.multiworld.get_location(
            "Dire, Dire Docks - Sea-Floor Coin Ring by the Koopa Shell Clam Coin 1",
            self.player,
        )
        explanation = "".join(
            part.get("text", "") for part in location.access_rule.explain_json(self.multiworld.state)
        )
        self.assertNotIn("Missing CoinLogic source", explanation)

    def test_rainbow_ride_maze_red_coins_always_require_the_maze_region(self):
        state = self.multiworld.state
        state.collect(self.world.create_item("Red Coins"), prevent_sweep=True)
        state.collect(self.world.create_item("Wall Kick"), prevent_sweep=True)
        for location_name in (
                "Rainbow Ride - Red Coin Requiring Maze Movement",
                "Rainbow Ride - Other Maze Red Coin 1"):
            with self.subTest(location=location_name):
                location = self.multiworld.get_location(location_name, self.player)
                self.assertFalse(location.access_rule(state))
                explanation = "".join(
                    part.get("text", "") for part in location.access_rule.explain_json(state))
                self.assertIn("Cannot reach region Rainbow Ride - Maze", explanation)

    def test_shuffled_sub_area_outputs_are_created_in_their_physical_regions(self):
        for output in coin_output_catalog:
            expected_region = coin_output_region_name(output)
            if expected_region is None:
                continue
            with self.subTest(output=output.location_name):
                location = self.multiworld.get_location(output.location_name, self.player)
                self.assertEqual(location.parent_region.name, expected_region)

    def test_slot_data_contains_authoritative_selection(self):
        slot_data = self.world.fill_slot_data()
        self.assertEqual(set(slot_data["CoinCheckLocations"]), set(coin_output_by_name))
        self.assertNotIn("CoinOutputMap", slot_data)
        self.assertNotIn("CoinOutputMapV2", slot_data)
        self.assertNotIn("CoinOutputSelections", slot_data)
        self.assertNotIn("CoinOutputImplications", slot_data)
        self.assertNotIn("CoinOutputCatalogComplete", slot_data)
        self.assertNotIn("CoinOutputCatalogVersion", slot_data)

    def test_ut_regeneration_restores_selection_without_rerolling(self):
        selected_name = self.world.coin_check_location_names[0]
        slot_data = self.world.fill_slot_data()
        slot_data["CoinCheckLocations"] = [selected_name]
        self.multiworld.re_gen_passthrough = {self.world.game: slot_data}

        self.world.generate_early()

        self.assertEqual(self.world.coin_check_location_names, (selected_name,))


class WetDryWorldWoodenStructureCoinChecksAccessTest(SM64TestBase):
    run_default_tests = False
    options = {
        "area_rando": "off",
        "level_unlocks": "full",
        "level_features": "per_level",
        "coin_checks": 100,
        "coin_object_unlocks": "per_level",
    }

    def test_highest_water_alone_does_not_reach_block_coins(self):
        location_name = "Wet-Dry World - Wooden Structure 3-Coin Block Coin 1"
        self.run_location_tests([
            [location_name, False, ["Wet-Dry World - 3-Coin Blocks"]],
        ], starting_regions=["Wet-Dry World - Highest Water"])

    def test_mid_water_reaches_block_coins(self):
        location_name = "Wet-Dry World - Wooden Structure 3-Coin Block Coin 1"
        self.run_location_tests([
            [location_name, True, ["Wet-Dry World - 3-Coin Blocks"]],
        ], starting_regions=["Wet-Dry World - Mid Water"])


class BigBoosHauntCoinChecksAccessTest(SM64TestBase):
    run_default_tests = False
    options = {
        "coin_checks": 100,
        "coin_object_unlocks": "per_level",
        "level_unlocks": "special_only",
        "backflip": "global",
        "side_flip": "global",
        "triple_jump": "global",
        "wall_kick": "global",
    }

    def test_second_bookshelf_red_coin_requires_movement(self):
        self.collect_by_name([
            "Unlock Big Boo's Haunt",
            "Big Boo's Haunt - Red Coins",
        ])
        for location_name in (
                "Big Boo's Haunt - Mad Piano Red Coin",
                "Big Boo's Haunt - Bookshelf Red Coin 1",
                "Big Boo's Haunt - Hole Room Red Coin"):
            self.assertTrue(self.can_reach_location(location_name))

        movement_coin = "Big Boo's Haunt - Bookshelf Red Coin 2"
        self.assertFalse(self.can_reach_location(movement_coin))
        self.collect_by_name(["Side Flip"])
        self.assertTrue(self.can_reach_location(movement_coin))


class WingMarioOverTheRainbowRedCoinChecksAccessTest(SM64TestBase):
    run_default_tests = False
    options = {
        "coin_checks": 100,
        "buddy_checks": True,
        "coin_object_unlocks": "per_level",
        "cap_items": "per_level",
        "triple_jump": "global",
    }

    def test_physical_red_coin_groups_use_their_routes(self):
        red_coins = ["Wing Mario Over the Rainbow - Red Coins"]
        flight = red_coins + ["Wing Mario Over the Rainbow - Wing Cap", "Triple Jump"]
        cannon_flight = flight + ["Wing Mario Over the Rainbow - Cannon Unlock"]
        self.run_location_tests([
            ["Wing Mario Over the Rainbow - Initial Red Coin", True, red_coins],
            ["Wing Mario Over the Rainbow - Flight Path Red Coin 1", False, red_coins],
            ["Wing Mario Over the Rainbow - Flight Path Red Coin 1", True, flight],
            ["Wing Mario Over the Rainbow - Cannon Region Red Coin 1", False, flight],
            ["Wing Mario Over the Rainbow - Cannon Region Red Coin 1", True, cannon_flight],
            ["Wing Mario Over the Rainbow - Cannon Region Red Coin 4", True, cannon_flight],
        ], starting_regions=["Wing Mario Over the Rainbow"])


class ShiftingSandLandSubAreaCoinChecksAccessTest(SM64TestBase):
    run_default_tests = False
    options = {
        "coin_checks": 100,
        "coin_object_unlocks": "per_level",
        "level_unlocks": "full",
        "shifting_sand_land_coin_star_requirement": 1,
    }

    def test_pyramid_access_does_not_grant_outdoor_coin_sources(self):
        self.run_location_tests([
            ["Shifting Sand Land - Crazy Box 1 Coin 1", False,
             ["Shifting Sand Land - Crazy Boxes"]],
            ["Shifting Sand Land - Inside Pyramid Coin 1", True,
             ["Shifting Sand Land - Single Yellow Coins"]],
        ], starting_regions=["Shifting Sand Land - Pyramid"])

        state = CollectionState(self.multiworld)

        class PyramidOnlyState:
            def can_reach(self, spot, *args, **kwargs):
                return spot in {
                    "Shifting Sand Land - Pyramid",
                    "Shifting Sand Land - Coins",
                }

            def __getattr__(self, name):
                return getattr(state, name)

        for item_name in ("Shifting Sand Land - Crazy Boxes",):
            item = self.world.create_item(item_name)
            item.classification = ItemClassification.progression
            state.collect(item, prevent_sweep=True)
        evaluation = COIN_EVALUATORS["Shifting Sand Land"](
            PyramidOnlyState(), self.player, 1)
        self.assertEqual(evaluation.reachable_coins, 0)
        del evaluation, item, state


class TallTallMountainUpperCoinLineChecksAccessTest(SM64TestBase):
    run_default_tests = False
    options = {
        "coin_checks": 100,
        "coin_object_unlocks": "per_level",
        "climb": "global",
    }

    def test_first_coin_does_not_require_climb(self):
        line_item = ["Tall, Tall Mountain - Horizontal Coin Lines"]
        self.run_location_tests([
            ["Tall, Tall Mountain - Upper Vine Wall Hangable Ceiling Coin Line Coin 1",
             False, []],
            ["Tall, Tall Mountain - Upper Vine Wall Hangable Ceiling Coin Line Coin 1",
             True, line_item],
            ["Tall, Tall Mountain - Upper Vine Wall Hangable Ceiling Coin Line Coin 2",
             False, line_item],
            ["Tall, Tall Mountain - Upper Vine Wall Hangable Ceiling Coin Line Coin 2",
             True, line_item + ["Climb"]],
        ], starting_regions=["Tall, Tall Mountain - Upper"])


class TallTallMountainUpperCoinLineTrickChecksAccessTest(SM64TestBase):
    run_default_tests = False
    options = {
        "coin_checks": 100,
        "coin_object_unlocks": "per_level",
        "logic_tricks": {"Tall, Tall Mountain Coins without Climb"},
    }

    def test_no_climb_trick_reaches_remaining_coins(self):
        self.run_location_tests([
            ["Tall, Tall Mountain - Upper Vine Wall Hangable Ceiling Coin Line Coin 2",
             True, ["Tall, Tall Mountain - Horizontal Coin Lines"]],
        ], starting_regions=["Tall, Tall Mountain - Upper"])


class TickTockClockRedCoinChecksAccessTest(SM64TestBase):
    run_default_tests = False
    options = {
        "coin_checks": 100,
        "coin_object_unlocks": "per_level",
        "level_features": "per_level",
    }

    def test_stopped_time_and_spinners_are_both_required(self):
        red_coins = ["Tick Tock Clock - Red Coins"]
        spinners = ["Tick Tock Clock - Spinners"]
        self.run_location_tests([
            ["Tick Tock Clock - Red Coin 1", False, red_coins],
            ["Tick Tock Clock - Red Coin 1", False, spinners],
            ["Tick Tock Clock - Red Coin 1", True, red_coins + spinners],
            ["Tick Tock Clock - Red Coin 8", True, red_coins + spinners],
        ], starting_regions=["Tick Tock Clock Stopped"])

    def test_moving_time_cannot_reach_red_coins(self):
        self.run_location_tests([
            ["Tick Tock Clock - Red Coin 1", False,
             ["Tick Tock Clock - Red Coins", "Tick Tock Clock - Spinners"]],
            ["Tick Tock Clock - Red Coin 8", False,
             ["Tick Tock Clock - Red Coins", "Tick Tock Clock - Spinners"]],
        ], starting_regions=["Tick Tock Clock Moving"])


class BowserInTheDarkWorldCoinChecksAccessTest(SM64TestBase):
    run_default_tests = False
    options = {
        "coin_checks": 100,
        "coin_object_unlocks": "per_level",
        "level_features": "per_level",
    }

    def test_upper_slope_coins_require_purple_switches_but_moving_platform_coins_do_not(self):
        yellow_coins = ["Bowser in the Dark World - Single Yellow Coins"]
        purple_switch = ["Bowser in the Dark World - Purple Switch"]
        self.run_location_tests([
            ["Bowser in the Dark World - Moving Platform Coin 1", False, []],
            ["Bowser in the Dark World - Moving Platform Coin 1", True, yellow_coins],
            ["Bowser in the Dark World - Upper Slope Coin 1", False, yellow_coins],
            ["Bowser in the Dark World - Upper Slope Coin 1", True, yellow_coins + purple_switch],
        ], starting_regions=["Bowser in the Dark World"])


class BowserInTheFireSeaCoinChecksAccessTest(SM64TestBase):
    run_default_tests = False
    options = {
        "blocksanity": True,
        "climb": "global",
        "coin_checks": 100,
        "coin_object_unlocks": "per_level",
    }

    def test_physical_coin_routes(self):
        rings = ["Bowser in the Fire Sea - Horizontal Coin Rings"]
        red_coins = ["Bowser in the Fire Sea - Red Coins"]
        three_coin_block = ["Bowser in the Fire Sea - 3-Coin Block"]
        climb = ["Climb"]
        self.run_location_tests([
            ["Bowser in the Fire Sea - Wire Platform Coin Ring Coin 1", True, rings],
            ["Bowser in the Fire Sea - Coin Ring by the First Bully Coin 1", False, rings],
            ["Bowser in the Fire Sea - Coin Ring by the First Bully Coin 1", True, rings + climb],
            ["Bowser in the Fire Sea - Wire Platform Red Coin", True, red_coins],
            ["Bowser in the Fire Sea - Below the Lift Red Coin", False, red_coins],
            ["Bowser in the Fire Sea - Below the Lift Red Coin", True, red_coins + climb],
            ["Bowser in the Fire Sea - Seesaw Platform Red Coin", False, red_coins],
            ["Bowser in the Fire Sea - Seesaw Platform Red Coin", True, red_coins + climb],
            ["Bowser in the Fire Sea - 3-Coin Block Coin 1", False, three_coin_block],
            ["Bowser in the Fire Sea - 3-Coin Block Coin 1", True, three_coin_block + climb],
            ["Bowser in the Fire Sea - 3 Coins Block", False, three_coin_block],
            ["Bowser in the Fire Sea - 3 Coins Block", True, three_coin_block + climb],
        ], starting_regions=["Bowser in the Fire Sea"])


class BowserInTheFireSeaLavaDamageBoostingCoinChecksAccessTest(SM64TestBase):
    run_default_tests = False
    options = {
        "blocksanity": True,
        "climb": "global",
        "coin_checks": 100,
        "coin_object_unlocks": "per_level",
        "logic_tricks": {"Lava Damage Boosting"},
    }

    def test_trick_reaches_seesaw_red_coin_and_three_coin_block(self):
        self.run_location_tests([
            ["Bowser in the Fire Sea - Seesaw Platform Red Coin", True,
             ["Bowser in the Fire Sea - Red Coins"]],
            ["Bowser in the Fire Sea - 3-Coin Block Coin 1", True,
             ["Bowser in the Fire Sea - 3-Coin Block"]],
            ["Bowser in the Fire Sea - 3 Coins Block", True,
             ["Bowser in the Fire Sea - 3-Coin Block"]],
        ], starting_regions=["Bowser in the Fire Sea"])


class HazyMazeCaveSwoopCoinChecksAccessTest(SM64TestBase):
    run_default_tests = False
    options = {
        "coin_checks": 100,
        "enemy_unlocks": "per_level",
        "level_unlocks": "disabled",
        "wall_kick": "global",
        "ledge_grab": "global",
        "backflip": "global",
        "side_flip": "global",
        "triple_jump": "global",
    }

    def test_pit_island_swoop_is_initial_but_emergency_exit_swoops_need_movement(self):
        movement_items = {
            action
            for action in ("Wall Kick", "Ledge Grab", "Backflip", "Side Flip", "Triple Jump")
        } | {f"Hazy Maze Cave - {action}" for action in (
            "Wall Kick", "Ledge Grab", "Backflip", "Side Flip", "Triple Jump"
        )}
        self.collect_all_but(movement_items)
        pit_island_swoop = "Hazy Maze Cave - Pit Island Room Swoop Coin"
        emergency_exit_swoops = (
            "Hazy Maze Cave - A-Maze-Ing Emergency Exit Swoop 1 Coin",
            "Hazy Maze Cave - A-Maze-Ing Emergency Exit Swoop 2 Coin",
        )

        self.assertTrue(self.can_reach_location(pit_island_swoop))
        for location_name in emergency_exit_swoops:
            self.assertFalse(self.can_reach_location(location_name))

        self.collect_by_name(["Wall Kick"])
        for location_name in emergency_exit_swoops:
            self.assertTrue(self.can_reach_location(location_name))


class HazyMazeCaveRedCoinRoomCoinChecksAccessTest(SM64TestBase):
    run_default_tests = False
    options = {
        "coin_checks": 100,
        "coin_object_unlocks": "per_level",
        "enemy_unlocks": "per_level",
        "level_features": "per_level",
        "level_unlocks": "disabled",
        "wall_kick": "global",
        "ledge_grab": "global",
        "backflip": "global",
        "side_flip": "global",
        "triple_jump": "global",
        "climb": "global",
        "long_jump": "global",
    }

    def test_mid_and_upper_room_sources_use_their_physical_routes(self):
        lower_red_coin = "Hazy Maze Cave - Lower Red Coin 1"
        arrival_red_coin = (
            "Hazy Maze Cave - Checkerboard Platform Arrival Platform Red Coin 1")
        ride_red_coin = "Hazy Maze Cave - Checkerboard Platform Ride Red Coin 1"
        mr_i = "Hazy Maze Cave - Red Coin Room Mr. I 1 Blue Coin"
        swoop = "Hazy Maze Cave - Checkerboard Platform Ride Swoop 1 Coin"
        self.collect_by_name([
            "Progressive Key",
            "Hazy Maze Cave - Red Coins",
            "Hazy Maze Cave - Mr. Is",
            "Hazy Maze Cave - Swoops",
        ])

        self.assertFalse(self.can_reach_region("Hazy Maze Cave - Mid Red Coin Room"))
        for location_name in (lower_red_coin, arrival_red_coin, ride_red_coin, mr_i, swoop):
            self.assertFalse(self.can_reach_location(location_name))

        self.collect_by_name(["Wall Kick"])
        self.assertTrue(self.can_reach_region("Hazy Maze Cave - Mid Red Coin Room"))
        self.assertTrue(self.can_reach_location(lower_red_coin))
        self.assertTrue(self.can_reach_location(mr_i))
        self.assertFalse(self.can_reach_region("Hazy Maze Cave - Upper Red Coin Room"))

        self.collect_by_name(["Climb"])
        self.assertTrue(self.can_reach_region("Hazy Maze Cave - Upper Red Coin Room"))
        self.assertFalse(self.can_reach_location(arrival_red_coin))
        self.assertFalse(self.can_reach_location(ride_red_coin))
        self.assertFalse(self.can_reach_location(swoop))

        self.collect_by_name(["Long Jump"])
        self.assertTrue(self.can_reach_location(arrival_red_coin))
        self.assertFalse(self.can_reach_location(ride_red_coin))
        self.assertFalse(self.can_reach_location(swoop))

        self.collect_by_name(["Hazy Maze Cave - Checkerboard Platform"])
        self.assertTrue(self.can_reach_location(ride_red_coin))
        self.assertTrue(self.can_reach_location(swoop))


class HazyMazeCaveUpperRedCoinRoomTrickCoinChecksAccessTest(SM64TestBase):
    run_default_tests = False
    options = {
        **HazyMazeCaveRedCoinRoomCoinChecksAccessTest.options,
        "logic_tricks": {"Hazy Maze Cave Upper Red Coin Area with Wall Kick Only"},
    }

    def test_wall_kick_trick_reaches_upper_but_checkerboard_sources_still_require_platforms(self):
        arrival_red_coin = (
            "Hazy Maze Cave - Checkerboard Platform Arrival Platform Red Coin 1")
        ride_red_coin = "Hazy Maze Cave - Checkerboard Platform Ride Red Coin 1"
        swoop = "Hazy Maze Cave - Checkerboard Platform Ride Swoop 1 Coin"
        self.collect_by_name([
            "Progressive Key",
            "Wall Kick",
            "Long Jump",
            "Hazy Maze Cave - Red Coins",
            "Hazy Maze Cave - Swoops",
        ])

        self.assertTrue(self.can_reach_region("Hazy Maze Cave - Upper Red Coin Room"))
        self.assertTrue(self.can_reach_location(arrival_red_coin))
        self.assertFalse(self.can_reach_location(ride_red_coin))
        self.assertFalse(self.can_reach_location(swoop))

        self.collect_by_name(["Hazy Maze Cave - Checkerboard Platform"])
        self.assertTrue(self.can_reach_location(ride_red_coin))
        self.assertTrue(self.can_reach_location(swoop))


class WhompsFortressCoinChecksAccessTest(SM64TestBase):
    run_default_tests = False
    options = {
        "coin_checks": 100,
        "coin_object_unlocks": "per_level",
        "enemy_unlocks": "per_level",
        "level_unlocks": "disabled",
        "triple_jump": "global",
    }

    def test_thwomp_red_coin_requires_thwomp_or_triple_jump(self):
        location_name = "Whomp's Fortress - Thwomp Red Coin"
        self.collect_by_name(["Whomp's Fortress - Red Coins"])
        self.assertFalse(self.can_reach_location(location_name))

        self.collect_by_name(["Triple Jump"])
        self.assertTrue(self.can_reach_location(location_name))
        self.remove_by_name(["Triple Jump"])
        self.assertFalse(self.can_reach_location(location_name))

        self.collect_by_name(["Whomp's Fortress - Thwomps"])
        self.assertTrue(self.can_reach_location(location_name))


class LethalLavaLandCrossLavaCoinChecksAccessTest(SM64TestBase):
    run_default_tests = False
    options = {
        "coin_checks": 100,
        "coin_object_unlocks": "per_level",
        "level_unlocks": "disabled",
        "triple_jump": "global",
        "cap_items": "per_level",
    }

    def test_central_crescent_and_northeast_platform_require_lava_crossing(self):
        locations = (
            "Lethal Lava Land - Central Gray Crescent Coin 1",
            "Lethal Lava Land - Northeast Brown Platform Coin Line Coin 1",
        )
        for location_name in locations:
            self.run_location_tests(
                [
                    [location_name, False, [
                        "Lethal Lava Land - Single Yellow Coins",
                        "Lethal Lava Land - Horizontal Coin Lines",
                    ]],
                    [location_name, True, [
                        "Lethal Lava Land - Single Yellow Coins",
                        "Lethal Lava Land - Horizontal Coin Lines",
                        "Lethal Lava Land - Koopa Shell",
                    ]],
                    [location_name, True, [
                        "Lethal Lava Land - Single Yellow Coins",
                        "Lethal Lava Land - Horizontal Coin Lines",
                        "Lethal Lava Land - Wing Cap",
                        "Triple Jump",
                    ]],
                ],
                starting_regions=("Lethal Lava Land",),
            )


class CastleCoinChecksAccessTest(SM64TestBase):
    run_default_tests = False
    options = {
        "coin_checks": 100,
        "coin_count_checks": 100,
        "combined_progressive_keys": False,
        "coin_object_unlocks": "per_level",
        "enemy_unlocks": "per_level",
        "one_up_checks": True,
        "one_up_unlocks": "per_level",
        "triple_jump": "global",
        "side_flip": "global",
        "wall_kick": "global",
        "ground_pound": "global",
    }

    def test_castle_does_not_create_coin_count_checks(self):
        self.assertFalse(any(name.startswith("Castle - ")
                             for name in self.world.coin_count_check_location_names))

    def test_bridge_coins_use_bridge_route_and_castle_yellow_coins(self):
        coin_name = "Castle - Coin Under the Bridge 1"
        self.assertFalse(self.can_reach_location(coin_name))
        self.collect_by_name([
            "Castle - Single Yellow Coins",
            "Progressive Basement Key",
            "Ground Pound",
            "Wall Kick",
            "Side Flip",
        ])
        self.assertTrue(self.can_reach_location(coin_name))
        self.assertFalse(self.can_reach_location("Castle - Bridge Coins 1-Up"))

    def test_lobby_coins_require_castle_yellow_coins(self):
        coin_name = "Castle - Lobby Coin 1"
        self.assertFalse(self.can_reach_location(coin_name))
        self.collect_by_name(["Castle - Single Yellow Coins"])
        self.assertTrue(self.can_reach_location(coin_name))

    def test_castle_boos_require_castle_or_global_boo_item(self):
        courtyard_boo = "Castle - Courtyard Boo 1 Coin"
        self.assertFalse(self.can_reach_location(courtyard_boo))
        self.collect_by_name(["Castle - Boos"])
        self.assertTrue(self.can_reach_location(courtyard_boo))

    def test_global_boos_also_unlock_castle_courtyard_boos(self):
        courtyard_boo = "Castle - Courtyard Boo 1 Coin"
        self.collect(self.world.create_item("Boos"))
        self.assertTrue(self.can_reach_location(courtyard_boo))

    def test_big_boos_haunt_unlock_does_not_unlock_coin_boos(self):
        courtyard_boo = "Castle - Courtyard Boo 1 Coin"
        self.collect_by_name(["Unlock Big Boo's Haunt"])
        self.assertFalse(self.can_reach_location(courtyard_boo))


class FullAccessibilityImpossibleCoinChecksTest(SM64TestBase):
    run_default_tests = False
    options = {"coin_checks": 100, "accessibility": "full"}

    def test_impossible_coins_are_not_created_without_their_tricks(self):
        self.assertNotIn("Snowman's Land - Impossible Coin", self.world.coin_check_location_names)
        self.assertNotIn("Tiny-Huge Island - Impossible Coin", self.world.coin_check_location_names)


class FullAccessibilityEnabledImpossibleCoinChecksTest(SM64TestBase):
    run_default_tests = False
    options = {
        "coin_checks": 100,
        "accessibility": "full",
        "logic_tricks": {
            "Snowman's Land Impossible Coin",
            "Tiny-Huge Island Impossible Coin",
        },
    }

    def test_impossible_coins_are_created_with_their_tricks(self):
        self.assertIn("Snowman's Land - Impossible Coin", self.world.coin_check_location_names)
        self.assertIn("Tiny-Huge Island - Impossible Coin", self.world.coin_check_location_names)
