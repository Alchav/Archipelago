from ..bases import SM64TestBase
from ... import Options


HMC_OPTIONS = {
    "area_rando": Options.AreaRandomizer.option_Off,
    "blocksanity": Options.Blocksanity.option_true,
    "buddy_checks": Options.BuddyChecks.option_true,
    "coin_object_unlocks": Options.CoinObjectUnlocks.option_per_level,
    "enemy_unlocks": Options.EnemyUnlocks.option_per_level,
    "hazy_maze_cave_coin_star_requirement": 139,
    "level_features": Options.LevelFeatures.option_per_level,
        "bobomb_buddies": Options.BobombBuddies.option_per_level,
    "one_up_checks": Options.OneUpChecks.option_true,
    "one_up_unlocks": Options.OneUpUnlocks.option_per_level,
    "per_level_cap_items": Options.PerLevelCapItems.option_true,
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


class TestHazyMazeCaveLocations(SM64TestBase):
    run_default_tests = False
    options = HMC_OPTIONS

    def test_locations(self):
        red_coin_area = [
            "Hazy Maze Cave - Checkerboard Platform",
            "Climb",
            "Wall Kick",
        ]
        pit_islands = ["Triple Jump", "Climb"]

        self.run_location_tests([
            ["Hazy Maze Cave - Swimming Beast in the Cavern", False, []],
            ["Hazy Maze Cave - Swimming Beast in the Cavern", True,
             ["Hazy Maze Cave - Swimming Beast"]],

            ["Hazy Maze Cave - Elevate for 8 Red Coins", False, red_coin_area],
            ["Hazy Maze Cave - Elevate for 8 Red Coins", True,
             red_coin_area + ["Hazy Maze Cave - Red Coins"]],

            ["Hazy Maze Cave - Metal-Head Mario Can Move!", False,
             ["Hazy Maze Cave - Purple Switch", "Long Jump"]],
            ["Hazy Maze Cave - Metal-Head Mario Can Move!", True, [
                "Hazy Maze Cave - Purple Switch",
                "Long Jump",
                "Hazy Maze Cave - Metal Cap",
            ]],

            ["Hazy Maze Cave - Navigating the Toxic Maze", False, []],
            ["Hazy Maze Cave - Navigating the Toxic Maze", True, ["Side Flip"]],
            ["Hazy Maze Cave - Watch for Rolling Rocks", False, []],
            ["Hazy Maze Cave - Watch for Rolling Rocks", True, ["Wall Kick"]],

            ["Hazy Maze Cave - A-Maze-Ing Emergency Exit", False, ["Triple Jump"]],
            ["Hazy Maze Cave - A-Maze-Ing Emergency Exit", True, pit_islands],

            ["Hazy Maze Cave - Above Pit Block 1-Up", False, pit_islands],
            ["Hazy Maze Cave - Above Pit Block 1-Up", True,
             pit_islands + ["Hazy Maze Cave - 1-Up Blocks"]],
            ["Hazy Maze Cave - Above Pit 1-Up Block", False, ["Triple Jump"]],
            ["Hazy Maze Cave - Above Pit 1-Up Block", True,
             pit_islands + ["Hazy Maze Cave - 1-Up Blocks"]],

            ["Hazy Maze Cave - Past Rolling Rocks Block 1-Up", False, []],
            ["Hazy Maze Cave - Past Rolling Rocks Block 1-Up", True,
             ["Hazy Maze Cave - 1-Up Blocks"]],
            ["Hazy Maze Cave - Past Rolling Rocks 1-Up Block", True,
             ["Hazy Maze Cave - 1-Up Blocks"]],

            ["Hazy Maze Cave - Blue Coin Trail Monty Moles", False,
             ["Hazy Maze Cave - Trigger 1-Ups"]],
            ["Hazy Maze Cave - Blue Coin Trail Monty Moles", True,
             ["Hazy Maze Cave - Monty Moles"]],
            ["Hazy Maze Cave - Twin Hole Monty Moles", False,
             ["Hazy Maze Cave - Trigger 1-Ups"]],
            ["Hazy Maze Cave - Twin Hole Monty Moles", True,
             ["Hazy Maze Cave - Monty Moles"]],

            ["Hazy Maze Cave - Beginning Metal Cap Block", False, []],
            ["Hazy Maze Cave - Beginning Metal Cap Block", True,
             ["Hazy Maze Cave - Metal Cap"]],
            ["Hazy Maze Cave - Metal-Head Mario Can Move Metal Cap Block", False, []],
            ["Hazy Maze Cave - Metal-Head Mario Can Move Metal Cap Block", True,
             ["Hazy Maze Cave - Metal Cap"]],
            ["Hazy Maze Cave - Toxic Maze Near Empty Alcove Metal Cap Block", False, []],
            ["Hazy Maze Cave - Toxic Maze Near Empty Alcove Metal Cap Block", True,
             ["Hazy Maze Cave - Metal Cap"]],
            ["Hazy Maze Cave - Toxic Maze Near Bats Metal Cap Block", False, []],
            ["Hazy Maze Cave - Toxic Maze Near Bats Metal Cap Block", True,
             ["Hazy Maze Cave - Metal Cap"]],
            ["Hazy Maze Cave - Toxic Maze Near Twin Monty Mole Holes Metal Cap Block", False, []],
            ["Hazy Maze Cave - Toxic Maze Near Twin Monty Mole Holes Metal Cap Block", True,
             ["Hazy Maze Cave - Metal Cap"]],

            ["Hazy Maze Cave - Coins Star", False, [],
             ["Hazy Maze Cave - Red Coins"]],
            ["Hazy Maze Cave - Coins Star", True, [], ALL_ITEMS],
        ], starting_regions=["Hazy Maze Cave"])
