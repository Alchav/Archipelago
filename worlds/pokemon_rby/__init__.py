import settings
import typing
import threading
import base64
import random
from copy import deepcopy
from typing import TextIO

from Utils import __version__
from BaseClasses import Item, MultiWorld, Tutorial, ItemClassification
from Fill import fill_restrictive, FillError, sweep_from_pool
from worlds.AutoWorld import World, WebWorld
from worlds.generic.Rules import add_item_rule
from .items import item_table, item_groups
from .locations import (PokemonRedLocation, PokemonBlueLocation, PokemonYellowLocation, build_location_data,
                        build_location_name_to_id, location_data_blue, location_data_red, location_data_yellow)
from .regions import create_regions
from .options import PokemonRBOptions, PokemonYellowOptions
from .rom_addresses import rom_addresses_rb, rom_addresses_yellow
from .text import encode_text
from .rom import generate_output, PokemonRedProcedurePatch, PokemonBlueProcedurePatch, PokemonYellowProcedurePatch
from .pokemon import process_pokemon_data, process_move_data, verify_hm_moves
from .encounters import process_pokemon_locations, process_trainer_data
from .rules import set_rules
from .level_scaling import level_scaling
from .trainer_data import trainer_data_rb, trainer_data_yellow
from .trade_data import trade_data_blue, trade_data_red, trade_data_yellow
from .warp_data import warp_data_rb, warp_data_yellow
from . import logic
from . import poke_data
from . import client


class PokemonRedSettings(settings.Group):
    class RedRomFile(settings.UserFilePath):
        """File name of the Pokemon Red rom"""
        description = "Pokemon Red (UE) ROM File"
        copy_to = "Pokemon Red (UE) [S][!].gb"
        md5s = [PokemonRedProcedurePatch.hash]
    red_rom_file: RedRomFile = RedRomFile(RedRomFile.copy_to)

class PokemonBlueSettings(settings.Group):
    class BlueRomFile(settings.UserFilePath):
        """File name of the Pokemon Blue rom"""
        description = "Pokemon Blue (UE) ROM File"
        copy_to = "Pokemon Blue (UE) [S][!].gb"
        md5s = [PokemonBlueProcedurePatch.hash]
    blue_rom_file: BlueRomFile = BlueRomFile(BlueRomFile.copy_to)

class PokemonYellowSettings(settings.Group):
    class YellowRomFile(settings.UserFilePath):
        """File name of the Pokemon Yellow rom"""
        description = "Pokemon Yellow (UE) ROM File"
        copy_to = "Pokemon Yellow (U)[C][!].gbc"
        md5s = [PokemonYellowProcedurePatch.hash]
    yellow_rom_file: YellowRomFile = YellowRomFile(YellowRomFile.copy_to)


class PokemonWebWorld(WebWorld):
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to playing Pokémon Red, Blue, and Yellow with Archipelago.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Alchav"]
    )

    setup_es = Tutorial(
        setup_en.tutorial_name,
        setup_en.description,
        "Español",
        "setup_es.md",
        "setup/es",
        ["Shiny"]
    )

    tutorials = [setup_en, setup_es]



class PokemonRBYWorld(World):
    """Pokémon Red and Pokémon Blue are the original monster-collecting turn-based RPGs.  Explore the Kanto region with
    your Pokémon, catch more than 150 unique creatures, earn badges from the region's Gym Leaders, and challenge the
    Elite Four to become the champion!"""
    # -MuffinJets#4559

    options_dataclass = PokemonRBOptions
    options: PokemonRBOptions

    required_client_version = (0, 4, 2)

    topology_present = True
    ut_can_gen_without_yaml = True

    item_name_to_id = {name: data.id for name, data in item_table.items()}
    location_data = []
    level_list = []
    level_name_list = []
    location_groups = {}
    location_name_to_id = {}
    trade_data = []
    warp_data = {}
    pokemon_data = poke_data.pokemon_data
    pokemon_learnsets = poke_data.learnsets
    item_name_groups = item_groups
    location_name_groups = {}

    glitches_item_name = "ut_glitch"

    web = PokemonWebWorld()

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.item_pool = []
        self.total_key_items = None
        self.fly_map = None
        self.fly_map_code = None
        self.town_map_fly_map = None
        self.town_map_fly_map_code = None
        self.extra_badges = {}
        self.type_chart = None
        self.local_poke_data = None
        self.local_move_data = None
        self.local_tms = None
        self.learnsets = None
        self.trainer_name = None
        self.rival_name = None
        self.traps = None
        self.trade_mons = {}
        self.finished_level_scaling = threading.Event()
        self.dexsanity_table = []
        self.trainersanity_table = []
        self.local_locs = []
        self.rock_tunnel_1f_data = None
        self.rock_tunnel_b1f_data = None
        self.gen_seed = None
        self.region_seed = None
        self.rock_tunnel_seed = None
        self.mapped_door_shuffle_spoiler = []
        self.ut = False

    @classmethod
    def stage_generate_early(cls, multiworld: MultiWorld):
        if getattr(multiworld, "_pokemon_rby_stage_generate_early_claimed", False):
            return
        multiworld._pokemon_rby_stage_generate_early_claimed = True

        seed_groups = {}
        pokemon_rb_worlds = list(get_rby_worlds(multiworld))

        for world in pokemon_rb_worlds:
            if not (world.options.type_chart_seed.value.isdigit() or world.options.type_chart_seed.value == "random"):
                seed_groups[world.options.type_chart_seed.value] = seed_groups.get(world.options.type_chart_seed.value,
                                                                                   []) + [world]

        copy_chart_worlds = {}

        for worlds in seed_groups.values():
            chosen_world = multiworld.random.choice(worlds)
            for world in worlds:
                if world is not chosen_world:
                    copy_chart_worlds[world.player] = chosen_world

        for world in pokemon_rb_worlds:
            if world.player in copy_chart_worlds:
                continue
            tc_random = world.random
            if world.options.type_chart_seed.value.isdigit():
                tc_random = random.Random()
                tc_random.seed(int(world.options.type_chart_seed.value))

            if world.options.randomize_type_chart == "vanilla":
                chart = deepcopy(poke_data.type_chart)
            elif world.options.randomize_type_chart == "randomize":
                types = poke_data.type_names.values()
                matchups = []
                for type1 in types:
                    for type2 in types:
                        matchups.append([type1, type2])
                tc_random.shuffle(matchups)
                immunities = world.options.immunity_matchups.value
                super_effectives = world.options.super_effective_matchups.value
                not_very_effectives = world.options.not_very_effective_matchups.value
                normals = world.options.normal_matchups.value
                while super_effectives + not_very_effectives + normals < 225 - immunities:
                    if super_effectives == not_very_effectives == normals == 0:
                        super_effectives = 225
                        not_very_effectives = 225
                        normals = 225
                    else:
                        super_effectives += world.options.super_effective_matchups.value
                        not_very_effectives += world.options.not_very_effective_matchups.value
                        normals += world.options.normal_matchups.value
                if super_effectives + not_very_effectives + normals > 225 - immunities:
                    total = super_effectives + not_very_effectives + normals
                    excess = total - (225 - immunities)
                    subtract_amounts = (
                        int((excess / (super_effectives + not_very_effectives + normals)) * super_effectives),
                        int((excess / (super_effectives + not_very_effectives + normals)) * not_very_effectives),
                        int((excess / (super_effectives + not_very_effectives + normals)) * normals))
                    super_effectives -= subtract_amounts[0]
                    not_very_effectives -= subtract_amounts[1]
                    normals -= subtract_amounts[2]
                    while super_effectives + not_very_effectives + normals > 225 - immunities:
                        r = tc_random.randint(0, 2)
                        if r == 0 and super_effectives:
                            super_effectives -= 1
                        elif r == 1 and not_very_effectives:
                            not_very_effectives -= 1
                        elif normals:
                            normals -= 1
                chart = []
                for matchup_list, matchup_value in zip([immunities, normals, super_effectives, not_very_effectives],
                                                       [0, 10, 20, 5]):
                    for _ in range(matchup_list):
                        matchup = matchups.pop()
                        matchup.append(matchup_value)
                        chart.append(matchup)
            elif world.options.randomize_type_chart == "chaos":
                types = poke_data.type_names.values()
                matchups = []
                for type1 in types:
                    for type2 in types:
                        matchups.append([type1, type2])
                chart = []
                values = list(range(21))
                tc_random.shuffle(matchups)
                tc_random.shuffle(values)
                for matchup in matchups:
                    value = values.pop(0)
                    values.append(value)
                    matchup.append(value)
                    chart.append(matchup)
            # sort so that super-effective matchups occur first, to prevent dual "not very effective" / "super effective"
            # matchups from leading to damage being ultimately divided by 2 and then multiplied by 2, which can lead to
            # damage being reduced by 1 which leads to a "not very effective" message appearing due to my changes
            # to the way effectiveness messages are generated.
            world.type_chart = sorted(chart, key=lambda matchup: -matchup[2])

        for player in copy_chart_worlds:
            multiworld.worlds[player].type_chart = copy_chart_worlds[player].type_chart

    def generate_early(self):

        if hasattr(self.multiworld, "re_gen_passthrough") and self.game in self.multiworld.re_gen_passthrough:
            self.ut = True
            for key, value in self.multiworld.re_gen_passthrough[self.game].items():
                if hasattr(self.options, key):
                    option = getattr(self.options, key)
                    option.value = option.from_any(value).value
                else:
                    setattr(self, key, value)
            seed = self.gen_seed
        else:
            seed = self.random.randint(0, 999999999999999999)
        self.gen_seed = seed
        self.random.seed(seed)

        def encode_name(name, t):
            try:
                if len(encode_text(name)) > 7:
                    raise IndexError(f"{t} name too long for player {self.multiworld.player_name[self.player]}. Must be 7 characters or fewer.")
                return encode_text(name, length=8, whitespace="@", safety=True)
            except KeyError as e:
                raise KeyError(f"Invalid character(s) in {t} name for player {self.multiworld.player_name[self.player]}") from e
        if self.options.trainer_name == "choose_in_game":
            self.trainer_name = "choose_in_game"
        else:
            self.trainer_name = encode_name(self.options.trainer_name.value, "Player")
        if self.options.rival_name == "choose_in_game":
            self.rival_name = "choose_in_game"
        else:
            self.rival_name = encode_name(self.options.rival_name.value, "Rival")

        if not self.options.badgesanity:
            self.options.non_local_items.value -= self.item_name_groups["Badges"]

        if self.options.badges_needed_for_hm_moves.value >= 2:
            badges_to_add = ["Marsh Badge", "Volcano Badge", "Earth Badge"]
            if self.options.badges_needed_for_hm_moves.value == 3:
                badges = ["Boulder Badge", "Cascade Badge", "Thunder Badge", "Rainbow Badge", "Marsh Badge",
                          "Soul Badge", "Volcano Badge", "Earth Badge"]
                self.random.shuffle(badges)
                badges_to_add += [badges.pop(), badges.pop()]
            hm_moves = ["Cut", "Fly", "Surf", "Strength", "Flash"]
            self.random.shuffle(hm_moves)
            self.extra_badges = {}
            for badge in badges_to_add:
                self.extra_badges[hm_moves.pop()] = badge

        process_move_data(self)
        process_pokemon_data(self)


        dex_count = self.options.dexsanity.value
        trainersanity_count = self.options.trainersanity.value

        self.dexsanity_table = [
            *(True for _ in range(dex_count)),
            *(False for _ in range(151 - dex_count))
        ]
        self.random.shuffle(self.dexsanity_table)

        self.trainersanity_table = [
            *(True for _ in range(trainersanity_count)),
            *(False for _ in range(317 - trainersanity_count))
        ]
        self.random.shuffle(self.trainersanity_table)

    def create_regions(self):
        if self.ut:
            fly_map_code = self.free_fly_map
            town_map_fly_map_code = self.town_map_fly_map
        else:
            if (self.options.old_man == "vanilla" or
                    self.options.door_shuffle in ("full", "mapped", "insanity", "insanity_mapped")):
                fly_map_codes = self.random.sample(range(2, 11), 2)
            elif (self.options.door_shuffle == "simple" or
                    self.options.route_3_condition == "boulder_badge" or
                  (self.options.route_3_condition == "any_badge" and
                   self.options.badgesanity)):
                fly_map_codes = self.random.sample(range(3, 11), 2)

            else:
                fly_map_codes = self.random.sample([4, 6, 7, 8, 9, 10], 2)
            if self.options.free_fly_location:
                fly_map_code = fly_map_codes[0]
            else:
                fly_map_code = 0
            if self.options.town_map_fly_location:
                town_map_fly_map_code = fly_map_codes[1]
            else:
                town_map_fly_map_code = 0
        fly_maps = ["Pallet Town", "Viridian City", "Pewter City", "Cerulean City", "Lavender Town",
                    "Vermilion City", "Celadon City", "Fuchsia City", "Cinnabar Island", "Indigo Plateau",
                    "Saffron City"]
        self.fly_map = fly_maps[fly_map_code]
        self.town_map_fly_map = fly_maps[town_map_fly_map_code]
        self.fly_map_code = fly_map_code
        self.town_map_fly_map_code = town_map_fly_map_code

        create_regions(self)

    def create_items(self):
        process_pokemon_locations(self)
        self.multiworld.itempool += self.item_pool

    def set_rules(self):
        set_rules(self.multiworld, self, self.player)
        self.multiworld.completion_condition[self.player] = lambda state, player=self.player: state.has("Become Champion", player=player)

    def generate_basic(self):
        verify_hm_moves(self.multiworld, self, self.player)
        # TrackerCore regeneration stops at generate_basic. When slot data is available, use the exact set of
        # addressless Pokemon locations that remained progression after stage_post_fill in the real generated world.
        if self.ut and hasattr(self, "progression_pokemon_locations"):
            progression_locations = set(self.progression_pokemon_locations)
            for location in self.multiworld.get_locations(self.player):
                if (location.address is None and location.item
                        and (location.item.name in poke_data.pokemon_data
                             or location.item.name.startswith("Static "))):
                    location.item.classification = (
                        ItemClassification.progression
                        if location.name in progression_locations
                        else ItemClassification.useful
                    )
            return

        # Before fill, approximate spoiler/playthrough pressure by downgrading duplicate wild mons within a region.
        for region in self.multiworld.get_regions(self.player):
            region_mons = set()
            for location in region.locations:
                if "Wild Pokemon" in location.name:
                    if location.item.name in region_mons:
                        location.item.classification = ItemClassification.useful
                    else:
                        region_mons.add(location.item.name)

    def pre_fill(self) -> None:
        process_trainer_data(self)
        locs = [location.name for location in self.location_data if location.type != "Item"]
        for location in self.multiworld.get_locations(self.player):
            if location.name in locs:
                location.show_in_spoiler = False

        if self.options.old_man == "early_parcel":
            self.multiworld.local_early_items[self.player]["Oak's Parcel"] = 1
            if self.options.dexsanity:
                for i, mon in enumerate(poke_data.pokemon_data):
                    if self.dexsanity_table[i]:
                        location = self.multiworld.get_location(f"Pokedex - {mon}", self.player)
                        add_item_rule(location, lambda item: item.name != "Oak's Parcel" or item.player != self.player)

        # Place local items in some locations to prevent save-scumming. Also Oak's PC to prevent an "AP Item" from
        # entering the player's inventory.

        locs = {self.multiworld.get_location("Fossil - Choice A", self.player),
                self.multiworld.get_location("Fossil - Choice B", self.player)}

        rule = None
        if self.options.fossil_check_item_types == "key_items":
            rule = lambda i: i.advancement
        elif self.options.fossil_check_item_types == "unique_items":
            rule = lambda i: i.name in item_groups["Unique"]
        elif self.options.fossil_check_item_types == "no_key_items":
            rule = lambda i: not i.advancement
        if rule:
            for loc in locs:
                add_item_rule(loc, rule)

        for mon in ([" ".join(self.multiworld.get_location(
                f"Oak's Lab - Starter {i}", self.player).item.name.split(" ")[1:]) for i in range(1, 4)]
                if self.game != "Pokemon Yellow" else []
                + [" ".join(self.multiworld.get_location(
                f"Saffron Fighting Dojo - Gift {i}", self.player).item.name.split(" ")[1:]) for i in range(1, 3)]
                + ["Vaporeon", "Jolteon", "Flareon"]):
            if self.dexsanity_table[poke_data.pokemon_dex[mon] - 1]:
                loc = self.multiworld.get_location(f"Pokedex - {mon}", self.player)
                if loc.item is None:
                    locs.add(loc)

        for loc in sorted(locs):
            if loc.name in self.options.priority_locations.value:
                add_item_rule(loc, lambda i: i.advancement)
            add_item_rule(loc, lambda i: i.player == self.player
                                         or (i.player in self.multiworld.groups
                                             and self.player in self.multiworld.groups[i.player]["players"]))
            if self.options.old_man == "early_parcel" and loc.name != "Player's House 2F - Player's PC":
                add_item_rule(loc, lambda i: i.name != "Oak's Parcel")

        self.local_locs = locs

        all_state = self.multiworld.get_all_state(False, True, False)

        reachable_mons = set()
        for mon in poke_data.pokemon_data:
            if logic.has_pokedex_mon(all_state, mon, self.player):
                reachable_mons.add(mon)

        self.options.elite_four_pokedex_condition.total = \
            int((len(reachable_mons) / 100) * self.options.elite_four_pokedex_condition.value)

    @classmethod
    def stage_fill_hook(cls, multiworld, progitempool, usefulitempool, filleritempool, fill_locations):
        if getattr(multiworld, "_pokemon_rby_stage_fill_hook_claimed", False):
            return
        multiworld._pokemon_rby_stage_fill_hook_claimed = True

        locs = []
        for world in get_rby_worlds(multiworld):
            locs += world.local_locs
        for loc in sorted(locs):
            if loc.item:
                continue
            itempool = progitempool + usefulitempool + filleritempool
            multiworld.random.shuffle(itempool)
            unplaced_items = []
            for i, item in enumerate(itempool):
                if ((item.player == loc.player or (item.player in multiworld.groups
                                                   and loc.player in multiworld.groups[item.player]["players"]))
                        and loc.can_fill(multiworld.state, item, False)):
                    if item.advancement:
                        pool = progitempool
                    elif item.useful:
                        pool = usefulitempool
                    else:
                        pool = filleritempool
                    for i, check_item in enumerate(pool):
                        if item is check_item:
                            pool.pop(i)
                            break
                    if item.advancement:
                        state = sweep_from_pool(multiworld.state, progitempool + unplaced_items)
                    if (not item.advancement) or state.can_reach(loc, "Location", loc.player):
                        multiworld.push_item(loc, item, False)
                        fill_locations.remove(loc)
                        break
                    else:
                        unplaced_items.append(item)
            progitempool += [item for item in unplaced_items if item.advancement]
            usefulitempool += [item for item in unplaced_items if item.useful]
            filleritempool += [item for item in unplaced_items if (not item.advancement) and (not item.useful)]


    def fill_hook(self, progitempool, usefulitempool, filleritempool, fill_locations):
        if not self.options.badgesanity:
            # Door Shuffle options besides Simple place badges during door shuffling
            if self.options.door_shuffle in ("off", "simple"):
                badges = [item for item in progitempool if "Badge" in item.name and item.player == self.player]
                for badge in badges:
                    self.multiworld.itempool.remove(badge)
                    progitempool.remove(badge)
                for attempt in range(6):
                    badgelocs = [
                        self.multiworld.get_location(loc, self.player) for loc in [
                            "Pewter Gym - Brock Prize", "Cerulean Gym - Misty Prize",
                            "Vermilion Gym - Lt. Surge Prize", "Celadon Gym - Erika Prize",
                            "Fuchsia Gym - Koga Prize", "Saffron Gym - Sabrina Prize",
                            "Cinnabar Gym - Blaine Prize", "Viridian Gym - Giovanni Prize"
                        ] if self.multiworld.get_location(loc, self.player).item is None]
                    state = self.multiworld.get_all_state(False, True, False)
                    # Give it two tries to place badges with wild Pokemon and learnsets as-is.
                    # If it can't, then try with all Pokemon collected, and we'll try to fix HM move availability after.
                    if attempt > 1:
                        for mon in poke_data.pokemon_data.keys():
                            state.collect(self.create_item(mon), True)
                    state.sweep_for_advancements()
                    self.random.shuffle(badges)
                    self.random.shuffle(badgelocs)
                    badgelocs_copy = badgelocs.copy()
                    # allow_partial so that unplaced badges aren't lost, for debugging purposes
                    fill_restrictive(self.multiworld, state, badgelocs_copy, badges, True, True, allow_partial=True)
                    if len(badges) > 8 - len(badgelocs):
                        for location in badgelocs:
                            if location.item:
                                badges.append(location.item)
                                location.item = None
                        continue
                    else:
                        for location in badgelocs:
                            if location.item:
                                fill_locations.remove(location)
                        progitempool += badges
                        break
                else:
                    raise FillError(f"Failed to place badges for player {self.player}")
            verify_hm_moves(self.multiworld, self, self.player)

        tms = [item for item in usefulitempool + filleritempool if item.name.startswith("TM") and (item.player ==
               self.player or (item.player in self.multiworld.groups and self.player in
                               self.multiworld.groups[item.player]["players"]))]
        if len(tms) > 7:
            for gym_leader in (("Pewter Gym", "Brock"), ("Cerulean Gym", "Misty"), ("Vermilion Gym", "Lt. Surge"),
                               ("Celadon Gym-C", "Erika"), ("Fuchsia Gym", "Koga"), ("Saffron Gym-C", "Sabrina"),
                               ("Cinnabar Gym", "Blaine"), ("Viridian Gym", "Giovanni")):
                loc = self.multiworld.get_location(f"{gym_leader[0].split('-')[0]} - {gym_leader[1]} TM",
                                                   self.player)
                if loc.item:
                    continue
                for party in self.multiworld.get_location(gym_leader[0] + " - Trainer Parties", self.player).party_data:
                    if party["party_address"] == \
                            f"Trainer_Party_{gym_leader[1].replace('. ', '').replace('Giovanni', 'Viridian_Gym_Giovanni')}_A":
                        mon = party["party"][-1]
                        learnable_tms = [tm for tm in tms if self.local_poke_data[mon]["tms"][
                            int((int(tm.name[2:4]) - 1) / 8)] & 1 << ((int(tm.name[2:4]) - 1) % 8)]
                        if not learnable_tms:
                            learnable_tms = tms
                        tm = self.random.choice(learnable_tms)

                        loc.place_locked_item(tm)
                        fill_locations.remove(loc)
                        tms.remove(tm)
                        if tm.useful:
                            usefulitempool.remove(tm)
                        else:
                            filleritempool.remove(tm)
                        break
                else:
                    raise Exception("Missing Gym Leader data")

    @classmethod
    def stage_post_fill(cls, multiworld):
        # The shared Pokemon R/B/Y stage methods are inherited by all three world classes,
        # so this prevents stage_post_fill from running multiple times for the same multiworld.
        if getattr(multiworld, "_pokemon_rby_stage_post_fill_claimed", False):
            return
        multiworld._pokemon_rby_stage_post_fill_claimed = True

        # Convert all but one of each instance of a wild Pokemon to useful classification.
        # This cuts down on time spent calculating the spoiler playthrough.
        found_mons = set()
        for sphere in multiworld.get_spheres():
            mon_locations_in_sphere = {}
            for location in sphere:
                if (location.game == location.item.game and location.game in pokemon_rby_games
                        and (location.item.name in poke_data.pokemon_data.keys() or "Static " in location.item.name)
                        and location.item.advancement):
                    key = (location.player, location.item.name)
                    if key in found_mons:
                        location.item.classification = ItemClassification.useful
                    else:
                        mon_locations_in_sphere.setdefault(key, []).append(location)
            for key, mon_locations in mon_locations_in_sphere.items():
                found_mons.add(key)
                if len(mon_locations) > 1:
                    # Sort for deterministic results.
                    mon_locations.sort()
                    # Convert all but the first to useful classification.
                    for location in mon_locations[1:]:
                        location.item.classification = ItemClassification.useful

    @classmethod
    def stage_generate_output(cls, multiworld, output_directory):
        if getattr(multiworld, "_pokemon_rby_level_scaling_claimed", False):
            return
        multiworld._pokemon_rby_level_scaling_claimed = True
        level_scaling(multiworld)

    def generate_output(self, output_directory: str):
        generate_output(self, output_directory)

    def get_pre_fill_items(self) -> typing.List["Item"]:
        pool = [self.create_item(mon) for mon in poke_data.pokemon_data]
        return pool

    def modify_multidata(self, multidata: dict):
        rom_name = bytearray(f'AP{__version__.replace(".", "")[0:3]}_{self.player}_{self.multiworld.seed:11}\0',
                             'utf8')[:21]
        rom_name.extend([0] * (21 - len(rom_name)))
        new_name = base64.b64encode(bytes(rom_name)).decode()
        multidata["connect_names"][new_name] = multidata["connect_names"][self.multiworld.player_name[self.player]]

    def write_spoiler_header(self, spoiler_handle: TextIO):
        spoiler_handle.write(f"Cerulean Cave Total Key Items:   {self.options.cerulean_cave_key_items_condition.total}\n")
        spoiler_handle.write(f"Elite Four Total Key Items:      {self.options.elite_four_key_items_condition.total}\n")
        spoiler_handle.write(f"Elite Four Total Pokemon:        {self.options.elite_four_pokedex_condition.total}\n")
        if self.options.free_fly_location:
            spoiler_handle.write(f"Free Fly Location:               {self.fly_map}\n")
        if self.options.town_map_fly_location:
            spoiler_handle.write(f"Town Map Fly Location:           {self.town_map_fly_map}\n")
        if self.extra_badges:
            for hm_move, badge in self.extra_badges.items():
                spoiler_handle.write(hm_move + " enabled by: " + (" " * 20)[:20 - len(hm_move)] + badge + "\n")

    def write_spoiler(self, spoiler_handle):
        if self.mapped_door_shuffle_spoiler:
            spoiler_handle.write(f"\n\nMapped door shuffle region groups "
                                 f"({self.multiworld.player_name[self.player]}):\n\n")
            for slot_group, replacement_group in self.mapped_door_shuffle_spoiler:
                spoiler_handle.write(f"{slot_group}: {replacement_group}\n")
        if self.options.randomize_type_chart:
            spoiler_handle.write(f"\n\nType matchups ({self.multiworld.player_name[self.player]}):\n\n")
            for matchup in self.type_chart:
                spoiler_handle.write(f"{matchup[0]} deals {matchup[2] * 10}% damage to {matchup[1]}\n")
        spoiler_handle.write(f"\n\nPokémon locations ({self.multiworld.player_name[self.player]}):\n\n")
        pokemon_locs = [
            location.name
            for location in self.location_data
            if location.type not in ("Item", "Trainer Parties")
        ]
        for location in self.multiworld.get_locations(self.player):
            if location.name in pokemon_locs:
                spoiler_handle.write(location.name + ": " + location.item.name + "\n")

    def get_filler_item_name(self) -> str:
        combined_traps = (self.options.poison_trap_weight.value
                          + self.options.fire_trap_weight.value
                          + self.options.paralyze_trap_weight.value
                          + self.options.ice_trap_weight.value
                          + self.options.sleep_trap_weight.value)
        if (combined_traps > 0 and
                self.random.randint(1, 100) <= self.options.trap_percentage.value):
            return self.select_trap()
        banned_items = item_groups["Unique"].copy()
        if (((not self.options.tea) or "Saffron City" not in [self.fly_map, self.town_map_fly_map])
                and (not self.options.door_shuffle)):
            # under these conditions, you should never be able to reach the Copycat or Pokémon Tower without being
            # able to reach the Celadon Department Store, so Poké Dolls would not allow early access to anything
            banned_items.append("Poke Doll")
        if not self.options.tea:
            banned_items += item_groups["Vending Machine Drinks"]
        return self.random.choice([item for item in item_table if item_table[item].id and item_table[
            item].classification == ItemClassification.filler and item not in banned_items])

    def select_trap(self):
        if self.traps is None:
            self.traps = []
            self.traps += ["Poison Trap"] * self.options.poison_trap_weight.value
            self.traps += ["Fire Trap"] * self.options.fire_trap_weight.value
            self.traps += ["Paralyze Trap"] * self.options.paralyze_trap_weight.value
            self.traps += ["Ice Trap"] * self.options.ice_trap_weight.value
            self.traps += ["Sleep Trap"] * self.options.sleep_trap_weight.value
        return self.random.choice(self.traps)

    def extend_hint_information(self, hint_data):
        if self.options.dexsanity or self.options.door_shuffle:
            hint_data[self.player] = {}
        if self.options.dexsanity:
            mon_locations = {mon: set() for mon in poke_data.pokemon_data.keys()}
            for loc in self.location_data:
                if loc.type in ["Wild Encounter", "Static Pokemon", "Legendary Pokemon"]:
                    mon = self.multiworld.get_location(loc.name, self.player).item.name
                    if mon.startswith("Static "):
                        mon = " ".join(mon.split(" ")[1:])
                    if "Wild" in loc.name or "Fishing" in loc.name or "Prize" in loc.name:
                        encounter_label = loc.name.split(" -")[0]
                    elif "Surf" in loc.name:
                        encounter_label = f"{loc.name.split(' -')[0]} (Surf)"
                    elif "Fake" in loc.name:
                        encounter_label = f"{loc.name.split(' -')[0]} (Fake Pokeball)"
                    else:
                        split_loc_name = loc.name.split(" - ")
                        encounter_label = f"{split_loc_name[0]} ({split_loc_name[1]})"
                    mon_locations[mon].add(encounter_label)
            for i, mon in enumerate(mon_locations):
                if self.dexsanity_table[i] and mon_locations[mon]:
                    hint_data[self.player][self.multiworld.get_location(f"Pokedex - {mon}", self.player).address] =\
                        ", ".join(mon_locations[mon])

        if self.options.door_shuffle:
            for location in self.multiworld.get_locations(self.player):
                if location.parent_region.entrance_hint and location.address:
                    hint_data[self.player][location.address] = location.parent_region.entrance_hint

    def fill_slot_data(self) -> dict:
        ret = self.options.as_dict(
            "accessibility", "trainer_name", "rival_name", "badgesanity", "fossil_check_item_types",
            "second_fossil_check_condition", "require_item_finder", "randomize_hidden_items",
            "badges_needed_for_hm_moves", "oaks_aide_rt_2", "oaks_aide_rt_11", "oaks_aide_rt_15",
            "extra_key_items", "extra_strength_boulders", "tea", "old_man", "elite_four_badges_condition",
            "elite_four_key_items_condition", "elite_four_pokedex_condition", "victory_road_condition",
            "route_22_gate_condition", "route_3_condition", "vermilion_city_jenny_requirement",
            "robbed_house_officer", "viridian_gym_condition", "cerulean_cave_badges_condition",
            "cerulean_cave_key_items_condition", "randomize_pokedex", "dexsanity", "trainersanity", "death_link",
            "prizesanity", "poke_doll_skip", "bicycle_gate_skips", "stonesanity", "door_shuffle", "warp_tile_shuffle",
            "dark_rock_tunnel_logic", "split_card_key", "all_elevators_locked", "require_pokedex",
            "area_1_to_1_mapping", "blind_trainers", "exp_all", "randomize_rock_tunnel", "randomize_pokemon_locations",
            "randomize_legendary_pokemon", "catch_em_all", "hm_same_type_compatibility", "hm_normal_type_compatibility",
            "hm_other_type_compatibility", "tm_same_type_compatibility", "tm_normal_type_compatibility",
            "tm_other_type_compatibility", "inherit_tm_hm_compatibility", "randomize_move_types", "move_balancing",
            "no_trapping_moves", "randomize_tm_moves", "randomize_pokemon_stats", "randomize_pokemon_catch_rates",
            "minimum_catch_rate", "randomize_pokemon_movesets", "confine_transform_to_ditto", "start_with_four_moves",
            "randomize_pokemon_types", "secondary_type_chance", "randomize_type_chart", "normal_matchups",
            "super_effective_matchups", "not_very_effective_matchups", "immunity_matchups", "type_chart_seed",
            "randomize_trainer_parties", "trainer_legendaries", "randomize_pokemon_palettes", "trap_percentage",
            "poison_trap_weight", "fire_trap_weight", "paralyze_trap_weight", "sleep_trap_weight", "ice_trap_weight"
        )
        ret |= {
            "free_fly_map": self.fly_map_code,
            "town_map_fly_map": self.town_map_fly_map_code,
            "extra_badges": self.extra_badges,
            "gen_seed": self.gen_seed,
            "region_seed": self.region_seed,
            "rock_tunnel_seed": self.rock_tunnel_seed,
            "progression_pokemon_locations": [
                location.name
                for location in self.multiworld.get_locations(self.player)
                if (location.address is None and location.item
                    and (location.item.name in poke_data.pokemon_data
                         or location.item.name.startswith("Static "))
                    and location.item.advancement)
            ],
        }
        if self.options.type_chart_seed == "random" or self.options.type_chart_seed.value.isdigit():
            ret["type_chart"] = self.type_chart

        return ret

    @staticmethod
    def interpret_slot_data(slot_data: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any]:
        return slot_data


class PokemonRedWorld(PokemonRBYWorld):
    game = "Pokemon Red"

    settings: typing.ClassVar[PokemonRedSettings]
    item_name_to_id = PokemonRBYWorld.item_name_to_id
    item_name_groups = PokemonRBYWorld.item_name_groups
    patch = PokemonRedProcedurePatch
    location = PokemonRedLocation
    rom_addresses = rom_addresses_rb
    trainer_data = trainer_data_rb
    trade_data = trade_data_red
    warp_data = warp_data_rb
    location_data, level_list, level_name_list, location_groups = build_location_data(
        location_data_red,
        trainer_data=trainer_data,
    )
    location_name_to_id = build_location_name_to_id(location_data)
    location_name_groups = location_groups

    def create_item(self, name: str) -> Item:
        return PokemonRedItem(name, self.player)

class PokemonBlueWorld(PokemonRBYWorld):
    game = "Pokemon Blue"

    settings: typing.ClassVar[PokemonBlueSettings]
    item_name_to_id = PokemonRBYWorld.item_name_to_id
    item_name_groups = PokemonRBYWorld.item_name_groups
    patch = PokemonBlueProcedurePatch
    location = PokemonBlueLocation
    rom_addresses = rom_addresses_rb
    trainer_data = trainer_data_rb
    trade_data = trade_data_blue
    warp_data = warp_data_rb
    location_data, level_list, level_name_list, location_groups = build_location_data(
        location_data_blue,
        trainer_data=trainer_data,
    )
    location_name_to_id = build_location_name_to_id(location_data)
    location_name_groups = location_groups

    def create_item(self, name: str) -> Item:
        return PokemonBlueItem(name, self.player)

class PokemonYellowWorld(PokemonRBYWorld):
    game = "Pokemon Yellow"

    options_dataclass = PokemonYellowOptions
    options: PokemonYellowOptions
    settings: typing.ClassVar[PokemonYellowSettings]
    item_name_to_id = PokemonRBYWorld.item_name_to_id
    item_name_groups = PokemonRBYWorld.item_name_groups
    patch = PokemonYellowProcedurePatch
    location = PokemonYellowLocation
    rom_addresses = rom_addresses_yellow
    trainer_data = trainer_data_yellow
    trade_data = trade_data_yellow
    warp_data = warp_data_yellow
    pokemon_data = poke_data.pokemon_data_yellow
    pokemon_learnsets = poke_data.learnsets_yellow
    location_data, level_list, level_name_list, location_groups = build_location_data(
        location_data_yellow,
        trainer_data=trainer_data,
    )
    location_name_to_id = build_location_name_to_id(location_data)
    location_name_groups = location_groups

    def create_item(self, name: str) -> Item:
        return PokemonYellowItem(name, self.player)


class PokemonRBYItem(Item):
    type = None

    def __init__(self, name, player: int = None):
        item_data = item_table[name]
        super(PokemonRBYItem, self).__init__(
            name,
            item_data.classification,
            item_data.id, player
        )

class PokemonRedItem(PokemonRBYItem):
    game = "Pokemon Red"

class PokemonBlueItem(PokemonRBYItem):
    game = "Pokemon Blue"

class PokemonYellowItem(PokemonRBYItem):
    game = "Pokemon Yellow"

pokemon_rby_games = ("Pokemon Red", "Pokemon Blue", "Pokemon Yellow")

def get_rby_worlds(multiworld: MultiWorld):
    for game in pokemon_rby_games:
        yield from multiworld.get_game_worlds(game)
