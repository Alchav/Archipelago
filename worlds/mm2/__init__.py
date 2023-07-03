from BaseClasses import Tutorial, ItemClassification, MultiWorld
from worlds.AutoWorld import World, WebWorld
from worlds.generic.Rules import set_rule, add_rule
import Names
from .Items import item_table, item_names, MM2Item, filler_item_table, filler_item_weights, robot_master_weapon_table, \
    stage_access_table, item_item_table
from .Locations import location_table, MM2Location
from .Rom import get_base_rom_bytes, get_base_rom_path, RomData
from typing import Dict
import os
import math
import threading
import base64


class MM2WebWorld(WebWorld):
    theme = "partyTime"
    tutorials = [

        # Tutorial(
        #    "Multiworld Setup Guide",
        #    "A guide to setting up the Mega Man 2 randomizer connected to an Archipelago Multiworld.",
        #    "English",
        #    "setup_en.md",
        #    "setup/en",
        #    ["Silvris"]
        # )
    ]


class MM2World(World):
    """
    In the year 200X, following his prior defeat by Mega Man, Dr. Wily has returned to take over the world with his own
    group of Robot Masters. Mega Man once again sets out to defeat the eight Robot Masters and stop Dr. Wily.

    """

    game: str = "Mega Man 2"
    #option_definitions = mm2_options
    item_name_to_id = {item: item_table[item].code for item in item_table}
    location_name_to_id = location_table
    item_name_groups = item_names
    data_version = 0
    web = MM2WebWorld()
    boss_requirements = dict()

    def __init__(self, world: MultiWorld, player: int):
        self.rom_name_available_event = threading.Event()
        super().__init__(world, player)

    @classmethod
    def stage_assert_generate(cls, multiworld: MultiWorld) -> None:
        rom_file: str = get_base_rom_path()
        if not os.path.exists(rom_file):
            raise FileNotFoundError(f"Could not find base ROM for {cls.game}: {rom_file}")

    create_regions = create_levels

    def create_item(self, name: str, force_non_progression=False) -> MM2Item:
        item = item_table[name]
        classification = ItemClassification.filler
        if item.progression and not force_non_progression:
            classification = ItemClassification.progression_skip_balancing \
                if item.skip_balancing else ItemClassification.progression
        return MM2Item(name, classification, item.code, self.player)

    def get_filler_item_name(self) -> str:
        return self.multiworld.random.choices(list(filler_item_weights.keys()),
                                              weights=list(filler_item_weights.values()))[0]

    def create_items(self) -> None:
        itempool = []
        itempool.extend([name for name in robot_master_weapon_table.keys()])
        itempool.extend([name for name in stage_access_table.keys()])
        itempool.extend([name for name in item_item_table.keys()])

        self.multiworld.itempool += itempool

    def set_rules(self) -> None:
        print("NotImplemented")

    def generate_basic(self) -> None:
        goal_location = self.multiworld.get_location(Names.dr_wily, self.player)
        goal_location.place_locked_item(MM2Item("Victory", ItemClassification.progression, None, self.player))
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

    def generate_output(self, output_directory: str):
        rompath = ""
        try:
            world = self.multiworld
            player = self.player

            rom = RomData(get_base_rom_path())
            patch_rom(self.multiworld, self.player, rom, self.required_heart_stars[self.player],
                      self.boss_requirements[self.player],
                      self.player_levels[self.player])

            rompath = os.path.join(output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}.sfc")
            rom.write_to_file(rompath)
            self.rom_name = rom.name

            patch = KDL3DeltaPatch(os.path.splitext(rompath)[0] + KDL3DeltaPatch.patch_file_ending, player=player,
                                   player_name=world.player_name[player], patched_path=rompath)
            patch.write()
        except Exception:
            raise
        finally:
            self.rom_name_available_event.set()  # make sure threading continues and errors are collected
            if os.path.exists(rompath):
                os.unlink(rompath)

    def modify_multidata(self, multidata: dict):
        # wait for self.rom_name to be available.
        self.rom_name_available_event.wait()
        rom_name = getattr(self, "rom_name", None)
        # we skip in case of error, so that the original error in the output thread is the one that gets raised
        if rom_name:
            new_name = base64.b64encode(bytes(self.rom_name)).decode()
            multidata["connect_names"][new_name] = multidata["connect_names"][self.multiworld.player_name[self.player]]