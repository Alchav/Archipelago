from ..bases import SM64TestBase
from ... import Options


LLL_OPTIONS = {
    "area_rando": Options.AreaRandomizer.option_Off,
    "blocksanity": Options.Blocksanity.option_true,
    "coin_object_unlocks": Options.CoinObjectUnlocks.option_per_level,
    "enemy_unlocks": Options.EnemyUnlocks.option_per_level,
    "lethal_lava_land_coin_star_requirement": 133,
    "one_up_checks": Options.OneUpChecks.option_true,
    "one_up_mushroom_unlocks": Options.OneUpMushroomUnlocks.option_per_level,
    "per_level_cap_items": Options.PerLevelCapItems.option_true,
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


class TestLethalLavaLandLocations(SM64TestBase):
    run_default_tests = False
    options = LLL_OPTIONS

    def test_locations(self):
        freestanding = ["Lethal Lava Land - Freestanding 1-Ups"]

        self.run_location_tests([
            ["Lethal Lava Land - Boil the Big Bully", False, []],
            ["Lethal Lava Land - Boil the Big Bully", True,
             ["Lethal Lava Land - Big Bullies"]],
            ["Lethal Lava Land - Bully the Bullies", False,
             ["Lethal Lava Land - Big Bullies"]],
            ["Lethal Lava Land - Bully the Bullies", True, [
                "Lethal Lava Land - Big Bullies",
                "Lethal Lava Land - Bullies",
            ]],

            ["Lethal Lava Land - 8-Coin Puzzle with 15 Pieces", False,
             ["Lethal Lava Land - Bowser Puzzle"]],
            ["Lethal Lava Land - 8-Coin Puzzle with 15 Pieces", False,
             ["Lethal Lava Land - Red Coins"]],
            ["Lethal Lava Land - 8-Coin Puzzle with 15 Pieces", True, [
                "Lethal Lava Land - Bowser Puzzle",
                "Lethal Lava Land - Red Coins",
            ]],

            ["Lethal Lava Land - Red-Hot Log Rolling", False, []],
            ["Lethal Lava Land - Red-Hot Log Rolling", True,
             ["Lethal Lava Land - Rolling Log"]],

            ["Lethal Lava Land - Hot-Foot-It into the Volcano", False, []],
            ["Lethal Lava Land - Hot-Foot-It into the Volcano", True, ["Climb"]],
            ["Lethal Lava Land - Elevator Tour in the Volcano", False, ["Climb"]],
            ["Lethal Lava Land - Elevator Tour in the Volcano", True, [
                "Climb",
                "Lethal Lava Land - Checkerboard Platforms",
            ]],

            ["Lethal Lava Land - Flamethrower Ring 1-Up", False, []],
            ["Lethal Lava Land - Flamethrower Ring 1-Up", True,
             ["Lethal Lava Land - Trigger 1-Ups"]],
            ["Lethal Lava Land - Volcano Flamethrower 1-Up", False, []],
            ["Lethal Lava Land - Volcano Flamethrower 1-Up", True, freestanding],
            ["Lethal Lava Land - Volcano Curve 1-Up", False, []],
            ["Lethal Lava Land - Volcano Curve 1-Up", True, freestanding],
            ["Lethal Lava Land - Volcano Brown Platform 1-Up", False, []],
            ["Lethal Lava Land - Volcano Brown Platform 1-Up", True, freestanding],

            ["Lethal Lava Land - Northeast Brown Platform 1-Up", False, freestanding],
            ["Lethal Lava Land - Northeast Brown Platform 1-Up", True,
             freestanding + ["Lethal Lava Land - Koopa Shell"]],
            ["Lethal Lava Land - Boil the Big Bully Star Lava 1-Up", False, freestanding],
            ["Lethal Lava Land - Boil the Big Bully Star Lava 1-Up", True,
             freestanding + ["Lethal Lava Land - Koopa Shell"]],
            ["Lethal Lava Land - Northwest Curve 1-Up", False, freestanding],
            ["Lethal Lava Land - Northwest Curve 1-Up", True,
             freestanding + ["Lethal Lava Land - Koopa Shell"]],

            ["Lethal Lava Land - Volcano Pole 1-Up", False,
             ["Lethal Lava Land - Trigger 1-Ups"]],
            ["Lethal Lava Land - Volcano Pole 1-Up", True, [
                "Climb",
                "Lethal Lava Land - Trigger 1-Ups",
            ]],

            ["Lethal Lava Land - Wing Cap Block", False, []],
            ["Lethal Lava Land - Wing Cap Block", True,
             ["Lethal Lava Land - Wing Cap"]],
            ["Lethal Lava Land - Koopa Shell Block", False, []],
            ["Lethal Lava Land - Koopa Shell Block", True,
             ["Lethal Lava Land - Koopa Shell"]],

            ["Lethal Lava Land - Coins Star", False, [],
             ["Lethal Lava Land - Red Coins"]],
            ["Lethal Lava Land - Coins Star", True, [], ALL_ITEMS],
        ], starting_regions=["Lethal Lava Land"])


class TestLethalLavaLandLavaDamageBoosting(SM64TestBase):
    run_default_tests = False
    options = {
        **LLL_OPTIONS,
        "logic_tricks": {"Lava Damage Boosting"},
    }

    def test_lava_damage_boosting_routes(self):
        freestanding = ["Lethal Lava Land - Freestanding 1-Ups"]
        self.run_location_tests([
            ["Lethal Lava Land - Red-Hot Log Rolling", True, []],
            ["Lethal Lava Land - Northeast Brown Platform 1-Up", True, freestanding],
            ["Lethal Lava Land - Boil the Big Bully Star Lava 1-Up", True, freestanding],
            ["Lethal Lava Land - Northwest Curve 1-Up", True, freestanding],
            ["Lethal Lava Land - 8-Coin Puzzle with 15 Pieces", False,
             ["Lethal Lava Land - Red Coins"]],
            ["Lethal Lava Land - 8-Coin Puzzle with 15 Pieces", True, [
                "Lethal Lava Land - Red Coins",
                "Lethal Lava Land - Horizontal Coin Lines",
            ]],
        ], starting_regions=["Lethal Lava Land"])


class TestLethalLavaLandHotFootWallKick(SM64TestBase):
    run_default_tests = False
    options = {
        **LLL_OPTIONS,
        "logic_tricks": {"Lethal Lava Land Hot-Foot it Into the Volcano With Wall Kick"},
    }

    def test_route(self):
        self.run_location_tests([
            ["Lethal Lava Land - Hot-Foot-It into the Volcano", False, []],
            ["Lethal Lava Land - Hot-Foot-It into the Volcano", True, ["Wall Kick"]],
        ], starting_regions=["Lethal Lava Land"])


class TestLethalLavaLandHotFootTripleJump(SM64TestBase):
    run_default_tests = False
    options = {
        **LLL_OPTIONS,
        "logic_tricks": {"Lethal Lava Land Hot-Foot it Into the Volcano With Triple Jump"},
    }

    def test_route(self):
        self.run_location_tests([
            ["Lethal Lava Land - Hot-Foot-It into the Volcano", False, []],
            ["Lethal Lava Land - Hot-Foot-It into the Volcano", True, ["Triple Jump"]],
        ], starting_regions=["Lethal Lava Land"])


class TestLethalLavaLandHotFootSideFlip(SM64TestBase):
    run_default_tests = False
    options = {
        **LLL_OPTIONS,
        "logic_tricks": {"Lethal Lava Land Hot-Foot it Into the Volcano With Side Flip"},
    }

    def test_route(self):
        self.run_location_tests([
            ["Lethal Lava Land - Hot-Foot-It into the Volcano", False, []],
            ["Lethal Lava Land - Hot-Foot-It into the Volcano", True, ["Side Flip"]],
        ], starting_regions=["Lethal Lava Land"])


class TestLethalLavaLandHotFootBackflip(SM64TestBase):
    run_default_tests = False
    options = {
        **LLL_OPTIONS,
        "logic_tricks": {"Lethal Lava Land Hot-Foot it Into the Volcano With Backflip"},
    }

    def test_route(self):
        self.run_location_tests([
            ["Lethal Lava Land - Hot-Foot-It into the Volcano", False, []],
            ["Lethal Lava Land - Hot-Foot-It into the Volcano", True, ["Backflip"]],
        ], starting_regions=["Lethal Lava Land"])


class TestLethalLavaLandHotFootNoMovement(SM64TestBase):
    run_default_tests = False
    options = {
        **LLL_OPTIONS,
        "logic_tricks": {"Lethal Lava Land Hot-Foot it Into the Volcano With No Movement Abilities"},
    }

    def test_route(self):
        self.run_location_tests([
            ["Lethal Lava Land - Hot-Foot-It into the Volcano", True, []],
        ], starting_regions=["Lethal Lava Land"])


class TestLethalLavaLandElevatorTricks(SM64TestBase):
    run_default_tests = False
    options = {
        **LLL_OPTIONS,
        "logic_tricks": {
            "Lethal Lava Land Hot-Foot it Into the Volcano With No Movement Abilities",
            "Lethal Lava Land Long Jump From Hot-Foot-It into the Volcano to Elevator Tour in the Volcano",
            "Lethal Lava Land Triple Jump or Dive From Hot-Foot-It into the Volcano to Elevator Tour in the Volcano",
        },
    }

    def test_long_jump_route(self):
        self.run_location_tests([
            ["Lethal Lava Land - Elevator Tour in the Volcano", False, []],
            ["Lethal Lava Land - Elevator Tour in the Volcano", True, ["Long Jump"]],
        ], starting_regions=["Lethal Lava Land"])

    def test_triple_jump_or_dive_route_still_requires_climb(self):
        for movement in ("Triple Jump", "Dive"):
            self.run_location_tests([
                ["Lethal Lava Land - Elevator Tour in the Volcano", False, [movement]],
                ["Lethal Lava Land - Elevator Tour in the Volcano", True,
                 [movement, "Climb"]],
            ], starting_regions=["Lethal Lava Land"])
