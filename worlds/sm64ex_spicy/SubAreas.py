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
        "thi_red_cave", 4, "Tiny-Huge Island - Huge Tree Area", "thi_red_cave", "thi_huge"),
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


# Reusable exits from shuffled sub-areas.
RETURN_SOURCES: dict[str, SubAreaSource] = {
    "ccm_slide_exit": SubAreaSource("ccm_slide_exit", 21, "Cool, Cool Mountain - Secret Slide", "ccm_cabin"),
    "sl_igloo_exit": SubAreaSource("sl_igloo_exit", 22, "Snowman's Land - Igloo", "sl_main"),
    "ttm_slide_exit": SubAreaSource("ttm_slide_exit", 23, "Tall, Tall Mountain - Secret Slide", "ttm_main"),
    "thi_red_cave_exit": SubAreaSource(
        "thi_red_cave_exit", 24, "Tiny-Huge Island - Red Coin Cave", "thi_huge"),
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
    "thi_red_cave": SubAreaDestination("thi_red_cave", "Tiny-Huge Island - Red Coin Cave", 13, 3, 0x0A),
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
    "sl_main": SubAreaDestination(
        "sl_main", "Snowman's Land - Igloo Entrance", 10, 1, 0x0B),
    "ttm_main": SubAreaDestination(
        "ttm_main", "Tall, Tall Mountain - Slide Exit Alcove", 36, 1, 0x14),
    "thi_huge": SubAreaDestination("thi_huge", "Tiny-Huge Island (Huge)", 13, 1, 0x0B),
}


CASTLE_RETURN_DESTINATIONS: dict[str, SubAreaDestination] = {
    "castle_lobby_pss": SubAreaDestination("castle_lobby_pss", "Castle First Floor", 6, 1, 0x20),
    "castle_lobby_totwc": SubAreaDestination("castle_lobby_totwc", "Castle First Floor", 6, 1, 0x20),
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
    "jrb_ship": "the entrance to the Jolly Roger Bay sunken ship",
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
    "jrb_ship": "Jolly Roger Bay - Sunken Ship Entrance",
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
    "jrb_ship": "the inside of the Jolly Roger Bay sunken ship",
    "lll_volcano": "the inside of the Lethal Lava Land volcano",
    "ssl_pyramid_lower": "the lower Shifting Sand Land pyramid",
    "ssl_pyramid_upper": "the upper Shifting Sand Land pyramid",
    "thi_wiggler": "Wiggler's Cave",
    "bowser_1": "the Bowser in the Dark World arena",
    "bowser_2": "the Bowser in the Fire Sea arena",
    "bowser_3": "the Bowser in the Sky arena",
    "ccm_cabin": "Cool, Cool Mountain outside the slide exit",
    "sl_main": "the Snowman's Land igloo entrance",
    "ttm_main": "the Mysterious Mountainside area in Tall, Tall Mountain",
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


# Bowser in the Sky must remain the only way into its arena. These are the
# level destinations with an internal sub-area entrance and no second
# destination that enters the same level from elsewhere in the shuffled graph.
BITS_BRANCH_DESTINATIONS = frozenset({
    "Jolly Roger Bay",
    "Lethal Lava Land",
    "Shifting Sand Land",
    "Bowser in the Dark World",
    "Bowser in the Fire Sea",
    "Bowser in the Sky",
})


CASTLE_RETURN_OUTGOING_BY_DESTINATION = {
    "The Princess's Secret Slide": ("pss_fall",),
    "Tower of the Wing Cap": ("totwc_fall",),
    "Vanish Cap Under the Moat": ("vcutm_fall",),
    "Cavern of the Metal Cap": ("cotmc_fall",),
    "Dire, Dire Docks": ("ddd_fall",),
    "Wing Mario Over the Rainbow": ("wmotr_fall",),
}


def build_separate_connections(
        random: Random, include_castle_returns: bool = False) -> dict[str, str]:
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

    if include_castle_returns:
        castle_return_destinations = list(CASTLE_RETURN_DESTINATIONS)
        random.shuffle(castle_return_destinations)
        connections.update(zip(CASTLE_RETURN_SOURCES, castle_return_destinations))

    return connections


def build_mixed_connections(
        random: Random,
        normal_sources: dict[str, int],
        normal_destinations: tuple[str, ...],
        include_castle_returns: bool,
        include_sub_areas: bool = True,
        decoupled: bool = False,
        allow_castle_return_bits_branch: bool = False,
) -> dict[str, str]:
    """Build a two-deep directed entrance graph.

    Every destination containing an active outgoing source is placed at a root
    Castle entrance. All remaining outgoing sources then receive terminal
    destinations, so no shuffled path can exceed root -> branch -> terminal.
    """
    sources = list(normal_sources)
    destinations = list(normal_destinations)
    outgoing = {}

    if include_sub_areas:
        sources.extend(SUB_AREA_SOURCES)
        sources.extend(RETURN_SOURCES)
        destinations.extend(SUB_AREA_DESTINATIONS)
        destinations.extend(RETURN_DESTINATIONS)
        outgoing.update(OUTGOING_SOURCES_BY_DESTINATION)

    if include_castle_returns:
        sources.extend(CASTLE_RETURN_SOURCES)
        destinations.extend(CASTLE_RETURN_DESTINATIONS)
        outgoing.update(CASTLE_RETURN_OUTGOING_BY_DESTINATION)

    if len(sources) != len(destinations):
        raise ValueError(f"Sub-area source/destination mismatch: {len(sources)} != {len(destinations)}")

    if not decoupled and include_sub_areas:
        return _build_coupled_mixed_connections(
            random, sources, destinations, normal_sources, outgoing,
            allow_castle_return_bits_branch)

    branch_destinations = [destination for destination in destinations if destination in outgoing]
    root_sources = list(normal_sources)
    bits_source = "normal:Bowser in the Sky"
    connections: dict[str, str] = {}
    remaining_roots = list(root_sources)
    remaining_branches = list(branch_destinations)
    if bits_source in root_sources and "bowser_3" in destinations:
        available_branches = [
            destination for destination in branch_destinations
            if destination in BITS_BRANCH_DESTINATIONS and outgoing[destination]
        ]
        if available_branches:
            bits_branch = random.choice(available_branches)
            connections[bits_source] = bits_branch
            branch_exit = random.choice(list(outgoing[bits_branch]))
            connections[branch_exit] = "bowser_3"
            remaining_roots.remove(bits_source)
            remaining_branches.remove(bits_branch)

    if len(remaining_branches) > len(remaining_roots):
        # There are not enough mixed Castle entrances to anchor every physical
        # area. Preserve the reserved BITS route, then directly permute the
        # remaining sources and destinations. A flat random permutation does
        # not respect the root/branch/terminal layering the rest of this
        # function relies on, so a branch destination (e.g. "Cool, Cool
        # Mountain", which gates access to its Secret Slide sub-area) can end
        # up assigned behind a source that is never itself reachable from a
        # root. Retry the permutation until every branch is actually
        # reachable from an always-available root, rather than silently
        # returning a layout that strands a whole sub-area.
        remaining_sources = [source for source in sources if source not in connections]
        remaining_destinations = [
            destination for destination in destinations
            if destination not in connections.values()
        ]
        fixed_roots = [source for source in connections if source in root_sources]
        max_attempts = 200
        for _ in range(max_attempts):
            shuffled_sources = list(remaining_sources)
            shuffled_destinations = list(remaining_destinations)
            random.shuffle(shuffled_sources)
            random.shuffle(shuffled_destinations)
            attempt_connections = dict(connections)
            attempt_connections.update(zip(shuffled_sources, shuffled_destinations))
            if _all_branches_reachable(attempt_connections, root_sources, fixed_roots, outgoing, destinations):
                return attempt_connections
        raise ValueError(
            "Mixed sub-area shuffle could not find a layout reaching every "
            "branch destination after {} attempts".format(max_attempts))

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

def _all_branches_reachable(
        connections: dict[str, str],
        root_sources: list[str],
        fixed_roots: list[str],
        outgoing: dict[str, tuple[str, ...]],
        destinations: list[str],
) -> bool:
    """Check that every branch destination present in this graph is reachable.

    A "root" is any normal Castle entrance source, always available from the
    start; a source is also reachable once the branch destination it lives
    behind has been reached. A branch destination that isn't part of this
    mixed pool at all (e.g. its level is on a separate/vanilla painting
    shuffle instead) is reached through that other, always-valid mechanism,
    so its outgoing sources are already available too. A destination that
    never becomes reachable by either path would strand any sub-area gated
    behind it (and any locations inside).
    """
    reachable_destinations: set[str] = set()
    frontier: set[str] = set(root_sources) | set(fixed_roots)
    for destination, outgoing_sources in outgoing.items():
        if destination not in destinations:
            frontier.update(outgoing_sources)
    while frontier:
        next_frontier: set[str] = set()
        for source in frontier:
            destination = connections.get(source)
            if destination is None or destination in reachable_destinations:
                continue
            reachable_destinations.add(destination)
            next_frontier.update(outgoing.get(destination, ()))
        frontier = next_frontier
    return all(
        destination in reachable_destinations
        for destination in outgoing
        if destination in destinations
    )

def _build_coupled_mixed_connections(
        random: Random,
        sources: list[str],
        destinations: list[str],
        normal_sources: dict[str, int],
        outgoing: dict[str, tuple[str, ...]],
        allow_castle_return_bits_branch: bool,
) -> dict[str, str]:
    """Shuffle mixed entrances while preserving reusable level returns."""
    branch_destinations = [destination for destination in destinations if destination in outgoing]
    bits_source = "normal:Bowser in the Sky"
    connections: dict[str, str] = {}

    source_homes = {
        source: source.removeprefix("normal:")
        for source in normal_sources
    }
    source_homes.update({
        key: SUB_AREA_SOURCES[key].return_destination
        for key in REUSABLE_ENTRY_KEYS if key in sources
    })
    available_sources = set(sources)
    available_destinations = set(destinations)

    if bits_source in sources and "bowser_3" in destinations:
        bits_candidates = set(BITS_BRANCH_DESTINATIONS)
        if allow_castle_return_bits_branch:
            bits_candidates.update(CASTLE_RETURN_OUTGOING_BY_DESTINATION)
        available = [
            destination for destination in branch_destinations
            if destination in bits_candidates and outgoing[destination]
        ]
        if available:
            destination = random.choice(available)
            connections[bits_source] = destination
            exit_source = random.choice(list(outgoing[destination]))
            connections[exit_source] = "bowser_3"
            available_sources.difference_update((bits_source, exit_source))
            available_destinations.difference_update((destination, "bowser_3"))
            branch_destinations.remove(destination)

    random.shuffle(branch_destinations)
    for destination in tuple(branch_destinations):
        if destination not in available_destinations:
            continue
        candidates = [
            source for source, home in source_homes.items()
            if source in available_sources
            and source not in outgoing[destination]
            and home in available_destinations
            and home != destination
        ]
        exit_sources = [source for source in outgoing[destination] if source in available_sources]
        if not candidates or not exit_sources:
            continue
        source = random.choice(candidates)
        exit_source = random.choice(exit_sources)
        home = source_homes[source]
        connections[source] = destination
        connections[exit_source] = home
        available_sources.difference_update((source, exit_source))
        available_destinations.difference_update((destination, home))

    remaining_sources = [source for source in sources if source in available_sources]
    remaining_destinations = [
        destination for destination in destinations if destination in available_destinations
    ]
    if len(remaining_sources) != len(remaining_destinations):
        raise ValueError(
            f"Coupled mixed source/destination mismatch: "
            f"{len(remaining_sources)} != {len(remaining_destinations)}")
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
