"""
Archipelago World definition for Final Fantasy Tactics Advance
"""

import os
from typing import ClassVar, Dict, Any
import settings
import sys
import logging
from Utils import visualize_regions

from .client import FFTAClient

from BaseClasses import ItemClassification, MultiWorld, Tutorial
from worlds.AutoWorld import WebWorld, World
from .data import get_random_job, JobID, attacker_jobs, magic_jobs, support_jobs
from .regions import create_regions
from .rules import set_rules

from .options import (FFTAOptions, StartingUnits, StartingUnitEquip, StartingAbilitiesMastered, JobUnlockReq, RandomEnemies,
                      EnemyScaling, DoubleExp, StartingGil, GateNumber, GatePaths, DispatchMissions, DispatchRandom, GateUnlock,
                      MissionOrder, FinalMission, FinalMissionUnlock, QuickOptions, ForceRecruitment)
from .items import (create_item_label_to_code_map, AllItems, item_table, FFTAItem, WeaponBlades,
                    WeaponSabers, WeaponKatanas, WeaponBows, WeaponGreatBows, WeaponRods, WeaponStaves, WeaponKnuckles,
                    WeaponMaces, WeaponInstruments, WeaponSouls, WeaponRapiers, WeaponGuns, WeaponKnives, ItemData,
                    EquipArmor, EquipRobes, EquipClothing, MissionUnlockItems, TotemaUnlockItems,
                    SoldierWeapons, PaladinWeapons, WarriorWeapons, DefenderWeapons, TemplarWeapons, AssassinWeapons,
                    DragoonWeapons)
from .locations import (create_location_label_to_id_map)
from .rom import FFTADeltaPatch, generate_output


class FFTAWebWorld(WebWorld):
    """
    Webhost info for Final Fantasy Tactics Advance
    """
    theme = "grass"
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to playing Final Fantasy Tactics Advance with Archipelago.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Spicynun"]
    )

    tutorials = [setup_en]


class FFTASettings(settings.Group):
    class FFTARomFile(settings.UserFilePath):
        """File name of your Final Fantasy Tactics Advance ROM"""
        description = "Final Fantasy Tactics Advance ROM File"
        copy_to = "Final Fantasy Tactics Advance (USA).gba"
        md5s = [FFTADeltaPatch.hash]

    rom_file: FFTARomFile = FFTARomFile(FFTARomFile.copy_to)


class FFTAWorld(World):
    """
    Final Fantasy Tactics Advance is a game
    """
    game = "Final Fantasy Tactics Advance"
    web = FFTAWebWorld()
    topology_present = True

    settings_key = "ffta_options"
    settings: ClassVar[FFTASettings]

    options_dataclass = FFTAOptions
    options: FFTAOptions

    required_client_version = (0, 4, 4)

    item_name_to_id = create_item_label_to_code_map()
    location_name_to_id = create_location_label_to_id_map()
        
    randomized_jobs = []
    balanced_jobs = []
    randomized_judge = []
    judge_weapon = []
    judge_equip = []
    randomized_weapons = []
    randomized_equip = []
    randomized_abilities = []
    basic_weapon = []
    basic_equip = []
    MissionGroups = []
    DispatchMissionGroups = []
    location_ids = []
    path1_length = []
    path2_length = []
    path3_length = []

    def get_filler_item_name(self) -> str:
        filler = ["Potion", "Hi-Potion", "X-Potion", "Ether", "Elixir", "Antidote",
        "Eye Drops", "Echo Screen", "Maiden's Kiss", "Soft", "Holy Water", "Bandage",
        "Cureall", "Phoenix Down"]
        return self.random.choice(filler)

    def create_regions(self) -> None:
        create_regions(self, self.player)

    def create_items(self):

        required_items = []

        item_index = 0
        req_gate_num = self.options.gate_num.value

        # Add progression items with multiple mission gate paths
        if self.options.gate_paths.value == 2:
            req_gate_num = req_gate_num + 1

        elif self.options.gate_paths.value == 3:
            req_gate_num = req_gate_num + 2

        for i in range(0, req_gate_num):
            required_items.append(MissionUnlockItems[item_index].itemName)

            # Add second item for the gate unlock
            if self.options.gate_items == GateUnlock.option_two or self.options.gate_items == GateUnlock.option_dispatch_gate:
                required_items.append(MissionUnlockItems[item_index + 1].itemName)

            item_index = item_index + 2

        # Add totema unlock items to pool if option is selected
        if self.options.final_unlock == FinalMissionUnlock.option_totema:
            for i in range(0, len(TotemaUnlockItems)):
                required_items.append(TotemaUnlockItems[i].itemName)

        # Adding required items to the pool first
        for itemName in required_items:
            self.multiworld.itempool.append(self.create_item(itemName))

        # Count number of mission reward locations, account for totema goal
        gate_number = self.options.gate_num.value
        if gate_number > 30 and self.options.final_unlock == FinalMissionUnlock.option_totema:
            gate_number = 30

        dispatch_number = self.options.dispatch.value * 2
        unfilled_locations = gate_number * 8 + gate_number * dispatch_number + 1

        # Add totema mission locations to unfilled location count
        if self.options.final_unlock == FinalMissionUnlock.option_totema:
            unfilled_locations = unfilled_locations + 10

        useful_items = []
        for item in AllItems:
            if item.progression == ItemClassification.useful:

                #To DO: add back in job unlock items self.options.job_unlock_req != JobUnlockReq.option_job_items
                if item.itemID >= 0x2ac:
                    continue

                else:
                    useful_items += [item.itemName]

        # Shuffle the useful items to be added to the pool based on the locations remaining
        self.random.shuffle(useful_items)

        items_remaining = unfilled_locations - len(required_items)

        # Add extra locations for multiple gate paths
        if self.options.gate_paths.value == 2:
            items_remaining = items_remaining + 2

        elif self.options.gate_paths.value == 3:
            items_remaining = items_remaining + 4

        for i in range(items_remaining - 1):
            if i > len(useful_items) - 1:
                self.multiworld.itempool.append(self.create_filler())
            else:
                self.multiworld.itempool.append(self.create_item(useful_items[i]))

    def set_rules(self) -> None:
        set_rules(self)

    def generate_basic(self) -> None:
        # Setting the victory item at the victory location
        victory_event = FFTAItem('Victory', ItemClassification.progression, None, self.player)

        if self.options.final_mission == FinalMission.option_royal_valley:
            self.multiworld.get_location("Royal Valley", self.player)\
                .place_locked_item(victory_event)

        elif self.options.final_mission == FinalMission.option_decision_time:
            self.multiworld.get_location("Decision Time", self.player) \
                .place_locked_item(victory_event)

        self.multiworld.completion_condition[self.player] =\
            lambda state: state.has("Victory", self.player)

        if self.options.gate_paths.value == 2:
            path1_complete = FFTAItem('Path 1 Complete', ItemClassification.progression, None, self.player)
            path2_complete = FFTAItem('Path 2 Complete', ItemClassification.progression, None, self.player)

            self.multiworld.get_location("Path 1 Completion", self.player) \
                .place_locked_item(path1_complete)

            self.multiworld.get_location("Path 2 Completion", self.player) \
                .place_locked_item(path2_complete)

        elif self.options.gate_paths.value == 3:
            path1_complete = FFTAItem('Path 1 Complete', ItemClassification.progression, None, self.player)
            path2_complete = FFTAItem('Path 2 Complete', ItemClassification.progression, None, self.player)
            path3_complete = FFTAItem('Path 3 Complete', ItemClassification.progression, None, self.player)

            self.multiworld.get_location("Path 1 Completion", self.player) \
                .place_locked_item(path1_complete)

            self.multiworld.get_location("Path 2 Completion", self.player) \
                .place_locked_item(path2_complete)

            self.multiworld.get_location("Path 3 Completion", self.player) \
                .place_locked_item(path3_complete)



    @classmethod
    def stage_assert_generate(cls, multiworld: MultiWorld):
        if not os.path.exists(cls.settings.rom_file):
            raise FileNotFoundError(cls.settings.rom_file)

    def fill_slot_data(self) -> Dict[str, Any]:

        slot_data = self.options.as_dict(
            "final_mission",
            "job_unlock_req"
        )

        return slot_data

    def create_item(self, name: str) -> "Item":
        item = item_table[name]
        # Maybe remove this later
        offset = 41234532
        return FFTAItem(item.itemName, item.progression, item.itemID + offset, self.player)

    def generate_output(self, output_directory: str) -> None:
    
        # Import this from data instead
        human = 0
        bangaa = 1
        mou = 2
        viera = 3
        moogle = 4
        monster = 5
        all = 6
        all_with_monster = 7
        
        self.randomized_jobs = []
        self.balanced_jobs = []
        self.randomized_judge = []
        self.judge_weapon = []
        self.judge_equip = []
        self.randomized_weapons = []
        self.randomized_equip = []
        self.randomized_abilities = []
        self.basic_weapon = []
        self.basic_equip = []

        if self.options.starting_units == StartingUnits.option_starting_balanced:
            self.balanced_jobs.append(self.random.choice(attacker_jobs))
            self.balanced_jobs.append(self.random.choice(attacker_jobs))
            self.balanced_jobs.append(self.random.choice(magic_jobs))
            self.balanced_jobs.append(self.random.choice(magic_jobs))
            self.balanced_jobs.append(self.random.choice(support_jobs))
            self.balanced_jobs.append(self.random.choice(support_jobs))
            self.random.shuffle(self.balanced_jobs)

        def randomize_starting(random_choice: int):

            # Randomize job for Marche

            # Add balanced job if selected
            if self.options.starting_units == StartingUnits.option_starting_balanced:
                self.randomized_jobs.append(self.balanced_jobs[0])

            else:
                self.randomized_jobs.append(get_random_job(self.random, random_choice))

            if self.options.starting_unit_equip == StartingUnitEquip.option_equip_basic:
                self.basic_weapon.append(get_basic_weapon(self.randomized_jobs[0]))
                self.basic_equip.append(get_basic_equip(self.randomized_jobs[0]))

            self.randomized_weapons.append(get_valid_weapon(self.randomized_jobs[0]))
            self.randomized_equip.append(get_valid_equip(self.randomized_jobs[0]))

            # Randomize job for Montblanc

            if self.options.starting_units == StartingUnits.option_starting_balanced:
                self.randomized_jobs.append(self.balanced_jobs[1])

            else:
                self.randomized_jobs.append(get_random_job(self.random, random_choice))

            if self.options.starting_unit_equip == StartingUnitEquip.option_equip_basic:

                self.basic_weapon.append(get_basic_weapon(self.randomized_jobs[1]))
                self.basic_equip.append(get_basic_equip(self.randomized_jobs[1]))

            self.randomized_weapons.append(get_valid_weapon(self.randomized_jobs[1]))
            self.randomized_equip.append(get_valid_equip(self.randomized_jobs[1]))

            # Randomize job for third clan member

            if self.options.starting_units == StartingUnits.option_starting_balanced:
                self.randomized_jobs.append(self.balanced_jobs[2])

            else:
                self.randomized_jobs.append(get_random_job(self.random, random_choice))

            if self.options.starting_unit_equip == StartingUnitEquip.option_equip_basic:
                self.basic_weapon.append(get_basic_weapon(self.randomized_jobs[2]))
                self.basic_equip.append(get_basic_equip(self.randomized_jobs[2]))

            self.randomized_weapons.append(get_valid_weapon(self.randomized_jobs[2]))
            self.randomized_equip.append(get_valid_equip(self.randomized_jobs[2]))

            # Randomize job for fourth clan member

            if self.options.starting_units == StartingUnits.option_starting_balanced:
                self.randomized_jobs.append(self.balanced_jobs[3])

            else:
                self.randomized_jobs.append(get_random_job(self.random, random_choice))

            if self.options.starting_unit_equip == StartingUnitEquip.option_equip_basic:
                self.basic_weapon.append(get_basic_weapon(self.randomized_jobs[3]))
                self.basic_equip.append(get_basic_equip(self.randomized_jobs[3]))

            self.randomized_weapons.append(get_valid_weapon(self.randomized_jobs[3]))
            self.randomized_equip.append(get_valid_equip(self.randomized_jobs[3]))

            # Randomize job for fifth clan member

            if self.options.starting_units == StartingUnits.option_starting_balanced:
                self.randomized_jobs.append(self.balanced_jobs[4])

            else:
                self.randomized_jobs.append(get_random_job(self.random, random_choice))

            if self.options.starting_unit_equip == StartingUnitEquip.option_equip_basic:
                self.basic_weapon.append(get_basic_weapon(self.randomized_jobs[4]))
                self.basic_equip.append(get_basic_equip(self.randomized_jobs[4]))

            self.randomized_weapons.append(get_valid_weapon(self.randomized_jobs[4]))
            self.randomized_equip.append(get_valid_equip(self.randomized_jobs[4]))

            # Randomize job for sixth clan member

            if self.options.starting_units == StartingUnits.option_starting_balanced:
                self.randomized_jobs.append(self.balanced_jobs[5])

            else:
                self.randomized_jobs.append(get_random_job(self.random, random_choice))

            if self.options.starting_unit_equip == StartingUnitEquip.option_equip_basic:
                self.basic_weapon.append(get_basic_weapon(self.randomized_jobs[5]))
                self.basic_equip.append(get_basic_equip(self.randomized_jobs[5]))

            self.randomized_weapons.append(get_valid_weapon(self.randomized_jobs[5]))
            self.randomized_equip.append(get_valid_equip(self.randomized_jobs[5]))

        def get_valid_weapon(job: int):

            weapon: ItemData

            # Soldier
            if job == JobID.soldier:
                weapon = self.random.choice(SoldierWeapons)
                return weapon.itemID

            # Paladin
            elif job == JobID.paladin:
                weapon = self.random.choice(PaladinWeapons)
                return weapon.itemID

            # Fighter
            elif job == JobID.fighter:
                weapon = self.random.choice(WeaponBlades)
                return weapon.itemID

            # Thief
            elif job == JobID.thiefhum or job == JobID.thiefmog or job == JobID.juggler:
                weapon = self.random.choice(WeaponKnives)
                return weapon.itemID

            # Ninja and assassins
            elif job == JobID.ninja:
                weapon = self.random.choice(WeaponKatanas)
                return weapon.itemID

            # White mage
            elif job == JobID.whitemagehum or job == JobID.whitemagemou or job == JobID.whitemagevra or job == JobID.summoner:
                weapon = self.random.choice(WeaponStaves)
                return weapon.itemID

            # Rod users
            elif job == JobID.blackmagehum or job == JobID.illusionisthum or job == JobID.blackmagemou \
                    or job == JobID.timemagemou or job == JobID.illusionistmou or job == JobID.blackmagemog or job == JobID.timemagemog:
                weapon = self.random.choice(WeaponRods)
                return weapon.itemID

            # Blue mage
            elif job == JobID.bluemage:
                weapon = self.random.choice(WeaponSabers)
                return weapon.itemID

            # Archer
            elif job == JobID.archerhum or job == JobID.archervra:
                weapon = self.random.choice(WeaponBows)
                return weapon.itemID

            # Hunter or Snipers
            elif job == JobID.hunter or job == JobID.sniper:
                weapon = self.random.choice(WeaponGreatBows)
                return weapon.itemID

            # Warrior
            elif job == JobID.warrior:
                weapon = self.random.choice(WarriorWeapons)
                return weapon.itemID

            # Dragoon
            elif job == JobID.dragoon:
                weapon = self.random.choice(DragoonWeapons)
                return weapon.itemID

            # Defender
            elif job == JobID.defender:
                weapon = self.random.choice(DefenderWeapons)
                return weapon.itemID

            # Gladiator and Mog Knight
            elif job == JobID.gladiator or job == JobID.mogknight:
                weapon = self.random.choice(WeaponBlades)
                return weapon.itemID

            # White monk and gadgeteer
            elif job == JobID.whitemonk or job == JobID.gadgeteer:
                weapon = self.random.choice(WeaponKnuckles)
                return weapon.itemID

            # Bishop
            elif job == JobID.bishop:
                weapon = self.random.choice(WeaponStaves)
                return weapon.itemID

            # Templar
            elif job == JobID.templar:
                weapon = self.random.choice(TemplarWeapons)
                return weapon.itemID

            # Alchemist and sage
            elif job == JobID.alchemist or job == JobID.sage:
                weapon = self.random.choice(WeaponMaces)
                return weapon.itemID

            # Beasmaster or animist
            elif job == JobID.beastmaster or job == JobID.animist:
                weapon = self.random.choice(WeaponInstruments)
                return weapon.itemID

            # Morpher
            elif job == JobID.morpher:
                weapon = self.random.choice(WeaponSouls)
                return weapon.itemID

            # Fencer, red mage and Elementalist
            elif job == JobID.fencer or job == JobID.elementalist or job == JobID.redmage:
                weapon = self.random.choice(WeaponRapiers)
                return weapon.itemID

            # Assassin
            elif job == JobID.assassin:
                weapon = self.random.choice(AssassinWeapons)
                return weapon.itemID

            # Gunner
            elif job == JobID.gunner:
                weapon = self.random.choice(WeaponGuns)
                return weapon.itemID

            else:
                weapon = 0
                return weapon

        def get_basic_weapon(job: int):

            weapon: ItemData

            # Soldier
            if job == JobID.soldier:
                return SoldierWeapons[0].itemID

            # Paladin
            elif job == JobID.paladin:
                return PaladinWeapons[0].itemID

            # Fighter
            elif job == JobID.fighter:
                return WeaponBlades[0].itemID

            # Thief
            elif job == JobID.thiefhum or job == JobID.thiefmog or job == JobID.juggler:
                return WeaponKnives[0].itemID

            # Ninja
            elif job == JobID.ninja:
                return WeaponKatanas[0].itemID

            # White mage
            elif job == JobID.whitemagehum or job == JobID.whitemagemou or job == JobID.whitemagevra or job == JobID.summoner:
                return WeaponStaves[0].itemID

            # Rod users
            elif job == JobID.blackmagehum or job == JobID.illusionisthum or job == JobID.blackmagemou \
                    or job == JobID.timemagemou or job == JobID.illusionistmou or job == JobID.blackmagemog or job == JobID.timemagemog:
                return WeaponRods[0].itemID

            # Blue mage
            elif job == JobID.bluemage:
                return WeaponSabers[0].itemID

            # Archer
            elif job == JobID.archerhum or job == JobID.archervra:
                return WeaponBows[0].itemID

            # Hunter or Snipers
            elif job == JobID.hunter or job == JobID.sniper:
                return WeaponGreatBows[0].itemID

            # Warrior
            elif job == JobID.warrior:
                return WarriorWeapons[0].itemID

            # Dragoon
            elif job == JobID.dragoon:
                return DragoonWeapons[0].itemID

            # Defender
            elif job == JobID.defender:
                return DefenderWeapons[0].itemID

            # Gladiator and Mog Knight
            elif job == JobID.gladiator or job == JobID.mogknight:
                return WeaponBlades[0].itemID

            # White monk and gadgeteer
            elif job == JobID.whitemonk or job == JobID.gadgeteer:
                return WeaponKnuckles[0].itemID

            # Bishop
            elif job == JobID.bishop:
                return WeaponStaves[0].itemID

            # Templar
            elif job == JobID.templar:
                return TemplarWeapons[0].itemID

            # Alchemist and sage
            elif job == JobID.alchemist or job == JobID.sage:
                return WeaponMaces[0].itemID

            # Beasmaster or animist
            elif job == JobID.beastmaster or job == JobID.animist:
                return WeaponInstruments[0].itemID

            # Morpher
            elif job == JobID.morpher:
                return WeaponSouls[0].itemID

            # Fencer, red mage and Elementalist
            elif job == JobID.fencer or job == JobID.elementalist or job == JobID.redmage:
                return WeaponRapiers[0].itemID

            # Assassin
            elif job == JobID.assassin:
                return AssassinWeapons[0].itemID

            # Gunner
            elif job == JobID.gunner:
                return WeaponGuns[0].itemID

            else:
                weapon = 0
                return weapon

        def get_valid_equip(job: int):
            equip: ItemData

            armor_valid_jobs = [JobID.soldier, JobID.paladin, JobID.warrior, JobID.templar, JobID.dragoon,
                                JobID.defender, JobID.mogknight]

            robe_valid_jobs = [JobID.paladin, JobID.whitemagehum, JobID.whitemagevra, JobID.whitemagevra,
                               JobID.blackmagehum, JobID.blackmagemou, JobID.blackmagemog, JobID.illusionisthum,
                               JobID.illusionistmou, JobID.bluemage, JobID.defender,
                               JobID.bishop, JobID.templar, JobID.timemagemou, JobID.timemagemog, JobID.morpher,
                               JobID.sage, JobID.elementalist, JobID.redmage, JobID.summoner]

            for x in armor_valid_jobs:
                if job == x:
                    equip = self.random.choice(EquipArmor)
                    return equip.itemID

            for x in robe_valid_jobs:
                if job == x:
                    equip = self.random.choice(EquipRobes)
                    return equip.itemID

            if job < 0x2B:
                equip = self.random.choice(EquipClothing)
                return equip.itemID

            else:
                equip = 0
                return equip

        def get_basic_equip(job: int):
            equip: ItemData

            armor_valid_jobs = [JobID.soldier, JobID.paladin, JobID.warrior, JobID.templar, JobID.dragoon,
                                JobID.defender, JobID.mogknight]

            robe_valid_jobs = [JobID.paladin, JobID.whitemagehum, JobID.whitemagevra, JobID.whitemagevra,
                               JobID.blackmagehum, JobID.blackmagemou, JobID.blackmagemog, JobID.illusionisthum,
                               JobID.illusionistmou, JobID.bluemage, JobID.defender,
                               JobID.bishop, JobID.templar, JobID.timemagemou, JobID.timemagemog, JobID.morpher,
                               JobID.sage, JobID.elementalist, JobID.redmage, JobID.summoner]

            for x in armor_valid_jobs:
                if job == x:
                    return EquipArmor[0].itemID

            for x in robe_valid_jobs:
                if job == x:
                    return EquipRobes[0].itemID

            if job < 0x2B:
                return EquipClothing[0].itemID

            else:
                equip = 0
                return equip

        # Append randomized units even if randomization is turned off to allow for random enemies to work
        if self.options.starting_units == StartingUnits.option_starting_vanilla or \
           self.options.starting_units == StartingUnits.option_starting_random or \
           self.options.starting_units == StartingUnits.option_starting_balanced:
            randomize_starting(all)

        # Shuffle starting unit jobs within their race
        elif self.options.starting_units == StartingUnits.option_starting_shuffle:
            self.randomized_jobs.append(get_random_job(self.random, human))

            if self.options.starting_unit_equip == StartingUnitEquip.option_equip_basic:
                self.basic_weapon.append(get_basic_weapon(self.randomized_jobs[0]))
                self.basic_equip.append(get_basic_equip(self.randomized_jobs[0]))

            self.randomized_weapons.append(get_valid_weapon(self.randomized_jobs[0]))
            self.randomized_equip.append(get_valid_equip(self.randomized_jobs[0]))

            # Randomize job for Montblanc
            self.randomized_jobs.append(get_random_job(self.random, moogle))

            if self.options.starting_unit_equip == StartingUnitEquip.option_equip_basic:
                self.basic_weapon.append(get_basic_weapon(self.randomized_jobs[1]))
                self.basic_equip.append(get_basic_equip(self.randomized_jobs[1]))

            self.randomized_weapons.append(get_valid_weapon(self.randomized_jobs[1]))
            self.randomized_equip.append(get_valid_equip(self.randomized_jobs[1]))

            # Randomize job for third clan member
            self.randomized_jobs.append(get_random_job(self.random, human))

            if self.options.starting_unit_equip == StartingUnitEquip.option_equip_basic:
                self.basic_weapon.append(get_basic_weapon(self.randomized_jobs[2]))
                self.basic_equip.append(get_basic_equip(self.randomized_jobs[2]))

            self.randomized_weapons.append(get_valid_weapon(self.randomized_jobs[2]))
            self.randomized_equip.append(get_valid_equip(self.randomized_jobs[2]))

            # Randomize job for fourth clan member
            self.randomized_jobs.append(get_random_job(self.random, bangaa))

            if self.options.starting_unit_equip == StartingUnitEquip.option_equip_basic:
                self.basic_weapon.append(get_basic_weapon(self.randomized_jobs[3]))
                self.basic_equip.append(get_basic_equip(self.randomized_jobs[3]))

            self.randomized_weapons.append(get_valid_weapon(self.randomized_jobs[3]))
            self.randomized_equip.append(get_valid_equip(self.randomized_jobs[3]))

            # Randomize job for fifth clan member
            self.randomized_jobs.append(get_random_job(self.random, mou))

            if self.options.starting_unit_equip == StartingUnitEquip.option_equip_basic:
                self.basic_weapon.append(get_basic_weapon(self.randomized_jobs[4]))
                self.basic_equip.append(get_basic_equip(self.randomized_jobs[4]))

            self.randomized_weapons.append(get_valid_weapon(self.randomized_jobs[4]))
            self.randomized_equip.append(get_valid_equip(self.randomized_jobs[4]))

            # Randomize job for sixth clan member
            self.randomized_jobs.append(get_random_job(self.random, viera))

            if self.options.starting_unit_equip == StartingUnitEquip.option_equip_basic:
                self.basic_weapon.append(get_basic_weapon(self.randomized_jobs[5]))
                self.basic_equip.append(get_basic_equip(self.randomized_jobs[5]))

            self.randomized_weapons.append(get_valid_weapon(self.randomized_jobs[5]))
            self.randomized_equip.append(get_valid_equip(self.randomized_jobs[5]))

        elif self.options.starting_units.value == StartingUnits.option_random_monster:
            randomize_starting(all_with_monster)

        if self.options.randomize_enemies.value == 1:
            for index in range(6, 0xA46):
                self.randomized_jobs.append(get_random_job(self.random, all_with_monster))
                self.randomized_weapons.append(get_valid_weapon(self.randomized_jobs[index]))
                self.randomized_equip.append(get_valid_equip(self.randomized_jobs[index]))

        # Always randomize the judge encounters for now
        for index in range(0, 5):
            self.randomized_judge.append(get_random_job(self.random, all))
            self.judge_weapon.append(get_valid_weapon(self.randomized_judge[index]))
            self.judge_equip.append(get_valid_equip(self.randomized_judge[index]))

        # print(self.random_data.all_abilities)
        # self.random.shuffle(self.random_data.all_abilities)

        self.location_ids = [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x09, 0x0a, 0x0b, 0x0c,
                0x0d, 0x0e, 0x0f, 0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18,
                0x19, 0x1a, 0x1b, 0x1c, 0x1d]

        # Randomize location nodes on map
        self.random.shuffle(self.location_ids)

        # Add Ambervale to the end
        self.location_ids.append(0x08)

        #Visualize regions
        #visualize_regions(self.multiworld.get_region("Menu", self.player), "ffta.puml", show_entrance_names=True)

        generate_output(self, self.player, output_directory)






