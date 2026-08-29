from BaseClasses import CollectionState
from test.general import setup_solo_multiworld
from worlds.AutoWorld import call_all

from .. import Options, SM64World
from ..Regions import SM64Levels, SM64_TTC_FAST, SM64_TTC_RANDOM, SM64_TTC_SLOW, SM64_TTC_STOPPED, \
    sm64_level_to_entrances
from ..SubAreas import CASTLE_RETURN_SOURCES, OUTGOING_SOURCES_BY_DESTINATION, RETURN_DESTINATIONS, \
    RETURN_SOURCES, SUB_AREA_SOURCES, SUB_AREA_SOURCE_NAMES, normal_source_id, sub_area_source_by_id
from .bases import SM64TestBase


class SeparateSubAreaShuffleTest(SM64TestBase):
    run_default_tests = False
    options = {
        "area_rando": Options.AreaRandomizer.option_Off,
        "sub_area_shuffle": Options.SubAreaShuffle.option_separate,
    }

    def test_separate_map_contains_only_physical_sub_area_sources(self):
        source_ids = set(self.world.sub_area_slot_data)
        expected_ids = {
            source.source_id for source in (*SUB_AREA_SOURCES.values(), *RETURN_SOURCES.values())
        }
        self.assertEqual(source_ids, expected_ids)
        self.assertFalse(any(source_id >= 1000 for source_id in source_ids))

    def test_ccm_slide_exit_uses_the_exterior_side_of_the_door(self):
        destination = RETURN_DESTINATIONS["ccm_cabin"]
        self.assertEqual(destination.region, "Cool, Cool Mountain - Slide Exit")
        self.assertEqual(destination.warp_arg, 6)
        self.assertEqual((destination.packed >> 28) & 0x0F, 6)

    def test_sl_igloo_exit_reaches_the_igloo_entrance_region(self):
        destination = RETURN_DESTINATIONS["sl_main"]
        self.assertEqual(destination.region, "Snowman's Land - Igloo Entrance")
        self.assertEqual(destination.node, 0x0B)

    def test_slip_slidin_away_is_at_the_slide_exit(self):
        location = self.multiworld.get_location(
            "Cool, Cool Mountain - Slip Slidin' Away", self.player)
        self.assertEqual(location.parent_region.name, "Cool, Cool Mountain - Slide Exit")
        self.assertTrue(any(
            entrance.connected_region.name == "Cool, Cool Mountain"
            for entrance in location.parent_region.exits
        ))

    def test_bowser_in_the_sky_source_can_extend_hint_information(self):
        self.world.area_connections[int(SM64Levels.BOWSER_IN_THE_SKY)] = int(
            SM64Levels.BOB_OMB_BATTLEFIELD)
        hint_data = {}

        self.world.extend_hint_information(hint_data)

        bob_location = self.multiworld.get_location(
            "Bob-omb Battlefield - Big Bob-Omb on the Summit", self.player)
        self.assertEqual(hint_data[self.player][bob_location.address], "Bowser in the Sky")

    def test_thi_combined_hint_accepts_a_physical_sub_area_source(self):
        for source, destination in tuple(self.world.area_connections.items()):
            if destination in {
                int(SM64Levels.TINY_HUGE_ISLAND_TINY),
                int(SM64Levels.TINY_HUGE_ISLAND_HUGE),
            }:
                del self.world.area_connections[source]
        self.world.area_connections[int(SM64Levels.BOWSER_IN_THE_SKY)] = int(
            SM64Levels.TINY_HUGE_ISLAND_HUGE)
        self.world.area_connections["ccm_slide"] = int(SM64Levels.TINY_HUGE_ISLAND_TINY)
        hint_data = {}

        self.world.extend_hint_information(hint_data)

        thi_location = self.multiworld.get_location(
            "Tiny-Huge Island - Rematch with Koopa the Quick", self.player)
        self.assertEqual(
            hint_data[self.player][thi_location.address],
            "Bowser in the Sky or Cool, Cool Mountain - Chimney",
        )


class MixedSubAreaShuffleTest(SM64TestBase):
    run_default_tests = False
    options = {
        "area_rando": Options.AreaRandomizer.option_Off,
        "sub_area_shuffle": Options.SubAreaShuffle.option_mixed,
    }

    def test_mixed_map_is_complete_and_forces_bowser_three_after_a_branch(self):
        self.assertEqual(len(self.world.area_connections), 46)
        bits_destination = self.world.area_connections[int(SM64Levels.BOWSER_IN_THE_SKY)]
        destination_name = sm64_level_to_entrances.get(bits_destination, bits_destination)
        self.assertIn(destination_name, OUTGOING_SOURCES_BY_DESTINATION)
        self.assertTrue(any(
            self.world.area_connections[source] == "bowser_3"
            for source in OUTGOING_SOURCES_BY_DESTINATION[destination_name]
        ))

    def test_mixed_map_is_authoritative_in_slot_data(self):
        slot_data = self.world.fill_slot_data()
        self.assertEqual(slot_data["AreaConnections"], self.world.area_connections)
        self.assertNotIn("SubAreaConnections", slot_data)
        self.assertEqual(slot_data["SubAreaRando"], self.world.sub_area_slot_data)

    def test_course_entrance_explanation_handles_mixed_sources(self):
        messages = self.world.explain_rule(
            "Shifting Sand Land", CollectionState(self.multiworld))
        explanation = "".join(part.get("text", "") for part in messages)

        self.assertIn("Shifting Sand Land entrances:", explanation)
        self.assertIn("Shifting Sand Land", explanation)
        self.assertIn("the lower Shifting Sand Land pyramid", explanation)
        self.assertIn("the upper Shifting Sand Land pyramid", explanation)

    def test_spoiler_uses_the_authoritative_map_and_friendly_names(self):
        self.assertEqual(
            len(self.multiworld.spoiler.entrances),
            len(self.world.shuffled_entrance_source_ids),
        )
        for source_id in self.world.shuffled_entrance_source_ids:
            physical_source = sub_area_source_by_id(source_id)
            source_key = physical_source.key if physical_source else source_id
            source_name = (
                SUB_AREA_SOURCE_NAMES[source_key] if physical_source else
                self.world.get_normal_entrance_source_name(source_id)
            )
            spoiler_entry = self.multiworld.spoiler.entrances[(source_name, "entrance", 1)]
            self.assertEqual(
                spoiler_entry["exit"],
                self.world.get_entrance_destination_name(
                    self.world.area_connections[source_key]),
            )
            self.assertNotIn("thi_red_cave_exit", spoiler_entry["entrance"])
            self.assertNotIn("thi_red_cave_exit", spoiler_entry["exit"])

    def test_user_facing_entrance_names(self):
        expected_normal_names = {
            int(SM64Levels.TINY_HUGE_ISLAND_TINY): "Tiny Island Entrance",
            int(SM64Levels.TINY_HUGE_ISLAND_HUGE): "Huge Island Entrance",
            SM64_TTC_STOPPED: "Tick Tock Clock 12 O'Clock Entrance",
            SM64_TTC_SLOW: "Tick Tock Clock 3 O'Clock Entrance",
            SM64_TTC_RANDOM: "Tick Tock Clock 6 O'Clock Entrance",
            SM64_TTC_FAST: "Tick Tock Clock 9 O'Clock Entrance",
        }
        for source_id, expected_name in expected_normal_names.items():
            with self.subTest(source_id=source_id):
                self.assertEqual(
                    self.world.get_normal_entrance_source_name(source_id), expected_name)

        self.assertEqual(
            SUB_AREA_SOURCE_NAMES["jrb_ship"],
            "Jolly Roger Bay - Sunken Ship Entrance",
        )
        self.assertEqual(
            SUB_AREA_SOURCE_NAMES["hmc_cotmc"],
            "Hazy Maze Cave - Cavern of the Metal Cap Entrance",
        )

    def test_ut_regeneration_restores_sub_area_map(self):
        slot_data = self.world.fill_slot_data()
        expected_connections = self.world.area_connections.copy()
        expected_warps = self.world.sub_area_slot_data.copy()
        self.multiworld.re_gen_passthrough = {self.world.game: slot_data}

        self.world.generate_early()

        self.assertEqual(self.world.area_connections, expected_connections)
        self.assertEqual(self.world.sub_area_slot_data, expected_warps)

    def test_ut_regeneration_can_set_rules_from_mixed_map(self):
        slot_data = self.world.fill_slot_data()
        tracker_multiworld = setup_solo_multiworld(SM64World, steps=(), seed=7)
        tracker_multiworld.re_gen_passthrough = {self.world.game: slot_data}
        tracker_multiworld.generation_is_fake = True
        tracker_multiworld.enforce_deferred_connections = "on"

        for step in ("generate_early", "create_regions", "create_items", "set_rules"):
            call_all(tracker_multiworld, step)

        tracker_world = tracker_multiworld.worlds[1]
        self.assertEqual(tracker_world.area_connections, self.world.area_connections)
        self.assertIn(
            int(SM64Levels.BOWSER_IN_THE_SKY),
            tracker_world.randomized_entrance_connections,
        )

    def test_bowser_in_the_sky_uses_its_castle_source_and_level_ids(self):
        source_id = int(SM64Levels.BOWSER_IN_THE_SKY)
        self.assertEqual(source_id, 211)
        self.assertIn(normal_source_id(source_id), self.world.sub_area_slot_data)
        bits_source = next(
            source_key for source_key, destination_key in self.world.area_connections.items()
            if destination_key == int(SM64Levels.BOWSER_IN_THE_SKY)
        )
        packed_destination = self.world.sub_area_slot_data[
            normal_source_id(int(bits_source))
        ]
        self.assertEqual((packed_destination >> 16) & 0xFF, 21)

    def test_ut_reconnects_a_low_physical_source_bit(self):
        world = self._create_fake_tracker_world(Options.SubAreaShuffle.option_mixed)
        source_id = SUB_AREA_SOURCES["ccm_slide"].source_id
        self.assertIsNone(world.randomized_entrance_connections[source_id].connected_region)

        world.reconnect_found_entrances("SM64SpicyFoundSubAreaEntrancesLow_1", 1 << (source_id - 1))

        self.assertIsNotNone(world.randomized_entrance_connections[source_id].connected_region)
        self.assertTrue(all(
            entrance.connected_region is None
            for other_id, entrance in world.randomized_entrance_connections.items()
            if other_id != source_id
        ))

    @staticmethod
    def _create_fake_tracker_world(sub_area_mode):
        multiworld = setup_solo_multiworld(
            SM64World,
            steps=("generate_early", "create_regions", "create_items"),
            seed=7,
        )
        world = multiworld.worlds[1]
        world.options.sub_area_shuffle.value = sub_area_mode
        multiworld.generation_is_fake = True
        multiworld.enforce_deferred_connections = "on"
        call_all(multiworld, "set_rules")
        return world


class MixedCastleReturnSubAreaShuffleTest(SM64TestBase):
    run_default_tests = False
    options = {
        "area_rando": Options.AreaRandomizer.option_Off,
        "sub_area_shuffle": Options.SubAreaShuffle.option_mixed_plus_castle_returns,
    }

    def test_castle_return_sources_are_included(self):
        self.assertEqual(len(self.world.area_connections), 52)
        for source in CASTLE_RETURN_SOURCES.values():
            self.assertIn(source.source_id, self.world.sub_area_slot_data)

    def test_ut_reconnects_a_high_physical_source_bit(self):
        world = MixedSubAreaShuffleTest._create_fake_tracker_world(
            Options.SubAreaShuffle.option_mixed_plus_castle_returns)
        source_id = CASTLE_RETURN_SOURCES["vcutm_fall"].source_id
        self.assertIsNone(world.randomized_entrance_connections[source_id].connected_region)

        world.reconnect_found_entrances("SM64SpicyFoundSubAreaEntrancesHigh_1", 1 << (source_id - 32))

        self.assertIsNotNone(world.randomized_entrance_connections[source_id].connected_region)
        self.assertTrue(all(
            entrance.connected_region is None
            for other_id, entrance in world.randomized_entrance_connections.items()
            if other_id != source_id
        ))
