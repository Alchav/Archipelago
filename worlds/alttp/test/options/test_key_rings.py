import unittest

from BaseClasses import CollectionState
from test.general import setup_multiworld

from ... import ALTTPWorld


class TestKeyRings(unittest.TestCase):
    def test_key_ring_dungeon_items_with_key_drop_off(self):
        multiworld = setup_multiworld(
            ALTTPWorld,
            ("generate_early", "create_regions", "create_items"),
            options={
                "key_rings": "all",
                "key_drop_shuffle": 0,
            },
        )
        world = multiworld.worlds[1]

        assert world.key_ring_data["Small Key Ring (Hyrule Castle)"] == 1
        assert world.key_ring_data["Small Key Ring (Eastern Palace)"] == 0
        assert [item.name for item in world.dungeons["Hyrule Castle"].small_keys] == ["Small Key (Hyrule Castle)"]
        assert world.dungeons["Eastern Palace"].small_keys == []

    def test_key_ring_collect_and_remove_uses_reduced_count(self):
        multiworld = setup_multiworld(
            ALTTPWorld,
            ("generate_early",),
            options={
                "key_rings": "all",
                "key_drop_shuffle": 0,
            },
        )
        world = multiworld.worlds[1]
        state = CollectionState(multiworld)
        item = world.create_item("Small Key Ring (Palace of Darkness)")

        state.collect(item, prevent_sweep=True)
        assert state.count("Small Key (Palace of Darkness)", 1) == 6
        assert state.count("Small Key Ring (Palace of Darkness)", 1) == 0

        state.remove(item)
        assert state.count("Small Key (Palace of Darkness)", 1) == 0

    def test_key_ring_item_properties_are_distinct_from_small_keys(self):
        multiworld = setup_multiworld(ALTTPWorld, ("generate_early",))
        world = multiworld.worlds[1]

        key_ring = world.create_item("Small Key Ring (Palace of Darkness)")
        small_key = world.create_item("Small Key (Palace of Darkness)")

        assert key_ring.smallkeyring
        assert not key_ring.smallkey
        assert small_key.smallkey
        assert not small_key.smallkeyring

    def test_key_rings_keep_itempool_size_with_any_world_small_keys(self):
        base_world = setup_multiworld(
            ALTTPWorld,
            ("generate_early", "create_regions", "create_items"),
            seed=0,
            options={
                "small_key_shuffle": "any_world",
            },
        )
        key_ring_world = setup_multiworld(
            ALTTPWorld,
            ("generate_early", "create_regions", "create_items"),
            seed=0,
            options={
                "small_key_shuffle": "any_world",
                "key_rings": "all",
            },
        )

        assert len(base_world.itempool) == len(key_ring_world.itempool)
        assert sum(item.name.startswith("Small Key Ring (") for item in key_ring_world.itempool) == 12

    def test_standard_mode_hyrule_castle_ring_is_local_early(self):
        multiworld = setup_multiworld(
            ALTTPWorld,
            ("generate_early",),
            options={
                "mode": "standard",
                "small_key_shuffle": "any_world",
                "key_rings": "choose",
                "key_rings_list": ["Hyrule Castle"],
            },
        )

        assert multiworld.local_early_items[1]["Small Key Ring (Hyrule Castle)"] == 1
        assert "Small Key (Hyrule Castle)" not in multiworld.local_early_items[1]

    def test_universal_keys_ignores_key_rings(self):
        multiworld = setup_multiworld(
            ALTTPWorld,
            ("generate_early", "create_regions", "create_items"),
            options={
                "small_key_shuffle": "universal",
                "key_rings": "all",
            },
        )
        world = multiworld.worlds[1]

        assert world.key_rings == set()
        assert all(not item.name.startswith("Small Key Ring (") for item in multiworld.itempool)
