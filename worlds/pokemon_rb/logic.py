from ..AutoWorld import LogicMixin
import worlds.pokemon_rb.poke_data as poke_data


class PokemonLogic(LogicMixin):
    def _pokemon_rb_can_surf(self, player):
        return (((self.has("HM03 Surf", player) and self._can_learn_hm("10000", player)) or self.has("Flippers", player)) and
                (self.has("Soul Badge", player) or self.has(self.world.worlds[player].extra_badges.get("Surf"), player)
                 or self.world.badges_needed_for_hm_moves[player].value == 0))

    def _pokemon_rb_can_cut(self, player):
        return (self.has("HM01 Cut", player and self._can_learn_hm("100", player)) or self.has("Master Sword", player)) and (self.has("Cascade Badge", player)
                or self.has(self.world.worlds[player].extra_badges.get("Cut"), player) or
                self.world.badges_needed_for_hm_moves[player].value == 0)

    def _pokemon_rb_can_fly(self, player):
        return ((self.has("HM02 Fly", player) and self._can_learn_hm("1000", player)) or self.has("Flute", player)) and (self.has("Thunder Badge", player) or
                self.has(self.world.worlds[player].extra_badges.get("Fly"), player) or
                self.world.badges_needed_for_hm_moves[player].value == 0)

    def _pokemon_rb_can_strength(self, player):
        return ((self.has("HM04 Strength", player) and self._can_learn_hm("100000", player)) or self.has("Titan's Mitt", player)) and\
               (self.has("Rainbow Badge", player) or self.has(self.world.worlds[player].extra_badges.get("Strength"), player)
                or self.world.badges_needed_for_hm_moves[player].value == 0)

    def _pokemon_rb_can_flash(self, player):
        return ((self.has("HM05 Flash", player) and self._can_learn_hm("1000000", player)) or self.has("Lamp", player)) and (self.has("Boulder Badge", player) or
                self.has(self.world.worlds[player].extra_badges.get("Flash"), player) or self.world.badges_needed_for_hm_moves[player].value == 0)

    def _can_learn_hm(self, move, player):
        for pokemon, data in self.world.worlds[player].local_poke_data.items():
            if self.has(pokemon, player) and data["tms"][6] & int(move, 2):
                return True
        return False

    def _pokemon_rb_can_get_hidden_items(self, player):
        return self.has("Item Finder", player) or not self.world.require_item_finder[player].value

    def _pokemon_rb_cerulean_cave(self, count, player):
        return len([item for item in
                    ["Boulder Badge", "Cascade Badge", "Thunder Badge", "Rainbow Badge", "Soul Badge", "Marsh Badge",
                     "Volcano Badge", "Earth Badge", "Bicycle", "Silph Scope", "Item Finder", "Super Rod", "Good Rod",
                     "Old Rod", "Lift Key", "Card Key", "Town Map", "Coin Case", "S.S. Ticket", "Secret Key",
                     "Mansion Key", "Safari Pass", "Plant Key", "Hideout Key", "HM01 Cut", "HM02 Fly", "HM03 Surf",
                     "HM04 Strength", "HM05 Flash"] if self.has(item, player)]) >= count

    def _pokemon_rb_can_pass_guards(self, player):
        return self.has("Tea", player)

    def _pokemon_rb_has_badges(self, count, player):
        return (self.has("Boulder Badge", player) + self.has("Cascade Badge", player)
                + self.has("Thunder Badge", player) + self.has("Rainbow Badge", player)
                + self.has("Marsh Badge", player) + self.has("Soul Badge", player)
                + self.has("Volcano Badge", player) + self.has("Earth Badge", player)) >= count

    def _pokemon_rb_has_pokemon(self, count, player):
        obtained_pokemon = set()
        for pokemon in poke_data.pokemon_data.keys():
            if self.has(pokemon, player) or self.has(f"Static {pokemon}", player):
                obtained_pokemon.add(pokemon)

        return len(obtained_pokemon) >= count