def has_sword(state, player):
    return state.has("Progressive Weapon", player, 1)

def has_fork(state, player):
    return state.has("Progressive Weapon", player, count=2)

def has_shovel(state, player):
    return state.has("Progressive Weapon", player, count=3)