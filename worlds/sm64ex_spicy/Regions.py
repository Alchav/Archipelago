import typing
from enum import Enum

from BaseClasses import MultiWorld, Region, Entrance, Location
from .Options import SM64Options
from .Locations import SM64Location, location_table, locBoB_table, locWhomp_table, locJRB_table, locCCM_table, \
    locBBH_table, \
    locHMC_table, locLLL_table, locSSL_table, locDDD_table, locSL_table, \
    locWDW_table, locTTM_table, locTHI_table, locTTC_table, locRR_table, \
    locPSS_table, locSA_table, locBitDW_table, locTotWC_table, locCotMC_table, \
    locVCutM_table, locBitFS_table, locWMotR_table, locBitS_table, locSS_table


class SM64Levels(int, Enum):
    BOB_OMB_BATTLEFIELD = 91
    WHOMPS_FORTRESS = 241
    JOLLY_ROGER_BAY = 121
    COOL_COOL_MOUNTAIN = 51
    BIG_BOOS_HAUNT = 41
    HAZY_MAZE_CAVE = 71
    LETHAL_LAVA_LAND = 221
    SHIFTING_SAND_LAND = 81
    DIRE_DIRE_DOCKS = 231
    SNOWMANS_LAND = 101
    WET_DRY_WORLD = 111
    TALL_TALL_MOUNTAIN = 361
    TINY_HUGE_ISLAND_TINY = 132
    TINY_HUGE_ISLAND_HUGE = 131
    TICK_TOCK_CLOCK = 141
    RAINBOW_RIDE = 151
    THE_PRINCESS_SECRET_SLIDE = 271
    THE_SECRET_AQUARIUM = 201
    BOWSER_IN_THE_DARK_WORLD = 171
    TOWER_OF_THE_WING_CAP = 291
    CAVERN_OF_THE_METAL_CAP = 281
    VANISH_CAP_UNDER_THE_MOAT = 181
    BOWSER_IN_THE_FIRE_SEA = 191
    WING_MARIO_OVER_THE_RAINBOW = 311


class SM64Region(Region):
    subregions: typing.List[Region] = []


SM64_WDW_LOW = int(SM64Levels.WET_DRY_WORLD)
SM64_WDW_MIDDLE = SM64_WDW_LOW + 1
SM64_WDW_HIGH = SM64_WDW_LOW + 2

SM64_TTC_STOPPED = int(SM64Levels.TICK_TOCK_CLOCK)
SM64_TTC_SLOW = SM64_TTC_STOPPED + 1
SM64_TTC_RANDOM = SM64_TTC_STOPPED + 2
SM64_TTC_FAST = SM64_TTC_STOPPED + 3

sm64_wdw_entrances = (
    "Wet-Dry World Low",
    "Wet-Dry World Middle",
    "Wet-Dry World High",
)

sm64_ttc_entrances = (
    "Tick Tock Clock Stopped Entrance",
    "Tick Tock Clock Slow",
    "Tick Tock Clock Random",
    "Tick Tock Clock Fast",
)

# sm64paintings is a dict of entrances, format LEVEL | AREA
sm64_level_to_paintings: typing.Dict[int, str] = {
    SM64Levels.BOB_OMB_BATTLEFIELD: "Bob-omb Battlefield",
    SM64Levels.WHOMPS_FORTRESS: "Whomp's Fortress",
    SM64Levels.JOLLY_ROGER_BAY: "Jolly Roger Bay",
    SM64Levels.COOL_COOL_MOUNTAIN: "Cool, Cool Mountain",
    SM64Levels.BIG_BOOS_HAUNT: "Big Boo's Haunt",
    SM64Levels.HAZY_MAZE_CAVE: "Hazy Maze Cave",
    SM64Levels.LETHAL_LAVA_LAND: "Lethal Lava Land",
    SM64Levels.SHIFTING_SAND_LAND: "Shifting Sand Land",
    SM64Levels.DIRE_DIRE_DOCKS: "Dire, Dire Docks",
    SM64Levels.SNOWMANS_LAND: "Snowman's Land",
    SM64_WDW_LOW: "Wet-Dry World Low",
    SM64_WDW_MIDDLE: "Wet-Dry World Middle",
    SM64_WDW_HIGH: "Wet-Dry World High",
    SM64Levels.TALL_TALL_MOUNTAIN: "Tall, Tall Mountain",
    SM64Levels.TINY_HUGE_ISLAND_TINY: "Tiny-Huge Island (Tiny)",
    SM64Levels.TINY_HUGE_ISLAND_HUGE: "Tiny-Huge Island (Huge)",
    SM64_TTC_STOPPED: "Tick Tock Clock Stopped Entrance",
    SM64_TTC_SLOW: "Tick Tock Clock Slow",
    SM64_TTC_RANDOM: "Tick Tock Clock Random",
    SM64_TTC_FAST: "Tick Tock Clock Fast",
    SM64Levels.RAINBOW_RIDE: "Rainbow Ride"
}
sm64_paintings_to_level = {painting: level for (level, painting) in sm64_level_to_paintings.items() }

# sm64secrets is a dict of secret areas, same format as sm64paintings
sm64_level_to_secrets: typing.Dict[SM64Levels, str] = {
    SM64Levels.THE_PRINCESS_SECRET_SLIDE: "The Princess's Secret Slide",
    SM64Levels.THE_SECRET_AQUARIUM: "The Secret Aquarium",
    SM64Levels.BOWSER_IN_THE_DARK_WORLD: "Bowser in the Dark World",
    SM64Levels.TOWER_OF_THE_WING_CAP: "Tower of the Wing Cap",
    SM64Levels.CAVERN_OF_THE_METAL_CAP: "Cavern of the Metal Cap",
    SM64Levels.VANISH_CAP_UNDER_THE_MOAT: "Vanish Cap under the Moat",
    SM64Levels.BOWSER_IN_THE_FIRE_SEA: "Bowser in the Fire Sea",
    SM64Levels.WING_MARIO_OVER_THE_RAINBOW: "Wing Mario over the Rainbow"
}
sm64_secrets_to_level = {secret: level for (level,secret) in sm64_level_to_secrets.items() }

sm64_entrances_to_level = {**sm64_paintings_to_level, **sm64_secrets_to_level }
sm64_entrances_to_level["Wet-Dry World"] = SM64_WDW_LOW
sm64_entrances_to_level["Tick Tock Clock"] = SM64_TTC_STOPPED
sm64_level_to_entrances = {**sm64_level_to_paintings, **sm64_level_to_secrets }

sm64_entrance_to_region = {
    **{entrance: entrance for entrance in sm64_entrances_to_level},
    "Tick Tock Clock Stopped Entrance": "Tick Tock Clock Stopped",
    "Tick Tock Clock Slow": "Tick Tock Clock Moving",
    "Tick Tock Clock Random": "Tick Tock Clock Moving",
    "Tick Tock Clock Fast": "Tick Tock Clock Moving",
}

def create_regions(multiworld: MultiWorld, options: SM64Options, player: int):
    regSS = Region("Menu", player, multiworld, "Castle Area")
    create_default_locs(regSS, locSS_table)
    multiworld.regions.append(regSS)

    regBoB = create_region("Bob-omb Battlefield", player, multiworld)
    create_locs(regBoB, "Bob-omb Battlefield - Big Bob-Omb on the Summit", "Bob-omb Battlefield - Footrace with Koopa The Quick",
                        "Bob-omb Battlefield - Mario Wings to the Sky", "Bob-omb Battlefield - Behind Chain Chomp's Gate", "Bob-omb Battlefield - Bob-omb Buddy")
    bob_island = create_subregion(regBoB, "Bob-omb Battlefield - Island", "Bob-omb Battlefield - Shoot to the Island in the Sky", "Bob-omb Battlefield - Find the 8 Red Coins")
    regBoB.subregions = [bob_island]
    if options.enable_coin_stars:
        create_locs(regBoB, "Bob-omb Battlefield - Coins Star")

    regWhomp = create_region("Whomp's Fortress", player, multiworld)
    create_locs(regWhomp, "Whomp's Fortress - Shoot into the Wild Blue",
                          "Whomp's Fortress - Fall onto the Caged Island", "Whomp's Fortress - Blast Away the Wall",
                          "Whomp's Fortress - Bob-omb Buddy")
    wf_top = create_subregion(regWhomp, "Whomp's Fortress - Top",
                              "Whomp's Fortress - Chip Off Whomp's Block",
                              "Whomp's Fortress - Red Coins on the Floating Isle",
                              "Whomp's Fortress - To the Top of the Fortress")
    regWhomp.subregions = [wf_top]
    if options.enable_coin_stars:
        create_locs(regWhomp, "Whomp's Fortress - Coins Star")

    regJRBDoor = create_region("Jolly Roger Bay Door", player, multiworld)
    regJRB = create_region("Jolly Roger Bay", player, multiworld)
    create_locs(regJRB, "Jolly Roger Bay - Plunder in the Sunken Ship", "Jolly Roger Bay - Can the Eel Come Out to Play?", "Jolly Roger Bay - Treasure of the Ocean Cave",
                        "Jolly Roger Bay - Blast to the Stone Pillar", "Jolly Roger Bay - Through the Jet Stream", "Jolly Roger Bay - Bob-omb Buddy")
    jrb_upper = create_subregion(regJRB, 'Jolly Roger Bay - Upper', "Jolly Roger Bay - Red Coins on the Ship Afloat")
    regJRB.subregions = [jrb_upper]
    if options.enable_coin_stars:
        create_locs(regJRB, "Jolly Roger Bay - Coins Star")

    regCCM = create_region("Cool, Cool Mountain", player, multiworld)
    create_default_locs(regCCM, locCCM_table)
    if options.enable_coin_stars:
        create_locs(regCCM, "Cool, Cool Mountain - Coins Star")

    regBBH = create_region("Big Boo's Haunt", player, multiworld)
    create_locs(regBBH, "Big Boo's Haunt - Go on a Ghost Hunt", "Big Boo's Haunt - Ride Big Boo's Merry-Go-Round")
    bbh_second_floor = create_subregion(regBBH, "Big Boo's Haunt - Second Floor",
                                        "Big Boo's Haunt - Secret of the Haunted Books",
                                        "Big Boo's Haunt - Seek the 8 Red Coins")
    bbh_third_floor = create_subregion(bbh_second_floor, "Big Boo's Haunt - Third Floor",
                                       "Big Boo's Haunt - Eye to Eye in the Secret Room")
    bbh_roof = create_subregion(bbh_third_floor, "Big Boo's Haunt - Roof", "Big Boo's Haunt - Big Boo's Balcony", "Big Boo's Haunt - 1Up Block Top of Mansion")
    regBBH.subregions = [bbh_second_floor, bbh_third_floor, bbh_roof]
    if options.enable_coin_stars:
        create_locs(regBBH, "Big Boo's Haunt - Coins Star")

    regPSS = create_region("The Princess's Secret Slide", player, multiworld)
    create_default_locs(regPSS, locPSS_table)

    regSA = create_region("The Secret Aquarium", player, multiworld)
    create_default_locs(regSA, locSA_table)

    regTotWC = create_region("Tower of the Wing Cap", player, multiworld)
    create_default_locs(regTotWC, locTotWC_table)

    regBitDW = create_region("Bowser in the Dark World", player, multiworld)
    create_default_locs(regBitDW, locBitDW_table)

    create_region("Basement", player, multiworld)

    regHMC = create_region("Hazy Maze Cave", player, multiworld)
    create_locs(regHMC, "Hazy Maze Cave - Swimming Beast in the Cavern", "Hazy Maze Cave - Metal-Head Mario Can Move!",
                        "Hazy Maze Cave - Watch for Rolling Rocks", "Hazy Maze Cave - Navigating the Toxic Maze","Hazy Maze Cave - 1Up Block Past Rolling Rocks")
    hmc_red_coin_area = create_subregion(regHMC, "Hazy Maze Cave - Red Coin Area", "Hazy Maze Cave - Elevate for 8 Red Coins")
    hmc_pit_islands = create_subregion(regHMC, "Hazy Maze Cave - Pit Islands", "Hazy Maze Cave - A-Maze-Ing Emergency Exit", "Hazy Maze Cave - 1Up Block above Pit")
    regHMC.subregions = [hmc_red_coin_area, hmc_pit_islands]
    if options.enable_coin_stars:
        create_locs(regHMC, "Hazy Maze Cave - Coins Star")

    regLLL = create_region("Lethal Lava Land", player, multiworld)
    create_locs(regLLL, "Lethal Lava Land - Boil the Big Bully", "Lethal Lava Land - Bully the Bullies",
                        "Lethal Lava Land - 8-Coin Puzzle with 15 Pieces", "Lethal Lava Land - Red-Hot Log Rolling")
    lll_upper_volcano = create_subregion(regLLL, "Lethal Lava Land - Upper Volcano", "Lethal Lava Land - Hot-Foot-It into the Volcano", "Lethal Lava Land - Elevator Tour in the Volcano")
    regLLL.subregions = [lll_upper_volcano]
    if options.enable_coin_stars:
        create_locs(regLLL, "Lethal Lava Land - Coins Star")

    regSSL = create_region("Shifting Sand Land", player, multiworld)
    create_locs(regSSL, "Shifting Sand Land - In the Talons of the Big Bird", "Shifting Sand Land - Shining Atop the Pyramid",
                        "Shifting Sand Land - Free Flying for 8 Red Coins", "Shifting Sand Land - Bob-omb Buddy",
                        "Shifting Sand Land - 1Up Block Outside Pyramid", "Shifting Sand Land - 1Up Block Pyramid Left Path", "Shifting Sand Land - 1Up Block Pyramid Back")
    ssl_upper_pyramid = create_subregion(regSSL, "Shifting Sand Land - Upper Pyramid", "Shifting Sand Land - Inside the Ancient Pyramid",
                                         "Shifting Sand Land - Stand Tall on the Four Pillars", "Shifting Sand Land - Pyramid Puzzle")
    regSSL.subregions = [ssl_upper_pyramid]
    if options.enable_coin_stars:
        create_locs(regSSL, "Shifting Sand Land - Coins Star")

    regDDD = create_region("Dire, Dire Docks", player, multiworld)
    create_locs(regDDD, "Dire, Dire Docks - Board Bowser's Sub", "Dire, Dire Docks - Chests in the Current", "Dire, Dire Docks - Through the Jet Stream",
                        "Dire, Dire Docks - The Manta Ray's Reward", "Dire, Dire Docks - Collect the Caps...", "Dire, Dire Docks - Pole-Jumping for Red Coins")
    if options.enable_coin_stars:
        create_locs(regDDD, "Dire, Dire Docks - Coins Star")

    regCotMC = create_region("Cavern of the Metal Cap", player, multiworld)
    create_default_locs(regCotMC, locCotMC_table)

    regVCutM = create_region("Vanish Cap under the Moat", player, multiworld)
    create_default_locs(regVCutM, locVCutM_table)

    regBitFS = create_region("Bowser in the Fire Sea", player, multiworld)
    bitfs_upper = create_subregion(regBitFS, "Bowser in the Fire Sea - Upper", *locBitFS_table.keys())
    regBitFS.subregions = [bitfs_upper]

    create_region("Second Floor", player, multiworld)

    regSL = create_region("Snowman's Land", player, multiworld)
    create_default_locs(regSL, locSL_table)
    if options.enable_coin_stars:
        create_locs(regSL, "Snowman's Land - Coins Star")

    regWDWLow = create_region("Wet-Dry World Low", player, multiworld)
    regWDWMiddle = create_region("Wet-Dry World Middle", player, multiworld)
    regWDWHigh = create_region("Wet-Dry World High", player, multiworld)

    regWDW = create_region("Wet-Dry World", player, multiworld)
    create_locs(regWDW, "Wet-Dry World - Shocking Arrow Lifts!", "Wet-Dry World - Bob-omb Buddy")
    wdw_low_water = create_region("Wet-Dry World - Low Water", player, multiworld)
    create_locs(wdw_low_water, "Wet-Dry World - Express Elevator--Hurry Up!",
                "Wet-Dry World - Secrets in the Shallows & Sky")
    wdw_mid_water = create_region("Wet-Dry World - Mid Water", player, multiworld)
    wdw_mid_high_water = create_region("Wet-Dry World - Mid-High Water", player, multiworld)
    wdw_high_water = create_region("Wet-Dry World - High Water", player, multiworld)
    wdw_highest_water = create_region("Wet-Dry World - Highest Water", player, multiworld)
    wdw_cannon = create_region("Wet-Dry World - Cannon", player, multiworld)
    wdw_top = create_subregion(regWDW, "Wet-Dry World - Top", "Wet-Dry World - Top o' the Town")
    wdw_downtown = create_subregion(regWDW, "Wet-Dry World - Downtown", "Wet-Dry World - Go to Town for Red Coins", "Wet-Dry World - Quick Race Through Downtown!", "Wet-Dry World - 1Up Block in Downtown")
    regWDW.subregions = [
        wdw_low_water, wdw_mid_water, wdw_mid_high_water, wdw_high_water, wdw_highest_water, wdw_cannon,
        wdw_top, wdw_downtown
    ]
    regWDWLow.connect(regWDW)
    regWDWLow.connect(wdw_low_water)
    regWDWMiddle.connect(regWDW)
    regWDWMiddle.connect(wdw_mid_water)
    regWDWHigh.connect(regWDW)
    regWDWHigh.connect(wdw_highest_water)
    wdw_low_water.connect(wdw_mid_water, name="Wet-Dry World - Low Water to Mid Water")
    wdw_mid_water.connect(wdw_low_water, name="Wet-Dry World - Mid Water to Low Water")
    wdw_mid_water.connect(wdw_mid_high_water, name="Wet-Dry World - Mid Water to Mid-High Water")
    wdw_mid_high_water.connect(wdw_mid_water, name="Wet-Dry World - Mid-High Water to Mid Water")
    wdw_mid_high_water.connect(wdw_high_water, name="Wet-Dry World - Mid-High Water to High Water")
    wdw_high_water.connect(wdw_mid_high_water, name="Wet-Dry World - High Water to Mid-High Water")
    wdw_highest_water.connect(wdw_high_water, name="Wet-Dry World - Highest Water to High Water")
    wdw_low_water.connect(wdw_cannon)
    wdw_high_water.connect(wdw_cannon)
    for wdw_entrance_region in (regWDWLow, regWDWMiddle, regWDWHigh):
        wdw_entrance_region.subregions = [regWDW, *regWDW.subregions]
    if options.enable_coin_stars:
        create_locs(regWDW, "Wet-Dry World - Coins Star")

    regTTM = create_region("Tall, Tall Mountain", player, multiworld)
    ttm_middle = create_subregion(regTTM, "Tall, Tall Mountain - Middle", "Tall, Tall Mountain - Scary 'Shrooms, Red Coins", "Tall, Tall Mountain - Blast to the Lonely Mushroom",
                                                         "Tall, Tall Mountain - Bob-omb Buddy", "Tall, Tall Mountain - 1Up Block on Red Mushroom")
    ttm_top = create_subregion(ttm_middle, "Tall, Tall Mountain - Top", "Tall, Tall Mountain - Scale the Mountain", "Tall, Tall Mountain - Mystery of the Monkey Cage",
                                                       "Tall, Tall Mountain - Mysterious Mountainside", "Tall, Tall Mountain - Breathtaking View from Bridge")
    regTTM.subregions = [ttm_middle, ttm_top]
    if options.enable_coin_stars:
        create_locs(regTTM, "Tall, Tall Mountain - Coins Star")

    create_region("Tiny-Huge Island (Huge)", player, multiworld)
    create_region("Tiny-Huge Island (Tiny)", player, multiworld)
    regTHI = create_region("Tiny-Huge Island", player, multiworld)
    create_locs(regTHI, "Tiny-Huge Island - 1Up Block THI Small near Start",
                "Tiny-Huge Island - Five Itty Bitty Secrets")
    thi_pipes = create_subregion(regTHI, "Tiny-Huge Island - Pipes", "Tiny-Huge Island - The Tip Top of the Huge Island", "Tiny-Huge Island - Pluck the Piranha Flower", "Tiny-Huge Island - Rematch with Koopa the Quick",
                                                       "Tiny-Huge Island - Wiggler's Red Coins", "Tiny-Huge Island - Bob-omb Buddy",
                                                       "Tiny-Huge Island - 1Up Block THI Large near Start", "Tiny-Huge Island - 1Up Block Windy Area")
    thi_large_top = create_subregion(thi_pipes, "Tiny-Huge Island - Large Top", "Tiny-Huge Island - Make Wiggler Squirm")
    regTHI.subregions = [thi_pipes, thi_large_top]
    if options.enable_coin_stars:
        create_locs(regTHI, "Tiny-Huge Island - Coins Star")

    regFloor3 = create_region("Third Floor", player, multiworld)

    regTTC = create_region("Tick Tock Clock", player, multiworld)
    ttc_lower = create_subregion(regTTC, "Tick Tock Clock - Lower", "Tick Tock Clock - Roll into the Cage",
                                 "Tick Tock Clock - Get a Hand", "Tick Tock Clock - Stop Time for Red Coins")
    ttc_upper = create_subregion(ttc_lower, "Tick Tock Clock - Upper", "Tick Tock Clock - Timed Jumps on Moving Bars", "Tick Tock Clock - The Pit and the Pendulums")
    ttc_top = create_subregion(ttc_upper, "Tick Tock Clock - Top", "Tick Tock Clock - 1Up Block Midway Up")
    ttc_top_past_spinners = create_subregion(ttc_top, "Tick Tock Clock - Top Past Spinners",
                                             "Tick Tock Clock - Stomp on the Thwomp",
                                             "Tick Tock Clock - 1Up Block at the Top")
    regTTC.subregions = [ttc_lower, ttc_upper, ttc_top, ttc_top_past_spinners]
    regTTCStopped = create_region("Tick Tock Clock Stopped", player, multiworld)
    regTTCStopped.connect(regTTC)
    regTTCStopped.subregions = [regTTC, *regTTC.subregions]
    regTTCMoving = create_region("Tick Tock Clock Moving", player, multiworld)
    regTTCMoving.connect(regTTC)
    regTTCMoving.subregions = [regTTC, *regTTC.subregions]
    if options.enable_coin_stars:
        create_locs(regTTC, "Tick Tock Clock - Coins Star")

    regRR = create_region("Rainbow Ride", player, multiworld)
    rr_carpets = create_subregion(regRR, "Rainbow Ride - Carpets", "Rainbow Ride - Swingin' in the Breeze",
                                  "Rainbow Ride - Tricky Triangles!", "Rainbow Ride - 1Up Block Top of Red Coin Maze",
                                  "Rainbow Ride - 1Up Block Under Fly Guy", "Rainbow Ride - Bob-omb Buddy")
    rr_maze = create_subregion(rr_carpets, "Rainbow Ride - Maze", "Rainbow Ride - Coins Amassed in a Maze")
    rr_cruiser = create_subregion(rr_carpets, "Rainbow Ride - Cruiser", "Rainbow Ride - Cruiser Crossing the Rainbow", "Rainbow Ride - Somewhere Over the Rainbow")
    rr_house = create_subregion(rr_carpets, "Rainbow Ride - House", "Rainbow Ride - The Big House in the Sky", "Rainbow Ride - 1Up Block On House in the Sky")
    regRR.subregions = [rr_carpets, rr_maze, rr_cruiser, rr_house]
    if options.enable_coin_stars:
        create_locs(rr_maze, "Rainbow Ride - Coins Star")

    regWMotR = create_region("Wing Mario over the Rainbow", player, multiworld)
    create_default_locs(regWMotR, locWMotR_table)

    regBitS = create_region("Bowser in the Sky", player, multiworld)
    create_locs(regBitS, "Bowser in the Sky 1Up Block")
    bits_top = create_subregion(regBitS, "Bowser in the Sky - Top", "Bowser in the Sky Red Coins")
    regBitS.subregions = [bits_top]


def connect_regions(multiworld: MultiWorld, player: int, source: str, target: str, rule=None,
                    name: str | None = None) -> Entrance:
    sourceRegion = multiworld.get_region(source, player)
    targetRegion = multiworld.get_region(target, player)
    return sourceRegion.connect(targetRegion, name=name, rule=rule)


def create_region(name: str, player: int, multiworld: MultiWorld) -> SM64Region:
    region = SM64Region(name, player, multiworld)
    multiworld.regions.append(region)
    return region


def create_subregion(source_region: Region, name: str, *locs: str) -> SM64Region:
    region = SM64Region(name, source_region.player, source_region.multiworld)
    connection = Entrance(source_region.player, name, source_region)
    source_region.exits.append(connection)
    connection.connect(region)
    source_region.multiworld.regions.append(region)
    create_locs(region, *locs)
    return region


def set_subregion_access_rule(world, player, region_name: str, rule):
    world.get_entrance(world, player, region_name).access_rule = rule


def create_default_locs(reg: Region, default_locs: dict):
    create_locs(reg, *default_locs.keys())


def create_locs(reg: Region, *locs: str):
    reg.locations += [SM64Location(reg.player, loc_name, location_table[loc_name], reg) for loc_name in locs]
