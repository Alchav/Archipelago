from ..bases import SM64TestBase
from ... import Options


CCM_OPTIONS = {
    "area_rando": Options.AreaRandomizer.option_Off,
    "blocksanity": Options.Blocksanity.option_true,
    "buddy_checks": Options.BuddyChecks.option_true,
    "one_up_checks": Options.OneUpChecks.option_true,
    "one_up_mushroom_unlocks": Options.OneUpMushroomUnlocks.option_per_level,
    "coin_object_unlocks": Options.CoinObjectUnlocks.option_per_level,
    "enemy_unlocks": Options.EnemyUnlocks.option_per_level,
    "level_features": Options.LevelFeatures.option_per_level,
        "bobomb_buddies": Options.BobombBuddies.option_per_level,
    "no_despawns": Options.NoDespawns.option_true,
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

ALL_ITEMS = ["__no_item_has_this_name__"]
FREESTANDING_1UPS = ["Cool, Cool Mountain - Freestanding 1-Ups"]
TRIGGER_1UPS = ["Cool, Cool Mountain - Trigger 1-Ups"]
BLOCK_1UPS = ["Cool, Cool Mountain - 1-Up Blocks"]


class TestCoolCoolMountainLocations(SM64TestBase):
    run_default_tests = False
    options = CCM_OPTIONS

    def test_locations(self):
        self.run_location_tests([
            ["Cool, Cool Mountain - Slip Slidin' Away", True, []],
            ["Cool, Cool Mountain - Li'l Penguin Lost", False, []],
            ["Cool, Cool Mountain - Li'l Penguin Lost", True,
             ["Cool, Cool Mountain - Baby Penguins"]],
            ["Cool, Cool Mountain - Big Penguin Race", False, []],
            ["Cool, Cool Mountain - Big Penguin Race", True,
             ["Cool, Cool Mountain - Big Penguin"]],
            ["Cool, Cool Mountain - Frosty Slide for 8 Red Coins", False, []],
            ["Cool, Cool Mountain - Frosty Slide for 8 Red Coins", True,
             ["Cool, Cool Mountain - Red Coins"]],
            ["Cool, Cool Mountain - Snowman's Lost His Head", False, []],
            ["Cool, Cool Mountain - Snowman's Lost His Head", True,
             ["Cool, Cool Mountain - Snowman's Head"]],
            ["Cool, Cool Mountain - Wall Kicks Will Work", False, []],
            ["Cool, Cool Mountain - Wall Kicks Will Work", True, ["Triple Jump"]],
            ["Cool, Cool Mountain - Bob-omb Buddy", False, []],
            ["Cool, Cool Mountain - Bob-omb Buddy", True,
             ["Cool, Cool Mountain - Bob-omb Buddy"]],

            ["Cool, Cool Mountain - Snowman Tree 1-Up", False, []],
            ["Cool, Cool Mountain - Snowman Tree 1-Up", True, TRIGGER_1UPS],
            ["Cool, Cool Mountain - Slide Shortcut First 1-Up", False, []],
            ["Cool, Cool Mountain - Slide Shortcut First 1-Up", True, FREESTANDING_1UPS],
            ["Cool, Cool Mountain - Slide Shortcut Second 1-Up", False, []],
            ["Cool, Cool Mountain - Slide Shortcut Second 1-Up", True, FREESTANDING_1UPS],

            ["Cool, Cool Mountain - Near Snowman Block 1-Up", False, []],
            ["Cool, Cool Mountain - Near Snowman Block 1-Up", True, BLOCK_1UPS],
            ["Cool, Cool Mountain - Ice Pillar Block 1-Up", False, []],
            ["Cool, Cool Mountain - Ice Pillar Block 1-Up", True, BLOCK_1UPS],
            ["Cool, Cool Mountain - Secret Slide Block 1-Up", False, []],
            ["Cool, Cool Mountain - Secret Slide Block 1-Up", True, BLOCK_1UPS],

            ["Cool, Cool Mountain - Near Snowman 1-Up Block", True, []],
            ["Cool, Cool Mountain - Ice Pillar 1-Up Block", True, []],
            ["Cool, Cool Mountain - Secret Slide 1-Up Block", True, []],

            ["Cool, Cool Mountain - Coins Star", False, []],
            ["Cool, Cool Mountain - Coins Star", True, [], ALL_ITEMS],
        ], starting_regions=["Cool, Cool Mountain"])


class TestCoolCoolMountainSpinJumpTrick(SM64TestBase):
    run_default_tests = False
    options = {
        **CCM_OPTIONS,
        "logic_tricks": {"Cool, Cool Mountain Wall Kicks Will Work With Spin Jump"},
    }

    def test_wall_kicks_will_work_with_spindrift(self):
        self.run_location_tests([
            ["Cool, Cool Mountain - Wall Kicks Will Work", False, []],
            ["Cool, Cool Mountain - Wall Kicks Will Work", True,
             ["Cool, Cool Mountain - Spindrifts"]],
        ], starting_regions=["Cool, Cool Mountain"])


class TestCoolCoolMountainImpossibleOneUpDisabled(SM64TestBase):
    run_default_tests = False
    options = {
        **CCM_OPTIONS,
        "no_despawns": Options.NoDespawns.option_false,
    }

    def test_second_slide_shortcut_is_not_created(self):
        with self.assertRaises(KeyError):
            self.multiworld.get_location(
                "Cool, Cool Mountain - Slide Shortcut Second 1-Up", self.player)
