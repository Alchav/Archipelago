from worlds.oot import OOTWorld, OOTCollectionState
from worlds.oot.LocationList import set_drop_location_names
from Options import Choice, Toggle, Range
from BaseClasses import ItemClassification, LocationProgressType, CollectionState
import logging

default_options = ['logic_no_night_tokens_without_suns_song', 'open_forest', 'open_kakariko', 'open_door_of_time',
                   'zora_fountain', 'gerudo_fortress', 'bridge', 'trials', 'owl_drops', 'shopsanity', 'shop_slots',
                   'bombchus_in_logic', 'dungeon_shortcuts', 'dungeon_shortcuts_list', 'mq_dungeons_list',
                   'mq_dungeons_count', 'bridge_stones', 'bridge_medallions', 'bridge_rewards', 'bridge_tokens',
                   'bridge_hearts',  'shuffle_hideoutkeys', 'enhance_map_compass', 'ganon_bosskey_medallions',
                   'ganon_bosskey_stones', 'ganon_bosskey_tokens', 'ganon_bosskey_hearts', 'shopsanity_prices',
                   'tokensanity', 'shuffle_scrubs', 'shuffle_child_trade', 'logic_rules', 'logic_tricks',
                   'shuffle_kokiri_sword', 'shuffle_gerudo_card', 'shuffle_beans', 'shuffle_medigoron_carpet_salesman',
                   'shuffle_frog_song_rupees', 'no_escape_sequence', 'no_guard_stealth', 'no_epona_race',
                   'skip_some_minigame_phases', 'complete_mask_quest', 'useful_cutscenes', 'fast_chests',
                   'fast_bunny_hood', 'plant_beans', 'chicken_count', 'fae_torch_count', 'hint_dist', 'starting_tod',
                   'blue_fire_arrows', 'fix_broken_drops', 'start_with_rupees', 'item_pool_value', 'adult_trade_start',
                   'key_rings', 'key_rings_list', 'sfx_horse_neigh', 'sfx_nightfall',
                   'boomerang_trail_color_outer', 'boomerang_trail_color_inner', ]

set_options = {'starting_age': 'adult', 'shuffle_interior_entrances': 'all', 'spawn_positions': 'adult',
               'shuffle_grotto_entrances': 'on', 'shuffle_dungeon_entrances': 'all',
               'hints': 'none', 'triforce_hunt': 'on', 'triforce_goal': 1, 'extra_triforce_percentage': 1,
               'shuffle_pots': "all", 'shuffle_crates': "all", 'shuffle_cows': "on", 'shuffle_beehives': "on",
               'shuffle_ocarinas': "on", 'shuffle_freestanding_items': "all", 'shuffle_song_items': "any",
               "mq_dungeons_mode": "mq", 'misc_hints': "off", 'free_scarecrow': 'on', 'big_poe_count': 4,
               'ganon_bosskey_rewards': 2, 'shuffle_ganon_bosskey': "dungeons", 'warp_songs': 'on',
               'shuffle_mapcompass': 'keysanity', 'shuffle_smallkeys': 'keysanity', 'shuffle_bosskeys': 'keysanity',
               'junk_ice_traps': 'off', 'ice_trap_appearance': 'anything', 'shuffle_overworld_entrances': 'on',
               'shuffle_bosses': 'full'}

warp_song_connectors = [
    "Nocturne of Shadow Warp -> Graveyard Warp Pad Region", "Minuet of Forest Warp -> Sacred Forest Meadow",
    'Bolero of Fire Warp -> DMC Central Local', 'Serenade of Water Warp -> Lake Hylia',
    'Requiem of Spirit Warp -> Desert Colossus', 'Prelude of Light Warp -> Temple of Time'
]

warp_song_destinations = [
    'LH Fishing Island -> LH Fishing Hole', 'Lon Lon Ranch -> LLR Stables', 'Lake Hylia -> LH Lab',
    'Graveyard -> Graveyard Heart Piece Grave', 'Kakariko Village -> Kak House of Skulltula'
]

connections = [
    ('LH Fishing Hole -> LH Fishing Island', "Lake Hylia -> Water Temple Lobby"),
    ("Market Guard House -> Market Entrance", "Lake Hylia -> Water Temple Lobby"),
    ("Kak House of Skulltula -> Kakariko Village", "Lake Hylia -> Water Temple Lobby"),
    ('LLR Stables -> Lon Lon Ranch', "Lake Hylia -> Water Temple Lobby"),
    ('LH Lab -> Lake Hylia', "Lake Hylia -> Water Temple Lobby"),
    ('Graveyard Heart Piece Grave -> Graveyard', "Lake Hylia -> Water Temple Lobby"),
    ('KF Midos House -> Kokiri Forest', "Lake Hylia -> Water Temple Lobby")
]

boss_rooms = {
    "queen_gohma": ("Deku Tree Boss Door -> Queen Gohma Boss Room", "Queen Gohma Boss Room -> Deku Tree Boss Door"),
    "king_dodongo": ("Dodongos Cavern Boss Door -> King Dodongo Boss Room", "King Dodongo Boss Room -> Dodongos Cavern Boss Door"),
    "phantom_ganon": ("Forest Temple Boss Door -> Phantom Ganon Boss Room", "Phantom Ganon Boss Room -> Forest Temple Boss Door"),
    "volvagia": ("Fire Temple Boss Door -> Volvagia Boss Room", "Volvagia Boss Room -> Fire Temple Boss Door"),
    "morpha": ("Water Temple Boss Door -> Morpha Boss Room", "Morpha Boss Room -> Water Temple Boss Door"),
    "twinrova": ("Spirit Temple Boss Door -> Twinrova Boss Room", "Twinrova Boss Room -> Spirit Temple Boss Door"),
    "bongo_bongo": ("Shadow Temple Boss Door -> Bongo Bongo Boss Room", "Bongo Bongo Boss Room -> Shadow Temple Boss Door"),

}

option_pool_size = ((136, 149), (128, 145))

always_pool = ["Progressive Hookshot", "Magic Meter", "Ocarina", "Small Key (Water Temple)", "Progressive Scale"] * 2
always_pool += ["Progressive Strength Upgrade"] * 3
always_pool += ["Song of Time", "Zeldas Lullaby", "Fire Arrows", "Bow", "Ice Arrows", "Light Arrows",
                "Bomb Bag", "Double Defense", "Dins Fire", 'Megaton Hammer', "Lens of Truth",
                "Biggoron Sword", "Hover Boots", "Nayrus Love", "Farores Wind",  "Map (Water Temple)",
                "Compass (Water Temple)", "Goron Tunic", "Deku Nut Capacity", "Hylian Shield", "Mirror Shield"]

filler = ["Hylian Shield", "Ice Arrows", "Light Arrows"]

final_clears = ['Skull Mask from Market Mask Shop', 'Mask of Truth from Market Mask Shop', 'Queen Gohma',
                'King Dodongo', 'Barinade', 'Phantom Ganon', 'Morpha', 'Volvagia', 'Bongo Bongo', 'Twinrova',
                'Forest Trial Clear from Ganons Castle Forest Trial Ending',
                'Water Trial Clear from Ganons Castle Water Trial Ending',
                'Shadow Trial Clear from Ganons Castle Shadow Trial Ending',
                'Fire Trial Clear from Ganons Castle Fire Trial',
                'Light Trial Clear from Ganons Castle Light Trial Ending',
                'Spirit Trial Clear from Ganons Castle Spirit Trial Ending',
                'Water Temple Clear from Morpha Boss Room']


class StartMode(Choice):
    """Determines how, if at all, you can reach sphere 1 locations.
    iron_boots starts you with Iron Boots and, if fewer_tunic_requirements is off, Zora Tunic.
    guard_house starts you in the Market Guard House with 7 pots to open. If warp_songs is off, you can return
    to the Guard House by exiting the Water Temple into the Gold Skulltula House, then exiting it..
    burger_king starts you with nothing. No sphere 1 for you. We'll break all the rules. I won't tell if you won't.
    If every player in the multiworld has burger_king selected, one player will be changed to guard_house."""
    option_burger_king = 0
    option_iron_boots = 1
    option_guard_house = 2
    default = 2


class WarpSongs(Toggle):
    """Shuffle warp songs into the item pool, which will take you to various locations for some additional location
    checks. If this is on, you will need a warp song to access the Skulltula House. If it's off, you can access it
    by exiting the Water Temple."""
    display_name = "Warp Songs"
    default = 1


class BossKeyOption(Choice):
    """Where your Boss Key (Water Temple) may be found. Note that if you do not place it at a Skulltula reward location,
    your game may end up being over with very quickly. If a Skulltula reward location is chosen, rewards beyond the one
    chosen will be guaranteed to contain filler items."""
    display_name = "Boss Key Location"
    option_anywhere = 0
    option_own_game = 1
    option_10_skulltulas_reward = 2
    option_20_skulltulas_reward = 3
    option_30_skulltulas_reward = 4
    option_40_skulltulas_reward = 5
    option_50_skulltulas_reward = 6
    default = 4


class Boss(Choice):
    """Select which boss you will fight at the end of the dungeon."""
    option_queen_gohma = 0
    option_king_dodongo = 1
    option_phantom_ganon = 2
    option_volvagia = 3
    option_morpha = 4
    option_twinrova = 5
    option_bongo_bongo = 6
    default = 4


class TokensInPool(Range):
    """Number of Gold Skulltula Tokens in the item pool. A minimum may be enforced by your boss key location setting."""
    display_name = "Tokens in Pool"
    range_start = 10
    range_end = 70
    default = 50


class LocalTokens(Toggle):
    """This will place Gold Skulltula Tokens into local_items, so you don't have to do it manually by typing out the
    whole name of the item into local_items, because you have more important things to do with your time."""
    display_name = "Local Gold Skulltula Tokens"
    default = 1


class EnableScarecrow(Toggle):
    """Enable the Scarecrow to be spawned by using your Ocarina."""
    default = 1
    display_name = "Enable Scarecrow"


class MaxHealth(Range):
    """What maximum hearts will be obtainable."""
    range_start = 3
    range_end = 20
    default = 12


class LogicFewerTunicRequirements(Toggle):
    """Enable the "Fewer Tunic Requirements" trick to logic, which may require you to do any and all of Water Temple
    except below the central pillar without Zora Tunic."""
    display_name = "Logic: Fewer Tunic Requirements"


class LogicWaterDragonJumpDive(Toggle):
    """Enable the "Water Temple Dragon Statue Jump Dive" trick into logic, which may require you to reach the submerged
    tunnel in the dragon statue room without Scales or Iron Boots using momentum from your fall from above."""
    display_name = "Logic: Water Temple Dragon Statue Jump Dive"


class LogicWaterTempleNorthBasementLedgewWithPreciseJump(Toggle):
    """Enable the "Water Temple North Basement Ledge with Precise Jump" trick to logic, which may require a precise jump
    in the northern basement to reach the ledge without hover boots or scarecrow."""
    display_name = "Logic: Water Temple North Basement Ledge with Precise Jump"


class LogicWaterMQCentralPillarWithFireArrows(Toggle):
    """Enable the "Water Temple MQ Central Pillar with Fire Arrows" trick to logic, which may require you to light the
    torches in the Central Pillar with Fire Arrows."""
    display_name = "Logic: Water Temple MQ Central Pillar with Fire Arrows"


class LogicWaterTempleMQNorthBasementGSWithoutSmallKey(Toggle):
    """Enable the "Water Temple MQ North Basement GS Without Small Key" trick to logic, which may require hookshotting an
    invisible hookshot target to get over the gate to the basement GS, skipping the locked door."""
    display_name = "Logic: Water Temple MQ North Basement GS without Small Key"


class LogicLakeHyliaLabDive(Toggle):
    """Enable the "Lake Hylia Lab Dive without Gold Scale" trick to logic, which may require removing the Iron Boots in
    the midst of hookshotting the crate, to trick the scientist into thinking you're a great swimmer.
    Only relevant if shuffle_warp_songs is on."""
    display_name = "Logic: Lake Hylia Lab Dive without Gold Scale"


class LogicBongoBongoWithoutLensOfTruth(Toggle):
    """Enable the "Shadow Temple Bongo Bongo without Lens of Truth" trick to logic."""
    display_name = "Logic: Shadow Temple Bongo Bongo without Lens of Truth"


class LogicDodongosCavernSmashtheBossLobbyFloor(Toggle):
    """Enable the "Dodongo's Cavern Smash the Boss Lobby Floor" trick to logic. The bombable floor before King Dodongo
    can be destroyed with Hammer if hit in the very center."""
    display_name = "Logic: Dodongo's Cavern Smash the Boss Lobby Floor"


def init_mixin(self, parent):
    oot_ids = (parent.get_game_players(OOTWorld.game) + parent.get_game_groups(OOTWorld.game)
               + parent.get_game_players(OOTBIJMQWTWorld.game) + parent.get_game_groups(OOTBIJMQWTWorld.game))
    self.child_reachable_regions = {player: set() for player in oot_ids}
    self.adult_reachable_regions = {player: set() for player in oot_ids}
    self.child_blocked_connections = {player: set() for player in oot_ids}
    self.adult_blocked_connections = {player: set() for player in oot_ids}
    self.day_reachable_regions = {player: set() for player in oot_ids}
    self.dampe_reachable_regions = {player: set() for player in oot_ids}
    self.age = {player: None for player in oot_ids}


for i, function in enumerate(CollectionState.additional_init_functions):
    if function == OOTCollectionState.init_mixin:
        CollectionState.additional_init_functions[i] = init_mixin
        break
else:
    raise Exception("OOTBIJMQWT failed to inject CollectionState init_mixin function")


class OOTBIJMQWTWorld(OOTWorld):
    game: str = "Ocarina of Time but it's just Master Quest Water Temple"
    oot_options = OOTWorld.option_definitions.copy()
    for option in (default_options + list(set_options.keys())):
        del oot_options[option]
    option_definitions = {"start_mode": StartMode, "shuffle_warp_songs": WarpSongs, "boss": Boss,
                          "boss_key_location": BossKeyOption, "tokens_in_pool": TokensInPool,
                          "local_tokens": LocalTokens, "enable_scarecrow": EnableScarecrow, "max_health": MaxHealth,
                          "logic_fewer_tunic_requirements": LogicFewerTunicRequirements,
                          "logic_water_mq_central_pillar": LogicWaterMQCentralPillarWithFireArrows,
                          "logic_water_mq_locked_gs": LogicWaterTempleMQNorthBasementGSWithoutSmallKey,
                          "logic_lab_diving": LogicLakeHyliaLabDive,
                          "logic_water_dragon_jump_dive": LogicWaterDragonJumpDive,
                          "logic_water_north_basement_ledge_jump": LogicWaterTempleNorthBasementLedgewWithPreciseJump,
                          "logic_dc_hammer_floor": LogicDodongosCavernSmashtheBossLobbyFloor,
                          "logic_lens_bongo": LogicBongoBongoWithoutLensOfTruth,
                          **oot_options}

    topology_present: bool = False
    item_name_to_id = OOTWorld.item_name_to_id
    location_name_to_id = OOTWorld.location_name_to_id
    web = OOTWorld.web

    required_client_version = OOTWorld.required_client_version

    item_name_groups = OOTWorld.item_name_groups

    @classmethod
    def stage_assert_generate(cls, multiworld):
        setattr(multiworld, "mix_entrance_pools", {})
        if len(multiworld.start_mode) == multiworld.players:
            # every player is playing OOTBIJMQWT
            options = set(multiworld.start_mode.values())
            if len(options) == 1 and list(multiworld.start_mode.values())[0] == "burger_king":
                # every player has the same option and first player has bk start = every player has bk start
                multiworld.random.choice(list(multiworld.start_mode.values())).value = 2
                logging.warning("Every player has burger_king start, changing one to guard_house")
        for world in multiworld.get_game_worlds("Ocarina of Time but it's just Master Quest Water Temple"):
            multiworld.worlds[world.player].game = "Ocarina of Time"
            multiworld.game[world.player] = "Ocarina of Time"
            for option in default_options:
                try:
                    optiondict = getattr(multiworld, option)
                except AttributeError:
                    optiondict = {}
                    setattr(multiworld, option, optiondict)
                optionobj = OOTWorld.option_definitions[option]
                optiondict[world.player] = optionobj(optionobj.default)
            for option in set_options.keys():
                try:
                    optiondict = getattr(multiworld, option)
                except AttributeError:
                    optiondict = {}
                    setattr(multiworld, option, optiondict)
                optionobj = OOTWorld.option_definitions[option]
                optiondict[world.player] = optionobj(optionobj.from_any(set_options[option]))
                if isinstance(set_options[option], int):
                    optiondict[world.player].value = set_options[option]

            if multiworld.local_tokens[world.player]:
                multiworld.local_items[world.player].value.add("Gold Skulltula Token")
            if multiworld.boss_key_location[world.player] == "own_game":
                multiworld.local_items[world.player].value.add("Boss Key (Water Temple)")
            multiworld.free_scarecrow[world.player].value = multiworld.enable_scarecrow[world.player].value
            for trick in ["logic_fewer_tunic_requirements", "logic_water_mq_central_pillar", "logic_water_mq_locked_gs",
                          "logic_lab_diving", "logic_water_dragon_jump_dive", "logic_water_north_basement_ledge_jump",
                          "logic_dc_hammer_floor", "logic_lens_bongo"]:
                if getattr(multiworld, trick)[world.player]:
                    multiworld.logic_tricks[world.player].value.append(getattr(multiworld, trick)[world.player].display_name.split(": ")[1].casefold())

    def create_items(self):
        set_drop_location_names(self)

        item_pool = always_pool.copy()

        self.pre_fill_items = []

        if self.multiworld.shuffle_warp_songs[self.player]:
            item_pool += ["Prelude of Light", "Serenade of Water", "Bolero of Fire", "Nocturne of Shadow",
                          "Requiem of Spirit", "Minuet of Forest", "Eponas Song", "Suns Song"]
        if self.multiworld.start_mode[self.player] != "guard_house" and not self.multiworld.shuffle_warp_songs[self.player]:
            # there is no guard house, no use for big poes
            item_pool += ["Bottle with Red Potion", "Bottle with Green Potion", "Bottle with Blue Potion",
                          "Bottle with Fairy"]
        else:
            item_pool += ["Bottle with Big Poe"] * 4

        token_count = max(self.multiworld.tokens_in_pool[self.player].value,
                          [0, 0, 10, 20, 30, 40, 50][self.multiworld.boss_key_location[self.player]])
        item_pool += ["Gold Skulltula Token"] * token_count

        pool_size = option_pool_size[
            self.multiworld.start_mode[self.player] != "guard_house"][self.multiworld.shuffle_warp_songs[self.player].value]

        if self.multiworld.boss_key_location[self.player] < 2:
            item_pool.append("Boss Key (Water Temple)")
        else:
            pool_size -= 1
            r = self.multiworld.boss_key_location[self.player].value * 10
            for i in range(r, 50, 10):
                self.multiworld.get_location(f"Kak {i} Gold Skulltula Reward", self.player).progress_type = LocationProgressType.EXCLUDED

        if self.multiworld.start_mode[self.player] == "iron_boots":
            self.multiworld.push_precollected(self.create_item("Iron Boots"))
            if "fewer tunic requirements" not in self.multiworld.logic_tricks[self.player]:
                self.multiworld.push_precollected(self.create_item("Zora Tunic"))
            else:
                item_pool.append("Zora Tunic")
        else:
            item_pool.append("Iron Boots")
            item_pool.append("Zora Tunic")

        for i in (20, 30, 40, 50):
            if token_count < i:
                pool_size -= 1

        heart_piece_sets = min(int((pool_size - (len(item_pool) + self.multiworld.max_health[self.player].value)) / 3),
                               self.multiworld.max_health[self.player].value)

        item_pool += ["Heart Container"] * (self.multiworld.max_health[self.player].value - heart_piece_sets)
        item_pool += ["Piece of Heart"] * 4 * heart_piece_sets

        extrapool = ["Bombchus (20)", 'Arrows (30)', "Bombchus (10)", 'Arrows (10)', "Bombs (10)", "Bombs (20)",
                     'Deku Nuts (5)', 'Deku Nuts (10)', 'Recovery Heart', 'Arrows (5)',  "Bombs (5)", "Bombchus (5)",
                     'Ice Trap']

        boss = self.multiworld.boss[self.player].current_key
        if boss == "king_dodongo":
            pool_size += 1

        while len(item_pool) < pool_size:
            item_pool += self.multiworld.random.sample(extrapool, min(pool_size - len(item_pool), len(extrapool)))

        for item in self.multiworld.precollected_items[self.player]:
            self.starting_items[item.name] += 1
        if self.start_with_consumables:
            self.starting_items['Deku Nuts'] = 40

        self.itempool = []
        for item_name in item_pool:
            item = self.create_item(item_name)
            if item_name in filler:
                item.classification = ItemClassification.filler
            self.itempool.append(item)
        self.multiworld.itempool += self.itempool
        for boss in ['Queen Gohma', 'King Dodongo', 'Barinade', 'Phantom Ganon', 'Morpha', 'Volvagia', 'Bongo Bongo',
                     'Twinrova', 'Links Pocket']:
            loc = self.multiworld.get_location(boss, self.player)
            loc.place_locked_item(self.multiworld.create_item(loc.vanilla_item, self.player))

    def pre_fill(self):
        pass

    def set_rules(self):
        multiworld = self.multiworld
        world = self
        from worlds.oot.EntranceShuffle import set_all_entrances_data
        from worlds.oot.Rules import set_rules, set_entrances_based_rules
        set_all_entrances_data(multiworld, self.player)
        entrances = self.get_shufflable_entrances()
        for entrance in entrances:
            if entrance.data:
                entrance.shuffled = True
                entrance.replaces = entrance
        set_rules(self)

        boss_room_door = boss_rooms[self.multiworld.boss[self.player].current_key]

        c1, c2 = world.get_entrance("Water Temple Boss Door -> Morpha Boss Room"), \
            world.get_entrance(boss_room_door[0])
        c1.connect(world.get_region(c2.vanilla_connected_region))
        c1.replaces = c2
        c1, c2 = world.get_entrance(boss_room_door[1]), \
            world.get_entrance("Morpha Boss Room -> Water Temple Boss Door")
        c1.connect(world.get_region(c2.vanilla_connected_region))
        c1.replaces = c2

        for connection in connections:
            c1, c2 = world.get_entrance(connection[0]), world.get_entrance(connection[1])
            c1.connect(world.get_region(c2.vanilla_connected_region))
            c1.replaces = c2
        if multiworld.shuffle_warp_songs[world.player]:
            connectors = warp_song_connectors.copy()
            multiworld.random.shuffle(connectors)
            destinations = warp_song_destinations.copy()
            if multiworld.start_mode[world.player] != "guard_house":
                destinations.append("Market Entrance -> Market Guard House")
                c1, c2 = world.get_entrance("Water Temple Lobby -> Lake Hylia"), \
                         world.get_entrance("Lake Hylia -> Water Temple Lobby")
                c1.connect(world.get_region(c2.vanilla_connected_region))
                c1.replaces = c2
            else:
                destinations.append("Kokiri Forest -> KF Midos House")
                c1, c2 = world.get_entrance("Water Temple Lobby -> Lake Hylia"), \
                         world.get_entrance("Market Entrance -> Market Guard House")
                c1.connect(world.get_region(c2.vanilla_connected_region))
                c1.replaces = c2
            for connection, destination in zip(connectors, destinations):
                c1, c2 = world.get_entrance(connection), world.get_entrance(destination)
                c1.connect(world.get_region(c2.vanilla_connected_region))
                c1.replaces = c2
        else:
            c1, c2 = world.get_entrance("Water Temple Lobby -> Lake Hylia"), \
                     world.get_entrance("Kakariko Village -> Kak House of Skulltula")
            c1.connect(world.get_region(c2.vanilla_connected_region))
            c1.replaces = c2
            if self.multiworld.start_mode[self.player] == "guard_house":
                c1, c2 = world.get_entrance("Kak House of Skulltula -> Kakariko Village"), \
                    world.get_entrance("Market Entrance -> Market Guard House")
                c1.connect(world.get_region(c2.vanilla_connected_region))
                c1.replaces = c2
        if multiworld.start_mode[world.player] != "guard_house":
            c1, c2 = world.get_entrance("Adult Spawn -> Temple of Time"), \
                     world.get_entrance("Lake Hylia -> Water Temple Lobby")
            c1.connect(world.get_region(c2.vanilla_connected_region))
            c1.replaces = c2
        else:
            c1, c2 = world.get_entrance("Adult Spawn -> Temple of Time"), \
                     world.get_entrance("Market Entrance -> Market Guard House")
            c1.connect(world.get_region(c2.vanilla_connected_region))
            c1.replaces = c2

        if multiworld.start_mode[world.player] != "iron_boots":
            if multiworld.boss_key_location[world.player].value < 2 or multiworld.random.randint(0, 7) < 5:
                multiworld.early_items[world.player]["Iron Boots"] = 1
                if "fewer tunic requirements" in multiworld.logic_tricks[world.player]:
                    multiworld.early_items[world.player]["Zora Tunic"] = 1
            else:
                multiworld.early_items[world.player]["Progressive Hookshot"] = 2
                multiworld.early_items[world.player]["Small Key (Water Temple)"] = 1

    def get_entrance(self, entrance):
        return self.multiworld.get_entrance(entrance, self.player)

    def extend_hint_information(self, er_hint_data: dict):
        er_hint_data[self.player] = {}
        if self.multiworld.shuffle_warp_songs[self.player]:
            for entrance in [self.multiworld.get_entrance(entrance, self.player) for entrance in warp_song_connectors]:
                for location in entrance.connected_region.locations:
                    if type(location.address) == int:
                        er_hint_data[self.player][location.address] = entrance.name.split(" -> ")[0]

    @classmethod
    def stage_fill_hook(cls, multiworld, progitempool, usefulitempool, filleritempool, fill_locations):
        wtplayerids = [world.player for world in
                       multiworld.get_game_worlds("Ocarina of Time but it's just Master Quest Water Temple")]
        state = multiworld.get_all_state(False)
        for player in wtplayerids:
            state.collect(multiworld.worlds[player].create_item("Boss Key (Water Temple)"))
            for location in [multiworld.get_location(loc, player) for loc in final_clears
                             if loc != multiworld.boss[player].current_key.replace("_", " ").title()]:
                if location.item is None:
                    location.place_locked_item(multiworld.worlds[location.player].create_item(location.vanilla_item))
                location.item.classification = ItemClassification.filler
                location.event = False
        for location in reversed(fill_locations):
            if location.player in wtplayerids:
                if location.name == "Gift from Sages":
                    location.item = None
                    location.place_locked_item(multiworld.worlds[location.player].create_item("Triforce Piece"))
                    fill_locations.remove(location)
                elif location.name == f"Kak {multiworld.boss_key_location[location.player].current_key.split('_')[0]} Gold Skulltula Reward":
                    location.place_locked_item(multiworld.worlds[location.player].create_item("Boss Key (Water Temple)"))
                    fill_locations.remove(location)
                elif not state.can_reach(location):
                    if not location.item:
                        location.place_locked_item(multiworld.worlds[location.player].create_item(location.vanilla_item))
                    location.progress_type = LocationProgressType.EXCLUDED
                    location.item.classification = ItemClassification.filler
                    location.address = None
                    location.event = False
                    location.show_in_spoiler = False
                    location.price = 1
                    fill_locations.remove(location)
                elif location.type == "Drop":
                    location.place_locked_item(multiworld.worlds[location.player].create_item(location.vanilla_item))
                    location.show_in_spoiler = False
                    fill_locations.remove(location)

        # this is to prevent the early spheres from being filled with tokens which had caused some generation failures
        progitempool.sort(key=lambda i: i.name == "Gold Skulltula Token")

    @classmethod
    def stage_generate_early(cls, multiworld):
        for world in multiworld.get_game_worlds("Ocarina of Time but it's just Master Quest Water Temple"):
            # this gets undone because of the triforce setting, it's needed to be "dungeons" so that gift from sages
            # is not disabled.
            multiworld.worlds[world.player].shuffle_ganon_bosskey = "dungeons"
