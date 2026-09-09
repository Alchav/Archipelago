import typing
import os
import json
import pkgutil
from .Items import item_data_table, action_item_data_table, cannon_item_data_table, cap_item_data_table, \
    castle_progression_item_data_table, feature_item_data_table, global_cap_item_names, \
    painting_unlock_item_data_table, item_table, SM64Item, global_checkerboard_item_names, \
    global_rolling_log_item_names, global_purple_switch_item_names, global_bobomb_buddy_item_names, \
    global_treasure_chest_item_names, global_warp_pipe_item_names, checkerboard_item_data_table, \
    global_vertical_wind_item_names, global_horizontal_wind_item_names, vertical_wind_item_data_table, \
    horizontal_wind_item_data_table, global_freestanding_star_item_names, freestanding_star_item_data_table, \
    global_star_block_item_names, star_block_item_data_table, global_koopa_shell_block_item_names, \
    koopa_shell_block_item_data_table, global_star_secret_item_names, star_secret_item_data_table, \
    global_jet_stream_item_names, jet_stream_item_data_table, global_cap_switch_item_names, \
    cap_switch_item_data_table, moat_exit_item_data_table, \
    rolling_log_item_data_table, purple_switch_item_data_table, optional_item_data_table, \
    simple_arbitrary_item_data_table, per_level_bobomb_buddy_item_names, per_level_treasure_chest_item_names, \
    per_level_warp_pipe_item_names, \
    bowser_stage_1up_item_data_table, randomized_action_item_names, main_course_move_area_names, \
    separate_misc_move_area_names, collapsed_misc_move_area_names, non_climb_move_area_names, ut_glitch_item_name, \
    item_name_groups, global_coin_object_item_data_table, per_level_coin_object_item_data_table, \
    global_enemy_item_data_table, per_level_enemy_item_data_table, global_mode_coin_object_item_names, \
    global_mode_enemy_item_names, bowser_bomb_item_data_table, special_level_unlock_item_names, \
    global_one_up_unlock_item_names, global_one_up_unlock_item_data_table, \
    per_level_one_up_unlock_item_data_table, global_sign_unlock_item_data_table, \
    per_level_sign_unlock_item_data_table, sign_unlock_item_names, progressive_filler_item_names
from .Locations import location_table, SM64Location, coin_count_check_course_data, get_coin_count_check_location_name, \
    get_coin_count_check_location_names, get_secret_stage_coin_count_check_location_names, \
    get_global_coin_count_check_location_names, get_global_coin_count_caps, location_name_groups
from .CoinChecks import CoinOutputID, coin_output_by_name, coin_output_region_name, select_individual_coin_outputs
from .Music import build_music_slot_data
from .Options import sm64_options_groups, SM64Options, coin_star_requirement_option_names, \
    move_randomizer_option_name_by_action, secret_stage_coin_count_max_coin_option_names, \
    trap_weight_option_names, trap_item_name_by_option_name
from .Rules import set_rules
from .Signs import fallback_hints, sign_data, sign_data_by_location_name
from .LogicTricks import get_enabled_logic_tricks, logic_tricks
from .Regions import create_regions, sm64_entrance_to_region, sm64_level_to_entrances, \
    sm64_level_to_paintings, sm64_level_to_secrets, SM64Levels, \
    sm64_shuffled_entrance_ids, sm64_entrance_source_descriptions, \
    sm64_entrance_destination_descriptions, sm64_entrance_source_names
from .SubAreas import CASTLE_RETURN_SOURCES, RETURN_SOURCES, SUB_AREA_SOURCES, \
    SUB_AREA_DESTINATION_DESCRIPTIONS, SUB_AREA_SOURCE_DESCRIPTIONS, SUB_AREA_SOURCE_NAMES, \
    sub_area_destination_name, sub_area_source_by_id
from BaseClasses import CollectionState, Entrance, Item, Region, Tutorial
from Options import OptionError
from ..AutoWorld import WebWorld, World


def _read_world_version() -> tuple[int, int, int]:
    manifest_data = pkgutil.get_data(__package__, "archipelago.json")
    if manifest_data is None:
        raise RuntimeError("Could not load the Spicy Mycena archipelago.json manifest")
    version_text = json.loads(manifest_data.decode("utf-8"))["world_version"]
    try:
        version = tuple(int(part) for part in version_text.split("."))
    except (AttributeError, ValueError) as error:
        raise RuntimeError(f"Invalid Spicy Mycena world_version: {version_text!r}") from error
    if len(version) != 3 or any(part < 0 for part in version):
        raise RuntimeError(f"Invalid Spicy Mycena world_version: {version_text!r}")
    return typing.cast(tuple[int, int, int], version)


SPICY_MYCENA_VERSION = _read_world_version()


class SM64Web(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up SM64EX for MultiWorld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["N00byKing", "Alchav"]
    )]

    option_groups = sm64_options_groups


class SM64World(World):
    """ 
    The first Super Mario game to feature 3D gameplay, it features freedom of movement within a large open world based on polygons,
    combined with traditional Mario gameplay, visual style, and characters.
    """

    game: str = "SM64: Spicy Mycena 64"
    origin_region_name = "Castle Grounds"
    topology_present = False

    web = SM64Web()

    item_name_to_id = item_table
    location_name_to_id = location_table
    item_name_groups = item_name_groups
    location_name_groups = location_name_groups

    required_client_version = (0, 3, 5)

    ut_can_gen_without_yaml = True
    glitches_item_name = ut_glitch_item_name
    found_entrances_datastorage_key = None
    permanent_coin_sources_datastorage_key = "SM64SpicyPermanentCoinSources_{player}"

    area_connections: dict[int | str, int | str]
    sub_area_slot_data: dict[int, int]

    options_dataclass = SM64Options
    options: SM64Options

    number_of_stars: int
    move_rando_bitvec: int
    filler_count: int

    @staticmethod
    def _clear_coin_evaluation_cache(state: CollectionState, player: int) -> None:
        cache = getattr(state, "sm64_coin_evaluation_cache", None)
        if cache is None:
            return
        for cache_key in tuple(cache):
            if cache_key[0] == player:
                del cache[cache_key]

    def collect(self, state: CollectionState, item: Item) -> bool:
        changed = super().collect(state, item)
        if changed:
            self._clear_coin_evaluation_cache(state, self.player)
        return changed

    def remove(self, state: CollectionState, item: Item) -> bool:
        changed = super().remove(state, item)
        if changed:
            self._clear_coin_evaluation_cache(state, self.player)
        return changed

    def reached_region(self, state: CollectionState, region: Region) -> None:
        super().reached_region(state, region)
        self._clear_coin_evaluation_cache(state, self.player)

    star_costs: typing.Dict[str, int]
    coin_count_check_location_names: typing.Tuple[str, ...]
    global_coin_count_check_location_names: typing.Tuple[str, ...]
    coin_check_location_names: typing.Tuple[str, ...]
    music_slot_data: typing.Dict[str, typing.Any] | None
    using_slot_coin_count_check_locations: bool
    start_inventory_item_ids: set[int]
    start_inventory_item_counts: dict[int, int]
    sign_hint_count: int
    sign_hints: dict[str, str]
    sign_hint_locations: dict[str, int]
    sign_hint_location_players: dict[str, int]
    sign_hint_entrances: dict[str, int]
    randomized_entrance_connections: dict[int, Entrance]
    deferred_entrance_targets: dict[int, Region]
    shuffled_entrance_source_ids: set[int]
    permanent_coin_source_counts: dict[str, int]

    slot_option_names = (
        "main_course_shuffle",
        "secret_course_shuffle",
        "sub_area_shuffle",
        "castle_return_shuffle",
        "buddy_checks",
        "one_up_checks",
        "blocksanity",
        "visit_checks",
        "easy_butterflies",
        "trigger_sparkles",
        "no_despawns",
        "combined_progressive_keys",
        "level_unlocks",
        "one_up_unlocks",
        "sign_unlocks",
        "triple_jump",
        "long_jump",
        "backflip",
        "side_flip",
        "wall_kick",
        "dive",
        "ground_pound",
        "kick",
        "climb",
        "ledge_grab",
        "combined_castle_and_secret_stage_move_items",
        "cap_items",
        "level_features",
        "bobomb_buddies",
        "bowser_bombs",
        "bowser_in_the_dark_world_health",
        "bowser_in_the_fire_sea_health",
        "bowser_in_the_sky_health",
        "bowser_in_the_sky_stage_collapse_hits",
        "bowser_stage_1ups",
        "logic_tricks",
        "universal_tracker_glitched_logic",
        "marios_hat",
        "mario_hat_color",
        "mario_shirt_color",
        "mario_overalls_color",
        "mario_gloves_color",
        "mario_shoes_color",
        "mario_skin_color",
        "mario_hair_color",
        "music_shuffle",
        "skybox_shuffle",
        "coin_checks",
        "coin_count_checks",
        "global_coin_count_checks",
        "counts_coins_beyond_coin_stars",
        *secret_stage_coin_count_max_coin_option_names,
        *coin_star_requirement_option_names,
        "traps_filler_percentage",
        *trap_weight_option_names,
        "death_link",
        "completion_type",
    )

    def generate_early(self):
        slot_data = self.get_re_gen_slot_data()
        self.area_connections = {}
        self.sub_area_slot_data = {}
        self.music_slot_data = None
        self.skybox_slot_data = None
        self.using_slot_coin_count_check_locations = False
        self.sign_hint_count = 0
        self.sign_hints = dict(slot_data.get("SignHints", {})) if slot_data else {}
        self.sign_hint_locations = dict(slot_data.get("SignHintLocations", {})) if slot_data else {}
        self.sign_hint_location_players = {
            key: int(value) for key, value in slot_data.get("SignHintLocationPlayers", {}).items()
        } if slot_data else {}
        self.sign_hint_entrances = {
            key: int(value) for key, value in slot_data.get("SignHintEntrances", {}).items()
        } if slot_data else {}
        self.randomized_entrance_connections = {}
        self.deferred_entrance_targets = {}
        self.bypass_entrance_connections = {}
        self.shuffled_entrance_source_ids = set()
        self.permanent_coin_source_counts = {}
        if slot_data:
            self.restore_options_from_slot_data(slot_data)
            self.area_connections = {
                int(source) if str(source).isdigit() else str(source): destination
                for source, destination in slot_data.get("AreaConnections", {}).items()
            }
            self.sub_area_slot_data = {
                int(source): int(destination)
                for source, destination in slot_data.get("SubAreaRando", {}).items()
            }
            self.music_slot_data = self.get_music_slot_data_from_slot_data(slot_data)
            self.skybox_slot_data = self.get_skybox_slot_data_from_slot_data(slot_data)
            self.start_inventory_item_counts = {
                int(item_id): int(count)
                for item_id, count in slot_data.get("StartInventory", {}).items()
            }
        else:
            self.start_inventory_item_counts = self.get_start_inventory_slot_data()

        enabled_logic_tricks = get_enabled_logic_tricks(self.options.logic_tricks.value)
        tracker_logic_tricks = get_enabled_logic_tricks(self.options.universal_tracker_glitched_logic.value)
        for trick, data in logic_tricks.items():
            setattr(self, data["internal_id"], trick in enabled_logic_tricks)
            setattr(self, f"{data['internal_id']}_ut_glitch", trick in tracker_logic_tricks)

        if slot_data and "CoinCheckLocations" in slot_data:
            unknown_coin_checks = set(slot_data["CoinCheckLocations"]) - coin_output_by_name.keys()
            if unknown_coin_checks:
                raise OptionError(
                    f"Unknown individual Coin Check locations in slot data: {sorted(unknown_coin_checks)}")
            self.coin_check_location_names = tuple(slot_data["CoinCheckLocations"])
        else:
            excluded_coin_outputs = set()
            if self.options.accessibility == self.options.accessibility.option_full:
                if not self.logic_sl_impossible_coin:
                    excluded_coin_outputs.add(CoinOutputID(
                        "Snowman's Land", "sl_impossible_coin", 1))
                if not self.logic_thi_impossible_coin:
                    excluded_coin_outputs.add(CoinOutputID(
                        "Tiny-Huge Island", "tiny_impossible_coin", 1))
            selected_coin_outputs = select_individual_coin_outputs(
                self.options.coin_checks.value,
                self.random,
                excluded_output_ids=frozenset(excluded_coin_outputs),
            )
            self.coin_check_location_names = tuple(
                output.location_name for output in selected_coin_outputs
            )
        tracker_datastorage_keys = []
        if self.get_shuffled_normal_entrance_ids():
            tracker_datastorage_keys.append("SM64SpicyFoundEntrances_{player}")
        if (
                self.options.sub_area_shuffle.value != self.options.sub_area_shuffle.option_vanilla
                or self.options.castle_return_shuffle.value
                == self.options.castle_return_shuffle.option_mixed
        ):
            tracker_datastorage_keys.extend((
                "SM64SpicyFoundSubAreaEntrancesLow_{player}",
                "SM64SpicyFoundSubAreaEntrancesHigh_{player}",
            ))
        tracker_datastorage_keys.append(self.permanent_coin_sources_datastorage_key)
        self.found_entrances_datastorage_key = tracker_datastorage_keys or None
        self.start_inventory_item_ids = set(self.start_inventory_item_counts)

        self.move_rando_bitvec = 0
        double_jump_bitvec_offset = action_item_data_table['Double Jump'].code
        for action in randomized_action_item_names:
            option = getattr(self.options, move_randomizer_option_name_by_action[action])
            if option.value != option.option_not_shuffled:
                self.move_rando_bitvec |= (1 << (action_item_data_table[action].code - double_jump_bitvec_offset))

        self.filler_count = 0
        self.topology_present = bool(
            self.options.main_course_shuffle or self.options.secret_course_shuffle
            or self.options.sub_area_shuffle or self.options.castle_return_shuffle)
        if (
                self.options.accessibility == self.options.accessibility.option_full
                and not self.logic_sl_impossible_coin
        ):
            self.options.snowmans_land_coin_star_requirement.value = min(
                self.options.snowmans_land_coin_star_requirement.value, 126)

        if (
                self.options.accessibility == self.options.accessibility.option_full
                and not self.logic_thi_impossible_coin
        ):
            self.options.tiny_huge_island_coin_star_requirement.value = min(
                self.options.tiny_huge_island_coin_star_requirement.value, 191)
        coin_star_requirements = {
            option_name: getattr(self.options, option_name).value
            for option_name in coin_star_requirement_option_names
        }
        if "CoinCountCheckLocations" in slot_data:
            self.coin_count_check_location_names = tuple(slot_data["CoinCountCheckLocations"])
            self.using_slot_coin_count_check_locations = True
        else:
            self.coin_count_check_location_names = get_coin_count_check_location_names(
                coin_star_requirements, self.options.coin_count_checks.value)
            secret_stage_coin_maxes = {
                option_name: getattr(self.options, option_name).value
                for option_name in secret_stage_coin_count_max_coin_option_names
            }
            self.coin_count_check_location_names += get_secret_stage_coin_count_check_location_names(
                secret_stage_coin_maxes, self.options.coin_count_checks.value)
        if "GlobalCoinCountCheckLocations" in slot_data:
            self.global_coin_count_check_location_names = tuple(slot_data["GlobalCoinCountCheckLocations"])
        else:
            self.global_coin_count_check_location_names = get_global_coin_count_check_location_names(
                sum(self.get_global_coin_count_caps()),
                self.options.global_coin_count_checks.value,
            )
        if "MoveRandoVec" in slot_data:
            self.move_rando_bitvec = slot_data["MoveRandoVec"]

    def get_shuffled_normal_entrance_ids(self) -> set[int]:
        entrance_ids = set()
        if self.options.main_course_shuffle.value != self.options.main_course_shuffle.option_vanilla:
            entrance_ids.update(int(entrance_id) for entrance_id in sm64_level_to_paintings)
        if self.options.secret_course_shuffle.value != self.options.secret_course_shuffle.option_vanilla:
            entrance_ids.update(int(entrance_id) for entrance_id in sm64_level_to_secrets)
        return entrance_ids

    def get_shuffled_entrance_source_ids(self) -> set[int]:
        source_ids = self.get_shuffled_normal_entrance_ids()
        sub_area_mode = self.options.sub_area_shuffle.value
        if sub_area_mode != self.options.sub_area_shuffle.option_vanilla:
            source_ids.update(
                source.source_id for source in (*SUB_AREA_SOURCES.values(), *RETURN_SOURCES.values()))
        if self.options.castle_return_shuffle.value == self.options.castle_return_shuffle.option_mixed:
            source_ids.update(source.source_id for source in CASTLE_RETURN_SOURCES.values())
        return source_ids

    def get_entrance_hint_text(self, source_id: int) -> str:
        physical_source = sub_area_source_by_id(source_id)
        if physical_source is not None:
            destination_key = self.area_connections[physical_source.key]
            return (
                f"{self.get_entrance_destination_description(destination_key)} is at "
                f"{SUB_AREA_SOURCE_DESCRIPTIONS[physical_source.key]}."
            )

        source_name = sm64_level_to_entrances.get(source_id)
        if source_id == int(SM64Levels.BOWSER_IN_THE_SKY):
            source_name = "Bowser in the Sky"
        if source_name is None:
            raise KeyError(source_id)

        destination_key = self.area_connections[source_id]
        return (
            f"{self.get_entrance_destination_description(destination_key)} is at "
            f"{sm64_entrance_source_descriptions[source_id]}."
        )

    @staticmethod
    def get_entrance_destination_description(destination: int | str) -> str:
        if isinstance(destination, int):
            return sm64_entrance_destination_descriptions[destination]
        return SUB_AREA_DESTINATION_DESCRIPTIONS[destination]

    @staticmethod
    def get_entrance_destination_name(destination: int | str) -> str:
        if isinstance(destination, int):
            return sm64_entrance_destination_descriptions[destination]
        return sub_area_destination_name(destination)

    @staticmethod
    def get_normal_entrance_name(entrance_id: int) -> str:
        if entrance_id == int(SM64Levels.BOWSER_IN_THE_SKY):
            return "Bowser in the Sky"
        return sm64_level_to_entrances[entrance_id]

    @classmethod
    def get_normal_entrance_source_name(cls, entrance_id: int) -> str:
        if entrance_id == int(SM64Levels.BOWSER_IN_THE_SKY):
            return "Bowser in the Sky"
        source_name = sm64_entrance_source_names.get(entrance_id)
        if source_name is not None:
            return source_name
        return f"{cls.get_normal_entrance_name(entrance_id)} Entrance"

    @classmethod
    def get_connection_source_name(cls, source: int | str) -> str:
        if isinstance(source, int):
            return cls.get_normal_entrance_source_name(source)
        return SUB_AREA_SOURCE_NAMES[source]

    def explain_rule(self, name: str, state: CollectionState):
        def destination_region_name(destination: int | str) -> str:
            if isinstance(destination, int):
                entrance_name = self.get_normal_entrance_name(destination)
                return sm64_entrance_to_region.get(entrance_name, entrance_name)
            return sub_area_destination_name(destination)

        def destination_course_name(destination: int | str) -> str:
            region_name = destination_region_name(destination)
            for course_name in ("Wet-Dry World", "Tick Tock Clock", "Tiny-Huge Island"):
                if region_name.startswith(course_name):
                    return course_name
            return region_name.split(" - ", 1)[0]

        connections = list(self.area_connections.items())
        configured_sources = {source for source, _destination in connections}
        for source in (*SUB_AREA_SOURCES.values(), *RETURN_SOURCES.values()):
            if source.key not in configured_sources:
                connections.append((source.key, source.vanilla_destination))
        if self.options.castle_return_shuffle.value == self.options.castle_return_shuffle.option_mixed:
            for source in CASTLE_RETURN_SOURCES.values():
                if source.key not in configured_sources:
                    connections.append((source.key, source.vanilla_destination))

        requested_name = name.casefold()
        course_connections = [
            (source, destination) for source, destination in connections
            if destination_course_name(destination).casefold() == requested_name
        ]
        if not course_connections:
            return None

        course_name = destination_course_name(course_connections[0][1])
        messages = [{"type": "text", "text": f"{course_name} entrances:"}]
        course_connections.sort(key=lambda connection: (
            not isinstance(connection[1], int),
            self.get_entrance_destination_description(connection[1]),
        ))
        for source_id, destination_id in course_connections:
            destination_name = self.get_entrance_destination_description(destination_id)
            if isinstance(source_id, str):
                physical_source = next(
                    table[source_id] for table in (SUB_AREA_SOURCES, RETURN_SOURCES, CASTLE_RETURN_SOURCES)
                    if source_id in table
                )
                connection_id = physical_source.source_id
            else:
                physical_source = sub_area_source_by_id(source_id)
                connection_id = source_id

            entrance = self.randomized_entrance_connections.get(connection_id)
            if entrance is None and physical_source is not None:
                entrance = self.multiworld.get_entrance(SUB_AREA_SOURCE_NAMES[physical_source.key], self.player)
            if entrance is None or entrance.connected_region is None:
                messages.append({
                    "type": "text",
                    "text": f"\n{destination_name}: entrance not discovered.",
                })
                continue

            if physical_source is not None:
                source_name = SUB_AREA_SOURCE_DESCRIPTIONS[physical_source.key]
            else:
                source_name = sm64_entrance_source_descriptions[source_id]

            reachable = entrance.can_reach(state)
            messages.extend(({
                "type": "text",
                "text": f"\n{destination_name} is at {source_name}: ",
            }, {
                "type": "color",
                "color": "green" if reachable else "salmon",
                "text": "reachable" if reachable else "not reachable",
            }))
            if hasattr(entrance.access_rule, "explain_json"):
                explanation = entrance.access_rule.explain_json(state)
                plain_text = "".join(part.get("text", "") for part in explanation).strip()
                if plain_text not in {"", "True", "False"}:
                    messages.append({"type": "text", "text": "\n  Requirements: "})
                    messages.extend(explanation)

        return messages

    def create_regions(self):
        create_regions(self.multiworld, self.options, self.player)
        if not self.using_slot_coin_count_check_locations:
            self.add_overflow_coin_count_check_locations()
        coin_check_region_names = {
            "Jolly Roger Bay": "Jolly Roger Bay - Coins",
            "Cool, Cool Mountain": "Cool, Cool Mountain - Coins",
            "Lethal Lava Land": "Lethal Lava Land - Coins",
            "Shifting Sand Land": "Shifting Sand Land - Coins",
            "Snowman's Land": "Snowman's Land - Coins",
            "Tall, Tall Mountain": "Tall, Tall Mountain - Coins",
            "Tiny-Huge Island": "Tiny-Huge Island - Coins",
        }
        coin_check_source_region_names = {
            ("Castle", "castle_grounds_bridge_coins"): "Castle Grounds",
            ("Castle", "castle_lobby_coins"): "Castle First Floor",
            ("Castle", "castle_courtyard_boos"): "Castle Courtyard",
        }
        for location_name in self.coin_count_check_location_names:
            region_name = location_name.rsplit(" - ", 1)[0]
            region_name = coin_check_region_names.get(region_name, region_name)
            region = self.multiworld.get_region(region_name, self.player)
            region.locations.append(SM64Location(self.player, location_name, location_table[location_name], region))
        global_coin_count_region = self.multiworld.get_region(self.origin_region_name, self.player)
        for location_name in self.global_coin_count_check_location_names:
            global_coin_count_region.locations.append(SM64Location(
                self.player, location_name, location_table[location_name], global_coin_count_region))
        for location_name in self.coin_check_location_names:
            output = coin_output_by_name[location_name]
            output_id = output.output_id
            region_name = coin_output_region_name(output) or coin_check_source_region_names.get(
                (output_id.course_name, output_id.source_id),
                output_id.course_name,
            )
            region = self.multiworld.get_region(region_name, self.player)
            region.locations.append(SM64Location(
                self.player, location_name, output.location_id, region))

    def set_rules(self):
        set_rules(self.multiworld, self.options, self.player, self.area_connections, self.move_rando_bitvec)
        if self.topology_present:
            for source_id in self.shuffled_entrance_source_ids:
                physical_source = sub_area_source_by_id(source_id)
                source = physical_source.key if physical_source else source_id
                destination = self.area_connections[source]
                self.multiworld.spoiler.set_entrance(
                    SUB_AREA_SOURCE_NAMES[source] if physical_source else
                    self.get_normal_entrance_source_name(source_id),
                    self.get_entrance_destination_name(destination),
                    'entrance', self.player)

    @classmethod
    def stage_set_rules(cls, multiworld) -> None:
        for world in multiworld.worlds.values():
            if isinstance(world, cls):
                world.configure_full_level_unlock_early_items()

    def configure_full_level_unlock_early_items(self) -> None:
        if self.options.level_unlocks.value != self.options.level_unlocks.option_full:
            return

        unlock_name_by_entrance_name = {
            "Wet-Dry World Low": "Unlock Wet-Dry World",
            "Wet-Dry World Middle": "Unlock Wet-Dry World",
            "Wet-Dry World High": "Unlock Wet-Dry World",
            "Tick Tock Clock Stopped Entrance": "Unlock Tick Tock Clock",
            "Tick Tock Clock Slow": "Unlock Tick Tock Clock",
            "Tick Tock Clock Random": "Unlock Tick Tock Clock",
            "Tick Tock Clock Fast": "Unlock Tick Tock Clock",
            "Tiny-Huge Island (Tiny)": "Unlock Tiny Island",
            "Tiny-Huge Island (Huge)": "Unlock Huge Island",
        }
        available_unlocks = set(self.get_level_unlock_item_names())
        state = CollectionState(self.multiworld)
        state.reachable_regions[self.player].add(
            self.multiworld.get_region(self.origin_region_name, self.player))
        state.update_reachable_regions(self.player)

        candidates = []
        for entrance_id, entrance in self.randomized_entrance_connections.items():
            entrance_name = sm64_level_to_entrances.get(entrance_id)
            if entrance_name is None or not entrance.parent_region.can_reach(state):
                continue
            item_name = unlock_name_by_entrance_name.get(entrance_name, f"Unlock {entrance_name}")
            if item_name in available_unlocks:
                candidates.append(item_name)

        candidates = list(dict.fromkeys(candidates))
        if not candidates:
            raise OptionError("Full Level Unlocks has no sphere-one entrance unlock candidates.")
        self.random.shuffle(candidates)
        self.multiworld.local_early_items[self.player][candidates[0]] = 1
        sphere_one_state = CollectionState(self.multiworld)
        sphere_one_location_count = sum(
            location.address is not None and location.can_reach(sphere_one_state)
            for location in self.multiworld.get_locations(self.player)
        )
        if sphere_one_location_count > 2 and len(candidates) > 1:
            self.multiworld.early_items[self.player][candidates[1]] = 1

    def create_item(self, name: str) -> Item:
        data = item_data_table[name]
        item = SM64Item(name, self.get_item_classification(data), data.code, self.player)

        return item

    def get_item_classification(self, item_data):
        if callable(item_data.classification):
            return item_data.classification(self.options)
        return item_data.classification

    def create_event_item(self, name: str) -> Item:
        data = item_data_table[name]
        return SM64Item(name, self.get_item_classification(data), None, self.player)

    def get_castle_key_item_names(self) -> typing.List[str]:
        if self.options.combined_progressive_keys:
            return ["Progressive Key"] * 6
        return ["Dark World Key"] + ["Progressive Basement Key"] * 2 + ["Progressive Upstairs Key"] * 3

    def get_cap_item_names(self) -> typing.List[str]:
        option = self.options.cap_items
        if option.value == option.option_per_level:
            return list(cap_item_data_table)
        if option.value == option.option_both:
            return list(global_cap_item_names) + list(cap_item_data_table)
        return list(global_cap_item_names)

    def get_level_feature_item_names(self) -> typing.List[str]:
        item_names = []
        mode = self.options.level_features.value
        if mode != self.options.level_features.option_not_shuffled:
            item_names += [
                name for name in feature_item_data_table
                if name not in per_level_bobomb_buddy_item_names
                and not (mode != self.options.level_features.option_per_act_only and name in {
                    "Lethal Lava Land - Koopa Shell", "Jolly Roger Bay - Jet Stream"})
            ]
        if mode in {
                self.options.level_features.option_global,
                self.options.level_features.option_per_level,
                self.options.level_features.option_both,
        }:
            item_names += [
                name for name in simple_arbitrary_item_data_table
                if name not in per_level_bobomb_buddy_item_names
                and name not in per_level_treasure_chest_item_names
            ]
            item_names += self.get_unlock_item_names(
                self.options.level_features, global_checkerboard_item_names, checkerboard_item_data_table)
            item_names += self.get_unlock_item_names(
                self.options.level_features, global_rolling_log_item_names, rolling_log_item_data_table)
            item_names += self.get_unlock_item_names(
                self.options.level_features, global_purple_switch_item_names, purple_switch_item_data_table)
            item_names += self.get_unlock_item_names(
                self.options.level_features,
                global_treasure_chest_item_names,
                per_level_treasure_chest_item_names)
            item_names += self.get_unlock_item_names(
                self.options.level_features,
                global_warp_pipe_item_names,
                per_level_warp_pipe_item_names)
            item_names += self.get_unlock_item_names(
                self.options.level_features,
                global_vertical_wind_item_names,
                vertical_wind_item_data_table)
            item_names += self.get_unlock_item_names(
                self.options.level_features,
                global_horizontal_wind_item_names,
                horizontal_wind_item_data_table)
            item_names += self.get_unlock_item_names(
                self.options.level_features,
                global_freestanding_star_item_names,
                freestanding_star_item_data_table)
            item_names += self.get_unlock_item_names(
                self.options.level_features,
                global_star_block_item_names,
                star_block_item_data_table)
            item_names += self.get_unlock_item_names(
                self.options.level_features,
                global_koopa_shell_block_item_names,
                koopa_shell_block_item_data_table)
            item_names += self.get_unlock_item_names(
                self.options.level_features,
                global_star_secret_item_names,
                star_secret_item_data_table)
            item_names += self.get_unlock_item_names(
                self.options.level_features,
                global_jet_stream_item_names,
                jet_stream_item_data_table)
            item_names += self.get_unlock_item_names(
                self.options.level_features,
                global_cap_switch_item_names,
                cap_switch_item_data_table)

        buddy_mode = self.options.bobomb_buddies.value
        if buddy_mode == self.options.bobomb_buddies.option_per_act_only:
            item_names += [
                name for name in feature_item_data_table
                if name in per_level_bobomb_buddy_item_names
            ]
        elif buddy_mode == self.options.bobomb_buddies.option_global:
            item_names += list(global_bobomb_buddy_item_names)
        elif buddy_mode == self.options.bobomb_buddies.option_per_level:
            item_names += list(per_level_bobomb_buddy_item_names)
        elif buddy_mode == self.options.bobomb_buddies.option_both:
            item_names += list(global_bobomb_buddy_item_names)
            item_names += list(per_level_bobomb_buddy_item_names)
        return item_names

    def get_unrandomized_level_feature_item_names(self) -> typing.List[str]:
        item_names = []
        mode = self.options.level_features.value
        if mode == self.options.level_features.option_not_shuffled:
            item_names += [
                name for name in feature_item_data_table
                if name not in per_level_bobomb_buddy_item_names
            ]
        if mode in {
                self.options.level_features.option_not_shuffled,
                self.options.level_features.option_per_act_only,
        }:
            item_names += [
                name for name in simple_arbitrary_item_data_table
                if name not in per_level_bobomb_buddy_item_names
                and name not in per_level_treasure_chest_item_names
            ]
            item_names += list(global_checkerboard_item_names)
            item_names += list(global_rolling_log_item_names)
            item_names += list(global_purple_switch_item_names)
            item_names += list(global_treasure_chest_item_names)
            item_names += list(global_warp_pipe_item_names)
            item_names += list(global_vertical_wind_item_names)
            item_names += list(global_horizontal_wind_item_names)
            item_names += list(global_freestanding_star_item_names)
            item_names += list(global_star_block_item_names)
            if mode == self.options.level_features.option_not_shuffled:
                item_names += list(global_koopa_shell_block_item_names)
            item_names += list(global_star_secret_item_names)
            if mode == self.options.level_features.option_not_shuffled:
                item_names += list(global_jet_stream_item_names)
            else:
                item_names += [
                    name for name in (*koopa_shell_block_item_data_table, *jet_stream_item_data_table)
                    if name not in {"Lethal Lava Land - Koopa Shell", "Jolly Roger Bay - Jet Stream"}
                ]
            item_names += list(global_cap_switch_item_names)

        buddy_mode = self.options.bobomb_buddies.value
        if buddy_mode == self.options.bobomb_buddies.option_not_shuffled:
            item_names += list(global_bobomb_buddy_item_names)
        elif buddy_mode == self.options.bobomb_buddies.option_per_act_only:
            item_names += [
                name for name in per_level_bobomb_buddy_item_names
                if name not in feature_item_data_table
            ]
        return item_names

    def get_optional_item_names(self) -> typing.List[str]:
        if self.options.marios_hat:
            return list(optional_item_data_table)
        return []

    def get_unrandomized_optional_item_names(self) -> typing.List[str]:
        if self.options.marios_hat:
            return []
        return list(optional_item_data_table)

    @staticmethod
    def get_unlock_item_names(option, global_mode_item_names, per_level_item_data_table) -> typing.List[str]:
        if option.value == option.option_global:
            return list(global_mode_item_names)
        if option.value == option.option_per_level:
            return list(per_level_item_data_table)
        if option.value == option.option_both:
            return list(dict.fromkeys((*global_mode_item_names, *per_level_item_data_table)))
        return []

    def get_coin_object_unlock_item_names(self) -> typing.List[str]:
        return self.get_unlock_item_names(
            self.options.coin_object_unlocks,
            global_mode_coin_object_item_names,
            per_level_coin_object_item_data_table)

    def get_enemy_unlock_item_names(self) -> typing.List[str]:
        item_names = self.get_unlock_item_names(
            self.options.enemy_unlocks,
            global_mode_enemy_item_names,
            per_level_enemy_item_data_table)
        if self.options.one_up_unlocks.value == self.options.one_up_unlocks.option_not_shuffled:
            item_names += self.get_unlock_item_names(
                self.options.enemy_unlocks,
                ("Monty Moles",),
                ("Hazy Maze Cave - Monty Moles", "Tall, Tall Mountain - Monty Moles"))
        return item_names

    def get_one_up_unlock_item_names(self) -> typing.List[str]:
        item_names = self.get_unlock_item_names(
            self.options.one_up_unlocks,
            global_one_up_unlock_item_names,
            per_level_one_up_unlock_item_data_table)
        if self.options.one_up_unlocks.value == self.options.one_up_unlocks.option_not_shuffled:
            return []
        if self.options.one_up_checks:
            return item_names
        return [item_name for item_name in item_names if item_name.endswith("Monty Moles")]

    def get_sign_unlock_item_names(self) -> typing.List[str]:
        return self.get_unlock_item_names(
            self.options.sign_unlocks,
            global_sign_unlock_item_data_table,
            per_level_sign_unlock_item_data_table)

    def get_level_unlock_item_names(self) -> typing.List[str]:
        option = self.options.level_unlocks
        if option.value == option.option_disabled:
            return []

        item_names = list(special_level_unlock_item_names)
        if option.value == option.option_full:
            item_names += list(painting_unlock_item_data_table)
        return item_names

    def get_bowser_arena_bomb_item_names(self) -> typing.List[str]:
        option = self.options.bowser_bombs
        item_names = []
        if option.value in {option.option_global, option.option_both}:
            item_names += [
                "Bowser Arena Bomb 1",
                "Bowser Arena Bomb 2",
                "Bowser Arena Bomb 3",
                "Bowser Arena Bomb 4",
                "Bowser in the Sky - Bowser Arena Bomb 5",
            ]
        if option.value in {option.option_per_level, option.option_both}:
            item_names += (
                [f"Bowser in the Dark World - Bowser Arena Bomb {index}" for index in range(1, 5)]
                + [f"Bowser in the Fire Sea - Bowser Arena Bomb {index}" for index in range(1, 5)]
                + [f"Bowser in the Sky - Bowser Arena Bomb {index}" for index in range(1, 6)]
            )
        return list(dict.fromkeys(item_names))

    def get_unrandomized_bowser_arena_bomb_item_names(self) -> typing.List[str]:
        if self.options.bowser_bombs.value == self.options.bowser_bombs.option_not_shuffled:
            return [
                "Bowser Arena Bomb 1",
                "Bowser Arena Bomb 2",
                "Bowser Arena Bomb 3",
                "Bowser Arena Bomb 4",
                "Bowser in the Sky - Bowser Arena Bomb 5",
            ]
        return []

    def get_unrandomized_unlock_item_names(self) -> typing.List[str]:
        item_names = []
        if self.options.coin_object_unlocks.value == self.options.coin_object_unlocks.option_not_shuffled:
            item_names += list(global_coin_object_item_data_table)
            item_names += list(per_level_coin_object_item_data_table)
        if self.options.enemy_unlocks.value == self.options.enemy_unlocks.option_not_shuffled:
            item_names += list(global_enemy_item_data_table)
            item_names += list(per_level_enemy_item_data_table)
        if self.options.one_up_unlocks.value == \
                self.options.one_up_unlocks.option_not_shuffled:
            item_names += list(global_one_up_unlock_item_data_table)
            item_names += list(per_level_one_up_unlock_item_data_table)
        if (self.options.enemy_unlocks.value != self.options.enemy_unlocks.option_not_shuffled
                or self.options.one_up_unlocks.value != self.options.one_up_unlocks.option_not_shuffled):
            item_names = [name for name in item_names if not name.endswith("Monty Moles")]
        if self.options.sign_unlocks.value == self.options.sign_unlocks.option_not_shuffled:
            item_names += list(global_sign_unlock_item_data_table)
            item_names += list(per_level_sign_unlock_item_data_table)
        if self.options.level_unlocks.value != self.options.level_unlocks.option_full:
            item_names += list(painting_unlock_item_data_table)
        if self.options.level_unlocks.value == self.options.level_unlocks.option_disabled:
            item_names += list(special_level_unlock_item_names)
        return list(dict.fromkeys(item_names))

    def get_bowser_stage_1up_item_names(self) -> typing.List[str]:
        option = self.options.bowser_stage_1ups
        item_names = []
        if option.value in {option.option_global, option.option_both}:
            item_names.append("Bowser Stage Extra 1-Ups")
        if option.value in {option.option_per_level, option.option_both}:
            item_names += [
                "Bowser in the Dark World - Extra 1-Ups",
                "Bowser in the Fire Sea - Extra 1-Ups",
            ]
        return item_names

    def get_unrandomized_bowser_stage_1up_item_names(self) -> typing.List[str]:
        if self.options.bowser_stage_1ups.value == self.options.bowser_stage_1ups.option_always_spawn:
            return ["Bowser Stage Extra 1-Ups"]
        return []

    def get_action_item_names(self) -> typing.List[str]:
        item_names = []
        per_level_area_names = (
            main_course_move_area_names
            + (collapsed_misc_move_area_names
               if self.options.combined_castle_and_secret_stage_move_items else separate_misc_move_area_names)
        )
        for action in randomized_action_item_names:
            option = getattr(self.options, move_randomizer_option_name_by_action[action])
            if option.value == option.option_global:
                item_names.append(action)
            elif option.value == option.option_per_level:
                item_names += [
                    f"{area_name} - {action}" for area_name in per_level_area_names
                    if not (area_name in non_climb_move_area_names and action == "Climb")
                ]
            elif option.value == option.option_both:
                item_names.append(action)
                item_names += [
                    f"{area_name} - {action}" for area_name in per_level_area_names
                    if not (area_name in non_climb_move_area_names and action == "Climb")
                ]
        return item_names

    def get_progression_item_names(self) -> typing.List[str]:
        item_names = self.get_level_feature_item_names()
        item_names += self.get_castle_key_item_names()
        item_names += ["Castle - Progressive MIPS"] * 2
        item_names += [
            item_name for item_name in castle_progression_item_data_table
            if item_name != "Castle - Progressive MIPS"
            and item_name not in special_level_unlock_item_names
        ]
        item_names += self.get_level_unlock_item_names()
        item_names += self.get_cap_item_names()
        item_names += self.get_bowser_stage_1up_item_names()

        if self.options.buddy_checks:
            item_names += list(cannon_item_data_table)

        item_names += self.get_action_item_names()
        item_names += self.get_coin_object_unlock_item_names()
        item_names += self.get_enemy_unlock_item_names()
        item_names += self.get_one_up_unlock_item_names()
        item_names += self.get_sign_unlock_item_names()
        item_names += self.get_bowser_arena_bomb_item_names()
        item_names += list(moat_exit_item_data_table)

        return item_names

    def get_item_pool_item_count(self) -> int:
        return len(self.get_progression_item_names()) + len(self.get_optional_item_names())

    def get_coin_star_requirements_by_option(self) -> typing.Dict[str, int]:
        return {
            option_name: getattr(self.options, option_name).value
            for option_name in coin_star_requirement_option_names
        }

    def get_global_coin_count_caps(self) -> tuple[int, ...]:
        reachable_coin_maxima = {}
        if self.options.accessibility == self.options.accessibility.option_full:
            if not self.logic_sl_impossible_coin:
                reachable_coin_maxima["Snowman's Land"] = 126
            if not self.logic_thi_impossible_coin:
                reachable_coin_maxima["Tiny-Huge Island"] = 191
        return get_global_coin_count_caps(
            self.get_coin_star_requirements_by_option(),
            {
                option_name: getattr(self.options, option_name).value
                for option_name in secret_stage_coin_count_max_coin_option_names
            },
            bool(self.options.counts_coins_beyond_coin_stars),
            reachable_coin_maxima,
        )

    def add_overflow_coin_count_check_locations(self) -> None:
        item_count = self.get_item_pool_item_count()
        fillable_location_count = (
            len(self.multiworld.get_unfilled_locations(self.player))
            + len(self.coin_count_check_location_names)
            + len(self.global_coin_count_check_location_names)
            + len(self.coin_check_location_names)
            - self.get_future_locked_location_count()
        )
        extra_location_count = item_count - fillable_location_count
        if extra_location_count <= 0:
            return

        coin_star_requirements = self.get_coin_star_requirements_by_option()
        selected_locations = set(self.coin_count_check_location_names)
        extra_locations: list[str] = []

        below_threshold_pool = [
            get_coin_count_check_location_name(course_name, coin_count)
            for course_name, _course_offset, option_name, _max_coins in coin_count_check_course_data
            for coin_count in range(1, coin_star_requirements[option_name])
            if get_coin_count_check_location_name(course_name, coin_count) not in selected_locations
        ]
        self.random.shuffle(below_threshold_pool)
        for location_name in below_threshold_pool[:extra_location_count]:
            selected_locations.add(location_name)
            extra_locations.append(location_name)

        remaining_location_count = extra_location_count - len(extra_locations)
        coin_offset = 0
        while remaining_location_count > 0:
            added_this_round = False
            for course_name, _course_offset, option_name, max_coin_star_requirement in coin_count_check_course_data:
                coin_count = coin_star_requirements[option_name] + coin_offset
                if coin_count >= max_coin_star_requirement:
                    continue
                location_name = get_coin_count_check_location_name(course_name, coin_count)
                if location_name in selected_locations:
                    continue
                selected_locations.add(location_name)
                extra_locations.append(location_name)
                remaining_location_count -= 1
                added_this_round = True
                if remaining_location_count <= 0:
                    break
            if not added_this_round:
                break
            coin_offset += 1

        self.coin_count_check_location_names = (*self.coin_count_check_location_names, *extra_locations)

    def get_future_locked_location_count(self) -> int:
        locked_count = 0
        if not self.options.buddy_checks:
            locked_count += len(cannon_item_data_table)
        return locked_count
        
    def get_filler_replacements(self, filler_count: int) -> typing.List[str]:
        replacement_names: typing.List[str] = []

        trap_items = []
        trap_weights = []
        for option_name in trap_weight_option_names:
            weight = getattr(self.options, option_name).value
            if weight > 0:
                trap_items.append(trap_item_name_by_option_name[option_name])
                trap_weights.append(weight)

        trap_count = (filler_count * self.options.traps_filler_percentage.value) // 100
        if trap_items: replacement_names.extend(self.random.choices(trap_items, weights=trap_weights, k=trap_count,))
        self.random.shuffle(replacement_names)
        return replacement_names

    def create_items(self):
        item_names = self.get_progression_item_names()
        item_names += self.get_optional_item_names()
        fillable_location_count = len(self.multiworld.get_unfilled_locations(self.player)) - self.get_future_locked_location_count()
        self.filler_count = fillable_location_count - len(item_names)
        if self.filler_count < 0:
            raise OptionError(f"{self.player_name}'s Spicy Mycena 64 world has {abs(self.filler_count)} more "
                              f"required items than randomized locations.")

        replacement_item_names = self.get_filler_replacements(self.filler_count)
        plain_filler_count = self.filler_count - len(replacement_item_names)
        filler_item_names = [
            progressive_filler_item_names[index % len(progressive_filler_item_names)]
            for index in range(plain_filler_count)
        ]
        self.random.shuffle(filler_item_names)
        self.multiworld.itempool += [self.create_item(item_name) for item_name in item_names]
        self.multiworld.itempool += [self.create_item(item_name) for item_name in replacement_item_names]
        self.multiworld.itempool += [self.create_item(item_name) for item_name in filler_item_names]
        advancement_count = sum(
            item.advancement for item in self.multiworld.itempool
            if item.player == self.player and item.name not in sign_unlock_item_names
        )
        entrance_count = len(self.get_shuffled_entrance_source_ids())
        self.sign_hint_count = min(len(sign_data) - 1, (advancement_count + entrance_count) // 5)

    @classmethod
    def stage_pre_output(cls, multiworld):
        worlds = [world for world in multiworld.worlds.values() if isinstance(world, cls)]
        if not worlds:
            return

        state = CollectionState(multiworld)
        remaining_locations = set(multiworld.get_filled_locations())
        remaining_entrances = {
            entrance
            for world in worlds
            for entrance_id in world.get_shuffled_entrance_source_ids()
            if (entrance := world.randomized_entrance_connections.get(entrance_id)) is not None
        }
        spheres = []
        entrance_spheres = []
        while remaining_locations:
            sphere = {
                location for location in remaining_locations
                if location.can_reach(state)
            }
            if not sphere:
                break
            entrance_sphere = {
                entrance for entrance in remaining_entrances
                if entrance.can_reach(state)
            }
            spheres.append(sorted(sphere))
            entrance_spheres.append(entrance_sphere)
            remaining_entrances -= entrance_sphere
            for location in sphere:
                state.collect(location.item, True, location)
            remaining_locations -= sphere

        for world in worlds:
            if world.sign_hints:
                continue

            shuffled_fallback_hints = list(fallback_hints)
            world.random.shuffle(shuffled_fallback_hints)
            world.sign_hints = {
                sign.key: shuffled_fallback_hints[index]
                for index, sign in enumerate(sign_data)
            }
            world.sign_hint_locations = {sign.key: 0 for sign in sign_data}
            world.sign_hint_location_players = {sign.key: 0 for sign in sign_data}
            world.sign_hint_entrances = {sign.key: 0 for sign in sign_data}

            signs_by_sphere: list[list] = [[] for _sphere in spheres]
            candidates_by_sphere: list[list[tuple[str, object]]] = [[] for _sphere in spheres]
            for sphere_index, sphere in enumerate(spheres):
                for location in sphere:
                    if location.player == world.player and location.name in sign_data_by_location_name:
                        signs_by_sphere[sphere_index].append(location)
                    elif (
                            location.item is not None
                            and location.item.player == world.player
                            and location.item.advancement
                            and location.item.name not in sign_unlock_item_names
                            and location.item.code is not None
                            and location.address is not None
                    ):
                        candidates_by_sphere[sphere_index].append(("item", location))

                for entrance in entrance_spheres[sphere_index]:
                    if entrance.player != world.player:
                        continue
                    source_id = next(
                        entrance_id for entrance_id, connection
                        in world.randomized_entrance_connections.items()
                        if connection is entrance
                    )
                    candidates_by_sphere[sphere_index].append(("entrance", source_id))

            for locations in signs_by_sphere:
                world.random.shuffle(locations)
            for candidates in candidates_by_sphere:
                world.random.shuffle(candidates)

            sign_entries = [
                (sphere_index, sign_location)
                for sphere_index, sign_locations in enumerate(signs_by_sphere)
                for sign_location in sign_locations
            ]
            target_hint_count = min(world.sign_hint_count, len(sign_entries), len(sign_data) - 1)
            sign_buckets = [
                sign_entries[
                    bucket_index * len(sign_entries) // target_hint_count:
                    (bucket_index + 1) * len(sign_entries) // target_hint_count
                ]
                for bucket_index in range(target_hint_count)
            ] if target_hint_count else []
            for bucket in sign_buckets:
                world.random.shuffle(bucket)

            selected_signs = set()
            assignments = []

            def take_candidate(sign_sphere_index):
                for candidate_sphere_index in range(sign_sphere_index, len(candidates_by_sphere)):
                    if candidates_by_sphere[candidate_sphere_index]:
                        return candidates_by_sphere[candidate_sphere_index].pop()
                return None

            # Work backward so late signs get first claim on the candidates that can validly hint them.
            for bucket_index in reversed(range(target_hint_count)):
                eligible_signs = sign_buckets[bucket_index]
                if not eligible_signs:
                    continue
                assignment = None
                for sign_sphere_index, sign_location in eligible_signs:
                    if sign_location in selected_signs:
                        continue
                    candidate = take_candidate(sign_sphere_index)
                    if candidate is not None:
                        assignment = (sign_location, candidate)
                        break
                if assignment is None:
                    # If this portion of the playthrough has no later candidate, move its hint earlier.
                    for sign_sphere_index, sign_location in reversed(sign_entries):
                        if sign_location in selected_signs:
                            continue
                        candidate = take_candidate(sign_sphere_index)
                        if candidate is not None:
                            assignment = (sign_location, candidate)
                            break
                if assignment is not None:
                    selected_signs.add(assignment[0])
                    assignments.append(assignment)

            for sign_location, candidate in assignments:
                sign = sign_data_by_location_name[sign_location.name]
                candidate_type, candidate_value = candidate
                if candidate_type == "entrance":
                    source_id = typing.cast(int, candidate_value)
                    hint = world.get_entrance_hint_text(source_id)
                    world.sign_hint_entrances[sign.key] = source_id
                else:
                    item_location = typing.cast(typing.Any, candidate_value)
                    hint = f"{item_location.item.name} is at {item_location.name}"
                    if item_location.player != sign_location.player:
                        hint += f" in {multiworld.player_name[item_location.player]}'s game"
                    hint += "."
                    world.sign_hint_locations[sign.key] = item_location.address
                    world.sign_hint_location_players[sign.key] = item_location.player
                world.sign_hints[sign.key] = hint

    def generate_basic(self):
        if not self.options.buddy_checks:
            for location_name, item_name in (
                    ("Bob-omb Battlefield - Bob-omb Buddy", "Bob-omb Battlefield - Cannon Unlock"),
                    ("Whomp's Fortress - Bob-omb Buddy", "Whomp's Fortress - Cannon Unlock"),
                    ("Jolly Roger Bay - Bob-omb Buddy", "Jolly Roger Bay - Cannon Unlock"),
                    ("Cool, Cool Mountain - Bob-omb Buddy", "Cool, Cool Mountain - Cannon Unlock"),
                    ("Shifting Sand Land - Bob-omb Buddy", "Shifting Sand Land - Cannon Unlock"),
                    ("Snowman's Land - Bob-omb Buddy", "Snowman's Land - Cannon Unlock"),
                    ("Wet-Dry World - Bob-omb Buddy", "Wet-Dry World - Cannon Unlock"),
                    ("Tall, Tall Mountain - Bob-omb Buddy", "Tall, Tall Mountain - Cannon Unlock"),
                    ("Tiny-Huge Island - Bob-omb Buddy", "Tiny-Huge Island - Cannon Unlock"),
                    ("Rainbow Ride - Bob-omb Buddy", "Rainbow Ride - Cannon Unlock"),
                    ("Wing Mario Over the Rainbow - Bob-omb Buddy",
                     "Wing Mario Over the Rainbow - Cannon Unlock"),
            ):
                location = self.multiworld.get_location(location_name, self.player)
                location.address = None
                location.place_locked_item(self.create_event_item(item_name))

    def get_filler_item_name(self) -> str:
        return self.random.choice(progressive_filler_item_names)

    @staticmethod
    def get_rgb_color(value: int) -> typing.List[int]:
        return [(value >> 16) & 0xFF, (value >> 8) & 0xFF, value & 0xFF]

    def get_mario_colors_slot_data(self) -> typing.Dict[str, typing.List[int]]:
        return {
            "hat": self.get_rgb_color(self.options.mario_hat_color.value),
            "shirt": self.get_rgb_color(self.options.mario_shirt_color.value),
            "overalls": self.get_rgb_color(self.options.mario_overalls_color.value),
            "gloves": self.get_rgb_color(self.options.mario_gloves_color.value),
            "shoes": self.get_rgb_color(self.options.mario_shoes_color.value),
            "skin": self.get_rgb_color(self.options.mario_skin_color.value),
            "hair": self.get_rgb_color(self.options.mario_hair_color.value),
        }

    def get_coin_star_requirements_slot_data(self) -> typing.List[int]:
        return [
            getattr(self.options, option_name).value
            for option_name in coin_star_requirement_option_names
        ]

    def get_start_inventory_slot_data(self) -> typing.Dict[int, int]:
        start_inventory = {}
        for item_name in (
                self.get_unrandomized_level_feature_item_names()
                + self.get_unrandomized_optional_item_names()
                + self.get_unrandomized_bowser_stage_1up_item_names()
                + self.get_unrandomized_bowser_arena_bomb_item_names()
                + self.get_unrandomized_unlock_item_names()):
            item_id = item_table[item_name]
            start_inventory[item_id] = start_inventory.get(item_id, 0) + 1
        return start_inventory

    def get_re_gen_slot_data(self) -> typing.Dict[str, typing.Any]:
        return getattr(self.multiworld, "re_gen_passthrough", {}).get(self.game, {})

    def restore_options_from_slot_data(self, slot_data: typing.Dict[str, typing.Any]) -> None:
        for option_name, value in slot_data.get("Options", {}).items():
            if hasattr(self.options, option_name):
                getattr(self.options, option_name).value = value
        for option_name, value in zip(coin_star_requirement_option_names, slot_data.get("CoinStarRequirements", [])):
            getattr(self.options, option_name).value = value
        if "MusicShuffleMode" in slot_data:
            self.options.music_shuffle.value = slot_data["MusicShuffleMode"]
        if "SkyboxShuffleMode" in slot_data:
            self.options.skybox_shuffle.value = slot_data["SkyboxShuffleMode"]

    def get_music_slot_data_from_slot_data(
            self, slot_data: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any] | None:
        if "MusicShuffleMode" not in slot_data:
            return None
        music_slot_data = {"MusicShuffleMode": slot_data["MusicShuffleMode"]}
        if "MusicMap" in slot_data:
            music_slot_data["MusicMap"] = slot_data["MusicMap"]
        return music_slot_data

    def get_music_slot_data(self) -> typing.Dict[str, typing.Any]:
        if self.music_slot_data is None:
            self.music_slot_data = build_music_slot_data(
                self.options.music_shuffle.value, self.random)
        return self.music_slot_data.copy()

    def get_skybox_slot_data(self) -> typing.Dict[str, typing.Any]:
        if self.skybox_slot_data is None:
            from .Skyboxes import build_skybox_slot_data
            self.skybox_slot_data = build_skybox_slot_data(
                self.options.skybox_shuffle.value, self.random)
        return self.skybox_slot_data.copy()

    @staticmethod
    def get_skybox_slot_data_from_slot_data(
            slot_data: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any] | None:
        if "SkyboxShuffleMode" not in slot_data:
            return None
        skybox_slot_data = {"SkyboxShuffleMode": slot_data["SkyboxShuffleMode"]}
        if "SkyboxMap" in slot_data:
            skybox_slot_data["SkyboxMap"] = slot_data["SkyboxMap"]
        return skybox_slot_data

    def fill_slot_data(self):
        course_map = {
            source: destination for source, destination in self.area_connections.items()
            if isinstance(source, int) and isinstance(destination, int)
        }
        slot_data = {
            "SpicyMycenaVersion": SPICY_MYCENA_VERSION,
            "Options": self.options.as_dict(*self.slot_option_names),
            "AreaRando": course_map,
            "AreaConnections": self.area_connections,
            "SubAreaRando": self.sub_area_slot_data,
            "SubAreaShuffleMode": self.options.sub_area_shuffle.value,
            "CastleReturnShuffleMode": self.options.castle_return_shuffle.value,
            "MoveRandoVec": self.move_rando_bitvec,
            "GlobalCapItems": self.options.cap_items.value in {
                self.options.cap_items.option_global,
                self.options.cap_items.option_both,
            },
            "FullLevelUnlocks": self.options.level_unlocks.value == self.options.level_unlocks.option_full,
            "DeathLink": self.options.death_link.value,
            "CompletionType": self.options.completion_type.value,
            "CoinStarRequirements": self.get_coin_star_requirements_slot_data(),
            "CoinCountCheckLocations": list(self.coin_count_check_location_names),
            "GlobalCoinCountCheckLocations": list(self.global_coin_count_check_location_names),
            "GlobalCoinCountChecksEnabled": self.options.global_coin_count_checks.value > 0,
            "GlobalCoinCountCaps": list(self.get_global_coin_count_caps()),
            "CoinCheckLocations": list(self.coin_check_location_names),
            "StartInventory": self.get_start_inventory_slot_data(),
            "BowserStage1UpBehavior": self.options.bowser_stage_1ups.value != self.options.bowser_stage_1ups.option_vanilla,
            "OneUpChecks": self.options.one_up_checks.value,
            "BuddyChecks": self.options.buddy_checks.value,
            "EasyButterflies": self.options.easy_butterflies.value,
            "TriggerSparkles": self.options.trigger_sparkles.value,
            "NoDespawn": self.options.no_despawns.value,
            "MipsSkipEnabled": self.logic_castle_30_star_door_mips_skip,
            "BowserInTheDarkWorldHits": self.options.bowser_in_the_dark_world_health.value,
            "BowserInTheFireSeaHits": self.options.bowser_in_the_fire_sea_health.value,
            "BowserInTheSkyHits": self.options.bowser_in_the_sky_health.value,
            "BowserInTheSkyStageCollapseHits": self.options.bowser_in_the_sky_stage_collapse_hits.value,
            "SignHints": self.sign_hints,
            "SignHintLocations": self.sign_hint_locations,
            "SignHintLocationPlayers": self.sign_hint_location_players,
            "SignHintEntrances": self.sign_hint_entrances,
            "SignHintData": {
                str(sign.level * 256 + sign.dialog): [
                    self.sign_hints.get(sign.key, ""),
                    self.sign_hint_locations.get(sign.key, 0),
                    self.sign_hint_entrances.get(sign.key, 0),
                    self.sign_hint_location_players.get(sign.key, 0),
                ]
                for sign in sign_data
            },
        }
        slot_data.update(self.get_music_slot_data())
        slot_data.update(self.get_skybox_slot_data())
        mario_colors = self.get_mario_colors_slot_data()
        if mario_colors:
            slot_data["MarioColors"] = mario_colors
        return slot_data

    @staticmethod
    def interpret_slot_data(slot_data: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any]:
        return slot_data

    def reconnect_found_entrances(self, _found_key: str, data_storage_value) -> None:
        if _found_key.startswith("SM64SpicyPermanentCoinSources_"):
            if not isinstance(data_storage_value, dict):
                return
            self.permanent_coin_source_counts = {
                str(source_id): max(0, int(count))
                for source_id, count in data_storage_value.items()
                if isinstance(count, (int, float))
            }
            return

        try:
            discovered = int(data_storage_value or 0)
        except (TypeError, ValueError):
            return

        if _found_key.startswith("SM64SpicyFoundSubAreaEntrancesLow_"):
            discovered_source_ids = (
                source_id for source_id in range(1, 32)
                if discovered & (1 << (source_id - 1))
            )
        elif _found_key.startswith("SM64SpicyFoundSubAreaEntrancesHigh_"):
            discovered_source_ids = (
                source_id for source_id in range(32, 64)
                if discovered & (1 << (source_id - 32))
            )
        else:
            discovered_source_ids = (
                int(entrance_id) for bit, entrance_id in enumerate(sm64_shuffled_entrance_ids)
                if discovered & (1 << bit)
            )

        for source_id in discovered_source_ids:
            entrance = self.randomized_entrance_connections.get(source_id)
            target = self.deferred_entrance_targets.get(source_id)
            if entrance is None or target is None:
                continue
            if entrance.connected_region is None:
                entrance.connect(target)
            state = self.multiworld.state
            previous_allow_partial_entrances = state.allow_partial_entrances
            state.allow_partial_entrances = True
            try:
                source_was_in_logic = entrance.can_reach(state)
            finally:
                state.allow_partial_entrances = previous_allow_partial_entrances
            if source_id not in self.bypass_entrance_connections and not source_was_in_logic:
                bypass_region = self.multiworld.get_region("Bypassing Logic", self.player)
                physical_source = sub_area_source_by_id(source_id)
                source_name = (
                    SUB_AREA_SOURCE_DESCRIPTIONS[physical_source.key]
                    if physical_source is not None
                    else sm64_entrance_source_descriptions[source_id]
                )
                self.bypass_entrance_connections[source_id] = bypass_region.connect(
                    target,
                    name=f"Bypassing Logic -> {source_name}",
                )

    def get_apsm64ex_slot_data(self):
        slot_data = self.fill_slot_data()
        for item in self.multiworld.precollected_items[self.player]:
            if item.code is None:
                continue
            slot_data["StartInventory"][item.code] = slot_data["StartInventory"].get(item.code, 0) + 1
        return slot_data

    def generate_output(self, output_directory: str):
        if self.multiworld.players != 1:
            return
        data = {
            "slot_data": self.get_apsm64ex_slot_data(),
            "location_to_item": {
                location.address: location.item.code
                for location in self.multiworld.get_locations()
                if location.address is not None and location.item is not None and location.item.code is not None
            },
            "data_package": {
                "data": {
                    "games": {
                        self.game: {
                            "item_name_to_id": self.item_name_to_id,
                            "location_name_to_id": self.location_name_to_id
                        }
                    }
                }
            }
        }
        filename = f"{self.multiworld.get_out_file_name_base(self.player)}.apsm64ex"
        with open(os.path.join(output_directory, filename), 'w') as f:
            json.dump(data, f)

    def extend_hint_information(self, hint_data: typing.Dict[int, typing.Dict[int, str]]):
        if self.topology_present:
            er_hint_data = {}
            for entrance, destination in self.area_connections.items():
                if not isinstance(entrance, int) or not isinstance(destination, int):
                    continue
                destination_name = self.get_normal_entrance_name(destination)
                region_name = (
                    "Bowser in the Sky" if destination == int(SM64Levels.BOWSER_IN_THE_SKY)
                    else sm64_entrance_to_region[destination_name]
                )
                if destination_name == "Tiny-Huge Island (Tiny)":
                    continue
                if region_name == "Tick Tock Clock Moving":
                    region_name = "Tick Tock Clock"
                if destination_name == "Tiny-Huge Island (Huge)":
                    # Special rules for Tiny-Huge Island's dual entrances
                    reverse_area_connections = {
                        mapped_destination: mapped_entrance
                        for mapped_entrance, mapped_destination in self.area_connections.items()
                    }
                    entrance_name = (
                        self.get_connection_source_name(
                            reverse_area_connections[SM64Levels.TINY_HUGE_ISLAND_HUGE])
                        + ' or ' + self.get_connection_source_name(
                            reverse_area_connections[SM64Levels.TINY_HUGE_ISLAND_TINY])
                    )
                    regions = [
                        self.multiworld.get_region("Tiny-Huge Island (Huge)", self.player),
                        self.multiworld.get_region("Tiny-Huge Island (Tiny)", self.player),
                    ]
                else:
                    entrance_name = self.get_normal_entrance_source_name(entrance)
                    regions = [self.multiworld.get_region(region_name, self.player)]
                for region in regions[:]:
                    regions += region.subregions
                for region in regions:
                    for location in region.locations:
                        if location.address is None:
                            continue
                        er_hint_data[location.address] = entrance_name
            hint_data[self.player] = er_hint_data
