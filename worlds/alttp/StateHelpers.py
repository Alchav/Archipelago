from bisect import bisect_left, bisect_right
from typing import NamedTuple

from .SubClasses import LTTPRegion
from .enemizer_data.enemy_combat_data import (
    BLOB_TRANSFORM_EFFECT,
    DIRECT_KILL_DELIVERY_OVERRIDES,
    EnemyCombatModel,
    FAIRY_TRANSFORM_EFFECT,
    FIGHTER_SWORD_DAMAGE_CLASSES,
    FREEZE_EFFECT,
    FREEZOR_SPRITE_ID,
    GOLDEN_SWORD_DAMAGE_CLASSES,
    INCINERATE_EFFECT,
    KEY_DROP_INCINERATION_REQUIRED_SPRITE_NAMES,
    KHOLDSTARE_ICE_BLOCK_SPRITE_ID,
    KHOLDSTARE_SPRITE_ID,
    LIGHTNING_GATE_SPRITE_ID,
    MASTER_SWORD_DAMAGE_CLASSES,
    SWORD_BEAM_DAMAGE_CLASS,
    STUN_32_FRAMES_EFFECT,
    STUN_128_FRAMES_EFFECT,
    STUN_255_FRAMES_EFFECT,
    TEMPERED_SWORD_DAMAGE_CLASSES,
    TRANSFORM_DAMAGE_EFFECTS,
    TRINEXX_BLUE_HEAD_SPRITE_ID,
    TRINEXX_RED_HEAD_SPRITE_ID,
    VANILLA_COMBAT_MODEL,
    YELLOW_SLIME_SPRITE_ID,
    get_blob_transform_damage_classes,
    get_damage_classes_with_effects,
    get_damage_effect,
    get_enemy_health_for_logic,
    get_hardcoded_enemy_hp,
    get_hits_to_kill,
    get_incinerating_damage_classes,
    get_killing_damage_classes,
    get_yellow_slime_follow_up_delivery_override,
    is_killing_damage_effect,
    with_killable_thief_combat_model,
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
    return min(4,
               state.multiworld.worlds[player].difficulty_requirements.progressive_bottle_limit,
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


class EnemyHpOverride(NamedTuple):
    requirement: object
    hp_override: int


FREE_RESOURCE_COSTS = ResourceCosts()
ENEMY_COMBAT_CACHE_ATTRIBUTE = "_alttp_enemy_combat_logic_cache"
ENEMY_COMBAT_STATE_ITEMS = (
    "Fighter Sword",
    "Master Sword",
    "Tempered Sword",
    "Golden Sword",
    "Hammer",
    "Blue Boomerang",
    "Red Boomerang",
    "Hookshot",
    "Cane of Somaria",
    "Cane of Byrna",
    "Magic Powder",
    "Lamp",
    "Bow",
    "Silver Bow",
    "Silver Arrows",
    "Fire Rod",
    "Ice Rod",
    "Bombos",
    "Ether",
    "Quake",
)
ENEMY_COMBAT_STATE_VERSION_ITEMS = frozenset(ENEMY_COMBAT_STATE_ITEMS + (
    "Bomb Upgrade (+5)",
    "Bomb Upgrade (+10)",
    "Bomb Upgrade (50)",
    "Arrow Upgrade (+5)",
    "Arrow Upgrade (+10)",
    "Arrow Upgrade (70)",
    "Capacity Upgrade Shop",
))
ENEMY_CLEAR_MAGIC_UNITS_PER_LOGIC_UNIT = 2
FIRE_ROD_MAGIC_COST = 2
ICE_ROD_MAGIC_COST = 2
MEDALLION_MAGIC_COST = 4
MAGIC_POWDER_MAGIC_COST = 1
SOMARIA_MAGIC_COST = 1
BYRNA_INITIAL_MAGIC_COST = 2
BYRNA_DRAIN_MAGIC_COST = 1
SUPERTILE_QUADRANT_SIZE = 256
ROOM_WIDE_MEDALLION_DAMAGE_CLASSES = {
    "Bombos": 13,
    "Ether": 14,
    "Quake": 15,
}
SWORDLESS_MEDALLION_EXCEPTION_SPRITE_IDS = frozenset((
    FREEZOR_SPRITE_ID,
    KHOLDSTARE_SPRITE_ID,
    KHOLDSTARE_ICE_BLOCK_SPRITE_ID,
))
THROWN_OBJECT_DAMAGE_CLASS = 3
LIGHTNING_GATE_MAGIC_POWDER_DAMAGE_CLASS = 10
LIGHTNING_GATE_REMOVAL_EFFECTS = frozenset((FAIRY_TRANSFORM_EFFECT, BLOB_TRANSFORM_EFFECT, FREEZE_EFFECT))
# Evil Barrier rejects Fighter Sword and Hammer contact hits before the damage table result matters.
LIGHTNING_GATE_CONTACT_SWORD_DAMAGE_CLASSES = (
    ("Master Sword", frozenset((1, 2, 3))),
    ("Tempered Sword", frozenset((2, 3, 4))),
    ("Golden Sword", frozenset((3, 4, 5))),
)
TRINEXX_SIDE_HEAD_VULNERABLE_MELEE_HITS_PER_OPENER = 3
TRINEXX_SIDE_HEAD_OPENER_EFFECTS = frozenset((
    FREEZE_EFFECT,
    STUN_32_FRAMES_EFFECT,
    STUN_128_FRAMES_EFFECT,
    STUN_255_FRAMES_EFFECT,
))
ENEMY_COMBAT_STATE_VERSION_ATTRIBUTE = "_alttp_enemy_combat_logic_version"


def init_enemy_combat_state_version(state: CollectionState, parent) -> None:
    setattr(state, ENEMY_COMBAT_STATE_VERSION_ATTRIBUTE, {})


def copy_enemy_combat_state_version(state: CollectionState, ret: CollectionState) -> CollectionState:
    version_by_player = getattr(state, ENEMY_COMBAT_STATE_VERSION_ATTRIBUTE, None)
    if version_by_player is not None:
        setattr(ret, ENEMY_COMBAT_STATE_VERSION_ATTRIBUTE, version_by_player.copy())
    cache_by_player = getattr(state, ENEMY_COMBAT_CACHE_ATTRIBUTE, None)
    if cache_by_player is not None:
        setattr(ret, ENEMY_COMBAT_CACHE_ATTRIBUTE, cache_by_player.copy())
    return ret


def bump_enemy_combat_state_version(state: CollectionState, player: int, item_name: str | None = None) -> None:
    if item_name is not None and item_name not in ENEMY_COMBAT_STATE_VERSION_ITEMS:
        world = state.multiworld.worlds[player]
        if not world.options.retro_bow:
            return

    version_by_player = getattr(state, ENEMY_COMBAT_STATE_VERSION_ATTRIBUTE, None)
    if version_by_player is None:
        version_by_player = {}
        setattr(state, ENEMY_COMBAT_STATE_VERSION_ATTRIBUTE, version_by_player)
    version_by_player[player] = version_by_player.get(player, 0) + 1


def _get_enemy_combat_state_version(state: CollectionState, player: int) -> int | None:
    version_by_player = getattr(state, ENEMY_COMBAT_STATE_VERSION_ATTRIBUTE, None)
    if version_by_player is None:
        return None
    return version_by_player.get(player, 0)


def _get_enemy_combat_state_key(state: CollectionState, player: int) -> tuple:
    player_items = state.prog_items[player]
    has_arrow_weapon = bool(player_items["Bow"] or player_items["Silver Bow"])
    return (
        id(_get_active_combat_model(state, player)),
        _get_enemy_health_key(state, player),
        _get_max_attacks_in_logic(state, player),
        bool(state.multiworld.worlds[player].options.killable_thieves),
        can_shoot_arrows(state, player, 1) if has_arrow_weapon else False,
        can_use_bombs(state, player, 1),
        tuple(player_items[item_name] for item_name in ENEMY_COMBAT_STATE_ITEMS),
    )


def _get_enemy_combat_cache(state: CollectionState, player: int) -> dict:
    cache_by_player = getattr(state, ENEMY_COMBAT_CACHE_ATTRIBUTE, None)
    if cache_by_player is None:
        cache_by_player = {}
        setattr(state, ENEMY_COMBAT_CACHE_ATTRIBUTE, cache_by_player)

    state_version = _get_enemy_combat_state_version(state, player)
    if state_version is None:
        state_key = _get_enemy_combat_state_key(state, player)
    else:
        state_key = (
            state_version,
            id(_get_active_combat_model(state, player)),
            _get_enemy_health_key(state, player),
            _get_max_attacks_in_logic(state, player),
            bool(state.multiworld.worlds[player].options.killable_thieves),
        )
    cache_entry = cache_by_player.get(player)
    if cache_entry is None or cache_entry[0] != state_key:
        cache_entry = (state_key, {})
        cache_by_player[player] = cache_entry
    return cache_entry[1]


def _get_enemy_requirement_cache_key(requirement) -> tuple:
    enemy_or_requirement = requirement
    requirement = _get_enemy_requirement(enemy_or_requirement)
    return (
        requirement.sprite_id,
        requirement.combat_reference_id,
        requirement.sprite_name,
        getattr(requirement, "killable", None),
        _get_enemy_hp_override(enemy_or_requirement),
    )


def _add_resource_costs(left: ResourceCosts, right: ResourceCosts) -> ResourceCosts:
    return ResourceCosts(
        left.bombs + right.bombs,
        left.arrows + right.arrows,
        left.magic + right.magic,
    )


def _multiply_resource_costs(costs: ResourceCosts, count: int) -> ResourceCosts:
    return ResourceCosts(
        costs.bombs * count,
        costs.arrows * count,
        costs.magic * count,
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
    if (
        state.multiworld.worlds[player].options.swordless
        and state.has("Hammer", player)
        and _lightning_gate_damage_class_removes_barrier(THROWN_OBJECT_DAMAGE_CLASS, combat_model)
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
    return is_killing_damage_effect(effect) or effect in LIGHTNING_GATE_REMOVAL_EFFECTS


def _prune_dominated_resource_costs(costs: set[ResourceCosts]) -> tuple[ResourceCosts, ...]:
    if not costs:
        return tuple()
    if FREE_RESOURCE_COSTS in costs:
        return (FREE_RESOURCE_COSTS,)
    if len(costs) == 1:
        return tuple(costs)

    frontier: list[ResourceCosts] = []
    arrow_values: list[int] = []
    arrow_magic_frontier: list[tuple[int, int]] = []
    for candidate in sorted(costs):
        candidate_bombs, candidate_arrows, candidate_magic = candidate
        index = bisect_right(arrow_values, candidate_arrows) - 1
        if index >= 0 and arrow_magic_frontier[index][1] <= candidate_magic:
            continue

        insert_index = bisect_left(arrow_values, candidate_arrows)
        remove_end = insert_index
        while remove_end < len(arrow_magic_frontier) and arrow_magic_frontier[remove_end][1] >= candidate_magic:
            remove_end += 1
        arrow_values[insert_index:remove_end] = [candidate_arrows]
        arrow_magic_frontier[insert_index:remove_end] = [(candidate_arrows, candidate_magic)]
        frontier.append(candidate)
    return tuple(frontier)


def can_clear_enemy_room(state: CollectionState, player: int, room_name_or_id: str | int) -> bool:
    from .EnemyShuffle import get_effective_dungeon_room_enemies, get_room_id

    room_id = room_name_or_id if isinstance(room_name_or_id, int) else get_room_id(room_name_or_id)
    if room_id is None:
        raise ValueError(f"Unknown ALTTP room {room_name_or_id!r}")

    effective_room_enemies = tuple(get_effective_dungeon_room_enemies(state.multiworld.worlds[player], room_id))
    room_enemies = tuple(
        enemy
        for enemy in effective_room_enemies
        if _enemy_requirement_counts_for_room_clear(enemy)
    )
    return _can_clear_enemy_requirements(
        state,
        player,
        room_enemies,
        thrown_object_hits_by_quadrant=_get_thrown_object_hits_by_quadrant(room_id, effective_room_enemies),
        medallion_cast_context_enemies=effective_room_enemies,
    )


def can_clear_enemy_region(state: CollectionState, player: int, target_name: str) -> bool:
    from .EnemyLogicTargets import get_enemy_clear_target, get_enemy_clear_target_enemies
    from .EnemyShuffle import get_effective_dungeon_room_enemies, get_room_id

    target = get_enemy_clear_target(target_name)
    room_id = get_room_id(target.room_name)
    if room_id is None:
        raise ValueError(f"Unknown ALTTP room {target.room_name!r}")
    target_enemies = tuple(get_enemy_clear_target_enemies(state.multiworld.worlds[player], target_name))
    room_enemies = tuple(
        enemy
        for enemy in target_enemies
        if _enemy_requirement_counts_for_room_clear(enemy)
    )
    effective_room_enemies = tuple(get_effective_dungeon_room_enemies(state.multiworld.worlds[player], room_id))
    return _can_clear_enemy_requirements(
        state,
        player,
        room_enemies,
        thrown_object_hits_by_quadrant=_get_thrown_object_hits_by_quadrant(room_id, target_enemies, target),
        medallion_cast_context_enemies=effective_room_enemies,
    )


def can_clear_enemy_regions(state: CollectionState, player: int, *target_names: str) -> bool:
    from .EnemyLogicTargets import get_enemy_clear_target, get_enemy_clear_target_enemies
    from .EnemyShuffle import get_effective_dungeon_room_enemies, get_room_id

    target_data = tuple(
        (target_name, get_enemy_clear_target(target_name))
        for target_name in target_names
    )
    enemy_groups = tuple(
        tuple(
            enemy
            for enemy in get_enemy_clear_target_enemies(state.multiworld.worlds[player], target_name)
            if _enemy_requirement_counts_for_room_clear(enemy)
        )
        for target_name, _target in target_data
    )
    thrown_object_hits_by_group = []
    medallion_cast_context_groups = []
    for target_name, target in target_data:
        room_id = get_room_id(target.room_name)
        if room_id is None:
            raise ValueError(f"Unknown ALTTP room {target.room_name!r}")
        target_enemies = tuple(get_enemy_clear_target_enemies(state.multiworld.worlds[player], target_name))
        effective_room_enemies = tuple(get_effective_dungeon_room_enemies(state.multiworld.worlds[player], room_id))
        thrown_object_hits_by_group.append(_get_thrown_object_hits_by_quadrant(room_id, target_enemies, target))
        medallion_cast_context_groups.append(effective_room_enemies)
    return _can_clear_enemy_requirement_groups(
        state,
        player,
        enemy_groups,
        thrown_object_hits_by_group=tuple(thrown_object_hits_by_group),
        medallion_cast_context_groups=tuple(medallion_cast_context_groups),
    )


def can_kill_key_drop_enemy(state: CollectionState, player: int, location_name: str) -> bool:
    from .EnemyLogicTargets import get_key_drop_enemy, get_key_drop_enemy_target
    from .EnemyShuffle import get_effective_dungeon_room_enemies, get_room_id

    enemy = get_key_drop_enemy(state.multiworld.worlds[player], location_name)
    if enemy is None or not enemy.has_key or not _enemy_requirement_can_be_killed(state, player, enemy):
        return False

    target = get_key_drop_enemy_target(location_name)
    room_id = get_room_id(target.room_name)
    if room_id is None:
        raise ValueError(f"Unknown ALTTP room {target.room_name!r}")
    room_enemies = tuple(get_effective_dungeon_room_enemies(state.multiworld.worlds[player], room_id))
    context_enemies = tuple(
        context_enemy
        for context_enemy in room_enemies
        if context_enemy is enemy or _enemy_requirement_counts_for_room_clear(context_enemy)
    )
    return _can_clear_enemy_requirements(
        state,
        player,
        (enemy,),
        key_drop_enemy=True,
        freeze_throw_context_enemies=context_enemies,
        medallion_cast_context_enemies=room_enemies,
    )


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
    return _get_enemy_requirement(enemy_or_requirement).counts_for_enemy_clear


def _enemy_requirement_can_be_killed(state: CollectionState, player: int, requirement) -> bool:
    requirement = _get_enemy_requirement(requirement)
    if not requirement.killable:
        return False
    return bool(_get_enemy_kill_plans(state, player, requirement))


def _get_enemy_requirement(enemy_or_requirement):
    requirement = getattr(enemy_or_requirement, "requirement", enemy_or_requirement)
    if requirement is enemy_or_requirement:
        return requirement
    return _get_enemy_requirement(requirement)


def _get_enemy_hp_override(enemy_or_requirement) -> int | None:
    explicit_hp_override = getattr(enemy_or_requirement, "hp_override", None)
    if explicit_hp_override is not None:
        return explicit_hp_override
    requirement = _get_enemy_requirement(enemy_or_requirement)
    x_coord_pixels = getattr(enemy_or_requirement, "x_coord_pixels", None)
    return get_hardcoded_enemy_hp(requirement.sprite_id, x_coord_pixels)


def _get_thrown_object_hits_by_quadrant(
    room_id: int | None,
    room_enemies: tuple = tuple(),
    target=None,
) -> tuple[tuple[tuple[int, int], int], ...]:
    counts: dict[tuple[int, int], int] = {}
    for quadrant, count in _get_room_pot_hits_by_quadrant(room_id, target):
        counts[quadrant] = counts.get(quadrant, 0) + count
    for quadrant, count in _get_fake_master_sword_hits_by_quadrant(room_enemies, target):
        counts[quadrant] = counts.get(quadrant, 0) + count
    return tuple(sorted(counts.items()))


def _get_room_pot_hits_by_quadrant(room_id: int | None, target=None) -> tuple[tuple[tuple[int, int], int], ...]:
    if room_id is None:
        return tuple()

    room_pots = _get_pot_data_by_room_id().get(room_id)
    if room_pots is None:
        return tuple()

    counts: dict[tuple[int, int], int] = {}
    for pot in room_pots:
        if target is not None and not _target_contains_pot(target, pot):
            continue
        quadrant = _get_position_quadrant(pot.x * 2, pot.y * 16)
        counts[quadrant] = counts.get(quadrant, 0) + 1
    return tuple(sorted(counts.items()))


def _get_fake_master_sword_hits_by_quadrant(room_enemies: tuple, target=None) -> tuple[tuple[tuple[int, int], int], ...]:
    counts: dict[tuple[int, int], int] = {}
    for enemy in room_enemies:
        if _get_enemy_requirement(enemy).sprite_name != "Fake Master Sword":
            continue
        if target is not None and not target.contains(enemy):
            continue
        quadrant = _get_enemy_position_quadrant(enemy)
        if quadrant is None:
            continue
        counts[quadrant] = counts.get(quadrant, 0) + 1
    return tuple(sorted(counts.items()))


def _get_pot_data_by_room_id() -> dict[int, tuple]:
    if not hasattr(_get_pot_data_by_room_id, "cache"):
        from .enemizer_data.pot_shuffle_data import POT_ROOMS

        _get_pot_data_by_room_id.cache = {
            room.room_id: room.pots
            for room in POT_ROOMS
        }
    return _get_pot_data_by_room_id.cache


def _target_contains_pot(target, pot) -> bool:
    x_coord_pixels = pot.x * 2
    y_coord_pixels = pot.y * 16
    if x_coord_pixels < target.min_x or y_coord_pixels < target.min_y:
        return False
    if target.max_x is not None and x_coord_pixels >= target.max_x:
        return False
    if target.max_y is not None and y_coord_pixels >= target.max_y:
        return False
    return True


def _get_position_quadrant(x_coord_pixels: int, y_coord_pixels: int) -> tuple[int, int]:
    return (
        x_coord_pixels // SUPERTILE_QUADRANT_SIZE,
        y_coord_pixels // SUPERTILE_QUADRANT_SIZE,
    )


def _get_enemy_position_quadrant(enemy_or_requirement) -> tuple[int, int] | None:
    x_coord_pixels = getattr(enemy_or_requirement, "x_coord_pixels", None)
    y_coord_pixels = getattr(enemy_or_requirement, "y_coord_pixels", None)
    if x_coord_pixels is None or y_coord_pixels is None:
        return None
    return _get_position_quadrant(x_coord_pixels, y_coord_pixels)


def _can_clear_enemy_requirements(
    state: CollectionState,
    player: int,
    room_enemies: tuple,
    *,
    key_drop_enemy: bool = False,
    thrown_object_hits_by_quadrant: tuple[tuple[tuple[int, int], int], ...] = tuple(),
    freeze_throw_context_enemies: tuple = tuple(),
    medallion_cast_context_enemies: tuple = tuple(),
) -> bool:
    return _can_clear_enemy_requirement_groups(
        state,
        player,
        (room_enemies,),
        key_drop_enemy=key_drop_enemy,
        thrown_object_hits_by_group=(thrown_object_hits_by_quadrant,),
        freeze_throw_context_groups=((freeze_throw_context_enemies or room_enemies),),
        medallion_cast_context_groups=((medallion_cast_context_enemies or room_enemies),),
    )


def _can_clear_enemy_requirement_groups(
    state: CollectionState,
    player: int,
    enemy_groups: tuple[tuple, ...],
    *,
    key_drop_enemy: bool = False,
    thrown_object_hits_by_group: tuple[tuple[tuple[tuple[int, int], int], ...], ...] | None = None,
    freeze_throw_context_groups: tuple[tuple, ...] | None = None,
    medallion_cast_context_groups: tuple[tuple, ...] | None = None,
) -> bool:
    budget = _get_enemy_clear_resource_budget(state, player)
    if thrown_object_hits_by_group is None:
        thrown_object_hits_by_group = (tuple(),) * len(enemy_groups)
    if freeze_throw_context_groups is None:
        freeze_throw_context_groups = enemy_groups
    if medallion_cast_context_groups is None:
        medallion_cast_context_groups = enemy_groups
    group_clear_plans = tuple(
        _get_enemy_group_clear_plans(
            state,
            player,
            enemy_group,
            budget,
            key_drop_enemy=key_drop_enemy,
            thrown_object_hits_by_quadrant=thrown_object_hits_by_quadrant,
            freeze_throw_context_enemies=freeze_throw_context_enemies,
            medallion_cast_context_enemies=medallion_cast_context_enemies,
        )
        for enemy_group, thrown_object_hits_by_quadrant, freeze_throw_context_enemies, medallion_cast_context_enemies
        in zip(enemy_groups, thrown_object_hits_by_group, freeze_throw_context_groups, medallion_cast_context_groups)
    )
    return _can_execute_enemy_kill_plans(group_clear_plans, budget)


def _get_enemy_group_clear_plans(
    state: CollectionState,
    player: int,
    room_enemies: tuple,
    budget: ResourceBudget,
    *,
    key_drop_enemy: bool = False,
    thrown_object_hits_by_quadrant: tuple[tuple[tuple[int, int], int], ...] = tuple(),
    freeze_throw_context_enemies: tuple = tuple(),
    medallion_cast_context_enemies: tuple = tuple(),
) -> tuple[ResourceCosts, ...]:
    if not room_enemies:
        return (FREE_RESOURCE_COSTS,)

    cache = _get_enemy_combat_cache(state, player)
    cache_key = (
        "enemy_group_clear_plans",
        tuple(_get_enemy_requirement_cache_key(requirement) for requirement in room_enemies),
        key_drop_enemy,
        thrown_object_hits_by_quadrant,
        tuple(_get_enemy_requirement_cache_key(requirement) for requirement in freeze_throw_context_enemies),
        tuple(_get_enemy_requirement_cache_key(requirement) for requirement in medallion_cast_context_enemies),
        budget,
    )
    if cache_key in cache:
        return cache[cache_key]

    clear_plans: set[ResourceCosts] = set()
    thrown_object_adjusted_enemy_groups = _get_thrown_object_adjusted_enemy_groups(
        state,
        player,
        room_enemies,
        thrown_object_hits_by_quadrant,
        key_drop_enemy=key_drop_enemy,
    )
    available_medallions = _get_available_room_wide_medallions(
        state,
        player,
        medallion_cast_context_enemies or room_enemies,
    )
    pre_adjusted_group_plans = []
    for adjusted_enemy_group in thrown_object_adjusted_enemy_groups:
        pre_adjusted_group_plans.append((adjusted_enemy_group, FREE_RESOURCE_COSTS))
        pre_adjusted_group_plans.extend(_get_frozen_throw_adjusted_enemy_group_plans(
            state,
            player,
            adjusted_enemy_group,
            freeze_throw_context_enemies or adjusted_enemy_group,
            key_drop_enemy=key_drop_enemy,
        ))

    for adjusted_enemy_group, pre_adjustment_costs in pre_adjusted_group_plans:
        useful_medallions = _get_useful_room_wide_medallions(
            state,
            player,
            adjusted_enemy_group,
            available_medallions,
            key_drop_enemy=key_drop_enemy,
        )
        for room_wide_medallions in _get_room_wide_medallion_cast_sets(useful_medallions):
            base_costs = _add_resource_costs(
                pre_adjustment_costs,
                ResourceCosts(magic=MEDALLION_MAGIC_COST * len(room_wide_medallions)),
            )
            plans_by_enemy = tuple(
                _get_enemy_kill_plans_after_room_wide_medallions(
                    state,
                    player,
                    requirement,
                    room_wide_medallions,
                    key_drop_enemy=key_drop_enemy,
                )
                for requirement in adjusted_enemy_group
            )
            clear_plans.update(_get_executable_enemy_kill_costs(
                plans_by_enemy,
                budget,
                base_costs=base_costs,
            ))

    result = _prune_dominated_resource_costs(clear_plans)
    cache[cache_key] = result
    return result


def _get_thrown_object_adjusted_enemy_groups(
    state: CollectionState,
    player: int,
    room_enemies: tuple,
    thrown_object_hits_by_quadrant: tuple[tuple[tuple[int, int], int], ...],
    *,
    key_drop_enemy: bool = False,
) -> tuple[tuple, ...]:
    thrown_object_hits_by_quadrant = {
        quadrant: count
        for quadrant, count in thrown_object_hits_by_quadrant
        if count > 0
    }
    if not thrown_object_hits_by_quadrant:
        return (room_enemies,)

    enemy_health_key = _get_enemy_health_key(state, player)
    killable_thieves = bool(state.multiworld.worlds[player].options.killable_thieves)
    combat_model = _get_active_combat_model(state, player)
    enemy_entries = []
    for enemy in room_enemies:
        requirement = _get_enemy_requirement(enemy)
        combat_reference_id = _get_combat_reference_id(requirement, combat_model)
        if combat_reference_id is None:
            enemy_entries.append((enemy, None, None, None))
            continue

        hp = get_enemy_health_for_logic(
            combat_reference_id,
            enemy_health_key,
            hp_override=_get_enemy_hp_override(enemy),
            killable_thieves=killable_thieves,
            combat_model=combat_model,
        )
        effect = get_damage_effect(combat_reference_id, THROWN_OBJECT_DAMAGE_CLASS, combat_model)
        if hp is None or not _thrown_object_damage_effect_counts_for_room_clear(
            state, player, effect, enemy, key_drop_enemy=key_drop_enemy,
        ):
            enemy_entries.append((enemy, hp, None, None))
            continue
        enemy_entries.append((enemy, hp, effect, _get_enemy_position_quadrant(enemy)))

    if not any(
        effect is not None and quadrant in thrown_object_hits_by_quadrant
        for _, _, effect, quadrant in enemy_entries
    ):
        return (room_enemies,)

    hp_state = [hp for _, hp, _, _ in enemy_entries]
    for quadrant, thrown_object_hits in thrown_object_hits_by_quadrant.items():
        remaining_thrown_object_hits = thrown_object_hits
        thrown_object_targets = sorted(
            (
                (_get_thrown_object_hits_to_remove_enemy(state, player, hp, effect), index)
                for index, (_, hp, effect, enemy_quadrant) in enumerate(enemy_entries)
                if hp is not None and effect is not None and enemy_quadrant == quadrant
            ),
            key=lambda target: (target[0], target[1]),
        )
        for hits_to_remove, index in thrown_object_targets:
            if remaining_thrown_object_hits <= 0:
                break
            _, _, effect, _ = enemy_entries[index]
            if remaining_thrown_object_hits >= hits_to_remove:
                hp_state[index] = 0
                remaining_thrown_object_hits -= hits_to_remove
            else:
                for _ in range(remaining_thrown_object_hits):
                    hp_state[index] = _apply_thrown_object_damage_to_hp(state, player, hp_state[index], effect)
                remaining_thrown_object_hits = 0

    adjusted_group = []
    for index, remaining_hp in enumerate(hp_state):
        if remaining_hp == 0:
            continue
        enemy = enemy_entries[index][0]
        original_hp = enemy_entries[index][1]
        if remaining_hp is not None and original_hp is not None and remaining_hp < original_hp:
            adjusted_group.append(EnemyHpOverride(enemy, remaining_hp))
        else:
            adjusted_group.append(enemy)
    return (tuple(adjusted_group),)


def _thrown_object_damage_effect_counts_for_room_clear(
    state: CollectionState,
    player: int,
    effect: int,
    enemy=None,
    *,
    key_drop_enemy: bool = False,
) -> bool:
    if key_drop_enemy and enemy is not None:
        requirement = _get_enemy_requirement(enemy)
        if requirement.sprite_name in KEY_DROP_INCINERATION_REQUIRED_SPRITE_NAMES:
            return effect == INCINERATE_EFFECT
    return (
        effect == INCINERATE_EFFECT
        or 0 < effect < FAIRY_TRANSFORM_EFFECT
        or (effect == FREEZE_EFFECT and state.has("Hammer", player))
    )


def _pot_adjusted_enemy_group_sort_key(group: tuple) -> tuple[int, tuple[str, ...]]:
    return (
        len(group),
        tuple(repr(_get_enemy_requirement_cache_key(enemy)) for enemy in group),
    )


def _get_thrown_object_hits_to_remove_enemy(state: CollectionState, player: int, hp: int, effect: int) -> int:
    if effect == INCINERATE_EFFECT or (effect == FREEZE_EFFECT and state.has("Hammer", player)):
        return 1
    return (hp + effect - 1) // effect


def _apply_thrown_object_damage_to_hp(state: CollectionState, player: int, hp: int, effect: int) -> int:
    if effect == INCINERATE_EFFECT or (effect == FREEZE_EFFECT and state.has("Hammer", player)):
        return 0
    return max(0, hp - effect)


def _get_frozen_throw_adjusted_enemy_group_plans(
    state: CollectionState,
    player: int,
    room_enemies: tuple,
    freeze_throw_context_enemies: tuple,
    *,
    key_drop_enemy: bool = False,
) -> tuple[tuple[tuple, ResourceCosts], ...]:
    if not room_enemies:
        return tuple()

    combat_model = _get_active_combat_model(state, player)
    enemy_health_key = _get_enemy_health_key(state, player)
    killable_thieves = bool(state.multiworld.worlds[player].options.killable_thieves)
    plans: list[tuple[tuple, ResourceCosts]] = []
    seen_plan_keys: set[tuple[tuple, ResourceCosts]] = set()
    target_entries = []
    for target_index, enemy in enumerate(room_enemies):
        requirement = _get_enemy_requirement(enemy)
        combat_reference_id = _get_combat_reference_id(requirement, combat_model)
        if combat_reference_id is None:
            continue
        hp = get_enemy_health_for_logic(
            combat_reference_id,
            enemy_health_key,
            hp_override=_get_enemy_hp_override(enemy),
            killable_thieves=killable_thieves,
            combat_model=combat_model,
        )
        effect = get_damage_effect(combat_reference_id, THROWN_OBJECT_DAMAGE_CLASS, combat_model)
        if hp is None or not _thrown_object_damage_effect_counts_for_room_clear(
            state, player, effect, enemy, key_drop_enemy=key_drop_enemy,
        ):
            continue
        target_entries.append((target_index, enemy, hp, effect, _get_enemy_position_quadrant(enemy)))

    if not target_entries:
        return tuple()

    for source_enemy in freeze_throw_context_enemies:
        source_requirement = _get_enemy_requirement(source_enemy)
        source_combat_reference_id = _get_combat_reference_id(source_requirement, combat_model)
        if source_combat_reference_id is None:
            continue
        source_quadrant = _get_enemy_position_quadrant(source_enemy)
        if source_quadrant is None:
            continue
        freeze_damage_classes = set(get_damage_classes_with_effects(
            source_combat_reference_id,
            frozenset({FREEZE_EFFECT}),
            combat_model,
        ))
        if not freeze_damage_classes:
            continue
        freeze_plans = _build_single_hit_plans_for_damage_classes(
            state,
            player,
            freeze_damage_classes,
            medallion_exception_sprite_ids=frozenset(
                _get_enemy_requirement(context_enemy).sprite_id
                for context_enemy in freeze_throw_context_enemies
            ),
        )
        if not freeze_plans:
            continue
        for target_index, target_enemy, hp, effect, target_quadrant in target_entries:
            if target_enemy is source_enemy or target_quadrant != source_quadrant:
                continue
            adjusted_group = list(room_enemies)
            remaining_hp = _apply_thrown_object_damage_to_hp(state, player, hp, effect)
            if remaining_hp == 0:
                del adjusted_group[target_index]
            elif remaining_hp < hp:
                adjusted_group[target_index] = EnemyHpOverride(target_enemy, remaining_hp)
            else:
                continue
            for freeze_plan in freeze_plans:
                plan = (tuple(adjusted_group), freeze_plan)
                plan_key = (
                    tuple(_get_enemy_requirement_cache_key(requirement) for requirement in plan[0]),
                    freeze_plan,
                )
                if plan_key in seen_plan_keys:
                    continue
                seen_plan_keys.add(plan_key)
                plans.append(plan)
    return tuple(sorted(plans, key=lambda plan: (_pot_adjusted_enemy_group_sort_key(plan[0]), plan[1])))


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
    if combat_model is None and bool(getattr(world.options, "killable_thieves", False)):
        return with_killable_thief_combat_model()
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
    combat_reference_id = _get_combat_reference_id(requirement, combat_model)
    if combat_reference_id is None:
        return set(), None
    direct_kill_damage_classes = _get_direct_kill_damage_classes(requirement, combat_model)
    direct_kill_delivery_override = DIRECT_KILL_DELIVERY_OVERRIDES.get(requirement.sprite_name)
    if key_drop_enemy:
        if requirement.sprite_name in KEY_DROP_INCINERATION_REQUIRED_SPRITE_NAMES:
            direct_kill_damage_classes = set(get_incinerating_damage_classes(combat_reference_id, combat_model))
            direct_kill_delivery_override = None
        else:
            direct_kill_damage_classes = {
                damage_class for damage_class in direct_kill_damage_classes
                if get_damage_effect(combat_reference_id, damage_class, combat_model) != FAIRY_TRANSFORM_EFFECT
            }
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
    ignore_attack_limit: bool = False,
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
            allow_frozen_hammer_kill=state.has("Hammer", player),
        )
        for damage_class in damage_classes
        if damage_class in allowed_damage_classes
    ]
    valid_hit_counts = [hit_count for hit_count in hit_counts if hit_count is not None]
    if not ignore_attack_limit:
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
    ignore_attack_limit: bool = False,
    extra_magic_per_two_hits: int = 0,
) -> tuple[ResourceCosts, ...]:
    allowed_items_set = set(allowed_items) if allowed_items is not None else None
    allowed_abilities_set = set(allowed_abilities) if allowed_abilities is not None else None

    def item_allowed(item_name: str) -> bool:
        return allowed_items_set is None or item_name in allowed_items_set

    def ability_allowed(ability_name: str) -> bool:
        return allowed_abilities_set is None or ability_name in allowed_abilities_set

    plans: set[ResourceCosts] = set()

    def add_plan(costs: ResourceCosts, hit_count: int) -> None:
        if extra_magic_per_two_hits:
            vulnerability_windows = (hit_count + 1) // 2
            costs = costs._replace(magic=costs.magic + (extra_magic_per_two_hits * vulnerability_windows))
        plans.add(costs)

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
                ignore_attack_limit=ignore_attack_limit,
            )
            if hit_count is not None:
                add_plan(FREE_RESOURCE_COSTS, hit_count)

    if item_allowed("Cane of Somaria") and state.has("Cane of Somaria", player):
        hit_count = _get_best_hit_count(
            state,
            player,
            sprite_id,
            (1,),
            {1} if bypass_damage_class_filter else allowed_damage_classes,
            combat_model,
            hp_override=hp_override,
            ignore_attack_limit=ignore_attack_limit,
        )
        if hit_count is not None:
            add_plan(ResourceCosts(magic=SOMARIA_MAGIC_COST * hit_count), hit_count)

    if item_allowed("Cane of Byrna") and state.has("Cane of Byrna", player):
        hit_count = _get_best_hit_count(
            state,
            player,
            sprite_id,
            (1,),
            {1} if bypass_damage_class_filter else allowed_damage_classes,
            combat_model,
            hp_override=hp_override,
            ignore_attack_limit=ignore_attack_limit,
        )
        if hit_count is not None:
            add_plan(
                ResourceCosts(magic=BYRNA_INITIAL_MAGIC_COST + (BYRNA_DRAIN_MAGIC_COST * max(0, hit_count - 1))),
                hit_count,
            )

    if item_allowed("Magic Powder") and state.has("Magic Powder", player):
        hit_count = _get_best_hit_count(
            state,
            player,
            sprite_id,
            (10,),
            {10} if bypass_damage_class_filter else allowed_damage_classes,
            combat_model,
            hp_override=hp_override,
            ignore_attack_limit=ignore_attack_limit,
        )
        if hit_count is not None:
            add_plan(ResourceCosts(magic=MAGIC_POWDER_MAGIC_COST * hit_count), hit_count)

    if item_allowed("Bow") and state.has("Bow", player) and can_shoot_arrows(state, player, 1):
        hit_count = _get_best_hit_count(
            state,
            player,
            sprite_id,
            (6,),
            {6} if bypass_damage_class_filter else allowed_damage_classes,
            combat_model,
            hp_override=hp_override,
            ignore_attack_limit=ignore_attack_limit,
        )
        if hit_count is not None:
            add_plan(ResourceCosts(arrows=hit_count), hit_count)

    if item_allowed("Silver Bow") and _has_silver_arrow_attack(state, player) and can_shoot_arrows(state, player, 1):
        hit_count = _get_best_hit_count(
            state,
            player,
            sprite_id,
            (9,),
            {9} if bypass_damage_class_filter else allowed_damage_classes,
            combat_model,
            hp_override=hp_override,
            ignore_attack_limit=ignore_attack_limit,
        )
        if hit_count is not None:
            add_plan(ResourceCosts(arrows=hit_count), hit_count)

    if ability_allowed("bombs") and can_use_bombs(state, player, 1):
        hit_count = _get_best_hit_count(
            state,
            player,
            sprite_id,
            (8,),
            {8} if bypass_damage_class_filter else allowed_damage_classes,
            combat_model,
            hp_override=hp_override,
            ignore_attack_limit=ignore_attack_limit,
        )
        if hit_count is not None:
            add_plan(ResourceCosts(bombs=hit_count), hit_count)

    if ability_allowed("sword_beams") and _has_sword_beam_attack(state, player):
        hit_count = _get_best_hit_count(
            state,
            player,
            sprite_id,
            (SWORD_BEAM_DAMAGE_CLASS,),
            {SWORD_BEAM_DAMAGE_CLASS} if bypass_damage_class_filter else allowed_damage_classes,
            combat_model,
            hp_override=hp_override,
            ignore_attack_limit=ignore_attack_limit,
        )
        if hit_count is not None:
            add_plan(FREE_RESOURCE_COSTS, hit_count)

    if item_allowed("Fire Rod") and state.has("Fire Rod", player):
        hit_count = _get_best_hit_count(
            state,
            player,
            sprite_id,
            (11,),
            {11} if bypass_damage_class_filter else allowed_damage_classes,
            combat_model,
            hp_override=hp_override,
            ignore_attack_limit=ignore_attack_limit,
        )
        if hit_count is not None:
            add_plan(ResourceCosts(magic=FIRE_ROD_MAGIC_COST * hit_count), hit_count)

    if item_allowed("Ice Rod") and state.has("Ice Rod", player):
        hit_count = _get_best_hit_count(
            state,
            player,
            sprite_id,
            (12,),
            {12} if bypass_damage_class_filter else allowed_damage_classes,
            combat_model,
            hp_override=hp_override,
            ignore_attack_limit=ignore_attack_limit,
        )
        if hit_count is not None:
            add_plan(ResourceCosts(magic=ICE_ROD_MAGIC_COST * hit_count), hit_count)

    if _can_use_medallion_damage_against_sprite(state, player, sprite_id):
        for medallion, damage_class in ROOM_WIDE_MEDALLION_DAMAGE_CLASSES.items():
            if item_allowed(medallion) and state.has(medallion, player):
                hit_count = _get_best_hit_count(
                    state,
                    player,
                    sprite_id,
                    (damage_class,),
                    {damage_class} if bypass_damage_class_filter else allowed_damage_classes,
                    combat_model,
                    hp_override=hp_override,
                    ignore_attack_limit=ignore_attack_limit,
                )
                if hit_count is not None:
                    add_plan(ResourceCosts(magic=MEDALLION_MAGIC_COST * hit_count), hit_count)

    return _prune_dominated_resource_costs(plans)


def _build_single_hit_plans_for_damage_classes(
    state: CollectionState,
    player: int,
    allowed_damage_classes: set[int],
    *,
    allowed_items: tuple[str, ...] | None = None,
    allowed_abilities: tuple[str, ...] | None = None,
    medallion_exception_sprite_ids: frozenset[int] = frozenset(),
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

    if _can_use_medallion_damage_with_exception_sprites(state, player, medallion_exception_sprite_ids):
        for medallion, damage_class in ROOM_WIDE_MEDALLION_DAMAGE_CLASSES.items():
            if item_allowed(medallion) and state.has(medallion, player) and damage_class in allowed_damage_classes:
                plans.add(ResourceCosts(magic=MEDALLION_MAGIC_COST))

    return _prune_dominated_resource_costs(plans)


def _build_fixed_hit_plans_for_damage_classes(
    state: CollectionState,
    player: int,
    allowed_damage_classes: set[int],
    hit_count: int,
    *,
    allowed_items: tuple[str, ...] | None = None,
    allowed_abilities: tuple[str, ...] | None = None,
    medallion_exception_sprite_ids: frozenset[int] = frozenset(),
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
        plans.add(ResourceCosts(magic=SOMARIA_MAGIC_COST * hit_count))

    if item_allowed("Cane of Byrna") and state.has("Cane of Byrna", player) and 1 in allowed_damage_classes:
        plans.add(ResourceCosts(magic=BYRNA_INITIAL_MAGIC_COST + (BYRNA_DRAIN_MAGIC_COST * max(0, hit_count - 1))))

    if item_allowed("Magic Powder") and state.has("Magic Powder", player) and 10 in allowed_damage_classes:
        plans.add(ResourceCosts(magic=MAGIC_POWDER_MAGIC_COST * hit_count))

    if (
        item_allowed("Bow")
        and state.has("Bow", player)
        and can_shoot_arrows(state, player, 1)
        and 6 in allowed_damage_classes
    ):
        plans.add(ResourceCosts(arrows=hit_count))

    if (
        item_allowed("Silver Bow")
        and _has_silver_arrow_attack(state, player)
        and can_shoot_arrows(state, player, 1)
        and 9 in allowed_damage_classes
    ):
        plans.add(ResourceCosts(arrows=hit_count))

    if ability_allowed("bombs") and can_use_bombs(state, player, 1) and 8 in allowed_damage_classes:
        plans.add(ResourceCosts(bombs=hit_count))

    if (
        ability_allowed("sword_beams")
        and _has_sword_beam_attack(state, player)
        and SWORD_BEAM_DAMAGE_CLASS in allowed_damage_classes
    ):
        plans.add(FREE_RESOURCE_COSTS)

    if item_allowed("Fire Rod") and state.has("Fire Rod", player) and 11 in allowed_damage_classes:
        plans.add(ResourceCosts(magic=FIRE_ROD_MAGIC_COST * hit_count))

    if item_allowed("Ice Rod") and state.has("Ice Rod", player) and 12 in allowed_damage_classes:
        plans.add(ResourceCosts(magic=ICE_ROD_MAGIC_COST * hit_count))

    if _can_use_medallion_damage_with_exception_sprites(state, player, medallion_exception_sprite_ids):
        for medallion, damage_class in ROOM_WIDE_MEDALLION_DAMAGE_CLASSES.items():
            if item_allowed(medallion) and state.has(medallion, player) and damage_class in allowed_damage_classes:
                plans.add(ResourceCosts(magic=MEDALLION_MAGIC_COST * hit_count))

    return _prune_dominated_resource_costs(plans)


def _get_boss_attack_plans(
    state: CollectionState,
    player: int,
    sprite_id: int,
    *,
    allowed_items: tuple[str, ...] | None = None,
    allowed_abilities: tuple[str, ...] | None = None,
    hp_override: int | None = None,
    include_transform_removal: bool = False,
    extra_magic_per_two_hits: int = 0,
) -> tuple[ResourceCosts, ...]:
    boss_allowed_abilities = allowed_abilities if allowed_abilities is not None else tuple()
    cache = _get_enemy_combat_cache(state, player)
    cache_key = (
        "boss_attack_plans",
        sprite_id,
        allowed_items,
        boss_allowed_abilities,
        hp_override,
        include_transform_removal,
        extra_magic_per_two_hits,
    )
    if cache_key in cache:
        return cache[cache_key]

    combat_model = _get_active_combat_model(state, player)
    plans = set(_build_attack_plans_for_damage_classes(
        state,
        player,
        sprite_id,
        set(get_killing_damage_classes(sprite_id, combat_model)),
        combat_model,
        hp_override=hp_override,
        allowed_items=allowed_items,
        allowed_abilities=boss_allowed_abilities,
        ignore_attack_limit=True,
        extra_magic_per_two_hits=extra_magic_per_two_hits,
    ))

    if include_transform_removal:
        transform_damage_classes = set(get_damage_classes_with_effects(
            sprite_id,
            frozenset((FAIRY_TRANSFORM_EFFECT, BLOB_TRANSFORM_EFFECT)),
            combat_model,
        ))
        plans.update(_build_single_hit_plans_for_damage_classes(
            state,
            player,
            transform_damage_classes,
            allowed_items=allowed_items,
            allowed_abilities=boss_allowed_abilities,
            medallion_exception_sprite_ids=frozenset((sprite_id,)),
        ))

    result = _prune_dominated_resource_costs(plans)
    cache[cache_key] = result
    return result


def can_damage_blind_sprite(
    state: CollectionState,
    player: int,
    sprite_id: int,
    *,
    allowed_items: tuple[str, ...] | None = None,
    allowed_abilities: tuple[str, ...] | None = None,
) -> bool:
    boss_allowed_abilities = allowed_abilities if allowed_abilities is not None else tuple()
    cache = _get_enemy_combat_cache(state, player)
    cache_key = ("blind_fixed_hit_plans", sprite_id, allowed_items, boss_allowed_abilities)
    if cache_key in cache:
        plans = cache[cache_key]
        return _can_execute_enemy_kill_plans((plans,), _get_enemy_clear_resource_budget(state, player))

    combat_model = _get_active_combat_model(state, player)
    damage_classes = {
        damage_class
        for damage_class in range(16)
        if (
            effect := get_damage_effect(sprite_id, damage_class, combat_model)
        ) != 0 and effect not in (FAIRY_TRANSFORM_EFFECT, BLOB_TRANSFORM_EFFECT)
    }
    plans = _build_fixed_hit_plans_for_damage_classes(
        state,
        player,
        damage_classes,
        9,
        allowed_items=allowed_items,
        allowed_abilities=boss_allowed_abilities,
        medallion_exception_sprite_ids=frozenset((sprite_id,)),
    )
    cache[cache_key] = plans
    return _can_execute_enemy_kill_plans((plans,), _get_enemy_clear_resource_budget(state, player))


def _get_trinexx_side_head_attack_plans(
    state: CollectionState,
    player: int,
    sprite_id: int,
    *,
    opener_items: tuple[str, ...],
    opener_abilities: tuple[str, ...],
    follow_up_items: tuple[str, ...],
) -> tuple[ResourceCosts, ...]:
    if sprite_id not in (TRINEXX_RED_HEAD_SPRITE_ID, TRINEXX_BLUE_HEAD_SPRITE_ID):
        raise ValueError(f"Expected Trinexx side head sprite, got 0x{sprite_id:02X}")

    cache = _get_enemy_combat_cache(state, player)
    cache_key = ("trinexx_side_head_attack_plans", sprite_id, opener_items, opener_abilities, follow_up_items)
    if cache_key in cache:
        return cache[cache_key]

    combat_model = _get_active_combat_model(state, player)
    hp = get_enemy_health_for_logic(
        sprite_id,
        _get_enemy_health_key(state, player),
        killable_thieves=bool(state.multiworld.worlds[player].options.killable_thieves),
        combat_model=combat_model,
    )
    if hp is None:
        cache[cache_key] = tuple()
        return tuple()

    opener_classes = {
        damage_class
        for damage_class in range(len(combat_model.damage_sources))
        if damage_class != ROOM_WIDE_MEDALLION_DAMAGE_CLASSES["Quake"]
        and _trinexx_side_head_opener_effect(get_damage_effect(sprite_id, damage_class, combat_model))
    }
    follow_up_classes = {
        damage_class
        for damage_class in range(len(combat_model.damage_sources))
        if _trinexx_side_head_effect_damage(get_damage_effect(sprite_id, damage_class, combat_model), hp) > 0
    }

    plans: set[ResourceCosts] = set()
    for opener_class in opener_classes:
        opener_plans = _build_single_hit_plans_for_damage_classes(
            state,
            player,
            {opener_class},
            allowed_items=opener_items,
            allowed_abilities=opener_abilities,
            medallion_exception_sprite_ids=frozenset((sprite_id,)),
        )
        if not opener_plans:
            continue

        opener_effect = get_damage_effect(sprite_id, opener_class, combat_model)
        opener_damage = _trinexx_side_head_effect_damage(opener_effect, hp)
        if opener_effect in TRANSFORM_DAMAGE_EFFECTS:
            for opener_plan in opener_plans:
                plans.add(opener_plan)
            continue

        for opener_plan in opener_plans:
            plans.update(_get_trinexx_side_head_window_plans(
                state,
                player,
                sprite_id,
                hp,
                opener_plan,
                opener_damage,
                follow_up_classes,
                follow_up_items,
                combat_model,
            ))

    result = _prune_dominated_resource_costs(plans)
    cache[cache_key] = result
    return result


def _trinexx_side_head_opener_effect(effect: int) -> bool:
    return (
        is_killing_damage_effect(effect)
        or effect in TRANSFORM_DAMAGE_EFFECTS
        or effect in TRINEXX_SIDE_HEAD_OPENER_EFFECTS
    )


def _trinexx_side_head_effect_damage(effect: int, hp: int) -> int:
    if effect == INCINERATE_EFFECT or effect in TRANSFORM_DAMAGE_EFFECTS:
        return hp
    if 0 < effect < FAIRY_TRANSFORM_EFFECT:
        return effect
    return 0


def _get_trinexx_side_head_window_plans(
    state: CollectionState,
    player: int,
    sprite_id: int,
    hp: int,
    opener_plan: ResourceCosts,
    opener_damage: int,
    follow_up_classes: set[int],
    follow_up_items: tuple[str, ...],
    combat_model: EnemyCombatModel,
) -> set[ResourceCosts]:
    plans: set[ResourceCosts] = set()
    max_cycle_damage = opener_damage
    follow_up_damage_by_class = {
        damage_class: _trinexx_side_head_effect_damage(get_damage_effect(sprite_id, damage_class, combat_model), hp)
        for damage_class in follow_up_classes
    }
    if follow_up_damage_by_class:
        max_cycle_damage += TRINEXX_SIDE_HEAD_VULNERABLE_MELEE_HITS_PER_OPENER * max(follow_up_damage_by_class.values())
    if max_cycle_damage <= 0:
        return plans

    for opener_count in range(1, hp + 1):
        remaining_hp = hp - (opener_damage * opener_count)
        if remaining_hp <= 0:
            plans.add(_multiply_resource_costs(opener_plan, opener_count))
            continue

        max_follow_up_hits = opener_count * TRINEXX_SIDE_HEAD_VULNERABLE_MELEE_HITS_PER_OPENER
        for damage_class, follow_up_damage in follow_up_damage_by_class.items():
            if follow_up_damage <= 0:
                continue
            follow_up_hits = (remaining_hp + follow_up_damage - 1) // follow_up_damage
            if follow_up_hits > max_follow_up_hits:
                continue
            follow_up_plans = _build_fixed_hit_plans_for_damage_classes(
                state,
                player,
                {damage_class},
                follow_up_hits,
                allowed_items=follow_up_items,
                medallion_exception_sprite_ids=frozenset((sprite_id,)),
            )
            for follow_up_plan in follow_up_plans:
                plans.add(_add_resource_costs(
                    _multiply_resource_costs(opener_plan, opener_count),
                    follow_up_plan,
                ))

    return plans


def can_damage_boss_sprite(
    state: CollectionState,
    player: int,
    sprite_id: int,
    *,
    allowed_items: tuple[str, ...] | None = None,
    allowed_abilities: tuple[str, ...] | None = None,
    hp_override: int | None = None,
    include_transform_removal: bool = False,
    extra_magic_per_two_hits: int = 0,
) -> bool:
    return _can_execute_enemy_kill_plans(
        (_get_boss_attack_plans(
            state,
            player,
            sprite_id,
            allowed_items=allowed_items,
            allowed_abilities=allowed_abilities,
            hp_override=hp_override,
            include_transform_removal=include_transform_removal,
            extra_magic_per_two_hits=extra_magic_per_two_hits,
        ),),
        _get_enemy_clear_resource_budget(state, player),
    )


def can_damage_boss_sprite_phases(
    state: CollectionState,
    player: int,
    *phase_plans: tuple[ResourceCosts, ...],
) -> bool:
    return _can_execute_enemy_kill_plans(phase_plans, _get_enemy_clear_resource_budget(state, player))


def can_hit_boss_sprite(
    state: CollectionState,
    player: int,
    sprite_id: int,
    *,
    allowed_items: tuple[str, ...] | None = None,
    allowed_abilities: tuple[str, ...] | None = None,
) -> bool:
    boss_allowed_abilities = allowed_abilities if allowed_abilities is not None else tuple()
    cache = _get_enemy_combat_cache(state, player)
    cache_key = ("boss_hit_plans", sprite_id, allowed_items, boss_allowed_abilities)
    if cache_key in cache:
        plans = cache[cache_key]
        return _can_execute_enemy_kill_plans((plans,), _get_enemy_clear_resource_budget(state, player))

    combat_model = _get_active_combat_model(state, player)
    damage_classes = set(get_killing_damage_classes(sprite_id, combat_model))
    plans = _build_single_hit_plans_for_damage_classes(
        state,
        player,
        damage_classes,
        allowed_items=allowed_items,
        allowed_abilities=boss_allowed_abilities,
        medallion_exception_sprite_ids=frozenset((sprite_id,)),
    )
    cache[cache_key] = plans
    return _can_execute_enemy_kill_plans((plans,), _get_enemy_clear_resource_budget(state, player))


def can_hit_boss_sprite_for_at_least_damage(
    state: CollectionState,
    player: int,
    sprite_id: int,
    minimum_damage: int,
    *,
    allowed_items: tuple[str, ...] | None = None,
    allowed_abilities: tuple[str, ...] | None = None,
) -> bool:
    boss_allowed_abilities = allowed_abilities if allowed_abilities is not None else tuple()
    cache = _get_enemy_combat_cache(state, player)
    cache_key = (
        "boss_minimum_damage_hit_plans",
        sprite_id,
        minimum_damage,
        allowed_items,
        boss_allowed_abilities,
    )
    if cache_key in cache:
        plans = cache[cache_key]
        return _can_execute_enemy_kill_plans((plans,), _get_enemy_clear_resource_budget(state, player))

    combat_model = _get_active_combat_model(state, player)
    damage_classes = {
        damage_class
        for damage_class in range(len(combat_model.damage_sources))
        if (
            (effect := get_damage_effect(sprite_id, damage_class, combat_model)) == INCINERATE_EFFECT
            or 0 < effect < FAIRY_TRANSFORM_EFFECT and effect >= minimum_damage
        )
    }
    plans = _build_single_hit_plans_for_damage_classes(
        state,
        player,
        damage_classes,
        allowed_items=allowed_items,
        allowed_abilities=boss_allowed_abilities,
        medallion_exception_sprite_ids=frozenset((sprite_id,)),
    )
    cache[cache_key] = plans
    return _can_execute_enemy_kill_plans((plans,), _get_enemy_clear_resource_budget(state, player))


def _get_transform_source_plans(
    state: CollectionState,
    player: int,
    transform_damage_classes: set[int],
    sprite_id: int | None = None,
) -> tuple[ResourceCosts, ...]:
    return _build_single_hit_plans_for_damage_classes(
        state,
        player,
        transform_damage_classes,
        medallion_exception_sprite_ids=frozenset((sprite_id,)) if sprite_id is not None else frozenset(),
    )


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
        medallion_exception_sprite_ids=frozenset((combat_reference_id,)),
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

    return _build_attack_plans_for_damage_classes(
        state,
        player,
        YELLOW_SLIME_SPRITE_ID,
        set(get_killing_damage_classes(YELLOW_SLIME_SPRITE_ID, combat_model)),
        combat_model,
        allowed_items=follow_up_override.items if follow_up_override is not None else None,
        allowed_abilities=follow_up_override.abilities if follow_up_override is not None else None,
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
        combat_reference_id,
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
    cache = _get_enemy_combat_cache(state, player)
    cache_key = ("enemy_kill_plans", _get_enemy_requirement_cache_key(requirement), key_drop_enemy)
    if cache_key in cache:
        return cache[cache_key]

    hp_override = _get_enemy_hp_override(requirement)
    requirement = _get_enemy_requirement(requirement)
    combat_model = _get_active_combat_model(state, player)
    combat_reference_id = _get_combat_reference_id(requirement, combat_model)
    if combat_reference_id is None:
        return tuple()

    direct_kill_damage_classes = _get_direct_kill_damage_classes(requirement, combat_model)
    direct_kill_delivery_override = DIRECT_KILL_DELIVERY_OVERRIDES.get(requirement.sprite_name)
    if key_drop_enemy:
        if requirement.sprite_name in KEY_DROP_INCINERATION_REQUIRED_SPRITE_NAMES:
            direct_kill_damage_classes = set(get_incinerating_damage_classes(combat_reference_id, combat_model))
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

    if key_drop_enemy and requirement.sprite_name in KEY_DROP_INCINERATION_REQUIRED_SPRITE_NAMES:
        cache[cache_key] = direct_attack_plans
        return direct_attack_plans

    plans = set(direct_attack_plans)
    if state.has("Hammer", player) and (
        direct_kill_delivery_override is None or "Hammer" in direct_kill_delivery_override.items
    ):
        freeze_damage_classes = set(get_damage_classes_with_effects(
            combat_reference_id,
            frozenset({FREEZE_EFFECT}),
            combat_model,
        ))
        plans.update(_build_single_hit_plans_for_damage_classes(
            state,
            player,
            freeze_damage_classes,
            medallion_exception_sprite_ids=frozenset((requirement.sprite_id,)),
        ))
    if requirement.sprite_name == "Floating Stalfos Head" and direct_kill_delivery_override is not None:
        plans.update(_build_single_hit_plans_for_damage_classes(
            state,
            player,
            {0, 1},
            allowed_items=direct_kill_delivery_override.items,
            allowed_abilities=direct_kill_delivery_override.abilities,
            medallion_exception_sprite_ids=frozenset((requirement.sprite_id,)),
        ))
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
    result = _prune_dominated_resource_costs(plans)
    cache[cache_key] = result
    return result


def _get_enemy_kill_plans_after_room_wide_medallions(
    state: CollectionState,
    player: int,
    requirement,
    room_wide_medallions: tuple[str, ...],
    *,
    key_drop_enemy: bool = False,
) -> tuple[ResourceCosts, ...]:
    cache = _get_enemy_combat_cache(state, player)
    cache_key = (
        "enemy_kill_plans_after_medallions",
        _get_enemy_requirement_cache_key(requirement),
        room_wide_medallions,
        key_drop_enemy,
    )
    if cache_key in cache:
        return cache[cache_key]

    individual_plans = _get_enemy_kill_plans(state, player, requirement, key_drop_enemy=key_drop_enemy)
    if FREE_RESOURCE_COSTS in individual_plans:
        cache[cache_key] = (FREE_RESOURCE_COSTS,)
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
    result = _prune_dominated_resource_costs(plans)
    cache[cache_key] = result
    return result


def _get_available_room_wide_medallions(state: CollectionState, player: int, room_enemies: tuple) -> tuple[str, ...]:
    if not _can_use_medallion_damage_in_room(state, player, room_enemies):
        return tuple()
    return tuple(
        medallion
        for medallion in ROOM_WIDE_MEDALLION_DAMAGE_CLASSES
        if state.has(medallion, player)
    )


def _get_useful_room_wide_medallions(
    state: CollectionState,
    player: int,
    room_enemies: tuple,
    available_medallions: tuple[str, ...],
    *,
    key_drop_enemy: bool = False,
) -> tuple[str, ...]:
    if not available_medallions or not room_enemies:
        return tuple()

    useful_medallions: set[str] = set()
    combat_model = _get_active_combat_model(state, player)
    for enemy_or_requirement in room_enemies:
        hp_override = _get_enemy_hp_override(enemy_or_requirement)
        requirement = _get_enemy_requirement(enemy_or_requirement)
        combat_reference_id = _get_combat_reference_id(requirement, combat_model)
        if combat_reference_id is None:
            continue

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

        for medallion in available_medallions:
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
                useful_medallions.add(medallion)
                continue

            if key_drop_enemy and requirement.sprite_name in KEY_DROP_INCINERATION_REQUIRED_SPRITE_NAMES:
                continue
            if damage_class in transform_damage_classes or damage_class in disable_damage_classes:
                useful_medallions.add(medallion)

    return tuple(medallion for medallion in available_medallions if medallion in useful_medallions)


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

        if key_drop_enemy and requirement.sprite_name in KEY_DROP_INCINERATION_REQUIRED_SPRITE_NAMES:
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
    if not _fits_within_resource_budget(base_costs, budget):
        return False

    frontier: tuple[ResourceCosts, ...] = (base_costs,)
    for enemy_plans in sorted(plans_by_enemy, key=len):
        if not enemy_plans:
            return False
        if FREE_RESOURCE_COSTS in enemy_plans:
            continue
        next_frontier: set[ResourceCosts] = set()
        for used_bombs, used_arrows, used_magic in frontier:
            for plan_bombs, plan_arrows, plan_magic in enemy_plans:
                bombs = used_bombs + plan_bombs
                arrows = used_arrows + plan_arrows
                magic = used_magic + plan_magic
                if bombs <= budget.bombs and (budget.arrows is None or arrows <= budget.arrows) and magic <= budget.magic:
                    next_frontier.add(ResourceCosts(bombs, arrows, magic))
        if not next_frontier:
            return False
        frontier = _prune_dominated_resource_costs(next_frontier)
    return True


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
        for used_bombs, used_arrows, used_magic in frontier:
            for plan_bombs, plan_arrows, plan_magic in enemy_plans:
                bombs = used_bombs + plan_bombs
                arrows = used_arrows + plan_arrows
                magic = used_magic + plan_magic
                if bombs <= budget.bombs and (budget.arrows is None or arrows <= budget.arrows) and magic <= budget.magic:
                    next_frontier.add(ResourceCosts(bombs, arrows, magic))
        if not next_frontier:
            return tuple()
        frontier = _prune_dominated_resource_costs(next_frontier)
    return frontier


def _can_ready_medallion(state: CollectionState, player: int) -> bool:
    world = state.multiworld.worlds[player]
    return world.options.item_functionality == 'easy' or has_sword(state, player)


def _can_use_medallion_damage_against_sprite(state: CollectionState, player: int, sprite_id: int) -> bool:
    return _can_use_medallion_damage_with_exception_sprites(state, player, frozenset((sprite_id,)))


def _can_use_medallion_damage_with_exception_sprites(
    state: CollectionState,
    player: int,
    sprite_ids: frozenset[int],
) -> bool:
    if _can_ready_medallion(state, player):
        return True
    return (
        state.multiworld.worlds[player].options.swordless
        and bool(sprite_ids.intersection(SWORDLESS_MEDALLION_EXCEPTION_SPRITE_IDS))
    )


def _can_use_medallion_damage_in_room(state: CollectionState, player: int, room_enemies: tuple) -> bool:
    return _can_use_medallion_damage_with_exception_sprites(
        state,
        player,
        frozenset(_get_enemy_requirement(enemy).sprite_id for enemy in room_enemies),
    )


def _can_cast_medallion(state: CollectionState, player: int) -> bool:
    return _can_ready_medallion(state, player) and can_extend_magic(state, player, 16)


def can_use_medallions(state: CollectionState, player: int) -> bool:
    return _can_ready_medallion(state, player)


def can_clear_standard_escape(state: CollectionState, player: int) -> bool:
    # Standard start enemies are not enemy-shuffled, but randomized damage classes still affect them.
    from .EnemyLogicTargets import (
        HYRULE_CASTLE_BIG_KEY_DROP,
        HYRULE_CASTLE_BOOMERANG_GUARD_KEY_DROP,
        HYRULE_CASTLE_MAP_GUARD_KEY_DROP,
        HYRULE_CASTLE_PRE_BOOMERANG_CHEST_ROOM,
        SEWERS_KEY_RAT_KEY_DROP,
    )

    return (
        can_kill_key_drop_enemy(state, player, HYRULE_CASTLE_MAP_GUARD_KEY_DROP)
        and can_clear_enemy_region(state, player, HYRULE_CASTLE_PRE_BOOMERANG_CHEST_ROOM)
        and can_kill_key_drop_enemy(state, player, HYRULE_CASTLE_BOOMERANG_GUARD_KEY_DROP)
        and can_kill_key_drop_enemy(state, player, HYRULE_CASTLE_BIG_KEY_DROP)
        and can_kill_key_drop_enemy(state, player, SEWERS_KEY_RAT_KEY_DROP)
    )


def can_kill_standard_start(state: CollectionState, player: int, enemies: int = 5) -> bool:
    from .EnemyLogicTargets import HYRULE_CASTLE_BIG_KEY_DROP

    if enemies <= 1:
        return can_kill_key_drop_enemy(state, player, HYRULE_CASTLE_BIG_KEY_DROP)
    return can_clear_standard_escape(state, player)


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
        (state.has('Bombos', player) and _can_ready_medallion(state, player))


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
