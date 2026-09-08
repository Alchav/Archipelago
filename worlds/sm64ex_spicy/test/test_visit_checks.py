from .. import Options
from ..Locations import locVisit_table
from .bases import SM64TestBase


class VisitChecksOffTest(SM64TestBase):
    options = {"visit_checks": Options.VisitChecks.option_false}

    def test_visit_locations_are_not_created(self):
        active_locations = {location.name for location in self.multiworld.get_locations(self.player)}
        self.assertTrue(active_locations.isdisjoint(locVisit_table))


class VisitChecksOnTest(SM64TestBase):
    options = {"visit_checks": Options.VisitChecks.option_true}

    def test_visit_checks_are_preserved_in_slot_data(self):
        self.assertEqual(
            Options.VisitChecks.option_true,
            self.world.fill_slot_data()["Options"]["visit_checks"],
        )

    def test_all_visit_locations_are_created(self):
        active_locations = {location.name for location in self.multiworld.get_locations(self.player)}
        self.assertEqual(set(locVisit_table), active_locations & set(locVisit_table))

    def test_starting_castle_visits_are_reachable(self):
        for location_name in (
                "Castle Grounds - Visited",
                "Castle First Floor - Visited",
                "Castle Courtyard - Visited",
        ):
            with self.subTest(location=location_name):
                self.assertTrue(self.multiworld.get_location(location_name, self.player).can_reach(
                    self.multiworld.state))

    def test_castle_floor_visits_match_loaded_zones(self):
        self.assertEqual(
            "Castle Second Floor",
            self.multiworld.get_location("Castle Second Floor - Visited", self.player).parent_region.name,
        )
        self.assertNotIn("Castle Third Floor - Visited", locVisit_table)

    def test_pyramid_visit_is_reachable_from_both_entrances(self):
        location = self.multiworld.get_location("Shifting Sand Land - Pyramid Visited", self.player)
        self.assertEqual("Shifting Sand Land - Pyramid", location.parent_region.name)
        self.assertTrue(any(
            entrance.parent_region.name == "Shifting Sand Land - Pyramid Top Entry"
            for entrance in location.parent_region.entrances
        ))

    def test_internal_area_boundaries_do_not_create_visits(self):
        self.assertNotIn("Dire, Dire Docks - Bowser's Sub Area Visited", locVisit_table)
        self.assertNotIn("Wet-Dry World - Downtown Visited", locVisit_table)
        self.assertNotIn("Tiny-Huge Island - Red Coin Cave Visited", locVisit_table)
        self.assertNotIn("Tiny-Huge Island - Wiggler's Cave Visited", locVisit_table)

    def test_thi_caves_share_one_visit(self):
        location = self.multiworld.get_location("Tiny-Huge Island - Cave Visited", self.player)
        self.assertEqual("Tiny-Huge Island - Cave Visit", location.parent_region.name)
        self.assertEqual(
            {"Tiny-Huge Island - Red Coin Cave", "Tiny-Huge Island - Wiggler's Cave"},
            {entrance.parent_region.name for entrance in location.parent_region.entrances},
        )
