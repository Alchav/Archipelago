logic_tricks = {
    # Bob-omb Battlefield
    "Bob-omb Battlefield Island with Wing Cap": {
        "name": "logic_bob_island_without_cannon",
        "difficulty": "easy",
        "description": "Reaching the floating island without the cannon by using Wing Cap and Triple Jump.",
    },
    "Bob-omb Battlefield Island Red Coin With Ground Pound": {
        "name": "logic_bob_island_red_coin_with_ground_pound",
        "difficulty": "easy",
        "description": "Collecting the red coin (and three yellow coins) above the tree on the island"
                       "using Ground Pound",
        "video": "https://www.youtube.com/watch?v=hOHwdJ2UIo0"
    },
    "Bob-omb Battlefield Mario Wings to the Sky without Wing Cap": {
        "name": "logic_bob_mario_wings_capless",
        "difficulty": "medium",
        "description": "Allows Mario Wings to the Sky, and all coins in the sky,"
                       "without Wing Cap when the cannon is unlocked.",
        "video": "https://www.youtube.com/watch?v=iK1Fn8PhRyk"
    },
    "Bob-omb Battlefield Mario Wings to the Sky without Cannon": {
        "name": "logic_bob_mario_wings_to_the_sky_without_cannon",
        "difficulty": "hard",
        "description": "Collecting Mario Wings to the Sky and every coin without Cannon,"
                       "using Wing Cap, Triple Jump, and Ground Pound, by flying off of King Bob-omb's Summit and"
                       "using a Ground Pound just under the highest trigger coin.",
        "video": "https://www.youtube.com/watch?v=vsrevAfIvMA"
    },
    "Bob-omb Battlefield Island with Long Jump": {
        "name": "logic_bob_island_long_jump",
        "difficulty": "hard",
        "description": "Reaching the floating island without the cannon using Long Jump.",
        "video": "https://www.youtube.com/watch?v=9Nr1m61izSs"
    },
    "Bob-omb Battlefield Island with Koopa Shell": {
        "name": "logic_bob_island_koopa_shell",
        "difficulty": "hard",
        "description": "Reaching the floating island (and collecting the red coin on it) without the cannon by"
                       "using the Koopa shell.",
        "video": "https://www.youtube.com/watch?v=l_Xrf8jIyy8"
    },
    "Bob-omb Battlefield Chain Chomp Gate without Ground Pound": {
        "name": "logic_bob_chain_chomp_gate_without_ground_pound",
        "difficulty": "hard",
        "description": "Collecting Behind Chain Chomp's Gate without Ground Pound, using a Bob-omb to clip through"
                       "the gate.",
        "video": "https://www.youtube.com/watch?v=-dZKkhB30LY"
    },
}


logic_trick_difficulty_order = {
    "easy": 0,
    "medium": 1,
    "hard": 2,
}

logic_trick_presets = (
    "All Easy Tricks",
    "All Medium Tricks",
    "All Hard Tricks",
)


def get_enabled_logic_tricks(selected_tricks: set[str]) -> set[str]:
    enabled_tricks = {trick for trick in selected_tricks if trick in logic_tricks}
    selected_difficulties = {
        preset.removeprefix("All ").removesuffix(" Tricks").lower()
        for preset in logic_trick_presets
        if preset in selected_tricks
    }
    if selected_difficulties:
        maximum_difficulty = max(logic_trick_difficulty_order[difficulty] for difficulty in selected_difficulties)
        enabled_tricks.update(
            trick for trick, data in logic_tricks.items()
            if logic_trick_difficulty_order[data["difficulty"]] <= maximum_difficulty
        )
    return enabled_tricks


logic_trick_option_keys = logic_trick_presets + tuple(logic_tricks)
