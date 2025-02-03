from .Types import LocData
from .Rules import *

def get_location_table(player):
    return {
        # Veggieville
        "Veggieville - Deliver Fertilizer": LocData(
            None, region="Veggieville",
            rule=lambda state: state.has("Fertilizer", player), event_name="Deliver Fertilizer"),
        "Veggieville - Deliver Fork": LocData(
            None, region="Veggieville",
            rule=lambda state: state.has("Deliver Fertilizer", player) and has_fork(state, player), event_name="Deliver Fork"),
        "Veggieville - Deliver Goop": LocData(
            None, region="Veggieville",
            rule=lambda state: state.has_all(["Deliver Fork", "Green Goop"], player), event_name="Deliver Goop"),
        "Veggieville - Deliver Laser Pointer": LocData(
            None, region="Veggieville",
            rule=lambda state: state.has_all(["Deliver Goop", "Laser Pointer"], player), event_name="Deliver Laser Pointer"),
        "Veggieville - Steal From Lemon": LocData(1, region="Veggieville"),
        "Veggieville - Florist Reward": LocData(
            2, region="Veggieville",
            rule=lambda state: state.has("Flower", player)),
        "Veggieville - Water Florist's Flower": LocData(
            4, region="Veggieville",
            rule=lambda state: state.has("Watering Can", player)),
        "Veggieville - Mailbox (Free Item)": LocData(5, region="Veggieville"),
        "Veggieville - Mailbox (Lost Cat Reward)": LocData(
            6, region="Veggieville",
            rule=lambda state: state.has("Lost Cat Apple", player)),

        # Weapon Woods
        "Weapon Woods - Soil Sword Patch": LocData(
            101, region="Weapon Woods",
            rule=lambda state: state.has("Watering Can", player)),
        "Weapon Woods - Murder Jerry": LocData(
            102, region="Weapon Woods",
            rule=lambda state: has_sword(state, player)),
        "Weapon Woods - Babysitter Reward": LocData(
            103, region="Weapon Woods",
            rule=lambda state: state.has("Lost Carrot Baby", player)),

        # Layer Lane
        "Layer Lane - Trophy Corner": LocData(201, region="Layer Lane 1"),
        "Layer Lane - Sandwich Stall": LocData(202, region="Layer Lane 1"),
        "Layer Lane - Shady Blueberry": LocData(
            203, region="Layer Lane 2",
            rule=lambda state: state.has("Defeat King Pig", player)),
        "Layer Lane - Shady Carrot": LocData(
            204, region="Layer Lane 2",
            rule=lambda state: state.has("Defeat Rotten Cat Apple", player)),
        "Layer Lane - Invest in Real Estate": LocData(
            205, region="Layer Lane 1",
            rule=lambda state: state.has("Leaf", player)),
        "Layer Lane - Edgar Reward": LocData(
            206, region="Layer Lane 1",
            rule=lambda state: state.has("Hair Dye", player)),

        # Bustling Barn
        "Bustling Barn - Barn Key": LocData(None, region="Bustling Barn 4", event_name="Key"),
        "Bustling Barn - Defeat King Pig": LocData(None, region="Bustling Barn 6", event_name="Defeat King Pig"),
        "Bustling Barn - Boom Boots Room": LocData(302, region="Bustling Barn 3"),
        "Bustling Barn - Past The King Pig": LocData(304, region="Bustling Barn 7"),
        "Bustling Barn - slayQueen32 Reward": LocData(
            305, region="Bustling Barn 1",
            rule=lambda state: state.has("Defeat King Pig", player)),
        "Bustling Barn - Bald Beet Reward": LocData(
            306, region="Bustling Barn 6",
            rule=lambda state: state.has_all(["Wood", "Defeat King Pig"], player)),

        # Plain Plains
        "Plain Plains - Trash Can": LocData(401, region="Plain Plains 1"),

        # Forsaken Farmhouse
        "Forsaken Farmhouse - Defeat Rotten Cat Apple": LocData(None, region="Forsaken Farmhouse 7", event_name="Defeat Rotten Cat Apple"),
        "Forsaken Farmhouse - Restart Generator": LocData(None, region="Forsaken Farmhouse 8", event_name="Restart Generator"),
        "Forsaken Farmhouse - Donut Loot": LocData(501, region="Forsaken Farmhouse 1"),
        "Forsaken Farmhouse - Behind Key Block": LocData(502, region="Forsaken Farmhouse 3"),
        "Forsaken Farmhouse - Boom Boots Puzzle": LocData(503, region="Forsaken Farmhouse 2"),
        "Forsaken Farmhouse - Move Mittens Room": LocData(504, region="Forsaken Farmhouse 4"),
        "Forsaken Farmhouse - Cherrynapper": LocData(
            505, region="Forsaken Farmhouse 6",
            # If you defeat the boss, all farmhouse enemies despawn. To prevent a softlock, we 
            # report this location as checked when the player checks the "Boss Arena" location.
            rule=lambda state: has_sword(state, player) or state.has("Defeat Rotten Cat Apple", player)),
        "Forsaken Farmhouse - Boss Arena": LocData(
            506, region="Forsaken Farmhouse 7",
            rule=lambda state: state.has("Defeat Rotten Cat Apple", player)),
        "Forsaken Farmhouse - Generator Room": LocData(507, region="Forsaken Farmhouse 8"),

        # Idle Icebox
        "Idle Icebox - Deb's Key": LocData(None, region="Idle Icebox 1", event_name="Key"),
        "Idle Icebox - Nurse Berry's Key": LocData(
            None, region="Idle Icebox 1",
            rule=lambda state: state.has_all(["Face Mask", "Medicine", "Bandage"], player),
            event_name="Key"),
        "Idle Icebox - Carly's Key": LocData(
            None, region="Idle Icebox 1",
            rule=lambda state: state.has("Lost Cherry Baby", player),
            event_name="Key"),
        "Idle Icebox - Deb Reward": LocData(
            601, region="Idle Icebox 1",
            rule=lambda state: state.has("Restart Generator", player)),
        "Idle Icebox - Pickled Gang Reward": LocData(
            602, region="Idle Icebox 1",
            rule=lambda state: state.has_all(["Defeat Rotten Cat Apple", "Hammer"], player)),
        "Idle Icebox - Pops' Reply": LocData(
            603, region="Idle Icebox 1",
            rule=lambda state: state.has("Tot's Letter", player)),
        "Idle Icebox - Pops' Reward": LocData(
            604, region="Idle Icebox 1",
            rule=lambda state: state.has("Tot's Letter", player) and state.can_reach_location("Grim Graveyard - Tots' Reward", player)),

        # Rocky Ramp
        "Rocky Ramp - Bottom of Cliff": LocData(701, region="Rocky Ramp 2"),

        # Forgotten Forest
        "Forgotten Forest - Annie's Key 1": LocData(
            None, region="Forgotten Forest 1",
            rule=lambda state: state.has("Mural Doodle", player),
            event_name="Key"),
        "Forgotten Forest - Annie's Key 2": LocData(
            None, region="Forgotten Forest 1",
            rule=lambda state: state.has_all(["Mural Doodle", "Turnip?"], player),
            event_name="Key"),
        "Forgotten Forest - Defeat Stag": LocData(
            None, region="Forgotten Forest 6",
            # You could theoretically win this fight with just the sword, but let's keep that out of logic for now
            rule=lambda state: state.has("Boom Boots", player),
            event_name="Defeat Stag"),
        "Forgotten Forest - Mural Cave": LocData(801, region="Forgotten Forest 3"),
        "Forgotten Forest - Turnip(?) Field": LocData(802, region="Forgotten Forest 4"),
        "Forgotten Forest - Petalportal Cave": LocData(803, region="Forgotten Forest 5"),
        "Forgotten Forest - Past the Stag": LocData(804, region="Forgotten Forest 7"),
        "Forgotten Forest - Annie Reward": LocData(
            805, region="Forgotten Forest 1",
            rule=lambda state: state.has_all(["Mural Doodle", "Turnip?", "Defeat Stag"], player)),
        "Forgotten Forest - Acorn's Down Payment": LocData(
            806, region="Forgotten Forest 1",
            rule=lambda state: state.has("Defeat Stag", player)),

        # Grim Graveyard
        "Grim Graveyard - Graverobbing": LocData(
            901, region="Grim Graveyard 1",
            rule=lambda state: has_sword(state, player)),
        "Grim Graveyard - Tots' Trade": LocData(902, region="Grim Graveyard 3"),
        "Grim Graveyard - Tots' Request": LocData(903, region="Grim Graveyard 3"),
        "Grim Graveyard - Tots' Reward": LocData(
            904, region="Grim Graveyard 3",
            rule=lambda state: state.has("Pop's Letter", player)),

        # Bomb Bunker
        "Bomb Bunker - Bedroom 1 Key": LocData(None, region="Bomb Bunker 2", event_name="Key"),
        "Bomb Bunker - Bedroom 2 Key": LocData(None, region="Bomb Bunker 4", event_name="Key"),
        "Bomb Bunker - Defeat Liz": LocData(None, region="Bomb Bunker 6", event_name="Defeat Liz"),
        "Bomb Bunker - Bathroom": LocData(1003, region="Bomb Bunker 1"),
        "Bomb Bunker - Grum's Room": LocData(1005, region="Bomb Bunker 7"),
        "Bomb Bunker - Raid the Fridge": LocData(1006, region="Bomb Bunker 1"),
        "Bomb Bunker - Bedroom 2 Item": LocData(1007, region="Bomb Bunker 4"),

        # Mysterious Mafia Base
        "Mysterious Mafia Base - Defeat Corrupt Onion": LocData(None, region="Mysterious Mafia Base 4", event_name="Defeat Corrupt Onion"),
    }