import unittest
from types import SimpleNamespace

from ..music import default_music, default_music_yellow, music_pointers, music_pointers_yellow, randomize_map_music
from ..regions import map_ids
from ..rom_addresses import rom_addresses_rb as rom_addresses, rom_addresses_yellow


class RecordingWriter:
    def __init__(self) -> None:
        self.writes = {}

    def __call__(self, address: int, data) -> None:
        self.writes[address] = data


class ReverseShuffleRandom:
    def shuffle(self, sequence) -> None:
        sequence.reverse()


class PalletToPokemonTowerShuffleRandom:
    def shuffle(self, sequence) -> None:
        sequence.remove("MUSIC_POKEMON_TOWER")
        sequence.insert(0, "MUSIC_POKEMON_TOWER")


class FirstThenSecondChoiceRandom:
    def __init__(self) -> None:
        self.calls = 0

    def choice(self, sequence):
        self.calls += 1
        return sequence[0] if self.calls == 1 else sequence[1]


def make_world(mode: str, rng, game: str = "Pokemon Red", addresses=rom_addresses) -> SimpleNamespace:
    return SimpleNamespace(
        game=game,
        options=SimpleNamespace(randomize_map_music=mode),
        random=rng,
        rom_addresses=addresses,
    )


def read_pointer(song_table: bytes, map_name: str) -> int:
    map_id = map_ids[map_name]
    return int.from_bytes(song_table[map_id * 2:(map_id * 2) + 2], byteorder="big")


class TestMapMusicRandomization(unittest.TestCase):
    def test_vanilla_music_leaves_rom_data_untouched(self) -> None:
        writer = RecordingWriter()

        randomize_map_music(make_world("vanilla", ReverseShuffleRandom()), writer)

        self.assertEqual({}, writer.writes)

    def test_shuffle_remaps_music_by_default_track_groups(self) -> None:
        writer = RecordingWriter()

        randomize_map_music(make_world("shuffle", ReverseShuffleRandom()), writer)
        song_table = bytes(writer.writes[rom_addresses["Map_Songs"]])

        shuffled_tracks = list(music_pointers.keys())
        shuffled_tracks.reverse()
        expected_mapping = dict(zip(music_pointers.keys(), shuffled_tracks))
        actual_pointers = {
            map_name: read_pointer(song_table, map_name)
            for map_name in default_music
        }
        expected_pointers = {
            map_name: music_pointers[expected_mapping[default_track]]
            for map_name, default_track in default_music.items()
        }

        self.assertEqual(expected_pointers, actual_pointers)

    def test_yellow_shuffle_uses_yellow_music_ids(self) -> None:
        writer = RecordingWriter()

        randomize_map_music(
            make_world("shuffle", PalletToPokemonTowerShuffleRandom(), "Pokemon Yellow", rom_addresses_yellow),
            writer,
        )
        song_table = bytes(writer.writes[rom_addresses_yellow["Map_Songs"]])

        shuffled_tracks = list(music_pointers_yellow.keys())
        shuffled_tracks.remove("MUSIC_POKEMON_TOWER")
        shuffled_tracks.insert(0, "MUSIC_POKEMON_TOWER")
        expected_mapping = dict(zip(music_pointers_yellow.keys(), shuffled_tracks))

        self.assertEqual(0xEF1F, music_pointers_yellow["MUSIC_POKEMON_TOWER"])
        self.assertEqual(0xF01F, music_pointers["MUSIC_POKEMON_TOWER"])
        self.assertEqual(music_pointers_yellow["MUSIC_POKEMON_TOWER"], read_pointer(song_table, "Player's House 1F"))
        self.assertEqual(
            music_pointers_yellow[expected_mapping["MUSIC_ROUTES3"]],
            read_pointer(song_table, "Summer Beach House"),
        )

    def test_randomize_picks_music_per_map_instead_of_per_default_track(self) -> None:
        rng = FirstThenSecondChoiceRandom()
        writer = RecordingWriter()

        randomize_map_music(make_world("randomize", rng), writer)
        song_table = bytes(writer.writes[rom_addresses["Map_Songs"]])

        first_pointer, second_pointer = list(music_pointers.values())[:2]

        self.assertEqual(len(default_music), rng.calls)
        self.assertEqual(first_pointer, read_pointer(song_table, "Pallet Town"))
        self.assertEqual(second_pointer, read_pointer(song_table, "Viridian City"))
        self.assertEqual(second_pointer, read_pointer(song_table, "Player's House 1F"))
        self.assertNotEqual(
            read_pointer(song_table, "Pallet Town"),
            read_pointer(song_table, "Player's House 1F"),
        )

    def test_chaos_mode_enables_option_and_writes_full_pointer_table(self) -> None:
        writer = RecordingWriter()

        randomize_map_music(make_world("chaos", ReverseShuffleRandom()), writer)

        self.assertEqual([0, 0], writer.writes[rom_addresses["Option_Chaos_Music"]])
        self.assertEqual(len(music_pointers), writer.writes[rom_addresses["Chaos_Music_Quantity"]])

        song_table = bytes(writer.writes[rom_addresses["Map_Songs"]])
        expected_prefix = b"".join(
            pointer.to_bytes(2, byteorder="big")
            for pointer in music_pointers.values()
        )

        self.assertEqual((max(map_ids[music_map] for music_map in default_music) + 1) * 2, len(song_table))
        self.assertTrue(song_table.startswith(expected_prefix))
        self.assertEqual(bytes(len(song_table) - len(expected_prefix)), song_table[len(expected_prefix):])

    def test_yellow_chaos_mode_writes_yellow_pointer_table(self) -> None:
        writer = RecordingWriter()

        randomize_map_music(
            make_world("chaos", ReverseShuffleRandom(), "Pokemon Yellow", rom_addresses_yellow),
            writer,
        )

        self.assertEqual([0, 0], writer.writes[rom_addresses_yellow["Option_Chaos_Music"]])
        self.assertEqual(len(music_pointers_yellow), writer.writes[rom_addresses_yellow["Chaos_Music_Quantity"]])

        song_table = bytes(writer.writes[rom_addresses_yellow["Map_Songs"]])
        expected_prefix = b"".join(
            pointer.to_bytes(2, byteorder="big")
            for pointer in music_pointers_yellow.values()
        )

        self.assertEqual((max(map_ids[music_map] for music_map in default_music_yellow) + 1) * 2, len(song_table))
        self.assertTrue(song_table.startswith(expected_prefix))
        self.assertEqual(bytes(len(song_table) - len(expected_prefix)), song_table[len(expected_prefix):])
