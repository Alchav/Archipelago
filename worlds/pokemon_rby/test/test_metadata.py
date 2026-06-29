import unittest
from types import SimpleNamespace

from BaseClasses import ItemClassification

from .. import PokemonBlueWorld, PokemonRBYWorld, PokemonRedWorld, PokemonYellowWorld
from ..items import item_groups, item_table
from ..locations import LocationData, PokemonRBYLocation
from ..rom_addresses import rom_addresses_rb, rom_addresses_yellow
from ..poke_data import pokemon_data


class TestPokemonItemMetadata(unittest.TestCase):
    def test_all_pokemon_have_standard_item_variants_with_expected_classifications(self) -> None:
        problems = []
        for pokemon in pokemon_data:
            if pokemon not in item_table:
                problems.append(f"missing base item for {pokemon}")
                continue
            if f"Uncatchable {pokemon}" not in item_table:
                problems.append(f"missing uncatchable item for {pokemon}")
                continue
            if f"Static {pokemon}" not in item_table:
                problems.append(f"missing static item for {pokemon}")
                continue
            if item_table[pokemon].classification != ItemClassification.progression:
                problems.append(f"{pokemon} classification changed")
            if item_table[f"Uncatchable {pokemon}"].classification != ItemClassification.useful:
                problems.append(f"Uncatchable {pokemon} classification changed")
            if item_table[f"Static {pokemon}"].classification != ItemClassification.progression:
                problems.append(f"Static {pokemon} classification changed")

        self.assertEqual([], problems)

class TestPokemonLocationMetadata(unittest.TestCase):
    def test_location_data_formats_names_from_region_and_special_cases(self) -> None:
        self.assertEqual(
            "Route 1 - Free Sample Man",
            LocationData("Route 1", "Free Sample Man", "Potion").name,
        )
        self.assertEqual(
            "Cerulean Bicycle Shop",
            LocationData("Cerulean Bicycle Shop", "", "Bicycle").name,
        )
        self.assertEqual(
            "Pokemon Tower 3F - Trainer Parties",
            LocationData("Pokemon Tower 3F", "Trainer Parties", "Trainer Parties").name,
        )
        self.assertEqual(
            "Silph Co 11F - Silph Co President",
            LocationData("Silph Co 11F-C", "Silph Co President", "Master Ball").name,
        )

    def test_location_groups_include_floor_aliases(self) -> None:
        self.assertIn("Silph Co 11F - Silph Co President", PokemonRedWorld.location_groups["Silph Co"])
        self.assertIn("Silph Co 11F - Silph Co President", PokemonRedWorld.location_groups["Silph Co 11F"])

    def test_pokemon_location_rule_accepts_normal_and_prefixed_pokemon_items(self) -> None:
        location = PokemonRBYLocation(1, "Test", None, None, "Static Pokemon", None, None)

        self.assertTrue(location.item_rule(SimpleNamespace(player=1, name="Bulbasaur")))
        self.assertTrue(location.item_rule(SimpleNamespace(player=1, name="Static Bulbasaur")))
        self.assertFalse(location.item_rule(SimpleNamespace(player=1, name="Poke Ball")))
        self.assertFalse(location.item_rule(SimpleNamespace(player=2, name="Static Bulbasaur")))

    def test_trainer_parties_location_rule_only_accepts_trainer_party_items(self) -> None:
        location = PokemonRBYLocation(1, "Test", None, None, "Trainer Parties", None, None)

        self.assertTrue(location.item_rule(SimpleNamespace(player=1, name="Trainer Parties")))
        self.assertFalse(location.item_rule(SimpleNamespace(player=1, name="Bulbasaur")))

    def test_all_trainersanity_hooks_have_matching_locations(self) -> None:
        rb_location_hooks = {
            location.rom_address
            for world_type in (PokemonRedWorld, PokemonBlueWorld)
            for location in world_type.location_data
            if isinstance(location.rom_address, str) and location.rom_address.startswith("Trainersanity_")
        }
        yellow_location_hooks = {
            location.rom_address
            for location in PokemonYellowWorld.location_data
            if isinstance(location.rom_address, str) and location.rom_address.startswith("Trainersanity_")
        }

        self.assertEqual(
            {key for key in rom_addresses_rb if key.startswith("Trainersanity_")},
            rb_location_hooks,
        )
        self.assertEqual(
            {key for key in rom_addresses_yellow if key.startswith("Trainersanity_")},
            yellow_location_hooks,
        )
