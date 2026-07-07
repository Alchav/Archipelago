from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import ALTTPWorld
    from .EnemyShuffle import EffectiveDungeonEnemySprite


@dataclass(frozen=True)
class EnemyClearTarget:
    name: str
    room_name: str
    min_x: int = 0
    max_x: int | None = None
    min_y: int = 0
    max_y: int | None = None

    def contains(self, enemy: "EffectiveDungeonEnemySprite") -> bool:
        if enemy.x_coord_pixels < self.min_x or enemy.y_coord_pixels < self.min_y:
            return False
        if self.max_x is not None and enemy.x_coord_pixels >= self.max_x:
            return False
        if self.max_y is not None and enemy.y_coord_pixels >= self.max_y:
            return False
        return True


@dataclass(frozen=True)
class KeyDropEnemyTarget:
    location_name: str
    room_name: str
    x_coord_pixels: int
    y_coord_pixels: int

    def matches(self, enemy: "EffectiveDungeonEnemySprite") -> bool:
        return (
            enemy.x_coord_pixels == self.x_coord_pixels
            and enemy.y_coord_pixels == self.y_coord_pixels
        )


MIMIC_CAVE_ROOM = "Mimic Cave"
MINI_MOLDORM_CAVE_ROOM = "Mini-Moldorm Cave"
AGA_TOWER_ENTRANCE_TOP_LEFT = "Agahnim's Tower (Second Room)"
AGA_TOWER_CIRCLE_OF_POTS_TOP_HALF = "Agahnim's Tower (Pre-Circle of Pots)"
AGA_TOWER_CIRCLE_OF_POTS_SOUTHWEST = "Agahnim's Tower (Pre-Circle of Pots) - Southwest"
EASTERN_BIG_KEY_ROOM = "Eastern Palace (Big Key Room)"
EASTERN_BIG_KEY_ROOM_EAST = "Eastern Palace (Big Key Room) - East"
EASTERN_STALFOS_ROOM_SOUTHWEST = "Eastern Palace (Stalfos Spawn Room) - Southwest"
EASTERN_DARK_SQUARE_NORTHWEST = "Eastern Palace (Dark Square Room) - Northwest"
EASTERN_PRE_ARMOS_ROOM = "Eastern Palace (Pre-Armos Knights Rooms)"
ICE_PALACE_BLOCK_PUZZLE_SOUTHEAST = "Ice Palace (Block Puzzle Room) - Southeast"
ICE_PALACE_BOMB_FLOOR_SOUTHWEST = "Ice Palace (Bomb Floor / Bari Room) - Southwest"
ICE_PALACE_BIG_KEY_ROOM_SOUTHWEST = "Ice Palace (Pengator / Big Key Room) - Southwest"
DESERT_EAST_ENTRANCE_TOP_RIGHT = "Desert Palace (Compass Room)"
DESERT_MAP_CHEST_NORTH_HALF = "Desert Palace (Map Chest Room)"
DESERT_BIG_CHEST_BOTTOM_LEFT = "Desert Palace (Big Chest Room)"
DESERT_BEAMOS_HELLWAY_BOTTOM_LEFT = "Desert Palace (4 Statues Room)"
DESERT_FINAL_SECTION_ENTRANCE_SOUTHWEST = "Desert Palace (Final Section Entrance Room) - Southwest"
HERA_HARDHAT_BEETLES_BOTTOM_RIGHT = "Tower of Hera (Hardhat Beetles Room)"
HERA_TILE_ROOM_SOUTHEAST = "Tower of Hera (Tile Room) - Southeast"
TURTLE_ROCK_BIG_CHEST_ROOM_TOP_LEFT = "Turtle Rock (Double Hokku-Bokku Room)"
SWAMP_STATUE_ROOM_SOUTH = "Swamp Palace (Statue Room) - South"
SWAMP_COMPASS_CHEST_NORTH = "Swamp Palace (Compass Chest Room) - North"
SWAMP_HIDDEN_DOOR_ROOM_SOUTH = "Swamp Palace (Hidden Door Room) - South"
ICE_PALACE_COMPASS_ROOM = "Ice Palace (Compass Room)"
ICE_PALACE_MAP_ROOM_WEST = "Ice Palace (Map Chest Room) - West"
ICE_PALACE_HIDDEN_CHEST_ROOM = "Ice Palace (Hidden Chest Room)"
ICE_PALACE_SPIKE_ROOM_SOUTHWEST = "Ice Palace (Spike Room) - Southwest"
ICE_PALACE_BOMB_JUMP_ROOM_NORTHWEST = "Ice Palace (Bomb Jump Room) - Northwest"
ICE_PALACE_ICED_T_ROOM_SOUTHWEST = "Ice Palace (Iced T Room) - Southwest"
ICE_PALACE_PENGATORS_ROOM = "Ice Palace (Pengators Room)"
ICE_PALACE_CONVEYOR_HELLWAY_TOP_RIGHT = "Ice Palace (Conveyor Hellway)"
POD_NORTH_MIMICS_BOTTOM_LEFT = "Palace of Darkness (North Mimics Room)"
POD_MAP_CHEST_ROOM_WEST = "Palace of Darkness (Map Chest Room) - West"
POD_TURTLE_ROOM_BOTTOM_LEFT = "Palace of Darkness (Turtle Room)"
POD_SOUTH_MIMICS_TOP_LEFT = "Palace of Darkness (South Mimics Room)"
POD_STALFOS_TRAP_ROOM = "Palace of Darkness (Stalfos Trap Room)"
MISERY_MIRE_WIZZROBES_ROOM = "Misery Mire (Wizzrobes Room)"
MISERY_MIRE_MAIN_LOBBY_ROOM = "Misery Mire (Main Lobby)"
MISERY_MIRE_BRIDGE_CHEST_SOUTHEAST = "Misery Mire (Bridge Chest Room) - Southeast"
MISERY_MIRE_SPIKE_CHEST_ROOM = "Misery Mire (Spike Chest Room)"
MISERY_MIRE_DARK_CANE_ROOM_NORTH = "Misery Mire (Dark Cane Room) - North"
GANONS_TOWER_WIZZROBES_TOP_HALF = "Ganon's Tower (Wizzrobes Rooms)"
GANONS_TOWER_GAUNTLET_123_ROOM = "Ganon's Tower (Gauntlet 1/2/3)"
GANONS_TOWER_GAUNTLET_123_NORTH = "Ganon's Tower (Gauntlet 1/2/3) - North"
GANONS_TOWER_GAUNTLET_123_NORTHEAST = "Ganon's Tower (Gauntlet 1/2/3) - Northeast"
GANONS_TOWER_GAUNTLET_45_ROOM = "Ganon's Tower (Gauntlet 4/5)"
GANONS_TOWER_GAUNTLET_45_NORTHWEST = "Ganon's Tower (Gauntlet 4/5) - Northwest"
GANONS_TOWER_BLOCK_PUZZLE_NORTHEAST = "Ganon's Tower (Block Puzzle Room) - Northeast"
GANONS_TOWER_BIG_CHEST_ROOM_NORTHEAST = "Ganon's Tower (Big Chest Room) - Northeast"
GANONS_TOWER_SPIKE_PIT_EAST = "Ganon's Tower (Spike Pit Room) - East"
GANONS_TOWER_MIMICS_BOTTOM_HALF = "Ganon's Tower (Mimics Rooms) - Bottom Half"
GANONS_TOWER_MIMICS_NORTHWEST = "Ganon's Tower (Mimics Rooms) - Northwest"
GANONS_TOWER_MIMICS_SOUTHWEST = "Ganon's Tower (Mimics Rooms) - Southwest"
GANONS_TOWER_MIMICS_WEST = "Ganon's Tower (Mimics Rooms) - West"
GANONS_TOWER_TILE_TORCH_PUZZLE_TOP_LEFT = "Ganon's Tower (Tile / Torch Puzzle Room) - Top Left"
GANONS_TOWER_WINDER_WARP_MAZE_NORTH = "Ganon's Tower (Winder / Warp Maze Room) - North"
ICE_PALACE_ICE_FLOOR_ROOM_SOUTHWEST = "Ice Palace (Room with ice floor, key, and 4 wall rats) - Southwest"
HYRULE_CASTLE_PRE_BOOMERANG_CHEST_ROOM = "Hyrule Castle (Pre-Boomerang Chest Room)"
HYRULE_CASTLE_SWITCH_ROOM_SOUTH = "Hyrule Castle (Switch Room) - South"
THIEVES_TOWN_JAIL_CELLS_TOP_LEFT = "Thieves Town (Basement)"
THIEVES_TOWN_WEST_ATTIC_SOUTHWEST = "Thieves Town (West Attic Room) - Southwest"
SKULL_WOODS_GIBDO_TORCH_EAST = "Skull Woods (Gibdo Torch Puzzle Room) - East"
SKULL_WOODS_BIG_KEY_ROOM_SOUTHWEST = "Skull Woods (Big Key Room) - Southwest"

HYRULE_CASTLE_MAP_GUARD_KEY_DROP = "Hyrule Castle - Map Guard Key Drop"
HYRULE_CASTLE_BOOMERANG_GUARD_KEY_DROP = "Hyrule Castle - Boomerang Guard Key Drop"
SEWERS_KEY_RAT_KEY_DROP = "Sewers - Key Rat Key Drop"
HYRULE_CASTLE_BIG_KEY_DROP = "Hyrule Castle - Big Key Drop"
EASTERN_DARK_EYEGORE_KEY_DROP = "Eastern Palace - Dark Eyegore Key Drop"
CASTLE_TOWER_DARK_ARCHER_KEY_DROP = "Castle Tower - Dark Archer Key Drop"
CASTLE_TOWER_CIRCLE_OF_POTS_KEY_DROP = "Castle Tower - Circle of Pots Key Drop"
SKULL_WOODS_SPIKE_CORNER_KEY_DROP = "Skull Woods - Spike Corner Key Drop"
ICE_PALACE_JELLY_KEY_DROP = "Ice Palace - Jelly Key Drop"
ICE_PALACE_CONVEYOR_KEY_DROP = "Ice Palace - Conveyor Key Drop"
MISERY_MIRE_CONVEYOR_CRYSTAL_KEY_DROP = "Misery Mire - Conveyor Crystal Key Drop"
TURTLE_ROCK_POKEY_1_KEY_DROP = "Turtle Rock - Pokey 1 Key Drop"
TURTLE_ROCK_POKEY_2_KEY_DROP = "Turtle Rock - Pokey 2 Key Drop"
GANONS_TOWER_MINI_HELMASAUR_KEY_DROP = "Ganons Tower - Mini Helmasaur Key Drop"

ENEMY_CLEAR_TARGETS = (
    EnemyClearTarget(name=MIMIC_CAVE_ROOM, room_name="Mimic Cave"),
    EnemyClearTarget(name=MINI_MOLDORM_CAVE_ROOM, room_name="Mini-Moldorm Cave"),
    EnemyClearTarget(name=AGA_TOWER_ENTRANCE_TOP_LEFT, room_name="Agahnim's Tower (Entrance Room)", max_x=256, max_y=256),
    EnemyClearTarget(name=AGA_TOWER_CIRCLE_OF_POTS_TOP_HALF, room_name="Agahnim's Tower (Circle of Pots)", max_y=256),
    EnemyClearTarget(
        name=AGA_TOWER_CIRCLE_OF_POTS_SOUTHWEST,
        room_name="Agahnim's Tower (Circle of Pots)",
        max_x=256,
        min_y=256,
    ),
    EnemyClearTarget(name=EASTERN_BIG_KEY_ROOM, room_name="Eastern Palace (Big Key Room)"),
    EnemyClearTarget(name=EASTERN_BIG_KEY_ROOM_EAST, room_name="Eastern Palace (Big Key Room)", min_x=256),
    EnemyClearTarget(
        name=EASTERN_STALFOS_ROOM_SOUTHWEST,
        room_name="Eastern Palace (Stalfos Spawn Room)",
        max_x=256,
        min_y=256,
    ),
    EnemyClearTarget(
        name=EASTERN_DARK_SQUARE_NORTHWEST,
        room_name="Eastern Palace (Dark Antifairy / Key Pot Room)",
        max_x=256,
        max_y=256,
    ),
    EnemyClearTarget(
        name=EASTERN_PRE_ARMOS_ROOM,
        room_name="Eastern Palace ('Zeldagamer Room' / Pre-Armos Knights Room)",
        min_x=256,
    ),
    EnemyClearTarget(
        name=ICE_PALACE_BLOCK_PUZZLE_SOUTHEAST,
        room_name="Ice Palace (Block Puzzle Room)",
        min_x=256,
        min_y=256,
    ),
    EnemyClearTarget(
        name=ICE_PALACE_BOMB_FLOOR_SOUTHWEST,
        room_name="Ice Palace (Bomb Floor / Bari Room)",
        max_x=256,
        min_y=256,
    ),
    EnemyClearTarget(
        name=ICE_PALACE_BIG_KEY_ROOM_SOUTHWEST,
        room_name="Ice Palace (Pengator / Big Key Room)",
        max_x=256,
        min_y=256,
    ),
    EnemyClearTarget(name=DESERT_EAST_ENTRANCE_TOP_RIGHT, room_name="Desert Palace (East Entrance Room)", min_x=256, max_y=256),
    EnemyClearTarget(name=DESERT_MAP_CHEST_NORTH_HALF, room_name="Desert Palace (Map Chest Room)", max_y=256),
    EnemyClearTarget(
        name=DESERT_BIG_CHEST_BOTTOM_LEFT,
        room_name="Desert Palace (Big Chest Room)",
        max_x=256,
        min_y=256,
    ),
    EnemyClearTarget(
        name=DESERT_BEAMOS_HELLWAY_BOTTOM_LEFT,
        room_name="Desert Palace (Popos 2 / Beamos Hellway Room)",
        max_x=256,
        min_y=256,
    ),
    EnemyClearTarget(
        name=DESERT_FINAL_SECTION_ENTRANCE_SOUTHWEST,
        room_name="Desert Palace (Final Section Entrance Room)",
        max_x=256,
        min_y=256,
    ),
    EnemyClearTarget(
        name=HERA_HARDHAT_BEETLES_BOTTOM_RIGHT,
        room_name="Tower of Hera (Hardhat Beetles Room)",
        min_x=256,
        min_y=256,
    ),
    EnemyClearTarget(
        name=HERA_TILE_ROOM_SOUTHEAST,
        room_name="Tower of Hera (Tile Room)",
        min_x=256,
        min_y=256,
    ),
    EnemyClearTarget(
        name=TURTLE_ROCK_BIG_CHEST_ROOM_TOP_LEFT,
        room_name="Turtle Rock (Double Hokku-Bokku / Big chest Room)",
        max_x=256,
        max_y=256,
    ),
    EnemyClearTarget(name=SWAMP_STATUE_ROOM_SOUTH, room_name="Swamp Palace (Statue Room)", min_y=256),
    EnemyClearTarget(name=SWAMP_COMPASS_CHEST_NORTH, room_name="Swamp Palace (Compass Chest Room)", max_y=256),
    EnemyClearTarget(name=SWAMP_HIDDEN_DOOR_ROOM_SOUTH, room_name="Swamp Palace (Hidden Chest / Hidden Door Room)", min_y=256),
    EnemyClearTarget(name=ICE_PALACE_COMPASS_ROOM, room_name="Ice Palace (Compass Room)"),
    EnemyClearTarget(name=ICE_PALACE_MAP_ROOM_WEST, room_name="Ice Palace (Map Chest Room)", max_x=256),
    EnemyClearTarget(name=ICE_PALACE_HIDDEN_CHEST_ROOM, room_name="Ice Palace (2 Blue Bari and Hidden Chest)"),
    EnemyClearTarget(
        name=ICE_PALACE_SPIKE_ROOM_SOUTHWEST,
        room_name="Ice Palace (Hidden Chest / Spike Floor Room)",
        max_x=256,
        min_y=256,
    ),
    EnemyClearTarget(
        name=ICE_PALACE_BOMB_JUMP_ROOM_NORTHWEST,
        room_name="Ice Palace (Bomb-Jump Room)",
        max_x=256,
        max_y=256,
    ),
    EnemyClearTarget(
        name=ICE_PALACE_ICED_T_ROOM_SOUTHWEST,
        room_name="Ice Palace (Room with ice floor, key, and 4 wall rats)",
        max_x=256,
        min_y=256,
    ),
    EnemyClearTarget(name=ICE_PALACE_PENGATORS_ROOM, room_name="Ice Palace (Pengators Room)"),
    EnemyClearTarget(
        name=ICE_PALACE_CONVEYOR_HELLWAY_TOP_RIGHT,
        room_name="Ice Palace (Stalfos Knights / Conveyor Hellway)",
        min_x=256,
        max_y=256,
    ),
    EnemyClearTarget(
        name=POD_NORTH_MIMICS_BOTTOM_LEFT,
        room_name="Palace of Darkness (Mimics / Moving Wall Room)",
        max_x=256,
        min_y=256,
    ),
    EnemyClearTarget(name=POD_MAP_CHEST_ROOM_WEST, room_name="Palace of Darkness (Map Chest / Fairy Room)", max_x=256),
    EnemyClearTarget(
        name=POD_TURTLE_ROOM_BOTTOM_LEFT,
        room_name="Palace of Darkness (Turtle Room)",
        max_x=256,
        min_y=256,
    ),
    EnemyClearTarget(
        name=POD_SOUTH_MIMICS_TOP_LEFT,
        room_name="Palace of Darkness (Warps / South Mimics Room)",
        max_x=256,
        max_y=256,
    ),
    EnemyClearTarget(name=POD_STALFOS_TRAP_ROOM, room_name="Palace of Darkness (Stalfos Trap Room)"),
    EnemyClearTarget(
        name=MISERY_MIRE_WIZZROBES_ROOM,
        room_name="Misery Mire (Mire02 / Wizzrobes Room)",
    ),
    EnemyClearTarget(name=MISERY_MIRE_MAIN_LOBBY_ROOM, room_name="Misery Mire (Big Hub Room)"),
    EnemyClearTarget(
        name=MISERY_MIRE_BRIDGE_CHEST_SOUTHEAST,
        room_name="Misery Mire (Slug Room)",
        min_x=256,
        min_y=256,
    ),
    EnemyClearTarget(name=MISERY_MIRE_SPIKE_CHEST_ROOM, room_name="Misery Mire (Spike Key Chest Room)"),
    EnemyClearTarget(
        name=MISERY_MIRE_DARK_CANE_ROOM_NORTH,
        room_name="Misery Mire (Dark Cane Floor Switch Puzzle Room)",
        max_y=256,
    ),
    EnemyClearTarget(
        name=GANONS_TOWER_GAUNTLET_123_ROOM,
        room_name="Ganon's Tower (Gauntlet 1/2/3)",
    ),
    EnemyClearTarget(name=GANONS_TOWER_GAUNTLET_123_NORTH, room_name="Ganon's Tower (Gauntlet 1/2/3)", max_y=256),
    EnemyClearTarget(
        name=GANONS_TOWER_GAUNTLET_123_NORTHEAST,
        room_name="Ganon's Tower (Gauntlet 1/2/3)",
        min_x=256,
        max_y=256,
    ),
    EnemyClearTarget(
        name=GANONS_TOWER_GAUNTLET_45_ROOM,
        room_name="Ganon's Tower (Gauntlet 4/5)",
    ),
    EnemyClearTarget(
        name=GANONS_TOWER_GAUNTLET_45_NORTHWEST,
        room_name="Ganon's Tower (Gauntlet 4/5)",
        max_x=256,
        max_y=256,
    ),
    EnemyClearTarget(
        name=GANONS_TOWER_BLOCK_PUZZLE_NORTHEAST,
        room_name="Ganon's Tower (Block Puzzle / Spike Skip / Map Chest Room)",
        min_x=256,
        max_y=256,
    ),
    EnemyClearTarget(
        name=GANONS_TOWER_BIG_CHEST_ROOM_NORTHEAST,
        room_name="Ganon's Tower (East and West Downstairs / Big Chest Room)",
        min_x=256,
        max_y=256,
    ),
    EnemyClearTarget(name=GANONS_TOWER_SPIKE_PIT_EAST, room_name="Ganon's Tower (Spike Pit Room)", min_x=256),
    EnemyClearTarget(
        name=GANONS_TOWER_MIMICS_BOTTOM_HALF,
        room_name="Ganon's Tower (Mimics Rooms)",
        min_y=256,
    ),
    EnemyClearTarget(
        name=GANONS_TOWER_MIMICS_NORTHWEST,
        room_name="Ganon's Tower (Mimics Rooms)",
        max_x=256,
        max_y=256,
    ),
    EnemyClearTarget(
        name=GANONS_TOWER_MIMICS_SOUTHWEST,
        room_name="Ganon's Tower (Mimics Rooms)",
        max_x=256,
        min_y=256,
    ),
    EnemyClearTarget(name=GANONS_TOWER_MIMICS_WEST, room_name="Ganon's Tower (Mimics Rooms)", max_x=256),
    EnemyClearTarget(
        name=GANONS_TOWER_TILE_TORCH_PUZZLE_TOP_LEFT,
        room_name="Ganon's Tower (Tile / Torch Puzzle Room)",
        max_x=256,
        max_y=256,
    ),
    EnemyClearTarget(
        name=GANONS_TOWER_WINDER_WARP_MAZE_NORTH,
        room_name="Ganon's Tower (Winder / Warp Maze Room)",
        max_y=256,
    ),
    EnemyClearTarget(
        name=ICE_PALACE_ICE_FLOOR_ROOM_SOUTHWEST,
        room_name="Ice Palace (Room with ice floor, key, and 4 wall rats)",
        max_x=256,
        min_y=256,
    ),
    EnemyClearTarget(
        name=THIEVES_TOWN_JAIL_CELLS_TOP_LEFT,
        room_name="Thieves Town (Jail Cells Room)",
        max_x=256,
        max_y=256,
    ),
    EnemyClearTarget(name=GANONS_TOWER_WIZZROBES_TOP_HALF, room_name="Ganon's Tower (Wizzrobes Rooms)", max_y=256),
    EnemyClearTarget(
        name=HYRULE_CASTLE_PRE_BOOMERANG_CHEST_ROOM,
        room_name="Hyrule Castle (Boomerang Chest Room)",
        max_x=256,
        min_y=256,
    ),
    EnemyClearTarget(
        name=HYRULE_CASTLE_SWITCH_ROOM_SOUTH,
        room_name="Hyrule Castle (Switch Room)",
        min_y=256,
    ),
    EnemyClearTarget(
        name=THIEVES_TOWN_WEST_ATTIC_SOUTHWEST,
        room_name="Thieves Town (West Attic Room)",
        max_x=256,
        min_y=256,
    ),
    EnemyClearTarget(name=SKULL_WOODS_GIBDO_TORCH_EAST, room_name="Skull Woods (Gibdo Torch Puzzle Room)", min_x=256),
    EnemyClearTarget(
        name=SKULL_WOODS_BIG_KEY_ROOM_SOUTHWEST,
        room_name="Skull Woods (Big Key Room)",
        max_x=256,
        min_y=256,
    ),
)

ENEMY_CLEAR_TARGET_LOOKUP = {target.name: target for target in ENEMY_CLEAR_TARGETS}

KEY_DROP_ENEMY_TARGETS = (
    KeyDropEnemyTarget(
        location_name=HYRULE_CASTLE_MAP_GUARD_KEY_DROP,
        room_name="Hyrule Castle (Map Chest Room)",
        x_coord_pixels=272,
        y_coord_pixels=96,
    ),
    KeyDropEnemyTarget(
        location_name=HYRULE_CASTLE_BOOMERANG_GUARD_KEY_DROP,
        room_name="Hyrule Castle (Boomerang Chest Room)",
        x_coord_pixels=416,
        y_coord_pixels=384,
    ),
    KeyDropEnemyTarget(
        location_name=SEWERS_KEY_RAT_KEY_DROP,
        room_name="Hyrule Castle (Key-rat Room)",
        x_coord_pixels=80,
        y_coord_pixels=96,
    ),
    KeyDropEnemyTarget(
        location_name=HYRULE_CASTLE_BIG_KEY_DROP,
        room_name="Hyrule Castle (Jail Cell Room)",
        x_coord_pixels=416,
        y_coord_pixels=144,
    ),
    KeyDropEnemyTarget(
        location_name=EASTERN_DARK_EYEGORE_KEY_DROP,
        room_name="Eastern Palace (Eyegore Key Room)",
        x_coord_pixels=272,
        y_coord_pixels=368,
    ),
    KeyDropEnemyTarget(
        location_name=CASTLE_TOWER_DARK_ARCHER_KEY_DROP,
        room_name="Agahnim's Tower (Dark Bridge Room)",
        x_coord_pixels=320,
        y_coord_pixels=176,
    ),
    KeyDropEnemyTarget(
        location_name=CASTLE_TOWER_CIRCLE_OF_POTS_KEY_DROP,
        room_name="Agahnim's Tower (Circle of Pots)",
        x_coord_pixels=128,
        y_coord_pixels=384,
    ),
    KeyDropEnemyTarget(
        location_name=SKULL_WOODS_SPIKE_CORNER_KEY_DROP,
        room_name="Skull Woods (Gibdo Key / Mothula Hole Room)",
        x_coord_pixels=80,
        y_coord_pixels=336,
    ),
    KeyDropEnemyTarget(
        location_name=ICE_PALACE_JELLY_KEY_DROP,
        room_name="Ice Palace (Entrance Room)",
        x_coord_pixels=80,
        y_coord_pixels=416,
    ),
    KeyDropEnemyTarget(
        location_name=ICE_PALACE_CONVEYOR_KEY_DROP,
        room_name="Ice Palace (Stalfos Knights / Conveyor Hellway)",
        x_coord_pixels=272,
        y_coord_pixels=384,
    ),
    KeyDropEnemyTarget(
        location_name=MISERY_MIRE_CONVEYOR_CRYSTAL_KEY_DROP,
        room_name="Misery Mire (Compass Chest / Tile Room)",
        x_coord_pixels=304,
        y_coord_pixels=432,
    ),
    KeyDropEnemyTarget(
        location_name=TURTLE_ROCK_POKEY_1_KEY_DROP,
        room_name="Turtle Rock (Chain Chomps Room)",
        x_coord_pixels=112,
        y_coord_pixels=336,
    ),
    KeyDropEnemyTarget(
        location_name=TURTLE_ROCK_POKEY_2_KEY_DROP,
        room_name="Turtle Rock (Hokku-Bokku Key Room 2)",
        x_coord_pixels=352,
        y_coord_pixels=384,
    ),
    KeyDropEnemyTarget(
        location_name=GANONS_TOWER_MINI_HELMASAUR_KEY_DROP,
        room_name="Ganon's Tower (Torch Room 2)",
        x_coord_pixels=368,
        y_coord_pixels=112,
    ),
)

KEY_DROP_ENEMY_TARGET_LOOKUP = {
    target.location_name: target
    for target in KEY_DROP_ENEMY_TARGETS
}


def get_enemy_clear_target(target_name: str) -> EnemyClearTarget:
    return ENEMY_CLEAR_TARGET_LOOKUP[target_name]


def get_key_drop_enemy_target(location_name: str) -> KeyDropEnemyTarget:
    return KEY_DROP_ENEMY_TARGET_LOOKUP[location_name]


def get_enemy_clear_target_enemies(
    world: "ALTTPWorld",
    target_name: str,
) -> tuple["EffectiveDungeonEnemySprite", ...]:
    from .EnemyShuffle import get_effective_dungeon_room_enemies, get_room_id

    target = get_enemy_clear_target(target_name)
    room_id = get_room_id(target.room_name)
    if room_id is None:
        raise ValueError(f"Unknown ALTTP room {target.room_name!r}")

    return tuple(
        enemy
        for enemy in get_effective_dungeon_room_enemies(world, room_id)
        if target.contains(enemy)
    )


def get_key_drop_enemy(
    world: "ALTTPWorld",
    location_name: str,
) -> "EffectiveDungeonEnemySprite | None":
    from .EnemyShuffle import get_effective_dungeon_room_enemies, get_room_id

    target = get_key_drop_enemy_target(location_name)
    room_id = get_room_id(target.room_name)
    if room_id is None:
        raise ValueError(f"Unknown ALTTP room {target.room_name!r}")

    for enemy in get_effective_dungeon_room_enemies(world, room_id):
        if target.matches(enemy):
            return enemy
    return None
