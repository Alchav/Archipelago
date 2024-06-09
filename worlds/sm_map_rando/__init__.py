from __future__ import annotations

import logging
import copy
import os
import platform
import shutil
import sys
import tempfile
import threading
import base64
import itertools
import json
from typing import Any, Dict, Iterable, List, Optional, Set, TextIO, TypedDict

from BaseClasses import LocationProgressType, Region, Entrance, Location, MultiWorld, Item, ItemClassification, CollectionState, Tutorial
from Fill import fill_restrictive
from Utils import snes_to_pc
from worlds.AutoWorld import World, AutoLogicRegister, WebWorld
from worlds.generic.Rules import set_rule, add_rule, add_item_rule

logger = logging.getLogger("Super Metroid Map Rando")

from .Rom import get_base_rom_path, get_sm_symbols, openFile, SMMR_ROM_MAX_PLAYERID, SMMR_ROM_PLAYERDATA_COUNT, SMMapRandoDeltaPatch 
from .ips import IPS_Patch
from .Client import SMMRSNIClient
from importlib.metadata import version, PackageNotFoundError

required_pysmmaprando_version = "0.111.2"

class WrongVersionError(Exception):
    pass

try:
    if version("pysmmaprando") != required_pysmmaprando_version:
        raise WrongVersionError
    from pysmmaprando import create_gamedata, APRandomizer, APCollectionState, patch_rom, Item as Pysmmr_items, Options as Pysmmr_options
    from pysmmaprando import ControllerButton, ControllerConfig, CustomizeSettings, MusicSettings, PaletteTheme, ShakingSetting, TileTheme

# required for APWorld distribution outside official AP releases as stated at https://docs.python.org/3/library/zipimport.html:
# ZIP import of dynamic modules (.pyd, .so) is disallowed.
except (ImportError, WrongVersionError, PackageNotFoundError) as e:
    python_version = f"cp{sys.version_info.major}{sys.version_info.minor}"
    if sys.platform.startswith('win'):
        abi_version = "none-win_amd64"
    elif sys.platform.startswith('linux'):
        abi_version = f"{python_version}-manylinux_2_17_{platform.machine()}.manylinux2014_{platform.machine()}"
    elif sys.platform.startswith('darwin'):
        mac_ver = platform.mac_ver()[0].split('.')
        if (int(mac_ver[0]) * 10 + int(mac_ver[1]) <= 107):
            abi_version = f"{python_version}-macosx_10_7_{platform.machine()}"
        else:
            abi_version = f"{python_version}-macosx_10_9_x86_64.macosx_11_0_arm64.macosx_10_9_universal2"
    map_rando_lib_file = f'https://github.com/lordlou/MapRandomizer/releases/download/v{required_pysmmaprando_version}/pysmmaprando-{required_pysmmaprando_version}-{python_version}-{abi_version}.whl'
    import Utils
    if not Utils.is_frozen():
        import subprocess
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', map_rando_lib_file])
    else:
        import requests
        import zipfile
        import io
        import glob
        import shutil
        dirs_to_delete = glob.glob(f"{os.path.dirname(sys.executable)}/lib/pysmmaprando-*.dist-info")
        for dir in dirs_to_delete:
            shutil. rmtree(dir)
        with requests.get(map_rando_lib_file) as r:
            r.raise_for_status()
            z = zipfile.ZipFile(io.BytesIO(r.content))
            z.extractall(f"{os.path.dirname(sys.executable)}/lib")
            
    from pysmmaprando import create_gamedata, APRandomizer, APCollectionState, patch_rom, Item as Pysmmr_items, Options as Pysmmr_options
    from pysmmaprando import ControllerButton, ControllerConfig, CustomizeSettings, MusicSettings, PaletteTheme, ShakingSetting, TileTheme

def GetAPWorldPath():
    filename = sys.modules[__name__].__file__
    apworldExt = ".apworld"
    game = "sm_map_rando/"
    if apworldExt in filename:
        return filename[:filename.index(apworldExt) + len(apworldExt)]
    else:
        return None

map_rando_game_data = create_gamedata(GetAPWorldPath())

from .Options import SMMROptions

class ByteEdit(TypedDict):
    sym: Dict[str, Any]
    offset: int
    values: Iterable[int]

class SMMRCollectionState(metaclass=AutoLogicRegister):
    def init_mixin(self, parent: MultiWorld):
        
        # for unit tests where MultiWorld is instantiated before worlds
        if hasattr(parent, "state"):
            self.smmrcs = {player: parent.state.smmrcs[player].copy() for player in parent.get_game_players(SMMapRandoWorld.game)}
            for player, group in parent.groups.items():
                if (group["game"] == SMMapRandoWorld.game):
                    self.smmrcs[player] = APCollectionState(None)
                    if player not in parent.state.smmrcs:
                        parent.state.smmrcs[player] = APCollectionState(None)
        else:
            self.smmrcs = {}

    def copy_mixin(self, ret) -> CollectionState:
        ret.smmrcs = {player: self.smmrcs[player].copy() for player in self.smmrcs}
        return ret

class SMMapRandoWeb(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Super Metroid Map Rando Client on your computer. This guide covers single-player, multiworld, and related software.",
        "English",
        "multiworld_en.md",
        "multiworld/en",
        ["Farrak Kilhn"]
    )]


locations_start_id = 86000
items_start_id = 87000

locations_count = 100
locations_flag_start = 256

location_address_to_id = {}
with openFile("/".join((os.path.dirname(__file__), "data", "loc_address_to_id.json")), "r") as stream:
    location_address_to_id = json.load(stream)

class SMMapRandoWorld(World):
    """
    After planet Zebes exploded, Mother Brain put it back together again but arranged it differently this time.

    Can you find the items needed to defeat Mother Brain and restore peace to the galaxy?
    """

    game: str = "Super Metroid Map Rando"
    topology_present = True
    data_version = 0
    options_dataclass = SMMROptions
    options: SMMROptions

    gamedata = map_rando_game_data

    item_name_to_id = {item_name: items_start_id + idx for idx, item_name in enumerate(itertools.chain(gamedata.item_isv, gamedata.flag_isv))}
    location_name_to_id = {loc_name: locations_start_id + 
                           (location_address_to_id[str(addr)] if idx < locations_count else locations_flag_start + idx - locations_count) 
                           for idx, (loc_name, addr) in 
                                enumerate(itertools.chain(
                                    zip(gamedata.get_location_names(), gamedata.get_location_addresses()), 
                                    zip(gamedata.flag_isv, [None] * len(gamedata.flag_isv))))}
    
    flag_location_names = {name: i for i, name in enumerate(gamedata.get_flag_location_names())}

    locations_idx_range_to_area = {
        12 : "Crateria",
        48 : "Brinstar",
        80 : "Norfair",
        135 : "Wrecked Ship",
        154 : "Maridia"
    }

    nothing_item_id = 22

    web = SMMapRandoWeb()

    required_client_version = (0, 4, 4)

    def __init__(self, world: MultiWorld, player: int):
        super().__init__(world, player)
        self.rom_name_available_event = threading.Event()
        self.locations = {}

    @classmethod
    def stage_assert_generate(cls, multiworld: MultiWorld):
        rom_file = get_base_rom_path()
        if not os.path.exists(rom_file):
            raise FileNotFoundError(rom_file)

    """  
    @classmethod
    def stage_fill_hook(cls, world, progitempool, usefulitempool, filleritempool, fill_locations):
        if world.get_game_players(cls.game):
            progitempool.sort(
                key=lambda item: 1 if (item.name == 'Morph' or item.name == 'Varia' or item.name == 'Gravity') else 0)
    """

    def generate_early(self):
        item_pool = self.options.custom_item_pool.default
        if self.options.item_pool.value == self.options.item_pool.option_Reduced:
            item_pool = self.options.custom_item_pool.reduced
        elif self.options.item_pool.value == self.options.item_pool.option_Custom:
            item_pool = self.options.custom_item_pool.value

        item_mapping = {
            "ETank": Pysmmr_items.ETank,
            "Missile": Pysmmr_items.Missile,
            "Super": Pysmmr_items.Super,
            "PowerBomb": Pysmmr_items.PowerBomb,
            "ReserveTank": Pysmmr_items.ReserveTank
                        }
        pysmmr_item_pool = [(item_mapping[key], value) for key, value in item_pool.items()]

        options = Pysmmr_options(self.options.preset.value,
                          list(self.options.techs.value),
                          list(self.options.strats.value),
                          pysmmr_item_pool,
                          self.options.shinespark_tiles.value,
                          self.options.heated_shinespark_tiles.value,
                          self.options.shinecharge_leniency_frames.value,
                          self.options.resource_multiplier.value / 100,
                          self.options.gate_glitch_leniency.value,
                          self.options.door_stuck_leniency.value,
                          self.options.phantoon_proficiency.value / 100,
                          self.options.draygon_proficiency.value / 100,
                          self.options.ridley_proficiency.value / 100,
                          self.options.botwoon_proficiency.value / 100,
                          self.options.mother_brain_proficiency.value / 100,
                          self.options.escape_timer_multiplier.value / 100,
                          self.options.start_location_mode.value,
                          self.options.save_animals.value,
                          self.options.early_save.value == 1,
                          self.options.objectives.value,
                          self.options.doors_mode.value,
                          self.options.area_assignment.value == 1,
                          "", #filler_items
                          self.options.supers_double.value == 1,
                          self.options.mother_brain.value,
                          self.options.escape_enemies_cleared.value == 1,
                          self.options.escape_refill.value == 1,
                          self.options.escape_movement_items.value == 1,
                          self.options.mark_map_stations.value == 1,
                          self.options.room_outline_revealed.value == 1,
                          self.options.transition_letters.value == 1,
                          self.options.item_markers.value,
                          self.options.item_dots_disappear.value == 1,
                          self.options.all_items_spawn.value == 1,
                          self.options.buffed_drops.value == 1,
                          self.options.acid_chozo.value == 1,
                          self.options.fast_elevators.value == 1,
                          self.options.fast_doors.value == 1,
                          self.options.fast_pause_menu.value == 1,
                          self.options.respin.value == 1,
                          self.options.infinite_space_jump.value == 1,
                          self.options.momentum_conservation.value == 1,
                          self.options.wall_jump.value,
                          self.options.etank_refill.value,
                          self.options.maps_revealed.value,
                          self.options.map_layout.value,
                          self.options.energy_free_shinesparks.value == 1,
                          self.options.ultra_low_qol.value == 1,
                          "", #skill_assumptions_preset
                          "", #item_progression_preset
                          self.options.quality_of_life.value,
                          )
        for tries in range(5):
            try:
                self.map_rando = APRandomizer(SMMapRandoWorld.gamedata, options, self.multiworld.random.randint(1, sys.maxsize)) # self.multiworld.seed // 10)
                break
            except:
                continue

        self.update_reachability = 0
        self.debug = False

        self.multiworld.state.smmrcs[self.player] = APCollectionState(self.multiworld.worlds[self.player].map_rando)
        #self.multiworld.local_early_items[self.player]['Morph'] = 1
        #self.multiworld.local_early_items[self.player]['Varia'] = 1
        #self.multiworld.local_early_items[self.player]['Gravity'] = 1

    def create_region(self, world: MultiWorld, player: int, name: str, index: int, locations=None, exits=None):
        ret = SMMRRegion(name, player, world, index)
        if locations:
            for loc in locations:
                location = self.locations[loc]
                location.parent_region = ret
                ret.locations.append(location)
        if exits:
            for exit in exits:
                ret.exits.append(Entrance(player, exit, ret))
        return ret

    def create_regions(self):
        def add_entrance_rule(srcDestEntrance, player, link_from):
            add_rule(srcDestEntrance, lambda state: state.smmrcs[player].can_traverse(link_from, srcDestEntrance.strats_links))

        # create locations
        for loc_name, id in SMMapRandoWorld.location_name_to_id.items():
            is_not_flag = id < locations_start_id + locations_flag_start
            if is_not_flag or loc_name in SMMapRandoWorld.flag_location_names.keys():
                self.locations[loc_name] = SMMRLocation(self.player, loc_name, id if is_not_flag else None)


        # self.locations["Missile (green Maridia shinespark)"].progress_type = LocationProgressType.EXCLUDED

        # create regions
        regions = []
        #self.region_dict = []
        for i, (vertex_name, location_name) in enumerate(self.map_rando.randomizer.game_data.get_vertex_names()):
            regions.append(self.create_region(  self.multiworld, 
                                                self.player, 
                                                vertex_name,
                                                i,
                                                [location_name] if location_name != None else None))

        self.vertex_cnt = len(regions)    
        for i, flag_name in enumerate(SMMapRandoWorld.flag_location_names.keys()):
            regions.append(self.create_region(  self.multiworld, 
                                                self.player, 
                                                flag_name,
                                                self.vertex_cnt + i,
                                                [flag_name]))

        #for region in regions:
        #    self.region_dict[region.index] = region
        self.region_dict = regions

        self.multiworld.regions += regions

        self.events_connections = self.map_rando.randomizer.game_data.get_event_vertex_ids()
        (self.region_map, self.region_map_reverse) = self.map_rando.randomizer.game_data.get_regions_map()
        self.flag_id_to_region_dict = [SMMapRandoWorld.flag_location_names.get(flag, None) for flag in self.map_rando.randomizer.game_data.flag_isv]

        #create entrances
        """
        links_infos = self.map_rando.get_links_infos()
        for (link_from, link_to), link_map in links_infos.items():
            src_region = regions[link_from]
            dest_region = regions[link_to]
            link_map_debug = {}
            for name, links in link_map.items():
                link_map_debug[name] = [self.map_rando.get_link_requirement(link) for link in links]
            srcDestEntrance = SMMREntrance(self.player, src_region.name + "->" + dest_region.name, src_region, link_map, link_map_debug)
            src_region.exits.append(srcDestEntrance)
            srcDestEntrance.connect(dest_region)
            # add_entrance_rule(srcDestEntrance, self.player, link_from)

        for vertex_id, flag_ids in self.events_connections.items():
            for flag_id in flag_ids:
                src_region = regions[self.region_map[vertex_id]]
                dest_region = regions[self.vertex_cnt + SMMapRandoWorld.flag_location_names[self.map_rando.randomizer.game_data.flag_isv[flag_id]]]
                srcDestEntrance = SMMREntrance(self.player, src_region.name + "->" + dest_region.name, src_region)
                src_region.exits.append(srcDestEntrance)
                srcDestEntrance.connect(dest_region)  
        """
        self.multiworld.regions += [self.create_region(self.multiworld, self.player, 'Menu', -1, None, ['StartAP'])]

        #victory_entrance = self.multiworld.get_entrance("Ship->Escape Zebes", self.player)
        #add_rule(victory_entrance, lambda state: state.has('f_ZebesSetAblaze', self.player))

        startAP = self.multiworld.get_entrance('StartAP', self.player)
        startAP.connect(self.multiworld.get_region("Landing Site Ship", self.player))   

    def create_items(self):
        self.startItems = [variaItem for item in self.multiworld.precollected_items[self.player] for variaItem in self.item_name_to_id.keys() if variaItem == item.name]
        pool = []
        for idx, type_count in enumerate(self.map_rando.randomizer.initial_items_remaining):
            for item_count in range(type_count):
                minor_count = [
                    14,# etanks       // 0
                    2, # missiles     // 1
                    2, # supers       // 2
                    1, # powerbomb    // 3
                    1, # Bombs        // 4
                    1, # Charge       // 5
                    1, # Ice          // 6
                    1, # HiJump       // 7
                    1, # SpeedBooster // 8
                    1, # Wave         // 9
                    1, # Spazer       // 10
                    1, # SpringBall   // 11
                    1, # Varia        // 12
                    1, # Gravity      // 13
                    1, # XRayScope    // 14
                    1, # Plasma       // 15
                    1, # Grapple      // 16
                    1, # SpaceJump    // 17
                    1, # ScrewAttack  // 18
                    1, # Morph        // 19
                    4, # ReserveTank  // 20
                    1, # WallJump     // 21
                    0  # Nothing      // 22
                ]
                is_progression = item_count < minor_count[idx]
                mr_item = SMMRItem(SMMapRandoWorld.item_id_to_name[items_start_id + idx], 
                            ItemClassification.progression if is_progression else ItemClassification.filler, 
                            items_start_id + idx, 
                            player=self.player)
                pool.append(mr_item)
        self.multiworld.itempool += pool

        gamedata = self.map_rando.randomizer.game_data
        for flag_name, i in SMMapRandoWorld.flag_location_names.items():
            item = SMMRItem(flag_name, 
                            ItemClassification.progression, 
                            None,
                            player=self.player)
            self.multiworld.get_location(flag_name, self.player).place_locked_item(item)
            self.multiworld.get_location(flag_name, self.player).address = None 
        
    def set_rules(self):
        chozo_regions = [   
                            self.multiworld.get_region("Bowling Alley Bowling Chozo Statue (unlocked)", self.player), 
                            self.multiworld.get_region("Bomb Torizo Room Bomb Torizo (unlocked)", self.player)
                        ]
        pirates_regions = [ 
                            self.multiworld.get_region("Pit Room Left Door (unlocked)", self.player),
                            self.multiworld.get_region("Baby Kraid Room Left Door (unlocked)", self.player),
                            self.multiworld.get_region("Plasma Room Top Left Door (unlocked)", self.player),
                            self.multiworld.get_region("Metal Pirates Room Left Door (unlocked)", self.player)
                          ]
        goals = [
                    lambda state: state.can_reach(self.multiworld.get_region("Mother Brain Room Right Door", self.player)),
                    lambda state: state.has_all(["f_DefeatedKraid", "f_DefeatedPhantoon", "f_DefeatedDraygon", "f_DefeatedRidley"], self.player),
                    lambda state: state.has_all(["f_DefeatedBotwoon", "f_DefeatedCrocomire", "f_DefeatedSporeSpawn", "f_DefeatedGoldenTorizo"], self.player),
                    lambda state: state.has_all(["f_KilledMetroidRoom1", "f_KilledMetroidRoom2", "f_KilledMetroidRoom3", "f_KilledMetroidRoom4"], self.player),
                    lambda state: state.has_all(["f_UsedAcidChozoStatue", "f_DefeatedGoldenTorizo", "Morph", "f_DefeatedPhantoon"], self.player) \
                        and all(state.can_reach(region) for region in chozo_regions),
                    lambda state: state.has_all(["Morph", "Missile"], self.player) and all(state.can_reach(region) for region in pirates_regions)
                ]
        
        self.multiworld.completion_condition[self.player] = goals[self.options.objectives.value]

    def post_fill(self):
        spheres: List[Location] = getattr(self.multiworld, "_smmr_spheres", None)
        if spheres is None:
            spheres = list(self.multiworld.get_spheres())
            setattr(self.multiworld, "_smmr_spheres", spheres)

    def collect(self, state: CollectionState, item: Item) -> bool:
        if (item.code != None): # - items_start_id < len(self.gamedata.item_isv)):
            state.smmrcs[self.player].add_item(item.code - items_start_id, self.gamedata)
        else:
            state.smmrcs[self.player].add_flag(SMMapRandoWorld.item_name_to_id[item.name] - items_start_id - len(self.gamedata.item_isv))
        return super(SMMapRandoWorld, self).collect(state, item)

    def remove(self, state: CollectionState, item: Item) -> bool:
        if (item.code - items_start_id < len(self.gamedata.item_isv)):
            state.smmrcs[self.player].remove_item(item.code - items_start_id, self.gamedata)
        else:
            state.smmrcs[self.player].remove_flag(item.code - items_start_id - len(self.gamedata.item_isv))
        return super(SMMapRandoWorld, self).remove(state, item)
    
    def create_item(self, name: str) -> Item:
        return SMMRItem(name, ItemClassification.progression, self.item_name_to_id[name], player=self.player)

    def get_filler_item_name(self) -> str:
        return "Missile"

    def getWordArray(self, w: int) -> List[int]:
        """ little-endian convert a 16-bit number to an array of numbers <= 255 each """
        return [w & 0x00FF, (w & 0xFF00) >> 8]

    def convertToROMItemName(self, itemName):
        charMap = { "A" : 0x2CC0, 
                    "B" : 0x2CC1,
                    "C" : 0x2CC2,
                    "D" : 0x2CC3,
                    "E" : 0x2CC4,
                    "F" : 0x2CC5,
                    "G" : 0x2CC6,
                    "H" : 0x2CC7,
                    "I" : 0x2CC8,
                    "J" : 0x2CC9,
                    "K" : 0x2CCA,
                    "L" : 0x2CCB,
                    "M" : 0x2CCC,
                    "N" : 0x2CCD,
                    "O" : 0x2CCE,
                    "P" : 0x2CCF,
                    "Q" : 0x2CD0,
                    "R" : 0x2CD1,
                    "S" : 0x2CD2,
                    "T" : 0x2CD3,
                    "U" : 0x2CD4,
                    "V" : 0x2CD5,
                    "W" : 0x2CD6,
                    "X" : 0x2CD7,
                    "Y" : 0x2CD8,
                    "Z" : 0x2CD9,
                    " " : 0x2C0F,
                    "!" : 0x2CDF,
                    "?" : 0x2CDE,
                    "'" : 0x2CDD,
                    "," : 0x2CDA,
                    "." : 0x2CDA,
                    "-" : 0x2CDD,
                    "_" : 0x000F,
                    "1" : 0x2C01,
                    "2" : 0x2C02,
                    "3" : 0x2C03,
                    "4" : 0x2C04,
                    "5" : 0x2C05,
                    "6" : 0x2C06,
                    "7" : 0x2C07,
                    "8" : 0x2C08,
                    "9" : 0x2C09,
                    "0" : 0x2C00,
                    "%" : 0x2C0A}
        data = []

        itemName = itemName.upper()[:26]
        itemName = itemName.strip()
        itemName = itemName.center(26, " ")    
        itemName = "___" + itemName + "___"

        for char in itemName:
            [w0, w1] = self.getWordArray(charMap.get(char, 0x2CDE))
            data.append(w0)
            data.append(w1)
        return data
        
    def generate_output(self, output_directory: str):
        def get_area_name(loc_idx: int):
            for idx, area_name in SMMapRandoWorld.locations_idx_range_to_area.items():
                if loc_idx <= idx:
                    return area_name
            return ""

        sorted_item_locs = list(self.locations.values())
        items = [(itemLoc.item.code if isinstance(itemLoc.item, SMMRItem) else (self.item_name_to_id['ArchipelagoProgItem'] if itemLoc.item.classification == ItemClassification.progression else self.item_name_to_id['ArchipelagoItem'])) - items_start_id for itemLoc in sorted_item_locs if itemLoc.address is not None]
        spheres: List[Location] = getattr(self.multiworld, "_smmr_spheres", None)
        summary =   [   (
                            sphere_idx, 
                            loc.item.name, 
                            get_area_name(SMMapRandoWorld.location_name_to_id[loc.name] - locations_start_id) if loc.player == self.player else 
                            self.multiworld.get_player_name(loc.player) + " world" #+ itemloc.loc.name
                        ) 
                    for sphere_idx, sphere in enumerate(spheres) for loc in sphere if loc.item.player == self.player and not loc.item.name.startswith("f_") and loc.item.name != "Nothing"
                    ]
        
        controller_mapping_string = {
                                        "X": ControllerButton.X, 
                                        "Y": ControllerButton.Y,  
                                        "A": ControllerButton.A,  
                                        "B": ControllerButton.B, 
                                        "L": ControllerButton.L,  
                                        "R": ControllerButton.R, 
                                        "Select": ControllerButton.Select, 
                                        "Start": ControllerButton.Start, 
                                        "Up": ControllerButton.Up, 
                                        "Down": ControllerButton.Down, 
                                        "Left": ControllerButton.Left, 
                                        "Right": ControllerButton.Right,
                                     }
        controller_mapping_int = {
                                    int(ControllerButton.X): ControllerButton.X, 
                                    int(ControllerButton.Y): ControllerButton.Y,  
                                    int(ControllerButton.A): ControllerButton.A,  
                                    int(ControllerButton.B): ControllerButton.B, 
                                    int(ControllerButton.L): ControllerButton.L,  
                                    int(ControllerButton.R): ControllerButton.R, 
                                    int(ControllerButton.Select): ControllerButton.Select, 
                                    int(ControllerButton.Start): ControllerButton.Start, 
                                    int(ControllerButton.Up): ControllerButton.Up, 
                                    int(ControllerButton.Down): ControllerButton.Down, 
                                    int(ControllerButton.Left): ControllerButton.Left, 
                                    int(ControllerButton.Right): ControllerButton.Right, 
                                }
        music_settings_mapping = {
                                    0: MusicSettings.Vanilla,
                                    1: MusicSettings.AreaThemed,
                                    2: MusicSettings.Disabled
                                  }
        tile_theme_mapping = { 
                                0: TileTheme.Vanilla,
                                1: TileTheme.Scrambled,
                                2: TileTheme.OuterCrateria,
                                3: TileTheme.InnerCrateria,
                                4: TileTheme.GreenBrinstar,
                                5: TileTheme.UpperNorfair,
                                6: TileTheme.WreckedShip,
                                7: TileTheme.WestMaridia,
                            }
        shaking_settings_mapping = {
                                    0: ShakingSetting.Vanilla,
                                    1: ShakingSetting.Reduced,
                                    2: ShakingSetting.Disabled
                                  }

        controller_config = ControllerConfig(
                controller_mapping_int[self.options.shot.value],
                controller_mapping_int[self.options.jump.value],
                controller_mapping_int[self.options.dash.value],
                controller_mapping_int[self.options.item_select.value],
                controller_mapping_int[self.options.item_cancel.value],
                controller_mapping_int[self.options.angle_up.value],
                controller_mapping_int[self.options.angle_down.value],
                [controller_mapping_string[button] for button in self.options.spin_lock_buttons.value],
                [controller_mapping_string[button] for button in self.options.quick_reload_buttons.value],
                self.options.moonwalk.value == 1)
        customize_settings = CustomizeSettings(
                None,
                (self.options.etank_color_red.value // 8, self.options.etank_color_green.value // 8, self.options.etank_color_blue.value // 8),
                self.options.reserve_hud_style.value == 1,
                self.options.vanilla_screw_attack_animation.value == 1,
                PaletteTheme.Vanilla if self.options.palette_theme.value == 0 else PaletteTheme.AreaThemed,
                tile_theme_mapping[self.options.tile_theme.value],
                music_settings_mapping[self.options.music.value],
                self.options.disable_beeping.value == 1,
                shaking_settings_mapping[self.options.shaking.value],
                controller_config)
        patched_rom_bytes = patch_rom(get_base_rom_path(), self.map_rando, items, self.multiworld.state.smmrcs[self.player].randomization_state, summary, customize_settings)
        #patched_rom_bytes = None
        #with open(get_base_rom_path(), "rb") as stream:
        #    patched_rom_bytes = stream.read()

        patches = []
        patches.append(IPS_Patch.load("/".join((os.path.dirname(self.__file__),
                                              "data", "SMBasepatch_prebuilt", "multiworld-basepatch.ips"))))
        symbols = get_sm_symbols("/".join((os.path.dirname(self.__file__),
                                              "data", "SMBasepatch_prebuilt", "sm-basepatch-symbols.json")))

        # gather all player ids and names relevant to this rom, then write player name and player id data tables
        playerIdSet: Set[int] = {0}  # 0 is for "Archipelago" server
        for itemLoc in self.multiworld.get_locations():
            assert itemLoc.item, f"World of player '{self.multiworld.player_name[itemLoc.player]}' has a loc.item " + \
                                 f"that is {itemLoc.item} during generate_output"
            # add each playerid who has a location containing an item to send to us *or* to an item_link we're part of
            if itemLoc.item.player == self.player or \
                    (itemLoc.item.player in self.multiworld.groups and
                     self.player in self.multiworld.groups[itemLoc.item.player]['players']):
                playerIdSet |= {itemLoc.player}
            # add each playerid, including item link ids, that we'll be sending items to
            if itemLoc.player == self.player:
                playerIdSet |= {itemLoc.item.player}
        if len(playerIdSet) > SMMR_ROM_PLAYERDATA_COUNT:
            # max 202 entries, but it's possible for item links to add enough replacement items for us, that are placed
            # in worlds that otherwise have no relation to us, that the 2*location count limit is exceeded
            logger.warning("SMMR is interacting with too many players to fit in ROM. "
                           f"Removing the highest {len(playerIdSet) - SMMR_ROM_PLAYERDATA_COUNT} ids to fit")
            playerIdSet = set(sorted(playerIdSet)[:SMMR_ROM_PLAYERDATA_COUNT])
        otherPlayerIndex: Dict[int, int] = {}  # ap player id -> rom-local player index
        playerNameData: List[ByteEdit] = []
        playerIdData: List[ByteEdit] = []
        # sort all player data by player id so that the game can look up a player's data reasonably quickly when
        # the client sends an ap playerid to the game
        for i, playerid in enumerate(sorted(playerIdSet)):
            playername = self.multiworld.player_name[playerid] if playerid != 0 else "Archipelago"
            playerIdForRom = playerid
            if playerid > SMMR_ROM_MAX_PLAYERID:
                # note, playerIdForRom = 0 is not unique so the game cannot look it up.
                # instead it will display the player received-from as "Archipelago"
                playerIdForRom = 0
                if playerid == self.player:
                    raise Exception(f"SM rom cannot fit enough bits to represent self player id {playerid}")
                else:
                    logger.warning(f"SM rom cannot fit enough bits to represent player id {playerid}, setting to 0 in rom")
            otherPlayerIndex[playerid] = i
            playerNameData.append({"sym": symbols["rando_player_name_table"],
                                   "offset": i * 16,
                                   "values": playername[:16].upper().center(16).encode()})
            playerIdData.append({"sym": symbols["rando_player_id_table"],
                                 "offset": i * 2,
                                 "values": self.getWordArray(playerIdForRom)})

        multiWorldLocations: List[ByteEdit] = []
        multiWorldItems: List[ByteEdit] = []
        idx = 0
        vanillaItemTypesCount = 23
        locations_nothing = bytearray(20)
        for itemLoc in self.multiworld.get_locations():
            if itemLoc.player == self.player and not itemLoc.name.startswith("f_"):
                # item to place in this SMMR world: write full item data to tables
                if isinstance(itemLoc.item, SMMRItem) and itemLoc.item.code < items_start_id + vanillaItemTypesCount:
                    if itemLoc.item.code == items_start_id + self.nothing_item_id:
                        locations_nothing[(itemLoc.address - locations_start_id)//8] |= 1 << (itemLoc.address % 8)
                    itemId = itemLoc.item.code - items_start_id
                else:
                    itemId = self.item_name_to_id['ArchipelagoItem'] - items_start_id + idx
                    multiWorldItems.append({"sym": symbols["message_item_names"],
                                            "offset": (vanillaItemTypesCount + idx)*64,
                                            "values": self.convertToROMItemName(itemLoc.item.name)})
                    idx += 1

                if itemLoc.item.player == self.player:
                    itemDestinationType = 0  # dest type 0 means 'regular old SM item' per itemtable.asm
                elif itemLoc.item.player in self.multiworld.groups and \
                        self.player in self.multiworld.groups[itemLoc.item.player]['players']:
                    # dest type 2 means 'SM item link item that sends to the current player and others'
                    # per itemtable.asm (groups are synonymous with item_links, currently)
                    itemDestinationType = 2
                else:
                    itemDestinationType = 1  # dest type 1 means 'item for entirely someone else' per itemtable.asm

                [w0, w1] = self.getWordArray(itemDestinationType)
                [w2, w3] = self.getWordArray(itemId)
                [w4, w5] = self.getWordArray(otherPlayerIndex[itemLoc.item.player] if itemLoc.item.player in
                                             otherPlayerIndex else 0)
                [w6, w7] = self.getWordArray(0 if itemLoc.item.advancement else 1)
                multiWorldLocations.append({"sym": symbols["rando_item_table"],
                                            "offset": (itemLoc.address - locations_start_id)*8,
                                            "values": [w0, w1, w2, w3, w4, w5, w6, w7]})

        itemSprites = [{"fileName":          "off_world_prog_item.bin",
                        "paletteSymbolName": "prog_item_eight_palette_indices",
                        "dataSymbolName":    "offworld_graphics_data_progression_item"},

                       {"fileName":          "off_world_item.bin",
                        "paletteSymbolName": "nonprog_item_eight_palette_indices",
                        "dataSymbolName":    "offworld_graphics_data_item"}]
        idx = 0
        offworldSprites: List[ByteEdit] = []
        for itemSprite in itemSprites:
            with openFile("/".join((os.path.dirname(self.__file__), "data", "custom_sprite", itemSprite["fileName"])), 'rb') as stream:
                buffer = bytearray(stream.read())
                offworldSprites.append({"sym": symbols[itemSprite["paletteSymbolName"]],
                                        "offset": 0,
                                        "values": buffer[0:8]})
                offworldSprites.append({"sym": symbols[itemSprite["dataSymbolName"]],
                                        "offset": 0,
                                        "values": buffer[8:264]})
                idx += 1

        deathLink: List[ByteEdit] = [{
            "sym": symbols["config_deathlink"],
            "offset": 0,
            "values": [self.options.death_link.value]
        }]
        remoteItem: List[ByteEdit] = [{
            "sym": symbols["config_remote_items"],
            "offset": 0,
            "values": self.getWordArray(0b001 + (0b010 if self.options.remote_items else 0b000))
        }]
        ownPlayerId: List[ByteEdit] = [{
            "sym": symbols["config_player_id"],
            "offset": 0,
            "values": self.getWordArray(self.player)
        }]

        location_nothing: List[ByteEdit] = [{
            "sym": symbols["locations_nothing"],
            "offset": 0,
            "values": locations_nothing
        }]

        patchDict = {   'MultiWorldLocations': multiWorldLocations,
                        'MultiWorldItems': multiWorldItems,
                        'offworldSprites': offworldSprites,
                        'deathLink': deathLink,
                        'remoteItem': remoteItem,
                        'ownPlayerId': ownPlayerId,
                        'playerNameData':  playerNameData,
                        'playerIdData':  playerIdData,
                        'location_nothing': location_nothing}

        # convert an array of symbolic byte_edit dicts like {"sym": symobj, "offset": 0, "values": [1, 0]}
        # to a single rom patch dict like {0x438c: [1, 0], 0xa4a5: [0, 0, 0]}
        def resolve_symbols_to_file_offset_based_dict(byte_edits_arr: List[ByteEdit]) -> Dict[int, Iterable[int]]:
            this_patch_as_dict: Dict[int, Iterable[int]] = {}
            for byte_edit in byte_edits_arr:
                offset_within_rom_file: int = byte_edit["sym"]["offset_within_rom_file"] + byte_edit["offset"]
                this_patch_as_dict[offset_within_rom_file] = byte_edit["values"]
            return this_patch_as_dict

        for patchname, byte_edits_arr in patchDict.items():
            patches.append(IPS_Patch(resolve_symbols_to_file_offset_based_dict(byte_edits_arr)))
        

        # set rom name
        # 21 bytes
        from Main import __version__
        self.romName = bytearray(f'SMMR{__version__.replace(".", "")[0:3]}{required_pysmmaprando_version.replace(".", "")}{self.player}{self.multiworld.seed:8}', 'utf8')[:21]
        self.romName.extend([0] * (21 - len(self.romName)))
        self.rom_name = self.romName
        # clients should read from 0x7FC0, the location of the rom title in the SNES header.
        patches.append(IPS_Patch({0x007FC0 : self.romName}))

        # array for each item: (must match Map Rando's new_game_extra.asm !initial_X addresses)
        #  offset within ROM of this item"s info (starting status)
        #  item bitmask or amount per pickup (BVOB = base value or bitmask),
        #  offset within ROM of this item"s info (starting maximum/starting collected items)
        #  
        #                                 current  BVOB   max
        #                                 -------  ----   ---
        startItemROMDict = {"ETank":        [ snes_to_pc(0xB5FE52), 0x64, snes_to_pc(0xB5FE54)],
                            "Missile":      [ snes_to_pc(0xB5FE5C),  0x5, snes_to_pc(0xB5FE5E)],
                            "Super":        [ snes_to_pc(0xB5FE60),  0x5, snes_to_pc(0xB5FE62)],
                            "PowerBomb":    [ snes_to_pc(0xB5FE64),  0x5, snes_to_pc(0xB5FE66)],
                            "ReserveTank":  [ snes_to_pc(0xB5FE56), 0x64, snes_to_pc(0xB5FE58)],
                            "Morph":        [ snes_to_pc(0xB5FE04),  0x4, snes_to_pc(0xB5FE06)],
                            "Bombs":        [ snes_to_pc(0xB5FE05), 0x10, snes_to_pc(0xB5FE07)],
                            "SpringBall":   [ snes_to_pc(0xB5FE04),  0x2, snes_to_pc(0xB5FE06)],
                            "HiJump":       [ snes_to_pc(0xB5FE05),  0x1, snes_to_pc(0xB5FE07)],
                            "Varia":        [ snes_to_pc(0xB5FE04),  0x1, snes_to_pc(0xB5FE06)],
                            "Gravity":      [ snes_to_pc(0xB5FE04), 0x20, snes_to_pc(0xB5FE06)],
                            "SpeedBooster": [ snes_to_pc(0xB5FE05), 0x20, snes_to_pc(0xB5FE07)],
                            "SpaceJump":    [ snes_to_pc(0xB5FE05),  0x2, snes_to_pc(0xB5FE07)],
                            "ScrewAttack":  [ snes_to_pc(0xB5FE04),  0x8, snes_to_pc(0xB5FE06)],
                            "Charge":       [ snes_to_pc(0xB5FE09), 0x10, snes_to_pc(0xB5FE0B)],
                            "Ice":          [ snes_to_pc(0xB5FE08),  0x2, snes_to_pc(0xB5FE0A)],
                            "Wave":         [ snes_to_pc(0xB5FE08),  0x1, snes_to_pc(0xB5FE0A)],
                            "Spazer":       [ snes_to_pc(0xB5FE08),  0x4, snes_to_pc(0xB5FE0A)],
                            "Plasma":       [ snes_to_pc(0xB5FE08),  0x8, snes_to_pc(0xB5FE0A)],
                            "Grapple":      [ snes_to_pc(0xB5FE05), 0x40, snes_to_pc(0xB5FE07)],
                            "XRayScope":    [ snes_to_pc(0xB5FE05), 0x80, snes_to_pc(0xB5FE07)]

        # BVOB = base value or bitmask
                            }
        mergedData = {}
        hasETank = False
        hasSpazer = False
        hasPlasma = False
        for startItem in self.startItems:
            item = startItem
            if item == "ETank": hasETank = True
            if item == "Spazer": hasSpazer = True
            if item == "Plasma": hasPlasma = True
            if (item in ["ETank", "Missile", "Super", "PowerBomb", "Reserve"]):
                (currentValue, amountPerItem, maxValue) = startItemROMDict[item]
                if currentValue in mergedData:
                    mergedData[currentValue] += amountPerItem
                    mergedData[maxValue] += amountPerItem
                else:
                    mergedData[currentValue] = amountPerItem
                    mergedData[maxValue] = amountPerItem
            else:
                (collected, bitmask, equipped) = startItemROMDict[item]
                if collected in mergedData:
                    mergedData[collected] |= bitmask
                    mergedData[equipped] |= bitmask
                else:
                    mergedData[collected] = bitmask
                    mergedData[equipped] = bitmask

        if hasETank:
            # we are overwriting the starting energy, so add up the E from 99 (normal starting energy) rather than from 0
            mergedData[snes_to_pc(0xB5FE52)] += 99
            mergedData[snes_to_pc(0xB5FE54)] += 99

        if hasSpazer and hasPlasma:
            # de-equip spazer.
            # otherwise, firing the unintended spazer+plasma combo would cause massive game glitches and crashes
            mergedData[snes_to_pc(0xB5FE0A)] &= ~0x4

        for key, value in mergedData.items():
            if (key > snes_to_pc(0xB5FE0B)):
                [w0, w1] = self.getWordArray(value)
                mergedData[key] = [w0, w1]
            else:
                mergedData[key] = [value]

        patches.append(IPS_Patch(mergedData))

        # commit all the changes we've made here to the ROM
        for ips in patches:
            patched_rom_bytes = ips.apply(patched_rom_bytes)

        outfilebase = self.multiworld.get_out_file_name_base(self.player)
        outputFilename = os.path.join(output_directory, f"{outfilebase}.sfc")

        with open(outputFilename, "wb") as binary_file:
            binary_file.write(bytes(patched_rom_bytes))

        try:
            self.write_crc(outputFilename)
        except:
            raise
        else:
            patch = SMMapRandoDeltaPatch(os.path.splitext(outputFilename)[0] + SMMapRandoDeltaPatch.patch_file_ending, player=self.player,
                                            player_name=self.multiworld.player_name[self.player], patched_path=outputFilename)
            patch.write()
        finally:
            if os.path.exists(outputFilename):
                os.unlink(outputFilename)
            self.rom_name_available_event.set()  # make sure threading continues and errors are collected

    def checksum_mirror_sum(self, start, length, mask = 0x800000):
        while not(length & mask) and mask:
            mask >>= 1

        part1 = sum(start[:mask]) & 0xFFFF
        part2 = 0

        next_length = length - mask
        if next_length:
            part2 = self.checksum_mirror_sum(start[mask:], next_length, mask >> 1)

            while (next_length < mask):
                next_length += next_length
                part2 += part2

        return (part1 + part2) & 0xFFFF

    def write_bytes(self, buffer, startaddress: int, values):
        buffer[startaddress:startaddress + len(values)] = values

    def write_crc(self, romName):
        with open(romName, 'rb') as stream:
            buffer = bytearray(stream.read())
            crc = self.checksum_mirror_sum(buffer, len(buffer))
            inv = crc ^ 0xFFFF
            self.write_bytes(buffer, 0x7FDC, [inv & 0xFF, (inv >> 8) & 0xFF, crc & 0xFF, (crc >> 8) & 0xFF])
        with open(romName, 'wb') as outfile:
            outfile.write(buffer)

    def modify_multidata(self, multidata: dict):
        # wait for self.rom_name to be available.
        self.rom_name_available_event.wait()
        rom_name = getattr(self, "rom_name", None)
        # we skip in case of error, so that the original error in the output thread is the one that gets raised
        if rom_name:
            new_name = base64.b64encode(bytes(self.rom_name)).decode()
            multidata["connect_names"][new_name] = multidata["connect_names"][self.multiworld.player_name[self.player]]

    def fill_slot_data(self): 
        slot_data = {}
        if not self.multiworld.is_race:
            locations_nothing = [itemLoc.address - locations_start_id 
                                for itemLoc in self.locations.values()
                                if itemLoc.address is not None and itemLoc.player == self.player and itemLoc.item.code == items_start_id + self.nothing_item_id ]
        
            slot_data["locations_nothing"] = locations_nothing
                
        return slot_data
    
    
class SMMRLocation(Location):
    game: str = SMMapRandoWorld.game

    def __init__(self, player: int, name: str, address=None, parent=None):
        super(SMMRLocation, self).__init__(player, name, address, parent)

class SMMRItem(Item):
    game: str = SMMapRandoWorld.game

    def __init__(self, name, classification, code, player: int):
        super(SMMRItem, self).__init__(name, classification, code, player)

class SMMREntrance(Entrance):
    game: str = SMMapRandoWorld.game

    def __init__(self, player: int, name: str = '', parent: Region = None, strats_links: Dict[str, List[int]] = None, strats_links_debug: Dict[str, List[str]] = None):
        super(SMMREntrance, self).__init__(player, name, parent)
        self.strats_links = strats_links
        self.strats_links_debug = strats_links_debug

class SMMRRegion(Region):
    game: str = SMMapRandoWorld.game

    def __init__(self, name: str, player: int, multiworld: MultiWorld, index:int, hint: Optional[str] = None):
        super(SMMRRegion, self).__init__(name, player, multiworld, hint)
        self.index = index

    def can_reach(self, state: CollectionState) -> bool:
        f_regions = set()
        r_regions = set()
        if state.stale[self.player]:
            local_world = self.multiworld.worlds[self.player]
            defeated_mother_brain_flag_id = local_world.item_name_to_id["f_DefeatedMotherBrain"] - items_start_id - len(local_world.gamedata.item_isv)
            rrp = state.reachable_regions[self.player]
            state.stale[self.player] = False
            (bi_reachability, f_reachability, r_reachability, f_traverse, r_traverse) = local_world.map_rando.update_reachability(state.smmrcs[self.player].randomization_state, local_world.debug)
            local_world.update_reachability += 1
            for i, region in enumerate(bi_reachability):
                #if f_reachability[i] and local_world.events_connections.get(local_world.region_map_reverse[i], None) != None:
                #    state.reachable_regions[self.player].add(local_world.region_dict[i])
                #    event_src = local_world.events_connections.get(local_world.region_map_reverse[i], None)
                #    if (event_src != None):
                #        for event in event_src:
                #            state.reachable_regions[self.player].add(local_world.region_dict[local_world.vertex_cnt + SMMapRandoWorld.flag_location_names[local_world.map_rando.randomizer.game_data.flag_isv[event]]])
                if region:
                    rrp.add(local_world.region_dict[i])
                    # check for added events regions that MapRando doesnt know about
                    event_src = local_world.events_connections.get(local_world.region_map_reverse[i], None)
                    if (event_src != None):
                        for event in event_src:
                            rrp.add(local_world.region_dict[local_world.flag_id_to_region_dict[event] + local_world.vertex_cnt])
                if (f_reachability[i]):
                    f_regions.add(local_world.region_dict[i])
                    # special case for f_DefeatedMotherBrain as it cant be reverse reachable
                    event_src = local_world.events_connections.get(local_world.region_map_reverse[i], None)
                    if (event_src != None):
                        for event in event_src:
                            if event == defeated_mother_brain_flag_id:
                                rrp.add(local_world.region_dict[local_world.flag_id_to_region_dict[defeated_mother_brain_flag_id] + local_world.vertex_cnt])

                if (r_reachability[i]):
                    r_regions.add(local_world.region_dict[i])
            #state.update_reachable_regions(self.player)
            if local_world.debug:
                local_world.debug = False
        return self in state.reachable_regions[self.player]