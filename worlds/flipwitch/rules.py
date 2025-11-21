from BaseClasses import CollectionState
from typing import Dict, List, TYPE_CHECKING

from worlds.generic.Rules import CollectionRule

from .options import FlipwitchOptions
from .strings.regions_entrances import FlipwitchEntrance, FlipwitchRegion
from .strings.items import Coin, Upgrade, QuestItem, Unlock, Goal, Costume, Key, Power, Custom
from .strings.locations import WitchyWoods, Quest, Gacha, SpiritTown, ShadySewers, GhostCastle, Jigoku, ClubDemon, Tengoku, AngelicHallway, FungalForest, SlimeCitadel, \
    UmiUmi, ChaosCastle

if TYPE_CHECKING:
    from . import FlipwitchWorld


class FlipwitchRules:
    player: int
    world: "FlipwitchWorld"
    region_rules: Dict[str, CollectionRule]
    entrance_rules: Dict[str, CollectionRule]
    location_rules: Dict[str, CollectionRule]
    animal_order: List[str]
    bunny_order: List[str]
    monster_order: List[str]
    angel_order: List[str]

    def __init__(self, world: "FlipwitchWorld") -> None:
        self.player = world.player
        self.world = world
        self.world.options = world.options

        self.region_rules = {
        }

        self.entrance_rules = {
            FlipwitchEntrance.witchy_to_spirit: lambda state: state.has(Unlock.crystal_block, self.player),
            FlipwitchEntrance.woods_to_sex_experience_layer_1: lambda state: state.has(QuestItem.fairy_bubble, self.player),
            FlipwitchEntrance.sex_experience_layer_1_to_sex_experience_layer_2: lambda state: self.can_present_gender(state, self.world.options, "Female"),
            FlipwitchEntrance.sex_experience_layer_2_to_sex_experience_layer_3: lambda state: state.has(Upgrade.bewitched_bubble, self.player),
            FlipwitchEntrance.woods_to_woods_lower: lambda state: self.can_present_gender(state, self.world.options, "Male"),
            FlipwitchEntrance.spirit_to_cafe: lambda state: self.can_complete_quest(state, Quest.let_the_dog_out) and
                                                            self.can_complete_quest(state, Quest.panty_raid) and
                                                            self.can_complete_quest(state, Quest.need_my_cowbell),
            FlipwitchEntrance.spirit_to_mansion: lambda state: self.can_reach_mansion_door(world.options, state) and self.can_convince_mansion_guard(state),
            FlipwitchEntrance.spirit_to_shady: lambda state: state.has(Power.slime_form, self.player) and state.has(Power.ghost_form,
                                                                                                                    self.player) and self.has_upgrade_stage(3, state),
            FlipwitchEntrance.spirit_to_early_ghost: lambda state: state.has(Unlock.goblin_crystal_block, self.player) and self.has_upgrade_stage(1, state),
            FlipwitchEntrance.early_ghost_to_ghost: lambda state: state.has(Key.ghostly_castle, self.player) and self.can_take_either_ghost_castle_path_up_to_rose(state),
            FlipwitchEntrance.ghost_to_ghost_rose: lambda state: self.can_take_either_ghost_castle_path(state),
            FlipwitchEntrance.ghost_rose_to_upper_ghost: lambda state: state.has(Power.ghost_form, self.player) and state.has(Upgrade.bewitched_bubble, self.player),
            FlipwitchEntrance.spirit_to_jigoku: lambda state: state.has(Power.ghost_form, self.player) and self.has_upgrade_stage(1, state),
            FlipwitchEntrance.jigoku_to_club_demon: lambda state: self.can_move_horizontally_enough(state),
            FlipwitchEntrance.early_ghost_to_fungal_forest: lambda state: state.has(Power.ghost_form, self.player),
            FlipwitchEntrance.fungal_forest_to_tengoku: lambda state: self.can_move_horizontally_enough(state) and self.has_upgrade_stage(2, state),
            FlipwitchEntrance.tengoku_to_tengoku_upper: lambda state: self.can_present_gender(state, self.world.options, "Male") or state.has(Upgrade.angel_feathers,
                                                                                                                                              self.player),
            FlipwitchEntrance.angelic_to_angelic_mid: lambda state: state.has(Upgrade.bewitched_bubble, self.player),
            FlipwitchEntrance.angelic_mid_to_angelic_upper: lambda state: state.has(Upgrade.angel_feathers, self.player),
            FlipwitchEntrance.fungal_to_deep_fungal: lambda state: state.has(Upgrade.angel_feathers, self.player) and self.has_upgrade_stage(
                3, state),
            FlipwitchEntrance.deep_fungal_to_slime_citadel: lambda state: state.has(Power.slime_form, self.player) and state.has(Key.slime_citadel,
                                                                                                                                 self.player),
            FlipwitchEntrance.fungal_to_umi_umi: lambda state: state.has(Upgrade.mermaid_scale, self.player) and self.has_upgrade_stage(3, state),
            FlipwitchEntrance.umi_umi_to_umi_umi_depths: lambda state: state.has(Upgrade.angel_feathers, self.player) or self.can_present_gender(state,
                                                                                                                                                 self.world.options,
                                                                                                                                                 "Male"),
            FlipwitchEntrance.spirit_to_outside_chaos_castle: lambda state: state.has(Goal.chaos_piece, self.player, 6),
            FlipwitchEntrance.outside_chaos_to_chaos: lambda state: state.has(Upgrade.bewitched_bubble, self.player) and self.has_upgrade_stage(4, state),
        }

        self.location_rules = {
            WitchyWoods.red_costume: lambda state: self.can_present_gender(state, self.world.options, "Male"),
            WitchyWoods.sexual_experience_1: lambda state: self.has_fucked_enough(state, 4, self.world.options),
            WitchyWoods.sexual_experience_2: lambda state: self.has_fucked_enough(state, 8, self.world.options),
            WitchyWoods.sexual_experience_3: lambda state: self.has_fucked_enough(state, 8, self.world.options),
            WitchyWoods.sexual_experience_4: lambda state: self.has_fucked_enough(state, 12, self.world.options),
            WitchyWoods.sexual_experience_5: lambda state: self.has_fucked_enough(state, 16, self.world.options),
            WitchyWoods.sexual_experience_6: lambda state: self.has_fucked_enough(state, 16, self.world.options),
            WitchyWoods.sexual_experience_7: lambda state: self.has_fucked_enough(state, 20, self.world.options),
            WitchyWoods.sexual_experience_8: lambda state: self.has_fucked_enough(state, 24, self.world.options),
            WitchyWoods.sexual_experience_9: lambda state: self.has_fucked_enough(state, 24, self.world.options),
            WitchyWoods.sexual_experience_10: lambda state: self.has_fucked_enough(state, 28, self.world.options),
            WitchyWoods.sexual_experience_11: lambda state: self.has_fucked_enough(state, 32, self.world.options),
            WitchyWoods.sexual_experience_12: lambda state: self.has_fucked_enough(state, 32, self.world.options),
            WitchyWoods.sexual_experience_13: lambda state: self.has_fucked_enough(state, 36, self.world.options),
            WitchyWoods.sexual_experience_14: lambda state: self.has_fucked_enough(state, 40, self.world.options),
            WitchyWoods.goblin_apartment: lambda state: state.has(QuestItem.goblin_apartment, self.player) and
                                                        self.can_complete_quest(state, Quest.model_goblin),
            WitchyWoods.fairy_chest: lambda state: state.has(Upgrade.bewitched_bubble, self.player),
            WitchyWoods.hidden_spring: lambda state: state.has(Upgrade.bewitched_bubble, self.player),
            WitchyWoods.red_wine: lambda state: state.has(Upgrade.angel_feathers, self.player),
            WitchyWoods.before_fairy: lambda state: state.has(Upgrade.angel_feathers, self.player),
            WitchyWoods.hidden_coin_early: lambda state: self.can_present_gender(state, self.world.options, "Male"),
            WitchyWoods.hidden_coin_early_chest: lambda state: self.can_present_gender(state, self.world.options, "Male"),
            WitchyWoods.flip_platform: lambda state: state.has(Upgrade.angel_feathers, self.player),
            WitchyWoods.man_cave: lambda state: state.has(QuestItem.goblin_headshot, self.player),
            WitchyWoods.goblin_queen_mp: lambda state: state.has(Key.goblin_queen, self.player),
            WitchyWoods.goblin_queen_chaos: lambda state: state.has(Key.goblin_queen, self.player),
            WitchyWoods.post_fight: lambda state: state.has(Key.goblin_queen, self.player) and state.has(Power.slime_form, self.player),
            WitchyWoods.fairy_reward: lambda state: state.can_reach_location(WitchyWoods.goblin_queen_chaos, self.player),

            SpiritTown.city_hp: lambda state: state.has(Upgrade.bewitched_bubble, self.player),
            SpiritTown.city_mp: lambda state: state.has(Upgrade.bewitched_bubble, self.player),
            SpiritTown.toilet_coin: lambda state: state.has(Upgrade.angel_feathers, self.player) or state.has(Upgrade.demon_wings, self.player),
            SpiritTown.cabaret_cherry_key: lambda state: self.can_complete_quest(state, Quest.deluxe_milkshake),
            SpiritTown.cabaret_vip_chest: lambda state: state.has(QuestItem.vip_key, self.player),
            SpiritTown.cemetery: lambda state: state.has(Upgrade.mermaid_scale, self.player) and state.has(Unlock.goblin_crystal_block, self.player),
            SpiritTown.ghost_key: lambda state: state.has(Upgrade.bewitched_bubble, self.player) and state.has(Unlock.goblin_crystal_block, self.player),
            SpiritTown.apartment_key: lambda state: self.can_complete_quest(state, Quest.model_goblin),
            SpiritTown.alley: lambda state: state.has(Power.slime_form, self.player),
            SpiritTown.chaos: lambda state: state.has(Key.abandoned_apartment, self.player),
            SpiritTown.home_2: lambda state: state.has(Unlock.goblin_crystal_block, self.player) and (
                    state.has(Upgrade.angel_feathers, self.player) or state.has(Upgrade.demon_wings, self.player)),
            SpiritTown.home_1: lambda state: state.has(Unlock.goblin_crystal_block, self.player) and state.has(Power.ghost_form, self.player),
            SpiritTown.home_6: lambda state: state.has(Unlock.goblin_crystal_block, self.player) and state.has(Upgrade.mermaid_scale, self.player),
            SpiritTown.green_house: lambda state: state.has(Unlock.goblin_crystal_block, self.player) and state.has(Power.slime_form, self.player),
            SpiritTown.fungal_key: lambda state: self.can_wear_costume(state, self.world.options, Costume.pigman),
            SpiritTown.maid_contract: lambda state: self.can_wear_costume(state, self.world.options, Costume.maid),
            SpiritTown.lone_house: lambda state: state.has(Upgrade.angel_feathers, self.player) and self.can_reach_mansion_door(self.world.options, state),
            SpiritTown.special_milkshake: lambda state: state.can_reach_region(FlipwitchRegion.cabaret_cafe, self.player) and state.has(QuestItem.delicious_milk,
                                                                                                                                        self.player),

            ShadySewers.side_chest: lambda state: state.has(Upgrade.angel_feathers, self.player),
            ShadySewers.shady_hp: lambda state: state.has(Upgrade.angel_feathers, self.player) and state.has(Upgrade.bewitched_bubble, self.player),
            ShadySewers.shady_chest: lambda state: state.has(Upgrade.angel_feathers, self.player) and state.has(Upgrade.bewitched_bubble, self.player),
            ShadySewers.ratchel_coin: lambda state: self.can_present_gender(state, self.world.options, "Male") or state.has(Upgrade.angel_feathers, self.player),
            ShadySewers.dwd_tutorial: lambda state: state.has(Upgrade.mermaid_scale, self.player),

            GhostCastle.below_entrance: lambda state: state.has(Power.ghost_form, self.player),
            GhostCastle.slime_1: lambda state: state.has(Key.ghostly_castle, self.player) and state.has(Power.slime_form, self.player),
            GhostCastle.slime_2: lambda state: state.has(Key.ghostly_castle, self.player) and state.has(Power.slime_form, self.player),
            GhostCastle.slime_3: lambda state: state.has(Key.ghostly_castle, self.player) and state.has(Power.slime_form, self.player) and
                                               (self.can_present_gender(state, self.world.options, "Male") or
                                                state.has(Upgrade.angel_feathers, self.player)),
            GhostCastle.up_ladder: lambda state: state.has(Upgrade.angel_feathers, self.player),
            GhostCastle.giant_flip: lambda state: state.has(Key.ghostly_castle, self.player) and
                                                  (state.has(Upgrade.bewitched_bubble, self.player) or (self.can_present_gender(state, self.world.options, "Male") and
                                                                                                        state.has(Upgrade.angel_feathers, self.player) and state.has(
                                                              Upgrade.demon_wings, self.player))),
            GhostCastle.hidden_ledge: lambda state: state.has(Key.ghostly_castle, self.player) and
                                                    (state.has(Upgrade.bewitched_bubble, self.player) or (self.can_present_gender(state, self.world.options, "Male") and
                                                                                                          state.has(Upgrade.angel_feathers, self.player) and state.has(
                                                                Upgrade.demon_wings, self.player))),
            GhostCastle.elf: lambda state: state.has(Upgrade.bewitched_bubble, self.player) or self.can_move_horizontally_enough(state),
            GhostCastle.elf_chest: lambda state: state.has(Upgrade.bewitched_bubble, self.player) or state.has(Upgrade.angel_feathers, self.player),
            GhostCastle.across_boss: lambda state: state.has(Upgrade.demon_wings, self.player) or state.has(Upgrade.angel_feathers, self.player),

            Jigoku.hidden_flip: lambda state: self.can_present_gender(state, self.world.options, "Male"),
            Jigoku.slime_form: lambda state: state.has(Power.slime_form, self.player),
            Jigoku.cat_shrine: lambda state: self.can_wear_costume(state, self.world.options, Costume.miko),
            Jigoku.hot_guy: lambda state: state.has(Key.beast, self.player) and state.has(Upgrade.bewitched_bubble, self.player),
            Jigoku.far_ledge: lambda state: state.has(Upgrade.angel_feathers, self.player) or (state.has(Upgrade.bewitched_bubble, self.player) and state.has(Upgrade.demon_wings, self.player)),
            Jigoku.hidden_flip_chest: lambda state: state.has(Upgrade.bewitched_bubble, self.player) or
                                                    (self.can_present_gender(state, self.world.options, "Male") and state.has(Upgrade.angel_feathers, self.player) and
                                                     state.has(Upgrade.demon_wings, self.player)),
            Jigoku.hidden_ledge: lambda state: self.can_present_gender(state, self.world.options, "Male") or state.has(Upgrade.angel_feathers, self.player),
            Jigoku.demon_wings: lambda state: state.has(Key.collapsed_temple, self.player) or self.can_move_horizontally_enough(state),
            Jigoku.demon_tutorial: lambda state: state.has(Upgrade.demon_wings, self.player),
            Jigoku.northern_cat_shrine: lambda state: self.can_wear_costume(state, self.world.options, Costume.miko) and
                                                      (state.has(Key.collapsed_temple, self.player) or self.can_move_horizontally_enough(state)),
            Jigoku.cat_coin: lambda state: state.has(Key.collapsed_temple, self.player) or self.can_move_horizontally_enough(state),
            Jigoku.cat_chest: lambda state: state.has(Key.collapsed_temple, self.player) or self.can_move_horizontally_enough(state),

            ClubDemon.demon_letter: lambda state: state.has(QuestItem.angelic_letter, self.player) and self.can_wear_costume(state, self.world.options, Costume.postman),
            ClubDemon.door: lambda state: state.has(Upgrade.bewitched_bubble, self.player) and state.has(Key.demon_club, self.player),
            ClubDemon.flip_magic_chest: lambda state: self.can_present_gender(state, self.world.options, "Female") or state.has(Upgrade.angel_feathers, self.player),
            ClubDemon.flip_magic_coin: lambda state: state.has(Upgrade.bewitched_bubble, self.player),
            ClubDemon.demonic_gauntlet: lambda state: state.has(Upgrade.bewitched_bubble, self.player),
            ClubDemon.cat_shrine: lambda state: self.can_wear_costume(state, self.world.options, Costume.miko),
            ClubDemon.demon_boss_chest: lambda state: state.has(Key.secret_club, self.player),
            ClubDemon.demon_boss_chaos: lambda state: state.has(Key.demon_boss, self.player) and state.has(Upgrade.bewitched_bubble, self.player),
            ClubDemon.demon_boss_mp: lambda state: state.has(Key.demon_boss, self.player) and state.has(Upgrade.bewitched_bubble, self.player),

            Tengoku.hidden_flip: lambda state: self.can_present_gender(state, self.world.options, "Female"),
            Tengoku.birby: lambda state: state.has(Upgrade.bewitched_bubble, self.player),
            Tengoku.flip_magic: lambda state: self.can_present_gender(state, self.world.options, "Female"),

            AngelicHallway.hidden_foliage_2: lambda state: state.has(Upgrade.angel_feathers, self.player),
            AngelicHallway.angelic_gauntlet: lambda state: state.has(Upgrade.bewitched_bubble, self.player),
            AngelicHallway.below_thimble: lambda state: state.has(Power.ghost_form, self.player) and
                                                        (self.can_present_gender(state, self.world.options, "Female") or
                                                         state.has(Upgrade.angel_feathers, self.player)),
            AngelicHallway.thimble_chest: lambda state: state.has(Power.ghost_form, self.player) and state.has(Upgrade.bewitched_bubble, self.player),
            AngelicHallway.thimble_1: lambda state: state.has(Power.ghost_form, self.player) and state.has(Upgrade.bewitched_bubble, self.player),
            AngelicHallway.thimble_2: lambda state: state.has(Power.ghost_form, self.player) and state.has(Upgrade.bewitched_bubble, self.player),
            AngelicHallway.angel_letter: lambda state: self.can_wear_costume(state, self.world.options, Costume.postman),

            FungalForest.fungal_deal: lambda state: state.has(QuestItem.fungal, self.player),
            FungalForest.fungella: lambda state: state.has(QuestItem.fungal, self.player),
            FungalForest.flip_magic: lambda state: state.has(Upgrade.demon_wings, self.player) or state.has(Upgrade.bewitched_bubble, self.player),
            FungalForest.heavenly_daikon: lambda state: state.has(Upgrade.angel_feathers, self.player) and
                                                        (state.has(Upgrade.bewitched_bubble, self.player) or
                                                         (self.can_present_gender(state, self.world.options, "Female") and
                                                          state.has(Upgrade.demon_wings, self.player))),
            FungalForest.fungal_gauntlet: lambda state: self.can_present_gender(state, self.world.options, "Male"),
            FungalForest.blue_jelly: lambda state: self.can_present_gender(state, self.world.options, "Male"),
            FungalForest.slime_form: lambda state: self.can_present_gender(state, self.world.options, "Male") and state.has(Key.forgotten_fungal, self.player),
            FungalForest.slime_tutorial: lambda state: state.has(Power.slime_form, self.player) and
                                                       self.can_present_gender(state, self.world.options, "Male") and state.has(Key.forgotten_fungal, self.player),
            FungalForest.slime_citadel_key: lambda state: state.has(Power.slime_form, self.player),

            SlimeCitadel.secret_spring_stone: lambda state: self.can_wear_costume(state, self.world.options, Costume.alchemist),
            SlimeCitadel.silky_slime_stone: lambda state: self.can_wear_costume(state, self.world.options, Costume.alchemist),
            SlimeCitadel.slurp_stone: lambda state: self.can_wear_costume(state, self.world.options, Costume.alchemist) and state.has(Key.slimy_sub_boss, self.player),
            SlimeCitadel.slurp_chest: lambda state: state.has(Key.slimy_sub_boss, self.player),
            SlimeCitadel.slimy_princess_chaos: lambda state: state.has(Key.slime_boss, self.player),
            SlimeCitadel.slimy_princess_mp: lambda state: state.has(Key.slime_boss, self.player),

            UmiUmi.early_coin: lambda state: self.can_move_horizontally_enough(state),
            UmiUmi.flip_magic_chest: lambda state: state.has(Upgrade.angel_feathers, self.player),
            UmiUmi.flip_magic_coin: lambda state: state.has(Upgrade.angel_feathers, self.player),
            UmiUmi.save_chest: lambda state: state.has(Upgrade.angel_feathers, self.player),
            UmiUmi.chaos_fight: lambda state: self.can_move_horizontally_enough(state),
            UmiUmi.octrina_chest: lambda state: state.has(Upgrade.bewitched_bubble, self.player) and state.has(Upgrade.angel_feathers, self.player),
            UmiUmi.watery_gauntlet: lambda state: self.can_present_gender(state, self.world.options, "Female") or state.has(Upgrade.angel_feathers, self.player),
            UmiUmi.frog_boss_chaos: lambda state: state.has(Key.frog_boss, self.player),
            UmiUmi.frog_boss_mp: lambda state: state.has(Key.frog_boss, self.player),

            ChaosCastle.outside_coin: lambda state: state.has(Upgrade.angel_feathers, self.player) and state.has(Upgrade.demon_wings, self.player),
            ChaosCastle.ghost_coin: lambda state: state.has(Power.ghost_form, self.player),
            ChaosCastle.citadel: lambda state: state.has(Power.slime_form, self.player),
            ChaosCastle.fungal: lambda state: state.has(Power.slime_form, self.player),
            ChaosCastle.pandora_key: lambda state: state.has(Power.slime_form, self.player),
            ChaosCastle.pandora_mp: lambda state: state.has(Power.slime_form, self.player),
            ChaosCastle.jump_chest: lambda state: state.has(Upgrade.angel_feathers, self.player) and state.has(Upgrade.demon_wings, self.player),
            ChaosCastle.jump_hp: lambda state: state.has(Upgrade.angel_feathers, self.player) and state.has(Upgrade.demon_wings, self.player),

            Quest.magic_mentor: lambda state: state.has(QuestItem.fairy_bubble, self.player),
            Quest.need_my_cowbell: lambda state: state.has(QuestItem.cowbell, self.player),
            Quest.giant_chest_key: lambda state: state.has(QuestItem.mimic_chest, self.player),
            Quest.fairy_mushroom: lambda state: self.can_wear_costume(state, self.world.options, Costume.fairy) and state.has(Upgrade.bewitched_bubble, self.player),
            Quest.model_goblin: lambda state: state.has(QuestItem.business_card, self.player) and state.has(QuestItem.goblin_headshot, self.player),
            Quest.goblin_stud: lambda state: self.can_wear_costume(state, self.world.options, Costume.goblin) and state.has(Key.goblin_queen, self.player),
            Quest.legendary_chewtoy: lambda state: self.can_complete_quest(state, Quest.boned) and state.has(QuestItem.legendary_halo, self.player),
            Quest.deluxe_milkshake: lambda state: state.has(QuestItem.delicious_milk, self.player) and state.has(QuestItem.belle_milkshake, self.player),
            Quest.rat_problem: lambda state: state.has(QuestItem.cherry_key, self.player) and self.can_complete_quest(state, Quest.deluxe_milkshake),
            Quest.haunted_bedroom: lambda state: self.can_complete_quest(state, Quest.ghost_hunters) and state.has(Power.slime_form, self.player),
            Quest.ectogasm: lambda state: self.can_complete_quest(state, Quest.haunted_bedroom) and self.can_wear_costume(state, self.world.options, Costume.cat),
            Quest.jelly_mushroom: lambda state: state.has(QuestItem.blue_jelly_mushroom, self.player),
            Quest.booze_bunny: lambda state: state.has(QuestItem.red_wine, self.player),
            Quest.help_wanted: lambda state: self.can_complete_quest(state, Quest.booze_bunny) and
                                             self.can_complete_quest(state, Quest.legendary_chewtoy) and
                                             self.can_complete_quest(state, Quest.rat_problem) and
                                             self.can_complete_quest(state, Quest.haunted_bedroom),
            Quest.medical_emergency: lambda state: self.can_wear_costume(state, self.world.options, Costume.nurse),
            Quest.let_the_dog_out: lambda state: state.has(Power.ghost_form, self.player) and self.can_present_gender(state, self.world.options, "Female"),
            Quest.stop_democracy: lambda state: self.can_wear_costume(state, self.world.options, Costume.dominating),
            Quest.bunny_club: lambda state: self.can_wear_costume(state, self.world.options, Costume.bunny),
            Quest.silky_slime: lambda state: state.has(QuestItem.silky_slime, self.player) and self.can_present_gender(state, self.world.options, "Male"),
            Quest.emotional_baggage: lambda state: state.has(QuestItem.gobliana_luggage, self.player) and self.can_complete_quest(state, Quest.model_goblin),
            Quest.dirty_debut: lambda state: self.can_complete_quest(state, Quest.emotional_baggage) and state.can_reach_location(AngelicHallway.elf_1, self.player),
            Quest.devilicious: lambda state: self.can_complete_quest(state, Quest.deluxe_milkshake) and state.has(QuestItem.hellish_dango, self.player),
            Quest.daikon: lambda state: self.can_complete_quest(state, Quest.devilicious) and state.has(QuestItem.heavenly_daikon, self.player),
            Quest.out_of_service: lambda state: state.has(QuestItem.mono_password, self.player),
            Quest.whorus: lambda state: self.can_wear_costume(state, self.world.options, Costume.nun),
            Quest.priest: lambda state: self.can_wear_costume(state, self.world.options, Costume.priest),
            Quest.alley_cat: lambda state: state.has(Upgrade.angel_feathers, self.player) and self.can_present_gender(state, self.world.options, "Male") and
                                           (state.has(Upgrade.bewitched_bubble, self.player) or state.has(Upgrade.demon_wings, self.player)),
            Quest.tatils_tale: lambda state: state.has(QuestItem.fungal, self.player) and state.has(QuestItem.deed, self.player) and
                                             self.can_wear_costume(state, self.world.options, Costume.pigman),
            Quest.signing_bonus: lambda state: state.has(QuestItem.maid_contract, self.player) and self.can_wear_costume(state, self.world.options, Costume.maid),
            Quest.cardio_day: lambda state: self.can_wear_costume(state, self.world.options, Costume.rat),
            Quest.panty_raid: lambda state: state.has(QuestItem.clothes, self.player) and self.can_present_gender(state, self.world.options, "Male"),
            Quest.unlucky_cat: lambda state: self.can_wear_costume(state, self.world.options, Costume.miko) and state.has(QuestItem.soul_fragment, self.player, 3) and
                                             self.can_move_horizontally_enough(state),
            Quest.harvest_season: lambda state: self.can_wear_costume(state, self.world.options, Costume.farmer),
            Quest.long_distance: lambda state: self.can_wear_costume(state, self.world.options, Costume.postman) and state.has(QuestItem.demonic_letter, self.player) and
                                               state.has(QuestItem.angelic_letter, self.player) and state.can_reach_region(FlipwitchRegion.club_demon, self.player),
            Quest.summoning_stones: lambda state: self.can_wear_costume(state, self.world.options, Costume.alchemist) and
                                                  state.has(QuestItem.summon_stone, self.player, 3) and state.has(Key.slimy_sub_boss, self.player),
            Quest.semen_with_a: lambda state: self.can_wear_costume(state, self.world.options, Costume.angler) and state.has(Key.frog_boss, self.player),

            Gacha.gacha_sp1: lambda state: state.has(Coin.promotional_coin, self.player),
            Gacha.gacha_ad1: lambda state: self.has_enough_coins(Gacha.gacha_ad1, state),
            Gacha.gacha_ad2: lambda state: self.has_enough_coins(Gacha.gacha_ad2, state),
            Gacha.gacha_ad3: lambda state: self.has_enough_coins(Gacha.gacha_ad3, state),
            Gacha.gacha_ad4: lambda state: self.has_enough_coins(Gacha.gacha_ad4, state),
            Gacha.gacha_ad5: lambda state: self.has_enough_coins(Gacha.gacha_ad5, state),
            Gacha.gacha_ad6: lambda state: self.has_enough_coins(Gacha.gacha_ad6, state),
            Gacha.gacha_ad7: lambda state: self.has_enough_coins(Gacha.gacha_ad7, state),
            Gacha.gacha_ad8: lambda state: self.has_enough_coins(Gacha.gacha_ad8, state),
            Gacha.gacha_ad9: lambda state: self.has_enough_coins(Gacha.gacha_ad9, state),
            Gacha.gacha_ad0: lambda state: self.has_enough_coins(Gacha.gacha_ad0, state),
            Gacha.gacha_mg1: lambda state: self.has_enough_coins(Gacha.gacha_mg1, state),
            Gacha.gacha_mg2: lambda state: self.has_enough_coins(Gacha.gacha_mg2, state),
            Gacha.gacha_mg3: lambda state: self.has_enough_coins(Gacha.gacha_mg3, state),
            Gacha.gacha_mg4: lambda state: self.has_enough_coins(Gacha.gacha_mg4, state),
            Gacha.gacha_mg5: lambda state: self.has_enough_coins(Gacha.gacha_mg5, state),
            Gacha.gacha_mg6: lambda state: self.has_enough_coins(Gacha.gacha_mg6, state),
            Gacha.gacha_mg7: lambda state: self.has_enough_coins(Gacha.gacha_mg7, state),
            Gacha.gacha_mg8: lambda state: self.has_enough_coins(Gacha.gacha_mg8, state),
            Gacha.gacha_mg9: lambda state: self.has_enough_coins(Gacha.gacha_mg9, state),
            Gacha.gacha_mg0: lambda state: self.has_enough_coins(Gacha.gacha_mg0, state),
            Gacha.gacha_bg1: lambda state: self.has_enough_coins(Gacha.gacha_bg1, state),
            Gacha.gacha_bg2: lambda state: self.has_enough_coins(Gacha.gacha_bg2, state),
            Gacha.gacha_bg3: lambda state: self.has_enough_coins(Gacha.gacha_bg3, state),
            Gacha.gacha_bg4: lambda state: self.has_enough_coins(Gacha.gacha_bg4, state),
            Gacha.gacha_bg5: lambda state: self.has_enough_coins(Gacha.gacha_bg5, state),
            Gacha.gacha_bg6: lambda state: self.has_enough_coins(Gacha.gacha_bg6, state),
            Gacha.gacha_bg7: lambda state: self.has_enough_coins(Gacha.gacha_bg7, state),
            Gacha.gacha_bg8: lambda state: self.has_enough_coins(Gacha.gacha_bg8, state),
            Gacha.gacha_bg9: lambda state: self.has_enough_coins(Gacha.gacha_bg9, state),
            Gacha.gacha_bg0: lambda state: self.has_enough_coins(Gacha.gacha_bg0, state),
            Gacha.gacha_ag1: lambda state: self.has_enough_coins(Gacha.gacha_ag1, state),
            Gacha.gacha_ag2: lambda state: self.has_enough_coins(Gacha.gacha_ag2, state),
            Gacha.gacha_ag3: lambda state: self.has_enough_coins(Gacha.gacha_ag3, state),
            Gacha.gacha_ag4: lambda state: self.has_enough_coins(Gacha.gacha_ag4, state),
            Gacha.gacha_ag5: lambda state: self.has_enough_coins(Gacha.gacha_ag5, state),
            Gacha.gacha_ag6: lambda state: self.has_enough_coins(Gacha.gacha_ag6, state),
            Gacha.gacha_ag7: lambda state: self.has_enough_coins(Gacha.gacha_ag7, state),
            Gacha.gacha_ag8: lambda state: self.has_enough_coins(Gacha.gacha_ag8, state),
            Gacha.gacha_ag9: lambda state: self.has_enough_coins(Gacha.gacha_ag9, state),
            Gacha.gacha_ag0: lambda state: self.has_enough_coins(Gacha.gacha_ag0, state),
        }

    def has_fucked_enough(self, state: CollectionState, amount: int, options: FlipwitchOptions):
        if options.quest_for_sex == options.quest_for_sex.option_all:
            return state.has(Custom.sex_experience, self.player, amount)
        total_sex_experience = 0
        for quest in Quest.fuck_points:
            if self.can_complete_quest(state, quest):
                total_sex_experience += Quest.fuck_points[quest]
        if total_sex_experience > 7:
            total_sex_experience += 1
        if total_sex_experience > 23:
            total_sex_experience += 1
        return total_sex_experience >= amount

    def can_move_horizontally_enough(self, state: CollectionState):
        return state.has(Upgrade.angel_feathers, self.player) or state.has(Upgrade.demon_wings, self.player)

    def can_complete_quest(self, state: CollectionState, quest: str):
        return state.can_reach_location(quest, self.player)

    def can_wear_costume(self, state: CollectionState, options: FlipwitchOptions, costume: str):
        if costume in Costume.male_costumes:
            return state.has(costume, self.player) and self.can_present_gender(state, options, "Male")
        else:
            return state.has(costume, self.player) and self.can_present_gender(state, options, "Female")

    def can_reach_mansion_door(self, options: FlipwitchOptions, state: CollectionState):
        if options.starting_gender == options.starting_gender.option_female:
            return state.has(Unlock.goblin_crystal_block, self.player) and (
                    state.has(Upgrade.angel_feathers, self.player) or state.has(Upgrade.bewitched_bubble, self.player))
        return state.has(Unlock.goblin_crystal_block, self.player) and state.has(Upgrade.bewitched_bubble, self.player)

    def can_convince_mansion_guard(self, state: CollectionState):
        return self.can_wear_costume(state, self.world.options, Costume.maid) or self.can_wear_costume(state, self.world.options, Costume.pigman)

    def can_present_gender(self, state: CollectionState, options: FlipwitchOptions, gender: str):

        if options.starting_gender == options.starting_gender.option_male:
            return state.has(Upgrade.bewitched_bubble, self.player) or gender == "Male"
        else:
            return state.has(Upgrade.bewitched_bubble, self.player) or gender == "Female"

    def can_take_either_ghost_castle_path_up_to_rose(self, state: CollectionState):
        return state.has(Upgrade.bewitched_bubble, self.player) or (state.has(Power.ghost_form, self.player) and state.has(Key.secret_garden, self.player))

    def can_take_either_ghost_castle_path(self, state: CollectionState):
        return (state.has(Upgrade.bewitched_bubble, self.player) and state.has(Key.rose_garden, self.player)) or (state.has(Power.ghost_form, self.player) and
                                                                                                                  state.has(Key.secret_garden, self.player) and (
                                                                                                                          state.has(Upgrade.angel_feathers,
                                                                                                                                    self.player) or state.has(
                                                                                                                      Upgrade.demon_wings, self.player)))

    def has_enough_coins(self, gacha: str, state: CollectionState):
        if "Animal" in gacha:
            amount = self.animal_order.index(gacha) + 1
            return state.has(Coin.animal_coin, self.player, amount)
        if "Bunny" in gacha:
            amount = self.bunny_order.index(gacha) + 1
            return state.has(Coin.bunny_coin, self.player, amount)
        if "Monster" in gacha:
            amount = self.monster_order.index(gacha) + 1
            return state.has(Coin.monster_coin, self.player, amount)
        if "Angel" in gacha:
            amount = self.angel_order.index(gacha) + 1
            return state.has(Coin.angel_demon_coin, self.player, amount)
        return False

    def has_upgrade_stage(self, stage: int, state: CollectionState):
        return state.has(Upgrade.health, self.player, stage) and state.has(Upgrade.peachy_peach, self.player, stage)

    def set_flipwitch_rules(self, animal_order: List[str], bunny_order: List[str], monster_order: List[str], angel_order: List[str]) -> None:
        self.angel_order = angel_order
        self.bunny_order = bunny_order
        self.monster_order = monster_order
        self.animal_order = animal_order
        multiworld = self.world.multiworld
        for region in multiworld.get_regions(self.player):
            if region.name in self.region_rules:
                for entrance in region.entrances:
                    entrance.access_rule = self.region_rules[region.name]
                for location in region.locations:
                    location.access_rule = self.region_rules[region.name]
            for entrance in region.entrances:
                multiworld.register_indirect_condition(region, entrance)
                if entrance.name in self.entrance_rules:
                    entrance.access_rule = entrance.access_rule and self.entrance_rules[entrance.name]
            for loc in region.locations:
                if loc.name in self.location_rules:
                    loc.access_rule = loc.access_rule and self.location_rules[loc.name]
