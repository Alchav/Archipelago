from BaseClasses import MultiWorld
from ..AutoWorld import LogicMixin
from ..generic.Rules import set_rule


class SpireLogic(LogicMixin):
    def _spire_has_items(self, player: int, amount: int) -> bool:
        count: int = self.count("Relic", player) + self.count("Boss Relic", player) + self.count("Card Draw", player) + self.count("Rare Card Draw", player)
        return count >= amount

    def _spire_has_relics(self, player: int, amount: int) -> bool:
        count: int = self.count("Relic", player) + self.count("Boss Relic", player)
        return count >= amount

    def _spire_has_cards(self, player: int, amount: int) -> bool:
        count = self.count("Card Draw", player) + self.count("Rare Card Draw", player)
        return count >= amount


def set_rules(world: MultiWorld, player: int):

    # # Act 1 Card Draws
    # set_rule(world.get_location("Card Draw 1", player), lambda state: True)
    # set_rule(world.get_location("Card Draw 2", player), lambda state: state._spire_has_items(player, 1))
    # set_rule(world.get_location("Card Draw 3", player), lambda state: state._spire_has_items(player, 3))
    # set_rule(world.get_location("Card Draw 4", player), lambda state: state._spire_has_items(player, 4))
    # set_rule(world.get_location("Card Draw 5", player), lambda state: state._spire_has_items(player, 6))
    #
    # # Act 1 Relics
    # set_rule(world.get_location("Relic 1", player), lambda state: state._spire_has_items(player, 2))
    # set_rule(world.get_location("Relic 2", player), lambda state: state._spire_has_items(player, 5))
    # set_rule(world.get_location("Relic 3", player), lambda state: state._spire_has_items(player, 1))
    #
    # # Act 1 Boss Event
    # set_rule(world.get_location("Act 1 Boss", player), lambda state: state._spire_has_items(player, 7))
    #
    # # Act 1 Boss Rewards
    # set_rule(world.get_location("Rare Card Draw 1", player), lambda state: state._spire_has_items(player, 8))
    # set_rule(world.get_location("Boss Relic 1", player), lambda state: state._spire_has_items(player, 8))
    #
    # # Act 2 Card Draws
    # set_rule(world.get_location("Card Draw 6", player), lambda state: state._spire_has_items(player, 10))
    # set_rule(world.get_location("Card Draw 7", player), lambda state: state._spire_has_items(player, 12))
    # set_rule(world.get_location("Card Draw 8", player), lambda state: state._spire_has_items(player, 13))
    # set_rule(world.get_location("Card Draw 9", player), lambda state: state._spire_has_items(player, 15))
    # set_rule(world.get_location("Card Draw 10", player), lambda state: state._spire_has_items(player, 16))
    #
    # # Act 2 Relics
    # set_rule(world.get_location("Relic 4", player), lambda state: state._spire_has_items(player, 11))
    # set_rule(world.get_location("Relic 5", player), lambda state: state._spire_has_items(player, 14))
    # set_rule(world.get_location("Relic 6", player), lambda state: state._spire_has_items(player, 17))
    #
    # # Act 2 Boss Event
    # set_rule(world.get_location("Act 2 Boss", player), lambda state: state._spire_has_items(player, 18))
    #
    # # Act 2 Boss Rewards
    # set_rule(world.get_location("Rare Card Draw 2", player), lambda state: state._spire_has_items(player, 18))
    # set_rule(world.get_location("Boss Relic 2", player), lambda state: state._spire_has_items(player, 18))
    #
    # # Act 3 Card Draws
    # set_rule(world.get_location("Card Draw 11", player), lambda state: state._spire_has_items(player, 20))
    # set_rule(world.get_location("Card Draw 12", player), lambda state: state._spire_has_items(player, 22))
    # set_rule(world.get_location("Card Draw 13", player), lambda state: state._spire_has_items(player, 23))
    # set_rule(world.get_location("Card Draw 14", player), lambda state: state._spire_has_items(player, 25))
    set_rule(world.get_location("Card Draw 15", player), lambda state: state._spire_has_items(player, 25))
    #
    # # Act 3 Relics
    # set_rule(world.get_location("Relic 7", player), lambda state: state._spire_has_items(player, 21))
    # set_rule(world.get_location("Relic 8", player), lambda state: state._spire_has_items(player, 24))
    # set_rule(world.get_location("Relic 9", player), lambda state: state._spire_has_items(player, 27))
    set_rule(world.get_location("Relic 10", player), lambda state: state._spire_has_items(player, 25))

    # Act 3 Boss Event
    set_rule(world.get_location("Act 3 Boss", player), lambda state: state._spire_has_items(player, 26))

    set_rule(world.get_location("Heart Room", player), lambda state: state._spire_has_items(player, 26))

    world.completion_condition[player] = lambda state: state.has("Victory", player)
