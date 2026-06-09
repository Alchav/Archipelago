import random
import typing


SM64_MUSIC_AREA_SEQUENCES = {
    41: 0x0A,
    51: 0x08,
    52: 0x09,
    61: 0x04,
    62: 0x04,
    63: 0x04,
    71: 0x0C,
    81: 0x06,
    82: 0x0C,
    83: 0x0C,
    91: 0x03,
    101: 0x08,
    102: 0x0C,
    111: 0x0C,
    112: 0x0C,
    121: 0x05,
    122: 0x05,
    131: 0x03,
    132: 0x03,
    133: 0x0C,
    141: 0x09,
    151: 0x09,
    161: 0x00,
    171: 0x11,
    181: 0x09,
    191: 0x11,
    201: 0x85,
    211: 0x11,
    221: 0x06,
    222: 0x06,
    231: 0x05,
    232: 0x05,
    241: 0x03,
    261: 0x00,
    271: 0x09,
    281: 0x0C,
    291: 0x09,
    301: 0x07,
    311: 0x09,
    331: 0x07,
    341: 0x19,
    361: 0x03,
    362: 0x09,
    363: 0x09,
    364: 0x09,
}

SM64_MUSIC_SAFE_SEQUENCE_IDS = [
    0x03,
    0x04,
    0x05,
    0x85,
    0x06,
    0x07,
    0x08,
    0x09,
    0x0A,
    0x0C,
    0x11,
    # 0x13,
    # 0x14,
    # 0x16,
    # 0x18,
    0x19,
    # 0x21,
]


def generate_music_map(random: random.Random) -> typing.Dict[str, int]:
    area_keys = sorted(SM64_MUSIC_AREA_SEQUENCES)
    assignments = []

    while len(assignments) < len(area_keys):
        shuffled_pool = sorted(SM64_MUSIC_AREA_SEQUENCES.values())
        random.shuffle(shuffled_pool)
        assignments.extend(shuffled_pool)

    return {str(area_key): assignments[i] for i, area_key in enumerate(area_keys)}


def build_music_slot_data(mode: int, random: random.Random) -> typing.Dict[str, typing.Any]:
    slot_data = {"MusicShuffleMode": mode, "MusicMap": {}}
    if mode == 1:
        slot_data["MusicMap"] = generate_music_map(random)
    return slot_data
