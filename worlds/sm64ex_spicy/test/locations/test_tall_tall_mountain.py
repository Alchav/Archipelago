from ..bases import SM64TestBase
from ... import Options


TTM_OPTIONS = {
    "area_rando": Options.AreaRandomizer.option_Off,
    "level_unlocks": Options.LevelUnlocks.option_full,
    "blocksanity": Options.Blocksanity.option_true,
    "buddy_checks": Options.BuddyChecks.option_true,
    "one_up_checks": Options.OneUpChecks.option_true,
    "one_up_unlocks": Options.OneUpUnlocks.option_per_level,
    "coin_object_unlocks": Options.CoinObjectUnlocks.option_per_level,
    "enemy_unlocks": Options.EnemyUnlocks.option_per_level,
    "level_features": Options.LevelFeatures.option_per_level,
        "bobomb_buddies": Options.BobombBuddies.option_per_level,
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
MIDDLE = ["Tall, Tall Mountain - Vertical Wind"]


class TestTallTallMountainLocations(SM64TestBase):
    run_default_tests = False
    options = TTM_OPTIONS

    def test_mysterious_mountainside_is_at_the_slide_exit(self):
        location = self.multiworld.get_location(
            "Tall, Tall Mountain - Mysterious Mountainside", self.player)
        self.assertEqual(
            location.parent_region.name,
            "Tall, Tall Mountain - Slide Exit Alcove",
        )
        self.assertTrue(any(
            entrance.connected_region.name == "Tall, Tall Mountain"
            for entrance in location.parent_region.exits
        ))

        self.run_location_tests([
            ["Tall, Tall Mountain - Mysterious Mountainside", True, []],
        ], starting_regions=["Tall, Tall Mountain - Slide Exit Alcove"])

    def test_locations(self):
        upper = MIDDLE + ["Triple Jump", "Ledge Grab"]
        top = upper + ["Long Jump"]

        self.run_location_tests([
            ["Tall, Tall Mountain - Start Edge 1-Up", False, []],
            ["Tall, Tall Mountain - Start Edge 1-Up", True, [FREESTANDING_1UPS]],

            ["Tall, Tall Mountain - Blast to the Lonely Mushroom", False, []],
            ["Tall, Tall Mountain - Blast to the Lonely Mushroom", True,
             MIDDLE + ["Tall, Tall Mountain - Cannon Unlock"]],
            ["Tall, Tall Mountain - Bob-omb Buddy", False, []],
            ["Tall, Tall Mountain - Bob-omb Buddy", True,
             MIDDLE + ["Tall, Tall Mountain - Bob-omb Buddy"]],
            ["Tall, Tall Mountain - Red Mushroom Block 1-Up", False, []],
            ["Tall, Tall Mountain - Red Mushroom Block 1-Up", True, MIDDLE + [BLOCK_1UPS]],
            ["Tall, Tall Mountain - Red Mushroom 1-Up Block", True, MIDDLE + [BLOCK_1UPS]],
            ["Tall, Tall Mountain - Lower Monty Moles", False, []],
            ["Tall, Tall Mountain - Lower Monty Moles", False, [TRIGGER_1UPS]],
            ["Tall, Tall Mountain - Lower Monty Moles", True, MIDDLE + [MONTY_MOLES]],

            ["Tall, Tall Mountain - Scary 'Shrooms, Red Coins", False, upper],
            ["Tall, Tall Mountain - Scary 'Shrooms, Red Coins", True,
             upper + ["Tall, Tall Mountain - Red Coins"]],
            ["Tall, Tall Mountain - Upper Vine Wall 1-Up", False, upper],
            ["Tall, Tall Mountain - Upper Vine Wall 1-Up", True,
             upper + [FREESTANDING_1UPS]],
            ["Tall, Tall Mountain - Waterfall Gap 1-Up", False, upper],
            ["Tall, Tall Mountain - Waterfall Gap 1-Up", True,
             upper + [FREESTANDING_1UPS]],
            ["Tall, Tall Mountain - Upper Monty Moles", False, upper],
            ["Tall, Tall Mountain - Upper Monty Moles", True,
             upper + [MONTY_MOLES]],

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
             MIDDLE + ["Tall, Tall Mountain - Rolling Log", "Tall, Tall Mountain - Red Coins"]],
        ], starting_regions=["Tall, Tall Mountain"])

    def test_triple_jump_requires_ledge_grab_to_reach_upper(self):
        self.run_location_tests([
            ["Tall, Tall Mountain - Scary 'Shrooms, Red Coins", False,
             ["Triple Jump", "Tall, Tall Mountain - Red Coins"]],
            ["Tall, Tall Mountain - Scary 'Shrooms, Red Coins", True,
             ["Triple Jump", "Ledge Grab", "Tall, Tall Mountain - Red Coins"]],
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
        ], starting_regions=["Castle Grounds"])


class TestTallTallMountainTopWithKickTrick(SM64TestBase):
    run_default_tests = False
    options = {
        **TTM_OPTIONS,
        "logic_tricks": {"Tall, Tall Mountain Top with Kick"},
    }

    def test_kick_reaches_top(self):
        upper = MIDDLE + ["Tall, Tall Mountain - Rolling Log"]
        self.run_location_tests([
            ["Tall, Tall Mountain - Scale the Mountain", False, upper],
            ["Tall, Tall Mountain - Scale the Mountain", True, upper + ["Kick"]],
        ], starting_regions=["Tall, Tall Mountain"])


class TestTallTallMountainUpperFlyGuySpinJumpTrick(SM64TestBase):
    run_default_tests = False
    options = {
        **TTM_OPTIONS,
        "logic_tricks": {"Tall, Tall Mountain Upper Region with Spin Jump Off of Fly Guy"},
    }

    def test_spin_jump_reaches_upper_and_requires_fly_guy(self):
        route = MIDDLE + [FREESTANDING_1UPS]
        self.run_location_tests([
            ["Tall, Tall Mountain - Upper Vine Wall 1-Up", False, route],
            ["Tall, Tall Mountain - Upper Vine Wall 1-Up", True,
             route + ["Tall, Tall Mountain - Fly Guy"]],
        ], starting_regions=["Tall, Tall Mountain"])


class TestTallTallMountainBreathtakingViewTripleJumpTrick(SM64TestBase):
    run_default_tests = False
    options = {
        **TTM_OPTIONS,
        "logic_tricks": {
            "Tall, Tall Mountain Breathtaking View from Bridge with Triple Jump from Below"
        },
    }

    def test_triple_jump_from_upper_reaches_star(self):
        upper = MIDDLE + ["Tall, Tall Mountain - Rolling Log"]
        self.run_location_tests([
            ["Tall, Tall Mountain - Breathtaking View from Bridge", False, upper],
            ["Tall, Tall Mountain - Breathtaking View from Bridge", True,
             upper + ["Triple Jump"]],
        ], starting_regions=["Tall, Tall Mountain"])


class TestTallTallMountainTopWithDiveTrick(SM64TestBase):
    run_default_tests = False
    options = {
        **TTM_OPTIONS,
        "logic_tricks": {"Tall, Tall Mountain Top with Dive"},
    }

    def test_dive_reaches_top(self):
        upper = MIDDLE + ["Tall, Tall Mountain - Rolling Log"]
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
             MIDDLE + ["Tall, Tall Mountain - Fly Guy"]],
        ], starting_regions=["Tall, Tall Mountain"])


class TestTallTallMountainGlobalUnlockModes(SM64TestBase):
    run_default_tests = False
    options = {
        **TTM_OPTIONS,
        "coin_object_unlocks": Options.CoinObjectUnlocks.option_global,
        "enemy_unlocks": Options.EnemyUnlocks.option_global,
        "one_up_unlocks": Options.OneUpUnlocks.option_global,
        "level_features": Options.LevelFeatures.option_global,
        "bobomb_buddies": Options.BobombBuddies.option_global,
    }

    def test_global_items_replace_per_level_items(self):
        self.run_location_tests([
            ["Tall, Tall Mountain - Coins Star", True,
             ["Tall, Tall Mountain - Horizontal Coin Rings"]],
            ["Tall, Tall Mountain - Coins Star", True, ["Horizontal Coin Rings"]],
            ["Tall, Tall Mountain - Lower Monty Moles", True,
             ["Vertical Wind", "Monty Moles"]],
            ["Tall, Tall Mountain - Scary 'Shrooms, Red Coins", True,
             ["Vertical Wind", "Rolling Logs", "Red Coins"]],
        ], starting_regions=["Tall, Tall Mountain"])


class TestTallTallMountainNotShuffledUnlockModes(SM64TestBase):
    run_default_tests = False
    options = {
        **TTM_OPTIONS,
        "level_unlocks": Options.LevelUnlocks.option_disabled,
        "coin_object_unlocks": Options.CoinObjectUnlocks.option_not_shuffled,
        "enemy_unlocks": Options.EnemyUnlocks.option_not_shuffled,
        "one_up_unlocks": Options.OneUpUnlocks.option_not_shuffled,
        "level_features": Options.LevelFeatures.option_not_shuffled,
    }

    def test_not_shuffled_items_require_no_inventory(self):
        self.run_location_tests([
            ["Tall, Tall Mountain - Coins Star", True, []],
            ["Tall, Tall Mountain - Lower Monty Moles", True, []],
        ], starting_regions=["Tall, Tall Mountain"])
        self.run_location_tests([
            ["Tall, Tall Mountain - Start Edge 1-Up", True,
             ["Progressive Upstairs Key"]],
        ], starting_regions=["Castle Grounds"])
