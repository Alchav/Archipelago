import random
import unittest
from pathlib import Path
from types import SimpleNamespace

from Utils import snes_to_pc
from worlds.alttp.PotShuffle import (
    FilledPot,
    ICE_PALACE_PENGATOR_BIG_KEY_ROOM_ID,
    ICE_PALACE_PENGATOR_BIG_KEY_SWITCH_POTS,
    POD_ENTRANCE_LEFT_SWITCH_POTS,
    POD_ENTRANCE_RIGHT_SWITCH_POTS,
    POD_ENTRANCE_ROOM_ID,
    POT_BLUE_RUPEE,
    POT_ITEM_ADDRESSES,
    POT_KEY,
    POT_HOLE,
    POT_SWITCH,
    SWAMP_TRENCH_2_PAST_TRENCH_KEY_POTS,
    SWAMP_TRENCH_2_ROOM_ID,
    generate_pot_shuffle,
    get_unique_pot_item_position,
    get_vanilla_pot_item,
    get_vanilla_pot_items,
)
from worlds.alttp.enemizer_data.pot_shuffle_data import POT_ROOMS


class TestPotShuffle(unittest.TestCase):
    BASEPATCH_ROM = Path(__file__).resolve().parents[3] / "basepatch.sfc"
    ROOM_OBJECT_POINTER_TABLE = 0xF8000
    POT_OBJECT_ID = 0xFAF
    NON_POT_ITEM_RECORDS = frozenset({
        (0x35, 112, 23),  # Vanilla orphan item: one row below its physical pot.
        (0x3F, 28, 23),   # Block marker item.
        (0x44, 204, 7),   # Block marker item.
        (0x45, 156, 7),   # Block marker item.
        (0x93, 156, 23),  # Block marker item.
        (0xCE, 108, 8),   # Block marker item.
        (0xCE, 204, 11),  # Reserved hole marker.
        (0x117, 24, 8),   # Block marker item.
    })

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

    def test_fixed_key_drop_swamp_trench_2_key_stays_before_trench(self) -> None:
        for seed in range(100):
            world = SimpleNamespace(
                random=random.Random(seed),
                options=SimpleNamespace(retro_bow=False, key_drop_shuffle=False),
            )
            shuffled_pots = generate_pot_shuffle(world)
            key_position = get_unique_pot_item_position(shuffled_pots, SWAMP_TRENCH_2_ROOM_ID, POT_KEY)

            with self.subTest(seed=seed):
                self.assertNotIn(key_position, SWAMP_TRENCH_2_PAST_TRENCH_KEY_POTS)

    def test_pod_entrance_keeps_one_switch_per_side(self) -> None:
        middle_pots = {(56, 8), (68, 8)}

        for seed in range(100):
            world = SimpleNamespace(
                random=random.Random(seed),
                options=SimpleNamespace(retro_bow=False),
            )
            shuffled_pots = generate_pot_shuffle(world)
            switch_positions = {
                (pot.x, pot.y)
                for pot in shuffled_pots[POD_ENTRANCE_ROOM_ID]
                if pot.item == POT_SWITCH
            }

            with self.subTest(seed=seed):
                self.assertEqual(len(switch_positions), 2)
                self.assertEqual(len(switch_positions & POD_ENTRANCE_LEFT_SWITCH_POTS), 1)
                self.assertEqual(len(switch_positions & POD_ENTRANCE_RIGHT_SWITCH_POTS), 1)
                self.assertFalse(switch_positions & middle_pots)

    def test_ice_palace_pengator_big_key_switch_stays_out_of_southeast_pots(self) -> None:
        southeast_pots = {(86, 26), (86, 27)}

        for seed in range(100):
            world = SimpleNamespace(
                random=random.Random(seed),
                options=SimpleNamespace(retro_bow=False),
            )
            shuffled_pots = generate_pot_shuffle(world)
            switch_positions = {
                (pot.x, pot.y)
                for pot in shuffled_pots[ICE_PALACE_PENGATOR_BIG_KEY_ROOM_ID]
                if pot.item == POT_SWITCH
            }

            with self.subTest(seed=seed):
                self.assertEqual(len(switch_positions), 1)
                self.assertTrue(switch_positions <= ICE_PALACE_PENGATOR_BIG_KEY_SWITCH_POTS)
                self.assertFalse(switch_positions & southeast_pots)

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

    def test_pot_item_records_fit_before_next_room_pointer(self) -> None:
        room_data = {room.room_id: room for room in POT_ROOMS}
        sorted_addresses = sorted(POT_ITEM_ADDRESSES.items(), key=lambda entry: entry[1])

        for (room_id, address), (next_room_id, next_address) in zip(sorted_addresses, sorted_addresses[1:]):
            room = room_data[room_id]
            entry_count = sum(
                1
                for pot in room.pots
                if pot.item is not None and pot.item != POT_HOLE
            )
            entry_count += sum(1 for pot in room.pots if pot.reserved == 3)
            required_end = address + entry_count * 3

            with self.subTest(room=room_id, next_room=next_room_id):
                self.assertLessEqual(
                    required_end,
                    next_address,
                    f"room {room_id:#04x} has {entry_count} pot item records requiring "
                    f"{required_end - address} record bytes at {address:#06x}, but room "
                    f"{next_room_id:#04x} starts at {next_address:#06x}",
                )

    def test_vanilla_pot_items_match_basepatch_rom(self) -> None:
        if not self.BASEPATCH_ROM.exists():
            self.skipTest(f"{self.BASEPATCH_ROM} is not present")

        rom = self.BASEPATCH_ROM.read_bytes()

        for room_id, address in sorted(POT_ITEM_ADDRESSES.items()):
            with self.subTest(room=room_id):
                self.assertEqual(
                    get_vanilla_pot_items(room_id),
                    self._read_pot_items_from_rom(rom, address),
                )

    def test_pot_candidates_match_basepatch_room_objects(self) -> None:
        if not self.BASEPATCH_ROM.exists():
            self.skipTest(f"{self.BASEPATCH_ROM} is not present")

        rom = self.BASEPATCH_ROM.read_bytes()

        for room in POT_ROOMS:
            pot_records = [
                pot for pot in room.pots
                if (room.room_id, pot.x, pot.y) not in self.NON_POT_ITEM_RECORDS
            ]
            if not pot_records:
                continue

            room_pot_objects = self._read_room_pot_object_positions(rom, room.room_id)
            seen_pots = {}
            with self.subTest(room=room.room_id):
                self.assertTrue(room_pot_objects, f"room {room.room_id:#04x} has no 0xFAF pot objects")

            for pot in pot_records:
                physical_position = self._pot_record_physical_position(pot.x, pot.y)
                with self.subTest(room=room.room_id, x=pot.x, y=pot.y):
                    self.assertIn(
                        physical_position,
                        room_pot_objects,
                        f"room {room.room_id:#04x} pot candidate {(pot.x, pot.y)} does not map to a "
                        "0xFAF room object",
                    )
                    self.assertNotIn(
                        physical_position,
                        seen_pots,
                        f"room {room.room_id:#04x} has duplicate pot candidates {seen_pots.get(physical_position)} "
                        f"and {(pot.x, pot.y)} for the same physical 0xFAF room object",
                    )
                seen_pots[physical_position] = (pot.x, pot.y)

    @staticmethod
    def _read_pot_items_from_rom(rom: bytes, address: int) -> tuple:
        pots = []
        offset = address
        while True:
            x, y = rom[offset], rom[offset + 1]
            if x == 0xFF and y == 0xFF:
                return tuple(pots)
            pots.append(FilledPot(x, y, rom[offset + 2]))
            offset += 3

    @classmethod
    def _read_room_pot_object_positions(cls, rom: bytes, room_id: int) -> frozenset[tuple[int, int]]:
        pointer_address = cls.ROOM_OBJECT_POINTER_TABLE + (room_id * 3)
        snes_address = (
            rom[pointer_address]
            | (rom[pointer_address + 1] << 8)
            | (rom[pointer_address + 2] << 16)
        )
        offset = snes_to_pc(snes_address) + 2
        positions: set[tuple[int, int]] = set()

        for layer in range(3):
            is_door_layer = False
            while True:
                if rom[offset:offset + 2] == bytes((0xF0, 0xFF)):
                    is_door_layer = True
                    offset += 2
                    continue
                if rom[offset:offset + 2] == bytes((0xFF, 0xFF)):
                    offset += 2
                    break
                if is_door_layer:
                    offset += 2
                    continue

                object_bytes = rom[offset:offset + 3]
                if cls._room_object_id(object_bytes) == cls.POT_OBJECT_ID:
                    positions.add(cls._room_object_to_pot_position(object_bytes, layer))
                offset += 3

        return frozenset(positions)

    @staticmethod
    def _room_object_id(object_bytes: bytes) -> int:
        if object_bytes[0] >= 0xFC:
            return (object_bytes[2] & 0x3F) + 0x100
        if object_bytes[2] >= 0xF8:
            return 0xF00 | ((object_bytes[2] & 0x0F) << 4) | ((object_bytes[1] & 0x03) << 2) | (object_bytes[0] & 0x03)
        return object_bytes[2]

    @staticmethod
    def _room_object_to_pot_position(object_bytes: bytes, layer: int) -> tuple[int, int]:
        hm_x = (object_bytes[0] & 0xFC) >> 2
        hm_y = (object_bytes[1] & 0xFC) >> 2
        pot_x = hm_x * 2
        if hm_y & 1:
            pot_x |= 0x80
        return pot_x, hm_y // 2

    @staticmethod
    def _pot_record_physical_position(x: int, y: int) -> tuple[int, int]:
        return x, y & 0x1F


if __name__ == "__main__":
    unittest.main()
