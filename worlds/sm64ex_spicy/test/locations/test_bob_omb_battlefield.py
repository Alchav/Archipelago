from ..bases import SM64TestBase
from ... import Options


BOB_OPTIONS = {
    "area_rando": Options.AreaRandomizer.option_Off,
    "blocksanity": Options.Blocksanity.option_true,
    "buddy_checks": Options.BuddyChecks.option_true,
    "one_up_checks": Options.OneUpChecks.option_true,
    "one_up_unlocks": Options.OneUpUnlocks.option_per_level,
    "coin_object_unlocks": Options.CoinObjectUnlocks.option_per_level,
    "enemy_unlocks": Options.EnemyUnlocks.option_per_level,
    "cap_items": Options.CapItems.option_per_level,
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
CANNON = ["Bob-omb Battlefield - Cannon Unlock"]
ISLAND = CANNON
WING_CAP = ["Bob-omb Battlefield - Wing Cap"]
TRIGGER_1UPS = ["Bob-omb Battlefield - Trigger 1-Ups"]
FREESTANDING_1UPS = ["Bob-omb Battlefield - Freestanding 1-Ups"]


class TestBobOmbBattlefieldLocations(SM64TestBase):
    run_default_tests = False
    options = BOB_OPTIONS

    def test_locations(self):
        self.run_location_tests([
            ["Bob-omb Battlefield - Big Bob-Omb on the Summit", False, []],
            ["Bob-omb Battlefield - Big Bob-Omb on the Summit", True,
             ["Bob-omb Battlefield - King Bob-omb"]],
            ["Bob-omb Battlefield - Footrace with Koopa The Quick", False, []],
            ["Bob-omb Battlefield - Footrace with Koopa The Quick", True,
             ["Bob-omb Battlefield - Koopa the Quick"]],

            ["Bob-omb Battlefield - Mario Wings to the Sky", False,
             CANNON + WING_CAP],
            ["Bob-omb Battlefield - Mario Wings to the Sky", True,
             CANNON + WING_CAP + ["Bob-omb Battlefield - Single Yellow Coins"]],
            ["Bob-omb Battlefield - Mario Wings to the Sky", True,
             CANNON + WING_CAP + ["Bob-omb Battlefield - Vertical Coin Rings"]],

            ["Bob-omb Battlefield - Behind Chain Chomp's Gate", False,
             ["Bob-omb Battlefield - Chain Chomp", "Bob-omb Battlefield - Wooden Posts"]],
            ["Bob-omb Battlefield - Behind Chain Chomp's Gate", False,
             ["Bob-omb Battlefield - Wooden Posts", "Ground Pound"]],
            ["Bob-omb Battlefield - Behind Chain Chomp's Gate", True,
             ["Bob-omb Battlefield - Chain Chomp", "Bob-omb Battlefield - Wooden Posts", "Ground Pound"]],
            ["Bob-omb Battlefield - Bob-omb Buddy", False, []],
            ["Bob-omb Battlefield - Bob-omb Buddy", True,
             ["Bob-omb Battlefield - Bob-omb Buddy"]],

            ["Bob-omb Battlefield - Flower Ring 1-Up", False, []],
            ["Bob-omb Battlefield - Flower Ring 1-Up", True, TRIGGER_1UPS],
            ["Bob-omb Battlefield - Switch Tunnel 1-Up", False, []],
            ["Bob-omb Battlefield - Switch Tunnel 1-Up", True, FREESTANDING_1UPS],
            ["Bob-omb Battlefield - Cannon Tree 1-Up", False, ISLAND + TRIGGER_1UPS],
            ["Bob-omb Battlefield - Cannon Tree 1-Up", True,
             ISLAND + TRIGGER_1UPS + ["Climb"]],

            ["Bob-omb Battlefield - Shoot to the Island in the Sky", False, []],
            ["Bob-omb Battlefield - Shoot to the Island in the Sky", True, ISLAND],
            ["Bob-omb Battlefield - Find the 8 Red Coins", False, ISLAND],
            ["Bob-omb Battlefield - Find the 8 Red Coins", True,
             ISLAND + ["Bob-omb Battlefield - Red Coins", "Climb"]],

            ["Bob-omb Battlefield - Near Flower Patches Wing Cap Block", False, []],
            ["Bob-omb Battlefield - Near Flower Patches Wing Cap Block", True, WING_CAP],
            ["Bob-omb Battlefield - Wooden Ramp Wing Cap Block", False, []],
            ["Bob-omb Battlefield - Wooden Ramp Wing Cap Block", True, WING_CAP],
            ["Bob-omb Battlefield - Island Wing Cap Block", False, ISLAND],
            ["Bob-omb Battlefield - Island Wing Cap Block", True, ISLAND + WING_CAP],
            ["Bob-omb Battlefield - Shoot to the Island in the Sky Star Block", False, []],
            ["Bob-omb Battlefield - Shoot to the Island in the Sky Star Block", True, ISLAND],

            ["Bob-omb Battlefield - Coins Star", False, []],
            ["Bob-omb Battlefield - Coins Star", True, [], ALL_ITEMS],
        ], starting_regions=["Bob-omb Battlefield"])


class TestBobOmbBattlefieldIslandTricks(SM64TestBase):
    run_default_tests = False
    options = {
        **BOB_OPTIONS,
        "one_up_unlocks": Options.OneUpUnlocks.option_not_shuffled,
        "logic_tricks": {
            "Bob-omb Battlefield Island with Wing Cap",
            "Bob-omb Battlefield Island with Long Jump",
            "Bob-omb Battlefield Island with Koopa Shell",
        },
    }

    def test_wing_cap_route(self):
        self.run_location_tests([
            ["Bob-omb Battlefield - Shoot to the Island in the Sky", False, WING_CAP],
            ["Bob-omb Battlefield - Shoot to the Island in the Sky", True,
             WING_CAP + ["Triple Jump"]],
        ], starting_regions=["Bob-omb Battlefield"])

    def test_long_jump_route(self):
        self.run_location_tests([
            ["Bob-omb Battlefield - Shoot to the Island in the Sky", False, []],
            ["Bob-omb Battlefield - Shoot to the Island in the Sky", True, ["Long Jump"]],
        ], starting_regions=["Bob-omb Battlefield"])

    def test_koopa_shell_route(self):
        self.run_location_tests([
            ["Bob-omb Battlefield - Shoot to the Island in the Sky", False, []],
            ["Bob-omb Battlefield - Shoot to the Island in the Sky", True,
             ["Bob-omb Battlefield - Koopa Troopa"]],
        ], starting_regions=["Bob-omb Battlefield"])


class TestBobOmbBattlefieldMarioWingsWithoutWingCap(SM64TestBase):
    run_default_tests = False
    options = {
        **BOB_OPTIONS,
        "logic_tricks": {
            "Bob-omb Battlefield Mario Wings to the Sky without Wing Cap",
        },
    }

    def test_location(self):
        self.run_location_tests([
            ["Bob-omb Battlefield - Mario Wings to the Sky", False, CANNON],
            ["Bob-omb Battlefield - Mario Wings to the Sky", True,
             CANNON + ["Bob-omb Battlefield - Single Yellow Coins"]],
        ], starting_regions=["Bob-omb Battlefield"])


class TestBobOmbBattlefieldMarioWingsWithoutCannon(SM64TestBase):
    run_default_tests = False
    options = {
        **BOB_OPTIONS,
        "logic_tricks": {
            "Bob-omb Battlefield Mario Wings to the Sky without Cannon",
        },
    }

    def test_location(self):
        route = WING_CAP + ["Triple Jump", "Ground Pound"]
        self.run_location_tests([
            ["Bob-omb Battlefield - Mario Wings to the Sky", False,
             WING_CAP + ["Triple Jump"]],
            ["Bob-omb Battlefield - Mario Wings to the Sky", True,
             route + ["Bob-omb Battlefield - Vertical Coin Rings"]],
        ], starting_regions=["Bob-omb Battlefield"])


class TestBobOmbBattlefieldMarioWingsWithoutCoinMarkers(SM64TestBase):
    run_default_tests = False
    options = {
        **BOB_OPTIONS,
        "logic_tricks": {
            "Bob-omb Battlefield Mario Wings to the Sky without Coin Markers",
        },
    }

    def test_location(self):
        self.run_location_tests([
            ["Bob-omb Battlefield - Mario Wings to the Sky", True,
             CANNON + WING_CAP],
        ], starting_regions=["Bob-omb Battlefield"])


class TestBobOmbBattlefieldChainChompTrick(SM64TestBase):
    run_default_tests = False
    options = {
        **BOB_OPTIONS,
        "logic_tricks": {
            "Bob-omb Battlefield Chain Chomp Gate with Bob-omb Clip",
            "Bob-omb Battlefield Chain Chomp Gate with Throwable Cork Box Clip"
        },
    }

    def test_chain_chomp_gate_with_bob_omb(self):
        self.run_location_tests([
            ["Bob-omb Battlefield - Behind Chain Chomp's Gate", False, []],
            ["Bob-omb Battlefield - Behind Chain Chomp's Gate", False,
             ["Bob-omb Battlefield - Bob-ombs"]],
            ["Bob-omb Battlefield - Behind Chain Chomp's Gate", True,
             ["Bob-omb Battlefield - Chain Chomp", "Bob-omb Battlefield - Bob-ombs"]],
        ], starting_regions=["Bob-omb Battlefield"])

    def test_chain_chomp_gate_with_cork_box(self):
        self.run_location_tests([
            ["Bob-omb Battlefield - Behind Chain Chomp's Gate", False, []],
            ["Bob-omb Battlefield - Behind Chain Chomp's Gate", False,
             ["Bob-omb Battlefield - Throwable Cork Boxes"]],
            ["Bob-omb Battlefield - Behind Chain Chomp's Gate", True,
             ["Bob-omb Battlefield - Chain Chomp", "Bob-omb Battlefield - Throwable Cork Boxes"]],
        ], starting_regions=["Bob-omb Battlefield"])
