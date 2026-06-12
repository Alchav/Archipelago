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


class GroupedCastleKeyAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "enable_locked_paintings": Options.EnableLockedPaintings.option_false,
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
        self.collect(self.get_item_by_name("Cannon Unlock - Castle"))
        self.assertFalse(self.can_reach_region("Wing Mario over the Rainbow"))
        self.collect([self.get_item_by_name("Progressive Upstairs Key")] * 2)
        self.assertTrue(self.can_reach_region("Wing Mario over the Rainbow"))

    def test_yoshi_access(self):
        self.assertFalse(self.can_reach_location("Yoshi"))
        self.collect(self.get_item_by_name("Cannon Unlock - Castle"))
        self.assertFalse(self.can_reach_location("Yoshi"))
        self.collect(self.get_item_by_name("Yoshi"))
        self.assertTrue(self.can_reach_location("Yoshi"))

    def test_yoshi_access_requires_castle_cannon(self):
        self.collect(self.get_item_by_name("Yoshi"))
        self.assertFalse(self.can_reach_location("Yoshi"))
        self.collect(self.get_item_by_name("Cannon Unlock - Castle"))
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

    def test_cap_switch_stage_rule_uses_shared_move_item(self):
        self.collect([self.get_item_by_name("Progressive Key")] * 2)
        self.collect(self.get_item_by_name("Checkerboard Platforms"))
        self.assertFalse(self.can_reach_location("Vanish Cap Under the Moat Switch"))

        self.collect(self.world.create_item("Whomp's Fortress - Wall Kick"))
        self.assertFalse(self.can_reach_location("Vanish Cap Under the Moat Switch"))

        self.collect(self.world.create_item("Cap Switch Stages - Wall Kick"))
        self.assertTrue(self.can_reach_location("Vanish Cap Under the Moat Switch"))

    def test_cap_switch_stage_names_use_shared_move_items(self):
        for level_name in (
                "Tower of the Wing Cap",
                "Cavern of the Metal Cap",
                "Vanish Cap Under the Moat",
        ):
            with self.subTest("Cap switch stage move alias", level=level_name):
                self.assertEqual(
                    get_per_level_action_item_name(level_name, "Triple Jump"),
                    "Cap Switch Stages - Triple Jump")

    def test_wmotR_rule_uses_castle_move_item(self):
        self.collect([self.get_item_by_name("Progressive Key")] * 5)
        self.collect(self.world.create_item("Wing Cap"))
        self.assertFalse(self.can_reach_location("Wing Mario Over the Rainbow Red Coins"))

        self.collect(self.world.create_item("Cap Switch Stages - Triple Jump"))
        self.assertFalse(self.can_reach_location("Wing Mario Over the Rainbow Red Coins"))

        self.collect(self.world.create_item("Castle - Triple Jump"))
        self.assertTrue(self.can_reach_location("Wing Mario Over the Rainbow Red Coins"))


class ArbitraryFeatureAccessTestBase(SM64TestBase):
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

    def test_whomps_fortress_top_access(self):
        self.assertFalse(self.can_reach_region("Whomp's Fortress - Top"))
        self.collect(self.get_item_by_name("Wall Kick"))
        self.assertFalse(self.can_reach_region("Whomp's Fortress - Top"))
        self.collect(self.get_item_by_name("Side Flip"))
        self.assertTrue(self.can_reach_region("Whomp's Fortress - Top"))

    def test_whomps_fortress_caged_island_fortress_routes_need_top(self):
        self.collect([self.get_item_by_name("Whomp's Fortress - Fortress"), self.get_item_by_name("Climb")])
        self.assertFalse(self.can_reach_location("Whomp's Fortress - Fall onto the Caged Island"))

        self.collect(self.world.create_item("Checkerboard Platforms"))
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

    def test_tiny_huge_island_pipes_from_tiny_do_not_require_purple_switches(self):
        self.multiworld.get_entrance("Second Floor -> Tiny-Huge Island (Huge)", self.player).access_rule = \
            lambda state: False

        self.collect_second_floor_access()
        self.collect([
            self.get_item_by_name("Long Jump"),
            self.get_item_by_name("Tiny-Huge Island - Warp Pipes"),
        ])
        self.assertTrue(self.can_reach_region("Tiny-Huge Island (Tiny)"))
        self.assertFalse(self.can_reach_region("Tiny-Huge Island (Huge)"))
        self.assertTrue(self.can_reach_region("Tiny-Huge Island - Pipes"))

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

    def test_wet_dry_world_express_elevator_requires_purple_switches(self):
        self.collect_second_floor_access()
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

    def test_tiny_huge_island_five_secrets_from_tiny_requires_purple_switches(self):
        self.multiworld.get_entrance("Second Floor -> Tiny-Huge Island (Huge)", self.player).access_rule = \
            lambda state: False

        self.collect_second_floor_access()
        self.assertTrue(self.can_reach_region("Tiny-Huge Island (Tiny)"))
        self.assertFalse(self.can_reach_region("Tiny-Huge Island - Pipes"))
        self.assertFalse(self.can_reach_location("Tiny-Huge Island - Five Itty Bitty Secrets"))

        self.collect(self.get_item_by_name("Purple Switches"))
        self.assertTrue(self.can_reach_location("Tiny-Huge Island - Five Itty Bitty Secrets"))

    def test_tiny_huge_island_five_secrets_from_huge_requires_pipes_and_purple_switches(self):
        self.multiworld.get_entrance("Second Floor -> Tiny-Huge Island (Tiny)", self.player).access_rule = \
            lambda state: False

        self.collect_second_floor_access()
        self.assertTrue(self.can_reach_region("Tiny-Huge Island (Huge)"))
        self.assertFalse(self.can_reach_region("Tiny-Huge Island (Tiny)"))
        self.assertFalse(self.can_reach_location("Tiny-Huge Island - Five Itty Bitty Secrets"))

        self.collect(self.get_item_by_name("Purple Switches"))
        self.assertFalse(self.can_reach_location("Tiny-Huge Island - Five Itty Bitty Secrets"))

        self.collect([
            self.get_item_by_name("Long Jump"),
            self.get_item_by_name("Tiny-Huge Island - Warp Pipes"),
        ])
        self.assertTrue(self.can_reach_region("Tiny-Huge Island - Pipes"))
        self.assertTrue(self.can_reach_location("Tiny-Huge Island - Five Itty Bitty Secrets"))

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

    def test_bitdw_red_coins_and_key_require_purple_switches(self):
        self.collect(self.get_item_by_name("Dark World Key"))
        self.assertTrue(self.can_reach_region("Bowser in the Dark World"))
        self.assertFalse(self.can_reach_location("Bowser in the Dark World Red Coins"))
        self.assertFalse(self.can_reach_location("Bowser in the Dark World Key"))

        self.collect(self.get_item_by_name("Purple Switches"))
        self.assertTrue(self.can_reach_location("Bowser in the Dark World Red Coins"))
        self.assertTrue(self.can_reach_location("Bowser in the Dark World Key"))

    def test_bowser_in_the_sky_top_requires_purple_switches(self):
        self.collect([self.get_item_by_name("Progressive Upstairs Key")] * 3)
        self.collect([
            self.get_item_by_name("Climb"),
            self.get_item_by_name("Triple Jump"),
        ])
        self.assertTrue(self.can_reach_region("Bowser in the Sky"))
        self.assertFalse(self.can_reach_region("Bowser in the Sky - Top"))

        self.collect(self.get_item_by_name("Purple Switches"))
        self.assertTrue(self.can_reach_region("Bowser in the Sky - Top"))

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

        self.collect(self.get_item_by_name("Whomp's Fortress - Checkerboard Platforms"))
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

        self.collect(self.get_item_by_name("Tiny-Huge Island - Purple Switch"))
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
        self.collect(self.get_item_by_name("Cannon Unlock Cool, Cool Mountain"))
        self.assertTrue(self.can_reach_location("Cool, Cool Mountain - Coins Star"))


class CoolCoolMountainCoinStar141MovelessAccessTestBase(CoolCoolMountainCoinStarAccessTestBase):
    options = {
        **CoolCoolMountainCoinStarAccessTestBase.options,
        "strict_move_requirements": Options.StrictMoveRequirements.option_false,
        "cool_cool_mountain_coin_star_requirement": 141,
    }

    def test_moveless_wall_kicks_route_coins_reach_coin_star(self):
        self.assertTrue(self.can_reach_location("Cool, Cool Mountain - Coins Star"))


class CoolCoolMountainCoinStar144MovelessAccessTestBase(CoolCoolMountainCoinStarAccessTestBase):
    options = {
        **CoolCoolMountainCoinStarAccessTestBase.options,
        "strict_move_requirements": Options.StrictMoveRequirements.option_false,
        "cool_cool_mountain_coin_star_requirement": 144,
    }

    def test_moveless_wall_kicks_route_needs_cannon_for_extra_spindrift_coins(self):
        self.assertFalse(self.can_reach_location("Cool, Cool Mountain - Coins Star"))
        self.collect(self.get_item_by_name("Cannon Unlock Cool, Cool Mountain"))
        self.assertTrue(self.can_reach_location("Cool, Cool Mountain - Coins Star"))


class CoolCoolMountainCoinStar154AccessTestBase(CoolCoolMountainCoinStarAccessTestBase):
    options = {
        **CoolCoolMountainCoinStarAccessTestBase.options,
        "cool_cool_mountain_coin_star_requirement": 154,
    }

    def test_all_coin_sources_reach_coin_star(self):
        self.collect(self.get_item_by_name("Cannon Unlock Cool, Cool Mountain"))
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


class WhompsFortressCoinStar73AccessTestBase(WhompsFortressCoinStarAccessTestBase):
    options = {
        **WhompsFortressCoinStarAccessTestBase.options,
        "whomps_fortress_coin_star_requirement": 73,
    }

    def test_start_coins_reach_coin_star(self):
        self.assertTrue(self.can_reach_location("Whomp's Fortress - Coins Star"))


class WhompsFortressCoinStar74AccessTestBase(WhompsFortressCoinStarAccessTestBase):
    options = {
        **WhompsFortressCoinStarAccessTestBase.options,
        "whomps_fortress_coin_star_requirement": 74,
    }

    def test_shoot_into_the_wild_blue_coins_reach_coin_star(self):
        self.assertFalse(self.can_reach_location("Whomp's Fortress - Coins Star"))
        self.collect(self.get_item_by_name("Cannon Unlock Whomp's Fortress"))
        self.assertTrue(self.can_reach_location("Whomp's Fortress - Shoot into the Wild Blue"))
        self.assertTrue(self.can_reach_location("Whomp's Fortress - Coins Star"))


class WhompsFortressCoinStar82AccessTestBase(WhompsFortressCoinStarAccessTestBase):
    options = {
        **WhompsFortressCoinStarAccessTestBase.options,
        "whomps_fortress_coin_star_requirement": 82,
    }

    def test_top_coins_reach_coin_star(self):
        self.assertFalse(self.can_reach_location("Whomp's Fortress - Coins Star"))
        self.collect(self.get_item_by_name("Checkerboard Platforms"))
        self.assertTrue(self.can_reach_region("Whomp's Fortress - Top"))
        self.assertTrue(self.can_reach_location("Whomp's Fortress - Coins Star"))


class WhompsFortressCoinStar94AccessTestBase(WhompsFortressCoinStarAccessTestBase):
    options = {
        **WhompsFortressCoinStarAccessTestBase.options,
        "whomps_fortress_coin_star_requirement": 94,
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
            self.get_item_by_name("Cannon Unlock Whomp's Fortress"),
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


class BobOmbBattlefieldCoinStar109AccessTestBase(BobOmbBattlefieldCoinStarAccessTestBase):
    options = {
        **BobOmbBattlefieldCoinStarAccessTestBase.options,
        "bob_omb_battlefield_coin_star_requirement": 109,
    }

    def test_start_coins_reach_coin_star(self):
        self.assertTrue(self.can_reach_location("Bob-omb Battlefield - Coins Star"))


class BobOmbBattlefieldCoinStar110AccessTestBase(BobOmbBattlefieldCoinStarAccessTestBase):
    options = {
        **BobOmbBattlefieldCoinStarAccessTestBase.options,
        "bob_omb_battlefield_coin_star_requirement": 110,
    }

    def test_island_coins_reach_coin_star(self):
        self.assertFalse(self.can_reach_location("Bob-omb Battlefield - Coins Star"))
        self.collect(self.get_item_by_name("Cannon Unlock Bob-omb Battlefield"))
        self.assertTrue(self.can_reach_region("Bob-omb Battlefield - Island"))
        self.assertTrue(self.can_reach_location("Bob-omb Battlefield - Coins Star"))


class BobOmbBattlefieldCoinStar113AccessTestBase(BobOmbBattlefieldCoinStarAccessTestBase):
    options = {
        **BobOmbBattlefieldCoinStarAccessTestBase.options,
        "bob_omb_battlefield_coin_star_requirement": 113,
    }

    def test_climb_coins_reach_coin_star(self):
        self.collect(self.get_item_by_name("Cannon Unlock Bob-omb Battlefield"))
        self.assertFalse(self.can_reach_location("Bob-omb Battlefield - Coins Star"))
        self.collect(self.get_item_by_name("Climb"))
        self.assertTrue(self.can_reach_location("Bob-omb Battlefield - Coins Star"))


class BobOmbBattlefieldCoinStar115AccessTestBase(BobOmbBattlefieldCoinStarAccessTestBase):
    options = {
        **BobOmbBattlefieldCoinStarAccessTestBase.options,
        "bob_omb_battlefield_coin_star_requirement": 115,
    }

    def test_side_flip_backflip_or_triple_jump_coins_reach_coin_star(self):
        self.collect(self.get_item_by_name("Cannon Unlock Bob-omb Battlefield"))
        self.assertFalse(self.can_reach_location("Bob-omb Battlefield - Coins Star"))
        self.collect(self.get_item_by_name("Side Flip"))
        self.assertTrue(self.can_reach_location("Bob-omb Battlefield - Coins Star"))


class BobOmbBattlefieldCoinStar118AccessTestBase(BobOmbBattlefieldCoinStarAccessTestBase):
    options = {
        **BobOmbBattlefieldCoinStarAccessTestBase.options,
        "bob_omb_battlefield_coin_star_requirement": 118,
    }

    def test_triple_jump_extra_coin_reaches_coin_star(self):
        self.collect([
            self.get_item_by_name("Cannon Unlock Bob-omb Battlefield"),
            self.get_item_by_name("Side Flip"),
        ])
        self.assertFalse(self.can_reach_location("Bob-omb Battlefield - Coins Star"))
        self.remove_by_name("Side Flip")
        self.collect(self.get_item_by_name("Triple Jump"))
        self.assertTrue(self.can_reach_location("Bob-omb Battlefield - Coins Star"))


class BobOmbBattlefieldCoinStar121AccessTestBase(BobOmbBattlefieldCoinStarAccessTestBase):
    options = {
        **BobOmbBattlefieldCoinStarAccessTestBase.options,
        "bob_omb_battlefield_coin_star_requirement": 121,
    }

    def test_mario_wings_to_the_sky_coins_reach_coin_star(self):
        self.collect(self.get_item_by_name("Cannon Unlock Bob-omb Battlefield"))
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


class JollyRogerBayCoinStar54AccessTestBase(JollyRogerBayCoinStarAccessTestBase):
    options = {
        **JollyRogerBayCoinStarAccessTestBase.options,
        "jolly_roger_bay_coin_star_requirement": 54,
    }

    def test_start_coins_reach_coin_star(self):
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


class JollyRogerBayCoinStar71AccessTestBase(JollyRogerBayCoinStarAccessTestBase):
    options = {
        **JollyRogerBayCoinStarAccessTestBase.options,
        "jolly_roger_bay_coin_star_requirement": 71,
    }

    def test_raised_ship_coins_reach_coin_star(self):
        self.collect(self.get_item_by_name("Side Flip"))
        self.assertFalse(self.can_reach_location("Jolly Roger Bay - Coins Star"))
        self.collect(self.get_item_by_name("Jolly Roger Bay - Raised Ship"))
        self.assertTrue(self.can_reach_location("Jolly Roger Bay - Coins Star"))


class JollyRogerBayCoinStar75AccessTestBase(JollyRogerBayCoinStarAccessTestBase):
    options = {
        **JollyRogerBayCoinStarAccessTestBase.options,
        "jolly_roger_bay_coin_star_requirement": 75,
    }

    def test_ground_pound_coins_reach_coin_star(self):
        self.assertFalse(self.can_reach_location("Jolly Roger Bay - Coins Star"))
        self.collect(self.get_item_by_name("Ground Pound"))
        self.assertTrue(self.can_reach_location("Jolly Roger Bay - Coins Star"))


class JollyRogerBayCoinStar85AccessTestBase(JollyRogerBayCoinStarAccessTestBase):
    options = {
        **JollyRogerBayCoinStarAccessTestBase.options,
        "jolly_roger_bay_coin_star_requirement": 85,
    }

    def test_ground_pound_and_upper_coins_reach_coin_star(self):
        self.collect(self.get_item_by_name("Ground Pound"))
        self.assertFalse(self.can_reach_location("Jolly Roger Bay - Coins Star"))
        self.collect(self.get_item_by_name("Side Flip"))
        self.assertTrue(self.can_reach_location("Jolly Roger Bay - Coins Star"))


class JollyRogerBayCoinStar101AccessTestBase(JollyRogerBayCoinStarAccessTestBase):
    options = {
        **JollyRogerBayCoinStarAccessTestBase.options,
        "jolly_roger_bay_coin_star_requirement": 101,
    }

    def test_all_jrb_coin_sources_reach_coin_star(self):
        self.collect([
            self.get_item_by_name("Ground Pound"),
            self.get_item_by_name("Side Flip"),
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


class TinyHugeIslandCoinStar120FromTinyAccessTestBase(TinyHugeIslandCoinStarAccessTestBase):
    options = {
        **TinyHugeIslandCoinStarAccessTestBase.options,
        "tiny_huge_island_coin_star_requirement": 120,
    }

    def test_tiny_start_reaches_huge_coins_with_pipes(self):
        self.disable_huge_entry()
        self.collect_second_floor_access()
        self.assertTrue(self.can_reach_region("Tiny-Huge Island (Tiny)"))
        self.assertFalse(self.can_reach_region("Tiny-Huge Island (Huge)"))
        self.assertFalse(self.can_reach_location("Tiny-Huge Island - Coins Star"))

        self.collect([
            self.get_item_by_name("Ledge Grab"),
            self.get_item_by_name("Tiny-Huge Island - Warp Pipes"),
        ])
        self.assertTrue(self.can_reach_region("Tiny-Huge Island - Pipes"))
        self.assertTrue(self.can_reach_location("Tiny-Huge Island - Coins Star"))


class TinyHugeIslandCoinStar119AccessTestBase(TinyHugeIslandCoinStarAccessTestBase):
    options = {
        **TinyHugeIslandCoinStarAccessTestBase.options,
        "tiny_huge_island_coin_star_requirement": 119,
    }

    def test_huge_start_coins_reach_coin_star(self):
        self.disable_tiny_entry()
        self.collect_second_floor_access()
        self.assertTrue(self.can_reach_region("Tiny-Huge Island (Huge)"))
        self.assertTrue(self.can_reach_location("Tiny-Huge Island - Coins Star"))


class TinyHugeIslandCoinStar120FromHugeAccessTestBase(TinyHugeIslandCoinStarAccessTestBase):
    options = {
        **TinyHugeIslandCoinStarAccessTestBase.options,
        "tiny_huge_island_coin_star_requirement": 120,
    }

    def test_huge_start_reaches_tiny_coin_with_pipes(self):
        self.disable_tiny_entry()
        self.collect_second_floor_access()
        self.assertFalse(self.can_reach_location("Tiny-Huge Island - Coins Star"))
        self.collect([
            self.get_item_by_name("Ledge Grab"),
            self.get_item_by_name("Tiny-Huge Island - Warp Pipes"),
        ])
        self.assertTrue(self.can_reach_region("Tiny-Huge Island - Pipes"))
        self.assertTrue(self.can_reach_location("Tiny-Huge Island - Coins Star"))


class TinyHugeIslandCoinStar123AccessTestBase(TinyHugeIslandCoinStarAccessTestBase):
    options = {
        **TinyHugeIslandCoinStarAccessTestBase.options,
        "tiny_huge_island_coin_star_requirement": 123,
    }

    def test_wall_kick_coins_reach_coin_star(self):
        self.disable_tiny_entry()
        self.collect_second_floor_access()
        self.assertFalse(self.can_reach_location("Tiny-Huge Island - Coins Star"))
        self.collect(self.get_item_by_name("Wall Kick"))
        self.assertTrue(self.can_reach_location("Tiny-Huge Island - Coins Star"))


class TinyHugeIslandCoinStar124AccessTestBase(TinyHugeIslandCoinStarAccessTestBase):
    options = {
        **TinyHugeIslandCoinStarAccessTestBase.options,
        "tiny_huge_island_coin_star_requirement": 124,
    }

    def test_cannon_coins_reach_coin_star(self):
        self.disable_tiny_entry()
        self.collect_second_floor_access()
        self.assertFalse(self.can_reach_location("Tiny-Huge Island - Coins Star"))
        self.collect(self.get_item_by_name("Cannon Unlock Tiny-Huge Island"))
        self.assertTrue(self.can_reach_location("Tiny-Huge Island - Coins Star"))


class TinyHugeIslandCoinStar129AccessTestBase(TinyHugeIslandCoinStarAccessTestBase):
    options = {
        **TinyHugeIslandCoinStarAccessTestBase.options,
        "tiny_huge_island_coin_star_requirement": 129,
    }

    def test_ground_pound_coins_reach_coin_star(self):
        self.disable_tiny_entry()
        self.collect_second_floor_access()
        self.assertFalse(self.can_reach_location("Tiny-Huge Island - Coins Star"))
        self.collect(self.get_item_by_name("Ground Pound"))
        self.assertTrue(self.can_reach_location("Tiny-Huge Island - Coins Star"))


class TinyHugeIslandCoinStar130AccessTestBase(TinyHugeIslandCoinStarAccessTestBase):
    options = {
        **TinyHugeIslandCoinStarAccessTestBase.options,
        "tiny_huge_island_coin_star_requirement": 130,
    }

    def test_large_top_coins_reach_coin_star(self):
        self.disable_tiny_entry()
        self.collect_second_floor_access()
        self.collect([
            self.get_item_by_name("Ledge Grab"),
            self.get_item_by_name("Tiny-Huge Island - Warp Pipes"),
        ])
        self.assertFalse(self.can_reach_location("Tiny-Huge Island - Coins Star"))
        self.collect(self.get_item_by_name("Dive"))
        self.assertTrue(self.can_reach_region("Tiny-Huge Island - Large Top"))
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
        self.assertTrue(self.can_reach_region("Tiny-Huge Island - Large Top"))
        self.assertTrue(self.can_reach_location("Tiny-Huge Island - Make Wiggler Squirm"))
        self.assertFalse(self.can_reach_location("Tiny-Huge Island - Coins Star"))
        self.collect(self.get_item_by_name("Cannon Unlock Tiny-Huge Island"))
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


class HazyMazeCaveCoinStar83AccessTestBase(HazyMazeCaveCoinStarAccessTestBase):
    options = {
        **HazyMazeCaveCoinStarAccessTestBase.options,
        "hazy_maze_cave_coin_star_requirement": 83,
    }

    def test_start_coins_reach_coin_star(self):
        self.collect_basement_access()
        self.assertTrue(self.can_reach_location("Hazy Maze Cave - Coins Star"))


class HazyMazeCaveCoinStar86AccessTestBase(HazyMazeCaveCoinStarAccessTestBase):
    options = {
        **HazyMazeCaveCoinStarAccessTestBase.options,
        "hazy_maze_cave_coin_star_requirement": 86,
    }

    def test_metal_cap_coins_reach_coin_star(self):
        self.collect_basement_access()
        self.assertFalse(self.can_reach_location("Hazy Maze Cave - Coins Star"))
        self.collect(self.get_item_by_name("Metal Cap"))
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
        self.collect(self.get_item_by_name("Triple Jump"))
        self.assertTrue(self.can_reach_location("Hazy Maze Cave - Coins Star"))


class HazyMazeCaveCoinStar88AccessTestBase(HazyMazeCaveCoinStarAccessTestBase):
    options = {
        **HazyMazeCaveCoinStarAccessTestBase.options,
        "hazy_maze_cave_coin_star_requirement": 88,
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


class HazyMazeCaveCoinStar91AccessTestBase(HazyMazeCaveCoinStarAccessTestBase):
    options = {
        **HazyMazeCaveCoinStarAccessTestBase.options,
        "hazy_maze_cave_coin_star_requirement": 91,
    }

    def test_swimming_beast_coins_reach_coin_star(self):
        self.collect_basement_access()
        self.assertFalse(self.can_reach_location("Hazy Maze Cave - Coins Star"))
        self.collect(self.get_item_by_name("Hazy Maze Cave - Swimming Beast"))
        self.assertTrue(self.can_reach_location("Hazy Maze Cave - Coins Star"))


class HazyMazeCaveCoinStar118AccessTestBase(HazyMazeCaveCoinStarAccessTestBase):
    options = {
        **HazyMazeCaveCoinStarAccessTestBase.options,
        "hazy_maze_cave_coin_star_requirement": 118,
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
        ])
        self.assertFalse(self.can_reach_location("Hazy Maze Cave - Coins Star"))

        self.collect(self.get_item_by_name("Climb"))
        self.assertTrue(self.can_reach_region("Hazy Maze Cave - Pit Islands"))
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

        self.collect(self.get_item_by_name("Cannon Unlock Snowman's Land"))
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
        self.collect(self.get_item_by_name("Cannon Unlock Snowman's Land"))
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
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
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


class BigBooHauntCoinStarAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
        "enable_locked_paintings": Options.EnableLockedPaintings.option_false,
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "area_rando": Options.AreaRandomizer.option_Off,
    }

    def collect_bbh_access(self):
        self.collect(self.get_item_by_name("Courtyard Boos"))


class BigBooHauntCoinStar88AccessTestBase(BigBooHauntCoinStarAccessTestBase):
    options = {
        **BigBooHauntCoinStarAccessTestBase.options,
        "big_boos_haunt_coin_star_requirement": 88,
    }

    def test_start_coins_reach_coin_star(self):
        self.collect_bbh_access()
        self.assertTrue(self.can_reach_location("Big Boo's Haunt - Coins Star"))


class BigBooHauntCoinStar89AccessTestBase(BigBooHauntCoinStarAccessTestBase):
    options = {
        **BigBooHauntCoinStarAccessTestBase.options,
        "big_boos_haunt_coin_star_requirement": 89,
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


class BigBooHauntCoinStar113AccessTestBase(BigBooHauntCoinStarAccessTestBase):
    options = {
        **BigBooHauntCoinStarAccessTestBase.options,
        "big_boos_haunt_coin_star_requirement": 113,
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
        self.assertFalse(self.can_reach_region("Wet-Dry World - Downtown"))

        self.collect([self.get_item_by_name("Ledge Grab"), self.get_item_by_name("Triple Jump")])
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
        self.assertFalse(self.can_reach_location("Wet-Dry World - 1Up Block in Downtown"))

        self.collect(self.get_item_by_name("Wet-Dry World - Water Level Diamond"))
        self.assertTrue(self.can_reach_location("Wet-Dry World - Go to Town for Red Coins"))
        self.assertTrue(self.can_reach_location("Wet-Dry World - 1Up Block in Downtown"))

    def test_low_water_can_raise_to_high_but_not_highest(self):
        self.disable_wdw_entrance("Wet-Dry World Middle")
        self.disable_wdw_entrance("Wet-Dry World High")
        self.collect_second_floor_access()
        self.assertTrue(self.can_reach_region("Wet-Dry World - Low Water"))
        self.assertFalse(self.can_reach_region("Wet-Dry World - Mid Water"))
        self.assertTrue(self.can_reach_region("Wet-Dry World - Cannon"))
        self.assertTrue(self.can_reach_location("Wet-Dry World - Shocking Arrow Lifts!"))
        self.assertTrue(self.can_reach_location("Wet-Dry World - Secrets in the Shallows & Sky"))

        self.collect(self.get_item_by_name("Wet-Dry World - Water Level Diamond"))
        self.assertTrue(self.can_reach_region("Wet-Dry World - Mid Water"))
        self.assertFalse(self.can_reach_region("Wet-Dry World - Mid-High Water"))

        self.collect([
            self.get_item_by_name("Purple Switches"),
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

        self.collect(self.get_item_by_name("Purple Switches"))
        self.assertFalse(self.can_reach_region("Wet-Dry World - Top"))

        self.collect(self.get_item_by_name("Long Jump"))
        self.assertTrue(self.can_reach_region("Wet-Dry World - Top"))


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
        **SHUFFLED_ARBITRARY_FEATURE_OPTIONS,
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
        self.assertTrue(self.can_reach_location("Tower of the Wing Cap Red Coins"))

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

    def test_timed_jumps_require_moving_ttc_or_wall_kick(self):
        self.use_stopped_ttc_without_entry_move()
        self.collect_third_floor_access()
        self.collect([
            self.get_item_by_name("Tick Tock Clock - Spinners"),
            self.get_item_by_name("Climb"),
        ])
        self.assertTrue(self.can_reach_region("Tick Tock Clock - Upper"))
        self.assertFalse(self.can_reach_location("Tick Tock Clock - Timed Jumps on Moving Bars"))
        self.collect(self.get_item_by_name("Wall Kick"))
        self.assertTrue(self.can_reach_location("Tick Tock Clock - Timed Jumps on Moving Bars"))

    def test_timed_jumps_reachable_in_moving_ttc_without_wall_kick(self):
        self.collect_third_floor_access()
        self.collect([
            self.get_item_by_name("Side Flip"),
            self.get_item_by_name("Climb"),
        ])
        self.assertTrue(self.can_reach_region("Tick Tock Clock Moving"))
        self.assertTrue(self.can_reach_region("Tick Tock Clock - Upper"))
        self.assertTrue(self.can_reach_location("Tick Tock Clock - Timed Jumps on Moving Bars"))

    def test_midway_1up_requires_spinners_or_long_jump_and_ledge_grab(self):
        self.collect_third_floor_access()
        self.collect([
            self.get_item_by_name("Triple Jump"),
            self.get_item_by_name("Ledge Grab"),
            self.get_item_by_name("Climb"),
        ])
        self.assertTrue(self.can_reach_region("Tick Tock Clock - Top"))
        self.assertFalse(self.can_reach_location("Tick Tock Clock - 1Up Block Midway Up"))
        self.collect(self.get_item_by_name("Long Jump"))
        self.assertTrue(self.can_reach_location("Tick Tock Clock - 1Up Block Midway Up"))

    def test_midway_1up_reachable_with_spinners(self):
        self.collect_third_floor_access()
        self.collect([
            self.get_item_by_name("Triple Jump"),
            self.get_item_by_name("Ledge Grab"),
            self.get_item_by_name("Climb"),
            self.get_item_by_name("Tick Tock Clock - Spinners"),
        ])
        self.assertTrue(self.can_reach_location("Tick Tock Clock - 1Up Block Midway Up"))


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
            self.get_item_by_name("Cannon Unlock Rainbow Ride"),
        ])
        self.assertTrue(self.can_reach_location("Rainbow Ride - Coins Star"))
