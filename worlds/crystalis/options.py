from dataclasses import dataclass
from Options import Choice, Toggle, PerGameCommonOptions, DeathLink, DeathLinkMixin, OptionGroup, StartInventoryPool, \
    Visibility, PlandoConnections
from .regions import entrances_data, GBC_CAVE_NAMES, SHUFFLE_GROUPING
from .types import CrystalisEntranceTypeEnum

# World Options
class RandomizeMaps(Toggle):
    """NOT IMPLEMENTED YET: Individual maps are randomized. For now this is only a subset of possible maps. A randomized
    map will have all the same features (exits, chests, NPCs, etc) except things are moved around.
    """
    display_name = "Randomize maps (Wm)"
    visibility = Visibility.none

    def flag_name(self) -> (str, str):
        if self:
            return "W", "m"
        return "", ""


class ShuffleAreas(Toggle):
    """Shuffles some or all area connections."""
    display_name = "Shuffle areas (Wa)"
    visibility = Visibility.none

    def flag_name(self) -> (str, str):
        if self:
            return "W", "a"
        return "", ""


class ShuffleHouseEntrances(Toggle):
    """Shuffles all the house entrances, as well as a handful of other things, like the
    palace/fortress-type entrances at the top of several towns, and standalone houses.
    """
    display_name = "Shuffle house entrances (Wh)"
    visibility = Visibility.none

    def flag_name(self) -> (str, str):
        if self:
            return "W", "h"
        return "", ""


class RandomizeTradeInItems(Toggle):
    """Items expected by various NPCs will be shuffled: specifically, Statue of Onyx, Kirisa Plant, Love Pendant, Ivory
    Statue, and Fog Lamp. Rage will expect a random sword, and Tornel will expect a random bracelet.
    """
    display_name = "Randomize trade-in items (Wt)"


    def flag_name(self) -> (str, str):
        if self:
            return "W", "t"
        return "", ""


class UnidentifiedKeyItems(Toggle):
    """Item names will be generic and effects will be shuffled. This includes keys, flutes, lamps, and statues."""
    display_name = "Unidentified key items (Wu)"


    def flag_name(self) -> (str, str):
        if self:
            return "W", "u"
        return "", ""


class RandomizeWallElements(Toggle):
    """Walls will require a randomized element to break. Normal rock and ice walls will indicate the required element by
    the color (light grey or yellow for wind, blue for fire, bright orange ("embers") for water, or dark grey ("steel")
    for thunder. The element to break these walls is the same throughout an area. Iron walls require a one-off random
    element, with no visual cue, and two walls in the same area may have different requirements.
    """
    display_name = "Randomize elements to break walls (We)"


    def flag_name(self) -> (str, str):
        if self:
            return "W", "e"
        return "", ""


class ShuffleGoa(Toggle):
    """The four areas of Goa fortress will appear in a random order."""
    display_name = "Shuffle Goa fortress floors (Wg)"


    def flag_name(self) -> (str, str):
        if self:
            return "W", "g"
        return "", ""


class RandomizeSpriteColors(Toggle):
    """Monsters and NPCs will have different colors."""
    display_name = "Randomize sprite colors (Ws)"


    def flag_name(self) -> (str, str):
        if self:
            return "W", "s"
        return "", ""


class RandomizeWildWarp(Toggle):
    """Wild warp will go to Mezame Shrine and 15 other random locations. These locations will be considered in-logic."""
    display_name = "Randomize wild warp (Ww)"


    def flag_name(self) -> (str, str):
        if self:
            return "W", "w"
        return "", ""


# Routing Options
class StoryMode(Toggle):
    """Draygon 2 won't spawn unless you have all four swords and have defeated all major bosses of the tetrarchy."""
    display_name = "Story Mode (Rs)"


    def flag_name(self) -> (str, str):
        if self:
            return "R", "s"
        return "", ""

class NoBowMode(Toggle):
    """No items are required to finish the game. An exit is added from Mezame shrine directly to the Draygon 2 fight
    (and the normal entrance is removed). Draygon 2 spawns automatically with no Bow of Truth.
    """
    display_name = "No Bow mode (Rb)"


    def flag_name(self) -> (str, str):
        if self:
            return "R", "b"
        return "", ""


class OrbsNotRequired(Toggle):
    """If true, walls can be broken and bridges formed with level 1 shots."""
    display_name = "Orbs not required to break walls (Ro)"


    def flag_name(self) -> (str, str):
        if self:
            return "R", "o"
        return "", ""


class ThunderWarp(Choice):
    """Determines where the player is warped to when receiving the Sword of Thunder.
    Shuffled: The Sword of Thunder will warp you to a random town.
    None: The Sword of Thunder won't warp you. (Rt)
    Vanilla: The Sword of Thunder will warp you to Shyron. (R!t)
    """
    display_name = "Sword of Thunder warp"
    option_shuffled = 0
    option_none = 1
    option_vanilla = 2


    def flag_name(self) -> (str, str):
        if self == self.option_none:
            return "R", "t"
        elif self == self.option_vanilla:
            return "R", "!t"
        return "", ""


class VanillaDolphin(Toggle):
    """By default, the randomizer changes a number of dolphin and boat interactions: (1) healing the dolphin and having
    the Shell Flute is no longer required before the fisherman spawns: instead, he will spawn as soon as you have the
    item he wants; (2) talking to Kensu in the beach cabin is no longer required for the Shell Flute to work: instead,
    the Shell Flute will always work, and Kensu will spawn after the Fog Lamp is turned in and will give a key item
    check. This flag restores the vanilla interaction where healing and shell flute are required, and Kensu no longer
    drops an item.
    """
    display_name = "Vanilla Dolphin interactions (Rd)"


    def flag_name(self) -> (str, str):
        if self:
            return "R", "d"
        return "", ""


# Glitch Options
class FakeFlight(Choice):
    """Fake flight allows using Dolphin and Rabbit Boots to fly up the waterfalls in the Angry Sea (without calming the
    whirlpools). This is done by swimming up to a diagonal beach and jumping in a different direction immediately before
     disembarking.  Note: Fake flight cannot be disabled. The available options are in_logic or out_of_logic.
     """
    display_name = "Fake flight (Gf)"
    option_out_of_logic = 0
    option_in_logic = 1


    def flag_name(self) -> (str, str):
        if self:
            return "G", "f"
        return "", ""


class StatueGlitch(Choice):
    """Statue glitch allows getting behind statues that block certain entrances: the guards in Portoa, Amazones, Oak,
    Goa, and Shyron, as well as the statues in the Waterfall Cave. It is done by approaching the statue from the top
    right and holding down and left on the controller while mashing B.
    """
    display_name = "Statue glitch (Gs)"
    option_disabled = 0
    option_out_of_logic = 1
    option_in_logic = 2


    def flag_name(self) -> (str, str):
        if self == self.option_in_logic:
            return "G", "s"
        elif self == self.option_out_of_logic:
            return "G", "!s"
        return "", ""


class MtSabreSkip(Choice):
    """Entering Mt Sabre North normally requires (1) having Teleport, and (2) talking to the rabbit in Leaf after the
    abduction (via Telepathy). Both of these requirements can be skipped: first by flying over the river in Cordel plain
    rather than crossing the bridge, and then by threading the needle between the hitboxes in Mt Sabre North.
    """
    display_name = "Mt Sabre requirements skip (Gn)"
    option_disabled = 0
    option_out_of_logic = 1
    option_in_logic = 2


    def flag_name(self) -> (str, str):
        if self == self.option_in_logic:
            return "G", "n"
        elif self == self.option_out_of_logic:
            return "G", "!n"
        return "", ""


class StatueGauntletSkip(Choice):
    """The shooting statues in front of Goa and Stxy normally require Barrier to pass safely. With this flag, Flight can
    also be used by flying around the edge of the statue.
    """
    display_name = "Statue gauntlet skip (Gg)"
    option_disabled = 0
    option_out_of_logic = 1
    option_in_logic = 2


    def flag_name(self) -> (str, str):
        if self == self.option_in_logic:
            return "G", "g"
        elif self == self.option_out_of_logic:
            return "G", "!g"
        return "", ""


class SwordChargeGlitch(Choice):
    """Sword charge glitch allows charging one sword to the level of another sword by equipping the higher-level sword,
    re-entering the menu, changing to the lower-level sword without exiting the menu, creating a hard save, resetting,
    and then continuing.
    """
    display_name = "Sword charge glitch (Gc)"
    option_disabled = 0
    option_out_of_logic = 1
    option_in_logic = 2


    def flag_name(self) -> (str, str):
        if self == self.option_in_logic:
            return "G", "c"
        elif self == self.option_out_of_logic:
            return "G", "!c"
        return "", ""


class TriggerSkip(Choice):
    """A wide variety of triggers and exit squares can be skipped by using an invalid item every frame while walking.
    This allows bypassing both Mt Sabre North entrance triggers, the Evil Spirit Island entrance trigger, triggers for
    guards to move, slopes, damage tiles, and seamless map transitions.
    """
    display_name = "Trigger skip (Gt)"
    option_disabled = 0
    option_out_of_logic = 1
    option_in_logic = 2


    def flag_name(self) -> (str, str):
        if self == self.option_in_logic:
            return "G", "t"
        elif self == self.option_out_of_logic:
            return "G", "!t"
        return "", ""


class RageSkip(Choice):
    """Rage can be skipped by damage-boosting diagonally into the Lime Tree Lake screen. This provides access to the
    area beyond the lake if flight or bridges are available. For simplicity, the logic only assumes this is possible if
    there's a flyer.
    """
    display_name = "Rage skip (Gr)"
    option_disabled = 0
    option_out_of_logic = 1
    option_in_logic = 2


    def flag_name(self) -> (str, str):
        if self == self.option_in_logic:
            return "G", "r"
        elif self == self.option_out_of_logic:
            return "G", "!r"
        return "", ""


# Aesthetic Options
class RandomizeBackgroundMusic(Choice):
    """Randomizes or disables the background music."""
    display_name = "Randomize background music (Am/As)"
    option_vanilla = 0
    option_shuffle = 1
    option_disable = 2


    def flag_name(self) -> (str, str):
        if self == self.option_shuffle:
            return "A", "!m"
        elif self == self.option_disable:
            return "A", "s"
        return "", ""

class RandomizeMapColors(Toggle):
    """Randomizes the palettes of the background tiles."""
    display_name = "Randomize map colors (Ac)"


    def flag_name(self) -> (str, str):
        if self:
            return "A", "c"
        return "", ""


# Monster Options
class RandomizeMonsterWeaknesses(Toggle):
    """Monster and boss elemental weaknesses are shuffled."""
    display_name = "Randomize monster weaknesses (Me)"


    def flag_name(self) -> (str, str):
        if self:
            return "M", "e"
        return "", ""


class OopsAllMimics(Toggle):
    """Every chest is now a mimic, and killing the mimic will drop the real item chest. Careful when killing the mimic,
    if it drops the chest out of reach you'll need to reset the room!
    """
    display_name = "Replace all chests with mimics (Mg)"


    def flag_name(self) -> (str, str):
        if self:
            return "M", "g"
        return "", ""


class ShuffleTowerRobots(Toggle):
    """Tower robots will be shuffled into the normal pool."""
    display_name = "Shuffle tower robots (Mt)"


    def flag_name(self) -> (str, str):
        if self:
            return "M", "t"
        return "", ""


# Easy Mode Options
class DontShuffleMimics(Toggle):
    """Mimics will be in their vanilla locations."""
    display_name = "Don't shuffle mimics (Et)"


    def flag_name(self) -> (str, str):
        if self:
            return "E", "t"
        return "", ""


class KeepUniqueItemsAndConsumablesSeparate(Toggle):
    """Normally all items and mimics are shuffled into a single pool and distributed from there. If this flag is set,
    unique items (specifically, anything that cannot be sold) will only be found in either (a) checks that held unique
    items in vanilla, or (b) boss drops. Chests containing consumables in vanilla may be safely ignored, but chests
    containing unique items in vanilla may still end up with non-unique items because of bosses like Vampire 2 that drop
    consumables. If mimics are shuffled, they will only be in consumable locations. These locations are tracked by the
    multiworld, so they will still count against your hint points, but they will only contain your non-unique items.
    """
    display_name = "Keep unique items and consumables separate (Eu)"


    def flag_name(self) -> (str, str):
        if self:
            return "E", "u"
        return "", ""


class DecreaseEnemyDamage(Toggle):
    """Enemy attack power will be significantly decreased in the early game (by a factor of 3). The gap will narrow in
    the mid-game and eventually phase out at scaling level 40.
    """
    display_name = "Decrease enemy damage (Ed)"


    def flag_name(self) -> (str, str):
        if self:
            return "E", "d"
        return "", ""


class GuaranteeStartingSword(Toggle):
    """The Leaf elder is guaranteed to give a sword. It will not be required to deal with any enemies before finding the
    first sword.
    """
    display_name = "Guarantee starting sword (Es)"


    def flag_name(self) -> (str, str):
        if self:
            return "E", "s"
        return "", ""


class GuaranteeRefresh(Toggle):
    """Guarantees the Refresh spell will be available before fighting Tetrarchs."""
    display_name = "Guarantee refresh (Er)"


    def flag_name(self) -> (str, str):
        if self:
            return "E", "r"
        return "", ""


class ExperienceScalesFaster(Toggle):
    """Less grinding will be required to "keep up" with the game difficulty."""
    display_name = "Experience scales faster (Ex)"


    def flag_name(self) -> (str, str):
        if self:
            return "E", "x"
        return "", ""


class NoCommunityJokes(Toggle):
    """Skip community jokes, such as funny/misspelled item, monster, or character names. This will make it easier to
    look up information in guides/FAQs if necessary.
    """
    display_name = "No community jokes (Ec)"


    def flag_name(self) -> (str, str):
        if self:
            return "E", "c"
        return "", ""


# No Guarantees Options
class BattleMagicNotGuaranteed(Toggle):
    """Normally, the logic will guarantee that level 3 sword charges are available before fighting the tetrarchs (with
    the exception of Karmine, who only requires level 2). This disables that check.
    """
    display_name = "Battle magic not guaranteed (Nw)"


    def flag_name(self) -> (str, str):
        if self:
            return "N", "w"
        return "", ""


class TinkMode(Toggle):
    """Enables "tink strats", where wrong-element swords will still do a single damage per hit. Player may be required
    to fight monsters (including bosses) with tinks.
    """
    display_name = "Matching sword not guaranteed (\"Tink Mode\") (Ns)"


    def flag_name(self) -> (str, str):
        if self:
            return "N", "s"
        return "", ""


class BarrierNotGuaranteed(Toggle):
    """Normally, the logic will guarantee Barrier before entering Stxy, the Fortress, or fighting Karmine. This puts
    those locations in logic with any sword (to farm money) and one of Shield Ring, Refresh, or a place to buy Medical
    Herbs.
    """
    display_name = "Barrier not guaranteed (Nb)"


    def flag_name(self) -> (str, str):
        if self:
            return "N", "b"
        return "", ""


class GasMaskNotGuaranteed(Toggle):
    """The logic will not guarantee gas mask before needing to enter the swamp, nor will leather boots (or hazmat suit)
    be guaranteed to cross long stretches of spikes. Gas mask is still guaranteed to kill the insect.
    """
    display_name = "Gas mask not guaranteed (Ng)"


    def flag_name(self) -> (str, str):
        if self:
            return "N", "g"
        return "", ""


# Hard Mode Options
class DontBuffConsumables(Toggle):
    """If this is set to true, Medical Herb is not buffed to heal 80 damage, which is helpful to make up for cases where
    Refresh is unavailable early. Fruit of Power is not buffed to restore 56 MP.
    """
    display_name = "Don't buff medical herb or fruit of power (Hm)"


    def flag_name(self) -> (str, str):
        if self:
            return "H", "m"
        return "", ""


class MaxScalingInTower(Toggle):
    """Enemies in the tower spawn at max scaling level."""
    display_name = "Max scaling level in tower (Ht)"


    def flag_name(self) -> (str, str):
        if self:
            return "H", "t"
        return "", ""


class ExperienceScalesSlower(Toggle):
    """More grinding will be required to "keep up" with the difficulty."""
    display_name = "Experience scales slower (Hx)"


    def flag_name(self) -> (str, str):
        if self:
            return "H", "x"
        return "", ""


class ChargeShotsOnly(Toggle):
    """Stabbing is completely ineffective. Only charged shots work."""
    display_name = "Charge shots only (Hc)"


    def flag_name(self) -> (str, str):
        if self:
            return "H", "c"
        return "", ""


class Blackout(Toggle):
    """All caves and fortresses are permanently dark."""
    display_name = "Blackout (Hz)"


    def flag_name(self) -> (str, str):
        if self:
            return "H", "z"
        return "", ""


class Permadeath(Toggle):
    """Hardcore mode: checkpoints and saves are removed."""
    display_name = "Permadeath (Hh)"


    def flag_name(self) -> (str, str):
        if self:
            return "H", "h"
        return "", ""


# Vanilla Options
class DontBuffDyna(Toggle):
    """By default, we make the Dyna fight a bit more of a challenge. Side pods will fire significantly more. The safe
    spot has been removed. The revenge beams pass through barrier. Side pods can now be killed. This flag prevents that
    change.
    """
    display_name = "Don't buff Dyna (Vd)"


    def flag_name(self) -> (str, str):
        if self:
            return "V", "d"
        return "", ""


class DontBuffBonusItems(Toggle):
    """Leather Boots are changed to Speed Boots, which increase player walking speed (this allows climbing up the slope
    to access the Tornado Bracelet chest, which is taken into consideration by the logic). Deo's pendant restores MP
    while moving. Rabbit boots enable sword charging up to level 2 while walking (level 3 still requires being
    stationary, so as to prevent wasting tons of magic). Turning this on removes all these changes.
    """
    display_name = "Don't buff bonus items (Vb)"


    def flag_name(self) -> (str, str):
        if self:
            return "V", "b"
        return "", ""


class VanillaMaps(Choice):
    """Normally the randomizer adds a new "East Cave" to Valley of Wind, borrowed from the GBC version of the game. This
     cave contains two chests (one considered a key item) on the upper floor and exits to two random areas (chosen
     between Lime Tree Valley, Cordel Plain, Goa Valley, or Desert 2), one unblocked on the lower floor, and one down
     the stairs and behind a rock wall from the upper floor. This flag prevents adding that cave. If set as "Lime
     Passage" then a direct path will instead be added between Valley of Wind and Lime Tree Valley.
     """
    display_name = "Vanilla maps (Vm)"
    option_GBC_cave = 0
    option_lime_passage = 1
    option_vanilla = 2

    @classmethod
    def get_option_name(cls, value: int) -> str:
        if value == 0:
            return "GBC Cave"
        return super().get_option_name(value)


    def flag_name(self) -> (str, str):
        if self == self.option_lime_passage:
            return "V", "!m"
        elif self == self.option_vanilla:
            return "V", "m"
        return "", ""

class VanillaShops(Toggle):
    """By default, we disable shop glitch, shuffle shop contents, and tie the prices to the scaling level (item shops
    and inns increase by a factor of 2 every 10 scaling levels, armor shops decrease by a factor of 2 every 12 scaling
    levels). This flag prevents all of these changes, restoring shops to be completely vanilla.
    """
    display_name = "Vanilla shops (Vs)"


    def flag_name(self) -> (str, str):
        if self:
            return "V", "s"
        return "", ""


class VanillaWildWarp(Choice):
    """By default, Wild Warp is nerfed to only return to Mezame Shrine. This flag restores it to work like normal. Note
    that this will put all wild warp locations in logic unless the flag is set as "Out Of Logic".
    """
    display_name = "Vanilla wild warp (Vw)"
    option_disabled = 0
    option_out_of_logic = 1
    option_vanilla = 2
    alias_enabled = option_vanilla


    def flag_name(self) -> (str, str):
        if self == self.option_out_of_logic:
            return "V", "!w"
        elif self == self.option_vanilla:
            return "V", "w"
        return "", ""


class VanillaHUD(Toggle):
    """By default, the blue status bar (HUD) at the bottom of the screen is reorganized a bit, including displaying
    enemies' names and HP. This disables those changes.
    """
    display_name = "Vanilla HUD (Vh)"


    def flag_name(self) -> (str, str):
        if self:
            return "V", "h"
        return "", ""


# Quality of Life Options
class DontAutoEquipUpgrades(Toggle):
    """Prevents adding a quality-of-life improvement to automatically equip the corresponding orb/bracelet whenever
    changing swords.
    """
    display_name = "Don't automatically equip orbs and bracelets (Qa)"


    def flag_name(self) -> (str, str):
        if self:
            return "Q", "a"
        return "", ""


class DisableControllerShortcuts(Toggle):
    """By default, we disable second controller input and instead enable some new shortcuts on controller 1: Start+A+B
    for wild warp, and Select+B to quickly change swords. To support this, the action of the start and select buttons is
    changed slightly. This flag disables this change and retains normal behavior.
    """
    display_name = "Disable controller shortcuts (Qc)"


    def flag_name(self) -> (str, str):
        if self:
            return "Q", "c"
        return "", ""


class AudibleWallCues(Toggle):
    """Provide an audible cue when failing to break a non-iron wall. The intended way to determine which sword is
    required for normal cave walls is by looking at the color. This causes the level 3 sword sound of the required
    element to play when the wall fails to break. Note that fortress walls (iron in vanilla) do not give this hint,
    since there is no visual cue for them, either.
    """
    display_name = "Audible wall cues (Qw)"


    def flag_name(self) -> (str, str):
        if self:
            return "Q", "w"
        return "", ""


class CrystalisPlandoConnections(PlandoConnections):
    """
    Generic connection plando. Format is:
    - entrance: "Entrance Name"
      exit: "Exit Name"
      percentage: 100
    Percentage is an integer from 0 to 100 which determines whether that connection will be made. Defaults to 100 if omitted.
    Note: direction is ignored and assumed to always be "both", as uncoupled ER is not supported for Crystalis.
    """
    entrances = {*(name for name, data in entrances_data.items() if "->" not in name and
                   data.entrance_type != CrystalisEntranceTypeEnum.GOA_TRANSITION)}
    exits = {*(name for name, data in entrances_data.items() if "->" not in name and
               data.entrance_type != CrystalisEntranceTypeEnum.GOA_TRANSITION)}

    @classmethod
    def can_connect(cls, entrance: str, exit: str) -> bool:
        return entrances_data[entrance].entrance_type in SHUFFLE_GROUPING[entrances_data[exit].entrance_type]


crystalis_option_groups = [
    OptionGroup('World Options', [
        RandomizeMaps,
        ShuffleAreas,
        ShuffleHouseEntrances,
        RandomizeTradeInItems,
        UnidentifiedKeyItems,
        RandomizeWallElements,
        ShuffleGoa,
        RandomizeSpriteColors,
        RandomizeWildWarp,
    ]),
    OptionGroup('Routing Options', [
        StoryMode,
        NoBowMode,
        OrbsNotRequired,
        ThunderWarp,
        VanillaDolphin,
    ]),
    OptionGroup('Glitch Options', [
        FakeFlight,
        StatueGlitch,
        MtSabreSkip,
        StatueGauntletSkip,
        SwordChargeGlitch,
        TriggerSkip,
        RageSkip,
    ]),
    OptionGroup('Aesthetic Options', [
        RandomizeBackgroundMusic,
        RandomizeMapColors,
    ]),
    OptionGroup('Monster Options', [
        RandomizeMonsterWeaknesses,
        OopsAllMimics,
        ShuffleTowerRobots,
    ]),
    OptionGroup('Easy Mode Options', [
        DontShuffleMimics,
        KeepUniqueItemsAndConsumablesSeparate,
        DecreaseEnemyDamage,
        GuaranteeStartingSword,
        GuaranteeRefresh,
        ExperienceScalesFaster,
        NoCommunityJokes,
    ]),
    OptionGroup('No Guarantees Options', [
        BattleMagicNotGuaranteed,
        TinkMode,
        BarrierNotGuaranteed,
        GasMaskNotGuaranteed,
    ]),
    OptionGroup('Hard Mode Options', [
        DontBuffConsumables,
        MaxScalingInTower,
        ExperienceScalesSlower,
        ChargeShotsOnly,
        Blackout,
        Permadeath,
        DeathLink,
    ]),
    OptionGroup('Vanilla Options', [
        DontBuffDyna,
        DontBuffBonusItems,
        VanillaMaps,
        VanillaShops,
        VanillaWildWarp,
        VanillaHUD,
    ]),
    OptionGroup('Quality of Life Options', [
        DontAutoEquipUpgrades,
        DisableControllerShortcuts,
        AudibleWallCues,
    ]),
    OptionGroup('Plando', [
        CrystalisPlandoConnections
    ])
]


@dataclass
class CrystalisOptions(PerGameCommonOptions, DeathLinkMixin):
    #World options
    randomize_maps: RandomizeMaps
    shuffle_areas: ShuffleAreas
    shuffle_houses: ShuffleHouseEntrances
    randomize_tradeins: RandomizeTradeInItems
    unidentified_key_items: UnidentifiedKeyItems
    randomize_wall_elements: RandomizeWallElements
    shuffle_goa: ShuffleGoa
    randomize_sprite_colors: RandomizeSpriteColors
    randomize_wild_warp: RandomizeWildWarp
    #Routing options
    story_mode: StoryMode
    no_bow_mode: NoBowMode
    orbs_not_required: OrbsNotRequired
    thunder_warp: ThunderWarp
    vanilla_dolphin: VanillaDolphin
    #Glitch options
    fake_flight: FakeFlight
    statue_glitch: StatueGlitch
    mt_sabre_skip: MtSabreSkip
    statue_gauntlet_skip: StatueGauntletSkip
    sword_charge_glitch: SwordChargeGlitch
    trigger_skip: TriggerSkip
    rage_skip: RageSkip
    #Aesthetic options
    randomize_background_music: RandomizeBackgroundMusic
    randomize_map_colors: RandomizeMapColors
    #Monster options
    randomize_monster_weaknesses: RandomizeMonsterWeaknesses
    oops_all_mimics: OopsAllMimics
    shuffle_tower_robots: ShuffleTowerRobots
    #Easy mode options
    dont_shuffle_mimics: DontShuffleMimics
    keep_unique_items_and_consumables_separate: KeepUniqueItemsAndConsumablesSeparate
    decrease_enemy_damage: DecreaseEnemyDamage
    guarantee_starting_sword: GuaranteeStartingSword
    guarantee_refresh: GuaranteeRefresh
    experience_scales_faster: ExperienceScalesFaster
    no_community_jokes: NoCommunityJokes
    #No guarantees options
    battle_magic_not_guaranteed: BattleMagicNotGuaranteed
    tink_mode: TinkMode
    barrier_not_guaranteed: BarrierNotGuaranteed
    gas_mask_not_guaranteed: GasMaskNotGuaranteed
    #Hard mode options
    dont_buff_consumables: DontBuffConsumables
    max_scaling_in_tower: MaxScalingInTower
    experience_scales_slower: ExperienceScalesSlower
    charge_shots_only: ChargeShotsOnly
    blackout: Blackout
    permadeath: Permadeath
    #Vanilla options
    dont_buff_dyna: DontBuffDyna
    dont_buff_bonus_items: DontBuffBonusItems
    vanilla_maps: VanillaMaps
    vanilla_shops: VanillaShops
    vanilla_wild_warp: VanillaWildWarp
    vanilla_hud: VanillaHUD
    #Quality of Life options
    dont_auto_equip_upgrades: DontAutoEquipUpgrades
    disable_controller_shortcuts: DisableControllerShortcuts
    audible_wall_cues: AudibleWallCues
    #Misc Archipelago Only options
    start_inventory_from_pool: StartInventoryPool
    plando_connections: CrystalisPlandoConnections
