from ..bases import SM64TestBase
from ... import Options


DDD_OPTIONS = {
    "area_rando": Options.AreaRandomizer.option_Off,
    "blocksanity": Options.Blocksanity.option_true,
    "coin_object_unlocks": Options.CoinObjectUnlocks.option_per_level,
    "dire_dire_docks_coin_star_requirement": 106,
    "enemy_unlocks": Options.EnemyUnlocks.option_per_level,
    "one_up_checks": Options.OneUpChecks.option_true,
    "one_up_unlocks": Options.OneUpUnlocks.option_per_level,
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


class TestDireDireDocksLocations(SM64TestBase):
    run_default_tests = False
    options = DDD_OPTIONS

    def test_locations(self):
        self.run_location_tests([
            ["Dire, Dire Docks - Board Bowser's Sub", False,
             ["Dire, Dire Docks - Purple Switch"]],
            ["Dire, Dire Docks - Board Bowser's Sub", True, [
                "Dire, Dire Docks - Purple Switch",
                "Dire, Dire Docks - Bowser's Sub",
            ]],
            ["Dire, Dire Docks - Chests in the Current", False, []],
            ["Dire, Dire Docks - Chests in the Current", True,
             ["Dire, Dire Docks - Treasure Chests"]],

            ["Dire, Dire Docks - Pole-Jumping for Red Coins", False, [
                "Dire, Dire Docks - Red Coins",
                "Dire, Dire Docks - Purple Switch",
                "Dire, Dire Docks - Poles",
            ]],
            ["Dire, Dire Docks - Pole-Jumping for Red Coins", True, [
                "Dire, Dire Docks - Red Coins",
                "Dire, Dire Docks - Purple Switch",
                "Dire, Dire Docks - Poles",
                "Climb",
            ]],

            ["Dire, Dire Docks - Through the Jet Stream", False, []],
            ["Dire, Dire Docks - Through the Jet Stream", True,
             ["Dire, Dire Docks - Metal Cap"]],
            ["Dire, Dire Docks - The Manta Ray's Reward", False, []],
            ["Dire, Dire Docks - The Manta Ray's Reward", True,
             ["Dire, Dire Docks - Manta Ray"]],
            ["Dire, Dire Docks - Collect the Caps...", False, []],
            ["Dire, Dire Docks - Collect the Caps...", True,
             ["Dire, Dire Docks - Vanish Cap"]],

            ["Dire, Dire Docks - Whirlpool Clam 1-Up", False, []],
            ["Dire, Dire Docks - Whirlpool Clam 1-Up", True,
             ["Dire, Dire Docks - Trigger 1-Ups"]],

            ["Dire, Dire Docks - Metal Cap Block", False, []],
            ["Dire, Dire Docks - Metal Cap Block", True,
             ["Dire, Dire Docks - Metal Cap"]],
            ["Dire, Dire Docks - Vanish Cap Block", False, []],
            ["Dire, Dire Docks - Vanish Cap Block", True,
             ["Dire, Dire Docks - Vanish Cap"]],

            ["Dire, Dire Docks - Coins Star", False, [],
             ["Dire, Dire Docks - Red Coins"]],
            ["Dire, Dire Docks - Coins Star", True, [], ALL_ITEMS],
        ], starting_regions=["Dire, Dire Docks"])


class TestDireDireDocksSubPoleRoute(SM64TestBase):
    run_default_tests = False
    options = DDD_OPTIONS

    def test_sub_route_to_red_coins(self):
        self.run_location_tests([
            ["Dire, Dire Docks - Pole-Jumping for Red Coins", False, [
                "Dire, Dire Docks - Red Coins",
                "Dire, Dire Docks - Bowser's Sub",
                "Dire, Dire Docks - Poles",
                "Climb",
            ]],
            ["Dire, Dire Docks - Pole-Jumping for Red Coins", True, [
                "Dire, Dire Docks - Red Coins",
                "Dire, Dire Docks - Bowser's Sub",
                "Dire, Dire Docks - Poles",
                "Climb",
                "Triple Jump",
            ]],
        ], starting_regions=["Dire, Dire Docks"])
