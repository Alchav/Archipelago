from .Types import RegionData, ExitData
from .Rules import *

max_keys = 8

# Define regions, their connections, and required checks for those connections
def get_region_table(player):
    return {
        # Veggieville
        "Veggieville": RegionData(exits=[
            ExitData("Weapon Woods"),
            ExitData("Layer Lane 1",
                     rule=lambda state: has_sword(state, player)),
            ExitData("Rocky Ramp 1",
                     rule=lambda state: state.has("Deliver Fertilizer", player)),
            ExitData("Grim Graveyard 1",
                     rule=lambda state: state.has("Deliver Goop", player)),
            ExitData("Mysterious Mafia Base 1",
                     rule=lambda state: state.has("Deliver Laser Pointer", player)),
        ]),

        # Weapon Woods
        "Weapon Woods": RegionData(exits=[
            ExitData("Bomb Bunker 1",
                     rule=lambda state: has_shovel(state, player))
        ]),

        # Layer Lane
        "Layer Lane 1": RegionData(exits=[
            ExitData("Bustling Barn 1"),
            ExitData("Layer Lane 2",
                     rule=lambda state: state.has("Defeat King Pig", player))
        ]),
        "Layer Lane 2": RegionData(),

        # Bustling Barn
        "Bustling Barn 1": RegionData(exits=[
            ExitData("Bustling Barn 2",
                     rule=lambda state: state.has("Tier 3 Sub", player))
        ]),
        "Bustling Barn 2": RegionData(exits=[
            ExitData("Bustling Barn 3",
                     rule=lambda state: state.has("Watering Can", player)),
            ExitData("Bustling Barn 5",
                     rule=lambda state: state.has("Key", player, max_keys))
        ]),
        "Bustling Barn 3": RegionData(exits=[
            ExitData("Bustling Barn 4",
                     rule=lambda state: state.has("Boom Boots", player)),
        ]),
        "Bustling Barn 4": RegionData(),
        "Bustling Barn 5": RegionData(exits=[
            ExitData("Bustling Barn 6",
                     rule=lambda state: state.has_all(["Watering Can", "Boom Boots"], player))
        ]),
        "Bustling Barn 6": RegionData([
            ExitData("Bustling Barn 7",
                     rule=lambda state: state.has("Defeat King Pig", player))
        ]),
        "Bustling Barn 7": RegionData(),

        # Rocky Ramp
        "Rocky Ramp 1": RegionData([
            ExitData("Plain Plains 1")
        ]),
        "Rocky Ramp 2": RegionData(),

        # Plain Plains
        "Plain Plains 1": RegionData([
            ExitData("Forsaken Farmhouse 1",
                     rule=lambda state: state.has("Stool", player)),
            ExitData("Forgotten Forest 1",
                     rule=lambda state: state.has("Deliver Fork", player)),
        ]),

        # Forsaken Farmhouse
        "Forsaken Farmhouse 1": RegionData(exits=[
            ExitData("Forsaken Farmhouse 2",
                     rule=lambda state: state.has_all(["Boom Boots", "Watering Can"], player)),
            # Don't need to require every key because there is another lock behind this one
            ExitData("Forsaken Farmhouse 3",
                     rule=lambda state: state.has("Key", player, max_keys - 1)),
            ExitData("Forsaken Farmhouse 5",
                     rule=lambda state: state.has_all(["Watering Can", "Move Mittens"], player)),
            ExitData("Idle Icebox 1",
                     rule=lambda state: state.has_all(["Boom Boots", "Watering Can"], player)),
        ]),
        "Forsaken Farmhouse 2": RegionData(),
        "Forsaken Farmhouse 3": RegionData(exits=[
            ExitData("Forsaken Farmhouse 4",
                     rule=lambda state: state.has("Key", player, max_keys))
        ]),
        "Forsaken Farmhouse 4": RegionData(),
        "Forsaken Farmhouse 5": RegionData(exits=[
            ExitData("Forsaken Farmhouse 6",
                     rule=lambda state: state.has("Boom Boots", player)),
            ExitData("Forsaken Farmhouse 7",
                     rule=lambda state: state.has("Boom Boots", player) and state.has("Key", player, max_keys))
        ]),
        "Forsaken Farmhouse 6": RegionData(),
        "Forsaken Farmhouse 7": RegionData(exits=[
            ExitData("Forsaken Farmhouse 8",
                     rule=lambda state: state.has("Defeat Rotten Cat Apple", player)),
        ]),
        "Forsaken Farmhouse 8": RegionData(),

        # Idle Icebox
        "Idle Icebox 1": RegionData(),

        # Forgotten Forest
        "Forgotten Forest 1": RegionData(exits=[
            ExitData("Rocky Ramp 2"),
            ExitData("Forgotten Forest 2",
                     rule=lambda state: state.has_all(["Boom Boots", "Watering Can"], player)),
            ExitData("Forgotten Forest 4",
                     rule=lambda state: state.has_all(["Boom Boots", "Watering Can", "Move Mittens"], player) and state.has("Key", player, max_keys)),
            ExitData("Forgotten Forest 6",
                     rule=lambda state: state.has_all(["Watering Can", "Potted Petalportal"], player) and state.has("Key", player, max_keys)),
        ]),
        "Forgotten Forest 2": RegionData(exits=[
            ExitData("Forgotten Forest 3",
                     rule=lambda state: has_sword(state, player)),
        ]),
        "Forgotten Forest 3": RegionData(),
        "Forgotten Forest 4": RegionData(exits=[
            ExitData("Forgotten Forest 5",
                     rule=lambda state: has_sword(state, player)),
        ]),
        "Forgotten Forest 5": RegionData(),
        "Forgotten Forest 6": RegionData(exits=[
            ExitData("Forgotten Forest 7",
                     rule=lambda state: state.has("Defeat Stag", player)),
        ]),
        "Forgotten Forest 7": RegionData(),

        # Grim Graveyard
        "Grim Graveyard 1": RegionData(exits=[
            ExitData("Grim Graveyard 2",
                     rule=lambda state: state.has_all(["Watering Can", "Boom Boots"], player))
        ]),
        "Grim Graveyard 2": RegionData(exits=[
            ExitData("Grim Graveyard 3",
                     rule=lambda state: state.has_all(["Move Mittens", "Potted Petalportal"], player))
        ]),
        "Grim Graveyard 3": RegionData(),

        # Bomb Bunker
        "Bomb Bunker 1": RegionData(exits=[
            ExitData("Bomb Bunker 2",
                     rule=lambda state: state.has("Watering Can", player)),
            # Only require 1 key because the player can immediately get a replacement key from the
            # 2nd bedroom
            ExitData("Bomb Bunker 3",
                     rule=lambda state: state.has("Watering Can", player) and state.has("Key", player, 1))
        ]),
        "Bomb Bunker 2": RegionData(),
        "Bomb Bunker 3": RegionData(exits=[
            ExitData("Bomb Bunker 4"),
            ExitData("Bomb Bunker 5",
                     rule=lambda state: state.has("Key", player, max_keys))
        ]),
        "Bomb Bunker 4": RegionData(),
        "Bomb Bunker 5": RegionData(exits=[
            ExitData("Bomb Bunker 6",
                     rule=lambda state: state.has_all(["Hazmat Suit", "Move Mittens", "Boom Boots"], player))
        ]),
        "Bomb Bunker 6": RegionData(exits=[
            ExitData("Bomb Bunker 7",
                     rule=lambda state: state.has("Defeat Liz", player))
        ]),
        "Bomb Bunker 7": RegionData(),

        # Mysterious Mafia Base
        "Mysterious Mafia Base 1": RegionData(exits=[
            ExitData("Mysterious Mafia Base 2",
                     rule=lambda state: state.has_all(["Watering Can", "Potted Petalportal"], player))
        ]),
        "Mysterious Mafia Base 2": RegionData(exits=[
            ExitData("Mysterious Mafia Base 3",
                     rule=lambda state: state.has("Boom Boots", player))
        ]),
        "Mysterious Mafia Base 3": RegionData(exits=[
            ExitData("Mysterious Mafia Base 4",
                     rule=lambda state: state.has("Move Mittens", player))
        ]),
        "Mysterious Mafia Base 4": RegionData(),
    }