from worlds.generic.Rules import add_rule, forbid_item
from .Locations import (
    cursor_achievements,
    farm_achievements,
    mine_achievements,
    factory_achievements,
    bank_achievements,
    temple_achievements,
    wizard_tower_achievements,
    shipment_achievements,
    alchemy_lab_achievements,
    portal_achievements,
    time_machine_achievements,
    antimatter_condenser_achievements,
    prism_achievements,
    chancemaker_achievements,
    fractal_engine_achievements,
    javascript_console_achievements,
    idleverse_achievements,
    cortex_baker_achievements,
    you_achievements,
)

CURSOR = "Cursor"
GRANDMA = "Grandma"
FARM = "Farm"
MINE = "Mine"
FACTORY = "Factory"
BANK = "Bank"
TEMPLE = "Temple"
WIZARD_TOWER = "Wizard Tower"
SHIPMENT = "Shipment"
ALCHEMY_LAB = "Alchemy Lab"
PORTAL = "Portal"
TIME_MACHINE = "Time Machine"
ANTIMATTER_CONDENSER = "Antimatter Condenser"
PRISM = "Prism"
CHANCEMAKER = "Chancemaker"
FRACTAL_ENGINE = "Fractal Engine"
JAVASCRIPT_CONSOLE = "Javascript Console"
IDLEVERSE = "Idleverse"
CORTEX_BAKER = "Cortex Baker"
YOU = "You"

# Grandma is always available, so not listed here
building_unlock_items = {
    CURSOR: ("Unlock Cursor", cursor_achievements),
    FARM: ("Unlock Farm", farm_achievements),
    MINE: ("Unlock Mine", mine_achievements),
    FACTORY: ("Unlock Factory", factory_achievements),
    BANK: ("Unlock Bank", bank_achievements),
    TEMPLE: ("Unlock Temple", temple_achievements),
    WIZARD_TOWER: ("Unlock Wizard Tower", wizard_tower_achievements),
    SHIPMENT: ("Unlock Shipment", shipment_achievements),
    ALCHEMY_LAB: ("Unlock Alchemy Lab", alchemy_lab_achievements),
    PORTAL: ("Unlock Portal", portal_achievements),
    TIME_MACHINE: ("Unlock Time Machine", time_machine_achievements),
    ANTIMATTER_CONDENSER: ("Unlock Antimatter Condenser", antimatter_condenser_achievements),
    PRISM: ("Unlock Prism", prism_achievements),
    CHANCEMAKER: ("Unlock Chancemaker", chancemaker_achievements),
    FRACTAL_ENGINE: ("Unlock Fractal Engine", fractal_engine_achievements),
    JAVASCRIPT_CONSOLE: ("Unlock Javascript Console", javascript_console_achievements),
    IDLEVERSE: ("Unlock Idleverse", idleverse_achievements),
    CORTEX_BAKER: ("Unlock Cortex Baker", cortex_baker_achievements),
    YOU: ("Unlock You", you_achievements),
}

sphere0_achievements = [
    "Wake and bake",
    "Making some dough",
    "So baked right now",
    "Clicktastic",
    "Clickathlon",
    "Just wrong",
    "Grandma's cookies",
    "Sloppy kisses",
    "Golden cookie",
    "Lucky cookie",
    "A stroke of luck",
    "Fortune",
    "Early bird",
    "Fading luck",
    "Cookie-dunker",
    "Tiny cookie",
    "What's in a name",
    "Here you go",
    "Tabloid addiction",
    "Stifling the press",
    "Olden days",
    "Uncanny clicker",
    "Cheated cookies taste awful",
    "God complex",
    "Third-party"
]

def set_rules(self: "CookieClicker"):
    world  = self.multiworld
    player = self.player

    # 1) Prevent each “Unlock Building” item from ever appearing in any of that building’s own-achievement locations.
    for building_name, (unlock_item, achievement_list) in building_unlock_items.items():
        for location_name in achievement_list:
            location = world.get_location(location_name, player)
            forbid_item(location, unlock_item, player)

    # 2) Make the “sphere 0” achievements always available
    for location_name in sphere0_achievements:
        location = world.get_location(location_name, player)
        add_rule(location, lambda state: True)

    # TODO: Make sure there's logic, like not have the first check in-logic be "Bake 1 trevigintillion cookies in one ascension."

    # 3) Standard completion check
    def goal_achieved(state):
        return len(state.prog_items[player]) >= self.options.advancement_goal.value

    self.multiworld.completion_condition[player] = goal_achieved
