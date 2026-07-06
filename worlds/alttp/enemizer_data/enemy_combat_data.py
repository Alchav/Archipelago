from __future__ import annotations

import random
from dataclasses import dataclass
from typing import NamedTuple

from .enemy_sprite_requirements import ENEMY_SPRITE_REQUIREMENTS


DAMAGE_SOURCE_TABLE_ADDRESS = 0x06B8F1
DAMAGE_SOURCE_TABLE_SIZE = 0x80
ENEMY_HP_TABLE_ADDRESS = 0x06B173
ENEMY_HEALTH_TABLE_SIZE = 0xF3
SPRITE_DAMAGE_SUBCLASS_TABLE_SNES_ADDRESS = 0x31C800
SPRITE_DAMAGE_SUBCLASS_TABLE_SIZE = 0x800
REACHABLE_SPRITE_DAMAGE_SUBCLASS_COUNT = 0xD8
RANDOMIZABLE_DAMAGE_CLASS_COUNT = 0x10
MOLDORM_SPRITE_ID = 0x09
ARMOS_KNIGHTS_SPRITE_ID = 0x53
MOTHULA_SPRITE_ID = 0x88
LANMOLAS_SPRITE_ID = 0x54
ARRGHUS_SPRITE_ID = 0x8C
ARRGHUS_FUZZ_SPRITE_ID = 0x8D
HELMASAUR_KING_SPRITE_ID = 0x92
KHOLDSTARE_SPRITE_ID = 0xA2
KHOLDSTARE_ICE_BLOCK_SPRITE_ID = 0xA3
VITREOUS_SMALL_EYE_SPRITE_ID = 0xBD
VITREOUS_SPRITE_ID = 0xBE
TRINEXX_MAIN_HEAD_SPRITE_ID = 0xCB
TRINEXX_RED_HEAD_SPRITE_ID = 0xCC
TRINEXX_BLUE_HEAD_SPRITE_ID = 0xCD
BLIND_SPRITE_ID = 0xCE
GANON_D6_SPRITE_ID = 0xD6
GANON_D7_SPRITE_ID = 0xD7
ANTI_FAIRY_SPRITE_ID = 0x15
DEADROCK_SPRITE_ID = 0x27
HARDHAT_BEETLE_SPRITE_ID = 0x26
HARDHAT_BEETLE_RED_HP = 32
HARDHAT_BEETLE_BLUE_HP = 6
RED_BARI_SPRITE_ID = 0x23
BUZZBLOB_SPRITE_ID = 0x0D
FLOATING_STALFOS_HEAD_SPRITE_ID = 0x7C
THIEF_SPRITE_ID = 0xC4
THIEF_DEFAULT_HP = 4
YELLOW_SLIME_SPRITE_ID = 0x8F
LIGHTNING_GATE_SPRITE_ID = 0x40
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
LOST_SWORD_UPGRADE_DAMAGE_CLASS = 2
GOLDEN_SWORD_SPIN_DAMAGE_CLASS = 5
SWORD_CLASS_2_REPLACEMENT_DAMAGE_CLASSES = (1, 3, 4, 5)
NORMAL_ARROW_DAMAGE_CLASS = 6
SILVER_ARROW_DAMAGE_CLASS = 9
VANILLA_RANDOMIZE_DAMAGE_CLASSES = "vanilla"
ENEMY_SWAP_RANDOMIZE_DAMAGE_CLASSES = "enemy_swap"
DAMAGE_CLASS_SWAP_RANDOMIZE_DAMAGE_CLASSES = "damage_class_swap"
MIXED_RANDOMIZE_DAMAGE_CLASSES = "mixed"
CHAOS_RANDOMIZE_DAMAGE_CLASSES = "chaos"
NIGHTMARE_RANDOMIZE_DAMAGE_CLASSES = "nightmare"
NON_VANILLA_RANDOMIZE_DAMAGE_CLASS_MODES = (
    ENEMY_SWAP_RANDOMIZE_DAMAGE_CLASSES,
    DAMAGE_CLASS_SWAP_RANDOMIZE_DAMAGE_CLASSES,
    MIXED_RANDOMIZE_DAMAGE_CLASSES,
    CHAOS_RANDOMIZE_DAMAGE_CLASSES,
    NIGHTMARE_RANDOMIZE_DAMAGE_CLASSES,
)
GUARANTEED_LOGIC_KILL_DAMAGE_CLASS = 9
PROGRESSION_LOGIC_KILL_DAMAGE_CLASSES = frozenset((1, 3, 6, 7, 9, 10, 11, 12, 13, 14, 15))
NON_SILVER_PROGRESSION_LOGIC_KILL_DAMAGE_CLASSES = PROGRESSION_LOGIC_KILL_DAMAGE_CLASSES - {
    SILVER_ARROW_DAMAGE_CLASS
}
GUARANTEED_LOGIC_KILL_EFFECT = 0x64
KEY_DROP_INCINERATION_REQUIRED_SPRITE_NAMES = frozenset({"Red Bari"})
BOSS_DAMAGE_CLASS_RANDOMIZER_SPRITE_IDS = frozenset({
    MOLDORM_SPRITE_ID,
    ARMOS_KNIGHTS_SPRITE_ID,
    LANMOLAS_SPRITE_ID,
    MOTHULA_SPRITE_ID,
    ARRGHUS_SPRITE_ID,
    ARRGHUS_FUZZ_SPRITE_ID,
    HELMASAUR_KING_SPRITE_ID,
    KHOLDSTARE_SPRITE_ID,
    KHOLDSTARE_ICE_BLOCK_SPRITE_ID,
    VITREOUS_SMALL_EYE_SPRITE_ID,
    VITREOUS_SPRITE_ID,
    TRINEXX_MAIN_HEAD_SPRITE_ID,
    TRINEXX_RED_HEAD_SPRITE_ID,
    TRINEXX_BLUE_HEAD_SPRITE_ID,
    BLIND_SPRITE_ID,
    GANON_D6_SPRITE_ID,
    GANON_D7_SPRITE_ID,
})
EXCLUDED_ENEMY_TABLE_SPRITE_IDS = frozenset({
    0x70, 0x7A, 0x7B, 0x89, 0xA4, 0xBF,
})
ENEMY_HEALTH_RANDOMIZER_INCLUDED_SPRITE_IDS = frozenset(
    requirement.sprite_id
    for requirement in ENEMY_SPRITE_REQUIREMENTS
    if requirement.killable
)
STUN_DAMAGE_EFFECTS = frozenset({
    STUN_32_FRAMES_EFFECT,
    STUN_128_FRAMES_EFFECT,
    STUN_255_FRAMES_EFFECT,
})
TRANSFORM_DAMAGE_EFFECTS = frozenset({
    FAIRY_TRANSFORM_EFFECT,
    BLOB_TRANSFORM_EFFECT,
})
SPECIAL_DAMAGE_EFFECTS = frozenset({
    FAIRY_TRANSFORM_EFFECT,
    BLOB_TRANSFORM_EFFECT,
    STUN_32_FRAMES_EFFECT,
    STUN_128_FRAMES_EFFECT,
    INCINERATE_EFFECT,
    FREEZE_EFFECT,
    STUN_255_FRAMES_EFFECT,
})
# These boss rows remain excluded from randomization until Bosses.py uses the
# combat model for boss defeat rules, but the policy is shared with logic tests
# and custom combat-model consumers.
BOSS_SPRITE_IDS_FORBID_SPECIAL_DAMAGE_EFFECTS = frozenset({
    MOLDORM_SPRITE_ID,
    ARMOS_KNIGHTS_SPRITE_ID,
    LANMOLAS_SPRITE_ID,
    ARRGHUS_SPRITE_ID,
    TRINEXX_MAIN_HEAD_SPRITE_ID,
    GANON_D6_SPRITE_ID,
    GANON_D7_SPRITE_ID,
})
BOSS_SPRITE_IDS_ALLOW_ONLY_STUN_SPECIAL_DAMAGE_EFFECTS = frozenset({
    MOTHULA_SPRITE_ID,
    HELMASAUR_KING_SPRITE_ID,
    KHOLDSTARE_SPRITE_ID,
    KHOLDSTARE_ICE_BLOCK_SPRITE_ID,
    VITREOUS_SPRITE_ID,
})
BOSS_SPRITE_IDS_FORBID_TRANSFORM_DAMAGE_EFFECTS = frozenset({
    BLIND_SPRITE_ID,
    VITREOUS_SMALL_EYE_SPRITE_ID,
})
BOSS_SPRITE_IDS_ALLOW_ALL_SPECIAL_DAMAGE_EFFECTS = frozenset({
    ARRGHUS_FUZZ_SPRITE_ID,
    TRINEXX_RED_HEAD_SPRITE_ID,
    TRINEXX_BLUE_HEAD_SPRITE_ID,
})
BOSS_REQUIRED_LOGIC_KILL_DAMAGE_CLASS_GROUPS = {
    MOLDORM_SPRITE_ID: ((3,),),
    ARMOS_KNIGHTS_SPRITE_ID: ((3,),),
    LANMOLAS_SPRITE_ID: ((3,),),
    MOTHULA_SPRITE_ID: ((3,),),
    ARRGHUS_SPRITE_ID: ((3,),),
    ARRGHUS_FUZZ_SPRITE_ID: ((3,),),
    HELMASAUR_KING_SPRITE_ID: ((3,), (9,)),
    KHOLDSTARE_ICE_BLOCK_SPRITE_ID: ((11,),),
    KHOLDSTARE_SPRITE_ID: ((3,),),
    VITREOUS_SMALL_EYE_SPRITE_ID: ((3,),),
    VITREOUS_SPRITE_ID: ((3,),),
    TRINEXX_MAIN_HEAD_SPRITE_ID: ((3,),),
    TRINEXX_RED_HEAD_SPRITE_ID: ((3,),),
    TRINEXX_BLUE_HEAD_SPRITE_ID: ((3,),),
    BLIND_SPRITE_ID: ((3,),),
    GANON_D6_SPRITE_ID: ((3,),),
    GANON_D7_SPRITE_ID: ((9,),),
}
GANON_D7_SWORDLESS_LOGIC_DAMAGE_CLASSES = (0, 3, 6, 9, 10, 11, 12, 13, 14, 15)
BOSS_SWORDLESS_NIGHTMARE_LOGIC_DAMAGE_CLASSES = {
    ARMOS_KNIGHTS_SPRITE_ID: (6, 9, 11, 12, 1, 0),
    LANMOLAS_SPRITE_ID: (6, 9, 11, 12, 1),
    HELMASAUR_KING_SPRITE_ID: (6, 9),
    ARRGHUS_SPRITE_ID: (6, 9, 11, 12),
    ARRGHUS_FUZZ_SPRITE_ID: (6, 9, 11, 12, 3),
    MOTHULA_SPRITE_ID: (11, 1, 3),
    BLIND_SPRITE_ID: (1, 3),
    KHOLDSTARE_ICE_BLOCK_SPRITE_ID: (11, 13),
    KHOLDSTARE_SPRITE_ID: (11, 13, 1, 3),
    VITREOUS_SMALL_EYE_SPRITE_ID: (6, 9, 3),
    VITREOUS_SPRITE_ID: (6, 9, 3),
    TRINEXX_RED_HEAD_SPRITE_ID: (11, 12, 1, 3),
    TRINEXX_BLUE_HEAD_SPRITE_ID: (11, 12, 1, 3),
    GANON_D7_SPRITE_ID: GANON_D7_SWORDLESS_LOGIC_DAMAGE_CLASSES,
}
DAMAGE_CLASS_RANDOMIZER_HP_255_INCLUDED_SPRITE_IDS = frozenset({
    ANTI_FAIRY_SPRITE_ID,
    DEADROCK_SPRITE_ID,
    GANON_D6_SPRITE_ID,
    GANON_D7_SPRITE_ID,
})
DAMAGE_CLASS_RANDOMIZER_FORCE_INCLUDED_SPRITE_IDS = frozenset({
    LIGHTNING_GATE_SPRITE_ID,
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
    item_pool_key: str = "normal",
    available_damage_classes: frozenset[int] | None = None,
    hammer_available_for_freeze: bool = False,
    swordless: bool = False,
) -> EnemyCombatModel:
    if mode == VANILLA_RANDOMIZE_DAMAGE_CLASSES:
        return combat_model

    resolved_effects = _resolve_sprite_damage_effects(combat_model)
    randomized_effects = [list(row) for row in resolved_effects]
    eligible_sprite_ids = _get_damage_class_randomizable_sprite_ids(combat_model, resolved_effects)
    locked_sprite_ids = _get_locked_damage_class_sprite_ids(resolved_effects, eligible_sprite_ids)
    locked_damage_classes = _get_locked_damage_classes_for_item_pool(item_pool_key)

    max_attacks = max(1, max_attacks_in_logic)

    if mode in {DAMAGE_CLASS_SWAP_RANDOMIZE_DAMAGE_CLASSES, MIXED_RANDOMIZE_DAMAGE_CLASSES}:
        damage_class_permutation = _build_valid_damage_class_permutation(
            rng,
            locked_damage_classes,
            randomized_effects,
            eligible_sprite_ids,
            combat_model,
            max_attacks=None,
            enemy_health_key=enemy_health_key,
            available_damage_classes=available_damage_classes,
            hammer_available_for_freeze=hammer_available_for_freeze,
            enforce_non_silver_guarantee=(
                available_damage_classes is not None
                and SILVER_ARROW_DAMAGE_CLASS not in available_damage_classes
            ),
            swordless=swordless,
        )
        randomized_effects = _swap_damage_class_effects(
            randomized_effects,
            eligible_sprite_ids,
            damage_class_permutation,
        )
        _sanitize_randomized_damage_effects(randomized_effects, eligible_sprite_ids, rng)

    if mode in {ENEMY_SWAP_RANDOMIZE_DAMAGE_CLASSES, MIXED_RANDOMIZE_DAMAGE_CLASSES}:
        randomized_effects = _swap_enemy_damage_profiles(
            randomized_effects,
            eligible_sprite_ids,
            rng,
            combat_model,
            max_attacks=max_attacks,
            enemy_health_key=enemy_health_key,
            available_damage_classes=available_damage_classes,
            hammer_available_for_freeze=hammer_available_for_freeze,
            enforce_non_silver_guarantee=(
                available_damage_classes is not None
                and SILVER_ARROW_DAMAGE_CLASS not in available_damage_classes
            ),
            swordless=swordless,
        )
        _sanitize_randomized_damage_effects(randomized_effects, eligible_sprite_ids, rng)

    elif mode == CHAOS_RANDOMIZE_DAMAGE_CLASSES:
        effect_palettes = _build_effect_palettes(resolved_effects, locked_sprite_ids)
        _fill_effect_palettes(effect_palettes, resolved_effects, rng)
        for sprite_id in eligible_sprite_ids:
            randomized_effects[sprite_id] = _build_chaos_sprite_damage_effects(effect_palettes, rng)
        _sanitize_randomized_damage_effects(randomized_effects, eligible_sprite_ids, rng)

    elif mode == NIGHTMARE_RANDOMIZE_DAMAGE_CLASSES:
        effect_palettes = _build_effect_palettes(resolved_effects, locked_sprite_ids)
        _fill_effect_palettes(effect_palettes, resolved_effects, rng)
        nightmare_damage_classes = available_damage_classes
        if nightmare_damage_classes is not None:
            nightmare_damage_classes = nightmare_damage_classes - locked_damage_classes
        for sprite_id in eligible_sprite_ids:
            randomized_effects[sprite_id] = _build_nightmare_sprite_damage_effects(
                sprite_id,
                effect_palettes,
                rng,
                combat_model,
                max_attacks_in_logic=max_attacks_in_logic,
                enemy_health_key=enemy_health_key,
                available_damage_classes=nightmare_damage_classes,
                hammer_available_for_freeze=hammer_available_for_freeze,
                swordless=swordless,
            )

    elif mode not in {
        DAMAGE_CLASS_SWAP_RANDOMIZE_DAMAGE_CLASSES,
        ENEMY_SWAP_RANDOMIZE_DAMAGE_CLASSES,
        MIXED_RANDOMIZE_DAMAGE_CLASSES,
    }:
        raise ValueError(f"Unknown damage class randomization mode: {mode}")

    if mode == CHAOS_RANDOMIZE_DAMAGE_CLASSES:
        _ensure_damage_class_logic_guarantees(
            randomized_effects,
            eligible_sprite_ids,
            combat_model,
            max_attacks_in_logic=max_attacks_in_logic,
            enemy_health_key=enemy_health_key,
            available_damage_classes=available_damage_classes,
            hammer_available_for_freeze=hammer_available_for_freeze,
            enforce_non_silver_guarantee=(
                available_damage_classes is not None
                and SILVER_ARROW_DAMAGE_CLASS not in available_damage_classes
            ),
            swordless=swordless,
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


def _get_damage_class_randomizable_sprite_ids(
    combat_model: EnemyCombatModel,
    resolved_effects: tuple[tuple[int, ...], ...],
) -> tuple[int, ...]:
    max_sprite_id = min(
        len(combat_model.sprite_damage_subclasses),
        REACHABLE_SPRITE_DAMAGE_SUBCLASS_COUNT,
        len(combat_model.enemy_health_table),
        len(resolved_effects),
    )
    return tuple(
        sprite_id
        for sprite_id in range(max_sprite_id)
        if sprite_id not in EXCLUDED_ENEMY_TABLE_SPRITE_IDS
        and _has_nonzero_damage_profile(resolved_effects[sprite_id])
        and (
            combat_model.enemy_health_table[sprite_id] != 0xFF
            or sprite_id in DAMAGE_CLASS_RANDOMIZER_HP_255_INCLUDED_SPRITE_IDS
            or sprite_id in DAMAGE_CLASS_RANDOMIZER_FORCE_INCLUDED_SPRITE_IDS
        )
    )


def _has_nonzero_damage_profile(row: tuple[int, ...]) -> bool:
    return any(effect != 0 for effect in row)


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


def _get_locked_damage_classes_for_item_pool(item_pool_key: str) -> frozenset[int]:
    if item_pool_key == "hard":
        return frozenset({4})
    if item_pool_key == "expert":
        return frozenset({4, 5})
    return frozenset()


def _build_damage_class_permutation(
    rng: random.Random,
    locked_damage_classes: frozenset[int],
) -> tuple[int, ...]:
    shufflable_damage_classes = [
        damage_class
        for damage_class in range(RANDOMIZABLE_DAMAGE_CLASS_COUNT)
        if damage_class not in locked_damage_classes
    ]
    shuffled_damage_classes = shufflable_damage_classes.copy()
    rng.shuffle(shuffled_damage_classes)

    damage_class_permutation = list(range(RANDOMIZABLE_DAMAGE_CLASS_COUNT))
    for damage_class, source_damage_class in zip(shufflable_damage_classes, shuffled_damage_classes):
        damage_class_permutation[damage_class] = source_damage_class
    return tuple(damage_class_permutation)


def _build_valid_damage_class_permutation(
    rng: random.Random,
    locked_damage_classes: frozenset[int],
    randomized_effects: list[list[int]],
    eligible_sprite_ids: tuple[int, ...],
    combat_model: EnemyCombatModel,
    *,
    max_attacks: int | None,
    enemy_health_key: str,
    available_damage_classes: frozenset[int] | None,
    hammer_available_for_freeze: bool,
    enforce_non_silver_guarantee: bool,
    swordless: bool,
) -> tuple[int, ...]:
    constraints = _build_damage_class_permutation_constraints(
        randomized_effects,
        eligible_sprite_ids,
        combat_model,
        max_attacks=max_attacks,
        enemy_health_key=enemy_health_key,
        available_damage_classes=available_damage_classes,
        hammer_available_for_freeze=hammer_available_for_freeze,
        enforce_non_silver_guarantee=enforce_non_silver_guarantee,
        swordless=swordless,
    )
    locked_assignments = {
        damage_class: damage_class
        for damage_class in locked_damage_classes
    }
    unused_source_classes = set(range(RANDOMIZABLE_DAMAGE_CLASS_COUNT)) - set(locked_assignments.values())
    target_damage_classes = [
        damage_class
        for damage_class in range(RANDOMIZABLE_DAMAGE_CLASS_COUNT)
        if damage_class not in locked_assignments
    ]
    target_damage_classes.sort(
        key=lambda damage_class: -sum(
            damage_class in target_damage_classes
            for target_damage_classes, _ in constraints
        )
    )

    assignment = _solve_damage_class_permutation(
        rng,
        constraints,
        locked_assignments,
        target_damage_classes,
        unused_source_classes,
    )
    if assignment is None:
        return _build_damage_class_permutation(rng, locked_damage_classes)

    permutation = tuple(assignment[damage_class] for damage_class in range(RANDOMIZABLE_DAMAGE_CLASS_COUNT))
    if not _damage_class_permutation_preserves_logic(
        permutation,
        randomized_effects,
        eligible_sprite_ids,
        combat_model,
        max_attacks=max_attacks,
        enemy_health_key=enemy_health_key,
        available_damage_classes=available_damage_classes,
        hammer_available_for_freeze=hammer_available_for_freeze,
        enforce_non_silver_guarantee=enforce_non_silver_guarantee,
        swordless=swordless,
    ):
        return _build_damage_class_permutation(rng, locked_damage_classes)
    return permutation


def _build_damage_class_permutation_constraints(
    randomized_effects: list[list[int]],
    eligible_sprite_ids: tuple[int, ...],
    combat_model: EnemyCombatModel,
    *,
    max_attacks: int | None,
    enemy_health_key: str,
    available_damage_classes: frozenset[int] | None,
    hammer_available_for_freeze: bool,
    enforce_non_silver_guarantee: bool,
    swordless: bool,
) -> list[tuple[frozenset[int], frozenset[int]]]:
    constraints = []
    for sprite_id in eligible_sprite_ids:
        if sprite_id == LIGHTNING_GATE_SPRITE_ID:
            continue

        hp = get_enemy_health_for_logic(sprite_id, enemy_health_key, combat_model=combat_model)
        if hp is None:
            continue

        source_damage_classes = frozenset(
            damage_class
            for damage_class in range(RANDOMIZABLE_DAMAGE_CLASS_COUNT)
            if _effect_is_allowed_logic_kill(
                sprite_id,
                randomized_effects[sprite_id][damage_class],
                hp,
                max_attacks,
                allow_frozen_hammer_kill=hammer_available_for_freeze,
            )
        )
        if not source_damage_classes:
            continue

        candidate_damage_classes = _filter_available_logic_damage_classes(
            get_progression_kill_damage_classes(sprite_id),
            available_damage_classes,
        )
        _add_damage_class_permutation_constraint(
            constraints,
            candidate_damage_classes,
            source_damage_classes,
        )

        if enforce_non_silver_guarantee:
            non_silver_candidate_damage_classes = _filter_available_logic_damage_classes(
                get_non_silver_progression_kill_damage_classes(sprite_id),
                available_damage_classes,
            )
            _add_damage_class_permutation_constraint(
                constraints,
                non_silver_candidate_damage_classes,
                source_damage_classes,
            )

        for required_damage_classes in _get_required_logic_kill_damage_class_groups(sprite_id, swordless):
            required_damage_classes = _filter_available_logic_damage_classes(
                required_damage_classes,
                available_damage_classes,
                fallback_to_original=False,
            )
            _add_damage_class_permutation_constraint(
                constraints,
                required_damage_classes,
                source_damage_classes,
            )

        if sprite_id == RED_BARI_SPRITE_ID:
            red_bari_incineration_classes = _filter_available_logic_damage_classes(
                get_progression_kill_damage_classes(RED_BARI_SPRITE_ID),
                available_damage_classes,
                fallback_to_original=False,
            )
            red_bari_source_damage_classes = frozenset(
                damage_class
                for damage_class in range(RANDOMIZABLE_DAMAGE_CLASS_COUNT)
                if randomized_effects[sprite_id][damage_class] == INCINERATE_EFFECT
            )
            _add_damage_class_permutation_constraint(
                constraints,
                red_bari_incineration_classes,
                red_bari_source_damage_classes,
            )

    constraints.sort(key=lambda constraint: (len(constraint[0]) * len(constraint[1]), len(constraint[0])))
    return constraints


def _add_damage_class_permutation_constraint(
    constraints: list[tuple[frozenset[int], frozenset[int]]],
    target_damage_classes: tuple[int, ...],
    source_damage_classes: frozenset[int],
) -> None:
    if target_damage_classes and source_damage_classes:
        constraints.append((frozenset(target_damage_classes), source_damage_classes))


def _solve_damage_class_permutation(
    rng: random.Random,
    constraints: list[tuple[frozenset[int], frozenset[int]]],
    assignment: dict[int, int],
    target_damage_classes: list[int],
    unused_source_classes: set[int],
) -> dict[int, int] | None:
    if not _damage_class_permutation_constraints_remain_possible(constraints, assignment, unused_source_classes):
        return None
    if not target_damage_classes:
        if _damage_class_permutation_constraints_are_satisfied(constraints, assignment):
            return assignment.copy()
        return None

    target_damage_class = target_damage_classes[0]
    candidate_source_classes = list(unused_source_classes)
    rng.shuffle(candidate_source_classes)
    candidate_source_classes.sort(key=lambda source_damage_class: source_damage_class == target_damage_class)

    for source_damage_class in candidate_source_classes:
        assignment[target_damage_class] = source_damage_class
        remaining_source_classes = unused_source_classes - {source_damage_class}
        solution = _solve_damage_class_permutation(
            rng,
            constraints,
            assignment,
            target_damage_classes[1:],
            remaining_source_classes,
        )
        if solution is not None:
            return solution
        del assignment[target_damage_class]

    return None


def _damage_class_permutation_constraints_are_satisfied(
    constraints: list[tuple[frozenset[int], frozenset[int]]],
    assignment: dict[int, int],
) -> bool:
    return all(
        any(assignment.get(target_damage_class) in source_damage_classes
            for target_damage_class in target_damage_classes)
        for target_damage_classes, source_damage_classes in constraints
    )


def _damage_class_permutation_constraints_remain_possible(
    constraints: list[tuple[frozenset[int], frozenset[int]]],
    assignment: dict[int, int],
    unused_source_classes: set[int],
) -> bool:
    for target_damage_classes, source_damage_classes in constraints:
        satisfied = False
        possible = False
        for target_damage_class in target_damage_classes:
            if target_damage_class in assignment:
                if assignment[target_damage_class] in source_damage_classes:
                    satisfied = True
                    break
            elif unused_source_classes & source_damage_classes:
                possible = True
        if not satisfied and not possible:
            return False
    return True


def _damage_class_permutation_preserves_logic(
    permutation: tuple[int, ...],
    randomized_effects: list[list[int]],
    eligible_sprite_ids: tuple[int, ...],
    combat_model: EnemyCombatModel,
    *,
    max_attacks: int | None,
    enemy_health_key: str,
    available_damage_classes: frozenset[int] | None,
    hammer_available_for_freeze: bool,
    enforce_non_silver_guarantee: bool,
    swordless: bool,
) -> bool:
    for sprite_id in eligible_sprite_ids:
        hp = get_enemy_health_for_logic(sprite_id, enemy_health_key, combat_model=combat_model)
        if (
            sprite_id != LIGHTNING_GATE_SPRITE_ID
            and hp is not None
            and not any(
                _effect_is_allowed_logic_kill(
                    sprite_id,
                    randomized_effects[sprite_id][damage_class],
                    hp,
                    max_attacks,
                    allow_frozen_hammer_kill=hammer_available_for_freeze,
                )
                for damage_class in range(RANDOMIZABLE_DAMAGE_CLASS_COUNT)
            )
        ):
            continue
        row = [
            randomized_effects[sprite_id][permutation[damage_class]]
            for damage_class in range(RANDOMIZABLE_DAMAGE_CLASS_COUNT)
        ]
        for damage_class, effect in enumerate(row):
            if not _damage_effect_allowed_for_sprite(sprite_id, effect):
                row[damage_class] = 0
        if not _row_compatible_for_sprite_logic(
            sprite_id,
            tuple(row),
            combat_model,
            max_attacks=max_attacks,
            enemy_health_key=enemy_health_key,
            available_damage_classes=available_damage_classes,
            hammer_available_for_freeze=hammer_available_for_freeze,
            enforce_non_silver_guarantee=enforce_non_silver_guarantee,
            swordless=swordless,
        ):
            return False
    return True


def _swap_damage_class_effects(
    randomized_effects: list[list[int]],
    eligible_sprite_ids: tuple[int, ...],
    damage_class_permutation: tuple[int, ...],
) -> list[list[int]]:
    output = [list(row) for row in randomized_effects]
    for sprite_id in eligible_sprite_ids:
        row = randomized_effects[sprite_id]
        output[sprite_id] = [
            row[damage_class_permutation[damage_class]]
            for damage_class in range(RANDOMIZABLE_DAMAGE_CLASS_COUNT)
        ]
    return output


def _swap_enemy_damage_profiles(
    randomized_effects: list[list[int]],
    eligible_sprite_ids: tuple[int, ...],
    rng: random.Random,
    combat_model: EnemyCombatModel,
    *,
    max_attacks: int | None,
    enemy_health_key: str,
    available_damage_classes: frozenset[int] | None,
    hammer_available_for_freeze: bool,
    enforce_non_silver_guarantee: bool,
    swordless: bool,
) -> list[list[int]]:
    profiles = [
        (sprite_id, tuple(randomized_effects[sprite_id]))
        for sprite_id in eligible_sprite_ids
    ]
    remaining_profiles = profiles.copy()
    rng.shuffle(remaining_profiles)

    target_sprite_ids = list(eligible_sprite_ids)
    rng.shuffle(target_sprite_ids)
    target_sprite_ids.sort(
        key=lambda sprite_id: sum(
            int(_row_allowed_for_sprite(sprite_id, profile))
            for _, profile in profiles
        )
    )

    assigned_profiles: dict[int, list[int]] = {}
    for target_sprite_id in target_sprite_ids:
        candidate_indexes = [
            index
            for index, (_, profile) in enumerate(remaining_profiles)
            if _row_compatible_for_sprite_logic(
                target_sprite_id,
                profile,
                combat_model,
                max_attacks=max_attacks,
                enemy_health_key=enemy_health_key,
                available_damage_classes=available_damage_classes,
                hammer_available_for_freeze=hammer_available_for_freeze,
                enforce_non_silver_guarantee=enforce_non_silver_guarantee,
                swordless=swordless,
            )
        ]
        if candidate_indexes:
            _, profile = remaining_profiles.pop(rng.choice(candidate_indexes))
            assigned_profiles[target_sprite_id] = list(profile)
            continue

        compatible_profiles = [
            profile
            for _, profile in profiles
            if _row_compatible_for_sprite_logic(
                target_sprite_id,
                profile,
                combat_model,
                max_attacks=max_attacks,
                enemy_health_key=enemy_health_key,
                available_damage_classes=available_damage_classes,
                hammer_available_for_freeze=hammer_available_for_freeze,
                enforce_non_silver_guarantee=enforce_non_silver_guarantee,
                swordless=swordless,
            )
        ]
        if compatible_profiles:
            assigned_profiles[target_sprite_id] = list(rng.choice(compatible_profiles))
            continue

        assigned_profiles[target_sprite_id] = list(randomized_effects[target_sprite_id])

    output = [list(row) for row in randomized_effects]
    for sprite_id, profile in assigned_profiles.items():
        output[sprite_id] = profile
    return output


def _sanitize_randomized_damage_effects(
    randomized_effects: list[list[int]],
    eligible_sprite_ids: tuple[int, ...],
    rng: random.Random,
) -> None:
    effect_palettes = _build_effect_palettes(tuple(tuple(row) for row in randomized_effects))
    for sprite_id in eligible_sprite_ids:
        row = randomized_effects[sprite_id]
        for damage_class, effect in enumerate(row):
            if not _damage_effect_allowed_for_sprite(sprite_id, effect):
                row[damage_class] = 0
        _enforce_upgrade_damage_safety(row, rng, effect_palettes)


def _fit_randomized_damage_effects_to_locked_palettes(
    randomized_effects: list[list[int]],
    eligible_sprite_ids: tuple[int, ...],
    locked_sprite_ids: tuple[int, ...],
    rng: random.Random,
) -> None:
    effect_palettes = _build_effect_palettes(tuple(tuple(row) for row in randomized_effects), locked_sprite_ids)
    for sprite_id in eligible_sprite_ids:
        randomized_effects[sprite_id] = _fit_sprite_damage_effects(
            randomized_effects[sprite_id],
            effect_palettes,
            rng,
        )


def _row_allowed_for_sprite(sprite_id: int, row: tuple[int, ...]) -> bool:
    return all(_damage_effect_allowed_for_sprite(sprite_id, effect) for effect in row)


def _row_compatible_for_sprite_logic(
    sprite_id: int,
    row: tuple[int, ...],
    combat_model: EnemyCombatModel,
    *,
    max_attacks: int | None,
    enemy_health_key: str,
    available_damage_classes: frozenset[int] | None,
    hammer_available_for_freeze: bool,
    enforce_non_silver_guarantee: bool,
    swordless: bool,
) -> bool:
    if not _row_allowed_for_sprite(sprite_id, row):
        return False
    if sprite_id == LIGHTNING_GATE_SPRITE_ID:
        return True

    hp = get_enemy_health_for_logic(sprite_id, enemy_health_key, combat_model=combat_model)
    if hp is None:
        return True

    guarantee_attacks = None if sprite_id in BOSS_DAMAGE_CLASS_RANDOMIZER_SPRITE_IDS else max_attacks
    candidate_damage_classes = _filter_available_logic_damage_classes(
        get_progression_kill_damage_classes(sprite_id),
        available_damage_classes,
    )
    if not _has_direct_kill_within_attack_limit(
        list(row),
        sprite_id,
        hp,
        guarantee_attacks,
        candidate_damage_classes,
        allow_frozen_hammer_kill=hammer_available_for_freeze,
    ):
        return False

    if enforce_non_silver_guarantee:
        non_silver_candidate_damage_classes = _filter_available_logic_damage_classes(
            get_non_silver_progression_kill_damage_classes(sprite_id),
            available_damage_classes,
        )
        if non_silver_candidate_damage_classes and not _has_direct_kill_within_attack_limit(
            list(row),
            sprite_id,
            hp,
            guarantee_attacks,
            non_silver_candidate_damage_classes,
            allow_frozen_hammer_kill=hammer_available_for_freeze,
        ):
            return False

    for required_damage_classes in _get_required_logic_kill_damage_class_groups(sprite_id, swordless):
        required_damage_classes = _filter_available_logic_damage_classes(
            required_damage_classes,
            available_damage_classes,
            fallback_to_original=False,
        )
        if required_damage_classes and not _has_direct_kill_within_attack_limit(
            list(row),
            sprite_id,
            hp,
            guarantee_attacks,
            required_damage_classes,
            allow_frozen_hammer_kill=hammer_available_for_freeze,
        ):
            return False

    if sprite_id == RED_BARI_SPRITE_ID:
        red_bari_incineration_classes = _filter_available_logic_damage_classes(
            get_progression_kill_damage_classes(RED_BARI_SPRITE_ID),
            available_damage_classes,
            fallback_to_original=False,
        )
        if red_bari_incineration_classes and not any(
            row[damage_class] == INCINERATE_EFFECT
            for damage_class in red_bari_incineration_classes
        ):
            return False

    return True


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
    available_damage_classes: frozenset[int] | None,
    hammer_available_for_freeze: bool,
    enforce_non_silver_guarantee: bool,
    swordless: bool,
) -> None:
    max_attacks = max(1, max_attacks_in_logic)
    effect_palettes = _build_effect_palettes(tuple(tuple(row) for row in randomized_effects))

    for sprite_id in eligible_sprite_ids:
        guarantee_attacks = None if sprite_id in BOSS_DAMAGE_CLASS_RANDOMIZER_SPRITE_IDS else max_attacks
        hp = get_enemy_health_for_logic(sprite_id, enemy_health_key, combat_model=combat_model)
        if hp is None:
            continue
        row = randomized_effects[sprite_id]
        candidate_damage_classes = _filter_available_logic_damage_classes(
            get_progression_kill_damage_classes(sprite_id),
            available_damage_classes,
        )
        if not _has_direct_kill_within_attack_limit(
            row,
            sprite_id,
            hp,
            guarantee_attacks,
            candidate_damage_classes,
            allow_frozen_hammer_kill=hammer_available_for_freeze,
        ):
            _set_guaranteed_logic_kill_effect_for_row(
                row,
                effect_palettes,
                sprite_id,
                hp,
                guarantee_attacks,
                candidate_damage_classes,
                allow_frozen_hammer_kill=hammer_available_for_freeze,
            )

        if enforce_non_silver_guarantee:
            non_silver_candidate_damage_classes = _filter_available_logic_damage_classes(
                get_non_silver_progression_kill_damage_classes(sprite_id),
                available_damage_classes,
            )
            if (
                non_silver_candidate_damage_classes
                and not _has_direct_kill_within_attack_limit(
                    row,
                    sprite_id,
                    hp,
                    guarantee_attacks,
                    non_silver_candidate_damage_classes,
                    allow_frozen_hammer_kill=hammer_available_for_freeze,
                )
            ):
                _set_guaranteed_logic_kill_effect_for_row(
                    row,
                    effect_palettes,
                    sprite_id,
                    hp,
                    guarantee_attacks,
                    non_silver_candidate_damage_classes,
                    allow_frozen_hammer_kill=hammer_available_for_freeze,
                )

        for required_damage_classes in _get_required_logic_kill_damage_class_groups(sprite_id, swordless):
            required_damage_classes = _filter_available_logic_damage_classes(
                required_damage_classes,
                available_damage_classes,
                fallback_to_original=False,
            )
            if not required_damage_classes:
                continue
            if _has_direct_kill_within_attack_limit(
                row,
                sprite_id,
                hp,
                guarantee_attacks,
                required_damage_classes,
                allow_frozen_hammer_kill=hammer_available_for_freeze,
            ):
                continue
            _set_guaranteed_logic_kill_effect_for_row(
                row,
                effect_palettes,
                sprite_id,
                hp,
                guarantee_attacks,
                required_damage_classes,
                allow_frozen_hammer_kill=hammer_available_for_freeze,
            )

    if RED_BARI_SPRITE_ID in eligible_sprite_ids:
        red_bari_row = randomized_effects[RED_BARI_SPRITE_ID]
        red_bari_incineration_classes = _filter_available_logic_damage_classes(
            get_progression_kill_damage_classes(RED_BARI_SPRITE_ID),
            available_damage_classes,
            fallback_to_original=False,
        )
        if red_bari_incineration_classes and not any(
            red_bari_row[damage_class] == INCINERATE_EFFECT
            for damage_class in red_bari_incineration_classes
        ):
            _set_red_bari_incineration_guarantee(red_bari_row, effect_palettes, red_bari_incineration_classes)


def _get_required_logic_kill_damage_class_groups(sprite_id: int, swordless: bool) -> tuple[tuple[int, ...], ...]:
    if swordless and sprite_id == HELMASAUR_KING_SPRITE_ID:
        return ((6,), (9,))
    if swordless and sprite_id == GANON_D7_SPRITE_ID:
        return (GANON_D7_SWORDLESS_LOGIC_DAMAGE_CLASSES,)
    return BOSS_REQUIRED_LOGIC_KILL_DAMAGE_CLASS_GROUPS.get(sprite_id, tuple())


def _filter_available_logic_damage_classes(
    damage_classes: tuple[int, ...],
    available_damage_classes: frozenset[int] | None,
    *,
    fallback_to_original: bool = True,
) -> tuple[int, ...]:
    if available_damage_classes is None:
        return damage_classes
    filtered_damage_classes = tuple(
        damage_class
        for damage_class in damage_classes
        if damage_class in available_damage_classes
    )
    return filtered_damage_classes or (damage_classes if fallback_to_original else tuple())


def _set_red_bari_incineration_guarantee(
    row: list[int],
    effect_palettes: list[set[int]],
    damage_classes: tuple[int, ...],
) -> None:
    for damage_class in damage_classes:
        if _effect_fits_palette(INCINERATE_EFFECT, effect_palettes[damage_class]):
            _set_guaranteed_logic_kill_effect(row, effect_palettes, damage_class, INCINERATE_EFFECT)
            return
    raise ValueError("Could not guarantee Red Bari incineration")


def get_progression_kill_damage_classes(sprite_id: int) -> tuple[int, ...]:
    if sprite_id == MOLDORM_SPRITE_ID:
        return (1, 2, 3, 4, 5, 10)
    if sprite_id == TRINEXX_MAIN_HEAD_SPRITE_ID:
        return (1, 2, 3, 4, 5)
    if sprite_id in {
        ARMOS_KNIGHTS_SPRITE_ID,
        LANMOLAS_SPRITE_ID,
        HELMASAUR_KING_SPRITE_ID,
        ARRGHUS_SPRITE_ID,
        MOTHULA_SPRITE_ID,
        BLIND_SPRITE_ID,
        VITREOUS_SMALL_EYE_SPRITE_ID,
        VITREOUS_SPRITE_ID,
    }:
        return (1, 2, 3, 4, 5, 6, 9, 11, 12)
    if sprite_id == KHOLDSTARE_ICE_BLOCK_SPRITE_ID:
        return (11, 13)
    if sprite_id == KHOLDSTARE_SPRITE_ID:
        return (1, 2, 3, 4, 5, 11, 13)
    if sprite_id in {TRINEXX_RED_HEAD_SPRITE_ID, TRINEXX_BLUE_HEAD_SPRITE_ID}:
        return (1, 2, 3, 4, 5, 11, 12)
    if sprite_id == GANON_D6_SPRITE_ID:
        return (1, 2, 3, 4, 5, 10, 11, 12, 13, 14, 15)
    if sprite_id == GANON_D7_SPRITE_ID:
        return (1, 2, 3, 4, 5, 6, 9, 10, 11, 12, 13, 14, 15)
    if sprite_id == FLOATING_STALFOS_HEAD_SPRITE_ID:
        return (1,)
    if sprite_id == BUZZBLOB_SPRITE_ID:
        return (1, 3, 6, 9, 11, 13)
    if sprite_id == ANTI_FAIRY_SPRITE_ID:
        return (1, 6, 7, 9, 10, 11, 12, 13, 14, 15)
    return tuple(sorted(PROGRESSION_LOGIC_KILL_DAMAGE_CLASSES))


def get_non_silver_progression_kill_damage_classes(sprite_id: int) -> tuple[int, ...]:
    if sprite_id in BOSS_DAMAGE_CLASS_RANDOMIZER_SPRITE_IDS:
        return tuple()
    return tuple(
        damage_class
        for damage_class in get_progression_kill_damage_classes(sprite_id)
        if damage_class in NON_SILVER_PROGRESSION_LOGIC_KILL_DAMAGE_CLASSES
    )


def _has_direct_kill_within_attack_limit(
    row: list[int],
    sprite_id: int,
    hp: int,
    max_attacks: int | None,
    damage_classes: tuple[int, ...],
    *,
    allow_frozen_hammer_kill: bool = False,
) -> bool:
    return any(
        _effect_is_allowed_logic_kill(
            sprite_id,
            row[damage_class],
            hp,
            max_attacks,
            allow_frozen_hammer_kill=allow_frozen_hammer_kill,
        )
        for damage_class in damage_classes
    )


def _effect_is_allowed_logic_kill(
    sprite_id: int,
    effect: int,
    hp: int,
    max_attacks: int | None,
    *,
    allow_frozen_hammer_kill: bool = False,
) -> bool:
    if not _damage_effect_allowed_for_sprite(sprite_id, effect):
        return False
    if effect == FREEZE_EFFECT:
        return allow_frozen_hammer_kill and can_shatter_frozen_sprite_with_hammer(sprite_id)
    return _effect_kills_within_attack_limit(effect, hp, max_attacks)


def _effect_kills_within_attack_limit(effect: int, hp: int, max_attacks: int | None) -> bool:
    if effect == INCINERATE_EFFECT:
        return True
    if not 0 < effect < FAIRY_TRANSFORM_EFFECT:
        return False
    if max_attacks is None:
        return True
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


def _set_guaranteed_logic_kill_effect_for_row(
    row: list[int],
    effect_palettes: list[set[int]],
    sprite_id: int,
    hp: int,
    max_attacks: int | None,
    damage_classes: tuple[int, ...],
    *,
    allow_frozen_hammer_kill: bool = False,
) -> None:
    for damage_class in damage_classes:
        if (
            _effect_is_allowed_logic_kill(
                sprite_id,
                GUARANTEED_LOGIC_KILL_EFFECT,
                hp,
                max_attacks,
                allow_frozen_hammer_kill=allow_frozen_hammer_kill,
            )
            and _effect_fits_palette(GUARANTEED_LOGIC_KILL_EFFECT, effect_palettes[damage_class])
        ):
            _set_guaranteed_logic_kill_effect(
                row,
                effect_palettes,
                damage_class,
                GUARANTEED_LOGIC_KILL_EFFECT,
            )
            return

        for effect in sorted(effect_palettes[damage_class], reverse=True):
            if _effect_is_allowed_logic_kill(
                sprite_id,
                effect,
                hp,
                max_attacks,
                allow_frozen_hammer_kill=allow_frozen_hammer_kill,
            ):
                _set_guaranteed_logic_kill_effect(
                    row,
                    effect_palettes,
                    damage_class,
                    effect,
                )
                return

    for damage_class in damage_classes:
        for effect in (0x64, 0x40, 0x20, 0x10, 0x08, 0x04, 0x03, 0x02, 0x01, INCINERATE_EFFECT, FREEZE_EFFECT):
            if (
                _effect_is_allowed_logic_kill(
                    sprite_id,
                    effect,
                    hp,
                    max_attacks,
                    allow_frozen_hammer_kill=allow_frozen_hammer_kill,
                )
                and _effect_fits_palette(effect, effect_palettes[damage_class])
            ):
                _set_guaranteed_logic_kill_effect(row, effect_palettes, damage_class, effect)
                return

    raise ValueError(f"Could not guarantee a logical damage class for sprite 0x{sprite_id:02X}")


def _get_guaranteed_logic_kill_effect_candidates(
    sprite_id: int,
    hp: int,
    max_attacks: int | None,
    *,
    allow_frozen_hammer_kill: bool = False,
) -> tuple[int, ...]:
    candidates = [GUARANTEED_LOGIC_KILL_EFFECT]
    candidates.extend((0x64, 0x40, 0x20, 0x10, 0x08, 0x04, 0x03, 0x02, 0x01, INCINERATE_EFFECT, FREEZE_EFFECT))
    return tuple(
        effect
        for effect in candidates
        if _effect_is_allowed_logic_kill(
            sprite_id,
            effect,
            hp,
            max_attacks,
            allow_frozen_hammer_kill=allow_frozen_hammer_kill,
        )
    )


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
    if not _sword_class_2_loss_is_safe(fallback):
        fallback[LOST_SWORD_UPGRADE_DAMAGE_CLASS] = 0
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
    if not _sword_class_2_loss_is_safe(candidate):
        candidate[LOST_SWORD_UPGRADE_DAMAGE_CLASS] = 0
    return candidate


def _build_nightmare_sprite_damage_effects(
    sprite_id: int,
    effect_palettes: list[set[int]],
    rng: random.Random,
    combat_model: EnemyCombatModel,
    *,
    max_attacks_in_logic: int,
    enemy_health_key: str,
    available_damage_classes: frozenset[int] | None,
    hammer_available_for_freeze: bool,
    swordless: bool,
) -> list[int]:
    row = [
        _get_nightmare_non_defeating_effect(sprite_id, effect_palettes[damage_class], rng)
        for damage_class in range(RANDOMIZABLE_DAMAGE_CLASS_COUNT)
    ]
    _enforce_upgrade_damage_safety(row, rng, effect_palettes)
    hp = get_enemy_health_for_logic(sprite_id, enemy_health_key, combat_model=combat_model)
    if hp is None:
        _add_row_to_effect_palettes(row, effect_palettes)
        return row

    progression_damage_classes = _get_nightmare_progression_damage_classes(sprite_id, swordless)

    candidate_damage_classes = tuple(
        damage_class
        for damage_class in progression_damage_classes
        if (
            available_damage_classes is None
            or (
                damage_class in available_damage_classes
                and (
                    damage_class != LOST_SWORD_UPGRADE_DAMAGE_CLASS
                    or GOLDEN_SWORD_SPIN_DAMAGE_CLASS in available_damage_classes
                )
            )
            or (
                damage_class == LOST_SWORD_UPGRADE_DAMAGE_CLASS
                and GOLDEN_SWORD_SPIN_DAMAGE_CLASS in available_damage_classes
            )
        )
    )
    if not candidate_damage_classes:
        candidate_damage_classes = progression_damage_classes

    max_attacks = None if sprite_id in BOSS_DAMAGE_CLASS_RANDOMIZER_SPRITE_IDS else max(1, max_attacks_in_logic)
    if sprite_id == RED_BARI_SPRITE_ID:
        _set_nightmare_defeat_effect_for_row(
            row,
            effect_palettes,
            sprite_id,
            hp,
            max_attacks,
            candidate_damage_classes,
            preferred_effect=INCINERATE_EFFECT,
            allow_frozen_hammer_kill=hammer_available_for_freeze,
        )
    else:
        _set_nightmare_defeat_effect_for_row(
            row,
            effect_palettes,
            sprite_id,
            hp,
            max_attacks,
            candidate_damage_classes,
            allow_frozen_hammer_kill=hammer_available_for_freeze,
        )
    _add_row_to_effect_palettes(row, effect_palettes)
    return row


def _get_nightmare_progression_damage_classes(sprite_id: int, swordless: bool) -> tuple[int, ...]:
    if swordless and sprite_id in BOSS_SWORDLESS_NIGHTMARE_LOGIC_DAMAGE_CLASSES:
        return BOSS_SWORDLESS_NIGHTMARE_LOGIC_DAMAGE_CLASSES[sprite_id]
    if sprite_id in BOSS_REQUIRED_LOGIC_KILL_DAMAGE_CLASS_GROUPS:
        return tuple(BOSS_REQUIRED_LOGIC_KILL_DAMAGE_CLASS_GROUPS[sprite_id][0])
    return get_progression_kill_damage_classes(sprite_id)


def _get_nightmare_non_defeating_effect(
    sprite_id: int,
    effect_palette: set[int],
    rng: random.Random,
) -> int:
    candidates = [
        effect
        for effect in effect_palette
        if _damage_effect_allowed_for_sprite(sprite_id, effect)
        and not is_defeating_damage_effect_for_nightmare(effect)
    ]
    if not candidates and _effect_fits_palette(0, effect_palette):
        candidates = [0]
    if not candidates:
        raise ValueError(f"Could not find a non-defeating Nightmare effect for sprite 0x{sprite_id:02X}")
    return rng.choice(tuple(sorted(candidates)))


def _set_nightmare_defeat_effect_for_row(
    row: list[int],
    effect_palettes: list[set[int]],
    sprite_id: int,
    hp: int,
    max_attacks: int,
    damage_classes: tuple[int, ...],
    *,
    preferred_effect: int | None = None,
    allow_frozen_hammer_kill: bool = False,
) -> None:
    if preferred_effect is not None:
        for damage_class in damage_classes:
            if (
                _effect_is_allowed_logic_kill(
                    sprite_id,
                    preferred_effect,
                    hp,
                    max_attacks,
                    allow_frozen_hammer_kill=allow_frozen_hammer_kill,
                )
                and _effect_fits_palette(preferred_effect, effect_palettes[damage_class])
            ):
                _set_guaranteed_logic_kill_effect(row, effect_palettes, damage_class, preferred_effect)
                return

    if LOST_SWORD_UPGRADE_DAMAGE_CLASS in damage_classes:
        paired_damage_classes = (LOST_SWORD_UPGRADE_DAMAGE_CLASS, GOLDEN_SWORD_SPIN_DAMAGE_CLASS)
        effects = _get_guaranteed_logic_kill_effect_candidates(
            sprite_id,
            hp,
            max_attacks,
            allow_frozen_hammer_kill=allow_frozen_hammer_kill,
        ) + tuple(
            effect
            for effect in sorted(
                effect_palettes[LOST_SWORD_UPGRADE_DAMAGE_CLASS] & effect_palettes[GOLDEN_SWORD_SPIN_DAMAGE_CLASS],
                reverse=True,
            )
            if _effect_is_allowed_logic_kill(
                sprite_id,
                effect,
                hp,
                max_attacks,
                allow_frozen_hammer_kill=allow_frozen_hammer_kill,
            )
        )
        for effect in effects:
            if all(_effect_fits_palette(effect, effect_palettes[damage_class]) for damage_class in paired_damage_classes):
                for damage_class in paired_damage_classes:
                    _set_guaranteed_logic_kill_effect(row, effect_palettes, damage_class, effect)
                return

    _set_guaranteed_logic_kill_effect_for_row(
        row,
        effect_palettes,
        sprite_id,
        hp,
        max_attacks,
        damage_classes,
        allow_frozen_hammer_kill=allow_frozen_hammer_kill,
    )


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


def _enforce_upgrade_damage_safety(
    row: list[int],
    rng: random.Random,
    effect_palettes: list[set[int]] | None = None,
) -> None:
    _enforce_sword_upgrade_damage_safety(row, rng, effect_palettes)


def _enforce_sword_upgrade_damage_safety(
    row: list[int],
    rng: random.Random,
    effect_palettes: list[set[int]] | None = None,
) -> None:
    if _sword_class_2_loss_is_safe(row):
        return

    replacement_damage_classes = list(SWORD_CLASS_2_REPLACEMENT_DAMAGE_CLASSES)
    rng.shuffle(replacement_damage_classes)
    class_2_effect = row[LOST_SWORD_UPGRADE_DAMAGE_CLASS]
    for damage_class in replacement_damage_classes:
        if effect_palettes is not None and not _effect_fits_palette(class_2_effect, effect_palettes[damage_class]):
            continue
        row[damage_class] = class_2_effect
        if effect_palettes is not None:
            effect_palettes[damage_class].add(class_2_effect)
        return

    row[LOST_SWORD_UPGRADE_DAMAGE_CLASS] = 0


def _sword_class_2_loss_is_safe(row: list[int]) -> bool:
    class_2_effect = row[LOST_SWORD_UPGRADE_DAMAGE_CLASS]
    if class_2_effect == 0:
        return True

    return any(
        _damage_effect_covers_lost_sword_class_2(row[damage_class], class_2_effect)
        for damage_class in SWORD_CLASS_2_REPLACEMENT_DAMAGE_CLASSES
    )


def _damage_effect_covers_lost_sword_class_2(effect: int, class_2_effect: int) -> bool:
    if _is_special_damage_effect(class_2_effect):
        return effect == class_2_effect
    if is_killing_damage_effect(class_2_effect):
        return is_killing_damage_effect(effect) and not _is_special_damage_effect(effect) and effect >= class_2_effect
    return effect == class_2_effect


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


_DAMAGE_CLASS_EFFECT_CACHE: dict[
    int,
    tuple[EnemyCombatModel, dict[tuple[int, frozenset[int]], tuple[int, ...]]],
] = {}
_KILLING_DAMAGE_CLASS_CACHE: dict[int, tuple[EnemyCombatModel, dict[tuple[int, bool], tuple[int, ...]]]] = {}


def get_damage_classes_with_effects(
    sprite_id: int,
    effects: frozenset[int],
    combat_model: EnemyCombatModel = VANILLA_COMBAT_MODEL,
) -> tuple[int, ...]:
    model_id = id(combat_model)
    cached_model, cache = _DAMAGE_CLASS_EFFECT_CACHE.get(model_id, (None, {}))
    if cached_model is not combat_model:
        cache = {}
        _DAMAGE_CLASS_EFFECT_CACHE[model_id] = (combat_model, cache)
    cache_key = (sprite_id, effects)
    if cache_key in cache:
        return cache[cache_key]

    matching_damage_classes = []
    for damage_class in range(len(combat_model.damage_sources)):
        effect = get_damage_effect(sprite_id, damage_class, combat_model)
        if effect in effects and _damage_effect_allowed_for_sprite(sprite_id, effect):
            matching_damage_classes.append(damage_class)
    result = tuple(matching_damage_classes)
    cache[cache_key] = result
    return result


def is_killing_damage_effect(effect: int) -> bool:
    return 0 < effect < FAIRY_TRANSFORM_EFFECT or effect == INCINERATE_EFFECT


def can_shatter_frozen_sprite_with_hammer(sprite_id: int) -> bool:
    return sprite_id < GANON_D6_SPRITE_ID and _damage_effect_allowed_for_sprite(sprite_id, FREEZE_EFFECT)


def is_defeating_damage_effect_for_nightmare(effect: int) -> bool:
    return is_killing_damage_effect(effect) or effect in TRANSFORM_DAMAGE_EFFECTS or effect == FREEZE_EFFECT


def get_killing_damage_classes(
    sprite_id: int,
    combat_model: EnemyCombatModel = VANILLA_COMBAT_MODEL,
    *,
    include_freeze_hammer: bool = False,
) -> tuple[int, ...]:
    model_id = id(combat_model)
    cached_model, cache = _KILLING_DAMAGE_CLASS_CACHE.get(model_id, (None, {}))
    if cached_model is not combat_model:
        cache = {}
        _KILLING_DAMAGE_CLASS_CACHE[model_id] = (combat_model, cache)
    cache_key = (sprite_id, include_freeze_hammer)
    if cache_key in cache:
        return cache[cache_key]

    matching_damage_classes = []
    for damage_class in range(len(combat_model.damage_sources)):
        effect = get_damage_effect(sprite_id, damage_class, combat_model)
        if _damage_effect_allowed_for_sprite(sprite_id, effect) and (
            is_killing_damage_effect(effect)
            or (
                include_freeze_hammer
                and effect == FREEZE_EFFECT
                and can_shatter_frozen_sprite_with_hammer(sprite_id)
            )
            or (
                sprite_id in BOSS_DAMAGE_CLASS_RANDOMIZER_SPRITE_IDS
                and effect in TRANSFORM_DAMAGE_EFFECTS
            )
        ):
            matching_damage_classes.append(damage_class)
    result = tuple(matching_damage_classes)
    cache[cache_key] = result
    return result


def get_incinerating_damage_classes(
    sprite_id: int,
    combat_model: EnemyCombatModel = VANILLA_COMBAT_MODEL,
) -> tuple[int, ...]:
    return get_damage_classes_with_effects(sprite_id, frozenset({INCINERATE_EFFECT}), combat_model)


def get_blob_transform_damage_classes(
    sprite_id: int,
    combat_model: EnemyCombatModel = VANILLA_COMBAT_MODEL,
) -> tuple[int, ...]:
    return get_damage_classes_with_effects(sprite_id, frozenset({BLOB_TRANSFORM_EFFECT}), combat_model)


def _damage_effect_allowed_for_sprite(sprite_id: int, effect: int) -> bool:
    if not _is_special_damage_effect(effect):
        return True
    if sprite_id in BOSS_SPRITE_IDS_ALLOW_ALL_SPECIAL_DAMAGE_EFFECTS:
        return True
    if sprite_id in BOSS_SPRITE_IDS_FORBID_SPECIAL_DAMAGE_EFFECTS:
        return False
    if sprite_id in BOSS_SPRITE_IDS_ALLOW_ONLY_STUN_SPECIAL_DAMAGE_EFFECTS:
        return effect in STUN_DAMAGE_EFFECTS
    if sprite_id in BOSS_SPRITE_IDS_FORBID_TRANSFORM_DAMAGE_EFFECTS:
        return effect not in TRANSFORM_DAMAGE_EFFECTS
    return True


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

    if hp_override is not None:
        hp = hp_override
    elif enemy_health_key != "default" and hp != 0xFF and sprite_id not in EXCLUDED_ENEMY_TABLE_SPRITE_IDS:
        hp = ENEMY_HEALTH_RANGE_BY_KEY[enemy_health_key][1] - 1
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
    allow_frozen_hammer_kill: bool = False,
) -> int | None:
    effect = get_damage_effect(sprite_id, damage_class, combat_model)
    if not _damage_effect_allowed_for_sprite(sprite_id, effect):
        return None
    if effect == FREEZE_EFFECT and allow_frozen_hammer_kill and can_shatter_frozen_sprite_with_hammer(sprite_id):
        return 1
    if effect == INCINERATE_EFFECT or (
        sprite_id in BOSS_DAMAGE_CLASS_RANDOMIZER_SPRITE_IDS
        and effect in TRANSFORM_DAMAGE_EFFECTS
    ):
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
