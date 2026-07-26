from ..bases import SM64TestBase
from ... import Options


SL_OPTIONS = {
    "area_rando": Options.AreaRandomizer.option_Off,
    "blocksanity": Options.Blocksanity.option_true,
    "buddy_checks": Options.BuddyChecks.option_true,
    "coin_object_unlocks": Options.CoinObjectUnlocks.option_per_level,
    "enemy_unlocks": Options.EnemyUnlocks.option_per_level,
    "no_despawns": Options.NoDespawns.option_false,
    "one_up_checks": Options.OneUpChecks.option_true,
    "one_up_mushroom_unlocks": Options.OneUpMushroomUnlocks.option_per_level,
    "per_level_cap_items": Options.PerLevelCapItems.option_true,
    "snowmans_land_coin_star_requirement": 126,
    "snowmans_land_penguin": Options.SnowmansLandPenguin.option_true,
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


class TestSnowmansLandLocations(SM64TestBase):
    run_default_tests = False
    options = SL_OPTIONS

    def test_locations(self):
        cannon = ["Snowman's Land - Cannon Unlock"]
        igloo = cannon

        self.run_location_tests([
            ["Snowman's Land - Chill with the Bully", False, []],
            ["Snowman's Land - Chill with the Bully", True,
             ["Snowman's Land - Chill Bully"]],
            ["Snowman's Land - In the Deep Freeze", False, []],
            ["Snowman's Land - In the Deep Freeze", True, ["Wall Kick"]],
            ["Snowman's Land - Bob-omb Buddy", True, []],

            ["Snowman's Land - Whirl from the Freezing Pond", False, []],
            ["Snowman's Land - Whirl from the Freezing Pond", True,
             ["Snowman's Land - Spindrifts"]],
            ["Snowman's Land - Koopa Shell Block", False, []],
            ["Snowman's Land - Koopa Shell Block", True,
             ["Snowman's Land - Spindrifts"]],
            ["Snowman's Land - Shell Shreddin' for Red Coins", False,
             ["Snowman's Land - Spindrifts"]],
            ["Snowman's Land - Shell Shreddin' for Red Coins", True, [
                "Snowman's Land - Spindrifts",
                "Snowman's Land - Red Coins",
            ]],
            ["Snowman's Land - Whirl from the Freezing Pond Star Block", False, []],
            ["Snowman's Land - Whirl from the Freezing Pond Star Block", True,
             ["Snowman's Land - Spindrifts"]],

            ["Snowman's Land - Snowman's Big Head", False, ["Backflip"]],
            ["Snowman's Land - Snowman's Big Head", True, cannon],
            ["Snowman's Land - Snowman's Big Head", True,
             ["Snowman's Land - Penguin", "Backflip"]],

            ["Snowman's Land - Snowman Tree 1-Up", False,
             cannon + ["Snowman's Land - Trigger 1-Ups"]],
            ["Snowman's Land - Snowman Tree 1-Up", True, cannon + [
                "Side Flip",
                "Snowman's Land - Trigger 1-Ups",
            ]],

            ["Snowman's Land - Into the Igloo", False,
             igloo + ["Snowman's Land - Vanish Cap"]],
            ["Snowman's Land - Into the Igloo", True, igloo + [
                "Snowman's Land - Vanish Cap",
                "Wall Kick",
            ]],
            ["Snowman's Land - Igloo Ice Block 1-Up", False,
             igloo + ["Snowman's Land - Freestanding 1-Ups"]],
            ["Snowman's Land - Igloo Ice Block 1-Up", True, igloo + [
                "Snowman's Land - Vanish Cap",
                "Wall Kick",
                "Snowman's Land - Freestanding 1-Ups",
            ]],

            ["Snowman's Land - Near Moneybags Block 1-Up", False, []],
            ["Snowman's Land - Near Moneybags Block 1-Up", True,
             ["Snowman's Land - 1-Up Blocks"]],
            ["Snowman's Land - Near Moneybags 1-Up Block", True, []],

            ["Snowman's Land - Inside Igloo Block 1-Up", False,
             igloo + ["Snowman's Land - Vanish Cap", "Wall Kick"]],
            ["Snowman's Land - Inside Igloo Block 1-Up", True, igloo + [
                "Snowman's Land - Vanish Cap",
                "Wall Kick",
                "Snowman's Land - 1-Up Blocks",
            ]],
            ["Snowman's Land - Inside Igloo 1-Up Block", False,
             igloo + ["Snowman's Land - Vanish Cap"]],
            ["Snowman's Land - Inside Igloo 1-Up Block", True, igloo + [
                "Snowman's Land - Vanish Cap",
                "Wall Kick",
            ]],

            ["Snowman's Land - Vanish Cap Block", False, igloo],
            ["Snowman's Land - Vanish Cap Block", True,
             igloo + ["Snowman's Land - Vanish Cap"]],
            ["Snowman's Land - 3 Coins Block", False, igloo],
            ["Snowman's Land - 3 Coins Block", True,
             igloo + ["Snowman's Land - 3-Coin Block"]],

            ["Snowman's Land - Coins Star", False, [],
             ["Snowman's Land - Red Coins"]],
            ["Snowman's Land - Coins Star", True, [], ALL_ITEMS],
        ], starting_regions=["Snowman's Land"])


class TestSnowmansLandWhirlCannonRoute(SM64TestBase):
    run_default_tests = False
    options = SL_OPTIONS

    def test_cannon_reaches_whirl(self):
        self.run_location_tests([
            ["Snowman's Land - Whirl from the Freezing Pond", False, []],
            ["Snowman's Land - Whirl from the Freezing Pond", True,
             ["Snowman's Land - Cannon Unlock"]],
        ], starting_regions=["Snowman's Land"])


class TestSnowmansLandImpossibleCoin(SM64TestBase):
    run_default_tests = False
    options = {
        **SL_OPTIONS,
        "accessibility": "minimal",
        "logic_tricks": {"Snowman's Land Impossible Coin"},
        "snowmans_land_coin_star_requirement": 127,
    }

    def test_impossible_coin_route(self):
        self.run_location_tests([
            ["Snowman's Land - Coins Star", False, [],
             ["Snowman's Land - Cannon Unlock"]],
            ["Snowman's Land - Coins Star", True, [], ALL_ITEMS],
        ], starting_regions=["Snowman's Land"])
