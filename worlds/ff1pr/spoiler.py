from typing import Dict, List, Any, NamedTuple, TextIO, TYPE_CHECKING
from .regions import overworld_regions
if TYPE_CHECKING:
    from . import FF1pixelWorld, FF1pixelOptions

def generate_entrances_spoiler(world: "FF1pixelWorld") -> str:
    all_regions = world.multiworld.regions.region_cache[world.player]

    def visit_region(next_region: str, depth: int, depths: List[bool]) -> str:
        spoiler_text: str = ""

        indent = ""
        if depth > 0:
            for i in range(0, depth):
                if depths[i]:
                    indent += "║ "
                else:
                    indent += "  "

            if depths[depth]:
                indent += "╟>"
            else:
                indent += "╚>"

        if depth == 0: spoiler_text += f"[{next_region}]\n"
        if depth > 0: spoiler_text += f"{indent}{next_region}\n"

        crawled_region = all_regions[next_region]
        exits_to_crawl = [e for e in crawled_region.exits if e.connected_region.name not in overworld_regions]
        exit_count = len(exits_to_crawl)
        current_count = 1

        for crawled_exit in exits_to_crawl:
            if depth > 0:
                if current_count < exit_count: depths[depth + 1] = True
                else: depths[depth + 1] = False
            current_count += 1

            if depth == 0: spoiler_text += f" >{crawled_exit.name}\n"
            spoiler_text += visit_region(crawled_exit.connected_region.name, depth + 1, depths)
            if depth == 0: spoiler_text += "\n"

        if depth == 0 and exit_count == 0: spoiler_text += "\n"
        return spoiler_text

    entrances_spoiler: str = ""
    for ow_region in overworld_regions:
        false_depth = [False for i in range(0, 20)]
        entrances_spoiler += visit_region(ow_region, 0, false_depth)

    return entrances_spoiler