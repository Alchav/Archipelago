import unittest
from collections import defaultdict
from fractions import Fraction
from types import SimpleNamespace
from unittest.mock import Mock, patch

from NetUtils import ClientStatus
from BaseClasses import ItemClassification
from MultiServer import Context, ServerCommandProcessor, _apportion_hint_values_by_sphere, collect_player_cleared, \
    is_refundable_hint, release_player, send_remaining, update_client_status
from NetUtils import Hint


class TestResolvePlayerName(unittest.TestCase):
    def test_resolve(self) -> None:
        p = ServerCommandProcessor(Context("", 0, "", "", 0, 0, 0, False))
        p.ctx.player_names = {
            (1, 1): "AAA",
            (1, 2): "aBc",
            (1, 3): "abC",
        }
        assert not p.resolve_player("abc"), "ambiguous name entry shouldn't resolve to player"
        assert not p.resolve_player("Abc"), "ambiguous name entry shouldn't resolve to player"
        assert p.resolve_player("aBc") == (1, 2, "aBc"), "matching case resolve"
        assert p.resolve_player("abC") == (1, 3, "abC"), "matching case resolve"
        assert not p.resolve_player("aB"), "partial name shouldn't resolve to player"
        assert not p.resolve_player("abCD"), "incorrect name shouldn't resolve to player"

        p.ctx.player_names = {
            (1, 1): "aaa",
            (1, 2): "abc",
            (1, 3): "abC",
        }
        assert p.resolve_player("abc") == (1, 2, "abc"), "matching case resolve"
        assert not p.resolve_player("Abc"), "ambiguous name entry shouldn't resolve to player"
        assert not p.resolve_player("aBc"), "ambiguous name entry shouldn't resolve to player"
        assert p.resolve_player("abC") == (1, 3, "abC"), "matching case resolve"

        p.ctx.player_names = {
            (1, 1): "AbcdE",
            (1, 2): "abc",
            (1, 3): "abCD",
        }
        assert p.resolve_player("abc") == (1, 2, "abc"), "matching case resolve"
        assert p.resolve_player("abC") == (1, 2, "abc"), "case insensitive resolves when 1 match"
        assert p.resolve_player("Abc") == (1, 2, "abc"), "case insensitive resolves when 1 match"
        assert p.resolve_player("ABC") == (1, 2, "abc"), "case insensitive resolves when 1 match"
        assert p.resolve_player("abcd") == (1, 3, "abCD"), "case insensitive resolves when 1 match"
        assert not p.resolve_player("aB"), "partial name shouldn't resolve to player"


class TestClearedCollect(unittest.TestCase):
    def setUp(self) -> None:
        self.ctx = SimpleNamespace(
            client_game_state=defaultdict(int),
            location_checks=defaultdict(set),
            locations={1: {10: (), 11: (), 12: ()}},
            er_hint_data={1: {12: "Unreachable"}},
        )

    def test_requires_goal_completion(self) -> None:
        self.ctx.location_checks[0, 1] = {10, 11, 12}
        with patch("MultiServer.collect_player") as collect:
            self.assertFalse(collect_player_cleared(self.ctx, 0, 1))
            collect.assert_not_called()

    def test_collects_reachable_locations_after_goal(self) -> None:
        self.ctx.client_game_state[0, 1] = ClientStatus.CLIENT_GOAL
        self.ctx.location_checks[0, 1] = {10, 11}
        with patch("MultiServer.collect_player") as collect:
            self.assertTrue(collect_player_cleared(self.ctx, 0, 1))
            collect.assert_called_once_with(self.ctx, 0, 1, include_unreachable=False)

    def test_collects_all_locations_after_goal(self) -> None:
        self.ctx.client_game_state[0, 1] = ClientStatus.CLIENT_GOAL
        self.ctx.location_checks[0, 1] = {10, 11, 12}
        with patch("MultiServer.collect_player") as collect:
            self.assertTrue(collect_player_cleared(self.ctx, 0, 1))
            collect.assert_called_once_with(self.ctx, 0, 1)

    def test_goal_state_is_set_before_goal_callback(self) -> None:
        client = SimpleNamespace(team=0, slot=1)
        ctx = SimpleNamespace(
            client_game_state=defaultdict(int),
            player_names={(0, 1): "Player"},
            on_client_status_change=Mock(),
            save=Mock(),
        )

        def assert_goal_is_set(_client) -> None:
            self.assertEqual(ClientStatus.CLIENT_GOAL, ctx.client_game_state[0, 1])

        ctx.on_goal_achieved = Mock(side_effect=assert_goal_is_set)
        ctx.broadcast_text_all = Mock()

        update_client_status(ctx, client, ClientStatus.CLIENT_GOAL)
        ctx.on_goal_achieved.assert_called_once_with(client)

    def test_auto_remaining_runs_on_goal_completion(self) -> None:
        client = SimpleNamespace(team=0, slot=1)
        ctx = SimpleNamespace(
            get_aliased_name=Mock(return_value="Player"),
            broadcast_text_all=Mock(),
            collect_mode="disabled",
            release_mode="disabled",
            remaining_mode="auto",
            save=Mock(),
        )

        with patch("MultiServer.send_remaining") as send_remaining:
            Context.on_goal_achieved(ctx, client)

        send_remaining.assert_called_once_with(ctx, client)

    def test_auto_remaining_runs_after_auto_release(self) -> None:
        client = SimpleNamespace(team=0, slot=1)
        calls = Mock()
        ctx = SimpleNamespace(
            get_aliased_name=Mock(return_value="Player"),
            broadcast_text_all=Mock(),
            collect_mode="disabled",
            release_mode="auto",
            remaining_mode="auto",
            save=Mock(),
        )

        with patch("MultiServer.release_player", side_effect=calls.release), \
                patch("MultiServer.send_remaining", side_effect=calls.remaining):
            Context.on_goal_achieved(ctx, client)

        self.assertEqual(["release", "remaining"], [call[0] for call in calls.mock_calls])

    def test_remaining_list_is_sent_before_hints(self) -> None:
        client = SimpleNamespace(team=0, slot=1)
        calls = Mock()
        ctx = SimpleNamespace(
            notify_client_multiple=Mock(side_effect=calls.remaining_list),
            notify_client=Mock(side_effect=calls.no_remaining),
            notify_hints=Mock(side_effect=calls.hints),
        )

        with patch("MultiServer._prepare_remaining", return_value=(["Item"], ["Hint"])):
            send_remaining(ctx, client)

        self.assertEqual(["remaining_list", "hints"], [call[0] for call in calls.mock_calls])


class TestNonAdvancementRelease(unittest.TestCase):
    def test_releases_only_non_advancement_locations(self) -> None:
        ctx = SimpleNamespace(
            locations={1: {
                10: (100, 2, ItemClassification.progression),
                11: (101, 2, ItemClassification.useful),
                12: (102, 2, ItemClassification.trap),
                13: (103, 2, ItemClassification.filler),
            }},
            player_names={(0, 1): "Player"},
            broadcast_text_all=Mock(),
        )

        with patch("MultiServer.register_location_checks") as register, \
                patch("MultiServer.update_checked_locations") as update:
            release_player(ctx, 0, 1, non_advancement=True)

        register.assert_called_once_with(ctx, 0, 1, {11, 12, 13})
        update.assert_called_once_with(ctx, 0, 1)


class TestProportionalHintPoints(unittest.TestCase):
    def test_dense_sphere_items_are_worth_proportionally_less(self) -> None:
        sparse_location = (1, 100)
        dense_locations = [(2, location) for location in range(200, 224)]
        values = _apportion_hint_values_by_sphere({
            2: [sparse_location],
            4: dense_locations,
        }, 44)

        self.assertEqual(Fraction(22), values[sparse_location])
        self.assertEqual(Fraction(11, 12), values[dense_locations[0]])
        self.assertEqual(Fraction(24), values[sparse_location] / values[dense_locations[0]])
        self.assertEqual(Fraction(44), sum(values.values(), Fraction()))

    def test_integer_remainder_is_distributed_between_spheres(self) -> None:
        values = _apportion_hint_values_by_sphere({
            1: [(1, 10), (1, 11)],
            2: [(1, 12)],
        }, 5)

        self.assertEqual(Fraction(3), values[1, 10] + values[1, 11])
        self.assertEqual(Fraction(2), values[1, 12])
        self.assertEqual(Fraction(5), sum(values.values(), Fraction()))


class TestRefundableHints(unittest.TestCase):
    def test_all_items_in_selected_location_games_are_refundable(self) -> None:
        ctx = SimpleNamespace(games={1: "Jigsaw", 2: "Tetris", 3: "Yacht Dice"})

        for player, classification in (
                (1, ItemClassification.filler),
                (2, ItemClassification.trap),
                (3, ItemClassification.progression)):
            with self.subTest(player=player, classification=classification):
                hint = Hint(4, player, 100, 200, False, item_flags=classification)
                self.assertTrue(is_refundable_hint(ctx, hint))

    def test_items_in_other_location_games_are_not_refundable(self) -> None:
        ctx = SimpleNamespace(games={1: "A Link to the Past"})

        hint = Hint(3, 1, 100, 200, False, item_flags=ItemClassification.progression)

        self.assertFalse(is_refundable_hint(ctx, hint))
