from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING

from Utils import snes_to_pc

from .enemizer_data.default_dungeon_room_enemies import DEFAULT_DUNGEON_ROOM_ENEMIES
from .enemizer_data.dungeon_sprite_addresses import DUNGEON_SPRITE_ADDRESSES, KEYED_SPRITE_ID_ADDRESSES
from .enemizer_data.enemy_shuffle_base_data import DUNGEON_ENEMY_ROOMS, DUNGEON_SPRITE_GROUPS, OVERWORLD_ENEMY_AREAS
from .enemizer_data.enemy_combat_data import (
    BLOB_TRANSFORM_EFFECT,
    DIRECT_KILL_DELIVERY_OVERRIDES,
    FAIRY_TRANSFORM_EFFECT,
    KEY_DROP_INCINERATION_REQUIRED_SPRITE_NAMES,
    EnemyCombatModel,
    VANILLA_COMBAT_MODEL,
    YELLOW_SLIME_SPRITE_ID,
    get_blob_transform_damage_classes,
    get_damage_effect,
    get_incinerating_damage_classes,
    get_killing_damage_classes,
    get_hits_to_kill,
    get_progression_kill_damage_classes,
    get_yellow_slime_follow_up_delivery_override,
    with_killable_thief_combat_model,
)
from .enemizer_data.enemy_room_metadata import (
    BOSS_ROOM_IDS,
    DONT_RANDOMIZE_ROOM_IDS,
    NO_SPECIAL_ENEMIES_STANDARD_ROOM_IDS,
    ROOM_GROUP_REQUIREMENTS,
    SHUTTER_ROOM_IDS,
    WATER_ROOM_IDS,
)
from .enemizer_data.enemy_sprite_requirements import ENEMY_SPRITE_REQUIREMENTS
from .enemizer_data.overworld_enemy_metadata import (
    AREA_IDS,
    DO_NOT_RANDOMIZE_AREA_IDS,
    FORCED_GROUP_REQUIREMENTS,
)
from .enemizer_data.room_names import ROOM_NAME_TO_ID
from .enemizer_data.symbols import ENEMIZER_SYMBOLS

if TYPE_CHECKING:
    from . import ALTTPWorld
    from .Rom import TokenRom


DUNGEON_HEADER_POINTER_TABLE_BASE = 0x271E2
DUNGEON_SPRITE_POINTER_TABLE_BASE = 0x4D62E
OVERWORLD_SPRITE_POINTER_TABLE_BASE = 0x4C901
OVERWORLD_AREA_GRAPHICS_BLOCK_BASE = 0x7A81
ROOM_HEADER_BANK_LOCATION = 0xB5E7
SPRITE_GROUP_BASE_ADDRESS = 0x5B97
TOTAL_SPRITE_GROUPS = 144
TOTAL_DUNGEON_ROOMS = 0x128

SPRITE_OVERLORD_MASK = 0xE0
SPRITE_OVERLORD_REMOVE_MASK = 0x1F
SPRITE_SUBTYPE_BYTE_0_MASK = 0x60
KEY_SPRITE_ID = 0xE4
BIG_KEY_SPRITE_ID = 0xE5
WALLMASTER_SPRITE_ID = 0x90
STAL_SPRITE_ID = 0xD3
FLOPPING_FISH_SPRITE_ID = 0xD2
OW_FALLING_ROCKS_SPRITE_ID = 0xF4
OW_WALLMASTER_TO_HOULIHAN_SPRITE_ID = 0xFB
WATER_TEKTITE_SPRITE_ID = 0x81
ROOM_CLEAR_IGNORED_SPRITE_IDS = frozenset({
    0x15,  # Anti-Fairy
    0x5B,  # Spark (clockwise)
    0x5C,  # Spark (counter-clockwise)
    0x61,  # Beamos
    0x7D,  # Big Spike Trap
    0x82,  # Anti-Fairy Circle
    0x8A,  # Spike Trap
    0x9A,  # Kyameron
    0xE8,  # Fake Master Sword
})
KEY_DROP_DELIVERY_DAMAGE_CLASSES_BY_ITEM = {
    "Fighter Sword": frozenset((1, 2)),
    "Master Sword": frozenset((1, 2, 3)),
    "Tempered Sword": frozenset((1, 2, 3, 4)),
    "Golden Sword": frozenset((1, 3, 4, 5)),
    "Hammer": frozenset((3,)),
    "Blue Boomerang": frozenset((0,)),
    "Red Boomerang": frozenset((0,)),
    "Cane of Somaria": frozenset((1,)),
    "Cane of Byrna": frozenset((1,)),
    "Bow": frozenset((6,)),
    "Silver Bow": frozenset((9,)),
    "Hookshot": frozenset((7,)),
    "Magic Powder": frozenset((10,)),
    "Fire Rod": frozenset((11,)),
    "Ice Rod": frozenset((12,)),
    "Bombos": frozenset((13,)),
    "Ether": frozenset((14,)),
    "Quake": frozenset((15,)),
}
KEY_DROP_DELIVERY_DAMAGE_CLASSES_BY_ABILITY = {
    "bombs": frozenset((8,)),
    "sword_beams": frozenset((1,)),
}
POTENTIAL_SUBGROUP_0 = (22, 31, 47, 14)
POTENTIAL_SUBGROUP_1 = (44, 30, 32)
POTENTIAL_SUBGROUP_2 = (12, 18, 23, 24, 28, 46, 34, 35, 39, 40, 38, 41, 36, 37, 42)
POTENTIAL_SUBGROUP_3 = (17, 16, 27, 20, 82, 83)
IMPOSSIBLE_GRAPHICS_VALUE = -1
STANDARD_ESCAPE_OVERWORLD_AREA_IDS = frozenset((0x1B, 0x2B, 0x2C))
STANDARD_ESCAPE_DUNGEON_ROOM_IDS = frozenset((
    0x21,  # Hyrule Castle (Key-rat Room)
    0x71,  # Hyrule Castle (Boomerang Chest Room)
    0x72,  # Hyrule Castle (Map Chest Room)
    0x80,  # Hyrule Castle (Jail Cell Room)
))
# Standard opening escape uses the separate Beginning-mode overworld sheets rather than
# the ordinary area graphics-block bytes. The three relevant groups are the runtime
# Beginning sheet observed in Hyrule Castle courtyard (group 2) plus the first-part
# graphics blocks used by the linked courtyard/Link's House screens (groups 0 and 1).
STANDARD_BEGINNING_OVERWORLD_GROUP_IDS = frozenset((0x00, 0x01, 0x02))
GUARD_SUBGROUP_1_DUNGEON_GROUP_IDS = frozenset((1, 2, 3, 4))
SELECTED_BOSS_GROUP_REQUIREMENTS = {
    "Armos": (9, 83),
    "Lanmola": (11, 84),
    "Moldorm": (12, 9),
    "Arrghus": (20, 140),
    "Helmasaur": (21, 146),
    "Kholdstare": (22, 162),
    "Vitreous": (22, 189),
    "Trinexx": (23, 203),
    "Mothula": (26, 136),
    "Blind": (32, 206),
}

@dataclass(frozen=True)
class RoomGroupRequirement:
    group_id: Optional[int]
    subgroup_0: Optional[int]
    subgroup_1: Optional[int]
    subgroup_2: Optional[int]
    subgroup_3: Optional[int]
    rooms: tuple[int, ...]


@dataclass(frozen=True)
class OverworldGroupRequirement:
    group_id: Optional[int]
    subgroup_0: Optional[int]
    subgroup_1: Optional[int]
    subgroup_2: Optional[int]
    subgroup_3: Optional[int]
    areas: tuple[int, ...]


@dataclass
class DungeonSpriteGroup:
    group_id: int
    dungeon_group_id: int
    subgroup_0: int
    subgroup_1: int
    subgroup_2: int
    subgroup_3: int
    preserve_subgroup_0: bool = False
    preserve_subgroup_1: bool = False
    preserve_subgroup_2: bool = False
    preserve_subgroup_3: bool = False


@dataclass(frozen=True)
class EnemySpriteRequirement:
    sprite_name: str
    sprite_id: int
    boss: bool
    overlord: bool
    do_not_randomize: bool
    killable: bool
    counts_for_enemy_clear: bool
    npc: bool
    never_use_dungeon: bool
    never_use_overworld: bool
    cannot_have_key: bool
    is_object: bool
    absorbable: bool
    is_water_sprite: bool
    is_enemy_sprite: bool
    group_ids: tuple[int, ...]
    subgroup_0: tuple[int, ...]
    subgroup_1: tuple[int, ...]
    subgroup_2: tuple[int, ...]
    subgroup_3: tuple[int, ...]
    parameters: Optional[int]
    special_glitched: bool
    excluded_rooms: tuple[int, ...]
    dont_randomize_rooms: tuple[int, ...]
    spawnable_rooms: tuple[int, ...]
    combat_reference_id: Optional[int] = None


@dataclass(frozen=True)
class DungeonEnemySprite:
    address: int
    byte_0: int
    byte_1: int
    sprite_id: int
    is_overlord: bool
    has_key: bool

    @property
    def is_on_bg2(self) -> bool:
        return bool(self.byte_0 & 0x80)

    @property
    def hm_param(self) -> int:
        return ((self.byte_0 & 0x60) >> 2) | ((self.byte_1 & 0xE0) >> 5)

    @property
    def y_coord_pixels(self) -> int:
        return (self.byte_0 & 0x1F) * 16

    @property
    def x_coord_pixels(self) -> int:
        return (self.byte_1 & 0x1F) * 16


@dataclass(frozen=True)
class DungeonEnemyRoom:
    room_id: int
    room_header_address: int
    sprite_table_address: int
    graphics_block_id: int
    tag_1: int
    tag_2: int
    sort_sprites_value: int
    sprites: tuple[DungeonEnemySprite, ...]
    required_group_id: Optional[int]
    required_subgroup_0: tuple[int, ...]
    required_subgroup_1: tuple[int, ...]
    required_subgroup_2: tuple[int, ...]
    required_subgroup_3: tuple[int, ...]
    is_shutter_room: bool
    is_water_room: bool
    do_not_randomize: bool
    no_special_enemies_standard: bool
    all_sprites: tuple[DungeonEnemySprite, ...] = tuple()


@dataclass(frozen=True)
class RandomizedDungeonEnemySprite:
    address: int
    byte_0: int
    byte_1: int
    original_sprite_id: int
    sprite_id: int
    is_overlord: bool
    has_key: bool

    @property
    def is_on_bg2(self) -> bool:
        return bool(self.byte_0 & 0x80)

    @property
    def hm_param(self) -> int:
        return ((self.byte_0 & 0x60) >> 2) | ((self.byte_1 & 0xE0) >> 5)

    @property
    def y_coord_pixels(self) -> int:
        return (self.byte_0 & 0x1F) * 16

    @property
    def x_coord_pixels(self) -> int:
        return (self.byte_1 & 0x1F) * 16


@dataclass(frozen=True)
class RandomizedDungeonEnemyRoom:
    room_id: int
    room_header_address: int
    sprite_table_address: int
    original_graphics_block_id: int
    graphics_block_id: int
    tag_1: int
    tag_2: int
    sort_sprites_value: int
    sprites: tuple[RandomizedDungeonEnemySprite, ...]
    skipped_randomization: bool


@dataclass(frozen=True)
class EffectiveDungeonEnemySprite:
    requirement: EnemySpriteRequirement
    has_key: bool
    x_coord_pixels: int
    y_coord_pixels: int


@dataclass(frozen=True)
class DefaultDungeonEnemySprite:
    sprite_id: int
    has_key: bool
    x_coord_pixels: int
    y_coord_pixels: int


@dataclass(frozen=True)
class OverworldEnemySprite:
    address: int
    y_coord: int
    x_coord: int
    sprite_id: int


@dataclass(frozen=True)
class OverworldEnemyArea:
    area_id: int
    sprite_table_address: int
    graphics_block_address: int
    graphics_block_id: int
    bush_sprite_id: int
    sprites: tuple[OverworldEnemySprite, ...]
    do_not_randomize: bool


@dataclass(frozen=True)
class RandomizedOverworldEnemySprite:
    address: int
    y_coord: int
    x_coord: int
    original_sprite_id: int
    sprite_id: int


@dataclass(frozen=True)
class RandomizedOverworldEnemyArea:
    area_id: int
    sprite_table_address: int
    graphics_block_address: int
    original_graphics_block_id: int
    graphics_block_id: int
    original_bush_sprite_id: int
    bush_sprite_id: int
    sprites: tuple[RandomizedOverworldEnemySprite, ...]
    skipped_randomization: bool


@dataclass(frozen=True)
class EnemyShuffleState:
    dungeon_rooms: dict[int, DungeonEnemyRoom]
    overworld_areas: dict[int, OverworldEnemyArea]
    sprite_groups: dict[int, DungeonSpriteGroup]
    sprite_requirements: tuple[EnemySpriteRequirement, ...]
    room_group_requirements: tuple[RoomGroupRequirement, ...]
    overworld_group_requirements: tuple[OverworldGroupRequirement, ...]
    shutter_room_ids: frozenset[int]
    water_room_ids: frozenset[int]
    dont_randomize_room_ids: frozenset[int]
    no_special_enemies_standard_room_ids: frozenset[int]
    boss_room_ids: frozenset[int]
    dont_randomize_overworld_area_ids: frozenset[int]
    randomized_dungeon_rooms: dict[int, RandomizedDungeonEnemyRoom]
    randomized_overworld_areas: dict[int, RandomizedOverworldEnemyArea]
    combat_model: EnemyCombatModel = VANILLA_COMBAT_MODEL
    enemy_health_key: str = "default"
    max_attacks_in_logic: int = 16
    killable_thieves: bool = False
    available_damage_classes: frozenset[int] = frozenset(range(16))
    hammer_available_for_freeze: bool = True


def generate_enemy_shuffle_state(world: "ALTTPWorld") -> EnemyShuffleState:
    metadata = _load_enemy_room_metadata()
    overworld_metadata = _load_overworld_enemy_metadata()
    sprite_requirements = _load_enemy_sprite_requirements()
    dungeon_rooms = {
        room.room_id: room
        for room in _load_base_dungeon_rooms(metadata)
    }
    overworld_areas = {
        area.area_id: area
        for area in _load_base_overworld_areas(overworld_metadata)
    }
    sprite_groups = {
        group.group_id: group
        for group in _load_base_sprite_groups()
    }
    original_sprite_groups = _snapshot_sprite_groups(sprite_groups)
    _setup_required_dungeon_groups(world, sprite_groups, metadata["room_requirements"])
    _apply_selected_boss_group_requirements(world, sprite_groups, sprite_requirements)
    _setup_combined_dungeon_room_graphics_groups(world, dungeon_rooms, sprite_groups, sprite_requirements)
    _randomize_dungeon_groups(world, sprite_groups)
    _restore_skipped_room_sprite_groups(world, dungeon_rooms, sprite_groups, sprite_requirements, original_sprite_groups)
    _restore_original_groups_for_rooms_without_possible_groups(
        world,
        dungeon_rooms,
        sprite_groups,
        sprite_requirements,
        original_sprite_groups,
    )
    randomized_dungeon_rooms = _randomize_dungeon_rooms(
        world,
        dungeon_rooms,
        sprite_groups,
        sprite_requirements,
    )
    _setup_required_overworld_groups(sprite_groups, overworld_metadata["forced_group_requirements"])
    _randomize_overworld_groups(world, sprite_groups)
    _restore_standard_beginning_overworld_sprite_groups(
        world,
        sprite_groups,
        original_sprite_groups,
    )
    randomized_overworld_areas = _randomize_overworld_areas(
        world,
        overworld_areas,
        sprite_groups,
        sprite_requirements,
        overworld_metadata["forced_group_requirements"],
    )
    state = EnemyShuffleState(
        dungeon_rooms=dungeon_rooms,
        overworld_areas=overworld_areas,
        sprite_groups=sprite_groups,
        sprite_requirements=sprite_requirements,
        room_group_requirements=metadata["room_requirements"],
        overworld_group_requirements=overworld_metadata["forced_group_requirements"],
        shutter_room_ids=metadata["shutter_room_ids"],
        water_room_ids=metadata["water_room_ids"],
        dont_randomize_room_ids=metadata["dont_randomize_room_ids"],
        no_special_enemies_standard_room_ids=metadata["no_special_enemies_standard_room_ids"],
        boss_room_ids=metadata["boss_room_ids"],
        dont_randomize_overworld_area_ids=overworld_metadata["do_not_randomize_area_ids"],
        randomized_dungeon_rooms=randomized_dungeon_rooms,
        randomized_overworld_areas=randomized_overworld_areas,
        combat_model=_get_world_combat_model(world),
        enemy_health_key=_get_world_enemy_health_key(world),
        max_attacks_in_logic=_get_world_max_attacks_in_logic(world),
        killable_thieves=_get_world_killable_thieves(world),
        available_damage_classes=_get_world_available_damage_classes(world),
        hammer_available_for_freeze=True,
    )
    validate_enemy_shuffle_state(state, is_standard_mode=world.options.mode == "standard")
    return state


def _get_world_enemy_health_key(world: "ALTTPWorld") -> str:
    option = getattr(world.options, "enemy_health", "default")
    return str(getattr(option, "current_key", option))


def _get_world_max_attacks_in_logic(world: "ALTTPWorld") -> int:
    option = getattr(world.options, "max_attacks_in_logic", 16)
    return int(getattr(option, "value", option))


def _get_world_killable_thieves(world: "ALTTPWorld") -> bool:
    return bool(getattr(world.options, "killable_thieves", False))


def _get_world_combat_model(world: "ALTTPWorld") -> EnemyCombatModel:
    combat_model = getattr(world, "enemy_combat_model", None)
    if combat_model is not None:
        return combat_model
    if _get_world_killable_thieves(world):
        return with_killable_thief_combat_model()
    return VANILLA_COMBAT_MODEL


def _get_world_available_damage_classes(world: "ALTTPWorld") -> frozenset[int]:
    return frozenset(getattr(world, "enemy_shuffle_available_damage_classes", frozenset(range(16))))


def _get_base_patched_rom_bytes() -> bytes:
    raise RuntimeError("Enemy shuffle base data is bundled; generation should not read a local ALttP ROM.")


def _load_base_dungeon_rooms(metadata: dict[str, object]) -> tuple[DungeonEnemyRoom, ...]:
    rooms = getattr(_load_base_dungeon_rooms, "rooms", None)
    if rooms is None:
        shutter_room_ids = metadata["shutter_room_ids"]
        water_room_ids = metadata["water_room_ids"]
        dont_randomize_room_ids = metadata["dont_randomize_room_ids"]
        no_special_enemies_standard_room_ids = metadata["no_special_enemies_standard_room_ids"]
        room_requirements = metadata["room_requirements"]
        loaded_rooms = []
        for (
            room_id,
            room_header_address,
            sprite_table_address,
            graphics_block_id,
            tag_1,
            tag_2,
            sort_sprites_value,
            sprites,
            all_sprites,
        ) in DUNGEON_ENEMY_ROOMS:
            merged_requirement = _merge_room_requirements(room_id, room_requirements)
            loaded_rooms.append(
                DungeonEnemyRoom(
                    room_id=room_id,
                    room_header_address=room_header_address,
                    sprite_table_address=sprite_table_address,
                    graphics_block_id=graphics_block_id,
                    tag_1=tag_1,
                    tag_2=tag_2,
                    sort_sprites_value=sort_sprites_value,
                    sprites=tuple(DungeonEnemySprite(*sprite) for sprite in sprites),
                    all_sprites=tuple(DungeonEnemySprite(*sprite) for sprite in all_sprites),
                    required_group_id=merged_requirement.group_id,
                    required_subgroup_0=merged_requirement.subgroup_0,
                    required_subgroup_1=merged_requirement.subgroup_1,
                    required_subgroup_2=merged_requirement.subgroup_2,
                    required_subgroup_3=merged_requirement.subgroup_3,
                    is_shutter_room=room_id in shutter_room_ids,
                    is_water_room=room_id in water_room_ids,
                    do_not_randomize=room_id in dont_randomize_room_ids,
                    no_special_enemies_standard=room_id in no_special_enemies_standard_room_ids,
                )
            )
        rooms = tuple(loaded_rooms)
        _load_base_dungeon_rooms.rooms = rooms
    return rooms


def _load_base_sprite_groups() -> tuple[DungeonSpriteGroup, ...]:
    groups = getattr(_load_base_sprite_groups, "groups", None)
    if groups is None:
        groups = tuple(DungeonSpriteGroup(*group) for group in DUNGEON_SPRITE_GROUPS)
        _load_base_sprite_groups.groups = groups
    return tuple(
        DungeonSpriteGroup(
            group.group_id,
            group.dungeon_group_id,
            group.subgroup_0,
            group.subgroup_1,
            group.subgroup_2,
            group.subgroup_3,
        )
        for group in groups
    )


def _load_base_overworld_areas(metadata: dict[str, object]) -> tuple[OverworldEnemyArea, ...]:
    areas = getattr(_load_base_overworld_areas, "areas", None)
    if areas is None:
        do_not_randomize_area_ids = metadata["do_not_randomize_area_ids"]
        loaded_areas = []
        for (
            area_id,
            sprite_table_address,
            graphics_block_address,
            graphics_block_id,
            bush_sprite_id,
            sprites,
        ) in OVERWORLD_ENEMY_AREAS:
            loaded_areas.append(
                OverworldEnemyArea(
                    area_id=area_id,
                    sprite_table_address=sprite_table_address,
                    graphics_block_address=graphics_block_address,
                    graphics_block_id=graphics_block_id,
                    bush_sprite_id=bush_sprite_id,
                    sprites=tuple(OverworldEnemySprite(*sprite) for sprite in sprites),
                    do_not_randomize=area_id in do_not_randomize_area_ids,
                )
            )
        areas = tuple(loaded_areas)
        _load_base_overworld_areas.areas = areas
    return areas


def _read_dungeon_rooms(rom_bytes: bytes, moved_header_bank_address: int, metadata: dict[str, object]) -> list[DungeonEnemyRoom]:
    rooms: list[DungeonEnemyRoom] = []
    room_header_bank = _get_room_header_bank(rom_bytes, moved_header_bank_address)
    dungeon_sprite_metadata = _load_dungeon_sprite_metadata()
    shutter_room_ids = metadata["shutter_room_ids"]
    water_room_ids = metadata["water_room_ids"]
    dont_randomize_room_ids = metadata["dont_randomize_room_ids"]
    no_special_enemies_standard_room_ids = metadata["no_special_enemies_standard_room_ids"]
    room_requirements = metadata["room_requirements"]

    for room_id in range(TOTAL_DUNGEON_ROOMS):
        room_header_address = _read_room_header_address(rom_bytes, room_id, room_header_bank)
        sprite_table_address = _read_room_sprite_table_address(rom_bytes, room_id)
        merged_requirement = _merge_room_requirements(room_id, room_requirements)
        rooms.append(
            DungeonEnemyRoom(
                room_id=room_id,
                room_header_address=room_header_address,
                sprite_table_address=sprite_table_address,
                graphics_block_id=rom_bytes[room_header_address + 3],
                tag_1=rom_bytes[room_header_address + 5],
                tag_2=rom_bytes[room_header_address + 6],
                sort_sprites_value=rom_bytes[sprite_table_address],
                sprites=_read_room_sprites(rom_bytes, room_id, sprite_table_address, dungeon_sprite_metadata),
                all_sprites=_read_all_room_sprites(rom_bytes, sprite_table_address, dungeon_sprite_metadata),
                required_group_id=merged_requirement.group_id,
                required_subgroup_0=merged_requirement.subgroup_0,
                required_subgroup_1=merged_requirement.subgroup_1,
                required_subgroup_2=merged_requirement.subgroup_2,
                required_subgroup_3=merged_requirement.subgroup_3,
                is_shutter_room=room_id in shutter_room_ids,
                is_water_room=room_id in water_room_ids,
                do_not_randomize=room_id in dont_randomize_room_ids,
                no_special_enemies_standard=room_id in no_special_enemies_standard_room_ids,
            )
        )

    return rooms


def _get_room_header_bank(rom_bytes: bytes, moved_header_bank_address: int) -> int:
    if 0 <= moved_header_bank_address < len(rom_bytes):
        moved_header_bank = rom_bytes[moved_header_bank_address]
        if moved_header_bank:
            return moved_header_bank
    return rom_bytes[ROOM_HEADER_BANK_LOCATION]


def _read_sprite_groups(rom_bytes: bytes) -> tuple[DungeonSpriteGroup, ...]:
    groups = []
    for group_id in range(TOTAL_SPRITE_GROUPS):
        groups.append(
            DungeonSpriteGroup(
                group_id=group_id,
                dungeon_group_id=group_id - 0x40,
                subgroup_0=rom_bytes[SPRITE_GROUP_BASE_ADDRESS + (group_id * 4)],
                subgroup_1=rom_bytes[SPRITE_GROUP_BASE_ADDRESS + (group_id * 4) + 1],
                subgroup_2=rom_bytes[SPRITE_GROUP_BASE_ADDRESS + (group_id * 4) + 2],
                subgroup_3=rom_bytes[SPRITE_GROUP_BASE_ADDRESS + (group_id * 4) + 3],
            )
        )
    return tuple(groups)


def _snapshot_sprite_groups(sprite_groups: dict[int, DungeonSpriteGroup]) -> dict[int, tuple[int, int, int, int]]:
    return {
        group_id: (group.subgroup_0, group.subgroup_1, group.subgroup_2, group.subgroup_3)
        for group_id, group in sprite_groups.items()
    }


def _setup_required_dungeon_groups(
    world: "ALTTPWorld",
    sprite_groups: dict[int, DungeonSpriteGroup],
    room_requirements: tuple[RoomGroupRequirement, ...],
) -> None:
    for requirement in room_requirements:
        if requirement.group_id is None:
            continue
        group = sprite_groups.get(requirement.group_id + 0x40)
        if group is None:
            continue
        _apply_required_subgroups(group, requirement)

    merged_room_requirements = {
        room_id: _merge_room_requirements(room_id, room_requirements)
        for requirement in room_requirements
        for room_id in requirement.rooms
    }

    for merged_requirement in merged_room_requirements.values():
        if merged_requirement.group_id is not None:
            continue
        if _has_preserved_group_for_room_requirement(sprite_groups, merged_requirement):
            continue

        possible_groups = [
            group for group in sprite_groups.values()
            if 0 < group.dungeon_group_id < 60
            and (
                not group.preserve_subgroup_0
                or not group.preserve_subgroup_1
                or not group.preserve_subgroup_2
                or not group.preserve_subgroup_3
            )
            and (not merged_requirement.subgroup_0 or not group.preserve_subgroup_0)
            and (not merged_requirement.subgroup_1 or not group.preserve_subgroup_1)
            and (not merged_requirement.subgroup_2 or not group.preserve_subgroup_2)
            and (not merged_requirement.subgroup_3 or not group.preserve_subgroup_3)
        ]
        if not possible_groups:
            continue

        selected_group = world.random.choice(possible_groups)
        _apply_merged_room_requirement(selected_group, merged_requirement)


def _setup_combined_dungeon_room_graphics_groups(
    world: "ALTTPWorld",
    dungeon_rooms: dict[int, DungeonEnemyRoom],
    sprite_groups: dict[int, DungeonSpriteGroup],
    sprite_requirements: tuple[EnemySpriteRequirement, ...],
) -> None:
    for room in dungeon_rooms.values():
        requirement = _build_combined_room_graphics_requirement(sprite_requirements, room)
        if _combined_room_graphics_requirement_is_empty(requirement):
            continue
        if _has_preserved_group_for_combined_room_graphics_requirement(sprite_groups, requirement):
            continue

        possible_groups = [
            group for group in sprite_groups.values()
            if _group_can_accept_combined_room_graphics_requirement(group, requirement)
        ]
        assert possible_groups, f"Enemy shuffle found no reservable dungeon sprite group for room {room.room_id}"
        if not possible_groups:
            continue

        selected_group = world.random.choice(possible_groups)
        _apply_combined_room_graphics_requirement(selected_group, requirement)


def _apply_selected_boss_group_requirements(
    world: "ALTTPWorld",
    sprite_groups: dict[int, DungeonSpriteGroup],
    sprite_requirements: tuple[EnemySpriteRequirement, ...],
) -> None:
    requirement_by_sprite_id = {requirement.sprite_id: requirement for requirement in sprite_requirements}
    for boss_name in _get_selected_boss_names(world):
        boss_group_data = SELECTED_BOSS_GROUP_REQUIREMENTS.get(boss_name)
        if boss_group_data is None:
            continue
        dungeon_group_id, sprite_id = boss_group_data
        group = sprite_groups.get(dungeon_group_id + 0x40)
        requirement = requirement_by_sprite_id.get(sprite_id)
        if group is None or requirement is None:
            continue
        _apply_selected_boss_requirement(group, requirement)


def _get_selected_boss_names(world: "ALTTPWorld") -> tuple[str, ...]:
    dungeons = getattr(world, "dungeons", None)
    if not dungeons:
        return tuple()

    gt_dungeon_name = "Ganons Tower" if world.options.mode != "inverted" else "Inverted Ganons Tower"
    gt_dungeon = dungeons.get(gt_dungeon_name)
    gt_bosses = getattr(gt_dungeon, "bosses", {}) if gt_dungeon is not None else {}

    selected_bosses = [
        dungeons["Eastern Palace"].boss.enemizer_name,
        dungeons["Desert Palace"].boss.enemizer_name,
        dungeons["Tower of Hera"].boss.enemizer_name,
        dungeons["Palace of Darkness"].boss.enemizer_name,
        dungeons["Swamp Palace"].boss.enemizer_name,
        dungeons["Skull Woods"].boss.enemizer_name,
        dungeons["Thieves Town"].boss.enemizer_name,
        dungeons["Ice Palace"].boss.enemizer_name,
        dungeons["Misery Mire"].boss.enemizer_name,
        dungeons["Turtle Rock"].boss.enemizer_name,
    ]
    for gt_slot in ("bottom", "middle", "top"):
        if gt_slot in gt_bosses:
            selected_bosses.append(gt_bosses[gt_slot].enemizer_name)
    return tuple(selected_bosses)


def _apply_selected_boss_requirement(group: DungeonSpriteGroup, requirement: EnemySpriteRequirement) -> None:
    if requirement.subgroup_0:
        group.subgroup_0 = requirement.subgroup_0[0]
        group.preserve_subgroup_0 = True
    if requirement.subgroup_1:
        group.subgroup_1 = requirement.subgroup_1[0]
        group.preserve_subgroup_1 = True
    if requirement.subgroup_2:
        group.subgroup_2 = requirement.subgroup_2[0]
        group.preserve_subgroup_2 = True
    if requirement.subgroup_3:
        group.subgroup_3 = requirement.subgroup_3[0]
        group.preserve_subgroup_3 = True


def _setup_required_overworld_groups(
    sprite_groups: dict[int, DungeonSpriteGroup],
    overworld_group_requirements: tuple[OverworldGroupRequirement, ...],
) -> None:
    for requirement in overworld_group_requirements:
        if requirement.group_id is None:
            continue
        group = sprite_groups.get(requirement.group_id)
        if group is None:
            continue
        if (
            requirement.subgroup_0 is None
            and requirement.subgroup_1 is None
            and requirement.subgroup_2 is None
            and requirement.subgroup_3 is None
        ):
            group.preserve_subgroup_0 = True
            group.preserve_subgroup_1 = True
            group.preserve_subgroup_2 = True
            group.preserve_subgroup_3 = True
            continue
        _apply_required_subgroups(group, requirement)


def _apply_required_subgroups(group: DungeonSpriteGroup, requirement: RoomGroupRequirement | OverworldGroupRequirement) -> None:
    if requirement.subgroup_0 is not None:
        group.subgroup_0 = requirement.subgroup_0
        group.preserve_subgroup_0 = True
    if requirement.subgroup_1 is not None:
        group.subgroup_1 = requirement.subgroup_1
        group.preserve_subgroup_1 = True
    if requirement.subgroup_2 is not None:
        group.subgroup_2 = requirement.subgroup_2
        group.preserve_subgroup_2 = True
    if requirement.subgroup_3 is not None:
        group.subgroup_3 = requirement.subgroup_3
        group.preserve_subgroup_3 = True


def _apply_merged_room_requirement(group: DungeonSpriteGroup, requirement: MergedRoomRequirement) -> None:
    if requirement.subgroup_0:
        group.subgroup_0 = requirement.subgroup_0[0]
        group.preserve_subgroup_0 = True
    if requirement.subgroup_1:
        group.subgroup_1 = requirement.subgroup_1[0]
        group.preserve_subgroup_1 = True
    if requirement.subgroup_2:
        group.subgroup_2 = requirement.subgroup_2[0]
        group.preserve_subgroup_2 = True
    if requirement.subgroup_3:
        group.subgroup_3 = requirement.subgroup_3[0]
        group.preserve_subgroup_3 = True


def _build_combined_room_graphics_requirement(
    sprite_requirements: tuple[EnemySpriteRequirement, ...],
    room: DungeonEnemyRoom,
) -> CombinedRoomGraphicsRequirement:
    group_ids: tuple[int, ...] = tuple()
    subgroup_0 = room.required_subgroup_0
    subgroup_1 = room.required_subgroup_1
    subgroup_2 = room.required_subgroup_2
    subgroup_3 = room.required_subgroup_3

    for requirement in _get_room_do_not_update_alternative_requirements(sprite_requirements, room):
        group_ids = _intersect_allowed_values(group_ids, requirement.group_ids)
        subgroup_0 = _intersect_allowed_values(subgroup_0, requirement.subgroup_0)
        subgroup_1 = _intersect_allowed_values(subgroup_1, requirement.subgroup_1)
        subgroup_2 = _intersect_allowed_values(subgroup_2, requirement.subgroup_2)
        subgroup_3 = _intersect_allowed_values(subgroup_3, requirement.subgroup_3)

    return CombinedRoomGraphicsRequirement(
        dungeon_group_id=room.required_group_id,
        group_ids=group_ids,
        subgroup_0=subgroup_0,
        subgroup_1=subgroup_1,
        subgroup_2=subgroup_2,
        subgroup_3=subgroup_3,
    )


def _get_room_do_not_update_requirements(
    sprite_requirements: tuple[EnemySpriteRequirement, ...],
    room: DungeonEnemyRoom,
) -> tuple[EnemySpriteRequirement, ...]:
    editable_addresses = {sprite.address for sprite in room.sprites}
    constraint_sprites = _get_room_constraint_sprites(room)
    return tuple(
        requirement for requirement in sprite_requirements
        if any(
            sprite.sprite_id == requirement.sprite_id
            and (
                sprite.address not in editable_addresses
                or requirement.do_not_randomize
                or room.room_id in requirement.dont_randomize_rooms
            )
            for sprite in constraint_sprites
        )
        and can_spawn_in_room(requirement, room)
    )


def _get_room_do_not_update_alternative_requirements(
    sprite_requirements: tuple[EnemySpriteRequirement, ...],
    room: DungeonEnemyRoom,
) -> tuple[CombinedRoomGraphicsRequirement, ...]:
    editable_addresses = {sprite.address for sprite in room.sprites}
    sprite_requirements_by_id: dict[int, list[EnemySpriteRequirement]] = {}
    for requirement in sprite_requirements:
        sprite_requirements_by_id.setdefault(requirement.sprite_id, []).append(requirement)

    fixed_sprite_requirements: list[CombinedRoomGraphicsRequirement] = []
    for sprite in _get_room_constraint_sprites(room):
        alternatives = tuple(
            requirement for requirement in sprite_requirements_by_id.get(sprite.sprite_id, ())
            if (
                sprite.address not in editable_addresses
                or requirement.do_not_randomize
                or room.room_id in requirement.dont_randomize_rooms
            )
            and can_spawn_in_room(requirement, room)
        )
        if alternatives:
            fixed_sprite_requirements.append(_merge_alternative_sprite_graphics_requirements(alternatives))

    return tuple(fixed_sprite_requirements)


def _merge_alternative_sprite_graphics_requirements(
    alternatives: tuple[EnemySpriteRequirement, ...],
) -> CombinedRoomGraphicsRequirement:
    return CombinedRoomGraphicsRequirement(
        dungeon_group_id=None,
        group_ids=_union_alternative_allowed_values(tuple(requirement.group_ids for requirement in alternatives)),
        subgroup_0=_union_alternative_allowed_values(tuple(requirement.subgroup_0 for requirement in alternatives)),
        subgroup_1=_union_alternative_allowed_values(tuple(requirement.subgroup_1 for requirement in alternatives)),
        subgroup_2=_union_alternative_allowed_values(tuple(requirement.subgroup_2 for requirement in alternatives)),
        subgroup_3=_union_alternative_allowed_values(tuple(requirement.subgroup_3 for requirement in alternatives)),
    )


def _union_alternative_allowed_values(alternatives: tuple[tuple[int, ...], ...]) -> tuple[int, ...]:
    if any(not values for values in alternatives):
        return tuple()
    result: list[int] = []
    for values in alternatives:
        for value in values:
            if value not in result:
                result.append(value)
    return tuple(result)


def _intersect_allowed_values(current: tuple[int, ...], incoming: tuple[int, ...]) -> tuple[int, ...]:
    if not incoming:
        return current
    if not current:
        return incoming
    incoming_set = set(incoming)
    intersection = tuple(value for value in current if value in incoming_set)
    return intersection or (IMPOSSIBLE_GRAPHICS_VALUE,)


def _combined_room_graphics_requirement_is_empty(requirement: CombinedRoomGraphicsRequirement) -> bool:
    return (
        requirement.dungeon_group_id is None
        and not requirement.group_ids
        and not requirement.subgroup_0
        and not requirement.subgroup_1
        and not requirement.subgroup_2
        and not requirement.subgroup_3
    )


def _has_preserved_group_for_combined_room_graphics_requirement(
    sprite_groups: dict[int, DungeonSpriteGroup],
    requirement: CombinedRoomGraphicsRequirement,
) -> bool:
    return any(
        _group_matches_combined_room_graphics_requirement(group, requirement, require_preserved=True)
        for group in sprite_groups.values()
    )


def _group_can_accept_combined_room_graphics_requirement(
    group: DungeonSpriteGroup,
    requirement: CombinedRoomGraphicsRequirement,
) -> bool:
    return _group_matches_combined_room_graphics_requirement(group, requirement, require_preserved=False)


def _group_matches_combined_room_graphics_requirement(
    group: DungeonSpriteGroup,
    requirement: CombinedRoomGraphicsRequirement,
    *,
    require_preserved: bool,
) -> bool:
    return (
        0 < group.dungeon_group_id < 60
        and (requirement.dungeon_group_id is None or group.dungeon_group_id == requirement.dungeon_group_id)
        and (not requirement.group_ids or group.group_id in requirement.group_ids)
        and _subgroup_can_satisfy_requirement(
            group.subgroup_0, group.preserve_subgroup_0, requirement.subgroup_0, require_preserved
        )
        and _subgroup_can_satisfy_requirement(
            group.subgroup_1, group.preserve_subgroup_1, requirement.subgroup_1, require_preserved
        )
        and _subgroup_can_satisfy_requirement(
            group.subgroup_2, group.preserve_subgroup_2, requirement.subgroup_2, require_preserved
        )
        and _subgroup_can_satisfy_requirement(
            group.subgroup_3, group.preserve_subgroup_3, requirement.subgroup_3, require_preserved
        )
    )


def _subgroup_can_satisfy_requirement(
    value: int,
    preserved: bool,
    allowed_values: tuple[int, ...],
    require_preserved: bool,
) -> bool:
    if not allowed_values:
        return True
    if preserved or require_preserved:
        return preserved and value in allowed_values
    return True


def _apply_combined_room_graphics_requirement(
    group: DungeonSpriteGroup,
    requirement: CombinedRoomGraphicsRequirement,
) -> None:
    if requirement.subgroup_0 and not group.preserve_subgroup_0:
        group.subgroup_0 = requirement.subgroup_0[0]
        group.preserve_subgroup_0 = True
    if requirement.subgroup_1 and not group.preserve_subgroup_1:
        group.subgroup_1 = requirement.subgroup_1[0]
        group.preserve_subgroup_1 = True
    if requirement.subgroup_2 and not group.preserve_subgroup_2:
        group.subgroup_2 = requirement.subgroup_2[0]
        group.preserve_subgroup_2 = True
    if requirement.subgroup_3 and not group.preserve_subgroup_3:
        group.subgroup_3 = requirement.subgroup_3[0]
        group.preserve_subgroup_3 = True


def _has_preserved_group_for_room_requirement(
    sprite_groups: dict[int, DungeonSpriteGroup],
    requirement: MergedRoomRequirement,
) -> bool:
    for group in sprite_groups.values():
        if not (0 < group.dungeon_group_id < 60):
            continue
        if requirement.subgroup_0 and (group.subgroup_0 != requirement.subgroup_0[0] or not group.preserve_subgroup_0):
            continue
        if requirement.subgroup_1 and (group.subgroup_1 != requirement.subgroup_1[0] or not group.preserve_subgroup_1):
            continue
        if requirement.subgroup_2 and (group.subgroup_2 != requirement.subgroup_2[0] or not group.preserve_subgroup_2):
            continue
        if requirement.subgroup_3 and (group.subgroup_3 != requirement.subgroup_3[0] or not group.preserve_subgroup_3):
            continue
        return True
    return False


def _randomize_dungeon_groups(world: "ALTTPWorld", sprite_groups: dict[int, DungeonSpriteGroup]) -> None:
    for group in sprite_groups.values():
        if not (0 < group.dungeon_group_id < 60):
            continue
        if not group.preserve_subgroup_1 and group.dungeon_group_id in GUARD_SUBGROUP_1_DUNGEON_GROUP_IDS:
            group.preserve_subgroup_1 = True
            group.subgroup_1 = world.random.choice((73, 13))
        if not group.preserve_subgroup_0:
            group.subgroup_0 = world.random.choice(POTENTIAL_SUBGROUP_0)
        if not group.preserve_subgroup_1:
            group.subgroup_1 = world.random.choice(POTENTIAL_SUBGROUP_1)
        if not group.preserve_subgroup_2:
            group.subgroup_2 = world.random.choice(POTENTIAL_SUBGROUP_2)
        if not group.preserve_subgroup_3:
            group.subgroup_3 = world.random.choice(POTENTIAL_SUBGROUP_3)


def _restore_skipped_room_sprite_groups(
    world: "ALTTPWorld",
    dungeon_rooms: dict[int, DungeonEnemyRoom],
    sprite_groups: dict[int, DungeonSpriteGroup],
    sprite_requirements: tuple[EnemySpriteRequirement, ...],
    original_sprite_groups: dict[int, tuple[int, int, int, int]],
) -> None:
    state = EnemyShuffleState(
        dungeon_rooms=dungeon_rooms,
        overworld_areas={},
        sprite_groups=sprite_groups,
        sprite_requirements=sprite_requirements,
        room_group_requirements=tuple(),
        overworld_group_requirements=tuple(),
        shutter_room_ids=frozenset(room.room_id for room in dungeon_rooms.values() if room.is_shutter_room),
        water_room_ids=frozenset(room.room_id for room in dungeon_rooms.values() if room.is_water_room),
        dont_randomize_room_ids=frozenset(room.room_id for room in dungeon_rooms.values() if room.do_not_randomize),
        no_special_enemies_standard_room_ids=frozenset(
            room.room_id for room in dungeon_rooms.values() if room.no_special_enemies_standard
        ),
        boss_room_ids=frozenset(),
        dont_randomize_overworld_area_ids=frozenset(),
        randomized_dungeon_rooms={},
        randomized_overworld_areas={},
        combat_model=_get_world_combat_model(world),
        enemy_health_key=_get_world_enemy_health_key(world),
        max_attacks_in_logic=_get_world_max_attacks_in_logic(world),
        killable_thieves=_get_world_killable_thieves(world),
        available_damage_classes=_get_world_available_damage_classes(world),
        hammer_available_for_freeze=True,
    )

    skipped_group_ids = {
        room.graphics_block_id + 0x40
        for room in dungeon_rooms.values()
        if _dungeon_room_skips_enemy_randomization(world, state, room)
    }
    for group_id in skipped_group_ids:
        group = sprite_groups.get(group_id)
        original_group = original_sprite_groups.get(group_id)
        if group is None or original_group is None:
            continue
        group.subgroup_0, group.subgroup_1, group.subgroup_2, group.subgroup_3 = original_group
        group.preserve_subgroup_0 = True
        group.preserve_subgroup_1 = True
        group.preserve_subgroup_2 = True
        group.preserve_subgroup_3 = True


def _restore_original_groups_for_rooms_without_possible_groups(
    world: "ALTTPWorld",
    dungeon_rooms: dict[int, DungeonEnemyRoom],
    sprite_groups: dict[int, DungeonSpriteGroup],
    sprite_requirements: tuple[EnemySpriteRequirement, ...],
    original_sprite_groups: dict[int, tuple[int, int, int, int]],
) -> None:
    state = EnemyShuffleState(
        dungeon_rooms=dungeon_rooms,
        overworld_areas={},
        sprite_groups=sprite_groups,
        sprite_requirements=sprite_requirements,
        room_group_requirements=tuple(),
        overworld_group_requirements=tuple(),
        shutter_room_ids=frozenset(room.room_id for room in dungeon_rooms.values() if room.is_shutter_room),
        water_room_ids=frozenset(room.room_id for room in dungeon_rooms.values() if room.is_water_room),
        dont_randomize_room_ids=frozenset(room.room_id for room in dungeon_rooms.values() if room.do_not_randomize),
        no_special_enemies_standard_room_ids=frozenset(
            room.room_id for room in dungeon_rooms.values() if room.no_special_enemies_standard
        ),
        boss_room_ids=frozenset(),
        dont_randomize_overworld_area_ids=frozenset(),
        randomized_dungeon_rooms={},
        randomized_overworld_areas={},
        combat_model=_get_world_combat_model(world),
        enemy_health_key=_get_world_enemy_health_key(world),
        max_attacks_in_logic=_get_world_max_attacks_in_logic(world),
        killable_thieves=_get_world_killable_thieves(world),
        available_damage_classes=_get_world_available_damage_classes(world),
        hammer_available_for_freeze=True,
    )

    for _ in range(len(dungeon_rooms)):
        changed = False
        for room in dungeon_rooms.values():
            if _dungeon_room_skips_enemy_randomization(world, state, room):
                continue
            if get_possible_dungeon_sprite_groups(state, room):
                continue

            group = sprite_groups.get(room.graphics_block_id + 0x40)
            original_group = original_sprite_groups.get(room.graphics_block_id + 0x40)
            assert group is not None and original_group is not None, (
                f"Enemy shuffle found no restorable original sprite group for room {room.room_id}"
            )
            if group is None or original_group is None:
                continue
            if (group.subgroup_0, group.subgroup_1, group.subgroup_2, group.subgroup_3) == original_group:
                continue
            group.subgroup_0, group.subgroup_1, group.subgroup_2, group.subgroup_3 = original_group
            group.preserve_subgroup_0 = True
            group.preserve_subgroup_1 = True
            group.preserve_subgroup_2 = True
            group.preserve_subgroup_3 = True
            changed = True
        if not changed:
            break

    for room in dungeon_rooms.values():
        if not _dungeon_room_skips_enemy_randomization(world, state, room):
            assert get_possible_dungeon_sprite_groups(state, room), (
                f"Enemy shuffle found no legal dungeon sprite group for room {room.room_id}"
            )


def _randomize_overworld_groups(world: "ALTTPWorld", sprite_groups: dict[int, DungeonSpriteGroup]) -> None:
    for group in sprite_groups.values():
        if not (0 < group.group_id < 0x40):
            continue
        if not group.preserve_subgroup_0:
            group.subgroup_0 = world.random.choice(POTENTIAL_SUBGROUP_0)
        if not group.preserve_subgroup_1:
            group.subgroup_1 = world.random.choice(POTENTIAL_SUBGROUP_1)
        if not group.preserve_subgroup_2:
            group.subgroup_2 = world.random.choice(POTENTIAL_SUBGROUP_2)
        if not group.preserve_subgroup_3:
            group.subgroup_3 = world.random.choice(POTENTIAL_SUBGROUP_3)


def _restore_standard_beginning_overworld_sprite_groups(
    world: "ALTTPWorld",
    sprite_groups: dict[int, DungeonSpriteGroup],
    original_sprite_groups: dict[int, tuple[int, int, int, int]],
) -> None:
    if world.options.mode != "standard":
        return

    for group_id in STANDARD_BEGINNING_OVERWORLD_GROUP_IDS:
        group = sprite_groups.get(group_id)
        original_group = original_sprite_groups.get(group_id)
        if group is None or original_group is None:
            continue
        group.subgroup_0, group.subgroup_1, group.subgroup_2, group.subgroup_3 = original_group
        group.preserve_subgroup_0 = True
        group.preserve_subgroup_1 = True
        group.preserve_subgroup_2 = True
        group.preserve_subgroup_3 = True


def _read_room_header_address(rom_bytes: bytes, room_id: int, room_header_bank: int) -> int:
    pointer_address = DUNGEON_HEADER_POINTER_TABLE_BASE + (room_id * 2)
    snes_address = (
        rom_bytes[pointer_address]
        | (rom_bytes[pointer_address + 1] << 8)
        | (room_header_bank << 16)
    )
    return snes_to_pc(snes_address)


def _read_room_sprite_table_address(rom_bytes: bytes, room_id: int) -> int:
    pointer_address = DUNGEON_SPRITE_POINTER_TABLE_BASE + (room_id * 2)
    snes_address = (
        rom_bytes[pointer_address]
        | (rom_bytes[pointer_address + 1] << 8)
        | (0x09 << 16)
    )
    return snes_to_pc(snes_address)


def _read_overworld_areas(
    rom_bytes: bytes,
    bush_spawn_table_address: int,
    metadata: dict[str, object],
) -> list[OverworldEnemyArea]:
    areas: list[OverworldEnemyArea] = []
    do_not_randomize_area_ids = metadata["do_not_randomize_area_ids"]

    for area_id in metadata["area_ids"]:
        sprite_table_address = _read_overworld_sprite_table_address(rom_bytes, area_id)
        graphics_block_address = _get_overworld_graphics_block_address(area_id)
        areas.append(
            OverworldEnemyArea(
                area_id=area_id,
                sprite_table_address=sprite_table_address,
                graphics_block_address=graphics_block_address,
                graphics_block_id=rom_bytes[graphics_block_address],
                bush_sprite_id=rom_bytes[bush_spawn_table_address + area_id],
                sprites=_read_overworld_sprites(rom_bytes, sprite_table_address),
                do_not_randomize=area_id in do_not_randomize_area_ids,
            )
        )

    return areas


def _read_overworld_sprite_table_address(rom_bytes: bytes, area_id: int) -> int:
    pointer_address = OVERWORLD_SPRITE_POINTER_TABLE_BASE + (area_id * 2)
    snes_address = (
        rom_bytes[pointer_address]
        | (rom_bytes[pointer_address + 1] << 8)
        | (0x09 << 16)
    )
    return snes_to_pc(snes_address)


def _get_overworld_graphics_block_address(area_id: int) -> int:
    if area_id in {0x80, 0x81}:
        return 0x16576 + (area_id - 0x80)
    if area_id in {0x110, 0x111}:
        return 0x16576 + (area_id - 0x110)

    address = OVERWORLD_AREA_GRAPHICS_BLOCK_BASE + area_id
    if 0x40 <= area_id < 0x80:
        address += 0x40
    if 0x90 <= area_id < 0x110:
        address -= 0x50
    return address


def _read_overworld_sprites(rom_bytes: bytes, sprite_table_address: int) -> tuple[OverworldEnemySprite, ...]:
    sprites: list[OverworldEnemySprite] = []
    index = sprite_table_address
    while rom_bytes[index] != 0xFF:
        sprites.append(
            OverworldEnemySprite(
                address=index,
                y_coord=rom_bytes[index],
                x_coord=rom_bytes[index + 1],
                sprite_id=rom_bytes[index + 2],
            )
        )
        index += 3
    return tuple(sprites)


def _read_room_sprites(
    rom_bytes: bytes,
    room_id: int,
    sprite_table_address: int,
    dungeon_sprite_metadata: dict[str, object],
) -> tuple[DungeonEnemySprite, ...]:
    keyed_sprite_id_addresses = dungeon_sprite_metadata["keyed_sprite_id_addresses"]
    editable_sprite_id_addresses = dungeon_sprite_metadata["room_sprite_id_addresses"].get(room_id)

    if editable_sprite_id_addresses is None:
        sprite_addresses = _read_room_sprite_addresses(rom_bytes, sprite_table_address)
    else:
        sprite_addresses = [sprite_id_address - 2 for sprite_id_address in editable_sprite_id_addresses]

    return _read_room_sprites_from_addresses(rom_bytes, sprite_addresses, keyed_sprite_id_addresses)


def _read_all_room_sprites(
    rom_bytes: bytes,
    sprite_table_address: int,
    dungeon_sprite_metadata: dict[str, object],
) -> tuple[DungeonEnemySprite, ...]:
    return _read_room_sprites_from_addresses(
        rom_bytes,
        _read_room_sprite_addresses(rom_bytes, sprite_table_address),
        dungeon_sprite_metadata["keyed_sprite_id_addresses"],
    )


def _read_room_sprite_addresses(rom_bytes: bytes, sprite_table_address: int) -> list[int]:
    sprite_addresses = []
    index = sprite_table_address + 1  # byte 0 is sort-sprites metadata
    while rom_bytes[index] != 0xFF:
        sprite_addresses.append(index)
        index += 3
    return sprite_addresses


def _read_room_sprites_from_addresses(
    rom_bytes: bytes,
    sprite_addresses: list[int],
    keyed_sprite_id_addresses: frozenset[int],
) -> tuple[DungeonEnemySprite, ...]:
    sprites: list[DungeonEnemySprite] = []
    seen_sprite_addresses: set[int] = set()
    unique_sprite_addresses = []
    for address in sprite_addresses:
        if address in seen_sprite_addresses:
            continue
        seen_sprite_addresses.add(address)
        unique_sprite_addresses.append(address)

    for index in unique_sprite_addresses:
        byte_0 = rom_bytes[index]
        byte_1 = rom_bytes[index + 1]
        sprite_id = rom_bytes[index + 2]
        is_overlord = (byte_1 & SPRITE_OVERLORD_MASK) == SPRITE_OVERLORD_MASK and (
            (byte_0 & SPRITE_SUBTYPE_BYTE_0_MASK) != SPRITE_SUBTYPE_BYTE_0_MASK
        )
        if not is_overlord and sprite_id not in {KEY_SPRITE_ID, WALLMASTER_SPRITE_ID}:
            byte_0 &= 0x9F
            byte_1 &= SPRITE_OVERLORD_REMOVE_MASK
        has_key = (index + 2) in keyed_sprite_id_addresses
        sprites.append(
            DungeonEnemySprite(
                address=index,
                byte_0=byte_0,
                byte_1=byte_1,
                sprite_id=sprite_id + (0x100 if is_overlord else 0),
                is_overlord=is_overlord,
                has_key=has_key,
            )
        )

    return tuple(sprites)


def _get_enemizer_symbol(symbol_name: str) -> int:
    return snes_to_pc(ENEMIZER_SYMBOLS[symbol_name])


def _load_enemy_room_metadata() -> dict[str, object]:
    return {
        "shutter_room_ids": SHUTTER_ROOM_IDS,
        "water_room_ids": WATER_ROOM_IDS,
        "dont_randomize_room_ids": DONT_RANDOMIZE_ROOM_IDS,
        "no_special_enemies_standard_room_ids": NO_SPECIAL_ENEMIES_STANDARD_ROOM_IDS,
        "boss_room_ids": BOSS_ROOM_IDS,
        "room_requirements": tuple(
            RoomGroupRequirement(
                group_id=requirement.group_id,
                subgroup_0=requirement.subgroup_0,
                subgroup_1=requirement.subgroup_1,
                subgroup_2=requirement.subgroup_2,
                subgroup_3=requirement.subgroup_3,
                rooms=requirement.rooms,
            )
            for requirement in ROOM_GROUP_REQUIREMENTS
        ),
    }


def _load_dungeon_sprite_metadata() -> dict[str, object]:
    return {
        "room_sprite_id_addresses": {
            room.room_id: room.sprite_id_addresses
            for room in DUNGEON_SPRITE_ADDRESSES
        },
        "keyed_sprite_id_addresses": KEYED_SPRITE_ID_ADDRESSES,
    }


def _load_enemy_sprite_requirements() -> tuple[EnemySpriteRequirement, ...]:
    return tuple(
        EnemySpriteRequirement(
            sprite_name=entry.sprite_name,
            sprite_id=entry.sprite_id,
            boss=entry.boss,
            overlord=entry.overlord,
            do_not_randomize=entry.do_not_randomize,
            killable=entry.killable,
            counts_for_enemy_clear=_entry_counts_for_enemy_clear(entry),
            npc=entry.npc,
            never_use_dungeon=entry.never_use_dungeon,
            never_use_overworld=entry.never_use_overworld,
            cannot_have_key=entry.cannot_have_key,
            is_object=entry.is_object,
            absorbable=entry.absorbable,
            is_water_sprite=entry.is_water_sprite,
            is_enemy_sprite=entry.is_enemy_sprite,
            group_ids=entry.group_ids,
            subgroup_0=entry.subgroup_0,
            subgroup_1=entry.subgroup_1,
            subgroup_2=entry.subgroup_2,
            subgroup_3=entry.subgroup_3,
            parameters=entry.parameters,
            special_glitched=entry.special_glitched,
            excluded_rooms=entry.excluded_rooms,
            dont_randomize_rooms=entry.dont_randomize_rooms,
            spawnable_rooms=entry.spawnable_rooms,
            combat_reference_id=entry.combat_reference_id,
        )
        for entry in ENEMY_SPRITE_REQUIREMENTS
    )


def _entry_counts_for_enemy_clear(entry) -> bool:
    if entry.counts_for_enemy_clear is not None:
        return entry.counts_for_enemy_clear
    return (
        entry.is_enemy_sprite
        and not entry.boss
        and not entry.overlord
        and not entry.npc
        and not entry.is_object
        and not entry.absorbable
        and not entry.never_use_dungeon
        and entry.sprite_id not in ROOM_CLEAR_IGNORED_SPRITE_IDS
    )


def get_room_name(room_id: int) -> Optional[str]:
    return _load_room_names().get(room_id)


def get_room_id(room_name: str) -> Optional[int]:
    return _load_room_name_to_id().get(room_name)


def get_effective_dungeon_room_sprite_requirements(world: "ALTTPWorld", room_id: int) -> tuple[EnemySpriteRequirement, ...]:
    return tuple(
        enemy.requirement
        for enemy in get_effective_dungeon_room_enemies(world, room_id)
    )


def get_effective_dungeon_room_enemies(world: "ALTTPWorld", room_id: int) -> tuple[EffectiveDungeonEnemySprite, ...]:
    sprite_requirements = _get_sprite_requirement_lookup()
    room_sprites = _get_effective_dungeon_room_sprites(world, room_id)
    return tuple(
        EffectiveDungeonEnemySprite(
            requirement=sprite_requirements[sprite.sprite_id],
            has_key=sprite.has_key,
            x_coord_pixels=sprite.x_coord_pixels,
            y_coord_pixels=sprite.y_coord_pixels,
        )
        for sprite in room_sprites
        if sprite.sprite_id in sprite_requirements
        and sprite_requirements[sprite.sprite_id].is_enemy_sprite
        and not sprite_requirements[sprite.sprite_id].npc
        and not sprite_requirements[sprite.sprite_id].is_object
    )


def _get_effective_dungeon_room_sprites(
    world: "ALTTPWorld",
    room_id: int,
) -> tuple[DefaultDungeonEnemySprite | RandomizedDungeonEnemySprite, ...]:
    if world.options.enemy_shuffle and world.enemy_shuffle_state is not None:
        randomized_room = world.enemy_shuffle_state.randomized_dungeon_rooms.get(room_id)
        if randomized_room is not None:
            return randomized_room.sprites

    room_sprites = _load_default_dungeon_room_sprites().get(room_id)
    if room_sprites is None:
        raise KeyError(f"Unknown ALTTP room id {room_id}")
    return room_sprites


def _load_default_dungeon_room_sprites() -> dict[int, tuple[DefaultDungeonEnemySprite, ...]]:
    room_sprites = getattr(_load_default_dungeon_room_sprites, "room_sprites", None)
    if room_sprites is None:
        room_sprites = {
            room.room_id: tuple(
                DefaultDungeonEnemySprite(
                    sprite_id=sprite.sprite_id,
                    has_key=sprite.has_key,
                    x_coord_pixels=sprite.x_coord_pixels,
                    y_coord_pixels=sprite.y_coord_pixels,
                )
                for sprite in room.sprites
            )
            for room in DEFAULT_DUNGEON_ROOM_ENEMIES
        }
        _load_default_dungeon_room_sprites.room_sprites = room_sprites
    return room_sprites


def _load_room_names() -> dict[int, str]:
    room_names = getattr(_load_room_names, "room_names", None)
    if room_names is None:
        room_names = {
            room_id: room_name
            for room_name, room_id in ROOM_NAME_TO_ID.items()
        }
        _load_room_names.room_names = room_names
    return room_names


def _load_room_name_to_id() -> dict[str, int]:
    room_name_to_id = getattr(_load_room_name_to_id, "room_name_to_id", None)
    if room_name_to_id is None:
        room_name_to_id = {
            room_name: int(room_id)
            for room_name, room_id in ROOM_NAME_TO_ID.items()
        }
        _load_room_name_to_id.room_name_to_id = room_name_to_id
    return room_name_to_id


def _get_sprite_requirement_lookup() -> dict[int, EnemySpriteRequirement]:
    requirement_lookup = getattr(_get_sprite_requirement_lookup, "requirement_lookup", None)
    if requirement_lookup is None:
        requirement_lookup = {
            requirement.sprite_id: requirement
            for requirement in _load_enemy_sprite_requirements()
        }
        _get_sprite_requirement_lookup.requirement_lookup = requirement_lookup
    return requirement_lookup


def _load_overworld_enemy_metadata() -> dict[str, object]:
    return {
        "area_ids": AREA_IDS,
        "do_not_randomize_area_ids": DO_NOT_RANDOMIZE_AREA_IDS,
        "forced_group_requirements": tuple(
            OverworldGroupRequirement(
                group_id=requirement.group_id,
                subgroup_0=requirement.subgroup_0,
                subgroup_1=requirement.subgroup_1,
                subgroup_2=requirement.subgroup_2,
                subgroup_3=requirement.subgroup_3,
                areas=requirement.areas,
            )
            for requirement in FORCED_GROUP_REQUIREMENTS
        ),
    }


@dataclass(frozen=True)
class MergedRoomRequirement:
    group_id: Optional[int]
    subgroup_0: tuple[int, ...]
    subgroup_1: tuple[int, ...]
    subgroup_2: tuple[int, ...]
    subgroup_3: tuple[int, ...]


@dataclass(frozen=True)
class CombinedRoomGraphicsRequirement:
    dungeon_group_id: Optional[int]
    group_ids: tuple[int, ...]
    subgroup_0: tuple[int, ...]
    subgroup_1: tuple[int, ...]
    subgroup_2: tuple[int, ...]
    subgroup_3: tuple[int, ...]


def _merge_room_requirements(room_id: int, room_requirements: tuple[RoomGroupRequirement, ...]) -> MergedRoomRequirement:
    group_id: Optional[int] = None
    subgroup_0: list[int] = []
    subgroup_1: list[int] = []
    subgroup_2: list[int] = []
    subgroup_3: list[int] = []

    for requirement in room_requirements:
        if room_id not in requirement.rooms:
            continue
        if requirement.group_id is not None:
            group_id = requirement.group_id
        if requirement.subgroup_0 is not None:
            subgroup_0.append(requirement.subgroup_0)
        if requirement.subgroup_1 is not None:
            subgroup_1.append(requirement.subgroup_1)
        if requirement.subgroup_2 is not None:
            subgroup_2.append(requirement.subgroup_2)
        if requirement.subgroup_3 is not None:
            subgroup_3.append(requirement.subgroup_3)

    return MergedRoomRequirement(
        group_id=group_id,
        subgroup_0=tuple(subgroup_0),
        subgroup_1=tuple(subgroup_1),
        subgroup_2=tuple(subgroup_2),
        subgroup_3=tuple(subgroup_3),
    )


def get_room_do_not_update_requirements(state: EnemyShuffleState, room: DungeonEnemyRoom) -> tuple[EnemySpriteRequirement, ...]:
    return _get_room_do_not_update_requirements(state.sprite_requirements, room)


def _get_room_constraint_sprites(room: DungeonEnemyRoom) -> tuple[DungeonEnemySprite, ...]:
    return room.all_sprites or room.sprites


def get_possible_dungeon_sprite_groups(state: EnemyShuffleState, room: DungeonEnemyRoom) -> tuple[DungeonSpriteGroup, ...]:
    do_not_update = _get_room_do_not_update_alternative_requirements(state.sprite_requirements, room)
    usable_groups = tuple(
        group for group in state.sprite_groups.values()
        if 0 < group.dungeon_group_id < 60
        and _get_possible_enemy_requirements_for_group(state, room, group)
    )
    needs_key = any(sprite.has_key for sprite in room.sprites)
    needs_killable = room.is_shutter_room
    needs_water = room.is_water_room
    needs_killable_key = needs_key and needs_killable
    room_requirements = _get_requirements_for_usable_dungeon_enemies(state)
    water_requirements = tuple(requirement for requirement in room_requirements if requirement.is_water_sprite)
    if (
        not needs_key and not needs_killable and not needs_water
        and not do_not_update
        and room.required_group_id is None
        and not room.required_subgroup_0
        and not room.required_subgroup_1
        and not room.required_subgroup_2
        and not room.required_subgroup_3
    ):
        return _get_unconstrained_possible_dungeon_sprite_groups(usable_groups, room_requirements, water_requirements)

    return tuple(
        group for group in usable_groups
        if (
            (not do_not_update or _group_matches_fixed_sprite_graphics_requirements(group, do_not_update))
            and _group_matches_room_requirement(group, room)
            and (
                lambda possible_requirements: (
                    (not needs_killable or any(
                        _can_be_shutter_room_clear_enemy(state, requirement)
                        for requirement in _filter_requirements_for_room_water_state(room, possible_requirements)
                    ))
                    and (not needs_key or any(
                        _can_be_key_drop_enemy(state, requirement)
                        for requirement in _filter_requirements_for_room_water_state(room, possible_requirements)
                    ))
                    and (not needs_killable_key or any(
                        _can_be_key_drop_enemy(state, requirement)
                        and _can_be_shutter_room_clear_enemy(state, requirement)
                        for requirement in _filter_requirements_for_room_water_state(room, possible_requirements)
                    ))
                    and (not needs_water or any(
                        requirement.is_water_sprite
                        for requirement in _filter_requirements_for_room_water_state(room, possible_requirements)
                    ))
                )
            )(_get_possible_enemy_requirements_for_group(state, room, group))
        )
    )


def _group_matches_fixed_sprite_graphics_requirements(
    group: DungeonSpriteGroup,
    requirements: tuple[CombinedRoomGraphicsRequirement, ...],
) -> bool:
    return all(_group_matches_fixed_sprite_graphics_requirement(group, requirement) for requirement in requirements)


def _group_matches_fixed_sprite_graphics_requirement(
    group: DungeonSpriteGroup,
    requirement: CombinedRoomGraphicsRequirement,
) -> bool:
    return (
        (requirement.dungeon_group_id is None or group.dungeon_group_id == requirement.dungeon_group_id)
        and (not requirement.group_ids or group.group_id in requirement.group_ids)
        and (not requirement.subgroup_0 or group.subgroup_0 in requirement.subgroup_0)
        and (not requirement.subgroup_1 or group.subgroup_1 in requirement.subgroup_1)
        and (not requirement.subgroup_2 or group.subgroup_2 in requirement.subgroup_2)
        and (not requirement.subgroup_3 or group.subgroup_3 in requirement.subgroup_3)
    )


def can_spawn_in_room(requirement: EnemySpriteRequirement, room: DungeonEnemyRoom) -> bool:
    return (
        room.room_id not in requirement.excluded_rooms
        and (not requirement.spawnable_rooms or room.room_id in requirement.spawnable_rooms)
        and (requirement.sprite_id != WALLMASTER_SPRITE_ID or room.room_id < 0x100)
    )


def _get_requirements_for_usable_dungeon_enemies(state: EnemyShuffleState) -> tuple[EnemySpriteRequirement, ...]:
    return tuple(
        requirement for requirement in state.sprite_requirements
        if not requirement.npc
        and requirement.is_enemy_sprite
        and not requirement.boss
        and not requirement.overlord
        and not requirement.is_object
        and not requirement.absorbable
        and not requirement.never_use_dungeon
    )


def _get_requirements_for_usable_overworld_enemies(state: EnemyShuffleState) -> tuple[EnemySpriteRequirement, ...]:
    return tuple(
        requirement for requirement in state.sprite_requirements
        if not requirement.npc
        and requirement.is_enemy_sprite
        and not requirement.boss
        and not requirement.overlord
        and not requirement.is_object
        and not requirement.absorbable
        and not requirement.never_use_overworld
    )


def _filter_requirements_for_room_water_state(
    room: DungeonEnemyRoom,
    requirements: tuple[EnemySpriteRequirement, ...],
) -> tuple[EnemySpriteRequirement, ...]:
    if room.is_water_room:
        return tuple(requirement for requirement in requirements if requirement.is_water_sprite)
    return tuple(requirement for requirement in requirements if not requirement.is_water_sprite)


def _is_effectively_killable(requirement: EnemySpriteRequirement) -> bool:
    return requirement.killable


def _damage_class_is_fairy_transform(
    combat_reference_id: int,
    damage_class: int,
    combat_model: EnemyCombatModel,
) -> bool:
    return get_damage_effect(combat_reference_id, damage_class, combat_model) == FAIRY_TRANSFORM_EFFECT


def _has_yellow_slime_follow_up_for_key_drop(state: EnemyShuffleState, source_combat_reference_id: int) -> bool:
    candidate_damage_classes = set(get_killing_damage_classes(
        YELLOW_SLIME_SPRITE_ID,
        state.combat_model,
        include_freeze_hammer=state.hammer_available_for_freeze,
    ))
    candidate_damage_classes &= set(get_progression_kill_damage_classes(YELLOW_SLIME_SPRITE_ID))
    candidate_damage_classes &= state.available_damage_classes
    follow_up_override = get_yellow_slime_follow_up_delivery_override(source_combat_reference_id)
    if follow_up_override is not None:
        candidate_damage_classes &= _get_deliverable_damage_classes(follow_up_override)
    return any(
        _damage_class_kills_within_enemy_shuffle_logic(state, YELLOW_SLIME_SPRITE_ID, damage_class)
        for damage_class in candidate_damage_classes
    )


def _can_be_key_drop_enemy(state: EnemyShuffleState, requirement: EnemySpriteRequirement) -> bool:
    if requirement.cannot_have_key or requirement.sprite_id == STAL_SPRITE_ID:
        return False

    combat_reference_id = _get_combat_reference_id(requirement, state.combat_model)
    if combat_reference_id is None:
        return False
    if not _is_effectively_killable(requirement):
        return False

    if requirement.sprite_name in KEY_DROP_INCINERATION_REQUIRED_SPRITE_NAMES:
        candidate_damage_classes = set(get_incinerating_damage_classes(combat_reference_id, state.combat_model))
    else:
        delivery_override = DIRECT_KILL_DELIVERY_OVERRIDES.get(requirement.sprite_name)
        if delivery_override is None:
            candidate_damage_classes = set(
                get_killing_damage_classes(
                    combat_reference_id,
                    state.combat_model,
                    include_freeze_hammer=state.hammer_available_for_freeze,
                )
            )
            candidate_damage_classes |= set(get_blob_transform_damage_classes(combat_reference_id, state.combat_model))
        else:
            candidate_damage_classes = _get_deliverable_damage_classes(delivery_override)
            candidate_damage_classes |= (
                set(get_blob_transform_damage_classes(combat_reference_id, state.combat_model))
                & _get_deliverable_damage_classes(delivery_override)
            )
    candidate_damage_classes &= set(get_progression_kill_damage_classes(combat_reference_id))
    candidate_damage_classes &= state.available_damage_classes
    candidate_damage_classes = {
        damage_class for damage_class in candidate_damage_classes
        if not _damage_class_is_fairy_transform(combat_reference_id, damage_class, state.combat_model)
    }

    return any(
        (
            get_damage_effect(combat_reference_id, damage_class, state.combat_model) == BLOB_TRANSFORM_EFFECT
            and _has_yellow_slime_follow_up_for_key_drop(state, combat_reference_id)
        )
        or _damage_class_kills_within_enemy_shuffle_logic(state, combat_reference_id, damage_class)
        for damage_class in candidate_damage_classes
    )


def _can_be_shutter_room_clear_enemy(state: EnemyShuffleState, requirement: EnemySpriteRequirement) -> bool:
    if not requirement.counts_for_enemy_clear:
        return False
    if not _is_effectively_killable(requirement) or requirement.sprite_id == STAL_SPRITE_ID:
        return False

    combat_reference_id = _get_combat_reference_id(requirement, state.combat_model)
    if combat_reference_id is None:
        return False

    delivery_override = DIRECT_KILL_DELIVERY_OVERRIDES.get(requirement.sprite_name)
    if delivery_override is None:
        candidate_damage_classes = set(
            get_killing_damage_classes(
                combat_reference_id,
                state.combat_model,
                include_freeze_hammer=state.hammer_available_for_freeze,
            )
        )
    else:
        candidate_damage_classes = _get_deliverable_damage_classes(delivery_override)
    candidate_damage_classes &= set(get_progression_kill_damage_classes(combat_reference_id))
    candidate_damage_classes &= state.available_damage_classes

    return any(
        _damage_class_kills_within_enemy_shuffle_logic(state, combat_reference_id, damage_class)
        for damage_class in candidate_damage_classes
    )


def _is_enemy_clear_dealbreaker(state: EnemyShuffleState, requirement: EnemySpriteRequirement) -> bool:
    return requirement.counts_for_enemy_clear and not _can_be_shutter_room_clear_enemy(state, requirement)


def _is_safe_for_enemy_clear_room(state: EnemyShuffleState, requirement: EnemySpriteRequirement) -> bool:
    return not _is_enemy_clear_dealbreaker(state, requirement)


def _damage_class_kills_within_enemy_shuffle_logic(
    state: EnemyShuffleState,
    combat_reference_id: int,
    damage_class: int,
) -> bool:
    hit_count = get_hits_to_kill(
        combat_reference_id,
        damage_class,
        state.enemy_health_key,
        killable_thieves=state.killable_thieves,
        combat_model=state.combat_model,
        allow_frozen_hammer_kill=state.hammer_available_for_freeze,
    )
    return hit_count is not None and hit_count <= state.max_attacks_in_logic


def _get_requirement_for_sprite_id(
    state: EnemyShuffleState,
    sprite_id: int,
) -> EnemySpriteRequirement | None:
    for requirement in state.sprite_requirements:
        if requirement.sprite_id == sprite_id:
            return requirement
    return None


def _get_combat_reference_id(requirement: EnemySpriteRequirement, combat_model: EnemyCombatModel) -> Optional[int]:
    combat_reference_id = requirement.combat_reference_id
    if combat_reference_id is None:
        combat_reference_id = requirement.sprite_id
    if 0 <= combat_reference_id < len(combat_model.sprite_damage_subclasses):
        return combat_reference_id
    return None


def _get_deliverable_damage_classes(delivery_override) -> set[int]:
    damage_classes: set[int] = set()
    for item_name in delivery_override.items:
        damage_classes.update(KEY_DROP_DELIVERY_DAMAGE_CLASSES_BY_ITEM.get(item_name, tuple()))
    for ability_name in delivery_override.abilities:
        damage_classes.update(KEY_DROP_DELIVERY_DAMAGE_CLASSES_BY_ABILITY.get(ability_name, tuple()))
    return damage_classes


def _get_unconstrained_possible_dungeon_sprite_groups(
    usable_groups: tuple[DungeonSpriteGroup, ...],
    room_requirements: tuple[EnemySpriteRequirement, ...],
    water_requirements: tuple[EnemySpriteRequirement, ...],
) -> tuple[DungeonSpriteGroup, ...]:
    water_subgroup_3 = set(_flatten_requirement_values(water_requirements, "subgroup_3"))
    included_group_ids = set(_flatten_requirement_values(room_requirements, "group_ids"))
    included_subgroup_0 = set(_flatten_requirement_values(room_requirements, "subgroup_0"))
    included_subgroup_1 = set(_flatten_requirement_values(room_requirements, "subgroup_1"))
    included_subgroup_2 = set(_flatten_requirement_values(room_requirements, "subgroup_2"))
    included_subgroup_3 = {
        subgroup for subgroup in _flatten_requirement_values(room_requirements, "subgroup_3")
        if subgroup not in water_subgroup_3 and subgroup not in {54, 80}
    }

    return tuple(
        group for group in usable_groups
        if group.group_id in included_group_ids
        or group.subgroup_0 in included_subgroup_0
        or group.subgroup_1 in included_subgroup_1
        or group.subgroup_2 in included_subgroup_2
        or group.subgroup_3 in included_subgroup_3
    )


def _build_requirement_group_matcher(requirements: tuple[EnemySpriteRequirement, ...]):
    allowed_group_ids = set(_flatten_requirement_values(requirements, "group_ids"))
    allowed_subgroup_0 = set(_flatten_requirement_values(requirements, "subgroup_0"))
    allowed_subgroup_1 = set(_flatten_requirement_values(requirements, "subgroup_1"))
    allowed_subgroup_2 = set(_flatten_requirement_values(requirements, "subgroup_2"))
    allowed_subgroup_3 = set(_flatten_requirement_values(requirements, "subgroup_3"))

    def matches(group: DungeonSpriteGroup) -> bool:
        return (
            not allowed_group_ids or group.group_id in allowed_group_ids
        ) and (
            not allowed_subgroup_0 or group.subgroup_0 in allowed_subgroup_0
        ) and (
            not allowed_subgroup_1 or group.subgroup_1 in allowed_subgroup_1
        ) and (
            not allowed_subgroup_2 or group.subgroup_2 in allowed_subgroup_2
        ) and (
            not allowed_subgroup_3 or group.subgroup_3 in allowed_subgroup_3
        )

    return matches


def _build_overworld_requirement_group_matcher(requirements: tuple[EnemySpriteRequirement, ...]):
    allowed_group_ids = set(_flatten_requirement_values(requirements, "group_ids"))
    allowed_subgroup_0 = set(_flatten_requirement_values(requirements, "subgroup_0"))
    allowed_subgroup_1 = set(_flatten_requirement_values(requirements, "subgroup_1"))
    allowed_subgroup_2 = set(_flatten_requirement_values(requirements, "subgroup_2"))
    allowed_subgroup_3 = set(_flatten_requirement_values(requirements, "subgroup_3"))

    def matches(group: DungeonSpriteGroup) -> bool:
        return (
            not allowed_group_ids or group.group_id in allowed_group_ids
        ) and (
            not allowed_subgroup_0 or group.subgroup_0 in allowed_subgroup_0
        ) and (
            not allowed_subgroup_1 or group.subgroup_1 in allowed_subgroup_1
        ) and (
            not allowed_subgroup_2 or group.subgroup_2 in allowed_subgroup_2
        ) and (
            not allowed_subgroup_3 or group.subgroup_3 in allowed_subgroup_3
        )

    return matches


def _build_requirement_group_presence_matcher(requirements: tuple[EnemySpriteRequirement, ...]):
    allowed_group_ids = set(_flatten_requirement_values(requirements, "group_ids"))
    allowed_subgroup_0 = set(_flatten_requirement_values(requirements, "subgroup_0"))
    allowed_subgroup_1 = set(_flatten_requirement_values(requirements, "subgroup_1"))
    allowed_subgroup_2 = set(_flatten_requirement_values(requirements, "subgroup_2"))
    allowed_subgroup_3 = set(_flatten_requirement_values(requirements, "subgroup_3"))

    def matches(group: DungeonSpriteGroup) -> bool:
        return (
            group.group_id in allowed_group_ids
            or group.subgroup_0 in allowed_subgroup_0
            or group.subgroup_1 in allowed_subgroup_1
            or group.subgroup_2 in allowed_subgroup_2
            or group.subgroup_3 in allowed_subgroup_3
        )

    return matches


def _flatten_requirement_values(requirements: tuple[EnemySpriteRequirement, ...], attribute: str) -> tuple[int, ...]:
    return tuple(
        value
        for requirement in requirements
        for value in getattr(requirement, attribute)
    )


def _group_matches_room_requirement(group: DungeonSpriteGroup, room: DungeonEnemyRoom) -> bool:
    return (
        (room.required_group_id is None or room.required_group_id == group.dungeon_group_id)
        and (not room.required_subgroup_0 or group.subgroup_0 in room.required_subgroup_0)
        and (not room.required_subgroup_1 or group.subgroup_1 in room.required_subgroup_1)
        and (not room.required_subgroup_2 or group.subgroup_2 in room.required_subgroup_2)
        and (not room.required_subgroup_3 or group.subgroup_3 in room.required_subgroup_3)
    )


def get_overworld_do_not_update_requirements(
    state: EnemyShuffleState,
    area: OverworldEnemyArea,
) -> tuple[EnemySpriteRequirement, ...]:
    area_sprite_ids = {sprite.sprite_id for sprite in area.sprites}
    return tuple(
        requirement for requirement in state.sprite_requirements
        if requirement.do_not_randomize and requirement.sprite_id in area_sprite_ids
    )


def get_possible_overworld_sprite_groups(
    state: EnemyShuffleState,
    area: OverworldEnemyArea,
) -> tuple[DungeonSpriteGroup, ...]:
    usable_groups = tuple(
        group for group in state.sprite_groups.values()
        if 0 < group.group_id < 0x40
        and _get_possible_enemy_requirements_for_overworld_group(state, group)
    )
    do_not_update = get_overworld_do_not_update_requirements(state, area)
    if not do_not_update:
        return usable_groups

    do_not_update_matcher = _build_overworld_requirement_group_matcher(do_not_update)
    return tuple(group for group in usable_groups if do_not_update_matcher(group))


def _get_possible_enemy_requirements_for_group(
    state: EnemyShuffleState,
    room: DungeonEnemyRoom,
    group: DungeonSpriteGroup,
) -> tuple[EnemySpriteRequirement, ...]:
    dungeon_requirements = _get_requirements_for_usable_dungeon_enemies(state)
    return tuple(
        requirement for requirement in dungeon_requirements
        if can_spawn_in_room(requirement, room)
        and (
            not requirement.group_ids or group.dungeon_group_id in requirement.group_ids
        )
        and (not requirement.subgroup_0 or group.subgroup_0 in requirement.subgroup_0)
        and (not requirement.subgroup_1 or group.subgroup_1 in requirement.subgroup_1)
        and (not requirement.subgroup_2 or group.subgroup_2 in requirement.subgroup_2)
        and (not requirement.subgroup_3 or group.subgroup_3 in requirement.subgroup_3)
    )


def _get_randomizable_sprites_in_room(
    state: EnemyShuffleState,
    room: DungeonEnemyRoom,
) -> tuple[DungeonEnemySprite, ...]:
    randomizable_sprite_ids = {
        requirement.sprite_id for requirement in state.sprite_requirements
        if not requirement.do_not_randomize and room.room_id not in requirement.dont_randomize_rooms
    }
    return tuple(sprite for sprite in room.sprites if sprite.sprite_id in randomizable_sprite_ids)


def _get_possible_enemy_requirements_for_overworld_group(
    state: EnemyShuffleState,
    group: DungeonSpriteGroup,
) -> tuple[EnemySpriteRequirement, ...]:
    overworld_requirements = _get_requirements_for_usable_overworld_enemies(state)
    return tuple(
        requirement for requirement in overworld_requirements
        if (
            not requirement.group_ids or group.group_id in requirement.group_ids
        )
        and (not requirement.subgroup_0 or group.subgroup_0 in requirement.subgroup_0)
        and (not requirement.subgroup_1 or group.subgroup_1 in requirement.subgroup_1)
        and (not requirement.subgroup_2 or group.subgroup_2 in requirement.subgroup_2)
        and (not requirement.subgroup_3 or group.subgroup_3 in requirement.subgroup_3)
    )


def _get_randomizable_sprites_in_overworld_area(
    state: EnemyShuffleState,
    area: OverworldEnemyArea,
) -> tuple[OverworldEnemySprite, ...]:
    randomizable_sprite_ids = {
        requirement.sprite_id for requirement in state.sprite_requirements
        if not requirement.do_not_randomize
    }
    return tuple(sprite for sprite in area.sprites if sprite.sprite_id in randomizable_sprite_ids)


def _randomize_dungeon_rooms(
    world: "ALTTPWorld",
    dungeon_rooms: dict[int, DungeonEnemyRoom],
    sprite_groups: dict[int, DungeonSpriteGroup],
    sprite_requirements: tuple[EnemySpriteRequirement, ...],
) -> dict[int, RandomizedDungeonEnemyRoom]:
    state = EnemyShuffleState(
        dungeon_rooms=dungeon_rooms,
        overworld_areas={},
        sprite_groups=sprite_groups,
        sprite_requirements=sprite_requirements,
        room_group_requirements=tuple(),
        overworld_group_requirements=tuple(),
        shutter_room_ids=frozenset(room.room_id for room in dungeon_rooms.values() if room.is_shutter_room),
        water_room_ids=frozenset(room.room_id for room in dungeon_rooms.values() if room.is_water_room),
        dont_randomize_room_ids=frozenset(room.room_id for room in dungeon_rooms.values() if room.do_not_randomize),
        no_special_enemies_standard_room_ids=frozenset(
            room.room_id for room in dungeon_rooms.values() if room.no_special_enemies_standard
        ),
        boss_room_ids=frozenset(),
        dont_randomize_overworld_area_ids=frozenset(),
        randomized_dungeon_rooms={},
        randomized_overworld_areas={},
        combat_model=_get_world_combat_model(world),
        enemy_health_key=_get_world_enemy_health_key(world),
        max_attacks_in_logic=_get_world_max_attacks_in_logic(world),
        killable_thieves=_get_world_killable_thieves(world),
        available_damage_classes=_get_world_available_damage_classes(world),
        hammer_available_for_freeze=True,
    )
    randomized_rooms: dict[int, RandomizedDungeonEnemyRoom] = {}

    for room_id in sorted(dungeon_rooms):
        room = dungeon_rooms[room_id]
        skip_randomization = _dungeon_room_skips_enemy_randomization(world, state, room)

        selected_group = sprite_groups.get(room.graphics_block_id + 0x40)
        if not skip_randomization:
            possible_groups = get_possible_dungeon_sprite_groups(state, room)
            if possible_groups:
                selected_group = world.random.choice(possible_groups)

        if selected_group is None:
            selected_group = sprite_groups[room.graphics_block_id + 0x40]

        randomized_rooms[room_id] = _randomize_room_sprites(
            world,
            state,
            room,
            selected_group,
            skip_randomization,
        )

    return randomized_rooms


def _randomize_overworld_areas(
    world: "ALTTPWorld",
    overworld_areas: dict[int, OverworldEnemyArea],
    sprite_groups: dict[int, DungeonSpriteGroup],
    sprite_requirements: tuple[EnemySpriteRequirement, ...],
    forced_group_requirements: tuple[OverworldGroupRequirement, ...],
) -> dict[int, RandomizedOverworldEnemyArea]:
    state = EnemyShuffleState(
        dungeon_rooms={},
        overworld_areas=overworld_areas,
        sprite_groups=sprite_groups,
        sprite_requirements=sprite_requirements,
        room_group_requirements=tuple(),
        overworld_group_requirements=forced_group_requirements,
        shutter_room_ids=frozenset(),
        water_room_ids=frozenset(),
        dont_randomize_room_ids=frozenset(),
        no_special_enemies_standard_room_ids=frozenset(),
        boss_room_ids=frozenset(),
        dont_randomize_overworld_area_ids=frozenset(area.area_id for area in overworld_areas.values() if area.do_not_randomize),
        randomized_dungeon_rooms={},
        randomized_overworld_areas={},
        combat_model=_get_world_combat_model(world),
        enemy_health_key=_get_world_enemy_health_key(world),
        max_attacks_in_logic=_get_world_max_attacks_in_logic(world),
        killable_thieves=_get_world_killable_thieves(world),
        available_damage_classes=_get_world_available_damage_classes(world),
        hammer_available_for_freeze=True,
    )
    randomized_areas: dict[int, RandomizedOverworldEnemyArea] = {}

    for area_id in sorted(overworld_areas):
        area = overworld_areas[area_id]
        selected_group = sprite_groups.get(area.graphics_block_id)
        skip_randomization = area.do_not_randomize
        if not skip_randomization:
            possible_groups = get_possible_overworld_sprite_groups(state, area)
            if possible_groups:
                selected_group = world.random.choice(possible_groups)

        forced_group = _get_forced_overworld_group(area.area_id, forced_group_requirements, sprite_groups)
        if forced_group is not None:
            selected_group = forced_group
        if selected_group is None:
            selected_group = sprite_groups[area.graphics_block_id]

        randomized_areas[area_id] = _randomize_overworld_area_sprites(
            world,
            state,
            area,
            selected_group,
            skip_randomization,
        )

    return randomized_areas


def _dungeon_room_skips_enemy_randomization(
    world: "ALTTPWorld",
    state: EnemyShuffleState,
    room: DungeonEnemyRoom,
) -> bool:
    return (
        room.do_not_randomize
        or (world.options.mode == "standard" and room.room_id in STANDARD_ESCAPE_DUNGEON_ROOM_IDS)
        or (world.options.mode == "standard" and room.no_special_enemies_standard)
        or not _get_randomizable_sprites_in_room(state, room)
    )


def _get_forced_overworld_group(
    area_id: int,
    forced_group_requirements: tuple[OverworldGroupRequirement, ...],
    sprite_groups: dict[int, DungeonSpriteGroup],
) -> Optional[DungeonSpriteGroup]:
    for requirement in forced_group_requirements:
        if area_id not in requirement.areas or requirement.group_id is None:
            continue
        return sprite_groups.get(requirement.group_id)
    return None


def _randomize_room_sprites(
    world: "ALTTPWorld",
    state: EnemyShuffleState,
    room: DungeonEnemyRoom,
    selected_group: DungeonSpriteGroup,
    skip_randomization: bool,
) -> RandomizedDungeonEnemyRoom:
    randomized_sprites = list(_clone_room_sprites(room))

    if not skip_randomization:
        possible_requirements = _get_possible_enemy_requirements_for_group(state, room, selected_group)
        sprites_to_update = _get_randomizable_sprites_in_room(state, room)
        sprites_to_update_addresses = {sprite.address for sprite in sprites_to_update}

        if possible_requirements:
            water_sprite_ids = [
                requirement.sprite_id for requirement in possible_requirements
                if requirement.is_water_sprite
            ]

            if room.is_water_room:
                if water_sprite_ids:
                    replacement_water_sprite_ids = water_sprite_ids
                    if room.is_shutter_room:
                        killable_water_sprite_ids = [
                            requirement.sprite_id for requirement in possible_requirements
                            if requirement.is_water_sprite
                            and _can_be_shutter_room_clear_enemy(state, requirement)
                        ]
                        if killable_water_sprite_ids:
                            replacement_water_sprite_ids = killable_water_sprite_ids
                    for sprite in randomized_sprites:
                        if sprite.address in sprites_to_update_addresses:
                            _set_randomized_sprite_id(
                                randomized_sprites,
                                sprite.address,
                                world.random.choice(replacement_water_sprite_ids),
                            )
                return _build_randomized_room(room, selected_group, randomized_sprites, False)

            non_water_requirements = _filter_requirements_for_room_water_state(room, possible_requirements)
            safe_non_water_requirements = [
                requirement for requirement in non_water_requirements
                if not room.is_shutter_room or _is_safe_for_enemy_clear_room(state, requirement)
            ]
            possible_sprite_ids = [requirement.sprite_id for requirement in safe_non_water_requirements]
            if not possible_sprite_ids:
                return _build_randomized_room(room, selected_group, randomized_sprites, False)
            killable_sprite_ids = [
                requirement.sprite_id for requirement in safe_non_water_requirements
                if _can_be_shutter_room_clear_enemy(state, requirement)
            ]
            killable_key_sprite_ids = [
                requirement.sprite_id for requirement in safe_non_water_requirements
                if _can_be_key_drop_enemy(state, requirement)
            ]
            killable_shutter_key_sprite_ids = [
                requirement.sprite_id for requirement in safe_non_water_requirements
                if _can_be_key_drop_enemy(state, requirement)
                and _can_be_shutter_room_clear_enemy(state, requirement)
            ]
            stal_count = 0

            for sprite in sprites_to_update:
                replacement_sprite_id: int
                if sprite.has_key and room.is_shutter_room and killable_shutter_key_sprite_ids:
                    replacement_sprite_id = world.random.choice(killable_shutter_key_sprite_ids)
                elif sprite.has_key and killable_key_sprite_ids:
                    replacement_sprite_id = world.random.choice(killable_key_sprite_ids)
                elif room.is_shutter_room and killable_sprite_ids:
                    replacement_sprite_id = world.random.choice(killable_sprite_ids)
                elif not room.is_shutter_room and world.random.randrange(100) < 5:
                    replacement_sprite_id = STAL_SPRITE_ID
                else:
                    replacement_sprite_id = world.random.choice(possible_sprite_ids)

                _set_randomized_sprite_id(randomized_sprites, sprite.address, replacement_sprite_id)

                if replacement_sprite_id == STAL_SPRITE_ID:
                    stal_count += 1
                    if stal_count > 2:
                        possible_sprite_ids = [sprite_id for sprite_id in possible_sprite_ids if sprite_id != STAL_SPRITE_ID]

    return _build_randomized_room(room, selected_group, randomized_sprites, skip_randomization)


def _randomize_overworld_area_sprites(
    world: "ALTTPWorld",
    state: EnemyShuffleState,
    area: OverworldEnemyArea,
    selected_group: DungeonSpriteGroup,
    skip_randomization: bool,
) -> RandomizedOverworldEnemyArea:
    randomized_sprites = list(_clone_overworld_area_sprites(area))
    bush_sprite_id = area.bush_sprite_id

    if not skip_randomization:
        possible_requirements = _get_possible_enemy_requirements_for_overworld_group(state, selected_group)
        possible_sprite_ids = [requirement.sprite_id for requirement in possible_requirements]
        sprites_to_update = _get_randomizable_sprites_in_overworld_area(state, area)
        sprites_to_update_addresses = {sprite.address for sprite in sprites_to_update}

        if possible_sprite_ids:
            for sprite in sprites_to_update:
                _set_randomized_overworld_sprite_id(
                    randomized_sprites,
                    sprite.address,
                    world.random.choice(possible_sprite_ids),
                )

            flopping_fish_addresses = [
                sprite.address for sprite in randomized_sprites
                if sprite.address in sprites_to_update_addresses and sprite.sprite_id == FLOPPING_FISH_SPRITE_ID
            ]
            if len(flopping_fish_addresses) > 1:
                non_fish_sprite_ids = [
                    sprite_id for sprite_id in possible_sprite_ids if sprite_id != FLOPPING_FISH_SPRITE_ID
                ]
                for address in flopping_fish_addresses[1:]:
                    if non_fish_sprite_ids:
                        _set_randomized_overworld_sprite_id(
                            randomized_sprites,
                            address,
                            world.random.choice(non_fish_sprite_ids),
                        )

            bush_candidates = [
                requirement.sprite_id for requirement in possible_requirements
                if not requirement.overlord
            ]
            if bush_candidates:
                bush_sprite_id = world.random.choice(bush_candidates)

    return RandomizedOverworldEnemyArea(
        area_id=area.area_id,
        sprite_table_address=area.sprite_table_address,
        graphics_block_address=area.graphics_block_address,
        original_graphics_block_id=area.graphics_block_id,
        graphics_block_id=selected_group.group_id,
        original_bush_sprite_id=area.bush_sprite_id,
        bush_sprite_id=bush_sprite_id,
        sprites=tuple(randomized_sprites),
        skipped_randomization=skip_randomization,
    )


def _clone_room_sprites(room: DungeonEnemyRoom) -> list[RandomizedDungeonEnemySprite]:
    return [
        RandomizedDungeonEnemySprite(
            address=sprite.address,
            byte_0=sprite.byte_0,
            byte_1=sprite.byte_1,
            original_sprite_id=sprite.sprite_id,
            sprite_id=sprite.sprite_id,
            is_overlord=sprite.is_overlord,
            has_key=sprite.has_key,
        )
        for sprite in room.sprites
    ]


def _clone_overworld_area_sprites(area: OverworldEnemyArea) -> list[RandomizedOverworldEnemySprite]:
    return [
        RandomizedOverworldEnemySprite(
            address=sprite.address,
            y_coord=sprite.y_coord,
            x_coord=sprite.x_coord,
            original_sprite_id=sprite.sprite_id,
            sprite_id=sprite.sprite_id,
        )
        for sprite in area.sprites
    ]


def _set_randomized_sprite_id(
    randomized_sprites: list[RandomizedDungeonEnemySprite],
    address: int,
    sprite_id: int,
) -> None:
    for index, sprite in enumerate(randomized_sprites):
        if sprite.address != address:
            continue
        randomized_sprites[index] = RandomizedDungeonEnemySprite(
            address=sprite.address,
            byte_0=sprite.byte_0,
            byte_1=sprite.byte_1,
            original_sprite_id=sprite.original_sprite_id,
            sprite_id=sprite_id,
            is_overlord=sprite.is_overlord,
            has_key=sprite.has_key,
        )
        return


def _set_randomized_overworld_sprite_id(
    randomized_sprites: list[RandomizedOverworldEnemySprite],
    address: int,
    sprite_id: int,
) -> None:
    for index, sprite in enumerate(randomized_sprites):
        if sprite.address != address:
            continue
        randomized_sprites[index] = RandomizedOverworldEnemySprite(
            address=sprite.address,
            y_coord=sprite.y_coord,
            x_coord=sprite.x_coord,
            original_sprite_id=sprite.original_sprite_id,
            sprite_id=sprite_id,
        )
        return


def _build_randomized_room(
    room: DungeonEnemyRoom,
    selected_group: DungeonSpriteGroup,
    sprites: list[RandomizedDungeonEnemySprite],
    skipped_randomization: bool,
) -> RandomizedDungeonEnemyRoom:
    return RandomizedDungeonEnemyRoom(
        room_id=room.room_id,
        room_header_address=room.room_header_address,
        sprite_table_address=room.sprite_table_address,
        original_graphics_block_id=room.graphics_block_id,
        graphics_block_id=selected_group.dungeon_group_id,
        tag_1=room.tag_1,
        tag_2=room.tag_2,
        sort_sprites_value=room.sort_sprites_value,
        sprites=tuple(sprites),
        skipped_randomization=skipped_randomization,
    )


def validate_enemy_shuffle_state(state: EnemyShuffleState, is_standard_mode: bool) -> None:
    for room_id, room in state.dungeon_rooms.items():
        randomized_room = state.randomized_dungeon_rooms[room_id]
        _validate_dungeon_room(state, room, randomized_room, is_standard_mode)

    for area_id, area in state.overworld_areas.items():
        randomized_area = state.randomized_overworld_areas[area_id]
        _validate_overworld_area(state, area, randomized_area, is_standard_mode)


def _validate_dungeon_room(
    state: EnemyShuffleState,
    room: DungeonEnemyRoom,
    randomized_room: RandomizedDungeonEnemyRoom,
    is_standard_mode: bool,
) -> None:
    selected_group = state.sprite_groups.get(randomized_room.graphics_block_id + 0x40)
    if selected_group is None:
        raise ValueError(f"Enemy shuffle produced unknown dungeon sprite group {randomized_room.graphics_block_id} for room {room.room_id}")

    skipped = (
        room.do_not_randomize
        or (is_standard_mode and room.no_special_enemies_standard)
        or not _get_randomizable_sprites_in_room(state, room)
    )
    if skipped and randomized_room.graphics_block_id != room.graphics_block_id:
        raise ValueError(f"Enemy shuffle changed skipped room {room.room_id} graphics block")

    if not skipped:
        possible_groups = get_possible_dungeon_sprite_groups(state, room)
        assert possible_groups, f"Enemy shuffle found no legal dungeon sprite group for room {room.room_id}"
        if possible_groups and selected_group not in possible_groups:
            raise ValueError(f"Enemy shuffle selected illegal sprite group {selected_group.group_id} for room {room.room_id}")
        _validate_dungeon_room_sprite_graphics(state, room, randomized_room, selected_group)

    possible_requirements = _get_possible_enemy_requirements_for_group(state, room, selected_group)
    possible_sprite_ids = {requirement.sprite_id for requirement in possible_requirements}
    killable_sprite_ids = {
        requirement.sprite_id for requirement in possible_requirements
        if _can_be_shutter_room_clear_enemy(state, requirement)
    }
    killable_key_sprite_ids = {
        requirement.sprite_id for requirement in possible_requirements
        if _can_be_key_drop_enemy(state, requirement)
    }
    water_sprite_ids = {
        requirement.sprite_id for requirement in possible_requirements
        if requirement.is_water_sprite
    }
    if not room.is_water_room:
        possible_sprite_ids -= water_sprite_ids
        killable_sprite_ids -= water_sprite_ids
        killable_key_sprite_ids -= water_sprite_ids
    do_not_randomize_sprite_ids = {
        requirement.sprite_id for requirement in state.sprite_requirements
        if requirement.do_not_randomize or room.room_id in requirement.dont_randomize_rooms
    }
    randomized_by_address = {sprite.address: sprite for sprite in randomized_room.sprites}

    for original_sprite in room.sprites:
        randomized_sprite = randomized_by_address[original_sprite.address]
        if original_sprite.sprite_id in do_not_randomize_sprite_ids and randomized_sprite.sprite_id != original_sprite.sprite_id:
            raise ValueError(f"Enemy shuffle changed do-not-randomize sprite in room {room.room_id} at {hex(original_sprite.address)}")

        if original_sprite.sprite_id in do_not_randomize_sprite_ids or skipped:
            continue

        if room.is_water_room:
            if randomized_sprite.sprite_id not in water_sprite_ids:
                raise ValueError(f"Enemy shuffle placed non-water enemy {hex(randomized_sprite.sprite_id)} in water room {room.room_id}")
            continue
        if randomized_sprite.sprite_id in water_sprite_ids:
            raise ValueError(f"Enemy shuffle placed water enemy {hex(randomized_sprite.sprite_id)} in non-water room {room.room_id}")

        if original_sprite.has_key:
            if randomized_sprite.sprite_id not in killable_key_sprite_ids:
                raise ValueError(f"Enemy shuffle placed invalid key enemy {hex(randomized_sprite.sprite_id)} in room {room.room_id}")
            if room.is_shutter_room and randomized_sprite.sprite_id not in killable_sprite_ids:
                raise ValueError(f"Enemy shuffle placed non-killable shutter key enemy {hex(randomized_sprite.sprite_id)} in room {room.room_id}")
            continue

        if room.is_shutter_room:
            randomized_requirement = _get_requirement_for_sprite_id(state, randomized_sprite.sprite_id)
            if randomized_requirement is not None and _is_enemy_clear_dealbreaker(state, randomized_requirement):
                raise ValueError(f"Enemy shuffle placed enemy-clear blocker {hex(randomized_sprite.sprite_id)} in room {room.room_id}")

        if randomized_sprite.sprite_id != STAL_SPRITE_ID and randomized_sprite.sprite_id not in possible_sprite_ids:
            raise ValueError(f"Enemy shuffle placed illegal sprite {hex(randomized_sprite.sprite_id)} in room {room.room_id}")

    if not skipped and room.is_shutter_room and _get_randomizable_sprites_in_room(state, room):
        all_killable_sprite_ids = {
            requirement.sprite_id for requirement in _filter_requirements_for_room_water_state(room, state.sprite_requirements)
            if _can_be_shutter_room_clear_enemy(state, requirement)
        }
        randomized_sprite_ids = {
            sprite.sprite_id for sprite in randomized_room.sprites
            if (
                (requirement := _get_requirement_for_sprite_id(state, sprite.sprite_id)) is not None
                and requirement.counts_for_enemy_clear
            )
        }
        if not (randomized_sprite_ids & all_killable_sprite_ids):
            raise ValueError(f"Enemy shuffle left shutter room {room.room_id} without any killable enemies")


def _validate_dungeon_room_sprite_graphics(
    state: EnemyShuffleState,
    room: DungeonEnemyRoom,
    randomized_room: RandomizedDungeonEnemyRoom,
    selected_group: DungeonSpriteGroup,
) -> None:
    for sprite in randomized_room.sprites:
        requirement = _get_requirement_for_sprite_id(state, sprite.sprite_id)
        if requirement is None:
            continue
        if not _dungeon_sprite_group_supports_requirement(selected_group, requirement):
            raise ValueError(
                "Enemy shuffle produced bad graphics in room "
                f"{room.room_id}: {requirement.sprite_name} ({sprite.sprite_id:#04x}) "
                f"uses graphics block {randomized_room.graphics_block_id} "
                f"(group {selected_group.group_id:#04x}, subgroups "
                f"{selected_group.subgroup_0:#04x}/"
                f"{selected_group.subgroup_1:#04x}/"
                f"{selected_group.subgroup_2:#04x}/"
                f"{selected_group.subgroup_3:#04x})"
                f"{_format_sprite_graphics_requirement(requirement)}"
            )


def _dungeon_sprite_group_supports_requirement(
    group: DungeonSpriteGroup,
    requirement: EnemySpriteRequirement,
) -> bool:
    return (
        (not requirement.group_ids or group.group_id in requirement.group_ids)
        and (not requirement.subgroup_0 or group.subgroup_0 in requirement.subgroup_0)
        and (not requirement.subgroup_1 or group.subgroup_1 in requirement.subgroup_1)
        and (not requirement.subgroup_2 or group.subgroup_2 in requirement.subgroup_2)
        and (not requirement.subgroup_3 or group.subgroup_3 in requirement.subgroup_3)
    )


def _format_sprite_graphics_requirement(requirement: EnemySpriteRequirement) -> str:
    parts = []
    if requirement.group_ids:
        parts.append(f"group in {_format_int_tuple(requirement.group_ids)}")
    if requirement.subgroup_0:
        parts.append(f"subgroup 0 in {_format_int_tuple(requirement.subgroup_0)}")
    if requirement.subgroup_1:
        parts.append(f"subgroup 1 in {_format_int_tuple(requirement.subgroup_1)}")
    if requirement.subgroup_2:
        parts.append(f"subgroup 2 in {_format_int_tuple(requirement.subgroup_2)}")
    if requirement.subgroup_3:
        parts.append(f"subgroup 3 in {_format_int_tuple(requirement.subgroup_3)}")
    return "" if not parts else "; requires " + ", ".join(parts)


def _format_int_tuple(values: tuple[int, ...]) -> str:
    return "(" + ", ".join(f"{value:#04x}" for value in values) + ")"


def _validate_overworld_area(
    state: EnemyShuffleState,
    area: OverworldEnemyArea,
    randomized_area: RandomizedOverworldEnemyArea,
    is_standard_mode: bool,
) -> None:
    selected_group = state.sprite_groups.get(randomized_area.graphics_block_id)
    if selected_group is None:
        raise ValueError(f"Enemy shuffle produced unknown overworld sprite group {randomized_area.graphics_block_id} for area {hex(area.area_id)}")

    if area.do_not_randomize and randomized_area.graphics_block_id != area.graphics_block_id:
        raise ValueError(f"Enemy shuffle changed skipped overworld area {hex(area.area_id)} graphics block")

    forced_group = _get_forced_overworld_group(area.area_id, state.overworld_group_requirements, state.sprite_groups)
    if forced_group is not None and randomized_area.graphics_block_id != forced_group.group_id:
        raise ValueError(f"Enemy shuffle failed forced overworld group for area {hex(area.area_id)}")

    if not area.do_not_randomize and forced_group is None:
        possible_groups = get_possible_overworld_sprite_groups(state, area)
        if possible_groups and selected_group not in possible_groups:
            raise ValueError(f"Enemy shuffle selected illegal overworld group {selected_group.group_id} for area {hex(area.area_id)}")

    possible_requirements = _get_possible_enemy_requirements_for_overworld_group(state, selected_group)
    possible_sprite_ids = {requirement.sprite_id for requirement in possible_requirements}
    bush_sprite_ids = {
        requirement.sprite_id for requirement in possible_requirements
        if not requirement.overlord
    }
    known_sprite_ids = {requirement.sprite_id for requirement in state.sprite_requirements}
    do_not_randomize_sprite_ids = {
        requirement.sprite_id for requirement in state.sprite_requirements
        if requirement.do_not_randomize
    }
    randomized_by_address = {sprite.address: sprite for sprite in randomized_area.sprites}

    for original_sprite in area.sprites:
        randomized_sprite = randomized_by_address[original_sprite.address]
        if original_sprite.sprite_id not in known_sprite_ids:
            continue
        if original_sprite.sprite_id in do_not_randomize_sprite_ids and randomized_sprite.sprite_id != original_sprite.sprite_id:
            raise ValueError(f"Enemy shuffle changed do-not-randomize overworld sprite in area {hex(area.area_id)} at {hex(original_sprite.address)}")
        if original_sprite.sprite_id in do_not_randomize_sprite_ids or area.do_not_randomize:
            continue
        if randomized_sprite.sprite_id not in possible_sprite_ids:
            raise ValueError(f"Enemy shuffle placed illegal overworld sprite {hex(randomized_sprite.sprite_id)} in area {hex(area.area_id)}")

    randomizable_addresses = {sprite.address for sprite in _get_randomizable_sprites_in_overworld_area(state, area)}
    non_fish_sprite_ids = possible_sprite_ids - {FLOPPING_FISH_SPRITE_ID}
    if non_fish_sprite_ids and sum(
        1 for sprite in randomized_area.sprites
        if sprite.address in randomizable_addresses and sprite.sprite_id == FLOPPING_FISH_SPRITE_ID
    ) > 1:
        raise ValueError(f"Enemy shuffle placed multiple flopping fish in area {hex(area.area_id)}")

    if area.do_not_randomize and randomized_area.bush_sprite_id != area.bush_sprite_id:
        raise ValueError(f"Enemy shuffle changed skipped overworld bush sprite in area {hex(area.area_id)}")
    if not area.do_not_randomize and bush_sprite_ids and randomized_area.bush_sprite_id not in bush_sprite_ids:
        raise ValueError(f"Enemy shuffle placed illegal bush enemy {hex(randomized_area.bush_sprite_id)} in area {hex(area.area_id)}")


def apply_enemy_shuffle(rom: "TokenRom", state: EnemyShuffleState) -> None:
    for group in state.sprite_groups.values():
        _write_sprite_group(rom, group)

    for room in state.randomized_dungeon_rooms.values():
        rom.write_byte(room.room_header_address + 3, room.graphics_block_id)
        for sprite in room.sprites:
            _write_dungeon_sprite(rom, sprite)

    rom.write_byte(0x04CF4F, 0x10)
    for area in state.randomized_overworld_areas.values():
        rom.write_byte(area.graphics_block_address, area.graphics_block_id)
        for sprite in area.sprites:
            _write_overworld_sprite(rom, sprite)

    bush_spawn_table_address = _get_enemizer_symbol("sprite_bush_spawn_table_overworld")
    for area in state.randomized_overworld_areas.values():
        rom.write_byte(bush_spawn_table_address + area.area_id, area.bush_sprite_id)


def _write_sprite_group(rom: "TokenRom", group: DungeonSpriteGroup) -> None:
    address = SPRITE_GROUP_BASE_ADDRESS + (group.group_id * 4)
    rom.write_byte(address, group.subgroup_0)
    rom.write_byte(address + 1, group.subgroup_1)
    rom.write_byte(address + 2, group.subgroup_2)
    rom.write_byte(address + 3, group.subgroup_3)


def _write_dungeon_sprite(rom: "TokenRom", sprite: RandomizedDungeonEnemySprite) -> None:
    sprite_id = sprite.sprite_id
    byte_1 = sprite.byte_1

    if sprite_id == WALLMASTER_SPRITE_ID:
        sprite_id = 0x09
        byte_1 |= SPRITE_OVERLORD_MASK

    rom.write_byte(sprite.address, sprite.byte_0)
    rom.write_byte(sprite.address + 1, byte_1)
    rom.write_byte(sprite.address + 2, sprite_id & 0xFF)


def _write_overworld_sprite(rom: "TokenRom", sprite: RandomizedOverworldEnemySprite) -> None:
    sprite_id = sprite.sprite_id
    if sprite_id == OW_FALLING_ROCKS_SPRITE_ID:
        rom.write_byte(sprite.address, 0)
        rom.write_byte(sprite.address + 1, 0)
    if sprite_id == WALLMASTER_SPRITE_ID:
        sprite_id = OW_WALLMASTER_TO_HOULIHAN_SPRITE_ID
    rom.write_byte(sprite.address + 2, sprite_id & 0xFF)
