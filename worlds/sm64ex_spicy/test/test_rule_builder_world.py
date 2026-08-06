import json

from BaseClasses import CollectionState
from rule_builder.rules import Rule

from .bases import SM64TestBase
from .. import Options
from ..Items import item_table
from ..CoinLogic import COIN_EVALUATORS, _coin_source_rule_specs
from ..RuleBuilder import CanCollectCoins, CoinSourceTrace
from ..Rules import has_unlock


class RuleBuilderWorldTestBase(SM64TestBase):
    def test_unlock_logic_uses_start_inventory_not_shuffle_option(self):
        state = CollectionState(self.multiworld)
        self.world.start_inventory_item_ids = set()
        self.assertFalse(has_unlock(
            state, self.player, "enemy_unlocks",
            "Thwomp", "Whomp's Fortress - Thwomp"))

        self.world.start_inventory_item_ids.add(item_table["Whomp's Fortress - Thwomp"])
        self.assertTrue(has_unlock(
            state, self.player, "enemy_unlocks",
            "Thwomp", "Whomp's Fortress - Thwomp"))

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
        self.assertIn(
            "Small Goomba in the starting Tiny region (unavailable)\n      (",
            explanation,
        )
        self.assertIn("Tiny-Huge Island (Tiny)", explanation)
        self.assertIn("Tiny-Huge Island - Goombas", explanation)

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
