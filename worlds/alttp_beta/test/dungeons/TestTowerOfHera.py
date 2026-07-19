from worlds.alttp_beta.PuzzleShuffle import (
    PuzzleShuffleState,
    TAG_LIGHT_TORCHES_TO_GET_CHEST,
    TAG_NW_KILL_ENEMY_TO_OPEN,
    TAG_SE_KILL_ENEMY_FOR_CHEST,
    TAG_SWITCH_OPENS_DOOR_HOLD,
    TAG_SWITCH_OPENS_DOOR_TOGGLE,
    TAG_TRIGGER_ACTIVATED_CHEST,
)

from .TestDungeon import TestDungeon


class TestTowerOfHera(TestDungeon):

    def testTowerOfHera(self):
        self.starting_regions = ['Tower of Hera (Bottom)']
        self.run_tests([
            ["Tower of Hera - Big Key Chest", False, []],
            ["Tower of Hera - Big Key Chest", False, [], ['Small Key (Tower of Hera)']],
            ["Tower of Hera - Big Key Chest", False, [], ['Lamp', 'Fire Rod']],
            ["Tower of Hera - Big Key Chest", True, ['Small Key (Tower of Hera)', 'Lamp', 'Bomb Upgrade (50)']],
            ["Tower of Hera - Big Key Chest", True, ['Small Key (Tower of Hera)', 'Fire Rod']],

            ["Tower of Hera - Basement Cage", False, []],
            ["Tower of Hera - Basement Cage", True, ['Bomb Upgrade (50)']],
            ["Tower of Hera - Basement Cage", True, ['Progressive Sword']],

            ["Tower of Hera - Map Chest", False, []],
            ["Tower of Hera - Map Chest", True, ['Bomb Upgrade (50)']],
            ["Tower of Hera - Map Chest", True, ['Progressive Sword']],

            ["Tower of Hera - Compass Chest", False, []],
            ["Tower of Hera - Compass Chest", False, [], ['Big Key (Tower of Hera)']],
            ["Tower of Hera - Compass Chest", False, ['Big Key (Tower of Hera)', 'Progressive Bow']],
            ["Tower of Hera - Compass Chest", True, ['Big Key (Tower of Hera)', 'Progressive Sword']],
            ["Tower of Hera - Compass Chest", True, ['Big Key (Tower of Hera)', 'Hammer']],
            ["Tower of Hera - Compass Chest", True, ['Big Key (Tower of Hera)', 'Silver Bow']],

            ["Tower of Hera - Big Chest", False, []],
            ["Tower of Hera - Big Chest", False, [], ['Big Key (Tower of Hera)']],
            ["Tower of Hera - Big Chest", True, ['Big Key (Tower of Hera)', 'Progressive Sword']],

            ["Tower of Hera - Boss", False, []],
            ["Tower of Hera - Boss", False, [], ['Big Key (Tower of Hera)']],
            ["Tower of Hera - Boss", False, [], ['Progressive Sword', 'Hammer']],
            ["Tower of Hera - Boss", True, ['Progressive Sword', 'Big Key (Tower of Hera)']],
            ["Tower of Hera - Boss", True, ['Hammer', 'Big Key (Tower of Hera)']],
        ])

    def testBigKeyChestCanRequireSoutheastEnemyClear(self):
        self.starting_regions = ['Tower of Hera (Bottom)']
        self.rebuild_with_puzzle_shuffle(PuzzleShuffleState(
            desert_map_chest_tag=TAG_LIGHT_TORCHES_TO_GET_CHEST,
            desert_big_chest_tag=TAG_SWITCH_OPENS_DOOR_TOGGLE,
            hera_big_key_chest_tag=TAG_SE_KILL_ENEMY_FOR_CHEST,
            hera_tile_room_tag=TAG_NW_KILL_ENEMY_TO_OPEN,
        ))

        self.run_tests([
            ["Tower of Hera - Big Key Chest", False, ['Small Key (Tower of Hera)']],
            ["Tower of Hera - Big Key Chest", True, ['Small Key (Tower of Hera)', 'Progressive Sword']],
        ])

    def testBigKeyChestTriggerTagDoesNotRequireFireSource(self):
        self.starting_regions = ['Tower of Hera (Bottom)']
        self.rebuild_with_puzzle_shuffle(PuzzleShuffleState(
            desert_map_chest_tag=TAG_LIGHT_TORCHES_TO_GET_CHEST,
            desert_big_chest_tag=TAG_SWITCH_OPENS_DOOR_TOGGLE,
            hera_big_key_chest_tag=TAG_TRIGGER_ACTIVATED_CHEST,
            hera_tile_room_tag=TAG_NW_KILL_ENEMY_TO_OPEN,
            hera_big_key_chest_switch_pot=(76, 20),
        ))

        self.run_tests([
            ["Tower of Hera - Big Key Chest", True, ['Small Key (Tower of Hera)', 'Progressive Sword']],
        ])

    def testBigKeyChestHoldDoorRequiresSomaria(self):
        self.starting_regions = ['Tower of Hera (Bottom)']
        self.rebuild_with_puzzle_shuffle(PuzzleShuffleState(
            desert_map_chest_tag=TAG_LIGHT_TORCHES_TO_GET_CHEST,
            desert_big_chest_tag=TAG_SWITCH_OPENS_DOOR_TOGGLE,
            hera_big_key_chest_tag=TAG_LIGHT_TORCHES_TO_GET_CHEST,
            hera_tile_room_tag=TAG_SWITCH_OPENS_DOOR_HOLD,
            hera_tile_room_switch_pot=(12, 11),
        ))

        self.run_tests([
            ["Tower of Hera - Big Key Chest", False, ['Small Key (Tower of Hera)', 'Lamp']],
            ["Tower of Hera - Big Key Chest", True, ['Small Key (Tower of Hera)', 'Lamp', 'Cane of Somaria']],
        ])
