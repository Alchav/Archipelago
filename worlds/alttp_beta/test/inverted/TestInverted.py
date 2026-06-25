from ...Dungeons import get_dungeon_item_pool
from ...EntranceShuffle import link_inverted_entrances
from ...InvertedRegions import create_inverted_regions
from ...ItemPool import difficulties
from ...Items import item_factory
from ...Regions import mark_light_world_regions
from ...Shops import create_shops

from ..bases import LTTPTestBase, TestBase


class TestInverted(TestBase, LTTPTestBase):
    def setUp(self):
        self.world_setup()
        self.multiworld.worlds[1].difficulty_requirements = difficulties['normal']
        self.multiworld.worlds[1].options.mode.value = 2
        self.multiworld.worlds[1].options.bombless_start.value = True
        self.multiworld.worlds[1].options.shuffle_capacity_upgrades.value = 2
        create_inverted_regions(self.multiworld, 1)
        self.world.create_dungeons()
        create_shops(self.multiworld, 1)
        link_inverted_entrances(self.multiworld, 1)
        self.world.create_items()
        self.multiworld.itempool.extend(get_dungeon_item_pool(self.multiworld))
        self.multiworld.itempool.extend(item_factory(['Pendant of Courage', 'Pendant of Wisdom', 'Pendant of Power', 'Beat Agahnim 1', 'Beat Agahnim 2', 'Crystal (Palace of Darkness)', 'Crystal (Swamp Palace)', 'Crystal (Skull Woods)', "Crystal (Thieves' Town)", 'Crystal (Ice Palace)', 'Crystal (Misery Mire)', 'Crystal (Turtle Rock)'], self.world))
        self.multiworld.get_location('Agahnim 1', 1).item = None
        self.multiworld.get_location('Agahnim 2', 1).item = None
        mark_light_world_regions(self.multiworld, 1)
        self.world.set_rules()
