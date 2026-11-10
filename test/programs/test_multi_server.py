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


class TestHintAll(unittest.TestCase):
    def run_purchase(self, query="Sword", enabled=True, for_location=False, points=10, cost=10, known=()):
        import random
        from MultiServer import ClientMessageProcessor
        from NetUtils import HintStatus
        sword = [Hint(2, 3, location, 100, False, item_flags=1, status=HintStatus.HINT_PRIORITY)
                 for location in (10, 11)]
        shield = [Hint(2, 3, 12, 101, False, item_flags=1, status=HintStatus.HINT_PRIORITY)]
        ctx = SimpleNamespace(
            hint_all=enabled, games={2: "Test", 3: "Test"}, slot_data={},
            get_hint_cost=Mock(return_value=cost), get_hint_location_cost=Mock(return_value=cost),
            hints=defaultdict(set), hints_used=defaultdict(int), hint_locations_used=defaultdict(int),
            all_item_and_group_names={"Test": {"Sword", "Shield", "Equipment"}},
            all_location_and_group_names={"Test": {"Locations"}},
            item_names={"Test": {100: "Sword", 101: "Shield"}}, location_names={"Test": {}},
            item_names_for_game=lambda game: {"Sword": 100, "Shield": 101},
            location_names_for_game=lambda game: {"Locations": 10},
            item_name_groups={"Test": {"Equipment": {"Sword", "Shield"}}},
            location_name_groups={"Test": {}}, non_hintable_names={"Test": set()},
            random=random.Random(1), get_sphere=lambda player, location: location,
            er_hint_data={3: {10: "", 11: "", 12: ""}}, notify_hints=Mock(), save=Mock(),
        )
        ctx.hints[0, 2].update(sword[index] for index in known)
        processor = ClientMessageProcessor(ctx, SimpleNamespace(team=0, slot=2))
        processor.output = Mock()
        def collect(_ctx, team, slot, name):
            return sword if name in ("Sword", 100) else shield
        with patch("MultiServer.get_client_points", return_value=points), \
                patch("MultiServer.get_client_location_points", return_value=points), \
                patch("MultiServer.collect_hints", side_effect=collect), \
                patch("MultiServer.collect_hint_location_name", return_value=sword):
            processor.get_hints(query, for_location)
        return ctx

    def test_name_and_id_reveal_every_copy_for_one_purchase(self):
        for query in ("Sword", "100"):
            ctx = self.run_purchase(query)
            self.assertEqual({10, 11}, {h.location for h in ctx.notify_hints.call_args.args[1]})
            self.assertEqual(1, ctx.hints_used[0, 2])

    def test_group_selects_only_one_item_even_when_hints_are_free(self):
        for cost in (0, 10):
            ctx = self.run_purchase("Equipment", cost=cost)
            hints = ctx.notify_hints.call_args.args[1]
            self.assertEqual({100}, {hint.item for hint in hints})
            self.assertEqual(2, len(hints))

    def test_disabled_keeps_single_hint(self):
        ctx = self.run_purchase(enabled=False)
        self.assertEqual(1, len(ctx.notify_hints.call_args.args[1]))

    def test_location_hint_is_not_expanded(self):
        ctx = self.run_purchase("Locations", for_location=True)
        self.assertEqual(1, len(ctx.notify_hints.call_args.args[1]))
        self.assertEqual(1, ctx.hint_locations_used[0, 2])
        self.assertEqual(0, ctx.hints_used[0, 2])

    def test_insufficient_points_does_not_reveal_new_copies(self):
        ctx = self.run_purchase(points=0)
        self.assertEqual([], ctx.notify_hints.call_args.args[1])
        self.assertEqual(0, ctx.hints_used[0, 2])

    def test_previous_copy_does_not_prevent_expansion(self):
        ctx = self.run_purchase(known=(0,))
        self.assertEqual({10, 11}, {h.location for h in ctx.notify_hints.call_args.args[1]})
        self.assertEqual(1, ctx.hints_used[0, 2])

    def test_admin_option(self):
        ctx = Context("", 0, "", "", 0, 10, 10, False)
        self.assertFalse(ctx.hint_all)
        processor = ServerCommandProcessor(ctx)
        processor.output = Mock()
        self.assertTrue(processor._cmd_option("hint_all", "true"))
        self.assertTrue(ctx.hint_all)
        self.assertTrue(processor._cmd_option("hint_all", "false"))
        self.assertFalse(ctx.hint_all)


    def test_option_survives_save_and_old_saves_keep_default(self):
        ctx = Context("", 0, "", "", 0, 10, 10, False)
        ctx.hint_all = True
        saved = ctx.get_save()
        restored = Context("", 0, "", "", 0, 10, 10, False)
        restored.set_save(saved)
        self.assertTrue(restored.hint_all)
        del saved["game_options"]["hint_all"]
        old_room = Context("", 0, "", "", 0, 10, 10, False)
        old_room.set_save(saved)
        self.assertFalse(old_room.hint_all)


class TestSphereCommandsHideBot(unittest.TestCase):
    def processor(self, slot=7):
        from MultiServer import ClientMessageProcessor
        ctx = SimpleNamespace(
            games={7: "AlchapelaBot", 2: "Test"},
            er_hint_data={7: {70: "Sphere 1"}, 2: {20: "Sphere 1", 21: "Sphere 2"}},
            locations={7: {70: (1, 2, 1)}, 2: {20: (2, 2, 1), 21: (3, 2, 1)}},
            location_checks=defaultdict(set, {(0, 7): {70}, (0, 2): {20}}),
            hints=defaultdict(set), player_name_lookup={"Bot": (0, 7), "Player": (0, 2)},
            player_names={(0, 7): "Bot", (0, 2): "Player"},
            slot_info={7: SimpleNamespace(game="AlchapelaBot"), 2: SimpleNamespace(game="Test")},
            location_names={"AlchapelaBot": {70: "Secret Pack Contents"},
                            "Test": {20: "First Check", 21: "Second Check"}},
        )
        processor = ClientMessageProcessor(ctx, SimpleNamespace(team=0, slot=slot))
        processor.output = Mock()
        processor.output_multiple = Mock()
        return processor

    def test_global_sphere_totals_exclude_bot_even_when_bot_issues_command(self):
        processor = self.processor()
        processor._cmd_spheres()
        self.assertEqual("1/1 Checked Locations in Sphere 1\n0/1 Checked Locations in Sphere 2",
                         processor.output.call_args.args[0])
        self.assertIn(70, processor.ctx.locations[7])

    def test_numbered_sphere_lists_only_real_players(self):
        processor = self.processor()
        processor._cmd_spheres("1")
        self.assertEqual(["1/1 Locations Checked in Sphere 1 by Player"],
                         processor.output_multiple.call_args.args[0])

    def test_explicit_or_default_bot_target_does_not_reveal_checks(self):
        for command, target in (("_cmd_sphere", None), ("_cmd_sphere", "Bot"), ("_cmd_spheres", "Bot")):
            with self.subTest(command=command, target=target):
                processor = self.processor()
                getattr(processor, command)(target)
                processor.output_multiple.assert_not_called()
                self.assertEqual("AlchapelaBot checks are hidden from sphere commands.",
                                 processor.output.call_args.args[0])

    def test_normal_player_missing_locations_are_unchanged(self):
        processor = self.processor(slot=2)
        processor._cmd_sphere()
        self.assertEqual(["Missing: Second Check at Sphere 2"],
                         processor.output_multiple.call_args.args[0])
