import unittest
from collections import defaultdict
from types import SimpleNamespace
from unittest.mock import Mock, patch

from NetUtils import ClientStatus
from BaseClasses import ItemClassification
from MultiServer import Context, ServerCommandProcessor, collect_player_cleared, \
    is_refundable_hint, release_player, send_remaining, update_client_status
from NetUtils import Hint, LocationStore


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


class TestCustomCollectionHints(unittest.TestCase):
    def setUp(self):
        from MultiServer import collect_hints, resolve_custom_item_hints
        self.collect = collect_hints
        self.resolve = resolve_custom_item_hints
        self.ctx = SimpleNamespace(
            groups={}, games={1: "AlchapelaBot", 2: "Metroid"},
            slot_data={1: {"custom_item_triggers": {2: {
                "Missile Pack": {"item_id": 100, "locations": [10, 11]},
                "Progressive Missile": {"item_id": 101, "locations": [12, 13]},
            }}}},
            locations=LocationStore({
                1: {10: (50, 2, 1), 11: (50, 2, 1), 12: (100, 1, 1), 13: (51, 2, 1)},
                3: {20: (101, 1, 1), 21: (101, 1, 1)},
                2: {30: (52, 2, 1)},
            }),
            get_hint=Mock(return_value=None), location_checks=defaultdict(set), er_hint_data={},
        )

    def test_nested_pack_hints_outer_progressive_with_real_recipient(self):
        hints = self.resolve(self.ctx, 0, 2, self.collect(self.ctx, 0, 2, 50))
        self.assertEqual({20, 21}, {hint.location for hint in hints})
        self.assertTrue(all(hint.receiving_player == 1 and hint.item == 101 for hint in hints))

    def test_direct_progressive_content(self):
        hints = self.resolve(self.ctx, 0, 2, self.collect(self.ctx, 0, 2, 51))
        self.assertEqual({20, 21}, {hint.location for hint in hints})

    def test_regular_item_is_unchanged(self):
        hints = self.collect(self.ctx, 0, 2, 52)
        self.assertEqual(hints, self.resolve(self.ctx, 0, 2, hints))

    def test_custom_pack_alias_follows_outer_progressive(self):
        from MultiServer import collect_custom_trigger_hints
        hints = collect_custom_trigger_hints(self.ctx, 0, 2, {"item_id": 100})
        self.assertEqual({20, 21}, {hint.location for hint in hints})

    def test_buyer_receives_and_remembers_foreign_hint(self):
        hint = self.collect(self.ctx, 0, 1, 101)[0]
        client = SimpleNamespace(no_text=False)
        ctx = SimpleNamespace(
            hints=defaultdict(set), slot_set=lambda slot: {slot},
            logger=Mock(), on_new_hint=Mock(), clients={0: {2: [client]}},
            send_msgs=Mock(return_value="send task"),
        )
        with patch("MultiServer.format_hint", return_value="hint text"), \
                patch("MultiServer.async_start") as start:
            Context.notify_hints(ctx, 0, [hint], hinting_player=2)
        self.assertIn(hint, ctx.hints[0, 2])
        self.assertIn(hint, ctx.hints[0, 1])
        self.assertIn(hint, ctx.hints[0, 3])
        ctx.send_msgs.assert_called_once_with(client, [hint.as_network_message()])
        start.assert_called_once_with("send task")


class TestGeneratedHintPoints(unittest.TestCase):
    def test_generated_values_survive_datapackage_and_credit_all_owners(self):
        import json
        from BaseClasses import MultiWorld
        from Fill import get_hint_sphere_point_totals
        from MultiServer import get_owner_hint_point_items, get_hint_point_item_value
        from NetUtils import NetworkItem
        from worlds.alchapelabot import AlchapelaBotWorld

        multiworld = MultiWorld(1)
        multiworld.player_name = {1: "Bot"}
        world = AlchapelaBotWorld(multiworld, 1)
        world.options = SimpleNamespace(start_games=SimpleNamespace(value=[]))
        world.generate_early()
        received = []
        expected = {}
        for owner, budget in ((0, 44), (10, 35), (15, 57)):
            totals = get_hint_sphere_point_totals({1: 1, 2: 4, 999: 2}, budget, 999)
            self.assertEqual(budget, totals[1] + totals[2])
            self.assertLessEqual(abs(totals[1] - totals[2]), 1)
            expected[owner] = sum(totals.values())
            for sphere, count in ((1, 1), (2, 4), (999, 2)):
                base, remainder = divmod(totals[sphere], count)
                for index in range(count):
                    item = world.create_hint_point_item(owner, base + (index < remainder))
                    received.append(NetworkItem(item.code, len(received), 2, item.flags))
        data = {"datapackage": {world.game: {}}}
        world.modify_multidata(data)
        package = json.loads(json.dumps(data))["datapackage"][world.game]
        ctx = SimpleNamespace(
            games={1: world.game}, owners={2: 0, 3: 10, 4: 15},
            item_names={world.game: {code: name for name, code in package["item_name_to_id"].items()}},
            received_items={(0, 1, True): received[1:]}, start_inventory={1: received[:1]},
            er_hint_data={}, seed_name="31218148747982571502",
        )
        for owner, total in expected.items():
            self.assertEqual(total, get_owner_hint_point_items(ctx, 0, owner))
        self.assertEqual(sum(expected.values()), sum(get_hint_point_item_value(ctx, item)[1] for item in received))
        self.assertEqual("Ophilla", get_hint_point_item_value(ctx, received[7])[0])
        ctx.start_inventory[1].append(NetworkItem(1010, -2, 0))
        self.assertEqual(expected[10] + 1, get_owner_hint_point_items(ctx, 0, 10))
        self.assertIsNone(get_hint_point_item_value(ctx, NetworkItem(100000, 1, 2)))

    def test_empty_and_unreachable_only_spheres(self):
        from Fill import get_hint_sphere_point_totals
        self.assertEqual({}, get_hint_sphere_point_totals({}, 20, 999))
        self.assertEqual({}, get_hint_sphere_point_totals({999: 2}, 20, 999))


class TestExactConnectionNames(unittest.IsolatedAsyncioTestCase):
    async def test_xp_name_does_not_authenticate_against_ap_alias(self):
        import base64
        from unittest.mock import AsyncMock
        from MultiServer import process_client_cmd
        xp = base64.b64encode(b"XP123_1_12345678900").decode()
        ap = base64.b64encode(b"AP123_1_12345678900").decode()
        ctx = SimpleNamespace(password=None, connect_names={ap: (0, 2)}, compatibility=2,
                              logger=Mock(), send_msgs=AsyncMock())
        args = {"cmd": "Connect", "name": xp, "password": None, "game": "A Link to the Past Beta"}
        await process_client_cmd(ctx, SimpleNamespace(), args)
        self.assertEqual(xp, args["name"])
        self.assertIn("InvalidSlot", ctx.send_msgs.call_args.args[1][0]["errors"])


    async def test_exact_xp_key_connects(self):
        import base64
        from unittest.mock import AsyncMock
        from MultiServer import process_client_cmd
        from NetUtils import NetworkItem
        from Utils import Version
        key = base64.b64encode(b"XP123_1_12345678900").decode()
        ctx = SimpleNamespace(
            password=None, connect_names={key: (0, 2)}, compatibility=2,
            games={2: "A Link to the Past Beta"}, minimum_client_versions={2: Version(0, 0, 0)},
            received_items={(0, 1, True): [NetworkItem(2, 1, 1)]}, start_inventory={},
            clients={0: {2: []}}, client_ids={}, slot_info={}, get_players_package=Mock(return_value=[]),
            send_msgs=AsyncMock(),
        )
        client = SimpleNamespace(auth=False, remote_items=True, remote_start_inventory=True, no_items=False)
        args = {"cmd": "Connect", "name": key, "password": None, "game": ctx.games[2],
                "tags": set(), "items_handling": 7, "version": Version(0, 6, 8),
                "uuid": "test", "slot_data": False}
        with patch("MultiServer.get_missing_checks", return_value=[]), \
                patch("MultiServer.get_checked_checks", return_value=[]), \
                patch("MultiServer.get_slot_points", return_value=0), \
                patch("MultiServer.get_slot_location_points", return_value=0), \
                patch("MultiServer.on_client_joined", new=AsyncMock()):
            await process_client_cmd(ctx, client, args)
        self.assertTrue(client.auth)
        self.assertEqual("Connected", ctx.send_msgs.call_args.args[1][0]["cmd"])
