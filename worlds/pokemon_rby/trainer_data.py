"""Trainer party data for Pokemon Red/Blue and Pokemon Yellow.

The common data matches Red/Blue and Yellow. The version-specific dictionaries contain
party records that are missing or different in that version.
"""

from copy import deepcopy

trainer_data_common = {
    'Fossil Level': [
        {
            'level': 30,
            'party': [],
            'party_address': 'Fossil_Level',
        },
    ],
    'Route 3': [
        {
            'level': 11,
            'party': ['Rattata', 'Ekans'],
            'party_address': 'Trainer_Party_Route_3_Youngster_A',
        },
        {
            'level': 14,
            'party': ['Spearow'],
            'party_address': 'Trainer_Party_Route_3_Youngster_B',
        },
        {
            'level': 10,
            'party': ['Caterpie', 'Weedle', 'Caterpie'],
            'party_address': 'Trainer_Party_Route_3_BugCatcher_A',
        },
        {
            'level': 9,
            'party': ['Weedle', 'Kakuna', 'Caterpie', 'Metapod'],
            'party_address': 'Trainer_Party_Route_3_BugCatcher_B',
        },
        {
            'level': 11,
            'party': ['Caterpie', 'Metapod'],
            'party_address': 'Trainer_Party_Route_3_BugCatcher_C',
        },
        {
            'level': 9,
            'party': ['Pidgey', 'Pidgey'],
            'party_address': 'Trainer_Party_Route_3_Lass_A',
        },
        {
            'level': 10,
            'party': ['Rattata', 'Nidoran M'],
            'party_address': 'Trainer_Party_Route_3_Lass_B',
        },
        {
            'level': 14,
            'party': ['Jigglypuff'],
            'party_address': 'Trainer_Party_Route_3_Lass_C',
        },
    ],
    'Mt Moon 1F': [
        {
            'level': 10,
            'party': ['Rattata', 'Rattata', 'Zubat'],
            'party_address': 'Trainer_Party_Mt_Moon_1F_Youngster_A',
        },
        {
            'level': 11,
            'party': ['Weedle', 'Kakuna'],
            'party_address': 'Trainer_Party_Mt_Moon_1F_BugCatcher_A',
        },
        {
            'level': 10,
            'party': ['Caterpie', 'Metapod', 'Caterpie'],
            'party_address': 'Trainer_Party_Mt_Moon_1F_BugCatcher_B',
        },
        {
            'level': 11,
            'party': ['Oddish', 'Bellsprout'],
            'party_address': 'Trainer_Party_Mt_Moon_1F_Lass_A',
        },
        {
            'level': 14,
            'party': ['Clefairy'],
            'party_address': 'Trainer_Party_Mt_Moon_1F_Lass_B',
        },
        {
            'level': 11,
            'party': ['Magnemite', 'Voltorb'],
            'party_address': 'Trainer_Party_Mt_Moon_1F_SuperNerd_A',
        },
        {
            'level': 10,
            'party': ['Geodude', 'Geodude', 'Onix'],
            'party_address': 'Trainer_Party_Mt_Moon_1F_Hiker_A',
        },
    ],
    'S.S. Anne 1F Rooms-Youngster and Lass Room': [
        {
            'level': 18,
            'party': ['Pidgey', 'Nidoran F'],
            'party_address': 'Trainer_Party_SS_Anne_1F_Rooms_Lass_A',
        },
        {
            'level': 21,
            'party': ['Nidoran M'],
            'party_address': 'Trainer_Party_SS_Anne_1F_Rooms_Youngster_A',
        },
    ],
    'S.S. Anne 1F Rooms-East Gentleman Room': [
        {
            'level': 18,
            'party': ['Growlithe', 'Growlithe'],
            'party_address': 'Trainer_Party_SS_Anne_1F_Rooms_Gentleman_A',
        },
    ],
    'S.S. Anne 1F Rooms-West Gentleman Room': [
        {
            'level': 19,
            'party': ['Nidoran M', 'Nidoran F'],
            'party_address': 'Trainer_Party_SS_Anne_1F_Rooms_Gentleman_B',
        },
    ],
    'Route 24': [
        {
            'level': 14,
            'party': ['Caterpie', 'Weedle'],
            'party_address': 'Trainer_Party_Route_24_BugCatcher_A',
        },
        {
            'level': 16,
            'party': ['Pidgey', 'Nidoran F'],
            'party_address': 'Trainer_Party_Route_24_Lass_A',
        },
        {
            'level': 14,
            'party': ['Pidgey', 'Nidoran F'],
            'party_address': 'Trainer_Party_Route_24_Lass_B',
        },
        {
            'level': 14,
            'party': ['Rattata', 'Ekans'],
            'party_address': 'Trainer_Party_Route_24_JrTrainerM_A',
        },
        {
            'level': 18,
            'party': ['Mankey'],
            'party_address': 'Trainer_Party_Route_24_JrTrainerM_C',
        },
        {
            'level': 15,
            'party': ['Ekans', 'Zubat'],
            'party_address': 'Trainer_Party_Route_24_Rocket_A',
        },
        {
            'level': 14,
            'party': ['Rattata', 'Ekans', 'Zubat'],
            'party_address': 'Trainer_Party_Route_24_Youngster_A',
        },
    ],
    'Route 6': [
        {
            'level': 16,
            'party': ['Weedle', 'Caterpie', 'Weedle'],
            'party_address': 'Trainer_Party_Route_6_BugCatcher_A',
        },
        {
            'level': 20,
            'party': ['Butterfree'],
            'party_address': 'Trainer_Party_Route_6_BugCatcher_B',
        },
        {
            'level': 20,
            'party': ['Squirtle'],
            'party_address': 'Trainer_Party_Route_6_JrTrainerM_A',
        },
        {
            'level': 16,
            'party': ['Spearow', 'Raticate'],
            'party_address': 'Trainer_Party_Route_6_JrTrainerM_B',
        },
        {
            'level': 16,
            'party': ['Pidgey', 'Pidgey', 'Pidgey'],
            'party_address': 'Trainer_Party_Route_6_JrTrainerF_B',
        },
    ],
    'Route 9': [
        {
            'level': 19,
            'party': ['Beedrill', 'Beedrill'],
            'party_address': 'Trainer_Party_Route_9_BugCatcher_A',
        },
        {
            'level': 20,
            'party': ['Caterpie', 'Weedle', 'Venonat'],
            'party_address': 'Trainer_Party_Route_9_BugCatcher_B',
        },
        {
            'level': 21,
            'party': ['Growlithe', 'Charmander'],
            'party_address': 'Trainer_Party_Route_9_JrTrainerM_A',
        },
        {
            'level': 19,
            'party': ['Rattata', 'Diglett', 'Ekans', 'Sandshrew'],
            'party_address': 'Trainer_Party_Route_9_JrTrainerM_B',
        },
        {
            'level': 18,
            'party': ['Oddish', 'Bellsprout', 'Oddish', 'Bellsprout'],
            'party_address': 'Trainer_Party_Route_9_JrTrainerF_A',
        },
        {
            'level': 23,
            'party': ['Meowth'],
            'party_address': 'Trainer_Party_Route_9_JrTrainerF_B',
        },
        {
            'level': 21,
            'party': ['Geodude', 'Onix'],
            'party_address': 'Trainer_Party_Route_9_Hiker_A',
        },
        {
            'level': 20,
            'party': ['Geodude', 'Machop', 'Geodude'],
            'party_address': 'Trainer_Party_Route_9_Hiker_B',
        },
        {
            'level': 20,
            'party': ['Machop', 'Onix'],
            'party_address': 'Trainer_Party_Route_9_Hiker_D',
        },
    ],
    'Route 4-Lass': [
        {
            'level': 31,
            'party': ['Paras', 'Paras', 'Parasect'],
            'party_address': 'Trainer_Party_Route_4_Lass_A',
        },
    ],
    'Route 25': [
        {
            'level': 15,
            'party': ['Nidoran M', 'Nidoran F'],
            'party_address': 'Trainer_Party_Route_25_Lass_A',
        },
        {
            'level': 13,
            'party': ['Oddish', 'Pidgey', 'Oddish'],
            'party_address': 'Trainer_Party_Route_25_Lass_B',
        },
        {
            'level': 14,
            'party': ['Rattata', 'Ekans'],
            'party_address': 'Trainer_Party_Route_25_JrTrainerM_A',
        },
        {
            'level': 15,
            'party': ['Machop', 'Geodude'],
            'party_address': 'Trainer_Party_Route_25_Hiker_A',
        },
        {
            'level': 13,
            'party': ['Geodude', 'Geodude', 'Machop', 'Geodude'],
            'party_address': 'Trainer_Party_Route_25_Hiker_B',
        },
        {
            'level': 17,
            'party': ['Onix'],
            'party_address': 'Trainer_Party_Route_25_Hiker_C',
        },
        {
            'level': 15,
            'party': ['Rattata', 'Spearow'],
            'party_address': 'Trainer_Party_Route_25_Youngster_A',
        },
        {
            'level': 17,
            'party': ['Slowpoke'],
            'party_address': 'Trainer_Party_Route_25_Youngster_B',
        },
        {
            'level': 14,
            'party': ['Ekans', 'Sandshrew'],
            'party_address': 'Trainer_Party_Route_25_Youngster_C',
        },
    ],
    'S.S. Anne 2F Rooms-Gentleman and Lass Room': [
        {
            'level': 17,
            'party': ['Growlithe', 'Ponyta'],
            'party_address': 'Trainer_Party_SS_Anne_2F_Rooms_Gentleman_C',
        },
    ],
    'S.S. Anne 2F Rooms-Fisherman and Gentleman Room': [
        {
            'level': 17,
            'party': ['Goldeen', 'Tentacool', 'Goldeen'],
            'party_address': 'Trainer_Party_SS_Anne_2F_Rooms_Fisher_A',
        },
    ],
    'Route 8': [
        {
            'level': 23,
            'party': ['Nidoran F', 'Nidorina'],
            'party_address': 'Trainer_Party_Route_8_Lass_A',
        },
        {
            'level': 24,
            'party': ['Meowth', 'Meowth', 'Meowth'],
            'party_address': 'Trainer_Party_Route_8_Lass_B',
        },
        {
            'level': 22,
            'party': ['Clefairy', 'Clefairy'],
            'party_address': 'Trainer_Party_Route_8_Lass_D',
        },
        {
            'level': 20,
            'party': ['Voltorb', 'Koffing', 'Voltorb', 'Magnemite'],
            'party_address': 'Trainer_Party_Route_8_SuperNerd_A',
        },
        {
            'level': 22,
            'party': ['Grimer', 'Muk', 'Grimer'],
            'party_address': 'Trainer_Party_Route_8_SuperNerd_B',
        },
        {
            'level': 26,
            'party': ['Koffing'],
            'party_address': 'Trainer_Party_Route_8_SuperNerd_C',
        },
        {
            'level': 22,
            'party': ['Poliwag', 'Poliwag', 'Poliwhirl'],
            'party_address': 'Trainer_Party_Route_8_Gambler_A',
        },
        {
            'level': 24,
            'party': ['Growlithe', 'Vulpix'],
            'party_address': 'Trainer_Party_Route_8_Gambler_C',
        },
    ],
    'Celadon Gym': [
        {
            'level': 23,
            'party': ['Bellsprout', 'Weepinbell'],
            'party_address': 'Trainer_Party_Celadon_Gym_Lass_A',
        },
        {
            'level': 24,
            'party': ['Bulbasaur', 'Ivysaur'],
            'party_address': 'Trainer_Party_Celadon_Gym_JrTrainerF_A',
        },
        {
            'level': 21,
            'party': ['Oddish', 'Bellsprout', 'Oddish', 'Bellsprout'],
            'party_address': 'Trainer_Party_Celadon_Gym_Beauty_A',
        },
        {
            'level': 24,
            'party': ['Bellsprout', 'Bellsprout'],
            'party_address': 'Trainer_Party_Celadon_Gym_Beauty_B',
        },
    ],
    'Celadon Gym-C': [
        {
            'level': 24,
            'party': ['Weepinbell', 'Gloom', 'Ivysaur'],
            'party_address': 'Trainer_Party_Celadon_Gym_CooltrainerF_A',
        },
        {
            'level': 23,
            'party': ['Oddish', 'Gloom'],
            'party_address': 'Trainer_Party_Celadon_Gym_Lass_B',
        },
        {
            'level': 26,
            'party': ['Exeggcute'],
            'party_address': 'Trainer_Party_Celadon_Gym_Beauty_C',
        },
    ],
    'S.S. Anne Bow': [
        {
            'level': 18,
            'party': ['Machop', 'Shellder'],
            'party_address': 'Trainer_Party_SS_Anne_Stern_Sailor_A',
        },
        {
            'level': 17,
            'party': ['Machop', 'Tentacool'],
            'party_address': 'Trainer_Party_SS_Anne_Stern_Sailor_B',
        },
    ],
    'S.S. Anne B1F Rooms-Two Sailors Room': [
        {
            'level': 21,
            'party': ['Shellder'],
            'party_address': 'Trainer_Party_SS_Anne_B1F_Rooms_Sailor_A',
        },
        {
            'level': 17,
            'party': ['Horsea', 'Shellder', 'Tentacool'],
            'party_address': 'Trainer_Party_SS_Anne_B1F_Rooms_Sailor_B',
        },
    ],
    'S.S. Anne B1F Rooms-East Single Sailor Room': [
        {
            'level': 17,
            'party': ['Horsea', 'Horsea', 'Horsea'],
            'party_address': 'Trainer_Party_SS_Anne_B1F_Rooms_Sailor_D',
        },
    ],
    'S.S. Anne B1F Rooms-West Single Sailor Room': [
        {
            'level': 18,
            'party': ['Tentacool', 'Staryu'],
            'party_address': 'Trainer_Party_SS_Anne_B1F_Rooms_Sailor_C',
        },
    ],
    'S.S. Anne B1F Rooms-Fisherman Room': [
        {
            'level': 20,
            'party': ['Machop'],
            'party_address': 'Trainer_Party_SS_Anne_B1F_Rooms_Sailor_E',
        },
        {
            'level': 17,
            'party': ['Tentacool', 'Staryu', 'Shellder'],
            'party_address': 'Trainer_Party_SS_Anne_B1F_Rooms_Fisher_A',
        },
    ],
    'Route 12-Grass': [
        {
            'level': 24,
            'party': ['Magikarp', 'Magikarp'],
            'party_address': 'Trainer_Party_Route_12_Fisher_F',
        },
    ],
    'Route 12-S': [
        {
            'level': 29,
            'party': ['Nidoran M', 'Nidorino'],
            'party_address': 'Trainer_Party_Route_12_JrTrainerM_A',
        },
        {
            'level': 29,
            'party': ['Voltorb', 'Electrode'],
            'party_address': 'Trainer_Party_Route_12_Rocker_A',
        },
    ],
    'Route 12-N': [
        {
            'level': 22,
            'party': ['Goldeen', 'Poliwag', 'Goldeen'],
            'party_address': 'Trainer_Party_Route_12_Fisher_A',
        },
        {
            'level': 24,
            'party': ['Tentacool', 'Goldeen'],
            'party_address': 'Trainer_Party_Route_12_Fisher_B',
        },
        {
            'level': 27,
            'party': ['Goldeen'],
            'party_address': 'Trainer_Party_Route_12_Fisher_C',
        },
        {
            'level': 21,
            'party': ['Poliwag', 'Shellder', 'Goldeen', 'Horsea'],
            'party_address': 'Trainer_Party_Route_12_Fisher_D',
        },
    ],
    'Cerulean Gym': [
        {
            'level': 19,
            'party': ['Goldeen'],
            'party_address': 'Trainer_Party_Cerulean_Gym_JrTrainerF_A',
        },
        {
            'level': 16,
            'party': ['Horsea', 'Shellder'],
            'party_address': 'Trainer_Party_Cerulean_Gym_Swimmer_A',
        },
        {
            'level': [18, 21],
            'party': ['Staryu', 'Starmie'],
            'party_address': 'Trainer_Party_Misty_A',
        },
    ],
    'Route 10-C': [
        {
            'level': 30,
            'party': ['Rhyhorn', 'Lickitung'],
            'party_address': 'Trainer_Party_Route_10_Pokemaniac_A',
        },
    ],
    'Route 10-S': [
        {
            'level': 21,
            'party': ['Pidgey', 'Pidgeotto'],
            'party_address': 'Trainer_Party_Route_10_JrTrainerF_B',
        },
        {
            'level': 20,
            'party': ['Cubone', 'Slowpoke'],
            'party_address': 'Trainer_Party_Route_10_Pokemaniac_B',
        },
        {
            'level': 21,
            'party': ['Geodude', 'Onix'],
            'party_address': 'Trainer_Party_Route_10_Hiker_A',
        },
        {
            'level': 19,
            'party': ['Onix', 'Graveler'],
            'party_address': 'Trainer_Party_Route_10_Hiker_B',
        },
    ],
    'Rock Tunnel B1F-W': [
        {
            'level': 21,
            'party': ['Jigglypuff', 'Pidgey', 'Meowth'],
            'party_address': 'Trainer_Party_Rock_Tunnel_B1F_JrTrainerF_A',
            'location_name': 'Rock Tunnel B1F - Jr Trainer F 2',
        },
        {
            'level': 20,
            'party': ['Slowpoke', 'Slowpoke', 'Slowpoke'],
            'party_address': 'Trainer_Party_Rock_Tunnel_B1F_Pokemaniac_A',
            'location_name': 'Rock Tunnel B1F - PokeManiac 3',
        },
        {
            'level': 21,
            'party': ['Geodude', 'Geodude', 'Graveler'],
            'party_address': 'Trainer_Party_Rock_Tunnel_B1F_Hiker_A',
            'location_name': 'Rock Tunnel B1F - Hiker 3',
        },
    ],
    'Rock Tunnel B1F-E': [
        {
            'level': 22,
            'party': ['Oddish', 'Bulbasaur'],
            'party_address': 'Trainer_Party_Rock_Tunnel_B1F_JrTrainerF_B',
            'location_name': 'Rock Tunnel B1F - Jr Trainer F 1',
        },
        {
            'level': 22,
            'party': ['Charmander', 'Cubone'],
            'party_address': 'Trainer_Party_Rock_Tunnel_B1F_Pokemaniac_B',
            'location_name': 'Rock Tunnel B1F - PokeManiac 2',
        },
        {
            'level': 25,
            'party': ['Slowpoke'],
            'party_address': 'Trainer_Party_Rock_Tunnel_B1F_Pokemaniac_C',
            'location_name': 'Rock Tunnel B1F - PokeManiac 1',
        },
        {
            'level': 25,
            'party': ['Geodude'],
            'party_address': 'Trainer_Party_Rock_Tunnel_B1F_Hiker_B',
            'location_name': 'Rock Tunnel B1F - Hiker 2',
        },
        {
            'level': 20,
            'party': ['Machop', 'Onix'],
            'party_address': 'Trainer_Party_Rock_Tunnel_B1F_Hiker_D',
            'location_name': 'Rock Tunnel B1F - Hiker 1',
        },
    ],
    'Route 13-E': [
        {
            'level': 28,
            'party': ['Goldeen', 'Poliwag', 'Horsea'],
            'party_address': 'Trainer_Party_Route_13_JrTrainerF_D',
        },
        {
            'level': 29,
            'party': ['Pidgey', 'Pidgeotto'],
            'party_address': 'Trainer_Party_Route_13_BirdKeeper_A',
        },
    ],
    'Route 13': [
        {
            'level': 30,
            'party': ['Poliwag', 'Poliwag'],
            'party_address': 'Trainer_Party_Route_13_JrTrainerF_B',
        },
        {
            'level': 27,
            'party': ['Pidgey', 'Meowth', 'Pidgey', 'Pidgeotto'],
            'party_address': 'Trainer_Party_Route_13_JrTrainerF_C',
        },
        {
            'level': 28,
            'party': ['Koffing', 'Koffing', 'Koffing'],
            'party_address': 'Trainer_Party_Route_13_Biker_A',
        },
        {
            'level': 29,
            'party': ['Clefairy', 'Meowth'],
            'party_address': 'Trainer_Party_Route_13_Beauty_B',
        },
        {
            'level': 25,
            'party': ['Spearow', 'Pidgey', 'Pidgey', 'Spearow', 'Spearow'],
            'party_address': 'Trainer_Party_Route_13_BirdKeeper_B',
        },
        {
            'level': 26,
            'party': ['Pidgey', 'Pidgeotto', 'Spearow', 'Fearow'],
            'party_address': 'Trainer_Party_Route_13_BirdKeeper_C',
        },
    ],
    'Route 20-E': [
        {
            'level': 31,
            'party': ['Shellder', 'Cloyster'],
            'party_address': 'Trainer_Party_Route_20_Swimmer_A',
        },
        {
            'level': 28,
            'party': ['Horsea', 'Horsea', 'Seadra', 'Horsea'],
            'party_address': 'Trainer_Party_Route_20_Swimmer_C',
        },
        {
            'level': 30,
            'party': ['Seadra', 'Horsea', 'Seadra'],
            'party_address': 'Trainer_Party_Route_20_Beauty_E',
        },
        {
            'level': 35,
            'party': ['Seaking'],
            'party_address': 'Trainer_Party_Route_20_Beauty_A',
        },
    ],
    'Route 20-W': [
        {
            'level': 31,
            'party': ['Goldeen', 'Seaking'],
            'party_address': 'Trainer_Party_Route_20_JrTrainerF_A',
        },
        {
            'level': 30,
            'party': ['Tentacool', 'Horsea', 'Seel'],
            'party_address': 'Trainer_Party_Route_20_JrTrainerF_C',
        },
        {
            'level': 35,
            'party': ['Staryu'],
            'party_address': 'Trainer_Party_Route_20_Swimmer_B',
        },
        {
            'level': 30,
            'party': ['Shellder', 'Shellder', 'Cloyster'],
            'party_address': 'Trainer_Party_Route_20_Beauty_B',
        },
        {
            'level': 31,
            'party': ['Poliwag', 'Seaking'],
            'party_address': 'Trainer_Party_Route_20_Beauty_C',
        },
        {
            'level': 30,
            'party': ['Fearow', 'Fearow', 'Pidgeotto'],
            'party_address': 'Trainer_Party_Route_20_BirdKeeper_A',
        },
    ],
    'Rock Tunnel 1F-S': [
        {
            'level': 22,
            'party': ['Bellsprout', 'Clefairy'],
            'party_address': 'Trainer_Party_Rock_Tunnel_1F_JrTrainerF_A',
            'location_name': 'Rock Tunnel B1F - Jr Trainer F 1',
        },
        {
            'level': 20,
            'party': ['Meowth', 'Oddish', 'Pidgey'],
            'party_address': 'Trainer_Party_Rock_Tunnel_1F_JrTrainerF_B',
            'location_name': 'Rock Tunnel B1F - Jr Trainer F 2',
        },
        {
            'level': 19,
            'party': ['Pidgey', 'Rattata', 'Rattata', 'Bellsprout'],
            'party_address': 'Trainer_Party_Rock_Tunnel_1F_JrTrainerF_C',
            'location_name': 'Rock Tunnel B1F - Jr Trainer F 3',
        },
    ],
    'Rock Tunnel 1F-NE': [
        {
            'level': 23,
            'party': ['Cubone', 'Slowpoke'],
            'party_address': 'Trainer_Party_Rock_Tunnel_1F_Pokemaniac_A',
            'location_name': 'Rock Tunnel 1F - PokeManiac',
        },
    ],
    'Rock Tunnel 1F-NW': [
        {
            'level': 19,
            'party': ['Geodude', 'Machop', 'Geodude', 'Geodude'],
            'party_address': 'Trainer_Party_Rock_Tunnel_1F_Hiker_A',
            'location_name': 'Rock Tunnel 1F - Hiker 1',
        },
        {
            'level': 20,
            'party': ['Onix', 'Onix', 'Geodude'],
            'party_address': 'Trainer_Party_Rock_Tunnel_1F_Hiker_B',
            'location_name': 'Rock Tunnel 1F - Hiker 2',
        },
        {
            'level': 21,
            'party': ['Geodude', 'Graveler'],
            'party_address': 'Trainer_Party_Rock_Tunnel_1F_Hiker_C',
            'location_name': 'Rock Tunnel 1F - Hiker 3',
        },
    ],
    'Route 15-N': [
        {
            'level': 33,
            'party': ['Clefairy'],
            'party_address': 'Trainer_Party_Route_15_JrTrainerF_C',
        },
    ],
    'Route 15': [
        {
            'level': 28,
            'party': ['Gloom', 'Oddish', 'Oddish'],
            'party_address': 'Trainer_Party_Route_15_JrTrainerF_A',
        },
        {
            'level': 29,
            'party': ['Bellsprout', 'Oddish', 'Tangela'],
            'party_address': 'Trainer_Party_Route_15_JrTrainerF_D',
        },
        {
            'level': 25,
            'party': ['Koffing', 'Koffing', 'Weezing', 'Koffing', 'Grimer'],
            'party_address': 'Trainer_Party_Route_15_Biker_A',
        },
        {
            'level': 28,
            'party': ['Koffing', 'Grimer', 'Weezing'],
            'party_address': 'Trainer_Party_Route_15_Biker_B',
        },
        {
            'level': 29,
            'party': ['Pidgeotto', 'Wigglytuff'],
            'party_address': 'Trainer_Party_Route_15_Beauty_A',
        },
        {
            'level': 29,
            'party': ['Bulbasaur', 'Ivysaur'],
            'party_address': 'Trainer_Party_Route_15_Beauty_B',
        },
        {
            'level': 26,
            'party': ['Pidgeotto', 'Farfetchd', 'Doduo', 'Pidgey'],
            'party_address': 'Trainer_Party_Route_15_BirdKeeper_A',
        },
        {
            'level': 28,
            'party': ['Dodrio', 'Doduo', 'Doduo'],
            'party_address': 'Trainer_Party_Route_15_BirdKeeper_B',
        },
    ],
    'Victory Road 2F-NW': [
        {
            'level': 40,
            'party': ['Charmeleon', 'Lapras', 'Lickitung'],
            'party_address': 'Trainer_Party_Victory_Road_2F_Pokemaniac_A',
        },
    ],
    'Victory Road 2F-C': [
        {
            'level': 41,
            'party': ['Drowzee', 'Hypno', 'Kadabra', 'Kadabra'],
            'party_address': 'Trainer_Party_Victory_Road_2F_Juggler_A',
        },
        {
            'level': 48,
            'party': ['Mr Mime'],
            'party_address': 'Trainer_Party_Victory_Road_2F_Juggler_C',
        },
        {
            'level': 44,
            'party': ['Persian', 'Golduck'],
            'party_address': 'Trainer_Party_Victory_Road_2F_Tamer_A',
        },
        {
            'level': 43,
            'party': ['Machoke', 'Machop', 'Machoke'],
            'party_address': 'Trainer_Party_Victory_Road_2F_Blackbelt_A',
        },
    ],
    'Mt Moon B2F': [
        {
            'level': 12,
            'party': ['Grimer', 'Voltorb', 'Koffing'],
            'party_address': 'Trainer_Party_Mt_Moon_B2F_SuperNerd_A',
        },
        {
            'level': 13,
            'party': ['Rattata', 'Zubat'],
            'party_address': 'Trainer_Party_Mt_Moon_B2F_Rocket_A',
        },
        {
            'level': 16,
            'party': ['Raticate'],
            'party_address': 'Trainer_Party_Mt_Moon_B2F_Rocket_D',
        },
    ],
    'Mt Moon B2F-NE': [
        {
            'level': 12,
            'party': ['Zubat', 'Ekans'],
            'party_address': 'Trainer_Party_Mt_Moon_B2F_Rocket_C',
        },
    ],
    'Mt Moon B2F-C': [
        {
            'level': 11,
            'party': ['Sandshrew', 'Rattata', 'Zubat'],
            'party_address': 'Trainer_Party_Mt_Moon_B2F_Rocket_B',
        },
    ],
    'Cinnabar Gym': [
        {
            'level': 36,
            'party': ['Vulpix', 'Vulpix', 'Ninetales'],
            'party_address': 'Trainer_Party_Cinnabar_Gym_SuperNerd_A',
        },
        {
            'level': 34,
            'party': ['Ponyta', 'Charmander', 'Vulpix', 'Growlithe'],
            'party_address': 'Trainer_Party_Cinnabar_Gym_SuperNerd_B',
        },
        {
            'level': 41,
            'party': ['Rapidash'],
            'party_address': 'Trainer_Party_Cinnabar_Gym_SuperNerd_C',
        },
        {
            'level': 37,
            'party': ['Growlithe', 'Vulpix'],
            'party_address': 'Trainer_Party_Cinnabar_Gym_SuperNerd_D',
        },
        {
            'level': 36,
            'party': ['Growlithe', 'Vulpix', 'Ninetales'],
            'party_address': 'Trainer_Party_Cinnabar_Gym_Burglar_A',
        },
        {
            'level': 41,
            'party': ['Ponyta'],
            'party_address': 'Trainer_Party_Cinnabar_Gym_Burglar_B',
        },
        {
            'level': 37,
            'party': ['Vulpix', 'Growlithe'],
            'party_address': 'Trainer_Party_Cinnabar_Gym_Burglar_C',
        },
    ],
    'Route 14': [
        {
            'level': 29,
            'party': ['Koffing', 'Grimer'],
            'party_address': 'Trainer_Party_Route_14_Biker_A',
        },
        {
            'level': 26,
            'party': ['Koffing', 'Koffing', 'Grimer', 'Koffing'],
            'party_address': 'Trainer_Party_Route_14_Biker_C',
        },
        {
            'level': 28,
            'party': ['Grimer', 'Grimer', 'Koffing'],
            'party_address': 'Trainer_Party_Route_14_Biker_D',
        },
        {
            'level': 29,
            'party': ['Koffing', 'Muk'],
            'party_address': 'Trainer_Party_Route_14_Biker_E',
        },
        {
            'level': 33,
            'party': ['Farfetchd'],
            'party_address': 'Trainer_Party_Route_14_BirdKeeper_A',
        },
        {
            'level': 29,
            'party': ['Spearow', 'Fearow'],
            'party_address': 'Trainer_Party_Route_14_BirdKeeper_B',
        },
        {
            'level': 28,
            'party': ['Pidgey', 'Doduo', 'Pidgeotto'],
            'party_address': 'Trainer_Party_Route_14_BirdKeeper_D',
        },
        {
            'level': 26,
            'party': ['Pidgey', 'Spearow', 'Pidgey', 'Fearow'],
            'party_address': 'Trainer_Party_Route_14_BirdKeeper_E',
        },
        {
            'level': 29,
            'party': ['Pidgeotto', 'Fearow'],
            'party_address': 'Trainer_Party_Route_14_BirdKeeper_F',
        },
        {
            'level': 28,
            'party': ['Spearow', 'Doduo', 'Fearow'],
            'party_address': 'Trainer_Party_Route_14_BirdKeeper_G',
        },
    ],
    'Route 16-SW': [
        {
            'level': 29,
            'party': ['Grimer', 'Koffing'],
            'party_address': 'Trainer_Party_Route_16_Biker_A',
        },
        {
            'level': 33,
            'party': ['Weezing'],
            'party_address': 'Trainer_Party_Route_16_Biker_B',
        },
        {
            'level': 26,
            'party': ['Grimer', 'Grimer', 'Grimer', 'Grimer'],
            'party_address': 'Trainer_Party_Route_16_Biker_C',
        },
        {
            'level': 28,
            'party': ['Machop', 'Mankey', 'Machop'],
            'party_address': 'Trainer_Party_Route_16_CueBall_A',
        },
        {
            'level': 29,
            'party': ['Mankey', 'Machop'],
            'party_address': 'Trainer_Party_Route_16_CueBall_B',
        },
        {
            'level': 33,
            'party': ['Machop'],
            'party_address': 'Trainer_Party_Route_16_CueBall_C',
        },
    ],
    'Route 17': [
        {
            'level': 28,
            'party': ['Weezing', 'Koffing', 'Weezing'],
            'party_address': 'Trainer_Party_Route_17_Biker_A',
        },
        {
            'level': 33,
            'party': ['Muk'],
            'party_address': 'Trainer_Party_Route_17_Biker_B',
        },
        {
            'level': 29,
            'party': ['Voltorb', 'Voltorb'],
            'party_address': 'Trainer_Party_Route_17_Biker_C',
        },
        {
            'level': 29,
            'party': ['Weezing', 'Muk'],
            'party_address': 'Trainer_Party_Route_17_Biker_D',
        },
        {
            'level': 25,
            'party': ['Koffing', 'Weezing', 'Koffing', 'Koffing', 'Weezing'],
            'party_address': 'Trainer_Party_Route_17_Biker_E',
        },
        {
            'level': 29,
            'party': ['Mankey', 'Primeape'],
            'party_address': 'Trainer_Party_Route_17_CueBall_A',
        },
        {
            'level': 29,
            'party': ['Machop', 'Machoke'],
            'party_address': 'Trainer_Party_Route_17_CueBall_B',
        },
        {
            'level': 33,
            'party': ['Machoke'],
            'party_address': 'Trainer_Party_Route_17_CueBall_C',
        },
        {
            'level': 26,
            'party': ['Mankey', 'Mankey', 'Machoke', 'Machop'],
            'party_address': 'Trainer_Party_Route_17_CueBall_D',
        },
        {
            'level': 29,
            'party': ['Primeape', 'Machoke'],
            'party_address': 'Trainer_Party_Route_17_CueBall_E',
        },
    ],
    'Pokemon Mansion 2F': [
        {
            'level': 34,
            'party': ['Charmander', 'Charmeleon'],
            'party_address': 'Trainer_Party_Mansion_2F_Burglar_A',
        },
    ],
    'Pokemon Mansion 3F-SW': [
        {
            'level': 38,
            'party': ['Ninetales'],
            'party_address': 'Trainer_Party_Mansion_3F_Burglar_A',
        },
    ],
    'Pokemon Mansion 3F-SE': [
        {
            'level': 33,
            'party': ['Magnemite', 'Magneton', 'Voltorb'],
            'party_address': 'Trainer_Party_Mansion_3F_Scientist_A',
        },
    ],
    'Pokemon Mansion B1F': [
        {
            'level': 34,
            'party': ['Growlithe', 'Ponyta'],
            'party_address': 'Trainer_Party_Mansion_B1F_Burglar_A',
        },
        {
            'level': 34,
            'party': ['Magnemite', 'Electrode'],
            'party_address': 'Trainer_Party_Mansion_B1F_Scientist_A',
        },
    ],
    'Route 11': [
        {
            'level': 21,
            'party': ['Magnemite'],
            'party_address': 'Trainer_Party_Route_11_Engineer_A',
        },
        {
            'level': 18,
            'party': ['Magnemite', 'Magnemite', 'Magneton'],
            'party_address': 'Trainer_Party_Route_11_Engineer_B',
        },
        {
            'level': 18,
            'party': ['Poliwag', 'Horsea'],
            'party_address': 'Trainer_Party_Route_11_Gambler_A',
        },
        {
            'level': 18,
            'party': ['Bellsprout', 'Oddish'],
            'party_address': 'Trainer_Party_Route_11_Gambler_B',
        },
        {
            'level': 18,
            'party': ['Voltorb', 'Magnemite'],
            'party_address': 'Trainer_Party_Route_11_Gambler_C',
        },
        {
            'level': 18,
            'party': ['Growlithe', 'Vulpix'],
            'party_address': 'Trainer_Party_Route_11_Gambler_D',
        },
        {
            'level': 21,
            'party': ['Ekans'],
            'party_address': 'Trainer_Party_Route_11_Youngster_A',
        },
        {
            'level': 19,
            'party': ['Sandshrew', 'Zubat'],
            'party_address': 'Trainer_Party_Route_11_Youngster_B',
        },
        {
            'level': 17,
            'party': ['Rattata', 'Rattata', 'Raticate'],
            'party_address': 'Trainer_Party_Route_11_Youngster_C',
        },
        {
            'level': 18,
            'party': ['Nidoran M', 'Nidorino'],
            'party_address': 'Trainer_Party_Route_11_Youngster_D',
        },
    ],
    'Route 21': [
        {
            'level': 28,
            'party': ['Seaking', 'Goldeen', 'Seaking', 'Seaking'],
            'party_address': 'Trainer_Party_Route_21_Fisher_A',
        },
        {
            'level': 31,
            'party': ['Shellder', 'Cloyster'],
            'party_address': 'Trainer_Party_Route_21_Fisher_B',
        },
        {
            'level': 27,
            'party': ['Magikarp', 'Magikarp', 'Magikarp', 'Magikarp', 'Magikarp', 'Magikarp'],
            'party_address': 'Trainer_Party_Route_21_Fisher_C',
        },
        {
            'level': 33,
            'party': ['Seaking', 'Goldeen'],
            'party_address': 'Trainer_Party_Route_21_Fisher_D',
        },
        {
            'level': 33,
            'party': ['Seadra', 'Tentacruel'],
            'party_address': 'Trainer_Party_Route_21_Swimmer_A',
        },
        {
            'level': 37,
            'party': ['Starmie'],
            'party_address': 'Trainer_Party_Route_21_Swimmer_B',
        },
        {
            'level': 33,
            'party': ['Staryu', 'Wartortle'],
            'party_address': 'Trainer_Party_Route_21_Swimmer_C',
        },
        {
            'level': 32,
            'party': ['Poliwhirl', 'Tentacool', 'Seadra'],
            'party_address': 'Trainer_Party_Route_21_Swimmer_D',
        },
        {
            'level': 31,
            'party': ['Tentacool', 'Tentacool', 'Tentacruel'],
            'party_address': 'Trainer_Party_Route_21_CueBall_A',
        },
    ],
    'Route 19-N': [
        {
            'level': 30,
            'party': ['Tentacool', 'Shellder'],
            'party_address': 'Trainer_Party_Route_19_Swimmer_A',
        },
        {
            'level': 29,
            'party': ['Goldeen', 'Horsea', 'Staryu'],
            'party_address': 'Trainer_Party_Route_19_Swimmer_B',
        },
    ],
    'Route 19-S': [
        {
            'level': 30,
            'party': ['Poliwag', 'Poliwhirl'],
            'party_address': 'Trainer_Party_Route_19_Swimmer_C',
        },
        {
            'level': 27,
            'party': ['Horsea', 'Tentacool', 'Tentacool', 'Goldeen'],
            'party_address': 'Trainer_Party_Route_19_Swimmer_D',
        },
        {
            'level': 29,
            'party': ['Goldeen', 'Shellder', 'Seaking'],
            'party_address': 'Trainer_Party_Route_19_Swimmer_E',
        },
        {
            'level': 30,
            'party': ['Horsea', 'Horsea'],
            'party_address': 'Trainer_Party_Route_19_Swimmer_F',
        },
        {
            'level': 27,
            'party': ['Tentacool', 'Tentacool', 'Staryu', 'Horsea', 'Tentacruel'],
            'party_address': 'Trainer_Party_Route_19_Swimmer_G',
        },
        {
            'level': 27,
            'party': ['Poliwag', 'Goldeen', 'Seaking', 'Goldeen', 'Poliwag'],
            'party_address': 'Trainer_Party_Route_19_Beauty_A',
        },
        {
            'level': 30,
            'party': ['Goldeen', 'Seaking'],
            'party_address': 'Trainer_Party_Route_19_Beauty_B',
        },
        {
            'level': 29,
            'party': ['Staryu', 'Staryu', 'Staryu'],
            'party_address': 'Trainer_Party_Route_19_Beauty_C',
        },
    ],
    'Saffron Gym-NE': [
        {
            'level': 31,
            'party': ['Kadabra', 'Slowpoke', 'Mr Mime', 'Kadabra'],
            'party_address': 'Trainer_Party_Saffron_Gym_Psychic_A',
        },
    ],
    'Saffron Gym-E': [
        {
            'level': 34,
            'party': ['Mr Mime', 'Kadabra'],
            'party_address': 'Trainer_Party_Saffron_Gym_Psychic_B',
        },
    ],
    'Saffron Gym-SE': [
        {
            'level': 33,
            'party': ['Slowpoke', 'Slowpoke', 'Slowbro'],
            'party_address': 'Trainer_Party_Saffron_Gym_Psychic_C',
        },
    ],
    'Saffron Gym-NW': [
        {
            'level': 38,
            'party': ['Slowbro'],
            'party_address': 'Trainer_Party_Saffron_Gym_Psychic_D',
        },
    ],
    'Saffron Gym-N': [
        {
            'level': 34,
            'party': ['Gastly', 'Haunter'],
            'party_address': 'Trainer_Party_Saffron_Gym_Channeler_A',
        },
    ],
    'Saffron Gym-W': [
        {
            'level': 38,
            'party': ['Haunter'],
            'party_address': 'Trainer_Party_Saffron_Gym_Channeler_B',
        },
    ],
    'Saffron Gym-SW': [
        {
            'level': 33,
            'party': ['Gastly', 'Gastly', 'Haunter'],
            'party_address': 'Trainer_Party_Saffron_Gym_Channeler_C',
        },
    ],
    'Silph Co 5F': [
        {
            'level': 29,
            'party': ['Kadabra', 'Mr Mime'],
            'party_address': 'Trainer_Party_Silph_Co_5F_Juggler_A',
        },
        {
            'level': 26,
            'party': ['Magneton', 'Koffing', 'Weezing', 'Magnemite'],
            'party_address': 'Trainer_Party_Silph_Co_5F_Scientist_A',
        },
        {
            'level': 33,
            'party': ['Arbok'],
            'party_address': 'Trainer_Party_Silph_Co_5F_Rocket_A',
        },
        {
            'level': 33,
            'party': ['Hypno'],
            'party_address': 'Trainer_Party_Silph_Co_5F_Rocket_B',
        },
    ],
    'Fuchsia Gym': [
        {
            'level': 31,
            'party': ['Drowzee', 'Drowzee', 'Kadabra', 'Drowzee'],
            'party_address': 'Trainer_Party_Fuchsia_Gym_Juggler_A',
        },
        {
            'level': 34,
            'party': ['Drowzee', 'Hypno'],
            'party_address': 'Trainer_Party_Fuchsia_Gym_Juggler_B',
        },
        {
            'level': 38,
            'party': ['Hypno'],
            'party_address': 'Trainer_Party_Fuchsia_Gym_Juggler_D',
        },
        {
            'level': 34,
            'party': ['Drowzee', 'Kadabra'],
            'party_address': 'Trainer_Party_Fuchsia_Gym_Juggler_E',
        },
        {
            'level': 34,
            'party': ['Sandslash', 'Arbok'],
            'party_address': 'Trainer_Party_Fuchsia_Gym_Tamer_A',
        },
        {
            'level': 33,
            'party': ['Arbok', 'Sandslash', 'Arbok'],
            'party_address': 'Trainer_Party_Fuchsia_Gym_Tamer_B',
        },
    ],
    'Viridian Gym': [
        {
            'level': 43,
            'party': ['Rhyhorn'],
            'party_address': 'Trainer_Party_Viridian_Gym_Tamer_A',
        },
        {
            'level': 39,
            'party': ['Arbok', 'Tauros'],
            'party_address': 'Trainer_Party_Viridian_Gym_Tamer_B',
        },
        {
            'level': 40,
            'party': ['Machop', 'Machoke'],
            'party_address': 'Trainer_Party_Viridian_Gym_Blackbelt_A',
        },
        {
            'level': 43,
            'party': ['Machoke'],
            'party_address': 'Trainer_Party_Viridian_Gym_Blackbelt_B',
        },
        {
            'level': 38,
            'party': ['Machoke', 'Machop', 'Machoke'],
            'party_address': 'Trainer_Party_Viridian_Gym_Blackbelt_C',
        },
        {
            'level': 39,
            'party': ['Nidorino', 'Nidoking'],
            'party_address': 'Trainer_Party_Viridian_Gym_CooltrainerM_A',
        },
        {
            'level': 39,
            'party': ['Sandslash', 'Dugtrio'],
            'party_address': 'Trainer_Party_Viridian_Gym_CooltrainerM_C',
        },
        {
            'level': 43,
            'party': ['Rhyhorn'],
            'party_address': 'Trainer_Party_Viridian_Gym_CooltrainerM_D',
        },
    ],
    'Route 18-E': [
        {
            'level': 29,
            'party': ['Spearow', 'Fearow'],
            'party_address': 'Trainer_Party_Route_18_BirdKeeper_A',
        },
        {
            'level': 34,
            'party': ['Dodrio'],
            'party_address': 'Trainer_Party_Route_18_BirdKeeper_B',
        },
        {
            'level': 26,
            'party': ['Spearow', 'Spearow', 'Fearow', 'Spearow'],
            'party_address': 'Trainer_Party_Route_18_BirdKeeper_C',
        },
    ],
    'Saffron Fighting Dojo': [
        {
            'level': 37,
            'party': ['Hitmonlee', 'Hitmonchan'],
            'party_address': 'Trainer_Party_Fighting_Dojo_Blackbelt_A',
        },
        {
            'level': 31,
            'party': ['Mankey', 'Mankey', 'Primeape'],
            'party_address': 'Trainer_Party_Fighting_Dojo_Blackbelt_B',
        },
        {
            'level': 32,
            'party': ['Machop', 'Machoke'],
            'party_address': 'Trainer_Party_Fighting_Dojo_Blackbelt_C',
        },
        {
            'level': 36,
            'party': ['Primeape'],
            'party_address': 'Trainer_Party_Fighting_Dojo_Blackbelt_D',
        },
        {
            'level': 31,
            'party': ['Machop', 'Mankey', 'Primeape'],
            'party_address': 'Trainer_Party_Fighting_Dojo_Blackbelt_E',
        },
    ],
    'Cerulean City': [
        {
            'level': 17,
            'party': ['Machop', 'Drowzee'],
            'party_address': 'Trainer_Party_Cerulean_City_Rocket_A',
        },
    ],
    'Pokemon Mansion 1F-SE': [
        {
            'level': 29,
            'party': ['Electrode', 'Weezing'],
            'party_address': 'Trainer_Party_Mansion_1F_Scientist_A',
        },
    ],
    'Silph Co 2F-SW': [
        {
            'level': 26,
            'party': ['Grimer', 'Weezing', 'Koffing', 'Weezing'],
            'party_address': 'Trainer_Party_Silph_Co_2F_Scientist_A',
        },
    ],
    'Silph Co 2F': [
        {
            'level': 28,
            'party': ['Magnemite', 'Voltorb', 'Magneton'],
            'party_address': 'Trainer_Party_Silph_Co_2F_Scientist_B',
        },
        {
            'level': 29,
            'party': ['Cubone', 'Zubat'],
            'party_address': 'Trainer_Party_Silph_Co_2F_Rocket_A',
        },
        {
            'level': 25,
            'party': ['Golbat', 'Zubat', 'Zubat', 'Raticate', 'Zubat'],
            'party_address': 'Trainer_Party_Silph_Co_2F_Rocket_B',
        },
    ],
    'Silph Co 3F-W': [
        {
            'level': 29,
            'party': ['Electrode', 'Weezing'],
            'party_address': 'Trainer_Party_Silph_Co_3F_Scientist_A',
        },
    ],
    'Silph Co 3F': [
        {
            'level': 28,
            'party': ['Raticate', 'Hypno', 'Raticate'],
            'party_address': 'Trainer_Party_Silph_Co_3F_Rocket_A',
        },
    ],
    'Silph Co 4F-N': [
        {
            'level': 33,
            'party': ['Electrode'],
            'party_address': 'Trainer_Party_Silph_Co_4F_Scientist_A',
        },
    ],
    'Silph Co 4F': [
        {
            'level': 29,
            'party': ['Machop', 'Drowzee'],
            'party_address': 'Trainer_Party_Silph_Co_4F_Rocket_A',
        },
        {
            'level': 28,
            'party': ['Ekans', 'Zubat', 'Cubone'],
            'party_address': 'Trainer_Party_Silph_Co_4F_Rocket_B',
        },
    ],
    'Silph Co 6F': [
        {
            'level': 25,
            'party': ['Voltorb', 'Koffing', 'Magneton', 'Magnemite', 'Koffing'],
            'party_address': 'Trainer_Party_Silph_Co_6F_Scientist_A',
        },
        {
            'level': 29,
            'party': ['Machop', 'Machoke'],
            'party_address': 'Trainer_Party_Silph_Co_6F_Rocket_A',
        },
        {
            'level': 28,
            'party': ['Zubat', 'Zubat', 'Golbat'],
            'party_address': 'Trainer_Party_Silph_Co_6F_Rocket_B',
        },
    ],
    'Silph Co 7F': [
        {
            'level': 29,
            'party': ['Electrode', 'Muk'],
            'party_address': 'Trainer_Party_Silph_Co_7F_Scientist_A',
        },
        {
            'level': 26,
            'party': ['Raticate', 'Arbok', 'Koffing', 'Golbat'],
            'party_address': 'Trainer_Party_Silph_Co_7F_Rocket_A',
        },
        {
            'level': 29,
            'party': ['Cubone', 'Cubone'],
            'party_address': 'Trainer_Party_Silph_Co_7F_Rocket_B',
        },
    ],
    'Silph Co 7F-SE': [
        {
            'level': 29,
            'party': ['Sandshrew', 'Sandslash'],
            'party_address': 'Trainer_Party_Silph_Co_7F_Rocket_C',
        },
    ],
    'Silph Co 8F': [
        {
            'level': 29,
            'party': ['Grimer', 'Electrode'],
            'party_address': 'Trainer_Party_Silph_Co_8F_Scientist_A',
        },
        {
            'level': 26,
            'party': ['Raticate', 'Zubat', 'Golbat', 'Rattata'],
            'party_address': 'Trainer_Party_Silph_Co_8F_Rocket_A',
        },
        {
            'level': 28,
            'party': ['Weezing', 'Golbat', 'Koffing'],
            'party_address': 'Trainer_Party_Silph_Co_8F_Rocket_B',
        },
    ],
    'Silph Co 9F': [
        {
            'level': 28,
            'party': ['Voltorb', 'Koffing', 'Magneton'],
            'party_address': 'Trainer_Party_Silph_Co_9F_Scientist_A',
        },
        {
            'level': 28,
            'party': ['Golbat', 'Drowzee', 'Hypno'],
            'party_address': 'Trainer_Party_Silph_Co_9F_Rocket_B',
        },
    ],
    'Silph Co 9F-NW': [
        {
            'level': 28,
            'party': ['Drowzee', 'Grimer', 'Machop'],
            'party_address': 'Trainer_Party_Silph_Co_9F_Rocket_A',
        },
    ],
    'Silph Co 10F': [
        {
            'level': 29,
            'party': ['Magnemite', 'Koffing'],
            'party_address': 'Trainer_Party_Silph_Co_10F_Scientist_A',
        },
        {
            'level': 33,
            'party': ['Machoke'],
            'party_address': 'Trainer_Party_Silph_Co_10F_Rocket_A',
        },
    ],
    'Rocket Hideout B4F': [
        {
            'level': 23,
            'party': ['Sandshrew', 'Ekans', 'Sandslash'],
            'party_address': 'Trainer_Party_Rocket_Hideout_B4F_Rocket_A',
        },
        {
            'level': 23,
            'party': ['Ekans', 'Sandshrew', 'Arbok'],
            'party_address': 'Trainer_Party_Rocket_Hideout_B4F_Rocket_B',
        },
    ],
    'Rocket Hideout B4F-NW': [
        {
            'level': 21,
            'party': ['Koffing', 'Zubat'],
            'party_address': 'Trainer_Party_Rocket_Hideout_B4F_Rocket_C',
        },
    ],
    'Silph Co 11F': [
        {
            'level': 25,
            'party': ['Rattata', 'Rattata', 'Zubat', 'Rattata', 'Ekans'],
            'party_address': 'Trainer_Party_Silph_Co_11F_Rocket_A',
        },
    ],
    'Silph Co 11F-W': [
        {
            'level': 32,
            'party': ['Cubone', 'Drowzee', 'Marowak'],
            'party_address': 'Trainer_Party_Silph_Co_11F_Rocket_B',
        },
    ],
    'Celadon Game Corner': [
        {
            'level': 20,
            'party': ['Raticate', 'Zubat'],
            'party_address': 'Trainer_Party_Game_Corner_Rocket_A',
        },
    ],
    'Rocket Hideout B1F': [
        {
            'level': 21,
            'party': ['Drowzee', 'Machop'],
            'party_address': 'Trainer_Party_Rocket_Hideout_B1F_Rocket_A',
        },
        {
            'level': 21,
            'party': ['Raticate', 'Raticate'],
            'party_address': 'Trainer_Party_Rocket_Hideout_B1F_Rocket_B',
        },
    ],
    'Rocket Hideout B1F-S': [
        {
            'level': 20,
            'party': ['Grimer', 'Koffing', 'Koffing'],
            'party_address': 'Trainer_Party_Rocket_Hideout_B1F_Rocket_C',
        },
        {
            'level': 19,
            'party': ['Rattata', 'Raticate', 'Raticate', 'Rattata'],
            'party_address': 'Trainer_Party_Rocket_Hideout_B1F_Rocket_D',
        },
    ],
    'Rocket Hideout B1F-SE': [
        {
            'level': 22,
            'party': ['Grimer', 'Koffing'],
            'party_address': 'Trainer_Party_Rocket_Hideout_B1F_Rocket_E',
        },
    ],
    'Rocket Hideout B2F': [
        {
            'level': 17,
            'party': ['Zubat', 'Koffing', 'Grimer', 'Zubat', 'Raticate'],
            'party_address': 'Trainer_Party_Rocket_Hideout_B2F_Rocket_A',
        },
    ],
    'Rocket Hideout B3F': [
        {
            'level': 20,
            'party': ['Rattata', 'Raticate', 'Drowzee'],
            'party_address': 'Trainer_Party_Rocket_Hideout_B3F_Rocket_A',
        },
        {
            'level': 21,
            'party': ['Machop', 'Machop'],
            'party_address': 'Trainer_Party_Rocket_Hideout_B3F_Rocket_B',
        },
    ],
    'Pokemon Tower 7F': [
        {
            'level': 25,
            'party': ['Zubat', 'Zubat', 'Golbat'],
            'party_address': 'Trainer_Party_Pokemon_Tower_7F_Rocket_A',
        },
        {
            'level': 26,
            'party': ['Koffing', 'Drowzee'],
            'party_address': 'Trainer_Party_Pokemon_Tower_7F_Rocket_B',
        },
        {
            'level': 23,
            'party': ['Zubat', 'Rattata', 'Raticate', 'Zubat'],
            'party_address': 'Trainer_Party_Pokemon_Tower_7F_Rocket_C',
        },
    ],
    'Victory Road 3F': [
        {
            'level': 43,
            'party': ['Exeggutor', 'Cloyster', 'Arcanine'],
            'party_address': 'Trainer_Party_Victory_Road_3F_CooltrainerM_A',
        },
        {
            'level': 43,
            'party': ['Parasect', 'Dewgong', 'Chansey'],
            'party_address': 'Trainer_Party_Victory_Road_3F_CooltrainerF_B',
        },
    ],
    'Victory Road 3F-S': [
        {
            'level': 43,
            'party': ['Kingler', 'Tentacruel', 'Blastoise'],
            'party_address': 'Trainer_Party_Victory_Road_3F_CooltrainerM_B',
        },
        {
            'level': 43,
            'party': ['Bellsprout', 'Weepinbell', 'Victreebel'],
            'party_address': 'Trainer_Party_Victory_Road_3F_CooltrainerF_A',
        },
    ],
    'Victory Road 1F': [
        {
            'level': 42,
            'party': ['Ivysaur', 'Wartortle', 'Charmeleon', 'Charizard'],
            'party_address': 'Trainer_Party_Victory_Road_1F_CooltrainerM_A',
        },
        {
            'level': 44,
            'party': ['Persian', 'Ninetales'],
            'party_address': 'Trainer_Party_Victory_Road_1F_CooltrainerF_A',
        },
    ],
    "Indigo Plateau Bruno's Room": [
        {
            'level': [53, 55, 55, 56, 58],
            'party': ['Onix', 'Hitmonchan', 'Hitmonlee', 'Onix', 'Machamp'],
            'party_address': 'Trainer_Party_Bruno_A',
        },
    ],
    "Indigo Plateau Lorelei's Room": [
        {
            'level': [54, 53, 54, 56, 56],
            'party': ['Dewgong', 'Cloyster', 'Slowbro', 'Jynx', 'Lapras'],
            'party_address': 'Trainer_Party_Lorelei_A',
        },
    ],
    "Indigo Plateau Agatha's Room": [
        {
            'level': [56, 56, 55, 58, 60],
            'party': ['Gengar', 'Golbat', 'Haunter', 'Arbok', 'Gengar'],
            'party_address': 'Trainer_Party_Agatha_A',
        },
    ],
    "Indigo Plateau Lance's Room": [
        {
            'level': [58, 56, 56, 60, 62],
            'party': ['Gyarados', 'Dragonair', 'Dragonair', 'Aerodactyl', 'Dragonite'],
            'party_address': 'Trainer_Party_Lance_A',
        },
    ],
    'Pokemon Tower 3F': [
        {
            'level': 23,
            'party': ['Gastly'],
            'party_address': 'Trainer_Party_Pokemon_Tower_3F_Channeler_A',
        },
        {
            'level': 24,
            'party': ['Gastly'],
            'party_address': 'Trainer_Party_Pokemon_Tower_3F_Channeler_B',
        },
        {
            'level': 22,
            'party': ['Gastly'],
            'party_address': 'Trainer_Party_Pokemon_Tower_3F_Channeler_D',
        },
    ],
    'Pokemon Tower 4F': [
        {
            'level': 24,
            'party': ['Gastly'],
            'party_address': 'Trainer_Party_Pokemon_Tower_4F_Channeler_A',
        },
        {
            'level': 23,
            'party': ['Gastly', 'Gastly'],
            'party_address': 'Trainer_Party_Pokemon_Tower_4F_Channeler_B',
        },
        {
            'level': 22,
            'party': ['Gastly'],
            'party_address': 'Trainer_Party_Pokemon_Tower_4F_Channeler_D',
        },
    ],
    'Pokemon Tower 5F': [
        {
            'level': 23,
            'party': ['Haunter'],
            'party_address': 'Trainer_Party_Pokemon_Tower_5F_Channeler_A',
        },
        {
            'level': 22,
            'party': ['Gastly'],
            'party_address': 'Trainer_Party_Pokemon_Tower_5F_Channeler_C',
        },
        {
            'level': 24,
            'party': ['Gastly'],
            'party_address': 'Trainer_Party_Pokemon_Tower_5F_Channeler_D',
        },
        {
            'level': 22,
            'party': ['Haunter'],
            'party_address': 'Trainer_Party_Pokemon_Tower_5F_Channeler_E',
        },
    ],
    'Pokemon Tower 6F': [
        {
            'level': 22,
            'party': ['Gastly', 'Gastly', 'Gastly'],
            'party_address': 'Trainer_Party_Pokemon_Tower_6F_Channeler_A',
        },
        {
            'level': 24,
            'party': ['Gastly'],
            'party_address': 'Trainer_Party_Pokemon_Tower_6F_Channeler_B',
        },
        {
            'level': 24,
            'party': ['Gastly'],
            'party_address': 'Trainer_Party_Pokemon_Tower_6F_Channeler_C',
        },
    ],
}


_trainer_data_rb = {
    'Viridian Forest': [
        {
            'level': 6,
            'party': ['Weedle', 'Caterpie'],
            'party_address': 'Trainer_Party_Viridian_Forest_BugCatcher_A',
        },
        {
            'level': 7,
            'party': ['Weedle', 'Kakuna', 'Weedle'],
            'party_address': 'Trainer_Party_Viridian_Forest_BugCatcher_B',
        },
        {
            'level': 9,
            'party': ['Weedle'],
            'party_address': 'Trainer_Party_Viridian_Forest_BugCatcher_C',
        },
    ],
    'Route 6': [
        {
            'level': 16,
            'party': ['Rattata', 'Pikachu'],
            'party_address': 'Trainer_Party_Route_6_JrTrainerF_A',
        },
    ],
    'S.S. Anne 2F Rooms-Gentleman and Lass Room': [
        {
            'level': 18,
            'party': ['Rattata', 'Pikachu'],
            'party_address': 'Trainer_Party_SS_Anne_2F_Rooms_Lass_A',
        },
    ],
    'S.S. Anne 2F Rooms-Fisherman and Gentleman Room': [
        {
            'level': 23,
            'party': ['Pikachu'],
            'party_address': 'Trainer_Party_SS_Anne_2F_Rooms_Gentleman_A',
        },
    ],
    'Route 8': [
        {
            'level': 19,
            'party': ['Pidgey', 'Rattata', 'Nidoran M', 'Meowth', 'Pikachu'],
            'party_address': 'Trainer_Party_Route_8_Lass_C',
        },
    ],
    'Celadon Gym-C': [
        {
            'level': [29, 24, 29],
            'party': ['Victreebel', 'Tangela', 'Vileplume'],
            'party_address': 'Trainer_Party_Erika_A',
        },
    ],
    'Vermilion Gym': [
        {
            'level': 21,
            'party': ['Pikachu', 'Pikachu'],
            'party_address': 'Trainer_Party_Vermilion_Gym_Sailor_A',
        },
        {
            'level': 20,
            'party': ['Voltorb', 'Magnemite', 'Voltorb'],
            'party_address': 'Trainer_Party_Vermilion_Gym_Rocker_A',
        },
        {
            'level': 23,
            'party': ['Pikachu'],
            'party_address': 'Trainer_Party_Vermilion_Gym_Gentleman_A',
        },
        {
            'level': [21, 18, 24],
            'party': ['Voltorb', 'Pikachu', 'Raichu'],
            'party_address': 'Trainer_Party_LtSurge_A',
        },
    ],
    'Pewter Gym': [
        {
            'level': 11,
            'party': ['Diglett', 'Sandshrew'],
            'party_address': 'Trainer_Party_Pewter_Gym_JrTrainerM_A',
        },
        {
            'level': [12, 14],
            'party': ['Geodude', 'Onix'],
            'party_address': 'Trainer_Party_Brock_A',
        },
    ],
    'Route 10-N': [
        {
            'level': 20,
            'party': ['Pikachu', 'Clefairy'],
            'party_address': 'Trainer_Party_Route_10_JrTrainerF_A',
        },
    ],
    'Route 13-E': [
        {
            'level': 24,
            'party': ['Pidgey', 'Meowth', 'Rattata', 'Pikachu', 'Meowth'],
            'party_address': 'Trainer_Party_Route_13_JrTrainerF_A',
        },
    ],
    'Route 13': [
        {
            'level': 27,
            'party': ['Rattata', 'Pikachu', 'Rattata'],
            'party_address': 'Trainer_Party_Route_13_Beauty_A',
        },
    ],
    'Route 15': [
        {
            'level': 29,
            'party': ['Pikachu', 'Raichu'],
            'party_address': 'Trainer_Party_Route_15_JrTrainerF_B',
        },
    ],
    'Cinnabar Gym': [
        {
            'level': [42, 40, 42, 47],
            'party': ['Growlithe', 'Ponyta', 'Rapidash', 'Arcanine'],
            'party_address': 'Trainer_Party_Blaine_A',
        },
    ],
    'Saffron Gym-C': [
        {
            'level': [38, 37, 38, 43],
            'party': ['Kadabra', 'Mr Mime', 'Venomoth', 'Alakazam'],
            'party_address': 'Trainer_Party_Sabrina_A',
        },
    ],
    'Fuchsia Gym': [
        {
            'level': [37, 39, 37, 43],
            'party': ['Koffing', 'Muk', 'Koffing', 'Weezing'],
            'party_address': 'Trainer_Party_Koga_A',
        },
    ],
    'Viridian Gym': [
        {
            'level': [45, 42, 44, 45, 50],
            'party': ['Rhyhorn', 'Dugtrio', 'Nidoqueen', 'Nidoking', 'Rhydon'],
            'party_address': 'Trainer_Party_Viridian_Gym_Giovanni_A',
        },
    ],
    "Oak's Lab": [
        {
            'level': 5,
            'party': [
                ['Squirtle'],
                ['Bulbasaur'],
                ['Charmander'],
            ],
            'party_address': [
                'Trainer_Party_Pallet_Town_Green1_A',
                'Trainer_Party_Pallet_Town_Green1_B',
                'Trainer_Party_Pallet_Town_Green1_C',
            ],
        },
    ],
    'Route 22': [
        {
            'level': [9, 8],
            'party': [
                ['Pidgey', 'Squirtle'],
                ['Pidgey', 'Bulbasaur'],
                ['Pidgey', 'Charmander'],
            ],
            'party_address': [
                'Trainer_Party_Route_22_Green1_A',
                'Trainer_Party_Route_22_Green1_B',
                'Trainer_Party_Route_22_Green1_C',
            ],
        },
    ],
    'Route 22-F': [
        {
            'level': [47, 45, 45, 47, 50, 53],
            'party': [
                ['Pidgeot', 'Rhyhorn', 'Growlithe', 'Exeggcute', 'Alakazam', 'Blastoise'],
                ['Pidgeot', 'Rhyhorn', 'Gyarados', 'Growlithe', 'Alakazam', 'Venusaur'],
                ['Pidgeot', 'Rhyhorn', 'Exeggcute', 'Gyarados', 'Alakazam', 'Charizard'],
            ],
            'party_address': [
                'Trainer_Party_Route_22_Green2_A',
                'Trainer_Party_Route_22_Green2_B',
                'Trainer_Party_Route_22_Green2_C',
            ],
        },
    ],
    'Cerulean City': [
        {
            'level': [18, 15, 15, 17],
            'party': [
                ['Pidgeotto', 'Abra', 'Rattata', 'Squirtle'],
                ['Pidgeotto', 'Abra', 'Rattata', 'Bulbasaur'],
                ['Pidgeotto', 'Abra', 'Rattata', 'Charmander'],
            ],
            'party_address': [
                'Trainer_Party_Cerulean_City_Green1_A',
                'Trainer_Party_Cerulean_City_Green1_B',
                'Trainer_Party_Cerulean_City_Green1_C',
            ],
        },
    ],
    'Silph Co 7F-NW': [
        {
            'level': [37, 38, 35, 35, 40],
            'party': [
                ['Pidgeot', 'Growlithe', 'Exeggcute', 'Alakazam', 'Blastoise'],
                ['Pidgeot', 'Gyarados', 'Growlithe', 'Alakazam', 'Venusaur'],
                ['Pidgeot', 'Exeggcute', 'Gyarados', 'Alakazam', 'Charizard'],
            ],
            'party_address': [
                'Trainer_Party_Silph_Co_7F_Green2_A',
                'Trainer_Party_Silph_Co_7F_Green2_B',
                'Trainer_Party_Silph_Co_7F_Green2_C',
            ],
        },
    ],
    'Rocket Hideout B4F': [
        {
            'level': [25, 24, 29],
            'party': ['Onix', 'Rhyhorn', 'Kangaskhan'],
            'party_address': 'Trainer_Party_Rocket_Hideout_B4F_Giovanni_A',
        },
    ],
    'Silph Co 11F-C': [
        {
            'level': [37, 35, 37, 41],
            'party': ['Nidorino', 'Kangaskhan', 'Rhyhorn', 'Nidoqueen'],
            'party_address': 'Trainer_Party_Silph_Co_11F_Giovanni_A',
        },
    ],
    'S.S. Anne 2F': [
        {
            'level': [19, 16, 18, 20],
            'party': [
                ['Pidgeotto', 'Raticate', 'Kadabra', 'Wartortle'],
                ['Pidgeotto', 'Raticate', 'Kadabra', 'Ivysaur'],
                ['Pidgeotto', 'Raticate', 'Kadabra', 'Charmeleon'],
            ],
            'party_address': [
                'Trainer_Party_SS_Anne_2F_Green2_A',
                'Trainer_Party_SS_Anne_2F_Green2_B',
                'Trainer_Party_SS_Anne_2F_Green2_C',
            ],
        },
    ],
    'Pokemon Tower 2F': [
        {
            'level': [25, 23, 22, 20, 25],
            'party': [
                ['Pidgeotto', 'Growlithe', 'Exeggcute', 'Kadabra', 'Wartortle'],
                ['Pidgeotto', 'Gyarados', 'Growlithe', 'Kadabra', 'Ivysaur'],
                ['Pidgeotto', 'Exeggcute', 'Gyarados', 'Kadabra', 'Charmeleon'],
            ],
            'party_address': [
                'Trainer_Party_Pokemon_Tower_2F_Green2_A',
                'Trainer_Party_Pokemon_Tower_2F_Green2_B',
                'Trainer_Party_Pokemon_Tower_2F_Green2_C',
            ],
        },
    ],
    "Indigo Plateau Champion's Room": [
        {
            'level': [61, 59, 61, 61, 63, 65],
            'party': [
                ['Pidgeot', 'Alakazam', 'Rhydon', 'Arcanine', 'Exeggutor', 'Blastoise'],
                ['Pidgeot', 'Alakazam', 'Rhydon', 'Gyarados', 'Arcanine', 'Venusaur'],
                ['Pidgeot', 'Alakazam', 'Rhydon', 'Exeggutor', 'Gyarados', 'Charizard'],
            ],
            'party_address': [
                'Trainer_Party_Indigo_Plateau_Green3_A',
                'Trainer_Party_Indigo_Plateau_Green3_B',
                'Trainer_Party_Indigo_Plateau_Green3_C',
            ],
        },
    ],
}


_trainer_data_yellow = {
    'Viridian Forest': [
        {
            'level': 7,
            'party': ['Caterpie', 'Caterpie'],
            'party_address': 'Trainer_Party_Viridian_Forest_BugCatcher_A',
        },
        {
            'level': 6,
            'party': ['Metapod', 'Caterpie', 'Metapod'],
            'party_address': 'Trainer_Party_Viridian_Forest_BugCatcher_B',
        },
        {
            'level': 10,
            'party': ['Caterpie'],
            'party_address': 'Trainer_Party_Viridian_Forest_BugCatcher_C',
        },
        {
            'level': 6,
            'party': ['Nidoran F', 'Nidoran M'],
            'party_address': 'Trainer_Party_Viridian_Forest_Lass_A',
        },
        {
            'level': 8,
            'party': ['Caterpie', 'Metapod'],
            'party_address': 'Trainer_Party_Viridian_Forest_BugCatcher_D',
        },
    ],
    'S.S. Anne 2F Rooms-Gentleman and Lass Room': [
        {
            'level': 20,
            'party': ['Jigglypuff'],
            'party_address': 'Trainer_Party_SS_Anne_2F_Rooms_Lass_A',
        },
    ],
    'Route 8': [
        {
            'level': 19,
            'party': ['Pidgey', 'Rattata', 'Nidoran F', 'Meowth', 'Nidoran M'],
            'party_address': 'Trainer_Party_Route_8_Lass_C',
        },
    ],
    'Vermilion Gym': [
        {
            'level': 24,
            'party': ['Magnemite'],
            'party_address': 'Trainer_Party_Vermilion_Gym_Sailor_A',
        },
        {
            'level': 20,
            'party': ['Voltorb', 'Voltorb', 'Voltorb'],
            'party_address': 'Trainer_Party_Vermilion_Gym_Rocker_A',
        },
        {
            'level': [28],
            'party': ['Raichu'],
            'party_address': 'Trainer_Party_LtSurge_A',
        },
        {
            'level': 22,
            'party': ['Voltorb', 'Magnemite'],
            'party_address': 'Trainer_Party_Vermilion_Gym_Gentleman_A',
        },
    ],
    'Pewter Gym': [
        {
            'level': 9,
            'party': ['Diglett', 'Sandshrew'],
            'party_address': 'Trainer_Party_Pewter_Gym_JrTrainerM_A',
        },
        {
            'level': [10, 12],
            'party': ['Geodude', 'Onix'],
            'party_address': 'Trainer_Party_Brock_A',
        },
    ],
    'Route 6': [
        {
            'level': 16,
            'party': ['Oddish', 'Bellsprout'],
            'party_address': 'Trainer_Party_Route_6_JrTrainerF_A',
        },
    ],
    'Route 10-N': [
        {
            'level': 20,
            'party': ['Jigglypuff', 'Clefairy'],
            'party_address': 'Trainer_Party_Route_10_JrTrainerF_A',
        },
    ],
    'Route 13-E': [
        {
            'level': 24,
            'party': ['Pidgey', 'Meowth', 'Rattata', 'Pidgey', 'Meowth'],
            'party_address': 'Trainer_Party_Route_13_JrTrainerF_A',
        },
    ],
    'Route 15': [
        {
            'level': 29,
            'party': ['Pidgey', 'Pidgeotto'],
            'party_address': 'Trainer_Party_Route_15_JrTrainerF_B',
        },
    ],
    'Route 13': [
        {
            'level': 27,
            'party': ['Rattata', 'Vulpix', 'Rattata'],
            'party_address': 'Trainer_Party_Route_13_Beauty_A',
        },
    ],
    'Rocket Hideout B4F': [
        {
            'level': [25, 24, 29],
            'party': ['Onix', 'Rhyhorn', 'Persian'],
            'party_address': 'Trainer_Party_Rocket_Hideout_B4F_Giovanni_A',
        },
        {
            'level': 27,
            'party': ['Meowth', 'Arbok', 'Weezing'],
            'party_address': 'Trainer_Party_Rocket_Hideout_B4F_Rocket_Jessie_James_A',
        },
    ],
    'Silph Co 11F-C': [
        {
            'level': [37, 35, 37, 41],
            'party': ['Nidorino', 'Persian', 'Rhyhorn', 'Nidoqueen'],
            'party_address': 'Trainer_Party_Silph_Co_11F_Giovanni_A',
        },
        {
            'level': 31,
            'party': ['Weezing', 'Arbok', 'Meowth'],
            'party_address': 'Trainer_Party_Silph_Co_11F_Rocket_Jessie_James_A',
        },
    ],
    'Viridian Gym': [
        {
            'level': [50, 53, 53, 55, 55],
            'party': ['Dugtrio', 'Persian', 'Nidoqueen', 'Nidoking', 'Rhydon'],
            'party_address': 'Trainer_Party_Viridian_Gym_Giovanni_A',
        },
    ],
    'Celadon Gym-C': [
        {
            'level': [30, 32, 32],
            'party': ['Tangela', 'Weepinbell', 'Gloom'],
            'party_address': 'Trainer_Party_Erika_A',
        },
    ],
    'Fuchsia Gym': [
        {
            'level': [44, 46, 48, 50],
            'party': ['Venonat', 'Venonat', 'Venonat', 'Venomoth'],
            'party_address': 'Trainer_Party_Koga_A',
        },
    ],
    'Cinnabar Gym': [
        {
            'level': [48, 50, 54],
            'party': ['Ninetales', 'Rapidash', 'Arcanine'],
            'party_address': 'Trainer_Party_Blaine_A',
        },
    ],
    'Saffron Gym-C': [
        {
            'level': [50, 50, 50],
            'party': ['Abra', 'Kadabra', 'Alakazam'],
            'party_address': 'Trainer_Party_Sabrina_A',
        },
    ],
    'S.S. Anne 2F Rooms-Fisherman and Gentleman Room': [
        {
            'level': 22,
            'party': ['Voltorb', 'Magnemite'],
            'party_address': 'Trainer_Party_SS_Anne_2F_Rooms_Gentleman_A',
        },
    ],
    "Oak's Lab": [
        {
            'level': 5,
            'party': ['Eevee'],
            'party_address': 'Trainer_Party_Oaks_Lab_Rival1_A',
        },
    ],
    'Route 22': [
        {
            'level': [9, 8],
            'party': ['Spearow', 'Eevee'],
            'party_address': 'Trainer_Party_Route_22_Rival1_A',
        },
    ],
    'Cerulean City': [
        {
            'level': [18, 15, 15, 17],
            'party': ['Spearow', 'Sandshrew', 'Rattata', 'Eevee'],
            'party_address': 'Trainer_Party_Cerulean_City_Rival1_A',
        },
    ],
    'Mt Moon B2F': [
        {
            'level': 14,
            'party': ['Ekans', 'Meowth', 'Koffing'],
            'party_address': 'Trainer_Party_Mt_Moon_B2F_Rocket_Jessie_James_A',
        },
    ],
    'Pokemon Tower 7F': [
        {
            'level': 25,
            'party': ['Koffing', 'Meowth', 'Ekans'],
            'party_address': 'Trainer_Party_Pokemon_Tower_7F_Rocket_Jessie_James_A',
        },
    ],
    'S.S. Anne 2F': [
        {
            'level': [19, 16, 18, 20],
            'party': ['Spearow', 'Rattata', 'Sandshrew', 'Eevee'],
            'party_address': 'Trainer_Party_SS_Anne_2F_Rival2_A',
        },
    ],
    'Pokemon Tower 2F': [
        {
            'level': [25, 23, 22, 20, 25],
            'party': [
                ['Fearow', 'Shellder', 'Vulpix', 'Sandshrew', 'Eevee'],
                ['Fearow', 'Magnemite', 'Shellder', 'Sandshrew', 'Eevee'],
                ['Fearow', 'Vulpix', 'Magnemite', 'Sandshrew', 'Eevee'],
            ],
            'party_address': [
                'Trainer_Party_Pokemon_Tower_2F_Rival2_Jolteon_A',
                'Trainer_Party_Pokemon_Tower_2F_Rival2_Flareon_A',
                'Trainer_Party_Pokemon_Tower_2F_Rival2_Vaporeon_A',
            ],
        },
    ],
    'Silph Co 7F-NW': [
        {
            'level': [38, 35, 37, 35, 40],
            'party': [
                ['Sandslash', 'Ninetales', 'Cloyster', 'Kadabra', 'Jolteon'],
                ['Sandslash', 'Cloyster', 'Magneton', 'Kadabra', 'Flareon'],
                ['Sandslash', 'Magneton', 'Ninetales', 'Kadabra', 'Vaporeon'],
            ],
            'party_address': [
                'Trainer_Party_Silph_Co_7F_Rival2_Jolteon_A',
                'Trainer_Party_Silph_Co_7F_Rival2_Flareon_A',
                'Trainer_Party_Silph_Co_7F_Rival2_Vaporeon_A',
            ],
        },
    ],
    'Route 22-F': [
        {
            'level': [47, 45, 45, 47, 50, 53],
            'party': [
                ['Sandslash', 'Exeggcute', 'Ninetales', 'Cloyster', 'Kadabra', 'Jolteon'],
                ['Sandslash', 'Exeggcute', 'Cloyster', 'Magneton', 'Kadabra', 'Flareon'],
                ['Sandslash', 'Exeggcute', 'Magneton', 'Ninetales', 'Kadabra', 'Vaporeon'],
            ],
            'party_address': [
                'Trainer_Party_Route_22_Rival2_Jolteon_A',
                'Trainer_Party_Route_22_Rival2_Flareon_A',
                'Trainer_Party_Route_22_Rival2_Vaporeon_A',
            ],
        },
    ],
    "Indigo Plateau Champion's Room": [
        {
            'level': [61, 59, 61, 61, 63, 65],
            'party': [
                ['Sandslash', 'Alakazam', 'Exeggutor', 'Cloyster', 'Ninetales', 'Jolteon'],
                ['Sandslash', 'Alakazam', 'Exeggutor', 'Magneton', 'Cloyster', 'Flareon'],
                ['Sandslash', 'Alakazam', 'Exeggutor', 'Ninetales', 'Magneton', 'Vaporeon'],
            ],
            'party_address': [
                'Trainer_Party_Indigo_Plateau_Rival3_Jolteon_A',
                'Trainer_Party_Indigo_Plateau_Rival3_Flareon_A',
                'Trainer_Party_Indigo_Plateau_Rival3_Vaporeon_A',
            ],
        },
    ],
}


_trainer_data_rb_order = {
    'Fossil Level': [
        'Fossil_Level',
    ],
    'Route 3': [
        'Trainer_Party_Route_3_Youngster_A',
        'Trainer_Party_Route_3_Youngster_B',
        'Trainer_Party_Route_3_BugCatcher_A',
        'Trainer_Party_Route_3_BugCatcher_B',
        'Trainer_Party_Route_3_BugCatcher_C',
        'Trainer_Party_Route_3_Lass_A',
        'Trainer_Party_Route_3_Lass_B',
        'Trainer_Party_Route_3_Lass_C',
    ],
    'Mt Moon 1F': [
        'Trainer_Party_Mt_Moon_1F_Youngster_A',
        'Trainer_Party_Mt_Moon_1F_BugCatcher_A',
        'Trainer_Party_Mt_Moon_1F_BugCatcher_B',
        'Trainer_Party_Mt_Moon_1F_Lass_A',
        'Trainer_Party_Mt_Moon_1F_Lass_B',
        'Trainer_Party_Mt_Moon_1F_SuperNerd_A',
        'Trainer_Party_Mt_Moon_1F_Hiker_A',
    ],
    'S.S. Anne 1F Rooms-Youngster and Lass Room': [
        'Trainer_Party_SS_Anne_1F_Rooms_Lass_A',
        'Trainer_Party_SS_Anne_1F_Rooms_Youngster_A',
    ],
    'S.S. Anne 1F Rooms-East Gentleman Room': [
        'Trainer_Party_SS_Anne_1F_Rooms_Gentleman_A',
    ],
    'S.S. Anne 1F Rooms-West Gentleman Room': [
        'Trainer_Party_SS_Anne_1F_Rooms_Gentleman_B',
    ],
    'Viridian Forest': [
        'Trainer_Party_Viridian_Forest_BugCatcher_A',
        'Trainer_Party_Viridian_Forest_BugCatcher_B',
        'Trainer_Party_Viridian_Forest_BugCatcher_C',
        'Trainer_Party_Viridian_Forest_Lass_A',
        'Trainer_Party_Viridian_Forest_BugCatcher_D',
    ],
    'Route 24': [
        'Trainer_Party_Route_24_BugCatcher_A',
        'Trainer_Party_Route_24_Lass_A',
        'Trainer_Party_Route_24_Lass_B',
        'Trainer_Party_Route_24_JrTrainerM_A',
        'Trainer_Party_Route_24_JrTrainerM_C',
        'Trainer_Party_Route_24_Rocket_A',
        'Trainer_Party_Route_24_Youngster_A',
    ],
    'Route 6': [
        'Trainer_Party_Route_6_BugCatcher_A',
        'Trainer_Party_Route_6_BugCatcher_B',
        'Trainer_Party_Route_6_JrTrainerM_A',
        'Trainer_Party_Route_6_JrTrainerM_B',
        'Trainer_Party_Route_6_JrTrainerF_A',
        'Trainer_Party_Route_6_JrTrainerF_B',
    ],
    'Route 9': [
        'Trainer_Party_Route_9_BugCatcher_A',
        'Trainer_Party_Route_9_BugCatcher_B',
        'Trainer_Party_Route_9_JrTrainerM_A',
        'Trainer_Party_Route_9_JrTrainerM_B',
        'Trainer_Party_Route_9_JrTrainerF_A',
        'Trainer_Party_Route_9_JrTrainerF_B',
        'Trainer_Party_Route_9_Hiker_A',
        'Trainer_Party_Route_9_Hiker_B',
        'Trainer_Party_Route_9_Hiker_D',
    ],
    'Route 4-Lass': [
        'Trainer_Party_Route_4_Lass_A',
    ],
    'Route 25': [
        'Trainer_Party_Route_25_Lass_A',
        'Trainer_Party_Route_25_Lass_B',
        'Trainer_Party_Route_25_JrTrainerM_A',
        'Trainer_Party_Route_25_Hiker_A',
        'Trainer_Party_Route_25_Hiker_B',
        'Trainer_Party_Route_25_Hiker_C',
        'Trainer_Party_Route_25_Youngster_A',
        'Trainer_Party_Route_25_Youngster_B',
        'Trainer_Party_Route_25_Youngster_C',
    ],
    'S.S. Anne 2F Rooms-Gentleman and Lass Room': [
        'Trainer_Party_SS_Anne_2F_Rooms_Lass_A',
        'Trainer_Party_SS_Anne_2F_Rooms_Gentleman_C',
    ],
    'S.S. Anne 2F Rooms-Fisherman and Gentleman Room': [
        'Trainer_Party_SS_Anne_2F_Rooms_Fisher_A',
        'Trainer_Party_SS_Anne_2F_Rooms_Gentleman_A',
    ],
    'Route 8': [
        'Trainer_Party_Route_8_Lass_A',
        'Trainer_Party_Route_8_Lass_B',
        'Trainer_Party_Route_8_Lass_C',
        'Trainer_Party_Route_8_Lass_D',
        'Trainer_Party_Route_8_SuperNerd_A',
        'Trainer_Party_Route_8_SuperNerd_B',
        'Trainer_Party_Route_8_SuperNerd_C',
        'Trainer_Party_Route_8_Gambler_A',
        'Trainer_Party_Route_8_Gambler_C',
    ],
    'Celadon Gym': [
        'Trainer_Party_Celadon_Gym_Lass_A',
        'Trainer_Party_Celadon_Gym_JrTrainerF_A',
        'Trainer_Party_Celadon_Gym_Beauty_A',
        'Trainer_Party_Celadon_Gym_Beauty_B',
    ],
    'Celadon Gym-C': [
        'Trainer_Party_Celadon_Gym_CooltrainerF_A',
        'Trainer_Party_Erika_A',
        'Trainer_Party_Celadon_Gym_Lass_B',
        'Trainer_Party_Celadon_Gym_Beauty_C',
    ],
    'S.S. Anne Bow': [
        'Trainer_Party_SS_Anne_Stern_Sailor_A',
        'Trainer_Party_SS_Anne_Stern_Sailor_B',
    ],
    'S.S. Anne B1F Rooms-Two Sailors Room': [
        'Trainer_Party_SS_Anne_B1F_Rooms_Sailor_A',
        'Trainer_Party_SS_Anne_B1F_Rooms_Sailor_B',
    ],
    'S.S. Anne B1F Rooms-East Single Sailor Room': [
        'Trainer_Party_SS_Anne_B1F_Rooms_Sailor_D',
    ],
    'S.S. Anne B1F Rooms-West Single Sailor Room': [
        'Trainer_Party_SS_Anne_B1F_Rooms_Sailor_C',
    ],
    'S.S. Anne B1F Rooms-Fisherman Room': [
        'Trainer_Party_SS_Anne_B1F_Rooms_Sailor_E',
        'Trainer_Party_SS_Anne_B1F_Rooms_Fisher_A',
    ],
    'Vermilion Gym': [
        'Trainer_Party_Vermilion_Gym_Sailor_A',
        'Trainer_Party_Vermilion_Gym_Rocker_A',
        'Trainer_Party_Vermilion_Gym_Gentleman_A',
        'Trainer_Party_LtSurge_A',
    ],
    'Pewter Gym': [
        'Trainer_Party_Pewter_Gym_JrTrainerM_A',
        'Trainer_Party_Brock_A',
    ],
    'Route 12-Grass': [
        'Trainer_Party_Route_12_Fisher_F',
    ],
    'Route 12-S': [
        'Trainer_Party_Route_12_JrTrainerM_A',
        'Trainer_Party_Route_12_Rocker_A',
    ],
    'Route 12-N': [
        'Trainer_Party_Route_12_Fisher_A',
        'Trainer_Party_Route_12_Fisher_B',
        'Trainer_Party_Route_12_Fisher_C',
        'Trainer_Party_Route_12_Fisher_D',
    ],
    'Cerulean Gym': [
        'Trainer_Party_Cerulean_Gym_JrTrainerF_A',
        'Trainer_Party_Cerulean_Gym_Swimmer_A',
        'Trainer_Party_Misty_A',
    ],
    'Route 10-N': [
        'Trainer_Party_Route_10_JrTrainerF_A',
    ],
    'Route 10-C': [
        'Trainer_Party_Route_10_Pokemaniac_A',
    ],
    'Route 10-S': [
        'Trainer_Party_Route_10_JrTrainerF_B',
        'Trainer_Party_Route_10_Pokemaniac_B',
        'Trainer_Party_Route_10_Hiker_A',
        'Trainer_Party_Route_10_Hiker_B',
    ],
    'Rock Tunnel B1F-W': [
        'Trainer_Party_Rock_Tunnel_B1F_JrTrainerF_A',
        'Trainer_Party_Rock_Tunnel_B1F_Pokemaniac_A',
        'Trainer_Party_Rock_Tunnel_B1F_Hiker_A',
    ],
    'Rock Tunnel B1F-E': [
        'Trainer_Party_Rock_Tunnel_B1F_JrTrainerF_B',
        'Trainer_Party_Rock_Tunnel_B1F_Pokemaniac_B',
        'Trainer_Party_Rock_Tunnel_B1F_Pokemaniac_C',
        'Trainer_Party_Rock_Tunnel_B1F_Hiker_B',
        'Trainer_Party_Rock_Tunnel_B1F_Hiker_D',
    ],
    'Route 13-E': [
        'Trainer_Party_Route_13_JrTrainerF_D',
        'Trainer_Party_Route_13_BirdKeeper_A',
        'Trainer_Party_Route_13_JrTrainerF_A',
    ],
    'Route 13': [
        'Trainer_Party_Route_13_JrTrainerF_B',
        'Trainer_Party_Route_13_JrTrainerF_C',
        'Trainer_Party_Route_13_Biker_A',
        'Trainer_Party_Route_13_Beauty_A',
        'Trainer_Party_Route_13_Beauty_B',
        'Trainer_Party_Route_13_BirdKeeper_B',
        'Trainer_Party_Route_13_BirdKeeper_C',
    ],
    'Route 20-E': [
        'Trainer_Party_Route_20_Swimmer_A',
        'Trainer_Party_Route_20_Swimmer_C',
        'Trainer_Party_Route_20_Beauty_E',
        'Trainer_Party_Route_20_Beauty_A',
    ],
    'Route 20-W': [
        'Trainer_Party_Route_20_JrTrainerF_A',
        'Trainer_Party_Route_20_JrTrainerF_C',
        'Trainer_Party_Route_20_Swimmer_B',
        'Trainer_Party_Route_20_Beauty_B',
        'Trainer_Party_Route_20_Beauty_C',
        'Trainer_Party_Route_20_BirdKeeper_A',
    ],
    'Rock Tunnel 1F-S': [
        'Trainer_Party_Rock_Tunnel_1F_JrTrainerF_A',
        'Trainer_Party_Rock_Tunnel_1F_JrTrainerF_B',
        'Trainer_Party_Rock_Tunnel_1F_JrTrainerF_C',
    ],
    'Rock Tunnel 1F-NE': [
        'Trainer_Party_Rock_Tunnel_1F_Pokemaniac_A',
    ],
    'Rock Tunnel 1F-NW': [
        'Trainer_Party_Rock_Tunnel_1F_Hiker_A',
        'Trainer_Party_Rock_Tunnel_1F_Hiker_B',
        'Trainer_Party_Rock_Tunnel_1F_Hiker_C',
    ],
    'Route 15-N': [
        'Trainer_Party_Route_15_JrTrainerF_C',
    ],
    'Route 15': [
        'Trainer_Party_Route_15_JrTrainerF_A',
        'Trainer_Party_Route_15_JrTrainerF_B',
        'Trainer_Party_Route_15_JrTrainerF_D',
        'Trainer_Party_Route_15_Biker_A',
        'Trainer_Party_Route_15_Biker_B',
        'Trainer_Party_Route_15_Beauty_A',
        'Trainer_Party_Route_15_Beauty_B',
        'Trainer_Party_Route_15_BirdKeeper_A',
        'Trainer_Party_Route_15_BirdKeeper_B',
    ],
    'Victory Road 2F-NW': [
        'Trainer_Party_Victory_Road_2F_Pokemaniac_A',
    ],
    'Victory Road 2F-C': [
        'Trainer_Party_Victory_Road_2F_Juggler_A',
        'Trainer_Party_Victory_Road_2F_Juggler_C',
        'Trainer_Party_Victory_Road_2F_Tamer_A',
        'Trainer_Party_Victory_Road_2F_Blackbelt_A',
    ],
    'Mt Moon B2F': [
        'Trainer_Party_Mt_Moon_B2F_SuperNerd_A',
        'Trainer_Party_Mt_Moon_B2F_Rocket_A',
        'Trainer_Party_Mt_Moon_B2F_Rocket_D',
    ],
    'Mt Moon B2F-NE': [
        'Trainer_Party_Mt_Moon_B2F_Rocket_C',
    ],
    'Mt Moon B2F-C': [
        'Trainer_Party_Mt_Moon_B2F_Rocket_B',
    ],
    'Cinnabar Gym': [
        'Trainer_Party_Cinnabar_Gym_SuperNerd_A',
        'Trainer_Party_Cinnabar_Gym_SuperNerd_B',
        'Trainer_Party_Cinnabar_Gym_SuperNerd_C',
        'Trainer_Party_Cinnabar_Gym_SuperNerd_D',
        'Trainer_Party_Cinnabar_Gym_Burglar_A',
        'Trainer_Party_Cinnabar_Gym_Burglar_B',
        'Trainer_Party_Cinnabar_Gym_Burglar_C',
        'Trainer_Party_Blaine_A',
    ],
    'Route 14': [
        'Trainer_Party_Route_14_Biker_A',
        'Trainer_Party_Route_14_Biker_C',
        'Trainer_Party_Route_14_Biker_D',
        'Trainer_Party_Route_14_Biker_E',
        'Trainer_Party_Route_14_BirdKeeper_A',
        'Trainer_Party_Route_14_BirdKeeper_B',
        'Trainer_Party_Route_14_BirdKeeper_D',
        'Trainer_Party_Route_14_BirdKeeper_E',
        'Trainer_Party_Route_14_BirdKeeper_F',
        'Trainer_Party_Route_14_BirdKeeper_G',
    ],
    'Route 16-SW': [
        'Trainer_Party_Route_16_Biker_A',
        'Trainer_Party_Route_16_Biker_B',
        'Trainer_Party_Route_16_Biker_C',
        'Trainer_Party_Route_16_CueBall_A',
        'Trainer_Party_Route_16_CueBall_B',
        'Trainer_Party_Route_16_CueBall_C',
    ],
    'Route 17': [
        'Trainer_Party_Route_17_Biker_A',
        'Trainer_Party_Route_17_Biker_B',
        'Trainer_Party_Route_17_Biker_C',
        'Trainer_Party_Route_17_Biker_D',
        'Trainer_Party_Route_17_Biker_E',
        'Trainer_Party_Route_17_CueBall_A',
        'Trainer_Party_Route_17_CueBall_B',
        'Trainer_Party_Route_17_CueBall_C',
        'Trainer_Party_Route_17_CueBall_D',
        'Trainer_Party_Route_17_CueBall_E',
    ],
    'Pokemon Mansion 2F': [
        'Trainer_Party_Mansion_2F_Burglar_A',
    ],
    'Pokemon Mansion 3F-SW': [
        'Trainer_Party_Mansion_3F_Burglar_A',
    ],
    'Pokemon Mansion 3F-SE': [
        'Trainer_Party_Mansion_3F_Scientist_A',
    ],
    'Pokemon Mansion B1F': [
        'Trainer_Party_Mansion_B1F_Burglar_A',
        'Trainer_Party_Mansion_B1F_Scientist_A',
    ],
    'Route 11': [
        'Trainer_Party_Route_11_Engineer_A',
        'Trainer_Party_Route_11_Engineer_B',
        'Trainer_Party_Route_11_Gambler_A',
        'Trainer_Party_Route_11_Gambler_B',
        'Trainer_Party_Route_11_Gambler_C',
        'Trainer_Party_Route_11_Gambler_D',
        'Trainer_Party_Route_11_Youngster_A',
        'Trainer_Party_Route_11_Youngster_B',
        'Trainer_Party_Route_11_Youngster_C',
        'Trainer_Party_Route_11_Youngster_D',
    ],
    'Route 21': [
        'Trainer_Party_Route_21_Fisher_A',
        'Trainer_Party_Route_21_Fisher_B',
        'Trainer_Party_Route_21_Fisher_C',
        'Trainer_Party_Route_21_Fisher_D',
        'Trainer_Party_Route_21_Swimmer_A',
        'Trainer_Party_Route_21_Swimmer_B',
        'Trainer_Party_Route_21_Swimmer_C',
        'Trainer_Party_Route_21_Swimmer_D',
        'Trainer_Party_Route_21_CueBall_A',
    ],
    'Route 19-N': [
        'Trainer_Party_Route_19_Swimmer_A',
        'Trainer_Party_Route_19_Swimmer_B',
    ],
    'Route 19-S': [
        'Trainer_Party_Route_19_Swimmer_C',
        'Trainer_Party_Route_19_Swimmer_D',
        'Trainer_Party_Route_19_Swimmer_E',
        'Trainer_Party_Route_19_Swimmer_F',
        'Trainer_Party_Route_19_Swimmer_G',
        'Trainer_Party_Route_19_Beauty_A',
        'Trainer_Party_Route_19_Beauty_B',
        'Trainer_Party_Route_19_Beauty_C',
    ],
    'Saffron Gym-C': [
        'Trainer_Party_Sabrina_A',
    ],
    'Saffron Gym-NE': [
        'Trainer_Party_Saffron_Gym_Psychic_A',
    ],
    'Saffron Gym-E': [
        'Trainer_Party_Saffron_Gym_Psychic_B',
    ],
    'Saffron Gym-SE': [
        'Trainer_Party_Saffron_Gym_Psychic_C',
    ],
    'Saffron Gym-NW': [
        'Trainer_Party_Saffron_Gym_Psychic_D',
    ],
    'Saffron Gym-N': [
        'Trainer_Party_Saffron_Gym_Channeler_A',
    ],
    'Saffron Gym-W': [
        'Trainer_Party_Saffron_Gym_Channeler_B',
    ],
    'Saffron Gym-SW': [
        'Trainer_Party_Saffron_Gym_Channeler_C',
    ],
    'Silph Co 5F': [
        'Trainer_Party_Silph_Co_5F_Juggler_A',
        'Trainer_Party_Silph_Co_5F_Scientist_A',
        'Trainer_Party_Silph_Co_5F_Rocket_A',
        'Trainer_Party_Silph_Co_5F_Rocket_B',
    ],
    'Fuchsia Gym': [
        'Trainer_Party_Fuchsia_Gym_Juggler_A',
        'Trainer_Party_Fuchsia_Gym_Juggler_B',
        'Trainer_Party_Fuchsia_Gym_Juggler_D',
        'Trainer_Party_Fuchsia_Gym_Juggler_E',
        'Trainer_Party_Fuchsia_Gym_Tamer_A',
        'Trainer_Party_Fuchsia_Gym_Tamer_B',
        'Trainer_Party_Koga_A',
    ],
    'Viridian Gym': [
        'Trainer_Party_Viridian_Gym_Tamer_A',
        'Trainer_Party_Viridian_Gym_Tamer_B',
        'Trainer_Party_Viridian_Gym_Blackbelt_A',
        'Trainer_Party_Viridian_Gym_Blackbelt_B',
        'Trainer_Party_Viridian_Gym_Blackbelt_C',
        'Trainer_Party_Viridian_Gym_Giovanni_A',
        'Trainer_Party_Viridian_Gym_CooltrainerM_A',
        'Trainer_Party_Viridian_Gym_CooltrainerM_C',
        'Trainer_Party_Viridian_Gym_CooltrainerM_D',
    ],
    'Route 18-E': [
        'Trainer_Party_Route_18_BirdKeeper_A',
        'Trainer_Party_Route_18_BirdKeeper_B',
        'Trainer_Party_Route_18_BirdKeeper_C',
    ],
    'Saffron Fighting Dojo': [
        'Trainer_Party_Fighting_Dojo_Blackbelt_A',
        'Trainer_Party_Fighting_Dojo_Blackbelt_B',
        'Trainer_Party_Fighting_Dojo_Blackbelt_C',
        'Trainer_Party_Fighting_Dojo_Blackbelt_D',
        'Trainer_Party_Fighting_Dojo_Blackbelt_E',
    ],
    "Oak's Lab": [
        (
            'Trainer_Party_Pallet_Town_Green1_A',
            'Trainer_Party_Pallet_Town_Green1_B',
            'Trainer_Party_Pallet_Town_Green1_C',
        ),
    ],
    'Route 22': [
        (
            'Trainer_Party_Route_22_Green1_A',
            'Trainer_Party_Route_22_Green1_B',
            'Trainer_Party_Route_22_Green1_C',
        ),
    ],
    'Route 22-F': [
        (
            'Trainer_Party_Route_22_Green2_A',
            'Trainer_Party_Route_22_Green2_B',
            'Trainer_Party_Route_22_Green2_C',
        ),
    ],
    'Cerulean City': [
        (
            'Trainer_Party_Cerulean_City_Green1_A',
            'Trainer_Party_Cerulean_City_Green1_B',
            'Trainer_Party_Cerulean_City_Green1_C',
        ),
        'Trainer_Party_Cerulean_City_Rocket_A',
    ],
    'Pokemon Mansion 1F-SE': [
        'Trainer_Party_Mansion_1F_Scientist_A',
    ],
    'Silph Co 2F-SW': [
        'Trainer_Party_Silph_Co_2F_Scientist_A',
    ],
    'Silph Co 2F': [
        'Trainer_Party_Silph_Co_2F_Scientist_B',
        'Trainer_Party_Silph_Co_2F_Rocket_A',
        'Trainer_Party_Silph_Co_2F_Rocket_B',
    ],
    'Silph Co 3F-W': [
        'Trainer_Party_Silph_Co_3F_Scientist_A',
    ],
    'Silph Co 3F': [
        'Trainer_Party_Silph_Co_3F_Rocket_A',
    ],
    'Silph Co 4F-N': [
        'Trainer_Party_Silph_Co_4F_Scientist_A',
    ],
    'Silph Co 4F': [
        'Trainer_Party_Silph_Co_4F_Rocket_A',
        'Trainer_Party_Silph_Co_4F_Rocket_B',
    ],
    'Silph Co 6F': [
        'Trainer_Party_Silph_Co_6F_Scientist_A',
        'Trainer_Party_Silph_Co_6F_Rocket_A',
        'Trainer_Party_Silph_Co_6F_Rocket_B',
    ],
    'Silph Co 7F': [
        'Trainer_Party_Silph_Co_7F_Scientist_A',
        'Trainer_Party_Silph_Co_7F_Rocket_A',
        'Trainer_Party_Silph_Co_7F_Rocket_B',
    ],
    'Silph Co 7F-SE': [
        'Trainer_Party_Silph_Co_7F_Rocket_C',
    ],
    'Silph Co 7F-NW': [
        (
            'Trainer_Party_Silph_Co_7F_Green2_A',
            'Trainer_Party_Silph_Co_7F_Green2_B',
            'Trainer_Party_Silph_Co_7F_Green2_C',
        ),
    ],
    'Silph Co 8F': [
        'Trainer_Party_Silph_Co_8F_Scientist_A',
        'Trainer_Party_Silph_Co_8F_Rocket_A',
        'Trainer_Party_Silph_Co_8F_Rocket_B',
    ],
    'Silph Co 9F': [
        'Trainer_Party_Silph_Co_9F_Scientist_A',
        'Trainer_Party_Silph_Co_9F_Rocket_B',
    ],
    'Silph Co 9F-NW': [
        'Trainer_Party_Silph_Co_9F_Rocket_A',
    ],
    'Silph Co 10F': [
        'Trainer_Party_Silph_Co_10F_Scientist_A',
        'Trainer_Party_Silph_Co_10F_Rocket_A',
    ],
    'Rocket Hideout B4F': [
        'Trainer_Party_Rocket_Hideout_B4F_Giovanni_A',
        'Trainer_Party_Rocket_Hideout_B4F_Rocket_A',
        'Trainer_Party_Rocket_Hideout_B4F_Rocket_B',
    ],
    'Rocket Hideout B4F-NW': [
        'Trainer_Party_Rocket_Hideout_B4F_Rocket_C',
    ],
    'Silph Co 11F': [
        'Trainer_Party_Silph_Co_11F_Rocket_A',
    ],
    'Silph Co 11F-W': [
        'Trainer_Party_Silph_Co_11F_Rocket_B',
    ],
    'Silph Co 11F-C': [
        'Trainer_Party_Silph_Co_11F_Giovanni_A',
    ],
    'Celadon Game Corner': [
        'Trainer_Party_Game_Corner_Rocket_A',
    ],
    'Rocket Hideout B1F': [
        'Trainer_Party_Rocket_Hideout_B1F_Rocket_A',
        'Trainer_Party_Rocket_Hideout_B1F_Rocket_B',
    ],
    'Rocket Hideout B1F-S': [
        'Trainer_Party_Rocket_Hideout_B1F_Rocket_C',
        'Trainer_Party_Rocket_Hideout_B1F_Rocket_D',
    ],
    'Rocket Hideout B1F-SE': [
        'Trainer_Party_Rocket_Hideout_B1F_Rocket_E',
    ],
    'Rocket Hideout B2F': [
        'Trainer_Party_Rocket_Hideout_B2F_Rocket_A',
    ],
    'Rocket Hideout B3F': [
        'Trainer_Party_Rocket_Hideout_B3F_Rocket_A',
        'Trainer_Party_Rocket_Hideout_B3F_Rocket_B',
    ],
    'Pokemon Tower 7F': [
        'Trainer_Party_Pokemon_Tower_7F_Rocket_A',
        'Trainer_Party_Pokemon_Tower_7F_Rocket_B',
        'Trainer_Party_Pokemon_Tower_7F_Rocket_C',
    ],
    'Victory Road 3F': [
        'Trainer_Party_Victory_Road_3F_CooltrainerM_A',
        'Trainer_Party_Victory_Road_3F_CooltrainerF_B',
    ],
    'Victory Road 3F-S': [
        'Trainer_Party_Victory_Road_3F_CooltrainerM_B',
        'Trainer_Party_Victory_Road_3F_CooltrainerF_A',
    ],
    'Victory Road 1F': [
        'Trainer_Party_Victory_Road_1F_CooltrainerM_A',
        'Trainer_Party_Victory_Road_1F_CooltrainerF_A',
    ],
    "Indigo Plateau Bruno's Room": [
        'Trainer_Party_Bruno_A',
    ],
    "Indigo Plateau Lorelei's Room": [
        'Trainer_Party_Lorelei_A',
    ],
    "Indigo Plateau Agatha's Room": [
        'Trainer_Party_Agatha_A',
    ],
    "Indigo Plateau Lance's Room": [
        'Trainer_Party_Lance_A',
    ],
    'S.S. Anne 2F': [
        (
            'Trainer_Party_SS_Anne_2F_Green2_A',
            'Trainer_Party_SS_Anne_2F_Green2_B',
            'Trainer_Party_SS_Anne_2F_Green2_C',
        ),
    ],
    'Pokemon Tower 2F': [
        (
            'Trainer_Party_Pokemon_Tower_2F_Green2_A',
            'Trainer_Party_Pokemon_Tower_2F_Green2_B',
            'Trainer_Party_Pokemon_Tower_2F_Green2_C',
        ),
    ],
    "Indigo Plateau Champion's Room": [
        (
            'Trainer_Party_Indigo_Plateau_Green3_A',
            'Trainer_Party_Indigo_Plateau_Green3_B',
            'Trainer_Party_Indigo_Plateau_Green3_C',
        ),
    ],
    'Pokemon Tower 3F': [
        'Trainer_Party_Pokemon_Tower_3F_Channeler_A',
        'Trainer_Party_Pokemon_Tower_3F_Channeler_B',
        'Trainer_Party_Pokemon_Tower_3F_Channeler_D',
    ],
    'Pokemon Tower 4F': [
        'Trainer_Party_Pokemon_Tower_4F_Channeler_A',
        'Trainer_Party_Pokemon_Tower_4F_Channeler_B',
        'Trainer_Party_Pokemon_Tower_4F_Channeler_D',
    ],
    'Pokemon Tower 5F': [
        'Trainer_Party_Pokemon_Tower_5F_Channeler_A',
        'Trainer_Party_Pokemon_Tower_5F_Channeler_C',
        'Trainer_Party_Pokemon_Tower_5F_Channeler_D',
        'Trainer_Party_Pokemon_Tower_5F_Channeler_E',
    ],
    'Pokemon Tower 6F': [
        'Trainer_Party_Pokemon_Tower_6F_Channeler_A',
        'Trainer_Party_Pokemon_Tower_6F_Channeler_B',
        'Trainer_Party_Pokemon_Tower_6F_Channeler_C',
    ],
}


_trainer_data_yellow_order = {
    'Fossil Level': [
        'Fossil_Level',
    ],
    'Route 3': [
        'Trainer_Party_Route_3_Youngster_A',
        'Trainer_Party_Route_3_Youngster_B',
        'Trainer_Party_Route_3_BugCatcher_A',
        'Trainer_Party_Route_3_BugCatcher_B',
        'Trainer_Party_Route_3_BugCatcher_C',
        'Trainer_Party_Route_3_Lass_A',
        'Trainer_Party_Route_3_Lass_B',
        'Trainer_Party_Route_3_Lass_C',
    ],
    'Mt Moon 1F': [
        'Trainer_Party_Mt_Moon_1F_Youngster_A',
        'Trainer_Party_Mt_Moon_1F_BugCatcher_A',
        'Trainer_Party_Mt_Moon_1F_BugCatcher_B',
        'Trainer_Party_Mt_Moon_1F_Lass_A',
        'Trainer_Party_Mt_Moon_1F_Lass_B',
        'Trainer_Party_Mt_Moon_1F_SuperNerd_A',
        'Trainer_Party_Mt_Moon_1F_Hiker_A',
    ],
    'Route 24': [
        'Trainer_Party_Route_24_Youngster_A',
        'Trainer_Party_Route_24_BugCatcher_A',
        'Trainer_Party_Route_24_Lass_A',
        'Trainer_Party_Route_24_Lass_B',
        'Trainer_Party_Route_24_JrTrainerM_A',
        'Trainer_Party_Route_24_JrTrainerM_C',
        'Trainer_Party_Route_24_Rocket_A',
    ],
    'Route 25': [
        'Trainer_Party_Route_25_Youngster_A',
        'Trainer_Party_Route_25_Youngster_B',
        'Trainer_Party_Route_25_Youngster_C',
        'Trainer_Party_Route_25_Lass_A',
        'Trainer_Party_Route_25_Lass_B',
        'Trainer_Party_Route_25_JrTrainerM_A',
        'Trainer_Party_Route_25_Hiker_A',
        'Trainer_Party_Route_25_Hiker_B',
        'Trainer_Party_Route_25_Hiker_C',
    ],
    'S.S. Anne 1F Rooms-Youngster and Lass Room': [
        'Trainer_Party_SS_Anne_1F_Rooms_Youngster_A',
        'Trainer_Party_SS_Anne_1F_Rooms_Lass_A',
    ],
    'Route 11': [
        'Trainer_Party_Route_11_Youngster_A',
        'Trainer_Party_Route_11_Youngster_B',
        'Trainer_Party_Route_11_Youngster_C',
        'Trainer_Party_Route_11_Youngster_D',
        'Trainer_Party_Route_11_Engineer_A',
        'Trainer_Party_Route_11_Engineer_B',
        'Trainer_Party_Route_11_Gambler_A',
        'Trainer_Party_Route_11_Gambler_B',
        'Trainer_Party_Route_11_Gambler_C',
        'Trainer_Party_Route_11_Gambler_D',
    ],
    'Viridian Forest': [
        'Trainer_Party_Viridian_Forest_BugCatcher_A',
        'Trainer_Party_Viridian_Forest_BugCatcher_B',
        'Trainer_Party_Viridian_Forest_BugCatcher_C',
    ],
    'Route 6': [
        'Trainer_Party_Route_6_BugCatcher_A',
        'Trainer_Party_Route_6_BugCatcher_B',
        'Trainer_Party_Route_6_JrTrainerM_A',
        'Trainer_Party_Route_6_JrTrainerM_B',
        'Trainer_Party_Route_6_JrTrainerF_A',
        'Trainer_Party_Route_6_JrTrainerF_B',
    ],
    'Route 9': [
        'Trainer_Party_Route_9_BugCatcher_A',
        'Trainer_Party_Route_9_BugCatcher_B',
        'Trainer_Party_Route_9_JrTrainerM_A',
        'Trainer_Party_Route_9_JrTrainerM_B',
        'Trainer_Party_Route_9_JrTrainerF_A',
        'Trainer_Party_Route_9_JrTrainerF_B',
        'Trainer_Party_Route_9_Hiker_A',
        'Trainer_Party_Route_9_Hiker_B',
        'Trainer_Party_Route_9_Hiker_D',
    ],
    'Route 4-Lass': [
        'Trainer_Party_Route_4_Lass_A',
    ],
    'S.S. Anne 2F Rooms-Gentleman and Lass Room': [
        'Trainer_Party_SS_Anne_2F_Rooms_Lass_A',
        'Trainer_Party_SS_Anne_2F_Rooms_Gentleman_C',
    ],
    'Route 8': [
        'Trainer_Party_Route_8_Lass_A',
        'Trainer_Party_Route_8_Lass_B',
        'Trainer_Party_Route_8_Lass_C',
        'Trainer_Party_Route_8_Lass_D',
        'Trainer_Party_Route_8_SuperNerd_A',
        'Trainer_Party_Route_8_SuperNerd_B',
        'Trainer_Party_Route_8_SuperNerd_C',
        'Trainer_Party_Route_8_Gambler_A',
        'Trainer_Party_Route_8_Gambler_C',
    ],
    'Celadon Gym': [
        'Trainer_Party_Celadon_Gym_Lass_A',
        'Trainer_Party_Celadon_Gym_JrTrainerF_A',
        'Trainer_Party_Celadon_Gym_Beauty_A',
        'Trainer_Party_Celadon_Gym_Beauty_B',
    ],
    'Celadon Gym-C': [
        'Trainer_Party_Celadon_Gym_Lass_B',
        'Trainer_Party_Celadon_Gym_Beauty_C',
        'Trainer_Party_Celadon_Gym_CooltrainerF_A',
        'Trainer_Party_Erika_A',
    ],
    'S.S. Anne Bow': [
        'Trainer_Party_SS_Anne_Stern_Sailor_A',
        'Trainer_Party_SS_Anne_Stern_Sailor_B',
    ],
    'S.S. Anne B1F Rooms-Two Sailors Room': [
        'Trainer_Party_SS_Anne_B1F_Rooms_Sailor_A',
        'Trainer_Party_SS_Anne_B1F_Rooms_Sailor_B',
    ],
    'S.S. Anne B1F Rooms-West Single Sailor Room': [
        'Trainer_Party_SS_Anne_B1F_Rooms_Sailor_C',
    ],
    'S.S. Anne B1F Rooms-East Single Sailor Room': [
        'Trainer_Party_SS_Anne_B1F_Rooms_Sailor_D',
    ],
    'S.S. Anne B1F Rooms-Fisherman Room': [
        'Trainer_Party_SS_Anne_B1F_Rooms_Sailor_E',
        'Trainer_Party_SS_Anne_B1F_Rooms_Fisher_A',
    ],
    'Vermilion Gym': [
        'Trainer_Party_Vermilion_Gym_Sailor_A',
        'Trainer_Party_Vermilion_Gym_Rocker_A',
        'Trainer_Party_LtSurge_A',
        'Trainer_Party_Vermilion_Gym_Gentleman_A',
    ],
    'Pewter Gym': [
        'Trainer_Party_Pewter_Gym_JrTrainerM_A',
        'Trainer_Party_Brock_A',
    ],
    'Route 12-S': [
        'Trainer_Party_Route_12_JrTrainerM_A',
        'Trainer_Party_Route_12_Rocker_A',
    ],
    'Cerulean Gym': [
        'Trainer_Party_Cerulean_Gym_JrTrainerF_A',
        'Trainer_Party_Cerulean_Gym_Swimmer_A',
        'Trainer_Party_Misty_A',
    ],
    'Route 10-N': [
        'Trainer_Party_Route_10_JrTrainerF_A',
    ],
    'Route 10-S': [
        'Trainer_Party_Route_10_JrTrainerF_B',
        'Trainer_Party_Route_10_Pokemaniac_B',
        'Trainer_Party_Route_10_Hiker_A',
        'Trainer_Party_Route_10_Hiker_B',
    ],
    'Rock Tunnel B1F-W': [
        'Trainer_Party_Rock_Tunnel_B1F_JrTrainerF_A',
        'Trainer_Party_Rock_Tunnel_B1F_Pokemaniac_A',
        'Trainer_Party_Rock_Tunnel_B1F_Hiker_A',
    ],
    'Rock Tunnel B1F-E': [
        'Trainer_Party_Rock_Tunnel_B1F_JrTrainerF_B',
        'Trainer_Party_Rock_Tunnel_B1F_Pokemaniac_B',
        'Trainer_Party_Rock_Tunnel_B1F_Pokemaniac_C',
        'Trainer_Party_Rock_Tunnel_B1F_Hiker_B',
        'Trainer_Party_Rock_Tunnel_B1F_Hiker_D',
    ],
    'Route 13-E': [
        'Trainer_Party_Route_13_JrTrainerF_A',
        'Trainer_Party_Route_13_JrTrainerF_D',
        'Trainer_Party_Route_13_BirdKeeper_A',
    ],
    'Route 13': [
        'Trainer_Party_Route_13_JrTrainerF_B',
        'Trainer_Party_Route_13_JrTrainerF_C',
        'Trainer_Party_Route_13_Biker_A',
        'Trainer_Party_Route_13_Beauty_A',
        'Trainer_Party_Route_13_Beauty_B',
        'Trainer_Party_Route_13_BirdKeeper_B',
        'Trainer_Party_Route_13_BirdKeeper_C',
    ],
    'Route 20-W': [
        'Trainer_Party_Route_20_JrTrainerF_A',
        'Trainer_Party_Route_20_JrTrainerF_C',
        'Trainer_Party_Route_20_Swimmer_B',
        'Trainer_Party_Route_20_Beauty_B',
        'Trainer_Party_Route_20_Beauty_C',
        'Trainer_Party_Route_20_BirdKeeper_A',
    ],
    'Rock Tunnel 1F-S': [
        'Trainer_Party_Rock_Tunnel_1F_JrTrainerF_A',
        'Trainer_Party_Rock_Tunnel_1F_JrTrainerF_B',
        'Trainer_Party_Rock_Tunnel_1F_JrTrainerF_C',
    ],
    'Route 15': [
        'Trainer_Party_Route_15_JrTrainerF_A',
        'Trainer_Party_Route_15_JrTrainerF_B',
        'Trainer_Party_Route_15_JrTrainerF_D',
        'Trainer_Party_Route_15_Biker_A',
        'Trainer_Party_Route_15_Biker_B',
        'Trainer_Party_Route_15_Beauty_A',
        'Trainer_Party_Route_15_Beauty_B',
        'Trainer_Party_Route_15_BirdKeeper_A',
        'Trainer_Party_Route_15_BirdKeeper_B',
    ],
    'Route 15-N': [
        'Trainer_Party_Route_15_JrTrainerF_C',
    ],
    'Route 10-C': [
        'Trainer_Party_Route_10_Pokemaniac_A',
    ],
    'Victory Road 2F-NW': [
        'Trainer_Party_Victory_Road_2F_Pokemaniac_A',
    ],
    'Rock Tunnel 1F-NE': [
        'Trainer_Party_Rock_Tunnel_1F_Pokemaniac_A',
    ],
    'Mt Moon B2F': [
        'Trainer_Party_Mt_Moon_B2F_SuperNerd_A',
        'Trainer_Party_Mt_Moon_B2F_Rocket_A',
        'Trainer_Party_Mt_Moon_B2F_Rocket_D',
        'Trainer_Party_Mt_Moon_B2F_Rocket_Jessie_James_A',
    ],
    'Cinnabar Gym': [
        'Trainer_Party_Cinnabar_Gym_SuperNerd_A',
        'Trainer_Party_Cinnabar_Gym_SuperNerd_B',
        'Trainer_Party_Cinnabar_Gym_SuperNerd_C',
        'Trainer_Party_Cinnabar_Gym_SuperNerd_D',
        'Trainer_Party_Cinnabar_Gym_Burglar_A',
        'Trainer_Party_Cinnabar_Gym_Burglar_B',
        'Trainer_Party_Cinnabar_Gym_Burglar_C',
        'Trainer_Party_Blaine_A',
    ],
    'Rock Tunnel 1F-NW': [
        'Trainer_Party_Rock_Tunnel_1F_Hiker_A',
        'Trainer_Party_Rock_Tunnel_1F_Hiker_B',
        'Trainer_Party_Rock_Tunnel_1F_Hiker_C',
    ],
    'Route 14': [
        'Trainer_Party_Route_14_Biker_A',
        'Trainer_Party_Route_14_Biker_C',
        'Trainer_Party_Route_14_Biker_D',
        'Trainer_Party_Route_14_Biker_E',
        'Trainer_Party_Route_14_BirdKeeper_A',
        'Trainer_Party_Route_14_BirdKeeper_B',
        'Trainer_Party_Route_14_BirdKeeper_D',
        'Trainer_Party_Route_14_BirdKeeper_E',
        'Trainer_Party_Route_14_BirdKeeper_F',
        'Trainer_Party_Route_14_BirdKeeper_G',
    ],
    'Route 16-SW': [
        'Trainer_Party_Route_16_Biker_A',
        'Trainer_Party_Route_16_Biker_B',
        'Trainer_Party_Route_16_Biker_C',
        'Trainer_Party_Route_16_CueBall_A',
        'Trainer_Party_Route_16_CueBall_B',
        'Trainer_Party_Route_16_CueBall_C',
    ],
    'Route 17': [
        'Trainer_Party_Route_17_Biker_A',
        'Trainer_Party_Route_17_Biker_B',
        'Trainer_Party_Route_17_Biker_C',
        'Trainer_Party_Route_17_Biker_D',
        'Trainer_Party_Route_17_Biker_E',
        'Trainer_Party_Route_17_CueBall_A',
        'Trainer_Party_Route_17_CueBall_B',
        'Trainer_Party_Route_17_CueBall_C',
        'Trainer_Party_Route_17_CueBall_D',
        'Trainer_Party_Route_17_CueBall_E',
    ],
    'Pokemon Mansion 2F': [
        'Trainer_Party_Mansion_2F_Burglar_A',
    ],
    'Pokemon Mansion 3F-SW': [
        'Trainer_Party_Mansion_3F_Burglar_A',
    ],
    'Pokemon Mansion B1F': [
        'Trainer_Party_Mansion_B1F_Burglar_A',
        'Trainer_Party_Mansion_B1F_Scientist_A',
    ],
    'S.S. Anne 2F Rooms-Fisherman and Gentleman Room': [
        'Trainer_Party_SS_Anne_2F_Rooms_Fisher_A',
        'Trainer_Party_SS_Anne_2F_Rooms_Gentleman_A',
    ],
    'Route 12-N': [
        'Trainer_Party_Route_12_Fisher_A',
        'Trainer_Party_Route_12_Fisher_B',
        'Trainer_Party_Route_12_Fisher_C',
        'Trainer_Party_Route_12_Fisher_D',
    ],
    'Route 21': [
        'Trainer_Party_Route_21_Fisher_A',
        'Trainer_Party_Route_21_Fisher_B',
        'Trainer_Party_Route_21_Fisher_C',
        'Trainer_Party_Route_21_Fisher_D',
        'Trainer_Party_Route_21_Swimmer_A',
        'Trainer_Party_Route_21_Swimmer_B',
        'Trainer_Party_Route_21_Swimmer_C',
        'Trainer_Party_Route_21_Swimmer_D',
        'Trainer_Party_Route_21_CueBall_A',
    ],
    'Route 12-Grass': [
        'Trainer_Party_Route_12_Fisher_F',
    ],
    'Route 19-N': [
        'Trainer_Party_Route_19_Swimmer_A',
        'Trainer_Party_Route_19_Swimmer_B',
    ],
    'Route 19-S': [
        'Trainer_Party_Route_19_Swimmer_C',
        'Trainer_Party_Route_19_Swimmer_D',
        'Trainer_Party_Route_19_Swimmer_E',
        'Trainer_Party_Route_19_Swimmer_F',
        'Trainer_Party_Route_19_Swimmer_G',
        'Trainer_Party_Route_19_Beauty_A',
        'Trainer_Party_Route_19_Beauty_B',
        'Trainer_Party_Route_19_Beauty_C',
    ],
    'Route 20-E': [
        'Trainer_Party_Route_20_Swimmer_A',
        'Trainer_Party_Route_20_Swimmer_C',
        'Trainer_Party_Route_20_Beauty_A',
        'Trainer_Party_Route_20_Beauty_E',
    ],
    'Saffron Gym-NE': [
        'Trainer_Party_Saffron_Gym_Psychic_A',
    ],
    'Saffron Gym-E': [
        'Trainer_Party_Saffron_Gym_Psychic_B',
    ],
    'Saffron Gym-SE': [
        'Trainer_Party_Saffron_Gym_Psychic_C',
    ],
    'Saffron Gym-NW': [
        'Trainer_Party_Saffron_Gym_Psychic_D',
    ],
    'Silph Co 5F': [
        'Trainer_Party_Silph_Co_5F_Juggler_A',
        'Trainer_Party_Silph_Co_5F_Scientist_A',
        'Trainer_Party_Silph_Co_5F_Rocket_A',
        'Trainer_Party_Silph_Co_5F_Rocket_B',
    ],
    'Victory Road 2F-C': [
        'Trainer_Party_Victory_Road_2F_Juggler_A',
        'Trainer_Party_Victory_Road_2F_Juggler_C',
        'Trainer_Party_Victory_Road_2F_Tamer_A',
        'Trainer_Party_Victory_Road_2F_Blackbelt_A',
    ],
    'Fuchsia Gym': [
        'Trainer_Party_Fuchsia_Gym_Juggler_A',
        'Trainer_Party_Fuchsia_Gym_Juggler_B',
        'Trainer_Party_Fuchsia_Gym_Juggler_D',
        'Trainer_Party_Fuchsia_Gym_Juggler_E',
        'Trainer_Party_Fuchsia_Gym_Tamer_A',
        'Trainer_Party_Fuchsia_Gym_Tamer_B',
        'Trainer_Party_Koga_A',
    ],
    'Viridian Gym': [
        'Trainer_Party_Viridian_Gym_Tamer_A',
        'Trainer_Party_Viridian_Gym_Tamer_B',
        'Trainer_Party_Viridian_Gym_Blackbelt_A',
        'Trainer_Party_Viridian_Gym_Blackbelt_B',
        'Trainer_Party_Viridian_Gym_Blackbelt_C',
        'Trainer_Party_Viridian_Gym_Giovanni_A',
        'Trainer_Party_Viridian_Gym_CooltrainerM_A',
        'Trainer_Party_Viridian_Gym_CooltrainerM_C',
        'Trainer_Party_Viridian_Gym_CooltrainerM_D',
    ],
    'Route 18-E': [
        'Trainer_Party_Route_18_BirdKeeper_A',
        'Trainer_Party_Route_18_BirdKeeper_B',
        'Trainer_Party_Route_18_BirdKeeper_C',
    ],
    'Saffron Fighting Dojo': [
        'Trainer_Party_Fighting_Dojo_Blackbelt_A',
        'Trainer_Party_Fighting_Dojo_Blackbelt_B',
        'Trainer_Party_Fighting_Dojo_Blackbelt_C',
        'Trainer_Party_Fighting_Dojo_Blackbelt_D',
        'Trainer_Party_Fighting_Dojo_Blackbelt_E',
    ],
    "Oak's Lab": [
        'Trainer_Party_Oaks_Lab_Rival1_A',
    ],
    'Route 22': [
        'Trainer_Party_Route_22_Rival1_A',
    ],
    'Cerulean City': [
        'Trainer_Party_Cerulean_City_Rival1_A',
        'Trainer_Party_Cerulean_City_Rocket_A',
    ],
    'Pokemon Mansion 1F-SE': [
        'Trainer_Party_Mansion_1F_Scientist_A',
    ],
    'Silph Co 2F-SW': [
        'Trainer_Party_Silph_Co_2F_Scientist_A',
    ],
    'Silph Co 2F': [
        'Trainer_Party_Silph_Co_2F_Scientist_B',
        'Trainer_Party_Silph_Co_2F_Rocket_A',
        'Trainer_Party_Silph_Co_2F_Rocket_B',
    ],
    'Silph Co 3F-W': [
        'Trainer_Party_Silph_Co_3F_Scientist_A',
    ],
    'Silph Co 4F-N': [
        'Trainer_Party_Silph_Co_4F_Scientist_A',
    ],
    'Silph Co 6F': [
        'Trainer_Party_Silph_Co_6F_Scientist_A',
        'Trainer_Party_Silph_Co_6F_Rocket_A',
        'Trainer_Party_Silph_Co_6F_Rocket_B',
    ],
    'Silph Co 7F': [
        'Trainer_Party_Silph_Co_7F_Scientist_A',
        'Trainer_Party_Silph_Co_7F_Rocket_A',
        'Trainer_Party_Silph_Co_7F_Rocket_B',
    ],
    'Silph Co 8F': [
        'Trainer_Party_Silph_Co_8F_Scientist_A',
        'Trainer_Party_Silph_Co_8F_Rocket_A',
        'Trainer_Party_Silph_Co_8F_Rocket_B',
    ],
    'Silph Co 9F': [
        'Trainer_Party_Silph_Co_9F_Scientist_A',
        'Trainer_Party_Silph_Co_9F_Rocket_B',
    ],
    'Silph Co 10F': [
        'Trainer_Party_Silph_Co_10F_Scientist_A',
        'Trainer_Party_Silph_Co_10F_Rocket_A',
    ],
    'Pokemon Mansion 3F-SE': [
        'Trainer_Party_Mansion_3F_Scientist_A',
    ],
    'Rocket Hideout B4F': [
        'Trainer_Party_Rocket_Hideout_B4F_Giovanni_A',
        'Trainer_Party_Rocket_Hideout_B4F_Rocket_A',
        'Trainer_Party_Rocket_Hideout_B4F_Rocket_B',
        'Trainer_Party_Rocket_Hideout_B4F_Rocket_Jessie_James_A',
    ],
    'Silph Co 11F-C': [
        'Trainer_Party_Silph_Co_11F_Giovanni_A',
        'Trainer_Party_Silph_Co_11F_Rocket_Jessie_James_A',
    ],
    'Mt Moon B2F-C': [
        'Trainer_Party_Mt_Moon_B2F_Rocket_B',
    ],
    'Mt Moon B2F-NE': [
        'Trainer_Party_Mt_Moon_B2F_Rocket_C',
    ],
    'Celadon Game Corner': [
        'Trainer_Party_Game_Corner_Rocket_A',
    ],
    'Rocket Hideout B1F': [
        'Trainer_Party_Rocket_Hideout_B1F_Rocket_A',
        'Trainer_Party_Rocket_Hideout_B1F_Rocket_B',
    ],
    'Rocket Hideout B1F-S': [
        'Trainer_Party_Rocket_Hideout_B1F_Rocket_C',
        'Trainer_Party_Rocket_Hideout_B1F_Rocket_D',
    ],
    'Rocket Hideout B1F-SE': [
        'Trainer_Party_Rocket_Hideout_B1F_Rocket_E',
    ],
    'Rocket Hideout B2F': [
        'Trainer_Party_Rocket_Hideout_B2F_Rocket_A',
    ],
    'Rocket Hideout B3F': [
        'Trainer_Party_Rocket_Hideout_B3F_Rocket_A',
        'Trainer_Party_Rocket_Hideout_B3F_Rocket_B',
    ],
    'Rocket Hideout B4F-NW': [
        'Trainer_Party_Rocket_Hideout_B4F_Rocket_C',
    ],
    'Pokemon Tower 7F': [
        'Trainer_Party_Pokemon_Tower_7F_Rocket_A',
        'Trainer_Party_Pokemon_Tower_7F_Rocket_B',
        'Trainer_Party_Pokemon_Tower_7F_Rocket_C',
        'Trainer_Party_Pokemon_Tower_7F_Rocket_Jessie_James_A',
    ],
    'Silph Co 3F': [
        'Trainer_Party_Silph_Co_3F_Rocket_A',
    ],
    'Silph Co 4F': [
        'Trainer_Party_Silph_Co_4F_Rocket_A',
        'Trainer_Party_Silph_Co_4F_Rocket_B',
    ],
    'Silph Co 7F-SE': [
        'Trainer_Party_Silph_Co_7F_Rocket_C',
    ],
    'Silph Co 9F-NW': [
        'Trainer_Party_Silph_Co_9F_Rocket_A',
    ],
    'Silph Co 11F': [
        'Trainer_Party_Silph_Co_11F_Rocket_A',
    ],
    'Silph Co 11F-W': [
        'Trainer_Party_Silph_Co_11F_Rocket_B',
    ],
    'Victory Road 3F': [
        'Trainer_Party_Victory_Road_3F_CooltrainerM_A',
        'Trainer_Party_Victory_Road_3F_CooltrainerF_B',
    ],
    'Victory Road 3F-S': [
        'Trainer_Party_Victory_Road_3F_CooltrainerM_B',
        'Trainer_Party_Victory_Road_3F_CooltrainerF_A',
    ],
    'Victory Road 1F': [
        'Trainer_Party_Victory_Road_1F_CooltrainerM_A',
        'Trainer_Party_Victory_Road_1F_CooltrainerF_A',
    ],
    "Indigo Plateau Bruno's Room": [
        'Trainer_Party_Bruno_A',
    ],
    'Saffron Gym-C': [
        'Trainer_Party_Sabrina_A',
    ],
    'S.S. Anne 1F Rooms-East Gentleman Room': [
        'Trainer_Party_SS_Anne_1F_Rooms_Gentleman_A',
    ],
    'S.S. Anne 1F Rooms-West Gentleman Room': [
        'Trainer_Party_SS_Anne_1F_Rooms_Gentleman_B',
    ],
    'S.S. Anne 2F': [
        'Trainer_Party_SS_Anne_2F_Rival2_A',
    ],
    'Pokemon Tower 2F': [
        (
            'Trainer_Party_Pokemon_Tower_2F_Rival2_Jolteon_A',
            'Trainer_Party_Pokemon_Tower_2F_Rival2_Flareon_A',
            'Trainer_Party_Pokemon_Tower_2F_Rival2_Vaporeon_A',
        ),
    ],
    'Silph Co 7F-NW': [
        (
            'Trainer_Party_Silph_Co_7F_Rival2_Jolteon_A',
            'Trainer_Party_Silph_Co_7F_Rival2_Flareon_A',
            'Trainer_Party_Silph_Co_7F_Rival2_Vaporeon_A',
        ),
    ],
    'Route 22-F': [
        (
            'Trainer_Party_Route_22_Rival2_Jolteon_A',
            'Trainer_Party_Route_22_Rival2_Flareon_A',
            'Trainer_Party_Route_22_Rival2_Vaporeon_A',
        ),
    ],
    "Indigo Plateau Champion's Room": [
        (
            'Trainer_Party_Indigo_Plateau_Rival3_Jolteon_A',
            'Trainer_Party_Indigo_Plateau_Rival3_Flareon_A',
            'Trainer_Party_Indigo_Plateau_Rival3_Vaporeon_A',
        ),
    ],
    "Indigo Plateau Lorelei's Room": [
        'Trainer_Party_Lorelei_A',
    ],
    'Pokemon Tower 3F': [
        'Trainer_Party_Pokemon_Tower_3F_Channeler_A',
        'Trainer_Party_Pokemon_Tower_3F_Channeler_B',
        'Trainer_Party_Pokemon_Tower_3F_Channeler_D',
    ],
    'Pokemon Tower 4F': [
        'Trainer_Party_Pokemon_Tower_4F_Channeler_A',
        'Trainer_Party_Pokemon_Tower_4F_Channeler_B',
        'Trainer_Party_Pokemon_Tower_4F_Channeler_D',
    ],
    'Pokemon Tower 5F': [
        'Trainer_Party_Pokemon_Tower_5F_Channeler_A',
        'Trainer_Party_Pokemon_Tower_5F_Channeler_C',
        'Trainer_Party_Pokemon_Tower_5F_Channeler_D',
        'Trainer_Party_Pokemon_Tower_5F_Channeler_E',
    ],
    'Pokemon Tower 6F': [
        'Trainer_Party_Pokemon_Tower_6F_Channeler_A',
        'Trainer_Party_Pokemon_Tower_6F_Channeler_B',
        'Trainer_Party_Pokemon_Tower_6F_Channeler_C',
    ],
    'Saffron Gym-N': [
        'Trainer_Party_Saffron_Gym_Channeler_A',
    ],
    'Saffron Gym-W': [
        'Trainer_Party_Saffron_Gym_Channeler_B',
    ],
    'Saffron Gym-SW': [
        'Trainer_Party_Saffron_Gym_Channeler_C',
    ],
    "Indigo Plateau Agatha's Room": [
        'Trainer_Party_Agatha_A',
    ],
    "Indigo Plateau Lance's Room": [
        'Trainer_Party_Lance_A',
    ],
}

def combine_trainer_data(*data_sets):
    combined = {}
    for data_set in data_sets:
        for region, parties in data_set.items():
            combined.setdefault(region, [])
            combined[region].extend(deepcopy(parties))
    return combined


trainer_data_rb = combine_trainer_data(trainer_data_common, _trainer_data_rb)
trainer_data_yellow = combine_trainer_data(
    trainer_data_common,
    _trainer_data_yellow,
)
