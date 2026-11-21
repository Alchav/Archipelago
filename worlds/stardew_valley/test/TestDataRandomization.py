from .bases import SVTestBase
from ..data.requirement import SkillRequirement, MasteryRequirement
from ..data.shop import ShopSource
from ..options.options import DataRandomization, DataRandomizationBehavior
from ..strings.region_names import Region
from ..strings.skill_names import Skill
from ..strings.tool_names import FishingRod


class TestCohesiveFishDeterminism(SVTestBase):
    options = {
        DataRandomization.internal_name: frozenset({
            "Cohesive Fish", "Fish Catch Method", "Fish Difficulty", "Fish Location",
            "Fish Season", "Fish Weather", "Fish Sell Price",
        }),
    }

    def test_cohesive_data_is_repeatable_for_every_behavior(self):
        from copy import copy
        from random import Random
        from ..content import create_content
        from ..data_randomization.randomized_data_writer import prepare_randomized_data

        options = copy(self.world.options)
        options.data_randomization_behavior = DataRandomizationBehavior(1)
        for behavior in range(1, 6):
            with self.subTest(behavior=behavior):
                options.data_randomization_behavior.value = behavior
                first = create_content(options, Random(172))
                # Keep allocations alive so a new content build gets different addresses.
                allocations = [object() for _ in range(10000)]
                second = create_content(options, Random(172))
                self.assertEqual(prepare_randomized_data(first, options),
                                 prepare_randomized_data(second, options))
                self.assertEqual(len(allocations), 10000)

    def test_legacy_order_is_repeatable_and_affects_randomization(self):
        from copy import copy
        from random import Random
        from ..content import create_content
        from ..data_randomization.randomized_data_writer import prepare_randomized_data

        from ..options import DataRandomizationFishOrder
        options = copy(self.world.options)
        options.data_randomization_behavior = DataRandomizationBehavior(DataRandomizationBehavior.option_shuffled)
        options.data_randomization_fish_order = DataRandomizationFishOrder([])
        first = create_content(options, Random(172))
        options.data_randomization_fish_order.value = sorted(first.fishes, reverse=True)
        recovered = create_content(options, Random(172))
        repeated = create_content(options, Random(172))
        self.assertNotEqual(prepare_randomized_data(first, options),
                            prepare_randomized_data(recovered, options))
        self.assertEqual(prepare_randomized_data(recovered, options),
                         prepare_randomized_data(repeated, options))


class TestDataRandomizationRequirements(SVTestBase):
    options = {
        DataRandomization.internal_name: DataRandomization.preset_all,
        DataRandomizationBehavior.internal_name: DataRandomizationBehavior.option_randomized
    }

    def test_training_bamboo_rod_requirements(self):
        content = self.world.content
        tools = content.tool_upgrades
        rods = [FishingRod.training, FishingRod.bamboo]
        for rod_name in rods:
            with self.subTest(rod_name):
                rod = tools[rod_name]
                for source in rod.sources:
                    if isinstance(source, ShopSource):
                        self.assertEqual(source.shop_region, Region.fish_shop)
                        self.assertEqual(len(source.other_requirements), 0)
                        return
                self.fail(f"{rod_name} should have a ShopSource with no other requirements")

    def test_fiberglass_iridium_rod_requirements(self):
        content = self.world.content
        tools = content.tool_upgrades
        rods = [FishingRod.fiberglass, FishingRod.iridium]
        for rod_name in rods:
            with self.subTest(rod_name):
                rod = tools[rod_name]
                for source in rod.sources:
                    if isinstance(source, ShopSource):
                        self.assertEqual(source.shop_region, Region.fish_shop)
                        self.assertEqual(len(source.other_requirements), 1)
                        other_requirement = source.other_requirements[0]
                        if isinstance(other_requirement, SkillRequirement):
                            self.assertTrue(other_requirement.skill == Skill.fishing)
                            level = 2 if rod_name == FishingRod.fiberglass else 6
                            self.assertTrue(other_requirement.level == level)
                            return
                        self.fail(f"{rod_name} should have a SkillRequirement")
                self.fail(f"{rod_name} should have a ShopSource with a SkillRequirement")

    def test_advanced_iridium_rod_requirements(self):
        content = self.world.content
        tools = content.tool_upgrades
        rod_name = FishingRod.advanced_iridium
        rod = tools[rod_name]
        for source in rod.sources:
            if isinstance(source, ShopSource):
                self.assertEqual(source.shop_region, Region.fish_shop)
                self.assertEqual(len(source.other_requirements), 1)
                other_requirement = source.other_requirements[0]
                if isinstance(other_requirement, MasteryRequirement):
                    self.assertTrue(other_requirement.skill == Skill.fishing)
                    return
                self.fail(f"{rod_name} should have a MasteryRequirement")
        self.fail(f"{rod_name} should have a ShopSource with a MasteryRequirement")
