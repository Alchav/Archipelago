from ..bases import SM64TestBase
from ... import Options


TTM_OPTIONS = {
    "area_rando": Options.AreaRandomizer.option_Off,
    "level_unlocks": Options.LevelUnlocks.option_full,
    "blocksanity": Options.Blocksanity.option_true,
    "buddy_checks": Options.BuddyChecks.option_true,
    "one_up_checks": Options.OneUpChecks.option_true,
    "one_up_mushroom_unlocks": Options.OneUpMushroomUnlocks.option_per_level,
    "coin_object_unlocks": Options.CoinObjectUnlocks.option_per_level,
    "enemy_unlocks": Options.EnemyUnlocks.option_per_level,
    "purple_switches": Options.PurpleSwitches.option_per_level,
    "rolling_logs": Options.RollingLogs.option_per_level,
    "tall_tall_mountain_coin_star_requirement": 1,
    "triple_jump": Options.TripleJump.option_global,
    "long_jump": Options.LongJump.option_global,
    "backflip": Options.Backflip.option_global,
    "side_flip": Options.SideFlip.option_global,
    "wall_kick": Options.WallKick.option_global,
    "dive": Options.Dive.option_global,
    "ground_pound": Options.GroundPound.option_global,
    "kick": Options.Kick.option_global,
    "climb": Options.Climb.option_global,
    "ledge_grab": Options.LedgeGrab.option_global,
}

FREESTANDING_1UPS = "Tall, Tall Mountain - Freestanding 1-Ups"
TRIGGER_1UPS = "Tall, Tall Mountain - Trigger 1-Ups"
BLOCK_1UPS = "Tall, Tall Mountain - 1-Up Blocks"
BUTTERFLIES = "Tall, Tall Mountain - Butterflies"
MONTY_MOLES = "Tall, Tall Mountain - Monty Moles"


class TestTallTallMountainLocations(SM64TestBase):
    run_default_tests = False
    options = TTM_OPTIONS

    def test_locations(self):
        upper = ["Triple Jump"]
        top = upper + ["Long Jump", "Ledge Grab"]

        self.run_location_tests([
            ["Tall, Tall Mountain - Start Edge 1-Up", False, []],
            ["Tall, Tall Mountain - Start Edge 1-Up", True, [FREESTANDING_1UPS]],

            ["Tall, Tall Mountain - Blast to the Lonely Mushroom", False, []],
            ["Tall, Tall Mountain - Blast to the Lonely Mushroom", True,
             ["Tall, Tall Mountain - Cannon Unlock"]],
            ["Tall, Tall Mountain - Bob-omb Buddy", True, []],
            ["Tall, Tall Mountain - Red Mushroom Block 1-Up", False, []],
            ["Tall, Tall Mountain - Red Mushroom Block 1-Up", True, [BLOCK_1UPS]],
            ["Tall, Tall Mountain - Red Mushroom 1-Up Block", True, []],
            ["Tall, Tall Mountain - Lower Monty Moles", False, []],
            ["Tall, Tall Mountain - Lower Monty Moles", False, [TRIGGER_1UPS]],
            ["Tall, Tall Mountain - Lower Monty Moles", True,
             [TRIGGER_1UPS, MONTY_MOLES]],

            ["Tall, Tall Mountain - Scary 'Shrooms, Red Coins", False, upper],
            ["Tall, Tall Mountain - Scary 'Shrooms, Red Coins", True,
             upper + ["Tall, Tall Mountain - Red Coins"]],
            ["Tall, Tall Mountain - Monty Mole Platform 1-Up", False, upper],
            ["Tall, Tall Mountain - Monty Mole Platform 1-Up", True,
             upper + [FREESTANDING_1UPS]],
            ["Tall, Tall Mountain - Waterfall Gap 1-Up", False, upper],
            ["Tall, Tall Mountain - Waterfall Gap 1-Up", True,
             upper + [FREESTANDING_1UPS]],
            ["Tall, Tall Mountain - Upper Monty Moles", False, upper],
            ["Tall, Tall Mountain - Upper Monty Moles", True,
             upper + [TRIGGER_1UPS, MONTY_MOLES]],

            ["Tall, Tall Mountain - Scale the Mountain", False, upper],
            ["Tall, Tall Mountain - Scale the Mountain", True, top],
            ["Tall, Tall Mountain - Mystery of the Monkey Cage", False, top],
            ["Tall, Tall Mountain - Mystery of the Monkey Cage", True,
             top + ["Tall, Tall Mountain - Ukiki"]],
            ["Tall, Tall Mountain - Mysterious Mountainside", True, top],
            ["Tall, Tall Mountain - Breathtaking View from Bridge", False, top],
            ["Tall, Tall Mountain - Breathtaking View from Bridge", True,
             top + ["Tall, Tall Mountain - Purple Switch"]],
            ["Tall, Tall Mountain - Vine Platform Butterfly 1-Up", False, top],
            ["Tall, Tall Mountain - Vine Platform Butterfly 1-Up", True,
             top + [BUTTERFLIES]],
            ["Tall, Tall Mountain - Slide Start Room Corners 1-Up", False, top],
            ["Tall, Tall Mountain - Slide Start Room Corners 1-Up", True,
             top + [TRIGGER_1UPS]],
            ["Tall, Tall Mountain - Slide Entry Ledge 1-Up", False, top],
            ["Tall, Tall Mountain - Slide Entry Ledge 1-Up", True,
             top + [FREESTANDING_1UPS]],
            ["Tall, Tall Mountain - Slide First 1-Up", False, top],
            ["Tall, Tall Mountain - Slide First 1-Up", True,
             top + [FREESTANDING_1UPS]],
            ["Tall, Tall Mountain - Slide Second 1-Up", False, top],
            ["Tall, Tall Mountain - Slide Second 1-Up", True,
             top + [FREESTANDING_1UPS]],

            ["Tall, Tall Mountain - Coins Star", False, []],
            ["Tall, Tall Mountain - Coins Star", True,
             ["Tall, Tall Mountain - Horizontal Coin Rings"]],
        ], starting_regions=["Tall, Tall Mountain"])

    def test_rolling_log_reaches_upper(self):
        self.run_location_tests([
            ["Tall, Tall Mountain - Scary 'Shrooms, Red Coins", False,
             ["Tall, Tall Mountain - Red Coins"]],
            ["Tall, Tall Mountain - Scary 'Shrooms, Red Coins", True,
             ["Tall, Tall Mountain - Rolling Log", "Tall, Tall Mountain - Red Coins"]],
        ], starting_regions=["Tall, Tall Mountain"])


class TestTallTallMountainFullLevelUnlock(SM64TestBase):
    run_default_tests = False
    options = TTM_OPTIONS

    def test_painting_unlock(self):
        route = ["Progressive Upstairs Key", FREESTANDING_1UPS]
        self.run_location_tests([
            ["Tall, Tall Mountain - Start Edge 1-Up", False, route],
            ["Tall, Tall Mountain - Start Edge 1-Up", True,
             route + ["Unlock Tall, Tall Mountain"]],
        ], starting_regions=["Menu"])


class TestTallTallMountainTopWithKickTrick(SM64TestBase):
    run_default_tests = False
    options = {
        **TTM_OPTIONS,
        "logic_tricks": {"Tall, Tall Mountain Top with Kick"},
    }

    def test_kick_reaches_top(self):
        upper = ["Tall, Tall Mountain - Rolling Log"]
        self.run_location_tests([
            ["Tall, Tall Mountain - Scale the Mountain", False, upper],
            ["Tall, Tall Mountain - Scale the Mountain", True, upper + ["Kick"]],
        ], starting_regions=["Tall, Tall Mountain"])


class TestTallTallMountainTopWithDiveTrick(SM64TestBase):
    run_default_tests = False
    options = {
        **TTM_OPTIONS,
        "logic_tricks": {"Tall, Tall Mountain Top with Dive"},
    }

    def test_dive_reaches_top(self):
        upper = ["Tall, Tall Mountain - Rolling Log"]
        self.run_location_tests([
            ["Tall, Tall Mountain - Scale the Mountain", False, upper],
            ["Tall, Tall Mountain - Scale the Mountain", True, upper + ["Dive"]],
        ], starting_regions=["Tall, Tall Mountain"])


class TestTallTallMountainLonelyMushroomFlyGuyTrick(SM64TestBase):
    run_default_tests = False
    options = {
        **TTM_OPTIONS,
        "logic_tricks": {"Tall, Tall Mountain Lonely Mushroom with Spin Jump Off of Fly Guy"},
    }

    def test_spin_jump_requires_fly_guy(self):
        self.run_location_tests([
            ["Tall, Tall Mountain - Blast to the Lonely Mushroom", False, []],
            ["Tall, Tall Mountain - Blast to the Lonely Mushroom", True,
             ["Tall, Tall Mountain - Fly Guy"]],
        ], starting_regions=["Tall, Tall Mountain"])


class TestTallTallMountainGlobalUnlockModes(SM64TestBase):
    run_default_tests = False
    options = {
        **TTM_OPTIONS,
        "coin_object_unlocks": Options.CoinObjectUnlocks.option_global,
        "enemy_unlocks": Options.EnemyUnlocks.option_global,
        "one_up_mushroom_unlocks": Options.OneUpMushroomUnlocks.option_global,
        "purple_switches": Options.PurpleSwitches.option_global,
        "rolling_logs": Options.RollingLogs.option_global,
    }

    def test_global_items_replace_per_level_items(self):
        self.run_location_tests([
            ["Tall, Tall Mountain - Coins Star", True,
             ["Tall, Tall Mountain - Horizontal Coin Rings"]],
            ["Tall, Tall Mountain - Coins Star", True, ["Horizontal Coin Rings"]],
            ["Tall, Tall Mountain - Lower Monty Moles", True,
             ["Trigger 1-Ups", "Tall, Tall Mountain - Monty Moles"]],
            ["Tall, Tall Mountain - Lower Monty Moles", True,
             ["Trigger 1-Ups", "Monty Moles"]],
            ["Tall, Tall Mountain - Scary 'Shrooms, Red Coins", True,
             ["Rolling Logs", "Red Coins"]],
        ], starting_regions=["Tall, Tall Mountain"])


class TestTallTallMountainNotShuffledUnlockModes(SM64TestBase):
    run_default_tests = False
    options = {
        **TTM_OPTIONS,
        "level_unlocks": Options.LevelUnlocks.option_disabled,
        "coin_object_unlocks": Options.CoinObjectUnlocks.option_not_shuffled,
        "enemy_unlocks": Options.EnemyUnlocks.option_not_shuffled,
        "one_up_mushroom_unlocks": Options.OneUpMushroomUnlocks.option_not_shuffled,
    }

    def test_not_shuffled_items_require_no_inventory(self):
        self.run_location_tests([
            ["Tall, Tall Mountain - Coins Star", True, []],
            ["Tall, Tall Mountain - Lower Monty Moles", True, []],
        ], starting_regions=["Tall, Tall Mountain"])
        self.run_location_tests([
            ["Tall, Tall Mountain - Start Edge 1-Up", True,
             ["Progressive Upstairs Key"]],
        ], starting_regions=["Menu"])
