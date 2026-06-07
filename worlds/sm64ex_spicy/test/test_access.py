from .bases import SM64TestBase
from .. import Options
from ..Regions import sm64_ttc_entrances


class GroupedCastleKeyAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "enable_locked_paintings": Options.EnableLockedPaintings.option_false,
        "area_rando": Options.AreaRandomizer.option_Off,
    }

    def test_BitDW_entrance_access(self):
        self.assertFalse(self.can_reach_region("Bowser in the Dark World"))
        self.collect(self.get_item_by_name("First Floor Key"))
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
        self.collect(self.get_item_by_name("Dire, Dire Docks - Bowser's Sub"))
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


class CastleFeatureAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "enable_locked_paintings": Options.EnableLockedPaintings.option_false,
        "area_rando": Options.AreaRandomizer.option_Off,
    }

    def test_mips_access(self):
        self.assertFalse(self.can_reach_location("MIPS 1"))
        self.collect(self.get_item_by_name("Progressive Basement Key"))
        self.assertFalse(self.can_reach_location("MIPS 1"))
        self.collect(self.get_item_by_name("Progressive MIPS"))
        self.assertTrue(self.can_reach_location("MIPS 1"))
        self.assertFalse(self.can_reach_location("MIPS 2"))
        self.collect(self.get_item_by_name("Progressive MIPS"))
        self.assertTrue(self.can_reach_location("MIPS 2"))

    def test_castle_toad_access(self):
        self.assertFalse(self.can_reach_location("Toad (Basement)"))
        self.collect(self.get_item_by_name("Castle Toads"))
        self.collect(self.get_item_by_name("Progressive Basement Key"))
        self.assertTrue(self.can_reach_location("Toad (Basement)"))

        self.assertFalse(self.can_reach_location("Toad (Second Floor)"))
        self.collect(self.get_item_by_name("Progressive Upstairs Key"))
        self.assertTrue(self.can_reach_location("Toad (Second Floor)"))

        self.assertFalse(self.can_reach_location("Toad (Third Floor)"))
        self.collect(self.get_item_by_name("Progressive Upstairs Key"))
        self.assertTrue(self.can_reach_location("Toad (Third Floor)"))

    def test_castle_feature_regions(self):
        self.assertFalse(self.can_reach_region("Big Boo's Haunt"))
        self.collect(self.get_item_by_name("Courtyard Boos"))
        self.assertTrue(self.can_reach_region("Big Boo's Haunt"))

        self.assertFalse(self.can_reach_region("Tower of the Wing Cap"))
        self.collect(self.get_item_by_name("Wing Cap Light"))
        self.assertTrue(self.can_reach_region("Tower of the Wing Cap"))

        self.assertFalse(self.can_reach_region("Wing Mario over the Rainbow"))
        self.collect(self.get_item_by_name("Castle Cannon"))
        self.assertTrue(self.can_reach_region("Wing Mario over the Rainbow"))

    def test_yoshi_access(self):
        self.assertFalse(self.can_reach_location("Yoshi"))
        self.collect(self.get_item_by_name("Castle Cannon"))
        self.assertFalse(self.can_reach_location("Yoshi"))
        self.collect(self.get_item_by_name("Yoshi"))
        self.assertTrue(self.can_reach_location("Yoshi"))

    def test_yoshi_access_requires_castle_cannon(self):
        self.collect(self.get_item_by_name("Yoshi"))
        self.assertFalse(self.can_reach_location("Yoshi"))
        self.collect(self.get_item_by_name("Castle Cannon"))
        self.assertTrue(self.can_reach_location("Yoshi"))


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


class ArbitraryFeatureAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "buddy_checks": Options.BuddyChecks.option_true,
        "enable_locked_paintings": Options.EnableLockedPaintings.option_false,
        "enable_move_rando": Options.EnableMoveRandomizer.option_true,
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

        self.collect(self.get_item_by_name("Checkerboard Platforms"))
        self.assertTrue(self.can_reach_region("Hazy Maze Cave - Red Coin Area"))

    def test_rainbow_ride_carpets_gate_all_checks(self):
        self.collect_third_floor_access()
        self.collect(self.get_item_by_name("Side Flip"))
        self.assertTrue(self.can_reach_region("Rainbow Ride"))
        self.assertFalse(self.can_reach_region("Rainbow Ride - Carpets"))
        self.assertFalse(self.can_reach_location("Rainbow Ride - Swingin' in the Breeze"))

        self.collect(self.get_item_by_name("Rainbow Ride - Carpets"))
        self.assertTrue(self.can_reach_region("Rainbow Ride - Carpets"))
        self.assertTrue(self.can_reach_location("Rainbow Ride - Swingin' in the Breeze"))

    def test_rainbow_ride_cruiser_still_requires_carpets(self):
        self.collect_third_floor_access()
        self.collect([self.get_item_by_name("Side Flip"), self.get_item_by_name("Long Jump")])
        self.assertTrue(self.can_reach_region("Rainbow Ride - Carpets"))
        self.assertFalse(self.can_reach_region("Rainbow Ride - Cruiser"))

        self.collect(self.get_item_by_name("Rainbow Ride - Carpets"))
        self.assertTrue(self.can_reach_region("Rainbow Ride - Cruiser"))

    def test_whomps_fortress_top_access(self):
        self.assertFalse(self.can_reach_region("Whomp's Fortress - Top"))
        self.collect(self.get_item_by_name("Wall Kick"))
        self.assertFalse(self.can_reach_region("Whomp's Fortress - Top"))
        self.collect(self.get_item_by_name("Side Flip"))
        self.assertTrue(self.can_reach_region("Whomp's Fortress - Top"))

    def test_whomps_fortress_caged_island_fortress_routes_need_top(self):
        self.collect([self.get_item_by_name("Whomp's Fortress - Fortress"), self.get_item_by_name("Climb")])
        self.assertFalse(self.can_reach_location("Whomp's Fortress - Fall onto the Caged Island"))

        self.collect(self.get_item_by_name("Checkerboard Platforms"))
        self.assertTrue(self.can_reach_location("Whomp's Fortress - Fall onto the Caged Island"))

    def test_lll_red_hot_log_rolling_requires_log_shell_or_wing_cap(self):
        self.collect_basement_access()
        self.assertFalse(self.can_reach_location("Lethal Lava Land - Red-Hot Log Rolling"))

        self.collect(self.get_item_by_name("Lethal Lava Land - Rolling Log"))
        self.assertTrue(self.can_reach_location("Lethal Lava Land - Red-Hot Log Rolling"))

    def test_lll_elevator_tour_accepts_checkerboard_platforms(self):
        self.collect_basement_access()
        self.collect(self.get_item_by_name("Climb"))
        self.assertFalse(self.can_reach_location("Lethal Lava Land - Elevator Tour in the Volcano"))

        self.collect(self.get_item_by_name("Checkerboard Platforms"))
        self.assertTrue(self.can_reach_location("Lethal Lava Land - Elevator Tour in the Volcano"))

    def test_vanish_cap_under_moat_requires_checkerboard_platforms(self):
        self.collect_basement_access()
        self.collect([
            self.get_item_by_name("Ground Pound"),
            self.get_item_by_name("Wall Kick"),
            self.get_item_by_name("Vanish Cap"),
        ])
        self.assertFalse(self.can_reach_location("Vanish Cap Under the Moat Switch"))
        self.assertFalse(self.can_reach_location("Vanish Cap Under the Moat Red Coins"))

        self.collect(self.get_item_by_name("Checkerboard Platforms"))
        self.assertTrue(self.can_reach_location("Vanish Cap Under the Moat Switch"))
        self.assertTrue(self.can_reach_location("Vanish Cap Under the Moat Red Coins"))

    def test_tiny_huge_island_pipes_require_warp_pipes(self):
        self.collect_second_floor_access()
        self.collect(self.get_item_by_name("Long Jump"))
        self.assertFalse(self.can_reach_region("Tiny-Huge Island - Pipes"))

        self.collect(self.get_item_by_name("Tiny-Huge Island - Warp Pipes"))
        self.assertTrue(self.can_reach_region("Tiny-Huge Island - Pipes"))

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

        self.collect(self.get_item_by_name("Cannon Unlock Snowman's Land"))
        self.assertTrue(self.can_reach_location("Snowman's Land - Snowman's Big Head"))

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


class BigBooHauntAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        "enable_locked_paintings": Options.EnableLockedPaintings.option_false,
        "enable_move_rando": Options.EnableMoveRandomizer.option_true,
        "area_rando": Options.AreaRandomizer.option_Off,
    }

    def collect_bbh_access(self):
        self.collect(self.get_item_by_name("Courtyard Boos"))

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


class WetDryWorldVariantAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "enable_locked_paintings": Options.EnableLockedPaintings.option_false,
        "enable_move_rando": Options.EnableMoveRandomizer.option_true,
        "area_rando": Options.AreaRandomizer.option_Off,
    }

    def collect_second_floor_access(self):
        self.collect(self.get_item_by_name("Progressive Upstairs Key"))

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
        self.assertFalse(self.can_reach_region("Wet-Dry World - Downtown"))

        self.collect([self.get_item_by_name("Ledge Grab"), self.get_item_by_name("Triple Jump")])
        self.assertTrue(self.can_reach_region("Wet-Dry World - Downtown"))


class GlobalCapAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "enable_locked_paintings": Options.EnableLockedPaintings.option_false,
        "area_rando": Options.AreaRandomizer.option_Off,
    }

    def test_bob_wing_cap_access(self):
        self.collect(self.get_item_by_name("Bob-omb Battlefield - Bob-omb Buddy"))
        self.collect(self.get_item_by_name("Cannon Unlock Bob-omb Battlefield"))
        self.assertFalse(self.can_reach_location("Bob-omb Battlefield - Mario Wings to the Sky"))
        self.collect(self.world.create_item("Bob-omb Battlefield - Wing Cap"))
        self.assertFalse(self.can_reach_location("Bob-omb Battlefield - Mario Wings to the Sky"))
        self.collect(self.get_item_by_name("Wing Cap"))
        self.assertTrue(self.can_reach_location("Bob-omb Battlefield - Mario Wings to the Sky"))


class PerLevelCapAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "enable_locked_paintings": Options.EnableLockedPaintings.option_false,
        "area_rando": Options.AreaRandomizer.option_Off,
        "per_level_cap_items": Options.PerLevelCapItems.option_true,
    }

    def test_bob_wing_cap_access(self):
        self.collect(self.get_item_by_name("Bob-omb Battlefield - Bob-omb Buddy"))
        self.collect(self.get_item_by_name("Cannon Unlock Bob-omb Battlefield"))
        self.assertFalse(self.can_reach_location("Bob-omb Battlefield - Mario Wings to the Sky"))
        self.collect(self.world.create_item("Wing Cap"))
        self.assertFalse(self.can_reach_location("Bob-omb Battlefield - Mario Wings to the Sky"))
        self.collect(self.get_item_by_name("Bob-omb Battlefield - Wing Cap"))
        self.assertTrue(self.can_reach_location("Bob-omb Battlefield - Mario Wings to the Sky"))

    def test_tower_wing_cap_access(self):
        self.collect(self.get_item_by_name("Wing Cap Light"))
        self.assertFalse(self.can_reach_location("Tower of the Wing Cap Red Coins"))
        self.collect(self.get_item_by_name("Tower of the Wing Cap - Wing Cap"))
        self.assertTrue(self.can_reach_location("Tower of the Wing Cap Red Coins"))

    def test_hmc_metal_cap_access(self):
        self.collect(self.get_item_by_name("Progressive Basement Key"))
        self.assertFalse(self.can_reach_location("Hazy Maze Cave - Metal-Head Mario Can Move!"))
        self.collect(self.get_item_by_name("Hazy Maze Cave - Metal Cap"))
        self.assertTrue(self.can_reach_location("Hazy Maze Cave - Metal-Head Mario Can Move!"))

    def test_vcutm_vanish_cap_access(self):
        self.collect(self.get_item_by_name("Progressive Basement Key"))
        self.collect(self.get_item_by_name("Checkerboard Platforms"))
        self.assertFalse(self.can_reach_location("Vanish Cap Under the Moat Red Coins"))
        self.collect(self.get_item_by_name("Vanish Cap Under the Moat - Vanish Cap"))
        self.assertTrue(self.can_reach_location("Vanish Cap Under the Moat Red Coins"))

    def test_lethal_lava_land_wing_cap_access(self):
        self.collect(self.get_item_by_name("Progressive Basement Key"))
        self.assertFalse(self.can_reach_location("Lethal Lava Land - Red-Hot Log Rolling"))
        self.collect(self.get_item_by_name("Lethal Lava Land - Wing Cap"))
        self.assertTrue(self.can_reach_location("Lethal Lava Land - Red-Hot Log Rolling"))


class TTCVariantAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
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
