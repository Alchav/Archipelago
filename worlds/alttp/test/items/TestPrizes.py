from typing import List

from BaseClasses import Item, Location
from test.bases import WorldTestBase


class TestPrizes(WorldTestBase):
    game = "A Link to the Past"

    def test_item_rules(self):
        prize_locations: List[Location] = [
            self.multiworld.get_location("Eastern Palace - Prize", 1),
            self.multiworld.get_location("Desert Palace - Prize", 1),
            self.multiworld.get_location("Tower of Hera - Prize", 1),
            self.multiworld.get_location("Palace of Darkness - Prize", 1),
            self.multiworld.get_location("Swamp Palace - Prize", 1),
            self.multiworld.get_location("Thieves\' Town - Prize", 1),
            self.multiworld.get_location("Skull Woods - Prize", 1),
            self.multiworld.get_location("Ice Palace - Prize", 1),
            self.multiworld.get_location("Misery Mire - Prize", 1),
            self.multiworld.get_location("Turtle Rock - Prize", 1),
        ]
        prize_items: List[Item] = [
            self.get_item_by_name("Pendant of Courage"),
            self.get_item_by_name("Pendant of Power"),
            self.get_item_by_name("Pendant of Wisdom"),
            self.get_item_by_name("Crystal (Palace of Darkness)"),
            self.get_item_by_name("Crystal (Swamp Palace)"),
            self.get_item_by_name("Crystal (Skull Woods)"),
            self.get_item_by_name("Crystal (Thieves' Town)"),
            self.get_item_by_name("Crystal (Ice Palace)"),
            self.get_item_by_name("Crystal (Misery Mire)"),
            self.get_item_by_name("Crystal (Turtle Rock)"),
        ]

        for item in self.multiworld.get_items():
            for prize_location in prize_locations:
                self.assertEqual(item in prize_items, prize_location.item_rule(item),
                                 f"{item} must {'' if item in prize_items else 'not '}be allowed in {prize_location}.")
