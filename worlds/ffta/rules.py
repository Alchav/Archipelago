from worlds.generic.Rules import add_rule, set_rule, forbid_item
from .items import MissionUnlockItems


def set_rules(world) -> None:

    # Set final mission unlock to require all paths based on settings
    if world.options.gate_paths.value == 2:
        add_rule(world.multiworld.get_location("Royal Valley", world.player),
                 lambda state: state.has("Path 1 Complete", world.player))

        add_rule(world.multiworld.get_location("Royal Valley", world.player),
                 lambda state: state.has("Path 2 Complete", world.player))

    elif world.options.gate_paths.value == 3:
        add_rule(world.multiworld.get_location("Royal Valley", world.player),
                 lambda state: state.has("Path 1 Complete", world.player))

        add_rule(world.multiworld.get_location("Royal Valley", world.player),
                 lambda state: state.has("Path 2 Complete", world.player))

        add_rule(world.multiworld.get_location("Royal Valley", world.player),
                 lambda state: state.has("Path 3 Complete", world.player))

    if world.options.final_unlock.value == 1:
        add_rule(world.multiworld.get_entrance("Totema 1", world.player),
                 lambda state: state.has("Water Sigil", world.player))

        add_rule(world.multiworld.get_entrance("Totema 2", world.player),
                 lambda state: state.has("Fire Sigil", world.player))

        add_rule(world.multiworld.get_entrance("Totema 3", world.player),
                 lambda state: state.has("Wind Sigil", world.player))

        add_rule(world.multiworld.get_entrance("Totema 4", world.player),
                 lambda state: state.has("Earth Sigil", world.player))

        add_rule(world.multiworld.get_entrance("Totema 5", world.player),
                 lambda state: state.has("Old Statue", world.player))

    num_gates = world.options.gate_num.value

    if world.options.gate_paths.value == 2:
        num_gates = num_gates + 1

    elif world.options.gate_paths.value == 3:
        num_gates = num_gates + 2

    add_rule(world.multiworld.get_entrance("Gate 2", world.player),
        lambda state: state.has("Magic Trophy", world.player))

    if world.options.gate_items.value == 1:
        add_rule(world.multiworld.get_entrance("Gate 2", world.player),
            lambda state: state.has("Fight Trophy", world.player))

    elif world.options.gate_items.value == 2:
        add_rule(world.multiworld.get_entrance("Dispatch Gate 2", world.player),
                 lambda state: state.has("Fight Trophy", world.player))

    if num_gates == 1:
        return

    add_rule(world.multiworld.get_entrance("Gate 3", world.player),
             lambda state: state.has("Magic Medal", world.player))

    if world.options.gate_items.value == 1:
        add_rule(world.multiworld.get_entrance("Gate 3", world.player),
                 lambda state: state.has("Ancient Medal", world.player))

    elif world.options.gate_items.value == 2:
        add_rule(world.multiworld.get_entrance("Dispatch Gate 3", world.player),
                 lambda state: state.has("Ancient Medal", world.player))

    if num_gates == 2:
        return

    add_rule(world.multiworld.get_entrance("Gate 4", world.player),
             lambda state: state.has("Choco Bread", world.player))

    if world.options.gate_items.value == 1:
        add_rule(world.multiworld.get_entrance("Gate 4", world.player),
                 lambda state: state.has("Choco Gratin", world.player))

    elif world.options.gate_items.value == 2:
        add_rule(world.multiworld.get_entrance("Dispatch Gate 4", world.player),
                 lambda state: state.has("Choco Gratin", world.player))

    if num_gates == 3:
        return

    add_rule(world.multiworld.get_entrance("Gate 5", world.player),
             lambda state: state.has("Black Thread", world.player))

    if world.options.gate_items.value == 1:
        add_rule(world.multiworld.get_entrance("Gate 5", world.player),
                 lambda state: state.has("White Thread", world.player))

    elif world.options.gate_items.value == 2:
        add_rule(world.multiworld.get_entrance("Dispatch Gate 5", world.player),
                 lambda state: state.has("White Thread", world.player))

    if num_gates == 4:
        return

    add_rule(world.multiworld.get_entrance("Gate 6", world.player),
             lambda state: state.has("Thunderstone", world.player))

    if world.options.gate_items.value == 1:
        add_rule(world.multiworld.get_entrance("Gate 6", world.player),
                 lambda state: state.has("Stormstone", world.player))

    elif world.options.gate_items.value == 2:
        add_rule(world.multiworld.get_entrance("Dispatch Gate 6", world.player),
                 lambda state: state.has("Stormstone", world.player))

    if num_gates == 5:
        return

    add_rule(world.multiworld.get_entrance("Gate 7", world.player),
             lambda state: state.has("Ahriman Eye", world.player))

    if world.options.gate_items.value == 1:
        add_rule(world.multiworld.get_entrance("Gate 7", world.player),
                 lambda state: state.has("Ahriman Wing", world.player))

    elif world.options.gate_items.value == 2:
        add_rule(world.multiworld.get_entrance("Dispatch Gate 7", world.player),
                 lambda state: state.has("Ahriman Wing", world.player))

    if num_gates == 6:
        return

    add_rule(world.multiworld.get_entrance("Gate 8", world.player),
             lambda state: state.has("Magic Cloth", world.player))

    if world.options.gate_items.value == 1:
        add_rule(world.multiworld.get_entrance("Gate 8", world.player),
                 lambda state: state.has("Magic Cotton", world.player))

    elif world.options.gate_items.value == 2:
        add_rule(world.multiworld.get_entrance("Dispatch Gate 8", world.player),
                 lambda state: state.has("Magic Cotton", world.player))

    if num_gates == 7:
        return

    add_rule(world.multiworld.get_entrance("Gate 9", world.player),
             lambda state: state.has("Adaman Alloy", world.player))

    if world.options.gate_items.value == 1:
        add_rule(world.multiworld.get_entrance("Gate 9", world.player),
                 lambda state: state.has("Mysidia Alloy", world.player))

    elif world.options.gate_items.value == 2:
        add_rule(world.multiworld.get_entrance("Dispatch Gate 9", world.player),
                 lambda state: state.has("Mysidia Alloy", world.player))

    if num_gates == 8:
        return

    add_rule(world.multiworld.get_entrance("Gate 10", world.player),
             lambda state: state.has("Elda's Cup", world.player))

    if world.options.gate_items.value == 1:
        add_rule(world.multiworld.get_entrance("Gate 10", world.player),
                 lambda state: state.has("Gold Vessel", world.player))

    elif world.options.gate_items.value == 2:
        add_rule(world.multiworld.get_entrance("Dispatch Gate 10", world.player),
                 lambda state: state.has("Gold Vessel", world.player))

    if num_gates == 9:
        return

    add_rule(world.multiworld.get_entrance("Gate 11", world.player),
             lambda state: state.has("Kiddy Bread", world.player))

    if world.options.gate_items.value == 1:
        add_rule(world.multiworld.get_entrance("Gate 11", world.player),
                 lambda state: state.has("Grownup Bread", world.player))

    elif world.options.gate_items.value == 2:
        add_rule(world.multiworld.get_entrance("Dispatch Gate 11", world.player),
                 lambda state: state.has("Grownup Bread", world.player))

    if num_gates == 10:
        return

    add_rule(world.multiworld.get_entrance("Gate 12", world.player),
             lambda state: state.has("Danbukwood", world.player))

    if world.options.gate_items.value == 1:
        add_rule(world.multiworld.get_entrance("Gate 12", world.player),
                 lambda state: state.has("Moonwood", world.player))

    elif world.options.gate_items.value == 2:
        add_rule(world.multiworld.get_entrance("Dispatch Gate 12", world.player),
                 lambda state: state.has("Moonwood", world.player))

    if num_gates == 11:
        return

    add_rule(world.multiworld.get_entrance("Gate 13", world.player),
             lambda state: state.has("Dragon Bone", world.player))

    if world.options.gate_items.value == 1:
        add_rule(world.multiworld.get_entrance("Gate 13", world.player),
                 lambda state: state.has("Animal Bone", world.player))

    elif world.options.gate_items.value == 2:
        add_rule(world.multiworld.get_entrance("Dispatch Gate 13", world.player),
                 lambda state: state.has("Animal Bone", world.player))

    if num_gates == 12:
        return

    add_rule(world.multiworld.get_entrance("Gate 14", world.player),
             lambda state: state.has("Magic Fruit", world.player))

    if world.options.gate_items.value == 1:
        add_rule(world.multiworld.get_entrance("Gate 14", world.player),
                 lambda state: state.has("Power Fruit", world.player))

    elif world.options.gate_items.value == 2:
        add_rule(world.multiworld.get_entrance("Dispatch Gate 14", world.player),
                 lambda state: state.has("Power Fruit", world.player))

    if num_gates == 13:
        return

    add_rule(world.multiworld.get_entrance("Gate 15", world.player),
             lambda state: state.has("Malboro Wine", world.player))

    if world.options.gate_items.value == 1:
        add_rule(world.multiworld.get_entrance("Gate 15", world.player),
                 lambda state: state.has("Gedegg Soup", world.player))

    elif world.options.gate_items.value == 2:
        add_rule(world.multiworld.get_entrance("Dispatch Gate 15", world.player),
                 lambda state: state.has("Gedegg Soup", world.player))

    if num_gates == 14:
        return

    add_rule(world.multiworld.get_entrance("Gate 16", world.player),
             lambda state: state.has("Encyclopedia", world.player))

    if world.options.gate_items.value == 1:
        add_rule(world.multiworld.get_entrance("Gate 16", world.player),
                 lambda state: state.has("Dictionary", world.player))

    elif world.options.gate_items.value == 2:
        add_rule(world.multiworld.get_entrance("Dispatch Gate 16", world.player),
                 lambda state: state.has("Dictionary", world.player))

    if num_gates == 15:
        return

    add_rule(world.multiworld.get_entrance("Gate 17", world.player),
             lambda state: state.has("Rat Tail", world.player))

    if world.options.gate_items.value == 1:
        add_rule(world.multiworld.get_entrance("Gate 17", world.player),
                 lambda state: state.has("Rabbit Tail", world.player))

    elif world.options.gate_items.value == 2:
        add_rule(world.multiworld.get_entrance("Dispatch Gate 17", world.player),
                 lambda state: state.has("Rabbit Tail", world.player))

    if num_gates == 16:
        return

    add_rule(world.multiworld.get_entrance("Gate 18", world.player),
             lambda state: state.has("Stasis Rope", world.player))

    if world.options.gate_items.value == 1:
        add_rule(world.multiworld.get_entrance("Gate 18", world.player),
                 lambda state: state.has("Mythril Pick", world.player))

    elif world.options.gate_items.value == 2:
        add_rule(world.multiworld.get_entrance("Dispatch Gate 18", world.player),
                 lambda state: state.has("Mythril Pick", world.player))

    if num_gates == 17:
        return

    add_rule(world.multiworld.get_entrance("Gate 19", world.player),
             lambda state: state.has("Clock Gear", world.player))

    if world.options.gate_items.value == 1:
        add_rule(world.multiworld.get_entrance("Gate 19", world.player),
                 lambda state: state.has("Gun Gear", world.player))

    elif world.options.gate_items.value == 2:
        add_rule(world.multiworld.get_entrance("Dispatch Gate 19", world.player),
                 lambda state: state.has("Gun Gear", world.player))

    if num_gates == 18:
        return

    add_rule(world.multiworld.get_entrance("Gate 20", world.player),
             lambda state: state.has("Blood Shawl", world.player))

    if world.options.gate_items.value == 1:
        add_rule(world.multiworld.get_entrance("Gate 20", world.player),
                 lambda state: state.has("Blood Apple", world.player))

    elif world.options.gate_items.value == 2:
        add_rule(world.multiworld.get_entrance("Dispatch Gate 20", world.player),
                 lambda state: state.has("Blood Apple", world.player))

    if num_gates == 19:
        return

    add_rule(world.multiworld.get_entrance("Gate 21", world.player),
             lambda state: state.has("Eldagusto", world.player))

    if world.options.gate_items.value == 1:
        add_rule(world.multiworld.get_entrance("Gate 21", world.player),
                 lambda state: state.has("Cyril Ice", world.player))

    elif world.options.gate_items.value == 2:
        add_rule(world.multiworld.get_entrance("Dispatch Gate 21", world.player),
                 lambda state: state.has("Cyril Ice", world.player))

    if num_gates == 20:
        return

    add_rule(world.multiworld.get_entrance("Gate 22", world.player),
             lambda state: state.has("Crystal", world.player))

    if world.options.gate_items.value == 1:
        add_rule(world.multiworld.get_entrance("Gate 22", world.player),
                 lambda state: state.has("Trichord", world.player))

    elif world.options.gate_items.value == 2:
        add_rule(world.multiworld.get_entrance("Dispatch Gate 22", world.player),
                 lambda state: state.has("Trichord", world.player))

    if num_gates == 21:
        return

    add_rule(world.multiworld.get_entrance("Gate 23", world.player),
             lambda state: state.has("Tranquil Box", world.player))

    if world.options.gate_items.value == 1:
        add_rule(world.multiworld.get_entrance("Gate 23", world.player),
                 lambda state: state.has("Flower Vase", world.player))

    elif world.options.gate_items.value == 2:
        add_rule(world.multiworld.get_entrance("Dispatch Gate 23", world.player),
                 lambda state: state.has("Flower Vase", world.player))

    if num_gates == 22:
        return

    add_rule(world.multiworld.get_entrance("Gate 24", world.player),
             lambda state: state.has("Cat's Tears", world.player))

    if world.options.gate_items.value == 1:
        add_rule(world.multiworld.get_entrance("Gate 24", world.player),
                 lambda state: state.has("Dame's Blush", world.player))

    elif world.options.gate_items.value == 2:
        add_rule(world.multiworld.get_entrance("Dispatch Gate 24", world.player),
                 lambda state: state.has("Dame's Blush", world.player))

    if num_gates == 23:
        return

    add_rule(world.multiworld.get_entrance("Gate 25", world.player),
             lambda state: state.has("Justice Badge", world.player))

    if world.options.gate_items.value == 1:
        add_rule(world.multiworld.get_entrance("Gate 25", world.player),
                 lambda state: state.has("Friend Badge", world.player))

    elif world.options.gate_items.value == 2:
        add_rule(world.multiworld.get_entrance("Dispatch Gate 25", world.player),
                 lambda state: state.has("Friend Badge", world.player))

    if num_gates == 24:
        return

    add_rule(world.multiworld.get_entrance("Gate 26", world.player),
             lambda state: state.has("Love Potion", world.player))

    if world.options.gate_items.value == 1:
        add_rule(world.multiworld.get_entrance("Gate 26", world.player),
                 lambda state: state.has("Tonberry Lamp", world.player))

    elif world.options.gate_items.value == 2:
        add_rule(world.multiworld.get_entrance("Dispatch Gate 26", world.player),
                 lambda state: state.has("Tonberry Lamp", world.player))

    if num_gates == 25:
        return

    add_rule(world.multiworld.get_entrance("Gate 27", world.player),
             lambda state: state.has("Runba's Tale", world.player))

    if world.options.gate_items.value == 1:
        add_rule(world.multiworld.get_entrance("Gate 27", world.player),
                 lambda state: state.has("The Hero Gaol", world.player))

    elif world.options.gate_items.value == 2:
        add_rule(world.multiworld.get_entrance("Dispatch Gate 27", world.player),
                 lambda state: state.has("The Hero Gaol", world.player))

    if num_gates == 26:
        return

    add_rule(world.multiworld.get_entrance("Gate 28", world.player),
             lambda state: state.has("Mind Ceffyl", world.player))

    if world.options.gate_items.value == 1:
        add_rule(world.multiworld.get_entrance("Gate 28", world.player),
                 lambda state: state.has("Body Ceffyl", world.player))

    elif world.options.gate_items.value == 2:
        add_rule(world.multiworld.get_entrance("Dispatch Gate 28", world.player),
                 lambda state: state.has("Body Ceffyl", world.player))

    if num_gates == 27:
        return

    add_rule(world.multiworld.get_entrance("Gate 29", world.player),
             lambda state: state.has("Ancient Bills", world.player))

    if world.options.gate_items.value == 1:
        add_rule(world.multiworld.get_entrance("Gate 29", world.player),
                 lambda state: state.has("Ancient Coins", world.player))

    elif world.options.gate_items.value == 2:
        add_rule(world.multiworld.get_entrance("Dispatch Gate 29", world.player),
                 lambda state: state.has("Ancient Coins", world.player))

    if num_gates == 28:
        return

    add_rule(world.multiworld.get_entrance("Gate 30", world.player),
             lambda state: state.has("Blue Rose", world.player))

    if world.options.gate_items.value == 1:
        add_rule(world.multiworld.get_entrance("Gate 30", world.player),
                 lambda state: state.has("White Flowers", world.player))

    elif world.options.gate_items.value == 2:
        add_rule(world.multiworld.get_entrance("Dispatch Gate 30", world.player),
                 lambda state: state.has("White Flowers", world.player))

    if num_gates == 29:
        return

    add_rule(world.multiworld.get_entrance("Gate 31", world.player),
             lambda state: state.has("Gysahl Greens", world.player))

    if world.options.gate_items.value == 1:
        add_rule(world.multiworld.get_entrance("Gate 31", world.player),
                 lambda state: state.has("Chocobo Egg", world.player))

    elif world.options.gate_items.value == 2:
        add_rule(world.multiworld.get_entrance("Dispatch Gate 31", world.player),
                 lambda state: state.has("Chocobo Egg", world.player))

    if num_gates == 30 or world.options.final_unlock.value == 1:
        return

    add_rule(world.multiworld.get_entrance("Gate 32", world.player),
             lambda state: state.has("Delta Fang", world.player))

    if world.options.gate_items.value == 1:
        add_rule(world.multiworld.get_entrance("Gate 32", world.player),
                 lambda state: state.has("Esteroth", world.player))

    elif world.options.gate_items.value == 2:
        add_rule(world.multiworld.get_entrance("Dispatch Gate 32", world.player),
                 lambda state: state.has("Esteroth", world.player))

    if num_gates == 31:
        return

    add_rule(world.multiworld.get_entrance("Gate 33", world.player),
             lambda state: state.has("Moon Bloom", world.player))

    if world.options.gate_items.value == 1:
        add_rule(world.multiworld.get_entrance("Gate 33", world.player),
                 lambda state: state.has("Telaq Flowers", world.player))

    elif world.options.gate_items.value == 2:
        add_rule(world.multiworld.get_entrance("Dispatch Gate 33", world.player),
                 lambda state: state.has("Telaq Flowers", world.player))

    if num_gates == 32:
        return

