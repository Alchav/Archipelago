from ..bases import SM64TestBase
from ... import Options


RR_OPTIONS = {
    "area_rando": Options.AreaRandomizer.option_Off,
    "level_unlocks": Options.LevelUnlocks.option_full,
    "blocksanity": Options.Blocksanity.option_true,
    "buddy_checks": Options.BuddyChecks.option_true,
    "one_up_checks": Options.OneUpChecks.option_true,
    "one_up_mushroom_unlocks": Options.OneUpMushroomUnlocks.option_per_level,
    "coin_object_unlocks": Options.CoinObjectUnlocks.option_per_level,
    "enemy_unlocks": Options.EnemyUnlocks.option_per_level,
    "level_features": Options.LevelFeatures.option_true,
        "hazy_maze_cave_swimming_beast": Options.HazyMazeCaveSwimmingBeast.option_true,
        "rainbow_ride_carpets": Options.RainbowRideCarpets.option_true,
        "tiny_huge_island_warp_pipes": Options.TinyHugeIslandWarpPipes.option_true,
        "cool_cool_mountain_baby_penguins": Options.CoolCoolMountainBabyPenguins.option_true,
        "snowmans_land_penguin": Options.SnowmansLandPenguin.option_true,
        "shifting_sand_land_pyramid_elevator": Options.ShiftingSandLandPyramidElevator.option_true,
        "wet_dry_world_water_level_diamond": Options.WetDryWorldWaterLevelDiamond.option_true,
        "tick_tock_clock_spinners": Options.TickTockClockSpinners.option_true,
        "checkerboard_platforms": Options.CheckerboardPlatforms.option_per_level,
        "rolling_logs": Options.RollingLogs.option_per_level,
        "purple_switches": Options.PurpleSwitches.option_per_level,
        "bobomb_buddies": Options.BobombBuddies.option_per_level,
        "treasure_chests": Options.TreasureChests.option_per_level,
    "rainbow_ride_coin_star_requirement": 1,
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

CARPETS = "Rainbow Ride - Carpets"
PURPLE_SWITCH = "Rainbow Ride - Purple Switch"
CANNON = "Rainbow Ride - Cannon Unlock"
RED_COINS = "Rainbow Ride - Red Coins"
FREESTANDING_1UPS = "Rainbow Ride - Freestanding 1-Ups"
TRIGGER_1UPS = "Rainbow Ride - Trigger 1-Ups"
BLOCK_1UPS = "Rainbow Ride - 1-Up Blocks"


class TestRainbowRideLocations(SM64TestBase):
    run_default_tests = False
    options = RR_OPTIONS

    def test_locations(self):
        beneath_pole = ["Long Jump"]
        beneath_checks = beneath_pole + ["Side Flip"]
        maze = beneath_pole + ["Climb"]
        carpets = [CARPETS]
        cruiser = carpets + ["Side Flip"]
        house = carpets + ["Side Flip"]

        self.run_location_tests([
            ["Rainbow Ride - Swingin' in the Breeze", False, beneath_pole],
            ["Rainbow Ride - Swingin' in the Breeze", True, beneath_checks],
            ["Rainbow Ride - Tricky Triangles!", False, beneath_checks],
            ["Rainbow Ride - Tricky Triangles!", True, beneath_checks + [PURPLE_SWITCH]],
            ["Rainbow Ride - Tricky Triangles 1-Up", False,
             beneath_checks + [PURPLE_SWITCH]],
            ["Rainbow Ride - Tricky Triangles 1-Up", True,
             beneath_checks + [PURPLE_SWITCH, FREESTANDING_1UPS]],
            ["Rainbow Ride - Under Fly Guy Block 1-Up", False, beneath_pole],
            ["Rainbow Ride - Under Fly Guy Block 1-Up", True,
             beneath_pole + [BLOCK_1UPS]],
            ["Rainbow Ride - Under Fly Guy 1-Up Block", True, beneath_pole],

            ["Rainbow Ride - Coins Amassed in a Maze", False, maze],
            ["Rainbow Ride - Coins Amassed in a Maze", False, maze + [RED_COINS]],
            ["Rainbow Ride - Coins Amassed in a Maze", True,
             maze + [RED_COINS, "Wall Kick"]],

            ["Rainbow Ride - Bob-omb Buddy", False, carpets],
            ["Rainbow Ride - Bob-omb Buddy", True,
             carpets + ["Wall Kick", "Rainbow Ride - Bob-omb Buddy"]],

            ["Rainbow Ride - Cruiser Crossing the Rainbow", False, carpets],
            ["Rainbow Ride - Cruiser Crossing the Rainbow", True, cruiser],
            ["Rainbow Ride - Somewhere Over the Rainbow", False, cruiser],
            ["Rainbow Ride - Somewhere Over the Rainbow", True, cruiser + [CANNON]],
            ["Rainbow Ride - Somewhere Over the Rainbow Star Block", False, cruiser],
            ["Rainbow Ride - Somewhere Over the Rainbow Star Block", True,
             cruiser + [CANNON]],
            ["Rainbow Ride - Ship Tip 1-Up", False, cruiser],
            ["Rainbow Ride - Ship Tip 1-Up", True, cruiser + [FREESTANDING_1UPS]],
            ["Rainbow Ride - Ship Pole 1-Up", False,
             cruiser + [TRIGGER_1UPS]],
            ["Rainbow Ride - Ship Pole 1-Up", True,
             cruiser + [TRIGGER_1UPS, "Climb"]],
            ["Rainbow Ride - Rotating Bridge Platform 1-Up", False, cruiser],
            ["Rainbow Ride - Rotating Bridge Platform 1-Up", True,
             cruiser + [FREESTANDING_1UPS]],

            ["Rainbow Ride - The Big House in the Sky", False, carpets],
            ["Rainbow Ride - The Big House in the Sky", True, house],
            ["Rainbow Ride - House in the Sky Block 1-Up", False, house],
            ["Rainbow Ride - House in the Sky Block 1-Up", True,
             house + [BLOCK_1UPS]],
            ["Rainbow Ride - House in the Sky 1-Up Block", True, house],
            ["Rainbow Ride - House Path Donut Lifts 1-Up", False, house],
            ["Rainbow Ride - House Path Donut Lifts 1-Up", True,
             house + [FREESTANDING_1UPS]],
            ["Rainbow Ride - Donut Top of Red Coin Maze 1-Up", False, house],
            ["Rainbow Ride - Donut Top of Red Coin Maze 1-Up", True,
             house + [TRIGGER_1UPS]],
            ["Rainbow Ride - Top of Red Coin Maze Block 1-Up", False, house],
            ["Rainbow Ride - Top of Red Coin Maze Block 1-Up", True,
             house + [BLOCK_1UPS]],
            ["Rainbow Ride - Top of Red Coin Maze 1-Up Block", True, house],

            ["Rainbow Ride - Coins Star", False, beneath_pole],
            ["Rainbow Ride - Coins Star", True,
             beneath_pole + ["Rainbow Ride - Goomba"]],
        ], starting_regions=["Rainbow Ride"])

    def test_carpets_shortcut_reaches_maze_without_beneath_pole(self):
        self.run_location_tests([
            ["Rainbow Ride - Coins Amassed in a Maze", False, [CARPETS, RED_COINS]],
            ["Rainbow Ride - Coins Amassed in a Maze", True,
             [CARPETS, RED_COINS, "Wall Kick"]],
        ], starting_regions=["Rainbow Ride"])


class TestRainbowRideFullLevelUnlock(SM64TestBase):
    run_default_tests = False
    options = RR_OPTIONS

    def test_level_unlock(self):
        third_floor = [
            "Progressive Upstairs Key",
            "Progressive Upstairs Key",
            "Side Flip",
            "Long Jump",
            "Rainbow Ride - Goomba",
        ]
        self.run_location_tests([
            ["Rainbow Ride - Coins Star", False, third_floor],
            ["Rainbow Ride - Coins Star", True,
             third_floor + ["Unlock Rainbow Ride"]],
        ], starting_regions=["Menu"])


class TestRainbowRideBuddyLedgeGrabAndCarpetsTrick(SM64TestBase):
    run_default_tests = False
    options = {
        **RR_OPTIONS,
        "logic_tricks": {"Rainbow Ride Bob-omb Buddy with Ledge Grab and Carpets"},
    }

    def test_trick_requires_ledge_grab_and_carpets(self):
        self.run_location_tests([
            ["Rainbow Ride - Bob-omb Buddy", False, ["Ledge Grab"]],
            ["Rainbow Ride - Bob-omb Buddy", False, [CARPETS]],
            ["Rainbow Ride - Bob-omb Buddy", True,
             [CARPETS, "Ledge Grab", "Rainbow Ride - Bob-omb Buddy"]],
        ], starting_regions=["Rainbow Ride - Carpets"])


class TestRainbowRideMazeCoinsLedgeGrabAndCarpetsTrick(SM64TestBase):
    run_default_tests = False
    options = {
        **RR_OPTIONS,
        "logic_tricks": {"Rainbow Ride Maze Coins with Ledge Grab and Carpets"},
    }

    def test_trick_reaches_all_red_coins_with_ledge_grab_and_carpets(self):
        self.run_location_tests([
            ["Rainbow Ride - Coins Amassed in a Maze", False,
             [RED_COINS, "Ledge Grab"]],
            ["Rainbow Ride - Coins Amassed in a Maze", False,
             [RED_COINS, CARPETS]],
            ["Rainbow Ride - Coins Amassed in a Maze", True,
             [RED_COINS, CARPETS, "Ledge Grab"]],
        ], starting_regions=["Rainbow Ride"])


class TestRainbowRideGlobalUnlockModes(SM64TestBase):
    run_default_tests = False
    options = {
        **RR_OPTIONS,
        "coin_object_unlocks": Options.CoinObjectUnlocks.option_global,
        "enemy_unlocks": Options.EnemyUnlocks.option_global,
        "one_up_mushroom_unlocks": Options.OneUpMushroomUnlocks.option_global,
        "level_features": Options.LevelFeatures.option_true,
        "hazy_maze_cave_swimming_beast": Options.HazyMazeCaveSwimmingBeast.option_true,
        "rainbow_ride_carpets": Options.RainbowRideCarpets.option_true,
        "tiny_huge_island_warp_pipes": Options.TinyHugeIslandWarpPipes.option_true,
        "cool_cool_mountain_baby_penguins": Options.CoolCoolMountainBabyPenguins.option_true,
        "snowmans_land_penguin": Options.SnowmansLandPenguin.option_true,
        "shifting_sand_land_pyramid_elevator": Options.ShiftingSandLandPyramidElevator.option_true,
        "wet_dry_world_water_level_diamond": Options.WetDryWorldWaterLevelDiamond.option_true,
        "tick_tock_clock_spinners": Options.TickTockClockSpinners.option_true,
        "checkerboard_platforms": Options.CheckerboardPlatforms.option_global,
        "rolling_logs": Options.RollingLogs.option_global,
        "purple_switches": Options.PurpleSwitches.option_global,
        "bobomb_buddies": Options.BobombBuddies.option_global,
        "treasure_chests": Options.TreasureChests.option_global,
    }

    def test_global_items_replace_per_level_items(self):
        route = ["Long Jump"]
        self.run_location_tests([
            ["Rainbow Ride - Coins Star", True,
             route + ["Rainbow Ride - Goomba"]],
            ["Rainbow Ride - Coins Star", True, route + ["Goombas"]],
            ["Rainbow Ride - Tricky Triangles 1-Up", False,
             route + ["Side Flip", "Purple Switches",
                      "Rainbow Ride - Freestanding 1-Ups"]],
            ["Rainbow Ride - Tricky Triangles 1-Up", True,
             route + ["Side Flip", "Purple Switches", "Freestanding 1-Ups"]],
        ], starting_regions=["Rainbow Ride"])


class TestRainbowRideNotShuffledUnlockModes(SM64TestBase):
    run_default_tests = False
    options = {
        **RR_OPTIONS,
        "level_unlocks": Options.LevelUnlocks.option_disabled,
        "coin_object_unlocks": Options.CoinObjectUnlocks.option_not_shuffled,
        "enemy_unlocks": Options.EnemyUnlocks.option_not_shuffled,
        "one_up_mushroom_unlocks": Options.OneUpMushroomUnlocks.option_not_shuffled,
        "level_features": Options.LevelFeatures.option_false,
        "rainbow_ride_carpets": Options.RainbowRideCarpets.option_false,
        "purple_switches": Options.PurpleSwitches.option_not_shuffled,
        "bobomb_buddies": Options.BobombBuddies.option_not_shuffled,
    }

    def test_not_shuffled_items_require_no_inventory(self):
        third_floor = [
            "Progressive Upstairs Key",
            "Progressive Upstairs Key",
            "Side Flip",
            "Long Jump",
        ]
        self.run_location_tests([
            ["Rainbow Ride - Coins Star", True, ["Long Jump"]],
            ["Rainbow Ride - Tricky Triangles 1-Up", True,
             ["Long Jump", "Side Flip"]],
        ], starting_regions=["Rainbow Ride"])
        self.run_location_tests([
            ["Rainbow Ride - Coins Star", True, third_floor],
        ], starting_regions=["Menu"])
