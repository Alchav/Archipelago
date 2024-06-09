import typing
from Options import Choice, OptionSet, PerGameCommonOptions, Range, OptionDict, OptionList, Option, StartInventoryPool, Toggle, DefaultOnToggle
from dataclasses import dataclass
from . import map_rando_game_data

from schema import Schema, And

# schema helpers
IntRange = lambda low, high: And(int, lambda f: low <= f <= high)

class DeathLink(Choice):
    """When DeathLink is enabled and someone dies, you will die. With survive reserve tanks can save you."""
    display_name = "Death Link"
    option_disable = 0
    option_enable = 1
    option_enable_survive = 3
    alias_false = 0
    alias_true = 1
    default = 0

class RemoteItems(Toggle):
    """Indicates you get items sent from your own world. This allows coop play of a world."""
    display_name = "Remote Items"  

class Preset(Choice):
    """
    Skill assumptions determine which tricks the randomizer assumes the player is able to perform.
    Use "Custom" to specify your own Techs, Strats, Leniencies and Boss Proficiencies.
    """
    display_name = "Preset"
    option_Basic = 0
    option_Medium = 1
    option_Hard = 2
    option_VeryHard = 3
    option_Expert = 4
    option_Extreme = 5
    option_Insane = 6
    option_Beyond = 7
    option_Custom = 8
    default = 2

class Techs(OptionSet):
    "Custom list of techs used when Preset is set to Custom. The list can also contain one of the Preset name to include all its Techs."
    display_name = "Techs"
    valid_keys = frozenset(map_rando_game_data.tech_isv + ["Basic", "Medium", "Hard", "VeryHard", "Expert", "Extreme", "Insane", "Beyond"])

class Strats(OptionSet):
    "Custom list of strats used when Preset is set to Custom. The list can also contain one of the Preset name to include all its Strats."
    display_name = "Strats"
    valid_keys = frozenset(map_rando_game_data.notable_strat_isv + ["Basic", "Medium", "Hard", "VeryHard", "Expert", "Extreme", "Insane", "Beyond"])

class ItemPool(Choice):
    """
    This setting affects the amount of ammo and tanks which may be placed:

    - Full: 46 Missile packs, 10 Super packs, 10 Power Bomb packs, 14 Energy Tanks, 4 Reserve Tanks
    - Reduced: 12 Missile packs, 6 Super packs, 6 Power Bomb packs, 3 Energy Tanks, 3 Reserve Tanks
    - Custom: Use CustomItemPool to specify ammo and tanks
    
    Using a reduced amount of ammo and tanks causes some item locations to be missing an item. Regardless of the item pool settings, 
    extra Energy Tanks may be added to ensure the game is beatable based on selected difficulty settings.
    """
    display_name = "Item Pool"
    option_Full = 0
    option_Reduced = 1
    option_Custom = 2
    default = 0

class CustomItemPool(OptionDict):
    """
    This setting is only used when ItemPool is set to Custom. The default is the vanilla amounts.
    Values must be in the following range:
     - Missile between 2 and 46
     - ETank between 2 and 14
     - ReserveTank between 1 and 4
     - Super between 2 and 19
     - PowerBomb between 2 and 19
    """    
    display_name = "Custom Item Pool"
    default = {
        "Missile": 46,
        "ETank": 14,
        "ReserveTank": 4,
        "Super": 10,
        "PowerBomb": 10
    }
    reduced = {
        "Missile": 12,
        "ETank": 3,
        "ReserveTank": 3,
        "Super": 6,
        "PowerBomb": 5
    }
    schema = Schema({
        "Missile": IntRange(2, 46),
        "ETank": IntRange(2, 14),
        "ReserveTank": IntRange(1, 4),
        "Super": IntRange(2, 19),
        "PowerBomb": IntRange(1, 19)
    })

class ShinesparkTiles(Range):
    """Smaller values assume ability to short-charge over shorter distances"""
    display_name = "Shinespark tiles count"
    range_start = 13
    range_end = 33
    default = 26

class HeatedShinesparkTiles(Range):
    """Smaller values assume ability to short-charge over shorter distances"""
    display_name = "Heated Shinespark tiles count"
    range_start = 14
    range_end = 33
    default = 29

class ShinechargeLeniencyFrames(Range):
    """Extra time assumed needed to position to activate a shinespark"""
    display_name = "Heated Shinespark tiles count"
    range_start = 0
    range_end = 120
    default = 90
    
class ResourceMultiplier(Range):
    """Leniency factor on assumed energy & ammo usage, between 1 and 300"""
    display_name = "Resource multiplier"
    range_start = 1
    range_end = 300
    default = 100

class GateGlitchLeniency(Range):
    """Expected failed attempts to get a successful gate glitch"""
    display_name = "Gate Glitch Leniency"
    range_start = 0
    range_end = 100
    default = 14

class DoorStuckLeniency(Range):
    """Expected failed attempts to get door stuck for X-ray climbing"""
    display_name = "Door Stuck Leniency"
    range_start = 0
    range_end = 100
    default = 2

class EscapeTimerMultiplier(Range):
    """Leniency factor on escape timer, between 1 and 300"""
    display_name = "Escape timer multiplier"
    range_start = 1
    range_end = 300
    default = 100

class StartLocationMode(Choice):
    """
    This setting determines where Samus begins the game:
    - Ship: Samus begins in Landing Site at the Ship.
    - RandomRoom: Samus begins in a random room somewhere on Zebes.
    - Escape: Samus begins in Mother Brain Room at the start of the escape sequence.
    """
    display_name = "Start location"
    option_Ship = 0
    option_RandomRoom = 1
    option_Escape = 2

class RandomizedStart(Toggle):
    """
    This setting determines where Samus begins the game:

    - Ship: Samus begins in Landing Site at the Ship.
    - Random: Samus begins in a random room somewhere on Zebes.
    """
    display_name = "Randomized start location"  

class PhantoonProficiency(Range):
    """Skill level at the Phantoon fight, between 0 and 100"""
    display_name = "Phantoon proficiency"
    range_start = 0
    range_end = 100
    default = 50

class DraygonProficiency(Range):
    """Skill level at the Draygon fight, between 0 and 100"""
    display_name = "Draygon proficiency"
    range_start = 0
    range_end = 100
    default = 50

class RidleyProficiency(Range):
    """Skill level at the Ridley fight, between 0 and 100"""
    display_name = "Ridley proficiency"
    range_start = 0
    range_end = 100
    default = 50

class BotwoonProficiency(Range):
    """Skill level at the Botwoon fight, between 0 and 100"""
    display_name = "Botwoon proficiency"
    range_start = 0
    range_end = 100
    default = 50

class MotherBrainProficiency(Range):
    """Skill level at the Mother Brain fight, between 0 and 100"""
    display_name = "Mother Brain proficiency"
    range_start = 0
    range_end = 100
    default = 50

class SaveAnimals(Choice):
    """
    This setting affects whether saving the animals (Etecoons and Dachora) will be possible and/or required in the escape:

    - No: Saving the animals might not be possible to do.
    - Maybe: Extra escape time is given, making it possible but not required to save the animals.
    - Yes: Extra escape time is given, and the player is required to save the animals.
    """
    display_name = "Save the animals"
    option_Off = 0
    alias_No = 0
    option_Maybe = 1
    option_On = 2
    alias_Yes = 2
    default = 0

class EarlySave(Toggle):
    """
    This option ensures that a save station will be accessible early in the game,
    no later than during the second logical progression step. This has an effect 
    only when using Random start location.
    """
    display_name = "Guaranteed early save station"

class UltraLowQol(Toggle):
    """
    This disables many quality-of-life changes that are normally built into the randomizer, including:

    - Faster cutscenes (e.g., involving Baby Metroid, Mother Brain, save & refill stations)
    - Refill stations giving Supers and Power Bombs in addition to Missiles
    - The auto-save before the escape sequence
    - Patching out major glitches: Spacetime beam, GT code, and out-of-bounds (death trigger)
    - Fast decompression (for quicker room loading)
    - Camera fix when entering Kraid's, Crocomire's, or Spore Spawn's room
    - Graphical fixes when exiting boss rooms
    - Graphical fix to Bomb Torizo statue crumble animation

    This setting also automatically disables all other quality-of-life options. For AP,
    enabling any quality-of-life option DOESNT causes this setting to be automatically disabled. Also, item fanfares are always disabled.

    This setting is not recommended for most players, but it is an option for those wanting the game to 
    feel and behave as vanilla as possible. If enabled, expect to encounter a significant amount of graphical glitches.

    Note: If this setting is enabled, the logic will take into account that refill stations no longer give Supers and Power Bombs.
    """
    display_name = "Ultra-low quality of life"

class QualityOfLife(Choice):
    """
    These options help provide a smoother, more intuitive, and less tedious game experience.
    Players wanting a full experience of exploration may want to disable some of these options.
    Three presets are provided:

    - Off: All quality-of-life options are turned off. This is for players who want a full experience
        of exploration, with a similar feel to the original game. This may involve a lot of wandering around and backtracking 
        to figure out where to go. Map stations are harder to find and provide minimal assistance as all item dots look the same.
    - Low: Many quality-of-life options are turned off, restoring some unintuitive but potentially
        interesting vanilla game behavior: some items do not spawn until defeating Phantoon or waking the planet, 
        Acid Chozo statue requires Space Jump to use it, and completing the escape may require collecting certain items 
        and/or carefully managing energy in the Mother Brain fight. Map stations are somewhat less powerful because all ammo and 
        tank items appear as small dots the same as Missiles.
    - Default: Quality-of-life options are turned to their generally recommended settings (mostly on).
        Map stations are very useful, with different item dot shapes to distinguish three tiers of items: Missiles, other 
        ammo/tank items, and unique items.
    - Max: All quality-of-life options are turned on to their highest settings. This includes 
        respin, lenient Space Jump, and momentum conservation to more easily control Samus, and an extra-fast Mother Brain fight
        that completely skips the second and third phases.
    - Custom: Uses your specified quality of life options, defaulting to "Default" Quality-of-life values if not specified.
    """
    display_name = "Quality-of-life options"
    option_Off = 0
    option_Low = 1
    option_Default = 2
    option_Max = 3
    option_Custom = 4
    default = 2

class Objectives(Choice):
    """
    This setting determines the conditions needed to open the way to Mother Brain:

    - None: The way is already open from the start of the game.
    - Bosses: Defeat Kraid, Phantoon, Draygon, and Ridley.
    - Minibosses: Defeat Spore Spawn, Crocomire, Botwoon, and Golden Torizo.
    - Metroids: Defeat all the Metroids in the four Metroid rooms.
    - Chozos: Defeat Bomb Torizo and Golden Torizo, and activate Bowling Alley and Acid Chozo statues.
      Note that Phantoon must be defeated before the Bowling Alley statue can be activated.
    - Pirates: Defeat the enemies in Pit Room, Baby Kraid Room, Plasma Room, and Metal Pirates Room.
      Note that Morph and Missiles must be collected before the enemies spawn in Pit Room.

    In every case, the way to beat the game is to escape after defeating Mother Brain. Objective rooms are marked with X's on the map.
    """
    display_name = "Objective"
    option_None = 0
    option_Bosses = 1
    option_Minibosses = 2
    option_Metroids = 3
    option_Chozos = 4
    option_Pirates = 5
    default = 1

class DoorsMode(Choice):
    """
    This setting determines the types of non-gray doors that exist in the game:

    - Blue: All doors are blue, except for gray doors.
    - Ammo: Red, green, and yellow doors are randomly mixed in.

    Gray doors are unaffected by this setting and always exist in the same set of rooms: boss/miniboss 
    rooms and the four Pirates rooms (Pit Room, Baby Kraid Room, Plasma Room, and Metal Pirates Room).

    For ammo doors, both sides of the door will have the same color and share a lock, so that unlocking
    one side of the door also unlocks the other.
    """
    display_name = "Doors"
    option_Blue = 0
    option_Ammo = 1
    default = 0


class AreaAssignment(Choice):
    """
    Each map is partitioned into six connected regions, which are assigned to in-game areas in different ways depending on this setting:

    - Standard: Landing Site is always in Crateria. The other areas are assigned based on their size (in number of map tiles), 
                in order from largest to smallest: Norfair, Brinstar, Maridia, Tourian, Wrecked Ship.
    - Randomized: The areas are assigned randomly. In particular, Landing Site can be in any area.
    """
    display_name = "Area Assignment"
    option_Standard = 0
    option_Randomized = 1
    default = 0

class SupersDouble(Toggle):
    """
    If enabled, Supers will deal double damage to Mother Brain, applying to all three phases of the fight.
    Given that the randomizer does not change the ammo distribution (there are only 50 Supers in the game),
    this option reduces the need for a long "ammo hunt" before fighting Mother Brain if the player has not found Charge Beam.
    This option can be set independently of the "Mother Brain fight" setting, though in case of a "Short" Mother Brain fight,
    its practical effect is minimal.
    """
    display_name = "Supers double"

class MotherBrain(Choice):
    """
    This option affects the length of the Mother Brain fight, affecting only phases 2 and 3:

    - Vanilla: The fight behaves as in the vanilla game. Some cutscenes are accelerated, but only in ways that 
    should not interfere with how the player executes the fight (including the stand-up glitch).
    - Short: The fight ends immediately after Mother Brain finishes the first Rainbow Beam attack.
    - Skip: The fight is skipped entirely.

    With the "Short" and "Skip" options, Samus will not get an energy refill before the escape, as the cutscene is 
    skipped where the refill would normally happen. However, Samus will always collect Hyper Beam.
    """
    display_name = "Mother brain short"
    option_Vanilla = 0
    option_Short = 1
    option_Skip = 2
    default = 1

class EscapeEnemiesCleared(Toggle):
    """
    If this option is enabled, enemies do not spawn during the escape.

    If this option is disabled, in many rooms enemies will cause heavy lag and visual glitches during the escape 
    (much of which is vanilla game behavior but not normally observable in casual play).

    Note that regardless of whether or not this option is enabled, currently the randomizer opens up major 
    barriers during the escape (though a future version of the randomizer might make these behaviors become 
    part of the same option):

    - All bosses/minibosses are cleared.
    - Shaktool Room is cleared.
    - Acid Chozo Statue acid is drained.
    - Maridia Tube is broken.
    """
    display_name = "Escape enemies cleared"

class EscapeRefill(Toggle):
    """
    If this option is enabled, then Samus' energy is refilled at the beginning of the escape sequence. 
    This is mainly effective in combination with the "Short" Mother Brain option (which is the default),
    to compensate for not being refilled by the Baby Metroid.

    If this option is disabled, it is possible that the escape may require having collected Reserve Tanks 
    and/or manipulating Mother Brain to end the fight with more energy (up to 340, by damaging down correctly 
    and disabling suits).
    """
    display_name = "Refill energy for escape"

class EscapeMovementItems(Toggle):
    """
    If enabled, Samus will collect and equip all movement items when acquiring Hyper Beam:

    - Varia Suit
    - Gravity Suit
    - Morph Ball
    - Bombs
    - Spring Ball
    - Screw Attack
    - Hi-Jump Boots
    - Space Jump
    - Speed Booster
    - Grapple
    - X-Ray

    The escape timer is based on an assumption that the player has all these items available. By granting them
    with Hyper Beam, it avoids the possibility of the player needing to hunt for movement items in order to 
    complete the escape fast enough.

    Note: Regardless of this setting, in this randomizer Hyper Beam always breaks bomb blocks, Super blocks,
    and Power Bomb blocks and can open blue/green gates from either side.
    """
    display_name = "Escape movement items"

class MarkMapStations(Toggle):
    """
    If enabled, the map station for the current area will always be visible as a special tile on the map even before
    you have reached it. This affects both the pause menu map and the HUD mini-map.
    """
    display_name = "Mark map stations"

class RoomOutlineRevealed(Toggle):
    """
    If enabled, entering a room causes the outline of the room to be revealed in the pause map. Tiles which have 
    only been revealed in this way are shown in the pause map with a black interior. Room details such as item dots 
    or door locks are not shown. This feature is limited to the pause map and has no effect on the HUD mini-map.

    This option can make it easier for players to remember the rooms they have visited and to see how they connect.
    """
    display_name = "Room outline revealed on entry"

class TransitionLetters(Toggle):
    """
    This option affects how transitions between areas are marked on the map:

    - Off: An arrow is used, showing the direction of the transition.
    - On: A letter is used, the first letter of the name of the neighboring area.

    In both cases, transitions markers (arrows or letters) are colored according to the neighboring area's color.
    """
    display_name = "Area transition markers on map"

class ItemMarkers(Choice):
    """
    This option affects the way that items are drawn on the map (pause menu map and HUD minimap). There are four choices:

    - Basic: All items are marked on the map with small dots.
    - Majors: Foreign progression items, Unique items, E-Tanks, and Reserve Tanks are marked with large solid dots; other items are marked with small dots.
    - Uniques: Foreign progression items and Unique items are marked with large solid dots; other items are marked with small dots.
    - 3Tiered: Foreign progression items and Unique items are marked with large solid dots; Foreign non-progression items, Supers, Power Bombs, E-Tanks, and Reserve
      Tanks are marked with large hollow dots; Missiles are marked with small dots.
    """
    display_name = "Item markers"
    option_Basic = 0
    option_Majors = 1
    option_Uniques = 2
    option_3Tiered = 3

class ItemDotsDisappear(Toggle):
    """
    If enabled, this option makes item dots disappear on the map after item collection:
    """
    display_name = "Item dots after collection"

class AllItemsSpawn(Toggle):
    """
    In the vanilla game, some items do not spawn until certain conditions are fulfilled:

    - Items in Wrecked Ship rooms (with the exception of the one item in Wrecked Ship Main Shaft) do not
      spawn until after Phantoon is defeated, when the rooms change to appearing "powered on".
    - The item in the left side of Morph Ball Room and in The Final Missile do not spawn until the planet is 
      awakened.
    - The item in Pit Room does not spawn until entering with Morph and Missiles collected.

    These conditions are apparently unintended artifacts of how the game was coded and are not normally 
    observable during casual play of the vanilla game. However, they can frequently be observed in the 
    randomizer, which can be counter-intuitive for players. When this quality-of-life option is enabled, these 
    items will spawn from the beginning of the game instead of requiring those conditions.
    """
    display_name = "All items spawn"

class BuffedDrops(Toggle):
    """
    If enabled, then certain enemy drops are improved:

    - Small energy drops give 10 energy.
    - Respawning enemies drop Power Bombs at double the normal rate.
    """
    display_name = "Enemy drops are buffed"

class AcidChozo(Toggle):
    """
    In the vanilla game, the statue in Acid Chozo Statue Room will not activate (to lower the acid) 
    unless Space Jump has been collected. This option removes this requirement, allowing the statue
    to be activated without Space Jump.
    """
    display_name = "Acid Chozo usable without Space Jump"


class FastElevators(Toggle):
    """
    If enabled, Samus moves up and down elevators at a faster speed.

    This also has an effect of reducing the total heat damage taken while on elevators. For example, it
    makes it more likely to be able to survive an unexpected trip down the Lower Norfair Main Hall elevator, which takes
    47 energy in each direction with this option enabled, compared to 109 energy with it disabled.
    """
    display_name = "Fast elevators"
    
class FastDoors(Toggle):
    """
    If enabled, this doubles the speed of aligning the camera and scrolling through the door. It does not affect
    the speed at which the game fades out to black or fades back in, so it should not disrupt the execution of 
    strats across rooms.
    """
    display_name = "Fast doors"

class FastPauseMenu(Toggle):
    """
    If enabled, this increases the speed and responsiveness of pause menu navigation:

    - It is no longer needed to hold L, R, or Start for 4 frames for these inputs to have their effect.
    - The fade-in and fade-out of the pause menu is faster.
    - Fade-in and fade-out are faster when switching between map and equipment screens with L & R.
    - Fade-in and fade-out are faster when switching between maps with Select.
    - Diagonal scrolling is enabled on the map screen.
    Changes are avoided that could meaningfully affect pause buffering strats or game behavior:

    - Fade-out of gameplay while pausing is unaffected.
    - Fade-in of gameplay while unpausing is unaffected.
    """
    display_name = "Fast pause menu"

class Respin(Toggle):
    """
    If enabled, you can press jump to make Samus spin while mid-air. For example, this can be used 
    after having broken spin, or when falling or jumping without spin.

    Note: The randomizer logic does not take this setting into account. Therefore, even when it is enabled,
    the game will not require it to be used, and it may create sequence break opportunities.
    """
    display_name = "Respin"

class InfiniteSpaceJump(Toggle):
    """
    If enabled, Space Jump behaves in air the same as it does underwater, making it easier to use by widening 
    the window of time to press jump.

    Note: The randomizer logic does not take this setting into account. Therefore, even when it is enabled, 
    the game will not require it to be used, and it may create sequence break opportunities.
    """
    display_name = "Lenient Space Jump"

class Walljump(Choice):
    """
    This affects how the wall jump ability works in the game.

    - Vanilla: Wall jumping behaves like in the vanilla game.
    - Collectible: A special new "WallJump" item is added to the game (replacing one "Missile" pack), 
                    and wall jumping is only possible after collecting this item.

    This setting is taken into account in the logic. Selections other than "Vanilla" may significantly increase 
    the difficulty of the game, by requiring the player to know how to perform many tricks to avoid wall jumping 
    (using frozen enemies, Speed Booster, Bombs, etc.), depending on the Skill Assumption settings.

    Regardless of this setting, it is always possible to get a wall-jump check (the pose that Samus makes when 
    moving away from a nearby wall), even if pressing jump during the check will not trigger a wall jump.
    """
    display_name = "Wall jumps"
    option_Vanilla = 0
    option_Collectible = 1
    default = 0

class ETankRefill(Choice):
    """
    This option affects the refill that E-Tanks give when collected:

    - Disabled: E-Tanks do not provide an energy refill.
    - Vanilla: E-Tanks behave as in the vanilla game, refilling regular energy but not reserve energy.
    - Full: E-Tanks also refill reserves, on top of regular energy.
    """
    display_name = "E-Tank refill"
    option_Disabled = 0
    option_Vanilla = 1
    option_Full = 2
    default = 1

class MomentumConservation(Toggle):
    """
    If enabled, Samus' horizontal momentum is conserved when landing from a spin jump while holding run and forward.

    Note: The randomizer logic does not take this setting into account. Therefore, even when it is enabled, 
    the game will not require it to be used, and it may create sequence break opportunities.
    """
    display_name = "Momentum conservation"

class MapsRevealed(Choice):
    """
    This setting affects to what extent the map is already revealed when starting the game:

    - Hidden: Maps are not initially revealed. Map stations must be activated in order to reveal the maps.
    - Partial: Room outlines and area transitions are shown. Details such as item dots or door locks are 
                not shown. Activating map stations will reveal those details.
    - Revealed: Maps are revealed, as though all the map stations were already activated.
    """
    display_name = "Maps revealed from start"
    option_Hidden = 0
    option_Partial = 1
    option_Revealed = 2

class MapLayout(Choice):
    """
    This setting affects how the rooms are arranged on the map:

        - Vanilla: The rooms are arranged as they are in the vanilla game, i.e. there is no map randomization.
        - Tame: The rooms are arranged in a random but relatively friendly way: one-ways tend to have short return paths that loop back around.
        - Wild: The rooms are arranged in a more random and less friendly way: there will often be one-ways with only long return paths.
    """
    display_name = "Map Layout"
    option_Vanilla = 0
    option_Tame = 1
    option_Wild = 2

class EnergyFreeShinesparks(Toggle):
    """
    If enabled, then shinesparks neither require nor consume energy.

    This setting is taken into account in the logic.
    """
    display_name = "Energy-free shinesparks"

class EtankColorRed(Range):
    """
    Use this to make Energy Tanks appear with a different color in the HUD.

    This option has minor side effects on the colors of certain items.
    """
    display_name = "Etank red intensity"
    range_start = 0
    range_end = 255
    default = 222

class EtankColorGreen(Range):
    """
    Use this to make Energy Tanks appear with a different color in the HUD.

    This option has minor side effects on the colors of certain items.
    """
    display_name = "Etank green intensity"
    range_start = 0
    range_end = 255
    default = 56

class EtankColorBlue(Range):
    """
    Use this to make Energy Tanks appear with a different color in the HUD.

    This option has minor side effects on the colors of certain items.
    """
    display_name = "Etank blue intensity"
    range_start = 0
    range_end = 255
    default = 148

class ReserveHudStyle(Choice):
    """
    The setting affects how reserve tanks are displayed on the HUD.
    - Vanilla: A reserve tank indicator is shown on the HUD only if reserve mode is AUTO, and its color indicates whether reserves have any energy or not.
    - Revamped: Each reserve tank is indicated with a bar showing how full it is. If reserve mode is AUTO, then the AUTO text also appears, 
                and its color indicates whether reserves have any energy or not.
    """
    display_name = "Reserve tank HUD style"
    option_Vanilla = 0
    option_Revamped = 1
    default = 0

class VanillaScrewAttackAnimation(Choice):
    """
    This setting determines how the Screw Attack animation appears:
    - Vanilla: The Screw Attack animation is always based on the Space Jump animation regardless of whether or not Space Jump is equipped.
    - Split: Screw Attack without Space Jump equipped is based on the spin-jump animation. Screw Attack with Space Jump equipped is based 
            on the Space Jump animation.
    """ 
    display_name = "Screw Attack animation"
    option_Vanilla = 0
    option_Split = 1
    default = 0

class PaletteTheme(Choice):
    """
    This setting controls the palettes for rooms (affecting foregrounds and backgrounds):
    - Vanilla: Rooms use the palette from the original game.
    - AreaThemed: Rooms use a palette based on the area in which they appear in the randomized map. This adds variety and can help the 
                    randomized areas to feel more coherent.
    """ 
    display_name = "Room palettes"
    option_Vanilla = 0
    option_AreaThemed = 1
    default = 0

class TileTheme(Choice):
    """
    If enabled, the rooms in the game will be retiled using the selected theme. This affects only the graphical appearance of the rooms.
    Note: This option is still under development and may contain bugs. If you notice any issues, please let us know on the Discord.
    """ 
    display_name = "Tile theme"
    option_None = 0
    option_Scrambled = 1
    option_Outer_Crateria = 2
    option_Inner_Crateria = 3
    option_Green_Brinstar = 4
    option_Upper_Norfair = 5
    option_Wrecked_Ship = 6
    option_West_Maridia = 7
    default = 0

class Music(Choice):
    """
    This setting determines which music plays in each room:
    - Vanilla: The same music plays as would in the vanilla game for the given room. On a randomized map this implies that music 
                will change across most door transitions, which increases the room load times.
    - AreaThemed: The music is based on the area that the room belongs to on the randomized map, which can help the areas to feel more coherent.
    - Disabled: Music is disabled, though sound effects still play.
    """ 
    display_name = "Music"
    option_Vanilla = 0
    option_AreaThemed = 1
    option_Disabled = 2
    default = 0

class DisableBeeping(Choice):
    """
    This setting affects the low-energy beeping which alerts the player when Samus is at 30 energy or less.
    - Vanilla: The low-energy beeping behaves as in the vanilla game.
    - Disabled: The low-energy beeping is disabled.
    """ 
    display_name = "Low-energy beeping"
    option_Vanilla = 0
    option_Disabled = 1
    default = 0

class Shaking(Choice):
    """
    This setting affects the graphical appearance of screen shaking, e.g., during the escape sequence, bosses, and in rooms where lava or acid rises.
    - Vanilla: Screen shaking happens as in the vanilla game (which has up to 3-pixel displacements).
    - Reduced: Screen shaking is capped to 1-pixel displacements.
    - Disabled: Screen shaking is disabled.
    """ 
    display_name = "Screen shaking"
    option_Vanilla = 0
    option_Reduced = 1
    option_Disabled = 2
    default = 0

class ControllerButton(Choice):
    option_Default = 0
    option_Left = 1
    option_Right = 2
    option_Up = 3
    option_Down = 4
    option_X = 5
    option_Y = 6
    option_A = 7
    option_B = 8
    option_L = 9
    option_R = 10
    option_Select = 11
    option_Start = 12

class Shot(ControllerButton):
    display_name = "Shot button"
    default = 5

class Jump(ControllerButton):
    display_name = "Jump button"
    default = 7

class Dash(ControllerButton):
    display_name = "Dash button"
    default = 8

class ItemSelect(ControllerButton):
    display_name = "ItemSelect button"
    default = 11

class ItemCancel(ControllerButton):
    display_name = "ItemCancel button"
    default = 6

class AngleUp(ControllerButton):
    display_name = "AngleUp button"
    default = 10

class AngleDown(ControllerButton):
    display_name = "AngleDown button"
    default = 9

class SpinLockButtons(OptionSet):
    """
    Press the combination simultaneously to activate Spin Lock, temporarily preventing up/down inputs from breaking spin. Pressing shot will cancel this mode.
    """
    display_name = "SpinLock button combination"
    default = {"L", "R", "Up", "X"}
    valid_keys = {"X", "Y", "A", "B", "L", "R", "Select", "Start", "Up","Down", "Left", "Right"}

class QuickReloadButtons(OptionSet):
    """
    Press the combination simultaneously to quick reload from the last save. Repeat to cycle through previous saves.
    """
    display_name = "QuickReload button combination"
    default = {"L", "R", "Select", "Start"}
    valid_keys = {"X", "Y", "A", "B", "L", "R", "Select", "Start", "Up","Down", "Left", "Right"}

class Moonwalk(Toggle):
    display_name = "Moonwalk"
    default = 0

@dataclass
class SMMROptions(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    remote_items: RemoteItems
    death_link: DeathLink
    preset: Preset
    techs: Techs
    strats: Strats
    item_pool: ItemPool
    custom_item_pool: CustomItemPool
    shinespark_tiles: ShinesparkTiles
    heated_shinespark_tiles: HeatedShinesparkTiles
    shinecharge_leniency_frames: ShinechargeLeniencyFrames
    resource_multiplier: ResourceMultiplier
    gate_glitch_leniency: GateGlitchLeniency
    door_stuck_leniency: DoorStuckLeniency
    escape_timer_multiplier: EscapeTimerMultiplier
    start_location_mode: StartLocationMode
    phantoon_proficiency: PhantoonProficiency
    draygon_proficiency: DraygonProficiency
    ridley_proficiency: RidleyProficiency
    botwoon_proficiency: BotwoonProficiency
    mother_brain_proficiency: MotherBrainProficiency
    save_animals: SaveAnimals
    early_save: EarlySave
    ultra_low_qol: UltraLowQol
    quality_of_life: QualityOfLife
    objectives: Objectives
    doors_mode: DoorsMode
    area_assignment: AreaAssignment
    #"filler_items": String
    supers_double: SupersDouble
    mother_brain: MotherBrain
    escape_enemies_cleared: EscapeEnemiesCleared
    escape_refill: EscapeRefill
    escape_movement_items: EscapeMovementItems
    mark_map_stations: MarkMapStations
    room_outline_revealed: RoomOutlineRevealed
    transition_letters: TransitionLetters
    item_markers: ItemMarkers
    item_dots_disappear: ItemDotsDisappear
    all_items_spawn: AllItemsSpawn
    buffed_drops: BuffedDrops
    acid_chozo: AcidChozo
    fast_elevators: FastElevators
    fast_doors: FastDoors
    fast_pause_menu: FastPauseMenu
    respin: Respin
    infinite_space_jump: InfiniteSpaceJump
    momentum_conservation: MomentumConservation
    wall_jump: Walljump
    etank_refill: ETankRefill
    maps_revealed: MapsRevealed
    map_layout: MapLayout
    energy_free_shinesparks: EnergyFreeShinesparks
    etank_color_red: EtankColorRed
    etank_color_green: EtankColorGreen
    etank_color_blue: EtankColorBlue
    reserve_hud_style: ReserveHudStyle
    vanilla_screw_attack_animation: VanillaScrewAttackAnimation
    palette_theme: PaletteTheme
    tile_theme: TileTheme
    music: Music
    disable_beeping: DisableBeeping
    shaking: Shaking
    shot: Shot
    jump: Jump
    dash: Dash
    item_select: ItemSelect
    item_cancel: ItemCancel
    angle_up: AngleUp
    angle_down: AngleDown
    spin_lock_buttons: SpinLockButtons
    quick_reload_buttons: QuickReloadButtons
    moonwalk: Moonwalk