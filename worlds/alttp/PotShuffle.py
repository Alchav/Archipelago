from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from .enemizer_data.pot_shuffle_data import POT_ROOMS

if TYPE_CHECKING:
    from . import ALTTPWorld
    from .Rom import LocalRom


POT_ITEM_POINTER_TABLE = 0xDB67
POT_KEY = 0x08
POT_ARROW = 0x09
POT_BLUE_RUPEE = 0x07
POT_SWITCH = 0x88
POT_HOLE = 0x80
POT_ITEM_ADDRESSES = {
    4: 0xDDE9,
    9: 0xDDF1,
    10: 0xDDFC,
    17: 0xDE15,
    21: 0xDE23,
    22: 0xDE40,
    26: 0xDE83,
    33: 0xDEA3,
    35: 0xDEAE,
    36: 0xDEBF,
    38: 0xDECD,
    39: 0xDEDE,
    43: 0xDEFA,
    47: 0xDF22,
    53: 0xDF4E,
    54: 0xDF6B,
    55: 0xDF79,
    56: 0xDF7E,
    57: 0xDF8C,
    60: 0xDF9A,
    61: 0xDFB1,
    62: 0xDFC8,
    63: 0xDFD6,
    65: 0xDFED,
    67: 0xDFFB,
    69: 0xE00C,
    73: 0xE025,
    78: 0xE061,
    83: 0xE07C,
    84: 0xE08A,
    86: 0xE0A0,
    87: 0xE0C3,
    88: 0xE0DD,
    91: 0xE0FC,
    92: 0xE101,
    93: 0xE109,
    94: 0xE123,
    99: 0xE143,
    100: 0xE14B,
    102: 0xE16A,
    103: 0xE18A,
    104: 0xE1A1,
    115: 0xE1DC,
    116: 0xE1FC,
    117: 0xE213,
    123: 0xE229,
    124: 0xE231,
    125: 0xE239,
    126: 0xE247,
    130: 0xE25D,
    131: 0xE262,
    132: 0xE270,
    135: 0xE280,
    139: 0xE288,
    140: 0xE293,
    145: 0xE2BD,
    150: 0xE2CD,
    155: 0xE2E3,
    157: 0xE2F3,
    159: 0xE2FB,
    161: 0xE312,
    168: 0xE32B,
    169: 0xE333,
    170: 0xE347,
    176: 0xE362,
    179: 0xE395,
    180: 0xE3A0,
    181: 0xE3A8,
    184: 0xE3C6,
    185: 0xE3D1,
    186: 0xE3DF,
    188: 0xE3F3,
    191: 0xE421,
    192: 0xE435,
    194: 0xE443,
    196: 0xE451,
    199: 0xE473,
    201: 0xE481,
    203: 0xE48C,
    204: 0xE494,
    206: 0xE4A2,
    208: 0xE4B3,
    209: 0xE4CA,
    214: 0xE4DB,
    216: 0xE4E3,
    218: 0xE505,
    219: 0xE513,
    220: 0xE51B,
    235: 0xE561,
}


@dataclass(frozen=True)
class PotData:
    x: int
    y: int
    reserved: int


@dataclass(frozen=True)
class PotRoomData:
    room_id: int
    pots: tuple[PotData, ...]
    items: tuple[int, ...]


@dataclass(frozen=True)
class FilledPot:
    x: int
    y: int
    item: int


def generate_pot_shuffle(world: "ALTTPWorld") -> dict[int, tuple[FilledPot, ...]]:
    room_data = _load_pot_room_data()
    shuffled_pots: dict[int, tuple[FilledPot, ...]] = {}

    for room in room_data:
        room_items = [item for item in room.items if item != POT_HOLE]
        if world.options.retro_bow:
            room_items = [POT_BLUE_RUPEE if item == POT_ARROW else item for item in room_items]

        empty_pots: list[PotData] = []
        filled_pots: list[FilledPot] = []

        for pot in room.pots:
            if pot.reserved == 3:
                filled_pots.append(FilledPot(pot.x, pot.y, POT_HOLE))
            else:
                empty_pots.append(pot)

        while POT_KEY in room_items:
            candidate_indices = list(range(len(empty_pots)))
            if not candidate_indices:
                break
            pot_index = world.random.choice(candidate_indices)
            pot = empty_pots.pop(pot_index)
            room_items.remove(POT_KEY)
            filled_pots.append(FilledPot(pot.x, pot.y, POT_KEY))

        while POT_SWITCH in room_items:
            candidate_indices = [index for index, pot in enumerate(empty_pots) if pot.reserved == 2]
            if not candidate_indices:
                break
            pot_index = world.random.choice(candidate_indices)
            pot = empty_pots.pop(pot_index)
            room_items.remove(POT_SWITCH)
            filled_pots.append(FilledPot(pot.x, pot.y, POT_SWITCH))

        while room_items and empty_pots:
            pot_index = world.random.randrange(len(empty_pots))
            item_index = world.random.randrange(len(room_items))
            pot = empty_pots.pop(pot_index)
            item = room_items.pop(item_index)
            filled_pots.append(FilledPot(pot.x, pot.y, item))

        shuffled_pots[room.room_id] = tuple(filled_pots)

    return shuffled_pots


def apply_pot_shuffle(rom: "LocalRom", shuffled_pots: dict[int, tuple[FilledPot, ...]]) -> None:
    for room_id, pots in shuffled_pots.items():
        address = POT_ITEM_ADDRESSES[room_id]
        for index, pot in enumerate(pots):
            rom.write_bytes(address + (index * 3), (pot.x, pot.y, pot.item))


def get_unique_pot_item_position(
    shuffled_pots: dict[int, tuple[FilledPot, ...]],
    room_id: int,
    item: int,
) -> tuple[int, int]:
    positions = [
        (pot.x, pot.y)
        for pot in shuffled_pots.get(room_id, ())
        if pot.item == item
    ]
    if len(positions) != 1:
        raise ValueError(
            f"Expected exactly one pot item {hex(item)} in room {hex(room_id)}, found {len(positions)}"
        )
    return positions[0]


def _load_pot_room_data() -> tuple[PotRoomData, ...]:
    return tuple(
        PotRoomData(
            room_id=room.room_id,
            pots=tuple(PotData(x=pot.x, y=pot.y, reserved=pot.reserved) for pot in room.pots),
            items=room.items,
        )
        for room in POT_ROOMS
    )
