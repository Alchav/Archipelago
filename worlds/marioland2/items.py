from BaseClasses import ItemClassification
from .locations import level_name_to_id

items = {
    "Space Zone Progression": ItemClassification.progression,
    "Space Zone Secret": ItemClassification.progression,
    "Tree Zone Progression": ItemClassification.progression,
    "Tree Zone Progression x2": ItemClassification.progression,
    "Tree Zone Secret": ItemClassification.progression,
    "Macro Zone Progression": ItemClassification.progression,
    "Macro Zone Progression x2": ItemClassification.progression,
    "Macro Zone Secret 1": ItemClassification.progression,
    "Macro Zone Secret 2": ItemClassification.progression_skip_balancing,
    "Pumpkin Zone Progression": ItemClassification.progression,
    "Pumpkin Zone Progression x2": ItemClassification.progression,
    "Pumpkin Zone Secret 1": ItemClassification.progression,
    "Pumpkin Zone Secret 2": ItemClassification.progression,
    "Mario Zone Progression": ItemClassification.progression,
    "Mario Zone Progression x2": ItemClassification.progression,
    "Turtle Zone Progression": ItemClassification.progression,
    "Turtle Zone Progression x2": ItemClassification.progression,
    "Turtle Zone Secret": ItemClassification.progression,
    "Tree Coin": ItemClassification.progression_skip_balancing,
    "Space Coin": ItemClassification.progression_skip_balancing,
    "Macro Coin": ItemClassification.progression_skip_balancing,
    "Pumpkin Coin": ItemClassification.progression_skip_balancing,
    "Mario Coin": ItemClassification.progression_skip_balancing,
    "Turtle Coin": ItemClassification.progression_skip_balancing,
    "Mario Coin Fragment": ItemClassification.progression_skip_balancing,
    "Mushroom": ItemClassification.progression,
    "Fire Flower": ItemClassification.progression,
    "Carrot": ItemClassification.progression,
    "Space Physics": ItemClassification.progression_skip_balancing,
    "Hippo Bubble": ItemClassification.progression_skip_balancing,
    "Water Physics": ItemClassification.progression,
    "Pipe Traversal":  ItemClassification.progression,
    "Pipe Traversal - Down":  ItemClassification.progression,
    "Pipe Traversal - Up":  ItemClassification.progression,
    "Pipe Traversal - Right":  ItemClassification.progression,
    "Pipe Traversal - Left":  ItemClassification.progression_skip_balancing,
    "Super Star Duration Increase": ItemClassification.filler,
    "Easy Mode": ItemClassification.useful,
    "Normal Mode": ItemClassification.trap,
    "Auto Scroll": ItemClassification.trap,
    **{f"Auto Scroll - {level}": ItemClassification.trap for level in level_name_to_id if level != "Wario's Castle"},
    "Cancel Auto Scroll": ItemClassification.progression,
    **{f"Cancel Auto Scroll - {level}": ItemClassification.progression for level in level_name_to_id
       if level != "Wario's Castle"},
    "Mushroom Zone Midway Bell": ItemClassification.filler,
    "Tree Zone 1 Midway Bell": ItemClassification.filler,
    "Tree Zone 2 Midway Bell": ItemClassification.progression_skip_balancing,
    "Tree Zone 4 Midway Bell": ItemClassification.progression_skip_balancing,
    "Tree Zone 5 Midway Bell": ItemClassification.filler,
    "Space Zone 1 Midway Bell": ItemClassification.filler,
    "Space Zone 2 Midway Bell": ItemClassification.progression_skip_balancing,
    "Macro Zone 1 Midway Bell": ItemClassification.progression_skip_balancing,
    "Macro Zone 2 Midway Bell": ItemClassification.progression_skip_balancing,
    "Macro Zone 3 Midway Bell": ItemClassification.progression_skip_balancing,
    "Macro Zone 4 Midway Bell": ItemClassification.filler,
    "Pumpkin Zone 1 Midway Bell": ItemClassification.progression_skip_balancing,
    "Pumpkin Zone 2 Midway Bell": ItemClassification.filler,
    "Pumpkin Zone 3 Midway Bell": ItemClassification.filler,
    "Pumpkin Zone 4 Midway Bell": ItemClassification.filler,
    "Mario Zone 1 Midway Bell": ItemClassification.progression_skip_balancing,
    "Mario Zone 2 Midway Bell": ItemClassification.filler,
    "Mario Zone 3 Midway Bell": ItemClassification.filler,
    "Mario Zone 4 Midway Bell": ItemClassification.filler,
    "Turtle Zone 1 Midway Bell": ItemClassification.filler,
    "Turtle Zone 2 Midway Bell": ItemClassification.progression_skip_balancing,
    "Turtle Zone 3 Midway Bell": ItemClassification.filler,
    "Mario's Castle Midway Bell": ItemClassification.progression_skip_balancing,
    "1 Coin": ItemClassification.filler,
    **{f"{i} Coins": ItemClassification.filler for i in range(2, 169)}
}

for level in {"Turtle Zone Secret", "Macro Zone Secret", "Turtle Zone 3", "Scenic Course", "Mario Zone 2"}:
    items[f"Cancel Auto Scroll - {level}"] = ItemClassification.useful
