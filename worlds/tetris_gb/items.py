from BaseClasses import ItemClassification

items = {
    "Score Multiplier": ItemClassification.progression,
    "Decrease Speed": ItemClassification.progression | ItemClassification.useful,
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
    "Active Piece Locks Instantly": ItemClassification.trap,
    "Active Piece Gets Stuck in the Left Wall": ItemClassification.trap,
    "Active Piece Gets Stuck in the Right Wall": ItemClassification.trap,
    "Instantly Lock Active Piece": ItemClassification.trap,
    **{f"Clear Row {i}": ItemClassification.filler for i in range(17)},
    "Clear All Rows": ItemClassification.useful
}

item_name_to_id = {item: code for code, item in enumerate(items.keys(), start=1)}

# trap_weights = {
#     "Garbage Line": 64,
#     "Shuffle Garbage Line Hole": 8,
#     "1 Frame of Random Inputs": 16,
#     "1 Second of Random Inputs": 8,
#     "2 Seconds of Random Inputs": 4,
#     "3 Seconds of Random Inputs": 2,
#     "4 Seconds of Random Inputs": 1,
#     "Active Piece Gets Stuck in the Left Wall": 16,
#     "Active Piece Gets Stuck in the Right Wall": 16,
#     "Toggle Next Piece": 4
#
# }