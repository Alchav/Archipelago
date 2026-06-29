from .. import SohWorld
from ..Items import Items, SohItem
from BaseClasses import ItemClassification as IC
from ..Enums import Regions, Events, Enemies, EnemyDistance
from .bases import SohTestBase
from ..LogicHelpers import can_kill_enemy
from itertools import combinations

class KillBase(SohTestBase):
    __Test__ = False

    def require_all_to_beat(self, items: list[Items | Events], enemy: Enemies, distance: EnemyDistance = EnemyDistance.CLOSE,
                   wall_or_floor: bool = True, quantity: int = 1, timer: bool = False, in_water: bool = False) -> None:
        # ideally we run these as subtests, but those are currently broken 
        # and report as Success if any subtest succeeds
        # (https://github.com/microsoft/vscode-python/issues/25824)

        self.sweep()
        self.remove_by_name(items)

        for size in range(1, len(items)):
            for invalid_combo in combinations(items, size):
                self.collect_by_name(invalid_combo)
                self.assertFalse(can_kill_enemy(self.get_bundle(), enemy, distance, wall_or_floor, quantity, timer, in_water)._instantiate(self.world)._evaluate(self.multiworld.state), f"Was able to kill {quantity} {str(enemy)}, but shouldn't have been able to with only {invalid_combo} at distance {str(distance.name)} {"on wall or floor" if wall_or_floor else "not on wall or floor"}")
                self.remove_by_name(invalid_combo)
                

        self.collect_by_name(items)

        self.assertTrue(can_kill_enemy(self.get_bundle(), enemy, distance, wall_or_floor, quantity, timer, in_water)._instantiate(self.world)._evaluate(self.multiworld.state), f"Wasn't able to kill {quantity} {str(enemy)}, but should have been able to at distance {str(distance.name)} {"on wall or floor" if wall_or_floor else "not on wall or floor"}")

        self.remove_by_name(items)

    def require_any_to_beat(self, items: list[Items | Events], enemy: Enemies, distance: EnemyDistance = EnemyDistance.CLOSE,
                   wall_or_floor: bool = True, quantity: int = 1, timer: bool = False, in_water: bool = False) -> None:
        # ideally we run these as subtests, but those are currently broken 
        # and report as Success if any subtest succeeds
        # (https://github.com/microsoft/vscode-python/issues/25824)

        self.sweep()
        self.remove_by_name(items)

        for size in range(1, len(items)):
            for valid_combo in combinations(items, size):
                self.collect_by_name(valid_combo)
                self.assertTrue(can_kill_enemy(self.get_bundle(), enemy, distance, wall_or_floor, quantity, timer, in_water)._instantiate(self.world)._evaluate(self.multiworld.state), f"Wasn't able to kill {quantity} {str(enemy)}, but should have been able to with only {valid_combo} at distance {str(distance.name)} {"on wall or floor" if wall_or_floor else "not on wall or floor"}")
                self.remove_by_name(valid_combo)
                

        self.collect_by_name(items)

        self.assertTrue(can_kill_enemy(self.get_bundle(), enemy, distance, wall_or_floor, quantity, timer, in_water)._instantiate(self.world)._evaluate(self.multiworld.state), f"Wasn't able to kill {quantity} {str(enemy)}, but should have been able to at distance {str(distance.name)} {"on wall or floor" if wall_or_floor else "not on wall or floor"}")
        
        self.remove_by_name(items)

# Can Kill Regular Enemies
class TestCanKillEnemy(KillBase):
    options = {"shuffle_deku_nut_bag": True, "shuffle_deku_stick_bag": True, "closed_forest": 2, "door_of_time": 2, "shuffle_kokiri_sword": 1, "shuffle_master_sword": 1}

    """
    Testing to see if we can kill regular enemies. 
    This only checks for special cases, not other helper functions
    """
    def test_gerudo_guard(self):
        """
        Checking if player can kill Gerudo Guard
        """
        for enemy in (Enemies.GERUDO_GUARD, Enemies.BREAK_ROOM_GUARD):
            self.assertFalse(can_kill_enemy(self.get_bundle(), enemy)._instantiate(self.world)._evaluate(self.multiworld.state), f'Could kill {str(enemy)}. This should be impossible.')

    def test_gold_skulltula(self):
        """
        Checking if player can kill Gold Skulltula
        """
        enemy = Enemies.GOLD_SKULLTULA
        items = [Items.BOOMERANG]
        # Boomerang and Hookshot overlapping distances
        for distance in (EnemyDistance.CLOSE, EnemyDistance.SHORT_JUMPSLASH, EnemyDistance.MASTER_SWORD_JUMPSLASH, 
                         EnemyDistance.LONG_JUMPSLASH, EnemyDistance.BOMB_THROW, EnemyDistance.BOOMERANG):
            self.require_all_to_beat(items, enemy, distance)

        # Dins Fire
        items = [Items.PROGRESSIVE_MAGIC_METER, Items.DINS_FIRE]
        for distance in (EnemyDistance.CLOSE, EnemyDistance.SHORT_JUMPSLASH, EnemyDistance.MASTER_SWORD_JUMPSLASH, 
                         EnemyDistance.LONG_JUMPSLASH, EnemyDistance.BOMB_THROW, EnemyDistance.BOOMERANG):
            self.require_all_to_beat(items, enemy, distance)

        # Bombchus
        items = [Items.PROGRESSIVE_BOMB_BAG]
        for distance in (EnemyDistance.CLOSE, EnemyDistance.SHORT_JUMPSLASH, EnemyDistance.MASTER_SWORD_JUMPSLASH, 
                         EnemyDistance.LONG_JUMPSLASH, EnemyDistance.BOMB_THROW, EnemyDistance.BOOMERANG, 
                         EnemyDistance.HOOKSHOT, EnemyDistance.LONGSHOT):
            self.require_all_to_beat(items, enemy, distance)

    def test_big_skulltula(self):
        """
        Checking if player can kill Big Skulltula
        """
        enemy = Enemies.BIG_SKULLTULA
        items = [Items.BOOMERANG]

        # Dins Fire
        items = [Items.PROGRESSIVE_MAGIC_METER, Items.DINS_FIRE]
        for distance in (EnemyDistance.CLOSE, EnemyDistance.SHORT_JUMPSLASH, EnemyDistance.MASTER_SWORD_JUMPSLASH, 
                         EnemyDistance.LONG_JUMPSLASH, EnemyDistance.BOMB_THROW, EnemyDistance.BOOMERANG):
            self.require_all_to_beat(items, enemy, distance)

    def test_dodongo(self):
        """
        Checking if player can kill Dodongo
        """
        enemy = Enemies.DODONGO
     
 
        items = [Items.MEGATON_HAMMER, Items.PROGRESSIVE_SLINGSHOT, Items.PROGRESSIVE_BOW]
        self.require_any_to_beat(items, enemy)

        # Sticks
        items = [Items.PROGRESSIVE_STICK_CAPACITY]
        for i in range(1,6):
            self.require_any_to_beat(items, enemy, quantity=i)

    def test_lizalfos(self):
        """
        Checking if player can kill Lizalfos
        """
        enemy = Enemies.LIZALFOS

        items = [Items.MEGATON_HAMMER, Items.KOKIRI_SWORD, Items.MASTER_SWORD, 
                 Items.BIGGORONS_SWORD, Items.PROGRESSIVE_BOW, Items.PROGRESSIVE_SLINGSHOT, Items.PROGRESSIVE_BOMB_BAG]
        self.require_any_to_beat(items, enemy)

    def test_keese(self):
        for enemy in (Enemies.KEESE, Enemies.FIRE_KEESE):
            # Close
            self.require_all_to_beat([Items.KOKIRI_SWORD], enemy)

            # <= Boomerang
            for distance in (EnemyDistance.CLOSE, EnemyDistance.SHORT_JUMPSLASH, EnemyDistance.MASTER_SWORD_JUMPSLASH, 
                             EnemyDistance.LONG_JUMPSLASH, EnemyDistance.BOMB_THROW, EnemyDistance.BOOMERANG):
                self.require_all_to_beat([Items.BOOMERANG], enemy, distance)

            # Short Jumpslash
            self.require_all_to_beat([Items.MEGATON_HAMMER], enemy, EnemyDistance.SHORT_JUMPSLASH)

    def test_gohma_larva(self):
        """
        Checking if player can kill Gohma Larva
        """
        items = [Items.KOKIRI_SWORD, Items.MASTER_SWORD, Items.BIGGORONS_SWORD, Items.PROGRESSIVE_STICK_CAPACITY, Items.MEGATON_HAMMER, Items.PROGRESSIVE_BOMB_BAG, Items.PROGRESSIVE_SLINGSHOT, Items.PROGRESSIVE_BOW, Items.BOOMERANG, Items.PROGRESSIVE_HOOKSHOT]
        self.require_any_to_beat(items, Enemies.GOHMA_LARVA)
        self.require_all_to_beat([Items.PROGRESSIVE_MAGIC_METER, Items.DINS_FIRE], Enemies.GOHMA_LARVA)

    def test_mad_scrub(self):
        """
        Checking if player can kill Mad Scrub
        """
        items = [Items.KOKIRI_SWORD, Items.MASTER_SWORD, Items.BIGGORONS_SWORD, Items.PROGRESSIVE_STICK_CAPACITY, Items.MEGATON_HAMMER, Items.PROGRESSIVE_BOMB_BAG, Items.PROGRESSIVE_SLINGSHOT, Items.PROGRESSIVE_BOW, Items.BOOMERANG, Items.PROGRESSIVE_HOOKSHOT]
        self.require_any_to_beat(items, Enemies.MAD_SCRUB)
        self.require_all_to_beat([Items.PROGRESSIVE_MAGIC_METER, Items.DINS_FIRE], Enemies.MAD_SCRUB)

    def test_deku_baba(self):
        """
        Checking if player can kill Deku Baba
        """
        items = [Items.KOKIRI_SWORD, Items.MASTER_SWORD, Items.BIGGORONS_SWORD, Items.PROGRESSIVE_STICK_CAPACITY, Items.MEGATON_HAMMER, Items.PROGRESSIVE_BOMB_BAG, Items.PROGRESSIVE_SLINGSHOT, Items.PROGRESSIVE_BOW, Items.BOOMERANG, Items.PROGRESSIVE_HOOKSHOT]
        self.require_any_to_beat(items, Enemies.DEKU_BABA)
        self.require_all_to_beat([Items.PROGRESSIVE_MAGIC_METER, Items.DINS_FIRE], Enemies.DEKU_BABA)

    def test_blue_bubble(self):
        """
        Checking if player can kill Blue Bubble
        """
        items = [Items.MEGATON_HAMMER, Items.KOKIRI_SWORD, Items.MASTER_SWORD, 
                 Items.PROGRESSIVE_BOMB_BAG, Items.PROGRESSIVE_BOW, Items.PROGRESSIVE_SLINGSHOT]
        self.require_any_to_beat(items, Enemies.BLUE_BUBBLE)

    def test_dead_hand(self):
        """
        Checking if player can kill Dead Hand
        """
        items = [Items.KOKIRI_SWORD, Items.MASTER_SWORD, Items.BIGGORONS_SWORD]
        self.require_any_to_beat(items, Enemies.DEAD_HAND)

    def test_withered_deku_baba(self):
        """
        Checking if player can kill Withered Deku Baba
        """
        items = [Items.KOKIRI_SWORD, Items.MASTER_SWORD, Items.BIGGORONS_SWORD, Items.PROGRESSIVE_STICK_CAPACITY, Items.MEGATON_HAMMER, Items.PROGRESSIVE_BOMB_BAG, Items.PROGRESSIVE_SLINGSHOT, Items.PROGRESSIVE_BOW, Items.BOOMERANG, Items.PROGRESSIVE_HOOKSHOT]
        self.require_any_to_beat(items, Enemies.DEKU_BABA)
        self.require_all_to_beat([Items.PROGRESSIVE_MAGIC_METER, Items.DINS_FIRE], Enemies.DEKU_BABA)

    def test_like_like(self):
        """
        Checking if player can kill Like Like
        """
        items = [Items.KOKIRI_SWORD, Items.MASTER_SWORD, Items.BIGGORONS_SWORD, Items.PROGRESSIVE_STICK_CAPACITY, Items.MEGATON_HAMMER, Items.PROGRESSIVE_BOMB_BAG, Items.PROGRESSIVE_SLINGSHOT, Items.PROGRESSIVE_BOW, Items.BOOMERANG, Items.PROGRESSIVE_HOOKSHOT]
        self.require_any_to_beat(items, Enemies.DEKU_BABA)
        self.require_all_to_beat([Items.PROGRESSIVE_MAGIC_METER, Items.DINS_FIRE], Enemies.DEKU_BABA)

    def test_floormaster(self):
        """
        Checking if player can kill Floormaster
        """
        items = [Items.KOKIRI_SWORD, Items.MASTER_SWORD, Items.BIGGORONS_SWORD, Items.PROGRESSIVE_STICK_CAPACITY, Items.MEGATON_HAMMER, Items.PROGRESSIVE_BOMB_BAG, Items.PROGRESSIVE_SLINGSHOT, Items.PROGRESSIVE_BOW, Items.BOOMERANG, Items.PROGRESSIVE_HOOKSHOT]
        self.require_any_to_beat(items, Enemies.DEKU_BABA)
        self.require_all_to_beat([Items.PROGRESSIVE_MAGIC_METER, Items.DINS_FIRE], Enemies.DEKU_BABA)

    def test_stalfos(self):
        """
        Checking if player can kill Stalfos
        """
        items = [Items.KOKIRI_SWORD, Items.MEGATON_HAMMER]
        self.require_any_to_beat(items, Enemies.STALFOS, EnemyDistance.SHORT_JUMPSLASH)
        self.require_all_to_beat([Items.MASTER_SWORD], Enemies.STALFOS, EnemyDistance.MASTER_SWORD_JUMPSLASH)
        items = [Items.BIGGORONS_SWORD, Items.PROGRESSIVE_STICK_CAPACITY]
        self.require_any_to_beat(items, Enemies.STALFOS, EnemyDistance.LONG_JUMPSLASH)
        self.require_all_to_beat([Items.PROGRESSIVE_BOMB_BAG], Enemies.STALFOS, EnemyDistance.BOMB_THROW)
        self.require_all_to_beat([Items.PROGRESSIVE_BOW], Enemies.STALFOS, EnemyDistance.FAR)

    def test_iron_knuckle(self):
        """
        Checking if player can kill Iron Knuckle
        """
        items = [Items.KOKIRI_SWORD, Items.MASTER_SWORD, Items.BIGGORONS_SWORD, Items.MEGATON_HAMMER, Items.PROGRESSIVE_BOMB_BAG]
        self.require_any_to_beat(items, Enemies.IRON_KNUCKLE)

    def test_flare_dancer(self):
        """
        Checking if player can kill Flare Dancer
        """
        items = [Items.MEGATON_HAMMER, Items.PROGRESSIVE_HOOKSHOT]
        self.require_any_to_beat(items, Enemies.FLARE_DANCER)
        self.require_all_to_beat([Items.PROGRESSIVE_BOMB_BAG, Items.KOKIRI_SWORD], Enemies.FLARE_DANCER)
        self.require_all_to_beat([Items.PROGRESSIVE_BOMB_BAG, Items.PROGRESSIVE_BOW], Enemies.FLARE_DANCER)
        self.require_all_to_beat([Items.PROGRESSIVE_BOMB_BAG, Items.PROGRESSIVE_SLINGSHOT], Enemies.FLARE_DANCER)
        self.require_all_to_beat([Items.PROGRESSIVE_BOMB_BAG, Items.BOOMERANG], Enemies.FLARE_DANCER)

    def test_wolfos(self):
        """
        Checking if player can kill Wolfos
        """
        items = [Items.KOKIRI_SWORD, Items.MASTER_SWORD, Items.BIGGORONS_SWORD, Items.PROGRESSIVE_STICK_CAPACITY, 
                 Items.MEGATON_HAMMER, Items.PROGRESSIVE_BOW, Items.PROGRESSIVE_SLINGSHOT, Items.PROGRESSIVE_BOMB_BAG]
        self.require_any_to_beat(items, Enemies.WOLFOS)
        self.require_all_to_beat([Items.PROGRESSIVE_MAGIC_METER, Items.DINS_FIRE], Enemies.WOLFOS)

    def test_white_wolfos(self):
        """
        Checking if player can kill White Wolfos
        """
        items = [Items.KOKIRI_SWORD, Items.MASTER_SWORD, Items.BIGGORONS_SWORD, Items.PROGRESSIVE_STICK_CAPACITY, 
                 Items.MEGATON_HAMMER, Items.PROGRESSIVE_BOW, Items.PROGRESSIVE_SLINGSHOT, Items.PROGRESSIVE_BOMB_BAG]
        self.require_any_to_beat(items, Enemies.WHITE_WOLFOS)
        self.require_all_to_beat([Items.PROGRESSIVE_MAGIC_METER, Items.DINS_FIRE], Enemies.WHITE_WOLFOS)

    def test_wallmaster(self):
        """
        Checking if player can kill Wallmaster
        """
        items = [Items.KOKIRI_SWORD, Items.MASTER_SWORD, Items.BIGGORONS_SWORD, Items.PROGRESSIVE_STICK_CAPACITY, 
                 Items.MEGATON_HAMMER, Items.PROGRESSIVE_BOW, Items.PROGRESSIVE_SLINGSHOT, Items.PROGRESSIVE_BOMB_BAG]
        self.require_any_to_beat(items, Enemies.WALLMASTER)
        self.require_all_to_beat([Items.PROGRESSIVE_MAGIC_METER, Items.DINS_FIRE], Enemies.WALLMASTER)

    def test_armos(self):
        """
        Checking if player can kill Armos
        """
        items = [Items.MASTER_SWORD, Items.BIGGORONS_SWORD, Items.PROGRESSIVE_STICK_CAPACITY, Items.MEGATON_HAMMER, 
                 Items.PROGRESSIVE_BOMB_BAG, Items.PROGRESSIVE_BOW]
        self.require_any_to_beat(items, Enemies.ARMOS)

    def test_dinolfos(self):
        """
        Checking if player can kill Dinolfos
        """
        items = [Items.KOKIRI_SWORD, Items.MASTER_SWORD, Items.BIGGORONS_SWORD, Items.PROGRESSIVE_SLINGSHOT, Items.PROGRESSIVE_BOW]
        self.require_any_to_beat(items, Enemies.DINOLFOS)

    def test_torch_slug(self):
        """
        Checking if player can kill Torch Slug
        """
        items = [Items.KOKIRI_SWORD, Items.MASTER_SWORD, Items.BIGGORONS_SWORD, Items.PROGRESSIVE_STICK_CAPACITY, Items.MEGATON_HAMMER, 
                 Items.PROGRESSIVE_BOW]
        self.require_any_to_beat(items, Enemies.TORCH_SLUG)
        self.require_all_to_beat([Items.PROGRESSIVE_BOMB_BAG], Enemies.TORCH_SLUG)

    def test_freezard(self):
        """
        Checking if player can kill Freezard
        """
        items = [Items.MASTER_SWORD, Items.BIGGORONS_SWORD, Items.MEGATON_HAMMER, Items.PROGRESSIVE_STICK_CAPACITY, 
                 Items.PROGRESSIVE_HOOKSHOT, Items.PROGRESSIVE_BOMB_BAG]
        self.require_any_to_beat(items, Enemies.FREEZARD)
        self.require_all_to_beat([Items.PROGRESSIVE_MAGIC_METER, Items.DINS_FIRE], Enemies.FREEZARD)
        self.require_all_to_beat([Items.PROGRESSIVE_BOW, Items.PROGRESSIVE_MAGIC_METER, Items.FIRE_ARROW], Enemies.FREEZARD)

    def test_shell_blade(self):
        """
        Checking if player can kill Shell Blade
        """
        items = [Items.KOKIRI_SWORD, Items.MASTER_SWORD, Items.BIGGORONS_SWORD, Items.PROGRESSIVE_STICK_CAPACITY, 
                 Items.MEGATON_HAMMER, Items.PROGRESSIVE_BOMB_BAG]
        self.require_any_to_beat(items, Enemies.SHELL_BLADE)
        self.require_all_to_beat([Items.PROGRESSIVE_MAGIC_METER, Items.DINS_FIRE], Enemies.FREEZARD)
        self.require_all_to_beat([Items.PROGRESSIVE_BOW, Items.PROGRESSIVE_MAGIC_METER, Items.FIRE_ARROW], Enemies.FREEZARD)

    def test_spike(self):
        """
        Checking if player can kill Spike
        """
        items = [Items.MASTER_SWORD, Items.BIGGORONS_SWORD, Items.MEGATON_HAMMER, Items.PROGRESSIVE_STICK_CAPACITY, 
                 Items.PROGRESSIVE_HOOKSHOT, Items.PROGRESSIVE_BOW, Items.PROGRESSIVE_BOMB_BAG]
        self.require_any_to_beat(items, Enemies.SPIKE)
        self.require_all_to_beat([Items.PROGRESSIVE_MAGIC_METER, Items.DINS_FIRE], Enemies.SPIKE)

    def test_stinger(self):
        """
        Checking if player can kill Stinger
        """
        items = [Items.KOKIRI_SWORD, Items.MASTER_SWORD, Items.BIGGORONS_SWORD, Items.PROGRESSIVE_STICK_CAPACITY, 
                 Items.MEGATON_HAMMER, Items.PROGRESSIVE_SLINGSHOT, Items.PROGRESSIVE_BOW, Items.PROGRESSIVE_BOMB_BAG, 
                 Items.PROGRESSIVE_HOOKSHOT]
        self.require_any_to_beat(items, Enemies.STINGER)

    def test_big_octo(self):
        """
        Checking if player can kill Big Octo
        """
        items = [Items.KOKIRI_SWORD, Items.MASTER_SWORD, Items.PROGRESSIVE_STICK_CAPACITY]
        self.require_any_to_beat(items, Enemies.BIG_OCTO)

    def test_dark_link(self):
        """
        Checking if player can kill Dark Link
        """
        items = [Items.KOKIRI_SWORD, Items.MASTER_SWORD, Items.BIGGORONS_SWORD, Items.PROGRESSIVE_BOW]
        self.require_any_to_beat(items, Enemies.DARK_LINK)

    def test_anubis(self):
        """
        Checking if player can kill Anubis
        """
        self.require_all_to_beat([Items.PROGRESSIVE_MAGIC_METER, Items.DINS_FIRE], Enemies.ANUBIS)
        self.require_all_to_beat([Items.PROGRESSIVE_BOW, Items.PROGRESSIVE_MAGIC_METER, Items.FIRE_ARROW], Enemies.ANUBIS)

    def test_beamos(self):
        """
        Checking if player can kill Beamos
        """
        items = [Items.PROGRESSIVE_BOMB_BAG]
        self.require_any_to_beat(items, Enemies.BEAMOS)

    def test_purple_leever(self):
        """
        Checking if player can kill Purple Leever
        """
        items = [Items.MASTER_SWORD, Items.BIGGORONS_SWORD]
        self.require_any_to_beat(items, Enemies.PURPLE_LEEVER)

    def test_tentacle(self):
        """
        Checking if player can kill Tentacle
        """
        self.require_all_to_beat([Items.BOOMERANG], Enemies.TENTACLE)

    def test_bari(self):
        """
        Checking if player can kill Bari
        """
        items = [Items.PROGRESSIVE_HOOKSHOT, Items.BOOMERANG, Items.PROGRESSIVE_BOW, Items.PROGRESSIVE_STICK_CAPACITY, 
                 Items.MEGATON_HAMMER, Items.PROGRESSIVE_BOMB_BAG]
        self.require_any_to_beat(items, Enemies.BARI)
        self.require_all_to_beat([Items.PROGRESSIVE_MAGIC_METER, Items.DINS_FIRE], Enemies.BARI)

    def test_shabom(self):
        """
        Checking if player can kill Shabom
        """
        items = [Items.BOOMERANG, Items.PROGRESSIVE_NUT_CAPACITY, Items.KOKIRI_SWORD, Items.MASTER_SWORD, Items.BIGGORONS_SWORD, Items.PROGRESSIVE_STICK_CAPACITY, Items.MEGATON_HAMMER]
        self.require_any_to_beat(items, Enemies.SHABOM)
        self.require_all_to_beat([Items.PROGRESSIVE_MAGIC_METER, Items.DINS_FIRE], Enemies.SHABOM)
        self.require_all_to_beat([Items.PROGRESSIVE_BOW, Items.PROGRESSIVE_MAGIC_METER, Items.ICE_ARROW], Enemies.SHABOM)

    def test_octorok(self):
        """
        Checking if player can kill Octorok
        """
        items = [Items.DEKU_SHIELD, Items.HYLIAN_SHIELD, Items.PROGRESSIVE_HOOKSHOT, Items.BOOMERANG, Items.PROGRESSIVE_BOW, Items.PROGRESSIVE_SLINGSHOT, Items.PROGRESSIVE_BOMB_BAG, Items.BOMBCHUS_5]
        self.require_any_to_beat(items, Enemies.OCTOROK)

    def test_redead(self):
        """
        Checking if player can kill ReDead
        """
        items = [Items.KOKIRI_SWORD, Items.MASTER_SWORD, Items.BIGGORONS_SWORD]
        self.require_any_to_beat(items, Enemies.REDEAD)
        self.require_all_to_beat([Items.PROGRESSIVE_MAGIC_METER, Items.DINS_FIRE], Enemies.REDEAD)

    def test_meg(self):
        """
        Checking if player can kill Meg
        """
        items = [Items.PROGRESSIVE_BOW, Items.PROGRESSIVE_HOOKSHOT, Items.PROGRESSIVE_BOMB_BAG]
        self.require_any_to_beat(items, Enemies.MEG)

    def test_green_bubble(self):
        """
        Checking if player can kill Green Bubble
        """
        items = [Items.MEGATON_HAMMER, Items.KOKIRI_SWORD, Items.MASTER_SWORD, 
            Items.PROGRESSIVE_BOMB_BAG, Items.PROGRESSIVE_BOW, Items.PROGRESSIVE_SLINGSHOT]
        self.require_any_to_beat(items, Enemies.BLUE_BUBBLE)

    def test_gerudo_warrior(self):
        """
        Checking if player can kill Gerudo Warrior
        """
        items = [Items.KOKIRI_SWORD, Items.MASTER_SWORD, Items.BIGGORONS_SWORD, Items.PROGRESSIVE_BOW]
        self.require_any_to_beat(items, Enemies.GERUDO_WARRIOR)

    def test_gibdo(self):
        """
        Checking if player can kill Gibdo
        """
        items = [Items.KOKIRI_SWORD, Items.MASTER_SWORD, Items.BIGGORONS_SWORD]
        self.require_any_to_beat(items, Enemies.GIBDO)
        self.require_all_to_beat([Items.PROGRESSIVE_MAGIC_METER, Items.DINS_FIRE], Enemies.GIBDO)


# Can Kill Bosses
class TestCanKillBoss(KillBase):
    """
    Testing to see if we can kill all the bosses without boss souls on
    """
    options = {"shuffle_boss_souls": 0, "closed_forest": 2, "door_of_time": 2}
    world: SohWorld

    def test_queen_gohma(self):
        """
        Checking if player can kill Queen Ghoma
        """
        items = []

        if self.options["shuffle_boss_souls"]  >= 1:
            items.append(Items.GOHMAS_SOUL)

        self.require_all_to_beat(items, Enemies.GOHMA)

    def test_king_dodongo(self):
        """
        Checking if player can kill King Dodongo
        """
        items = [Items.PROGRESSIVE_BOMB_BAG]

        if self.options["shuffle_boss_souls"]  >= 1:
            items.append(Items.KING_DODONGOS_SOUL)

        self.require_all_to_beat(items, Enemies.KING_DODONGO)

    def test_barinade(self):
        """
        Checking if player can kill Barinade
        """
        items = [Items.BOOMERANG]

        if self.options["shuffle_boss_souls"]  >= 1:
            items.append(Items.BARINADES_SOUL)

        self.require_all_to_beat(items, Enemies.BARINADE)

    def test_phantom_ganon(self):
        """
        Checking if player can kill Phantom Ganon
        """
        items = [Items.PROGRESSIVE_HOOKSHOT]

        if self.options["shuffle_boss_souls"]  >= 1:
            items.append(Items.PHANTOM_GANONS_SOUL)

        self.require_all_to_beat(items, Enemies.PHANTOM_GANON)

    def test_volvagia(self):
        """
        Checking if player can kill Volvagia
        """
        items = [Items.MEGATON_HAMMER]

        if self.options["shuffle_boss_souls"]  >= 1:
            items.append(Items.VOLVAGIAS_SOUL)

        self.require_all_to_beat(items, Enemies.VOLVAGIA)

    def test_morpha(self):
        """
        Checking if player can kill Morpha
        """
        items = [Items.PROGRESSIVE_HOOKSHOT]

        if self.options["shuffle_boss_souls"]  >= 1:
            items.append(Items.MORPHAS_SOUL)

        self.require_all_to_beat(items, Enemies.MORPHA)

    def test_bongo_bongo(self):
        """
        Checking if player can kill Bongo Bongo
        """
        items = [Items.PROGRESSIVE_HOOKSHOT, Items.LENS_OF_TRUTH, Items.PROGRESSIVE_MAGIC_METER]

        if self.options["shuffle_boss_souls"]  >= 1:
            items.append(Items.BONGO_BONGOS_SOUL)

        self.require_all_to_beat(items, Enemies.BONGO_BONGO)

    def test_twinrova(self):
        """
        Checking if player can kill Twinrova
        """
        items = [Items.MIRROR_SHIELD]

        if self.options["shuffle_boss_souls"]  >= 1:
            items.append(Items.TWINROVAS_SOUL)

        self.require_all_to_beat(items, Enemies.TWINROVA)

    def test_ganondorf(self):
        """
        Checking if player can kill Ganondorf
        """
        items = [Items.PROGRESSIVE_MAGIC_METER, Items.LIGHT_ARROW, Items.PROGRESSIVE_BOW]

        if self.options["shuffle_boss_souls"] == 2:
            items.append(Items.GANONS_SOUL)

        self.require_all_to_beat(items, Enemies.GANONDORF)

    def test_ganon(self):
        """
        Checking if player can kill Ganon
        """
        items = []

        if self.options["shuffle_boss_souls"] == 2:
            items.append(Items.GANONS_SOUL)

        self.require_all_to_beat(items, Enemies.GANON)        
        
# Derivative of without boss soul test
class TestAccessCanKillBossWithSoul(TestCanKillBoss):
    """
    Testing to see if we can kill all the bosses with boss souls on
    """
    options = {"shuffle_boss_souls": 1, "closed_forest": 2, "door_of_time": 2, "jabu_jabu": 1, "zoras_fountain": 2, "sleeping_waterfall": 1,"small_key_shuffle": 5, "boss_key_shuffle": 5, "key_rings": 1, "key_rings_count": 9,
               "shuffle_songs": 3}
    world: SohWorld

# Derivative of without boss soul test with ganons soul
class TestAccessCanKillBossWithSoulPlus(TestCanKillBoss):
    """
    Testing to see if we can kill all the bosses with boss souls on
    """
    options = {"shuffle_boss_souls": 2, "closed_forest": 2, "door_of_time": 2, "jabu_jabu": 1, "zoras_fountain": 2, "sleeping_waterfall": 1,"small_key_shuffle": 5, "boss_key_shuffle": 5, "key_rings": 1, "key_rings_count": 9,
               "shuffle_songs": 3}
    world: SohWorld