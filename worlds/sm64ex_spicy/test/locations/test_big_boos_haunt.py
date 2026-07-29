from ..bases import SM64TestBase
from ... import Options


BBH_OPTIONS = {
    "area_rando": Options.AreaRandomizer.option_Off,
    "blocksanity": Options.Blocksanity.option_true,
    "one_up_checks": Options.OneUpChecks.option_true,
    "one_up_mushroom_unlocks": Options.OneUpMushroomUnlocks.option_per_level,
    "coin_object_unlocks": Options.CoinObjectUnlocks.option_per_level,
    "enemy_unlocks": Options.EnemyUnlocks.option_per_level,
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
SECOND_FLOOR = ["Big Boo's Haunt - Staircase"]
THIRD_FLOOR = SECOND_FLOOR + ["Wall Kick", "Ledge Grab"]
ROOF = THIRD_FLOOR + ["Long Jump"]
VANISH_CAP = ["Big Boo's Haunt - Vanish Cap"]


class TestBigBoosHauntLocations(SM64TestBase):
    run_default_tests = False
    options = BBH_OPTIONS

    def test_locations(self):
        self.run_location_tests([
            ["Big Boo's Haunt - Go on a Ghost Hunt", False,
             ["Big Boo's Haunt - Boos"]],
            ["Big Boo's Haunt - Go on a Ghost Hunt", True,
             ["Big Boo's Haunt - Boos", "Big Boo's Haunt - Big Boo"]],
            ["Big Boo's Haunt - Ride Big Boo's Merry-Go-Round", False,
             ["Big Boo's Haunt - Merry-go-round", "Big Boo's Haunt - Boos"]],
            ["Big Boo's Haunt - Ride Big Boo's Merry-Go-Round", True,
             [
                 "Big Boo's Haunt - Merry-go-round",
                 "Big Boo's Haunt - Boos",
                 "Big Boo's Haunt - Big Boo",
             ]],
            ["Big Boo's Haunt - Shed Roof 1-Up", False,
             ["Big Boo's Haunt - Freestanding 1-Ups"]],
            ["Big Boo's Haunt - Shed Roof 1-Up", True,
             ["Big Boo's Haunt - Freestanding 1-Ups", "Triple Jump"]],
            ["Big Boo's Haunt - Back Entrance Vanish Cap Block", False, []],
            ["Big Boo's Haunt - Back Entrance Vanish Cap Block", True, VANISH_CAP],
            ["Big Boo's Haunt - 10 Coins Block", False, []],
            ["Big Boo's Haunt - 10 Coins Block", True,
             ["Big Boo's Haunt - 10-Coin Block"]],

            ["Big Boo's Haunt - Secret of the Haunted Books", False, SECOND_FLOOR],
            ["Big Boo's Haunt - Secret of the Haunted Books", True,
             SECOND_FLOOR + ["Kick"]],
            ["Big Boo's Haunt - Seek the 8 Red Coins", False,
             SECOND_FLOOR],
            ["Big Boo's Haunt - Seek the 8 Red Coins", True,
             SECOND_FLOOR + ["Big Boo's Haunt - Red Coins"]],
            ["Big Boo's Haunt - Second Floor Vanish Cap Block", False, SECOND_FLOOR],
            ["Big Boo's Haunt - Second Floor Vanish Cap Block", True,
             SECOND_FLOOR + VANISH_CAP],

            ["Big Boo's Haunt - Eye to Eye in the Secret Room", False,
             THIRD_FLOOR + VANISH_CAP],
            ["Big Boo's Haunt - Eye to Eye in the Secret Room", True,
             THIRD_FLOOR + VANISH_CAP + ["Big Boo's Haunt - Mr. Is"]],
            ["Big Boo's Haunt - Secret Room Vanish Cap Block", False, THIRD_FLOOR],
            ["Big Boo's Haunt - Secret Room Vanish Cap Block", True,
             THIRD_FLOOR + VANISH_CAP],

            ["Big Boo's Haunt - Big Boo's Balcony", False, ROOF],
            ["Big Boo's Haunt - Big Boo's Balcony", True,
             ROOF + ["Big Boo's Haunt - Big Boo"]],
            ["Big Boo's Haunt - Top of Mansion Block 1-Up", False, ROOF],
            ["Big Boo's Haunt - Top of Mansion Block 1-Up", True,
             ROOF + ["Big Boo's Haunt - 1-Up Blocks"]],
            ["Big Boo's Haunt - Top of Mansion 1-Up Block", True, ROOF],

            ["Big Boo's Haunt - Coins Star", False, []],
            ["Big Boo's Haunt - Coins Star", True, [], ALL_ITEMS],
        ], starting_regions=["Big Boo's Haunt"])


class TestBigBoosHauntTricks(SM64TestBase):
    run_default_tests = False
    options = {
        **BBH_OPTIONS,
        "one_up_mushroom_unlocks": Options.OneUpMushroomUnlocks.option_not_shuffled,
        "logic_tricks": {
            "Big Boo's Haunt Second Floor with Wall Kick",
            "Big Boo's Haunt Third Floor with Side Flip and Bounce Off of Bookends",
            "Big Boo's Haunt Roof without Long Jump",
        },
    }

    def test_second_floor_with_wall_kick(self):
        self.run_location_tests([
            ["Big Boo's Haunt - Secret of the Haunted Books", False,
             ["Kick"]],
            ["Big Boo's Haunt - Secret of the Haunted Books", True,
             ["Wall Kick", "Kick"]],
        ], starting_regions=["Big Boo's Haunt"])

    def test_third_floor_with_bookend_bounce(self):
        self.run_location_tests([
            ["Big Boo's Haunt - Eye to Eye in the Secret Room", False,
             SECOND_FLOOR + ["Side Flip"] + VANISH_CAP + ["Big Boo's Haunt - Mr. Is"]],
            ["Big Boo's Haunt - Eye to Eye in the Secret Room", True,
             SECOND_FLOOR + [
                 "Side Flip",
                 "Big Boo's Haunt - Flying Bookends",
                 "Big Boo's Haunt - Vanish Cap",
                 "Big Boo's Haunt - Mr. Is",
             ]],
        ], starting_regions=["Big Boo's Haunt"])

    def test_roof_without_long_jump(self):
        self.run_location_tests([
            ["Big Boo's Haunt - Big Boo's Balcony", True,
             THIRD_FLOOR + ["Big Boo's Haunt - Big Boo"]],
        ], starting_regions=["Big Boo's Haunt"])
