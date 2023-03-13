from BaseClasses import ItemClassification
from typing import TypedDict, Dict, Set


class ItemDict(TypedDict):
    classification: ItemClassification
    count: int
    name: str
    tech_type: str


item_table: Dict[int, ItemDict] = {
    35000: {'classification': ItemClassification.useful,
            'count': 1,
            'name': 'Compass',
            'tech_type': 'Compass'},
    35001: {'classification': ItemClassification.progression,
            'count': 1,
            'name': 'Lightweight High Capacity Tank',
            'tech_type': 'PlasteelTank'},
    35002: {'classification': ItemClassification.progression,
            'count': 1,
            'name': 'Vehicle Upgrade Console',
            'tech_type': 'BaseUpgradeConsole'},
    35003: {'classification': ItemClassification.progression,
            'count': 1,
            'name': 'Ultra Glide Fins',
            'tech_type': 'UltraGlideFins'},
    35004: {'classification': ItemClassification.useful,
            'count': 1,
            'name': 'Cyclops Sonar Upgrade',
            'tech_type': 'CyclopsSonarModule'},
    35005: {'classification': ItemClassification.useful,
            'count': 1,
            'name': 'Reinforced Dive Suit',
            'tech_type': 'ReinforcedDiveSuit'},
    35006: {'classification': ItemClassification.useful,
            'count': 1,
            'name': 'Cyclops Thermal Reactor Module',
            'tech_type': 'CyclopsThermalReactorModule'},
    35007: {'classification': ItemClassification.filler,
            'count': 1,
            'name': 'Stillsuit',
            'tech_type': 'WaterFiltrationSuitFragment'},
    35008: {'classification': ItemClassification.progression,
            'count': 1,
            'name': 'Alien Containment',
            'tech_type': 'BaseWaterPark'},
    35009: {'classification': ItemClassification.useful,
            'count': 1,
            'name': 'Creature Decoy',
            'tech_type': 'CyclopsDecoy'},
    35010: {'classification': ItemClassification.useful,
            'count': 1,
            'name': 'Cyclops Fire Suppression System',
            'tech_type': 'CyclopsFireSuppressionModule'},
    35011: {'classification': ItemClassification.useful,
            'count': 1,
            'name': 'Swim Charge Fins',
            'tech_type': 'SwimChargeFins'},
    35012: {'classification': ItemClassification.useful,
            'count': 1,
            'name': 'Repulsion Cannon',
            'tech_type': 'RepulsionCannon'},
    35013: {'classification': ItemClassification.useful,
            'count': 1,
            'name': 'Cyclops Decoy Tube Upgrade',
            'tech_type': 'CyclopsDecoyModule'},
    35014: {'classification': ItemClassification.progression,
            'count': 1,
            'name': 'Cyclops Shield Generator',
            'tech_type': 'CyclopsShieldModule'},
    35015: {'classification': ItemClassification.progression,
            'count': 1,
            'name': 'Cyclops Depth Module MK1',
            'tech_type': 'CyclopsHullModule1'},
    35016: {'classification': ItemClassification.useful,
            'count': 1,
            'name': 'Cyclops Docking Bay Repair Module',
            'tech_type': 'CyclopsSeamothRepairModule'},
    35017: {'classification': ItemClassification.useful,
            'count': 2,
            'name': 'Battery Charger fragment',
            'tech_type': 'BatteryChargerFragment'},
    35018: {'classification': ItemClassification.filler,
            'count': 2,
            'name': 'Beacon Fragment',
            'tech_type': 'BeaconFragment'},
    35019: {'classification': ItemClassification.useful,
            'count': 2,
            'name': 'Bioreactor Fragment',
            'tech_type': 'BaseBioReactorFragment'},
    35020: {'classification': ItemClassification.progression,
            'count': 4,
            'name': 'Cyclops Bridge Fragment',
            'tech_type': 'CyclopsBridgeFragment'},
    35021: {'classification': ItemClassification.progression,
            'count': 4,
            'name': 'Cyclops Engine Fragment',
            'tech_type': 'CyclopsEngineFragment'},
    35022: {'classification': ItemClassification.progression,
            'count': 4,
            'name': 'Cyclops Hull Fragment',
            'tech_type': 'CyclopsHullFragment'},
    35023: {'classification': ItemClassification.filler,
            'count': 2,
            'name': 'Grav Trap Fragment',
            'tech_type': 'GravSphereFragment'},
    35024: {'classification': ItemClassification.progression,
            'count': 3,
            'name': 'Laser Cutter Fragment',
            'tech_type': 'LaserCutterFragment'},
    35025: {'classification': ItemClassification.filler,
            'count': 2,
            'name': 'Light Stick Fragment',
            'tech_type': 'TechlightFragment'},
    35026: {'classification': ItemClassification.progression,
            'count': 5,
            'name': 'Mobile Vehicle Bay Fragment',
            'tech_type': 'ConstructorFragment'},
    35027: {'classification': ItemClassification.progression,
            'count': 3,
            'name': 'Modification Station Fragment',
            'tech_type': 'WorkbenchFragment'},
    35028: {'classification': ItemClassification.progression,
            'count': 2,
            'name': 'Moonpool Fragment',
            'tech_type': 'MoonpoolFragment'},
    35029: {'classification': ItemClassification.useful,
            'count': 3,
            'name': 'Nuclear Reactor Fragment',
            'tech_type': 'BaseNuclearReactorFragment'},
    35030: {'classification': ItemClassification.useful,
            'count': 2,
            'name': 'Power Cell Charger Fragment',
            'tech_type': 'PowerCellChargerFragment'},
    35031: {'classification': ItemClassification.filler,
            'count': 1,
            'name': 'Power Transmitter Fragment',
            'tech_type': 'PowerTransmitterFragment'},
    35032: {'classification': ItemClassification.progression,
            'count': 6,
            'name': 'Prawn Suit Fragment',
            'tech_type': 'ExosuitFragment'},
    35033: {'classification': ItemClassification.useful,
            'count': 2,
            'name': 'Prawn Suit Drill Arm Fragment',
            'tech_type': 'ExosuitDrillArmFragment'},
    35034: {'classification': ItemClassification.useful,
            'count': 2,
            'name': 'Prawn Suit Grappling Arm Fragment',
            'tech_type': 'ExosuitGrapplingArmFragment'},
    35035: {'classification': ItemClassification.useful,
            'count': 2,
            'name': 'Prawn Suit Propulsion Cannon Fragment',
            'tech_type': 'ExosuitPropulsionArmFragment'},
    35036: {'classification': ItemClassification.useful,
            'count': 2,
            'name': 'Prawn Suit Torpedo Arm Fragment',
            'tech_type': 'ExosuitTorpedoArmFragment'},
    35037: {'classification': ItemClassification.useful,
            'count': 3,
            'name': 'Scanner Room Fragment',
            'tech_type': 'BaseMapRoomFragment'},
    35038: {'classification': ItemClassification.progression,
            'count': 5,
            'name': 'Seamoth Fragment',
            'tech_type': 'SeamothFragment'},
    35039: {'classification': ItemClassification.progression,
            'count': 2,
            'name': 'Stasis Rifle Fragment',
            'tech_type': 'StasisRifleFragment'},
    35040: {'classification': ItemClassification.useful,
            'count': 2,
            'name': 'Thermal Plant Fragment',
            'tech_type': 'ThermalPlantFragment'},
    35041: {'classification': ItemClassification.progression,
            'count': 4,
            'name': 'Seaglide Fragment',
            'tech_type': 'SeaglideFragment'},
    35042: {'classification': ItemClassification.progression,
            'count': 1,
            'name': 'Radiation Suit',
            'tech_type': 'RadiationSuit'},
    35043: {'classification': ItemClassification.progression,
            'count': 2,
            'name': 'Propulsion Cannon Fragment',
            'tech_type': 'PropulsionCannonFragment'},
    35044: {'classification': ItemClassification.progression_skip_balancing,
            'count': 1,
            'name': 'Neptune Launch Platform',
            'tech_type': 'RocketBase'},
    35045: {'classification': ItemClassification.progression,
            'count': 1,
            'name': 'Ion Power Cell',
            'tech_type': 'PrecursorIonPowerCell'},
    35046: {'classification': ItemClassification.filler,
            'count': 2,
            'name': 'Exterior Growbed',
            'tech_type': 'FarmingTray'},
    35047: {'classification': ItemClassification.filler,
            'count': 1,
            'name': 'Picture Frame',
            'tech_type': 'PictureFrameFragment'},
    35048: {'classification': ItemClassification.filler,
            'count': 1,
            'name': 'Bench',
            'tech_type': 'Bench'},
    35049: {'classification': ItemClassification.filler,
            'count': 1,
            'name': 'Basic Plant Pot',
            'tech_type': 'PlanterPotFragment'},
    35050: {'classification': ItemClassification.filler,
            'count': 1,
            'name': 'Interior Growbed',
            'tech_type': 'PlanterBoxFragment'},
    35051: {'classification': ItemClassification.filler,
            'count': 1,
            'name': 'Plant Shelf',
            'tech_type': 'PlanterShelfFragment'},
    35052: {'classification': ItemClassification.filler,
            'count': 1,
            'name': 'Observatory',
            'tech_type': 'BaseObservatory'},
    35053: {'classification': ItemClassification.progression,
            'count': 1,
            'name': 'Multipurpose Room',
            'tech_type': 'BaseRoom'},
    35054: {'classification': ItemClassification.useful,
            'count': 1,
            'name': 'Bulkhead',
            'tech_type': 'BaseBulkhead'},
    35055: {'classification': ItemClassification.filler,
            'count': 1,
            'name': 'Spotlight',
            'tech_type': 'Spotlight'},
    35056: {'classification': ItemClassification.filler,
            'count': 1,
            'name': 'Desk',
            'tech_type': 'StarshipDesk'},
    35057: {'classification': ItemClassification.filler,
            'count': 1,
            'name': 'Swivel Chair',
            'tech_type': 'StarshipChair'},
    35058: {'classification': ItemClassification.filler,
            'count': 1,
            'name': 'Office Chair',
            'tech_type': 'StarshipChair2'},
    35059: {'classification': ItemClassification.filler,
            'count': 1,
            'name': 'Command Chair',
            'tech_type': 'StarshipChair3'},
    35060: {'classification': ItemClassification.filler,
            'count': 1,
            'name': 'Counter',
            'tech_type': 'LabCounter'},
    35061: {'classification': ItemClassification.filler,
            'count': 1,
            'name': 'Single Bed',
            'tech_type': 'NarrowBed'},
    35062: {'classification': ItemClassification.filler,
            'count': 1,
            'name': 'Basic Double Bed',
            'tech_type': 'Bed1'},
    35063: {'classification': ItemClassification.filler,
            'count': 1,
            'name': 'Quilted Double Bed',
            'tech_type': 'Bed2'},
    35064: {'classification': ItemClassification.filler,
            'count': 1,
            'name': 'Coffee Vending Machine',
            'tech_type': 'CoffeeVendingMachine'},
    35065: {'classification': ItemClassification.filler,
            'count': 1,
            'name': 'Trash Can',
            'tech_type': 'Trashcans'},
    35066: {'classification': ItemClassification.filler,
            'count': 1,
            'name': 'Floodlight',
            'tech_type': 'Techlight'},
    35067: {'classification': ItemClassification.filler,
            'count': 1,
            'name': 'Bar Table',
            'tech_type': 'BarTable'},
    35068: {'classification': ItemClassification.filler,
            'count': 1,
            'name': 'Vending Machine',
            'tech_type': 'VendingMachine'},
    35069: {'classification': ItemClassification.filler,
            'count': 1,
            'name': 'Single Wall Shelf',
            'tech_type': 'SingleWallShelf'},
    35070: {'classification': ItemClassification.filler,
            'count': 1,
            'name': 'Wall Shelves',
            'tech_type': 'WallShelves'},
    35071: {'classification': ItemClassification.filler,
            'count': 1,
            'name': 'Round Plant Pot',
            'tech_type': 'PlanterPot2'},
    35072: {'classification': ItemClassification.filler,
            'count': 1,
            'name': 'Chic Plant Pot',
            'tech_type': 'PlanterPot3'},
    35073: {'classification': ItemClassification.filler,
            'count': 1,
            'name': 'Nuclear Waste Disposal',
            'tech_type': 'LabTrashcan'},
    35074: {'classification': ItemClassification.filler,
            'count': 1,
            'name': 'Wall Planter',
            'tech_type': 'BasePlanter'},
    35075: {'classification': ItemClassification.progression,
            'count': 1,
            'name': 'Ion Battery',
            'tech_type': 'PrecursorIonBattery'},
    35076: {'classification': ItemClassification.progression_skip_balancing,
            'count': 1,
            'name': 'Neptune Gantry',
            'tech_type': 'RocketBaseLadder'},
    35077: {'classification': ItemClassification.progression_skip_balancing,
            'count': 1,
            'name': 'Neptune Boosters',
            'tech_type': 'RocketStage1'},
    35078: {'classification': ItemClassification.progression_skip_balancing,
            'count': 1,
            'name': 'Neptune Fuel Reserve',
            'tech_type': 'RocketStage2'},
    35079: {'classification': ItemClassification.progression_skip_balancing,
            'count': 1,
            'name': 'Neptune Cockpit',
            'tech_type': 'RocketStage3'},
    35080: {'classification': ItemClassification.filler,
            'count': 1,
            'name': 'Water Filtration Machine',
            'tech_type': 'BaseFiltrationMachine'},
    35081: {'classification': ItemClassification.progression,
            'count': 1,
            'name': 'Ultra High Capacity Tank',
            'tech_type': 'HighCapacityTank'},
    35082: {'classification': ItemClassification.progression,
            'count': 1,
            'name': 'Large Room',
            'tech_type': 'BaseLargeRoom'},
    # awarded with their rooms, keeping that as-is as they're cosmetic
    35083: {'classification': ItemClassification.filler,
            'count': 0,
            'name': 'Large Room Glass Dome',
            'tech_type': 'BaseLargeGlassDome'},
    35084: {'classification': ItemClassification.filler,
            'count': 0,
            'name': 'Multipurpose Room Glass Dome',
            'tech_type': 'BaseGlassDome'},
    35085: {'classification': ItemClassification.filler,
            'count': 0,
            'name': 'Partition',
            'tech_type': 'BasePartition'},
    35086: {'classification': ItemClassification.filler,
            'count': 0,
            'name': 'Partition Door',
            'tech_type': 'BasePartitionDoor'},
}

advancement_item_names: Set[str] = set()
non_advancement_item_names: Set[str] = set()

for item_id, item_data in item_table.items():
    item_name = item_data["name"]
    if ItemClassification.progression in item_data["classification"]:
        advancement_item_names.add(item_name)
    else:
        non_advancement_item_names.add(item_name)

if False:  # turn to True to export for Subnautica mod
    from .Locations import location_table
    itemcount = sum(item_data["count"] for item_data in item_table.values())
    assert itemcount == len(location_table), f"{itemcount} != {len(location_table)}"
    payload = {item_id: item_data["tech_type"] for item_id, item_data in item_table.items()}
    import json

    with open("items.json", "w") as f:
        json.dump(payload, f)
