from typing import Dict, TYPE_CHECKING
from BaseClasses import Region, Location
from .Locations import LocationData, TetrisAttackLocation
from .Logic import stage_clear_round_accessible, puzzle_level_accessible, cave_of_wickedness_accessible, \
    extra_puzzle_set_included, normal_puzzle_set_included, stage_clear_included, versus_mode_included, \
    puzzle_mode_included

if TYPE_CHECKING:
    from . import TetrisAttackWorld


def init_areas(world: "TetrisAttackWorld", locations: Dict[str, LocationData]) -> None:
    multiworld = world.multiworld
    player = world.player
    include_sc = stage_clear_included(world.options)
    include_pz = puzzle_mode_included(world.options)
    include_normal_puzzles = normal_puzzle_set_included(world.options)
    include_extra_puzzles = extra_puzzle_set_included(world.options)
    include_vs = versus_mode_included(world.options)

    locations_per_region = get_locations_per_region(locations)

    regions = [
        create_region(world, player, locations_per_region, "Menu"),
    ]
    if include_sc:
        regions.append(create_region(world, player, locations_per_region, "Stage Clear"))
        regions.append(create_region(world, player, locations_per_region, "SC Round 1"))
        regions.append(create_region(world, player, locations_per_region, "SC Round 2"))
        regions.append(create_region(world, player, locations_per_region, "SC Round 3"))
        regions.append(create_region(world, player, locations_per_region, "SC Round 4"))
        regions.append(create_region(world, player, locations_per_region, "SC Round 5"))
        regions.append(create_region(world, player, locations_per_region, "SC Round 6"))
    if include_pz:
        regions.append(create_region(world, player, locations_per_region, "Puzzle"))
        if include_normal_puzzles:
            regions.append(create_region(world, player, locations_per_region, "Puzzle L1"))
            regions.append(create_region(world, player, locations_per_region, "Puzzle L2"))
            regions.append(create_region(world, player, locations_per_region, "Puzzle L3"))
            regions.append(create_region(world, player, locations_per_region, "Puzzle L4"))
            regions.append(create_region(world, player, locations_per_region, "Puzzle L5"))
            regions.append(create_region(world, player, locations_per_region, "Puzzle L6"))
        if include_extra_puzzles:
            regions.append(create_region(world, player, locations_per_region, "Extra L1"))
            regions.append(create_region(world, player, locations_per_region, "Extra L2"))
            regions.append(create_region(world, player, locations_per_region, "Extra L3"))
            regions.append(create_region(world, player, locations_per_region, "Extra L4"))
            regions.append(create_region(world, player, locations_per_region, "Extra L5"))
            regions.append(create_region(world, player, locations_per_region, "Extra L6"))
    if include_vs:
        regions.append(create_region(world, player, locations_per_region, "Versus"))
        regions.append(create_region(world, player, locations_per_region, "Overworld"))
        regions.append(create_region(world, player, locations_per_region, "Mt Wickedness"))

    multiworld.regions += regions

    menu = multiworld.get_region("Menu", player)
    if include_sc:
        stage_clear_region = multiworld.get_region("Stage Clear", player)
        menu.connect(stage_clear_region, "Select Stage Clear")
        for x in range(1, 7):
            round_region = multiworld.get_region(f"SC Round {x}", player)
            stage_clear_region.connect(round_region, f"Select Round {x}",
                                       lambda state, n=x: stage_clear_round_accessible(world, state, n))
    if include_pz:
        puzzle_region = multiworld.get_region("Puzzle", player)
        menu.connect(puzzle_region, "Select Puzzle")
        for x in range(1, 7):
            if include_normal_puzzles:
                level_region = multiworld.get_region(f"Puzzle L{x}", player)
                puzzle_region.connect(level_region, f"Select Puzzle L{x}",
                                           lambda state, n=x: puzzle_level_accessible(world, state, n))
            if include_extra_puzzles:
                level_region = multiworld.get_region(f"Extra L{x}", player)
                puzzle_region.connect(level_region, f"Select Extra Puzzle L{x}",
                                           lambda state, n=x + 6: puzzle_level_accessible(world, state, n))
    if include_vs:
        versus_region = multiworld.get_region("Versus", player)
        menu.connect(versus_region, "Select Versus")
        overworld_region = multiworld.get_region("Overworld", player)
        versus_region.connect(overworld_region, f"Select Vs.")
        mt_region = multiworld.get_region("Mt Wickedness", player)
        versus_region.connect(mt_region, f"Enter Mt Wickedness",
                                        lambda state: cave_of_wickedness_accessible(world, state))


def create_location(player: int, name: str, location_data: LocationData, region: Region) -> Location:
    location = TetrisAttackLocation(player, name, location_data.code, region)
    location.access_rule = location_data.access_rule
    return location


def create_region(world: "TetrisAttackWorld", player: int, locations_per_region: Dict[str, Dict[str, LocationData]],
                  region_name: str) -> Region:
    region = Region(region_name, player, world.multiworld)

    if region_name in locations_per_region:
        for name, data in locations_per_region[region_name].items():
            location = create_location(player, name, data, region)
            region.locations.append(location)

    return region


def get_locations_per_region(locations: Dict[str, LocationData]) -> Dict[str, Dict[str, LocationData]]:
    per_region: Dict[str, Dict[str, LocationData]] = {}

    for name, data in locations.items():
        per_region.setdefault(data.region, dict())[name] = data

    return per_region
