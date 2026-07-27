from __future__ import annotations

from dataclasses import dataclass, field
from functools import lru_cache
import random
from typing import TYPE_CHECKING, Optional

from Utils import pc_to_snes, snes_to_pc
from .enemizer_data.base_patch_data import ENEMIZER_BASE_PATCHES
from .enemizer_data.enemy_combat_data import (
    DAMAGE_SOURCE_TABLE_ADDRESS,
    ENEMY_HEALTH_RANDOMIZER_INCLUDED_SPRITE_IDS,
    ENEMY_HEALTH_RANGE_BY_KEY,
    ENEMY_HP_TABLE_ADDRESS,
    EnemyCombatModel,
    EXCLUDED_ENEMY_TABLE_SPRITE_IDS,
    SPRITE_DAMAGE_SUBCLASS_TABLE_SNES_ADDRESS,
    VANILLA_COMBAT_MODEL,
    VANILLA_RANDOMIZE_DAMAGE_CLASSES,
    build_damage_source_table_bytes,
    build_packed_sprite_damage_subclass_table,
    build_randomized_damage_class_combat_model,
    with_killable_thief_combat_model,
)
from .enemizer_data.symbols import ENEMIZER_SYMBOLS

if TYPE_CHECKING:
    from . import ALTTPWorld
    from .Rom import ProcedureRom, TokenRom

# These patch helpers are intentionally shared by generation and patch application:
# generation records writes through TokenRom, while boss shuffle is finalized as a
# procedure step using ProcedureRom after the player supplies their base ROM.

DUNGEON_HEADER_POINTER_TABLE_BASE = 0x271E2
ROOM_HEADER_BANK_LOCATION = 0xB5E7


@dataclass(frozen=True)
class BossPatchData:
    pointer: tuple[int, int]
    graphics: int
    sprite_array: tuple[int, ...]


@dataclass(frozen=True)
class DungeonBossPatchData:
    room_id: int
    sprite_pointer_address: int
    shell_x: int
    shell_y: int
    clear_layer2: bool = False
    extra_sprites: tuple[int, ...] = ()
    gt_sprite_write_address: Optional[int] = None


@dataclass
class RoomObjectTable:
    header_byte_0: int
    header_byte_1: int
    layer_1_objects: list[bytes] = field(default_factory=list)
    layer_1_doors: list[bytes] = field(default_factory=list)
    layer_2_objects: list[bytes] = field(default_factory=list)
    layer_2_doors: list[bytes] = field(default_factory=list)
    layer_3_objects: list[bytes] = field(default_factory=list)
    layer_3_doors: list[bytes] = field(default_factory=list)

    @classmethod
    def from_bytes(cls, table_bytes: bytes) -> "RoomObjectTable":
        table = cls(table_bytes[0], table_bytes[1])
        layers = (
            (table.layer_1_objects, table.layer_1_doors),
            (table.layer_2_objects, table.layer_2_doors),
            (table.layer_3_objects, table.layer_3_doors),
        )
        index = 2

        for objects, doors in layers:
            is_door = False
            while True:
                if table_bytes[index:index + 2] == bytes((0xF0, 0xFF)):
                    is_door = True
                    index += 2
                    continue
                if table_bytes[index:index + 2] == bytes((0xFF, 0xFF)):
                    index += 2
                    break
                if is_door:
                    doors.append(table_bytes[index:index + 2])
                    index += 2
                else:
                    objects.append(table_bytes[index:index + 3])
                    index += 3

        return table

    def add_shell(self, x: int, y: int, clear_layer_2: bool, shell_id: int) -> None:
        self.header_byte_0 = 0xF0
        if clear_layer_2:
            self.layer_2_objects.clear()
        self.layer_2_objects.append(_build_subtype_3_object(x, y, shell_id))

    def remove_shell(self, shell_id: int) -> None:
        self.layer_2_objects = [obj for obj in self.layer_2_objects if _object_id(obj) != shell_id]

    def to_bytes(self) -> bytes:
        output = bytearray((self.header_byte_0, self.header_byte_1))
        output.extend(self._serialize_layer(self.layer_1_objects, self.layer_1_doors, is_last_layer=False))
        output.extend(self._serialize_layer(self.layer_2_objects, self.layer_2_doors, is_last_layer=False))
        output.extend(self._serialize_layer(self.layer_3_objects, self.layer_3_doors, is_last_layer=True))
        return bytes(output)

    @staticmethod
    def _serialize_layer(objects: list[bytes], doors: list[bytes], is_last_layer: bool) -> bytes:
        output = bytearray()
        for obj in objects:
            output.extend(obj)
        if is_last_layer or doors:
            output.extend((0xF0, 0xFF))
        for door in doors:
            output.extend(door)
        output.extend((0xFF, 0xFF))
        return bytes(output)


BOSS_PATCH_DATA: dict[str, BossPatchData] = {
    "Armos": BossPatchData((0x87, 0xE8), 9, (0x05, 0x04, 0x53, 0x05, 0x07, 0x53, 0x05, 0x0A, 0x53,
                                              0x08, 0x0A, 0x53, 0x08, 0x07, 0x53, 0x08, 0x04, 0x53,
                                              0x08, 0xE7, 0x19)),
    "Arrghus": BossPatchData((0x97, 0xD9), 20, (0x07, 0x07, 0x8C, 0x07, 0x07, 0x8D, 0x07, 0x07, 0x8D,
                                                0x07, 0x07, 0x8D, 0x07, 0x07, 0x8D, 0x07, 0x07, 0x8D,
                                                0x07, 0x07, 0x8D, 0x07, 0x07, 0x8D, 0x07, 0x07, 0x8D,
                                                0x07, 0x07, 0x8D, 0x07, 0x07, 0x8D, 0x07, 0x07, 0x8D,
                                                0x07, 0x07, 0x8D, 0x07, 0x07, 0x8D)),
    "Blind": BossPatchData((0x54, 0xE6), 32, (0x05, 0x09, 0xCE)),
    "Helmasaur": BossPatchData((0x49, 0xE0), 21, (0x06, 0x07, 0x92)),
    "Kholdstare": BossPatchData((0x01, 0xEA), 22, (0x05, 0x07, 0xA3, 0x05, 0x07, 0xA4, 0x05, 0x07, 0xA2)),
    "Lanmola": BossPatchData((0xCB, 0xDC), 11, (0x07, 0x06, 0x54, 0x07, 0x09, 0x54, 0x09, 0x07, 0x54)),
    "Moldorm": BossPatchData((0xC3, 0xD9), 12, (0x09, 0x09, 0x09)),
    "Mothula": BossPatchData((0x31, 0xDC), 26, (0x06, 0x08, 0x88)),
    "Trinexx": BossPatchData((0xBA, 0xE5), 23, (0x05, 0x07, 0xCB, 0x05, 0x07, 0xCC, 0x05, 0x07, 0xCD)),
    "Vitreous": BossPatchData((0x57, 0xE4), 22, (0x05, 0x07, 0xBD)),
}

DUNGEON_BOSS_PATCH_DATA: dict[tuple[str, Optional[str]], DungeonBossPatchData] = {
    ("Eastern Palace", None): DungeonBossPatchData(200, 0x04D7BE, 0x2B, 0x28),
    ("Desert Palace", None): DungeonBossPatchData(51, 0x04D694, 0x0B, 0x28),
    ("Tower of Hera", None): DungeonBossPatchData(7, 0x04D63C, 0x18, 0x16),
    ("Palace of Darkness", None): DungeonBossPatchData(90, 0x04D6E2, 0x2B, 0x28),
    ("Swamp Palace", None): DungeonBossPatchData(6, 0x04D63A, 0x0B, 0x28),
    ("Skull Woods", None): DungeonBossPatchData(41, 0x04D680, 0x2B, 0x28),
    ("Thieves Town", None): DungeonBossPatchData(172, 0x04D786, 0x2B, 0x28, clear_layer2=True),
    ("Ice Palace", None): DungeonBossPatchData(222, 0x04D7EA, 0x2B, 0x08, clear_layer2=True),
    ("Misery Mire", None): DungeonBossPatchData(144, 0x04D74E, 0x0B, 0x28, clear_layer2=True),
    ("Turtle Rock", None): DungeonBossPatchData(164, 0x04D776, 0x0B, 0x28, clear_layer2=True),
    ("Ganons Tower", "bottom"): DungeonBossPatchData(
        28, 0x04D666, 0x2B, 0x28, extra_sprites=(0x07, 0x07, 0xE3, 0x07, 0x08, 0xE3, 0x08, 0x07, 0xE3, 0x08, 0x08, 0xE3),
        gt_sprite_write_address=0x04D87E,
    ),
    ("Ganons Tower", "middle"): DungeonBossPatchData(
        108, 0x04D706, 0x0B, 0x28, extra_sprites=(0x18, 0x17, 0xD1, 0x1C, 0x03, 0xC5), gt_sprite_write_address=0x04D8B6,
    ),
    ("Ganons Tower", "top"): DungeonBossPatchData(77, 0x04D6C8, 0x18, 0x16),
}
ROOM_OBJECT_TABLE_BYTES: dict[int, bytes] = {
    200: bytes.fromhex("e10098923a88aa65e8aa66fffffffff0ff8118ffff"),
    51: bytes.fromhex("e900fffffffff0ff6118ffff"),
    7: bytes.fromhex(
        "811c0a4e0d0aaa0e0b5161c02ca2b0200fb02262fec102c93801ffa382bae610e8aa62ff43b95353e09153e05391e091"
        "91e03c6bc23d9bc354a6c35caac368b1c375b0c38fb1c39baac3a6a0c3ad98c3b46ac2513dc34549c33d51c39c39c2a1"
        "49c3ad51c33a508a38502244446944442258130560155578103a085b650c617fc83905e85b66ec4a8058eb0660ed5678"
        "ec3b50386950385fa83869a84422b44469b45122c6508a3bc8228bc82274bc6988bc69633cc2664f2964506b5c542b5c"
        "586b545c2b54606b4c642b4e6b6b4c982d549c6b54a02d5ca46b5ca82d64ac6b66b32a98ac6a98a82ea0a46aa0a02ea8"
        "9c6aa8982eb26b6aa8642ca8606aa05c2ca0586a98542c98506a6874c268712768776a74776b688528fc317274ae0471"
        "a0e00a13a00abfa1bef7a3c311c0d13100fffffffff0ffffff"
    ),
    90: bytes.fromhex("e900a8a8deb0a0deb8a8dec0a0dec8a8ded0a0defffffffff0ff8118ffff"),
    6: bytes.fromhex(
        "e1001ba3c858a3c81bd8c858d8c8179f3f549f3f17a37914e17917eb4054eb406ba37a68e17a2190f85190f80ca57f6c"
        "a580fffffffff0ff6118ffff"
    ),
    41: bytes.fromhex(
        "e500979cdeb79cded69cde97e4deb7e4ded6e4de94a7de94c7dee4a7dee4c7deffff0303ca4303ca8303cac303ca0343"
        "ca4343ca8343cac343ca0383ca4383ca8383cac383ca03c3ca43c3ca83c3cac3c3caffff9fa7c6d4a7c6fef9f4ff1e74"
        "fe5c74ff9c74f0ffffff"
    ),
    172: bytes.fromhex("e90088a40d88d00ee0900fe0e41089ab61e9ab628891a088e5a1e491a2e4f5a3ffffb1a8fffffff0ff8118ffff"),
    222: bytes.fromhex("e400ffffad21f9fffff0ffffff"),
    144: bytes.fromhex("e10028ec5648ec561ba2ffffff169cfefffff0ff6118ffff"),
    164: bytes.fromhex(
        "e100fc0800138001fdc802029361fc0e8113e802fdce837293621393c45193c451c9c410c9c40e8dde0d9cde0ca5de5e"
        "8cde6594de6c9cdeffff2e98fffffff0ff6118ffff"
    ),
    28: bytes.fromhex(
        "e1002d32a4a91edca8913a88ad76ecad77a8503dd0503d30a93d30c13dfc6938979fd1cd9fd197dcd1cddcd1bd32f9b1"
        "22f9c922f9fffffffff0ff803682186028ffff"
    ),
    108: bytes.fromhex(
        "e200179fe84d9fe817dce84ddce818e1fe88ad7699bc339bbb349bcf34d8b834d8cc34afaafec7aafeafd2fec7d2fe28"
        "113a28913afce1382b33fa5333fa2b53fa5353fafffffffff0ff823860188300ffff"
    ),
    77: bytes.fromhex(
        "821c09340d083a6109c00e08c261d1100fe83a625e1c03174963df4b64dcca64ff7dcb9ddf043b5be07b5be0b85be06a"
        "b1e07854c25b2ac2982ac2214bc3217bc321a1c3387bc2488ac23aaac25b9cc2c94bc3c97bc3b879c2a888c29b9bc29b"
        "d0c2d0a3c2788cc2154522591f69a51f69c9452268e45e15b92235b96937d92288d92298d96966cb2a69c90479cbf98d"
        "baf9375729875729785a6a845a6b786528355b6b347a2d447e6b448a2d548e6b559b2a788e6a788927848e6b859b2aa8"
        "8e6aa88a2eb87e6ab87a2ec95b6a66af2965b16b99b16a384b03a84b0348133a0c4a7fec4a80fee1390911a0d511a209"
        "d5a1ffff5b19db9819db114bdb118adb3948dba948dbd94bdbd98bdb6ac8db9bcadbd9cadbfffff0ff001c2200ffff"
    ),
}

TRINEXX_SHELL_OBJECT_ID = 0xFF2
KHOLDSTARE_SHELL_OBJECT_ID = 0xF95
TRINEXX_VANILLA_ROOM_ID = 164
KHOLDSTARE_VANILLA_ROOM_ID = 222
ENEMY_DAMAGE_TABLE_ADDRESS = 0x6B266
VANILLA_ENEMY_DAMAGE_TABLE_HIGH_NIBBLES = (
    0x80, 0x80, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x10, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x40, 0x00, 0x00, 0x00,
    0x00, 0x80, 0x00, 0x00, 0x00, 0x40, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x40,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x10, 0x10, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x80,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x40, 0x00, 0x00,
    0x00, 0x00, 0x10, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x10, 0x00, 0x00,
    0x00, 0x10, 0x10, 0x00, 0x00, 0x00, 0x00, 0x10,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x10, 0x10, 0x10, 0x00, 0x00, 0x00,
    0x80, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x10, 0x10, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x10, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x10, 0x10, 0x10, 0x10, 0x00,
    0x00, 0x10, 0x00, 0x00, 0x00, 0x00, 0x10, 0x10,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00,
)
HIDDEN_ENEMY_CHANCE_POOL_ADDRESS = 0xD7BBB
DAMAGE_GROUP_TABLE_ADDRESS = 0x3742D
RETRO_ARROW_REPLACEMENT_CHECK_ADDRESS = 0x301FC
RETRO_RUPEE_REPLACEMENT_SPRITE_ID = 0xDA
ARROW_REFILL_5_SPRITE_ID = 0xE1
VANILLA_HIDDEN_ENEMY_ITEM_TABLE = (
    0x00, 0xD9, 0x3E, 0x79, 0xD9, 0xDC, 0xD8, 0xDA,
    0xE4, 0xE1, 0xDC, 0xD8, 0xDF, 0xE0, 0x0B, 0x42,
    0xD3, 0x41, 0xD4, 0xD9, 0xE3, 0xD8,
)
VANILLA_HIDDEN_ENEMY_CHANCE_POOL = (
    0x01, 0x01, 0x01, 0x01, 0x0F, 0x01, 0x01, 0x12,
    0x10, 0x01, 0x01, 0x01, 0x11, 0x01, 0x01, 0x03,
)
RANDOMIZED_HIDDEN_ENEMY_CHANCE_POOL = (
    0x01, 0x0F, 0x0F, 0x0F, 0x0F, 0x0F, 0x0F, 0x12,
    0x0F, 0x01, 0x0F, 0x0F, 0x11, 0x0F, 0x0F, 0x03,
)

_ENEMIZER_SYMBOLS: Optional[dict[str, int]] = None

BOSS_GFX_SHEET_INDEXES = {
    "Agahnim1": 0x8D,
    "Agahnim2": 0xB5,
    "Agahnim3": 0xC8,
    "Agahnim4": 0xB6,
    "ArmosKnight1": 0x90,
    "Ganon1": 0x94,
    "Ganon2": 0xA6,
    "Ganon3": 0xB4,
    "Ganon4": 0xB8,
    "Moldorm1": 0xA3,
    "Lanmola1": 0xA4,
    "Arrghus1": 0xAC,
    "Mothula1": 0xAB,
    "Helmasaure1": 0xAD,
    "Helmasaure2": 0xB1,
    "Blind1": 0xAE,
    "Kholdstare1": 0xAF,
    "Vitreous1": 0xB0,
    "Trinexx1": 0xB2,
    "Trinexx2": 0xB3,
}

BOSS_GFX_TABLE = {
    "Agahnim1": (21, 190, 228),
    "Agahnim2": (22, 255, 135),
    "Agahnim3": (23, 220, 101),
    "Agahnim4": (23, 132, 92),
    "ArmosKnight1": (21, 206, 27),
    "Ganon1": (21, 227, 160),
    "Ganon2": (22, 186, 55),
    "Ganon3": (22, 250, 199),
    "Ganon4": (23, 142, 33),
    "Moldorm1": (22, 175, 152),
    "Lanmola1": (22, 180, 23),
    "Arrghus1": (22, 214, 147),
    "Mothula1": (22, 210, 84),
    "Helmasaure1": (22, 219, 114),
    "Helmasaure2": (22, 239, 177),
    "Blind1": (22, 224, 90),
    "Kholdstare1": (22, 230, 31),
    "Vitreous1": (22, 235, 9),
    "Trinexx1": (22, 243, 89),
    "Trinexx2": (22, 246, 35),
}

TRINEXX_ICE_FLOOR_ROUTINE_ADDRESS = 0x04B37E
TRINEXX_ICE_PROJECTILE_TILE_ADDRESS = 0xE7A5
TILE_TRAP_FLOOR_TILE_ADDRESS = 0xF3BED
SPRITE_DAMAGE_SUBCLASS_TABLE_ADDRESS = snes_to_pc(SPRITE_DAMAGE_SUBCLASS_TABLE_SNES_ADDRESS)
HARDHAT_BEETLE_HP_TABLE_ADDRESS = 0x3111F


def apply_enemizer_base_patch(rom: "TokenRom | ProcedureRom") -> None:
    for address, patch_data in _load_enemizer_base_patches():
        rom.write_bytes(address, patch_data)
    _apply_trinexx_room_fixes(rom)


def apply_enemy_combat_data(
    rom: "TokenRom | ProcedureRom",
    combat_model: EnemyCombatModel = VANILLA_COMBAT_MODEL,
) -> None:
    rom.write_bytes(ENEMY_HP_TABLE_ADDRESS, combat_model.enemy_health_table)
    rom.write_bytes(DAMAGE_SOURCE_TABLE_ADDRESS, build_damage_source_table_bytes(combat_model.damage_sources))
    rom.write_bytes(
        SPRITE_DAMAGE_SUBCLASS_TABLE_ADDRESS,
        build_packed_sprite_damage_subclass_table(combat_model.sprite_damage_subclasses),
    )


def patch_bosses(world: "ALTTPWorld", rom: "TokenRom | ProcedureRom") -> None:
    moved_room_object_base = _get_enemizer_symbol("modified_room_object_table")
    gt_dungeon_name = "Ganons Tower" if world.options.mode != "inverted" else "Inverted Ganons Tower"
    gt_dungeon = world.dungeons[gt_dungeon_name]

    placements = (
        (world.dungeons["Eastern Palace"].boss.enemizer_name, DUNGEON_BOSS_PATCH_DATA[("Eastern Palace", None)]),
        (world.dungeons["Desert Palace"].boss.enemizer_name, DUNGEON_BOSS_PATCH_DATA[("Desert Palace", None)]),
        (world.dungeons["Tower of Hera"].boss.enemizer_name, DUNGEON_BOSS_PATCH_DATA[("Tower of Hera", None)]),
        (world.dungeons["Palace of Darkness"].boss.enemizer_name, DUNGEON_BOSS_PATCH_DATA[("Palace of Darkness", None)]),
        (world.dungeons["Swamp Palace"].boss.enemizer_name, DUNGEON_BOSS_PATCH_DATA[("Swamp Palace", None)]),
        (world.dungeons["Skull Woods"].boss.enemizer_name, DUNGEON_BOSS_PATCH_DATA[("Skull Woods", None)]),
        (world.dungeons["Thieves Town"].boss.enemizer_name, DUNGEON_BOSS_PATCH_DATA[("Thieves Town", None)]),
        (world.dungeons["Ice Palace"].boss.enemizer_name, DUNGEON_BOSS_PATCH_DATA[("Ice Palace", None)]),
        (world.dungeons["Misery Mire"].boss.enemizer_name, DUNGEON_BOSS_PATCH_DATA[("Misery Mire", None)]),
        (world.dungeons["Turtle Rock"].boss.enemizer_name, DUNGEON_BOSS_PATCH_DATA[("Turtle Rock", None)]),
        (gt_dungeon.bosses["bottom"].enemizer_name, DUNGEON_BOSS_PATCH_DATA[("Ganons Tower", "bottom")]),
        (gt_dungeon.bosses["middle"].enemizer_name, DUNGEON_BOSS_PATCH_DATA[("Ganons Tower", "middle")]),
        (gt_dungeon.bosses["top"].enemizer_name, DUNGEON_BOSS_PATCH_DATA[("Ganons Tower", "top")]),
    )

    modified_room_tables: dict[int, RoomObjectTable] = {}

    for boss_name, dungeon_data in placements:
        boss_data = BOSS_PATCH_DATA[boss_name]
        dungeon_header_address = get_dungeon_room_header_address(rom, dungeon_data.room_id)
        rom.write_bytes(dungeon_data.sprite_pointer_address, boss_data.pointer)
        rom.write_byte(dungeon_header_address + 3, boss_data.graphics)

        if boss_name == "Trinexx" and dungeon_data.room_id != TRINEXX_VANILLA_ROOM_ID:
            room_table = _get_room_object_table(modified_room_tables, dungeon_data.room_id)
            room_table.add_shell(
                dungeon_data.shell_x,
                dungeon_data.shell_y - 2,
                dungeon_data.clear_layer2,
                TRINEXX_SHELL_OBJECT_ID,
            )
            rom.write_byte(dungeon_header_address, 0x60)
            rom.write_byte(dungeon_header_address + 4, 0x04)

        if boss_name == "Kholdstare" and dungeon_data.room_id != KHOLDSTARE_VANILLA_ROOM_ID:
            room_table = _get_room_object_table(modified_room_tables, dungeon_data.room_id)
            room_table.add_shell(
                dungeon_data.shell_x,
                dungeon_data.shell_y,
                dungeon_data.clear_layer2,
                KHOLDSTARE_SHELL_OBJECT_ID,
            )
            rom.write_byte(dungeon_header_address, 0xE0)
            rom.write_byte(dungeon_header_address + 4, 0x01)

        if boss_name != "Trinexx" and dungeon_data.room_id == TRINEXX_VANILLA_ROOM_ID:
            _get_room_object_table(modified_room_tables, dungeon_data.room_id).remove_shell(TRINEXX_SHELL_OBJECT_ID)

        if boss_name != "Kholdstare" and dungeon_data.room_id == KHOLDSTARE_VANILLA_ROOM_ID:
            _get_room_object_table(modified_room_tables, dungeon_data.room_id).remove_shell(KHOLDSTARE_SHELL_OBJECT_ID)

        if dungeon_data.gt_sprite_write_address is not None:
            _write_gt_boss_sprite_block(rom, dungeon_data, boss_data)

    write_address = moved_room_object_base
    for room_id in sorted(modified_room_tables):
        table_bytes = modified_room_tables[room_id].to_bytes()
        _write_room_object_pointer(rom, room_id, write_address)
        rom.write_bytes(write_address, table_bytes)
        write_address += len(table_bytes)

    rom.write_byte(0x1B0101, 0x01)
    rom.write_byte(0x04DE81, 0x00)
    if world.dungeons["Thieves Town"].boss.enemizer_name == "Blind":
        rom.write_byte(0x04DE81, 0x06)
        rom.write_byte(0x1B0101, 0x00)


def _get_room_object_table(cache: dict[int, RoomObjectTable], room_id: int) -> RoomObjectTable:
    room_table = cache.get(room_id)
    if room_table is not None:
        return room_table

    room_table = RoomObjectTable.from_bytes(ROOM_OBJECT_TABLE_BYTES[room_id])
    cache[room_id] = room_table
    return room_table


def _write_gt_boss_sprite_block(rom: "TokenRom | ProcedureRom", dungeon_data: DungeonBossPatchData, boss_data: BossPatchData) -> None:
    assert dungeon_data.gt_sprite_write_address is not None
    rom.write_int16(dungeon_data.sprite_pointer_address, dungeon_data.gt_sprite_write_address)

    sprite_block = bytearray((0x00,))
    sprite_block.extend(boss_data.sprite_array)
    if dungeon_data.room_id == 28 and boss_data.pointer == BOSS_PATCH_DATA["Arrghus"].pointer:
        sprite_block.extend(dungeon_data.extra_sprites[:6])
    else:
        sprite_block.extend(dungeon_data.extra_sprites)
    sprite_block.append(0xFF)
    rom.write_bytes(dungeon_data.gt_sprite_write_address, sprite_block)


def _write_room_object_pointer(rom: "TokenRom | ProcedureRom", room_id: int, pc_address: int) -> None:
    snes_address = pc_to_snes(pc_address)
    pointer_address = 0xF8000 + (room_id * 3)
    rom.write_bytes(pointer_address, (
        snes_address & 0xFF,
        (snes_address >> 8) & 0xFF,
        (snes_address >> 16) & 0xFF,
    ))


def _build_subtype_3_object(x: int, y: int, object_id: int) -> bytes:
    return bytes((
        ((x << 2) & 0xFC) | (object_id & 0x03),
        ((y << 2) & 0xFC) | ((object_id >> 2) & 0x03),
        0xF0 | ((object_id >> 4) & 0x0F),
    ))


def _object_id(object_bytes: bytes) -> Optional[int]:
    if len(object_bytes) != 3:
        return None
    if object_bytes[0] >= 0xFC:
        return (object_bytes[2] & 0x3F) + 0x100
    if object_bytes[2] >= 0xF8:
        return 0xF00 | ((object_bytes[2] & 0x0F) << 4) | ((object_bytes[1] & 0x03) << 2) | (object_bytes[0] & 0x03)
    return object_bytes[2]


def _set_enemizer_flag(rom: "TokenRom | ProcedureRom", symbol_name: str, enabled: bool) -> None:
    rom.write_byte(_get_enemizer_symbol(symbol_name), 0x01 if enabled else 0x00)


def _randomize_enemy_health(
    rom: "TokenRom | ProcedureRom",
    random: random.Random,
    enemy_health_key: str,
    combat_model: EnemyCombatModel = VANILLA_COMBAT_MODEL,
) -> None:
    min_hp, max_hp = ENEMY_HEALTH_RANGE_BY_KEY[enemy_health_key]
    for sprite_id in range(0xF3):
        hp_address = ENEMY_HP_TABLE_ADDRESS + sprite_id
        if (
            combat_model.enemy_health_table[sprite_id] == 0xFF
            or sprite_id in EXCLUDED_ENEMY_TABLE_SPRITE_IDS
            or sprite_id not in ENEMY_HEALTH_RANDOMIZER_INCLUDED_SPRITE_IDS
        ):
            continue
        rom.write_byte(hp_address, random.randrange(min_hp, max_hp))
    rom.write_bytes(
        HARDHAT_BEETLE_HP_TABLE_ADDRESS,
        (
            random.randrange(min_hp, max_hp),
            random.randrange(min_hp, max_hp),
        ),
    )


def _randomize_enemy_damage(rom: "TokenRom | ProcedureRom", random: random.Random, allow_zero_damage: bool) -> None:
    for sprite_id in range(0xF3):
        if sprite_id in EXCLUDED_ENEMY_TABLE_SPRITE_IDS:
            continue
        damage_address = ENEMY_DAMAGE_TABLE_ADDRESS + sprite_id
        new_damage = random.randrange(8)
        if not allow_zero_damage and new_damage == 2:
            continue
        rom.write_byte(damage_address, VANILLA_ENEMY_DAMAGE_TABLE_HIGH_NIBBLES[sprite_id] | new_damage)


def _shuffle_damage_groups(
    rom: "TokenRom | ProcedureRom",
    random: random.Random,
    *,
    chaos_mode: bool,
    allow_zero_damage: bool,
) -> None:
    min_damage = 0 if allow_zero_damage else 4
    max_damage = 64 if chaos_mode else 32

    for group_id in range(10):
        green_mail_damage = random.randrange(min_damage, max_damage)
        if chaos_mode:
            blue_mail_damage = random.randrange(min_damage, max_damage)
            red_mail_damage = random.randrange(min_damage, max_damage)
        else:
            blue_mail_damage = green_mail_damage * 3 // 4
            red_mail_damage = green_mail_damage * 3 // 8
        group_address = DAMAGE_GROUP_TABLE_ADDRESS + (group_id * 3)
        rom.write_bytes(group_address, (green_mail_damage, blue_mail_damage, red_mail_damage))


def _update_hidden_enemy_item_table_for_retro_mode(rom: "TokenRom | ProcedureRom") -> None:
    if rom.read_byte(RETRO_ARROW_REPLACEMENT_CHECK_ADDRESS) != RETRO_RUPEE_REPLACEMENT_SPRITE_ID:
        return

    item_table_address = _get_enemizer_symbol("sprite_bush_spawn_item_table")
    for index, default_item in enumerate(VANILLA_HIDDEN_ENEMY_ITEM_TABLE):
        try:
            item = rom.read_byte(item_table_address + index)
        except RuntimeError:
            item = default_item
        if item == ARROW_REFILL_5_SPRITE_ID:
            rom.write_byte(item_table_address + index, RETRO_RUPEE_REPLACEMENT_SPRITE_ID)


def _apply_trinexx_room_fixes(rom: "TokenRom | ProcedureRom") -> None:
    # Match original Enemizer's unconditional Trinexx ice-floor removal so
    # blue-head projectiles do not create solid walls in non-vanilla rooms.
    rom.write_bytes(TRINEXX_ICE_FLOOR_ROUTINE_ADDRESS, (0xEA, 0xEA, 0xEA, 0xEA))


def _apply_randomized_tile_trap_floor_tile(rom: "TokenRom | ProcedureRom") -> None:
    # Original Enemizer's RandomizeTileTrapFloorTile option changes the tile
    # left behind by flying floor tile traps. AP does not currently expose or
    # call this option, so keep the implementation isolated and unused.
    rom.write_bytes(TRINEXX_ICE_PROJECTILE_TILE_ADDRESS, (0x88, 0x01))
    rom.write_byte(TILE_TRAP_FLOOR_TILE_ADDRESS, 0x12)


@lru_cache(maxsize=1)
def _load_enemizer_base_patches() -> tuple[tuple[int, bytes], ...]:
    return tuple(
        (entry.address, entry.patch_data)
        for entry in ENEMIZER_BASE_PATCHES
    )


def _option_key(option: object) -> str:
    return str(getattr(option, "current_key", option))


def _get_enemizer_symbol(symbol_name: str) -> int:
    global _ENEMIZER_SYMBOLS
    if _ENEMIZER_SYMBOLS is None:
        _ENEMIZER_SYMBOLS = _load_enemizer_symbols()
    return _ENEMIZER_SYMBOLS[symbol_name]


def get_dungeon_room_header_address(rom: "TokenRom | ProcedureRom", room_id: int) -> int:
    moved_header_bank = rom.read_byte(_get_enemizer_symbol("moved_room_header_bank_value_address"))
    room_header_bank = moved_header_bank or rom.read_byte(ROOM_HEADER_BANK_LOCATION)
    pointer_address = DUNGEON_HEADER_POINTER_TABLE_BASE + (room_id * 2)
    header_pointer = rom.read_byte(pointer_address) | (rom.read_byte(pointer_address + 1) << 8)
    return snes_to_pc(header_pointer | (room_header_bank << 16))


def _load_enemizer_symbols() -> dict[str, int]:
    return {
        name: snes_to_pc(snes_address)
        for name, snes_address in ENEMIZER_SYMBOLS.items()
    }
