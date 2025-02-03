from BaseClasses import ItemClassification
from .Types import ItemData

item_table = {
    # Progression
    "Watering Can": ItemData(1, ItemClassification.progression),
    "Boom Boots": ItemData(3, ItemClassification.progression),
    "Fertilizer": ItemData(4, ItemClassification.progression),
    "Flower": ItemData(5, ItemClassification.progression),
    "Rent Money": ItemData(6, ItemClassification.progression),
    "Tier 3 Sub": ItemData(7, ItemClassification.progression),
    "Wood": ItemData(8, ItemClassification.progression),
    "Lost Carrot Baby": ItemData(9, ItemClassification.progression),
    "Stool": ItemData(10, ItemClassification.progression),
    "Face Mask": ItemData(11, ItemClassification.progression),
    "Medicine": ItemData(12, ItemClassification.progression),
    "Bandage": ItemData(13, ItemClassification.progression),
    "Move Mittens": ItemData(14, ItemClassification.progression),
    "Lost Cherry Baby": ItemData(15, ItemClassification.progression),
    "Lost Cat Apple": ItemData(16, ItemClassification.progression),
    "Spray Paint": ItemData(17, ItemClassification.progression),
    "Hammer": ItemData(19, ItemClassification.progression),
    "Holly's Phone": ItemData(20, ItemClassification.progression),
    "Mural Doodle": ItemData(21, ItemClassification.progression),
    "Turnip?": ItemData(22, ItemClassification.progression),
    "Potted Petalportal": ItemData(23, ItemClassification.progression),
    "Green Goop": ItemData(24, ItemClassification.progression),
    "Leaf": ItemData(25, ItemClassification.progression),
    "Real Estate Letter": ItemData(26, ItemClassification.progression),
    # Soil Sword -> Fork -> Shovel
    "Progressive Weapon": ItemData(27, ItemClassification.progression, count=3),
    "Tot's Letter": ItemData(28, ItemClassification.progression),
    "Hair Dye": ItemData(29, ItemClassification.progression),
    "Hazmat Suit": ItemData(30, ItemClassification.progression),
    "Laser Pointer": ItemData(31, ItemClassification.progression),
    "Pop's Letter": ItemData(32, ItemClassification.progression),

    # Useful
    "The Last Slice": ItemData(101, ItemClassification.useful),

    # Filler
    "Sunhat": ItemData(201, ItemClassification.filler),
    "Crown": ItemData(202, ItemClassification.filler),
    "Trophy": ItemData(203, ItemClassification.filler),
    "Hardhat": ItemData(204, ItemClassification.filler),
    "Fedora": ItemData(205, ItemClassification.filler),
    "Explorer Hat": ItemData(206, ItemClassification.filler),
    "Tophat": ItemData(207, ItemClassification.filler),
    "Scissors": ItemData(208, ItemClassification.filler),
    "Bird Hat": ItemData(209, ItemClassification.filler),
    "Farmer Hat": ItemData(210, ItemClassification.filler),
    "DLC Hat": ItemData(211, ItemClassification.filler),
    "Cat Ears": ItemData(212, ItemClassification.filler),
}

# Not currently used anywhere, but still useful as a reference
event_table = {
    "Key": ItemData(None, ItemClassification.progression),
    "Defeat King Pig": ItemData(None, ItemClassification.progression),
    "Deliver Fertilizer": ItemData(None, ItemClassification.progression),
    "Defeat Rotten Cat Apple": ItemData(None, ItemClassification.progression),
    "Restart Generator": ItemData(None, ItemClassification.progression),
    "Deliver Fork": ItemData(None, ItemClassification.progression),
    "Defeat Stag": ItemData(None, ItemClassification.progression),
    "Deliver Goop": ItemData(None, ItemClassification.progression),
    "Defeat Liz": ItemData(None, ItemClassification.progression),
    "Deliver Laser Pointer": ItemData(None, ItemClassification.progression),
    "Defeat Corrupt Onion": ItemData(None, ItemClassification.progression),
}