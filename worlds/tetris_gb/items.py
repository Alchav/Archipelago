from BaseClasses import ItemClassification

items = {
    "Score Multiplier": ItemClassification.progression,
    "Decrease Speed": ItemClassification.progression | ItemClassification.useful,
    "Increase Speed": ItemClassification.trap,
    "Toggle Next Piece": ItemClassification.trap | ItemClassification.useful,
    "Show Next Piece": ItemClassification.useful,
    "Hide Next Piece": ItemClassification.trap,
    "Garbage Line": ItemClassification.trap,
    "Shuffle Garbage Line Hole": ItemClassification.trap

}

item_name_to_id = {item: code for code, item in enumerate(items.keys(), start=1)}