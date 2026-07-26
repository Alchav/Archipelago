from ..bases import SM64TestBase
from ... import Options


JRB_OPTIONS = {
    "area_rando": Options.AreaRandomizer.option_Off,
    "blocksanity": Options.Blocksanity.option_true,
    "buddy_checks": Options.BuddyChecks.option_true,
    "one_up_checks": Options.OneUpChecks.option_true,
    "one_up_mushroom_unlocks": Options.OneUpMushroomUnlocks.option_per_level,
    "coin_object_unlocks": Options.CoinObjectUnlocks.option_per_level,
    "enemy_unlocks": Options.EnemyUnlocks.option_per_level,
    "purple_switches": Options.PurpleSwitches.option_per_level,
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
UPPER = ["Triple Jump"]
METAL_CAP = ["Jolly Roger Bay - Metal Cap"]
TRIGGER_1UPS = ["Jolly Roger Bay - Trigger 1-Ups"]
FREESTANDING_1UPS = ["Jolly Roger Bay - Freestanding 1-Ups"]


class TestJollyRogerBayLocations(SM64TestBase):
    run_default_tests = False
    options = JRB_OPTIONS

    def test_locations(self):
        self.run_location_tests([
            ["Jolly Roger Bay - Plunder in the Sunken Ship", False, []],
            ["Jolly Roger Bay - Plunder in the Sunken Ship", True,
             ["Jolly Roger Bay - Sunken Ship"]],
            ["Jolly Roger Bay - Can the Eel Come Out to Play?", False, []],
            ["Jolly Roger Bay - Can the Eel Come Out to Play?", True,
             ["Jolly Roger Bay - Unagi"]],
            ["Jolly Roger Bay - Treasure of the Ocean Cave", True, []],
            ["Jolly Roger Bay - Bob-omb Buddy", False, []],
            ["Jolly Roger Bay - Bob-omb Buddy", True,
             ["Jolly Roger Bay - Bob-omb Buddy"]],

            ["Jolly Roger Bay - Blast to the Stone Pillar", False,
             ["Jolly Roger Bay - Cannon Unlock"]],
            ["Jolly Roger Bay - Blast to the Stone Pillar", True,
             ["Jolly Roger Bay - Cannon Unlock", "Climb"]],
            ["Jolly Roger Bay - Through the Jet Stream", False,
             ["Jolly Roger Bay - Jet Stream"]],
            ["Jolly Roger Bay - Through the Jet Stream", True,
             ["Jolly Roger Bay - Jet Stream", "Jolly Roger Bay - Metal Cap"]],

            ["Jolly Roger Bay - Underwater Coin Ring 1-Up", False, []],
            ["Jolly Roger Bay - Underwater Coin Ring 1-Up", True, TRIGGER_1UPS],
            ["Jolly Roger Bay - Stone Pillar 1-Up", False, FREESTANDING_1UPS],
            ["Jolly Roger Bay - Stone Pillar 1-Up", True,
             FREESTANDING_1UPS + ["Jolly Roger Bay - Cannon Unlock"]],

            ["Jolly Roger Bay - Beginning Metal Cap Block", False, []],
            ["Jolly Roger Bay - Beginning Metal Cap Block", True, METAL_CAP],
            ["Jolly Roger Bay - Ocean Cave Metal Cap Block", False, []],
            ["Jolly Roger Bay - Ocean Cave Metal Cap Block", True, METAL_CAP],
            ["Jolly Roger Bay - 3 Coins Block", False, []],
            ["Jolly Roger Bay - 3 Coins Block", True,
             ["Jolly Roger Bay - 3-Coin Block"]],

            ["Jolly Roger Bay - Plunder in the Sunken Ship Star Block", False, []],
            ["Jolly Roger Bay - Plunder in the Sunken Ship Star Block", True,
             ["Jolly Roger Bay - Sunken Ship"]],
            ["Jolly Roger Bay - Blast to the Stone Pillar Star Block", False,
             ["Jolly Roger Bay - Cannon Unlock"]],
            ["Jolly Roger Bay - Blast to the Stone Pillar Star Block", True,
             ["Jolly Roger Bay - Cannon Unlock", "Climb"]],

            ["Jolly Roger Bay - Red Coins on the Ship Afloat", False,
             UPPER + ["Jolly Roger Bay - Red Coins", "Jolly Roger Bay - Raised Ship"]],
            ["Jolly Roger Bay - Red Coins on the Ship Afloat", True,
             UPPER + ["Jolly Roger Bay - Red Coins", "Jolly Roger Bay - Raised Ship", "Climb"]],
            ["Jolly Roger Bay - Purple Switch Metal Cap Block", False, UPPER],
            ["Jolly Roger Bay - Purple Switch Metal Cap Block", True, UPPER + METAL_CAP],

            ["Jolly Roger Bay - Coins Star", False, []],
            ["Jolly Roger Bay - Coins Star", True, [], ALL_ITEMS],
        ], starting_regions=["Jolly Roger Bay"])


class TestJollyRogerBayTricks(SM64TestBase):
    run_default_tests = False
    options = {
        **JRB_OPTIONS,
        "one_up_mushroom_unlocks": Options.OneUpMushroomUnlocks.option_not_shuffled,
        "logic_tricks": {
            "Jolly Roger Bay Upper Platform with Ledge Grab",
            "Jolly Roger Bay Pillar Red Coin with Cannon",
            "Jolly Roger Bay Stone Pillar without Cannon",
            "Jolly Roger Bay Through the Jet Stream without Metal Cap",
        },
    }

    def test_upper_with_ledge_grab(self):
        self.run_location_tests([
            ["Jolly Roger Bay - Purple Switch Metal Cap Block", False, METAL_CAP],
            ["Jolly Roger Bay - Purple Switch Metal Cap Block", True,
             METAL_CAP + ["Ledge Grab"]],
        ], starting_regions=["Jolly Roger Bay"])

    def test_ship_red_coin_with_cannon(self):
        route = UPPER + [
            "Jolly Roger Bay - Raised Ship",
            "Jolly Roger Bay - Red Coins",
        ]
        self.run_location_tests([
            ["Jolly Roger Bay - Red Coins on the Ship Afloat", False, route],
            ["Jolly Roger Bay - Red Coins on the Ship Afloat", True,
             route + ["Jolly Roger Bay - Cannon Unlock"]],
        ], starting_regions=["Jolly Roger Bay"])

    def test_stone_pillar_without_cannon(self):
        self.run_location_tests([
            ["Jolly Roger Bay - Blast to the Stone Pillar", True, []],
            ["Jolly Roger Bay - Blast to the Stone Pillar Star Block", True, []],
        ], starting_regions=["Jolly Roger Bay"])

    def test_jet_stream_without_metal_cap(self):
        self.run_location_tests([
            ["Jolly Roger Bay - Through the Jet Stream", False, []],
            ["Jolly Roger Bay - Through the Jet Stream", True,
             ["Jolly Roger Bay - Jet Stream"]],
        ], starting_regions=["Jolly Roger Bay"])
