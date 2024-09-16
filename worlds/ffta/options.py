"""
Option definitions for Final Fantasy Tactics Advance
"""
from typing import Dict
from dataclasses import dataclass
from Options import Choice, DefaultOnToggle, Option, OptionSet, Range, Toggle, FreeText, DeathLink, PerGameCommonOptions


class StartingUnits(Choice):
    """
    Sets the option for your starting units

    Vanilla: The same starting units as the original game
    Shuffle: Jobs are randomized within the original starting races of the game.
    Random: Jobs and race of the starting units are randomized
    Balanced: Ensures two attacker jobs, two magic jobs, and two support jobs. Excludes morphers, beastmasters, and gadgeteers.
    Random Monster: Starting units jobs and race are randomized with monster units also in the pool

    Note: Monsters are unable to change jobs, equip anything or use items.
    """
    display_name = "Starting units"
    default = 0
    option_starting_vanilla = 0
    option_starting_shuffle = 1
    option_starting_random = 2
    option_starting_balanced = 3
    option_random_monster = 4


class StartingUnitEquip(Choice):
    """
    Sets the equipment option for your starting units

    Basic: Units will always start with their most basic equipment
    Randomized: The equipment load out will be random within the job's equipment
    """
    display_name = "Starting unit equipment"
    default = 0
    option_equip_basic = 0
    option_equip_random = 1


class StartingAbilitiesMastered(Range):
    """
    Sets the amount of mastered abilities for each starting unit's job. Based on percentage. 1 = 10% and 10 = 100% of abilities mastered
    """
    display_name = "Percent of starting abilities mastered"
    default = 0
    range_start = 0
    range_end = 10


class JobUnlockReq(Choice):
    """
    Sets the unlock requirements for every unit's job

    Vanilla: Job unlock requirements are the same as vanilla
    All Unlocked: All jobs are unlocked from the start
    All Locked: All jobs are locked. The unit must use their assigned job and cannot change
    """
    display_name = "Job Unlock Requirements"
    default = 0
    option_req_vanilla = 0
    option_all_unlocked = 1
    option_all_locked = 2
    #FIX THIS
    #option_job_items = 3


class Laws(Choice):
    """
    Enable or disable the law and judge system found in the game. JP will rarely be awarded with laws turned off.

    No Laws: Judges and laws are disabled. Judge units like in Decision Time become random units with all abilities mastered.
    Laws: Laws are vanilla but are enabled. Judge units are vanilla.
    """
    display_name = "Enables or disables laws/judges."
    default = 1
    option_disable_laws = 0
    option_enable_laws = 1


class RandomEnemies(Choice):
    """
    Randomizes the enemy units. Special units such as bosses currently are not randomized.

    Vanilla: Enemies aren't changed
    Randomized: Enemies are randomized
    """
    display_name = "Randomize Enemies"
    default = 0
    option_enemy_vanilla = 0
    option_enemy_random = 1


class EnemyScaling(Choice):
    """
    Sets the level scaling for enemies.

    Average Level: Enemies are scaled to the average level of your units.
    Highest Level: Enemies are scaled to your highest level unit.
    """
    display_name = "Enemy Level Scaling"
    default = 0
    option_average_level = 0
    option_highest_level = 1


class DoubleExp(Toggle):
    """
    Turns on double exp
    """
    display_name = "Double EXP"
    default = 0


class StartingGil(Range):
    """
    Sets the amount of gil you will start with.
    """
    display_name = "Starting gil"
    default = 5000
    range_start = 0
    range_end = 99999999


class GateNumber(Range):
    """
    Sets the number of mission gates. Each gate contains four missions each. Expect an hour added for every gate.
    Royal Valley or Decision Time will always be the last mission depending on options.

    (8 locations added for each gate)
    """
    display_name = "Number of mission gates"
    default = 6
    range_start = 1
    range_end = 28


class GatePaths(Range):
    """
    Sets the number of branching mission gates paths. Each must currently still
    be progressed through to unlock the final mission.
    Useful for higher mission gate counts.
    """
    display_name = "Mission gate paths"
    default = 1
    range_start = 1
    range_end = 3


class DispatchMissions(Range):
    """
    Sets the number of dispatch missions per gate. Each dispatch mission adds two locations for each gate.
    """
    display_name = "Number of dispatch missions"
    default = 0
    range_start = 0
    range_end = 6


class DispatchRandom(Toggle):
    """
    Randomizes the order of the dispatch mission. Setting only has effect is dispatch missions setting is more than 0.
    """
    display_name = "Randomize dispatch missions"
    default = 0


class GateUnlock(Choice):
    """
    Sets how the mission gates are unlocked
    One Mission item: Mission gates are unlocked by one mission item. Gate unlocks both encounter and dispatch missions.
    Two Mission items: Mission gates are unlocked by two mission items. Gate unlocks both encounter and dispatch missions.
    Dispatch mission gate: Dispatch missions are separated into their own gate sequence which each require an item.
    Dispatch missions must be more than 0 for this setting or it will default to one mission item.

    (Adds 1 or 2 progression items to the pool for each gate depending on the setting)
    """
    display_name = "Number of required gate unlock items"
    default = 0
    option_one = 0
    option_two = 1
    option_dispatch_gate = 2


class MissionOrder(Choice):
    """
    Sets the option for the order of missions

    Linear: Missions are in order, with the first 26 being story.
    Story as gate unlocks: The story missions in linear order will be the gate unlock mission for the first 23 gates. Every other mission is random. 
    Randomized: Missions are completely randomized

    """
    display_name = "Mission order"
    default = 0
    option_linear = 0
    option_story_gate = 1
    option_randomized = 2


class FinalMission(Choice):
    """
    Sets what the final mission will be between the two missions that play the credits.
    Royal Valley: The final mission will be Royal Valley. This mission is three phases. Original final mission.
    Decision Time: The final mission will be Decision Time. This mission is one phase.
    """

    display_name = "Final mission"
    default = 0
    option_royal_valley = 0
    option_decision_time = 1


class FinalMissionUnlock(Choice):
    """
    Sets the unlock condition for the final mission

    All mission gates: The final mission is unlocked after going through every mission gate.
    Totemas: A series of the five Totema battles must be cleared to unlock the final mission. The first is unlocked by default and clearing it unlocks the next
    and so on until the final mission is unlocked. Allows for the possibility of not having to go through every mission gate to beat the game. Items required to beat the game
    in totema mode include the four elemental sigils and the old statue and however many gate items are needed to acquire them.
    (Totemas option adds five progression items needed to unlock the totema missions to the pool and 10 item locations, also max gate number with Totema Goal is 31, if set higher, it will be set to 31)
    """
    display_name = "Final Mission Unlock Requirements"
    default = 0
    option_mission_gates = 0
    option_totema = 1


class QuickOptions(Toggle):
    """
    Enables quick options by default which turn off attack names, exp popups, and turns on
    fast text and fast cursor. All of these can be tweaked in the game options. 
    """
    display_name = "Turn on quick options by default"
    default = 0


class ForceRecruitment(Toggle):
    """
    Forces every mission to give a new recruit. 
    """
    display_name = "Force recruitment"
    default = 0


@dataclass
class FFTAOptions(PerGameCommonOptions):
    #"death_link": DeathLink,
    starting_units: StartingUnits
    starting_unit_equip: StartingUnitEquip
    starting_abilities: StartingAbilitiesMastered
    job_unlock_req: JobUnlockReq
    laws: Laws
    randomize_enemies: RandomEnemies
    scaling: EnemyScaling
    double_exp: DoubleExp
    starting_gil: StartingGil
    gate_num: GateNumber
    gate_paths: GatePaths
    dispatch: DispatchMissions
    #"dispatch_chance": DispatchChance
    randomize_dispatch: DispatchRandom
    gate_items: GateUnlock
    mission_order: MissionOrder
    final_mission: FinalMission
    final_unlock: FinalMissionUnlock
    quick_options: QuickOptions
    force_recruitment: ForceRecruitment

