import pytest
from unittest import TestCase
from typing import cast
from types import SimpleNamespace

from Options import Accessibility
from ..Options import SohOptions, RainbowBridge, GanonsCastleBossKey, ShuffleTokens
from ..Locations import token_amounts
from ..Enums import TokenCounts

class TestSohOptionsForRequiredSkulltulaCount(TestCase):

    def setUp(self):
        # These are picked to avoid the conditions we're testing for to make it easier to isolate
        # conditional logics in the tests
        self.shuffle_100_gs_reward = False
        self.accessibility = Accessibility.option_full
        self.exclude_locations = set()

        self.rainbow_bridge = RainbowBridge.option_vanilla
        self.rainbow_bridge_skull_tokens_required = SimpleNamespace(value=0)

        self.ganons_castle_boss_key = GanonsCastleBossKey.option_vanilla
        self.ganons_castle_boss_key_skull_tokens_required = SimpleNamespace(value=0)

        self.shuffle_skull_tokens = ShuffleTokens.option_off
    
    def set_rainbow_bridge_tokens(self, amount):
        self.rainbow_bridge = RainbowBridge.option_tokens
        self.rainbow_bridge_skull_tokens_required.value = amount

    def set_ganons_castle_key_tokens(self, amount):
        self.ganons_castle_boss_key = GanonsCastleBossKey.option_lacs_skull_tokens
        self.ganons_castle_boss_key_skull_tokens_required.value = amount
    
    def calculate_progression_skulltula_count(self):
        return SohOptions.calculate_progression_skulltula_count(
            cast(SohOptions, self), 
            token_reward_counts=token_amounts
        )

    def test_base_case(self):
        self.assertEqual(self.calculate_progression_skulltula_count(), 0)

    def test_100_gs_reward(self):
        self.shuffle_100_gs_reward = True
        self.assertEqual(self.calculate_progression_skulltula_count(), 0)

        self.shuffle_skull_tokens = ShuffleTokens.option_all
        self.assertEqual(self.calculate_progression_skulltula_count(), 100)

        self.shuffle_skull_tokens = ShuffleTokens.option_dungeon
        self.assertEqual(self.calculate_progression_skulltula_count(), 44)

        self.shuffle_skull_tokens = ShuffleTokens.option_overworld
        self.assertEqual(self.calculate_progression_skulltula_count(), 56)

    def test_excludes_first_location(self):
        keys = list(token_amounts.keys())
        self.exclude_locations = {str(keys[0])}

        self.assertEqual(self.calculate_progression_skulltula_count(), 0)

    def test_rainbow_bridge_tokens(self):
        self.set_rainbow_bridge_tokens(80)
        self.assertEqual(self.calculate_progression_skulltula_count(), 0)

    def test_ganons_castle_tokens(self):
        self.set_ganons_castle_key_tokens(70)
        self.assertEqual(self.calculate_progression_skulltula_count(), 0)

    def test_max_requirement_used(self):
        self.set_rainbow_bridge_tokens(80)
        self.set_ganons_castle_key_tokens(90)

        self.assertEqual(self.calculate_progression_skulltula_count(), 0)

    def test_shuffle_all_tokens(self):
        self.shuffle_skull_tokens = ShuffleTokens.option_all
        self.assertEqual(self.calculate_progression_skulltula_count(), 50)

    def test_shuffle_overworld_tokens(self):
        self.shuffle_skull_tokens = ShuffleTokens.option_overworld
        self.assertEqual(self.calculate_progression_skulltula_count(), 6)

    def test_partial_shuffle_with_requirement(self):
        self.set_rainbow_bridge_tokens(80)
        self.shuffle_skull_tokens = ShuffleTokens.option_dungeon

        self.assertEqual(self.calculate_progression_skulltula_count(), 24)

    def test_shuffle_all_with_high_requirement(self):
        self.set_rainbow_bridge_tokens(80)
        self.shuffle_skull_tokens = ShuffleTokens.option_all

        self.assertEqual(self.calculate_progression_skulltula_count(), 80)

    def test_zero_when_requirement_fully_covered(self):
        self.set_rainbow_bridge_tokens(10)
        self.assertEqual(self.calculate_progression_skulltula_count(), 0)

    def test_caps_at_100(self):
        self.shuffle_100_gs_reward = True
        self.shuffle_skull_tokens = ShuffleTokens.option_all

        self.assertEqual(self.calculate_progression_skulltula_count(), 100)

    def test_minimal_accessibility_all_tokens(self):
        self.accessibility = Accessibility.option_minimal
        self.shuffle_skull_tokens = ShuffleTokens.option_all

        self.assertEqual(self.calculate_progression_skulltula_count(), 100)

    def test_minimal_accessibility_dungeon_tokens(self):
        self.accessibility = Accessibility.option_minimal
        self.shuffle_skull_tokens = ShuffleTokens.option_dungeon

        self.assertEqual(self.calculate_progression_skulltula_count(), TokenCounts.DUNGEON)

    def test_minimal_accessibility_overworld_tokens(self):
        self.accessibility = Accessibility.option_minimal
        self.shuffle_skull_tokens = ShuffleTokens.option_overworld

        self.assertEqual(self.calculate_progression_skulltula_count(), TokenCounts.OVERWORLD)

    def test_shuffle_count_is_ceiling_for_tokens(self):
        self.set_rainbow_bridge_tokens(100)
        self.shuffle_skull_tokens = ShuffleTokens.option_dungeon

        result = self.calculate_progression_skulltula_count()

        self.assertEqual(result, TokenCounts.DUNGEON)

    def test_no_shuffle_tokens(self):
        self.shuffle_skull_tokens = ShuffleTokens.option_off
        self.assertEqual(self.calculate_progression_skulltula_count(), 0)