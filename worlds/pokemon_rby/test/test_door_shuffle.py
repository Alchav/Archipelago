import unittest

from test.general import setup_multiworld

from .. import PokemonRedWorld
from ..regions import PokemonRBWarp, discover_mapped_region_groups, outdoor_map, saffron_gym_warps


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
        shuffleable_warps = self.get_entrances([
            "Saffron City-G to Saffron Gym-S",
            "Saffron Gym-S to Saffron City-G",
            *saffron_gym_warps,
        ])

        region_groups = discover_mapped_region_groups(
            self.multiworld, self.player, shuffleable_warps, blocked_warps=shuffleable_warps)
        saffron_gym_group = self.find_group_containing(region_groups, "Saffron Gym-S")

        self.assertEqual({"Saffron Gym-S"}, self.region_names(saffron_gym_group))
        self.assertCountEqual(
            ["Saffron Gym-S to Saffron City-G", "Saffron Gym-S to Saffron Gym-SE"],
            [warp.name for warp in saffron_gym_group["warps"]],
        )

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
