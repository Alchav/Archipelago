from BaseClasses import ItemClassification

from ..bases import SM64TestBase
from ... import Options
from ...Items import global_enemy_item_data_table, per_level_enemy_item_data_table


SSL_OPTIONS = {
        "blocksanity": Options.Blocksanity.option_true,
    "buddy_checks": Options.BuddyChecks.option_true,
    "coin_object_unlocks": Options.CoinObjectUnlocks.option_per_level,
    "enemy_unlocks": Options.EnemyUnlocks.option_per_level,
    "one_up_checks": Options.OneUpChecks.option_true,
    "one_up_unlocks": Options.OneUpUnlocks.option_per_level,
    "cap_items": Options.CapItems.option_per_level,
    "shifting_sand_land_coin_star_requirement": 136,
    "level_features": Options.LevelFeatures.option_per_level,
        "bobomb_buddies": Options.BobombBuddies.option_per_level,
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

ALL_ITEMS = ["__all_items_except_nothing__"]


class TestShiftingSandLandLocations(SM64TestBase):
    run_default_tests = False
    options = SSL_OPTIONS

    def test_locations(self):
        block_mushroom = ["Shifting Sand Land - 1-Up Blocks"]
        freestanding = ["Shifting Sand Land - Freestanding 1-Ups"]
        upper = ["Climb"]

        self.run_location_tests([
            ["Shifting Sand Land - In the Talons of the Big Bird", False, []],
            ["Shifting Sand Land - In the Talons of the Big Bird", True,
             ["Shifting Sand Land - Klepto with Star"]],
            ["Shifting Sand Land - Shining Atop the Pyramid", True, []],

            ["Shifting Sand Land - Inside the Ancient Pyramid", False, []],
            ["Shifting Sand Land - Inside the Ancient Pyramid", False, upper],
            ["Shifting Sand Land - Inside the Ancient Pyramid", True, upper + ["Side Flip"]],
            ["Shifting Sand Land - Inside the Ancient Pyramid", True, upper + ["Wall Kick"]],
            ["Shifting Sand Land - Pyramid Puzzle", False, []],
            ["Shifting Sand Land - Pyramid Puzzle", True, upper],

            ["Shifting Sand Land - Stand Tall on the Four Pillars", False, [
                "Climb",
                "Shifting Sand Land - Pyramid Elevator",
            ]],
            ["Shifting Sand Land - Stand Tall on the Four Pillars", False, [
                "Climb",
                "Shifting Sand Land - Pyramid Elevator",
                "Shifting Sand Land - Eyerok",
            ]],

            ["Shifting Sand Land - Free Flying for 8 Red Coins", False, [
                "Triple Jump",
                "Shifting Sand Land - Wing Cap",
            ]],
            ["Shifting Sand Land - Free Flying for 8 Red Coins", True, [
                "Triple Jump",
                "Shifting Sand Land - Wing Cap",
                "Shifting Sand Land - Red Coins",
            ]],

            ["Shifting Sand Land - Bob-omb Buddy", False, []],
            ["Shifting Sand Land - Bob-omb Buddy", True,
             ["Shifting Sand Land - Bob-omb Buddy"]],

            ["Shifting Sand Land - Outside Pyramid Block 1-Up", False, []],
            ["Shifting Sand Land - Outside Pyramid Block 1-Up", True, block_mushroom],
            ["Shifting Sand Land - Pyramid Left Path Block 1-Up", False, []],
            ["Shifting Sand Land - Pyramid Left Path Block 1-Up", True, block_mushroom],
            ["Shifting Sand Land - Pyramid Back Block 1-Up", False, []],
            ["Shifting Sand Land - Pyramid Back Block 1-Up", True, block_mushroom],

            ["Shifting Sand Land - Oasis Tree 1-Up", False,
             ["Shifting Sand Land - Trigger 1-Ups"]],
            ["Shifting Sand Land - Oasis Tree 1-Up", True, [
                "Side Flip",
                "Shifting Sand Land - Trigger 1-Ups",
            ]],
            ["Shifting Sand Land - Near Quicksand Pits 1-Up", False, []],
            ["Shifting Sand Land - Near Quicksand Pits 1-Up", True, freestanding],
            ["Shifting Sand Land - Above Quicksand Pit 1-Up", False, freestanding],
            ["Shifting Sand Land - Above Quicksand Pit 1-Up", True,
             freestanding + ["Long Jump"]],

            ["Shifting Sand Land - Pyramid Platform Triggers 1-Up", False,
             ["Shifting Sand Land - Trigger 1-Ups"]],
            ["Shifting Sand Land - Pyramid Platform Triggers 1-Up", True,
             upper + ["Shifting Sand Land - Trigger 1-Ups"]],
            ["Shifting Sand Land - Pyramid Grindel 1-Up", False, freestanding],
            ["Shifting Sand Land - Pyramid Grindel 1-Up", True, [
                "Shifting Sand Land - Grindel",
                "Shifting Sand Land - Freestanding 1-Ups",
            ]],
            ["Shifting Sand Land - Pyramid Above the First Wire Grid 1-Up", False, freestanding],
            ["Shifting Sand Land - Pyramid Above the First Wire Grid 1-Up", True,
             freestanding + ["Climb"]],

            ["Shifting Sand Land - Outside Pyramid Wing Cap Block", False, []],
            ["Shifting Sand Land - Outside Pyramid Wing Cap Block", True,
             ["Shifting Sand Land - Wing Cap"]],
            ["Shifting Sand Land - Outside Pyramid 1-Up Block", True, block_mushroom],

            ["Shifting Sand Land - Stone Structure Koopa Shell Block", False, []],
            ["Shifting Sand Land - Stone Structure Koopa Shell Block", True, [
                "Triple Jump",
                "Shifting Sand Land - Koopa Shell Block",
            ]],
            ["Shifting Sand Land - Stone Structure Wing Cap Block", False, ["Triple Jump"]],
            ["Shifting Sand Land - Stone Structure Wing Cap Block", True, [
                "Triple Jump",
                "Shifting Sand Land - Wing Cap",
            ]],
            ["Shifting Sand Land - Cannon Wing Cap Block", False, []],
            ["Shifting Sand Land - Cannon Wing Cap Block", True,
             ["Shifting Sand Land - Wing Cap"]],
            ["Shifting Sand Land - Pyramid Left Path 1-Up Block", True, block_mushroom],
            ["Shifting Sand Land - Pyramid Back 1-Up Block", True, block_mushroom],

            ["Shifting Sand Land - Coins Star", False, [],
             ["Shifting Sand Land - Red Coins"]],
            ["Shifting Sand Land - Coins Star", True, [], ALL_ITEMS],
        ], starting_regions=["Shifting Sand Land"])


class TestShiftingSandLandStoneStructureTrick(SM64TestBase):
    run_default_tests = False
    options = {
        **SSL_OPTIONS,
        "logic_tricks": {"Shifting Sand Land Top of Stone Structure with Spin Jump or Tweesters"},
    }

    def test_shy_guy_bounce(self):
        self.run_location_tests([
            ["Shifting Sand Land - Stone Structure Koopa Shell Block", False, []],
            ["Shifting Sand Land - Stone Structure Koopa Shell Block", True,
             ["Shifting Sand Land - Fly Guys", "Shifting Sand Land - Koopa Shell Block"]],
        ], starting_regions=["Shifting Sand Land"])

    def test_tweester_route(self):
        self.run_location_tests([
            ["Shifting Sand Land - Stone Structure Koopa Shell Block", False,
             ["Shifting Sand Land - Koopa Shell Block"]],
            ["Shifting Sand Land - Stone Structure Koopa Shell Block", True, [
                "Shifting Sand Land - Tweesters",
                "Shifting Sand Land - Koopa Shell Block",
            ]],
        ], starting_regions=["Shifting Sand Land"])

    def test_tweesters_are_progression_when_trick_is_enabled(self):
        self.assertEqual(
            self.world.get_item_classification(
                per_level_enemy_item_data_table["Shifting Sand Land - Tweesters"]),
            ItemClassification.progression_deprioritized_skip_balancing,
        )


class TestShiftingSandLandRedCoinTricks(SM64TestBase):
    run_default_tests = False
    options = {
        **SSL_OPTIONS,
        "logic_tricks": {
            "Shifting Sand Land Three Red Coins with Tweesters",
            "Shifting Sand Land One Red Coin with Spin Jump",
        },
    }

    def test_red_coin_star_route(self):
        self.run_location_tests([
            ["Shifting Sand Land - Free Flying for 8 Red Coins", False,
             ["Shifting Sand Land - Red Coins"]],
            ["Shifting Sand Land - Free Flying for 8 Red Coins", True, [
                "Shifting Sand Land - Red Coins",
                "Shifting Sand Land - Fly Guys",
                "Shifting Sand Land - Tweesters",
            ]],
        ], starting_regions=["Shifting Sand Land"])

    def test_tweesters_are_progression_when_the_trick_is_enabled(self):
        for item_name, item_data in (
                ("Shifting Sand Land - Tweesters",
                 per_level_enemy_item_data_table["Shifting Sand Land - Tweesters"]),
        ):
            with self.subTest(item=item_name):
                self.assertEqual(
                    self.world.get_item_classification(item_data),
                    ItemClassification.progression_deprioritized_skip_balancing)


class TestShiftingSandLandPillarShellTrick(SM64TestBase):
    run_default_tests = False
    options = {
        **SSL_OPTIONS,
        "logic_tricks": {"Shifting Sand Land Pillars with Koopa Shell"},
    }

    def test_upper_pyramid_route(self):
        self.run_location_tests([
            ["Shifting Sand Land - Inside the Ancient Pyramid", False, ["Triple Jump"]],
            ["Shifting Sand Land - Inside the Ancient Pyramid", True, [
                "Triple Jump",
                "Shifting Sand Land - Koopa Shell Block",
                "Shifting Sand Land - Pyramid Elevator",
            ]],
        ], starting_regions=["Shifting Sand Land"])


class TestShiftingSandLandPillarSideFlipOrKickTrick(SM64TestBase):
    run_default_tests = False
    options = {
        **SSL_OPTIONS,
        "logic_tricks": {"Shifting Sand Land Pillars with Side Flip or Kick"},
    }

    def test_upper_pyramid_routes(self):
        for movement in ("Side Flip", "Kick"):
            self.run_location_tests([
                ["Shifting Sand Land - Inside the Ancient Pyramid", False, [movement]],
                ["Shifting Sand Land - Inside the Ancient Pyramid", True, [
                    movement,
                    "Shifting Sand Land - Pyramid Elevator",
                ]],
            ], starting_regions=["Shifting Sand Land"])


class TestShiftingSandLandInteriorRoutes(SM64TestBase):
    run_default_tests = False
    options = SSL_OPTIONS

    def test_lower_pyramid_to_upper_pyramid_routes(self):
        self.run_location_tests([
            ["Shifting Sand Land - Pyramid Puzzle", False,
             ["Shifting Sand Land - Pyramid Elevator"]],
            ["Shifting Sand Land - Pyramid Puzzle", True, ["Climb"]],
            ["Shifting Sand Land - Inside the Ancient Pyramid", False, ["Climb"]],
            ["Shifting Sand Land - Inside the Ancient Pyramid", True, ["Climb", "Side Flip"]],
        ], starting_regions=["Shifting Sand Land - Pyramid"])

    def test_top_entry_elevator_route(self):
        self.run_location_tests([
            ["Shifting Sand Land - Pyramid Puzzle", False, []],
            ["Shifting Sand Land - Inside the Ancient Pyramid", True,
             ["Shifting Sand Land - Pyramid Elevator"]],
            ["Shifting Sand Land - Stand Tall on the Four Pillars", False,
             ["Shifting Sand Land - Pyramid Elevator"]],
            ["Shifting Sand Land - Stand Tall on the Four Pillars", True, [
                "Shifting Sand Land - Pyramid Elevator",
                "Shifting Sand Land - Eyerok",
            ]],
        ], starting_regions=["Shifting Sand Land - Pyramid Top Entry"])


class TestShiftingSandLandStandTallTrick(SM64TestBase):
    run_default_tests = False
    options = {
        **SSL_OPTIONS,
        "logic_tricks": {"Shifting Sand Land Stand Tall on the Four Pyramids Without Pyramid Elevator"},
    }

    def test_route_without_elevator(self):
        self.run_location_tests([
            ["Shifting Sand Land - Stand Tall on the Four Pillars", False,
             ["Shifting Sand Land - Eyerok"]],
            ["Shifting Sand Land - Stand Tall on the Four Pillars", True, [
                "Shifting Sand Land - Eyerok",
                "Ledge Grab",
            ]],
        ], starting_regions=["Shifting Sand Land"])
