import unittest
from types import SimpleNamespace
from unittest import mock

from .. import poke_data
from .. import encounters
from ..encounters import (get_base_stat_total, get_encounter_slots, process_pokemon_locations, process_trainer_data,
                          randomize_pokemon)
from ..locations import build_location_data, location_data_blue, location_data_red


red_location_data, _, _, _ = build_location_data(
    location_data_red,
    trainer_data={},
)
blue_location_data, _, _, _ = build_location_data(
    location_data_blue,
    trainer_data={},
)


class FixedTriangularRandom:
    def __init__(self, value: float = 0) -> None:
        self.value = value

    def triangular(self, low: float, high: float, mode: float) -> float:
        return self.value


class FakeChoice:
    def __init__(self, value: int, current_key: str) -> None:
        self.value = value
        self.current_key = current_key

    def __bool__(self) -> bool:
        return bool(self.value)

    def __eq__(self, other) -> bool:
        return other == self.value or other == self.current_key


class FakePlacedLocation:
    def __init__(self, name: str) -> None:
        self.name = name
        self.item = None
        self.locked = False

    def place_locked_item(self, item) -> None:
        self.item = item
        self.locked = True
        item.location = self


class FakeMultiWorld:
    def __init__(self, names) -> None:
        self.locations = {name: FakePlacedLocation(name) for name in names}

    def get_location(self, name: str, player: int) -> FakePlacedLocation:
        return self.locations[name]


class FakeTrainerMultiWorld:
    def __init__(self, locations) -> None:
        self.locations = locations

    def get_locations(self, player: int):
        return self.locations

    def get_location(self, name: str, player: int):
        raise AssertionError(f"Unexpected starter lookup for {name}")


def make_world(game_version: int = 1, catch_em_all: bool = False,
               randomize_pokemon_locations: bool = False, accessibility: str = "minimal") -> SimpleNamespace:
    return SimpleNamespace(
        game="Pokemon Red" if game_version else "Pokemon Blue",
        options=SimpleNamespace(
            game_version=SimpleNamespace(value=game_version),
            catch_em_all=catch_em_all,
            randomize_pokemon_locations=randomize_pokemon_locations,
            accessibility=accessibility,
        ),
        location_data=red_location_data if game_version else blue_location_data,
        local_poke_data=poke_data.pokemon_data,
    )


def slot_by_name(slots):
    return {slot.name: slot for slot in slots}


class TestEncounterSlots(unittest.TestCase):
    def test_get_encounter_slots_filters_to_requested_types(self) -> None:
        slots = get_encounter_slots(make_world(), ["Starter Pokemon"])

        self.assertEqual(
            {"Oak's Lab - Starter 1", "Oak's Lab - Starter 2", "Oak's Lab - Starter 3"},
            {slot.name for slot in slots},
        )

    def test_get_encounter_slots_uses_game_version_for_wild_exclusives(self) -> None:
        red_slots = slot_by_name(get_encounter_slots(make_world(game_version=1), ["Wild Encounter"]))
        blue_slots = slot_by_name(get_encounter_slots(make_world(game_version=0), ["Wild Encounter"]))

        self.assertEqual("Weedle", red_slots["Route 2 - Wild Pokemon - 6"].original_item)
        self.assertEqual("Caterpie", blue_slots["Route 2 - Wild Pokemon - 6"].original_item)

    def test_get_encounter_slots_alternates_version_exclusives_for_non_randomized_catch_em_all(self) -> None:
        slots = slot_by_name(get_encounter_slots(
            make_world(game_version=1, catch_em_all=True),
            ["Wild Encounter"],
        ))

        self.assertEqual("Weedle", slots["Route 2 - Wild Pokemon - 6"].original_item)
        self.assertEqual("Caterpie", slots["Route 2 - Wild Pokemon - 9"].original_item)
        self.assertEqual("Weedle", slots["Route 2 - Wild Pokemon - 10"].original_item)
        self.assertEqual("Ekans", slots["Route 4 - Wild Pokemon - 4"].original_item)
        self.assertEqual("Sandshrew", slots["Route 4 - Wild Pokemon - 6"].original_item)

    def test_get_encounter_slots_alternates_version_exclusives_for_full_accessibility(self) -> None:
        slots = slot_by_name(get_encounter_slots(
            make_world(game_version=1, accessibility="full"),
            ["Wild Encounter"],
        ))

        self.assertEqual("Weedle", slots["Route 2 - Wild Pokemon - 6"].original_item)
        self.assertEqual("Caterpie", slots["Route 2 - Wild Pokemon - 9"].original_item)
        self.assertEqual("Weedle", slots["Route 2 - Wild Pokemon - 10"].original_item)
        self.assertEqual("Ekans", slots["Route 4 - Wild Pokemon - 4"].original_item)
        self.assertEqual("Sandshrew", slots["Route 4 - Wild Pokemon - 6"].original_item)

    def test_get_encounter_slots_keeps_special_prize_slots_version_specific(self) -> None:
        red_prize_4_source = next(
            location.original_item for location in red_location_data
            if location.name == "Celadon Prize Corner - Pokemon Prize - 4"
        )
        red_prize_5_source = next(
            location.original_item for location in red_location_data
            if location.name == "Celadon Prize Corner - Pokemon Prize - 5"
        )
        blue_prize_4_source = next(
            location.original_item for location in blue_location_data
            if location.name == "Celadon Prize Corner - Pokemon Prize - 4"
        )
        blue_prize_5_source = next(
            location.original_item for location in blue_location_data
            if location.name == "Celadon Prize Corner - Pokemon Prize - 5"
        )
        red_slots = slot_by_name(get_encounter_slots(
            make_world(game_version=1, catch_em_all=True),
            ["Static Repeatable Pokemon"],
        ))
        blue_slots = slot_by_name(get_encounter_slots(
            make_world(game_version=0, catch_em_all=True),
            ["Static Repeatable Pokemon"],
        ))

        self.assertEqual(red_prize_4_source, red_slots["Celadon Prize Corner - Pokemon Prize - 4"].original_item)
        self.assertEqual(red_prize_5_source, red_slots["Celadon Prize Corner - Pokemon Prize - 5"].original_item)
        self.assertEqual(blue_prize_4_source, blue_slots["Celadon Prize Corner - Pokemon Prize - 4"].original_item)
        self.assertEqual(blue_prize_5_source, blue_slots["Celadon Prize Corner - Pokemon Prize - 5"].original_item)

    def test_get_encounter_slots_deepcopies_location_data(self) -> None:
        source_slot = next(location for location in red_location_data if location.name == "Route 2 - Wild Pokemon - 6")
        returned_slot = slot_by_name(get_encounter_slots(make_world(), ["Wild Encounter"]))[
            "Route 2 - Wild Pokemon - 6"
        ]

        self.assertIsNot(source_slot, returned_slot)
        self.assertEqual("Weedle", source_slot.original_item)
        self.assertEqual("Weedle", returned_slot.original_item)


class TestEncounterRandomizationHelpers(unittest.TestCase):
    def test_get_base_stat_total_sums_all_five_base_stats(self) -> None:
        self.assertEqual(253, get_base_stat_total("Bulbasaur"))

    def test_randomize_pokemon_prefers_type_matches_when_possible(self) -> None:
        world = make_world()

        self.assertEqual(
            "Growlithe",
            randomize_pokemon(world, "Charmander", ["Squirtle", "Growlithe", "Vulpix"], 1, FixedTriangularRandom()),
        )

    def test_randomize_pokemon_falls_back_to_full_list_without_type_matches(self) -> None:
        world = make_world()

        self.assertEqual(
            "Squirtle",
            randomize_pokemon(world, "Charmander", ["Squirtle", "Oddish"], 1, FixedTriangularRandom()),
        )

    def test_randomize_pokemon_prefers_closest_base_stat_total(self) -> None:
        world = make_world()

        self.assertEqual(
            "Ivysaur",
            randomize_pokemon(world, "Bulbasaur", ["Mewtwo", "Ivysaur", "Caterpie"], 2, FixedTriangularRandom()),
        )

    def test_randomize_pokemon_can_match_types_and_stats_together(self) -> None:
        world = make_world()

        self.assertEqual(
            "Oddish",
            randomize_pokemon(world, "Bulbasaur", ["Psyduck", "Oddish", "Bellsprout"], 3, FixedTriangularRandom()),
        )

    def test_process_trainer_data_keeps_yellow_rival_eevee_line_vanilla(self) -> None:
        flat_rival_party = {
            "level": [9, 8],
            "party": ["Spearow", "Eevee"],
            "party_address": "Trainer_Party_Route_22_Rival1_A",
        }
        branched_rival_party = {
            "level": [38, 40],
            "party": [
                ["Sandslash", "Jolteon"],
                ["Sandslash", "Flareon"],
                ["Sandslash", "Vaporeon"],
            ],
            "party_address": [
                "Trainer_Party_Silph_Co_7F_Rival2_Jolteon_A",
                "Trainer_Party_Silph_Co_7F_Rival2_Flareon_A",
                "Trainer_Party_Silph_Co_7F_Rival2_Vaporeon_A",
            ],
        }
        non_rival_party = {
            "level": 20,
            "party": ["Eevee"],
            "party_address": "Trainer_Party_Test_A",
        }
        world = SimpleNamespace(
            game="Pokemon Yellow",
            player=1,
            multiworld=FakeTrainerMultiWorld([
                SimpleNamespace(
                    name="Route 22 - Trainer Parties",
                    type="Trainer Parties",
                    party_data=[flat_rival_party],
                ),
                SimpleNamespace(
                    name="Silph Co 7F-NW - Trainer Parties",
                    type="Trainer Parties",
                    party_data=[branched_rival_party],
                ),
                SimpleNamespace(
                    name="Test Region - Trainer Parties",
                    type="Trainer Parties",
                    party_data=[non_rival_party],
                ),
            ]),
            options=SimpleNamespace(
                trainer_legendaries=SimpleNamespace(value=False),
                randomize_legendary_pokemon=SimpleNamespace(value=0),
                randomize_pokemon_locations=FakeChoice(0, "vanilla"),
                randomize_trainer_parties=FakeChoice(4, "completely_random"),
            ),
            random=SimpleNamespace(),
        )

        with mock.patch.object(encounters, "randomize_pokemon", side_effect=lambda *args: "Pikachu"):
            process_trainer_data(world)

        self.assertEqual(["Pikachu", "Eevee"], flat_rival_party["party"])
        self.assertEqual(
            [
                ["Pikachu", "Jolteon"],
                ["Pikachu", "Flareon"],
                ["Pikachu", "Vaporeon"],
            ],
            branched_rival_party["party"],
        )
        self.assertEqual(["Pikachu"], non_rival_party["party"])

    def test_process_pokemon_locations_counts_static_repeatable_pokemon_for_catch_em_all(self) -> None:
        repeatable_slot = SimpleNamespace(
            name="Route 4 Pokemon Center - Pokemon For Sale",
            type="Static Repeatable Pokemon",
            original_item="Bulbasaur",
        )
        wild_slots = [
            SimpleNamespace(name="Route 1 - Wild Pokemon - 1", type="Wild Encounter", original_item="Charmander"),
            SimpleNamespace(name="Route 1 - Wild Pokemon - 2", type="Wild Encounter", original_item="Charmander"),
        ]
        multiworld = FakeMultiWorld([repeatable_slot.name, *(slot.name for slot in wild_slots)])
        world = SimpleNamespace(
            game="Pokemon Red",
            options=SimpleNamespace(
                randomize_legendary_pokemon=FakeChoice(0, "vanilla"),
                randomize_pokemon_locations=FakeChoice(4, "completely_random"),
                catch_em_all=FakeChoice(1, "first_stage"),
                area_1_to_1_mapping=False,
                oaks_aide_rt_2=SimpleNamespace(value=0),
                oaks_aide_rt_11=SimpleNamespace(value=0),
                oaks_aide_rt_15=SimpleNamespace(value=0),
                elite_four_pokedex_condition=SimpleNamespace(total=0),
                accessibility="minimal",
            ),
            multiworld=multiworld,
            player=1,
            random=SimpleNamespace(
                shuffle=lambda sequence: None,
                sample=lambda sequence, count: sequence[:count],
            ),
            local_poke_data=poke_data.pokemon_data,
            create_item=lambda name: SimpleNamespace(name=name, location=None),
        )

        def fake_get_encounter_slots(world_obj, types):
            if types == ["Starter Pokemon"] or types == ["Legendary Pokemon"]:
                return []
            if types == ["Static Pokemon", "Static Repeatable Pokemon", "Uncatchable Pokemon"]:
                return [repeatable_slot]
            if types == ["Wild Encounter"]:
                return wild_slots
            raise AssertionError(types)

        with mock.patch.object(encounters, "get_encounter_slots", side_effect=fake_get_encounter_slots), \
                mock.patch.object(encounters, "randomize_pokemon", side_effect=lambda self, mon, mons, typ, rnd: mon), \
                mock.patch.object(encounters.poke_data, "first_stage_pokemon", ["Bulbasaur"]):
            process_pokemon_locations(world)

        self.assertEqual("Bulbasaur", multiworld.get_location(repeatable_slot.name, 1).item.name)
        self.assertEqual("Charmander", multiworld.get_location("Route 1 - Wild Pokemon - 1", 1).item.name)
        self.assertEqual("Charmander", multiworld.get_location("Route 1 - Wild Pokemon - 2", 1).item.name)

    def test_process_pokemon_locations_uses_repeatable_slots_for_full_accessibility(self) -> None:
        repeatable_slots = [
            SimpleNamespace(name="Route 4 Pokemon Center - Pokemon For Sale", type="Static Repeatable Pokemon",
                            original_item="Magikarp"),
            SimpleNamespace(name="Underground Path Route 5 - Spot Trade", type="Static Repeatable Pokemon",
                            original_item="Nidoran M"),
            SimpleNamespace(name="Route 11 Gate 2F - Terry Trade", type="Static Repeatable Pokemon",
                            original_item="Nidoran F"),
            SimpleNamespace(name="Cinnabar Lab Fossil Room - Sailor Trade", type="Static Repeatable Pokemon",
                            original_item="Lickitung"),
        ]
        multiworld = FakeMultiWorld([slot.name for slot in repeatable_slots])
        world = SimpleNamespace(
            game="Pokemon Red",
            options=SimpleNamespace(
                randomize_legendary_pokemon=FakeChoice(0, "vanilla"),
                randomize_pokemon_locations=FakeChoice(0, "vanilla"),
                catch_em_all=False,
                accessibility="full",
            ),
            multiworld=multiworld,
            player=1,
            random=SimpleNamespace(
                shuffle=lambda sequence: None,
                sample=lambda sequence, count: sequence[:count],
            ),
            local_poke_data=poke_data.pokemon_data,
            create_item=lambda name: SimpleNamespace(name=name, location=None),
        )

        def fake_get_encounter_slots(world_obj, types):
            if types == ["Starter Pokemon"] or types == ["Legendary Pokemon"] or types == ["Wild Encounter"]:
                return []
            if types == ["Static Pokemon", "Static Repeatable Pokemon", "Uncatchable Pokemon"]:
                return repeatable_slots
            raise AssertionError(types)

        with mock.patch.object(encounters, "get_encounter_slots", side_effect=fake_get_encounter_slots), \
                mock.patch.object(encounters, "get_full_accessibility_evolution_roots",
                                  return_value=["Bulbasaur", "Charmander", "Squirtle", "Eevee"]):
            process_pokemon_locations(world)

        placed = [multiworld.get_location(slot.name, 1).item.name for slot in repeatable_slots]
        self.assertEqual(["Bulbasaur", "Charmander", "Eevee", "Squirtle"], sorted(placed))

    def test_non_randomized_accessibility_requires_normal_evolution_roots(self) -> None:
        candidate_location = FakePlacedLocation("Cinnabar Lab Fossil Room - Dome Fossil Pokemon")
        candidate_location.item = SimpleNamespace(name="Articuno", location=candidate_location)
        placed_mons = {pokemon: 0 for pokemon in poke_data.pokemon_data}
        placed_mons["Articuno"] = 1
        static_placed_mons = {pokemon: 0 for pokemon in poke_data.pokemon_data}
        static_placed_mons["Kabuto"] = 1
        world = SimpleNamespace(
            options=SimpleNamespace(accessibility="full", dexsanity=False),
            create_item=lambda name: SimpleNamespace(name=name, location=None),
        )

        with mock.patch.object(encounters, "get_full_accessibility_evolution_roots", return_value=["Kabuto"]):
            encounters.ensure_non_randomized_accessibility(
                world, placed_mons, static_placed_mons, [candidate_location])

        self.assertEqual("Kabuto", candidate_location.item.name)
