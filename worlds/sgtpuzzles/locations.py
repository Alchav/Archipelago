from BaseClasses import Location
import typing
from .items import max_puzzles


class AdvData(typing.NamedTuple):
    id: int
    region: str = "Puzzles"


class SimonTathamPuzzlesLocation(Location):
    game: str = "SimonTathamPuzzles"


base_id = 9250000
advancement_table = {f"Puzzle {i+1} Reward": AdvData(base_id + i) for i in range(max_puzzles)}
advancement_table.update({f"Puzzle {i+1} Reward 2": AdvData(base_id + max_puzzles + i) for i in range(max_puzzles)})
advancement_table.update({f"Puzzle {i+1} Reward 3": AdvData(base_id + max_puzzles*2 + i) for i in range(max_puzzles)})

lookup_id_to_name: typing.Dict[int, str] = {data.id: location_name for location_name, data in advancement_table.items()}
