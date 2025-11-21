import os
import unittest
from argparse import Namespace
from contextlib import contextmanager
from typing import Dict, ClassVar, Iterable, Hashable, Tuple, Optional, List, Union, Any

from BaseClasses import MultiWorld, CollectionState, get_seed, Location
from Utils import cache_argsless
from test.bases import WorldTestBase
from test.general import gen_steps, setup_solo_multiworld as setup_base_solo_multiworld
from worlds.AutoWorld import call_all
from worlds.flipwitch import FlipwitchWorld, options
from worlds.flipwitch.options import FlipwitchOptions, FlipwitchOption

DEFAULT_TEST_SEED = get_seed()


@cache_argsless
def default_options():
    return {}


@cache_argsless
def allsanity_options():
    return {
        options.StatShuffle.internal_name: options.StatShuffle.option_true,
        options.Shopsanity.internal_name: options.Shopsanity.option_true,
        options.ShuffleChaosPieces.internal_name: options.ShuffleChaosPieces.option_true,
        options.GachaponShuffle.internal_name: options.GachaponShuffle.option_all,
        options.QuestForSex.internal_name: options.QuestForSex.option_all,
    }


class FlipwitchTestCase(unittest.TestCase):
    # Set False to not skip some 'extra' tests
    skip_base_tests: bool = True
    # Set False to run tests that take long
    skip_long_tests: bool = True

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        base_tests_key = "base"
        if base_tests_key in os.environ:
            cls.skip_base_tests = not bool(os.environ[base_tests_key])
        long_tests_key = "long"
        if long_tests_key in os.environ:
            cls.skip_long_tests = not bool(os.environ[long_tests_key])

    @contextmanager
    def solo_world_sub_test(self, msg: Optional[str] = None,
                            /,
                            world_options: Optional[Dict[Union[str, FlipwitchOption], Any]] = None,
                            *,
                            seed=DEFAULT_TEST_SEED,
                            world_caching=True,
                            dirty_state=False,
                            **kwargs) -> Tuple[MultiWorld, FlipwitchWorld]:
        if msg is not None:
            msg += " "
        else:
            msg = ""
        msg += f"[Seed = {seed}]"

        with self.subTest(msg, **kwargs):
            if world_caching:
                multi_world = setup_solo_multiworld(world_options, seed)
                if dirty_state:
                    original_state = multi_world.state.copy()
            else:
                multi_world = setup_solo_multiworld(world_options, seed, _cache={})

            yield multi_world, multi_world.worlds[1]

            if world_caching and dirty_state:
                multi_world.state = original_state


class FlipwitchTestBase(WorldTestBase, FlipwitchTestCase):
    game = "Flipwitch Forbidden Sex Hex"
    world: FlipwitchWorld
    player: ClassVar[int] = 1

    seed = DEFAULT_TEST_SEED

    def world_setup(self, *args, **kwargs):
        self.options = parse_class_option_keys(self.options)

        super().world_setup(seed=self.seed)
        if self.constructed:
            self.world = self.multiworld.worlds[self.player]  # noqa

    @property
    def run_default_tests(self) -> bool:
        if self.skip_base_tests:
            return False
        # world_setup is overridden, so it'd always run default tests when importing SVTestBase
        is_not_lunacid_test = type(self) is not FlipwitchTestBase
        should_run_default_tests = is_not_lunacid_test and super().run_default_tests
        return should_run_default_tests

    def get_real_locations(self) -> List[Location]:
        return [location for location in self.multiworld.get_locations(self.player) if not location.is_event]

    def get_real_location_names(self) -> List[str]:
        return [location.name for location in self.multiworld.get_locations(self.player) if not location.is_event]


pre_generated_worlds = {}


# Mostly a copy of test.general.setup_solo_multiworld, I just don't want to change the core.
def setup_solo_multiworld(test_options: Optional[Dict[Union[str, FlipwitchOption], str]] = None,
                          seed=DEFAULT_TEST_SEED,
                          _cache: Dict[Hashable, MultiWorld] = {},  # noqa
                          _steps=gen_steps) -> MultiWorld:
    test_options = parse_class_option_keys(test_options)

    # Yes I reuse the worlds generated between tests, its speeds the execution by a couple seconds
    should_cache = "start_inventory" not in test_options
    frozen_options = frozenset({})
    if should_cache:
        frozen_options = frozenset(test_options.items()).union({seed})
        if frozen_options in _cache:
            cached_multi_world = _cache[frozen_options]
            print(f"Using cached solo multi world [Seed = {cached_multi_world.seed}]")
            return cached_multi_world

    multiworld = setup_base_solo_multiworld(FlipwitchWorld, (), seed=seed)
    # print(f"Seed: {multiworld.seed}") # Uncomment to print the seed for every test

    args = Namespace()
    for name, option in FlipwitchWorld.options_dataclass.type_hints.items():
        value = option.from_any(test_options.get(name, option.default))

        setattr(args, name, {1: value})
    multiworld.set_options(args)

    if "start_inventory" in test_options:
        for item, amount in test_options["start_inventory"].items():
            for _ in range(amount):
                multiworld.push_precollected(multiworld.create_item(item, 1))

    for step in _steps:
        call_all(multiworld, step)

    if should_cache:
        _cache[frozen_options] = multiworld

    return multiworld


def parse_class_option_keys(test_options: dict) -> dict:
    """ Now the option class is allowed as key. """
    parsed_options = {}

    if test_options:
        for option, value in test_options.items():
            if hasattr(option, "internal_name"):
                assert option.internal_name not in test_options, "Defined two times by class and internal_name"
                parsed_options[option.internal_name] = value
            else:
                assert option in FlipwitchOptions.type_hints, \
                    f"All keys of world_options must be a possible Flipwitch option, {option} is not."
                parsed_options[option] = value

    return parsed_options


def complete_options_with_default(options_to_complete=None) -> FlipwitchOptions:
    if options_to_complete is None:
        options_to_complete = {}

    for name, option in FlipwitchOptions.type_hints.items():
        options_to_complete[name] = option.from_any(options_to_complete.get(name, option.default))

    return FlipwitchOptions(**options_to_complete)


def setup_multiworld(test_options: Iterable[Dict[str, int]] = None, seed=None) -> MultiWorld:  # noqa
    if test_options is None:
        test_options = []

    multiworld = MultiWorld(len(test_options))
    multiworld.player_name = {}
    multiworld.set_seed(seed)
    multiworld.state = CollectionState(multiworld)
    for i in range(1, len(test_options) + 1):
        multiworld.game[i] = FlipwitchWorld.game
        multiworld.player_name.update({i: f"Tester{i}"})
    args = Namespace()
    for name, option in FlipwitchWorld.options_dataclass.type_hints.items():
        options = {}
        for i in range(1, len(test_options) + 1):
            player_options = test_options[i - 1]
            value = option(player_options[name]) if name in player_options else option.from_any(option.default)
            options.update({i: value})
        setattr(args, name, options)
    multiworld.set_options(args)

    for step in gen_steps:
        call_all(multiworld, step)

    return multiworld
