from ..bases import SM64TestBase
from ... import Options


SECRET_STAGE_OPTIONS = {
    "area_rando": Options.AreaRandomizer.option_Off,
    "blocksanity": Options.Blocksanity.option_true,
    "one_up_checks": Options.OneUpChecks.option_true,
    "one_up_unlocks": Options.OneUpUnlocks.option_per_level,
    "coin_object_unlocks": Options.CoinObjectUnlocks.option_per_level,
    "enemy_unlocks": Options.EnemyUnlocks.option_per_level,
    "level_features": Options.LevelFeatures.option_per_level,
        "bobomb_buddies": Options.BobombBuddies.option_per_level,
    "cap_items": Options.CapItems.option_per_level,
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


class TestPrincessSecretSlideLocations(SM64TestBase):
    run_default_tests = False
    options = SECRET_STAGE_OPTIONS

    def test_locations(self):
        self.run_location_tests([
            ["The Princess's Secret Slide - Block Star", True, []],
            ["The Princess's Secret Slide - Fast", True, []],
            ["The Princess's Secret Slide - Coin Triggers 1-Up", False, []],
            ["The Princess's Secret Slide - Coin Triggers 1-Up", True,
             ["The Princess's Secret Slide - Trigger 1-Ups"]],
            ["The Princess's Secret Slide - Slide 1-Up", False, []],
            ["The Princess's Secret Slide - Slide 1-Up", True,
             ["The Princess's Secret Slide - Freestanding 1-Ups"]],
            ["The Princess's Secret Slide - Star Block", True, []],
        ], starting_regions=["The Princess's Secret Slide"])


class TestSecretAquariumLocations(SM64TestBase):
    run_default_tests = False
    options = SECRET_STAGE_OPTIONS

    def test_locations(self):
        self.run_location_tests([
            ["The Secret Aquarium - Red Coins", False, []],
            ["The Secret Aquarium - Red Coins", True, ["Secret Aquarium - Red Coins"]],
            ["The Secret Aquarium - Center Coin Ring 1-Up", False, []],
            ["The Secret Aquarium - Center Coin Ring 1-Up", True,
             ["The Secret Aquarium - Trigger 1-Ups"]],
        ], starting_regions=["The Secret Aquarium"])


class TestTowerOfTheWingCapLocations(SM64TestBase):
    run_default_tests = False
    options = SECRET_STAGE_OPTIONS

    def test_locations(self):
        self.run_location_tests([
            ["Tower of the Wing Cap - Switch", True, []],
            ["Tower of the Wing Cap - Red Coins", False, []],
            ["Tower of the Wing Cap - Red Coins", True, ["Tower of the Wing Cap - Red Coins"]],
            ["Tower of the Wing Cap - Wing Cap Block", False, []],
            ["Tower of the Wing Cap - Wing Cap Block", True, ["Tower of the Wing Cap - Wing Cap"]],
        ], starting_regions=["Tower of the Wing Cap"])


class TestCavernOfTheMetalCapLocations(SM64TestBase):
    run_default_tests = False
    options = SECRET_STAGE_OPTIONS

    def test_locations(self):
        metal_cap = ["Cavern of the Metal Cap - Metal Cap"]
        self.run_location_tests([
            ["Cavern of the Metal Cap - Switch", True, []],
            ["Cavern of the Metal Cap - Red Coins", False,
             ["Cavern of the Metal Cap - Red Coins"]],
            ["Cavern of the Metal Cap - Red Coins", False, metal_cap],
            ["Cavern of the Metal Cap - Red Coins", True,
             metal_cap + ["Cavern of the Metal Cap - Red Coins"]],
            ["Cavern of the Metal Cap - Block 1-Up", False, []],
            ["Cavern of the Metal Cap - Block 1-Up", True,
             ["Cavern of the Metal Cap - 1-Up Blocks"]],
            ["Cavern of the Metal Cap - Alcove 1-Up", False, []],
            ["Cavern of the Metal Cap - Alcove 1-Up", True,
             ["Cavern of the Metal Cap - Freestanding 1-Ups"]],
            ["Cavern of the Metal Cap - First Metal Cap Block", False, []],
            ["Cavern of the Metal Cap - First Metal Cap Block", True, metal_cap],
            ["Cavern of the Metal Cap - 1-Up Block", True,
             ["Cavern of the Metal Cap - 1-Up Blocks"]],
            ["Cavern of the Metal Cap - Near Switch Metal Cap Block", False, []],
            ["Cavern of the Metal Cap - Near Switch Metal Cap Block", True, metal_cap],
        ], starting_regions=["Cavern of the Metal Cap"])


class TestCavernOfTheMetalCapTrick(SM64TestBase):
    run_default_tests = False
    options = {
        **SECRET_STAGE_OPTIONS,
        "logic_tricks": {"Deep Underwater Coins Without Metal Cap"},
    }

    def test_deep_underwater_red_coins_without_metal_cap(self):
        self.run_location_tests([
            ["Cavern of the Metal Cap - Red Coins", False, []],
            ["Cavern of the Metal Cap - Red Coins", True,
             ["Cavern of the Metal Cap - Red Coins"]],
        ], starting_regions=["Cavern of the Metal Cap"])


class TestVanishCapUnderTheMoatLocations(SM64TestBase):
    run_default_tests = False
    options = SECRET_STAGE_OPTIONS

    def test_locations(self):
        checkerboards = ["Vanish Cap Under the Moat - Checkerboard Platforms"]
        vanish_cap = ["Vanish Cap Under the Moat - Vanish Cap"]
        movement = ["Wall Kick"]
        red_coins = ["Vanish Cap Under the Moat - Red Coins"]

        self.run_location_tests([
            ["Vanish Cap Under the Moat - Switch", False, checkerboards],
            ["Vanish Cap Under the Moat - Switch", False, movement],
            ["Vanish Cap Under the Moat - Switch", True, checkerboards + movement],

            ["Vanish Cap Under the Moat - Red Coins", False,
             checkerboards + movement + vanish_cap],
            ["Vanish Cap Under the Moat - Red Coins", False,
             checkerboards + movement + red_coins],
            ["Vanish Cap Under the Moat - Red Coins", True,
             checkerboards + movement + vanish_cap + red_coins],
            ["Vanish Cap Under the Moat - Block 1-Up", False, []],
            ["Vanish Cap Under the Moat - Block 1-Up", True,
             ["Vanish Cap Under the Moat - 1-Up Blocks"]],

            ["Vanish Cap Under the Moat - Upper Platform 1-Up", False, []],
            ["Vanish Cap Under the Moat - Upper Platform 1-Up", True,
             ["Vanish Cap Under the Moat - Freestanding 1-Ups"]],
            ["Vanish Cap Under the Moat - Lower Platform 1-Up", False, []],
            ["Vanish Cap Under the Moat - Lower Platform 1-Up", True,
             ["Vanish Cap Under the Moat - Freestanding 1-Ups"]],
            ["Vanish Cap Under the Moat - Red Coin Platform 1-Up", False,
             checkerboards + movement + vanish_cap],
            ["Vanish Cap Under the Moat - Red Coin Platform 1-Up", False,
             checkerboards + movement + ["Vanish Cap Under the Moat - Trigger 1-Ups"]],
            ["Vanish Cap Under the Moat - Red Coin Platform 1-Up", True,
             checkerboards + movement + vanish_cap + ["Vanish Cap Under the Moat - Trigger 1-Ups"]],

            ["Vanish Cap Under the Moat - Bottom of Slide Vanish Cap Block", False, []],
            ["Vanish Cap Under the Moat - Bottom of Slide Vanish Cap Block", True, vanish_cap],
            ["Vanish Cap Under the Moat - 1-Up Block", True,
             ["Vanish Cap Under the Moat - 1-Up Blocks"]],
            ["Vanish Cap Under the Moat - 3 Coins Block", False, ["Ledge Grab"]],
            ["Vanish Cap Under the Moat - 3 Coins Block", False,
             ["Vanish Cap Under the Moat - 3-Coin Block"]],
            ["Vanish Cap Under the Moat - 3 Coins Block", True,
             ["Ledge Grab", "Vanish Cap Under the Moat - 3-Coin Block"]],
            ["Vanish Cap Under the Moat - Near Switch Vanish Cap Block", False,
             checkerboards + vanish_cap],
            ["Vanish Cap Under the Moat - Near Switch Vanish Cap Block", True,
             checkerboards + vanish_cap + movement],
        ], starting_regions=["Vanish Cap Under the Moat"])


class TestSecretStageEntrances(SM64TestBase):
    run_default_tests = False
    options = {
        **SECRET_STAGE_OPTIONS,
        "level_features": Options.LevelFeatures.option_per_level,
        "bobomb_buddies": Options.BobombBuddies.option_per_level,
    }

    def test_entrance_requirements(self):
        self.run_location_tests([
            ["The Princess's Secret Slide - Fast", True, []],
            ["The Secret Aquarium - Red Coins", False, ["Secret Aquarium - Red Coins"]],
            ["The Secret Aquarium - Red Coins", True,
             ["Side Flip", "Secret Aquarium - Red Coins"]],
            ["Tower of the Wing Cap - Switch", False, []],
            ["Tower of the Wing Cap - Switch", True, ["Unlock Tower of the Wing Cap"]],
            ["Cavern of the Metal Cap - Switch", False, ["Progressive Basement Key"]],
            ["Cavern of the Metal Cap - Switch", True, [
                "Progressive Basement Key",
                "Hazy Maze Cave - Swimming Beast",
            ]],
            ["Vanish Cap Under the Moat - Upper Platform 1-Up", False,
             ["Vanish Cap Under the Moat - Freestanding 1-Ups"]],
            ["Vanish Cap Under the Moat - Upper Platform 1-Up", True, [
                "Unlock Vanish Cap Under the Moat",
                "Vanish Cap Under the Moat - Freestanding 1-Ups",
            ]],
        ], starting_regions=["Castle Grounds"])


class TestVanishCapUnderTheMoatWallKickTrick(SM64TestBase):
    run_default_tests = False
    options = {
        **SECRET_STAGE_OPTIONS,
        "logic_tricks": {"Vanish Cap Under the Moat Wall Kick over the Vanish Cap Grate"},
    }

    def test_wall_kick_bypasses_vanish_cap(self):
        route = [
            "Vanish Cap Under the Moat - Checkerboard Platforms",
            "Wall Kick",
        ]
        self.run_location_tests([
            ["Vanish Cap Under the Moat - Red Coins", False, route],
            ["Vanish Cap Under the Moat - Red Coins", True,
             route + ["Vanish Cap Under the Moat - Red Coins"]],
            ["Vanish Cap Under the Moat - Red Coin Platform 1-Up", True,
             route + ["Vanish Cap Under the Moat - Trigger 1-Ups"]],
        ], starting_regions=["Vanish Cap Under the Moat"])


class TestVanishCapUnderTheMoatDropTrick(SM64TestBase):
    run_default_tests = False
    options = {
        **SECRET_STAGE_OPTIONS,
        "logic_tricks": {"Vanish Cap Under the Moat Drop to Checkerboard Platforms From Above"},
    }

    def test_drop_bypasses_movement(self):
        route = [
            "Vanish Cap Under the Moat - Checkerboard Platforms",
            "Vanish Cap Under the Moat - Vanish Cap",
        ]
        self.run_location_tests([
            ["Vanish Cap Under the Moat - Red Coins", False, route],
            ["Vanish Cap Under the Moat - Red Coins", False,
             route + ["Vanish Cap Under the Moat - Red Coins"]],
            ["Vanish Cap Under the Moat - Red Coin Platform 1-Up", True,
             route + ["Vanish Cap Under the Moat - Trigger 1-Ups"]],
        ], starting_regions=["Vanish Cap Under the Moat"])


class TestVanishCapUnderTheMoatCrawlBackTrick(SM64TestBase):
    run_default_tests = False
    options = {
        **SECRET_STAGE_OPTIONS,
        "logic_tricks": {
            "Vanish Cap Under the Moat Drop to Checkerboard Platforms From Above After Crawling Back Up the Slide"
        },
    }

    def test_crawl_back_bypasses_movement(self):
        self.run_location_tests([
            ["Vanish Cap Under the Moat - Red Coins", True, [
                "Vanish Cap Under the Moat - Checkerboard Platforms",
                "Vanish Cap Under the Moat - Vanish Cap",
                "Vanish Cap Under the Moat - Red Coins",
            ]],
        ], starting_regions=["Vanish Cap Under the Moat"])
