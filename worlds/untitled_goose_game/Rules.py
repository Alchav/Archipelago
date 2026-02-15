from BaseClasses import CollectionState
from typing import TYPE_CHECKING
from worlds.generic.Rules import set_rule

from .names import itemNames, locationNames, regionNames

if TYPE_CHECKING:
    from . import GooseGameWorld

class UntitledGooseRules:
    world: "GooseGameWorld"

    def __init__(self, world: "GooseGameWorld") -> None:
        self.player = world.player
        self.world = world
        
        # To Do (As Well) Task Rules
        if self.world.options.include_extra_tasks.value:
            self.extra_task_rules = {
                locationNames.EXTRA_TASK_GROUNDSKEEPER: self.lock_groundskeeper_out,
                locationNames.EXTRA_TASK_CABBAGE: self.cabbage_picnic,
                locationNames.EXTRA_TASK_PUDDLE: self.trip_boy_in_puddle,
                locationNames.EXTRA_TASK_SCALES: self.make_scales_ding,
                locationNames.EXTRA_TASK_UMBRELLA: self.open_umbrella_on_tv,
                locationNames.EXTRA_TASK_BUY: self.make_groundskeeper_buyback,
                locationNames.EXTRA_TASK_FLOWERS: self.collect_five_flowers,
                locationNames.EXTRA_TASK_GARAGE: self.trap_boy_in_garage,
                locationNames.EXTRA_TASK_CATCH: self.catch_thrown_object,
                locationNames.EXTRA_TASK_THROWN: self.get_thrown_over_fence,
                locationNames.EXTRA_TASK_BUST: self.dress_up_bust_outside_items,
                locationNames.EXTRA_TASK_GOAL: self.score_goal,
                locationNames.EXTRA_TASK_BOAT: self.sail_boat_under_bridge,
                locationNames.EXTRA_TASK_RIBBON: self.perform_with_ribbon,
                locationNames.EXTRA_TASK_HAT: self.steal_woolen_hat,
            }

        # To Do (Quickly!!) Task Rules
        if self.world.options.include_speedrun_tasks.value:
            self.speedrun_task_rules = {
                locationNames.SPEEDRUN_TASK_GARDEN: self.speedrun_garden,
                locationNames.SPEEDRUN_TASK_HIGH_STREET: self.speedrun_high_street,
                locationNames.SPEEDRUN_TASK_BACK_GARDENS: self.speedrun_back_gardens,
                locationNames.SPEEDRUN_TASK_PUB: self.speedrun_pub,
            }

        # Item Pickup Rules
        if self.world.options.include_item_pickups.value:
            self.pickup_rules = {
                locationNames.PICKUP_RADIO: self.pickup_radio,
                locationNames.PICKUP_TROWEL: self.pickup_trowel,
                locationNames.PICKUP_KEYS: self.pickup_keys,
                locationNames.PICKUP_TULIP: self.pickup_tulip,
                locationNames.PICKUP_APPLE_1: self.pickup_apples,
                locationNames.PICKUP_JAM: self.pickup_jam,
                locationNames.PICKUP_PICNIC_MUG: self.pickup_picnic_mug,
                locationNames.PICKUP_THERMOS: self.pickup_thermos,
                locationNames.PICKUP_SANDWICH_R: self.pickup_sandwich,
                locationNames.PICKUP_SANDWICH_L: self.pickup_sandwich,
                locationNames.PICKUP_STRAW_HAT: self.pickup_straw_hat,
                locationNames.PICKUP_DRINK_CAN: self.pickup_drink_can,
                locationNames.PICKUP_TENNIS_BALL: self.pickup_tennis_ball,
                locationNames.PICKUP_GROUNDSKEEPERS_HAT: self.pickup_grounsdkeepers_hat,
                locationNames.PICKUP_APPLE_2: self.pickup_apples,
                locationNames.PICKUP_BOYS_GLASSES: self.pickup_boys_glasses,
                locationNames.PICKUP_HORN_RIMMED_GLASSES: self.pickup_horn_rimmed_glasses,
                locationNames.PICKUP_RED_GLASSES: self.pickup_red_glasses,
                locationNames.PICKUP_SUNGLASSES: self.pickup_sunglasses,
                locationNames.PICKUP_LOO_PAPER: self.pickup_loo_paper,
                locationNames.PICKUP_TOY_CAR: self.pickup_toy_car,
                locationNames.PICKUP_HAIRBRUSH: self.pickup_hairbrush,
                locationNames.PICKUP_TOOTHBRUSH: self.pickup_toothbrush,
                locationNames.PICKUP_STEREOSCOPE: self.pickup_stereoscope,
                locationNames.PICKUP_DISH_SOAP_BOTTLE: self.pickup_dish_soap_bottle,
                locationNames.PICKUP_TINNED_FOOD_BLUE: self.pickup_food_cans,
                locationNames.PICKUP_TINNED_FOOD_YELLOW: self.pickup_food_cans,
                locationNames.PICKUP_TINNED_FOOD_ORANGE: self.pickup_food_cans,
                locationNames.PICKUP_WEED_TOOL: self.pickup_weed_tools,
                locationNames.PICKUP_LILY_FLOWER: self.pickup_lily_flower,
                locationNames.PICKUP_ORANGE_1: self.pickup_oranges,
                locationNames.PICKUP_ORANGE_2: self.pickup_oranges,
                locationNames.PICKUP_ORANGE_3: self.pickup_oranges,
                locationNames.PICKUP_SHOP_TOMATO_1: self.pickup_tomatoes_high_street,
                locationNames.PICKUP_SHOP_TOMATO_2: self.pickup_tomatoes_high_street,
                locationNames.PICKUP_SHOP_TOMATO_3: self.pickup_tomatoes_high_street,
                locationNames.PICKUP_SHOP_CARROT_1: self.pickup_carrots_high_street,
                locationNames.PICKUP_SHOP_CARROT_2: self.pickup_carrots_high_street,
                locationNames.PICKUP_SHOP_CARROT_3: self.pickup_carrots_high_street,
                locationNames.PICKUP_CUCUMBER_1: self.pickup_cucumbers,
                locationNames.PICKUP_CUCUMBER_2: self.pickup_cucumbers,
                locationNames.PICKUP_CUCUMBER_3: self.pickup_cucumbers,
                locationNames.PICKUP_LEEK_1: self.pickup_leeks,
                locationNames.PICKUP_LEEK_2: self.pickup_leeks,
                locationNames.PICKUP_LEEK_3: self.pickup_leeks,
                locationNames.PICKUP_TOY_PLANE: self.pickup_fusilage,
                locationNames.PICKUP_PINT_BOTTLE_1: self.pickup_pint_bottle_hub,
                locationNames.PICKUP_PINT_BOTTLE_2: self.pickup_pint_bottle_high_street,
                locationNames.PICKUP_PINT_BOTTLE_3: self.pickup_pint_bottle_high_street,
                locationNames.PICKUP_SPRAY_BOTTLE: self.pickup_spray_bottle,
                locationNames.PICKUP_WALKIE_TALKIE_1: self.pickup_walkie_talkies,
                locationNames.PICKUP_WALKIE_TALKIE_2: self.pickup_walkie_talkies,
                locationNames.PICKUP_APPLE_CORE_1: self.pickup_apple_cores,
                locationNames.PICKUP_APPLE_CORE_2: self.pickup_apple_cores,
                locationNames.PICKUP_DUSTBIN_LID: self.pickup_dustbin_lid,
                locationNames.PICKUP_CHALK: self.pickup_chalk,
                locationNames.PICKUP_GARDEN_FORK: self.pickup_weed_tools,
                locationNames.PICKUP_RIBBON_RED: self.pickup_red_bow,
                locationNames.PICKUP_BLUE_RIBBON: self.pickup_blue_bow,
                locationNames.PICKUP_DUMMY: self.pickup_dummy,
                locationNames.PICKUP_CRICKET_BALL: self.pickup_cricket_ball,
                locationNames.PICKUP_BUST_PIPE: self.pickup_bust_pipe,
                locationNames.PICKUP_BUST_HAT: self.pickup_bust_hat,
                locationNames.PICKUP_BUST_GLASSES: self.pickup_bust_glasses,
                locationNames.PICKUP_SLIPPER_R: self.pickup_slippers,
                locationNames.PICKUP_SLIPPER_L: self.pickup_slippers,
                locationNames.PICKUP_TEA_CUP: self.pickup_tea_cup,
                locationNames.PICKUP_NEWSPAPER: self.pickup_newspaper,
                locationNames.PICKUP_SOCK_1: self.pickup_socks,
                locationNames.PICKUP_SOCK_2: self.pickup_socks,
                locationNames.PICKUP_VASE: self.pickup_vase,
                locationNames.PICKUP_POT_STACK: self.pickup_pot_stack,
                locationNames.PICKUP_SOAP: self.pickup_soap,
                locationNames.PICKUP_PAINTBRUSH: self.pickup_paintbrush,
                locationNames.PICKUP_VASE_PIECE_1: self.pickup_vase_pieces,
                locationNames.PICKUP_VASE_PIECE_2: self.pickup_vase_pieces,
                locationNames.PICKUP_BRA: self.pickup_bra,
                locationNames.PICKUP_BADMINTON_RACKET: self.pickup_badminton_racket,
                locationNames.PICKUP_ROSE: self.pickup_rose,
                locationNames.PICKUP_FISHING_BOBBER: self.pickup_fishing_bobber,
                locationNames.PICKUP_LETTER: self.pickup_exit_letter,
                locationNames.PICKUP_PLATE_1: self.pickup_plates,
                locationNames.PICKUP_PLATE_2: self.pickup_plates,
                locationNames.PICKUP_PLATE_3: self.pickup_plates,
                locationNames.PICKUP_GREEN_QUOIT_1: self.pickup_green_quoits,
                locationNames.PICKUP_GREEN_QUOIT_2: self.pickup_green_quoits,
                locationNames.PICKUP_GREEN_QUOIT_3: self.pickup_green_quoits,
                locationNames.PICKUP_RED_QUOIT_1: self.pickup_red_quoits,
                locationNames.PICKUP_RED_QUOIT_2: self.pickup_red_quoits,
                locationNames.PICKUP_RED_QUOIT_3: self.pickup_red_quoits,
                locationNames.PICKUP_FORK_1: self.pickup_forks,
                locationNames.PICKUP_FORK_2: self.pickup_forks,
                locationNames.PICKUP_KNIFE_1: self.pickup_knives,
                locationNames.PICKUP_KNIFE_2: self.pickup_knives,
                locationNames.PICKUP_CORK: self.pickup_cork,
                locationNames.PICKUP_CANDLESTICK: self.pickup_candlestick,
                locationNames.PICKUP_FLOWER_FOR_VASE: self.pickup_vase_flower,
                locationNames.PICKUP_DART_1: self.pickup_darts,
                locationNames.PICKUP_DART_2: self.pickup_darts,
                locationNames.PICKUP_DART_3: self.pickup_darts,
                locationNames.PICKUP_HARMONICA: self.pickup_harmonica,
                locationNames.PICKUP_PINT_GLASS: self.pickup_pint_glass,
                locationNames.PICKUP_TOY_BOAT: self.pickup_toy_boat,
                locationNames.PICKUP_OLD_MANS_WOOLEN_HAT: self.pickup_woolen_hat,
                locationNames.PICKUP_PEPPER_GRINDER: self.pickup_pepper_grinder,
                locationNames.PICKUP_PUB_WOMANS_CLOTH: self.pickup_pub_woman_cloth,
                locationNames.PICKUP_MINI_PERSON_CHILD: self.pickup_people_miniatures,
                locationNames.PICKUP_MINI_PERSON_JUMPSUIT: self.pickup_people_miniatures,
                locationNames.PICKUP_MINI_PERSON_GARDENER: self.pickup_people_miniatures,
                locationNames.PICKUP_MINI_PERSON_OLD_WOMAN: self.pickup_people_miniatures,
                locationNames.PICKUP_MINI_PERSON_POSTIE: self.pickup_people_miniatures,
                locationNames.PICKUP_MINI_PERSON_VEST_MAN: self.pickup_people_miniatures,
                locationNames.PICKUP_MINI_PERSON: self.pickup_people_miniatures,
                locationNames.PICKUP_MINI_GOOSE: self.pickup_mini_goose,
                locationNames.PICKUP_MINI_SHOVEL: self.pickup_mini_shovel,
                locationNames.PICKUP_POPPY_FLOWER: self.pickup_poppy,
                locationNames.PICKUP_MINI_PHONE_DOOR: self.pickup_mini_phone_booth,
                locationNames.PICKUP_MINI_MAIL_PILLAR: self.pickup_mini_mail_pillar,
                locationNames.PICKUP_TIMBER_HANDLE: self.pickup_timber_handle,
                locationNames.PICKUP_GOLDEN_BELL: self.pickup_golden_bell,
                locationNames.PICKUP_CARROT_1: self.pickup_garden_carrots,
                locationNames.PICKUP_CARROT_2: self.pickup_garden_carrots,
                locationNames.PICKUP_CARROT_3: self.pickup_garden_carrots,
                locationNames.PICKUP_CARROT_4: self.pickup_garden_carrots,
                locationNames.PICKUP_CARROT_5: self.pickup_garden_carrots,
                locationNames.PICKUP_CARROT_6: self.pickup_garden_carrots,
                locationNames.PICKUP_CARROT_7: self.pickup_garden_carrots,
                locationNames.PICKUP_CARROT_8: self.pickup_garden_carrots,
                locationNames.PICKUP_CARROT_9: self.pickup_garden_carrots,
                locationNames.PICKUP_CARROT_10: self.pickup_garden_carrots,
                locationNames.PICKUP_PUB_TOMATO_1: self.pickup_pub_boxed_tomatoes,
                locationNames.PICKUP_PUB_TOMATO_2: self.pickup_pub_boxed_tomatoes,
                locationNames.PICKUP_PUB_TOMATO_3: self.pickup_pub_boxed_tomatoes,
                locationNames.PICKUP_PUB_TOMATO_4: self.pickup_pub_boxed_tomatoes,
                locationNames.PICKUP_PUB_TOMATO_5: self.pickup_pub_boxed_tomatoes,
                locationNames.PICKUP_PUB_TOMATO_6: self.pickup_pub_boxed_tomatoes,
                locationNames.PICKUP_PUB_TOMATO_7: self.pickup_pub_boxed_tomatoes,
                locationNames.PICKUP_PUB_TOMATO_8: self.pickup_pub_boxed_tomatoes,
                locationNames.PICKUP_PUB_TOMATO_9: self.pickup_pub_boxed_tomatoes,
                locationNames.PICKUP_PUB_TOMATO_10: self.pickup_pub_open_tomatoes,
                locationNames.PICKUP_PUB_TOMATO_11: self.pickup_pub_open_tomatoes,
                locationNames.PICKUP_BOOT_START: self.pickup_boots,
                locationNames.PICKUP_BOOT_HUB: self.pickup_boots,
            }

        # Item Drag Rules
        if self.world.options.include_drag_items.value:
            self.drag_rules = {
                locationNames.DRAG_RAKE: self.drag_rake,
                locationNames.DRAG_PICNIC_BASKET: self.drag_picnic_basket,
                locationNames.DRAG_ESKY: self.drag_esky,
                locationNames.DRAG_SHOVEL: self.drag_shovel,
                locationNames.DRAG_PUMKPIN_1: self.drag_pumpkins,
                locationNames.DRAG_PUMKPIN_2: self.drag_pumpkins,
                locationNames.DRAG_PUMKPIN_3: self.drag_pumpkins,
                locationNames.DRAG_PUMKPIN_4: self.drag_pumpkins,
                locationNames.DRAG_WATERING_CAN: self.drag_watering_can,
                locationNames.DRAG_GUMBOOT_1: self.drag_gumboots,
                locationNames.DRAG_GUMBOOT_2: self.drag_gumboots,
                locationNames.DRAG_NO_GOOSE_SIGN_GARDEN: self.drag_gardener_sign,
                locationNames.DRAG_WOODEN_CRATE: self.drag_wooden_crate,
                locationNames.DRAG_FENCE_BOLT: self.drag_fence_bolt,
                locationNames.DRAG_MALLET: self.drag_mallet,
                locationNames.DRAG_SHOPPING_BASKET: self.drag_shopping_basket,
                locationNames.DRAG_UMBRELLA_BLACK: self.drag_umbrellas,
                locationNames.DRAG_UMBRELLA_RAINBOW: self.drag_umbrellas,
                locationNames.DRAG_UMBRELLA_RED: self.drag_umbrellas,
                locationNames.DRAG_PUSH_BROOM: self.drag_push_broom,
                locationNames.DRAG_BROKEN_BROOM_HEAD: self.drag_broom_head,
                locationNames.DRAG_DUSTBIN: self.drag_dustbin,
                locationNames.DRAG_BABY_DOLL: self.drag_baby_doll,
                locationNames.DRAG_PRICING_GUN: self.drag_pricing_gun,
                locationNames.DRAG_ADDING_MACHINE: self.drag_adding_machine,
                locationNames.DRAG_ROSE_BOX: self.drag_rose_box,
                locationNames.DRAG_CRICKET_BAT: self.drag_cricket_bat,
                locationNames.DRAG_TEA_POT: self.drag_tea_pot,
                locationNames.DRAG_CLIPPERS: self.drag_clippers,
                locationNames.DRAG_DUCK_STATUE: self.drag_duck_statue,
                locationNames.DRAG_FROG_STATUE: self.drag_frog_statue,
                locationNames.DRAG_JEREMY_FISH: self.drag_jeremy_fish,
                locationNames.DRAG_NO_GOOSE_SIGN_MESSY: self.drag_messy_sign,
                locationNames.DRAG_DRAWER: self.drag_drawer,
                locationNames.DRAG_ENAMEL_JUG: self.drag_enamel_jug,
                locationNames.DRAG_NO_GOOSE_SIGN_CLEAN: self.drag_clean_sign,
                locationNames.DRAG_TACKLE_BOX: self.drag_tackle_box,
                locationNames.DRAG_TRAFFIC_CONE: self.drag_traffic_cone,
                locationNames.DRAG_PARCEL: self.drag_exit_parcel,
                locationNames.DRAG_STEALTH_BOX: self.drag_stealth_box,
                locationNames.DRAG_NO_GOOSE_SIGN_PUB: self.drag_no_goose_sign,
                locationNames.DRAG_PORTABLE_STOOL: self.drag_portable_stool,
                locationNames.DRAG_DARTBOARD: self.drag_dartboard,
                locationNames.DRAG_MOP_BUCKET: self.drag_mop_bucket,
                locationNames.DRAG_MOP: self.drag_mop,
                locationNames.DRAG_DELIVERY_BOX: self.drag_delivery_box,
                locationNames.DRAG_BUCKET: self.drag_burly_mans_bucket,
                locationNames.DRAG_MINI_BENCH: self.drag_mini_benches,
                locationNames.DRAG_MINI_PUMP: self.drag_mini_pump,
                locationNames.DRAG_MINI_STREET_BENCH: self.drag_mini_benches,
                locationNames.DRAG_MINI_BIRDBATH: self.drag_mini_birdbath,
                locationNames.DRAG_MINI_EASEL: self.drag_mini_easel,
                locationNames.DRAG_MINI_SUN_LOUNGE: self.drag_sun_lounge,
                locationNames.DRAG_TOPSOIL_BAG_1: self.drag_topsoil_bags,
                locationNames.DRAG_TOPSOIL_BAG_2: self.drag_topsoil_bags,
                locationNames.DRAG_TOPSOIL_BAG_3: self.drag_topsoil_bags,
            }

        # Interaction Rules
        if self.world.options.include_interactions.value:
            self.interaction_rules = {
                locationNames.INTERACT_BIKE_BELL: self.interact_bike_bell,
                locationNames.INTERACT_GARDEN_TAP: self.interact_garden_water,
                locationNames.INTERACT_SPRINKLER: self.interact_garden_water,
                locationNames.INTERACT_UNPLUG_RADIO: self.interact_radio,
                locationNames.INTERACT_UMBRELLA_BLACK: self.interact_umbrellas,
                locationNames.INTERACT_UMBRELLA_RAINBOW: self.interact_umbrellas,
                locationNames.INTERACT_UMBRELLA_RED: self.interact_umbrellas,
                locationNames.INTERACT_BOYS_LACES_L: self.interact_boys_laces,
                locationNames.INTERACT_BOYS_LACES_R: self.interact_boys_laces,
                locationNames.INTERACT_FOOTBALL: self.interact_football,
                locationNames.INTERACT_RING_BELL: self.interact_back_gardens_objects,
                locationNames.INTERACT_WINDMILL: self.interact_back_gardens_objects,
                locationNames.INTERACT_PURPLE_FLOWER: self.interact_back_gardens_objects,
                locationNames.INTERACT_TRELLIS: self.interact_trellis,
                locationNames.INTERACT_SUNFLOWER: self.interact_back_gardens_objects,
                locationNames.INTERACT_TOPIARY: self.interact_back_gardens_objects,
                locationNames.INTERACT_WIND_CHIME_C: self.interact_back_gardens_objects,
                locationNames.INTERACT_WIND_CHIME_D: self.interact_back_gardens_objects,
                locationNames.INTERACT_WIND_CHIME_E: self.interact_back_gardens_objects,
                locationNames.INTERACT_WIND_CHIME_F: self.interact_back_gardens_objects,
                locationNames.INTERACT_WIND_CHIME_G: self.interact_back_gardens_objects,
                locationNames.INTERACT_WIND_CHIME_A: self.interact_back_gardens_objects,
                locationNames.INTERACT_WIND_CHIME_B: self.interact_back_gardens_objects,
                locationNames.INTERACT_VAN_DOOR_L: self.interact_van_doors,
                locationNames.INTERACT_VAN_DOOR_R: self.interact_van_doors,
                locationNames.INTERACT_BURLY_MANS_LACES_L: self.interact_burly_laces,
                locationNames.INTERACT_BURLY_MANS_LACES_R: self.interact_burly_laces,
                locationNames.INTERACT_PUB_TAP: self.interact_pub_tap,
                locationNames.INTERACT_WELL: self.interact_well,
            }

        # New Tasks Rules
        if self.world.options.include_new_tasks.value:
            self.new_tasks_rules = {
                locationNames.SHORT_OUT_RADIO: self.short_out_radio,
                locationNames.LOCK_GROUNDSKEEPER_IN: self.lock_groundskeeper_out,
                locationNames.OPEN_INTRO_GATE: self.interact_intro_gate,
                locationNames.DROP_MAIL_IN_WELL: self.drop_mail_in_well,
                locationNames.BREAK_THROUGH_BOARDS: self.interact_boards,
                locationNames.MAKE_WOMAN_FIX_TOPIARY: self.interact_make_woman_fix_topiary,
                locationNames.POSE_AS_DUCK: self.pose_as_duck_statue,
                locationNames.DRESS_UP_BUSH: self.dress_up_bush,
                locationNames.INTERIOR_REDECORATING: self.drag_messy_sign,
                locationNames.TRIP_BURLY_MAN: self.interact_burly_laces,
                locationNames.BREAK_PINT_GLASS: self.pickup_pint_glass,
                locationNames.TRAP_TV_SHOP_OWNER_GARAGE: self.trap_tv_shop_owner_in_garage,
                locationNames.PERFORM_WITH_HARMONICA: self.perform_with_harmonica,
            }

        # Model Church Pecking Rules
        if self.world.options.include_model_church_pecks.value == 1:
            self.church_first_peck_rules = {
                locationNames.PECK_DOORWAY: self.peck_church,
                locationNames.PECK_TOWER: self.peck_church,
            }
        elif self.world.options.include_model_church_pecks.value == 2:
            self.church_all_peck_rules = {
                locationNames.PECK_DOORWAY_1: self.peck_church,
                locationNames.PECK_DOORWAY_2: self.peck_church,
                locationNames.PECK_DOORWAY_3: self.peck_church,
                locationNames.PECK_DOORWAY_4: self.peck_church,
                locationNames.PECK_DOORWAY_5: self.peck_church,
                locationNames.PECK_DOORWAY_6: self.peck_church,
                locationNames.PECK_DOORWAY_7: self.peck_church,
                locationNames.PECK_DOORWAY_8: self.peck_church,
                locationNames.PECK_DOORWAY_9: self.peck_church,
                locationNames.PECK_DOORWAY_10: self.peck_church,
                locationNames.PECK_DOORWAY_11: self.peck_church,
                locationNames.PECK_DOORWAY_12: self.peck_church,
                locationNames.PECK_DOORWAY_13: self.peck_church,
                locationNames.PECK_DOORWAY_14: self.peck_church,
                locationNames.PECK_DOORWAY_15: self.peck_church,
                locationNames.PECK_DOORWAY_16: self.peck_church,
                locationNames.PECK_DOORWAY_17: self.peck_church,
                locationNames.PECK_DOORWAY_18: self.peck_church,
                locationNames.PECK_DOORWAY_19: self.peck_church,
                locationNames.PECK_TOWER_1: self.peck_church,
                locationNames.PECK_TOWER_2: self.peck_church,
                locationNames.PECK_TOWER_3: self.peck_church,
                locationNames.PECK_TOWER_4: self.peck_church,
                locationNames.PECK_TOWER_5: self.peck_church,
                locationNames.PECK_TOWER_6: self.peck_church,
                locationNames.PECK_TOWER_7: self.peck_church,
                locationNames.PECK_TOWER_8: self.peck_church,
                locationNames.PECK_TOWER_9: self.peck_church,
                locationNames.PECK_TOWER_10: self.peck_church,
                locationNames.PECK_TOWER_11: self.peck_church,
                locationNames.PECK_TOWER_12: self.peck_church,
                locationNames.PECK_TOWER_13: self.peck_church,
                locationNames.PECK_TOWER_14: self.peck_church,
                locationNames.PECK_TOWER_15: self.peck_church,
                locationNames.PECK_TOWER_16: self.peck_church,
            }

        # Milestone Rules
        if self.world.options.include_milestone_locations.value and self.world.options.include_extra_tasks.value and self.world.options.include_speedrun_tasks.value:
            self.all_milestone_rules = {
                locationNames.MILESTONE_ALL_GARDEN: self.all_garden_tasks,
                locationNames.MILESTONE_ALL_HIGH_STREET: self.all_high_street_tasks,
                locationNames.MILESTONE_ALL_BACK_GARDENS: self.all_back_gardens_tasks,
                locationNames.MILESTONE_ALL_PUB: self.all_pub_tasks,
                locationNames.MILESTONE_ALL_MAIN: self.all_main_task_lists,
                locationNames.MILESTONE_ALL_EXTRA: self.all_to_do_as_well_tasks,
                locationNames.MILESTONE_ALL_SPEEDRUN: self.all_speedrun_tasks,
                locationNames.MILESTONE_ALL_TASKS: self.all_tasks_complete,
            }
        elif self.world.options.include_milestone_locations.value and self.world.options.include_extra_tasks.value:
            self.non_speedrun_milestone_rules = {
                locationNames.MILESTONE_ALL_GARDEN: self.all_garden_tasks,
                locationNames.MILESTONE_ALL_HIGH_STREET: self.all_high_street_tasks,
                locationNames.MILESTONE_ALL_BACK_GARDENS: self.all_back_gardens_tasks,
                locationNames.MILESTONE_ALL_PUB: self.all_pub_tasks,
                locationNames.MILESTONE_ALL_MAIN: self.all_main_task_lists,
                locationNames.MILESTONE_ALL_EXTRA: self.all_to_do_as_well_tasks,
            }
        elif self.world.options.include_milestone_locations.value and self.world.options.include_speedrun_tasks.value:
            self.non_to_do_as_well_milestone_rules = {
                locationNames.MILESTONE_ALL_GARDEN: self.all_garden_tasks,
                locationNames.MILESTONE_ALL_HIGH_STREET: self.all_high_street_tasks,
                locationNames.MILESTONE_ALL_BACK_GARDENS: self.all_back_gardens_tasks,
                locationNames.MILESTONE_ALL_PUB: self.all_pub_tasks,
                locationNames.MILESTONE_ALL_MAIN: self.all_main_task_lists,
                locationNames.MILESTONE_ALL_SPEEDRUN: self.all_speedrun_tasks,
            }
        elif self.world.options.include_milestone_locations.value:
            self.basic_milestone_rules = {
                locationNames.MILESTONE_ALL_GARDEN: self.all_garden_tasks,
                locationNames.MILESTONE_ALL_HIGH_STREET: self.all_high_street_tasks,
                locationNames.MILESTONE_ALL_BACK_GARDENS: self.all_back_gardens_tasks,
                locationNames.MILESTONE_ALL_PUB: self.all_pub_tasks,
                locationNames.MILESTONE_ALL_MAIN: self.all_main_task_lists,
            }

        # Goals
        if self.world.options.goal.value == 0:
            self.simple_goal_rules = {
                locationNames.GOAL_MODEL_VILLAGE_ENTRY: self.get_into_model_village,
            }
        # elif self.world.options.goal.value == 1:\
            # No special locations
        elif self.world.options.goal.value == 2:
            self.all_main_tasks_goal_rules = {
                locationNames.GOAL_ALL_MAIN: self.all_main_task_lists,
            }
        elif self.world.options.goal.value == 3:
            self.all_speedrun_tasks_goal_rules = {
                locationNames.GOAL_ALL_SPEEDRUN: self.all_speedrun_tasks,
            }
        elif self.world.options.goal.value == 4:
            self.all_non_speedrun_tasks_goal_rules = {
                locationNames.GOAL_ALL_NON_SPEEDRUN: self.all_non_speedrun_tasks,
            }
        elif self.world.options.goal.value == 5:
            self.all_tasks_goal_rules = {
                locationNames.GOAL_ALL_TASKS: self.all_tasks_complete,
            }
        elif self.world.options.goal.value == 6:
            self.four_final_tasks_rules = {
                locationNames.GOAL_ALL_FINAL_TASKS: self.four_final_tasks,
            }
        
        # Main Task Rules
        self.main_tasks_rules = {
            locationNames.TASK_GARDEN_ENTRY: self.get_into_garden,
            locationNames.TASK_GARDEN_WET: self.get_groundskeeper_wet,
            locationNames.TASK_GARDEN_KEYS: self.steal_groundskeepers_keys,
            locationNames.TASK_GARDEN_HAT: self.make_groundskeeper_wear_sun_hat,
            locationNames.TASK_GARDEN_RAKE: self.rake_in_lake,
            locationNames.TASK_GARDEN_PICNIC: self.picnic,
            locationNames.TASK_GARDEN_FINAL: self.make_groundskeeper_hammer_thumb,
            locationNames.TASK_HIGH_STREET_BROOM: self.break_broom,
            locationNames.TASK_HIGH_STREET_PHONE: self.trap_boy_in_phone_booth,
            locationNames.TASK_HIGH_STREET_GLASSES: self.make_boy_wear_wrong_glasses,
            locationNames.TASK_HIGH_STREET_BUY: self.make_someone_buyback,
            locationNames.TASK_HIGH_STREET_TV: self.get_on_tv,
            locationNames.TASK_HIGH_STREET_SHOPPING: self.go_shopping,
            locationNames.TASK_HIGH_STREET_FINAL: self.trap_shopkeep_in_garage,
            locationNames.TASK_BACK_GARDENS_VASE: self.make_someone_break_vase,
            locationNames.TASK_BACK_GARDENS_BUST: self.dress_up_bust,
            locationNames.TASK_BACK_GARDENS_TEA: self.make_man_spit_out_tea,
            locationNames.TASK_BACK_GARDENS_RIBBON: self.get_dressed_up,
            locationNames.TASK_BACK_GARDENS_BAREFOOT: self.make_man_barefoot,
            locationNames.TASK_BACK_GARDENS_WASHING: self.do_washing,
            locationNames.TASK_BACK_GARDENS_FINAL: self.make_someone_prune_rose,
            locationNames.TASK_PUB_ENTRY: self.get_into_pub,
            locationNames.TASK_PUB_DARTBOARD: self.break_dartboard,
            locationNames.TASK_PUB_BOAT: self.get_toy_boat,
            locationNames.TASK_PUB_BUM: self.make_old_man_fall_on_bum,
            locationNames.TASK_PUB_FLOWER: self.be_awarded_flower,
            locationNames.TASK_PUB_PINT: self.drop_pint_glass_in_canal,
            locationNames.TASK_PUB_TABLE: self.set_table,
            locationNames.TASK_PUB_FINAL: self.drop_bucket_on_burly_man,
        }
        
        # Model Village Rules/Victory Rules
        self.victory_rules = {
            locationNames.TASK_MODEL_VILLAGE_ENTRY: self.get_into_model_village,
            locationNames.TASK_MODEL_VILLAGE_BELL: self.steal_bell,
            locationNames.TASK_MODEL_VILLAGE_VICTORY: self.steal_bell,
        }
    
    
    # ----- Region Defs -----
    
    def has_area(self, state: CollectionState, area) -> bool:
        return state.has(f"{area} Access", self.player)

    def has_garden(self, state: CollectionState) -> bool:
        return self.has_area(state, regionNames.GARDEN)

    def has_high_street(self, state: CollectionState) -> bool:
        return self.has_area(state, regionNames.HIGH_STREET)

    def has_back_gardens(self, state: CollectionState) -> bool:
        return self.has_area(state, regionNames.BACK_GARDENS)

    def has_pub(self, state: CollectionState) -> bool:
        return self.has_area(state, regionNames.PUB)

    def has_model_village(self, state: CollectionState) -> bool:
        return (
            self.has_area(state, regionNames.PUB)
            and self.has_area(state, regionNames.MODEL_VILLAGE)
        )
    
    
    # ----- Souls Defs -----

    def has_npc(self, state: CollectionState, npc_soul) -> bool:
        if self.world.options.include_npc_souls.value:
            return state.has(f"{npc_soul}", self.player)
        return True
    
    def has_prop(self, state: CollectionState, prop) -> bool:
        if self.world.options.include_prop_souls.value:
            return state.has(f"{prop}", self.player)
        return True
    
    
    # ----- Garden Task Rule Defs -----
    
    def get_into_garden(self, state: CollectionState) -> bool:
        return self.has_garden(state)
    
    def get_groundskeeper_wet(self, state: CollectionState) -> bool:
        return (
            self.has_garden(state)
            and self.has_npc(state, itemNames.NPC_GROUNDSKEEPER)
        )
    
    def steal_groundskeepers_keys(self, state: CollectionState) -> bool:
        return (
            self.has_garden(state)
            and self.has_npc(state, itemNames.NPC_GROUNDSKEEPER)
        )
    
    def make_groundskeeper_wear_sun_hat(self, state: CollectionState) -> bool:
        return (
            self.pickup_grounsdkeepers_hat(state)
            and self.has_prop(state, itemNames.PROP_STRAW_HAT)
        )
    
    def rake_in_lake(self, state: CollectionState) -> bool:
        return (
            self.has_garden(state)
            and self.has_prop(state, itemNames.PROP_RAKE)
        )
    
    def picnic(self, state: CollectionState) -> bool:
        return (
            self.has_garden(state)
            and self.has_prop(state, itemNames.PROP_SANDWICH)
            and self.has_prop(state, itemNames.PROP_APPLES)
            and self.has_prop(state, itemNames.PROP_PUMPKINS)
            and self.has_prop(state, itemNames.PROP_CARROTS)
            and self.has_prop(state, itemNames.PROP_JAM)
            and self.has_prop(state, itemNames.PROP_THERMOS)
            and self.has_prop(state, itemNames.PROP_RADIO)
            and self.has_prop(state, itemNames.PROP_PICNIC_BASKET)
        )
    
    def make_groundskeeper_hammer_thumb(self, state: CollectionState) -> bool:
        task_count = 0
        
        if self.get_into_garden(state):
            task_count += 1
        if self.get_groundskeeper_wet(state):
            task_count += 1
        if self.steal_groundskeepers_keys(state):
            task_count += 1
        if self.make_groundskeeper_wear_sun_hat(state):
            task_count += 1
        if self.rake_in_lake(state):
            task_count += 1
        if self.picnic(state):
            task_count += 1
        
        return (
            self.has_npc(state, itemNames.NPC_GROUNDSKEEPER)
            and self.has_prop(state, itemNames.PROP_MALLET)
            and task_count >= 5
        )
    
    
    # ----- High Street Task Rule Defs -----
    
    def break_broom(self, state: CollectionState) -> bool:
        return (
            self.has_high_street(state)
            and self.has_npc(state, itemNames.NPC_MARKET_LADY)
            and self.has_prop(state, itemNames.PROP_PUSH_BROOM)
        )
    
    def trap_boy_in_phone_booth(self, state: CollectionState) -> bool:
        return (
            self.has_high_street(state)
            and self.has_npc(state, itemNames.NPC_BOY)
            and self.has_npc(state, itemNames.NPC_TV_SHOP_OWNER)
            and self.has_prop(state, itemNames.PROP_GARAGE_ROPE)
        )
    
    def make_boy_wear_wrong_glasses(self, state: CollectionState) -> bool:
        return (
            self.has_high_street(state)
            and self.has_npc(state, itemNames.NPC_BOY)
            and (
                self.has_prop(state, itemNames.PROP_HORN_RIMMED_GLASSES)
                or self.has_prop(state, itemNames.PROP_RED_GLASSES) 
                or self.has_prop(state, itemNames.PROP_SUNGLASSES)
            )
        )
    
    def make_someone_buyback(self, state: CollectionState) -> bool:
        return (
            self.has_high_street(state)
            and self.has_npc(state, itemNames.NPC_MARKET_LADY)
            and (
                self.has_npc(state, itemNames.NPC_BOY) and self.has_prop(state, itemNames.PROP_TOY_PLANE)
                or self.has_garden(state) and self.has_npc(state, itemNames.NPC_GROUNDSKEEPER) and self.has_prop(state, itemNames.PROP_TROWEL)
            )
        )
    
    def get_on_tv(self, state: CollectionState) -> bool:
        return (
            self.has_high_street(state)
            and self.has_npc(state, itemNames.NPC_TV_SHOP_OWNER)
            and (
                self.has_npc(state, itemNames.NPC_BOY)
                or self.has_prop(state, itemNames.PROP_WALKIE_TALKIES)
            )
        )
    
    def go_shopping(self, state: CollectionState) -> bool:
        return (
            self.has_high_street(state)
            and self.has_prop(state, itemNames.PROP_SHOPPING_BASKET)
            and self.has_prop(state, itemNames.PROP_TOOTHRBRUSH)
            and self.has_prop(state, itemNames.PROP_HAIRBRUSH)
            and self.has_prop(state, itemNames.PROP_LOO_PAPER)
            and self.has_prop(state, itemNames.PROP_TINNED_FOOD)
            and (
                self.has_prop(state, itemNames.PROP_DISH_SOAP_BOTTLE)
                or self.has_prop(state, itemNames.PROP_SPRAY_BOTTLE)
            )
            and (
                self.has_prop(state, itemNames.PROP_ORANGES)
                or self.has_prop(state, itemNames.PROP_CUCUMBERS)
                or self.has_prop(state, itemNames.PROP_LEEKS)
                or self.has_prop(state, itemNames.PROP_CARROTS)
                or self.has_prop(state, itemNames.PROP_TOMATOES)
                # TO DO: Test if apple cores work
                or self.has_garden(state) and self.has_prop(state, itemNames.PROP_APPLES)
            )
        )
    
    def trap_shopkeep_in_garage(self, state: CollectionState) -> bool:
        task_count = 0
        
        if self.break_broom(state):
            task_count += 1
        if self.trap_boy_in_phone_booth(state):
            task_count += 1
        if self.make_boy_wear_wrong_glasses(state):
            task_count += 1
        if self.make_someone_buyback(state):
            task_count += 1
        if self.get_on_tv(state):
            task_count += 1
        if self.go_shopping(state):
            task_count += 1
        
        return (
            self.has_npc(state, itemNames.NPC_MARKET_LADY)
            and self.has_prop(state, itemNames.PROP_CHALK)
            and self.has_prop(state, itemNames.PROP_GARAGE_ROPE)
            and task_count >= 5
        )
    
    
    # ----- Back Gardens Task Rule Defs -----
    
    def make_someone_break_vase(self, state: CollectionState) -> bool:
        return (
            self.has_back_gardens(state)
            and self.has_npc(state, itemNames.NPC_TIDY_NEIGHBOUR)
            and self.has_prop(state, itemNames.PROP_VASE)
            and self.has_prop(state, itemNames.PROP_DRAWER)
        )
    
    def make_man_spit_out_tea(self, state: CollectionState) -> bool:
        return (
            self.has_back_gardens(state)
            and self.has_npc(state, itemNames.NPC_TIDY_NEIGHBOUR)
            and self.has_prop(state, itemNames.NPC_MESSY_NEIGHBOUR)
            and self.has_prop(state, itemNames.PROP_TEA_CUP)
        )
    
    def get_dressed_up(self, state: CollectionState) -> bool:
        return (
            self.has_back_gardens(state)
            and self.has_npc(state, itemNames.NPC_MESSY_NEIGHBOUR)
            and self.has_prop(state, itemNames.PROP_DUCK_STATUE)
            and self.has_prop(state, itemNames.PROP_RIBBONS)
        )
    
    def make_man_barefoot(self, state: CollectionState) -> bool:
        return (
            self.has_back_gardens(state)
            and self.has_npc(state, itemNames.NPC_TIDY_NEIGHBOUR)
        )
    
    def do_washing(self, state: CollectionState) -> bool:
        return (
            self.has_back_gardens(state)
            and self.has_npc(state, itemNames.NPC_TIDY_NEIGHBOUR)
            and self.has_prop(state, itemNames.PROP_DRAWER)
            and self.has_prop(state, itemNames.PROP_SOCKS)
            and self.has_prop(state, itemNames.PROP_BRA)
            and self.has_prop(state, itemNames.PROP_SOAP)
        )
    
    def dress_up_bust(self, state: CollectionState) -> bool:
        return (
            self.has_back_gardens(state)
            and self.has_npc(state, itemNames.NPC_MESSY_NEIGHBOUR)
            and self.has_prop(state, itemNames.PROP_DRAWER)
            and (
                self.has_prop(state, itemNames.PROP_BUST_HAT)
                or self.has_garden(state) and self.has_npc(state, itemNames.NPC_GROUNDSKEEPER)
                or self.has_pub(state) and (
                    self.has_prop(state, itemNames.PROP_TRAFFIC_CONE)
                    or self.has_npc(state, itemNames.NPC_OLD_MAN)
                )
            )
            and (
                self.has_prop(state, itemNames.PROP_BUST_GLASSES)
                or self.has_high_street(state) and (
                    self.has_prop(state, itemNames.PROP_HORN_RIMMED_GLASSES)
                    or self.has_prop(state, itemNames.PROP_RED_GLASSES)
                    or self.has_prop(state, itemNames.PROP_SUNGLASSES)
                    or self.has_prop(state, itemNames.PROP_STEREOSCOPE)
                    or self.has_npc(state, itemNames.NPC_BOY)
                )
            )
            and (
                self.has_prop(state, itemNames.PROP_BUST_PIPE)
                or self.has_prop(state, itemNames.PROP_DUMMY)
                or self.has_garden(state) and self.has_prop(state, itemNames.PROP_TULIP)
                or self.has_high_street(state) and (
                    self.has_prop(state, itemNames.PROP_TOOTHRBRUSH)
                    or self.has_prop(state, itemNames.PROP_LILY_FLOWER)
                )
                or self.has_pub(state) and (
                    self.has_prop(state, itemNames.PROP_KNIVES)
                    or self.has_prop(state, itemNames.PROP_FORKS)
                    or self.has_prop(state, itemNames.PROP_HARMONICA)
                    or self.has_npc(state, itemNames.NPC_FANCY_LADIES) and self.has_prop(state, itemNames.PROP_FLOWER_FOR_VASE)
                )
                or self.has_model_village(state) and self.has_prop(state, itemNames.PROP_POPPY_FLOWER)
                or ( # Rose from completing all other Back Gardens tasks
                    self.make_someone_break_vase(state)
                    and self.make_man_spit_out_tea(state)
                    and self.get_dressed_up(state)
                    and self.make_man_barefoot(state)
                    and self.do_washing(state)
                    and self.has_prop(state, itemNames.PROP_ROSE)
                    and self.has_prop(state, itemNames.PROP_ROSE_BOX)
                    and self.has_prop(state, itemNames.PROP_CLIPPERS)
                    and self.has_prop(state, itemNames.PROP_NO_GOOSE_SIGN_CLEAN)
                )
            )
        )
    
    def make_someone_prune_rose(self, state: CollectionState) -> bool:
        task_count = 0
        
        if self.make_someone_break_vase(state):
            task_count += 1
        if self.make_man_spit_out_tea(state):
            task_count += 1
        if self.get_dressed_up(state):
            task_count += 1
        if self.make_man_barefoot(state):
            task_count += 1
        if self.do_washing(state):
            task_count += 1
        if self.dress_up_bust(state):
            task_count += 1
        
        return (
            self.has_npc(state, itemNames.NPC_TIDY_NEIGHBOUR)
            and self.has_npc(state, itemNames.NPC_MESSY_NEIGHBOUR)
            and self.has_prop(state, itemNames.PROP_DRAWER)
            and self.has_prop(state, itemNames.PROP_ROSE)
            and self.has_prop(state, itemNames.PROP_ROSE_BOX)
            and self.has_prop(state, itemNames.PROP_CLIPPERS)
            and self.has_prop(state, itemNames.PROP_NO_GOOSE_SIGN_CLEAN)
            and task_count >= 5
        )
    
    
    # ----- Pub Task Rule Defs -----
    
    def get_into_pub(self, state: CollectionState) -> bool:
        return self.has_pub(state)
    
    def break_dartboard(self, state: CollectionState) -> bool:
        return (
            self.has_pub(state)
            and self.has_npc(state, itemNames.NPC_OLD_MAN)
            and self.has_prop(state, itemNames.PROP_DARTBOARD)
        )
    
    def get_toy_boat(self, state: CollectionState) -> bool:
        return (
            self.has_pub(state)
            and self.has_prop(state, itemNames.PROP_TOY_BOAT)
        )
    
    def make_old_man_fall_on_bum(self, state: CollectionState) -> bool:
        return (
            self.has_pub(state)
            and self.has_npc(state, itemNames.NPC_OLD_MAN)
            and self.has_prop(state, itemNames.PROP_PORTABLE_STOOL)
            and (
                self.has_prop(state, itemNames.PROP_DARTBOARD)
                or self.has_prop(state, itemNames.PROP_GREEN_QUOITS)
                or self.has_prop(state, itemNames.PROP_RED_QUOITS)
            )
        )
    
    def be_awarded_flower(self, state: CollectionState) -> bool:
        return (
            self.has_pub(state)
            and self.has_npc(state, itemNames.NPC_FANCY_LADIES)
            and self.has_prop(state, itemNames.PROP_FLOWER_FOR_VASE)
        )
    
    def drop_pint_glass_in_canal(self, state: CollectionState) -> bool:
        return (
            self.has_pub(state)
            and self.has_prop(state, itemNames.PROP_PINT_GLASSES)
        )
    
    def set_table(self, state: CollectionState) -> bool:
        return (
            self.has_pub(state)
            and self.has_prop(state, itemNames.PROP_PLATES)
            and self.has_prop(state, itemNames.PROP_FORKS)
            and self.has_prop(state, itemNames.PROP_KNIVES)
            and self.has_prop(state, itemNames.PROP_PEPPER_GRINDER)
            and self.has_prop(state, itemNames.PROP_CANDLESTICK)
        )
    
    def drop_bucket_on_burly_man(self, state: CollectionState) -> bool:
        task_count = 0
        
        if self.get_into_pub(state):
            task_count += 1
        if self.break_dartboard(state):
            task_count += 1
        if self.get_toy_boat(state):
            task_count += 1
        if self.make_old_man_fall_on_bum(state):
            task_count += 1
        if self.be_awarded_flower(state):
            task_count += 1
        if self.drop_pint_glass_in_canal(state):
            task_count += 1
        if self.set_table(state):
            task_count += 1
        
        return (
            self.has_npc(state, itemNames.NPC_BURLY_MAN)
            and self.has_npc(state, itemNames.NPC_PUB_LADY)
            and self.has_prop(state, itemNames.PROP_BUCKET)
            and self.has_prop(state, itemNames.PROP_TOMATOES)
            and self.has_prop(state, itemNames.PROP_NO_GOOSE_SIGN_PUB)
            and task_count >= 6
        )
    
    
    # ----- To Do (As Well) Task Rule Defs -----
    
    def lock_groundskeeper_out(self, state: CollectionState) -> bool:
        return (
            self.has_garden(state)
            and self.has_npc(state, itemNames.NPC_GROUNDSKEEPER)
        )
    
    def cabbage_picnic(self, state: CollectionState) -> bool:
        return (
            self.has_garden(state)
            and self.has_prop(state, itemNames.PROP_CABBAGES)
        )
    
    def trip_boy_in_puddle(self, state: CollectionState) -> bool:
        return (
            self.has_high_street(state)
            and self.has_npc(state, itemNames.NPC_BOY)
        )
    
    def make_scales_ding(self, state: CollectionState) -> bool:
        if not self.has_high_street(state):
            return False
        
        # Any of these provides enough items to complete the task alone
        if self.has_prop(state, itemNames.PROP_CARROTS):
            return True
        if self.has_prop(state, itemNames.PROP_TOMATOES):
            return True
        if self.has_prop(state, itemNames.PROP_ORANGES):
            return True
        if self.has_prop(state, itemNames.PROP_LEEKS):
            return True
        if self.has_prop(state, itemNames.PROP_CUCUMBERS):
            return True
        if self.has_prop(state, itemNames.PROP_TINNED_FOOD):
            return True
        if self.has_pub(state) and self.has_prop(state, itemNames.PROP_GREEN_QUOITS):
            return True
        if self.has_pub(state) and self.has_prop(state, itemNames.PROP_RED_QUOITS):
            return True
        if self.has_pub(state) and self.has_prop(state, itemNames.PROP_PLATES):
            return True
        if self.has_pub(state) and self.has_prop(state, itemNames.PROP_DARTBOARD):
            return True
        if self.has_pub(state) and self.has_model_village(state) and self.has_prop(state, itemNames.PROP_MINI_PEOPLE):
            return True
        if self.has_prop(state, itemNames.PROP_PINT_BOTTLES):
            return True # Two in High Street, one in the hub near the dummy
            
        item_count = 0
        
        # High Street items (1 each)
        if self.has_prop(state, itemNames.PROP_TOOTHRBRUSH):
            item_count += 1
        if self.has_prop(state, itemNames.PROP_HAIRBRUSH):
            item_count += 1
        if self.has_prop(state, itemNames.PROP_LOO_PAPER):
            item_count += 1
        if self.has_prop(state, itemNames.PROP_DISH_SOAP_BOTTLE):
            item_count += 1
        if self.has_prop(state, itemNames.PROP_SPRAY_BOTTLE):
            item_count += 1
        if self.has_prop(state, itemNames.PROP_TOY_CAR):
            item_count += 1
        if self.has_prop(state, itemNames.PROP_HORN_RIMMED_GLASSES):
            item_count += 1
        if self.has_prop(state, itemNames.PROP_RED_GLASSES):
            item_count += 1
        if self.has_prop(state, itemNames.PROP_SUNGLASSES):
            item_count += 1
        if self.has_npc(state, itemNames.NPC_BOY):
            item_count += 1
        if self.has_prop(state, itemNames.PROP_TOY_PLANE):
            item_count += 1
        if self.has_prop(state, itemNames.PROP_LILY_FLOWER):
            item_count += 1
        if self.has_prop(state, itemNames.PROP_STEREOSCOPE):
            item_count += 1
        if self.has_prop(state, itemNames.PROP_DUSTBIN_LID):
            item_count += 1
        
        # High Street items (2 each)
        if self.has_prop(state, itemNames.PROP_APPLE_CORES):
            item_count += 2
        if self.has_prop(state, itemNames.PROP_WALKIE_TALKIES):
            item_count += 2
        if self.has_prop(state, itemNames.PROP_WEED_TOOLS):
            item_count += 2
        
        # Hub items (1 each)
        if self.has_prop(state, itemNames.PROP_TENNIS_BALL):
            item_count += 1
        if self.has_prop(state, itemNames.PROP_DUMMY):
            item_count += 1
        if self.has_prop(state, itemNames.PROP_FISHING_BOBBER):
            item_count += 1
        if self.has_prop(state, itemNames.PROP_DRINK_CAN):
            item_count += 1
        if self.has_prop(state, itemNames.PROP_RIBBONS):
            item_count += 1
        
        # Hub items (2 each)
        if self.has_prop(state, itemNames.PROP_BOOTS):
            item_count += 2
        
        if self.has_garden(state):
            # Garden items (1 each)
            if self.has_prop(state, itemNames.PROP_JAM):
                item_count += 1
            if self.has_prop(state, itemNames.PROP_TULIP):
                item_count += 1
            if self.has_prop(state, itemNames.PROP_PICNIC_MUG):
                item_count += 1
            if self.has_prop(state, itemNames.PROP_THERMOS):
                item_count += 1
            if self.has_prop(state, itemNames.PROP_TROWEL):
                item_count += 1
            if self.has_prop(state, itemNames.PROP_RADIO):
                item_count += 1
                
            # Garden items (2 each)
            if self.has_prop(state, itemNames.PROP_APPLES):
                item_count += 2
            if self.has_prop(state, itemNames.PROP_SANDWICH):
                item_count += 2
        
        if self.has_back_gardens(state):
            # Back Garden front items (1 each)
            if self.has_prop(state, itemNames.PROP_TEA_CUP):
                item_count += 1
            if self.has_prop(state, itemNames.PROP_CRICKET_BALL):
                item_count += 1
            if self.has_prop(state, itemNames.PROP_BUST_PIPE):
                item_count += 1
            if self.has_prop(state, itemNames.PROP_BUST_HAT):
                item_count += 1
            if self.has_prop(state, itemNames.PROP_BUST_GLASSES):
                item_count += 1
            if self.has_prop(state, itemNames.PROP_NEWSPAPER):
                item_count += 1
                
            # Back Garden back items (mostly 1 each)
            if self.has_prop(state, itemNames.PROP_DRAWER):
                if self.has_prop(state, itemNames.PROP_SOAP):
                    item_count += 1
                if self.has_prop(state, itemNames.PROP_POT_STACK):
                    item_count += 1
                if self.has_prop(state, itemNames.PROP_PAINTBRUSH):
                    item_count += 1
                if self.has_prop(state, itemNames.PROP_BRA):
                    item_count += 1
                    
                if self.has_prop(state, itemNames.PROP_SOCKS):
                    item_count += 2
        
        if self.has_pub(state):
            # Pub items (1 each)
            if self.has_prop(state, itemNames.PROP_CORK):
                item_count += 1
            if self.has_prop(state, itemNames.PROP_LETTER):
                item_count += 1
            if self.has_prop(state, itemNames.PROP_CANDLESTICK):
                item_count += 1
            if self.has_prop(state, itemNames.PROP_HARMONICA):
                item_count += 1
            if self.has_prop(state, itemNames.PROP_TOY_BOAT):
                item_count += 1
            if self.has_prop(state, itemNames.PROP_PEPPER_GRINDER):
                item_count += 1
                
            # Pub items (2 each)
            if self.has_prop(state, itemNames.PROP_KNIVES):
                item_count += 2
            if self.has_prop(state, itemNames.PROP_FORKS):
                item_count += 2
                
            if self.has_model_village(state):
                if self.has_prop(state, itemNames.PROP_MINI_GOOSE):
                    item_count += 1
                if self.has_prop(state, itemNames.PROP_MINI_MAIL_PILLAR):
                    item_count += 1
                if self.has_prop(state, itemNames.PROP_MINI_PHONE_DOOR):
                    item_count += 1
                if self.has_prop(state, itemNames.PROP_MINI_SHOVEL):
                    item_count += 1
                if self.has_prop(state, itemNames.PROP_POPPY_FLOWER):
                    item_count += 1
                if self.has_prop(state, itemNames.PROP_TIMBER_HANDLE):
                    item_count += 1
        
        return item_count >= 3
    
    def open_umbrella_on_tv(self, state: CollectionState) -> bool:
        return (
            self.has_pub(state)
            and self.has_npc(state, itemNames.NPC_TV_SHOP_OWNER)
            and self.has_npc(state, itemNames.NPC_MARKET_LADY)
            and self.has_prop(state, itemNames.PROP_UMBRELLAS)
            and (
                self.has_npc(state, itemNames.NPC_BOY)
                or self.has_prop(state, itemNames.PROP_WALKIE_TALKIES)
            )
        )
    
    def make_groundskeeper_buyback(self, state: CollectionState) -> bool:
        return (
            self.has_garden(state)
            and self.has_high_street(state)
            and self.has_npc(state, itemNames.NPC_GROUNDSKEEPER)
            and self.has_npc(state, itemNames.NPC_MARKET_LADY)
            and self.has_prop(state, itemNames.PROP_TROWEL)
        )
    
    def collect_five_flowers(self, state: CollectionState) -> bool:
        return (
            self.has_garden(state)
            and self.has_high_street(state)
            and self.has_pub(state)
            and self.has_model_village(state)
            and self.has_npc(state, itemNames.NPC_FANCY_LADIES)
            and self.has_prop(state, itemNames.PROP_TULIP)
            and self.has_prop(state, itemNames.PROP_LILY_FLOWER)
            and self.has_prop(state, itemNames.PROP_FLOWER_FOR_VASE)
            and self.has_prop(state, itemNames.PROP_POPPY_FLOWER)
            and self.make_someone_prune_rose(state)
        )
    
    def trap_boy_in_garage(self, state: CollectionState) -> bool:
        return self.trap_shopkeep_in_garage(state)
    
    def catch_thrown_object(self, state: CollectionState) -> bool:
        return ( # Tracking any prop souls here is unnecessary as it can be done with the Fence Bolt from the starting area
            self.has_back_gardens(state)
            and self.has_npc(state, itemNames.NPC_TIDY_NEIGHBOUR)
            and self.has_prop(state, itemNames.PROP_DRAWER)
        )
    
    def get_thrown_over_fence(self, state: CollectionState) -> bool:
        return (
            self.has_back_gardens(state)
            and self.has_pub(state)
            and self.has_npc(state, itemNames.NPC_TIDY_NEIGHBOUR)
            and self.has_prop(state, itemNames.PROP_DRAWER)
            and self.has_prop(state, itemNames.PROP_STEALTH_BOX)
        )
    
    def dress_up_bust_outside_items(self, state: CollectionState) -> bool:
        return (
            self.has_back_gardens(state)
            and self.has_npc(state, itemNames.NPC_MESSY_NEIGHBOUR)
            and self.has_prop(state, itemNames.PROP_DRAWER)
            and (
                self.has_garden(state) and self.has_npc(state, itemNames.NPC_GROUNDSKEEPER)
                or self.has_pub(state) and (
                    self.has_prop(state, itemNames.PROP_TRAFFIC_CONE)
                    or self.has_npc(state, itemNames.NPC_OLD_MAN)
                )
            )
            and self.has_high_street(state) and (
                self.has_prop(state, itemNames.PROP_HORN_RIMMED_GLASSES)
                or self.has_prop(state, itemNames.PROP_RED_GLASSES)
                or self.has_prop(state, itemNames.PROP_SUNGLASSES)
                or self.has_prop(state, itemNames.PROP_STEREOSCOPE)
                or self.has_npc(state, itemNames.NPC_BOY)
            )
            and (
                self.has_prop(state, itemNames.PROP_DUMMY)
                or self.has_garden(state) and self.has_prop(state, itemNames.PROP_TULIP)
                or self.has_high_street(state) and (
                    self.has_prop(state, itemNames.PROP_TOOTHRBRUSH)
                    or self.has_prop(state, itemNames.PROP_LILY_FLOWER)
                )
                or self.has_pub(state) and (
                    self.has_prop(state, itemNames.PROP_KNIVES)
                    or self.has_prop(state, itemNames.PROP_FORKS)
                    or self.has_prop(state, itemNames.PROP_HARMONICA)
                    or self.has_npc(state, itemNames.NPC_FANCY_LADIES) and self.has_prop(state, itemNames.PROP_FLOWER_FOR_VASE)
                )
                or self.has_model_village(state) and self.has_prop(state, itemNames.PROP_POPPY_FLOWER)
            )
        )
    
    def score_goal(self, state: CollectionState) -> bool:
        return (
            self.has_high_street(state)
            and self.make_someone_prune_rose(state)
            and self.has_prop(state, itemNames.PROP_FOOTBALL)
            and self.has_prop(state, itemNames.PROP_NO_GOOSE_SIGN_MESSY)
        )
    
    def sail_boat_under_bridge(self, state: CollectionState) -> bool:
        return (
            self.has_pub(state)
            and self.has_prop(state, itemNames.PROP_TOY_BOAT)
        )
    
    def perform_with_ribbon(self, state: CollectionState) -> bool:
        return (
            self.has_pub(state)
            and self.has_back_gardens(state)
            and self.has_npc(state, itemNames.NPC_FANCY_LADIES)
            and self.has_npc(state, itemNames.NPC_MESSY_NEIGHBOUR)
            and self.has_prop(state, itemNames.PROP_DUCK_STATUE)
            and self.has_prop(state, itemNames.PROP_RIBBONS)
            and self.has_prop(state, itemNames.PROP_DRAWER)
        )
    
    def steal_woolen_hat(self, state: CollectionState) -> bool:
        return self.make_old_man_fall_on_bum(state)
    
    
    # ----- To Do (Quickly!!) Task Rule Defs -----
    
    def speedrun_garden(self, state: CollectionState) -> bool:
        return self.make_groundskeeper_hammer_thumb(state)
    
    def speedrun_high_street(self, state: CollectionState) -> bool:
        return self.trap_shopkeep_in_garage(state)
    
    def speedrun_back_gardens(self, state: CollectionState) -> bool:
        task_count = 0
        
        if self.make_someone_break_vase(state):
            task_count += 1
        if self.make_man_spit_out_tea(state):
            task_count += 1
        if self.get_dressed_up(state):
            task_count += 1
        if self.make_man_barefoot(state):
            task_count += 1
        if self.do_washing(state):
            task_count += 1
        if (
            self.has_npc(state, itemNames.NPC_MESSY_NEIGHBOUR)
            and self.has_prop(state, itemNames.PROP_BUST_HAT)
            and self.has_prop(state, itemNames.PROP_BUST_GLASSES)
            and self.has_prop(state, itemNames.PROP_BUST_PIPE)
        ):
            task_count += 1
        
        return (
            self.has_npc(state, itemNames.NPC_TIDY_NEIGHBOUR)
            and self.has_npc(state, itemNames.NPC_MESSY_NEIGHBOUR)
            and self.has_prop(state, itemNames.PROP_DRAWER)
            and self.has_prop(state, itemNames.PROP_ROSE)
            and self.has_prop(state, itemNames.PROP_ROSE_BOX)
            and self.has_prop(state, itemNames.PROP_CLIPPERS)
            and self.has_prop(state, itemNames.PROP_NO_GOOSE_SIGN_CLEAN)
            and task_count >= 5
        )
    
    def speedrun_pub(self, state: CollectionState) -> bool:
        return self.drop_bucket_on_burly_man(state)
    
    
    # ----- Milestone & Goal Defs -----
    
    def all_garden_tasks(self, state: CollectionState) -> bool:
        return (
            self.get_into_garden(state)
            and self.get_groundskeeper_wet(state)
            and self.steal_groundskeepers_keys(state)
            and self.make_groundskeeper_wear_sun_hat(state)
            and self.rake_in_lake(state)
            and self.picnic(state)
            and self.make_groundskeeper_hammer_thumb(state)
        )
    
    def all_high_street_tasks(self, state: CollectionState) -> bool:
        return (
            self.break_broom(state)
            and self.trap_boy_in_phone_booth(state)
            and self.make_boy_wear_wrong_glasses(state)
            and self.make_someone_buyback(state)
            and self.get_on_tv(state)
            and self.go_shopping(state)
            and self.trap_shopkeep_in_garage(state)
        )
    
    def all_back_gardens_tasks(self, state: CollectionState) -> bool:
        return (
            self.make_someone_break_vase(state)
            and self.make_man_spit_out_tea(state)
            and self.get_dressed_up(state)
            and self.make_man_barefoot(state)
            and self.do_washing(state)
            and self.dress_up_bust(state)
            and self.make_someone_prune_rose(state)
        )
    
    def all_pub_tasks(self, state: CollectionState) -> bool:
        return (
            self.get_into_pub(state)
            and self.break_dartboard(state)
            and self.get_toy_boat(state)
            and self.make_old_man_fall_on_bum(state)
            and self.be_awarded_flower(state)
            and self.drop_pint_glass_in_canal(state)
            and self.set_table(state)
            and self.drop_bucket_on_burly_man(state)
        )
    
    def all_main_task_lists(self, state: CollectionState) -> bool:
        return (
            self.all_garden_tasks(state)
            and self.all_high_street_tasks(state)
            and self.all_back_gardens_tasks(state)
            and self.all_pub_tasks(state)
        )
    
    def all_to_do_as_well_tasks(self, state: CollectionState) -> bool:
        return (
            self.lock_groundskeeper_out(state)
            and self.cabbage_picnic(state)
            and self.trip_boy_in_puddle(state)
            and self.make_scales_ding(state)
            and self.open_umbrella_on_tv(state)
            and self.make_groundskeeper_buyback(state)
            and self.collect_five_flowers(state)
            and self.trap_boy_in_garage(state)
            and self.catch_thrown_object(state)
            and self.get_thrown_over_fence(state)
            and self.dress_up_bust_outside_items(state)
            and self.score_goal(state)
            and self.sail_boat_under_bridge(state)
            and self.perform_with_ribbon(state)
            and self.steal_woolen_hat(state)
        )
    
    def all_speedrun_tasks(self, state: CollectionState) -> bool:
        return (
            self.speedrun_garden(state)
            and self.speedrun_high_street(state)
            and self.speedrun_back_gardens(state)
            and self.speedrun_pub(state)
        )
    
    def all_tasks_complete(self, state: CollectionState) -> bool:
        return (
            self.all_main_task_lists(state)
            and self.all_to_do_as_well_tasks(state)
            and self.all_speedrun_tasks(state)
        )
    
    def all_non_speedrun_tasks(self, state: CollectionState) -> bool:
        return (
            self.all_main_task_lists(state)
            and self.all_to_do_as_well_tasks(state)
        )
    
    def four_final_tasks(self, state: CollectionState) -> bool:
        return (
            self.make_groundskeeper_hammer_thumb(state)
            and self.trap_shopkeep_in_garage(state)
            and self.make_someone_prune_rose(state)
            and self.drop_bucket_on_burly_man(state)
        )
    
    
    # ----- Model Village Defs -----
    
    def get_into_model_village(self, state: CollectionState) -> bool:
        return self.has_model_village(state)
    
    def steal_bell(self, state: CollectionState) -> bool:
        if self.world.options.logically_require_npc_souls.value:
            return (
                self.has_garden(state)
                and self.has_high_street(state)
                and self.has_back_gardens(state)
                and self.has_pub(state)
                and self.has_model_village(state)
                and self.has_prop(state, itemNames.PROP_TIMBER_HANDLE)
                and state.has(itemNames.PROP_GOLDEN_BELL, self.player)
                and self.has_npc(state, itemNames.NPC_GROUNDSKEEPER)
                and self.has_npc(state, itemNames.NPC_BOY)
                and self.has_npc(state, itemNames.NPC_TV_SHOP_OWNER)
                and self.has_npc(state, itemNames.NPC_MARKET_LADY)
                and self.has_npc(state, itemNames.NPC_TIDY_NEIGHBOUR)
                and self.has_npc(state, itemNames.NPC_MESSY_NEIGHBOUR)
                and self.has_npc(state, itemNames.NPC_BURLY_MAN)
                and self.has_npc(state, itemNames.NPC_OLD_MAN)
                and self.has_npc(state, itemNames.NPC_PUB_LADY)
                and self.has_npc(state, itemNames.NPC_FANCY_LADIES)
                and self.has_npc(state, itemNames.NPC_COOK)
            )

        return (
            self.has_garden(state)
            and self.has_high_street(state)
            and self.has_back_gardens(state)
            and self.has_pub(state)
            and self.has_model_village(state)
            and self.has_prop(state, itemNames.PROP_TIMBER_HANDLE)
            and state.has(itemNames.PROP_GOLDEN_BELL, self.player)
        )
    
    
    # ----- Hub Item Pickup Defs -----
    
    def pickup_drink_can(self, state: CollectionState) -> bool:
        return self.has_prop(state, itemNames.PROP_DRINK_CAN)
    
    def pickup_tennis_ball(self, state: CollectionState) -> bool:
        return self.has_prop(state, itemNames.PROP_TENNIS_BALL)
    
    def pickup_blue_bow(self, state: CollectionState) -> bool:
        return self.has_prop(state, itemNames.PROP_RIBBONS)
    
    def pickup_dummy(self, state: CollectionState) -> bool:
        return self.has_prop(state, itemNames.PROP_DUMMY)
    
    def pickup_fishing_bobber(self, state: CollectionState) -> bool:
        return self.has_prop(state, itemNames.PROP_FISHING_BOBBER)
    
    def pickup_boots(self, state: CollectionState) -> bool:
        return self.has_prop(state, itemNames.PROP_BOOTS)
    
    
    # ----- Garden Item Pickup Defs -----
    
    def pickup_radio(self, state: CollectionState) -> bool:
        return (
            self.has_garden(state)
            and self.has_prop(state, itemNames.PROP_RADIO)
        )
    
    def pickup_trowel(self, state: CollectionState) -> bool:
        return (
            self.has_garden(state)
            and self.has_prop(state, itemNames.PROP_TROWEL)
        )
    
    def pickup_keys(self, state: CollectionState) -> bool:
        return (
            self.has_garden(state)
            and self.has_npc(state, itemNames.NPC_GROUNDSKEEPER)
        )
    
    def pickup_grounsdkeepers_hat(self, state: CollectionState) -> bool:
        return (
            self.has_garden(state)
            and self.has_npc(state, itemNames.NPC_GROUNDSKEEPER)
            and
            (
                self.has_prop(state, itemNames.PROP_TULIP)
                or self.rake_in_lake(state)
                and self.picnic(state)
                and self.has_prop(state, itemNames.PROP_MALLET)
            )
        )
    
    def pickup_tulip(self, state: CollectionState) -> bool:
        return (
            self.has_garden(state)
            and self.has_prop(state, itemNames.PROP_TULIP)
        )
    
    def pickup_apples(self, state: CollectionState) -> bool:
        return (
            self.has_garden(state)
            and self.has_prop(state, itemNames.PROP_APPLES)
        )
    
    def pickup_jam(self, state: CollectionState) -> bool:
        return (
            self.has_garden(state)
            and self.has_prop(state, itemNames.PROP_JAM)
        )
    
    def pickup_picnic_mug(self, state: CollectionState) -> bool:
        return (
            self.has_garden(state)
            and self.has_prop(state, itemNames.PROP_PICNIC_MUG)
        )
    
    def pickup_thermos(self, state: CollectionState) -> bool:
        return (
            self.has_garden(state)
            and self.has_prop(state, itemNames.PROP_THERMOS)
        )
    
    def pickup_sandwich(self, state: CollectionState) -> bool:
        return (
            self.has_garden(state)
            and self.has_prop(state, itemNames.PROP_SANDWICH)
        )
    
    def pickup_straw_hat(self, state: CollectionState) -> bool:
        return (
            self.pickup_grounsdkeepers_hat(state)
            and self.has_prop(state, itemNames.PROP_STRAW_HAT)
        )
    
    def pickup_garden_carrots(self, state: CollectionState) -> bool:
        return (
            self.has_garden(state)
            and self.has_prop(state, itemNames.PROP_CARROTS)
        )
    
    
    # ----- High Street Item Pickup Defs -----
    
    def pickup_boys_glasses(self, state: CollectionState) -> bool:
        return (
            self.has_high_street(state)
            and self.has_npc(state, itemNames.NPC_BOY)
        )
    
    def pickup_horn_rimmed_glasses(self, state: CollectionState) -> bool:
        return (
            self.has_high_street(state)
            and self.has_prop(state, itemNames.PROP_HORN_RIMMED_GLASSES)
        )
    
    def pickup_red_glasses(self, state: CollectionState) -> bool:
        return (
            self.has_high_street(state)
            and self.has_prop(state, itemNames.PROP_RED_GLASSES)
        )
    
    def pickup_sunglasses(self, state: CollectionState) -> bool:
        return (
            self.has_high_street(state)
            and self.has_prop(state, itemNames.PROP_SUNGLASSES)
        )
    
    def pickup_loo_paper(self, state: CollectionState) -> bool:
        return (
            self.has_high_street(state)
            and self.has_prop(state, itemNames.PROP_LOO_PAPER)
        )
    
    def pickup_toy_car(self, state: CollectionState) -> bool:
        return (
            self.has_high_street(state)
            and self.has_prop(state, itemNames.PROP_TOY_CAR)
        )
    
    def pickup_hairbrush(self, state: CollectionState) -> bool:
        return (
            self.has_high_street(state)
            and self.has_prop(state, itemNames.PROP_HAIRBRUSH)
        )
    
    def pickup_toothbrush(self, state: CollectionState) -> bool:
        return (
            self.has_high_street(state)
            and self.has_prop(state, itemNames.PROP_TOOTHRBRUSH)
        )
    
    def pickup_stereoscope(self, state: CollectionState) -> bool:
        return (
            self.has_high_street(state)
            and self.has_prop(state, itemNames.PROP_STEREOSCOPE)
        )
    
    def pickup_dish_soap_bottle(self, state: CollectionState) -> bool:
        return (
            self.has_high_street(state)
            and self.has_prop(state, itemNames.PROP_DISH_SOAP_BOTTLE)
        )
    
    def pickup_food_cans(self, state: CollectionState) -> bool:
        return (
            self.has_high_street(state)
            and self.has_prop(state, itemNames.PROP_TINNED_FOOD)
        )
    
    def pickup_weed_tools(self, state: CollectionState) -> bool:
        return (
            self.has_high_street(state)
            and self.has_prop(state, itemNames.PROP_WEED_TOOLS)
        )
    
    def pickup_lily_flower(self, state: CollectionState) -> bool:
        return (
            self.has_high_street(state)
            and self.has_prop(state, itemNames.PROP_LILY_FLOWER)
        )
    
    def pickup_oranges(self, state: CollectionState) -> bool:
        return (
            self.has_high_street(state)
            and self.has_prop(state, itemNames.PROP_ORANGES)
        )
    
    def pickup_tomatoes_high_street(self, state: CollectionState) -> bool:
        return (
            self.has_high_street(state)
            and self.has_prop(state, itemNames.PROP_TOMATOES)
        )
    
    def pickup_carrots_high_street(self, state: CollectionState) -> bool:
        return (
            self.has_high_street(state)
            and self.has_prop(state, itemNames.PROP_CARROTS)
        )
    
    def pickup_cucumbers(self, state: CollectionState) -> bool:
        return (
            self.has_high_street(state)
            and self.has_prop(state, itemNames.PROP_CUCUMBERS)
        )
    
    def pickup_leeks(self, state: CollectionState) -> bool:
        return (
            self.has_high_street(state)
            and self.has_prop(state, itemNames.PROP_LEEKS)
        )
    
    def pickup_fusilage(self, state: CollectionState) -> bool:
        return (
            self.has_high_street(state)
            and self.has_prop(state, itemNames.PROP_TOY_PLANE)
        )
    
    def pickup_pint_bottle_hub(self, state: CollectionState) -> bool:
        return self.has_prop(state, itemNames.PROP_PINT_BOTTLES)
    
    def pickup_pint_bottle_high_street(self, state: CollectionState) -> bool:
        return (
            self.has_high_street(state)
            and self.has_prop(state, itemNames.PROP_PINT_BOTTLES)
        )
    
    def pickup_spray_bottle(self, state: CollectionState) -> bool:
        return (
            self.has_high_street(state)
            and self.has_prop(state, itemNames.PROP_SPRAY_BOTTLE)
        )
    
    def pickup_walkie_talkies(self, state: CollectionState) -> bool:
        return (
            self.has_high_street(state)
            and self.has_prop(state, itemNames.PROP_WALKIE_TALKIES)
        )
    
    def pickup_apple_cores(self, state: CollectionState) -> bool:
        return (
            self.has_high_street(state)
            and self.has_prop(state, itemNames.PROP_APPLE_CORES)
        )
    
    def pickup_dustbin_lid(self, state: CollectionState) -> bool:
        return (
            self.has_high_street(state)
            and self.has_prop(state, itemNames.PROP_DUSTBIN_LID)
        )
    
    def pickup_chalk(self, state: CollectionState) -> bool:
        return self.trap_shopkeep_in_garage(state)
    
    
    # ----- Back Gardens Item Pickup Defs -----
    
    def pickup_red_bow(self, state: CollectionState) -> bool:
        return self.get_dressed_up(state)
    
    def pickup_cricket_ball(self, state: CollectionState) -> bool:
        return (
            self.has_back_gardens(state)
            and self.has_prop(state, itemNames.PROP_CRICKET_BALL)
        )
    
    def pickup_bust_pipe(self, state: CollectionState) -> bool:
        return (
            self.has_back_gardens(state)
            and self.has_prop(state, itemNames.PROP_BUST_PIPE)
        )
    
    def pickup_bust_hat(self, state: CollectionState) -> bool:
        return (
            self.has_back_gardens(state)
            and self.has_prop(state, itemNames.PROP_BUST_HAT)
        )
    
    def pickup_bust_glasses(self, state: CollectionState) -> bool:
        return (
            self.has_back_gardens(state)
            and self.has_prop(state, itemNames.PROP_BUST_GLASSES)
        )
    
    def pickup_slippers(self, state: CollectionState) -> bool:
        return (
            self.has_back_gardens(state)
            and self.has_npc(state, itemNames.NPC_TIDY_NEIGHBOUR)
        )
    
    def pickup_tea_cup(self, state: CollectionState) -> bool:
        return (
            self.has_back_gardens(state)
            and self.has_prop(state, itemNames.PROP_TEA_CUP)
        )
    
    def pickup_newspaper(self, state: CollectionState) -> bool:
        return (
            self.has_back_gardens(state)
            and self.has_prop(state, itemNames.PROP_NEWSPAPER)
        )
    
    def pickup_socks(self, state: CollectionState) -> bool:
        return (
            self.has_back_gardens(state)
            and self.has_prop(state, itemNames.PROP_SOCKS)
            and self.has_prop(state, itemNames.PROP_DRAWER)
        )
    
    def pickup_vase(self, state: CollectionState) -> bool:
        return (
            self.has_back_gardens(state)
            and self.has_prop(state, itemNames.PROP_VASE)
            and self.has_prop(state, itemNames.PROP_DRAWER)
        )
    
    def pickup_pot_stack(self, state: CollectionState) -> bool:
        return (
            self.has_back_gardens(state)
            and self.has_prop(state, itemNames.PROP_POT_STACK)
            and self.has_prop(state, itemNames.PROP_DRAWER)
        )
    
    def pickup_soap(self, state: CollectionState) -> bool:
        return (
            self.has_back_gardens(state)
            and self.has_prop(state, itemNames.PROP_SOAP)
            and self.has_prop(state, itemNames.PROP_DRAWER)
        )
    
    def pickup_paintbrush(self, state: CollectionState) -> bool:
        return (
            self.has_back_gardens(state)
            and self.has_prop(state, itemNames.PROP_PAINTBRUSH)
            and self.has_prop(state, itemNames.PROP_DRAWER)
        )
    
    def pickup_vase_pieces(self, state: CollectionState) -> bool:
        return (
            self.has_back_gardens(state)
            and self.has_npc(state, itemNames.NPC_TIDY_NEIGHBOUR)
            and self.has_prop(state, itemNames.PROP_VASE)
            and self.has_prop(state, itemNames.PROP_DRAWER)
        )
    
    def pickup_bra(self, state: CollectionState) -> bool:
        return (
            self.has_back_gardens(state)
            and self.has_prop(state, itemNames.PROP_BRA)
            and self.has_prop(state, itemNames.PROP_DRAWER)
        )
    
    def pickup_badminton_racket(self, state: CollectionState) -> bool:
        return (
            self.has_prop(state, itemNames.PROP_BADMINTON_RACKET)
            and self.has_prop(state, itemNames.PROP_NO_GOOSE_SIGN_MESSY)
            and self.make_someone_prune_rose(state)
        )
    
    def pickup_rose(self, state: CollectionState) -> bool:
        return self.make_someone_prune_rose(state)
    
    
    # ----- Pub Item Pickup Defs -----
    
    def pickup_exit_letter(self, state: CollectionState) -> bool:
        return (
            self.has_pub(state)
            and self.has_prop(state, itemNames.PROP_LETTER)
        )
    
    def pickup_plates(self, state: CollectionState) -> bool:
        return (
            self.has_pub(state)
            and self.has_prop(state, itemNames.PROP_PLATES)
        )
    
    def pickup_green_quoits(self, state: CollectionState) -> bool:
        return (
            self.has_pub(state)
            and self.has_prop(state, itemNames.PROP_GREEN_QUOITS)
        )
    
    def pickup_red_quoits(self, state: CollectionState) -> bool:
        return (
            self.has_pub(state)
            and self.has_prop(state, itemNames.PROP_RED_QUOITS)
        )
    
    def pickup_forks(self, state: CollectionState) -> bool:
        return (
            self.has_pub(state)
            and self.has_prop(state, itemNames.PROP_FORKS)
        )
    
    def pickup_knives(self, state: CollectionState) -> bool:
        return (
            self.has_pub(state)
            and self.has_prop(state, itemNames.PROP_KNIVES)
        )
    
    def pickup_cork(self, state: CollectionState) -> bool:
        return (
            self.has_pub(state)
            and self.has_prop(state, itemNames.PROP_CORK)
        )
    
    def pickup_candlestick(self, state: CollectionState) -> bool:
        return (
            self.has_pub(state)
            and self.has_prop(state, itemNames.PROP_CANDLESTICK)
        )
    
    def pickup_vase_flower(self, state: CollectionState) -> bool:
        return (
            self.has_pub(state)
            and self.has_npc(state, itemNames.NPC_FANCY_LADIES)
            and self.has_prop(state, itemNames.PROP_FLOWER_FOR_VASE)
        )
    
    def pickup_darts(self, state: CollectionState) -> bool:
        return (
            self.has_pub(state)
            and self.has_npc(state, itemNames.NPC_OLD_MAN)
            and self.has_prop(state, itemNames.PROP_DARTBOARD)
        )
    
    def pickup_harmonica(self, state: CollectionState) -> bool:
        return (
            self.has_pub(state)
            and self.has_prop(state, itemNames.PROP_HARMONICA)
        )
    
    def pickup_pint_glass(self, state: CollectionState) -> bool:
        return (
            self.has_pub(state)
            and self.has_prop(state, itemNames.PROP_PINT_GLASSES)
        )
    
    def pickup_toy_boat(self, state: CollectionState) -> bool:
        return (
            self.has_pub(state)
            and self.has_prop(state, itemNames.PROP_TOY_BOAT)
        )
    
    def pickup_woolen_hat(self, state: CollectionState) -> bool:
        return self.make_old_man_fall_on_bum(state)
    
    def pickup_pepper_grinder(self, state: CollectionState) -> bool:
        return (
            self.has_pub(state)
            and self.has_prop(state, itemNames.PROP_PEPPER_GRINDER)
        )
    
    def pickup_pub_woman_cloth(self, state: CollectionState) -> bool:
        return (
            self.has_pub(state)
            and self.has_npc(state, itemNames.NPC_PUB_LADY)
        )
    
    def pickup_pub_open_tomatoes(self, state: CollectionState) -> bool:
        return (
            self.has_pub(state)
            and self.has_prop(state, itemNames.PROP_TOMATOES)
        )
    
    def pickup_pub_boxed_tomatoes(self, state: CollectionState) -> bool:
        task_count = 0
        
        if self.get_into_pub(state):
            task_count += 1
        if self.break_dartboard(state):
            task_count += 1
        if self.get_toy_boat(state):
            task_count += 1
        if self.make_old_man_fall_on_bum(state):
            task_count += 1
        if self.be_awarded_flower(state):
            task_count += 1
        if self.drop_pint_glass_in_canal(state):
            task_count += 1
        if self.set_table(state):
            task_count += 1
        
        return (
            self.has_npc(state, itemNames.NPC_PUB_LADY)
            and self.has_prop(state, itemNames.PROP_NO_GOOSE_SIGN_PUB)
            and self.has_prop(state, itemNames.PROP_TOMATOES)
            and task_count >= 6
        )
    
    
    # ----- Model Village Item Pickup Defs -----
    
    def pickup_people_miniatures(self, state: CollectionState) -> bool:
        return (
            self.has_model_village(state)
            and self.has_prop(state, itemNames.PROP_MINI_PEOPLE)
        )
    
    def pickup_mini_shovel(self, state: CollectionState) -> bool:
        return (
            self.has_model_village(state)
            and self.has_prop(state, itemNames.PROP_MINI_SHOVEL)
        )
    
    def pickup_mini_goose(self, state: CollectionState) -> bool:
        return (
            self.has_model_village(state)
            and self.has_prop(state, itemNames.PROP_MINI_GOOSE)
        )
    
    def pickup_poppy(self, state: CollectionState) -> bool:
        return (
            self.has_model_village(state)
            and self.has_prop(state, itemNames.PROP_POPPY_FLOWER)
        )
    
    def pickup_mini_phone_booth(self, state: CollectionState) -> bool:
        return (
            self.has_model_village(state)
            and self.has_prop(state, itemNames.PROP_MINI_PHONE_DOOR)
        )
    
    def pickup_mini_mail_pillar(self, state: CollectionState) -> bool:
        return (
            self.has_model_village(state)
            and self.has_prop(state, itemNames.PROP_MINI_MAIL_PILLAR)
        )
    
    def pickup_timber_handle(self, state: CollectionState) -> bool:
        return (
            self.has_model_village(state)
            and self.has_prop(state, itemNames.PROP_TIMBER_HANDLE)
        )
    
    def pickup_golden_bell(self, state: CollectionState) -> bool:
        return self.steal_bell(state)
    
    
    # ----- Hub Item Drag Defs -----
    
    def drag_fence_bolt(self, state: CollectionState) -> bool:
        return True
    
    def drag_tackle_box(self, state: CollectionState) -> bool:
        return self.has_prop(state, itemNames.PROP_TACKLE_BOX)
    
    
    # ----- Garden Item Drag Defs -----
    
    def drag_rake(self, state: CollectionState) -> bool:
        return (
            self.has_garden(state)
            and self.has_prop(state, itemNames.PROP_RAKE)
        )
    
    def drag_picnic_basket(self, state: CollectionState) -> bool:
        return (
            self.has_garden(state)
            and self.has_prop(state, itemNames.PROP_PICNIC_BASKET)
        )
    
    def drag_esky(self, state: CollectionState) -> bool:
        return (
            self.has_garden(state)
            and self.has_prop(state, itemNames.PROP_ESKY)
        )
    
    def drag_shovel(self, state: CollectionState) -> bool:
        return (
            self.has_garden(state)
            and self.has_prop(state, itemNames.PROP_SHOVEL)
        )
    
    def drag_pumpkins(self, state: CollectionState) -> bool:
        return (
            self.has_garden(state)
            and self.has_prop(state, itemNames.PROP_PUMPKINS)
        )
    
    def drag_watering_can(self, state: CollectionState) -> bool:
        return (
            self.has_garden(state)
            and self.has_prop(state, itemNames.PROP_WATERING_CAN)
        )
    
    def drag_gumboots(self, state: CollectionState) -> bool:
        return (
            self.has_garden(state)
            and self.has_prop(state, itemNames.PROP_GUMBOOTS)
        )
    
    def drag_gardener_sign(self, state: CollectionState) -> bool:
        task_count = 0
        
        if self.get_into_garden(state):
            task_count += 1
        if self.get_groundskeeper_wet(state):
            task_count += 1
        if self.steal_groundskeepers_keys(state):
            task_count += 1
        if self.make_groundskeeper_wear_sun_hat(state):
            task_count += 1
        if self.rake_in_lake(state):
            task_count += 1
        if self.picnic(state):
            task_count += 1
        
        return (
            self.has_npc(state, itemNames.NPC_GROUNDSKEEPER)
            and task_count >= 5
        )
    
    def drag_wooden_crate(self, state: CollectionState) -> bool:
        return (
            self.has_garden(state)
            and self.has_prop(state, itemNames.PROP_WOODEN_CRATE)
        )
    
    def drag_mallet(self, state: CollectionState) -> bool:
        return self.make_groundskeeper_hammer_thumb(state)
    
    def drag_topsoil_bags(self, state: CollectionState) -> bool:
        return (
            self.has_garden(state)
            and self.has_prop(state, itemNames.PROP_TOPSOIL_BAGS)
        )
    
    
    # ----- High Street Item Drag Defs -----
    
    def drag_shopping_basket(self, state: CollectionState) -> bool:
        return (
            self.has_high_street(state)
            and self.has_prop(state, itemNames.PROP_SHOPPING_BASKET)
        )
    
    def drag_umbrellas(self, state: CollectionState) -> bool:
        return (
            self.has_high_street(state)
            and self.has_npc(state, itemNames.NPC_MARKET_LADY)
            and self.has_prop(state, itemNames.PROP_UMBRELLAS)
        )
    
    def drag_push_broom(self, state: CollectionState) -> bool:
        return (
            self.has_high_street(state)
            and self.has_prop(state, itemNames.PROP_PUSH_BROOM)
        )
    
    def drag_broom_head(self, state: CollectionState) -> bool:
        return self.break_broom(state)
    
    def drag_dustbin(self, state: CollectionState) -> bool:
        return (
            self.has_high_street(state)
            and self.has_prop(state, itemNames.PROP_DUSTBIN)
        )
    
    def drag_baby_doll(self, state: CollectionState) -> bool:
        return (
            self.has_high_street(state)
            and self.has_prop(state, itemNames.PROP_BABY_DOLL)
        )
    
    def drag_pricing_gun(self, state: CollectionState) -> bool:
        return (
            self.has_high_street(state)
            and self.has_prop(state, itemNames.PROP_PRICING_GUN)
        )
    
    def drag_adding_machine(self, state: CollectionState) -> bool:
        return (
            self.has_high_street(state)
            and self.has_prop(state, itemNames.PROP_ADDING_MACHINE)
        )
    
    
    # ----- Back Gardens Item Drag Defs -----
    
    def drag_rose_box(self, state: CollectionState) -> bool:
        task_count = 0
        
        if self.make_someone_break_vase(state):
            task_count += 1
        if self.make_man_spit_out_tea(state):
            task_count += 1
        if self.get_dressed_up(state):
            task_count += 1
        if self.make_man_barefoot(state):
            task_count += 1
        if self.do_washing(state):
            task_count += 1
        if self.dress_up_bust(state):
            task_count += 1
        
        return (
            self.has_npc(state, itemNames.NPC_TIDY_NEIGHBOUR)
            and self.has_prop(state, itemNames.PROP_ROSE_BOX)
            and self.has_prop(state, itemNames.PROP_NO_GOOSE_SIGN_CLEAN)
            and task_count >= 5
        )
    
    def drag_cricket_bat(self, state: CollectionState) -> bool:
        return (
            self.has_back_gardens(state)
            and self.has_prop(state, itemNames.PROP_CRICKET_BAT)
        )
    
    def drag_tea_pot(self, state: CollectionState) -> bool:
        return (
            self.has_back_gardens(state)
            and self.has_prop(state, itemNames.PROP_TEA_POT)
        )
    
    def drag_clippers(self, state: CollectionState) -> bool:
        return (
            self.has_back_gardens(state)
            and self.has_prop(state, itemNames.PROP_CLIPPERS)
        )
    
    def drag_duck_statue(self, state: CollectionState) -> bool:
        return (
            self.has_back_gardens(state)
            and self.has_prop(state, itemNames.PROP_DUCK_STATUE)
            and self.has_prop(state, itemNames.PROP_DRAWER)
        )
    
    def drag_frog_statue(self, state: CollectionState) -> bool:
        return (
            self.has_back_gardens(state)
            and self.has_prop(state, itemNames.PROP_FROG_STATUE)
            and self.has_prop(state, itemNames.PROP_DRAWER)
        )
    
    def drag_jeremy_fish(self, state: CollectionState) -> bool:
        return (
            self.has_back_gardens(state)
            and self.has_prop(state, itemNames.PROP_JEREMY_FISH)
            and self.has_prop(state, itemNames.PROP_DRAWER)
        )
    
    def drag_messy_sign(self, state: CollectionState) -> bool:
        return (
            self.has_prop(state, itemNames.PROP_NO_GOOSE_SIGN_MESSY)
            and self.make_someone_prune_rose(state)
        )
    
    def drag_drawer(self, state: CollectionState) -> bool:
        return (
            self.has_back_gardens(state)
            and self.has_prop(state, itemNames.PROP_DRAWER)
        )
    
    def drag_enamel_jug(self, state: CollectionState) -> bool:
        return (
            self.has_back_gardens(state)
            and self.has_prop(state, itemNames.PROP_ENAMEL_JUG)
            and self.has_prop(state, itemNames.PROP_DRAWER)
        )
    
    def drag_clean_sign(self, state: CollectionState) -> bool:
        task_count = 0
        
        if self.make_someone_break_vase(state):
            task_count += 1
        if self.make_man_spit_out_tea(state):
            task_count += 1
        if self.get_dressed_up(state):
            task_count += 1
        if self.make_man_barefoot(state):
            task_count += 1
        if self.do_washing(state):
            task_count += 1
        if self.dress_up_bust(state):
            task_count += 1
        
        return (
            self.has_npc(state, itemNames.NPC_TIDY_NEIGHBOUR)
            and self.has_prop(state, itemNames.PROP_NO_GOOSE_SIGN_CLEAN)
            and task_count >= 5
        )
    
    
    # ----- Pub Item Drag Defs -----
    
    def drag_traffic_cone(self, state: CollectionState) -> bool:
        return (
            self.has_pub(state)
            and self.has_prop(state, itemNames.PROP_TRAFFIC_CONE)
        )
    
    def drag_exit_parcel(self, state: CollectionState) -> bool:
        return (
            self.has_pub(state)
            and self.has_prop(state, itemNames.PROP_PARCEL)
        )
    
    def drag_stealth_box(self, state: CollectionState) -> bool:
        return (
            self.has_pub(state)
            and self.has_prop(state, itemNames.PROP_STEALTH_BOX)
        )
    
    def drag_no_goose_sign(self, state: CollectionState) -> bool:
        task_count = 0
        
        if self.get_into_pub(state):
            task_count += 1
        if self.break_dartboard(state):
            task_count += 1
        if self.get_toy_boat(state):
            task_count += 1
        if self.make_old_man_fall_on_bum(state):
            task_count += 1
        if self.be_awarded_flower(state):
            task_count += 1
        if self.drop_pint_glass_in_canal(state):
            task_count += 1
        if self.set_table(state):
            task_count += 1
        
        return (
            self.has_npc(state, itemNames.NPC_PUB_LADY)
            and self.has_prop(state, itemNames.PROP_NO_GOOSE_SIGN_PUB)
            and task_count >= 6
        )
    
    def drag_portable_stool(self, state: CollectionState) -> bool:
        return (
            self.has_pub(state)
            and self.has_prop(state, itemNames.PROP_PORTABLE_STOOL)
        )
    
    def drag_dartboard(self, state: CollectionState) -> bool:
        return self.break_dartboard(state)
    
    def drag_mop_bucket(self, state: CollectionState) -> bool:
        return (
            self.has_pub(state)
            and self.has_prop(state, itemNames.PROP_MOP_BUCKET)
        )
    
    def drag_mop(self, state: CollectionState) -> bool:
        return (
            self.has_pub(state)
            and self.has_prop(state, itemNames.PROP_MOP)
        )
    
    def drag_delivery_box(self, state: CollectionState) -> bool:
        return (
            self.has_pub(state)
            and self.has_npc(state, itemNames.NPC_COOK)
        )
    
    def drag_burly_mans_bucket(self, state: CollectionState) -> bool:
        return (
            self.has_pub(state)
            and self.has_prop(state, itemNames.PROP_BUCKET)
        )
    
    
    # ----- Model Village Item Drag Defs -----
    
    def drag_mini_benches(self, state: CollectionState) -> bool:
        return (
            self.has_model_village(state)
            and self.has_prop(state, itemNames.PROP_MINI_BENCHES)
        )
    
    def drag_mini_pump(self, state: CollectionState) -> bool:
        return (
            self.has_model_village(state)
            and self.has_prop(state, itemNames.PROP_MINI_PUMP)
        )
    
    def drag_mini_birdbath(self, state: CollectionState) -> bool:
        return (
            self.has_model_village(state)
            and self.has_prop(state, itemNames.PROP_MINI_BIRDBATH)
        )
    
    def drag_mini_easel(self, state: CollectionState) -> bool:
        return (
            self.has_model_village(state)
            and self.has_prop(state, itemNames.PROP_MINI_EASEL)
        )
    
    def drag_sun_lounge(self, state: CollectionState) -> bool:
        return (
            self.has_model_village(state)
            and self.has_prop(state, itemNames.PROP_MINI_SUN_LOUNGE)
        )
    
    
    # ----- Interaction & Church Pecking Defs -----
    
    def interact_bike_bell(self, state: CollectionState) -> bool:
        return True
    
    def interact_garden_water(self, state: CollectionState) -> bool:
        return self.has_garden(state)
    
    def short_out_radio(self, state: CollectionState) -> bool:
        return (
            self.has_garden(state)
            and self.has_prop(state, itemNames.PROP_RADIO)
        )
    
    def interact_intro_gate(self, state: CollectionState) -> bool:
        return True
    
    def interact_well(self, state: CollectionState) -> bool:
        return True
    
    def drop_mail_in_well(self, state: CollectionState) -> bool:
        return (
            self.has_pub(state)
            and (
                self.has_prop(state, itemNames.PROP_LETTER)
                or self.has_model_village(state)
                and self.has_prop(state, itemNames.PROP_MINI_MAIL_PILLAR)
            )
        )
    
    def interact_boards(self, state: CollectionState) -> bool:
        return self.has_back_gardens(state)
    
    def interact_radio(self, state: CollectionState) -> bool:
        return self.has_high_street(state)
    
    def interact_football(self, state: CollectionState) -> bool:
        return (
            self.has_high_street(state)
            and self.has_prop(state, itemNames.PROP_FOOTBALL)
        )
    
    def interact_umbrellas(self, state: CollectionState) -> bool:
        return (
            self.has_high_street(state)
            and self.has_npc(state, itemNames.NPC_MARKET_LADY)
            and self.has_prop(state, itemNames.PROP_UMBRELLAS)
        )
    
    def interact_boys_laces(self, state: CollectionState) -> bool:
        return (
            self.has_high_street(state)
            and self.has_npc(state, itemNames.NPC_BOY)
        )
    
    def trap_tv_shop_owner_in_garage(self, state: CollectionState) -> bool:
        return (
            self.trap_shopkeep_in_garage(state)
            and self.has_npc(state, itemNames.NPC_TV_SHOP_OWNER)
            and self.has_prop(state, itemNames.PROP_WALKIE_TALKIES)
        )
    
    def interact_back_gardens_objects(self, state: CollectionState) -> bool:
        return (
            self.has_back_gardens(state)
            and self.has_prop(state, itemNames.PROP_DRAWER)
        )
    
    def interact_trellis(self, state: CollectionState) -> bool:
        return self.has_back_gardens(state)

    def interact_make_woman_fix_topiary(self, state: CollectionState) -> bool:
        return (
            self.has_back_gardens(state)
            and self.has_npc(state, itemNames.NPC_MESSY_NEIGHBOUR)
            and self.has_prop(state, itemNames.PROP_CLIPPERS)
            and self.has_prop(state, itemNames.PROP_DRAWER)
        )

    def pose_as_duck_statue(self, state: CollectionState) -> bool:
        return (
            self.has_back_gardens(state)
            and self.has_npc(state, itemNames.NPC_MESSY_NEIGHBOUR)
            and self.has_prop(state, itemNames.PROP_DUCK_STATUE)
            and self.has_prop(state, itemNames.PROP_DRAWER)
        )
    
    def dress_up_bush(self, state: CollectionState) -> bool:
        return (
            self.make_someone_prune_rose(state)
            and self.has_prop(state, itemNames.PROP_RIBBONS)
        )
    
    def interact_van_doors(self, state: CollectionState) -> bool:
        return self.has_pub(state)
    
    def interact_burly_laces(self, state: CollectionState) -> bool:
        return (
            self.has_pub(state)
            and self.has_npc(state, itemNames.NPC_BURLY_MAN)
        )
    
    def interact_pub_tap(self, state: CollectionState) -> bool:
        return self.has_pub(state)
    
    def perform_with_harmonica(self, state: CollectionState) -> bool:
        return (
            self.be_awarded_flower(state)
            and self.has_prop(state, itemNames.PROP_HARMONICA)
        )
    
    def peck_church(self, state: CollectionState) -> bool:
        return self.has_model_village(state)
    
    
    # --------------- Set Rules ---------------

    def set_rules(self) -> None:
        # Model Village Rules/Victory Rules
        for location, rules in self.victory_rules.items():
            new_rule = self.world.multiworld.get_location(location, self.player)
            set_rule(new_rule, rules)
        
        # Main Task Rules
        for location, rules in self.main_tasks_rules.items():
            new_rule = self.world.multiworld.get_location(location, self.player)
            set_rule(new_rule, rules)
        
        # To Do (As Well) Task Rules
        if self.world.options.include_extra_tasks.value:
            for location, rules in self.extra_task_rules.items():
                new_rule = self.world.multiworld.get_location(location, self.player)
                set_rule(new_rule, rules)

        # To Do (Quickly!!) Task Rules
        if self.world.options.include_speedrun_tasks.value:
            for location, rules in self.speedrun_task_rules.items():
                new_rule = self.world.multiworld.get_location(location, self.player)
                set_rule(new_rule, rules)

        # Item Pickup Rules
        if self.world.options.include_item_pickups.value:
            for location, rules in self.pickup_rules.items():
                new_rule = self.world.multiworld.get_location(location, self.player)
                set_rule(new_rule, rules)

        # Item Drag Rules
        if self.world.options.include_drag_items.value:
            for location, rules in self.drag_rules.items():
                new_rule = self.world.multiworld.get_location(location, self.player)
                set_rule(new_rule, rules)

        # Interaction Rules
        if self.world.options.include_interactions.value:
            for location, rules in self.interaction_rules.items():
                new_rule = self.world.multiworld.get_location(location, self.player)
                set_rule(new_rule, rules)

        # New Tasks Rules
        if self.world.options.include_new_tasks.value:
            for location, rules in self.new_tasks_rules.items():
                new_rule = self.world.multiworld.get_location(location, self.player)
                set_rule(new_rule, rules)

        # Model Church Pecking Rules
        if self.world.options.include_model_church_pecks.value == 1:
            for location, rules in self.church_first_peck_rules.items():
                new_rule = self.world.multiworld.get_location(location, self.player)
                set_rule(new_rule, rules)
        elif self.world.options.include_model_church_pecks.value == 2:
            for location, rules in self.church_all_peck_rules.items():
                new_rule = self.world.multiworld.get_location(location, self.player)
                set_rule(new_rule, rules)

        # Milestone Rules
        if self.world.options.include_milestone_locations.value and self.world.options.include_extra_tasks.value and self.world.options.include_speedrun_tasks.value:
            for location, rules in self.all_milestone_rules.items():
                new_rule = self.world.multiworld.get_location(location, self.player)
                set_rule(new_rule, rules)
        elif self.world.options.include_milestone_locations.value and self.world.options.include_extra_tasks.value:
            for location, rules in self.non_speedrun_milestone_rules.items():
                new_rule = self.world.multiworld.get_location(location, self.player)
                set_rule(new_rule, rules)
        elif self.world.options.include_milestone_locations.value and self.world.options.include_speedrun_tasks.value:
            for location, rules in self.non_to_do_as_well_milestone_rules.items():
                new_rule = self.world.multiworld.get_location(location, self.player)
                set_rule(new_rule, rules)
        elif self.world.options.include_milestone_locations.value:
            for location, rules in self.basic_milestone_rules.items():
                new_rule = self.world.multiworld.get_location(location, self.player)
                set_rule(new_rule, rules)

        # Goals
        if self.world.options.goal.value == 0:
            for location, rules in self.simple_goal_rules.items():
                new_rule = self.world.multiworld.get_location(location, self.player)
                set_rule(new_rule, rules)
        # elif self.world.options.goal.value == 1:\
            # No special locations
        elif self.world.options.goal.value == 2:
            for location, rules in self.all_main_tasks_goal_rules.items():
                new_rule = self.world.multiworld.get_location(location, self.player)
                set_rule(new_rule, rules)
        elif self.world.options.goal.value == 3:
            for location, rules in self.all_speedrun_tasks_goal_rules.items():
                new_rule = self.world.multiworld.get_location(location, self.player)
                set_rule(new_rule, rules)
        elif self.world.options.goal.value == 4:
            for location, rules in self.all_non_speedrun_tasks_goal_rules.items():
                new_rule = self.world.multiworld.get_location(location, self.player)
                set_rule(new_rule, rules)
        elif self.world.options.goal.value == 5:
            for location, rules in self.all_tasks_goal_rules.items():
                new_rule = self.world.multiworld.get_location(location, self.player)
                set_rule(new_rule, rules)
        elif self.world.options.goal.value == 6:
            for location, rules in self.four_final_tasks_rules.items():
                new_rule = self.world.multiworld.get_location(location, self.player)
                set_rule(new_rule, rules)
        
        self.world.multiworld.completion_condition[self.player] = self.steal_bell