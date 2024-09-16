import typing
from typing import Dict

from BaseClasses import Location


class FFTALocation(Location):
    game: str = "Final Fantasy Tactics Advance"


class FFTALocationData(typing.NamedTuple):
    name: str
    mission_id: int
    rom_address: int


MissionGroups = []
DispatchMissionGroups = []
bitflags = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80]

FFTALocations: typing.List[FFTALocationData] = [
    # Decide whether to use address or memory offset from data array

    FFTALocationData('Herb Picking Reward 1', 0, 0x55AF40),
    FFTALocationData('Herb Picking Reward 2', 0, 0x55AF42),

    FFTALocationData('Thesis Hunt Reward 1', 1, 0x55AF86),
    FFTALocationData('Thesis Hunt Reward 2', 1, 0x55AF88),

    FFTALocationData('The Cheetahs Reward 1', 2, 0x55AFCC),
    FFTALocationData('The Cheetahs Reward 2', 2, 0x55AFCE),

    FFTALocationData('Desert Peril Reward 1', 3, 0x55b012),
    FFTALocationData('Desert Peril Reward 2', 3, 0x55b014),

    FFTALocationData('Twisted Flow Reward 1', 4, 0x55b058),
    FFTALocationData('Twisted Flow Reward 2', 4, 0x55b05a),

    FFTALocationData('Antilaws Reward 1', 5, 0x55b09e),
    FFTALocationData('Antilaws Reward 2', 5, 0x55b0a0),

    FFTALocationData('Diamond Rain Reward 1', 6, 0x55b0e4),
    FFTALocationData('Diamond Rain Reward 2', 6, 0x55b0e6),

    FFTALocationData('Hot Awakening Reward 1', 7, 0x55b12a),
    FFTALocationData('Hot Awakening Reward 2', 7, 0x55b12c),

    FFTALocationData('Magic Wood Reward 1', 8, 0x55b170),
    FFTALocationData('Magic Wood Reward 2', 8, 0x55b172),

    FFTALocationData('Emerald Keep Reward 1', 9, 0x55b1b6),
    FFTALocationData('Emerald Keep Reward 2', 9, 0x55b1b8),

    FFTALocationData('Pale Company Reward 1', 10,  0x55b1fc),
    FFTALocationData('Pale Company Reward 2', 10,  0x55b1fe),

    FFTALocationData('Jagd Hunt Reward 1', 11, 0x55b242),
    FFTALocationData('Jagd Hunt Reward 2', 11, 0x55b244),

    FFTALocationData('The Bounty Reward 1', 12, 0x55b288),
    FFTALocationData('The Bounty Reward 2', 12, 0x55b28a),

    FFTALocationData('Golden Clock Reward 1', 13, 0x55b2ce),
    FFTALocationData('Golden Clock Reward 2', 13, 0x55b2d0),

    FFTALocationData('Scouring Time Reward 1', 14, 0x55b314),
    FFTALocationData('Scouring Time Reward 2', 14, 0x55b316),

    FFTALocationData('The Big Find Reward 1', 15, 0x55b35a),
    FFTALocationData('The Big Find Reward 2', 15, 0x55b35c),

    FFTALocationData('Desert Patrol Reward 1', 16, 0x55b3a0),
    FFTALocationData('Desert Patrol Reward 2', 16, 0x55b3a2),

    FFTALocationData('Quiet Sands Reward 1', 17, 0x55b3e6),
    FFTALocationData('Quiet Sands Reward 2', 17, 0x55b3e8),

    FFTALocationData('Materite Now! Reward 1', 18, 0x55b42c),
    FFTALocationData('Materite Now! Reward 2', 18, 0x55b42e),

    FFTALocationData('Present Day Reward 1', 19, 0x55b472),
    FFTALocationData('Present Day Reward 2', 19, 0x55b474),

    FFTALocationData('Hidden Vein Reward 1', 20, 0x55b4b8),
    FFTALocationData('Hidden Vein Reward 2', 20, 0x55b4ba),

    FFTALocationData('To Ambervale Reward 1', 21, 0x55b4fe),
    FFTALocationData('To Ambervale Reward 2', 21, 0x55b500),

    FFTALocationData('Over The Hill Reward 1', 22, 0x55b544),
    FFTALocationData('Over The Hill Reward 2', 22, 0x55b546),

    # Non story missions
    FFTALocationData('Wanted! Black Mage Dolce Reward 1', 25, 0x55b616),
    FFTALocationData('Wanted! Black Mage Dolce Reward 2', 25, 0x55b618),

    FFTALocationData('Wanted! Gabbana Brothers Reward 1', 26, 0x55b65c),
    FFTALocationData('Wanted! Gabbana Brothers Reward 2', 26,  0x55b65e),

    FFTALocationData('Wanted! Godeye Reward 1', 27, 0x55b6a2),
    FFTALocationData('Wanted! Godeye Reward 2', 27,  0x55b6a4),

    FFTALocationData('Wanted! Swampking Reward 1', 28, 0x55b6e8),
    FFTALocationData('Wanted! Swampking Reward 2', 28,  0x55b6ea),

    FFTALocationData('Wanted! Killer Rayne Reward 1', 29, 0x55b72e),
    FFTALocationData('Wanted! Killer Rayne Reward 2', 29,  0x55b730),

    FFTALocationData('Wanted! Dark Duke Lodion Reward 1', 30, 0x55b774),
    FFTALocationData('Wanted! Dark Duke Lodion Reward 2', 30,  0x55b776),

    FFTALocationData('Ruby Red Reward 1', 31, 0x55b7ba),
    FFTALocationData('Ruby Red Reward 2', 31,  0x55b7bc),

    FFTALocationData('Tower Ruins Reward 1', 32, 0x55b800),
    FFTALocationData('Tower Ruins Reward 2', 32, 0x55b802),

    FFTALocationData('Battle in Aisen Reward 1', 33, 0x55b846),
    FFTALocationData('Battle in Aisen Reward 2', 33, 0x55b848),

    FFTALocationData('Magewyrm Reward 1', 34, 0x55b88c),
    FFTALocationData('Magewyrm Reward 2', 34, 0x55b88e),

    FFTALocationData('Salika Keep Reward 1', 35, 0x55b8d2),
    FFTALocationData('Salika Keep Reward 2', 35, 0x55b8d4),

    FFTALocationData('Twin Swords Reward 1', 36, 0x55b918),
    FFTALocationData('Twin Swords Reward 2', 36, 0x55b91a),

    FFTALocationData('Village Hunt Reward 1', 37, 0x55b95e),
    FFTALocationData('Village Hunt Reward 2', 37, 0x55b960),

    FFTALocationData('Fire! Fire! Reward 1', 38, 0x55b9a4),
    FFTALocationData('Fire! Fire! Reward 2', 38, 0x55b9a6),

    FFTALocationData('The Wanderer Reward 1', 39, 0x55b9ea),
    FFTALocationData('The Wanderer Reward 2', 39, 0x55b9ec),

    FFTALocationData('Battle Tourney Reward 1', 40, 0x55ba30),
    FFTALocationData('Battle Tourney Reward 2', 40, 0x55ba32),

    FFTALocationData('Mage Tourney Reward 1', 41, 0x55ba76),
    FFTALocationData('Mage Tourney Reward 2', 41, 0x55ba78),

    FFTALocationData('Swimming Meet Reward 1', 42, 0x55babc),
    FFTALocationData('Swimming Meet Reward 2', 42, 0x55babe),

    FFTALocationData('Clan League Reward 1', 43, 0x55bb02),
    FFTALocationData('Clan League Reward 2', 43, 0x55bb04),

    FFTALocationData('Snow in Lutia Reward 1', 44, 0x55bb48),
    FFTALocationData('Snow in Lutia Reward 2', 44, 0x55bb4a),

    FFTALocationData('Frosty Mage Reward 1', 45, 0x55bb8e),
    FFTALocationData('Frosty Mage Reward 2', 45, 0x55bb90),

    FFTALocationData('Prof in Trouble Reward 1', 46, 0x55bbd4),
    FFTALocationData('Prof in Trouble Reward 2', 46, 0x55bbd6),

    FFTALocationData('Hot Recipe Reward 1', 47, 0x55bc1a),
    FFTALocationData('Hot Recipe Reward 2', 47, 0x55bc1c),

    FFTALocationData('S.O.S. Reward 1', 48, 0x55bc60),
    FFTALocationData('S.O.S. Reward 2', 48, 0x55bc62),

    FFTALocationData('A Lost Ring Reward 1', 49, 0x55bca6),
    FFTALocationData('A Lost Ring Reward 2', 49, 0x55bca8),

    FFTALocationData('Staring Eyes Reward 1', 50, 0x55bcec),
    FFTALocationData('Staring Eyes Reward 2', 50, 0x55bcee),

    FFTALocationData('Desert Rose Reward 1', 51, 0x55bd32),
    FFTALocationData('Desert Rose Reward 2', 51, 0x55bd34),

    FFTALocationData('Friend Trouble Reward 1', 52, 0x55bd78),
    FFTALocationData('Friend Trouble Reward 2', 52, 0x55bd7a),

    FFTALocationData('Flesh & Bones Reward 1', 53, 0x55bdbe),
    FFTALocationData('Flesh & Bones Reward 2', 53, 0x55bdc0),

    FFTALocationData('For a Song Reward 1', 54, 0x55be04),
    FFTALocationData('For a Song Reward 2', 54, 0x55be06),

    FFTALocationData('White Flowers Reward 1', 55, 0x55be4a),
    FFTALocationData('White Flowers Reward 2', 55, 0x55be4c),

    FFTALocationData('New Antilaw Reward 1', 56, 0x55be90),
    FFTALocationData('New Antilaw Reward 2', 56, 0x55be92),

    FFTALocationData('Prison Break Reward 1', 57, 0x55bed6),
    FFTALocationData('Prison Break Reward 2', 57, 0x55bed8),

    FFTALocationData('Royal Ruins Reward 1', 58, 0x55bf1c),
    FFTALocationData('Royal Ruins Reward 2', 58, 0x55bf1e),

    FFTALocationData('Sketchy Thief Reward 1', 59, 0x55bf62),
    FFTALocationData('Sketchy Thief Reward 2', 59, 0x55bf64),

    FFTALocationData('Showdown! Reward 1', 60, 0x55bfa8),
    FFTALocationData('Showdown! Reward 2', 60, 0x55bfaa),

    FFTALocationData('Hit Again Reward 1', 61, 0x55bfee),
    FFTALocationData('Hit Again Reward 2', 61, 0x55bff0),

    FFTALocationData('Oasis Frogs Reward 1', 62, 0x55c034),
    FFTALocationData('Oasis Frogs Reward 2', 62, 0x55c036),

    FFTALocationData('Missing Prof Reward 1', 63, 0x55c07a),
    FFTALocationData('Missing Prof Reward 2', 63, 0x55c07c),

    FFTALocationData('Den of Evil Reward 1', 64, 0x55c0c0),
    FFTALocationData('Den of Evil Reward 2', 64, 0x55c0c2),

    FFTALocationData('Exploration Reward 1', 65, 0x55c106),
    FFTALocationData('Exploration Reward 2', 65, 0x55c108),

    FFTALocationData("A Dragon's Aid Reward 1", 66, 0x55c14c),
    FFTALocationData("A Dragon's Aid Reward 2", 66, 0x55c14e),

    FFTALocationData("Missing Meow Reward 1", 68, 0x55c1d8),
    FFTALocationData("Missing Meow Reward 2", 68, 0x55c1da),

    FFTALocationData("Fowl Thief Reward 1", 69, 0x55c21e),
    FFTALocationData("Fowl Thief Reward 2", 69, 0x55c220),

    FFTALocationData("Free Sprohm! Reward 1", 70, 0x55c264),
    FFTALocationData("Free Sprohm! Reward 2", 70, 0x55c266),

    FFTALocationData("Raven's Oath Reward 1", 71, 0x55c2aa),
    FFTALocationData("Raven's Oath Reward 2", 71, 0x55c2ac),

    FFTALocationData("Nubswood Base Reward 1", 72, 0x55c2f0),
    FFTALocationData("Nubswood Base Reward 2", 72, 0x55c2f2),

    FFTALocationData("Lutia Mop-Up Reward 1", 73, 0x55c336),
    FFTALocationData("Lutia Mop-Up Reward 2", 73, 0x55c338),

    FFTALocationData("Borzoi Falling Reward 1", 74, 0x55c37c),
    FFTALocationData("Borzoi Falling Reward 2", 74, 0x55c37e),

    FFTALocationData("Cadoan Watch Reward 1", 75, 0x55c3c2),
    FFTALocationData("Cadoan Watch Reward 2", 75, 0x55c3c4),

    FFTALocationData("Free Cadoan! Reward 1", 76, 0x55c408),
    FFTALocationData("Free Cadoan! Reward 2", 76, 0x55c40a),

    FFTALocationData("Fire Sigil Reward 1", 77, 0x55c44e),
    FFTALocationData("Fire Sigil Reward 2", 77, 0x55c450),

    FFTALocationData("Free Baguba! Reward 1", 78, 0x55c494),
    FFTALocationData("Free Baguba! Reward 2", 78, 0x55c496),

    FFTALocationData("Water Sigil Reward 1", 79, 0x55c4da),
    FFTALocationData("Water Sigil Reward 2", 79, 0x55c4dc),

    FFTALocationData("Wind Sigil Reward 1", 80, 0x55c520),
    FFTALocationData("Wind Sigil Reward 2", 80, 0x55c522),

    FFTALocationData("Earth Sigil Reward 1", 81, 0x55c566),
    FFTALocationData("Earth Sigil Reward 2", 81, 0x55c568),

    FFTALocationData("The Redwings Reward 1", 82, 0x55c5ac),
    FFTALocationData("The Redwings Reward 2", 82, 0x55c5ae),

    FFTALocationData("Free Muscadet! Reward 1", 83, 0x55c5f2),
    FFTALocationData("Free Muscadet! Reward 2", 83, 0x55c5f4),

    FFTALocationData("Foreign Fiend Reward 1", 84, 0x55c638),
    FFTALocationData("Foreign Fiend Reward 2", 84, 0x55c63a),

    FFTALocationData("Foreign Fiend 2 Reward 1", 85, 0x55c67e),
    FFTALocationData("Foreign Fiend 2 Reward 2", 85, 0x55c680),

    FFTALocationData("Foreign Fiend 3 Reward 1", 86, 0x55c6c4),
    FFTALocationData("Foreign Fiend 3 Reward 2", 86, 0x55c6c6),

    FFTALocationData("Last Stand Reward 1", 87, 0x55c70a),
    FFTALocationData("Last Stand Reward 2", 87, 0x55c70c),

    FFTALocationData("Free Bervenia! Reward 1", 88, 0x55c750),
    FFTALocationData("Free Bervenia! Reward 2", 88, 0x55c752),

    FFTALocationData("The Worldwyrm Reward 1", 89, 0x55c796),
    FFTALocationData("The Worldwyrm Reward 2", 89, 0x55c798),

    FFTALocationData("Moogle Bride Reward 1", 90, 0x55c7dc),
    FFTALocationData("Moogle Bride Reward 2", 90, 0x55c7de),

    FFTALocationData("Clan Law Reward 1", 91, 0x55c822),
    FFTALocationData("Clan Law Reward 2", 91, 0x55c824),

    FFTALocationData("Challengers? Reward 1", 92, 0x55c868),
    FFTALocationData("Challengers? Reward 2", 92, 0x55c86a),

    FFTALocationData("Cursed Bride Reward 1", 93, 0x55c8ae),
    FFTALocationData("Cursed Bride Reward 2", 93, 0x55c8b0),

    FFTALocationData("Flan Breakout Reward 1", 94, 0x55c8f4),
    FFTALocationData("Flan Breakout Reward 2", 94, 0x55c8f6),

    FFTALocationData("Sorry, Friend Reward 1", 95, 0x55c93a),
    FFTALocationData("Sorry, Friend Reward 2", 95, 0x55c93c),

    FFTALocationData("Carrot! Reward 1", 96, 0x55c980),
    FFTALocationData("Carrot! Reward 2", 96, 0x55c982),

    FFTALocationData("Shadow Clan Reward 1", 97, 0x55c9c6),
    FFTALocationData("Shadow Clan Reward 2", 97, 0x55c9c8),

    FFTALocationData("The Dark Blade Reward 1", 98, 0x55ca0c),
    FFTALocationData("The Dark Blade Reward 2", 98, 0x55ca0e),

    FFTALocationData("The Hero Blade Reward 1", 99, 0x55ca52),
    FFTALocationData("The Hero Blade Reward 2", 99, 0x55ca54),

    FFTALocationData("The Fey Blade Reward 1", 100, 0x55ca98),
    FFTALocationData("The Fey Blade Reward 2", 100, 0x55ca9a),

    FFTALocationData("Fiend Run Reward 1", 101, 0x55cade),
    FFTALocationData("Fiend Run Reward 2", 101, 0x55cae0),

    FFTALocationData("Clan Roundup Reward 1", 102, 0x55cb24),
    FFTALocationData("Clan Roundup Reward 2", 102, 0x55cb26),

    FFTALocationData("Wyrms Awaken Reward 1", 103, 0x55cb6a),
    FFTALocationData("Wyrms Awaken Reward 2", 103, 0x55cb6c),

    # League missions currently not working
    #FFTALocationData("Yellow Powerz Reward 1", 104, 0x55cbb0),
    #FFTALocationData("Yellow Powerz Reward 2", 104, 0x55cbb2),

    #FFTALocationData("Blue Geniuses Reward 1", 105, 0x55cbf6),
    #FFTALocationData("Blue Geniuses Reward 2", 105, 0x55cbf8),

    #FFTALocationData("Brown Rabbits Reward 1", 106, 0x55cc3c),
    #FFTALocationData("Brown Rabbits Reward 2", 106, 0x55cc3e),

    #FFTALocationData("White Kupos Reward 1", 107, 0x55cc82),
    #FFTALocationData("White Kupos Reward 2", 107, 0x55cc84),

    FFTALocationData("Mythril Rush Reward 1", 108, 0x55ccc8),
    FFTALocationData("Mythril Rush Reward 2", 108, 0x55ccca),

    FFTALocationData("Stolen Scoop Reward 1", 109, 0x55cd0e),
    FFTALocationData("Stolen Scoop Reward 2", 109, 0x55cd10),

    FFTALocationData("Smuggle Bust Reward 1", 110, 0x55cd54),
    FFTALocationData("Smuggle Bust Reward 2", 110, 0x55cd56),

    FFTALocationData("Resistance Reward 1", 111, 0x55cd9a),
    FFTALocationData("Resistance Reward 2", 111, 0x55cd9c),

    FFTALocationData("Old Friends Reward 1", 113, 0x55ce26),
    FFTALocationData("Old Friends Reward 2", 113, 0x55ce28),

    FFTALocationData("Poachers Reward 1", 114, 0x55ce6c),
    FFTALocationData("Poachers Reward 2", 114, 0x55ce6e),

    FFTALocationData("Snow Fairy Reward 1", 115, 0x55ceb2),
    FFTALocationData("Snow Fairy Reward 2", 115, 0x55ceb4),

    FFTALocationData("Revenge Reward 1", 116, 0x55cef8),
    FFTALocationData("Revenge Reward 2", 116, 0x55cefa),

    FFTALocationData("Retrieve Mail Reward 1", 117, 0x55cf3e),
    FFTALocationData("Retrieve Mail Reward 2", 117, 0x55cf40),

    FFTALocationData("A Challenge Reward 1", 118, 0x55cf84),
    FFTALocationData("A Challenge Reward 2", 118, 0x55cf86),

    # First dispatch mission
    FFTALocationData("Watching You Reward 1", 125, 0x55d16e),
    FFTALocationData("Watching You Reward 2", 125, 0x55d170),

    FFTALocationData("Golden Gil Reward 1", 126, 0x55d1b4),
    FFTALocationData("Golden Gil Reward 2", 126, 0x55d1b6),

    FFTALocationData("Dueling Sub Reward 1", 127, 0x55d1fa),
    FFTALocationData("Dueling Sub Reward 2", 127, 0x55d1fc),

    FFTALocationData("Gulag Ghost Reward 1", 128, 0x55d240),
    FFTALocationData("Gulag Ghost Reward 2", 128, 0x55d242),

    FFTALocationData("Water City Reward 1", 129, 0x55d286),
    FFTALocationData("Water City Reward 2", 129, 0x55d288),

    FFTALocationData("Mirage Tower Reward 1", 130, 0x55d2cc),
    FFTALocationData("Mirage Tower Reward 2", 130, 0x55d2ce),

    FFTALocationData("A Barren Land Reward 1", 131, 0x55d312),
    FFTALocationData("A Barren Land Reward 2", 131, 0x55d314),

    FFTALocationData("Cadoan Meet Reward 1", 132, 0x55d358),
    FFTALocationData("Cadoan Meet Reward 2", 132, 0x55d35a),

    FFTALocationData("Sprohm Meet Reward 1", 133, 0x55d39e),
    FFTALocationData("Sprohm Meet Reward 2", 133, 0x55d3a0),

    FFTALocationData("Run for Fun Reward 1", 134, 0x55d3e4),
    FFTALocationData("Run for Fun Reward 2", 134, 0x55d3e6),

    FFTALocationData("Hungry Ghost Reward 1", 135, 0x55d42a),
    FFTALocationData("Hungry Ghost Reward 2", 135, 0x55d42c),

    FFTALocationData("Pirates Ahoy Reward 1", 136, 0x55d470),
    FFTALocationData("Pirates Ahoy Reward 2", 136, 0x55d472),

    FFTALocationData("Castle Sit-In Reward 1", 137, 0x55d4b6),
    FFTALocationData("Castle Sit-In Reward 2", 137, 0x55d4b8),

    FFTALocationData("Wine Delivery Reward 1", 138, 0x55d4fc),
    FFTALocationData("Wine Delivery Reward 2", 138, 0x55d4fe),

    FFTALocationData("Broken Tunes Reward 1", 139, 0x55d542),
    FFTALocationData("Broken Tunes Reward 2", 139, 0x55d544),

    FFTALocationData("Falcon Flown Reward 1", 140, 0x55d588),
    FFTALocationData("Falcon Flown Reward 2", 140, 0x55d58a),

    FFTALocationData("Danger Pass Reward 1", 141, 0x55d5ce),
    FFTALocationData("Danger Pass Reward 2", 141, 0x55d5d0),

    FFTALocationData("Mist Stars Reward 1", 142, 0x55d614),
    FFTALocationData("Mist Stars Reward 2", 142, 0x55d616),

    FFTALocationData("Adaman Alloy Reward 1", 143, 0x55d65a),
    FFTALocationData("Adaman Alloy Reward 2", 143, 0x55d65c),

    FFTALocationData("Mysidia Alloy Reward 1", 144, 0x55d6a0),
    FFTALocationData("Mysidia Alloy Reward 2", 144, 0x55d6a2),

    FFTALocationData("Crusite Alloy Reward 1", 145, 0x55d6e6),
    FFTALocationData("Crusite Alloy Reward 2", 145, 0x55d6e8),

    FFTALocationData("Faceless Dolls Reward 1", 146, 0x55d72c),
    FFTALocationData("Faceless Dolls Reward 2", 146, 0x55d72e),

    FFTALocationData("Faithful Fairy Reward 1", 147, 0x55d772),
    FFTALocationData("Faithful Fairy Reward 2", 147, 0x55d774),

    FFTALocationData("For the Lady Reward 1", 148, 0x55d7b8),
    FFTALocationData("For the Lady Reward 2", 148, 0x55d7ba),

    FFTALocationData("Seven Nights Reward 1", 149, 0x55d7fe),
    FFTALocationData("Seven Nights Reward 2", 149, 0x55d800),

    FFTALocationData("Shady Deals Reward 1", 150, 0x55d844),
    FFTALocationData("Shady Deals Reward 2", 150, 0x55d846),

    FFTALocationData("Earthy Colors Reward 1", 151, 0x55d88a),
    FFTALocationData("Earthy Colors Reward 2", 151, 0x55d88c),

    FFTALocationData("Lost Heirloom Reward 1", 152, 0x55d8d0),
    FFTALocationData("Lost Heirloom Reward 2", 152, 0x55d8d2),

    FFTALocationData("Young Love Reward 1", 153, 0x55d916),
    FFTALocationData("Young Love Reward 2", 153, 0x55d918),

    FFTALocationData("Ghosts of War Reward 1", 154, 0x55d95c),
    FFTALocationData("Ghosts of War Reward 2", 154, 0x55d95e),

    FFTALocationData("The Last Day Reward 1", 155, 0x55d9a2),
    FFTALocationData("The Last Day Reward 2", 155, 0x55d9a4),

    FFTALocationData("The Bell Tolls Reward 1", 156, 0x55d9e8),
    FFTALocationData("The Bell Tolls Reward 2", 156, 0x55d9ea),

    FFTALocationData("Goblin Town Reward 1", 157, 0x55da2e),
    FFTALocationData("Goblin Town Reward 2", 157, 0x55da30),

    FFTALocationData("Secret Books Reward 1", 158, 0x55da74),
    FFTALocationData("Secret Books Reward 2", 158, 0x55da76),

    FFTALocationData("Words of Love Reward 1", 159, 0x55daba),
    FFTALocationData("Words of Love Reward 2", 159, 0x55dabc),

    FFTALocationData("You, Immortal Reward 1", 160, 0x55db00),
    FFTALocationData("You, Immortal Reward 2", 160, 0x55db02),

    FFTALocationData("Clocktower Reward 1", 161, 0x55db46),
    FFTALocationData("Clocktower Reward 2", 161, 0x55db48),

    FFTALocationData("An Education Reward 1", 162, 0x55db8c),
    FFTALocationData("An Education Reward 2", 162, 0x55db8e),

    FFTALocationData("Morning Woes Reward 1", 163, 0x55dbd2),
    FFTALocationData("Morning Woes Reward 2", 163, 0x55dbd4),

    FFTALocationData("Down to Earth Reward 1", 164, 0x55dc18),
    FFTALocationData("Down to Earth Reward 2", 164, 0x55dc1a),

    FFTALocationData("To Meden Reward 1", 165, 0x55dc5e),
    FFTALocationData("To Meden Reward 2", 165, 0x55dc60),

    FFTALocationData("Neighbor! Reward 1", 166, 0x55dca4),
    FFTALocationData("Neighbor! Reward 2", 166, 0x55dca6),

    FFTALocationData("Honor Lost Reward 1", 167, 0x55dcea),
    FFTALocationData("Honor Lost Reward 2", 167, 0x55dcec),

    FFTALocationData("Inspiration Reward 1", 168, 0x55dd30),
    FFTALocationData("Inspiration Reward 2", 168, 0x55dd32),

    FFTALocationData("Coo's Break Reward 1", 169, 0x55dd76),
    FFTALocationData("Coo's Break Reward 2", 169, 0x55dd78),

    FFTALocationData("The Match Reward 1", 170, 0x55ddbc),
    FFTALocationData("The Match Reward 2", 170, 0x55ddbe),

    FFTALocationData("The Deep Sea Reward 1", 171, 0x55de02),
    FFTALocationData("The Deep Sea Reward 2", 171, 0x55de04),

    FFTALocationData("A Worthy Eye Reward 1", 172, 0x55de48),
    FFTALocationData("A Worthy Eye Reward 2", 172, 0x55de4a),

    FFTALocationData("Lost in Mist Reward 1", 173, 0x55de8e),
    FFTALocationData("Lost in Mist Reward 2", 173, 0x55de90),

    FFTALocationData("Darn Kids Reward 1", 174, 0x55ded4),
    FFTALocationData("Darn Kids Reward 2", 174, 0x55ded6),

    FFTALocationData("Stage Fright Reward 1", 175, 0x55df1a),
    FFTALocationData("Stage Fright Reward 2", 175, 0x55df1c),

    FFTALocationData("Diary Dilemma Reward 1", 176, 0x55df60),
    FFTALocationData("Diary Dilemma Reward 2", 176, 0x55df62),

    FFTALocationData("Hundred-Eye Reward 1", 177, 0x55dfa6),
    FFTALocationData("Hundred-Eye Reward 2", 177, 0x55dfa8),

    FFTALocationData("Runaway Boy Reward 1", 178, 0x55dfec),
    FFTALocationData("Runaway Boy Reward 2", 178, 0x55dfee),

    FFTALocationData("Mad Alchemist Reward 1", 179, 0x55e032),
    FFTALocationData("Mad Alchemist Reward 2", 179, 0x55e034),

    FFTALocationData("Caravan Guard Reward 1", 180, 0x55e078),
    FFTALocationData("Caravan Guard Reward 2", 180, 0x55e07a),

    FFTALocationData("Lifework Reward 1", 181, 0x55e0be),
    FFTALocationData("Lifework Reward 2", 181, 0x55e0c0),

    FFTALocationData("Cheap Laughs Reward 1", 182, 0x55e104),
    FFTALocationData("Cheap Laughs Reward 2", 182, 0x55e106),

    FFTALocationData("T.L.C. Reward 1", 183, 0x55e14a),
    FFTALocationData("T.L.C. Reward 2", 183, 0x55e14c),

    FFTALocationData("Frozen Spring Reward 1", 184, 0x55e190),
    FFTALocationData("Frozen Spring Reward 2", 184, 0x55e192),

    FFTALocationData("No Scents Reward 1", 185, 0x55e1d6),
    FFTALocationData("No Scents Reward 2", 185, 0x55e1d8),

    FFTALocationData("On The Waves Reward 1", 186, 0x55e21c),
    FFTALocationData("On The Waves Reward 2", 186, 0x55e21e),

    FFTALocationData("Spirited Boy Reward 1", 187, 0x55e262),
    FFTALocationData("Spirited Boy Reward 2", 187, 0x55e264),

    FFTALocationData("Powder Worries Reward 1", 188, 0x55e2a8),
    FFTALocationData("Powder Worries Reward 2", 188, 0x55e2aa),

    FFTALocationData("The Blue Bolt Reward 1", 189, 0x55e2ee),
    FFTALocationData("The Blue Bolt Reward 2", 189, 0x55e2f0),

    FFTALocationData("Sweet Talk Reward 1", 190, 0x55e334),
    FFTALocationData("Sweet Talk Reward 2", 190, 0x55e336),

    FFTALocationData("Scarface Reward 1", 191, 0x55e37a),
    FFTALocationData("Scarface Reward 2", 191, 0x55e37c),

    FFTALocationData("Mirage Town Reward 1", 192, 0x55e3c0),
    FFTALocationData("Mirage Town Reward 2", 192, 0x55e3c2),

    FFTALocationData("Soldier's Wish Reward 1", 193, 0x55e406),
    FFTALocationData("Soldier's Wish Reward 2", 193, 0x55e408),

    FFTALocationData("Dry Spell Reward 1", 194, 0x55e44c),
    FFTALocationData("Dry Spell Reward 2", 194, 0x55e44e),

    FFTALocationData("Swap Meet Reward 1", 195, 0x55e492),
    FFTALocationData("Swap Meet Reward 2", 195, 0x55e494),

    FFTALocationData("Adaman Order Reward 1", 196, 0x55e4d8),
    FFTALocationData("Adaman Order Reward 2", 196, 0x55e4da),

    FFTALocationData("Magic Mysidia Reward 1", 197, 0x55e51e),
    FFTALocationData("Magic Mysidia Reward 2", 197, 0x55e520),

    FFTALocationData("Conundrum Reward 1", 198, 0x55e564),
    FFTALocationData("Conundrum Reward 2", 198, 0x55e566),

    FFTALocationData("Lucky Night Reward 1", 199, 0x55e5aa),
    FFTALocationData("Lucky Night Reward 2", 199, 0x55e5ac),

    FFTALocationData("Tutor Search Reward 1", 200, 0x55e5f0),
    FFTALocationData("Tutor Search Reward 2", 200, 0x55e5f2),

    FFTALocationData("Why Am I Wet? Reward 1", 201, 0x55e636),
    FFTALocationData("Why Am I Wet? Reward 2", 201, 0x55e638),

    FFTALocationData("Run With Us Reward 1", 202, 0x55e67c),
    FFTALocationData("Run With Us Reward 2", 202, 0x55e67e),

    FFTALocationData("Lucky Charm Reward 1", 203, 0x55e6c2),
    FFTALocationData("Lucky Charm Reward 2", 203, 0x55e6c4),

    FFTALocationData("Alchemist Boy Reward 1", 204, 0x55e708),
    FFTALocationData("Alchemist Boy Reward 2", 204, 0x55e70a),

    FFTALocationData("Thorny Dreams Reward 1", 205, 0x55e74e),
    FFTALocationData("Thorny Dreams Reward 2", 205, 0x55e750),

    FFTALocationData("Free Cyril! Reward 1", 206, 0x55e794),
    FFTALocationData("Free Cyril! Reward 2", 206, 0x55e796),

    FFTALocationData("Ship Needed Reward 1", 207, 0x55e7da),
    FFTALocationData("Ship Needed Reward 2", 207, 0x55e7dc),

    FFTALocationData("Mind Ceffyl Reward 1", 208, 0x55e820),
    FFTALocationData("Mind Ceffyl Reward 2", 208, 0x55e822),

    FFTALocationData("Body Ceffyl Reward 1", 209, 0x55e866),
    FFTALocationData("Body Ceffyl Reward 2", 209, 0x55e868),

    FFTALocationData("The Spiritstone Reward 1", 210, 0x55e8ac),
    FFTALocationData("The Spiritstone Reward 2", 210, 0x55e8ae),

    FFTALocationData("Girl In Love Reward 1", 211, 0x55e8f2),
    FFTALocationData("Girl In Love Reward 2", 211, 0x55e8f4),

    FFTALocationData("Chocobo Help! Reward 1", 212, 0x55e938),
    FFTALocationData("Chocobo Help! Reward 2", 212, 0x55e93a),

    FFTALocationData("The Skypole Reward 1", 213, 0x55e97e),
    FFTALocationData("The Skypole Reward 2", 213, 0x55e980),

    FFTALocationData("Ruins Survey Reward 1", 214, 0x55e9c4),
    FFTALocationData("Ruins Survey Reward 2", 214, 0x55e9c6),

    FFTALocationData("Dig Dig Dig Reward 1", 215, 0x55ea0a),
    FFTALocationData("Dig Dig Dig Reward 2", 215, 0x55ea0c),

    FFTALocationData("Seeking Silver Reward 1", 216, 0x55ea50),
    FFTALocationData("Seeking Silver Reward 2", 216, 0x55ea52),

    FFTALocationData("Materite Reward 1", 217, 0x55ea96),
    FFTALocationData("Materite Reward 2", 217, 0x55ea98),

    FFTALocationData("The Wormhole Reward 1", 218, 0x55eadc),
    FFTALocationData("The Wormhole Reward 2", 218, 0x55eade),

    FFTALocationData("Metal Hunt Reward 1", 219, 0x55eb22),
    FFTALocationData("Metal Hunt Reward 2", 219, 0x55eb24),

    FFTALocationData("Math Is Hard Reward 1", 220, 0x55eb68),
    FFTALocationData("Math Is Hard Reward 2", 220, 0x55eb6a),

    FFTALocationData("The Witness Reward 1", 221, 0x55ebae),
    FFTALocationData("The Witness Reward 2", 221, 0x55ebb0),

    FFTALocationData("Life Or Death Reward 1", 222, 0x55ebf4),
    FFTALocationData("Life Or Death Reward 2", 222, 0x55ebf6),

    FFTALocationData("Karlos's Day Reward 1", 223, 0x55ec3a),
    FFTALocationData("Karlos's Day Reward 2", 223, 0x55ec3c),

    FFTALocationData("To Father Reward 1", 224, 0x55ec80),
    FFTALocationData("To Father Reward 2", 224, 0x55ec82),

    FFTALocationData("Oh Milese Reward 1", 225, 0x55ecc6),
    FFTALocationData("Oh Milese Reward 2", 225, 0x55ecc8),

    FFTALocationData("Skinning Time Reward 1", 226, 0x55ed0c),
    FFTALocationData("Skinning Time Reward 2", 226, 0x55ed0e),

    FFTALocationData("Wild River Reward 1", 227, 0x55ed52),
    FFTALocationData("Wild River Reward 2", 227, 0x55ed54),

    FFTALocationData("Magic Cloth Reward 1", 228, 0x55ed98),
    FFTALocationData("Magic Cloth Reward 2", 228, 0x55ed9a),

    FFTALocationData("Cotton Guard Reward 1", 229, 0x55edde),
    FFTALocationData("Cotton Guard Reward 2", 229, 0x55ede0),

    FFTALocationData("Help Dad Reward 1", 230, 0x55ee24),
    FFTALocationData("Help Dad Reward 2", 230, 0x55ee26),

    FFTALocationData("Rubber or Real Reward 1", 231, 0x55ee6a),
    FFTALocationData("Rubber or Real Reward 2", 231, 0x55ee6c),

    FFTALocationData("Into The Woods Reward 1", 232, 0x55eeb0),
    FFTALocationData("Into The Woods Reward 2", 232, 0x55eeb2),

    FFTALocationData("Jerky Days Reward 1", 233, 0x55eef6),
    FFTALocationData("Jerky Days Reward 2", 233, 0x55eef8),

    FFTALocationData("New Fields Reward 1", 234, 0x55ef3c),
    FFTALocationData("New Fields Reward 2", 234, 0x55ef3e),

    FFTALocationData("Strange Fires Reward 1", 235, 0x55ef82),
    FFTALocationData("Strange Fires Reward 2", 235, 0x55ef84),

    FFTALocationData("Better Living Reward 1", 236, 0x55efc8),
    FFTALocationData("Better Living Reward 2", 236, 0x55efca),

    FFTALocationData("Malboro Hunt Reward 1", 237, 0x55f00e),
    FFTALocationData("Malboro Hunt Reward 2", 237, 0x55f010),

    FFTALocationData("Chocobo Work Reward 1", 238, 0x55f054),
    FFTALocationData("Chocobo Work Reward 2", 238, 0x55f056),

    FFTALocationData("Party Night Reward 1", 239, 0x55f09a),
    FFTALocationData("Party Night Reward 2", 239, 0x55f09c),

    FFTALocationData("Mama's Taste Reward 1", 240, 0x55f0e0),
    FFTALocationData("Mama's Taste Reward 2", 240, 0x55f0e2),

    FFTALocationData("The Well Maze Reward 1", 241, 0x55f126),
    FFTALocationData("The Well Maze Reward 2", 241, 0x55f128),

    FFTALocationData("She's Gone Reward 1", 242, 0x55f16c),
    FFTALocationData("She's Gone Reward 2", 242, 0x55f16e),

    FFTALocationData("Magic Vellum Reward 1", 243, 0x55f1b2),
    FFTALocationData("Magic Vellum Reward 2", 243, 0x55f1b4),

    FFTALocationData("Novel Ascent Reward 1", 244, 0x55f1f8),
    FFTALocationData("Novel Ascent Reward 2", 244, 0x55f1fa),

    FFTALocationData("Shiver Reward 1", 245, 0x55f23e),
    FFTALocationData("Shiver Reward 2", 245, 0x55f240),

    FFTALocationData("Bread Woes Reward 1", 246, 0x55f284),
    FFTALocationData("Bread Woes Reward 2", 246, 0x55f286),

    FFTALocationData("Book Mess Reward 1", 247, 0x55f2ca),
    FFTALocationData("Book Mess Reward 2", 247, 0x55f2cc),

    FFTALocationData("One More Tail Reward 1", 248, 0x55f310),
    FFTALocationData("One More Tail Reward 2", 248, 0x55f312),

    FFTALocationData("Relax Time! Reward 1", 249, 0x55f356),
    FFTALocationData("Relax Time! Reward 2", 249, 0x55f358),

    FFTALocationData("Foma Jungle Reward 1", 250, 0x55f39c),
    FFTALocationData("Foma Jungle Reward 2", 250, 0x55f39e),

    FFTALocationData("For A Flower Reward 1", 251, 0x55f3e2),
    FFTALocationData("For A Flower Reward 2", 251, 0x55f3e4),

    FFTALocationData("Giza Plains Reward 1", 252, 0x55f428),
    FFTALocationData("Giza Plains Reward 2", 252, 0x55f42a),

    FFTALocationData("Lutia Pass Reward 1", 253, 0x55f46e),
    FFTALocationData("Lutia Pass Reward 2", 253, 0x55f470),

    FFTALocationData("Eluut Sands Reward 1", 254, 0x55f4b4),
    FFTALocationData("Eluut Sands Reward 2", 254, 0x55f4b6),

    FFTALocationData("Ulei River Reward 1", 255, 0x55f4fa),
    FFTALocationData("Ulei River Reward 2", 255, 0x55f4fc),

    FFTALocationData("Aisenfield Reward 1", 256, 0x55f540),
    FFTALocationData("Aisenfield Reward 2", 256, 0x55f542),

    FFTALocationData("The Nubswood Reward 1", 257, 0x55f586),
    FFTALocationData("The Nubswood Reward 2", 257, 0x55f588),
    
    FFTALocationData("Roda Volcano Reward 1", 258, 0x55f5cc),
    FFTALocationData("Roda Volcano Reward 2", 258, 0x55f5ce),

    FFTALocationData("Travel Aid Reward 1", 259, 0x55f612),
    FFTALocationData("Travel Aid Reward 2", 259, 0x55f614),

    FFTALocationData("The Salikwood Reward 1", 260, 0x55f658),
    FFTALocationData("The Salikwood Reward 2", 260, 0x55f65a),

    FFTALocationData("Nargai Cave Reward 1", 261, 0x55f69e),
    FFTALocationData("Nargai Cave Reward 2", 261, 0x55f6a0),

    FFTALocationData("Kudik Peaks Reward 1", 262, 0x55f6e4),
    FFTALocationData("Kudik Peaks Reward 2", 262, 0x55f6e6),

    FFTALocationData("Jeraw Sands Reward 1", 263, 0x55f72a),
    FFTALocationData("Jeraw Sands Reward 2", 263, 0x55f72c),

    FFTALocationData("Uladon Bog Reward 1", 264, 0x55f770),
    FFTALocationData("Uladon Bog Reward 2", 264, 0x55f772),

    FFTALocationData("Gotor Sands Reward 1", 265, 0x55f7b6),
    FFTALocationData("Gotor Sands Reward 2", 265, 0x55f7b8),

    FFTALocationData("Delia Dunes Reward 1", 266, 0x55f7fc),
    FFTALocationData("Delia Dunes Reward 2", 266, 0x55f7fe),

    FFTALocationData("Bugbusters Reward 1", 267, 0x55f842),
    FFTALocationData("Bugbusters Reward 2", 267, 0x55f844),

    FFTALocationData("Tubola Cave Reward 1", 268, 0x55f888),
    FFTALocationData("Tubola Cave Reward 2", 268, 0x55f88a),

    FFTALocationData("Deti Plains Reward 1", 269, 0x55f8ce),
    FFTALocationData("Deti Plains Reward 2", 269, 0x55f8d0),

    FFTALocationData("Siena Gorge Reward 1", 270, 0x55f914),
    FFTALocationData("Siena Gorge Reward 2", 270, 0x55f916),

    FFTALocationData("Jagd Ahli Reward 1", 271, 0x55f95a),
    FFTALocationData("Jagd Ahli Reward 2", 271, 0x55f95c),

    FFTALocationData("Jagd Helje Reward 1", 272, 0x55f9a0),
    FFTALocationData("Jagd Helje Reward 2", 272, 0x55f9a2),

    FFTALocationData("Jagd Dorsa Reward 1", 273, 0x55f9e6),
    FFTALocationData("Jagd Dorsa Reward 2", 273, 0x55f9e8),

    FFTALocationData("Ambervale Reward 1", 274, 0x55fa2c),
    FFTALocationData("Ambervale Reward 2", 274, 0x55fa2e),

    FFTALocationData("Ozmonfield Reward 1", 275, 0x55fa72),
    FFTALocationData("Ozmonfield Reward 2", 275, 0x55fa74),

    FFTALocationData("Swords in Cyril Reward 1", 276, 0x55fab8),
    FFTALocationData("Swords in Cyril Reward 2", 276, 0x55faba),

    FFTALocationData("Newbie Hall Reward 1", 277, 0x55fafe),
    FFTALocationData("Newbie Hall Reward 2", 277, 0x55fb00),

    FFTALocationData("Voodoo Doll Reward 1", 278, 0x55fb44),
    FFTALocationData("Voodoo Doll Reward 2", 278, 0x55fb46),

    FFTALocationData("Come On Out Reward 1", 279, 0x55fb8a),
    FFTALocationData("Come On Out Reward 2", 279, 0x55fb8c),

    FFTALocationData("Food for Truth Reward 1", 280, 0x55fbd0),
    FFTALocationData("Food for Truth Reward 2", 280, 0x55fbd2),

    FFTALocationData("Alba Cave Reward 1", 281, 0x55fc16),
    FFTALocationData("Alba Cave Reward 2", 281, 0x55fc18),

    FFTALocationData("The Performer Reward 1", 282, 0x55fc5c),
    FFTALocationData("The Performer Reward 2", 282, 0x55fc5e),

    FFTALocationData("One More Time Reward 1", 283, 0x55fca2),
    FFTALocationData("One More Time Reward 2", 283, 0x55fca4),

    FFTALocationData("Spring Tree Reward 1", 284, 0x55fce8),
    FFTALocationData("Spring Tree Reward 2", 284, 0x55fcea),

    FFTALocationData("Who Am I Reward 1", 285, 0x55fd2e),
    FFTALocationData("Who Am I Reward 2", 285, 0x55fd30),

    FFTALocationData("Reaper Rumors Reward 1", 286, 0x55fd74),
    FFTALocationData("Reaper Rumors Reward 2", 286, 0x55fd76),

    FFTALocationData("Dog Days Reward 1", 287, 0x55fdba),
    FFTALocationData("Dog Days Reward 2", 287, 0x55fdbc),

    FFTALocationData("Good Bread Reward 1", 288, 0x55fe00),
    FFTALocationData("Good Bread Reward 2", 288, 0x55fe02),

    FFTALocationData("Sword Needed Reward 1", 289, 0x55fe46),
    FFTALocationData("Sword Needed Reward 2", 289, 0x55fe48),

    FFTALocationData("El Ritmo Reward 1", 290, 0x55fe8c),
    FFTALocationData("El Ritmo Reward 2", 290, 0x55fe8e),

    FFTALocationData("Her Big Move Reward 1", 291, 0x55fed2),
    FFTALocationData("Her Big Move Reward 2", 291, 0x55fed4),

    FFTALocationData("Don't Look! Reward 1", 292, 0x55ff18),
    FFTALocationData("Don't Look! Reward 2", 292, 0x55ff1a),

    FFTALocationData("Janitor Duty Reward 1", 293, 0x55ff5e),
    FFTALocationData("Janitor Duty Reward 2", 293, 0x55ff60),

    FFTALocationData("Unlucky Star Reward 1", 294, 0x55ffa4),
    FFTALocationData("Unlucky Star Reward 2", 294, 0x55ffa6),

    FFTALocationData("Corral Care Reward 1", 295, 0x55ffea),
    FFTALocationData("Corral Care Reward 2", 295, 0x55ffec),

    FFTALocationData("Beastly Gun Reward 1", 296, 0x560030),
    FFTALocationData("Beastly Gun Reward 2", 296, 0x560032),

    FFTALocationData("Blade & Turtle Reward 1", 297, 0x560076),
    FFTALocationData("Blade & Turtle Reward 2", 297, 0x560078),

    FFTALocationData("Valuable Fake Reward 1", 298, 0x5600bc),
    FFTALocationData("Valuable Fake Reward 2", 298, 0x5600be),

    FFTALocationData("Weaver's War Reward 1", 299, 0x560102),
    FFTALocationData("Weaver's War Reward 2", 299, 0x560104),

    FFTALocationData("Fabled Sword Reward 1", 300, 0x560148),
    FFTALocationData("Fabled Sword Reward 2", 300, 0x56014a),

    FFTALocationData("Refurbishing Reward 1", 301, 0x56018e),
    FFTALocationData("Refurbishing Reward 2", 301, 0x560190),

    FFTALocationData("Stone Secret Reward 1", 302, 0x5601d4),
    FFTALocationData("Stone Secret Reward 2", 302, 0x5601d6),

    FFTALocationData("Sword Stuff Reward 1", 303, 0x56021a),
    FFTALocationData("Sword Stuff Reward 2", 303, 0x56021c),

    FFTALocationData("A Stormy Night Reward 1", 304, 0x560260),
    FFTALocationData("A Stormy Night Reward 2", 304, 0x560262),

    FFTALocationData("Minstrel Song Reward 1", 305, 0x5602a6),
    FFTALocationData("Minstrel Song Reward 2", 305, 0x5602a8),

    FFTALocationData("Gun Crazy Reward 1", 306, 0x5602ec),
    FFTALocationData("Gun Crazy Reward 2", 306, 0x5602ee),

    FFTALocationData("Black Hat Reward 1", 307, 0x560332),
    FFTALocationData("Black Hat Reward 2", 307, 0x560334),

    FFTALocationData("Hat For A Girl Reward 1", 308, 0x560378),
    FFTALocationData("Hat For A Girl Reward 2", 308, 0x56037a),

    FFTALocationData("Armor & Turtle Reward 1", 309, 0x5603be),
    FFTALocationData("Armor & Turtle Reward 2", 309, 0x5603c0),

    FFTALocationData("Dark Armor Reward 1", 310, 0x560404),
    FFTALocationData("Dark Armor Reward 2", 310, 0x560406),

    FFTALocationData("Fashion World Reward 1", 311, 0x56044a),
    FFTALocationData("Fashion World Reward 2", 311, 0x56044c),

    FFTALocationData("Fashion Hoopla Reward 1", 312, 0x560490),
    FFTALocationData("Fashion Hoopla Reward 2", 312, 0x560492),

    # Extra missions
    FFTALocationData("Reconciliation Reward 1", 374, 0x561584),
    FFTALocationData("Reconciliation Reward 2", 374, 0x561586),

    FFTALocationData("With Babus Reward 1", 376, 0x561610),
    FFTALocationData("With Babus Reward 2", 376, 0x561612),

    # Ritz might be required to be recruited
    FFTALocationData("Mortal Snow Reward 1", 377, 0x561656),
    FFTALocationData("Mortal Snow Reward 2", 377, 0x561658),

    FFTALocationData("Cleanup Time Reward 1", 379, 0x5616e2),
    FFTALocationData("Cleanup Time Reward 2", 379, 0x5616e4),

    FFTALocationData("No Arms Rule Reward 1", 385, 0x561886),
    FFTALocationData("No Arms Rule Reward 2", 385, 0x561888),

    FFTALocationData("Kissing Rule Reward 1", 386, 0x5618cc),
    FFTALocationData("Kissing Rule Reward 2", 386, 0x5618ce),

    FFTALocationData("Immunity Pass Reward 1", 387, 0x561912),
    FFTALocationData("Immunity Pass Reward 2", 387, 0x561914),

    FFTALocationData("No Full HP Reward 1", 388, 0x561958),
    FFTALocationData("No Full HP Reward 2", 388, 0x56195a),

    FFTALocationData("No Literacy Reward 1", 389, 0x56199e),
    FFTALocationData("No Literacy Reward 2", 389, 0x5619a0),

    FFTALocationData("Favoritism Reward 1", 390, 0x5619e4),
    FFTALocationData("Favoritism Reward 2", 390, 0x5619e6),

    FFTALocationData("No Answers Reward 1", 391, 0x561a2a),
    FFTALocationData("No Answers Reward 2", 391, 0x561a2c),

    FFTALocationData("No Jumping Reward 1", 392, 0x561a70),
    FFTALocationData("No Jumping Reward 2", 392, 0x561a72),
]

bitflag_index = 2
byte_i = 0
# Setting up the mission complete flags
for index in range(0, len(FFTALocations), 2):
    #if byte_i == 2 and bitflag_index == 5:
    #    bitflag_index = 6

    if byte_i == 3 and bitflag_index == 1:
        bitflag_index = 3

    elif byte_i == 8 and bitflag_index == 5:
        bitflag_index = 6

    # Skipping the league mission bitflags for now
    elif byte_i == 13 and bitflag_index == 2:
        bitflag_index = 6

    elif byte_i == 14 and bitflag_index == 2:
        bitflag_index = 3

    elif byte_i == 15 and bitflag_index == 1:
        bitflag_index = 7
        
    elif byte_i == 39 and bitflag_index == 3:
        byte_i = 47
        bitflag_index = 0

    elif byte_i == 47 and bitflag_index == 0:
        bitflag_index = 1

    elif byte_i == 47 and bitflag_index == 1:
        bitflag_index = 2

    elif byte_i == 47 and bitflag_index == 4:
        bitflag_index = 5

    elif byte_i == 47 and bitflag_index == 6:
        bitflag_index = 3
        byte_i = 48

    # Immunity pass
    #elif byte_i == 48 and bitflag_index == 4:
    #    bitflag_index = 5
    #    byte_i = 48

    # Add dispatch missions to dispatch mission group
    if 125 <= FFTALocations[index].mission_id <= 312:
        DispatchMissionGroups.append(tuple([FFTALocations[index], FFTALocations[(index + 1)], bitflags[bitflag_index], byte_i]))

    else:
        MissionGroups.append(tuple([FFTALocations[index], FFTALocations[(index + 1)], bitflags[bitflag_index], byte_i]))
        
    bitflag_index = bitflag_index + 1
    if bitflag_index > 7:
        bitflag_index = 0
        byte_i = byte_i + 1

#for index, mission_group in enumerate(MissionGroups):
#    print("Mission group index: " + str(index) + " mission group [0] consists of: " + mission_group[0].name)
#    print("Mission group index: " + str(index) + " mission group [1] consists of: " + mission_group[1].name)

def create_location_label_to_id_map() -> Dict[str, int]:
    """
    Creates a map from location labels to their AP location id (address)
    """
    label_to_id_map: Dict[str, int] = {}
    for location in FFTALocations:
        label_to_id_map[location.name] = location.rom_address

    return label_to_id_map


location_flags: Dict



