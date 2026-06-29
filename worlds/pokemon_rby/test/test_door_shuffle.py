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
        self.assertEqual(set(silph_co_warp_tile_regions), self.region_names(silph_co_group))

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
