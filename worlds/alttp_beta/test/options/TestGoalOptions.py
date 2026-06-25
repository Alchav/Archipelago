import unittest

from ...Options import DungeonsGanon, Goal


class TestGoalOptions(unittest.TestCase):
    def test_bosses_aliases_to_dungeons(self):
        goal = Goal.from_any("bosses")

        self.assertEqual(goal.value, Goal.option_dungeons)
        self.assertEqual(goal.current_key, "dungeons")

    def test_dungeons_required_default_preserves_old_bosses_goal(self):
        self.assertEqual(DungeonsGanon.from_any("default").value, 12)
