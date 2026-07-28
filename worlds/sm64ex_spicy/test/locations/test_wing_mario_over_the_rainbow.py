from ..bases import SM64TestBase
from ... import Options


WMOTR_OPTIONS = {
    "area_rando": Options.AreaRandomizer.option_Off,
    "blocksanity": Options.Blocksanity.option_true,
    "buddy_checks": Options.BuddyChecks.option_true,
    "one_up_checks": Options.OneUpChecks.option_true,
    "one_up_mushroom_unlocks": Options.OneUpMushroomUnlocks.option_per_level,
    "coin_object_unlocks": Options.CoinObjectUnlocks.option_per_level,
    "enemy_unlocks": Options.EnemyUnlocks.option_per_level,
    "per_level_cap_items": Options.PerLevelCapItems.option_true,
    "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
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


class TestWingMarioOverTheRainbowLocations(SM64TestBase):
    run_default_tests = False
    options = WMOTR_OPTIONS

    def test_locations(self):
        wing_cap = ["Wing Mario Over the Rainbow - Wing Cap"]
        flight = wing_cap + ["Triple Jump"]
        cannon_route = flight + ["Wing Mario Over the Rainbow - Cannon Unlock"]

        self.run_location_tests([
            ["Wing Mario Over the Rainbow - Cloud 1-Up", False, flight],
            ["Wing Mario Over the Rainbow - Cloud 1-Up", True,
             flight + ["Wing Mario Over the Rainbow - Freestanding 1-Ups"]],
            ["Wing Mario Over the Rainbow - Cloud Across From Starting Cloud Wing Cap Block",
             False, wing_cap],
            ["Wing Mario Over the Rainbow - Cloud Across From Starting Cloud Wing Cap Block",
             True, flight],
            ["Wing Mario Over the Rainbow - Starting Cloud Wing Cap Block", False, []],
            ["Wing Mario Over the Rainbow - Starting Cloud Wing Cap Block", True, wing_cap],
            ["Wing Mario Over the Rainbow - Lowest Cloud Wing Cap Block", False, wing_cap],
            ["Wing Mario Over the Rainbow - Lowest Cloud Wing Cap Block", True, flight],

            ["Wing Mario Over the Rainbow - Bob-omb Buddy", False, wing_cap],
            ["Wing Mario Over the Rainbow - Bob-omb Buddy", True,
             flight + ["Wing Mario Over the Rainbow - Bob-omb Buddy"]],
            ["Wing Mario Over the Rainbow - Bob-omb Buddy Platform 1-Up", False, flight],
            ["Wing Mario Over the Rainbow - Bob-omb Buddy Platform 1-Up", True,
             flight + ["Wing Mario Over the Rainbow - Trigger 1-Ups"]],
            ["Wing Mario Over the Rainbow - Bob-omb Buddy Platform Wing Cap Block",
             False, ["Triple Jump"]],
            ["Wing Mario Over the Rainbow - Bob-omb Buddy Platform Wing Cap Block",
             True, flight],
            ["Wing Mario Over the Rainbow - Overlooking Bob-omb Buddy Cloud Wing Cap Block",
             False, wing_cap],
            ["Wing Mario Over the Rainbow - Overlooking Bob-omb Buddy Cloud Wing Cap Block",
             True, flight],

            ["Wing Mario Over the Rainbow - Red Coins", False, cannon_route],
            ["Wing Mario Over the Rainbow - Red Coins", True,
             cannon_route + ["Wing Mario Over the Rainbow - Red Coins"]],
            ["Wing Mario Over the Rainbow - Block 1-Up", False, cannon_route],
            ["Wing Mario Over the Rainbow - Block 1-Up", True,
             cannon_route + ["Wing Mario Over the Rainbow - 1-Up Blocks"]],
            ["Wing Mario Over the Rainbow - Hanging Pole 1-Up", False, cannon_route],
            ["Wing Mario Over the Rainbow - Hanging Pole 1-Up", True,
             cannon_route + ["Wing Mario Over the Rainbow - Freestanding 1-Ups"]],
            ["Wing Mario Over the Rainbow - Highest Cloud Wing Cap Block",
             False, flight],
            ["Wing Mario Over the Rainbow - Highest Cloud Wing Cap Block",
             True, cannon_route],
            ["Wing Mario Over the Rainbow - 1-Up Block", False, flight],
            ["Wing Mario Over the Rainbow - 1-Up Block", True, cannon_route],
        ], starting_regions=["Wing Mario Over the Rainbow"])


class TestWingMarioOverTheRainbowEntrance(SM64TestBase):
    run_default_tests = False
    options = {
        **WMOTR_OPTIONS,
        "level_unlocks": Options.LevelUnlocks.option_full,
    }

    def test_entrance_requires_third_floor_alcove_and_unlock(self):
        third_floor = ["Progressive Upstairs Key", "Progressive Upstairs Key"]
        self.run_location_tests([
            ["Wing Mario Over the Rainbow - Starting Cloud Wing Cap Block", False,
             third_floor + ["Side Flip", "Wing Mario Over the Rainbow - Wing Cap"]],
            ["Wing Mario Over the Rainbow - Starting Cloud Wing Cap Block", False, [
                *third_floor,
                "Unlock Wing Mario Over the Rainbow",
                "Wing Mario Over the Rainbow - Wing Cap",
            ]],
            ["Wing Mario Over the Rainbow - Starting Cloud Wing Cap Block", True, [
                *third_floor,
                "Side Flip",
                "Unlock Wing Mario Over the Rainbow",
                "Wing Mario Over the Rainbow - Wing Cap",
            ]],
        ], starting_regions=["Menu"])


class TestWingMarioOverTheRainbowLeapOfFaith(SM64TestBase):
    run_default_tests = False
    options = {
        **WMOTR_OPTIONS,
        "logic_tricks": {"Wing Mario Over the Rainbow Leap of Faith"},
    }

    def test_leap_of_faith_routes(self):
        leap = ["Long Jump", "Ledge Grab"]
        buddy_leap = leap + ["Wing Mario Over the Rainbow - Bob-omb Buddy"]
        self.run_location_tests([
            ["Wing Mario Over the Rainbow - Bob-omb Buddy", False, ["Long Jump"]],
            ["Wing Mario Over the Rainbow - Bob-omb Buddy", True, buddy_leap],
            ["Wing Mario Over the Rainbow - Lowest Cloud Wing Cap Block", False, ["Long Jump"]],
            ["Wing Mario Over the Rainbow - Lowest Cloud Wing Cap Block", True, leap],
            ["Wing Mario Over the Rainbow - Red Coins", False, [
                *leap,
                "Wing Mario Over the Rainbow - Wing Cap",
                "Wing Mario Over the Rainbow - Cannon Unlock",
            ]],
            ["Wing Mario Over the Rainbow - Red Coins", True, [
                *leap,
                "Wing Mario Over the Rainbow - Wing Cap",
                "Wing Mario Over the Rainbow - Cannon Unlock",
                "Wing Mario Over the Rainbow - Red Coins",
            ]],
        ], starting_regions=["Wing Mario Over the Rainbow"])


class TestWingMarioOverTheRainbowLeapWithoutLedgeGrab(SM64TestBase):
    run_default_tests = False
    options = {
        **WMOTR_OPTIONS,
        "logic_tricks": {"Wing Mario Over the Rainbow Leap of Faith Without Ledge Grab"},
    }

    def test_leap_of_faith_without_ledge_grab_routes(self):
        self.run_location_tests([
            ["Wing Mario Over the Rainbow - Bob-omb Buddy", False, []],
            ["Wing Mario Over the Rainbow - Bob-omb Buddy", True,
             ["Long Jump", "Wing Mario Over the Rainbow - Bob-omb Buddy"]],
            ["Wing Mario Over the Rainbow - Lowest Cloud Wing Cap Block", True, ["Long Jump"]],
        ], starting_regions=["Wing Mario Over the Rainbow"])
