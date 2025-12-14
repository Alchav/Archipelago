from worlds.oot import OOTWorld, OOTCollectionState, OOTWeb
from worlds.oot.LocationList import set_drop_location_names
from BaseClasses import ItemClassification, LocationProgressType, CollectionState
from settings import get_settings
import logging
from .options.options import OOTBIJMQWTOptions

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


class OOTBIJMQWTWeb(OOTWeb):
    option_groups = []


class OOTBIJMQWTWorld(OOTWorld):
    game: str = "Ocarina of Time but it's just Master Quest Water Temple"

    options_dataclass = OOTBIJMQWTOptions
    topology_present: bool = False
    item_name_to_id = OOTWorld.item_name_to_id
    location_name_to_id = OOTWorld.location_name_to_id
    web = OOTWorld.web

    required_client_version = OOTWorld.required_client_version

    item_name_groups = OOTWorld.item_name_groups

    web = OOTBIJMQWTWeb()

    @classmethod
    def stage_assert_generate(cls, multiworld):
        if get_settings().generator.panic_method != "start_inventory" and set(multiworld.game.values()) == OOTBIJMQWTWorld.game:
            # every player is playing OOTBIJMQWT, panic method is not start inventory
            options = [multiworld.worlds[i].options.start_mode for i in multiworld.player_ids]
            if len(set(options)) == 1 and options[0] == "burger_king":
                # every player has the same option and first player has bk start = every player has bk start
                multiworld.random.choice(options).value = 2
                logging.warning("Every player has burger_king start, changing one to guard_house")
        for world in multiworld.get_game_worlds("Ocarina of Time but it's just Master Quest Water Temple"):
            multiworld.worlds[world.player].game = "Ocarina of Time"
            multiworld.game[world.player] = "Ocarina of Time"
            world = multiworld.worlds[world.player]
            if world.options.local_tokens:
                world.options.local_items.value.add("Gold Skulltula Token")
            if world.options.boss_key_location == "own_game":
                world.options.local_items.value.add("Boss Key (Water Temple)")
            world.options.free_scarecrow.value = world.options.enable_scarecrow.value
            for trick in ["logic_fewer_tunic_requirements", "logic_water_mq_central_pillar", "logic_water_mq_locked_gs",
                          "logic_lab_diving", "logic_water_dragon_jump_dive", "logic_water_north_basement_ledge_jump",
                          "logic_dc_hammer_floor", "logic_lens_bongo"]:
                if getattr(world.options, trick):
                    world.options.logic_tricks.value.add(getattr(world.options, trick).display_name.split(": ")[1].casefold())

    def create_items(self):
        set_drop_location_names(self)

        item_pool = always_pool.copy()

        self.pre_fill_items = []

        if self.options.shuffle_warp_songs:
            item_pool += ["Prelude of Light", "Serenade of Water", "Bolero of Fire", "Nocturne of Shadow",
                          "Requiem of Spirit", "Minuet of Forest", "Eponas Song", "Suns Song"]
        if self.options.start_mode != "guard_house" and not self.options.shuffle_warp_songs:
            # there is no guard house, no use for big poes
            item_pool += ["Bottle with Red Potion", "Bottle with Green Potion", "Bottle with Blue Potion",
                          "Bottle with Fairy"]
        else:
            item_pool += ["Bottle with Big Poe", "Bottle with Blue Potion", "Bottle with Fairy"]
            item_pool.append(self.random.choice(["Bottle with Red Potion", "Bottle with Green Potion"]))

        token_count = max(self.options.tokens_in_pool.value,
                          [0, 0, 10, 20, 30, 40, 50][self.options.boss_key_location])
        item_pool += ["Gold Skulltula Token"] * token_count

        pool_size = option_pool_size[
            self.options.start_mode != "guard_house"][self.options.shuffle_warp_songs.value]

        if self.options.boss_key_location < 2:
            item_pool.append("Boss Key (Water Temple)")
        else:
            pool_size -= 1
            r = self.options.boss_key_location.value * 10
            for i in range(r, 50, 10):
                self.multiworld.get_location(f"Kak {i} Gold Skulltula Reward", self.player).progress_type = LocationProgressType.EXCLUDED

        if self.options.start_mode == "iron_boots":
            self.multiworld.push_precollected(self.create_item("Iron Boots"))
            if "fewer tunic requirements" not in self.options.logic_tricks:
                self.multiworld.push_precollected(self.create_item("Zora Tunic"))
            else:
                item_pool.append("Zora Tunic")
        else:
            item_pool.append("Iron Boots")
            item_pool.append("Zora Tunic")

        for i in (20, 30, 40, 50):
            if token_count < i:
                pool_size -= 1

        heart_piece_sets = min(int((pool_size - (len(item_pool) + self.options.max_health.value)) / 3),
                               self.options.max_health.value)

        item_pool += ["Heart Container"] * (self.options.max_health.value - heart_piece_sets)
        item_pool += ["Piece of Heart"] * 4 * heart_piece_sets

        extrapool = ["Bombchus (20)", 'Arrows (30)', "Bombchus (10)", 'Arrows (10)', "Bombs (10)", "Bombs (20)",
                     'Deku Nuts (5)', 'Deku Nuts (10)', 'Recovery Heart', 'Arrows (5)',  "Bombs (5)", "Bombchus (5)",
                     'Ice Trap']

        boss = self.options.boss.current_key
        if boss == "king_dodongo":
            pool_size += 1

        while len(item_pool) < pool_size:
            item_pool += self.random.sample(extrapool, min(pool_size - len(item_pool), len(extrapool)))

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

        if self.options.warp_songs:
            # ensure access to repeatable money
            multiworld.get_location("LH Adult Fishing", self.player).access_rule = lambda state: state.can_reach("Market Guard House", "Region", self.player)

        boss_room_door = boss_rooms[self.options.boss.current_key]

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
        if self.options.shuffle_warp_songs:
            connectors = warp_song_connectors.copy()
            self.random.shuffle(connectors)
            destinations = warp_song_destinations.copy()
            if self.options.start_mode != "guard_house":
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
            if self.options.start_mode == "guard_house":
                c1, c2 = world.get_entrance("Kak House of Skulltula -> Kakariko Village"), \
                    world.get_entrance("Market Entrance -> Market Guard House")
                c1.connect(world.get_region(c2.vanilla_connected_region))
                c1.replaces = c2
        if self.options.start_mode != "guard_house":
            c1, c2 = world.get_entrance("Adult Spawn -> Temple of Time"), \
                     world.get_entrance("Lake Hylia -> Water Temple Lobby")
            c1.connect(world.get_region(c2.vanilla_connected_region))
            c1.replaces = c2
        else:
            c1, c2 = world.get_entrance("Adult Spawn -> Temple of Time"), \
                     world.get_entrance("Market Entrance -> Market Guard House")
            c1.connect(world.get_region(c2.vanilla_connected_region))
            c1.replaces = c2

        if self.options.start_mode != "iron_boots":
            if self.options.boss_key_location.value < 2 or self.random.randint(0, 7) < 5:
                multiworld.early_items[world.player]["Iron Boots"] = 1
                if "fewer tunic requirements" in self.options.logic_tricks:
                    multiworld.early_items[world.player]["Zora Tunic"] = 1
            else:
                multiworld.early_items[world.player]["Progressive Hookshot"] = 2
                multiworld.early_items[world.player]["Small Key (Water Temple)"] = 1

    def get_entrance(self, entrance):
        return self.multiworld.get_entrance(entrance, self.player)

    def extend_hint_information(self, er_hint_data: dict):
        er_hint_data[self.player] = {}
        if self.options.shuffle_warp_songs:
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
                             if loc != multiworld.worlds[player].options.boss.current_key.replace("_", " ").title()]:
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
                elif location.name == f"Kak {multiworld.worlds[location.player].options.boss_key_location.current_key.split('_')[0]} Gold Skulltula Reward":
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

    def fill_slot_data(self):
        self.collectible_flags_available.wait()

        slot_data = {
            'collectible_override_flags': self.collectible_override_flags,
            'collectible_flag_offsets': self.collectible_flag_offsets
        }
        return slot_data
