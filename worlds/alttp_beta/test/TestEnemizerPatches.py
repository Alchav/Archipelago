import unittest
import random
from types import SimpleNamespace

from worlds.alttp.EnemizerPatches import (
    ARROW_REFILL_5_SPRITE_ID,
    BOSS_GFX_SHEET_INDEXES,
    BOSS_PATCH_DATA,
    DAMAGE_GROUP_TABLE_ADDRESS,
    DUNGEON_BOSS_PATCH_DATA,
    ENEMY_DAMAGE_TABLE_ADDRESS,
    ENEMY_HP_TABLE_ADDRESS,
    EXCLUDED_ENEMY_TABLE_SPRITE_IDS,
    HARDHAT_BEETLE_HP_TABLE_ADDRESS,
    HIDDEN_ENEMY_CHANCE_POOL_ADDRESS,
    RANDOMIZED_HIDDEN_ENEMY_CHANCE_POOL,
    RETRO_ARROW_REPLACEMENT_CHECK_ADDRESS,
    RETRO_RUPEE_REPLACEMENT_SPRITE_ID,
    THIEF_DEFAULT_HP,
    THIEF_SPRITE_ID,
    TILE_TRAP_FLOOR_TILE_ADDRESS,
    TRINEXX_ICE_FLOOR_ROUTINE_ADDRESS,
    TRINEXX_ICE_PROJECTILE_TILE_ADDRESS,
    VANILLA_HIDDEN_ENEMY_CHANCE_POOL,
    SPRITE_DAMAGE_SUBCLASS_TABLE_ADDRESS,
    apply_enemy_combat_data,
    _apply_killable_thief,
    _apply_randomized_tile_trap_floor_tile,
    _get_enemizer_symbol,
    _make_native_enemizer_rng,
    _option_key,
    patch_bosses,
    _randomize_enemy_damage,
    _randomize_enemy_health,
    _set_enemizer_flag,
    _shuffle_damage_groups,
    _update_hidden_enemy_item_table_for_retro_mode,
    apply_enemizer_base_patch,
)
from worlds.alttp.enemizer_data.enemy_combat_data import (
    ANTI_FAIRY_SPRITE_ID,
    BLOB_TRANSFORM_EFFECT,
    BOSS_DAMAGE_CLASS_RANDOMIZER_SPRITE_IDS,
    BOSS_REQUIRED_LOGIC_KILL_DAMAGE_CLASS_GROUPS,
    BOSS_SPRITE_IDS_FORBID_SPECIAL_DAMAGE_EFFECTS,
    CHAOS_RANDOMIZE_DAMAGE_CLASSES,
    DAMAGE_CLASS_RANDOMIZER_HP_255_INCLUDED_SPRITE_IDS,
    DAMAGE_SOURCE_TABLE_ADDRESS,
    DAMAGE_SOURCE_TABLE_SIZE,
    DEADROCK_SPRITE_ID,
    EnemyCombatModel,
    EXCLUDED_ENEMY_TABLE_SPRITE_IDS,
    FAIRY_TRANSFORM_EFFECT,
    FIGHTER_SWORD_DAMAGE_CLASSES,
    GOLDEN_SWORD_SPIN_DAMAGE_CLASS,
    GOLDEN_SWORD_DAMAGE_CLASSES,
    GANON_D7_SPRITE_ID,
    HELMASAUR_KING_SPRITE_ID,
    INCINERATE_EFFECT,
    LANMOLAS_SPRITE_ID,
    LIGHTNING_GATE_SPRITE_ID,
    LOST_SWORD_UPGRADE_DAMAGE_CLASS,
    MASTER_SWORD_DAMAGE_CLASSES,
    MIXED_RANDOMIZE_DAMAGE_CLASSES,
    MOTHULA_SPRITE_ID,
    NIGHTMARE_RANDOMIZE_DAMAGE_CLASSES,
    NON_VANILLA_RANDOMIZE_DAMAGE_CLASS_MODES,
    RED_BARI_SPRITE_ID,
    SPRITE_DAMAGE_SUBCLASS_TABLE_SIZE,
    SPRITE_DAMAGE_SUBCLASSES,
    SPECIAL_DAMAGE_EFFECTS,
    SWORD_CLASS_2_REPLACEMENT_DAMAGE_CLASSES,
    SWORD_BEAM_DAMAGE_CLASS,
    TEMPERED_SWORD_DAMAGE_CLASSES,
    VANILLA_COMBAT_MODEL,
    build_damage_source_table_bytes,
    build_packed_sprite_damage_subclass_table,
    build_randomized_damage_class_combat_model,
    get_blob_transform_damage_classes,
    get_damage_classes_with_effects,
    get_damage_effect,
    get_enemy_health_for_logic,
    get_hits_to_kill,
    get_incinerating_damage_classes,
    get_killing_damage_classes,
    is_defeating_damage_effect_for_nightmare,
    _swap_damage_class_effects,
)


SPIKE_BLOCK_SPRITE_ID = 0x8A


class FakeRom:
    def __init__(self, size: int = 0x400000) -> None:
        self.buffer = bytearray(size)

    def read_byte(self, address: int) -> int:
        return self.buffer[address]

    def read_bytes(self, startaddress: int, length: int) -> bytearray:
        return self.buffer[startaddress:startaddress + length]

    def write_byte(self, address: int, value: int) -> None:
        self.buffer[address] = value

    def write_bytes(self, startaddress: int, values) -> None:
        self.buffer[startaddress:startaddress + len(values)] = values

    def write_int16(self, address: int, value: int) -> None:
        self.write_bytes(address, (value & 0xFF, (value >> 8) & 0xFF))


class FakeTokenRom:
    def __init__(self) -> None:
        self.bytes: dict[int, int] = {}

    def read_byte(self, address: int) -> int:
        try:
            return self.bytes[address]
        except KeyError as e:
            raise RuntimeError(f"unwritten byte {address:#x}") from e

    def write_byte(self, address: int, value: int) -> None:
        self.write_bytes(address, (value,))

    def write_bytes(self, startaddress: int, values) -> None:
        for offset, value in enumerate(values):
            self.bytes[startaddress + offset] = value

    def write_int16(self, address: int, value: int) -> None:
        self.write_bytes(address, (value & 0xFF, (value >> 8) & 0xFF))


def has_vanilla_damage_profile(sprite_id: int) -> bool:
    return any(get_damage_effect(sprite_id, damage_class) != 0 for damage_class in range(16))


class TestEnemizerPatches(unittest.TestCase):
    def test_enemizer_base_patch_applies_mimic_hooks(self) -> None:
        rom = FakeRom()

        apply_enemizer_base_patch(rom)

        self.assertEqual(tuple(rom.read_bytes(0x307CB, 2)), (0xB6, 0x91))
        self.assertEqual(tuple(rom.read_bytes(0x311B6, 4)), (0x22, 0x1A, 0x9A, 0x36))
        self.assertEqual(tuple(rom.read_bytes(0x36C08, 5)), (0x22, 0x4E, 0x9A, 0x36, 0xEA))
        self.assertEqual(tuple(rom.read_bytes(0x36DA6, 4)), (0x22, 0x66, 0x9A, 0x36))
        self.assertEqual(tuple(rom.read_bytes(0xF0BB1, 2)), (0x95, 0xC7))
        self.assertEqual(tuple(rom.read_bytes(TRINEXX_ICE_FLOOR_ROUTINE_ADDRESS, 4)), (0xEA, 0xEA, 0xEA, 0xEA))
        self.assertEqual(tuple(rom.read_bytes(TRINEXX_ICE_PROJECTILE_TILE_ADDRESS, 2)), (0x00, 0x00))
        self.assertEqual(rom.read_byte(TILE_TRAP_FLOOR_TILE_ADDRESS), 0x00)

    def test_randomized_tile_trap_floor_tile_patch_is_separate(self) -> None:
        rom = FakeRom()

        _apply_randomized_tile_trap_floor_tile(rom)

        self.assertEqual(tuple(rom.read_bytes(TRINEXX_ICE_PROJECTILE_TILE_ADDRESS, 2)), (0x88, 0x01))
        self.assertEqual(rom.read_byte(TILE_TRAP_FLOOR_TILE_ADDRESS), 0x12)

    def test_enemy_combat_data_is_written_from_python_tables(self) -> None:
        rom = FakeRom()

        apply_enemy_combat_data(rom)

        damage_sources = build_damage_source_table_bytes()
        packed_subclasses = build_packed_sprite_damage_subclass_table()
        mothula_packed_offset = SPRITE_DAMAGE_SUBCLASS_TABLE_ADDRESS + (MOTHULA_SPRITE_ID * 8)

        self.assertEqual(len(damage_sources), DAMAGE_SOURCE_TABLE_SIZE)
        self.assertEqual(len(packed_subclasses), SPRITE_DAMAGE_SUBCLASS_TABLE_SIZE)
        self.assertEqual(tuple(rom.read_bytes(DAMAGE_SOURCE_TABLE_ADDRESS, len(damage_sources))), tuple(damage_sources))
        self.assertEqual(
            tuple(rom.read_bytes(SPRITE_DAMAGE_SUBCLASS_TABLE_ADDRESS, len(packed_subclasses))),
            tuple(packed_subclasses),
        )
        self.assertEqual(SPRITE_DAMAGE_SUBCLASSES[MOTHULA_SPRITE_ID][4:6], (1, 1))
        self.assertEqual(get_damage_effect(MOTHULA_SPRITE_ID, 4), 0x10)
        self.assertEqual(get_damage_effect(MOTHULA_SPRITE_ID, 5), 0x10)
        self.assertIn(4, get_killing_damage_classes(MOTHULA_SPRITE_ID))
        self.assertIn(5, get_killing_damage_classes(MOTHULA_SPRITE_ID))
        self.assertEqual(get_damage_effect(0x27, 10), BLOB_TRANSFORM_EFFECT)
        self.assertEqual(get_blob_transform_damage_classes(0x27), (10, 15))
        self.assertEqual(
            tuple(rom.read_bytes(mothula_packed_offset, 8)),
            (0x01, 0x11, 0x11, 0x00, 0x00, 0x04, 0x00, 0x00),
        )

    def test_enemy_combat_damage_source_names_are_readable(self) -> None:
        damage_source_names = {
            source.damage_class: source.name
            for source in VANILLA_COMBAT_MODEL.damage_sources
        }

        self.assertEqual(damage_source_names[9], "Silver Arrows")
        self.assertEqual(damage_source_names[10], "Magic Powder")
        self.assertEqual(damage_source_names[11], "Fire Rod")
        self.assertEqual(damage_source_names[12], "Ice Rod")

    def test_lanmolas_forbids_special_damage_effects(self) -> None:
        custom_damage_sources = list(VANILLA_COMBAT_MODEL.damage_sources)
        custom_damage_sources[0] = custom_damage_sources[0]._replace(
            subclasses=(0, INCINERATE_EFFECT) + custom_damage_sources[0].subclasses[2:]
        )
        custom_damage_sources[1] = custom_damage_sources[1]._replace(
            subclasses=(0, 4) + custom_damage_sources[1].subclasses[2:]
        )
        custom_damage_sources[10] = custom_damage_sources[10]._replace(
            subclasses=(0, BLOB_TRANSFORM_EFFECT) + custom_damage_sources[10].subclasses[2:]
        )
        custom_sprite_rows = list(VANILLA_COMBAT_MODEL.sprite_damage_subclasses)
        lanmolas_row = [0] * 16
        lanmolas_row[0] = 1
        lanmolas_row[1] = 1
        lanmolas_row[10] = 1
        custom_sprite_rows[LANMOLAS_SPRITE_ID] = tuple(lanmolas_row)
        custom_combat_model = EnemyCombatModel(
            damage_sources=tuple(custom_damage_sources),
            sprite_damage_subclasses=tuple(custom_sprite_rows),
            enemy_health_table=VANILLA_COMBAT_MODEL.enemy_health_table,
        )

        self.assertIn(LANMOLAS_SPRITE_ID, BOSS_SPRITE_IDS_FORBID_SPECIAL_DAMAGE_EFFECTS)
        self.assertEqual(
            get_damage_classes_with_effects(
                LANMOLAS_SPRITE_ID,
                frozenset({INCINERATE_EFFECT, BLOB_TRANSFORM_EFFECT}),
                custom_combat_model,
            ),
            tuple(),
        )
        self.assertEqual(get_killing_damage_classes(LANMOLAS_SPRITE_ID, custom_combat_model), (1,))
        self.assertEqual(get_hits_to_kill(LANMOLAS_SPRITE_ID, 0, "default", combat_model=custom_combat_model), None)
        self.assertEqual(get_blob_transform_damage_classes(LANMOLAS_SPRITE_ID, custom_combat_model), tuple())

    def test_enemy_combat_data_uses_supplied_combat_model(self) -> None:
        rom = FakeRom()
        custom_damage_sources = list(VANILLA_COMBAT_MODEL.damage_sources)
        custom_damage_sources[0] = custom_damage_sources[0]._replace(subclasses=(0x7F,) + custom_damage_sources[0].subclasses[1:])
        custom_sprite_rows = list(VANILLA_COMBAT_MODEL.sprite_damage_subclasses)
        mothula_row = list(custom_sprite_rows[MOTHULA_SPRITE_ID])
        mothula_row[0] = 0x07
        custom_sprite_rows[MOTHULA_SPRITE_ID] = tuple(mothula_row)
        custom_combat_model = EnemyCombatModel(
            damage_sources=tuple(custom_damage_sources),
            sprite_damage_subclasses=tuple(custom_sprite_rows),
            enemy_health_table=VANILLA_COMBAT_MODEL.enemy_health_table,
        )

        apply_enemy_combat_data(rom, custom_combat_model)

        self.assertEqual(
            tuple(rom.read_bytes(DAMAGE_SOURCE_TABLE_ADDRESS, DAMAGE_SOURCE_TABLE_SIZE)),
            tuple(build_damage_source_table_bytes(custom_combat_model.damage_sources)),
        )
        self.assertEqual(
            tuple(rom.read_bytes(SPRITE_DAMAGE_SUBCLASS_TABLE_ADDRESS, SPRITE_DAMAGE_SUBCLASS_TABLE_SIZE)),
            tuple(build_packed_sprite_damage_subclass_table(custom_combat_model.sprite_damage_subclasses)),
        )

    def test_randomized_damage_classes_preserve_excluded_effects(self) -> None:
        for mode in NON_VANILLA_RANDOMIZE_DAMAGE_CLASS_MODES:
            with self.subTest(mode=mode):
                combat_model = build_randomized_damage_class_combat_model(random.Random(0), mode)

                for sprite_id in EXCLUDED_ENEMY_TABLE_SPRITE_IDS:
                    if sprite_id >= len(VANILLA_COMBAT_MODEL.sprite_damage_subclasses):
                        continue
                    for damage_class in range(16):
                        self.assertEqual(
                            get_damage_effect(sprite_id, damage_class, combat_model),
                            get_damage_effect(sprite_id, damage_class),
                        )

    def test_randomized_damage_classes_change_boss_rows(self) -> None:
        for mode in NON_VANILLA_RANDOMIZE_DAMAGE_CLASS_MODES:
            with self.subTest(mode=mode):
                combat_model = build_randomized_damage_class_combat_model(random.Random(2), mode)
                changed = any(
                    get_damage_effect(sprite_id, damage_class, combat_model) != get_damage_effect(sprite_id, damage_class)
                    for sprite_id in BOSS_DAMAGE_CLASS_RANDOMIZER_SPRITE_IDS
                    if sprite_id < len(VANILLA_COMBAT_MODEL.sprite_damage_subclasses)
                    for damage_class in range(16)
                )
                self.assertTrue(changed)

    def test_randomized_damage_classes_change_lightning_gate_row(self) -> None:
        for mode in NON_VANILLA_RANDOMIZE_DAMAGE_CLASS_MODES:
            with self.subTest(mode=mode):
                changed = any(
                    get_damage_effect(
                        LIGHTNING_GATE_SPRITE_ID,
                        damage_class,
                        build_randomized_damage_class_combat_model(random.Random(seed), mode),
                    ) != get_damage_effect(LIGHTNING_GATE_SPRITE_ID, damage_class)
                    for seed in range(10)
                    for damage_class in range(16)
                )
                self.assertTrue(changed)

    def test_randomized_damage_classes_sanitize_forbidden_boss_special_effects(self) -> None:
        for mode in NON_VANILLA_RANDOMIZE_DAMAGE_CLASS_MODES:
            with self.subTest(mode=mode):
                combat_model = build_randomized_damage_class_combat_model(random.Random(3), mode)

                for sprite_id in BOSS_SPRITE_IDS_FORBID_SPECIAL_DAMAGE_EFFECTS:
                    with self.subTest(mode=mode, sprite_id=sprite_id):
                        self.assertFalse(any(
                            get_damage_effect(sprite_id, damage_class, combat_model) in SPECIAL_DAMAGE_EFFECTS
                            for damage_class in range(16)
                        ))

    def test_randomized_damage_classes_guarantee_boss_logic_classes(self) -> None:
        for mode in NON_VANILLA_RANDOMIZE_DAMAGE_CLASS_MODES:
            if mode == NIGHTMARE_RANDOMIZE_DAMAGE_CLASSES:
                continue
            with self.subTest(mode=mode):
                combat_model = build_randomized_damage_class_combat_model(
                    random.Random(4),
                    mode,
                    enemy_health_key="hard",
                )

                for sprite_id, damage_class_groups in BOSS_REQUIRED_LOGIC_KILL_DAMAGE_CLASS_GROUPS.items():
                    with self.subTest(mode=mode, sprite_id=sprite_id):
                        for damage_classes in damage_class_groups:
                            hit_counts = tuple(
                                get_hits_to_kill(
                                    sprite_id,
                                    damage_class,
                                    "hard",
                                    combat_model=combat_model,
                                )
                                for damage_class in damage_classes
                            )
                            self.assertTrue(any(hit_count is not None for hit_count in hit_counts))

    def test_randomized_damage_classes_guarantee_swordless_helmasaur_bow_logic_classes(self) -> None:
        for mode in NON_VANILLA_RANDOMIZE_DAMAGE_CLASS_MODES:
            if mode == NIGHTMARE_RANDOMIZE_DAMAGE_CLASSES:
                continue
            with self.subTest(mode=mode):
                combat_model = build_randomized_damage_class_combat_model(
                    random.Random(5),
                    mode,
                    enemy_health_key="hard",
                    available_damage_classes=frozenset({6, 9}),
                    swordless=True,
                )

                self.assertIsNotNone(get_hits_to_kill(
                    HELMASAUR_KING_SPRITE_ID,
                    6,
                    "hard",
                    combat_model=combat_model,
                ))
                self.assertIsNotNone(get_hits_to_kill(
                    HELMASAUR_KING_SPRITE_ID,
                    9,
                    "hard",
                    combat_model=combat_model,
                ))

    def test_randomized_damage_classes_guarantee_swordless_ganon_d7_delivery_classes(self) -> None:
        for mode in NON_VANILLA_RANDOMIZE_DAMAGE_CLASS_MODES:
            if mode == NIGHTMARE_RANDOMIZE_DAMAGE_CLASSES:
                continue
            with self.subTest(mode=mode, damage_classes="hammer"):
                combat_model = build_randomized_damage_class_combat_model(
                    random.Random(6),
                    mode,
                    enemy_health_key="hard",
                    available_damage_classes=frozenset({1, 3}),
                    swordless=True,
                )
                self.assertIsNotNone(get_hits_to_kill(
                    GANON_D7_SPRITE_ID,
                    3,
                    "hard",
                    hp_override=0x60,
                    combat_model=combat_model,
                ))

            with self.subTest(mode=mode, damage_classes="boomerang"):
                combat_model = build_randomized_damage_class_combat_model(
                    random.Random(6),
                    mode,
                    enemy_health_key="hard",
                    available_damage_classes=frozenset({0, 1}),
                    swordless=True,
                )
                self.assertIsNotNone(get_hits_to_kill(
                    GANON_D7_SPRITE_ID,
                    0,
                    "hard",
                    hp_override=0x60,
                    combat_model=combat_model,
                ))

    def test_randomized_damage_classes_preserve_all_zero_profiles(self) -> None:
        all_zero_sprite_ids = tuple(
            sprite_id
            for sprite_id in range(len(VANILLA_COMBAT_MODEL.sprite_damage_subclasses))
            if not has_vanilla_damage_profile(sprite_id)
        )
        self.assertIn(SPIKE_BLOCK_SPRITE_ID, all_zero_sprite_ids)

        for mode in NON_VANILLA_RANDOMIZE_DAMAGE_CLASS_MODES:
            with self.subTest(mode=mode):
                combat_model = build_randomized_damage_class_combat_model(random.Random(0), mode)

                for sprite_id in all_zero_sprite_ids:
                    for damage_class in range(16):
                        self.assertEqual(get_damage_effect(sprite_id, damage_class, combat_model), 0)

    def test_randomized_damage_classes_preserve_lost_sword_class_2(self) -> None:
        for mode in NON_VANILLA_RANDOMIZE_DAMAGE_CLASS_MODES:
            with self.subTest(mode=mode):
                combat_model = build_randomized_damage_class_combat_model(random.Random(1), mode)

                for sprite_id in range(len(combat_model.sprite_damage_subclasses)):
                    if (
                        sprite_id in EXCLUDED_ENEMY_TABLE_SPRITE_IDS
                        or sprite_id in BOSS_DAMAGE_CLASS_RANDOMIZER_SPRITE_IDS
                        or (
                            VANILLA_COMBAT_MODEL.enemy_health_table[sprite_id] == 0xFF
                            and sprite_id not in DAMAGE_CLASS_RANDOMIZER_HP_255_INCLUDED_SPRITE_IDS
                        )
                        or not has_vanilla_damage_profile(sprite_id)
                    ):
                        continue
                    class_2_effect = get_damage_effect(
                        sprite_id,
                        LOST_SWORD_UPGRADE_DAMAGE_CLASS,
                        combat_model,
                    )
                    if class_2_effect == 0:
                        continue
                    replacement_effects = [
                        get_damage_effect(sprite_id, damage_class, combat_model)
                        for damage_class in SWORD_CLASS_2_REPLACEMENT_DAMAGE_CLASSES
                    ]
                    if class_2_effect >= FAIRY_TRANSFORM_EFFECT:
                        self.assertIn(class_2_effect, replacement_effects)
                    else:
                        self.assertTrue(
                            any(0 < effect < FAIRY_TRANSFORM_EFFECT and effect >= class_2_effect
                                for effect in replacement_effects)
                        )

    def test_sword_beam_damage_class_is_retained_after_sword_upgrades(self) -> None:
        self.assertNotEqual(SWORD_BEAM_DAMAGE_CLASS, LOST_SWORD_UPGRADE_DAMAGE_CLASS)
        self.assertIn(SWORD_BEAM_DAMAGE_CLASS, FIGHTER_SWORD_DAMAGE_CLASSES)
        self.assertIn(SWORD_BEAM_DAMAGE_CLASS, MASTER_SWORD_DAMAGE_CLASSES)
        self.assertIn(SWORD_BEAM_DAMAGE_CLASS, TEMPERED_SWORD_DAMAGE_CLASSES)
        self.assertIn(SWORD_BEAM_DAMAGE_CLASS, GOLDEN_SWORD_DAMAGE_CLASSES)

    def test_damage_class_swap_globally_permutates_eligible_columns(self) -> None:
        rows = [
            list(range(16)),
            list(range(0x10, 0x20)),
            [0xEE] * 16,
        ]
        permutation = tuple(reversed(range(16)))

        swapped_rows = _swap_damage_class_effects(rows, (0, 1), permutation)

        self.assertEqual(swapped_rows[0], list(reversed(range(16))))
        self.assertEqual(swapped_rows[1], list(reversed(range(0x10, 0x20))))
        self.assertEqual(swapped_rows[2], [0xEE] * 16)

    def test_randomized_damage_classes_include_selected_hp_255_enemies(self) -> None:
        combat_model = build_randomized_damage_class_combat_model(random.Random(2), CHAOS_RANDOMIZE_DAMAGE_CLASSES)

        for sprite_id in (ANTI_FAIRY_SPRITE_ID, DEADROCK_SPRITE_ID):
            with self.subTest(sprite_id=sprite_id):
                vanilla_effects = tuple(get_damage_effect(sprite_id, damage_class) for damage_class in range(16))
                randomized_effects = tuple(
                    get_damage_effect(sprite_id, damage_class, combat_model)
                    for damage_class in range(16)
                )
                self.assertNotEqual(vanilla_effects, randomized_effects)

    def test_randomized_damage_classes_guarantee_capped_direct_kill(self) -> None:
        for mode in NON_VANILLA_RANDOMIZE_DAMAGE_CLASS_MODES:
            with self.subTest(mode=mode):
                combat_model = build_randomized_damage_class_combat_model(
                    random.Random(3),
                    mode,
                    max_attacks_in_logic=4,
                )

                for sprite_id in range(len(combat_model.sprite_damage_subclasses)):
                    if (
                        sprite_id in EXCLUDED_ENEMY_TABLE_SPRITE_IDS
                        or sprite_id in BOSS_DAMAGE_CLASS_RANDOMIZER_SPRITE_IDS
                        or (
                            VANILLA_COMBAT_MODEL.enemy_health_table[sprite_id] == 0xFF
                            and sprite_id not in DAMAGE_CLASS_RANDOMIZER_HP_255_INCLUDED_SPRITE_IDS
                        )
                        or not has_vanilla_damage_profile(sprite_id)
                    ):
                        continue
                    with self.subTest(mode=mode, sprite_id=sprite_id):
                        hp = get_enemy_health_for_logic(sprite_id, "default", combat_model=combat_model)
                        self.assertIsNotNone(hp)
                        hit_counts = tuple(
                            hit_count
                            for damage_class in range(16)
                            if (
                                hit_count := get_hits_to_kill(
                                    sprite_id,
                                    damage_class,
                                    "default",
                                    combat_model=combat_model,
                                )
                            ) is not None
                        )
                        self.assertTrue(any(hit_count <= 4 for hit_count in hit_counts))

                self.assertTrue(get_incinerating_damage_classes(RED_BARI_SPRITE_ID, combat_model))

    def test_nightmare_damage_classes_have_exactly_one_defeating_class(self) -> None:
        combat_model = build_randomized_damage_class_combat_model(
            random.Random(9),
            NIGHTMARE_RANDOMIZE_DAMAGE_CLASSES,
            max_attacks_in_logic=4,
        )

        for sprite_id in range(len(combat_model.sprite_damage_subclasses)):
            if (
                sprite_id in EXCLUDED_ENEMY_TABLE_SPRITE_IDS
                or (
                    VANILLA_COMBAT_MODEL.enemy_health_table[sprite_id] == 0xFF
                    and sprite_id not in DAMAGE_CLASS_RANDOMIZER_HP_255_INCLUDED_SPRITE_IDS
                )
                or not has_vanilla_damage_profile(sprite_id)
            ):
                continue
            with self.subTest(sprite_id=sprite_id):
                defeat_classes = tuple(
                    damage_class
                    for damage_class in range(16)
                    if is_defeating_damage_effect_for_nightmare(
                        get_damage_effect(sprite_id, damage_class, combat_model)
                    )
                )
                if LOST_SWORD_UPGRADE_DAMAGE_CLASS in defeat_classes:
                    self.assertIn(GOLDEN_SWORD_SPIN_DAMAGE_CLASS, defeat_classes)
                    self.assertEqual(
                        get_damage_effect(sprite_id, LOST_SWORD_UPGRADE_DAMAGE_CLASS, combat_model),
                        get_damage_effect(sprite_id, GOLDEN_SWORD_SPIN_DAMAGE_CLASS, combat_model),
                    )
                    self.assertEqual(set(defeat_classes), {LOST_SWORD_UPGRADE_DAMAGE_CLASS, GOLDEN_SWORD_SPIN_DAMAGE_CLASS})
                else:
                    self.assertEqual(len(defeat_classes), 1)

    def test_randomized_damage_classes_change_non_boss_rows(self) -> None:
        vanilla_effects = {
            (sprite_id, damage_class): get_damage_effect(sprite_id, damage_class)
            for sprite_id in range(len(VANILLA_COMBAT_MODEL.sprite_damage_subclasses))
            if sprite_id not in EXCLUDED_ENEMY_TABLE_SPRITE_IDS
            for damage_class in range(16)
        }

        for mode in NON_VANILLA_RANDOMIZE_DAMAGE_CLASS_MODES:
            with self.subTest(mode=mode):
                combat_model = build_randomized_damage_class_combat_model(random.Random(2), mode)
                changed = any(
                    get_damage_effect(sprite_id, damage_class, combat_model) != effect
                    for (sprite_id, damage_class), effect in vanilla_effects.items()
                )
                self.assertTrue(changed)

    def test_enemy_shuffle_enables_hidden_enemy_and_mimic_support(self) -> None:
        rom = FakeRom()
        world = self._build_world(enemy_shuffle=True, bush_shuffle=False)

        self._apply_native_enemizer_features(world, rom)

        self.assertEqual(
            tuple(rom.read_bytes(HIDDEN_ENEMY_CHANCE_POOL_ADDRESS, len(VANILLA_HIDDEN_ENEMY_CHANCE_POOL))),
            VANILLA_HIDDEN_ENEMY_CHANCE_POOL,
        )
        self.assertEqual(rom.read_byte(_get_enemizer_symbol("EnemizerFlags_randomize_bushes")), 0x01)
        self.assertEqual(rom.read_byte(_get_enemizer_symbol("EnemizerFlags_randomize_sprites")), 0x01)
        self.assertEqual(rom.read_byte(_get_enemizer_symbol("EnemizerFlags_enable_mimic_override")), 0x01)
        self.assertEqual(rom.read_byte(_get_enemizer_symbol("EnemizerFlags_enable_terrorpin_ai_fix")), 0x01)
        self.assertEqual(tuple(rom.read_bytes(0x1F2D5, 2)), (0x54, 0x9C))
        self.assertEqual(rom.read_byte(0x1F2E5), 0xB0)
        self.assertEqual(rom.read_byte(0x1F2EB), 0xD0)

    def test_bush_shuffle_and_remaining_tables_are_patched_natively(self) -> None:
        rom = FakeRom()
        item_table_address = _get_enemizer_symbol("sprite_bush_spawn_item_table")
        not_item_sprite_address = _get_enemizer_symbol("notItemSprite_Mimic")
        rom.write_byte(RETRO_ARROW_REPLACEMENT_CHECK_ADDRESS, RETRO_RUPEE_REPLACEMENT_SPRITE_ID)
        rom.write_byte(item_table_address + 5, ARROW_REFILL_5_SPRITE_ID)
        rom.write_byte(ENEMY_HP_TABLE_ADDRESS + THIEF_SPRITE_ID, 0x08)

        included_hp_sprite_id = 0x01
        included_damage_sprite_id = 0x02
        boss_damage_sprite_id = 0x53
        excluded_sprite_id = min(EXCLUDED_ENEMY_TABLE_SPRITE_IDS)
        rom.write_byte(ENEMY_HP_TABLE_ADDRESS + included_hp_sprite_id, 0x06)
        rom.write_byte(ENEMY_HP_TABLE_ADDRESS + excluded_sprite_id, 0x07)
        rom.write_byte(ENEMY_DAMAGE_TABLE_ADDRESS + included_damage_sprite_id, 0x86)
        rom.write_byte(ENEMY_DAMAGE_TABLE_ADDRESS + boss_damage_sprite_id, 0x17)
        rom.write_byte(ENEMY_DAMAGE_TABLE_ADDRESS + excluded_sprite_id, 0x05)

        world = self._build_world(
            bush_shuffle=True,
            killable_thieves=True,
            enemy_health="hard",
            enemy_damage="chaos",
        )

        self._apply_native_enemizer_features(world, rom)

        self.assertEqual(
            tuple(rom.read_bytes(HIDDEN_ENEMY_CHANCE_POOL_ADDRESS, len(RANDOMIZED_HIDDEN_ENEMY_CHANCE_POOL))),
            RANDOMIZED_HIDDEN_ENEMY_CHANCE_POOL,
        )
        self.assertEqual(rom.read_byte(item_table_address + 5), RETRO_RUPEE_REPLACEMENT_SPRITE_ID)
        self.assertEqual(rom.read_byte(not_item_sprite_address + 4), THIEF_SPRITE_ID)
        self.assertNotEqual(rom.read_byte(ENEMY_HP_TABLE_ADDRESS + THIEF_SPRITE_ID), 0x08)
        self.assertGreaterEqual(rom.read_byte(ENEMY_HP_TABLE_ADDRESS + THIEF_SPRITE_ID), 2)
        self.assertLess(rom.read_byte(ENEMY_HP_TABLE_ADDRESS + THIEF_SPRITE_ID), 25)
        self.assertGreaterEqual(rom.read_byte(ENEMY_HP_TABLE_ADDRESS + included_hp_sprite_id), 2)
        self.assertLess(rom.read_byte(ENEMY_HP_TABLE_ADDRESS + included_hp_sprite_id), 25)
        self.assertEqual(rom.read_byte(ENEMY_HP_TABLE_ADDRESS + excluded_sprite_id), 0x07)
        red_hardhat_hp, blue_hardhat_hp = rom.read_bytes(HARDHAT_BEETLE_HP_TABLE_ADDRESS, 2)
        self.assertGreaterEqual(red_hardhat_hp, 2)
        self.assertLess(red_hardhat_hp, 25)
        self.assertGreaterEqual(blue_hardhat_hp, 2)
        self.assertLess(blue_hardhat_hp, 25)
        randomized_damage = rom.read_byte(ENEMY_DAMAGE_TABLE_ADDRESS + included_damage_sprite_id)
        self.assertEqual(randomized_damage & 0xF0, 0x80)
        self.assertIn(randomized_damage & 0x0F, range(8))
        randomized_boss_damage = rom.read_byte(ENEMY_DAMAGE_TABLE_ADDRESS + boss_damage_sprite_id)
        self.assertEqual(randomized_boss_damage & 0x10, 0x10)
        self.assertIn(randomized_boss_damage & 0x0F, range(8))
        self.assertEqual(rom.read_byte(ENEMY_DAMAGE_TABLE_ADDRESS + excluded_sprite_id), 0x05)
        for group_id in range(10):
            group_address = DAMAGE_GROUP_TABLE_ADDRESS + (group_id * 3)
            green_mail, blue_mail, red_mail = rom.read_bytes(group_address, 3)
            self.assertIn(green_mail, range(64))
            self.assertIn(blue_mail, range(64))
            self.assertIn(red_mail, range(64))

    def test_enemy_damage_randomizer_supports_token_only_roms(self) -> None:
        rom = FakeTokenRom()

        _randomize_enemy_damage(rom, random.Random(0), allow_zero_damage=True)

        randomized_damage = rom.read_byte(ENEMY_DAMAGE_TABLE_ADDRESS + 0x02)
        self.assertEqual(randomized_damage & 0xF0, 0x80)
        self.assertIn(randomized_damage & 0x0F, range(8))
        randomized_boss_damage = rom.read_byte(ENEMY_DAMAGE_TABLE_ADDRESS + 0x53)
        self.assertEqual(randomized_boss_damage & 0x10, 0x10)
        self.assertIn(randomized_boss_damage & 0x0F, range(8))

    def test_enemy_health_randomizer_does_not_corrupt_sprite_prep_helper(self) -> None:
        rom = FakeRom()
        move_down_helper_jsr_address = 0x31117
        rom.write_bytes(move_down_helper_jsr_address, (0x20, 0xD3, 0x90))
        rom.write_bytes(HARDHAT_BEETLE_HP_TABLE_ADDRESS, (0x20, 0x06))

        _randomize_enemy_health(rom, random.Random(0), "hard")

        self.assertEqual(tuple(rom.read_bytes(move_down_helper_jsr_address, 3)), (0x20, 0xD3, 0x90))
        red_hardhat_hp, blue_hardhat_hp = rom.read_bytes(HARDHAT_BEETLE_HP_TABLE_ADDRESS, 2)
        self.assertGreaterEqual(red_hardhat_hp, 2)
        self.assertLess(red_hardhat_hp, 25)
        self.assertGreaterEqual(blue_hardhat_hp, 2)
        self.assertLess(blue_hardhat_hp, 25)

    def test_killable_thief_sets_default_hp_without_enemy_health_shuffle(self) -> None:
        rom = FakeRom()
        rom.write_byte(ENEMY_HP_TABLE_ADDRESS + THIEF_SPRITE_ID, 0x08)

        world = self._build_world(killable_thieves=True)

        self._apply_native_enemizer_features(world, rom)

        self.assertEqual(rom.read_byte(ENEMY_HP_TABLE_ADDRESS + THIEF_SPRITE_ID), THIEF_DEFAULT_HP)

    def test_bush_shuffle_without_enemy_shuffle_does_not_enable_sprite_randomization_flags(self) -> None:
        rom = FakeRom()

        self._apply_native_enemizer_features(self._build_world(bush_shuffle=True), rom)

        self.assertEqual(rom.read_byte(_get_enemizer_symbol("EnemizerFlags_randomize_bushes")), 0x01)
        self.assertEqual(rom.read_byte(_get_enemizer_symbol("EnemizerFlags_randomize_sprites")), 0x00)
        self.assertEqual(rom.read_byte(_get_enemizer_symbol("EnemizerFlags_enable_mimic_override")), 0x00)
        self.assertEqual(rom.read_byte(_get_enemizer_symbol("EnemizerFlags_enable_terrorpin_ai_fix")), 0x00)
        self.assertEqual(tuple(rom.read_bytes(0x1F2D5, 2)), (0x00, 0x00))
        self.assertEqual(rom.read_byte(0x1F2E5), 0x00)
        self.assertEqual(rom.read_byte(0x1F2EB), 0x00)

    def test_non_chaos_enemy_damage_uses_expected_mail_scaling(self) -> None:
        rom = FakeRom()

        self._apply_native_enemizer_features(self._build_world(enemy_damage="hard"), rom)

        for group_id in range(10):
            group_address = DAMAGE_GROUP_TABLE_ADDRESS + (group_id * 3)
            green_mail, blue_mail, red_mail = rom.read_bytes(group_address, 3)
            self.assertEqual(blue_mail, green_mail * 3 // 4)
            self.assertEqual(red_mail, green_mail * 3 // 8)

    def test_patch_bosses_overwrites_enemy_shuffle_boss_room_graphics(self) -> None:
        rom = FakeRom()
        dungeon_header_base = _get_enemizer_symbol("room_header_table")
        eastern_dungeon_data = DUNGEON_BOSS_PATCH_DATA[("Eastern Palace", None)]
        rom.write_byte(dungeon_header_base + (eastern_dungeon_data.room_id * 14) + 3, BOSS_PATCH_DATA["Armos"].graphics)

        for table_index in BOSS_GFX_SHEET_INDEXES.values():
            rom.write_byte(0x4FC0 + table_index, 0xAA)
            rom.write_byte(0x509F + table_index, 0xBB)
            rom.write_byte(0x517E + table_index, 0xCC)

        patch_bosses(self._build_boss_world({"Eastern Palace": "Vitreous"}), rom)

        eastern_boss_data = BOSS_PATCH_DATA["Vitreous"]
        self.assertEqual(
            tuple(rom.read_bytes(eastern_dungeon_data.sprite_pointer_address, 2)),
            eastern_boss_data.pointer,
        )
        self.assertEqual(
            rom.read_byte(dungeon_header_base + (eastern_dungeon_data.room_id * 14) + 3),
            eastern_boss_data.graphics,
        )

        for table_index in BOSS_GFX_SHEET_INDEXES.values():
            self.assertEqual(rom.read_byte(0x4FC0 + table_index), 0xAA)
            self.assertEqual(rom.read_byte(0x509F + table_index), 0xBB)
            self.assertEqual(rom.read_byte(0x517E + table_index), 0xCC)

    def test_patch_bosses_supports_token_only_roms(self) -> None:
        rom = FakeTokenRom()
        dungeon_header_base = _get_enemizer_symbol("room_header_table")
        moved_room_object_base = _get_enemizer_symbol("modified_room_object_table")
        eastern_dungeon_data = DUNGEON_BOSS_PATCH_DATA[("Eastern Palace", None)]
        turtle_rock_dungeon_data = DUNGEON_BOSS_PATCH_DATA[("Turtle Rock", None)]

        patch_bosses(self._build_boss_world({
            "Eastern Palace": "Trinexx",
            "Turtle Rock": "Armos",
        }), rom)

        self.assertEqual(
            (rom.read_byte(eastern_dungeon_data.sprite_pointer_address),
             rom.read_byte(eastern_dungeon_data.sprite_pointer_address + 1)),
            BOSS_PATCH_DATA["Trinexx"].pointer,
        )
        self.assertEqual(
            rom.read_byte(dungeon_header_base + (eastern_dungeon_data.room_id * 14) + 3),
            BOSS_PATCH_DATA["Trinexx"].graphics,
        )
        self.assertIn(moved_room_object_base, rom.bytes)
        self.assertIn(moved_room_object_base + 1, rom.bytes)
        self.assertIn(0xF8000 + (eastern_dungeon_data.room_id * 3), rom.bytes)
        self.assertIn(0xF8000 + (turtle_rock_dungeon_data.room_id * 3), rom.bytes)

    def test_native_enemizer_rng_is_deterministic_for_same_world_settings(self) -> None:
        world = self._build_world(enemy_health="hard", enemy_damage="chaos", bush_shuffle=True)

        rng_a = _make_native_enemizer_rng(world)
        rng_b = _make_native_enemizer_rng(world)

        self.assertEqual([rng_a.randrange(256) for _ in range(8)], [rng_b.randrange(256) for _ in range(8)])

    @staticmethod
    def _apply_native_enemizer_features(world: SimpleNamespace, rom: FakeRom) -> None:
        enemy_shuffle_enabled = bool(world.options.enemy_shuffle)
        bush_shuffle_enabled = bool(world.options.bush_shuffle)
        enemy_health_key = _option_key(world.options.enemy_health)
        enemy_damage_key = _option_key(world.options.enemy_damage)

        if enemy_shuffle_enabled or bush_shuffle_enabled:
            _set_enemizer_flag(rom, "EnemizerFlags_randomize_bushes", True)
            hidden_enemy_chance_pool = (
                RANDOMIZED_HIDDEN_ENEMY_CHANCE_POOL if bush_shuffle_enabled else VANILLA_HIDDEN_ENEMY_CHANCE_POOL
            )
            rom.write_bytes(HIDDEN_ENEMY_CHANCE_POOL_ADDRESS, hidden_enemy_chance_pool)
            _update_hidden_enemy_item_table_for_retro_mode(rom)

        if enemy_shuffle_enabled:
            _set_enemizer_flag(rom, "EnemizerFlags_randomize_sprites", True)
            _set_enemizer_flag(rom, "EnemizerFlags_enable_mimic_override", True)
            _set_enemizer_flag(rom, "EnemizerFlags_enable_terrorpin_ai_fix", True)
            rom.write_bytes(0x1F2D5, (0x54, 0x9C))
            rom.write_byte(0x1F2E5, 0xB0)
            rom.write_byte(0x1F2EB, 0xD0)

        if world.options.killable_thieves:
            _apply_killable_thief(rom)

        if enemy_health_key != "default" or enemy_damage_key != "default":
            rng = _make_native_enemizer_rng(world)
        else:
            rng = None

        if enemy_health_key != "default":
            assert rng is not None
            _randomize_enemy_health(rom, rng, enemy_health_key)

        if enemy_damage_key != "default":
            assert rng is not None
            _randomize_enemy_damage(rom, rng, allow_zero_damage=True)
            _shuffle_damage_groups(rom, rng, chaos_mode=enemy_damage_key == "chaos", allow_zero_damage=True)

    @staticmethod
    def _build_world(
        *,
        enemy_shuffle: bool = False,
        bush_shuffle: bool = False,
        killable_thieves: bool = False,
        enemy_health: str = "default",
        enemy_damage: str = "default",
        randomize_damage_classes: str = "vanilla",
        max_attacks_in_logic: int = 16,
    ) -> SimpleNamespace:
        return SimpleNamespace(
            player=1,
            multiworld=SimpleNamespace(seed=12345, seed_name="native-enemizer-test"),
            options=SimpleNamespace(
                enemy_shuffle=enemy_shuffle,
                bush_shuffle=bush_shuffle,
                killable_thieves=killable_thieves,
                enemy_health=SimpleNamespace(current_key=enemy_health),
                enemy_damage=SimpleNamespace(current_key=enemy_damage),
                randomize_damage_classes=SimpleNamespace(current_key=randomize_damage_classes),
                max_attacks_in_logic=SimpleNamespace(value=max_attacks_in_logic),
            ),
        )

    @staticmethod
    def _build_boss_world(boss_overrides: dict[str, str] | None = None) -> SimpleNamespace:
        boss_overrides = boss_overrides or {}

        def boss(name: str) -> SimpleNamespace:
            return SimpleNamespace(enemizer_name=name)

        return SimpleNamespace(
            options=SimpleNamespace(mode="open"),
            dungeons={
                "Eastern Palace": SimpleNamespace(boss=boss(boss_overrides.get("Eastern Palace", "Armos"))),
                "Desert Palace": SimpleNamespace(boss=boss(boss_overrides.get("Desert Palace", "Lanmola"))),
                "Tower of Hera": SimpleNamespace(boss=boss(boss_overrides.get("Tower of Hera", "Moldorm"))),
                "Palace of Darkness": SimpleNamespace(boss=boss(boss_overrides.get("Palace of Darkness", "Helmasaur"))),
                "Swamp Palace": SimpleNamespace(boss=boss(boss_overrides.get("Swamp Palace", "Arrghus"))),
                "Skull Woods": SimpleNamespace(boss=boss(boss_overrides.get("Skull Woods", "Mothula"))),
                "Thieves Town": SimpleNamespace(boss=boss(boss_overrides.get("Thieves Town", "Blind"))),
                "Ice Palace": SimpleNamespace(boss=boss(boss_overrides.get("Ice Palace", "Kholdstare"))),
                "Misery Mire": SimpleNamespace(boss=boss(boss_overrides.get("Misery Mire", "Vitreous"))),
                "Turtle Rock": SimpleNamespace(boss=boss(boss_overrides.get("Turtle Rock", "Trinexx"))),
                "Ganons Tower": SimpleNamespace(
                    bosses={
                        "bottom": boss(boss_overrides.get("Ganons Tower Bottom", "Armos")),
                        "middle": boss(boss_overrides.get("Ganons Tower Middle", "Lanmola")),
                        "top": boss(boss_overrides.get("Ganons Tower Top", "Moldorm")),
                    }
                ),
            },
        )


if __name__ == "__main__":
    unittest.main()
