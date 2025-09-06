from typing import Dict, TYPE_CHECKING

from worlds.generic.Rules import set_rule, forbid_item, add_rule
from .items import item_table
from .options import FF1pixelOptions
from BaseClasses import CollectionState
if TYPE_CHECKING:
    from . import FF1pixelWorld, FF1pixelOptions

lute = "Lute"
crown = "Crown"
crystal_eye = "Crystal Eye"
jolt_tonic = "Jolt Tonic"
mystic_key = "Mystic Key"
nitro_powder = "Nitro Powder"
star_ruby = "Star Ruby"
earth_rod = "Earth Rod"
levistone = "Levistone"
warp_cube = "Warp Cube"
chime = "Chime"
oxyale = "Oxyale"
rosetta_stone = "Rosetta Stone"
adamantite = "Adamantite"
rattail = "Rat's Tail"
alljobsitem = "All Promotion Jobs"
tablature = "Lute Tablature"

ship = "Ship"
canoe = "Canoe"
airship = "Airship"
submarine = "Submarine"
lufenian_learned = "Lufenian Learned"
garland_defeated = "Garland Defeated"
canal = "Canal"
vampire_defeated = "Vampire Defeated"
titan_fed = "Titan Fed"
earth_crystal = "Earth Crystal"
fire_crystal = "Fire Crystal"
water_crystal = "Water Crystal"
air_crystal = "Air Crystal"
bottle = "Bottled Faerie"
black_orb_destroyed = "Black Orb Destroyed"
chaos_defeated = "Chaos Defeated"

mystic_key_locked_Locations = [
    "Chaos Shrine - Locked Single",
    "Chaos Shrine - Locked Duo 1",
    "Chaos Shrine - Locked Duo 2",
    "Castle Cornelia - Treasury 1",
    "Castle Cornelia - Treasury 2",
    "Castle Cornelia - Treasury 3",
    "Castle Cornelia - Treasury 4",
    "Castle Cornelia - Treasury 5",
    "Castle Cornelia - Treasury Major",
    "Marsh Cave B3 (Bottom) - Locked Corner",
    "Marsh Cave B3 (Bottom) - Locked Middle",
    "Marsh Cave B3 (Bottom) - Locked Cross",
    "Western Keep - Treasury 1",
    "Western Keep - Treasury 2",
    "Western Keep - Treasury 3",
    "Elven Castle - Treasury 1",
    "Elven Castle - Treasury 2",
    "Elven Castle - Treasury 3",
    "Elven Castle - Treasury 4",
    "Mount Duergar - Treasury 1",
    "Mount Duergar - Treasury 2",
    "Mount Duergar - Treasury 3",
    "Mount Duergar - Treasury 4",
    "Mount Duergar - Treasury 5",
    "Mount Duergar - Treasury 6",
    "Mount Duergar - Treasury 7",
    "Mount Duergar - Treasury 8",
]

def has_tablatures(state: CollectionState, options: FF1pixelOptions, player: int) -> bool:
    return state.has(tablature, player, options.lute_tablatures.value)

def has_crystals(state: CollectionState, options: FF1pixelOptions, player: int) -> bool:
    return (state.has(earth_crystal, player) + state.has(fire_crystal, player) +
        state.has(water_crystal, player) + state.has(air_crystal, player)) >= options.crystals_required

def set_region_rules(world: "FF1pixelWorld") -> None:
    player = world.player
    options = world.options

    if world.options.early_progression.value == 0: # bikke ship
        world.get_entrance("Overworld -> Innersea Region").access_rule = \
            lambda state: state.has(ship, player) or state.has(airship, player)
        world.get_entrance("Overworld -> Ice Region").access_rule = \
            lambda state: state.has(canoe, player) or state.has(airship, player)
        world.get_entrance("Overworld -> Crescent Region").access_rule = \
            lambda state: state.has_all({ship, canal}, player) or state.has_all({ship, canoe}, player) or state.has(airship, player)
        world.get_entrance("Overworld -> Gulg Region").access_rule = \
            lambda state: state.has_all({ship, canoe}, player) or state.has(airship, player)
        world.get_entrance("Overworld -> Ryukhan Desert").access_rule = \
            lambda state: state.has_all({ship, canoe, canal}, player) or state.has(airship, player)
    else:
        world.get_entrance("Overworld -> Pravoka Region").access_rule = \
            lambda state: state.has(ship, player) or state.has(airship, player)
        world.get_entrance("Overworld -> Ice Region").access_rule = \
            lambda state: state.has_all({ship, canoe}, player) or state.has(airship, player)
        world.get_entrance("Overworld -> Crescent Region").access_rule = \
            lambda state: state.has_all({ship, canal}, player) or state.has(canoe, player) or state.has(airship, player)
        world.get_entrance("Overworld -> Gulg Region").access_rule = \
            lambda state: state.has(canoe, player) or state.has(airship, player)
        world.get_entrance("Overworld -> Ryukhan Desert").access_rule = \
            lambda state: state.has_all({canoe, ship, canal}, player) or state.has(airship, player)

    world.get_entrance("Overworld -> Melmond Region").access_rule = \
        lambda state: state.has_all({ship, canal}, player) or state.has(airship, player)
    world.get_entrance("Overworld -> Sage Region").access_rule = \
        lambda state: state.has_all({ship, canal, titan_fed}, player) or state.has_all({airship, titan_fed}, player)
    world.get_entrance("Overworld -> Dragon Region").access_rule = \
        lambda state: state.has(airship, player)
    world.get_entrance("Overworld -> Onrac Region").access_rule = \
        lambda state: state.has(airship, player)
    world.get_entrance("Overworld -> Trials Region").access_rule = \
        lambda state: state.has_all({airship, canoe, crown}, player) or state.has_all({ship, canal, canoe, crown}, player)
    world.get_entrance("Overworld -> Gaia").access_rule = \
        lambda state: state.has(airship, player)
    world.get_entrance("Overworld -> Mirage Desert").access_rule = \
        lambda state: state.has(airship, player)
    world.get_entrance("Overworld -> Lufenia Region").access_rule = \
        lambda state: state.has(airship, player)
    world.get_entrance("Overworld -> Beyond the Black Orb").access_rule = \
        lambda state: (state.has_all({black_orb_destroyed, lute}, player) and
                       has_tablatures(state, options, player))
    world.get_entrance("Melmond Region -> Cavern of Earth Deep").access_rule = \
        lambda state: state.has(earth_rod, player)
    world.get_entrance("Onrac Region -> Waterfall").access_rule = \
        lambda state: state.has(canoe, player)
    world.get_entrance("Onrac Region -> Sunken Shrine").access_rule = \
        lambda state: state.has(submarine, player)
    world.get_entrance("Mirage Desert -> Mirage Tower").access_rule = \
        lambda state: state.has(chime, player)
    world.get_entrance("Mirage Tower -> Flying Fortress").access_rule = \
        lambda state: state.has(warp_cube, player)

    if world.options.northern_docks.value:
        world.get_entrance("Overworld -> Onrac Region").access_rule = \
            lambda state: state.has(airship, player) or state.has_all({ship, canal}, player)
        world.get_entrance("Overworld -> Mirage Desert").access_rule = \
            lambda state: state.has(airship, player) or state.has_all({ship, canal}, player)

def set_location_rules(world: "FF1pixelWorld") -> None:
    player = world.player

    # NPCs
    set_rule(world.get_location("Castle Cornelia - Princess"),
             lambda state: state.has(garland_defeated, player))
    set_rule(world.get_location("Matoya's Cave - Matoya"),
             lambda state: state.has(crystal_eye, player))
    set_rule(world.get_location("Western Keep - Astos"),
             lambda state: state.has(crown, player))
    set_rule(world.get_location("Elven Castle - Elf Prince"),
             lambda state: state.has(jolt_tonic, player))
    set_rule(world.get_location("Mount Duergar - Smitt"),
             lambda state: state.has(adamantite, player))
    set_rule(world.get_location("Sage's Cave - Sarda"),
             lambda state: state.has(vampire_defeated, player))
    set_rule(world.get_location("Crescent Lake - Canoe Sage"),
             lambda state: state.has(earth_crystal, player))
    set_rule(world.get_location("Gaia - Fairy"),
             lambda state: state.has(bottle, player))
    set_rule(world.get_location("Lufenia - Lufenian Man"),
             lambda state: state.has(lufenian_learned, player))

    # Mystic Key locations
    for loc_name in mystic_key_locked_Locations:
        set_rule(world.get_location(loc_name),
                 lambda state: state.has(mystic_key, player))

    # Event Location
    world.get_location("Chaos Shrine - Garland").place_locked_item(world.create_event(garland_defeated))
    world.get_location("Mount Duergar - Nerrick").place_locked_item(world.create_event(canal))
    set_rule(world.get_location("Mount Duergar - Nerrick"),
             lambda state: state.has(nitro_powder, player))
    world.get_location("Cavern of Earth - Vampire").place_locked_item(world.create_event(vampire_defeated))
    world.get_location("Giant's Cave - Titan").place_locked_item(world.create_event(titan_fed))
    set_rule(world.get_location("Giant's Cave - Titan"),
             lambda state: state.has(star_ruby, player))
    world.get_location("Cavern of Earth - Lich").place_locked_item(world.create_event(earth_crystal))
    world.get_location("Ryukhan Desert - Airship").place_locked_item(world.create_event(airship))
    set_rule(world.get_location("Ryukhan Desert - Airship"),
             lambda state: state.has(levistone, player))
    world.get_location("Mount Gulg - Kary").place_locked_item(world.create_event(fire_crystal))
    #world.get_location("Caravan").place_locked_item(world.create_event(bottle))
    world.get_location("Onrac - Sub Engineer").place_locked_item(world.create_event(submarine))
    set_rule(world.get_location("Onrac - Sub Engineer"),
             lambda state: state.has(oxyale, player))
    world.get_location("Sunken Shrine - Kraken").place_locked_item(world.create_event(water_crystal))
    world.get_location("Melmond - Dr Unne").place_locked_item(world.create_event(lufenian_learned))
    set_rule(world.get_location("Melmond - Dr Unne"),
             lambda state: state.has(rosetta_stone, player))
    world.get_location("Flying Fortress - Tiamat").place_locked_item(world.create_event(air_crystal))
    world.get_location("Chaos Shrine - Black Orb").place_locked_item(world.create_event(black_orb_destroyed))
    set_rule(world.get_location("Chaos Shrine - Black Orb"),
             lambda state: has_crystals(state, world.options, player))
    world.get_location("Chaos Shrine - Chaos").place_locked_item(world.create_event(chaos_defeated))
    set_rule(world.get_location("Chaos Shrine - Chaos"),
             lambda state: state.has_all({black_orb_destroyed, lute}, player))

    # Ship Logic
    if world.options.early_progression.value == 0 and not world.spawn_ship:
        world.get_location("Pravoka - Bikke").place_locked_item(world.create_item(ship))

    # Bahamut
    set_rule(world.get_location("Dragon Caves - Bahamut"),
        lambda state: state.has(rattail, player))
    if world.options.job_promotion.value == 0:
        world.get_location("Dragon Caves - Bahamut").place_locked_item(world.create_item(alljobsitem))

    # Prevent Gil landing in the Caravan
    for item_name, item_value in item_table.items():
        if item_value.item_id_offset == 1:
            forbid_item(world.get_location("Onrac Desert - Caravan"), item_name, player)

    # Victory Condition
    world.multiworld.completion_condition[world.player] = lambda state: state.has(chaos_defeated, world.player)

