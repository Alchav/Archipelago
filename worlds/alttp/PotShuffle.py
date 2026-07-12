from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from .enemizer_data.pot_shuffle_data import POT_ROOMS

if TYPE_CHECKING:
    from . import ALTTPWorld
    from .Rom import TokenRom


POT_ITEM_POINTER_TABLE = 0xDB67
POT_KEY = 0x08
POT_ARROW = 0x09
POT_BLUE_RUPEE = 0x07
POT_HEART = 0x0B
POT_SWITCH = 0x88
POT_HOLE = 0x80
ICE_PALACE_PENGATOR_BIG_KEY_ROOM_ID = 31
ICE_PALACE_PENGATOR_BIG_KEY_SWITCH_POTS = frozenset(((28, 23), (28, 25)))
POD_ENTRANCE_ROOM_ID = 74
POD_ENTRANCE_LEFT_SWITCH_POTS = frozenset(((14, 5), (32, 5), (14, 11), (32, 11)))
POD_ENTRANCE_RIGHT_SWITCH_POTS = frozenset(((92, 5), (110, 5), (92, 11), (110, 11)))
SWITCH_POT_GROUPS = {
    ICE_PALACE_PENGATOR_BIG_KEY_ROOM_ID: (ICE_PALACE_PENGATOR_BIG_KEY_SWITCH_POTS,),
    POD_ENTRANCE_ROOM_ID: (POD_ENTRANCE_LEFT_SWITCH_POTS, POD_ENTRANCE_RIGHT_SWITCH_POTS),
}
POT_ITEM_ADDRESSES = {
    2: 0xDDE7,
    4: 0xDDE9,
    9: 0xDDF1,
    10: 0xDDFC,
    11: 0xDE0D,
    17: 0xDE15,
    21: 0xDE23,
    22: 0xDE40,
    23: 0xDE5D,
    26: 0xDE83,
    27: 0xDE91,
    30: 0xDE99,
    31: 0xDE9E,
    33: 0xDEA3,
    35: 0xDEAE,
    36: 0xDEBF,
    38: 0xDECD,
    39: 0xDEDE,
    42: 0xDEF2,
    43: 0xDEFA,
    44: 0xDF1A,
    47: 0xDF22,
    49: 0xDF3C,
    50: 0xDF41,
    52: 0xDF46,
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
    68: 0xE00A,
    69: 0xE00C,
    70: 0xE01D,
    73: 0xE025,
    74: 0xE039,
    75: 0xE059,
    78: 0xE061,
    80: 0xE06C,
    82: 0xE074,
    83: 0xE07C,
    84: 0xE08A,
    85: 0xE098,
    86: 0xE0A0,
    87: 0xE0C3,
    88: 0xE0DD,
    89: 0xE0F7,
    91: 0xE0FC,
    92: 0xE101,
    93: 0xE109,
    94: 0xE123,
    95: 0xE131,
    96: 0xE136,
    98: 0xE13E,
    99: 0xE143,
    100: 0xE14B,
    101: 0xE162,
    102: 0xE16A,
    103: 0xE18A,
    104: 0xE1A1,
    107: 0xE1B2,
    108: 0xE1C0,
    109: 0xE1CE,
    115: 0xE1DC,
    116: 0xE1FC,
    117: 0xE213,
    118: 0xE21E,
    123: 0xE229,
    124: 0xE231,
    125: 0xE239,
    126: 0xE247,
    128: 0xE252,
    130: 0xE25D,
    131: 0xE262,
    132: 0xE270,
    133: 0xE278,
    135: 0xE280,
    139: 0xE288,
    140: 0xE293,
    141: 0xE2AA,
    142: 0xE2B8,
    145: 0xE2BD,
    146: 0xE2C3,
    147: 0xE2C5,
    150: 0xE2CD,
    153: 0xE2DB,
    155: 0xE2E3,
    156: 0xE2EB,
    157: 0xE2F3,
    159: 0xE2FB,
    161: 0xE312,
    162: 0xE326,
    168: 0xE32B,
    169: 0xE333,
    170: 0xE347,
    171: 0xE358,
    174: 0xE35D,
    176: 0xE362,
    177: 0xE382,
    178: 0xE38A,
    179: 0xE395,
    180: 0xE3A0,
    181: 0xE3A8,
    182: 0xE3BC,
    183: 0xE3C1,
    184: 0xE3C6,
    185: 0xE3D1,
    186: 0xE3DF,
    188: 0xE3F3,
    190: 0xE41C,
    191: 0xE421,
    192: 0xE435,
    194: 0xE443,
    196: 0xE451,
    198: 0xE46B,
    199: 0xE473,
    201: 0xE481,
    203: 0xE48C,
    204: 0xE494,
    206: 0xE4A2,
    208: 0xE4B3,
    209: 0xE4CA,
    214: 0xE4DB,
    216: 0xE4E3,
    217: 0xE4FD,
    218: 0xE505,
    219: 0xE513,
    220: 0xE51B,
    227: 0xE52E,
    228: 0xE533,
    229: 0xE53B,
    230: 0xE549,
    231: 0xE554,
    232: 0xE55C,
    235: 0xE561,
    241: 0xE572,
    243: 0xE575,
    248: 0xE577,
    253: 0xE57C,
    255: 0xE58A,
    257: 0xE595,
    258: 0xE5A0,
    259: 0xE5A8,
    260: 0xE5B0,
    261: 0xE5BB,
    262: 0xE5C4,
    263: 0xE5C6,
    264: 0xE5DD,
    268: 0xE5E2,
    276: 0xE5E7,
    279: 0xE5FB,
    281: 0xE615,
    282: 0xE623,
    283: 0xE631,
    285: 0xE65A,
    287: 0xE66E,
    292: 0xE676,
    293: 0xE696,
    295: 0xE6AE,
}


@dataclass(frozen=True)
class PotData:
    x: int
    y: int
    reserved: int
    item: int | None = None


@dataclass(frozen=True)
class PotRoomData:
    room_id: int
    pots: tuple[PotData, ...]


@dataclass(frozen=True)
class FilledPot:
    x: int
    y: int
    item: int


def generate_pot_shuffle(world: "ALTTPWorld") -> dict[int, tuple[FilledPot, ...]]:
    room_data = _load_pot_room_data()
    shuffled_pots: dict[int, tuple[FilledPot, ...]] = {}

    for room in room_data:
        room_items = [pot.item for pot in room.pots if pot.item is not None and pot.item != POT_HOLE]
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

        _place_grouped_switches(world, room.room_id, room_items, empty_pots, filled_pots)

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


def _place_grouped_switches(
    world: "ALTTPWorld",
    room_id: int,
    room_items: list[int],
    empty_pots: list[PotData],
    filled_pots: list[FilledPot],
) -> None:
    for switch_group in SWITCH_POT_GROUPS.get(room_id, ()):
        if POT_SWITCH not in room_items:
            return
        candidate_indices = [
            index
            for index, pot in enumerate(empty_pots)
            if (pot.x, pot.y) in switch_group
        ]
        if not candidate_indices:
            continue
        pot_index = world.random.choice(candidate_indices)
        pot = empty_pots.pop(pot_index)
        room_items.remove(POT_SWITCH)
        filled_pots.append(FilledPot(pot.x, pot.y, POT_SWITCH))


def apply_pot_shuffle(rom: "TokenRom", shuffled_pots: dict[int, tuple[FilledPot, ...]]) -> None:
    for room_id, pots in shuffled_pots.items():
        address = POT_ITEM_ADDRESSES[room_id]
        for index, pot in enumerate(pots):
            rom.write_bytes(address + (index * 3), (pot.x, pot.y, pot.item))
        rom.write_bytes(address + (len(pots) * 3), (0xFF, 0xFF))


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


def get_vanilla_pot_items(room_id: int) -> tuple[FilledPot, ...]:
    return tuple(
        FilledPot(pot.x, pot.y, pot.item)
        for room in _load_pot_room_data()
        if room.room_id == room_id
        for pot in room.pots
        if pot.item is not None
    )


def get_vanilla_pot_item(room_id: int, x: int, y: int) -> int | None:
    for pot in get_vanilla_pot_items(room_id):
        if pot.x == x and pot.y == y:
            return pot.item
    return None


def _load_pot_room_data() -> tuple[PotRoomData, ...]:
    return tuple(
        PotRoomData(
            room_id=room.room_id,
            pots=tuple(PotData(x=pot.x, y=pot.y, reserved=pot.reserved, item=pot.item) for pot in room.pots),
        )
        for room in POT_ROOMS
    )
