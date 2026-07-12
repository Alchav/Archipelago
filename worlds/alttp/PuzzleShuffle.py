from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from .PotShuffle import (
    FilledPot,
    POT_ARROW,
    POT_BLUE_RUPEE,
    POT_HEART,
    POT_ITEM_ADDRESSES,
    POT_KEY,
    POT_SWITCH,
    get_vanilla_pot_items,
)
from .EnemyLogicTargets import (
    DESERT_BEAMOS_HELLWAY_BOTTOM_LEFT,
    DESERT_BIG_CHEST_BOTTOM_LEFT,
    DESERT_FINAL_SECTION_ENTRANCE_SOUTHWEST,
    EASTERN_STALFOS_ROOM_SOUTHWEST,
    GANONS_TOWER_BIG_CHEST_ROOM_NORTHEAST,
    GANONS_TOWER_WINDER_WARP_MAZE_NORTH,
    ICE_PALACE_BOMB_JUMP_ROOM_NORTHWEST,
    get_enemy_clear_target_enemies,
)
from .enemizer_data.room_tags import ROOM_TAGS

if TYPE_CHECKING:
    from . import ALTTPWorld
    from .Rom import TokenRom


DESERT_MAP_CHEST_ROOM_ID = 0x74
DESERT_BIG_CHEST_ROOM_ID = 0x73
DESERT_FINAL_SECTION_ENTRANCE_ROOM_ID = 0x63
HYRULE_CASTLE_SWITCH_ROOM_ID = 0x02
TURTLE_ROCK_CRYSTAROLLER_ROOM_ID = 0x04
POD_STALFOS_TRAP_ROOM_ID = 0x0A
POD_TURTLE_ROOM_ID = 0x0B
POD_MIMICS_MOVING_WALL_ROOM_ID = 0x1B
ICE_PALACE_BOMB_FLOOR_ROOM_ID = 0x1E
ICE_PALACE_PENGATOR_BIG_KEY_ROOM_ID = 0x1F
TURTLE_ROCK_BIG_CHEST_ROOM_ID = 0x24
SWAMP_STATUE_ROOM_ID = 0x26
POD_MAP_CHEST_ROOM_ID = 0x2B
HERA_HARDHAT_BEETLES_ROOM_ID = 0x31
ICE_PALACE_CONVEYOR_HELLWAY_ROOM_ID = 0x3E
ICE_PALACE_MAP_ROOM_ID = 0x3F
THIEVES_TOWN_JAIL_CELLS_ROOM_ID = 0x45
SKULL_WOODS_GIBDO_TORCH_ROOM_ID = 0x49
POD_SOUTH_MIMICS_ROOM_ID = 0x4B
ICE_PALACE_BOMB_JUMP_ROOM_ID = 0x4E
SKULL_WOODS_BIG_KEY_ROOM_ID = 0x57
SKULL_WOODS_BIG_CHEST_ROOM_ID = 0x58
GT_GAUNTLET_123_ROOM_ID = 0x5D
ICE_PALACE_SPIKE_ROOM_ID = 0x5F
THIEVES_TOWN_WEST_ATTIC_ROOM_ID = 0x64
SWAMP_HIDDEN_DOOR_ROOM_ID = 0x66
GT_MIMICS_ROOM_ID = 0x6B
GT_GAUNTLET_45_ROOM_ID = 0x6D
GT_WINDER_WARP_MAZE_ROOM_ID = 0x7D
DESERT_WEST_ENTRANCE_ROOM_ID = 0x83
HERA_TILE_ROOM_ID = 0x87
GT_BLOCK_PUZZLE_ROOM_ID = 0x8B
GT_BIG_CHEST_ROOM_ID = 0x8C
GT_TILE_TORCH_PUZZLE_ROOM_ID = 0x8D
MISERY_MIRE_DARK_CANE_ROOM_ID = 0x93
GT_TORCHES_1_ROOM_ID = 0x96
ICE_PALACE_ICE_FLOOR_ROOM_ID = 0x9F
SWAMP_FLOODWAY_ROOM_ID = 0x10B
EASTERN_STALFOS_ROOM_ID = 0xA8
EASTERN_BIG_CHEST_ROOM_ID = 0xA9
EASTERN_MAP_CHEST_ROOM_ID = 0xAA
ICE_PALACE_HIDDEN_CHEST_ROOM_ID = 0xAE
AGA_TOWER_CIRCLE_OF_POTS_ROOM_ID = 0xB0
MISERY_MIRE_BRIDGE_CHEST_ROOM_ID = 0xB2
MISERY_MIRE_SPIKE_CHEST_ROOM_ID = 0xB3
EASTERN_BIG_KEY_ROOM_ID = 0xB8
EASTERN_DARK_SQUARE_ROOM_ID = 0xBA
THIEVES_TOWN_CONVEYOR_TOILET_ROOM_ID = 0xBC
ICE_PALACE_BLOCK_PUZZLE_ROOM_ID = 0xBE
AGA_TOWER_DARK_BRIDGE_ROOM_ID = 0xC0
MISERY_MIRE_TILE_ROOM_ID = 0xC1
MISERY_MIRE_MAIN_LOBBY_ROOM_ID = 0xC2
TURTLE_ROCK_TORCH_PUZZLE_ROOM_ID = 0xC7
ICE_PALACE_HOLE_TO_KHOLDSTARE_ROOM_ID = 0xCE
AGA_TOWER_DARK_MAZE_ROOM_ID = 0xD0
EASTERN_PRE_ARMOS_ROOM_ID = 0xD8
EASTERN_PRE_BOSS_ROOM_ID = 0xD9
EASTERN_SWITCH_ROOM_ID = 0xDA
TURTLE_ROCK_CHAIN_CHOMPS_ROOM_ID = 0xB6
TAG_NW_KILL_ENEMY_TO_OPEN = 0x01
TAG_NE_KILL_ENEMY_TO_OPEN = 0x02
TAG_SW_KILL_ENEMY_TO_OPEN = 0x03
TAG_SE_KILL_ENEMY_TO_OPEN = 0x04
TAG_W_KILL_ENEMY_TO_OPEN = 0x05
TAG_E_KILL_ENEMY_TO_OPEN = 0x06
TAG_N_KILL_ENEMY_TO_OPEN = 0x07
TAG_S_KILL_ENEMY_TO_OPEN = 0x08
TAG_CLEAR_QUADRANT_TO_OPEN = 0x09
TAG_NW_MOVE_BLOCK_TO_OPEN = 0x0B
TAG_NE_MOVE_BLOCK_TO_OPEN = 0x0C
TAG_SW_MOVE_BLOCK_TO_OPEN = 0x0D
TAG_SE_MOVE_BLOCK_TO_OPEN = 0x0E
TAG_W_MOVE_BLOCK_TO_OPEN = 0x0F
TAG_E_MOVE_BLOCK_TO_OPEN = 0x10
TAG_PULL_LEVER_TO_OPEN = 0x14
TAG_NOTHING = 0x00
TAG_USE_SWITCH_TO_BOMB_WALL = 0x20
TAG_USE_LEVER_TO_BOMB_WALL = 0x28
TAG_SECRET_WALL_RIGHT = 0x1C
TAG_SE_KILL_ENEMY_TO_MOVE_BLOCK = 0x26
TAG_NW_KILL_ENEMY_FOR_CHEST = 0x29
TAG_NE_KILL_ENEMY_FOR_CHEST = 0x2A
TAG_SW_KILL_ENEMY_FOR_CHEST = 0x2B
TAG_SE_KILL_ENEMY_FOR_CHEST = 0x2C
TAG_W_KILL_ENEMY_FOR_CHEST = 0x2D
TAG_TRIGGER_ACTIVATED_CHEST = 0x27
TAG_N_KILL_ENEMY_FOR_CHEST = 0x2F
TAG_LIGHT_TORCHES_TO_OPEN = 0x33
TAG_LIGHT_TORCHES_TO_GET_CHEST = 0x3E
TAG_SWITCH_OPENS_DOOR_HOLD = 0x16
TAG_SWITCH_OPENS_DOOR_TOGGLE = 0x17
TAG_WATER_TWIN = 0x1A
PULL_SWITCH_GOOD = 0x04
PULL_SWITCH_TRAP = 0x06
ROOM_VARIANT_VANILLA = 0
ROOM_VARIANT_SWAP_PULL_SWITCHES = 1
ROOM_VARIANT_KILL_ENEMIES = 2
ROOM_VARIANT_HOLD_SWITCH = 3
ROOM_VARIANT_TOGGLE_SWITCH = 4
HYRULE_CASTLE_SWITCH_ROOM_PULL_SWITCH_TRAP_SPRITE_ID_ADDRESS = 0x4D95A
HYRULE_CASTLE_SWITCH_ROOM_PULL_SWITCH_GOOD_SPRITE_ID_ADDRESS = 0x4D95D
HYRULE_CASTLE_SWITCH_ROOM_MIRRORED_BOMB_DROP_X_BYTES = (
    (0x4D944, 0xF0),
    (0x4D947, 0xF6),
    (0x4D94A, 0xF4),
    (0x4D94D, 0xF5),
    (0x4D950, 0xF3),
    (0x4D953, 0xF6),
    (0x4D956, 0xF4),
)
TURTLE_ROCK_CRYSTAROLLER_PULL_SWITCH_GOOD_SPRITE_ID_ADDRESS = 0x4D97A
TURTLE_ROCK_CRYSTAROLLER_PULL_SWITCH_TRAP_SPRITE_ID_ADDRESS = 0x4D97D
SWAMP_FLOODWAY_PULL_SWITCH_TRAP_SPRITE_ID_ADDRESS = 0x4EBAC
SWAMP_FLOODWAY_PULL_SWITCH_GOOD_SPRITE_ID_ADDRESS = 0x4EBBB
ICE_PALACE_HOLE_TO_KHOLDSTARE_PULL_SWITCH_X_ADDRESS = 0x4E903
ICE_PALACE_HOLE_TO_KHOLDSTARE_PULL_SWITCH_MOVED_X = 0x13
SKULL_WOODS_BIG_CHEST_PULL_SWITCH_GOOD_SPRITE_ID_ADDRESS = 0x4E018
SKULL_WOODS_BIG_CHEST_PULL_SWITCH_GOOD_SPRITE_ADDRESS = SKULL_WOODS_BIG_CHEST_PULL_SWITCH_GOOD_SPRITE_ID_ADDRESS - 2
SKULL_WOODS_BIG_CHEST_ROPE_TRAP_COMPATIBLE_SUBGROUP_2 = frozenset((28, 36))
SKULL_WOODS_BIG_CHEST_ROPE_TRAP_RECORD_BYTES = (0x0C, 0xE8, 0x06)
THIEVES_TOWN_WEST_ATTIC_PULL_SWITCH_TRAP_SPRITE_ID_ADDRESS = 0x4E0EA
DESERT_MAP_CHEST_TAG_CHOICES = (
    TAG_TRIGGER_ACTIVATED_CHEST,
    TAG_N_KILL_ENEMY_FOR_CHEST,
    TAG_LIGHT_TORCHES_TO_GET_CHEST,
)
DESERT_BIG_CHEST_BASE_TAG_CHOICES = (
    TAG_SWITCH_OPENS_DOOR_TOGGLE,
    TAG_SWITCH_OPENS_DOOR_HOLD,
)
DESERT_FINAL_SECTION_ENTRANCE_BASE_TAG_CHOICES = (
    TAG_SW_MOVE_BLOCK_TO_OPEN,
)
HERA_BIG_KEY_CHEST_BASE_TAG_CHOICES = (
    TAG_LIGHT_TORCHES_TO_GET_CHEST,
    TAG_SE_KILL_ENEMY_FOR_CHEST,
)
HERA_TILE_ROOM_BASE_TAG_2_CHOICES = (
    TAG_NW_KILL_ENEMY_TO_OPEN,
)
HERA_SWITCH_TAG_CHOICES = (
    TAG_SWITCH_OPENS_DOOR_TOGGLE,
    TAG_SWITCH_OPENS_DOOR_HOLD,
)
HERA_BIG_KEY_CHEST_SWITCH_POTS = frozenset(((76, 20), (112, 20)))
HERA_TILE_ROOM_WEST_SWITCH_POTS = frozenset(((12, 11), (16, 11), (16, 12), (24, 12), (32, 12), (40, 12)))
GT_BLOCK_PUZZLE_TOP_RIGHT_SWITCH_POTS = frozenset(((76, 12), (112, 12)))
GT_BIG_CHEST_ROOM_SWITCH_POT_ITEM = POT_SWITCH
NORMAL_SWITCH_REPLACEMENT_POT_ITEMS = (POT_ARROW, POT_BLUE_RUPEE, POT_HEART)
GT_BIG_CHEST_ROOM_PULL_SWITCH_TRAP_SPRITE_ID_ADDRESS = 0x4E3E5
GT_BIG_CHEST_ROOM_PULL_SWITCH_GOOD = 0x04
GT_TILE_TORCH_PUZZLE_TAG_CHOICES = (
    TAG_LIGHT_TORCHES_TO_OPEN,
    TAG_E_MOVE_BLOCK_TO_OPEN,
)
GT_TILE_TORCH_PUZZLE_EAST_SWITCH_POTS = frozenset(((204, 11), (204, 14)))
MISERY_MIRE_DARK_CANE_ROOM_VANILLA_SWITCH_POT = (28, 7)
MISERY_MIRE_DARK_CANE_ROOM_TOGGLE_SWITCH_POTS = frozenset((
    MISERY_MIRE_DARK_CANE_ROOM_VANILLA_SWITCH_POT,
    (96, 7),
))
GT_TORCHES_1_TAG_CHOICES = (
    TAG_LIGHT_TORCHES_TO_OPEN,
)
GT_TORCHES_1_SWITCH_POTS = frozenset(((14, 18), (14, 24), (32, 5), (32, 17), (32, 24), (46, 11)))
GT_TORCHES_1_HOLD_SWITCH_POTS = frozenset(((14, 18), (14, 24), (32, 24)))
ICE_PALACE_ICE_FLOOR_ROOM_TAG_CHOICES = (
    TAG_SWITCH_OPENS_DOOR_TOGGLE,
    TAG_SWITCH_OPENS_DOOR_HOLD,
    TAG_SW_KILL_ENEMY_TO_OPEN,
)
EASTERN_STALFOS_ROOM_HOLD_SWITCH_POTS = frozenset(((138, 19), (178, 19), (138, 28), (178, 28)))
EASTERN_BIG_CHEST_ROOM_TAG_CHOICES = (
    TAG_SWITCH_OPENS_DOOR_TOGGLE,
    TAG_SWITCH_OPENS_DOOR_HOLD,
)
EASTERN_BIG_CHEST_LEFT_SWITCH_POTS = frozenset(((12, 19), (112, 19), (16, 20), (108, 20)))
EASTERN_BIG_CHEST_RIGHT_SWITCH_POTS = frozenset((
    (144, 11), (236, 11), (144, 12), (236, 12),
    (144, 43), (236, 43), (144, 44), (236, 44),
))
EASTERN_MAP_CHEST_ROOM_TAG_CHOICES = (
    TAG_SWITCH_OPENS_DOOR_TOGGLE,
    TAG_SWITCH_OPENS_DOOR_HOLD,
)
ICE_PALACE_HIDDEN_CHEST_ROOM_TAG_CHOICES = (
    TAG_TRIGGER_ACTIVATED_CHEST,
    TAG_NE_KILL_ENEMY_FOR_CHEST,
)
MISERY_MIRE_BRIDGE_CHEST_TAG_2_CHOICES = (
    TAG_SE_MOVE_BLOCK_TO_OPEN,
    TAG_SE_KILL_ENEMY_TO_OPEN,
)
MISERY_MIRE_SPIKE_CHEST_TAG_CHOICES = (
    TAG_TRIGGER_ACTIVATED_CHEST,
    TAG_SW_KILL_ENEMY_FOR_CHEST,
)
EASTERN_DARK_SQUARE_ROOM_TAG_CHOICES = (
    TAG_SWITCH_OPENS_DOOR_TOGGLE,
    TAG_SWITCH_OPENS_DOOR_HOLD,
    TAG_NW_KILL_ENEMY_TO_OPEN,
)
THIEVES_TOWN_CONVEYOR_TOILET_TAG_CHOICES = (
    TAG_SWITCH_OPENS_DOOR_TOGGLE,
    TAG_SWITCH_OPENS_DOOR_HOLD,
    TAG_NW_KILL_ENEMY_TO_OPEN,
)
ICE_PALACE_BLOCK_PUZZLE_TAG_CHOICES = (
    TAG_SWITCH_OPENS_DOOR_HOLD,
    TAG_SWITCH_OPENS_DOOR_TOGGLE,
    TAG_SE_KILL_ENEMY_TO_OPEN,
)
MISERY_MIRE_TILE_ROOM_TAG_CHOICES = (
    TAG_LIGHT_TORCHES_TO_OPEN,
    TAG_SW_KILL_ENEMY_TO_OPEN,
)
TURTLE_ROCK_TORCH_PUZZLE_SWITCH_POTS = frozenset(((12, 10), (12, 11)))
ICE_PALACE_HOLE_TO_KHOLDSTARE_SWITCH_POTS = frozenset(((76, 8), (80, 8), (108, 12), (112, 12), (204, 11)))
EASTERN_PRE_ARMOS_NORTHEAST_SWITCH_POTS = frozenset(((202, 8), (242, 8), (202, 10), (242, 10), (202, 12), (242, 12)))
EASTERN_PRE_ARMOS_SOUTHEAST_SWITCH_POTS = frozenset(((92, 24), (96, 24)))
EASTERN_PRE_BOSS_ROOM_TAG_CHOICES = (
    TAG_SWITCH_OPENS_DOOR_TOGGLE,
    TAG_SWITCH_OPENS_DOOR_HOLD,
)
EASTERN_SWITCH_ROOM_TAG_CHOICES = (
    TAG_SWITCH_OPENS_DOOR_TOGGLE,
    TAG_SWITCH_OPENS_DOOR_HOLD,
)
HYRULE_CASTLE_SWITCH_ROOM_VARIANTS = (
    ROOM_VARIANT_VANILLA,
    ROOM_VARIANT_SWAP_PULL_SWITCHES,
    ROOM_VARIANT_KILL_ENEMIES,
)
TURTLE_ROCK_CRYSTAROLLER_VARIANTS = (
    ROOM_VARIANT_VANILLA,
    ROOM_VARIANT_SWAP_PULL_SWITCHES,
    ROOM_VARIANT_TOGGLE_SWITCH,
    ROOM_VARIANT_HOLD_SWITCH,
)
SWAMP_FLOODWAY_VARIANTS = (
    ROOM_VARIANT_VANILLA,
    ROOM_VARIANT_SWAP_PULL_SWITCHES,
)
POD_TURTLE_ROOM_TAG_CHOICES = (
    TAG_SW_KILL_ENEMY_TO_OPEN,
    TAG_LIGHT_TORCHES_TO_OPEN,
)
POD_MIMICS_MOVING_WALL_TAG_CHOICES = (
    TAG_SW_KILL_ENEMY_TO_OPEN,
    TAG_SWITCH_OPENS_DOOR_TOGGLE,
    TAG_SWITCH_OPENS_DOOR_HOLD,
)
POD_MIMICS_MOVING_WALL_SWITCH_POTS = frozenset(((20, 23), (40, 23)))
POD_TURTLE_ROOM_PUSH_BLOCK_SOURCE = (48, 46)
POD_TURTLE_ROOM_PUSH_BLOCK_TARGETS = ((44, 46), (46, 44), (46, 52))
POD_SOUTH_MIMICS_PUSH_BLOCK_SOURCE = (44, 4)
DESERT_FINAL_SECTION_ENTRANCE_PUSH_BLOCK_SOURCE = (21, 44)
DESERT_FINAL_SECTION_ENTRANCE_PUSH_BLOCK_TARGETS = ((9, 44),)
SWAMP_HIDDEN_DOOR_PUSH_BLOCK_SOURCE = (30, 48)
SWAMP_HIDDEN_DOOR_PUSH_BLOCK_TARGETS = ((18, 48), (24, 48), (38, 48), (44, 48), (50, 48))
GT_MIMICS_PUSH_BLOCK_SOURCE = (6, 12)
GT_MIMICS_PUSH_BLOCK_TARGETS = ((6, 20),)
TURTLE_ROCK_CHAIN_CHOMPS_PUSH_BLOCK_SOURCES = ((11, 21), (19, 21))
TURTLE_ROCK_CHAIN_CHOMPS_PUSH_BLOCK_TARGETS = ((19, 23),)
ICE_PALACE_BOMB_FLOOR_VARIANTS = (
    ROOM_VARIANT_VANILLA,
    ROOM_VARIANT_KILL_ENEMIES,
)
ICE_PALACE_BOMB_FLOOR_PUSH_BLOCK_POSITION_ADDRESS = 0x26F30
ICE_PALACE_BOMB_FLOOR_DOOR_TRIGGER_PUSH_BLOCK_POSITION = 0x185E
ICE_PALACE_PENGATOR_BIG_KEY_TAG_CHOICES = (
    TAG_SWITCH_OPENS_DOOR_TOGGLE,
    TAG_SW_KILL_ENEMY_TO_OPEN,
)
TURTLE_ROCK_BIG_CHEST_TAG_CHOICES = (
    TAG_NW_KILL_ENEMY_TO_OPEN,
    TAG_SWITCH_OPENS_DOOR_TOGGLE,
    TAG_SWITCH_OPENS_DOOR_HOLD,
)
SWAMP_STATUE_ROOM_TAG_CHOICES = (
    TAG_SWITCH_OPENS_DOOR_HOLD,
    TAG_SWITCH_OPENS_DOOR_TOGGLE,
)
POD_MAP_CHEST_ROOM_TAG_CHOICES = (
    TAG_SWITCH_OPENS_DOOR_HOLD,
    TAG_SWITCH_OPENS_DOOR_TOGGLE,
)
POD_MAP_CHEST_BOTTOM_SWITCH_POTS = frozenset(((146, 21), (170, 21), (146, 22), (170, 22)))
HERA_HARDHAT_BEETLES_TAG_2_CHOICES = (
    TAG_SE_KILL_ENEMY_TO_OPEN,
    TAG_SWITCH_OPENS_DOOR_TOGGLE,
    TAG_SWITCH_OPENS_DOOR_HOLD,
)
HERA_HARDHAT_BEETLES_SWITCH_POTS = frozenset(((92, 28),))
ICE_PALACE_CONVEYOR_HELLWAY_TAG_CHOICES = (
    TAG_NE_KILL_ENEMY_TO_OPEN,
    TAG_SWITCH_OPENS_DOOR_TOGGLE,
    TAG_SWITCH_OPENS_DOOR_HOLD,
)
ICE_PALACE_MAP_ROOM_TAG_CHOICES = (
    TAG_TRIGGER_ACTIVATED_CHEST,
    TAG_W_KILL_ENEMY_FOR_CHEST,
)
THIEVES_TOWN_JAIL_CELLS_TAG_CHOICES = (
    TAG_NW_KILL_ENEMY_TO_OPEN,
    TAG_SWITCH_OPENS_DOOR_HOLD,
    TAG_SWITCH_OPENS_DOOR_TOGGLE,
    TAG_NOTHING,
)
THIEVES_TOWN_JAIL_CELLS_NORTHWEST_SWITCH_POTS = frozenset(((12, 4), (108, 11), (48, 12)))
SKULL_WOODS_GIBDO_TORCH_BASE_TAG_CHOICES = (
    TAG_LIGHT_TORCHES_TO_OPEN,
)
SKULL_WOODS_GIBDO_TORCH_HOLD_SWITCH_POTS = frozenset(((104, 15),))
SKULL_WOODS_GIBDO_TORCH_EAST_SWITCH_POTS = frozenset(((144, 19), (172, 20), (144, 27), (172, 28)))
SKULL_WOODS_GIBDO_TORCH_SWITCH_POTS = (
    SKULL_WOODS_GIBDO_TORCH_HOLD_SWITCH_POTS | SKULL_WOODS_GIBDO_TORCH_EAST_SWITCH_POTS
)
POD_SOUTH_MIMICS_TAG_CHOICES = (
    TAG_NW_KILL_ENEMY_TO_OPEN,
    TAG_SWITCH_OPENS_DOOR_TOGGLE,
    TAG_SWITCH_OPENS_DOOR_HOLD,
)
POD_SOUTH_MIMICS_SWITCH_POTS = frozenset(((20, 6), (40, 6)))
ICE_PALACE_BOMB_JUMP_BASE_TAG_CHOICES = (
    TAG_SWITCH_OPENS_DOOR_TOGGLE,
    TAG_SWITCH_OPENS_DOOR_HOLD,
)
SKULL_WOODS_BIG_KEY_TAG_CHOICES = (
    TAG_SWITCH_OPENS_DOOR_HOLD,
    TAG_SWITCH_OPENS_DOOR_TOGGLE,
    TAG_SW_KILL_ENEMY_TO_OPEN,
)
SKULL_WOODS_BIG_CHEST_TAG_2_CHOICES = (
    TAG_USE_LEVER_TO_BOMB_WALL,
    TAG_USE_SWITCH_TO_BOMB_WALL,
)
SKULL_WOODS_BIG_CHEST_NORTHWEST_SWITCH_POTS = frozenset(((12, 7), (16, 7), (16, 8), (12, 12)))
GT_GAUNTLET_123_NORTHWEST_SWITCH_POTS = frozenset(((16, 5), (44, 5), (16, 11), (44, 11)))
GT_GAUNTLET_123_SOUTHWEST_SWITCH_POTS = frozenset(((12, 20), (48, 20), (12, 28), (48, 28)))
ICE_PALACE_SPIKE_ROOM_TAG_CHOICES = (
    TAG_TRIGGER_ACTIVATED_CHEST,
    TAG_SW_KILL_ENEMY_FOR_CHEST,
)
THIEVES_TOWN_WEST_ATTIC_TAG_CHOICES = (
    TAG_SWITCH_OPENS_DOOR_TOGGLE,
    TAG_SWITCH_OPENS_DOOR_HOLD,
    TAG_PULL_LEVER_TO_OPEN,
    TAG_SW_KILL_ENEMY_TO_OPEN,
)
GT_MIMICS_NORTHWEST_SWITCH_POTS = frozenset(((28, 5), (44, 8), (28, 11)))
GT_MIMICS_SOUTHEAST_SWITCH_POTS = frozenset(((98, 25),))
GT_GAUNTLET_45_VARIANTS = (
    ROOM_VARIANT_VANILLA,
    ROOM_VARIANT_TOGGLE_SWITCH,
)
GT_GAUNTLET_45_SOUTHWEST_SWITCH_POTS = frozenset(((28, 26), (32, 26), (28, 27), (32, 27)))
GT_WINDER_WARP_MAZE_TAG_1_CHOICES = (
    TAG_SWITCH_OPENS_DOOR_TOGGLE,
    TAG_SWITCH_OPENS_DOOR_HOLD,
)
GT_WINDER_WARP_MAZE_TAG_2_CHOICES = (
    TAG_TRIGGER_ACTIVATED_CHEST,
)
GT_WINDER_WARP_MAZE_SOUTHEAST_SWITCH_POTS = frozenset(((114, 20), (76, 28)))
GT_WINDER_WARP_MAZE_NORTH_SWITCH_POTS = frozenset(((44, 12), (44, 6), (112, 6)))
DESERT_WEST_ENTRANCE_TAG_CHOICES = (
    TAG_SWITCH_OPENS_DOOR_TOGGLE,
)
DESERT_WEST_ENTRANCE_PUSH_BLOCK_SOURCE = (10, 42)
DESERT_WEST_ENTRANCE_PUSH_BLOCK_TARGETS = ((6, 42),)
ROOM_OBJECT_RECORD_ADDRESSES = {
    (DESERT_WEST_ENTRANCE_ROOM_ID, (6, 36), 0x05, 1): 0xF8B60,
    (DESERT_WEST_ENTRANCE_ROOM_ID, (6, 42), 0x5E, 1): 0xF8B6C,
    (POD_TURTLE_ROOM_ID, POD_TURTLE_ROOM_PUSH_BLOCK_SOURCE, 0x00, 1): 0xFABA2,
    (POD_TURTLE_ROOM_ID, (44, 46), 0x5E, 1): 0xFAB7B,
    (POD_TURTLE_ROOM_ID, (46, 44), 0x5E, 1): 0xFAB81,
    (POD_TURTLE_ROOM_ID, (46, 52), 0x5E, 1): 0xFAB87,
    (POD_SOUTH_MIMICS_ROOM_ID, POD_SOUTH_MIMICS_PUSH_BLOCK_SOURCE, 0x05, 1): 0xFA857,
    (POD_SOUTH_MIMICS_ROOM_ID, (46, 16), 0x5E, 1): 0xFA872,
    (DESERT_FINAL_SECTION_ENTRANCE_ROOM_ID, DESERT_FINAL_SECTION_ENTRANCE_PUSH_BLOCK_SOURCE, 0x38, 1): 0xF88E1,
    (DESERT_FINAL_SECTION_ENTRANCE_ROOM_ID, (9, 44), 0x5E, 1): 0xF88D8,
    (SWAMP_HIDDEN_DOOR_ROOM_ID, SWAMP_HIDDEN_DOOR_PUSH_BLOCK_SOURCE, 0xF99, 2): 0xF9FAB,
    (SWAMP_HIDDEN_DOOR_ROOM_ID, (18, 48), 0x5E, 2): 0xF9FA5,
    (SWAMP_HIDDEN_DOOR_ROOM_ID, (24, 48), 0x5E, 2): 0xF9FA8,
    (SWAMP_HIDDEN_DOOR_ROOM_ID, (38, 48), 0x5E, 2): 0xF9FAE,
    (SWAMP_HIDDEN_DOOR_ROOM_ID, (44, 48), 0x5E, 2): 0xF9FB1,
    (SWAMP_HIDDEN_DOOR_ROOM_ID, (50, 48), 0x5E, 2): 0xF9FB4,
    (GT_MIMICS_ROOM_ID, GT_MIMICS_PUSH_BLOCK_SOURCE, 0xB8, 1): 0xFF7B8,
    (GT_MIMICS_ROOM_ID, (6, 20), 0x5E, 1): 0xFF7E5,
    (TURTLE_ROCK_CHAIN_CHOMPS_ROOM_ID, (3, 21), 0xB8, 1): 0xFDD08,
    (TURTLE_ROCK_CHAIN_CHOMPS_ROOM_ID, (21, 21), 0xB8, 1): 0xFDD0B,
    (TURTLE_ROCK_CHAIN_CHOMPS_ROOM_ID, (19, 23), 0x89, 1): 0xFDCF3,
}
ROOM_OBJECT_RECORD_SUBTYPES = {
    (DESERT_WEST_ENTRANCE_ROOM_ID, (6, 42), 0x5E, 1): 0,
    (POD_TURTLE_ROOM_ID, (44, 46), 0x5E, 1): 0,
    (POD_TURTLE_ROOM_ID, (46, 44), 0x5E, 1): 0,
    (POD_TURTLE_ROOM_ID, (46, 52), 0x5E, 1): 0,
    (DESERT_FINAL_SECTION_ENTRANCE_ROOM_ID, (9, 44), 0x5E, 1): 0,
    (SWAMP_HIDDEN_DOOR_ROOM_ID, (18, 48), 0x5E, 2): 0,
    (SWAMP_HIDDEN_DOOR_ROOM_ID, (24, 48), 0x5E, 2): 0,
    (SWAMP_HIDDEN_DOOR_ROOM_ID, (38, 48), 0x5E, 2): 0,
    (SWAMP_HIDDEN_DOOR_ROOM_ID, (44, 48), 0x5E, 2): 0,
    (SWAMP_HIDDEN_DOOR_ROOM_ID, (50, 48), 0x5E, 2): 0,
    (GT_MIMICS_ROOM_ID, (6, 20), 0x5E, 1): 0,
    (TURTLE_ROCK_CHAIN_CHOMPS_ROOM_ID, (19, 23), 0x89, 1): 0,
}
JP_PUSH_BLOCK_RECORDS = {
    (POD_TURTLE_ROOM_ID, POD_TURTLE_ROOM_PUSH_BLOCK_SOURCE): (0x26F72, 0x4000),
    (DESERT_FINAL_SECTION_ENTRANCE_ROOM_ID, DESERT_FINAL_SECTION_ENTRANCE_PUSH_BLOCK_SOURCE): (0x26ECA, 0x0000),
    (SWAMP_HIDDEN_DOOR_ROOM_ID, SWAMP_HIDDEN_DOOR_PUSH_BLOCK_SOURCE): (0x26EF6, 0x2000),
    (GT_MIMICS_ROOM_ID, GT_MIMICS_PUSH_BLOCK_SOURCE): (0x26FC2, 0x0000),
    (DESERT_WEST_ENTRANCE_ROOM_ID, DESERT_WEST_ENTRANCE_PUSH_BLOCK_SOURCE): (0x26ECE, 0x0000),
    (TURTLE_ROCK_CHAIN_CHOMPS_ROOM_ID, (11, 21)): (0x26FBA, 0x0000),
    (TURTLE_ROCK_CHAIN_CHOMPS_ROOM_ID, (19, 21)): (0x26FCE, 0x0000),
}
HOLD_SWITCH_TILE_DETECTOR_CALL_ADDRESS = 0xC570
FORCE_NON_VANILLA_PUZZLES_FOR_TESTING = True


@dataclass(frozen=True)
class PuzzleShuffleState:
    desert_map_chest_tag: int
    desert_big_chest_tag: int
    switch_replacement_item: int = POT_HEART
    desert_final_section_entrance_tag: int = TAG_SW_MOVE_BLOCK_TO_OPEN
    hera_big_key_chest_tag: int = TAG_LIGHT_TORCHES_TO_GET_CHEST
    hera_tile_room_tag: int = TAG_NW_KILL_ENEMY_TO_OPEN
    hera_big_key_chest_switch_pot: tuple[int, int] | None = None
    hera_tile_room_switch_pot: tuple[int, int] | None = None
    gt_block_puzzle_tag: int = TAG_NE_MOVE_BLOCK_TO_OPEN
    gt_big_chest_room_tag: int = TAG_SWITCH_OPENS_DOOR_HOLD
    gt_block_puzzle_switch_pot: tuple[int, int] | None = None
    gt_tile_torch_puzzle_tag: int = TAG_LIGHT_TORCHES_TO_OPEN
    gt_tile_torch_puzzle_switch_pot: tuple[int, int] | None = None
    misery_mire_dark_cane_room_tag: int = TAG_SWITCH_OPENS_DOOR_HOLD
    misery_mire_dark_cane_room_switch_pot: tuple[int, int] | None = None
    gt_torches_1_tag: int = TAG_LIGHT_TORCHES_TO_OPEN
    gt_torches_1_switch_pot: tuple[int, int] | None = None
    ice_palace_ice_floor_room_tag: int = TAG_SWITCH_OPENS_DOOR_TOGGLE
    eastern_stalfos_room_tag: int = TAG_SW_KILL_ENEMY_TO_OPEN
    eastern_stalfos_room_switch_pot: tuple[int, int] | None = None
    eastern_big_chest_room_tag: int = TAG_SWITCH_OPENS_DOOR_TOGGLE
    eastern_big_chest_left_switch_pot: tuple[int, int] | None = None
    eastern_big_chest_right_switch_pot: tuple[int, int] | None = None
    eastern_map_chest_room_tag: int = TAG_SWITCH_OPENS_DOOR_TOGGLE
    ice_palace_hidden_chest_room_tag: int = TAG_TRIGGER_ACTIVATED_CHEST
    misery_mire_bridge_chest_tag_2: int = TAG_SE_MOVE_BLOCK_TO_OPEN
    misery_mire_spike_chest_room_tag: int = TAG_TRIGGER_ACTIVATED_CHEST
    eastern_dark_square_room_tag: int = TAG_SWITCH_OPENS_DOOR_TOGGLE
    thieves_town_conveyor_toilet_tag: int = TAG_SWITCH_OPENS_DOOR_TOGGLE
    ice_palace_block_puzzle_tag: int = TAG_SWITCH_OPENS_DOOR_HOLD
    misery_mire_tile_room_tag: int = TAG_LIGHT_TORCHES_TO_OPEN
    turtle_rock_torch_puzzle_tag: int = TAG_LIGHT_TORCHES_TO_OPEN
    turtle_rock_torch_puzzle_switch_pot: tuple[int, int] | None = None
    ice_palace_hole_to_kholdstare_tag: int = TAG_PULL_LEVER_TO_OPEN
    ice_palace_hole_to_kholdstare_switch_pot: tuple[int, int] | None = None
    ice_palace_hole_to_kholdstare_pull_switch_moved: bool = False
    eastern_pre_armos_tag: int = TAG_E_KILL_ENEMY_TO_OPEN
    eastern_pre_armos_northeast_switch_pot: tuple[int, int] | None = None
    eastern_pre_armos_southeast_switch_pot: tuple[int, int] | None = None
    eastern_pre_boss_room_tag: int = TAG_SWITCH_OPENS_DOOR_TOGGLE
    eastern_switch_room_tag: int = TAG_SWITCH_OPENS_DOOR_TOGGLE
    hyrule_castle_switch_room_variant: int = ROOM_VARIANT_VANILLA
    turtle_rock_crystaroller_room_variant: int = ROOM_VARIANT_VANILLA
    swamp_floodway_room_variant: int = ROOM_VARIANT_VANILLA
    pod_turtle_room_tag: int = TAG_SW_KILL_ENEMY_TO_OPEN
    pod_mimics_moving_wall_room_tag: int = TAG_SW_KILL_ENEMY_TO_OPEN
    pod_mimics_moving_wall_switch_pot: tuple[int, int] | None = None
    pod_turtle_room_push_block_target: tuple[int, int] | None = None
    ice_palace_bomb_floor_room_variant: int = ROOM_VARIANT_VANILLA
    ice_palace_pengator_big_key_room_tag: int = TAG_SWITCH_OPENS_DOOR_TOGGLE
    turtle_rock_big_chest_room_tag: int = TAG_NW_KILL_ENEMY_TO_OPEN
    turtle_rock_big_chest_room_switch_pot: tuple[int, int] | None = None
    swamp_statue_room_tag: int = TAG_SWITCH_OPENS_DOOR_HOLD
    pod_map_chest_room_tag: int = TAG_SWITCH_OPENS_DOOR_HOLD
    pod_map_chest_room_switch_pot: tuple[int, int] | None = None
    hera_hardhat_beetles_room_tag_2: int = TAG_SE_KILL_ENEMY_TO_OPEN
    hera_hardhat_beetles_room_switch_pot: tuple[int, int] | None = None
    ice_palace_conveyor_hellway_tag: int = TAG_NE_KILL_ENEMY_TO_OPEN
    ice_palace_conveyor_hellway_switch_pot: tuple[int, int] | None = None
    ice_palace_map_room_tag: int = TAG_TRIGGER_ACTIVATED_CHEST
    thieves_town_jail_cells_tag: int = TAG_NW_KILL_ENEMY_TO_OPEN
    thieves_town_jail_cells_switch_pot: tuple[int, int] | None = None
    skull_woods_gibdo_torch_room_tag: int = TAG_LIGHT_TORCHES_TO_OPEN
    skull_woods_gibdo_torch_room_switch_pot: tuple[int, int] | None = None
    pod_south_mimics_room_tag: int = TAG_NW_KILL_ENEMY_TO_OPEN
    pod_south_mimics_room_switch_pot: tuple[int, int] | None = None
    pod_south_mimics_push_block_target: tuple[int, int] | None = None
    desert_final_section_entrance_push_block_target: tuple[int, int] | None = None
    swamp_hidden_door_push_block_target: tuple[int, int] | None = None
    ice_palace_bomb_jump_room_tag: int = TAG_SWITCH_OPENS_DOOR_TOGGLE
    skull_woods_big_key_room_tag: int = TAG_SWITCH_OPENS_DOOR_HOLD
    skull_woods_big_chest_room_tag_2: int = TAG_USE_LEVER_TO_BOMB_WALL
    skull_woods_big_chest_room_switch_pot: tuple[int, int] | None = None
    skull_woods_big_chest_rope_trap_sprite_address: int | None = None
    gt_gauntlet_123_room_variant: int = ROOM_VARIANT_VANILLA
    gt_gauntlet_123_room_northwest_switch_pot: tuple[int, int] | None = None
    gt_gauntlet_123_room_southwest_switch_pot: tuple[int, int] | None = None
    ice_palace_spike_room_tag: int = TAG_TRIGGER_ACTIVATED_CHEST
    thieves_town_west_attic_room_tag: int = TAG_SWITCH_OPENS_DOOR_TOGGLE
    gt_mimics_room_variant: int = ROOM_VARIANT_VANILLA
    gt_mimics_room_northwest_switch_pot: tuple[int, int] | None = None
    gt_mimics_room_southeast_switch_pot: tuple[int, int] | None = None
    gt_mimics_push_block_target: tuple[int, int] | None = None
    gt_gauntlet_45_room_variant: int = ROOM_VARIANT_VANILLA
    gt_gauntlet_45_room_switch_pot: tuple[int, int] | None = None
    gt_winder_warp_maze_tag_1: int = TAG_SWITCH_OPENS_DOOR_TOGGLE
    gt_winder_warp_maze_tag_2: int = TAG_TRIGGER_ACTIVATED_CHEST
    gt_winder_warp_maze_southeast_switch_pot: tuple[int, int] | None = None
    gt_winder_warp_maze_north_switch_pot: tuple[int, int] | None = None
    desert_west_entrance_tag: int = TAG_SWITCH_OPENS_DOOR_TOGGLE
    desert_west_entrance_push_block_target: tuple[int, int] | None = None
    turtle_rock_chain_chomps_push_block_source: tuple[int, int] | None = None
    turtle_rock_chain_chomps_push_block_target: tuple[int, int] | None = None


def generate_puzzle_shuffle(world: "ALTTPWorld") -> PuzzleShuffleState:
    def choice(choices, forced=None, vanilla=None):
        return _choose_puzzle_test_variant(world, choices, forced, vanilla)

    hera_big_key_chest_tag = choice(get_hera_big_key_chest_tag_choices(world))
    hera_tile_room_tag = choice(get_hera_tile_room_tag_choices(world))
    gt_block_puzzle_tag = choice(get_gt_block_puzzle_tag_choices(world))
    gt_tile_torch_puzzle_tag = choice(get_gt_tile_torch_puzzle_tag_choices(world))
    misery_mire_dark_cane_room_tag = choice(
        get_misery_mire_dark_cane_room_tag_choices(world),
        vanilla=TAG_SWITCH_OPENS_DOOR_HOLD,
    )
    gt_torches_1_tag = choice(get_gt_torches_1_tag_choices(world))
    ice_palace_ice_floor_room_tag = choice(ICE_PALACE_ICE_FLOOR_ROOM_TAG_CHOICES)
    eastern_stalfos_room_tag = choice(get_eastern_stalfos_room_tag_choices(world))
    turtle_rock_torch_puzzle_tag = choice(get_turtle_rock_torch_puzzle_tag_choices(world))
    ice_palace_hole_to_kholdstare_tag = choice(get_ice_palace_hole_to_kholdstare_tag_choices(world))
    eastern_pre_armos_tag = choice(get_eastern_pre_armos_tag_choices(world))
    turtle_rock_big_chest_room_tag = choice(TURTLE_ROCK_BIG_CHEST_TAG_CHOICES)
    thieves_town_jail_cells_tag = choice(THIEVES_TOWN_JAIL_CELLS_TAG_CHOICES)
    skull_woods_gibdo_torch_room_tag = choice(get_skull_woods_gibdo_torch_tag_choices(world))
    skull_woods_big_chest_room_switch_pot = _choose_skull_woods_big_chest_switch_pot(world)
    skull_woods_big_chest_rope_trap_sprite_address = _choose_skull_woods_big_chest_rope_trap_sprite(world)
    skull_woods_big_chest_room_tag_2 = (
        TAG_USE_SWITCH_TO_BOMB_WALL
        if (
            skull_woods_big_chest_room_switch_pot is not None
            and skull_woods_big_chest_rope_trap_sprite_address is not None
        )
        else TAG_USE_LEVER_TO_BOMB_WALL
    )
    gt_gauntlet_123_room_variant = choice(get_gt_gauntlet_123_variants(world))
    ice_palace_conveyor_hellway_tag = choice(ICE_PALACE_CONVEYOR_HELLWAY_TAG_CHOICES)
    hera_hardhat_beetles_room_tag_2 = choice(HERA_HARDHAT_BEETLES_TAG_2_CHOICES)
    pod_south_mimics_room_tag = choice(POD_SOUTH_MIMICS_TAG_CHOICES)
    pod_mimics_moving_wall_room_tag = choice(POD_MIMICS_MOVING_WALL_TAG_CHOICES)
    gt_mimics_room_variant = choice(get_gt_mimics_variants(world))
    gt_gauntlet_45_room_variant = choice(get_gt_gauntlet_45_variants(world))
    gt_winder_warp_maze_tag_1 = choice(get_gt_winder_warp_maze_tag_1_choices(world))
    gt_winder_warp_maze_tag_2 = choice(get_gt_winder_warp_maze_tag_2_choices(world))
    desert_west_entrance_tag = choice(get_desert_west_entrance_tag_choices(world))
    turtle_rock_chain_chomps_push_block_target = world.random.choice(TURTLE_ROCK_CHAIN_CHOMPS_PUSH_BLOCK_TARGETS)
    eastern_big_chest_room_tag = choice(get_eastern_big_chest_room_tag_choices(world))
    pod_map_chest_room_tag = choice(POD_MAP_CHEST_ROOM_TAG_CHOICES)
    pod_map_chest_room_switch_pot = _choose_optional_switch_pot(
        world,
        POD_MAP_CHEST_ROOM_ID,
        POD_MAP_CHEST_BOTTOM_SWITCH_POTS,
        allow_key=False,
    ) if pod_map_chest_room_tag == TAG_SWITCH_OPENS_DOOR_TOGGLE else None
    return PuzzleShuffleState(
        desert_map_chest_tag=choice(DESERT_MAP_CHEST_TAG_CHOICES, forced=TAG_LIGHT_TORCHES_TO_GET_CHEST),
        desert_big_chest_tag=choice(get_desert_big_chest_tag_choices(world)),
        switch_replacement_item=choice(_get_normal_switch_replacement_pot_items(world)),
        desert_final_section_entrance_tag=choice(get_desert_final_section_entrance_tag_choices(world)),
        hera_big_key_chest_tag=hera_big_key_chest_tag,
        hera_tile_room_tag=hera_tile_room_tag,
        hera_big_key_chest_switch_pot=_choose_switch_pot(
            world,
            HERA_TILE_ROOM_ID,
            HERA_BIG_KEY_CHEST_SWITCH_POTS,
        ) if hera_big_key_chest_tag == TAG_TRIGGER_ACTIVATED_CHEST else None,
        hera_tile_room_switch_pot=_choose_switch_pot(
            world,
            HERA_TILE_ROOM_ID,
            HERA_TILE_ROOM_WEST_SWITCH_POTS,
        ) if hera_tile_room_tag in HERA_SWITCH_TAG_CHOICES else None,
        gt_block_puzzle_tag=gt_block_puzzle_tag,
        gt_big_chest_room_tag=choice(get_gt_big_chest_room_tag_choices(world)),
        gt_block_puzzle_switch_pot=_choose_switch_pot(
            world,
            GT_BLOCK_PUZZLE_ROOM_ID,
            GT_BLOCK_PUZZLE_TOP_RIGHT_SWITCH_POTS,
            allow_key=False,
        ) if gt_block_puzzle_tag in HERA_SWITCH_TAG_CHOICES else None,
        gt_tile_torch_puzzle_tag=gt_tile_torch_puzzle_tag,
        gt_tile_torch_puzzle_switch_pot=_choose_switch_pot(
            world,
            GT_TILE_TORCH_PUZZLE_ROOM_ID,
            GT_TILE_TORCH_PUZZLE_EAST_SWITCH_POTS,
            allow_key=False,
        ) if gt_tile_torch_puzzle_tag in HERA_SWITCH_TAG_CHOICES else None,
        misery_mire_dark_cane_room_tag=misery_mire_dark_cane_room_tag,
        misery_mire_dark_cane_room_switch_pot=_choose_switch_pot(
            world,
            MISERY_MIRE_DARK_CANE_ROOM_ID,
            MISERY_MIRE_DARK_CANE_ROOM_TOGGLE_SWITCH_POTS,
            allow_key=False,
        ) if misery_mire_dark_cane_room_tag == TAG_SWITCH_OPENS_DOOR_TOGGLE else None,
        gt_torches_1_tag=gt_torches_1_tag,
        gt_torches_1_switch_pot=_choose_switch_pot(
            world,
            GT_TORCHES_1_ROOM_ID,
            GT_TORCHES_1_HOLD_SWITCH_POTS
            if gt_torches_1_tag == TAG_SWITCH_OPENS_DOOR_HOLD
            else GT_TORCHES_1_SWITCH_POTS,
            allow_key=False,
        ) if gt_torches_1_tag in HERA_SWITCH_TAG_CHOICES else None,
        ice_palace_ice_floor_room_tag=ice_palace_ice_floor_room_tag,
        eastern_stalfos_room_tag=eastern_stalfos_room_tag,
        eastern_stalfos_room_switch_pot=_choose_switch_pot(
            world,
            EASTERN_STALFOS_ROOM_ID,
            EASTERN_STALFOS_ROOM_HOLD_SWITCH_POTS,
        ) if eastern_stalfos_room_tag == TAG_SWITCH_OPENS_DOOR_HOLD else None,
        eastern_big_chest_room_tag=eastern_big_chest_room_tag,
        eastern_big_chest_left_switch_pot=_choose_switch_pot(
            world,
            EASTERN_BIG_CHEST_ROOM_ID,
            EASTERN_BIG_CHEST_LEFT_SWITCH_POTS,
            allow_key=False,
        ) if eastern_big_chest_room_tag == TAG_SWITCH_OPENS_DOOR_HOLD else None,
        eastern_big_chest_right_switch_pot=_choose_switch_pot(
            world,
            EASTERN_BIG_CHEST_ROOM_ID,
            EASTERN_BIG_CHEST_RIGHT_SWITCH_POTS,
            allow_key=False,
        ) if eastern_big_chest_room_tag == TAG_SWITCH_OPENS_DOOR_HOLD else None,
        eastern_map_chest_room_tag=choice(EASTERN_MAP_CHEST_ROOM_TAG_CHOICES),
        ice_palace_hidden_chest_room_tag=choice(ICE_PALACE_HIDDEN_CHEST_ROOM_TAG_CHOICES),
        misery_mire_bridge_chest_tag_2=choice(MISERY_MIRE_BRIDGE_CHEST_TAG_2_CHOICES),
        misery_mire_spike_chest_room_tag=choice(MISERY_MIRE_SPIKE_CHEST_TAG_CHOICES),
        eastern_dark_square_room_tag=choice(EASTERN_DARK_SQUARE_ROOM_TAG_CHOICES),
        thieves_town_conveyor_toilet_tag=choice(THIEVES_TOWN_CONVEYOR_TOILET_TAG_CHOICES),
        ice_palace_block_puzzle_tag=choice(ICE_PALACE_BLOCK_PUZZLE_TAG_CHOICES),
        misery_mire_tile_room_tag=choice(MISERY_MIRE_TILE_ROOM_TAG_CHOICES),
        turtle_rock_torch_puzzle_tag=turtle_rock_torch_puzzle_tag,
        turtle_rock_torch_puzzle_switch_pot=_choose_switch_pot(
            world,
            TURTLE_ROCK_TORCH_PUZZLE_ROOM_ID,
            TURTLE_ROCK_TORCH_PUZZLE_SWITCH_POTS,
        ) if turtle_rock_torch_puzzle_tag in HERA_SWITCH_TAG_CHOICES else None,
        ice_palace_hole_to_kholdstare_tag=ice_palace_hole_to_kholdstare_tag,
        ice_palace_hole_to_kholdstare_switch_pot=_choose_switch_pot(
            world,
            ICE_PALACE_HOLE_TO_KHOLDSTARE_ROOM_ID,
            ICE_PALACE_HOLE_TO_KHOLDSTARE_SWITCH_POTS,
        ) if ice_palace_hole_to_kholdstare_tag in HERA_SWITCH_TAG_CHOICES else None,
        ice_palace_hole_to_kholdstare_pull_switch_moved=choice((False, True)),
        eastern_pre_armos_tag=eastern_pre_armos_tag,
        eastern_pre_armos_northeast_switch_pot=_choose_switch_pot(
            world,
            EASTERN_PRE_ARMOS_ROOM_ID,
            EASTERN_PRE_ARMOS_NORTHEAST_SWITCH_POTS,
        ) if eastern_pre_armos_tag in HERA_SWITCH_TAG_CHOICES else None,
        eastern_pre_armos_southeast_switch_pot=_choose_switch_pot(
            world,
            EASTERN_PRE_ARMOS_ROOM_ID,
            EASTERN_PRE_ARMOS_SOUTHEAST_SWITCH_POTS,
        ) if eastern_pre_armos_tag in HERA_SWITCH_TAG_CHOICES else None,
        eastern_pre_boss_room_tag=choice(EASTERN_PRE_BOSS_ROOM_TAG_CHOICES),
        eastern_switch_room_tag=choice(EASTERN_SWITCH_ROOM_TAG_CHOICES),
        hyrule_castle_switch_room_variant=choice(HYRULE_CASTLE_SWITCH_ROOM_VARIANTS),
        turtle_rock_crystaroller_room_variant=choice(TURTLE_ROCK_CRYSTAROLLER_VARIANTS),
        swamp_floodway_room_variant=choice(SWAMP_FLOODWAY_VARIANTS),
        pod_turtle_room_tag=choice(POD_TURTLE_ROOM_TAG_CHOICES, forced=TAG_LIGHT_TORCHES_TO_OPEN),
        pod_mimics_moving_wall_room_tag=pod_mimics_moving_wall_room_tag,
        pod_mimics_moving_wall_switch_pot=_choose_switch_pot(
            world,
            POD_MIMICS_MOVING_WALL_ROOM_ID,
            POD_MIMICS_MOVING_WALL_SWITCH_POTS,
        ) if pod_mimics_moving_wall_room_tag in HERA_SWITCH_TAG_CHOICES else None,
        pod_turtle_room_push_block_target=choice(POD_TURTLE_ROOM_PUSH_BLOCK_TARGETS),
        ice_palace_bomb_floor_room_variant=choice(ICE_PALACE_BOMB_FLOOR_VARIANTS),
        ice_palace_pengator_big_key_room_tag=choice(ICE_PALACE_PENGATOR_BIG_KEY_TAG_CHOICES),
        turtle_rock_big_chest_room_tag=turtle_rock_big_chest_room_tag,
        turtle_rock_big_chest_room_switch_pot=_choose_switch_pot(
            world,
            TURTLE_ROCK_BIG_CHEST_ROOM_ID,
            frozenset((pot.x, pot.y) for pot in _get_current_pot_items(world, TURTLE_ROCK_BIG_CHEST_ROOM_ID)),
        ) if turtle_rock_big_chest_room_tag in HERA_SWITCH_TAG_CHOICES else None,
        swamp_statue_room_tag=choice(SWAMP_STATUE_ROOM_TAG_CHOICES),
        pod_map_chest_room_tag=pod_map_chest_room_tag,
        pod_map_chest_room_switch_pot=pod_map_chest_room_switch_pot,
        hera_hardhat_beetles_room_tag_2=hera_hardhat_beetles_room_tag_2,
        hera_hardhat_beetles_room_switch_pot=_choose_switch_pot(
            world,
            HERA_HARDHAT_BEETLES_ROOM_ID,
            HERA_HARDHAT_BEETLES_SWITCH_POTS,
        ) if hera_hardhat_beetles_room_tag_2 in HERA_SWITCH_TAG_CHOICES else None,
        ice_palace_conveyor_hellway_tag=ice_palace_conveyor_hellway_tag,
        ice_palace_conveyor_hellway_switch_pot=_choose_switch_pot(
            world,
            ICE_PALACE_CONVEYOR_HELLWAY_ROOM_ID,
            frozenset((pot.x, pot.y) for pot in _get_current_pot_items(world, ICE_PALACE_CONVEYOR_HELLWAY_ROOM_ID)),
        ) if ice_palace_conveyor_hellway_tag in HERA_SWITCH_TAG_CHOICES else None,
        ice_palace_map_room_tag=choice(ICE_PALACE_MAP_ROOM_TAG_CHOICES),
        thieves_town_jail_cells_tag=thieves_town_jail_cells_tag,
        thieves_town_jail_cells_switch_pot=_choose_switch_pot(
            world,
            THIEVES_TOWN_JAIL_CELLS_ROOM_ID,
            THIEVES_TOWN_JAIL_CELLS_NORTHWEST_SWITCH_POTS,
        ) if thieves_town_jail_cells_tag in HERA_SWITCH_TAG_CHOICES else None,
        skull_woods_gibdo_torch_room_tag=skull_woods_gibdo_torch_room_tag,
        skull_woods_gibdo_torch_room_switch_pot=_choose_switch_pot(
            world,
            SKULL_WOODS_GIBDO_TORCH_ROOM_ID,
            SKULL_WOODS_GIBDO_TORCH_HOLD_SWITCH_POTS
            if skull_woods_gibdo_torch_room_tag == TAG_SWITCH_OPENS_DOOR_HOLD
            else SKULL_WOODS_GIBDO_TORCH_SWITCH_POTS,
            allow_key=False,
        ) if skull_woods_gibdo_torch_room_tag in HERA_SWITCH_TAG_CHOICES else None,
        pod_south_mimics_room_tag=pod_south_mimics_room_tag,
        pod_south_mimics_room_switch_pot=_choose_switch_pot(
            world,
            POD_SOUTH_MIMICS_ROOM_ID,
            POD_SOUTH_MIMICS_SWITCH_POTS,
        ) if pod_south_mimics_room_tag in HERA_SWITCH_TAG_CHOICES else None,
        pod_south_mimics_push_block_target=None,
        desert_final_section_entrance_push_block_target=choice(DESERT_FINAL_SECTION_ENTRANCE_PUSH_BLOCK_TARGETS),
        swamp_hidden_door_push_block_target=choice(SWAMP_HIDDEN_DOOR_PUSH_BLOCK_TARGETS),
        ice_palace_bomb_jump_room_tag=choice(get_ice_palace_bomb_jump_room_tag_choices(world)),
        skull_woods_big_key_room_tag=choice(SKULL_WOODS_BIG_KEY_TAG_CHOICES),
        skull_woods_big_chest_room_tag_2=skull_woods_big_chest_room_tag_2,
        skull_woods_big_chest_room_switch_pot=skull_woods_big_chest_room_switch_pot
        if skull_woods_big_chest_room_tag_2 == TAG_USE_SWITCH_TO_BOMB_WALL else None,
        skull_woods_big_chest_rope_trap_sprite_address=skull_woods_big_chest_rope_trap_sprite_address
        if skull_woods_big_chest_room_tag_2 == TAG_USE_SWITCH_TO_BOMB_WALL else None,
        gt_gauntlet_123_room_variant=gt_gauntlet_123_room_variant,
        gt_gauntlet_123_room_northwest_switch_pot=_choose_switch_pot(
            world,
            GT_GAUNTLET_123_ROOM_ID,
            GT_GAUNTLET_123_NORTHWEST_SWITCH_POTS,
        ) if gt_gauntlet_123_room_variant == ROOM_VARIANT_TOGGLE_SWITCH else None,
        gt_gauntlet_123_room_southwest_switch_pot=_choose_switch_pot(
            world,
            GT_GAUNTLET_123_ROOM_ID,
            GT_GAUNTLET_123_SOUTHWEST_SWITCH_POTS,
        ) if gt_gauntlet_123_room_variant in (ROOM_VARIANT_TOGGLE_SWITCH, ROOM_VARIANT_KILL_ENEMIES) else None,
        ice_palace_spike_room_tag=choice(ICE_PALACE_SPIKE_ROOM_TAG_CHOICES),
        thieves_town_west_attic_room_tag=choice(THIEVES_TOWN_WEST_ATTIC_TAG_CHOICES),
        gt_mimics_room_variant=gt_mimics_room_variant,
        gt_mimics_room_northwest_switch_pot=_choose_switch_pot(
            world,
            GT_MIMICS_ROOM_ID,
            GT_MIMICS_NORTHWEST_SWITCH_POTS,
        ) if gt_mimics_room_variant in (2, 4) else None,
        gt_mimics_room_southeast_switch_pot=_choose_switch_pot(
            world,
            GT_MIMICS_ROOM_ID,
            GT_MIMICS_SOUTHEAST_SWITCH_POTS,
        ) if gt_mimics_room_variant == 4 else None,
        gt_mimics_push_block_target=choice(GT_MIMICS_PUSH_BLOCK_TARGETS),
        gt_gauntlet_45_room_variant=gt_gauntlet_45_room_variant,
        gt_gauntlet_45_room_switch_pot=_choose_switch_pot(
            world,
            GT_GAUNTLET_45_ROOM_ID,
            GT_GAUNTLET_45_SOUTHWEST_SWITCH_POTS,
        ) if gt_gauntlet_45_room_variant == ROOM_VARIANT_TOGGLE_SWITCH else None,
        gt_winder_warp_maze_tag_1=gt_winder_warp_maze_tag_1,
        gt_winder_warp_maze_tag_2=gt_winder_warp_maze_tag_2,
        gt_winder_warp_maze_southeast_switch_pot=_choose_switch_pot(
            world,
            GT_WINDER_WARP_MAZE_ROOM_ID,
            GT_WINDER_WARP_MAZE_SOUTHEAST_SWITCH_POTS,
        ) if gt_winder_warp_maze_tag_1 in HERA_SWITCH_TAG_CHOICES else None,
        gt_winder_warp_maze_north_switch_pot=_choose_switch_pot(
            world,
            GT_WINDER_WARP_MAZE_ROOM_ID,
            GT_WINDER_WARP_MAZE_NORTH_SWITCH_POTS,
        ) if gt_winder_warp_maze_tag_2 == TAG_TRIGGER_ACTIVATED_CHEST else None,
        desert_west_entrance_tag=desert_west_entrance_tag,
        desert_west_entrance_push_block_target=choice(DESERT_WEST_ENTRANCE_PUSH_BLOCK_TARGETS),
        turtle_rock_chain_chomps_push_block_source=choice(TURTLE_ROCK_CHAIN_CHOMPS_PUSH_BLOCK_SOURCES)
        if turtle_rock_chain_chomps_push_block_target is not None else None,
        turtle_rock_chain_chomps_push_block_target=turtle_rock_chain_chomps_push_block_target,
    )


def _choose_puzzle_test_variant(world: "ALTTPWorld", choices, forced=None, vanilla=None):
    choices = tuple(choices)
    if forced is not None and forced in choices:
        return forced
    if not FORCE_NON_VANILLA_PUZZLES_FOR_TESTING or len(choices) < 2:
        return world.random.choice(choices)
    if vanilla is not None:
        non_vanilla_choices = tuple(choice for choice in choices if choice != vanilla)
        if non_vanilla_choices:
            return world.random.choice(non_vanilla_choices)
    return world.random.choice(choices[1:])


def encode_puzzle_shuffle(state: PuzzleShuffleState | None) -> dict[str, int] | None:
    if state is None:
        return None
    return {
        "desert_map_chest_tag": state.desert_map_chest_tag,
        "desert_big_chest_tag": state.desert_big_chest_tag,
        "switch_replacement_item": state.switch_replacement_item,
        "desert_final_section_entrance_tag": state.desert_final_section_entrance_tag,
        "hera_big_key_chest_tag": state.hera_big_key_chest_tag,
        "hera_tile_room_tag": state.hera_tile_room_tag,
        "hera_big_key_chest_switch_pot": state.hera_big_key_chest_switch_pot,
        "hera_tile_room_switch_pot": state.hera_tile_room_switch_pot,
        "gt_block_puzzle_tag": state.gt_block_puzzle_tag,
        "gt_big_chest_room_tag": state.gt_big_chest_room_tag,
        "gt_block_puzzle_switch_pot": state.gt_block_puzzle_switch_pot,
        "gt_tile_torch_puzzle_tag": state.gt_tile_torch_puzzle_tag,
        "gt_tile_torch_puzzle_switch_pot": state.gt_tile_torch_puzzle_switch_pot,
        "misery_mire_dark_cane_room_tag": state.misery_mire_dark_cane_room_tag,
        "misery_mire_dark_cane_room_switch_pot": state.misery_mire_dark_cane_room_switch_pot,
        "gt_torches_1_tag": state.gt_torches_1_tag,
        "gt_torches_1_switch_pot": state.gt_torches_1_switch_pot,
        "ice_palace_ice_floor_room_tag": state.ice_palace_ice_floor_room_tag,
        "eastern_stalfos_room_tag": state.eastern_stalfos_room_tag,
        "eastern_stalfos_room_switch_pot": state.eastern_stalfos_room_switch_pot,
        "eastern_big_chest_room_tag": state.eastern_big_chest_room_tag,
        "eastern_big_chest_left_switch_pot": state.eastern_big_chest_left_switch_pot,
        "eastern_big_chest_right_switch_pot": state.eastern_big_chest_right_switch_pot,
        "eastern_map_chest_room_tag": state.eastern_map_chest_room_tag,
        "ice_palace_hidden_chest_room_tag": state.ice_palace_hidden_chest_room_tag,
        "misery_mire_bridge_chest_tag_2": state.misery_mire_bridge_chest_tag_2,
        "misery_mire_spike_chest_room_tag": state.misery_mire_spike_chest_room_tag,
        "eastern_dark_square_room_tag": state.eastern_dark_square_room_tag,
        "thieves_town_conveyor_toilet_tag": state.thieves_town_conveyor_toilet_tag,
        "ice_palace_block_puzzle_tag": state.ice_palace_block_puzzle_tag,
        "misery_mire_tile_room_tag": state.misery_mire_tile_room_tag,
        "turtle_rock_torch_puzzle_tag": state.turtle_rock_torch_puzzle_tag,
        "turtle_rock_torch_puzzle_switch_pot": state.turtle_rock_torch_puzzle_switch_pot,
        "ice_palace_hole_to_kholdstare_tag": state.ice_palace_hole_to_kholdstare_tag,
        "ice_palace_hole_to_kholdstare_switch_pot": state.ice_palace_hole_to_kholdstare_switch_pot,
        "ice_palace_hole_to_kholdstare_pull_switch_moved": state.ice_palace_hole_to_kholdstare_pull_switch_moved,
        "eastern_pre_armos_tag": state.eastern_pre_armos_tag,
        "eastern_pre_armos_northeast_switch_pot": state.eastern_pre_armos_northeast_switch_pot,
        "eastern_pre_armos_southeast_switch_pot": state.eastern_pre_armos_southeast_switch_pot,
        "eastern_pre_boss_room_tag": state.eastern_pre_boss_room_tag,
        "eastern_switch_room_tag": state.eastern_switch_room_tag,
        "hyrule_castle_switch_room_variant": state.hyrule_castle_switch_room_variant,
        "turtle_rock_crystaroller_room_variant": state.turtle_rock_crystaroller_room_variant,
        "swamp_floodway_room_variant": state.swamp_floodway_room_variant,
        "pod_turtle_room_tag": state.pod_turtle_room_tag,
        "pod_mimics_moving_wall_room_tag": state.pod_mimics_moving_wall_room_tag,
        "pod_mimics_moving_wall_switch_pot": state.pod_mimics_moving_wall_switch_pot,
        "pod_turtle_room_push_block_target": state.pod_turtle_room_push_block_target,
        "ice_palace_bomb_floor_room_variant": state.ice_palace_bomb_floor_room_variant,
        "ice_palace_pengator_big_key_room_tag": state.ice_palace_pengator_big_key_room_tag,
        "turtle_rock_big_chest_room_tag": state.turtle_rock_big_chest_room_tag,
        "turtle_rock_big_chest_room_switch_pot": state.turtle_rock_big_chest_room_switch_pot,
        "swamp_statue_room_tag": state.swamp_statue_room_tag,
        "pod_map_chest_room_tag": state.pod_map_chest_room_tag,
        "pod_map_chest_room_switch_pot": state.pod_map_chest_room_switch_pot,
        "hera_hardhat_beetles_room_tag_2": state.hera_hardhat_beetles_room_tag_2,
        "hera_hardhat_beetles_room_switch_pot": state.hera_hardhat_beetles_room_switch_pot,
        "ice_palace_conveyor_hellway_tag": state.ice_palace_conveyor_hellway_tag,
        "ice_palace_conveyor_hellway_switch_pot": state.ice_palace_conveyor_hellway_switch_pot,
        "ice_palace_map_room_tag": state.ice_palace_map_room_tag,
        "thieves_town_jail_cells_tag": state.thieves_town_jail_cells_tag,
        "thieves_town_jail_cells_switch_pot": state.thieves_town_jail_cells_switch_pot,
        "skull_woods_gibdo_torch_room_tag": state.skull_woods_gibdo_torch_room_tag,
        "skull_woods_gibdo_torch_room_switch_pot": state.skull_woods_gibdo_torch_room_switch_pot,
        "pod_south_mimics_room_tag": state.pod_south_mimics_room_tag,
        "pod_south_mimics_room_switch_pot": state.pod_south_mimics_room_switch_pot,
        "pod_south_mimics_push_block_target": state.pod_south_mimics_push_block_target,
        "desert_final_section_entrance_push_block_target": state.desert_final_section_entrance_push_block_target,
        "swamp_hidden_door_push_block_target": state.swamp_hidden_door_push_block_target,
        "ice_palace_bomb_jump_room_tag": state.ice_palace_bomb_jump_room_tag,
        "skull_woods_big_key_room_tag": state.skull_woods_big_key_room_tag,
        "skull_woods_big_chest_room_tag_2": state.skull_woods_big_chest_room_tag_2,
        "skull_woods_big_chest_room_switch_pot": state.skull_woods_big_chest_room_switch_pot,
        "skull_woods_big_chest_rope_trap_sprite_address": state.skull_woods_big_chest_rope_trap_sprite_address,
        "gt_gauntlet_123_room_variant": state.gt_gauntlet_123_room_variant,
        "gt_gauntlet_123_room_northwest_switch_pot": state.gt_gauntlet_123_room_northwest_switch_pot,
        "gt_gauntlet_123_room_southwest_switch_pot": state.gt_gauntlet_123_room_southwest_switch_pot,
        "ice_palace_spike_room_tag": state.ice_palace_spike_room_tag,
        "thieves_town_west_attic_room_tag": state.thieves_town_west_attic_room_tag,
        "gt_mimics_room_variant": state.gt_mimics_room_variant,
        "gt_mimics_room_northwest_switch_pot": state.gt_mimics_room_northwest_switch_pot,
        "gt_mimics_room_southeast_switch_pot": state.gt_mimics_room_southeast_switch_pot,
        "gt_mimics_push_block_target": state.gt_mimics_push_block_target,
        "gt_gauntlet_45_room_variant": state.gt_gauntlet_45_room_variant,
        "gt_gauntlet_45_room_switch_pot": state.gt_gauntlet_45_room_switch_pot,
        "gt_winder_warp_maze_tag_1": state.gt_winder_warp_maze_tag_1,
        "gt_winder_warp_maze_tag_2": state.gt_winder_warp_maze_tag_2,
        "gt_winder_warp_maze_southeast_switch_pot": state.gt_winder_warp_maze_southeast_switch_pot,
        "gt_winder_warp_maze_north_switch_pot": state.gt_winder_warp_maze_north_switch_pot,
        "desert_west_entrance_tag": state.desert_west_entrance_tag,
        "desert_west_entrance_push_block_target": state.desert_west_entrance_push_block_target,
        "turtle_rock_chain_chomps_push_block_source": state.turtle_rock_chain_chomps_push_block_source,
        "turtle_rock_chain_chomps_push_block_target": state.turtle_rock_chain_chomps_push_block_target,
    }


def decode_puzzle_shuffle(data: dict[str, int] | None) -> PuzzleShuffleState | None:
    if not data:
        return None
    return PuzzleShuffleState(
        desert_map_chest_tag=int(data["desert_map_chest_tag"]),
        desert_big_chest_tag=int(data["desert_big_chest_tag"]),
        switch_replacement_item=int(data.get("switch_replacement_item", POT_HEART)),
        desert_final_section_entrance_tag=int(
            data.get("desert_final_section_entrance_tag", TAG_SW_MOVE_BLOCK_TO_OPEN)
        ),
        hera_big_key_chest_tag=int(data.get("hera_big_key_chest_tag", TAG_LIGHT_TORCHES_TO_GET_CHEST)),
        hera_tile_room_tag=int(data.get("hera_tile_room_tag", TAG_NW_KILL_ENEMY_TO_OPEN)),
        hera_big_key_chest_switch_pot=_decode_position(data.get("hera_big_key_chest_switch_pot")),
        hera_tile_room_switch_pot=_decode_position(data.get("hera_tile_room_switch_pot")),
        gt_block_puzzle_tag=int(data.get("gt_block_puzzle_tag", TAG_NE_MOVE_BLOCK_TO_OPEN)),
        gt_big_chest_room_tag=int(data.get("gt_big_chest_room_tag", TAG_SWITCH_OPENS_DOOR_HOLD)),
        gt_block_puzzle_switch_pot=_decode_position(data.get("gt_block_puzzle_switch_pot")),
        gt_tile_torch_puzzle_tag=int(data.get("gt_tile_torch_puzzle_tag", TAG_LIGHT_TORCHES_TO_OPEN)),
        gt_tile_torch_puzzle_switch_pot=_decode_position(data.get("gt_tile_torch_puzzle_switch_pot")),
        misery_mire_dark_cane_room_tag=int(data.get("misery_mire_dark_cane_room_tag", TAG_SWITCH_OPENS_DOOR_HOLD)),
        misery_mire_dark_cane_room_switch_pot=_decode_position(
            data.get("misery_mire_dark_cane_room_switch_pot")
        ),
        gt_torches_1_tag=int(data.get("gt_torches_1_tag", TAG_LIGHT_TORCHES_TO_OPEN)),
        gt_torches_1_switch_pot=_decode_position(data.get("gt_torches_1_switch_pot")),
        ice_palace_ice_floor_room_tag=int(data.get("ice_palace_ice_floor_room_tag", TAG_SWITCH_OPENS_DOOR_TOGGLE)),
        eastern_stalfos_room_tag=int(data.get("eastern_stalfos_room_tag", TAG_SW_KILL_ENEMY_TO_OPEN)),
        eastern_stalfos_room_switch_pot=_decode_position(data.get("eastern_stalfos_room_switch_pot")),
        eastern_big_chest_room_tag=int(data.get("eastern_big_chest_room_tag", TAG_SWITCH_OPENS_DOOR_TOGGLE)),
        eastern_big_chest_left_switch_pot=_decode_position(data.get("eastern_big_chest_left_switch_pot")),
        eastern_big_chest_right_switch_pot=_decode_position(data.get("eastern_big_chest_right_switch_pot")),
        eastern_map_chest_room_tag=int(data.get("eastern_map_chest_room_tag", TAG_SWITCH_OPENS_DOOR_TOGGLE)),
        ice_palace_hidden_chest_room_tag=int(data.get("ice_palace_hidden_chest_room_tag", TAG_TRIGGER_ACTIVATED_CHEST)),
        misery_mire_bridge_chest_tag_2=int(data.get("misery_mire_bridge_chest_tag_2", TAG_SE_MOVE_BLOCK_TO_OPEN)),
        misery_mire_spike_chest_room_tag=int(data.get("misery_mire_spike_chest_room_tag", TAG_TRIGGER_ACTIVATED_CHEST)),
        eastern_dark_square_room_tag=int(data.get("eastern_dark_square_room_tag", TAG_SWITCH_OPENS_DOOR_TOGGLE)),
        thieves_town_conveyor_toilet_tag=int(data.get("thieves_town_conveyor_toilet_tag", TAG_SWITCH_OPENS_DOOR_TOGGLE)),
        ice_palace_block_puzzle_tag=int(data.get("ice_palace_block_puzzle_tag", TAG_SWITCH_OPENS_DOOR_HOLD)),
        misery_mire_tile_room_tag=int(data.get("misery_mire_tile_room_tag", TAG_LIGHT_TORCHES_TO_OPEN)),
        turtle_rock_torch_puzzle_tag=int(data.get("turtle_rock_torch_puzzle_tag", TAG_LIGHT_TORCHES_TO_OPEN)),
        turtle_rock_torch_puzzle_switch_pot=_decode_position(data.get("turtle_rock_torch_puzzle_switch_pot")),
        ice_palace_hole_to_kholdstare_tag=int(data.get("ice_palace_hole_to_kholdstare_tag", TAG_PULL_LEVER_TO_OPEN)),
        ice_palace_hole_to_kholdstare_switch_pot=_decode_position(data.get("ice_palace_hole_to_kholdstare_switch_pot")),
        ice_palace_hole_to_kholdstare_pull_switch_moved=bool(
            data.get("ice_palace_hole_to_kholdstare_pull_switch_moved", False)
        ),
        eastern_pre_armos_tag=int(data.get("eastern_pre_armos_tag", TAG_E_KILL_ENEMY_TO_OPEN)),
        eastern_pre_armos_northeast_switch_pot=_decode_position(data.get("eastern_pre_armos_northeast_switch_pot")),
        eastern_pre_armos_southeast_switch_pot=_decode_position(data.get("eastern_pre_armos_southeast_switch_pot")),
        eastern_pre_boss_room_tag=int(data.get("eastern_pre_boss_room_tag", TAG_SWITCH_OPENS_DOOR_TOGGLE)),
        eastern_switch_room_tag=int(data.get("eastern_switch_room_tag", TAG_SWITCH_OPENS_DOOR_TOGGLE)),
        hyrule_castle_switch_room_variant=int(data.get("hyrule_castle_switch_room_variant", ROOM_VARIANT_VANILLA)),
        turtle_rock_crystaroller_room_variant=int(data.get("turtle_rock_crystaroller_room_variant", ROOM_VARIANT_VANILLA)),
        swamp_floodway_room_variant=int(data.get("swamp_floodway_room_variant", ROOM_VARIANT_VANILLA)),
        pod_turtle_room_tag=int(data.get("pod_turtle_room_tag", TAG_SW_KILL_ENEMY_TO_OPEN)),
        pod_mimics_moving_wall_room_tag=int(data.get("pod_mimics_moving_wall_room_tag", TAG_SW_KILL_ENEMY_TO_OPEN)),
        pod_mimics_moving_wall_switch_pot=_decode_position(data.get("pod_mimics_moving_wall_switch_pot")),
        pod_turtle_room_push_block_target=_decode_position(data.get("pod_turtle_room_push_block_target")),
        ice_palace_bomb_floor_room_variant=int(data.get("ice_palace_bomb_floor_room_variant", ROOM_VARIANT_VANILLA)),
        ice_palace_pengator_big_key_room_tag=int(data.get("ice_palace_pengator_big_key_room_tag", TAG_SWITCH_OPENS_DOOR_TOGGLE)),
        turtle_rock_big_chest_room_tag=int(data.get("turtle_rock_big_chest_room_tag", TAG_NW_KILL_ENEMY_TO_OPEN)),
        turtle_rock_big_chest_room_switch_pot=_decode_position(data.get("turtle_rock_big_chest_room_switch_pot")),
        swamp_statue_room_tag=int(data.get("swamp_statue_room_tag", TAG_SWITCH_OPENS_DOOR_HOLD)),
        pod_map_chest_room_tag=int(data.get("pod_map_chest_room_tag", TAG_SWITCH_OPENS_DOOR_HOLD)),
        pod_map_chest_room_switch_pot=_decode_position(data.get("pod_map_chest_room_switch_pot")),
        hera_hardhat_beetles_room_tag_2=int(data.get("hera_hardhat_beetles_room_tag_2", TAG_SE_KILL_ENEMY_TO_OPEN)),
        hera_hardhat_beetles_room_switch_pot=_decode_position(data.get("hera_hardhat_beetles_room_switch_pot")),
        ice_palace_conveyor_hellway_tag=int(data.get("ice_palace_conveyor_hellway_tag", TAG_NE_KILL_ENEMY_TO_OPEN)),
        ice_palace_conveyor_hellway_switch_pot=_decode_position(data.get("ice_palace_conveyor_hellway_switch_pot")),
        ice_palace_map_room_tag=int(data.get("ice_palace_map_room_tag", TAG_TRIGGER_ACTIVATED_CHEST)),
        thieves_town_jail_cells_tag=int(data.get("thieves_town_jail_cells_tag", TAG_NW_KILL_ENEMY_TO_OPEN)),
        thieves_town_jail_cells_switch_pot=_decode_position(data.get("thieves_town_jail_cells_switch_pot")),
        skull_woods_gibdo_torch_room_tag=int(data.get("skull_woods_gibdo_torch_room_tag", TAG_LIGHT_TORCHES_TO_OPEN)),
        skull_woods_gibdo_torch_room_switch_pot=_decode_position(data.get("skull_woods_gibdo_torch_room_switch_pot")),
        pod_south_mimics_room_tag=int(data.get("pod_south_mimics_room_tag", TAG_NW_KILL_ENEMY_TO_OPEN)),
        pod_south_mimics_room_switch_pot=_decode_position(data.get("pod_south_mimics_room_switch_pot")),
        pod_south_mimics_push_block_target=_decode_position(data.get("pod_south_mimics_push_block_target")),
        desert_final_section_entrance_push_block_target=_decode_position(
            data.get("desert_final_section_entrance_push_block_target")
        ),
        swamp_hidden_door_push_block_target=_decode_position(data.get("swamp_hidden_door_push_block_target")),
        ice_palace_bomb_jump_room_tag=int(data.get("ice_palace_bomb_jump_room_tag", TAG_SWITCH_OPENS_DOOR_TOGGLE)),
        skull_woods_big_key_room_tag=int(data.get("skull_woods_big_key_room_tag", TAG_SWITCH_OPENS_DOOR_HOLD)),
        skull_woods_big_chest_room_tag_2=int(data.get("skull_woods_big_chest_room_tag_2", TAG_USE_LEVER_TO_BOMB_WALL)),
        skull_woods_big_chest_room_switch_pot=_decode_position(data.get("skull_woods_big_chest_room_switch_pot")),
        skull_woods_big_chest_rope_trap_sprite_address=(
            int(data["skull_woods_big_chest_rope_trap_sprite_address"])
            if data.get("skull_woods_big_chest_rope_trap_sprite_address") is not None else None
        ),
        gt_gauntlet_123_room_variant=int(data.get("gt_gauntlet_123_room_variant", ROOM_VARIANT_VANILLA)),
        gt_gauntlet_123_room_northwest_switch_pot=_decode_position(data.get("gt_gauntlet_123_room_northwest_switch_pot")),
        gt_gauntlet_123_room_southwest_switch_pot=_decode_position(data.get("gt_gauntlet_123_room_southwest_switch_pot")),
        ice_palace_spike_room_tag=int(data.get("ice_palace_spike_room_tag", TAG_TRIGGER_ACTIVATED_CHEST)),
        thieves_town_west_attic_room_tag=int(data.get("thieves_town_west_attic_room_tag", TAG_SWITCH_OPENS_DOOR_TOGGLE)),
        gt_mimics_room_variant=int(data.get("gt_mimics_room_variant", ROOM_VARIANT_VANILLA)),
        gt_mimics_room_northwest_switch_pot=_decode_position(data.get("gt_mimics_room_northwest_switch_pot")),
        gt_mimics_room_southeast_switch_pot=_decode_position(data.get("gt_mimics_room_southeast_switch_pot")),
        gt_mimics_push_block_target=_decode_position(data.get("gt_mimics_push_block_target")),
        gt_gauntlet_45_room_variant=int(data.get("gt_gauntlet_45_room_variant", ROOM_VARIANT_VANILLA)),
        gt_gauntlet_45_room_switch_pot=_decode_position(data.get("gt_gauntlet_45_room_switch_pot")),
        gt_winder_warp_maze_tag_1=int(data.get("gt_winder_warp_maze_tag_1", TAG_SWITCH_OPENS_DOOR_TOGGLE)),
        gt_winder_warp_maze_tag_2=int(data.get("gt_winder_warp_maze_tag_2", TAG_TRIGGER_ACTIVATED_CHEST)),
        gt_winder_warp_maze_southeast_switch_pot=_decode_position(data.get("gt_winder_warp_maze_southeast_switch_pot")),
        gt_winder_warp_maze_north_switch_pot=_decode_position(data.get("gt_winder_warp_maze_north_switch_pot")),
        desert_west_entrance_tag=int(data.get("desert_west_entrance_tag", TAG_SWITCH_OPENS_DOOR_TOGGLE)),
        desert_west_entrance_push_block_target=_decode_position(data.get("desert_west_entrance_push_block_target")),
        turtle_rock_chain_chomps_push_block_source=_decode_position(
            data.get("turtle_rock_chain_chomps_push_block_source")
        ),
        turtle_rock_chain_chomps_push_block_target=_decode_position(
            data.get("turtle_rock_chain_chomps_push_block_target")
        ),
    )


def desert_map_chest_uses_switch(state: PuzzleShuffleState | None) -> bool:
    return state is None or state.desert_map_chest_tag == TAG_TRIGGER_ACTIVATED_CHEST


def get_desert_big_chest_tag_choices(world: "ALTTPWorld") -> tuple[int, ...]:
    choices = list(DESERT_BIG_CHEST_BASE_TAG_CHOICES)
    if desert_big_chest_has_killable_bottom_left_enemy(world):
        choices.append(TAG_SW_KILL_ENEMY_TO_OPEN)
    return tuple(choices)


def desert_big_chest_has_killable_bottom_left_enemy(world: "ALTTPWorld") -> bool:
    from .StateHelpers import _enemy_requirement_counts_for_room_clear

    return any(
        _enemy_requirement_counts_for_room_clear(enemy)
        for enemy in get_enemy_clear_target_enemies(world, DESERT_BIG_CHEST_BOTTOM_LEFT)
    )


def get_desert_final_section_entrance_tag_choices(world: "ALTTPWorld") -> tuple[int, ...]:
    choices = list(DESERT_FINAL_SECTION_ENTRANCE_BASE_TAG_CHOICES)
    if _has_randomized_killable_enemy(
        world,
        DESERT_FINAL_SECTION_ENTRANCE_ROOM_ID,
        DESERT_FINAL_SECTION_ENTRANCE_SOUTHWEST,
    ):
        choices.append(TAG_SW_KILL_ENEMY_TO_OPEN)
    return tuple(choices)


def get_hera_big_key_chest_tag_choices(world: "ALTTPWorld") -> tuple[int, ...]:
    choices = list(HERA_BIG_KEY_CHEST_BASE_TAG_CHOICES)
    if _filled_pot_positions_in_target(world, HERA_TILE_ROOM_ID, HERA_BIG_KEY_CHEST_SWITCH_POTS):
        choices.append(TAG_TRIGGER_ACTIVATED_CHEST)
    return tuple(choices)


def get_hera_tile_room_tag_choices(world: "ALTTPWorld") -> tuple[int, ...]:
    choices = list(HERA_TILE_ROOM_BASE_TAG_2_CHOICES)
    # Do not enable NW pot-switch variants for now. The crystal switch tile
    # layout can trap the player behind a shut door, and keeping NW kill-open
    # forces the flying floor tile overlord to finish before the room opens.
    # A higher-difficulty puzzle option may re-enable this later.
    # if _filled_pot_positions_in_target(world, HERA_TILE_ROOM_ID, HERA_TILE_ROOM_WEST_SWITCH_POTS):
    #     choices.extend(HERA_SWITCH_TAG_CHOICES)
    return tuple(choices)


def get_gt_block_puzzle_tag_choices(world: "ALTTPWorld") -> tuple[int, ...]:
    choices = [TAG_NE_MOVE_BLOCK_TO_OPEN, TAG_NE_KILL_ENEMY_TO_OPEN]
    if _filled_pot_positions_in_target(
        world,
        GT_BLOCK_PUZZLE_ROOM_ID,
        GT_BLOCK_PUZZLE_TOP_RIGHT_SWITCH_POTS,
        allow_key=False,
    ):
        choices.extend(HERA_SWITCH_TAG_CHOICES)
    return tuple(choices)


def get_gt_tile_torch_puzzle_tag_choices(world: "ALTTPWorld") -> tuple[int, ...]:
    choices = list(GT_TILE_TORCH_PUZZLE_TAG_CHOICES)
    if _filled_pot_positions_in_target(
        world,
        GT_TILE_TORCH_PUZZLE_ROOM_ID,
        GT_TILE_TORCH_PUZZLE_EAST_SWITCH_POTS,
        allow_key=False,
    ):
        choices.extend(HERA_SWITCH_TAG_CHOICES)
    return tuple(choices)


def get_gt_torches_1_tag_choices(world: "ALTTPWorld") -> tuple[int, ...]:
    choices = list(GT_TORCHES_1_TAG_CHOICES)
    if _filled_pot_positions_in_target(
        world,
        GT_TORCHES_1_ROOM_ID,
        GT_TORCHES_1_SWITCH_POTS,
        allow_key=False,
    ):
        choices.append(TAG_SWITCH_OPENS_DOOR_TOGGLE)
    if _filled_pot_positions_in_target(
        world,
        GT_TORCHES_1_ROOM_ID,
        GT_TORCHES_1_HOLD_SWITCH_POTS,
        allow_key=False,
    ):
        choices.append(TAG_SWITCH_OPENS_DOOR_HOLD)
    return tuple(choices)


def get_misery_mire_dark_cane_room_tag_choices(world: "ALTTPWorld") -> tuple[int, ...]:
    choices = [TAG_SWITCH_OPENS_DOOR_TOGGLE, TAG_N_KILL_ENEMY_FOR_CHEST]
    if _filled_pot_positions_in_target(
        world,
        MISERY_MIRE_DARK_CANE_ROOM_ID,
        frozenset((MISERY_MIRE_DARK_CANE_ROOM_VANILLA_SWITCH_POT,)),
        allow_key=False,
    ):
        choices.insert(0, TAG_SWITCH_OPENS_DOOR_HOLD)
    return tuple(choices)


def get_gt_big_chest_room_tag_choices(world: "ALTTPWorld") -> tuple[int, ...]:
    choices = [TAG_SWITCH_OPENS_DOOR_HOLD, TAG_PULL_LEVER_TO_OPEN, TAG_SWITCH_OPENS_DOOR_TOGGLE]
    if _has_randomized_killable_enemy(world, GT_BIG_CHEST_ROOM_ID, GANONS_TOWER_BIG_CHEST_ROOM_NORTHEAST):
        choices.append(TAG_NE_KILL_ENEMY_TO_OPEN)
    return tuple(choices)


def get_eastern_stalfos_room_tag_choices(world: "ALTTPWorld") -> tuple[int, ...]:
    choices = [TAG_SW_KILL_ENEMY_TO_OPEN, TAG_SWITCH_OPENS_DOOR_TOGGLE]
    if _filled_pot_positions_in_target(world, EASTERN_STALFOS_ROOM_ID, EASTERN_STALFOS_ROOM_HOLD_SWITCH_POTS):
        choices.append(TAG_SWITCH_OPENS_DOOR_HOLD)
    return tuple(choices)


def get_gt_gauntlet_123_variants(world: "ALTTPWorld") -> tuple[int, ...]:
    choices = [ROOM_VARIANT_VANILLA]
    has_northwest_switch_pot = bool(_filled_pot_positions_in_target(
        world,
        GT_GAUNTLET_123_ROOM_ID,
        GT_GAUNTLET_123_NORTHWEST_SWITCH_POTS,
    ))
    has_southwest_switch_pot = bool(_filled_pot_positions_in_target(
        world,
        GT_GAUNTLET_123_ROOM_ID,
        GT_GAUNTLET_123_SOUTHWEST_SWITCH_POTS,
    ))
    if has_northwest_switch_pot and has_southwest_switch_pot:
        choices.append(ROOM_VARIANT_TOGGLE_SWITCH)
    if has_southwest_switch_pot:
        choices.append(ROOM_VARIANT_KILL_ENEMIES)
    return tuple(choices)


def get_gt_mimics_variants(world: "ALTTPWorld") -> tuple[int, ...]:
    choices = [ROOM_VARIANT_VANILLA, 1]
    has_northwest_switch_pot = bool(_filled_pot_positions_in_target(
        world,
        GT_MIMICS_ROOM_ID,
        GT_MIMICS_NORTHWEST_SWITCH_POTS,
    ))
    has_southeast_switch_pot = bool(_filled_pot_positions_in_target(
        world,
        GT_MIMICS_ROOM_ID,
        GT_MIMICS_SOUTHEAST_SWITCH_POTS,
    ))
    if has_northwest_switch_pot:
        choices.append(2)
    if has_northwest_switch_pot and has_southeast_switch_pot:
        choices.append(4)
    return tuple(choices)


def get_gt_gauntlet_45_variants(world: "ALTTPWorld") -> tuple[int, ...]:
    choices = [GT_GAUNTLET_45_VARIANTS[0]]
    if _filled_pot_positions_in_target(world, GT_GAUNTLET_45_ROOM_ID, GT_GAUNTLET_45_SOUTHWEST_SWITCH_POTS):
        choices.extend(GT_GAUNTLET_45_VARIANTS[1:])
    return tuple(choices)


def get_gt_winder_warp_maze_tag_1_choices(world: "ALTTPWorld") -> tuple[int, ...]:
    if _filled_pot_positions_in_target(world, GT_WINDER_WARP_MAZE_ROOM_ID, GT_WINDER_WARP_MAZE_SOUTHEAST_SWITCH_POTS):
        return GT_WINDER_WARP_MAZE_TAG_1_CHOICES
    return (TAG_SWITCH_OPENS_DOOR_TOGGLE,)


def get_gt_winder_warp_maze_tag_2_choices(world: "ALTTPWorld") -> tuple[int, ...]:
    choices = []
    if _filled_pot_positions_in_target(world, GT_WINDER_WARP_MAZE_ROOM_ID, GT_WINDER_WARP_MAZE_NORTH_SWITCH_POTS):
        choices.append(TAG_TRIGGER_ACTIVATED_CHEST)
    return tuple(choices)


def get_desert_west_entrance_tag_choices(world: "ALTTPWorld") -> tuple[int, ...]:
    choices = list(DESERT_WEST_ENTRANCE_TAG_CHOICES)
    if _has_randomized_killable_enemy(world, DESERT_WEST_ENTRANCE_ROOM_ID, DESERT_BEAMOS_HELLWAY_BOTTOM_LEFT):
        choices.append(TAG_SW_KILL_ENEMY_TO_OPEN)
    return tuple(choices)


def get_turtle_rock_torch_puzzle_tag_choices(world: "ALTTPWorld") -> tuple[int, ...]:
    choices = [TAG_LIGHT_TORCHES_TO_OPEN]
    if _filled_pot_positions_in_target(world, TURTLE_ROCK_TORCH_PUZZLE_ROOM_ID, TURTLE_ROCK_TORCH_PUZZLE_SWITCH_POTS):
        choices.append(TAG_SWITCH_OPENS_DOOR_TOGGLE)
    return tuple(choices)


def get_ice_palace_hole_to_kholdstare_tag_choices(world: "ALTTPWorld") -> tuple[int, ...]:
    choices = [TAG_PULL_LEVER_TO_OPEN, TAG_NE_KILL_ENEMY_TO_OPEN]
    if _filled_pot_positions_in_target(world, ICE_PALACE_HOLE_TO_KHOLDSTARE_ROOM_ID, ICE_PALACE_HOLE_TO_KHOLDSTARE_SWITCH_POTS):
        choices.extend(HERA_SWITCH_TAG_CHOICES)
    return tuple(choices)


def get_skull_woods_gibdo_torch_tag_choices(world: "ALTTPWorld") -> tuple[int, ...]:
    choices = list(SKULL_WOODS_GIBDO_TORCH_BASE_TAG_CHOICES)
    if _filled_pot_positions_in_target(
        world,
        SKULL_WOODS_GIBDO_TORCH_ROOM_ID,
        SKULL_WOODS_GIBDO_TORCH_HOLD_SWITCH_POTS,
        allow_key=False,
    ):
        choices.append(TAG_SWITCH_OPENS_DOOR_HOLD)
    if _filled_pot_positions_in_target(
        world,
        SKULL_WOODS_GIBDO_TORCH_ROOM_ID,
        SKULL_WOODS_GIBDO_TORCH_SWITCH_POTS,
        allow_key=False,
    ):
        choices.append(TAG_SWITCH_OPENS_DOOR_TOGGLE)
    return tuple(choices)


def get_eastern_pre_armos_tag_choices(world: "ALTTPWorld") -> tuple[int, ...]:
    choices = [TAG_E_KILL_ENEMY_TO_OPEN]
    if (
        _filled_pot_positions_in_target(world, EASTERN_PRE_ARMOS_ROOM_ID, EASTERN_PRE_ARMOS_NORTHEAST_SWITCH_POTS)
        and _filled_pot_positions_in_target(world, EASTERN_PRE_ARMOS_ROOM_ID, EASTERN_PRE_ARMOS_SOUTHEAST_SWITCH_POTS)
    ):
        choices.extend(HERA_SWITCH_TAG_CHOICES)
    return tuple(choices)


def get_ice_palace_bomb_jump_room_tag_choices(world: "ALTTPWorld") -> tuple[int, ...]:
    choices = list(ICE_PALACE_BOMB_JUMP_BASE_TAG_CHOICES)
    if _has_randomized_killable_enemy(world, ICE_PALACE_BOMB_JUMP_ROOM_ID, ICE_PALACE_BOMB_JUMP_ROOM_NORTHWEST):
        choices.append(TAG_NW_KILL_ENEMY_TO_OPEN)
    return tuple(choices)


def _get_normal_switch_replacement_pot_items(world: "ALTTPWorld") -> tuple[int, ...]:
    if world.options.retro_bow:
        return tuple(item for item in NORMAL_SWITCH_REPLACEMENT_POT_ITEMS if item != POT_ARROW)
    return NORMAL_SWITCH_REPLACEMENT_POT_ITEMS


def apply_puzzle_pot_modifications(
    pot_shuffle_state: dict[int, tuple[FilledPot, ...]] | None,
    state: PuzzleShuffleState | None,
) -> dict[int, tuple[FilledPot, ...]] | None:
    if pot_shuffle_state is None or state is None:
        return None
    modified_state = dict(pot_shuffle_state)
    if not desert_map_chest_uses_switch(state):
        room_pots = modified_state.get(DESERT_MAP_CHEST_ROOM_ID)
        if room_pots is not None:
            modified_state[DESERT_MAP_CHEST_ROOM_ID] = _replace_pot_item_value(
                room_pots,
                POT_SWITCH,
                state.switch_replacement_item,
            )
    if state.hera_big_key_chest_switch_pot is not None:
        modified_state[HERA_TILE_ROOM_ID] = _replace_pot_item(
            modified_state.get(HERA_TILE_ROOM_ID, tuple()),
            state.hera_big_key_chest_switch_pot,
            POT_SWITCH,
        )
    if state.hera_tile_room_switch_pot is not None:
        modified_state[HERA_TILE_ROOM_ID] = _replace_pot_item(
            modified_state.get(HERA_TILE_ROOM_ID, tuple()),
            state.hera_tile_room_switch_pot,
            POT_SWITCH,
        )
    if state.gt_block_puzzle_switch_pot is not None:
        modified_state[GT_BLOCK_PUZZLE_ROOM_ID] = _replace_pot_item(
            modified_state.get(GT_BLOCK_PUZZLE_ROOM_ID, tuple()),
            state.gt_block_puzzle_switch_pot,
            POT_SWITCH,
        )
    if state.gt_big_chest_room_tag not in HERA_SWITCH_TAG_CHOICES:
        modified_state[GT_BIG_CHEST_ROOM_ID] = _replace_pot_item_value(
            modified_state.get(GT_BIG_CHEST_ROOM_ID, tuple()),
            GT_BIG_CHEST_ROOM_SWITCH_POT_ITEM,
            state.switch_replacement_item,
        )
    if state.gt_tile_torch_puzzle_switch_pot is not None:
        modified_state[GT_TILE_TORCH_PUZZLE_ROOM_ID] = _replace_pot_item(
            modified_state.get(GT_TILE_TORCH_PUZZLE_ROOM_ID, tuple()),
            state.gt_tile_torch_puzzle_switch_pot,
            POT_SWITCH,
        )
    if state.misery_mire_dark_cane_room_switch_pot is not None:
        room_pots = _replace_pot_item_value(
            modified_state.get(MISERY_MIRE_DARK_CANE_ROOM_ID, tuple()),
            POT_SWITCH,
            state.switch_replacement_item,
        )
        modified_state[MISERY_MIRE_DARK_CANE_ROOM_ID] = _replace_pot_item(
            room_pots,
            state.misery_mire_dark_cane_room_switch_pot,
            POT_SWITCH,
        )
    elif state.misery_mire_dark_cane_room_tag not in HERA_SWITCH_TAG_CHOICES:
        modified_state[MISERY_MIRE_DARK_CANE_ROOM_ID] = _replace_pot_item_value(
            modified_state.get(MISERY_MIRE_DARK_CANE_ROOM_ID, tuple()),
            POT_SWITCH,
            state.switch_replacement_item,
        )
    if state.gt_torches_1_switch_pot is not None:
        modified_state[GT_TORCHES_1_ROOM_ID] = _replace_pot_item(
            modified_state.get(GT_TORCHES_1_ROOM_ID, tuple()),
            state.gt_torches_1_switch_pot,
            POT_SWITCH,
        )
    if state.ice_palace_ice_floor_room_tag == TAG_SW_KILL_ENEMY_TO_OPEN:
        modified_state[ICE_PALACE_ICE_FLOOR_ROOM_ID] = _replace_pot_item_value(
            modified_state.get(ICE_PALACE_ICE_FLOOR_ROOM_ID, tuple()),
            POT_SWITCH,
            state.switch_replacement_item,
        )
    if state.eastern_stalfos_room_switch_pot is not None:
        modified_state[EASTERN_STALFOS_ROOM_ID] = _replace_pot_item(
            modified_state.get(EASTERN_STALFOS_ROOM_ID, tuple()),
            state.eastern_stalfos_room_switch_pot,
            POT_SWITCH,
        )
    if state.misery_mire_spike_chest_room_tag != TAG_TRIGGER_ACTIVATED_CHEST:
        modified_state[MISERY_MIRE_SPIKE_CHEST_ROOM_ID] = _replace_pot_item_value(
            modified_state.get(MISERY_MIRE_SPIKE_CHEST_ROOM_ID, tuple()),
            POT_SWITCH,
            state.switch_replacement_item,
        )
    if state.turtle_rock_torch_puzzle_switch_pot is not None:
        modified_state[TURTLE_ROCK_TORCH_PUZZLE_ROOM_ID] = _replace_pot_item(
            modified_state.get(TURTLE_ROCK_TORCH_PUZZLE_ROOM_ID, tuple()),
            state.turtle_rock_torch_puzzle_switch_pot,
            POT_SWITCH,
        )
    if state.ice_palace_hole_to_kholdstare_switch_pot is not None:
        modified_state[ICE_PALACE_HOLE_TO_KHOLDSTARE_ROOM_ID] = _replace_pot_item(
            modified_state.get(ICE_PALACE_HOLE_TO_KHOLDSTARE_ROOM_ID, tuple()),
            state.ice_palace_hole_to_kholdstare_switch_pot,
            POT_SWITCH,
        )
    if state.eastern_pre_armos_northeast_switch_pot is not None:
        modified_state[EASTERN_PRE_ARMOS_ROOM_ID] = _replace_pot_item(
            modified_state.get(EASTERN_PRE_ARMOS_ROOM_ID, tuple()),
            state.eastern_pre_armos_northeast_switch_pot,
            POT_SWITCH,
        )
    if state.eastern_pre_armos_southeast_switch_pot is not None:
        modified_state[EASTERN_PRE_ARMOS_ROOM_ID] = _replace_pot_item(
            modified_state.get(EASTERN_PRE_ARMOS_ROOM_ID, tuple()),
            state.eastern_pre_armos_southeast_switch_pot,
            POT_SWITCH,
        )
    _replace_switch_pots_for_puzzle_state(modified_state, state)
    return modified_state


def apply_puzzle_shuffle(
    rom: "TokenRom",
    state: PuzzleShuffleState,
    pot_shuffle_state: dict[int, tuple[FilledPot, ...]] | None = None,
) -> None:
    from .EnemizerPatches import get_dungeon_room_header_address

    def write_room_header_byte(room_id: int, offset: int, value: int) -> None:
        rom.write_byte(get_dungeon_room_header_address(rom, room_id) + offset, value)

    patch_hold_switch_tile_detector(rom)

    write_room_header_byte(DESERT_MAP_CHEST_ROOM_ID, 5, state.desert_map_chest_tag)
    write_room_header_byte(DESERT_BIG_CHEST_ROOM_ID, 5, state.desert_big_chest_tag)
    write_room_header_byte(
        DESERT_FINAL_SECTION_ENTRANCE_ROOM_ID,
        5,
        state.desert_final_section_entrance_tag,
    )
    write_room_header_byte(HERA_TILE_ROOM_ID, 5, state.hera_big_key_chest_tag)
    write_room_header_byte(HERA_TILE_ROOM_ID, 6, state.hera_tile_room_tag)
    write_room_header_byte(GT_BLOCK_PUZZLE_ROOM_ID, 6, state.gt_block_puzzle_tag)
    write_room_header_byte(GT_BIG_CHEST_ROOM_ID, 5, state.gt_big_chest_room_tag)
    write_room_header_byte(GT_TILE_TORCH_PUZZLE_ROOM_ID, 5, state.gt_tile_torch_puzzle_tag)
    write_room_header_byte(MISERY_MIRE_DARK_CANE_ROOM_ID, 5, state.misery_mire_dark_cane_room_tag)
    write_room_header_byte(GT_TORCHES_1_ROOM_ID, 5, state.gt_torches_1_tag)
    write_room_header_byte(ICE_PALACE_ICE_FLOOR_ROOM_ID, 5, state.ice_palace_ice_floor_room_tag)
    write_room_header_byte(EASTERN_STALFOS_ROOM_ID, 5, state.eastern_stalfos_room_tag)
    write_room_header_byte(EASTERN_BIG_CHEST_ROOM_ID, 5, state.eastern_big_chest_room_tag)
    write_room_header_byte(EASTERN_MAP_CHEST_ROOM_ID, 5, state.eastern_map_chest_room_tag)
    write_room_header_byte(ICE_PALACE_HIDDEN_CHEST_ROOM_ID, 5, state.ice_palace_hidden_chest_room_tag)
    write_room_header_byte(MISERY_MIRE_BRIDGE_CHEST_ROOM_ID, 6, state.misery_mire_bridge_chest_tag_2)
    write_room_header_byte(MISERY_MIRE_SPIKE_CHEST_ROOM_ID, 5, state.misery_mire_spike_chest_room_tag)
    write_room_header_byte(EASTERN_DARK_SQUARE_ROOM_ID, 5, state.eastern_dark_square_room_tag)
    write_room_header_byte(THIEVES_TOWN_CONVEYOR_TOILET_ROOM_ID, 5, state.thieves_town_conveyor_toilet_tag)
    write_room_header_byte(ICE_PALACE_BLOCK_PUZZLE_ROOM_ID, 5, state.ice_palace_block_puzzle_tag)
    write_room_header_byte(MISERY_MIRE_TILE_ROOM_ID, 5, state.misery_mire_tile_room_tag)
    write_room_header_byte(TURTLE_ROCK_TORCH_PUZZLE_ROOM_ID, 5, state.turtle_rock_torch_puzzle_tag)
    write_room_header_byte(ICE_PALACE_HOLE_TO_KHOLDSTARE_ROOM_ID, 5, state.ice_palace_hole_to_kholdstare_tag)
    write_room_header_byte(EASTERN_PRE_ARMOS_ROOM_ID, 5, state.eastern_pre_armos_tag)
    write_room_header_byte(EASTERN_PRE_BOSS_ROOM_ID, 5, state.eastern_pre_boss_room_tag)
    write_room_header_byte(EASTERN_SWITCH_ROOM_ID, 5, state.eastern_switch_room_tag)
    write_room_header_byte(
        HYRULE_CASTLE_SWITCH_ROOM_ID,
        5,
        TAG_S_KILL_ENEMY_TO_OPEN
        if state.hyrule_castle_switch_room_variant == ROOM_VARIANT_KILL_ENEMIES
        else TAG_PULL_LEVER_TO_OPEN,
    )
    write_room_header_byte(
        TURTLE_ROCK_CRYSTAROLLER_ROOM_ID,
        6,
        TAG_SWITCH_OPENS_DOOR_TOGGLE
        if state.turtle_rock_crystaroller_room_variant == ROOM_VARIANT_TOGGLE_SWITCH
        else TAG_SWITCH_OPENS_DOOR_HOLD
        if state.turtle_rock_crystaroller_room_variant == ROOM_VARIANT_HOLD_SWITCH
        else TAG_PULL_LEVER_TO_OPEN,
    )
    write_room_header_byte(POD_TURTLE_ROOM_ID, 5, state.pod_turtle_room_tag)
    write_room_header_byte(POD_MIMICS_MOVING_WALL_ROOM_ID, 5, state.pod_mimics_moving_wall_room_tag)
    write_room_header_byte(
        ICE_PALACE_BOMB_FLOOR_ROOM_ID,
        5,
        TAG_SW_KILL_ENEMY_TO_OPEN
        if state.ice_palace_bomb_floor_room_variant == ROOM_VARIANT_KILL_ENEMIES
        else TAG_SWITCH_OPENS_DOOR_TOGGLE,
    )
    write_room_header_byte(
        ICE_PALACE_BOMB_FLOOR_ROOM_ID,
        6,
        TAG_SE_MOVE_BLOCK_TO_OPEN
        if state.ice_palace_bomb_floor_room_variant == ROOM_VARIANT_KILL_ENEMIES
        else 0,
    )
    if state.ice_palace_bomb_floor_room_variant == ROOM_VARIANT_KILL_ENEMIES:
        rom.write_bytes(
            ICE_PALACE_BOMB_FLOOR_PUSH_BLOCK_POSITION_ADDRESS,
            ICE_PALACE_BOMB_FLOOR_DOOR_TRIGGER_PUSH_BLOCK_POSITION.to_bytes(2, "little"),
        )
    write_room_header_byte(
        ICE_PALACE_PENGATOR_BIG_KEY_ROOM_ID,
        5,
        state.ice_palace_pengator_big_key_room_tag,
    )
    write_room_header_byte(TURTLE_ROCK_BIG_CHEST_ROOM_ID, 5, state.turtle_rock_big_chest_room_tag)
    write_room_header_byte(SWAMP_STATUE_ROOM_ID, 5, state.swamp_statue_room_tag)
    write_room_header_byte(POD_MAP_CHEST_ROOM_ID, 5, state.pod_map_chest_room_tag)
    write_room_header_byte(HERA_HARDHAT_BEETLES_ROOM_ID, 6, state.hera_hardhat_beetles_room_tag_2)
    write_room_header_byte(ICE_PALACE_CONVEYOR_HELLWAY_ROOM_ID, 5, state.ice_palace_conveyor_hellway_tag)
    write_room_header_byte(ICE_PALACE_MAP_ROOM_ID, 5, state.ice_palace_map_room_tag)
    write_room_header_byte(THIEVES_TOWN_JAIL_CELLS_ROOM_ID, 5, state.thieves_town_jail_cells_tag)
    write_room_header_byte(SKULL_WOODS_GIBDO_TORCH_ROOM_ID, 5, state.skull_woods_gibdo_torch_room_tag)
    write_room_header_byte(POD_SOUTH_MIMICS_ROOM_ID, 5, state.pod_south_mimics_room_tag)
    write_room_header_byte(ICE_PALACE_BOMB_JUMP_ROOM_ID, 5, state.ice_palace_bomb_jump_room_tag)
    write_room_header_byte(SKULL_WOODS_BIG_KEY_ROOM_ID, 5, state.skull_woods_big_key_room_tag)
    write_room_header_byte(SKULL_WOODS_BIG_CHEST_ROOM_ID, 6, state.skull_woods_big_chest_room_tag_2)
    gt_gauntlet_tag_1, gt_gauntlet_tag_2 = _get_gt_gauntlet_123_tags(state.gt_gauntlet_123_room_variant)
    write_room_header_byte(GT_GAUNTLET_123_ROOM_ID, 5, gt_gauntlet_tag_1)
    write_room_header_byte(GT_GAUNTLET_123_ROOM_ID, 6, gt_gauntlet_tag_2)
    write_room_header_byte(ICE_PALACE_SPIKE_ROOM_ID, 5, state.ice_palace_spike_room_tag)
    write_room_header_byte(THIEVES_TOWN_WEST_ATTIC_ROOM_ID, 5, state.thieves_town_west_attic_room_tag)
    gt_mimics_tag_1, gt_mimics_tag_2 = _get_gt_mimics_tags(state.gt_mimics_room_variant)
    write_room_header_byte(GT_MIMICS_ROOM_ID, 5, gt_mimics_tag_1)
    write_room_header_byte(GT_MIMICS_ROOM_ID, 6, gt_mimics_tag_2)
    gt_gauntlet_45_tag_1, gt_gauntlet_45_tag_2 = _get_gt_gauntlet_45_tags(state.gt_gauntlet_45_room_variant)
    write_room_header_byte(GT_GAUNTLET_45_ROOM_ID, 5, gt_gauntlet_45_tag_1)
    write_room_header_byte(GT_GAUNTLET_45_ROOM_ID, 6, gt_gauntlet_45_tag_2)
    write_room_header_byte(GT_WINDER_WARP_MAZE_ROOM_ID, 5, state.gt_winder_warp_maze_tag_1)
    write_room_header_byte(GT_WINDER_WARP_MAZE_ROOM_ID, 6, state.gt_winder_warp_maze_tag_2)
    write_room_header_byte(DESERT_WEST_ENTRANCE_ROOM_ID, 5, state.desert_west_entrance_tag)

    if not desert_map_chest_uses_switch(state):
        apply_desert_map_chest_switch_removal(rom, state.switch_replacement_item, pot_shuffle_state)
    if pot_shuffle_state is None and _room_needs_direct_pot_patch(HERA_TILE_ROOM_ID, state):
        write_pot_room_items(rom, HERA_TILE_ROOM_ID, _get_pots_with_puzzle_modifications(HERA_TILE_ROOM_ID, state))
    if pot_shuffle_state is None and _room_needs_direct_pot_patch(GT_BLOCK_PUZZLE_ROOM_ID, state):
        write_pot_room_items(rom, GT_BLOCK_PUZZLE_ROOM_ID, _get_pots_with_puzzle_modifications(GT_BLOCK_PUZZLE_ROOM_ID, state))
    if pot_shuffle_state is None and _room_needs_direct_pot_patch(GT_BIG_CHEST_ROOM_ID, state):
        write_pot_room_items(rom, GT_BIG_CHEST_ROOM_ID, _get_pots_with_puzzle_modifications(GT_BIG_CHEST_ROOM_ID, state))
    if pot_shuffle_state is None and _room_needs_direct_pot_patch(GT_TILE_TORCH_PUZZLE_ROOM_ID, state):
        write_pot_room_items(rom, GT_TILE_TORCH_PUZZLE_ROOM_ID, _get_pots_with_puzzle_modifications(GT_TILE_TORCH_PUZZLE_ROOM_ID, state))
    if pot_shuffle_state is None and _room_needs_direct_pot_patch(MISERY_MIRE_DARK_CANE_ROOM_ID, state):
        write_pot_room_items(rom, MISERY_MIRE_DARK_CANE_ROOM_ID, _get_pots_with_puzzle_modifications(MISERY_MIRE_DARK_CANE_ROOM_ID, state))
    if pot_shuffle_state is None and _room_needs_direct_pot_patch(GT_TORCHES_1_ROOM_ID, state):
        write_pot_room_items(rom, GT_TORCHES_1_ROOM_ID, _get_pots_with_puzzle_modifications(GT_TORCHES_1_ROOM_ID, state))
    if pot_shuffle_state is None and _room_needs_direct_pot_patch(ICE_PALACE_ICE_FLOOR_ROOM_ID, state):
        write_pot_room_items(rom, ICE_PALACE_ICE_FLOOR_ROOM_ID, _get_pots_with_puzzle_modifications(ICE_PALACE_ICE_FLOOR_ROOM_ID, state))
    if pot_shuffle_state is None and _room_needs_direct_pot_patch(EASTERN_STALFOS_ROOM_ID, state):
        write_pot_room_items(rom, EASTERN_STALFOS_ROOM_ID, _get_pots_with_puzzle_modifications(EASTERN_STALFOS_ROOM_ID, state))
    if pot_shuffle_state is None and _room_needs_direct_pot_patch(EASTERN_BIG_KEY_ROOM_ID, state):
        write_pot_room_items(rom, EASTERN_BIG_KEY_ROOM_ID, _get_pots_with_puzzle_modifications(EASTERN_BIG_KEY_ROOM_ID, state))
    if pot_shuffle_state is None and _room_needs_direct_pot_patch(MISERY_MIRE_SPIKE_CHEST_ROOM_ID, state):
        write_pot_room_items(rom, MISERY_MIRE_SPIKE_CHEST_ROOM_ID, _get_pots_with_puzzle_modifications(MISERY_MIRE_SPIKE_CHEST_ROOM_ID, state))
    if pot_shuffle_state is None and _room_needs_direct_pot_patch(TURTLE_ROCK_TORCH_PUZZLE_ROOM_ID, state):
        write_pot_room_items(rom, TURTLE_ROCK_TORCH_PUZZLE_ROOM_ID, _get_pots_with_puzzle_modifications(TURTLE_ROCK_TORCH_PUZZLE_ROOM_ID, state))
    if pot_shuffle_state is None and _room_needs_direct_pot_patch(ICE_PALACE_HOLE_TO_KHOLDSTARE_ROOM_ID, state):
        write_pot_room_items(rom, ICE_PALACE_HOLE_TO_KHOLDSTARE_ROOM_ID, _get_pots_with_puzzle_modifications(ICE_PALACE_HOLE_TO_KHOLDSTARE_ROOM_ID, state))
    if pot_shuffle_state is None and _room_needs_direct_pot_patch(EASTERN_PRE_ARMOS_ROOM_ID, state):
        write_pot_room_items(rom, EASTERN_PRE_ARMOS_ROOM_ID, _get_pots_with_puzzle_modifications(EASTERN_PRE_ARMOS_ROOM_ID, state))
    for room_id in (
        TURTLE_ROCK_BIG_CHEST_ROOM_ID,
        SWAMP_STATUE_ROOM_ID,
        POD_MAP_CHEST_ROOM_ID,
        HERA_HARDHAT_BEETLES_ROOM_ID,
        ICE_PALACE_CONVEYOR_HELLWAY_ROOM_ID,
        ICE_PALACE_MAP_ROOM_ID,
        THIEVES_TOWN_JAIL_CELLS_ROOM_ID,
        SKULL_WOODS_GIBDO_TORCH_ROOM_ID,
        POD_SOUTH_MIMICS_ROOM_ID,
        ICE_PALACE_BOMB_JUMP_ROOM_ID,
        SKULL_WOODS_BIG_KEY_ROOM_ID,
        SKULL_WOODS_BIG_CHEST_ROOM_ID,
        GT_GAUNTLET_123_ROOM_ID,
        THIEVES_TOWN_WEST_ATTIC_ROOM_ID,
        GT_MIMICS_ROOM_ID,
        GT_GAUNTLET_45_ROOM_ID,
        GT_WINDER_WARP_MAZE_ROOM_ID,
    ):
        if pot_shuffle_state is None and _room_needs_direct_pot_patch(room_id, state):
            write_pot_room_items(rom, room_id, _get_pots_with_puzzle_modifications(room_id, state))
    if state.gt_big_chest_room_tag == TAG_PULL_LEVER_TO_OPEN:
        rom.write_byte(GT_BIG_CHEST_ROOM_PULL_SWITCH_TRAP_SPRITE_ID_ADDRESS, GT_BIG_CHEST_ROOM_PULL_SWITCH_GOOD)
    if state.skull_woods_big_chest_room_tag_2 == TAG_USE_SWITCH_TO_BOMB_WALL:
        rom.write_byte(SKULL_WOODS_BIG_CHEST_PULL_SWITCH_GOOD_SPRITE_ID_ADDRESS, PULL_SWITCH_TRAP)
        if state.skull_woods_big_chest_rope_trap_sprite_address is not None:
            rom.write_bytes(
                state.skull_woods_big_chest_rope_trap_sprite_address,
                SKULL_WOODS_BIG_CHEST_ROPE_TRAP_RECORD_BYTES,
            )
    if state.thieves_town_west_attic_room_tag == TAG_PULL_LEVER_TO_OPEN:
        rom.write_byte(THIEVES_TOWN_WEST_ATTIC_PULL_SWITCH_TRAP_SPRITE_ID_ADDRESS, PULL_SWITCH_GOOD)
    if state.ice_palace_hole_to_kholdstare_pull_switch_moved:
        rom.write_byte(
            ICE_PALACE_HOLE_TO_KHOLDSTARE_PULL_SWITCH_X_ADDRESS,
            ICE_PALACE_HOLE_TO_KHOLDSTARE_PULL_SWITCH_MOVED_X,
        )
    _write_hyrule_castle_switch_room_sprites(rom, state.hyrule_castle_switch_room_variant)
    _write_turtle_rock_crystaroller_sprites(rom, state.turtle_rock_crystaroller_room_variant)
    _write_swamp_floodway_sprites(rom, state.swamp_floodway_room_variant)
    write_puzzle_object_swaps(rom, state)


def apply_desert_map_chest_switch_removal(
    rom: "TokenRom",
    replacement_item: int,
    pot_shuffle_state: dict[int, tuple[FilledPot, ...]] | None = None,
) -> None:
    if pot_shuffle_state and DESERT_MAP_CHEST_ROOM_ID in pot_shuffle_state:
        pots = _replace_pot_item_value(
            pot_shuffle_state[DESERT_MAP_CHEST_ROOM_ID],
            POT_SWITCH,
            replacement_item,
        )
    else:
        pots = _replace_pot_item_value(
            get_vanilla_pot_items(DESERT_MAP_CHEST_ROOM_ID),
            POT_SWITCH,
            replacement_item,
        )
    write_pot_room_items(rom, DESERT_MAP_CHEST_ROOM_ID, pots)


def write_pot_room_items(rom: "TokenRom", room_id: int, pots: tuple[FilledPot, ...]) -> None:
    address = POT_ITEM_ADDRESSES[room_id]
    for index, pot in enumerate(pots):
        rom.write_bytes(address + (index * 3), (pot.x, pot.y, pot.item))
    rom.write_bytes(address + (len(pots) * 3), (0xFF, 0xFF))


def patch_hold_switch_tile_detector(rom: "TokenRom") -> None:
    # Tag 0x16 originally calls the star-tile-aware detector at $CDCC. Use the
    # floor-switch detector at $CD39 instead so star tiles keep their vanilla
    # toggle behavior in rooms whose puzzle tag was changed to hold-switch.
    rom.write_bytes(HOLD_SWITCH_TILE_DETECTOR_CALL_ADDRESS, (0x20, 0x39, 0xCD))


def write_puzzle_object_swaps(rom: "TokenRom", state: PuzzleShuffleState) -> None:
    _write_push_block_swap(
        rom,
        POD_TURTLE_ROOM_ID,
        POD_TURTLE_ROOM_PUSH_BLOCK_SOURCE,
        state.pod_turtle_room_push_block_target,
        0x5E,
    )
    _write_push_block_swap(
        rom,
        DESERT_FINAL_SECTION_ENTRANCE_ROOM_ID,
        DESERT_FINAL_SECTION_ENTRANCE_PUSH_BLOCK_SOURCE,
        state.desert_final_section_entrance_push_block_target,
        0x5E,
    )
    _write_push_block_swap(
        rom,
        SWAMP_HIDDEN_DOOR_ROOM_ID,
        SWAMP_HIDDEN_DOOR_PUSH_BLOCK_SOURCE,
        state.swamp_hidden_door_push_block_target,
        0x5E,
        layer=2,
    )
    _write_push_block_swap(
        rom,
        GT_MIMICS_ROOM_ID,
        GT_MIMICS_PUSH_BLOCK_SOURCE,
        state.gt_mimics_push_block_target,
        0x5E,
    )
    _write_push_block_swap(
        rom,
        DESERT_WEST_ENTRANCE_ROOM_ID,
        DESERT_WEST_ENTRANCE_PUSH_BLOCK_SOURCE,
        state.desert_west_entrance_push_block_target,
        0x5E,
    )
    _write_push_block_swap(
        rom,
        TURTLE_ROCK_CHAIN_CHOMPS_ROOM_ID,
        state.turtle_rock_chain_chomps_push_block_source,
        state.turtle_rock_chain_chomps_push_block_target,
        0x89,
    )


def _write_push_block_swap(
    rom: "TokenRom",
    room_id: int,
    source_position: tuple[int, int] | None,
    target_position: tuple[int, int] | None,
    target_object_id: int,
    layer: int = 1,
) -> None:
    if source_position is None or target_position is None or target_position == source_position:
        return
    push_block_address, preserved_flags = JP_PUSH_BLOCK_RECORDS[(room_id, source_position)]
    rom.write_bytes(push_block_address + 2, _encode_push_block_position(target_position, preserved_flags))
    _write_room_object_position(
        rom,
        room_id,
        target_position,
        target_object_id,
        layer,
        source_position,
    )


def _write_room_object_position(
    rom: "TokenRom",
    room_id: int,
    object_position: tuple[int, int],
    object_id: int,
    layer: int,
    new_position: tuple[int, int],
) -> None:
    key = (room_id, object_position, object_id, layer)
    address = ROOM_OBJECT_RECORD_ADDRESSES[key]
    subtype = ROOM_OBJECT_RECORD_SUBTYPES[key]
    rom.write_bytes(address, _encode_room_object_position(new_position, object_id, subtype))


def _encode_push_block_position(position: tuple[int, int], preserved_flags: int) -> bytes:
    x, y = position
    raw = preserved_flags | (((y << 6) | x) << 1)
    return raw.to_bytes(2, "little")


def _encode_room_object_position(position: tuple[int, int], object_id: int, subtype: int) -> bytes:
    x, y = position
    dm_x = x | (y << 6)
    if object_id < 0xF8:
        return bytes((
            ((dm_x << 2) & 0xFC) | ((subtype >> 2) & 0x03),
            ((dm_x >> 4) & 0xFC) | (subtype & 0x03),
        ))
    return bytes((
        ((dm_x << 2) & 0xFC) | (subtype & 0x03),
        ((dm_x >> 4) & 0xFC) | ((subtype >> 2) & 0x03),
    ))


def _write_hyrule_castle_switch_room_sprites(rom: "TokenRom", variant: int) -> None:
    if variant == ROOM_VARIANT_SWAP_PULL_SWITCHES:
        trap_switch = PULL_SWITCH_GOOD
        good_switch = PULL_SWITCH_TRAP
        _mirror_hyrule_castle_switch_room_bomb_drops(rom)
    elif variant == ROOM_VARIANT_KILL_ENEMIES:
        trap_switch = PULL_SWITCH_TRAP
        good_switch = PULL_SWITCH_TRAP
    else:
        trap_switch = PULL_SWITCH_TRAP
        good_switch = PULL_SWITCH_GOOD
    rom.write_byte(HYRULE_CASTLE_SWITCH_ROOM_PULL_SWITCH_TRAP_SPRITE_ID_ADDRESS, trap_switch)
    rom.write_byte(HYRULE_CASTLE_SWITCH_ROOM_PULL_SWITCH_GOOD_SPRITE_ID_ADDRESS, good_switch)


def _mirror_hyrule_castle_switch_room_bomb_drops(rom: "TokenRom") -> None:
    for address, mirrored_x in HYRULE_CASTLE_SWITCH_ROOM_MIRRORED_BOMB_DROP_X_BYTES:
        rom.write_byte(address, mirrored_x)


def _write_turtle_rock_crystaroller_sprites(rom: "TokenRom", variant: int) -> None:
    if variant == ROOM_VARIANT_SWAP_PULL_SWITCHES:
        good_switch = PULL_SWITCH_TRAP
        trap_switch = PULL_SWITCH_GOOD
    elif variant in (ROOM_VARIANT_TOGGLE_SWITCH, ROOM_VARIANT_HOLD_SWITCH):
        good_switch = PULL_SWITCH_TRAP
        trap_switch = PULL_SWITCH_TRAP
    else:
        good_switch = PULL_SWITCH_GOOD
        trap_switch = PULL_SWITCH_TRAP
    rom.write_byte(TURTLE_ROCK_CRYSTAROLLER_PULL_SWITCH_GOOD_SPRITE_ID_ADDRESS, good_switch)
    rom.write_byte(TURTLE_ROCK_CRYSTAROLLER_PULL_SWITCH_TRAP_SPRITE_ID_ADDRESS, trap_switch)


def _write_swamp_floodway_sprites(rom: "TokenRom", variant: int) -> None:
    if variant == ROOM_VARIANT_SWAP_PULL_SWITCHES:
        trap_switch = PULL_SWITCH_GOOD
        good_switch = PULL_SWITCH_TRAP
    else:
        trap_switch = PULL_SWITCH_TRAP
        good_switch = PULL_SWITCH_GOOD
    rom.write_byte(SWAMP_FLOODWAY_PULL_SWITCH_TRAP_SPRITE_ID_ADDRESS, trap_switch)
    rom.write_byte(SWAMP_FLOODWAY_PULL_SWITCH_GOOD_SPRITE_ID_ADDRESS, good_switch)


def _get_gt_gauntlet_123_tags(variant: int) -> tuple[int, int]:
    if variant == ROOM_VARIANT_TOGGLE_SWITCH:
        return TAG_SWITCH_OPENS_DOOR_TOGGLE, TAG_NE_KILL_ENEMY_TO_OPEN
    if variant == ROOM_VARIANT_KILL_ENEMIES:
        return TAG_N_KILL_ENEMY_TO_OPEN, TAG_SWITCH_OPENS_DOOR_TOGGLE
    return TAG_CLEAR_QUADRANT_TO_OPEN, TAG_NOTHING


def _get_gt_mimics_tags(variant: int) -> tuple[int, int]:
    if variant == 1:
        return TAG_S_KILL_ENEMY_TO_OPEN, TAG_NW_KILL_ENEMY_TO_OPEN
    if variant == 2:
        return TAG_S_KILL_ENEMY_TO_OPEN, TAG_SWITCH_OPENS_DOOR_TOGGLE
    if variant == 4:
        return TAG_SW_KILL_ENEMY_TO_OPEN, TAG_SWITCH_OPENS_DOOR_TOGGLE
    return TAG_S_KILL_ENEMY_TO_OPEN, TAG_NW_MOVE_BLOCK_TO_OPEN


def _get_gt_gauntlet_45_tags(variant: int) -> tuple[int, int]:
    if variant == ROOM_VARIANT_TOGGLE_SWITCH:
        return TAG_NW_KILL_ENEMY_TO_OPEN, TAG_SWITCH_OPENS_DOOR_TOGGLE
    return TAG_W_KILL_ENEMY_TO_OPEN, TAG_NOTHING


def validate_puzzle_shuffle_data() -> None:
    desert_map_chest_tags = ROOM_TAGS[DESERT_MAP_CHEST_ROOM_ID]
    if desert_map_chest_tags.tag_1 != TAG_TRIGGER_ACTIVATED_CHEST:
        raise ValueError("Desert Palace Map Chest room tag is not Trigger-activated chest")
    desert_big_chest_tags = ROOM_TAGS[DESERT_BIG_CHEST_ROOM_ID]
    if desert_big_chest_tags.tag_1 != TAG_SWITCH_OPENS_DOOR_TOGGLE:
        raise ValueError("Desert Palace Big Chest room tag is not Switch opens door (toggle)")
    if ROOM_TAGS[DESERT_FINAL_SECTION_ENTRANCE_ROOM_ID].tag_1 != TAG_SW_MOVE_BLOCK_TO_OPEN:
        raise ValueError("Desert Palace Final Section Entrance first room tag is not SW Move a block to open")
    hera_tile_room_tags = ROOM_TAGS[HERA_TILE_ROOM_ID]
    if hera_tile_room_tags.tag_1 != TAG_LIGHT_TORCHES_TO_GET_CHEST:
        raise ValueError("Tower of Hera Big Key Chest room tag is not Light torches to get chest")
    if hera_tile_room_tags.tag_2 != TAG_NW_KILL_ENEMY_TO_OPEN:
        raise ValueError("Tower of Hera Tile Room second room tag is not NW Kill enemies to open")
    gt_block_puzzle_tags = ROOM_TAGS[GT_BLOCK_PUZZLE_ROOM_ID]
    if gt_block_puzzle_tags.tag_2 != TAG_NE_MOVE_BLOCK_TO_OPEN:
        raise ValueError("Ganon's Tower Block Puzzle second room tag is not NE Move a block to open")
    gt_big_chest_room_tags = ROOM_TAGS[GT_BIG_CHEST_ROOM_ID]
    if gt_big_chest_room_tags.tag_1 != TAG_SWITCH_OPENS_DOOR_HOLD:
        raise ValueError("Ganon's Tower Big Chest Room first room tag is not Switch opens door (hold)")
    if ROOM_TAGS[GT_TILE_TORCH_PUZZLE_ROOM_ID].tag_1 != TAG_LIGHT_TORCHES_TO_OPEN:
        raise ValueError("Ganon's Tower Tile/Torch Puzzle first room tag is not Light torches to open")
    if ROOM_TAGS[GT_TILE_TORCH_PUZZLE_ROOM_ID].tag_2 != TAG_NW_KILL_ENEMY_FOR_CHEST:
        raise ValueError("Ganon's Tower Tile/Torch Puzzle second room tag is not NW Kill enemies for chest")
    if ROOM_TAGS[MISERY_MIRE_DARK_CANE_ROOM_ID].tag_1 != TAG_SWITCH_OPENS_DOOR_HOLD:
        raise ValueError("Misery Mire Dark Cane Room first room tag is not Switch opens door (hold)")
    if ROOM_TAGS[GT_TORCHES_1_ROOM_ID].tag_1 != TAG_LIGHT_TORCHES_TO_OPEN:
        raise ValueError("Ganon's Tower Torches 1 first room tag is not Light torches to open")
    if ROOM_TAGS[ICE_PALACE_ICE_FLOOR_ROOM_ID].tag_1 != TAG_SWITCH_OPENS_DOOR_TOGGLE:
        raise ValueError("Ice Palace Ice Floor Room first room tag is not Switch opens door (toggle)")
    if ROOM_TAGS[EASTERN_STALFOS_ROOM_ID].tag_1 != TAG_SW_KILL_ENEMY_TO_OPEN:
        raise ValueError("Eastern Palace Stalfos Room first room tag is not SW Kill enemies to open")
    if ROOM_TAGS[EASTERN_BIG_CHEST_ROOM_ID].tag_1 != TAG_SWITCH_OPENS_DOOR_TOGGLE:
        raise ValueError("Eastern Palace Big Chest Room first room tag is not Switch opens door (toggle)")
    if ROOM_TAGS[EASTERN_MAP_CHEST_ROOM_ID].tag_1 != TAG_SWITCH_OPENS_DOOR_TOGGLE:
        raise ValueError("Eastern Palace Map Chest Room first room tag is not Switch opens door (toggle)")
    if ROOM_TAGS[ICE_PALACE_HIDDEN_CHEST_ROOM_ID].tag_1 != TAG_TRIGGER_ACTIVATED_CHEST:
        raise ValueError("Ice Palace Hidden Chest Room first room tag is not Trigger-activated chest")
    if ROOM_TAGS[AGA_TOWER_CIRCLE_OF_POTS_ROOM_ID].tag_1 != TAG_W_KILL_ENEMY_TO_OPEN:
        raise ValueError("Agahnim's Tower Circle of Pots first room tag is not W Kill enemies to open")
    if ROOM_TAGS[AGA_TOWER_CIRCLE_OF_POTS_ROOM_ID].tag_2 != TAG_NE_KILL_ENEMY_TO_OPEN:
        raise ValueError("Agahnim's Tower Circle of Pots second room tag is not NE Kill enemies to open")
    if ROOM_TAGS[MISERY_MIRE_BRIDGE_CHEST_ROOM_ID].tag_2 != TAG_SE_MOVE_BLOCK_TO_OPEN:
        raise ValueError("Misery Mire Bridge Chest second room tag is not SE Move a block to open")
    if ROOM_TAGS[MISERY_MIRE_SPIKE_CHEST_ROOM_ID].tag_1 != TAG_TRIGGER_ACTIVATED_CHEST:
        raise ValueError("Misery Mire Spike Chest first room tag is not Trigger-activated chest")
    if ROOM_TAGS[EASTERN_BIG_KEY_ROOM_ID].tag_1 != TAG_TRIGGER_ACTIVATED_CHEST:
        raise ValueError("Eastern Palace Big Key Room first room tag is not Trigger-activated chest")
    if ROOM_TAGS[EASTERN_DARK_SQUARE_ROOM_ID].tag_1 != TAG_SWITCH_OPENS_DOOR_TOGGLE:
        raise ValueError("Eastern Palace Dark Square Room first room tag is not Switch opens door (toggle)")
    if ROOM_TAGS[THIEVES_TOWN_CONVEYOR_TOILET_ROOM_ID].tag_1 != TAG_SWITCH_OPENS_DOOR_TOGGLE:
        raise ValueError("Thieves' Town Conveyor Toilet first room tag is not Switch opens door (toggle)")
    if ROOM_TAGS[ICE_PALACE_BLOCK_PUZZLE_ROOM_ID].tag_1 != TAG_SWITCH_OPENS_DOOR_HOLD:
        raise ValueError("Ice Palace Block Puzzle first room tag is not Switch opens door (hold)")
    if ROOM_TAGS[AGA_TOWER_DARK_BRIDGE_ROOM_ID].tag_1 != TAG_NE_KILL_ENEMY_TO_OPEN:
        raise ValueError("Agahnim's Tower Dark Bridge first room tag is not NE Kill enemies to open")
    if ROOM_TAGS[AGA_TOWER_DARK_BRIDGE_ROOM_ID].tag_2 != TAG_W_MOVE_BLOCK_TO_OPEN:
        raise ValueError("Agahnim's Tower Dark Bridge second room tag is not W Move a block to open")
    if ROOM_TAGS[MISERY_MIRE_TILE_ROOM_ID].tag_1 != TAG_LIGHT_TORCHES_TO_OPEN:
        raise ValueError("Misery Mire Tile Room first room tag is not Light torches to open")
    if ROOM_TAGS[MISERY_MIRE_MAIN_LOBBY_ROOM_ID].tag_1 != TAG_TRIGGER_ACTIVATED_CHEST:
        raise ValueError("Misery Mire Main Lobby first room tag is not Trigger-activated chest")
    if ROOM_TAGS[TURTLE_ROCK_TORCH_PUZZLE_ROOM_ID].tag_1 != TAG_LIGHT_TORCHES_TO_OPEN:
        raise ValueError("Turtle Rock Torch Puzzle first room tag is not Light torches to open")
    if ROOM_TAGS[ICE_PALACE_HOLE_TO_KHOLDSTARE_ROOM_ID].tag_1 != TAG_PULL_LEVER_TO_OPEN:
        raise ValueError("Ice Palace Hole to Kholdstare first room tag is not Pull a lever to open")
    if ROOM_TAGS[AGA_TOWER_DARK_MAZE_ROOM_ID].tag_1 != TAG_W_MOVE_BLOCK_TO_OPEN:
        raise ValueError("Agahnim's Tower Dark Maze first room tag is not W Move a block to open")
    if ROOM_TAGS[EASTERN_PRE_ARMOS_ROOM_ID].tag_1 != TAG_E_KILL_ENEMY_TO_OPEN:
        raise ValueError("Eastern Palace Pre-Armos first room tag is not E Kill enemies to open")
    if ROOM_TAGS[EASTERN_PRE_BOSS_ROOM_ID].tag_1 != TAG_SWITCH_OPENS_DOOR_TOGGLE:
        raise ValueError("Eastern Palace Pre-Boss first room tag is not Switch opens door (toggle)")
    if ROOM_TAGS[EASTERN_SWITCH_ROOM_ID].tag_1 != TAG_SWITCH_OPENS_DOOR_TOGGLE:
        raise ValueError("Eastern Palace Switch Room first room tag is not Switch opens door (toggle)")
    if ROOM_TAGS[HYRULE_CASTLE_SWITCH_ROOM_ID].tag_1 != TAG_PULL_LEVER_TO_OPEN:
        raise ValueError("Hyrule Castle Switch Room first room tag is not Pull a lever to open")
    turtle_rock_crystaroller_tags = ROOM_TAGS[TURTLE_ROCK_CRYSTAROLLER_ROOM_ID]
    if turtle_rock_crystaroller_tags.tag_1 != TAG_SE_KILL_ENEMY_TO_MOVE_BLOCK:
        raise ValueError("Turtle Rock Crystaroller first room tag is not SE Kill enemies to move block")
    if turtle_rock_crystaroller_tags.tag_2 != TAG_PULL_LEVER_TO_OPEN:
        raise ValueError("Turtle Rock Crystaroller second room tag is not Pull a lever to open")
    if ROOM_TAGS[SWAMP_FLOODWAY_ROOM_ID].tag_2 != TAG_WATER_TWIN:
        raise ValueError("Swamp Floodway second room tag is not Water twin")
    if ROOM_TAGS[POD_STALFOS_TRAP_ROOM_ID].tag_1 != TAG_TRIGGER_ACTIVATED_CHEST:
        raise ValueError("Palace of Darkness Stalfos Trap first room tag is not Trigger-activated chest")
    if ROOM_TAGS[POD_TURTLE_ROOM_ID].tag_1 != TAG_SW_KILL_ENEMY_TO_OPEN:
        raise ValueError("Palace of Darkness Turtle Room first room tag is not SW Kill enemies to open")
    pod_mimics_moving_wall_tags = ROOM_TAGS[POD_MIMICS_MOVING_WALL_ROOM_ID]
    if pod_mimics_moving_wall_tags.tag_1 != TAG_SW_KILL_ENEMY_TO_OPEN:
        raise ValueError("Palace of Darkness Mimics Moving Wall first room tag is not SW Kill enemies to open")
    if pod_mimics_moving_wall_tags.tag_2 != TAG_SECRET_WALL_RIGHT:
        raise ValueError("Palace of Darkness Mimics Moving Wall second room tag is not Secret wall (right)")
    ice_palace_bomb_floor_tags = ROOM_TAGS[ICE_PALACE_BOMB_FLOOR_ROOM_ID]
    if ice_palace_bomb_floor_tags.tag_1 != TAG_SWITCH_OPENS_DOOR_TOGGLE:
        raise ValueError("Ice Palace Bomb Floor first room tag is not Switch opens door (toggle)")
    if ice_palace_bomb_floor_tags.tag_2 != 0:
        raise ValueError("Ice Palace Bomb Floor second room tag is not Nothing")
    if ROOM_TAGS[ICE_PALACE_PENGATOR_BIG_KEY_ROOM_ID].tag_1 != TAG_SWITCH_OPENS_DOOR_TOGGLE:
        raise ValueError("Ice Palace Pengator Big Key Room first room tag is not Switch opens door (toggle)")


def _decode_position(position) -> tuple[int, int] | None:
    if position is None:
        return None
    return int(position[0]), int(position[1])


def _choose_switch_pot(
    world: "ALTTPWorld",
    room_id: int,
    target_positions: frozenset[tuple[int, int]],
    allow_key: bool = True,
) -> tuple[int, int] | None:
    candidates = _filled_pot_positions_in_target(world, room_id, target_positions, allow_key=allow_key)
    if not candidates:
        return None
    return world.random.choice(candidates)


def _choose_optional_switch_pot(
    world: "ALTTPWorld",
    room_id: int,
    target_positions: frozenset[tuple[int, int]],
    allow_key: bool = True,
) -> tuple[int, int] | None:
    candidates = _filled_pot_positions_in_target(world, room_id, target_positions, allow_key=allow_key)
    return world.random.choice((None,) + tuple(candidates))


def _choose_skull_woods_big_chest_switch_pot(world: "ALTTPWorld") -> tuple[int, int] | None:
    if not _skull_woods_big_chest_has_rope_trap_compatible_sprite_group(world):
        return None
    return _choose_switch_pot(
        world,
        SKULL_WOODS_BIG_CHEST_ROOM_ID,
        SKULL_WOODS_BIG_CHEST_NORTHWEST_SWITCH_POTS,
        allow_key=False,
    )


def _choose_skull_woods_big_chest_rope_trap_sprite(world: "ALTTPWorld") -> int | None:
    if not _skull_woods_big_chest_has_rope_trap_compatible_sprite_group(world):
        return None
    enemy_shuffle_state = getattr(world, "enemy_shuffle_state", None)
    room = enemy_shuffle_state.randomized_dungeon_rooms.get(SKULL_WOODS_BIG_CHEST_ROOM_ID)
    if room is None:
        return None
    candidates = tuple(
        sprite.address for sprite in room.sprites
        if sprite.address != SKULL_WOODS_BIG_CHEST_PULL_SWITCH_GOOD_SPRITE_ADDRESS
    )
    if not candidates:
        return None
    return world.random.choice(candidates)


def _skull_woods_big_chest_has_rope_trap_compatible_sprite_group(world: "ALTTPWorld") -> bool:
    enemy_shuffle_state = getattr(world, "enemy_shuffle_state", None)
    if enemy_shuffle_state is None:
        return False
    room = enemy_shuffle_state.randomized_dungeon_rooms.get(SKULL_WOODS_BIG_CHEST_ROOM_ID)
    if room is None:
        return False
    group = enemy_shuffle_state.sprite_groups.get(room.graphics_block_id + 0x40)
    return (
        group is not None
        and group.subgroup_2 in SKULL_WOODS_BIG_CHEST_ROPE_TRAP_COMPATIBLE_SUBGROUP_2
    )


def _filled_pot_positions_in_target(
    world: "ALTTPWorld",
    room_id: int,
    target_positions: frozenset[tuple[int, int]],
    allow_key: bool = True,
) -> list[tuple[int, int]]:
    return [
        (pot.x, pot.y)
        for pot in _get_current_pot_items(world, room_id)
        if (pot.x, pot.y) in target_positions
        and (allow_key or pot.item != POT_KEY)
    ]


def _get_current_pot_items(world: "ALTTPWorld", room_id: int) -> tuple[FilledPot, ...]:
    pot_shuffle_state = getattr(world, "pot_shuffle_state", None)
    if pot_shuffle_state and room_id in pot_shuffle_state:
        return pot_shuffle_state[room_id]
    return get_vanilla_pot_items(room_id)


def get_eastern_big_chest_room_tag_choices(world: "ALTTPWorld") -> tuple[int, ...]:
    if (
        _filled_pot_positions_in_target(
            world,
            EASTERN_BIG_CHEST_ROOM_ID,
            EASTERN_BIG_CHEST_LEFT_SWITCH_POTS,
            allow_key=False,
        )
        and _filled_pot_positions_in_target(
            world,
            EASTERN_BIG_CHEST_ROOM_ID,
            EASTERN_BIG_CHEST_RIGHT_SWITCH_POTS,
            allow_key=False,
        )
    ):
        return EASTERN_BIG_CHEST_ROOM_TAG_CHOICES
    return (TAG_SWITCH_OPENS_DOOR_TOGGLE,)


def _replace_pot_item(pots: tuple[FilledPot, ...], position: tuple[int, int], item: int) -> tuple[FilledPot, ...]:
    x, y = position
    return tuple(
        FilledPot(pot.x, pot.y, item if (pot.x, pot.y) == (x, y) else pot.item)
        for pot in pots
    )


def _replace_pot_item_value(pots: tuple[FilledPot, ...], old_item: int, new_item: int) -> tuple[FilledPot, ...]:
    return tuple(
        FilledPot(pot.x, pot.y, new_item if pot.item == old_item else pot.item)
        for pot in pots
    )


def _replace_switch_pots_for_puzzle_state(
    pot_state: dict[int, tuple[FilledPot, ...]],
    state: PuzzleShuffleState,
) -> None:
    replacements = (
        (TURTLE_ROCK_BIG_CHEST_ROOM_ID, state.turtle_rock_big_chest_room_switch_pot, True),
        (SWAMP_STATUE_ROOM_ID, None, state.swamp_statue_room_tag in HERA_SWITCH_TAG_CHOICES),
        (POD_MAP_CHEST_ROOM_ID, None, state.pod_map_chest_room_tag in HERA_SWITCH_TAG_CHOICES),
        (EASTERN_BIG_CHEST_ROOM_ID, state.eastern_big_chest_left_switch_pot, state.eastern_big_chest_room_tag == TAG_SWITCH_OPENS_DOOR_HOLD),
        (EASTERN_BIG_CHEST_ROOM_ID, state.eastern_big_chest_right_switch_pot, state.eastern_big_chest_room_tag == TAG_SWITCH_OPENS_DOOR_HOLD),
        (GT_TILE_TORCH_PUZZLE_ROOM_ID, state.gt_tile_torch_puzzle_switch_pot, state.gt_tile_torch_puzzle_tag in HERA_SWITCH_TAG_CHOICES),
        (GT_TORCHES_1_ROOM_ID, state.gt_torches_1_switch_pot, state.gt_torches_1_tag in HERA_SWITCH_TAG_CHOICES),
        (HERA_HARDHAT_BEETLES_ROOM_ID, state.hera_hardhat_beetles_room_switch_pot, state.hera_hardhat_beetles_room_tag_2 in HERA_SWITCH_TAG_CHOICES),
        (ICE_PALACE_CONVEYOR_HELLWAY_ROOM_ID, state.ice_palace_conveyor_hellway_switch_pot, state.ice_palace_conveyor_hellway_tag in HERA_SWITCH_TAG_CHOICES),
        (ICE_PALACE_MAP_ROOM_ID, None, state.ice_palace_map_room_tag == TAG_TRIGGER_ACTIVATED_CHEST),
        (THIEVES_TOWN_JAIL_CELLS_ROOM_ID, state.thieves_town_jail_cells_switch_pot, state.thieves_town_jail_cells_tag in HERA_SWITCH_TAG_CHOICES),
        (SKULL_WOODS_GIBDO_TORCH_ROOM_ID, state.skull_woods_gibdo_torch_room_switch_pot, state.skull_woods_gibdo_torch_room_tag in HERA_SWITCH_TAG_CHOICES),
        (POD_SOUTH_MIMICS_ROOM_ID, state.pod_south_mimics_room_switch_pot, state.pod_south_mimics_room_tag in HERA_SWITCH_TAG_CHOICES),
        (POD_MIMICS_MOVING_WALL_ROOM_ID, state.pod_mimics_moving_wall_switch_pot, state.pod_mimics_moving_wall_room_tag in HERA_SWITCH_TAG_CHOICES),
        (ICE_PALACE_PENGATOR_BIG_KEY_ROOM_ID, None, state.ice_palace_pengator_big_key_room_tag in HERA_SWITCH_TAG_CHOICES),
        (ICE_PALACE_BOMB_JUMP_ROOM_ID, None, state.ice_palace_bomb_jump_room_tag in HERA_SWITCH_TAG_CHOICES),
        (ICE_PALACE_BLOCK_PUZZLE_ROOM_ID, None, state.ice_palace_block_puzzle_tag in HERA_SWITCH_TAG_CHOICES),
        (SKULL_WOODS_BIG_KEY_ROOM_ID, None, state.skull_woods_big_key_room_tag in HERA_SWITCH_TAG_CHOICES),
        (SKULL_WOODS_BIG_CHEST_ROOM_ID, state.skull_woods_big_chest_room_switch_pot, state.skull_woods_big_chest_room_tag_2 == TAG_USE_SWITCH_TO_BOMB_WALL),
        (GT_GAUNTLET_123_ROOM_ID, state.gt_gauntlet_123_room_northwest_switch_pot, state.gt_gauntlet_123_room_variant == ROOM_VARIANT_TOGGLE_SWITCH),
        (GT_GAUNTLET_123_ROOM_ID, state.gt_gauntlet_123_room_southwest_switch_pot, state.gt_gauntlet_123_room_variant in (ROOM_VARIANT_TOGGLE_SWITCH, ROOM_VARIANT_KILL_ENEMIES)),
        (THIEVES_TOWN_WEST_ATTIC_ROOM_ID, None, state.thieves_town_west_attic_room_tag in HERA_SWITCH_TAG_CHOICES),
        (GT_MIMICS_ROOM_ID, state.gt_mimics_room_northwest_switch_pot, state.gt_mimics_room_variant in (2, 4)),
        (GT_MIMICS_ROOM_ID, state.gt_mimics_room_southeast_switch_pot, state.gt_mimics_room_variant == 4),
        (GT_GAUNTLET_45_ROOM_ID, state.gt_gauntlet_45_room_switch_pot, state.gt_gauntlet_45_room_variant == ROOM_VARIANT_TOGGLE_SWITCH),
        (GT_WINDER_WARP_MAZE_ROOM_ID, state.gt_winder_warp_maze_southeast_switch_pot, state.gt_winder_warp_maze_tag_1 in HERA_SWITCH_TAG_CHOICES),
        (GT_WINDER_WARP_MAZE_ROOM_ID, state.gt_winder_warp_maze_north_switch_pot, state.gt_winder_warp_maze_tag_2 == TAG_TRIGGER_ACTIVATED_CHEST),
    )
    for room_id, switch_pot, keep_switch in replacements:
        pots = pot_state.get(room_id)
        if pots is None:
            continue
        if switch_pot is not None and keep_switch:
            pot_state[room_id] = _replace_pot_item(pots, switch_pot, POT_SWITCH)
        elif not keep_switch:
            pot_state[room_id] = _replace_pot_item_value(pots, POT_SWITCH, state.switch_replacement_item)
    if (
        state.pod_map_chest_room_tag == TAG_SWITCH_OPENS_DOOR_TOGGLE
        and state.pod_map_chest_room_switch_pot is not None
    ):
        pots = pot_state.get(POD_MAP_CHEST_ROOM_ID)
        if pots is not None:
            pots = _replace_pot_item_value(pots, POT_SWITCH, state.switch_replacement_item)
            pot_state[POD_MAP_CHEST_ROOM_ID] = _replace_pot_item(
                pots,
                state.pod_map_chest_room_switch_pot,
                POT_SWITCH,
            )


def _has_randomized_killable_enemy(world: "ALTTPWorld", room_id: int, target_name: str) -> bool:
    enemy_shuffle_state = getattr(world, "enemy_shuffle_state", None)
    if not getattr(world.options, "enemy_shuffle", False) or enemy_shuffle_state is None:
        return False
    if room_id not in enemy_shuffle_state.randomized_dungeon_rooms:
        return False
    from .StateHelpers import _enemy_requirement_counts_for_room_clear

    return any(
        _enemy_requirement_counts_for_room_clear(enemy)
        for enemy in get_enemy_clear_target_enemies(world, target_name)
    )


def _room_needs_direct_pot_patch(room_id: int, state: PuzzleShuffleState) -> bool:
    if room_id == HERA_TILE_ROOM_ID:
        return state.hera_big_key_chest_switch_pot is not None or state.hera_tile_room_switch_pot is not None
    if room_id == GT_BLOCK_PUZZLE_ROOM_ID:
        return state.gt_block_puzzle_switch_pot is not None
    if room_id == GT_BIG_CHEST_ROOM_ID:
        return state.gt_big_chest_room_tag not in HERA_SWITCH_TAG_CHOICES
    if room_id == GT_TILE_TORCH_PUZZLE_ROOM_ID:
        return state.gt_tile_torch_puzzle_switch_pot is not None
    if room_id == MISERY_MIRE_DARK_CANE_ROOM_ID:
        return (
            state.misery_mire_dark_cane_room_switch_pot is not None
            or state.misery_mire_dark_cane_room_tag not in HERA_SWITCH_TAG_CHOICES
        )
    if room_id == GT_TORCHES_1_ROOM_ID:
        return state.gt_torches_1_switch_pot is not None
    if room_id == ICE_PALACE_ICE_FLOOR_ROOM_ID:
        return state.ice_palace_ice_floor_room_tag == TAG_SW_KILL_ENEMY_TO_OPEN
    if room_id == EASTERN_STALFOS_ROOM_ID:
        return state.eastern_stalfos_room_switch_pot is not None
    if room_id == EASTERN_BIG_CHEST_ROOM_ID:
        return (
            state.eastern_big_chest_left_switch_pot is not None
            or state.eastern_big_chest_right_switch_pot is not None
        )
    if room_id == MISERY_MIRE_SPIKE_CHEST_ROOM_ID:
        return state.misery_mire_spike_chest_room_tag != TAG_TRIGGER_ACTIVATED_CHEST
    if room_id == TURTLE_ROCK_TORCH_PUZZLE_ROOM_ID:
        return state.turtle_rock_torch_puzzle_switch_pot is not None
    if room_id == ICE_PALACE_HOLE_TO_KHOLDSTARE_ROOM_ID:
        return state.ice_palace_hole_to_kholdstare_switch_pot is not None
    if room_id == EASTERN_PRE_ARMOS_ROOM_ID:
        return (
            state.eastern_pre_armos_northeast_switch_pot is not None
            or state.eastern_pre_armos_southeast_switch_pot is not None
        )
    if room_id in {
        TURTLE_ROCK_BIG_CHEST_ROOM_ID,
        SWAMP_STATUE_ROOM_ID,
        POD_MAP_CHEST_ROOM_ID,
        HERA_HARDHAT_BEETLES_ROOM_ID,
        ICE_PALACE_CONVEYOR_HELLWAY_ROOM_ID,
        ICE_PALACE_MAP_ROOM_ID,
        THIEVES_TOWN_JAIL_CELLS_ROOM_ID,
        SKULL_WOODS_GIBDO_TORCH_ROOM_ID,
        POD_SOUTH_MIMICS_ROOM_ID,
        POD_MIMICS_MOVING_WALL_ROOM_ID,
        ICE_PALACE_PENGATOR_BIG_KEY_ROOM_ID,
        ICE_PALACE_BOMB_JUMP_ROOM_ID,
        ICE_PALACE_BLOCK_PUZZLE_ROOM_ID,
        SKULL_WOODS_BIG_KEY_ROOM_ID,
        SKULL_WOODS_BIG_CHEST_ROOM_ID,
        GT_GAUNTLET_123_ROOM_ID,
        THIEVES_TOWN_WEST_ATTIC_ROOM_ID,
        GT_MIMICS_ROOM_ID,
        GT_GAUNTLET_45_ROOM_ID,
        GT_WINDER_WARP_MAZE_ROOM_ID,
    }:
        modified = {room_id: get_vanilla_pot_items(room_id)}
        _replace_switch_pots_for_puzzle_state(modified, state)
        return modified[room_id] != get_vanilla_pot_items(room_id)
    return False


def _get_pots_with_puzzle_modifications(room_id: int, state: PuzzleShuffleState) -> tuple[FilledPot, ...]:
    pots = get_vanilla_pot_items(room_id)
    if room_id == DESERT_MAP_CHEST_ROOM_ID and not desert_map_chest_uses_switch(state):
        pots = _replace_pot_item_value(pots, POT_SWITCH, state.switch_replacement_item)
    if room_id == HERA_TILE_ROOM_ID and state.hera_big_key_chest_switch_pot is not None:
        pots = _replace_pot_item(pots, state.hera_big_key_chest_switch_pot, POT_SWITCH)
    if room_id == HERA_TILE_ROOM_ID and state.hera_tile_room_switch_pot is not None:
        pots = _replace_pot_item(pots, state.hera_tile_room_switch_pot, POT_SWITCH)
    if room_id == GT_BLOCK_PUZZLE_ROOM_ID and state.gt_block_puzzle_switch_pot is not None:
        pots = _replace_pot_item(pots, state.gt_block_puzzle_switch_pot, POT_SWITCH)
    if room_id == GT_BIG_CHEST_ROOM_ID and state.gt_big_chest_room_tag not in HERA_SWITCH_TAG_CHOICES:
        pots = _replace_pot_item_value(pots, GT_BIG_CHEST_ROOM_SWITCH_POT_ITEM, state.switch_replacement_item)
    if room_id == GT_TILE_TORCH_PUZZLE_ROOM_ID and state.gt_tile_torch_puzzle_switch_pot is not None:
        pots = _replace_pot_item(pots, state.gt_tile_torch_puzzle_switch_pot, POT_SWITCH)
    if room_id == MISERY_MIRE_DARK_CANE_ROOM_ID and state.misery_mire_dark_cane_room_switch_pot is not None:
        pots = _replace_pot_item_value(pots, POT_SWITCH, state.switch_replacement_item)
        pots = _replace_pot_item(pots, state.misery_mire_dark_cane_room_switch_pot, POT_SWITCH)
    if room_id == MISERY_MIRE_DARK_CANE_ROOM_ID and state.misery_mire_dark_cane_room_tag not in HERA_SWITCH_TAG_CHOICES:
        pots = _replace_pot_item_value(pots, POT_SWITCH, state.switch_replacement_item)
    if room_id == GT_TORCHES_1_ROOM_ID and state.gt_torches_1_switch_pot is not None:
        pots = _replace_pot_item(pots, state.gt_torches_1_switch_pot, POT_SWITCH)
    if room_id == ICE_PALACE_ICE_FLOOR_ROOM_ID and state.ice_palace_ice_floor_room_tag == TAG_SW_KILL_ENEMY_TO_OPEN:
        pots = _replace_pot_item_value(pots, POT_SWITCH, state.switch_replacement_item)
    if room_id == EASTERN_STALFOS_ROOM_ID and state.eastern_stalfos_room_switch_pot is not None:
        pots = _replace_pot_item(pots, state.eastern_stalfos_room_switch_pot, POT_SWITCH)
    if room_id == MISERY_MIRE_SPIKE_CHEST_ROOM_ID and state.misery_mire_spike_chest_room_tag != TAG_TRIGGER_ACTIVATED_CHEST:
        pots = _replace_pot_item_value(pots, POT_SWITCH, state.switch_replacement_item)
    if room_id == TURTLE_ROCK_TORCH_PUZZLE_ROOM_ID and state.turtle_rock_torch_puzzle_switch_pot is not None:
        pots = _replace_pot_item(pots, state.turtle_rock_torch_puzzle_switch_pot, POT_SWITCH)
    if room_id == ICE_PALACE_HOLE_TO_KHOLDSTARE_ROOM_ID and state.ice_palace_hole_to_kholdstare_switch_pot is not None:
        pots = _replace_pot_item(pots, state.ice_palace_hole_to_kholdstare_switch_pot, POT_SWITCH)
    if room_id == EASTERN_PRE_ARMOS_ROOM_ID and state.eastern_pre_armos_northeast_switch_pot is not None:
        pots = _replace_pot_item(pots, state.eastern_pre_armos_northeast_switch_pot, POT_SWITCH)
    if room_id == EASTERN_PRE_ARMOS_ROOM_ID and state.eastern_pre_armos_southeast_switch_pot is not None:
        pots = _replace_pot_item(pots, state.eastern_pre_armos_southeast_switch_pot, POT_SWITCH)
    modified = {room_id: pots}
    _replace_switch_pots_for_puzzle_state(modified, state)
    pots = modified[room_id]
    return pots
