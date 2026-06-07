from typing import Callable, Union, Dict, Set

from BaseClasses import CollectionState, Entrance, MultiWorld
from ..generic.Rules import add_rule, set_rule
from .Locations import loc100Coin_table, location_table
from .Options import SM64Options
from .Regions import connect_regions, SM64Levels, sm64_entrance_to_region, sm64_level_to_paintings, \
    sm64_level_to_secrets, sm64_secrets_to_level, sm64_entrances_to_level, sm64_level_to_entrances, \
    sm64_ttc_entrances, sm64_wdw_entrances
from .Items import action_item_data_table, cap_item_data_table


initial_reachable_entrances = (
    "Bob-omb Battlefield",
    "Whomp's Fortress",
    "Jolly Roger Bay",
    "Cool, Cool Mountain",
    "The Princess's Secret Slide",
)

def shuffle_dict_keys(multiworld: MultiWorld, dictionary: dict) -> dict:
    keys = list(dictionary.keys())
    values = list(dictionary.values())
    multiworld.random.shuffle(keys)
    return dict(zip(keys, values))

def fix_reg(entrance_map: Dict[SM64Levels, str], entrance: SM64Levels, invalid_regions: Set[str],
            swapdict: Dict[SM64Levels, str], multiworld: MultiWorld):
    if entrance_map[entrance] in invalid_regions: # Unlucky :C
        replacement_regions = [(rand_entrance, rand_region) for rand_entrance, rand_region in swapdict.items()
                               if rand_region not in invalid_regions]
        rand_entrance, rand_region = multiworld.random.choice(replacement_regions)
        old_dest = entrance_map[entrance]
        entrance_map[entrance], entrance_map[rand_entrance] = rand_region, old_dest
        swapdict[entrance], swapdict[rand_entrance] = rand_region, old_dest
    swapdict.pop(entrance)


def is_starting_check_location(location_name: str, options: SM64Options) -> bool:
    if options.enable_coin_stars == options.enable_coin_stars.option_vanilla and location_name in loc100Coin_table:
        return False
    if not options.exclamation_boxes and "1Up Block" in location_name:
        return False
    if not options.buddy_checks and location_name.endswith(" - Bob-omb Buddy"):
        return False
    return True


def get_starting_check_sources(options: SM64Options) -> tuple[str, ...]:
    if options.enable_locked_paintings:
        return ("Bob-omb Battlefield",)
    return initial_reachable_entrances


def get_randomized_entrance_connections(multiworld: MultiWorld, player: int) -> Dict[str, Entrance]:
    return {
        entrance.name.split(" -> ", 1)[1]: entrance
        for entrance in multiworld.get_entrances(player)
        if " -> " in entrance.name and entrance.name.split(" -> ", 1)[1] in sm64_entrances_to_level
        and entrance.parent_region.name not in sm64_wdw_entrances
    }


def has_reachable_starting_check(
        multiworld: MultiWorld, options: SM64Options, player: int,
        allowed_source_entrances: tuple[str, ...] | None = None,
        randomized_entrance_connections: Dict[str, Entrance] | None = None) -> bool:
    if allowed_source_entrances is None:
        allowed_source_entrances = get_starting_check_sources(options)
    if randomized_entrance_connections is None:
        randomized_entrance_connections = get_randomized_entrance_connections(multiworld, player)

    allowed_source_entrance_set = set(allowed_source_entrances)
    disabled_connections = {}
    for source_entrance, entrance in randomized_entrance_connections.items():
        if source_entrance not in allowed_source_entrance_set:
            disabled_connections[entrance] = entrance.access_rule
            entrance.access_rule = lambda state: False

    try:
        state = CollectionState(multiworld)
        return any(
            is_starting_check_location(location.name, options) and location.can_reach(state)
            for location in multiworld.get_locations(player)
        )
    finally:
        for entrance, access_rule in disabled_connections.items():
            entrance.access_rule = access_rule


def retarget_entrance(entrance: Entrance, target_region_name: str, multiworld: MultiWorld, player: int) -> None:
    target_region = multiworld.get_region(target_region_name, player)
    if entrance.connected_region is target_region:
        return
    if entrance.connected_region:
        entrance.connected_region.entrances.remove(entrance)
    entrance.connected_region = target_region
    target_region.entrances.append(entrance)


def sources_share_entrance_pool(source: str, donor: str, options: SM64Options) -> bool:
    source_is_course = sm64_entrances_to_level[source] in sm64_level_to_paintings
    donor_is_course = sm64_entrances_to_level[donor] in sm64_level_to_paintings
    if options.area_rando == options.area_rando.option_Courses_Only:
        return source_is_course and donor_is_course
    if options.area_rando == options.area_rando.option_Courses_and_Secrets:
        return True
    return source_is_course == donor_is_course


def has_valid_fixed_assignments(entrance_map: Dict[SM64Levels, str]) -> bool:
    if entrance_map[SM64Levels.BOWSER_IN_THE_FIRE_SEA] == "Dire, Dire Docks":
        return False
    invalid_cotmc_destinations = {"Hazy Maze Cave"}
    if entrance_map[SM64Levels.BOWSER_IN_THE_FIRE_SEA] == "Hazy Maze Cave":
        invalid_cotmc_destinations.add("Dire, Dire Docks")
    return entrance_map[SM64Levels.CAVERN_OF_THE_METAL_CAP] not in invalid_cotmc_destinations


def ensure_reachable_starting_check(
        multiworld: MultiWorld, options: SM64Options, player: int,
        randomized_entrances: Dict[SM64Levels, str], randomized_entrances_s: Dict[str, str],
        randomized_entrance_connections: Dict[str, Entrance]) -> None:
    starting_check_sources = get_starting_check_sources(options)
    if has_reachable_starting_check(
            multiworld, options, player, starting_check_sources, randomized_entrance_connections):
        return

    for source in starting_check_sources:
        source_connection = randomized_entrance_connections[source]
        old_source_destination = randomized_entrances_s[source]
        old_source_region = sm64_entrance_to_region[old_source_destination]

        for donor, donor_destination in randomized_entrances_s.items():
            if donor == source or not sources_share_entrance_pool(source, donor, options):
                continue

            source_level = sm64_entrances_to_level[source]
            donor_level = sm64_entrances_to_level[donor]
            swapped_entrances = randomized_entrances.copy()
            swapped_entrances[source_level], swapped_entrances[donor_level] = \
                donor_destination, old_source_destination
            if not has_valid_fixed_assignments(swapped_entrances):
                continue

            donor_connection = randomized_entrance_connections[donor]
            old_donor_region = sm64_entrance_to_region[donor_destination]
            retarget_entrance(source_connection, old_donor_region, multiworld, player)
            retarget_entrance(donor_connection, old_source_region, multiworld, player)

            if has_reachable_starting_check(
                    multiworld, options, player, starting_check_sources, randomized_entrance_connections):
                randomized_entrances[source_level], randomized_entrances[donor_level] = \
                    donor_destination, old_source_destination
                randomized_entrances_s[source], randomized_entrances_s[donor] = \
                    donor_destination, old_source_destination
                return

            retarget_entrance(source_connection, old_source_region, multiworld, player)
            retarget_entrance(donor_connection, old_donor_region, multiworld, player)

    raise Exception("Unable to place a reachable starting check in an initially accessible SM64 entrance.")

def set_rules(multiworld: MultiWorld, options: SM64Options, player: int, area_connections: dict, star_costs: dict, move_rando_bitvec: int):
    randomized_level_to_paintings = sm64_level_to_paintings.copy()
    randomized_level_to_secrets = sm64_level_to_secrets.copy()

    if options.area_rando > options.area_rando.option_Off:  # Some randomization is happening, randomize Courses
        randomized_level_to_paintings = shuffle_dict_keys(multiworld, sm64_level_to_paintings)

    if options.area_rando == options.area_rando.option_Courses_and_Secrets_Separate:  # Randomize Secrets as well
        randomized_level_to_secrets = shuffle_dict_keys(multiworld, sm64_level_to_secrets)

    randomized_entrances = {**randomized_level_to_paintings, **randomized_level_to_secrets} # Concatenate courses and secrets for rest

    if options.area_rando == options.area_rando.option_Courses_and_Secrets:  # Randomize Courses and Secrets in one pool
        randomized_entrances = shuffle_dict_keys(multiworld, randomized_entrances)
    
    # Now, fix assignment if necessary
    swapdict = randomized_entrances.copy()
    # Guarantee BITFS is not mapped to DDD
    fix_reg(randomized_entrances, SM64Levels.BOWSER_IN_THE_FIRE_SEA, {"Dire, Dire Docks"}, swapdict, multiworld)
    # Guarantee COTMC is not mapped to HMC, cuz thats impossible. If BitFS -> HMC, also no COTMC -> DDD.
    if randomized_entrances[SM64Levels.BOWSER_IN_THE_FIRE_SEA] == "Hazy Maze Cave":
        fix_reg(randomized_entrances, SM64Levels.CAVERN_OF_THE_METAL_CAP, {"Hazy Maze Cave", "Dire, Dire Docks"}, swapdict, multiworld)
    else:
        fix_reg(randomized_entrances, SM64Levels.CAVERN_OF_THE_METAL_CAP, {"Hazy Maze Cave"}, swapdict, multiworld)

    randomized_entrances_s = {sm64_level_to_entrances[entrance_lvl]: destination for (entrance_lvl,destination) in randomized_entrances.items()}
    randomized_entrance_connections = {}

    rf = RuleFactory(multiworld, options, player, move_rando_bitvec)

    def connect_randomized_entrance(source: str, source_entrance: str, rule=None):
        destination_entrance = randomized_entrances_s[source_entrance]
        target_region = sm64_entrance_to_region[destination_entrance]
        entrance = connect_regions(
            multiworld, player, source, target_region, rule,
            name=f"{source} -> {source_entrance}"
        )
        randomized_entrance_connections[source_entrance] = entrance
        return entrance

    def has_first_floor_key(state):
        return state.has("First Floor Key", player) or state.has("Progressive Key", player, 1)

    def has_basement_key(state):
        return state.has("Basement Key", player) or state.has("Progressive Basement Key", player, 1) or \
            state.has("Progressive Key", player, 2)

    def has_thirty_star_key(state):
        return state.has("Progressive Basement Key", player, 2) or state.has("Progressive Key", player, 3)

    def has_second_floor_key(state):
        return state.has("Second Floor Key", player) or state.has("Progressive Upstairs Key", player, 1) or \
            state.has("Progressive Key", player, 4)

    def has_third_floor_key(state):
        return state.has("Progressive Upstairs Key", player, 2) or state.has("Progressive Key", player, 5)

    def has_endless_stairs_key(state):
        return state.has("Progressive Upstairs Key", player, 3) or state.has("Progressive Key", player, 6)

    connect_randomized_entrance("Menu", "Bob-omb Battlefield")
    connect_randomized_entrance("Menu", "Whomp's Fortress",
                                rf.build_rule("", painting_lvl_name="Whomp's Fortress"))
    # JRB door is separated from JRB itself because the secret aquarium can be accessed without entering the painting
    connect_regions(multiworld, player, "Menu", "Jolly Roger Bay Door")
    connect_randomized_entrance("Jolly Roger Bay Door", "Jolly Roger Bay",
                                rf.build_rule("", painting_lvl_name="Jolly Roger Bay"))
    connect_randomized_entrance("Menu", "Cool, Cool Mountain",
                                rf.build_rule("", painting_lvl_name="Cool, Cool Mountain"))
    connect_randomized_entrance("Menu", "Big Boo's Haunt",
                                lambda state: state.has("Courtyard Boos", player))
    connect_randomized_entrance("Menu", "The Princess's Secret Slide")
    connect_randomized_entrance("Jolly Roger Bay Door", "The Secret Aquarium",
                                rf.build_rule("SF/BF | TJ & LG | MOVELESS & TJ"))
    connect_randomized_entrance("Menu", "Tower of the Wing Cap",
                                lambda state: state.has("Wing Cap Light", player))
    connect_randomized_entrance("Menu", "Bowser in the Dark World", has_first_floor_key)

    connect_regions(multiworld, player, "Menu", "Basement", has_basement_key)

    connect_randomized_entrance("Basement", "Hazy Maze Cave")
    connect_randomized_entrance("Basement", "Lethal Lava Land",
                                rf.build_rule("", painting_lvl_name="Lethal Lava Land"))
    connect_randomized_entrance("Basement", "Shifting Sand Land",
                                rf.build_rule("", painting_lvl_name="Shifting Sand Land"))
    ddd_entry_rule = rf.build_rule("", painting_lvl_name="Dire, Dire Docks")
    connect_randomized_entrance("Basement", "Dire, Dire Docks",
                                lambda state: has_thirty_star_key(state) and ddd_entry_rule(state))
    connect_randomized_entrance("Hazy Maze Cave", "Cavern of the Metal Cap",
                                rf.build_rule("HMC_SWIMMING_BEAST"))
    connect_randomized_entrance("Basement", "Vanish Cap under the Moat",
                                rf.build_rule("GP"))
    connect_randomized_entrance("Basement", "Bowser in the Fire Sea",
                                lambda state: has_thirty_star_key(state) and
                                state.has_any({"Dire, Dire Docks - Bowser's Sub", "Dire, Dire Docks - Poles"}, player))

    connect_regions(multiworld, player, "Menu", "Second Floor", has_second_floor_key)

    connect_randomized_entrance("Second Floor", "Snowman's Land",
                                rf.build_rule("", painting_lvl_name="Snowman's Land"))
    for wdw_entrance in sm64_wdw_entrances:
        wdw_entrance_rule = "LG & TJ/SF/BF" if wdw_entrance == "Wet-Dry World High" else ""
        connect_randomized_entrance("Second Floor", wdw_entrance,
                                    rf.build_rule(wdw_entrance_rule, painting_lvl_name="Wet-Dry World"))
    connect_randomized_entrance("Second Floor", "Tall, Tall Mountain",
                                rf.build_rule("", painting_lvl_name="Tall, Tall Mountain"))
    connect_randomized_entrance("Second Floor", "Tiny-Huge Island (Tiny)",
                                rf.build_rule("", painting_lvl_name="Tiny-Huge Island"))
    connect_randomized_entrance("Second Floor", "Tiny-Huge Island (Huge)",
                                rf.build_rule("", painting_lvl_name="Tiny-Huge Island"))
    connect_regions(multiworld, player, "Tiny-Huge Island (Tiny)", "Tiny-Huge Island")
    connect_regions(multiworld, player, "Tiny-Huge Island (Huge)", "Tiny-Huge Island")

    connect_regions(multiworld, player, "Second Floor", "Third Floor", has_third_floor_key)

    for ttc_entrance in sm64_ttc_entrances:
        connect_randomized_entrance("Third Floor", ttc_entrance,
                                    rf.build_rule("LG/TJ/SF/BF/WK", painting_lvl_name="Tick Tock Clock"))
    connect_randomized_entrance("Third Floor", "Rainbow Ride", rf.build_rule("TJ/SF/BF"))
    connect_randomized_entrance("Menu", "Wing Mario over the Rainbow",
                                lambda state: state.has("Castle Cannon", player))
    connect_regions(multiworld, player, "Third Floor", "Bowser in the Sky", has_endless_stairs_key)

    # Course Rules
    # Bob-omb Battlefield
    rf.assign_rule("Bob-omb Battlefield - Big Bob-Omb on the Summit", "BOB_KING")
    rf.assign_rule("Bob-omb Battlefield - Footrace with Koopa The Quick", "BOB_KOOPA")
    rf.assign_rule("Bob-omb Battlefield - Island", "CANN | CANNLESS & WC & TJ | CAPLESS & CANNLESS & LJ")
    rf.assign_rule("Bob-omb Battlefield - Mario Wings to the Sky",  "CANN & WC | CAPLESS & CANN")
    rf.assign_rule("Bob-omb Battlefield - Behind Chain Chomp's Gate", "GP | MOVELESS")
    rf.assign_rule("Bob-omb Battlefield - Bob-omb Buddy", "BOB_BUDDY")
    # Whomp's Fortress
    rf.assign_rule("Whomp's Fortress - To the Top of the Fortress", "WF_FORTRESS")
    rf.assign_rule("Whomp's Fortress - Chip Off Whomp's Block", "WF_KING & GP")
    rf.assign_rule("Whomp's Fortress - Top", "CHECKERBOARD_PLATFORMS | WF_HOOT | WK & SF/TJ")
    rf.assign_rule("Whomp's Fortress - Shoot into the Wild Blue", "WK & TJ/SF | CANN")
    rf.assign_rule("Whomp's Fortress - Red Coins on the Floating Isle", "WF_FORTRESS")
    rf.assign_rule("Whomp's Fortress - Fall onto the Caged Island",
                   "WF_HOOT | CL & WF_FORTRESS & {Whomp's Fortress - Top} | "
                   "MOVELESS & TJ & WF_FORTRESS & {Whomp's Fortress - Top} | "
                   "MOVELESS & LJ & WF_FORTRESS & {Whomp's Fortress - Top} | MOVELESS & CANN")
    rf.assign_rule("Whomp's Fortress - Blast Away the Wall", "CANN | CANNLESS & LG")
    rf.assign_rule("Whomp's Fortress - Bob-omb Buddy", "WF_BUDDY")
    # Jolly Roger Bay
    rf.assign_rule("Jolly Roger Bay - Plunder in the Sunken Ship", "JRB_SUNKEN_SHIP")
    rf.assign_rule("Jolly Roger Bay - Can the Eel Come Out to Play?", "JRB_UNAGI")
    rf.assign_rule("Jolly Roger Bay - Upper", "TJ/BF/SF/WK | MOVELESS & LG")
    rf.assign_rule("Jolly Roger Bay - Red Coins on the Ship Afloat",
                   "JRB_RAISED_SHIP & CL/TJ | JRB_RAISED_SHIP & CANN | "
                   "JRB_RAISED_SHIP & MOVELESS & BF/WK")
    rf.assign_rule("Jolly Roger Bay - Blast to the Stone Pillar",
                   "CANN+CL | CANNLESS & MOVELESS | CANN & MOVELESS")
    rf.assign_rule("Jolly Roger Bay - Through the Jet Stream", "JRB_JET_STREAM & MC/CAPLESS")
    rf.assign_rule("Jolly Roger Bay - Bob-omb Buddy", "JRB_BUDDY")
    # Cool, Cool Mountain
    rf.assign_rule("Cool, Cool Mountain - Big Penguin Race", "CCM_BIG_PENGUIN")
    rf.assign_rule("Cool, Cool Mountain - Snowman's Lost His Head", "CCM_SNOWMAN_HEAD")
    rf.assign_rule("Cool, Cool Mountain - Li'l Penguin Lost", "CCM_BABY_PENGUINS")
    rf.assign_rule("Cool, Cool Mountain - Wall Kicks Will Work", "TJ/WK & CANN | CANNLESS & TJ/WK | MOVELESS")
    # Big Boo's Haunt
    rf.assign_rule("Big Boo's Haunt - Ride Big Boo's Merry-Go-Round", "BBH_MERRY_GO_ROUND")
    rf.assign_rule("Big Boo's Haunt - Second Floor", "BBH_STAIRCASE | WK & TJ/SF")
    rf.assign_rule("Big Boo's Haunt - Third Floor", "WK+LG | MOVELESS & WK")
    rf.assign_rule("Big Boo's Haunt - Roof", "LJ | MOVELESS")
    rf.assign_rule("Big Boo's Haunt - Secret of the Haunted Books", "KK | MOVELESS")
    rf.assign_rule("Big Boo's Haunt - Seek the 8 Red Coins", "BF/WK/TJ/SF")
    rf.assign_rule("Big Boo's Haunt - Eye to Eye in the Secret Room", "VC")
    # Haze Maze Cave
    rf.assign_rule("Hazy Maze Cave - Swimming Beast in the Cavern", "HMC_SWIMMING_BEAST")
    rf.assign_rule("Hazy Maze Cave - Red Coin Area",
                   "CHECKERBOARD_PLATFORMS & CL & WK/LG/BF/SF/TJ | CHECKERBOARD_PLATFORMS & MOVELESS & WK")
    rf.assign_rule("Hazy Maze Cave - Pit Islands", "TJ+CL | MOVELESS & WK & TJ/LJ | MOVELESS & WK+SF+LG")
    rf.assign_rule("Hazy Maze Cave - Metal-Head Mario Can Move!", "LJ+MC | CAPLESS & LJ+TJ | CAPLESS & MOVELESS & LJ/TJ/WK")
    rf.assign_rule("Hazy Maze Cave - Navigating the Toxic Maze", "WK/SF/BF/TJ")
    rf.assign_rule("Hazy Maze Cave - Watch for Rolling Rocks", "WK")
    # Lethal Lava Land
    rf.assign_rule("Lethal Lava Land - Red-Hot Log Rolling", "WC | LLL_ROLLING_LOG | LLL_KOOPA_SHELL")
    rf.assign_rule("Lethal Lava Land - Upper Volcano", "CL")
    rf.assign_rule("Lethal Lava Land - Elevator Tour in the Volcano", "CHECKERBOARD_PLATFORMS/DV/TJ/LJ")
    # Shifting Sand Land
    rf.assign_rule("Shifting Sand Land - In the Talons of the Big Bird", "SSL_KLEPTO")
    rf.assign_rule("Shifting Sand Land - Upper Pyramid", "CL & TJ/BF/SF/LG | SSL_PYRAMID_ELEVATOR")
    rf.assign_rule("Shifting Sand Land - Stand Tall on the Four Pillars",
                   "SSL_PYRAMID_ELEVATOR & TJ+WC+GP | SSL_PYRAMID_ELEVATOR & CANN+WC+GP | "
                   "SSL_PYRAMID_ELEVATOR & TJ/SF/BF & CAPLESS | MOVELESS & LG/KK")
    rf.assign_rule("Shifting Sand Land - Free Flying for 8 Red Coins", "TJ+WC | CANN+WC | TJ/SF/BF & CAPLESS | MOVELESS & CAPLESS")
    # Dire, Dire Docks
    rf.assign_rule("Dire, Dire Docks - Board Bowser's Sub", "DDD_BOWSER_SUB")
    rf.assign_rule("Dire, Dire Docks - Pole-Jumping for Red Coins", "DDD_POLES & CL | DDD_POLES & TJ+DV+LG+WK & MOVELESS")
    rf.assign_rule("Dire, Dire Docks - Through the Jet Stream", "MC | CAPLESS")
    rf.assign_rule("Dire, Dire Docks - The Manta Ray's Reward", "DDD_MANTA_RAY")
    rf.assign_rule("Dire, Dire Docks - Collect the Caps...", "VC+MC | CAPLESS & VC")
    # Snowman's Land
    rf.assign_rule("Snowman's Land - Snowman's Big Head", "SL_PENGUIN & BF/SF/CANN/TJ | CANN")
    rf.assign_rule("Snowman's Land - In the Deep Freeze", "WK/SF/LG/BF/CANN/TJ")
    rf.assign_rule("Snowman's Land - Into the Igloo", "VC & TJ/SF/BF/WK/LG | MOVELESS & VC")
    # Wet-Dry World
    rf.assign_rule("Wet-Dry World - Top", "WK/TJ/SF/BF | MOVELESS")
    rf.assign_rule("Wet-Dry World - Downtown", "{Wet-Dry World High} | CANN | MOVELESS & TJ+DV")
    rf.assign_rule("Wet-Dry World - Go to Town for Red Coins", "WK | MOVELESS & TJ")
    rf.assign_rule("Wet-Dry World - Quick Race Through Downtown!", "VC & WK/BF | VC & TJ+LG | MOVELESS & VC & TJ")
    rf.assign_rule("Wet-Dry World - Bob-omb Buddy", "TJ | SF+LG | NAR & BF/SF")
    # Tall, Tall Mountain
    rf.assign_rule("Tall, Tall Mountain - Top", "MOVELESS & TJ | LJ/DV & LG/KK | MOVELESS & WK & SF/LG | MOVELESS & KK/DV")
    rf.assign_rule("Tall, Tall Mountain - Mystery of the Monkey Cage", "TTM_UKIKI")
    rf.assign_rule("Tall, Tall Mountain - Blast to the Lonely Mushroom", "CANN | CANNLESS & LJ | MOVELESS & CANNLESS")
    # Tiny-Huge Island
    rf.assign_rule("Tiny-Huge Island - 1Up Block THI Small near Start", "NAR | {Tiny-Huge Island - Pipes}")
    rf.assign_rule("Tiny-Huge Island - Pipes", "THI_WARP_PIPES & LJ/TJ/DV/LG | THI_WARP_PIPES & MOVELESS & BF/SF/KK")
    rf.assign_rule("Tiny-Huge Island - Large Top", "LJ/TJ/DV | MOVELESS")
    rf.assign_rule("Tiny-Huge Island - Rematch with Koopa the Quick", "THI_KOOPA")
    rf.assign_rule("Tiny-Huge Island - Wiggler's Red Coins", "WK")
    rf.assign_rule("Tiny-Huge Island - Make Wiggler Squirm", "GP | MOVELESS & DV")
    # Tick Tock Clock
    rf.assign_rule("Tick Tock Clock - Lower", "LG/TJ/SF/BF/WK")
    rf.assign_rule("Tick Tock Clock - Upper", "CL | MOVELESS & WK")
    rf.assign_rule("Tick Tock Clock - Top", "TJ+LG | MOVELESS & WK/TJ")
    rf.assign_rule("Tick Tock Clock - Stomp on the Thwomp", "{Tick Tock Clock Moving}")
    rf.assign_rule("Tick Tock Clock - Stop Time for Red Coins", "{Tick Tock Clock Stopped} | {Tick Tock Clock - Lower}")
    # Rainbow Ride
    rf.assign_rule("Rainbow Ride - Carpets", "RR_CARPETS/LJ/DV/TJ")
    rf.assign_rule("Rainbow Ride - Maze", "WK | LJ & SF/BF/TJ | MOVELESS & LG/TJ")
    rf.assign_rule("Rainbow Ride - Bob-omb Buddy", "WK | MOVELESS & LG")
    rf.assign_rule("Rainbow Ride - Swingin' in the Breeze", "LG/TJ/BF/SF | MOVELESS")
    rf.assign_rule("Rainbow Ride - Tricky Triangles!", "LG/TJ/BF/SF | MOVELESS")
    rf.assign_rule("Rainbow Ride - Cruiser", "RR_CARPETS & WK/SF/BF/LG/TJ")
    rf.assign_rule("Rainbow Ride - House", "RR_CARPETS & TJ/SF/BF/LG")
    rf.assign_rule("Rainbow Ride - Somewhere Over the Rainbow", "CANN")
    # Tower of the Wing Cap
    rf.assign_rule("Tower of the Wing Cap Red Coins", "WC")
    # Cavern of the Metal Cap
    rf.assign_rule("Cavern of the Metal Cap Red Coins", "MC | CAPLESS")
    # Vanish Cap Under the Moat
    rf.assign_rule("Vanish Cap Under the Moat Switch",
                   "CHECKERBOARD_PLATFORMS & WK/TJ/BF/SF/LG | CHECKERBOARD_PLATFORMS & MOVELESS")
    rf.assign_rule("Vanish Cap Under the Moat Red Coins",
                   "CHECKERBOARD_PLATFORMS & TJ/BF/SF/LG/WK & VC | CHECKERBOARD_PLATFORMS & CAPLESS & WK")
    # Bowser in the Fire Sea
    rf.assign_rule("Bowser in the Fire Sea - Upper", "CL")
    rf.assign_rule("Bowser in the Fire Sea Red Coins", "LG/WK")
    rf.assign_rule("Bowser in the Fire Sea 1Up Block Near Poles", "LG/WK")
    # Wing Mario Over the Rainbow
    rf.assign_rule("Wing Mario Over the Rainbow Red Coins", "TJ+WC")
    rf.assign_rule("Wing Mario Over the Rainbow 1Up Block", "TJ+WC")
    # Bowser in the Sky
    rf.assign_rule("Bowser in the Sky - Top", "CL+TJ | CL+SF+LG | MOVELESS & TJ+WK+LG")
    # 100 Coin Stars
    if options.enable_coin_stars:
        rf.assign_rule("Bob-omb Battlefield - 100 Coins", "CANN & WC | CANNLESS & WC & TJ")
        rf.assign_rule("Whomp's Fortress - 100 Coins",
                       "GP | {Whomp's Fortress - Top} & WF_FORTRESS & WK & TJ/SF | "
                       "{Whomp's Fortress - Top} & WF_FORTRESS & CANN")
        rf.assign_rule("Jolly Roger Bay - 100 Coins", "GP & {Jolly Roger Bay - Upper}")
        rf.assign_rule("Hazy Maze Cave - 100 Coins", "GP")
        rf.assign_rule("Shifting Sand Land - 100 Coins", "{Shifting Sand Land - Upper Pyramid} | GP")
        rf.assign_rule("Dire, Dire Docks - 100 Coins", "GP & {{Dire, Dire Docks - Pole-Jumping for Red Coins}}")
        rf.assign_rule("Snowman's Land - 100 Coins", "VC | CAPLESS")
        rf.assign_rule("Wet-Dry World - 100 Coins", "GP | {Wet-Dry World - Downtown}")
        rf.assign_rule("Tick Tock Clock - 100 Coins", "GP")
        rf.assign_rule("Tiny-Huge Island - 100 Coins", "GP & {Tiny-Huge Island (Huge)} | GP & {Tiny-Huge Island - Pipes}")
        rf.assign_rule("Rainbow Ride - 100 Coins", "GP & WK")
    # Castle Stars
    add_rule(multiworld.get_location("Toad (Basement)", player),
             lambda state: state.can_reach("Basement", 'Region', player) and state.has("Castle Toads", player))
    add_rule(multiworld.get_location("Toad (Second Floor)", player),
             lambda state: state.can_reach("Second Floor", 'Region', player) and state.has("Castle Toads", player))
    add_rule(multiworld.get_location("Toad (Third Floor)", player),
             lambda state: state.can_reach("Third Floor", 'Region', player) and state.has("Castle Toads", player))
    add_rule(multiworld.get_location("Yoshi", player),
             lambda state: state.has("Castle Cannon", player) and state.has("Yoshi", player))

    rf.assign_rule("MIPS 1", "DV | MOVELESS")
    rf.assign_rule("MIPS 2", "DV | MOVELESS")
    add_rule(multiworld.get_location("MIPS 1", player),
             lambda state: state.can_reach("Basement", 'Region', player) and state.has("Progressive MIPS", player))
    add_rule(multiworld.get_location("MIPS 2", player),
             lambda state: state.can_reach("Basement", 'Region', player) and
             state.has("Progressive MIPS", player, 2))

    ensure_reachable_starting_check(
        multiworld, options, player, randomized_entrances, randomized_entrances_s, randomized_entrance_connections)

    # Destination Format: LVL | AREA with LVL = LEVEL_x, AREA = Area as used in sm64 code
    # Cast to int to not rely on availability of SM64Levels enum. Will cause crash in MultiServer otherwise
    area_connections.update({int(entrance_lvl): int(sm64_entrances_to_level[destination])
                             for (entrance_lvl, destination) in randomized_entrances.items()})

    multiworld.completion_condition[player] = lambda state: state.can_reach("Bowser in the Sky - Top", 'Region', player)

    if options.completion_type == options.completion_type.option_Last_Bowser_Stage:
        multiworld.completion_condition[player] = lambda state: state.can_reach("Bowser in the Sky - Top", 'Region', player)
    elif options.completion_type == options.completion_type.option_All_Bowser_Stages:
        multiworld.completion_condition[player] = lambda state: state.can_reach("Bowser in the Dark World", 'Region', player) and \
                                                           state.can_reach("Bowser in the Fire Sea - Upper", 'Region', player) and \
                                                           state.can_reach("Bowser in the Sky - Top", 'Region', player)


class RuleFactory:

    multiworld: MultiWorld
    player: int
    move_rando_bitvec: bool
    area_randomizer: bool
    capless: bool
    cannonless: bool
    moveless: bool

    global_cap_item_name_by_token = {
        "WC": "Wing Cap",
        "MC": "Metal Cap",
        "VC": "Vanish Cap",
    }
    token_table = {
        "TJ": "Triple Jump",
        "DJ": "Triple Jump",
        "LJ": "Long Jump",
        "BF": "Backflip",
        "SF": "Side Flip",
        "WK": "Wall Kick",
        "DV": "Dive",
        "GP": "Ground Pound",
        "KK": "Kick",
        "CL": "Climb",
        "LG": "Ledge Grab",
        "BOB_KING": "Bob-omb Battlefield - King Bob-omb",
        "BOB_KOOPA": "Bob-omb Battlefield - Koopa the Quick",
        "BOB_BUDDY": "Bob-omb Battlefield - Bob-omb Buddy",
        "WF_KING": "Whomp's Fortress - Whomp King",
        "WF_FORTRESS": "Whomp's Fortress - Fortress",
        "WF_BUDDY": "Whomp's Fortress - Bob-omb Buddy",
        "WF_HOOT": "Whomp's Fortress - Hoot",
        "CCM_SNOWMAN_HEAD": "Cool, Cool Mountain - Snowman's Head",
        "CCM_BIG_PENGUIN": "Cool, Cool Mountain - Big Penguin",
        "JRB_SUNKEN_SHIP": "Jolly Roger Bay - Sunken Ship",
        "JRB_RAISED_SHIP": "Jolly Roger Bay - Raised Ship",
        "JRB_BUDDY": "Jolly Roger Bay - Bob-omb Buddy",
        "JRB_JET_STREAM": "Jolly Roger Bay - Jet Stream",
        "JRB_UNAGI": "Jolly Roger Bay - Unagi",
        "LLL_KOOPA_SHELL": "Lethal Lava Land - Koopa Shell",
        "SSL_KLEPTO": "Shifting Sand Land - Klepto Star",
        "THI_KOOPA": "Tiny-Huge Island - Koopa the Quick",
        "TTM_UKIKI": "Tall, Tall Mountain - Ukiki",
        "DDD_MANTA_RAY": "Dire, Dire Docks - Manta Ray",
        "DDD_BOWSER_SUB": "Dire, Dire Docks - Bowser's Sub",
        "DDD_POLES": "Dire, Dire Docks - Poles",
        "BBH_STAIRCASE": "Big Boo's Haunt - Staircase",
        "BBH_MERRY_GO_ROUND": "Big Boo's Haunt - Merry-go-round",
        "HMC_SWIMMING_BEAST": "Hazy Maze Cave - Swimming Beast",
        "RR_CARPETS": "Rainbow Ride - Carpets",
        "CHECKERBOARD_PLATFORMS": "Checkerboard Platforms",
        "THI_WARP_PIPES": "Tiny-Huge Island - Warp Pipes",
        "CCM_BABY_PENGUINS": "Cool, Cool Mountain - Baby Penguins",
        "SL_PENGUIN": "Snowman's Land - Penguin",
        "SSL_PYRAMID_ELEVATOR": "Shifting Sand Land - Pyramid Elevator",
        "LLL_ROLLING_LOG": "Lethal Lava Land - Rolling Log",
    }
    cap_item_name_by_token_and_level = {
        "WC": {
            "Bob-omb Battlefield": "Bob-omb Battlefield - Wing Cap",
            "Castle": "Castle - Wing Cap",
            "Lethal Lava Land": "Lethal Lava Land - Wing Cap",
            "Shifting Sand Land": "Shifting Sand Land - Wing Cap",
            "Tower of the Wing Cap": "Tower of the Wing Cap - Wing Cap",
            "Wing Mario Over the Rainbow": "Wing Mario Over the Rainbow - Wing Cap",
            "Wing Mario over the Rainbow": "Wing Mario Over the Rainbow - Wing Cap",
        },
        "MC": {
            "Whomp's Fortress": "Whomp's Fortress - Metal Cap",
            "Jolly Roger Bay": "Jolly Roger Bay - Metal Cap",
            "Hazy Maze Cave": "Hazy Maze Cave - Metal Cap",
            "Dire, Dire Docks": "Dire, Dire Docks - Metal Cap",
            "Wet-Dry World": "Wet-Dry World - Metal Cap",
            "Cavern of the Metal Cap": "Cavern of the Metal Cap - Metal Cap",
            "Bowser in the Dark World": "Bowser in the Dark World - Metal Cap",
        },
        "VC": {
            "Big Boo's Haunt": "Big Boo's Haunt - Vanish Cap",
            "Dire, Dire Docks": "Dire, Dire Docks - Vanish Cap",
            "Snowman's Land": "Snowman's Land - Vanish Cap",
            "Vanish Cap Under the Moat": "Vanish Cap Under the Moat - Vanish Cap",
            "Vanish Cap under the Moat": "Vanish Cap Under the Moat - Vanish Cap",
            "Wet-Dry World": "Wet-Dry World - Vanish Cap",
        },
    }

    class SM64LogicException(Exception):
        pass

    def __init__(self, multiworld, options: SM64Options, player: int, move_rando_bitvec: int):
        self.multiworld = multiworld
        self.player = player
        self.move_rando_bitvec = move_rando_bitvec
        self.area_randomizer = options.area_rando > 0
        self.painting_randomizer = options.enable_locked_paintings
        self.capless = not options.strict_cap_requirements
        self.cannonless = not options.strict_cannon_requirements
        self.moveless = not options.strict_move_requirements
        self.per_level_caps = options.per_level_cap_items

    def assign_rule(self, target_name: str, rule_expr: str):
        target = self.multiworld.get_location(target_name, self.player) if target_name in location_table else self.multiworld.get_entrance(target_name, self.player)
        cannon_name = "Cannon Unlock " + target_name.split(" - ", 1)[0]
        try:
            rule = self.build_rule(rule_expr, cannon_name, self.get_cap_item_names(target_name))
        except RuleFactory.SM64LogicException as exception:
            raise RuleFactory.SM64LogicException(
                f"Error generating rule for {target_name} using rule expression {rule_expr}: {exception}")
        if rule:
            set_rule(target, rule)

    def build_rule(
            self, rule_expr: str, cannon_name: str = '', cap_item_names: dict[str, str] | None = None,
            painting_lvl_name: str = None, star_num_req: int = None) -> Callable:
        # Star/painting requirements are outer and'd requirements, logically (painting? star? and (rule_expr))
        base_rule = self.build_star_painting_entry_requirements(painting_lvl_name, star_num_req)
        if cap_item_names is None:
            cap_item_names = {}
        expressions = rule_expr.split(" | ") if len(rule_expr) > 0 else []
        rules = []
        for expression in expressions:
            or_clause = self.combine_and_clauses(expression, cannon_name, cap_item_names)
            if or_clause is True:
                return base_rule
            if or_clause is not False:
                rules.append(or_clause)
        if rules:
            if len(rules) == 1:
                return lambda state: base_rule(state) and rules[0](state)
            else:
                return lambda state: base_rule(state) and any(rule(state) for rule in rules)
        else:
            return base_rule

    def build_star_painting_entry_requirements(self, painting_lvl_name: str = None, star_num_req: int = None) -> Callable:
        nop_condition = lambda state: True
        star_rule = nop_condition
        painting_rule = nop_condition
        if painting_lvl_name is not None and self.painting_randomizer:
            painting_item_name = f"Painting Unlock {painting_lvl_name}"
            painting_rule = lambda state: state.has(painting_item_name, self.player)
        return lambda state: star_rule(state) and painting_rule(state)

    def get_level_name_from_target(self, target_name: str) -> str:
        if " - " in target_name:
            return target_name.split(" - ", 1)[0]
        for level_name in (
                "Tower of the Wing Cap",
                "Cavern of the Metal Cap",
                "Vanish Cap Under the Moat",
                "Vanish Cap under the Moat",
                "Wing Mario Over the Rainbow",
                "Wing Mario over the Rainbow",
                "Bowser in the Dark World",
        ):
            if target_name.startswith(level_name):
                return level_name
        return "Castle"

    def get_cap_item_names(self, target_name: str) -> dict[str, str]:
        level_name = self.get_level_name_from_target(target_name)
        return {
            token: item_name_by_level[level_name]
            for token, item_name_by_level in self.cap_item_name_by_token_and_level.items()
            if level_name in item_name_by_level
        }

    def combine_and_clauses(self, rule_expr: str, cannon_name: str, cap_item_names: dict[str, str]) -> Union[Callable, bool]:
        expressions = rule_expr.split(" & ")
        rules = []
        for expression in expressions:
            and_clause = self.make_lambda(expression, cannon_name, cap_item_names)
            if and_clause is False:
                return False
            if and_clause is not True:
                rules.append(and_clause)
        if rules:
            if len(rules) == 1:
                return rules[0]
            return lambda state: all(rule(state) for rule in rules)
        else:
            return True

    def make_lambda(self, expression: str, cannon_name: str, cap_item_names: dict[str, str]) -> Union[Callable, bool]:
        if '+' in expression:
            tokens = expression.split('+')
            items = set()
            for token in tokens:
                item = self.parse_token(token, cannon_name, cap_item_names)
                if item is True:
                    continue
                if item is False:
                    return False
                items.add(item)
            if items:
                return lambda state: state.has_all(items, self.player)
            else:
                return True
        if '/' in expression:
            tokens = expression.split('/')
            items = set()
            for token in tokens:
                item = self.parse_token(token, cannon_name, cap_item_names)
                if item is True:
                    return True
                if item is False:
                    continue
                items.add(item)
            if items:
                return lambda state: state.has_any(items, self.player)
            else:
                return False
        if '{{' in expression:
            return lambda state: state.can_reach(expression[2:-2], "Location", self.player)
        if '{' in expression:
            return lambda state: state.can_reach(expression[1:-1], "Region", self.player)
        item = self.parse_token(expression, cannon_name, cap_item_names)
        if item in (True, False):
            return item
        return lambda state: state.has(item, self.player)

    def parse_token(self, token: str, cannon_name: str, cap_item_names: dict[str, str]) -> Union[str, bool]:
        if token == "CANN":
            return cannon_name
        if token in self.global_cap_item_name_by_token:
            if not self.per_level_caps:
                return self.global_cap_item_name_by_token[token]
            item = cap_item_names.get(token)
            if not item:
                raise RuleFactory.SM64LogicException(f"No per-level cap item for token '{token}' in this target.")
            return item
        if token == "CAPLESS":
            return self.capless
        if token == "CANNLESS":
            return self.cannonless
        if token == "MOVELESS":
            return self.moveless
        if token == "NAR":
            return not self.area_randomizer
        item = self.token_table.get(token, None)
        if not item:
            raise Exception(f"Invalid token: '{item}'")
        if item in action_item_data_table:
            double_jump_bitvec_offset = action_item_data_table['Double Jump'].code
            if self.move_rando_bitvec & (1 << (action_item_data_table[item].code - double_jump_bitvec_offset)) == 0:
                # This action item is not randomized.
                return True
        elif item in cap_item_data_table:
            return item
        return item
