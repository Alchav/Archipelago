from ..bases import SM64TestBase
from ... import Options


BOWSER_STAGE_OPTIONS = {
    "area_rando": Options.AreaRandomizer.option_Off,
    "blocksanity": Options.Blocksanity.option_true,
    "one_up_checks": Options.OneUpChecks.option_true,
    "one_up_mushroom_unlocks": Options.OneUpMushroomUnlocks.option_per_level,
    "bowser_stage_1ups": Options.BowserStage1Ups.option_per_level,
    "bowser_bombs": Options.BowserBombs.option_per_level,
    "bowser_in_the_dark_world_health": 2,
    "bowser_in_the_fire_sea_health": 2,
    "bowser_in_the_sky_health": 2,
    "coin_object_unlocks": Options.CoinObjectUnlocks.option_per_level,
    "enemy_unlocks": Options.EnemyUnlocks.option_per_level,
    "level_features": Options.LevelFeatures.option_per_level,
        "bobomb_buddies": Options.BobombBuddies.option_per_level,
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


class TestBowserInTheDarkWorldLocations(SM64TestBase):
    run_default_tests = False
    options = BOWSER_STAGE_OPTIONS

    def test_locations(self):
        purple_switch = ["Bowser in the Dark World - Purple Switch"]
        red_coins = ["Bowser in the Dark World - Red Coins"]
        bombs = [
            "Bowser in the Dark World - Progressive Bowser Arena Bomb",
            "Bowser in the Dark World - Progressive Bowser Arena Bomb",
        ]
        freestanding = ["Bowser in the Dark World - Freestanding 1-Ups"]
        extra = ["Bowser in the Dark World - Extra 1-Ups"]

        self.run_location_tests([
            ["Bowser in the Dark World - Red Coins", False, purple_switch],
            ["Bowser in the Dark World - Red Coins", False, red_coins],
            ["Bowser in the Dark World - Red Coins", True, purple_switch + red_coins],
            ["Bowser in the Dark World - Key", False, purple_switch],
            ["Bowser in the Dark World - Key", False, purple_switch + bombs[:1]],
            ["Bowser in the Dark World - Key", True, purple_switch + bombs],

            ["Bowser in the Dark World - Tower Block 1-Up", False, []],
            ["Bowser in the Dark World - Tower Block 1-Up", True,
             ["Bowser in the Dark World - 1-Up Blocks"]],
            ["Bowser in the Dark World - Near Goombas Block 1-Up", False, []],
            ["Bowser in the Dark World - Near Goombas Block 1-Up", True,
             ["Bowser in the Dark World - 1-Up Blocks"]],

            ["Bowser in the Dark World - Center Overhang 1-Up", False, freestanding],
            ["Bowser in the Dark World - Center Overhang 1-Up", False, extra],
            ["Bowser in the Dark World - Center Overhang 1-Up", True, freestanding + extra],
            ["Bowser in the Dark World - Right Tilting Platform Base 1-Up", False, []],
            ["Bowser in the Dark World - Right Tilting Platform Base 1-Up", True, freestanding],
            ["Bowser in the Dark World - Left Tilting Platform Base 1-Up", False, freestanding],
            ["Bowser in the Dark World - Left Tilting Platform Base 1-Up", True, freestanding + extra],
            ["Bowser in the Dark World - Far Overhang 1-Up", False, freestanding],
            ["Bowser in the Dark World - Far Overhang 1-Up", True, freestanding + extra],

            ["Bowser in the Dark World - Metal Cap Block", False, []],
            ["Bowser in the Dark World - Metal Cap Block", True,
             ["Bowser in the Dark World - Metal Cap"]],
            ["Bowser in the Dark World - 3 Coins Block", False, []],
            ["Bowser in the Dark World - 3 Coins Block", True,
             ["Bowser in the Dark World - 3-Coin Block"]],
            ["Bowser in the Dark World - Tower 1-Up Block", True, []],
            ["Bowser in the Dark World - Near Goombas 1-Up Block", True, []],
        ], starting_regions=["Bowser in the Dark World"])


class TestBowserInTheDarkWorldSlopeTrick(SM64TestBase):
    run_default_tests = False
    options = {
        **BOWSER_STAGE_OPTIONS,
        "logic_tricks": {"Bowser in the Dark World Triple Jump up the Purple Switch Slope"},
    }

    def test_trick_reaches_bowser_but_not_red_coin_star(self):
        trick_route = [
            "Triple Jump",
            "Bowser in the Dark World - Progressive Bowser Arena Bomb",
            "Bowser in the Dark World - Progressive Bowser Arena Bomb",
        ]
        self.run_location_tests([
            ["Bowser in the Dark World - Key", False, trick_route[:-1]],
            ["Bowser in the Dark World - Key", True, trick_route],
            ["Bowser in the Dark World - Red Coins", False,
             trick_route + ["Bowser in the Dark World - Red Coins"]],
        ], starting_regions=["Bowser in the Dark World"])


class TestBowserInTheFireSeaLocations(SM64TestBase):
    run_default_tests = False
    options = BOWSER_STAGE_OPTIONS

    def test_locations(self):
        upper = ["Climb"]
        near_poles = upper + ["Ledge Grab"]
        bombs = [
            "Bowser in the Fire Sea - Progressive Bowser Arena Bomb",
            "Bowser in the Fire Sea - Progressive Bowser Arena Bomb",
        ]
        freestanding = ["Bowser in the Fire Sea - Freestanding 1-Ups"]
        triggers = ["Bowser in the Fire Sea - Trigger 1-Ups"]
        extra = ["Bowser in the Fire Sea - Extra 1-Ups"]

        self.run_location_tests([
            ["Bowser in the Fire Sea - First Stone Structure 1-Up", False, []],
            ["Bowser in the Fire Sea - First Stone Structure 1-Up", True, freestanding],
            ["Bowser in the Fire Sea - Second Stone Structure 1-Up", False, freestanding],
            ["Bowser in the Fire Sea - Second Stone Structure 1-Up", False, extra],
            ["Bowser in the Fire Sea - Second Stone Structure 1-Up", True, freestanding + extra],
            ["Bowser in the Fire Sea - 3 Coins Block", False, []],
            ["Bowser in the Fire Sea - 3 Coins Block", True,
             ["Bowser in the Fire Sea - 3-Coin Block"]],

            ["Bowser in the Fire Sea - Red Coins", True, upper + ["Bowser in the Fire Sea - Red Coins"]],
            ["Bowser in the Fire Sea - Red Coins", False, near_poles],
            ["Bowser in the Fire Sea - Key", False, upper + bombs[:1]],
            ["Bowser in the Fire Sea - Key", True, upper + bombs],

            ["Bowser in the Fire Sea - Swaying Stairs Block 1-Up", False, upper],
            ["Bowser in the Fire Sea - Swaying Stairs Block 1-Up", True,
             upper + ["Bowser in the Fire Sea - 1-Up Blocks"]],
            ["Bowser in the Fire Sea - Near Poles Block 1-Up", False,
             near_poles],
            ["Bowser in the Fire Sea - Near Poles Block 1-Up", True,
             near_poles + ["Bowser in the Fire Sea - 1-Up Blocks"]],
            ["Bowser in the Fire Sea - Elevator Pole 1-Up", False, upper],
            ["Bowser in the Fire Sea - Elevator Pole 1-Up", True, upper + triggers],
            ["Bowser in the Fire Sea - Stretching Platform Trigger 1-Up", False, upper],
            ["Bowser in the Fire Sea - Stretching Platform Trigger 1-Up", True, upper + triggers],
            ["Bowser in the Fire Sea - Near Poles 1-Up", False,
             near_poles + freestanding],
            ["Bowser in the Fire Sea - Near Poles 1-Up", False,
             near_poles + extra],
            ["Bowser in the Fire Sea - Near Poles 1-Up", True,
             near_poles + freestanding + extra],
            ["Bowser in the Fire Sea - Swaying Stairs 1-Up Block", False, []],
            ["Bowser in the Fire Sea - Swaying Stairs 1-Up Block", True, upper],
            ["Bowser in the Fire Sea - 10 Coins Block", False, upper],
            ["Bowser in the Fire Sea - 10 Coins Block", True,
             upper + ["Bowser in the Fire Sea - 10-Coin Block"]],
            ["Bowser in the Fire Sea - Near Poles 1-Up Block", True, upper],
        ], starting_regions=["Bowser in the Fire Sea"])


class TestBowserInTheSkyLocations(SM64TestBase):
    run_default_tests = False
    options = BOWSER_STAGE_OPTIONS

    def test_locations(self):
        freestanding = ["Bowser in the Sky - Freestanding 1-Ups"]
        trigger = ["Bowser in the Sky - Trigger 1-Ups"]
        chuckya = ["Side Flip"]
        arrow_ride = chuckya + ["Bowser in the Sky - Purple Switch"]
        top = arrow_ride + ["Climb"]

        self.run_location_tests([
            ["Bowser in the Sky - Block 1-Up", False, []],
            ["Bowser in the Sky - Block 1-Up", True,
             ["Bowser in the Sky - 1-Up Blocks"]],
            ["Bowser in the Sky - 1-Up Block", True, []],
            ["Bowser in the Sky - Before Tilting Platform 1-Up", False, []],
            ["Bowser in the Sky - Before Tilting Platform 1-Up", True, freestanding],
            ["Bowser in the Sky - Ferris Wheel 1-Up", False, []],
            ["Bowser in the Sky - Ferris Wheel 1-Up", True, freestanding],

            ["Bowser in the Sky - Spark Pole Coins 1-Up", False, arrow_ride],
            ["Bowser in the Sky - Spark Pole Coins 1-Up", True, arrow_ride + trigger],
            ["Bowser in the Sky - Arrow Ride 1-Up", False, chuckya + freestanding],
            ["Bowser in the Sky - Arrow Ride 1-Up", False,
             ["Bowser in the Sky - Purple Switch", *freestanding]],
            ["Bowser in the Sky - Arrow Ride 1-Up", True, arrow_ride + freestanding],

            ["Bowser in the Sky - Red Coins", False, top],
            ["Bowser in the Sky - Red Coins", True,
             top + ["Bowser in the Sky - Red Coins"]],
            ["Bowser in the Sky - Final Platform 1-Up", False, arrow_ride + freestanding],
            ["Bowser in the Sky - Final Platform 1-Up", True, top + freestanding],
        ], starting_regions=["Bowser in the Sky"])


class TestBowserStageEntrances(SM64TestBase):
    run_default_tests = False
    options = BOWSER_STAGE_OPTIONS

    def test_entrance_requirements(self):
        self.run_location_tests([
            ["Bowser in the Dark World - Right Tilting Platform Base 1-Up", False,
             ["Bowser in the Dark World - Freestanding 1-Ups"]],
            ["Bowser in the Dark World - Right Tilting Platform Base 1-Up", True, [
                "Dark World Key",
                "Bowser in the Dark World - Freestanding 1-Ups",
            ]],
            ["Bowser in the Fire Sea - First Stone Structure 1-Up", False, [
                "Progressive Basement Key",
                "Unlock Bowser in the Fire Sea",
                "Bowser in the Fire Sea - Freestanding 1-Ups",
            ]],
            ["Bowser in the Fire Sea - First Stone Structure 1-Up", False, [
                "Progressive Basement Key",
                "Progressive Basement Key",
                "Bowser in the Fire Sea - Freestanding 1-Ups",
            ]],
            ["Bowser in the Fire Sea - First Stone Structure 1-Up", True, [
                "Progressive Basement Key",
                "Progressive Basement Key",
                "Unlock Bowser in the Fire Sea",
                "Bowser in the Fire Sea - Freestanding 1-Ups",
            ]],
            ["Bowser in the Sky - Before Tilting Platform 1-Up", False, [
                "Progressive Upstairs Key",
                "Progressive Upstairs Key",
                "Bowser in the Sky - Freestanding 1-Ups",
            ]],
            ["Bowser in the Sky - Before Tilting Platform 1-Up", True, [
                "Progressive Upstairs Key",
                "Progressive Upstairs Key",
                "Progressive Upstairs Key",
                "Bowser in the Sky - Freestanding 1-Ups",
            ]],
        ], starting_regions=["Menu"])
