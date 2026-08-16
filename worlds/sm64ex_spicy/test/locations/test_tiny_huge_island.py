from ..bases import SM64TestBase
from ... import Options


THI_OPTIONS = {
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
    "tiny_huge_island_coin_star_requirement": 1,
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

PIPES = "Tiny-Huge Island - Warp Pipes"
PURPLE_SWITCH = "Tiny-Huge Island - Purple Switch"
CANNON = "Tiny-Huge Island - Cannon Unlock"
FREESTANDING_1UPS = "Tiny-Huge Island - Freestanding 1-Ups"
TRIGGER_1UPS = "Tiny-Huge Island - Trigger 1-Ups"
BLOCK_1UPS = "Tiny-Huge Island - 1-Up Blocks"
BUTTERFLIES = "Tiny-Huge Island - Butterflies"


class TestTinyHugeIslandTinyLocations(SM64TestBase):
    run_default_tests = False
    options = THI_OPTIONS

    def test_locations(self):
        piranha_area = ["Long Jump"]
        tiny_main = piranha_area + [PURPLE_SWITCH]

        self.run_location_tests([
            ["Tiny-Huge Island - Tiny Island Near Start Block 1-Up", False, []],
            ["Tiny-Huge Island - Tiny Island Near Start Block 1-Up", True, [BLOCK_1UPS]],
            ["Tiny-Huge Island - Tiny Island Near Start 1-Up Block", True, [BLOCK_1UPS]],
            ["Tiny-Huge Island - Start Butterfly 1-Up", False, []],
            ["Tiny-Huge Island - Start Butterfly 1-Up", True, [BUTTERFLIES]],

            ["Tiny-Huge Island - Pluck the Piranha Flower", False,
             piranha_area + [PIPES]],
            ["Tiny-Huge Island - Pluck the Piranha Flower", True,
             piranha_area + [PIPES, "Tiny-Huge Island - Fire Piranha Plants"]],

            ["Tiny-Huge Island - Five Itty Bitty Secrets", False, piranha_area],
            ["Tiny-Huge Island - Five Itty Bitty Secrets", True, tiny_main],
            ["Tiny-Huge Island - Bob-omb Buddy", False, piranha_area],
            ["Tiny-Huge Island - Bob-omb Buddy", True,
             tiny_main + ["Tiny-Huge Island - Bob-omb Buddy"]],
            ["Tiny-Huge Island - 3 Coins Block", False, tiny_main],
            ["Tiny-Huge Island - 3 Coins Block", True,
             tiny_main + ["Tiny-Huge Island - 3-Coin Block"]],

            ["Tiny-Huge Island - Coins Star", False, []],
            ["Tiny-Huge Island - Coins Star", True, ["Tiny-Huge Island - Goombas"]],
        ], starting_regions=["Tiny-Huge Island (Tiny)"])


class TestTinyHugeIslandHugeLocations(SM64TestBase):
    run_default_tests = False
    options = THI_OPTIONS

    def test_locations(self):
        windswept = ["Long Jump"]
        koopa_region = windswept + ["Triple Jump"]
        top = koopa_region
        red_area = [CANNON]

        self.run_location_tests([
            ["Tiny-Huge Island - Beach Coins 1-Up", False, []],
            ["Tiny-Huge Island - Beach Coins 1-Up", True, [TRIGGER_1UPS]],
            ["Tiny-Huge Island - Boss Bass 1-Up", False, []],
            ["Tiny-Huge Island - Boss Bass 1-Up", True, [FREESTANDING_1UPS]],

            ["Tiny-Huge Island - Windy Area Block 1-Up", False, windswept],
            ["Tiny-Huge Island - Windy Area Block 1-Up", True,
             windswept + [BLOCK_1UPS]],
            ["Tiny-Huge Island - Windy Area 1-Up Block", True,
             windswept + [BLOCK_1UPS]],

            ["Tiny-Huge Island - Rematch with Koopa the Quick", False, koopa_region],
            ["Tiny-Huge Island - Rematch with Koopa the Quick", True,
             koopa_region + ["Tiny-Huge Island - Koopa the Quick"]],
            ["Tiny-Huge Island - Huge Island Near Start Block 1-Up", False,
             koopa_region],
            ["Tiny-Huge Island - Huge Island Near Start Block 1-Up", True,
             koopa_region + [BLOCK_1UPS]],
            ["Tiny-Huge Island - Huge Island Near Start 1-Up Block", True,
             koopa_region + [BLOCK_1UPS]],
            ["Tiny-Huge Island - Koopa Area Butterfly 1-Up", False, koopa_region],
            ["Tiny-Huge Island - Koopa Area Butterfly 1-Up", True,
             koopa_region + [BUTTERFLIES]],

            ["Tiny-Huge Island - The Tip Top of the Huge Island", False, windswept],
            ["Tiny-Huge Island - The Tip Top of the Huge Island", True, top],
            ["Tiny-Huge Island - The Tip Top of the Huge Island Star Block", True, top],

            ["Tiny-Huge Island - Wiggler's Red Coins", False, red_area + ["Wall Kick"]],
            ["Tiny-Huge Island - Wiggler's Red Coins", True,
             red_area + ["Wall Kick", "Tiny-Huge Island - Red Coins"]],
            ["Tiny-Huge Island - Cannon Tree 1-Up", False, red_area],
            ["Tiny-Huge Island - Cannon Tree 1-Up", True,
             red_area + [TRIGGER_1UPS]],
            ["Tiny-Huge Island - Red Coin Bridge Tree 1-Up", False, red_area],
            ["Tiny-Huge Island - Red Coin Bridge Tree 1-Up", True,
             red_area + [TRIGGER_1UPS]],
            ["Tiny-Huge Island - Red Coin Cave 1-Up", False, red_area],
            ["Tiny-Huge Island - Red Coin Cave 1-Up", True,
             red_area + ["Wall Kick", FREESTANDING_1UPS]],

            ["Tiny-Huge Island - Make Wiggler Squirm", False, top + [PIPES]],
            ["Tiny-Huge Island - Make Wiggler Squirm", False, top + ["Ground Pound"]],
            ["Tiny-Huge Island - Make Wiggler Squirm", False,
             top + [PIPES, "Ground Pound"]],
            ["Tiny-Huge Island - Make Wiggler Squirm", True,
             top + [PIPES, "Ground Pound", "Tiny-Huge Island - Wiggler"]],
        ], starting_regions=["Tiny-Huge Island (Huge)"])


class TestTinyHugeIslandPipeDirections(SM64TestBase):
    run_default_tests = False
    options = THI_OPTIONS

    def test_huge_piranha_pipe_returns_to_tiny_start(self):
        self.run_location_tests([
            ["Tiny-Huge Island - Beach Coins 1-Up", True, [TRIGGER_1UPS]],
            ["Tiny-Huge Island - Start Butterfly 1-Up", False, [BUTTERFLIES]],
            ["Tiny-Huge Island - Start Butterfly 1-Up", True, [PIPES, BUTTERFLIES]],
        ], starting_regions=["Tiny-Huge Island - Huge Piranha Area"])

    def test_tiny_main_pipe_reaches_koopa_region(self):
        self.run_location_tests([
            ["Tiny-Huge Island - Huge Island Near Start 1-Up Block", False, []],
            ["Tiny-Huge Island - Huge Island Near Start 1-Up Block", True,
             [PIPES, BLOCK_1UPS]],
        ], starting_regions=["Tiny-Huge Island - Tiny Main"])

    def test_terminal_regions_do_not_lead_back_upstream(self):
        self.run_location_tests([
            ["Tiny-Huge Island - Beach Coins 1-Up", False, [TRIGGER_1UPS]],
            ["Tiny-Huge Island - The Tip Top of the Huge Island", False, []],
        ], starting_regions=["Tiny-Huge Island - Red Coins Area"])
        self.run_location_tests([
            ["Tiny-Huge Island - The Tip Top of the Huge Island", False, []],
        ], starting_regions=["Tiny-Huge Island - Wiggler's Cave"])


class TestTinyHugeIslandFlyGuyTrick(SM64TestBase):
    run_default_tests = False
    options = {
        **THI_OPTIONS,
        "logic_tricks": {"Tiny-Huge Island Windswept Valley with Fly Guy Spin Jump"},
    }

    def test_fly_guy_one_use_ascent(self):
        upper_movement = ["Side Flip"]
        self.run_location_tests([
            ["Tiny-Huge Island - The Tip Top of the Huge Island", False, upper_movement],
            ["Tiny-Huge Island - The Tip Top of the Huge Island", True,
             upper_movement + ["Tiny-Huge Island - Fly Guys"]],
        ], starting_regions=["Tiny-Huge Island (Huge)"])


class TestTinyHugeIslandKoopaShellTrick(SM64TestBase):
    run_default_tests = False
    options = {
        **THI_OPTIONS,
        "logic_tricks": {"Tiny-Huge Island Scale the Huge Mountain on the Koopa Shell"},
    }

    def test_koopa_shell_one_use_ascent(self):
        self.run_location_tests([
            ["Tiny-Huge Island - The Tip Top of the Huge Island", False, []],
            ["Tiny-Huge Island - The Tip Top of the Huge Island", True,
             ["Tiny-Huge Island - Koopa Troopas"]],
        ], starting_regions=["Tiny-Huge Island (Huge)"])


class TestTinyHugeIslandFullLevelUnlocks(SM64TestBase):
    run_default_tests = False
    options = THI_OPTIONS

    def test_tiny_and_huge_painting_unlocks_are_independent(self):
        upstairs = ["Progressive Upstairs Key"]
        self.run_location_tests([
            ["Tiny-Huge Island - Tiny Island Near Start 1-Up Block", False, upstairs],
            ["Tiny-Huge Island - Tiny Island Near Start 1-Up Block", True,
             upstairs + ["Unlock Tiny Island", BLOCK_1UPS]],
            ["Tiny-Huge Island - Beach Coins 1-Up", False,
             upstairs + [TRIGGER_1UPS]],
            ["Tiny-Huge Island - Beach Coins 1-Up", True,
             upstairs + ["Unlock Huge Island", TRIGGER_1UPS]],
        ], starting_regions=["Castle Grounds"])


class TestTinyHugeIslandGlobalUnlockModes(SM64TestBase):
    run_default_tests = False
    options = {
        **THI_OPTIONS,
        "coin_object_unlocks": Options.CoinObjectUnlocks.option_global,
        "enemy_unlocks": Options.EnemyUnlocks.option_global,
        "one_up_unlocks": Options.OneUpUnlocks.option_global,
        "level_features": Options.LevelFeatures.option_global,
        "bobomb_buddies": Options.BobombBuddies.option_global,
    }

    def test_global_items_replace_per_level_items(self):
        self.run_location_tests([
            ["Tiny-Huge Island - Coins Star", True, ["Tiny-Huge Island - Goombas"]],
            ["Tiny-Huge Island - Coins Star", True, ["Goombas"]],
            ["Tiny-Huge Island - Start Butterfly 1-Up", True,
             ["Tiny-Huge Island - Butterflies"]],
            ["Tiny-Huge Island - Start Butterfly 1-Up", True, ["Butterflies"]],
            ["Tiny-Huge Island - Five Itty Bitty Secrets", False, ["Long Jump"]],
            ["Tiny-Huge Island - Five Itty Bitty Secrets", True,
             ["Long Jump", "Purple Switches"]],
        ], starting_regions=["Tiny-Huge Island (Tiny)"])


class TestTinyHugeIslandNotShuffledUnlockModes(SM64TestBase):
    run_default_tests = False
    options = {
        **THI_OPTIONS,
        "level_unlocks": Options.LevelUnlocks.option_disabled,
        "coin_object_unlocks": Options.CoinObjectUnlocks.option_not_shuffled,
        "enemy_unlocks": Options.EnemyUnlocks.option_not_shuffled,
        "one_up_unlocks": Options.OneUpUnlocks.option_not_shuffled,
        "level_features": Options.LevelFeatures.option_not_shuffled,
        "bobomb_buddies": Options.BobombBuddies.option_not_shuffled,
    }

    def test_not_shuffled_items_require_no_inventory(self):
        self.run_location_tests([
            ["Tiny-Huge Island - Coins Star", True, []],
            ["Tiny-Huge Island - Start Butterfly 1-Up", True, []],
            ["Tiny-Huge Island - Five Itty Bitty Secrets", True, ["Long Jump"]],
        ], starting_regions=["Tiny-Huge Island (Tiny)"])
        self.run_location_tests([
            ["Tiny-Huge Island - Tiny Island Near Start 1-Up Block", True,
             ["Progressive Upstairs Key"]],
        ], starting_regions=["Castle Grounds"])
