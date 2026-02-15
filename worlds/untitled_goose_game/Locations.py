from typing import Dict, NamedTuple
from BaseClasses import Location

from .names import locationNames, regionNames


class GooseGameLocationData(NamedTuple):
    id: int
    region: str


class GooseGameLocation(Location):
    game = "Untitled Goose Game"


BASE_ID = 119000000

# GOAL LOCATIONS - Completing to-do list objectives (IDs 1-80)

location_table: Dict[str, GooseGameLocationData] = {
    # Garden (7 goals)
    locationNames.TASK_GARDEN_ENTRY: GooseGameLocationData(BASE_ID + 1, regionNames.GARDEN),
    locationNames.TASK_GARDEN_WET: GooseGameLocationData(BASE_ID + 2, regionNames.GARDEN),
    locationNames.TASK_GARDEN_KEYS: GooseGameLocationData(BASE_ID + 3, regionNames.GARDEN),
    locationNames.TASK_GARDEN_HAT: GooseGameLocationData(BASE_ID + 4, regionNames.GARDEN),
    locationNames.TASK_GARDEN_RAKE: GooseGameLocationData(BASE_ID + 5, regionNames.GARDEN),
    locationNames.TASK_GARDEN_PICNIC: GooseGameLocationData(BASE_ID + 6, regionNames.GARDEN),
    locationNames.TASK_GARDEN_FINAL: GooseGameLocationData(BASE_ID + 7, regionNames.GARDEN),
    
    # High Street (7 goals)
    locationNames.TASK_HIGH_STREET_BROOM: GooseGameLocationData(BASE_ID + 10, regionNames.HIGH_STREET),
    locationNames.TASK_HIGH_STREET_PHONE: GooseGameLocationData(BASE_ID + 11, regionNames.HIGH_STREET),
    locationNames.TASK_HIGH_STREET_GLASSES: GooseGameLocationData(BASE_ID + 12, regionNames.HIGH_STREET),
    locationNames.TASK_HIGH_STREET_BUY: GooseGameLocationData(BASE_ID + 13, regionNames.HIGH_STREET),
    locationNames.TASK_HIGH_STREET_TV: GooseGameLocationData(BASE_ID + 14, regionNames.HIGH_STREET),
    locationNames.TASK_HIGH_STREET_SHOPPING: GooseGameLocationData(BASE_ID + 15, regionNames.HIGH_STREET),
    locationNames.TASK_HIGH_STREET_FINAL: GooseGameLocationData(BASE_ID + 16, regionNames.HIGH_STREET),
    
    # Back Gardens (7 goals)
    locationNames.TASK_BACK_GARDENS_VASE: GooseGameLocationData(BASE_ID + 20, regionNames.BACK_GARDENS),
    locationNames.TASK_BACK_GARDENS_BUST: GooseGameLocationData(BASE_ID + 21, regionNames.BACK_GARDENS),
    locationNames.TASK_BACK_GARDENS_TEA: GooseGameLocationData(BASE_ID + 22, regionNames.BACK_GARDENS),
    locationNames.TASK_BACK_GARDENS_RIBBON: GooseGameLocationData(BASE_ID + 23, regionNames.BACK_GARDENS),
    locationNames.TASK_BACK_GARDENS_BAREFOOT: GooseGameLocationData(BASE_ID + 24, regionNames.BACK_GARDENS),
    locationNames.TASK_BACK_GARDENS_WASHING: GooseGameLocationData(BASE_ID + 25, regionNames.BACK_GARDENS),
    locationNames.TASK_BACK_GARDENS_FINAL: GooseGameLocationData(BASE_ID + 26, regionNames.BACK_GARDENS),
    
    # Pub (8 goals)
    locationNames.TASK_PUB_ENTRY: GooseGameLocationData(BASE_ID + 30, regionNames.PUB),
    locationNames.TASK_PUB_DARTBOARD: GooseGameLocationData(BASE_ID + 31, regionNames.PUB),
    locationNames.TASK_PUB_BOAT: GooseGameLocationData(BASE_ID + 32, regionNames.PUB),
    locationNames.TASK_PUB_BUM: GooseGameLocationData(BASE_ID + 33, regionNames.PUB),
    locationNames.TASK_PUB_FLOWER: GooseGameLocationData(BASE_ID + 34, regionNames.PUB),
    locationNames.TASK_PUB_PINT: GooseGameLocationData(BASE_ID + 35, regionNames.PUB),
    locationNames.TASK_PUB_TABLE: GooseGameLocationData(BASE_ID + 36, regionNames.PUB),
    locationNames.TASK_PUB_FINAL: GooseGameLocationData(BASE_ID + 37, regionNames.PUB),
    
    # Model Village (3 goals)
    locationNames.TASK_MODEL_VILLAGE_ENTRY: GooseGameLocationData(BASE_ID + 40, regionNames.MODEL_VILLAGE),
    locationNames.TASK_MODEL_VILLAGE_BELL: GooseGameLocationData(BASE_ID + 41, regionNames.MODEL_VILLAGE),
    locationNames.TASK_MODEL_VILLAGE_VICTORY: GooseGameLocationData(BASE_ID + 42, regionNames.MODEL_VILLAGE),

    # Moved here because it is always used in pre_fill()
    locationNames.PICKUP_GOLDEN_BELL: GooseGameLocationData(BASE_ID + 1143, regionNames.MODEL_VILLAGE),
}

# Extra goals (post-game) - placed in their actual area regions
extra_locations: Dict[str, GooseGameLocationData] = {
    # Extra Garden goals
    locationNames.EXTRA_TASK_GROUNDSKEEPER: GooseGameLocationData(BASE_ID + 50, regionNames.GARDEN),
    locationNames.EXTRA_TASK_CABBAGE: GooseGameLocationData(BASE_ID + 51, regionNames.GARDEN),
    
    # Extra High Street goals
    locationNames.EXTRA_TASK_PUDDLE: GooseGameLocationData(BASE_ID + 52, regionNames.HIGH_STREET),
    locationNames.EXTRA_TASK_SCALES: GooseGameLocationData(BASE_ID + 53, regionNames.HIGH_STREET),
    locationNames.EXTRA_TASK_UMBRELLA: GooseGameLocationData(BASE_ID + 54, regionNames.HIGH_STREET),
    locationNames.EXTRA_TASK_BUY: GooseGameLocationData(BASE_ID + 55, regionNames.HIGH_STREET),
    locationNames.EXTRA_TASK_FLOWERS: GooseGameLocationData(BASE_ID + 56, regionNames.HUB),
    locationNames.EXTRA_TASK_GARAGE: GooseGameLocationData(BASE_ID + 60, regionNames.HIGH_STREET),
    
    # Extra Back Gardens goals
    locationNames.EXTRA_TASK_CATCH: GooseGameLocationData(BASE_ID + 61, regionNames.BACK_GARDENS),
    locationNames.EXTRA_TASK_THROWN: GooseGameLocationData(BASE_ID + 62, regionNames.BACK_GARDENS),
    locationNames.EXTRA_TASK_BUST: GooseGameLocationData(BASE_ID + 63, regionNames.BACK_GARDENS),
    locationNames.EXTRA_TASK_GOAL: GooseGameLocationData(BASE_ID + 64, regionNames.BACK_GARDENS),
    
    # Extra Pub goals
    locationNames.EXTRA_TASK_BOAT: GooseGameLocationData(BASE_ID + 65, regionNames.PUB),
    locationNames.EXTRA_TASK_RIBBON: GooseGameLocationData(BASE_ID + 66, regionNames.PUB),
    locationNames.EXTRA_TASK_HAT: GooseGameLocationData(BASE_ID + 67, regionNames.PUB),
}

# Speedrun goals
speedrun_locations: Dict[str, GooseGameLocationData] = {
    locationNames.SPEEDRUN_TASK_GARDEN: GooseGameLocationData(BASE_ID + 70, regionNames.GARDEN),
    locationNames.SPEEDRUN_TASK_HIGH_STREET: GooseGameLocationData(BASE_ID + 71, regionNames.HIGH_STREET),
    locationNames.SPEEDRUN_TASK_BACK_GARDENS: GooseGameLocationData(BASE_ID + 72, regionNames.BACK_GARDENS),
    locationNames.SPEEDRUN_TASK_PUB: GooseGameLocationData(BASE_ID + 73, regionNames.PUB),
}

# 100% completion - currently unused
completion_location: Dict[str, GooseGameLocationData] = {
    locationNames.COMPLETION: GooseGameLocationData(BASE_ID + 80, regionNames.MODEL_VILLAGE),
}

# Milestone locations for different goal options
milestone_locations: Dict[str, GooseGameLocationData] = {
    locationNames.MILESTONE_ALL_GARDEN: GooseGameLocationData(BASE_ID + 81, regionNames.GARDEN),
    locationNames.MILESTONE_ALL_HIGH_STREET: GooseGameLocationData(BASE_ID + 82, regionNames.HIGH_STREET),
    locationNames.MILESTONE_ALL_BACK_GARDENS: GooseGameLocationData(BASE_ID + 83, regionNames.BACK_GARDENS),
    locationNames.MILESTONE_ALL_PUB: GooseGameLocationData(BASE_ID + 84, regionNames.PUB),
    locationNames.MILESTONE_ALL_EXTRA: GooseGameLocationData(BASE_ID + 85, regionNames.HUB),
    locationNames.MILESTONE_ALL_SPEEDRUN: GooseGameLocationData(BASE_ID + 86, regionNames.HUB),
    locationNames.GOAL_ALL_SPEEDRUN: GooseGameLocationData(BASE_ID + 87, regionNames.HUB),
    locationNames.MILESTONE_ALL_MAIN: GooseGameLocationData(BASE_ID + 88, regionNames.HUB),
    locationNames.GOAL_ALL_MAIN: GooseGameLocationData(BASE_ID + 89, regionNames.HUB),
    locationNames.MILESTONE_ALL_TASKS: GooseGameLocationData(BASE_ID + 90, regionNames.HUB),
    locationNames.GOAL_ALL_TASKS: GooseGameLocationData(BASE_ID + 91, regionNames.HUB),
    locationNames.GOAL_ALL_NON_SPEEDRUN: GooseGameLocationData(BASE_ID + 92, regionNames.HUB),
    locationNames.GOAL_MODEL_VILLAGE_ENTRY: GooseGameLocationData(BASE_ID + 93, regionNames.MODEL_VILLAGE),
    locationNames.GOAL_ALL_FINAL_TASKS: GooseGameLocationData(BASE_ID + 94, regionNames.HUB),
}
# Separation of the above Milestone locations for Regions.py (DO NOT INCLUDE in get_all_location_ids as they already all are)
milestone_locations_main_tasks: Dict[str, GooseGameLocationData] = {
    locationNames.MILESTONE_ALL_GARDEN: GooseGameLocationData(BASE_ID + 81, regionNames.GARDEN),
    locationNames.MILESTONE_ALL_HIGH_STREET: GooseGameLocationData(BASE_ID + 82, regionNames.HIGH_STREET),
    locationNames.MILESTONE_ALL_BACK_GARDENS: GooseGameLocationData(BASE_ID + 83, regionNames.BACK_GARDENS),
    locationNames.MILESTONE_ALL_PUB: GooseGameLocationData(BASE_ID + 84, regionNames.PUB),
    locationNames.MILESTONE_ALL_MAIN: GooseGameLocationData(BASE_ID + 88, regionNames.HUB),
}

# =============================================================================
# ITEM PICKUP LOCATIONS - First time picking up each item (IDs 1001-1150)
# =============================================================================

item_pickup_locations: Dict[str, GooseGameLocationData] = {
    # Garden items (1002-1020)
    locationNames.PICKUP_RADIO: GooseGameLocationData(BASE_ID + 1002, regionNames.GARDEN),
    locationNames.PICKUP_TROWEL: GooseGameLocationData(BASE_ID + 1003, regionNames.GARDEN),
    locationNames.PICKUP_KEYS: GooseGameLocationData(BASE_ID + 1004, regionNames.GARDEN),
    locationNames.PICKUP_TULIP: GooseGameLocationData(BASE_ID + 1006, regionNames.GARDEN),
    locationNames.PICKUP_APPLE_1: GooseGameLocationData(BASE_ID + 1007, regionNames.GARDEN),
    locationNames.PICKUP_JAM: GooseGameLocationData(BASE_ID + 1008, regionNames.GARDEN),
    locationNames.PICKUP_PICNIC_MUG: GooseGameLocationData(BASE_ID + 1009, regionNames.GARDEN),
    locationNames.PICKUP_THERMOS: GooseGameLocationData(BASE_ID + 1010, regionNames.GARDEN),
    locationNames.PICKUP_SANDWICH_R: GooseGameLocationData(BASE_ID + 1011, regionNames.GARDEN),
    locationNames.PICKUP_SANDWICH_L: GooseGameLocationData(BASE_ID + 1012, regionNames.GARDEN),
    locationNames.PICKUP_STRAW_HAT: GooseGameLocationData(BASE_ID + 1014, regionNames.GARDEN),
    locationNames.PICKUP_DRINK_CAN: GooseGameLocationData(BASE_ID + 1015, regionNames.START_AREA),
    locationNames.PICKUP_TENNIS_BALL: GooseGameLocationData(BASE_ID + 1016, regionNames.START_AREA),
    locationNames.PICKUP_GROUNDSKEEPERS_HAT: GooseGameLocationData(BASE_ID + 1017, regionNames.GARDEN),
    locationNames.PICKUP_APPLE_2: GooseGameLocationData(BASE_ID + 1018, regionNames.GARDEN),
    
    # High Street items (1021-1062)
    locationNames.PICKUP_BOYS_GLASSES: GooseGameLocationData(BASE_ID + 1021, regionNames.HIGH_STREET),
    locationNames.PICKUP_HORN_RIMMED_GLASSES: GooseGameLocationData(BASE_ID + 1022, regionNames.HIGH_STREET),
    locationNames.PICKUP_RED_GLASSES: GooseGameLocationData(BASE_ID + 1023, regionNames.HIGH_STREET),
    locationNames.PICKUP_SUNGLASSES: GooseGameLocationData(BASE_ID + 1024, regionNames.HIGH_STREET),
    locationNames.PICKUP_LOO_PAPER: GooseGameLocationData(BASE_ID + 1025, regionNames.HIGH_STREET),
    locationNames.PICKUP_TOY_CAR: GooseGameLocationData(BASE_ID + 1026, regionNames.HIGH_STREET),
    locationNames.PICKUP_HAIRBRUSH: GooseGameLocationData(BASE_ID + 1027, regionNames.HIGH_STREET),
    locationNames.PICKUP_TOOTHBRUSH: GooseGameLocationData(BASE_ID + 1028, regionNames.HIGH_STREET),
    locationNames.PICKUP_STEREOSCOPE: GooseGameLocationData(BASE_ID + 1029, regionNames.HIGH_STREET),
    locationNames.PICKUP_DISH_SOAP_BOTTLE: GooseGameLocationData(BASE_ID + 1030, regionNames.HIGH_STREET),
    locationNames.PICKUP_TINNED_FOOD_BLUE: GooseGameLocationData(BASE_ID + 1031, regionNames.HIGH_STREET),
    locationNames.PICKUP_TINNED_FOOD_YELLOW: GooseGameLocationData(BASE_ID + 1032, regionNames.HIGH_STREET),
    locationNames.PICKUP_TINNED_FOOD_ORANGE: GooseGameLocationData(BASE_ID + 1033, regionNames.HIGH_STREET),
    locationNames.PICKUP_WEED_TOOL: GooseGameLocationData(BASE_ID + 1034, regionNames.HIGH_STREET),
    locationNames.PICKUP_LILY_FLOWER: GooseGameLocationData(BASE_ID + 1035, regionNames.HIGH_STREET),
    locationNames.PICKUP_ORANGE_1: GooseGameLocationData(BASE_ID + 1036, regionNames.HIGH_STREET),
    locationNames.PICKUP_SHOP_TOMATO_1: GooseGameLocationData(BASE_ID + 1037, regionNames.HIGH_STREET),
    locationNames.PICKUP_SHOP_CARROT_1: GooseGameLocationData(BASE_ID + 1038, regionNames.HIGH_STREET),
    locationNames.PICKUP_CUCUMBER_1: GooseGameLocationData(BASE_ID + 1039, regionNames.HIGH_STREET),
    locationNames.PICKUP_LEEK_1: GooseGameLocationData(BASE_ID + 1040, regionNames.HIGH_STREET),
    locationNames.PICKUP_TOY_PLANE: GooseGameLocationData(BASE_ID + 1041, regionNames.HIGH_STREET),
    locationNames.PICKUP_PINT_BOTTLE_1: GooseGameLocationData(BASE_ID + 1042, regionNames.HUB),
    locationNames.PICKUP_SPRAY_BOTTLE: GooseGameLocationData(BASE_ID + 1043, regionNames.HIGH_STREET),
    locationNames.PICKUP_WALKIE_TALKIE_2: GooseGameLocationData(BASE_ID + 1044, regionNames.HIGH_STREET),
    locationNames.PICKUP_WALKIE_TALKIE_1: GooseGameLocationData(BASE_ID + 1045, regionNames.HIGH_STREET),
    locationNames.PICKUP_APPLE_CORE_1: GooseGameLocationData(BASE_ID + 1046, regionNames.HIGH_STREET),
    locationNames.PICKUP_APPLE_CORE_2: GooseGameLocationData(BASE_ID + 1058, regionNames.HIGH_STREET),
    locationNames.PICKUP_DUSTBIN_LID: GooseGameLocationData(BASE_ID + 1047, regionNames.HIGH_STREET),
    locationNames.PICKUP_PINT_BOTTLE_2: GooseGameLocationData(BASE_ID + 1048, regionNames.HIGH_STREET),
    locationNames.PICKUP_PINT_BOTTLE_3: GooseGameLocationData(BASE_ID + 1049, regionNames.HIGH_STREET),
    locationNames.PICKUP_CHALK: GooseGameLocationData(BASE_ID + 1050, regionNames.HIGH_STREET),
    locationNames.PICKUP_SHOP_TOMATO_2: GooseGameLocationData(BASE_ID + 1051, regionNames.HIGH_STREET),
    locationNames.PICKUP_ORANGE_2: GooseGameLocationData(BASE_ID + 1052, regionNames.HIGH_STREET),
    locationNames.PICKUP_ORANGE_3: GooseGameLocationData(BASE_ID + 1053, regionNames.HIGH_STREET),
    locationNames.PICKUP_SHOP_CARROT_2: GooseGameLocationData(BASE_ID + 1054, regionNames.HIGH_STREET),
    locationNames.PICKUP_CUCUMBER_2: GooseGameLocationData(BASE_ID + 1055, regionNames.HIGH_STREET),
    locationNames.PICKUP_LEEK_2: GooseGameLocationData(BASE_ID + 1056, regionNames.HIGH_STREET),
    locationNames.PICKUP_SHOP_CARROT_3: GooseGameLocationData(BASE_ID + 1057, regionNames.HIGH_STREET),
    locationNames.PICKUP_LEEK_3: GooseGameLocationData(BASE_ID + 1059, regionNames.HIGH_STREET),
    locationNames.PICKUP_SHOP_TOMATO_3: GooseGameLocationData(BASE_ID + 1060, regionNames.HIGH_STREET),
    locationNames.PICKUP_CUCUMBER_3: GooseGameLocationData(BASE_ID + 1061, regionNames.HIGH_STREET),
    locationNames.PICKUP_GARDEN_FORK: GooseGameLocationData(BASE_ID + 1062, regionNames.HIGH_STREET),
    
    # Back Gardens items (1071-1093)
    locationNames.PICKUP_BLUE_RIBBON: GooseGameLocationData(BASE_ID + 1071, regionNames.HUB),
    locationNames.PICKUP_DUMMY: GooseGameLocationData(BASE_ID + 1072, regionNames.HUB),
    locationNames.PICKUP_CRICKET_BALL: GooseGameLocationData(BASE_ID + 1073, regionNames.BACK_GARDENS),
    locationNames.PICKUP_BUST_PIPE: GooseGameLocationData(BASE_ID + 1074, regionNames.BACK_GARDENS),
    locationNames.PICKUP_BUST_HAT: GooseGameLocationData(BASE_ID + 1075, regionNames.BACK_GARDENS),
    locationNames.PICKUP_BUST_GLASSES: GooseGameLocationData(BASE_ID + 1076, regionNames.BACK_GARDENS),
    locationNames.PICKUP_SLIPPER_R: GooseGameLocationData(BASE_ID + 1077, regionNames.BACK_GARDENS),
    locationNames.PICKUP_SLIPPER_L: GooseGameLocationData(BASE_ID + 1078, regionNames.BACK_GARDENS),
    locationNames.PICKUP_TEA_CUP: GooseGameLocationData(BASE_ID + 1079, regionNames.BACK_GARDENS),
    locationNames.PICKUP_NEWSPAPER: GooseGameLocationData(BASE_ID + 1080, regionNames.BACK_GARDENS),
    locationNames.PICKUP_SOCK_1: GooseGameLocationData(BASE_ID + 1081, regionNames.BACK_GARDENS),
    locationNames.PICKUP_SOCK_2: GooseGameLocationData(BASE_ID + 1082, regionNames.BACK_GARDENS),
    locationNames.PICKUP_VASE: GooseGameLocationData(BASE_ID + 1083, regionNames.BACK_GARDENS),
    locationNames.PICKUP_RIBBON_RED: GooseGameLocationData(BASE_ID + 1084, regionNames.BACK_GARDENS),
    locationNames.PICKUP_POT_STACK: GooseGameLocationData(BASE_ID + 1085, regionNames.BACK_GARDENS),
    locationNames.PICKUP_SOAP: GooseGameLocationData(BASE_ID + 1086, regionNames.BACK_GARDENS),
    locationNames.PICKUP_PAINTBRUSH: GooseGameLocationData(BASE_ID + 1087, regionNames.BACK_GARDENS),
    locationNames.PICKUP_VASE_PIECE_1: GooseGameLocationData(BASE_ID + 1088, regionNames.BACK_GARDENS),
    locationNames.PICKUP_VASE_PIECE_2: GooseGameLocationData(BASE_ID + 1089, regionNames.BACK_GARDENS),
    locationNames.PICKUP_BRA: GooseGameLocationData(BASE_ID + 1090, regionNames.BACK_GARDENS),
    locationNames.PICKUP_BADMINTON_RACKET: GooseGameLocationData(BASE_ID + 1093, regionNames.BACK_GARDENS),
    locationNames.PICKUP_ROSE: GooseGameLocationData(BASE_ID + 1094, regionNames.BACK_GARDENS),
    
    # Pub items (1101-1128)
    locationNames.PICKUP_FISHING_BOBBER: GooseGameLocationData(BASE_ID + 1101, regionNames.HUB),
    locationNames.PICKUP_LETTER: GooseGameLocationData(BASE_ID + 1102, regionNames.PUB),
    locationNames.PICKUP_PLATE_1: GooseGameLocationData(BASE_ID + 1104, regionNames.PUB),
    locationNames.PICKUP_PLATE_2: GooseGameLocationData(BASE_ID + 1105, regionNames.PUB),
    locationNames.PICKUP_PLATE_3: GooseGameLocationData(BASE_ID + 1106, regionNames.PUB),
    locationNames.PICKUP_GREEN_QUOIT_1: GooseGameLocationData(BASE_ID + 1107, regionNames.PUB),
    locationNames.PICKUP_RED_QUOIT_1: GooseGameLocationData(BASE_ID + 1108, regionNames.PUB),
    locationNames.PICKUP_FORK_1: GooseGameLocationData(BASE_ID + 1109, regionNames.PUB),
    locationNames.PICKUP_FORK_2: GooseGameLocationData(BASE_ID + 1110, regionNames.PUB),
    locationNames.PICKUP_KNIFE_1: GooseGameLocationData(BASE_ID + 1111, regionNames.PUB),
    locationNames.PICKUP_KNIFE_2: GooseGameLocationData(BASE_ID + 1112, regionNames.PUB),
    locationNames.PICKUP_CORK: GooseGameLocationData(BASE_ID + 1113, regionNames.PUB),
    locationNames.PICKUP_CANDLESTICK: GooseGameLocationData(BASE_ID + 1114, regionNames.PUB),
    locationNames.PICKUP_FLOWER_FOR_VASE: GooseGameLocationData(BASE_ID + 1115, regionNames.PUB),
    locationNames.PICKUP_DART_1: GooseGameLocationData(BASE_ID + 1116, regionNames.PUB),
    locationNames.PICKUP_DART_2: GooseGameLocationData(BASE_ID + 1117, regionNames.PUB),
    locationNames.PICKUP_DART_3: GooseGameLocationData(BASE_ID + 1118, regionNames.PUB),
    locationNames.PICKUP_HARMONICA: GooseGameLocationData(BASE_ID + 1119, regionNames.PUB),
    locationNames.PICKUP_PINT_GLASS: GooseGameLocationData(BASE_ID + 1120, regionNames.PUB),
    locationNames.PICKUP_TOY_BOAT: GooseGameLocationData(BASE_ID + 1121, regionNames.PUB),
    locationNames.PICKUP_OLD_MANS_WOOLEN_HAT: GooseGameLocationData(BASE_ID + 1122, regionNames.PUB),
    locationNames.PICKUP_PEPPER_GRINDER: GooseGameLocationData(BASE_ID + 1123, regionNames.PUB),
    locationNames.PICKUP_PUB_WOMANS_CLOTH: GooseGameLocationData(BASE_ID + 1124, regionNames.PUB),
    locationNames.PICKUP_GREEN_QUOIT_2: GooseGameLocationData(BASE_ID + 1125, regionNames.PUB),
    locationNames.PICKUP_GREEN_QUOIT_3: GooseGameLocationData(BASE_ID + 1126, regionNames.PUB),
    locationNames.PICKUP_RED_QUOIT_2: GooseGameLocationData(BASE_ID + 1127, regionNames.PUB),
    locationNames.PICKUP_RED_QUOIT_3: GooseGameLocationData(BASE_ID + 1128, regionNames.PUB),

    # Model Village items (1131-1143)
    locationNames.PICKUP_MINI_PERSON_CHILD: GooseGameLocationData(BASE_ID + 1131, regionNames.MODEL_VILLAGE),
    locationNames.PICKUP_MINI_PERSON_JUMPSUIT: GooseGameLocationData(BASE_ID + 1132, regionNames.MODEL_VILLAGE),
    locationNames.PICKUP_MINI_PERSON_GARDENER: GooseGameLocationData(BASE_ID + 1133, regionNames.MODEL_VILLAGE),
    locationNames.PICKUP_MINI_SHOVEL: GooseGameLocationData(BASE_ID + 1134, regionNames.MODEL_VILLAGE),
    locationNames.PICKUP_POPPY_FLOWER: GooseGameLocationData(BASE_ID + 1135, regionNames.MODEL_VILLAGE),
    locationNames.PICKUP_MINI_PERSON_OLD_WOMAN: GooseGameLocationData(BASE_ID + 1136, regionNames.MODEL_VILLAGE),
    locationNames.PICKUP_MINI_PHONE_DOOR: GooseGameLocationData(BASE_ID + 1137, regionNames.MODEL_VILLAGE),
    locationNames.PICKUP_MINI_MAIL_PILLAR: GooseGameLocationData(BASE_ID + 1138, regionNames.MODEL_VILLAGE),
    locationNames.PICKUP_MINI_PERSON_POSTIE: GooseGameLocationData(BASE_ID + 1139, regionNames.MODEL_VILLAGE),
    locationNames.PICKUP_MINI_PERSON_VEST_MAN: GooseGameLocationData(BASE_ID + 1140, regionNames.MODEL_VILLAGE),
    locationNames.PICKUP_MINI_PERSON: GooseGameLocationData(BASE_ID + 1141, regionNames.MODEL_VILLAGE),
    locationNames.PICKUP_MINI_GOOSE: GooseGameLocationData(BASE_ID + 1144, regionNames.MODEL_VILLAGE),
    locationNames.PICKUP_TIMBER_HANDLE: GooseGameLocationData(BASE_ID + 1142, regionNames.MODEL_VILLAGE),
    # Moved to location_table as it is always needed in pre_fill()
    # locationNames.PICKUP_GOLDEN_BELL: GooseGameLocationData(BASE_ID + 1143, regionNames.MODEL_VILLAGE),
}

# =============================================================================
# DRAG ITEM LOCATIONS - First time dragging heavy items (IDs 1201-1299)
# =============================================================================

drag_item_locations: Dict[str, GooseGameLocationData] = {
    # Garden drags (1201-1215) - Topsoil moved to unique_item_drag_locations
    locationNames.DRAG_RAKE: GooseGameLocationData(BASE_ID + 1201, regionNames.GARDEN),
    locationNames.DRAG_PICNIC_BASKET: GooseGameLocationData(BASE_ID + 1202, regionNames.GARDEN),
    locationNames.DRAG_ESKY: GooseGameLocationData(BASE_ID + 1203, regionNames.GARDEN),
    locationNames.DRAG_SHOVEL: GooseGameLocationData(BASE_ID + 1205, regionNames.GARDEN),
    locationNames.DRAG_PUMKPIN_1: GooseGameLocationData(BASE_ID + 1206, regionNames.GARDEN),
    locationNames.DRAG_PUMKPIN_2: GooseGameLocationData(BASE_ID + 1207, regionNames.GARDEN),
    locationNames.DRAG_PUMKPIN_3: GooseGameLocationData(BASE_ID + 1208, regionNames.GARDEN),
    locationNames.DRAG_PUMKPIN_4: GooseGameLocationData(BASE_ID + 1209, regionNames.GARDEN),
    locationNames.DRAG_WATERING_CAN: GooseGameLocationData(BASE_ID + 1210, regionNames.GARDEN),
    locationNames.DRAG_GUMBOOT_1: GooseGameLocationData(BASE_ID + 1211, regionNames.GARDEN),
    locationNames.DRAG_GUMBOOT_2: GooseGameLocationData(BASE_ID + 1212, regionNames.GARDEN),
    locationNames.DRAG_NO_GOOSE_SIGN_GARDEN: GooseGameLocationData(BASE_ID + 1213, regionNames.GARDEN),
    locationNames.DRAG_WOODEN_CRATE: GooseGameLocationData(BASE_ID + 1214, regionNames.GARDEN),
    locationNames.DRAG_FENCE_BOLT: GooseGameLocationData(BASE_ID + 1215, regionNames.START_AREA),
    locationNames.DRAG_MALLET: GooseGameLocationData(BASE_ID + 1216, regionNames.GARDEN),
    
    # High Street drags (1220-1229)
    locationNames.DRAG_SHOPPING_BASKET: GooseGameLocationData(BASE_ID + 1220, regionNames.HIGH_STREET),
    locationNames.DRAG_UMBRELLA_BLACK: GooseGameLocationData(BASE_ID + 1221, regionNames.HIGH_STREET),
    locationNames.DRAG_PUSH_BROOM: GooseGameLocationData(BASE_ID + 1222, regionNames.HIGH_STREET),
    locationNames.DRAG_BROKEN_BROOM_HEAD: GooseGameLocationData(BASE_ID + 1223, regionNames.HIGH_STREET),
    locationNames.DRAG_DUSTBIN: GooseGameLocationData(BASE_ID + 1224, regionNames.HIGH_STREET),
    locationNames.DRAG_BABY_DOLL: GooseGameLocationData(BASE_ID + 1225, regionNames.HIGH_STREET),
    locationNames.DRAG_PRICING_GUN: GooseGameLocationData(BASE_ID + 1226, regionNames.HIGH_STREET),
    locationNames.DRAG_ADDING_MACHINE: GooseGameLocationData(BASE_ID + 1227, regionNames.HIGH_STREET),
    locationNames.DRAG_UMBRELLA_RAINBOW: GooseGameLocationData(BASE_ID + 1228, regionNames.HIGH_STREET),
    locationNames.DRAG_UMBRELLA_RED: GooseGameLocationData(BASE_ID + 1229, regionNames.HIGH_STREET),
    
    # Back Gardens drags (1240-1250)
    locationNames.DRAG_ROSE_BOX: GooseGameLocationData(BASE_ID + 1240, regionNames.BACK_GARDENS),
    locationNames.DRAG_CRICKET_BAT: GooseGameLocationData(BASE_ID + 1241, regionNames.BACK_GARDENS),
    locationNames.DRAG_TEA_POT: GooseGameLocationData(BASE_ID + 1242, regionNames.BACK_GARDENS),
    locationNames.DRAG_CLIPPERS: GooseGameLocationData(BASE_ID + 1243, regionNames.BACK_GARDENS),
    locationNames.DRAG_DUCK_STATUE: GooseGameLocationData(BASE_ID + 1244, regionNames.BACK_GARDENS),
    locationNames.DRAG_FROG_STATUE: GooseGameLocationData(BASE_ID + 1245, regionNames.BACK_GARDENS),
    locationNames.DRAG_JEREMY_FISH: GooseGameLocationData(BASE_ID + 1246, regionNames.BACK_GARDENS),
    locationNames.DRAG_NO_GOOSE_SIGN_MESSY: GooseGameLocationData(BASE_ID + 1247, regionNames.BACK_GARDENS),
    locationNames.DRAG_DRAWER: GooseGameLocationData(BASE_ID + 1248, regionNames.BACK_GARDENS),
    locationNames.DRAG_ENAMEL_JUG: GooseGameLocationData(BASE_ID + 1249, regionNames.BACK_GARDENS),
    locationNames.DRAG_NO_GOOSE_SIGN_CLEAN: GooseGameLocationData(BASE_ID + 1250, regionNames.BACK_GARDENS),
    
    # Pub drags (1270-1280)
    locationNames.DRAG_TACKLE_BOX: GooseGameLocationData(BASE_ID + 1270, regionNames.HUB),
    locationNames.DRAG_TRAFFIC_CONE: GooseGameLocationData(BASE_ID + 1271, regionNames.PUB),
    locationNames.DRAG_PARCEL: GooseGameLocationData(BASE_ID + 1272, regionNames.PUB),
    locationNames.DRAG_STEALTH_BOX: GooseGameLocationData(BASE_ID + 1273, regionNames.PUB),
    locationNames.DRAG_NO_GOOSE_SIGN_PUB: GooseGameLocationData(BASE_ID + 1274, regionNames.PUB),
    locationNames.DRAG_PORTABLE_STOOL: GooseGameLocationData(BASE_ID + 1275, regionNames.PUB),
    locationNames.DRAG_DARTBOARD: GooseGameLocationData(BASE_ID + 1276, regionNames.PUB),
    locationNames.DRAG_MOP_BUCKET: GooseGameLocationData(BASE_ID + 1277, regionNames.PUB),
    locationNames.DRAG_MOP: GooseGameLocationData(BASE_ID + 1278, regionNames.PUB),
    locationNames.DRAG_DELIVERY_BOX: GooseGameLocationData(BASE_ID + 1279, regionNames.PUB),
    locationNames.DRAG_BUCKET: GooseGameLocationData(BASE_ID + 1280, regionNames.PUB),
    
    # Model Village drags (1290-1295)
    locationNames.DRAG_MINI_BENCH: GooseGameLocationData(BASE_ID + 1290, regionNames.MODEL_VILLAGE),
    locationNames.DRAG_MINI_PUMP: GooseGameLocationData(BASE_ID + 1291, regionNames.MODEL_VILLAGE),
    locationNames.DRAG_MINI_STREET_BENCH: GooseGameLocationData(BASE_ID + 1292, regionNames.MODEL_VILLAGE),
    locationNames.DRAG_MINI_BIRDBATH: GooseGameLocationData(BASE_ID + 1293, regionNames.MODEL_VILLAGE),
    locationNames.DRAG_MINI_EASEL: GooseGameLocationData(BASE_ID + 1294, regionNames.MODEL_VILLAGE),
    locationNames.DRAG_MINI_SUN_LOUNGE: GooseGameLocationData(BASE_ID + 1295, regionNames.MODEL_VILLAGE),
}

# =============================================================================
# INTERACTION LOCATIONS - First time interacting with objects (IDs 1301-1399)
# =============================================================================

interaction_locations: Dict[str, GooseGameLocationData] = {
    # Hub interactions (1300)
    locationNames.INTERACT_WELL: GooseGameLocationData(BASE_ID + 1300, regionNames.HUB),

    # Garden interactions (1301-1303)
    locationNames.INTERACT_BIKE_BELL: GooseGameLocationData(BASE_ID + 1301, regionNames.START_AREA),
    locationNames.INTERACT_GARDEN_TAP: GooseGameLocationData(BASE_ID + 1302, regionNames.GARDEN),
    locationNames.INTERACT_SPRINKLER: GooseGameLocationData(BASE_ID + 1303, regionNames.GARDEN),
    
    # High Street interactions (1310-1317)
    locationNames.INTERACT_UNPLUG_RADIO: GooseGameLocationData(BASE_ID + 1311, regionNames.HIGH_STREET),
    locationNames.INTERACT_UMBRELLA_BLACK: GooseGameLocationData(BASE_ID + 1313, regionNames.HIGH_STREET),
    locationNames.INTERACT_UMBRELLA_RAINBOW: GooseGameLocationData(BASE_ID + 1314, regionNames.HIGH_STREET),
    locationNames.INTERACT_UMBRELLA_RED: GooseGameLocationData(BASE_ID + 1315, regionNames.HIGH_STREET),
    locationNames.INTERACT_BOYS_LACES_L: GooseGameLocationData(BASE_ID + 1316, regionNames.HIGH_STREET),
    locationNames.INTERACT_BOYS_LACES_R: GooseGameLocationData(BASE_ID + 1317, regionNames.HIGH_STREET),
    locationNames.INTERACT_FOOTBALL: GooseGameLocationData(BASE_ID + 1318, regionNames.HIGH_STREET),
    
    # Back Gardens interactions (1320-1346)
    locationNames.INTERACT_RING_BELL: GooseGameLocationData(BASE_ID + 1320, regionNames.BACK_GARDENS),
    locationNames.INTERACT_WINDMILL: GooseGameLocationData(BASE_ID + 1322, regionNames.BACK_GARDENS),
    locationNames.INTERACT_PURPLE_FLOWER: GooseGameLocationData(BASE_ID + 1323, regionNames.BACK_GARDENS),
    locationNames.INTERACT_TRELLIS: GooseGameLocationData(BASE_ID + 1324, regionNames.BACK_GARDENS),
    locationNames.INTERACT_SUNFLOWER: GooseGameLocationData(BASE_ID + 1325, regionNames.BACK_GARDENS),
    locationNames.INTERACT_TOPIARY: GooseGameLocationData(BASE_ID + 1326, regionNames.BACK_GARDENS),
    
    # Wind Chimes - individual notes (1340-1346) - left to right: G, F, E, D, C, B, A
    locationNames.INTERACT_WIND_CHIME_G: GooseGameLocationData(BASE_ID + 1340, regionNames.BACK_GARDENS),
    locationNames.INTERACT_WIND_CHIME_F: GooseGameLocationData(BASE_ID + 1341, regionNames.BACK_GARDENS),
    locationNames.INTERACT_WIND_CHIME_E: GooseGameLocationData(BASE_ID + 1342, regionNames.BACK_GARDENS),
    locationNames.INTERACT_WIND_CHIME_D: GooseGameLocationData(BASE_ID + 1343, regionNames.BACK_GARDENS),
    locationNames.INTERACT_WIND_CHIME_C: GooseGameLocationData(BASE_ID + 1344, regionNames.BACK_GARDENS),
    locationNames.INTERACT_WIND_CHIME_B: GooseGameLocationData(BASE_ID + 1345, regionNames.BACK_GARDENS),
    locationNames.INTERACT_WIND_CHIME_A: GooseGameLocationData(BASE_ID + 1346, regionNames.BACK_GARDENS),
    
    # Pub interactions (1330-1334)
    locationNames.INTERACT_VAN_DOOR_L: GooseGameLocationData(BASE_ID + 1330, regionNames.PUB),
    locationNames.INTERACT_VAN_DOOR_R: GooseGameLocationData(BASE_ID + 1331, regionNames.PUB),
    locationNames.INTERACT_BURLY_MANS_LACES_L: GooseGameLocationData(BASE_ID + 1332, regionNames.PUB),
    locationNames.INTERACT_BURLY_MANS_LACES_R: GooseGameLocationData(BASE_ID + 1333, regionNames.PUB),
    locationNames.INTERACT_PUB_TAP: GooseGameLocationData(BASE_ID + 1334, regionNames.PUB),
}

# UNIQUE TRACKED ITEMS - Runtime-renamed items (IDs 1401-1450)
# Items are renamed at runtime based on position sorting for unique tracking
unique_item_pickup_locations: Dict[str, GooseGameLocationData] = {
    # Carrots (IDs 1401-1413)
    # Carrots 1-10: Garden area (lower X positions)
    # Carrots 11-13: High Street shop display (higher X positions around 28)
    locationNames.PICKUP_CARROT_1: GooseGameLocationData(BASE_ID + 1401, regionNames.GARDEN),
    locationNames.PICKUP_CARROT_2: GooseGameLocationData(BASE_ID + 1402, regionNames.GARDEN),
    locationNames.PICKUP_CARROT_3: GooseGameLocationData(BASE_ID + 1403, regionNames.GARDEN),
    locationNames.PICKUP_CARROT_4: GooseGameLocationData(BASE_ID + 1404, regionNames.GARDEN),
    locationNames.PICKUP_CARROT_5: GooseGameLocationData(BASE_ID + 1405, regionNames.GARDEN),
    locationNames.PICKUP_CARROT_6: GooseGameLocationData(BASE_ID + 1406, regionNames.GARDEN),
    locationNames.PICKUP_CARROT_7: GooseGameLocationData(BASE_ID + 1407, regionNames.GARDEN),
    locationNames.PICKUP_CARROT_8: GooseGameLocationData(BASE_ID + 1408, regionNames.GARDEN),
    locationNames.PICKUP_CARROT_9: GooseGameLocationData(BASE_ID + 1409, regionNames.GARDEN),
    locationNames.PICKUP_CARROT_10: GooseGameLocationData(BASE_ID + 1410, regionNames.GARDEN),
    
    # Pub Tomatoes (IDs 1421-1431)
    locationNames.PICKUP_PUB_TOMATO_1: GooseGameLocationData(BASE_ID + 1421, regionNames.PUB),
    locationNames.PICKUP_PUB_TOMATO_2: GooseGameLocationData(BASE_ID + 1422, regionNames.PUB),
    locationNames.PICKUP_PUB_TOMATO_3: GooseGameLocationData(BASE_ID + 1423, regionNames.PUB),
    locationNames.PICKUP_PUB_TOMATO_4: GooseGameLocationData(BASE_ID + 1424, regionNames.PUB),
    locationNames.PICKUP_PUB_TOMATO_5: GooseGameLocationData(BASE_ID + 1425, regionNames.PUB),
    locationNames.PICKUP_PUB_TOMATO_6: GooseGameLocationData(BASE_ID + 1426, regionNames.PUB),
    locationNames.PICKUP_PUB_TOMATO_7: GooseGameLocationData(BASE_ID + 1427, regionNames.PUB),
    locationNames.PICKUP_PUB_TOMATO_8: GooseGameLocationData(BASE_ID + 1428, regionNames.PUB),
    locationNames.PICKUP_PUB_TOMATO_9: GooseGameLocationData(BASE_ID + 1429, regionNames.PUB),
    locationNames.PICKUP_PUB_TOMATO_10: GooseGameLocationData(BASE_ID + 1430, regionNames.PUB),
    locationNames.PICKUP_PUB_TOMATO_11: GooseGameLocationData(BASE_ID + 1431, regionNames.PUB),
    
    # Boots (IDs 1440-1441)
    locationNames.PICKUP_BOOT_START: GooseGameLocationData(BASE_ID + 1440, regionNames.START_AREA),
    locationNames.PICKUP_BOOT_HUB: GooseGameLocationData(BASE_ID + 1441, regionNames.HUB),
}
unique_item_drag_locations: Dict[str, GooseGameLocationData] = {
    # Topsoil Bags (IDs 1450-1452)
    locationNames.DRAG_TOPSOIL_BAG_1: GooseGameLocationData(BASE_ID + 1450, regionNames.GARDEN),
    locationNames.DRAG_TOPSOIL_BAG_2: GooseGameLocationData(BASE_ID + 1451, regionNames.GARDEN),
    locationNames.DRAG_TOPSOIL_BAG_3: GooseGameLocationData(BASE_ID + 1452, regionNames.GARDEN),
}

# Sandcastle peck locations (1350-1384) - 35 total raw pecks
sandcastle_peck_locations: Dict[str, GooseGameLocationData] = {
    # Doorway side - 19 pecks
    locationNames.PECK_DOORWAY_1: GooseGameLocationData(BASE_ID + 1350, regionNames.MODEL_VILLAGE),
    locationNames.PECK_DOORWAY_2: GooseGameLocationData(BASE_ID + 1351, regionNames.MODEL_VILLAGE),
    locationNames.PECK_DOORWAY_3: GooseGameLocationData(BASE_ID + 1352, regionNames.MODEL_VILLAGE),
    locationNames.PECK_DOORWAY_4: GooseGameLocationData(BASE_ID + 1353, regionNames.MODEL_VILLAGE),
    locationNames.PECK_DOORWAY_5: GooseGameLocationData(BASE_ID + 1354, regionNames.MODEL_VILLAGE),
    locationNames.PECK_DOORWAY_6: GooseGameLocationData(BASE_ID + 1355, regionNames.MODEL_VILLAGE),
    locationNames.PECK_DOORWAY_7: GooseGameLocationData(BASE_ID + 1356, regionNames.MODEL_VILLAGE),
    locationNames.PECK_DOORWAY_8: GooseGameLocationData(BASE_ID + 1357, regionNames.MODEL_VILLAGE),
    locationNames.PECK_DOORWAY_9: GooseGameLocationData(BASE_ID + 1358, regionNames.MODEL_VILLAGE),
    locationNames.PECK_DOORWAY_10: GooseGameLocationData(BASE_ID + 1359, regionNames.MODEL_VILLAGE),
    locationNames.PECK_DOORWAY_11: GooseGameLocationData(BASE_ID + 1360, regionNames.MODEL_VILLAGE),
    locationNames.PECK_DOORWAY_12: GooseGameLocationData(BASE_ID + 1361, regionNames.MODEL_VILLAGE),
    locationNames.PECK_DOORWAY_13: GooseGameLocationData(BASE_ID + 1362, regionNames.MODEL_VILLAGE),
    locationNames.PECK_DOORWAY_14: GooseGameLocationData(BASE_ID + 1363, regionNames.MODEL_VILLAGE),
    locationNames.PECK_DOORWAY_15: GooseGameLocationData(BASE_ID + 1364, regionNames.MODEL_VILLAGE),
    locationNames.PECK_DOORWAY_16: GooseGameLocationData(BASE_ID + 1365, regionNames.MODEL_VILLAGE),
    locationNames.PECK_DOORWAY_17: GooseGameLocationData(BASE_ID + 1366, regionNames.MODEL_VILLAGE),
    locationNames.PECK_DOORWAY_18: GooseGameLocationData(BASE_ID + 1367, regionNames.MODEL_VILLAGE),
    locationNames.PECK_DOORWAY_19: GooseGameLocationData(BASE_ID + 1368, regionNames.MODEL_VILLAGE),
    # Tower side - 16 pecks
    locationNames.PECK_TOWER_1: GooseGameLocationData(BASE_ID + 1369, regionNames.MODEL_VILLAGE),
    locationNames.PECK_TOWER_2: GooseGameLocationData(BASE_ID + 1370, regionNames.MODEL_VILLAGE),
    locationNames.PECK_TOWER_3: GooseGameLocationData(BASE_ID + 1371, regionNames.MODEL_VILLAGE),
    locationNames.PECK_TOWER_4: GooseGameLocationData(BASE_ID + 1372, regionNames.MODEL_VILLAGE),
    locationNames.PECK_TOWER_5: GooseGameLocationData(BASE_ID + 1373, regionNames.MODEL_VILLAGE),
    locationNames.PECK_TOWER_6: GooseGameLocationData(BASE_ID + 1374, regionNames.MODEL_VILLAGE),
    locationNames.PECK_TOWER_7: GooseGameLocationData(BASE_ID + 1375, regionNames.MODEL_VILLAGE),
    locationNames.PECK_TOWER_8: GooseGameLocationData(BASE_ID + 1376, regionNames.MODEL_VILLAGE),
    locationNames.PECK_TOWER_9: GooseGameLocationData(BASE_ID + 1377, regionNames.MODEL_VILLAGE),
    locationNames.PECK_TOWER_10: GooseGameLocationData(BASE_ID + 1378, regionNames.MODEL_VILLAGE),
    locationNames.PECK_TOWER_11: GooseGameLocationData(BASE_ID + 1379, regionNames.MODEL_VILLAGE),
    locationNames.PECK_TOWER_12: GooseGameLocationData(BASE_ID + 1380, regionNames.MODEL_VILLAGE),
    locationNames.PECK_TOWER_13: GooseGameLocationData(BASE_ID + 1381, regionNames.MODEL_VILLAGE),
    locationNames.PECK_TOWER_14: GooseGameLocationData(BASE_ID + 1382, regionNames.MODEL_VILLAGE),
    locationNames.PECK_TOWER_15: GooseGameLocationData(BASE_ID + 1383, regionNames.MODEL_VILLAGE),
    locationNames.PECK_TOWER_16: GooseGameLocationData(BASE_ID + 1384, regionNames.MODEL_VILLAGE),
}

# Sandcastle first peck locations (1390-1391) - 2 pecks
sandcastle_first_peck_locations: Dict[str, GooseGameLocationData] = {
    # First pecks only option
    locationNames.PECK_DOORWAY: GooseGameLocationData(BASE_ID + 1390, regionNames.MODEL_VILLAGE),
    locationNames.PECK_TOWER: GooseGameLocationData(BASE_ID + 1391, regionNames.MODEL_VILLAGE),
}

# =============================================================================
# NEW TASK LOCATIONS - A new list of tasks made for Archipelago (1500-1520)
# =============================================================================
new_tasks_locations: Dict[str, GooseGameLocationData] = {
    locationNames.DROP_MAIL_IN_WELL: GooseGameLocationData(BASE_ID + 1500, regionNames.PUB),
    locationNames.OPEN_INTRO_GATE: GooseGameLocationData(BASE_ID + 1501, regionNames.START_AREA),
    locationNames.BREAK_THROUGH_BOARDS: GooseGameLocationData(BASE_ID + 1502, regionNames.BACK_GARDENS),
    locationNames.SHORT_OUT_RADIO: GooseGameLocationData(BASE_ID + 1503, regionNames.GARDEN),
    locationNames.LOCK_GROUNDSKEEPER_IN: GooseGameLocationData(BASE_ID + 1504, regionNames.GARDEN),
    locationNames.MAKE_WOMAN_FIX_TOPIARY: GooseGameLocationData(BASE_ID + 1505, regionNames.BACK_GARDENS),
    locationNames.POSE_AS_DUCK: GooseGameLocationData(BASE_ID + 1506, regionNames.BACK_GARDENS),
    locationNames.DRESS_UP_BUSH: GooseGameLocationData(BASE_ID + 1507, regionNames.BACK_GARDENS),
    locationNames.TRIP_BURLY_MAN: GooseGameLocationData(BASE_ID + 1508, regionNames.PUB),
    locationNames.BREAK_PINT_GLASS: GooseGameLocationData(BASE_ID + 1509, regionNames.PUB),
    locationNames.INTERIOR_REDECORATING: GooseGameLocationData(BASE_ID + 1510, regionNames.BACK_GARDENS),
    locationNames.TRAP_TV_SHOP_OWNER_GARAGE: GooseGameLocationData(BASE_ID + 1511, regionNames.HIGH_STREET),
    locationNames.PERFORM_WITH_HARMONICA: GooseGameLocationData(BASE_ID + 1512, regionNames.PUB),
}


def get_all_locations(include_extra: bool = False, include_speedrun: bool = False, 
                      include_items: bool = True, include_drags: bool = True,
                      include_interactions: bool = True, include_unique: bool = True,
                      include_sandcastle: bool = True) -> Dict[str, GooseGameLocationData]:
    """Get locations based on options (for region creation)"""
    locations = dict(location_table)
    
    if include_extra:
        locations.update(extra_locations)
        locations.update(completion_location)
    
    if include_speedrun:
        locations.update(speedrun_locations)
    
    if include_items:
        locations.update(item_pickup_locations)
    
    if include_drags:
        locations.update(drag_item_locations)
    
    if include_interactions:
        locations.update(interaction_locations)
    
    if include_unique:
        locations.update(unique_item_pickup_locations)
    
    if include_unique:
        locations.update(unique_item_drag_locations)
    
    if include_sandcastle:
        locations.update(sandcastle_peck_locations)
    
    return locations


def get_all_location_ids() -> Dict[str, int]:
    """Get ALL location name->ID mappings (for AP registration)
    
    IMPORTANT: AP requires all possible locations registered upfront,
    regardless of whether they're enabled by options.
    """
    all_locs = {}
    all_locs.update({name: data.id for name, data in location_table.items()})
    all_locs.update({name: data.id for name, data in extra_locations.items()})
    all_locs.update({name: data.id for name, data in speedrun_locations.items()})
    all_locs.update({name: data.id for name, data in completion_location.items()})
    all_locs.update({name: data.id for name, data in milestone_locations.items()})
    all_locs.update({name: data.id for name, data in item_pickup_locations.items()})
    all_locs.update({name: data.id for name, data in drag_item_locations.items()})
    all_locs.update({name: data.id for name, data in interaction_locations.items()})
    all_locs.update({name: data.id for name, data in unique_item_pickup_locations.items()})
    all_locs.update({name: data.id for name, data in unique_item_drag_locations.items()})
    all_locs.update({name: data.id for name, data in sandcastle_peck_locations.items()})
    all_locs.update({name: data.id for name, data in sandcastle_first_peck_locations.items()})
    all_locs.update({name: data.id for name, data in new_tasks_locations.items()})
    return all_locs
