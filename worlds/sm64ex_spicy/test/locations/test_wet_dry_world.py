from ..bases import SM64TestBase
from ... import Options


WDW_OPTIONS = {
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
    "cap_items": Options.CapItems.option_per_level,
    "wet_dry_world_coin_star_requirement": 1,
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

PURPLE_SWITCH = "Wet-Dry World - Purple Switch"
DIAMOND = "Wet-Dry World - Water Level Diamond"
CANNON = "Wet-Dry World - Cannon Unlock"
VANISH_CAP = "Wet-Dry World - Vanish Cap"
METAL_CAP = "Wet-Dry World - Metal Cap"
RED_COINS = "Wet-Dry World - Red Coins"
THREE_COIN_BLOCKS = "Wet-Dry World - 3-Coin Blocks"
TEN_COIN_BLOCKS = "Wet-Dry World - 10-Coin Blocks"
BREAKABLE_COIN_BOXES = "Wet-Dry World - Breakable Coin Boxes"
HEAVE_HOS = "Wet-Dry World - Heave-Hos"
FREESTANDING_1UPS = "Wet-Dry World - Freestanding 1-Ups"
TRIGGER_1UPS = "Wet-Dry World - Trigger 1-Ups"
BLOCK_1UPS = "Wet-Dry World - 1-Up Blocks"


class TestWetDryWorldLowLocations(SM64TestBase):
    run_default_tests = False
    options = WDW_OPTIONS

    def test_locations(self):
        near_top = [DIAMOND]
        top_of_elevator = near_top + [PURPLE_SWITCH]
        top_of_elevator_without_diamond = [HEAVE_HOS, PURPLE_SWITCH]
        top = top_of_elevator + ["Long Jump"]
        downtown = [CANNON]

        self.run_location_tests([
            ["Wet-Dry World - Shocking Arrow Lifts!", True, []],
            ["Wet-Dry World - Shocking Arrow Lifts Star Block", True, []],

            ["Wet-Dry World - Pedestal 10 Coins Block", False, []],
            ["Wet-Dry World - Pedestal 10 Coins Block", True,
             near_top + [TEN_COIN_BLOCKS]],
            ["Wet-Dry World - Push Block 3 Coins Block", False, []],
            ["Wet-Dry World - Push Block 3 Coins Block", True,
             near_top + [THREE_COIN_BLOCKS]],
            ["Wet-Dry World - Push Block 10 Coins Block", False, []],
            ["Wet-Dry World - Push Block 10 Coins Block", True, [TEN_COIN_BLOCKS]],

            ["Wet-Dry World - Express Elevator--Hurry Up!", False,
             top_of_elevator_without_diamond],
            ["Wet-Dry World - Express Elevator--Hurry Up!", True,
             top_of_elevator_without_diamond + ["Backflip"]],
            ["Wet-Dry World - Express Elevator--Hurry Up!", True,
             top_of_elevator],
            ["Wet-Dry World - Top of Express Elevator 10 Coins Block", False,
             top_of_elevator],
            ["Wet-Dry World - Top of Express Elevator 10 Coins Block", True,
             top_of_elevator + [TEN_COIN_BLOCKS]],
            ["Wet-Dry World - Secrets in the Shallows & Sky", False,
             []],
            ["Wet-Dry World - Secrets in the Shallows & Sky", True, [DIAMOND]],

            ["Wet-Dry World - Top o' the Town", False, top_of_elevator],
            ["Wet-Dry World - Top o' the Town", True, top],
            ["Wet-Dry World - Top o' the Town Star Block", True, top],
            ["Wet-Dry World - Cylinder Lower 1-Up", False, top],
            ["Wet-Dry World - Cylinder Lower 1-Up", True, top + [FREESTANDING_1UPS]],
            ["Wet-Dry World - Cylinder Upper 1-Up", False, top],
            ["Wet-Dry World - Cylinder Upper 1-Up", True, top + [FREESTANDING_1UPS]],

            ["Wet-Dry World - Go to Town for Red Coins", False,
             downtown + [DIAMOND, "Wall Kick", "Kick"]],
            ["Wet-Dry World - Go to Town for Red Coins", True,
             downtown + [DIAMOND, "Wall Kick", "Kick", RED_COINS]],
            ["Wet-Dry World - Quick Race Through Downtown!", False,
             downtown + [DIAMOND, "Wall Kick"]],
            ["Wet-Dry World - Quick Race Through Downtown!", True,
             downtown + [DIAMOND, "Wall Kick", VANISH_CAP]],
            ["Wet-Dry World - Downtown Block 1-Up", False,
             downtown + [DIAMOND]],
            ["Wet-Dry World - Downtown Block 1-Up", True,
             downtown + [DIAMOND, BLOCK_1UPS]],
            ["Wet-Dry World - Downtown Center Coin Ring 1-Up", False, downtown],
            ["Wet-Dry World - Downtown Center Coin Ring 1-Up", True,
             downtown + [TRIGGER_1UPS]],
            ["Wet-Dry World - Downtown Vanish Cap Block", False,
             downtown + [DIAMOND]],
            ["Wet-Dry World - Downtown Vanish Cap Block", True,
             downtown + [DIAMOND, VANISH_CAP]],
            ["Wet-Dry World - Metal Cap Block", False, downtown],
            ["Wet-Dry World - Metal Cap Block", True, downtown + [METAL_CAP]],
            ["Wet-Dry World - Quick Race Through Downtown Star Vanish Cap Block",
             False, downtown + [DIAMOND]],
            ["Wet-Dry World - Quick Race Through Downtown Star Vanish Cap Block",
             True, downtown + [DIAMOND, VANISH_CAP]],
            ["Wet-Dry World - Downtown 1-Up Block", False, downtown],
            ["Wet-Dry World - Downtown 1-Up Block", True,
             downtown + [DIAMOND, BLOCK_1UPS]],

            ["Wet-Dry World - Coins Star", False, []],
            ["Wet-Dry World - Coins Star", True,
             [BREAKABLE_COIN_BOXES]],
        ], starting_regions=["Wet-Dry World - Low Water"])

    def test_heave_hos_reach_near_top(self):
        self.run_location_tests([
            ["Wet-Dry World - Push Block 3 Coins Block", False, [THREE_COIN_BLOCKS]],
            ["Wet-Dry World - Push Block 3 Coins Block", True,
             [HEAVE_HOS, THREE_COIN_BLOCKS]],
            ["Wet-Dry World - Top o' the Town", False, [HEAVE_HOS]],
            ["Wet-Dry World - Top o' the Town", True, [HEAVE_HOS, "Side Flip"]],
        ], starting_regions=["Wet-Dry World - Low Water"])


class TestWetDryWorldMiddleLocations(SM64TestBase):
    run_default_tests = False
    options = WDW_OPTIONS

    def test_middle_water_block(self):
        self.run_location_tests([
            ["Wet-Dry World - Wooden Structure 3 Coins Block", False, []],
            ["Wet-Dry World - Wooden Structure 3 Coins Block", True,
             [THREE_COIN_BLOCKS]],
            ["Wet-Dry World - Pedestal 10 Coins Block", False, [TEN_COIN_BLOCKS]],
            ["Wet-Dry World - Pedestal 10 Coins Block", True,
             ["Side Flip", TEN_COIN_BLOCKS]],
        ], starting_regions=["Wet-Dry World - Mid Water"])


class TestWetDryWorldHighLocations(SM64TestBase):
    run_default_tests = False
    options = WDW_OPTIONS

    def test_highest_water_reaches_top_freely(self):
        self.run_location_tests([
            ["Wet-Dry World - Top o' the Town", True, []],
        ], starting_regions=["Wet-Dry World - Highest Water"])

    def test_highest_water_buddy_route(self):
        self.run_location_tests([
            ["Wet-Dry World - Bob-omb Buddy", False, []],
            ["Wet-Dry World - Bob-omb Buddy", True,
             ["Triple Jump", "Wet-Dry World - Bob-omb Buddy"]],
            ["Wet-Dry World - Bob-omb Buddy", True,
             ["Backflip", "Wet-Dry World - Bob-omb Buddy"]],
            ["Wet-Dry World - Bob-omb Buddy", True,
             ["Side Flip", "Wet-Dry World - Bob-omb Buddy"]],
        ], starting_regions=["Wet-Dry World - Highest Water"])

    def test_highest_water_does_not_reach_shocking_arrow_lifts_via_top(self):
        self.run_location_tests([
            ["Wet-Dry World - Shocking Arrow Lifts!", False, []],
            ["Wet-Dry World - Shocking Arrow Lifts!", False,
             ["Ground Pound", "Triple Jump", "Ledge Grab"]],
            ["Wet-Dry World - Shocking Arrow Lifts Star Block", False, []],
            ["Wet-Dry World - Wooden Structure 3 Coins Block", False,
             ["Wet-Dry World - 3-Coin Blocks", "Long Jump", "Purple Switches"]],
        ], starting_regions=["Wet-Dry World - Highest Water"])

    def test_separately_reached_water_and_top_states_do_not_combine(self):
        self.run_location_tests([
            ["Wet-Dry World - Shocking Arrow Lifts!", False, []],
        ], starting_regions=[
            "Wet-Dry World - Highest Water",
            "Wet-Dry World - Mid-High Water",
        ])
        self.run_location_tests([
            ["Wet-Dry World - Wooden Structure 3 Coins Block", False,
             [THREE_COIN_BLOCKS]],
        ], starting_regions=[
            "Wet-Dry World - Highest Water",
            "Wet-Dry World - Low Water",
        ])


class TestWetDryWorldShockingArrowLiftsGroundPoundTrick(SM64TestBase):
    run_default_tests = False
    options = {
        **WDW_OPTIONS,
        "logic_tricks": {"Wet-Dry World Ground Pound Underwater Shocking Arrow Lifts Box"},
    }

    def test_highest_water_cannon_route_accepts_ground_pound_trick(self):
        self.run_location_tests([
            ["Wet-Dry World - Shocking Arrow Lifts!", False, []],
            ["Wet-Dry World - Shocking Arrow Lifts!", True, ["Ground Pound"]],
        ], starting_regions=["Wet-Dry World - Highest Water"])


class TestWetDryWorldDowntownTripleJumpTrick(SM64TestBase):
    run_default_tests = False
    options = {
        **WDW_OPTIONS,
        "logic_tricks": {"Wet-Dry World Downtown with Triple Jump"},
    }

    def test_top_connects_to_downtown_with_triple_jump(self):
        top_access = [DIAMOND, PURPLE_SWITCH, "Long Jump", TRIGGER_1UPS]
        self.run_location_tests([
            ["Wet-Dry World - Downtown Center Coin Ring 1-Up", False,
             top_access],
            ["Wet-Dry World - Downtown Center Coin Ring 1-Up", True,
             top_access + ["Triple Jump"]],
        ], starting_regions=["Wet-Dry World - Low Water"])


class TestWetDryWorldHighRedCoinsTripleJumpTrick(SM64TestBase):
    run_default_tests = False
    options = {
        **WDW_OPTIONS,
        "logic_tricks": {"Wet-Dry World High Red Coins with Triple Jump"},
    }

    def test_red_coin_star_accepts_triple_jump_instead_of_wall_kick(self):
        requirements = [CANNON, DIAMOND, RED_COINS]
        self.run_location_tests([
            ["Wet-Dry World - Go to Town for Red Coins", False, requirements],
            ["Wet-Dry World - Go to Town for Red Coins", True,
             requirements + ["Wall Kick"]],
            ["Wet-Dry World - Go to Town for Red Coins", True,
             requirements + ["Triple Jump"]],
        ], starting_regions=["Wet-Dry World - Low Water"])


class TestWetDryWorldFullLevelUnlock(SM64TestBase):
    run_default_tests = False
    options = WDW_OPTIONS

    def test_painting_unlock(self):
        upstairs = ["Progressive Upstairs Key"]
        self.run_location_tests([
            ["Wet-Dry World - Shocking Arrow Lifts!", False, upstairs],
            ["Wet-Dry World - Shocking Arrow Lifts!", True,
             upstairs + ["Unlock Wet-Dry World"]],
        ], starting_regions=["Castle Grounds"])


class TestWetDryWorldGlobalUnlockModes(SM64TestBase):
    run_default_tests = False
    options = {
        **WDW_OPTIONS,
        "coin_object_unlocks": Options.CoinObjectUnlocks.option_global,
        "one_up_unlocks": Options.OneUpUnlocks.option_global,
        "level_features": Options.LevelFeatures.option_global,
        "bobomb_buddies": Options.BobombBuddies.option_global,
    }

    def test_global_items_replace_per_level_items(self):
        top = [DIAMOND, "Purple Switches", "Long Jump"]
        self.run_location_tests([
            ["Wet-Dry World - Coins Star", True,
             ["Wet-Dry World - Breakable Coin Boxes"]],
            ["Wet-Dry World - Coins Star", True, ["Breakable Coin Boxes"]],
            ["Wet-Dry World - Cylinder Lower 1-Up", True,
             top + ["Wet-Dry World - Freestanding 1-Ups"]],
            ["Wet-Dry World - Cylinder Lower 1-Up", True,
             top + ["Freestanding 1-Ups"]],
        ], starting_regions=["Wet-Dry World - Low Water"])


class TestWetDryWorldNotShuffledUnlockModes(SM64TestBase):
    run_default_tests = False
    options = {
        **WDW_OPTIONS,
        "level_unlocks": Options.LevelUnlocks.option_disabled,
        "coin_object_unlocks": Options.CoinObjectUnlocks.option_not_shuffled,
        "one_up_unlocks": Options.OneUpUnlocks.option_not_shuffled,
        "level_features": Options.LevelFeatures.option_not_shuffled,
        "bobomb_buddies": Options.BobombBuddies.option_not_shuffled,
    }

    def test_not_shuffled_items_require_no_inventory(self):
        self.run_location_tests([
            ["Wet-Dry World - Coins Star", True, []],
            ["Wet-Dry World - Cylinder Lower 1-Up", True, ["Long Jump"]],
        ], starting_regions=["Wet-Dry World - Low Water"])
        self.run_location_tests([
            ["Wet-Dry World - Shocking Arrow Lifts!", True,
             ["Progressive Upstairs Key"]],
        ], starting_regions=["Castle Grounds"])
