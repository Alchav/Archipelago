from .. import SohWorld
from ..Items import Items, SohItem
from ..Enums import EnemyDistance
from .bases import SohTestBase
from ..LogicHelpers import can_hit_at_range, can_attack, can_jump_slash, can_use_sword, can_jump_slash_except_hammer
from itertools import combinations

class TestCanHitAtRange(SohTestBase):
    """
    Test can_hit_at_range helper
    """
    options = {"shuffle_deku_nut_bag": True, "shuffle_deku_stick_bag": True, "closed_forest": 2, "door_of_time": 2, "shuffle_kokiri_sword": 1, "shuffle_master_sword": 1, "bombchu_bag": 1, "bombchu_drops": 1}

    def require_any_to_hit(self, items: list[Items], distance: EnemyDistance = EnemyDistance.CLOSE, wall_or_floor: bool = True, in_water: bool = False) -> None:
        # ideally we run these as subtests, but those are currently broken 
        # and report as Success if any subtest succeeds
        # (https://github.com/microsoft/vscode-python/issues/25824)

        self.sweep()
        self.remove_by_name(items)

        for size in range(1, len(items)):
            for valid_combo in combinations(items, size):
                self.collect_by_name(valid_combo)
                self.assertTrue(can_hit_at_range(self.get_bundle(), distance, wall_or_floor, in_water)._instantiate(self.world)._evaluate(self.multiworld.state), 
                                f"Wasn't able to hit, but should have been able to with only {valid_combo} at distance {str(distance.name)} {"on wall or floor" if wall_or_floor else "not on wall or floor"}")
                self.remove_by_name(valid_combo)
                

        self.collect_by_name(items)

        self.assertTrue(can_hit_at_range(self.get_bundle(), distance, wall_or_floor, in_water)._instantiate(self.world)._evaluate(self.multiworld.state), 
                        f"Wasn't able to hit, but should have been able to at distance {str(distance.name)} {"on wall or floor" if wall_or_floor else "not on wall or floor"}")
        
        self.remove_by_name(items)

    def can_not_hit_with_any(self, items: list[Items], distance: EnemyDistance = EnemyDistance.CLOSE, wall_or_floor: bool = True, in_water: bool = False) -> None:
        # ideally we run these as subtests, but those are currently broken 
        # and report as Success if any subtest succeeds
        # (https://github.com/microsoft/vscode-python/issues/25824)

        self.sweep()
        self.remove_by_name(items)

        for size in range(1, len(items)):
            for valid_combo in combinations(items, size):
                self.collect_by_name(valid_combo)
                self.assertFalse(can_hit_at_range(self.get_bundle(), distance, wall_or_floor, in_water)._instantiate(self.world)._evaluate(self.multiworld.state), 
                                f"Was able to hit, but should not have been able to with only {valid_combo} at distance {str(distance.name)} {"on wall or floor" if wall_or_floor else "not on wall or floor"}")
                self.remove_by_name(valid_combo)
                

        self.collect_by_name(items)

        self.assertFalse(can_hit_at_range(self.get_bundle(), distance, wall_or_floor, in_water)._instantiate(self.world)._evaluate(self.multiworld.state), 
                        f"Was able to hit, but should not have been able to at distance {str(distance.name)} {"on wall or floor" if wall_or_floor else "not on wall or floor"}")
        
        self.remove_by_name(items)

    def test_can_kill_at_range(self):

        self.assertFalse(can_hit_at_range(self.get_bundle(), EnemyDistance.CLOSE, True)._instantiate(self.world)._evaluate(self.multiworld.state), f'Could hit with nothing.')
        
        # Close
        items = [Items.MEGATON_HAMMER, Items.KOKIRI_SWORD, Items.MASTER_SWORD, Items.BIGGORONS_SWORD, Items.PROGRESSIVE_STICK_CAPACITY, 
                 Items.PROGRESSIVE_HOOKSHOT, Items.PROGRESSIVE_SLINGSHOT, Items.PROGRESSIVE_BOW]
        self.require_any_to_hit(items)

        # Short Jumpslash
        items = [Items.KOKIRI_SWORD, Items.MASTER_SWORD, Items.BIGGORONS_SWORD, Items.PROGRESSIVE_STICK_CAPACITY, 
                 Items.PROGRESSIVE_HOOKSHOT, Items.PROGRESSIVE_SLINGSHOT, Items.PROGRESSIVE_BOW]
        self.require_any_to_hit(items, EnemyDistance.SHORT_JUMPSLASH)

        # Master Sword Jumpslash
        items = [Items.MASTER_SWORD, Items.BIGGORONS_SWORD, Items.PROGRESSIVE_STICK_CAPACITY, 
                 Items.PROGRESSIVE_HOOKSHOT, Items.PROGRESSIVE_SLINGSHOT, Items.PROGRESSIVE_BOW]
        self.require_any_to_hit(items, EnemyDistance.MASTER_SWORD_JUMPSLASH)

        # Long Jumpslash
        items = [Items.BIGGORONS_SWORD, Items.PROGRESSIVE_STICK_CAPACITY, Items.PROGRESSIVE_HOOKSHOT, Items.PROGRESSIVE_SLINGSHOT, Items.PROGRESSIVE_BOW]
        self.require_any_to_hit(items, EnemyDistance.LONG_JUMPSLASH)

        # Hookshot
        items = [Items.PROGRESSIVE_HOOKSHOT, Items.PROGRESSIVE_SLINGSHOT, Items.PROGRESSIVE_BOW]
        self.require_any_to_hit(items, EnemyDistance.HOOKSHOT)

        # Longshot
        items = [Items.PROGRESSIVE_HOOKSHOT, Items.PROGRESSIVE_SLINGSHOT, Items.PROGRESSIVE_BOW]
        self.require_any_to_hit(items, EnemyDistance.LONGSHOT)

        # Far
        items = [Items.PROGRESSIVE_SLINGSHOT, Items.PROGRESSIVE_BOW]
        self.require_any_to_hit(items, EnemyDistance.FAR)

        # Bomb Special Cases
        items = [Items.PROGRESSIVE_BOMB_BAG]
        self.collect_by_name(items)
        
        for distance in (EnemyDistance.CLOSE, EnemyDistance.SHORT_JUMPSLASH, EnemyDistance.MASTER_SWORD_JUMPSLASH, 
                    EnemyDistance.LONG_JUMPSLASH, EnemyDistance.BOMB_THROW):
            self.assertTrue(can_hit_at_range(self.get_bundle(), distance)._instantiate(self.world)._evaluate(self.multiworld.state), f"Wasn't able to hit enemy from {str(distance.name)} distance and not in water.")
            self.assertFalse(can_hit_at_range(self.get_bundle(), distance, in_water=True)._instantiate(self.world)._evaluate(self.multiworld.state), f"Was able to hit enemy from {str(distance.name)} distance and in water.")

        self.remove_by_name(items)

        items = [Items.BOMBCHU_BAG]
        self.collect_by_name(items)
        for distance in (EnemyDistance.CLOSE, EnemyDistance.SHORT_JUMPSLASH, EnemyDistance.MASTER_SWORD_JUMPSLASH, 
                EnemyDistance.LONG_JUMPSLASH, EnemyDistance.BOMB_THROW, EnemyDistance.HOOKSHOT):
            self.assertTrue(can_hit_at_range(self.get_bundle(), distance)._instantiate(self.world)._evaluate(self.multiworld.state), f"Wasn't able to hit enemy from {str(distance.name)} distance using bombchus and on wall or floor.")
            self.assertFalse(can_hit_at_range(self.get_bundle(), distance, False)._instantiate(self.world)._evaluate(self.multiworld.state), f"Was able to hit enemy from {str(distance.name)} distance using bombchus and not on wall or floor.")

        self.remove_by_name(items)
        
        # Test Distances and items that shouldn't be able to hit
        items = [Items.MEGATON_HAMMER, Items.KOKIRI_SWORD, Items.MASTER_SWORD, Items.BIGGORONS_SWORD, Items.PROGRESSIVE_STICK_CAPACITY, Items.PROGRESSIVE_HOOKSHOT]
        self.can_not_hit_with_any(items, EnemyDistance.FAR)

        items = [Items.MEGATON_HAMMER, Items.KOKIRI_SWORD, Items.MASTER_SWORD, Items.BIGGORONS_SWORD, Items.PROGRESSIVE_STICK_CAPACITY]
        self.can_not_hit_with_any(items, EnemyDistance.HOOKSHOT)
        self.can_not_hit_with_any(items, EnemyDistance.LONGSHOT)

        items = [Items.MEGATON_HAMMER, Items.KOKIRI_SWORD, Items.MASTER_SWORD]
        self.can_not_hit_with_any(items, EnemyDistance.LONG_JUMPSLASH)
                                  
        items = [Items.MEGATON_HAMMER, Items.KOKIRI_SWORD]
        self.can_not_hit_with_any(items, EnemyDistance.MASTER_SWORD_JUMPSLASH)

        items = []
        self.can_not_hit_with_any(items)

class TestCanAttack(SohTestBase):
    """
    Test can_attack helper
    """
    options = {"shuffle_deku_nut_bag": True, "shuffle_deku_stick_bag": True, "closed_forest": 2, "door_of_time": 2, "shuffle_kokiri_sword": 1, "shuffle_master_sword": 1, "bombchu_bag": 1, "bombchu_drops": 1}

    def require_any_to_damage(self, items: list[Items]) -> None:
        # ideally we run these as subtests, but those are currently broken 
        # and report as Success if any subtest succeeds
        # (https://github.com/microsoft/vscode-python/issues/25824)

        self.sweep()
        self.remove_by_name(items)

        for size in range(1, len(items)):
            for valid_combo in combinations(items, size):
                self.collect_by_name(valid_combo)
                self.assertTrue(can_attack(self.get_bundle())._instantiate(self.world)._evaluate(self.multiworld.state), f"Couldn't attack but should have been able to.")
                self.remove_by_name(valid_combo)
                

        self.collect_by_name(items)

        self.assertTrue(can_attack(self.get_bundle())._instantiate(self.world)._evaluate(self.multiworld.state), f"Couldn't attack but should have been able to.")
        
        self.remove_by_name(items)

    def test_can_attack(self):

        # Has Nothing
        self.assertFalse(can_attack(self.get_bundle())._instantiate(self.world)._evaluate(self.multiworld.state), f"Could attack but shouldn't have been able to.")

        # Attacking items
        items = [Items.MEGATON_HAMMER, Items.KOKIRI_SWORD, Items.MASTER_SWORD, Items.BIGGORONS_SWORD, Items.PROGRESSIVE_STICK_CAPACITY, 
            Items.PROGRESSIVE_HOOKSHOT, Items.PROGRESSIVE_SLINGSHOT, Items.PROGRESSIVE_BOW, Items.BOOMERANG, Items.PROGRESSIVE_BOMB_BAG, Items.BOMBCHU_BAG]
        self.require_any_to_damage(items)

        # Check Din's Fire
        items = [Items.PROGRESSIVE_MAGIC_METER, Items.DINS_FIRE]
        self.collect_by_name(items)

        self.assertTrue(can_attack(self.get_bundle())._instantiate(self.world)._evaluate(self.multiworld.state), f"Couldn't attack but should have been able to.")

        self.remove_by_name(items)