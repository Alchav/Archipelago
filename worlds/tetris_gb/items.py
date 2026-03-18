from BaseClasses import ItemClassification

items = {
    "Score Multiplier": ItemClassification.progression_skip_balancing,
    "Score Multiplier x2": ItemClassification.progression_skip_balancing,
    "Score Multiplier x3": ItemClassification.progression_skip_balancing,
    "Decrease Speed": ItemClassification.progression_skip_balancing | ItemClassification.useful,
    "Increase Speed": ItemClassification.trap,
    "Toggle Next Piece": ItemClassification.trap | ItemClassification.useful,
    "Show Next Piece": ItemClassification.useful,
    "Hide Next Piece": ItemClassification.trap,
    "Garbage Line": ItemClassification.trap,
    "Shuffle Garbage Line Hole": ItemClassification.trap,
    "1 Frame of Random Inputs": ItemClassification.trap,
    "1 Second of Random Inputs": ItemClassification.trap,
    "2 Seconds of Random Inputs": ItemClassification.trap,
    "3 Seconds of Random Inputs": ItemClassification.trap,
    "4 Seconds of Random Inputs": ItemClassification.trap,
    "Active Piece Gets Stuck in the Left Wall": ItemClassification.trap,
    "Active Piece Gets Stuck in the Right Wall": ItemClassification.trap,
    "Instantly Lock Active Piece": ItemClassification.trap,
    "Active Piece is an Illusion": ItemClassification.trap,
    "Clear Random Line": ItemClassification.filler
}

item_name_to_id = {item: code for code, item in enumerate(items.keys(), start=1)}
