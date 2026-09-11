import unittest
from collections import defaultdict
from types import SimpleNamespace
from unittest.mock import Mock, patch

from NetUtils import ClientStatus
from MultiServer import Context, ServerCommandProcessor, collect_player_cleared, update_client_status


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
