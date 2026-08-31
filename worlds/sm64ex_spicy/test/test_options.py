import unittest

from .bases import SM64TestBase
from BaseClasses import CollectionState, ItemClassification
from .. import Options
from ..Items import arbitrary_item_data_table, cap_item_data_table, castle_key_item_data_table, \
    castle_progression_item_data_table, feature_item_data_table, generic_item_data_table, global_cap_item_names, \
    simple_arbitrary_item_data_table, global_arbitrary_item_data_table, checkerboard_item_data_table, \
    rolling_log_item_data_table, purple_switch_item_data_table, optional_item_data_table, item_table, item_data_table, \
    bowser_stage_1up_item_data_table, per_level_action_item_data_table, main_course_move_area_names, \
    separate_misc_move_area_names, collapsed_misc_move_area_names, non_climb_move_area_names, \
    cannon_item_data_table, painting_unlock_item_data_table, item_name_groups, \
    global_coin_object_item_data_table, per_level_coin_object_item_data_table, \
    global_enemy_item_data_table, per_level_enemy_item_data_table, global_mode_coin_object_item_names, \
    global_mode_enemy_item_names, bowser_bomb_item_data_table, special_level_unlock_item_names, \
    global_one_up_unlock_item_data_table, per_level_one_up_unlock_item_data_table, \
    global_sign_unlock_item_data_table, per_level_sign_unlock_item_data_table, \
    global_checkerboard_item_names, global_rolling_log_item_names, global_purple_switch_item_names, \
    global_bobomb_buddy_item_names, global_treasure_chest_item_names, global_warp_pipe_item_names, \
    per_level_bobomb_buddy_item_names, per_level_treasure_chest_item_names, per_level_warp_pipe_item_names, \
    global_vertical_wind_item_names, global_horizontal_wind_item_names, vertical_wind_item_data_table, \
    horizontal_wind_item_data_table, global_freestanding_star_item_names, global_star_block_item_names, \
    global_koopa_shell_block_item_names, global_star_secret_item_names, global_jet_stream_item_names, \
    freestanding_star_item_data_table, star_block_item_data_table, koopa_shell_block_item_data_table, \
    star_secret_item_data_table, jet_stream_item_data_table
from ..Locations import coin_count_check_course_data, loc100Coin_table, locOneUp_table, locBlocksanity_table, location_table, \
    coin_count_check_location_table, secret_stage_coin_count_check_location_table, get_coin_count_check_location_name, \
    location_name_groups
from ..Music import SM64_MUSIC_AREA_SEQUENCES, SM64_MUSIC_SAFE_SEQUENCE_IDS
from ..LogicTricks import get_enabled_logic_tricks, logic_tricks, logic_trick_option_keys
from ..Regions import SM64_TTC_FAST, SM64_TTC_RANDOM, SM64_TTC_SLOW, SM64_TTC_STOPPED, SM64_WDW_HIGH, \
    SM64_WDW_LOW, SM64_WDW_MIDDLE, sm64_entrances_to_level, sm64_level_to_paintings, sm64_level_to_secrets


def world_has_two_reachable_starting_checks(test_base: SM64TestBase) -> bool:
    state = CollectionState(test_base.multiworld)
    return sum(
        location.address is not None and location.can_reach(state)
        for location in test_base.multiworld.get_locations(test_base.player)
    ) >= 2

wdw_variant_ids = {SM64_WDW_LOW, SM64_WDW_MIDDLE, SM64_WDW_HIGH}
ttc_variant_ids = {SM64_TTC_STOPPED, SM64_TTC_SLOW, SM64_TTC_RANDOM, SM64_TTC_FAST}


class LogicTrickOptionTest(unittest.TestCase):
    def test_presets_are_first_in_option_keys(self):
        self.assertEqual(logic_trick_option_keys[:3], (
            "All Easy Tricks",
            "All Medium Tricks",
            "All Hard Tricks",
        ))

    def test_difficulty_presets_include_lower_difficulties(self):
        for preset, maximum_difficulty in (("All Easy Tricks", "easy"),
                                           ("All Medium Tricks", "medium"),
                                           ("All Hard Tricks", "hard")):
            enabled = get_enabled_logic_tricks({preset})
            expected = {
                trick for trick, data in logic_tricks.items()
                if ("easy", "medium", "hard").index(data["difficulty"])
                <= ("easy", "medium", "hard").index(maximum_difficulty)
            }
            self.assertEqual(enabled, expected)


class MipsSkipSlotDataDisabledTestBase(SM64TestBase):
    run_default_tests = False

    def test_mips_skip_slot_data_is_disabled(self):
        self.assertFalse(self.world.fill_slot_data()["MipsSkipEnabled"])


class MipsSkipSlotDataEnabledTestBase(SM64TestBase):
    run_default_tests = False
    options = {"logic_tricks": {"Castle MIPS Skip Through the 30 Star Door"}}

    def test_mips_skip_slot_data_is_enabled(self):
        self.assertTrue(self.world.fill_slot_data()["MipsSkipEnabled"])


class BowserStageCollapseHitsOptionTest(unittest.TestCase):
    def test_range(self):
        self.assertEqual(Options.BowserInTheSkyStageCollapseHits.range_start, 1)
        self.assertEqual(Options.BowserInTheSkyStageCollapseHits.range_end, 5)


UNCOLLECT_TRAP_ONLY_OPTIONS = {
    "traps_filler_percentage": 100,
    "bonk_trap_weight": 0,
    "fire_trap_weight": 0,
    "electric_trap_weight": 0,
    "chuckya_trap_weight": 0,
    "spin_trap_weight": 0,
    "gust_trap_weight": 0,
    "uncollect_random_coin_trap_weight": 100,
}


class UncollectTrapTestBase(SM64TestBase):
    options = UNCOLLECT_TRAP_ONLY_OPTIONS

    def test_uncollect_trap_weight_is_used(self):
        self.assertGreater(len(self.get_items_by_name("Uncollect Random Coin Trap")), 0)


class PerLevelOptionAliasTest(unittest.TestCase):
    def test_individual_aliases_per_level(self):
        option_classes = (
            Options.CoinObjectUnlocks,
            Options.EnemyUnlocks,
            Options.OneUpUnlocks,
            Options.SignUnlocks,
            Options.BowserBombs,
            Options.BowserStage1Ups,
            Options.TripleJump,
        )
        for option_class in option_classes:
            with self.subTest(option=option_class.__name__):
                self.assertEqual(option_class.from_text("per_level").value, option_class.option_per_level)
                self.assertEqual(option_class.from_text("individual").value, option_class.option_per_level)

    def test_both_is_available(self):
        option_classes = (
            Options.LevelFeatures,
            Options.BobombBuddies,
            Options.CoinObjectUnlocks,
            Options.EnemyUnlocks,
            Options.OneUpUnlocks,
            Options.SignUnlocks,
            Options.BowserBombs,
            Options.BowserStage1Ups,
            Options.CapItems,
            *Options.move_randomizer_options,
        )
        for option_class in option_classes:
            with self.subTest(option=option_class.__name__):
                self.assertEqual(option_class.from_text("both").value, option_class.option_both)


class LevelUnlockOptionTest(unittest.TestCase):
    def test_legacy_boolean_aliases(self):
        self.assertEqual(Options.LevelUnlocks.from_any(False).value, Options.LevelUnlocks.option_special_only)
        self.assertEqual(Options.LevelUnlocks.from_any(True).value, Options.LevelUnlocks.option_full)


class CapItemOptionTest(unittest.TestCase):
    def test_legacy_boolean_aliases(self):
        self.assertEqual(
            Options.CapItems.from_any(False).value,
            Options.CapItems.option_global,
        )
        self.assertEqual(
            Options.CapItems.from_any(True).value,
            Options.CapItems.option_per_level,
        )


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

SINGLE_BLOCKSANITY_CHECK_CAP_ITEMS = (
    "Castle - Wing Cap",
    "Tower of the Wing Cap - Wing Cap",
    "Whomp's Fortress - Metal Cap",
    "Wet-Dry World - Metal Cap",
    "Bowser in the Dark World - Metal Cap",
)


class FeatureItemPoolTestBase(SM64TestBase):
    def get_item_data_classification(self, item_data):
        return self.world.get_item_classification(item_data)

    def test_yoshi_location_id(self):
        self.assertEqual(location_table["Castle - Yoshi"], 3626244)

    def test_drain_the_moat_location_id(self):
        self.assertEqual(location_table["Castle - Drain the Moat"], 3626245)

    def test_wmotr_bob_omb_buddy_location_id(self):
        self.assertEqual(location_table["Wing Mario Over the Rainbow - Bob-omb Buddy"], 3626525)

    def test_monty_mole_location_ids(self):
        expected_ids = {
            "Hazy Maze Cave - Blue Coin Trail Monty Moles": 3629189,
            "Tall, Tall Mountain - Upper Monty Moles": 3629190,
            "Hazy Maze Cave - Twin Hole Monty Moles": 3629191,
            "Tall, Tall Mountain - Lower Monty Moles": 3629192,
        }
        for location_name, location_id in expected_ids.items():
            with self.subTest(location=location_name):
                self.assertEqual(location_table[location_name], location_id)

    def test_blocksanity_location_ids(self):
        expected_ids = {
            "Big Boo's Haunt - Back Entrance Vanish Cap Block": 3629758,
            "The Princess's Secret Slide - Star Block": 3629800,
            "Tower of the Wing Cap - Wing Cap Block": 3629823,
            "Wet-Dry World - Downtown 1-Up Block": 3629852,
            "Wing Mario Over the Rainbow - Overlooking Bob-omb Buddy Cloud Wing Cap Block": 3629860,
        }
        self.assertEqual(len(locBlocksanity_table), 103)
        self.assertEqual(set(range(3629758, 3629861)), set(locBlocksanity_table.values()))
        for location_name, location_id in expected_ids.items():
            with self.subTest(location=location_name):
                self.assertEqual(location_table[location_name], location_id)

    def test_wmotr_cannon_unlock_item_id(self):
        self.assertEqual(cannon_item_data_table["Wing Mario Over the Rainbow - Cannon Unlock"].code, 3626525)

    def test_uncollect_random_coin_trap_item_id(self):
        self.assertEqual(item_table["Uncollect Random Coin Trap"], 3627766)

    def test_item_name_groups(self):
        for group_name, group_items in item_name_groups.items():
            with self.subTest(group=group_name):
                self.assertLessEqual(group_items, set(item_table))

        self.assertIn("Wing Cap", self.world.item_name_groups["Caps"])
        self.assertIn("Bob-omb Battlefield - Cannon Unlock", self.world.item_name_groups["Cannon Unlocks"])
        self.assertIn("Bob-omb Battlefield - Triple Jump", self.world.item_name_groups["Per-Level Moves"])
        self.assertIn("Castle - Yoshi", self.world.item_name_groups["Castle Unlocks"])
        self.assertIn("Tiny-Huge Island - Purple Switch", self.world.item_name_groups["Per-Level Purple Switches"])

    def test_location_name_groups(self):
        for group_name, group_locations in location_name_groups.items():
            with self.subTest(group=group_name):
                self.assertLessEqual(group_locations, set(location_table))

        self.assertIn("Bob-omb Battlefield - Big Bob-Omb on the Summit",
                      self.world.location_name_groups["Bob-omb Battlefield"])
        self.assertIn("Wing Mario Over the Rainbow - Red Coins",
                      self.world.location_name_groups["Secret Stages"])
        self.assertIn("Wet-Dry World - Downtown 1-Up Block",
                      self.world.location_name_groups["Blocksanity"])
        self.assertIn("Wet-Dry World - Downtown Block 1-Up",
                      self.world.location_name_groups["1-Ups"])
        self.assertIn("Wet-Dry World - Downtown 1-Up Block",
                      self.world.location_name_groups["1-Up Blocks"])
        self.assertIn("The Princess's Secret Slide - 1 Coin",
                      self.world.location_name_groups["Secret Stage Coin Count Checks"])

    def test_item_ids_match_client_doc(self):
        expected_ids = {
            "Bob-omb Battlefield - King Bob-omb": 3626245,
            "Bob-omb Battlefield - Koopa the Quick": 3626246,
            "Bob-omb Battlefield - Bob-omb Buddy": 3626247,
            "Whomp's Fortress - Whomp King": 3626248,
            "Whomp's Fortress - Fortress": 3626249,
            "Whomp's Fortress - Bob-omb Buddy": 3626250,
            "Whomp's Fortress - Hoot": 3626251,
            "Cool, Cool Mountain - Snowman's Body": 3626252,
            "Cool, Cool Mountain - Big Penguin": 3626253,
            "Jolly Roger Bay - Sunken Ship": 3626254,
            "Jolly Roger Bay - Raised Ship": 3626255,
            "Jolly Roger Bay - Bob-omb Buddy": 3626256,
            "Jolly Roger Bay - Jet Stream": 3626257,
            "Jolly Roger Bay - Unagi": 3626258,
            "Lethal Lava Land - Koopa Shell": 3626259,
            "Shifting Sand Land - Klepto with Star": 3626260,
            "Tiny-Huge Island - Koopa the Quick": 3626261,
            "Tall, Tall Mountain - Ukiki": 3626262,
            "Dire, Dire Docks - Manta Ray": 3626263,
            "Dire, Dire Docks - Bowser's Sub": 3626264,
            "Dire, Dire Docks - Poles": 3626265,
            "Big Boo's Haunt - Staircase": 3626266,
            "Big Boo's Haunt - Merry-go-round": 3626267,
            "Dark World Key": 3626268,
            "Progressive Basement Key": 3626269,
            "Progressive Upstairs Key": 3626270,
            "Castle - Progressive MIPS": 3626271,
            "Unlock Tower of the Wing Cap": 3626272,
            "Unlock Big Boo's Haunt": 3626273,
            "Castle - Toads": 3626274,
            "Castle - Cannon Unlock": 3626275,
            "Castle - Yoshi": 3626276,
            "Unlock Bowser in the Fire Sea": 3626304,
            "Unlock Vanish Cap Under the Moat": 3626555,
            "Unlock Bob-omb Battlefield": 3626230,
            "Unlock Whomp's Fortress": 3626231,
            "Unlock Jolly Roger Bay": 3626232,
            "Unlock Cool, Cool Mountain": 3626233,
            "Unlock Hazy Maze Cave": 3626235,
            "Unlock Lethal Lava Land": 3626236,
            "Unlock Shifting Sand Land": 3626237,
            "Unlock Dire, Dire Docks": 3626238,
            "Unlock Snowman's Land": 3626239,
            "Unlock Wet-Dry World": 3626240,
            "Unlock Tall, Tall Mountain": 3626241,
            "Unlock Tiny Island": 3626242,
            "Unlock Tick Tock Clock": 3626243,
            "Unlock Huge Island": 3626559,
            "Wing Cap": 3626181,
            "Metal Cap": 3626182,
            "Vanish Cap": 3626183,
            "Bob-omb Battlefield - Wing Cap": 3626277,
            "Castle - Wing Cap": 3626278,
            "Lethal Lava Land - Wing Cap": 3626279,
            "Shifting Sand Land - Wing Cap": 3626280,
            "Tower of the Wing Cap - Wing Cap": 3626281,
            "Wing Mario Over the Rainbow - Wing Cap": 3626282,
            "Whomp's Fortress - Metal Cap": 3626283,
            "Jolly Roger Bay - Metal Cap": 3626284,
            "Hazy Maze Cave - Metal Cap": 3626285,
            "Dire, Dire Docks - Metal Cap": 3626286,
            "Wet-Dry World - Metal Cap": 3626287,
            "Cavern of the Metal Cap - Metal Cap": 3626288,
            "Bowser in the Dark World - Metal Cap": 3626289,
            "Big Boo's Haunt - Vanish Cap": 3626290,
            "Dire, Dire Docks - Vanish Cap": 3626291,
            "Snowman's Land - Vanish Cap": 3626292,
            "Vanish Cap Under the Moat - Vanish Cap": 3626293,
            "Wet-Dry World - Vanish Cap": 3626294,
            "Hazy Maze Cave - Swimming Beast": 3626295,
            "Rainbow Ride - Carpets": 3626296,
            "Checkerboard Platforms": 3626297,
            "Tiny-Huge Island - Warp Pipes": 3626298,
            "Cool, Cool Mountain - Baby Penguins": 3626299,
            "Snowman's Land - Penguin": 3626300,
            "Shifting Sand Land - Pyramid Elevator": 3626301,
            "Rolling Logs": 3626302,
            "Purple Switches": 3626303,
            "Wet-Dry World - Water Level Diamond": 3626305,
            "Bob-omb Battlefield - Checkerboard Platform": 3626306,
            "Whomp's Fortress - Checkerboard Platform": 3626307,
            "Lethal Lava Land - Checkerboard Platforms": 3626308,
            "Hazy Maze Cave - Checkerboard Platform": 3626309,
            "Vanish Cap Under the Moat - Checkerboard Platforms": 3626310,
            "Lethal Lava Land - Rolling Log": 3626311,
            "Tall, Tall Mountain - Rolling Log": 3626312,
            "Bob-omb Battlefield - Purple Switch": 3626313,
            "Hazy Maze Cave - Purple Switch": 3626314,
            "Wet-Dry World - Purple Switch": 3626315,
            "Rainbow Ride - Purple Switch": 3626316,
            "Bowser in the Dark World - Purple Switch": 3626317,
            "Bowser in the Sky - Purple Switch": 3626318,
            "Tick Tock Clock - Spinners": 3626319,
            "Mario's Hat": 3626320,
            "Jolly Roger Bay - Purple Switch": 3626321,
            "Dire, Dire Docks - Purple Switch": 3626322,
            "Tall, Tall Mountain - Purple Switch": 3626323,
            "Tiny-Huge Island - Purple Switch": 3626324,
            "Bowser Stage Extra 1-Ups": 3626556,
            "Bowser in the Dark World - Extra 1-Ups": 3626557,
            "Bowser in the Fire Sea - Extra 1-Ups": 3626558,
            "Cool, Cool Mountain - Bob-omb Buddy": 3626920,
            "Shifting Sand Land - Bob-omb Buddy": 3626921,
            "Snowman's Land - Bob-omb Buddy": 3626922,
            "Wet-Dry World - Bob-omb Buddy": 3626923,
            "Tall, Tall Mountain - Bob-omb Buddy": 3626924,
            "Tiny-Huge Island - Bob-omb Buddy": 3626925,
            "Rainbow Ride - Bob-omb Buddy": 3626926,
            "Wing Mario Over the Rainbow - Bob-omb Buddy": 3626927,
            "Bob-omb Buddies": 3626928,
            "Jolly Roger Bay - Treasure Chests": 3626929,
            "Dire, Dire Docks - Treasure Chests": 3626930,
            "Treasure Chests": 3626931,
            "Bowser in the Dark World - Warp Pipes": 3626932,
            "Bowser in the Sky - Warp Pipes": 3626934,
            "Warp Pipes": 3626935,
            "Signs": 3626939,
            "Castle - Signs": 3626940,
            "Bob-omb Battlefield - Signs": 3626941,
            "Whomp's Fortress - Signs": 3626942,
            "Jolly Roger Bay - Signs": 3626943,
            "Cool, Cool Mountain - Signs": 3626944,
            "Big Boo's Haunt - Signs": 3626945,
            "Hazy Maze Cave - Signs": 3626946,
            "Lethal Lava Land - Signs": 3626947,
            "Shifting Sand Land - Signs": 3626948,
            "Dire, Dire Docks - Signs": 3626949,
            "Snowman's Land - Signs": 3626950,
            "Wet-Dry World - Signs": 3626951,
            "Tall, Tall Mountain - Signs": 3626952,
            "Tiny-Huge Island - Signs": 3626953,
            "The Princess's Secret Slide - Signs": 3626954,
            "Cavern of the Metal Cap - Signs": 3626955,
            "Bowser in the Dark World - Signs": 3626956,
            "Vertical Wind": 3627102,
            "Cool, Cool Mountain - Vertical Wind": 3627103,
            "Tall, Tall Mountain - Vertical Wind": 3627104,
            "Tiny-Huge Island - Vertical Wind": 3627105,
            "Horizontal Wind": 3627106,
            "Bowser in the Sky - Horizontal Wind": 3627107,
            "Rainbow Ride - Horizontal Wind": 3627108,
            "Snowman's Land - Horizontal Wind": 3627109,
            "Tiny-Huge Island - Horizontal Wind": 3627110,
            "Dire, Dire Docks - Moat Exit": 3627114,
            "Freestanding Stars": 3627115,
            "Star Blocks": 3627116,
            "Koopa Shell Blocks": 3627117,
            "Star Secrets": 3627118,
            "Bob-omb Battlefield - Freestanding Star": 3627119,
            "Whomp's Fortress - Freestanding Stars": 3627120,
            "Jolly Roger Bay - Freestanding Stars": 3627121,
            "Cool, Cool Mountain - Freestanding Star": 3627122,
            "Big Boo's Haunt - Freestanding Star": 3627123,
            "Hazy Maze Cave - Freestanding Stars": 3627124,
            "Lethal Lava Land - Freestanding Stars": 3627125,
            "Shifting Sand Land - Freestanding Stars": 3627126,
            "Dire, Dire Docks - Freestanding Stars": 3627127,
            "Snowman's Land - Freestanding Stars": 3627128,
            "Wet-Dry World - Freestanding Stars": 3627129,
            "Tall, Tall Mountain - Freestanding Stars": 3627130,
            "Tick Tock Clock - Freestanding Stars": 3627131,
            "Rainbow Ride - Freestanding Stars": 3627132,
            "Bob-omb Battlefield - Star Block": 3627133,
            "Jolly Roger Bay - Star Blocks": 3627134,
            "The Princess's Secret Slide - Star Block": 3627135,
            "Rainbow Ride - Star Block": 3627136,
            "Snowman's Land - Star Block": 3627137,
            "Tiny-Huge Island - Star Block": 3627138,
            "Wet-Dry World - Star Blocks": 3627139,
            "Shifting Sand Land - Koopa Shell Block": 3627140,
            "Snowman's Land - Koopa Shell Block": 3627141,
            "Bob-omb Battlefield - Star Secrets": 3627142,
            "Shifting Sand Land - Star Secrets": 3627143,
            "Wet-Dry World - Star Secrets": 3627144,
            "Tiny-Huge Island - Star Secrets": 3627145,
            "Dire, Dire Docks - Jet Stream": 3627146,
            "Jet Streams": 3627147,
        }
        item_data = {
            **feature_item_data_table,
            **castle_key_item_data_table,
            **castle_progression_item_data_table,
            **cap_item_data_table,
            **arbitrary_item_data_table,
            **optional_item_data_table,
            **bowser_stage_1up_item_data_table,
            **global_sign_unlock_item_data_table,
            **per_level_sign_unlock_item_data_table,
            **{
                item_name: item_data
                for item_name, item_data in painting_unlock_item_data_table.items()
                if item_data.code < 3626853
            },
            **{item_name: generic_item_data_table[item_name] for item_name in global_cap_item_names},
        }
        self.assertEqual({name: data.code for name, data in item_data.items()}, expected_ids)

    def test_per_level_move_item_ids_match_client_table(self):
        self.assertEqual(len(per_level_action_item_data_table), 240)
        self.assertEqual(item_table["Bob-omb Battlefield - Triple Jump"], 3626325)
        self.assertEqual(item_table["Bob-omb Battlefield - Ledge Grab"], 3626334)
        self.assertEqual(item_table["Whomp's Fortress - Triple Jump"], 3626335)
        self.assertEqual(item_table["Castle - Triple Jump"], 3626475)
        self.assertEqual(item_table["Castle - Ledge Grab"], 3626484)
        self.assertEqual(item_table["Bowser in the Dark World - Triple Jump"], 3627022)
        self.assertEqual(item_table["Wing Mario Over the Rainbow - Ledge Grab"], 3627091)
        self.assertEqual(item_table["Misc - Triple Jump"], 3627092)
        self.assertEqual(item_table["Misc - Ledge Grab"], 3627101)

    def test_wind_item_classifications(self):
        expected = {
            "Vertical Wind": ItemClassification.progression,
            "Cool, Cool Mountain - Vertical Wind": ItemClassification.useful,
            "Tall, Tall Mountain - Vertical Wind": ItemClassification.progression,
            "Tiny-Huge Island - Vertical Wind": ItemClassification.progression,
            "Horizontal Wind": ItemClassification.trap,
            "Bowser in the Sky - Horizontal Wind": ItemClassification.trap,
            "Rainbow Ride - Horizontal Wind": ItemClassification.trap,
            "Snowman's Land - Horizontal Wind": ItemClassification.trap,
            "Tiny-Huge Island - Horizontal Wind": ItemClassification.trap,
        }
        for item_name, classification in expected.items():
            with self.subTest(item=item_name):
                self.assertEqual(
                    self.get_item_data_classification(item_data_table[item_name]),
                    classification)

    def test_current_per_level_move_item_classifications(self):
        expected_classifications = {
            "Bob-omb Battlefield - Dive": ItemClassification.useful,
            "Castle - Ground Pound": ItemClassification.progression,
            "Castle - Triple Jump": ItemClassification.progression,
            "Castle - Kick": ItemClassification.filler,
            "Castle - Climb": ItemClassification.progression,
            "Dire, Dire Docks - Wall Kick": ItemClassification.filler,
            "Dire, Dire Docks - Dive": ItemClassification.filler,
            "Dire, Dire Docks - Ledge Grab": ItemClassification.filler,
            "Tiny-Huge Island - Backflip": ItemClassification.filler,
            "Tiny-Huge Island - Kick": ItemClassification.filler,
        }
        for item_name, classification in expected_classifications.items():
            with self.subTest("Per-level move item classification", item=item_name):
                self.assertEqual(
                    self.get_item_data_classification(per_level_action_item_data_table[item_name]), classification)

    def test_one_check_per_level_move_items_skip_balancing(self):
        for item_name in (
                "Bob-omb Battlefield - Ground Pound",
                "Cool, Cool Mountain - Triple Jump",
                "Jolly Roger Bay - Long Jump",
                "Snowman's Land - Climb",
                "Wet-Dry World - Kick",
                "Tick Tock Clock - Ground Pound",
        ):
            with self.subTest("One-check per-level move item skips balancing", item=item_name):
                self.assertEqual(
                    self.get_item_data_classification(per_level_action_item_data_table[item_name]),
                    ItemClassification.progression_deprioritized_skip_balancing)

    def test_multi_check_per_level_move_items_are_progression(self):
        for item_name in (
                "Bob-omb Battlefield - Triple Jump",
                "Whomp's Fortress - Wall Kick",
                "Castle - Dive",
                "Castle - Triple Jump",
        ):
            with self.subTest("Multi-check per-level move item is progression", item=item_name):
                self.assertEqual(
                    self.get_item_data_classification(per_level_action_item_data_table[item_name]),
                    ItemClassification.progression)

    def test_feature_items_are_generated(self):
        for item_name in feature_item_data_table:
            if (
                    item_name in per_level_bobomb_buddy_item_names
            ):
                continue
            with self.subTest("Feature item generated", item=item_name):
                self.assertEqual(len(self.get_items_by_name(item_name)), 1)

    def test_default_arbitrary_items_are_not_generated(self):
        for item_name in {
                **simple_arbitrary_item_data_table,
                **global_arbitrary_item_data_table,
        }:
            with self.subTest("Default arbitrary item not generated", item=item_name):
                self.assertEqual(len(self.get_items_by_name(item_name)), 0)

    def test_default_arbitrary_items_are_start_inventory_slot_data_only(self):
        start_inventory = self.world.fill_slot_data()["StartInventory"]
        precollected_names = {item.name for item in self.multiworld.precollected_items[self.player]}
        for item_name in {
                **simple_arbitrary_item_data_table,
                **global_arbitrary_item_data_table,
        }:
            if item_name in {
                    "Bob-omb Buddies",
                    "Jolly Roger Bay - Treasure Chests",
                    "Dire, Dire Docks - Treasure Chests",
                    *global_koopa_shell_block_item_names,
                    *global_jet_stream_item_names,
                    *per_level_warp_pipe_item_names,
            }:
                continue
            with self.subTest("Default arbitrary item in StartInventory only", item=item_name):
                self.assertEqual(start_inventory[item_table[item_name]], 1)
                self.assertNotIn(item_name, precollected_names)

        for item_name in per_level_bobomb_buddy_item_names:
            if item_name in feature_item_data_table:
                continue
            with self.subTest("Non-act buddy in StartInventory", item=item_name):
                self.assertEqual(start_inventory[item_table[item_name]], 1)

        for item_name in (*koopa_shell_block_item_data_table, *jet_stream_item_data_table):
            if item_name in {"Lethal Lava Land - Koopa Shell", "Jolly Roger Bay - Jet Stream"}:
                continue
            with self.subTest("Non-act level feature in StartInventory", item=item_name):
                self.assertEqual(start_inventory[item_table[item_name]], 1)

    def test_precollected_items_are_only_added_to_apsm64ex_start_inventory(self):
        self.multiworld.push_precollected(self.world.create_item("Dark World Key"))
        item_id = item_table["Dark World Key"]
        self.assertNotIn(item_id, self.world.fill_slot_data()["StartInventory"])
        self.assertEqual(self.world.get_apsm64ex_slot_data()["StartInventory"][item_id], 1)

    def test_default_individual_arbitrary_items_are_not_generated(self):
        for item_name in {
                **checkerboard_item_data_table,
                **rolling_log_item_data_table,
                **purple_switch_item_data_table,
                **{name: None for name in per_level_warp_pipe_item_names},
        }:
            with self.subTest("Individual arbitrary item not generated", item=item_name):
                self.assertEqual(len(self.get_items_by_name(item_name)), 0)

    def test_unused_individual_arbitrary_items_are_filler(self):
        for item_name in (
                "Bob-omb Battlefield - Checkerboard Platform",
                "Bob-omb Battlefield - Purple Switch",
        ):
            with self.subTest("Unused individual arbitrary item is filler", item=item_name):
                self.assertEqual(
                    self.get_item_data_classification(arbitrary_item_data_table[item_name]),
                    ItemClassification.filler)

    def test_castle_progression_items_are_generated(self):
        self.assertEqual(len(self.get_items_by_name("Progressive Key")), 6)
        self.assertEqual(len(self.get_items_by_name("Castle - Progressive MIPS")), 2)
        for item_name in castle_progression_item_data_table:
            if item_name != "Castle - Progressive MIPS":
                with self.subTest("Castle progression item generated", item=item_name):
                    self.assertEqual(len(self.get_items_by_name(item_name)), 1)

    def test_default_global_cap_items_are_generated(self):
        self.assertTrue(self.world.fill_slot_data()["GlobalCapItems"])
        for item_name in global_cap_item_names:
            with self.subTest("Global cap item generated", item=item_name):
                self.assertEqual(len(self.get_items_by_name(item_name)), 1)

    def test_default_cap_items_are_not_generated(self):
        for item_name in cap_item_data_table:
            with self.subTest("Per-level cap item not generated", item=item_name):
                self.assertEqual(len(self.get_items_by_name(item_name)), 0)

    def test_default_move_items_are_not_generated(self):
        self.assertEqual(self.world.fill_slot_data()["MoveRandoVec"], 0)
        self.assertEqual(len(self.get_items_by_name("Triple Jump")), 0)
        self.assertEqual(len(self.get_items_by_name("Bob-omb Battlefield - Triple Jump")), 0)

    def test_old_keys_are_not_generated(self):
        self.assertEqual(len(self.get_items_by_name("Basement Key")), 0)
        self.assertEqual(len(self.get_items_by_name("Second Floor Key")), 0)

    def test_marios_hat_defaults_to_start_inventory_slot_data_only(self):
        start_inventory = self.world.fill_slot_data()["StartInventory"]
        precollected_names = {item.name for item in self.multiworld.precollected_items[self.player]}
        self.assertEqual(len(self.get_items_by_name("Mario's Hat")), 0)
        self.assertEqual(start_inventory[item_table["Mario's Hat"]], 1)
        self.assertNotIn("Mario's Hat", precollected_names)

    def test_marios_hat_is_useful(self):
        self.assertEqual(
            self.get_item_data_classification(optional_item_data_table["Mario's Hat"]),
            ItemClassification.useful)

    def test_one_up_checks_default_to_off(self):
        active_locations = {location.name for location in self.multiworld.get_locations(self.player)}
        self.assertEqual(self.world.fill_slot_data()["OneUpChecks"], 0)
        self.assertTrue(set(locOneUp_table).isdisjoint(active_locations))

    def test_blocksanity_defaults_to_off(self):
        active_locations = {location.name for location in self.multiworld.get_locations(self.player)}
        slot_data = self.world.fill_slot_data()
        self.assertEqual(slot_data["Options"]["blocksanity"], 0)
        self.assertNotIn("Blocksanity", slot_data)
        self.assertTrue(set(locBlocksanity_table).isdisjoint(active_locations))

    def test_buddy_checks_default_to_events(self):
        location = self.multiworld.get_location("Bob-omb Battlefield - Bob-omb Buddy", self.player)
        self.assertEqual(self.world.fill_slot_data()["BuddyChecks"], 0)
        self.assertIsNone(location.address)
        self.assertEqual(location.item.name, "Bob-omb Battlefield - Cannon Unlock")
        self.assertIsNone(location.item.code)

    def test_bowser_stage_1up_items_default_to_vanilla_behavior(self):
        self.assertFalse(self.world.fill_slot_data()["BowserStage1UpBehavior"])
        for item_name in bowser_stage_1up_item_data_table:
            with self.subTest("Bowser stage 1-Up item not generated by default", item=item_name):
                self.assertEqual(len(self.get_items_by_name(item_name)), 0)
                self.assertNotIn(item_table[item_name], self.world.fill_slot_data()["StartInventory"])


class GlobalBowserStage1UpsItemPoolTestBase(SM64TestBase):
    options = {
        "bowser_stage_1ups": Options.BowserStage1Ups.option_global,
    }

    def test_global_bowser_stage_1up_item_is_generated(self):
        self.assertTrue(self.world.fill_slot_data()["BowserStage1UpBehavior"])
        self.assertEqual(len(self.get_items_by_name("Bowser Stage Extra 1-Ups")), 1)
        self.assertEqual(len(self.get_items_by_name("Bowser in the Dark World - Extra 1-Ups")), 0)
        self.assertEqual(len(self.get_items_by_name("Bowser in the Fire Sea - Extra 1-Ups")), 0)
        self.assertNotIn(item_table["Bowser Stage Extra 1-Ups"], self.world.fill_slot_data()["StartInventory"])


class IndividualBowserStage1UpsItemPoolTestBase(SM64TestBase):
    options = {
        "bowser_stage_1ups": Options.BowserStage1Ups.option_per_level,
    }

    def test_individual_bowser_stage_1up_items_are_generated(self):
        self.assertTrue(self.world.fill_slot_data()["BowserStage1UpBehavior"])
        self.assertEqual(len(self.get_items_by_name("Bowser Stage Extra 1-Ups")), 0)
        self.assertEqual(len(self.get_items_by_name("Bowser in the Dark World - Extra 1-Ups")), 1)
        self.assertEqual(len(self.get_items_by_name("Bowser in the Fire Sea - Extra 1-Ups")), 1)


class BothBowserStage1UpsItemPoolTestBase(SM64TestBase):
    options = {
        "bowser_stage_1ups": Options.BowserStage1Ups.option_both,
    }

    def test_both_bowser_stage_1up_item_forms_are_generated(self):
        for item_name in bowser_stage_1up_item_data_table:
            self.assertEqual(len(self.get_items_by_name(item_name)), 1)


class AlwaysSpawnBowserStage1UpsItemPoolTestBase(SM64TestBase):
    options = {
        "bowser_stage_1ups": Options.BowserStage1Ups.option_always_spawn,
    }

    def test_bowser_stage_1ups_start_unlocked(self):
        start_inventory = self.world.fill_slot_data()["StartInventory"]
        self.assertTrue(self.world.fill_slot_data()["BowserStage1UpBehavior"])
        self.assertEqual(len(self.get_items_by_name("Bowser Stage Extra 1-Ups")), 0)
        self.assertEqual(start_inventory[item_table["Bowser Stage Extra 1-Ups"]], 1)


class PerLevelCapItemPoolTestBase(SM64TestBase):
    options = {
        "cap_items": Options.CapItems.option_per_level,
    }

    def test_cap_items_are_generated(self):
        for item_name in cap_item_data_table:
            with self.subTest("Per-level cap item generated", item=item_name):
                self.assertEqual(len(self.get_items_by_name(item_name)), 1)

    def test_global_cap_items_are_not_generated(self):
        self.assertFalse(self.world.fill_slot_data()["GlobalCapItems"])
        for item_name in global_cap_item_names:
            with self.subTest("Global cap item not generated", item=item_name):
                self.assertEqual(len(self.get_items_by_name(item_name)), 0)


class BothCapItemPoolTestBase(SM64TestBase):
    options = {
        "cap_items": Options.CapItems.option_both,
    }

    def test_both_cap_item_forms_are_generated(self):
        self.assertTrue(self.world.fill_slot_data()["GlobalCapItems"])
        for item_name in (*global_cap_item_names, *cap_item_data_table):
            with self.subTest(item=item_name):
                self.assertEqual(len(self.get_items_by_name(item_name)), 1)

    def test_either_cap_item_form_satisfies_logic(self):
        from ..Rules import has_wing_cap

        for item_name in ("Wing Cap", "Bob-omb Battlefield - Wing Cap"):
            with self.subTest(item=item_name):
                state = CollectionState(self.multiworld)
                state.collect(self.world.create_item(item_name), True)
                self.assertTrue(has_wing_cap(state, self.player, "Bob-omb Battlefield"))

    def test_blocksanity_only_cap_items_remain_filler_without_blocksanity(self):
        for item_name in SINGLE_BLOCKSANITY_CHECK_CAP_ITEMS:
            with self.subTest("Blocksanity-only cap item remains filler", item=item_name):
                self.assertEqual(
                    self.world.get_item_classification(cap_item_data_table[item_name]),
                    ItemClassification.filler)


class BlocksanityPerLevelCapItemPoolTestBase(SM64TestBase):
    options = {
        "cap_items": Options.CapItems.option_per_level,
        "blocksanity": Options.Blocksanity.option_true,
    }

    def test_blocksanity_only_cap_items_are_progression_skip_balancing(self):
        for item_name in SINGLE_BLOCKSANITY_CHECK_CAP_ITEMS:
            with self.subTest("Blocksanity-only cap item is progression", item=item_name):
                self.assertEqual(
                    self.world.get_item_classification(cap_item_data_table[item_name]),
                    ItemClassification.progression_deprioritized_skip_balancing)
                self.assertTrue(self.get_items_by_name(item_name)[0].advancement)

    def test_all_cap_items_are_progression_with_blocksanity(self):
        for item_name in cap_item_data_table:
            with self.subTest("Per-level cap item is progression", item=item_name):
                self.assertTrue(self.get_items_by_name(item_name)[0].advancement)


class TowerOfTheWingCapCoinCountChecksCapItemPoolTestBase(SM64TestBase):
    options = {
        "cap_items": Options.CapItems.option_per_level,
        "coin_count_checks": 100,
        "tower_of_the_wing_cap_coin_count_max_coins": 63,
    }

    def test_wing_cap_is_progression_for_high_coin_checks(self):
        item_name = "Tower of the Wing Cap - Wing Cap"
        self.assertEqual(
            self.world.get_item_classification(cap_item_data_table[item_name]),
            ItemClassification.progression_deprioritized_skip_balancing)
        self.assertTrue(self.get_items_by_name(item_name)[0].advancement)

class MariosHatItemPoolTestBase(SM64TestBase):
    options = {
        "marios_hat": Options.MariosHat.option_true,
    }

    def test_marios_hat_is_generated(self):
        self.assertEqual(len(self.get_items_by_name("Mario's Hat")), 1)

    def test_marios_hat_is_not_start_inventory_when_generated(self):
        start_inventory = self.world.fill_slot_data()["StartInventory"]
        self.assertNotIn(item_table["Mario's Hat"], start_inventory)


class MariosHatLavaDamageBoostingItemPoolTestBase(SM64TestBase):
    options = {
        "logic_tricks": {"Lava Damage Boosting"},
        "marios_hat": Options.MariosHat.option_true,
    }

    def test_marios_hat_is_progression_for_lava_damage_boosting(self):
        self.assertEqual(
            self.world.get_item_classification(optional_item_data_table["Mario's Hat"]),
            ItemClassification.progression,
        )
        self.assertTrue(self.get_items_by_name("Mario's Hat")[0].advancement)


class OneUpChecksOnTestBase(SM64TestBase):
    options = {
        "one_up_checks": Options.OneUpChecks.option_true,
    }

    def test_one_up_locations_are_generated(self):
        active_locations = {location.name for location in self.multiworld.get_locations(self.player)}
        self.assertEqual(self.world.fill_slot_data()["OneUpChecks"], 1)
        for location_name in locOneUp_table:
            if location_name == "Cool, Cool Mountain - Slide Shortcut Second 1-Up":
                continue
            with self.subTest("1-Up location generated", location=location_name):
                self.assertIn(location_name, active_locations)
        self.assertNotIn("Cool, Cool Mountain - Slide Shortcut Second 1-Up", active_locations)


class OneUpChecksNoDespawnsOnTestBase(SM64TestBase):
    options = {
        "one_up_checks": Options.OneUpChecks.option_true,
        "no_despawns": Options.NoDespawns.option_true,
    }

    def test_impossible_one_up_location_is_generated_with_no_despawns(self):
        active_locations = {location.name for location in self.multiworld.get_locations(self.player)}
        self.assertIn("Cool, Cool Mountain - Slide Shortcut Second 1-Up", active_locations)


class GlobalOneUpUnlockItemPoolTestBase(SM64TestBase):
    options = {
        "one_up_checks": Options.OneUpChecks.option_true,
        "one_up_unlocks": Options.OneUpUnlocks.option_global,
    }

    def test_global_one_up_unlock_items_are_generated(self):
        self.assertNotIn("OneUpUnlockMode", self.world.fill_slot_data())
        for item_name in global_one_up_unlock_item_data_table:
            self.assertEqual(len(self.get_items_by_name(item_name)), 1)
        for item_name in per_level_one_up_unlock_item_data_table:
            self.assertEqual(len(self.get_items_by_name(item_name)), 0)
        self.assertEqual(item_table["Butterflies"], 3626919)


class PerLevelOneUpUnlockItemPoolTestBase(SM64TestBase):
    options = {
        "one_up_checks": Options.OneUpChecks.option_true,
        "one_up_unlocks": Options.OneUpUnlocks.option_per_level,
    }

    def test_per_level_one_up_unlock_items_are_generated(self):
        self.assertNotIn("OneUpUnlockMode", self.world.fill_slot_data())
        for item_name in global_one_up_unlock_item_data_table:
            self.assertEqual(len(self.get_items_by_name(item_name)), 0)
        for item_name in per_level_one_up_unlock_item_data_table:
            self.assertEqual(len(self.get_items_by_name(item_name)), 1)
        self.assertEqual(item_table["Castle - Butterflies"], 3626915)
        self.assertEqual(item_table["Tall, Tall Mountain - Butterflies"], 3626918)


class BothOneUpUnlockItemPoolTestBase(SM64TestBase):
    options = {
        "one_up_checks": Options.OneUpChecks.option_true,
        "one_up_unlocks": Options.OneUpUnlocks.option_both,
    }

    def test_both_one_up_unlock_item_forms_are_generated(self):
        for item_name in (*global_one_up_unlock_item_data_table, *per_level_one_up_unlock_item_data_table):
            self.assertEqual(len(self.get_items_by_name(item_name)), 1)


class MontyMoleEnemyUnlockItemPoolTestBase(SM64TestBase):
    options = {
        "enemy_unlocks": Options.EnemyUnlocks.option_per_level,
        "one_up_unlocks": Options.OneUpUnlocks.option_not_shuffled,
    }

    def test_enemy_unlocks_generate_monty_moles_when_one_ups_are_not_shuffled(self):
        self.assertEqual(len(self.get_items_by_name("Hazy Maze Cave - Monty Moles")), 1)
        self.assertEqual(len(self.get_items_by_name("Tall, Tall Mountain - Monty Moles")), 1)
        self.assertEqual(len(self.get_items_by_name("Monty Moles")), 0)


class MontyMoleOneUpUnlockItemPoolTestBase(SM64TestBase):
    options = {
        "enemy_unlocks": Options.EnemyUnlocks.option_per_level,
        "one_up_unlocks": Options.OneUpUnlocks.option_per_level,
    }

    def test_one_up_unlocks_own_monty_moles_without_duplicates(self):
        self.assertEqual(len(self.get_items_by_name("Hazy Maze Cave - Monty Moles")), 1)
        self.assertEqual(len(self.get_items_by_name("Tall, Tall Mountain - Monty Moles")), 1)
        self.assertEqual(len(self.get_items_by_name("Monty Moles")), 0)


class DddMoatExitClassificationTestBase(SM64TestBase):
    options = {"sub_area_shuffle": Options.SubAreaShuffle.option_separate}

    def test_moat_exit_is_a_trap_without_castle_returns(self):
        items = self.get_items_by_name("Dire, Dire Docks - Moat Exit")
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].classification, ItemClassification.trap)


class DddMoatExitCastleReturnsClassificationTestBase(SM64TestBase):
    options = {"sub_area_shuffle": Options.SubAreaShuffle.option_mixed_plus_castle_returns}

    def test_moat_exit_is_progression_with_castle_returns(self):
        items = self.get_items_by_name("Dire, Dire Docks - Moat Exit")
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].classification, ItemClassification.progression)


class DisabledLevelUnlockItemPoolTestBase(SM64TestBase):
    options = {"level_unlocks": Options.LevelUnlocks.option_disabled}

    def test_no_level_unlock_items_are_generated(self):
        slot_data = self.world.fill_slot_data()
        for item_name in (*special_level_unlock_item_names, *painting_unlock_item_data_table):
            self.assertEqual(len(self.get_items_by_name(item_name)), 0)
            self.assertEqual(slot_data["StartInventory"][item_table[item_name]], 1)


class DefaultLevelUnlockItemPoolTestBase(SM64TestBase):
    options = {"level_unlocks": Options.LevelUnlocks.option_special_only}

    def test_only_special_level_unlock_items_are_generated(self):
        slot_data = self.world.fill_slot_data()
        for item_name in special_level_unlock_item_names:
            self.assertEqual(len(self.get_items_by_name(item_name)), 1)
            self.assertNotIn(item_table[item_name], slot_data["StartInventory"])
        for item_name in painting_unlock_item_data_table:
            self.assertEqual(len(self.get_items_by_name(item_name)), 0)
            self.assertEqual(slot_data["StartInventory"][item_table[item_name]], 1)


class FullLevelUnlockItemPoolTestBase(SM64TestBase):
    options = {"level_unlocks": Options.LevelUnlocks.option_full}

    def test_all_level_unlock_items_are_generated(self):
        slot_data = self.world.fill_slot_data()
        for item_name in (*special_level_unlock_item_names, *painting_unlock_item_data_table):
            self.assertEqual(len(self.get_items_by_name(item_name)), 1)
            self.assertNotIn(item_table[item_name], slot_data["StartInventory"])


class BlocksanityOnTestBase(SM64TestBase):
    options = {
        "blocksanity": Options.Blocksanity.option_true,
    }

    def test_blocksanity_locations_are_generated(self):
        active_locations = {location.name for location in self.multiworld.get_locations(self.player)}
        slot_data = self.world.fill_slot_data()
        self.assertEqual(slot_data["Options"]["blocksanity"], 1)
        self.assertNotIn("Blocksanity", slot_data)
        for location_name in locBlocksanity_table:
            with self.subTest("Blocksanity location generated", location=location_name):
                self.assertIn(location_name, active_locations)


class GameBehaviorSlotDataTestBase(SM64TestBase):
    options = {
        "easy_butterflies": Options.EasyButterflies.option_true,
        "trigger_sparkles": Options.TriggerSparkles.option_true,
        "no_despawns": Options.NoDespawns.option_true,
    }

    def test_game_behavior_slot_data(self):
        slot_data = self.world.fill_slot_data()
        self.assertEqual(slot_data["EasyButterflies"], 1)
        self.assertEqual(slot_data["TriggerSparkles"], 1)
        self.assertEqual(slot_data["NoDespawn"], 1)
        self.assertNotIn("PermanentCoinCollection", slot_data)


class GlobalMoveItemPoolTestBase(SM64TestBase):
    options = {
        "triple_jump": Options.TripleJump.option_global,
    }

    def test_global_move_item_is_generated(self):
        self.assertEqual(self.world.fill_slot_data()["MoveRandoVec"], 2)
        self.assertEqual(len(self.get_items_by_name("Triple Jump")), 1)
        self.assertEqual(len(self.get_items_by_name("Bob-omb Battlefield - Triple Jump")), 0)


class PerLevelMoveItemPoolTestBase(SM64TestBase):
    options = {
        "triple_jump": Options.TripleJump.option_per_level,
    }

    def test_per_level_move_items_are_generated(self):
        self.assertEqual(self.world.fill_slot_data()["MoveRandoVec"], 2)
        self.assertEqual(len(self.get_items_by_name("Triple Jump")), 0)
        for area_name in main_course_move_area_names + collapsed_misc_move_area_names:
            with self.subTest("Per-level move item generated", area=area_name):
                self.assertEqual(len(self.get_items_by_name(f"{area_name} - Triple Jump")), 1)


class BothMoveItemPoolTestBase(SM64TestBase):
    options = {
        "triple_jump": Options.TripleJump.option_both,
    }

    def test_both_move_item_forms_are_generated(self):
        self.assertEqual(len(self.get_items_by_name("Triple Jump")), 1)
        for area_name in main_course_move_area_names + collapsed_misc_move_area_names:
            with self.subTest(area=area_name):
                self.assertEqual(len(self.get_items_by_name(f"{area_name} - Triple Jump")), 1)

    def test_either_move_item_form_satisfies_logic(self):
        from ..Rules import has_action

        for item_name in ("Triple Jump", "Bob-omb Battlefield - Triple Jump"):
            with self.subTest(item=item_name):
                state = CollectionState(self.multiworld)
                state.collect(self.world.create_item(item_name), True)
                self.assertTrue(has_action(state, self.player, "Triple Jump", "Bob-omb Battlefield"))


class PerLevelClimbItemPoolTestBase(SM64TestBase):
    options = {
        "climb": Options.Climb.option_per_level,
    }

    def test_big_boos_haunt_climb_is_not_generated(self):
        self.assertEqual(per_level_action_item_data_table["Big Boo's Haunt - Climb"].code, 3626373)
        self.assertEqual(len(self.get_items_by_name("Big Boo's Haunt - Climb")), 0)

    def test_other_per_level_climb_items_are_generated(self):
        self.assertEqual(self.world.fill_slot_data()["MoveRandoVec"], 512)
        self.assertEqual(len(self.get_items_by_name("Climb")), 0)
        for area_name in main_course_move_area_names + collapsed_misc_move_area_names:
            if area_name in non_climb_move_area_names:
                continue
            with self.subTest("Per-level Climb item generated", area=area_name):
                self.assertEqual(len(self.get_items_by_name(f"{area_name} - Climb")), 1)


class SeparateSecretStageMoveItemPoolTestBase(SM64TestBase):
    options = {
        "triple_jump": Options.TripleJump.option_per_level,
        "climb": Options.Climb.option_per_level,
        "combined_castle_and_secret_stage_move_items":
            Options.CombinedCastleAndSecretStageMoveItems.option_false,
    }

    def test_separate_castle_and_secret_stage_moves_are_generated(self):
        for area_name in main_course_move_area_names + separate_misc_move_area_names:
            with self.subTest(area=area_name):
                self.assertEqual(len(self.get_items_by_name(f"{area_name} - Triple Jump")), 1)
        self.assertEqual(len(self.get_items_by_name("Misc - Triple Jump")), 0)

    def test_climb_is_not_generated_for_stages_without_climbable_objects(self):
        for area_name in main_course_move_area_names + separate_misc_move_area_names:
            expected_count = 0 if area_name in non_climb_move_area_names else 1
            with self.subTest(area=area_name):
                self.assertEqual(len(self.get_items_by_name(f"{area_name} - Climb")), expected_count)

    def test_collapse_option_is_in_slot_data(self):
        self.assertEqual(
            self.world.fill_slot_data()["Options"]["combined_castle_and_secret_stage_move_items"], 0)


class IndividualArbitraryItemPoolTestBase(SM64TestBase):
    options = {
        "level_features": Options.LevelFeatures.option_per_level,
        "bobomb_buddies": Options.BobombBuddies.option_per_level,
    }

    def test_individual_arbitrary_items_are_generated(self):
        for item_name in {
                **checkerboard_item_data_table,
                **rolling_log_item_data_table,
                **purple_switch_item_data_table,
                **vertical_wind_item_data_table,
                **horizontal_wind_item_data_table,
                **freestanding_star_item_data_table,
                **star_block_item_data_table,
                **koopa_shell_block_item_data_table,
                **star_secret_item_data_table,
                **jet_stream_item_data_table,
        }:
            with self.subTest("Individual arbitrary item generated", item=item_name):
                self.assertEqual(len(self.get_items_by_name(item_name)), 1)

    def test_global_arbitrary_family_items_are_not_generated(self):
        for item_name in global_arbitrary_item_data_table:
            with self.subTest("Global arbitrary family item not generated", item=item_name):
                self.assertEqual(len(self.get_items_by_name(item_name)), 0)


class BothLevelFeatureAndBuddyItemPoolTestBase(SM64TestBase):
    options = {
        "level_features": Options.LevelFeatures.option_both,
        "bobomb_buddies": Options.BobombBuddies.option_both,
    }

    def test_both_level_feature_item_forms_are_generated(self):
        global_names = (
            *global_checkerboard_item_names,
            *global_rolling_log_item_names,
            *global_purple_switch_item_names,
            *global_treasure_chest_item_names,
            *global_warp_pipe_item_names,
            *global_vertical_wind_item_names,
            *global_horizontal_wind_item_names,
            *global_freestanding_star_item_names,
            *global_star_block_item_names,
            *global_koopa_shell_block_item_names,
            *global_star_secret_item_names,
            *global_jet_stream_item_names,
        )
        per_level_names = (
            *checkerboard_item_data_table,
            *rolling_log_item_data_table,
            *purple_switch_item_data_table,
            *per_level_treasure_chest_item_names,
            *per_level_warp_pipe_item_names,
            *vertical_wind_item_data_table,
            *horizontal_wind_item_data_table,
            *freestanding_star_item_data_table,
            *star_block_item_data_table,
            *koopa_shell_block_item_data_table,
            *star_secret_item_data_table,
            *jet_stream_item_data_table,
        )
        for item_name in (*global_names, *per_level_names):
            with self.subTest(item=item_name):
                self.assertEqual(len(self.get_items_by_name(item_name)), 1)

    def test_both_bobomb_buddy_item_forms_are_generated(self):
        for item_name in (*global_bobomb_buddy_item_names, *per_level_bobomb_buddy_item_names):
            with self.subTest(item=item_name):
                self.assertEqual(len(self.get_items_by_name(item_name)), 1)


class UnshuffledArbitraryItemPoolTestBase(SM64TestBase):
    options = {
        "level_features": Options.LevelFeatures.option_not_shuffled,
    }

    def test_unshuffled_arbitrary_items_are_not_generated(self):
        for item_name in (
                "Hazy Maze Cave - Swimming Beast",
                "Tick Tock Clock - Spinners",
                "Checkerboard Platforms",
                "Rolling Logs",
                "Purple Switches",
                "Treasure Chests",
                "Warp Pipes",
                "Vertical Wind",
                "Horizontal Wind",
                "Freestanding Stars",
                "Star Blocks",
                "Koopa Shell Blocks",
                "Star Secrets",
                "Jet Streams",
        ):
            with self.subTest("Unshuffled arbitrary item not generated", item=item_name):
                self.assertEqual(len(self.get_items_by_name(item_name)), 0)

    def test_unshuffled_arbitrary_items_are_start_inventory_slot_data_only(self):
        start_inventory = self.world.fill_slot_data()["StartInventory"]
        precollected_names = {item.name for item in self.multiworld.precollected_items[self.player]}
        for item_name in (
                "Hazy Maze Cave - Swimming Beast",
                "Tick Tock Clock - Spinners",
                "Checkerboard Platforms",
                "Rolling Logs",
                "Purple Switches",
                "Treasure Chests",
                "Warp Pipes",
                "Vertical Wind",
                "Horizontal Wind",
                "Freestanding Stars",
                "Star Blocks",
                "Koopa Shell Blocks",
                "Star Secrets",
                "Jet Streams",
        ):
            with self.subTest("Unshuffled arbitrary item in StartInventory only", item=item_name):
                self.assertEqual(start_inventory[item_table[item_name]], 1)
                self.assertNotIn(item_name, precollected_names)


class UnshuffledCoinAndEnemyUnlockItemPoolTestBase(SM64TestBase):
    def test_all_unlock_items_are_start_inventory_slot_data_only(self):
        unlock_items = {
            **global_coin_object_item_data_table,
            **per_level_coin_object_item_data_table,
            **global_enemy_item_data_table,
            **per_level_enemy_item_data_table,
        }
        start_inventory = self.world.fill_slot_data()["StartInventory"]
        precollected_names = {item.name for item in self.multiworld.precollected_items[self.player]}

        self.assertEqual(len(unlock_items), 280)
        for item_name, item_data in unlock_items.items():
            with self.subTest(item=item_name):
                self.assertEqual(start_inventory[item_data.code], 1)
                self.assertEqual(len(self.get_items_by_name(item_name)), 0)
                self.assertNotIn(item_name, precollected_names)

    def test_heave_ho_item_classifications(self):
        self.assertEqual(
            self.world.get_item_classification(
                per_level_enemy_item_data_table["Wet-Dry World - Heave-Hos"]),
            ItemClassification.progression)
        self.assertEqual(
            self.world.get_item_classification(
                per_level_enemy_item_data_table["Tick Tock Clock - Heave-Ho"]),
            ItemClassification.trap)

    def test_tweesters_are_traps_without_their_logic_trick(self):
        for item_name, item_data in (
                ("Shifting Sand Land - Tweesters",
                 per_level_enemy_item_data_table["Shifting Sand Land - Tweesters"]),
        ):
            with self.subTest(item=item_name):
                self.assertEqual(
                    self.world.get_item_classification(item_data),
                    ItemClassification.trap)


class GlobalCoinAndEnemyUnlockItemPoolTestBase(SM64TestBase):
    options = {
        "coin_object_unlocks": Options.CoinObjectUnlocks.option_global,
        "enemy_unlocks": Options.EnemyUnlocks.option_global,
    }

    def test_global_mode_unlock_items_are_generated(self):
        expected_names = set(global_mode_coin_object_item_names) | set(global_mode_enemy_item_names)
        self.assertEqual(len(expected_names), 62)
        for item_name in expected_names:
            with self.subTest(item=item_name):
                self.assertEqual(len(self.get_items_by_name(item_name)), 1)
                self.assertNotIn(item_table[item_name], self.world.fill_slot_data()["StartInventory"])

    def test_single_level_enemy_types_reuse_their_level_item(self):
        expected_level_items = {
            "Bob-omb Battlefield - Chain Chomp",
            "Tiny-Huge Island - Wiggler",
            "Shifting Sand Land - Tweesters",
            "Shifting Sand Land - Klepto",
            "Big Boo's Haunt - Mad Piano",
            "Big Boo's Haunt - Haunted Chairs",
            "Dire, Dire Docks - Sushi Sharks",
            "Dire, Dire Docks - Bubs",
            "Tiny-Huge Island - Bubbas",
            "Shifting Sand Land - Tox Boxes",
            "Bob-omb Battlefield - Water Bombs",
            "Hazy Maze Cave - Boulders",
            "Lethal Lava Land - Bouncing Fireballs",
            "Shifting Sand Land - Spindel",
            "Jolly Roger Bay - Falling Pillars",
        }
        self.assertLessEqual(expected_level_items, set(global_mode_enemy_item_names))
        self.assertTrue(expected_level_items.isdisjoint(global_enemy_item_data_table))

    def test_new_cross_level_enemy_items_are_the_only_new_global_items(self):
        new_global_items = {
            name for name, data in global_enemy_item_data_table.items()
            if data.code >= 3626957
        }
        self.assertEqual(new_global_items, {
            "Bowsers",
            "Amps",
            "Bowling Balls",
            "Flamethrowers and Fire Bars",
            "Fire Spitters",
        })

    def test_enemy_item_names_match_physical_counts(self):
        expected_names = {
            "Shifting Sand Land - Fly Guys",
            "Tiny-Huge Island - Fly Guys",
            "Tiny-Huge Island - Koopa Troopas",
            "Big Boo's Haunt - Big Boos",
            "Whomp's Fortress - Thwomps",
            "Snowman's Land - Amp",
            "Vanish Cap Under the Moat - Amp",
        }
        self.assertLessEqual(expected_names, set(per_level_enemy_item_data_table))


class IndividualCoinAndEnemyUnlockItemPoolTestBase(SM64TestBase):
    options = {
        "coin_object_unlocks": Options.CoinObjectUnlocks.option_per_level,
        "enemy_unlocks": Options.EnemyUnlocks.option_per_level,
    }

    def test_individual_unlock_items_are_generated(self):
        individual_items = {
            **per_level_coin_object_item_data_table,
            **per_level_enemy_item_data_table,
        }
        self.assertEqual(len(individual_items), 242)
        for item_name in individual_items:
            with self.subTest(item=item_name):
                self.assertEqual(len(self.get_items_by_name(item_name)), 1)
                self.assertNotIn(item_table[item_name], self.world.fill_slot_data()["StartInventory"])


class BothCoinAndEnemyUnlockItemPoolTestBase(SM64TestBase):
    options = {
        "coin_object_unlocks": Options.CoinObjectUnlocks.option_both,
        "enemy_unlocks": Options.EnemyUnlocks.option_both,
    }

    def test_both_unlock_item_forms_are_generated(self):
        expected_names = (
            set(global_mode_coin_object_item_names)
            | set(per_level_coin_object_item_data_table)
            | set(global_mode_enemy_item_names)
            | set(per_level_enemy_item_data_table)
        )
        for item_name in expected_names:
            with self.subTest(item=item_name):
                self.assertEqual(len(self.get_items_by_name(item_name)), 1)


class UnshuffledBowserArenaBombItemPoolTestBase(SM64TestBase):
    def test_bowser_arena_bombs_are_start_inventory_slot_data_only(self):
        start_inventory = self.world.fill_slot_data()["StartInventory"]
        self.assertEqual(start_inventory[item_table["Progressive Bowser Arena Bomb"]], 5)
        for item_name in bowser_bomb_item_data_table:
            self.assertEqual(len(self.get_items_by_name(item_name)), 0)


class GlobalBowserArenaBombItemPoolTestBase(SM64TestBase):
    options = {"bowser_bombs": Options.BowserBombs.option_global}

    def test_global_bowser_arena_bombs_are_generated(self):
        self.assertEqual(len(self.get_items_by_name("Progressive Bowser Arena Bomb")), 5)
        self.assertEqual(
            len(self.get_items_by_name("Bowser in the Sky - Progressive Bowser Arena Bomb")), 0)
        self.assertEqual(
            len(self.get_items_by_name("Bowser in the Dark World - Progressive Bowser Arena Bomb")), 0)
        self.assertEqual(
            len(self.get_items_by_name("Bowser in the Fire Sea - Progressive Bowser Arena Bomb")), 0)


class IndividualBowserArenaBombItemPoolTestBase(SM64TestBase):
    options = {"bowser_bombs": Options.BowserBombs.option_per_level}

    def test_individual_bowser_arena_bombs_are_generated(self):
        expected_counts = {
            "Bowser in the Dark World - Progressive Bowser Arena Bomb": 4,
            "Bowser in the Fire Sea - Progressive Bowser Arena Bomb": 4,
            "Bowser in the Sky - Progressive Bowser Arena Bomb": 5,
        }
        for item_name, count in expected_counts.items():
            self.assertEqual(len(self.get_items_by_name(item_name)), count)
        self.assertEqual(len(self.get_items_by_name("Progressive Bowser Arena Bomb")), 0)


class BothBowserArenaBombItemPoolTestBase(SM64TestBase):
    options = {"bowser_bombs": Options.BowserBombs.option_both}

    def test_both_bowser_arena_bomb_item_forms_are_generated(self):
        self.assertEqual(len(self.get_items_by_name("Progressive Bowser Arena Bomb")), 5)
        self.assertEqual(
            len(self.get_items_by_name("Bowser in the Dark World - Progressive Bowser Arena Bomb")), 4)
        self.assertEqual(
            len(self.get_items_by_name("Bowser in the Fire Sea - Progressive Bowser Arena Bomb")), 4)
        self.assertEqual(
            len(self.get_items_by_name("Bowser in the Sky - Progressive Bowser Arena Bomb")), 5)


class GroupedCastleKeyPoolTestBase(SM64TestBase):
    options = {
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
    }

    def test_grouped_castle_keys_are_generated(self):
        self.assertEqual(len(self.get_items_by_name("Dark World Key")), 1)
        self.assertEqual(len(self.get_items_by_name("Progressive Basement Key")), 2)
        self.assertEqual(len(self.get_items_by_name("Progressive Upstairs Key")), 3)
        self.assertEqual(len(self.get_items_by_name("Progressive Key")), 0)


class MarioColorsTestBase(SM64TestBase):
    options = {
        "mario_hat_color": 0x010203,
        "mario_shirt_color": "green",
        "mario_overalls_color": "purple",
        "mario_gloves_color": "black",
        "mario_shoes_color": "default_brown",
        "mario_skin_color": "default_skin",
        "mario_hair_color": "default_brown",
    }

    def test_mario_colors_slot_data(self):
        self.assertEqual(self.world.fill_slot_data()["MarioColors"], {
            "hat": [1, 2, 3],
            "shirt": [0, 255, 0],
            "overalls": [255, 0, 255],
            "gloves": [0, 0, 0],
            "shoes": [114, 28, 14],
            "skin": [254, 193, 121],
            "hair": [115, 6, 0],
        })


class MarioColorsValidationTestBase(SM64TestBase):
    auto_construct = False

    def test_named_color_values(self):
        self.assertEqual(Options.MarioShirtColor.from_any("red").value, 16711680)
        self.assertEqual(Options.MarioShirtColor.from_any("green").value, 65280)
        self.assertEqual(Options.MarioShirtColor.from_any("purple").value, 16711935)

    def test_exact_decimal_color_value(self):
        self.assertEqual(Options.MarioHatColor.from_any(0x123456).value, 1193046)

    def test_part_specific_default_color_values(self):
        self.assertEqual(Options.MarioShoesColor.from_any("default_brown").value, 7478286)
        self.assertEqual(Options.MarioSkinColor.from_any("default_skin").value, 16695673)
        self.assertEqual(Options.MarioHairColor.from_any("default_brown").value, 7538176)

    def test_color_value_must_be_in_rgb_range(self):
        with self.assertRaises(Exception):
            Options.MarioHatColor.from_any(16777216)


class MusicShuffleOffTestBase(SM64TestBase):
    options = {
        "music_shuffle": Options.MusicShuffle.option_off
    }

    def test_music_shuffle_slot_data(self):
        slot_data = self.world.fill_slot_data()
        self.assertEqual(0, slot_data["MusicShuffleMode"])
        self.assertNotIn("MusicMap", slot_data)


class MusicShuffleShuffleTestBase(SM64TestBase):
    options = {
        "music_shuffle": Options.MusicShuffle.option_shuffle
    }

    def test_music_shuffle_slot_data(self):
        slot_data = self.world.fill_slot_data()
        self.assertEqual(1, slot_data["MusicShuffleMode"])
        self.assertEqual({str(area_key) for area_key in SM64_MUSIC_AREA_SEQUENCES}, set(slot_data["MusicMap"]))
        self.assertTrue(all(song in SM64_MUSIC_SAFE_SEQUENCE_IDS for song in slot_data["MusicMap"].values()))


class MusicShuffleRandomOnLoadTestBase(SM64TestBase):
    options = {
        "music_shuffle": Options.MusicShuffle.option_random_on_load
    }

    def test_music_shuffle_slot_data(self):
        slot_data = self.world.fill_slot_data()
        self.assertEqual(2, slot_data["MusicShuffleMode"])
        self.assertNotIn("MusicMap", slot_data)


class SkyboxShuffleOffTestBase(SM64TestBase):
    options = {"skybox_shuffle": Options.SkyboxShuffle.option_off}

    def test_skybox_shuffle_slot_data(self):
        slot_data = self.world.fill_slot_data()
        self.assertEqual(0, slot_data["SkyboxShuffleMode"])
        self.assertNotIn("SkyboxMap", slot_data)


class SkyboxShuffleShuffleTestBase(SM64TestBase):
    options = {"skybox_shuffle": Options.SkyboxShuffle.option_shuffle}

    def test_skybox_shuffle_slot_data(self):
        from ..Skyboxes import SM64_SKYBOX_AREAS, SM64_SKYBOX_IDS
        slot_data = self.world.fill_slot_data()
        self.assertEqual(1, slot_data["SkyboxShuffleMode"])
        self.assertEqual({str(area) for area in SM64_SKYBOX_AREAS}, set(slot_data["SkyboxMap"]))
        self.assertTrue(all(skybox in SM64_SKYBOX_IDS for skybox in slot_data["SkyboxMap"].values()))


class SkyboxShuffleRandomOnLoadTestBase(SM64TestBase):
    options = {"skybox_shuffle": Options.SkyboxShuffle.option_random_on_load}

    def test_skybox_shuffle_slot_data(self):
        slot_data = self.world.fill_slot_data()
        self.assertEqual(2, slot_data["SkyboxShuffleMode"])
        self.assertNotIn("SkyboxMap", slot_data)


class CoinStarRequirementTestBase(SM64TestBase):
    options = {
        "bob_omb_battlefield_coin_star_requirement": 100,
        "whomps_fortress_coin_star_requirement": 90,
        "jolly_roger_bay_coin_star_requirement": 100,
        "cool_cool_mountain_coin_star_requirement": 80,
        "big_boos_haunt_coin_star_requirement": 100,
        "hazy_maze_cave_coin_star_requirement": 100,
        "lethal_lava_land_coin_star_requirement": 75,
        "shifting_sand_land_coin_star_requirement": 100,
        "dire_dire_docks_coin_star_requirement": 100,
        "snowmans_land_coin_star_requirement": 100,
        "wet_dry_world_coin_star_requirement": 100,
        "tall_tall_mountain_coin_star_requirement": 100,
        "tiny_huge_island_coin_star_requirement": 100,
        "tick_tock_clock_coin_star_requirement": 100,
        "rainbow_ride_coin_star_requirement": 100,
    }

    def test_coin_star_requirements_slot_data(self):
        self.assertEqual(self.world.fill_slot_data()["CoinStarRequirements"], [
            100, 90, 100, 80, 100, 100, 75, 100, 100, 100, 100, 100, 100, 100, 100
        ])

    def test_coin_star_requirement_ranges(self):
        expected_range_ends = {
            Options.BobOmbBattlefieldCoinStarRequirement: 146,
            Options.WhompsFortressCoinStarRequirement: 141,
            Options.JollyRogerBayCoinStarRequirement: 104,
            Options.CoolCoolMountainCoinStarRequirement: 154,
            Options.BigBoosHauntCoinStarRequirement: 151,
            Options.HazyMazeCaveCoinStarRequirement: 139,
            Options.LethalLavaLandCoinStarRequirement: 133,
            Options.ShiftingSandLandCoinStarRequirement: 136,
            Options.DireDireDocksCoinStarRequirement: 106,
            Options.SnowmansLandCoinStarRequirement: 127,
            Options.WetDryWorldCoinStarRequirement: 152,
            Options.TallTallMountainCoinStarRequirement: 137,
            Options.TinyHugeIslandCoinStarRequirement: 192,
            Options.TickTockClockCoinStarRequirement: 128,
            Options.RainbowRideCoinStarRequirement: 146,
        }
        for option in Options.coin_star_requirement_options:
            with self.subTest(option=option.__name__):
                self.assertEqual(option.range_start, 1)
                self.assertEqual(option.range_end, expected_range_ends.get(option, 100))


class CoinStarsTestBase(SM64TestBase):
    # Ensure Coin Star locations are always created.
    def test_coin_star_locations(self):
        possible_locations = self.world.location_names
        for loc in loc100Coin_table:
            # Use subtest to force all locations to be tested
            with self.subTest("Location created", location=loc):
                self.assertIn(loc, possible_locations)


class SecretStageCoinCountMaxCoinsOptionTestBase(SM64TestBase):
    run_default_tests = False

    def test_secret_stage_coin_count_max_coin_ranges_and_defaults(self):
        expected_options = {
            Options.PrincessSecretSlideCoinCountMaxCoins: (80, 80),
            Options.SecretAquariumCoinCountMaxCoins: (56, 56),
            Options.WingMarioOverTheRainbowCoinCountMaxCoins: (56, 56),
            Options.TowerOfTheWingCapCoinCountMaxCoins: (63, 63),
            Options.VanishCapUnderTheMoatCoinCountMaxCoins: (27, 27),
            Options.CavernOfTheMetalCapCoinCountMaxCoins: (47, 47),
            Options.BowserInTheDarkWorldCoinCountMaxCoins: (80, 80),
            Options.BowserInTheFireSeaCoinCountMaxCoins: (80, 80),
            Options.BowserInTheSkyCoinCountMaxCoins: (76, 76),
        }
        self.assertEqual(set(Options.secret_stage_coin_count_max_coin_options), set(expected_options))
        for option, (range_end, default) in expected_options.items():
            with self.subTest(option=option.__name__):
                self.assertEqual(option.range_start, 0)
                self.assertEqual(option.range_end, range_end)
                self.assertEqual(option.default, default)


class CoinCountChecksLocationTableTestBase(SM64TestBase):
    run_default_tests = False

    def test_coin_count_check_location_ids_match_client_doc(self):
        expected_ids = {
            "Bob-omb Battlefield - 1 Coin": 3627000,
            "Bob-omb Battlefield - 145 Coins": 3627144,
            "Whomp's Fortress - 1 Coin": 3627146,
            "Jolly Roger Bay - 1 Coin": 3627287,
            "Rainbow Ride - 145 Coins": 3629089,
            "The Princess's Secret Slide - 1 Coin": 3629193,
            "The Princess's Secret Slide - 80 Coins": 3629272,
            "The Secret Aquarium - 1 Coin": 3629273,
            "Wing Mario Over the Rainbow - 1 Coin": 3629329,
            "Tower of the Wing Cap - 1 Coin": 3629385,
            "Tower of the Wing Cap - 63 Coins": 3629447,
            "Vanish Cap Under the Moat - 1 Coin": 3629448,
            "Cavern of the Metal Cap - 1 Coin": 3629475,
            "Bowser in the Dark World - 1 Coin": 3629522,
            "Bowser in the Fire Sea - 1 Coin": 3629602,
            "Bowser in the Sky - 1 Coin": 3629682,
            "Bowser in the Sky - 76 Coins": 3629757,
        }
        for location_name, location_id in expected_ids.items():
            with self.subTest("CoinCountChecks location ID", location=location_name):
                self.assertEqual(coin_count_check_location_table[location_name], location_id)
                self.assertEqual(location_table[location_name], location_id)

    def test_coin_count_checks_skips_final_coin_threshold_for_each_course(self):
        skipped_final_locations = {
            "Bob-omb Battlefield": 146,
            "Whomp's Fortress": 141,
            "Jolly Roger Bay": 104,
            "Cool, Cool Mountain": 154,
            "Big Boo's Haunt": 151,
            "Hazy Maze Cave": 139,
            "Lethal Lava Land": 133,
            "Shifting Sand Land": 136,
            "Dire, Dire Docks": 106,
            "Snowman's Land": 127,
            "Wet-Dry World": 152,
            "Tall, Tall Mountain": 137,
            "Tiny-Huge Island": 192,
            "Tick Tock Clock": 128,
            "Rainbow Ride": 146,
        }
        self.assertEqual(len(coin_count_check_location_table), 2642)
        self.assertEqual(len(secret_stage_coin_count_check_location_table), 565)
        for course_name, coin_count in skipped_final_locations.items():
            with self.subTest("Final coin threshold skipped", course=course_name):
                self.assertNotIn(get_coin_count_check_location_name(course_name, coin_count), coin_count_check_location_table)


class CoinCountChecksDefaultOffTestBase(SM64TestBase):
    run_default_tests = False

    def test_default_no_active_coin_count_check_locations(self):
        active_locations = {location.name for location in self.multiworld.get_locations(self.player)}
        self.assertFalse(active_locations.intersection(coin_count_check_location_table))


class CoinCountChecksGenerationTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        "coin_count_checks": 2,
        "bob_omb_battlefield_coin_star_requirement": 50,
    }

    def test_coin_count_checks_generates_even_thresholds_below_coin_star(self):
        active_locations = {location.name for location in self.multiworld.get_locations(self.player)}
        self.assertIn("Bob-omb Battlefield - 25 Coins", active_locations)
        self.assertNotIn("Bob-omb Battlefield - 1 Coin", active_locations)
        self.assertNotIn("Bob-omb Battlefield - 50 Coins", active_locations)

    def test_thi_coin_count_check_locations_use_shared_coins_region(self):
        location = self.multiworld.get_location("Tiny-Huge Island - 33 Coins", self.player)
        self.assertEqual(location.parent_region.name, "Tiny-Huge Island - Coins")

    def test_courses_with_shufflable_subareas_use_shared_coins_regions(self):
        for course_name in (
                "Jolly Roger Bay",
                "Cool, Cool Mountain",
                "Lethal Lava Land",
                "Shifting Sand Land",
                "Snowman's Land",
                "Tall, Tall Mountain",
        ):
            with self.subTest(course=course_name):
                location_name = next(
                    name for name in self.world.coin_count_check_location_names
                    if name.startswith(f"{course_name} - ")
                )
                location = self.multiworld.get_location(location_name, self.player)
                self.assertEqual(location.parent_region.name, f"{course_name} - Coins")

    def test_ttm_coins_region_accepts_main_area_or_secret_slide_access(self):
        coin_region = self.multiworld.get_region("Tall, Tall Mountain - Coins", self.player)
        self.assertEqual(
            {entrance.parent_region.name for entrance in coin_region.entrances},
            {"Tall, Tall Mountain", "Tall, Tall Mountain - Secret Slide"},
        )


class SecretStageCoinCountChecksTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        "coin_count_checks": 100,
    }

    def test_secret_stage_coin_count_checks_use_percentage(self):
        active_locations = {location.name for location in self.multiworld.get_locations(self.player)}
        self.assertTrue(active_locations.intersection(secret_stage_coin_count_check_location_table))


class SecretStageCoinCountChecksGenerationTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        "coin_count_checks": 50,
        "princess_secret_slide_coin_count_max_coins": 10,
        "tower_of_the_wing_cap_coin_count_max_coins": 16,
    }

    def test_secret_stage_coin_count_checks_generates_locations(self):
        active_locations = {location.name for location in self.multiworld.get_locations(self.player)}
        self.assertIn("The Princess's Secret Slide - 1 Coin", active_locations)
        self.assertIn("The Secret Aquarium - 1 Coin", active_locations)
        self.assertIn("Wing Mario Over the Rainbow - 1 Coin", active_locations)

    def test_secret_stage_max_coin_option_controls_location_count(self):
        active_locations = {location.name for location in self.multiworld.get_locations(self.player)}
        active_slide_locations = {
            location_name for location_name in active_locations
            if location_name in secret_stage_coin_count_check_location_table
            and location_name.startswith("The Princess's Secret Slide - ")
        }
        self.assertEqual(len(active_slide_locations), 5)
        self.assertIn("The Princess's Secret Slide - 1 Coin", active_locations)
        self.assertIn("The Princess's Secret Slide - 9 Coins", active_locations)
        self.assertNotIn("The Princess's Secret Slide - 10 Coins", active_locations)
        self.assertNotIn("The Princess's Secret Slide - 80 Coins", active_locations)

    def test_tower_of_the_wing_cap_max_coin_option_controls_location_count(self):
        active_locations = {location.name for location in self.multiworld.get_locations(self.player)}
        active_totwc_locations = {
            location_name for location_name in active_locations
            if location_name in secret_stage_coin_count_check_location_table
            and location_name.startswith("Tower of the Wing Cap - ")
        }
        self.assertEqual(len(active_totwc_locations), 8)
        self.assertIn("Tower of the Wing Cap - 1 Coin", active_locations)
        self.assertIn("Tower of the Wing Cap - 15 Coins", active_locations)
        self.assertNotIn("Tower of the Wing Cap - 16 Coins", active_locations)
        self.assertNotIn("Tower of the Wing Cap - 63 Coins", active_locations)

    def test_secret_stage_coin_count_check_locations_use_stage_regions(self):
        location = self.multiworld.get_location("Wing Mario Over the Rainbow - 1 Coin", self.player)
        self.assertEqual(location.parent_region.name, "Wing Mario Over the Rainbow")


class TowerOfTheWingCapFullAccessibilityCapTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        "accessibility": Options.SM64Accessibility.option_full,
        "coin_count_checks": 100,
        "tower_of_the_wing_cap_coin_count_max_coins": 63,
    }

    def test_full_accessibility_keeps_locations_above_31(self):
        active_locations = {location.name for location in self.multiworld.get_locations(self.player)}
        self.assertIn("Tower of the Wing Cap - 31 Coins", active_locations)
        self.assertIn("Tower of the Wing Cap - 63 Coins", active_locations)


class TowerOfTheWingCapItemsAccessibilityTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        "accessibility": Options.SM64Accessibility.option_items,
        "coin_count_checks": 100,
        "tower_of_the_wing_cap_coin_count_max_coins": 63,
    }

    def test_items_accessibility_keeps_locations_above_31(self):
        active_locations = {location.name for location in self.multiworld.get_locations(self.player)}
        self.assertIn("Tower of the Wing Cap - 63 Coins", active_locations)


class TowerOfTheWingCapMinimalAccessibilityTestBase(TowerOfTheWingCapItemsAccessibilityTestBase):
    options = {
        **TowerOfTheWingCapItemsAccessibilityTestBase.options,
        "accessibility": Options.SM64Accessibility.option_minimal,
    }


class TowerOfTheWingCapMasteryGenerationTestBase(TowerOfTheWingCapItemsAccessibilityTestBase):
    options = {
        **TowerOfTheWingCapItemsAccessibilityTestBase.options,
        "accessibility": Options.SM64Accessibility.option_full,
    }


class CoinCountChecksOverflowGenerationTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        "area_rando": Options.AreaRandomizer.option_Off,
        "level_unlocks": Options.LevelUnlocks.option_full,
        "cap_items": Options.CapItems.option_per_level,
        "buddy_checks": Options.BuddyChecks.option_true,
        "one_up_checks": Options.OneUpChecks.option_false,
        "marios_hat": Options.MariosHat.option_true,
        "level_features": Options.LevelFeatures.option_per_level,
        "bobomb_buddies": Options.BobombBuddies.option_per_level,
        "triple_jump": Options.TripleJump.option_per_level,
        "long_jump": Options.LongJump.option_per_level,
        "backflip": Options.Backflip.option_per_level,
        "side_flip": Options.SideFlip.option_per_level,
        "wall_kick": Options.WallKick.option_per_level,
        "dive": Options.Dive.option_per_level,
        "ground_pound": Options.GroundPound.option_per_level,
        "kick": Options.Kick.option_per_level,
        "climb": Options.Climb.option_per_level,
        "ledge_grab": Options.LedgeGrab.option_per_level,
        **{option_name: 1 for option_name in Options.coin_star_requirement_option_names},
    }

    def get_active_coin_counts_by_course(self):
        active_locations = set(self.world.coin_count_check_location_names)
        return {
            course_name: [
                coin_count for coin_count in range(1, max_coin_star_requirement)
                if get_coin_count_check_location_name(course_name, coin_count) in active_locations
            ]
            for course_name, _course_offset, _option_name, max_coin_star_requirement in coin_count_check_course_data
        }

    def test_overflow_adds_extra_coin_count_check_locations_before_item_creation(self):
        self.assertGreater(len(self.world.coin_count_check_location_names), 0)
        self.assertGreaterEqual(self.world.filler_count, 0)

    def test_overflow_locations_at_coin_star_thresholds_are_distributed_evenly(self):
        coin_counts_by_course = self.get_active_coin_counts_by_course()
        location_counts = [len(coin_counts) for coin_counts in coin_counts_by_course.values()]
        self.assertGreater(min(location_counts), 0)
        self.assertLessEqual(max(location_counts) - min(location_counts), 1)
        for course_name, coin_counts in coin_counts_by_course.items():
            with self.subTest("Overflow coin checks are consecutive from threshold", course=course_name):
                self.assertEqual(coin_counts, list(range(1, len(coin_counts) + 1)))


class CoinCountChecksNoOverflowWithIndividualCoinChecksTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        **CoinCountChecksOverflowGenerationTestBase.options,
        "coin_checks": 100,
    }

    def test_individual_coin_locations_prevent_false_overflow(self):
        self.assertEqual(self.world.coin_count_check_location_names, ())
        self.assertGreater(self.world.filler_count, 0)


# 1-Up Checks
class OneUpChecksOffTestBase(SM64TestBase):
    options = {
        "one_up_checks": Options.OneUpChecks.option_false,
    }

    def test_one_up_locations_are_not_generated(self):
        active_locations = {location.name for location in self.multiworld.get_locations(self.player)}
        self.assertTrue(set(locOneUp_table).isdisjoint(active_locations))


# Entrance Randomizer
class EntranceRandoOffTestBase(SM64TestBase):
    options = {
        "area_rando": Options.AreaRandomizer.option_Off
    }

    # Ensure entrance rando disabled
    def test_all_entrances_are_vanilla(self):
        for entrance_level_id in {*sm64_level_to_paintings, *sm64_level_to_secrets}:
            with self.subTest("Entrance maps to itself", entrance=entrance_level_id):
                self.assertEqual(self.world.area_connections[entrance_level_id], entrance_level_id)

    def test_BoB_entrance(self):
        bob_level_id = sm64_entrances_to_level["Bob-omb Battlefield"]
        self.assertEqual(self.world.area_connections[bob_level_id], bob_level_id)

    def test_BitFS_entrance(self):
        bitfs_level_id = sm64_entrances_to_level["Bowser in the Fire Sea"]
        self.assertEqual(self.world.area_connections[bitfs_level_id], bitfs_level_id)

    def test_WDW_variant_entrances(self):
        for variant_id in wdw_variant_ids:
            with self.subTest("WDW variant maps to itself", variant=variant_id):
                self.assertEqual(self.world.area_connections[variant_id], variant_id)

    def test_TTC_variant_entrances(self):
        for variant_id in ttc_variant_ids:
            with self.subTest("TTC variant maps to itself", variant=variant_id):
                self.assertEqual(self.world.area_connections[variant_id], variant_id)

    def test_starting_state_has_two_reachable_checks(self):
        self.assertTrue(world_has_two_reachable_starting_checks(self))


class EntranceRandoOffLockedPaintingsTestBase(SM64TestBase):
    options = {
        "area_rando": Options.AreaRandomizer.option_Off,
        "level_unlocks": Options.LevelUnlocks.option_full,
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
    }

    def test_all_entrances_are_vanilla(self):
        for entrance_level_id in {*sm64_level_to_paintings, *sm64_level_to_secrets}:
            with self.subTest("Entrance maps to itself", entrance=entrance_level_id):
                self.assertEqual(self.world.area_connections[entrance_level_id], entrance_level_id)

    def test_starting_state_has_two_reachable_checks(self):
        self.assertTrue(world_has_two_reachable_starting_checks(self))

class EntranceRandoCourseTestBase(SM64TestBase):
    options = {
        "area_rando": Options.AreaRandomizer.option_Courses_Only
    }

    def test_BoB_entrance(self):
        bob_level_id = sm64_entrances_to_level["Bob-omb Battlefield"]
        # BoB goes to a painting, not a secret
        self.assertNotIn(self.world.area_connections[bob_level_id], sm64_level_to_secrets.keys())
        self.assertIn(self.world.area_connections[bob_level_id], sm64_level_to_paintings.keys())

    def test_BitFS_entrance(self):
        bitfs_level_id = sm64_entrances_to_level["Bowser in the Fire Sea"]
        # BitFS is a secret (aka not a course), unaffected by Course Only entrance rando.
        self.assertEqual(self.world.area_connections[bitfs_level_id], bitfs_level_id)

    def test_WDW_and_TTC_variants_are_course_entrances(self):
        for variant_id in wdw_variant_ids | ttc_variant_ids:
            with self.subTest("Variant source is shuffled in course pool", variant=variant_id):
                self.assertIn(variant_id, self.world.area_connections)
                self.assertIn(self.world.area_connections[variant_id], sm64_level_to_paintings.keys())

    def test_starting_state_has_two_reachable_checks(self):
        self.assertTrue(world_has_two_reachable_starting_checks(self))

    def test_event_locations_are_not_entrance_hinted(self):
        hint_data = {}
        self.world.extend_hint_information(hint_data)
        self.assertIn(self.player, hint_data)
        self.assertNotIn(None, hint_data[self.player])
        self.assertIsNone(self.multiworld.get_location("Bob-omb Battlefield - Bob-omb Buddy", self.player).address)


class EntranceRandoSeparateTestBase(SM64TestBase):
    options = {
        "area_rando": Options.AreaRandomizer.option_Courses_and_Secrets_Separate
    }

    def test_BoB_entrance(self):
        bob_level_id = sm64_entrances_to_level["Bob-omb Battlefield"]
        # BoB goes to a painting, not a secret
        self.assertNotIn(self.world.area_connections[bob_level_id], sm64_level_to_secrets.keys())
        self.assertIn(self.world.area_connections[bob_level_id], sm64_level_to_paintings.keys())

    def test_BitFS_entrance(self):
        bitfs_level_id = sm64_entrances_to_level["Bowser in the Fire Sea"]
        # BitFS goes to a secret, not a painting
        self.assertIn(self.world.area_connections[bitfs_level_id], sm64_level_to_secrets.keys())
        self.assertNotIn(self.world.area_connections[bitfs_level_id], sm64_level_to_paintings.keys())
        # BitFS does not go to DDD
        self.assertIsNot(self.world.area_connections[bitfs_level_id], sm64_entrances_to_level["Dire, Dire Docks"])

    def test_WDW_and_TTC_variants_are_course_entrances(self):
        for variant_id in wdw_variant_ids | ttc_variant_ids:
            with self.subTest("Variant source is shuffled in course pool", variant=variant_id):
                self.assertIn(variant_id, self.world.area_connections)
                self.assertIn(self.world.area_connections[variant_id], sm64_level_to_paintings.keys())


class EntranceRandoAllTestBase(SM64TestBase):
    options = {
        "area_rando": Options.AreaRandomizer.option_Courses_and_Secrets
    }

    def test_BitFS_entrance(self):
        bitfs_level_id = sm64_entrances_to_level["Bowser in the Fire Sea"]
        # BitFS does not go to DDD
        self.assertIsNot(self.world.area_connections[bitfs_level_id], sm64_entrances_to_level["Dire, Dire Docks"])

    def test_WDW_and_TTC_variants_are_independent_sources(self):
        for variant_id in wdw_variant_ids | ttc_variant_ids:
            with self.subTest("Variant source is present", variant=variant_id):
                self.assertIn(variant_id, self.world.area_connections)


# Completion Type
class CompletionLastBowserTestBase(SM64TestBase):
    options = {
        "completion_type": Options.CompletionType.option_Last_Bowser_Stage
    }

    def test_grand_star_check_is_not_created(self):
        self.assertNotIn(
            "Bowser in the Sky - Grand Star",
            {location.name for location in self.multiworld.get_locations(self.player)},
        )


class CompletionAllBowserTestBase(SM64TestBase):
    options = {
        "completion_type": Options.CompletionType.option_All_Bowser_Stages
    }

    def test_grand_star_check_is_created(self):
        location = self.multiworld.get_location("Bowser in the Sky - Grand Star", self.player)
        self.assertEqual(location.parent_region.name, "Bowser in the Sky - Bowser Arena")

    def test_grand_star_check_requires_all_bowser_stages(self):
        state = self.multiworld.get_all_state(False)
        location = self.multiworld.get_location("Bowser in the Sky - Grand Star", self.player)
        self.assertTrue(location.can_reach(state))

        for required_location_name in (
            "Bowser in the Dark World - Key",
            "Bowser in the Fire Sea - Key",
        ):
            required_location = self.multiworld.get_location(required_location_name, self.player)
            original_rule = required_location.access_rule
            try:
                required_location.access_rule = lambda _: False
                self.assertFalse(
                    location.can_reach(self.multiworld.get_all_state(False)),
                    required_location_name,
                )
            finally:
                required_location.access_rule = original_rule


# Option Combos


# Power Star item generation
class NoPowerStarsTestBase(SM64TestBase):
    options = {
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "one_up_checks": Options.OneUpChecks.option_false,
    }

    def test_no_power_stars_generated(self):
        cap_length_items = sum(
            len(self.get_items_by_name(item_name))
            for item_name in (
                "Progressive Wing Cap Length",
                "Progressive Metal Cap Length",
                "Progressive Vanish Cap Length",
            )
        )
        self.assertGreater(cap_length_items, 0)
        self.assertNotIn("1-Up Mushroom", self.world.item_name_to_id)
        slot_data = self.world.fill_slot_data()
        cap_length_counts = [
            slot_data["WingCapLengthItemCount"],
            slot_data["MetalCapLengthItemCount"],
            slot_data["VanishCapLengthItemCount"],
        ]
        self.assertEqual(sum(cap_length_counts), cap_length_items)
        self.assertLessEqual(max(cap_length_counts) - min(cap_length_counts), 1)
        self.assertNotIn("Power Star", {item.name for item in self.multiworld.get_items()})


# Entrance + Move Randos
class CourseEntrancesMoveTestBase(SM64TestBase):
    options = {
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "area_rando": Options.AreaRandomizer.option_Courses_Only
    }

    def test_BoB_entrance(self):
        bob_level_id = sm64_entrances_to_level["Bob-omb Battlefield"]
        # BoB goes to a course, not a secret.
        self.assertNotIn(self.world.area_connections[bob_level_id], sm64_level_to_secrets.keys())
        self.assertIn(self.world.area_connections[bob_level_id], sm64_level_to_paintings.keys())

    def test_BitFS_entrance(self):
        bitfs_level_id = sm64_entrances_to_level["Bowser in the Fire Sea"]
        # BitFS is a secret (aka not a course), unaffected by Course Only entrance rando.
        self.assertEqual(self.world.area_connections[bitfs_level_id], bitfs_level_id)

    def test_starting_state_has_reachable_check(self):
        self.assertTrue(world_has_two_reachable_starting_checks(self))


class CourseEntrancesLockedPaintingsMoveTestBase(SM64TestBase):
    options = {
        "level_unlocks": Options.LevelUnlocks.option_full,
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "area_rando": Options.AreaRandomizer.option_Courses_Only
    }

    def test_starting_state_has_reachable_check(self):
        self.assertTrue(world_has_two_reachable_starting_checks(self))


class SeparateEntrancesMoveTestBase(SM64TestBase):
    options = {
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "area_rando": Options.AreaRandomizer.option_Courses_and_Secrets_Separate
    }

    def test_BoB_entrance(self):
        bob_level_id = sm64_entrances_to_level["Bob-omb Battlefield"]
        # BoB goes to a course, not a secret.
        self.assertNotIn(self.world.area_connections[bob_level_id], sm64_level_to_secrets.keys())
        self.assertIn(self.world.area_connections[bob_level_id], sm64_level_to_paintings.keys())

    def test_BitFS_entrance(self):
        bitfs_level_id = sm64_entrances_to_level["Bowser in the Fire Sea"]
        # BitFS does not go to DDD.
        self.assertIsNot(self.world.area_connections[bitfs_level_id], sm64_entrances_to_level["Dire, Dire Docks"])

    def test_starting_state_has_reachable_check(self):
        self.assertTrue(world_has_two_reachable_starting_checks(self))


class LockedPaintingsSeparateEntrancesMoveTestBase(SM64TestBase):
    options = {
        "level_unlocks": Options.LevelUnlocks.option_full,
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "area_rando": Options.AreaRandomizer.option_Courses_and_Secrets_Separate
    }

    def test_starting_sources_have_reachable_checks(self):
        self.assertTrue(world_has_two_reachable_starting_checks(self))


class AllEntrancesMoveTestBase(SM64TestBase):
    options = {
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "area_rando": Options.AreaRandomizer.option_Courses_and_Secrets
    }

    def test_BoB_entrance(self):
        self.assertIn(sm64_entrances_to_level["Bob-omb Battlefield"], self.world.area_connections)

    def test_BitFS_entrance(self):
        bitfs_level_id = sm64_entrances_to_level["Bowser in the Fire Sea"]
        # BitFS does not go to DDD.
        self.assertIsNot(self.world.area_connections[bitfs_level_id], sm64_entrances_to_level["Dire, Dire Docks"])

    def test_starting_state_has_reachable_check(self):
        self.assertTrue(world_has_two_reachable_starting_checks(self))

    def test_CotMC_entrance(self):
        cotmc_level_id = sm64_entrances_to_level["Cavern of the Metal Cap"]
        # CotMC does not go to HMC.
        self.assertIsNot(self.world.area_connections[cotmc_level_id], sm64_entrances_to_level["Hazy Maze Cave"])
        # If BitFS -> HMC, CotMC does not go to DDD.
        bitfs_level_id = sm64_entrances_to_level["Bowser in the Fire Sea"]
        if self.world.area_connections[bitfs_level_id] == sm64_entrances_to_level["Hazy Maze Cave"]:
            self.assertIsNot(self.world.area_connections[cotmc_level_id], sm64_entrances_to_level["Dire, Dire Docks"])


# No Strict Requirements
class NoStrictRequirementsTestBase(SM64TestBase):
    options = {
        **SHUFFLED_GLOBAL_MOVE_OPTIONS,
        "buddy_checks": Options.BuddyChecks.option_true,
    }
