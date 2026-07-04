from .TestDungeon import TestDungeon
from worlds.alttp.PotShuffle import FilledPot, POT_KEY


class TestThievesTown(TestDungeon):
    
    def testThievesTown(self):
        self.starting_regions = ['Thieves Town (Entrance)']
        self.run_tests([

            ["Thieves' Town - Big Key Chest", True, []],

            ["Thieves' Town - Map Chest", True, []],

            ["Thieves' Town - Compass Chest", True, []],

            ["Thieves' Town - Ambush Chest", True, []],

            ["Thieves' Town - Hallway Pot Key", False, []],
            ["Thieves' Town - Hallway Pot Key", False, [], ['Big Key (Thieves Town)']],
            ["Thieves' Town - Hallway Pot Key", True, ['Big Key (Thieves Town)']],

            ["Thieves' Town - Spike Switch Pot Key", False, []],
            ["Thieves' Town - Spike Switch Pot Key", False, [], ['Big Key (Thieves Town)']],
            ["Thieves' Town - Spike Switch Pot Key", False, [], ['Small Key (Thieves Town)']],
            ["Thieves' Town - Spike Switch Pot Key", True, ['Big Key (Thieves Town)', 'Small Key (Thieves Town)']],

            ["Thieves' Town - Attic", False, []],
            ["Thieves' Town - Attic", False, [], ['Big Key (Thieves Town)']],
            ["Thieves' Town - Attic", False, [], ['Small Key (Thieves Town)']],
            ["Thieves' Town - Attic", True, ['Big Key (Thieves Town)', 'Small Key (Thieves Town)', 'Small Key (Thieves Town)', 'Small Key (Thieves Town)']],

            ["Thieves' Town - Big Chest", False, []],
            ["Thieves' Town - Big Chest", False, [], ['Big Key (Thieves Town)']],
            ["Thieves' Town - Big Chest", False, [], ['Small Key (Thieves Town)']],
            ["Thieves' Town - Big Chest", False, [], ['Hammer']],
            ["Thieves' Town - Big Chest", True, ['Hammer', 'Small Key (Thieves Town)', 'Small Key (Thieves Town)', 'Small Key (Thieves Town)', 'Big Key (Thieves Town)']],

            ["Thieves' Town - Blind's Cell", False, []],
            ["Thieves' Town - Blind's Cell", False, [], ['Big Key (Thieves Town)']],
            ["Thieves' Town - Blind's Cell", False, [], ['Small Key (Thieves Town)']],
            ["Thieves' Town - Blind's Cell", True, ['Big Key (Thieves Town)', 'Small Key (Thieves Town)', 'Power Glove']],
            ["Thieves' Town - Blind's Cell", True, ['Big Key (Thieves Town)', 'Small Key (Thieves Town)', 'Hammer']],

            ["Thieves' Town - Boss", False, []],
            ["Thieves' Town - Boss", False, [], ['Big Key (Thieves Town)']],
            ["Thieves' Town - Boss", False, [], ['Hammer', 'Progressive Sword', 'Cane of Somaria', 'Cane of Byrna']],
            ["Thieves' Town - Boss", False, [], ['Bomb Upgrade (+5)', 'Bomb Upgrade (+10)', 'Bomb Upgrade (50)']],
            ["Thieves' Town - Boss", True, ['Bomb Upgrade (+5)', 'Small Key (Thieves Town)', 'Small Key (Thieves Town)', 'Small Key (Thieves Town)', 'Big Key (Thieves Town)', 'Hammer']],
            ["Thieves' Town - Boss", True, ['Bomb Upgrade (+5)', 'Small Key (Thieves Town)', 'Small Key (Thieves Town)', 'Small Key (Thieves Town)', 'Big Key (Thieves Town)', 'Progressive Sword']],
            ["Thieves' Town - Boss", True, ['Bomb Upgrade (+5)', 'Small Key (Thieves Town)', 'Small Key (Thieves Town)', 'Small Key (Thieves Town)', 'Big Key (Thieves Town)', 'Cane of Somaria']],
            ["Thieves' Town - Boss", True, ['Bomb Upgrade (+5)', 'Small Key (Thieves Town)', 'Small Key (Thieves Town)', 'Small Key (Thieves Town)', 'Big Key (Thieves Town)', 'Cane of Byrna']],
        ])

    def testThievesTownPotShuffleHallwayKeyLogic(self):
        self.rebuild_with_pot_shuffle(self.get_test_pot_shuffle_state())
        self.starting_regions = ['Thieves Town (Entrance)']
        self.run_tests([
            ["Thieves' Town - Hallway Pot Key", False, []],
            ["Thieves' Town - Hallway Pot Key", True, ['Big Key (Thieves Town)']],
        ])

        self.rebuild_with_pot_shuffle(self.get_test_pot_shuffle_state({
            0xBC: (FilledPot(28, 27, POT_KEY),),
        }))
        self.starting_regions = ['Thieves Town (Entrance)']
        self.run_tests([
            ["Thieves' Town - Hallway Pot Key", False, []],
            ["Thieves' Town - Hallway Pot Key", False, ['Big Key (Thieves Town)']],
            ["Thieves' Town - Hallway Pot Key", True, ['Bomb Upgrade (+5)']],
        ])

        self.rebuild_with_pot_shuffle(self.get_test_pot_shuffle_state({
            0xBC: (FilledPot(48, 20, POT_KEY),),
        }))
        self.starting_regions = ['Thieves Town (Entrance)']
        self.run_tests([
            ["Thieves' Town - Hallway Pot Key", False, []],
            ["Thieves' Town - Hallway Pot Key", False, ['Big Key (Thieves Town)']],
            ["Thieves' Town - Hallway Pot Key", False, ['Small Key (Thieves Town)']],
            ["Thieves' Town - Hallway Pot Key", True, ['Big Key (Thieves Town)', 'Small Key (Thieves Town)']],
        ])

        self.rebuild_with_pot_shuffle(self.get_test_pot_shuffle_state({
            0xBC: (FilledPot(138, 3, POT_KEY),),
        }))
        self.starting_regions = ['Thieves Town (Entrance)']
        self.run_tests([
            ["Thieves' Town - Hallway Pot Key", False, []],
            ["Thieves' Town - Hallway Pot Key", False, ['Big Key (Thieves Town)', 'Small Key (Thieves Town)']],
            ["Thieves' Town - Hallway Pot Key", True, ['Big Key (Thieves Town)', 'Small Key (Thieves Town)', 'Progressive Sword']],
        ])
