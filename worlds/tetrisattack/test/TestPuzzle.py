from worlds.tetrisattack.Options import StarterPack, PuzzleMode, PuzzleGoal, VersusGoal
from worlds.tetrisattack.test import TetrisAttackTestBase


class TestPuzzleIncremental(TetrisAttackTestBase):
    options = {
        "stage_clear_goal": False,
        "puzzle_goal": PuzzleGoal.option_puzzle,
        "versus_goal": VersusGoal.option_no_vs,
        "puzzle_mode": PuzzleMode.option_incremental,
        "starter_pack": StarterPack.option_puzzle_level_1,
        "puzzle_filler": 0
    }

    def test_incremental_unlocks(self) -> None:
        locations = ["Puzzle 3-10 Clear"]
        items = [["Puzzle Level 3 Gate",
                  "Puzzle Progressive Level 3 Unlock",
                  "Puzzle Progressive Level 3 Unlock",
                  "Puzzle Progressive Level 3 Unlock",
                  "Puzzle Progressive Level 3 Unlock",
                  "Puzzle Progressive Level 3 Unlock",
                  "Puzzle Progressive Level 3 Unlock",
                  "Puzzle Progressive Level 3 Unlock",
                  "Puzzle Progressive Level 3 Unlock",
                  "Puzzle Progressive Level 3 Unlock"]]
        self.assertAccessDependency(locations, items, only_check_listed=True)


class TestPuzzleWholeLevels(TetrisAttackTestBase):
    options = {
        "stage_clear_goal": False,
        "puzzle_goal": PuzzleGoal.option_puzzle,
        "versus_goal": VersusGoal.option_no_vs,
        "puzzle_mode": PuzzleMode.option_whole_levels,
        "starter_pack": StarterPack.option_puzzle_level_1,
        "puzzle_filler": 0
    }


class TestPuzzleAndExtraPuzzleIndividualStages(TetrisAttackTestBase):
    options = {
        "stage_clear_goal": False,
        "puzzle_goal": PuzzleGoal.option_puzzle_and_extra_puzzle,
        "versus_goal": VersusGoal.option_no_vs,
        "puzzle_mode": PuzzleMode.option_individual_stages,
        "starter_pack": StarterPack.option_puzzle_level_2,
        "puzzle_filler": 0
    }


class TestPuzzleSkippableStages(TetrisAttackTestBase):
    options = {
        "stage_clear_goal": False,
        "puzzle_goal": PuzzleGoal.option_puzzle,
        "versus_goal": VersusGoal.option_no_vs,
        "puzzle_mode": PuzzleMode.option_skippable,
        "starter_pack": StarterPack.option_puzzle_level_3,
        "puzzle_filler": 0
    }


class TestPuzzleSkippableStagesWithLevelGates(TetrisAttackTestBase):
    options = {
        "stage_clear_goal": False,
        "puzzle_goal": PuzzleGoal.option_puzzle,
        "versus_goal": VersusGoal.option_no_vs,
        "puzzle_mode": PuzzleMode.option_skippable_with_level_gate,
        "starter_pack": StarterPack.option_puzzle_level_4,
        "puzzle_filler": 0
    }


class TestExtraPuzzle(TetrisAttackTestBase):
    options = {
        "stage_clear_goal": False,
        "puzzle_goal": PuzzleGoal.option_extra_puzzle,
        "versus_goal": VersusGoal.option_no_vs,
        "starter_pack": StarterPack.option_puzzle_level_1,
        "puzzle_filler": 0
    }

    def test_extra_start(self) -> None:
        self.assertTrue(self.count("Extra Puzzle Level 1 Gate") > 0,
                        "Starter Pack did not give access to Extra Puzzle level")


class TestPuzzleAndExtraPuzzle(TetrisAttackTestBase):
    options = {
        "stage_clear_goal": False,
        "puzzle_goal": PuzzleGoal.option_puzzle_and_extra_puzzle,
        "versus_goal": VersusGoal.option_no_vs,
        "starter_pack": StarterPack.option_puzzle_level_1,
        "puzzle_filler": 0
    }


class TestPuzzleOrExtraPuzzle(TetrisAttackTestBase):
    options = {
        "stage_clear_goal": False,
        "puzzle_goal": PuzzleGoal.option_puzzle_or_extra_puzzle,
        "versus_goal": VersusGoal.option_no_vs,
        "starter_pack": StarterPack.option_puzzle_level_1,
        "puzzle_filler": 0
    }


class TestPuzzleMaxFiller(TetrisAttackTestBase):
    options = {
        "stage_clear_goal": False,
        "puzzle_goal": PuzzleGoal.option_puzzle,
        "versus_goal": VersusGoal.option_no_vs,
        "starter_pack": StarterPack.option_puzzle_level_5,
        "puzzle_mode": PuzzleMode.option_whole_levels,
        "puzzle_filler": 1
    }
