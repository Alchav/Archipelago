from . import content_packs
from .feature import friendsanity, fishsanity
from .game_content import ContentPack, StardewContent, StardewFeatures
from .unpacking import unpack_content
from .. import options


def create_content(player_options: options.StardewValleyOptions) -> StardewContent:
    active_packs = choose_content_packs(player_options)
    features = choose_features(player_options)
    return unpack_content(features, active_packs)


def choose_content_packs(player_options: options.StardewValleyOptions):
    active_packs = [content_packs.pelican_town]

    if player_options.exclude_ginger_island == options.ExcludeGingerIsland.option_false:
        active_packs.append(content_packs.ginger_island)

        if player_options.special_order_locations == options.SpecialOrderLocations.option_board_qi:
            active_packs.append(content_packs.qi_board)

    for mod in player_options.mods.value:
        active_packs.append(content_packs.by_mod[mod])

    return active_packs


def choose_features(player_options: options.StardewValleyOptions) -> StardewFeatures:
    return StardewFeatures(
        choose_fishsanity(player_options.fishsanity),
        choose_friendsanity(player_options.friendsanity, player_options.friendsanity_heart_size)
    )


fishsanity_by_option = {
    options.Fishsanity.option_none: fishsanity.FishsanityNone(),
    options.Fishsanity.option_legendaries: fishsanity.FishsanityLegendaries(),
    options.Fishsanity.option_special: fishsanity.FishsanitySpecial(),
    options.Fishsanity.option_randomized: fishsanity.FishsanityAll(randomization_ratio=0.4),
    options.Fishsanity.option_all: fishsanity.FishsanityAll(),
    options.Fishsanity.option_exclude_legendaries: fishsanity.FishsanityExcludeLegendaries(),
    options.Fishsanity.option_exclude_hard_fish: fishsanity.FishsanityExcludeHardFish(),
    options.Fishsanity.option_only_easy_fish: fishsanity.FishsanityOnlyEasyFish(),
}


def choose_fishsanity(fishsanity_option: options.Fishsanity) -> fishsanity.FishsanityFeature:
    fishsanity_feature = fishsanity_by_option.get(fishsanity_option)

    if fishsanity_feature is None:
        raise ValueError(f"No fishsanity feature mapped to {str(fishsanity_option.value)}")

    return fishsanity_feature


def choose_friendsanity(friendsanity_option: options.Friendsanity, heart_size: options.FriendsanityHeartSize) -> friendsanity.FriendsanityFeature:
    if friendsanity_option == options.Friendsanity.option_none:
        return friendsanity.FriendsanityNone()

    if friendsanity_option == options.Friendsanity.option_bachelors:
        return friendsanity.FriendsanityBachelors(heart_size.value)

    if friendsanity_option == options.Friendsanity.option_starting_npcs:
        return friendsanity.FriendsanityStartingNpc(heart_size.value)

    if friendsanity_option == options.Friendsanity.option_all:
        return friendsanity.FriendsanityAll(heart_size.value)

    if friendsanity_option == options.Friendsanity.option_all_with_marriage:
        return friendsanity.FriendsanityAllWithMarriage(heart_size.value)

    raise ValueError(f"No friendsanity feature mapped to {str(friendsanity_option.value)}")
