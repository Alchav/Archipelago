import hashlib
import logging
import typing

from BaseClasses import Tutorial, ItemClassification, MultiWorld, Region, Entrance, Item
from worlds.AutoWorld import World, WebWorld
from worlds.generic.Rules import set_rule, add_rule
from .Names import *
from .Items import item_table, item_names, MM2Item, filler_item_table, filler_item_weights, robot_master_weapon_table, \
    stage_access_table, item_item_table
from .Locations import location_table, MM2Location, mm2_regions
from .Rom import get_base_rom_bytes, get_base_rom_path, RomData, patch_rom, extract_mm2, MM2DeltaPatch, \
    MM2LCHASH, PROTEUSHASH, MM2VCHASH, MM2NESHASH
from .Options import MM2Options
from .Client import MegaMan2Client
from .Rules import set_rules, weapon_damage, robot_masters, weapons_to_name
import os
import threading
import base64
import settings
from worlds.LauncherComponents import components, SuffixIdentifier
logger = logging.getLogger("Mega Man 2")

if typing.TYPE_CHECKING:
    from BaseClasses import CollectionState


class MM2Settings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the MM2 EN rom"""
        description = "Mega Man 2 ROM File"
        copy_to = "Mega Man 2 (USA).nes"
        md5s = [MM2NESHASH, MM2VCHASH, MM2LCHASH, PROTEUSHASH]

        def browse(self: settings.T,
                   filetypes: typing.Optional[typing.Sequence[typing.Tuple[str, typing.Sequence[str]]]] = None,
                   **kwargs: typing.Any) -> typing.Optional[settings.T]:
            if not filetypes:
                from Utils import is_windows
                file_types = [("NES", [".nes"]), ("Program", [".exe"] if is_windows else [""])]
                return super().browse(file_types, **kwargs)
            else:
                return super().browse(filetypes, **kwargs)

        def validate(self, path: str) -> None:
            """Try to open and validate file against hashes"""
            with open(path, "rb", buffering=0) as f:
                try:
                    self._validate_stream_hashes(f)
                    base_rom_bytes = f.read()
                    basemd5 = hashlib.md5()
                    basemd5.update(base_rom_bytes)
                    if basemd5.hexdigest() == PROTEUSHASH:
                        # we need special behavior here
                        self.copy_to = None
                except ValueError:
                    raise ValueError(f"File hash does not match for {path}")

    rom_file: RomFile = RomFile(RomFile.copy_to)


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
    In the year 200X, following his prior defeat by Mega Man, the evil Dr. Wily has returned to take over the world with
    his own group of Robot Masters. Mega Man once again sets out to defeat the eight Robot Masters and stop Dr. Wily.

    """

    game = "Mega Man 2"
    settings: typing.ClassVar[MM2Settings]
    options_dataclass = MM2Options
    options: MM2Options
    item_name_to_id = {item: item_table[item].code for item in item_table}
    location_name_to_id = location_table
    item_name_groups = item_names
    data_version = 0
    web = MM2WebWorld()
    boss_requirements = dict()

    def __init__(self, world: MultiWorld, player: int):
        self.rom_name_available_event = threading.Event()
        super().__init__(world, player)
        self.weapon_damage = weapon_damage.copy()

    @classmethod
    def stage_assert_generate(cls, multiworld: MultiWorld) -> None:
        rom_file: str = get_base_rom_path()
        if not os.path.exists(rom_file):
            raise FileNotFoundError(f"Could not find base ROM for {cls.game}: {rom_file}")

    def create_regions(self):
        menu = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu)
        for region in mm2_regions:
            stage = Region(region, self.player, self.multiworld)
            required_items = mm2_regions[region][0]
            locations = mm2_regions[region][1]
            prevStage = mm2_regions[region][2]
            if prevStage is None:
                entrance = Entrance(self.player, f"To {region}", menu)
                menu.exits.append(entrance)
            else:
                old_stage = self.multiworld.get_region(prevStage, self.player)
                entrance = Entrance(self.player, f"To {region}", old_stage)
                old_stage.exits.append(entrance)
            entrance.connect(stage)
            for item in required_items:
                add_rule(entrance, lambda state, required_item=item: state.has(required_item, self.player))
            stage.add_locations(locations)
            for location in stage.get_locations():
                if location.address is None and location.name is not Names.dr_wily:
                    location.place_locked_item(MM2Item(location.name, ItemClassification.progression,
                                                       None, self.player))
            if self.options.consumables:
                if region in Locations.consumables:
                    stage.add_locations(Locations.consumables[region], MM2Location)
            self.multiworld.regions.append(stage)

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
        # grab first robot master
        robot_master = self.item_id_to_name[0x880101 + self.options.starting_robot_master.value]
        self.multiworld.push_precollected(self.create_item(robot_master))
        itempool.extend([self.create_item(name) for name in stage_access_table.keys()
                         if name != robot_master])
        itempool.extend([self.create_item(name) for name in robot_master_weapon_table.keys()])
        itempool.extend([self.create_item(name) for name in item_item_table.keys()])
        remaining = 24 + (38 if self.options.consumables else 0) - len(itempool)
        itempool.extend([self.create_item(self.get_filler_item_name())
                         for _ in range(remaining)])
        self.multiworld.itempool += itempool

    set_rules = set_rules

    def generate_early(self) -> None:
        if (not self.options.yoku_jumps
            and self.options.starting_robot_master.current_key == "heat_man") or \
                (not self.options.enable_lasers
                 and self.options.starting_robot_master.current_key == "quick_man"):
            robot_master_pool = [1, 2, 3, 5, 6, 7, ]
            if self.options.yoku_jumps:
                robot_master_pool.append(0)
            if self.options.enable_lasers:
                robot_master_pool.append(4)
            self.options.starting_robot_master.value = self.random.choice(robot_master_pool)
            logger.warning(
                f"Incompatible starting Robot Master, changing to {self.options.starting_robot_master.current_key.replace('_', ' ').title()}")

    def generate_basic(self) -> None:
        goal_location = self.multiworld.get_location(Names.dr_wily, self.player)
        goal_location.place_locked_item(MM2Item("Victory", ItemClassification.progression, None, self.player))
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

    def generate_output(self, output_directory: str):
        rompath = ""
        try:
            world = self.multiworld
            player = self.player

            rom = RomData(get_base_rom_bytes())
            patch_rom(self, rom)

            rompath = os.path.join(output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}.nes")
            rom.write_to_file(rompath)
            self.rom_name = rom.name

            patch = MM2DeltaPatch(os.path.splitext(rompath)[0] + MM2DeltaPatch.patch_file_ending, player=player,
                                  player_name=world.player_name[player], patched_path=rompath)
            patch.write()
        except Exception:
            raise
        finally:
            self.rom_name_available_event.set()  # make sure threading continues and errors are collected
            if os.path.exists(rompath):
                os.unlink(rompath)

    def fill_slot_data(self) -> typing.Dict[str, typing.Any]:
        return {
            "death_link": self.options.death_link.value
        }

    def modify_multidata(self, multidata: dict):
        # wait for self.rom_name to be available.
        self.rom_name_available_event.wait()
        rom_name = getattr(self, "rom_name", None)
        # we skip in case of error, so that the original error in the output thread is the one that gets raised
        if rom_name:
            new_name = base64.b64encode(bytes(self.rom_name)).decode()
            multidata["connect_names"][new_name] = multidata["connect_names"][self.multiworld.player_name[self.player]]

    def collect(self, state: "CollectionState", item: "Item") -> bool:
        change = super().collect(state, item)
        if change and item.name in self.item_name_groups["Weapons"]:
            # need to evaluate robot master access
            weapon = next((wp for wp in weapons_to_name if weapons_to_name[wp] == item.name), None)
            if weapon:
                for rbm in robot_masters:
                    if (weapon != 1 and self.weapon_damage[weapon][rbm] > 0) or self.weapon_damage[weapon][rbm] >= 14:
                        state.prog_items[self.player][robot_masters[rbm]] = 1
        return change

    def remove(self, state: "CollectionState", item: "Item") -> bool:
        change = super().remove(state, item)
        if change and item.name in self.item_name_groups["Weapons"]:
            weapon = next((weapons_to_name[weapon] == item.name for weapon in weapons_to_name), None)
            received_weapons = {weapon for weapon in weapons_to_name if weapons_to_name[weapon] in state.prog_items}
            if weapon:
                for rbm in robot_masters:
                    if self.weapon_damage[weapon][rbm] > 0 and not any(self.weapon_damage[wp][rbm] > 0
                                                                       for wp in received_weapons):
                        state.prog_items[self.player][robot_masters[rbm]] = 0
        return change
