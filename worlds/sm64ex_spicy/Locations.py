from BaseClasses import Location

from .CoinChecks import individual_coin_location_table

class SM64Location(Location):
    game: str = "SM64: Spicy Mycena 64"

coin_count_check_location_base_id = 3627000
tiny_huge_island_extra_coin_count_check_location_id = 3629091

coin_count_check_course_data = (
    ("Bob-omb Battlefield", 0, "bob_omb_battlefield_coin_star_requirement", 146),
    ("Whomp's Fortress", 146, "whomps_fortress_coin_star_requirement", 141),
    ("Jolly Roger Bay", 287, "jolly_roger_bay_coin_star_requirement", 104),
    ("Cool, Cool Mountain", 391, "cool_cool_mountain_coin_star_requirement", 154),
    ("Big Boo's Haunt", 545, "big_boos_haunt_coin_star_requirement", 151),
    ("Hazy Maze Cave", 696, "hazy_maze_cave_coin_star_requirement", 139),
    ("Lethal Lava Land", 835, "lethal_lava_land_coin_star_requirement", 133),
    ("Shifting Sand Land", 968, "shifting_sand_land_coin_star_requirement", 136),
    ("Dire, Dire Docks", 1104, "dire_dire_docks_coin_star_requirement", 106),
    ("Snowman's Land", 1210, "snowmans_land_coin_star_requirement", 127),
    ("Wet-Dry World", 1337, "wet_dry_world_coin_star_requirement", 152),
    ("Tall, Tall Mountain", 1489, "tall_tall_mountain_coin_star_requirement", 137),
    ("Tiny-Huge Island", 1626, "tiny_huge_island_coin_star_requirement", 193),
    ("Tick Tock Clock", 1817, "tick_tock_clock_coin_star_requirement", 128),
    ("Rainbow Ride", 1945, "rainbow_ride_coin_star_requirement", 146),
)

secret_stage_coin_count_check_location_base_id = 3629193

secret_stage_coin_count_check_data = (
    ("The Princess's Secret Slide", 3629193, "princess_secret_slide_coin_count_max_coins", 80),
    ("The Secret Aquarium", 3629273, "secret_aquarium_coin_count_max_coins", 56),
    ("Wing Mario Over the Rainbow", 3629329, "wing_mario_over_the_rainbow_coin_count_max_coins", 56),
    ("Tower of the Wing Cap", 3629385, "tower_of_the_wing_cap_coin_count_max_coins", 63),
    ("Vanish Cap Under the Moat", 3629448, "vanish_cap_under_the_moat_coin_count_max_coins", 27),
    ("Cavern of the Metal Cap", 3629475, "cavern_of_the_metal_cap_coin_count_max_coins", 47),
    ("Bowser in the Dark World", 3629522, "bowser_in_the_dark_world_coin_count_max_coins", 80),
    ("Bowser in the Fire Sea", 3629602, "bowser_in_the_fire_sea_coin_count_max_coins", 80),
    ("Bowser in the Sky", 3629682, "bowser_in_the_sky_coin_count_max_coins", 76),
)


def get_coin_count_check_location_name(course_name: str, coin_count: int) -> str:
    return f"{course_name} - {coin_count} Coin{'s' if coin_count != 1 else ''}"


def get_coin_count_check_thresholds(coin_star_requirement: int, percentage: int) -> tuple[int, ...]:
    if coin_star_requirement <= 1 or percentage <= 0:
        return ()

    available_coin_checks = coin_star_requirement - 1
    check_count = min((available_coin_checks * percentage + 99) // 100, available_coin_checks)
    return tuple(
        (coin_star_requirement * check_index) // (check_count + 1)
        for check_index in range(1, check_count + 1)
    )


def get_coin_count_check_location_names(coin_star_requirements: dict[str, int], percentage: int) -> tuple[str, ...]:
    return tuple(
        get_coin_count_check_location_name(course_name, coin_count)
        for course_name, _course_offset, option_name, _max_coins in coin_count_check_course_data
        for coin_count in get_coin_count_check_thresholds(coin_star_requirements[option_name], percentage)
    )


def get_secret_stage_coin_count_check_location_names(
        secret_stage_coin_maxes: dict[str, int], percentage: int) -> tuple[str, ...]:
    return tuple(
        get_coin_count_check_location_name(course_name, coin_count)
        for course_name, _base_id, option_name, _max_coins in secret_stage_coin_count_check_data
        for coin_count in get_coin_count_check_thresholds(secret_stage_coin_maxes[option_name] + 1, percentage)
    )


def parse_coin_count_check_location_name(location_name: str) -> tuple[str, int] | None:
    if location_name not in coin_count_check_location_table:
        return None
    course_name, coin_text = location_name.rsplit(" - ", 1)
    return course_name, int(coin_text.split(" ", 1)[0])


coin_count_check_location_table = {
    get_coin_count_check_location_name(course_name, coin_count): (
        tiny_huge_island_extra_coin_count_check_location_id
        if course_name == "Tiny-Huge Island" and coin_count == 192
        else coin_count_check_location_base_id + course_offset + coin_count - 1
    )
    for course_name, course_offset, _option_name, max_coin_star_requirement in coin_count_check_course_data
    for coin_count in range(1, max_coin_star_requirement)
}

secret_stage_coin_count_check_location_table = {
    get_coin_count_check_location_name(course_name, coin_count): base_id + coin_count - 1
    for course_name, base_id, _option_name, max_coins in secret_stage_coin_count_check_data
    for coin_count in range(1, max_coins + 1)
}

coin_count_check_location_table = {
    **coin_count_check_location_table,
    **secret_stage_coin_count_check_location_table,
}

#Bob-omb Battlefield
locBoB_table = {
    "Bob-omb Battlefield - Big Bob-Omb on the Summit": 3626000,
    "Bob-omb Battlefield - Footrace with Koopa The Quick": 3626001,
    "Bob-omb Battlefield - Shoot to the Island in the Sky": 3626002,
    "Bob-omb Battlefield - Find the 8 Red Coins": 3626003,
    "Bob-omb Battlefield - Mario Wings to the Sky": 3626004,
    "Bob-omb Battlefield - Behind Chain Chomp's Gate": 3626005,
    "Bob-omb Battlefield - Bob-omb Buddy": 3626200,
}

#Whomp's Fortress
locWhomp_table = {
    "Whomp's Fortress - Chip Off Whomp's Block": 3626007,
    "Whomp's Fortress - To the Top of the Fortress": 3626008,
    "Whomp's Fortress - Shoot into the Wild Blue": 3626009,
    "Whomp's Fortress - Red Coins on the Floating Isle": 3626010,
    "Whomp's Fortress - Fall onto the Caged Island": 3626011,
    "Whomp's Fortress - Blast Away the Wall": 3626012,
    "Whomp's Fortress - Bob-omb Buddy": 3626201,
}

#Jolly Roger Bay
locJRB_table = {
    "Jolly Roger Bay - Plunder in the Sunken Ship": 3626014,
    "Jolly Roger Bay - Can the Eel Come Out to Play?": 3626015,
    "Jolly Roger Bay - Treasure of the Ocean Cave": 3626016,
    "Jolly Roger Bay - Red Coins on the Ship Afloat": 3626017,
    "Jolly Roger Bay - Blast to the Stone Pillar": 3626018,
    "Jolly Roger Bay - Through the Jet Stream": 3626019,
    "Jolly Roger Bay - Bob-omb Buddy": 3626202,
}


#Cool, Cool Mountain
locCCM_table = {
    "Cool, Cool Mountain - Slip Slidin' Away": 3626021,
    "Cool, Cool Mountain - Li'l Penguin Lost": 3626022,
    "Cool, Cool Mountain - Big Penguin Race": 3626023,
    "Cool, Cool Mountain - Frosty Slide for 8 Red Coins": 3626024,
    "Cool, Cool Mountain - Snowman's Lost His Head": 3626025,
    "Cool, Cool Mountain - Wall Kicks Will Work": 3626026,
    "Cool, Cool Mountain - Bob-omb Buddy": 3626203,
    "Cool, Cool Mountain - Near Snowman Block 1-Up": 3626215,
    "Cool, Cool Mountain - Ice Pillar Block 1-Up": 3626216,
    "Cool, Cool Mountain - Secret Slide Block 1-Up": 3626217
}

#Big Boo's Haunt
locBBH_table = {
    "Big Boo's Haunt - Go on a Ghost Hunt": 3626028,
    "Big Boo's Haunt - Ride Big Boo's Merry-Go-Round": 3626029,
    "Big Boo's Haunt - Secret of the Haunted Books": 3626030,
    "Big Boo's Haunt - Seek the 8 Red Coins": 3626031,
    "Big Boo's Haunt - Big Boo's Balcony": 3626032,
    "Big Boo's Haunt - Eye to Eye in the Secret Room": 3626033,
    "Big Boo's Haunt - Top of Mansion Block 1-Up": 3626218
}

#Hazy Maze Cave
locHMC_table = {
    "Hazy Maze Cave - Swimming Beast in the Cavern": 3626035,
    "Hazy Maze Cave - Elevate for 8 Red Coins": 3626036,
    "Hazy Maze Cave - Metal-Head Mario Can Move!": 3626037,
    "Hazy Maze Cave - Navigating the Toxic Maze": 3626038,
    "Hazy Maze Cave - A-Maze-Ing Emergency Exit": 3626039,
    "Hazy Maze Cave - Watch for Rolling Rocks": 3626040,
    "Hazy Maze Cave - Above Pit Block 1-Up": 3626219,
    "Hazy Maze Cave - Past Rolling Rocks Block 1-Up": 3626220,
}

#Lethal Lava Land
locLLL_table = {
    "Lethal Lava Land - Boil the Big Bully": 3626042,
    "Lethal Lava Land - Bully the Bullies": 3626043,
    "Lethal Lava Land - 8-Coin Puzzle with 15 Pieces": 3626044,
    "Lethal Lava Land - Red-Hot Log Rolling": 3626045,
    "Lethal Lava Land - Hot-Foot-It into the Volcano": 3626046,
    "Lethal Lava Land - Elevator Tour in the Volcano": 3626047
}

#Shifting Sand Land
locSSL_table = {
    "Shifting Sand Land - In the Talons of the Big Bird": 3626049,
    "Shifting Sand Land - Shining Atop the Pyramid": 3626050,
    "Shifting Sand Land - Inside the Ancient Pyramid": 3626051,
    "Shifting Sand Land - Stand Tall on the Four Pillars": 3626052,
    "Shifting Sand Land - Free Flying for 8 Red Coins": 3626053,
    "Shifting Sand Land - Pyramid Puzzle": 3626054,
    "Shifting Sand Land - Bob-omb Buddy": 3626207,
    "Shifting Sand Land - Outside Pyramid Block 1-Up": 3626221,
    "Shifting Sand Land - Pyramid Left Path Block 1-Up": 3626222,
    "Shifting Sand Land - Pyramid Back Block 1-Up": 3626223
}

#Dire, Dire Docks
locDDD_table = {
    "Dire, Dire Docks - Board Bowser's Sub": 3626056,
    "Dire, Dire Docks - Chests in the Current": 3626057,
    "Dire, Dire Docks - Pole-Jumping for Red Coins": 3626058,
    "Dire, Dire Docks - Through the Jet Stream": 3626059,
    "Dire, Dire Docks - The Manta Ray's Reward": 3626060,
    "Dire, Dire Docks - Collect the Caps...": 3626061
}

#Snowman's Land
locSL_table = {
    "Snowman's Land - Snowman's Big Head": 3626063,
    "Snowman's Land - Chill with the Bully": 3626064,
    "Snowman's Land - In the Deep Freeze": 3626065,
    "Snowman's Land - Whirl from the Freezing Pond": 3626066,
    "Snowman's Land - Shell Shreddin' for Red Coins": 3626067,
    "Snowman's Land - Into the Igloo": 3626068,
    "Snowman's Land - Bob-omb Buddy": 3626209,
    "Snowman's Land - Near Moneybags Block 1-Up": 3626224,
    "Snowman's Land - Inside Igloo Block 1-Up": 3626225
}

#Wet-Dry World
locWDW_table = {
    "Wet-Dry World - Shocking Arrow Lifts!": 3626070,
    "Wet-Dry World - Top o' the Town": 3626071,
    "Wet-Dry World - Secrets in the Shallows & Sky": 3626072,
    "Wet-Dry World - Express Elevator--Hurry Up!": 3626073,
    "Wet-Dry World - Go to Town for Red Coins": 3626074,
    "Wet-Dry World - Quick Race Through Downtown!": 3626075,
    "Wet-Dry World - Bob-omb Buddy": 3626210,
    "Wet-Dry World - Downtown Block 1-Up": 3626226
}

#Tall, Tall Mountain
locTTM_table = {
    "Tall, Tall Mountain - Scale the Mountain": 3626077,
    "Tall, Tall Mountain - Mystery of the Monkey Cage": 3626078,
    "Tall, Tall Mountain - Scary 'Shrooms, Red Coins": 3626079,
    "Tall, Tall Mountain - Mysterious Mountainside": 3626080,
    "Tall, Tall Mountain - Breathtaking View from Bridge": 3626081,
    "Tall, Tall Mountain - Blast to the Lonely Mushroom": 3626082,
    "Tall, Tall Mountain - Bob-omb Buddy": 3626211,
    "Tall, Tall Mountain - Red Mushroom Block 1-Up": 3626227
}

#Tiny-Huge Island
locTHI_table = {
    "Tiny-Huge Island - Pluck the Piranha Flower": 3626084,
    "Tiny-Huge Island - The Tip Top of the Huge Island": 3626085,
    "Tiny-Huge Island - Rematch with Koopa the Quick": 3626086,
    "Tiny-Huge Island - Five Itty Bitty Secrets": 3626087,
    "Tiny-Huge Island - Wiggler's Red Coins": 3626088,
    "Tiny-Huge Island - Make Wiggler Squirm": 3626089,
    "Tiny-Huge Island - Bob-omb Buddy": 3626212,
    "Tiny-Huge Island - Tiny Island Near Start Block 1-Up": 3626228,
    "Tiny-Huge Island - Huge Island Near Start Block 1-Up": 3626229,
    "Tiny-Huge Island - Windy Area Block 1-Up": 3626230
}

#Tick Tock Clock
locTTC_table = {
    "Tick Tock Clock - Roll into the Cage": 3626091,
    "Tick Tock Clock - The Pit and the Pendulums": 3626092,
    "Tick Tock Clock - Get a Hand": 3626093,
    "Tick Tock Clock - Stomp on the Thwomp": 3626094,
    "Tick Tock Clock - Timed Jumps on Moving Bars": 3626095,
    "Tick Tock Clock - Stop Time for Red Coins": 3626096,
    "Tick Tock Clock - Midway Up Block 1-Up": 3626231,
    "Tick Tock Clock - Top Block 1-Up": 3626232
}

#Rainbow Ride
locRR_table = {
    "Rainbow Ride - Cruiser Crossing the Rainbow": 3626098,
    "Rainbow Ride - The Big House in the Sky": 3626099,
    "Rainbow Ride - Coins Amassed in a Maze": 3626100,
    "Rainbow Ride - Swingin' in the Breeze": 3626101,
    "Rainbow Ride - Tricky Triangles!": 3626102,
    "Rainbow Ride - Somewhere Over the Rainbow": 3626103,
    "Rainbow Ride - Bob-omb Buddy": 3626214,
    "Rainbow Ride - Top of Red Coin Maze Block 1-Up": 3626233,
    "Rainbow Ride - Under Fly Guy Block 1-Up": 3626234,
    "Rainbow Ride - House in the Sky Block 1-Up": 3626235
}

loc100Coin_table = {
        "Bob-omb Battlefield - Coins Star": 3626006,
        "Whomp's Fortress - Coins Star": 3626013,
        "Jolly Roger Bay - Coins Star": 3626020,
        "Cool, Cool Mountain - Coins Star": 3626027,
        "Big Boo's Haunt - Coins Star": 3626034,
        "Hazy Maze Cave - Coins Star": 3626041,
        "Lethal Lava Land - Coins Star": 3626048,
        "Shifting Sand Land - Coins Star": 3626055,
        "Dire, Dire Docks - Coins Star": 3626062,
        "Snowman's Land - Coins Star": 3626069,
        "Wet-Dry World - Coins Star": 3626076,
        "Tall, Tall Mountain - Coins Star": 3626083,
        "Tiny-Huge Island - Coins Star": 3626090,
        "Tick Tock Clock - Coins Star": 3626097,
        "Rainbow Ride - Coins Star": 3626104
}

locPSS_table = {
    "The Princess's Secret Slide - Block Star": 3626126,
    "The Princess's Secret Slide - Fast": 3626127,
}

locSA_table = {
    "The Secret Aquarium - Red Coins": 3626161
}

locBitDW_table = {
    "Bowser in the Dark World - Red Coins": 3626105,
    "Bowser in the Dark World - Key": 3626178,
    "Bowser in the Dark World - Tower Block 1-Up": 3626236,
    "Bowser in the Dark World - Near Goombas Block 1-Up": 3626237
}

locTotWC_table = {
    "Tower of the Wing Cap - Switch": 3626181,
    "Tower of the Wing Cap - Red Coins": 3626140
}

locCotMC_table = {
    "Cavern of the Metal Cap - Switch": 3626182,
    "Cavern of the Metal Cap - Red Coins": 3626133,
    "Cavern of the Metal Cap - Block 1-Up": 3626241
}

locVCutM_table = {
    "Vanish Cap Under the Moat - Switch": 3626183,
    "Vanish Cap Under the Moat - Red Coins": 3626147,
    "Vanish Cap Under the Moat - Block 1-Up": 3626242
}

locBitFS_table = {
    "Bowser in the Fire Sea - Red Coins": 3626112,
    "Bowser in the Fire Sea - Key": 3626179,
    "Bowser in the Fire Sea - Swaying Stairs Block 1-Up": 3626238,
    "Bowser in the Fire Sea - Near Poles Block 1-Up": 3626239
}

locWMotR_table = {
    "Wing Mario Over the Rainbow - Red Coins": 3626154,
    "Wing Mario Over the Rainbow - Block 1-Up": 3626243,
    "Wing Mario Over the Rainbow - Bob-omb Buddy": 3626525
}

locBitS_table = {
    "Bowser in the Sky - Red Coins": 3626119,
    "Bowser in the Sky - Block 1-Up": 3626240
}

#Secret Stars found inside the Castle
locSS_table = {
    "Castle - Toad (Basement)": 3626168,
    "Castle - Toad (Second Floor)": 3626169,
    "Castle - Toad (Third Floor)": 3626170,
    "Castle - MIPS 1": 3626171,
    "Castle - MIPS 2": 3626172,
    "Castle - Yoshi": 3626244
}

locBasement_table = {
    "Castle - Drain the Moat": 3626245
}

locFreestanding1Up_table = {
    "Big Boo's Haunt - Shed Roof 1-Up": 3629100,

    "Bowser in the Dark World - Center Overhang 1-Up": 3629101,
    "Bowser in the Dark World - Right Tilting Platform Base 1-Up": 3629102,
    "Bowser in the Dark World - Left Tilting Platform Base 1-Up": 3629103,
    "Bowser in the Dark World - Far Overhang 1-Up": 3629104,

    "Bowser in the Fire Sea - First Stone Structure 1-Up": 3629105,
    "Bowser in the Fire Sea - Elevator Pole 1-Up": 3629106,
    "Bowser in the Fire Sea - Stretching Platform Trigger 1-Up": 3629107,
    "Bowser in the Fire Sea - Near Poles 1-Up": 3629108,
    "Bowser in the Fire Sea - Second Stone Structure 1-Up": 3629109,

    "Bowser in the Sky - Before Tilting Platform 1-Up": 3629110,
    "Bowser in the Sky - Arrow Ride 1-Up": 3629111,
    "Bowser in the Sky - Spark Pole Coins 1-Up": 3629112,
    "Bowser in the Sky - Final Platform 1-Up": 3629113,
    "Bowser in the Sky - Ferris Wheel 1-Up": 3629114,

    "Bob-omb Battlefield - Flower Ring 1-Up": 3629115,
    "Bob-omb Battlefield - Switch Tunnel 1-Up": 3629116,
    "Bob-omb Battlefield - Cannon Tree 1-Up": 3629117,

    "Castle - Third Tree From Waterfall 1-Up": 3629118,
    "Castle - Roof Back 1-Up": 3629119,
    "Castle - Roof Center 1-Up": 3629120,
    "Castle - Roof Front 1-Up": 3629121,
    "Castle - Bridge Coins 1-Up": 3629122,
    "Castle - Left Butterfly 1-Up": 3629123,
    "Castle - Right Butterfly 1-Up": 3629124,

    "Castle - Jolly Roger Bay Lobby 1-Up": 3629125,
    "Castle - Basement Water Tunnel Four Corners 1-Up": 3629126,

    "Cool, Cool Mountain - Snowman Tree 1-Up": 3629127,
    "Cool, Cool Mountain - Slide Shortcut First 1-Up": 3629128,
    "Cool, Cool Mountain - Slide Shortcut Second 1-Up": 3629129,

    "Cavern of the Metal Cap - Alcove 1-Up": 3629130,

    "Dire, Dire Docks - Whirlpool Clam 1-Up": 3629131,

    "Jolly Roger Bay - Underwater Coin Ring 1-Up": 3629132,
    "Jolly Roger Bay - Stone Pillar 1-Up": 3629133,

    "Lethal Lava Land - Flamethrower Ring 1-Up": 3629134,
    "Lethal Lava Land - Volcano Flamethrower 1-Up": 3629135,
    "Lethal Lava Land - Northeast Brown Platform 1-Up": 3629136,
    "Lethal Lava Land - Boil the Big Bully Star Lava 1-Up": 3629137,
    "Lethal Lava Land - Central Gray Crescent 1-Up": 3629138,
    "Lethal Lava Land - Volcano Brown Platform 1-Up": 3629139,
    "Lethal Lava Land - Northwest Curve 1-Up": 3629140,
    "Lethal Lava Land - Volcano Pole 1-Up": 3629141,

    "The Princess's Secret Slide - Coin Triggers 1-Up": 3629142,
    "The Princess's Secret Slide - Slide 1-Up": 3629143,

    "Rainbow Ride - Tricky Triangles 1-Up": 3629144,
    "Rainbow Ride - Rotating Bridge Platform 1-Up": 3629145,
    "Rainbow Ride - Ship Pole 1-Up": 3629146,
    "Rainbow Ride - Ship Tip 1-Up": 3629147,
    "Rainbow Ride - House Path Donut Lifts 1-Up": 3629148,
    "Rainbow Ride - Donut Top of Red Coin Maze 1-Up": 3629149,

    "The Secret Aquarium - Center Coin Ring 1-Up": 3629150,

    "Snowman's Land - Snowman Tree 1-Up": 3629151,
    "Snowman's Land - Igloo Ice Block 1-Up": 3629152,

    "Shifting Sand Land - Oasis Tree 1-Up": 3629153,
    "Shifting Sand Land - Near Quicksand Pits 1-Up": 3629154,
    "Shifting Sand Land - Above Quicksand Pit 1-Up": 3629155,
    "Shifting Sand Land - Pyramid Platform Triggers 1-Up": 3629156,
    "Shifting Sand Land - Pyramid Grindel 1-Up": 3629157,
    "Shifting Sand Land - Pyramid Above the First Wire Grid 1-Up": 3629158,

    "Tiny-Huge Island - Huge Island Tree 1-Up": 3629159,
    "Tiny-Huge Island - Beach Coins 1-Up": 3629160,
    "Tiny-Huge Island - Boss Bass 1-Up": 3629161,
    "Tiny-Huge Island - Koopa Area Butterfly 1-Up": 3629162,
    "Tiny-Huge Island - Huge Island Tree Butterfly 1-Up": 3629163,
    "Tiny-Huge Island - Start Butterfly 1-Up": 3629164,
    "Tiny-Huge Island - Red Coin Cave 1-Up": 3629165,

    "Tick Tock Clock - Pole 1-Up": 3629166,
    "Tick Tock Clock - Moving Bars Platform 1-Up": 3629167,

    "Tall, Tall Mountain - Start Edge 1-Up": 3629168,
    "Tall, Tall Mountain - Upper Vine Wall 1-Up": 3629169,
    "Tall, Tall Mountain - Waterfall Gap 1-Up": 3629170,
    "Tall, Tall Mountain - Vine Platform Butterfly 1-Up": 3629171,
    "Tall, Tall Mountain - Slide Start Room Corners 1-Up": 3629172,
    "Tall, Tall Mountain - Slide Entry Ledge 1-Up": 3629173,
    "Tall, Tall Mountain - Slide First 1-Up": 3629174,
    "Tall, Tall Mountain - Slide Second 1-Up": 3629175,

    "Vanish Cap Under the Moat - Upper Platform 1-Up": 3629176,
    "Vanish Cap Under the Moat - Lower Platform 1-Up": 3629177,
    "Vanish Cap Under the Moat - Red Coin Platform 1-Up": 3629178,

    "Wet-Dry World - Cylinder Lower 1-Up": 3629179,
    "Wet-Dry World - Cylinder Upper 1-Up": 3629180,
    "Wet-Dry World - Downtown Center Coin Ring 1-Up": 3629181,

    "Whomp's Fortress - Flagpole 1-Up": 3629182,
    "Whomp's Fortress - Rotating Platform Coins 1-Up": 3629183,
    "Whomp's Fortress - Flower Patch Butterfly 1-Up": 3629184,

    "Wing Mario Over the Rainbow - Bob-omb Buddy Platform 1-Up": 3629185,
    "Wing Mario Over the Rainbow - Cloud 1-Up": 3629186,
    "Wing Mario Over the Rainbow - Hanging Pole 1-Up": 3629187,

    "Whomp's Fortress - Tower Alcove 1-Up": 3629188,

    "Hazy Maze Cave - Blue Coin Trail Monty Moles": 3629189,
    "Tall, Tall Mountain - Upper Monty Moles": 3629190,
    "Hazy Maze Cave - Twin Hole Monty Moles": 3629191,
    "Tall, Tall Mountain - Lower Monty Moles": 3629192,
}

locBlocksanity_table = {
    "Big Boo's Haunt - Back Entrance Vanish Cap Block": 3629758,
    "Big Boo's Haunt - Second Floor Vanish Cap Block": 3629759,
    "Big Boo's Haunt - Top of Mansion 1-Up Block": 3629760,
    "Big Boo's Haunt - 10 Coins Block": 3629761,
    "Big Boo's Haunt - Secret Room Vanish Cap Block": 3629762,

    "Bowser in the Dark World - Metal Cap Block": 3629763,
    "Bowser in the Dark World - 3 Coins Block": 3629764,
    "Bowser in the Dark World - Tower 1-Up Block": 3629765,
    "Bowser in the Dark World - Near Goombas 1-Up Block": 3629766,

    "Bowser in the Fire Sea - Swaying Stairs 1-Up Block": 3629767,
    "Bowser in the Fire Sea - 10 Coins Block": 3629768,
    "Bowser in the Fire Sea - Near Poles 1-Up Block": 3629769,
    "Bowser in the Fire Sea - 3 Coins Block": 3629770,

    "Bowser in the Sky - 1-Up Block": 3629771,

    "Bob-omb Battlefield - Near Flower Patches Wing Cap Block": 3629772,
    "Bob-omb Battlefield - Wooden Ramp Wing Cap Block": 3629773,
    "Bob-omb Battlefield - Island Wing Cap Block": 3629774,
    "Bob-omb Battlefield - Shoot to the Island in the Sky Star Block": 3629775,

    "Castle - Roof Wing Cap Block": 3629776,

    "Cool, Cool Mountain - Near Snowman 1-Up Block": 3629777,
    "Cool, Cool Mountain - Ice Pillar 1-Up Block": 3629778,
    "Cool, Cool Mountain - Secret Slide 1-Up Block": 3629779,

    "Cavern of the Metal Cap - First Metal Cap Block": 3629780,
    "Cavern of the Metal Cap - 1-Up Block": 3629781,
    "Cavern of the Metal Cap - Near Switch Metal Cap Block": 3629782,

    "Dire, Dire Docks - Metal Cap Block": 3629783,
    "Dire, Dire Docks - Vanish Cap Block": 3629784,

    "Hazy Maze Cave - Beginning Metal Cap Block": 3629785,
    "Hazy Maze Cave - Above Pit 1-Up Block": 3629786,
    "Hazy Maze Cave - Metal-Head Mario Can Move Metal Cap Block": 3629787,
    "Hazy Maze Cave - Past Rolling Rocks 1-Up Block": 3629788,
    "Hazy Maze Cave - Toxic Maze Near Empty Alcove Metal Cap Block": 3629789,
    "Hazy Maze Cave - Toxic Maze Near Bats Metal Cap Block": 3629790,
    "Hazy Maze Cave - Toxic Maze Near Twin Monty Mole Holes Metal Cap Block": 3629791,

    "Jolly Roger Bay - Beginning Metal Cap Block": 3629792,
    "Jolly Roger Bay - 3 Coins Block": 3629793,
    "Jolly Roger Bay - Ocean Cave Metal Cap Block": 3629794,
    "Jolly Roger Bay - Blast to the Stone Pillar Star Block": 3629795,
    "Jolly Roger Bay - Purple Switch Metal Cap Block": 3629796,
    "Jolly Roger Bay - Plunder in the Sunken Ship Star Block": 3629797,

    "Lethal Lava Land - Wing Cap Block": 3629798,
    "Lethal Lava Land - Koopa Shell Block": 3629799,

    "The Princess's Secret Slide - Star Block": 3629800,

    "Rainbow Ride - Top of Red Coin Maze 1-Up Block": 3629801,
    "Rainbow Ride - Under Fly Guy 1-Up Block": 3629802,
    "Rainbow Ride - House in the Sky 1-Up Block": 3629803,
    "Rainbow Ride - Somewhere Over the Rainbow Star Block": 3629804,

    "Snowman's Land - Koopa Shell Block": 3629805,
    "Snowman's Land - Whirl from the Freezing Pond Star Block": 3629806,
    "Snowman's Land - Near Moneybags 1-Up Block": 3629807,
    "Snowman's Land - 3 Coins Block": 3629808,
    "Snowman's Land - Inside Igloo 1-Up Block": 3629809,
    "Snowman's Land - Vanish Cap Block": 3629810,

    "Shifting Sand Land - Outside Pyramid Wing Cap Block": 3629811,
    "Shifting Sand Land - Outside Pyramid 1-Up Block": 3629812,
    "Shifting Sand Land - Stone Structure Koopa Shell Block": 3629813,
    "Shifting Sand Land - Stone Structure Wing Cap Block": 3629814,
    "Shifting Sand Land - Cannon Wing Cap Block": 3629815,
    "Shifting Sand Land - Pyramid Left Path 1-Up Block": 3629816,
    "Shifting Sand Land - Pyramid Back 1-Up Block": 3629817,

    "Tiny-Huge Island - Huge Island Near Start 1-Up Block": 3629818,
    "Tiny-Huge Island - The Tip Top of the Huge Island Star Block": 3629819,
    "Tiny-Huge Island - Windy Area 1-Up Block": 3629820,
    "Tiny-Huge Island - Tiny Island Near Start 1-Up Block": 3629821,
    "Tiny-Huge Island - 3 Coins Block": 3629822,

    "Tower of the Wing Cap - Wing Cap Block": 3629823,

    "Tick Tock Clock - Above Timed Jumps on Moving Bars 3 Coins Block": 3629824,
    "Tick Tock Clock - First Pendulum 3 Coins Block": 3629825,
    "Tick Tock Clock - Top 1-Up Block": 3629826,
    "Tick Tock Clock - Top Clock Hand 10 Coins Block": 3629827,
    "Tick Tock Clock - Above Four Moving Bars 10 Coins Block": 3629828,
    "Tick Tock Clock - Past Three Spinners 3 Coins Block": 3629829,
    "Tick Tock Clock - Top Central Platform 10 Coins Block": 3629830,
    "Tick Tock Clock - Below Red Coin Spinners 10 Coins Block": 3629831,
    "Tick Tock Clock - Heave-ho First 3 Coins Block": 3629832,
    "Tick Tock Clock - Above Red Coin Spinners 3 Coins Block": 3629833,
    "Tick Tock Clock - Heave-ho Second 3 Coins Block": 3629834,
    "Tick Tock Clock - Midway Up 1-Up Block": 3629835,
    "Tick Tock Clock - Beneath the Thwomp 10 Coins Block": 3629836,

    "Tall, Tall Mountain - Red Mushroom 1-Up Block": 3629837,

    "Vanish Cap Under the Moat - Bottom of Slide Vanish Cap Block": 3629838,
    "Vanish Cap Under the Moat - 1-Up Block": 3629839,
    "Vanish Cap Under the Moat - 3 Coins Block": 3629840,
    "Vanish Cap Under the Moat - Near Switch Vanish Cap Block": 3629841,

    "Wet-Dry World - Push Block 10 Coins Block": 3629842,
    "Wet-Dry World - Shocking Arrow Lifts Star Block": 3629843,
    "Wet-Dry World - Push Block 3 Coins Block": 3629844,
    "Wet-Dry World - Pedestal 10 Coins Block": 3629845,
    "Wet-Dry World - Top of Express Elevator 10 Coins Block": 3629846,
    "Wet-Dry World - Top o' the Town Star Block": 3629847,
    "Wet-Dry World - Wooden Structure 3 Coins Block": 3629848,
    "Wet-Dry World - Downtown Vanish Cap Block": 3629849,
    "Wet-Dry World - Metal Cap Block": 3629850,
    "Wet-Dry World - Quick Race Through Downtown Star Vanish Cap Block": 3629851,
    "Wet-Dry World - Downtown 1-Up Block": 3629852,

    "Whomp's Fortress - Metal Cap Block": 3629853,

    "Wing Mario Over the Rainbow - Highest Cloud Wing Cap Block": 3629854,
    "Wing Mario Over the Rainbow - Cloud Across From Starting Cloud Wing Cap Block": 3629855,
    "Wing Mario Over the Rainbow - 1-Up Block": 3629856,
    "Wing Mario Over the Rainbow - Starting Cloud Wing Cap Block": 3629857,
    "Wing Mario Over the Rainbow - Lowest Cloud Wing Cap Block": 3629858,
    "Wing Mario Over the Rainbow - Bob-omb Buddy Platform Wing Cap Block": 3629859,
    "Wing Mario Over the Rainbow - Overlooking Bob-omb Buddy Cloud Wing Cap Block": 3629860,
}

# Correspond to 3626000 + course index * 7 + star index, then secret stars, then keys, then Coin Stars
location_table = {**locBoB_table,**locWhomp_table,**locJRB_table,**locCCM_table,**locBBH_table, \
                  **locHMC_table,**locLLL_table,**locSSL_table,**locDDD_table,**locSL_table, \
                  **locWDW_table,**locTTM_table,**locTHI_table,**locTTC_table,**locRR_table, \
                  **loc100Coin_table,**locPSS_table,**locSA_table,**locBitDW_table,**locTotWC_table, \
                  **locCotMC_table, **locVCutM_table, **locBitFS_table, **locWMotR_table, **locBitS_table, \
                  **locSS_table, **locBasement_table, **locFreestanding1Up_table, **locBlocksanity_table, \
                  **coin_count_check_location_table, **individual_coin_location_table}

loc1UpBlock_table = {
    location_name: location_table[location_name]
    for location_name in (
        "Cool, Cool Mountain - Near Snowman Block 1-Up",
        "Cool, Cool Mountain - Ice Pillar Block 1-Up",
        "Cool, Cool Mountain - Secret Slide Block 1-Up",
        "Big Boo's Haunt - Top of Mansion Block 1-Up",
        "Hazy Maze Cave - Above Pit Block 1-Up",
        "Hazy Maze Cave - Past Rolling Rocks Block 1-Up",
        "Shifting Sand Land - Outside Pyramid Block 1-Up",
        "Shifting Sand Land - Pyramid Left Path Block 1-Up",
        "Shifting Sand Land - Pyramid Back Block 1-Up",
        "Snowman's Land - Near Moneybags Block 1-Up",
        "Snowman's Land - Inside Igloo Block 1-Up",
        "Wet-Dry World - Downtown Block 1-Up",
        "Tall, Tall Mountain - Red Mushroom Block 1-Up",
        "Tiny-Huge Island - Tiny Island Near Start Block 1-Up",
        "Tiny-Huge Island - Huge Island Near Start Block 1-Up",
        "Tiny-Huge Island - Windy Area Block 1-Up",
        "Tick Tock Clock - Midway Up Block 1-Up",
        "Tick Tock Clock - Top Block 1-Up",
        "Rainbow Ride - Top of Red Coin Maze Block 1-Up",
        "Rainbow Ride - Under Fly Guy Block 1-Up",
        "Rainbow Ride - House in the Sky Block 1-Up",
        "Bowser in the Dark World - Tower Block 1-Up",
        "Bowser in the Dark World - Near Goombas Block 1-Up",
        "Cavern of the Metal Cap - Block 1-Up",
        "Vanish Cap Under the Moat - Block 1-Up",
        "Bowser in the Fire Sea - Swaying Stairs Block 1-Up",
        "Bowser in the Fire Sea - Near Poles Block 1-Up",
        "Wing Mario Over the Rainbow - Block 1-Up",
        "Bowser in the Sky - Block 1-Up",
    )
}
locOneUp_table = {**loc1UpBlock_table, **locFreestanding1Up_table}

trigger_1up_location_ids = {
    3629106, 3629107, 3629112, 3629115, 3629117, 3629118,
    3629122, 3629125, 3629126, 3629127,
    3629131, 3629132, 3629134, 3629141, 3629142, 3629146,
    3629149, 3629150, 3629151, 3629153, 3629156, 3629159,
    3629160, 3629166, 3629167,
    3629172, 3629178, 3629181, 3629182, 3629183,
    3629185, 3629189, 3629190, 3629191, 3629192,
}

butterfly_1up_location_ids = {
    3629123, 3629124, 3629162, 3629163, 3629164, 3629171, 3629184,
}

locTrigger1Up_table = {
    location_name: location_id
    for location_name, location_id in locFreestanding1Up_table.items()
    if location_id in trigger_1up_location_ids
}
locButterfly1Up_table = {
    location_name: location_id
    for location_name, location_id in locFreestanding1Up_table.items()
    if location_id in butterfly_1up_location_ids
}
locStandalone1Up_table = {
    location_name: location_id
    for location_name, location_id in locFreestanding1Up_table.items()
    if location_id not in trigger_1up_location_ids
    and location_id not in butterfly_1up_location_ids
}

one_up_unlock_category_by_location = {
    **{location_name: "Freestanding 1-Ups" for location_name in locStandalone1Up_table},
    **{location_name: "Trigger 1-Ups" for location_name in locTrigger1Up_table},
    **{location_name: "Butterflies" for location_name in locButterfly1Up_table},
    **{location_name: "1-Up Blocks" for location_name in loc1UpBlock_table},
    **{location_name: "1-Up Blocks" for location_name in locBlocksanity_table
       if location_name.endswith("1-Up Block")},
}


def _locations_with_prefix(prefix: str) -> set[str]:
    return {
        location_name
        for location_name in location_table
        if location_name.startswith(f"{prefix} - ")
    }


main_course_location_group_names = (
    "Bob-omb Battlefield",
    "Whomp's Fortress",
    "Jolly Roger Bay",
    "Cool, Cool Mountain",
    "Big Boo's Haunt",
    "Hazy Maze Cave",
    "Lethal Lava Land",
    "Shifting Sand Land",
    "Dire, Dire Docks",
    "Snowman's Land",
    "Wet-Dry World",
    "Tall, Tall Mountain",
    "Tiny-Huge Island",
    "Tick Tock Clock",
    "Rainbow Ride",
)

secret_stage_location_group_names = (
    "The Princess's Secret Slide",
    "The Secret Aquarium",
    "Tower of the Wing Cap",
    "Cavern of the Metal Cap",
    "Vanish Cap Under the Moat",
    "Wing Mario Over the Rainbow",
)

bowser_stage_location_group_names = (
    "Bowser in the Dark World",
    "Bowser in the Fire Sea",
    "Bowser in the Sky",
)

location_name_groups: dict[str, set[str]] = {
    location_group_name: _locations_with_prefix(location_group_name)
    for location_group_name in (
        *main_course_location_group_names,
        *secret_stage_location_group_names,
        *bowser_stage_location_group_names,
        "Castle",
    )
}

location_name_groups.update({
    "Main Courses": set().union(
        *(location_name_groups[group_name] for group_name in main_course_location_group_names)),
    "Secret Stages": set().union(
        *(location_name_groups[group_name] for group_name in secret_stage_location_group_names)),
    "Bowser Stages": set().union(
        *(location_name_groups[group_name] for group_name in bowser_stage_location_group_names)),
    "Coin Stars": set(loc100Coin_table),
    "Coin Count Checks": set(coin_count_check_location_table),
    "Main Course Coin Count Checks": set(coin_count_check_location_table) - set(secret_stage_coin_count_check_location_table),
    "Secret Stage Coin Count Checks": set(secret_stage_coin_count_check_location_table),
    "1-Ups": set(locOneUp_table),
    "1-Ups from Blocks": set(loc1UpBlock_table),
    "Freestanding 1-Ups": set(locFreestanding1Up_table),
    "Blocksanity": set(locBlocksanity_table),
    "1-Up Blocks": {
        location_name for location_name in locBlocksanity_table if "1-Up Block" in location_name
    },
    "Cap Blocks": {
        location_name for location_name in locBlocksanity_table if "Cap Block" in location_name
    },
    "Coin Blocks": {
        location_name for location_name in locBlocksanity_table if " Coins Block" in location_name
    },
    "Individual Coin Checks": set(individual_coin_location_table),
    "Shell Blocks": {
        location_name for location_name in locBlocksanity_table if "Shell Block" in location_name
    },
    "Star Blocks": {
        location_name for location_name in locBlocksanity_table if "Star Block" in location_name
    },
    "Bob-omb Buddies": {
        location_name for location_name in location_table if location_name.endswith(" - Bob-omb Buddy")
    },
})
