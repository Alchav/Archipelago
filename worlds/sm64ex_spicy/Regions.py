import typing
from enum import Enum

from BaseClasses import MultiWorld, Region, Entrance, Location
from rule_builder.rules import Rule
from .Options import SM64Options
from .Locations import SM64Location, location_table, locBoB_table, locWhomp_table, locJRB_table, locCCM_table, \
    locBBH_table, \
    locHMC_table, locLLL_table, locSSL_table, locDDD_table, locSL_table, \
    locWDW_table, locTTM_table, locTHI_table, locTTC_table, locRR_table, \
    locPSS_table, locSA_table, locBitDW_table, locTotWC_table, locCotMC_table, \
    locVCutM_table, locBitFS_table, locWMotR_table, locBitS_table, locSS_table, locBasement_table, \
    locOneUp_table, locBlocksanity_table


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
    SM64Levels.VANISH_CAP_UNDER_THE_MOAT: "Vanish Cap Under the Moat",
    SM64Levels.BOWSER_IN_THE_FIRE_SEA: "Bowser in the Fire Sea",
    SM64Levels.WING_MARIO_OVER_THE_RAINBOW: "Wing Mario Over the Rainbow"
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
    create_locs(regSS,
                "Castle - Toad (Basement)",
                "Castle - Toad (Second Floor)",
                "Castle - Toad (Third Floor)",
                "Castle - MIPS 1",
                "Castle - MIPS 2",
                "Castle - Third Tree From Waterfall 1-Up",
                "Castle - Bridge Coins 1-Up",
                "Castle - Left Butterfly 1-Up",
                "Castle - Right Butterfly 1-Up",
                "Castle - Jolly Roger Bay Lobby 1-Up")
    multiworld.regions.append(regSS)
    castle_roof = create_subregion(regSS, "Castle - Roof",
                                   "Castle - Yoshi",
                                   "Castle - Roof Back 1-Up",
                                   "Castle - Roof Center 1-Up",
                                   "Castle - Roof Front 1-Up",
                                   "Castle - Roof Wing Cap Block")
    regSS.subregions = [castle_roof]

    regBoB = create_region("Bob-omb Battlefield", player, multiworld)
    create_locs(regBoB, "Bob-omb Battlefield - Big Bob-Omb on the Summit", "Bob-omb Battlefield - Footrace with Koopa The Quick",
                        "Bob-omb Battlefield - Mario Wings to the Sky", "Bob-omb Battlefield - Behind Chain Chomp's Gate", "Bob-omb Battlefield - Bob-omb Buddy",
                        "Bob-omb Battlefield - Flower Ring 1-Up", "Bob-omb Battlefield - Switch Platform 1-Up",
                        "Bob-omb Battlefield - Near Flower Patches Wing Cap Block",
                        "Bob-omb Battlefield - Wooden Ramp Wing Cap Block")
    bob_island = create_subregion(regBoB, "Bob-omb Battlefield - Island",
                                  "Bob-omb Battlefield - Shoot to the Island in the Sky",
                                  "Bob-omb Battlefield - Find the 8 Red Coins",
                                  "Bob-omb Battlefield - Cannon Tree 1-Up",
                                  "Bob-omb Battlefield - Island Wing Cap Block",
                                  "Bob-omb Battlefield - Shoot to the Island in the Sky Star Block")
    regBoB.subregions = [bob_island]
    create_locs(regBoB, "Bob-omb Battlefield - Coins Star")

    regWhomp = create_region("Whomp's Fortress", player, multiworld)
    create_locs(regWhomp, "Whomp's Fortress - Shoot into the Wild Blue",
                          "Whomp's Fortress - Fall onto the Caged Island", "Whomp's Fortress - Blast Away the Wall",
                          "Whomp's Fortress - Bob-omb Buddy", "Whomp's Fortress - Flower Patch Butterfly 1-Up",
                          "Whomp's Fortress - Metal Cap Block")
    wf_top = create_subregion(regWhomp, "Whomp's Fortress - Top",
                              "Whomp's Fortress - Chip Off Whomp's Block",
                              "Whomp's Fortress - Red Coins on the Floating Isle",
                              "Whomp's Fortress - To the Top of the Fortress",
                              "Whomp's Fortress - Flagpole 1-Up",
                              "Whomp's Fortress - Rotating Platform Coins 1-Up",
                              "Whomp's Fortress - Tower Alcove 1-Up")
    regWhomp.subregions = [wf_top]
    create_locs(regWhomp, "Whomp's Fortress - Coins Star")

    regJRBDoor = create_region("Jolly Roger Bay Door", player, multiworld)
    regJRB = create_region("Jolly Roger Bay", player, multiworld)
    create_locs(regJRB, "Jolly Roger Bay - Plunder in the Sunken Ship", "Jolly Roger Bay - Can the Eel Come Out to Play?", "Jolly Roger Bay - Treasure of the Ocean Cave",
                        "Jolly Roger Bay - Blast to the Stone Pillar", "Jolly Roger Bay - Through the Jet Stream", "Jolly Roger Bay - Bob-omb Buddy",
                        "Jolly Roger Bay - Underwater Coin Ring 1-Up", "Jolly Roger Bay - Stone Pillar 1-Up",
                        "Jolly Roger Bay - Beginning Metal Cap Block",
                        "Jolly Roger Bay - 3 Coins Block",
                        "Jolly Roger Bay - Ocean Cave Metal Cap Block",
                        "Jolly Roger Bay - Blast to the Stone Pillar Star Block",
                        "Jolly Roger Bay - Plunder in the Sunken Ship Star Block")
    jrb_upper = create_subregion(regJRB, 'Jolly Roger Bay - Upper',
                                 "Jolly Roger Bay - Red Coins on the Ship Afloat",
                                 "Jolly Roger Bay - Purple Switch Metal Cap Block")
    regJRB.subregions = [jrb_upper]
    create_locs(regJRB, "Jolly Roger Bay - Coins Star")

    regCCM = create_region("Cool, Cool Mountain", player, multiworld)
    create_default_locs(regCCM, locCCM_table)
    create_locs(regCCM,
                "Cool, Cool Mountain - Snowman Tree 1-Up",
                "Cool, Cool Mountain - Slide Shortcut First 1-Up",
                "Cool, Cool Mountain - Near Snowman 1-Up Block",
                "Cool, Cool Mountain - Ice Pillar 1-Up Block",
                "Cool, Cool Mountain - Secret Slide 1-Up Block")
    if options.no_despawns:
        create_locs(regCCM, "Cool, Cool Mountain - Slide Shortcut Second 1-Up")
    create_locs(regCCM, "Cool, Cool Mountain - Coins Star")

    regBBH = create_region("Big Boo's Haunt", player, multiworld)
    create_locs(regBBH, "Big Boo's Haunt - Go on a Ghost Hunt", "Big Boo's Haunt - Ride Big Boo's Merry-Go-Round",
                "Big Boo's Haunt - Shed Roof 1-Up",
                "Big Boo's Haunt - Back Entrance Vanish Cap Block",
                "Big Boo's Haunt - 10 Coins Block")
    bbh_second_floor = create_subregion(regBBH, "Big Boo's Haunt - Second Floor",
                                        "Big Boo's Haunt - Secret of the Haunted Books",
                                        "Big Boo's Haunt - Seek the 8 Red Coins",
                                        "Big Boo's Haunt - Second Floor Vanish Cap Block")
    bbh_third_floor = create_subregion(bbh_second_floor, "Big Boo's Haunt - Third Floor",
                                       "Big Boo's Haunt - Eye to Eye in the Secret Room",
                                       "Big Boo's Haunt - Secret Room Vanish Cap Block")
    bbh_roof = create_subregion(bbh_third_floor, "Big Boo's Haunt - Roof",
                                "Big Boo's Haunt - Big Boo's Balcony",
                                "Big Boo's Haunt - Top of Mansion Block 1-Up",
                                "Big Boo's Haunt - Top of Mansion 1-Up Block")
    regBBH.subregions = [bbh_second_floor, bbh_third_floor, bbh_roof]
    create_locs(regBBH, "Big Boo's Haunt - Coins Star")

    regPSS = create_region("The Princess's Secret Slide", player, multiworld)
    create_default_locs(regPSS, locPSS_table)
    create_locs(regPSS,
                "The Princess's Secret Slide - Coin Triggers 1-Up",
                "The Princess's Secret Slide - Slide 1-Up",
                "The Princess's Secret Slide - Star Block")

    regSA = create_region("The Secret Aquarium", player, multiworld)
    create_default_locs(regSA, locSA_table)
    create_locs(regSA, "The Secret Aquarium - Center Coin Ring 1-Up")

    regTotWC = create_region("Tower of the Wing Cap", player, multiworld)
    create_default_locs(regTotWC, locTotWC_table)
    create_locs(regTotWC, "Tower of the Wing Cap - Wing Cap Block")

    regBitDW = create_region("Bowser in the Dark World", player, multiworld)
    create_default_locs(regBitDW, locBitDW_table)
    create_locs(regBitDW,
                "Bowser in the Dark World - Center Overhang 1-Up",
                "Bowser in the Dark World - Right Tilting Platform Base 1-Up",
                "Bowser in the Dark World - Left Tilting Platform Base 1-Up",
                "Bowser in the Dark World - Far Overhang 1-Up",
                "Bowser in the Dark World - Metal Cap Block",
                "Bowser in the Dark World - 3 Coins Block",
                "Bowser in the Dark World - Tower 1-Up Block",
                "Bowser in the Dark World - Near Goombas 1-Up Block")

    regBasement = create_region("Basement", player, multiworld)
    create_default_locs(regBasement, locBasement_table)
    create_locs(regBasement, "Castle - Basement Water Tunnel Four Corners 1-Up")

    regHMC = create_region("Hazy Maze Cave", player, multiworld)
    create_locs(regHMC, "Hazy Maze Cave - Swimming Beast in the Cavern", "Hazy Maze Cave - Metal-Head Mario Can Move!",
                        "Hazy Maze Cave - Watch for Rolling Rocks", "Hazy Maze Cave - Navigating the Toxic Maze","Hazy Maze Cave - Past Rolling Rocks Block 1-Up",
                        "Hazy Maze Cave - Blue Coin Trail Monty Moles", "Hazy Maze Cave - Twin Hole Monty Moles",
                        "Hazy Maze Cave - Beginning Metal Cap Block",
                        "Hazy Maze Cave - Metal-Head Mario Can Move Metal Cap Block",
                        "Hazy Maze Cave - Past Rolling Rocks 1-Up Block",
                        "Hazy Maze Cave - Toxic Maze Near Empty Alcove Metal Cap Block",
                        "Hazy Maze Cave - Toxic Maze Near Bats Metal Cap Block",
                        "Hazy Maze Cave - Toxic Maze Near Twin Monty Mole Holes Metal Cap Block")
    hmc_red_coin_area = create_subregion(regHMC, "Hazy Maze Cave - Red Coin Area", "Hazy Maze Cave - Elevate for 8 Red Coins")
    hmc_pit_islands = create_subregion(regHMC, "Hazy Maze Cave - Pit Islands",
                                       "Hazy Maze Cave - A-Maze-Ing Emergency Exit",
                                       "Hazy Maze Cave - Above Pit Block 1-Up",
                                       "Hazy Maze Cave - Above Pit 1-Up Block")
    regHMC.subregions = [hmc_red_coin_area, hmc_pit_islands]
    create_locs(regHMC, "Hazy Maze Cave - Coins Star")

    regLLL = create_region("Lethal Lava Land", player, multiworld)
    create_locs(regLLL, "Lethal Lava Land - Boil the Big Bully", "Lethal Lava Land - Bully the Bullies",
                        "Lethal Lava Land - 8-Coin Puzzle with 15 Pieces", "Lethal Lava Land - Red-Hot Log Rolling",
                        "Lethal Lava Land - Flamethrower Ring 1-Up",
                        "Lethal Lava Land - Volcano Flamethrower 1-Up",
                        "Lethal Lava Land - Northeast Brown Platform 1-Up",
                        "Lethal Lava Land - Boil the Big Bully Star Lava 1-Up",
                        "Lethal Lava Land - Volcano Curve 1-Up",
                        "Lethal Lava Land - Volcano Brown Platform 1-Up",
                        "Lethal Lava Land - Northwest Curve 1-Up",
                        "Lethal Lava Land - Wing Cap Block",
                        "Lethal Lava Land - Koopa Shell Block")
    lll_hot_foot_ledge = create_subregion(
        regLLL, "Lethal Lava Land - Hot-Foot-It Ledge",
        "Lethal Lava Land - Hot-Foot-It into the Volcano")
    lll_upper_volcano = create_subregion(
        regLLL, "Lethal Lava Land - Upper Volcano",
        "Lethal Lava Land - Volcano Pole 1-Up")
    lll_elevator_tour = create_region("Lethal Lava Land - Elevator Tour", player, multiworld)
    create_locs(lll_elevator_tour, "Lethal Lava Land - Elevator Tour in the Volcano")
    regLLL.subregions = [lll_hot_foot_ledge, lll_upper_volcano, lll_elevator_tour]
    create_locs(regLLL, "Lethal Lava Land - Coins Star")

    regSSL = create_region("Shifting Sand Land", player, multiworld)
    create_locs(regSSL, "Shifting Sand Land - In the Talons of the Big Bird", "Shifting Sand Land - Shining Atop the Pyramid",
                        "Shifting Sand Land - Free Flying for 8 Red Coins",
                        "Shifting Sand Land - Stand Tall on the Four Pillars",
                        "Shifting Sand Land - Bob-omb Buddy",
                        "Shifting Sand Land - Outside Pyramid Block 1-Up", "Shifting Sand Land - Pyramid Left Path Block 1-Up", "Shifting Sand Land - Pyramid Back Block 1-Up",
                        "Shifting Sand Land - Oasis Tree 1-Up",
                        "Shifting Sand Land - Near Quicksand Pits 1-Up",
                        "Shifting Sand Land - Above Quicksand Pit 1-Up",
                        "Shifting Sand Land - Pyramid Mummified Thwomp 1-Up",
                        "Shifting Sand Land - Pyramid Right Path 1-Up",
                        "Shifting Sand Land - Outside Pyramid Wing Cap Block",
                        "Shifting Sand Land - Outside Pyramid 1-Up Block",
                        "Shifting Sand Land - Cannon Wing Cap Block",
                        "Shifting Sand Land - Pyramid Left Path 1-Up Block",
                        "Shifting Sand Land - Pyramid Back 1-Up Block")
    ssl_stone_structure = create_subregion(
        regSSL, "Shifting Sand Land - Stone Structure",
        "Shifting Sand Land - Stone Structure Koopa Shell Block",
        "Shifting Sand Land - Stone Structure Wing Cap Block")
    ssl_upper_pyramid = create_subregion(regSSL, "Shifting Sand Land - Upper Pyramid", "Shifting Sand Land - Inside the Ancient Pyramid",
                                         "Shifting Sand Land - Pyramid Puzzle",
                                         "Shifting Sand Land - Pyramid Platform Triggers 1-Up")
    regSSL.subregions = [ssl_stone_structure, ssl_upper_pyramid]
    create_locs(regSSL, "Shifting Sand Land - Coins Star")

    regDDD = create_region("Dire, Dire Docks", player, multiworld)
    create_locs(regDDD, "Dire, Dire Docks - Board Bowser's Sub", "Dire, Dire Docks - Chests in the Current", "Dire, Dire Docks - Through the Jet Stream",
                        "Dire, Dire Docks - The Manta Ray's Reward", "Dire, Dire Docks - Collect the Caps...", "Dire, Dire Docks - Pole-Jumping for Red Coins",
                        "Dire, Dire Docks - Whirlpool Clam 1-Up",
                        "Dire, Dire Docks - Metal Cap Block",
                        "Dire, Dire Docks - Vanish Cap Block")
    create_locs(regDDD, "Dire, Dire Docks - Coins Star")

    regCotMC = create_region("Cavern of the Metal Cap", player, multiworld)
    create_default_locs(regCotMC, locCotMC_table)
    create_locs(regCotMC, "Cavern of the Metal Cap - Alcove 1-Up",
                "Cavern of the Metal Cap - First Metal Cap Block",
                "Cavern of the Metal Cap - 1-Up Block",
                "Cavern of the Metal Cap - Near Switch Metal Cap Block")

    regVCutM = create_region("Vanish Cap Under the Moat", player, multiworld)
    create_default_locs(regVCutM, locVCutM_table)
    create_locs(regVCutM,
                "Vanish Cap Under the Moat - Upper Platform 1-Up",
                "Vanish Cap Under the Moat - Lower Platform 1-Up",
                "Vanish Cap Under the Moat - Red Coin Platform 1-Up",
                "Vanish Cap Under the Moat - Bottom of Slide Vanish Cap Block",
                "Vanish Cap Under the Moat - 1-Up Block",
                "Vanish Cap Under the Moat - 3 Coins Block",
                "Vanish Cap Under the Moat - Near Switch Vanish Cap Block")

    regBitFS = create_region("Bowser in the Fire Sea", player, multiworld)
    create_locs(regBitFS,
                "Bowser in the Fire Sea - First Stone Structure 1-Up",
                "Bowser in the Fire Sea - Second Stone Structure 1-Up",
                "Bowser in the Fire Sea - 3 Coins Block")
    bitfs_upper = create_subregion(regBitFS, "Bowser in the Fire Sea - Upper",
                                   "Bowser in the Fire Sea - Red Coins",
                                   "Bowser in the Fire Sea - Key",
                                   "Bowser in the Fire Sea - Swaying Stairs Block 1-Up",
                                   "Bowser in the Fire Sea - Near Poles Block 1-Up",
                                   "Bowser in the Fire Sea - Elevator Pole 1-Up",
                                   "Bowser in the Fire Sea - Stretching Platform Trigger 1-Up",
                                   "Bowser in the Fire Sea - Near Poles 1-Up",
                                   "Bowser in the Fire Sea - Swaying Stairs 1-Up Block",
                                   "Bowser in the Fire Sea - 10 Coins Block",
                                   "Bowser in the Fire Sea - Near Poles 1-Up Block")
    regBitFS.subregions = [bitfs_upper]

    create_region("Second Floor", player, multiworld)

    regSL = create_region("Snowman's Land", player, multiworld)
    create_locs(regSL,
                "Snowman's Land - Chill with the Bully",
                "Snowman's Land - In the Deep Freeze",
                "Snowman's Land - Bob-omb Buddy",
                "Snowman's Land - Near Moneybags Block 1-Up",
                "Snowman's Land - Near Moneybags 1-Up Block")
    sl_whirl = create_subregion(regSL, "Snowman's Land - Whirl from the Freezing Pond",
                                "Snowman's Land - Whirl from the Freezing Pond",
                                "Snowman's Land - Koopa Shell Block",
                                "Snowman's Land - Shell Shreddin' for Red Coins",
                                "Snowman's Land - Whirl from the Freezing Pond Star Block")
    sl_upper = create_subregion(regSL, "Snowman's Land - Upper")
    sl_top_of_snowmans_head = create_subregion(
        sl_upper, "Snowman's Land - Top of Snowman's Head",
        "Snowman's Land - Snowman's Big Head",
        "Snowman's Land - Snowman Tree 1-Up")
    sl_igloo = create_subregion(regSL, "Snowman's Land - Igloo",
                                "Snowman's Land - Into the Igloo",
                                "Snowman's Land - Inside Igloo Block 1-Up",
                                "Snowman's Land - Igloo Ice Block 1-Up",
                                "Snowman's Land - Inside Igloo 1-Up Block",
                                "Snowman's Land - Vanish Cap Block",
                                "Snowman's Land - 3 Coins Block")
    sl_top_of_snowmans_head.connect(
        sl_igloo, name="Snowman's Land - Top of Snowman's Head to Igloo")
    regSL.subregions = [sl_whirl, sl_upper, sl_top_of_snowmans_head, sl_igloo]
    create_locs(regSL, "Snowman's Land - Coins Star")

    regWDWLow = create_region("Wet-Dry World Low", player, multiworld)
    regWDWMiddle = create_region("Wet-Dry World Middle", player, multiworld)
    regWDWHigh = create_region("Wet-Dry World High", player, multiworld)

    regWDW = create_region("Wet-Dry World", player, multiworld)
    create_locs(regWDW, "Wet-Dry World - Shocking Arrow Lifts!", "Wet-Dry World - Bob-omb Buddy",
                "Wet-Dry World - Shocking Arrow Lifts Star Block",
                "Wet-Dry World - Pedestal 10 Coins Block",
                "Wet-Dry World - Push Block 3 Coins Block",
                "Wet-Dry World - Wooden Structure 3 Coins Block")
    wdw_low_water = create_region("Wet-Dry World - Low Water", player, multiworld)
    create_locs(wdw_low_water, "Wet-Dry World - Secrets in the Shallows & Sky",
                "Wet-Dry World - Push Block 10 Coins Block")
    wdw_mid_water = create_region("Wet-Dry World - Mid Water", player, multiworld)
    wdw_mid_high_water = create_region("Wet-Dry World - Mid-High Water", player, multiworld)
    wdw_high_water = create_region("Wet-Dry World - High Water", player, multiworld)
    wdw_highest_water = create_region("Wet-Dry World - Highest Water", player, multiworld)
    wdw_cannon = create_region("Wet-Dry World - Cannon", player, multiworld)
    wdw_top_of_express_elevator = create_subregion(regWDW, "Wet-Dry World - Top of the Express Elevator",
                                                   "Wet-Dry World - Express Elevator--Hurry Up!",
                                                   "Wet-Dry World - Top of Express Elevator 10 Coins Block")
    wdw_top = create_subregion(regWDW, "Wet-Dry World - Top",
                               "Wet-Dry World - Top o' the Town",
                               "Wet-Dry World - Cylinder Lower 1-Up",
                               "Wet-Dry World - Cylinder Upper 1-Up",
                               "Wet-Dry World - Top o' the Town Star Block")
    wdw_downtown = create_subregion(regWDW, "Wet-Dry World - Downtown",
                                    "Wet-Dry World - Go to Town for Red Coins",
                                    "Wet-Dry World - Quick Race Through Downtown!",
                                    "Wet-Dry World - Downtown Block 1-Up",
                                    "Wet-Dry World - Downtown Center Coin Ring 1-Up",
                                    "Wet-Dry World - Downtown Vanish Cap Block",
                                    "Wet-Dry World - Metal Cap Block",
                                    "Wet-Dry World - Quick Race Through Downtown Star Vanish Cap Block",
                                    "Wet-Dry World - Downtown 1-Up Block")
    regWDW.subregions = [
        wdw_low_water, wdw_mid_water, wdw_mid_high_water, wdw_high_water, wdw_highest_water, wdw_cannon,
        wdw_top_of_express_elevator, wdw_top, wdw_downtown
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
    create_locs(regWDW, "Wet-Dry World - Coins Star")

    regTTM = create_region("Tall, Tall Mountain", player, multiworld)
    create_locs(regTTM, "Tall, Tall Mountain - Start Edge 1-Up")
    ttm_middle = create_subregion(regTTM, "Tall, Tall Mountain - Middle", "Tall, Tall Mountain - Blast to the Lonely Mushroom",
                                          "Tall, Tall Mountain - Bob-omb Buddy", "Tall, Tall Mountain - Red Mushroom Block 1-Up",
                                          "Tall, Tall Mountain - Red Mushroom 1-Up Block",
                                          "Tall, Tall Mountain - Lower Monty Moles")
    ttm_upper = create_subregion(ttm_middle, "Tall, Tall Mountain - Upper",
                                 "Tall, Tall Mountain - Scary 'Shrooms, Red Coins",
                                 "Tall, Tall Mountain - Monty Mole Platform 1-Up",
                                 "Tall, Tall Mountain - Waterfall Gap 1-Up",
                                 "Tall, Tall Mountain - Upper Monty Moles")
    ttm_top = create_subregion(ttm_upper, "Tall, Tall Mountain - Top", "Tall, Tall Mountain - Scale the Mountain", "Tall, Tall Mountain - Mystery of the Monkey Cage",
                                                       "Tall, Tall Mountain - Mysterious Mountainside", "Tall, Tall Mountain - Breathtaking View from Bridge",
                                                       "Tall, Tall Mountain - Vine Platform Butterfly 1-Up",
                                                       "Tall, Tall Mountain - Slide Start Room Corners 1-Up",
                                                       "Tall, Tall Mountain - Slide Entry Ledge 1-Up",
                                                       "Tall, Tall Mountain - Slide First 1-Up",
                                                       "Tall, Tall Mountain - Slide Second 1-Up")
    regTTM.subregions = [ttm_middle, ttm_upper, ttm_top]
    create_locs(regTTM, "Tall, Tall Mountain - Coins Star")

    hugeTHI = create_region("Tiny-Huge Island (Huge)", player, multiworld)
    tinyTHI = create_region("Tiny-Huge Island (Tiny)", player, multiworld)
    create_locs(tinyTHI, "Tiny-Huge Island - Tiny Island Near Start Block 1-Up",
                "Tiny-Huge Island - Tiny Island Near Start 1-Up Block",
                "Tiny-Huge Island - Start Butterfly 1-Up")
    create_locs(hugeTHI, "Tiny-Huge Island - Beach Coins 1-Up",
                         "Tiny-Huge Island - Boss Bass 1-Up")
    thi_windswept_valley = create_subregion(
        hugeTHI, "Tiny-Huge Island - Windswept Valley",
        "Tiny-Huge Island - Windy Area Block 1-Up",
        "Tiny-Huge Island - Windy Area 1-Up Block")
    thi_cannonball = create_subregion(
        thi_windswept_valley, "Tiny-Huge Island - Cannonball")
    thi_koopa_the_quick = create_subregion(
        thi_cannonball, "Tiny-Huge Island - Koopa the Quick",
        "Tiny-Huge Island - Rematch with Koopa the Quick",
        "Tiny-Huge Island - Huge Island Near Start Block 1-Up",
        "Tiny-Huge Island - Huge Island Near Start 1-Up Block",
        "Tiny-Huge Island - Koopa Area Butterfly 1-Up")
    thi_huge_top = create_subregion(
        thi_koopa_the_quick, "Tiny-Huge Island - Huge Top",
        "Tiny-Huge Island - The Tip Top of the Huge Island",
        "Tiny-Huge Island - The Tip Top of the Huge Island Star Block")
    thi_wiggler_cave = create_subregion(
        thi_huge_top, "Tiny-Huge Island - Wiggler's Cave",
        "Tiny-Huge Island - Make Wiggler Squirm")
    thi_red_coins = create_region("Tiny-Huge Island - Red Coins Area", player, multiworld)
    create_locs(thi_red_coins,
                "Tiny-Huge Island - Wiggler's Red Coins",
                "Tiny-Huge Island - Cannon Tree 1-Up",
                "Tiny-Huge Island - Red Coin Bridge Tree 1-Up",
                "Tiny-Huge Island - Red Coin Cave 1-Up")
    thi_coins = create_region("Tiny-Huge Island - Coins", player, multiworld)
    create_locs(thi_coins, "Tiny-Huge Island - Coins Star")
    hugeTHI.connect(thi_coins)
    tinyTHI.connect(thi_coins)
    thi_huge_piranha_area = create_region("Tiny-Huge Island - Huge Piranha Area", player, multiworld)
    create_locs(thi_huge_piranha_area, "Tiny-Huge Island - Pluck the Piranha Flower")
    thi_tiny_piranha_area = create_subregion(tinyTHI, "Tiny-Huge Island - Tiny Piranha Area")
    thi_tiny_main = create_subregion(thi_tiny_piranha_area, "Tiny-Huge Island - Tiny Main",
                                     "Tiny-Huge Island - Five Itty Bitty Secrets",
                                     "Tiny-Huge Island - Bob-omb Buddy",
                                     "Tiny-Huge Island - 3 Coins Block")

    thi_huge_top.connect(thi_koopa_the_quick, name="Tiny-Huge Island - Huge Top to Koopa the Quick")
    thi_koopa_the_quick.connect(thi_cannonball, name="Tiny-Huge Island - Koopa the Quick to Cannonball")
    thi_cannonball.connect(thi_windswept_valley, name="Tiny-Huge Island - Cannonball to Windswept Valley")
    thi_koopa_the_quick.connect(hugeTHI, name="Tiny-Huge Island - Koopa the Quick to Huge Island")
    thi_koopa_the_quick.connect(thi_huge_piranha_area,
                                name="Tiny-Huge Island - Koopa the Quick to Huge Piranha Area")
    thi_huge_piranha_area.connect(hugeTHI,
                                  name="Tiny-Huge Island - Huge Piranha Area to Huge Island")
    hugeTHI.connect(thi_huge_top, name="Tiny-Huge Island - Huge Island to Huge Top with Koopa Shell")
    hugeTHI.connect(thi_red_coins, name="Tiny-Huge Island - Huge Island to Red Coins Area")
    thi_huge_top.connect(thi_red_coins, name="Tiny-Huge Island - Huge Top to Red Coins Area")
    thi_tiny_piranha_area.connect(tinyTHI, name="Tiny-Huge Island - Tiny Piranha Area to Tiny Island")
    thi_tiny_piranha_area.connect(thi_huge_piranha_area,
                                  name="Tiny-Huge Island - Tiny Piranha Area to Huge Piranha Area")
    thi_huge_piranha_area.connect(thi_tiny_piranha_area,
                                  name="Tiny-Huge Island - Huge Piranha Area to Tiny Piranha Area")
    thi_tiny_main.connect(thi_koopa_the_quick, name="Tiny-Huge Island - Tiny Main to Koopa the Quick")
    thi_koopa_the_quick.connect(thi_tiny_main, name="Tiny-Huge Island - Koopa the Quick to Tiny Main")

    hugeTHI.subregions = [
        thi_coins, thi_windswept_valley, thi_cannonball, thi_koopa_the_quick,
        thi_huge_top, thi_wiggler_cave, thi_red_coins, thi_huge_piranha_area]
    tinyTHI.subregions = [thi_coins, thi_tiny_piranha_area, thi_tiny_main]

    regFloor3 = create_region("Third Floor", player, multiworld)

    regTTC = create_region("Tick Tock Clock", player, multiworld)
    create_locs(regTTC,
                "Tick Tock Clock - Below Red Coin Spinners 10 Coins Block",
                "Tick Tock Clock - First Pendulum 3 Coins Block")
    ttc_lower = create_subregion(regTTC, "Tick Tock Clock - Lower", "Tick Tock Clock - Roll into the Cage",
                                 "Tick Tock Clock - Get a Hand", "Tick Tock Clock - Stop Time for Red Coins",
                                 "Tick Tock Clock - Above Red Coin Spinners 3 Coins Block")
    ttc_mid = create_subregion(ttc_lower, "Tick Tock Clock - Mid",
                               "Tick Tock Clock - The Pit and the Pendulums",
                               "Tick Tock Clock - Heave-ho First 3 Coins Block",
                               "Tick Tock Clock - Heave-ho Second 3 Coins Block")
    ttc_upper = create_subregion(ttc_mid, "Tick Tock Clock - Upper", "Tick Tock Clock - Timed Jumps on Moving Bars",
                                 "Tick Tock Clock - Moving Bars Platform 1-Up",
                                 "Tick Tock Clock - Pole 1-Up",
                                 "Tick Tock Clock - Above Timed Jumps on Moving Bars 3 Coins Block",
                                 "Tick Tock Clock - Above Four Moving Bars 10 Coins Block")
    ttc_top = create_subregion(ttc_upper, "Tick Tock Clock - Top", "Tick Tock Clock - Midway Up Block 1-Up",
                               "Tick Tock Clock - Midway Up 1-Up Block",
                               "Tick Tock Clock - Past Three Spinners 3 Coins Block")
    ttc_top_past_spinners = create_subregion(ttc_top, "Tick Tock Clock - Top Past Spinners",
                                             "Tick Tock Clock - Stomp on the Thwomp",
                                             "Tick Tock Clock - Top Block 1-Up",
                                             "Tick Tock Clock - Top 1-Up Block",
                                             "Tick Tock Clock - Top Clock Hand 10 Coins Block",
                                             "Tick Tock Clock - Top Central Platform 10 Coins Block",
                                             "Tick Tock Clock - Beneath the Thwomp 10 Coins Block")
    regTTC.subregions = [ttc_lower, ttc_mid, ttc_upper, ttc_top, ttc_top_past_spinners]
    regTTCStopped = create_region("Tick Tock Clock Stopped", player, multiworld)
    regTTCStopped.connect(regTTC)
    regTTCStopped.subregions = [regTTC, *regTTC.subregions]
    regTTCMoving = create_region("Tick Tock Clock Moving", player, multiworld)
    regTTCMoving.connect(regTTC)
    regTTCMoving.subregions = [regTTC, *regTTC.subregions]
    create_locs(regTTC, "Tick Tock Clock - Coins Star")

    regRR = create_region("Rainbow Ride", player, multiworld)
    rr_beneath_pole = create_subregion(regRR, "Rainbow Ride - Beneath the Pole",
                                       "Rainbow Ride - Swingin' in the Breeze",
                                       "Rainbow Ride - Tricky Triangles!",
                                       "Rainbow Ride - Under Fly Guy Block 1-Up",
                                       "Rainbow Ride - Under Fly Guy 1-Up Block",
                                       "Rainbow Ride - Tricky Triangles 1-Up",)
    rr_maze = create_subregion(rr_beneath_pole, "Rainbow Ride - Maze",
                               "Rainbow Ride - Coins Amassed in a Maze",
                               )
    connect_regions(multiworld, player, "Rainbow Ride", "Rainbow Ride - Maze",
                    name="Rainbow Ride - Initial to Maze")
    rr_carpets = create_subregion(rr_maze, "Rainbow Ride - Carpets", "Rainbow Ride - Bob-omb Buddy")
    rr_cruiser = create_subregion(rr_carpets, "Rainbow Ride - Cruiser",
                                  "Rainbow Ride - Cruiser Crossing the Rainbow",
                                  "Rainbow Ride - Somewhere Over the Rainbow",
                                  "Rainbow Ride - Somewhere Over the Rainbow Star Block",
                                  "Rainbow Ride - Ship Pole 1-Up",
                                  "Rainbow Ride - Ship Tip 1-Up",
                                  "Rainbow Ride - Rotating Bridge Platform 1-Up")
    rr_house = create_subregion(rr_carpets, "Rainbow Ride - House", "Rainbow Ride - The Big House in the Sky",
                                "Rainbow Ride - House in the Sky Block 1-Up",
                                "Rainbow Ride - House in the Sky 1-Up Block",
                                "Rainbow Ride - House Path Donut Lifts 1-Up",
                                "Rainbow Ride - Donut Top of Red Coin Maze 1-Up",
                                "Rainbow Ride - Top of Red Coin Maze Block 1-Up",
                                "Rainbow Ride - Top of Red Coin Maze 1-Up Block",)
    regRR.subregions = [rr_beneath_pole, rr_maze, rr_carpets, rr_cruiser, rr_house]
    create_locs(regRR, "Rainbow Ride - Coins Star")

    regWMotR = create_region("Wing Mario Over the Rainbow", player, multiworld)
    create_locs(regWMotR,
                "Wing Mario Over the Rainbow - Cloud 1-Up",
                "Wing Mario Over the Rainbow - Cloud Across From Starting Cloud Wing Cap Block",
                "Wing Mario Over the Rainbow - Starting Cloud Wing Cap Block",
                "Wing Mario Over the Rainbow - Lowest Cloud Wing Cap Block")
    wmotr_buddy_platform = create_subregion(regWMotR, "Wing Mario Over the Rainbow - Bob-omb Buddy Platform",
                                            "Wing Mario Over the Rainbow - Bob-omb Buddy",
                                            "Wing Mario Over the Rainbow - Bob-omb Buddy Platform 1-Up",
                                            "Wing Mario Over the Rainbow - Bob-omb Buddy Platform Wing Cap Block",
                                            "Wing Mario Over the Rainbow - Overlooking Bob-omb Buddy Cloud Wing Cap Block")
    wmotr_cannon = create_subregion(wmotr_buddy_platform, "Wing Mario Over the Rainbow - Cannon",
                                    "Wing Mario Over the Rainbow - Red Coins",
                                    "Wing Mario Over the Rainbow - Block 1-Up",
                                    "Wing Mario Over the Rainbow - Hanging Pole 1-Up",
                                    "Wing Mario Over the Rainbow - Highest Cloud Wing Cap Block",
                                    "Wing Mario Over the Rainbow - 1-Up Block")
    regWMotR.subregions = [wmotr_buddy_platform, wmotr_cannon]

    regBitS = create_region("Bowser in the Sky", player, multiworld)
    create_locs(regBitS, "Bowser in the Sky - Block 1-Up",
                "Bowser in the Sky - 1-Up Block",
                "Bowser in the Sky - Before Tilting Platform 1-Up",
                "Bowser in the Sky - Ferris Wheel 1-Up")
    bits_chuckya = create_subregion(regBitS, "Bowser in the Sky - Chuckya")
    bits_arrow_ride = create_subregion(bits_chuckya, "Bowser in the Sky - Arrow Ride",
                                       "Bowser in the Sky - Spark Pole Coins 1-Up",
                                       "Bowser in the Sky - Arrow Ride 1-Up")
    bits_top = create_subregion(bits_arrow_ride, "Bowser in the Sky - Top", "Bowser in the Sky - Red Coins",
                                "Bowser in the Sky - Final Platform 1-Up")
    regBitS.subregions = [bits_chuckya, bits_arrow_ride, bits_top]

    if not options.one_up_checks:
        remove_locs(multiworld, player, set(locOneUp_table))
    if not options.blocksanity:
        remove_locs(multiworld, player, set(locBlocksanity_table))


def connect_regions(multiworld: MultiWorld, player: int, source: str, target: str, rule=None,
                    name: str | None = None) -> Entrance:
    sourceRegion = multiworld.get_region(source, player)
    targetRegion = multiworld.get_region(target, player)
    if isinstance(rule, Rule):
        return multiworld.worlds[player].create_entrance(sourceRegion, targetRegion, rule, name=name)
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


def remove_locs(multiworld: MultiWorld, player: int, locs: set[str]):
    for region in multiworld.get_regions(player):
        region.locations = [location for location in region.locations if location.name not in locs]
