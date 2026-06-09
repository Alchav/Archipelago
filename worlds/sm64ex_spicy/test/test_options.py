from .bases import SM64TestBase
from Options import OptionError
from .. import Options
from ..Items import arbitrary_item_data_table, cap_item_data_table, castle_key_item_data_table, \
    castle_progression_item_data_table, feature_item_data_table, generic_item_data_table, global_cap_item_names
from ..Locations import loc100Coin_table, location_table
from ..Music import SM64_MUSIC_AREA_SEQUENCES, SM64_MUSIC_SAFE_SEQUENCE_IDS
from ..Regions import SM64_TTC_FAST, SM64_TTC_RANDOM, SM64_TTC_SLOW, SM64_TTC_STOPPED, SM64_WDW_HIGH, \
    SM64_WDW_LOW, SM64_WDW_MIDDLE, sm64_entrances_to_level, sm64_level_to_paintings, sm64_level_to_secrets


def world_has_reachable_starting_check(test_base: SM64TestBase, allowed_source_entrances=None) -> bool:
    from ..Rules import has_reachable_starting_check
    return has_reachable_starting_check(
        test_base.multiworld, test_base.world.options, test_base.player, allowed_source_entrances)

wdw_variant_ids = {SM64_WDW_LOW, SM64_WDW_MIDDLE, SM64_WDW_HIGH}
ttc_variant_ids = {SM64_TTC_STOPPED, SM64_TTC_SLOW, SM64_TTC_RANDOM, SM64_TTC_FAST}


class FeatureItemPoolTestBase(SM64TestBase):
    def test_yoshi_location_id(self):
        self.assertEqual(location_table["Yoshi"], 3626244)

    def test_item_ids_match_client_doc(self):
        expected_ids = {
            "Bob-omb Battlefield - King Bob-omb": 3626245,
            "Bob-omb Battlefield - Koopa the Quick": 3626246,
            "Bob-omb Battlefield - Bob-omb Buddy": 3626247,
            "Whomp's Fortress - Whomp King": 3626248,
            "Whomp's Fortress - Fortress": 3626249,
            "Whomp's Fortress - Bob-omb Buddy": 3626250,
            "Whomp's Fortress - Hoot": 3626251,
            "Cool, Cool Mountain - Snowman's Head": 3626252,
            "Cool, Cool Mountain - Big Penguin": 3626253,
            "Jolly Roger Bay - Sunken Ship": 3626254,
            "Jolly Roger Bay - Raised Ship": 3626255,
            "Jolly Roger Bay - Bob-omb Buddy": 3626256,
            "Jolly Roger Bay - Jet Stream": 3626257,
            "Jolly Roger Bay - Unagi": 3626258,
            "Lethal Lava Land - Koopa Shell": 3626259,
            "Shifting Sand Land - Klepto Star": 3626260,
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
            "Progressive MIPS": 3626271,
            "Wing Cap Light": 3626272,
            "Courtyard Boos": 3626273,
            "Castle Toads": 3626274,
            "Cannon Unlock - Castle": 3626275,
            "Yoshi": 3626276,
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
        }
        item_data = {
            **feature_item_data_table,
            **castle_key_item_data_table,
            **castle_progression_item_data_table,
            **cap_item_data_table,
            **arbitrary_item_data_table,
            **{item_name: generic_item_data_table[item_name] for item_name in global_cap_item_names},
        }
        self.assertEqual({name: data.code for name, data in item_data.items()}, expected_ids)

    def test_feature_items_are_generated(self):
        for item_name in feature_item_data_table:
            with self.subTest("Feature item generated", item=item_name):
                self.assertEqual(len(self.get_items_by_name(item_name)), 1)

    def test_arbitrary_items_are_generated(self):
        for item_name in arbitrary_item_data_table:
            with self.subTest("Arbitrary item generated", item=item_name):
                self.assertEqual(len(self.get_items_by_name(item_name)), 1)

    def test_castle_progression_items_are_generated(self):
        self.assertEqual(len(self.get_items_by_name("Progressive Key")), 6)
        self.assertEqual(len(self.get_items_by_name("Progressive MIPS")), 2)
        for item_name in castle_progression_item_data_table:
            if item_name != "Progressive MIPS":
                with self.subTest("Castle progression item generated", item=item_name):
                    self.assertEqual(len(self.get_items_by_name(item_name)), 1)

    def test_default_global_cap_items_are_generated(self):
        for item_name in global_cap_item_names:
            with self.subTest("Global cap item generated", item=item_name):
                self.assertEqual(len(self.get_items_by_name(item_name)), 1)

    def test_default_per_level_cap_items_are_not_generated(self):
        for item_name in cap_item_data_table:
            with self.subTest("Per-level cap item not generated", item=item_name):
                self.assertEqual(len(self.get_items_by_name(item_name)), 0)

    def test_old_keys_are_not_generated(self):
        self.assertEqual(len(self.get_items_by_name("Basement Key")), 0)
        self.assertEqual(len(self.get_items_by_name("Second Floor Key")), 0)


class PerLevelCapItemPoolTestBase(SM64TestBase):
    options = {
        "per_level_cap_items": Options.PerLevelCapItems.option_true,
    }

    def test_per_level_cap_items_are_generated(self):
        for item_name in cap_item_data_table:
            with self.subTest("Per-level cap item generated", item=item_name):
                self.assertEqual(len(self.get_items_by_name(item_name)), 1)

    def test_global_cap_items_are_not_generated(self):
        for item_name in global_cap_item_names:
            with self.subTest("Global cap item not generated", item=item_name):
                self.assertEqual(len(self.get_items_by_name(item_name)), 0)


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
        "mario_colors": {
            "shirt": [1, 2, 3],
            "hair": [4, 5, 6],
        }
    }

    def test_mario_colors_slot_data(self):
        self.assertEqual(self.world.fill_slot_data()["MarioColors"], {
            "shirt": [1, 2, 3],
            "hair": [4, 5, 6],
        })


class MarioColorsValidationTestBase(SM64TestBase):
    auto_construct = False

    def assert_mario_colors_invalid(self, value):
        option = Options.MarioColors.from_any(value)
        with self.assertRaises(OptionError):
            option.verify(None, "Tester", None)

    def test_unknown_color_key_is_invalid(self):
        self.assert_mario_colors_invalid({"unknown": [1, 2, 3]})

    def test_color_channels_must_be_rgb_triplets(self):
        self.assert_mario_colors_invalid({"shirt": [1, 2]})

    def test_color_channels_must_be_ints(self):
        self.assert_mario_colors_invalid({"shirt": [True, 2, 3]})

    def test_color_channels_must_be_in_range(self):
        self.assert_mario_colors_invalid({"shirt": [256, 2, 3]})


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
            Options.DireDireDocksCoinStarRequirement: 106,
            Options.SnowmansLandCoinStarRequirement: 127,
            Options.TallTallMountainCoinStarRequirement: 137,
            Options.TinyHugeIslandCoinStarRequirement: 191,
        }
        for option in Options.coin_star_requirement_options:
            with self.subTest(option=option.__name__):
                self.assertEqual(option.range_start, 1)
                self.assertEqual(option.range_end, expected_range_ends.get(option, 100))


# Coin Star Logic
class EnableCoinStarsTestBase(SM64TestBase):
    options = {
        "enable_coin_stars": Options.EnableCoinStars.option_true
    }

    # Ensure Coin Star locations are created
    def test_coin_star_locations(self):
        possible_locations = self.world.location_names
        for loc in loc100Coin_table:
            # Use subtest to force all locations to be tested
            with self.subTest("Location created", location=loc):
                self.assertIn(loc, possible_locations)


class DisableCoinStarsTestBase(SM64TestBase):
    options = {
        "enable_coin_stars": Options.EnableCoinStars.option_false
    }

    # Ensure Coin Star locations are not created
    def test_coin_star_locations(self):
        possible_locations = self.world.get_locations()
        for loc in loc100Coin_table:
            # Use subtest to force all locations to be tested
            with self.subTest("Location not created", location=loc):
                self.assertNotIn(loc, possible_locations)


# Exclamation Boxes
class ExclamationBoxesOnTestBase(SM64TestBase):
    options = {
        "exclamation_boxes": Options.ExclamationBoxes.option_true,
    }


class ExclamationBoxesOffTestBase(SM64TestBase):
    options = {
        "exclamation_boxes": Options.ExclamationBoxes.option_false,
    }

    # Should populate the boxes with the players own 1Up Mushrooms
    def test_items_in_exclamation_box_locations(self):
        # Get 1Up Block locations
        loc1ups_table = {name for name in location_table.keys() if "1Up Block" in name}
        for loc in loc1ups_table:
            # Use subtest to force all locations to be tested
            with self.subTest("Location has own 1Up Mushroom.", location=loc):
                item_in_loc = self.world.get_location(loc).item
                self.assertEqual(item_in_loc.name, "1Up Mushroom")
                # By default, these test bases are single player multiworld.
                # In any other case, we should test that they belong to their respective worlds.


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

    def test_princess_slide_source_has_reachable_check(self):
        self.assertTrue(world_has_reachable_starting_check(self, ("The Princess's Secret Slide",)))


class EntranceRandoOffLockedPaintingsTestBase(SM64TestBase):
    options = {
        "area_rando": Options.AreaRandomizer.option_Off,
        "enable_locked_paintings": Options.EnableLockedPaintings.option_true,
        "enable_move_rando": Options.EnableMoveRandomizer.option_true,
    }

    def test_all_entrances_are_vanilla(self):
        for entrance_level_id in {*sm64_level_to_paintings, *sm64_level_to_secrets}:
            with self.subTest("Entrance maps to itself", entrance=entrance_level_id):
                self.assertEqual(self.world.area_connections[entrance_level_id], entrance_level_id)

    def test_princess_slide_source_has_reachable_check(self):
        self.assertTrue(world_has_reachable_starting_check(self, ("The Princess's Secret Slide",)))


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

    def test_princess_slide_source_has_reachable_check(self):
        self.assertTrue(world_has_reachable_starting_check(self, ("The Princess's Secret Slide",)))


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


class CompletionAllBowserTestBase(SM64TestBase):
    options = {
        "completion_type": Options.CompletionType.option_All_Bowser_Stages
    }


# Option Combos


# Power Star item generation
class NoPowerStarsTestBase(SM64TestBase):
    options = {
        "enable_move_rando": Options.EnableMoveRandomizer.option_true,
        "exclamation_boxes": Options.ExclamationBoxes.option_false,
        "enable_coin_stars": Options.EnableCoinStars.option_false
    }

    def test_no_power_stars_generated(self):
        self.assertGreater(len(self.get_items_by_name("1Up Mushroom")), 0)
        self.assertNotIn("Power Star", {item.name for item in self.multiworld.get_items()})


# Entrance + Move Randos
class CourseEntrancesMoveTestBase(SM64TestBase):
    options = {
        "enable_move_rando": Options.EnableMoveRandomizer.option_true,
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
        self.assertTrue(world_has_reachable_starting_check(self))


class CourseEntrancesLockedPaintingsMoveTestBase(SM64TestBase):
    options = {
        "enable_locked_paintings": Options.EnableLockedPaintings.option_true,
        "enable_move_rando": Options.EnableMoveRandomizer.option_true,
        "area_rando": Options.AreaRandomizer.option_Courses_Only
    }

    def test_starting_state_has_reachable_check(self):
        self.assertTrue(world_has_reachable_starting_check(self))

    def test_princess_slide_source_has_reachable_check(self):
        self.assertTrue(world_has_reachable_starting_check(self, ("The Princess's Secret Slide",)))


class SeparateEntrancesMoveTestBase(SM64TestBase):
    options = {
        "enable_move_rando": Options.EnableMoveRandomizer.option_true,
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
        self.assertTrue(world_has_reachable_starting_check(self))


class LockedPaintingsSeparateEntrancesMoveTestBase(SM64TestBase):
    options = {
        "enable_locked_paintings": Options.EnableLockedPaintings.option_true,
        "enable_move_rando": Options.EnableMoveRandomizer.option_true,
        "area_rando": Options.AreaRandomizer.option_Courses_and_Secrets_Separate
    }

    def test_starting_sources_have_reachable_checks(self):
        self.assertTrue(world_has_reachable_starting_check(self))


class AllEntrancesMoveTestBase(SM64TestBase):
    options = {
        "enable_move_rando": Options.EnableMoveRandomizer.option_true,
        "area_rando": Options.AreaRandomizer.option_Courses_and_Secrets
    }

    def test_BoB_entrance(self):
        self.assertIn(sm64_entrances_to_level["Bob-omb Battlefield"], self.world.area_connections)

    def test_BitFS_entrance(self):
        bitfs_level_id = sm64_entrances_to_level["Bowser in the Fire Sea"]
        # BitFS does not go to DDD.
        self.assertIsNot(self.world.area_connections[bitfs_level_id], sm64_entrances_to_level["Dire, Dire Docks"])

    def test_starting_state_has_reachable_check(self):
        self.assertTrue(world_has_reachable_starting_check(self))

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
        "enable_move_rando": Options.EnableMoveRandomizer.option_true,
        "buddy_checks": Options.BuddyChecks.option_true,
        "strict_move_requirements": Options.StrictMoveRequirements.option_false,
        "strict_cap_requirements": Options.StrictCapRequirements.option_false,
        "strict_cannon_requirements": Options.StrictCannonRequirements.option_false,
    }
