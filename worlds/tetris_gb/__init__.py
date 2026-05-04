from Options import OptionError
from BaseClasses import Item, Tutorial, ItemClassification, Region, Location, Item
from ..AutoWorld import World, WebWorld

from . import client
from .locations import score_locations, location_name_to_id
from .items import items, item_name_to_id
from .options import TetrisOptions

version = (0, 0)

filler_weight_options = ["clear_random_line_weight", "garbage_line_weight", "illusory_piece_weight",
                         "shuffle_garbage_line_hole_weight", "random_inputs_weight", "wall_trap_weight",
                         "toggle_next_piece_weight", "instant_lock_weight", "nothing_weight"]


class TetrisWebWorld(WebWorld):
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to playing Tetris for Gameboy with Archipelago.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Alchav"]
    )

    tutorials = [setup_en]


class TetrisGBWorld(World):
    game = "Tetris"
    location_name_to_id = location_name_to_id
    item_name_to_id = item_name_to_id

    options_dataclass = TetrisOptions
    options: TetrisOptions

    web = TetrisWebWorld()

    def __init__(self, multiworld, player: int):
        super().__init__(multiworld, player)
        self.speed_decreases = 0
        self.speed_increases = 0
        self.location_count = 0
        self.filler_weights = {option: 1 for option in filler_weight_options}

    def generate_early(self):
        if self.options.overclocked_location_count > 0:
            self.location_count = self.options.overclocked_location_count.value
            if self.location_count > round(self.options.goal_score / 50):
                raise OptionError(f"Overclocked Location Count set too high for Goal Score for player {self.player}")
        else:
            self.location_count = self.options.location_count.value

        starting_speed = self.options.starting_speed.value
        maximum_speed = self.options.maximum_speed.value
        target_speed = max(self.options.target_speed.value, maximum_speed)
        self.speed_increases = starting_speed - maximum_speed
        self.speed_decreases = target_speed - maximum_speed

        self.filler_weights = {option: getattr(self.options, option).value for option in filler_weight_options}

        if self.options.next_piece_display != "toggles":
            del self.filler_weights["toggle_next_piece_weight"]

    def create_regions(self):

        locs = list(range(1, min(20000, round(self.options.goal_score / 50) + 1)))

        locations_used = [int(i * len(locs) / self.location_count) for i in range(1, self.location_count + 1)]

        menu_region = Region("Menu", self.player, self.multiworld)

        for i, score in enumerate(locations_used, start=1):
            def score_rule(state, i=i):
                speed_decreases = state.count("Decrease Speed", self.player)
                score_multipliers = (state.count("Score Multiplier", self.player)
                                     + (state.count("Score Multiplier x2", self.player) * 2)
                                     + (state.count("Score Multiplier x3", self.player) * 3))
                required_speed_decreases = int((self.speed_decreases / len(locations_used)) * i)
                required_score_multipliers = int((self.options.score_multipliers.value / len(locations_used)) * i)
                if speed_decreases < required_speed_decreases:
                    return False
                if score_multipliers < required_score_multipliers:
                    return False
                return True

            location = TetrisLocation(self.player, self.location_id_to_name[score], score, menu_region)
            location.access_rule = score_rule
            menu_region.locations.append(location)

        self.multiworld.regions.append(menu_region)

    def set_rules(self):

        self.multiworld.completion_condition[self.player] = lambda state: (
                state.has("Decrease Speed", self.player, self.speed_decreases)
                and (state.count("Score Multiplier", self.player)
                     + (state.count("Score Multiplier x2", self.player) * 2)
                     + (state.count("Score Multiplier x3", self.player) * 3))
                >= self.options.score_multipliers.value
        )

    def create_items(self):
        location_count = len(self.multiworld.get_unfilled_locations(self.player))
        item_pool = []
        if self.options.next_piece_display == "disabled":
            self.multiworld.push_precollected(self.create_item("Hide Next Piece"))
        elif self.options.next_piece_display == "disabled_to_enabled":
            self.multiworld.push_precollected(self.create_item("Hide Next Piece"))
            item_pool.append(self.create_item("Show Next Piece"))
        elif self.options.next_piece_display == "enabled_to_disabled":
            item_pool.append(self.create_item("Hide Next Piece"))

        item_pool += [self.create_item("Decrease Speed") for _ in range(self.speed_decreases)]
        item_pool += [self.create_item("Increase Speed") for _ in range(self.speed_increases)]

        items_remaining = location_count - len(item_pool)
        score_multipliers = self.options.score_multipliers.value

        if score_multipliers <= items_remaining:
            item_pool += [self.create_item("Score Multiplier") for _ in range(score_multipliers)]
            items_remaining -= score_multipliers
        else:
            extra = score_multipliers - items_remaining  # required extra multiplier value beyond all-x1

            # Hard cap: even all x3 gives +2 per slot
            if extra > 2 * items_remaining:
                raise ValueError(
                    f"Not enough item slots ({items_remaining}) to fit total score multiplier {score_multipliers} "
                    f"(max possible is {items_remaining * 3})."
                )

            # Prefer x2, only use x3 if x2-only can't supply enough extra
            n_x3 = max(0, extra - items_remaining)
            n_x2 = extra - 2 * n_x3
            n_x1 = items_remaining - n_x2 - n_x3

            item_pool += [self.create_item("Score Multiplier x3") for _ in range(n_x3)]
            item_pool += [self.create_item("Score Multiplier x2") for _ in range(n_x2)]
            item_pool += [self.create_item("Score Multiplier") for _ in range(n_x1)]

        filler_weights = list(self.filler_weights.values())
        if not sum(filler_weights):
            filler_weights = [1] * len(filler_weights)

        fillers = [item for item in self.random.choices(
            list(self.filler_weights.keys()),
            weights=filler_weights,
            k=location_count - len(item_pool))]

        item_pool += [self.create_item(getattr(self.options, option).get_item(self.random)) for option in fillers if option != "nothing_weight"]

        self.multiworld.itempool += item_pool

    @classmethod
    def stage_post_fill(cls, multiworld):
        # Traps are an important part of the concept for this apworld.
        # We wouldn't want progression balancing to push them all out of the early spheres, now would we?
        for location in multiworld.get_locations():
            if location.item.game == cls.game and location.item.classification == ItemClassification.trap:
                location.locked = True

    def get_filler_item_name(self):
        i = None
        while i is None:
            i = getattr(self.options, self.random.choices(list(self.filler_weights.keys()),
                                                          weights=list(self.filler_weights.values()),
                                                          k=1)[0]).get_item(self.random)
        return i

    def create_item(self, item):
        return TetrisItem(item, items[item], self.item_name_to_id[item], self.player)

    def fill_slot_data(self):
        return {
            "starting_speed": self.options.starting_speed.value,
            "cancel_out": self.options.clear_random_lines_and_garbage_lines_cancel_each_other_out.value,
            "max_garbage": self.options.max_simultaneous_garbage_lines.value,
            "max_clears": self.options.max_simultaneous_clear_random_lines.value,
            "goal": self.options.goal_score.value,
            "version": version
        }


class TetrisLocation(Location):
    game = "Tetris"


class TetrisItem(Item):
    game = "Tetris"
