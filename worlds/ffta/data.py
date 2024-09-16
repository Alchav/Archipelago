
from random import Random
from typing import List, NamedTuple, Optional, Set


class FFTAObject:
    memory = 0
    displayName = ''

    def __init__(world, memory, displayName):
        world.memory = memory
        world.displayName = displayName


human_jobs = [0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C]
bangaa_jobs = [0x0D, 0x0E, 0x0F, 0x10, 0x11, 0x12, 0x13]
mou_jobs = [0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1A, 0x1B]
viera_jobs = [0x1C, 0x1D, 0x1E, 0x1F, 0x20, 0x21, 0x22, 0x23]
moogle_jobs = [0x24, 0x25, 0x26, 0x27, 0x28, 0x29, 0x2A, 0x2B]
monster_jobs = [0x2C, 0x2D, 0x2E, 0x2F, 0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39, 0x3A,
                0x3B, 0x3C, 0x3D, 0x3E, 0x3F, 0x40, 0x41, 0x42, 0x43, 0x44, 0x45, 0x46, 0x47]

all_jobs = human_jobs + bangaa_jobs + mou_jobs + viera_jobs + moogle_jobs
all_jobs_with_monster = human_jobs + bangaa_jobs + mou_jobs + viera_jobs + moogle_jobs + monster_jobs
attacker_jobs = [0x02, 0x03, 0x04, 0x05, 0x06, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F, 0x10, 0x11, 0x13, 0x1C, 0x21, 0x22, 0x23,
                 0x25, 0x26, 0x27, 0x28, ]
magic_jobs = [0x08, 0x09, 0x0A, 0x12, 0x15, 0x17, 0x18, 0x1B, 0x1D, 0x1E, 0x20, 0x2A]
support_jobs = [0x07, 0x14, 0x16, 0x1F, 0x24, 0x2B]

mission_item_memory = 0x2002B08
mission_items = []
for i in range(64):
    mission_items.append(mission_item_memory)
    mission_item_memory = mission_item_memory + 0x04


class MissionOffsets:
    type = 0x02
    rank = 0x03
    cancellation = 0x04
    unlockflag1 = 0x05
    unlockflag2 = 0x08
    unlockflag3 = 0x0b
    pub_visibility = 0x0e
    days_available = 0x0f
    rewardItem1 = 0x22
    rewardItem2 = 0x24
    cardItem1 = 0x26
    cardItem2 = 0x28
    clan_reward = 0x2A
    gil_reward = 0x33
    ap_reward = 0x34
    recruit = 0x35
    required_item1 = 0x36
    required_item2 = 0x37
    required_skill = 0x38
    required_job = 0x39
    price = 0x3e
    timeout_days = 0x40
    mission_display = 0x41
    dispatch_ability = 0x43 # Set to 0 for all to be jumpy time
    mission_location = 0x45


class FFTAMission(FFTAObject):

    def __init__(world, memory, name: Optional[str]):
        world.memory = memory
        world.name = name


class JobOffsets:
    sprite_index = 0x07
    equip_items = 0x2D
    ability_start = 0x2E
    ability_end = 0x2F
    job_requirement = 0x30


class AbilityOffsets:
    mp_cost = 0x04
    weapon_required = 0x05


class UnitOffsets:
    type = 0x00
    job = 0x01
    level = 0x03
    unit_item1 = 0x08
    unit_item2 = 0x0a
    unit_item3 = 0x0c
    unit_item4 = 0x0e
    unit_item5 = 0x10
    abilities = 0x14
    ability_reaction = 0x28
    ability_support = 0x29

class UnitBattleOffsets:
    #0x00 is name string
    character_id = 0x004
    first_item = 0x02A
    status_3 = 0x0EA


class JobID:
    soldier = 0x02
    paladin = 0x03
    fighter = 0x04
    thiefhum = 0x05
    ninja = 0x06
    whitemagehum = 0x07
    blackmagehum = 0x08
    illusionisthum = 0x09
    bluemage = 0x0A
    archerhum = 0x0B
    hunter = 0x0C
    warrior = 0x0D
    dragoon = 0x0E
    defender = 0x0F
    gladiator = 0x10
    whitemonk = 0x11
    bishop = 0x12
    templar = 0x13
    whitemagemou = 0x14
    blackmagemou = 0x15
    timemagemou = 0x16
    illusionistmou = 0x17
    alchemist = 0x18
    beastmaster = 0x19
    morpher = 0x1A
    sage = 0x1B
    fencer = 0x1C
    elementalist = 0x1D
    redmage = 0x1E
    whitemagevra = 0x1F
    summoner = 0x20
    archervra = 0x21
    assassin = 0x22
    sniper = 0x23
    animist = 0x24
    mogknight = 0x25
    gunner = 0x26
    thiefmog = 0x27
    juggler = 0x28
    gadgeteer = 0x29
    blackmagemog = 0x2A
    timemagemog = 0x2B

    #Monsters
    goblin = 0x2C
    red_cap = 0x2D
    jelly = 0x2E
    ice_flan = 0x2F
    cream = 0x30
    bomb = 0x31
    grenade = 0x32
    icedrake = 0x33
    firewyrm = 0x34
    thundrake = 0x35
    lamia = 0x36
    lilith = 0x37
    antlion = 0x38
    jawbreaker = 0x39
    toughskin = 0x3A
    blade_biter = 0x3B
    tonberry = 0x3C
    masterberry = 0x3D
    red_panther = 0x3E
    coeurl = 0x3F
    malboro = 0x40
    big_malboro = 0x41
    floateye = 0x42
    ahriman = 0x43
    zombie = 0x44
    vampire = 0x45
    sprite = 0x46
    titania = 0x47


def master_abilities(address, index):
    address | (1 << index)

class UnitType:
    normal = 0x01
    marche = 0x02
    judge1 = 0x5A

class LocationData(NamedTuple):
    name: str
    label: str
    rom_address: int
    flag: int
    tags: Set[str]


class MemorySpace(NamedTuple):
    offset: int
    byteSize: int
    length: int


class Items(MemorySpace):
    offset = 0x51d1a0
    byteSize = 0x20
    length = 375


class MissionNames(MemorySpace):
    offset = 0x55a64c
    byteSize = 0x4
    length = 0x196

class Jobs(MemorySpace):
    offset = 0x521A14
    byteSize = 0x34
    length = 0x73


class Formation(MemorySpace):
    offset = 0x52cde0
    byteSize = 0x30
    length = 0xA46
    #414 original length


class UnitInBattle(MemorySpace):
    offset = 0x2000080
    byteSize = 0x108
    length = 6
    #Maybe see if it applies to enemy units as well?


class Missions(MemorySpace):
    # 0x55ae4c original offset
    # 0x196 original length
    offset = 0x55af1e
    byteSize = 0x46
    length = 0x196


class Abilities(MemorySpace):
    offset = 0x55187C
    byteSize = 0x1C
    length = 0x15A


class HumanAbilities(MemorySpace):
    offset = 0x51bb6c
    byteSize = 0x8
    length = 0x8c


class BangaaAbilities(MemorySpace):
    offset = 0x51bfdc
    byteSize = 0x8
    length = 0x4c


class NuMouAbilities(MemorySpace):
    offset = 0x51c244
    byteSize = 0x8
    length = 0x5e


class VieraAbilities(MemorySpace):
    offset = 0x51c53c
    byteSize = 0x8
    length = 0x54


class MoogleAbilities(MemorySpace):
    offset = 0x51c7e4
    byteSize = 0x8
    length = 0x57


class FFTAFormations(FFTAObject):

    def __init__(world, memory):
        world.memory = memory


class FFTAJobs(FFTAObject):

    def __init__(world, memory):
        world.memory = memory


class FFTAAbility(FFTAObject):

    def __init__(world, memory):
        world.memory = memory


class FFTARaceAbility(FFTAObject):

    def __init__(world, memory):
        world.memory = memory


class FFTAData:
    rom: bytearray
    #itemJobNames: List[str]
    #abilityNames: List[str]
    missionNames: List[str]
    #locations: Dict[str, LocationData]
    #animations: List[int]
    formations: List[FFTAFormations]
    missions: List[FFTAMission]
    abilities: List[FFTAAbility]
    human_abilities: List[FFTARaceAbility]
    bangaa_abilities: List[FFTARaceAbility]
    numou_abilities: List[FFTARaceAbility]
    viera_abilities: List[FFTARaceAbility]
    moogle_abilities: List[FFTARaceAbility]
    all_abilities: List[FFTARaceAbility]
    jobs: List[FFTAJobs]


    def __init__(world, buffer: bytearray):
        world.rom = buffer
        #world.itemJobNames = world.initializeItemNames()
        #world.abilityNames = world.initializeAbilityNames()
        #world.missionNames = world.initializeMissionNames()
        world.formations = world.initializeFormations()
        world.missions = world.initializeMissions()
        world.abilities = world.initializeAbilities()
        world.human_abilities = world.initializeHumanAbilities()
        world.bangaa_abilities = world.initializeBangaaAbilities()
        world.numou_abilities = world.initializeNuMouAbilities()
        world.viera_abilities = world.initializeVieraAbilities()
        world.moogle_abilities = world.initializeMoogleAbilities()
        world.all_abilities = world.human_abilities + world.bangaa_abilities + world.numou_abilities + world.viera_abilities + world.moogle_abilities
        world.jobs = world.initializeJobs()
        #world.lawSets = world.initializeLawSets()

    def initializeMissions(world):
        missions = []
        dataType = Missions(0x55af1e, 0x46, 0x196)
        for n in range(dataType.length):
            memory = dataType.offset + dataType.byteSize * n

            new_item = FFTAMission(memory, "Name")

            missions.append(new_item)

        return missions

    def initializeFormations(world):
        formations = []
        #414 original length
        dataType = Formation(0x52cde0, 0x30, 0xA46)
        for n in range(dataType.length):
            memory = dataType.offset + dataType.byteSize * n

            new_item = FFTAFormations(memory)

            formations.append(new_item)

        return formations

    def initializeJobs(world):
        jobs = []

        dataType = Jobs(0x521A14, 0x34, 0x73)
        for n in range(dataType.length):
            memory = dataType.offset + dataType.byteSize * n

            new_item = FFTAJobs(memory)

            jobs.append(new_item)

        return jobs

    def initializeAbilities(world):
        abilities = []

        dataType = Abilities(0x55187c, 0x1c, 0x15a)
        for n in range(dataType.length):
            memory = dataType.offset + dataType.byteSize * n

            new_item = FFTAAbility(memory)

            abilities.append(new_item)

        return abilities

    def initializeHumanAbilities(world):
        human_abilities = []
        dataType = HumanAbilities(0x51bb6c, 0x8, 0x8c)
        for n in range(dataType.length):
            memory = dataType.offset + dataType.byteSize * n

            new_item = FFTARaceAbility(memory)

            human_abilities.append(new_item)

        return human_abilities

    def initializeBangaaAbilities(world):
        bangaa_abilities = []
        dataType = BangaaAbilities(0x51bfdc, 0x8, 0x4c)
        for n in range(dataType.length):
            memory = dataType.offset + dataType.byteSize * n

            new_item = FFTARaceAbility(memory)

            bangaa_abilities.append(new_item)

        return bangaa_abilities

    def initializeNuMouAbilities(world):
        numou_abilities = []
        dataType = NuMouAbilities(0x51c244, 0x8, 0x5e)
        for n in range(dataType.length):
            memory = dataType.offset + dataType.byteSize * n

            new_item = FFTARaceAbility(memory)

            numou_abilities.append(new_item)

        return numou_abilities

    def initializeVieraAbilities(world):
        viera_abilities = []
        dataType = VieraAbilities(0x51c53c, 0x8, 0x54)
        for n in range(dataType.length):
            memory = dataType.offset + dataType.byteSize * n

            new_item = FFTARaceAbility(memory)

            viera_abilities.append(new_item)

        return viera_abilities

    def initializeMoogleAbilities(world):
        moogle_abilities = []
        dataType = MoogleAbilities(0x51c7e4, 0x8, 0x57)
        for n in range(dataType.length):
            memory = dataType.offset + dataType.byteSize * n

            new_item = FFTARaceAbility(memory)

            moogle_abilities.append(new_item)

        return moogle_abilities

    #def initializeMissionNames(world):
        #names = []
       # dataType = MissionNames()
        #for n in range(dataType.length):
           # memory = dataType.offset + dataType.byteSize * n
           # stringLookUpTable = world.rom.slice(memory, memory + dataType.byteSize)

            #address = FFTAUtils.getLittleEndianAddress(stringLookUpTable)

            #startingByte = address
            #endingByte = startingByte

            #Change into do while somehow
            #endingByte += 0x01
            #while world.rom[endingByte != 0]:
            #    endingByte += 0x01

            #names.append(FFTAUtils.decodeFFTAText(world.rom.slice(startingByte, endingByte)))

       # return names


def get_random_job(random: Random, random_pool: int):
    human = 0
    bangaa = 1
    mou = 2
    viera = 3
    moogle = 4
    monster = 5
    all = 6
    all_with_monster = 7

    random_job: int

    if random_pool == human:
        random_job = random.choice(human_jobs)
        return random_job

    elif random_pool == bangaa:
        random_job = random.choice(bangaa_jobs)
        return random_job

    elif random_pool == mou:
        random_job = random.choice(mou_jobs)
        return random_job

    elif random_pool == viera:
        random_job = random.choice(viera_jobs)
        return random_job

    elif random_pool == moogle:
        random_job = random.choice(moogle_jobs)
        return random_job

    elif random_pool == monster:
        random_job = random.choice(monster_jobs)
        return random_job

    elif random_pool == all:
        random_job = random.choice(all_jobs)
        return random_job

    elif random_pool == all_with_monster:
        random_job = random.choice(all_jobs_with_monster)
        return random_job




