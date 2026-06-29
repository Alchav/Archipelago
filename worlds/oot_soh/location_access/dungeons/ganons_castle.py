from ...Enums import GanonsTrials as GanonTrialClears
from ...LogicHelpers import *

if TYPE_CHECKING:
    from ... import SohWorld


class EventLocations(StrEnum):
    GANONS_CASTLE_FREE_FAIRIES = "Ganon's Castle Free Fairies"
    GANONS_CASTLE_FOREST_TRIAL_AREA = "Ganon's Castle Forest Trial Area"
    GANONS_CASTLE_FIRE_TRIAL_AREA = "Ganon's Castle Fire Trial Area"
    GANONS_CASTLE_WATER_TRIAL_AREA = "Ganon's Castle Water Trial Area"
    GANONS_CASTLE_SHADOW_TRIAL_AREA = "Ganon's Castle Shadow Trial Area"
    GANONS_CASTLE_SPIRIT_TRIAL_AREA = "Ganon's Castle Spirit Trial Area"
    GANONS_CASTLE_LIGHT_TRIAL_AREA = "Ganon's Castle Light Trial Area"
    GANONS_CASTLE_BLUE_FIRE_ACCESS = "Ganon's Castle Blue Fire Access"
    GANONS_CASTLE_WATER_TRIAL_FAIRY_POT = "Ganon's Castle Water Trial Fairy Pot"
    GANONS_CASTLE_SPIRIT_TRIAL_NUT_POT = "Ganon's Castle Spirit Trial Nut Pot"
    GANON_DEFEATED = "Ganon Defeated"


class LocalEvents(StrEnum):
    GANONS_CASTLE_FOREST_TRIAL_CLEARED = "Ganon's Castle Forest Trial Cleared"
    GANONS_CASTLE_FIRE_TRIAL_CLEARED = "Ganon's Castle Fire Trial Cleared"
    GANONS_CASTLE_WATER_TRIAL_CLEARED = "Ganon's Castle Water Trial Cleared"
    GANONS_CASTLE_SHADOW_TRIAL_CLEARED = "Ganon's Castle Shadow Trial Cleared"
    GANONS_CASTLE_SPIRIT_TRIAL_CLEARED = "Ganon's Castle Spirit Trial Cleared"
    GANONS_CASTLE_LIGHT_TRIAL_CLEARED = "Ganon's Castle Light Trial Cleared"


trial_mapping: dict[GanonTrialClears,LocalEvents] = {
    GanonTrialClears.FOREST_TRIAL: LocalEvents.GANONS_CASTLE_FOREST_TRIAL_CLEARED,
    GanonTrialClears.FIRE_TRIAL: LocalEvents.GANONS_CASTLE_FIRE_TRIAL_CLEARED,
    GanonTrialClears.WATER_TRIAL: LocalEvents.GANONS_CASTLE_WATER_TRIAL_CLEARED,
    GanonTrialClears.SHADOW_TRIAL: LocalEvents.GANONS_CASTLE_SHADOW_TRIAL_CLEARED,
    GanonTrialClears.SPIRIT_TRIAL: LocalEvents.GANONS_CASTLE_SPIRIT_TRIAL_CLEARED,
    GanonTrialClears.LIGHT_TRIAL: LocalEvents.GANONS_CASTLE_LIGHT_TRIAL_CLEARED
}


def set_region_rules(world: "SohWorld") -> None:
    # Ganon's Castle Entryway
    # Connections
    connect_regions(Regions.GANONS_CASTLE_ENTRYWAY, world, [
        (Regions.GANONS_CASTLE_LOBBY, lambda bundle: True_()),
        (Regions.CASTLE_GROUNDS_FROM_GANONS_CASTLE, lambda bundle: True_())
    ])

    # Ganon's Castle Lobby
    # Connections
    connect_regions(Regions.GANONS_CASTLE_LOBBY, world, [
        (Regions.GANONS_CASTLE_ENTRYWAY, lambda bundle: True_()),
        (Regions.GANONS_CASTLE_FOREST_TRIAL, lambda bundle: OptionFilter(MedallionLockedTrials, False) | has_item(Items.FOREST_MEDALLION, bundle)),
        (Regions.GANONS_CASTLE_FIRE_TRIAL, lambda bundle: OptionFilter(MedallionLockedTrials, False) | has_item(Items.FIRE_MEDALLION, bundle)),
        (Regions.GANONS_CASTLE_WATER_TRIAL, lambda bundle: OptionFilter(MedallionLockedTrials, False) | has_item(Items.WATER_MEDALLION, bundle)),
        (Regions.GANONS_CASTLE_SHADOW_TRIAL, lambda bundle: OptionFilter(MedallionLockedTrials, False) | has_item(Items.SHADOW_MEDALLION, bundle)),
        (Regions.GANONS_CASTLE_SPIRIT_TRIAL, lambda bundle: OptionFilter(MedallionLockedTrials, False) | has_item(Items.SPIRIT_MEDALLION, bundle)),
        (Regions.GANONS_CASTLE_LIGHT_TRIAL, lambda bundle: can_use(Items.GOLDEN_GAUNTLETS, bundle) & (OptionFilter(MedallionLockedTrials, False) | has_item(Items.LIGHT_MEDALLION, bundle))),
        (Regions.GANONS_TOWER_ENTRYWAY, lambda bundle: True_()),
        (Regions.GANONS_CASTLE_DEKU_SCRUBS, lambda bundle: can_do_trick(Tricks.LENS_GANON, bundle) |
         can_use(Items.LENS_OF_TRUTH, bundle)),
    ])

    # Ganon's Castle Deku Scrubs
    # Events
    add_events(Regions.GANONS_CASTLE_DEKU_SCRUBS, world, [
        (EventLocations.GANONS_CASTLE_FREE_FAIRIES,
         Events.CAN_ACCESS_FAIRIES, lambda bundle: True_())
    ])
    # Locations
    add_locations(Regions.GANONS_CASTLE_DEKU_SCRUBS, world, [
        (Locations.GANONS_CASTLE_DEKU_SCRUB_CENTER_LEFT,
         lambda bundle: can_stun_deku(bundle) & can_afford_slot(Locations.GANONS_CASTLE_DEKU_SCRUB_CENTER_LEFT, bundle)),
        (Locations.GANONS_CASTLE_DEKU_SCRUB_CENTER_RIGHT,
         lambda bundle: can_stun_deku(bundle) & can_afford_slot(Locations.GANONS_CASTLE_DEKU_SCRUB_CENTER_RIGHT, bundle)),
        (Locations.GANONS_CASTLE_DEKU_SCRUB_RIGHT,
         lambda bundle: can_stun_deku(bundle) & can_afford_slot(Locations.GANONS_CASTLE_DEKU_SCRUB_RIGHT, bundle)),
        (Locations.GANONS_CASTLE_DEKU_SCRUB_LEFT,
         lambda bundle: can_stun_deku(bundle) & can_afford_slot(Locations.GANONS_CASTLE_DEKU_SCRUB_LEFT, bundle)),
        (Locations.GANONS_CASTLE_SCRUBS_FAIRY1, lambda bundle: True_()),
        (Locations.GANONS_CASTLE_SCRUBS_FAIRY2, lambda bundle: True_()),
        (Locations.GANONS_CASTLE_SCRUBS_FAIRY3, lambda bundle: True_()),
        (Locations.GANONS_CASTLE_SCRUBS_FAIRY4, lambda bundle: True_()),
        (Locations.GANONS_CASTLE_SCRUBS_FAIRY5, lambda bundle: True_()),
        (Locations.GANONS_CASTLE_SCRUBS_FAIRY6, lambda bundle: True_()),
        (Locations.GANONS_CASTLE_SCRUBS_FAIRY7, lambda bundle: True_()),
        (Locations.GANONS_CASTLE_SCRUBS_FAIRY8, lambda bundle: True_()),
    ])

    # Ganon's Castle Forest Trial
    # Events
    add_events(Regions.GANONS_CASTLE_FOREST_TRIAL, world, [
        (EventLocations.GANONS_CASTLE_FOREST_TRIAL_AREA, LocalEvents.GANONS_CASTLE_FOREST_TRIAL_CLEARED, lambda bundle: can_use(Items.LIGHT_ARROW, bundle) &
         (can_use(Items.FIRE_ARROW, bundle) |
          can_use(Items.DINS_FIRE, bundle)))
    ])
    # Locations
    add_locations(Regions.GANONS_CASTLE_FOREST_TRIAL, world, [
        (Locations.GANONS_CASTLE_FOREST_TRIAL_CHEST,
         lambda bundle: can_kill_enemy(bundle, Enemies.WOLFOS)),
        (Locations.GANONS_CASTLE_FOREST_TRIAL_POT1, lambda bundle: can_break_pots(bundle) & (can_use(Items.FIRE_ARROW,
         bundle) | (can_use(Items.DINS_FIRE, bundle) & can_use_any([Items.FAIRY_BOW, Items.HOOKSHOT], bundle)))),
        (Locations.GANONS_CASTLE_FOREST_TRIAL_POT2, lambda bundle: can_break_pots(bundle) & (can_use(Items.FIRE_ARROW,
         bundle) | (can_use(Items.DINS_FIRE, bundle) & can_use_any([Items.FAIRY_BOW, Items.HOOKSHOT], bundle)))),
    ])

    # Ganon's Castle Fire Trial
    # Events
    add_events(Regions.GANONS_CASTLE_FIRE_TRIAL, world, [
        (EventLocations.GANONS_CASTLE_FIRE_TRIAL_AREA, LocalEvents.GANONS_CASTLE_FIRE_TRIAL_CLEARED, lambda bundle: can_use(Items.GORON_TUNIC,
         bundle) & can_use(Items.GOLDEN_GAUNTLETS, bundle) & can_use(Items.LIGHT_ARROW, bundle) & can_use(Items.LONGSHOT, bundle))
    ])
    # Locations
    add_locations(Regions.GANONS_CASTLE_FIRE_TRIAL, world, [
        (Locations.GANONS_CASTLE_FIRE_TRIAL_POT1, lambda bundle: can_break_pots(bundle) & can_use(
            Items.GORON_TUNIC, bundle) & can_use(Items.GOLDEN_GAUNTLETS, bundle) & can_use(Items.LONGSHOT, bundle)),
        (Locations.GANONS_CASTLE_FIRE_TRIAL_POT2, lambda bundle: can_break_pots(bundle) & can_use(
            Items.GORON_TUNIC, bundle) & can_use(Items.GOLDEN_GAUNTLETS, bundle) & can_use(Items.LONGSHOT, bundle)),
        (Locations.GANONS_CASTLE_FIRE_TRIAL_HEART,
         lambda bundle: can_use(Items.GORON_TUNIC, bundle))
    ])

    # Ganon's Castle Water Trial
    # Events
    add_events(Regions.GANONS_CASTLE_WATER_TRIAL, world, [
        (EventLocations.GANONS_CASTLE_BLUE_FIRE_ACCESS,
         Events.CAN_ACCESS_BLUE_FIRE, lambda bundle: True_()),
        (EventLocations.GANONS_CASTLE_WATER_TRIAL_FAIRY_POT, Events.CAN_ACCESS_FAIRIES,
         lambda bundle: blue_fire(bundle) & can_kill_enemy(bundle, Enemies.FREEZARD)),
        (EventLocations.GANONS_CASTLE_WATER_TRIAL_AREA, LocalEvents.GANONS_CASTLE_WATER_TRIAL_CLEARED, lambda bundle: (
            blue_fire(bundle) & is_adult(bundle) & can_use(Items.MEGATON_HAMMER, bundle) & can_use(Items.LIGHT_ARROW, bundle)))
    ])
    # Locations
    add_locations(Regions.GANONS_CASTLE_WATER_TRIAL, world, [
        (Locations.GANONS_CASTLE_WATER_TRIAL_LEFT_CHEST, lambda bundle: True_()),
        (Locations.GANONS_CASTLE_WATER_TRIAL_RIGHT_CHEST, lambda bundle: True_()),
        (Locations.GANONS_CASTLE_WATER_TRIAL_POT1, lambda bundle: can_break_pots(bundle)
         & blue_fire(bundle) & is_adult(bundle) & can_use(Items.MEGATON_HAMMER, bundle)),
        (Locations.GANONS_CASTLE_WATER_TRIAL_POT2, lambda bundle: can_break_pots(bundle)
         & blue_fire(bundle) & is_adult(bundle) & can_use(Items.MEGATON_HAMMER, bundle)),
        (Locations.GANONS_CASTLE_WATER_TRIAL_POT3, lambda bundle: can_break_pots(
            bundle) & blue_fire(bundle) & can_kill_enemy(bundle, Enemies.FREEZARD))
    ])

    # Ganon's Castle Shadow Trial
    # Events
    add_events(Regions.GANONS_CASTLE_SHADOW_TRIAL, world, [
        (EventLocations.GANONS_CASTLE_SHADOW_TRIAL_AREA, LocalEvents.GANONS_CASTLE_SHADOW_TRIAL_CLEARED, lambda bundle:
            can_use(Items.LIGHT_ARROW, bundle) & can_use(Items.MEGATON_HAMMER, bundle) & ((can_use(Items.FIRE_ARROW, bundle) & (can_do_trick(Tricks.LENS_GANON, bundle) | can_use(Items.LENS_OF_TRUTH, bundle))) | (can_use(Items.LONGSHOT, bundle) & (can_use(Items.HOVER_BOOTS, bundle) | (can_use(Items.DINS_FIRE, bundle) & (can_do_trick(Tricks.LENS_GANON, bundle) | can_use(Items.LENS_OF_TRUTH, bundle)))))))
    ])
    # Locations
    add_locations(Regions.GANONS_CASTLE_SHADOW_TRIAL, world, [
        (Locations.GANONS_CASTLE_SHADOW_TRIAL_FRONT_CHEST, lambda bundle: can_use_any(
            [Items.FIRE_ARROW, Items.HOOKSHOT, Items.HOVER_BOOTS, Items.SONG_OF_TIME], bundle) | is_child(bundle)),
        (Locations.GANONS_CASTLE_SHADOW_TRIAL_GOLDEN_GAUNTLETS_CHEST, lambda bundle: can_use(Items.FIRE_ARROW, bundle) | (
            can_use(Items.LONGSHOT, bundle) & (can_use(Items.HOVER_BOOTS, bundle) | can_use(Items.DINS_FIRE, bundle)))),
        (Locations.GANONS_CASTLE_SHADOW_TRIAL_POT1, lambda bundle: can_use(
            Items.FIRE_ARROW, bundle) | can_use(Items.LONGSHOT, bundle)),
        (Locations.GANONS_CASTLE_SHADOW_TRIAL_POT2, lambda bundle: can_use(
            Items.FIRE_ARROW, bundle) | can_use(Items.LONGSHOT, bundle)),
        (Locations.GANONS_CASTLE_SHADOW_TRIAL_POT3, lambda bundle: (can_break_pots(bundle) &
                                                                    can_use(Items.MEGATON_HAMMER, bundle) &
                                                                    ((can_use(Items.FIRE_ARROW, bundle) &
                                                                      (can_do_trick(Tricks.LENS_GANON, bundle) |
                                                                       can_use(Items.LENS_OF_TRUTH, bundle))) |
                                                                     (can_use(Items.LONGSHOT, bundle) &
                                                                      (can_use(Items.HOVER_BOOTS, bundle) |
                                                                       (can_use(Items.DINS_FIRE, bundle) &
                                                                        (can_do_trick(Tricks.LENS_GANON, bundle) |
                                                                         can_use(Items.LENS_OF_TRUTH, bundle)))))))),
        (Locations.GANONS_CASTLE_SHADOW_TRIAL_POT4, lambda bundle: (can_break_pots(bundle) &
                                                                    can_use(Items.MEGATON_HAMMER, bundle) &
                                                                    ((can_use(Items.FIRE_ARROW, bundle) &
                                                                      (can_do_trick(Tricks.LENS_GANON, bundle) |
                                                                       can_use(Items.LENS_OF_TRUTH, bundle))) |
                                                                     (can_use(Items.LONGSHOT, bundle) &
                                                                      (can_use(Items.HOVER_BOOTS, bundle) |
                                                                       (can_use(Items.DINS_FIRE, bundle) &
                                                                        (can_do_trick(Tricks.LENS_GANON, bundle) |
                                                                         can_use(Items.LENS_OF_TRUTH, bundle)))))))),
        (Locations.GANONS_CASTLE_SHADOW_TRIAL_HEART1, lambda bundle: ((can_use(Items.FIRE_ARROW, bundle) |
                                                                       (can_use(Items.LONGSHOT, bundle) &
                                                                        (can_use(Items.HOVER_BOOTS, bundle) |
                                                                         can_use(Items.DINS_FIRE, bundle)))) &
                                                                      (can_do_trick(Tricks.LENS_GANON, bundle) |
                                                                       can_use(Items.LENS_OF_TRUTH, bundle) |
                                                                       can_use(Items.BOOMERANG, bundle)))),
        (Locations.GANONS_CASTLE_SHADOW_TRIAL_HEART2, lambda bundle: ((can_use(Items.FIRE_ARROW, bundle) |
                                                                       (can_use(Items.LONGSHOT, bundle) &
                                                                        (can_use(Items.HOVER_BOOTS, bundle) |
                                                                         can_use(Items.DINS_FIRE, bundle)))) &
                                                                      (can_do_trick(Tricks.LENS_GANON, bundle) |
                                                                       can_use(Items.LENS_OF_TRUTH, bundle) |
                                                                       can_use(Items.BOOMERANG, bundle)))),
        (Locations.GANONS_CASTLE_SHADOW_TRIAL_HEART3, lambda bundle: ((can_use(Items.FIRE_ARROW, bundle) |
                                                                       (can_use(Items.LONGSHOT, bundle) &
                                                                        (can_use(Items.HOVER_BOOTS, bundle) |
                                                                         can_use(Items.DINS_FIRE, bundle)))) &
                                                                      (can_do_trick(Tricks.LENS_GANON, bundle) |
                                                                       can_use(Items.LENS_OF_TRUTH, bundle) |
                                                                       can_use(Items.BOOMERANG, bundle))))
    ])

    # Ganon's Castle Spirit Trial
    # Events
    add_events(Regions.GANONS_CASTLE_SPIRIT_TRIAL, world, [
        (EventLocations.GANONS_CASTLE_SPIRIT_TRIAL_NUT_POT, Events.CAN_FARM_NUTS, lambda bundle: (((can_do_trick(Tricks.GANON_SPIRIT_TRIAL_HOOKSHOT, bundle) &
                                                                                                    can_jump_slash_except_hammer(bundle)) |
                                                                                                   can_use(Items.HOOKSHOT, bundle)) &
                                                                                                  (can_use(Items.BOMBCHUS_5, bundle) |
                                                                                                   (can_do_trick(Tricks.HOOKSHOT_EXTENSION, bundle) &
                                                                                                    (can_use(Items.FAIRY_BOW, bundle) |
                                                                                                     can_use(Items.FAIRY_SLINGSHOT, bundle)))) &
                                                                                                  can_use(Items.FAIRY_BOW, bundle) &
                                                                                                  (can_use(Items.MIRROR_SHIELD, bundle) |
                                                                                                   (OptionFilter(SunlightArrows, True) & can_use(Items.LIGHT_ARROW, bundle))))),
        (EventLocations.GANONS_CASTLE_SPIRIT_TRIAL_AREA, LocalEvents.GANONS_CASTLE_SPIRIT_TRIAL_CLEARED, lambda bundle: (can_use(Items.LIGHT_ARROW, bundle) &
                                                                                                                         (can_use(Items.MIRROR_SHIELD, bundle) |
                                                                                                                          OptionFilter(SunlightArrows, True)) &
                                                                                                                         (can_use(Items.BOMBCHUS_5, bundle) |
                                                                                                                          (can_do_trick(Tricks.HOOKSHOT_EXTENSION, bundle) &
                                                                                                                           (can_use(Items.FAIRY_BOW, bundle) |
                                                                                                                            can_use(Items.FAIRY_SLINGSHOT, bundle)))) &
                                                                                                                         ((can_do_trick(Tricks.GANON_SPIRIT_TRIAL_HOOKSHOT, bundle) &
                                                                                                                           can_jump_slash_except_hammer(bundle)) |
                                                                                                                          can_use(Items.HOOKSHOT, bundle))))
    ])
    # Locations
    add_locations(Regions.GANONS_CASTLE_SPIRIT_TRIAL, world, [
        (Locations.GANONS_CASTLE_SPIRIT_TRIAL_CRYSTAL_SWITCH_CHEST, lambda bundle: ((can_do_trick(Tricks.GANON_SPIRIT_TRIAL_HOOKSHOT, bundle) |
                                                                                     can_use(Items.HOOKSHOT, bundle)) &
                                                                                    (can_jump_slash_except_hammer(bundle) |
                                                                                     (can_use(Items.BOMBCHUS_5, bundle) |
                                                                                      (can_do_trick(Tricks.HOOKSHOT_EXTENSION, bundle) &
                                                                                       (can_use(Items.FAIRY_BOW, bundle) |
                                                                                        can_use(Items.FAIRY_SLINGSHOT, bundle))))))),
        (Locations.GANONS_CASTLE_SPIRIT_TRIAL_INVISIBLE_CHEST, lambda bundle: (can_do_trick(Tricks.GANON_SPIRIT_TRIAL_HOOKSHOT, bundle) | can_use(Items.HOOKSHOT, bundle)) & (can_use(Items.BOMBCHUS_5, bundle) | (
            can_do_trick(Tricks.HOOKSHOT_EXTENSION, bundle) & (can_use_any([Items.FAIRY_BOW, Items.FAIRY_SLINGSHOT], bundle)))) & (can_do_trick(Tricks.LENS_GANON, bundle) | can_use(Items.LENS_OF_TRUTH, bundle))),
        (Locations.GANONS_CASTLE_SPIRIT_TRIAL_POT1, lambda bundle: (((can_do_trick(Tricks.GANON_SPIRIT_TRIAL_HOOKSHOT, bundle) &
                                                                      can_jump_slash_except_hammer(bundle)) |
                                                                     can_use(Items.HOOKSHOT, bundle)) &
                                                                    (can_use(Items.BOMBCHUS_5, bundle) |
                                                                     (can_do_trick(Tricks.HOOKSHOT_EXTENSION, bundle) &
                                                                      (can_use(Items.FAIRY_BOW, bundle) |
                                                                       can_use(Items.FAIRY_SLINGSHOT, bundle)))) &
                                                                    can_use(Items.FAIRY_BOW, bundle) &
                                                                    (can_use(Items.MIRROR_SHIELD, bundle) |
                                                                     (OptionFilter(SunlightArrows, True) & can_use(Items.LIGHT_ARROW, bundle))))),
        (Locations.GANONS_CASTLE_SPIRIT_TRIAL_POT2, lambda bundle: (((can_do_trick(Tricks.GANON_SPIRIT_TRIAL_HOOKSHOT, bundle) &
                                                                      can_jump_slash_except_hammer(bundle)) |
                                                                     can_use(Items.HOOKSHOT, bundle)) &
                                                                    (can_use(Items.BOMBCHUS_5, bundle) |
                                                                     (can_do_trick(Tricks.HOOKSHOT_EXTENSION, bundle) &
                                                                      (can_use(Items.FAIRY_BOW, bundle) |
                                                                       can_use(Items.FAIRY_SLINGSHOT, bundle)))) &
                                                                    can_use(Items.FAIRY_BOW, bundle) &
                                                                    (can_use(Items.MIRROR_SHIELD, bundle) |
                                                                     (OptionFilter(SunlightArrows, True) & can_use(Items.LIGHT_ARROW, bundle))))),
        (Locations.GANONS_CASTLE_SPIRIT_TRIAL_BEAMOS_SUNS_SONG_FAIRY,
         lambda bundle: can_use(Items.SUNS_SONG, bundle)),
        (Locations.GANONS_CASTLE_SPIRIT_TRIAL_HEART, lambda bundle: True_())
    ])

    # Ganon's Castle Light Trial
    # Events
    add_events(Regions.GANONS_CASTLE_LIGHT_TRIAL, world, [
        (EventLocations.GANONS_CASTLE_LIGHT_TRIAL_AREA, LocalEvents.GANONS_CASTLE_LIGHT_TRIAL_CLEARED, lambda bundle:
            can_use(Items.LIGHT_ARROW, bundle) & (can_use(Items.HOOKSHOT, bundle) | (is_adult(bundle) & can_ground_jump(bundle))) & small_keys(Items.GANONS_CASTLE_SMALL_KEY, 2, bundle) & (can_do_trick(Tricks.LENS_GANON, bundle) | can_use(Items.LENS_OF_TRUTH, bundle)))
    ])
    # Locations
    add_locations(Regions.GANONS_CASTLE_LIGHT_TRIAL, world, [
        (Locations.GANONS_CASTLE_LIGHT_TRIAL_FIRST_LEFT_CHEST, lambda bundle: True_()),
        (Locations.GANONS_CASTLE_LIGHT_TRIAL_SECOND_LEFT_CHEST, lambda bundle: True_()),
        (Locations.GANONS_CASTLE_LIGHT_TRIAL_THIRD_LEFT_CHEST, lambda bundle: True_()),
        (Locations.GANONS_CASTLE_LIGHT_TRIAL_FIRST_RIGHT_CHEST, lambda bundle: True_()),
        (Locations.GANONS_CASTLE_LIGHT_TRIAL_SECOND_RIGHT_CHEST, lambda bundle: True_()),
        (Locations.GANONS_CASTLE_LIGHT_TRIAL_THIRD_RIGHT_CHEST, lambda bundle: True_()),
        (Locations.GANONS_CASTLE_LIGHT_TRIAL_INVISIBLE_ENEMIES_CHEST, lambda bundle: (can_do_trick(Tricks.LENS_GANON, bundle) |
                                                                                      can_use(Items.LENS_OF_TRUTH, bundle))),
        (Locations.GANONS_CASTLE_LIGHT_TRIAL_LULLABY_CHEST, lambda bundle: (can_use(Items.ZELDAS_LULLABY, bundle) &
                                                                            small_keys(Items.GANONS_CASTLE_SMALL_KEY, 1, bundle))),
        (Locations.GANONS_CASTLE_LIGHT_TRIAL_BOULDER_POT1, lambda bundle: (can_break_pots(bundle) &
                                                                           small_keys(Items.GANONS_CASTLE_SMALL_KEY, 2, bundle))),
        (Locations.GANONS_CASTLE_LIGHT_TRIAL_POT1, lambda bundle: can_break_pots(bundle) & (can_use(Items.HOOKSHOT, bundle) | (is_adult(bundle) & can_ground_jump(
            bundle))) & small_keys(Items.GANONS_CASTLE_SMALL_KEY, 2, bundle) & (can_do_trick(Tricks.LENS_GANON, bundle) | can_use(Items.LENS_OF_TRUTH, bundle))),
        (Locations.GANONS_CASTLE_LIGHT_TRIAL_POT2, lambda bundle: can_break_pots(bundle) & (can_use(Items.HOOKSHOT, bundle) | (is_adult(bundle) & can_ground_jump(
            bundle))) & small_keys(Items.GANONS_CASTLE_SMALL_KEY, 2, bundle) & (can_do_trick(Tricks.LENS_GANON, bundle) | can_use(Items.LENS_OF_TRUTH, bundle)))
    ])

    # Ganon's Tower Entryway
    # Connections
    connect_regions(Regions.GANONS_TOWER_ENTRYWAY, world, [
        (Regions.GANONS_CASTLE_LOBBY, lambda bundle: True_()),
        (Regions.GANONS_TOWER_FLOOR_1, lambda bundle: OptionFilter(GanonsTrials, GanonsTrials.option_skip)
                        | HasAll(*[(str(trial_mapping[trial])) for trial in world.ganons_trials]))
    ])

    # Ganon's Tower Floor 1
    # Connections
    connect_regions(Regions.GANONS_TOWER_FLOOR_1, world, [
        (Regions.GANONS_TOWER_ENTRYWAY, lambda bundle: can_kill_enemy(
            bundle, Enemies.DINOLFOS, EnemyDistance.CLOSE, True, 2)),
        (Regions.GANONS_TOWER_FLOOR_2, lambda bundle: can_kill_enemy(
            bundle, Enemies.DINOLFOS, EnemyDistance.CLOSE, True, 2))
    ])

    # Ganon's Tower Floor 2
    # Locations
    add_locations(Regions.GANONS_TOWER_FLOOR_2, world, [
        (Locations.GANONS_CASTLE_TOWER_BOSS_KEY_CHEST, lambda bundle: can_kill_enemy(
            bundle, Enemies.STALFOS, EnemyDistance.CLOSE, True, 2))
    ])
    # Connections
    connect_regions(Regions.GANONS_TOWER_FLOOR_2, world, [
        (Regions.GANONS_TOWER_FLOOR_1, lambda bundle: can_kill_enemy(
            bundle, Enemies.STALFOS, EnemyDistance.CLOSE, True, 2)),
        (Regions.GANONS_TOWER_FLOOR_3, lambda bundle: can_kill_enemy(
            bundle, Enemies.STALFOS, EnemyDistance.CLOSE, True, 2))
    ])

    # Ganon's Tower Floor 3
    # Connections
    connect_regions(Regions.GANONS_TOWER_FLOOR_3, world, [
        (Regions.GANONS_TOWER_FLOOR_2, lambda bundle: can_kill_enemy(
            bundle, Enemies.IRON_KNUCKLE, EnemyDistance.CLOSE, True, 2)),
        (Regions.GANONS_TOWER_BEFORE_GANONDORFS_LAIR, lambda bundle: can_kill_enemy(
            bundle, Enemies.IRON_KNUCKLE, EnemyDistance.CLOSE, True, 2))
    ])

    # Ganon's Tower Before Ganondorf's Lair
    # Locations
    add_locations(Regions.GANONS_TOWER_BEFORE_GANONDORFS_LAIR, world, [
        (Locations.GANONS_CASTLE_GANONS_TOWER_POT1,
         lambda bundle: can_break_pots(bundle)),
        (Locations.GANONS_CASTLE_GANONS_TOWER_POT2,
         lambda bundle: can_break_pots(bundle)),
        (Locations.GANONS_CASTLE_GANONS_TOWER_POT3,
         lambda bundle: can_break_pots(bundle)),
        (Locations.GANONS_CASTLE_GANONS_TOWER_POT4,
         lambda bundle: can_break_pots(bundle)),
        (Locations.GANONS_CASTLE_GANONS_TOWER_POT5,
         lambda bundle: can_break_pots(bundle)),
        (Locations.GANONS_CASTLE_GANONS_TOWER_POT6,
         lambda bundle: can_break_pots(bundle)),
        (Locations.GANONS_CASTLE_GANONS_TOWER_POT7,
         lambda bundle: can_break_pots(bundle)),
        (Locations.GANONS_CASTLE_GANONS_TOWER_POT8,
         lambda bundle: can_break_pots(bundle)),
        (Locations.GANONS_CASTLE_GANONS_TOWER_POT9,
         lambda bundle: can_break_pots(bundle)),
        (Locations.GANONS_CASTLE_GANONS_TOWER_POT10,
         lambda bundle: can_break_pots(bundle)),
        (Locations.GANONS_CASTLE_GANONS_TOWER_POT11,
         lambda bundle: can_break_pots(bundle)),
        (Locations.GANONS_CASTLE_GANONS_TOWER_POT12,
         lambda bundle: can_break_pots(bundle)),
        (Locations.GANONS_CASTLE_GANONS_TOWER_POT13,
         lambda bundle: can_break_pots(bundle)),
        (Locations.GANONS_CASTLE_GANONS_TOWER_POT14,
         lambda bundle: can_break_pots(bundle)),
        (Locations.GANONS_CASTLE_GANONS_TOWER_POT15,
         lambda bundle: can_break_pots(bundle)),
        (Locations.GANONS_CASTLE_GANONS_TOWER_POT16,
         lambda bundle: can_break_pots(bundle)),
        (Locations.GANONS_CASTLE_GANONS_TOWER_POT17,
         lambda bundle: can_break_pots(bundle)),
        (Locations.GANONS_CASTLE_GANONS_TOWER_POT18,
         lambda bundle: can_break_pots(bundle)),
    ])
    # Connections
    connect_regions(Regions.GANONS_TOWER_BEFORE_GANONDORFS_LAIR, world, [
        (Regions.GANONS_TOWER_FLOOR_3, lambda bundle: True_()),
        (Regions.GANONDORFS_LAIR, lambda bundle: has_item(
            Items.GANONS_CASTLE_BOSS_KEY, bundle) | OptionFilter(TriforceHunt, True))
    ])

    # Ganondorf's Lair
    # Connections
    connect_regions(Regions.GANONDORFS_LAIR, world, [
        (Regions.GANONS_CASTLE_ESCAPE,
         lambda bundle: can_kill_enemy(bundle, Enemies.GANONDORF))
    ])

    # Ganon's Castle Escape
    # Connections
    connect_regions(Regions.GANONS_CASTLE_ESCAPE, world, [
        (Regions.GANONS_ARENA, lambda bundle: True_())
    ])

    # Ganon's Arena
    # Events
    if not bool(world.options.triforce_hunt):
        add_events(Regions.GANONS_ARENA, world, [
            (EventLocations.GANON_DEFEATED, Events.GAME_COMPLETED, lambda bundle:
             (can_kill_enemy(bundle, Enemies.GANON)))
        ])
