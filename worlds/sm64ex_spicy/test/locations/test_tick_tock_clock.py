from ..bases import SM64TestBase
from ... import Options


SHUFFLED_TTC_OPTIONS = {
    "area_rando": Options.AreaRandomizer.option_Off,
    "blocksanity": Options.Blocksanity.option_true,
    "one_up_checks": Options.OneUpChecks.option_true,
    "one_up_unlocks": Options.OneUpUnlocks.option_not_shuffled,
    "coin_object_unlocks": Options.CoinObjectUnlocks.option_per_level,
    "enemy_unlocks": Options.EnemyUnlocks.option_per_level,
    "level_features": Options.LevelFeatures.option_per_level,
        "bobomb_buddies": Options.BobombBuddies.option_per_level,
    "triple_jump": Options.TripleJump.option_global,
    "long_jump": Options.LongJump.option_global,
    "backflip": Options.Backflip.option_global,
    "side_flip": Options.SideFlip.option_global,
    "wall_kick": Options.WallKick.option_global,
    "climb": Options.Climb.option_global,
    "ledge_grab": Options.LedgeGrab.option_global,
}

LOWER = ["Ledge Grab"]
MID = LOWER + ["Climb"]
TOP = MID + ["Triple Jump"]
PAST_SPINNERS = TOP
ALL_ITEMS = ["__no_item_has_this_name__"]


class TestTickTockClockMovingLocations(SM64TestBase):
    run_default_tests = False
    options = SHUFFLED_TTC_OPTIONS

    def test_locations(self):
        self.run_location_tests([
            ["Tick Tock Clock - Below Red Coin Spinners 10 Coins Block", False, []],
            ["Tick Tock Clock - Below Red Coin Spinners 10 Coins Block", True,
             ["Tick Tock Clock - 10-Coin Blocks"]],
            ["Tick Tock Clock - First Pendulum 3 Coins Block", False, []],
            ["Tick Tock Clock - First Pendulum 3 Coins Block", True,
             ["Tick Tock Clock - 3-Coin Blocks"]],

            ["Tick Tock Clock - Roll into the Cage", False, []],
            ["Tick Tock Clock - Roll into the Cage", True, LOWER],
            ["Tick Tock Clock - Get a Hand", False, []],
            ["Tick Tock Clock - Get a Hand", True, LOWER],
            ["Tick Tock Clock - Above Red Coin Spinners 3 Coins Block", False, LOWER],
            ["Tick Tock Clock - Above Red Coin Spinners 3 Coins Block", True,
             LOWER + ["Tick Tock Clock - 3-Coin Blocks"]],
            ["Tick Tock Clock - Stop Time for Red Coins", False, PAST_SPINNERS],
            ["Tick Tock Clock - Stop Time for Red Coins", True,
             PAST_SPINNERS + ["Tick Tock Clock - Spinners", "Tick Tock Clock - Red Coins"]],

            ["Tick Tock Clock - The Pit and the Pendulums", False, LOWER],
            ["Tick Tock Clock - The Pit and the Pendulums", True, MID],
            ["Tick Tock Clock - Heave-ho First 3 Coins Block", False, MID],
            ["Tick Tock Clock - Heave-ho First 3 Coins Block", True,
             MID + ["Tick Tock Clock - 3-Coin Blocks"]],
            ["Tick Tock Clock - Heave-ho Second 3 Coins Block", False, MID],
            ["Tick Tock Clock - Heave-ho Second 3 Coins Block", True,
             MID + ["Tick Tock Clock - 3-Coin Blocks"]],

            ["Tick Tock Clock - Timed Jumps on Moving Bars", False, LOWER],
            ["Tick Tock Clock - Timed Jumps on Moving Bars", True, MID],
            ["Tick Tock Clock - Pole 1-Up", False, LOWER],
            ["Tick Tock Clock - Pole 1-Up", True, MID],
            ["Tick Tock Clock - Moving Bars Platform 1-Up", False, LOWER],
            ["Tick Tock Clock - Moving Bars Platform 1-Up", True, MID],
            ["Tick Tock Clock - Above Timed Jumps on Moving Bars 3 Coins Block", False, MID],
            ["Tick Tock Clock - Above Timed Jumps on Moving Bars 3 Coins Block", True,
             MID + ["Tick Tock Clock - 3-Coin Blocks"]],
            ["Tick Tock Clock - Above Four Moving Bars 10 Coins Block", False, MID],
            ["Tick Tock Clock - Above Four Moving Bars 10 Coins Block", True,
             MID + ["Tick Tock Clock - 10-Coin Blocks"]],

            ["Tick Tock Clock - Midway Up Block 1-Up", True, PAST_SPINNERS],
            ["Tick Tock Clock - Midway Up 1-Up Block", True, PAST_SPINNERS],
            ["Tick Tock Clock - Past Three Spinners 3 Coins Block", False, TOP],
            ["Tick Tock Clock - Past Three Spinners 3 Coins Block", True,
             PAST_SPINNERS + ["Tick Tock Clock - 3-Coin Blocks"]],

            ["Tick Tock Clock - Stomp on the Thwomp", False, PAST_SPINNERS],
            ["Tick Tock Clock - Stomp on the Thwomp", True,
             PAST_SPINNERS + ["Tick Tock Clock - Thwomp"]],
            ["Tick Tock Clock - Top Block 1-Up", True, PAST_SPINNERS],
            ["Tick Tock Clock - Top 1-Up Block", True, PAST_SPINNERS],
            ["Tick Tock Clock - Top Clock Hand 10 Coins Block", False, PAST_SPINNERS],
            ["Tick Tock Clock - Top Clock Hand 10 Coins Block", True,
             PAST_SPINNERS + ["Tick Tock Clock - 10-Coin Blocks"]],
            ["Tick Tock Clock - Top Central Platform 10 Coins Block", False, PAST_SPINNERS],
            ["Tick Tock Clock - Top Central Platform 10 Coins Block", True,
             PAST_SPINNERS + ["Tick Tock Clock - 10-Coin Blocks"]],
            ["Tick Tock Clock - Beneath the Thwomp 10 Coins Block", False, PAST_SPINNERS],
            ["Tick Tock Clock - Beneath the Thwomp 10 Coins Block", True,
             PAST_SPINNERS + ["Tick Tock Clock - 10-Coin Blocks"]],

            ["Tick Tock Clock - Coins Star", False, []],
            ["Tick Tock Clock - Coins Star", True, [], ALL_ITEMS],
        ], starting_regions=["Tick Tock Clock Moving"])

    def test_top_past_spinners_location_placement(self):
        for location_name in (
                "Tick Tock Clock - Midway Up Block 1-Up",
                "Tick Tock Clock - Midway Up 1-Up Block",
                "Tick Tock Clock - Past Three Spinners 3 Coins Block"):
            with self.subTest(location=location_name):
                location = self.multiworld.get_location(location_name, self.player)
                self.assertEqual(
                    "Tick Tock Clock - Top Past Spinners",
                    location.parent_region.name)

    def test_moving_time_and_side_flip_reach_top(self):
        self.run_location_tests([
            ["Tick Tock Clock - Midway Up Block 1-Up", True,
             ["Side Flip", "Climb"]],
        ], starting_regions=["Tick Tock Clock Moving"])


class TestTickTockClockStoppedLocations(SM64TestBase):
    run_default_tests = False
    options = SHUFFLED_TTC_OPTIONS

    def test_stomp_on_the_thwomp_is_out_of_logic(self):
        self.run_location_tests([
            ["Tick Tock Clock - Stomp on the Thwomp", False,
             [
                 "Tick Tock Clock - Spinners",
                 "Climb",
                 "Wall Kick",
                 "Triple Jump",
                 "Ledge Grab",
                 "Tick Tock Clock - Thwomp",
             ]],
        ], starting_regions=["Tick Tock Clock Stopped"])


class TestTickTockClockTopPastSpinnersWallKickTrick(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_TTC_OPTIONS,
        "logic_tricks": {"Tick Tock Clock Top Past Spinners with Wall Kick"},
    }

    def test_wall_kick_reaches_top_and_past_spinners(self):
        self.run_location_tests([
            ["Tick Tock Clock - Midway Up Block 1-Up", True, ["Wall Kick"]],
        ], starting_regions=["Tick Tock Clock - Moving Bars Area"])


class TestTickTockClockWallKickStompTrick(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_TTC_OPTIONS,
        "logic_tricks": {"Tick Tock Clock Stomp on the Thwomp with Wall Kick"},
    }

    def test_wall_kick_and_thwomp_do_not_require_moving_time(self):
        self.run_location_tests([
            ["Tick Tock Clock - Stomp on the Thwomp", False,
             ["Tick Tock Clock - Thwomp"]],
            ["Tick Tock Clock - Stomp on the Thwomp", False, ["Wall Kick"]],
            ["Tick Tock Clock - Stomp on the Thwomp", True,
             ["Wall Kick", "Tick Tock Clock - Thwomp"]],
        ], starting_regions=["Tick Tock Clock - Top Past Spinners"])


class TestTickTockClockCombinedStompTricks(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_TTC_OPTIONS,
        "logic_tricks": {
            "Tick Tock Clock Triple Jump and Wall Kick to Stomp the Thwomp without Thwomp",
            "Tick Tock Clock Stomp on the Thwomp with Wall Kick",
        },
    }

    def test_combined_tricks_require_neither_thwomp_nor_moving_time(self):
        self.run_location_tests([
            ["Tick Tock Clock - Stomp on the Thwomp", False, ["Wall Kick"]],
            ["Tick Tock Clock - Stomp on the Thwomp", False, ["Triple Jump"]],
            ["Tick Tock Clock - Stomp on the Thwomp", True,
             ["Triple Jump", "Wall Kick"]],
        ], starting_regions=["Tick Tock Clock - Top Past Spinners"])


class TestTickTockClockStompTrick(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_TTC_OPTIONS,
        "logic_tricks": {"Tick Tock Clock Triple Jump and Wall Kick to Stomp the Thwomp without Thwomp"},
    }

    def test_stomp_on_the_thwomp_trick(self):
        route = [
            "Ledge Grab",
            "Climb",
            "Triple Jump",
            "Tick Tock Clock - Spinners",
        ]
        self.run_location_tests([
            ["Tick Tock Clock - Stomp on the Thwomp", False, route],
            ["Tick Tock Clock - Stomp on the Thwomp", True, route + ["Wall Kick"]],
        ], starting_regions=["Tick Tock Clock Moving"])

        self.run_location_tests([
            ["Tick Tock Clock - Stomp on the Thwomp", False, route + ["Wall Kick"]],
        ], starting_regions=["Tick Tock Clock Stopped"])
