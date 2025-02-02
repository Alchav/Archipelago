from typing import Dict, List
from BaseClasses import Location, Region
from .types import CrystalisLocationData, CrystalisRegionData, CRYSTALIS_BASE_ID


class CrystalisLocation(Location):
    game: str = "Crystalis"

    def __init__(self, player: int, name="", code=None, parent=None) -> None:
        super(CrystalisLocation, self).__init__(player, name, code, parent)
        self.event = code is None


def create_location_from_location_data(player: int, location_data: CrystalisLocationData, region: Region) \
        -> CrystalisLocation:
    return CrystalisLocation(player,
                             location_data.name,
                             location_data.ap_id_offset + CRYSTALIS_BASE_ID,
                             region
                             )
