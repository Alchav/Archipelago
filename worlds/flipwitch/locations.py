from random import Random
from typing import List, Dict

from BaseClasses import MultiWorld, Item, ItemClassification, Location
from . import FlipwitchOptions
from .data.items import item_name_to_item
from .data.locations import all_locations, gacha_locations, FlipwitchLocation, coin_locations, shop_locations, quest_locations, sex_experience_locations, \
    stat_locations
from .strings.items import Goal, Coin, Upgrade
from .strings.locations import WitchyWoods, GhostCastle, ClubDemon, AngelicHallway, SlimeCitadel, UmiUmi

location_table = all_locations
locations_by_name: Dict[str, FlipwitchLocation] = {location.name: location for location in location_table}


def construct_forced_local_items(lookup_table: Dict[str, List[Location]], player: int, item_repository: Dict[str, int], options: FlipwitchOptions, random: Random):
    force_chaos_pieces(player, item_repository, lookup_table, options)
    force_gacha_items(player, item_repository, lookup_table, options, random)
    create_shop_locations(player, item_repository, lookup_table, options)
    create_quest_locations(player, item_repository, lookup_table, options)
    create_stat_locations(player, item_repository, lookup_table, options)


def force_location_table(multiworld: MultiWorld, player: int):
    location_dictionary: Dict[str, List[Location]] = \
        {
            "Chaos Pieces": [],
            "Shop Locations": [],
            "Gacha Locations": [],
            "Coin Locations": [],
            "Quest Locations": [],
            "Sex Experience Locations": [],
            "Stat Locations": [],
        }
    for location in multiworld.get_locations(player):
        if location.name in [WitchyWoods.goblin_queen_chaos, GhostCastle.ghost_chaos, ClubDemon.demon_boss_chaos,
                             AngelicHallway.angelica_chaos, SlimeCitadel.slimy_princess_chaos, UmiUmi.frog_boss_chaos]:
            location_dictionary["Chaos Pieces"].append(location)
        elif location.name in [spot.name for spot in shop_locations]:
            location_dictionary["Shop Locations"].append(location)
        elif location.name in [spot.name for spot in gacha_locations]:
            location_dictionary["Gacha Locations"].append(location)
        elif location.name in [spot.name for spot in coin_locations]:
            location_dictionary["Coin Locations"].append(location)
        elif location.name in [spot.name for spot in quest_locations]:
            location_dictionary["Quest Locations"].append(location)
        elif location.name in [spot.name for spot in sex_experience_locations]:
            location_dictionary["Sex Experience Locations"].append(location)
        elif location.name in [spot.name for spot in stat_locations]:
            location_dictionary["Stat Locations"].append(location)
    return location_dictionary


def get_forced_location_count(item_lookup: Dict[str, List[Location]], options: FlipwitchOptions):
    count = 0
    if options.shuffle_chaos_pieces == options.shuffle_chaos_pieces.option_false:
        count += len(item_lookup["Chaos Pieces"])
    if options.stat_shuffle == options.stat_shuffle.option_false:
        count += len(item_lookup["Stat Locations"])
    if options.gachapon_shuffle != options.gachapon_shuffle.option_all:
        count += len(item_lookup["Gacha Locations"])
        if options.gachapon_shuffle == options.gachapon_shuffle.option_off:
            count += len(item_lookup["Coin Locations"])
    if options.quest_for_sex != options.quest_for_sex.option_all and options.quest_for_sex != options.quest_for_sex.option_quests:
        count += len(item_lookup["Quest Locations"])
        if options.quest_for_sex == options.quest_for_sex.option_off:
            count += len(item_lookup["Sex Experience Locations"])
    if options.shopsanity == options.shopsanity.option_false:
        count += len(item_lookup["Shop Locations"])
    return count


def force_chaos_pieces(player: int, item_repository: Dict[str, int], lookup_table: Dict[str, List[Location]], options: FlipwitchOptions):
    if options.shuffle_chaos_pieces == options.shuffle_chaos_pieces.option_true:
        return
    for location in lookup_table["Chaos Pieces"]:
        created_item = Item(Goal.chaos_piece, item_name_to_item[Goal.chaos_piece].classification, None, player)
        location.place_locked_item(created_item)


def force_gacha_items(player: int, item_repository: Dict[str, int], lookup_table: Dict[str, List[Location]], options: FlipwitchOptions, random: Random):
    if options.gachapon_shuffle == options.gachapon_shuffle.option_all:
        return
    for location in lookup_table["Gacha Locations"]:
        static_item_name = locations_by_name[location.name].forced_off_item
        created_item = Item(static_item_name, item_name_to_item[static_item_name].classification, None, player)
        location.place_locked_item(created_item)
    if options.gachapon_shuffle == options.gachapon_shuffle.option_coin:
        return
    coins = [coin for coin in Coin.lucky_coins*10 if coin != Coin.promotional_coin]
    coins.append(Coin.promotional_coin)
    chosen_coins = random.sample(Coin.lucky_coins, 3)
    coins.extend(chosen_coins)
    random.shuffle(coins)
    coin_items = []
    for coin in coins:
        coin_items.append(Item(coin, ItemClassification.progression, None, player))
    for location in lookup_table["Coin Locations"]:
        static_item_name = coins.pop()
        created_item = Item(static_item_name, item_name_to_item[static_item_name].classification, None, player)
        location.place_locked_item(created_item)


def create_shop_locations(player: int, item_repository: Dict[str, int], lookup_table: Dict[str, List[Location]], options: FlipwitchOptions):
    if options.shopsanity == options.shopsanity.option_true:
        return
    for location in lookup_table["Shop Locations"]:
        static_item_name = locations_by_name[location.name].forced_off_item
        created_item = Item(static_item_name, item_name_to_item[static_item_name].classification, None, player)
        location.place_locked_item(created_item)


def create_quest_locations(player: int, item_repository: Dict[str, int], lookup_table: Dict[str, List[Location]], options: FlipwitchOptions):
    if options.quest_for_sex == options.quest_for_sex.option_all or options.quest_for_sex == options.quest_for_sex.option_quests:
        return
    for location in lookup_table["Quest Locations"]:
        static_item_name = locations_by_name[location.name].forced_off_item
        created_item = Item(static_item_name, item_name_to_item[static_item_name].classification, None, player)
        location.place_locked_item(created_item)
    if options.quest_for_sex == options.quest_for_sex.option_sensei:
        return
    count = 0
    for location in lookup_table["Sex Experience Locations"]:
        static_item_name = locations_by_name[location.name].forced_off_item
        if count < 8 and static_item_name == Upgrade.peachy_peach:
            created_item = Item(static_item_name, ItemClassification.progression, None, player)
            count += 1
        else:
            created_item = Item(static_item_name, item_name_to_item[static_item_name].classification, None, player)
        location.place_locked_item(created_item)


def create_stat_locations(player: int, item_repository: Dict[str, int], lookup_table: Dict[str, List[Location]], options: FlipwitchOptions):
    if options.stat_shuffle == options.stat_shuffle.option_true:
        return
    count = 0
    for location in lookup_table["Stat Locations"]:
        static_item_name = locations_by_name[location.name].forced_off_item
        if count < 8 and static_item_name == Upgrade.health:
            created_item = Item(static_item_name, ItemClassification.progression, None, player)
            count += 1
        else:
            created_item = Item(static_item_name, item_name_to_item[static_item_name].classification, None, player)
        location.place_locked_item(created_item)
