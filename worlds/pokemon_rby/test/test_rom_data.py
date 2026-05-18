import hashlib
import os
import unittest
from dataclasses import dataclass
from pathlib import Path
from types import SimpleNamespace

import Utils

from .. import PokemonBlueWorld, PokemonRedWorld, PokemonYellowWorld, poke_data
from ..items import item_table
from ..rom import resolve_rom_addresses


@dataclass(frozen=True)
class RomConfig:
    game: str
    world_type: type
    env_var: str
    default_file_name: str
    base_patch_file_name: str


ROM_CONFIGS = (
    RomConfig(
        "Pokemon Red",
        PokemonRedWorld,
        "POKEMON_RED_ROM",
        "Pokemon Red (UE) [S][!].gb",
        "basepatch_red.bsdiff4",
    ),
    RomConfig(
        "Pokemon Blue",
        PokemonBlueWorld,
        "POKEMON_BLUE_ROM",
        "Pokemon Blue (UE) [S][!].gb",
        "basepatch_blue.bsdiff4",
    ),
    RomConfig(
        "Pokemon Yellow",
        PokemonYellowWorld,
        "POKEMON_YELLOW_ROM",
        "Pokemon Yellow (U)[C][!].gbc",
        "basepatch_yellow.bsdiff4",
    ),
)

DEXSANITY_ROM_ADDRESS = "Dexsanity_Items"
POKEMON_RB_DIR = Path(__file__).resolve().parents[1]
TYPE_CHART_RESERVED_BYTES = 678


def get_base_rom_path(config: RomConfig) -> Path:
    if os.environ.get(config.env_var):
        return Path(os.environ[config.env_var]).expanduser()
    return Path(Utils.user_path(config.default_file_name))


def load_basepatched_rom(config: RomConfig) -> bytes:
    base_rom_path = get_base_rom_path(config)
    if not base_rom_path.exists():
        raise unittest.SkipTest(
            f"{config.game} ROM not found; set {config.env_var} or place {config.default_file_name} in the "
            "Archipelago user path."
        )

    base_rom = base_rom_path.read_bytes()
    actual_hash = hashlib.md5(base_rom).hexdigest()
    expected_hash = config.world_type.patch.hash
    if actual_hash != expected_hash:
        raise AssertionError(
            f"{config.game} ROM hash mismatch for {base_rom_path}: expected {expected_hash}, got {actual_hash}"
        )

    try:
        import bsdiff4
    except ImportError as exc:
        raise unittest.SkipTest(f"bsdiff4 is required to apply {config.game}'s base patch") from exc

    return bsdiff4.patch(base_rom, (POKEMON_RB_DIR / config.base_patch_file_name).read_bytes())


def item_byte_for_location(world_type: type, item_name: str) -> int:
    if item_name in world_type.pokemon_data:
        return world_type.pokemon_data[item_name]["id"]

    pokemon_name = " ".join(item_name.split()[1:])
    if pokemon_name in world_type.pokemon_data:
        return world_type.pokemon_data[pokemon_name]["id"]

    item_id = item_table[item_name].id
    if item_id > 255:
        item_id -= 256
    return item_id


def base_stats_address(world_type: type, mon_name: str, mon_data: dict) -> int:
    if mon_name == "Mew":
        return world_type.rom_addresses["Base_Stats_Mew"]
    return world_type.rom_addresses["Base_Stats"] + (28 * (mon_data["dex"] - 1))


def expected_move_record(move_data: dict) -> bytes:
    return bytes(
        (
            move_data["id"],
            move_data["effect"],
            move_data["power"],
            poke_data.type_ids[move_data["type"]],
            move_data["accuracy"] * 255 // 100,
            move_data["pp"],
        )
    )


def expected_type_chart() -> bytes:
    data = bytearray()
    for attacking_type, defending_type, effectiveness in poke_data.type_chart:
        if effectiveness != 10:
            data.extend(
                (
                    poke_data.type_ids[attacking_type],
                    poke_data.type_ids[defending_type],
                    effectiveness,
                )
            )
    return bytes(data)


def read_type_chart(rom: bytes, address: int) -> bytes:
    data = bytearray()
    end = address + TYPE_CHART_RESERVED_BYTES
    while address < end:
        matchup = rom[address:address + 3]
        if matchup == b"\xff\xff\xff":
            return bytes(data)
        if matchup != b"\xfe\xfe\xfe":
            data.extend(matchup)
        address += 3
    raise AssertionError("Type chart terminator was not found")


class TestBasepatchedRomData(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.roms = {config.game: load_basepatched_rom(config) for config in ROM_CONFIGS}

    def test_original_items_match_location_rom_addresses(self) -> None:
        for config in ROM_CONFIGS:
            world_type = config.world_type
            rom = self.roms[config.game]
            address_world = SimpleNamespace(rom_addresses=world_type.rom_addresses)

            for location in world_type.location_data:
                # Dexsanity has an AP-filled table, not vanilla ROM item bytes to validate.
                if location.rom_address in (None, DEXSANITY_ROM_ADDRESS) or location.original_item is None:
                    continue

                with self.subTest(game=config.game, location=location.name):
                    self.assertIsInstance(location.original_item, str)
                    expected = item_byte_for_location(world_type, location.original_item)
                    for address in resolve_rom_addresses(address_world, location.rom_address, location.address_offset):
                        self.assertEqual(expected, rom[address])

    def test_pokemon_data_matches_base_stats_tables(self) -> None:
        scalar_fields = (
            (0, "dex"),
            (1, "hp"),
            (2, "atk"),
            (3, "def"),
            (4, "spd"),
            (5, "spc"),
            (8, "catch rate"),
            (9, "base exp"),
            (19, "growth rate"),
        )
        type_fields = (
            (6, "type1"),
            (7, "type2"),
        )
        move_fields = (
            (15, "start move 1"),
            (16, "start move 2"),
            (17, "start move 3"),
            (18, "start move 4"),
        )

        for config in ROM_CONFIGS:
            world_type = config.world_type
            rom = self.roms[config.game]

            for mon_name, mon_data in world_type.pokemon_data.items():
                address = base_stats_address(world_type, mon_name, mon_data)
                with self.subTest(game=config.game, pokemon=mon_name):
                    for offset, field_name in scalar_fields:
                        self.assertEqual(mon_data[field_name], rom[address + offset], field_name)
                    for offset, field_name in type_fields:
                        self.assertEqual(poke_data.type_ids[mon_data[field_name]], rom[address + offset], field_name)
                    for offset, field_name in move_fields:
                        self.assertEqual(poke_data.moves[mon_data[field_name]]["id"], rom[address + offset], field_name)
                    self.assertEqual(bytes(mon_data["tms"]), rom[address + 20:address + 27], "tms")

    def test_moves_match_move_table(self) -> None:
        for config in ROM_CONFIGS:
            world_type = config.world_type
            rom = self.roms[config.game]
            move_table_address = world_type.rom_addresses["Move_Data"]

            for move_name, move_data in poke_data.moves.items():
                if move_data["id"] == 0:
                    continue

                address = move_table_address + ((move_data["id"] - 1) * 6)
                with self.subTest(game=config.game, move=move_name):
                    self.assertEqual(expected_move_record(move_data), rom[address:address + 6])

    def test_type_chart_matches_type_effect_table(self) -> None:
        expected = expected_type_chart()
        for config in ROM_CONFIGS:
            world_type = config.world_type
            rom = self.roms[config.game]
            address = world_type.rom_addresses["Type_Chart"]

            with self.subTest(game=config.game):
                self.assertEqual(expected, read_type_chart(rom, address))
