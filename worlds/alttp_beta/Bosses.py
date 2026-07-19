from __future__ import annotations

import logging
from typing import Optional, Union, List, Tuple, Callable, Dict, TYPE_CHECKING

from Fill import FillError
from .Options import LTTPBosses as Bosses
from .StateHelpers import (
    FIRE_ROD_MAGIC_COST,
    can_damage_boss_sprite,
    can_damage_boss_sprite_phases,
    can_damage_blind_sprite,
    can_get_good_bee,
    can_hit_boss_sprite,
    can_hit_boss_sprite_for_at_least_damage,
    has_fire_source,
    has_sword,
    can_use_bombs,
    _get_boss_attack_plans,
    _get_trinexx_side_head_attack_plans,
)
from .enemizer_data.enemy_combat_data import (
    ARRGHUS_FUZZ_SPRITE_ID,
    ARRGHUS_SPRITE_ID,
    ARMOS_KNIGHTS_SPRITE_ID,
    BLIND_SPRITE_ID,
    GANON_D6_SPRITE_ID,
    GANON_D7_SPRITE_ID,
    HELMASAUR_KING_SPRITE_ID,
    KHOLDSTARE_ICE_BLOCK_SPRITE_ID,
    KHOLDSTARE_SPRITE_ID,
    LANMOLAS_SPRITE_ID,
    MOLDORM_SPRITE_ID,
    MOTHULA_SPRITE_ID,
    TRINEXX_BLUE_HEAD_SPRITE_ID,
    TRINEXX_MAIN_HEAD_SPRITE_ID,
    TRINEXX_RED_HEAD_SPRITE_ID,
    VITREOUS_SMALL_EYE_SPRITE_ID,
    VITREOUS_SPRITE_ID,
)

if TYPE_CHECKING:
    from . import ALTTPWorld


class Boss:
    def __init__(self, name: str, enemizer_name: str, defeat_rule: Callable, player: int):
        self.name = name
        self.enemizer_name = enemizer_name
        self.defeat_rule = defeat_rule
        self.player = player

    def can_defeat(self, state) -> bool:
        return self.defeat_rule(state, self.player)

    def __repr__(self):
        return f"Boss({self.name})"


def BossFactory(boss: str, player: int) -> Optional[Boss]:
    if boss in boss_table:
        enemizer_name, defeat_rule = boss_table[boss]
        return Boss(boss, enemizer_name, defeat_rule, player)
    raise Exception('Unknown Boss: %s', boss)


BOSS_SWORD_ITEMS = ("Fighter Sword", "Master Sword", "Tempered Sword", "Golden Sword")
BOSS_MELEE_ITEMS = BOSS_SWORD_ITEMS + ("Hammer",)
BOSS_ARROW_ITEMS = ("Bow", "Silver Bow")
BOSS_BOOMERANG_ITEMS = ("Blue Boomerang", "Red Boomerang")
BOSS_CANE_ITEMS = ("Cane of Somaria", "Cane of Byrna")
BOSS_ROD_ITEMS = ("Fire Rod", "Ice Rod")
BOSS_MEDALLION_ITEMS = ("Bombos", "Ether", "Quake")
# Generic ancilla damage reaches active, same-floor sprites through Ancilla_CheckSpriteDamage.
# See Bank08.asm:402-472, Bank08.asm:1260-1316, Bank08.asm:1740-1826,
# ancilla_magic_powder.asm:250-253, and Bank06.asm:4653-4667.
BOSS_GENERIC_ATTACK_ITEMS = (
    BOSS_MELEE_ITEMS
    + BOSS_ARROW_ITEMS
    + BOSS_BOOMERANG_ITEMS
    + ("Hookshot",)
    + BOSS_CANE_ITEMS
    + ("Magic Powder",)
    + BOSS_ROD_ITEMS
    + BOSS_MEDALLION_ITEMS
)
BOSS_BOMB_ABILITIES = ("bombs",)

# No item delivery is excluded here; contact is checked by Sprite_CheckDamageFromPlayerLong
# at sprite_armos_knight.asm:142 and ordinary ancillas use the shared damage paths above.
ARMOS_ATTACK_ITEMS = BOSS_GENERIC_ATTACK_ITEMS
# Quake is excluded because Ancilla_CheckSpriteDamage rejects damage class 0x0F
# unless $0F70 is exactly zero, and Lanmolas only has narrow ground-crossing frames.
LANMOLAS_ATTACK_ITEMS = tuple(item for item in BOSS_GENERIC_ATTACK_ITEMS if item != "Quake")
# Bombs are excluded from the body phase: Bomb_CheckSpriteDamage explicitly skips
# Helmasaur King when $0DB0 >= 3, i.e. after the mask is gone. See Bank08.asm:458-464.
# Other basic ancillas skip only the mask and can hit the body; see Bank08.asm:1295-1316
# and Bank08.asm:1778-1826. Hammer is contact class 3 and reaches the body through
# the Helmasaur contact branch at Bank06.asm:6006-6012.
HELMASAUR_BODY_ATTACK_ITEMS = BOSS_GENERIC_ATTACK_ITEMS
# Hookshot is excluded from damaging Arrghus fuzz: the hookshot branch pulls sprite
# 0x8D before reaching Ancilla_CheckSpriteDamage. See Bank08.asm:1273-1287.
ARRGHUS_FUZZ_ATTACK_ITEMS = tuple(item for item in BOSS_GENERIC_ATTACK_ITEMS if item != "Hookshot")
# No item delivery is excluded from Arrghus body damage while vulnerable; it clears
# impervious status before contact damage at sprite_arrghus.asm:193-198, and ordinary
# ancillas use the shared damage paths above.
ARRGHUS_ATTACK_ITEMS = BOSS_GENERIC_ATTACK_ITEMS
# Magic Powder can affect Moldorm's head, while sustained tail damage remains
# player-contact only. See alttp_sprite_weapon_vulnerability_audit.md.
MOLDORM_ATTACK_ITEMS = BOSS_MELEE_ITEMS + ("Magic Powder",)
# Quake is excluded because Mothula ascends to and fights at nonzero altitude.
MOTHULA_ATTACK_ITEMS = tuple(item for item in BOSS_GENERIC_ATTACK_ITEMS if item != "Quake")
# No item delivery is excluded here; Blind calls Sprite4_CheckDamage at
# sprite_blind_entities.asm:259 and :1175, and ordinary ancillas use the shared paths above.
BLIND_ATTACK_ITEMS = BOSS_GENERIC_ATTACK_ITEMS
# No item delivery is excluded here; Kholdstare shell/body use contact damage at
# sprite_kholdstare.asm:19, :203, and :283, and ordinary ancillas use the shared paths above.
KHOLDSTARE_ATTACK_ITEMS = BOSS_GENERIC_ATTACK_ITEMS
# No item delivery is excluded here; Vitreous and small eyes call damage checks at
# sprite_vitreous.asm:19 and sprite_vitreolus.asm:47, and ordinary ancillas use the shared paths above.
VITREOUS_ATTACK_ITEMS = BOSS_GENERIC_ATTACK_ITEMS
# Trinexx side heads use a boss-specific vulnerable state. Before that state,
# sword and hammer contact is repulsed by $0CAA bit 2 in Bank06.asm:5900-5903.
# Non-melee ancilla/medallion hits can set $0EF0 and trigger the 0x80-frame
# vulnerable state at sprite_sidenexx.asm:43-54; Quake is excluded because
# Bank06.asm:4737-4744 rejects sprites with nonzero altitude.
TRINEXX_HEAD_OPENER_ITEMS = (
    BOSS_ARROW_ITEMS
    + BOSS_BOOMERANG_ITEMS
    + ("Hookshot",)
    + BOSS_CANE_ITEMS
    + ("Magic Powder",)
    + BOSS_ROD_ITEMS
    + ("Bombos", "Ether")
)
TRINEXX_HEAD_OPENER_ABILITIES = ("bombs", "sword_beams")
TRINEXX_HEAD_FOLLOW_UP_ITEMS = BOSS_MELEE_ITEMS
# Projectiles, rods, canes, powder, medallions, and bombs are excluded from the final
# Trinexx body: it temporarily clears impervious status only around
# Sprite_CheckDamageFromPlayerLong, then restores it. See sprite_trinexx.asm:408-420.
TRINEXX_BODY_ATTACK_ITEMS = BOSS_MELEE_ITEMS
# Hammer is excluded by the hardcoded Ganon contact check at Bank06.asm:5784-5791.
# Arrows are excluded from D6 logic because the Ganon-specific silver-arrow vulnerability
# branch only recognizes sprite D7; see Bank06.asm:4712-4724. Both canes can deliver
# class 1 damage to Ganon when his table row permits it.
GANON_D6_ATTACK_ITEMS = (
    BOSS_SWORD_ITEMS
    + BOSS_BOOMERANG_ITEMS
    + ("Hookshot",)
    + BOSS_CANE_ITEMS
    + ("Magic Powder", "Fire Rod", "Ice Rod")
    + BOSS_MEDALLION_ITEMS
)
# Hammer is excluded by the hardcoded Ganon contact check at Bank06.asm:5784-5791.
# Arrows are allowed here because D7 is the sprite handled by the silver-arrow
# vulnerability branch at Bank06.asm:4718-4724.
GANON_D7_ATTACK_ITEMS = (
    BOSS_SWORD_ITEMS
    + BOSS_ARROW_ITEMS
    + BOSS_BOOMERANG_ITEMS
    + ("Hookshot",)
    + BOSS_CANE_ITEMS
    + ("Magic Powder", "Fire Rod", "Ice Rod")
    + BOSS_MEDALLION_ITEMS
)
# Swordless Ganon keeps Hammer because Archipelago patches the swordless fight around it;
# vanilla still blocks Hammer in the shared contact routine cited above.
GANON_D7_SWORDLESS_ATTACK_ITEMS = ("Hammer",) + GANON_D7_ATTACK_ITEMS
GANON_HP_FOR_LOGIC = 0x60
GANON_D6_PHASE_SKIP_DAMAGE = 0x64


def _ganon_torch_relight_magic_per_two_hits(state, player: int) -> int:
    return 0 if state.has("Lamp", player) else FIRE_ROD_MAGIC_COST * 2


def ArmosKnightsDefeatRule(state, player: int) -> bool:
    return can_damage_boss_sprite(
        state,
        player,
        ARMOS_KNIGHTS_SPRITE_ID,
        allowed_items=ARMOS_ATTACK_ITEMS,
    )


def LanmolasDefeatRule(state, player: int) -> bool:
    return can_damage_boss_sprite(
        state,
        player,
        LANMOLAS_SPRITE_ID,
        allowed_items=LANMOLAS_ATTACK_ITEMS,
    )


def MoldormDefeatRule(state, player: int) -> bool:
    return can_damage_boss_sprite(
        state,
        player,
        MOLDORM_SPRITE_ID,
        allowed_items=MOLDORM_ATTACK_ITEMS,
    )


def HelmasaurKingDefeatRule(state, player: int) -> bool:
    return (
        (can_use_bombs(state, player, 5) or state.has("Hammer", player))
        and can_damage_boss_sprite(
            state,
            player,
            HELMASAUR_KING_SPRITE_ID,
            allowed_items=HELMASAUR_BODY_ATTACK_ITEMS,
        )
    )


def ArrghusDefeatRule(state, player: int) -> bool:
    if not state.has('Hookshot', player):
        return False

    fuzz_plans = _get_boss_attack_plans(
        state,
        player,
        ARRGHUS_FUZZ_SPRITE_ID,
        allowed_items=ARRGHUS_FUZZ_ATTACK_ITEMS,
        include_transform_removal=True,
    )
    body_plans = _get_boss_attack_plans(
        state,
        player,
        ARRGHUS_SPRITE_ID,
        allowed_items=ARRGHUS_ATTACK_ITEMS,
    )
    return can_damage_boss_sprite_phases(state, player, fuzz_plans, body_plans)


def MothulaDefeatRule(state, player: int) -> bool:
    return can_get_good_bee(state, player) or can_damage_boss_sprite(
        state,
        player,
        MOTHULA_SPRITE_ID,
        allowed_items=MOTHULA_ATTACK_ITEMS,
    )


def BlindDefeatRule(state, player: int) -> bool:
    return can_damage_blind_sprite(
        state,
        player,
        BLIND_SPRITE_ID,
        allowed_items=BLIND_ATTACK_ITEMS,
    )


def KholdstareDefeatRule(state, player: int) -> bool:
    shell_plans = _get_boss_attack_plans(
        state,
        player,
        KHOLDSTARE_ICE_BLOCK_SPRITE_ID,
        allowed_items=KHOLDSTARE_ATTACK_ITEMS,
        allowed_abilities=BOSS_BOMB_ABILITIES,
    )
    body_plans = _get_boss_attack_plans(
        state,
        player,
        KHOLDSTARE_SPRITE_ID,
        allowed_items=KHOLDSTARE_ATTACK_ITEMS,
        allowed_abilities=BOSS_BOMB_ABILITIES,
    )
    return can_damage_boss_sprite_phases(state, player, shell_plans, body_plans)


def VitreousDefeatRule(state, player: int) -> bool:
    small_eye_plans = _get_boss_attack_plans(
        state,
        player,
        VITREOUS_SMALL_EYE_SPRITE_ID,
        allowed_items=VITREOUS_ATTACK_ITEMS,
    )
    body_plans = _get_boss_attack_plans(
        state,
        player,
        VITREOUS_SPRITE_ID,
        allowed_items=VITREOUS_ATTACK_ITEMS,
    )
    return can_damage_boss_sprite_phases(state, player, small_eye_plans, body_plans)


def TrinexxDefeatRule(state, player: int) -> bool:
    red_head_plans = _get_trinexx_side_head_attack_plans(
        state,
        player,
        TRINEXX_RED_HEAD_SPRITE_ID,
        opener_items=TRINEXX_HEAD_OPENER_ITEMS,
        opener_abilities=TRINEXX_HEAD_OPENER_ABILITIES,
        follow_up_items=TRINEXX_HEAD_FOLLOW_UP_ITEMS,
    )
    blue_head_plans = _get_trinexx_side_head_attack_plans(
        state,
        player,
        TRINEXX_BLUE_HEAD_SPRITE_ID,
        opener_items=TRINEXX_HEAD_OPENER_ITEMS,
        opener_abilities=TRINEXX_HEAD_OPENER_ABILITIES,
        follow_up_items=TRINEXX_HEAD_FOLLOW_UP_ITEMS,
    )
    body_plans = _get_boss_attack_plans(
        state,
        player,
        TRINEXX_MAIN_HEAD_SPRITE_ID,
        allowed_items=TRINEXX_BODY_ATTACK_ITEMS,
    )
    return can_damage_boss_sprite_phases(state, player, red_head_plans, blue_head_plans, body_plans)


def AgahnimDefeatRule(state, player: int) -> bool:
    return has_sword(state, player) or state.has('Hammer', player) or state.has('Bug Catching Net', player)


def GanonDefeatRule(state, player: int) -> bool:
    torch_relight_magic = _ganon_torch_relight_magic_per_two_hits(state, player)
    if state.multiworld.worlds[player].options.swordless:
        return (
            state.has('Hammer', player)
            and has_fire_source(state, player)
            and can_damage_boss_sprite(
                state,
                player,
                GANON_D7_SPRITE_ID,
                allowed_items=GANON_D7_SWORDLESS_ATTACK_ITEMS,
                hp_override=GANON_HP_FOR_LOGIC,
                extra_magic_per_two_hits=torch_relight_magic,
            )
        )

    common = has_fire_source(state, player) and can_hit_boss_sprite(
        state,
        player,
        GANON_D6_SPRITE_ID,
        allowed_items=GANON_D6_ATTACK_ITEMS,
    )
    if not common:
        return False

    if can_hit_boss_sprite_for_at_least_damage(
        state,
        player,
        GANON_D6_SPRITE_ID,
        GANON_D6_PHASE_SKIP_DAMAGE,
        allowed_items=GANON_D6_ATTACK_ITEMS,
    ):
        return True

    d7_kill = can_damage_boss_sprite(
        state,
        player,
        GANON_D7_SPRITE_ID,
        allowed_items=GANON_D7_ATTACK_ITEMS,
        hp_override=GANON_HP_FOR_LOGIC,
        extra_magic_per_two_hits=torch_relight_magic,
    )
    if state.multiworld.worlds[player].options.glitches_required == 'no_glitches':
        return d7_kill

    d6_kill = can_damage_boss_sprite(
        state,
        player,
        GANON_D6_SPRITE_ID,
        allowed_items=GANON_D6_ATTACK_ITEMS,
        hp_override=GANON_HP_FOR_LOGIC,
        extra_magic_per_two_hits=torch_relight_magic,
    )
    return d7_kill or d6_kill


boss_table: Dict[str, Tuple[str, Optional[Callable]]] = {
    'Armos Knights': ('Armos', ArmosKnightsDefeatRule),
    'Lanmolas': ('Lanmola', LanmolasDefeatRule),
    'Moldorm': ('Moldorm', MoldormDefeatRule),
    'Helmasaur King': ('Helmasaur', HelmasaurKingDefeatRule),
    'Arrghus': ('Arrghus', ArrghusDefeatRule),
    'Mothula': ('Mothula', MothulaDefeatRule),
    'Blind': ('Blind', BlindDefeatRule),
    'Kholdstare': ('Kholdstare', KholdstareDefeatRule),
    'Vitreous': ('Vitreous', VitreousDefeatRule),
    'Trinexx': ('Trinexx', TrinexxDefeatRule),
    'Agahnim': ('Agahnim', AgahnimDefeatRule),
    'Agahnim2': ('Agahnim2', AgahnimDefeatRule)
}

BOSS_DAMAGE_CLASS_SPRITE_IDS_BY_BOSS_NAME = {
    "Armos Knights": frozenset({ARMOS_KNIGHTS_SPRITE_ID}),
    "Lanmolas": frozenset({LANMOLAS_SPRITE_ID}),
    "Moldorm": frozenset({MOLDORM_SPRITE_ID}),
    "Helmasaur King": frozenset({HELMASAUR_KING_SPRITE_ID}),
    "Arrghus": frozenset({ARRGHUS_SPRITE_ID, ARRGHUS_FUZZ_SPRITE_ID}),
    "Mothula": frozenset({MOTHULA_SPRITE_ID}),
    "Blind": frozenset({BLIND_SPRITE_ID}),
    "Kholdstare": frozenset({KHOLDSTARE_SPRITE_ID, KHOLDSTARE_ICE_BLOCK_SPRITE_ID}),
    "Vitreous": frozenset({VITREOUS_SPRITE_ID, VITREOUS_SMALL_EYE_SPRITE_ID}),
    "Trinexx": frozenset({TRINEXX_MAIN_HEAD_SPRITE_ID, TRINEXX_RED_HEAD_SPRITE_ID, TRINEXX_BLUE_HEAD_SPRITE_ID}),
}

boss_location_table: List[Tuple[str, str]] = [
        ('Ganons Tower', 'top'),
        ('Tower of Hera', None),
        ('Skull Woods', None),
        ('Ganons Tower', 'middle'),
        ('Eastern Palace', None),
        ('Desert Palace', None),
        ('Palace of Darkness', None),
        ('Swamp Palace', None),
        ('Thieves Town', None),
        ('Ice Palace', None),
        ('Misery Mire', None),
        ('Turtle Rock', None),
        ('Ganons Tower', 'bottom'),
    ]


def place_plando_bosses(world: "ALTTPWorld", bosses: List[str]) -> Tuple[List[str], List[Tuple[str, str]]]:
    # Most to least restrictive order
    boss_locations = boss_location_table.copy()
    world.multiworld.random.shuffle(boss_locations)
    boss_locations.sort(key=lambda location: -int(restrictive_boss_locations[location]))
    already_placed_bosses: List[str] = []

    for boss in bosses:
        if "-" in boss:  # handle plando locations
            loc, boss = boss.split("-")
            boss = boss.title()
            level: str = None
            if loc.split(" ")[-1] in {"top", "middle", "bottom"}:
                # split off level
                loc = loc.split(" ")
                level = loc[-1]
                loc = " ".join(loc[:-1])
            loc = loc.title().replace("Of", "of")
            place_boss(world, boss, loc, level)
            already_placed_bosses.append(boss)
            boss_locations.remove((loc, level))
        else:  # boss chosen with no specified locations
            boss = boss.title()
            boss_locations, already_placed_bosses = place_where_possible(world, boss, boss_locations)

    return already_placed_bosses, boss_locations


def can_place_boss(boss: str, dungeon_name: str, level: Optional[str] = None) -> bool:
    # blacklist approach
    if boss in {"Agahnim", "Agahnim2", "Ganon"}:
        return False

    if dungeon_name == 'Ganons Tower':
        if level == 'top':
            if boss in {"Armos Knights", "Arrghus", "Blind", "Trinexx", "Lanmolas"}:
                return False
        elif level == 'middle':
            if boss == "Blind":
                return False

    elif dungeon_name == 'Tower of Hera':
        if boss in {"Armos Knights", "Arrghus", "Blind", "Trinexx", "Lanmolas"}:
            return False

    elif dungeon_name == 'Skull Woods':
        if boss == "Trinexx":
            return False

    return True


restrictive_boss_locations: Dict[Tuple[str, str], bool] = {}
for location in boss_location_table:
    restrictive_boss_locations[location] = not all(can_place_boss(boss, *location)
                                               for boss in boss_table if not boss.startswith("Agahnim"))


def place_boss(world: "ALTTPWorld", boss: str, location: str, level: Optional[str]) -> None:
    player = world.player
    if location == 'Ganons Tower' and world.options.mode == 'inverted':
        location = 'Inverted Ganons Tower'
    logging.debug('Placing boss %s at %s', boss, location + (' (' + level + ')' if level else ''))
    world.dungeons[location].bosses[level] = BossFactory(boss, player)


def get_gt_only_boss_damage_class_sprite_ids(world: "ALTTPWorld") -> frozenset[int]:
    gt_dungeon_names = {"Ganons Tower", "Inverted Ganons Tower"}
    placements_by_boss: dict[str, set[str]] = {}
    for dungeon_name, dungeon in world.dungeons.items():
        for boss in dungeon.bosses.values():
            if boss is None or boss.name not in BOSS_DAMAGE_CLASS_SPRITE_IDS_BY_BOSS_NAME:
                continue
            placements_by_boss.setdefault(boss.name, set()).add(dungeon_name)

    allowed_sprite_ids: set[int] = set()
    for boss_name, dungeon_names in placements_by_boss.items():
        if dungeon_names and dungeon_names <= gt_dungeon_names:
            allowed_sprite_ids.update(BOSS_DAMAGE_CLASS_SPRITE_IDS_BY_BOSS_NAME[boss_name])
    return frozenset(allowed_sprite_ids)


def format_boss_location(location_name: str, level: str) -> str:
    return location_name + (' (' + level + ')' if level else '')


def encode_ut_bosses(world: "ALTTPWorld") -> dict[str, dict[str, str]]:
    bosses = {}
    for dungeon_name, dungeon in world.dungeons.items():
        dungeon_bosses = {
            str(level) if level is not None else "main": boss.name
            for level, boss in dungeon.bosses.items()
            if boss is not None
        }
        if dungeon_bosses:
            bosses[dungeon_name] = dungeon_bosses
    return bosses


def apply_ut_bosses(world: "ALTTPWorld", bosses: dict[str, dict[str, str]]) -> bool:
    if not bosses:
        return False

    for dungeon_name, dungeon_bosses in bosses.items():
        dungeon = world.dungeons[dungeon_name]
        for level_name, boss_name in dungeon_bosses.items():
            level = None if level_name == "main" else level_name
            dungeon.bosses[level] = BossFactory(boss_name, world.player)
    return True


def place_bosses(world: "ALTTPWorld") -> None:
    if getattr(world, "ut_replay_data", None):
        from . import _get_ut_replay_value

        bosses = _get_ut_replay_value(world.ut_replay_data, "ut_bosses", "bosses")
        if apply_ut_bosses(world, bosses):
            return

    multiworld = world.multiworld
    # will either be an int or a lower case string with ';' between options
    boss_shuffle: Union[str, int] = world.options.boss_shuffle.value
    already_placed_bosses: List[str] = []
    remaining_locations: List[Tuple[str, str]] = []
    # handle plando
    if isinstance(boss_shuffle, str):
        # figure out our remaining mode, convert it to an int and remove it from plando_args
        options = boss_shuffle.split(";")
        boss_shuffle = Bosses.options[options.pop()]
        # place our plando bosses
        already_placed_bosses, remaining_locations = place_plando_bosses(world, options)
    if boss_shuffle == Bosses.option_none:  # vanilla boss locations
        return

    # Most to least restrictive order
    if not remaining_locations and not already_placed_bosses:
        remaining_locations = boss_location_table.copy()
    multiworld.random.shuffle(remaining_locations)
    remaining_locations.sort(key=lambda location: -int(restrictive_boss_locations[location]))

    all_bosses = sorted(boss_table.keys())  # sorted to be deterministic on older pythons
    placeable_bosses = [boss for boss in all_bosses if boss not in ['Agahnim', 'Agahnim2', 'Ganon']]

    if boss_shuffle == Bosses.option_basic or boss_shuffle == Bosses.option_full:
        if boss_shuffle == Bosses.option_basic:  # vanilla bosses shuffled
            bosses = placeable_bosses + ['Armos Knights', 'Lanmolas', 'Moldorm']
        else:  # all bosses present, the three duplicates chosen at random
            bosses = placeable_bosses + multiworld.random.sample(placeable_bosses, 3)

        # there is probably a better way to do this
        while already_placed_bosses:
            # remove already manually placed bosses, to prevent for example triple Lanmolas
            boss = already_placed_bosses.pop()
            if boss in bosses:
                bosses.remove(boss)
            # there may be more bosses than locations at this point, depending on manual placement

        logging.debug('Bosses chosen %s', bosses)

        multiworld.random.shuffle(bosses)
        for loc, level in remaining_locations:
            for _ in range(len(bosses)):
                boss = bosses.pop()
                if can_place_boss(boss, loc, level):
                    break
                # put the boss back in queue
                bosses.insert(0, boss)  # this would be faster with deque,
                # but the deque size is small enough that it should not matter

            else:
                raise FillError(f'Could not place boss for location {format_boss_location(loc, level)}')

            place_boss(world, boss, loc, level)

    elif boss_shuffle == Bosses.option_chaos:  # all bosses chosen at random
        for loc, level in remaining_locations:
            try:
                boss = multiworld.random.choice(
                    [b for b in placeable_bosses if can_place_boss(b, loc, level)])
            except IndexError:
                raise FillError(f'Could not place boss for location {format_boss_location(loc, level)}')
            else:
                place_boss(world, boss, loc, level)

    elif boss_shuffle == Bosses.option_singularity:
        primary_boss = multiworld.random.choice(placeable_bosses)
        remaining_boss_locations, _ = place_where_possible(world, primary_boss, remaining_locations)
        if remaining_boss_locations:
            # pick a boss to go into the remaining locations
            remaining_boss = multiworld.random.choice([boss for boss in placeable_bosses if all(
                can_place_boss(boss, loc, level) for loc, level in remaining_boss_locations)])
            remaining_boss_locations, _ = place_where_possible(world, remaining_boss, remaining_boss_locations)
            if remaining_boss_locations:
                raise Exception("Unfilled boss locations!")
    else:
        raise FillError(f"Could not find boss shuffle mode {boss_shuffle}")


def place_where_possible(world: "ALTTPWorld", boss: str, boss_locations) -> Tuple[List[Tuple[str, str]], List[str]]:
    remainder: List[Tuple[str, str]] = []
    placed_bosses: List[str] = []
    for loc, level in boss_locations:
        # place that boss where it can go
        if can_place_boss(boss, loc, level):
            place_boss(world, boss, loc, level)
            placed_bosses.append(boss)
        else:
            remainder.append((loc, level))
    return remainder, placed_bosses
