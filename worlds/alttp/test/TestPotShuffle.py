import random
import unittest
from types import SimpleNamespace

from worlds.alttp.PotShuffle import (
    POT_BLUE_RUPEE,
    POT_ITEM_ADDRESSES,
    POT_KEY,
    POT_HOLE,
    POT_SWITCH,
    generate_pot_shuffle,
    get_unique_pot_item_position,
    get_vanilla_pot_item,
    get_vanilla_pot_items,
)
from worlds.alttp.enemizer_data.pot_shuffle_data import POT_ROOMS


class TestPotShuffle(unittest.TestCase):
    def test_key_rooms_place_actual_keys(self) -> None:
        for seed in range(10):
            world = SimpleNamespace(
                random=random.Random(seed),
                options=SimpleNamespace(retro_bow=False),
            )
            shuffled_pots = generate_pot_shuffle(world)
            conveyor_cross_keys = [
                pot for pot in shuffled_pots[0x8B]
                if pot.item == POT_KEY
            ]
            self.assertEqual(len(conveyor_cross_keys), 1)

    def test_get_unique_pot_item_position_returns_single_match(self) -> None:
        world = SimpleNamespace(
            random=random.Random(0),
            options=SimpleNamespace(retro_bow=False),
        )
        shuffled_pots = generate_pot_shuffle(world)
        key_positions = [
            (pot.x, pot.y)
            for pot in shuffled_pots[0x36]
            if pot.item == POT_KEY
        ]

        self.assertEqual(
            get_unique_pot_item_position(shuffled_pots, 0x36, POT_KEY),
            key_positions[0],
        )

    def test_reserved_hole_room_keeps_hole_fixed(self) -> None:
        for seed in range(25):
            world = SimpleNamespace(
                random=random.Random(seed),
                options=SimpleNamespace(retro_bow=False),
            )
            shuffled_pots = generate_pot_shuffle(world)
            hole_positions = [
                (pot.x, pot.y)
                for pot in shuffled_pots[206]
                if pot.item == POT_HOLE
            ]

            self.assertEqual(hole_positions, [(204, 11)])

    def test_get_vanilla_pot_item_returns_exact_room_188_items(self) -> None:
        self.assertEqual(get_vanilla_pot_item(0xBC, 138, 3), 0x0A)
        self.assertEqual(get_vanilla_pot_item(0xBC, 178, 3), POT_SWITCH)
        self.assertEqual(get_vanilla_pot_item(0xBC, 102, 4), POT_KEY)
        self.assertEqual(get_vanilla_pot_item(0xBC, 28, 21), POT_BLUE_RUPEE)
        self.assertIsNone(get_vanilla_pot_item(0xBC, 12, 20))

    def test_get_vanilla_pot_item_returns_exact_room_139_items(self) -> None:
        self.assertEqual(get_vanilla_pot_item(0x8B, 112, 12), POT_KEY)
        self.assertEqual(get_vanilla_pot_item(0x8B, 76, 28), 0x0B)
        self.assertIsNone(get_vanilla_pot_item(0x8B, 76, 20))

    def test_get_vanilla_pot_item_returns_exact_room_141_items(self) -> None:
        self.assertEqual(POT_ITEM_ADDRESSES[0x8D], 0xE2AA)
        self.assertIsNone(get_vanilla_pot_item(0x8D, 204, 11))
        self.assertEqual(get_vanilla_pot_item(0x8D, 204, 14), 0x0D)
        self.assertEqual(get_vanilla_pot_item(0x8D, 28, 23), 0x0B)
        self.assertEqual(get_vanilla_pot_item(0x8D, 36, 23), 0x0B)
        self.assertEqual(get_vanilla_pot_item(0x8D, 32, 24), 0x0D)

    def test_get_vanilla_pot_items_returns_filled_pots(self) -> None:
        items = get_vanilla_pot_items(0x8B)

        self.assertEqual(
            [(pot.x, pot.y, pot.item) for pot in items],
            [(112, 12, POT_KEY), (32, 9, 0x0C), (76, 28, 0x0B)],
        )

    def test_vanilla_filled_pots_match_candidate_pots_except_vanilla_orphans(self) -> None:
        vanilla_orphan_items = {
            (0x35, 112, 23),  # HM 38,2E: item is one row below the real pot at HM 38,2D.
        }

        for room in POT_ROOMS:
            candidate_positions = {(pot.x, pot.y) for pot in room.pots}
            for record in get_vanilla_pot_items(room.room_id):
                if (room.room_id, record.x, record.y) in vanilla_orphan_items:
                    continue
                self.assertIn((record.x, record.y), candidate_positions, room.room_id)


if __name__ == "__main__":
    unittest.main()
