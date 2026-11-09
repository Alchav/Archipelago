import unittest

from test.general import setup_multiworld

from .. import PokemonRedWorld, PokemonYellowWorld
from ..regions import (PokemonRBWarp, discover_mapped_region_groups, get_mapped_indoor_region_groups,
                       mapped_outdoor_region_groups, outdoor_map, saffron_gym_warps, silph_co_warps,
                       silph_co_warp_tile_regions)


SAFFRON_GYM_REGIONS = {
    "Saffron Gym-NW",
    "Saffron Gym-W",
    "Saffron Gym-SW",
    "Saffron Gym-N",
    "Saffron Gym-C",
    "Saffron Gym-S",
    "Saffron Gym-NE",
    "Saffron Gym-E",
    "Saffron Gym-SE",
}


class TestSafariSafeDestinations(unittest.TestCase):
    def test_sealed_position_cycle_is_rejected(self) -> None:
        from ..regions import DoorShuffleException, validate_mapped_position_graph
        with self.assertRaisesRegex(DoorShuffleException, "seals mapped positions"):
            validate_mapped_position_graph(
                {"start": {"house"}, "house": {"start"}, "a": {"b"}, "b": {"a"}}, {"start"})

    def test_reachable_one_way_positions_are_allowed(self) -> None:
        from ..regions import validate_mapped_position_graph
        validate_mapped_position_graph({"start": {"a"}, "a": {"b"}, "b": set()}, {"start"})

    def test_fly_escape_backyards_are_not_safe_destinations(self) -> None:
        from ..regions import insanity_safe_rooms, pokemarts, safe_rooms
        unsafe = {
            "Cerulean City-Badge House Backyard to Cerulean Badge House",
            "Fuchsia City-Good Rod House Backyard to Fuchsia Good Rod House",
        }
        for pool in (safe_rooms, insanity_safe_rooms, pokemarts):
            self.assertFalse(unsafe.intersection(pool))


class TestMappedDoorShuffleRegionGroups(unittest.TestCase):
    player = 1

    def setUp(self) -> None:
        self.multiworld = setup_multiworld(
            PokemonRedWorld,
            steps=("generate_early", "create_regions"),
            seed=0,
            options={"door_shuffle": "off"},
        )

    def get_entrances(self, entrance_names):
        return [self.multiworld.get_entrance(entrance_name, self.player) for entrance_name in entrance_names]

    def test_fly_escape_does_not_merge_backyard_with_city(self) -> None:
        for backyard, city in (("Fuchsia City-Good Rod House Backyard", "Fuchsia City"),
                               ("Cerulean City-Badge House Backyard", "Cerulean City")):
            with self.subTest(backyard=backyard):
                source = self.multiworld.get_region(backyard, self.player)
                target = self.multiworld.get_region(city, self.player)
                fly = self.multiworld.get_entrance(f"{backyard} to {city}", self.player)
                self.assertIs(fly.connected_region, target)
                self.assertFalse(fly.group_for_mapping)
                warps = [PokemonRBWarp(self.player, f"test {region.name}", region, 0, 0, "")
                         for region in (source, target)]
                groups = discover_mapped_region_groups(self.multiworld, self.player, warps)
                self.assertEqual(2, len(groups))
                self.assertFalse(any(source in group["static_regions"]
                                     and target in group["static_regions"] for group in groups))

    def get_warp_entrances(self):
        world = self.multiworld.worlds[self.player]
        warp_names = [
            entrance_data.get("name", f"{region_name} to {entrance_data['to']['map']}")
            for region_name, region_entrances in world.warp_data.items()
            for entrance_data in region_entrances
        ]
        return self.get_entrances(warp_names)

    @staticmethod
    def region_names(region_group):
        return {region.name for region in region_group["regions"]}

    @staticmethod
    def find_group_containing(region_groups, region_name):
        for region_group in region_groups:
            if region_name in TestMappedDoorShuffleRegionGroups.region_names(region_group):
                return region_group
        raise AssertionError(f"No mapped region group contains {region_name}.")

    def test_saffron_gym_is_one_dead_end_group_when_warp_tiles_are_not_mixed(self) -> None:
        shuffleable_warps = self.get_entrances([
            "Saffron City-G to Saffron Gym-S",
            "Saffron Gym-S to Saffron City-G",
        ])

        region_groups = discover_mapped_region_groups(
            self.multiworld, self.player, shuffleable_warps, blocked_warps=shuffleable_warps)
        saffron_gym_group = self.find_group_containing(region_groups, "Saffron Gym-S")

        self.assertEqual(SAFFRON_GYM_REGIONS, self.region_names(saffron_gym_group))
        self.assertEqual(
            ["Saffron Gym-S to Saffron City-G"],
            [warp.name for warp in saffron_gym_group["warps"]],
        )

    def test_saffron_gym_is_split_when_warp_tiles_are_mixed(self) -> None:
        multiworld = setup_multiworld(
            PokemonRedWorld,
            steps=("generate_early", "create_regions"),
            seed=0,
            options={"door_shuffle": "off", "warp_tile_shuffle": "mixed"},
        )
        shuffleable_warps = [
            multiworld.get_entrance(entrance_name, self.player)
            for entrance_name in [
                "Saffron City-G to Saffron Gym-S",
                "Saffron Gym-S to Saffron City-G",
                *saffron_gym_warps,
            ]
        ]

        region_groups = discover_mapped_region_groups(
            multiworld, self.player, shuffleable_warps, blocked_warps=shuffleable_warps)
        saffron_gym_group = self.find_group_containing(region_groups, "Saffron Gym-S")

        self.assertEqual({"Saffron Gym-S"}, self.region_names(saffron_gym_group))
        self.assertCountEqual(
            ["Saffron Gym-S to Saffron City-G", "Saffron Gym-S to Saffron Gym-SE"],
            [warp.name for warp in saffron_gym_group["warps"]],
        )

    def test_non_mixed_warp_tile_shuffle_merges_warp_tile_regions(self) -> None:
        multiworld = setup_multiworld(
            PokemonRedWorld,
            steps=("generate_early", "create_regions"),
            seed=0,
            options={"door_shuffle": "off", "warp_tile_shuffle": "shuffle"},
        )
        warp_tile_warps = [
            multiworld.get_entrance(entrance_name, self.player)
            for entrance_name in [*saffron_gym_warps, *silph_co_warps]
        ]

        region_groups = discover_mapped_region_groups(
            multiworld, self.player, warp_tile_warps, blocked_warps=[])
        saffron_gym_group = self.find_group_containing(region_groups, "Saffron Gym-S")
        silph_co_group = self.find_group_containing(region_groups, "Silph Co 4F")

        self.assertEqual(SAFFRON_GYM_REGIONS, self.region_names(saffron_gym_group))
        self.assertTrue(set(silph_co_warp_tile_regions).issubset(self.region_names(silph_co_group)))
        self.assertIn("Silph Co 7F", self.region_names(silph_co_group))

    def test_mapped_region_groups_follow_one_way_static_edges_backwards(self) -> None:
        shuffleable_warps = self.get_entrances([
            "Rocket Hideout B1F to Rocket Hideout B2F",
            "Rocket Hideout B1F to Celadon Game Corner-Hidden Stairs",
            "Rocket Hideout B1F-SE to Rocket Hideout Elevator-B1F",
        ])
        blocked_warps = self.get_warp_entrances()

        region_groups = discover_mapped_region_groups(
            self.multiworld, self.player, shuffleable_warps, blocked_warps=blocked_warps,
            include_outdoor_regions=False)
        rocket_hideout_group = self.find_group_containing(region_groups, "Rocket Hideout B1F")

        self.assertIn("Rocket Hideout B1F-SE", self.region_names(rocket_hideout_group))
        self.assertCountEqual(
            [
                "Rocket Hideout B1F to Rocket Hideout B2F",
                "Rocket Hideout B1F to Celadon Game Corner-Hidden Stairs",
                "Rocket Hideout B1F-SE to Rocket Hideout Elevator-B1F",
            ],
            [warp.name for warp in rocket_hideout_group["warps"]],
        )

    def test_fixed_connections_join_different_authored_groups(self) -> None:
        source = self.multiworld.get_region("Viridian Nickname House", self.player)
        target = self.multiworld.get_region("Route 2 Trade House", self.player)
        from BaseClasses import Entrance
        fixed_edge = Entrance(self.player, "Fixed passage between rooms", source)
        source.exits.append(fixed_edge)
        fixed_edge.connect(target)
        warps = self.get_entrances([
            "Viridian Nickname House to Viridian City",
            "Route 2 Trade House to Route 2-NE",
        ])
        groups = discover_mapped_region_groups(
            self.multiworld, self.player, warps,
            blocked_warps=self.get_warp_entrances(), include_outdoor_regions=False)
        group = self.find_group_containing(groups, source.name)
        self.assertIn(target.name, self.region_names(group))

    def test_fixed_passage_without_warps_joins_door_regions(self) -> None:
        from BaseClasses import Entrance, Region
        source = self.multiworld.get_region("Viridian Nickname House", self.player)
        target = self.multiworld.get_region("Route 2 Trade House", self.player)
        passage = Region("Rock Tunnel 1F-Generated passage", self.player, self.multiworld)
        second_passage = Region("Rock Tunnel 1F-Second generated passage", self.player, self.multiworld)
        self.multiworld.regions.append(passage)
        self.multiworld.regions.append(second_passage)
        for start, end in ((source, passage), (passage, second_passage), (second_passage, target)):
            edge = Entrance(self.player, f"{start.name} passage to {end.name}", start)
            start.exits.append(edge)
            edge.connect(end)
        warps = self.get_entrances([
            "Viridian Nickname House to Viridian City",
            "Route 2 Trade House to Route 2-NE",
        ])
        groups = discover_mapped_region_groups(
            self.multiworld, self.player, warps,
            blocked_warps=self.get_warp_entrances(), include_outdoor_regions=False)
        group = self.find_group_containing(groups, source.name)
        self.assertIn(target.name, self.region_names(group))
        self.assertIn(passage, group["static_regions"])
        self.assertIn(second_passage, group["static_regions"])

    def test_mapped_region_groups_do_not_merge_through_shared_one_way_dead_end(self) -> None:
        shuffleable_warps = self.get_entrances([
            "Seafoam Islands 1F to Route 20-IE",
            "Seafoam Islands 1F-SE to Route 20-IW",
        ])
        blocked_warps = self.get_warp_entrances()

        region_groups = discover_mapped_region_groups(
            self.multiworld, self.player, shuffleable_warps, blocked_warps=blocked_warps,
            include_outdoor_regions=False)
        seafoam_1f_group = self.find_group_containing(region_groups, "Seafoam Islands 1F")
        seafoam_1f_se_group = self.find_group_containing(region_groups, "Seafoam Islands 1F-SE")

        self.assertIsNot(seafoam_1f_group, seafoam_1f_se_group)
        self.assertEqual(
            ["Seafoam Islands 1F to Route 20-IE"],
            [warp.name for warp in seafoam_1f_group["warps"]],
        )
        self.assertEqual(
            ["Seafoam Islands 1F-SE to Route 20-IW"],
            [warp.name for warp in seafoam_1f_se_group["warps"]],
        )

    def test_mapped_region_group_regions_have_warps_or_outgoing_group_connections(self) -> None:
        for world_type in (PokemonRedWorld, PokemonYellowWorld):
            with self.subTest(world=world_type.game):
                multiworld = setup_multiworld(
                    world_type,
                    steps=("generate_early", "create_regions"),
                    seed=0,
                    options={"door_shuffle": "off"},
                )
                world = multiworld.worlds[self.player]
                existing_region_names = set(multiworld.regions.region_cache[self.player])
                warp_names = {
                    entrance_data.get("name", f"{region_name} to {entrance_data['to']['map']}")
                    for region_name, region_entrances in world.warp_data.items()
                    for entrance_data in region_entrances
                }
                invalid_regions = []

                for group_name, region_names in {
                    **get_mapped_indoor_region_groups(world),
                    **mapped_outdoor_region_groups,
                }.items():
                    existing_group_regions = set(region_names) & existing_region_names
                    for region_name in sorted(existing_group_regions):
                        if world.warp_data.get(region_name):
                            continue
                        region = multiworld.get_region(region_name, self.player)
                        has_outgoing_group_connection = any(
                            exit.connected_region is not None
                            and exit.name not in warp_names
                            and exit.connected_region.name in existing_group_regions
                            for exit in region.exits
                        )
                        if not has_outgoing_group_connection:
                            invalid_regions.append(f"{group_name}: {region_name}")

                self.assertEqual([], invalid_regions)

    def test_mapped_region_group_names_are_unique(self) -> None:
        all_warps = self.get_warp_entrances()

        region_groups = discover_mapped_region_groups(
            self.multiworld, self.player, all_warps, blocked_warps=all_warps,
            include_outdoor_regions=True)
        group_names = [region_group["name"] for region_group in region_groups]

        self.assertEqual(sorted(group_names), sorted(set(group_names)))

    def test_mapped_places_dead_end_slots_with_dead_end_groups(self) -> None:
        multiworld = setup_multiworld(
            PokemonRedWorld,
            seed=0,
            options={"door_shuffle": "mapped", "accessibility": "full"},
        )

        all_warps = [
            entrance for region in multiworld.get_regions(self.player)
            for entrance in region.exits
            if isinstance(entrance, PokemonRBWarp)
        ]
        interior_warps = [
            warp for warp in all_warps
            if not outdoor_map(warp.parent_region.name)
        ]
        region_groups = discover_mapped_region_groups(
            multiworld, self.player, interior_warps, blocked_warps=all_warps,
            include_outdoor_regions=False)

        nickname_destination = multiworld.get_entrance(
            "Viridian City to Viridian Nickname House", self.player).connected_region.name
        nickname_group = self.find_group_containing(region_groups, nickname_destination)
        self.assertEqual(1, len(nickname_group["warps"]))

    def test_yellow_mapped_with_generated_rock_tunnel(self) -> None:
        from ..regions import validate_mapped_door_shuffle_accessibility
        multiworld = setup_multiworld(
            PokemonYellowWorld,
            seed=0,
            options={"door_shuffle": "mapped", "randomize_rock_tunnel": True,
                     "accessibility": "full"},
        )
        validate_mapped_door_shuffle_accessibility(multiworld, self.player)

    def test_mapped_backtracks_when_complete_layout_is_rejected(self) -> None:
        from unittest.mock import patch
        from ..regions import DoorShuffleException, door_shuffle, validate_mapped_door_shuffle_accessibility
        calls = 0

        def reject_first_layout(multiworld, player):
            nonlocal calls
            calls += 1
            if calls == 1:
                raise DoorShuffleException("Reject first candidate to exercise rollback")
            validate_mapped_door_shuffle_accessibility(multiworld, player)

        with patch("worlds.pokemon_rby.regions.door_shuffle", wraps=door_shuffle) as shuffle_calls, \
                patch("worlds.pokemon_rby.regions.validate_mapped_door_shuffle_accessibility",
                      side_effect=reject_first_layout):
            multiworld = setup_multiworld(
                PokemonRedWorld, seed=0,
                options={"door_shuffle": "mapped", "accessibility": "full"},
            )
        self.assertGreater(calls, 1)
        self.assertEqual(1, shuffle_calls.call_count)
        validate_mapped_door_shuffle_accessibility(multiworld, self.player)
        for region in multiworld.get_regions(self.player):
            self.assertEqual(len(region.entrances), len(set(region.entrances)))
            for entrance in region.entrances:
                self.assertIs(entrance.connected_region, region)

    def test_accessibility_accepts_one_way_access_to_required_room(self) -> None:
        from ..regions import validate_mapped_door_shuffle_accessibility
        gym = self.multiworld.get_region("Pewter Gym", self.player)
        for entrance in gym.exits:
            if entrance.connected_region is not None:
                entrance.connected_region.entrances.remove(entrance)
                entrance.connected_region = None
        self.assertTrue(gym.entrances)
        validate_mapped_door_shuffle_accessibility(self.multiworld, self.player)

    def test_insanity_mapped_fixed_connections_remain_accessible(self) -> None:
        from unittest.mock import patch
        from ..regions import (connect_mapped_door_shuffle_region_groups,
                               validate_mapped_door_shuffle_accessibility)
        displaced = []

        def check_free_doors(world, groups, warps, destinations, *args, **kwargs):
            for warp in warps:
                if warp.mapped_slot_destination is not None:
                    displaced.append(warp.name)
                    self.assertIsNone(warp.connected_region)
                    self.assertIsNone(warp.mapped_slot_destination.connected_region)
            return connect_mapped_door_shuffle_region_groups(
                world, groups, warps, destinations, *args, **kwargs)

        for world_type in (PokemonRedWorld, PokemonYellowWorld):
            with self.subTest(game=world_type.game), patch(
                    "worlds.pokemon_rby.regions.connect_mapped_door_shuffle_region_groups",
                    side_effect=check_free_doors):
                multiworld = setup_multiworld(
                    world_type, seed=1,
                    options={"door_shuffle": "insanity_mapped", "accessibility": "full"},
                )
                validate_mapped_door_shuffle_accessibility(multiworld, self.player)
        self.assertTrue(displaced)

    def test_mapped_layouts_are_deterministic(self) -> None:
        def layout(multiworld):
            return sorted(
                (entrance.name, entrance.connected_region.name, entrance.target)
                for region in multiworld.get_regions(self.player) for entrance in region.exits
                if isinstance(entrance, PokemonRBWarp)
            )

        for mode in ("mapped", "insanity_mapped"):
            with self.subTest(mode=mode):
                options = {"door_shuffle": mode, "accessibility": "full"}
                first = setup_multiworld(PokemonYellowWorld, seed=0, options=options)
                second = setup_multiworld(PokemonYellowWorld, seed=0, options=options)
                self.assertEqual(layout(first), layout(second))

    def test_sealed_required_room_is_rejected_before_search(self) -> None:
        from ..regions import DoorShuffleException, connect_mapped_door_shuffle_region_groups
        gym = self.multiworld.get_region("Pewter Gym", self.player)
        for entrance in list(gym.entrances):
            entrance.parent_region.exits.remove(entrance)
            gym.entrances.remove(entrance)
        world = self.multiworld.worlds[self.player]
        with self.assertRaisesRegex(DoorShuffleException, "Pewter Gym"):
            connect_mapped_door_shuffle_region_groups(world, [], [], [], [])

    def test_search_budget_exhaustion_is_not_retried(self) -> None:
        from unittest.mock import patch
        from ..regions import MappedDoorShuffleSearchExhausted, door_shuffle
        with patch("worlds.pokemon_rby.regions.MAPPED_DOOR_SHUFFLE_WORK_LIMIT", 1), \
                patch("worlds.pokemon_rby.regions.door_shuffle", wraps=door_shuffle) as shuffle:
            with self.assertRaisesRegex(MappedDoorShuffleSearchExhausted,
                                        "does not prove that no valid layout exists"):
                setup_multiworld(PokemonYellowWorld, seed=0,
                                 options={"door_shuffle": "mapped", "accessibility": "full"})
        self.assertEqual(1, shuffle.call_count)
