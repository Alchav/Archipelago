import unittest

from worlds.alttp.enemizer_data.vanilla_room_tags import ROOM_TAG_NAMES, VANILLA_ROOM_TAGS


class TestRoomTags(unittest.TestCase):
    def test_vanilla_room_tags_cover_all_jp_dungeon_rooms(self) -> None:
        self.assertEqual(len(VANILLA_ROOM_TAGS), 0x128)
        self.assertEqual(set(VANILLA_ROOM_TAGS), set(range(0x128)))

    def test_vanilla_room_tags_use_known_tag_ids(self) -> None:
        self.assertEqual(len(ROOM_TAG_NAMES), 0x40)

        for room_id, tags in VANILLA_ROOM_TAGS.items():
            with self.subTest(room=room_id):
                self.assertLess(tags.tag_1, len(ROOM_TAG_NAMES))
                self.assertLess(tags.tag_2, len(ROOM_TAG_NAMES))

    def test_known_room_tags(self) -> None:
        self.assertEqual(VANILLA_ROOM_TAGS[0x000].tag_1, 0x3D)
        self.assertEqual(ROOM_TAG_NAMES[VANILLA_ROOM_TAGS[0x000].tag_1], "Kill to open Ganon's door")
        self.assertEqual(VANILLA_ROOM_TAGS[0x00D].tag_1, 0x38)
        self.assertEqual(ROOM_TAG_NAMES[VANILLA_ROOM_TAGS[0x00D].tag_1], "Agahnim's room")


if __name__ == "__main__":
    unittest.main()
