import random
import unittest
from types import SimpleNamespace

from worlds.alttp.EnemyShuffle import RandomizedDungeonEnemyRoom, RandomizedDungeonEnemySprite
from worlds.alttp.PotShuffle import FilledPot, POT_HEART, POT_KEY, POT_SWITCH, generate_pot_shuffle
from worlds.alttp.PuzzleShuffle import (
    GT_BIG_CHEST_ROOM_ID,
    GT_BLOCK_PUZZLE_ROOM_ID,
    HERA_TILE_ROOM_ID,
    EASTERN_PRE_ARMOS_ROOM_ID,
    ICE_PALACE_BLOCK_PUZZLE_ROOM_ID,
    ICE_PALACE_PENGATOR_BIG_KEY_ROOM_ID,
    POD_MIMICS_MOVING_WALL_ROOM_ID,
    DESERT_BIG_CHEST_BASE_TAG_CHOICES,
    DESERT_BIG_CHEST_ROOM_ID,
    DESERT_FINAL_SECTION_ENTRANCE_BASE_TAG_CHOICES,
    DESERT_FINAL_SECTION_ENTRANCE_ROOM_ID,
    DESERT_MAP_CHEST_ROOM_ID,
    DESERT_MAP_CHEST_TAG_CHOICES,
    PuzzleShuffleState,
    TAG_LIGHT_TORCHES_TO_GET_CHEST,
    decode_puzzle_shuffle,
    encode_puzzle_shuffle,
    generate_puzzle_shuffle,
    get_gt_big_chest_room_tag_choices,
    get_gt_block_puzzle_tag_choices,
    get_hera_big_key_chest_tag_choices,
    get_hera_tile_room_tag_choices,
    get_eastern_pre_armos_tag_choices,
    get_desert_big_chest_tag_choices,
    get_desert_final_section_entrance_tag_choices,
    apply_puzzle_pot_modifications,
    TAG_E_KILL_ENEMY_TO_OPEN,
    TAG_NE_KILL_ENEMY_FOR_CHEST,
    TAG_NE_KILL_ENEMY_TO_OPEN,
    TAG_NE_MOVE_BLOCK_TO_OPEN,
    TAG_NW_KILL_ENEMY_TO_OPEN,
    TAG_N_KILL_ENEMY_FOR_CHEST,
    TAG_PULL_LEVER_TO_OPEN,
    TAG_SE_KILL_ENEMY_FOR_CHEST,
    TAG_SE_KILL_ENEMY_TO_OPEN,
    TAG_SW_KILL_ENEMY_TO_OPEN,
    TAG_SW_MOVE_BLOCK_TO_OPEN,
    TAG_SWITCH_OPENS_DOOR_TOGGLE,
    TAG_SWITCH_OPENS_DOOR_HOLD,
    TAG_TRIGGER_ACTIVATED_CHEST,
    validate_puzzle_shuffle_data,
)


class TestPuzzleShuffle(unittest.TestCase):
    def test_desert_map_chest_vanilla_data_matches_expected_puzzle(self) -> None:
        validate_puzzle_shuffle_data()

    def test_generate_puzzle_shuffle_uses_known_desert_map_chest_tags(self) -> None:
        for seed in range(20):
            world = SimpleNamespace(
                random=random.Random(seed),
                options=SimpleNamespace(enemy_shuffle=False),
                enemy_shuffle_state=None,
            )

            state = generate_puzzle_shuffle(world)

            self.assertIn(state.desert_map_chest_tag, DESERT_MAP_CHEST_TAG_CHOICES)
            self.assertIn(state.desert_big_chest_tag, DESERT_BIG_CHEST_BASE_TAG_CHOICES)
            self.assertIn(
                state.desert_final_section_entrance_tag,
                DESERT_FINAL_SECTION_ENTRANCE_BASE_TAG_CHOICES,
            )

    def test_puzzle_shuffle_state_round_trips(self) -> None:
        state = PuzzleShuffleState(
            desert_map_chest_tag=DESERT_MAP_CHEST_TAG_CHOICES[-1],
            desert_big_chest_tag=TAG_SWITCH_OPENS_DOOR_HOLD,
            hera_big_key_chest_tag=TAG_TRIGGER_ACTIVATED_CHEST,
            hera_tile_room_tag=TAG_SWITCH_OPENS_DOOR_TOGGLE,
            hera_big_key_chest_switch_pot=(76, 20),
            hera_tile_room_switch_pot=(12, 11),
            eastern_pre_armos_northeast_switch_pot=(202, 8),
            eastern_pre_armos_southeast_switch_pot=(92, 24),
        )

        self.assertEqual(decode_puzzle_shuffle(encode_puzzle_shuffle(state)), state)

    def test_desert_big_chest_kill_enemy_tag_is_not_available_with_vanilla_beamos(self) -> None:
        world = SimpleNamespace(
            options=SimpleNamespace(enemy_shuffle=False),
            enemy_shuffle_state=None,
        )

        self.assertNotIn(TAG_NW_KILL_ENEMY_TO_OPEN, get_desert_big_chest_tag_choices(world))

    def test_desert_big_chest_kill_enemy_tag_is_available_with_shuffled_killable_enemy(self) -> None:
        world = SimpleNamespace(
            options=SimpleNamespace(enemy_shuffle=True),
            enemy_shuffle_state=SimpleNamespace(
                randomized_dungeon_rooms={
                    DESERT_BIG_CHEST_ROOM_ID: RandomizedDungeonEnemyRoom(
                        room_id=DESERT_BIG_CHEST_ROOM_ID,
                        room_header_address=0,
                        sprite_table_address=0,
                        original_graphics_block_id=0,
                        graphics_block_id=0,
                        tag_1=0,
                        tag_2=0,
                        sort_sprites_value=0,
                        sprites=(
                            RandomizedDungeonEnemySprite(0, 0x17, 0x09, 0x63, 0x8E, False, False),
                        ),
                        skipped_randomization=False,
                    )
                }
            ),
        )

        self.assertIn(TAG_NW_KILL_ENEMY_TO_OPEN, get_desert_big_chest_tag_choices(world))

    def test_desert_final_section_kill_enemy_tag_is_not_available_with_vanilla_beamos(self) -> None:
        world = SimpleNamespace(
            options=SimpleNamespace(enemy_shuffle=False),
            enemy_shuffle_state=None,
        )

        self.assertEqual(
            (TAG_SW_MOVE_BLOCK_TO_OPEN,),
            get_desert_final_section_entrance_tag_choices(world),
        )

    def test_desert_final_section_kill_enemy_tag_is_available_with_shuffled_killable_enemy(self) -> None:
        world = SimpleNamespace(
            options=SimpleNamespace(enemy_shuffle=True),
            enemy_shuffle_state=SimpleNamespace(
                randomized_dungeon_rooms={
                    DESERT_FINAL_SECTION_ENTRANCE_ROOM_ID: RandomizedDungeonEnemyRoom(
                        room_id=DESERT_FINAL_SECTION_ENTRANCE_ROOM_ID,
                        room_header_address=0,
                        sprite_table_address=0,
                        original_graphics_block_id=0,
                        graphics_block_id=0,
                        tag_1=0,
                        tag_2=0,
                        sort_sprites_value=0,
                        sprites=(
                            RandomizedDungeonEnemySprite(0, 0x17, 0x09, 0x63, 0x8E, False, False),
                        ),
                        skipped_randomization=False,
                    )
                }
            ),
        )

        self.assertIn(TAG_SW_KILL_ENEMY_TO_OPEN, get_desert_final_section_entrance_tag_choices(world))

    def test_desert_map_chest_switch_is_removed_from_pot_shuffle_state(self) -> None:
        world = SimpleNamespace(
            random=random.Random(0),
            options=SimpleNamespace(retro_bow=False),
        )
        state = generate_pot_shuffle(world)
        self.assertTrue(any(pot.item == POT_SWITCH for pot in state[DESERT_MAP_CHEST_ROOM_ID]))

        state = apply_puzzle_pot_modifications(
            state,
            PuzzleShuffleState(
                desert_map_chest_tag=TAG_N_KILL_ENEMY_FOR_CHEST,
                desert_big_chest_tag=TAG_SWITCH_OPENS_DOOR_HOLD,
            ),
        )

        self.assertIsNotNone(state)
        self.assertFalse(any(pot.item == POT_SWITCH for pot in state[DESERT_MAP_CHEST_ROOM_ID]))

    def test_desert_map_chest_switch_removal_preserves_other_room_pots(self) -> None:
        state = {
            DESERT_MAP_CHEST_ROOM_ID: (
                FilledPot(62, 5, POT_SWITCH),
                FilledPot(30, 5, 0x0C),
            ),
        }

        state = apply_puzzle_pot_modifications(
            state,
            PuzzleShuffleState(
                desert_map_chest_tag=TAG_N_KILL_ENEMY_FOR_CHEST,
                desert_big_chest_tag=TAG_SWITCH_OPENS_DOOR_HOLD,
            ),
        )

        self.assertEqual(state[DESERT_MAP_CHEST_ROOM_ID], (FilledPot(30, 5, 0x0C),))

    def test_hera_trigger_chest_tag_requires_item_in_bottom_right_pots(self) -> None:
        world = SimpleNamespace(
            pot_shuffle_state=None,
            options=SimpleNamespace(enemy_shuffle=False),
            enemy_shuffle_state=None,
        )

        self.assertIn(TAG_TRIGGER_ACTIVATED_CHEST, get_hera_big_key_chest_tag_choices(world))

        world.pot_shuffle_state = {
            HERA_TILE_ROOM_ID: (
                FilledPot(12, 11, 0x0C),
                FilledPot(16, 11, 0x0D),
            )
        }

        self.assertNotIn(TAG_TRIGGER_ACTIVATED_CHEST, get_hera_big_key_chest_tag_choices(world))

    def test_hera_switch_door_tags_require_item_in_west_pots(self) -> None:
        world = SimpleNamespace(
            pot_shuffle_state=None,
            options=SimpleNamespace(enemy_shuffle=False),
            enemy_shuffle_state=None,
        )

        self.assertEqual(get_hera_tile_room_tag_choices(world), (TAG_NW_KILL_ENEMY_TO_OPEN,))

        world.pot_shuffle_state = {
            HERA_TILE_ROOM_ID: (
                FilledPot(12, 11, 0x0C),
                FilledPot(76, 20, 0x0D),
            )
        }

        self.assertIn(TAG_SWITCH_OPENS_DOOR_TOGGLE, get_hera_tile_room_tag_choices(world))
        self.assertIn(TAG_SWITCH_OPENS_DOOR_HOLD, get_hera_tile_room_tag_choices(world))

    def test_hera_switch_tags_replace_existing_pot_items(self) -> None:
        state = {
            HERA_TILE_ROOM_ID: (
                FilledPot(12, 11, 0x0C),
                FilledPot(76, 20, 0x0D),
            )
        }

        state = apply_puzzle_pot_modifications(
            state,
            PuzzleShuffleState(
                desert_map_chest_tag=TAG_LIGHT_TORCHES_TO_GET_CHEST,
                desert_big_chest_tag=TAG_SWITCH_OPENS_DOOR_HOLD,
                hera_big_key_chest_tag=TAG_TRIGGER_ACTIVATED_CHEST,
                hera_tile_room_tag=TAG_SWITCH_OPENS_DOOR_HOLD,
                hera_big_key_chest_switch_pot=(76, 20),
                hera_tile_room_switch_pot=(12, 11),
            ),
        )

        self.assertEqual(
            state[HERA_TILE_ROOM_ID],
            (
                FilledPot(12, 11, POT_SWITCH),
                FilledPot(76, 20, POT_SWITCH),
            ),
        )

    def test_gt_block_puzzle_switch_tags_require_non_key_item_in_top_right(self) -> None:
        world = SimpleNamespace(
            pot_shuffle_state={
                GT_BLOCK_PUZZLE_ROOM_ID: (
                    FilledPot(112, 12, POT_KEY),
                ),
            },
            options=SimpleNamespace(enemy_shuffle=False),
            enemy_shuffle_state=None,
        )

        self.assertEqual(
            get_gt_block_puzzle_tag_choices(world),
            (TAG_NE_MOVE_BLOCK_TO_OPEN, TAG_NE_KILL_ENEMY_FOR_CHEST),
        )

        world.pot_shuffle_state = {
            GT_BLOCK_PUZZLE_ROOM_ID: (
                FilledPot(76, 12, 0x0C),
                FilledPot(112, 12, POT_KEY),
            ),
        }

        self.assertIn(TAG_SWITCH_OPENS_DOOR_TOGGLE, get_gt_block_puzzle_tag_choices(world))
        self.assertIn(TAG_SWITCH_OPENS_DOOR_HOLD, get_gt_block_puzzle_tag_choices(world))

    def test_gt_block_puzzle_switch_tag_replaces_selected_non_key_item(self) -> None:
        state = {
            GT_BLOCK_PUZZLE_ROOM_ID: (
                FilledPot(76, 12, 0x0C),
                FilledPot(112, 12, POT_KEY),
            ),
        }

        state = apply_puzzle_pot_modifications(
            state,
            PuzzleShuffleState(
                desert_map_chest_tag=TAG_LIGHT_TORCHES_TO_GET_CHEST,
                desert_big_chest_tag=TAG_SWITCH_OPENS_DOOR_HOLD,
                gt_block_puzzle_tag=TAG_SWITCH_OPENS_DOOR_HOLD,
                gt_block_puzzle_switch_pot=(76, 12),
            ),
        )

        self.assertEqual(
            state[GT_BLOCK_PUZZLE_ROOM_ID],
            (
                FilledPot(76, 12, POT_SWITCH),
                FilledPot(112, 12, POT_KEY),
            ),
        )

    def test_gt_big_chest_room_kill_enemy_tag_requires_shuffled_killable_enemy(self) -> None:
        world = SimpleNamespace(
            options=SimpleNamespace(enemy_shuffle=False),
            enemy_shuffle_state=None,
        )

        self.assertNotIn(TAG_NE_KILL_ENEMY_TO_OPEN, get_gt_big_chest_room_tag_choices(world))
        self.assertIn(TAG_PULL_LEVER_TO_OPEN, get_gt_big_chest_room_tag_choices(world))
        self.assertIn(TAG_SWITCH_OPENS_DOOR_TOGGLE, get_gt_big_chest_room_tag_choices(world))

        world.options.enemy_shuffle = True
        world.enemy_shuffle_state = SimpleNamespace(
            randomized_dungeon_rooms={
                GT_BIG_CHEST_ROOM_ID: RandomizedDungeonEnemyRoom(
                    room_id=GT_BIG_CHEST_ROOM_ID,
                    room_header_address=0,
                    sprite_table_address=0,
                    original_graphics_block_id=0,
                    graphics_block_id=0,
                    tag_1=0,
                    tag_2=0,
                    sort_sprites_value=0,
                    sprites=(
                        RandomizedDungeonEnemySprite(0, 0x05, 0x17, 0x63, 0x84, False, False),
                    ),
                    skipped_randomization=False,
                )
            }
        )

        self.assertIn(TAG_NE_KILL_ENEMY_TO_OPEN, get_gt_big_chest_room_tag_choices(world))

    def test_gt_big_chest_room_non_switch_tags_remove_pot_switch(self) -> None:
        state = {
            GT_BIG_CHEST_ROOM_ID: (
                FilledPot(76, 12, POT_SWITCH),
                FilledPot(24, 20, 0x0C),
            ),
        }

        state = apply_puzzle_pot_modifications(
            state,
            PuzzleShuffleState(
                desert_map_chest_tag=TAG_LIGHT_TORCHES_TO_GET_CHEST,
                desert_big_chest_tag=TAG_SWITCH_OPENS_DOOR_HOLD,
                gt_big_chest_room_tag=TAG_PULL_LEVER_TO_OPEN,
            ),
        )

        self.assertEqual(
            state[GT_BIG_CHEST_ROOM_ID],
            (
                FilledPot(76, 12, POT_HEART),
                FilledPot(24, 20, 0x0C),
            ),
        )

    def test_eastern_pre_armos_switch_tags_replace_northeast_and_southeast_pots(self) -> None:
        world = SimpleNamespace(
            pot_shuffle_state={
                EASTERN_PRE_ARMOS_ROOM_ID: (
                    FilledPot(202, 8, 0x0B),
                    FilledPot(92, 24, 0x0B),
                ),
            },
            options=SimpleNamespace(enemy_shuffle=False),
            enemy_shuffle_state=None,
        )

        self.assertIn(TAG_SWITCH_OPENS_DOOR_TOGGLE, get_eastern_pre_armos_tag_choices(world))
        self.assertIn(TAG_SWITCH_OPENS_DOOR_HOLD, get_eastern_pre_armos_tag_choices(world))

        state = apply_puzzle_pot_modifications(
            world.pot_shuffle_state,
            PuzzleShuffleState(
                desert_map_chest_tag=TAG_LIGHT_TORCHES_TO_GET_CHEST,
                desert_big_chest_tag=TAG_SWITCH_OPENS_DOOR_HOLD,
                eastern_pre_armos_tag=TAG_SWITCH_OPENS_DOOR_HOLD,
                eastern_pre_armos_northeast_switch_pot=(202, 8),
                eastern_pre_armos_southeast_switch_pot=(92, 24),
            ),
        )

        self.assertEqual(
            state[EASTERN_PRE_ARMOS_ROOM_ID],
            (
                FilledPot(202, 8, POT_SWITCH),
                FilledPot(92, 24, POT_SWITCH),
            ),
        )

    def test_eastern_pre_armos_switch_tags_require_pots_on_both_sides(self) -> None:
        world = SimpleNamespace(
            pot_shuffle_state={
                EASTERN_PRE_ARMOS_ROOM_ID: (
                    FilledPot(202, 8, 0x0B),
                ),
            },
            options=SimpleNamespace(enemy_shuffle=False),
            enemy_shuffle_state=None,
        )

        self.assertEqual(get_eastern_pre_armos_tag_choices(world), (TAG_E_KILL_ENEMY_TO_OPEN,))

    def test_ice_palace_block_puzzle_non_switch_tag_removes_pot_switch(self) -> None:
        state = {
            ICE_PALACE_BLOCK_PUZZLE_ROOM_ID: (
                FilledPot(92, 25, POT_SWITCH),
            ),
        }

        state = apply_puzzle_pot_modifications(
            state,
            PuzzleShuffleState(
                desert_map_chest_tag=TAG_LIGHT_TORCHES_TO_GET_CHEST,
                desert_big_chest_tag=TAG_SWITCH_OPENS_DOOR_HOLD,
                ice_palace_block_puzzle_tag=TAG_SE_KILL_ENEMY_TO_OPEN,
            ),
        )

        self.assertEqual(
            state[ICE_PALACE_BLOCK_PUZZLE_ROOM_ID],
            (
                FilledPot(92, 25, POT_HEART),
            ),
        )

    def test_pod_mimics_moving_wall_switch_tag_adds_pot_switch(self) -> None:
        state = {
            POD_MIMICS_MOVING_WALL_ROOM_ID: (
                FilledPot(20, 23, 0x09),
                FilledPot(40, 23, 0x09),
            ),
        }

        state = apply_puzzle_pot_modifications(
            state,
            PuzzleShuffleState(
                desert_map_chest_tag=TAG_LIGHT_TORCHES_TO_GET_CHEST,
                desert_big_chest_tag=TAG_SWITCH_OPENS_DOOR_HOLD,
                pod_mimics_moving_wall_room_tag=TAG_SWITCH_OPENS_DOOR_HOLD,
                pod_mimics_moving_wall_switch_pot=(20, 23),
            ),
        )

        self.assertEqual(
            state[POD_MIMICS_MOVING_WALL_ROOM_ID],
            (
                FilledPot(20, 23, POT_SWITCH),
                FilledPot(40, 23, 0x09),
            ),
        )

    def test_ice_palace_pengator_big_key_kill_tag_removes_pot_switch(self) -> None:
        state = {
            ICE_PALACE_PENGATOR_BIG_KEY_ROOM_ID: (
                FilledPot(28, 25, POT_SWITCH),
                FilledPot(28, 23, 0x0B),
            ),
        }

        state = apply_puzzle_pot_modifications(
            state,
            PuzzleShuffleState(
                desert_map_chest_tag=TAG_LIGHT_TORCHES_TO_GET_CHEST,
                desert_big_chest_tag=TAG_SWITCH_OPENS_DOOR_HOLD,
                ice_palace_pengator_big_key_room_tag=TAG_SW_KILL_ENEMY_TO_OPEN,
            ),
        )

        self.assertEqual(
            state[ICE_PALACE_PENGATOR_BIG_KEY_ROOM_ID],
            (
                FilledPot(28, 25, POT_HEART),
                FilledPot(28, 23, 0x0B),
            ),
        )


if __name__ == "__main__":
    unittest.main()
