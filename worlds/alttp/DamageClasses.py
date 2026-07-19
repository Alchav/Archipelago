from __future__ import annotations

from collections import Counter
from typing import TYPE_CHECKING

from .Bosses import get_gt_only_boss_damage_class_sprite_ids
from .enemizer_data.enemy_combat_data import (
    EnemyCombatModel,
    FIGHTER_SWORD_DAMAGE_CLASSES,
    GOLDEN_SWORD_DAMAGE_CLASSES,
    MASTER_SWORD_DAMAGE_CLASSES,
    TEMPERED_SWORD_DAMAGE_CLASSES,
    VANILLA_COMBAT_MODEL,
    VANILLA_RANDOMIZE_DAMAGE_CLASSES,
    build_randomized_damage_class_combat_model,
)

if TYPE_CHECKING:
    from . import ALTTPWorld


STANDARD_ESCAPE_DAMAGE_ROW_SPRITE_IDS = frozenset((0x41, 0x42, 0x6A, 0x6D, 0x6F))


def with_vanilla_standard_escape_damage_rows(combat_model: EnemyCombatModel) -> EnemyCombatModel:
    sprite_damage_subclasses = [tuple(row) for row in combat_model.sprite_damage_subclasses]
    for sprite_id in STANDARD_ESCAPE_DAMAGE_ROW_SPRITE_IDS:
        sprite_damage_subclasses[sprite_id] = VANILLA_COMBAT_MODEL.sprite_damage_subclasses[sprite_id]
    return EnemyCombatModel(
        damage_sources=combat_model.damage_sources,
        sprite_damage_subclasses=tuple(sprite_damage_subclasses),
        enemy_health_table=combat_model.enemy_health_table,
        gt_only_boss_special_allowed_sprite_ids=combat_model.gt_only_boss_special_allowed_sprite_ids,
    )


def get_enemy_shuffle_available_damage_classes(world: "ALTTPWorld", item_names) -> frozenset[int]:
    item_counts = Counter(item_names)
    damage_classes: set[int] = set()

    def has_item(item_name: str) -> bool:
        return item_counts[item_name] > 0

    progressive_sword_count = min(
        item_counts["Progressive Sword"],
        world.difficulty_requirements.progressive_sword_limit,
    )
    if has_item("Fighter Sword") or progressive_sword_count >= 1:
        damage_classes.update(FIGHTER_SWORD_DAMAGE_CLASSES)
    if has_item("Master Sword") or progressive_sword_count >= 2:
        damage_classes.update(MASTER_SWORD_DAMAGE_CLASSES)
    if has_item("Tempered Sword") or progressive_sword_count >= 3:
        damage_classes.update(TEMPERED_SWORD_DAMAGE_CLASSES)
    if has_item("Golden Sword") or progressive_sword_count >= 4:
        damage_classes.update(GOLDEN_SWORD_DAMAGE_CLASSES)

    if has_item("Hammer"):
        damage_classes.add(3)
    if has_item("Blue Boomerang") or has_item("Red Boomerang"):
        damage_classes.add(0)
    if has_item("Hookshot"):
        damage_classes.add(7)
    if has_item("Cane of Somaria") or has_item("Cane of Byrna"):
        damage_classes.add(1)
    if has_item("Magic Powder"):
        damage_classes.add(10)
    if has_item("Fire Rod"):
        damage_classes.add(11)
    if has_item("Ice Rod"):
        damage_classes.add(12)
    if has_item("Bombos"):
        damage_classes.add(13)
    if has_item("Ether"):
        damage_classes.add(14)
    if has_item("Quake"):
        damage_classes.add(15)

    if (
        not world.options.bombless_start
        or has_item("Bomb Upgrade (+5)")
        or has_item("Bomb Upgrade (+10)")
        or has_item("Bomb Upgrade (50)")
        or (
            not world.options.shuffle_capacity_upgrades
            and has_item("Capacity Upgrade Shop")
        )
    ):
        damage_classes.add(8)

    progressive_bow_count = min(
        item_counts["Progressive Bow"] + item_counts["Progressive Bow (Alt)"],
        world.difficulty_requirements.progressive_bow_limit,
    )
    has_bow = has_item("Bow") or has_item("Silver Bow") or progressive_bow_count >= 1
    if has_bow:
        damage_classes.add(6)
    if has_item("Silver Bow") or progressive_bow_count >= 2 or (has_bow and has_item("Silver Arrows")):
        damage_classes.add(9)

    return frozenset(damage_classes)


def get_enemy_shuffle_available_damage_delivery_context(
    world: "ALTTPWorld",
    item_names,
) -> tuple[frozenset[str], frozenset[str]]:
    item_counts = Counter(item_names)
    items: set[str] = set()
    abilities: set[str] = set()

    def has_item(item_name: str) -> bool:
        return item_counts[item_name] > 0

    progressive_sword_count = min(
        item_counts["Progressive Sword"],
        world.difficulty_requirements.progressive_sword_limit,
    )
    has_fighter_sword = has_item("Fighter Sword") or progressive_sword_count >= 1
    has_master_sword = has_item("Master Sword") or progressive_sword_count >= 2
    has_tempered_sword = has_item("Tempered Sword") or progressive_sword_count >= 3
    has_golden_sword = has_item("Golden Sword") or progressive_sword_count >= 4
    if has_fighter_sword:
        items.add("Fighter Sword")
    if has_master_sword:
        items.add("Master Sword")
        abilities.add("sword_beams")
    if has_tempered_sword:
        items.add("Tempered Sword")
        abilities.add("sword_beams")
    if has_golden_sword:
        items.add("Golden Sword")
        abilities.add("sword_beams")

    for item_name in (
        "Hammer",
        "Blue Boomerang",
        "Red Boomerang",
        "Hookshot",
        "Cane of Somaria",
        "Cane of Byrna",
        "Magic Powder",
        "Fire Rod",
        "Ice Rod",
        "Bombos",
        "Ether",
        "Quake",
    ):
        if has_item(item_name):
            items.add(item_name)

    if (
        not world.options.bombless_start
        or has_item("Bomb Upgrade (+5)")
        or has_item("Bomb Upgrade (+10)")
        or has_item("Bomb Upgrade (50)")
        or (
            not world.options.shuffle_capacity_upgrades
            and has_item("Capacity Upgrade Shop")
        )
    ):
        abilities.add("bombs")

    progressive_bow_count = min(
        item_counts["Progressive Bow"] + item_counts["Progressive Bow (Alt)"],
        world.difficulty_requirements.progressive_bow_limit,
    )
    has_bow = has_item("Bow") or has_item("Silver Bow") or progressive_bow_count >= 1
    if has_bow:
        items.add("Bow")
    if has_item("Silver Bow") or progressive_bow_count >= 2 or (has_bow and has_item("Silver Arrows")):
        items.add("Silver Bow")

    return frozenset(items), frozenset(abilities)


def set_enemy_combat_model(world: "ALTTPWorld", item_names=None) -> None:
    if getattr(world, "ut_replay_data", None):
        from . import _decode_ut_enemy_combat_model, _get_ut_replay_value

        enemy_combat_model = _get_ut_replay_value(world.ut_replay_data, "ut_enemy_combat_model", "enemy_combat_model")
        if enemy_combat_model is not None:
            world.enemy_combat_model = _decode_ut_enemy_combat_model(enemy_combat_model)
            return

    damage_class_mode = world.options.randomize_damage_classes.current_key
    if damage_class_mode == VANILLA_RANDOMIZE_DAMAGE_CLASSES:
        world.enemy_combat_model = VANILLA_COMBAT_MODEL
    else:
        item_pool_damage_classes = (
            get_enemy_shuffle_available_damage_classes(world, item_names)
            if item_names is not None
            else None
        )
        world.enemy_combat_model = build_randomized_damage_class_combat_model(
            world.random,
            damage_class_mode,
            max_attacks_in_logic=world.options.max_attacks_in_logic.value,
            enemy_health_key=world.options.enemy_health.current_key,
            item_pool_key=getattr(getattr(world.options, "item_pool", None), "current_key", "normal"),
            available_damage_classes=item_pool_damage_classes,
            hammer_available_for_freeze=True,
            swordless=bool(getattr(world.options, "swordless", False)),
            allow_swordless_medallion_damage=world.options.item_functionality == "easy",
            killable_thieves=bool(getattr(world.options, "killable_thieves", False)),
            enemy_shuffle=bool(getattr(world.options, "enemy_shuffle", False)),
            preserve_melee_damage_classes=bool(getattr(world.options, "preserve_melee_damage_classes", False)),
            gt_only_boss_special_allowed_sprite_ids=get_gt_only_boss_damage_class_sprite_ids(world),
        )
