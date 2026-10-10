import math
import unittest
from collections import defaultdict
from fractions import Fraction

from test.general import setup_multiworld

from . import Factorio
from .CraftSanity import (CRAFTSANITY_PRODUCTS, MAX_CHECKS_PER_PRODUCT, MAX_CRAFTSANITY_LOCATIONS,
                          ROCKET_PARTS_PER_LAUNCH, expand_product, location_name, make_thresholds)
from .Locations import location_table


class TestCraftsanityHelpers(unittest.TestCase):
    def test_static_location_reservation(self) -> None:
        self.assertEqual(len(CRAFTSANITY_PRODUCTS), 192)
        reserved = {
            location_name(product, ordinal)
            for product in CRAFTSANITY_PRODUCTS
            for ordinal in range(1, MAX_CHECKS_PER_PRODUCT + 1)
        }
        self.assertEqual(len(reserved), 19_200)
        self.assertTrue(reserved.issubset(location_table))

    def test_recipe_output_is_apportioned_per_item(self) -> None:
        contributions = defaultdict(list)
        expand_product(contributions, "copper-cable", Fraction(1), None, frozenset(), {})
        self.assertEqual(sum(entry.amount for entry in contributions["copper-plate"]), Fraction(1, 2))
        self.assertEqual(sum(entry.amount for entry in contributions["copper-ore"]), Fraction(1, 2))

    def test_final_threshold_is_always_the_full_expected_count(self) -> None:
        maximum = Fraction(49_355)
        thresholds = make_thresholds(maximum, MAX_CHECKS_PER_PRODUCT)
        self.assertEqual(thresholds[-1], 49_355)
        self.assertEqual(len(thresholds), len(set(thresholds)))


class TestCraftsanityWorld(unittest.TestCase):
    def test_maximum_option_creates_exactly_3000_locations(self) -> None:
        multiworld = setup_multiworld(Factorio, seed=1, options={"craftsanity": MAX_CRAFTSANITY_LOCATIONS})
        world = multiworld.worlds[1]

        self.assertEqual(len(world.craftsanity_locations), MAX_CRAFTSANITY_LOCATIONS)
        self.assertEqual(len({location.address for location in world.craftsanity_locations}),
                         MAX_CRAFTSANITY_LOCATIONS)
        self.assertEqual(len(multiworld.itempool), len(multiworld.get_unfilled_locations()))

        by_product = {}
        for location in world.craftsanity_locations:
            by_product.setdefault(location.crafted_item, []).append(location)
        self.assertTrue(by_product["iron-ore"][0].production_statistic)
        self.assertFalse(by_product["electronic-circuit"][0].production_statistic)
        self.assertEqual(math.ceil(sum(
            contribution.amount for contribution in world.craftsanity_contributions["rocket-part"]
        )), ROCKET_PARTS_PER_LAUNCH)
        for product, locations in by_product.items():
            expected_maximum = math.ceil(sum(
                contribution.amount for contribution in world.craftsanity_contributions[product]
            ))
            self.assertEqual(locations[-1].count, expected_maximum)


if __name__ == "__main__":
    unittest.main()
