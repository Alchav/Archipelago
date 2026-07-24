from typing import NamedTuple, Callable

from BaseClasses import Item, ItemClassification

sm64ex_base_id: int = 3626000
ut_glitch_item_name = "ut_glitch"


def progression(options):
    return ItemClassification.progression


def progression_deprioritized(options):
    return ItemClassification.progression_deprioritized


def progression_skip_balancing(options):
    return ItemClassification.progression_skip_balancing


def progression_deprioritized_skip_balancing(options):
    return ItemClassification.progression_deprioritized_skip_balancing


def useful(options):
    return ItemClassification.useful


def filler(options):
    return ItemClassification.filler


def progression_deprioritized_skip_balancing_if_blocksanity(options):
    if options.blocksanity:
        return ItemClassification.progression_deprioritized_skip_balancing
    return ItemClassification.filler
    
def trap(options):
    return ItemClassification.trap


class SM64Item(Item):
    game: str = "SM64: Spicy Mycena 64"


class SM64ItemData(NamedTuple):
    code: int | None = None
    classification: Callable = progression

generic_item_data_table: dict[str, SM64ItemData] = {
    "Basement Key": SM64ItemData(sm64ex_base_id + 178),
    "Second Floor Key": SM64ItemData(sm64ex_base_id + 179),
    "Progressive Key": SM64ItemData(sm64ex_base_id + 180),
    "Wing Cap": SM64ItemData(sm64ex_base_id + 181),
    "Metal Cap": SM64ItemData(sm64ex_base_id + 182),
    "Vanish Cap": SM64ItemData(sm64ex_base_id + 183),
    "1-Up Mushroom": SM64ItemData(sm64ex_base_id + 184, filler),
    ut_glitch_item_name: SM64ItemData(),
}

global_cap_item_names = ("Wing Cap", "Metal Cap", "Vanish Cap")

feature_item_data_table: dict[str, SM64ItemData] = {
    "Bob-omb Battlefield - King Bob-omb": SM64ItemData(sm64ex_base_id + 245, progression_deprioritized),
    "Bob-omb Battlefield - Koopa the Quick": SM64ItemData(sm64ex_base_id + 246, progression_deprioritized),
    "Bob-omb Battlefield - Bob-omb Buddy": SM64ItemData(sm64ex_base_id + 247, progression_deprioritized),
    "Whomp's Fortress - Whomp King": SM64ItemData(sm64ex_base_id + 248, progression_deprioritized),
    "Whomp's Fortress - Fortress": SM64ItemData(sm64ex_base_id + 249),
    "Whomp's Fortress - Bob-omb Buddy": SM64ItemData(sm64ex_base_id + 250, progression_deprioritized),
    "Whomp's Fortress - Hoot": SM64ItemData(sm64ex_base_id + 251),
    "Cool, Cool Mountain - Snowman's Head": SM64ItemData(sm64ex_base_id + 252, progression_deprioritized),
    "Cool, Cool Mountain - Big Penguin": SM64ItemData(sm64ex_base_id + 253, progression_deprioritized),
    "Jolly Roger Bay - Sunken Ship": SM64ItemData(sm64ex_base_id + 254, progression_deprioritized),
    "Jolly Roger Bay - Raised Ship": SM64ItemData(sm64ex_base_id + 255, progression_deprioritized),
    "Jolly Roger Bay - Bob-omb Buddy": SM64ItemData(sm64ex_base_id + 256, progression_deprioritized),
    "Jolly Roger Bay - Jet Stream": SM64ItemData(sm64ex_base_id + 257, progression_deprioritized),
    "Jolly Roger Bay - Unagi": SM64ItemData(sm64ex_base_id + 258, progression_deprioritized),
    "Lethal Lava Land - Koopa Shell": SM64ItemData(sm64ex_base_id + 259, progression_deprioritized_skip_balancing),
    "Shifting Sand Land - Klepto Star": SM64ItemData(sm64ex_base_id + 260, progression_deprioritized),
    "Tiny-Huge Island - Koopa the Quick": SM64ItemData(sm64ex_base_id + 261, progression_deprioritized),
    "Tall, Tall Mountain - Ukiki": SM64ItemData(sm64ex_base_id + 262, progression_deprioritized),
    "Dire, Dire Docks - Manta Ray": SM64ItemData(sm64ex_base_id + 263, progression_deprioritized),
    "Dire, Dire Docks - Bowser's Sub": SM64ItemData(sm64ex_base_id + 264, progression_deprioritized),
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
    "Castle - Progressive MIPS": SM64ItemData(sm64ex_base_id + 271, progression_deprioritized),
    "Unlock Tower of the Wing Cap": SM64ItemData(sm64ex_base_id + 272),
    "Unlock Big Boo's Haunt": SM64ItemData(sm64ex_base_id + 273),
    "Castle - Toads": SM64ItemData(sm64ex_base_id + 274),
    "Castle - Cannon Unlock": SM64ItemData(sm64ex_base_id + 275, progression_deprioritized_skip_balancing),
    "Castle - Yoshi": SM64ItemData(sm64ex_base_id + 276, progression_deprioritized_skip_balancing),
    "Unlock Bowser in the Fire Sea": SM64ItemData(sm64ex_base_id + 304),
    "Unlock Vanish Cap Under the Moat": SM64ItemData(sm64ex_base_id + 555),
}

cap_item_data_table: dict[str, SM64ItemData] = {
    "Bob-omb Battlefield - Wing Cap": SM64ItemData(sm64ex_base_id + 277),
    "Castle - Wing Cap": SM64ItemData(
        sm64ex_base_id + 278, progression_deprioritized_skip_balancing_if_blocksanity),
    "Lethal Lava Land - Wing Cap": SM64ItemData(sm64ex_base_id + 279, progression_deprioritized_skip_balancing),
    "Shifting Sand Land - Wing Cap": SM64ItemData(sm64ex_base_id + 280, progression_deprioritized),
    "Tower of the Wing Cap - Wing Cap": SM64ItemData(
        sm64ex_base_id + 281, progression_deprioritized_skip_balancing_if_blocksanity),
    "Wing Mario Over the Rainbow - Wing Cap": SM64ItemData(sm64ex_base_id + 282),
    "Whomp's Fortress - Metal Cap": SM64ItemData(
        sm64ex_base_id + 283, progression_deprioritized_skip_balancing_if_blocksanity),
    "Jolly Roger Bay - Metal Cap": SM64ItemData(sm64ex_base_id + 284, progression_deprioritized),
    "Hazy Maze Cave - Metal Cap": SM64ItemData(sm64ex_base_id + 285, progression_deprioritized),
    "Dire, Dire Docks - Metal Cap": SM64ItemData(sm64ex_base_id + 286, progression_deprioritized),
    "Wet-Dry World - Metal Cap": SM64ItemData(
        sm64ex_base_id + 287, progression_deprioritized_skip_balancing_if_blocksanity),
    "Cavern of the Metal Cap - Metal Cap": SM64ItemData(sm64ex_base_id + 288, progression_deprioritized),
    "Bowser in the Dark World - Metal Cap": SM64ItemData(
        sm64ex_base_id + 289, progression_deprioritized_skip_balancing_if_blocksanity),
    "Big Boo's Haunt - Vanish Cap": SM64ItemData(sm64ex_base_id + 290, progression_deprioritized),
    "Dire, Dire Docks - Vanish Cap": SM64ItemData(sm64ex_base_id + 291, progression_deprioritized),
    "Snowman's Land - Vanish Cap": SM64ItemData(sm64ex_base_id + 292, progression_deprioritized),
    "Vanish Cap Under the Moat - Vanish Cap": SM64ItemData(sm64ex_base_id + 293, progression_deprioritized),
    "Wet-Dry World - Vanish Cap": SM64ItemData(sm64ex_base_id + 294, progression_deprioritized_skip_balancing),
}

simple_arbitrary_item_data_table: dict[str, SM64ItemData] = {
    "Hazy Maze Cave - Swimming Beast": SM64ItemData(sm64ex_base_id + 295),
    "Rainbow Ride - Carpets": SM64ItemData(sm64ex_base_id + 296),
    "Tiny-Huge Island - Warp Pipes": SM64ItemData(sm64ex_base_id + 298),
    "Cool, Cool Mountain - Baby Penguins": SM64ItemData(sm64ex_base_id + 299, progression_deprioritized_skip_balancing),
    "Snowman's Land - Penguin": SM64ItemData(sm64ex_base_id + 300),
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
    "Bob-omb Battlefield - Checkerboard Platform": SM64ItemData(sm64ex_base_id + 306, filler),
    "Whomp's Fortress - Checkerboard Platform": SM64ItemData(sm64ex_base_id + 307),
    "Lethal Lava Land - Checkerboard Platforms": SM64ItemData(sm64ex_base_id + 308, progression_deprioritized_skip_balancing),
    "Hazy Maze Cave - Checkerboard Platform": SM64ItemData(sm64ex_base_id + 309),
    "Vanish Cap Under the Moat - Checkerboard Platforms": SM64ItemData(sm64ex_base_id + 310),
}

rolling_log_item_data_table: dict[str, SM64ItemData] = {
    "Lethal Lava Land - Rolling Log": SM64ItemData(sm64ex_base_id + 311, progression_deprioritized_skip_balancing),
    "Tall, Tall Mountain - Rolling Log": SM64ItemData(sm64ex_base_id + 312, progression),
}

purple_switch_item_data_table: dict[str, SM64ItemData] = {
    "Bob-omb Battlefield - Purple Switch": SM64ItemData(sm64ex_base_id + 313, filler),
    "Hazy Maze Cave - Purple Switch": SM64ItemData(sm64ex_base_id + 314, progression_deprioritized_skip_balancing),
    "Wet-Dry World - Purple Switch": SM64ItemData(sm64ex_base_id + 315),
    "Rainbow Ride - Purple Switch": SM64ItemData(sm64ex_base_id + 316, progression_deprioritized_skip_balancing),
    "Bowser in the Dark World - Purple Switch": SM64ItemData(sm64ex_base_id + 317),
    "Bowser in the Sky - Purple Switch": SM64ItemData(sm64ex_base_id + 318, progression_skip_balancing),
    "Jolly Roger Bay - Purple Switch": SM64ItemData(sm64ex_base_id + 321, progression_deprioritized_skip_balancing),
    "Dire, Dire Docks - Purple Switch": SM64ItemData(sm64ex_base_id + 322, progression_deprioritized_skip_balancing),
    "Tall, Tall Mountain - Purple Switch": SM64ItemData(sm64ex_base_id + 323, progression_deprioritized_skip_balancing),
    "Tiny-Huge Island - Purple Switch": SM64ItemData(sm64ex_base_id + 324, progression_deprioritized_skip_balancing),
}

optional_item_data_table: dict[str, SM64ItemData] = {
    "Mario's Hat": SM64ItemData(sm64ex_base_id + 320, useful),
}

bowser_stage_1up_item_data_table: dict[str, SM64ItemData] = {
    "Bowser Stage Extra 1-Ups": SM64ItemData(sm64ex_base_id + 556, progression_deprioritized),
    "Bowser in the Dark World - Extra 1-Ups": SM64ItemData(sm64ex_base_id + 557, progression_deprioritized),
    "Bowser in the Fire Sea - Extra 1-Ups": SM64ItemData(sm64ex_base_id + 558, progression_deprioritized),
}

trap_item_data_table: dict[str, SM64ItemData] = {
    "Bonk Trap": SM64ItemData(sm64ex_base_id + 1760, trap),
    "Burn Trap": SM64ItemData(sm64ex_base_id + 1761, trap),
    "Shock Trap": SM64ItemData(sm64ex_base_id + 1762, trap),
    "Chuckya Trap": SM64ItemData(sm64ex_base_id + 1763, trap),
    "Spin Trap": SM64ItemData(sm64ex_base_id + 1764, trap),
    "Gust Trap": SM64ItemData(sm64ex_base_id + 1765, trap),
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
    "Bob-omb Battlefield - Backflip": SM64ItemData(sm64ex_base_id + 327, progression_deprioritized_skip_balancing),
    "Bob-omb Battlefield - Side Flip": SM64ItemData(sm64ex_base_id + 328, progression_deprioritized_skip_balancing),
    "Bob-omb Battlefield - Wall Kick": SM64ItemData(sm64ex_base_id + 329, useful),
    "Bob-omb Battlefield - Dive": SM64ItemData(sm64ex_base_id + 330, useful),
    "Bob-omb Battlefield - Ground Pound": SM64ItemData(sm64ex_base_id + 331, progression_deprioritized_skip_balancing),
    "Bob-omb Battlefield - Kick": SM64ItemData(sm64ex_base_id + 332, useful),
    "Bob-omb Battlefield - Climb": SM64ItemData(sm64ex_base_id + 333, progression_deprioritized_skip_balancing),
    "Bob-omb Battlefield - Ledge Grab": SM64ItemData(sm64ex_base_id + 334, useful),
    # Whomp's Fortress
    "Whomp's Fortress - Triple Jump": SM64ItemData(sm64ex_base_id + 335),
    "Whomp's Fortress - Long Jump": SM64ItemData(sm64ex_base_id + 336, progression_deprioritized_skip_balancing),
    "Whomp's Fortress - Backflip": SM64ItemData(sm64ex_base_id + 337, useful),
    "Whomp's Fortress - Side Flip": SM64ItemData(sm64ex_base_id + 338),
    "Whomp's Fortress - Wall Kick": SM64ItemData(sm64ex_base_id + 339),
    "Whomp's Fortress - Dive": SM64ItemData(sm64ex_base_id + 340, useful),
    "Whomp's Fortress - Ground Pound": SM64ItemData(sm64ex_base_id + 341),
    "Whomp's Fortress - Kick": SM64ItemData(sm64ex_base_id + 342, useful),
    "Whomp's Fortress - Climb": SM64ItemData(sm64ex_base_id + 343, progression_deprioritized_skip_balancing),
    "Whomp's Fortress - Ledge Grab": SM64ItemData(sm64ex_base_id + 344, progression_deprioritized_skip_balancing),
    # Jolly Roger Bay
    "Jolly Roger Bay - Triple Jump": SM64ItemData(sm64ex_base_id + 345),
    "Jolly Roger Bay - Long Jump": SM64ItemData(sm64ex_base_id + 346, progression_deprioritized_skip_balancing),
    "Jolly Roger Bay - Backflip": SM64ItemData(sm64ex_base_id + 347),
    "Jolly Roger Bay - Side Flip": SM64ItemData(sm64ex_base_id + 348),
    "Jolly Roger Bay - Wall Kick": SM64ItemData(sm64ex_base_id + 349),
    "Jolly Roger Bay - Dive": SM64ItemData(sm64ex_base_id + 350, useful),
    "Jolly Roger Bay - Ground Pound": SM64ItemData(sm64ex_base_id + 351, progression_deprioritized_skip_balancing),
    "Jolly Roger Bay - Kick": SM64ItemData(sm64ex_base_id + 352, useful),
    "Jolly Roger Bay - Climb": SM64ItemData(sm64ex_base_id + 353),
    "Jolly Roger Bay - Ledge Grab": SM64ItemData(sm64ex_base_id + 354),
    # Cool, Cool Mountain
    "Cool, Cool Mountain - Triple Jump": SM64ItemData(sm64ex_base_id + 355, progression_deprioritized_skip_balancing),
    "Cool, Cool Mountain - Long Jump": SM64ItemData(sm64ex_base_id + 356, useful),
    "Cool, Cool Mountain - Backflip": SM64ItemData(sm64ex_base_id + 357, useful),
    "Cool, Cool Mountain - Side Flip": SM64ItemData(sm64ex_base_id + 358, useful),
    "Cool, Cool Mountain - Wall Kick": SM64ItemData(sm64ex_base_id + 359, progression_deprioritized_skip_balancing),
    "Cool, Cool Mountain - Dive": SM64ItemData(sm64ex_base_id + 360, useful),
    "Cool, Cool Mountain - Ground Pound": SM64ItemData(sm64ex_base_id + 361, progression_deprioritized_skip_balancing),
    "Cool, Cool Mountain - Kick": SM64ItemData(sm64ex_base_id + 362, useful),
    "Cool, Cool Mountain - Climb": SM64ItemData(sm64ex_base_id + 363, useful),
    "Cool, Cool Mountain - Ledge Grab": SM64ItemData(sm64ex_base_id + 364, useful),
    # Big Boo's Haunt
    "Big Boo's Haunt - Triple Jump": SM64ItemData(sm64ex_base_id + 365),
    "Big Boo's Haunt - Long Jump": SM64ItemData(sm64ex_base_id + 366),
    "Big Boo's Haunt - Backflip": SM64ItemData(sm64ex_base_id + 367, progression_deprioritized_skip_balancing),
    "Big Boo's Haunt - Side Flip": SM64ItemData(sm64ex_base_id + 368),
    "Big Boo's Haunt - Wall Kick": SM64ItemData(sm64ex_base_id + 369),
    "Big Boo's Haunt - Dive": SM64ItemData(sm64ex_base_id + 370, useful),
    "Big Boo's Haunt - Ground Pound": SM64ItemData(sm64ex_base_id + 371, progression_deprioritized_skip_balancing),
    "Big Boo's Haunt - Kick": SM64ItemData(sm64ex_base_id + 372, progression_deprioritized_skip_balancing),
    "Big Boo's Haunt - Climb": SM64ItemData(sm64ex_base_id + 373, useful),
    "Big Boo's Haunt - Ledge Grab": SM64ItemData(sm64ex_base_id + 374),
    # Hazy Maze Cave
    "Hazy Maze Cave - Triple Jump": SM64ItemData(sm64ex_base_id + 375),
    "Hazy Maze Cave - Long Jump": SM64ItemData(sm64ex_base_id + 376),
    "Hazy Maze Cave - Backflip": SM64ItemData(sm64ex_base_id + 377),
    "Hazy Maze Cave - Side Flip": SM64ItemData(sm64ex_base_id + 378),
    "Hazy Maze Cave - Wall Kick": SM64ItemData(sm64ex_base_id + 379),
    "Hazy Maze Cave - Dive": SM64ItemData(sm64ex_base_id + 380, useful),
    "Hazy Maze Cave - Ground Pound": SM64ItemData(sm64ex_base_id + 381, progression_deprioritized_skip_balancing),
    "Hazy Maze Cave - Kick": SM64ItemData(sm64ex_base_id + 382, useful),
    "Hazy Maze Cave - Climb": SM64ItemData(sm64ex_base_id + 383),
    "Hazy Maze Cave - Ledge Grab": SM64ItemData(sm64ex_base_id + 384),
    # Lethal Lava Land
    "Lethal Lava Land - Triple Jump": SM64ItemData(sm64ex_base_id + 385),
    "Lethal Lava Land - Long Jump": SM64ItemData(sm64ex_base_id + 386),
    "Lethal Lava Land - Backflip": SM64ItemData(sm64ex_base_id + 387, useful),
    "Lethal Lava Land - Side Flip": SM64ItemData(sm64ex_base_id + 388, useful),
    "Lethal Lava Land - Wall Kick": SM64ItemData(sm64ex_base_id + 389, useful),
    "Lethal Lava Land - Dive": SM64ItemData(sm64ex_base_id + 390),
    "Lethal Lava Land - Ground Pound": SM64ItemData(sm64ex_base_id + 391, useful),
    "Lethal Lava Land - Kick": SM64ItemData(sm64ex_base_id + 392, useful),
    "Lethal Lava Land - Climb": SM64ItemData(sm64ex_base_id + 393),
    "Lethal Lava Land - Ledge Grab": SM64ItemData(sm64ex_base_id + 394, useful),
    # Shifting Sand Land
    "Shifting Sand Land - Triple Jump": SM64ItemData(sm64ex_base_id + 395),
    "Shifting Sand Land - Long Jump": SM64ItemData(sm64ex_base_id + 396, progression_deprioritized_skip_balancing),
    "Shifting Sand Land - Backflip": SM64ItemData(sm64ex_base_id + 397),
    "Shifting Sand Land - Side Flip": SM64ItemData(sm64ex_base_id + 398),
    "Shifting Sand Land - Wall Kick": SM64ItemData(sm64ex_base_id + 399, useful),
    "Shifting Sand Land - Dive": SM64ItemData(sm64ex_base_id + 400, useful),
    "Shifting Sand Land - Ground Pound": SM64ItemData(sm64ex_base_id + 401),
    "Shifting Sand Land - Kick": SM64ItemData(sm64ex_base_id + 402, progression_deprioritized_skip_balancing),
    "Shifting Sand Land - Climb": SM64ItemData(sm64ex_base_id + 403),
    "Shifting Sand Land - Ledge Grab": SM64ItemData(sm64ex_base_id + 404),
    # Dire, Dire Docks
    "Dire, Dire Docks - Triple Jump": SM64ItemData(sm64ex_base_id + 405, progression_deprioritized_skip_balancing),
    "Dire, Dire Docks - Long Jump": SM64ItemData(sm64ex_base_id + 406, useful),
    "Dire, Dire Docks - Backflip": SM64ItemData(sm64ex_base_id + 407, useful),
    "Dire, Dire Docks - Side Flip": SM64ItemData(sm64ex_base_id + 408, useful),
    "Dire, Dire Docks - Wall Kick": SM64ItemData(sm64ex_base_id + 409, filler),
    "Dire, Dire Docks - Dive": SM64ItemData(sm64ex_base_id + 410, filler),
    "Dire, Dire Docks - Ground Pound": SM64ItemData(sm64ex_base_id + 411, progression_deprioritized_skip_balancing),
    "Dire, Dire Docks - Kick": SM64ItemData(sm64ex_base_id + 412, useful),
    "Dire, Dire Docks - Climb": SM64ItemData(sm64ex_base_id + 413, progression_deprioritized_skip_balancing),
    "Dire, Dire Docks - Ledge Grab": SM64ItemData(sm64ex_base_id + 414, filler),
    # Snowman's Land
    "Snowman's Land - Triple Jump": SM64ItemData(sm64ex_base_id + 415),
    "Snowman's Land - Long Jump": SM64ItemData(sm64ex_base_id + 416, useful),
    "Snowman's Land - Backflip": SM64ItemData(sm64ex_base_id + 417),
    "Snowman's Land - Side Flip": SM64ItemData(sm64ex_base_id + 418),
    "Snowman's Land - Wall Kick": SM64ItemData(sm64ex_base_id + 419),
    "Snowman's Land - Dive": SM64ItemData(sm64ex_base_id + 420, useful),
    "Snowman's Land - Ground Pound": SM64ItemData(sm64ex_base_id + 421, useful),
    "Snowman's Land - Kick": SM64ItemData(sm64ex_base_id + 422, useful),
    "Snowman's Land - Climb": SM64ItemData(sm64ex_base_id + 423, progression_deprioritized_skip_balancing),
    "Snowman's Land - Ledge Grab": SM64ItemData(sm64ex_base_id + 424),
    # Wet-Dry World
    "Wet-Dry World - Triple Jump": SM64ItemData(sm64ex_base_id + 425),
    "Wet-Dry World - Long Jump": SM64ItemData(sm64ex_base_id + 426),
    "Wet-Dry World - Backflip": SM64ItemData(sm64ex_base_id + 427),
    "Wet-Dry World - Side Flip": SM64ItemData(sm64ex_base_id + 428),
    "Wet-Dry World - Wall Kick": SM64ItemData(sm64ex_base_id + 429),
    "Wet-Dry World - Dive": SM64ItemData(sm64ex_base_id + 430),
    "Wet-Dry World - Ground Pound": SM64ItemData(sm64ex_base_id + 431, progression_deprioritized_skip_balancing),
    "Wet-Dry World - Kick": SM64ItemData(sm64ex_base_id + 432, progression_deprioritized_skip_balancing),
    "Wet-Dry World - Climb": SM64ItemData(sm64ex_base_id + 433, useful),
    "Wet-Dry World - Ledge Grab": SM64ItemData(sm64ex_base_id + 434),
    # Tall, Tall Mountain
    "Tall, Tall Mountain - Triple Jump": SM64ItemData(sm64ex_base_id + 435),
    "Tall, Tall Mountain - Long Jump": SM64ItemData(sm64ex_base_id + 436),
    "Tall, Tall Mountain - Backflip": SM64ItemData(sm64ex_base_id + 437, progression_deprioritized_skip_balancing),
    "Tall, Tall Mountain - Side Flip": SM64ItemData(sm64ex_base_id + 438),
    "Tall, Tall Mountain - Wall Kick": SM64ItemData(sm64ex_base_id + 439),
    "Tall, Tall Mountain - Dive": SM64ItemData(sm64ex_base_id + 440),
    "Tall, Tall Mountain - Ground Pound": SM64ItemData(sm64ex_base_id + 441, useful),
    "Tall, Tall Mountain - Kick": SM64ItemData(sm64ex_base_id + 442),
    "Tall, Tall Mountain - Climb": SM64ItemData(sm64ex_base_id + 443, progression_deprioritized_skip_balancing),
    "Tall, Tall Mountain - Ledge Grab": SM64ItemData(sm64ex_base_id + 444),
    # Tiny-Huge Island
    "Tiny-Huge Island - Triple Jump": SM64ItemData(sm64ex_base_id + 445),
    "Tiny-Huge Island - Long Jump": SM64ItemData(sm64ex_base_id + 446),
    "Tiny-Huge Island - Backflip": SM64ItemData(sm64ex_base_id + 447, filler),
    "Tiny-Huge Island - Side Flip": SM64ItemData(sm64ex_base_id + 448),
    "Tiny-Huge Island - Wall Kick": SM64ItemData(sm64ex_base_id + 449),
    "Tiny-Huge Island - Dive": SM64ItemData(sm64ex_base_id + 450),
    "Tiny-Huge Island - Ground Pound": SM64ItemData(sm64ex_base_id + 451),
    "Tiny-Huge Island - Kick": SM64ItemData(sm64ex_base_id + 452, filler),
    "Tiny-Huge Island - Climb": SM64ItemData(sm64ex_base_id + 453, useful),
    "Tiny-Huge Island - Ledge Grab": SM64ItemData(sm64ex_base_id + 454),
    # Tick Tock Clock
    "Tick Tock Clock - Triple Jump": SM64ItemData(sm64ex_base_id + 455),
    "Tick Tock Clock - Long Jump": SM64ItemData(sm64ex_base_id + 456, progression_deprioritized_skip_balancing),
    "Tick Tock Clock - Backflip": SM64ItemData(sm64ex_base_id + 457),
    "Tick Tock Clock - Side Flip": SM64ItemData(sm64ex_base_id + 458),
    "Tick Tock Clock - Wall Kick": SM64ItemData(sm64ex_base_id + 459),
    "Tick Tock Clock - Dive": SM64ItemData(sm64ex_base_id + 460, useful),
    "Tick Tock Clock - Ground Pound": SM64ItemData(sm64ex_base_id + 461, progression_deprioritized_skip_balancing),
    "Tick Tock Clock - Kick": SM64ItemData(sm64ex_base_id + 462, useful),
    "Tick Tock Clock - Climb": SM64ItemData(sm64ex_base_id + 463),
    "Tick Tock Clock - Ledge Grab": SM64ItemData(sm64ex_base_id + 464),
    # Rainbow Ride
    "Rainbow Ride - Triple Jump": SM64ItemData(sm64ex_base_id + 465),
    "Rainbow Ride - Long Jump": SM64ItemData(sm64ex_base_id + 466),
    "Rainbow Ride - Backflip": SM64ItemData(sm64ex_base_id + 467),
    "Rainbow Ride - Side Flip": SM64ItemData(sm64ex_base_id + 468),
    "Rainbow Ride - Wall Kick": SM64ItemData(sm64ex_base_id + 469),
    "Rainbow Ride - Dive": SM64ItemData(sm64ex_base_id + 470),
    "Rainbow Ride - Ground Pound": SM64ItemData(sm64ex_base_id + 471, progression_deprioritized_skip_balancing),
    "Rainbow Ride - Kick": SM64ItemData(sm64ex_base_id + 472, useful),
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
    "Castle - Kick": SM64ItemData(sm64ex_base_id + 482, filler),
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

global_coin_object_item_data_table: dict[str, SM64ItemData] = {
    "Single Yellow Coins": SM64ItemData(3626560, progression),
    "Red Coins": SM64ItemData(3626561, progression),
    "Single Blue Coins": SM64ItemData(3626562, progression),
    "Blue Coin Blocks": SM64ItemData(3626563, progression),
    "Horizontal Coin Lines": SM64ItemData(3626564, progression),
    "Horizontal Coin Rings": SM64ItemData(3626565, progression),
    "Coin Arrows": SM64ItemData(3626566, progression),
    "Vertical Coin Lines": SM64ItemData(3626568, progression),
    "Vertical Coin Rings": SM64ItemData(3626570, progression),
    "Breakable Coin Boxes": SM64ItemData(3626782, progression),
    "Throwable Cork Boxes": SM64ItemData(3626783, progression),
    "Crazy Boxes": SM64ItemData(3626784, progression),
    "Wooden Posts": SM64ItemData(3626785, progression),
    "Three-Coin Blocks": SM64ItemData(3626816, progression),
    "Ten-Coin Blocks": SM64ItemData(3626817, progression),
}


per_level_coin_object_item_data_table: dict[str, SM64ItemData] = {
    "Bowser in the Dark World - Single Yellow Coins": SM64ItemData(3626600, progression),
    "Bowser in the Fire Sea - Single Yellow Coins": SM64ItemData(3626601, progression),
    "Bowser in the Sky - Single Yellow Coins": SM64ItemData(3626602, progression),
    "Bob-omb Battlefield - Single Yellow Coins": SM64ItemData(3626603, progression),
    "Castle Grounds - Single Yellow Coins": SM64ItemData(3626604, useful),
    "Castle - Single Yellow Coins": SM64ItemData(3626605, useful),
    "Cool, Cool Mountain - Single Yellow Coins": SM64ItemData(3626606, progression),
    "Dire, Dire Docks - Single Yellow Coins": SM64ItemData(3626607, progression),
    "Hazy Maze Cave - Single Yellow Coins": SM64ItemData(3626608, progression),
    "Lethal Lava Land - Single Yellow Coins": SM64ItemData(3626609, progression),
    "Princess's Secret Slide - Single Yellow Coins": SM64ItemData(3626610, progression),
    "Rainbow Ride - Single Yellow Coins": SM64ItemData(3626611, useful),
    "Snowman's Land - Single Yellow Coins": SM64ItemData(3626612, progression),
    "Shifting Sand Land - Single Yellow Coins": SM64ItemData(3626613, progression),
    "Tiny-Huge Island - Single Yellow Coins": SM64ItemData(3626614, useful),
    "Tower of the Wing Cap - Single Yellow Coins": SM64ItemData(3626615, progression),
    "Tick Tock Clock - Single Yellow Coins": SM64ItemData(3626616, useful),
    "Tall, Tall Mountain - Single Yellow Coins": SM64ItemData(3626617, progression),
    "Vanish Cap Under the Moat - Single Yellow Coins": SM64ItemData(3626618, progression),
    "Whomp's Fortress - Single Yellow Coins": SM64ItemData(3626619, progression),
    "Big Boo's Haunt - Red Coins": SM64ItemData(3626620, progression),
    "Bowser in the Dark World - Red Coins": SM64ItemData(3626621, progression),
    "Bowser in the Fire Sea - Red Coins": SM64ItemData(3626622, progression),
    "Bowser in the Sky - Red Coins": SM64ItemData(3626623, progression),
    "Bob-omb Battlefield - Red Coins": SM64ItemData(3626624, progression),
    "Cool, Cool Mountain - Red Coins": SM64ItemData(3626625, progression),
    "Cavern of the Metal Cap - Red Coins": SM64ItemData(3626626, progression),
    "Dire, Dire Docks - Red Coins": SM64ItemData(3626627, progression),
    "Hazy Maze Cave - Red Coins": SM64ItemData(3626628, progression),
    "Jolly Roger Bay - Red Coins": SM64ItemData(3626629, progression),
    "Lethal Lava Land - Red Coins": SM64ItemData(3626630, progression),
    "Rainbow Ride - Red Coins": SM64ItemData(3626631, useful),
    "Secret Aquarium - Red Coins": SM64ItemData(3626632, progression),
    "Snowman's Land - Red Coins": SM64ItemData(3626633, progression),
    "Shifting Sand Land - Red Coins": SM64ItemData(3626634, progression),
    "Tiny-Huge Island - Red Coins": SM64ItemData(3626635, useful),
    "Tower of the Wing Cap - Red Coins": SM64ItemData(3626636, progression),
    "Tick Tock Clock - Red Coins": SM64ItemData(3626637, useful),
    "Tall, Tall Mountain - Red Coins": SM64ItemData(3626638, progression),
    "Vanish Cap Under the Moat - Red Coins": SM64ItemData(3626639, progression),
    "Wet-Dry World - Red Coins": SM64ItemData(3626640, progression),
    "Whomp's Fortress - Red Coins": SM64ItemData(3626641, progression),
    "Wing Mario Over the Rainbow - Red Coins": SM64ItemData(3626642, progression),
    "Cool, Cool Mountain - Single Blue Coin": SM64ItemData(3626643, progression_deprioritized_skip_balancing),
    "Tall, Tall Mountain - Single Blue Coins": SM64ItemData(3626644, progression),
    "Big Boo's Haunt - Blue Coin Block": SM64ItemData(3626645, progression),
    "Cool, Cool Mountain - Blue Coin Block": SM64ItemData(3626646, progression),
    "Dire, Dire Docks - Blue Coin Block": SM64ItemData(3626647, progression),
    "Hazy Maze Cave - Blue Coin Block": SM64ItemData(3626648, progression),
    "Jolly Roger Bay - Blue Coin Block": SM64ItemData(3626649, progression),
    "Princess's Secret Slide - Blue Coin Block": SM64ItemData(3626650, progression),
    "Rainbow Ride - Blue Coin Block": SM64ItemData(3626651, useful),
    "Shifting Sand Land - Blue Coin Block": SM64ItemData(3626652, progression),
    "Tiny-Huge Island - Blue Coin Block": SM64ItemData(3626653, useful),
    "Tick Tock Clock - Blue Coin Block": SM64ItemData(3626654, useful),
    "Wet-Dry World - Blue Coin Block": SM64ItemData(3626655, progression),
    "Whomp's Fortress - Blue Coin Block": SM64ItemData(3626656, progression),
    "Bowser in the Dark World - Horizontal Coin Lines": SM64ItemData(3626657, progression),
    "Bowser in the Fire Sea - Horizontal Coin Lines": SM64ItemData(3626658, progression),
    "Bowser in the Sky - Horizontal Coin Lines": SM64ItemData(3626659, progression),
    "Bob-omb Battlefield - Horizontal Coin Lines": SM64ItemData(3626660, progression),
    "Cool, Cool Mountain - Horizontal Coin Lines": SM64ItemData(3626661, progression),
    "Cavern of the Metal Cap - Horizontal Coin Lines": SM64ItemData(3626662, progression),
    "Dire, Dire Docks - Horizontal Coin Lines": SM64ItemData(3626663, progression),
    "Hazy Maze Cave - Horizontal Coin Lines": SM64ItemData(3626664, progression),
    "Jolly Roger Bay - Horizontal Coin Lines": SM64ItemData(3626665, progression),
    "Lethal Lava Land - Horizontal Coin Lines": SM64ItemData(3626666, progression),
    "Princess's Secret Slide - Horizontal Coin Lines": SM64ItemData(3626667, progression),
    "Rainbow Ride - Horizontal Coin Lines": SM64ItemData(3626668, useful),
    "Snowman's Land - Horizontal Coin Lines": SM64ItemData(3626669, progression),
    "Shifting Sand Land - Horizontal Coin Lines": SM64ItemData(3626670, progression),
    "Tiny-Huge Island - Horizontal Coin Lines": SM64ItemData(3626671, useful),
    "Tick Tock Clock - Horizontal Coin Lines": SM64ItemData(3626672, useful),
    "Tall, Tall Mountain - Horizontal Coin Lines": SM64ItemData(3626673, progression),
    "Vanish Cap Under the Moat - Horizontal Coin Lines": SM64ItemData(3626674, progression),
    "Wet-Dry World - Horizontal Coin Lines": SM64ItemData(3626675, progression),
    "Whomp's Fortress - Horizontal Coin Lines": SM64ItemData(3626676, progression),
    "Bowser in the Dark World - Horizontal Coin Rings": SM64ItemData(3626677, progression),
    "Bowser in the Fire Sea - Horizontal Coin Rings": SM64ItemData(3626678, progression),
    "Bob-omb Battlefield - Horizontal Coin Rings": SM64ItemData(3626679, progression),
    "Cavern of the Metal Cap - Horizontal Coin Rings": SM64ItemData(3626680, progression),
    "Dire, Dire Docks - Horizontal Coin Rings": SM64ItemData(3626681, progression),
    "Hazy Maze Cave - Horizontal Coin Rings": SM64ItemData(3626682, progression),
    "Jolly Roger Bay - Horizontal Coin Rings": SM64ItemData(3626683, progression),
    "Lethal Lava Land - Horizontal Coin Rings": SM64ItemData(3626684, progression),
    "Rainbow Ride - Horizontal Coin Rings": SM64ItemData(3626685, useful),
    "Secret Aquarium - Horizontal Coin Rings": SM64ItemData(3626686, progression),
    "Shifting Sand Land - Horizontal Coin Rings": SM64ItemData(3626687, progression),
    "Tall, Tall Mountain - Horizontal Coin Rings": SM64ItemData(3626688, progression),
    "Wet-Dry World - Horizontal Coin Rings": SM64ItemData(3626689, progression),
    "Whomp's Fortress - Horizontal Coin Rings": SM64ItemData(3626690, progression),
    "Wing Mario Over the Rainbow - Horizontal Coin Rings": SM64ItemData(3626691, progression),
    "Cool, Cool Mountain - Coin Arrows": SM64ItemData(3626692, progression),
    "Whomp's Fortress - Coin Arrows": SM64ItemData(3626693, progression),
    "Bowser in the Fire Sea - Vertical Coin Lines": SM64ItemData(3626701, progression),
    "Cool, Cool Mountain - Vertical Coin Lines": SM64ItemData(3626702, progression),
    "Dire, Dire Docks - Vertical Coin Lines": SM64ItemData(3626703, progression),
    "Jolly Roger Bay - Vertical Coin Lines": SM64ItemData(3626704, progression),
    "Rainbow Ride - Vertical Coin Lines": SM64ItemData(3626705, useful),
    "Shifting Sand Land - Vertical Coin Lines": SM64ItemData(3626706, progression),
    "Tall, Tall Mountain - Vertical Coin Lines": SM64ItemData(3626707, progression),
    "Bob-omb Battlefield - Vertical Coin Rings": SM64ItemData(3626717, progression),
    "Dire, Dire Docks - Vertical Coin Rings": SM64ItemData(3626718, progression),
    "Jolly Roger Bay - Vertical Coin Rings": SM64ItemData(3626719, progression),
    "Secret Aquarium - Vertical Coin Rings": SM64ItemData(3626720, progression),
    "Tower of the Wing Cap - Vertical Coin Rings": SM64ItemData(3626721, progression),
    "Wing Mario Over the Rainbow - Vertical Coin Rings": SM64ItemData(3626722, progression),
    "Big Boo's Haunt - Breakable Coin Boxes": SM64ItemData(3626796, progression),
    "Bob-omb Battlefield - Breakable Coin Box": SM64ItemData(3626797, progression),
    "Wet-Dry World - Breakable Coin Boxes": SM64ItemData(3626798, progression),
    "Bob-omb Battlefield - Throwable Cork Boxes": SM64ItemData(3626799, progression),
    "Shifting Sand Land - Throwable Cork Box": SM64ItemData(3626800, progression),
    "Whomp's Fortress - Throwable Cork Boxes": SM64ItemData(3626801, progression),
    "Big Boo's Haunt - Crazy Box": SM64ItemData(3626802, progression),
    "Lethal Lava Land - Crazy Box": SM64ItemData(3626803, progression),
    "Shifting Sand Land - Crazy Boxes": SM64ItemData(3626804, progression),
    "Tall, Tall Mountain - Crazy Box": SM64ItemData(3626805, progression),
    "Bob-omb Battlefield - Wooden Posts": SM64ItemData(3626806, progression),
    "Tiny-Huge Island - Wooden Posts": SM64ItemData(3626807, useful),
    "Lethal Lava Land - Bowser Puzzle": SM64ItemData(3626814, progression),
    "Bowser in the Dark World - Three-Coin Block": SM64ItemData(3626826, progression),
    "Bowser in the Fire Sea - Three-Coin Block": SM64ItemData(3626827, progression),
    "Jolly Roger Bay - Three-Coin Block": SM64ItemData(3626828, progression),
    "Snowman's Land - Three-Coin Block": SM64ItemData(3626829, progression),
    "Tiny-Huge Island - Three-Coin Block": SM64ItemData(3626830, useful),
    "Tick Tock Clock - Three-Coin Blocks": SM64ItemData(3626831, useful),
    "Vanish Cap Under the Moat - Three-Coin Block": SM64ItemData(3626832, progression),
    "Wet-Dry World - Three-Coin Blocks": SM64ItemData(3626833, progression),
    "Big Boo's Haunt - Ten-Coin Block": SM64ItemData(3626834, progression),
    "Bowser in the Fire Sea - Ten-Coin Block": SM64ItemData(3626835, progression),
    "Tick Tock Clock - Ten-Coin Blocks": SM64ItemData(3626836, useful),
    "Wet-Dry World - Ten-Coin Blocks": SM64ItemData(3626837, progression),
}


global_enemy_item_data_table: dict[str, SM64ItemData] = {
    "Bob-ombs": SM64ItemData(3626571, progression),
    "Boos": SM64ItemData(3626572, progression),
    "Bullies": SM64ItemData(3626573, progression),
    "Chuckyas": SM64ItemData(3626574, progression),
    "Lakitus": SM64ItemData(3626575, useful),
    "Fire Piranha Plants": SM64ItemData(3626576, progression),
    "Fly Guys": SM64ItemData(3626577, progression),
    "Goombas": SM64ItemData(3626578, progression),
    "Koopa Troopas": SM64ItemData(3626579, progression),
    "Mr Blizzards": SM64ItemData(3626580, progression),
    "Mr. Is": SM64ItemData(3626581, progression),
    "Scuttlebugs": SM64ItemData(3626582, progression),
    "Snufits": SM64ItemData(3626583, useful),
    "Spindrifts": SM64ItemData(3626584, progression),
    "Whomps": SM64ItemData(3626585, progression),
    "Monty Moles": SM64ItemData(3626838, useful),
    "Big Bully": SM64ItemData(3626839, progression),
    "Thwomp": SM64ItemData(3626845, progression),
}


per_level_enemy_item_data_table: dict[str, SM64ItemData] = {
    "Bowser in the Fire Sea - Bob-omb": SM64ItemData(3626723, progression),
    "Bowser in the Sky - Bob-ombs": SM64ItemData(3626724, progression),
    "Bob-omb Battlefield - Bob-ombs": SM64ItemData(3626725, progression),
    "Rainbow Ride - Bob-ombs": SM64ItemData(3626726, useful),
    "Shifting Sand Land - Bob-ombs": SM64ItemData(3626727, progression),
    "Tick Tock Clock - Bob-ombs": SM64ItemData(3626728, useful),
    "Tall, Tall Mountain - Bob-ombs": SM64ItemData(3626729, progression),
    "Big Boo's Haunt - Boos": SM64ItemData(3626730, progression),
    "Bowser in the Fire Sea - Bullies": SM64ItemData(3626733, progression),
    "Lethal Lava Land - Bullies": SM64ItemData(3626734, progression),
    "Bowser in the Sky - Chuckya": SM64ItemData(3626735, progression),
    "Rainbow Ride - Chuckya": SM64ItemData(3626736, useful),
    "Tiny-Huge Island - Chuckya": SM64ItemData(3626737, useful),
    "Tall, Tall Mountain - Chuckya": SM64ItemData(3626738, progression),
    "Wet-Dry World - Chuckya": SM64ItemData(3626739, progression),
    "Rainbow Ride - Lakitus": SM64ItemData(3626740, useful),
    "Tiny-Huge Island - Lakitu": SM64ItemData(3626741, useful),
    "Shifting Sand Land - Eyerok": SM64ItemData(3626742, progression),
    "Bowser in the Sky - Fire Piranha Plants": SM64ItemData(3626743, progression),
    "Tiny-Huge Island - Fire Piranha Plants": SM64ItemData(3626744, useful),
    "Rainbow Ride - Fly Guy": SM64ItemData(3626745, useful),
    "Snowman's Land - Fly Guy": SM64ItemData(3626746, progression),
    "Shifting Sand Land - Fly Guy": SM64ItemData(3626747, progression),
    "Tiny-Huge Island - Fly Guy": SM64ItemData(3626748, useful),
    "Tall, Tall Mountain - Fly Guy": SM64ItemData(3626749, progression),
    "Big Boo's Haunt - Flying Bookends": SM64ItemData(3626750, progression),
    "Bowser in the Dark World - Goombas": SM64ItemData(3626751, progression),
    "Bowser in the Fire Sea - Goombas": SM64ItemData(3626752, progression),
    "Bowser in the Sky - Goombas": SM64ItemData(3626753, progression),
    "Bob-omb Battlefield - Goombas": SM64ItemData(3626754, progression),
    "Jolly Roger Bay - Goombas": SM64ItemData(3626755, progression),
    "Rainbow Ride - Goomba": SM64ItemData(3626756, useful),
    "Snowman's Land - Goombas": SM64ItemData(3626757, progression),
    "Shifting Sand Land - Goombas": SM64ItemData(3626758, progression),
    "Tiny-Huge Island - Goombas": SM64ItemData(3626759, useful),
    "Tall, Tall Mountain - Goombas": SM64ItemData(3626760, progression),
    "Bob-omb Battlefield - Koopa Troopa": SM64ItemData(3626761, progression),
    "Tiny-Huge Island - Koopa Troopa": SM64ItemData(3626762, useful),
    "Snowman's Land - Moneybags": SM64ItemData(3626763, progression),
    "Cool, Cool Mountain - Mr Blizzards": SM64ItemData(3626764, progression),
    "Snowman's Land - Mr Blizzards": SM64ItemData(3626765, progression),
    "Big Boo's Haunt - Mr. Is": SM64ItemData(3626766, progression),
    "Hazy Maze Cave - Mr. Is": SM64ItemData(3626767, progression),
    "Lethal Lava Land - Mr. Is": SM64ItemData(3626768, progression),
    "Whomp's Fortress - Piranha Plants": SM64ItemData(3626769, progression),
    "Shifting Sand Land - Pokeys": SM64ItemData(3626770, progression),
    "Big Boo's Haunt - Scuttlebugs": SM64ItemData(3626771, progression),
    "Hazy Maze Cave - Scuttlebugs": SM64ItemData(3626772, progression),
    "Wet-Dry World - Skeeters": SM64ItemData(3626773, progression),
    "Cavern of the Metal Cap - Snufits": SM64ItemData(3626774, progression),
    "Hazy Maze Cave - Snufits": SM64ItemData(3626775, progression),
    "Cool, Cool Mountain - Spindrifts": SM64ItemData(3626776, progression),
    "Snowman's Land - Spindrifts": SM64ItemData(3626777, progression),
    "Hazy Maze Cave - Swoops": SM64ItemData(3626778, progression),
    "Bowser in the Sky - Whomp": SM64ItemData(3626779, progression),
    "Whomp's Fortress - Whomps": SM64ItemData(3626780, progression),
    "Hazy Maze Cave - Monty Mole": SM64ItemData(3626840, useful),
    "Tall, Tall Mountain - Monty Moles": SM64ItemData(3626841, progression),
    "Lethal Lava Land - Big Bullies": SM64ItemData(3626842, progression),
    "Snowman's Land - Chill Bully": SM64ItemData(3626843, progression),
    "Big Boo's Haunt - Big Boo": SM64ItemData(3626844, progression),
    "Whomp's Fortress - Thwomp": SM64ItemData(3626846, progression),
    "Shifting Sand Land - Thwomp": SM64ItemData(3626847, progression),
    "Tick Tock Clock - Thwomp": SM64ItemData(3626848, progression),
}

bowser_bomb_item_data_table: dict[str, SM64ItemData] = {
    "Progressive Bowser Arena Bomb": SM64ItemData(3626849, progression),
    "Bowser in the Dark World - Progressive Bowser Arena Bomb": SM64ItemData(3626850, progression),
    "Bowser in the Fire Sea - Progressive Bowser Arena Bomb": SM64ItemData(3626851, progression),
    "Bowser in the Sky - Progressive Bowser Arena Bomb": SM64ItemData(3626852, progression),
}


global_mode_coin_object_item_names = (
    "Single Yellow Coins",
    "Red Coins",
    "Single Blue Coins",
    "Blue Coin Blocks",
    "Horizontal Coin Lines",
    "Horizontal Coin Rings",
    "Coin Arrows",
    "Vertical Coin Lines",
    "Vertical Coin Rings",
    "Breakable Coin Boxes",
    "Throwable Cork Boxes",
    "Crazy Boxes",
    "Wooden Posts",
    "Three-Coin Blocks",
    "Ten-Coin Blocks",
    "Lethal Lava Land - Bowser Puzzle",
)


global_mode_enemy_item_names = (
    "Bob-ombs",
    "Boos",
    "Bullies",
    "Chuckyas",
    "Lakitus",
    "Fire Piranha Plants",
    "Fly Guys",
    "Goombas",
    "Koopa Troopas",
    "Mr Blizzards",
    "Mr. Is",
    "Scuttlebugs",
    "Snufits",
    "Spindrifts",
    "Whomps",
    "Monty Moles",
    "Big Bully",
    "Shifting Sand Land - Eyerok",
    "Big Boo's Haunt - Flying Bookends",
    "Snowman's Land - Moneybags",
    "Whomp's Fortress - Piranha Plants",
    "Shifting Sand Land - Pokeys",
    "Wet-Dry World - Skeeters",
    "Hazy Maze Cave - Swoops",
    "Big Boo's Haunt - Big Boo",
    "Thwomp",
)

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
    **painting_unlock_item_data_table,
    **global_coin_object_item_data_table,
    **per_level_coin_object_item_data_table,
    **global_enemy_item_data_table,
    **per_level_enemy_item_data_table,
    **bowser_bomb_item_data_table,
    **trap_item_data_table
}

item_table = {name: data.code for name, data in item_data_table.items() if data.code is not None}

item_name_groups: dict[str, set[str]] = {
    "Keys": {"Basement Key", "Second Floor Key", "Progressive Key", *castle_key_item_data_table},
    "Caps": set(global_cap_item_names) | set(cap_item_data_table),
    "Global Caps": set(global_cap_item_names),
    "Per-Level Caps": set(cap_item_data_table),
    "Moves": set(action_item_data_table) | set(per_level_action_item_data_table),
    "Global Moves": set(action_item_data_table),
    "Per-Level Moves": set(per_level_action_item_data_table),
    "Cannon Unlocks": set(cannon_item_data_table),
    "Painting Unlocks": set(painting_unlock_item_data_table),
    "Course Feature Unlocks": set(feature_item_data_table),
    "Castle Unlocks": set(castle_progression_item_data_table),
    "Optional Feature Unlocks": set(arbitrary_item_data_table),
    "Global Arbitrary Feature Unlocks": set(global_arbitrary_item_data_table),
    "Per-Level Checkerboard Platforms": set(checkerboard_item_data_table),
    "Per-Level Rolling Logs": set(rolling_log_item_data_table),
    "Per-Level Purple Switches": set(purple_switch_item_data_table),
    "Bowser Stage Extra 1-Up Unlocks": set(bowser_stage_1up_item_data_table),
    "Coin Object Unlocks": set(global_coin_object_item_data_table) | set(per_level_coin_object_item_data_table),
    "Global Coin Object Unlocks": set(global_coin_object_item_data_table),
    "Per-Level Coin Object Unlocks": set(per_level_coin_object_item_data_table),
    "Enemy Unlocks": set(global_enemy_item_data_table) | set(per_level_enemy_item_data_table),
    "Global Enemy Unlocks": set(global_enemy_item_data_table),
    "Per-Level Enemy Unlocks": set(per_level_enemy_item_data_table),
    "Progressive Bowser Arena Bombs": set(bowser_bomb_item_data_table),
    "Optional Items": set(optional_item_data_table),
    "Filler": {"1-Up Mushroom"},
     "Traps": set(trap_item_data_table),
}
