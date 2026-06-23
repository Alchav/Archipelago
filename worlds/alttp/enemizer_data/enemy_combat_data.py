from __future__ import annotations

import random
from dataclasses import dataclass
from typing import NamedTuple


DAMAGE_SOURCE_TABLE_ADDRESS = 0x06B8F1
DAMAGE_SOURCE_TABLE_SIZE = 0x80
ENEMY_HP_TABLE_ADDRESS = 0x06B173
ENEMY_HEALTH_TABLE_SIZE = 0xF3
SPRITE_DAMAGE_SUBCLASS_TABLE_SNES_ADDRESS = 0x31C800
SPRITE_DAMAGE_SUBCLASS_TABLE_SIZE = 0x800
REACHABLE_SPRITE_DAMAGE_SUBCLASS_COUNT = 0xD8
RANDOMIZABLE_DAMAGE_CLASS_COUNT = 0x10
MOTHULA_SPRITE_ID = 0x88
ANTI_FAIRY_SPRITE_ID = 0x15
DEADROCK_SPRITE_ID = 0x27
HARDHAT_BEETLE_SPRITE_ID = 0x26
HARDHAT_BEETLE_RED_HP = 32
HARDHAT_BEETLE_BLUE_HP = 6
RED_BARI_SPRITE_ID = 0x23
THIEF_SPRITE_ID = 0xC4
THIEF_DEFAULT_HP = 4
YELLOW_SLIME_SPRITE_ID = 0x8F
FAIRY_TRANSFORM_EFFECT = 0xF9
BLOB_TRANSFORM_EFFECT = 0xFA
STUN_32_FRAMES_EFFECT = 0xFB
STUN_128_FRAMES_EFFECT = 0xFC
INCINERATE_EFFECT = 0xFD
FREEZE_EFFECT = 0xFE
STUN_255_FRAMES_EFFECT = 0xFF
SWORD_BEAM_DAMAGE_CLASS = 1
FIGHTER_SWORD_DAMAGE_CLASSES = frozenset((1, 2))
MASTER_SWORD_DAMAGE_CLASSES = frozenset((1, 2, 3))
TEMPERED_SWORD_DAMAGE_CLASSES = frozenset((1, 2, 3, 4))
GOLDEN_SWORD_DAMAGE_CLASSES = frozenset((1, 3, 4, 5))
SWORD_UPGRADE_DAMAGE_CLASSES = (2, 3, 4)
NORMAL_ARROW_DAMAGE_CLASS = 6
SILVER_ARROW_DAMAGE_CLASS = 9
ARROW_UPGRADE_DAMAGE_CLASSES = (NORMAL_ARROW_DAMAGE_CLASS, SILVER_ARROW_DAMAGE_CLASS)
VANILLA_RANDOMIZE_DAMAGE_CLASSES = "vanilla"
INTRA_ENEMY_RANDOMIZE_DAMAGE_CLASSES = "intra_enemy"
INTER_ENEMY_RANDOMIZE_DAMAGE_CLASSES = "inter_enemy"
MIXED_RANDOMIZE_DAMAGE_CLASSES = "mixed"
CHAOS_RANDOMIZE_DAMAGE_CLASSES = "chaos"
GUARANTEED_LOGIC_KILL_DAMAGE_CLASS = 9
GUARANTEED_LOGIC_KILL_EFFECT = 0x64
KEY_DROP_KILL_DAMAGE_CLASS_OVERRIDES = {
    "Red Bari": (11, 13),
}
EXCLUDED_ENEMY_TABLE_SPRITE_IDS = frozenset({
    0x09, 0x53, 0x54, 0x70, 0x7A, 0x7B, 0x88, 0x89, 0x8C, 0x8D, 0x92,
    0xA2, 0xA3, 0xA4, 0xBD, 0xBE, 0xBF, 0xCB, 0xCC, 0xCD, 0xCE, 0xD6, 0xD7,
})
DAMAGE_CLASS_RANDOMIZER_HP_255_INCLUDED_SPRITE_IDS = frozenset({
    ANTI_FAIRY_SPRITE_ID,
    DEADROCK_SPRITE_ID,
})
ENEMY_HEALTH_RANGE_BY_KEY = {
    "easy": (1, 4),
    "normal": (2, 15),
    "hard": (2, 25),
    "expert": (4, 50),
}
VANILLA_ENEMY_HEALTH = bytes.fromhex(
    "0c06ff0303030303020c04ff00030c020014040400ff00020308000000000000"
    "08030802020003ff0003030303030303030003000303030003000000000302ff"
    "02060408060806040808080404020202ff08ff30100808ff020000ffffffffff"
    "ffffffff0404ffffffff100300020401ff04ff00000000ff000060ff18ffffff"
    "0304ff10080800ff2020202020080804084030ff02ffffffff10040204040808"
    "081040400804080404080c1000000000000000000000000000000000008030ff"
    "ffffff08000000200008052828285a10184000040000ffff0000000000000000"
    "00000000000000000000000000000000000000"
)


class CombatDeliveryOverride(NamedTuple):
    items: tuple[str, ...]
    abilities: tuple[str, ...] = tuple()


DIRECT_KILL_DELIVERY_OVERRIDES = {
    # Bubble / Anti-Fairy does not check normal sword or hammer contact damage.
    # Master Sword and higher can still deliver class 1 damage through sword beams.
    "Anti-Fairy": CombatDeliveryOverride(
        (
            "Blue Boomerang",
            "Red Boomerang",
            "Cane of Somaria",
            "Cane of Byrna",
            "Bow",
            "Silver Bow",
            "Hookshot",
            "Magic Powder",
            "Fire Rod",
            "Ice Rod",
            "Bombos",
            "Ether",
            "Quake",
        ),
        ("bombs", "sword_beams"),
    ),
    # Damage class 1 includes both safe Cane hits and unsafe sword contact shocks.
    "Buzzblob": CombatDeliveryOverride(
        ("Cane of Somaria", "Cane of Byrna", "Golden Sword", "Bow", "Silver Bow", "Fire Rod", "Bombos"),
        ("bombs",),
    ),
    # Most positive table hits only knock both actors back; only stun/contact tools are logical.
    "Floating Stalfos Head": CombatDeliveryOverride(
        ("Blue Boomerang", "Red Boomerang", "Cane of Somaria", "Cane of Byrna"),
    ),
}


def _build_yellow_slime_follow_up_override(
    *,
    boomerangs: bool = False,
    hookshot: bool = False,
    fire_rod: bool = True,
    ice_rod: bool = True,
    ether: bool = True,
) -> CombatDeliveryOverride:
    items: list[str] = []
    if boomerangs:
        items.extend(("Blue Boomerang", "Red Boomerang"))
    items.extend(
        (
            "Cane of Somaria",
            "Cane of Byrna",
            "Fighter Sword",
            "Master Sword",
            "Hammer",
            "Tempered Sword",
            "Golden Sword",
            "Bow",
        )
    )
    if hookshot:
        items.append("Hookshot")
    items.append("Silver Bow")
    if fire_rod:
        items.append("Fire Rod")
    if ice_rod:
        items.append("Ice Rod")
    items.append("Bombos")
    if ether:
        items.append("Ether")
    return CombatDeliveryOverride(tuple(items), ("bombs",))


# Blob-transform damage classes come from the ROM damage tables. These overrides
# only describe the logical follow-up tools needed to finish the spawned yellow slime.
YELLOW_SLIME_FOLLOW_UP_DELIVERY_OVERRIDES = {
    8: _build_yellow_slime_follow_up_override(),
    10: _build_yellow_slime_follow_up_override(),
    13: _build_yellow_slime_follow_up_override(hookshot=True, ice_rod=False, ether=False),
    14: _build_yellow_slime_follow_up_override(),
    17: _build_yellow_slime_follow_up_override(boomerangs=True),
    18: _build_yellow_slime_follow_up_override(),
    19: _build_yellow_slime_follow_up_override(fire_rod=False, ice_rod=False),
    23: _build_yellow_slime_follow_up_override(boomerangs=True),
    34: _build_yellow_slime_follow_up_override(),
    39: _build_yellow_slime_follow_up_override(hookshot=True, ice_rod=False, ether=False),
    65: _build_yellow_slime_follow_up_override(),
    66: _build_yellow_slime_follow_up_override(),
    67: _build_yellow_slime_follow_up_override(ice_rod=False),
    68: _build_yellow_slime_follow_up_override(ice_rod=False),
    69: _build_yellow_slime_follow_up_override(ice_rod=False),
    70: _build_yellow_slime_follow_up_override(),
    71: _build_yellow_slime_follow_up_override(),
    72: _build_yellow_slime_follow_up_override(ice_rod=False),
    73: _build_yellow_slime_follow_up_override(ice_rod=False),
    74: _build_yellow_slime_follow_up_override(),
    75: _build_yellow_slime_follow_up_override(),
    78: _build_yellow_slime_follow_up_override(hookshot=True),
    79: _build_yellow_slime_follow_up_override(hookshot=True),
    88: _build_yellow_slime_follow_up_override(),
    106: _build_yellow_slime_follow_up_override(boomerangs=True, ice_rod=False),
    109: _build_yellow_slime_follow_up_override(hookshot=True),
    110: _build_yellow_slime_follow_up_override(hookshot=True),
    167: _build_yellow_slime_follow_up_override(boomerangs=True),
    201: _build_yellow_slime_follow_up_override(boomerangs=True),
}


class DamageSource(NamedTuple):
    name: str
    damage_class: int
    subclasses: tuple[int, ...]


@dataclass(frozen=True)
class EnemyCombatModel:
    damage_sources: tuple[DamageSource, ...]
    sprite_damage_subclasses: tuple[tuple[int, ...], ...]
    enemy_health_table: bytes


DAMAGE_SOURCES: tuple[DamageSource, ...] = (
    DamageSource('Boomerang', 0x00, (0x00, 0x01, 0x20, 0xFF, 0xFC, 0xFB, 0x00, 0x00)),
    DamageSource('Damage Class 1', 0x01, (0x00, 0x02, 0x40, 0x04, 0x00, 0x00, 0x00, 0x00)),
    DamageSource('Damage Class 2', 0x02, (0x00, 0x04, 0x40, 0x02, 0x03, 0x00, 0x00, 0x00)),
    DamageSource('Damage Class 3', 0x03, (0x00, 0x08, 0x40, 0x04, 0x00, 0x00, 0x00, 0x00)),
    DamageSource('Damage Class 4', 0x04, (0x00, 0x10, 0x40, 0x08, 0x00, 0x00, 0x00, 0x00)),
    DamageSource('Damage Class 5', 0x05, (0x00, 0x10, 0x40, 0x08, 0x00, 0x00, 0x00, 0x00)),
    DamageSource('Arrow', 0x06, (0x00, 0x04, 0x40, 0x10, 0x00, 0x00, 0x00, 0x00)),
    DamageSource('Hookshot', 0x07, (0x00, 0xFF, 0x40, 0xFF, 0xFC, 0xFB, 0x00, 0x00)),
    DamageSource('Bomb', 0x08, (0x00, 0x04, 0x40, 0xFF, 0xFC, 0xFB, 0x20, 0x00)),
    DamageSource('Silver Arrows', 0x09, (0x00, 0x64, 0x18, 0x64, 0x00, 0x00, 0x00, 0x00)),
    DamageSource('Magic Powder', 0x0A, (0x00, 0xF9, 0xFA, 0xFF, 0x64, 0x00, 0x00, 0x00)),
    DamageSource('Fire Rod', 0x0B, (0x00, 0x08, 0x40, 0xFD, 0x04, 0x10, 0x00, 0x00)),
    DamageSource('Ice Rod', 0x0C, (0x00, 0x08, 0x40, 0xFE, 0x04, 0x00, 0x00, 0x00)),
    DamageSource('Bombos', 0x0D, (0x00, 0x10, 0x40, 0xFD, 0x00, 0x00, 0x00, 0x00)),
    DamageSource('Ether', 0x0E, (0x00, 0xFE, 0x40, 0x10, 0x00, 0x00, 0x00, 0x00)),
    DamageSource('Quake', 0x0F, (0x00, 0x20, 0x40, 0xFF, 0x00, 0x00, 0x00, 0xFA)),
)


# Sprite damage subclasses are indexed by sprite id, then damage class.
# Each value selects one entry from the matching row in DAMAGE_SOURCES.
# This table is vanilla JP 1.0 through sprite 0xD7, with Mothula (0x88)
# damage classes 4 and 5 changed from subclass 0 to subclass 1 so the
# Gold Sword uses the same 16-damage behavior as the GBA release.
SPRITE_DAMAGE_SUBCLASSES: tuple[tuple[int, ...], ...] = (
    (1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 3, 1, 3, 1, 1),  # 0x00
    (1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 3, 1, 3, 1, 1),  # 0x01
    (1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x02
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x03
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x04
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x05
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x06
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x07
    (3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 3, 3, 3, 1, 7),  # 0x08
    (0, 1, 3, 3, 3, 3, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0),  # 0x09
    (3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 3, 3, 3, 1, 7),  # 0x0A
    (1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 1, 1, 0, 0, 0),  # 0x0B
    (1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 1, 1, 1, 3, 1),  # 0x0C
    (3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 1, 3),  # 0x0D
    (3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 3, 3, 3, 2, 7),  # 0x0E
    (1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 3, 1, 3, 3, 2),  # 0x0F
    (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 3, 1),  # 0x10
    (4, 1, 1, 1, 1, 2, 1, 0, 2, 1, 0, 1, 3, 3, 1, 7),  # 0x11
    (3, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 3, 3, 3, 1, 7),  # 0x12
    (0, 1, 1, 1, 1, 1, 1, 3, 2, 3, 2, 0, 0, 3, 2, 7),  # 0x13
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x14
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0),  # 0x15
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x16
    (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 7),  # 0x17
    (0, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 3, 1, 3, 3, 7),  # 0x18
    (1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 0, 1, 1, 3, 2, 3),  # 0x19
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x1A
    (2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 2, 2, 2, 3, 2),  # 0x1B
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x1C
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x1D
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x1E
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x1F
    (3, 1, 1, 1, 1, 1, 1, 1, 0, 1, 2, 3, 3, 3, 1, 7),  # 0x20
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x21
    (3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 3, 3, 3, 2, 7),  # 0x22
    (0, 1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 3, 2, 3, 2, 3),  # 0x23
    (0, 1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 3, 2, 3, 2, 3),  # 0x24
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x25
    (0, 1, 1, 1, 1, 1, 0, 3, 3, 1, 0, 0, 0, 3, 1, 3),  # 0x26
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 7),  # 0x27
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x28
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x29
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0),  # 0x2A
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x2B
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x2C
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x2D
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x2E
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x2F
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x30
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x31
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x32
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x33
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x34
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x35
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x36
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x37
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x38
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x39
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x3A
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x3B
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x3C
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x3D
    (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 2, 2, 7),  # 0x3E
    (0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1),  # 0x3F
    (0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x40
    (3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 3, 1, 3, 1, 7),  # 0x41
    (3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 3, 3, 3, 1, 7),  # 0x42
    (3, 1, 4, 3, 1, 1, 1, 1, 1, 1, 0, 3, 0, 3, 1, 7),  # 0x43
    (3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 3, 0, 3, 1, 7),  # 0x44
    (3, 1, 4, 3, 1, 1, 1, 1, 1, 1, 0, 3, 0, 3, 1, 7),  # 0x45
    (3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 3, 3, 3, 1, 7),  # 0x46
    (3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 3, 1, 3, 2, 7),  # 0x47
    (3, 1, 4, 3, 1, 1, 1, 1, 1, 1, 0, 3, 0, 3, 1, 7),  # 0x48
    (3, 1, 4, 3, 1, 1, 1, 1, 1, 1, 0, 3, 0, 3, 2, 7),  # 0x49
    (3, 1, 4, 3, 1, 1, 1, 1, 1, 1, 0, 3, 3, 3, 1, 7),  # 0x4A
    (3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 3, 3, 3, 1, 7),  # 0x4B
    (1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 0, 1, 1, 3, 3, 3),  # 0x4C
    (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 3, 2, 3, 2, 3),  # 0x4D
    (3, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 3, 3, 3, 1, 7),  # 0x4E
    (3, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 3, 3, 3, 1, 7),  # 0x4F
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x50
    (3, 1, 1, 1, 1, 1, 2, 1, 1, 1, 0, 1, 3, 3, 3, 3),  # 0x51
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x52
    (1, 3, 3, 3, 3, 3, 3, 0, 1, 1, 0, 1, 1, 0, 0, 0),  # 0x53
    (0, 1, 3, 3, 3, 3, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0),  # 0x54
    (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 3, 1, 3, 2, 1),  # 0x55
    (3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 3, 1, 3, 2, 1),  # 0x56
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x57
    (3, 1, 1, 1, 1, 1, 1, 3, 1, 1, 2, 1, 3, 3, 1, 7),  # 0x58
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x59
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x5A
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 3),  # 0x5B
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 3),  # 0x5C
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x5D
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x5E
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x5F
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x60
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x61
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x62
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x63
    (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 3, 3, 3),  # 0x64
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x65
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x66
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x67
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x68
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x69
    (5, 1, 3, 1, 1, 1, 1, 1, 1, 1, 0, 3, 0, 3, 1, 7),  # 0x6A
    (3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1),  # 0x6B
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x6C
    (3, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 3, 3, 3, 1, 7),  # 0x6D
    (3, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 3, 3, 3, 1, 7),  # 0x6E
    (1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 3, 3, 3, 1, 3),  # 0x6F
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x70
    (3, 1, 1, 1, 1, 1, 1, 3, 1, 1, 0, 3, 3, 3, 1, 3),  # 0x71
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x72
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x73
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x74
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x75
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x76
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x77
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x78
    (1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 3, 1),  # 0x79
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x7A
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x7B
    (0, 1, 1, 1, 1, 1, 1, 0, 2, 1, 0, 3, 3, 3, 3, 3),  # 0x7C
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x7D
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x7E
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x7F
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x80
    (0, 1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 3, 3, 2, 3, 2),  # 0x81
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x82
    (0, 1, 1, 2, 2, 1, 2, 0, 1, 2, 0, 0, 0, 0, 0, 0),  # 0x83
    (0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0),  # 0x84
    (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 2, 3, 2, 3),  # 0x85
    (0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 3, 3, 1, 7),  # 0x86
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x87
    (0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0),  # 0x88
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x89
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x8A
    (3, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 3, 3, 3, 2, 3),  # 0x8B
    (0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0),  # 0x8C
    (0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0),  # 0x8D
    (1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 0, 1, 3, 2, 2, 3),  # 0x8E
    (3, 1, 1, 1, 1, 1, 1, 2, 2, 1, 0, 3, 3, 3, 1, 2),  # 0x8F
    (1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 3, 3, 2),  # 0x90
    (1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x91
    (0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0),  # 0x92
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x93
    (1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 3, 1, 3, 2, 3),  # 0x94
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x95
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x96
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x97
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x98
    (1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 0, 1, 0, 3, 1, 2),  # 0x99
    (1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 2, 3, 2, 1, 1),  # 0x9A
    (0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 2, 3, 2),  # 0x9B
    (0, 1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 3, 2, 3, 2, 2),  # 0x9C
    (0, 1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 3, 2, 3, 2, 2),  # 0x9D
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x9E
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0x9F
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0xA0
    (0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0),  # 0xA1
    (0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0),  # 0xA2
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 2, 0, 0),  # 0xA3
    (0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 3, 0, 1, 3, 1),  # 0xA4
    (3, 1, 1, 1, 1, 1, 1, 1, 2, 1, 0, 3, 3, 3, 1, 3),  # 0xA5
    (3, 1, 1, 1, 1, 1, 1, 1, 2, 1, 0, 3, 3, 3, 1, 3),  # 0xA6
    (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 3, 2, 7),  # 0xA7
    (0, 1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 3, 3, 3, 1, 1),  # 0xA8
    (0, 1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 3, 3, 3, 1, 1),  # 0xA9
    (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 3, 1, 3, 1, 3),  # 0xAA
    (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0),  # 0xAB
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0xAC
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0xAD
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0xAE
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0xAF
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0xB0
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0xB1
    (1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 1, 1, 1, 3, 1),  # 0xB2
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0xB3
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0xB4
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0xB5
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0xB6
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0xB7
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0xB8
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0xB9
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0xBA
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0xBB
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0xBC
    (0, 0, 1, 1, 1, 1, 3, 0, 1, 1, 0, 0, 0, 0, 0, 0),  # 0xBD
    (0, 0, 1, 1, 1, 1, 3, 0, 1, 1, 0, 0, 0, 0, 0, 0),  # 0xBE
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0xBF
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0xC0
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0xC1
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0xC2
    (0, 1, 1, 1, 1, 1, 3, 0, 1, 1, 0, 0, 0, 0, 0, 0),  # 0xC3
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0xC4
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 3, 1),  # 0xC5
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 3, 1),  # 0xC6
    (0, 1, 1, 1, 1, 1, 1, 0, 1, 2, 0, 3, 1, 3, 1, 3),  # 0xC7
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0xC8
    (5, 1, 1, 1, 1, 1, 3, 0, 2, 1, 0, 3, 3, 1, 3, 1),  # 0xC9
    (5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0xCA
    (0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0xCB
    (0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0),  # 0xCC
    (0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0),  # 0xCD
    (0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0xCE
    (1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 1, 1, 1, 2, 1),  # 0xCF
    (0, 0, 0, 1, 1, 1, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0),  # 0xD0
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 2, 2, 2),  # 0xD1
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 7),  # 0xD2
    (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 7),  # 0xD3
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0xD4
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0xD5
    (0, 0, 0, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),  # 0xD6
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0),  # 0xD7
)


VANILLA_COMBAT_MODEL = EnemyCombatModel(
    damage_sources=DAMAGE_SOURCES,
    sprite_damage_subclasses=SPRITE_DAMAGE_SUBCLASSES,
    enemy_health_table=VANILLA_ENEMY_HEALTH,
)


def build_randomized_damage_class_combat_model(
    rng: random.Random,
    mode: str,
    combat_model: EnemyCombatModel = VANILLA_COMBAT_MODEL,
    *,
    max_attacks_in_logic: int = 16,
    enemy_health_key: str = "default",
) -> EnemyCombatModel:
    if mode == VANILLA_RANDOMIZE_DAMAGE_CLASSES:
        return combat_model

    resolved_effects = _resolve_sprite_damage_effects(combat_model)
    randomized_effects = [list(row) for row in resolved_effects]
    eligible_sprite_ids = _get_damage_class_randomizable_sprite_ids(combat_model)
    locked_sprite_ids = _get_locked_damage_class_sprite_ids(resolved_effects, eligible_sprite_ids)

    if mode in {INTER_ENEMY_RANDOMIZE_DAMAGE_CLASSES, MIXED_RANDOMIZE_DAMAGE_CLASSES}:
        shuffled_profiles = [tuple(randomized_effects[sprite_id]) for sprite_id in eligible_sprite_ids]
        rng.shuffle(shuffled_profiles)
        for sprite_id, profile in zip(eligible_sprite_ids, shuffled_profiles):
            randomized_effects[sprite_id] = list(profile)
            _enforce_upgrade_damage_safety(randomized_effects[sprite_id], rng)

    if mode in {INTRA_ENEMY_RANDOMIZE_DAMAGE_CLASSES, MIXED_RANDOMIZE_DAMAGE_CLASSES}:
        effect_palettes = _build_effect_palettes(resolved_effects, locked_sprite_ids)
        for sprite_id in eligible_sprite_ids:
            randomized_effects[sprite_id] = _shuffle_sprite_damage_effects(
                randomized_effects[sprite_id],
                effect_palettes,
                rng,
            )

    elif mode == CHAOS_RANDOMIZE_DAMAGE_CLASSES:
        effect_palettes = _build_effect_palettes(resolved_effects, locked_sprite_ids)
        _fill_effect_palettes(effect_palettes, resolved_effects, rng)
        for sprite_id in eligible_sprite_ids:
            randomized_effects[sprite_id] = _build_chaos_sprite_damage_effects(effect_palettes, rng)

    elif mode == INTER_ENEMY_RANDOMIZE_DAMAGE_CLASSES:
        effect_palettes = _build_effect_palettes(resolved_effects, locked_sprite_ids)
        for sprite_id in eligible_sprite_ids:
            randomized_effects[sprite_id] = _fit_sprite_damage_effects(
                randomized_effects[sprite_id],
                effect_palettes,
                rng,
            )

    else:
        raise ValueError(f"Unknown damage class randomization mode: {mode}")

    _ensure_damage_class_logic_guarantees(
        randomized_effects,
        eligible_sprite_ids,
        combat_model,
        max_attacks_in_logic=max_attacks_in_logic,
        enemy_health_key=enemy_health_key,
    )

    return _encode_sprite_damage_effects(combat_model, tuple(tuple(row) for row in randomized_effects))


def _resolve_sprite_damage_effects(combat_model: EnemyCombatModel) -> tuple[tuple[int, ...], ...]:
    return tuple(
        tuple(
            combat_model.damage_sources[damage_class].subclasses[subclass]
            for damage_class, subclass in enumerate(row)
        )
        for row in combat_model.sprite_damage_subclasses
    )


def _get_damage_class_randomizable_sprite_ids(combat_model: EnemyCombatModel) -> tuple[int, ...]:
    max_sprite_id = min(
        len(combat_model.sprite_damage_subclasses),
        REACHABLE_SPRITE_DAMAGE_SUBCLASS_COUNT,
        len(combat_model.enemy_health_table),
    )
    return tuple(
        sprite_id
        for sprite_id in range(max_sprite_id)
        if sprite_id not in EXCLUDED_ENEMY_TABLE_SPRITE_IDS
        and (
            combat_model.enemy_health_table[sprite_id] != 0xFF
            or sprite_id in DAMAGE_CLASS_RANDOMIZER_HP_255_INCLUDED_SPRITE_IDS
        )
    )


def _get_locked_damage_class_sprite_ids(
    resolved_effects: tuple[tuple[int, ...], ...],
    eligible_sprite_ids: tuple[int, ...],
) -> tuple[int, ...]:
    eligible_sprite_ids_set = set(eligible_sprite_ids)
    return tuple(
        sprite_id
        for sprite_id in range(len(resolved_effects))
        if sprite_id not in eligible_sprite_ids_set
    )


def _build_effect_palettes(
    resolved_effects: tuple[tuple[int, ...], ...],
    sprite_ids: tuple[int, ...] | None = None,
) -> list[set[int]]:
    rows = resolved_effects if sprite_ids is None else tuple(resolved_effects[sprite_id] for sprite_id in sprite_ids)
    return [
        {row[damage_class] for row in rows}
        for damage_class in range(RANDOMIZABLE_DAMAGE_CLASS_COUNT)
    ]


def _ensure_damage_class_logic_guarantees(
    randomized_effects: list[list[int]],
    eligible_sprite_ids: tuple[int, ...],
    combat_model: EnemyCombatModel,
    *,
    max_attacks_in_logic: int,
    enemy_health_key: str,
) -> None:
    max_attacks = max(1, max_attacks_in_logic)
    effect_palettes = _build_effect_palettes(tuple(tuple(row) for row in randomized_effects))

    for sprite_id in eligible_sprite_ids:
        hp = get_enemy_health_for_logic(sprite_id, enemy_health_key, combat_model=combat_model)
        if hp is None:
            continue
        row = randomized_effects[sprite_id]
        if _has_direct_kill_within_attack_limit(row, hp, max_attacks):
            continue

        _set_guaranteed_logic_kill_effect_for_row(row, effect_palettes)

    if RED_BARI_SPRITE_ID in eligible_sprite_ids:
        red_bari_hp = get_enemy_health_for_logic(RED_BARI_SPRITE_ID, enemy_health_key, combat_model=combat_model)
        if red_bari_hp is not None and not _has_direct_kill_within_attack_limit(
            [randomized_effects[RED_BARI_SPRITE_ID][damage_class] for damage_class in (11, 13)],
            red_bari_hp,
            max_attacks,
        ):
            _set_guaranteed_logic_kill_effect(
                randomized_effects[RED_BARI_SPRITE_ID],
                effect_palettes,
                11,
                INCINERATE_EFFECT,
            )


def _has_direct_kill_within_attack_limit(row: list[int], hp: int, max_attacks: int) -> bool:
    return any(_effect_kills_within_attack_limit(effect, hp, max_attacks) for effect in row)


def _effect_kills_within_attack_limit(effect: int, hp: int, max_attacks: int) -> bool:
    if effect == INCINERATE_EFFECT:
        return True
    if not 0 < effect < FAIRY_TRANSFORM_EFFECT:
        return False
    return (hp + effect - 1) // effect <= max_attacks


def _set_guaranteed_logic_kill_effect(
    row: list[int],
    effect_palettes: list[set[int]],
    damage_class: int,
    effect: int,
) -> None:
    if not _effect_fits_palette(effect, effect_palettes[damage_class]):
        raise ValueError(f"Damage class {damage_class} has no subclass slot for guaranteed logic effect 0x{effect:02X}")
    row[damage_class] = effect
    effect_palettes[damage_class].add(effect)


def _set_guaranteed_logic_kill_effect_for_row(row: list[int], effect_palettes: list[set[int]]) -> None:
    arrow_safe_effect = _get_arrow_safe_silver_arrow_guarantee_effect(row)
    if (
        arrow_safe_effect is not None
        and _effect_fits_palette(arrow_safe_effect, effect_palettes[GUARANTEED_LOGIC_KILL_DAMAGE_CLASS])
    ):
        _set_guaranteed_logic_kill_effect(
            row,
            effect_palettes,
            GUARANTEED_LOGIC_KILL_DAMAGE_CLASS,
            arrow_safe_effect,
        )
        return

    _set_guaranteed_logic_kill_effect(row, effect_palettes, 11, INCINERATE_EFFECT)


def _get_arrow_safe_silver_arrow_guarantee_effect(row: list[int]) -> int | None:
    normal_arrow_effect = row[NORMAL_ARROW_DAMAGE_CLASS]
    if normal_arrow_effect == 0:
        return GUARANTEED_LOGIC_KILL_EFFECT
    if _is_special_damage_effect(normal_arrow_effect):
        return None
    if is_killing_damage_effect(normal_arrow_effect):
        return max(normal_arrow_effect, GUARANTEED_LOGIC_KILL_EFFECT)
    return None


def _fill_effect_palettes(
    effect_palettes: list[set[int]],
    resolved_effects: tuple[tuple[int, ...], ...],
    rng: random.Random,
) -> None:
    all_effects = sorted({effect for row in resolved_effects for effect in row})
    for palette in effect_palettes:
        while len(palette) < 8:
            palette.add(rng.choice(all_effects))


def _shuffle_sprite_damage_effects(
    row: list[int],
    effect_palettes: list[set[int]],
    rng: random.Random,
) -> list[int]:
    for _ in range(100):
        candidate = list(row)
        rng.shuffle(candidate)
        _enforce_upgrade_damage_safety(candidate, rng)
        if _row_fits_effect_palettes(candidate, effect_palettes):
            _add_row_to_effect_palettes(candidate, effect_palettes)
            return candidate

    fallback = list(row)
    _enforce_upgrade_damage_safety(fallback, rng)
    if _row_fits_effect_palettes(fallback, effect_palettes):
        _add_row_to_effect_palettes(fallback, effect_palettes)
        return fallback

    return _fit_sprite_damage_effects(row, effect_palettes, rng)


def _fit_sprite_damage_effects(
    row: list[int],
    effect_palettes: list[set[int]],
    rng: random.Random,
) -> list[int]:
    for _ in range(100):
        candidate = [
            effect if _effect_fits_palette(effect, effect_palettes[damage_class])
            else rng.choice(tuple(sorted(effect_palettes[damage_class])))
            for damage_class, effect in enumerate(row)
        ]
        _enforce_upgrade_damage_safety(candidate, rng)
        if _row_fits_effect_palettes(candidate, effect_palettes):
            _add_row_to_effect_palettes(candidate, effect_palettes)
            return candidate

    fallback = [
        effect if _effect_fits_palette(effect, effect_palettes[damage_class])
        else rng.choice(tuple(sorted(effect_palettes[damage_class])))
        for damage_class, effect in enumerate(row)
    ]
    for damage_class in SWORD_UPGRADE_DAMAGE_CLASSES:
        fallback[damage_class] = 0
    if not _arrow_upgrade_damage_is_safe(fallback):
        fallback[NORMAL_ARROW_DAMAGE_CLASS] = 0
    if not _row_fits_effect_palettes(fallback, effect_palettes):
        fallback = [
            effect if _effect_fits_palette(effect, effect_palettes[damage_class])
            else next(iter(effect_palettes[damage_class]))
            for damage_class, effect in enumerate(fallback)
        ]
    _add_row_to_effect_palettes(fallback, effect_palettes)
    return fallback


def _build_chaos_sprite_damage_effects(effect_palettes: list[set[int]], rng: random.Random) -> list[int]:
    ordered_palettes = [tuple(sorted(palette)) for palette in effect_palettes]
    for _ in range(100):
        candidate = [
            rng.choice(ordered_palettes[damage_class])
            for damage_class in range(RANDOMIZABLE_DAMAGE_CLASS_COUNT)
        ]
        _enforce_upgrade_damage_safety(candidate, rng)
        if _row_fits_effect_palettes(candidate, effect_palettes):
            return candidate

    candidate = [
        rng.choice(ordered_palettes[damage_class])
        for damage_class in range(RANDOMIZABLE_DAMAGE_CLASS_COUNT)
    ]
    for damage_class in SWORD_UPGRADE_DAMAGE_CLASSES:
        candidate[damage_class] = 0
    if not _arrow_upgrade_damage_is_safe(candidate):
        candidate[NORMAL_ARROW_DAMAGE_CLASS] = 0
    return candidate


def _row_fits_effect_palettes(row: list[int], effect_palettes: list[set[int]]) -> bool:
    return all(
        _effect_fits_palette(effect, effect_palettes[damage_class])
        for damage_class, effect in enumerate(row)
    )


def _add_row_to_effect_palettes(row: list[int], effect_palettes: list[set[int]]) -> None:
    for damage_class, effect in enumerate(row):
        if not _effect_fits_palette(effect, effect_palettes[damage_class]):
            raise ValueError(f"Damage class {damage_class} has no subclass slot for effect 0x{effect:02X}")
        effect_palettes[damage_class].add(effect)


def _effect_fits_palette(effect: int, palette: set[int]) -> bool:
    return effect in palette or len(palette) < 8


def _enforce_upgrade_damage_safety(row: list[int], rng: random.Random) -> None:
    _enforce_sword_upgrade_damage_order(row, rng)
    _enforce_arrow_upgrade_damage_order(row)


def _enforce_sword_upgrade_damage_order(row: list[int], rng: random.Random) -> None:
    sword_effects = [row[damage_class] for damage_class in SWORD_UPGRADE_DAMAGE_CLASSES]
    first_nonzero = next((index for index, effect in enumerate(sword_effects) if effect != 0), None)
    if first_nonzero is None:
        return

    suffix = sword_effects[first_nonzero:]
    special_effects = [effect for effect in suffix if _is_special_damage_effect(effect)]
    normal_effects = [
        effect for effect in suffix
        if is_killing_damage_effect(effect) and not _is_special_damage_effect(effect)
    ]

    if special_effects and (not normal_effects or rng.choice((False, True))):
        normalized_suffix = [rng.choice(special_effects)] * len(suffix)
    elif normal_effects:
        normalized_suffix = sorted(rng.choice(normal_effects) for _ in suffix)
    else:
        normalized_suffix = [0] * len(suffix)

    for index, effect in enumerate(normalized_suffix, start=first_nonzero):
        row[SWORD_UPGRADE_DAMAGE_CLASSES[index]] = effect


def _enforce_arrow_upgrade_damage_order(row: list[int]) -> None:
    normal_arrow_effect = row[NORMAL_ARROW_DAMAGE_CLASS]
    if normal_arrow_effect == 0 or _arrow_upgrade_damage_is_safe(row):
        return
    row[SILVER_ARROW_DAMAGE_CLASS] = normal_arrow_effect


def _arrow_upgrade_damage_is_safe(row: list[int]) -> bool:
    normal_arrow_effect = row[NORMAL_ARROW_DAMAGE_CLASS]
    silver_arrow_effect = row[SILVER_ARROW_DAMAGE_CLASS]
    if normal_arrow_effect == 0:
        return True
    if _is_special_damage_effect(normal_arrow_effect):
        return silver_arrow_effect == normal_arrow_effect
    if is_killing_damage_effect(normal_arrow_effect):
        return (
            is_killing_damage_effect(silver_arrow_effect)
            and not _is_special_damage_effect(silver_arrow_effect)
            and silver_arrow_effect >= normal_arrow_effect
        )
    return silver_arrow_effect == normal_arrow_effect


def _is_special_damage_effect(effect: int) -> bool:
    return effect >= FAIRY_TRANSFORM_EFFECT


def _encode_sprite_damage_effects(
    combat_model: EnemyCombatModel,
    resolved_effects: tuple[tuple[int, ...], ...],
) -> EnemyCombatModel:
    effect_palettes = _build_ordered_effect_palettes(combat_model, resolved_effects)
    damage_sources = tuple(
        source._replace(subclasses=effect_palettes[damage_class])
        for damage_class, source in enumerate(combat_model.damage_sources)
    )
    subclass_indexes = []
    for palette in effect_palettes:
        indexes: dict[int, int] = {}
        for index, effect in enumerate(palette):
            indexes.setdefault(effect, index)
        subclass_indexes.append(indexes)
    sprite_damage_subclasses = tuple(
        tuple(
            subclass_indexes[damage_class][effect]
            for damage_class, effect in enumerate(row)
        )
        for row in resolved_effects
    )
    return EnemyCombatModel(
        damage_sources=damage_sources,
        sprite_damage_subclasses=sprite_damage_subclasses,
        enemy_health_table=combat_model.enemy_health_table,
    )


def _build_ordered_effect_palettes(
    combat_model: EnemyCombatModel,
    resolved_effects: tuple[tuple[int, ...], ...],
) -> tuple[tuple[int, ...], ...]:
    palettes: list[tuple[int, ...]] = []
    for damage_class, source in enumerate(combat_model.damage_sources):
        effects = {row[damage_class] for row in resolved_effects}
        ordered_palette = []
        for effect in source.subclasses:
            if effect in effects and effect not in ordered_palette:
                ordered_palette.append(effect)
        for effect in sorted(effects):
            if effect not in ordered_palette:
                ordered_palette.append(effect)
        if len(ordered_palette) > 8:
            raise ValueError(f"Damage class {damage_class} has {len(ordered_palette)} effects, but only 8 fit")
        while len(ordered_palette) < 8:
            ordered_palette.append(0)
        palettes.append(tuple(ordered_palette))
    return tuple(palettes)


def build_damage_source_table_bytes(damage_sources: tuple[DamageSource, ...] = DAMAGE_SOURCES) -> bytes:
    if len(damage_sources) != 16:
        raise ValueError(f"Expected 16 damage sources, got {len(damage_sources)}")

    output = bytearray()
    for expected_class, source in enumerate(damage_sources):
        if source.damage_class != expected_class:
            raise ValueError(f"Damage source {source.name} has class {source.damage_class}, expected {expected_class}")
        if len(source.subclasses) != 8:
            raise ValueError(f"Damage source {source.name} has {len(source.subclasses)} subclasses, expected 8")
        output.extend(source.subclasses)

    return bytes(output)


def build_packed_sprite_damage_subclass_table(
    subclass_table: tuple[tuple[int, ...], ...] = SPRITE_DAMAGE_SUBCLASSES,
    table_size: int = SPRITE_DAMAGE_SUBCLASS_TABLE_SIZE,
) -> bytes:
    if len(subclass_table) > table_size // 8:
        raise ValueError(f"Sprite subclass table has {len(subclass_table)} rows, but only {table_size // 8} fit")

    output = bytearray()
    for sprite_id, row in enumerate(subclass_table):
        if len(row) != 16:
            raise ValueError(f"Sprite 0x{sprite_id:02X} has {len(row)} subclasses, expected 16")
        for index in range(0, 16, 2):
            upper = row[index]
            lower = row[index + 1]
            if not 0 <= upper <= 0x0F or not 0 <= lower <= 0x0F:
                raise ValueError(f"Sprite 0x{sprite_id:02X} has subclass outside nibble range")
            output.append((upper << 4) | lower)

    output.extend(b"\x00" * (table_size - len(output)))
    return bytes(output)


def get_damage_effect(
    sprite_id: int,
    damage_class: int,
    combat_model: EnemyCombatModel = VANILLA_COMBAT_MODEL,
) -> int:
    subclass = combat_model.sprite_damage_subclasses[sprite_id][damage_class]
    return combat_model.damage_sources[damage_class].subclasses[subclass]


def get_damage_classes_with_effects(
    sprite_id: int,
    effects: frozenset[int],
    combat_model: EnemyCombatModel = VANILLA_COMBAT_MODEL,
) -> tuple[int, ...]:
    return tuple(
        damage_class
        for damage_class in range(len(combat_model.damage_sources))
        if get_damage_effect(sprite_id, damage_class, combat_model) in effects
    )


def is_killing_damage_effect(effect: int) -> bool:
    return 0 < effect < FAIRY_TRANSFORM_EFFECT or effect == INCINERATE_EFFECT


def get_killing_damage_classes(
    sprite_id: int,
    combat_model: EnemyCombatModel = VANILLA_COMBAT_MODEL,
) -> tuple[int, ...]:
    return tuple(
        damage_class
        for damage_class in range(len(combat_model.damage_sources))
        if is_killing_damage_effect(get_damage_effect(sprite_id, damage_class, combat_model))
    )


def get_blob_transform_damage_classes(
    sprite_id: int,
    combat_model: EnemyCombatModel = VANILLA_COMBAT_MODEL,
) -> tuple[int, ...]:
    return tuple(
        damage_class
        for damage_class in range(len(combat_model.damage_sources))
        if get_damage_effect(sprite_id, damage_class, combat_model) == BLOB_TRANSFORM_EFFECT
    )


def get_yellow_slime_follow_up_delivery_override(sprite_id: int) -> CombatDeliveryOverride | None:
    return YELLOW_SLIME_FOLLOW_UP_DELIVERY_OVERRIDES.get(sprite_id)


def get_enemy_health_for_logic(
    sprite_id: int,
    enemy_health_key: str,
    *,
    hp_override: int | None = None,
    killable_thieves: bool = False,
    combat_model: EnemyCombatModel = VANILLA_COMBAT_MODEL,
) -> int | None:
    hp = combat_model.enemy_health_table[sprite_id]
    if sprite_id == THIEF_SPRITE_ID and killable_thieves:
        hp = THIEF_DEFAULT_HP

    if enemy_health_key != "default" and hp != 0xFF and sprite_id not in EXCLUDED_ENEMY_TABLE_SPRITE_IDS:
        hp = ENEMY_HEALTH_RANGE_BY_KEY[enemy_health_key][1] - 1
    elif hp_override is not None:
        hp = hp_override
    else:
        hardcoded_hp = get_hardcoded_enemy_hp(sprite_id)
        if hardcoded_hp is not None:
            hp = hardcoded_hp

    if hp == 0xFF and sprite_id in DAMAGE_CLASS_RANDOMIZER_HP_255_INCLUDED_SPRITE_IDS:
        return 0xFF
    if hp == 0xFF:
        return None
    return hp


def get_hits_to_kill(
    sprite_id: int,
    damage_class: int,
    enemy_health_key: str,
    *,
    hp_override: int | None = None,
    killable_thieves: bool = False,
    combat_model: EnemyCombatModel = VANILLA_COMBAT_MODEL,
) -> int | None:
    effect = get_damage_effect(sprite_id, damage_class, combat_model)
    if effect == INCINERATE_EFFECT:
        return 1
    if not 0 < effect < FAIRY_TRANSFORM_EFFECT:
        return None

    hp = get_enemy_health_for_logic(
        sprite_id,
        enemy_health_key,
        hp_override=hp_override,
        killable_thieves=killable_thieves,
        combat_model=combat_model,
    )
    if hp is None:
        return None
    return (hp + effect - 1) // effect


def get_hardcoded_enemy_hp(sprite_id: int, x_coord_pixels: int | None = None) -> int | None:
    if sprite_id != HARDHAT_BEETLE_SPRITE_ID:
        return None
    if x_coord_pixels is None:
        return max(HARDHAT_BEETLE_RED_HP, HARDHAT_BEETLE_BLUE_HP)
    if x_coord_pixels & 0x10:
        return HARDHAT_BEETLE_BLUE_HP
    return HARDHAT_BEETLE_RED_HP
