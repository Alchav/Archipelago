import json

from BaseClasses import CollectionState
from rule_builder.rules import Rule

from .bases import SM64TestBase
from .. import Options
from ..Items import item_table
from ..CoinLogic import COIN_EVALUATORS, _coin_source_rule_specs
from ..RuleBuilder import CanCollectCoins, CoinSourceTrace, HasUnlock
from ..Regions import SM64_WDW_LOW
from ..Rules import has_unlock


class RuleBuilderWorldTestBase(SM64TestBase):
    def test_unlock_logic_uses_start_inventory_not_shuffle_option(self):
        state = CollectionState(self.multiworld)
        self.world.start_inventory_item_ids = set()
        self.assertFalse(has_unlock(
            state, self.player, "enemy_unlocks",
            "Thwomps and Grindels", "Whomp's Fortress - Thwomps"))

        self.world.start_inventory_item_ids.add(item_table["Whomp's Fortress - Thwomps"])
        self.assertTrue(has_unlock(
            state, self.player, "enemy_unlocks",
            "Thwomps and Grindels", "Whomp's Fortress - Thwomps"))

    def test_start_inventory_unlock_has_no_internal_explanation_text(self):
        item_name = "Whomp's Fortress - Thwomps"
        self.world.start_inventory_item_ids.add(item_table[item_name])
        rule = HasUnlock("Thwomps and Grindels", item_name).resolve(self.world)

        self.assertTrue(rule(CollectionState(self.multiworld)))
        self.assertEqual(rule.explain_json(CollectionState(self.multiworld)), [])

    def test_all_access_rules_are_resolved_rule_builder_rules(self):
        for spot in (*self.multiworld.get_entrances(self.player), *self.multiworld.get_locations(self.player)):
            with self.subTest(spot=spot.name):
                self.assertIsInstance(spot.access_rule, Rule.Resolved)

        self.assertIsInstance(
            self.multiworld.completion_condition[self.player],
            Rule.Resolved,
        )

    def test_all_rule_explanations_are_json_serializable(self):
        states = (None, self.multiworld.state, self.multiworld.get_all_state(False))
        rules = [
            *(spot.access_rule for spot in self.multiworld.get_entrances(self.player)),
            *(spot.access_rule for spot in self.multiworld.get_locations(self.player)),
            self.multiworld.completion_condition[self.player],
        ]

        for rule in rules:
            for state in states:
                with self.subTest(rule=str(rule), has_state=state is not None):
                    result_before = rule(state) if state is not None else None
                    json.dumps(rule.explain_json(state))
                    if state is not None:
                        self.assertEqual(rule(state), result_before)


class VariantEntranceExplanationTest(SM64TestBase):
    options = {
        "area_rando": Options.AreaRandomizer.option_Off,
    }

    @staticmethod
    def explanation_text(messages) -> str:
        return "".join(part.get("text", "") for part in messages)

    def test_wet_dry_world_explains_all_painting_heights(self):
        explanation = self.explanation_text(
            self.world.explain_rule("Wet-Dry World", CollectionState(self.multiworld)))

        self.assertIn("Wet-Dry World entrances:", explanation)
        self.assertIn("Wet-Dry World with Low Water is at the bottom of the Wet-Dry World painting", explanation)
        self.assertIn("Wet-Dry World with Middle Water is at the middle of the Wet-Dry World painting", explanation)
        self.assertIn("Wet-Dry World with High Water is at the top of the Wet-Dry World painting", explanation)

    def test_tick_tock_clock_explains_all_clock_times(self):
        explanation = self.explanation_text(
            self.world.explain_rule("Tick Tock Clock", CollectionState(self.multiworld)))

        self.assertIn("Tick Tock Clock entrances:", explanation)
        self.assertIn("Tick-Tock Clock with Stopped Time is at Tick-Tock Clock, at 12 o'clock", explanation)
        self.assertIn("Tick-Tock Clock with Slow Time is at Tick-Tock Clock, at 3 o'clock", explanation)
        self.assertIn("Tick-Tock Clock with Random Time is at Tick-Tock Clock, at 6 o'clock", explanation)
        self.assertIn("Tick-Tock Clock with Fast Time is at Tick-Tock Clock, at 9 o'clock", explanation)

    def test_shifting_sand_land_explains_main_and_pyramid_entrances(self):
        explanation = self.explanation_text(
            self.world.explain_rule("Shifting Sand Land", CollectionState(self.multiworld)))

        self.assertIn("Shifting Sand Land entrances:", explanation)
        self.assertIn("Shifting Sand Land is at the Shifting Sand Land painting", explanation)
        self.assertIn(
            "the lower Shifting Sand Land pyramid is at the side entrance of the Shifting Sand Land pyramid",
            explanation,
        )
        self.assertIn(
            "the upper Shifting Sand Land pyramid is at the top entrance of the Shifting Sand Land pyramid",
            explanation,
        )

    def test_undiscovered_entrance_does_not_reveal_its_source(self):
        source_id = next(
            source for source, destination in self.world.area_connections.items()
            if destination == SM64_WDW_LOW
        )
        entrance = self.world.randomized_entrance_connections[source_id]
        target = entrance.connected_region
        target.entrances.remove(entrance)
        entrance.connected_region = None
        self.world.deferred_entrance_targets[source_id] = target

        explanation = self.explanation_text(
            self.world.explain_rule("Wet-Dry World", CollectionState(self.multiworld)))

        self.assertIn("Wet-Dry World with Low Water: entrance not discovered.", explanation)
        self.assertNotIn("Low Water is at the bottom of the Wet-Dry World painting", explanation)

    def test_regular_course_explains_its_main_entrance(self):
        explanation = self.explanation_text(
            self.world.explain_rule("Whomp's Fortress", CollectionState(self.multiworld)))

        self.assertIn("Whomp's Fortress entrances:", explanation)
        self.assertIn("Whomp's Fortress is at the Whomp's Fortress painting", explanation)

    def test_non_course_names_use_universal_trackers_normal_explanation(self):
        self.assertIsNone(self.world.explain_rule("Castle Lobby", CollectionState(self.multiworld)))


class CoinSourceExplanationTest(SM64TestBase):
    options = {
        "area_rando": Options.AreaRandomizer.option_Off,
        "level_unlocks": Options.LevelUnlocks.option_full,
        "coin_object_unlocks": Options.CoinObjectUnlocks.option_per_level,
        "enemy_unlocks": Options.EnemyUnlocks.option_per_level,
        "level_features": Options.LevelFeatures.option_per_level,
        "tiny_huge_island_coin_star_requirement": 1,
    }

    def test_tiny_start_goomba_explains_region_and_unlock(self):
        state = CollectionState(self.multiworld)
        rule = CanCollectCoins("Tiny-Huge Island", 1).resolve(self.world)

        explanation = "".join(part.get("text", "") for part in rule.explain_json(state))

        self.assertIn("Small Goomba in the starting Tiny region", explanation)
        self.assertIn("Small Goomba in the starting Tiny region (unavailable)", explanation)
        self.assertIn("Tiny-Huge Island (Tiny)", explanation)
        self.assertIn("Tiny-Huge Island - Goombas", explanation)
        self.assertIn("Collected: 0/1", explanation)

    def test_every_generated_coin_source_has_a_rule(self):
        state = self.multiworld.get_all_state(False)
        specs = _coin_source_rule_specs()

        def source_ids(sources: tuple[CoinSourceTrace, ...]):
            for source in sources:
                yield source.source_id
                yield from source_ids(source.children)

        missing = []
        for course_name, evaluator in COIN_EVALUATORS.items():
            evaluation = evaluator(state, self.player, 1)
            missing.extend(
                (course_name, source_id)
                for source_id in source_ids(evaluation.children)
                if (course_name, source_id) not in specs
            )

        self.assertEqual(missing, [])


class PermanentCoinSourceExplanationTest(CoinSourceExplanationTest):
    def test_collected_count_uses_restored_canonical_source(self):
        self.world.reconnect_found_entrances(
            "SM64SpicyPermanentCoinSources_1",
            {"Tiny-Huge Island:tiny_start_goomba": 1},
        )
        state = CollectionState(self.multiworld)
        rule = CanCollectCoins("Tiny-Huge Island", 1).resolve(self.world)

        explanation = "".join(part.get("text", "") for part in rule.explain_json(state))

        self.assertIn("Small Goomba in the starting Tiny region", explanation)
        self.assertIn("Collected: 1/1", explanation)
