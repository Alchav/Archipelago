import unittest

from BaseClasses import CollectionState, ItemClassification
from Fill import distribute_items_restrictive
from test.general import setup_multiworld, setup_solo_multiworld
from worlds.AutoWorld import call_all

from .. import SM64World
from ..Items import global_sign_unlock_item_data_table, per_level_sign_unlock_item_data_table, sign_unlock_item_names
from ..Options import SignUnlocks
from ..Regions import sm64_entrance_destination_descriptions, \
    sm64_entrance_source_descriptions, sm64_shuffled_entrance_ids
from ..Signs import fallback_hints, joke_hints, sign_data, tip_hints


class SignHintTest(unittest.TestCase):
    def test_sign_metadata_and_fallbacks_are_complete(self):
        self.assertEqual(len(sign_data), 91)
        self.assertEqual(len({sign.key for sign in sign_data}), 91)
        self.assertEqual(len({sign.location_name for sign in sign_data}), 91)
        self.assertGreaterEqual(len(joke_hints), 91)
        self.assertGreater(len(tip_hints), 0)
        self.assertEqual(len(fallback_hints), len(set(fallback_hints)))

    def test_sign_locations_are_filler_events_and_budget_is_twenty_percent(self):
        multiworld = setup_solo_multiworld(
            SM64World,
            steps=("generate_early", "create_regions", "create_items", "set_rules"),
            seed=1,
        )
        world = multiworld.worlds[1]
        sign_locations = [
            multiworld.get_location(sign.location_name, 1)
            for sign in sign_data
        ]

        self.assertTrue(all(location.address is None for location in sign_locations))
        self.assertTrue(all(location.locked for location in sign_locations))
        self.assertTrue(all(not location.show_in_spoiler for location in sign_locations))
        self.assertTrue(all(location.item.code is None for location in sign_locations))
        self.assertTrue(all(location.item.classification == ItemClassification.filler
                            for location in sign_locations))

        advancement_count = sum(item.advancement for item in multiworld.itempool if item.player == 1)
        entrance_count = len(world.get_shuffled_entrance_source_ids())
        self.assertEqual(world.sign_hint_count, min(91, (advancement_count + entrance_count) // 5))

    def test_castle_courtyard_signs_are_in_the_courtyard_region(self):
        multiworld = setup_solo_multiworld(
            SM64World,
            steps=("generate_early", "create_regions"),
            seed=1,
        )
        courtyard_signs = [sign for sign in sign_data if sign.area == "Castle Courtyard"]

        self.assertEqual(len(courtyard_signs), 4)
        self.assertTrue(all(
            multiworld.get_location(sign.location_name, 1).parent_region.name == "Castle Courtyard"
            for sign in courtyard_signs
        ))

    def test_global_sign_item_gates_sign_events_and_is_not_counted_for_hint_budget(self):
        multiworld = setup_multiworld(
            SM64World,
            steps=("generate_early", "create_regions", "create_items", "set_rules"),
            options={"sign_unlocks": SignUnlocks.option_global},
        )
        world = multiworld.worlds[1]
        state = CollectionState(multiworld)
        location = multiworld.get_location(sign_data[0].location_name, 1)
        advancement_without_signs = sum(
            item.advancement for item in multiworld.itempool
            if item.player == 1 and item.name not in sign_unlock_item_names
        )

        self.assertFalse(location.can_reach(state))
        state.collect(world.create_item("Signs"), True)
        self.assertTrue(location.can_reach(state))
        self.assertEqual(world.sign_hint_count, advancement_without_signs // 5)
        self.assertEqual(len([item for item in multiworld.itempool if item.name == "Signs"]), 1)

    def test_per_level_sign_items_gate_only_their_areas(self):
        multiworld = setup_multiworld(
            SM64World,
            steps=("generate_early", "create_regions", "create_items", "set_rules"),
            options={"sign_unlocks": SignUnlocks.option_per_level},
        )
        world = multiworld.worlds[1]
        state = CollectionState(multiworld)
        castle_sign = multiworld.get_location(sign_data[0].location_name, 1)
        jrb_sign_data = next(sign for sign in sign_data if sign.area == "Jolly Roger Bay")
        jrb_sign = multiworld.get_location(jrb_sign_data.location_name, 1)

        state.collect(world.create_item("Castle - Signs"), True)
        self.assertTrue(castle_sign.can_reach(state))
        self.assertFalse(jrb_sign.can_reach(state))
        state.collect(world.create_item("Jolly Roger Bay - Signs"), True)
        self.assertTrue(jrb_sign.can_reach(state))
        self.assertEqual(
            {item.name for item in multiworld.itempool if item.name in sign_unlock_item_names},
            set(per_level_sign_unlock_item_data_table),
        )
        self.assertFalse(any(item.name in global_sign_unlock_item_data_table for item in multiworld.itempool))

    def test_both_sign_item_forms_are_generated_and_either_unlocks_signs(self):
        multiworld = setup_multiworld(
            SM64World,
            steps=("generate_early", "create_regions", "create_items", "set_rules"),
            options={"sign_unlocks": SignUnlocks.option_both},
        )
        world = multiworld.worlds[1]
        state = CollectionState(multiworld)
        castle_sign = multiworld.get_location(sign_data[0].location_name, 1)

        self.assertEqual(
            {item.name for item in multiworld.itempool if item.name in sign_unlock_item_names},
            set(global_sign_unlock_item_data_table) | set(per_level_sign_unlock_item_data_table),
        )
        state.collect(world.create_item("Signs"), True)
        self.assertTrue(castle_sign.can_reach(state))

    def test_shuffled_entrances_are_counted_before_calculating_hint_budget(self):
        multiworld = setup_multiworld(
            SM64World,
            steps=("generate_early", "create_regions", "create_items"),
            seed=1,
            options={"main_course_shuffle": 2, "secret_course_shuffle": 2},
        )
        world = multiworld.worlds[1]
        advancement_count = sum(item.advancement for item in multiworld.itempool if item.player == 1)
        entrance_count = len(world.get_shuffled_entrance_source_ids())

        self.assertGreater(entrance_count, 0)
        self.assertEqual(world.sign_hint_count, min(91, (advancement_count + entrance_count) // 5))

    def test_real_hints_use_same_or_later_sphere_items_without_reuse(self):
        multiworld = setup_solo_multiworld(SM64World, seed=2)
        distribute_items_restrictive(multiworld)
        world = multiworld.worlds[1]

        spheres = []
        for sphere in multiworld.get_spheres():
            if not sphere:
                break
            spheres.append(sphere)
        sphere_by_location = {
            location: sphere_index
            for sphere_index, sphere in enumerate(spheres)
            for location in sphere
        }
        candidate_by_hint = {
            f"{location.item.name} is at {location.name}.": location
            for location in multiworld.get_filled_locations()
            if location.item.player == 1
            and location.item.advancement
            and location.item.code is not None
            and location.address is not None
        }

        SM64World.stage_pre_output(multiworld)

        item_hints = {
            key: text for key, text in world.sign_hints.items()
            if text in candidate_by_hint
        }
        entrance_hints = {
            key: text for key, text in world.sign_hints.items()
            if world.sign_hint_entrances.get(key, 0)
        }
        self.assertEqual(len(item_hints) + len(entrance_hints), world.sign_hint_count)
        self.assertEqual(
            len(set((*item_hints.values(), *entrance_hints.values()))),
            world.sign_hint_count,
        )
        for sign_key, hint in item_hints.items():
            sign = next(sign for sign in sign_data if sign.key == sign_key)
            sign_location = multiworld.get_location(sign.location_name, 1)
            item_location = candidate_by_hint[hint]
            self.assertGreaterEqual(
                sphere_by_location[item_location],
                sphere_by_location[sign_location],
            )
            self.assertEqual(world.sign_hint_locations[sign_key], item_location.address)
            self.assertEqual(world.sign_hint_location_players[sign_key], item_location.player)

        for sign_key, hint in entrance_hints.items():
            source_id = world.sign_hint_entrances[sign_key]
            destination_id = world.area_connections[source_id]
            self.assertEqual(
                hint,
                f"{sm64_entrance_destination_descriptions[destination_id]} is at "
                f"{sm64_entrance_source_descriptions[source_id]}.",
            )
            self.assertEqual(world.sign_hint_locations[sign_key], 0)
            self.assertEqual(world.sign_hint_location_players[sign_key], 0)

        self.assertEqual(set(world.sign_hints), {sign.key for sign in sign_data})
        self.assertFalse(any(world.sign_hint_entrances.values()))
        slot_data = world.fill_slot_data()["SignHintData"]
        self.assertEqual(len(slot_data), 91)
        for sign in sign_data:
            self.assertEqual(
                slot_data[str(sign.level * 256 + sign.dialog)],
                [
                    world.sign_hints[sign.key],
                    world.sign_hint_locations[sign.key],
                    world.sign_hint_entrances[sign.key],
                    world.sign_hint_location_players[sign.key],
                ],
            )

    def test_cross_player_item_hints_record_the_location_owner(self):
        multiworld = setup_multiworld([SM64World, SM64World], seed=17)
        distribute_items_restrictive(multiworld)
        SM64World.stage_pre_output(multiworld)

        for player in (1, 2):
            world = multiworld.worlds[player]
            foreign_hint_keys = [
                key for key, location in world.sign_hint_locations.items()
                if location and world.sign_hint_location_players[key] != player
            ]
            self.assertTrue(foreign_hint_keys)

            slot_data = world.fill_slot_data()["SignHintData"]
            for key in foreign_hint_keys:
                sign = next(sign for sign in sign_data if sign.key == key)
                self.assertEqual(
                    slot_data[str(sign.level * 256 + sign.dialog)][3],
                    world.sign_hint_location_players[key],
                )

    def test_deferred_entrances_reconnect_from_discovery_bitset(self):
        multiworld = setup_solo_multiworld(
            SM64World,
            steps=("generate_early", "create_regions", "create_items"),
            seed=3,
        )
        multiworld.worlds[1].options.main_course_shuffle.value = 2
        multiworld.worlds[1].options.secret_course_shuffle.value = 2
        multiworld.generation_is_fake = True
        multiworld.enforce_deferred_connections = "on"
        call_all(multiworld, "set_rules")
        world = multiworld.worlds[1]

        first_entrance_id = next(iter(world.randomized_entrance_connections))
        first_entrance = world.randomized_entrance_connections[first_entrance_id]
        self.assertIsNone(first_entrance.connected_region)

        world.reconnect_found_entrances("SM64SpicyFoundEntrances_1", 1)
        self.assertIsNotNone(first_entrance.connected_region)
        self.assertTrue(all(
            entrance.connected_region is None
            for entrance_id, entrance in world.randomized_entrance_connections.items()
            if entrance_id != first_entrance_id
        ))

    def test_discovered_entrance_has_glitched_logic_bypass(self):
        multiworld = setup_solo_multiworld(
            SM64World,
            steps=("generate_early", "create_regions", "create_items"),
            seed=5,
        )
        multiworld.worlds[1].options.main_course_shuffle.value = 2
        multiworld.worlds[1].options.secret_course_shuffle.value = 2
        multiworld.generation_is_fake = True
        multiworld.enforce_deferred_connections = "on"
        call_all(multiworld, "set_rules")
        world = multiworld.worlds[1]

        entrance_id = 141  # Tick Tock Clock stopped-time source on the normally inaccessible third floor.
        entrance_bit = sm64_shuffled_entrance_ids.index(entrance_id)
        target = world.deferred_entrance_targets[entrance_id]
        world.reconnect_found_entrances("SM64SpicyFoundEntrances_1", 1 << entrance_bit)

        state = CollectionState(multiworld)
        state.allow_partial_entrances = True
        self.assertFalse(target.can_reach(state))
        state.collect(world.create_item("Glitched Logic"), prevent_sweep=True)
        self.assertTrue(target.can_reach(state))
        self.assertIsNotNone(world.randomized_entrance_connections[entrance_id].connected_region)

    def test_discovered_in_logic_entrance_does_not_get_glitched_logic_bypass(self):
        multiworld = setup_solo_multiworld(
            SM64World,
            steps=("generate_early", "create_regions", "create_items"),
            seed=6,
        )
        multiworld.worlds[1].options.main_course_shuffle.value = 2
        multiworld.worlds[1].options.secret_course_shuffle.value = 2
        multiworld.generation_is_fake = True
        multiworld.enforce_deferred_connections = "on"
        call_all(multiworld, "set_rules")
        world = multiworld.worlds[1]

        entrance_id = 91  # Bob-omb Battlefield source in the accessible Castle Lobby.
        entrance_bit = sm64_shuffled_entrance_ids.index(entrance_id)
        multiworld.state.allow_partial_entrances = True
        self.assertTrue(world.randomized_entrance_connections[entrance_id].can_reach(multiworld.state))

        world.reconnect_found_entrances("SM64SpicyFoundEntrances_1", 1 << entrance_bit)

        self.assertNotIn(entrance_id, world.bypass_entrance_connections)

    def test_courses_only_does_not_defer_secret_entrances(self):
        multiworld = setup_solo_multiworld(
            SM64World,
            steps=("generate_early", "create_regions", "create_items"),
            seed=4,
        )
        multiworld.worlds[1].options.main_course_shuffle.value = 1
        multiworld.generation_is_fake = True
        multiworld.enforce_deferred_connections = "on"
        call_all(multiworld, "set_rules")
        world = multiworld.worlds[1]

        self.assertIsNone(world.randomized_entrance_connections[91].connected_region)
        self.assertIsNotNone(world.randomized_entrance_connections[271].connected_region)


if __name__ == "__main__":
    unittest.main()
