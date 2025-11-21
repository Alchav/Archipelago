from dataclasses import dataclass, field
from enum import IntFlag
from typing import List, Dict, Optional, Protocol, Iterable

from BaseClasses import MultiWorld, Region, Entrance

from worlds.flipwitch.strings.regions_entrances import FlipwitchRegion, FlipwitchEntrance, WitchyWoodsRegion


class RegionFactory(Protocol):
    def __call__(self, name: str, regions: Iterable[str]) -> Region:
        raise NotImplementedError


connector_keyword = " to "


def link_flipwitch_areas(world: MultiWorld, player: int):
    for (entrance, region) in flipwitch_entrances:
        world.get_entrance(entrance, player).connect(world.get_region(region, player))


@dataclass(frozen=True)
class RegionData:
    name: str
    exits: List[str] = field(default_factory=list)

    def get_merged_with(self, exits: List[str]):
        merged_exits = []
        merged_exits.extend(self.exits)
        if exits is not None:
            merged_exits.extend(exits)
        merged_exits = list(set(merged_exits))
        return RegionData(self.name, merged_exits)

    def get_clone(self):
        return self.get_merged_with(None)


class RandomizationFlag(IntFlag):
    NOT_RANDOMIZED = 0b0
    RANDOMIZED = 0b1


@dataclass(frozen=True)
class ConnectionData:
    name: str
    destination: str
    origin: Optional[str] = None
    reverse: Optional[str] = None
    flag: RandomizationFlag = RandomizationFlag.NOT_RANDOMIZED

    def __post_init__(self):
        if connector_keyword in self.name:
            origin, destination = self.name.split(connector_keyword)
            if self.reverse is None:
                super().__setattr__("reverse", f"{destination}{connector_keyword}{origin}")


new_flipwitch_regions = [
    RegionData(WitchyWoodsRegion.beatrix_hut, []),
]

flipwitch_regions = [
    RegionData(FlipwitchRegion.menu, [FlipwitchEntrance.menu_to_woods]),
    RegionData(FlipwitchRegion.witch_woods, [FlipwitchEntrance.witchy_to_spirit, FlipwitchEntrance.woods_to_woods_lower, FlipwitchEntrance.woods_to_sex_experience_layer_1]),
    RegionData(FlipwitchRegion.sex_experience_layer_1, [FlipwitchEntrance.sex_experience_layer_1_to_sex_experience_layer_2]),
    RegionData(FlipwitchRegion.sex_experience_layer_2, [FlipwitchEntrance.sex_experience_layer_2_to_sex_experience_layer_3]),
    RegionData(FlipwitchRegion.sex_experience_layer_3),
    RegionData(FlipwitchRegion.spirit_town, [FlipwitchEntrance.spirit_to_cafe, FlipwitchEntrance.spirit_to_mansion, FlipwitchEntrance.spirit_to_shady,
                                             FlipwitchEntrance.spirit_to_early_ghost, FlipwitchEntrance.spirit_to_jigoku,
                                             FlipwitchEntrance.spirit_to_outside_chaos_castle]),
    RegionData(FlipwitchRegion.shady_sewers),
    RegionData(FlipwitchRegion.cabaret_cafe),
    RegionData(FlipwitchRegion.pig_mansion),
    RegionData(FlipwitchRegion.witch_woods_lower),
    RegionData(FlipwitchRegion.early_ghost, [FlipwitchEntrance.early_ghost_to_ghost, FlipwitchEntrance.early_ghost_to_fungal_forest]),
    RegionData(FlipwitchRegion.ghost_castle, [FlipwitchEntrance.ghost_to_ghost_rose]),
    RegionData(FlipwitchRegion.ghost_rose, [FlipwitchEntrance.ghost_rose_to_upper_ghost]),
    RegionData(FlipwitchRegion.upper_ghost),
    RegionData(FlipwitchRegion.jigoku, [FlipwitchEntrance.jigoku_to_club_demon]),
    RegionData(FlipwitchRegion.club_demon),
    RegionData(FlipwitchRegion.fungal_forest, [FlipwitchEntrance.fungal_to_umi_umi, FlipwitchEntrance.fungal_forest_to_tengoku,
                                               FlipwitchEntrance.fungal_to_deep_fungal]),
    RegionData(FlipwitchRegion.tengoku, [FlipwitchEntrance.tengoku_to_tengoku_upper]),
    RegionData(FlipwitchRegion.tengoku_upper, [FlipwitchEntrance.tengoku_upper_to_angelic_hallway]),
    RegionData(FlipwitchRegion.angelic_hallway, [FlipwitchEntrance.angelic_to_angelic_mid]),
    RegionData(FlipwitchRegion.angelic_bewitched, [FlipwitchEntrance.angelic_mid_to_angelic_upper]),
    RegionData(FlipwitchRegion.angelic_upper),
    RegionData(FlipwitchRegion.deep_fungal, [FlipwitchEntrance.deep_fungal_to_slime_citadel]),
    RegionData(FlipwitchRegion.slime_citadel),
    RegionData(FlipwitchRegion.umi_umi, [FlipwitchEntrance.umi_umi_to_umi_umi_depths]),
    RegionData(FlipwitchRegion.umi_umi_depths),
    RegionData(FlipwitchRegion.outside_chaos, [FlipwitchEntrance.outside_chaos_to_chaos]),
    RegionData(FlipwitchRegion.chaos_castle),
]

flipwitch_entrances = [
    ConnectionData(FlipwitchEntrance.menu_to_woods, FlipwitchRegion.witch_woods),
    ConnectionData(FlipwitchEntrance.woods_to_sex_experience_layer_1, FlipwitchRegion.sex_experience_layer_1),
    ConnectionData(FlipwitchEntrance.sex_experience_layer_1_to_sex_experience_layer_2, FlipwitchRegion.sex_experience_layer_2),
    ConnectionData(FlipwitchEntrance.sex_experience_layer_2_to_sex_experience_layer_3, FlipwitchRegion.sex_experience_layer_3),
    ConnectionData(FlipwitchEntrance.witchy_to_spirit, FlipwitchRegion.spirit_town),
    ConnectionData(FlipwitchEntrance.woods_to_woods_lower, FlipwitchRegion.witch_woods_lower),
    ConnectionData(FlipwitchEntrance.spirit_to_cafe, FlipwitchRegion.cabaret_cafe),
    ConnectionData(FlipwitchEntrance.spirit_to_mansion, FlipwitchRegion.pig_mansion),
    ConnectionData(FlipwitchEntrance.spirit_to_shady, FlipwitchRegion.shady_sewers),
    ConnectionData(FlipwitchEntrance.spirit_to_early_ghost, FlipwitchRegion.early_ghost),
    ConnectionData(FlipwitchEntrance.early_ghost_to_ghost, FlipwitchRegion.ghost_castle),
    ConnectionData(FlipwitchEntrance.ghost_to_ghost_rose, FlipwitchRegion.ghost_rose),
    ConnectionData(FlipwitchEntrance.ghost_rose_to_upper_ghost, FlipwitchRegion.upper_ghost),
    ConnectionData(FlipwitchEntrance.spirit_to_jigoku, FlipwitchRegion.jigoku),
    ConnectionData(FlipwitchEntrance.jigoku_to_club_demon, FlipwitchRegion.club_demon),
    ConnectionData(FlipwitchEntrance.early_ghost_to_fungal_forest, FlipwitchRegion.fungal_forest),
    ConnectionData(FlipwitchEntrance.fungal_forest_to_tengoku, FlipwitchRegion.tengoku),
    ConnectionData(FlipwitchEntrance.tengoku_to_tengoku_upper, FlipwitchRegion.tengoku_upper),
    ConnectionData(FlipwitchEntrance.tengoku_upper_to_angelic_hallway, FlipwitchRegion.angelic_hallway),
    ConnectionData(FlipwitchEntrance.angelic_to_angelic_mid, FlipwitchRegion.angelic_bewitched),
    ConnectionData(FlipwitchEntrance.angelic_mid_to_angelic_upper, FlipwitchRegion.angelic_upper),
    ConnectionData(FlipwitchEntrance.fungal_to_deep_fungal, FlipwitchRegion.deep_fungal),
    ConnectionData(FlipwitchEntrance.deep_fungal_to_slime_citadel, FlipwitchRegion.slime_citadel),
    ConnectionData(FlipwitchEntrance.fungal_to_umi_umi, FlipwitchRegion.umi_umi),
    ConnectionData(FlipwitchEntrance.umi_umi_to_umi_umi_depths, FlipwitchRegion.umi_umi_depths),
    ConnectionData(FlipwitchEntrance.spirit_to_outside_chaos_castle, FlipwitchRegion.outside_chaos),
    ConnectionData(FlipwitchEntrance.outside_chaos_to_chaos, FlipwitchRegion.chaos_castle),
]


def create_regions(region_factory: RegionFactory) -> Dict[str, Region]:
    final_regions = flipwitch_regions
    regions: Dict[str: Region] = {region.name: region_factory(region.name, region.exits) for region in
                                  final_regions}
    entrances: Dict[str: Entrance] = {entrance.name: entrance
                                      for region in regions.values()
                                      for entrance in region.exits}

    connections = flipwitch_entrances

    for connection in connections:
        if connection.name in entrances:
            entrances[connection.name].connect(regions[connection.destination])

    return regions

