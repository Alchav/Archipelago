from typing import NamedTuple, Callable

from BaseClasses import Item, ItemClassification
from worlds.tloz.Items import useful

sm64ex_base_id: int = 3626000
ut_glitch_item_name = "ut_glitch"

def Progression(options):
    return ItemClassification.progression

def ProgressionDeprioritized(options):
    return ItemClassification.progression_deprioritized

def ProgressionDeprioritizedSkipBalancing(options):
    return ItemClassification.progression_deprioritized_skip_balancing

def Useful(options):
    return ItemClassification.useful

def Filler(options):
    return ItemClassification.filler

class SM64Item(Item):
    game: str = "SM64: Spicy Mycena 64"

class SM64ItemData(NamedTuple):
    code: int | None = None
    classification: Callable = Progression

generic_item_data_table: dict[str, SM64ItemData] = {
    "Basement Key": SM64ItemData(sm64ex_base_id + 178),
    "Second Floor Key": SM64ItemData(sm64ex_base_id + 179),
    "Progressive Key": SM64ItemData(sm64ex_base_id + 180),
    "Wing Cap": SM64ItemData(sm64ex_base_id + 181),
    "Metal Cap": SM64ItemData(sm64ex_base_id + 182),
    "Vanish Cap": SM64ItemData(sm64ex_base_id + 183),
    "1-Up Mushroom": SM64ItemData(sm64ex_base_id + 184, Filler),
    ut_glitch_item_name: SM64ItemData(),
}

global_cap_item_names = ("Wing Cap", "Metal Cap", "Vanish Cap")

feature_item_data_table: dict[str, SM64ItemData] = {
    "Bob-omb Battlefield - King Bob-omb": SM64ItemData(sm64ex_base_id + 245, ProgressionDeprioritized),
    "Bob-omb Battlefield - Koopa the Quick": SM64ItemData(sm64ex_base_id + 246, ProgressionDeprioritized),
    "Bob-omb Battlefield - Bob-omb Buddy": SM64ItemData(sm64ex_base_id + 247, ProgressionDeprioritized),
    "Whomp's Fortress - Whomp King": SM64ItemData(sm64ex_base_id + 248, ProgressionDeprioritized),
    "Whomp's Fortress - Fortress": SM64ItemData(sm64ex_base_id + 249),
    "Whomp's Fortress - Bob-omb Buddy": SM64ItemData(sm64ex_base_id + 250, ProgressionDeprioritized),
    "Whomp's Fortress - Hoot": SM64ItemData(sm64ex_base_id + 251),
    "Cool, Cool Mountain - Snowman's Head": SM64ItemData(sm64ex_base_id + 252, ProgressionDeprioritized),
    "Cool, Cool Mountain - Big Penguin": SM64ItemData(sm64ex_base_id + 253, ProgressionDeprioritized),
    "Jolly Roger Bay - Sunken Ship": SM64ItemData(sm64ex_base_id + 254, ProgressionDeprioritized),
    "Jolly Roger Bay - Raised Ship": SM64ItemData(sm64ex_base_id + 255, ProgressionDeprioritized),
    "Jolly Roger Bay - Bob-omb Buddy": SM64ItemData(sm64ex_base_id + 256, ProgressionDeprioritized),
    "Jolly Roger Bay - Jet Stream": SM64ItemData(sm64ex_base_id + 257, ProgressionDeprioritized),
    "Jolly Roger Bay - Unagi": SM64ItemData(sm64ex_base_id + 258, ProgressionDeprioritized),
    "Lethal Lava Land - Koopa Shell": SM64ItemData(sm64ex_base_id + 259, ProgressionDeprioritizedSkipBalancing),
    "Shifting Sand Land - Klepto Star": SM64ItemData(sm64ex_base_id + 260, ProgressionDeprioritized),
    "Tiny-Huge Island - Koopa the Quick": SM64ItemData(sm64ex_base_id + 261, ProgressionDeprioritized),
    "Tall, Tall Mountain - Ukiki": SM64ItemData(sm64ex_base_id + 262, ProgressionDeprioritized),
    "Dire, Dire Docks - Manta Ray": SM64ItemData(sm64ex_base_id + 263, ProgressionDeprioritized),
    "Dire, Dire Docks - Bowser's Sub": SM64ItemData(sm64ex_base_id + 264, ProgressionDeprioritized),
    "Dire, Dire Docks - Poles": SM64ItemData(sm64ex_base_id + 265),
    "Big Boo's Haunt - Staircase": SM64ItemData(sm64ex_base_id + 266),
    "Big Boo's Haunt - Merry-go-round": SM64ItemData(sm64ex_base_id + 267),
}

castle_key_item_data_table: dict[str, SM64ItemData] = {
    "Dark World Key": SM64ItemData(sm64ex_base_id + 268),
    "Progressive Basement Key": SM64ItemData(sm64ex_base_id + 269),
    "Progressive Upstairs Key": SM64ItemData(sm64ex_base_id + 270),
}

castle_progression_item_data_table: dict[str, SM64ItemData] = {
    "Castle - Progressive MIPS": SM64ItemData(sm64ex_base_id + 271, ProgressionDeprioritized),
    "Unlock Tower of the Wing Cap": SM64ItemData(sm64ex_base_id + 272),
    "Unlock Big Boo's Haunt": SM64ItemData(sm64ex_base_id + 273),
    "Castle - Toads": SM64ItemData(sm64ex_base_id + 274),
    "Castle - Cannon Unlock": SM64ItemData(sm64ex_base_id + 275, ProgressionDeprioritizedSkipBalancing),
    "Castle - Yoshi": SM64ItemData(sm64ex_base_id + 276, ProgressionDeprioritizedSkipBalancing),
    "Unlock Bowser in the Fire Sea": SM64ItemData(sm64ex_base_id + 304),
    "Unlock Vanish Cap Under the Moat": SM64ItemData(sm64ex_base_id + 555),
}

cap_item_data_table: dict[str, SM64ItemData] = {
    "Bob-omb Battlefield - Wing Cap": SM64ItemData(sm64ex_base_id + 277),
    "Castle - Wing Cap": SM64ItemData(sm64ex_base_id + 278, Filler),
    "Lethal Lava Land - Wing Cap": SM64ItemData(sm64ex_base_id + 279, ProgressionDeprioritizedSkipBalancing),
    "Shifting Sand Land - Wing Cap": SM64ItemData(sm64ex_base_id + 280, ProgressionDeprioritized),
    "Tower of the Wing Cap - Wing Cap": SM64ItemData(sm64ex_base_id + 281, Filler),
    "Wing Mario Over the Rainbow - Wing Cap": SM64ItemData(sm64ex_base_id + 282),
    "Whomp's Fortress - Metal Cap": SM64ItemData(sm64ex_base_id + 283, Filler),
    "Jolly Roger Bay - Metal Cap": SM64ItemData(sm64ex_base_id + 284, ProgressionDeprioritized),
    "Hazy Maze Cave - Metal Cap": SM64ItemData(sm64ex_base_id + 285, ProgressionDeprioritized),
    "Dire, Dire Docks - Metal Cap": SM64ItemData(sm64ex_base_id + 286, ProgressionDeprioritized),
    "Wet-Dry World - Metal Cap": SM64ItemData(sm64ex_base_id + 287, Filler),
    "Cavern of the Metal Cap - Metal Cap": SM64ItemData(sm64ex_base_id + 288, ProgressionDeprioritized),
    "Bowser in the Dark World - Metal Cap": SM64ItemData(sm64ex_base_id + 289, Filler),
    "Big Boo's Haunt - Vanish Cap": SM64ItemData(sm64ex_base_id + 290, ProgressionDeprioritized),
    "Dire, Dire Docks - Vanish Cap": SM64ItemData(sm64ex_base_id + 291, ProgressionDeprioritized),
    "Snowman's Land - Vanish Cap": SM64ItemData(sm64ex_base_id + 292, ProgressionDeprioritized),
    "Vanish Cap Under the Moat - Vanish Cap": SM64ItemData(sm64ex_base_id + 293, ProgressionDeprioritized),
    "Wet-Dry World - Vanish Cap": SM64ItemData(sm64ex_base_id + 294, ProgressionDeprioritizedSkipBalancing),
}

simple_arbitrary_item_data_table: dict[str, SM64ItemData] = {
    "Hazy Maze Cave - Swimming Beast": SM64ItemData(sm64ex_base_id + 295),
    "Rainbow Ride - Carpets": SM64ItemData(sm64ex_base_id + 296),
    "Tiny-Huge Island - Warp Pipes": SM64ItemData(sm64ex_base_id + 298),
    "Cool, Cool Mountain - Baby Penguins": SM64ItemData(sm64ex_base_id + 299, ProgressionDeprioritizedSkipBalancing),
    "Snowman's Land - Penguin": SM64ItemData(sm64ex_base_id + 300, ProgressionDeprioritizedSkipBalancing),
    "Shifting Sand Land - Pyramid Elevator": SM64ItemData(sm64ex_base_id + 301),
    "Wet-Dry World - Water Level Diamond": SM64ItemData(sm64ex_base_id + 305),
    "Tick Tock Clock - Spinners": SM64ItemData(sm64ex_base_id + 319),
}

global_checkerboard_item_names = ("Checkerboard Platforms",)
global_rolling_log_item_names = ("Rolling Logs",)
global_purple_switch_item_names = ("Purple Switches",)

global_arbitrary_item_data_table: dict[str, SM64ItemData] = {
    "Checkerboard Platforms": SM64ItemData(sm64ex_base_id + 297),
    "Rolling Logs": SM64ItemData(sm64ex_base_id + 302),
    "Purple Switches": SM64ItemData(sm64ex_base_id + 303),
}

checkerboard_item_data_table: dict[str, SM64ItemData] = {
    "Bob-omb Battlefield - Checkerboard Platforms": SM64ItemData(sm64ex_base_id + 306, Filler),
    "Whomp's Fortress - Checkerboard Platforms": SM64ItemData(sm64ex_base_id + 307),
    "Lethal Lava Land - Checkerboard Platforms": SM64ItemData(sm64ex_base_id + 308, ProgressionDeprioritizedSkipBalancing),
    "Hazy Maze Cave - Checkerboard Platform": SM64ItemData(sm64ex_base_id + 309),
    "Vanish Cap Under the Moat - Checkerboard Platforms": SM64ItemData(sm64ex_base_id + 310),
}

rolling_log_item_data_table: dict[str, SM64ItemData] = {
    "Lethal Lava Land - Rolling Log": SM64ItemData(sm64ex_base_id + 311, ProgressionDeprioritizedSkipBalancing),
    "Tall, Tall Mountain - Rolling Log": SM64ItemData(sm64ex_base_id + 312, Filler),
}

purple_switch_item_data_table: dict[str, SM64ItemData] = {
    "Bob-omb Battlefield - Purple Switch": SM64ItemData(sm64ex_base_id + 313, Filler),
    "Hazy Maze Cave - Purple Switch": SM64ItemData(sm64ex_base_id + 314, ProgressionDeprioritizedSkipBalancing),
    "Wet-Dry World - Purple Switch": SM64ItemData(sm64ex_base_id + 315),
    "Rainbow Ride - Purple Switch": SM64ItemData(sm64ex_base_id + 316, ProgressionDeprioritizedSkipBalancing),
    "Bowser in the Dark World - Purple Switch": SM64ItemData(sm64ex_base_id + 317),
    "Bowser in the Sky - Purple Switch": SM64ItemData(sm64ex_base_id + 318, ItemClassification.progression_skip_balancing),
    "Jolly Roger Bay - Purple Switch": SM64ItemData(sm64ex_base_id + 321, Filler),
    "Dire, Dire Docks - Purple Switch": SM64ItemData(sm64ex_base_id + 322, ProgressionDeprioritizedSkipBalancing),
    "Tall, Tall Mountain - Purple Switch": SM64ItemData(sm64ex_base_id + 323, ProgressionDeprioritizedSkipBalancing),
    "Tiny-Huge Island - Purple Switch": SM64ItemData(sm64ex_base_id + 324, ProgressionDeprioritizedSkipBalancing),
}

optional_item_data_table: dict[str, SM64ItemData] = {
    "Mario's Hat": SM64ItemData(sm64ex_base_id + 320, Useful),
}

bowser_stage_1up_item_data_table: dict[str, SM64ItemData] = {
    "Bowser Stage Extra 1-Ups": SM64ItemData(sm64ex_base_id + 556, ProgressionDeprioritized),
    "Bowser in the Dark World - Extra 1-Ups": SM64ItemData(sm64ex_base_id + 557, ProgressionDeprioritized),
    "Bowser in the Fire Sea - Extra 1-Ups": SM64ItemData(sm64ex_base_id + 558, ProgressionDeprioritized),
}

arbitrary_item_data_table: dict[str, SM64ItemData] = {
    **simple_arbitrary_item_data_table,
    **global_arbitrary_item_data_table,
    **checkerboard_item_data_table,
    **rolling_log_item_data_table,
    **purple_switch_item_data_table,
}

action_item_data_table: dict[str, SM64ItemData] = {
    "Double Jump": SM64ItemData(sm64ex_base_id + 185),
    "Triple Jump": SM64ItemData(sm64ex_base_id + 186),
    "Long Jump": SM64ItemData(sm64ex_base_id + 187),
    "Backflip": SM64ItemData(sm64ex_base_id + 188),
    "Side Flip": SM64ItemData(sm64ex_base_id + 189),
    "Wall Kick": SM64ItemData(sm64ex_base_id + 190),
    "Dive": SM64ItemData(sm64ex_base_id + 191),
    "Ground Pound": SM64ItemData(sm64ex_base_id + 192),
    "Kick": SM64ItemData(sm64ex_base_id + 193),
    "Climb": SM64ItemData(sm64ex_base_id + 194),
    "Ledge Grab": SM64ItemData(sm64ex_base_id + 195),
}

randomized_action_item_names = (
    "Triple Jump",
    "Long Jump",
    "Backflip",
    "Side Flip",
    "Wall Kick",
    "Dive",
    "Ground Pound",
    "Kick",
    "Climb",
    "Ledge Grab",
)

per_level_move_area_names = (
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
    "Castle",
)

per_level_action_item_data_table: dict[str, SM64ItemData] = {
    # Bob-omb Battlefield
    "Bob-omb Battlefield - Triple Jump": SM64ItemData(sm64ex_base_id + 325),
    "Bob-omb Battlefield - Long Jump": SM64ItemData(sm64ex_base_id + 326),
    "Bob-omb Battlefield - Backflip": SM64ItemData(sm64ex_base_id + 327, ProgressionDeprioritizedSkipBalancing),
    "Bob-omb Battlefield - Side Flip": SM64ItemData(sm64ex_base_id + 328, ProgressionDeprioritizedSkipBalancing),
    "Bob-omb Battlefield - Wall Kick": SM64ItemData(sm64ex_base_id + 329, Useful),
    "Bob-omb Battlefield - Dive": SM64ItemData(sm64ex_base_id + 330, Useful),
    "Bob-omb Battlefield - Ground Pound": SM64ItemData(sm64ex_base_id + 331, ProgressionDeprioritizedSkipBalancing),
    "Bob-omb Battlefield - Kick": SM64ItemData(sm64ex_base_id + 332, Useful),
    "Bob-omb Battlefield - Climb": SM64ItemData(sm64ex_base_id + 333, ProgressionDeprioritizedSkipBalancing),
    "Bob-omb Battlefield - Ledge Grab": SM64ItemData(sm64ex_base_id + 334, Useful),
    # Whomp's Fortress
    "Whomp's Fortress - Triple Jump": SM64ItemData(sm64ex_base_id + 335),
    "Whomp's Fortress - Long Jump": SM64ItemData(sm64ex_base_id + 336, ProgressionDeprioritizedSkipBalancing),
    "Whomp's Fortress - Backflip": SM64ItemData(sm64ex_base_id + 337, Useful),
    "Whomp's Fortress - Side Flip": SM64ItemData(sm64ex_base_id + 338),
    "Whomp's Fortress - Wall Kick": SM64ItemData(sm64ex_base_id + 339),
    "Whomp's Fortress - Dive": SM64ItemData(sm64ex_base_id + 340, Useful),
    "Whomp's Fortress - Ground Pound": SM64ItemData(sm64ex_base_id + 341),
    "Whomp's Fortress - Kick": SM64ItemData(sm64ex_base_id + 342, Useful),
    "Whomp's Fortress - Climb": SM64ItemData(sm64ex_base_id + 343, ProgressionDeprioritizedSkipBalancing),
    "Whomp's Fortress - Ledge Grab": SM64ItemData(sm64ex_base_id + 344, ProgressionDeprioritizedSkipBalancing),
    # Jolly Roger Bay
    "Jolly Roger Bay - Triple Jump": SM64ItemData(sm64ex_base_id + 345),
    "Jolly Roger Bay - Long Jump": SM64ItemData(sm64ex_base_id + 346, Useful),
    "Jolly Roger Bay - Backflip": SM64ItemData(sm64ex_base_id + 347),
    "Jolly Roger Bay - Side Flip": SM64ItemData(sm64ex_base_id + 348),
    "Jolly Roger Bay - Wall Kick": SM64ItemData(sm64ex_base_id + 349),
    "Jolly Roger Bay - Dive": SM64ItemData(sm64ex_base_id + 350, Useful),
    "Jolly Roger Bay - Ground Pound": SM64ItemData(sm64ex_base_id + 351, ProgressionDeprioritizedSkipBalancing),
    "Jolly Roger Bay - Kick": SM64ItemData(sm64ex_base_id + 352, Useful),
    "Jolly Roger Bay - Climb": SM64ItemData(sm64ex_base_id + 353),
    "Jolly Roger Bay - Ledge Grab": SM64ItemData(sm64ex_base_id + 354),
    # Cool, Cool Mountain
    "Cool, Cool Mountain - Triple Jump": SM64ItemData(sm64ex_base_id + 355, ProgressionDeprioritizedSkipBalancing),
    "Cool, Cool Mountain - Long Jump": SM64ItemData(sm64ex_base_id + 356, Useful),
    "Cool, Cool Mountain - Backflip": SM64ItemData(sm64ex_base_id + 357, Useful),
    "Cool, Cool Mountain - Side Flip": SM64ItemData(sm64ex_base_id + 358, Useful),
    "Cool, Cool Mountain - Wall Kick": SM64ItemData(sm64ex_base_id + 359, ProgressionDeprioritizedSkipBalancing),
    "Cool, Cool Mountain - Dive": SM64ItemData(sm64ex_base_id + 360, Useful),
    "Cool, Cool Mountain - Ground Pound": SM64ItemData(sm64ex_base_id + 361, ProgressionDeprioritizedSkipBalancing),
    "Cool, Cool Mountain - Kick": SM64ItemData(sm64ex_base_id + 362, Useful),
    "Cool, Cool Mountain - Climb": SM64ItemData(sm64ex_base_id + 363, Useful),
    "Cool, Cool Mountain - Ledge Grab": SM64ItemData(sm64ex_base_id + 364, Useful),
    # Big Boo's Haunt
    "Big Boo's Haunt - Triple Jump": SM64ItemData(sm64ex_base_id + 365),
    "Big Boo's Haunt - Long Jump": SM64ItemData(sm64ex_base_id + 366),
    "Big Boo's Haunt - Backflip": SM64ItemData(sm64ex_base_id + 367, ProgressionDeprioritizedSkipBalancing),
    "Big Boo's Haunt - Side Flip": SM64ItemData(sm64ex_base_id + 368),
    "Big Boo's Haunt - Wall Kick": SM64ItemData(sm64ex_base_id + 369),
    "Big Boo's Haunt - Dive": SM64ItemData(sm64ex_base_id + 370, Useful),
    "Big Boo's Haunt - Ground Pound": SM64ItemData(sm64ex_base_id + 371, ProgressionDeprioritizedSkipBalancing),
    "Big Boo's Haunt - Kick": SM64ItemData(sm64ex_base_id + 372, ProgressionDeprioritizedSkipBalancing),
    "Big Boo's Haunt - Climb": SM64ItemData(sm64ex_base_id + 373, Useful),
    "Big Boo's Haunt - Ledge Grab": SM64ItemData(sm64ex_base_id + 374),
    # Hazy Maze Cave
    "Hazy Maze Cave - Triple Jump": SM64ItemData(sm64ex_base_id + 375),
    "Hazy Maze Cave - Long Jump": SM64ItemData(sm64ex_base_id + 376),
    "Hazy Maze Cave - Backflip": SM64ItemData(sm64ex_base_id + 377),
    "Hazy Maze Cave - Side Flip": SM64ItemData(sm64ex_base_id + 378),
    "Hazy Maze Cave - Wall Kick": SM64ItemData(sm64ex_base_id + 379),
    "Hazy Maze Cave - Dive": SM64ItemData(sm64ex_base_id + 380, Useful),
    "Hazy Maze Cave - Ground Pound": SM64ItemData(sm64ex_base_id + 381, ProgressionDeprioritizedSkipBalancing),
    "Hazy Maze Cave - Kick": SM64ItemData(sm64ex_base_id + 382, Useful),
    "Hazy Maze Cave - Climb": SM64ItemData(sm64ex_base_id + 383),
    "Hazy Maze Cave - Ledge Grab": SM64ItemData(sm64ex_base_id + 384),
    # Lethal Lava Land
    "Lethal Lava Land - Triple Jump": SM64ItemData(sm64ex_base_id + 385),
    "Lethal Lava Land - Long Jump": SM64ItemData(sm64ex_base_id + 386),
    "Lethal Lava Land - Backflip": SM64ItemData(sm64ex_base_id + 387, Useful),
    "Lethal Lava Land - Side Flip": SM64ItemData(sm64ex_base_id + 388, Useful),
    "Lethal Lava Land - Wall Kick": SM64ItemData(sm64ex_base_id + 389, Useful),
    "Lethal Lava Land - Dive": SM64ItemData(sm64ex_base_id + 390),
    "Lethal Lava Land - Ground Pound": SM64ItemData(sm64ex_base_id + 391, Useful),
    "Lethal Lava Land - Kick": SM64ItemData(sm64ex_base_id + 392, Useful),
    "Lethal Lava Land - Climb": SM64ItemData(sm64ex_base_id + 393),
    "Lethal Lava Land - Ledge Grab": SM64ItemData(sm64ex_base_id + 394, Useful),
    # Shifting Sand Land
    "Shifting Sand Land - Triple Jump": SM64ItemData(sm64ex_base_id + 395),
    "Shifting Sand Land - Long Jump": SM64ItemData(sm64ex_base_id + 396, ProgressionDeprioritizedSkipBalancing),
    "Shifting Sand Land - Backflip": SM64ItemData(sm64ex_base_id + 397),
    "Shifting Sand Land - Side Flip": SM64ItemData(sm64ex_base_id + 398),
    "Shifting Sand Land - Wall Kick": SM64ItemData(sm64ex_base_id + 399, Useful),
    "Shifting Sand Land - Dive": SM64ItemData(sm64ex_base_id + 400, Useful),
    "Shifting Sand Land - Ground Pound": SM64ItemData(sm64ex_base_id + 401),
    "Shifting Sand Land - Kick": SM64ItemData(sm64ex_base_id + 402, ProgressionDeprioritizedSkipBalancing),
    "Shifting Sand Land - Climb": SM64ItemData(sm64ex_base_id + 403),
    "Shifting Sand Land - Ledge Grab": SM64ItemData(sm64ex_base_id + 404),
    # Dire, Dire Docks
    "Dire, Dire Docks - Triple Jump": SM64ItemData(sm64ex_base_id + 405, ProgressionDeprioritizedSkipBalancing),
    "Dire, Dire Docks - Long Jump": SM64ItemData(sm64ex_base_id + 406, Useful),
    "Dire, Dire Docks - Backflip": SM64ItemData(sm64ex_base_id + 407, Useful),
    "Dire, Dire Docks - Side Flip": SM64ItemData(sm64ex_base_id + 408, Useful),
    "Dire, Dire Docks - Wall Kick": SM64ItemData(sm64ex_base_id + 409, ProgressionDeprioritizedSkipBalancing),
    "Dire, Dire Docks - Dive": SM64ItemData(sm64ex_base_id + 410, ProgressionDeprioritizedSkipBalancing),
    "Dire, Dire Docks - Ground Pound": SM64ItemData(sm64ex_base_id + 411, ProgressionDeprioritizedSkipBalancing),
    "Dire, Dire Docks - Kick": SM64ItemData(sm64ex_base_id + 412, Useful),
    "Dire, Dire Docks - Climb": SM64ItemData(sm64ex_base_id + 413, ProgressionDeprioritizedSkipBalancing),
    "Dire, Dire Docks - Ledge Grab": SM64ItemData(sm64ex_base_id + 414, ProgressionDeprioritizedSkipBalancing),
    # Snowman's Land
    "Snowman's Land - Triple Jump": SM64ItemData(sm64ex_base_id + 415),
    "Snowman's Land - Long Jump": SM64ItemData(sm64ex_base_id + 416, Useful),
    "Snowman's Land - Backflip": SM64ItemData(sm64ex_base_id + 417),
    "Snowman's Land - Side Flip": SM64ItemData(sm64ex_base_id + 418),
    "Snowman's Land - Wall Kick": SM64ItemData(sm64ex_base_id + 419),
    "Snowman's Land - Dive": SM64ItemData(sm64ex_base_id + 420, Useful),
    "Snowman's Land - Ground Pound": SM64ItemData(sm64ex_base_id + 421, Useful),
    "Snowman's Land - Kick": SM64ItemData(sm64ex_base_id + 422, Useful),
    "Snowman's Land - Climb": SM64ItemData(sm64ex_base_id + 423, Useful),
    "Snowman's Land - Ledge Grab": SM64ItemData(sm64ex_base_id + 424),
    # Wet-Dry World
    "Wet-Dry World - Triple Jump": SM64ItemData(sm64ex_base_id + 425),
    "Wet-Dry World - Long Jump": SM64ItemData(sm64ex_base_id + 426),
    "Wet-Dry World - Backflip": SM64ItemData(sm64ex_base_id + 427),
    "Wet-Dry World - Side Flip": SM64ItemData(sm64ex_base_id + 428),
    "Wet-Dry World - Wall Kick": SM64ItemData(sm64ex_base_id + 429),
    "Wet-Dry World - Dive": SM64ItemData(sm64ex_base_id + 430),
    "Wet-Dry World - Ground Pound": SM64ItemData(sm64ex_base_id + 431, ProgressionDeprioritizedSkipBalancing),
    "Wet-Dry World - Kick": SM64ItemData(sm64ex_base_id + 432, ProgressionDeprioritizedSkipBalancing),
    "Wet-Dry World - Climb": SM64ItemData(sm64ex_base_id + 433, Useful),
    "Wet-Dry World - Ledge Grab": SM64ItemData(sm64ex_base_id + 434),
    # Tall, Tall Mountain
    "Tall, Tall Mountain - Triple Jump": SM64ItemData(sm64ex_base_id + 435),
    "Tall, Tall Mountain - Long Jump": SM64ItemData(sm64ex_base_id + 436),
    "Tall, Tall Mountain - Backflip": SM64ItemData(sm64ex_base_id + 437, ProgressionDeprioritizedSkipBalancing),
    "Tall, Tall Mountain - Side Flip": SM64ItemData(sm64ex_base_id + 438),
    "Tall, Tall Mountain - Wall Kick": SM64ItemData(sm64ex_base_id + 439),
    "Tall, Tall Mountain - Dive": SM64ItemData(sm64ex_base_id + 440),
    "Tall, Tall Mountain - Ground Pound": SM64ItemData(sm64ex_base_id + 441, Useful),
    "Tall, Tall Mountain - Kick": SM64ItemData(sm64ex_base_id + 442),
    "Tall, Tall Mountain - Climb": SM64ItemData(sm64ex_base_id + 443, ProgressionDeprioritizedSkipBalancing),
    "Tall, Tall Mountain - Ledge Grab": SM64ItemData(sm64ex_base_id + 444),
    # Tiny-Huge Island
    "Tiny-Huge Island - Triple Jump": SM64ItemData(sm64ex_base_id + 445),
    "Tiny-Huge Island - Long Jump": SM64ItemData(sm64ex_base_id + 446),
    "Tiny-Huge Island - Backflip": SM64ItemData(sm64ex_base_id + 447),
    "Tiny-Huge Island - Side Flip": SM64ItemData(sm64ex_base_id + 448),
    "Tiny-Huge Island - Wall Kick": SM64ItemData(sm64ex_base_id + 449),
    "Tiny-Huge Island - Dive": SM64ItemData(sm64ex_base_id + 450),
    "Tiny-Huge Island - Ground Pound": SM64ItemData(sm64ex_base_id + 451),
    "Tiny-Huge Island - Kick": SM64ItemData(sm64ex_base_id + 452),
    "Tiny-Huge Island - Climb": SM64ItemData(sm64ex_base_id + 453, Useful),
    "Tiny-Huge Island - Ledge Grab": SM64ItemData(sm64ex_base_id + 454),
    # Tick Tock Clock
    "Tick Tock Clock - Triple Jump": SM64ItemData(sm64ex_base_id + 455),
    "Tick Tock Clock - Long Jump": SM64ItemData(sm64ex_base_id + 456, ProgressionDeprioritizedSkipBalancing),
    "Tick Tock Clock - Backflip": SM64ItemData(sm64ex_base_id + 457),
    "Tick Tock Clock - Side Flip": SM64ItemData(sm64ex_base_id + 458),
    "Tick Tock Clock - Wall Kick": SM64ItemData(sm64ex_base_id + 459),
    "Tick Tock Clock - Dive": SM64ItemData(sm64ex_base_id + 460, Useful),
    "Tick Tock Clock - Ground Pound": SM64ItemData(sm64ex_base_id + 461, ProgressionDeprioritizedSkipBalancing),
    "Tick Tock Clock - Kick": SM64ItemData(sm64ex_base_id + 462, Useful),
    "Tick Tock Clock - Climb": SM64ItemData(sm64ex_base_id + 463),
    "Tick Tock Clock - Ledge Grab": SM64ItemData(sm64ex_base_id + 464),
    # Rainbow Ride
    "Rainbow Ride - Triple Jump": SM64ItemData(sm64ex_base_id + 465),
    "Rainbow Ride - Long Jump": SM64ItemData(sm64ex_base_id + 466),
    "Rainbow Ride - Backflip": SM64ItemData(sm64ex_base_id + 467),
    "Rainbow Ride - Side Flip": SM64ItemData(sm64ex_base_id + 468),
    "Rainbow Ride - Wall Kick": SM64ItemData(sm64ex_base_id + 469),
    "Rainbow Ride - Dive": SM64ItemData(sm64ex_base_id + 470),
    "Rainbow Ride - Ground Pound": SM64ItemData(sm64ex_base_id + 471, ProgressionDeprioritizedSkipBalancing),
    "Rainbow Ride - Kick": SM64ItemData(sm64ex_base_id + 472, Useful),
    "Rainbow Ride - Climb": SM64ItemData(sm64ex_base_id + 473),
    "Rainbow Ride - Ledge Grab": SM64ItemData(sm64ex_base_id + 474),
    # Castle
    "Castle - Triple Jump": SM64ItemData(sm64ex_base_id + 475),
    "Castle - Long Jump": SM64ItemData(sm64ex_base_id + 476),
    "Castle - Backflip": SM64ItemData(sm64ex_base_id + 477),
    "Castle - Side Flip": SM64ItemData(sm64ex_base_id + 478),
    "Castle - Wall Kick": SM64ItemData(sm64ex_base_id + 479),
    "Castle - Dive": SM64ItemData(sm64ex_base_id + 480),
    "Castle - Ground Pound": SM64ItemData(sm64ex_base_id + 481),
    "Castle - Kick": SM64ItemData(sm64ex_base_id + 482, Filler),
    "Castle - Climb": SM64ItemData(sm64ex_base_id + 483),
    "Castle - Ledge Grab": SM64ItemData(sm64ex_base_id + 484),
}

cannon_item_data_table: dict[str, SM64ItemData] = {
    "Bob-omb Battlefield - Cannon Unlock": SM64ItemData(sm64ex_base_id + 200),
    "Whomp's Fortress - Cannon Unlock": SM64ItemData(sm64ex_base_id + 201),
    "Jolly Roger Bay - Cannon Unlock": SM64ItemData(sm64ex_base_id + 202),
    "Cool, Cool Mountain - Cannon Unlock": SM64ItemData(sm64ex_base_id + 203),
    "Shifting Sand Land - Cannon Unlock": SM64ItemData(sm64ex_base_id + 207),
    "Snowman's Land - Cannon Unlock": SM64ItemData(sm64ex_base_id + 209),
    "Wet-Dry World - Cannon Unlock": SM64ItemData(sm64ex_base_id + 210),
    "Tall, Tall Mountain - Cannon Unlock": SM64ItemData(sm64ex_base_id + 211),
    "Tiny-Huge Island - Cannon Unlock": SM64ItemData(sm64ex_base_id + 212),
    "Rainbow Ride - Cannon Unlock": SM64ItemData(sm64ex_base_id + 214),
    "Wing Mario Over the Rainbow - Cannon Unlock": SM64ItemData(sm64ex_base_id + 525),

}

painting_unlock_item_data_table: dict[str, SM64ItemData] = {
    "Unlock Whomp's Fortress": SM64ItemData(sm64ex_base_id + 231),
    "Unlock Jolly Roger Bay": SM64ItemData(sm64ex_base_id + 232),
    "Unlock Cool, Cool Mountain": SM64ItemData(sm64ex_base_id + 233),
    "Unlock Hazy Maze Cave": SM64ItemData(sm64ex_base_id + 235),
    "Unlock Lethal Lava Land": SM64ItemData(sm64ex_base_id + 236),
    "Unlock Shifting Sand Land": SM64ItemData(sm64ex_base_id + 237),
    "Unlock Dire, Dire Docks": SM64ItemData(sm64ex_base_id + 238),
    "Unlock Snowman's Land": SM64ItemData(sm64ex_base_id + 239),
    "Unlock Wet-Dry World": SM64ItemData(sm64ex_base_id + 240),
    "Unlock Tall, Tall Mountain": SM64ItemData(sm64ex_base_id + 241),
    "Unlock Tiny Island": SM64ItemData(sm64ex_base_id + 242),
    "Unlock Tick Tock Clock": SM64ItemData(sm64ex_base_id + 243),
    "Unlock Huge Island": SM64ItemData(sm64ex_base_id + 559),
}

item_data_table = {
    **generic_item_data_table,
    **feature_item_data_table,
    **castle_key_item_data_table,
    **castle_progression_item_data_table,
    **cap_item_data_table,
    **arbitrary_item_data_table,
    **optional_item_data_table,
    **bowser_stage_1up_item_data_table,
    **action_item_data_table,
    **per_level_action_item_data_table,
    **cannon_item_data_table,
    **painting_unlock_item_data_table
}

item_table = {name: data.code for name, data in item_data_table.items() if data.code is not None}
