from typing import Callable, Dict, NamedTuple, Optional

from BaseClasses import Location, MultiWorld


class MMRLocation(Location):
    game = "Majora's Mask Recompiled"


class MMRLocationData(NamedTuple):
    region: str
    address: Optional[int] = None
    can_create: Callable = lambda options: True
    locked_item: Optional[str] = None


location_data_table: Dict[str, MMRLocationData] = {
    "Keaton Quiz": MMRLocationData(
        region="Clock Town",
        address=0x3476942007028C
    ),
    "Clock Tower Happy Mask Salesman #1": MMRLocationData(
        region="Clock Town",
        address=0x34769420040068
    ),
    "Clock Tower Happy Mask Salesman #2": MMRLocationData(
        region="Clock Town",
        address=0x34769420000078
    ),
    "Clock Town Postbox": MMRLocationData(
        region="Clock Town",
        address=0x347694200701F2
    ),
    "Clock Town Hide-and-Seek": MMRLocationData(
        region="Clock Town",
        address=0x34769420000050
    ),
    "Laundry Pool Stray Fairy (Clock Town)": MMRLocationData(
        region="Clock Town",
        address=0x3476942001007F
    ),
    "Laundry Pool Guru-Guru": MMRLocationData(
        region="Clock Town",
        address=0x3476942000008C
    ),
    "Laundry Pool Kafei's Request": MMRLocationData(
        region="Clock Town",
        address=0x347694200000AB
    ),
    "Laundry Pool Curiosity Shop Salesman #1": MMRLocationData(
        region="Clock Town",
        address=0x34769420000080
    ),
    "Laundry Pool Curiosity Shop Salesman #2": MMRLocationData(
        region="Clock Town",
        address=0x347694200000A1
    ),
    "South Clock Town Corner Chest": MMRLocationData(
        region="Clock Town",
        address=0x34769420066F00
    ),
    "South Clock Town Final Day Tower Chest": MMRLocationData(
        region="Clock Town",
        address=0x34769420066F01
    ),
    "East Clock Town Chest": MMRLocationData(
        region="Clock Town",
        address=0x34769420066C0A
    ),
    "East Clock Town Madame Aroma": MMRLocationData(
        region="Clock Town",
        address=0x3476942000008F
    ),
    "East Clock Town Mayor Dotour": MMRLocationData(
        region="Clock Town",
        address=0x3476942007026F
    ),
    "East Clock Town Shooting Gallery 40-49 Points": MMRLocationData(
        region="Clock Town",
        address=0x34769420000023
    ),
    "East Clock Town Shooting Gallery Perfect 50 Points": MMRLocationData(
        region="Clock Town",
        address=0x3476942007011D
    ),
    "East Clock Town Honey and Darling Any Day": MMRLocationData(
        region="Clock Town",
        address=0x347694200800B5
    ),
    "East Clock Town Honey and Darling All Days": MMRLocationData(
        region="Clock Town",
        address=0x347694200700B5
    ),
    "East Clock Town Treasure Game Chest": MMRLocationData(
        region="Clock Town",
        address=0x34769420061700
    ),
    "East Clock Town Sewer Chest": MMRLocationData(
        region="Clock Town",
        address=0x34769420062900
    ),
    "East Clock Town Astral Observatory": MMRLocationData(
        region="Clock Town",
        address=0x34769420000096
    ),
    "North Clock Town Tree HP": MMRLocationData(
        region="Clock Town",
        address=0x34769420056E0A
    ),
    "North Clock Town Deku Playground Any Day": MMRLocationData(
        region="Clock Town",
        address=0x347694200801C9
    ),
    "North Clock Town Deku Playground All Days": MMRLocationData(
        region="Clock Town",
        address=0x347694200701C9
    ),
    "North Clock Town Old Lady": MMRLocationData(
        region="Clock Town",
        address=0x3476942000008D
    ),
    "North Clock Town Great Fairy Reward": MMRLocationData(
        region="Clock Town",
        address=0x34769420030000
    ),
    "North Clock Town Great Fairy Reward (Has Transformation Mask)": MMRLocationData(
        region="Clock Town",
        address=0x34769420000086
    ),
    "West Clock Town Swordsman Expert Course": MMRLocationData(
        region="Clock Town",
        address=0x347694200701EF
    ),
    "West Clock Town Postman Counting": MMRLocationData(
        region="Clock Town",
        address=0x3476942007017D
    ),
    "West Clock Town Rosa Sisters": MMRLocationData(
        region="Clock Town",
        address=0x3476942007027B
    ),
    "West Clock Town Bank 200 Rupees": MMRLocationData(
        region="Clock Town",
        address=0x34769420000008
    ),
    "West Clock Town Bank 1000 Rupees": MMRLocationData(
        region="Clock Town",
        address=0x34769420070177
    ),
    "West Clock Town Priority Mail to Postman": MMRLocationData(
        region="Clock Town",
        address=0x34769420000084
    ),
    "Moon's Tear Trade": MMRLocationData(
        region="Clock Town",
        address=0x34769420000097
    ),
    "Moon's Tear Trade Freestanding HP": MMRLocationData(
        region="Clock Town",
        address=0x34769420056F0A
    ),
    "Top of Clock Tower (Ocarina of Time)": MMRLocationData(
        region="Clock Town",
        address=0x3476942000004C
    ),
    "Top of Clock Tower (Song of Time)": MMRLocationData(
        region="Clock Town",
        address=0x34769420040067
    ),
    "Stock Pot Inn Reservation": MMRLocationData(
        region="Clock Town",
        address=0x347694200000A0
    ),
    "Stock Pot Inn Midnight Meeting": MMRLocationData(
        region="Clock Town",
        address=0x347694200000AA
    ),
    "Stock Pot Inn Knife Chamber Chest": MMRLocationData(
        region="Clock Town",
        address=0x34769420066100
    ),
    "Stock Pot Inn Employees Only Room Chest": MMRLocationData(
        region="Clock Town",
        address=0x34769420066101
    ),
    "Stock Pot Inn ??? Hand": MMRLocationData(
        region="Clock Town",
        address=0x3476942007027D
    ),
    "Stock Pot Inn Granny Story #1": MMRLocationData(
        region="Clock Town",
        address=0x34769420070243
    ),
    "Stock Pot Inn Granny Story #2": MMRLocationData(
        region="Clock Town",
        address=0x34769420080243
    ),
    "Stock Pot Inn Anju and Kafei": MMRLocationData(
        region="Clock Town",
        address=0x34769420000085
    ),
    "Milk Bar Show": MMRLocationData(
        region="Clock Town",
        address=0x34769420000083
    ),
    "Milk Bar Priority Mail to Aroma": MMRLocationData(
        region="Clock Town",
        address=0x3476942000006F
    ),
    "Termina Stump Chest": MMRLocationData(
        region="Termina Field",
        address=0x34769420062D02
    ),
    "Termina Tall Grass Chest": MMRLocationData(
        region="Termina Field",
        address=0x34769420062D01
    ),
    "Termina Underwater Chest": MMRLocationData(
        region="Termina Field",
        address=0x34769420062D00
    ),
    "Termina Tall Grass Grotto Chest": MMRLocationData(
        region="Termina Field",
        address=0x3476942006071F
    ),
    "Termina Peahat Grotto Chest": MMRLocationData(
        region="Termina Field",
        address=0x34769420060704
    ),
    "Termina Dodongo Grotto Chest": MMRLocationData(
        region="Termina Field",
        address=0x34769420060700
    ),
    "Termina Ikana Pillar Grotto Chest": MMRLocationData(
        region="Termina Field",
        address=0x3476942006071A
    ),
    "Termina Kamaro": MMRLocationData(
        region="Termina Field",
        address=0x34769420000089
    ),
    "Milk Road Gorman Ranch Race": MMRLocationData(
        region="Termina Field",
        address=0x34769420000081
    ),
    "Romani Ranch Grog": MMRLocationData(
        region="Romani Ranch",
        address=0x3476942000007F
    ),
    # ~ "Romani Ranch Helping Cremia": MMRLocationData(
        # ~ region="Romani Ranch",
        # ~ address=0x34769420000082
    # ~ ),
    "Road to Swamp Tree HP": MMRLocationData(
        region="Southern Swamp",
        address=0x34769420054001
    ),
    "Road to Swamp Grotto Chest": MMRLocationData(
        region="Clock Town",
        address=0x3476942006071E
    ),
    "Southern Swamp Deku Trade": MMRLocationData(
        region="Southern Swamp",
        address=0x34769420000098
    ),
    "Southern Swamp Deku Trade Freestanding HP": MMRLocationData(
        region="Southern Swamp",
        address=0x3476942005451E
    ),
    "Southern Swamp Kotake Request": MMRLocationData(
        region="Southern Swamp",
        address=0x34769420000059
    ),
    "Southern Swamp Mystery Woods Grotto Chest": MMRLocationData(
        region="Southern Swamp",
        address=0x3476942006071C
    ),
    "Southern Swamp Koume Tour Gift": MMRLocationData(
        region="Southern Swamp",
        address=0x34769420000043
    ),
    "Swamphouse First Room Pot Near Entrance Token": MMRLocationData(
        region="Swamphouse",
        address=0x3476942006271E,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Swamphouse First Room Crawling In Water Token": MMRLocationData(
        region="Swamphouse",
        address=0x34769420062708,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Swamphouse First Room Crawling Right Column Token": MMRLocationData(
        region="Swamphouse",
        address=0x3476942006270F,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Swamphouse First Room Crawling Left Column Token": MMRLocationData(
        region="Swamphouse",
        address=0x34769420062713,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Swamphouse First Room Against Far Wall Token": MMRLocationData(
        region="Swamphouse",
        address=0x34769420062700,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Swamphouse First Room Left Bugpatch Token": MMRLocationData(
        region="Swamphouse",
        address=0x34769420062709,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Swamphouse First Room Right Bugpatch Token": MMRLocationData(
        region="Swamphouse",
        address=0x3476942006270C,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Swamphouse First Room Upper Right Bugpatch Token": MMRLocationData(
        region="Swamphouse",
        address=0x3476942006270B,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Swamphouse Monument Room Left Crate Token": MMRLocationData(
        region="Swamphouse",
        address=0x3476942006270A,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Swamphouse Monument Room Right Crate Token": MMRLocationData(
        region="Swamphouse",
        address=0x3476942006271B,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Swamphouse Monument Room Crawling Wall Token": MMRLocationData(
        region="Swamphouse",
        address=0x3476942006270D,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Swamphouse Monument Room Crawling On Monument Token": MMRLocationData(
        region="Swamphouse",
        address=0x3476942006270E,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Swamphouse Monument Room Behind Torch Token": MMRLocationData(
        region="Swamphouse",
        address=0x34769420062702,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Swamphouse Pottery Room Beehive #1 Token": MMRLocationData(
        region="Swamphouse",
        address=0x34769420062717,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Swamphouse Pottery Room Beehive #2 Token": MMRLocationData(
        region="Swamphouse",
        address=0x3476942006271C,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Swamphouse Pottery Room Small Pot Token": MMRLocationData(
        region="Swamphouse",
        address=0x34769420062705,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Swamphouse Pottery Room Left Large Pot Token": MMRLocationData(
        region="Swamphouse",
        address=0x34769420062710,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Swamphouse Pottery Room Right Large Pot Token": MMRLocationData(
        region="Swamphouse",
        address=0x34769420062711,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Swamphouse Pottery Room Behind Vines Token": MMRLocationData(
        region="Swamphouse",
        address=0x34769420062714,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Swamphouse Pottery Room Upper Wall Token": MMRLocationData(
        region="Swamphouse",
        address=0x34769420062716,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Swamphouse Golden Room Crawling Left Wall Token": MMRLocationData(
        region="Swamphouse",
        address=0x34769420062719,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Swamphouse Golden Room Crawling Right Column Token": MMRLocationData(
        region="Swamphouse",
        address=0x34769420062704,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Swamphouse Golden Room Against Far Wall Token": MMRLocationData(
        region="Swamphouse",
        address=0x34769420062701,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Swamphouse Golden Room Beehive Token": MMRLocationData(
        region="Swamphouse",
        address=0x34769420062712,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Swamphouse Tree Room Tall Grass #1 Token": MMRLocationData(
        region="Swamphouse",
        address=0x34769420062707,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Swamphouse Tree Room Tall Grass #2 Token": MMRLocationData(
        region="Swamphouse",
        address=0x34769420062706,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Swamphouse Tree Room Tree #1 Token": MMRLocationData(
        region="Swamphouse",
        address=0x34769420062715,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Swamphouse Tree Room Tree #2 Token": MMRLocationData(
        region="Swamphouse",
        address=0x34769420062718,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Swamphouse Tree Room Tree #3 Token": MMRLocationData(
        region="Swamphouse",
        address=0x3476942006271D,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Swamphouse Tree Room Beehive Token": MMRLocationData(
        region="Swamphouse",
        address=0x3476942006271A,
        can_create=lambda options: options.skullsanity.value != 2
    ),
    "Swamphouse Reward": MMRLocationData(
        region="Swamphouse",
        address=0x3476942000008A
    ),
    "Southern Swamp Near Swamphouse Grotto Chest": MMRLocationData(
        region="Southern Swamp (Deku Palace)",
        address=0x3476942006071D
    ),
    "Southern Swamp Song Tablet": MMRLocationData(
        region="Southern Swamp (Deku Palace)",
        address=0x3476942004006A
    ),
    "Deku Palace HP": MMRLocationData(
        region="Deku Palace",
        address=0x34769420052B1E
    ),
    "Deku Palace Bean Grotto Chest": MMRLocationData(
        region="Deku Palace",
        address=0x34769420060705
    ),
    "Deku Palace Monkey Song": MMRLocationData(
        region="Deku Palace",
        address=0x34769420040061
    ),
    "Deku Palace Butler Race": MMRLocationData(
        region="Southern Swamp (Deku Palace)",
        address=0x3476942000008E
    ),
    "Woodfall Near Owl Statue Chest": MMRLocationData(
        region="Woodfall",
        address=0x34769420064602
    ),
    "Woodfall After Great Fairy Cave Chest": MMRLocationData(
        region="Woodfall",
        address=0x34769420064601
    ),
    "Woodfall Near Swamp Entrance Chest": MMRLocationData(
        region="Woodfall",
        address=0x34769420064600
    ),
    "Woodfall Great Fairy Reward": MMRLocationData(
        region="Woodfall",
        address=0x34769420030001
    ),
    "Woodfall Temple Entrance Chest": MMRLocationData(
        region="Woodfall Temple",
        address=0x34769420061B18
    ),
    "Woodfall Temple Moving Flower Platform Room Chest": MMRLocationData(
        region="Woodfall Temple",
        address=0x34769420061B01
    ),
    "Woodfall Temple Gagwab Chest": MMRLocationData(
        region="Woodfall Temple",
        address=0x34769420061B1D
    ),
    "Woodfall Temple Dragonfly Chest": MMRLocationData(
        region="Woodfall Temple",
        address=0x34769420061B1C
    ),
    "Woodfall Temple Black Boe Room Chest": MMRLocationData(
        region="Woodfall Temple",
        address=0x34769420061B19
    ),
    "Woodfall Temple Wooden Flower Switch Chest": MMRLocationData(
        region="Woodfall Temple",
        address=0x34769420061B17
    ),
    "Woodfall Temple Dinofols Chest": MMRLocationData(
        region="Woodfall Temple",
        address=0x34769420061B1B
    ),
    "Woodfall Temple Boss Key Chest": MMRLocationData(
        region="Woodfall Temple",
        address=0x34769420061B1E
    ),
    "Woodfall Temple Entrance Freestanding SF": MMRLocationData(
        region="Woodfall Temple",
        address=0x34769420011B2B
    ),
    "Woodfall Temple Wooden Flower Deku Baba SF": MMRLocationData(
        region="Woodfall Temple",
        address=0x34769420011B2E
    ),
    "Woodfall Temple Wooden Flower Pot SF": MMRLocationData(
        region="Woodfall Temple",
        address=0x34769420011B1C
    ),
    "Woodfall Temple Moving Flower Platform Room Beehive SF": MMRLocationData(
        region="Woodfall Temple",
        address=0x34769420011B1E
    ),
    "Woodfall Temple Wooden Flower Bubble SF": MMRLocationData(
        region="Woodfall Temple",
        address=0x34769420011B30
    ),
    "Woodfall Temple Push Block Skulltula SF": MMRLocationData(
        region="Woodfall Temple",
        address=0x34769420011B31
    ),
    "Woodfall Temple Push Block Bubble SF": MMRLocationData(
        region="Woodfall Temple",
        address=0x34769420011B2F
    ),
    "Woodfall Temple Push Block Beehive SF": MMRLocationData(
        region="Woodfall Temple",
        address=0x34769420011B1D
    ),
    "Woodfall Temple Final Room Right Lower Platform SF": MMRLocationData(
        region="Woodfall Temple",
        address=0x34769420011B2A
    ),
    "Woodfall Temple Final Room Right Upper Platform SF": MMRLocationData(
        region="Woodfall Temple",
        address=0x34769420011B32
    ),
    "Woodfall Temple Final Room Left Upper Platform SF": MMRLocationData(
        region="Woodfall Temple",
        address=0x34769420011B2C
    ),
    "Woodfall Temple Final Room Bubble SF": MMRLocationData(
        region="Woodfall Temple",
        address=0x34769420011B2D
    ),
    "Woodfall Temple Heart Container": MMRLocationData(
        region="Woodfall Temple",
        address=0x34769420051F00
    ),
    "Woodfall Temple Odolwa's Remains": MMRLocationData(
        region="Woodfall Temple",
        address=0x34769420000055
    ),
    # ~ "Mountain Deku Trade": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x34769420000099
    # ~ ),
    # ~ "Ocean Deku Trade": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x3476942000009A
    # ~ ),
    # ~ "Mountain Deku Trade Freestanding HP": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x34769420054D1E
    # ~ ),
    # ~ "Ocean Deku Trade Freestanding HP": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x34769420054C1E
    # ~ ),
    # ~ "Canyon Deku Trade Freestanding HP": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x3476942005131E
    # ~ ),
    # ~ "Great Bay Scarecrow Ledge HP": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x34769420053705
    # ~ ),
    # ~ "Pirates' Fortress Tunnels HP": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x3476942005230C
    # ~ ),
    # ~ "Zora Cape Underwater Like-Like HP": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x34769420053807
    # ~ ),
    # ~ "Ikana Castle Pillar Freestanding HP": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x34769420051D0A
    # ~ ),
    # ~ "Snowhead Temple Initial Runway Under Platform Bubble SF": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x3476942001212F
    # ~ ),
    # ~ "Snowhead Temple Initial Runway Tower Bubble SF": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x34769420012130
    # ~ ),
    # ~ "Snowhead Temple Elevator Freestanding SF": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x34769420012132
    # ~ ),
    # ~ "Snowhead Temple Grey Door Box SF": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x3476942001211E
    # ~ ),
    # ~ "Snowhead Temple Timed Switch Room Bubble SF": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x3476942001212C
    # ~ ),
    # ~ "Snowhead Temple Snowman Bubble SF": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x3476942001212B
    # ~ ),
    # ~ "Snowhead Temple Dinofols Room First SF": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x34769420012131
    # ~ ),
    # ~ "Snowhead Temple Dinofols Room Second SF": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x3476942001212D
    # ~ ),
    # ~ "Great Bay Temple Waterwheel Room Skulltula SF": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x34769420014932
    # ~ ),
    # ~ "Great Bay Temple Waterwheel Room Bubble SF": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x34769420014930
    # ~ ),
    # ~ "Great Bay Temple Blender Room Barrel SF": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x3476942001491C
    # ~ ),
    # ~ "Great Bay Temple Red-Green Pipe First Room SF": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x3476942001491E
    # ~ ),
    # ~ "Great Bay Temple Froggy Entrance Room Pot SF": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x3476942001491D
    # ~ ),
    # ~ "Great Bay Temple Green Pipe Lever Room Underwater Barrel SF": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x3476942001491A
    # ~ ),
    # ~ "Great Bay Temple SF (?)": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x3476942001492F
    # ~ ),
    "Road to Ikana Pillar Chest": MMRLocationData(
        region="Termina Field",
        address=0x34769420065300
    ),
    "Road to Ikana Rock Grotto Chest": MMRLocationData(
        region="Termina Field",
        address=0x34769420060716
    ),
    "Road to Ikana Stone Soldier": MMRLocationData(
        region="Termina Field",
        address=0x3476942000008B
    ),
    # ~ "Graveyard Day 1 Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x34769420060C03
    # ~ ),
    # ~ "Graveyard Day 2 Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x34769420060C00
    # ~ ),
    # ~ "Graveyard Day 3 Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x34769420063000
    # ~ ),
    # ~ "Graveyard Skull Keeta Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x34769420064300
    # ~ ),
    # ~ "Mountain Village Darmani": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x34769420000079
    # ~ ),
    # ~ "Great Bay Mikau": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x3476942000007A
    # ~ ),
    # ~ "The Moon Majora All Masks": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x3476942000007B
    # ~ ),
    # ~ "Ikana Canyon Pamela's Father": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x34769420000087
    # ~ ),
    # ~ "Mountain Village Hungry Goron": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x34769420000088
    # ~ ),
    # ~ "Road to Ikana Invisible Guard": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x3476942000008B
    # ~ ),
    # ~ "Twin Islands Ramp Grotto Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x34769420060719
    # ~ ),
    # ~ "Twin Islands Hot Water Grotto Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x34769420060702
    # ~ ),
    # ~ "Goron Village Lens Cave Rock Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x34769420060706
    # ~ ),
    # ~ "Goron Village Lens Cave Invisible Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x34769420060703
    # ~ ),
    # ~ "Goron Village Lens Cave Center Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x34769420060701
    # ~ ),
    # ~ "Snowhead Temple Initial Runway Ice Owls Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x34769420062101
    # ~ ),
    # ~ "Snowhead Temple Elevator Room Lower Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x3476942006211D
    # ~ ),
    # ~ "Snowhead Temple Bottom Floor Switch Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x34769420062114
    # ~ ),
    # ~ "Snowhead Temple Green Door Ice Owls Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x34769420062118
    # ~ ),
    # ~ "Snowhead Temple Orange Door Behind Block Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x34769420062103
    # ~ ),
    # ~ "Snowhead Temple Orange Door Upper Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x34769420062115
    # ~ ),
    # ~ "Snowhead Temple Grey Door Center Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x3476942006211C
    # ~ ),
    # ~ "Snowhead Temple Grey Door Upper Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x34769420062119
    # ~ ),
    # ~ "Snowhead Temple Upstairs 2F Icicle Room Hidden Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x34769420062116
    # ~ ),
    # ~ "Snowhead Temple Upstairs 2F Icicle Room Snowball Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x34769420062104
    # ~ ),
    # ~ "Snowhead Temple Wizzrobe Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x3476942006211E
    # ~ ),
    # ~ "Snowhead Temple Column Room 2F Hidden Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x34769420062117
    # ~ ),
    # ~ "Mountain Village Spring Waterfall Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x34769420065A00
    # ~ ),
    # ~ "Mountain Village Spring Ramp Grotto": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x3476942006071B
    # ~ ),
    # ~ "Twin Islands Spring Underwater Cave Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x34769420065E00
    # ~ ),
    # ~ "Twin Islands Spring Underwater Center Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x34769420065E06
    # ~ ),
    # ~ "Pirates' Fortress Exterior Underwater Log Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x34769420063B00
    # ~ ),
    # ~ "Pirates' Fortress Exterior Underwater Near Entrance Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x34769420063B01
    # ~ ),
    # ~ "Pirates' Fortress Exterior Underwater Corner Near Fortress Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x34769420063B02
    # ~ ),
    # ~ "Pirates' Fortress Tunnels Cage Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x34769420062301
    # ~ ),
    # ~ "Pirates' Fortress Tunnels Mines Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x34769420062304
    # ~ ),
    # ~ "Pirates' Fortress Tunnels Lower Mines Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x34769420062306
    # ~ ),
    # ~ "Pirates' Fortress Near Egg Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x34769420062300
    # ~ ),
    # ~ "Pirates' Fortress Pirates Surrounding Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x34769420062303
    # ~ ),
    # ~ "Pirates' Fortress Hub Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x34769420061400
    # ~ ),
    # ~ "Pirates' Fortress Hub Upper Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x34769420061401
    # ~ ),
    # ~ "Pirates' Fortress Leader's Room Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x34769420062302
    # ~ ),
    # ~ "Zora Cape Near Great Fairy Grotto Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x34769420060715
    # ~ ),
    # ~ "Great Bay Temple Four Torches Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x34769420064918
    # ~ ),
    # ~ "Great Bay Temple Eye Miniboss Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x3476942006491B
    # ~ ),
    # ~ "Great Bay Temple Red-Green Pipe First Room Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x3476942006491D
    # ~ ),
    # ~ "Great Bay Temple Bio-Baba Hall Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x34769420064919
    # ~ ),
    # ~ "Great Bay Temple Froggy Entrance Room Upper Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x3476942006491C
    # ~ ),
    # ~ "Great Bay Temple Froggy Entrance Room Underwater Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x34769420064901
    # ~ ),
    # ~ "Great Bay Temple Froggy Entrance Room Caged Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x3476942006491E
    # ~ ),
    # ~ "Great Bay Temple Green-Yellow Pipe Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x34769420064915
    # ~ ),
    # ~ "Great Bay Temple Green Pipe Freezable Waterwheel Upper Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x34769420064914
    # ~ ),
    # ~ "Great Bay Temple Green Pipe Freezable Waterwheel Lower Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x34769420064917
    # ~ ),
    # ~ "Great Bay Temple Green Pipe Lever Room Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x34769420064916
    # ~ ),
    # ~ "Secret Shrine Left Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x34769420066000
    # ~ ),
    # ~ "Secret Shrine Middle-Left Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x34769420066001
    # ~ ),
    # ~ "Secret Shrine Middle-Right Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x34769420066002
    # ~ ),
    # ~ "Secret Shrine Right Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x34769420066003
    # ~ ),
    # ~ "Secret Shrine Center Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x3476942006600A
    # ~ ),
    # ~ "Secret Shrine Grotto Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x34769420060714
    # ~ ),
    # ~ "Ikana Well Final Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x34769420064B1B
    # ~ ),
    # ~ "Ikana Well Invisible Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x34769420064B02
    # ~ ),
    # ~ "Ikana Well Torch Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x34769420064B01
    # ~ ),
    # ~ "Stone Tower Inverted Outside Left Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x3476942006591F
    # ~ ),
    # ~ "Stone Tower Inverted Outside Middle Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x3476942006591E
    # ~ ),
    # ~ "Stone Tower Inverted Outside Right Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x3476942006591D
    # ~ ),
    # ~ "Stone Tower Temple First Room Center Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x34769420061616
    # ~ ),
    # ~ "Stone Tower Temple First Room Lower Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x34769420061612
    # ~ ),
    # ~ "Stone Tower Temple Armos Room Lava Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x34769420061602
    # ~ ),
    # ~ "Stone Tower Temple Armos Room Back Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x3476942006161D
    # ~ ),
    # ~ "Stone Tower Temple Armos Room Upper Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x34769420061615
    # ~ ),
    # ~ "Stone Tower Temple Eyegore Room Switch Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x34769420061618
    # ~ ),
    # ~ "Stone Tower Temple Eastern Water Room Sun Block Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x3476942006161C
    # ~ ),
    # ~ "Stone Tower Temple Eastern Water Room Underwater Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x34769420061617
    # ~ ),
    # ~ "Stone Tower Temple Wall Suns Room Sun Block Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x3476942006160B
    # ~ ),
    # ~ "Stone Tower Temple Wall Suns Room Center Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x3476942006160F
    # ~ ),
    # ~ "Stone Tower Temple Wall Air Gust Room Side Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x34769420061619
    # ~ ),
    # ~ "Stone Tower Temple Wall Air Gust Room End Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x3476942006160D
    # ~ ),
    # ~ "Stone Tower Temple Garo Master Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x3476942006161B
    # ~ ),
    # ~ "Stone Tower Temple After Garo Upside Down Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x34769420061614
    # ~ ),
    # ~ "Stone Tower Temple Eyegore Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x3476942006160C
    # ~ ),
    # ~ "Stone Tower Temple Inverted First Room Lower Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x34769420061810
    # ~ ),
    # ~ "Stone Tower Temple Inverted Eastern Air Gust Room Fire Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x3476942006180E
    # ~ ),
    # ~ "Stone Tower Temple Inverted Eastern Air Gust Room Snugly Tucked Cranny Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x34769420061813
    # ~ ),
    # ~ "Stone Tower Temple Inverted Eastern Air Gust Room Hall Floor Switch Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x34769420061804
    # ~ ),
    # ~ "Stone Tower Temple Inverted Wizzrobe Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x34769420061811
    # ~ ),
    # ~ "Stone Tower Temple Inverted Death Armos Maze Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x34769420061805
    # ~ ),
    # ~ "Stone Tower Temple Inverted Gomess Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x3476942006181E
    # ~ ),
    # ~ "Stone Tower Temple Inverted Eyegore Chest": MMRLocationData(
        # ~ region="Clock Town",
        # ~ address=0x3476942006181A
    # ~ ),
    "Defeat Majora": MMRLocationData(
        region="The Moon",
        locked_item="Victory"
    ),
}

location_table = {name: data.address for name, data in location_data_table.items() if data.address is not None}
code_to_location_table = {data.address: name for name, data in location_data_table.items() if data.address is not None}
locked_locations = {name: data for name, data in location_data_table.items() if data.locked_item}
