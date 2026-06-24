from typing import NamedTuple

from .SubClasses import LTTPRegion
from .enemizer_data.enemy_combat_data import (
    BLOB_TRANSFORM_EFFECT,
    DAMAGE_CLASS_RANDOMIZER_HP_255_INCLUDED_SPRITE_IDS,
    DIRECT_KILL_DELIVERY_OVERRIDES,
    EnemyCombatModel,
    FAIRY_TRANSFORM_EFFECT,
    FIGHTER_SWORD_DAMAGE_CLASSES,
    FREEZE_EFFECT,
    GOLDEN_SWORD_DAMAGE_CLASSES,
    KEY_DROP_KILL_DAMAGE_CLASS_OVERRIDES,
    MASTER_SWORD_DAMAGE_CLASSES,
    SWORD_BEAM_DAMAGE_CLASS,
    STUN_255_FRAMES_EFFECT,
    TEMPERED_SWORD_DAMAGE_CLASSES,
    VANILLA_COMBAT_MODEL,
    YELLOW_SLIME_SPRITE_ID,
    get_blob_transform_damage_classes,
    get_damage_classes_with_effects,
    get_damage_effect,
    get_hardcoded_enemy_hp,
    get_hits_to_kill,
    get_killing_damage_classes,
    get_yellow_slime_follow_up_delivery_override,
    is_killing_damage_effect,
)
from BaseClasses import CollectionState


BUZZBLOB_DISABLE_EFFECTS = frozenset((FREEZE_EFFECT, STUN_255_FRAMES_EFFECT))
BUZZBLOB_FOLLOW_UP_ITEMS = (
    "Fighter Sword",
    "Master Sword",
    "Tempered Sword",
    "Golden Sword",
    "Hammer",
)
BUZZBLOB_DISABLE_ITEMS = (
    "Blue Boomerang",
    "Red Boomerang",
    "Hookshot",
    "Cane of Somaria",
    "Cane of Byrna",
    "Golden Sword",
    "Bow",
    "Silver Bow",
    "Magic Powder",
    "Fire Rod",
    "Ice Rod",
)
BUZZBLOB_DISABLE_ABILITIES = ("bombs",)


def is_not_bunny(state: CollectionState, region: LTTPRegion, player: int) -> bool:
    if state.has('Moon Pearl', player):
        return True

    return region.is_light_world if state.multiworld.worlds[player].options.mode != 'inverted' else region.is_dark_world


def can_bomb_clip(state: CollectionState, region: LTTPRegion, player: int) -> bool:
    return can_use_bombs(state, player) and is_not_bunny(state, region, player) and state.has('Pegasus Boots', player)


def can_buy_unlimited(state: CollectionState, item: str, player: int) -> bool:
    return any(shop.has_unlimited(item) and shop.region.can_reach(state) for
               shop in state.multiworld.worlds[player].shops)


def can_buy(state: CollectionState, item: str, player: int) -> bool:
    return any(shop.has(item) and shop.region.can_reach(state) for
               shop in state.multiworld.worlds[player].shops)


def can_shoot_arrows(state: CollectionState, player: int, count: int = 0) -> bool:
    if state.multiworld.worlds[player].options.retro_bow:
        return (state.has('Bow', player) or state.has('Silver Bow', player)) and can_buy(state, 'Single Arrow', player)
    return (state.has('Bow', player) or state.has('Silver Bow', player)) and can_hold_arrows(state, player, count)


def has_triforce_pieces(state: CollectionState, player: int) -> bool:
    count = state.multiworld.worlds[player].treasure_hunt_required
    return state.count('Triforce Piece', player) + state.count('Power Star', player) >= count


def has_crystals(state: CollectionState, count: int, player: int) -> bool:
    found = state.count_group("Crystals", player)
    return found >= count


def can_lift_rocks(state: CollectionState, player: int):
    return state.has('Power Glove', player) or state.has('Titans Mitts', player)


def can_lift_heavy_rocks(state: CollectionState, player: int) -> bool:
    return state.has('Titans Mitts', player)


def bottle_count(state: CollectionState, player: int) -> int:
    return min(state.multiworld.worlds[player].difficulty_requirements.progressive_bottle_limit,
               state.count_group("Bottles", player))


def has_hearts(state: CollectionState, player: int, count: int) -> int:
    # Warning: This only considers items that are marked as advancement items
    return heart_count(state, player) >= count


def heart_count(state: CollectionState, player: int) -> int:
    # Warning: This only considers items that are marked as advancement items
    max_heart_pieces = state.multiworld.worlds[player].logical_heart_pieces
    max_heart_containers = state.multiworld.worlds[player].logical_heart_containers
    return min(state.count('Boss Heart Container', player), max_heart_containers) \
        + state.count('Sanctuary Heart Container', player) \
        + min(state.count('Piece of Heart', player), max_heart_pieces) // 4 \
        + 3  # starting hearts


def can_extend_magic(state: CollectionState, player: int, smallmagic: int = 16,
                     fullrefill: bool = False):  # This reflects the total magic Link has, not the total extra he has.
    return _get_available_magic_amount(state, player, fullrefill=fullrefill) >= smallmagic


def _get_available_magic_amount(
    state: CollectionState,
    player: int,
    *,
    fullrefill: bool = False,
) -> int:
    basemagic = _get_magic_meter_capacity(state, player)
    bottles = min(4, bottle_count(state, player))
    if can_buy_unlimited(state, 'Green Potion', player) or can_buy_unlimited(state, 'Blue Potion', player):
        if state.multiworld.worlds[player].options.item_functionality == 'hard' and not fullrefill:
            basemagic = basemagic + int(basemagic * 0.5 * bottles)
        elif state.multiworld.worlds[player].options.item_functionality == 'expert' and not fullrefill:
            basemagic = basemagic + int(basemagic * 0.25 * bottles)
        else:
            basemagic = basemagic + basemagic * bottles
    return basemagic


def _get_magic_meter_capacity(state: CollectionState, player: int) -> int:
    if state.has('Magic Upgrade (1/4)', player):
        return 32
    if state.has('Magic Upgrade (1/2)', player):
        return 16
    return 8


def can_hold_arrows(state: CollectionState, player: int, quantity: int):
    if quantity == 0:
        return True
    return _get_available_arrow_count(state, player) >= quantity


def _get_available_arrow_count(state: CollectionState, player: int) -> int:
    if state.multiworld.worlds[player].options.shuffle_capacity_upgrades:
        if state.has("Arrow Upgrade (70)", player):
            arrows = 70
        else:
            arrows = (30 + (state.count("Arrow Upgrade (+5)", player) * 5)
                      + (state.count("Arrow Upgrade (+10)", player) * 10))
            # Arrow Upgrade (+5) beyond the 6th gives +10
            arrows += max(0, ((state.count("Arrow Upgrade (+5)", player) - 6) * 10))
        return min(70, arrows)
    return 70 if state.has("Capacity Upgrade Shop", player) else 30


def can_use_bombs(state: CollectionState, player: int, quantity: int = 1) -> bool:
    return _get_available_bomb_count(state, player) >= min(quantity, 50)


def _get_available_bomb_count(state: CollectionState, player: int) -> int:
    bombs = 0 if state.multiworld.worlds[player].options.bombless_start else 10
    bombs += ((state.count("Bomb Upgrade (+5)", player) * 5) + (state.count("Bomb Upgrade (+10)", player) * 10)
              + (state.count("Bomb Upgrade (50)", player) * 50))
    # Bomb Upgrade (+5) beyond the 6th gives +10
    bombs += max(0, ((state.count("Bomb Upgrade (+5)", player) - 6) * 10))
    if (not state.multiworld.worlds[player].options.shuffle_capacity_upgrades) and state.has("Capacity Upgrade Shop", player):
        bombs += 40
    return min(bombs, 50)


def can_bomb_or_bonk(state: CollectionState, player: int) -> bool:
    return state.has("Pegasus Boots", player) or can_use_bombs(state, player)


def can_activate_crystal_switch(state: CollectionState, player: int) -> bool:
    return (has_melee_weapon(state, player) or can_use_bombs(state, player) or can_shoot_arrows(state, player)
            or state.has_any(["Hookshot", "Cane of Somaria", "Cane of Byrna", "Fire Rod", "Ice Rod", "Blue Boomerang",
                              "Red Boomerang"], player))


class ResourceCosts(NamedTuple):
    bombs: int = 0
    arrows: int = 0
    magic: int = 0


class ResourceBudget(NamedTuple):
    bombs: int
    arrows: int | None
    magic: int


FREE_RESOURCE_COSTS = ResourceCosts()
ENEMY_CLEAR_MAGIC_UNITS_PER_LOGIC_UNIT = 2
FIRE_ROD_MAGIC_COST = 2
ICE_ROD_MAGIC_COST = 2
MEDALLION_MAGIC_COST = 4
MAGIC_POWDER_MAGIC_COST = 1
SOMARIA_MAGIC_COST = 1
BYRNA_INITIAL_MAGIC_COST = 2
BYRNA_DRAIN_MAGIC_COST = 1
ROOM_WIDE_MEDALLION_DAMAGE_CLASSES = {
    "Bombos": 13,
    "Ether": 14,
    "Quake": 15,
}
LIGHTNING_GATE_SPRITE_ID = 0x40
LIGHTNING_GATE_MAGIC_POWDER_DAMAGE_CLASS = 10
LIGHTNING_GATE_TRANSFORM_EFFECTS = frozenset((FAIRY_TRANSFORM_EFFECT, BLOB_TRANSFORM_EFFECT))
# Evil Barrier rejects Fighter Sword and Hammer contact hits before the damage table result matters.
LIGHTNING_GATE_CONTACT_SWORD_DAMAGE_CLASSES = (
    ("Master Sword", frozenset((1, 2, 3))),
    ("Tempered Sword", frozenset((2, 3, 4))),
    ("Golden Sword", frozenset((3, 4, 5))),
)


def _add_resource_costs(left: ResourceCosts, right: ResourceCosts) -> ResourceCosts:
    return ResourceCosts(
        left.bombs + right.bombs,
        left.arrows + right.arrows,
        left.magic + right.magic,
    )


def _fits_within_resource_budget(costs: ResourceCosts, budget: ResourceBudget) -> bool:
    return (
        costs.bombs <= budget.bombs
        and (budget.arrows is None or costs.arrows <= budget.arrows)
        and costs.magic <= budget.magic
    )


def _resource_costs_dominate(left: ResourceCosts, right: ResourceCosts) -> bool:
    return (
        left.bombs <= right.bombs
        and left.arrows <= right.arrows
        and left.magic <= right.magic
    )


def can_pass_evil_barrier(state: CollectionState, player: int) -> bool:
    if state.has("Cape", player):
        return True

    combat_model = _get_active_combat_model(state, player)
    if state.has("Magic Powder", player) and _lightning_gate_damage_class_removes_barrier(
        LIGHTNING_GATE_MAGIC_POWDER_DAMAGE_CLASS,
        combat_model,
    ):
        return True

    return any(
        state.has(sword_name, player)
        and any(
            _lightning_gate_damage_class_removes_barrier(damage_class, combat_model)
            for damage_class in damage_classes
        )
        for sword_name, damage_classes in LIGHTNING_GATE_CONTACT_SWORD_DAMAGE_CLASSES
    )


def _lightning_gate_damage_class_removes_barrier(damage_class: int, combat_model: EnemyCombatModel) -> bool:
    effect = get_damage_effect(LIGHTNING_GATE_SPRITE_ID, damage_class, combat_model)
    return is_killing_damage_effect(effect) or effect in LIGHTNING_GATE_TRANSFORM_EFFECTS


def _prune_dominated_resource_costs(costs: set[ResourceCosts]) -> tuple[ResourceCosts, ...]:
    frontier: list[ResourceCosts] = []
    for candidate in sorted(costs):
        if any(_resource_costs_dominate(existing, candidate) for existing in frontier):
            continue
        frontier = [
            existing
            for existing in frontier
            if not _resource_costs_dominate(candidate, existing)
        ]
        frontier.append(candidate)
    return tuple(frontier)


def can_clear_enemy_room(state: CollectionState, player: int, room_name_or_id: str | int) -> bool:
    from .EnemyShuffle import get_effective_dungeon_room_enemies, get_room_id

    room_id = room_name_or_id if isinstance(room_name_or_id, int) else get_room_id(room_name_or_id)
    if room_id is None:
        raise ValueError(f"Unknown ALTTP room {room_name_or_id!r}")

    room_enemies = tuple(
        enemy
        for enemy in get_effective_dungeon_room_enemies(state.multiworld.worlds[player], room_id)
        if _enemy_requirement_counts_for_room_clear(enemy)
    )
    return _can_clear_enemy_requirements(state, player, room_enemies)


def can_clear_enemy_region(state: CollectionState, player: int, target_name: str) -> bool:
    from .EnemyLogicTargets import get_enemy_clear_target_enemies

    room_enemies = tuple(
        enemy
        for enemy in get_enemy_clear_target_enemies(state.multiworld.worlds[player], target_name)
        if _enemy_requirement_counts_for_room_clear(enemy)
    )
    return _can_clear_enemy_requirements(state, player, room_enemies)


def can_clear_enemy_regions(state: CollectionState, player: int, *target_names: str) -> bool:
    from .EnemyLogicTargets import get_enemy_clear_target_enemies

    enemy_groups = tuple(
        tuple(
            enemy
            for enemy in get_enemy_clear_target_enemies(state.multiworld.worlds[player], target_name)
            if _enemy_requirement_counts_for_room_clear(enemy)
        )
        for target_name in target_names
    )
    return _can_clear_enemy_requirement_groups(state, player, enemy_groups)


def can_kill_key_drop_enemy(state: CollectionState, player: int, location_name: str) -> bool:
    from .EnemyLogicTargets import get_key_drop_enemy

    enemy = get_key_drop_enemy(state.multiworld.worlds[player], location_name)
    if enemy is None or not enemy.has_key or not _enemy_requirement_can_be_killed(state, player, enemy):
        return False

    return _can_clear_enemy_requirements(state, player, (enemy,), key_drop_enemy=True)


def can_kill_enemy_sprite(state: CollectionState, player: int, sprite_name: str) -> bool:
    from .EnemyShuffle import _load_enemy_sprite_requirements

    if not hasattr(can_kill_enemy_sprite, "requirement_lookup"):
        can_kill_enemy_sprite.requirement_lookup = {
            requirement.sprite_name: requirement
            for requirement in _load_enemy_sprite_requirements()
        }

    requirement = can_kill_enemy_sprite.requirement_lookup[sprite_name]
    if not _enemy_requirement_can_be_killed(state, player, requirement):
        return False

    return _can_clear_enemy_requirements(state, player, (requirement,))


def _enemy_requirement_counts_for_room_clear(enemy_or_requirement) -> bool:
    return _get_enemy_requirement(enemy_or_requirement).killable


def _enemy_requirement_can_be_killed(state: CollectionState, player: int, requirement) -> bool:
    requirement = _get_enemy_requirement(requirement)
    if requirement.killable:
        return True

    combat_model = _get_active_combat_model(state, player)
    combat_reference_id = _get_combat_reference_id(requirement, combat_model)
    if combat_reference_id not in DAMAGE_CLASS_RANDOMIZER_HP_255_INCLUDED_SPRITE_IDS:
        return False
    return bool(_get_direct_kill_damage_classes(requirement, combat_model))


def _get_enemy_requirement(enemy_or_requirement):
    return getattr(enemy_or_requirement, "requirement", enemy_or_requirement)


def _get_enemy_hp_override(enemy_or_requirement) -> int | None:
    requirement = _get_enemy_requirement(enemy_or_requirement)
    x_coord_pixels = getattr(enemy_or_requirement, "x_coord_pixels", None)
    return get_hardcoded_enemy_hp(requirement.sprite_id, x_coord_pixels)


def _can_clear_enemy_requirements(
    state: CollectionState,
    player: int,
    room_enemies: tuple,
    *,
    key_drop_enemy: bool = False,
) -> bool:
    return _can_clear_enemy_requirement_groups(state, player, (room_enemies,), key_drop_enemy=key_drop_enemy)


def _can_clear_enemy_requirement_groups(
    state: CollectionState,
    player: int,
    enemy_groups: tuple[tuple, ...],
    *,
    key_drop_enemy: bool = False,
) -> bool:
    budget = _get_enemy_clear_resource_budget(state, player)
    group_clear_plans = tuple(
        _get_enemy_group_clear_plans(state, player, enemy_group, budget, key_drop_enemy=key_drop_enemy)
        for enemy_group in enemy_groups
    )
    return _can_execute_enemy_kill_plans(group_clear_plans, budget)


def _get_enemy_group_clear_plans(
    state: CollectionState,
    player: int,
    room_enemies: tuple,
    budget: ResourceBudget,
    *,
    key_drop_enemy: bool = False,
) -> tuple[ResourceCosts, ...]:
    if not room_enemies:
        return (FREE_RESOURCE_COSTS,)

    clear_plans: set[ResourceCosts] = set()
    available_medallions = _get_available_room_wide_medallions(state, player)
    for room_wide_medallions in _get_room_wide_medallion_cast_sets(available_medallions):
        base_costs = ResourceCosts(magic=MEDALLION_MAGIC_COST * len(room_wide_medallions))
        if not _fits_within_resource_budget(base_costs, budget):
            continue

        plans_by_enemy = tuple(
            _get_enemy_kill_plans_after_room_wide_medallions(
                state,
                player,
                requirement,
                room_wide_medallions,
                key_drop_enemy=key_drop_enemy,
            )
            for requirement in room_enemies
        )
        clear_plans.update(_get_executable_enemy_kill_costs(plans_by_enemy, budget, base_costs=base_costs))

    return _prune_dominated_resource_costs(clear_plans)


def _get_available_damage_classes(state: CollectionState, player: int, enemy_count: int) -> set[int]:
    available_damage_classes: set[int] = set()

    if state.has("Fighter Sword", player):
        available_damage_classes.update(FIGHTER_SWORD_DAMAGE_CLASSES)
    if state.has("Master Sword", player):
        available_damage_classes.update(MASTER_SWORD_DAMAGE_CLASSES)
    if state.has("Tempered Sword", player):
        available_damage_classes.update(TEMPERED_SWORD_DAMAGE_CLASSES)
    if state.has("Golden Sword", player):
        available_damage_classes.update(GOLDEN_SWORD_DAMAGE_CLASSES)
    if state.has("Hammer", player):
        available_damage_classes.add(3)
    if state.has("Blue Boomerang", player) or state.has("Red Boomerang", player):
        available_damage_classes.add(0)
    if state.has("Hookshot", player):
        available_damage_classes.add(7)
    if can_shoot_arrows(state, player, 1):
        if state.has("Bow", player):
            available_damage_classes.add(6)
        if state.has("Silver Bow", player) or (state.has("Bow", player) and state.has("Silver Arrows", player)):
            available_damage_classes.add(9)
    if can_use_bombs(state, player, 1):
        available_damage_classes.add(8)
    if state.has("Cane of Somaria", player):
        available_damage_classes.add(1)
    if state.has("Cane of Byrna", player):
        available_damage_classes.add(1)
    if state.has("Magic Powder", player):
        available_damage_classes.add(10)
    if state.has("Fire Rod", player):
        available_damage_classes.add(11)
    if state.has("Ice Rod", player):
        available_damage_classes.add(12)
    if state.has("Bombos", player) and _can_ready_medallion(state, player):
        available_damage_classes.add(13)
    if state.has("Ether", player) and _can_ready_medallion(state, player):
        available_damage_classes.add(14)
    if state.has("Quake", player) and _can_ready_medallion(state, player):
        available_damage_classes.add(15)

    return available_damage_classes


def _get_active_combat_model(state: CollectionState, player: int) -> EnemyCombatModel:
    world = state.multiworld.worlds[player]
    enemy_shuffle_state = getattr(world, "enemy_shuffle_state", None)
    combat_model = getattr(enemy_shuffle_state, "combat_model", None)
    if combat_model is None:
        combat_model = getattr(world, "enemy_combat_model", None)
    return combat_model or VANILLA_COMBAT_MODEL


def _get_combat_reference_id(requirement, combat_model: EnemyCombatModel) -> int | None:
    combat_reference_id = requirement.combat_reference_id
    if combat_reference_id is None:
        combat_reference_id = requirement.sprite_id
    if 0 <= combat_reference_id < len(combat_model.sprite_damage_subclasses):
        return combat_reference_id
    return None


def _get_direct_kill_damage_classes(requirement, combat_model: EnemyCombatModel) -> set[int]:
    requirement = _get_enemy_requirement(requirement)
    combat_reference_id = _get_combat_reference_id(requirement, combat_model)
    if combat_reference_id is None:
        return set()
    return set(get_killing_damage_classes(combat_reference_id, combat_model))


def _get_blob_transform_damage_classes(requirement, combat_model: EnemyCombatModel) -> set[int]:
    requirement = _get_enemy_requirement(requirement)
    combat_reference_id = _get_combat_reference_id(requirement, combat_model)
    if combat_reference_id is None:
        return set()
    return set(get_blob_transform_damage_classes(combat_reference_id, combat_model))


def _get_direct_kill_context(
    requirement,
    combat_model: EnemyCombatModel,
    *,
    key_drop_enemy: bool = False,
) -> tuple[set[int], object | None]:
    requirement = _get_enemy_requirement(requirement)
    direct_kill_damage_classes = _get_direct_kill_damage_classes(requirement, combat_model)
    direct_kill_delivery_override = DIRECT_KILL_DELIVERY_OVERRIDES.get(requirement.sprite_name)
    if key_drop_enemy:
        key_drop_damage_classes = KEY_DROP_KILL_DAMAGE_CLASS_OVERRIDES.get(requirement.sprite_name)
        if key_drop_damage_classes is not None:
            direct_kill_damage_classes = set(key_drop_damage_classes)
            direct_kill_delivery_override = None
    return direct_kill_damage_classes, direct_kill_delivery_override


def _get_enemy_health_key(state: CollectionState, player: int) -> str:
    enemy_health_option = state.multiworld.worlds[player].options.enemy_health
    return str(getattr(enemy_health_option, "current_key", enemy_health_option))


def _get_max_attacks_in_logic(state: CollectionState, player: int) -> int:
    option = getattr(state.multiworld.worlds[player].options, "max_attacks_in_logic", 16)
    return int(getattr(option, "value", option))


def _get_enemy_clear_resource_budget(state: CollectionState, player: int) -> ResourceBudget:
    if state.multiworld.worlds[player].options.retro_bow:
        arrows = None if can_shoot_arrows(state, player, 1) else 0
    else:
        arrows = _get_available_arrow_count(state, player) if can_shoot_arrows(state, player, 1) else 0
    return ResourceBudget(
        bombs=_get_available_bomb_count(state, player),
        arrows=arrows,
        magic=_get_enemy_clear_magic_budget(state, player),
    )


def _get_enemy_clear_magic_budget(state: CollectionState, player: int) -> int:
    meter_capacity = _get_magic_meter_capacity(state, player) * ENEMY_CLEAR_MAGIC_UNITS_PER_LOGIC_UNIT
    if can_buy_unlimited(state, 'Green Potion', player) or can_buy_unlimited(state, 'Blue Potion', player):
        return meter_capacity * (1 + min(4, bottle_count(state, player)))
    return meter_capacity


def _has_silver_arrow_attack(state: CollectionState, player: int) -> bool:
    return state.has("Silver Bow", player) or (state.has("Bow", player) and state.has("Silver Arrows", player))


def _has_sword_beam_attack(state: CollectionState, player: int) -> bool:
    return any(
        state.has(sword, player)
        for sword in ("Master Sword", "Tempered Sword", "Golden Sword")
    )


def _get_best_hit_count(
    state: CollectionState,
    player: int,
    sprite_id: int,
    damage_classes: tuple[int, ...],
    allowed_damage_classes: set[int],
    combat_model: EnemyCombatModel,
    hp_override: int | None = None,
) -> int | None:
    enemy_health_key = _get_enemy_health_key(state, player)
    killable_thieves = bool(state.multiworld.worlds[player].options.killable_thieves)
    hit_counts = [
        get_hits_to_kill(
            sprite_id,
            damage_class,
            enemy_health_key,
            hp_override=hp_override,
            killable_thieves=killable_thieves,
            combat_model=combat_model,
        )
        for damage_class in damage_classes
        if damage_class in allowed_damage_classes
    ]
    valid_hit_counts = [hit_count for hit_count in hit_counts if hit_count is not None]
    max_attacks = _get_max_attacks_in_logic(state, player)
    valid_hit_counts = [hit_count for hit_count in valid_hit_counts if hit_count <= max_attacks]
    if not valid_hit_counts:
        return None
    return min(valid_hit_counts)


def _build_attack_plans_for_damage_classes(
    state: CollectionState,
    player: int,
    sprite_id: int,
    allowed_damage_classes: set[int],
    combat_model: EnemyCombatModel,
    *,
    hp_override: int | None = None,
    allowed_items: tuple[str, ...] | None = None,
    allowed_abilities: tuple[str, ...] | None = None,
    bypass_damage_class_filter: bool = False,
) -> tuple[ResourceCosts, ...]:
    allowed_items_set = set(allowed_items) if allowed_items is not None else None
    allowed_abilities_set = set(allowed_abilities) if allowed_abilities is not None else None

    def item_allowed(item_name: str) -> bool:
        return allowed_items_set is None or item_name in allowed_items_set

    def ability_allowed(ability_name: str) -> bool:
        return allowed_abilities_set is None or ability_name in allowed_abilities_set

    plans: set[ResourceCosts] = set()

    zero_cost_damage_class_items = (
        ("Fighter Sword", FIGHTER_SWORD_DAMAGE_CLASSES, state.has("Fighter Sword", player)),
        ("Master Sword", MASTER_SWORD_DAMAGE_CLASSES, state.has("Master Sword", player)),
        ("Tempered Sword", TEMPERED_SWORD_DAMAGE_CLASSES, state.has("Tempered Sword", player)),
        ("Golden Sword", GOLDEN_SWORD_DAMAGE_CLASSES, state.has("Golden Sword", player)),
        ("Hammer", (3,), state.has("Hammer", player)),
        ("Blue Boomerang", (0,), state.has("Blue Boomerang", player)),
        ("Red Boomerang", (0,), state.has("Red Boomerang", player)),
        ("Hookshot", (7,), state.has("Hookshot", player)),
    )
    for item_name, item_damage_classes, available in zero_cost_damage_class_items:
        if available and item_allowed(item_name) and (
            bypass_damage_class_filter or allowed_damage_classes.intersection(item_damage_classes)
        ):
            hit_count = _get_best_hit_count(
                state,
                player,
                sprite_id,
                item_damage_classes,
                set(item_damage_classes) if bypass_damage_class_filter else allowed_damage_classes,
                combat_model,
                hp_override=hp_override,
            )
            if hit_count is not None:
                plans.add(FREE_RESOURCE_COSTS)

    if item_allowed("Cane of Somaria") and state.has("Cane of Somaria", player):
        hit_count = _get_best_hit_count(
            state,
            player,
            sprite_id,
            (1,),
            {1} if bypass_damage_class_filter else allowed_damage_classes,
            combat_model,
            hp_override=hp_override,
        )
        if hit_count is not None:
            plans.add(ResourceCosts(magic=SOMARIA_MAGIC_COST * hit_count))

    if item_allowed("Cane of Byrna") and state.has("Cane of Byrna", player):
        hit_count = _get_best_hit_count(
            state,
            player,
            sprite_id,
            (1,),
            {1} if bypass_damage_class_filter else allowed_damage_classes,
            combat_model,
            hp_override=hp_override,
        )
        if hit_count is not None:
            plans.add(ResourceCosts(magic=BYRNA_INITIAL_MAGIC_COST + (BYRNA_DRAIN_MAGIC_COST * max(0, hit_count - 1))))

    if item_allowed("Magic Powder") and state.has("Magic Powder", player):
        hit_count = _get_best_hit_count(
            state,
            player,
            sprite_id,
            (10,),
            {10} if bypass_damage_class_filter else allowed_damage_classes,
            combat_model,
            hp_override=hp_override,
        )
        if hit_count is not None:
            plans.add(ResourceCosts(magic=MAGIC_POWDER_MAGIC_COST * hit_count))

    if item_allowed("Bow") and state.has("Bow", player) and can_shoot_arrows(state, player, 1):
        hit_count = _get_best_hit_count(
            state,
            player,
            sprite_id,
            (6,),
            {6} if bypass_damage_class_filter else allowed_damage_classes,
            combat_model,
            hp_override=hp_override,
        )
        if hit_count is not None:
            plans.add(ResourceCosts(arrows=hit_count))

    if item_allowed("Silver Bow") and _has_silver_arrow_attack(state, player) and can_shoot_arrows(state, player, 1):
        hit_count = _get_best_hit_count(
            state,
            player,
            sprite_id,
            (9,),
            {9} if bypass_damage_class_filter else allowed_damage_classes,
            combat_model,
            hp_override=hp_override,
        )
        if hit_count is not None:
            plans.add(ResourceCosts(arrows=hit_count))

    if ability_allowed("bombs") and can_use_bombs(state, player, 1):
        hit_count = _get_best_hit_count(
            state,
            player,
            sprite_id,
            (8,),
            {8} if bypass_damage_class_filter else allowed_damage_classes,
            combat_model,
            hp_override=hp_override,
        )
        if hit_count is not None:
            plans.add(ResourceCosts(bombs=hit_count))

    if ability_allowed("sword_beams") and _has_sword_beam_attack(state, player):
        hit_count = _get_best_hit_count(
            state,
            player,
            sprite_id,
            (SWORD_BEAM_DAMAGE_CLASS,),
            {SWORD_BEAM_DAMAGE_CLASS} if bypass_damage_class_filter else allowed_damage_classes,
            combat_model,
            hp_override=hp_override,
        )
        if hit_count is not None:
            plans.add(FREE_RESOURCE_COSTS)

    if item_allowed("Fire Rod") and state.has("Fire Rod", player):
        hit_count = _get_best_hit_count(
            state,
            player,
            sprite_id,
            (11,),
            {11} if bypass_damage_class_filter else allowed_damage_classes,
            combat_model,
            hp_override=hp_override,
        )
        if hit_count is not None:
            plans.add(ResourceCosts(magic=FIRE_ROD_MAGIC_COST * hit_count))

    if item_allowed("Ice Rod") and state.has("Ice Rod", player):
        hit_count = _get_best_hit_count(
            state,
            player,
            sprite_id,
            (12,),
            {12} if bypass_damage_class_filter else allowed_damage_classes,
            combat_model,
            hp_override=hp_override,
        )
        if hit_count is not None:
            plans.add(ResourceCosts(magic=ICE_ROD_MAGIC_COST * hit_count))

    return _prune_dominated_resource_costs(plans)


def _build_single_hit_plans_for_damage_classes(
    state: CollectionState,
    player: int,
    allowed_damage_classes: set[int],
    *,
    allowed_items: tuple[str, ...] | None = None,
    allowed_abilities: tuple[str, ...] | None = None,
) -> tuple[ResourceCosts, ...]:
    allowed_items_set = set(allowed_items) if allowed_items is not None else None
    allowed_abilities_set = set(allowed_abilities) if allowed_abilities is not None else None

    def item_allowed(item_name: str) -> bool:
        return allowed_items_set is None or item_name in allowed_items_set

    def ability_allowed(ability_name: str) -> bool:
        return allowed_abilities_set is None or ability_name in allowed_abilities_set

    plans: set[ResourceCosts] = set()

    zero_cost_damage_class_items = (
        ("Fighter Sword", FIGHTER_SWORD_DAMAGE_CLASSES, state.has("Fighter Sword", player)),
        ("Master Sword", MASTER_SWORD_DAMAGE_CLASSES, state.has("Master Sword", player)),
        ("Tempered Sword", TEMPERED_SWORD_DAMAGE_CLASSES, state.has("Tempered Sword", player)),
        ("Golden Sword", GOLDEN_SWORD_DAMAGE_CLASSES, state.has("Golden Sword", player)),
        ("Hammer", (3,), state.has("Hammer", player)),
        ("Blue Boomerang", (0,), state.has("Blue Boomerang", player)),
        ("Red Boomerang", (0,), state.has("Red Boomerang", player)),
        ("Hookshot", (7,), state.has("Hookshot", player)),
    )
    for item_name, item_damage_classes, available in zero_cost_damage_class_items:
        if available and item_allowed(item_name) and allowed_damage_classes.intersection(item_damage_classes):
            plans.add(FREE_RESOURCE_COSTS)

    if item_allowed("Cane of Somaria") and state.has("Cane of Somaria", player) and 1 in allowed_damage_classes:
        plans.add(ResourceCosts(magic=SOMARIA_MAGIC_COST))

    if item_allowed("Cane of Byrna") and state.has("Cane of Byrna", player) and 1 in allowed_damage_classes:
        plans.add(ResourceCosts(magic=BYRNA_INITIAL_MAGIC_COST))

    if item_allowed("Magic Powder") and state.has("Magic Powder", player) and 10 in allowed_damage_classes:
        plans.add(ResourceCosts(magic=MAGIC_POWDER_MAGIC_COST))

    if (
        item_allowed("Bow")
        and state.has("Bow", player)
        and can_shoot_arrows(state, player, 1)
        and 6 in allowed_damage_classes
    ):
        plans.add(ResourceCosts(arrows=1))

    if (
        item_allowed("Silver Bow")
        and _has_silver_arrow_attack(state, player)
        and can_shoot_arrows(state, player, 1)
        and 9 in allowed_damage_classes
    ):
        plans.add(ResourceCosts(arrows=1))

    if ability_allowed("bombs") and can_use_bombs(state, player, 1) and 8 in allowed_damage_classes:
        plans.add(ResourceCosts(bombs=1))

    if (
        ability_allowed("sword_beams")
        and _has_sword_beam_attack(state, player)
        and SWORD_BEAM_DAMAGE_CLASS in allowed_damage_classes
    ):
        plans.add(FREE_RESOURCE_COSTS)

    if item_allowed("Fire Rod") and state.has("Fire Rod", player) and 11 in allowed_damage_classes:
        plans.add(ResourceCosts(magic=FIRE_ROD_MAGIC_COST))

    if item_allowed("Ice Rod") and state.has("Ice Rod", player) and 12 in allowed_damage_classes:
        plans.add(ResourceCosts(magic=ICE_ROD_MAGIC_COST))

    return _prune_dominated_resource_costs(plans)


def _get_transform_source_plans(
    state: CollectionState,
    player: int,
    transform_damage_classes: set[int],
) -> tuple[ResourceCosts, ...]:
    plans: set[ResourceCosts] = set()
    if 10 in transform_damage_classes and state.has("Magic Powder", player):
        plans.add(ResourceCosts(magic=MAGIC_POWDER_MAGIC_COST))
    return _prune_dominated_resource_costs(plans)


def _get_buzzblob_disable_follow_up_plans(
    state: CollectionState,
    player: int,
    combat_reference_id: int,
    direct_kill_damage_classes: set[int],
    combat_model: EnemyCombatModel,
) -> tuple[ResourceCosts, ...]:
    disable_damage_classes = set(
        get_damage_classes_with_effects(combat_reference_id, BUZZBLOB_DISABLE_EFFECTS, combat_model)
    )
    if not disable_damage_classes:
        return tuple()

    disable_plans = _build_single_hit_plans_for_damage_classes(
        state,
        player,
        disable_damage_classes,
        allowed_items=BUZZBLOB_DISABLE_ITEMS,
        allowed_abilities=BUZZBLOB_DISABLE_ABILITIES,
    )
    if not disable_plans:
        return tuple()

    follow_up_plans = _build_attack_plans_for_damage_classes(
        state,
        player,
        combat_reference_id,
        direct_kill_damage_classes,
        combat_model,
        allowed_items=BUZZBLOB_FOLLOW_UP_ITEMS,
    )
    if not follow_up_plans:
        return tuple()

    plans: set[ResourceCosts] = set()
    for disable_plan in disable_plans:
        for follow_up_plan in follow_up_plans:
            plans.add(_add_resource_costs(disable_plan, follow_up_plan))
    return _prune_dominated_resource_costs(plans)


def _get_yellow_slime_follow_up_plans(
    state: CollectionState,
    player: int,
    combat_reference_id: int,
    combat_model: EnemyCombatModel,
) -> tuple[ResourceCosts, ...]:
    follow_up_override = get_yellow_slime_follow_up_delivery_override(combat_reference_id)
    if follow_up_override is None:
        return tuple()

    return _build_attack_plans_for_damage_classes(
        state,
        player,
        YELLOW_SLIME_SPRITE_ID,
        set(get_killing_damage_classes(YELLOW_SLIME_SPRITE_ID, combat_model)),
        combat_model,
        allowed_items=follow_up_override.items,
        allowed_abilities=follow_up_override.abilities,
    )


def _get_transform_attack_plans(
    state: CollectionState,
    player: int,
    requirement,
) -> tuple[ResourceCosts, ...]:
    requirement = _get_enemy_requirement(requirement)
    combat_model = _get_active_combat_model(state, player)
    combat_reference_id = _get_combat_reference_id(requirement, combat_model)
    if combat_reference_id is None:
        return tuple()

    transform_source_plans = _get_transform_source_plans(
        state,
        player,
        _get_blob_transform_damage_classes(requirement, combat_model),
    )
    if not transform_source_plans:
        return tuple()

    yellow_slime_follow_up_plans = _get_yellow_slime_follow_up_plans(
        state,
        player,
        combat_reference_id,
        combat_model,
    )
    if not yellow_slime_follow_up_plans:
        return tuple()

    plans: set[ResourceCosts] = set()
    for transform_source_plan in transform_source_plans:
        for follow_up_plan in yellow_slime_follow_up_plans:
            plans.add(_add_resource_costs(transform_source_plan, follow_up_plan))
    return _prune_dominated_resource_costs(plans)


def _get_enemy_kill_plans(
    state: CollectionState,
    player: int,
    requirement,
    *,
    key_drop_enemy: bool = False,
) -> tuple[ResourceCosts, ...]:
    hp_override = _get_enemy_hp_override(requirement)
    requirement = _get_enemy_requirement(requirement)
    combat_model = _get_active_combat_model(state, player)
    combat_reference_id = _get_combat_reference_id(requirement, combat_model)
    if combat_reference_id is None:
        return tuple()

    direct_kill_damage_classes = _get_direct_kill_damage_classes(requirement, combat_model)
    direct_kill_delivery_override = DIRECT_KILL_DELIVERY_OVERRIDES.get(requirement.sprite_name)
    if key_drop_enemy:
        key_drop_damage_classes = KEY_DROP_KILL_DAMAGE_CLASS_OVERRIDES.get(requirement.sprite_name)
        if key_drop_damage_classes is not None:
            direct_kill_damage_classes = set(key_drop_damage_classes)
            direct_kill_delivery_override = None

    direct_attack_plans: tuple[ResourceCosts, ...] = tuple()
    if requirement.sprite_name != "Terrorpin" or state.has("Hammer", player):
        direct_attack_plans = _build_attack_plans_for_damage_classes(
            state,
            player,
            combat_reference_id,
            direct_kill_damage_classes,
            combat_model,
            hp_override=hp_override,
            allowed_items=(
                direct_kill_delivery_override.items
                if direct_kill_delivery_override is not None
                else None
            ),
            allowed_abilities=(
                direct_kill_delivery_override.abilities
                if direct_kill_delivery_override is not None
                else None
            ),
            bypass_damage_class_filter=direct_kill_delivery_override is not None,
        )

    if key_drop_enemy and requirement.sprite_name in KEY_DROP_KILL_DAMAGE_CLASS_OVERRIDES:
        return direct_attack_plans

    plans = set(direct_attack_plans)
    if requirement.sprite_name == "Buzzblob":
        plans.update(
            _get_buzzblob_disable_follow_up_plans(
                state,
                player,
                combat_reference_id,
                direct_kill_damage_classes,
                combat_model,
            )
        )
    plans.update(_get_transform_attack_plans(state, player, requirement))
    return _prune_dominated_resource_costs(plans)


def _get_enemy_kill_plans_after_room_wide_medallions(
    state: CollectionState,
    player: int,
    requirement,
    room_wide_medallions: tuple[str, ...],
    *,
    key_drop_enemy: bool = False,
) -> tuple[ResourceCosts, ...]:
    individual_plans = _get_enemy_kill_plans(state, player, requirement, key_drop_enemy=key_drop_enemy)
    if FREE_RESOURCE_COSTS in individual_plans:
        return (FREE_RESOURCE_COSTS,)

    plans = set(individual_plans)
    plans.update(
        _get_room_wide_medallion_enemy_plans(
            state,
            player,
            requirement,
            room_wide_medallions,
            key_drop_enemy=key_drop_enemy,
        )
    )
    return _prune_dominated_resource_costs(plans)


def _get_available_room_wide_medallions(state: CollectionState, player: int) -> tuple[str, ...]:
    if not _can_ready_medallion(state, player):
        return tuple()
    return tuple(
        medallion
        for medallion in ROOM_WIDE_MEDALLION_DAMAGE_CLASSES
        if state.has(medallion, player)
    )


def _get_room_wide_medallion_cast_sets(available_medallions: tuple[str, ...]) -> tuple[tuple[str, ...], ...]:
    cast_sets: list[tuple[str, ...]] = [tuple()]
    for mask in range(1, 1 << len(available_medallions)):
        cast_sets.append(tuple(
            medallion
            for index, medallion in enumerate(available_medallions)
            if mask & (1 << index)
        ))
    return tuple(cast_sets)


def _get_room_wide_medallion_enemy_plans(
    state: CollectionState,
    player: int,
    requirement,
    room_wide_medallions: tuple[str, ...],
    *,
    key_drop_enemy: bool = False,
) -> tuple[ResourceCosts, ...]:
    if not room_wide_medallions:
        return tuple()

    hp_override = _get_enemy_hp_override(requirement)
    requirement = _get_enemy_requirement(requirement)
    combat_model = _get_active_combat_model(state, player)
    combat_reference_id = _get_combat_reference_id(requirement, combat_model)
    if combat_reference_id is None:
        return tuple()

    plans: set[ResourceCosts] = set()
    direct_kill_damage_classes, direct_kill_delivery_override = _get_direct_kill_context(
        requirement,
        combat_model,
        key_drop_enemy=key_drop_enemy,
    )
    transform_damage_classes = _get_blob_transform_damage_classes(requirement, combat_model)
    disable_damage_classes = (
        set(get_damage_classes_with_effects(combat_reference_id, BUZZBLOB_DISABLE_EFFECTS, combat_model))
        if requirement.sprite_name == "Buzzblob"
        else set()
    )

    for medallion in room_wide_medallions:
        damage_class = ROOM_WIDE_MEDALLION_DAMAGE_CLASSES[medallion]
        if _room_wide_medallion_directly_kills_enemy(
            state,
            player,
            requirement,
            combat_reference_id,
            damage_class,
            direct_kill_damage_classes,
            direct_kill_delivery_override,
            combat_model,
            hp_override=hp_override,
        ):
            plans.add(FREE_RESOURCE_COSTS)

        if key_drop_enemy and requirement.sprite_name in KEY_DROP_KILL_DAMAGE_CLASS_OVERRIDES:
            continue

        if damage_class in transform_damage_classes:
            plans.update(_get_yellow_slime_follow_up_plans(state, player, combat_reference_id, combat_model))

        if damage_class in disable_damage_classes:
            plans.update(
                _build_attack_plans_for_damage_classes(
                    state,
                    player,
                    combat_reference_id,
                    direct_kill_damage_classes,
                    combat_model,
                    hp_override=hp_override,
                    allowed_items=BUZZBLOB_FOLLOW_UP_ITEMS,
                )
            )

    return _prune_dominated_resource_costs(plans)


def _room_wide_medallion_directly_kills_enemy(
    state: CollectionState,
    player: int,
    requirement,
    combat_reference_id: int,
    damage_class: int,
    direct_kill_damage_classes: set[int],
    direct_kill_delivery_override,
    combat_model: EnemyCombatModel,
    hp_override: int | None = None,
) -> bool:
    if requirement.sprite_name == "Terrorpin" and not state.has("Hammer", player):
        return False

    medallion = combat_model.damage_sources[damage_class].name
    if direct_kill_delivery_override is not None and medallion not in direct_kill_delivery_override.items:
        return False

    hit_count = _get_best_hit_count(
        state,
        player,
        combat_reference_id,
        (damage_class,),
        direct_kill_damage_classes,
        combat_model,
        hp_override=hp_override,
    )
    return hit_count == 1


def _can_execute_enemy_kill_plans(
    plans_by_enemy: tuple[tuple[ResourceCosts, ...], ...],
    budget: ResourceBudget,
    *,
    base_costs: ResourceCosts = FREE_RESOURCE_COSTS,
) -> bool:
    return bool(_get_executable_enemy_kill_costs(plans_by_enemy, budget, base_costs=base_costs))


def _get_executable_enemy_kill_costs(
    plans_by_enemy: tuple[tuple[ResourceCosts, ...], ...],
    budget: ResourceBudget,
    *,
    base_costs: ResourceCosts = FREE_RESOURCE_COSTS,
) -> tuple[ResourceCosts, ...]:
    if not _fits_within_resource_budget(base_costs, budget):
        return tuple()

    frontier: tuple[ResourceCosts, ...] = (base_costs,)
    for enemy_plans in sorted(plans_by_enemy, key=len):
        if not enemy_plans:
            return tuple()
        if FREE_RESOURCE_COSTS in enemy_plans:
            continue
        next_frontier: set[ResourceCosts] = set()
        for used_costs in frontier:
            for enemy_plan in enemy_plans:
                combined_costs = _add_resource_costs(used_costs, enemy_plan)
                if _fits_within_resource_budget(combined_costs, budget):
                    next_frontier.add(combined_costs)
        if not next_frontier:
            return tuple()
        frontier = _prune_dominated_resource_costs(next_frontier)
    return frontier


def _can_ready_medallion(state: CollectionState, player: int) -> bool:
    return state.multiworld.worlds[player].options.swordless or has_sword(state, player)


def _can_cast_medallion(state: CollectionState, player: int) -> bool:
    return _can_ready_medallion(state, player) and can_extend_magic(state, player, 16)


def can_kill_standard_start(state: CollectionState, player: int, enemies: int = 5) -> bool:
    # Enemizer does not randomize standard start enemies
        return (has_melee_weapon(state, player)
                or state.has('Cane of Somaria', player)
                or (state.has('Cane of Byrna', player) and (enemies < 6 or can_extend_magic(state, player)))
                or state.has_any(["Bow", "Progressive Bow"], player)
                or state.has('Fire Rod', player)
                or can_use_bombs(state, player, enemies)) # Escape assist is set


def can_get_good_bee(state: CollectionState, player: int) -> bool:
    cave = state.multiworld.get_region('Good Bee Cave', player)
    return (
            state.has_group("Bottles", player) and
            state.has('Bug Catching Net', player) and
            (state.has('Pegasus Boots', player) or (has_sword(state, player) and state.has('Quake', player))) and
            cave.can_reach(state) and
            is_not_bunny(state, cave, player)
    )


def can_retrieve_tablet(state: CollectionState, player: int) -> bool:
    return state.has('Book of Mudora', player) and (has_beam_sword(state, player) or
                                                    (state.multiworld.worlds[player].options.swordless and
                                                     state.has("Hammer", player)))


def has_sword(state: CollectionState, player: int) -> bool:
    return state.has('Fighter Sword', player) \
        or state.has('Master Sword', player) \
        or state.has('Tempered Sword', player) \
        or state.has('Golden Sword', player)


def has_beam_sword(state: CollectionState, player: int) -> bool:
    return state.has('Master Sword', player) or state.has('Tempered Sword', player) or state.has('Golden Sword',
                                                                                                 player)


def has_melee_weapon(state: CollectionState, player: int) -> bool:
    return has_sword(state, player) or state.has('Hammer', player)


def has_fire_source(state: CollectionState, player: int) -> bool:
    return state.has('Fire Rod', player) or state.has('Lamp', player)


def can_melt_things(state: CollectionState, player: int) -> bool:
    return state.has('Fire Rod', player) or \
        (state.has('Bombos', player) and
         (state.multiworld.worlds[player].options.swordless or
          has_sword(state, player)))


def has_misery_mire_medallion(state: CollectionState, player: int) -> bool:
    return state.has(state.multiworld.worlds[player].required_medallions[0], player)


def has_turtle_rock_medallion(state: CollectionState, player: int) -> bool:
    return state.has(state.multiworld.worlds[player].required_medallions[1], player)


def can_boots_clip_lw(state: CollectionState, player: int) -> bool:
    if state.multiworld.worlds[player].options.mode == 'inverted':
        return state.has('Pegasus Boots', player) and state.has('Moon Pearl', player)
    return state.has('Pegasus Boots', player)


def can_boots_clip_dw(state: CollectionState, player: int) -> bool:
    if state.multiworld.worlds[player].options.mode != 'inverted':
        return state.has('Pegasus Boots', player) and state.has('Moon Pearl', player)
    return state.has('Pegasus Boots', player)


def can_get_glitched_speed_dw(state: CollectionState, player: int) -> bool:
    rules = [state.has('Pegasus Boots', player), any([state.has('Hookshot', player), has_sword(state, player)])]
    if state.multiworld.worlds[player].options.mode != 'inverted':
        rules.append(state.has('Moon Pearl', player))
    return all(rules)
