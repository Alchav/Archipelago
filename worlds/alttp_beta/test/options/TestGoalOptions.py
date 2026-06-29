import unittest

from test.general import setup_multiworld
from ... import ALTTPWorld
from ...Options import DungeonsGanon, Goal


class TestGoalOptions(unittest.TestCase):
    def test_bosses_aliases_to_dungeons(self):
        goal = Goal.from_any("bosses")

        self.assertEqual(goal.value, Goal.option_dungeons)
        self.assertEqual(goal.current_key, "dungeons")

    def test_dungeons_required_default_preserves_old_bosses_goal(self):
        self.assertEqual(DungeonsGanon.from_any("default").value, 12)

    def test_triforce_hunt_total_matches_effective_piece_count(self):
        multiworld = setup_multiworld(
            ALTTPWorld,
            ("generate_early", "create_regions", "create_items"),
            seed=0,
            options={
                "goal": "ganon_triforce_hunt",
                "triforce_pieces_mode": "available",
                "triforce_pieces_required": 48,
                "triforce_pieces_available": 31,
            },
        )

        self.assertEqual(multiworld.worlds[1].treasure_hunt_required, 48)
        self.assertEqual(multiworld.worlds[1].treasure_hunt_total, 48)
        self.assertEqual(sum(item.name == "Triforce Piece" for item in multiworld.itempool), 48)
