from typing import Callable, Dict

from BaseClasses import CollectionState, MultiWorld

def universal_item_rule(item):
    pass

def can_play_song(song, state, player):
    return state.has(song, player) and state.has("Ocarina of Time", player)

def can_get_magic_beans(state, player):
    return state.has("Magic Bean", player) and state.has("Deku Mask", player) and state.can_reach("Deku Palace", 'Region', player)

def has_bombchus(state, player):
    return state.has("Bombchu (1)", player) or state.has("Bombchu (5)", player) or state.has("Bombchu (10)", player)

def has_explosives(state, player):
    return state.has("Progressive Bomb Bag", player) or has_bombchus(state, player)

def has_hard_projectiles(state, player):
    return state.has("Progressive Bow", player) or state.has("Zora Mask", player) or state.has("Hookshot", player)

def has_projectiles(state, player):
    return (state.has("Deku Mask", player) and state.has("Progressive Magic Upgrade", player)) or has_hard_projectiles(state, player)

def can_smack_hard(state, player):
    return state.has("Progressive Sword", player) or state.has("Fierce Deity's Mask", player) or state.has("Great Fairy Sword", player) or state.has("Goron Mask", player) or state.has("Zora Mask", player)

def can_smack(state, player):
    return can_smack_hard(state, player) or state.has("Deku Mask", player)

def can_clear_woodfall(state, player):
    return state.can_reach("Woodfall Temple Odolwa's Remains", 'Location', player)
    
def can_clear_snowhead(state, player):
    return state.can_reach("Snowhead Temple Goht's Remains", 'Location', player)
    
def can_clear_greatbay(state, player):
    return state.can_reach("Great Bay Temple Gyorg's Remains", 'Location', player)
    
def can_clear_stonetower(state, player):
    return state.can_reach("Stone Tower Temple Twinmold's Remains", 'Location', player)

def has_paper(state, player):
    return state.has("Land Title Deed", player) or state.has("Swamp Title Deed", player) or state.has("Mountain Title Deed", player) or state.has("Ocean Title Deed", player) or state.has("Letter to Kafei", player) or state.has("Priority Mail", player)

def has_bottle(state, player):
    return state.has("Bottle", player) or state.has("Bottle of Chateau Romani", player) or state.has("Bottle of Red Potion", player)

def can_plant_beans(state, player):
    return can_get_magic_beans(state, player) and (has_bottle(state, player) or can_play_song("Song of Storms", state, player))

def can_use_powder_keg(state, player):
    return state.has("Powder Keg", player) and state.has("Goron Mask", player)

def can_use_magic_arrow(item, state, player):
    return state.has(item, player) and state.has("Progressive Bow", player) and state.has("Progressive Magic Upgrade", player)

def can_use_fire_arrows(state, player):
    return can_use_magic_arrow("Fire Arrow", state, player)

def can_use_ice_arrows(state, player):
    return can_use_magic_arrow("Ice Arrow", state, player)

def can_use_light_arrows(state, player):
    return can_use_magic_arrow("Light Arrow", state, player)

def has_gilded_sword(state, player):
    return state.has("Progressive Sword", player, 3)

def get_region_rules(player):
    return {
        "Clock Town -> The Moon":
            lambda state: state.has("Ocarina of Time", player) and state.has("Oath to Order", player) and state.has("Odolwa's Remains", player) and state.has("Goht's Remains", player) and state.has("Gyorg's Remains", player) and state.has("Twinmold's Remains", player),
        "Southern Swamp -> Southern Swamp (Deku Palace)":
            lambda state: state.has("Bottle of Red Potion", player) and has_hard_projectiles(state, player) and state.has("Deku Mask", player), # or state.has("Pictograph Box", player)
        "Southern Swamp (Deku Palace) -> Swamphouse":
            lambda state: state.has("Deku Mask", player) and can_use_fire_arrows(state, player),
        "Southern Swamp (Deku Palace) -> Deku Palace":
            lambda state: state.has("Deku Mask", player),
        "Southern Swamp (Deku Palace) -> Woodfall":
            lambda state: state.has("Deku Mask", player),
        "Woodfall -> Woodfall Temple":
            lambda state: can_play_song("Sonata of Awakening", state, player),
        "Termina Field -> Path to Mountain Village":
            lambda state: state.has("Progressive Bow", player),
        "Path to Mountain Village -> Mountain Village":
            lambda state: state.has("Goron Mask", player) or has_explosives(state, player) or can_use_fire_arrows(state, player),
        "Path to Snowhead -> Snowhead Temple":
            lambda state: state.has("Goron Mask", player) and can_play_song("Goron's Lullaby", state, player) and state.has("Progressive Magic Upgrade", player),
        # ~ "Termina Field -> Great Bay":
            # ~ lambda state: can_play_song("Epona's Song", state, player),
        # ~ "Great Bay -> Ocean Spider House":
            # ~ lambda state: has_explosives(state, player),
        # ~ "Great Bay -> Pirates' Fortress":
            # ~ lambda state: state.has("Zora Mask", state, player),
        # ~ "Pirates' Fortress -> Pirates' Fortress (Interior)":
            # ~ lambda state: state.has("Goron Mask", state, player) or state.has("Hookshot", player),
        # ~ "Zora Cape -> Great Bay Temple":
            # ~ lambda state: can_play_song("New Wave Bossa Nova", state, player) and state.has("Hookshot", player) and state.has("Zora Mask", state, player),
        # ~ "Termina Field -> Ikana Graveyard":
            # ~ lambda state: can_play_song("Epona's Song", state, player),
        # ~ "Termina Field -> Ikana Canyon":
            # ~ lambda state: can_play_song("Epona's Song", state, player) and state.has("Hookshot", player) and (state.has("Garo Mask", player) or state.has("Gibdo Mask", player)),
        # ~ "Ikana Canyon -> Secret Shrine":
            # ~ lambda state: can_use_light_arrows(state, player),
        # ~ "Ikana Canyon -> Beneath the Well":
            # ~ lambda state: can_use_ice_arrows(state, player) and state.has("Gibdo Mask", state, player) and has_bottle(state, player),
        # ~ "Ikana Canyon -> Ikana Castle":
            # ~ lambda state: can_use_ice_arrows(state, player) and (can_use_light_arrows(state, player) or (state.has("Gibdo Mask", state, player) and state.has("Mirror Shield", player) and has_bottle(state, player))),
        # ~ "Ikana Canyon -> Stone Tower Temple":
            # ~ lambda state: can_use_ice_arrows(state, player) and can_play_song("Elegy of Emptiness", state, player) and state.has("Goron Mask", player) and state.has("Zora Mask", player),
        # ~ "Stone Tower Temple -> Stone Tower Temple (Inverted)":
            # ~ lambda state: can_use_light_arrows(state, player),
    }

def get_location_rules(player):
    return {
        "Keaton Quiz":
            lambda state: state.has("Keaton Mask", player),
        "Clock Tower Happy Mask Salesman #1":
            lambda state: state.has("Ocarina of Time", player),
        "Clock Tower Happy Mask Salesman #2":
            lambda state: state.has("Ocarina of Time", player),
        "Clock Town Postbox":
            lambda state: state.has("Postman's Hat", player),
        "Clock Town Hide-and-Seek":
            lambda state: has_projectiles(state, player),
        "Laundry Pool Kafei's Request":
            lambda state: state.has("Letter to Kafei", player),
        "Laundry Pool Curiosity Shop Salesman #1":
            lambda state: state.has("Letter to Kafei", player),
        "Laundry Pool Curiosity Shop Salesman #2":
            lambda state: state.has("Letter to Kafei", player),
        "South Clock Town Corner Chest":
            lambda state: state.has("Hookshot", player),
        "South Clock Town Final Day Tower Chest":
            lambda state: state.has("Hookshot", player) or (state.has("Deku Mask", player) and state.has("Moon's Tear", player)),
        "East Clock Town Mayor Dotour":
            lambda state: state.has("Couple's Mask", player),
        "East Clock Town Shooting Gallery 40-49 Points":
            lambda state: state.has("Progressive Bow", player),
        "East Clock Town Shooting Gallery Perfect 50 Points":
            lambda state: state.has("Progressive Bow", player),
        "East Clock Town Honey and Darling Any Day":
            lambda state: state.has("Progressive Bow", player) or state.has("Progressive Bomb Bag", player) or has_bombchus(state, player),
        "East Clock Town Honey and Darling All Days":
            lambda state: state.has("Progressive Bow", player) and state.has("Progressive Bomb Bag", player) and has_bombchus(state, player),
        "East Clock Town Treasure Game Chest (Goron)":
            lambda state: state.has("Goron Mask", player),
        "East Clock Town Sewer Chest":
            lambda state: state.can_reach("Clock Town Hide-and-Seek", 'Location', player) and has_explosives(state, player),
        "East Clock Town Astral Observatory":
            lambda state: has_projectiles(state, player),
        "North Clock Town Deku Playground Any Day":
            lambda state: state.has("Deku Mask", player),
        "North Clock Town Deku Playground All Days":
            lambda state: state.has("Deku Mask", player),
        "North Clock Town Old Lady":
            lambda state: state.has("Progressive Sword", player) or state.has("Great Fairy Sword", player),
        "North Clock Town Great Fairy Reward (Has Transformation Mask)":
            lambda state: state.has("Stray Fairy (Clock Town)", player) and (state.has("Deku Mask", player) or state.has("Goron Mask", player) or state.has("Zora Mask", player)),
        "North Clock Town Great Fairy Reward":
            lambda state: state.has("Stray Fairy (Clock Town)", player),
        "West Clock Town Swordsman Expert Course":
            lambda state: state.has("Progressive Sword", player),
        "West Clock Town Postman Counting":
            lambda state: state.has("Bunny Hood", player),
        "West Clock Town Rosa Sisters":
            lambda state: state.has("Kamaro Mask", player),
        "West Clock Town Bank 200 Rupees":
            lambda state: state.has("Progressive Sword", player) and state.has("Progressive Wallet", player),
        "West Clock Town Bank 500 Rupees":
            lambda state: state.has("Fierce Deity's Mask", player) and state.has("Great Fairy Sword", player) and state.has("Progressive Wallet", player),
        "West Clock Town Bank 1000 Rupees":
            lambda state: state.has("Fierce Deity's Mask", player) and state.has("Great Fairy Sword", player) and state.has("Progressive Wallet", player, 2),
        "West Clock Town Priority Mail to Postman":
            lambda state: state.has("Priority Mail", player),
        "Moon's Tear Trade":
            lambda state: state.has("Moon's Tear", player),
        "Top of Clock Tower (Ocarina of Time)":
            lambda state: has_projectiles(state, player),
        "Top of Clock Tower (Song of Time)":
            lambda state: has_projectiles(state, player),
        "Stock Pot Inn Midnight Meeting":
            lambda state: state.has("Kafei's Mask", player) and state.has("Deku Mask", player) and state.has("Room Key", player),
        "Stock Pot Inn Knife Chamber Chest":
            lambda state: state.has("Room Key", player),
        "Stock Pot Inn ??? Hand":
            lambda state: has_paper(state, player),
        "Stock Pot Inn Granny Story #1":
            lambda state: state.has("All-Night Mask", player),
        "Stock Pot Inn Granny Story #2":
            lambda state: state.has("All-Night Mask", player),
        "Stock Pot Inn Anju and Kafei":
            lambda state: state.has("Kafei's Mask", player) and can_play_song("Epona's Song", state, player) and state.has("Letter to Kafei", player) and state.has("Pendant of Memories", player) and state.has("Hookshot", player) and (state.has("Garo Mask", player) or state.has("Gibdo Mask", player)),
        "Milk Bar Show":
            lambda state: state.has("Romani Mask", player) and state.has("Deku Mask", player) and state.has("Goron Mask", player) and state.has("Zora Mask", player) and state.has("Ocarina of Time", player),
        "Milk Bar Priority Mail to Aroma":
            lambda state: state.has("Romani Mask", player) and state.has("Kafei's Mask", player) and state.has("Priority Mail", player),


        "Termina Stump Chest":
            lambda state: state.has("Hookshot", player) or can_plant_beans(state, player),
        "Termina Underwater Chest":
            lambda state: state.has("Zora Mask", player),
        "Termina Peahat Grotto Chest":
            lambda state: can_smack_hard(state, player),
        "Termina Dodongo Grotto Chest":
            lambda state: can_smack_hard(state, player),
        "Termina Bio Baba Grotto HP":
            lambda state: has_explosives(state, player) and state.has("Goron Mask", player) and state.has("Zora Mask", player) and has_projectiles(state, player),
        "Termina Kamaro":
            lambda state: state.has("Ocarina of Time", player) and state.has("Song of Healing", player),
        "Termina Gossip Stones HP":
            lambda state: (state.has("Deku Mask", player) and can_play_song("Sonata of Awakening", state, player)) and (state.has("Goron Mask", player) and can_play_song("Goron's Lullaby", state, player)) and (state.has("Zora Mask", player) and can_play_song("New Wave Bossa Nova", state, player)),
        "Termina Moon's Tear Scrub HP":
            lambda state: state.can_reach("East Clock Town Astral Observatory", 'Location', player) and state.has("Moon's Tear", player) and state.has("Progressive Wallet", player),
        "Milk Road Gorman Ranch Race":
            lambda state: state.has("Ocarina of Time", player) and state.has("Epona's Song", player),
        "Road to Swamp Tree HP":
            lambda state: has_projectiles(state, player),
        "Swamp Shooting Gallery 2120 Points":
            lambda state: state.has("Progressive Bow", player),
        "Swamp Shooting Gallery 2180 Points":
            lambda state: state.has("Progressive Bow", player),


        "Romani Ranch Grog":
            lambda state: state.has("Bremen Mask", player),
        # ~ "Romani Ranch Helping Cremia":
            # ~ lambda state: can_use_powder_keg(state, player) and state.has("Progressive Bow", player),
        # ~ "Romani Dog Racetrack Chest":
            # ~ lambda state: state.has("Hookshot", player),
        # ~ "Epona's Song":
            # ~ lambda state: can_use_powder_keg(state, player) and state.has("Progressive Bow", player),


        "Southern Swamp Deku Trade":
            lambda state: state.has("Land Title Deed", player),
        "Southern Swamp Deku Trade Freestanding HP":
            lambda state: state.has("Land Title Deed", player) and state.has("Deku Mask", player),
        "Southern Swamp Koume Tour Gift":
            lambda state: state.has("Bottle of Red Potion", player),
        "Southern Swamp Near Swamphouse Grotto Chest":
            lambda state: state.has("Deku Mask", player),
        "Southern Swamp Song Tablet":
            lambda state: state.has("Deku Mask", player),
        # ~ "Koume Target Shooting":
            # ~ lambda state: state.has("Progressive Bow", player) and state.has("Odolwa's Remains", player),


        "Swamphouse First Room Pot Near Entrance Token":
            lambda state: can_smack(state, player),
        "Swamphouse First Room Crawling In Water Token":
            lambda state: can_smack(state, player),
        "Swamphouse First Room Crawling Right Column Token":
            lambda state: can_smack(state, player) and state.has("Hookshot", player),
        "Swamphouse First Room Crawling Left Column Token":
            lambda state: can_smack(state, player) and state.has("Hookshot", player),
        "Swamphouse First Room Against Far Wall Token":
            lambda state: can_smack(state, player) and state.has("Hookshot", player) and can_plant_beans(state, player),
        "Swamphouse First Room Left Bugpatch Token":
            lambda state: can_smack(state, player) and has_bottle(state, player),
        "Swamphouse First Room Right Bugpatch Token":
            lambda state: can_smack(state, player) and has_bottle(state, player),
        "Swamphouse First Room Upper Right Bugpatch Token":
            lambda state: can_smack(state, player) and has_bottle(state, player),
        "Swamphouse Monument Room Left Crate Token":
            lambda state: can_smack(state, player),
        "Swamphouse Monument Room Right Crate Token":
            lambda state: can_smack(state, player),
        "Swamphouse Monument Room Crawling Wall Token":
            lambda state: can_smack(state, player) and state.has("Hookshot", player) and can_plant_beans(state, player),
        "Swamphouse Monument Room Crawling On Monument Token":
            lambda state: can_smack(state, player) and state.has("Hookshot", player) and can_plant_beans(state, player),
        "Swamphouse Monument Room Behind Torch Token":
            lambda state: can_smack(state, player),
        "Swamphouse Pottery Room Beehive #1 Token":
            lambda state: can_smack(state, player) and has_projectiles(state, player),
        "Swamphouse Pottery Room Beehive #2 Token":
            lambda state: can_smack(state, player) and has_projectiles(state, player),
        "Swamphouse Pottery Room Small Pot Token":
            lambda state: can_smack(state, player),
        "Swamphouse Pottery Room Left Large Pot Token":
            lambda state: can_smack(state, player),
        "Swamphouse Pottery Room Right Large Pot Token":
            lambda state: can_smack(state, player),
        "Swamphouse Pottery Room Behind Vines Token":
            lambda state: can_smack_hard(state, player),
        "Swamphouse Pottery Room Upper Wall Token":
            lambda state: can_smack(state, player) and can_play_song("Sonata of Awakening", state, player) and state.has("Deku Mask", player) and state.has("Hookshot", player),
        "Swamphouse Golden Room Crawling Left Wall Token":
            lambda state: can_smack(state, player) and state.has("Hookshot", player) and can_play_song("Sonata of Awakening", state, player) and state.has("Deku Mask", player),
        "Swamphouse Golden Room Crawling Right Column Token":
            lambda state: can_smack(state, player) and state.has("Hookshot", player),
        "Swamphouse Golden Room Against Far Wall Token":
            lambda state: can_smack(state, player) and state.has("Hookshot", player) and can_plant_beans(state, player),
        "Swamphouse Golden Room Beehive Token":
            lambda state: can_smack(state, player) and has_projectiles(state, player),
        "Swamphouse Tree Room Tall Grass #1 Token":
            lambda state: can_smack(state, player),
        "Swamphouse Tree Room Tall Grass #2 Token":
            lambda state: can_smack(state, player),
        "Swamphouse Tree Room Tree #1 Token":
            lambda state: can_smack(state, player),
        "Swamphouse Tree Room Tree #2 Token":
            lambda state: can_smack(state, player),
        "Swamphouse Tree Room Tree #3 Token":
            lambda state: can_smack(state, player),
        "Swamphouse Tree Room Beehive Token":
            lambda state: can_smack(state, player) and has_projectiles(state, player),
        "Swamphouse Reward":
            lambda state: state.has("Swamp Skulltula Token", player, 30),


        "Deku Palace Bean Seller":
            lambda state: state.has("Deku Mask", player),
        "Deku Palace Bean Grotto Chest":
            lambda state: can_plant_beans(state, player) and state.has("Hookshot", player),
        "Deku Palace Monkey Song":
            lambda state: state.has("Ocarina of Time", player) and can_plant_beans(state, player) and state.has("Deku Mask", player),
        "Deku Palace Butler Race":
            lambda state: can_clear_woodfall(state, player) and has_bottle(state, player),


        "Woodfall Great Fairy Reward":
            lambda state: state.has("Stray Fairy (Woodfall)", player, 15),


        "Woodfall Temple Dragonfly Chest":
            lambda state: state.has("Small Key (Woodfall)", player),
        "Woodfall Temple Black Boe Room Chest":
            lambda state: state.has("Small Key (Woodfall)", player),
        "Woodfall Temple Wooden Flower Switch Chest":
            lambda state: state.has("Progressive Bow", player),
        "Woodfall Temple Dinofols Chest":
            lambda state: state.has("Progressive Bow", player) and can_smack_hard(state, player),
        "Woodfall Temple Boss Key Chest":
            lambda state: state.has("Progressive Bow", player),
        "Woodfall Temple Wooden Flower Bubble SF":
            lambda state: state.has("Progressive Bow", player),
        "Woodfall Temple Moving Flower Platform Room Beehive SF":
            lambda state: has_projectiles(state, player) and state.has("Great Fairy Mask", player),
        "Woodfall Temple Push Block Skulltula SF":
            lambda state: state.has("Small Key (Woodfall)", player) and can_smack_hard(state, player),
        "Woodfall Temple Push Block Bubble SF":
            lambda state: state.has("Small Key (Woodfall)", player) and has_projectiles(state, player) and state.has("Great Fairy Mask", player),
        "Woodfall Temple Push Block Beehive SF":
            lambda state: state.has("Small Key (Woodfall)", player) and has_projectiles(state, player) and state.has("Great Fairy Mask", player),
        "Woodfall Temple Final Room Right Lower Platform SF":
            lambda state: state.has("Progressive Bow", player),
        "Woodfall Temple Final Room Right Upper Platform SF":
            lambda state: state.has("Progressive Bow", player),
        "Woodfall Temple Final Room Left Upper Platform SF":
            lambda state: state.has("Progressive Bow", player),
        "Woodfall Temple Final Room Bubble SF":
            lambda state: state.has("Progressive Bow", player) and state.has("Great Fairy Mask", player),
        "Woodfall Temple Heart Container":
            lambda state: state.has("Progressive Bow", player) and (state.has("Boss Key (Woodfall)", player) or state.has("Odolwa's Remains", player)),
        "Woodfall Temple Odolwa's Remains":
            lambda state: state.has("Progressive Bow", player) and (state.has("Boss Key (Woodfall)", player) or state.has("Odolwa's Remains", player)),
            
            
        "Koume Target Shooting":
            lambda state: can_clear_woodfall(state, player) and state.has("Bottle of Red Potion", player) and state.has("Bottle of Chateau Romani", player) and state.has("Progressive Bow", player),
            
            
        "Mountain Village Darmani":
            lambda state: state.has("Lens of Truth", player) and state.has("Progressive Magic Upgrade", player) and can_play_song("Song of Healing", state, player),
        "Mountain Village Hungry Goron":
            lambda state: state.has("Goron Mask", player) and can_use_fire_arrows(state, player),
        "Mountain Village Spring Ramp Grotto":
            lambda state: state.has("Hookshot", player) or can_clear_snowhead(state, player),
        # ~ "Don Gero HP":
            # ~ lambda state: state.has("Don Gero Mask", player) and can_clear_snowhead(state, player) and state.can_reach("Woodfall Boss Key Chest", 'Location', player) and state.can_reach("Great Bay Temple", 'Region', player) and can_use_ice_arrows(player, state),
        # ~ "Mountain Village Smithy Day 1":
            # ~ lambda state: state.has("Progressive Wallet", player) and (can_clear_snowhead(state, player) or (has_bottle(state, player) and state.can_reach("Mountain Village Darmani", 'Location', player)) or can_use_fire_arrows(state, player)),
        # ~ "Mountain Village Smithy Day 2":
            # ~ lambda state: state.has("Bottle of Gold Dust", state, player) and state.can_reach("Mountain Village Smithy Day 1", 'Location', player),
            
            
        "Twin Islands Ramp Grotto Chest":
            lambda state: has_explosives(state, player) and (state.has("Goron Mask", player) or state.has("Hookshot", player)),
        "Twin Islands Hot Water Grotto Chest":
            lambda state: has_explosives(state, player) and ((can_use_fire_arrows(state, player) or state.can_reach("Mountain Village Darmani", 'Location', player)) or can_clear_snowhead(state, player)),
        "Twin Islands Spring Underwater Cave Chest":
            lambda state: state.has("Zora Mask", player) and can_clear_snowhead(state, player),
        "Twin Islands Spring Underwater Center Chest":
            lambda state: state.has("Zora Mask", player) and can_clear_snowhead(state, player),
        # ~ "Goron Racetrack Bottle Prize":
            # ~ lambda state: state.has("Powder Keg", state, player) and can_clear_snowhead(state, player),
        # ~ "Gorons Lullaby Intro":
            # ~ lambda state: state.has("Goron Mask", player) and ((state.can_reach("Mountain Village Darmani", 'Location', player) and has_bottle(state, player)) or can_use_fire_arrows(state, player)),
            
            
        "Goron Village Lens Cave Rock Chest":
            lambda state: has_explosives(state, player),
        "Gorons Lullaby":
            lambda state: state.has("Goron Mask", player) and (state.can_reach("Mountain Village Darmani", 'Location', player) or can_use_fire_arrows(state, player)),
        "Mountain Title Deed":
            lambda state: state.has("Deku Mask", player) and state.has("Swamp Title Deed", player),
        "Goron Village Freestanding HP":
            lambda state: state.can_reach("Mountain Title Deed", 'Location', player),
        # ~ "Medigoron Reward":
            # ~ lambda state: state.has("Powder Keg", state, player) and can_clear_snowhead(state, player),
        # ~ "Goron Village Deku Scrub Bomb Bag":
            # ~ lambda state: state.has("Goron Mask", player),
            
            
        # ~ "Road to Snowhead Grotto Chest":
            # ~ lambda state: state.has("Goron Mask", player) and state.has("Progressive Magic Upgrade", player) and has_explosives(state, player),
        # ~ "Road to Snowhead HP":
            # ~ lambda state: state.has("Goron Mask", player) and state.has("Progressive Magic Upgrade", player) and state.has("Lens of Truth", player),
            
            
        # ~ "Snowhead Great Fairy Reward":
            # ~ lambda state: state.has("Stray Fairy (Snowhead)", player, 15),
            
            
        "Snowhead Temple Initial Runway Under Platform Bubble SF":
            lambda state: state.has("Great Fairy Mask", player) and state.has("Progressive Bow", player),
        "Snowhead Temple Initial Runway Tower Bubble SF":
            lambda state: state.has("Great Fairy Mask", player) and state.has("Progressive Bow", player) and state.has("Lens of Truth", player),
        "Snowhead Temple Grey Door Box SF":
            lambda state: state.has("Small Key (Snowhead)", player) and state.has("Great Fairy Mask", player) and has_explosives(state, player),
        "Snowhead Temple Timed Switch Room Bubble SF":
            lambda state: state.has("Small Key (Snowhead)", player) and state.has("Great Fairy Mask", player) and state.has("Progressive Bow", player) and state.has("Lens of Truth", player) and has_explosives(state, player),
        "Snowhead Temple Eenos Bubble SF":
            lambda state: state.has("Small Key (Snowhead)", player) and state.has("Great Fairy Mask", player) and state.has("Progressive Bow", player) and has_explosives(state, player),
        "Snowhead Temple Dinolfols Room First SF":
            lambda state: state.has("Small Key (Snowhead)", player) and has_explosives(state, player) and can_use_fire_arrows(state, player),
        "Snowhead Temple Dinolfols Room Second SF":
            lambda state: state.has("Small Key (Snowhead)", player) and has_explosives(state, player) and can_use_fire_arrows(state, player),
        "Snowhead Temple Initial Runway Freezards Chest":
            lambda state: can_use_fire_arrows(state, player),
        "Snowhead Temple Green Door Freezards Chest":
            lambda state: can_use_fire_arrows(state, player),
        "Snowhead Temple Orange Door Upper Chest":
            lambda state: state.has("Hookshot", player) or (state.has("Small Key (Snowhead)", player) and can_use_fire_arrows(state, player)),
        "Snowhead Temple Grey Door Center Chest":
            lambda state: state.has("Small Key (Snowhead)", player),
        "Snowhead Temple Grey Door Upper Chest":
            lambda state: state.has("Small Key (Snowhead)", player) and can_use_fire_arrows(state, player),
        "Snowhead Temple Upstairs 2F Icicle Room Hidden Chest":
            lambda state: state.has("Small Key (Snowhead)", player) and state.has("Lens of Truth", player) and has_explosives(state, player),
        "Snowhead Temple Upstairs 2F Icicle Room Snowball Chest":
            lambda state: state.has("Small Key (Snowhead)", player) and state.has("Progressive Bow", player) and has_explosives(state, player),
        "Snowhead Temple Elevator Room Invisible Platform Chest":
            lambda state: state.has("Lens of Truth", player) and (can_use_fire_arrows(state, player) or (state.has("Small Key (Snowhead)", player) and has_explosives(state, player))),
        "Snowhead Temple Wizzrobe Chest":
            lambda state: state.has("Small Key (Snowhead)", player) and has_explosives(state, player),
        "Snowhead Temple Column Room 2F Hidden Chest":
            lambda state: state.has("Small Key (Snowhead)", player) and state.has("Lens of Truth", state, player) and has_explosives(state, player) and (state.has("Hookshot", player) or (state.has("Deku Mask", player) and can_use_fire_arrows(state, player))),
        "Snowhead Temple Boss Key Chest":
            lambda state: state.has("Small Key (Snowhead)", player) and can_use_fire_arrows(state, player) and has_explosives(state, player),
        "Snowhead Temple Heart Container":
            lambda state: can_use_fire_arrows(state, player) and ((state.has("Boss Key (Snowhead)", player) and state.has("Small Key (Snowhead)", player) and has_explosives(state, player)) or state.has("Goht's Remains", player)),
        "Snowhead Temple Goht's Remains":
            lambda state: can_use_fire_arrows(state, player) and ((state.has("Boss Key (Snowhead)", player) and state.has("Small Key (Snowhead)", player) and has_explosives(state, player)) or state.has("Goht's Remains", player)),
            
        
        # ~ "Great Bay Scarecrow Ledge HP":
            # ~ lambda state: state.has("Hookshot", player) and can_plant_beans(state, player),
        # ~ "Great Bay Mikau":
            # ~ lambda state: state.can_play_song("Song of Healing", state, player),
        # ~ "Fisherman House":
            # ~ # ~ lambda state: state.has("Zora Mask", player) and state.has("Pictograph Box", state, player) and (state.has("Hookshot", player) or state.has("Goron Mask", player)),
        # ~ "Pinnacle Rock HP":
            # ~ lambda state: state.has("Zora Mask", player) and state.has("Progressive Magic Upgrade", state, player), and state.has("Pictograph Box", state, player) and has_bottle(state, player),
        # ~ "Pinnacle Rock Chest 1":
            # ~ lambda state: state.has("Zora Mask", player) and state.has("Progressive Magic Upgrade", state, player), and state.has("Pictograph Box", state, player) and has_bottle(state, player),
        # ~ "Pinnacle Rock Chest 2":
            # ~ lambda state: state.has("Zora Mask", player) and state.has("Progressive Magic Upgrade", state, player), and state.has("Pictograph Box", state, player) and has_bottle(state, player),
        # ~ "New Wave Bossa Nova":
            # ~ lambda state: state.has("Zora Mask", player) and state.has("Progressive Magic Upgrade", state, player) and has_bottle(state, player),
        # ~ "Fisherman Island Game HP":
            # ~ lambda state: can_clear_greatbay(state, player),
        
            
        # ~ "Ocean Spider House Ramp Top Token":
            # ~ lambda state: state.has("Hookshot", player),
        # ~ "Ocean Spider House Ramp Bottom Token":
            # ~ lambda state: state.has("Hookshot", player),
        # ~ "Ocean Spider House Lobby Ceiling Token":
            # ~ lambda state: state.has("Hookshot", player) and can_use_fire_arrows(state, player),
        # ~ "Ocean Spider House First Room Rafter Token":
            # ~ lambda state: state.has("Hookshot", player),
        # ~ "Ocean Spider House First Room Open Pot #1 Token":
            # ~ lambda state: state.has("Hookshot", player),
        # ~ "Ocean Spider House First Room Open Pot #2 Token":
            # ~ lambda state: state.has("Hookshot", player) and can_use_fire_arrows(state, player),
        # ~ "Ocean Spider House First Room Wall Token":
            # ~ lambda state: state.has("Hookshot", player),
        # ~ "Ocean Spider House Library Top Bookcase Token":
            # ~ lambda state: state.has("Hookshot", player) and can_use_fire_arrows(state, player),
        # ~ "Ocean Spider House Library Passage Behind Bookcase Front Token":
            # ~ lambda state: state.has("Hookshot", player) and can_use_fire_arrows(state, player),
        # ~ "Ocean Spider House Library Passage Behind Bookcase Rear Token":
            # ~ lambda state: state.has("Hookshot", player) and can_use_fire_arrows(state, player),
        # ~ "Ocean Spider House Libary Painting #1 Token":
            # ~ lambda state: state.has("Hookshot", player) and can_use_fire_arrows(state, player),
        # ~ "Ocean Spider House Library Painting #2 Token":
            # ~ lambda state: state.has("Hookshot", player) and can_use_fire_arrows(state, player),
        # ~ "Ocean Spider House Library Rafter Token":
            # ~ lambda state: state.has("Hookshot", player) and can_use_fire_arrows(state, player),
        # ~ "Ocean Spider House Library Bookshelf Hole Token":
            # ~ lambda state: state.has("Hookshot", player) and can_use_fire_arrows(state, player),
        # ~ "Ocean Spider House First Room Downstairs Rafter Token":
            # ~ lambda state: state.has("Hookshot", player),
        # ~ "Ocean Spider House First Room Downstairs Pot Token":
            # ~ lambda state: state.has("Hookshot", player),
        # ~ "Ocean Spider House First Room Downstairs Behind Staircase Token":
            # ~ lambda state: state.has("Hookshot", player) and can_use_fire_arrows(state, player),
        # ~ "Ocean Spider House First Room Downstairs Crate Token":
            # ~ lambda state: state.has("Hookshot", player),
        # ~ "Ocean Spider House First Room Downstairs Wall Token":
            # ~ lambda state: state.has("Hookshot", player),
        # ~ "Ocean Spider House Dining Room Pot Token":
            # ~ lambda state: state.has("Hookshot", player),
        # ~ "Ocean Spider House Dining Room Painting Token":
            # ~ # ~ lambda state: state.has("Hookshot", player),
        # ~ "Ocean Spider House Dining Room Ceiling Token":
            # ~ lambda state: state.has("Hookshot", player),
        # ~ "Ocean spider House Dining Room Chandelier #1 Token":
            # ~ lambda state: state.has("Hookshot", player) and state.has("Goron Mask", player),
        # ~ "Ocean Spider House Dining Room Chandelier #2 Token":
            # ~ lambda state: state.has("Hookshot", player) and state.has("Goron Mask", player),
        # ~ "Ocean Spider House Dining Room Chandelier #3 Token ":
            # ~ lambda state: state.has("Hookshot", player) and state.has("Goron Mask", player),
        # ~ "Ocean Spider House Storage Room SW Token":
            # ~ lambda state: state.has("Hookshot", player) and can_use_fire_arrows(state, player),
        # ~ "Ocean Spider House Storage Room North Wall Token":
            # ~ lambda state: state.has("Hookshot", player) and can_use_fire_arrows(state, player),
        # ~ "Ocean Spider House Storage Room Crate Token":
            # ~ lambda state: state.has("Hookshot", player) and can_use_fire_arrows(state, player),
        # ~ "Ocean Spider House Storage Room Hidden Hole Token":
            # ~ lambda state: state.has("Hookshot", player) and can_use_fire_arrows(state, player),
        # ~ "Ocean Spider House Storage Room Ceiling Barrel Token":
            # ~ lambda state: state.has("Hookshot", player) and can_use_fire_arrows(state, player),
        # ~ "Ocean Spider House HP":
            # ~ lambda state: state.has("Hookshot", player) and state.has("Captain's Hat", player) and state.has("Progressive Bow", player),
        # ~ "Ocean Spider House Reward":
            # ~ lambda state: state.has("Ocean Skulltula Token", player, 30),
        
        
        # ~ "Pirates' Fortress Tunnels HP":
            # ~ lambda state: state.has("Goron's Mask", player),
        # ~ "Pirates' Fortress Tunnels Cage Chest":
            # ~ lambda state: state.has("Goron's Mask", player),
        # ~ "Pirates' Fortress Tunnels Mines Chest":
            # ~ lambda state: state.has("Goron's Mask", player),
        # ~ "Pirates' Fortress Tunnels Lower Mines Chest":
            # ~ lambda state: state.has("Goron's Mask", player),
        # ~ "Pirates' Fortress Fish Tank Chest":
            # ~ lambda state: state.has("Hookshot", player),
        # ~ "Pirates' Fortress Pirates Surrounding Chest":
            # ~ lambda state: has_projectiles(state, player),
        # ~ "Pirates' Fortress Hub Lower Chest":
            # ~ lambda state: state.has("Goron's Mask", player) or state.has("Hookshot", player),
        # ~ "Pirates' Fortress Hub Upper Chest":
            # ~ lambda state: state.has("Hookshot", player),
            
            
        # ~ "Zora Cape Near Great Fairy Grotto Chest":
            # ~ lambda state: state.has("Goron Mask", player) or has_explosives(state, player),
        # ~ "Zora Cape Underwater Chest":
            # ~ lambda state: state.has("Zora Mask", player),
        # ~ "Zora Cape Underwater Like-Like HP":
            # ~ lambda state: state.has("Zora Mask", player),
        # ~ "Zora Cape Pot Game HP":
            # ~ lambda state: state.has("Zora Mask", player),
        # ~ "Zora Cape First High Ledge Chest":
            # ~ lambda state: state.has("Hookshot", player),
        # ~ "Zora Cape Second High Ledge Chest":
            # ~ lambda state: state.has("Hookshot", player),
        # ~ "Beaver Bros. Race Bottle Reward":
            # ~ lambda state: state.has("Hookshot", player) and state.has("Zora Mask", player),
        # ~ "Beaver Bros. Race HP":
            # ~ lambda state: state.has("Hookshot", player) and state.has("Zora Mask", player),
            
            
        # ~ "Zora Hall Evan HP":
            # ~ lambda state: state.has("Zora Mask", player),
        # ~ "Zora Hall Torches Chest":
            # ~ lambda state: can_use_fire_arrows(state, player),
        # ~ "Zora Hall Deku Scrub Trade":
            # ~ lambda state: state.has("Zora Mask", player) and state.has("Mountain Title Deed", state, player),
        # ~ "Zora Hall HP":
            # ~ lambda state: state.has("Deku Mask", player) and can_reach("Zora Hall Deku Scrub Trade", 'Location', player),
            
            
        # ~ "Great Bay Great Fairy Reward":
            # ~ lambda state: state.has("Stray Fairy (Great Bay)", player, 15),
            
            
        # ~ "Great Bay Temple Gekko Entrance Room Pot SF":
            # ~ lambda state: state.has("Great Fairy Mask", player),
        # ~ "Great Bay Temple Green Pipe Lever Room Underwater Barrel SF":
            # ~ lambda state: can_use_ice_arrows(state, player),
        # ~ "Great Bay Temple Four Torches Chest":
            # ~ lambda state: can_use_fire_arrows(state, player),
        # ~ "Great Bay Temple Wart Chest":
            # ~ lambda state: state.has("Progressive Bow", player),
        # ~ "Great Bay Temple Boss Key Chest":
            # ~ lambda state: can_use_ice_arrows(state, player) and can_use_fire_arrows(state, player),
        # ~ "Great Bay Temple Red-Green Pipe First Room Chest":
            # ~ lambda state: can_use_ice_arrows(state, player),
        # ~ "Great Bay Temple Green-Yellow Pipe Chest":
            # ~ lambda state: can_use_ice_arrows(player, state),
        # ~ "Great Bay Temple Green Pipe Freezable Waterwheel Upper Chest":
            # ~ lambda state: can_use_ice_arrows(state, player),
        # ~ "Great Bay Temple Green Pipe Freezable Waterwheel Lower Chest":
            # ~ lambda state: can_use_ice_arrows(state, player),
        # ~ "Great Bay Temple Green Pipe Lever Room Chest":
            # ~ lambda state: can_use_ice_arrows(state, player) and can_use_fire_arrows(state, player),
        # ~ "Great Bay Temple Heart Container":
            # ~ lambda state: (can_use_ice_arrows(state, player) and can_use_fire_arrows(state, player) and state.has("Small Key (Great Bay Temple)", player) and state.has("Boss Key (Great Bay Temple)", player)) or (state.has("Gyorg's Remains", player) and state.has("Progressive Bow", player)),
        # ~ "Great Bay Temple Gyorg's Remains":
            # ~ lambda state: (can_use_ice_arrows(state, player) and can_use_fire_arrows(state, player) and state.has("Small Key (Great Bay Temple)", player) and state.has("Boss Key (Great Bay Temple)", player)) or (state.has("Gyorg's Remains", player) and state.has("Progressive Bow", player)),
        

        "Road to Ikana Pillar Chest":
            lambda state: state.has("Hookshot", player),
        "Road to Ikana Rock Grotto Chest":
            lambda state: state.has("Goron Mask", player),
        "Road to Ikana Stone Soldier":
            lambda state: can_play_song("Epona's Song", state, player) and has_bottle(state, player) and state.has("Progressive Magic Upgrade", player) and state.has("Lens of Truth", player),
            
            
        # ~ "Graveyard Day 1 Chest":
            # ~ lambda state: state.has("Captain's Hat", player) and can_smack_hard(state, player),
        # ~ "Graveyard Day 2 Chest":
            # ~ lambda state: state.has("Captain's Hat", player) and can_smack_hard(state, player) and has_explosives(state, player),
        # ~ "Graveyard Day 3 Chest":
            # ~ lambda state: state.has("Captain's Hat", player) and (can_smack_hard(state, player) or has_projectiles(state, player)),
        # ~ "Graveyard Skull Keeta Chest":
            # ~ lambda state: can_play_song("Sonata of Awakening", state, player) and can_smack_hard(state, player),
        # ~ "Song of Storms":
            # ~ lambda state: state.has("Captain's Hat", player) and can_smack_hard(state, player) and can_use_fire_arrows(state, player),
            
        # ~ "Ikana Canyon Pamela's Father":
            # ~ lambda state: can_play_song("Song of Healing", state, player) and can_play_song("Song of Storms", state, player) and (has_explosives(state, player) or state.has("Stone Mask", player,)),
        # ~ "Ikana Canyon Deku Scrub Trade":
            # ~ lambda state: state.has("Zora Mask", player) and state.has("Ocean Title Deed", state, player),
        # ~ "Ikana Canyon HP":
            # ~ lambda state: state.has("Deku Mask", player) and can_reach("Ikana Canyon Deku Scrub Trade", 'Location', player),
            
            
        # ~ "Stone Temple Great Fairy Reward":
            # ~ lambda state: state.has("Stray Fairy (Stone Tower)", player, 15),
            
        
        # ~ "Secret Shrine Left Chest":
            # ~ lambda state: can_smack_hard(state, player),
        # ~ "Secret Shrine Middle-Left Chest":
            # ~ lambda state: can_smack_hard(state, player) and has_projectiles(state, player),
        # ~ "Secret Shrine Middle-Right Chest":
            # ~ lambda state: can_smack_hard(state, player) and has_projectiles(state, player),
        # ~ "Secret Shrine Right Chest":
            # ~ lambda state: can_smack_hard(state, player),
        # ~ "Secret Shrine Center Chest":
            # ~ lambda state: state.can_reach("Secret Shrine Left Chest", 'Location', player) and state.can_reach("Secret Shrine Middle-Left Chest", 'Location', player) and state.can_reach("Secret Shrine Middle-Right Chest", 'Location', player) and state.can_reach("Secret Shrine Right Chest", 'Location', player),
            
            
        # ~ "Beneath the Well Torch Chest":
            # ~ lambda state: has_bottle(state, player),
        # ~ "Beneath the Well Invisible Chest":
            # ~ lambda state: has_bottle(state, player) and can_plant_beans(state, player),
        # ~ "Beneath the Well Final Chest":
            # ~ lambda state: can_use_light_arrows(state, player) or (has_bottle(state, player) and can_plant_beans(state, player)),
            
            
        # ~ "Ikana Castle Pillar Freestanding HP":
            # ~ lambda state: state.has("Deku Mask", player) and state.has("Lens of Truth", state, player) and can_use_fire_arrows(state, player), 
            
            
        # ~ "Stone Tower Inverted Outside Left Chest":
            # ~ lambda state: can_plant_beans(state, player),
        # ~ "Stone Tower Inverted Outside Middle Chest":
            # ~ lambda state: can_plant_beans(state, player),
        # ~ "Stone Tower Inverted Outside Right Chest":
            # ~ lambda state: can_plant_beans(state, player),


        # ~ "Stone Tower Temple Armos Room Back Chest":
            # ~ lambda state: can_use_light_arrows(state, player) or (state.has("Mirror Shield", player) and has_explosives(state, player)),
        # ~ "Stone Tower Temple Eyegore Room Switch Chest":
            # ~ lambda state: can_use_light_arrows(state, player) and (has_explosives(state, player) or state.has("Great Spin Attack", player)),
        # ~ "Stone Tower Temple Eastern Water Room Sun Block Chest":
            # ~ lambda state: can_use_light_arrows(state, player) or state.has("Mirror Shield", player),
        # ~ "Stone Tower Temple Wall Suns Room Sun Block Chest":
            # ~ lambda state: state.has("Small Key (Stone Tower Temple)", state, player) and (can_use_light_arrows(state, player) or state.has("Mirror Shield", player)),
        # ~ "Stone Tower Temple Wall Suns Room Center Chest"
            # ~ lambda state: state.has("Small Key (Stone Tower Temple)", state, player), and (can_use_light_arrows(state, player) or state.has("Mirror Shield", player)),
        # ~ "Stone Tower Temple Wall Air Gust Room Side Chest":
            # ~ lambda state: state.has("Small Key (Stone Tower Temple)", state, player) and state.has("Deku Mask", player) and (can_use_light_arrows(state, player) or state.has("Mirror Shield", player)),
        # ~ "Stone Tower Temple Wall Air Gust Room End Chest":
            # ~ lambda state: state.has("Small Key (Stone Tower Temple)", state, player) and state.has("Deku Mask", player) and (can_use_light_arrows(state, player) or state.has("Mirror Shield", player)),
        # ~ "Stone Tower Temple Garo Master Chest":
            # ~ lambda state: state.has("Small Key (Stone Tower Temple)", state, player) and state.has("Deku Mask", player) and (can_use_light_arrows(state, player) or state.has("Mirror Shield", player)),
        # ~ "Stone Tower Temple After Garo Upside Down Chest":
            # ~ lambda state: state.has("Small Key (Stone Tower Temple)", state, player) and state.has("Deku Mask", player) and can_use_light_arrows(state, player),
        # ~ "Stone Tower Temple Eyegore Chest":
            # ~ lambda state: state.has("Small Key (Stone Tower Temple)", state, player) and state.has("Deku Mask", player) and (can_use_light_arrows(state, player) or state.has("Mirror Shield", player)),
        # ~ "Stone Tower Temple Inverted Eastern Air Gust Room Fire Chest":
            # ~ lambda state: state.has("Deku Mask", player),
        # ~ "Stone Tower Temple Inverted Eastern Air Gust Room Snugly Tucked Cranny Chest":
            # ~ lambda state: state.has("Deku Mask", player) and can_use_fire_arrows(state, player),
        # ~ "Stone Tower Temple Inverted Eastern Air Gust Room Hall Floor Switch Chest":
            # ~ lambda state: state.has("Deku Mask", player),
        # ~ "Stone Tower Temple Inverted Wizzrobe Chest":
            # ~ lambda state: state.has("Small Key (Stone Tower Temple)", state, player) and state.has("Deku Mask", player),
        # ~ "Stone Tower Temple Inverted Death Armos Maze Chest":
            # ~ lambda state: state.has("Small Key (Stone Tower Temple)", state, player) and state.has("Deku Mask", player),
        # ~ "Stone Tower Temple Inverted Gomess Chest":
            # ~ lambda state: state.has("Small Key (Stone Tower Temple)", state, player) and state.has("Deku Mask", player),
        # ~ "Stone Tower Temple Inverted Eyegore Chest":
            # ~ lambda state: state.has("Small Key (Stone Tower Temple)", state, player) and state.has("Deku Mask", player),
        # ~ "Stone Tower Temple Heart Container":
            # ~ lambda state: state.has("Small Key (Stone Tower Temple)", state, player) and state.has("Deku Mask", player) and state.has("Giant's Mask", player) and (state.has("Boss Key (Stone Tower Temple)", state, player) or state.has("Twinmold's Remains", state, player)),
        # ~ "Stone Tower Temple Twinmold's Remains":
            # ~ lambda state: state.has("Small Key (Stone Tower Temple)", state, player) and state.has("Deku Mask", player) and state.has("Giant's Mask", player) and (state.has("Boss Key (Stone Tower Temple)", state, player) or state.has("Twinmold's Remains", state, player)),


        "Defeat Majora":
            lambda state: state.has("Fierce Deity's Mask", player) and state.has("Progressive Magic Upgrade", player) and state.has("Great Fairy Sword", player) and has_gilded_sword(state, player) and state.has("Progressive Bow", player) and state.has("Light Arrow", player)
    }
