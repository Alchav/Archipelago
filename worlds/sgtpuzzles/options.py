from Options import Choice, CommonOptions, DefaultOnToggle, ExcludeLocations, ItemLinks, LocalItems, \
    NonLocalItems, OptionGroup, PriorityLocations, StartHints, StartInventory, StartLocationHints, Toggle, Range, \
    OptionDict, StartInventoryPool
from dataclasses import dataclass
from .items import max_puzzles

from schema import Schema, Optional, And, Or, Any

genres = [
    "blackbox","bridges","cube","dominosa","fifteen","filling","flip","flood","galaxies",
    "group","guess","inertia","keen","lightup","loopy","magnets","map","mines","mosaic","net",
    "netslide","palisade","pattern","pearl","pegs","range","rect","samegame","signpost",
    "singles","sixteen","slant","solo","tents","towers","tracks","twiddle","undead",
    "unequal","unruly","untangle"
]

# Each genre lists tuples specifying a parameter string, its weight, and its difficulty.
genrePresets = {
    "blackbox": [
        ("w5h5m3M3", 1, 0),
        ("w8h8m5M5", 1, 1),
        ("w8h8m3M6", 1, 1),
        ("w10h10m5M5", 1, 2),
        ("w10h10m4M10", 1, 2)
    ],
    "bridges": [
        ("7x7i30e10m2d0", 1, 0),
        ("7x7i30e10m2d1", 1, 0),
        ("7x7i30e10m2d2", 1, 1),
        ("10x10i30e10m2d0", 1, 0),
        ("10x10i30e10m2d1", 1, 1)
    ],
    "cube": [
        ("c4x4", 1, 0),
        ("t1x2", 1, 1),
        ("o2x2", 1, 2),
        ("i3x3", 1, 2)
    ],
    "dominosa": [
        ("3dt", 1, 0),
        ("4dt", 1, 0),
        ("5dt", 1, 1),
        ("6dt", 1, 1),
        ("4db", 1, 1),
        ("5db", 1, 1),
        ("6db", 1, 1),
        ("7db", 1, 2),
        ("8db", 1, 2),
        ("9db", 1, 2),
        ("6dt", 1, 2),
        ("6dt", 1, 2)
    ],
    "fifteen": [
        ("3x3", 1, 0),
        ("4x4", 1, 1),
        ("5x5", 1, 2)
    ],
    "filling": [
        ("9x7", 1, 0),
        ("13x9", 1, 1),
        ("17x13", 1, 2)
    ],
    "flip": [
        ("3x3c", 1, 0),
        ("4x4c", 1, 0),
        ("5x5c", 1, 1),
        ("3x3r", 1, 1),
        ("4x4r", 1, 2),
        ("5x5r", 1, 2)
    ],
    "flood": [
        ("12x12c6m5", 1, 0),
        ("12x12c6m2", 1, 1),
        ("12x12c6m0", 1, 2),
        ("16x16c6m2", 1, 1),
        ("16x16c6m0", 1, 2),
        ("12x12c3m0", 1, 1),
        ("12x12c4m0", 1, 2)
    ],
    "galaxies": [
        ("7x7dn", 1, 0),
        ("7x7du", 1, 2),
        ("10x10dn", 1, 1),
        ("10x10du", 1, 2),
        ("15x15dn", 1, 2),
        ("15x15du", 1, 2)
    ],
    "group": [
        ("6dn", 1, 0),
        ("6dni", 1, 0),
        ("8dn", 1, 1),
        ("8dni", 1, 1),
        ("8dh", 1, 2),
        ("8dhi", 1, 2),
        ("12dn", 1, 2),
    ],
    "guess": [
        ("c6p4g10Bm", 1, 0),
        ("c8p5g12Bm", 1, 1)
    ],
    "inertia": [
        ("10x8", 1, 0),
        ("15x12", 1, 2),
        ("20x16", 1, 2)
    ],
    "keen": [
        ("4de", 1, 0),
        ("5de", 1, 1),
        ("5dem", 1, 0),
        ("6de", 1, 1),
        ("6dn", 1, 1),
        ("6dnm", 1, 2),
        ("6dh", 1, 2),
        ("6dx", 1, 2),
        ("6du", 1, 2),
        ("9dn", 1, 2)
    ],
    "lightup": [
        ("7x7b20s4d0", 1, 0),
        ("7x7b20s4d1", 1, 1),
        ("7x7b20s4d2", 1, 2),
        ("10x10b20s2d0", 1, 0),
        ("10x10b20s2d1", 1, 1),
        ("10x10b20s2d2", 1, 2),
        ("14x14b20s2d0", 1, 0),
        ("14x14b20s2d1", 1, 1),
        ("14x14b20s2d2", 1, 2)
    ],
    "loopy": [
        ("7x7t0de", 1, 0),
        ("10x10t0de", 1, 1),
        ("7x7t0dn", 1, 1),
        ("10x10t0dn", 1, 1),
        ("7x7t0dh", 1, 2),
        ("10x10t0dh", 1, 2),
        ("12x10t1dh", 1/18, 2),
        ("7x7t3dh", 1/18, 2),
        ("9x9t4dh", 1/18, 2),
        ("5x5t7dh", 1/18, 2),
        ("10x10t11dh", 1/18, 2),
        ("10x10t12dh", 1/18, 2),
        ("10x10t2dh", 1/18, 2),
        ("5x4t5dh", 1/18, 2),
        ("5x4t14dh", 1/18, 2),
        ("7x7t6dh", 1/18, 2),
        ("5x5t8dh", 1/18, 2),
        ("5x4t9dh", 1/18, 2),
        ("5x4t9dh", 1/18, 2),
        ("5x4t10dh", 1/18, 2),
        ("5x3t13dh", 1/18, 2),
        ("5x4t15dh", 1/18, 2),
        ("10x10t16dh", 1/18, 2),
        ("10x10t18dh", 1/18, 2)
    ],
    "magnets": [
        ("6x5de", 1, 0),
        ("6x5dt", 1, 1),
        ("6x5dtS", 1, 1),
        ("8x7de", 1, 0),
        ("8x7dt", 1, 1),
        ("8x7dtS", 1, 1),
        ("10x9dt", 1, 2),
        ("10x9dtS", 1, 2)
    ],
    "map": [
        ("20x15n30de", 1, 0),
        ("20x15n30dn", 1, 1),
        ("20x15n30dh", 1, 2),
        ("20x15n30du", 1, 2),
        ("30x25n75dn", 1, 2),
        ("30x25n75dh", 1, 2)
    ],
    "mines": [
        ("9x9n10", 1, 0),
        ("9x9n35", 1, 1),
        ("16x16n40", 1, 0),
        ("16x16n99", 1, 1),
        ("30x16n99", 1, 1),
        ("30x16n170", 1, 2),
    ],
    "mosaic": [
        ("3x3", 1, 0),
        ("5x5", 1, 0),
        ("10x10", 1, 1),
        ("15x15", 1, 1),
        ("25x25", 1, 2),
        ("50x50", 1, 3)
    ],
    "net": [
        ("5x5", 1, 0),
        ("7x7", 1, 0),
        ("9x9", 1, 1),
        ("11x11", 1, 1),
        ("13x11", 1, 2),
        ("5x5w", 1, 0),
        ("7x7w", 1, 1),
        ("9x9w", 1, 1),
        ("11x11w", 1, 2),
        ("13x11w", 1, 2)
    ],
    "netslide": [
        ("3x3b1", 1, 0),
        ("3x3", 1, 1),
        ("3x3w", 1, 2),
        ("4x4b1", 1, 0),
        ("4x4", 1, 1),
        ("4x4w", 1, 2),
        ("5x5b1", 1, 1),
        ("5x5", 1, 2),
        ("5x5w", 1, 2),
    ],
    "palisade": [
        ("5x5n5", 1, 0),
        ("8x6n6", 1, 1),
        ("10x8n8", 1, 1),
        ("15x12n10", 1, 2),
    ],
    "pattern": [
        ("5x5", 1, 0), # This isn't a built-in preset
        ("10x10", 1, 1),
        ("15x15", 1, 1),
        ("20x20", 1, 2),
        ("25x25", 1, 3),
        ("30x30", 1, 3),
    ],
    "pearl": [
        ("6x6de", 1, 0),
        ("6x6dt", 1, 0),
        ("8x8de", 1, 1),
        ("8x8dt", 1, 1),
        ("10x10de", 1, 1),
        ("10x10dt", 1, 2),
        ("12x8de", 1, 1),
        ("12x8dt", 1, 2),
    ],
    "pegs": [
        ("5x7cross", 1/6, 3), # The cross and octagon presets aren't randomized
        ("7x7cross", 1/6, 3),
        ("5x9cross", 1/6, 3),
        ("7x9cross", 1/6, 3),
        ("9x9cross", 1/6, 3),
        ("7x7octagon", 1/6, 3),
        ("5x5random", 1, 0),
        ("7x7random", 1, 1),
        ("9x9random", 1, 2),
    ],
    "range": [
        ("7x4", 1, 0), # This isn't a built-in preset
        ("9x6", 1, 1),
        ("12x8", 1, 1),
        ("13x9", 1, 2),
        ("16x11", 1, 2),
    ],
    "rect": [
        ("7x7", 1, 0),
        ("9x9", 1, 1),
        ("11x11", 1, 1),
        ("13x13", 1, 2),
        ("15x15", 1, 2),
        ("17x17", 1, 2),
        ("19x19", 1, 2),
    ],
    "samegame": [
        ("5x5c3s2", 1, 0),
        ("10x5c3s2", 1, 1),
        ("15x10c3s2", 1, 1),
        ("15x10c4s2", 1, 2),
        ("20x15c4s2", 1, 2),
    ],
    "signpost": [
        ("4x4c", 1, 0),
        ("4x4", 1, 0),
        ("5x5c", 1, 1),
        ("5x5", 1, 1),
        ("6x6c", 1, 1),
        ("7x7c", 1, 2),
    ],
    "singles": [
        ("5x5de", 1, 0),
        ("5x5dk", 1, 0),
        ("6x6de", 1, 1),
        ("6x6dk", 1, 1),
        ("8x8de", 1, 1),
        ("8x8dk", 1, 1),
        ("10x10de", 1, 1),
        ("10x10dk", 1, 2),
        ("12x12de", 1, 2),
        ("12x12dk", 1, 2),
    ],
    "sixteen": [
        ("3x3", 1, 0),
        ("4x3", 1, 1),
        ("4x4", 1, 1),
        ("5x4", 1, 2),
        ("5x5", 1, 2),
    ],
    "slant": [
        ("5x5de", 1, 0),
        ("5x5dh", 1, 1),
        ("8x8de", 1, 0),
        ("8x8dh", 1, 1),
        ("12x10de", 1, 2),
        ("12x10dh", 1, 2),
    ],
    "solo": [
        ("2x2", 1, 0),
        ("2x3db", 2, 0),
        ("3x3", 1, 1),
        ("3x3db", 1, 1),
        ("3x3xdb", 1, 2),
        ("3x3di", 1, 1),
        ("3x3da", 1, 2),
        ("3x3xda", 1, 2),
        ("3x3de", 1, 2),
        ("3x3du", 1, 2),
        ("3x3ka", 1, 2),
        ("9jdb", 1, 2),
        ("9jxdb", 1, 2),
        ("9jda", 1, 2),
        ("3x4db", 1, 3),
        ("4x4db", 1, 3),
    ],
    "tents": [
        ("8x8de", 1, 0),
        ("8x8dt", 1, 1),
        ("10x10de", 1, 0),
        ("10x10dt", 1, 1),
        ("15x15de", 1, 2),
        ("15x15dt", 1, 2),
    ],
    "towers": [
        ("4de", 1, 0),
        ("5de", 1, 1),
        ("5dh", 1, 2),
        ("6de", 1, 1),
        ("6dh", 1, 2),
        ("6dx", 1, 2),
        ("6du", 1, 2),
    ],
    "tracks": [
        ("6x6de", 1, 0), # This isn't a built-in preset
        ("8x8de", 1, 0),
        ("8x8dt", 1, 1),
        ("10x8de", 1, 1),
        ("10x8dt", 1, 2),
        ("10x10de", 1, 2),
        ("10x10dt", 1, 2),
        ("10x10dh", 1, 2),
        ("15x10de", 1, 3),
        ("15x10dt", 1, 3),
        ("15x15de", 1, 3),
        ("15x15dt", 1, 3),
        ("15x15dh", 1, 3),
    ],
    "twiddle": [
        ("3x3n2r", 1, 0),
        ("3x3n2", 1, 1),
        ("3x3n2o", 1, 2),
        ("4x4n2", 1, 1),
        ("4x4n2o", 1, 2),
        ("4x4n3", 1, 2),
        ("5x5n3", 1, 2),
        ("6x6n4", 1, 2),
    ],
    "undead": [
        ("4x4de", 1, 0),
        ("4x4dn", 1, 1),
        ("4x4dt", 1, 1),
        ("5x5de", 1, 0),
        ("5x5dn", 1, 1),
        ("5x5dt", 1, 2),
        ("7x7de", 1, 1),
        ("7x7dn", 1, 2),
    ],
    "unequal": [
        ("4de", 1, 0),
        ("5de", 1, 1),
        ("5dk", 1, 1),
        ("5adk", 1, 1),
        ("5dx", 1, 2),
        ("6de", 1, 2),
        ("6dk", 1, 2),
        ("6adk", 1, 2),
        ("6dx", 1, 2),
        ("7dk", 1, 2),
        ("7adk", 1, 2),
        ("7dx", 1, 2),
    ],
    "unruly": [
        ("8x8dt", 1, 0),
        ("8x8de", 1, 1),
        ("8x8dn", 1, 1),
        ("10x10de", 1, 1),
        ("10x10dn", 1, 1),
        ("14x14de", 1, 2),
        ("14x14dn", 1, 2)
    ],
    "untangle": [
        ("6", 1, 0),
        ("10", 1, 1),
        ("15", 1, 1),
        ("20", 1, 2),
        ("25", 1, 2),
    ]
}

class PuzzleCount(Range):
    """
    Number of puzzles to randomly generate.
    """
    range_start = 1
    range_end = max_puzzles
    default = 50

class StartingPuzzles(Range):
    """
    Number of puzzles to randomly add to the starting inventory. These will be
    removed from the item pool.
    """
    range_start = 0
    range_end = 20
    default = 5

class CompletionPercentage(Range):
    """
    Percent of puzzles which must be completed to finish the world, rounding up.

    If you set this to a low value, it is HIGHLY RECOMMENDED to disable release on world completion.
    """
    display_name = "Target Completion Percentage"
    range_start = 10
    range_end = 100
    default = 80

class MinimumDifficulty(Choice):
    """
    Minimum difficulty to select generated presets from. Note that not all genres have presets at "Hard" difficulty,
    so they will never appear if the minimum difficulty is set to Hard (unless you specify custom presets for them).
    """
    default = 0
    option_easy = 0
    option_normal = 1
    option_hard = 2

class MaximumDifficulty(Choice):
    """
    Maximum difficulty to select generated presets from. Takes priority over the Minimum Difficulty option if it is lower.

    Puzzles on "Ridiculous" difficulty are either very big or not actually randomized. Use this difficulty at your own risk.
    """
    default = 1
    option_easy = 0
    option_normal = 1
    option_hard = 2
    option_ridiculous = 3

class GenreWeights(OptionDict):
    """
    Relative chance for each genre to be selected as a random preset. Set a genre's
    weight to 0 or remove it from this list to disable it.
    """
    schema = Schema({
        Optional(g): Or(float, int) for g in genres
    })
    default = {g: 10 for g in genres if g != "group"} # it's a secret :P

class GenreMinimumDifficulty(OptionDict):
    """
    Minimum difficulty for each genre. Use 0 for easy, 1 for normal, 2 for hard, and 3 for ridiculous.
    """
    schema = Schema({
        Optional(g): Or(0, 1, 2, 3) for g in genres
    })
    default = {}

class GenreMaximumDifficulty(OptionDict):
    """
    Maximum difficulty for each genre. Use 0 for easy, 1 for normal, 2 for hard, and 3 for ridiculous.
    """
    schema = Schema({
        Optional(g): Or(0, 1, 2, 3) for g in genres
    })
    default = {}

class PresetOverrides(OptionDict):
    """
    List of presets to use for a given genre. Replaces the default presets for
    that puzzle if specified.

    For example, to make Net puzzles always use wrapping grids, add:
    net: [5x5w, 7x7w, 9x9w, 11x11w]
    """
    default = {}

sgtpuzzles_option_groups = [
    OptionGroup("Game Options", [
        PuzzleCount,
        StartingPuzzles,
        CompletionPercentage,
        GenreWeights,
        PresetOverrides,
        GenreMinimumDifficulty,
        GenreMaximumDifficulty
    ])
]

@dataclass
class SimonTathamPuzzlesOptions(CommonOptions):
    puzzle_count: PuzzleCount
    starting_puzzles: StartingPuzzles
    completion_percentage: CompletionPercentage
    min_difficulty: MinimumDifficulty
    max_difficulty: MaximumDifficulty
    genre_weights: GenreWeights
    genre_min_difficulty: GenreMinimumDifficulty
    genre_max_difficulty: GenreMaximumDifficulty
    preset_overrides: PresetOverrides

    local_items: LocalItems
    non_local_items: NonLocalItems
    start_inventory: StartInventoryPool
    start_hints: StartHints
    start_location_hints: StartLocationHints
    exclude_locations: ExcludeLocations
    priority_locations: PriorityLocations
    item_links: ItemLinks