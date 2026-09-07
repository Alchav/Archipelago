from BaseClasses import CollectionState, ItemClassification

from .bases import SM64TestBase as _SM64TestBase
from .. import Options
from ..CoinLogic import COIN_EVALUATORS
from ..Regions import sm64_ttc_entrances
from ..Rules import can_use_logic_trick, get_per_level_action_item_name


class SM64TestBase(_SM64TestBase):
    """Legacy access tests assume star-producing objects themselves are present."""

    def world_setup(self, seed=None) -> None:
        super().world_setup(seed)
        if not hasattr(self, "world"):
            return
        for item_name in ("Freestanding Stars", "Star Blocks", "Star Secrets"):
            self.multiworld.state.collect(self.world.create_item(item_name))


def coin_rule(course_name):
    evaluator = COIN_EVALUATORS[course_name]

    def rule(state, player, coins):
        # These unit tests exercise a course's internal coin logic directly.
        # Treat that course as the starting region so entrance requirements do
        # not make every source unavailable.
        try:
            course_region = state.multiworld.get_region(course_name, player)
        except KeyError:
            pass
        else:
            state.reachable_regions[player].add(course_region)
            state.blocked_connections[player].update(
                entrance for entrance in course_region.exits
                if entrance.connected_region is not None)
            state.stale[player] = True
        return evaluator(state, player, coins).reachable_coins >= coins

    return rule


bob_omb_battlefield_coins = coin_rule("Bob-omb Battlefield")
whomps_fortress_coins = coin_rule("Whomp's Fortress")
jolly_roger_bay_coins = coin_rule("Jolly Roger Bay")
cool_cool_mountain_coins = coin_rule("Cool, Cool Mountain")
big_boos_haunt_coins = coin_rule("Big Boo's Haunt")
hazy_maze_cave_coins = coin_rule("Hazy Maze Cave")
lethal_lava_land_coins = coin_rule("Lethal Lava Land")
shifting_sand_land_coins = coin_rule("Shifting Sand Land")
dire_dire_docks_coins = coin_rule("Dire, Dire Docks")
snowmans_land_coins = coin_rule("Snowman's Land")
wet_dry_world_coins = coin_rule("Wet-Dry World")
tall_tall_mountain_coins = coin_rule("Tall, Tall Mountain")
tiny_huge_island_coins = coin_rule("Tiny-Huge Island")
tick_tock_clock_coins = coin_rule("Tick Tock Clock")
rainbow_ride_coins = coin_rule("Rainbow Ride")
princess_secret_slide_coins = coin_rule("The Princess's Secret Slide")
secret_aquarium_coins = coin_rule("The Secret Aquarium")
wing_mario_over_the_rainbow_coins = coin_rule("Wing Mario Over the Rainbow")
tower_of_the_wing_cap_coins = coin_rule("Tower of the Wing Cap")
vanish_cap_under_the_moat_coins = coin_rule("Vanish Cap Under the Moat")
cavern_of_the_metal_cap_coins = coin_rule("Cavern of the Metal Cap")
bowser_in_the_dark_world_coins = coin_rule("Bowser in the Dark World")
bowser_in_the_fire_sea_coins = coin_rule("Bowser in the Fire Sea")
bowser_in_the_sky_coins = coin_rule("Bowser in the Sky")


SHUFFLED_ARBITRARY_FEATURE_OPTIONS = {
    "level_features": Options.LevelFeatures.option_global,
        "bobomb_buddies": Options.BobombBuddies.option_global,
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
        "level_unlocks": Options.LevelUnlocks.option_special_only,
        "one_up_checks": Options.OneUpChecks.option_true,
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
                "logic_tricks": {"Castle Third Tree From Waterfall 1-Up With No Movement"},
    }

    def test_no_movement_trick_reaches_tree_one_up(self):
        self.assertTrue(self.can_reach_location("Castle - Third Tree From Waterfall 1-Up"))


class CastleTTCLogicTricksTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
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


class FullLevelUnlockAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
                "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "level_unlocks": Options.LevelUnlocks.option_full,
    }

    def test_third_floor_levels_require_their_unlocks(self):
        self.collect([self.get_item_by_name("Progressive Upstairs Key")] * 2)
        self.assertFalse(self.can_reach_region("Rainbow Ride"))
        self.assertFalse(self.can_reach_region("Wing Mario Over the Rainbow"))
        self.collect(self.get_item_by_name("Unlock Rainbow Ride"))
        self.assertTrue(self.can_reach_region("Rainbow Ride"))
        self.assertFalse(self.can_reach_region("Wing Mario Over the Rainbow"))
        self.collect(self.get_item_by_name("Unlock Wing Mario Over the Rainbow"))
        self.assertTrue(self.can_reach_region("Wing Mario Over the Rainbow"))


class GlobalOneUpUnlockAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
                "one_up_checks": Options.OneUpChecks.option_true,
        "one_up_unlocks": Options.OneUpUnlocks.option_global,
    }

    def test_each_global_item_controls_its_one_up_category(self):
        checks = (
            ("Bob-omb Battlefield - Switch Tunnel 1-Up", "Freestanding 1-Ups"),
            ("Bob-omb Battlefield - Flower Ring 1-Up", "Trigger 1-Ups"),
            ("Cool, Cool Mountain - Near Snowman Block 1-Up", "1-Up Blocks"),
            ("Castle - Left Butterfly 1-Up", "Butterflies"),
        )
        for location_name, item_name in checks:
            with self.subTest(location=location_name):
                self.assertFalse(self.can_reach_location(location_name))
                self.collect(self.get_item_by_name(item_name))
                self.assertTrue(self.can_reach_location(location_name))


class PerLevelOneUpUnlockAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
                "one_up_checks": Options.OneUpChecks.option_true,
        "one_up_unlocks": Options.OneUpUnlocks.option_per_level,
    }

    def test_per_level_item_only_unlocks_matching_level(self):
        location_name = "Bob-omb Battlefield - Switch Tunnel 1-Up"
        self.assertFalse(self.can_reach_location(location_name))
        self.collect(self.get_item_by_name("Big Boo's Haunt - Freestanding 1-Ups"))
        self.assertFalse(self.can_reach_location(location_name))
        self.collect(self.get_item_by_name("Bob-omb Battlefield - Freestanding 1-Ups"))
        self.assertTrue(self.can_reach_location(location_name))

    def test_per_level_butterfly_item_only_unlocks_matching_level(self):
        castle_location = "Castle - Left Butterfly 1-Up"
        self.assertFalse(self.can_reach_location(castle_location))
        self.collect(self.get_item_by_name("Whomp's Fortress - Butterflies"))
        self.assertFalse(self.can_reach_location(castle_location))
        self.collect(self.get_item_by_name("Castle - Butterflies"))
        self.assertTrue(self.can_reach_location(castle_location))


class CastleThirtyStarDoorLogicTricksTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
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
                "logic_tricks": {
            "Castle Lobby Backwards Long Jump Through the 8 Star Door",
            "Castle Backwards Long Jump Through the 50 Star Door",
            "Castle Backwards Long Jump Through the 70 Star Door",
        },
    }

    def test_lobby_8_star_door_blj_requires_long_jump_and_ledge_grab(self):
        self.assertFalse(self.can_reach_region("Bowser in the Dark World"))
        self.collect(self.get_item_by_name("Long Jump"))
        self.assertFalse(self.can_reach_region("Bowser in the Dark World"))
        self.collect(self.get_item_by_name("Ledge Grab"))
        self.assertTrue(self.can_reach_region("Bowser in the Dark World"))

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
        "level_unlocks": Options.LevelUnlocks.option_special_only,
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
                "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "level_unlocks": Options.LevelUnlocks.option_full,
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
        self.collect(self.world.create_item("Glitched Logic"))
        self.assertTrue(self.can_reach_location("Bob-omb Battlefield - Behind Chain Chomp's Gate"))

    def test_ut_glitch_satisfies_capless(self):
        self.collect(self.world.create_item("Bob-omb Battlefield - Cannon Unlock"))
        self.assertFalse(self.can_reach_location("Bob-omb Battlefield - Mario Wings to the Sky"))
        self.collect(self.world.create_item("Glitched Logic"))
        self.assertTrue(self.can_reach_location("Bob-omb Battlefield - Mario Wings to the Sky"))

    def test_ut_glitch_satisfies_cannonless(self):
        self.collect(self.world.create_item("Wing Cap"))
        self.assertFalse(self.can_reach_location("Bob-omb Battlefield - Shoot to the Island in the Sky"))
        self.collect(self.world.create_item("Glitched Logic"))
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
        self.assertFalse(self.can_reach_location("Bob-omb Battlefield - Mario Wings to the Sky"))
        self.collect(self.world.create_item("Glitched Logic"))
        self.assertFalse(self.can_reach_location("Bob-omb Battlefield - Mario Wings to the Sky"))
        self.collect(self.get_item_by_name("Bob-omb Battlefield - Cannon Unlock"))
        self.assertTrue(self.can_reach_location("Bob-omb Battlefield - Mario Wings to the Sky"))

    def test_unselected_hard_trick_remains_out_of_logic_with_ut_glitch(self):
        self.collect([self.get_item_by_name("Long Jump"), self.world.create_item("Glitched Logic")])
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


class BobOmbBattlefieldIndividualUnlockLogicTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "buddy_checks": Options.BuddyChecks.option_true,
        "coin_object_unlocks": Options.CoinObjectUnlocks.option_per_level,
        "enemy_unlocks": Options.EnemyUnlocks.option_per_level,
    }

    def test_initial_coin_sources_are_counted_independently(self):
        source_coins = {
            "Bob-omb Battlefield - Red Coins": 14,
            "Bob-omb Battlefield - Horizontal Coin Lines": 15,
            "Bob-omb Battlefield - Horizontal Coin Rings": 8,
            "Bob-omb Battlefield - Breakable Coin Box": 3,
            "Bob-omb Battlefield - Throwable Cork Boxes": 6,
            "Bob-omb Battlefield - Wooden Posts": 25,
            "Bob-omb Battlefield - Bob-ombs": 12,
            "Bob-omb Battlefield - Goombas": 11,
            "Bob-omb Battlefield - Koopa Troopa": 5,
        }
        self.assertFalse(bob_omb_battlefield_coins(self.multiworld.state, self.player, 1))
        for item_name, expected_coins in source_coins.items():
            with self.subTest(item=item_name):
                item = self.get_item_by_name(item_name)
                self.collect(item)
                self.assertTrue(bob_omb_battlefield_coins(
                    self.multiworld.state, self.player, expected_coins))
                self.assertFalse(bob_omb_battlefield_coins(
                    self.multiworld.state, self.player, expected_coins + 1))
                self.remove(item)

    def test_red_coin_star_requires_red_coins(self):
        self.collect_by_name([
            "Bob-omb Battlefield - Cannon Unlock",
            "Bob-omb Battlefield - Vertical Coin Rings",
            "Climb",
        ])
        self.assertFalse(self.can_reach_location("Bob-omb Battlefield - Find the 8 Red Coins"))
        self.collect(self.get_item_by_name("Bob-omb Battlefield - Red Coins"))
        self.assertTrue(self.can_reach_location("Bob-omb Battlefield - Find the 8 Red Coins"))

    def test_mario_wings_requires_visible_coin_markers(self):
        self.collect([
            self.get_item_by_name("Bob-omb Battlefield - Cannon Unlock"),
            self.get_item_by_name("Wing Cap"),
        ])
        self.assertFalse(self.can_reach_location("Bob-omb Battlefield - Mario Wings to the Sky"))
        self.collect(self.get_item_by_name("Bob-omb Battlefield - Vertical Coin Rings"))
        self.assertTrue(self.can_reach_location("Bob-omb Battlefield - Mario Wings to the Sky"))

    def test_single_yellow_coins_are_also_valid_markers(self):
        self.collect([
            self.get_item_by_name("Bob-omb Battlefield - Cannon Unlock"),
            self.get_item_by_name("Wing Cap"),
            self.get_item_by_name("Bob-omb Battlefield - Single Yellow Coins"),
        ])
        self.assertTrue(self.can_reach_location("Bob-omb Battlefield - Mario Wings to the Sky"))

    def test_single_yellow_and_vertical_ring_coins_are_counted_separately(self):
        self.collect([
            self.get_item_by_name("Bob-omb Battlefield - Cannon Unlock"),
            self.get_item_by_name("Wing Cap"),
            self.get_item_by_name("Bob-omb Battlefield - Single Yellow Coins"),
        ])
        evaluation = COIN_EVALUATORS["Bob-omb Battlefield"](
            self.multiworld.state, self.player, 146)
        self.assertEqual(5, evaluation.reachable_coins)

        self.remove_by_name("Bob-omb Battlefield - Single Yellow Coins")
        self.collect(self.get_item_by_name("Bob-omb Battlefield - Vertical Coin Rings"))
        evaluation = COIN_EVALUATORS["Bob-omb Battlefield"](
            self.multiworld.state, self.player, 146)
        self.assertEqual(40, evaluation.reachable_coins)

    def test_chain_chomp_normal_route_requires_wooden_posts(self):
        self.collect_by_name([
            "Ground Pound",
            "Bob-omb Battlefield - Chain Chomp",
        ])
        self.assertFalse(self.can_reach_location("Bob-omb Battlefield - Behind Chain Chomp's Gate"))
        self.collect(self.get_item_by_name("Bob-omb Battlefield - Wooden Posts"))
        self.assertTrue(self.can_reach_location("Bob-omb Battlefield - Behind Chain Chomp's Gate"))


class BobOmbBattlefieldUnlockTricksTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "buddy_checks": Options.BuddyChecks.option_true,
        "coin_object_unlocks": Options.CoinObjectUnlocks.option_per_level,
        "enemy_unlocks": Options.EnemyUnlocks.option_per_level,
        "logic_tricks": {
            "Bob-omb Battlefield Mario Wings to the Sky without Coin Markers",
            "Bob-omb Battlefield Island with Koopa Shell",
            "Bob-omb Battlefield Chain Chomp Gate with Bob-omb Clip",
            "Bob-omb Battlefield Chain Chomp Gate with Throwable Cork Box Clip",
        },
    }

    def test_markerless_trick_still_requires_a_mario_wings_movement_route(self):
        self.assertFalse(self.can_reach_location("Bob-omb Battlefield - Mario Wings to the Sky"))
        self.collect([
            self.get_item_by_name("Bob-omb Battlefield - Cannon Unlock"),
            self.get_item_by_name("Wing Cap"),
        ])
        self.assertTrue(self.can_reach_location("Bob-omb Battlefield - Mario Wings to the Sky"))

    def test_koopa_shell_trick_requires_koopa_troopa(self):
        self.assertFalse(self.can_reach_region("Bob-omb Battlefield - Island"))
        self.collect(self.get_item_by_name("Bob-omb Battlefield - Koopa Troopa"))
        self.assertTrue(self.can_reach_region("Bob-omb Battlefield - Island"))

    def test_chain_chomp_clip_requires_bob_ombs(self):
        self.assertFalse(self.can_reach_location("Bob-omb Battlefield - Behind Chain Chomp's Gate"))
        self.collect_by_name([
            "Bob-omb Battlefield - Chain Chomp",
            "Bob-omb Battlefield - Bob-ombs",
        ])
        self.assertTrue(self.can_reach_location("Bob-omb Battlefield - Behind Chain Chomp's Gate"))

    def test_chain_chomp_clip_requires_throwable_cork_boxes(self):
        self.assertFalse(self.can_reach_location("Bob-omb Battlefield - Behind Chain Chomp's Gate"))
        self.collect_by_name([
            "Bob-omb Battlefield - Chain Chomp",
            "Bob-omb Battlefield - Throwable Cork Boxes",
        ])
        self.assertTrue(self.can_reach_location("Bob-omb Battlefield - Behind Chain Chomp's Gate"))


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
        "level_unlocks": Options.LevelUnlocks.option_special_only,
        "one_up_checks": Options.OneUpChecks.option_true,
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
        self.assertTrue(self.can_reach_region("Castle Courtyard"))
        self.assertEqual(
            self.multiworld.get_entrance(
                "Castle Courtyard -> Big Boo's Haunt", self.player
            ).parent_region.name,
            "Castle Courtyard",
        )
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
        "level_unlocks": Options.LevelUnlocks.option_special_only,
        "one_up_checks": Options.OneUpChecks.option_true,
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
        "level_unlocks": Options.LevelUnlocks.option_special_only,
        "buddy_checks": Options.BuddyChecks.option_true,
        "one_up_checks": Options.OneUpChecks.option_true,
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

    def test_ssl_pyramid_1up_access(self):
        self.collect_basement_access()
        self.assertTrue(
            self.can_reach_location("Shifting Sand Land - Pyramid Grindel 1-Up"))
        # The elevator cannot carry a normal lower-pyramid entry to the upper interior.
        self.assertFalse(
            self.can_reach_location("Shifting Sand Land - Pyramid Above the First Wire Grid 1-Up"))


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
        "level_unlocks": Options.LevelUnlocks.option_special_only,
        "one_up_checks": Options.OneUpChecks.option_true,
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
        self.assertFalse(self.can_reach_location("Bowser in the Fire Sea - Near Final Poles 1-Up"))

        self.collect(self.get_item_by_name("Progressive Upstairs Key"))
        self.assertTrue(self.can_reach_location("Bowser in the Fire Sea - Second Stone Structure 1-Up"))
        self.assertTrue(self.can_reach_location("Bowser in the Fire Sea - Near Final Poles 1-Up"))


class GlobalBowserStageOneUpAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        "bowser_stage_1ups": Options.BowserStage1Ups.option_global,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "level_unlocks": Options.LevelUnlocks.option_special_only,
        "one_up_checks": Options.OneUpChecks.option_true,
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
        self.assertTrue(self.can_reach_location("Bowser in the Fire Sea - Near Final Poles 1-Up"))


class ShuffledMoveBowserInTheFireSeaOneUpAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "bowser_stage_1ups": Options.BowserStage1Ups.option_global,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "level_unlocks": Options.LevelUnlocks.option_special_only,
        "one_up_checks": Options.OneUpChecks.option_true,
            }

    def test_near_final_poles_freestanding_1up_accepts_triple_jump(self):
        self.collect([self.get_item_by_name("Progressive Basement Key")] * 2)
        self.collect([
            self.get_item_by_name("Unlock Bowser in the Fire Sea"),
            self.get_item_by_name("Bowser Stage Extra 1-Ups"),
            self.get_item_by_name("Climb"),
        ])
        self.assertFalse(self.can_reach_location("Bowser in the Fire Sea - Near Final Poles 1-Up"))

        self.collect(self.get_item_by_name("Triple Jump"))
        self.assertTrue(self.can_reach_location("Bowser in the Fire Sea - Near Final Poles 1-Up"))


class IndividualBowserStageOneUpAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        "bowser_stage_1ups": Options.BowserStage1Ups.option_per_level,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "level_unlocks": Options.LevelUnlocks.option_special_only,
        "one_up_checks": Options.OneUpChecks.option_true,
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
        "level_unlocks": Options.LevelUnlocks.option_special_only,
        "one_up_checks": Options.OneUpChecks.option_true,
            }

    def test_bowser_stage_1ups_are_always_spawned_in_logic(self):
        self.collect(self.get_item_by_name("Dark World Key"))
        self.assertTrue(self.can_reach_location("Bowser in the Dark World - Center Overhang 1-Up"))
        self.assertTrue(self.can_reach_location("Bowser in the Dark World - Left Tilting Platform Base 1-Up"))
        self.assertTrue(self.can_reach_location("Bowser in the Dark World - Far Overhang 1-Up"))

        self.collect([self.get_item_by_name("Progressive Basement Key")] * 2)
        self.collect(self.get_item_by_name("Unlock Bowser in the Fire Sea"))
        self.assertTrue(self.can_reach_location("Bowser in the Fire Sea - Second Stone Structure 1-Up"))
        self.assertTrue(self.can_reach_location("Bowser in the Fire Sea - Near Final Poles 1-Up"))


class LevelFeatureAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        "level_unlocks": Options.LevelUnlocks.option_special_only,
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
        self.collect(self.get_item_by_name("Cool, Cool Mountain - Snowman's Body"))
        self.assertTrue(self.can_reach_location("Cool, Cool Mountain - Snowman's Lost His Head"))


class NewLevelFeatureUnlockAccessTestBase(_SM64TestBase):
    run_default_tests = False
    options = {
                "level_features": Options.LevelFeatures.option_global,
        "level_unlocks": Options.LevelUnlocks.option_disabled,
        "blocksanity": Options.Blocksanity.option_true,
    }

    def assert_global_feature_gate(self, item_name, location_name):
        self.collect_all_but({item_name})
        self.assertFalse(self.can_reach_location(location_name))
        self.collect(self.world.create_item(item_name))
        self.assertTrue(self.can_reach_location(location_name))

    def test_freestanding_star_gate(self):
        self.assert_global_feature_gate(
            "Freestanding Stars", "Cool, Cool Mountain - Wall Kicks Will Work")

    def test_star_block_gate(self):
        self.assert_global_feature_gate(
            "Star Blocks", "Jolly Roger Bay - Blast to the Stone Pillar")

    def test_koopa_shell_block_gate(self):
        self.assert_global_feature_gate(
            "Koopa Shell Blocks", "Snowman's Land - Koopa Shell Block")

    def test_star_secret_gate(self):
        self.assert_global_feature_gate(
            "Star Secrets", "Bob-omb Battlefield - Mario Wings to the Sky")

    def test_jet_stream_gate(self):
        self.assert_global_feature_gate(
            "Jet Streams", "Dire, Dire Docks - Through the Jet Stream")


class StarBlockChecksAndStarsAccessTest(SM64TestBase):
    run_default_tests = False
    include_baseline_level_feature_unlocks = False
    options = {
                "level_features": Options.LevelFeatures.option_global,
        "level_unlocks": Options.LevelUnlocks.option_disabled,
        "blocksanity": Options.Blocksanity.option_true,
    }

    def test_every_star_block_and_its_star_require_star_blocks(self):
        pairs = (
            ("Bob-omb Battlefield - Shoot to the Island in the Sky Star Block",
             "Bob-omb Battlefield - Shoot to the Island in the Sky"),
            ("Jolly Roger Bay - Blast to the Stone Pillar Star Block",
             "Jolly Roger Bay - Blast to the Stone Pillar"),
            ("Jolly Roger Bay - Plunder in the Sunken Ship Star Block",
             "Jolly Roger Bay - Plunder in the Sunken Ship"),
            ("The Princess's Secret Slide - Star Block",
             "The Princess's Secret Slide - Block Star"),
            ("Rainbow Ride - Somewhere Over the Rainbow Star Block",
             "Rainbow Ride - Somewhere Over the Rainbow"),
            ("Snowman's Land - Whirl from the Freezing Pond Star Block",
             "Snowman's Land - Whirl from the Freezing Pond"),
            ("Tiny-Huge Island - The Tip Top of the Huge Island Star Block",
             "Tiny-Huge Island - The Tip Top of the Huge Island"),
            ("Wet-Dry World - Shocking Arrow Lifts Star Block",
             "Wet-Dry World - Shocking Arrow Lifts!"),
            ("Wet-Dry World - Top o' the Town Star Block",
             "Wet-Dry World - Top o' the Town"),
        )
        cases = []
        for block, star in pairs:
            cases.extend((
                [block, False, [], ["Star Blocks"]],
                [block, True, ["Star Blocks"], ["Star Blocks"]],
                [star, False, [], ["Star Blocks"]],
                [star, True, ["Star Blocks"], ["Star Blocks"]],
            ))
        self.run_location_tests(cases, starting_regions=(
            "Bob-omb Battlefield",
            "Jolly Roger Bay",
            "The Princess's Secret Slide",
            "Rainbow Ride",
            "Snowman's Land",
            "Tiny-Huge Island (Huge)",
            "Wet-Dry World",
            "Wet-Dry World - Low Water",
            "Wet-Dry World - Cannon",
        ))


class FullLevelEntranceUnlockAccessTestBase(_SM64TestBase):
    run_default_tests = False
    options = {
                "level_unlocks": Options.LevelUnlocks.option_full,
    }

    def assert_level_unlock_gate(self, item_name, region_name):
        self.collect_all_but({item_name})
        self.assertFalse(self.can_reach_region(region_name))
        self.collect(self.world.create_item(item_name))
        self.assertTrue(self.can_reach_region(region_name))

    def test_bob_omb_battlefield_unlock(self):
        self.assert_level_unlock_gate("Unlock Bob-omb Battlefield", "Bob-omb Battlefield")

    def test_princess_secret_slide_unlock(self):
        self.assert_level_unlock_gate("Unlock The Princess's Secret Slide", "The Princess's Secret Slide")

    def test_secret_aquarium_unlock(self):
        self.assert_level_unlock_gate("Unlock The Secret Aquarium", "The Secret Aquarium")

    def test_cavern_of_the_metal_cap_unlock(self):
        self.assert_level_unlock_gate("Unlock Cavern of the Metal Cap", "Cavern of the Metal Cap")


class PerLevelMoveAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        "level_unlocks": Options.LevelUnlocks.option_special_only,
                "level_features": Options.LevelFeatures.option_global,
        "bobomb_buddies": Options.BobombBuddies.option_global,
        "triple_jump": Options.TripleJump.option_per_level,
        "backflip": Options.Backflip.option_global,
        "side_flip": Options.SideFlip.option_per_level,
        "wall_kick": Options.WallKick.option_per_level,
        "ledge_grab": Options.LedgeGrab.option_global,
        "dive": Options.Dive.option_per_level,
        "climb": Options.Climb.option_per_level,
    }

    def test_course_rule_accepts_global_move_item(self):
        self.assertFalse(self.can_reach_region("Whomp's Fortress - Top"))
        self.collect(self.world.create_item("Wall Kick"))
        self.collect(self.world.create_item("Whomp's Fortress - Side Flip"))
        self.assertTrue(self.can_reach_region("Whomp's Fortress - Top"))

    def test_course_rule_accepts_per_level_move_item(self):
        self.assertFalse(self.can_reach_region("Whomp's Fortress - Top"))
        self.collect(self.world.create_item("Whomp's Fortress - Wall Kick"))
        self.collect(self.world.create_item("Whomp's Fortress - Side Flip"))
        self.assertTrue(self.can_reach_region("Whomp's Fortress - Top"))

    def test_castle_entrance_rule_requires_misc_move_item(self):
        self.assertFalse(self.can_reach_region("The Secret Aquarium"))
        self.collect(self.world.create_item("Jolly Roger Bay - Side Flip"))
        self.assertFalse(self.can_reach_region("The Secret Aquarium"))

        self.collect(self.world.create_item("Misc - Side Flip"))
        self.assertTrue(self.can_reach_region("The Secret Aquarium"))

    def test_cap_switch_stage_rule_uses_misc_move_item(self):
        self.collect([self.get_item_by_name("Progressive Key")] * 2)
        self.collect(self.get_item_by_name("Checkerboard Platforms"))
        self.collect(self.get_item_by_name("Cap Switches"))
        self.collect(self.get_item_by_name("Unlock Vanish Cap Under the Moat"))
        self.assertFalse(self.can_reach_location("Vanish Cap Under the Moat - Switch"))

        self.collect(self.world.create_item("Whomp's Fortress - Wall Kick"))
        self.assertFalse(self.can_reach_location("Vanish Cap Under the Moat - Switch"))

        self.collect(self.world.create_item("Misc - Wall Kick"))
        self.assertTrue(self.can_reach_location("Vanish Cap Under the Moat - Switch"))

    def test_secret_stage_names_use_misc_move_items(self):
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
                    "Misc - Triple Jump")

    def test_wmotR_rule_uses_misc_move_item(self):
        self.collect([self.get_item_by_name("Progressive Key")] * 5)
        self.collect(self.world.create_item("Wing Cap"))
        self.collect(self.world.create_item("Bob-omb Buddies"))
        self.assertFalse(self.can_reach_location("Wing Mario Over the Rainbow - Bob-omb Buddy"))

        self.collect(self.world.create_item("Bob-omb Battlefield - Triple Jump"))
        self.assertFalse(self.can_reach_location("Wing Mario Over the Rainbow - Bob-omb Buddy"))

        self.collect(self.world.create_item("Misc - Triple Jump"))
        self.assertTrue(self.can_reach_location("Wing Mario Over the Rainbow - Bob-omb Buddy"))

    def test_collapsed_rule_accepts_exact_secret_stage_item(self):
        self.collect([self.get_item_by_name("Progressive Key")] * 5)
        self.collect(self.world.create_item("Wing Cap"))
        self.collect(self.world.create_item("Bob-omb Buddies"))
        self.collect(self.world.create_item("Castle - Triple Jump"))
        self.collect(self.world.create_item("Wing Mario Over the Rainbow - Triple Jump"))
        self.assertTrue(self.can_reach_location("Wing Mario Over the Rainbow - Bob-omb Buddy"))


class SeparateSecretStageMoveAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        "triple_jump": Options.TripleJump.option_per_level,
        "combined_castle_and_secret_stage_move_items":
            Options.CombinedCastleAndSecretStageMoveItems.option_false,
    }

    def test_secret_stage_names_use_separate_move_items(self):
        self.assertEqual(
            get_per_level_action_item_name("Bowser in the Sky", "Triple Jump", False),
            "Bowser in the Sky - Triple Jump")
        self.assertEqual(
            get_per_level_action_item_name("The Secret Aquarium", "Triple Jump", False),
            "Castle - Triple Jump")

    def test_wmotr_rule_uses_wmotr_move_item(self):
        self.collect([self.get_item_by_name("Progressive Key")] * 5)
        self.collect(self.world.create_item("Wing Cap"))
        self.collect(self.world.create_item("Bob-omb Buddies"))
        self.assertFalse(self.can_reach_location("Wing Mario Over the Rainbow - Bob-omb Buddy"))
        self.collect(self.world.create_item("Castle - Triple Jump"))
        self.assertFalse(self.can_reach_location("Wing Mario Over the Rainbow - Bob-omb Buddy"))
        self.collect(self.world.create_item("Wing Mario Over the Rainbow - Triple Jump"))
        self.assertTrue(self.can_reach_location("Wing Mario Over the Rainbow - Bob-omb Buddy"))

    def test_separate_rule_accepts_misc_move_item(self):
        self.collect([self.get_item_by_name("Progressive Key")] * 5)
        self.collect(self.world.create_item("Wing Cap"))
        self.collect(self.world.create_item("Bob-omb Buddies"))
        self.collect(self.world.create_item("Misc - Triple Jump"))
        self.assertTrue(self.can_reach_location("Wing Mario Over the Rainbow - Bob-omb Buddy"))


class ArbitraryFeatureAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_ARBITRARY_FEATURE_OPTIONS,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "buddy_checks": Options.BuddyChecks.option_true,
        "level_unlocks": Options.LevelUnlocks.option_special_only,
        "one_up_checks": Options.OneUpChecks.option_true,
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
                "universal_tracker_glitched_logic": {
            "Dire, Dire Docks Board Bowser's Sub with Triple Jump",
            "Hazy Maze Cave Metal-Head Mario Room without Metal Cap",
            "Whomp's Fortress Caged Island from the Floating Island with Triple Jump Off of Whomp King",
        },
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

    def test_hmc_red_coin_room_regions(self):
        self.collect_basement_access()
        self.collect(self.get_item_by_name("Wall Kick"))
        self.assertTrue(self.can_reach_region("Hazy Maze Cave - Mid Red Coin Room"))
        self.assertFalse(self.can_reach_region("Hazy Maze Cave - Upper Red Coin Room"))

        self.collect(self.get_item_by_name("Climb"))
        self.assertTrue(self.can_reach_region("Hazy Maze Cave - Upper Red Coin Room"))

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
        self.assertFalse(self.can_reach_location("Rainbow Ride - Top of Red Coin Maze Donut 1-Up"))

        self.collect(self.get_item_by_name("Climb"))
        self.assertFalse(self.can_reach_location("Rainbow Ride - Top of Red Coin Maze Block 1-Up"))
        self.assertFalse(self.can_reach_location("Rainbow Ride - Top of Red Coin Maze Donut 1-Up"))

        self.collect(self.get_item_by_name("Rainbow Ride - Carpets"))
        self.assertTrue(self.can_reach_location("Rainbow Ride - Top of Red Coin Maze Block 1-Up"))
        self.assertTrue(self.can_reach_location("Rainbow Ride - Top of Red Coin Maze Donut 1-Up"))

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

    def test_rainbow_ride_cruiser_pole_requires_cruiser_and_climb(self):
        self.collect_third_floor_access()
        self.collect(self.get_item_by_name("Side Flip"))
        self.collect(self.get_item_by_name("Rainbow Ride - Carpets"))
        self.assertTrue(self.can_reach_region("Rainbow Ride - Cruiser"))
        self.assertTrue(self.can_reach_location("Rainbow Ride - Cruiser Tip 1-Up"))
        self.assertFalse(self.can_reach_location("Rainbow Ride - Cruiser Pole 1-Up"))

        self.collect(self.get_item_by_name("Climb"))
        self.assertTrue(self.can_reach_location("Rainbow Ride - Cruiser Pole 1-Up"))

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

    def test_whomps_fortress_top_hoot_route_requires_climb(self):
        self.collect(self.get_item_by_name("Whomp's Fortress - Hoot"))
        self.assertFalse(self.can_reach_region("Whomp's Fortress - Top"))
        self.collect(self.get_item_by_name("Climb"))
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
            self.world.create_item("Checkerboard Platforms"),
            self.get_item_by_name("Triple Jump"),
            self.world.create_item("Glitched Logic"),
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
            self.get_item_by_name("Cap Switches"),
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

        self.collect(self.get_item_by_name("Warp Pipes"))
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

        self.collect(self.get_item_by_name("Warp Pipes"))
        self.assertTrue(self.can_reach_region("Tiny-Huge Island (Huge)"))

    def test_tiny_huge_island_koopa_region_connects_to_tiny_main_with_warp_pipes(self):
        self.multiworld.get_entrance("Second Floor -> Tiny-Huge Island (Tiny)", self.player).access_rule = \
            lambda state: False

        self.collect_second_floor_access()
        self.assertTrue(self.can_reach_region("Tiny-Huge Island (Huge)"))
        self.assertFalse(self.can_reach_region("Tiny-Huge Island - Tiny Main"))

        self.collect([
            self.get_item_by_name("Long Jump"),
            self.get_item_by_name("Side Flip"),
            self.get_item_by_name("Vertical Wind"),
        ])
        self.assertTrue(self.can_reach_region("Tiny-Huge Island - Koopa the Quick"))
        self.assertFalse(self.can_reach_region("Tiny-Huge Island - Tiny Main"))

        self.collect(self.get_item_by_name("Warp Pipes"))
        self.assertTrue(self.can_reach_region("Tiny-Huge Island - Tiny Main"))

    def test_tiny_huge_island_rematch_accepts_long_jump_route(self):
        self.collect_second_floor_access()
        self.collect([
            self.get_item_by_name("Tiny-Huge Island - Koopa the Quick"),
            self.get_item_by_name("Side Flip"),
            self.get_item_by_name("Vertical Wind"),
        ])
        self.assertFalse(self.can_reach_location("Tiny-Huge Island - Rematch with Koopa the Quick"))

        self.collect(self.get_item_by_name("Long Jump"))
        self.assertTrue(self.can_reach_location("Tiny-Huge Island - Rematch with Koopa the Quick"))

    def test_tiny_huge_island_rematch_accepts_triple_jump_and_dive_route(self):
        self.collect_second_floor_access()
        self.collect([
            self.get_item_by_name("Tiny-Huge Island - Koopa the Quick"),
            self.get_item_by_name("Triple Jump"),
        ])
        self.assertFalse(self.can_reach_location("Tiny-Huge Island - Rematch with Koopa the Quick"))

        self.collect(self.get_item_by_name("Dive"))
        self.assertTrue(self.can_reach_location("Tiny-Huge Island - Rematch with Koopa the Quick"))

    def test_tiny_huge_island_rematch_top_route_does_not_require_moveless(self):
        self.collect_second_floor_access()
        self.collect([
            self.get_item_by_name("Tiny-Huge Island - Koopa the Quick"),
            self.get_item_by_name("Triple Jump"),
            self.get_item_by_name("Dive"),
        ])
        self.assertTrue(self.can_reach_location("Tiny-Huge Island - Rematch with Koopa the Quick"))

    def test_tiny_huge_island_rematch_warp_pipe_route_does_not_require_moveless(self):
        self.multiworld.get_entrance("Second Floor -> Tiny-Huge Island (Huge)", self.player).access_rule = \
            lambda state: False

        self.collect_second_floor_access()
        self.collect([
            self.get_item_by_name("Tiny-Huge Island - Koopa the Quick"),
            self.get_item_by_name("Long Jump"),
            self.get_item_by_name("Purple Switches"),
        ])
        self.assertTrue(self.can_reach_region("Tiny-Huge Island - Tiny Main"))
        self.assertFalse(self.can_reach_location("Tiny-Huge Island - Rematch with Koopa the Quick"))

        self.collect(self.get_item_by_name("Warp Pipes"))
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

        self.collect(self.world.create_item("Glitched Logic"))
        self.assertTrue(self.can_reach_location("Dire, Dire Docks - Board Bowser's Sub"))

    def test_hmc_metal_head_capless_route_requires_purple_switches(self):
        self.collect_basement_access()
        self.collect([
            self.get_item_by_name("Long Jump"),
            self.get_item_by_name("Triple Jump"),
            self.world.create_item("Glitched Logic"),
        ])
        self.assertFalse(self.can_reach_location("Hazy Maze Cave - Metal-Head Mario Can Move!"))

        self.collect(self.world.create_item("Purple Switches"))
        self.assertTrue(self.can_reach_location("Hazy Maze Cave - Metal-Head Mario Can Move!"))

    def test_wet_dry_world_express_elevator_requires_purple_switches_and_access_method(self):
        self.collect_second_floor_access()
        self.assertFalse(self.can_reach_location("Wet-Dry World - Express Elevator--Hurry Up!"))

        self.collect(self.get_item_by_name("Backflip"))
        self.assertFalse(self.can_reach_location("Wet-Dry World - Express Elevator--Hurry Up!"))

        self.collect([
            self.get_item_by_name("Purple Switches"),
            self.get_item_by_name("Wet-Dry World - Cannon Unlock"),
        ])
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
            self.get_item_by_name("Rolling Logs"),
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
            self.get_item_by_name("Rolling Logs"),
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
        self.collect([
            self.get_item_by_name("Long Jump"),
            self.get_item_by_name("Side Flip"),
            self.get_item_by_name("Vertical Wind"),
        ])
        self.assertTrue(self.can_reach_region("Tiny-Huge Island (Huge)"))
        self.assertTrue(self.can_reach_region("Tiny-Huge Island - Koopa the Quick"))
        self.assertFalse(self.can_reach_region("Tiny-Huge Island (Tiny)"))
        self.assertFalse(self.can_reach_location("Tiny-Huge Island - Five Itty Bitty Secrets"))

        self.collect(self.get_item_by_name("Warp Pipes"))
        self.assertTrue(self.can_reach_region("Tiny-Huge Island - Tiny Main"))
        self.assertFalse(self.can_reach_location("Tiny-Huge Island - Five Itty Bitty Secrets"))

        self.collect(self.get_item_by_name("Purple Switches"))
        self.assertTrue(self.can_reach_location("Tiny-Huge Island - Five Itty Bitty Secrets"))

    def test_tiny_huge_island_make_wiggler_requires_warp_pipes(self):
        self.collect_second_floor_access()
        self.collect([
            self.get_item_by_name("Triple Jump"),
            self.get_item_by_name("Dive"),
            self.get_item_by_name("Purple Switches"),
            self.get_item_by_name("Ground Pound"),
        ])
        self.assertTrue(self.can_reach_region("Tiny-Huge Island - Tiny Main"))
        self.assertTrue(self.can_reach_region("Tiny-Huge Island - Huge Top"))
        self.assertFalse(self.can_reach_location("Tiny-Huge Island - Make Wiggler Squirm"))

        self.collect(self.get_item_by_name("Warp Pipes"))
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

        self.collect([
            self.get_item_by_name("Purple Switches"),
            self.get_item_by_name("Warp Pipes"),
        ])
        self.assertTrue(self.can_reach_location("Bowser in the Dark World - Red Coins"))
        self.assertTrue(self.can_reach_location("Bowser in the Dark World - Key"))

    def test_bitdw_triple_jump_without_trick_does_not_bypass_purple_switches(self):
        self.collect(self.get_item_by_name("Dark World Key"))
        self.assertFalse(self.can_reach_location("Bowser in the Dark World - Red Coins"))
        self.assertFalse(self.can_reach_location("Bowser in the Dark World - Key"))

        self.collect(self.get_item_by_name("Triple Jump"))
        self.assertFalse(self.can_reach_location("Bowser in the Dark World - Red Coins"))
        self.assertFalse(self.can_reach_location("Bowser in the Dark World - Key"))

        self.collect(self.world.create_item("Glitched Logic"))
        self.assertFalse(self.can_reach_location("Bowser in the Dark World - Red Coins"))
        self.assertFalse(self.can_reach_location("Bowser in the Dark World - Key"))

        self.collect([
            self.get_item_by_name("Purple Switches"),
            self.get_item_by_name("Warp Pipes"),
        ])
        self.assertTrue(self.can_reach_location("Bowser in the Dark World - Red Coins"))
        self.assertTrue(self.can_reach_location("Bowser in the Dark World - Key"))

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
        self.collect([
            self.get_item_by_name("Triple Jump"),
            self.get_item_by_name("Wing Cap"),
            self.get_item_by_name("Ground Pound"),
        ])
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
        "level_features": Options.LevelFeatures.option_per_level,
        "bobomb_buddies": Options.BobombBuddies.option_per_level,
    }

    def collect_basement_access(self):
        self.collect(self.get_item_by_name("Progressive Basement Key"))

    def test_individual_checkerboard_platforms_accept_global_item(self):
        self.assertFalse(self.can_reach_region("Whomp's Fortress - Top"))

        self.collect(self.world.create_item("Checkerboard Platforms"))
        self.assertTrue(self.can_reach_region("Whomp's Fortress - Top"))

    def test_individual_rolling_logs_accept_global_item(self):
        self.collect_basement_access()
        self.assertFalse(self.can_reach_location("Lethal Lava Land - Red-Hot Log Rolling"))

        self.collect(self.world.create_item("Rolling Logs"))
        self.assertTrue(self.can_reach_location("Lethal Lava Land - Red-Hot Log Rolling"))

    def test_individual_purple_switches_accept_global_item(self):
        self.collect_basement_access()
        self.collect([
            self.get_item_by_name("Long Jump"),
            self.get_item_by_name("Metal Cap"),
        ])
        self.assertFalse(self.can_reach_location("Hazy Maze Cave - Metal-Head Mario Can Move!"))

        self.collect(self.world.create_item("Purple Switches"))
        self.assertTrue(self.can_reach_location("Hazy Maze Cave - Metal-Head Mario Can Move!"))

    def test_dire_dire_docks_uses_individual_purple_switch(self):
        self.collect([
            self.get_item_by_name("Progressive Basement Key"),
            self.get_item_by_name("Progressive Basement Key"),
            self.get_item_by_name("Dire, Dire Docks - Bowser's Sub"),
        ])
        self.assertFalse(self.can_reach_location("Dire, Dire Docks - Board Bowser's Sub"))

        self.collect(self.world.create_item("Purple Switches"))
        self.assertTrue(self.can_reach_location("Dire, Dire Docks - Board Bowser's Sub"))

    def test_tall_tall_mountain_uses_individual_purple_switch(self):
        self.collect([
            self.get_item_by_name("Progressive Upstairs Key"),
            self.get_item_by_name("Tall, Tall Mountain - Rolling Log"),
            self.get_item_by_name("Long Jump"),
            self.get_item_by_name("Kick"),
        ])
        self.assertFalse(self.can_reach_location("Tall, Tall Mountain - Breathtaking View from Bridge"))

        self.collect(self.world.create_item("Purple Switches"))
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
        "level_features": Options.LevelFeatures.option_not_shuffled,
        "bobomb_buddies": Options.BobombBuddies.option_not_shuffled,
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
        self.assertTrue(self.can_reach_region("Hazy Maze Cave - Mid Red Coin Room"))
        self.assertTrue(self.can_reach_region("Hazy Maze Cave - Upper Red Coin Room"))
        self.assertTrue(self.can_reach_location("Hazy Maze Cave - Metal-Head Mario Can Move!"))
        self.assertTrue(self.can_reach_location("Lethal Lava Land - Red-Hot Log Rolling"))


class VanishCapUnderTheMoatIndividualUnlockLogicTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "coin_object_unlocks": Options.CoinObjectUnlocks.option_per_level,
        "level_features": Options.LevelFeatures.option_global,
        "bobomb_buddies": Options.BobombBuddies.option_per_level,
        "cap_items": Options.CapItems.option_per_level,
    }

    def test_initial_coin_sources_are_counted_independently(self):
        source_coins = {
            "Vanish Cap Under the Moat - Horizontal Coin Lines": 5,
            "Vanish Cap Under the Moat - Red Coins": 8,
        }
        self.assertFalse(vanish_cap_under_the_moat_coins(
            self.multiworld.state, self.player, 1))
        for item_name, expected_coins in source_coins.items():
            with self.subTest(item=item_name):
                item = self.get_item_by_name(item_name)
                self.collect(item)
                self.assertTrue(vanish_cap_under_the_moat_coins(
                    self.multiworld.state, self.player, expected_coins))
                self.assertFalse(vanish_cap_under_the_moat_coins(
                    self.multiworld.state, self.player, expected_coins + 1))
                self.remove(item)

    def test_three_coin_block_requires_movement(self):
        self.collect(self.get_item_by_name("Vanish Cap Under the Moat - 3-Coin Block"))
        self.assertFalse(vanish_cap_under_the_moat_coins(
            self.multiworld.state, self.player, 1))

        self.collect(self.get_item_by_name("Triple Jump"))
        self.assertTrue(vanish_cap_under_the_moat_coins(
            self.multiworld.state, self.player, 3))
        self.assertFalse(vanish_cap_under_the_moat_coins(
            self.multiworld.state, self.player, 4))

    def test_upper_red_coins_require_movement_and_checkerboards(self):
        self.collect(self.get_item_by_name("Vanish Cap Under the Moat - Red Coins"))
        self.assertTrue(vanish_cap_under_the_moat_coins(
            self.multiworld.state, self.player, 8))

        self.collect(self.get_item_by_name("Triple Jump"))
        self.assertFalse(vanish_cap_under_the_moat_coins(
            self.multiworld.state, self.player, 9))
        self.collect(self.get_item_by_name("Checkerboard Platforms"))
        self.assertTrue(vanish_cap_under_the_moat_coins(
            self.multiworld.state, self.player, 16))
        self.assertFalse(vanish_cap_under_the_moat_coins(
            self.multiworld.state, self.player, 17))

    def test_end_coins_require_vanish_cap(self):
        self.collect_by_name([
            "Triple Jump",
            "Checkerboard Platforms",
            "Vanish Cap Under the Moat - Single Yellow Coins",
        ])
        self.assertFalse(vanish_cap_under_the_moat_coins(
            self.multiworld.state, self.player, 1))

        self.collect(self.get_item_by_name("Vanish Cap Under the Moat - Vanish Cap"))
        self.assertTrue(vanish_cap_under_the_moat_coins(
            self.multiworld.state, self.player, 3))
        self.assertFalse(vanish_cap_under_the_moat_coins(
            self.multiworld.state, self.player, 4))

    def test_all_unlocks_total_27_coins(self):
        self.collect_by_name([
            "Triple Jump",
            "Checkerboard Platforms",
            "Vanish Cap Under the Moat - Vanish Cap",
            "Vanish Cap Under the Moat - Single Yellow Coins",
            "Vanish Cap Under the Moat - Red Coins",
            "Vanish Cap Under the Moat - Horizontal Coin Lines",
            "Vanish Cap Under the Moat - 3-Coin Block",
        ])
        self.assertTrue(vanish_cap_under_the_moat_coins(
            self.multiworld.state, self.player, 27))


class PrincessSecretSlideIndividualUnlockLogicTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "coin_object_unlocks": Options.CoinObjectUnlocks.option_per_level,
    }

    def test_coin_sources_are_counted_independently(self):
        source_coins = {
            "Princess's Secret Slide - Single Yellow Coins": 20,
            "Princess's Secret Slide - Horizontal Coin Lines": 30,
        }
        self.assertFalse(princess_secret_slide_coins(
            self.multiworld.state, self.player, 1))
        for item_name, expected_coins in source_coins.items():
            with self.subTest(item=item_name):
                item = self.get_item_by_name(item_name)
                self.collect(item)
                self.assertTrue(princess_secret_slide_coins(
                    self.multiworld.state, self.player, expected_coins))
                self.assertFalse(princess_secret_slide_coins(
                    self.multiworld.state, self.player, expected_coins + 1))
                self.remove(item)

    def test_blue_coin_block_requires_ground_pound(self):
        self.collect(self.get_item_by_name("Princess's Secret Slide - Blue Coin Block"))
        self.assertFalse(princess_secret_slide_coins(
            self.multiworld.state, self.player, 1))

        self.collect(self.get_item_by_name("Ground Pound"))
        self.assertTrue(princess_secret_slide_coins(
            self.multiworld.state, self.player, 30))
        self.assertFalse(princess_secret_slide_coins(
            self.multiworld.state, self.player, 31))

    def test_all_unlocks_total_80_coins(self):
        self.collect_by_name([
            "Ground Pound",
            "Princess's Secret Slide - Single Yellow Coins",
            "Princess's Secret Slide - Blue Coin Block",
            "Princess's Secret Slide - Horizontal Coin Lines",
        ])
        self.assertTrue(princess_secret_slide_coins(
            self.multiworld.state, self.player, 80))


class BowserInTheDarkWorldIndividualUnlockLogicTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        "coin_object_unlocks": Options.CoinObjectUnlocks.option_per_level,
        "enemy_unlocks": Options.EnemyUnlocks.option_per_level,
        "level_features": Options.LevelFeatures.option_global,
        "bobomb_buddies": Options.BobombBuddies.option_per_level,
    }

    def test_coin_and_enemy_sources_are_counted_independently(self):
        source_coins = {
            "Bowser in the Dark World - Single Yellow Coins": 18,
            "Bowser in the Dark World - Red Coins": 12,
            "Bowser in the Dark World - Horizontal Coin Lines": 10,
            "Bowser in the Dark World - Horizontal Coin Rings": 24,
            "Bowser in the Dark World - 3-Coin Block": 3,
            "Bowser in the Dark World - Goombas": 6,
        }
        self.assertFalse(bowser_in_the_dark_world_coins(
            self.multiworld.state, self.player, 1))
        for item_name, expected_coins in source_coins.items():
            with self.subTest(item=item_name):
                item = self.get_item_by_name(item_name)
                self.collect(item)
                self.assertTrue(bowser_in_the_dark_world_coins(
                    self.multiworld.state, self.player, expected_coins))
                self.assertFalse(bowser_in_the_dark_world_coins(
                    self.multiworld.state, self.player, expected_coins + 1))
                self.remove(item)

    def test_purple_switches_add_final_seven_coins(self):
        self.collect_by_name([
            "Bowser in the Dark World - Single Yellow Coins",
            "Bowser in the Dark World - Red Coins",
        ])
        self.assertTrue(bowser_in_the_dark_world_coins(
            self.multiworld.state, self.player, 30))
        self.assertFalse(bowser_in_the_dark_world_coins(
            self.multiworld.state, self.player, 31))

        self.collect(self.get_item_by_name("Purple Switches"))
        self.assertTrue(bowser_in_the_dark_world_coins(
            self.multiworld.state, self.player, 37))

    def test_all_unlocks_total_80_coins(self):
        self.collect_by_name([
            "Purple Switches",
            "Bowser in the Dark World - Single Yellow Coins",
            "Bowser in the Dark World - Red Coins",
            "Bowser in the Dark World - Horizontal Coin Lines",
            "Bowser in the Dark World - Horizontal Coin Rings",
            "Bowser in the Dark World - 3-Coin Block",
            "Bowser in the Dark World - Goombas",
        ])
        self.assertTrue(bowser_in_the_dark_world_coins(
            self.multiworld.state, self.player, 80))


class BowserInTheDarkWorldSlopeTrickTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        "coin_object_unlocks": Options.CoinObjectUnlocks.option_per_level,
        "enemy_unlocks": Options.EnemyUnlocks.option_per_level,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "logic_tricks": {"Bowser in the Dark World Triple Jump up the Purple Switch Slope"},
        "level_features": Options.LevelFeatures.option_per_level,
        "bobomb_buddies": Options.BobombBuddies.option_per_level,
    }

    def collect_stage_access(self):
        self.collect_by_name([
            "Dark World Key",
            "Bowser in the Dark World - Warp Pipes",
        ])

    def test_trick_reaches_bowser_but_not_red_coin_star(self):
        self.collect_stage_access()
        self.collect_by_name([
            "Triple Jump",
            "Bowser in the Dark World - Bowser",
            "Bowser in the Dark World - Red Coins",
        ])
        self.assertTrue(self.can_reach_location("Bowser in the Dark World - Key"))
        self.assertFalse(self.can_reach_location("Bowser in the Dark World - Red Coins"))

    def test_trick_adds_only_three_slope_coins(self):
        self.collect_by_name([
            "Triple Jump",
            "Bowser in the Dark World - Single Yellow Coins",
        ])
        self.assertTrue(bowser_in_the_dark_world_coins(
            self.multiworld.state, self.player, 21))
        self.assertFalse(bowser_in_the_dark_world_coins(
            self.multiworld.state, self.player, 22))

        self.collect(self.get_item_by_name("Bowser in the Dark World - Red Coins"))
        self.assertTrue(bowser_in_the_dark_world_coins(
            self.multiworld.state, self.player, 33))
        self.assertFalse(bowser_in_the_dark_world_coins(
            self.multiworld.state, self.player, 34))


class SecretAquariumIndividualUnlockLogicTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        "coin_object_unlocks": Options.CoinObjectUnlocks.option_per_level,
    }

    def test_coin_sources_are_counted_independently(self):
        source_coins = {
            "Secret Aquarium - Red Coins": 16,
            "Secret Aquarium - Horizontal Coin Rings": 8,
            "Secret Aquarium - Vertical Coin Rings": 32,
        }
        self.assertFalse(secret_aquarium_coins(
            self.multiworld.state, self.player, 1))
        for item_name, expected_coins in source_coins.items():
            with self.subTest(item=item_name):
                item = self.get_item_by_name(item_name)
                self.collect(item)
                self.assertTrue(secret_aquarium_coins(
                    self.multiworld.state, self.player, expected_coins))
                self.assertFalse(secret_aquarium_coins(
                    self.multiworld.state, self.player, expected_coins + 1))
                self.remove(item)

    def test_all_unlocks_total_56_coins(self):
        self.collect_by_name([
            "Secret Aquarium - Red Coins",
            "Secret Aquarium - Horizontal Coin Rings",
            "Secret Aquarium - Vertical Coin Rings",
        ])
        self.assertTrue(secret_aquarium_coins(
            self.multiworld.state, self.player, 56))


class VanishCapUnderTheMoatTrickAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "blocksanity": Options.Blocksanity.option_true,
        "level_features": Options.LevelFeatures.option_global,
        "bobomb_buddies": Options.BobombBuddies.option_per_level,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "level_unlocks": Options.LevelUnlocks.option_special_only,
        "logic_tricks": {"Vanish Cap Under the Moat Wall Kick over the Vanish Cap Grate"},
        "one_up_checks": Options.OneUpChecks.option_true,
        "cap_items": Options.CapItems.option_per_level,
    }

    def collect_stage_access(self):
        self.collect_by_name([
            "Progressive Basement Key",
            "Cap Switches",
            "Unlock Vanish Cap Under the Moat",
        ])

    def test_wall_kick_trick_bypasses_vanish_cap(self):
        self.collect_stage_access()
        self.collect_by_name([
            "Checkerboard Platforms",
            "Wall Kick",
        ])
        self.assertTrue(self.can_reach_location("Vanish Cap Under the Moat - Red Coins"))
        self.assertTrue(self.can_reach_location(
            "Vanish Cap Under the Moat - Red Coin Platform 1-Up"))

    def test_near_switch_block_copies_switch_access_and_requires_vanish_cap(self):
        self.collect_stage_access()
        self.collect(self.get_item_by_name("Vanish Cap Under the Moat - Vanish Cap"))
        self.assertFalse(self.can_reach_location(
            "Vanish Cap Under the Moat - Near Switch Vanish Cap Block"))

        self.collect(self.get_item_by_name("Checkerboard Platforms"))
        self.assertFalse(self.can_reach_location(
            "Vanish Cap Under the Moat - Near Switch Vanish Cap Block"))

        self.collect(self.get_item_by_name("Triple Jump"))
        self.assertTrue(self.can_reach_location("Vanish Cap Under the Moat - Switch"))
        self.assertTrue(self.can_reach_location(
            "Vanish Cap Under the Moat - Near Switch Vanish Cap Block"))


class VanishCapUnderTheMoatDropTrickTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "coin_object_unlocks": Options.CoinObjectUnlocks.option_per_level,
        "level_features": Options.LevelFeatures.option_global,
        "bobomb_buddies": Options.BobombBuddies.option_per_level,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "level_unlocks": Options.LevelUnlocks.option_special_only,
        "logic_tricks": {"Vanish Cap Under the Moat Drop to Checkerboard Platforms From Above"},
        "one_up_checks": Options.OneUpChecks.option_true,
        "cap_items": Options.CapItems.option_per_level,
    }

    def collect_all_coin_sources(self):
        self.collect_by_name([
            "Checkerboard Platforms",
            "Vanish Cap Under the Moat - Vanish Cap",
            "Vanish Cap Under the Moat - Single Yellow Coins",
            "Vanish Cap Under the Moat - Red Coins",
            "Vanish Cap Under the Moat - Horizontal Coin Lines",
            "Vanish Cap Under the Moat - 3-Coin Block",
        ])

    def test_drop_counts_only_better_side_of_drop(self):
        self.collect_all_coin_sources()
        self.assertTrue(vanish_cap_under_the_moat_coins(
            self.multiworld.state, self.player, 14))
        self.assertFalse(vanish_cap_under_the_moat_coins(
            self.multiworld.state, self.player, 15))

    def test_drop_bypasses_movement_for_red_coin_checks(self):
        self.collect_by_name([
            "Unlock Vanish Cap Under the Moat",
            "Checkerboard Platforms",
            "Vanish Cap Under the Moat - Vanish Cap",
        ])
        self.assertTrue(self.can_reach_location(
            "Vanish Cap Under the Moat - Red Coin Platform 1-Up"))
        self.assertFalse(self.can_reach_location("Vanish Cap Under the Moat - Red Coins"))

        self.collect(self.get_item_by_name("Vanish Cap Under the Moat - Red Coins"))
        self.assertFalse(self.can_reach_location("Vanish Cap Under the Moat - Red Coins"))


class VanishCapUnderTheMoatCrawlBackDropTrickTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "coin_object_unlocks": Options.CoinObjectUnlocks.option_per_level,
        "level_features": Options.LevelFeatures.option_global,
        "bobomb_buddies": Options.BobombBuddies.option_per_level,
        "logic_tricks": {
            "Vanish Cap Under the Moat Drop to Checkerboard Platforms From Above After Crawling Back Up the Slide"
        },
        "cap_items": Options.CapItems.option_per_level,
    }

    def test_crawl_back_then_drop_counts_both_sides(self):
        self.collect_by_name([
            "Checkerboard Platforms",
            "Vanish Cap Under the Moat - Vanish Cap",
            "Vanish Cap Under the Moat - Single Yellow Coins",
            "Vanish Cap Under the Moat - Red Coins",
            "Vanish Cap Under the Moat - Horizontal Coin Lines",
            "Vanish Cap Under the Moat - 3-Coin Block",
        ])
        self.assertTrue(vanish_cap_under_the_moat_coins(
            self.multiworld.state, self.player, 27))


class BowserInTheSkyCoinCountChecksAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_ARBITRARY_FEATURE_OPTIONS,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "level_unlocks": Options.LevelUnlocks.option_special_only,
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
                "coin_count_checks": 100,
    }

    def collect_bowser_in_the_sky_access(self):
        self.collect([self.get_item_by_name("Progressive Upstairs Key")] * 3)

    def test_bowser_in_the_sky_coin_sources(self):
        self.collect_bowser_in_the_sky_access()
        self.assertTrue(self.can_reach_location("Bowser in the Sky - 27 Coins"))
        self.assertFalse(self.can_reach_location("Bowser in the Sky - 28 Coins"))

        self.collect(self.get_item_by_name("Ground Pound"))
        self.assertTrue(self.can_reach_location("Bowser in the Sky - 32 Coins"))
        self.assertFalse(self.can_reach_location("Bowser in the Sky - 33 Coins"))

        self.collect(self.get_item_by_name("Side Flip"))
        self.assertTrue(self.can_reach_region("Bowser in the Sky - Chuckya"))
        self.assertTrue(self.can_reach_location("Bowser in the Sky - 43 Coins"))
        self.assertFalse(self.can_reach_location("Bowser in the Sky - 44 Coins"))

        self.collect(self.get_item_by_name("Purple Switches"))
        self.assertTrue(self.can_reach_region("Bowser in the Sky - Arrow Ride"))
        self.assertTrue(self.can_reach_location("Bowser in the Sky - 60 Coins"))
        self.assertFalse(self.can_reach_location("Bowser in the Sky - 61 Coins"))

        self.collect(self.get_item_by_name("Climb"))
        self.assertTrue(self.can_reach_region("Bowser in the Sky - Top"))
        self.assertTrue(self.can_reach_location("Bowser in the Sky - 76 Coins"))


class BowserInTheSkyIndividualUnlockLogicTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_ARBITRARY_FEATURE_OPTIONS,
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "coin_object_unlocks": Options.CoinObjectUnlocks.option_per_level,
        "level_unlocks": Options.LevelUnlocks.option_special_only,
        "enemy_unlocks": Options.EnemyUnlocks.option_per_level,
            }

    def collect_full_bowser_in_the_sky_route(self):
        self.collect([self.get_item_by_name("Progressive Upstairs Key")] * 3)
        self.collect_by_name([
            "Ground Pound",
            "Side Flip",
            "Climb",
            "Purple Switches",
        ])
        self.assertTrue(self.can_reach_region("Bowser in the Sky - Top"))

    def test_each_unlock_matches_documented_total(self):
        self.collect_full_bowser_in_the_sky_route()
        source_coins = {
            "Bowser in the Sky - Single Yellow Coins": 12,
            "Bowser in the Sky - Red Coins": 16,
            "Bowser in the Sky - Horizontal Coin Lines": 20,
            "Bowser in the Sky - Bob-ombs": 4,
            "Bowser in the Sky - Chuckya": 5,
            "Bowser in the Sky - Fire Piranha Plants": 2,
            "Bowser in the Sky - Goombas": 7,
            "Bowser in the Sky - Whomp": 10,
        }
        for item_name, expected_coins in source_coins.items():
            with self.subTest(item=item_name):
                item = self.get_item_by_name(item_name)
                self.collect(item)
                self.assertTrue(bowser_in_the_sky_coins(
                    self.multiworld.state, self.player, expected_coins))
                self.assertFalse(bowser_in_the_sky_coins(
                    self.multiworld.state, self.player, expected_coins + 1))
                self.remove(item)

    def test_whomp_ground_pound_adds_second_five_coins(self):
        self.collect([self.get_item_by_name("Progressive Upstairs Key")] * 3)
        self.collect(self.get_item_by_name("Bowser in the Sky - Whomp"))
        self.assertTrue(bowser_in_the_sky_coins(
            self.multiworld.state, self.player, 5))
        self.assertFalse(bowser_in_the_sky_coins(
            self.multiworld.state, self.player, 6))

        self.collect(self.get_item_by_name("Ground Pound"))
        self.assertTrue(bowser_in_the_sky_coins(
            self.multiworld.state, self.player, 10))

    def test_all_unlocks_total_76_coins(self):
        self.collect_full_bowser_in_the_sky_route()
        self.collect([
            self.get_item_by_name("Bowser in the Sky - Single Yellow Coins"),
            self.get_item_by_name("Bowser in the Sky - Red Coins"),
            self.get_item_by_name("Bowser in the Sky - Horizontal Coin Lines"),
            self.get_item_by_name("Bowser in the Sky - Bob-ombs"),
            self.get_item_by_name("Bowser in the Sky - Chuckya"),
            self.get_item_by_name("Bowser in the Sky - Fire Piranha Plants"),
            self.get_item_by_name("Bowser in the Sky - Goombas"),
            self.get_item_by_name("Bowser in the Sky - Whomp"),
        ])
        self.assertTrue(bowser_in_the_sky_coins(
            self.multiworld.state, self.player, 76))


class BowserInTheFireSeaCoinCountChecksAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "level_unlocks": Options.LevelUnlocks.option_special_only,
                "coin_count_checks": 100,
    }

    def collect_bowser_in_the_fire_sea_access(self):
        self.collect([self.get_item_by_name("Progressive Basement Key")] * 2)
        self.collect(self.get_item_by_name("Unlock Bowser in the Fire Sea"))

    def test_bowser_in_the_fire_sea_coin_sources(self):
        self.collect_bowser_in_the_fire_sea_access()
        self.assertTrue(self.can_reach_location("Bowser in the Fire Sea - 21 Coins"))
        self.assertFalse(self.can_reach_location("Bowser in the Fire Sea - 22 Coins"))

        self.collect(self.get_item_by_name("Climb"))
        self.assertTrue(self.can_reach_location("Bowser in the Fire Sea - 80 Coins"))


class BowserInTheFireSeaLavaDamageBoostingTrickTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "logic_tricks": {"Lava Damage Boosting"},
        "marios_hat": True,
    }

    def test_lava_damage_boosting_reaches_only_marked_three_coins(self):
        self.collect(self.get_item_by_name("Mario's Hat"))
        self.assertTrue(bowser_in_the_fire_sea_coins(
            self.multiworld.state, self.player, 26))
        self.assertFalse(bowser_in_the_fire_sea_coins(
            self.multiworld.state, self.player, 27))


class BowserInTheFireSeaIndividualUnlockLogicTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "coin_object_unlocks": Options.CoinObjectUnlocks.option_per_level,
        "enemy_unlocks": Options.EnemyUnlocks.option_per_level,
    }

    def test_each_unlock_matches_documented_total_with_climb(self):
        self.collect(self.get_item_by_name("Climb"))
        source_coins = {
            "Bowser in the Fire Sea - Single Yellow Coins": 2,
            "Bowser in the Fire Sea - Red Coins": 16,
            "Bowser in the Fire Sea - Horizontal Coin Lines": 20,
            "Bowser in the Fire Sea - Horizontal Coin Rings": 16,
            "Bowser in the Fire Sea - Vertical Coin Lines": 5,
            "Bowser in the Fire Sea - 3-Coin Block": 3,
            "Bowser in the Fire Sea - 10-Coin Block": 10,
            "Bowser in the Fire Sea - Bob-omb": 1,
            "Bowser in the Fire Sea - Bullies": 4,
            "Bowser in the Fire Sea - Goombas": 3,
        }
        for item_name, expected_coins in source_coins.items():
            with self.subTest(item=item_name):
                item = self.get_item_by_name(item_name)
                self.collect(item)
                self.assertTrue(bowser_in_the_fire_sea_coins(
                    self.multiworld.state, self.player, expected_coins))
                self.assertFalse(bowser_in_the_fire_sea_coins(
                    self.multiworld.state, self.player, expected_coins + 1))
                self.remove(item)

    def test_three_coin_block_requires_climb_without_trick(self):
        self.collect(self.get_item_by_name("Bowser in the Fire Sea - 3-Coin Block"))
        self.assertFalse(bowser_in_the_fire_sea_coins(
            self.multiworld.state, self.player, 1))

        self.collect(self.get_item_by_name("Climb"))
        self.assertTrue(bowser_in_the_fire_sea_coins(
            self.multiworld.state, self.player, 3))

    def test_all_unlocks_total_80_coins(self):
        self.collect_by_name([
            "Climb",
            "Bowser in the Fire Sea - Single Yellow Coins",
            "Bowser in the Fire Sea - Red Coins",
            "Bowser in the Fire Sea - Horizontal Coin Lines",
            "Bowser in the Fire Sea - Horizontal Coin Rings",
            "Bowser in the Fire Sea - Vertical Coin Lines",
            "Bowser in the Fire Sea - 3-Coin Block",
            "Bowser in the Fire Sea - 10-Coin Block",
            "Bowser in the Fire Sea - Bob-omb",
            "Bowser in the Fire Sea - Bullies",
            "Bowser in the Fire Sea - Goombas",
        ])
        self.assertTrue(bowser_in_the_fire_sea_coins(
            self.multiworld.state, self.player, 80))


class CavernOfTheMetalCapDeepUnderwaterCoinsTrickTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_ARBITRARY_FEATURE_OPTIONS,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "level_unlocks": Options.LevelUnlocks.option_special_only,
        "logic_tricks": {"Deep Underwater Coins Without Metal Cap"},
    }

    def collect_stage_access(self):
        self.collect_by_name([
            "Progressive Basement Key",
            "Hazy Maze Cave - Swimming Beast",
        ])

    def test_trick_reaches_red_coin_star_without_metal_cap(self):
        self.collect_stage_access()
        self.assertTrue(self.can_reach_location("Cavern of the Metal Cap - Red Coins"))

    def test_trick_reaches_deep_underwater_coins_without_metal_cap(self):
        self.assertTrue(cavern_of_the_metal_cap_coins(
            self.multiworld.state, self.player, 47))


class CavernOfTheMetalCapCoinLogicTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        "cap_items": Options.CapItems.option_per_level,
    }

    def test_deep_underwater_coins_require_metal_cap_without_trick(self):
        self.assertTrue(cavern_of_the_metal_cap_coins(
            self.multiworld.state, self.player, 26))
        self.assertFalse(cavern_of_the_metal_cap_coins(
            self.multiworld.state, self.player, 27))

        self.collect(self.get_item_by_name("Cavern of the Metal Cap - Metal Cap"))
        self.assertTrue(cavern_of_the_metal_cap_coins(
            self.multiworld.state, self.player, 47))


class CavernOfTheMetalCapIndividualUnlockLogicTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        "coin_object_unlocks": Options.CoinObjectUnlocks.option_per_level,
        "enemy_unlocks": Options.EnemyUnlocks.option_per_level,
        "cap_items": Options.CapItems.option_per_level,
    }

    def test_unlocks_without_metal_cap(self):
        source_coins = {
            "Cavern of the Metal Cap - Red Coins": 8,
            "Cavern of the Metal Cap - Horizontal Coin Lines": 10,
            "Cavern of the Metal Cap - Snufits": 8,
        }
        for item_name, expected_coins in source_coins.items():
            with self.subTest(item=item_name):
                item = self.get_item_by_name(item_name)
                self.collect(item)
                self.assertTrue(cavern_of_the_metal_cap_coins(
                    self.multiworld.state, self.player, expected_coins))
                self.assertFalse(cavern_of_the_metal_cap_coins(
                    self.multiworld.state, self.player, expected_coins + 1))
                self.remove(item)

        self.collect(self.get_item_by_name("Cavern of the Metal Cap - Horizontal Coin Rings"))
        self.assertFalse(cavern_of_the_metal_cap_coins(
            self.multiworld.state, self.player, 1))

    def test_unlocks_with_metal_cap_match_documented_totals(self):
        self.collect(self.get_item_by_name("Cavern of the Metal Cap - Metal Cap"))
        source_coins = {
            "Cavern of the Metal Cap - Red Coins": 16,
            "Cavern of the Metal Cap - Horizontal Coin Lines": 15,
            "Cavern of the Metal Cap - Horizontal Coin Rings": 8,
            "Cavern of the Metal Cap - Snufits": 8,
        }
        for item_name, expected_coins in source_coins.items():
            with self.subTest(item=item_name):
                item = self.get_item_by_name(item_name)
                self.collect(item)
                self.assertTrue(cavern_of_the_metal_cap_coins(
                    self.multiworld.state, self.player, expected_coins))
                self.assertFalse(cavern_of_the_metal_cap_coins(
                    self.multiworld.state, self.player, expected_coins + 1))
                self.remove(item)

    def test_all_unlocks_total_47_coins(self):
        self.collect_by_name([
            "Cavern of the Metal Cap - Metal Cap",
            "Cavern of the Metal Cap - Red Coins",
            "Cavern of the Metal Cap - Horizontal Coin Lines",
            "Cavern of the Metal Cap - Horizontal Coin Rings",
            "Cavern of the Metal Cap - Snufits",
        ])
        self.assertTrue(cavern_of_the_metal_cap_coins(
            self.multiworld.state, self.player, 47))


class WingMarioOverTheRainbowCoinCountChecksAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "level_unlocks": Options.LevelUnlocks.option_special_only,
        "buddy_checks": Options.BuddyChecks.option_true,
                "coin_count_checks": 100,
    }

    def collect_wing_mario_over_the_rainbow_access(self):
        self.collect([self.get_item_by_name("Progressive Upstairs Key")] * 3)
        self.collect(self.get_item_by_name("Side Flip"))

    def test_long_jump_fallback_coins_do_not_use_capless(self):
        self.collect_wing_mario_over_the_rainbow_access()
        self.assertTrue(self.can_reach_location("Wing Mario Over the Rainbow - 2 Coins"))
        self.assertFalse(self.can_reach_location("Wing Mario Over the Rainbow - 3 Coins"))

        self.collect(self.get_item_by_name("Long Jump"))
        self.assertFalse(self.can_reach_location("Wing Mario Over the Rainbow - 3 Coins"))

        self.collect(self.world.create_item("Glitched Logic"))
        self.assertFalse(self.can_reach_location("Wing Mario Over the Rainbow - 3 Coins"))

    def test_wing_cap_fallback_coins_do_not_use_moveless(self):
        self.collect_wing_mario_over_the_rainbow_access()
        self.assertTrue(self.can_reach_location("Wing Mario Over the Rainbow - 2 Coins"))
        self.assertFalse(self.can_reach_location("Wing Mario Over the Rainbow - 3 Coins"))

        self.collect(self.get_item_by_name("Wing Cap"))
        self.assertFalse(self.can_reach_location("Wing Mario Over the Rainbow - 3 Coins"))

        self.collect(self.world.create_item("Glitched Logic"))
        self.assertFalse(self.can_reach_location("Wing Mario Over the Rainbow - 3 Coins"))

    def test_wing_cap_does_not_enable_long_jump_trick_without_trick_option(self):
        self.collect_wing_mario_over_the_rainbow_access()
        self.collect(self.get_item_by_name("Long Jump"))
        self.collect(self.world.create_item("Glitched Logic"))
        self.assertFalse(self.can_reach_location("Wing Mario Over the Rainbow - 3 Coins"))

        self.collect(self.get_item_by_name("Wing Cap"))
        self.assertFalse(self.can_reach_location("Wing Mario Over the Rainbow - 3 Coins"))

    def test_cannon_coin_route_requires_cannon_movement(self):
        self.collect_wing_mario_over_the_rainbow_access()
        self.collect([
            self.get_item_by_name("Wing Cap"),
            self.get_item_by_name("Wing Mario Over the Rainbow - Cannon Unlock"),
        ])
        self.assertFalse(self.can_reach_location("Wing Mario Over the Rainbow - 7 Coins"))

        self.collect(self.get_item_by_name("Triple Jump"))
        self.assertTrue(self.can_reach_location("Wing Mario Over the Rainbow - 56 Coins"))

    def test_cannon_coin_route_does_not_use_capless_long_jump(self):
        self.collect_wing_mario_over_the_rainbow_access()
        self.collect([
            self.get_item_by_name("Wing Cap"),
            self.get_item_by_name("Wing Mario Over the Rainbow - Cannon Unlock"),
            self.get_item_by_name("Long Jump"),
        ])
        self.assertFalse(self.can_reach_location("Wing Mario Over the Rainbow - 56 Coins"))

        self.collect(self.world.create_item("Glitched Logic"))
        self.assertFalse(self.can_reach_location("Wing Mario Over the Rainbow - 56 Coins"))


class WingMarioOverTheRainbowLeapOfFaithTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **WingMarioOverTheRainbowCoinCountChecksAccessTestBase.options,
        "logic_tricks": {"Wing Mario Over the Rainbow Leap of Faith"},
    }

    def collect_wing_mario_over_the_rainbow_access(self):
        self.collect([self.get_item_by_name("Progressive Upstairs Key")] * 3)
        self.collect(self.get_item_by_name("Side Flip"))

    def test_long_jump_coins_add_ledge_grab_for_second_coin(self):
        self.collect_wing_mario_over_the_rainbow_access()
        self.collect(self.get_item_by_name("Long Jump"))
        self.assertTrue(self.can_reach_location("Wing Mario Over the Rainbow - 4 Coins"))
        self.assertFalse(self.can_reach_location("Wing Mario Over the Rainbow - 5 Coins"))

        self.collect(self.get_item_by_name("Ledge Grab"))
        self.assertTrue(self.can_reach_location("Wing Mario Over the Rainbow - 6 Coins"))
        self.assertFalse(self.can_reach_location("Wing Mario Over the Rainbow - 7 Coins"))

    def test_buddy_platform_requires_ledge_grab(self):
        self.collect_wing_mario_over_the_rainbow_access()
        self.collect(self.get_item_by_name("Long Jump"))
        self.assertFalse(self.can_reach_region("Wing Mario Over the Rainbow - Bob-omb Buddy Platform"))

        self.collect(self.get_item_by_name("Ledge Grab"))
        self.assertTrue(self.can_reach_region("Wing Mario Over the Rainbow - Bob-omb Buddy Platform"))

    def test_wing_cap_fallback_uses_trick(self):
        self.collect_wing_mario_over_the_rainbow_access()
        self.collect(self.get_item_by_name("Wing Cap"))
        self.assertTrue(self.can_reach_location("Wing Mario Over the Rainbow - 4 Coins"))
        self.assertFalse(self.can_reach_location("Wing Mario Over the Rainbow - 5 Coins"))


class WingMarioOverTheRainbowLeapWithoutLedgeGrabTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **WingMarioOverTheRainbowCoinCountChecksAccessTestBase.options,
        "logic_tricks": {"Wing Mario Over the Rainbow Leap of Faith Without Ledge Grab"},
    }

    def collect_wing_mario_over_the_rainbow_access(self):
        self.collect([self.get_item_by_name("Progressive Upstairs Key")] * 3)
        self.collect(self.get_item_by_name("Side Flip"))

    def test_long_jump_reaches_both_fallback_red_coins(self):
        self.collect_wing_mario_over_the_rainbow_access()
        self.collect(self.get_item_by_name("Long Jump"))
        self.assertTrue(self.can_reach_location("Wing Mario Over the Rainbow - 6 Coins"))
        self.assertFalse(self.can_reach_location("Wing Mario Over the Rainbow - 7 Coins"))
        self.assertTrue(self.can_reach_region("Wing Mario Over the Rainbow - Bob-omb Buddy Platform"))


class WingMarioOverTheRainbowIndividualUnlockLogicTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "level_unlocks": Options.LevelUnlocks.option_special_only,
                "coin_object_unlocks": Options.CoinObjectUnlocks.option_per_level,
        "coin_count_checks": 100,
    }

    def collect_full_wmotr_route(self):
        self.collect([self.get_item_by_name("Progressive Upstairs Key")] * 3)
        self.collect_by_name([
            "Side Flip",
            "Triple Jump",
            "Wing Cap",
            "Wing Mario Over the Rainbow - Cannon Unlock",
        ])
        self.assertTrue(self.can_reach_region("Wing Mario Over the Rainbow - Cannon"))

    def test_each_coin_object_unlock_matches_documented_total(self):
        self.collect_full_wmotr_route()
        for item_name, expected_coins in {
            "Wing Mario Over the Rainbow - Red Coins": 16,
            "Wing Mario Over the Rainbow - Horizontal Coin Rings": 8,
            "Wing Mario Over the Rainbow - Vertical Coin Rings": 32,
        }.items():
            item = self.get_item_by_name(item_name)
            self.collect(item)
            self.assertTrue(self.multiworld.state.has(item_name, self.player))
            self.assertTrue(wing_mario_over_the_rainbow_coins(
                self.multiworld.state, self.player, expected_coins))
            self.assertFalse(wing_mario_over_the_rainbow_coins(
                self.multiworld.state, self.player, expected_coins + 1))
            self.remove(item)

    def test_all_unlocks_total_56_coins(self):
        self.collect_full_wmotr_route()
        self.collect([
            self.get_item_by_name("Wing Mario Over the Rainbow - Red Coins"),
            self.get_item_by_name("Wing Mario Over the Rainbow - Horizontal Coin Rings"),
            self.get_item_by_name("Wing Mario Over the Rainbow - Vertical Coin Rings"),
        ])
        self.assertTrue(self.multiworld.state.has(
            "Wing Mario Over the Rainbow - Red Coins", self.player))
        self.assertTrue(wing_mario_over_the_rainbow_coins(
            self.multiworld.state, self.player, 56))


class TowerOfTheWingCapIndividualUnlockLogicTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        "coin_object_unlocks": Options.CoinObjectUnlocks.option_per_level,
        "coin_count_checks": 100,
        "tower_of_the_wing_cap_coin_count_max_coins": 63,
    }

    def test_each_coin_object_unlock_matches_documented_total(self):
        for item_name, expected_coins in {
            "Tower of the Wing Cap - Single Yellow Coins": 15,
            "Tower of the Wing Cap - Red Coins": 16,
            "Tower of the Wing Cap - Vertical Coin Rings": 20,
        }.items():
            item = self.get_item_by_name(item_name)
            self.collect(item)
            self.assertTrue(tower_of_the_wing_cap_coins(
                self.multiworld.state, self.player, expected_coins))
            self.assertFalse(tower_of_the_wing_cap_coins(
                self.multiworld.state, self.player, expected_coins + 1))
            self.remove(item)

    def test_all_unlocks_reach_all_capless_coins_without_mastery(self):
        self.collect([
            self.get_item_by_name("Tower of the Wing Cap - Single Yellow Coins"),
            self.get_item_by_name("Tower of the Wing Cap - Red Coins"),
            self.get_item_by_name("Tower of the Wing Cap - Vertical Coin Rings"),
        ])
        self.assertTrue(tower_of_the_wing_cap_coins(
            self.multiworld.state, self.player, 51))
        self.assertFalse(tower_of_the_wing_cap_coins(
            self.multiworld.state, self.player, 52))


class TowerOfTheWingCapCoinMasteryLogicTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        "coin_object_unlocks": Options.CoinObjectUnlocks.option_per_level,
        "coin_count_checks": 100,
        "cap_items": Options.CapItems.option_global,
        "tower_of_the_wing_cap_coin_count_max_coins": 63,
    }

    def test_coin_rings_require_wing_cap_for_last_12_coins(self):
        self.collect(self.get_item_by_name("Tower of the Wing Cap - Vertical Coin Rings"))
        self.assertTrue(tower_of_the_wing_cap_coins(
            self.multiworld.state, self.player, 20))
        self.assertFalse(tower_of_the_wing_cap_coins(
            self.multiworld.state, self.player, 21))

        self.collect(self.get_item_by_name("Wing Cap"))
        self.assertTrue(tower_of_the_wing_cap_coins(
            self.multiworld.state, self.player, 32))

    def test_all_unlocks_reach_51_without_wing_cap_and_63_with_it(self):
        self.collect([
            self.get_item_by_name("Tower of the Wing Cap - Single Yellow Coins"),
            self.get_item_by_name("Tower of the Wing Cap - Red Coins"),
            self.get_item_by_name("Tower of the Wing Cap - Vertical Coin Rings"),
        ])
        self.assertTrue(tower_of_the_wing_cap_coins(
            self.multiworld.state, self.player, 51))
        self.assertFalse(tower_of_the_wing_cap_coins(
            self.multiworld.state, self.player, 52))

        self.collect(self.get_item_by_name("Wing Cap"))
        self.assertTrue(tower_of_the_wing_cap_coins(
            self.multiworld.state, self.player, 63))


class TowerOfTheWingCapPermanentCoinsLogicTestBase(TowerOfTheWingCapCoinMasteryLogicTestBase):
    options = {
        **TowerOfTheWingCapCoinMasteryLogicTestBase.options,
        "logic_tricks": set(),
    }


class CoolCoolMountainCoinStarAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_ARBITRARY_FEATURE_OPTIONS,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "buddy_checks": Options.BuddyChecks.option_true,
        "level_unlocks": Options.LevelUnlocks.option_special_only,
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
            }


class CoolCoolMountainIndividualUnlockLogicTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "buddy_checks": Options.BuddyChecks.option_true,
        "coin_object_unlocks": Options.CoinObjectUnlocks.option_per_level,
        "enemy_unlocks": Options.EnemyUnlocks.option_per_level,
    }

    def test_initial_coin_sources_are_counted_independently(self):
        source_coins = {
            "Cool, Cool Mountain - Single Yellow Coins": 27,
            "Cool, Cool Mountain - Red Coins": 16,
            "Cool, Cool Mountain - Single Blue Coin": 5,
            "Cool, Cool Mountain - Horizontal Coin Lines": 65,
            "Cool, Cool Mountain - Vertical Coin Lines": 5,
            "Cool, Cool Mountain - Mr Blizzards": 3,
            "Cool, Cool Mountain - Spindrifts": 9,
        }
        for item_name, expected_coins in source_coins.items():
            with self.subTest(item=item_name):
                state = CollectionState(self.multiworld)
                state.collect(self.world.create_item(item_name), prevent_sweep=True)

                class BothAreasReachableState:
                    def can_reach(self, spot, *args, **kwargs):
                        return getattr(spot, "name", spot) in {
                            "Cool, Cool Mountain",
                            "Cool, Cool Mountain - Secret Slide",
                        }

                    def __getattr__(self, name):
                        return getattr(state, name)

                actual_coins = COIN_EVALUATORS["Cool, Cool Mountain"](
                    BothAreasReachableState(), self.player, 154).reachable_coins
                self.assertEqual(expected_coins, actual_coins)

    def test_wall_kicks_route_sources(self):
        self.collect(self.get_item_by_name("Cool, Cool Mountain - Cannon Unlock"))

        coin_arrow = self.get_item_by_name("Cool, Cool Mountain - Coin Arrows")
        self.collect(coin_arrow)
        self.assertTrue(cool_cool_mountain_coins(self.multiworld.state, self.player, 8))
        self.assertFalse(cool_cool_mountain_coins(self.multiworld.state, self.player, 9))
        self.remove(coin_arrow)

        self.collect(self.get_item_by_name("Cool, Cool Mountain - Spindrifts"))
        self.assertTrue(cool_cool_mountain_coins(self.multiworld.state, self.player, 15))
        self.assertFalse(cool_cool_mountain_coins(self.multiworld.state, self.player, 16))

    def test_blue_coin_switch_requires_ground_pound(self):
        self.collect(self.get_item_by_name("Cool, Cool Mountain - Blue Coin Block"))
        self.assertFalse(cool_cool_mountain_coins(self.multiworld.state, self.player, 1))
        self.collect(self.get_item_by_name("Ground Pound"))
        self.assertTrue(cool_cool_mountain_coins(self.multiworld.state, self.player, 10))
        self.assertFalse(cool_cool_mountain_coins(self.multiworld.state, self.player, 11))

    def test_red_coin_star_requires_red_coins(self):
        self.assertFalse(self.can_reach_location("Cool, Cool Mountain - Frosty Slide for 8 Red Coins"))
        self.collect(self.get_item_by_name("Cool, Cool Mountain - Red Coins"))
        self.assertTrue(self.can_reach_location("Cool, Cool Mountain - Frosty Slide for 8 Red Coins"))


class CoolCoolMountainSpinJumpUnlockLogicTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "buddy_checks": Options.BuddyChecks.option_true,
        "coin_object_unlocks": Options.CoinObjectUnlocks.option_per_level,
        "enemy_unlocks": Options.EnemyUnlocks.option_per_level,
        "logic_tricks": {"Cool, Cool Mountain Wall Kicks Will Work With Spin Jump"},
    }

    def test_spin_jump_trick_requires_spindrifts(self):
        self.assertFalse(self.can_reach_location("Cool, Cool Mountain - Wall Kicks Will Work"))
        self.collect(self.get_item_by_name("Cool, Cool Mountain - Spindrifts"))
        self.assertTrue(self.can_reach_location("Cool, Cool Mountain - Wall Kicks Will Work"))
        self.assertTrue(cool_cool_mountain_coins(self.multiworld.state, self.player, 12))
        self.assertTrue(cool_cool_mountain_coins(self.multiworld.state, self.player, 15))
        self.assertFalse(cool_cool_mountain_coins(self.multiworld.state, self.player, 16))


class CoolCoolMountainSpinJumpPermanentCoinTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **CoolCoolMountainSpinJumpUnlockLogicTestBase.options,
    }

    def test_permanent_collection_preserves_spindrift_route_coins(self):
        self.collect(self.get_item_by_name("Cool, Cool Mountain - Spindrifts"))
        self.assertTrue(cool_cool_mountain_coins(self.multiworld.state, self.player, 15))
        self.assertFalse(cool_cool_mountain_coins(self.multiworld.state, self.player, 16))


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

    def test_spin_jump_wall_kicks_route_preserves_spindrift_coins(self):
        self.assertTrue(self.can_reach_location("Cool, Cool Mountain - Coins Star"))
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
        "level_unlocks": Options.LevelUnlocks.option_special_only,
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
            }


class WhompsFortressIndividualUnlockLogicTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "coin_object_unlocks": Options.CoinObjectUnlocks.option_per_level,
        "enemy_unlocks": Options.EnemyUnlocks.option_per_level,
        "level_features": Options.LevelFeatures.option_per_level,
        "bobomb_buddies": Options.BobombBuddies.option_per_level,
    }

    def test_initial_coin_sources_are_counted_independently(self):
        source_coins = {
            "Whomp's Fortress - Single Yellow Coins": 4,
            "Whomp's Fortress - Red Coins": 10,
            "Whomp's Fortress - Horizontal Coin Lines": 20,
            "Whomp's Fortress - Horizontal Coin Rings": 16,
            "Whomp's Fortress - Throwable Cork Boxes": 6,
            "Whomp's Fortress - Piranha Plants": 15,
            "Whomp's Fortress - Whomps": 10,
        }
        self.assertFalse(whomps_fortress_coins(self.multiworld.state, self.player, 1))
        for item_name, expected_coins in source_coins.items():
            with self.subTest(item=item_name):
                item = self.get_item_by_name(item_name)
                self.collect(item)
                self.assertTrue(whomps_fortress_coins(
                    self.multiworld.state, self.player, expected_coins))
                self.assertFalse(whomps_fortress_coins(
                    self.multiworld.state, self.player, expected_coins + 1))
                self.remove(item)

    def test_thwomp_unlock_adds_its_red_coin(self):
        self.collect(self.get_item_by_name("Whomp's Fortress - Red Coins"))
        self.assertTrue(whomps_fortress_coins(self.multiworld.state, self.player, 10))
        self.assertFalse(whomps_fortress_coins(self.multiworld.state, self.player, 11))

        self.collect(self.get_item_by_name("Whomp's Fortress - Thwomps"))
        self.assertTrue(whomps_fortress_coins(self.multiworld.state, self.player, 12))
        self.assertFalse(whomps_fortress_coins(self.multiworld.state, self.player, 13))

    def test_ground_pound_sources_use_their_own_unlocks(self):
        self.collect(self.get_item_by_name("Ground Pound"))

        whomps = self.get_item_by_name("Whomp's Fortress - Whomps")
        self.collect(whomps)
        self.assertTrue(whomps_fortress_coins(self.multiworld.state, self.player, 20))
        self.assertFalse(whomps_fortress_coins(self.multiworld.state, self.player, 21))
        self.remove(whomps)

        self.collect(self.get_item_by_name("Whomp's Fortress - Blue Coin Block"))
        self.assertTrue(whomps_fortress_coins(self.multiworld.state, self.player, 20))
        self.assertFalse(whomps_fortress_coins(self.multiworld.state, self.player, 21))

    def test_top_sources_use_their_own_unlocks(self):
        self.collect(self.get_item_by_name("Whomp's Fortress - Checkerboard Platform"))

        source_coins = {
            "Whomp's Fortress - Red Coins": 14,
            "Whomp's Fortress - Horizontal Coin Rings": 24,
            "Whomp's Fortress - Coin Arrows": 8,
        }
        for item_name, expected_coins in source_coins.items():
            with self.subTest(item=item_name):
                item = self.get_item_by_name(item_name)
                self.collect(item)
                self.assertTrue(whomps_fortress_coins(
                    self.multiworld.state, self.player, expected_coins))
                self.assertFalse(whomps_fortress_coins(
                    self.multiworld.state, self.player, expected_coins + 1))
                self.remove(item)

    def test_wild_blue_coins_require_horizontal_ring_unlock(self):
        self.collect(self.get_item_by_name("Whomp's Fortress - Cannon Unlock"))
        self.assertFalse(whomps_fortress_coins(self.multiworld.state, self.player, 1))
        self.collect(self.get_item_by_name("Whomp's Fortress - Horizontal Coin Rings"))
        self.assertTrue(whomps_fortress_coins(self.multiworld.state, self.player, 24))
        self.assertFalse(whomps_fortress_coins(self.multiworld.state, self.player, 25))

    def test_red_coin_star_requires_red_coins(self):
        self.collect_by_name([
            "Whomp's Fortress - Checkerboard Platform",
            "Whomp's Fortress - Thwomps",
        ])
        self.assertFalse(self.can_reach_location("Whomp's Fortress - Red Coins on the Floating Isle"))
        self.collect(self.get_item_by_name("Whomp's Fortress - Red Coins"))
        self.assertTrue(self.can_reach_location("Whomp's Fortress - Red Coins on the Floating Isle"))


class WhompsFortressWhompTricksTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "enemy_unlocks": Options.EnemyUnlocks.option_per_level,
        "level_features": Options.LevelFeatures.option_per_level,
        "bobomb_buddies": Options.BobombBuddies.option_per_level,
        "logic_tricks": {
            "Whomp's Fortress Top Access with Side Flip and Ledge Grab Off of Whomp",
            "Whomp's Fortress Top Access with Triple Jump Off of Whomp",
        },
    }

    def test_top_access_tricks_require_whomps(self):
        self.collect([
            self.get_item_by_name("Side Flip"),
            self.get_item_by_name("Ledge Grab"),
            self.get_item_by_name("Triple Jump"),
        ])
        self.assertFalse(self.can_reach_region("Whomp's Fortress - Top"))

        self.collect(self.get_item_by_name("Whomp's Fortress - Whomps"))
        self.assertTrue(self.can_reach_region("Whomp's Fortress - Top"))


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
        "level_unlocks": Options.LevelUnlocks.option_special_only,
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
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
        "level_unlocks": Options.LevelUnlocks.option_special_only,
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
            }


class JollyRogerBayIndividualUnlockLogicTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "coin_object_unlocks": Options.CoinObjectUnlocks.option_per_level,
        "enemy_unlocks": Options.EnemyUnlocks.option_per_level,
        "level_features": Options.LevelFeatures.option_per_level,
        "bobomb_buddies": Options.BobombBuddies.option_per_level,
    }

    def test_initial_coin_sources_are_counted_independently(self):
        source_coins = {
            "Jolly Roger Bay - Red Coins": 8,
            "Jolly Roger Bay - Horizontal Coin Rings": 24,
            "Jolly Roger Bay - Vertical Coin Lines": 5,
            "Jolly Roger Bay - Vertical Coin Rings": 8,
            "Jolly Roger Bay - 3-Coin Block": 3,
            "Jolly Roger Bay - Goombas": 3,
        }
        self.assertFalse(jolly_roger_bay_coins(self.multiworld.state, self.player, 1))
        for item_name, expected_coins in source_coins.items():
            with self.subTest(item=item_name):
                item = self.get_item_by_name(item_name)
                self.collect(item)
                self.assertTrue(jolly_roger_bay_coins(
                    self.multiworld.state, self.player, expected_coins))
                self.assertFalse(jolly_roger_bay_coins(
                    self.multiworld.state, self.player, expected_coins + 1))
                self.remove(item)

    def test_upper_sources_use_their_own_unlocks(self):
        self.collect(self.get_item_by_name("Side Flip"))

        source_coins = {
            "Jolly Roger Bay - Horizontal Coin Lines": 15,
        }
        for item_name, expected_coins in source_coins.items():
            with self.subTest(item=item_name):
                item = self.get_item_by_name(item_name)
                self.collect(item)
                self.assertTrue(jolly_roger_bay_coins(
                    self.multiworld.state, self.player, expected_coins))
                self.assertFalse(jolly_roger_bay_coins(
                    self.multiworld.state, self.player, expected_coins + 1))
                self.remove(item)

    def test_blue_coin_switch_requires_ground_pound(self):
        self.collect(self.get_item_by_name("Jolly Roger Bay - Blue Coin Block"))
        self.assertFalse(jolly_roger_bay_coins(self.multiworld.state, self.player, 1))
        self.collect(self.get_item_by_name("Ground Pound"))
        self.assertTrue(jolly_roger_bay_coins(self.multiworld.state, self.player, 30))
        self.assertFalse(jolly_roger_bay_coins(self.multiworld.state, self.player, 31))

    def test_red_coin_routes_total_sixteen(self):
        self.collect([
            self.get_item_by_name("Jolly Roger Bay - Red Coins"),
            self.get_item_by_name("Climb"),
        ])
        self.assertTrue(jolly_roger_bay_coins(self.multiworld.state, self.player, 10))
        self.assertFalse(jolly_roger_bay_coins(self.multiworld.state, self.player, 11))

        self.collect([
            self.get_item_by_name("Side Flip"),
            self.get_item_by_name("Jolly Roger Bay - Raised Ship"),
        ])
        self.assertTrue(jolly_roger_bay_coins(self.multiworld.state, self.player, 16))
        self.assertFalse(jolly_roger_bay_coins(self.multiworld.state, self.player, 17))

    def test_red_coin_star_requires_red_coins(self):
        self.collect([
            self.get_item_by_name("Jolly Roger Bay - Raised Ship"),
            self.get_item_by_name("Climb"),
            self.get_item_by_name("Side Flip"),
        ])
        self.assertFalse(self.can_reach_location("Jolly Roger Bay - Red Coins on the Ship Afloat"))
        self.collect(self.get_item_by_name("Jolly Roger Bay - Red Coins"))
        self.assertTrue(self.can_reach_location("Jolly Roger Bay - Red Coins on the Ship Afloat"))


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


class JollyRogerBayPillarBackflipSignTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
                "coin_object_unlocks": Options.CoinObjectUnlocks.option_per_level,
        "sign_unlocks": Options.SignUnlocks.option_per_level,
        "logic_tricks": {
            "Jolly Roger Bay Pillar Red Coin with Triple Jump, Backflip, or Wall Kick",
        },
    }

    def test_backflip_route_requires_jolly_roger_bay_signs(self):
        self.collect([
            self.get_item_by_name("Jolly Roger Bay - Raised Ship"),
            self.get_item_by_name("Jolly Roger Bay - Red Coins"),
            self.get_item_by_name("Side Flip"),
            self.get_item_by_name("Backflip"),
        ])
        self.assertFalse(self.can_reach_location("Jolly Roger Bay - Red Coins on the Ship Afloat"))
        self.collect(self.get_item_by_name("Jolly Roger Bay - Signs"))
        self.assertTrue(self.can_reach_location("Jolly Roger Bay - Red Coins on the Ship Afloat"))


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

    def test_start_coins_reach_coin_star_without_climb(self):
        self.assertTrue(self.can_reach_location("Jolly Roger Bay - Coins Star"))
        self.collect(self.get_item_by_name("Climb"))
        self.assertTrue(self.can_reach_location("Jolly Roger Bay - Coins Star"))

    def test_start_coins_reach_coin_star_without_cannon(self):
        self.assertTrue(self.can_reach_location("Jolly Roger Bay - Coins Star"))
        self.collect(self.get_item_by_name("Jolly Roger Bay - Cannon Unlock"))
        self.assertTrue(self.can_reach_location("Jolly Roger Bay - Coins Star"))

    def test_raised_ship_does_not_remove_start_coins(self):
        self.collect(self.get_item_by_name("Jolly Roger Bay - Raised Ship"))
        self.assertTrue(self.can_reach_location("Jolly Roger Bay - Coins Star"))


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
        "level_features": Options.LevelFeatures.option_global,
        "bobomb_buddies": Options.BobombBuddies.option_per_level,
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
        self.collect(self.world.create_item("Glitched Logic"))
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
    # Superseded by the route/resource tests below after the Huge Island region rewrite.
    __unittest_skip__ = True
    run_default_tests = False
    options = {
        **SHUFFLED_ARBITRARY_FEATURE_OPTIONS,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "buddy_checks": Options.BuddyChecks.option_true,
        "level_unlocks": Options.LevelUnlocks.option_special_only,
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
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
        self.collect(self.get_item_by_name("Warp Pipes"))
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
            self.get_item_by_name("Warp Pipes"),
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


class TinyHugeIslandRegionRewriteTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_ARBITRARY_FEATURE_OPTIONS,
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "level_unlocks": Options.LevelUnlocks.option_special_only,
                "enemy_unlocks": Options.EnemyUnlocks.option_per_level,
        "logic_tricks": {
            "Tiny-Huge Island Windswept Valley with Fly Guy Spin Jump",
            "Tiny-Huge Island Scale the Huge Mountain on the Koopa Shell",
        },
    }

    def collect_second_floor_access(self):
        self.collect(self.get_item_by_name("Progressive Upstairs Key"))

    def disable_huge_entry(self):
        self.multiworld.get_entrance(
            "Second Floor -> Tiny-Huge Island (Huge)", self.player).access_rule = lambda state: False

    def disable_tiny_entry(self):
        self.multiworld.get_entrance(
            "Second Floor -> Tiny-Huge Island (Tiny)", self.player).access_rule = lambda state: False

    def test_tiny_pipes_reach_each_matching_huge_region(self):
        self.disable_huge_entry()
        self.collect_second_floor_access()
        self.collect([
            self.get_item_by_name("Long Jump"),
            self.get_item_by_name("Vertical Wind"),
        ])
        self.assertTrue(self.can_reach_region("Tiny-Huge Island - Tiny Piranha Area"))
        self.assertFalse(self.can_reach_region("Tiny-Huge Island - Huge Piranha Area"))

        self.collect(self.get_item_by_name("Warp Pipes"))
        self.assertTrue(self.can_reach_region("Tiny-Huge Island - Huge Piranha Area"))
        self.assertTrue(self.can_reach_entrance("Tiny-Huge Island - Windswept Valley to Tiny Main"))
        self.assertTrue(self.can_reach_region("Tiny-Huge Island - Tiny Main"))
        self.assertTrue(self.can_reach_entrance("Tiny-Huge Island - Tiny Main to Windswept Valley"))
        self.assertTrue(self.can_reach_region("Tiny-Huge Island - Koopa the Quick"))

        self.collect(self.get_item_by_name("Purple Switches"))
        self.assertTrue(self.can_reach_region("Tiny-Huge Island - Tiny Main"))
        self.assertTrue(self.can_reach_region("Tiny-Huge Island - Koopa the Quick"))
        self.assertTrue(self.can_reach_region("Tiny-Huge Island (Huge)"))

    def test_repeatable_movement_reaches_the_huge_mountain_regions(self):
        self.disable_tiny_entry()
        self.collect_second_floor_access()
        self.collect([
            self.get_item_by_name("Long Jump"),
            self.get_item_by_name("Vertical Wind"),
        ])
        self.assertTrue(self.can_reach_region("Tiny-Huge Island - Windswept Valley"))
        self.assertFalse(self.can_reach_region("Tiny-Huge Island - Cannonball"))
        self.assertFalse(self.can_reach_entrance("Tiny-Huge Island - Windswept Valley to Tiny Main"))

        self.collect(self.get_item_by_name("Warp Pipes"))
        self.assertTrue(self.can_reach_entrance("Tiny-Huge Island - Windswept Valley to Tiny Main"))
        self.assertTrue(self.can_reach_region("Tiny-Huge Island - Tiny Main"))

        self.collect(self.get_item_by_name("Side Flip"))
        self.assertTrue(self.can_reach_region("Tiny-Huge Island - Cannonball"))
        self.assertTrue(self.can_reach_region("Tiny-Huge Island - Koopa the Quick"))
        self.assertTrue(self.can_reach_region("Tiny-Huge Island - Huge Top"))
        self.assertTrue(self.can_reach_region("Tiny-Huge Island - Huge Tree Area"))
        self.assertTrue(self.can_reach_region("Tiny-Huge Island - Huge Piranha Area"))
        self.assertFalse(self.can_reach_region("Tiny-Huge Island - Wiggler's Cave"))

    def test_wall_kick_reaches_cannonball_and_koopa_regions(self):
        self.disable_tiny_entry()
        self.collect_second_floor_access()
        self.collect([
            self.get_item_by_name("Long Jump"),
            self.get_item_by_name("Vertical Wind"),
        ])
        self.assertTrue(self.can_reach_region("Tiny-Huge Island - Windswept Valley"))
        self.assertFalse(self.can_reach_region("Tiny-Huge Island - Cannonball"))

        self.collect(self.get_item_by_name("Wall Kick"))
        self.assertTrue(self.can_reach_region("Tiny-Huge Island - Cannonball"))
        self.assertTrue(self.can_reach_region("Tiny-Huge Island - Koopa the Quick"))

    def test_huge_piranha_area_returns_through_both_pipes(self):
        self.disable_tiny_entry()
        self.collect_second_floor_access()
        self.collect([
            self.get_item_by_name("Tiny-Huge Island - Koopa Troopas"),
            self.get_item_by_name("Warp Pipes"),
            self.get_item_by_name("Purple Switches"),
        ])
        self.assertTrue(self.can_reach_region("Tiny-Huge Island - Huge Top"))
        self.assertTrue(self.can_reach_region("Tiny-Huge Island - Huge Piranha Area"))
        self.assertTrue(self.can_reach_region("Tiny-Huge Island - Tiny Piranha Area"))
        self.assertTrue(self.can_reach_region("Tiny-Huge Island - Tiny Main"))
        self.assertTrue(self.can_reach_region("Tiny-Huge Island - Koopa the Quick"))


class TinyHugeIslandOneUseAscentCoinTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_ARBITRARY_FEATURE_OPTIONS,
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "level_unlocks": Options.LevelUnlocks.option_special_only,
                "coin_object_unlocks": Options.CoinObjectUnlocks.option_per_level,
        "enemy_unlocks": Options.EnemyUnlocks.option_per_level,
        "logic_tricks": {
            "Tiny-Huge Island Windswept Valley with Fly Guy Spin Jump",
            "Tiny-Huge Island Scale the Huge Mountain on the Koopa Shell",
        },
    }

    def maximum_reachable_coins(self):
        return max(
            coins for coins in range(194)
            if tiny_huge_island_coins(self.multiworld.state, self.player, coins))

    def test_one_use_ascents_select_the_best_dead_end_routes(self):
        self.multiworld.get_entrance(
            "Second Floor -> Tiny-Huge Island (Tiny)", self.player).access_rule = lambda state: False
        self.collect(self.get_item_by_name("Progressive Upstairs Key"))
        self.collect([
            self.get_item_by_name(name)
            for name in (
                "Tiny-Huge Island - Single Yellow Coins",
                "Tiny-Huge Island - Red Coins",
                "Tiny-Huge Island - Blue Coin Block",
                "Tiny-Huge Island - Horizontal Coin Lines",
                "Tiny-Huge Island - 3-Coin Block",
                "Tiny-Huge Island - Wooden Posts",
                "Tiny-Huge Island - Chuckya",
                "Tiny-Huge Island - Lakitu",
                "Tiny-Huge Island - Fire Piranha Plants",
                "Tiny-Huge Island - Fly Guys",
                "Tiny-Huge Island - Goombas",
                "Tiny-Huge Island - Koopa Troopas",
            )
        ])

        one_ascent_total = self.maximum_reachable_coins()
        self.collect([
            self.get_item_by_name("Side Flip"),
            self.get_item_by_name("Ledge Grab"),
        ])
        two_ascent_total = self.maximum_reachable_coins()
        self.assertGreaterEqual(two_ascent_total, one_ascent_total)

        self.collect(self.get_item_by_name("Long Jump"))
        repeatable_ascent_total = self.maximum_reachable_coins()
        self.assertGreater(repeatable_ascent_total, two_ascent_total)

    def collect_full_two_way_pipe_route(self):
        self.collect(self.get_item_by_name("Progressive Upstairs Key"))
        self.collect_by_name([
            "Long Jump",
            "Side Flip",
            "Wall Kick",
            "Ground Pound",
            "Purple Switches",
            "Warp Pipes",
            "Tiny-Huge Island - Cannon Unlock",
            "Tiny-Huge Island - Single Yellow Coins",
            "Tiny-Huge Island - Red Coins",
            "Tiny-Huge Island - Blue Coin Block",
            "Tiny-Huge Island - Horizontal Coin Lines",
            "Tiny-Huge Island - 3-Coin Block",
            "Tiny-Huge Island - Wooden Posts",
            "Tiny-Huge Island - Chuckya",
            "Tiny-Huge Island - Lakitu",
            "Tiny-Huge Island - Fire Piranha Plants",
            "Tiny-Huge Island - Fly Guys",
            "Tiny-Huge Island - Goombas",
            "Tiny-Huge Island - Koopa Troopas",
        ])

    def test_tiny_entrance_route_can_collect_all_non_impossible_coins(self):
        self.multiworld.get_entrance(
            "Second Floor -> Tiny-Huge Island (Huge)", self.player).access_rule = lambda state: False
        self.collect_full_two_way_pipe_route()

        self.assertEqual(self.maximum_reachable_coins(), 191)

    def test_huge_entrance_route_can_collect_all_non_impossible_coins(self):
        self.multiworld.get_entrance(
            "Second Floor -> Tiny-Huge Island (Tiny)", self.player).access_rule = lambda state: False
        self.collect_full_two_way_pipe_route()

        self.assertEqual(self.maximum_reachable_coins(), 191)
        evaluation = COIN_EVALUATORS["Tiny-Huge Island"](
            self.multiworld.state, self.player, 191)
        source_ids = {source.source_id for source in evaluation.children}
        self.assertIn("huge_piranha_area_plants", source_ids)
        self.assertIn("tiny_piranha_area_plant", source_ids)
        self.assertIn("tiny_start_goomba", source_ids)


class TinyHugeIslandPermanentCoinCollectionTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **TinyHugeIslandOneUseAscentCoinTestBase.options,
    }

    def maximum_reachable_coins(self):
        return max(
            coins for coins in range(193)
            if tiny_huge_island_coins(self.multiworld.state, self.player, coins)
        )

    def test_permanent_collection_combines_tiny_and_huge_routes(self):
        self.collect(self.get_item_by_name("Progressive Upstairs Key"))
        self.collect_by_name([
            "Triple Jump",
            "Long Jump",
            "Side Flip",
            "Ledge Grab",
            "Ground Pound",
            "Purple Switches",
            "Tiny-Huge Island - Single Yellow Coins",
            "Tiny-Huge Island - Red Coins",
            "Tiny-Huge Island - Blue Coin Block",
            "Tiny-Huge Island - Horizontal Coin Lines",
            "Tiny-Huge Island - 3-Coin Block",
            "Tiny-Huge Island - Wooden Posts",
            "Tiny-Huge Island - Chuckya",
            "Tiny-Huge Island - Lakitu",
            "Tiny-Huge Island - Fire Piranha Plants",
            "Tiny-Huge Island - Fly Guys",
            "Tiny-Huge Island - Goombas",
            "Tiny-Huge Island - Koopa Troopas",
        ])
        self.assertTrue(self.can_reach_region("Tiny-Huge Island (Tiny)"))
        self.assertTrue(self.can_reach_region("Tiny-Huge Island (Huge)"))

        self.assertGreater(self.maximum_reachable_coins(), 0)


class TinyHugeIslandImpossibleCoinTrickTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_ARBITRARY_FEATURE_OPTIONS,
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "level_unlocks": Options.LevelUnlocks.option_special_only,
                "coin_object_unlocks": Options.CoinObjectUnlocks.option_per_level,
        "enemy_unlocks": Options.EnemyUnlocks.option_per_level,
        "accessibility": "minimal",
        "logic_tricks": {"Tiny Island Impossible Coin"},
    }

    def maximum_reachable_coins(self):
        return max(
            coins for coins in range(194)
            if tiny_huge_island_coins(self.multiworld.state, self.player, coins))

    def test_impossible_coin_requires_every_trick_action(self):
        self.multiworld.get_entrance(
            "Second Floor -> Tiny-Huge Island (Huge)", self.player).access_rule = lambda state: False
        self.collect(self.get_item_by_name("Progressive Upstairs Key"))
        self.collect([
            self.get_item_by_name("Tiny-Huge Island - Single Yellow Coins"),
            self.get_item_by_name("Purple Switches"),
            self.get_item_by_name("Warp Pipes"),
            self.get_item_by_name("Triple Jump"),
            self.get_item_by_name("Dive"),
            self.get_item_by_name("Ground Pound"),
        ])
        before_impossible_coin = self.maximum_reachable_coins()

        self.collect(self.get_item_by_name("Kick"))
        self.assertEqual(self.maximum_reachable_coins(), before_impossible_coin + 1)


class TinyHugeIslandImpossibleCoinFullAccessibilityCapTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        "accessibility": "full",
        "tiny_huge_island_coin_star_requirement": 192,
    }

    def test_full_accessibility_caps_requirement_at_191(self):
        self.assertEqual(self.world.options.tiny_huge_island_coin_star_requirement.value, 191)
        self.assertEqual(self.world.get_coin_star_requirements_slot_data()[12], 191)


class DireDireDocksCoinStarAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_ARBITRARY_FEATURE_OPTIONS,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "buddy_checks": Options.BuddyChecks.option_true,
        "level_unlocks": Options.LevelUnlocks.option_special_only,
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
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


class DireDireDocksIndividualUnlockLogicTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_ARBITRARY_FEATURE_OPTIONS,
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "coin_object_unlocks": Options.CoinObjectUnlocks.option_per_level,
        "level_unlocks": Options.LevelUnlocks.option_special_only,
            }

    def collect_full_dire_dire_docks_route(self):
        self.collect([self.get_item_by_name("Progressive Basement Key")] * 2)
        self.collect_by_name([
            "Triple Jump",
            "Ground Pound",
            "Climb",
            "Purple Switches",
            "Dire, Dire Docks - Bowser's Sub",
            "Dire, Dire Docks - Poles",
        ])

    def test_each_unlock_matches_documented_total(self):
        self.collect_full_dire_dire_docks_route()
        source_coins = {
            "Dire, Dire Docks - Single Yellow Coins": 3,
            "Dire, Dire Docks - Red Coins": 16,
            "Dire, Dire Docks - Blue Coin Block": 30,
            "Dire, Dire Docks - Horizontal Coin Lines": 10,
            "Dire, Dire Docks - Horizontal Coin Rings": 8,
            "Dire, Dire Docks - Vertical Coin Lines": 15,
            "Dire, Dire Docks - Vertical Coin Rings": 24,
        }
        for item_name, expected_coins in source_coins.items():
            with self.subTest(item=item_name):
                item = self.get_item_by_name(item_name)
                self.collect(item)
                self.assertTrue(dire_dire_docks_coins(
                    self.multiworld.state, self.player, expected_coins))
                self.assertFalse(dire_dire_docks_coins(
                    self.multiworld.state, self.player, expected_coins + 1))
                self.remove(item)

    def test_all_unlocks_total_106_coins(self):
        self.collect_full_dire_dire_docks_route()
        self.collect_by_name([
            "Dire, Dire Docks - Single Yellow Coins",
            "Dire, Dire Docks - Red Coins",
            "Dire, Dire Docks - Blue Coin Block",
            "Dire, Dire Docks - Horizontal Coin Lines",
            "Dire, Dire Docks - Horizontal Coin Rings",
            "Dire, Dire Docks - Vertical Coin Lines",
            "Dire, Dire Docks - Vertical Coin Rings",
        ])
        self.assertTrue(dire_dire_docks_coins(
            self.multiworld.state, self.player, 106))

    def test_red_coin_star_requires_red_coin_unlock(self):
        self.collect_full_dire_dire_docks_route()
        self.assertFalse(self.can_reach_location(
            "Dire, Dire Docks - Pole-Jumping for Red Coins"))
        self.collect(self.get_item_by_name("Dire, Dire Docks - Red Coins"))
        self.assertTrue(self.can_reach_location(
            "Dire, Dire Docks - Pole-Jumping for Red Coins"))


class HazyMazeCaveCoinStarAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_ARBITRARY_FEATURE_OPTIONS,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "buddy_checks": Options.BuddyChecks.option_true,
        "level_unlocks": Options.LevelUnlocks.option_special_only,
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
            }

    def collect_basement_access(self):
        self.collect(self.get_item_by_name("Progressive Basement Key"))


class HazyMazeCaveCoinCountChecksAccessTestBase(HazyMazeCaveCoinStarAccessTestBase):
    options = {
        **HazyMazeCaveCoinStarAccessTestBase.options,
        **ONE_COIN_STAR_REQUIREMENTS,
        "coin_count_checks": 100,
        "hazy_maze_cave_coin_star_requirement": 79,
    }

    def test_coin_count_check_location_uses_hmc_coin_logic(self):
        self.collect_basement_access()
        self.assertFalse(self.can_reach_location("Hazy Maze Cave - 78 Coins"))
        self.collect(self.get_item_by_name("Wall Kick"))
        self.assertTrue(self.can_reach_location("Hazy Maze Cave - 78 Coins"))


class HazyMazeCaveCoinStar51AccessTestBase(HazyMazeCaveCoinStarAccessTestBase):
    options = {
        **HazyMazeCaveCoinStarAccessTestBase.options,
        "hazy_maze_cave_coin_star_requirement": 51,
    }

    def test_start_coins_reach_coin_star(self):
        self.collect_basement_access()
        self.assertTrue(self.can_reach_location("Hazy Maze Cave - Coins Star"))


class HazyMazeCaveCoinStar54AccessTestBase(HazyMazeCaveCoinStarAccessTestBase):
    options = {
        **HazyMazeCaveCoinStarAccessTestBase.options,
        "hazy_maze_cave_coin_star_requirement": 54,
    }

    def test_metal_cap_coins_reach_coin_star(self):
        self.collect_basement_access()
        self.assertFalse(self.can_reach_location("Hazy Maze Cave - Coins Star"))
        self.collect(self.get_item_by_name("Metal Cap"))
        self.assertFalse(self.can_reach_location("Hazy Maze Cave - Coins Star"))
        self.collect(self.get_item_by_name("Purple Switches"))
        self.assertTrue(self.can_reach_location("Hazy Maze Cave - Coins Star"))


class HazyMazeCaveCoinStar71AccessTestBase(HazyMazeCaveCoinStarAccessTestBase):
    options = {
        **HazyMazeCaveCoinStarAccessTestBase.options,
        "hazy_maze_cave_coin_star_requirement": 71,
    }

    def test_basic_movement_coins_reach_coin_star(self):
        self.collect_basement_access()
        self.assertFalse(self.can_reach_location("Hazy Maze Cave - Coins Star"))
        self.collect(self.get_item_by_name("Ledge Grab"))
        self.assertTrue(self.can_reach_location("Hazy Maze Cave - Coins Star"))


class HazyMazeCaveCoinStar75AccessTestBase(HazyMazeCaveCoinStarAccessTestBase):
    options = {
        **HazyMazeCaveCoinStarAccessTestBase.options,
        "hazy_maze_cave_coin_star_requirement": 75,
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


class HazyMazeCaveCoinStar81CheckerboardAccessTestBase(HazyMazeCaveCoinStarAccessTestBase):
    options = {
        **HazyMazeCaveCoinStarAccessTestBase.options,
        "hazy_maze_cave_coin_star_requirement": 81,
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


class HazyMazeCaveCoinStar54CaplessAccessTestBase(HazyMazeCaveCoinStarAccessTestBase):
    options = {
        **HazyMazeCaveCoinStarAccessTestBase.options,
        "hazy_maze_cave_coin_star_requirement": 54,
    }

    def test_capless_triple_jump_coins_reach_coin_star(self):
        self.collect_basement_access()
        self.assertFalse(self.can_reach_location("Hazy Maze Cave - Coins Star"))
        self.collect([
            self.get_item_by_name("Triple Jump"),
            self.get_item_by_name("Purple Switches"),
        ])
        self.assertTrue(self.can_reach_location("Hazy Maze Cave - Coins Star"))


class HazyMazeCaveCoinStar78AccessTestBase(HazyMazeCaveCoinStarAccessTestBase):
    options = {
        **HazyMazeCaveCoinStarAccessTestBase.options,
        "hazy_maze_cave_coin_star_requirement": 78,
    }

    def test_toxic_maze_coins_reach_coin_star(self):
        self.collect_basement_access()
        self.assertFalse(self.can_reach_location("Hazy Maze Cave - Coins Star"))
        self.collect(self.get_item_by_name("Wall Kick"))
        self.assertTrue(self.can_reach_location("Hazy Maze Cave - Navigating the Toxic Maze"))
        self.assertTrue(self.can_reach_location("Hazy Maze Cave - Coins Star"))


class HazyMazeCaveCoinStar83AccessTestBase(HazyMazeCaveCoinStarAccessTestBase):
    options = {
        **HazyMazeCaveCoinStarAccessTestBase.options,
        "hazy_maze_cave_coin_star_requirement": 83,
    }

    def test_pit_islands_climb_coins_reach_coin_star(self):
        self.collect_basement_access()
        self.collect(self.get_item_by_name("Triple Jump"))
        self.assertTrue(self.can_reach_location("Hazy Maze Cave - Navigating the Toxic Maze"))
        self.assertFalse(self.can_reach_location("Hazy Maze Cave - Coins Star"))

        self.collect(self.get_item_by_name("Climb"))
        self.assertTrue(self.can_reach_region("Hazy Maze Cave - Pit Islands"))
        self.assertTrue(self.can_reach_location("Hazy Maze Cave - Coins Star"))


class HazyMazeCaveCoinStar59SwimmingBeastAccessTestBase(HazyMazeCaveCoinStarAccessTestBase):
    options = {
        **HazyMazeCaveCoinStarAccessTestBase.options,
        "hazy_maze_cave_coin_star_requirement": 59,
    }

    def test_swimming_beast_coins_reach_coin_star(self):
        self.collect_basement_access()
        self.assertFalse(self.can_reach_location("Hazy Maze Cave - Coins Star"))
        self.collect(self.get_item_by_name("Hazy Maze Cave - Swimming Beast"))
        self.assertTrue(self.can_reach_location("Hazy Maze Cave - Coins Star"))


class HazyMazeCaveElevatorClipAccessTestBase(HazyMazeCaveCoinStarAccessTestBase):
    options = {
        **HazyMazeCaveCoinStarAccessTestBase.options,
        "hazy_maze_cave_coin_star_requirement": 59,
        "logic_tricks": {"Hazy Maze Cave Elevator Clip"},
    }

    def test_elevator_clip_reaches_swimming_beast_and_cotmc(self):
        self.collect_basement_access()
        self.assertTrue(self.can_reach_location("Hazy Maze Cave - Swimming Beast in the Cavern"))
        self.assertTrue(self.can_reach_region("Cavern of the Metal Cap"))

    def test_elevator_clip_reaches_swimming_beast_coin_ring(self):
        self.collect_basement_access()
        self.assertTrue(self.can_reach_location("Hazy Maze Cave - Coins Star"))


class HazyMazeCaveCoinStar86AccessTestBase(HazyMazeCaveCoinStarAccessTestBase):
    options = {
        **HazyMazeCaveCoinStarAccessTestBase.options,
        "hazy_maze_cave_coin_star_requirement": 86,
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


class HazyMazeCaveIndividualUnlockLogicTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_ARBITRARY_FEATURE_OPTIONS,
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "coin_object_unlocks": Options.CoinObjectUnlocks.option_per_level,
        "level_unlocks": Options.LevelUnlocks.option_special_only,
        "enemy_unlocks": Options.EnemyUnlocks.option_per_level,
        "one_up_checks": Options.OneUpChecks.option_true,
        "one_up_unlocks": Options.OneUpUnlocks.option_per_level,
            }

    def collect_full_hazy_maze_cave_route(self):
        self.collect(self.get_item_by_name("Progressive Basement Key"))
        self.collect_by_name([
            "Triple Jump",
            "Long Jump",
            "Ground Pound",
            "Climb",
            "Metal Cap",
            "Checkerboard Platforms",
            "Purple Switches",
            "Hazy Maze Cave - Swimming Beast",
        ])
        self.assertTrue(self.can_reach_region("Hazy Maze Cave - Pit Islands"))
        self.assertTrue(self.can_reach_location("Hazy Maze Cave - Navigating the Toxic Maze"))

    def test_each_unlock_matches_documented_total(self):
        self.collect_full_hazy_maze_cave_route()
        source_coins = {
            "Hazy Maze Cave - Single Yellow Coins": 5,
            "Hazy Maze Cave - Red Coins": 16,
            "Hazy Maze Cave - Blue Coin Block": 35,
            "Hazy Maze Cave - Horizontal Coin Lines": 20,
            "Hazy Maze Cave - Horizontal Coin Rings": 16,
            "Hazy Maze Cave - Mr. Is": 10,
            "Hazy Maze Cave - Scuttlebugs": 18,
            "Hazy Maze Cave - Snufits": 8,
            "Hazy Maze Cave - Swoops": 11,
        }
        for item_name, expected_coins in source_coins.items():
            with self.subTest(item=item_name):
                item = self.get_item_by_name(item_name)
                self.collect(item)
                self.assertTrue(hazy_maze_cave_coins(
                    self.multiworld.state, self.player, expected_coins))
                self.assertFalse(hazy_maze_cave_coins(
                    self.multiworld.state, self.player, expected_coins + 1))
                self.remove(item)

    def test_all_unlocks_total_139_coins(self):
        self.collect_full_hazy_maze_cave_route()
        self.collect_by_name([
            "Hazy Maze Cave - Single Yellow Coins",
            "Hazy Maze Cave - Red Coins",
            "Hazy Maze Cave - Blue Coin Block",
            "Hazy Maze Cave - Horizontal Coin Lines",
            "Hazy Maze Cave - Horizontal Coin Rings",
            "Hazy Maze Cave - Mr. Is",
            "Hazy Maze Cave - Scuttlebugs",
            "Hazy Maze Cave - Snufits",
            "Hazy Maze Cave - Swoops",
        ])
        self.assertTrue(hazy_maze_cave_coins(
            self.multiworld.state, self.player, 139))

    def test_monty_mole_checks_require_monty_moles(self):
        self.collect_full_hazy_maze_cave_route()
        for location_name in (
                "Hazy Maze Cave - Blue Coin Trail Monty Moles",
                "Hazy Maze Cave - Twin Hole Monty Moles",
        ):
            self.assertFalse(self.can_reach_location(location_name))

        self.collect(self.get_item_by_name("Hazy Maze Cave - Monty Moles"))
        for location_name in (
                "Hazy Maze Cave - Blue Coin Trail Monty Moles",
                "Hazy Maze Cave - Twin Hole Monty Moles",
        ):
            self.assertTrue(self.can_reach_location(location_name))


class LethalLavaLandIndividualUnlockLogicTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_ARBITRARY_FEATURE_OPTIONS,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "level_unlocks": Options.LevelUnlocks.option_special_only,
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
                "coin_object_unlocks": Options.CoinObjectUnlocks.option_per_level,
        "enemy_unlocks": Options.EnemyUnlocks.option_per_level,
    }

    def collect_basement_access(self):
        self.collect(self.get_item_by_name("Progressive Basement Key"))

    def test_initial_coin_sources_are_counted_independently(self):
        self.collect_basement_access()
        source_coins = {
            "Lethal Lava Land - Single Yellow Coins": 21,
            "Lethal Lava Land - Horizontal Coin Lines": 25,
            "Lethal Lava Land - Horizontal Coin Rings": 16,
            "Lethal Lava Land - Crazy Box": 5,
            "Lethal Lava Land - Bowser Puzzle": 5,
            "Lethal Lava Land - Bullies": 10,
            "Lethal Lava Land - Mr. Is": 5,
        }
        self.assertFalse(lethal_lava_land_coins(self.multiworld.state, self.player, 1))
        for item_name, expected_coins in source_coins.items():
            with self.subTest(item=item_name):
                item = self.get_item_by_name(item_name)
                self.collect(item)
                self.assertTrue(lethal_lava_land_coins(
                    self.multiworld.state, self.player, expected_coins))
                self.assertFalse(lethal_lava_land_coins(
                    self.multiworld.state, self.player, expected_coins + 1))
                self.remove(item)

    def test_island_mr_i_requires_a_lava_route(self):
        self.collect_basement_access()
        self.collect(self.get_item_by_name("Lethal Lava Land - Mr. Is"))
        self.assertTrue(lethal_lava_land_coins(self.multiworld.state, self.player, 5))
        self.assertFalse(lethal_lava_land_coins(self.multiworld.state, self.player, 6))

        self.collect(self.get_item_by_name("Long Jump"))
        self.assertTrue(lethal_lava_land_coins(self.multiworld.state, self.player, 10))
        self.assertFalse(lethal_lava_land_coins(self.multiworld.state, self.player, 11))

    def test_red_coins_require_a_lava_route(self):
        self.collect(self.get_item_by_name("Lethal Lava Land - Red Coins"))
        self.assertFalse(lethal_lava_land_coins(self.multiworld.state, self.player, 1))

        self.collect(self.world.create_item("Koopa Shell Blocks"))
        self.assertTrue(lethal_lava_land_coins(self.multiworld.state, self.player, 10))
        self.assertFalse(lethal_lava_land_coins(self.multiworld.state, self.player, 11))

    def test_single_yellow_coin_routes(self):
        self.collect_basement_access()
        self.collect(self.get_item_by_name("Lethal Lava Land - Single Yellow Coins"))
        self.assertTrue(lethal_lava_land_coins(self.multiworld.state, self.player, 21))
        self.assertFalse(lethal_lava_land_coins(self.multiworld.state, self.player, 22))

        self.collect(self.get_item_by_name("Long Jump"))
        self.assertTrue(lethal_lava_land_coins(self.multiworld.state, self.player, 25))
        self.assertFalse(lethal_lava_land_coins(self.multiworld.state, self.player, 26))
        self.remove(self.get_item_by_name("Long Jump"))

        self.collect(self.world.create_item("Koopa Shell Blocks"))
        self.assertTrue(lethal_lava_land_coins(self.multiworld.state, self.player, 25))
        self.assertFalse(lethal_lava_land_coins(self.multiworld.state, self.player, 26))

    def test_under_bridge_coin_line_requires_a_lava_route(self):
        self.collect_basement_access()
        self.collect(self.get_item_by_name("Lethal Lava Land - Horizontal Coin Lines"))
        self.assertTrue(lethal_lava_land_coins(self.multiworld.state, self.player, 25))
        self.assertFalse(lethal_lava_land_coins(self.multiworld.state, self.player, 26))

        self.collect(self.world.create_item("Koopa Shell Blocks"))
        self.assertTrue(lethal_lava_land_coins(self.multiworld.state, self.player, 35))
        self.assertFalse(lethal_lava_land_coins(self.multiworld.state, self.player, 36))

    def test_red_coin_star_requires_red_coins_and_bowser_puzzle(self):
        self.collect_basement_access()
        self.assertFalse(self.can_reach_location("Lethal Lava Land - 8-Coin Puzzle with 15 Pieces"))

        self.collect(self.get_item_by_name("Lethal Lava Land - Red Coins"))
        self.assertFalse(self.can_reach_location("Lethal Lava Land - 8-Coin Puzzle with 15 Pieces"))

        self.collect(self.get_item_by_name("Lethal Lava Land - Bowser Puzzle"))
        self.assertTrue(self.can_reach_location("Lethal Lava Land - 8-Coin Puzzle with 15 Pieces"))
        self.assertTrue(lethal_lava_land_coins(self.multiworld.state, self.player, 21))
        self.assertFalse(lethal_lava_land_coins(self.multiworld.state, self.player, 22))

    def test_last_three_red_coins_need_a_route_and_healing_coins(self):
        self.collect([
            self.get_item_by_name("Lethal Lava Land - Red Coins"),
            self.world.create_item("Koopa Shell Blocks"),
        ])
        self.assertTrue(lethal_lava_land_coins(self.multiworld.state, self.player, 10))
        self.assertFalse(lethal_lava_land_coins(self.multiworld.state, self.player, 11))

        self.collect(self.get_item_by_name("Lethal Lava Land - Crazy Box"))
        self.assertTrue(lethal_lava_land_coins(self.multiworld.state, self.player, 15))
        self.assertFalse(lethal_lava_land_coins(self.multiworld.state, self.player, 16))

        self.collect(self.get_item_by_name("Lethal Lava Land - Horizontal Coin Rings"))
        self.assertTrue(lethal_lava_land_coins(self.multiworld.state, self.player, 45))
        self.assertFalse(lethal_lava_land_coins(self.multiworld.state, self.player, 46))

    def test_koopa_shell_red_coin_route_still_needs_healing_coins_for_star(self):
        self.collect_basement_access()
        self.collect([
            self.get_item_by_name("Lethal Lava Land - Red Coins"),
            self.world.create_item("Koopa Shell Blocks"),
        ])
        self.assertFalse(self.can_reach_location("Lethal Lava Land - 8-Coin Puzzle with 15 Pieces"))

        self.collect(self.get_item_by_name("Lethal Lava Land - Crazy Box"))
        self.assertFalse(self.can_reach_location("Lethal Lava Land - 8-Coin Puzzle with 15 Pieces"))

        self.collect(self.get_item_by_name("Lethal Lava Land - Horizontal Coin Lines"))
        self.assertTrue(self.can_reach_location("Lethal Lava Land - 8-Coin Puzzle with 15 Pieces"))

    def test_big_bully_stars_require_their_enemies(self):
        self.collect_basement_access()
        self.assertFalse(self.can_reach_location("Lethal Lava Land - Boil the Big Bully"))
        self.assertFalse(self.can_reach_location("Lethal Lava Land - Bully the Bullies"))

        self.collect(self.get_item_by_name("Lethal Lava Land - Big Bullies"))
        self.assertTrue(self.can_reach_location("Lethal Lava Land - Boil the Big Bully"))
        self.assertFalse(self.can_reach_location("Lethal Lava Land - Bully the Bullies"))

        self.collect(self.get_item_by_name("Lethal Lava Land - Bullies"))
        self.assertTrue(self.can_reach_location("Lethal Lava Land - Bully the Bullies"))


class LethalLavaLandCoinStarAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_ARBITRARY_FEATURE_OPTIONS,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "level_unlocks": Options.LevelUnlocks.option_special_only,
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
            }

    def collect_basement_access(self):
        self.collect(self.get_item_by_name("Progressive Basement Key"))


class LethalLavaLandLogicTricksTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_ARBITRARY_FEATURE_OPTIONS,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "level_unlocks": Options.LevelUnlocks.option_special_only,
        "one_up_checks": Options.OneUpChecks.option_true,
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
                "logic_tricks": {"Lava Damage Boosting"},
        "marios_hat": True,
    }

    def collect_basement_access(self):
        self.collect(self.get_item_by_name("Progressive Basement Key"))

    def test_bouncing_off_lava_reaches_log_star_and_one_ups(self):
        self.collect_basement_access()
        self.collect(self.get_item_by_name("Mario's Hat"))
        for location_name in (
                "Lethal Lava Land - Red-Hot Log Rolling",
                "Lethal Lava Land - Northeast Brown Platform 1-Up",
                "Lethal Lava Land - Boil the Big Bully Star Lava 1-Up",
                "Lethal Lava Land - Northwest Curve 1-Up",
        ):
            self.assertTrue(self.can_reach_location(location_name))


class LethalLavaLandLongJumpElevatorTricksTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_ARBITRARY_FEATURE_OPTIONS,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "level_unlocks": Options.LevelUnlocks.option_special_only,
        "one_up_checks": Options.OneUpChecks.option_true,
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
                "logic_tricks": {
            "Lethal Lava Land Hot-Foot it Into the Volcano With Wall Kick",
            "Lethal Lava Land Long Jump From Hot-Foot-It into the Volcano to Elevator Tour in the Volcano",
        },
    }

    def collect_basement_access(self):
        self.collect(self.get_item_by_name("Progressive Basement Key"))

    def test_long_jump_and_ledge_trick_bypass_climb(self):
        self.collect_basement_access()
        self.collect(self.get_item_by_name("Long Jump"))
        self.assertFalse(self.can_reach_location("Lethal Lava Land - Elevator Tour in the Volcano"))

        self.collect(self.get_item_by_name("Wall Kick"))
        self.assertTrue(self.can_reach_region("Lethal Lava Land - Hot-Foot-It Ledge"))
        self.assertFalse(self.can_reach_region("Lethal Lava Land - Upper Volcano"))
        self.assertFalse(self.can_reach_location("Lethal Lava Land - Volcano Pole 1-Up"))
        self.assertTrue(self.can_reach_location("Lethal Lava Land - Elevator Tour in the Volcano"))

    def test_climb_and_long_jump_reach_elevator_without_ledge_trick_move(self):
        self.collect_basement_access()
        self.collect([
            self.get_item_by_name("Climb"),
            self.get_item_by_name("Long Jump"),
        ])
        self.assertTrue(self.can_reach_location("Lethal Lava Land - Elevator Tour in the Volcano"))


class LethalLavaLandTripleJumpDiveElevatorTrickTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_ARBITRARY_FEATURE_OPTIONS,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "level_unlocks": Options.LevelUnlocks.option_special_only,
        "one_up_checks": Options.OneUpChecks.option_true,
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
                "logic_tricks": {
            "Lethal Lava Land Hot-Foot it Into the Volcano With No Movement Abilities",
            "Lethal Lava Land Triple Jump or Dive From Hot-Foot-It into the Volcano to Elevator Tour in the Volcano",
        },
    }

    def collect_basement_access(self):
        self.collect(self.get_item_by_name("Progressive Basement Key"))

    def test_triple_jump_or_dive_elevator_trick_always_requires_climb(self):
        self.collect_basement_access()
        self.assertTrue(self.can_reach_region("Lethal Lava Land - Hot-Foot-It Ledge"))
        self.collect(self.get_item_by_name("Triple Jump"))
        self.assertFalse(self.can_reach_location("Lethal Lava Land - Elevator Tour in the Volcano"))

        self.collect(self.get_item_by_name("Climb"))
        self.assertTrue(self.can_reach_location("Lethal Lava Land - Elevator Tour in the Volcano"))


class LethalLavaLandKoopaShellAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_ARBITRARY_FEATURE_OPTIONS,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "level_unlocks": Options.LevelUnlocks.option_special_only,
        "one_up_checks": Options.OneUpChecks.option_true,
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
            }

    def collect_basement_access(self):
        self.collect(self.get_item_by_name("Progressive Basement Key"))

    def test_koopa_shell_reaches_lava_crossing_one_ups_without_trick(self):
        self.collect_basement_access()
        self.assertFalse(self.can_reach_location("Lethal Lava Land - Northeast Brown Platform 1-Up"))
        self.collect(self.world.create_item("Koopa Shell Blocks"))
        self.assertTrue(self.can_reach_location("Lethal Lava Land - Northeast Brown Platform 1-Up"))


class LethalLavaLandCoinStar130BouncingOffLavaAccessTestBase(LethalLavaLandCoinStarAccessTestBase):
    options = {
        **LethalLavaLandCoinStarAccessTestBase.options,
        "logic_tricks": {"Lava Damage Boosting"},
        "lethal_lava_land_coin_star_requirement": 130,
        "marios_hat": True,
    }

    def test_bouncing_off_lava_reaches_bridge_coins(self):
        self.collect_basement_access()
        self.collect(self.get_item_by_name("Mario's Hat"))
        self.assertTrue(self.can_reach_location("Lethal Lava Land - Coins Star"))


class LethalLavaLandCoinStar125AccessTestBase(LethalLavaLandCoinStarAccessTestBase):
    options = {
        **LethalLavaLandCoinStarAccessTestBase.options,
        "lethal_lava_land_coin_star_requirement": 125,
    }

    def test_start_coins_need_a_lava_crossing_to_reach_coin_star(self):
        self.collect_basement_access()
        self.assertFalse(self.can_reach_location("Lethal Lava Land - Coins Star"))

        self.collect(self.world.create_item("Koopa Shell Blocks"))
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
        self.assertFalse(self.can_reach_location("Lethal Lava Land - Coins Star"))

        self.collect(self.world.create_item("Koopa Shell Blocks"))
        self.assertTrue(self.can_reach_location("Lethal Lava Land - Coins Star"))


class LethalLavaLandCoinStar130AccessTestBase(LethalLavaLandCoinStarAccessTestBase):
    options = {
        **LethalLavaLandCoinStarAccessTestBase.options,
        "lethal_lava_land_coin_star_requirement": 130,
    }

    def test_koopa_shell_coins_reach_coin_star(self):
        self.collect_basement_access()
        self.assertFalse(self.can_reach_location("Lethal Lava Land - Coins Star"))

        self.collect(self.world.create_item("Koopa Shell Blocks"))
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
            self.world.create_item("Koopa Shell Blocks"),
        ])
        self.assertFalse(self.can_reach_location("Lethal Lava Land - Coins Star"))

        self.collect(self.get_item_by_name("Checkerboard Platforms"))
        self.assertTrue(self.can_reach_location("Lethal Lava Land - Elevator Tour in the Volcano"))
        self.assertTrue(self.can_reach_location("Lethal Lava Land - Coins Star"))


class ShiftingSandLandStoneStructureAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_ARBITRARY_FEATURE_OPTIONS,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "level_unlocks": Options.LevelUnlocks.option_special_only,
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
                "blocksanity": Options.Blocksanity.option_true,
        "enemy_unlocks": Options.EnemyUnlocks.option_per_level,
        "logic_tricks": {
            "Shifting Sand Land Top of Stone Structure with Spin Jump or Tweesters",
            "Shifting Sand Land Pillars with Koopa Shell",
            "Shifting Sand Land Pillars with Side Flip or Kick",
            "Shifting Sand Land Stand Tall on the Four Pyramids Without Pyramid Elevator",
        },
    }

    def collect_basement_access(self):
        self.collect(self.get_item_by_name("Progressive Basement Key"))

    def test_stone_structure_requires_movement(self):
        self.collect_basement_access()
        self.assertFalse(self.can_reach_region("Shifting Sand Land - Stone Structure"))

        self.collect(self.get_item_by_name("Triple Jump"))
        self.assertTrue(self.can_reach_region("Shifting Sand Land - Stone Structure"))

    def test_shy_guy_bounce_requires_fly_guy(self):
        self.collect_basement_access()
        self.assertTrue(self.world.logic_ssl_top_of_stone_structure_spin_jump_or_tweesters)
        self.assertFalse(self.can_reach_region("Shifting Sand Land - Stone Structure"))

        self.collect(self.get_item_by_name("Shifting Sand Land - Fly Guys"))
        self.assertTrue(self.multiworld.state.has("Shifting Sand Land - Fly Guys", self.player))
        self.assertTrue(self.can_reach_region("Shifting Sand Land - Stone Structure"))

    def test_stone_structure_contains_both_blocks(self):
        region = self.multiworld.get_region("Shifting Sand Land - Stone Structure", self.player)
        self.assertEqual(
            {
                "Shifting Sand Land - Stone Structure Koopa Shell Block",
                "Shifting Sand Land - Stone Structure Wing Cap Block",
            },
            {location.name for location in region.locations if not location.name.startswith("Sign Hint - ")})

    def test_stone_structure_shell_route_reaches_upper_pyramid(self):
        self.collect_basement_access()
        self.collect(self.get_item_by_name("Triple Jump"))
        self.assertTrue(self.can_reach_region("Shifting Sand Land - Stone Structure"))
        self.assertFalse(self.can_reach_region("Shifting Sand Land - Upper Pyramid"))

        self.collect([
            self.get_item_by_name("Koopa Shell Blocks"),
            self.get_item_by_name("Shifting Sand Land - Pyramid Elevator"),
        ])
        self.assertTrue(self.can_reach_region("Shifting Sand Land - Upper Pyramid"))

    def test_side_flip_trick_reaches_upper_pyramid(self):
        self.collect_basement_access()
        self.collect(self.get_item_by_name("Side Flip"))
        self.assertFalse(self.can_reach_region("Shifting Sand Land - Upper Pyramid"))

        self.collect(self.get_item_by_name("Shifting Sand Land - Pyramid Elevator"))
        self.assertTrue(self.can_reach_region("Shifting Sand Land - Upper Pyramid"))

    def test_stand_tall_requires_eyerok(self):
        self.collect_basement_access()
        self.collect([
            self.get_item_by_name("Shifting Sand Land - Pyramid Elevator"),
            self.get_item_by_name("Climb"),
        ])
        self.assertTrue(self.can_reach_region("Shifting Sand Land - Upper Pyramid"))
        self.assertFalse(self.can_reach_location("Shifting Sand Land - Stand Tall on the Four Pillars"))

        self.collect(self.get_item_by_name("Shifting Sand Land - Eyerok"))
        self.assertFalse(self.can_reach_location("Shifting Sand Land - Stand Tall on the Four Pillars"))

    def test_stand_tall_trick_bypasses_upper_pyramid_and_elevator(self):
        self.collect_basement_access()
        self.collect([
            self.get_item_by_name("Shifting Sand Land - Eyerok"),
            self.get_item_by_name("Ledge Grab"),
        ])
        self.assertFalse(self.can_reach_region("Shifting Sand Land - Upper Pyramid"))
        self.assertTrue(self.can_reach_location("Shifting Sand Land - Stand Tall on the Four Pillars"))

    def test_stand_tall_is_in_eyerok_arena_inside_the_pyramid(self):
        location = self.multiworld.get_location(
            "Shifting Sand Land - Stand Tall on the Four Pillars", self.player)
        self.assertEqual("Shifting Sand Land - Eyerok Arena", location.parent_region.name)
        self.assertEqual(
            "Shifting Sand Land - Pyramid",
            location.parent_region.entrances[0].parent_region.name,
        )


class ShiftingSandLandRedCoinTricksTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_ARBITRARY_FEATURE_OPTIONS,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "level_unlocks": Options.LevelUnlocks.option_special_only,
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
                "coin_object_unlocks": Options.CoinObjectUnlocks.option_not_shuffled,
        "enemy_unlocks": Options.EnemyUnlocks.option_per_level,
        "logic_tricks": {
            "Shifting Sand Land Three Red Coins with Tweesters",
            "Shifting Sand Land One Red Coin with Spin Jump",
        },
    }

    def test_red_coin_tricks_are_counted_independently(self):
        self.collect_by_name([
            "Progressive Basement Key",
            "Shifting Sand Land - Bob-ombs",
            "Shifting Sand Land - Goombas",
            "Shifting Sand Land - Pokeys",
            "Shifting Sand Land - Tweesters",
        ])
        self.assertTrue(shifting_sand_land_coins(self.multiworld.state, self.player, 76))
        self.assertFalse(shifting_sand_land_coins(self.multiworld.state, self.player, 77))
        self.assertFalse(self.can_reach_location("Shifting Sand Land - Free Flying for 8 Red Coins"))

        self.collect(self.get_item_by_name("Shifting Sand Land - Fly Guys"))
        self.assertTrue(shifting_sand_land_coins(self.multiworld.state, self.player, 83))
        self.assertTrue(shifting_sand_land_coins(self.multiworld.state, self.player, 84))
        self.assertFalse(shifting_sand_land_coins(self.multiworld.state, self.player, 85))
        self.assertTrue(self.can_reach_location("Shifting Sand Land - Free Flying for 8 Red Coins"))


class ShiftingSandLandShyGuyRedCoinNoDespawnsTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_ARBITRARY_FEATURE_OPTIONS,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "level_unlocks": Options.LevelUnlocks.option_special_only,
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
                "coin_object_unlocks": Options.CoinObjectUnlocks.option_not_shuffled,
        "enemy_unlocks": Options.EnemyUnlocks.option_per_level,
        "no_despawns": Options.NoDespawns.option_true,
        "logic_tricks": {
            "Shifting Sand Land Three Red Coins with Tweesters",
            "Shifting Sand Land One Red Coin with Spin Jump",
        },
    }

    def test_shy_guy_red_coin_counts_with_no_despawns(self):
        self.collect_by_name([
            "Progressive Basement Key",
            "Shifting Sand Land - Bob-ombs",
            "Shifting Sand Land - Fly Guys",
            "Shifting Sand Land - Goombas",
            "Shifting Sand Land - Pokeys",
            "Shifting Sand Land - Tweesters",
        ])
        self.assertTrue(shifting_sand_land_coins(self.multiworld.state, self.player, 84))
        self.assertFalse(shifting_sand_land_coins(self.multiworld.state, self.player, 85))


class ShiftingSandLandIndividualUnlockLogicTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "coin_object_unlocks": Options.CoinObjectUnlocks.option_per_level,
        "coin_checks": 100,
        "enemy_unlocks": Options.EnemyUnlocks.option_per_level,
        "level_unlocks": Options.LevelUnlocks.option_special_only,
            }

    def get_isolated_coin_total(
            self,
            item_names: list[str],
            reachable_regions: set[str] | None = None,
    ) -> int:
        state = CollectionState(self.multiworld)
        for item_name in item_names:
            state.collect(self.world.create_item(item_name), prevent_sweep=True)

        if reachable_regions is not None:
            class RegionRestrictedState:
                def can_reach(self, spot, *args, **kwargs):
                    return getattr(spot, "name", spot) in reachable_regions

                def can_reach_region(self, region, *args, **kwargs):
                    return getattr(region, "name", region) in reachable_regions

                def __getattr__(self, name):
                    return getattr(state, name)

            evaluation_state = RegionRestrictedState()
        else:
            evaluation_state = state
        return COIN_EVALUATORS["Shifting Sand Land"](
            evaluation_state, self.player, 136).reachable_coins

    def test_initial_coin_sources_are_counted_independently(self):
        source_coins = {
            "Shifting Sand Land - Single Yellow Coins": 3,
            "Shifting Sand Land - Horizontal Coin Lines": 10,
            "Shifting Sand Land - Throwable Cork Box": 3,
            "Shifting Sand Land - Crazy Boxes": 10,
            "Shifting Sand Land - Red Coins": 8,
            "Shifting Sand Land - Bob-ombs": 2,
            "Shifting Sand Land - Fly Guys": 6,
            "Shifting Sand Land - Goombas": 3,
            "Shifting Sand Land - Pokeys": 20,
        }
        for item_name, expected_coins in source_coins.items():
            with self.subTest(item=item_name):
                self.assertEqual(
                    expected_coins,
                    self.get_isolated_coin_total(
                        [item_name], {"Shifting Sand Land"}),
                )

    def test_pyramid_goombas_require_access_to_the_pyramid(self):
        self.collect_by_name([
            "Progressive Basement Key",
            "Shifting Sand Land - Goombas",
        ])
        self.assertTrue(self.can_reach_region("Shifting Sand Land - Pyramid"))
        self.assertEqual(
            12,
            COIN_EVALUATORS["Shifting Sand Land"](
                self.multiworld.state, self.player, 136).reachable_coins,
        )

    def test_upper_pyramid_coin_sources(self):
        self.collect_by_name([
            "Progressive Basement Key",
            "Climb",
        ])
        self.assertTrue(self.can_reach_region("Shifting Sand Land - Upper Pyramid"))

        source_coins = {
            "Shifting Sand Land - Single Yellow Coins": 18,
            "Shifting Sand Land - Horizontal Coin Lines": 20,
            "Shifting Sand Land - Vertical Coin Lines": 4,
            "Shifting Sand Land - Horizontal Coin Rings": 8,
        }
        for item_name, expected_coins in source_coins.items():
            with self.subTest(item=item_name):
                self.assertEqual(
                    expected_coins,
                    self.get_isolated_coin_total([
                        "Progressive Basement Key", "Climb", item_name,
                    ]),
                )

    def test_pyramid_and_pillar_coin_checks_use_their_physical_regions(self):
        self.collect_by_name([
            "Progressive Basement Key",
            "Shifting Sand Land - Single Yellow Coins",
        ])
        for index in range(1, 3):
            self.assertTrue(self.can_reach_location(
                f"Shifting Sand Land - Inside Pyramid Coin {index}"))
        for index in range(1, 4):
            self.assertTrue(self.can_reach_location(
                f"Shifting Sand Land - Pillar Coin {index}"))
        self.assertFalse(self.can_reach_location(
            "Shifting Sand Land - Quicksand Pillar Coin"))

        self.collect_by_name(["Triple Jump", "Wing Cap", "Ground Pound"])
        for index in range(1, 4):
            self.assertTrue(self.can_reach_location(
                f"Shifting Sand Land - Pillar Coin {index}"))
        self.assertTrue(self.can_reach_location(
            "Shifting Sand Land - Quicksand Pillar Coin"))

    def test_blue_coin_block_requires_ground_pound(self):
        self.collect(self.get_item_by_name("Progressive Basement Key"))
        self.collect(self.get_item_by_name("Shifting Sand Land - Blue Coin Block"))
        self.assertFalse(shifting_sand_land_coins(self.multiworld.state, self.player, 1))

        self.collect(self.get_item_by_name("Ground Pound"))
        self.assertTrue(shifting_sand_land_coins(self.multiworld.state, self.player, 15))
        self.assertFalse(shifting_sand_land_coins(self.multiworld.state, self.player, 16))

    def test_red_coin_star_requires_red_coins(self):
        self.collect_by_name([
            "Progressive Basement Key",
            "Triple Jump",
            "Wing Cap",
        ])
        self.assertFalse(
            self.can_reach_location("Shifting Sand Land - Free Flying for 8 Red Coins"))

        self.collect(self.get_item_by_name("Shifting Sand Land - Red Coins"))
        self.assertTrue(
            self.can_reach_location("Shifting Sand Land - Free Flying for 8 Red Coins"))
        self.assertTrue(shifting_sand_land_coins(self.multiworld.state, self.player, 16))
        self.assertFalse(shifting_sand_land_coins(self.multiworld.state, self.player, 17))

    def test_all_unlocks_total_136_coins(self):
        self.collect_by_name([
            "Progressive Basement Key",
            "Climb",
            "Ground Pound",
            "Triple Jump",
            "Wing Cap",
            "Shifting Sand Land - Single Yellow Coins",
            "Shifting Sand Land - Red Coins",
            "Shifting Sand Land - Blue Coin Block",
            "Shifting Sand Land - Horizontal Coin Lines",
            "Shifting Sand Land - Horizontal Coin Rings",
            "Shifting Sand Land - Vertical Coin Lines",
            "Shifting Sand Land - Throwable Cork Box",
            "Shifting Sand Land - Crazy Boxes",
            "Shifting Sand Land - Bob-ombs",
            "Shifting Sand Land - Fly Guys",
            "Shifting Sand Land - Goombas",
            "Shifting Sand Land - Pokeys",
        ])
        self.assertTrue(shifting_sand_land_coins(self.multiworld.state, self.player, 136))


class ShiftingSandLandCoinStarAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_ARBITRARY_FEATURE_OPTIONS,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "level_unlocks": Options.LevelUnlocks.option_special_only,
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
                "coin_object_unlocks": Options.CoinObjectUnlocks.option_not_shuffled,
        "enemy_unlocks": Options.EnemyUnlocks.option_not_shuffled,
    }

    def collect_basement_access(self):
        self.collect(self.get_item_by_name("Progressive Basement Key"))


class ShiftingSandLandCoinStar77AccessTestBase(ShiftingSandLandCoinStarAccessTestBase):
    options = {
        **ShiftingSandLandCoinStarAccessTestBase.options,
        "shifting_sand_land_coin_star_requirement": 77,
    }

    def test_pillar_route_reaches_coin_star(self):
        self.collect_basement_access()
        self.assertFalse(self.can_reach_location("Shifting Sand Land - Coins Star"))

        self.collect_by_name(["Triple Jump", "Wing Cap", "Ground Pound"])
        self.assertTrue(self.can_reach_location("Shifting Sand Land - Coins Star"))


class ShiftingSandLandCoinStar85AccessTestBase(ShiftingSandLandCoinStarAccessTestBase):
    options = {
        **ShiftingSandLandCoinStarAccessTestBase.options,
        "shifting_sand_land_coin_star_requirement": 85,
    }

    def test_red_coin_star_coins_reach_coin_star(self):
        self.collect_basement_access()
        self.assertFalse(self.can_reach_location("Shifting Sand Land - Coins Star"))

        self.collect([
            self.get_item_by_name("Triple Jump"),
            self.get_item_by_name("Wing Cap"),
        ])
        self.assertTrue(self.can_reach_location("Shifting Sand Land - Free Flying for 8 Red Coins"))
        self.assertFalse(self.can_reach_location("Shifting Sand Land - Coins Star"))

        self.collect(self.get_item_by_name("Ground Pound"))
        self.assertTrue(self.can_reach_location("Shifting Sand Land - Coins Star"))


class ShiftingSandLandCoinStar92AccessTestBase(ShiftingSandLandCoinStarAccessTestBase):
    options = {
        **ShiftingSandLandCoinStarAccessTestBase.options,
        "shifting_sand_land_coin_star_requirement": 92,
    }

    def test_ground_pound_coins_reach_coin_star(self):
        self.collect_basement_access()
        self.assertFalse(self.can_reach_location("Shifting Sand Land - Coins Star"))

        self.collect(self.get_item_by_name("Ground Pound"))
        self.assertFalse(self.can_reach_location("Shifting Sand Land - Coins Star"))

        self.collect_by_name(["Triple Jump", "Wing Cap"])
        self.assertTrue(self.can_reach_location("Shifting Sand Land - Coins Star"))


class ShiftingSandLandCoinStar121AccessTestBase(ShiftingSandLandCoinStarAccessTestBase):
    options = {
        **ShiftingSandLandCoinStarAccessTestBase.options,
        "shifting_sand_land_coin_star_requirement": 121,
    }

    def test_upper_pyramid_coins_reach_coin_star(self):
        self.collect_basement_access()
        self.assertFalse(self.can_reach_location("Shifting Sand Land - Coins Star"))

        self.collect([
            self.get_item_by_name("Shifting Sand Land - Pyramid Elevator"),
            self.get_item_by_name("Climb"),
            self.get_item_by_name("Triple Jump"),
            self.get_item_by_name("Wing Cap"),
        ])
        self.assertTrue(self.can_reach_region("Shifting Sand Land - Upper Pyramid"))
        self.assertFalse(self.can_reach_location("Shifting Sand Land - Coins Star"))

        self.collect(self.get_item_by_name("Ground Pound"))
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
            self.get_item_by_name("Climb"),
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
        "level_unlocks": Options.LevelUnlocks.option_special_only,
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
                "start_inventory": {"Koopa Shell Blocks": 1},
    }

    def collect_second_floor_access(self):
        self.collect(self.get_item_by_name("Progressive Upstairs Key"))


class SnowmansLandCoinStar97AccessTestBase(SnowmansLandCoinStarAccessTestBase):
    options = {
        **SnowmansLandCoinStarAccessTestBase.options,
        "snowmans_land_coin_star_requirement": 97,
    }

    def test_upper_region_coins_reach_coin_star(self):
        self.collect_second_floor_access()
        self.assertTrue(self.can_reach_location("Snowman's Land - Coins Star"))


class SnowmansLandCoinStar100AccessTestBase(SnowmansLandCoinStarAccessTestBase):
    options = {
        **SnowmansLandCoinStarAccessTestBase.options,
        "snowmans_land_coin_star_requirement": 100,
    }

    def test_cannon_reaches_last_mr_blizzard_coins(self):
        self.collect_second_floor_access()
        self.assertTrue(self.can_reach_location("Snowman's Land - Coins Star"))

        self.collect(self.get_item_by_name("Snowman's Land - Cannon Unlock"))
        self.assertTrue(self.can_reach_location("Snowman's Land - Coins Star"))


class SnowmansLandCoinStar100NoDespawnsAccessTestBase(SnowmansLandCoinStarAccessTestBase):
    options = {
        **SnowmansLandCoinStarAccessTestBase.options,
        "snowmans_land_coin_star_requirement": 100,
        "no_despawns": Options.NoDespawns.option_true,
    }

    def test_no_despawns_reaches_last_mr_blizzard_coins_without_cannon(self):
        self.collect_second_floor_access()
        self.assertTrue(self.can_reach_location("Snowman's Land - Coins Star"))


class SnowmansLandCoinStar126AccessTestBase(SnowmansLandCoinStarAccessTestBase):
    options = {
        **SnowmansLandCoinStarAccessTestBase.options,
        "snowmans_land_coin_star_requirement": 126,
    }

    def test_igloo_coins_reach_coin_star(self):
        self.collect_second_floor_access()
        self.assertFalse(self.can_reach_location("Snowman's Land - Coins Star"))

        self.collect_by_name([
            "Vanish Cap",
            "Wall Kick",
            "Snowman's Land - Cannon Unlock",
        ])
        self.assertTrue(self.can_reach_location("Snowman's Land - Into the Igloo"))
        self.assertTrue(self.can_reach_location("Snowman's Land - Coins Star"))


class SnowmansLandImpossibleCoinLogicTestBase(SnowmansLandCoinStarAccessTestBase):
    options = {
        **SnowmansLandCoinStarAccessTestBase.options,
        "accessibility": "minimal",
        "snowmans_land_coin_star_requirement": 127,
    }

    def test_127_coins_are_out_of_logic_without_trick(self):
        self.collect_second_floor_access()
        self.collect_by_name([
            "Snowman's Land - Cannon Unlock",
            "Vanish Cap",
            "Wall Kick",
        ])
        self.assertTrue(self.can_reach_location("Snowman's Land - Into the Igloo"))
        self.assertFalse(self.can_reach_location("Snowman's Land - Coins Star"))


class SnowmansLandImpossibleCoinEnabledTestBase(SnowmansLandCoinStarAccessTestBase):
    options = {
        **SnowmansLandCoinStarAccessTestBase.options,
        "accessibility": "minimal",
        "logic_tricks": {"Snowman's Land Impossible Coin"},
        "snowmans_land_coin_star_requirement": 127,
    }

    def test_trick_and_cannon_reach_127_coins(self):
        self.collect_second_floor_access()
        self.collect_by_name(["Vanish Cap", "Wall Kick"])
        self.assertFalse(self.can_reach_location("Snowman's Land - Coins Star"))

        self.collect(self.get_item_by_name("Snowman's Land - Cannon Unlock"))
        self.assertTrue(self.can_reach_location("Snowman's Land - Coins Star"))


class SnowmansLandImpossibleCoinFullAccessibilityCapTestBase(SnowmansLandCoinStarAccessTestBase):
    options = {
        **SnowmansLandCoinStarAccessTestBase.options,
        "accessibility": "full",
        "snowmans_land_coin_star_requirement": 127,
    }

    def test_full_accessibility_caps_requirement_at_126(self):
        self.assertEqual(self.world.options.snowmans_land_coin_star_requirement.value, 126)
        self.assertEqual(self.world.get_coin_star_requirements_slot_data()[9], 126)


class SnowmansLandRegionAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "blocksanity": Options.Blocksanity.option_true,
        "buddy_checks": Options.BuddyChecks.option_true,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "level_unlocks": Options.LevelUnlocks.option_special_only,
        "enemy_unlocks": Options.EnemyUnlocks.option_per_level,
        "one_up_checks": Options.OneUpChecks.option_true,
            }

    def collect_second_floor_access(self):
        self.collect(self.get_item_by_name("Progressive Upstairs Key"))

    def test_spindrift_opens_whirl_and_upper(self):
        self.collect_second_floor_access()
        self.assertFalse(self.multiworld.state.has("Snowman's Land - Spindrifts", self.player))
        self.assertFalse(self.multiworld.state.has("Snowman's Land - Cannon Unlock", self.player))
        self.assertEqual(self.world.options.enemy_unlocks.value, Options.EnemyUnlocks.option_per_level)
        self.assertFalse(
            self.multiworld.get_region("Snowman's Land - Whirl from the Freezing Pond", self.player)
            .entrances[0].access_rule(self.multiworld.state))
        self.assertFalse(self.can_reach_region("Snowman's Land - Whirl from the Freezing Pond"))
        self.assertFalse(self.can_reach_region("Snowman's Land - Upper"))

        self.collect(self.get_item_by_name("Snowman's Land - Spindrifts"))
        self.assertTrue(self.can_reach_region("Snowman's Land - Whirl from the Freezing Pond"))
        self.assertTrue(self.can_reach_region("Snowman's Land - Upper"))

    def test_movement_can_reach_upper_without_whirl(self):
        self.collect_second_floor_access()
        self.collect(self.get_item_by_name("Triple Jump"))
        self.assertFalse(self.can_reach_region("Snowman's Land - Whirl from the Freezing Pond"))
        self.assertTrue(self.can_reach_region("Snowman's Land - Upper"))
        self.assertFalse(self.can_reach_entrance("Snowman's Land - Igloo Approach"))

    def test_top_of_snowmans_head_reaches_igloo_without_whirl(self):
        self.collect_second_floor_access()
        self.collect_by_name([
            "Snowman's Land - Penguin",
            "Backflip",
        ])
        self.assertFalse(self.can_reach_region("Snowman's Land - Whirl from the Freezing Pond"))
        self.assertTrue(self.can_reach_region("Snowman's Land - Top of Snowman's Head"))
        self.assertTrue(self.can_reach_region("Snowman's Land - Igloo Entrance"))
        self.assertTrue(self.can_reach_region("Snowman's Land - Igloo"))

    def test_cannon_reaches_upper_top_and_igloo(self):
        self.collect_second_floor_access()
        self.collect(self.get_item_by_name("Snowman's Land - Cannon Unlock"))
        self.assertTrue(self.can_reach_region("Snowman's Land - Upper"))
        self.assertTrue(self.can_reach_region("Snowman's Land - Top of Snowman's Head"))
        self.assertTrue(self.can_reach_region("Snowman's Land - Igloo"))

    def test_spindrift_shell_route_reaches_igloo(self):
        self.collect_second_floor_access()
        self.collect(self.get_item_by_name("Snowman's Land - Spindrifts"))
        self.assertTrue(self.can_reach_region("Snowman's Land - Whirl from the Freezing Pond"))
        self.assertFalse(self.can_reach_region("Snowman's Land - Top of Snowman's Head"))
        self.assertTrue(self.can_reach_region("Snowman's Land - Igloo"))

    def test_locations_are_in_requested_regions(self):
        whirl_locations = (
            "Snowman's Land - Whirl from the Freezing Pond",
            "Snowman's Land - Koopa Shell Block",
            "Snowman's Land - Shell Shreddin' for Red Coins",
            "Snowman's Land - Whirl from the Freezing Pond Star Block",
        )
        top_locations = (
            "Snowman's Land - Snowman's Big Head",
            "Snowman's Land - Snowman Tree 1-Up",
        )
        igloo_locations = (
            "Snowman's Land - Into the Igloo",
            "Snowman's Land - Bob-omb Buddy",
            "Snowman's Land - Inside Igloo Block 1-Up",
            "Snowman's Land - Igloo Ice Block 1-Up",
            "Snowman's Land - Inside Igloo 1-Up Block",
            "Snowman's Land - Vanish Cap Block",
            "Snowman's Land - 3 Coins Block",
        )
        for location_name in whirl_locations:
            self.assertEqual(
                self.multiworld.get_location(location_name, self.player).parent_region.name,
                "Snowman's Land - Whirl from the Freezing Pond")
        for location_name in top_locations:
            self.assertEqual(
                self.multiworld.get_location(location_name, self.player).parent_region.name,
                "Snowman's Land - Top of Snowman's Head")
        for location_name in igloo_locations:
            self.assertEqual(
                self.multiworld.get_location(location_name, self.player).parent_region.name,
                "Snowman's Land - Igloo")


class SnowmansLandIndividualUnlockLogicTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_ARBITRARY_FEATURE_OPTIONS,
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "accessibility": "minimal",
        "buddy_checks": Options.BuddyChecks.option_true,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "coin_object_unlocks": Options.CoinObjectUnlocks.option_per_level,
        "level_unlocks": Options.LevelUnlocks.option_special_only,
        "enemy_unlocks": Options.EnemyUnlocks.option_per_level,
        "logic_tricks": {"Snowman's Land Impossible Coin"},
            }

    def get_full_snowmans_land_route_state(self):
        state = CollectionState(self.multiworld)
        for item_name in [
            "Progressive Upstairs Key",
            "Triple Jump",
            "Wall Kick",
            "Vanish Cap",
            "Snowman's Land - Cannon Unlock",
            "Freestanding Stars",
            "Koopa Shell Blocks",
        ]:
            state.collect(self.world.create_item(item_name))
        self.assertTrue(self.world.logic_sl_impossible_coin)
        self.assertTrue(state.has("Snowman's Land - Cannon Unlock", self.player))
        self.assertTrue(can_use_logic_trick(
            state, self.player, "logic_sl_impossible_coin", "Snowman's Land - Coins Star"))
        self.assertTrue(state.can_reach("Snowman's Land - Upper", "Region", self.player))
        self.assertTrue(state.can_reach("Snowman's Land - Into the Igloo", "Location", self.player))
        return state

    def test_each_unlock_matches_documented_total(self):
        source_coins = {
            "Snowman's Land - Single Yellow Coins": 14,
            "Snowman's Land - Red Coins": 16,
            "Snowman's Land - Horizontal Coin Lines": 25,
            "Snowman's Land - 3-Coin Block": 3,
            "Snowman's Land - Fly Guy": 2,
            "Snowman's Land - Goombas": 3,
            "Snowman's Land - Moneybags": 10,
            "Snowman's Land - Mr Blizzards": 12,
            "Snowman's Land - Spindrifts": 42,
        }
        for item_name, expected_coins in source_coins.items():
            with self.subTest(item=item_name):
                state = self.get_full_snowmans_land_route_state()
                state.collect(self.world.create_item(item_name))
                actual_coins = max(
                    coin_count for coin_count in range(128)
                    if snowmans_land_coins(state, self.player, coin_count)
                )
                self.assertEqual(actual_coins, expected_coins)

    def test_all_unlocks_total_127_coins(self):
        state = self.get_full_snowmans_land_route_state()
        for item_name in [
            "Snowman's Land - Single Yellow Coins",
            "Snowman's Land - Red Coins",
            "Snowman's Land - Horizontal Coin Lines",
            "Snowman's Land - 3-Coin Block",
            "Snowman's Land - Fly Guy",
            "Snowman's Land - Goombas",
            "Snowman's Land - Moneybags",
            "Snowman's Land - Mr Blizzards",
            "Snowman's Land - Spindrifts",
        ]:
            state.collect(self.world.create_item(item_name))
        self.assertTrue(snowmans_land_coins(
            state, self.player, 127))

    def test_enemy_checks_require_their_unlocks(self):
        self.collect(self.get_item_by_name("Progressive Upstairs Key"))
        self.assertFalse(self.can_reach_region("Snowman's Land - Whirl from the Freezing Pond"))
        self.collect(self.get_item_by_name("Snowman's Land - Spindrifts"))
        self.assertTrue(self.can_reach_region("Snowman's Land - Whirl from the Freezing Pond"))

        self.assertFalse(self.can_reach_location("Snowman's Land - Chill with the Bully"))
        self.collect(self.get_item_by_name("Snowman's Land - Chill Bully"))
        self.assertTrue(self.can_reach_location("Snowman's Land - Chill with the Bully"))

    def test_slope_single_coins_split_between_main_and_highest_coin_routes(self):
        state = CollectionState(self.multiworld)
        state.collect(self.world.create_item("Progressive Upstairs Key"), prevent_sweep=True)
        state.collect(
            self.world.create_item("Snowman's Land - Single Yellow Coins"), prevent_sweep=True)
        self.assertEqual(
            max(coins for coins in range(128)
                if snowmans_land_coins(state, self.player, coins)),
            4,
        )

        state.collect(self.world.create_item("Long Jump"), prevent_sweep=True)
        self.assertEqual(
            max(coins for coins in range(128)
                if snowmans_land_coins(state, self.player, coins)),
            5,
        )


class SnowmansLandIglooShellCoinLossTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
                "buddy_checks": Options.BuddyChecks.option_true,
        "coin_object_unlocks": Options.CoinObjectUnlocks.option_per_level,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "level_unlocks": Options.LevelUnlocks.option_special_only,
        "enemy_unlocks": Options.EnemyUnlocks.option_per_level,
        "no_despawns": Options.NoDespawns.option_true,
    }

    def test_shell_transition_preserves_spindrift_coins(self):
        self.collect_by_name([
            "Progressive Upstairs Key",
            "Snowman's Land - Spindrifts",
        ])
        self.assertTrue(self.can_reach_region("Snowman's Land - Igloo"))
        self.assertFalse(self.can_reach_region("Snowman's Land - Top of Snowman's Head"))
        coins_before_igloo_block = max(
            coin_count for coin_count in range(128)
            if snowmans_land_coins(self.multiworld.state, self.player, coin_count)
        )

        self.collect(self.get_item_by_name("Snowman's Land - 3-Coin Block"))
        coins_after_igloo_block = max(
            coin_count for coin_count in range(128)
            if snowmans_land_coins(self.multiworld.state, self.player, coin_count)
        )
        self.assertEqual(coins_after_igloo_block, coins_before_igloo_block + 3)

        self.collect(self.get_item_by_name("Snowman's Land - Cannon Unlock"))
        self.assertTrue(self.can_reach_region("Snowman's Land - Top of Snowman's Head"))
        coins_after_cannon = max(
            coin_count for coin_count in range(128)
            if snowmans_land_coins(self.multiworld.state, self.player, coin_count)
        )
        self.assertEqual(coins_after_cannon, coins_after_igloo_block)


class SnowmansLandIglooPermanentCoinCollectionTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SnowmansLandIglooShellCoinLossTestBase.options,
    }

    def test_permanent_collection_preserves_spindrift_coins_across_igloo_transition(self):
        self.collect_by_name([
            "Progressive Upstairs Key",
            "Snowman's Land - Spindrifts",
        ])
        self.collect(self.world.create_item("Koopa Shell Blocks"))
        coins_before_igloo_block = max(
            coin_count for coin_count in range(128)
            if snowmans_land_coins(self.multiworld.state, self.player, coin_count)
        )

        self.collect(self.get_item_by_name("Snowman's Land - 3-Coin Block"))
        coins_after_igloo_block = max(
            coin_count for coin_count in range(128)
            if snowmans_land_coins(self.multiworld.state, self.player, coin_count)
        )
        self.assertEqual(coins_after_igloo_block, coins_before_igloo_block + 3)


class WetDryWorldCoinStarAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_ARBITRARY_FEATURE_OPTIONS,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "level_unlocks": Options.LevelUnlocks.option_special_only,
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
            }

    def collect_second_floor_access(self):
        self.collect(self.get_item_by_name("Progressive Upstairs Key"))

    def disable_wdw_entrance(self, entrance_name: str):
        self.multiworld.get_entrance(f"Second Floor -> {entrance_name}", self.player).access_rule = \
            lambda state: False


class WetDryWorldFirstDowntownRedCoinAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **WetDryWorldCoinStarAccessTestBase.options,
        "coin_object_unlocks": Options.CoinObjectUnlocks.option_per_level,
        "bobomb_buddies": Options.BobombBuddies.option_per_level,
        "logic_tricks": {
            "Wet-Dry World Downtown with Triple Jump",
            "Wet-Dry World High Red Coins with Triple Jump",
        },
    }

    def make_state(self, item_names, starting_region):
        state = CollectionState(self.multiworld)
        for item_name in item_names:
            item = item_name if not isinstance(item_name, str) else self.world.create_item(item_name)
            item.classification = ItemClassification.progression
            state.collect(item, prevent_sweep=True)
        region = self.multiworld.get_region(starting_region, self.player)
        state.reachable_regions[self.player].add(region)
        for entrance in region.exits:
            if entrance.connected_region is not None:
                state.blocked_connections[self.player].add(entrance)
        state.sweep_for_advancements()
        return state

    def first_downtown_red_coin_is_available(self, state):
        return self.coin_source_is_available(state, "downtown_diamond_red_coins")

    def coin_source_is_available(self, state, source_id):
        evaluation = COIN_EVALUATORS["Wet-Dry World"](state, self.player, 152)
        return any(
            source.available
            for source in evaluation.children
            if source.source_id == source_id
        )

    def test_expected_access_routes(self):
        cases = []
        for red_coins in ("Red Coins", "Wet-Dry World - Red Coins"):
            cases.append(("Wet-Dry World - Low Water", [
                red_coins, "Wet-Dry World - Cannon Unlock",
                "Wet-Dry World - Water Level Diamond"]))
            cases.extend((
                ("Wet-Dry World - Highest Water", [
                    red_coins, "Ledge Grab", "Wet-Dry World - Water Level Diamond"]),
                ("Wet-Dry World - Mid Water", [
                    red_coins, "Triple Jump", "Wet-Dry World - Water Level Diamond"]),
            ))
        for starting_region, item_names in cases:
            with self.subTest(starting_region=starting_region, items=item_names):
                state = self.make_state(item_names, starting_region)
                self.assertTrue(self.first_downtown_red_coin_is_available(state))

    def test_all_items_without_red_coin_unlock_do_not_reach_first_red_coin(self):
        items = [
            item for item in self.multiworld.get_items()
            if item.name not in {"Red Coins", "Wet-Dry World - Red Coins"}
        ]
        state = self.make_state(items, "Wet-Dry World - Highest Water")
        self.assertFalse(self.first_downtown_red_coin_is_available(state))

    def test_all_items_without_downtown_access_do_not_reach_first_red_coin(self):
        downtown_access_item_names = {
            "Wet-Dry World - Cannon Unlock",
            "Triple Jump",
            "Side Flip",
            "Backflip",
        }
        items = [
            item for item in self.multiworld.get_items()
            if item.name not in downtown_access_item_names
        ]
        items.append(self.world.create_item("Wet-Dry World - Red Coins"))
        state = self.make_state(items, "Wet-Dry World - Low Water")
        self.assertFalse(self.first_downtown_red_coin_is_available(state))

    def test_all_items_without_water_level_diamond_do_not_reach_first_red_coin(self):
        items = [
            item for item in self.multiworld.get_items()
            if item.name not in {"Water Level Diamond", "Wet-Dry World - Water Level Diamond"}
        ]
        state = self.make_state(items, "Wet-Dry World - Highest Water")
        self.assertFalse(self.first_downtown_red_coin_is_available(state))

    def test_downtown_red_coin_specific_requirements(self):
        red_coins = "Wet-Dry World - Red Coins"
        diamond = "Wet-Dry World - Water Level Diamond"

        state = self.make_state([red_coins, diamond], "Wet-Dry World - Downtown")
        self.assertTrue(self.coin_source_is_available(state, "downtown_diamond_red_coins"))
        self.assertFalse(self.coin_source_is_available(state, "downtown_brown_brick_red_coin"))
        self.assertFalse(self.coin_source_is_available(state, "downtown_beige_building_red_coin"))
        self.assertFalse(self.coin_source_is_available(state, "downtown_chapel_roof_red_coin"))

        for movement in ("Long Jump", "Dive"):
            with self.subTest(movement=movement):
                state = self.make_state([red_coins, diamond, movement], "Wet-Dry World - Downtown")
                self.assertTrue(self.coin_source_is_available(state, "downtown_brown_brick_red_coin"))
                self.assertFalse(self.coin_source_is_available(state, "downtown_beige_building_red_coin"))
                self.assertFalse(self.coin_source_is_available(state, "downtown_chapel_roof_red_coin"))

        for movement in ("Wall Kick", "Triple Jump"):
            with self.subTest(movement=movement):
                state = self.make_state([red_coins, diamond, movement], "Wet-Dry World - Downtown")
                self.assertTrue(self.coin_source_is_available(state, "downtown_brown_brick_red_coin"))
                self.assertTrue(self.coin_source_is_available(state, "downtown_beige_building_red_coin"))
                self.assertTrue(self.coin_source_is_available(state, "downtown_chapel_roof_red_coin"))

        state = self.make_state([red_coins, "Wall Kick"], "Wet-Dry World - Downtown")
        self.assertFalse(self.coin_source_is_available(state, "downtown_diamond_red_coins"))
        self.assertFalse(self.coin_source_is_available(state, "downtown_brown_brick_red_coin"))
        self.assertFalse(self.coin_source_is_available(state, "downtown_beige_building_red_coin"))
        self.assertTrue(self.coin_source_is_available(state, "downtown_chapel_roof_red_coin"))


class WetDryWorldCoinStar49AccessTestBase(WetDryWorldCoinStarAccessTestBase):
    options = {
        **WetDryWorldCoinStarAccessTestBase.options,
        "wet_dry_world_coin_star_requirement": 49,
    }

    def test_low_water_start_coins_reach_coin_star(self):
        self.disable_wdw_entrance("Wet-Dry World Middle")
        self.disable_wdw_entrance("Wet-Dry World High")
        self.collect_second_floor_access()
        self.assertTrue(self.can_reach_region("Wet-Dry World - Low Water"))
        self.assertFalse(self.can_reach_location("Wet-Dry World - Coins Star"))

        self.collect_by_name(["Wet-Dry World - Cannon Unlock", "Purple Switches"])
        self.assertTrue(self.can_reach_location("Wet-Dry World - Coins Star"))


class WetDryWorldCoinStar50AccessTestBase(WetDryWorldCoinStarAccessTestBase):
    options = {
        **WetDryWorldCoinStarAccessTestBase.options,
        "wet_dry_world_coin_star_requirement": 50,
    }

    def test_low_water_ground_pound_coins_reach_coin_star(self):
        self.disable_wdw_entrance("Wet-Dry World Middle")
        self.disable_wdw_entrance("Wet-Dry World High")
        self.collect_second_floor_access()
        self.assertFalse(self.can_reach_location("Wet-Dry World - Coins Star"))

        self.collect(self.get_item_by_name("Ground Pound"))
        self.assertTrue(self.can_reach_location("Wet-Dry World - Coins Star"))


class WetDryWorldCoinStar30AccessTestBase(WetDryWorldCoinStarAccessTestBase):
    options = {
        **WetDryWorldCoinStarAccessTestBase.options,
        "wet_dry_world_coin_star_requirement": 30,
    }

    def test_mid_water_start_coins_reach_coin_star(self):
        self.disable_wdw_entrance("Wet-Dry World Low")
        self.disable_wdw_entrance("Wet-Dry World High")
        self.collect_second_floor_access()
        self.assertTrue(self.can_reach_region("Wet-Dry World - Mid Water"))
        self.assertFalse(self.can_reach_location("Wet-Dry World - Coins Star"))

        self.collect_by_name(["Wet-Dry World - Cannon Unlock", "Purple Switches"])
        self.assertTrue(self.can_reach_location("Wet-Dry World - Coins Star"))


class WetDryWorldCoinStar50PurpleSwitchAccessTestBase(WetDryWorldCoinStarAccessTestBase):
    options = {
        **WetDryWorldCoinStarAccessTestBase.options,
        "wet_dry_world_coin_star_requirement": 50,
    }

    def test_mid_water_purple_switch_coins_reach_coin_star(self):
        self.disable_wdw_entrance("Wet-Dry World Middle")
        self.disable_wdw_entrance("Wet-Dry World High")
        self.collect_second_floor_access()
        self.assertFalse(self.can_reach_location("Wet-Dry World - Coins Star"))

        self.collect(self.get_item_by_name("Purple Switches"))
        self.assertTrue(self.can_reach_location("Wet-Dry World - Coins Star"))


class WetDryWorldCoinStar84AccessTestBase(WetDryWorldCoinStarAccessTestBase):
    options = {
        **WetDryWorldCoinStarAccessTestBase.options,
        "wet_dry_world_coin_star_requirement": 84,
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


class WetDryWorldIndividualUnlockLogicTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_ARBITRARY_FEATURE_OPTIONS,
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "accessibility": "minimal",
        "blocksanity": Options.Blocksanity.option_true,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "coin_object_unlocks": Options.CoinObjectUnlocks.option_per_level,
        "level_unlocks": Options.LevelUnlocks.option_special_only,
        "enemy_unlocks": Options.EnemyUnlocks.option_per_level,
            }

    def get_full_wet_dry_world_route_state(self):
        state = CollectionState(self.multiworld)
        for item_name in [
            "Progressive Upstairs Key",
            "Ground Pound",
            "Long Jump",
            "Triple Jump",
            "Dive",
            "Ledge Grab",
            "Wall Kick",
            "Wet-Dry World - Purple Switch",
            "Wet-Dry World - Water Level Diamond",
            "Wet-Dry World - Cannon Unlock",
        ]:
            state.collect(self.world.create_item(item_name))
        return state

    def make_wdw_route_state(self, starting_region, item_names):
        state = CollectionState(self.multiworld)
        for item_name in item_names:
            state.collect(self.world.create_item(item_name), prevent_sweep=True)
        region = self.multiworld.get_region(starting_region, self.player)
        state.reachable_regions[self.player].add(region)
        for entrance in region.exits:
            if entrance.connected_region is not None:
                state.blocked_connections[self.player].add(entrance)
        state.sweep_for_advancements()
        return state

    def fourth_diamond_coin_line_is_available(self, state):
        evaluation = COIN_EVALUATORS["Wet-Dry World"](
            state, self.player, 152)
        return next(
            source.available
            for source in evaluation.children
            if source.source_id == "fourth_diamond_coin_line"
        )

    def test_fourth_diamond_coin_line_requires_highest_or_mid_high_route(self):
        self.multiworld.get_entrance(
            "Wet-Dry World - Top", self.player).access_rule = lambda state: False
        state = self.make_wdw_route_state(
            "Wet-Dry World - Mid Water",
            ["Wet-Dry World - Horizontal Coin Lines"],
        )
        self.assertFalse(self.fourth_diamond_coin_line_is_available(state))

        state.collect(self.world.create_item("Triple Jump"), prevent_sweep=True)
        state.sweep_for_advancements()
        self.assertFalse(self.fourth_diamond_coin_line_is_available(state))

        state.collect(self.world.create_item("Dive"), prevent_sweep=True)
        state.sweep_for_advancements()
        self.assertTrue(self.fourth_diamond_coin_line_is_available(state))

    def test_fourth_diamond_coin_line_accepts_purple_switch_route(self):
        state = self.make_wdw_route_state(
            "Wet-Dry World - Mid Water",
            ["Wet-Dry World - Horizontal Coin Lines", "Purple Switches"],
        )
        self.assertTrue(state.can_reach(
            "Wet-Dry World - Top of the Express Elevator", "Region", self.player))
        self.assertTrue(self.fourth_diamond_coin_line_is_available(state))

    def test_fourth_diamond_coin_line_accepts_highest_water(self):
        state = self.make_wdw_route_state(
            "Wet-Dry World - Highest Water",
            ["Wet-Dry World - Horizontal Coin Lines"],
        )
        self.assertTrue(self.fourth_diamond_coin_line_is_available(state))

    def test_fourth_diamond_coin_line_accepts_top(self):
        state = self.make_wdw_route_state(
            "Wet-Dry World - Top",
            ["Wet-Dry World - Horizontal Coin Lines"],
        )
        self.assertTrue(self.fourth_diamond_coin_line_is_available(state))

    def test_each_unlock_matches_documented_total(self):
        source_coins = {
            "Wet-Dry World - Red Coins": 16,
            "Wet-Dry World - Blue Coin Block": 30,
            "Wet-Dry World - Horizontal Coin Lines": 25,
            "Wet-Dry World - Horizontal Coin Rings": 16,
            "Wet-Dry World - Breakable Coin Boxes": 12,
            "Wet-Dry World - 3-Coin Blocks": 6,
            "Wet-Dry World - 10-Coin Blocks": 30,
            "Wet-Dry World - Chuckya": 5,
            "Wet-Dry World - Skeeters": 12,
        }
        for item_name, expected_coins in source_coins.items():
            with self.subTest(item=item_name):
                state = self.get_full_wet_dry_world_route_state()
                state.collect(self.world.create_item(item_name))
                actual_coins = max(
                    coin_count for coin_count in range(153)
                    if wet_dry_world_coins(state, self.player, coin_count)
                )
                self.assertEqual(actual_coins, expected_coins)

    def test_all_unlocks_total_152_coins(self):
        state = self.get_full_wet_dry_world_route_state()
        for item_name in [
            "Wet-Dry World - Red Coins",
            "Wet-Dry World - Blue Coin Block",
            "Wet-Dry World - Horizontal Coin Lines",
            "Wet-Dry World - Horizontal Coin Rings",
            "Wet-Dry World - Breakable Coin Boxes",
            "Wet-Dry World - 3-Coin Blocks",
            "Wet-Dry World - 10-Coin Blocks",
            "Wet-Dry World - Chuckya",
            "Wet-Dry World - Skeeters",
        ]:
            state.collect(self.world.create_item(item_name))
        self.assertTrue(wet_dry_world_coins(state, self.player, 152))

    def test_coin_blocks_require_their_unlock(self):
        self.multiworld.get_entrance(
            "Second Floor -> Wet-Dry World Middle", self.player).access_rule = lambda state: False
        self.multiworld.get_entrance(
            "Second Floor -> Wet-Dry World High", self.player).access_rule = lambda state: False
        self.collect(self.get_item_by_name("Progressive Upstairs Key"))
        three_coin_blocks = (
            "Wet-Dry World - Push Block 3 Coins Block",
            "Wet-Dry World - Wooden Structure 3 Coins Block",
        )
        ten_coin_blocks = (
            "Wet-Dry World - Push Block 10 Coins Block",
            "Wet-Dry World - Pedestal 10 Coins Block",
            "Wet-Dry World - Top of Express Elevator 10 Coins Block",
        )
        for location_name in (*three_coin_blocks, *ten_coin_blocks):
            self.assertFalse(self.can_reach_location(location_name))

        self.collect(self.get_item_by_name("Wet-Dry World - 3-Coin Blocks"))
        self.assertFalse(self.can_reach_location("Wet-Dry World - Push Block 3 Coins Block"))
        self.assertFalse(self.can_reach_location("Wet-Dry World - Wooden Structure 3 Coins Block"))
        for location_name in ten_coin_blocks:
            self.assertFalse(self.can_reach_location(location_name))

        self.collect(self.get_item_by_name("Wet-Dry World - Heave-Hos"))
        self.assertTrue(self.can_reach_location("Wet-Dry World - Push Block 3 Coins Block"))

        self.collect(self.get_item_by_name("Purple Switches"))
        self.collect_by_name(["Triple Jump", "Dive"])
        self.assertTrue(self.can_reach_location("Wet-Dry World - Wooden Structure 3 Coins Block"))

        self.collect(self.get_item_by_name("Wet-Dry World - Water Level Diamond"))
        self.assertTrue(self.can_reach_location("Wet-Dry World - Wooden Structure 3 Coins Block"))

        self.collect(self.get_item_by_name("Wet-Dry World - 10-Coin Blocks"))
        for location_name in ten_coin_blocks:
            self.assertTrue(self.can_reach_location(location_name))


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
            self.get_item_by_name("Wall Kick"),
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
        "level_unlocks": Options.LevelUnlocks.option_special_only,
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
            }

    def collect_second_floor_access(self):
        self.collect(self.get_item_by_name("Progressive Upstairs Key"))


class TallTallMountainCoinStar17AccessTestBase(TallTallMountainCoinStarAccessTestBase):
    options = {
        **TallTallMountainCoinStarAccessTestBase.options,
        "tall_tall_mountain_coin_star_requirement": 17,
    }

    def test_coins_above_start_require_middle_region(self):
        self.multiworld.get_entrance("Tall, Tall Mountain - Middle", self.player).access_rule = \
            lambda state: False
        self.collect_second_floor_access()
        self.assertTrue(self.can_reach_region("Tall, Tall Mountain"))
        self.assertFalse(self.can_reach_region("Tall, Tall Mountain - Middle"))
        self.assertFalse(self.can_reach_location("Tall, Tall Mountain - Coins Star"))


class TallTallMountainCoinStar43AccessTestBase(TallTallMountainCoinStarAccessTestBase):
    options = {
        **TallTallMountainCoinStarAccessTestBase.options,
        "tall_tall_mountain_coin_star_requirement": 43,
    }

    def test_start_coins_reach_coin_star(self):
        self.collect_second_floor_access()
        self.assertFalse(self.can_reach_region("Tall, Tall Mountain - Middle"))
        self.collect(self.get_item_by_name("Vertical Wind"))
        self.assertTrue(self.can_reach_region("Tall, Tall Mountain - Middle"))
        self.assertTrue(self.can_reach_location("Tall, Tall Mountain - Coins Star"))


class TallTallMountainCoinStar57AccessTestBase(TallTallMountainCoinStarAccessTestBase):
    options = {
        **TallTallMountainCoinStarAccessTestBase.options,
        "tall_tall_mountain_coin_star_requirement": 57,
    }

    def test_climb_coins_reach_coin_star(self):
        self.collect_second_floor_access()
        self.collect([
            self.get_item_by_name("Backflip"),
            self.get_item_by_name("Vertical Wind"),
        ])
        self.assertFalse(self.can_reach_location("Tall, Tall Mountain - Coins Star"))

        self.collect(self.get_item_by_name("Climb"))
        self.assertTrue(self.can_reach_location("Tall, Tall Mountain - Coins Star"))


class TallTallMountainCoinStar57MovelessAccessTestBase(TallTallMountainCoinStarAccessTestBase):
    options = {
        **TallTallMountainCoinStarAccessTestBase.options,
        "logic_tricks": {"Tall, Tall Mountain Coins without Climb"},
        "tall_tall_mountain_coin_star_requirement": 57,
    }

    def test_moveless_coins_reach_coin_star(self):
        self.collect_second_floor_access()
        self.collect([
            self.get_item_by_name("Backflip"),
            self.get_item_by_name("Vertical Wind"),
        ])
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
            self.get_item_by_name("Rolling Logs"),
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
            self.get_item_by_name("Rolling Logs"),
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
            self.get_item_by_name("Rolling Logs"),
            self.get_item_by_name("Long Jump"),
            self.get_item_by_name("Ledge Grab"),
        ])
        self.assertTrue(self.can_reach_region("Tall, Tall Mountain - Top"))
        self.assertFalse(self.can_reach_location("Tall, Tall Mountain - Coins Star"))

        self.collect(self.get_item_by_name("Purple Switches"))
        self.assertTrue(self.can_reach_location("Tall, Tall Mountain - Coins Star"))


class TallTallMountainIndividualUnlockLogicTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "accessibility": "minimal",
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "coin_object_unlocks": Options.CoinObjectUnlocks.option_per_level,
        "level_unlocks": Options.LevelUnlocks.option_special_only,
        "enemy_unlocks": Options.EnemyUnlocks.option_per_level,
        "one_up_checks": Options.OneUpChecks.option_true,
        "one_up_unlocks": Options.OneUpUnlocks.option_per_level,
        "level_features": Options.LevelFeatures.option_per_level,
        "bobomb_buddies": Options.BobombBuddies.option_per_level,
            }

    def get_full_tall_tall_mountain_route_state(self):
        state = CollectionState(self.multiworld)
        for item_name in [
            "Progressive Upstairs Key",
            "Long Jump",
            "Ledge Grab",
            "Climb",
            "Tall, Tall Mountain - Rolling Log",
            "Tall, Tall Mountain - Purple Switch",
        ]:
            state.collect(self.world.create_item(item_name))
        return state

    def test_each_unlock_matches_documented_total(self):
        source_coins = {
            "Tall, Tall Mountain - Single Yellow Coins": 27,
            "Tall, Tall Mountain - Red Coins": 16,
            "Tall, Tall Mountain - Single Blue Coins": 15,
            "Tall, Tall Mountain - Horizontal Coin Lines": 40,
            "Tall, Tall Mountain - Horizontal Coin Rings": 8,
            "Tall, Tall Mountain - Vertical Coin Lines": 5,
            "Tall, Tall Mountain - Crazy Box": 5,
            "Tall, Tall Mountain - Bob-ombs": 5,
            "Tall, Tall Mountain - Chuckya": 5,
            "Tall, Tall Mountain - Fly Guy": 2,
            "Tall, Tall Mountain - Goombas": 9,
        }
        for item_name, expected_coins in source_coins.items():
            with self.subTest(item=item_name):
                state = self.get_full_tall_tall_mountain_route_state()
                state.collect(self.world.create_item(item_name))
                actual_coins = max(
                    coin_count for coin_count in range(138)
                    if tall_tall_mountain_coins(state, self.player, coin_count)
                )
                self.assertEqual(actual_coins, expected_coins)

    def test_all_unlocks_total_137_coins(self):
        state = self.get_full_tall_tall_mountain_route_state()
        for item_name in [
            "Tall, Tall Mountain - Single Yellow Coins",
            "Tall, Tall Mountain - Red Coins",
            "Tall, Tall Mountain - Single Blue Coins",
            "Tall, Tall Mountain - Horizontal Coin Lines",
            "Tall, Tall Mountain - Horizontal Coin Rings",
            "Tall, Tall Mountain - Vertical Coin Lines",
            "Tall, Tall Mountain - Crazy Box",
            "Tall, Tall Mountain - Bob-ombs",
            "Tall, Tall Mountain - Chuckya",
            "Tall, Tall Mountain - Fly Guy",
            "Tall, Tall Mountain - Goombas",
        ]:
            state.collect(self.world.create_item(item_name))
        self.assertTrue(tall_tall_mountain_coins(state, self.player, 137))

    def test_upper_region_and_monty_mole_checks(self):
        self.collect(self.get_item_by_name("Progressive Upstairs Key"))
        self.collect(self.get_item_by_name("Long Jump"))
        self.assertTrue(self.can_reach_region("Tall, Tall Mountain - Middle"))
        self.assertFalse(self.can_reach_region("Tall, Tall Mountain - Upper"))
        self.assertEqual(
            self.multiworld.get_location(
                "Tall, Tall Mountain - Lower Monty Moles", self.player).parent_region.name,
            "Tall, Tall Mountain - Middle")
        self.assertEqual(
            self.multiworld.get_location(
                "Tall, Tall Mountain - Upper Monty Moles", self.player).parent_region.name,
            "Tall, Tall Mountain - Upper")
        for location_name in (
                "Tall, Tall Mountain - Scary 'Shrooms, Red Coins",
                "Tall, Tall Mountain - Upper Vine Wall 1-Up",
                "Tall, Tall Mountain - Waterfall Gap 1-Up",
                "Tall, Tall Mountain - Breathtaking View from Bridge",
        ):
            self.assertEqual(
                self.multiworld.get_location(location_name, self.player).parent_region.name,
                "Tall, Tall Mountain - Upper")

        self.collect(self.get_item_by_name("Tall, Tall Mountain - Rolling Log"))
        self.assertTrue(self.can_reach_region("Tall, Tall Mountain - Upper"))
        self.assertFalse(self.can_reach_location("Tall, Tall Mountain - Lower Monty Moles"))
        self.assertFalse(self.can_reach_location("Tall, Tall Mountain - Upper Monty Moles"))

        self.collect(self.get_item_by_name("Tall, Tall Mountain - Monty Moles"))
        self.assertTrue(self.can_reach_location("Tall, Tall Mountain - Lower Monty Moles"))
        self.assertTrue(self.can_reach_location("Tall, Tall Mountain - Upper Monty Moles"))


class BigBooHauntAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        "level_unlocks": Options.LevelUnlocks.option_special_only,
        "logic_tricks": {
            "Big Boo's Haunt Second Floor with Wall Kick",
            "Big Boo's Haunt Third Floor with Side Flip and Bounce Off of Bookends",
            "Big Boo's Haunt Roof without Long Jump",
        },
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
            }

    def collect_bbh_access(self):
        self.collect(self.get_item_by_name("Unlock Big Boo's Haunt"))

    def test_second_floor_access_with_staircase(self):
        self.collect_bbh_access()
        self.assertFalse(self.can_reach_region("Big Boo's Haunt - Second Floor"))
        self.collect(self.get_item_by_name("Big Boo's Haunt - Staircase"))
        self.assertTrue(self.can_reach_region("Big Boo's Haunt - Second Floor"))

    def test_second_floor_access_with_wall_kick(self):
        self.collect_bbh_access()
        self.collect(self.get_item_by_name("Wall Kick"))
        self.assertTrue(self.can_reach_region("Big Boo's Haunt - Second Floor"))

    def test_secret_books_requires_second_floor(self):
        self.collect_bbh_access()
        self.collect(self.get_item_by_name("Kick"))
        self.assertFalse(self.can_reach_location("Big Boo's Haunt - Secret of the Haunted Books"))
        self.collect(self.get_item_by_name("Big Boo's Haunt - Staircase"))
        self.assertTrue(self.can_reach_location("Big Boo's Haunt - Secret of the Haunted Books"))

    def test_third_floor_inherits_second_floor_access(self):
        self.collect_bbh_access()
        self.collect(self.get_item_by_name("Ledge Grab"))
        self.assertFalse(self.can_reach_region("Big Boo's Haunt - Third Floor"))
        self.collect(self.get_item_by_name("Wall Kick"))
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


class BigBooHauntIndividualUnlockLogicTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        "level_unlocks": Options.LevelUnlocks.option_special_only,
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "coin_object_unlocks": Options.CoinObjectUnlocks.option_per_level,
        "enemy_unlocks": Options.EnemyUnlocks.option_per_level,
        "logic_tricks": {"Big Boo's Haunt Third Floor with Side Flip and Bounce Off of Bookends"},
            }

    def collect_bbh_access(self):
        self.collect(self.get_item_by_name("Unlock Big Boo's Haunt"))

    def test_initial_coin_sources_are_counted_independently(self):
        source_coins = {
            "Big Boo's Haunt - Red Coins": 6,
            "Big Boo's Haunt - Breakable Coin Boxes": 6,
            "Big Boo's Haunt - Crazy Box": 5,
            "Big Boo's Haunt - 10-Coin Block": 10,
            "Big Boo's Haunt - Boos": 25,
            "Big Boo's Haunt - Flying Bookends": 5,
            "Big Boo's Haunt - Mr. Is": 10,
            "Big Boo's Haunt - Scuttlebugs": 9,
        }
        self.assertFalse(big_boos_haunt_coins(self.multiworld.state, self.player, 1))
        for item_name, expected_coins in source_coins.items():
            with self.subTest(item=item_name):
                item = self.get_item_by_name(item_name)
                self.collect(item)
                self.assertTrue(big_boos_haunt_coins(
                    self.multiworld.state, self.player, expected_coins))
                self.assertFalse(big_boos_haunt_coins(
                    self.multiworld.state, self.player, expected_coins + 1))
                self.remove(item)

    def test_second_floor_sources(self):
        self.collect_bbh_access()
        self.collect(self.get_item_by_name("Big Boo's Haunt - Staircase"))

        source_coins = {
            "Big Boo's Haunt - Red Coins": 12,
            "Big Boo's Haunt - Flying Bookends": 15,
            "Big Boo's Haunt - Mr. Is": 15,
        }
        for item_name, expected_coins in source_coins.items():
            with self.subTest(item=item_name):
                item = self.get_item_by_name(item_name)
                self.collect(item)
                self.assertTrue(big_boos_haunt_coins(
                    self.multiworld.state, self.player, expected_coins))
                self.assertFalse(big_boos_haunt_coins(
                    self.multiworld.state, self.player, expected_coins + 1))
                self.remove(item)

    def test_bookshelf_red_coin_requires_a_movement_ability(self):
        red_coins = self.get_item_by_name("Big Boo's Haunt - Red Coins")
        self.collect(red_coins)
        self.assertTrue(big_boos_haunt_coins(self.multiworld.state, self.player, 6))
        self.assertFalse(big_boos_haunt_coins(self.multiworld.state, self.player, 7))

        for action in ("Side Flip", "Backflip", "Triple Jump", "Wall Kick"):
            with self.subTest(action=action):
                item = self.get_item_by_name(action)
                self.collect(item)
                self.assertTrue(big_boos_haunt_coins(self.multiworld.state, self.player, 8))
                self.assertFalse(big_boos_haunt_coins(self.multiworld.state, self.player, 9))
                self.remove(item)

    def test_side_flip_third_floor_trick_requires_flying_bookends(self):
        self.collect_bbh_access()
        self.collect([
            self.get_item_by_name("Big Boo's Haunt - Staircase"),
            self.get_item_by_name("Side Flip"),
        ])
        self.assertFalse(self.can_reach_region("Big Boo's Haunt - Third Floor"))
        self.collect(self.get_item_by_name("Big Boo's Haunt - Flying Bookends"))
        self.assertTrue(self.can_reach_region("Big Boo's Haunt - Third Floor"))
        self.assertTrue(big_boos_haunt_coins(self.multiworld.state, self.player, 15))
        self.assertFalse(big_boos_haunt_coins(self.multiworld.state, self.player, 16))

        self.collect([
            self.get_item_by_name("Wall Kick"),
            self.get_item_by_name("Ledge Grab"),
        ])
        self.assertTrue(big_boos_haunt_coins(self.multiworld.state, self.player, 15))
        self.assertFalse(big_boos_haunt_coins(self.multiworld.state, self.player, 16))

    def test_bookend_route_cost_only_reduces_third_floor_yield(self):
        self.collect_bbh_access()
        self.collect([
            self.get_item_by_name("Big Boo's Haunt - Staircase"),
            self.get_item_by_name("Big Boo's Haunt - Flying Bookends"),
            self.get_item_by_name("Big Boo's Haunt - Blue Coin Block"),
            self.get_item_by_name("Side Flip"),
            self.get_item_by_name("Ground Pound"),
        ])
        # Permanent collection allows the Bookends and third-floor block to be
        # collected on separate visits.
        self.assertTrue(big_boos_haunt_coins(self.multiworld.state, self.player, 35))
        self.assertFalse(big_boos_haunt_coins(self.multiworld.state, self.player, 36))

    def test_third_floor_sources(self):
        self.collect_bbh_access()
        self.collect([
            self.get_item_by_name("Big Boo's Haunt - Staircase"),
            self.get_item_by_name("Wall Kick"),
            self.get_item_by_name("Ledge Grab"),
        ])

        self.collect(self.get_item_by_name("Big Boo's Haunt - Boos"))
        self.assertTrue(big_boos_haunt_coins(self.multiworld.state, self.player, 30))
        self.assertFalse(big_boos_haunt_coins(self.multiworld.state, self.player, 31))

        self.remove(self.get_item_by_name("Big Boo's Haunt - Boos"))
        self.collect([
            self.get_item_by_name("Big Boo's Haunt - Blue Coin Block"),
            self.get_item_by_name("Ground Pound"),
        ])
        self.assertTrue(big_boos_haunt_coins(self.multiworld.state, self.player, 20))
        self.assertFalse(big_boos_haunt_coins(self.multiworld.state, self.player, 21))

    def test_merry_go_round_coins_require_boos(self):
        self.collect(self.get_item_by_name("Big Boo's Haunt - Merry-go-round"))
        self.assertFalse(big_boos_haunt_coins(self.multiworld.state, self.player, 1))
        self.collect(self.get_item_by_name("Big Boo's Haunt - Boos"))
        self.assertTrue(big_boos_haunt_coins(self.multiworld.state, self.player, 50))
        self.assertFalse(big_boos_haunt_coins(self.multiworld.state, self.player, 51))

    def test_enemy_and_red_coin_stars_require_unlocks(self):
        self.collect_bbh_access()
        self.collect([
            self.get_item_by_name("Big Boo's Haunt - Merry-go-round"),
            self.get_item_by_name("Big Boo's Haunt - Staircase"),
            self.get_item_by_name("Backflip"),
            self.get_item_by_name("Wall Kick"),
            self.get_item_by_name("Ledge Grab"),
            self.get_item_by_name("Vanish Cap"),
        ])

        self.assertFalse(self.can_reach_location("Big Boo's Haunt - Go on a Ghost Hunt"))
        self.assertFalse(self.can_reach_location("Big Boo's Haunt - Ride Big Boo's Merry-Go-Round"))
        self.collect(self.get_item_by_name("Big Boo's Haunt - Boos"))
        self.assertFalse(self.can_reach_location("Big Boo's Haunt - Go on a Ghost Hunt"))
        self.assertFalse(self.can_reach_location("Big Boo's Haunt - Ride Big Boo's Merry-Go-Round"))
        self.collect(self.get_item_by_name("Big Boo's Haunt - Big Boos"))
        self.assertTrue(self.can_reach_location("Big Boo's Haunt - Go on a Ghost Hunt"))
        self.assertTrue(self.can_reach_location("Big Boo's Haunt - Ride Big Boo's Merry-Go-Round"))

        self.assertFalse(self.can_reach_location("Big Boo's Haunt - Seek the 8 Red Coins"))
        self.collect(self.get_item_by_name("Big Boo's Haunt - Red Coins"))
        self.assertTrue(self.can_reach_location("Big Boo's Haunt - Seek the 8 Red Coins"))

        self.assertFalse(self.can_reach_location("Big Boo's Haunt - Eye to Eye in the Secret Room"))
        self.collect(self.get_item_by_name("Big Boo's Haunt - Mr. Is"))
        self.assertTrue(self.can_reach_location("Big Boo's Haunt - Eye to Eye in the Secret Room"))

    def test_balcony_requires_big_boo(self):
        self.collect_bbh_access()
        self.collect_by_name([
            "Big Boo's Haunt - Staircase",
            "Wall Kick",
            "Ledge Grab",
            "Long Jump",
        ])
        self.assertTrue(self.can_reach_region("Big Boo's Haunt - Roof"))
        self.assertFalse(self.can_reach_location("Big Boo's Haunt - Big Boo's Balcony"))

        self.collect(self.get_item_by_name("Big Boo's Haunt - Big Boos"))
        self.assertTrue(self.can_reach_location("Big Boo's Haunt - Big Boo's Balcony"))


class BigBooHauntCoinStarAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "level_unlocks": Options.LevelUnlocks.option_special_only,
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
            }

    def collect_bbh_access(self):
        self.collect(self.get_item_by_name("Unlock Big Boo's Haunt"))


class BigBooHauntBookendTrickNoDespawnsTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        "level_unlocks": Options.LevelUnlocks.option_special_only,
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "coin_object_unlocks": Options.CoinObjectUnlocks.option_per_level,
        "enemy_unlocks": Options.EnemyUnlocks.option_per_level,
        "logic_tricks": {"Big Boo's Haunt Third Floor with Side Flip and Bounce Off of Bookends"},
        "no_despawns": Options.NoDespawns.option_true,
            }

    def test_no_despawns_preserves_bookend_coins(self):
        self.collect([
            self.get_item_by_name("Unlock Big Boo's Haunt"),
            self.get_item_by_name("Big Boo's Haunt - Staircase"),
            self.get_item_by_name("Big Boo's Haunt - Flying Bookends"),
            self.get_item_by_name("Big Boo's Haunt - Blue Coin Block"),
            self.get_item_by_name("Side Flip"),
            self.get_item_by_name("Ground Pound"),
        ])
        self.assertTrue(self.can_reach_region("Big Boo's Haunt - Third Floor"))
        self.assertTrue(big_boos_haunt_coins(self.multiworld.state, self.player, 35))
        self.assertFalse(big_boos_haunt_coins(self.multiworld.state, self.player, 36))


class BigBooHauntBookendTrickPermanentCoinTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **BigBooHauntBookendTrickNoDespawnsTestBase.options,
        "no_despawns": Options.NoDespawns.option_false,
    }

    def test_permanent_collection_preserves_bookend_coins(self):
        self.collect_by_name([
            "Unlock Big Boo's Haunt",
            "Big Boo's Haunt - Staircase",
            "Big Boo's Haunt - Flying Bookends",
            "Big Boo's Haunt - Blue Coin Block",
            "Side Flip",
            "Ground Pound",
        ])
        self.assertTrue(self.can_reach_region("Big Boo's Haunt - Third Floor"))
        self.assertTrue(big_boos_haunt_coins(self.multiworld.state, self.player, 35))
        self.assertFalse(big_boos_haunt_coins(self.multiworld.state, self.player, 36))


class BigBooHauntCoinStar76AccessTestBase(BigBooHauntCoinStarAccessTestBase):
    options = {
        **BigBooHauntCoinStarAccessTestBase.options,
        "big_boos_haunt_coin_star_requirement": 76,
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


class BigBooHauntCoinStar101AccessTestBase(BigBooHauntCoinStarAccessTestBase):
    options = {
        **BigBooHauntCoinStarAccessTestBase.options,
        "big_boos_haunt_coin_star_requirement": 101,
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
        "level_unlocks": Options.LevelUnlocks.option_special_only,
        "one_up_checks": Options.OneUpChecks.option_true,
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
            }

    def collect_second_floor_access(self):
        self.collect(self.get_item_by_name("Progressive Upstairs Key"))

    def disable_wdw_entrance(self, entrance_name: str):
        self.multiworld.get_entrance(f"Second Floor -> {entrance_name}", self.player).access_rule = \
            lambda state: False

    def test_high_entrance_requires_jump(self):
        self.collect_second_floor_access()
        self.assertTrue(self.can_reach_region("Wet-Dry World"))
        self.assertFalse(self.can_reach_region("Wet-Dry World - Highest Water"))

        self.collect(self.get_item_by_name("Ledge Grab"))
        self.assertFalse(self.can_reach_region("Wet-Dry World - Highest Water"))
        self.remove(self.get_item_by_name("Ledge Grab"))

        for movement in ("Triple Jump", "Side Flip", "Backflip"):
            with self.subTest(movement=movement):
                item = self.get_item_by_name(movement)
                self.collect(item)
                self.assertTrue(self.can_reach_region("Wet-Dry World - Highest Water"))
                self.remove(item)

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
        self.assertFalse(self.can_reach_location("Wet-Dry World - Secrets in the Shallows & Sky"))

        self.collect([
            self.get_item_by_name("Long Jump"),
        ])
        self.assertTrue(self.can_reach_region("Wet-Dry World - Mid-High Water"))
        self.assertTrue(self.can_reach_region("Wet-Dry World - Top"))
        self.assertTrue(self.can_reach_region("Wet-Dry World - High Water"))
        self.assertFalse(self.can_reach_region("Wet-Dry World - Highest Water"))

        self.collect([
            self.get_item_by_name("Wet-Dry World - Cannon Unlock"),
            self.get_item_by_name("Backflip"),
        ])
        self.assertTrue(self.can_reach_location("Wet-Dry World - Express Elevator--Hurry Up!"))

    def test_middle_water_to_mid_high_accepts_triple_jump_and_dive(self):
        self.disable_wdw_entrance("Wet-Dry World Low")
        self.disable_wdw_entrance("Wet-Dry World High")
        self.collect_second_floor_access()
        self.collect(self.get_item_by_name("Wet-Dry World - Water Level Diamond"))
        self.assertTrue(self.can_reach_region("Wet-Dry World - Mid Water"))
        self.assertFalse(self.can_reach_region("Wet-Dry World - Mid-High Water"))

        self.collect([self.get_item_by_name("Triple Jump"), self.get_item_by_name("Dive")])
        self.assertTrue(self.can_reach_region("Wet-Dry World - Mid-High Water"))

    def test_middle_water_to_mid_high_accepts_purple_switch(self):
        self.disable_wdw_entrance("Wet-Dry World Low")
        self.disable_wdw_entrance("Wet-Dry World High")
        self.collect_second_floor_access()
        self.collect([
            self.get_item_by_name("Wet-Dry World - Water Level Diamond"),
            self.get_item_by_name("Purple Switches"),
        ])
        self.assertTrue(self.can_reach_region("Wet-Dry World - Top of the Express Elevator"))
        self.assertTrue(self.can_reach_region("Wet-Dry World - Mid-High Water"))

    def test_low_water_to_mid_high_requires_water_level_diamond_and_long_jump(self):
        self.disable_wdw_entrance("Wet-Dry World Middle")
        self.disable_wdw_entrance("Wet-Dry World High")
        self.collect_second_floor_access()
        self.assertTrue(self.can_reach_region("Wet-Dry World - Low Water"))
        self.assertFalse(self.can_reach_region("Wet-Dry World - Mid-High Water"))

        self.collect(self.get_item_by_name("Long Jump"))
        self.assertFalse(self.can_reach_region("Wet-Dry World - Mid-High Water"))

        self.collect(self.get_item_by_name("Wet-Dry World - Water Level Diamond"))
        self.assertTrue(self.can_reach_region("Wet-Dry World - Mid-High Water"))

    def test_cannon_unlock_reaches_near_top_and_top(self):
        self.disable_wdw_entrance("Wet-Dry World Middle")
        self.disable_wdw_entrance("Wet-Dry World High")
        self.collect_second_floor_access()
        self.assertTrue(self.can_reach_region("Wet-Dry World - Cannon"))
        self.assertFalse(self.can_reach_entrance("Wet-Dry World - Cannon to Near the Top"))
        self.assertFalse(self.can_reach_entrance("Wet-Dry World - Cannon to Top"))
        self.assertFalse(self.can_reach_region("Wet-Dry World - Top"))

        self.collect(self.get_item_by_name("Wet-Dry World - Cannon Unlock"))
        self.assertTrue(self.can_reach_entrance("Wet-Dry World - Cannon to Near the Top"))
        self.assertTrue(self.can_reach_entrance("Wet-Dry World - Cannon to Top"))
        self.assertTrue(self.can_reach_region("Wet-Dry World - Near the Top"))
        self.assertTrue(self.can_reach_region("Wet-Dry World - Top"))

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
        self.collect(self.get_item_by_name("Bob-omb Buddies"))
        self.collect([self.get_item_by_name("Ledge Grab"), self.get_item_by_name("Triple Jump")])
        self.assertTrue(self.can_reach_region("Wet-Dry World - Highest Water"))
        self.assertTrue(self.can_reach_location("Wet-Dry World - Bob-omb Buddy"))

    def test_bob_omb_buddy_high_water_requires_jump_route(self):
        self.disable_wdw_entrance("Wet-Dry World Middle")
        self.disable_wdw_entrance("Wet-Dry World High")
        self.collect_second_floor_access()
        self.collect(self.get_item_by_name("Bob-omb Buddies"))
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
        self.assertFalse(self.can_reach_region("Wet-Dry World - Top of the Express Elevator"))

    def test_express_elevator_requires_cannon_or_heave_ho(self):
        self.disable_wdw_entrance("Wet-Dry World Middle")
        self.disable_wdw_entrance("Wet-Dry World High")
        self.collect_second_floor_access()
        self.collect([
            self.get_item_by_name("Purple Switches"),
        ])
        self.assertTrue(self.can_reach_region("Wet-Dry World - Top of the Express Elevator"))
        self.assertFalse(self.can_reach_location("Wet-Dry World - Express Elevator--Hurry Up!"))

        self.collect([
            self.get_item_by_name("Wet-Dry World - Cannon Unlock"),
            self.get_item_by_name("Backflip"),
        ])
        self.assertTrue(self.can_reach_location("Wet-Dry World - Express Elevator--Hurry Up!"))

    def test_secrets_requires_its_low_water_route(self):
        self.disable_wdw_entrance("Wet-Dry World Middle")
        self.disable_wdw_entrance("Wet-Dry World High")
        self.collect_second_floor_access()
        self.assertFalse(self.can_reach_location("Wet-Dry World - Secrets in the Shallows & Sky"))
        self.collect(self.get_item_by_name("Wet-Dry World - Water Level Diamond"))
        self.assertFalse(self.can_reach_location("Wet-Dry World - Express Elevator--Hurry Up!"))
        self.assertFalse(self.can_reach_region("Wet-Dry World - Top of the Express Elevator"))
        self.assertFalse(self.can_reach_location("Wet-Dry World - Secrets in the Shallows & Sky"))

        self.collect(self.get_item_by_name("Purple Switches"))
        self.assertTrue(self.can_reach_region("Wet-Dry World - Top of the Express Elevator"))
        self.assertTrue(self.can_reach_location("Wet-Dry World - Express Elevator--Hurry Up!"))
        self.assertFalse(self.can_reach_location("Wet-Dry World - Secrets in the Shallows & Sky"))

        self.collect(self.get_item_by_name("Wet-Dry World - Cannon Unlock"))
        self.assertTrue(self.can_reach_location("Wet-Dry World - Secrets in the Shallows & Sky"))

    def test_secrets_do_not_accept_top_route_without_water_level_diamond(self):
        self.disable_wdw_entrance("Wet-Dry World Middle")
        self.disable_wdw_entrance("Wet-Dry World High")
        self.collect_second_floor_access()
        self.collect(self.get_item_by_name("Purple Switches"))
        self.assertTrue(self.can_reach_region("Wet-Dry World - Top of the Express Elevator"))
        self.assertFalse(self.can_reach_location("Wet-Dry World - Secrets in the Shallows & Sky"))

        self.collect(self.get_item_by_name("Long Jump"))
        self.assertFalse(self.can_reach_location("Wet-Dry World - Secrets in the Shallows & Sky"))


class WetDryWorldTopPlatformsTrickTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_ARBITRARY_FEATURE_OPTIONS,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "level_unlocks": Options.LevelUnlocks.option_special_only,
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "logic_tricks": {
            "Wet-Dry World Top Platforms to Express Elevator without Movement Items",
        },
            }

    def test_top_of_express_elevator_accepts_no_movement_jump(self):
        self.collect(self.get_item_by_name("Progressive Upstairs Key"))
        self.collect(self.get_item_by_name("Wall Kick"))
        self.assertTrue(self.can_reach_region("Wet-Dry World - Top of the Express Elevator"))


class GlobalCapAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_ARBITRARY_FEATURE_OPTIONS,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "level_unlocks": Options.LevelUnlocks.option_special_only,
        "buddy_checks": Options.BuddyChecks.option_true,
        "one_up_checks": Options.OneUpChecks.option_true,
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
                "universal_tracker_glitched_logic": {
            "Wing Mario Over the Rainbow Leap of Faith Without Ledge Grab",
        },
    }

    def test_bob_wing_cap_access(self):
        self.collect(self.get_item_by_name("Bob-omb Buddies"))
        self.collect(self.get_item_by_name("Bob-omb Battlefield - Cannon Unlock"))
        self.assertFalse(self.can_reach_location("Bob-omb Battlefield - Mario Wings to the Sky"))
        self.collect(self.world.create_item("Bob-omb Battlefield - Wing Cap"))
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

    def test_wmotr_red_coins_cannon_route_accepts_ut_leap_of_faith(self):
        self.collect([self.get_item_by_name("Progressive Upstairs Key")] * 3)
        self.collect([
            self.get_item_by_name("Wing Cap"),
            self.get_item_by_name("Side Flip"),
        ])
        self.assertFalse(self.can_reach_location("Wing Mario Over the Rainbow - Red Coins"))

        self.collect(self.get_item_by_name("Wing Mario Over the Rainbow - Cannon Unlock"))
        self.assertFalse(self.can_reach_location("Wing Mario Over the Rainbow - Red Coins"))

        self.collect(self.get_item_by_name("Long Jump"))
        self.collect(self.world.create_item("Glitched Logic"))
        self.assertTrue(self.can_reach_location("Wing Mario Over the Rainbow - Red Coins"))

    def test_wmotr_buddy_wing_cap_route_accepts_triple_jump(self):
        self.collect([self.get_item_by_name("Progressive Upstairs Key")] * 3)
        self.collect(self.get_item_by_name("Bob-omb Buddies"))
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

    def test_wmotr_cloud_cannon_route_accepts_ut_leap_of_faith(self):
        self.collect([self.get_item_by_name("Progressive Upstairs Key")] * 3)
        self.collect([
            self.get_item_by_name("Wing Cap"),
            self.get_item_by_name("Long Jump"),
            self.get_item_by_name("Side Flip"),
            self.world.create_item("Glitched Logic"),
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
        "level_unlocks": Options.LevelUnlocks.option_special_only,
        "one_up_checks": Options.OneUpChecks.option_true,
                "cap_items": Options.CapItems.option_per_level,
    }

    def test_bob_wing_cap_access(self):
        self.collect(self.get_item_by_name("Bob-omb Buddies"))
        self.collect(self.get_item_by_name("Bob-omb Battlefield - Cannon Unlock"))
        self.assertFalse(self.can_reach_location("Bob-omb Battlefield - Mario Wings to the Sky"))
        self.collect(self.world.create_item("Wing Cap"))
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
        self.assertTrue(self.can_reach_location("Wing Mario Over the Rainbow - Red Coins"))

    def test_wmotr_rejects_another_level_wing_cap(self):
        self.collect([self.get_item_by_name("Progressive Upstairs Key")] * 3)
        self.collect(self.get_item_by_name("Wing Mario Over the Rainbow - Cannon Unlock"))
        self.collect(self.get_item_by_name("Castle - Wing Cap"))
        self.assertFalse(self.can_reach_location("Wing Mario Over the Rainbow - Red Coins"))

    def test_wmotr_bob_omb_buddy_accepts_wing_cap(self):
        self.collect([self.get_item_by_name("Progressive Upstairs Key")] * 3)
        self.collect(self.get_item_by_name("Bob-omb Buddies"))
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


class WMotRLeapOfFaithBuddyAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "level_unlocks": Options.LevelUnlocks.option_special_only,
        "one_up_checks": Options.OneUpChecks.option_true,
                "logic_tricks": {
            "Wing Mario Over the Rainbow Leap of Faith Without Ledge Grab",
        },
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
    }

    def test_wmotr_bob_omb_buddy_accepts_long_jump_leap_of_faith(self):
        self.collect([self.get_item_by_name("Progressive Upstairs Key")] * 3)
        self.collect(self.get_item_by_name("Side Flip"))
        self.assertFalse(self.can_reach_location("Wing Mario Over the Rainbow - Bob-omb Buddy"))
        self.collect(self.get_item_by_name("Long Jump"))
        self.assertTrue(self.can_reach_location("Wing Mario Over the Rainbow - Bob-omb Buddy"))

    def test_wmotr_bob_omb_buddy_platform_uses_leap_of_faith_region(self):
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
        "level_unlocks": Options.LevelUnlocks.option_special_only,
        "one_up_checks": Options.OneUpChecks.option_true,
        "blocksanity": Options.Blocksanity.option_true,
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
                "universal_tracker_glitched_logic": {
            "Wing Mario Over the Rainbow Leap of Faith Without Ledge Grab",
        },
    }

    def test_cloud_blocks_require_flight(self):
        self.collect([self.get_item_by_name("Progressive Upstairs Key")] * 3)
        self.collect(self.get_item_by_name("Wing Cap"))
        self.assertFalse(self.can_reach_location(
            "Wing Mario Over the Rainbow - Below the Pole Cloud Wing Cap Block"))
        self.assertFalse(self.can_reach_location(
            "Wing Mario Over the Rainbow - Overlooking Bob-omb Buddy Cloud Wing Cap Block"))

        self.collect(self.get_item_by_name("Triple Jump"))
        self.assertTrue(self.can_reach_location(
            "Wing Mario Over the Rainbow - Below the Pole Cloud Wing Cap Block"))
        self.assertTrue(self.can_reach_location(
            "Wing Mario Over the Rainbow - Overlooking Bob-omb Buddy Cloud Wing Cap Block"))

    def test_cloud_blocks_accept_buddy_platform_and_cannon_flight(self):
        self.collect([self.get_item_by_name("Progressive Upstairs Key")] * 3)
        self.collect([
            self.get_item_by_name("Wing Cap"),
            self.get_item_by_name("Long Jump"),
            self.get_item_by_name("Side Flip"),
            self.world.create_item("Glitched Logic"),
        ])
        self.assertFalse(self.can_reach_location(
            "Wing Mario Over the Rainbow - Below the Pole Cloud Wing Cap Block"))

        self.collect(self.get_item_by_name("Wing Mario Over the Rainbow - Cannon Unlock"))
        self.assertTrue(self.can_reach_location(
            "Wing Mario Over the Rainbow - Below the Pole Cloud Wing Cap Block"))
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
        "level_unlocks": Options.LevelUnlocks.option_special_only,
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
        self.multiworld.get_entrance("Tick Tock Clock - First Clock Hand Area", self.player).access_rule = \
            lambda state: False

        self.collect_third_floor_access()
        self.assertFalse(self.can_reach_region("Tick Tock Clock Stopped"))
        self.assertTrue(self.can_reach_region("Tick Tock Clock Moving"))
        self.assertFalse(self.can_reach_region("Tick Tock Clock - First Clock Hand Area"))
        self.assertFalse(self.can_reach_location("Tick Tock Clock - Stop Time for Red Coins"))


class ThwompUnlockAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "level_unlocks": Options.LevelUnlocks.option_special_only,
        "enemy_unlocks": Options.EnemyUnlocks.option_per_level,
        "one_up_checks": Options.OneUpChecks.option_true,
            }

    def test_ssl_thwomp_1up_requires_thwomp(self):
        self.collect(self.get_item_by_name("Progressive Basement Key"))
        self.assertFalse(
            self.can_reach_location("Shifting Sand Land - Pyramid Grindel 1-Up"))

        self.collect(self.get_item_by_name("Shifting Sand Land - Grindel"))
        self.assertTrue(
            self.can_reach_location("Shifting Sand Land - Pyramid Grindel 1-Up"))

    def test_ttc_star_requires_thwomp(self):
        self.collect([self.get_item_by_name("Progressive Upstairs Key")] * 2)
        self.assertTrue(self.can_reach_region("Tick Tock Clock Moving"))
        self.assertFalse(self.can_reach_location("Tick Tock Clock - Stomp on the Thwomp"))

        self.collect(self.get_item_by_name("Tick Tock Clock - Thwomp"))
        self.assertTrue(self.can_reach_location("Tick Tock Clock - Stomp on the Thwomp"))


class TTCRandomizedMoveVariantAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_ARBITRARY_FEATURE_OPTIONS,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "level_unlocks": Options.LevelUnlocks.option_special_only,
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "one_up_checks": Options.OneUpChecks.option_true,
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
        self.assertFalse(self.can_reach_region("Tick Tock Clock - First Clock Hand Area"))
        self.collect(self.get_item_by_name("Tick Tock Clock - Spinners"))
        self.assertTrue(self.can_reach_region("Tick Tock Clock - First Clock Hand Area"))
        self.assertTrue(self.can_reach_location("Tick Tock Clock - Stop Time for Red Coins"))

    def test_wall_kick_does_not_reach_lower_without_moveless_logic(self):
        self.collect_third_floor_access()
        self.collect(self.get_item_by_name("Wall Kick"))
        self.assertFalse(self.can_reach_region("Tick Tock Clock - First Clock Hand Area"))

    def test_timed_jumps_require_moving_ttc_or_wall_kick(self):
        self.use_stopped_ttc_without_entry_move()
        self.collect_third_floor_access()
        self.collect([
            self.get_item_by_name("Tick Tock Clock - Spinners"),
            self.get_item_by_name("Climb"),
        ])
        self.assertTrue(self.can_reach_region("Tick Tock Clock - The Pit and the Pendulums Area"))
        self.assertTrue(self.can_reach_location("Tick Tock Clock - The Pit and the Pendulums"))
        self.assertFalse(self.can_reach_region("Tick Tock Clock - Moving Bars Area"))
        self.assertFalse(self.can_reach_location("Tick Tock Clock - Timed Jumps on Moving Bars"))
        self.assertFalse(self.can_reach_location("Tick Tock Clock - Moving Bars Platform 1-Up"))
        self.collect(self.get_item_by_name("Wall Kick"))
        self.assertTrue(self.can_reach_region("Tick Tock Clock - Moving Bars Area"))
        self.assertTrue(self.can_reach_location("Tick Tock Clock - Timed Jumps on Moving Bars"))
        self.assertTrue(self.can_reach_location("Tick Tock Clock - Moving Bars Platform 1-Up"))

    def test_timed_jumps_reachable_in_moving_ttc_without_wall_kick(self):
        self.collect_third_floor_access()
        self.collect([
            self.get_item_by_name("Side Flip"),
            self.get_item_by_name("Climb"),
        ])
        self.assertTrue(self.can_reach_region("Tick Tock Clock Moving"))
        self.assertTrue(self.can_reach_region("Tick Tock Clock - Moving Bars Area"))
        self.assertTrue(self.can_reach_location("Tick Tock Clock - Timed Jumps on Moving Bars"))

    def test_pole_1up_is_in_upper_region(self):
        self.collect_third_floor_access()
        self.collect(self.get_item_by_name("Triple Jump"))
        self.assertTrue(self.can_reach_region("Tick Tock Clock - First Clock Hand Area"))
        self.assertFalse(self.can_reach_region("Tick Tock Clock - Moving Bars Area"))
        self.assertFalse(self.can_reach_location("Tick Tock Clock - Pole 1-Up"))

        self.collect(self.get_item_by_name("Climb"))
        self.assertTrue(self.can_reach_region("Tick Tock Clock - Moving Bars Area"))
        self.assertTrue(self.can_reach_location("Tick Tock Clock - Pole 1-Up"))

    def test_midway_1up_uses_top_past_spinners_region_access(self):
        self.collect_third_floor_access()
        self.collect([
            self.get_item_by_name("Triple Jump"),
            self.get_item_by_name("Ledge Grab"),
            self.get_item_by_name("Climb"),
        ])
        self.assertTrue(self.can_reach_region("Tick Tock Clock - Top Past Spinners"))
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
        "level_unlocks": Options.LevelUnlocks.option_special_only,
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
                "logic_tricks": {"Castle Tick Tock Clock Entrance With Wall Kick"},
    }

    def collect_third_floor_access(self):
        self.collect([self.get_item_by_name("Progressive Upstairs Key")] * 2)

    def test_wall_kick_reaches_lower_with_moveless_logic(self):
        self.collect_third_floor_access()
        self.collect(self.get_item_by_name("Wall Kick"))
        self.assertTrue(self.can_reach_region("Tick Tock Clock - First Clock Hand Area"))


class TickTockClockCoinStarAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_ARBITRARY_FEATURE_OPTIONS,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "level_unlocks": Options.LevelUnlocks.option_special_only,
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
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


class TickTockClockCoinStar25MovingAccessTestBase(TickTockClockCoinStarAccessTestBase):
    options = {
        **TickTockClockCoinStarAccessTestBase.options,
        "tick_tock_clock_coin_star_requirement": 25,
    }

    def test_coin_star_access(self):
        self.collect_third_floor_access()
        self.collect(self.get_item_by_name("Side Flip"))
        self.assertTrue(self.can_reach_location("Tick Tock Clock - Coins Star"))


class TickTockClockCoinStar26MovingAccessTestBase(TickTockClockCoinStarAccessTestBase):
    options = {
        **TickTockClockCoinStarAccessTestBase.options,
        "tick_tock_clock_coin_star_requirement": 26,
    }

    def test_coin_star_access(self):
        self.collect_third_floor_access()
        self.collect(self.get_item_by_name("Side Flip"))
        self.assertFalse(self.can_reach_location("Tick Tock Clock - Coins Star"))


class TickTockClockCoinStar112SideFlipGroundPoundAccessTestBase(TickTockClockCoinStarAccessTestBase):
    options = {
        **TickTockClockCoinStarAccessTestBase.options,
        "tick_tock_clock_coin_star_requirement": 112,
    }

    def test_coin_star_access(self):
        self.collect_third_floor_access()
        self.collect([
            self.get_item_by_name("Side Flip"),
            self.get_item_by_name("Climb"),
            self.get_item_by_name("Ground Pound"),
        ])
        self.assertTrue(self.can_reach_location("Tick Tock Clock - Coins Star"))


class TickTockClockCoinStar113SideFlipGroundPoundAccessTestBase(TickTockClockCoinStarAccessTestBase):
    options = {
        **TickTockClockCoinStarAccessTestBase.options,
        "tick_tock_clock_coin_star_requirement": 113,
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


class TickTockClockIndividualUnlockLogicTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_ARBITRARY_FEATURE_OPTIONS,
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "level_unlocks": Options.LevelUnlocks.option_special_only,
                "coin_object_unlocks": Options.CoinObjectUnlocks.option_per_level,
        "enemy_unlocks": Options.EnemyUnlocks.option_per_level,
    }

    def test_coin_sources_are_counted_independently(self):
        self.collect([self.get_item_by_name("Progressive Upstairs Key")] * 2)
        self.collect([
            self.get_item_by_name("Triple Jump"),
            self.get_item_by_name("Ledge Grab"),
            self.get_item_by_name("Climb"),
            self.get_item_by_name("Ground Pound"),
            self.get_item_by_name("Tick Tock Clock - Spinners"),
        ])
        source_coins = {
            "Tick Tock Clock - Single Yellow Coins": 2,
            "Tick Tock Clock - Red Coins": 16,
            "Tick Tock Clock - Blue Coin Block": 35,
            "Tick Tock Clock - Horizontal Coin Lines": 5,
            "Tick Tock Clock - 3-Coin Blocks": 18,
            "Tick Tock Clock - 10-Coin Blocks": 50,
            "Tick Tock Clock - Bob-ombs": 2,
        }
        self.assertFalse(tick_tock_clock_coins(self.multiworld.state, self.player, 1))
        for item_name, expected_coins in source_coins.items():
            with self.subTest(item=item_name):
                item = self.get_item_by_name(item_name)
                self.collect(item)
                self.assertTrue(tick_tock_clock_coins(
                    self.multiworld.state, self.player, expected_coins))
                self.assertFalse(tick_tock_clock_coins(
                    self.multiworld.state, self.player, expected_coins + 1))
                self.remove(item)

    def test_red_coin_star_requires_red_coins(self):
        self.collect([self.get_item_by_name("Progressive Upstairs Key")] * 2)
        self.collect([
            self.get_item_by_name("Ledge Grab"),
            self.get_item_by_name("Tick Tock Clock - Spinners"),
        ])
        self.assertFalse(self.can_reach_location("Tick Tock Clock - Stop Time for Red Coins"))
        self.collect(self.get_item_by_name("Tick Tock Clock - Red Coins"))
        self.assertTrue(self.can_reach_location("Tick Tock Clock - Stop Time for Red Coins"))


class TickTockClockStompThwompTrickTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "level_unlocks": Options.LevelUnlocks.option_special_only,
                "enemy_unlocks": Options.EnemyUnlocks.option_per_level,
        "logic_tricks": {"Tick Tock Clock Triple Jump and Wall Kick to Stomp the Thwomp without Thwomp"},
    }

    def collect_third_floor_access(self):
        self.collect([self.get_item_by_name("Progressive Upstairs Key")] * 2)

    def test_triple_jump_and_wall_kick_bypass_thwomp(self):
        self.collect_third_floor_access()
        self.collect([
            self.get_item_by_name("Climb"),
            self.get_item_by_name("Ledge Grab"),
        ])
        self.assertFalse(self.can_reach_location("Tick Tock Clock - Stomp on the Thwomp"))
        self.collect(self.get_item_by_name("Triple Jump"))
        self.assertFalse(self.can_reach_location("Tick Tock Clock - Stomp on the Thwomp"))
        self.collect(self.get_item_by_name("Wall Kick"))
        self.assertTrue(self.can_reach_location("Tick Tock Clock - Stomp on the Thwomp"))

    def test_trick_does_not_work_in_stopped_ttc(self):
        for ttc_entrance in sm64_ttc_entrances[1:]:
            self.multiworld.get_entrance(
                f"Third Floor -> {ttc_entrance}", self.player).access_rule = lambda state: False
        self.collect_third_floor_access()
        self.collect([
            self.get_item_by_name("Triple Jump"),
            self.get_item_by_name("Wall Kick"),
            self.get_item_by_name("Climb"),
            self.get_item_by_name("Ledge Grab"),
        ])
        self.assertFalse(self.can_reach_location("Tick Tock Clock - Stomp on the Thwomp"))


class RainbowRideCoinStarAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_ARBITRARY_FEATURE_OPTIONS,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "buddy_checks": Options.BuddyChecks.option_true,
        "level_unlocks": Options.LevelUnlocks.option_special_only,
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
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


class RainbowRideCoinStar55AccessTestBase(RainbowRideCoinStarAccessTestBase):
    options = {
        **RainbowRideCoinStarAccessTestBase.options,
        "rainbow_ride_coin_star_requirement": 55,
    }

    def test_coin_star_access(self):
        self.collect_rr_access()
        self.collect([
            self.get_item_by_name("Dive"),
            self.get_item_by_name("Climb"),
            self.get_item_by_name("Rainbow Ride - Carpets"),
        ])
        self.assertTrue(self.can_reach_location("Rainbow Ride - Coins Star"))


class RainbowRideCoinStar56AccessTestBase(RainbowRideCoinStarAccessTestBase):
    options = {
        **RainbowRideCoinStarAccessTestBase.options,
        "rainbow_ride_coin_star_requirement": 56,
    }

    def test_coin_star_access(self):
        self.collect_rr_access()
        self.collect([
            self.get_item_by_name("Dive"),
            self.get_item_by_name("Climb"),
        ])
        self.assertFalse(self.can_reach_location("Rainbow Ride - Coins Star"))


class RainbowRideCoinStar101AccessTestBase(RainbowRideCoinStarAccessTestBase):
    options = {
        **RainbowRideCoinStarAccessTestBase.options,
        "rainbow_ride_coin_star_requirement": 101,
    }

    def test_coin_star_access(self):
        self.collect_rr_access()
        self.collect([
            self.get_item_by_name("Dive"),
            self.get_item_by_name("Climb"),
            self.get_item_by_name("Ground Pound"),
            self.get_item_by_name("Wall Kick"),
            self.get_item_by_name("Rainbow Ride - Carpets"),
        ])
        self.assertTrue(self.can_reach_location("Rainbow Ride - Coins Star"))


class RainbowRideCoinStar102AccessTestBase(RainbowRideCoinStarAccessTestBase):
    options = {
        **RainbowRideCoinStarAccessTestBase.options,
        "rainbow_ride_coin_star_requirement": 102,
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


class RainbowRideIndividualUnlockLogicTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **SHUFFLED_ARBITRARY_FEATURE_OPTIONS,
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "level_unlocks": Options.LevelUnlocks.option_special_only,
                "coin_object_unlocks": Options.CoinObjectUnlocks.option_per_level,
        "enemy_unlocks": Options.EnemyUnlocks.option_per_level,
    }

    def collect_all_rr_routes(self):
        self.collect([self.get_item_by_name("Progressive Upstairs Key")] * 2)
        self.collect([
            self.get_item_by_name("Rainbow Ride - Carpets"),
            self.get_item_by_name("Rainbow Ride - Cannon Unlock"),
            self.get_item_by_name("Side Flip"),
            self.get_item_by_name("Long Jump"),
            self.get_item_by_name("Climb"),
            self.get_item_by_name("Ground Pound"),
            self.get_item_by_name("Wall Kick"),
        ])

    def test_coin_sources_are_counted_independently(self):
        self.collect_all_rr_routes()
        source_coins = {
            "Rainbow Ride - Single Yellow Coins": 6,
            "Rainbow Ride - Red Coins": 16,
            "Rainbow Ride - Blue Coin Block": 30,
            "Rainbow Ride - Horizontal Coin Lines": 30,
            "Rainbow Ride - Horizontal Coin Rings": 32,
            "Rainbow Ride - Vertical Coin Lines": 10,
            "Rainbow Ride - Bob-ombs": 4,
            "Rainbow Ride - Chuckya": 5,
            "Rainbow Ride - Lakitus": 10,
            "Rainbow Ride - Fly Guy": 2,
            "Rainbow Ride - Goomba": 1,
        }
        self.assertFalse(rainbow_ride_coins(self.multiworld.state, self.player, 1))
        for item_name, expected_coins in source_coins.items():
            with self.subTest(item=item_name):
                item = self.get_item_by_name(item_name)
                self.collect(item)
                self.assertTrue(rainbow_ride_coins(
                    self.multiworld.state, self.player, expected_coins))
                self.assertFalse(rainbow_ride_coins(
                    self.multiworld.state, self.player, expected_coins + 1))
                self.remove(item)

    def test_red_coin_star_requires_red_coins(self):
        self.collect_all_rr_routes()
        self.assertFalse(self.can_reach_location("Rainbow Ride - Coins Amassed in a Maze"))
        self.collect(self.get_item_by_name("Rainbow Ride - Red Coins"))
        self.assertTrue(self.can_reach_location("Rainbow Ride - Coins Amassed in a Maze"))

    def test_lakitus_are_split_between_maze_and_carpets(self):
        self.collect([self.get_item_by_name("Progressive Upstairs Key")] * 2)
        self.collect([
            self.get_item_by_name("Long Jump"),
            self.get_item_by_name("Side Flip"),
            self.get_item_by_name("Climb"),
            self.get_item_by_name("Rainbow Ride - Lakitus"),
        ])

        self.assertTrue(rainbow_ride_coins(self.multiworld.state, self.player, 5))
        self.assertFalse(rainbow_ride_coins(self.multiworld.state, self.player, 6))

        self.collect(self.get_item_by_name("Rainbow Ride - Carpets"))
        self.assertTrue(rainbow_ride_coins(self.multiworld.state, self.player, 10))
        self.assertFalse(rainbow_ride_coins(self.multiworld.state, self.player, 11))


class BlocksanityCoinBlockUnlockAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        "accessibility": "minimal",
                "blocksanity": Options.Blocksanity.option_true,
        "coin_object_unlocks": Options.CoinObjectUnlocks.option_per_level,
        "level_unlocks": Options.LevelUnlocks.option_special_only,
    }

    coin_block_locations_by_item = {
        "Bowser in the Dark World - 3-Coin Block": (
            "Bowser in the Dark World - 3 Coins Block",
        ),
        "Bowser in the Fire Sea - 3-Coin Block": (
            "Bowser in the Fire Sea - 3 Coins Block",
        ),
        "Jolly Roger Bay - 3-Coin Block": (
            "Jolly Roger Bay - 3 Coins Block",
        ),
        "Snowman's Land - 3-Coin Block": (
            "Snowman's Land - 3 Coins Block",
        ),
        "Tiny-Huge Island - 3-Coin Block": (
            "Tiny-Huge Island - 3 Coins Block",
        ),
        "Tick Tock Clock - 3-Coin Blocks": (
            "Tick Tock Clock - Above Timed Jumps on Moving Bars 3 Coins Block",
            "Tick Tock Clock - First Pendulum 3 Coins Block",
            "Tick Tock Clock - Past Three Spinners 3 Coins Block",
            "Tick Tock Clock - Heave-ho First 3 Coins Block",
            "Tick Tock Clock - Above Red Coin Spinners 3 Coins Block",
            "Tick Tock Clock - Heave-ho Second 3 Coins Block",
        ),
        "Vanish Cap Under the Moat - 3-Coin Block": (
            "Vanish Cap Under the Moat - 3 Coins Block",
        ),
        "Wet-Dry World - 3-Coin Blocks": (
            "Wet-Dry World - Push Block 3 Coins Block",
            "Wet-Dry World - Wooden Structure 3 Coins Block",
        ),
        "Big Boo's Haunt - 10-Coin Block": (
            "Big Boo's Haunt - 10 Coins Block",
        ),
        "Bowser in the Fire Sea - 10-Coin Block": (
            "Bowser in the Fire Sea - 10 Coins Block",
        ),
        "Tick Tock Clock - 10-Coin Blocks": (
            "Tick Tock Clock - Top Clock Hand 10 Coins Block",
            "Tick Tock Clock - Above Four Moving Bars 10 Coins Block",
            "Tick Tock Clock - Top Central Platform 10 Coins Block",
            "Tick Tock Clock - Below Red Coin Spinners 10 Coins Block",
            "Tick Tock Clock - Beneath the Thwomp 10 Coins Block",
        ),
        "Wet-Dry World - 10-Coin Blocks": (
            "Wet-Dry World - Push Block 10 Coins Block",
            "Wet-Dry World - Pedestal 10 Coins Block",
            "Wet-Dry World - Top of Express Elevator 10 Coins Block",
        ),
    }

    def test_all_coin_block_checks_require_their_unlock(self):
        self.collect_all_but(set(self.coin_block_locations_by_item))
        for location_names in self.coin_block_locations_by_item.values():
            for location_name in location_names:
                with self.subTest(location=location_name, state="locked"):
                    self.assertFalse(self.can_reach_location(location_name))

        for item_name, location_names in self.coin_block_locations_by_item.items():
            self.collect(self.get_item_by_name(item_name))
            for location_name in location_names:
                with self.subTest(location=location_name, state="unlocked"):
                    self.assertTrue(self.can_reach_location(location_name))


class RedCoinStarUnlockAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        "coin_object_unlocks": Options.CoinObjectUnlocks.option_per_level,
    }

    red_coin_item_by_location = {
        "Bob-omb Battlefield - Find the 8 Red Coins": "Bob-omb Battlefield - Red Coins",
        "Whomp's Fortress - Red Coins on the Floating Isle": "Whomp's Fortress - Red Coins",
        "Jolly Roger Bay - Red Coins on the Ship Afloat": "Jolly Roger Bay - Red Coins",
        "Cool, Cool Mountain - Frosty Slide for 8 Red Coins": "Cool, Cool Mountain - Red Coins",
        "Big Boo's Haunt - Seek the 8 Red Coins": "Big Boo's Haunt - Red Coins",
        "Hazy Maze Cave - Elevate for 8 Red Coins": "Hazy Maze Cave - Red Coins",
        "Lethal Lava Land - 8-Coin Puzzle with 15 Pieces": "Lethal Lava Land - Red Coins",
        "Shifting Sand Land - Free Flying for 8 Red Coins": "Shifting Sand Land - Red Coins",
        "Dire, Dire Docks - Pole-Jumping for Red Coins": "Dire, Dire Docks - Red Coins",
        "Snowman's Land - Shell Shreddin' for Red Coins": "Snowman's Land - Red Coins",
        "Wet-Dry World - Go to Town for Red Coins": "Wet-Dry World - Red Coins",
        "Tall, Tall Mountain - Scary 'Shrooms, Red Coins": "Tall, Tall Mountain - Red Coins",
        "Tiny-Huge Island - Wiggler's Red Coins": "Tiny-Huge Island - Red Coins",
        "Tick Tock Clock - Stop Time for Red Coins": "Tick Tock Clock - Red Coins",
        "Rainbow Ride - Coins Amassed in a Maze": "Rainbow Ride - Red Coins",
        "The Secret Aquarium - Red Coins": "Secret Aquarium - Red Coins",
        "Bowser in the Dark World - Red Coins": "Bowser in the Dark World - Red Coins",
        "Tower of the Wing Cap - Red Coins": "Tower of the Wing Cap - Red Coins",
        "Cavern of the Metal Cap - Red Coins": "Cavern of the Metal Cap - Red Coins",
        "Vanish Cap Under the Moat - Red Coins": "Vanish Cap Under the Moat - Red Coins",
        "Bowser in the Fire Sea - Red Coins": "Bowser in the Fire Sea - Red Coins",
        "Wing Mario Over the Rainbow - Red Coins": "Wing Mario Over the Rainbow - Red Coins",
        "Bowser in the Sky - Red Coins": "Bowser in the Sky - Red Coins",
    }

    def test_red_coin_stars_require_their_per_level_red_coins(self):
        self.collect_all_but(set(self.red_coin_item_by_location.values()))
        for location_name in self.red_coin_item_by_location:
            with self.subTest(location=location_name, state="locked"):
                location = self.multiworld.get_location(location_name, self.player)
                self.assertFalse(location.access_rule(self.multiworld.state))

        for location_name, item_name in self.red_coin_item_by_location.items():
            self.collect(self.get_item_by_name(item_name))
            with self.subTest(location=location_name, state="unlocked"):
                location = self.multiworld.get_location(location_name, self.player)
                self.assertTrue(location.access_rule(self.multiworld.state))


class GlobalBowserArenaBombAccessTestBase(SM64TestBase):
    options = {
        "bowser_bombs": Options.BowserBombs.option_global,
        "bowser_in_the_dark_world_health": 4,
        "bowser_in_the_fire_sea_health": 4,
        "bowser_in_the_sky_health": 5,
    }

    def test_first_two_keys_require_four_global_bombs(self):
        self.collect_all_but({
            "Bowser Arena Bomb 1", "Bowser Arena Bomb 2", "Bowser Arena Bomb 3", "Bowser Arena Bomb 4",
            "Bowser in the Sky - Bowser Arena Bomb 5",
        })
        self.collect([
            self.get_item_by_name("Bowser Arena Bomb 1"),
            self.get_item_by_name("Bowser Arena Bomb 2"),
            self.get_item_by_name("Bowser Arena Bomb 3"),
        ])
        self.assertFalse(self.can_reach_location("Bowser in the Dark World - Key"))
        self.assertFalse(self.can_reach_location("Bowser in the Fire Sea - Key"))

        self.collect(self.get_item_by_name("Bowser Arena Bomb 4"))
        self.assertTrue(self.can_reach_location("Bowser in the Dark World - Key"))
        self.assertTrue(self.can_reach_location("Bowser in the Fire Sea - Key"))

    def test_bowser_in_the_sky_uses_its_fifth_bomb(self):
        self.collect_all_but({
            "Bowser Arena Bomb 1", "Bowser Arena Bomb 2", "Bowser Arena Bomb 3", "Bowser Arena Bomb 4",
            "Bowser in the Sky - Bowser Arena Bomb 5",
        })
        self.collect([
            self.get_item_by_name(f"Bowser Arena Bomb {bomb}") for bomb in range(1, 5)
        ])
        self.assertFalse(self.multiworld.can_beat_game(self.multiworld.state))

        self.collect(self.get_item_by_name("Bowser in the Sky - Bowser Arena Bomb 5"))
        self.assertTrue(self.multiworld.can_beat_game(self.multiworld.state))


class BothBowserArenaBombAccessTestBase(SM64TestBase):
    options = {
        "bowser_bombs": Options.BowserBombs.option_both,
        "bowser_in_the_dark_world_health": 4,
    }

    def test_global_and_per_level_bombs_are_combined(self):
        self.collect_all_but({
            "Bowser Arena Bomb 1", "Bowser Arena Bomb 2", "Bowser Arena Bomb 3", "Bowser Arena Bomb 4",
            "Bowser in the Dark World - Bowser Arena Bomb 1",
            "Bowser in the Dark World - Bowser Arena Bomb 2",
            "Bowser in the Dark World - Bowser Arena Bomb 3",
            "Bowser in the Dark World - Bowser Arena Bomb 4",
        })
        self.collect([
            self.get_item_by_name("Bowser Arena Bomb 1"),
            self.get_item_by_name("Bowser Arena Bomb 2"),
        ])
        self.collect([
            self.get_item_by_name("Bowser in the Dark World - Bowser Arena Bomb 3"),
            self.get_item_by_name("Bowser in the Dark World - Bowser Arena Bomb 4"),
        ])
        self.assertTrue(self.can_reach_location("Bowser in the Dark World - Key"))


class WetDryWorldPermanentCoinCollectionTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **WetDryWorldIndividualUnlockLogicTestBase.options,
    }

    @staticmethod
    def maximum_reachable_coins(state, player):
        return max(
            coins for coins in range(153)
            if wet_dry_world_coins(state, player, coins)
        )

    def test_permanent_collection_combines_reachable_water_levels(self):
        state = CollectionState(self.multiworld)
        for item_name in [
            "Progressive Upstairs Key",
            "Ground Pound",
            "Long Jump",
            "Triple Jump",
            "Dive",
            "Ledge Grab",
            "Wet-Dry World - Purple Switch",
            "Wet-Dry World - Cannon Unlock",
            "Wet-Dry World - Red Coins",
            "Wet-Dry World - Blue Coin Block",
            "Wet-Dry World - Horizontal Coin Lines",
            "Wet-Dry World - Horizontal Coin Rings",
            "Wet-Dry World - Breakable Coin Boxes",
            "Wet-Dry World - 3-Coin Blocks",
            "Wet-Dry World - 10-Coin Blocks",
            "Wet-Dry World - Chuckya",
            "Wet-Dry World - Skeeters",
        ]:
            state.collect(self.world.create_item(item_name))
        self.assertFalse(state.has("Wet-Dry World - Water Level Diamond", self.player))
        self.assertTrue(state.can_reach("Wet-Dry World - Low Water", "Region", self.player))
        self.assertTrue(state.can_reach("Wet-Dry World - Mid Water", "Region", self.player))
        self.assertTrue(state.can_reach("Wet-Dry World - Highest Water", "Region", self.player))

        self.assertGreater(self.maximum_reachable_coins(state, self.player), 0)
