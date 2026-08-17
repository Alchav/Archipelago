from __future__ import annotations

from dataclasses import dataclass
from random import Random


def pack_warp_destination(
        level: int, area: int, node: int, variant: int = 0, warp_arg: int = 0) -> int:
    return (warp_arg << 28) | (variant << 24) | (level << 16) | (area << 8) | node


@dataclass(frozen=True)
class SubAreaSource:
    key: str
    source_id: int
    region: str
    vanilla_destination: str
    return_destination: str | None = None


@dataclass(frozen=True)
class SubAreaDestination:
    key: str
    region: str
    level: int
    area: int
    node: int
    variant: int = 0
    warp_arg: int = 0

    @property
    def packed(self) -> int:
        return pack_warp_destination(
            self.level, self.area, self.node, self.variant, self.warp_arg)


# Source IDs are stable protocol values shared with sm64ex. IDs below 100 are
# physical course warps. Normal Castle entrances use 1000 + their existing
# level/variant entrance ID.
NORMAL_SOURCE_OFFSET = 1000


def normal_source_id(entrance_id: int) -> int:
    return NORMAL_SOURCE_OFFSET + entrance_id


# Physical sub-area entrances.
SUB_AREA_SOURCES: dict[str, SubAreaSource] = {
    "ccm_slide": SubAreaSource("ccm_slide", 1, "Cool, Cool Mountain", "ccm_slide", "ccm_cabin"),
    "sl_igloo": SubAreaSource("sl_igloo", 2, "Snowman's Land - Igloo Entrance", "sl_igloo", "sl_main"),
    "ttm_slide": SubAreaSource("ttm_slide", 3, "Tall, Tall Mountain - Top", "ttm_slide", "ttm_main"),
    "thi_red_cave": SubAreaSource(
        "thi_red_cave", 4, "Tiny-Huge Island - Red Coin Cave Entrance", "thi_red_cave", "thi_huge"),
    "hmc_cotmc": SubAreaSource("hmc_cotmc", 5, "Hazy Maze Cave", "cotmc"),
    "jrb_ship": SubAreaSource("jrb_ship", 6, "Jolly Roger Bay", "jrb_ship"),
    "lll_volcano": SubAreaSource(
        "lll_volcano", 7, "Lethal Lava Land - Volcano Entrance", "lll_volcano"),
    "ssl_pyramid_side": SubAreaSource(
        "ssl_pyramid_side", 8, "Shifting Sand Land", "ssl_pyramid_lower"),
    "ssl_pyramid_top": SubAreaSource(
        "ssl_pyramid_top", 9, "Shifting Sand Land - Upper Pyramid Entrance", "ssl_pyramid_upper"),
    "thi_wiggler": SubAreaSource(
        "thi_wiggler", 10, "Tiny-Huge Island - Huge Top", "thi_wiggler"),
    "bitdw_bowser": SubAreaSource(
        "bitdw_bowser", 11, "Bowser in the Dark World - Bowser Pipe", "bowser_1"),
    "bitfs_bowser": SubAreaSource(
        "bitfs_bowser", 12, "Bowser in the Fire Sea - Upper", "bowser_2"),
    "bits_bowser": SubAreaSource(
        "bits_bowser", 13, "Bowser in the Sky - Top", "bowser_3"),
}


# Reusable exits from shuffled sub-areas. Castle returns are activated only by
# mixed_plus_castle_returns.
RETURN_SOURCES: dict[str, SubAreaSource] = {
    "ccm_slide_exit": SubAreaSource("ccm_slide_exit", 21, "Cool, Cool Mountain - Secret Slide", "ccm_cabin"),
    "sl_igloo_exit": SubAreaSource("sl_igloo_exit", 22, "Snowman's Land - Igloo", "sl_main"),
    "ttm_slide_exit": SubAreaSource("ttm_slide_exit", 23, "Tall, Tall Mountain - Secret Slide", "ttm_main"),
    "thi_red_cave_exit": SubAreaSource(
        "thi_red_cave_exit", 24, "Tiny-Huge Island - Red Coins Area", "thi_huge"),
}


CASTLE_RETURN_SOURCES: dict[str, SubAreaSource] = {
    "pss_fall": SubAreaSource("pss_fall", 31, "The Princess's Secret Slide", "castle_lobby_pss"),
    "totwc_fall": SubAreaSource("totwc_fall", 32, "Tower of the Wing Cap", "castle_lobby_totwc"),
    "vcutm_fall": SubAreaSource("vcutm_fall", 33, "Vanish Cap Under the Moat", "castle_grounds_vcutm"),
    "cotmc_fall": SubAreaSource("cotmc_fall", 34, "Cavern of the Metal Cap", "castle_grounds_cotmc"),
    "ddd_fall": SubAreaSource("ddd_fall", 35, "Dire, Dire Docks", "castle_grounds_ddd"),
    "wmotr_fall": SubAreaSource("wmotr_fall", 36, "Wing Mario Over the Rainbow", "castle_grounds_wmotr"),
}


SUB_AREA_DESTINATIONS: dict[str, SubAreaDestination] = {
    "ccm_slide": SubAreaDestination("ccm_slide", "Cool, Cool Mountain - Secret Slide", 5, 2, 0x0A),
    "sl_igloo": SubAreaDestination("sl_igloo", "Snowman's Land - Igloo", 10, 2, 0x0A),
    "ttm_slide": SubAreaDestination("ttm_slide", "Tall, Tall Mountain - Secret Slide", 36, 2, 0x0A),
    "thi_red_cave": SubAreaDestination("thi_red_cave", "Tiny-Huge Island - Red Coins Area", 13, 3, 0x0A),
    "cotmc": SubAreaDestination("cotmc", "Cavern of the Metal Cap", 28, 1, 0x0A),
    "jrb_ship": SubAreaDestination("jrb_ship", "Jolly Roger Bay - Sunken Ship", 12, 2, 0x0A),
    "lll_volcano": SubAreaDestination("lll_volcano", "Lethal Lava Land - Volcano", 22, 2, 0x0A),
    "ssl_pyramid_lower": SubAreaDestination(
        "ssl_pyramid_lower", "Shifting Sand Land - Pyramid", 8, 2, 0x0A),
    "ssl_pyramid_upper": SubAreaDestination(
        "ssl_pyramid_upper", "Shifting Sand Land - Pyramid Top Entry", 8, 2, 0x14),
    "thi_wiggler": SubAreaDestination("thi_wiggler", "Tiny-Huge Island - Wiggler's Cave", 13, 3, 0x0B),
    "bowser_1": SubAreaDestination("bowser_1", "Bowser in the Dark World - Bowser Arena", 30, 1, 0x0A),
    "bowser_2": SubAreaDestination("bowser_2", "Bowser in the Fire Sea - Bowser Arena", 33, 1, 0x0A),
    "bowser_3": SubAreaDestination("bowser_3", "Bowser in the Sky - Bowser Arena", 34, 1, 0x0A),
}


RETURN_DESTINATIONS: dict[str, SubAreaDestination] = {
    "ccm_cabin": SubAreaDestination(
        "ccm_cabin", "Cool, Cool Mountain - Slide Exit", 5, 1, 0x14, warp_arg=6),
    "sl_main": SubAreaDestination("sl_main", "Snowman's Land", 10, 1, 0x0B),
    "ttm_main": SubAreaDestination("ttm_main", "Tall, Tall Mountain", 36, 1, 0x14),
    "thi_huge": SubAreaDestination("thi_huge", "Tiny-Huge Island (Huge)", 13, 1, 0x0B),
}


CASTLE_RETURN_DESTINATIONS: dict[str, SubAreaDestination] = {
    "castle_lobby_pss": SubAreaDestination("castle_lobby_pss", "Castle Lobby", 6, 1, 0x20),
    "castle_lobby_totwc": SubAreaDestination("castle_lobby_totwc", "Castle Lobby", 6, 1, 0x20),
    "castle_grounds_vcutm": SubAreaDestination(
        "castle_grounds_vcutm", "Castle Grounds", 16, 1, 0x07),
    "castle_grounds_cotmc": SubAreaDestination(
        "castle_grounds_cotmc", "Castle Grounds", 16, 1, 0x14),
    "castle_grounds_ddd": SubAreaDestination(
        "castle_grounds_ddd", "Castle Grounds", 16, 1, 0x1E),
    "castle_grounds_wmotr": SubAreaDestination(
        "castle_grounds_wmotr", "Castle Grounds", 16, 1, 0x0A),
}


SUB_AREA_SOURCE_DESCRIPTIONS = {
    "ccm_slide": "the Cool, Cool Mountain chimney",
    "sl_igloo": "the Snowman's Land igloo entrance",
    "ttm_slide": "the Tall, Tall Mountain slide entrance",
    "thi_red_cave": "the Tiny-Huge Island Red Coin Cave entrance",
    "hmc_cotmc": "the underground-lake waterfall in Hazy Maze Cave",
    "jrb_ship": "the opening in the Jolly Roger Bay sunken ship",
    "lll_volcano": "the Lethal Lava Land volcano entrance",
    "ssl_pyramid_side": "the side entrance of the Shifting Sand Land pyramid",
    "ssl_pyramid_top": "the top entrance of the Shifting Sand Land pyramid",
    "thi_wiggler": "the Tiny-Huge Island Wiggler's Cave entrance",
    "bitdw_bowser": "the Bowser in the Dark World arena pipe",
    "bitfs_bowser": "the Bowser in the Fire Sea arena funnel",
    "bits_bowser": "the Bowser in the Sky arena pipe",
    "ccm_slide_exit": "the Cool, Cool Mountain slide exit",
    "sl_igloo_exit": "the Snowman's Land igloo exit",
    "ttm_slide_exit": "the Tall, Tall Mountain slide exit",
    "thi_red_cave_exit": "the Tiny-Huge Island Red Coin Cave exit",
    "pss_fall": "falling out of the Princess's Secret Slide",
    "totwc_fall": "falling out of the Tower of the Wing Cap",
    "vcutm_fall": "falling out of Vanish Cap Under the Moat",
    "cotmc_fall": "the Cavern of the Metal Cap waterfall",
    "ddd_fall": "the Dire, Dire Docks moat exit",
    "wmotr_fall": "falling out of Wing Mario Over the Rainbow",
}

SUB_AREA_SOURCE_NAMES = {
    "ccm_slide": "Cool, Cool Mountain - Chimney",
    "sl_igloo": "Snowman's Land - Igloo Entrance",
    "ttm_slide": "Tall, Tall Mountain - Secret Slide Entrance",
    "thi_red_cave": "Tiny-Huge Island - Red Coin Cave Entrance",
    "hmc_cotmc": "Hazy Maze Cave - Cavern of the Metal Cap Waterfall",
    "jrb_ship": "Jolly Roger Bay - Sunken Ship Opening",
    "lll_volcano": "Lethal Lava Land - Volcano Entrance",
    "ssl_pyramid_side": "Shifting Sand Land - Pyramid Side Entrance",
    "ssl_pyramid_top": "Shifting Sand Land - Pyramid Top Entrance",
    "thi_wiggler": "Tiny-Huge Island - Wiggler's Cave Entrance",
    "bitdw_bowser": "Bowser in the Dark World - Bowser Arena Pipe",
    "bitfs_bowser": "Bowser in the Fire Sea - Bowser Arena Funnel",
    "bits_bowser": "Bowser in the Sky - Bowser Arena Pipe",
    "ccm_slide_exit": "Cool, Cool Mountain - Secret Slide Exit",
    "sl_igloo_exit": "Snowman's Land - Igloo Exit",
    "ttm_slide_exit": "Tall, Tall Mountain - Secret Slide Exit",
    "thi_red_cave_exit": "Tiny-Huge Island - Red Coin Cave Exit",
    "pss_fall": "The Princess's Secret Slide - Fall",
    "totwc_fall": "Tower of the Wing Cap - Fall",
    "vcutm_fall": "Vanish Cap Under the Moat - Fall",
    "cotmc_fall": "Cavern of the Metal Cap - Waterfall Exit",
    "ddd_fall": "Dire, Dire Docks - Moat Exit",
    "wmotr_fall": "Wing Mario Over the Rainbow - Fall",
}

SUB_AREA_DESTINATION_DESCRIPTIONS = {
    "ccm_slide": "the Cool, Cool Mountain Secret Slide",
    "sl_igloo": "the Snowman's Land igloo",
    "ttm_slide": "the Tall, Tall Mountain Secret Slide",
    "thi_red_cave": "the Tiny-Huge Island Red Coin Cave",
    "cotmc": "Cavern of the Metal Cap",
    "jrb_ship": "the inside of the Jolly Roger Bay sunken ship",
    "lll_volcano": "the inside of the Lethal Lava Land volcano",
    "ssl_pyramid_lower": "the lower Shifting Sand Land pyramid",
    "ssl_pyramid_upper": "the upper Shifting Sand Land pyramid",
    "thi_wiggler": "Wiggler's Cave",
    "bowser_1": "the Bowser in the Dark World arena",
    "bowser_2": "the Bowser in the Fire Sea arena",
    "bowser_3": "the Bowser in the Sky arena",
    "ccm_cabin": "Cool, Cool Mountain outside the slide exit",
    "sl_main": "the main Snowman's Land area",
    "ttm_main": "the main Tall, Tall Mountain area",
    "thi_huge": "the main Huge Island area",
    "castle_lobby_pss": "the Castle Lobby",
    "castle_lobby_totwc": "the Castle Lobby",
    "castle_grounds_vcutm": "the Castle Grounds moat",
    "castle_grounds_cotmc": "the Castle Grounds waterfall",
    "castle_grounds_ddd": "the Castle Grounds moat",
    "castle_grounds_wmotr": "the sky above the Castle Grounds",
}


def sub_area_source_by_id(source_id: int) -> SubAreaSource | None:
    for table in (SUB_AREA_SOURCES, RETURN_SOURCES, CASTLE_RETURN_SOURCES):
        for source in table.values():
            if source.source_id == source_id:
                return source
    return None


def sub_area_destination_name(destination_key: str) -> str:
    for table in (SUB_AREA_DESTINATIONS, RETURN_DESTINATIONS, CASTLE_RETURN_DESTINATIONS):
        destination = table.get(destination_key)
        if destination is not None:
            return destination.region
    raise KeyError(destination_key)


REUSABLE_ENTRY_KEYS = ("ccm_slide", "sl_igloo", "ttm_slide", "thi_red_cave")
REUSABLE_EXIT_BY_DESTINATION = {
    "ccm_slide": "ccm_slide_exit",
    "sl_igloo": "sl_igloo_exit",
    "ttm_slide": "ttm_slide_exit",
    "thi_red_cave": "thi_red_cave_exit",
}


# Destinations that expose further shuffled sources when entered. This is used
# to construct mixed-mode graphs with at most one intermediate area.
OUTGOING_SOURCES_BY_DESTINATION: dict[str, tuple[str, ...]] = {
    "Cool, Cool Mountain": ("ccm_slide",),
    "Snowman's Land": ("sl_igloo",),
    "Tall, Tall Mountain": ("ttm_slide",),
    "Tiny-Huge Island (Huge)": ("thi_red_cave", "thi_wiggler"),
    "Hazy Maze Cave": ("hmc_cotmc",),
    "Jolly Roger Bay": ("jrb_ship",),
    "Lethal Lava Land": ("lll_volcano",),
    "Shifting Sand Land": ("ssl_pyramid_side", "ssl_pyramid_top"),
    "Bowser in the Dark World": ("bitdw_bowser",),
    "Bowser in the Fire Sea": ("bitfs_bowser",),
    "Bowser in the Sky": ("bits_bowser",),
    "ccm_slide": ("ccm_slide_exit",),
    "sl_igloo": ("sl_igloo_exit",),
    "ttm_slide": ("ttm_slide_exit",),
    "thi_red_cave": ("thi_red_cave_exit",),
}


CASTLE_RETURN_OUTGOING_BY_DESTINATION = {
    "The Princess's Secret Slide": ("pss_fall",),
    "Tower of the Wing Cap": ("totwc_fall",),
    "Vanish Cap Under the Moat": ("vcutm_fall",),
    "cotmc": ("cotmc_fall",),
    "Dire, Dire Docks": ("ddd_fall",),
    "Wing Mario Over the Rainbow": ("wmotr_fall",),
}


def build_separate_connections(random: Random) -> dict[str, str]:
    connections: dict[str, str] = {}

    reusable_destinations = list(REUSABLE_ENTRY_KEYS)
    random.shuffle(reusable_destinations)
    for source_key, destination_key in zip(REUSABLE_ENTRY_KEYS, reusable_destinations):
        connections[source_key] = destination_key
        exit_source = REUSABLE_EXIT_BY_DESTINATION[destination_key]
        return_destination = SUB_AREA_SOURCES[source_key].return_destination
        assert return_destination is not None
        connections[exit_source] = return_destination

    dead_source_keys = [key for key in SUB_AREA_SOURCES if key not in REUSABLE_ENTRY_KEYS]
    dead_destination_keys = [key for key in SUB_AREA_DESTINATIONS if key not in REUSABLE_ENTRY_KEYS]
    random.shuffle(dead_destination_keys)
    connections.update(zip(dead_source_keys, dead_destination_keys))
    return connections


def build_mixed_connections(
        random: Random,
        normal_sources: dict[str, int],
        normal_destinations: tuple[str, ...],
        include_castle_returns: bool,
) -> dict[str, str]:
    """Build a two-deep directed entrance graph.

    Every destination containing an active outgoing source is placed at a root
    Castle entrance. All remaining outgoing sources then receive terminal
    destinations, so no shuffled path can exceed root -> branch -> terminal.
    """
    sources = list(normal_sources) + list(SUB_AREA_SOURCES) + list(RETURN_SOURCES)
    destinations = list(normal_destinations) + list(SUB_AREA_DESTINATIONS) + list(RETURN_DESTINATIONS)
    outgoing = dict(OUTGOING_SOURCES_BY_DESTINATION)

    if include_castle_returns:
        sources.extend(CASTLE_RETURN_SOURCES)
        destinations.extend(CASTLE_RETURN_DESTINATIONS)
        outgoing.update(CASTLE_RETURN_OUTGOING_BY_DESTINATION)

    if len(sources) != len(destinations):
        raise ValueError(f"Sub-area source/destination mismatch: {len(sources)} != {len(destinations)}")

    branch_destinations = [destination for destination in destinations if destination in outgoing]
    root_sources = list(normal_sources)
    if len(branch_destinations) > len(root_sources):
        raise ValueError("Not enough Castle entrances for all non-terminal sub-area destinations")

    bits_source = "normal:Bowser in the Sky"
    if bits_source not in root_sources:
        raise ValueError("Mixed sub-area shuffle requires the Bowser in the Sky root entrance")

    connections: dict[str, str] = {}
    available_branches = [destination for destination in branch_destinations if outgoing[destination]]
    bits_branch = random.choice(available_branches)
    connections[bits_source] = bits_branch

    branch_exit = random.choice(list(outgoing[bits_branch]))
    connections[branch_exit] = "bowser_3"

    remaining_roots = [source for source in root_sources if source != bits_source]
    remaining_branches = [destination for destination in branch_destinations if destination != bits_branch]
    random.shuffle(remaining_roots)
    random.shuffle(remaining_branches)
    for source, destination in zip(remaining_roots, remaining_branches):
        connections[source] = destination

    remaining_sources = [source for source in sources if source not in connections]
    remaining_destinations = [destination for destination in destinations if destination not in connections.values()]

    # All branch destinations were consumed by root sources, and Bowser 3 was
    # consumed by the reserved branch exit. Everything left is terminal.
    if any(destination in outgoing for destination in remaining_destinations):
        raise ValueError("Mixed sub-area shuffle left a branch destination outside the root layer")
    random.shuffle(remaining_sources)
    random.shuffle(remaining_destinations)
    connections.update(zip(remaining_sources, remaining_destinations))
    return connections


def destination_slot_data(destination_key: int | str, normal_destination_data: dict[int, int]) -> int:
    if destination_key in normal_destination_data:
        return normal_destination_data[destination_key]
    for table in (SUB_AREA_DESTINATIONS, RETURN_DESTINATIONS, CASTLE_RETURN_DESTINATIONS):
        destination = table.get(destination_key)
        if destination is not None:
            return destination.packed
    raise KeyError(destination_key)
