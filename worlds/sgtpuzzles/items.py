from BaseClasses import Item
import typing

base_id = 9250000
max_puzzles = 2000

class ItemData(typing.NamedTuple):
    code: int
    progression: bool = True


class SimonTathamPuzzlesItem(Item):
    game: str = "SimonTathamPuzzles"

item_table = {f"Puzzle {i+1}": ItemData(base_id+i) for i in range(max_puzzles)}
item_table["Filler"] = ItemData(base_id + max_puzzles, False)
item_table["Reroll"] = ItemData(base_id + max_puzzles+1, False)
item_table["Skip"] = ItemData(base_id + max_puzzles+2, False)
item_table["Checkmark"] = ItemData(base_id + max_puzzles+3)

lookup_id_to_name: typing.Dict[int, str] = {data.code: item_name for item_name, data in item_table.items()}
