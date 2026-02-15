from dataclasses import dataclass
from Options import Toggle, Range, Choice, PerGameCommonOptions


class StartingArea(Choice):
    """Which area the player starts with access to. 
    Without this, you'd be stuck at the hub with nothing to do!
    Model Village is not an option since it's the finale area."""
    display_name = "Starting Area"
    option_garden = 0
    option_high_street = 1
    option_back_gardens = 2
    option_pub = 3
    # option_random = 4
    default = 4  # Random by default


class Goal(Choice):
    """Victory is always when you steal the Golden Bell and bring it home. Goal settings change how it spawns:
    only_steal = Simply reach the bell and steal it!
    find_bell = The Golden Bell is lost somewhere in the multiworld! Find it before you can steal it.
    all_main_tasks = Complete all four area task lists to spawn the Golden Bell.
    only_speedrun_tasks = Complete all 'To Do (Quickly!!)' tasks to spawn the Golden Bell.
    all_tasks_no_speedrun = Complete all four area task lists as well as the 'To Do (As Well)' task lists to spawn the Golden Bell.
    all_tasks = Complete all task lists to spawn the Golden Bell.
    four_final_tasks = Complete the final task of each of the four area task lists to spawn the Golden Bell."""
    display_name = "Goal"
    option_only_steal = 0
    option_find_bell = 1
    option_all_main_tasks = 2
    option_only_speedrun_tasks = 3
    option_all_tasks_no_speedrun = 4
    option_all_tasks = 5
    option_four_final_tasks = 6
    default = 0


class IncludeNPCSouls(Toggle):
    """When enabled, NPCs won't appear until you receive their soul item.
    This adds NPC souls to the item pool and gates NPC-related goals behind them."""
    display_name = "Include NPC Souls"
    default = True


class LogicallyRequireNPCSouls(Toggle):
    """This option is only for when NPC Souls are included in the pool. When enabled, generation will think that all NPCs are required in order to complete the goal.
    You may be more likely to find them in your seed, which may make the experience more satisfying. NPCs make the final sequence of stealing the bell more difficult and interesting.
    WARNING: Only enable this option if you know what you are doing. Many NPCs may not be required in order to complete the goal, and doing so without them will be going out of logic!"""
    display_name = "Logically Require NPC Souls"
    default = False


class IncludeProps(Toggle):
    """When enabled, items can't be picked up or dragged until you receive them.
    This adds props to the item pool and gates item interactions behind them.
    If the find_bell goal is chosen and this option is disabled, the Golden Bell will be the only one added to the pool."""
    display_name = "Include Props"
    default = True


class IncludeExtraTasks(Toggle):
    """Include post-game extra challenge tasks as locations.
    Must be enabled when choosing either the all_tasks_no_speedrun or all_tasks goal."""
    display_name = "Include Extra Tasks"
    default = False


class IncludeSpeedrunTasks(Toggle):
    """Include speedrun challenge tasks (complete areas before noon).
    Must be enabled when choosing either the only_speedrun_tasks or all_tasks goal."""
    display_name = "Include Speedrun Tasks"
    default = False


class IncludeItemPickups(Toggle):
    """Include first-time item pickups as locations (100+ additional checks).
    Must be enabled when including prop souls in the pool."""
    display_name = "Include Item Pickups"
    default = True


class IncludeDragItems(Toggle):
    """Include first-time drag item locations (50+ additional checks for heavy/draggable items)."""
    display_name = "Include Drag Items"
    default = True


class IncludeInteractions(Toggle):
    """Include interaction locations (ringing bells, spinning windmills, breaking boards, etc.)."""
    display_name = "Include Interactions"
    default = True


class IncludeModelChurchPecks(Choice):
    """Include locations for pecking the model church apart
    first_pecks_only - includes two locations; 
    all_pecks - includes all 35 pecks each as their own location"""
    display_name = "Include Model Church Pecks"
    option_none = 0
    option_first_pecks_only = 1
    option_all_pecks = 2
    default = 1


class IncludeMilestoneLocations(Toggle):
    """Include extra locations for completing all garden tasks, all high street tasks, etc.
    - Including extra tasks adds a milestone for completing all To Do (As Well) tasks
    - Including speedrun tasks adds a milestone for completing all speedrun tasks"""
    display_name = "Include Milestone Locations"
    default = True


class IncludeNewTasks(Toggle):
    """Include locations for new tasks created for this archipelago!
    Some of these happen naturally throughout gameplay, and some are more involved.
    You can view these tasks at any time in-game by pressing F4. New tasks include:
    - Break the intro gate
    - Drop some mail in the well
    - Short out the garden radio
    - Lock the groundskeeper IN the garden
    - Trap the TV shop owner in the garage
    - Break through the boards to the back gardens
    - Make the woman fix the topiary
    - Pose as a duck statue
    - Dress up the bush with both ribbons
    - Do some interior redecorating
    - Trip the burly man
    - Break a pint glass
    - Perform at the pub with a harmonica"""
    display_name = "Include New Tasks"
    default = False


class FillerAmountMegaHonk(Range):
    """Amount of Mega Honk in the filler pool.
    Mega Honk effects - upgraded honking abilities
    Level 1: All NPCs react to honk (draws attention) - default behavior enhanced
    Level 2: Increased honk detection distance - always heard regardless of distance
    Level 3: Scary honk - NPCs drop held items"""
    display_name = "Filler Amount: Mega Honk"
    range_start = 0
    range_end = 3
    default = 3


class FillerAmountSpeedyFeet(Range):
    """Amount of Speedy Feet in filler pool. Speedy Feet increases your run speed."""
    display_name = "Filler Amount: Speedy Feet"
    range_start = 0
    range_end = 10
    default = 10


class FillerActiveSilentSteps(Toggle):
    """Whether or not Silent Steps is in the filler pool. Silent Steps prevents NPCs from hearing your footsteps."""
    display_name = "Filler Active: Silent Steps"
    default = True


class FillerAmountGooseDay(Range):
    """Amount of A Goose Day in filler pool. A Goose Day causes NPCs to ignore you for 15 seconds."""
    display_name = "Filler Amount: A Goose Day"
    range_start = 0
    range_end = 3
    default = 3

class FillerWeightCoins(Range):
    """Weight for Coins in the filler pool. Set to 0 to disable this filler.
    Please note that if you turn off all traps below, this filler item will be chosen to fill all remaining spots regardless of chosen weight."""
    display_name = "Filler Weight: Coins"
    range_start = 0
    range_end = 100
    default = 80


class TrapWeightTiredGoose(Range):
    """Weight for Tired Goose trap in the filler pool. Set to 0 to disable this trap."""
    display_name = "Trap Weight: Tired Goose"
    range_start = 0
    range_end = 100
    default = 5


class TrapWeightConfusedFeet(Range):
    """Weight for Confused Feet trap in the filler pool. Set to 0 to disable this trap."""
    display_name = "Trap Weight: Confused Feet"
    range_start = 0
    range_end = 100
    default = 5


class TrapWeightButterbeak(Range):
    """Weight for Butterbeak trap in the filler pool. Set to 0 to disable this trap."""
    display_name = "Trap Weight: Butterbeak"
    range_start = 0
    range_end = 100
    default = 5


class TrapWeightSuspiciousGoose(Range):
    """Weight for Suspicious Goose trap in the filler pool. Set to 0 to disable this trap."""
    display_name = "Trap Weight: Suspicious Goose"
    range_start = 0
    range_end = 100
    default = 5


class DeathLink(Toggle):
    """When you get caught/shooed, everyone dies. When someone else dies, you drop whatever you're holding and get teleported to the hub."""
    display_name = "Death Link"
    default = False


@dataclass
class GooseGameOptions(PerGameCommonOptions):
    starting_area: StartingArea
    goal: Goal
    include_npc_souls: IncludeNPCSouls
    logically_require_npc_souls: LogicallyRequireNPCSouls
    include_prop_souls: IncludeProps
    include_extra_tasks: IncludeExtraTasks
    include_speedrun_tasks: IncludeSpeedrunTasks
    include_item_pickups: IncludeItemPickups
    include_drag_items: IncludeDragItems
    include_interactions: IncludeInteractions
    include_model_church_pecks: IncludeModelChurchPecks
    include_milestone_locations: IncludeMilestoneLocations
    include_new_tasks: IncludeNewTasks
    filler_amount_mega_honk: FillerAmountMegaHonk
    filler_amount_speedy_feet: FillerAmountSpeedyFeet
    filler_active_silent_steps: FillerActiveSilentSteps
    filler_amount_goose_day: FillerAmountGooseDay
    filler_weight_coins: FillerWeightCoins
    trap_weight_tired_goose: TrapWeightTiredGoose
    trap_weight_confused_feet: TrapWeightConfusedFeet
    trap_weight_butterbeak: TrapWeightButterbeak
    trap_weight_suspicious_goose: TrapWeightSuspiciousGoose
    death_link: DeathLink