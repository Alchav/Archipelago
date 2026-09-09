from ..bases import SM64TestBase
from ... import Options


class TestCastleLocations(SM64TestBase):
    run_default_tests = False
    options = {
                "blocksanity": Options.Blocksanity.option_true,
        "one_up_checks": Options.OneUpChecks.option_true,
        "one_up_unlocks": Options.OneUpUnlocks.option_not_shuffled,
        "combined_progressive_keys": Options.CombinedProgressiveKeys.option_false,
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

    def test_locations(self):
        basement = ["Progressive Basement Key"]
        second_floor = ["Progressive Upstairs Key"]
        third_floor = ["Progressive Upstairs Key", "Progressive Upstairs Key"]

        self.run_location_tests([
            ["Castle Basement - Toad", False, basement],
            ["Castle Basement - Toad", True, basement + ["Castle - Toads"]],
            ["Castle Second Floor - Toad", False, second_floor],
            ["Castle Second Floor - Toad", True, second_floor + ["Castle - Toads"]],
            ["Castle Third Floor - Toad", False, third_floor],
            ["Castle Third Floor - Toad", True, third_floor + ["Castle - Toads"]],

            ["Castle Basement - MIPS 1", False, basement + ["Dive"]],
            ["Castle Basement - MIPS 1", True, basement + ["Dive", "Castle - Progressive MIPS"]],
            ["Castle Basement - MIPS 2", False, basement + ["Dive", "Castle - Progressive MIPS"]],
            ["Castle Basement - MIPS 2", True,
             basement + ["Dive", "Castle - Progressive MIPS", "Castle - Progressive MIPS"]],

            ["Castle Grounds - Yoshi", False, ["Castle - Yoshi"]],
            ["Castle Grounds - Yoshi", False, ["Castle - Cannon Unlock"]],
            ["Castle Grounds - Yoshi", True, ["Castle - Cannon Unlock", "Castle - Yoshi"]],
            ["Castle Grounds - Roof Back 1-Up", False, []],
            ["Castle Grounds - Roof Back 1-Up", True, ["Castle - Cannon Unlock"]],
            ["Castle Grounds - Roof Center 1-Up", False, []],
            ["Castle Grounds - Roof Center 1-Up", True, ["Castle - Cannon Unlock"]],
            ["Castle Grounds - Roof Front 1-Up", False, []],
            ["Castle Grounds - Roof Front 1-Up", True, ["Castle - Cannon Unlock"]],
            ["Castle Grounds - Roof Wing Cap Block", False, ["Castle - Cannon Unlock"]],
            ["Castle Grounds - Roof Wing Cap Block", True, ["Castle - Cannon Unlock", "Castle - Wing Cap"]],

            ["Castle Grounds - Third Tree From Waterfall 1-Up", False, []],
            ["Castle Grounds - Third Tree From Waterfall 1-Up", True, ["Climb"]],
            ["Castle Basement - Drain the Moat", False, []],
            ["Castle Basement - Drain the Moat", False, basement],
            ["Castle Basement - Drain the Moat", True, basement + ["Ground Pound"]],
            ["Castle Grounds - Bridge Coins 1-Up", False, basement + ["Ground Pound", "Wall Kick"]],
            ["Castle Grounds - Bridge Coins 1-Up", True,
             basement + ["Ground Pound", "Wall Kick", "Triple Jump"]],
            ["Castle Grounds - Left Butterfly 1-Up", True, []],
            ["Castle Grounds - Right Butterfly 1-Up", True, []],
            ["Castle First Floor - Jolly Roger Bay Room 1-Up", False, []],
            ["Castle First Floor - Jolly Roger Bay Room 1-Up", True, ["Side Flip"]],
            ["Castle Basement - Water Tunnel Four Corners 1-Up", False, []],
            ["Castle Basement - Water Tunnel Four Corners 1-Up", True, basement],
        ], starting_regions=["Castle Grounds"])

    def test_dynamic_starting_checks_are_in_the_lobby(self):
        active_locations = {
            location.name: location
            for location in self.multiworld.get_locations(self.player)
        }
        for location_name in (
                "Castle First Floor - Free Item",
                "Castle First Floor - Another Free Item",
        ):
            if location_name in active_locations:
                self.assertEqual(active_locations[location_name].parent_region.name, "Castle First Floor")
