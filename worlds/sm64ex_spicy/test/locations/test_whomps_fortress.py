from ..bases import SM64TestBase
from ... import Options


WF_OPTIONS = {
    "area_rando": Options.AreaRandomizer.option_Off,
    "blocksanity": Options.Blocksanity.option_true,
    "buddy_checks": Options.BuddyChecks.option_true,
    "one_up_checks": Options.OneUpChecks.option_true,
    "one_up_unlocks": Options.OneUpUnlocks.option_per_level,
    "coin_object_unlocks": Options.CoinObjectUnlocks.option_per_level,
    "enemy_unlocks": Options.EnemyUnlocks.option_per_level,
    "level_features": Options.LevelFeatures.option_per_level,
        "bobomb_buddies": Options.BobombBuddies.option_per_level,
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

ALL_ITEMS = ["__no_item_has_this_name__"]
TOP = ["Whomp's Fortress - Checkerboard Platform"]
TRIGGER_1UPS = ["Whomp's Fortress - Trigger 1-Ups"]
FREESTANDING_1UPS = ["Whomp's Fortress - Freestanding 1-Ups"]


class TestWhompsFortressLocations(SM64TestBase):
    run_default_tests = False
    options = WF_OPTIONS

    def test_locations(self):
        self.run_location_tests([
            ["Whomp's Fortress - Shoot into the Wild Blue", False, []],
            ["Whomp's Fortress - Shoot into the Wild Blue", True,
             ["Whomp's Fortress - Cannon Unlock"]],
            ["Whomp's Fortress - Fall onto the Caged Island", False, []],
            ["Whomp's Fortress - Fall onto the Caged Island", True,
             ["Whomp's Fortress - Hoot", "Climb"]],
            ["Whomp's Fortress - Blast Away the Wall", False, []],
            ["Whomp's Fortress - Blast Away the Wall", True,
             ["Whomp's Fortress - Cannon Unlock"]],
            ["Whomp's Fortress - Bob-omb Buddy", False, []],
            ["Whomp's Fortress - Bob-omb Buddy", True,
             ["Whomp's Fortress - Bob-omb Buddy"]],
            ["Whomp's Fortress - Flower Patch Butterfly 1-Up", False, []],
            ["Whomp's Fortress - Flower Patch Butterfly 1-Up", True,
             ["Whomp's Fortress - Butterflies"]],
            ["Whomp's Fortress - Metal Cap Block", False, []],
            ["Whomp's Fortress - Metal Cap Block", True,
             ["Whomp's Fortress - Metal Cap"]],

            ["Whomp's Fortress - Chip Off Whomp's Block", False, TOP],
            ["Whomp's Fortress - Chip Off Whomp's Block", True,
             TOP + ["Whomp's Fortress - Whomp King", "Ground Pound"]],
            ["Whomp's Fortress - To the Top of the Fortress", False, TOP],
            ["Whomp's Fortress - To the Top of the Fortress", True,
             TOP + ["Whomp's Fortress - Fortress"]],
            ["Whomp's Fortress - Red Coins on the Floating Isle", False, TOP],
            ["Whomp's Fortress - Red Coins on the Floating Isle", True,
             TOP + ["Whomp's Fortress - Red Coins", "Whomp's Fortress - Thwomp"]],

            ["Whomp's Fortress - Flagpole 1-Up", False, TOP + TRIGGER_1UPS],
            ["Whomp's Fortress - Flagpole 1-Up", True,
             TOP + TRIGGER_1UPS + ["Climb"]],
            ["Whomp's Fortress - Rotating Platform Coins 1-Up", False, TOP],
            ["Whomp's Fortress - Rotating Platform Coins 1-Up", True,
             TOP + TRIGGER_1UPS],
            ["Whomp's Fortress - Tower Alcove 1-Up", False, TOP + FREESTANDING_1UPS],
            ["Whomp's Fortress - Tower Alcove 1-Up", True,
             TOP + FREESTANDING_1UPS + ["Whomp's Fortress - Fortress"]],

            ["Whomp's Fortress - Coins Star", False, []],
            ["Whomp's Fortress - Coins Star", True, [], ALL_ITEMS],
        ], starting_regions=["Whomp's Fortress"])


class TestWhompsFortressTricks(SM64TestBase):
    run_default_tests = False
    options = {
        **WF_OPTIONS,
        "one_up_unlocks": Options.OneUpUnlocks.option_not_shuffled,
        "logic_tricks": {
            "Whomp's Fortress Top Access with Cannon",
            "Whomp's Fortress Top Access with Triple Jump Off of Whomp",
            "Whomp's Fortress Caged Island from the Floating Island with Triple Jump Off of Whomp King",
            "Whomp's Fortress Caged Island With Cannon",
            "Whomp's Fortress Blast Away the Wall with Ledge Grab",
            "Whomp's Fortress Shoot Into the Wild Blue with Long Jump",
        },
    }

    def test_top_with_cannon(self):
        self.run_location_tests([
            ["Whomp's Fortress - Red Coins on the Floating Isle", False,
             ["Whomp's Fortress - Red Coins"]],
            ["Whomp's Fortress - Red Coins on the Floating Isle", True,
             ["Whomp's Fortress - Cannon Unlock", "Whomp's Fortress - Red Coins",
              "Whomp's Fortress - Thwomp"]],
        ], starting_regions=["Whomp's Fortress"])

    def test_top_with_whomp_and_triple_jump(self):
        self.run_location_tests([
            ["Whomp's Fortress - To the Top of the Fortress", False,
             ["Triple Jump", "Whomp's Fortress - Fortress"]],
            ["Whomp's Fortress - To the Top of the Fortress", True,
             ["Whomp's Fortress - Whomps", "Triple Jump", "Whomp's Fortress - Fortress"]],
        ], starting_regions=["Whomp's Fortress"])

    def test_caged_island_from_whomp_king(self):
        self.run_location_tests([
            ["Whomp's Fortress - Fall onto the Caged Island", False,
             TOP + ["Triple Jump"]],
            ["Whomp's Fortress - Fall onto the Caged Island", False,
             TOP + ["Whomp's Fortress - Whomp King"]],
            ["Whomp's Fortress - Fall onto the Caged Island", True,
             TOP + ["Triple Jump", "Whomp's Fortress - Whomp King"]],
        ], starting_regions=["Whomp's Fortress"])

    def test_caged_island_with_cannon(self):
        self.run_location_tests([
            ["Whomp's Fortress - Fall onto the Caged Island", False, []],
            ["Whomp's Fortress - Fall onto the Caged Island", True,
             ["Whomp's Fortress - Cannon Unlock"]],
        ], starting_regions=["Whomp's Fortress"])

    def test_blast_away_wall_with_ledge_grab(self):
        self.run_location_tests([
            ["Whomp's Fortress - Blast Away the Wall", False, []],
            ["Whomp's Fortress - Blast Away the Wall", True, ["Ledge Grab"]],
        ], starting_regions=["Whomp's Fortress"])

    def test_wild_blue_with_long_jump(self):
        self.run_location_tests([
            ["Whomp's Fortress - Shoot into the Wild Blue", False, []],
            ["Whomp's Fortress - Shoot into the Wild Blue", True, ["Long Jump"]],
        ], starting_regions=["Whomp's Fortress"])
