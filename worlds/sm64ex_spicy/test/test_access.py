from .bases import SM64TestBase
from .. import Options
from ..Regions import sm64_ttc_entrances
from ..Rules import get_per_level_action_item_name


SHUFFLED_ARBITRARY_FEATURE_OPTIONS = {
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
}

SHUFFLED_GLOBAL_MOVE_OPTIONS = {
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

ONE_COIN_STAR_REQUIREMENTS = {
    option_name: 1 for option_name in Options.coin_star_requirement_option_names
}


class GroupedCastleKeyAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "enable_locked_paintings": Options.EnableLockedPaintings.option_false,
        "one_up_checks": Options.OneUpChecks.option_true,
        "area_rando": Options.AreaRandomizer.option_Off,
    }

    def test_BitDW_entrance_access(self):
        self.assertFalse(self.can_reach_region("Bowser in the Dark World"))
        self.collect(self.get_item_by_name("Dark World Key"))
        self.assertTrue(self.can_reach_region("Bowser in the Dark World"))

    def test_basement_access(self):
        self.assertFalse(self.can_reach_region("Basement"))
        self.collect(self.get_item_by_name("Progressive Basement Key"))
        self.assertTrue(self.can_reach_region("Basement"))

    def test_DDD_entrance_access(self):
        self.assertFalse(self.can_reach_region("Dire, Dire Docks"))
        self.collect([self.get_item_by_name("Progressive Basement Key")] * 2)
        self.assertTrue(self.can_reach_region("Dire, Dire Docks"))

    def test_BitFS_entrance_access(self):
        self.assertFalse(self.can_reach_region("Bowser in the Fire Sea"))
        self.collect([self.get_item_by_name("Progressive Basement Key")] * 2)
        self.assertFalse(self.can_reach_region("Bowser in the Fire Sea"))
        self.collect(self.get_item_by_name("Unlock Bowser in the Fire Sea"))
        self.assertTrue(self.can_reach_region("Bowser in the Fire Sea"))

    def test_second_floor_access(self):
        self.assertFalse(self.can_reach_region("Second Floor"))
        self.collect(self.get_item_by_name("Progressive Upstairs Key"))
        self.assertTrue(self.can_reach_region("Second Floor"))

    def test_third_floor_access(self):
        self.assertFalse(self.can_reach_region("Third Floor"))
        self.collect([self.get_item_by_name("Progressive Upstairs Key")] * 2)
        self.assertTrue(self.can_reach_region("Third Floor"))

    def test_BitS_entrance_access(self):
        self.assertFalse(self.can_reach_region("Bowser in the Sky"))
        self.collect([self.get_item_by_name("Progressive Upstairs Key")] * 3)
        self.assertTrue(self.can_reach_region("Bowser in the Sky"))

    def test_legacy_key_compatibility(self):
        self.assertFalse(self.can_reach_region("Basement"))
        self.collect(self.world.create_item("Basement Key"))
        self.assertTrue(self.can_reach_region("Basement"))

        self.assertFalse(self.can_reach_region("Second Floor"))
        self.collect(self.world.create_item("Second Floor Key"))
        self.assertTrue(self.can_reach_region("Second Floor"))


class CastleAquariumLogicTricksTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "one_up_checks": Options.OneUpChecks.option_true,
        "area_rando": Options.AreaRandomizer.option_Off,
        "logic_tricks": {"Castle Secret Aquarium Entrance with Triple Jump Only"},
    }

    def test_triple_jump_reaches_aquarium_and_lobby_one_up(self):
        self.assertFalse(self.can_reach_region("The Secret Aquarium"))
        self.collect(self.get_item_by_name("Triple Jump"))
        self.assertTrue(self.can_reach_region("The Secret Aquarium"))
        self.assertTrue(self.can_reach_location("Castle - Jolly Roger Bay Lobby 1-Up"))


class CastleWaterfallTreeLogicTrickTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "one_up_checks": Options.OneUpChecks.option_true,
        "area_rando": Options.AreaRandomizer.option_Off,
        "logic_tricks": {"Castle Third Tree From Waterfall 1-Up With No Movement"},
    }

    def test_no_movement_trick_reaches_tree_one_up(self):
        self.assertTrue(self.can_reach_location("Castle - Third Tree From Waterfall 1-Up"))


class CastleTTCLogicTricksTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "area_rando": Options.AreaRandomizer.option_Off,
        "logic_tricks": {"Castle Tick Tock Clock Entrance With Long Jump and Kick"},
    }

    def test_long_jump_and_kick_reach_ttc(self):
        self.collect([self.get_item_by_name("Progressive Upstairs Key")] * 2)
        self.collect(self.get_item_by_name("Long Jump"))
        self.assertFalse(self.can_reach_region("Tick Tock Clock"))
        self.collect(self.get_item_by_name("Kick"))
        self.assertTrue(self.can_reach_region("Tick Tock Clock"))


class CastleThirdFloorAlcoveLogicTricksTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "area_rando": Options.AreaRandomizer.option_Off,
        "logic_tricks": {"Castle Third Floor Alcoves With Dive and Ledge Grab"},
    }

    def test_dive_and_ledge_grab_reach_both_alcoves(self):
        self.collect([self.get_item_by_name("Progressive Upstairs Key")] * 2)
        self.collect(self.get_item_by_name("Dive"))
        self.assertFalse(self.can_reach_region("Rainbow Ride"))
        self.assertFalse(self.can_reach_region("Wing Mario Over the Rainbow"))
        self.collect(self.get_item_by_name("Ledge Grab"))
        self.assertTrue(self.can_reach_region("Rainbow Ride"))
        self.assertTrue(self.can_reach_region("Wing Mario Over the Rainbow"))


class CastleThirtyStarDoorLogicTricksTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "area_rando": Options.AreaRandomizer.option_Off,
        "logic_tricks": {"Castle Crackslide Through the 30 Star Door With Backflip, Kick, Double Jump, and Ledge grab"},
    }

    def test_crackslide_requires_every_listed_move(self):
        self.collect(self.get_item_by_name("Progressive Basement Key"))
        for item_name in ("Backflip", "Kick", "Triple Jump"):
            self.collect(self.get_item_by_name(item_name))
        self.assertFalse(self.can_reach_region("Dire, Dire Docks"))
        self.collect(self.get_item_by_name("Ledge Grab"))
        self.assertTrue(self.can_reach_region("Dire, Dire Docks"))


class CastleThirtyStarDoorSBLJLogicTricksTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "area_rando": Options.AreaRandomizer.option_Off,
        "logic_tricks": {"Castle Side Backwards Long Jump Through the 30 Star Door"},
    }

    def test_sblj_requires_only_long_jump(self):
        self.collect(self.get_item_by_name("Progressive Basement Key"))
        self.assertFalse(self.can_reach_entrance("Basement -> Dire, Dire Docks"))
        self.collect(self.get_item_by_name("Long Jump"))
        self.assertTrue(self.can_reach_entrance("Basement -> Dire, Dire Docks"))


class CastleThirtyStarDoorDoubleJumpLogicTricksTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "area_rando": Options.AreaRandomizer.option_Off,
        "logic_tricks": {"Castle Crackslide Through the 30 Star Door With Double Jump Setup"},
    }

    def test_double_jump_setup_uses_triple_jump_item(self):
        self.collect(self.get_item_by_name("Progressive Basement Key"))
        self.collect(self.get_item_by_name("Ledge Grab"))
        self.assertFalse(self.can_reach_entrance("Basement -> Dire, Dire Docks"))
        self.collect(self.get_item_by_name("Triple Jump"))
        self.assertTrue(self.can_reach_entrance("Basement -> Dire, Dire Docks"))


class CastleMIPSSkipLogicTricksTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "area_rando": Options.AreaRandomizer.option_Off,
        "logic_tricks": {"Castle MIPS Skip Through the 30 Star Door"},
    }

    def test_mips_skip_requires_one_mips_and_dive(self):
        self.collect(self.get_item_by_name("Progressive Basement Key"))
        self.collect(self.get_item_by_name("Castle - Progressive MIPS"))
        self.assertFalse(self.can_reach_entrance("Basement -> Dire, Dire Docks"))
        self.collect(self.get_item_by_name("Dive"))
        self.assertTrue(self.can_reach_entrance("Basement -> Dire, Dire Docks"))


class CastleMIPSSkipWithoutDiveLogicTricksTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "area_rando": Options.AreaRandomizer.option_Off,
        "logic_tricks": {
            "Castle MIPS Skip Through the 30 Star Door",
            "Castle MIPS Without Dive",
        },
    }

    def test_mips_without_dive_trick_removes_dive_requirement(self):
        self.collect(self.get_item_by_name("Progressive Basement Key"))
        self.assertFalse(self.can_reach_entrance("Basement -> Dire, Dire Docks"))
        self.collect(self.get_item_by_name("Castle - Progressive MIPS"))
        self.assertTrue(self.can_reach_entrance("Basement -> Dire, Dire Docks"))
        self.assertTrue(self.can_reach_location("Castle - MIPS 1"))


class CastleDoorBLJLogicTricksTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "area_rando": Options.AreaRandomizer.option_Off,
        "logic_tricks": {
            "Castle Backwards Long Jump Through the 50 Star Door",
            "Castle Backwards Long Jump Through the 70 Star Door",
        },
    }

    def test_fifty_and_seventy_star_door_blj_require_long_jump(self):
        self.collect(self.get_item_by_name("Progressive Upstairs Key"))
        self.assertFalse(self.can_reach_region("Third Floor"))
        self.collect(self.get_item_by_name("Long Jump"))
        self.assertTrue(self.can_reach_region("Third Floor"))
        self.assertTrue(self.can_reach_region("Bowser in the Sky"))


class SingleProgressiveKeyAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_true,
        "enable_locked_paintings": Options.EnableLockedPaintings.option_false,
        "area_rando": Options.AreaRandomizer.option_Off,
    }

    def collect_progressive_keys(self, count: int):
        self.collect([self.get_item_by_name("Progressive Key")] * count)

    def test_progressive_key_tiers(self):
        self.assertFalse(self.can_reach_region("Bowser in the Dark World"))
        self.collect_progressive_keys(1)
        self.assertTrue(self.can_reach_region("Bowser in the Dark World"))

        self.assertFalse(self.can_reach_region("Basement"))
        self.collect_progressive_keys(1)
        self.assertTrue(self.can_reach_region("Basement"))

        self.assertFalse(self.can_reach_region("Dire, Dire Docks"))
        self.collect_progressive_keys(1)
        self.assertTrue(self.can_reach_region("Dire, Dire Docks"))

        self.assertFalse(self.can_reach_region("Second Floor"))
        self.collect_progressive_keys(1)
        self.assertTrue(self.can_reach_region("Second Floor"))

        self.assertFalse(self.can_reach_region("Third Floor"))
        self.collect_progressive_keys(1)
        self.assertTrue(self.can_reach_region("Third Floor"))

        self.assertFalse(self.can_reach_region("Bowser in the Sky"))
        self.collect_progressive_keys(1)
        self.assertTrue(self.can_reach_region("Bowser in the Sky"))

    def test_BitFS_entrance_access(self):
        self.collect_progressive_keys(3)
        self.assertFalse(self.can_reach_region("Bowser in the Fire Sea"))
        self.collect(self.get_item_by_name("Unlock Bowser in the Fire Sea"))
        self.assertTrue(self.can_reach_region("Bowser in the Fire Sea"))


class LockedPaintingAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        "area_rando": Options.AreaRandomizer.option_Off,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "enable_locked_paintings": Options.EnableLockedPaintings.option_true,
    }

    def test_hazy_maze_cave_requires_unlock(self):
        self.collect(self.get_item_by_name("Progressive Basement Key"))
        self.assertFalse(self.can_reach_entrance("Basement -> Hazy Maze Cave"))

        self.collect(self.get_item_by_name("Unlock Hazy Maze Cave"))
        self.assertTrue(self.can_reach_entrance("Basement -> Hazy Maze Cave"))

    def test_tiny_island_requires_tiny_unlock(self):
        self.collect(self.get_item_by_name("Progressive Upstairs Key"))
        self.collect(self.get_item_by_name("Unlock Huge Island"))
        self.assertFalse(self.can_reach_entrance("Second Floor -> Tiny-Huge Island (Tiny)"))
        self.assertTrue(self.can_reach_entrance("Second Floor -> Tiny-Huge Island (Huge)"))

    def test_huge_island_requires_huge_unlock(self):
        self.collect(self.get_item_by_name("Progressive Upstairs Key"))
        self.collect(self.get_item_by_name("Unlock Tiny Island"))
        self.assertTrue(self.can_reach_entrance("Second Floor -> Tiny-Huge Island (Tiny)"))
        self.assertFalse(self.can_reach_entrance("Second Floor -> Tiny-Huge Island (Huge)"))


class UTGlitchLogicTestBase(SM64TestBase):
    options = {
        "buddy_checks": Options.BuddyChecks.option_true,
        "ground_pound": Options.GroundPound.option_global,
        "universal_tracker_glitched_logic": {"All Hard Tricks"},
    }

    def test_ut_glitch_satisfies_moveless(self):
        self.assertFalse(self.can_reach_location("Bob-omb Battlefield - Behind Chain Chomp's Gate"))
        self.collect(self.world.create_item("ut_glitch"))
        self.assertTrue(self.can_reach_location("Bob-omb Battlefield - Behind Chain Chomp's Gate"))

    def test_ut_glitch_satisfies_capless(self):
        self.collect(self.world.create_item("Bob-omb Battlefield - Cannon Unlock"))
        self.assertFalse(self.can_reach_location("Bob-omb Battlefield - Mario Wings to the Sky"))
        self.collect(self.world.create_item("ut_glitch"))
        self.assertTrue(self.can_reach_location("Bob-omb Battlefield - Mario Wings to the Sky"))

    def test_ut_glitch_satisfies_cannonless(self):
        self.collect(self.world.create_item("Wing Cap"))
        self.assertFalse(self.can_reach_location("Bob-omb Battlefield - Shoot to the Island in the Sky"))
        self.collect(self.world.create_item("ut_glitch"))
        self.assertTrue(self.can_reach_location("Bob-omb Battlefield - Shoot to the Island in the Sky"))


class SelectiveUTGlitchLogicTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "buddy_checks": Options.BuddyChecks.option_true,
        "logic_tricks": {"All Easy Tricks"},
        "universal_tracker_glitched_logic": {"All Medium Tricks"},
    }

    def test_regular_logic_trick_does_not_require_ut_glitch(self):
        self.collect([self.get_item_by_name("Wing Cap"), self.get_item_by_name("Triple Jump")])
        self.assertTrue(self.can_reach_region("Bob-omb Battlefield - Island"))

    def test_selected_tracker_trick_requires_ut_glitch(self):
        self.collect(self.get_item_by_name("Bob-omb Battlefield - Cannon Unlock"))
        self.assertFalse(self.can_reach_location("Bob-omb Battlefield - Mario Wings to the Sky"))
        self.collect(self.world.create_item("ut_glitch"))
        self.assertTrue(self.can_reach_location("Bob-omb Battlefield - Mario Wings to the Sky"))

    def test_unselected_hard_trick_remains_out_of_logic_with_ut_glitch(self):
        self.collect([self.get_item_by_name("Long Jump"), self.world.create_item("ut_glitch")])
        self.assertFalse(self.can_reach_region("Bob-omb Battlefield - Island"))

    def test_tracker_trick_selection_is_in_slot_data(self):
        options = self.world.fill_slot_data()["Options"]
        self.assertEqual(options["logic_tricks"], ["All Easy Tricks"])
        self.assertEqual(options["universal_tracker_glitched_logic"], ["All Medium Tricks"])


class BobOmbBattlefieldEasyLogicTricksTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "buddy_checks": Options.BuddyChecks.option_true,
        "logic_tricks": {"All Easy Tricks"},
    }

    def test_island_with_wing_cap(self):
        self.collect([self.get_item_by_name("Wing Cap"), self.get_item_by_name("Triple Jump")])
        self.assertTrue(self.can_reach_region("Bob-omb Battlefield - Island"))

    def test_island_red_coin_with_ground_pound_does_not_unlock_island(self):
        self.collect(self.get_item_by_name("Ground Pound"))
        self.assertFalse(self.can_reach_region("Bob-omb Battlefield - Island"))


class BobOmbBattlefieldMediumLogicTricksTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "buddy_checks": Options.BuddyChecks.option_true,
        "logic_tricks": {"All Medium Tricks"},
    }

    def test_mario_wings_without_wing_cap(self):
        self.collect(self.get_item_by_name("Bob-omb Battlefield - Cannon Unlock"))
        self.assertTrue(self.can_reach_location("Bob-omb Battlefield - Mario Wings to the Sky"))


class BobOmbBattlefieldHardLogicTricksTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "buddy_checks": Options.BuddyChecks.option_true,
        "logic_tricks": {"All Hard Tricks"},
    }

    def test_island_with_long_jump(self):
        self.collect(self.get_item_by_name("Long Jump"))
        self.assertTrue(self.can_reach_region("Bob-omb Battlefield - Island"))

    def test_island_with_koopa_shell(self):
        self.assertTrue(self.can_reach_region("Bob-omb Battlefield - Island"))

    def test_chain_chomp_gate_without_ground_pound(self):
        self.assertTrue(self.can_reach_location("Bob-omb Battlefield - Behind Chain Chomp's Gate"))

    def test_mario_wings_without_cannon(self):
        self.collect([
            self.get_item_by_name("Wing Cap"),
            self.get_item_by_name("Triple Jump"),
            self.get_item_by_name("Ground Pound"),
        ])
        self.assertTrue(self.can_reach_location("Bob-omb Battlefield - Mario Wings to the Sky"))


class BobOmbBattlefieldCannonlessMarioWingsCoinTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "buddy_checks": Options.BuddyChecks.option_true,
        "bob_omb_battlefield_coin_star_requirement": 146,
        "logic_tricks": {"Bob-omb Battlefield Mario Wings to the Sky without Cannon"},
    }

    def test_cannonless_mario_wings_puts_every_coin_in_logic(self):
        self.collect([
            self.get_item_by_name("Wing Cap"),
            self.get_item_by_name("Triple Jump"),
            self.get_item_by_name("Ground Pound"),
        ])
        self.assertTrue(self.can_reach_location("Bob-omb Battlefield - Coins Star"))


class BobOmbBattlefieldKoopaShellCoinTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "buddy_checks": Options.BuddyChecks.option_true,
        "bob_omb_battlefield_coin_star_requirement": 104,
        "logic_tricks": {"Bob-omb Battlefield Island with Koopa Shell"},
    }

    def test_koopa_shell_adds_only_island_and_red_coin_coins(self):
        self.assertTrue(self.can_reach_region("Bob-omb Battlefield - Island"))
        self.assertTrue(self.can_reach_location("Bob-omb Battlefield - Coins Star"))


class BobOmbBattlefieldKoopaShellCoinLimitTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "buddy_checks": Options.BuddyChecks.option_true,
        "bob_omb_battlefield_coin_star_requirement": 105,
        "logic_tricks": {"Bob-omb Battlefield Island with Koopa Shell"},
    }

    def test_koopa_shell_does_not_add_other_nearby_coins(self):
        self.assertFalse(self.can_reach_location("Bob-omb Battlefield - Coins Star"))


class CastleFeatureAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "enable_locked_paintings": Options.EnableLockedPaintings.option_false,
        "one_up_checks": Options.OneUpChecks.option_true,
        "area_rando": Options.AreaRandomizer.option_Off,
    }

    def test_mips_access(self):
        self.assertFalse(self.can_reach_location("Castle - MIPS 1"))
        self.collect(self.get_item_by_name("Progressive Basement Key"))
        self.assertFalse(self.can_reach_location("Castle - MIPS 1"))
        self.collect(self.get_item_by_name("Castle - Progressive MIPS"))
        self.assertTrue(self.can_reach_location("Castle - MIPS 1"))
        self.assertFalse(self.can_reach_location("Castle - MIPS 2"))
        self.collect(self.get_item_by_name("Castle - Progressive MIPS"))
        self.assertTrue(self.can_reach_location("Castle - MIPS 2"))

    def test_castle_toad_access(self):
        self.assertFalse(self.can_reach_location("Castle - Toad (Basement)"))
        self.collect(self.get_item_by_name("Castle - Toads"))
        self.collect(self.get_item_by_name("Progressive Basement Key"))
        self.assertTrue(self.can_reach_location("Castle - Toad (Basement)"))

        self.assertFalse(self.can_reach_location("Castle - Toad (Second Floor)"))
        self.collect(self.get_item_by_name("Progressive Upstairs Key"))
        self.assertTrue(self.can_reach_location("Castle - Toad (Second Floor)"))

        self.assertFalse(self.can_reach_location("Castle - Toad (Third Floor)"))
        self.collect(self.get_item_by_name("Progressive Upstairs Key"))
        self.assertTrue(self.can_reach_location("Castle - Toad (Third Floor)"))

    def test_castle_feature_regions(self):
        self.assertFalse(self.can_reach_region("Big Boo's Haunt"))
        self.collect(self.get_item_by_name("Unlock Big Boo's Haunt"))
        self.assertTrue(self.can_reach_region("Big Boo's Haunt"))

        self.assertFalse(self.can_reach_region("Tower of the Wing Cap"))
        self.collect(self.get_item_by_name("Unlock Tower of the Wing Cap"))
        self.assertTrue(self.can_reach_region("Tower of the Wing Cap"))

        self.assertFalse(self.can_reach_region("Wing Mario Over the Rainbow"))
        self.collect(self.get_item_by_name("Castle - Cannon Unlock"))
        self.assertFalse(self.can_reach_region("Wing Mario Over the Rainbow"))
        self.collect([self.get_item_by_name("Progressive Upstairs Key")] * 2)
        self.assertTrue(self.can_reach_region("Wing Mario Over the Rainbow"))

    def test_drain_the_moat_access_uses_old_vcutm_entrance_logic(self):
        self.assertFalse(self.can_reach_location("Castle - Drain the Moat"))
        self.collect(self.get_item_by_name("Progressive Basement Key"))
        self.assertTrue(self.can_reach_location("Castle - Drain the Moat"))

    def test_vcutm_entrance_not_unlocked_by_old_basement_route(self):
        self.assertFalse(self.can_reach_region("Vanish Cap Under the Moat"))
        self.collect(self.get_item_by_name("Progressive Basement Key"))
        self.assertFalse(self.can_reach_region("Vanish Cap Under the Moat"))

    def test_vcutm_entrance_requires_unlock_item_only(self):
        self.assertFalse(self.can_reach_region("Vanish Cap Under the Moat"))
        self.collect(self.get_item_by_name("Unlock Vanish Cap Under the Moat"))
        self.assertTrue(self.can_reach_region("Vanish Cap Under the Moat"))

    def test_yoshi_access(self):
        self.assertFalse(self.can_reach_location("Castle - Yoshi"))
        self.collect(self.get_item_by_name("Castle - Cannon Unlock"))
        self.assertFalse(self.can_reach_location("Castle - Yoshi"))
        self.collect(self.get_item_by_name("Castle - Yoshi"))
        self.assertTrue(self.can_reach_location("Castle - Yoshi"))

    def test_yoshi_access_requires_castle_cannon(self):
        self.collect(self.get_item_by_name("Castle - Yoshi"))
        self.assertFalse(self.can_reach_location("Castle - Yoshi"))
        self.collect(self.get_item_by_name("Castle - Cannon Unlock"))
        self.assertTrue(self.can_reach_location("Castle - Yoshi"))

    def test_castle_roof_1ups_require_castle_cannon_region(self):
        for location_name in (
                "Castle - Roof Back 1-Up",
                "Castle - Roof Center 1-Up",
                "Castle - Roof Front 1-Up",
        ):
            with self.subTest(location=location_name):
                self.assertFalse(self.can_reach_location(location_name))
        self.collect(self.get_item_by_name("Castle - Cannon Unlock"))
        for location_name in (
                "Castle - Roof Back 1-Up",
                "Castle - Roof Center 1-Up",
                "Castle - Roof Front 1-Up",
        ):
            with self.subTest(location=location_name):
                self.assertTrue(self.can_reach_location(location_name))


class CastleOneUpAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "enable_locked_paintings": Options.EnableLockedPaintings.option_false,
        "one_up_checks": Options.OneUpChecks.option_true,
        "area_rando": Options.AreaRandomizer.option_Off,
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
    }

    def test_castle_tree_1up_accepts_side_flip(self):
        self.assertFalse(self.can_reach_location("Castle - Third Tree From Waterfall 1-Up"))
        self.collect(self.get_item_by_name("Side Flip"))
        self.assertTrue(self.can_reach_location("Castle - Third Tree From Waterfall 1-Up"))

    def test_castle_bridge_coins_1up_requires_moat_drained_route_and_movement(self):
        self.collect([
            self.get_item_by_name("Progressive Basement Key"),
            self.get_item_by_name("Ground Pound"),
            self.get_item_by_name("Wall Kick"),
        ])
        self.assertTrue(self.can_reach_location("Castle - Drain the Moat"))
        self.assertFalse(self.can_reach_location("Castle - Bridge Coins 1-Up"))
        self.collect(self.get_item_by_name("Side Flip"))
        self.assertTrue(self.can_reach_location("Castle - Bridge Coins 1-Up"))

    def test_castle_jolly_roger_bay_lobby_1up_uses_secret_aquarium_logic(self):
        self.assertFalse(self.can_reach_location("Castle - Jolly Roger Bay Lobby 1-Up"))
        self.collect(self.get_item_by_name("Side Flip"))
        self.assertTrue(self.can_reach_location("Castle - Jolly Roger Bay Lobby 1-Up"))


class CourseOneUpAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "enable_locked_paintings": Options.EnableLockedPaintings.option_false,
        "buddy_checks": Options.BuddyChecks.option_true,
        "one_up_checks": Options.OneUpChecks.option_true,
        "area_rando": Options.AreaRandomizer.option_Off,
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
    }

    def collect_basement_access(self):
        self.collect(self.get_item_by_name("Progressive Basement Key"))

    def test_bob_cannon_tree_1up_accepts_side_flip(self):
        self.collect(self.get_item_by_name("Bob-omb Battlefield - Cannon Unlock"))
        self.assertFalse(self.can_reach_location("Bob-omb Battlefield - Cannon Tree 1-Up"))
        self.collect(self.get_item_by_name("Side Flip"))
        self.assertTrue(self.can_reach_location("Bob-omb Battlefield - Cannon Tree 1-Up"))

    def test_wf_flagpole_1up_requires_climb(self):
        self.assertFalse(self.can_reach_location("Whomp's Fortress - Flagpole 1-Up"))
        self.collect(self.get_item_by_name("Climb"))
        self.assertTrue(self.can_reach_location("Whomp's Fortress - Flagpole 1-Up"))

    def test_jrb_stone_pillar_1up_requires_cannon(self):
        self.assertFalse(self.can_reach_location("Jolly Roger Bay - Stone Pillar 1-Up"))
        self.collect(self.get_item_by_name("Jolly Roger Bay - Cannon Unlock"))
        self.assertTrue(self.can_reach_location("Jolly Roger Bay - Stone Pillar 1-Up"))

    def test_jrb_underwater_coin_ring_1up_has_no_extra_rule(self):
        self.assertTrue(self.can_reach_location("Jolly Roger Bay - Underwater Coin Ring 1-Up"))

    def test_ccm_snowman_tree_1up_has_no_extra_rule(self):
        self.assertTrue(self.can_reach_location("Cool, Cool Mountain - Snowman Tree 1-Up"))

    def test_ccm_slide_1ups_have_no_extra_rule(self):
        self.assertTrue(self.can_reach_location("Cool, Cool Mountain - Slide Shortcut First 1-Up"))
        active_locations = {location.name for location in self.multiworld.get_locations(self.player)}
        self.assertNotIn("Cool, Cool Mountain - Slide Shortcut Second 1-Up", active_locations)

    def test_bbh_shed_roof_1up_accepts_side_flip(self):
        self.collect(self.get_item_by_name("Unlock Big Boo's Haunt"))
        self.assertFalse(self.can_reach_location("Big Boo's Haunt - Shed Roof 1-Up"))
        self.collect(self.get_item_by_name("Side Flip"))
        self.assertTrue(self.can_reach_location("Big Boo's Haunt - Shed Roof 1-Up"))

    def test_bbh_shed_roof_1up_accepts_wall_kick(self):
        self.collect(self.get_item_by_name("Unlock Big Boo's Haunt"))
        self.assertFalse(self.can_reach_location("Big Boo's Haunt - Shed Roof 1-Up"))
        self.collect(self.get_item_by_name("Wall Kick"))
        self.assertTrue(self.can_reach_location("Big Boo's Haunt - Shed Roof 1-Up"))

    def test_ssl_oasis_tree_1up_accepts_side_flip(self):
        self.collect_basement_access()
        self.assertFalse(self.can_reach_location("Shifting Sand Land - Oasis Tree 1-Up"))
        self.collect(self.get_item_by_name("Side Flip"))
        self.assertTrue(self.can_reach_location("Shifting Sand Land - Oasis Tree 1-Up"))

    def test_ssl_near_quicksand_pits_1up_has_no_extra_rule(self):
        self.collect_basement_access()
        self.assertTrue(self.can_reach_location("Shifting Sand Land - Near Quicksand Pits 1-Up"))

    def test_ssl_above_quicksand_pit_1up_accepts_wing_cap_with_triple_jump(self):
        self.collect_basement_access()
        self.assertFalse(self.can_reach_location("Shifting Sand Land - Above Quicksand Pit 1-Up"))
        self.collect(self.get_item_by_name("Wing Cap"))
        self.assertFalse(self.can_reach_location("Shifting Sand Land - Above Quicksand Pit 1-Up"))
        self.collect(self.get_item_by_name("Triple Jump"))
        self.assertTrue(self.can_reach_location("Shifting Sand Land - Above Quicksand Pit 1-Up"))

    def test_ssl_above_quicksand_pit_1up_accepts_wing_cap_with_cannon(self):
        self.collect_basement_access()
        self.collect(self.get_item_by_name("Shifting Sand Land - Cannon Unlock"))
        self.assertFalse(self.can_reach_location("Shifting Sand Land - Above Quicksand Pit 1-Up"))
        self.collect(self.get_item_by_name("Wing Cap"))
        self.assertTrue(self.can_reach_location("Shifting Sand Land - Above Quicksand Pit 1-Up"))

    def test_ssl_above_quicksand_pit_1up_accepts_long_jump(self):
        self.collect_basement_access()
        self.assertFalse(self.can_reach_location("Shifting Sand Land - Above Quicksand Pit 1-Up"))
        self.collect(self.get_item_by_name("Long Jump"))
        self.assertTrue(self.can_reach_location("Shifting Sand Land - Above Quicksand Pit 1-Up"))

    def test_ssl_pyramid_1ups_accept_movement(self):
        self.collect_basement_access()
        for location_name in (
                "Shifting Sand Land - Pyramid Mummified Thwomp 1-Up",
                "Shifting Sand Land - Pyramid Right Path 1-Up",
        ):
            with self.subTest(location=location_name):
                self.assertFalse(self.can_reach_location(location_name))
        self.collect(self.get_item_by_name("Side Flip"))
        for location_name in (
                "Shifting Sand Land - Pyramid Mummified Thwomp 1-Up",
                "Shifting Sand Land - Pyramid Right Path 1-Up",
        ):
            with self.subTest(location=location_name):
                self.assertTrue(self.can_reach_location(location_name))


class NoDespawnCourseOneUpAccessTestBase(CourseOneUpAccessTestBase):
    options = {
        **CourseOneUpAccessTestBase.options,
        "no_despawns": Options.NoDespawns.option_true,
    }

    def test_ccm_slide_1ups_have_no_extra_rule(self):
        self.assertTrue(self.can_reach_location("Cool, Cool Mountain - Slide Shortcut First 1-Up"))
        self.assertTrue(self.can_reach_location("Cool, Cool Mountain - Slide Shortcut Second 1-Up"))


class VanillaBowserStageOneUpAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "enable_locked_paintings": Options.EnableLockedPaintings.option_false,
        "one_up_checks": Options.OneUpChecks.option_true,
        "area_rando": Options.AreaRandomizer.option_Off,
    }

    def test_bitdw_key_flag_1ups_use_vanilla_key_logic(self):
        self.collect(self.get_item_by_name("Dark World Key"))
        self.assertTrue(self.can_reach_region("Bowser in the Dark World"))
        self.assertFalse(self.can_reach_location("Bowser in the Dark World - Center Overhang 1-Up"))
        self.assertTrue(self.can_reach_location("Bowser in the Dark World - Right Tilting Platform Base 1-Up"))
        self.assertFalse(self.can_reach_location("Bowser in the Dark World - Left Tilting Platform Base 1-Up"))
        self.assertFalse(self.can_reach_location("Bowser in the Dark World - Far Overhang 1-Up"))

        self.collect(self.get_item_by_name("Progressive Basement Key"))
        self.assertTrue(self.can_reach_location("Bowser in the Dark World - Center Overhang 1-Up"))
        self.assertTrue(self.can_reach_location("Bowser in the Dark World - Left Tilting Platform Base 1-Up"))
        self.assertFalse(self.can_reach_location("Bowser in the Dark World - Far Overhang 1-Up"))

        self.collect(self.get_item_by_name("Progressive Upstairs Key"))
        self.assertTrue(self.can_reach_location("Bowser in the Dark World - Far Overhang 1-Up"))

    def test_bitfs_key_flag_1ups_use_vanilla_key_logic(self):
        self.collect([self.get_item_by_name("Progressive Basement Key")] * 2)
        self.collect(self.get_item_by_name("Unlock Bowser in the Fire Sea"))
        self.assertTrue(self.can_reach_region("Bowser in the Fire Sea"))
        self.assertFalse(self.can_reach_location("Bowser in the Fire Sea - Second Stone Structure 1-Up"))
        self.assertFalse(self.can_reach_location("Bowser in the Fire Sea - Near Poles 1-Up"))

        self.collect(self.get_item_by_name("Progressive Upstairs Key"))
        self.assertTrue(self.can_reach_location("Bowser in the Fire Sea - Second Stone Structure 1-Up"))
        self.assertTrue(self.can_reach_location("Bowser in the Fire Sea - Near Poles 1-Up"))


class GlobalBowserStageOneUpAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        "bowser_stage_1ups": Options.BowserStage1Ups.option_global,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "enable_locked_paintings": Options.EnableLockedPaintings.option_false,
        "one_up_checks": Options.OneUpChecks.option_true,
        "area_rando": Options.AreaRandomizer.option_Off,
    }

    def test_global_bowser_stage_1up_item_unlocks_bitdw_key_flag_1ups(self):
        self.collect(self.get_item_by_name("Dark World Key"))
        self.assertFalse(self.can_reach_location("Bowser in the Dark World - Center Overhang 1-Up"))
        self.collect(self.get_item_by_name("Bowser Stage Extra 1-Ups"))
        self.assertTrue(self.can_reach_location("Bowser in the Dark World - Center Overhang 1-Up"))
        self.assertTrue(self.can_reach_location("Bowser in the Dark World - Left Tilting Platform Base 1-Up"))
        self.assertTrue(self.can_reach_location("Bowser in the Dark World - Far Overhang 1-Up"))

    def test_global_bowser_stage_1up_item_unlocks_bitfs_key_flag_1ups(self):
        self.collect([self.get_item_by_name("Progressive Basement Key")] * 2)
        self.collect(self.get_item_by_name("Unlock Bowser in the Fire Sea"))
        self.assertFalse(self.can_reach_location("Bowser in the Fire Sea - Second Stone Structure 1-Up"))
        self.collect(self.get_item_by_name("Bowser Stage Extra 1-Ups"))
        self.assertTrue(self.can_reach_location("Bowser in the Fire Sea - Second Stone Structure 1-Up"))
        self.assertTrue(self.can_reach_location("Bowser in the Fire Sea - Near Poles 1-Up"))


class ShuffledMoveBowserInTheFireSeaOneUpAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "bowser_stage_1ups": Options.BowserStage1Ups.option_global,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "enable_locked_paintings": Options.EnableLockedPaintings.option_false,
        "one_up_checks": Options.OneUpChecks.option_true,
        "area_rando": Options.AreaRandomizer.option_Off,
    }

    def test_near_poles_1up_accepts_ledge_grab_like_near_poles_block(self):
        self.collect([self.get_item_by_name("Progressive Basement Key")] * 2)
        self.collect([
            self.get_item_by_name("Unlock Bowser in the Fire Sea"),
            self.get_item_by_name("Bowser Stage Extra 1-Ups"),
            self.get_item_by_name("Climb"),
        ])
        self.assertFalse(self.can_reach_location("Bowser in the Fire Sea - Near Poles Block 1-Up"))
        self.assertFalse(self.can_reach_location("Bowser in the Fire Sea - Near Poles 1-Up"))

        self.collect(self.get_item_by_name("Ledge Grab"))
        self.assertTrue(self.can_reach_location("Bowser in the Fire Sea - Near Poles Block 1-Up"))
        self.assertTrue(self.can_reach_location("Bowser in the Fire Sea - Near Poles 1-Up"))


class IndividualBowserStageOneUpAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        "bowser_stage_1ups": Options.BowserStage1Ups.option_individual,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "enable_locked_paintings": Options.EnableLockedPaintings.option_false,
        "one_up_checks": Options.OneUpChecks.option_true,
        "area_rando": Options.AreaRandomizer.option_Off,
    }

    def test_individual_bowser_stage_1up_items_are_stage_specific(self):
        self.collect(self.get_item_by_name("Dark World Key"))
        self.collect(self.get_item_by_name("Bowser in the Fire Sea - Extra 1-Ups"))
        self.assertFalse(self.can_reach_location("Bowser in the Dark World - Center Overhang 1-Up"))
        self.collect(self.get_item_by_name("Bowser in the Dark World - Extra 1-Ups"))
        self.assertTrue(self.can_reach_location("Bowser in the Dark World - Center Overhang 1-Up"))

        self.collect([self.get_item_by_name("Progressive Basement Key")] * 2)
        self.collect(self.get_item_by_name("Unlock Bowser in the Fire Sea"))
        self.assertTrue(self.can_reach_location("Bowser in the Fire Sea - Second Stone Structure 1-Up"))


class AlwaysSpawnBowserStageOneUpAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        "bowser_stage_1ups": Options.BowserStage1Ups.option_always_spawn,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "enable_locked_paintings": Options.EnableLockedPaintings.option_false,
        "one_up_checks": Options.OneUpChecks.option_true,
        "area_rando": Options.AreaRandomizer.option_Off,
    }

    def test_bowser_stage_1ups_are_always_spawned_in_logic(self):
        self.collect(self.get_item_by_name("Dark World Key"))
        self.assertTrue(self.can_reach_location("Bowser in the Dark World - Center Overhang 1-Up"))
        self.assertTrue(self.can_reach_location("Bowser in the Dark World - Left Tilting Platform Base 1-Up"))
        self.assertTrue(self.can_reach_location("Bowser in the Dark World - Far Overhang 1-Up"))

        self.collect([self.get_item_by_name("Progressive Basement Key")] * 2)
        self.collect(self.get_item_by_name("Unlock Bowser in the Fire Sea"))
        self.assertTrue(self.can_reach_location("Bowser in the Fire Sea - Second Stone Structure 1-Up"))
        self.assertTrue(self.can_reach_location("Bowser in the Fire Sea - Near Poles 1-Up"))


class LevelFeatureAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        "enable_locked_paintings": Options.EnableLockedPaintings.option_false,
        "area_rando": Options.AreaRandomizer.option_Off,
    }

    def test_BoB_feature_locations(self):
        self.assertFalse(self.can_reach_location("Bob-omb Battlefield - Big Bob-Omb on the Summit"))
        self.collect(self.get_item_by_name("Bob-omb Battlefield - King Bob-omb"))
        self.assertTrue(self.can_reach_location("Bob-omb Battlefield - Big Bob-Omb on the Summit"))

        self.assertFalse(self.can_reach_location("Bob-omb Battlefield - Footrace with Koopa The Quick"))
        self.collect(self.get_item_by_name("Bob-omb Battlefield - Koopa the Quick"))
        self.assertTrue(self.can_reach_location("Bob-omb Battlefield - Footrace with Koopa The Quick"))

    def test_CCM_feature_locations(self):
        self.assertFalse(self.can_reach_location("Cool, Cool Mountain - Big Penguin Race"))
        self.collect(self.get_item_by_name("Cool, Cool Mountain - Big Penguin"))
        self.assertTrue(self.can_reach_location("Cool, Cool Mountain - Big Penguin Race"))

        self.assertFalse(self.can_reach_location("Cool, Cool Mountain - Snowman's Lost His Head"))
        self.collect(self.get_item_by_name("Cool, Cool Mountain - Snowman's Head"))
        self.assertTrue(self.can_reach_location("Cool, Cool Mountain - Snowman's Lost His Head"))


class PerLevelMoveAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        "enable_locked_paintings": Options.EnableLockedPaintings.option_false,
        "area_rando": Options.AreaRandomizer.option_Off,
        "checkerboard_platforms": Options.CheckerboardPlatforms.option_global,
        "triple_jump": Options.TripleJump.option_per_level,
        "backflip": Options.Backflip.option_global,
        "side_flip": Options.SideFlip.option_per_level,
        "wall_kick": Options.WallKick.option_per_level,
        "ledge_grab": Options.LedgeGrab.option_global,
        "dive": Options.Dive.option_per_level,
        "climb": Options.Climb.option_per_level,
    }

    def test_course_rule_requires_course_move_item(self):
        self.assertFalse(self.can_reach_region("Whomp's Fortress - Top"))
        self.collect(self.world.create_item("Wall Kick"))
        self.collect(self.world.create_item("Whomp's Fortress - Side Flip"))
        self.assertFalse(self.can_reach_region("Whomp's Fortress - Top"))

        self.collect(self.world.create_item("Whomp's Fortress - Wall Kick"))
        self.assertTrue(self.can_reach_region("Whomp's Fortress - Top"))

    def test_castle_entrance_rule_requires_castle_move_item(self):
        self.assertFalse(self.can_reach_region("The Secret Aquarium"))
        self.collect(self.world.create_item("Jolly Roger Bay - Side Flip"))
        self.assertFalse(self.can_reach_region("The Secret Aquarium"))

        self.collect(self.world.create_item("Castle - Side Flip"))
        self.assertTrue(self.can_reach_region("The Secret Aquarium"))

    def test_cap_switch_stage_rule_uses_castle_move_item(self):
        self.collect([self.get_item_by_name("Progressive Key")] * 2)
        self.collect(self.get_item_by_name("Checkerboard Platforms"))
        self.collect(self.get_item_by_name("Unlock Vanish Cap Under the Moat"))
        self.assertFalse(self.can_reach_location("Vanish Cap Under the Moat - Switch"))

        self.collect(self.world.create_item("Whomp's Fortress - Wall Kick"))
        self.assertFalse(self.can_reach_location("Vanish Cap Under the Moat - Switch"))

        self.collect(self.world.create_item("Castle - Wall Kick"))
        self.assertTrue(self.can_reach_location("Vanish Cap Under the Moat - Switch"))

    def test_secret_stage_names_use_castle_move_items(self):
        for level_name in (
                "Tower of the Wing Cap",
                "Cavern of the Metal Cap",
                "Vanish Cap Under the Moat",
                "Bowser in the Dark World",
                "Bowser in the Fire Sea",
                "Bowser in the Sky",
        ):
            with self.subTest("Secret stage move alias", level=level_name):
                self.assertEqual(
                    get_per_level_action_item_name(level_name, "Triple Jump"),
                    "Castle - Triple Jump")

    def test_wmotR_rule_uses_castle_move_item(self):
        self.collect([self.get_item_by_name("Progressive Key")] * 5)
        self.collect(self.world.create_item("Wing Cap"))
        self.assertFalse(self.can_reach_location("Wing Mario Over the Rainbow - Bob-omb Buddy"))

        self.collect(self.world.create_item("Bob-omb Battlefield - Triple Jump"))
        self.assertFalse(self.can_reach_location("Wing Mario Over the Rainbow - Bob-omb Buddy"))

        self.collect(self.world.create_item("Castle - Triple Jump"))
        self.assertTrue(self.can_reach_location("Wing Mario Over the Rainbow - Bob-omb Buddy"))


class ArbitraryFeatureAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_ARBITRARY_FEATURE_OPTIONS,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "buddy_checks": Options.BuddyChecks.option_true,
        "enable_locked_paintings": Options.EnableLockedPaintings.option_false,
        "one_up_checks": Options.OneUpChecks.option_true,
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "area_rando": Options.AreaRandomizer.option_Off,
    }

    def collect_basement_access(self):
        self.collect(self.get_item_by_name("Progressive Basement Key"))

    def collect_second_floor_access(self):
        self.collect(self.get_item_by_name("Progressive Upstairs Key"))

    def collect_third_floor_access(self):
        self.collect([self.get_item_by_name("Progressive Upstairs Key")] * 2)

    def test_hmc_swimming_beast_access(self):
        self.collect_basement_access()
        self.assertFalse(self.can_reach_location("Hazy Maze Cave - Swimming Beast in the Cavern"))
        self.assertFalse(self.can_reach_region("Cavern of the Metal Cap"))

        self.collect(self.get_item_by_name("Hazy Maze Cave - Swimming Beast"))
        self.assertTrue(self.can_reach_location("Hazy Maze Cave - Swimming Beast in the Cavern"))
        self.assertTrue(self.can_reach_region("Cavern of the Metal Cap"))

    def test_checkerboard_platforms_gate_hmc_red_coin_area(self):
        self.collect_basement_access()
        self.collect([self.get_item_by_name("Climb"), self.get_item_by_name("Wall Kick")])
        self.assertFalse(self.can_reach_region("Hazy Maze Cave - Red Coin Area"))

        self.collect(self.world.create_item("Checkerboard Platforms"))
        self.assertTrue(self.can_reach_region("Hazy Maze Cave - Red Coin Area"))

    def test_rainbow_ride_beneath_pole_to_maze_route(self):
        self.collect_third_floor_access()
        self.collect(self.get_item_by_name("Side Flip"))
        self.assertTrue(self.can_reach_region("Rainbow Ride"))
        self.assertFalse(self.can_reach_region("Rainbow Ride - Beneath the Pole"))
        self.assertFalse(self.can_reach_region("Rainbow Ride - Maze"))
        self.assertFalse(self.can_reach_region("Rainbow Ride - Carpets"))
        self.assertFalse(self.can_reach_location("Rainbow Ride - Swingin' in the Breeze"))

        self.collect(self.get_item_by_name("Long Jump"))
        self.assertTrue(self.can_reach_region("Rainbow Ride - Beneath the Pole"))
        self.assertTrue(self.can_reach_location("Rainbow Ride - Swingin' in the Breeze"))
        self.assertFalse(self.can_reach_region("Rainbow Ride - Maze"))

        self.collect(self.get_item_by_name("Climb"))
        self.assertTrue(self.can_reach_region("Rainbow Ride - Maze"))
        self.assertFalse(self.can_reach_region("Rainbow Ride - Carpets"))

    def test_rainbow_ride_carpets_create_shortcut_to_maze(self):
        self.collect_third_floor_access()
        self.collect(self.get_item_by_name("Side Flip"))
        self.assertFalse(self.can_reach_region("Rainbow Ride - Maze"))

        self.collect(self.get_item_by_name("Rainbow Ride - Carpets"))
        self.assertTrue(self.can_reach_region("Rainbow Ride - Maze"))
        self.assertTrue(self.can_reach_region("Rainbow Ride - Carpets"))

    def test_rainbow_ride_1up_placement_and_logic(self):
        self.collect_third_floor_access()
        self.collect([
            self.get_item_by_name("Side Flip"),
            self.get_item_by_name("Long Jump"),
        ])
        self.assertTrue(self.can_reach_region("Rainbow Ride - Beneath the Pole"))
        self.assertFalse(self.can_reach_location("Rainbow Ride - Tricky Triangles 1-Up"))
        self.assertFalse(self.can_reach_location("Rainbow Ride - Rotating Bridge Platform 1-Up"))

        self.collect(self.get_item_by_name("Purple Switches"))
        self.assertTrue(self.can_reach_location("Rainbow Ride - Tricky Triangles!"))
        self.assertTrue(self.can_reach_location("Rainbow Ride - Tricky Triangles 1-Up"))

        self.collect(self.get_item_by_name("Rainbow Ride - Carpets"))
        self.assertTrue(self.can_reach_region("Rainbow Ride - Cruiser"))
        self.assertTrue(self.can_reach_location("Rainbow Ride - Rotating Bridge Platform 1-Up"))

    def test_rainbow_ride_red_coin_maze_donut_uses_top_block_logic(self):
        self.collect_third_floor_access()
        self.collect([
            self.get_item_by_name("Side Flip"),
            self.get_item_by_name("Long Jump"),
        ])
        self.assertFalse(self.can_reach_location("Rainbow Ride - Top of Red Coin Maze Block 1-Up"))
        self.assertFalse(self.can_reach_location("Rainbow Ride - Donut Top of Red Coin Maze 1-Up"))

        self.collect(self.get_item_by_name("Climb"))
        self.assertFalse(self.can_reach_location("Rainbow Ride - Top of Red Coin Maze Block 1-Up"))
        self.assertFalse(self.can_reach_location("Rainbow Ride - Donut Top of Red Coin Maze 1-Up"))

        self.collect(self.get_item_by_name("Rainbow Ride - Carpets"))
        self.assertTrue(self.can_reach_location("Rainbow Ride - Top of Red Coin Maze Block 1-Up"))
        self.assertTrue(self.can_reach_location("Rainbow Ride - Donut Top of Red Coin Maze 1-Up"))

    def test_rainbow_ride_cruiser_still_requires_carpets(self):
        self.collect_third_floor_access()
        self.collect([
            self.get_item_by_name("Side Flip"),
            self.get_item_by_name("Long Jump"),
            self.get_item_by_name("Climb"),
        ])
        self.assertTrue(self.can_reach_region("Rainbow Ride - Maze"))
        self.assertFalse(self.can_reach_region("Rainbow Ride - Carpets"))
        self.assertFalse(self.can_reach_region("Rainbow Ride - Cruiser"))

        self.collect(self.get_item_by_name("Rainbow Ride - Carpets"))
        self.assertTrue(self.can_reach_region("Rainbow Ride - Carpets"))
        self.assertTrue(self.can_reach_region("Rainbow Ride - Cruiser"))

    def test_rainbow_ride_ship_pole_requires_cruiser_and_climb(self):
        self.collect_third_floor_access()
        self.collect(self.get_item_by_name("Side Flip"))
        self.collect(self.get_item_by_name("Rainbow Ride - Carpets"))
        self.assertTrue(self.can_reach_region("Rainbow Ride - Cruiser"))
        self.assertTrue(self.can_reach_location("Rainbow Ride - Ship Tip 1-Up"))
        self.assertFalse(self.can_reach_location("Rainbow Ride - Ship Pole 1-Up"))

        self.collect(self.get_item_by_name("Climb"))
        self.assertTrue(self.can_reach_location("Rainbow Ride - Ship Pole 1-Up"))

    def test_rainbow_ride_house_path_donut_uses_house_logic(self):
        self.collect_third_floor_access()
        self.collect(self.get_item_by_name("Side Flip"))
        self.assertFalse(self.can_reach_location("Rainbow Ride - House Path Donut Lifts 1-Up"))

        self.collect(self.get_item_by_name("Rainbow Ride - Carpets"))
        self.assertTrue(self.can_reach_location("Rainbow Ride - The Big House in the Sky"))
        self.assertTrue(self.can_reach_location("Rainbow Ride - House Path Donut Lifts 1-Up"))

    def test_whomps_fortress_top_access(self):
        self.assertFalse(self.can_reach_region("Whomp's Fortress - Top"))
        self.collect(self.get_item_by_name("Wall Kick"))
        self.assertFalse(self.can_reach_region("Whomp's Fortress - Top"))
        self.collect(self.get_item_by_name("Side Flip"))
        self.assertTrue(self.can_reach_region("Whomp's Fortress - Top"))

    def test_whomps_fortress_top_access_with_climb_and_dive_or_ledge_grab(self):
        self.collect(self.get_item_by_name("Climb"))
        self.assertFalse(self.can_reach_region("Whomp's Fortress - Top"))
        self.collect(self.get_item_by_name("Dive"))
        self.assertTrue(self.can_reach_region("Whomp's Fortress - Top"))

    def test_whomps_fortress_top_access_with_climb_and_ledge_grab(self):
        self.collect([
            self.get_item_by_name("Climb"),
            self.get_item_by_name("Ledge Grab"),
        ])
        self.assertTrue(self.can_reach_region("Whomp's Fortress - Top"))

    def test_whomps_fortress_red_coins_on_floating_isle_does_not_require_fortress(self):
        self.assertFalse(self.can_reach_location("Whomp's Fortress - Red Coins on the Floating Isle"))
        self.collect(self.world.create_item("Checkerboard Platforms"))
        self.assertTrue(self.can_reach_location("Whomp's Fortress - Red Coins on the Floating Isle"))

    def test_whomps_fortress_caged_island_hoot_route_requires_climb(self):
        self.collect([self.get_item_by_name("Whomp's Fortress - Fortress"), self.get_item_by_name("Climb")])
        self.assertFalse(self.can_reach_location("Whomp's Fortress - Fall onto the Caged Island"))
        self.collect([
            self.world.create_item("Checkerboard Platforms"),
            self.get_item_by_name("Whomp's Fortress - Hoot"),
        ])
        self.assertTrue(self.can_reach_location("Whomp's Fortress - Fall onto the Caged Island"))

    def test_whomps_fortress_caged_island_triple_jump_route_uses_whomp_king(self):
        self.collect([
            self.get_item_by_name("Whomp's Fortress - Fortress"),
            self.world.create_item("Checkerboard Platforms"),
            self.get_item_by_name("Triple Jump"),
            self.world.create_item("ut_glitch"),
        ])
        self.assertFalse(self.can_reach_location("Whomp's Fortress - Fall onto the Caged Island"))

        self.collect(self.get_item_by_name("Whomp's Fortress - Whomp King"))
        self.assertTrue(self.can_reach_location("Whomp's Fortress - Fall onto the Caged Island"))

    def test_lll_red_hot_log_rolling_requires_log_shell_or_wing_cap(self):
        self.collect_basement_access()
        self.assertFalse(self.can_reach_location("Lethal Lava Land - Red-Hot Log Rolling"))

        self.collect(self.world.create_item("Rolling Logs"))
        self.assertTrue(self.can_reach_location("Lethal Lava Land - Red-Hot Log Rolling"))

    def test_lll_elevator_tour_accepts_checkerboard_platforms(self):
        self.collect_basement_access()
        self.collect(self.get_item_by_name("Climb"))
        self.assertFalse(self.can_reach_location("Lethal Lava Land - Elevator Tour in the Volcano"))

        self.collect(self.world.create_item("Checkerboard Platforms"))
        self.assertTrue(self.can_reach_location("Lethal Lava Land - Elevator Tour in the Volcano"))

    def test_vanish_cap_under_moat_requires_checkerboard_platforms(self):
        self.collect_basement_access()
        self.collect([
            self.get_item_by_name("Ground Pound"),
            self.get_item_by_name("Wall Kick"),
            self.get_item_by_name("Vanish Cap"),
            self.get_item_by_name("Unlock Vanish Cap Under the Moat"),
        ])
        self.assertFalse(self.can_reach_location("Vanish Cap Under the Moat - Switch"))
        self.assertFalse(self.can_reach_location("Vanish Cap Under the Moat - Red Coins"))

        self.collect(self.get_item_by_name("Checkerboard Platforms"))
        self.assertTrue(self.can_reach_location("Vanish Cap Under the Moat - Switch"))
        self.assertTrue(self.can_reach_location("Vanish Cap Under the Moat - Red Coins"))

    def test_tiny_huge_island_tiny_piranha_area_requires_movement(self):
        self.collect_second_floor_access()
        self.assertFalse(self.can_reach_region("Tiny-Huge Island - Tiny Piranha Area"))

        self.collect(self.get_item_by_name("Long Jump"))
        self.assertTrue(self.can_reach_region("Tiny-Huge Island - Tiny Piranha Area"))

    def test_tiny_huge_island_warp_from_tiny_requires_piranha_area_and_warp_pipes(self):
        self.multiworld.get_entrance("Second Floor -> Tiny-Huge Island (Huge)", self.player).access_rule = \
            lambda state: False

        self.collect_second_floor_access()
        self.assertTrue(self.can_reach_region("Tiny-Huge Island (Tiny)"))
        self.assertFalse(self.can_reach_region("Tiny-Huge Island (Huge)"))
        self.assertFalse(self.can_reach_region("Tiny-Huge Island - Huge Piranha Area"))

        self.collect(self.get_item_by_name("Tiny-Huge Island - Warp Pipes"))
        self.assertFalse(self.can_reach_region("Tiny-Huge Island (Huge)"))
        self.assertFalse(self.can_reach_region("Tiny-Huge Island - Huge Piranha Area"))

        self.collect(self.get_item_by_name("Long Jump"))
        self.assertTrue(self.can_reach_region("Tiny-Huge Island - Huge Piranha Area"))
        self.assertTrue(self.can_reach_region("Tiny-Huge Island (Huge)"))

    def test_tiny_huge_island_main_regions_connect_with_warp_pipes(self):
        self.multiworld.get_entrance("Second Floor -> Tiny-Huge Island (Huge)", self.player).access_rule = \
            lambda state: False

        self.collect_second_floor_access()
        self.collect([
            self.get_item_by_name("Long Jump"),
            self.get_item_by_name("Purple Switches"),
        ])
        self.assertTrue(self.can_reach_region("Tiny-Huge Island - Tiny Main"))
        self.assertFalse(self.can_reach_region("Tiny-Huge Island (Huge)"))

        self.collect(self.get_item_by_name("Tiny-Huge Island - Warp Pipes"))
        self.assertTrue(self.can_reach_region("Tiny-Huge Island (Huge)"))

    def test_tiny_huge_island_huge_main_connects_to_tiny_main_with_warp_pipes(self):
        self.multiworld.get_entrance("Second Floor -> Tiny-Huge Island (Tiny)", self.player).access_rule = \
            lambda state: False

        self.collect_second_floor_access()
        self.assertTrue(self.can_reach_region("Tiny-Huge Island (Huge)"))
        self.assertFalse(self.can_reach_region("Tiny-Huge Island - Tiny Main"))

        self.collect(self.get_item_by_name("Tiny-Huge Island - Warp Pipes"))
        self.assertTrue(self.can_reach_region("Tiny-Huge Island - Tiny Main"))

    def test_tiny_huge_island_rematch_accepts_long_jump_or_dive(self):
        self.collect_second_floor_access()
        self.collect(self.get_item_by_name("Tiny-Huge Island - Koopa the Quick"))
        self.assertFalse(self.can_reach_location("Tiny-Huge Island - Rematch with Koopa the Quick"))

        self.collect(self.get_item_by_name("Long Jump"))
        self.assertTrue(self.can_reach_location("Tiny-Huge Island - Rematch with Koopa the Quick"))

    def test_tiny_huge_island_rematch_accepts_dive(self):
        self.collect_second_floor_access()
        self.collect(self.get_item_by_name("Tiny-Huge Island - Koopa the Quick"))
        self.assertFalse(self.can_reach_location("Tiny-Huge Island - Rematch with Koopa the Quick"))

        self.collect(self.get_item_by_name("Dive"))
        self.assertTrue(self.can_reach_location("Tiny-Huge Island - Rematch with Koopa the Quick"))

    def test_tiny_huge_island_rematch_requires_moveless_for_top_return_movement(self):
        self.collect_second_floor_access()
        self.collect([
            self.get_item_by_name("Tiny-Huge Island - Koopa the Quick"),
            self.get_item_by_name("Triple Jump"),
        ])
        self.assertFalse(self.can_reach_location("Tiny-Huge Island - Rematch with Koopa the Quick"))

        self.collect(self.world.create_item("ut_glitch"))
        self.assertTrue(self.can_reach_location("Tiny-Huge Island - Rematch with Koopa the Quick"))

    def test_tiny_huge_island_rematch_requires_moveless_for_warp_pipes(self):
        self.collect_second_floor_access()
        self.collect(self.get_item_by_name("Tiny-Huge Island - Koopa the Quick"))
        self.assertFalse(self.can_reach_location("Tiny-Huge Island - Rematch with Koopa the Quick"))

        self.collect(self.get_item_by_name("Tiny-Huge Island - Warp Pipes"))
        self.assertFalse(self.can_reach_location("Tiny-Huge Island - Rematch with Koopa the Quick"))

        self.collect(self.world.create_item("ut_glitch"))
        self.assertTrue(self.can_reach_location("Tiny-Huge Island - Rematch with Koopa the Quick"))

    def test_purple_switch_gated_locations(self):
        self.collect_basement_access()
        self.collect([
            self.get_item_by_name("Long Jump"),
            self.get_item_by_name("Metal Cap"),
            self.get_item_by_name("Dire, Dire Docks - Bowser's Sub"),
        ])
        self.assertFalse(self.can_reach_location("Hazy Maze Cave - Metal-Head Mario Can Move!"))
        self.assertFalse(self.can_reach_location("Dire, Dire Docks - Board Bowser's Sub"))

        self.collect(self.world.create_item("Purple Switches"))
        self.assertTrue(self.can_reach_location("Hazy Maze Cave - Metal-Head Mario Can Move!"))
        self.collect(self.get_item_by_name("Progressive Basement Key"))
        self.assertTrue(self.can_reach_location("Dire, Dire Docks - Board Bowser's Sub"))

    def test_dire_dire_docks_board_bowser_sub_triple_jump_requires_moveless(self):
        self.collect([
            self.get_item_by_name("Progressive Basement Key"),
            self.get_item_by_name("Progressive Basement Key"),
            self.get_item_by_name("Dire, Dire Docks - Bowser's Sub"),
            self.get_item_by_name("Triple Jump"),
        ])
        self.assertFalse(self.can_reach_location("Dire, Dire Docks - Board Bowser's Sub"))

        self.collect(self.world.create_item("ut_glitch"))
        self.assertTrue(self.can_reach_location("Dire, Dire Docks - Board Bowser's Sub"))

    def test_hmc_metal_head_capless_route_requires_purple_switches(self):
        self.collect_basement_access()
        self.collect([
            self.get_item_by_name("Long Jump"),
            self.get_item_by_name("Triple Jump"),
            self.world.create_item("ut_glitch"),
        ])
        self.assertFalse(self.can_reach_location("Hazy Maze Cave - Metal-Head Mario Can Move!"))

        self.collect(self.world.create_item("Purple Switches"))
        self.assertTrue(self.can_reach_location("Hazy Maze Cave - Metal-Head Mario Can Move!"))

    def test_wet_dry_world_express_elevator_requires_purple_switches_and_access_method(self):
        self.collect_second_floor_access()
        self.assertFalse(self.can_reach_location("Wet-Dry World - Express Elevator--Hurry Up!"))

        self.collect(self.get_item_by_name("Backflip"))
        self.assertFalse(self.can_reach_location("Wet-Dry World - Express Elevator--Hurry Up!"))

        self.collect(self.get_item_by_name("Purple Switches"))
        self.assertTrue(self.can_reach_location("Wet-Dry World - Express Elevator--Hurry Up!"))

    def test_wet_dry_world_quick_race_tj_lg_route_requires_purple_switches(self):
        self.collect_second_floor_access()
        self.collect([
            self.get_item_by_name("Vanish Cap"),
            self.get_item_by_name("Triple Jump"),
            self.get_item_by_name("Ledge Grab"),
        ])
        self.assertTrue(self.can_reach_region("Wet-Dry World - Downtown"))
        self.assertFalse(self.can_reach_location("Wet-Dry World - Quick Race Through Downtown!"))

        self.collect(self.get_item_by_name("Purple Switches"))
        self.assertFalse(self.can_reach_location("Wet-Dry World - Quick Race Through Downtown!"))

        self.collect(self.get_item_by_name("Wet-Dry World - Water Level Diamond"))
        self.assertTrue(self.can_reach_location("Wet-Dry World - Quick Race Through Downtown!"))

    def test_tall_tall_mountain_bridge_accepts_purple_switches(self):
        self.collect_second_floor_access()
        self.collect([
            self.get_item_by_name("Long Jump"),
            self.get_item_by_name("Kick"),
        ])
        self.assertTrue(self.can_reach_region("Tall, Tall Mountain - Top"))
        self.assertFalse(self.can_reach_location("Tall, Tall Mountain - Breathtaking View from Bridge"))

        self.collect(self.get_item_by_name("Purple Switches"))
        self.assertTrue(self.can_reach_location("Tall, Tall Mountain - Breathtaking View from Bridge"))

    def test_tall_tall_mountain_vine_platform_uses_top_region(self):
        self.collect_second_floor_access()
        self.assertFalse(self.can_reach_location("Tall, Tall Mountain - Scale the Mountain"))
        self.assertFalse(self.can_reach_location("Tall, Tall Mountain - Vine Platform Butterfly 1-Up"))

        self.collect([
            self.get_item_by_name("Long Jump"),
            self.get_item_by_name("Kick"),
        ])
        self.assertTrue(self.can_reach_region("Tall, Tall Mountain - Top"))
        self.assertTrue(self.can_reach_location("Tall, Tall Mountain - Scale the Mountain"))
        self.assertTrue(self.can_reach_location("Tall, Tall Mountain - Vine Platform Butterfly 1-Up"))

    def test_tiny_huge_island_five_secrets_from_tiny_requires_purple_switches(self):
        self.multiworld.get_entrance("Second Floor -> Tiny-Huge Island (Huge)", self.player).access_rule = \
            lambda state: False

        self.collect_second_floor_access()
        self.assertTrue(self.can_reach_region("Tiny-Huge Island (Tiny)"))
        self.assertFalse(self.can_reach_region("Tiny-Huge Island - Tiny Piranha Area"))
        self.assertFalse(self.can_reach_location("Tiny-Huge Island - Five Itty Bitty Secrets"))

        self.collect(self.get_item_by_name("Purple Switches"))
        self.assertFalse(self.can_reach_location("Tiny-Huge Island - Five Itty Bitty Secrets"))

        self.collect(self.get_item_by_name("Long Jump"))
        self.assertTrue(self.can_reach_location("Tiny-Huge Island - Five Itty Bitty Secrets"))

    def test_tiny_huge_island_five_secrets_from_huge_requires_warp_pipes(self):
        self.multiworld.get_entrance("Second Floor -> Tiny-Huge Island (Tiny)", self.player).access_rule = \
            lambda state: False

        self.collect_second_floor_access()
        self.assertTrue(self.can_reach_region("Tiny-Huge Island (Huge)"))
        self.assertFalse(self.can_reach_region("Tiny-Huge Island (Tiny)"))
        self.assertFalse(self.can_reach_location("Tiny-Huge Island - Five Itty Bitty Secrets"))

        self.collect(self.get_item_by_name("Tiny-Huge Island - Warp Pipes"))
        self.assertTrue(self.can_reach_region("Tiny-Huge Island - Tiny Main"))
        self.assertFalse(self.can_reach_location("Tiny-Huge Island - Five Itty Bitty Secrets"))

        self.collect(self.get_item_by_name("Purple Switches"))
        self.assertTrue(self.can_reach_location("Tiny-Huge Island - Five Itty Bitty Secrets"))

    def test_tiny_huge_island_make_wiggler_requires_warp_pipes(self):
        self.collect_second_floor_access()
        self.collect([
            self.get_item_by_name("Ledge Grab"),
            self.get_item_by_name("Purple Switches"),
            self.get_item_by_name("Ground Pound"),
        ])
        self.assertTrue(self.can_reach_region("Tiny-Huge Island - Tiny Main"))
        self.assertFalse(self.can_reach_location("Tiny-Huge Island - Make Wiggler Squirm"))

        self.collect(self.get_item_by_name("Tiny-Huge Island - Warp Pipes"))
        self.assertTrue(self.can_reach_location("Tiny-Huge Island - Make Wiggler Squirm"))

    def test_rainbow_ride_tricky_triangles_requires_purple_switches(self):
        self.collect_third_floor_access()
        self.collect([
            self.get_item_by_name("Side Flip"),
            self.get_item_by_name("Long Jump"),
        ])
        self.assertTrue(self.can_reach_region("Rainbow Ride - Beneath the Pole"))
        self.assertFalse(self.can_reach_location("Rainbow Ride - Tricky Triangles!"))

        self.collect(self.get_item_by_name("Purple Switches"))
        self.assertTrue(self.can_reach_location("Rainbow Ride - Tricky Triangles!"))

    def test_bitdw_red_coins_and_key_accept_purple_switches(self):
        self.collect(self.get_item_by_name("Dark World Key"))
        self.assertTrue(self.can_reach_region("Bowser in the Dark World"))
        self.assertFalse(self.can_reach_location("Bowser in the Dark World - Red Coins"))
        self.assertFalse(self.can_reach_location("Bowser in the Dark World - Key"))

        self.collect(self.get_item_by_name("Purple Switches"))
        self.assertTrue(self.can_reach_location("Bowser in the Dark World - Red Coins"))
        self.assertTrue(self.can_reach_location("Bowser in the Dark World - Key"))

    def test_bitdw_key_accepts_moveless_triple_jump_but_red_coins_require_purple_switches(self):
        self.collect(self.get_item_by_name("Dark World Key"))
        self.assertFalse(self.can_reach_location("Bowser in the Dark World - Red Coins"))
        self.assertFalse(self.can_reach_location("Bowser in the Dark World - Key"))

        self.collect(self.get_item_by_name("Triple Jump"))
        self.assertFalse(self.can_reach_location("Bowser in the Dark World - Red Coins"))
        self.assertFalse(self.can_reach_location("Bowser in the Dark World - Key"))

        self.collect(self.world.create_item("ut_glitch"))
        self.assertFalse(self.can_reach_location("Bowser in the Dark World - Red Coins"))
        self.assertTrue(self.can_reach_location("Bowser in the Dark World - Key"))

        self.collect(self.get_item_by_name("Purple Switches"))
        self.assertTrue(self.can_reach_location("Bowser in the Dark World - Red Coins"))

    def test_bowser_in_the_sky_region_chain(self):
        self.collect([self.get_item_by_name("Progressive Upstairs Key")] * 3)
        self.assertTrue(self.can_reach_region("Bowser in the Sky"))
        self.assertTrue(self.can_reach_location("Bowser in the Sky - Ferris Wheel 1-Up"))
        self.assertFalse(self.can_reach_region("Bowser in the Sky - Chuckya"))
        self.assertFalse(self.can_reach_region("Bowser in the Sky - Arrow Ride"))
        self.assertFalse(self.can_reach_location("Bowser in the Sky - Spark Pole Coins 1-Up"))

        self.collect(self.get_item_by_name("Side Flip"))
        self.assertTrue(self.can_reach_region("Bowser in the Sky - Chuckya"))
        self.assertFalse(self.can_reach_region("Bowser in the Sky - Arrow Ride"))

        self.collect(self.get_item_by_name("Purple Switches"))
        self.assertTrue(self.can_reach_region("Bowser in the Sky - Arrow Ride"))
        self.assertTrue(self.can_reach_location("Bowser in the Sky - Spark Pole Coins 1-Up"))
        self.assertTrue(self.can_reach_location("Bowser in the Sky - Arrow Ride 1-Up"))
        self.assertFalse(self.can_reach_region("Bowser in the Sky - Top"))
        self.assertFalse(self.can_reach_location("Bowser in the Sky - Final Platform 1-Up"))

        self.collect(self.get_item_by_name("Climb"))
        self.assertTrue(self.can_reach_region("Bowser in the Sky - Top"))
        self.assertTrue(self.can_reach_location("Bowser in the Sky - Final Platform 1-Up"))

    def test_cool_cool_mountain_lil_penguin_lost_requires_baby_penguins(self):
        self.assertFalse(self.can_reach_location("Cool, Cool Mountain - Li'l Penguin Lost"))
        self.collect(self.get_item_by_name("Cool, Cool Mountain - Baby Penguins"))
        self.assertTrue(self.can_reach_location("Cool, Cool Mountain - Li'l Penguin Lost"))

    def test_snowmans_land_big_head_requires_penguin_with_movement(self):
        self.collect_second_floor_access()
        self.collect(self.get_item_by_name("Backflip"))
        self.assertFalse(self.can_reach_location("Snowman's Land - Snowman's Big Head"))

        self.collect(self.get_item_by_name("Snowman's Land - Penguin"))
        self.assertTrue(self.can_reach_location("Snowman's Land - Snowman's Big Head"))

    def test_snowmans_land_big_head_accepts_cannon(self):
        self.collect_second_floor_access()
        self.assertFalse(self.can_reach_location("Snowman's Land - Snowman's Big Head"))

        self.collect(self.get_item_by_name("Snowman's Land - Cannon Unlock"))
        self.assertTrue(self.can_reach_location("Snowman's Land - Snowman's Big Head"))

    def test_snowmans_land_snowman_tree_requires_top_and_accepts_side_flip(self):
        self.collect_second_floor_access()
        self.collect(self.get_item_by_name("Snowman's Land - Cannon Unlock"))
        self.assertTrue(self.can_reach_region("Snowman's Land - Top of Snowman's Head"))
        self.assertTrue(self.can_reach_location("Snowman's Land - Snowman's Big Head"))
        self.assertFalse(self.can_reach_location("Snowman's Land - Snowman Tree 1-Up"))

        self.collect(self.get_item_by_name("Side Flip"))
        self.assertTrue(self.can_reach_location("Snowman's Land - Snowman Tree 1-Up"))

    def test_shifting_sand_land_upper_pyramid_accepts_pyramid_elevator(self):
        self.collect_basement_access()
        self.assertFalse(self.can_reach_region("Shifting Sand Land - Upper Pyramid"))

        self.collect(self.get_item_by_name("Shifting Sand Land - Pyramid Elevator"))
        self.assertTrue(self.can_reach_region("Shifting Sand Land - Upper Pyramid"))

    def test_shifting_sand_land_stand_tall_requires_pyramid_elevator(self):
        self.collect_basement_access()
        self.collect([
            self.get_item_by_name("Triple Jump"),
            self.get_item_by_name("Wing Cap"),
            self.get_item_by_name("Ground Pound"),
        ])
        self.assertFalse(self.can_reach_location("Shifting Sand Land - Stand Tall on the Four Pillars"))

        self.collect(self.get_item_by_name("Shifting Sand Land - Pyramid Elevator"))
        self.assertTrue(self.can_reach_location("Shifting Sand Land - Stand Tall on the Four Pillars"))


class IndividualArbitraryFeatureAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **ArbitraryFeatureAccessTestBase.options,
        "checkerboard_platforms": Options.CheckerboardPlatforms.option_individual,
        "rolling_logs": Options.RollingLogs.option_individual,
        "purple_switches": Options.PurpleSwitches.option_individual,
    }

    def collect_basement_access(self):
        self.collect(self.get_item_by_name("Progressive Basement Key"))

    def test_individual_checkerboard_platforms_ignore_global_item(self):
        self.assertFalse(self.can_reach_region("Whomp's Fortress - Top"))

        self.collect(self.world.create_item("Checkerboard Platforms"))
        self.assertFalse(self.can_reach_region("Whomp's Fortress - Top"))

        self.collect(self.get_item_by_name("Whomp's Fortress - Checkerboard Platform"))
        self.assertTrue(self.can_reach_region("Whomp's Fortress - Top"))

    def test_individual_rolling_logs_ignore_global_item(self):
        self.collect_basement_access()
        self.assertFalse(self.can_reach_location("Lethal Lava Land - Red-Hot Log Rolling"))

        self.collect(self.world.create_item("Rolling Logs"))
        self.assertFalse(self.can_reach_location("Lethal Lava Land - Red-Hot Log Rolling"))

        self.collect(self.get_item_by_name("Lethal Lava Land - Rolling Log"))
        self.assertTrue(self.can_reach_location("Lethal Lava Land - Red-Hot Log Rolling"))

    def test_individual_purple_switches_ignore_global_item(self):
        self.collect_basement_access()
        self.collect([
            self.get_item_by_name("Long Jump"),
            self.get_item_by_name("Metal Cap"),
        ])
        self.assertFalse(self.can_reach_location("Hazy Maze Cave - Metal-Head Mario Can Move!"))

        self.collect(self.world.create_item("Purple Switches"))
        self.assertFalse(self.can_reach_location("Hazy Maze Cave - Metal-Head Mario Can Move!"))

        self.collect(self.get_item_by_name("Hazy Maze Cave - Purple Switch"))
        self.assertTrue(self.can_reach_location("Hazy Maze Cave - Metal-Head Mario Can Move!"))

    def test_dire_dire_docks_uses_individual_purple_switch(self):
        self.collect([
            self.get_item_by_name("Progressive Basement Key"),
            self.get_item_by_name("Progressive Basement Key"),
            self.get_item_by_name("Dire, Dire Docks - Bowser's Sub"),
        ])
        self.assertFalse(self.can_reach_location("Dire, Dire Docks - Board Bowser's Sub"))

        self.collect(self.world.create_item("Purple Switches"))
        self.assertFalse(self.can_reach_location("Dire, Dire Docks - Board Bowser's Sub"))

        self.collect(self.get_item_by_name("Dire, Dire Docks - Purple Switch"))
        self.assertTrue(self.can_reach_location("Dire, Dire Docks - Board Bowser's Sub"))

    def test_tall_tall_mountain_uses_individual_purple_switch(self):
        self.collect([
            self.get_item_by_name("Progressive Upstairs Key"),
            self.get_item_by_name("Long Jump"),
            self.get_item_by_name("Kick"),
        ])
        self.assertFalse(self.can_reach_location("Tall, Tall Mountain - Breathtaking View from Bridge"))

        self.collect(self.world.create_item("Purple Switches"))
        self.assertFalse(self.can_reach_location("Tall, Tall Mountain - Breathtaking View from Bridge"))

        self.collect(self.get_item_by_name("Tall, Tall Mountain - Purple Switch"))
        self.assertTrue(self.can_reach_location("Tall, Tall Mountain - Breathtaking View from Bridge"))

    def test_tiny_huge_island_uses_individual_purple_switch(self):
        self.collect(self.get_item_by_name("Progressive Upstairs Key"))
        self.assertTrue(self.can_reach_region("Tiny-Huge Island (Tiny)"))
        self.assertFalse(self.can_reach_location("Tiny-Huge Island - Five Itty Bitty Secrets"))

        self.collect(self.world.create_item("Purple Switches"))
        self.assertFalse(self.can_reach_location("Tiny-Huge Island - Five Itty Bitty Secrets"))

        self.collect([
            self.get_item_by_name("Tiny-Huge Island - Purple Switch"),
            self.get_item_by_name("Long Jump"),
        ])
        self.assertTrue(self.can_reach_location("Tiny-Huge Island - Five Itty Bitty Secrets"))


class UnshuffledArbitraryFeatureAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **ArbitraryFeatureAccessTestBase.options,
        "hazy_maze_cave_swimming_beast": Options.HazyMazeCaveSwimmingBeast.option_false,
        "checkerboard_platforms": Options.CheckerboardPlatforms.option_not_shuffled,
        "rolling_logs": Options.RollingLogs.option_not_shuffled,
        "purple_switches": Options.PurpleSwitches.option_not_shuffled,
    }

    def collect_basement_access(self):
        self.collect(self.get_item_by_name("Progressive Basement Key"))

    def test_unshuffled_simple_feature_passes_logic(self):
        self.collect_basement_access()
        self.assertTrue(self.can_reach_location("Hazy Maze Cave - Swimming Beast in the Cavern"))
        self.assertTrue(self.can_reach_region("Cavern of the Metal Cap"))

    def test_unshuffled_family_features_pass_logic(self):
        self.collect_basement_access()
        self.collect([
            self.get_item_by_name("Climb"),
            self.get_item_by_name("Wall Kick"),
            self.get_item_by_name("Long Jump"),
            self.get_item_by_name("Metal Cap"),
        ])
        self.assertTrue(self.can_reach_region("Hazy Maze Cave - Red Coin Area"))
        self.assertTrue(self.can_reach_location("Hazy Maze Cave - Metal-Head Mario Can Move!"))
        self.assertTrue(self.can_reach_location("Lethal Lava Land - Red-Hot Log Rolling"))


class BowserInTheSkyCoinsanityAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_ARBITRARY_FEATURE_OPTIONS,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "enable_locked_paintings": Options.EnableLockedPaintings.option_false,
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "area_rando": Options.AreaRandomizer.option_Off,
        "coinsanity": 100,
        "secret_stage_coinsanity": Options.SecretStageCoinsanity.option_true,
    }

    def collect_bowser_in_the_sky_access(self):
        self.collect([self.get_item_by_name("Progressive Upstairs Key")] * 3)

    def test_bowser_in_the_sky_coin_sources(self):
        self.collect_bowser_in_the_sky_access()
        self.assertTrue(self.can_reach_location("Bowser in the Sky - 23 Coins"))
        self.assertFalse(self.can_reach_location("Bowser in the Sky - 24 Coins"))

        self.collect(self.get_item_by_name("Ground Pound"))
        self.assertTrue(self.can_reach_location("Bowser in the Sky - 33 Coins"))
        self.assertFalse(self.can_reach_location("Bowser in the Sky - 34 Coins"))

        self.collect(self.get_item_by_name("Side Flip"))
        self.assertTrue(self.can_reach_region("Bowser in the Sky - Chuckya"))
        self.assertTrue(self.can_reach_location("Bowser in the Sky - 42 Coins"))
        self.assertFalse(self.can_reach_location("Bowser in the Sky - 43 Coins"))

        self.collect(self.get_item_by_name("Purple Switches"))
        self.assertTrue(self.can_reach_region("Bowser in the Sky - Arrow Ride"))
        self.assertTrue(self.can_reach_location("Bowser in the Sky - 60 Coins"))
        self.assertFalse(self.can_reach_location("Bowser in the Sky - 61 Coins"))

        self.collect(self.get_item_by_name("Climb"))
        self.assertTrue(self.can_reach_region("Bowser in the Sky - Top"))
        self.assertTrue(self.can_reach_location("Bowser in the Sky - 76 Coins"))


class BowserInTheFireSeaCoinsanityAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "enable_locked_paintings": Options.EnableLockedPaintings.option_false,
        "area_rando": Options.AreaRandomizer.option_Off,
        "coinsanity": 100,
        "secret_stage_coinsanity": Options.SecretStageCoinsanity.option_true,
    }

    def collect_bowser_in_the_fire_sea_access(self):
        self.collect([self.get_item_by_name("Progressive Basement Key")] * 2)
        self.collect(self.get_item_by_name("Unlock Bowser in the Fire Sea"))

    def test_bowser_in_the_fire_sea_coin_sources(self):
        self.collect_bowser_in_the_fire_sea_access()
        self.assertTrue(self.can_reach_location("Bowser in the Fire Sea - 26 Coins"))
        self.assertFalse(self.can_reach_location("Bowser in the Fire Sea - 27 Coins"))

        self.collect(self.get_item_by_name("Climb"))
        self.assertTrue(self.can_reach_location("Bowser in the Fire Sea - 80 Coins"))


class WingMarioOverTheRainbowCoinsanityAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "enable_locked_paintings": Options.EnableLockedPaintings.option_false,
        "buddy_checks": Options.BuddyChecks.option_true,
        "area_rando": Options.AreaRandomizer.option_Off,
        "coinsanity": 100,
        "secret_stage_coinsanity": Options.SecretStageCoinsanity.option_true,
    }

    def collect_wing_mario_over_the_rainbow_access(self):
        self.collect([self.get_item_by_name("Progressive Upstairs Key")] * 3)
        self.collect(self.get_item_by_name("Side Flip"))

    def test_long_jump_fallback_coins_require_capless(self):
        self.collect_wing_mario_over_the_rainbow_access()
        self.assertTrue(self.can_reach_location("Wing Mario Over the Rainbow - 2 Coins"))
        self.assertFalse(self.can_reach_location("Wing Mario Over the Rainbow - 3 Coins"))

        self.collect(self.get_item_by_name("Long Jump"))
        self.assertFalse(self.can_reach_location("Wing Mario Over the Rainbow - 3 Coins"))

        self.collect(self.world.create_item("ut_glitch"))
        self.assertTrue(self.can_reach_location("Wing Mario Over the Rainbow - 6 Coins"))
        self.assertFalse(self.can_reach_location("Wing Mario Over the Rainbow - 7 Coins"))

        self.collect(self.get_item_by_name("Ledge Grab"))
        self.assertFalse(self.can_reach_location("Wing Mario Over the Rainbow - 7 Coins"))

    def test_wing_cap_fallback_coins_require_moveless(self):
        self.collect_wing_mario_over_the_rainbow_access()
        self.assertTrue(self.can_reach_location("Wing Mario Over the Rainbow - 2 Coins"))
        self.assertFalse(self.can_reach_location("Wing Mario Over the Rainbow - 3 Coins"))

        self.collect(self.get_item_by_name("Wing Cap"))
        self.assertFalse(self.can_reach_location("Wing Mario Over the Rainbow - 3 Coins"))

        self.collect(self.world.create_item("ut_glitch"))
        self.assertTrue(self.can_reach_location("Wing Mario Over the Rainbow - 4 Coins"))
        self.assertFalse(self.can_reach_location("Wing Mario Over the Rainbow - 5 Coins"))

    def test_wing_cap_does_not_remove_long_jump_coins(self):
        self.collect_wing_mario_over_the_rainbow_access()
        self.collect(self.get_item_by_name("Long Jump"))
        self.collect(self.world.create_item("ut_glitch"))
        self.assertTrue(self.can_reach_location("Wing Mario Over the Rainbow - 6 Coins"))
        self.assertFalse(self.can_reach_location("Wing Mario Over the Rainbow - 7 Coins"))

        self.collect(self.get_item_by_name("Wing Cap"))
        self.assertTrue(self.can_reach_location("Wing Mario Over the Rainbow - 6 Coins"))
        self.assertFalse(self.can_reach_location("Wing Mario Over the Rainbow - 7 Coins"))

    def test_cannon_coin_route_requires_cannon_movement(self):
        self.collect_wing_mario_over_the_rainbow_access()
        self.collect([
            self.get_item_by_name("Wing Cap"),
            self.get_item_by_name("Wing Mario Over the Rainbow - Cannon Unlock"),
        ])
        self.assertFalse(self.can_reach_location("Wing Mario Over the Rainbow - 7 Coins"))

        self.collect(self.get_item_by_name("Triple Jump"))
        self.assertTrue(self.can_reach_location("Wing Mario Over the Rainbow - 56 Coins"))

    def test_cannon_coin_route_accepts_capless_long_jump(self):
        self.collect_wing_mario_over_the_rainbow_access()
        self.collect([
            self.get_item_by_name("Wing Cap"),
            self.get_item_by_name("Wing Mario Over the Rainbow - Cannon Unlock"),
            self.get_item_by_name("Long Jump"),
        ])
        self.assertFalse(self.can_reach_location("Wing Mario Over the Rainbow - 56 Coins"))

        self.collect(self.world.create_item("ut_glitch"))
        self.assertTrue(self.can_reach_location("Wing Mario Over the Rainbow - 56 Coins"))


class CoolCoolMountainCoinStarAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_ARBITRARY_FEATURE_OPTIONS,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "buddy_checks": Options.BuddyChecks.option_true,
        "enable_locked_paintings": Options.EnableLockedPaintings.option_false,
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "area_rando": Options.AreaRandomizer.option_Off,
    }


class CoolCoolMountainCoinStar130AccessTestBase(CoolCoolMountainCoinStarAccessTestBase):
    options = {
        **CoolCoolMountainCoinStarAccessTestBase.options,
        "cool_cool_mountain_coin_star_requirement": 130,
    }

    def test_start_coins_reach_coin_star(self):
        self.assertTrue(self.can_reach_location("Cool, Cool Mountain - Coins Star"))


class CoolCoolMountainCoinStar131AccessTestBase(CoolCoolMountainCoinStarAccessTestBase):
    options = {
        **CoolCoolMountainCoinStarAccessTestBase.options,
        "cool_cool_mountain_coin_star_requirement": 131,
    }

    def test_wall_kicks_route_coins_require_cannon_with_strict_moves(self):
        self.assertFalse(self.can_reach_location("Cool, Cool Mountain - Coins Star"))
        self.collect(self.get_item_by_name("Cool, Cool Mountain - Cannon Unlock"))
        self.assertTrue(self.can_reach_location("Cool, Cool Mountain - Coins Star"))


class CoolCoolMountainCoinStar141SpinJumpAccessTestBase(CoolCoolMountainCoinStarAccessTestBase):
    options = {
        **CoolCoolMountainCoinStarAccessTestBase.options,
        "logic_tricks": {"Cool, Cool Mountain Wall Kicks Will Work With Spin Jump"},
        "cool_cool_mountain_coin_star_requirement": 141,
    }

    def test_spin_jump_wall_kicks_route_coins_reach_coin_star(self):
        self.assertTrue(self.can_reach_location("Cool, Cool Mountain - Wall Kicks Will Work"))
        self.assertTrue(self.can_reach_location("Cool, Cool Mountain - Coins Star"))


class CoolCoolMountainCoinStar144SpinJumpAccessTestBase(CoolCoolMountainCoinStarAccessTestBase):
    options = {
        **CoolCoolMountainCoinStarAccessTestBase.options,
        "logic_tricks": {"Cool, Cool Mountain Wall Kicks Will Work With Spin Jump"},
        "cool_cool_mountain_coin_star_requirement": 144,
    }

    def test_spin_jump_wall_kicks_route_needs_cannon_for_extra_spindrift_coins(self):
        self.assertFalse(self.can_reach_location("Cool, Cool Mountain - Coins Star"))
        self.collect(self.get_item_by_name("Cool, Cool Mountain - Cannon Unlock"))
        self.assertTrue(self.can_reach_location("Cool, Cool Mountain - Coins Star"))


class CoolCoolMountainCoinStar154AccessTestBase(CoolCoolMountainCoinStarAccessTestBase):
    options = {
        **CoolCoolMountainCoinStarAccessTestBase.options,
        "cool_cool_mountain_coin_star_requirement": 154,
    }

    def test_all_coin_sources_reach_coin_star(self):
        self.collect(self.get_item_by_name("Cool, Cool Mountain - Cannon Unlock"))
        self.assertFalse(self.can_reach_location("Cool, Cool Mountain - Coins Star"))
        self.collect(self.get_item_by_name("Ground Pound"))
        self.assertTrue(self.can_reach_location("Cool, Cool Mountain - Coins Star"))


class WhompsFortressCoinStarAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_ARBITRARY_FEATURE_OPTIONS,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "buddy_checks": Options.BuddyChecks.option_true,
        "enable_locked_paintings": Options.EnableLockedPaintings.option_false,
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "area_rando": Options.AreaRandomizer.option_Off,
    }


class WhompsFortressCoinStar83AccessTestBase(WhompsFortressCoinStarAccessTestBase):
    options = {
        **WhompsFortressCoinStarAccessTestBase.options,
        "whomps_fortress_coin_star_requirement": 83,
    }

    def test_start_coins_reach_coin_star(self):
        self.assertTrue(self.can_reach_location("Whomp's Fortress - Coins Star"))


class WhompsFortressCoinStar84AccessTestBase(WhompsFortressCoinStarAccessTestBase):
    options = {
        **WhompsFortressCoinStarAccessTestBase.options,
        "whomps_fortress_coin_star_requirement": 84,
    }

    def test_shoot_into_the_wild_blue_coins_reach_coin_star(self):
        self.assertFalse(self.can_reach_location("Whomp's Fortress - Coins Star"))
        self.collect(self.get_item_by_name("Whomp's Fortress - Cannon Unlock"))
        self.assertTrue(self.can_reach_location("Whomp's Fortress - Shoot into the Wild Blue"))
        self.assertTrue(self.can_reach_location("Whomp's Fortress - Coins Star"))


class WhompsFortressCoinStar92AccessTestBase(WhompsFortressCoinStarAccessTestBase):
    options = {
        **WhompsFortressCoinStarAccessTestBase.options,
        "whomps_fortress_coin_star_requirement": 92,
    }

    def test_top_coins_reach_coin_star(self):
        self.assertFalse(self.can_reach_location("Whomp's Fortress - Coins Star"))
        self.collect(self.get_item_by_name("Checkerboard Platforms"))
        self.assertTrue(self.can_reach_region("Whomp's Fortress - Top"))
        self.assertTrue(self.can_reach_location("Whomp's Fortress - Coins Star"))


class WhompsFortressCoinStar104AccessTestBase(WhompsFortressCoinStarAccessTestBase):
    options = {
        **WhompsFortressCoinStarAccessTestBase.options,
        "whomps_fortress_coin_star_requirement": 104,
    }

    def test_ground_pound_coins_reach_coin_star(self):
        self.assertFalse(self.can_reach_location("Whomp's Fortress - Coins Star"))
        self.collect(self.get_item_by_name("Ground Pound"))
        self.assertTrue(self.can_reach_location("Whomp's Fortress - Coins Star"))


class WhompsFortressCoinStar141AccessTestBase(WhompsFortressCoinStarAccessTestBase):
    options = {
        **WhompsFortressCoinStarAccessTestBase.options,
        "whomps_fortress_coin_star_requirement": 141,
    }

    def test_all_coin_sources_reach_coin_star(self):
        self.collect([
            self.get_item_by_name("Checkerboard Platforms"),
            self.get_item_by_name("Whomp's Fortress - Cannon Unlock"),
        ])
        self.assertTrue(self.can_reach_region("Whomp's Fortress - Top"))
        self.assertTrue(self.can_reach_location("Whomp's Fortress - Shoot into the Wild Blue"))
        self.assertFalse(self.can_reach_location("Whomp's Fortress - Coins Star"))

        self.collect(self.get_item_by_name("Ground Pound"))
        self.assertTrue(self.can_reach_location("Whomp's Fortress - Coins Star"))


class BobOmbBattlefieldCoinStarAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "buddy_checks": Options.BuddyChecks.option_true,
        "enable_locked_paintings": Options.EnableLockedPaintings.option_false,
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "area_rando": Options.AreaRandomizer.option_Off,
    }


class BobOmbBattlefieldCoinStar99AccessTestBase(BobOmbBattlefieldCoinStarAccessTestBase):
    options = {
        **BobOmbBattlefieldCoinStarAccessTestBase.options,
        "bob_omb_battlefield_coin_star_requirement": 99,
    }

    def test_start_coins_reach_coin_star(self):
        self.assertTrue(self.can_reach_location("Bob-omb Battlefield - Coins Star"))


class BobOmbBattlefieldCoinStar102AccessTestBase(BobOmbBattlefieldCoinStarAccessTestBase):
    options = {
        **BobOmbBattlefieldCoinStarAccessTestBase.options,
        "bob_omb_battlefield_coin_star_requirement": 102,
    }

    def test_island_coins_reach_coin_star(self):
        self.assertFalse(self.can_reach_location("Bob-omb Battlefield - Coins Star"))
        self.collect(self.get_item_by_name("Bob-omb Battlefield - Cannon Unlock"))
        self.assertTrue(self.can_reach_region("Bob-omb Battlefield - Island"))
        self.assertTrue(self.can_reach_location("Bob-omb Battlefield - Coins Star"))


class BobOmbBattlefieldCoinStar104AccessTestBase(BobOmbBattlefieldCoinStarAccessTestBase):
    options = {
        **BobOmbBattlefieldCoinStarAccessTestBase.options,
        "bob_omb_battlefield_coin_star_requirement": 104,
    }

    def test_climb_coins_reach_coin_star(self):
        self.collect(self.get_item_by_name("Bob-omb Battlefield - Cannon Unlock"))
        self.assertFalse(self.can_reach_location("Bob-omb Battlefield - Coins Star"))
        self.collect(self.get_item_by_name("Climb"))
        self.assertTrue(self.can_reach_location("Bob-omb Battlefield - Coins Star"))


class BobOmbBattlefieldCoinStar107AccessTestBase(BobOmbBattlefieldCoinStarAccessTestBase):
    options = {
        **BobOmbBattlefieldCoinStarAccessTestBase.options,
        "bob_omb_battlefield_coin_star_requirement": 107,
    }

    def test_side_flip_backflip_or_triple_jump_coins_reach_coin_star(self):
        self.collect(self.get_item_by_name("Bob-omb Battlefield - Cannon Unlock"))
        self.assertFalse(self.can_reach_location("Bob-omb Battlefield - Coins Star"))
        self.collect(self.get_item_by_name("Side Flip"))
        self.assertTrue(self.can_reach_location("Bob-omb Battlefield - Coins Star"))


class BobOmbBattlefieldCoinStar110AccessTestBase(BobOmbBattlefieldCoinStarAccessTestBase):
    options = {
        **BobOmbBattlefieldCoinStarAccessTestBase.options,
        "bob_omb_battlefield_coin_star_requirement": 110,
    }

    def test_triple_jump_extra_coin_reaches_coin_star(self):
        self.collect([
            self.get_item_by_name("Bob-omb Battlefield - Cannon Unlock"),
            self.get_item_by_name("Side Flip"),
        ])
        self.assertFalse(self.can_reach_location("Bob-omb Battlefield - Coins Star"))
        self.remove_by_name("Side Flip")
        self.collect(self.get_item_by_name("Triple Jump"))
        self.assertTrue(self.can_reach_location("Bob-omb Battlefield - Coins Star"))


class BobOmbBattlefieldCoinStar146AccessTestBase(BobOmbBattlefieldCoinStarAccessTestBase):
    options = {
        **BobOmbBattlefieldCoinStarAccessTestBase.options,
        "bob_omb_battlefield_coin_star_requirement": 146,
    }

    def test_mario_wings_to_the_sky_coins_reach_coin_star(self):
        self.collect(self.get_item_by_name("Bob-omb Battlefield - Cannon Unlock"))
        self.assertFalse(self.can_reach_location("Bob-omb Battlefield - Coins Star"))
        self.collect(self.get_item_by_name("Wing Cap"))
        self.assertTrue(self.can_reach_location("Bob-omb Battlefield - Mario Wings to the Sky"))
        self.assertTrue(self.can_reach_location("Bob-omb Battlefield - Coins Star"))


class JollyRogerBayCoinStarAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "buddy_checks": Options.BuddyChecks.option_true,
        "enable_locked_paintings": Options.EnableLockedPaintings.option_false,
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "area_rando": Options.AreaRandomizer.option_Off,
    }


class JollyRogerBayLogicTricksTestBase(JollyRogerBayCoinStarAccessTestBase):
    options = {
        **JollyRogerBayCoinStarAccessTestBase.options,
        "logic_tricks": {
            "Jolly Roger Bay Upper Platform with Dive and Kick",
            "Jolly Roger Bay Pillar Red Coin with Triple Jump, Backflip, or Wall Kick",
            "Jolly Roger Bay Stone Pillar without Cannon",
            "Jolly Roger Bay Through the Jet Stream without Metal Cap",
        },
    }

    def test_dive_and_kick_reach_upper(self):
        self.collect(self.get_item_by_name("Dive"))
        self.assertFalse(self.can_reach_region("Jolly Roger Bay - Upper"))
        self.collect(self.get_item_by_name("Kick"))
        self.assertTrue(self.can_reach_region("Jolly Roger Bay - Upper"))

    def test_pillar_moves_reach_raised_ship_red_coins(self):
        self.collect(self.get_item_by_name("Jolly Roger Bay - Raised Ship"))
        self.assertFalse(self.can_reach_location("Jolly Roger Bay - Red Coins on the Ship Afloat"))
        self.collect(self.get_item_by_name("Backflip"))
        self.assertTrue(self.can_reach_location("Jolly Roger Bay - Red Coins on the Ship Afloat"))

    def test_stone_pillar_without_cannon(self):
        self.assertTrue(self.can_reach_location("Jolly Roger Bay - Blast to the Stone Pillar"))

    def test_jet_stream_without_metal_cap(self):
        self.assertFalse(self.can_reach_location("Jolly Roger Bay - Through the Jet Stream"))
        self.collect(self.get_item_by_name("Jolly Roger Bay - Jet Stream"))
        self.assertTrue(self.can_reach_location("Jolly Roger Bay - Through the Jet Stream"))


class JollyRogerBayCoinStar49AccessTestBase(JollyRogerBayCoinStarAccessTestBase):
    options = {
        **JollyRogerBayCoinStarAccessTestBase.options,
        "jolly_roger_bay_coin_star_requirement": 49,
    }

    def test_start_coins_reach_coin_star(self):
        self.assertTrue(self.can_reach_location("Jolly Roger Bay - Coins Star"))


class JollyRogerBayCoinStar51AccessTestBase(JollyRogerBayCoinStarAccessTestBase):
    options = {
        **JollyRogerBayCoinStarAccessTestBase.options,
        "logic_tricks": {"Jolly Roger Bay Pillar Red Coin with Cannon"},
        "jolly_roger_bay_coin_star_requirement": 51,
    }

    def test_climb_start_coins_reach_coin_star(self):
        self.assertFalse(self.can_reach_location("Jolly Roger Bay - Coins Star"))
        self.collect(self.get_item_by_name("Climb"))
        self.assertTrue(self.can_reach_location("Jolly Roger Bay - Coins Star"))

    def test_cannon_start_coins_reach_coin_star(self):
        self.assertFalse(self.can_reach_location("Jolly Roger Bay - Coins Star"))
        self.collect(self.get_item_by_name("Jolly Roger Bay - Cannon Unlock"))
        self.assertTrue(self.can_reach_location("Jolly Roger Bay - Coins Star"))

    def test_raised_ship_without_upper_does_not_reach_coin_star(self):
        self.collect(self.get_item_by_name("Jolly Roger Bay - Raised Ship"))
        self.assertFalse(self.can_reach_location("Jolly Roger Bay - Coins Star"))


class JollyRogerBayCoinStar55AccessTestBase(JollyRogerBayCoinStarAccessTestBase):
    options = {
        **JollyRogerBayCoinStarAccessTestBase.options,
        "jolly_roger_bay_coin_star_requirement": 55,
    }

    def test_upper_coins_reach_coin_star(self):
        self.assertFalse(self.can_reach_location("Jolly Roger Bay - Coins Star"))
        self.collect(self.get_item_by_name("Side Flip"))
        self.assertTrue(self.can_reach_region("Jolly Roger Bay - Upper"))
        self.assertTrue(self.can_reach_location("Jolly Roger Bay - Coins Star"))


class JollyRogerBayCoinStar68AccessTestBase(JollyRogerBayCoinStarAccessTestBase):
    options = {
        **JollyRogerBayCoinStarAccessTestBase.options,
        "purple_switches": Options.PurpleSwitches.option_global,
        "logic_tricks": {"Jolly Roger Bay Ship Red Coin With Long Jump"},
        "universal_tracker_glitched_logic": {
            "Jolly Roger Bay Pillar Red Coin with Triple Jump, Backflip, or Wall Kick"
        },
        "jolly_roger_bay_coin_star_requirement": 68,
    }

    def test_upper_long_jump_coins_reach_coin_star(self):
        self.collect(self.get_item_by_name("Side Flip"))
        self.assertFalse(self.can_reach_location("Jolly Roger Bay - Coins Star"))
        self.collect(self.get_item_by_name("Long Jump"))
        self.assertTrue(self.can_reach_location("Jolly Roger Bay - Coins Star"))

    def test_upper_purple_switch_coins_reach_coin_star(self):
        self.collect(self.get_item_by_name("Side Flip"))
        self.assertFalse(self.can_reach_location("Jolly Roger Bay - Coins Star"))
        self.collect(self.get_item_by_name("Purple Switches"))
        self.assertTrue(self.can_reach_location("Jolly Roger Bay - Coins Star"))

    def test_moveless_start_coins_reach_coin_star(self):
        self.collect(self.get_item_by_name("Backflip"))
        self.assertFalse(self.can_reach_location("Jolly Roger Bay - Coins Star"))
        self.collect(self.world.create_item("ut_glitch"))
        self.assertTrue(self.can_reach_location("Jolly Roger Bay - Coins Star"))


class JollyRogerBayCoinStar72AccessTestBase(JollyRogerBayCoinStarAccessTestBase):
    options = {
        **JollyRogerBayCoinStarAccessTestBase.options,
        "jolly_roger_bay_coin_star_requirement": 72,
    }

    def test_raised_ship_coins_reach_coin_star(self):
        self.collect(self.get_item_by_name("Side Flip"))
        self.assertFalse(self.can_reach_location("Jolly Roger Bay - Coins Star"))
        self.collect(self.get_item_by_name("Jolly Roger Bay - Raised Ship"))
        self.assertTrue(self.can_reach_location("Jolly Roger Bay - Coins Star"))


class JollyRogerBayCoinStar79AccessTestBase(JollyRogerBayCoinStarAccessTestBase):
    options = {
        **JollyRogerBayCoinStarAccessTestBase.options,
        "jolly_roger_bay_coin_star_requirement": 79,
    }

    def test_ground_pound_coins_reach_coin_star(self):
        self.assertFalse(self.can_reach_location("Jolly Roger Bay - Coins Star"))
        self.collect(self.get_item_by_name("Ground Pound"))
        self.assertTrue(self.can_reach_location("Jolly Roger Bay - Coins Star"))


class JollyRogerBayCoinStar96AccessTestBase(JollyRogerBayCoinStarAccessTestBase):
    options = {
        **JollyRogerBayCoinStarAccessTestBase.options,
        "jolly_roger_bay_coin_star_requirement": 96,
    }

    def test_ground_pound_and_upper_coins_reach_coin_star(self):
        self.collect(self.get_item_by_name("Ground Pound"))
        self.assertFalse(self.can_reach_location("Jolly Roger Bay - Coins Star"))
        self.collect(self.get_item_by_name("Side Flip"))
        self.assertTrue(self.can_reach_location("Jolly Roger Bay - Coins Star"))


class JollyRogerBayCoinStar104AccessTestBase(JollyRogerBayCoinStarAccessTestBase):
    options = {
        **JollyRogerBayCoinStarAccessTestBase.options,
        "jolly_roger_bay_coin_star_requirement": 104,
    }

    def test_all_jrb_coin_sources_reach_coin_star(self):
        self.collect([
            self.get_item_by_name("Ground Pound"),
            self.get_item_by_name("Side Flip"),
            self.get_item_by_name("Climb"),
        ])
        self.assertFalse(self.can_reach_location("Jolly Roger Bay - Coins Star"))
        self.collect(self.get_item_by_name("Jolly Roger Bay - Raised Ship"))
        self.assertTrue(self.can_reach_location("Jolly Roger Bay - Coins Star"))


class TinyHugeIslandCoinStarAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_ARBITRARY_FEATURE_OPTIONS,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "buddy_checks": Options.BuddyChecks.option_true,
        "enable_locked_paintings": Options.EnableLockedPaintings.option_false,
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "area_rando": Options.AreaRandomizer.option_Off,
    }

    def collect_second_floor_access(self):
        self.collect(self.get_item_by_name("Progressive Upstairs Key"))

    def disable_huge_entry(self):
        self.multiworld.get_entrance("Second Floor -> Tiny-Huge Island (Huge)", self.player).access_rule = \
            lambda state: False

    def disable_tiny_entry(self):
        self.multiworld.get_entrance("Second Floor -> Tiny-Huge Island (Tiny)", self.player).access_rule = \
            lambda state: False


class TinyHugeIslandCoinStar1AccessTestBase(TinyHugeIslandCoinStarAccessTestBase):
    options = {
        **TinyHugeIslandCoinStarAccessTestBase.options,
        "tiny_huge_island_coin_star_requirement": 1,
    }

    def test_tiny_start_coin_reaches_coin_star(self):
        self.disable_huge_entry()
        self.collect_second_floor_access()
        self.assertTrue(self.can_reach_region("Tiny-Huge Island (Tiny)"))
        self.assertTrue(self.can_reach_location("Tiny-Huge Island - Coins Star"))


class TinyHugeIslandCoinStar33AccessTestBase(TinyHugeIslandCoinStarAccessTestBase):
    options = {
        **TinyHugeIslandCoinStarAccessTestBase.options,
        "tiny_huge_island_coin_star_requirement": 33,
    }

    def test_five_itty_bitty_secrets_coins_reach_coin_star_from_tiny(self):
        self.disable_huge_entry()
        self.collect_second_floor_access()
        self.assertFalse(self.can_reach_location("Tiny-Huge Island - Coins Star"))
        self.collect([
            self.get_item_by_name("Purple Switches"),
            self.get_item_by_name("Long Jump"),
        ])
        self.assertTrue(self.can_reach_location("Tiny-Huge Island - Five Itty Bitty Secrets"))
        self.assertTrue(self.can_reach_location("Tiny-Huge Island - Coins Star"))


class TinyHugeIslandCoinStar56FromTinyAccessTestBase(TinyHugeIslandCoinStarAccessTestBase):
    options = {
        **TinyHugeIslandCoinStarAccessTestBase.options,
        "tiny_huge_island_coin_star_requirement": 56,
    }

    def test_tiny_pipe_reaches_huge_piranha_area_and_huge_main(self):
        self.disable_huge_entry()
        self.collect_second_floor_access()
        self.assertTrue(self.can_reach_region("Tiny-Huge Island (Tiny)"))
        self.assertFalse(self.can_reach_region("Tiny-Huge Island (Huge)"))
        self.assertFalse(self.can_reach_location("Tiny-Huge Island - Coins Star"))

        self.collect([
            self.get_item_by_name("Ledge Grab"),
            self.get_item_by_name("Tiny-Huge Island - Warp Pipes"),
        ])
        self.assertTrue(self.can_reach_region("Tiny-Huge Island (Huge)"))
        self.assertTrue(self.can_reach_region("Tiny-Huge Island - Huge Piranha Area"))
        self.assertTrue(self.can_reach_location("Tiny-Huge Island - Coins Star"))


class TinyHugeIslandCoinStar54AccessTestBase(TinyHugeIslandCoinStarAccessTestBase):
    options = {
        **TinyHugeIslandCoinStarAccessTestBase.options,
        "tiny_huge_island_coin_star_requirement": 54,
    }

    def test_huge_start_coins_reach_coin_star(self):
        self.disable_tiny_entry()
        self.collect_second_floor_access()
        self.assertTrue(self.can_reach_region("Tiny-Huge Island (Huge)"))
        self.assertTrue(self.can_reach_location("Tiny-Huge Island - Coins Star"))


class TinyHugeIslandCoinStar55FromHugeAccessTestBase(TinyHugeIslandCoinStarAccessTestBase):
    options = {
        **TinyHugeIslandCoinStarAccessTestBase.options,
        "tiny_huge_island_coin_star_requirement": 55,
    }

    def test_huge_start_reaches_tiny_coin_with_pipes(self):
        self.disable_tiny_entry()
        self.collect_second_floor_access()
        self.assertFalse(self.can_reach_location("Tiny-Huge Island - Coins Star"))
        self.collect(self.get_item_by_name("Tiny-Huge Island - Warp Pipes"))
        self.assertTrue(self.can_reach_region("Tiny-Huge Island - Tiny Main"))
        self.assertTrue(self.can_reach_location("Tiny-Huge Island - Coins Star"))


class TinyHugeIslandCoinStar84AccessTestBase(TinyHugeIslandCoinStarAccessTestBase):
    options = {
        **TinyHugeIslandCoinStarAccessTestBase.options,
        "tiny_huge_island_coin_star_requirement": 84,
    }

    def test_wall_kick_coins_require_top_gate(self):
        self.disable_tiny_entry()
        self.collect_second_floor_access()
        self.assertFalse(self.can_reach_location("Tiny-Huge Island - Coins Star"))
        self.collect(self.get_item_by_name("Wall Kick"))
        self.assertFalse(self.can_reach_location("Tiny-Huge Island - Coins Star"))
        self.collect(self.get_item_by_name("Tiny-Huge Island - Cannon Unlock"))
        self.assertTrue(self.can_reach_location("Tiny-Huge Island - Coins Star"))


class TinyHugeIslandCoinStar80AccessTestBase(TinyHugeIslandCoinStarAccessTestBase):
    options = {
        **TinyHugeIslandCoinStarAccessTestBase.options,
        "tiny_huge_island_coin_star_requirement": 80,
    }

    def test_cannon_coins_reach_coin_star(self):
        self.disable_tiny_entry()
        self.collect_second_floor_access()
        self.assertFalse(self.can_reach_location("Tiny-Huge Island - Coins Star"))
        self.collect(self.get_item_by_name("Tiny-Huge Island - Cannon Unlock"))
        self.assertTrue(self.can_reach_location("Tiny-Huge Island - Coins Star"))


class TinyHugeIslandCoinStar100AccessTestBase(TinyHugeIslandCoinStarAccessTestBase):
    options = {
        **TinyHugeIslandCoinStarAccessTestBase.options,
        "tiny_huge_island_coin_star_requirement": 100,
    }

    def test_ground_pound_coins_reach_coin_star(self):
        self.disable_tiny_entry()
        self.collect_second_floor_access()
        self.assertFalse(self.can_reach_location("Tiny-Huge Island - Coins Star"))
        self.collect(self.get_item_by_name("Ground Pound"))
        self.assertTrue(self.can_reach_location("Tiny-Huge Island - Coins Star"))


class TinyHugeIslandCoinStar134AccessTestBase(TinyHugeIslandCoinStarAccessTestBase):
    options = {
        **TinyHugeIslandCoinStarAccessTestBase.options,
        "tiny_huge_island_coin_star_requirement": 134,
    }

    def test_top_gated_ground_pound_coins_reach_coin_star(self):
        self.disable_tiny_entry()
        self.collect_second_floor_access()
        self.collect([
            self.get_item_by_name("Ground Pound"),
        ])
        self.assertFalse(self.can_reach_location("Tiny-Huge Island - Coins Star"))
        self.collect(self.get_item_by_name("Tiny-Huge Island - Cannon Unlock"))
        self.assertTrue(self.can_reach_location("Tiny-Huge Island - Coins Star"))


class TinyHugeIslandCoinStar86AccessTestBase(TinyHugeIslandCoinStarAccessTestBase):
    options = {
        **TinyHugeIslandCoinStarAccessTestBase.options,
        "tiny_huge_island_coin_star_requirement": 86,
    }

    def test_huge_piranha_area_and_final_tiny_main_coin_require_purple_switches(self):
        self.disable_tiny_entry()
        self.collect_second_floor_access()
        self.assertFalse(self.can_reach_location("Tiny-Huge Island - Coins Star"))
        self.collect(self.get_item_by_name("Tiny-Huge Island - Warp Pipes"))
        self.assertFalse(self.can_reach_region("Tiny-Huge Island - Huge Piranha Area"))
        self.assertFalse(self.can_reach_location("Tiny-Huge Island - Coins Star"))
        self.collect(self.get_item_by_name("Purple Switches"))
        self.assertTrue(self.can_reach_region("Tiny-Huge Island - Huge Piranha Area"))
        self.assertTrue(self.can_reach_location("Tiny-Huge Island - Coins Star"))


class TinyHugeIslandCoinStar12FromTinyAccessTestBase(TinyHugeIslandCoinStarAccessTestBase):
    options = {
        **TinyHugeIslandCoinStarAccessTestBase.options,
        "tiny_huge_island_coin_star_requirement": 12,
    }

    def test_huge_piranha_area_connects_to_huge_main_when_huge_entrance_is_disabled(self):
        self.disable_huge_entry()
        self.collect_second_floor_access()
        self.collect([
            self.get_item_by_name("Long Jump"),
            self.get_item_by_name("Tiny-Huge Island - Warp Pipes"),
        ])
        self.assertTrue(self.can_reach_region("Tiny-Huge Island - Tiny Piranha Area"))
        self.assertTrue(self.can_reach_region("Tiny-Huge Island (Huge)"))
        self.assertTrue(self.can_reach_region("Tiny-Huge Island - Huge Piranha Area"))
        self.assertTrue(self.can_reach_location("Tiny-Huge Island - Coins Star"))


class TinyHugeIslandCoinStar66FromTinyAccessTestBase(TinyHugeIslandCoinStarAccessTestBase):
    options = {
        **TinyHugeIslandCoinStarAccessTestBase.options,
        "tiny_huge_island_coin_star_requirement": 66,
    }

    def test_huge_piranha_area_coins_need_reentry_when_huge_island_is_reachable(self):
        self.collect_second_floor_access()
        self.collect([
            self.get_item_by_name("Ledge Grab"),
            self.get_item_by_name("Tiny-Huge Island - Warp Pipes"),
        ])
        self.assertTrue(self.can_reach_region("Tiny-Huge Island (Huge)"))
        self.assertTrue(self.can_reach_region("Tiny-Huge Island - Huge Piranha Area"))
        self.assertTrue(self.can_reach_location("Tiny-Huge Island - Coins Star"))
        self.collect(self.get_item_by_name("Purple Switches"))
        self.assertTrue(self.can_reach_region("Tiny-Huge Island - Huge Piranha Area"))
        self.assertTrue(self.can_reach_location("Tiny-Huge Island - Coins Star"))


class TinyHugeIslandCoinStar85AccessTestBase(TinyHugeIslandCoinStarAccessTestBase):
    options = {
        **TinyHugeIslandCoinStarAccessTestBase.options,
        "tiny_huge_island_coin_star_requirement": 85,
    }

    def test_top_return_movement_reaches_huge_piranha_and_top_gate_coins(self):
        self.disable_tiny_entry()
        self.collect_second_floor_access()
        self.assertFalse(self.can_reach_location("Tiny-Huge Island - Coins Star"))
        self.collect(self.get_item_by_name("Triple Jump"))
        self.assertTrue(self.can_reach_region("Tiny-Huge Island - Huge Piranha Area"))
        self.assertTrue(self.can_reach_location("Tiny-Huge Island - Coins Star"))


class TinyHugeIslandCoinStar150AccessTestBase(TinyHugeIslandCoinStarAccessTestBase):
    options = {
        **TinyHugeIslandCoinStarAccessTestBase.options,
        "tiny_huge_island_coin_star_requirement": 150,
    }

    def test_wiggler_and_ground_pound_coins_reach_coin_star(self):
        self.disable_tiny_entry()
        self.collect_second_floor_access()
        self.collect([
            self.get_item_by_name("Ledge Grab"),
            self.get_item_by_name("Dive"),
            self.get_item_by_name("Purple Switches"),
            self.get_item_by_name("Tiny-Huge Island - Warp Pipes"),
        ])
        self.assertFalse(self.can_reach_location("Tiny-Huge Island - Coins Star"))
        self.collect(self.get_item_by_name("Ground Pound"))
        self.assertTrue(self.can_reach_location("Tiny-Huge Island - Make Wiggler Squirm"))
        self.assertTrue(self.can_reach_location("Tiny-Huge Island - Coins Star"))


class TinyHugeIslandCoinStar191AccessTestBase(TinyHugeIslandCoinStarAccessTestBase):
    options = {
        **TinyHugeIslandCoinStarAccessTestBase.options,
        "tiny_huge_island_coin_star_requirement": 191,
    }

    def test_all_coin_sources_reach_coin_star(self):
        self.disable_tiny_entry()
        self.collect_second_floor_access()
        self.collect([
            self.get_item_by_name("Ledge Grab"),
            self.get_item_by_name("Dive"),
            self.get_item_by_name("Ground Pound"),
            self.get_item_by_name("Wall Kick"),
            self.get_item_by_name("Purple Switches"),
            self.get_item_by_name("Tiny-Huge Island - Warp Pipes"),
        ])
        self.assertTrue(self.can_reach_location("Tiny-Huge Island - Five Itty Bitty Secrets"))
        self.assertTrue(self.can_reach_region("Tiny-Huge Island - Huge Piranha Area"))
        self.assertTrue(self.can_reach_location("Tiny-Huge Island - Make Wiggler Squirm"))
        self.assertFalse(self.can_reach_location("Tiny-Huge Island - Coins Star"))
        self.collect(self.get_item_by_name("Tiny-Huge Island - Cannon Unlock"))
        self.assertTrue(self.can_reach_location("Tiny-Huge Island - Coins Star"))


class DireDireDocksCoinStarAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_ARBITRARY_FEATURE_OPTIONS,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "buddy_checks": Options.BuddyChecks.option_true,
        "enable_locked_paintings": Options.EnableLockedPaintings.option_false,
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "area_rando": Options.AreaRandomizer.option_Off,
    }

    def test_red_coins_and_hundred_coins_require_purple_switches(self):
        self.collect([self.get_item_by_name("Progressive Basement Key")] * 2)
        self.collect([
            self.get_item_by_name("Dire, Dire Docks - Poles"),
            self.get_item_by_name("Climb"),
            self.get_item_by_name("Ground Pound"),
        ])
        self.assertFalse(self.can_reach_location("Dire, Dire Docks - Pole-Jumping for Red Coins"))
        self.assertFalse(self.can_reach_location("Dire, Dire Docks - Coins Star"))

        self.collect(self.get_item_by_name("Purple Switches"))
        self.assertTrue(self.can_reach_location("Dire, Dire Docks - Pole-Jumping for Red Coins"))
        self.assertTrue(self.can_reach_location("Dire, Dire Docks - Coins Star"))


class DireDireDocksCoinStarThresholdTestBase(SM64TestBase):
    run_default_tests = False
    options = DireDireDocksCoinStarAccessTestBase.options


class DireDireDocksCoinStar60AccessTestBase(DireDireDocksCoinStarThresholdTestBase):
    options = {
        **DireDireDocksCoinStarThresholdTestBase.options,
        "dire_dire_docks_coin_star_requirement": 60,
    }

    def test_start_coins_reach_coin_star(self):
        self.collect([self.get_item_by_name("Progressive Basement Key")] * 2)
        self.assertTrue(self.can_reach_location("Dire, Dire Docks - Coins Star"))


class DireDireDocksCoinStar61AccessTestBase(DireDireDocksCoinStarThresholdTestBase):
    options = {
        **DireDireDocksCoinStarThresholdTestBase.options,
        "dire_dire_docks_coin_star_requirement": 61,
    }

    def test_purple_switch_coins_reach_coin_star(self):
        self.collect([self.get_item_by_name("Progressive Basement Key")] * 2)
        self.assertFalse(self.can_reach_location("Dire, Dire Docks - Coins Star"))
        self.collect(self.get_item_by_name("Purple Switches"))
        self.assertTrue(self.can_reach_location("Dire, Dire Docks - Coins Star"))


class DireDireDocksCoinStar63AccessTestBase(DireDireDocksCoinStarThresholdTestBase):
    options = {
        **DireDireDocksCoinStarThresholdTestBase.options,
        "dire_dire_docks_coin_star_requirement": 63,
    }

    def test_poles_coins_reach_coin_star(self):
        self.collect([self.get_item_by_name("Progressive Basement Key")] * 2)
        self.collect(self.get_item_by_name("Purple Switches"))
        self.assertFalse(self.can_reach_location("Dire, Dire Docks - Coins Star"))
        self.collect(self.get_item_by_name("Dire, Dire Docks - Poles"))
        self.assertFalse(self.can_reach_location("Dire, Dire Docks - Coins Star"))
        self.collect(self.get_item_by_name("Climb"))
        self.assertTrue(self.can_reach_location("Dire, Dire Docks - Coins Star"))


class DireDireDocksCoinStar77AccessTestBase(DireDireDocksCoinStarThresholdTestBase):
    options = {
        **DireDireDocksCoinStarThresholdTestBase.options,
        "dire_dire_docks_coin_star_requirement": 77,
    }

    def test_ground_pound_coins_reach_coin_star(self):
        self.collect([self.get_item_by_name("Progressive Basement Key")] * 2)
        self.collect([
            self.get_item_by_name("Purple Switches"),
            self.get_item_by_name("Dire, Dire Docks - Poles"),
        ])
        self.assertFalse(self.can_reach_location("Dire, Dire Docks - Coins Star"))
        self.collect(self.get_item_by_name("Ground Pound"))
        self.assertFalse(self.can_reach_location("Dire, Dire Docks - Coins Star"))
        self.collect(self.get_item_by_name("Climb"))
        self.assertTrue(self.can_reach_location("Dire, Dire Docks - Coins Star"))


class DireDireDocksCoinStar76SubPolesMovementAccessTestBase(DireDireDocksCoinStarThresholdTestBase):
    options = {
        **DireDireDocksCoinStarThresholdTestBase.options,
        "dire_dire_docks_coin_star_requirement": 76,
    }

    def test_sub_poles_triple_jump_climb_reach_purple_switch_and_poles_coins(self):
        self.collect([self.get_item_by_name("Progressive Basement Key")] * 2)
        self.collect([
            self.get_item_by_name("Dire, Dire Docks - Bowser's Sub"),
            self.get_item_by_name("Dire, Dire Docks - Poles"),
            self.get_item_by_name("Triple Jump"),
        ])
        self.assertFalse(self.can_reach_location("Dire, Dire Docks - Coins Star"))
        self.collect(self.get_item_by_name("Climb"))
        self.assertTrue(self.can_reach_location("Dire, Dire Docks - Coins Star"))


class HazyMazeCaveCoinStarAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_ARBITRARY_FEATURE_OPTIONS,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "buddy_checks": Options.BuddyChecks.option_true,
        "enable_locked_paintings": Options.EnableLockedPaintings.option_false,
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "area_rando": Options.AreaRandomizer.option_Off,
    }

    def collect_basement_access(self):
        self.collect(self.get_item_by_name("Progressive Basement Key"))


class HazyMazeCaveCoinsanityAccessTestBase(HazyMazeCaveCoinStarAccessTestBase):
    options = {
        **HazyMazeCaveCoinStarAccessTestBase.options,
        **ONE_COIN_STAR_REQUIREMENTS,
        "coinsanity": 100,
        "hazy_maze_cave_coin_star_requirement": 80,
    }

    def test_coinsanity_location_uses_hmc_coin_logic(self):
        self.collect_basement_access()
        self.assertFalse(self.can_reach_location("Hazy Maze Cave - 79 Coins"))
        self.collect(self.get_item_by_name("Wall Kick"))
        self.assertTrue(self.can_reach_location("Hazy Maze Cave - 79 Coins"))


class HazyMazeCaveCoinStar75AccessTestBase(HazyMazeCaveCoinStarAccessTestBase):
    options = {
        **HazyMazeCaveCoinStarAccessTestBase.options,
        "hazy_maze_cave_coin_star_requirement": 75,
    }

    def test_start_coins_reach_coin_star(self):
        self.collect_basement_access()
        self.assertTrue(self.can_reach_location("Hazy Maze Cave - Coins Star"))


class HazyMazeCaveCoinStar78AccessTestBase(HazyMazeCaveCoinStarAccessTestBase):
    options = {
        **HazyMazeCaveCoinStarAccessTestBase.options,
        "hazy_maze_cave_coin_star_requirement": 78,
    }

    def test_metal_cap_coins_reach_coin_star(self):
        self.collect_basement_access()
        self.assertFalse(self.can_reach_location("Hazy Maze Cave - Coins Star"))
        self.collect(self.get_item_by_name("Metal Cap"))
        self.assertFalse(self.can_reach_location("Hazy Maze Cave - Coins Star"))
        self.collect(self.get_item_by_name("Purple Switches"))
        self.assertTrue(self.can_reach_location("Hazy Maze Cave - Coins Star"))


class HazyMazeCaveCoinStar79AccessTestBase(HazyMazeCaveCoinStarAccessTestBase):
    options = {
        **HazyMazeCaveCoinStarAccessTestBase.options,
        "hazy_maze_cave_coin_star_requirement": 79,
    }

    def test_basic_movement_coins_reach_coin_star(self):
        self.collect_basement_access()
        self.assertFalse(self.can_reach_location("Hazy Maze Cave - Coins Star"))
        self.collect(self.get_item_by_name("Ledge Grab"))
        self.assertTrue(self.can_reach_location("Hazy Maze Cave - Coins Star"))


class HazyMazeCaveCoinStar81AccessTestBase(HazyMazeCaveCoinStarAccessTestBase):
    options = {
        **HazyMazeCaveCoinStarAccessTestBase.options,
        "hazy_maze_cave_coin_star_requirement": 81,
    }

    def test_long_jump_platform_route_coins_reach_coin_star(self):
        self.collect_basement_access()
        self.collect([
            self.get_item_by_name("Ledge Grab"),
            self.get_item_by_name("Climb"),
        ])
        self.assertFalse(self.can_reach_location("Hazy Maze Cave - Coins Star"))
        self.collect(self.get_item_by_name("Long Jump"))
        self.assertTrue(self.can_reach_location("Hazy Maze Cave - Coins Star"))


class HazyMazeCaveCoinStar83CheckerboardAccessTestBase(HazyMazeCaveCoinStarAccessTestBase):
    options = {
        **HazyMazeCaveCoinStarAccessTestBase.options,
        "hazy_maze_cave_coin_star_requirement": 83,
    }

    def test_checkerboard_platform_route_coins_reach_coin_star(self):
        self.collect_basement_access()
        self.collect([
            self.get_item_by_name("Ledge Grab"),
            self.get_item_by_name("Climb"),
            self.get_item_by_name("Long Jump"),
        ])
        self.assertFalse(self.can_reach_location("Hazy Maze Cave - Coins Star"))
        self.collect(self.get_item_by_name("Checkerboard Platforms"))
        self.assertTrue(self.can_reach_location("Hazy Maze Cave - Coins Star"))


class HazyMazeCaveCoinStar86CaplessAccessTestBase(HazyMazeCaveCoinStarAccessTestBase):
    options = {
        **HazyMazeCaveCoinStarAccessTestBase.options,
        "strict_cap_requirements": Options.StrictCapRequirements.option_false,
        "hazy_maze_cave_coin_star_requirement": 86,
    }

    def test_capless_triple_jump_coins_reach_coin_star(self):
        self.collect_basement_access()
        self.assertFalse(self.can_reach_location("Hazy Maze Cave - Coins Star"))
        self.collect([
            self.get_item_by_name("Triple Jump"),
            self.get_item_by_name("Purple Switches"),
        ])
        self.assertTrue(self.can_reach_location("Hazy Maze Cave - Coins Star"))


class HazyMazeCaveCoinStar84AccessTestBase(HazyMazeCaveCoinStarAccessTestBase):
    options = {
        **HazyMazeCaveCoinStarAccessTestBase.options,
        "hazy_maze_cave_coin_star_requirement": 84,
    }

    def test_toxic_maze_coins_reach_coin_star(self):
        self.collect_basement_access()
        self.assertFalse(self.can_reach_location("Hazy Maze Cave - Coins Star"))
        self.collect(self.get_item_by_name("Wall Kick"))
        self.assertTrue(self.can_reach_location("Hazy Maze Cave - Navigating the Toxic Maze"))
        self.assertTrue(self.can_reach_location("Hazy Maze Cave - Coins Star"))


class HazyMazeCaveCoinStar89AccessTestBase(HazyMazeCaveCoinStarAccessTestBase):
    options = {
        **HazyMazeCaveCoinStarAccessTestBase.options,
        "hazy_maze_cave_coin_star_requirement": 89,
    }

    def test_pit_islands_climb_coins_reach_coin_star(self):
        self.collect_basement_access()
        self.collect(self.get_item_by_name("Triple Jump"))
        self.assertTrue(self.can_reach_location("Hazy Maze Cave - Navigating the Toxic Maze"))
        self.assertFalse(self.can_reach_location("Hazy Maze Cave - Coins Star"))

        self.collect(self.get_item_by_name("Climb"))
        self.assertTrue(self.can_reach_region("Hazy Maze Cave - Pit Islands"))
        self.assertTrue(self.can_reach_location("Hazy Maze Cave - Coins Star"))


class HazyMazeCaveCoinStar83SwimmingBeastAccessTestBase(HazyMazeCaveCoinStarAccessTestBase):
    options = {
        **HazyMazeCaveCoinStarAccessTestBase.options,
        "hazy_maze_cave_coin_star_requirement": 83,
    }

    def test_swimming_beast_coins_reach_coin_star(self):
        self.collect_basement_access()
        self.assertFalse(self.can_reach_location("Hazy Maze Cave - Coins Star"))
        self.collect(self.get_item_by_name("Hazy Maze Cave - Swimming Beast"))
        self.assertTrue(self.can_reach_location("Hazy Maze Cave - Coins Star"))


class HazyMazeCaveCoinStar110AccessTestBase(HazyMazeCaveCoinStarAccessTestBase):
    options = {
        **HazyMazeCaveCoinStarAccessTestBase.options,
        "hazy_maze_cave_coin_star_requirement": 110,
    }

    def test_ground_pound_coins_reach_coin_star(self):
        self.collect_basement_access()
        self.assertFalse(self.can_reach_location("Hazy Maze Cave - Coins Star"))
        self.collect(self.get_item_by_name("Ground Pound"))
        self.assertTrue(self.can_reach_location("Hazy Maze Cave - Coins Star"))


class HazyMazeCaveCoinStar139AccessTestBase(HazyMazeCaveCoinStarAccessTestBase):
    options = {
        **HazyMazeCaveCoinStarAccessTestBase.options,
        "hazy_maze_cave_coin_star_requirement": 139,
    }

    def test_all_coin_sources_reach_coin_star(self):
        self.collect_basement_access()
        self.collect([
            self.get_item_by_name("Hazy Maze Cave - Swimming Beast"),
            self.get_item_by_name("Triple Jump"),
            self.get_item_by_name("Metal Cap"),
            self.get_item_by_name("Ground Pound"),
            self.get_item_by_name("Purple Switches"),
        ])
        self.assertFalse(self.can_reach_location("Hazy Maze Cave - Coins Star"))

        self.collect(self.get_item_by_name("Climb"))
        self.assertTrue(self.can_reach_region("Hazy Maze Cave - Pit Islands"))
        self.assertFalse(self.can_reach_location("Hazy Maze Cave - Coins Star"))
        self.collect(self.get_item_by_name("Checkerboard Platforms"))
        self.assertTrue(self.can_reach_location("Hazy Maze Cave - Coins Star"))


class LethalLavaLandCoinStarAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_ARBITRARY_FEATURE_OPTIONS,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "enable_locked_paintings": Options.EnableLockedPaintings.option_false,
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "area_rando": Options.AreaRandomizer.option_Off,
    }

    def collect_basement_access(self):
        self.collect(self.get_item_by_name("Progressive Basement Key"))


class LethalLavaLandCoinStar125AccessTestBase(LethalLavaLandCoinStarAccessTestBase):
    options = {
        **LethalLavaLandCoinStarAccessTestBase.options,
        "lethal_lava_land_coin_star_requirement": 125,
    }

    def test_start_coins_reach_coin_star(self):
        self.collect_basement_access()
        self.assertTrue(self.can_reach_location("Lethal Lava Land - Coins Star"))


class LethalLavaLandCoinStar128AccessTestBase(LethalLavaLandCoinStarAccessTestBase):
    options = {
        **LethalLavaLandCoinStarAccessTestBase.options,
        "lethal_lava_land_coin_star_requirement": 128,
    }

    def test_elevator_tour_coins_reach_coin_star(self):
        self.collect_basement_access()
        self.collect(self.get_item_by_name("Climb"))
        self.assertFalse(self.can_reach_location("Lethal Lava Land - Coins Star"))

        self.collect(self.get_item_by_name("Checkerboard Platforms"))
        self.assertTrue(self.can_reach_location("Lethal Lava Land - Elevator Tour in the Volcano"))
        self.assertTrue(self.can_reach_location("Lethal Lava Land - Coins Star"))


class LethalLavaLandCoinStar130AccessTestBase(LethalLavaLandCoinStarAccessTestBase):
    options = {
        **LethalLavaLandCoinStarAccessTestBase.options,
        "lethal_lava_land_coin_star_requirement": 130,
    }

    def test_koopa_shell_coins_reach_coin_star(self):
        self.collect_basement_access()
        self.assertFalse(self.can_reach_location("Lethal Lava Land - Coins Star"))

        self.collect(self.get_item_by_name("Lethal Lava Land - Koopa Shell"))
        self.assertTrue(self.can_reach_location("Lethal Lava Land - Coins Star"))


class LethalLavaLandCoinStar133AccessTestBase(LethalLavaLandCoinStarAccessTestBase):
    options = {
        **LethalLavaLandCoinStarAccessTestBase.options,
        "lethal_lava_land_coin_star_requirement": 133,
    }

    def test_all_coin_sources_reach_coin_star(self):
        self.collect_basement_access()
        self.collect([
            self.get_item_by_name("Climb"),
            self.get_item_by_name("Lethal Lava Land - Koopa Shell"),
        ])
        self.assertFalse(self.can_reach_location("Lethal Lava Land - Coins Star"))

        self.collect(self.get_item_by_name("Checkerboard Platforms"))
        self.assertTrue(self.can_reach_location("Lethal Lava Land - Elevator Tour in the Volcano"))
        self.assertTrue(self.can_reach_location("Lethal Lava Land - Coins Star"))


class ShiftingSandLandCoinStarAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_ARBITRARY_FEATURE_OPTIONS,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "enable_locked_paintings": Options.EnableLockedPaintings.option_false,
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "area_rando": Options.AreaRandomizer.option_Off,
    }

    def collect_basement_access(self):
        self.collect(self.get_item_by_name("Progressive Basement Key"))


class ShiftingSandLandCoinStar89AccessTestBase(ShiftingSandLandCoinStarAccessTestBase):
    options = {
        **ShiftingSandLandCoinStarAccessTestBase.options,
        "shifting_sand_land_coin_star_requirement": 89,
    }

    def test_start_coins_reach_coin_star(self):
        self.collect_basement_access()
        self.assertTrue(self.can_reach_location("Shifting Sand Land - Coins Star"))


class ShiftingSandLandCoinStar93AccessTestBase(ShiftingSandLandCoinStarAccessTestBase):
    options = {
        **ShiftingSandLandCoinStarAccessTestBase.options,
        "shifting_sand_land_coin_star_requirement": 93,
    }

    def test_red_coin_star_coins_reach_coin_star(self):
        self.collect_basement_access()
        self.assertFalse(self.can_reach_location("Shifting Sand Land - Coins Star"))

        self.collect([
            self.get_item_by_name("Triple Jump"),
            self.get_item_by_name("Wing Cap"),
        ])
        self.assertTrue(self.can_reach_location("Shifting Sand Land - Free Flying for 8 Red Coins"))
        self.assertTrue(self.can_reach_location("Shifting Sand Land - Coins Star"))


class ShiftingSandLandCoinStar104AccessTestBase(ShiftingSandLandCoinStarAccessTestBase):
    options = {
        **ShiftingSandLandCoinStarAccessTestBase.options,
        "shifting_sand_land_coin_star_requirement": 104,
    }

    def test_ground_pound_coins_reach_coin_star(self):
        self.collect_basement_access()
        self.assertFalse(self.can_reach_location("Shifting Sand Land - Coins Star"))

        self.collect(self.get_item_by_name("Ground Pound"))
        self.assertTrue(self.can_reach_location("Shifting Sand Land - Coins Star"))


class ShiftingSandLandCoinStar117AccessTestBase(ShiftingSandLandCoinStarAccessTestBase):
    options = {
        **ShiftingSandLandCoinStarAccessTestBase.options,
        "shifting_sand_land_coin_star_requirement": 117,
    }

    def test_upper_pyramid_coins_reach_coin_star(self):
        self.collect_basement_access()
        self.assertFalse(self.can_reach_location("Shifting Sand Land - Coins Star"))

        self.collect(self.get_item_by_name("Shifting Sand Land - Pyramid Elevator"))
        self.assertTrue(self.can_reach_region("Shifting Sand Land - Upper Pyramid"))
        self.assertTrue(self.can_reach_location("Shifting Sand Land - Coins Star"))


class ShiftingSandLandCoinStar136AccessTestBase(ShiftingSandLandCoinStarAccessTestBase):
    options = {
        **ShiftingSandLandCoinStarAccessTestBase.options,
        "shifting_sand_land_coin_star_requirement": 136,
    }

    def test_all_coin_sources_reach_coin_star(self):
        self.collect_basement_access()
        self.collect([
            self.get_item_by_name("Ground Pound"),
            self.get_item_by_name("Shifting Sand Land - Pyramid Elevator"),
            self.get_item_by_name("Triple Jump"),
        ])
        self.assertFalse(self.can_reach_location("Shifting Sand Land - Coins Star"))

        self.collect(self.get_item_by_name("Wing Cap"))
        self.assertTrue(self.can_reach_location("Shifting Sand Land - Free Flying for 8 Red Coins"))
        self.assertTrue(self.can_reach_location("Shifting Sand Land - Coins Star"))


class SnowmansLandCoinStarAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_ARBITRARY_FEATURE_OPTIONS,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "buddy_checks": Options.BuddyChecks.option_true,
        "enable_locked_paintings": Options.EnableLockedPaintings.option_false,
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "area_rando": Options.AreaRandomizer.option_Off,
    }

    def collect_second_floor_access(self):
        self.collect(self.get_item_by_name("Progressive Upstairs Key"))


class SnowmansLandCoinStar102AccessTestBase(SnowmansLandCoinStarAccessTestBase):
    options = {
        **SnowmansLandCoinStarAccessTestBase.options,
        "snowmans_land_coin_star_requirement": 102,
    }

    def test_start_coins_reach_coin_star(self):
        self.collect_second_floor_access()
        self.assertTrue(self.can_reach_location("Snowman's Land - Coins Star"))


class SnowmansLandCoinStar104AccessTestBase(SnowmansLandCoinStarAccessTestBase):
    options = {
        **SnowmansLandCoinStarAccessTestBase.options,
        "snowmans_land_coin_star_requirement": 104,
    }

    def test_big_head_coins_reach_coin_star_without_cannon(self):
        self.collect_second_floor_access()
        self.collect(self.get_item_by_name("Backflip"))
        self.assertFalse(self.can_reach_location("Snowman's Land - Coins Star"))

        self.collect(self.get_item_by_name("Snowman's Land - Penguin"))
        self.assertTrue(self.can_reach_location("Snowman's Land - Snowman's Big Head"))
        self.assertTrue(self.can_reach_location("Snowman's Land - Coins Star"))


class SnowmansLandCoinStar105AccessTestBase(SnowmansLandCoinStarAccessTestBase):
    options = {
        **SnowmansLandCoinStarAccessTestBase.options,
        "snowmans_land_coin_star_requirement": 105,
    }

    def test_cannon_coins_reach_coin_star(self):
        self.collect_second_floor_access()
        self.assertFalse(self.can_reach_location("Snowman's Land - Coins Star"))

        self.collect(self.get_item_by_name("Snowman's Land - Cannon Unlock"))
        self.assertTrue(self.can_reach_location("Snowman's Land - Coins Star"))


class SnowmansLandCoinStar105NoDespawnsAccessTestBase(SnowmansLandCoinStarAccessTestBase):
    options = {
        **SnowmansLandCoinStarAccessTestBase.options,
        "snowmans_land_coin_star_requirement": 105,
        "no_despawns": Options.NoDespawns.option_true,
    }

    def test_no_despawns_coins_reach_coin_star_without_cannon(self):
        self.collect_second_floor_access()
        self.assertTrue(self.can_reach_location("Snowman's Land - Coins Star"))


class SnowmansLandCoinStar122AccessTestBase(SnowmansLandCoinStarAccessTestBase):
    options = {
        **SnowmansLandCoinStarAccessTestBase.options,
        "snowmans_land_coin_star_requirement": 122,
    }

    def test_igloo_coins_reach_coin_star(self):
        self.collect_second_floor_access()
        self.collect(self.get_item_by_name("Wall Kick"))
        self.assertFalse(self.can_reach_location("Snowman's Land - Coins Star"))

        self.collect(self.get_item_by_name("Vanish Cap"))
        self.assertTrue(self.can_reach_location("Snowman's Land - Into the Igloo"))
        self.assertTrue(self.can_reach_location("Snowman's Land - Coins Star"))


class SnowmansLandCoinStar127AccessTestBase(SnowmansLandCoinStarAccessTestBase):
    options = {
        **SnowmansLandCoinStarAccessTestBase.options,
        "snowmans_land_coin_star_requirement": 127,
    }

    def test_all_coin_sources_reach_coin_star(self):
        self.collect_second_floor_access()
        self.collect(self.get_item_by_name("Snowman's Land - Cannon Unlock"))
        self.assertTrue(self.can_reach_location("Snowman's Land - Snowman's Big Head"))
        self.assertFalse(self.can_reach_location("Snowman's Land - Coins Star"))

        self.collect([
            self.get_item_by_name("Vanish Cap"),
            self.get_item_by_name("Wall Kick"),
        ])
        self.assertTrue(self.can_reach_location("Snowman's Land - Into the Igloo"))
        self.assertTrue(self.can_reach_location("Snowman's Land - Coins Star"))


class WetDryWorldCoinStarAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_ARBITRARY_FEATURE_OPTIONS,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "enable_locked_paintings": Options.EnableLockedPaintings.option_false,
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "strict_move_requirements": Options.StrictMoveRequirements.option_true,
        "area_rando": Options.AreaRandomizer.option_Off,
    }

    def collect_second_floor_access(self):
        self.collect(self.get_item_by_name("Progressive Upstairs Key"))

    def disable_wdw_entrance(self, entrance_name: str):
        self.multiworld.get_entrance(f"Second Floor -> {entrance_name}", self.player).access_rule = \
            lambda state: False


class WetDryWorldCoinStar25AccessTestBase(WetDryWorldCoinStarAccessTestBase):
    options = {
        **WetDryWorldCoinStarAccessTestBase.options,
        "wet_dry_world_coin_star_requirement": 25,
    }

    def test_low_water_start_coins_reach_coin_star(self):
        self.disable_wdw_entrance("Wet-Dry World Middle")
        self.disable_wdw_entrance("Wet-Dry World High")
        self.collect_second_floor_access()
        self.assertTrue(self.can_reach_region("Wet-Dry World - Low Water"))
        self.assertTrue(self.can_reach_location("Wet-Dry World - Coins Star"))


class WetDryWorldCoinStar26AccessTestBase(WetDryWorldCoinStarAccessTestBase):
    options = {
        **WetDryWorldCoinStarAccessTestBase.options,
        "wet_dry_world_coin_star_requirement": 26,
    }

    def test_low_water_ground_pound_coins_reach_coin_star(self):
        self.disable_wdw_entrance("Wet-Dry World Middle")
        self.disable_wdw_entrance("Wet-Dry World High")
        self.collect_second_floor_access()
        self.assertFalse(self.can_reach_location("Wet-Dry World - Coins Star"))

        self.collect(self.get_item_by_name("Ground Pound"))
        self.assertTrue(self.can_reach_location("Wet-Dry World - Coins Star"))


class WetDryWorldCoinStar8AccessTestBase(WetDryWorldCoinStarAccessTestBase):
    options = {
        **WetDryWorldCoinStarAccessTestBase.options,
        "wet_dry_world_coin_star_requirement": 8,
    }

    def test_mid_water_start_coins_reach_coin_star(self):
        self.disable_wdw_entrance("Wet-Dry World Low")
        self.disable_wdw_entrance("Wet-Dry World High")
        self.collect_second_floor_access()
        self.assertTrue(self.can_reach_region("Wet-Dry World - Mid Water"))
        self.assertTrue(self.can_reach_location("Wet-Dry World - Coins Star"))


class WetDryWorldCoinStar9AccessTestBase(WetDryWorldCoinStarAccessTestBase):
    options = {
        **WetDryWorldCoinStarAccessTestBase.options,
        "wet_dry_world_coin_star_requirement": 9,
    }

    def test_mid_water_purple_switch_coins_reach_coin_star(self):
        self.disable_wdw_entrance("Wet-Dry World Low")
        self.disable_wdw_entrance("Wet-Dry World High")
        self.collect_second_floor_access()
        self.assertFalse(self.can_reach_location("Wet-Dry World - Coins Star"))

        self.collect(self.get_item_by_name("Purple Switches"))
        self.assertTrue(self.can_reach_location("Wet-Dry World - Coins Star"))


class WetDryWorldCoinStar65AccessTestBase(WetDryWorldCoinStarAccessTestBase):
    options = {
        **WetDryWorldCoinStarAccessTestBase.options,
        "wet_dry_world_coin_star_requirement": 65,
    }

    def test_highest_water_downtown_diamond_coins_reach_coin_star(self):
        self.disable_wdw_entrance("Wet-Dry World Low")
        self.disable_wdw_entrance("Wet-Dry World Middle")
        self.collect_second_floor_access()
        self.collect([
            self.get_item_by_name("Ledge Grab"),
            self.get_item_by_name("Triple Jump"),
        ])
        self.assertTrue(self.can_reach_region("Wet-Dry World - Highest Water"))
        self.assertTrue(self.can_reach_region("Wet-Dry World - Downtown"))
        self.assertFalse(self.can_reach_location("Wet-Dry World - Coins Star"))

        self.collect(self.get_item_by_name("Wet-Dry World - Water Level Diamond"))
        self.assertTrue(self.can_reach_location("Wet-Dry World - Coins Star"))


class WetDryWorldCoinStar152AccessTestBase(WetDryWorldCoinStarAccessTestBase):
    options = {
        **WetDryWorldCoinStarAccessTestBase.options,
        "wet_dry_world_coin_star_requirement": 152,
    }

    def test_high_variant_diamond_route_reaches_all_coins(self):
        self.disable_wdw_entrance("Wet-Dry World Low")
        self.disable_wdw_entrance("Wet-Dry World Middle")
        self.collect_second_floor_access()
        self.collect([
            self.get_item_by_name("Ledge Grab"),
            self.get_item_by_name("Triple Jump"),
            self.get_item_by_name("Ground Pound"),
            self.get_item_by_name("Purple Switches"),
        ])
        self.assertFalse(self.can_reach_location("Wet-Dry World - Coins Star"))

        self.collect(self.get_item_by_name("Wet-Dry World - Water Level Diamond"))
        self.assertTrue(self.can_reach_location("Wet-Dry World - Coins Star"))


class TallTallMountainCoinStarAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_ARBITRARY_FEATURE_OPTIONS,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "buddy_checks": Options.BuddyChecks.option_true,
        "enable_locked_paintings": Options.EnableLockedPaintings.option_false,
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "area_rando": Options.AreaRandomizer.option_Off,
    }

    def collect_second_floor_access(self):
        self.collect(self.get_item_by_name("Progressive Upstairs Key"))


class TallTallMountainCoinStar16AccessTestBase(TallTallMountainCoinStarAccessTestBase):
    options = {
        **TallTallMountainCoinStarAccessTestBase.options,
        "tall_tall_mountain_coin_star_requirement": 16,
    }

    def test_coins_above_start_require_middle_region(self):
        self.multiworld.get_entrance("Tall, Tall Mountain - Middle", self.player).access_rule = \
            lambda state: False
        self.collect_second_floor_access()
        self.assertTrue(self.can_reach_region("Tall, Tall Mountain"))
        self.assertFalse(self.can_reach_region("Tall, Tall Mountain - Middle"))
        self.assertFalse(self.can_reach_location("Tall, Tall Mountain - Coins Star"))


class TallTallMountainCoinStar70AccessTestBase(TallTallMountainCoinStarAccessTestBase):
    options = {
        **TallTallMountainCoinStarAccessTestBase.options,
        "tall_tall_mountain_coin_star_requirement": 70,
    }

    def test_start_coins_reach_coin_star(self):
        self.collect_second_floor_access()
        self.assertTrue(self.can_reach_region("Tall, Tall Mountain - Middle"))
        self.assertTrue(self.can_reach_location("Tall, Tall Mountain - Coins Star"))


class TallTallMountainCoinStar75AccessTestBase(TallTallMountainCoinStarAccessTestBase):
    options = {
        **TallTallMountainCoinStarAccessTestBase.options,
        "tall_tall_mountain_coin_star_requirement": 75,
    }

    def test_climb_coins_reach_coin_star(self):
        self.collect_second_floor_access()
        self.assertFalse(self.can_reach_location("Tall, Tall Mountain - Coins Star"))

        self.collect(self.get_item_by_name("Climb"))
        self.assertTrue(self.can_reach_location("Tall, Tall Mountain - Coins Star"))


class TallTallMountainCoinStar75MovelessAccessTestBase(TallTallMountainCoinStarAccessTestBase):
    options = {
        **TallTallMountainCoinStarAccessTestBase.options,
        "strict_move_requirements": Options.StrictMoveRequirements.option_false,
        "tall_tall_mountain_coin_star_requirement": 75,
    }

    def test_moveless_coins_reach_coin_star(self):
        self.collect_second_floor_access()
        self.assertTrue(self.can_reach_location("Tall, Tall Mountain - Coins Star"))


class TallTallMountainCoinStar129AccessTestBase(TallTallMountainCoinStarAccessTestBase):
    options = {
        **TallTallMountainCoinStarAccessTestBase.options,
        "tall_tall_mountain_coin_star_requirement": 129,
    }

    def test_top_coins_reach_coin_star(self):
        self.collect_second_floor_access()
        self.assertFalse(self.can_reach_location("Tall, Tall Mountain - Coins Star"))

        self.collect([
            self.get_item_by_name("Long Jump"),
            self.get_item_by_name("Ledge Grab"),
        ])
        self.assertTrue(self.can_reach_region("Tall, Tall Mountain - Top"))
        self.assertTrue(self.can_reach_location("Tall, Tall Mountain - Coins Star"))


class TallTallMountainCoinStar131AccessTestBase(TallTallMountainCoinStarAccessTestBase):
    options = {
        **TallTallMountainCoinStarAccessTestBase.options,
        "tall_tall_mountain_coin_star_requirement": 131,
    }

    def test_top_backflip_coins_reach_coin_star(self):
        self.collect_second_floor_access()
        self.collect([
            self.get_item_by_name("Long Jump"),
            self.get_item_by_name("Ledge Grab"),
        ])
        self.assertTrue(self.can_reach_region("Tall, Tall Mountain - Top"))
        self.assertFalse(self.can_reach_location("Tall, Tall Mountain - Coins Star"))

        self.collect(self.get_item_by_name("Backflip"))
        self.assertTrue(self.can_reach_location("Tall, Tall Mountain - Coins Star"))


class TallTallMountainCoinStar137AccessTestBase(TallTallMountainCoinStarAccessTestBase):
    options = {
        **TallTallMountainCoinStarAccessTestBase.options,
        "tall_tall_mountain_coin_star_requirement": 137,
    }

    def test_all_coin_sources_reach_coin_star(self):
        self.collect_second_floor_access()
        self.collect([
            self.get_item_by_name("Climb"),
            self.get_item_by_name("Long Jump"),
            self.get_item_by_name("Ledge Grab"),
            self.get_item_by_name("Backflip"),
        ])
        self.assertTrue(self.can_reach_region("Tall, Tall Mountain - Top"))
        self.assertFalse(self.can_reach_location("Tall, Tall Mountain - Coins Star"))

        self.collect(self.get_item_by_name("Purple Switches"))
        self.assertTrue(self.can_reach_location("Tall, Tall Mountain - Coins Star"))


class BigBooHauntAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        "enable_locked_paintings": Options.EnableLockedPaintings.option_false,
        "logic_tricks": {
            "Big Boo's Haunt Second Floor with Triple Jump and Wall Kick",
            "Big Boo's Haunt Third Floor with Side Flip",
            "Big Boo's Haunt Roof without Long Jump",
        },
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "area_rando": Options.AreaRandomizer.option_Off,
    }

    def collect_bbh_access(self):
        self.collect(self.get_item_by_name("Unlock Big Boo's Haunt"))

    def test_second_floor_access_with_staircase(self):
        self.collect_bbh_access()
        self.assertFalse(self.can_reach_region("Big Boo's Haunt - Second Floor"))
        self.collect(self.get_item_by_name("Big Boo's Haunt - Staircase"))
        self.assertTrue(self.can_reach_region("Big Boo's Haunt - Second Floor"))

    def test_second_floor_access_with_movement(self):
        self.collect_bbh_access()
        self.collect(self.get_item_by_name("Wall Kick"))
        self.assertFalse(self.can_reach_region("Big Boo's Haunt - Second Floor"))
        self.collect(self.get_item_by_name("Triple Jump"))
        self.assertTrue(self.can_reach_region("Big Boo's Haunt - Second Floor"))

    def test_secret_books_requires_second_floor(self):
        self.collect_bbh_access()
        self.collect(self.get_item_by_name("Kick"))
        self.assertFalse(self.can_reach_location("Big Boo's Haunt - Secret of the Haunted Books"))
        self.collect(self.get_item_by_name("Big Boo's Haunt - Staircase"))
        self.assertTrue(self.can_reach_location("Big Boo's Haunt - Secret of the Haunted Books"))

    def test_third_floor_inherits_second_floor_access(self):
        self.collect_bbh_access()
        self.collect([self.get_item_by_name("Wall Kick"), self.get_item_by_name("Ledge Grab")])
        self.assertFalse(self.can_reach_region("Big Boo's Haunt - Third Floor"))
        self.collect(self.get_item_by_name("Big Boo's Haunt - Staircase"))
        self.assertTrue(self.can_reach_region("Big Boo's Haunt - Third Floor"))

    def test_third_floor_side_flip_trick(self):
        self.collect_bbh_access()
        self.collect(self.get_item_by_name("Big Boo's Haunt - Staircase"))
        self.assertFalse(self.can_reach_region("Big Boo's Haunt - Third Floor"))
        self.collect(self.get_item_by_name("Side Flip"))
        self.assertTrue(self.can_reach_region("Big Boo's Haunt - Third Floor"))

    def test_roof_without_long_jump_trick(self):
        self.collect_bbh_access()
        self.collect([
            self.get_item_by_name("Big Boo's Haunt - Staircase"),
            self.get_item_by_name("Wall Kick"),
            self.get_item_by_name("Ledge Grab"),
        ])
        self.assertTrue(self.can_reach_region("Big Boo's Haunt - Roof"))


class BigBooHauntCoinStarAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "enable_locked_paintings": Options.EnableLockedPaintings.option_false,
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "area_rando": Options.AreaRandomizer.option_Off,
    }

    def collect_bbh_access(self):
        self.collect(self.get_item_by_name("Unlock Big Boo's Haunt"))


class BigBooHauntCoinStar78AccessTestBase(BigBooHauntCoinStarAccessTestBase):
    options = {
        **BigBooHauntCoinStarAccessTestBase.options,
        "big_boos_haunt_coin_star_requirement": 78,
    }

    def test_start_coins_reach_coin_star(self):
        self.collect_bbh_access()
        self.assertTrue(self.can_reach_location("Big Boo's Haunt - Coins Star"))


class BigBooHauntCoinStar79AccessTestBase(BigBooHauntCoinStarAccessTestBase):
    options = {
        **BigBooHauntCoinStarAccessTestBase.options,
        "big_boos_haunt_coin_star_requirement": 79,
    }

    def test_second_floor_coins_reach_coin_star(self):
        self.collect_bbh_access()
        self.assertFalse(self.can_reach_location("Big Boo's Haunt - Coins Star"))
        self.collect(self.get_item_by_name("Big Boo's Haunt - Staircase"))
        self.assertTrue(self.can_reach_region("Big Boo's Haunt - Second Floor"))
        self.assertTrue(self.can_reach_location("Big Boo's Haunt - Coins Star"))


class BigBooHauntCoinStar102AccessTestBase(BigBooHauntCoinStarAccessTestBase):
    options = {
        **BigBooHauntCoinStarAccessTestBase.options,
        "big_boos_haunt_coin_star_requirement": 102,
    }

    def test_third_floor_coins_reach_coin_star(self):
        self.collect_bbh_access()
        self.collect(self.get_item_by_name("Big Boo's Haunt - Staircase"))
        self.assertFalse(self.can_reach_location("Big Boo's Haunt - Coins Star"))
        self.collect([
            self.get_item_by_name("Wall Kick"),
            self.get_item_by_name("Ledge Grab"),
        ])
        self.assertTrue(self.can_reach_region("Big Boo's Haunt - Third Floor"))
        self.assertTrue(self.can_reach_location("Big Boo's Haunt - Coins Star"))


class BigBooHauntCoinStar103AccessTestBase(BigBooHauntCoinStarAccessTestBase):
    options = {
        **BigBooHauntCoinStarAccessTestBase.options,
        "big_boos_haunt_coin_star_requirement": 103,
    }

    def test_merry_go_round_coins_reach_coin_star(self):
        self.collect_bbh_access()
        self.assertFalse(self.can_reach_location("Big Boo's Haunt - Coins Star"))
        self.collect(self.get_item_by_name("Big Boo's Haunt - Merry-go-round"))
        self.assertTrue(self.can_reach_location("Big Boo's Haunt - Ride Big Boo's Merry-Go-Round"))
        self.assertTrue(self.can_reach_location("Big Boo's Haunt - Coins Star"))


class BigBooHauntCoinStar126AccessTestBase(BigBooHauntCoinStarAccessTestBase):
    options = {
        **BigBooHauntCoinStarAccessTestBase.options,
        "big_boos_haunt_coin_star_requirement": 126,
    }

    def test_third_floor_ground_pound_coins_reach_coin_star(self):
        self.collect_bbh_access()
        self.collect([
            self.get_item_by_name("Big Boo's Haunt - Staircase"),
            self.get_item_by_name("Wall Kick"),
            self.get_item_by_name("Ledge Grab"),
        ])
        self.assertFalse(self.can_reach_location("Big Boo's Haunt - Coins Star"))
        self.collect(self.get_item_by_name("Ground Pound"))
        self.assertTrue(self.can_reach_location("Big Boo's Haunt - Coins Star"))


class BigBooHauntCoinStar151AccessTestBase(BigBooHauntCoinStarAccessTestBase):
    options = {
        **BigBooHauntCoinStarAccessTestBase.options,
        "big_boos_haunt_coin_star_requirement": 151,
    }

    def test_all_coin_sources_reach_coin_star(self):
        self.collect_bbh_access()
        self.collect([
            self.get_item_by_name("Big Boo's Haunt - Staircase"),
            self.get_item_by_name("Wall Kick"),
            self.get_item_by_name("Ledge Grab"),
            self.get_item_by_name("Ground Pound"),
        ])
        self.assertFalse(self.can_reach_location("Big Boo's Haunt - Coins Star"))
        self.collect(self.get_item_by_name("Big Boo's Haunt - Merry-go-round"))
        self.assertTrue(self.can_reach_location("Big Boo's Haunt - Coins Star"))


class WetDryWorldVariantAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_ARBITRARY_FEATURE_OPTIONS,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "enable_locked_paintings": Options.EnableLockedPaintings.option_false,
        "one_up_checks": Options.OneUpChecks.option_true,
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "area_rando": Options.AreaRandomizer.option_Off,
    }

    def collect_second_floor_access(self):
        self.collect(self.get_item_by_name("Progressive Upstairs Key"))

    def disable_wdw_entrance(self, entrance_name: str):
        self.multiworld.get_entrance(f"Second Floor -> {entrance_name}", self.player).access_rule = \
            lambda state: False

    def test_high_entrance_requires_ledge_grab_and_jump(self):
        self.collect_second_floor_access()
        self.assertTrue(self.can_reach_region("Wet-Dry World"))
        self.assertFalse(self.can_reach_region("Wet-Dry World High"))

        self.collect(self.get_item_by_name("Ledge Grab"))
        self.assertFalse(self.can_reach_region("Wet-Dry World High"))

        self.collect(self.get_item_by_name("Side Flip"))
        self.assertTrue(self.can_reach_region("Wet-Dry World High"))

    def test_downtown_requires_high_entrance_without_cannon(self):
        self.collect_second_floor_access()
        self.multiworld.get_entrance("Second Floor -> Wet-Dry World High", self.player).access_rule = \
            lambda state: True
        self.assertFalse(self.can_reach_region("Wet-Dry World - Downtown"))

        self.collect(self.get_item_by_name("Triple Jump"))
        self.assertTrue(self.can_reach_region("Wet-Dry World - Highest Water"))
        self.assertFalse(self.can_reach_region("Wet-Dry World - Downtown"))

        self.collect(self.get_item_by_name("Ledge Grab"))
        self.assertTrue(self.can_reach_region("Wet-Dry World - Downtown"))

    def test_downtown_checks_require_water_level_diamond(self):
        self.collect_second_floor_access()
        self.collect([
            self.get_item_by_name("Ledge Grab"),
            self.get_item_by_name("Triple Jump"),
            self.get_item_by_name("Wall Kick"),
        ])
        self.assertTrue(self.can_reach_region("Wet-Dry World - Downtown"))
        self.assertFalse(self.can_reach_location("Wet-Dry World - Go to Town for Red Coins"))
        self.assertFalse(self.can_reach_location("Wet-Dry World - Downtown Block 1-Up"))

        self.collect(self.get_item_by_name("Wet-Dry World - Water Level Diamond"))
        self.assertTrue(self.can_reach_location("Wet-Dry World - Go to Town for Red Coins"))
        self.assertTrue(self.can_reach_location("Wet-Dry World - Downtown Block 1-Up"))

    def test_low_water_can_raise_to_high_but_not_highest(self):
        self.disable_wdw_entrance("Wet-Dry World Middle")
        self.disable_wdw_entrance("Wet-Dry World High")
        self.collect_second_floor_access()
        self.assertTrue(self.can_reach_region("Wet-Dry World - Low Water"))
        self.assertFalse(self.can_reach_region("Wet-Dry World - Mid Water"))
        self.assertTrue(self.can_reach_region("Wet-Dry World - Cannon"))
        self.assertTrue(self.can_reach_location("Wet-Dry World - Shocking Arrow Lifts!"))
        self.assertFalse(self.can_reach_location("Wet-Dry World - Secrets in the Shallows & Sky"))

        self.collect(self.get_item_by_name("Wet-Dry World - Water Level Diamond"))
        self.assertTrue(self.can_reach_region("Wet-Dry World - Mid Water"))
        self.assertFalse(self.can_reach_region("Wet-Dry World - Mid-High Water"))
        self.assertFalse(self.can_reach_location("Wet-Dry World - Express Elevator--Hurry Up!"))
        self.assertFalse(self.can_reach_location("Wet-Dry World - Secrets in the Shallows & Sky"))

        self.collect(self.get_item_by_name("Purple Switches"))
        self.assertTrue(self.can_reach_region("Wet-Dry World - Top of the Express Elevator"))
        self.assertTrue(self.can_reach_region("Wet-Dry World - Mid-High Water"))
        self.assertFalse(self.can_reach_region("Wet-Dry World - Top"))
        self.assertTrue(self.can_reach_location("Wet-Dry World - Express Elevator--Hurry Up!"))
        self.assertTrue(self.can_reach_location("Wet-Dry World - Secrets in the Shallows & Sky"))

        self.collect([
            self.get_item_by_name("Long Jump"),
        ])
        self.assertTrue(self.can_reach_region("Wet-Dry World - Mid-High Water"))
        self.assertTrue(self.can_reach_region("Wet-Dry World - Top"))
        self.assertTrue(self.can_reach_region("Wet-Dry World - High Water"))
        self.assertFalse(self.can_reach_region("Wet-Dry World - Highest Water"))

    def test_middle_water_to_mid_high_accepts_triple_jump_and_dive(self):
        self.disable_wdw_entrance("Wet-Dry World Low")
        self.disable_wdw_entrance("Wet-Dry World High")
        self.collect_second_floor_access()
        self.collect(self.get_item_by_name("Wet-Dry World - Water Level Diamond"))
        self.assertTrue(self.can_reach_region("Wet-Dry World - Mid Water"))
        self.assertFalse(self.can_reach_region("Wet-Dry World - Mid-High Water"))

        self.collect([self.get_item_by_name("Triple Jump"), self.get_item_by_name("Dive")])
        self.assertTrue(self.can_reach_region("Wet-Dry World - Mid-High Water"))

    def test_middle_water_to_mid_high_accepts_top_of_express_elevator(self):
        self.disable_wdw_entrance("Wet-Dry World Low")
        self.disable_wdw_entrance("Wet-Dry World High")
        self.collect_second_floor_access()
        self.collect([
            self.get_item_by_name("Wet-Dry World - Water Level Diamond"),
            self.get_item_by_name("Purple Switches"),
        ])
        self.assertTrue(self.can_reach_region("Wet-Dry World - Top of the Express Elevator"))
        self.assertTrue(self.can_reach_region("Wet-Dry World - Mid-High Water"))

    def test_highest_water_lowers_with_diamond(self):
        self.disable_wdw_entrance("Wet-Dry World Low")
        self.disable_wdw_entrance("Wet-Dry World Middle")
        self.collect_second_floor_access()
        self.collect([self.get_item_by_name("Ledge Grab"), self.get_item_by_name("Triple Jump")])
        self.assertTrue(self.can_reach_region("Wet-Dry World - Highest Water"))
        self.assertFalse(self.can_reach_region("Wet-Dry World - High Water"))

        self.collect(self.get_item_by_name("Wet-Dry World - Water Level Diamond"))
        self.assertTrue(self.can_reach_region("Wet-Dry World - High Water"))
        self.assertTrue(self.can_reach_region("Wet-Dry World - Mid-High Water"))

    def test_bob_omb_buddy_uses_high_or_highest_water_routes(self):
        self.disable_wdw_entrance("Wet-Dry World Low")
        self.disable_wdw_entrance("Wet-Dry World Middle")
        self.collect_second_floor_access()
        self.collect([self.get_item_by_name("Ledge Grab"), self.get_item_by_name("Triple Jump")])
        self.assertTrue(self.can_reach_region("Wet-Dry World - Highest Water"))
        self.assertFalse(self.can_reach_location("Wet-Dry World - Bob-omb Buddy"))

        self.collect(self.get_item_by_name("Backflip"))
        self.assertTrue(self.can_reach_location("Wet-Dry World - Bob-omb Buddy"))

    def test_bob_omb_buddy_high_water_requires_jump_route(self):
        self.disable_wdw_entrance("Wet-Dry World Middle")
        self.disable_wdw_entrance("Wet-Dry World High")
        self.collect_second_floor_access()
        self.collect([
            self.get_item_by_name("Wet-Dry World - Water Level Diamond"),
            self.get_item_by_name("Purple Switches"),
            self.get_item_by_name("Long Jump"),
        ])
        self.assertTrue(self.can_reach_region("Wet-Dry World - High Water"))
        self.assertFalse(self.can_reach_location("Wet-Dry World - Bob-omb Buddy"))

        self.collect(self.get_item_by_name("Side Flip"))
        self.assertFalse(self.can_reach_location("Wet-Dry World - Bob-omb Buddy"))

        self.collect(self.get_item_by_name("Ledge Grab"))
        self.assertTrue(self.can_reach_location("Wet-Dry World - Bob-omb Buddy"))

    def test_top_accepts_purple_switch_and_long_jump(self):
        self.collect_second_floor_access()
        self.assertFalse(self.can_reach_region("Wet-Dry World - Top"))
        self.assertFalse(self.can_reach_region("Wet-Dry World - Top of the Express Elevator"))

        self.collect(self.get_item_by_name("Purple Switches"))
        self.assertTrue(self.can_reach_region("Wet-Dry World - Top of the Express Elevator"))
        self.assertFalse(self.can_reach_region("Wet-Dry World - Top"))

        self.collect(self.get_item_by_name("Long Jump"))
        self.assertTrue(self.can_reach_region("Wet-Dry World - Top"))

    def test_top_of_express_elevator_accepts_top_platform_drop_route(self):
        self.collect_second_floor_access()
        self.collect(self.get_item_by_name("Wall Kick"))
        self.assertTrue(self.can_reach_region("Wet-Dry World - Top"))
        self.assertFalse(self.can_reach_region("Wet-Dry World - Top of the Express Elevator"))

        self.collect(self.get_item_by_name("Ledge Grab"))
        self.assertTrue(self.can_reach_region("Wet-Dry World - Top of the Express Elevator"))

    def test_express_elevator_top_route_needs_elevator_access_method(self):
        self.disable_wdw_entrance("Wet-Dry World Middle")
        self.disable_wdw_entrance("Wet-Dry World High")
        self.collect_second_floor_access()
        self.collect(self.get_item_by_name("Triple Jump"))
        self.assertTrue(self.can_reach_region("Wet-Dry World - Top of the Express Elevator"))
        self.assertTrue(self.can_reach_region("Wet-Dry World - Top"))
        self.assertFalse(self.can_reach_location("Wet-Dry World - Express Elevator--Hurry Up!"))

        self.collect(self.get_item_by_name("Backflip"))
        self.assertTrue(self.can_reach_location("Wet-Dry World - Express Elevator--Hurry Up!"))

    def test_secrets_requires_top_of_express_elevator(self):
        self.disable_wdw_entrance("Wet-Dry World Middle")
        self.disable_wdw_entrance("Wet-Dry World High")
        self.collect_second_floor_access()
        self.collect(self.get_item_by_name("Wet-Dry World - Water Level Diamond"))
        self.assertFalse(self.can_reach_location("Wet-Dry World - Express Elevator--Hurry Up!"))
        self.assertFalse(self.can_reach_region("Wet-Dry World - Top of the Express Elevator"))
        self.assertFalse(self.can_reach_location("Wet-Dry World - Secrets in the Shallows & Sky"))

        self.collect(self.get_item_by_name("Purple Switches"))
        self.assertTrue(self.can_reach_region("Wet-Dry World - Top of the Express Elevator"))
        self.assertTrue(self.can_reach_location("Wet-Dry World - Express Elevator--Hurry Up!"))
        self.assertTrue(self.can_reach_location("Wet-Dry World - Secrets in the Shallows & Sky"))

    def test_secrets_accepts_top_of_express_elevator_and_long_jump(self):
        self.disable_wdw_entrance("Wet-Dry World Middle")
        self.disable_wdw_entrance("Wet-Dry World High")
        self.collect_second_floor_access()
        self.collect(self.get_item_by_name("Purple Switches"))
        self.assertTrue(self.can_reach_region("Wet-Dry World - Top of the Express Elevator"))
        self.assertFalse(self.can_reach_location("Wet-Dry World - Secrets in the Shallows & Sky"))

        self.collect(self.get_item_by_name("Long Jump"))
        self.assertTrue(self.can_reach_location("Wet-Dry World - Secrets in the Shallows & Sky"))


class NoStrictMoveWetDryWorldAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_ARBITRARY_FEATURE_OPTIONS,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "enable_locked_paintings": Options.EnableLockedPaintings.option_false,
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "strict_move_requirements": Options.StrictMoveRequirements.option_false,
        "area_rando": Options.AreaRandomizer.option_Off,
    }

    def test_quick_race_accepts_moveless_jump_and_kick_route(self):
        self.collect(self.get_item_by_name("Progressive Upstairs Key"))
        self.collect([
            self.get_item_by_name("Ledge Grab"),
            self.get_item_by_name("Side Flip"),
        ])
        self.assertTrue(self.can_reach_region("Wet-Dry World - Downtown"))
        self.assertFalse(self.can_reach_location("Wet-Dry World - Quick Race Through Downtown!"))

        self.collect(self.get_item_by_name("Kick"))
        self.assertFalse(self.can_reach_location("Wet-Dry World - Quick Race Through Downtown!"))

        self.collect(self.get_item_by_name("Wet-Dry World - Water Level Diamond"))
        self.assertTrue(self.can_reach_location("Wet-Dry World - Quick Race Through Downtown!"))

    def test_top_of_express_elevator_accepts_no_movement_jump(self):
        self.collect(self.get_item_by_name("Progressive Upstairs Key"))
        self.assertTrue(self.can_reach_region("Wet-Dry World - Top of the Express Elevator"))


class NoStrictMoveCapLethalLavaLandAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_ARBITRARY_FEATURE_OPTIONS,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "enable_locked_paintings": Options.EnableLockedPaintings.option_false,
        "strict_move_requirements": Options.StrictMoveRequirements.option_false,
        "strict_cap_requirements": Options.StrictCapRequirements.option_false,
        "area_rando": Options.AreaRandomizer.option_Off,
    }

    def test_log_rolling_accepts_moveless_capless(self):
        self.collect(self.get_item_by_name("Progressive Basement Key"))
        self.assertTrue(self.can_reach_location("Lethal Lava Land - Red-Hot Log Rolling"))


class GlobalCapAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_ARBITRARY_FEATURE_OPTIONS,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "enable_locked_paintings": Options.EnableLockedPaintings.option_false,
        "buddy_checks": Options.BuddyChecks.option_true,
        "one_up_checks": Options.OneUpChecks.option_true,
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "area_rando": Options.AreaRandomizer.option_Off,
    }

    def test_bob_wing_cap_access(self):
        self.collect(self.get_item_by_name("Bob-omb Battlefield - Bob-omb Buddy"))
        self.collect(self.get_item_by_name("Bob-omb Battlefield - Cannon Unlock"))
        self.assertFalse(self.can_reach_location("Bob-omb Battlefield - Mario Wings to the Sky"))
        self.collect(self.world.create_item("Bob-omb Battlefield - Wing Cap"))
        self.assertFalse(self.can_reach_location("Bob-omb Battlefield - Mario Wings to the Sky"))
        self.collect(self.get_item_by_name("Wing Cap"))
        self.assertTrue(self.can_reach_location("Bob-omb Battlefield - Mario Wings to the Sky"))

    def test_lll_wing_cap_route_requires_triple_jump(self):
        self.collect(self.get_item_by_name("Progressive Basement Key"))
        self.collect(self.get_item_by_name("Wing Cap"))
        self.assertFalse(self.can_reach_location("Lethal Lava Land - Red-Hot Log Rolling"))

        self.collect(self.get_item_by_name("Triple Jump"))
        self.assertTrue(self.can_reach_location("Lethal Lava Land - Red-Hot Log Rolling"))

    def test_wmotr_red_coins_require_cannon(self):
        self.collect([self.get_item_by_name("Progressive Upstairs Key")] * 3)
        self.collect([
            self.get_item_by_name("Wing Cap"),
            self.get_item_by_name("Triple Jump"),
        ])
        self.assertFalse(self.can_reach_location("Wing Mario Over the Rainbow - Red Coins"))

        self.collect(self.get_item_by_name("Wing Mario Over the Rainbow - Cannon Unlock"))
        self.assertTrue(self.can_reach_location("Wing Mario Over the Rainbow - Red Coins"))

    def test_wmotr_red_coins_cannon_route_accepts_capless_long_jump(self):
        self.collect([self.get_item_by_name("Progressive Upstairs Key")] * 3)
        self.collect([
            self.get_item_by_name("Wing Cap"),
            self.get_item_by_name("Side Flip"),
        ])
        self.assertFalse(self.can_reach_location("Wing Mario Over the Rainbow - Red Coins"))

        self.collect(self.get_item_by_name("Wing Mario Over the Rainbow - Cannon Unlock"))
        self.assertFalse(self.can_reach_location("Wing Mario Over the Rainbow - Red Coins"))

        self.collect(self.get_item_by_name("Long Jump"))
        self.collect(self.world.create_item("ut_glitch"))
        self.assertTrue(self.can_reach_location("Wing Mario Over the Rainbow - Red Coins"))

    def test_wmotr_buddy_wing_cap_route_accepts_triple_jump(self):
        self.collect([self.get_item_by_name("Progressive Upstairs Key")] * 3)
        self.collect(self.get_item_by_name("Wing Cap"))
        self.assertFalse(self.can_reach_location("Wing Mario Over the Rainbow - Bob-omb Buddy"))

        self.collect(self.get_item_by_name("Triple Jump"))
        self.assertTrue(self.can_reach_location("Wing Mario Over the Rainbow - Bob-omb Buddy"))

    def test_wmotr_buddy_wing_cap_route_rejects_cannon_without_platform_movement(self):
        self.collect([self.get_item_by_name("Progressive Upstairs Key")] * 3)
        self.collect([
            self.get_item_by_name("Wing Cap"),
            self.get_item_by_name("Side Flip"),
        ])
        self.assertFalse(self.can_reach_location("Wing Mario Over the Rainbow - Bob-omb Buddy"))

        self.collect(self.get_item_by_name("Wing Mario Over the Rainbow - Cannon Unlock"))
        self.assertFalse(self.can_reach_location("Wing Mario Over the Rainbow - Bob-omb Buddy"))

    def test_wmotr_cloud_wing_cap_route_accepts_triple_jump(self):
        self.collect([self.get_item_by_name("Progressive Upstairs Key")] * 3)
        self.collect(self.get_item_by_name("Wing Cap"))
        self.assertFalse(self.can_reach_location("Wing Mario Over the Rainbow - Cloud 1-Up"))

        self.collect(self.get_item_by_name("Triple Jump"))
        self.assertTrue(self.can_reach_location("Wing Mario Over the Rainbow - Cloud 1-Up"))

    def test_wmotr_cloud_wing_cap_route_accepts_cannon(self):
        self.collect([self.get_item_by_name("Progressive Upstairs Key")] * 3)
        self.collect([
            self.get_item_by_name("Wing Cap"),
            self.get_item_by_name("Long Jump"),
            self.get_item_by_name("Side Flip"),
            self.world.create_item("ut_glitch"),
        ])
        self.assertFalse(self.can_reach_location("Wing Mario Over the Rainbow - Cloud 1-Up"))

        self.collect(self.get_item_by_name("Wing Mario Over the Rainbow - Cannon Unlock"))
        self.assertTrue(self.can_reach_location("Wing Mario Over the Rainbow - Cloud 1-Up"))

    def test_wmotr_hanging_pole_requires_cannon(self):
        self.collect([self.get_item_by_name("Progressive Upstairs Key")] * 3)
        self.collect([
            self.get_item_by_name("Wing Cap"),
            self.get_item_by_name("Triple Jump"),
        ])
        self.assertFalse(self.can_reach_location("Wing Mario Over the Rainbow - Hanging Pole 1-Up"))

        self.collect(self.get_item_by_name("Wing Mario Over the Rainbow - Cannon Unlock"))
        self.assertTrue(self.can_reach_location("Wing Mario Over the Rainbow - Hanging Pole 1-Up"))


class PerLevelCapAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_ARBITRARY_FEATURE_OPTIONS,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "buddy_checks": Options.BuddyChecks.option_true,
        "enable_locked_paintings": Options.EnableLockedPaintings.option_false,
        "one_up_checks": Options.OneUpChecks.option_true,
        "area_rando": Options.AreaRandomizer.option_Off,
        "per_level_cap_items": Options.PerLevelCapItems.option_true,
    }

    def test_bob_wing_cap_access(self):
        self.collect(self.get_item_by_name("Bob-omb Battlefield - Bob-omb Buddy"))
        self.collect(self.get_item_by_name("Bob-omb Battlefield - Cannon Unlock"))
        self.assertFalse(self.can_reach_location("Bob-omb Battlefield - Mario Wings to the Sky"))
        self.collect(self.world.create_item("Wing Cap"))
        self.assertFalse(self.can_reach_location("Bob-omb Battlefield - Mario Wings to the Sky"))
        self.collect(self.get_item_by_name("Bob-omb Battlefield - Wing Cap"))
        self.assertTrue(self.can_reach_location("Bob-omb Battlefield - Mario Wings to the Sky"))

    def test_tower_wing_cap_access(self):
        self.collect(self.get_item_by_name("Unlock Tower of the Wing Cap"))
        self.assertTrue(self.can_reach_location("Tower of the Wing Cap - Red Coins"))

    def test_wmotr_wing_cap_access(self):
        self.collect([self.get_item_by_name("Progressive Upstairs Key")] * 3)
        self.assertFalse(self.can_reach_location("Wing Mario Over the Rainbow - Red Coins"))
        self.collect(self.get_item_by_name("Wing Mario Over the Rainbow - Cannon Unlock"))
        self.assertFalse(self.can_reach_location("Wing Mario Over the Rainbow - Red Coins"))
        self.collect(self.world.create_item("Wing Cap"))
        self.assertFalse(self.can_reach_location("Wing Mario Over the Rainbow - Red Coins"))
        self.collect(self.get_item_by_name("Castle - Wing Cap"))
        self.assertFalse(self.can_reach_location("Wing Mario Over the Rainbow - Red Coins"))
        self.collect(self.get_item_by_name("Wing Mario Over the Rainbow - Wing Cap"))
        self.assertTrue(self.can_reach_location("Wing Mario Over the Rainbow - Red Coins"))

    def test_wmotr_bob_omb_buddy_accepts_wing_cap(self):
        self.collect([self.get_item_by_name("Progressive Upstairs Key")] * 3)
        self.assertFalse(self.can_reach_location("Wing Mario Over the Rainbow - Bob-omb Buddy"))
        self.collect(self.get_item_by_name("Wing Mario Over the Rainbow - Wing Cap"))
        self.assertTrue(self.can_reach_location("Wing Mario Over the Rainbow - Bob-omb Buddy"))

    def test_wmotr_cloud_and_hanging_pole_access(self):
        self.collect([self.get_item_by_name("Progressive Upstairs Key")] * 3)
        self.assertFalse(self.can_reach_location("Wing Mario Over the Rainbow - Cloud 1-Up"))
        self.assertFalse(self.can_reach_location("Wing Mario Over the Rainbow - Hanging Pole 1-Up"))
        self.collect(self.get_item_by_name("Wing Mario Over the Rainbow - Wing Cap"))
        self.assertTrue(self.can_reach_location("Wing Mario Over the Rainbow - Cloud 1-Up"))
        self.assertFalse(self.can_reach_location("Wing Mario Over the Rainbow - Hanging Pole 1-Up"))
        self.collect(self.get_item_by_name("Wing Mario Over the Rainbow - Cannon Unlock"))
        self.assertTrue(self.can_reach_location("Wing Mario Over the Rainbow - Hanging Pole 1-Up"))

    def test_hmc_metal_cap_access(self):
        self.collect(self.get_item_by_name("Progressive Basement Key"))
        self.assertFalse(self.can_reach_location("Hazy Maze Cave - Metal-Head Mario Can Move!"))
        self.collect(self.get_item_by_name("Purple Switches"))
        self.assertFalse(self.can_reach_location("Hazy Maze Cave - Metal-Head Mario Can Move!"))
        self.collect(self.get_item_by_name("Hazy Maze Cave - Metal Cap"))
        self.assertTrue(self.can_reach_location("Hazy Maze Cave - Metal-Head Mario Can Move!"))

    def test_vcutm_vanish_cap_access(self):
        self.collect(self.get_item_by_name("Progressive Basement Key"))
        self.collect(self.get_item_by_name("Checkerboard Platforms"))
        self.collect(self.get_item_by_name("Unlock Vanish Cap Under the Moat"))
        self.assertFalse(self.can_reach_location("Vanish Cap Under the Moat - Red Coins"))
        self.assertFalse(self.can_reach_location("Vanish Cap Under the Moat - Red Coin Platform 1-Up"))
        self.collect(self.get_item_by_name("Vanish Cap Under the Moat - Vanish Cap"))
        self.assertTrue(self.can_reach_location("Vanish Cap Under the Moat - Red Coins"))
        self.assertTrue(self.can_reach_location("Vanish Cap Under the Moat - Red Coin Platform 1-Up"))

    def test_lethal_lava_land_wing_cap_access(self):
        self.collect(self.get_item_by_name("Progressive Basement Key"))
        self.assertFalse(self.can_reach_location("Lethal Lava Land - Red-Hot Log Rolling"))
        self.collect(self.get_item_by_name("Lethal Lava Land - Wing Cap"))
        self.assertTrue(self.can_reach_location("Lethal Lava Land - Red-Hot Log Rolling"))


class WMotRCaplessBuddyAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "enable_locked_paintings": Options.EnableLockedPaintings.option_false,
        "one_up_checks": Options.OneUpChecks.option_true,
        "area_rando": Options.AreaRandomizer.option_Off,
        "strict_cap_requirements": Options.StrictCapRequirements.option_false,
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
    }

    def test_wmotr_bob_omb_buddy_accepts_capless_long_jump(self):
        self.collect([self.get_item_by_name("Progressive Upstairs Key")] * 3)
        self.collect(self.get_item_by_name("Side Flip"))
        self.assertFalse(self.can_reach_location("Wing Mario Over the Rainbow - Bob-omb Buddy"))
        self.collect(self.get_item_by_name("Long Jump"))
        self.assertTrue(self.can_reach_location("Wing Mario Over the Rainbow - Bob-omb Buddy"))

    def test_wmotr_bob_omb_buddy_platform_uses_buddy_platform_region(self):
        self.collect([self.get_item_by_name("Progressive Upstairs Key")] * 3)
        self.collect(self.get_item_by_name("Side Flip"))
        self.collect(self.get_item_by_name("Long Jump"))
        self.assertTrue(self.can_reach_location("Wing Mario Over the Rainbow - Bob-omb Buddy"))
        self.assertTrue(self.can_reach_location("Wing Mario Over the Rainbow - Bob-omb Buddy Platform 1-Up"))


class WingMarioOverTheRainbowBlocksanityAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_ARBITRARY_FEATURE_OPTIONS,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "buddy_checks": Options.BuddyChecks.option_true,
        "enable_locked_paintings": Options.EnableLockedPaintings.option_false,
        "one_up_checks": Options.OneUpChecks.option_true,
        "blocksanity": Options.Blocksanity.option_true,
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "area_rando": Options.AreaRandomizer.option_Off,
    }

    def test_cloud_blocks_require_flight(self):
        self.collect([self.get_item_by_name("Progressive Upstairs Key")] * 3)
        self.collect(self.get_item_by_name("Wing Cap"))
        self.assertFalse(self.can_reach_location(
            "Wing Mario Over the Rainbow - Cloud Across From Starting Cloud Wing Cap Block"))
        self.assertFalse(self.can_reach_location(
            "Wing Mario Over the Rainbow - Overlooking Bob-omb Buddy Cloud Wing Cap Block"))

        self.collect(self.get_item_by_name("Triple Jump"))
        self.assertTrue(self.can_reach_location(
            "Wing Mario Over the Rainbow - Cloud Across From Starting Cloud Wing Cap Block"))
        self.assertTrue(self.can_reach_location(
            "Wing Mario Over the Rainbow - Overlooking Bob-omb Buddy Cloud Wing Cap Block"))

    def test_cloud_blocks_accept_buddy_platform_and_cannon_flight(self):
        self.collect([self.get_item_by_name("Progressive Upstairs Key")] * 3)
        self.collect([
            self.get_item_by_name("Wing Cap"),
            self.get_item_by_name("Long Jump"),
            self.get_item_by_name("Side Flip"),
            self.world.create_item("ut_glitch"),
        ])
        self.assertFalse(self.can_reach_location(
            "Wing Mario Over the Rainbow - Cloud Across From Starting Cloud Wing Cap Block"))

        self.collect(self.get_item_by_name("Wing Mario Over the Rainbow - Cannon Unlock"))
        self.assertTrue(self.can_reach_location(
            "Wing Mario Over the Rainbow - Cloud Across From Starting Cloud Wing Cap Block"))
        self.assertTrue(self.can_reach_location(
            "Wing Mario Over the Rainbow - Overlooking Bob-omb Buddy Cloud Wing Cap Block"))

    def test_highest_cloud_block_and_one_up_are_in_cannon_region(self):
        self.collect([self.get_item_by_name("Progressive Upstairs Key")] * 3)
        self.collect([
            self.get_item_by_name("Wing Cap"),
            self.get_item_by_name("Triple Jump"),
        ])
        self.assertFalse(self.can_reach_location("Wing Mario Over the Rainbow - Highest Cloud Wing Cap Block"))
        self.assertFalse(self.can_reach_location("Wing Mario Over the Rainbow - Block 1-Up"))

        self.collect(self.get_item_by_name("Wing Mario Over the Rainbow - Cannon Unlock"))
        self.assertTrue(self.can_reach_location("Wing Mario Over the Rainbow - Highest Cloud Wing Cap Block"))
        self.assertTrue(self.can_reach_location("Wing Mario Over the Rainbow - Block 1-Up"))


class TTCVariantAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_ARBITRARY_FEATURE_OPTIONS,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "enable_locked_paintings": Options.EnableLockedPaintings.option_false,
        "area_rando": Options.AreaRandomizer.option_Off,
    }

    def collect_third_floor_access(self):
        self.collect([self.get_item_by_name("Progressive Upstairs Key")] * 2)

    def test_stomp_on_the_thwomp_reachable_from_moving_ttc(self):
        self.collect_third_floor_access()
        self.assertTrue(self.can_reach_region("Tick Tock Clock Moving"))
        self.assertTrue(self.can_reach_location("Tick Tock Clock - Stomp on the Thwomp"))

    def test_stomp_on_the_thwomp_unreachable_from_stopped_ttc(self):
        for ttc_entrance in sm64_ttc_entrances[1:]:
            self.multiworld.get_entrance(f"Third Floor -> {ttc_entrance}", self.player).access_rule = \
                lambda state: False

        self.collect_third_floor_access()
        self.assertTrue(self.can_reach_region("Tick Tock Clock - Top"))
        self.assertFalse(self.can_reach_region("Tick Tock Clock Moving"))
        self.assertFalse(self.can_reach_location("Tick Tock Clock - Stomp on the Thwomp"))

    def test_stop_time_red_coins_reachable_from_stopped_ttc(self):
        self.collect_third_floor_access()
        self.assertTrue(self.can_reach_region("Tick Tock Clock Stopped"))
        self.assertFalse(self.can_reach_location("Tick Tock Clock - Stop Time for Red Coins"))
        self.collect(self.get_item_by_name("Tick Tock Clock - Spinners"))
        self.assertTrue(self.can_reach_location("Tick Tock Clock - Stop Time for Red Coins"))

    def test_stop_time_red_coins_unreachable_from_moving_ttc_without_lower_access(self):
        stopped_entrance = sm64_ttc_entrances[0]
        self.multiworld.get_entrance(f"Third Floor -> {stopped_entrance}", self.player).access_rule = \
            lambda state: False
        self.multiworld.get_entrance("Tick Tock Clock - Lower", self.player).access_rule = \
            lambda state: False

        self.collect_third_floor_access()
        self.assertFalse(self.can_reach_region("Tick Tock Clock Stopped"))
        self.assertTrue(self.can_reach_region("Tick Tock Clock Moving"))
        self.assertFalse(self.can_reach_region("Tick Tock Clock - Lower"))
        self.assertFalse(self.can_reach_location("Tick Tock Clock - Stop Time for Red Coins"))


class TTCRandomizedMoveVariantAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_ARBITRARY_FEATURE_OPTIONS,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "enable_locked_paintings": Options.EnableLockedPaintings.option_false,
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "one_up_checks": Options.OneUpChecks.option_true,
        "area_rando": Options.AreaRandomizer.option_Off,
    }

    def collect_third_floor_access(self):
        self.collect([self.get_item_by_name("Progressive Upstairs Key")] * 2)

    def use_stopped_ttc_without_entry_move(self):
        for ttc_entrance in sm64_ttc_entrances[1:]:
            self.multiworld.get_entrance(f"Third Floor -> {ttc_entrance}", self.player).access_rule = \
                lambda state: False
        stopped_entrance = sm64_ttc_entrances[0]
        self.multiworld.get_entrance(f"Third Floor -> {stopped_entrance}", self.player).access_rule = \
            lambda state: True

    def test_spinners_reach_lower_from_stopped_ttc_without_entry_move(self):
        self.use_stopped_ttc_without_entry_move()
        self.collect_third_floor_access()
        self.assertTrue(self.can_reach_region("Tick Tock Clock Stopped"))
        self.assertFalse(self.can_reach_region("Tick Tock Clock - Lower"))
        self.collect(self.get_item_by_name("Tick Tock Clock - Spinners"))
        self.assertTrue(self.can_reach_region("Tick Tock Clock - Lower"))
        self.assertTrue(self.can_reach_location("Tick Tock Clock - Stop Time for Red Coins"))

    def test_wall_kick_does_not_reach_lower_without_moveless_logic(self):
        self.collect_third_floor_access()
        self.collect(self.get_item_by_name("Wall Kick"))
        self.assertFalse(self.can_reach_region("Tick Tock Clock - Lower"))

    def test_timed_jumps_require_moving_ttc_or_wall_kick(self):
        self.use_stopped_ttc_without_entry_move()
        self.collect_third_floor_access()
        self.collect([
            self.get_item_by_name("Tick Tock Clock - Spinners"),
            self.get_item_by_name("Climb"),
        ])
        self.assertTrue(self.can_reach_region("Tick Tock Clock - Mid"))
        self.assertTrue(self.can_reach_location("Tick Tock Clock - The Pit and the Pendulums"))
        self.assertFalse(self.can_reach_region("Tick Tock Clock - Upper"))
        self.assertFalse(self.can_reach_location("Tick Tock Clock - Timed Jumps on Moving Bars"))
        self.assertFalse(self.can_reach_location("Tick Tock Clock - Moving Bars Platform 1-Up"))
        self.collect(self.get_item_by_name("Wall Kick"))
        self.assertTrue(self.can_reach_region("Tick Tock Clock - Upper"))
        self.assertTrue(self.can_reach_location("Tick Tock Clock - Timed Jumps on Moving Bars"))
        self.assertTrue(self.can_reach_location("Tick Tock Clock - Moving Bars Platform 1-Up"))

    def test_timed_jumps_reachable_in_moving_ttc_without_wall_kick(self):
        self.collect_third_floor_access()
        self.collect([
            self.get_item_by_name("Side Flip"),
            self.get_item_by_name("Climb"),
        ])
        self.assertTrue(self.can_reach_region("Tick Tock Clock Moving"))
        self.assertTrue(self.can_reach_region("Tick Tock Clock - Upper"))
        self.assertTrue(self.can_reach_location("Tick Tock Clock - Timed Jumps on Moving Bars"))

    def test_pole_1up_is_in_upper_region(self):
        self.collect_third_floor_access()
        self.collect(self.get_item_by_name("Triple Jump"))
        self.assertTrue(self.can_reach_region("Tick Tock Clock - Lower"))
        self.assertFalse(self.can_reach_region("Tick Tock Clock - Upper"))
        self.assertFalse(self.can_reach_location("Tick Tock Clock - Pole 1-Up"))

        self.collect(self.get_item_by_name("Climb"))
        self.assertTrue(self.can_reach_region("Tick Tock Clock - Upper"))
        self.assertTrue(self.can_reach_location("Tick Tock Clock - Pole 1-Up"))

    def test_midway_1up_requires_spinners_or_long_jump_and_ledge_grab(self):
        self.collect_third_floor_access()
        self.collect([
            self.get_item_by_name("Triple Jump"),
            self.get_item_by_name("Ledge Grab"),
            self.get_item_by_name("Climb"),
        ])
        self.assertTrue(self.can_reach_region("Tick Tock Clock - Top"))
        self.assertFalse(self.can_reach_location("Tick Tock Clock - Midway Up Block 1-Up"))
        self.collect(self.get_item_by_name("Long Jump"))
        self.assertTrue(self.can_reach_location("Tick Tock Clock - Midway Up Block 1-Up"))

    def test_midway_1up_reachable_with_spinners(self):
        self.collect_third_floor_access()
        self.collect([
            self.get_item_by_name("Triple Jump"),
            self.get_item_by_name("Ledge Grab"),
            self.get_item_by_name("Climb"),
            self.get_item_by_name("Tick Tock Clock - Spinners"),
        ])
        self.assertTrue(self.can_reach_location("Tick Tock Clock - Midway Up Block 1-Up"))


class TTCMovelessWallKickAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "enable_locked_paintings": Options.EnableLockedPaintings.option_false,
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "strict_move_requirements": Options.StrictMoveRequirements.option_false,
        "area_rando": Options.AreaRandomizer.option_Off,
        "logic_tricks": {"Castle Tick Tock Clock Entrance With Wall Kick"},
    }

    def collect_third_floor_access(self):
        self.collect([self.get_item_by_name("Progressive Upstairs Key")] * 2)

    def test_wall_kick_reaches_lower_with_moveless_logic(self):
        self.collect_third_floor_access()
        self.collect(self.get_item_by_name("Wall Kick"))
        self.assertTrue(self.can_reach_region("Tick Tock Clock - Lower"))


class TickTockClockCoinStarAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_ARBITRARY_FEATURE_OPTIONS,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "enable_locked_paintings": Options.EnableLockedPaintings.option_false,
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "area_rando": Options.AreaRandomizer.option_Off,
    }

    def collect_third_floor_access(self):
        self.collect([self.get_item_by_name("Progressive Upstairs Key")] * 2)

    def use_stopped_ttc_without_entry_move(self):
        for ttc_entrance in sm64_ttc_entrances[1:]:
            self.multiworld.get_entrance(f"Third Floor -> {ttc_entrance}", self.player).access_rule = \
                lambda state: False
        stopped_entrance = sm64_ttc_entrances[0]
        self.multiworld.get_entrance(f"Third Floor -> {stopped_entrance}", self.player).access_rule = \
            lambda state: True


class TickTockClockCoinStar17AccessTestBase(TickTockClockCoinStarAccessTestBase):
    options = {
        **TickTockClockCoinStarAccessTestBase.options,
        "tick_tock_clock_coin_star_requirement": 17,
    }

    def test_coin_star_access(self):
        self.use_stopped_ttc_without_entry_move()
        self.collect_third_floor_access()
        self.assertTrue(self.can_reach_location("Tick Tock Clock - Coins Star"))


class TickTockClockCoinStar18AccessTestBase(TickTockClockCoinStarAccessTestBase):
    options = {
        **TickTockClockCoinStarAccessTestBase.options,
        "tick_tock_clock_coin_star_requirement": 18,
    }

    def test_coin_star_access(self):
        self.use_stopped_ttc_without_entry_move()
        self.collect_third_floor_access()
        self.assertFalse(self.can_reach_location("Tick Tock Clock - Coins Star"))


class TickTockClockCoinStar36StoppedSpinnersAccessTestBase(TickTockClockCoinStarAccessTestBase):
    options = {
        **TickTockClockCoinStarAccessTestBase.options,
        "tick_tock_clock_coin_star_requirement": 36,
    }

    def test_coin_star_access(self):
        self.use_stopped_ttc_without_entry_move()
        self.collect_third_floor_access()
        self.collect(self.get_item_by_name("Tick Tock Clock - Spinners"))
        self.assertTrue(self.can_reach_location("Tick Tock Clock - Coins Star"))


class TickTockClockCoinStar37StoppedSpinnersAccessTestBase(TickTockClockCoinStarAccessTestBase):
    options = {
        **TickTockClockCoinStarAccessTestBase.options,
        "tick_tock_clock_coin_star_requirement": 37,
    }

    def test_coin_star_access(self):
        self.use_stopped_ttc_without_entry_move()
        self.collect_third_floor_access()
        self.collect(self.get_item_by_name("Tick Tock Clock - Spinners"))
        self.assertFalse(self.can_reach_location("Tick Tock Clock - Coins Star"))


class TickTockClockCoinStar41StoppedSpinnersWallKickAccessTestBase(TickTockClockCoinStarAccessTestBase):
    options = {
        **TickTockClockCoinStarAccessTestBase.options,
        "tick_tock_clock_coin_star_requirement": 41,
    }

    def test_coin_star_access(self):
        self.use_stopped_ttc_without_entry_move()
        self.collect_third_floor_access()
        self.collect([
            self.get_item_by_name("Tick Tock Clock - Spinners"),
            self.get_item_by_name("Wall Kick"),
        ])
        self.assertTrue(self.can_reach_location("Tick Tock Clock - Coins Star"))


class TickTockClockCoinStar35MovingAccessTestBase(TickTockClockCoinStarAccessTestBase):
    options = {
        **TickTockClockCoinStarAccessTestBase.options,
        "tick_tock_clock_coin_star_requirement": 35,
    }

    def test_coin_star_access(self):
        self.collect_third_floor_access()
        self.collect(self.get_item_by_name("Side Flip"))
        self.assertTrue(self.can_reach_location("Tick Tock Clock - Coins Star"))


class TickTockClockCoinStar36MovingAccessTestBase(TickTockClockCoinStarAccessTestBase):
    options = {
        **TickTockClockCoinStarAccessTestBase.options,
        "tick_tock_clock_coin_star_requirement": 36,
    }

    def test_coin_star_access(self):
        self.collect_third_floor_access()
        self.collect(self.get_item_by_name("Side Flip"))
        self.assertFalse(self.can_reach_location("Tick Tock Clock - Coins Star"))


class TickTockClockCoinStar76UpperGroundPoundAccessTestBase(TickTockClockCoinStarAccessTestBase):
    options = {
        **TickTockClockCoinStarAccessTestBase.options,
        "tick_tock_clock_coin_star_requirement": 76,
    }

    def test_coin_star_access(self):
        self.collect_third_floor_access()
        self.collect([
            self.get_item_by_name("Side Flip"),
            self.get_item_by_name("Climb"),
            self.get_item_by_name("Ground Pound"),
        ])
        self.assertTrue(self.can_reach_location("Tick Tock Clock - Coins Star"))


class TickTockClockCoinStar77UpperGroundPoundAccessTestBase(TickTockClockCoinStarAccessTestBase):
    options = {
        **TickTockClockCoinStarAccessTestBase.options,
        "tick_tock_clock_coin_star_requirement": 77,
    }

    def test_coin_star_access(self):
        self.collect_third_floor_access()
        self.collect([
            self.get_item_by_name("Side Flip"),
            self.get_item_by_name("Climb"),
            self.get_item_by_name("Ground Pound"),
        ])
        self.assertFalse(self.can_reach_location("Tick Tock Clock - Coins Star"))


class TickTockClockCoinStar128AccessTestBase(TickTockClockCoinStarAccessTestBase):
    options = {
        **TickTockClockCoinStarAccessTestBase.options,
        "tick_tock_clock_coin_star_requirement": 128,
    }

    def test_coin_star_access(self):
        self.collect_third_floor_access()
        self.collect([
            self.get_item_by_name("Triple Jump"),
            self.get_item_by_name("Ledge Grab"),
            self.get_item_by_name("Climb"),
            self.get_item_by_name("Ground Pound"),
            self.get_item_by_name("Tick Tock Clock - Spinners"),
        ])
        self.assertTrue(self.can_reach_location("Tick Tock Clock - Coins Star"))


class RainbowRideCoinStarAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_ARBITRARY_FEATURE_OPTIONS,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "buddy_checks": Options.BuddyChecks.option_true,
        "enable_locked_paintings": Options.EnableLockedPaintings.option_false,
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "area_rando": Options.AreaRandomizer.option_Off,
    }

    def collect_rr_access(self):
        self.collect([self.get_item_by_name("Progressive Upstairs Key")] * 2)
        self.collect(self.get_item_by_name("Side Flip"))

    def disable_carpet_shortcut_to_maze(self):
        self.multiworld.get_entrance("Rainbow Ride - Initial to Maze", self.player).access_rule = \
            lambda state: False


class RainbowRideCoinStar8AccessTestBase(RainbowRideCoinStarAccessTestBase):
    options = {
        **RainbowRideCoinStarAccessTestBase.options,
        "rainbow_ride_coin_star_requirement": 8,
    }

    def test_coin_star_access(self):
        self.disable_carpet_shortcut_to_maze()
        self.collect_rr_access()
        self.collect(self.get_item_by_name("Rainbow Ride - Carpets"))
        self.assertTrue(self.can_reach_location("Rainbow Ride - Coins Star"))


class RainbowRideCoinStar9AccessTestBase(RainbowRideCoinStarAccessTestBase):
    options = {
        **RainbowRideCoinStarAccessTestBase.options,
        "rainbow_ride_coin_star_requirement": 9,
    }

    def test_coin_star_access(self):
        self.disable_carpet_shortcut_to_maze()
        self.collect_rr_access()
        self.collect(self.get_item_by_name("Rainbow Ride - Carpets"))
        self.assertFalse(self.can_reach_location("Rainbow Ride - Coins Star"))


class RainbowRideCoinStar50AccessTestBase(RainbowRideCoinStarAccessTestBase):
    options = {
        **RainbowRideCoinStarAccessTestBase.options,
        "rainbow_ride_coin_star_requirement": 50,
    }

    def test_coin_star_access(self):
        self.collect_rr_access()
        self.collect([
            self.get_item_by_name("Dive"),
            self.get_item_by_name("Climb"),
        ])
        self.assertTrue(self.can_reach_location("Rainbow Ride - Coins Star"))


class RainbowRideCoinStar51AccessTestBase(RainbowRideCoinStarAccessTestBase):
    options = {
        **RainbowRideCoinStarAccessTestBase.options,
        "rainbow_ride_coin_star_requirement": 51,
    }

    def test_coin_star_access(self):
        self.collect_rr_access()
        self.collect([
            self.get_item_by_name("Dive"),
            self.get_item_by_name("Climb"),
        ])
        self.assertFalse(self.can_reach_location("Rainbow Ride - Coins Star"))


class RainbowRideCoinStar96AccessTestBase(RainbowRideCoinStarAccessTestBase):
    options = {
        **RainbowRideCoinStarAccessTestBase.options,
        "rainbow_ride_coin_star_requirement": 96,
    }

    def test_coin_star_access(self):
        self.collect_rr_access()
        self.collect([
            self.get_item_by_name("Dive"),
            self.get_item_by_name("Climb"),
            self.get_item_by_name("Ground Pound"),
            self.get_item_by_name("Wall Kick"),
        ])
        self.assertTrue(self.can_reach_location("Rainbow Ride - Coins Star"))


class RainbowRideCoinStar97AccessTestBase(RainbowRideCoinStarAccessTestBase):
    options = {
        **RainbowRideCoinStarAccessTestBase.options,
        "rainbow_ride_coin_star_requirement": 97,
    }

    def test_coin_star_access(self):
        self.collect_rr_access()
        self.collect([
            self.get_item_by_name("Dive"),
            self.get_item_by_name("Climb"),
            self.get_item_by_name("Ground Pound"),
            self.get_item_by_name("Wall Kick"),
        ])
        self.assertFalse(self.can_reach_location("Rainbow Ride - Coins Star"))


class RainbowRideCoinStar146AccessTestBase(RainbowRideCoinStarAccessTestBase):
    options = {
        **RainbowRideCoinStarAccessTestBase.options,
        "rainbow_ride_coin_star_requirement": 146,
    }

    def test_coin_star_access(self):
        self.collect_rr_access()
        self.collect([
            self.get_item_by_name("Rainbow Ride - Carpets"),
            self.get_item_by_name("Long Jump"),
            self.get_item_by_name("Climb"),
            self.get_item_by_name("Ground Pound"),
            self.get_item_by_name("Wall Kick"),
            self.get_item_by_name("Rainbow Ride - Cannon Unlock"),
        ])
        self.assertTrue(self.can_reach_location("Rainbow Ride - Coins Star"))
