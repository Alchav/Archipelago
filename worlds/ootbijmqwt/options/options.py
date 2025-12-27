from Options import Visibility
from worlds.oot.Options import *


class FakeChoice(Choice):
    visibility = Visibility.none

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return other.value == self.value
        elif isinstance(other, str):
            return other == self.current_key
        elif isinstance(other, int):
            return other == self.value
        elif isinstance(other, bool):
            return other == bool(self.value)
        else:
            raise TypeError(f"Can't compare {self.__class__.__name__} with {other.__class__.__name__}")

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return other.value != self.value
        elif isinstance(other, str):
            return other != self.current_key
        elif isinstance(other, int):
            return other != self.value
        elif isinstance(other, bool):
            return other != bool(self.value)
        elif other is None:
            return False
        else:
            raise TypeError(f"Can't compare {self.__class__.__name__} with {other.__class__.__name__}")

    def __lt__(self, other: typing.Union[Choice, int, str]):
        if isinstance(other, str):
            other = self.options[other]
        return super(Choice, self).__lt__(other)

    def __gt__(self, other: typing.Union[Choice, int, str]):
        if isinstance(other, str):
            other = self.options[other]
        return super(Choice, self).__gt__(other)

    def __le__(self, other: typing.Union[Choice, int, str]):
        if isinstance(other, str):
            other = self.options[other]
        return super(Choice, self).__le__(other)

    def __ge__(self, other: typing.Union[Choice, int, str]):
        if isinstance(other, str):
            other = self.options[other]
        return super(Choice, self).__ge__(other)


class StartMode(Choice):
    """Determines how, if at all, you can reach sphere 1 locations.
    iron_boots starts you with Iron Boots and, if fewer_tunic_requirements is off, Zora Tunic.
    guard_house starts you in the Market Guard House with 7 pots to open. If warp_songs is off, you can return
    to the Guard House by exiting the Water Temple into the Gold Skulltula House, then exiting it.
    burger_king starts you with nothing. No sphere 1 for you. We'll break all the rules. I won't tell if you won't.
    If every player in the multiworld has burger_king selected, one player may be changed to guard_house."""
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


class MQAccessibility(Choice):
    """
    Set rules for reachability of your items/locations.

    **Minimal:** ensure what is needed to reach your goal can be acquired.

    **Items:** ensure all logically relevant items can be acquired.
    """
    display_name = "Accessibility"
    rich_text_doc = True
    option_items = 1
    option_minimal = 2
    alias_none = 2
    alias_locations = 1
    default = 1


class Logic(FakeChoice):
    option_glitchless = 0
    visibility = Visibility.none


class NightTokens(Toggle):
    visibility = Visibility.none


class Forest(FakeChoice):
    option_open = 0
    visibility = Visibility.none


class Gate(FakeChoice):
    visibility = Visibility.none
    option_open = 0


class DoorOfTime(DefaultOnToggle):
    visibility = Visibility.none


class Fountain(FakeChoice):
    option_closed = 0


class Fortress(FakeChoice):
    option_fast = 1
    default = 1


class Bridge(FakeChoice):
    option_open = 0


class Trials(Range):
    randomized = False
    visibility = Visibility.none
    range_start = 0
    range_end = 6


class StartingAge(FakeChoice):
    option_adult = 1
    default = 1


class InteriorEntrances(FakeChoice):
    # option_all = 2
    default = 0
    option_off = 0


class GrottoEntrances(Toggle):
    default = 1
    visibility = Visibility.none


class DungeonEntrances(FakeChoice):
    option_all = 2
    default = 2


class BossEntrances(FakeChoice):
    option_full = 2
    default = 2


class OverworldEntrances(Toggle):
    visibility = Visibility.none
    default = 1


class OwlDrops(Toggle):
    visibility = Visibility.none
    default = 1


class SpawnPositions(FakeChoice):
    visibility = Visibility.none
    option_both = 3
    default = 3


class TriforceHunt(Toggle):
    visibility = Visibility.none
    default = 1


class TriforceGoal(Range):
    visibility = Visibility.none
    range_start = 1
    range_end = 1
    default = 1


class ExtraTriforces(Range):
    range_start = 0
    range_end = 0
    default = 0
    visibility = Visibility.none


class LogicalChus(Toggle):
    visibility = Visibility.none


class DungeonShortcuts(FakeChoice):
    option_off = 0
    visibility = Visibility.none


class DungeonShortcutsList(OptionSet):
    visibility = Visibility.none


class MQDungeons(FakeChoice):
    visibility = Visibility.none
    option_mq = 1
    default = 1


class MQDungeonList(OptionSet):
    visibility = Visibility.none
    default = {"Water Temple"}


class MQDungeonCount(Range):
    randomized = False
    range_start = 0
    range_end = 0
    default = 0
    visibility = Visibility.none


class BridgeStones(Range):

    visibility = Visibility.none
    range_end = 0
    range_start = 0


class BridgeMedallions(Range):
    visibility = Visibility.none
    range_start = 0
    range_end = 0


class BridgeRewards(Range):
    visibility = Visibility.none
    range_start = 0
    range_end = 0
    default = 0


class BridgeTokens(Range):
    visibility = Visibility.none
    range_start = 0
    range_end = 0
    default = 0


class BridgeHearts(Range):
    visibility = Visibility.none
    range_start = 0
    range_end = 0
    default = 0


class SongShuffle(FakeChoice):
    visibility = Visibility.none
    option_any = 2
    default = 2


class ShopShuffle(FakeChoice):
    visibility = Visibility.none
    option_off = 0


class ShopSlots(Range):
    visibility = Visibility.none
    range_start = 0
    range_end = 0


class ShopPrices(FakeChoice):
    visibility = Visibility.none
    option_normal = 0


class TokenShuffle(FakeChoice):
    visibility = Visibility.none
    option_all = 3
    default = 3


class ScrubShuffle(FakeChoice):
    visibility = Visibility.none
    option_off = 0


class ShuffleCows(Toggle):
    visibility = Visibility.none
    default = 1


class ShuffleSword(Toggle):
    visibility = Visibility.none


class ShuffleOcarinas(Toggle):
    visibility = Visibility.none
    default = 1


class ShuffleChildTrade(FakeChoice):
    visibility = Visibility.none
    option_vanilla = 0


class ShuffleCard(Toggle):
    visibility = Visibility.none


class ShuffleBeans(Toggle):
    visibility = Visibility.none


class ShuffleMedigoronCarpet(Toggle):
    visibility = Visibility.none


class ShuffleFreestanding(FakeChoice):
    visibility = Visibility.none
    option_all = 3
    default = 3


class ShufflePots(FakeChoice):
    visibility = Visibility.none
    option_all = 3
    default = 3


class ShuffleCrates(FakeChoice):
    visibility = Visibility.none
    option_all = 3
    default = 3


class ShuffleBeehives(Toggle):
    visibility = Visibility.none


class ShuffleFrogRupees(Toggle):
    visibility = Visibility.none


class ShuffleMapCompass(FakeChoice):
    visibility = Visibility.none
    option_keysanity = 7
    default = 7
    alias_anywhere = 7


class ShuffleKeys(FakeChoice):
    visibility = Visibility.none
    option_keysanity = 7
    default = 7
    alias_anywhere = 7


class ShuffleGerudoKeys(FakeChoice):
    visibility = Visibility.none
    option_keysanity = 4
    alias_anywhere = 4
    default = 4


class ShuffleBossKeys(FakeChoice):
    visibility = Visibility.none
    option_keysanity = 7
    default = 7


class ShuffleGanonBK(FakeChoice):
    visibility = Visibility.none
    option_dungeons = 11
    default = 11


class EnhanceMC(Toggle):
    visibility = Visibility.none
    default = 1


class GanonBKMedallions(Range):
    visibility = Visibility.none
    range_start = 1
    range_end = 1
    default = 1


class GanonBKStones(Range):
    visibility = Visibility.none
    range_start = 1
    range_end = 1
    default = 1


class GanonBKRewards(Range):
    visibility = Visibility.none
    range_start = 2
    range_end = 2
    default = 2


class GanonBKTokens(Range):
    visibility = Visibility.none
    range_start = 1
    range_end = 1
    default = 1


class GanonBKHearts(Range):
    visibility = Visibility.none
    range_start = 1
    range_end = 1
    default = 1


class KeyRings(FakeChoice):
    visibility = Visibility.none
    option_off = 0


class KeyRingList(OptionSet):
    visibility = Visibility.none
    valid_keys = {
        "Thieves' Hideout",
        "Forest Temple",
        "Fire Temple",
        "Water Temple",
        "Shadow Temple",
        "Spirit Temple",
        "Bottom of the Well",
        "Gerudo Training Ground",
        "Ganon's Castle"
    }


class SkipEscape(DefaultOnToggle):
    visibility = Visibility.none


class SkipStealth(DefaultOnToggle):
    visibility = Visibility.none


class SkipEponaRace(DefaultOnToggle):
    visibility = Visibility.none


class SkipMinigamePhases(DefaultOnToggle):
    visibility = Visibility.none


class CompleteMaskQuest(Toggle):
    visibility = Visibility.none


class UsefulCutscenes(Toggle):
    visibility = Visibility.none


class FreeScarecrow(Toggle):
    visibility = Visibility.none
    default = 1


class FastBunny(Toggle):
    visibility = Visibility.none


class PlantBeans(Toggle):
    visibility = Visibility.none


class ChickenCount(Range):
    visibility = Visibility.none
    range_start = 0
    range_end = 0
    default = 0


class BigPoeCount(Range):
    visibility = Visibility.none
    range_start = 1
    range_end = 1
    default = 1


class FAETorchCount(Range):
    visibility = Visibility.none
    range_start = 1
    range_end = 1
    default = 1


class InvisibleChests(Toggle):
    visibility = Visibility.none


class Hints(FakeChoice):
    option_none = 0
    visibility = Visibility.none


class MiscHints(DefaultOnToggle):
    visibility = Visibility.none


class HintDistribution(FakeChoice):
    visibility = Visibility.none
    option_async = 9
    default = 9


class StartingToD(FakeChoice):
    visibility = Visibility.none
    option_default = 0


class BlueFireArrows(Toggle):
    visibility = Visibility.none


class FixBrokenDrops(Toggle):
    visibility = Visibility.none


class RupeeStart(Toggle):
    visibility = Visibility.none


class ItemPoolValue(FakeChoice):
    option_balanced = 1
    default = 1


class IceTraps(FakeChoice):
    option_off = 0


class AdultTradeStart(FakeChoice):
    option_claim_check = 9
    default = 9


class LogicTricks(OptionSet):
    display_name = "Logic Tricks"
    visibility = Visibility.none


class OoTPlandoConnections(PlandoConnections):
    entrances = set([connection[1][0] for connection in entrance_shuffle_table])
    exits = set([connection[2][0] for connection in entrance_shuffle_table if len(connection) > 2])
    visibility = Visibility.none


class boomerang_trail_color_inner(FakeChoice):
    option_yellow = 3
    default = 3


class boomerang_trail_color_outer(FakeChoice):

    option_match_inner = 13
    default = 13


class DeadlyBonks(DeadlyBonks):
    """Bonking on a wall or object will hurt Link. "Normal" is a half heart of damage.
    If Start Mode is set to "Iron Boots" and Deadly Bonks is set to "ohko", you will also start with Nayru's Love and
    a Magic Meter."""


class ConsumableStart(ConsumableStart):
    """Start the game with full Deku Nuts."""


class WarpSongsFake(Toggle):
    default = 1
    visibility = Visibility.none


@dataclass
class OOTBIJMQWTOptions(PerGameCommonOptions):
    start_mode: StartMode
    shuffle_warp_songs: WarpSongs
    boss: Boss
    boss_key_location: BossKeyOption
    tokens_in_pool: TokensInPool
    local_tokens: LocalTokens
    enable_scarecrow: EnableScarecrow
    max_health: MaxHealth
    logic_fewer_tunic_requirements: LogicFewerTunicRequirements
    logic_water_mq_central_pillar: LogicWaterMQCentralPillarWithFireArrows
    logic_water_mq_locked_gs: LogicWaterTempleMQNorthBasementGSWithoutSmallKey
    logic_lab_diving: LogicLakeHyliaLabDive
    logic_water_dragon_jump_dive: LogicWaterDragonJumpDive
    logic_water_north_basement_ledge_jump: LogicWaterTempleNorthBasementLedgewWithPreciseJump
    logic_dc_hammer_floor: LogicDodongosCavernSmashtheBossLobbyFloor
    logic_lens_bongo: LogicBongoBongoWithoutLensOfTruth
    #############################
    plando_connections: OoTPlandoConnections
    death_link: DeathLink
    logic_rules: Logic
    logic_no_night_tokens_without_suns_song: NightTokens
    logic_tricks: LogicTricks
    open_forest: Forest
    open_kakariko: Gate
    open_door_of_time: DoorOfTime
    zora_fountain: Fountain
    gerudo_fortress: Fortress
    bridge: Bridge
    trials: Trials
    starting_age: StartingAge
    shuffle_interior_entrances: InteriorEntrances
    shuffle_grotto_entrances: GrottoEntrances
    shuffle_dungeon_entrances: DungeonEntrances
    shuffle_overworld_entrances: OverworldEntrances
    owl_drops: OwlDrops
    warp_songs: WarpSongsFake
    spawn_positions: SpawnPositions
    shuffle_bosses: BossEntrances
    triforce_hunt: TriforceHunt
    triforce_goal: TriforceGoal
    extra_triforce_percentage: ExtraTriforces
    bombchus_in_logic: LogicalChus
    dungeon_shortcuts: DungeonShortcuts
    dungeon_shortcuts_list: DungeonShortcutsList
    mq_dungeons_mode: MQDungeons
    mq_dungeons_list: MQDungeonList
    mq_dungeons_count: MQDungeonCount
    bridge_stones: BridgeStones
    bridge_medallions: BridgeMedallions
    bridge_rewards: BridgeRewards
    bridge_tokens: BridgeTokens
    bridge_hearts: BridgeHearts
    shuffle_mapcompass: ShuffleMapCompass
    shuffle_smallkeys: ShuffleKeys
    shuffle_hideoutkeys: ShuffleGerudoKeys
    shuffle_bosskeys: ShuffleBossKeys
    enhance_map_compass: EnhanceMC
    shuffle_ganon_bosskey: ShuffleGanonBK
    ganon_bosskey_medallions: GanonBKMedallions
    ganon_bosskey_stones: GanonBKStones
    ganon_bosskey_rewards: GanonBKRewards
    ganon_bosskey_tokens: GanonBKTokens
    ganon_bosskey_hearts: GanonBKHearts
    key_rings: KeyRings
    key_rings_list: KeyRingList
    shuffle_song_items: SongShuffle
    shopsanity: ShopShuffle
    shop_slots: ShopSlots
    shopsanity_prices: ShopPrices
    tokensanity: TokenShuffle
    shuffle_scrubs: ScrubShuffle
    shuffle_child_trade: ShuffleChildTrade
    shuffle_freestanding_items: ShuffleFreestanding
    shuffle_pots: ShufflePots
    shuffle_crates: ShuffleCrates
    shuffle_cows: ShuffleCows
    shuffle_beehives: ShuffleBeehives
    shuffle_kokiri_sword: ShuffleSword
    shuffle_ocarinas: ShuffleOcarinas
    shuffle_gerudo_card: ShuffleCard
    shuffle_beans: ShuffleBeans
    shuffle_medigoron_carpet_salesman: ShuffleMedigoronCarpet
    shuffle_frog_song_rupees: ShuffleFrogRupees
    no_escape_sequence: SkipEscape
    no_guard_stealth: SkipStealth
    no_epona_race: SkipEponaRace
    skip_some_minigame_phases: SkipMinigamePhases
    complete_mask_quest: CompleteMaskQuest
    useful_cutscenes: UsefulCutscenes
    fast_chests: FastChests
    free_scarecrow: FreeScarecrow
    fast_bunny_hood: FastBunny
    plant_beans: PlantBeans
    chicken_count: ChickenCount
    big_poe_count: BigPoeCount
    fae_torch_count: FAETorchCount
    correct_chest_appearances: CorrectChestAppearance
    minor_items_as_major_chest: MinorInMajor
    invisible_chests: InvisibleChests
    correct_potcrate_appearances: CorrectPotCrateAppearance
    hints: Hints
    misc_hints: MiscHints
    hint_dist: HintDistribution
    text_shuffle: TextShuffle
    damage_multiplier: DamageMultiplier
    deadly_bonks: DeadlyBonks
    no_collectible_hearts: HeroMode
    starting_tod: StartingToD
    blue_fire_arrows: BlueFireArrows
    fix_broken_drops: FixBrokenDrops
    start_with_consumables: ConsumableStart
    start_with_rupees: RupeeStart
    item_pool_value: ItemPoolValue
    junk_ice_traps: IceTraps
    ice_trap_appearance: IceTrapVisual
    adult_trade_start: AdultTradeStart
    default_targeting: Targeting
    display_dpad: DisplayDpad
    dpad_dungeon_menu: DpadDungeonMenu
    correct_model_colors: CorrectColors
    background_music: BackgroundMusic
    fanfares: Fanfares
    ocarina_fanfares: OcarinaFanfares
    kokiri_color: kokiri_color
    goron_color:  goron_color
    zora_color:   zora_color
    silver_gauntlets_color:   silver_gauntlets_color
    golden_gauntlets_color:   golden_gauntlets_color
    mirror_shield_frame_color: mirror_shield_frame_color
    navi_color_default_inner: navi_color_default_inner
    navi_color_default_outer: navi_color_default_outer
    navi_color_enemy_inner:   navi_color_enemy_inner
    navi_color_enemy_outer:   navi_color_enemy_outer
    navi_color_npc_inner:     navi_color_npc_inner
    navi_color_npc_outer:     navi_color_npc_outer
    navi_color_prop_inner:    navi_color_prop_inner
    navi_color_prop_outer:    navi_color_prop_outer
    sword_trail_duration: SwordTrailDuration
    sword_trail_color_inner: sword_trail_color_inner
    sword_trail_color_outer: sword_trail_color_outer
    bombchu_trail_color_inner: bombchu_trail_color_inner
    bombchu_trail_color_outer: bombchu_trail_color_outer
    boomerang_trail_color_inner: boomerang_trail_color_inner
    boomerang_trail_color_outer: boomerang_trail_color_outer
    heart_color:          heart_color
    magic_color:          magic_color
    a_button_color:       a_button_color
    b_button_color:       b_button_color
    c_button_color:       c_button_color
    start_button_color:   start_button_color
    sfx_navi_overworld:   sfx_navi_overworld
    sfx_navi_enemy:       sfx_navi_enemy
    sfx_low_hp:           sfx_low_hp
    sfx_menu_cursor:      sfx_menu_cursor
    sfx_menu_select:      sfx_menu_select
    sfx_nightfall:        sfx_nightfall
    sfx_horse_neigh:      sfx_horse_neigh
    sfx_hover_boots:      sfx_hover_boots
    sfx_ocarina:          SfxOcarina
    accessibility:        MQAccessibility

