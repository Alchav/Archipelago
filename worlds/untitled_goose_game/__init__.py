from typing import Dict, Any, ClassVar
from worlds.AutoWorld import World, WebWorld
from BaseClasses import Item, Tutorial
from Options import OptionError
from .Items import item_table, GooseGameItem, ITEM_GROUPS
from .Locations import location_table, GooseGameLocation, get_all_location_ids
from .Regions import create_regions
from .Options import GooseGameOptions
from .names import itemNames, locationNames, regionNames


class GooseGameWeb(WebWorld):
    theme = "grass"
    
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Untitled Goose Game for Archipelago multiworld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["PixelShake92, MiaSchemes"]
    )
    
    tutorials = [setup_en]


class GooseGameWorld(World):
    """
    Untitled Goose Game - It's a lovely morning in the village, 
    and you are a horrible goose.
    
    Start at the Hub (well) and collect area access items to explore!
    Complete to-do list goals, pick up items, and drag objects to send checks!
    """
    
    game = "Untitled Goose Game"
    web = GooseGameWeb()
    
    options_dataclass = GooseGameOptions
    options: GooseGameOptions
    
    item_name_to_id: ClassVar[Dict[str, int]] = {
        name: data.id for name, data in item_table.items()
    }
    
    # Register ALL possible locations - AP needs these upfront or it breaks badly (Lookin at you early MM Dev Builds)
    location_name_to_id: ClassVar[Dict[str, int]] = get_all_location_ids()
    
    item_name_groups = ITEM_GROUPS

    # Validating YAML options
    def generate_early(self) -> None:
        if self.options.include_prop_souls.value and not self.options.include_item_pickups.value:
            raise OptionError("The setting 'Include Prop Souls' requires 'Include Item Pickups' to be enabled in the YAML options.")
        if self.options.goal.value == 3 and not self.options.include_speedrun_tasks.value:
            raise OptionError("The goal 'only_speedrun_tasks' requires 'Include Speedrun Tasks' to be enabled in the YAML options.")
        elif self.options.goal.value == 4 and not self.options.include_extra_tasks.value:
            raise OptionError("The goal 'all_tasks_no_speedrun' requires 'Include Extra Tasks' to be enabled in the YAML options.")
        elif self.options.goal.value == 5 and (not self.options.include_speedrun_tasks.value or not self.options.include_extra_tasks.value):
            raise OptionError("The goal 'all_tasks' requires both 'Include Extra Tasks' and 'Include Speedrun Tasks' to be enabled in the YAML options.")
    
    def create_item(self, name: str) -> Item:
        item_data = item_table[name]
        return GooseGameItem(name, item_data.classification, item_data.id, self.player)
    
    def create_regions(self) -> None:
        create_regions(self)
    
    def get_starting_area_name(self) -> str:
        """Determine which area the player starts with access to."""
        starting_option = self.options.starting_area.value
        
        # Only 4 valid starting areas (Model Village excluded - it's the finale!)
        area_names = [
            itemNames.GARDEN_ACCESS,
            itemNames.HIGH_STREET_ACCESS,
            itemNames.BACK_GARDENS_ACCESS,
            itemNames.PUB_ACCESS,
        ]
        
        if starting_option == 4:  # Random
            return self.random.choice(area_names)
        else:
            return area_names[starting_option]
    
    def create_items(self) -> None:
        # Determine starting area
        starting_area = self.get_starting_area_name()
        
        # All area access items (5 total)
        area_items = [
            itemNames.GARDEN_ACCESS,
            itemNames.HIGH_STREET_ACCESS,
            itemNames.BACK_GARDENS_ACCESS,
            itemNames.PUB_ACCESS,
            itemNames.MODEL_VILLAGE_ACCESS,
        ]
        
        # NPC Soul items (11 total) - required for NPC-related goals
        npc_souls = [
            itemNames.NPC_GROUNDSKEEPER,
            itemNames.NPC_BOY,
            itemNames.NPC_TV_SHOP_OWNER,
            itemNames.NPC_MARKET_LADY,
            itemNames.NPC_TIDY_NEIGHBOUR,
            itemNames.NPC_MESSY_NEIGHBOUR,
            itemNames.NPC_BURLY_MAN,
            itemNames.NPC_OLD_MAN,
            itemNames.NPC_PUB_LADY,
            itemNames.NPC_FANCY_LADIES,
            itemNames.NPC_COOK,
        ]
        
        # Prop Soul items - required for picking up/dragging items
        # NOTE: NPC-tied items (Keys, Gardener Hat, Boy's Glasses, Slipper, Wooly Hat, Pub Cloth, etc)
        prop_souls = [
            # Grouped Props (26)
            itemNames.PROP_CARROTS,
            itemNames.PROP_TOMATOES,
            itemNames.PROP_PUMPKINS,
            itemNames.PROP_TOPSOIL_BAGS,
            itemNames.PROP_GREEN_QUOITS,
            itemNames.PROP_PLATES,
            itemNames.PROP_ORANGES,
            itemNames.PROP_LEEKS,
            itemNames.PROP_CUCUMBERS,
            itemNames.PROP_UMBRELLAS,
            itemNames.PROP_TINNED_FOOD,
            itemNames.PROP_SOCKS,
            itemNames.PROP_PINT_BOTTLES,
            itemNames.PROP_KNIVES,
            itemNames.PROP_GUMBOOTS,
            itemNames.PROP_FORKS,
            itemNames.PROP_APPLE_CORES,
            itemNames.PROP_APPLES,
            itemNames.PROP_SANDWICH,
            itemNames.PROP_RED_QUOITS,
            itemNames.PROP_RIBBONS,
            itemNames.PROP_WALKIE_TALKIES,
            itemNames.PROP_BOOTS,
            itemNames.PROP_MINI_PEOPLE,
            itemNames.PROP_MINI_BENCHES,
            itemNames.PROP_WEED_TOOLS,

            # Start Area One-Off Props (5)
            itemNames.PROP_DRINK_CAN,
            itemNames.PROP_TENNIS_BALL,
            itemNames.PROP_DUMMY,
            itemNames.PROP_FISHING_BOBBER,
            itemNames.PROP_TACKLE_BOX,
            
            # Garden One-Off Props (15)
            itemNames.PROP_RADIO,
            itemNames.PROP_TROWEL,
            itemNames.PROP_TULIP,
            itemNames.PROP_JAM,
            itemNames.PROP_PICNIC_MUG,
            itemNames.PROP_THERMOS,
            itemNames.PROP_STRAW_HAT,
            itemNames.PROP_RAKE,
            itemNames.PROP_PICNIC_BASKET,
            itemNames.PROP_ESKY,
            itemNames.PROP_SHOVEL,
            itemNames.PROP_WATERING_CAN,
            itemNames.PROP_MALLET,
            itemNames.PROP_WOODEN_CRATE,
            itemNames.PROP_CABBAGES,
            
            # High Street One-Off Props (22)
            itemNames.PROP_HORN_RIMMED_GLASSES,
            itemNames.PROP_RED_GLASSES,
            itemNames.PROP_SUNGLASSES,
            itemNames.PROP_LOO_PAPER,
            itemNames.PROP_TOY_CAR,
            itemNames.PROP_FOOTBALL,
            itemNames.PROP_HAIRBRUSH,
            itemNames.PROP_TOOTHRBRUSH,
            itemNames.PROP_STEREOSCOPE,
            itemNames.PROP_DISH_SOAP_BOTTLE,
            itemNames.PROP_SPRAY_BOTTLE,
            itemNames.PROP_LILY_FLOWER,
            itemNames.PROP_TOY_PLANE,
            itemNames.PROP_CHALK,
            itemNames.PROP_DUSTBIN_LID,
            itemNames.PROP_SHOPPING_BASKET,
            itemNames.PROP_PUSH_BROOM,
            itemNames.PROP_DUSTBIN,
            itemNames.PROP_BABY_DOLL,
            itemNames.PROP_PRICING_GUN,
            itemNames.PROP_ADDING_MACHINE,
            itemNames.PROP_GARAGE_ROPE,
            
            # Back Gardens One-Off Props (24)
            itemNames.PROP_CRICKET_BALL,
            itemNames.PROP_BUST_PIPE,
            itemNames.PROP_BUST_HAT,
            itemNames.PROP_BUST_GLASSES,
            itemNames.PROP_TEA_CUP,
            itemNames.PROP_NEWSPAPER,
            itemNames.PROP_BADMINTON_RACKET,
            itemNames.PROP_POT_STACK,
            itemNames.PROP_SOAP,
            itemNames.PROP_PAINTBRUSH,
            itemNames.PROP_VASE,
            itemNames.PROP_BRA,
            itemNames.PROP_ROSE,
            itemNames.PROP_ROSE_BOX,
            itemNames.PROP_CRICKET_BAT,
            itemNames.PROP_TEA_POT,
            itemNames.PROP_CLIPPERS,
            itemNames.PROP_DUCK_STATUE,
            itemNames.PROP_FROG_STATUE,
            itemNames.PROP_JEREMY_FISH,
            itemNames.PROP_NO_GOOSE_SIGN_MESSY,
            itemNames.PROP_DRAWER,
            itemNames.PROP_ENAMEL_JUG,
            itemNames.PROP_NO_GOOSE_SIGN_CLEAN,
            
            # Pub Prop One-Off Props (17)
            itemNames.PROP_LETTER,
            itemNames.PROP_PINT_GLASSES,
            itemNames.PROP_TOY_BOAT,
            itemNames.PROP_PEPPER_GRINDER,
            itemNames.PROP_CORK,
            itemNames.PROP_CANDLESTICK,
            itemNames.PROP_FLOWER_FOR_VASE,
            itemNames.PROP_HARMONICA,
            itemNames.PROP_TRAFFIC_CONE,
            itemNames.PROP_PARCEL,
            itemNames.PROP_STEALTH_BOX,
            itemNames.PROP_NO_GOOSE_SIGN_PUB,
            itemNames.PROP_PORTABLE_STOOL,
            itemNames.PROP_DARTBOARD,
            itemNames.PROP_MOP_BUCKET,
            itemNames.PROP_MOP,
            itemNames.PROP_BUCKET,
            
            # Model Village One-Off Props (10)
            itemNames.PROP_MINI_GOOSE,
            itemNames.PROP_MINI_MAIL_PILLAR,
            itemNames.PROP_MINI_PHONE_DOOR,
            itemNames.PROP_MINI_SHOVEL,
            itemNames.PROP_POPPY_FLOWER,
            itemNames.PROP_TIMBER_HANDLE,
            itemNames.PROP_MINI_BIRDBATH,
            itemNames.PROP_MINI_EASEL,
            itemNames.PROP_MINI_PUMP,
            itemNames.PROP_MINI_SUN_LOUNGE,
            
            # Golden Bell Soul is always required even when prop souls are turned off, so it's not in this list
        ]

        # Add Golden Bell Soul to pool if the chosen goal is to find the bell
        # If the chosen goal is NOT to find the bell, Golden Bell Soul is placed in pre_fill()
        if self.options.goal.value == 1:
            self.multiworld.itempool.append(self.create_item(itemNames.PROP_GOLDEN_BELL))

        # Track items added for filler calculation
        items_added = 2 # pre-fill item(s) + Golden Bell Soul
        
        # Add area items to pool (except the starting one)
        for item_name in area_items:
            if item_name == starting_area:
                # Give starting area to player directly (precollected)
                self.multiworld.push_precollected(self.create_item(item_name))
            else:
                self.multiworld.itempool.append(self.create_item(item_name))
        
        items_added += 4  # 4 area items in pool (1 is precollected)
        
        # Add NPC souls to pool if option enabled
        if self.options.include_npc_souls:
            for soul in npc_souls:
                self.multiworld.itempool.append(self.create_item(soul))
            items_added += len(npc_souls)
        
        # Add Prop souls to pool if option enabled
        if self.options.include_prop_souls:
            for soul in prop_souls:
                self.multiworld.itempool.append(self.create_item(soul))
            items_added += len(prop_souls)
        
        # NOTE: Golden Bell is NOT added to the pool here!
        # It is placed directly at "Pick up Golden Bell" location in pre_fill()
        # This ensures players must have Golden Bell Soul to access it
        
        # Calculate filler needed
        total_locations = len(self.multiworld.get_unfilled_locations(self.player))
        filler_needed = total_locations - items_added

        # Add Silent Steps first since there can only be one
        if self.options.filler_active_silent_steps:
            self.multiworld.itempool.append(self.create_item(itemNames.FILLER_SILENT_STEPS))
            filler_needed -= 1

        # Add other capped fillers next
        for i in range (self.options.filler_amount_mega_honk.value): # Max 3
            self.multiworld.itempool.append(self.create_item(itemNames.FILLER_MEGA_HONK))
            filler_needed -= 1
        for i in range (self.options.filler_amount_speedy_feet.value): # Max 10
            self.multiworld.itempool.append(self.create_item(itemNames.FILLER_SPEEDY_FEET))
            filler_needed -= 1
        for i in range (self.options.filler_amount_goose_day.value): # Max 3
            self.multiworld.itempool.append(self.create_item(itemNames.FILLER_A_GOOSE_DAY))
            filler_needed -= 1
        
        # Remaining filler items based on weights
        if filler_needed > 0:
            # Build weighted filler pool from options
            # Format: (item_name, weight)
            weighted_items = []
            coins_weight = self.options.filler_weight_coins.value
            tired_goose_weight = self.options.trap_weight_tired_goose.value
            confused_feet_weight = self.options.trap_weight_confused_feet.value
            butterbeak_weight = self.options.trap_weight_butterbeak.value
            suspicious_goose_weight = self.options.trap_weight_suspicious_goose.value
            
            # Filler items
            if coins_weight > 0:
                weighted_items.append((itemNames.FILLER_COIN, coins_weight))
            
            # Trap items
            if tired_goose_weight > 0:
                weighted_items.append((itemNames.TRAP_TIRED_GOOSE, tired_goose_weight))
            if confused_feet_weight > 0:
                weighted_items.append((itemNames.TRAP_CONFUSED_FEET, confused_feet_weight))
            if butterbeak_weight > 0:
                weighted_items.append((itemNames.TRAP_BUTTERBEAK, butterbeak_weight))
            if suspicious_goose_weight > 0:
                weighted_items.append((itemNames.TRAP_SUSPICIOUS_GOOSE, suspicious_goose_weight))
                
            total_weight = 0
            for item_name, weight in weighted_items:
                total_weight += weight
            
            for _ in range(filler_needed):
                if total_weight == 0:
                    # All weighted filler has been turned off, so Coins are forced
                    item_name = itemNames.FILLER_COIN
                else:
                    # Weighted random selection
                    roll = self.random.randint(1, total_weight)
                    if roll <= coins_weight:
                        continue
                        item_name = itemNames.FILLER_COIN
                    elif roll <= coins_weight + tired_goose_weight:
                        item_name = itemNames.TRAP_TIRED_GOOSE
                    elif roll <= coins_weight + tired_goose_weight + confused_feet_weight:
                        item_name = itemNames.TRAP_CONFUSED_FEET
                    elif roll <= coins_weight + tired_goose_weight + confused_feet_weight + butterbeak_weight:
                        item_name = itemNames.TRAP_BUTTERBEAK
                    elif roll <= coins_weight + tired_goose_weight + confused_feet_weight + butterbeak_weight + suspicious_goose_weight:
                        item_name = itemNames.TRAP_SUSPICIOUS_GOOSE
                    else:
                        continue
                        item_name = itemNames.FILLER_COIN # We shouldn't reach this, but if something goes wrong, we fall back on Coins
                
                self.multiworld.itempool.append(self.create_item(item_name))
    
    def pre_fill(self) -> None:
        """Place victory-related items at their fixed locations.
        
        The Golden Bell is placed directly at 'Pick up Golden Bell' rather than
        being in the item pool. This ensures players must:
        1. Have Pub Access (to reach Model Village area)
        2. Have Model Village Access (to enter Model Village)
        3. Have Golden Bell Soul (to spawn/pick up the bell)
        """
        golden_bell = self.create_item(itemNames.ESCAPE_SEQUENCE)
        golden_bell_location = self.multiworld.get_location(locationNames.PICKUP_GOLDEN_BELL, self.player)
        golden_bell_location.place_locked_item(golden_bell)

        # Pre-fill Golden Bell Soul depending on goal
        golden_bell_soul = self.create_item(itemNames.PROP_GOLDEN_BELL)
        goal = self.options.goal.value
        if goal == 0:  # Just reach the bell
            goal_0_location = self.multiworld.get_location(locationNames.GOAL_MODEL_VILLAGE_ENTRY, self.player)
            goal_0_location.place_locked_item(golden_bell_soul)
        # elif goal == 1:  # Find bell
        elif goal == 2:  # All main tasks
            goal_2_location = self.multiworld.get_location(locationNames.GOAL_ALL_MAIN, self.player)
            goal_2_location.place_locked_item(golden_bell_soul)
        elif goal == 3:  # Only speedrun tasks
            goal_3_location = self.multiworld.get_location(locationNames.GOAL_ALL_SPEEDRUN, self.player)
            goal_3_location.place_locked_item(golden_bell_soul)
        elif goal == 4:  # All except speedrun tasks
            goal_4_location = self.multiworld.get_location(locationNames.GOAL_ALL_NON_SPEEDRUN, self.player)
            goal_4_location.place_locked_item(golden_bell_soul)
        elif goal == 5:  # All tasks
            goal_5_location = self.multiworld.get_location(locationNames.GOAL_ALL_TASKS, self.player)
            goal_5_location.place_locked_item(golden_bell_soul)
        elif goal == 6:  # Four Final Tasks
            goal_6_location = self.multiworld.get_location(locationNames.GOAL_ALL_FINAL_TASKS, self.player)
            goal_6_location.place_locked_item(golden_bell_soul)
    
    def set_rules(self) -> None:
        from .Rules import UntitledGooseRules
        rules = UntitledGooseRules(self)
        rules.set_rules()
    
    def fill_slot_data(self) -> Dict[str, Any]:
        return {
            "starting_area": self.get_starting_area_name(),
            "goal": self.options.goal.value,
            "include_extra_tasks": self.options.include_extra_tasks.value,
            "include_speedrun_tasks": self.options.include_speedrun_tasks.value,
            "include_item_pickups": self.options.include_item_pickups.value,
            "include_drag_items": self.options.include_drag_items.value,
            "include_interactions": self.options.include_interactions.value,
            "include_model_church_pecks": self.options.include_model_church_pecks.value,
            "include_milestone_locations": self.options.include_milestone_locations.value,
            "include_new_tasks": self.options.include_new_tasks.value,
            "include_npc_souls": self.options.include_npc_souls.value,
            "include_prop_souls": self.options.include_prop_souls.value,
            "filler_amount_mega_honk": self.options.filler_amount_mega_honk.value,
            "filler_amount_speedy_feet": self.options.filler_amount_speedy_feet.value,
            "filler_active_silent_steps": self.options.filler_active_silent_steps.value,
            "filler_amount_goose_day": self.options.filler_amount_goose_day.value,
            "filler_weight_coins": self.options.filler_weight_coins.value,
            "trap_weight_tired_goose": self.options.trap_weight_tired_goose.value,
            "trap_weight_confused_feet": self.options.trap_weight_confused_feet.value,
            "trap_weight_butterbeak": self.options.trap_weight_butterbeak.value,
            "trap_weight_suspicious_goose": self.options.trap_weight_suspicious_goose.value,
            "death_link": self.options.death_link.value,
        }