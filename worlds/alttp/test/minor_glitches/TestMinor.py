from ...Dungeons import get_dungeon_item_pool
from ...InvertedRegions import mark_dark_world_regions
from ...ItemPool import difficulties
from ...Items import item_factory
from ...Options import GlitchesRequired

from ..bases import LTTPTestBase, TestBase


class TestMinor(TestBase, LTTPTestBase):
    def setUp(self):
        self.world_setup()
        self.multiworld.worlds[1].options.glitches_required = GlitchesRequired.from_any("minor_glitches")
        self.multiworld.worlds[1].options.bombless_start.value = True
        self.multiworld.worlds[1].options.shuffle_capacity_upgrades.value = 2
        self.multiworld.worlds[1].difficulty_requirements = difficulties['normal']
        self.world.er_seed = 0
        self.world.create_regions()
        self.world.create_items()
        self.multiworld.itempool.extend(get_dungeon_item_pool(self.multiworld))
        self.multiworld.itempool.extend(item_factory(
            ['Pendant of Courage', 'Pendant of Wisdom', 'Pendant of Power', 'Beat Agahnim 1', 'Beat Agahnim 2', 'Crystal (Palace of Darkness)',
             'Crystal (Swamp Palace)', 'Crystal (Skull Woods)', "Crystal (Thieves' Town)", 'Crystal (Ice Palace)', 'Crystal (Misery Mire)', 'Crystal (Turtle Rock)'], self.world))
        self.multiworld.get_location('Agahnim 1', 1).item = None
        self.multiworld.get_location('Agahnim 2', 1).item = None
        mark_dark_world_regions(self.multiworld, 1)
        self.world.set_rules()
