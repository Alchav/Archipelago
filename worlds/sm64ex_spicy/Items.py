from typing import NamedTuple

from BaseClasses import Item, ItemClassification

sm64ex_base_id: int = 3626000

class SM64Item(Item):
    game: str = "SM64: Spicy Mycena 64"

class SM64ItemData(NamedTuple):
    code: int | None = None
    classification: ItemClassification = ItemClassification.progression

generic_item_data_table: dict[str, SM64ItemData] = {
    "Basement Key": SM64ItemData(sm64ex_base_id + 178),
    "Second Floor Key": SM64ItemData(sm64ex_base_id + 179),
    "Progressive Key": SM64ItemData(sm64ex_base_id + 180),
    "Wing Cap": SM64ItemData(sm64ex_base_id + 181),
    "Metal Cap": SM64ItemData(sm64ex_base_id + 182),
    "Vanish Cap": SM64ItemData(sm64ex_base_id + 183),
    "1Up Mushroom": SM64ItemData(sm64ex_base_id + 184, ItemClassification.filler),
}

global_cap_item_names = ("Wing Cap", "Metal Cap", "Vanish Cap")

feature_item_data_table: dict[str, SM64ItemData] = {
    "Bob-omb Battlefield - King Bob-omb": SM64ItemData(sm64ex_base_id + 245, ItemClassification.progression_deprioritized),
    "Bob-omb Battlefield - Koopa the Quick": SM64ItemData(sm64ex_base_id + 246, ItemClassification.progression_deprioritized),
    "Bob-omb Battlefield - Bob-omb Buddy": SM64ItemData(sm64ex_base_id + 247, ItemClassification.progression_deprioritized),
    "Whomp's Fortress - Whomp King": SM64ItemData(sm64ex_base_id + 248, ItemClassification.progression_deprioritized),
    "Whomp's Fortress - Fortress": SM64ItemData(sm64ex_base_id + 249),
    "Whomp's Fortress - Bob-omb Buddy": SM64ItemData(sm64ex_base_id + 250, ItemClassification.progression_deprioritized),
    "Whomp's Fortress - Hoot": SM64ItemData(sm64ex_base_id + 251),
    "Cool, Cool Mountain - Snowman's Head": SM64ItemData(sm64ex_base_id + 252, ItemClassification.progression_deprioritized),
    "Cool, Cool Mountain - Big Penguin": SM64ItemData(sm64ex_base_id + 253, ItemClassification.progression_deprioritized),
    "Jolly Roger Bay - Sunken Ship": SM64ItemData(sm64ex_base_id + 254, ItemClassification.progression_deprioritized),
    "Jolly Roger Bay - Raised Ship": SM64ItemData(sm64ex_base_id + 255, ItemClassification.progression_deprioritized),
    "Jolly Roger Bay - Bob-omb Buddy": SM64ItemData(sm64ex_base_id + 256, ItemClassification.progression_deprioritized),
    "Jolly Roger Bay - Jet Stream": SM64ItemData(sm64ex_base_id + 257, ItemClassification.progression_deprioritized),
    "Jolly Roger Bay - Unagi": SM64ItemData(sm64ex_base_id + 258, ItemClassification.progression_deprioritized),
    "Lethal Lava Land - Koopa Shell": SM64ItemData(sm64ex_base_id + 259, ItemClassification.progression_deprioritized_skip_balancing),
    "Shifting Sand Land - Klepto Star": SM64ItemData(sm64ex_base_id + 260, ItemClassification.progression_deprioritized),
    "Tiny-Huge Island - Koopa the Quick": SM64ItemData(sm64ex_base_id + 261, ItemClassification.progression_deprioritized),
    "Tall, Tall Mountain - Ukiki": SM64ItemData(sm64ex_base_id + 262, ItemClassification.progression_deprioritized),
    "Dire, Dire Docks - Manta Ray": SM64ItemData(sm64ex_base_id + 263, ItemClassification.progression_deprioritized),
    "Dire, Dire Docks - Bowser's Sub": SM64ItemData(sm64ex_base_id + 264, ItemClassification.progression_deprioritized),
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
    "Progressive MIPS": SM64ItemData(sm64ex_base_id + 271, ItemClassification.progression_deprioritized),
    "Wing Cap Light": SM64ItemData(sm64ex_base_id + 272),
    "Courtyard Boos": SM64ItemData(sm64ex_base_id + 273),
    "Castle Toads": SM64ItemData(sm64ex_base_id + 274),
    "Cannon Unlock - Castle": SM64ItemData(sm64ex_base_id + 275, ItemClassification.progression_deprioritized_skip_balancing),
    "Yoshi": SM64ItemData(sm64ex_base_id + 276, ItemClassification.progression_deprioritized_skip_balancing),
    "Unlock Bowser in the Fire Sea": SM64ItemData(sm64ex_base_id + 304),
}

cap_item_data_table: dict[str, SM64ItemData] = {
    "Bob-omb Battlefield - Wing Cap": SM64ItemData(sm64ex_base_id + 277),
    "Castle - Wing Cap": SM64ItemData(sm64ex_base_id + 278, ItemClassification.filler),
    "Lethal Lava Land - Wing Cap": SM64ItemData(sm64ex_base_id + 279, ItemClassification.progression_deprioritized_skip_balancing),
    "Shifting Sand Land - Wing Cap": SM64ItemData(sm64ex_base_id + 280, ItemClassification.progression_deprioritized),
    "Tower of the Wing Cap - Wing Cap": SM64ItemData(sm64ex_base_id + 281, ItemClassification.filler),
    "Wing Mario Over the Rainbow - Wing Cap": SM64ItemData(sm64ex_base_id + 282),
    "Whomp's Fortress - Metal Cap": SM64ItemData(sm64ex_base_id + 283, ItemClassification.filler),
    "Jolly Roger Bay - Metal Cap": SM64ItemData(sm64ex_base_id + 284, ItemClassification.progression_deprioritized),
    "Hazy Maze Cave - Metal Cap": SM64ItemData(sm64ex_base_id + 285, ItemClassification.progression_deprioritized),
    "Dire, Dire Docks - Metal Cap": SM64ItemData(sm64ex_base_id + 286, ItemClassification.progression_deprioritized),
    "Wet-Dry World - Metal Cap": SM64ItemData(sm64ex_base_id + 287, ItemClassification.filler),
    "Cavern of the Metal Cap - Metal Cap": SM64ItemData(sm64ex_base_id + 288, ItemClassification.progression_deprioritized),
    "Bowser in the Dark World - Metal Cap": SM64ItemData(sm64ex_base_id + 289, ItemClassification.filler),
    "Big Boo's Haunt - Vanish Cap": SM64ItemData(sm64ex_base_id + 290, ItemClassification.progression_deprioritized),
    "Dire, Dire Docks - Vanish Cap": SM64ItemData(sm64ex_base_id + 291, ItemClassification.progression_deprioritized),
    "Snowman's Land - Vanish Cap": SM64ItemData(sm64ex_base_id + 292, ItemClassification.progression_deprioritized),
    "Vanish Cap Under the Moat - Vanish Cap": SM64ItemData(sm64ex_base_id + 293, ItemClassification.progression_deprioritized),
    "Wet-Dry World - Vanish Cap": SM64ItemData(sm64ex_base_id + 294, ItemClassification.progression_deprioritized_skip_balancing),
}

simple_arbitrary_item_data_table: dict[str, SM64ItemData] = {
    "Hazy Maze Cave - Swimming Beast": SM64ItemData(sm64ex_base_id + 295),
    "Rainbow Ride - Carpets": SM64ItemData(sm64ex_base_id + 296),
    "Tiny-Huge Island - Warp Pipes": SM64ItemData(sm64ex_base_id + 298),
    "Cool, Cool Mountain - Baby Penguins": SM64ItemData(sm64ex_base_id + 299, ItemClassification.progression_deprioritized_skip_balancing),
    "Snowman's Land - Penguin": SM64ItemData(sm64ex_base_id + 300, ItemClassification.progression_deprioritized_skip_balancing),
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
    "Bob-omb Battlefield - Checkerboard Platforms": SM64ItemData(sm64ex_base_id + 306, ItemClassification.filler),
    "Whomp's Fortress - Checkerboard Platforms": SM64ItemData(sm64ex_base_id + 307),
    "Lethal Lava Land - Checkerboard Platforms": SM64ItemData(sm64ex_base_id + 308, ItemClassification.progression_deprioritized_skip_balancing),
    "Hazy Maze Cave - Checkerboard Platform": SM64ItemData(sm64ex_base_id + 309),
    "Vanish Cap Under the Moat - Checkerboard Platforms": SM64ItemData(sm64ex_base_id + 310),
}

rolling_log_item_data_table: dict[str, SM64ItemData] = {
    "Lethal Lava Land - Rolling Log": SM64ItemData(sm64ex_base_id + 311, ItemClassification.progression_deprioritized_skip_balancing),
    "Tall, Tall Mountain - Rolling Log": SM64ItemData(sm64ex_base_id + 312, ItemClassification.filler),
}

purple_switch_item_data_table: dict[str, SM64ItemData] = {
    "Bob-omb Battlefield - Purple Switch": SM64ItemData(sm64ex_base_id + 313, ItemClassification.filler),
    "Hazy Maze Cave - Purple Switch": SM64ItemData(sm64ex_base_id + 314, ItemClassification.progression_deprioritized_skip_balancing),
    "Wet-Dry World - Purple Switch": SM64ItemData(sm64ex_base_id + 315),
    "Rainbow Ride - Purple Switch": SM64ItemData(sm64ex_base_id + 316, ItemClassification.progression_deprioritized_skip_balancing),
    "Bowser in the Dark World - Purple Switch": SM64ItemData(sm64ex_base_id + 317),
    "Bowser in the Sky - Purple Switch": SM64ItemData(sm64ex_base_id + 318, ItemClassification.progression_skip_balancing),
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

cannon_item_data_table: dict[str, SM64ItemData] = {
    "Cannon Unlock Bob-omb Battlefield": SM64ItemData(sm64ex_base_id + 200),
    "Cannon Unlock Whomp's Fortress": SM64ItemData(sm64ex_base_id + 201),
    "Cannon Unlock Jolly Roger Bay": SM64ItemData(sm64ex_base_id + 202),
    "Cannon Unlock Cool, Cool Mountain": SM64ItemData(sm64ex_base_id + 203),
    "Cannon Unlock Shifting Sand Land": SM64ItemData(sm64ex_base_id + 207),
    "Cannon Unlock Snowman's Land": SM64ItemData(sm64ex_base_id + 209),
    "Cannon Unlock Wet-Dry World": SM64ItemData(sm64ex_base_id + 210),
    "Cannon Unlock Tall, Tall Mountain": SM64ItemData(sm64ex_base_id + 211),
    "Cannon Unlock Tiny-Huge Island": SM64ItemData(sm64ex_base_id + 212),
    "Cannon Unlock Rainbow Ride": SM64ItemData(sm64ex_base_id + 214),

}

painting_unlock_item_data_table: dict[str, SM64ItemData] = {
    "Painting Unlock Whomp's Fortress": SM64ItemData(sm64ex_base_id + 231),
    "Painting Unlock Jolly Roger Bay": SM64ItemData(sm64ex_base_id + 232),
    "Painting Unlock Cool, Cool Mountain": SM64ItemData(sm64ex_base_id + 233),
    "Painting Unlock Lethal Lava Land": SM64ItemData(sm64ex_base_id + 236),
    "Painting Unlock Shifting Sand Land": SM64ItemData(sm64ex_base_id + 237),
    "Painting Unlock Dire, Dire Docks": SM64ItemData(sm64ex_base_id + 238),
    "Painting Unlock Snowman's Land": SM64ItemData(sm64ex_base_id + 239),
    "Painting Unlock Wet-Dry World": SM64ItemData(sm64ex_base_id + 240),
    "Painting Unlock Tall, Tall Mountain": SM64ItemData(sm64ex_base_id + 241),
    "Painting Unlock Tiny-Huge Island": SM64ItemData(sm64ex_base_id + 242),
    "Painting Unlock Tick Tock Clock": SM64ItemData(sm64ex_base_id + 243),
}

item_data_table = {
    **generic_item_data_table,
    **feature_item_data_table,
    **castle_key_item_data_table,
    **castle_progression_item_data_table,
    **cap_item_data_table,
    **arbitrary_item_data_table,
    **action_item_data_table,
    **cannon_item_data_table,
    **painting_unlock_item_data_table
}

item_table = {name: data.code for name, data in item_data_table.items() if data.code is not None}
