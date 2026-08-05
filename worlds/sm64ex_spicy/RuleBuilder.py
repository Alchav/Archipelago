from __future__ import annotations

import dataclasses
from collections.abc import Callable, Iterable
from typing import TYPE_CHECKING, ClassVar, TypeAlias

from typing_extensions import override

from BaseClasses import CollectionState
from NetUtils import JSONMessagePart
from rule_builder.rules import HasAny, Rule
from .Items import ut_glitch_item_name

if TYPE_CHECKING:
    from . import SM64World


@dataclasses.dataclass(frozen=True)
class CoinSourceTrace:
    """One coin source or route group in a coin-logic evaluation."""

    source_id: str
    label: str
    coins: int
    counted: bool
    available: bool = True
    children: tuple[CoinSourceTrace, ...] = ()
    red_coin_ids: frozenset[int] = frozenset()
    max_coins: int | None = None
    reachable_red_coin_ids_when_uncounted: frozenset[int] = frozenset()

    def __post_init__(self) -> None:
        if not self.source_id:
            raise ValueError("Coin source IDs must not be empty")
        if not self.label:
            raise ValueError("Coin source labels must not be empty")
        if self.coins < 0:
            raise ValueError("Coin source values must not be negative")
        if self.max_coins is not None and self.max_coins < self.coins:
            raise ValueError("Maximum coin source value cannot be less than its counted value")
        if self.counted and not self.available:
            raise ValueError("An unavailable coin source cannot be counted")
        if not isinstance(self.children, tuple):
            object.__setattr__(self, "children", tuple(self.children))
        if not isinstance(self.red_coin_ids, frozenset):
            object.__setattr__(self, "red_coin_ids", frozenset(self.red_coin_ids))
        if not self.red_coin_ids.issubset(range(1, 9)):
            raise ValueError("Red Coin IDs must be between 1 and 8")
        if not isinstance(self.reachable_red_coin_ids_when_uncounted, frozenset):
            object.__setattr__(
                self, "reachable_red_coin_ids_when_uncounted",
                frozenset(self.reachable_red_coin_ids_when_uncounted))
        if not self.reachable_red_coin_ids_when_uncounted.issubset(range(1, 9)):
            raise ValueError("Reachable uncounted Red Coin IDs must be between 1 and 8")

    @property
    def available_red_coin_ids(self) -> frozenset[int]:
        if not self.available:
            return frozenset()
        result = set(self.red_coin_ids)
        for child in self.children:
            result.update(child.available_red_coin_ids)
        return frozenset(result)


@dataclasses.dataclass(frozen=True)
class CoinEvaluation:
    """The reachable coin total and its structured explanation trace."""

    reachable_coins: int
    children: tuple[CoinSourceTrace, ...] = ()

    def __post_init__(self) -> None:
        if self.reachable_coins < 0:
            raise ValueError("Reachable coin totals must not be negative")
        if not isinstance(self.children, tuple):
            object.__setattr__(self, "children", tuple(self.children))

    @property
    def reachable_red_coin_ids(self) -> frozenset[int]:
        def collect(source: CoinSourceTrace, parent_counted: bool) -> set[int]:
            counted = parent_counted and source.counted
            result = set(source.red_coin_ids) if counted else set()
            if parent_counted and source.available:
                result.update(source.reachable_red_coin_ids_when_uncounted)
            for child in source.children:
                result.update(collect(child, counted))
            return result

        result: set[int] = set()
        for source in self.children:
            result.update(collect(source, True))
        return frozenset(result)


CoinEvaluator: TypeAlias = Callable[[CollectionState, int, int], bool | CoinEvaluation]


@dataclasses.dataclass()
class HasUnlock(Rule["SM64World"], game="SM64: Spicy Mycena 64"):
    """Accept a global or per-level unlock, including game-only StartInventory."""

    global_item_name: str
    per_level_item_name: str

    @override
    def _instantiate(self, world: SM64World) -> Rule.Resolved:
        item_names = tuple(
            name for name in dict.fromkeys((self.global_item_name, self.per_level_item_name))
            if name in world.item_name_to_id
        )
        if not item_names:
            raise ValueError(
                f"Neither unlock item exists: {self.global_item_name}, {self.per_level_item_name}")
        start_inventory_ids = getattr(world, "start_inventory_item_ids", set())
        starts_unlocked = any(world.item_name_to_id[name] in start_inventory_ids for name in item_names)
        return self.Resolved(
            item_names,
            HasAny(*item_names).resolve(world),
            starts_unlocked,
            player=world.player,
            caching_enabled=getattr(world, "rule_caching_enabled", False),
        )

    class Resolved(Rule.Resolved):
        item_names: tuple[str, ...]
        item_rule: Rule.Resolved
        starts_unlocked: bool

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            return self.starts_unlocked or self.item_rule(state)

        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            return self.item_rule.item_dependencies()

        @override
        def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
            if self.starts_unlocked:
                return [{"type": "text", "text": "Unlocked in StartInventory"}]
            return self.item_rule.explain_json(state)


@dataclasses.dataclass(frozen=True)
class CoinEvaluatorRegistration:
    evaluator: CoinEvaluator
    item_dependencies: tuple[str, ...] = ()
    region_dependencies: tuple[str, ...] = ()
    location_dependencies: tuple[str, ...] = ()
    entrance_dependencies: tuple[str, ...] = ()


_coin_evaluators: dict[str, CoinEvaluatorRegistration] = {}


def register_coin_evaluator(
        course_name: str,
        evaluator: CoinEvaluator,
        *,
        item_dependencies: Iterable[str] = (),
        region_dependencies: Iterable[str] = (),
        location_dependencies: Iterable[str] = (),
        entrance_dependencies: Iterable[str] = (),
) -> None:
    """Register a course evaluator without requiring RuleBuilder to import Rules."""
    if not course_name:
        raise ValueError("Course names must not be empty")

    registration = CoinEvaluatorRegistration(
        evaluator,
        tuple(item_dependencies),
        tuple(region_dependencies),
        tuple(location_dependencies),
        tuple(entrance_dependencies),
    )
    previous = _coin_evaluators.get(course_name)
    if previous is not None and previous != registration:
        raise ValueError(f"A coin evaluator is already registered for {course_name}")
    _coin_evaluators[course_name] = registration


def unregister_coin_evaluator(course_name: str) -> None:
    """Remove a registered evaluator. Intended primarily for isolated tests."""
    _coin_evaluators.pop(course_name, None)


def get_coin_evaluator(course_name: str) -> CoinEvaluatorRegistration:
    try:
        return _coin_evaluators[course_name]
    except KeyError as error:
        raise KeyError(f"No coin evaluator is registered for {course_name}") from error


def evaluate_coins(
        state: CollectionState,
        player: int,
        course_name: str,
        required_coins: int,
) -> bool | CoinEvaluation:
    cache = getattr(state, "sm64_coin_evaluation_cache", None)
    if cache is None:
        cache = {}
        try:
            state.sm64_coin_evaluation_cache = cache
        except AttributeError:
            # Lightweight evaluator tests may use an immutable stand-in state.
            pass

    cache_key = (player, course_name)
    cached = cache.get(cache_key)
    if isinstance(cached, CoinEvaluation):
        return cached

    result = get_coin_evaluator(course_name).evaluator(
        state, player, required_coins)
    if isinstance(result, CoinEvaluation):
        cache[cache_key] = result
    return result


def _format_coin_source(source: CoinSourceTrace, depth: int) -> list[JSONMessagePart]:
    displayed_max = source.max_coins if source.max_coins is not None else source.coins
    if source.counted:
        color = "green"
        amount = f"+{source.coins}"
        if source.max_coins is not None and source.coins != source.max_coins:
            amount += f"/{source.max_coins}"
        suffix = ""
    elif source.available:
        color = "yellow"
        amount = f"0/{displayed_max}"
        suffix = " (not selected)"
    else:
        color = "salmon"
        amount = f"0/{displayed_max}"
        suffix = " (unavailable)"

    messages: list[JSONMessagePart] = [
        {"type": "text", "text": f"\n{'  ' * depth}"},
        {"type": "color", "color": color, "text": amount},
        {"type": "text", "text": " "},
        {"type": "color", "color": color, "text": source.label},
    ]
    if suffix:
        messages.append({"type": "text", "text": suffix})
    for child in source.children:
        messages.extend(_format_coin_source(child, depth + 1))
    return messages


def format_coin_evaluation(
        course_name: str,
        required_coins: int,
        evaluation: CoinEvaluation,
) -> list[JSONMessagePart]:
    """Format a structured coin evaluation for print_json consumers."""
    accessible = evaluation.reachable_coins >= required_coins
    messages: list[JSONMessagePart] = [
        {"type": "text", "text": "Reachable coins in "},
        {"type": "color", "color": "cyan", "text": course_name},
        {"type": "text", "text": ": "},
        {
            "type": "color",
            "color": "green" if accessible else "salmon",
            "text": f"{evaluation.reachable_coins}/{required_coins}",
        },
    ]
    for child in evaluation.children:
        messages.extend(_format_coin_source(child, 1))
    return messages


@dataclasses.dataclass()
class CanCollectCoins(Rule["SM64World"], game="SM64: Spicy Mycena 64"):
    """Require a course's registered evaluator to reach a coin threshold."""

    course_name: str
    required_coins: int

    def __post_init__(self) -> None:
        super().__post_init__()
        if not self.course_name:
            raise ValueError("Course names must not be empty")
        if self.required_coins < 0:
            raise ValueError("Required coin counts must not be negative")

    @override
    def _instantiate(self, world: SM64World) -> Rule.Resolved:
        registration = get_coin_evaluator(self.course_name)
        return self.Resolved(
            self.course_name,
            self.required_coins,
            registration.item_dependencies,
            registration.region_dependencies,
            registration.location_dependencies,
            registration.entrance_dependencies,
            player=world.player,
            caching_enabled=getattr(world, "rule_caching_enabled", False),
        )

    class Resolved(Rule.Resolved):
        course_name: str
        required_coins: int
        item_dependency_names: tuple[str, ...]
        region_dependency_names: tuple[str, ...]
        location_dependency_names: tuple[str, ...]
        entrance_dependency_names: tuple[str, ...]

        # Coin evaluators may contain state.can_reach calls and route selection.
        # Recalculate until every migrated evaluator has audited dependencies.
        force_recalculate: ClassVar[bool] = True

        def _evaluate_registered(self, state: CollectionState) -> bool | CoinEvaluation:
            result = evaluate_coins(
                state, self.player, self.course_name, self.required_coins)
            if not isinstance(result, (bool, CoinEvaluation)):
                raise TypeError(
                    f"The coin evaluator for {self.course_name} returned "
                    f"{type(result).__name__}, expected bool or CoinEvaluation"
                )
            return result

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            result = self._evaluate_registered(state)
            if isinstance(result, bool):
                return result
            return result.reachable_coins >= self.required_coins

        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            return {name: {id(self)} for name in self.item_dependency_names}

        @override
        def region_dependencies(self) -> dict[str, set[int]]:
            return {name: {id(self)} for name in self.region_dependency_names}

        @override
        def location_dependencies(self) -> dict[str, set[int]]:
            return {name: {id(self)} for name in self.location_dependency_names}

        @override
        def entrance_dependencies(self) -> dict[str, set[int]]:
            return {name: {id(self)} for name in self.entrance_dependency_names}

        @override
        def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
            if state is None:
                return [
                    {"type": "text", "text": "Collect "},
                    {"type": "color", "color": "cyan", "text": str(self.required_coins)},
                    {"type": "text", "text": " coins in "},
                    {"type": "color", "color": "cyan", "text": self.course_name},
                ]

            result = self._evaluate_registered(state)
            if isinstance(result, CoinEvaluation):
                return format_coin_evaluation(self.course_name, self.required_coins, result)

            return [
                {"type": "text", "text": "Can collect " if result else "Cannot collect "},
                {
                    "type": "color",
                    "color": "green" if result else "salmon",
                    "text": str(self.required_coins),
                },
                {"type": "text", "text": " coins in "},
                {"type": "color", "color": "cyan", "text": self.course_name},
            ]

        @override
        def explain_str(self, state: CollectionState | None = None) -> str:
            if state is None:
                return str(self)
            result = self._evaluate_registered(state)
            if isinstance(result, bool):
                prefix = "Can" if result else "Cannot"
                return f"{prefix} collect {self.required_coins} coins in {self.course_name}"
            return (
                f"Reachable coins in {self.course_name}: "
                f"{result.reachable_coins}/{self.required_coins}"
            )

        @override
        def __str__(self) -> str:
            return f"Collect {self.required_coins} coins in {self.course_name}"


@dataclasses.dataclass()
class CanCollectAllRedCoins(Rule["SM64World"], game="SM64: Spicy Mycena 64"):
    """Require every Red Coin in a course to be logically reachable."""

    course_name: str

    @override
    def _instantiate(self, world: SM64World) -> Rule.Resolved:
        get_coin_evaluator(self.course_name)
        return self.Resolved(
            self.course_name,
            player=world.player,
            caching_enabled=getattr(world, "rule_caching_enabled", False),
        )

    class Resolved(Rule.Resolved):
        course_name: str
        force_recalculate: ClassVar[bool] = True

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            # Region reachability can change while CollectionState is sweeping.
            # Red Coin Stars must inspect a fresh trace rather than the coin-rule cache.
            result = get_coin_evaluator(self.course_name).evaluator(
                state, self.player, 0)
            return isinstance(result, CoinEvaluation) and result.reachable_red_coin_ids == frozenset(range(1, 9))

        @override
        def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
            return [
                {"type": "text", "text": "Reach all eight Red Coins in "},
                {"type": "color", "color": "cyan", "text": self.course_name},
            ]

        @override
        def explain_str(self, state: CollectionState | None = None) -> str:
            if state is None:
                return str(self)
            prefix = "Can" if self._evaluate(state) else "Cannot"
            return f"{prefix} reach all eight Red Coins in {self.course_name}"

        @override
        def __str__(self) -> str:
            return f"Reach all eight Red Coins in {self.course_name}"


@dataclasses.dataclass()
class LogicTrick(Rule["SM64World"], game="SM64: Spicy Mycena 64"):
    """Preserve a selected logic trick's identity around its concrete requirements."""

    option_key: str
    child: Rule
    ut_glitched: bool = False

    @override
    def _instantiate(self, world: SM64World) -> Rule.Resolved:
        return self.Resolved(
            self.option_key,
            self.child.resolve(world),
            self.ut_glitched,
            player=world.player,
            caching_enabled=getattr(world, "rule_caching_enabled", False),
        )

    @override
    def to_dict(self) -> dict:
        data = super().to_dict()
        data["args"]["child"] = self.child.to_dict()
        return data

    @override
    @classmethod
    def from_dict(cls, data, world_cls):
        args = dict(data.get("args", {}))
        child = world_cls.rule_from_dict(args.pop("child"))
        return cls(
            args["option_key"],
            child,
            args.get("ut_glitched", False),
            options=(),
            filtered_resolution=data.get("filtered_resolution", False),
        )

    class Resolved(Rule.Resolved):
        option_key: str
        child: Rule.Resolved
        ut_glitched: bool

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            if self.ut_glitched and not state.has(ut_glitch_item_name, self.player):
                return False
            return self.child(state)

        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            dependencies = {
                name: {id(self), *rules}
                for name, rules in self.child.item_dependencies().items()
            }
            if self.ut_glitched:
                dependencies.setdefault(ut_glitch_item_name, set()).add(id(self))
            return dependencies

        @override
        def region_dependencies(self) -> dict[str, set[int]]:
            return {
                name: {id(self), *rules}
                for name, rules in self.child.region_dependencies().items()
            }

        @override
        def location_dependencies(self) -> dict[str, set[int]]:
            return {
                name: {id(self), *rules}
                for name, rules in self.child.location_dependencies().items()
            }

        @override
        def entrance_dependencies(self) -> dict[str, set[int]]:
            return {
                name: {id(self), *rules}
                for name, rules in self.child.entrance_dependencies().items()
            }

        @override
        def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
            enabled = state is None or self(state)
            messages: list[JSONMessagePart] = [
                {
                    "type": "color",
                    "color": "green" if enabled else "salmon",
                    "text": self.option_key,
                },
            ]
            if self.ut_glitched:
                messages.append({"type": "text", "text": " (Universal Tracker glitched logic)"})
            messages.append({"type": "text", "text": ": "})
            messages.extend(self.child.explain_json(state))
            return messages

        @override
        def explain_str(self, state: CollectionState | None = None) -> str:
            suffix = " (Universal Tracker glitched logic)" if self.ut_glitched else ""
            return f"{self.option_key}{suffix}: {self.child.explain_str(state)}"

        @override
        def __str__(self) -> str:
            return self.explain_str()
