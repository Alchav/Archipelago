import logging
from dataclasses import dataclass
from BaseClasses import ItemClassification
from Utils import Version
from enum import IntEnum
from typing import List, Dict, Optional, Tuple

CRYSTALIS_BASE_ID: int = 2241000
CRYSTALIS_APWORLD_VERSION: Version = Version(2, 0, 0)
BOSS_NAMES: List[str] = ["Giant Insect", "Vampire 2", "Kelbesque 1", "Sabera 1", "Mado 1", "Kelbesque 2", "Sabera 2",
                         "Mado 2", "Karmine"]
ELEMENTS: List[str] = ["Wind", "Fire", "Water", "Thunder"]
WALL_NAMES: List[str] = ["Zebu Cave", "East Cave", "Sealed Cave", "Mt Sabre West", "Mt Sabre North", "Waterfall Cave",
                         "Fog Lamp Cave", "Kirisa Plant Cave", "Evil Spirit Island", "Mt Hydra",
                         "Goa Fortress - Entrance", "Goa Fortress Basement", "Goa Fortress - Sabera Item",
                         "Goa Fortress - Sabera Boss", "Goa Fortress - Mado 2", "Goa Fortress - Karmine 5"]
TRADE_IN_NPCS: List[str] = ["Akahana", "Aryllis", "Fisherman", "Kensu", "Slimed Kensu"]
SHOP_INVENTORIES: Dict[str, List[str]] = {
    "Leaf Item Shop":     ["Medical Herb", "Antidote", "Warp Boots"],
    "Brynmaer Item Shop": ["Medical Herb", "Antidote", "Warp Boots"],
    "Oak Item Shop":      ["Medical Herb", "Antidote", "Fruit of Power"],
    "Nadare's Item Shop": ["Medical Herb", "Antidote", "Fruit of Power", "Warp Boots"],
    "Amazones Item Shop": ["Warp Boots", "Lysis Plant", "Fruit of Power"],
    "Portoa Item Shop":   ["Medical Herb", "Warp Boots", "Lysis Plant", "Fruit of Lime"],
    "Joel Item Shop":     ["Medical Herb", "Antidote", "Fruit of Power"],
    "Swan Item Shop":     ["Medical Herb", "Antidote", "Fruit of Power", "Warp Boots"],
    "Goa Item Shop":      ["Medical Herb", "Antidote", "Lysis Plant", "Warp Boots"],
    "Shyron Item Shop":   ["Medical Herb", "Antidote", "Fruit of Lime", "Magic Ring"],
    "Sahara Item Shop":   ["Antidote", "Magic Ring", "Fruit of Repun", "Warp Boots"]
}
SCREEN_NAMES_TO_IDS: Dict[str, int] = {
    "Leaf - Outside Start" : 0x1,
    "Leaf" : 0x2,
    "Valley of Wind" : 0x3,
    "Sealed Cave 1" : 0x4,
    "Sealed Cave 2" : 0x5,
    "Sealed Cave 6" : 0x6,
    "Sealed Cave 4" : 0x7,
    "Sealed Cave 5" : 0x8,
    "Sealed Cave 3" : 0x9,
    "Sealed Cave 7" : 0xA,
    "East Cave 1" : 0xB,
    "Sealed Cave 8" : 0xC,
    "East Cave 2" : 0xD,
    "Windmill Cave" : 0xE,
    "Windmill" : 0xF,
    "Zebu Cave" : 0x10,
    "Mt Sabre West - Cave 1" : 0x11,
    "East Cave 3" : 0x12,
    "Cordel Plain West" : 0x14,
    "Cordel Plain East" : 0x15,
    "Brynmaer" : 0x18,
    "Outside Stom House" : 0x19,
    "Swamp" : 0x1A,
    "Amazones" : 0x1B,
    "Oak" : 0x1C,
    "Stom House" : 0x1E,
    "Mt Sabre West - Lower" : 0x20,
    "Mt Sabre West - Upper" : 0x21,
    "Mt Sabre West - Cave 2" : 0x22,
    "Mt Sabre West - Cave 3" : 0x23,
    "Mt Sabre West - Cave 4" : 0x24,
    "Mt Sabre West - Cave 5" : 0x25,
    "Mt Sabre West - Cave 6" : 0x26,
    "Mt Sabre West - Cave 7" : 0x27,
    "Mt Sabre North - Main" : 0x28,
    "Mt Sabre North - Middle" : 0x29,
    "Mt Sabre North - Cave 2" : 0x2A,
    "Mt Sabre North - Cave 3" : 0x2B,
    "Mt Sabre North - Cave 4" : 0x2C,
    "Mt Sabre North - Cave 5" : 0x2D,
    "Mt Sabre North - Cave 6" : 0x2E,
    "Mt Sabre North - Prison Hall" : 0x2F,
    "Mt Sabre North - Left Cell" : 0x30,
    "Mt Sabre North - Left Cell 2" : 0x31,
    "Mt Sabre North - Right Cell" : 0x32,
    "Mt Sabre North - Cave 8" : 0x33,
    "Mt Sabre North - Cave 9" : 0x34,
    "Mt Sabre North - Summit Cave" : 0x35,
    "Mt Sabre North - Cave 1" : 0x38,
    "Mt Sabre North - Cave 7" : 0x39,
    "Nadare - Back Room" : 0x3E,
    "Waterfall Valley North" : 0x40,
    "Waterfall Valley South" : 0x41,
    "Lime Tree Valley" : 0x42,
    "Kirisa Plant Cave 1" : 0x44,
    "Kirisa Plant Cave 2" : 0x45,
    "Kirisa Plant Cave 3" : 0x46,
    "Kirisa Meadow" : 0x47,
    "Fog Lamp Cave 1" : 0x48,
    "Fog Lamp Cave 2" : 0x49,
    "Fog Lamp Cave 3" : 0x4A,
    "Fog Lamp Cave Dead End" : 0x4B,
    "Fog Lamp Cave 4" : 0x4C,
    "Fog Lamp Cave 5" : 0x4D,
    "Fog Lamp Cave 6" : 0x4E,
    "Fog Lamp Cave 7" : 0x4F,
    "Portoa" : 0x50,
    "Portoa - Fisherman Island" : 0x51,
    "Waterfall Cave 1" : 0x54,
    "Waterfall Cave 2" : 0x55,
    "Waterfall Cave 3" : 0x56,
    "Waterfall Cave 4" : 0x57,
    "Angry Sea" : 0x60,
    "Boat House" : 0x61,
    "Joel Lighthouse" : 0x62,
    "Zombie Town" : 0x65,
    "Evil Spirit Island 2" : 0x69,
    "Evil Spirit Island 3" : 0x6A,
    "Evil Spirit Island 4" : 0x6B,
    "Sabera Palace 1" : 0x6C,
    "Sabera Palace 2" : 0x6D,
    "Sabera Palace 3" : 0x6E,
    "Sabera Palace 2 - West" : 0x6F,
    "Joel Secret Passage" : 0x70,
    "Joel" : 0x71,
    "Swan" : 0x72,
    "Swan Gate" : 0x73,
    "Goa Valley" : 0x78,
    "Mt Hydra" : 0x7C,
    "Mt Hydra - Cave 1" : 0x7D,
    "Mt Hydra - Outside Shyron" : 0x7E,
    "Mt Hydra - Cave 2" : 0x7F,
    "Mt Hydra - Cave 3" : 0x80,
    "Mt Hydra - Cave 4" : 0x81,
    "Mt Hydra - Cave 5" : 0x82,
    "Mt Hydra - Cave 6" : 0x83,
    "Mt Hydra - Cave 7" : 0x84,
    "Mt Hydra - Cave 8" : 0x85,
    "Mt Hydra - Cave 9" : 0x86,
    "Mt Hydra - Cave 10" : 0x87,
    "Styx 1" : 0x88,
    "Styx 2" : 0x89,
    "Styx 3" : 0x8A,
    "Shyron" : 0x8C,
    "Goa" : 0x8E,
    "Goa Fortress Basement" : 0x8F,
    "Desert 1" : 0x90,
    "Oasis Cave Main" : 0x91,
    "Desert Cave 1" : 0x92,
    "Sahara" : 0x93,
    "Sahara Outside Cave" : 0x94,
    "Desert Cave 2" : 0x95,
    "Sahara Meadow" : 0x96,
    "Desert 2" : 0x98,
    "Pyramid - Entrance" : 0x9C,
    "Pyramid - Branch" : 0x9D,
    "Pyramid - Main" : 0x9E,
    "Pyramid - Draygon" : 0x9F,
    "Crypt - Entrance" : 0xA0,
    "Crypt - Hall 1" : 0xA1,
    "Crypt - Branch" : 0xA2,
    "Crypt - Dead End Left" : 0xA3,
    "Crypt - Dead End Right" : 0xA4,
    "Crypt - Hall 2" : 0xA5,
    "Goa Fortress - Entrance" : 0xA8,
    "Goa Fortress - Kelbesque" : 0xA9,
    "Goa Fortress - Zebu" : 0xAA,
    "Goa Fortress - Sabera" : 0xAB,
    "Goa Fortress - Tornel" : 0xAC,
    "Goa Fortress - Mado 1" : 0xAD,
    "Goa Fortress - Mado 2" : 0xAE,
    "Goa Fortress - Mado 3" : 0xAF,
    "Goa Fortress - Karmine 1" : 0xB0,
    "Goa Fortress - Karmine 2" : 0xB1,
    "Goa Fortress - Karmine 3" : 0xB2,
    "Goa Fortress - Karmine 4" : 0xB3,
    "Goa Fortress - Karmine 5" : 0xB4,
    "Goa Fortress - Karmine 6" : 0xB5,
    "Goa Fortress - Karmine 7" : 0xB6,
    "Goa Fortress - Exit" : 0xB7,
    "Oasis Cave - Entrance" : 0xB8,
    "Goa Fortress - Asina" : 0xB9,
    "Goa Fortress - Kensu" : 0xBA,
    "Goa - House" : 0xBB,
    "Goa - Tavern" : 0xBF,
    "Leaf - Elder House" : 0xC0,
    "Leaf - Rabbit Hut" : 0xC1,
    "Leaf - Student House" : 0xC5,
    "Brynmaer - Tavern" : 0xC6,
    "Oak - Elder House" : 0xCD,
    "Oak - Mother House" : 0xCE,
    "Amazones - Elder" : 0xD4,
    "Nadare" : 0xD5,
    "Portoa - Fisherman House" : 0xD6,
    "Portoa - Palace Entrance" : 0xD7,
    "Portoa - Fortune Teller" : 0xD8,
    "Portoa Palace - Left" : 0xDE,
    "Portoa Palace - Throne Room" : 0xDF,
    "Portoa Palace - Right" : 0xE0,
    "Portoa - Asina Room" : 0xE1,
    "Amazones - Elder Downstairs" : 0xE2,
    "Joel - Elder House" : 0xE3,
    "Joel - Shed" : 0xE4,
    "Zombie Town - House" : 0xE8,
    "Zombie Town - House Basement" : 0xE9,
    "Swan - Stom Hut" : 0xEC,
    "Swan - Tavern" : 0xEF,
    "Swan - Dance Hall" : 0xF1,
    "Shyron - Temple" : 0xF2,
    "Shyron - Training Hall" : 0xF3,
    "Shyron - Hospital" : 0xF4,
    "Sahara - Elder House" : 0xFA,
}


def convert_text_to_elem_int(text: str) -> int:
    return ELEMENTS.index(text)


class CrystalisItemCategoryEnum(IntEnum):
    FILLER = 0
    PROGRESSION = 1
    USEFUL = 2
    CONDITIONAL = 3
    TRAP = 4
    PROGUSEFUL = 5


def convert_enum_to_item_classification(enum: CrystalisItemCategoryEnum) -> ItemClassification:
    if enum == CrystalisItemCategoryEnum.FILLER:
        return ItemClassification.filler
    if enum == CrystalisItemCategoryEnum.PROGRESSION:
        return ItemClassification.progression
    if enum == CrystalisItemCategoryEnum.USEFUL:
        return ItemClassification.useful
    if enum == CrystalisItemCategoryEnum.CONDITIONAL:
        logging.warning("Unhandled conditional progression item in Crystalis. Defaulting to progression.")
        return ItemClassification.progression
    if enum == CrystalisItemCategoryEnum.TRAP:
        return ItemClassification.trap
    if enum == CrystalisItemCategoryEnum.PROGUSEFUL:
        return ItemClassification.progression | ItemClassification.progression
    raise ValueError(f"Crystalis: Unrecognized value in convert_enum_to_item_classification: {enum}")
    return ItemClassification.filler


class CrystalisItemPaletteEnum(IntEnum):
    WIND_EQUIP = 0
    FIRE_EQUIP = 1
    WATER_EQUIP = 2
    THUNDER_EQUIP = 3
    WIND_CONSUMABLE = 4
    FIRE_CONSUMABLE = 5
    WATER_CONSUMABLE = 6
    THUNDER_CONSUMABLE = 7
    MIMIC = 8
    RANDOM = 9


def convert_enum_to_palette(enum: CrystalisItemPaletteEnum) -> Tuple[int, int]:
    if enum == CrystalisItemPaletteEnum.WIND_EQUIP:
        return [0x19,0x03]
    if enum == CrystalisItemPaletteEnum.FIRE_EQUIP:
        return [0x27,0x16]
    if enum == CrystalisItemPaletteEnum.WATER_EQUIP:
        return [0x2C,0x12]
    if enum == CrystalisItemPaletteEnum.THUNDER_EQUIP:
        return [0x37,0x0C]
    if enum == CrystalisItemPaletteEnum.WIND_CONSUMABLE:
        return [0x2A,0x03]
    if enum == CrystalisItemPaletteEnum.FIRE_CONSUMABLE:
        return [0x27,0x05]
    if enum == CrystalisItemPaletteEnum.WATER_CONSUMABLE:
        return [0x2C,0x12]
    if enum == CrystalisItemPaletteEnum.THUNDER_CONSUMABLE:
        return [0x28,0x00]
    if enum == CrystalisItemPaletteEnum.MIMIC:
        return [0x36,0x14]
    raise ValueError(f"Crystalis: Unrecognized value in convert_enum_to_palette: {enum}")
    return [0,0]


class CrystalisEntranceTypeEnum(IntEnum):
    STATIC = 0
    OW_UP = 1
    OW_DOWN = 2
    OW_LEFT = 3
    OW_RIGHT = 4
    CAVE_ENTRANCE = 5
    CAVE_EXIT = 6
    HOUSE_ENTRANCE = 7
    HOUSE_EXIT = 8
    PALACE_HOUSE_ENTRANCE = 9
    PALACE_HOUSE_EXIT = 10
    PALACE_AREA_ENTRANCE = 11
    PALACE_AREA_EXIT = 12
    SHED_ENTRANCE = 13
    SHED_EXIT = 14
    EXT_ENTRANCE = 15
    EXT_EXIT = 16
    GOA_TRANSITION = 17


@dataclass
class CrystalisLocationData:
    name: str
    rom_id: int
    ap_id_offset: int
    unique: bool
    lossy: bool
    prevent_loss: bool
    is_chest: bool


@dataclass
class CrystalisEntranceData:
    name: str
    parent_region: str
    entrance_type: CrystalisEntranceTypeEnum
    vanilla_target: str
    exit_key: str
    house_key: str
    related_entrances: List[str]
    house_type: str
    can_lock: bool


@dataclass
class CrystalisRegionData:
    name: str
    wildwarpIds: List[int]
    entrances: List[CrystalisEntranceData]
    locations: List[CrystalisLocationData]
    ban_wildwarp: bool


@dataclass
class CrystalisItemData:
    name: str
    rom_id: int
    ap_id_offset: int
    unique: bool
    losable: bool
    prevent_loss: bool
    community: bool
    default_count: int
    groups: List[str]
    palette: CrystalisItemPaletteEnum
    category: CrystalisItemCategoryEnum


@dataclass
class CrystalisShuffleData:
    wall_map: Dict[str, str]
    key_item_names: Dict[str, str]
    trade_in_map: Dict[str, str]
    boss_reqs: Dict[str, str]
    gbc_cave_exits: List[str]
    thunder_warp: str
    shop_inventories: Dict[str, List[str]]
    wildwarps: List[int]
    goa_connection_map: Dict[str, str]
    er_pairings: Dict[str, str]
