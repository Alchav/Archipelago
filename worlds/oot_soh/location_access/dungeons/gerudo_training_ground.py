from ...LogicHelpers import *

if TYPE_CHECKING:
    from ... import SohWorld


def set_region_rules(world: "SohWorld") -> None:
    # Gerudo Training Ground Entryway
    # Connections
    connect_regions(Regions.GERUDO_TRAINING_GROUND_ENTRYWAY, world, [
        (Regions.GERUDO_TRAINING_GROUND_LOBBY, lambda bundle: True_()),
        (Regions.GF_EXITING_GTG, lambda bundle: True_()),
    ])

    # Gerudo Training Ground Lobby
    # Locations
    add_locations(Regions.GERUDO_TRAINING_GROUND_LOBBY, world, [
        (Locations.GERUDO_TRAINING_GROUND_LOBBY_LEFT_CHEST,
         lambda bundle: can_hit_eye_targets(bundle)),
        (Locations.GERUDO_TRAINING_GROUND_LOBBY_RIGHT_CHEST,
         lambda bundle: can_hit_eye_targets(bundle)),
        (Locations.GERUDO_TRAINING_GROUND_STALFOS_CHEST,
         lambda bundle: can_kill_enemy(bundle, Enemies.STALFOS, EnemyDistance.CLOSE, True, 2, True)),
        (Locations.GERUDO_TRAINING_GROUND_BEAMOS_CHEST,
         lambda bundle: can_kill_enemy(bundle, Enemies.BEAMOS) & can_kill_enemy(bundle, Enemies.DINOLFOS,
                                                                                  EnemyDistance.CLOSE, True, 2, True)),
        (Locations.GERUDO_TRAINING_GROUND_ENTRANCE_SONG_OF_STORMS_FAIRY,
         lambda bundle: can_use(Items.SONG_OF_STORMS, bundle)),
        (Locations.GERUDO_TRAINING_GROUND_BEAMOS_EAST_HEART, lambda bundle: True_()),
        (Locations.GERUDO_TRAINING_GROUND_BEAMOS_SOUTH_HEART, lambda bundle: True_()),
    ])
    # Connections
    connect_regions(Regions.GERUDO_TRAINING_GROUND_LOBBY, world, [
        (Regions.GERUDO_TRAINING_GROUND_ENTRYWAY, lambda bundle: True_()),
        (Regions.GERUDO_TRAINING_GROUND_HEAVY_BLOCK_ROOM,
         lambda bundle: can_kill_enemy(bundle, Enemies.STALFOS, EnemyDistance.CLOSE, True, 2, True) & (
             can_use(Items.HOOKSHOT, bundle) | can_do_trick(Tricks.GTG_WITHOUT_HOOKSHOT, bundle))),
        (Regions.GERUDO_TRAINING_GROUND_LAVA_ROOM,
         lambda bundle: can_kill_enemy(bundle, Enemies.BEAMOS) & can_kill_enemy(bundle, Enemies.DINOLFOS,
                                                                                  EnemyDistance.CLOSE, True, 2, True)),
        (Regions.GERUDO_TRAINING_GROUND_CENTRAL_MAZE, lambda bundle: True_()),
    ])

    # Gerudo Training Ground Central Maze
    # Locations
    add_locations(Regions.GERUDO_TRAINING_GROUND_CENTRAL_MAZE, world, [
        (Locations.GERUDO_TRAINING_GROUND_HIDDEN_CEILING_CHEST,
         lambda bundle: small_keys(Items.TRAINING_GROUND_SMALL_KEY, 3, bundle) & (
             can_use(Items.LENS_OF_TRUTH, bundle) | can_do_trick(Tricks.LENS_GTG, bundle))),
        (Locations.GERUDO_TRAINING_GROUND_MAZE_PATH_FIRST_CHEST,
         lambda bundle: small_keys(Items.TRAINING_GROUND_SMALL_KEY, 4, bundle)),
        (Locations.GERUDO_TRAINING_GROUND_MAZE_PATH_SECOND_CHEST,
         lambda bundle: small_keys(Items.TRAINING_GROUND_SMALL_KEY, 6, bundle)),
        (Locations.GERUDO_TRAINING_GROUND_MAZE_PATH_THIRD_CHEST,
         lambda bundle: small_keys(Items.TRAINING_GROUND_SMALL_KEY, 7, bundle)),
        (Locations.GERUDO_TRAINING_GROUND_MAZE_PATH_FINAL_CHEST,
         lambda bundle: small_keys(Items.TRAINING_GROUND_SMALL_KEY, 9, bundle)),
    ])
    # Connections
    connect_regions(Regions.GERUDO_TRAINING_GROUND_CENTRAL_MAZE, world, [
        (Regions.GERUDO_TRAINING_GROUND_CENTRAL_MAZE_RIGHT,
         lambda bundle: small_keys(Items.TRAINING_GROUND_SMALL_KEY, 9, bundle)),
    ])

    # Gerudo Training Ground Central Maze Right
    # Locations
    add_locations(Regions.GERUDO_TRAINING_GROUND_CENTRAL_MAZE_RIGHT, world, [
        (Locations.GERUDO_TRAINING_GROUND_FREESTANDING_KEY, lambda bundle: True_()),
        (Locations.GERUDO_TRAINING_GROUND_MAZE_RIGHT_SIDE_CHEST, lambda bundle: True_()),
        (Locations.GERUDO_TRAINING_GROUND_MAZE_RIGHT_CENTRAL_CHEST, lambda bundle: True_()),
    ])
    # Connections
    connect_regions(Regions.GERUDO_TRAINING_GROUND_CENTRAL_MAZE_RIGHT, world, [
        (Regions.GERUDO_TRAINING_GROUND_HAMMER_ROOM,
         lambda bundle: can_use(Items.HOOKSHOT, bundle)),
        (Regions.GERUDO_TRAINING_GROUND_LAVA_ROOM, lambda bundle: True_()),
    ])

    # Gerudo Training Ground Lava Room
    # Locations
    add_locations(Regions.GERUDO_TRAINING_GROUND_LAVA_ROOM, world, [
        (Locations.GERUDO_TRAINING_GROUND_UNDERWATER_SILVER_RUPEE_CHEST,
         lambda bundle: can_use(Items.HOOKSHOT, bundle) & can_use(Items.SONG_OF_TIME, bundle) & can_use(
             Items.IRON_BOOTS, bundle) & water_timer_at_least(bundle, 24) & has_item(Items.BRONZE_SCALE, bundle)),
    ])
    # Connections
    connect_regions(Regions.GERUDO_TRAINING_GROUND_LAVA_ROOM, world, [
        (Regions.GERUDO_TRAINING_GROUND_CENTRAL_MAZE_RIGHT,
         lambda bundle: can_use(Items.SONG_OF_TIME, bundle) | is_child(bundle)),
        (Regions.GERUDO_TRAINING_GROUND_HAMMER_ROOM, lambda bundle: can_use(Items.LONGSHOT, bundle) | (
            can_use(Items.HOVER_BOOTS, bundle) & can_use(Items.HOOKSHOT, bundle))),
    ])

    # Gerudo Training Ground Hammer Room
    # Locations
    add_locations(Regions.GERUDO_TRAINING_GROUND_HAMMER_ROOM, world, [
        (Locations.GERUDO_TRAINING_GROUND_HAMMER_ROOM_CLEAR_CHEST,
         lambda bundle: can_attack(bundle)),
        (Locations.GERUDO_TRAINING_GROUND_HAMMER_ROOM_SWITCH_CHEST,
         lambda bundle: can_use(Items.MEGATON_HAMMER, bundle) | (
             take_damage(bundle) & can_do_trick(Tricks.FLAMING_CHESTS, bundle))),
    ])
    # Connections
    connect_regions(Regions.GERUDO_TRAINING_GROUND_HAMMER_ROOM, world, [
        (Regions.GERUDO_TRAINING_GROUND_EYE_STATUE_LOWER, lambda bundle: can_use(
            Items.MEGATON_HAMMER, bundle) & can_use(Items.FAIRY_BOW, bundle)),
        (Regions.GERUDO_TRAINING_GROUND_LAVA_ROOM, lambda bundle: True_()),
    ])

    # Gerudo Training Ground Eye Statue Lower
    # Locations
    add_locations(Regions.GERUDO_TRAINING_GROUND_EYE_STATUE_LOWER, world, [
        (Locations.GERUDO_TRAINING_GROUND_EYE_STATUE_CHEST,
         lambda bundle: can_use(Items.FAIRY_BOW, bundle)),
    ])
    # Connections
    connect_regions(Regions.GERUDO_TRAINING_GROUND_EYE_STATUE_LOWER, world, [
        (Regions.GERUDO_TRAINING_GROUND_HAMMER_ROOM, lambda bundle: True_()),
    ])

    # Gerudo Training Ground Eye Statue Upper
    # Locations
    add_locations(Regions.GERUDO_TRAINING_GROUND_EYE_STATUE_UPPER, world, [
        (Locations.GERUDO_TRAINING_GROUND_NEAR_SCARECROW_CHEST,
         lambda bundle: can_use(Items.FAIRY_BOW, bundle)),
    ])
    # Connections
    connect_regions(Regions.GERUDO_TRAINING_GROUND_EYE_STATUE_UPPER, world, [
        (Regions.GERUDO_TRAINING_GROUND_EYE_STATUE_LOWER, lambda bundle: True_()),
    ])

    # Gerudo Training Ground Heavy Block Room
    # Locations
    add_locations(Regions.GERUDO_TRAINING_GROUND_HEAVY_BLOCK_ROOM, world, [
        (Locations.GERUDO_TRAINING_GROUND_BEFORE_HEAVY_BLOCK_CHEST,
         lambda bundle: can_kill_enemy(bundle, Enemies.WOLFOS, EnemyDistance.CLOSE, True, 4, True)),
    ])
    # Connections
    connect_regions(Regions.GERUDO_TRAINING_GROUND_HEAVY_BLOCK_ROOM, world, [
        (Regions.GERUDO_TRAINING_GROUND_EYE_STATUE_UPPER,
         lambda bundle: (can_do_trick(Tricks.LENS_GTG, bundle) | can_use(Items.LENS_OF_TRUTH, bundle)) & (
             can_use(Items.HOOKSHOT, bundle) | (
                 is_adult(bundle) & (
                     can_do_trick(Tricks.GTG_FAKE_WALL, bundle) & can_use(Items.HOVER_BOOTS, bundle))) | can_ground_jump(bundle))),
        (Regions.GERUDO_TRAINING_GROUND_LIKE_LIKE_ROOM,
         lambda bundle: (can_do_trick(Tricks.LENS_GTG, bundle) | can_use(Items.LENS_OF_TRUTH, bundle)) & (
             can_use(Items.HOOKSHOT, bundle) | (
                 is_adult(bundle) & (
                     can_do_trick(Tricks.GTG_FAKE_WALL, bundle) & can_use(Items.HOVER_BOOTS, bundle)) | can_ground_jump(bundle))) & can_use(Items.SILVER_GAUNTLETS, bundle)),
    ])

    # Gerudo Training Ground Like Like Room
    # Locations
    add_locations(Regions.GERUDO_TRAINING_GROUND_LIKE_LIKE_ROOM, world, [
        (Locations.GERUDO_TRAINING_GROUND_HEAVY_BLOCK_FIRST_CHEST,
         lambda bundle: can_jump_slash_except_hammer(bundle)),
        (Locations.GERUDO_TRAINING_GROUND_HEAVY_BLOCK_SECOND_CHEST,
         lambda bundle: can_jump_slash_except_hammer(bundle)),
        (Locations.GERUDO_TRAINING_GROUND_HEAVY_BLOCK_THIRD_CHEST,
         lambda bundle: can_jump_slash_except_hammer(bundle)),
        (Locations.GERUDO_TRAINING_GROUND_HEAVY_BLOCK_FOURTH_CHEST,
         lambda bundle: can_jump_slash_except_hammer(bundle)),
    ])
