from ..Items import progressive_items, Items
from .bases import SohTestBase
from ..LogicHelpers import has_item
from itertools import combinations

class TestCollectRemoveNonProgressive(SohTestBase):
    options = {"shuffle_kokiri_sword": True, "shuffle_master_sword": True, "shuffle_songs": "anywhere",
               "start_with_sarias_song": True, "start_with_master_sword": True, "start_with_eponas_song": True}

    def test_collect_gives_item(self):
        """
        Testing to make sure that collecting items properly gives the player a single copy.
        """
        self.sweep()
        items = [Items.KOKIRI_SWORD, Items.MEGATON_HAMMER, Items.FIRE_ARROW, Items.SUNS_SONG, Items.BOOMERANG]
        for item in items:
            self.assertFalse(self.multiworld.state.has(item, self.player), f"Should not have {item} before collecting it.")

        for size in range(1, len(items) + 1):
            for combo in combinations(items, size):
                self.collect_by_name(combo)
                for item in combo:
                    self.assertTrue(self.multiworld.state.has(item, self.player), f"No {item} after trying to collect it.")
                    self.assertTrue(self.multiworld.state.count(item, self.player) == 1, f"{item} was collected, but has a count greater than 1 when it shouldn't.")
                self.remove_by_name(combo)

    def test_remove_takes_away_item(self):
        """
        Testing to make sure that removing items properly removes them.
        """
        self.sweep()
        items = [Items.BIGGORONS_SWORD, Items.LENS_OF_TRUTH, Items.ICE_ARROW, Items.SONG_OF_STORMS, Items.FARORES_WIND]
        for item in items:
            self.assertFalse(self.multiworld.state.has(item, self.player), f"Should not have {item} before collecting it.")

        for size in range(1, len(items) + 1):
            for combo in combinations(items, size):
                self.collect_by_name(combo)
                self.remove_by_name(combo)
                for item in combo:
                    self.assertFalse(self.multiworld.state.has(item, self.player), f"{item} should not be present after removing it.")

    def test_precollected_items(self):
        """
        Testing to ensure that starting items are collected properly, based on settings.
        """
        self.sweep()
        items = [Items.SARIAS_SONG, Items.MASTER_SWORD, Items.EPONAS_SONG]
        for item in items:
            self.assertTrue(self.multiworld.state.has(item, self.player), f"{item} should be precollected, but isn't.")
            self.assertTrue(self.multiworld.state.count(item, self.player) == 1,
                            f"{item} was precollected, but has a count greater than 1 when it shouldn't.")

class ProgressiveTestsMixin:
    optional_prog_item_set = set()

    def test_collect_progressive(self):
        """
        Testing to make sure that, depending on how many of each progressive item are collected, that we have the corresponding "ranks,"
        and that we don't have the unobtainable ranks.
        """
        for item_name, prog_items in progressive_items.items():
            total = len(prog_items)
            start = 1 if item_name in self.optional_prog_item_set else 0
            for i in range(start, total):
                self.collect(self.world.create_item(item_name))
                for rank in range(i + 1):
                    self.assertTrue(has_item(prog_items[rank], self.get_bundle())._instantiate(self.world)._evaluate(self.multiworld.state),
                                    f"Failed for {item_name}, we do not have {prog_items[rank]}")
                for rank in range(i + 1, total):
                    self.assertFalse(has_item(prog_items[rank], self.get_bundle())._instantiate(self.world)._evaluate(
                        self.multiworld.state),
                                    f"Failed for {item_name}, we should not have {prog_items[rank]}")

    def test_remove_progressive(self):
        """
        Testing to make sure that, if we remove progressive items, we have the correct amount of their corresponding ranks.
        """
        for item_name, prog_items in progressive_items.items():
            total = len(prog_items)
            start = 1 if item_name in self.optional_prog_item_set else 0
            for _ in range(start, total):
                self.collect(self.world.create_item(item_name))
            count = self.multiworld.state.count(item_name, self.player)
            self.assertTrue(count == total, f"Wrong count for {item_name}, should be {total}.")
            for i in range(count):
                self.remove(self.get_item_by_name(item_name))
                for rank in range(count - i - 1):
                    self.assertTrue(has_item(prog_items[rank], self.get_bundle())._instantiate(self.world)._evaluate(self.multiworld.state),
                                    f"Failed for {item_name}, we do not have {prog_items[rank]}")
                for rank in range(count- i - 1, total):
                    self.assertFalse(has_item(prog_items[rank], self.get_bundle())._instantiate(self.world)._evaluate(
                        self.multiworld.state),
                                    f"Failed for {item_name}, we should not have {prog_items[rank]}")

    def test_progressive_precollected_items(self):
        """
        Testing to make sure that we have the first rank of a progressive item if its setting results in one being precollected,
        and zero ranks otherwise.
        """
        self.sweep()
        for item_name, prog_items in progressive_items.items():
            first_rank = prog_items[0]
            if item_name in self.optional_prog_item_set:
                self.assertTrue(has_item(first_rank, self.get_bundle())._instantiate(self.world)._evaluate(
                    self.multiworld.state),
                    f"Failed for {item_name}, we do not have {first_rank}")
            else:
                self.assertFalse(has_item(first_rank, self.get_bundle())._instantiate(self.world)._evaluate(
                    self.multiworld.state),
                    f"Failed for {item_name}, we should not have {first_rank}")

class TestCollectRemoveProgressiveAllOff(ProgressiveTestsMixin, SohTestBase):
    options = {"shuffle_childs_wallet": False, "shuffle_swim": False, "shuffle_deku_stick_bag": False,
               "shuffle_deku_nut_bag": False, "bombchu_bag": "none", "shuffle_ocarinas": True}
    optional_prog_item_set = {Items.PROGRESSIVE_SCALE, Items.PROGRESSIVE_WALLET, Items.PROGRESSIVE_STICK_CAPACITY,
                              Items.PROGRESSIVE_NUT_CAPACITY, Items.BOMBCHU_BAG}

class TestCollectRemoveProgressiveAllOn(ProgressiveTestsMixin, SohTestBase):
    options = {"shuffle_childs_wallet": True, "shuffle_swim": True, "shuffle_deku_stick_bag": True,
               "shuffle_deku_nut_bag": True, "bombchu_bag": "single_bag", "shuffle_ocarinas": True}
