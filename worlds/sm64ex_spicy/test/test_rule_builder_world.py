import json

from BaseClasses import CollectionState
from rule_builder.rules import Rule

from .bases import SM64TestBase
from ..Items import item_table
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
