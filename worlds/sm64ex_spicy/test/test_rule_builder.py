import json
import unittest
from typing import cast

from BaseClasses import CollectionState

from .. import SM64World
from ..RuleBuilder import CanCollectCoins, CoinEvaluation, CoinSourceTrace, \
    register_coin_evaluator, unregister_coin_evaluator


TRACE_COURSE = "Rule Builder Trace Test"
BOOLEAN_COURSE = "Rule Builder Boolean Test"


def trace_evaluator(
        state: CollectionState,
        player: int,
        required_coins: int,
) -> CoinEvaluation:
    return CoinEvaluation(
        8,
        (
            CoinSourceTrace(
                "selected_route",
                "Selected route",
                8,
                True,
                children=(
                    CoinSourceTrace("counted_source", "Counted source", 8, True),
                    CoinSourceTrace("missing_source", "Missing source", 2, False, False),
                ),
            ),
            CoinSourceTrace("other_route", "Other route", 10, False),
        ),
    )


def boolean_evaluator(
        state: CollectionState,
        player: int,
        required_coins: int,
) -> bool:
    return required_coins <= 5


class FakeWorld:
    player = 1
    rule_caching_enabled = False


class CanCollectCoinsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        register_coin_evaluator(
            TRACE_COURSE,
            trace_evaluator,
            item_dependencies=("Test Item",),
            region_dependencies=("Test Region",),
        )
        register_coin_evaluator(BOOLEAN_COURSE, boolean_evaluator)

    @classmethod
    def tearDownClass(cls) -> None:
        unregister_coin_evaluator(TRACE_COURSE)
        unregister_coin_evaluator(BOOLEAN_COURSE)

    def test_serialization_round_trip(self) -> None:
        rule = CanCollectCoins(TRACE_COURSE, 10)
        serialized = rule.to_dict()

        self.assertEqual(serialized, {
            "rule": "CanCollectCoins",
            "options": [],
            "filtered_resolution": False,
            "args": {
                "course_name": TRACE_COURSE,
                "required_coins": 10,
            },
        })
        json.dumps(serialized)
        self.assertEqual(SM64World.rule_from_dict(serialized), rule)

    def test_structured_explanation_formatting(self) -> None:
        resolved = CanCollectCoins(TRACE_COURSE, 10).resolve(cast(SM64World, FakeWorld()))
        state = cast(CollectionState, object())

        self.assertFalse(resolved(state))
        self.assertEqual(resolved.explain_json(state), [
            {"type": "text", "text": "Reachable coins in "},
            {"type": "color", "color": "cyan", "text": TRACE_COURSE},
            {"type": "text", "text": ": "},
            {"type": "color", "color": "salmon", "text": "8/10"},
            {"type": "text", "text": "\n  "},
            {"type": "color", "color": "green", "text": "+8"},
            {"type": "text", "text": " "},
            {"type": "color", "color": "green", "text": "Selected route"},
            {"type": "text", "text": "\n    "},
            {"type": "color", "color": "green", "text": "+8"},
            {"type": "text", "text": " "},
            {"type": "color", "color": "green", "text": "Counted source"},
            {"type": "text", "text": "\n    "},
            {"type": "color", "color": "salmon", "text": "0/2"},
            {"type": "text", "text": " "},
            {"type": "color", "color": "salmon", "text": "Missing source"},
            {"type": "text", "text": " (unavailable)"},
            {"type": "text", "text": "\n  "},
            {"type": "color", "color": "yellow", "text": "0/10"},
            {"type": "text", "text": " "},
            {"type": "color", "color": "yellow", "text": "Other route"},
            {"type": "text", "text": " (not selected)"},
        ])

    def test_explanation_without_state(self) -> None:
        resolved = CanCollectCoins(TRACE_COURSE, 10).resolve(cast(SM64World, FakeWorld()))

        self.assertEqual(resolved.explain_json(), [
            {"type": "text", "text": "Collect "},
            {"type": "color", "color": "cyan", "text": "10"},
            {"type": "text", "text": " coins in "},
            {"type": "color", "color": "cyan", "text": TRACE_COURSE},
        ])

    def test_boolean_evaluator_compatibility(self) -> None:
        state = cast(CollectionState, object())
        reachable = CanCollectCoins(BOOLEAN_COURSE, 5).resolve(cast(SM64World, FakeWorld()))
        unreachable = CanCollectCoins(BOOLEAN_COURSE, 6).resolve(cast(SM64World, FakeWorld()))

        self.assertTrue(reachable(state))
        self.assertFalse(unreachable(state))
        self.assertEqual(unreachable.explain_json(state), [
            {"type": "text", "text": "Cannot collect "},
            {"type": "color", "color": "salmon", "text": "6"},
            {"type": "text", "text": " coins in "},
            {"type": "color", "color": "cyan", "text": BOOLEAN_COURSE},
        ])

    def test_resolved_dependencies_come_from_registration(self) -> None:
        resolved = CanCollectCoins(TRACE_COURSE, 10).resolve(cast(SM64World, FakeWorld()))

        self.assertEqual(resolved.item_dependencies(), {"Test Item": {id(resolved)}})
        self.assertEqual(resolved.region_dependencies(), {"Test Region": {id(resolved)}})
