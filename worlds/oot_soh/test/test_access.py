from .. import SohWorld
from ..Items import Items, Locations, SohItem
from BaseClasses import ItemClassification as IC
from ..Enums import Regions, Events, Enemies
from .bases import SohTestBase

# Ganon's Castle
class TestAccessGBK(SohTestBase):
    """
    Checking to see if the Ganons Boss Key Chest is accessible after passing the Rainbow Bridge.
    This was made to test for this issue https://github.com/aMannus/Archipelago/issues/241
    """
    # fill in the options here, formatted like "shuffle_childs_wallet": False,
    options = {"starting_age": 1, "ganons_trials": "skip", "rainbow_bridge_greg_modifier": "reward",
               "rainbow_bridge": "greg", "ganons_castle_boss_key_greg_modifier": "wildcard"}
    # options not set here will be set to default
    world: SohWorld

    def test_ganon_bk_chest_skip_trials(self):
        self.collect_by_name(Items.GREG_THE_GREEN_RUPEE)
        self.collect_by_name(Items.BIGGORONS_SWORD)

        self.assertTrue(self.can_reach_location(Locations.GANONS_CASTLE_TOWER_BOSS_KEY_CHEST),
                        f"Wasn't able to reach GBK chest")

# Deku Tree
class TestAccessDekuTreeUpperBasement(SohTestBase):
    options = {"starting_age": 0, "closed_forest": 2, "door_of_time": 0, "shuffle_kokiri_sword": 1}
    world: SohWorld

    def test_child_without_slingshot_upper_basement_access(self):
        self.collect_by_name(Items.KOKIRI_SWORD)
        self.assertTrue(self.can_reach_region(Regions.DEKU_TREE_BASEMENT_LOWER), f"The basement should be accessible.")
        self.assertFalse(self.can_reach_region(Regions.DEKU_TREE_BASEMENT_UPPER),
                         f"An unskilled child cannot get to the top of the basement.")
        self.enable_glitched_item()
        self.assertTrue(self.can_reach_region(Regions.DEKU_TREE_BASEMENT_UPPER),
                        f"A skilled child can go from lower basement to upper basement without pushing the block.")
