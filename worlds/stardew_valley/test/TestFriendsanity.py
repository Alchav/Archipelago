from collections import Counter
from typing import ClassVar, Set

from . import SVTestBase
from ..content.feature import friendsanity
from ..options import Friendsanity, FriendsanityHeartSize

all_vanilla_bachelor = {
    "Harvey", "Elliott", "Sam", "Alex", "Shane", "Sebastian", "Emily", "Haley", "Leah", "Abigail", "Penny", "Maru"
}

all_vanilla_starting_npc = {
    "Alex", "Elliott", "Harvey", "Sam", "Sebastian", "Shane", "Abigail", "Emily", "Haley", "Leah", "Maru", "Penny", "Caroline", "Clint", "Demetrius", "Evelyn",
    "George", "Gus", "Jas", "Jodi", "Lewis", "Linus", "Marnie", "Pam", "Pierre", "Robin", "Vincent", "Willy", "Wizard", "Pet",
}

all_vanilla_npc = {
    "Alex", "Elliott", "Harvey", "Sam", "Sebastian", "Shane", "Abigail", "Emily", "Haley", "Leah", "Maru", "Penny", "Caroline", "Clint", "Demetrius", "Evelyn",
    "George", "Gus", "Jas", "Jodi", "Lewis", "Linus", "Marnie", "Pam", "Pierre", "Robin", "Vincent", "Willy", "Wizard", "Pet", "Sandy", "Dwarf", "Kent", "Leo",
    "Krobus"
}


class SVFriendsanityTestBase(SVTestBase):
    expected_npcs: ClassVar[Set[str]] = {}
    expected_pet_heart_size: ClassVar[Set[str]] = {}
    expected_bachelor_heart_size: ClassVar[Set[str]] = {}
    expected_other_heart_size: ClassVar[Set[str]] = {}

    @property
    def run_test(self):
        return type(self) is not SVFriendsanityTestBase

    @property
    def run_default_tests(self) -> bool:
        return self.run_test and super().run_default_tests

    def test_friendsanity(self):
        if not self.run_test:
            return

        with self.subTest("Items are valid"):
            self.check_all_items_match_expected_npcs()
        with self.subTest("Correct number of items"):
            self.check_correct_number_of_items()
        with self.subTest("Locations are valid"):
            self.check_all_locations_match_expected_npcs()
        with self.subTest("Locations heart size are valid"):
            self.check_all_locations_match_heart_size()

    def check_all_items_match_expected_npcs(self):
        for item in self.multiworld.itempool:
            name = friendsanity.extract_npc_from_item_name(item.name)
            if name is None:
                continue

            self.assertIn(name, self.expected_npcs)

    def check_correct_number_of_items(self):
        item_by_npc = Counter()
        for item in self.multiworld.itempool:
            name = friendsanity.extract_npc_from_item_name(item.name)
            if name is None:
                continue

            item_by_npc[name] += 1

        for name, count in item_by_npc.items():

            if name == "Pet":
                self.assertEqual(count, len(self.expected_pet_heart_size))
            elif self.world.content.villagers[name].bachelor:
                self.assertEqual(count, len(self.expected_bachelor_heart_size))
            else:
                self.assertEqual(count, len(self.expected_other_heart_size))

    def check_all_locations_match_expected_npcs(self):
        for location_name in self.get_real_location_names():
            name, _ = friendsanity.extract_npc_from_location_name(location_name)
            if name is None:
                continue

            self.assertIn(name, self.expected_npcs)

    def check_all_locations_match_heart_size(self):
        for location_name in self.get_real_location_names():
            name, heart_size = friendsanity.extract_npc_from_location_name(location_name)
            if name is None:
                continue

            if name == "Pet":
                self.assertIn(heart_size, self.expected_pet_heart_size)
            elif self.world.content.villagers[name].bachelor:
                self.assertIn(heart_size, self.expected_bachelor_heart_size)
            else:
                self.assertIn(heart_size, self.expected_other_heart_size)


class TestFriendsanityNone(SVFriendsanityTestBase):
    options = {
        Friendsanity.internal_name: Friendsanity.option_none,
    }

    @property
    def run_default_tests(self) -> bool:
        # None is default
        return False


class TestFriendsanityBachelors(SVFriendsanityTestBase):
    options = {
        Friendsanity.internal_name: Friendsanity.option_bachelors,
        FriendsanityHeartSize.internal_name: 1,
    }
    expected_npcs = all_vanilla_bachelor
    expected_bachelor_heart_size = set(range(1, 8 + 1))


class TestFriendsanityStartingNpcs(SVFriendsanityTestBase):
    options = {
        Friendsanity.internal_name: Friendsanity.option_starting_npcs,
        FriendsanityHeartSize.internal_name: 1,
    }
    expected_npcs = all_vanilla_starting_npc
    expected_pet_heart_size = set(range(1, 5 + 1))
    expected_bachelor_heart_size = set(range(1, 8 + 1))
    expected_other_heart_size = set(range(1, 10 + 1))


class TestFriendsanityAllNpcs(SVFriendsanityTestBase):
    options = {
        Friendsanity.internal_name: Friendsanity.option_all,
        FriendsanityHeartSize.internal_name: 4,
    }
    expected_npcs = all_vanilla_npc
    expected_pet_heart_size = set(range(4, 5 + 1, 4)) | {5}
    expected_bachelor_heart_size = set(range(4, 8 + 1, 4)) | {8}
    expected_other_heart_size = set(range(4, 10 + 1, 4)) | {10}


class TestFriendsanityHeartSize3(SVFriendsanityTestBase):
    options = {
        Friendsanity.internal_name: Friendsanity.option_all_with_marriage,
        FriendsanityHeartSize.internal_name: 3,
    }
    expected_npcs = all_vanilla_npc
    expected_pet_heart_size = set(range(3, 5 + 1, 3)) | {5}
    expected_bachelor_heart_size = set(range(3, 14 + 1, 3)) | {14}
    expected_other_heart_size = set(range(3, 10 + 1, 3)) | {10}


class TestFriendsanityHeartSize5(SVFriendsanityTestBase):
    options = {
        Friendsanity.internal_name: Friendsanity.option_all_with_marriage,
        FriendsanityHeartSize.internal_name: 5,
    }
    expected_npcs = all_vanilla_npc
    expected_pet_heart_size = set(range(5, 5 + 1, 5)) | {5}
    expected_bachelor_heart_size = set(range(5, 14 + 1, 5)) | {14}
    expected_other_heart_size = set(range(5, 10 + 1, 5)) | {10}
