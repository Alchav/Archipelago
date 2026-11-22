import os
import pickle
import unittest
from pathlib import Path
from typing import ClassVar
from unittest.mock import Mock
from uuid import UUID, uuid4

from flask import url_for

from . import TestBase


class TestTracker(TestBase):
    room_id: UUID
    tracker_uuid: UUID
    log_filename: str
    data: ClassVar[bytes]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        with (Path(__file__).parent / "data" / "One_Archipelago.archipelago").open("rb") as f:
            cls.data = f.read()

    def setUp(self) -> None:
        from pony.orm import db_session
        from MultiServer import Context as MultiServerContext
        from Utils import user_path
        from WebHostLib.models import GameDataPackage, Room, Seed

        super().setUp()

        multidata = MultiServerContext.decompress(self.data)

        with self.client.session_transaction() as session:
            session["_id"] = uuid4()
            self.tracker_uuid = uuid4()
            with db_session:
                # store game datapackage(s)
                for game, game_data in multidata["datapackage"].items():
                    if not GameDataPackage.get(checksum=game_data["checksum"]):
                        GameDataPackage(checksum=game_data["checksum"],
                                        data=pickle.dumps(game_data))
                # create an empty seed and a room from it
                seed = Seed(multidata=self.data, owner=session["_id"])
                room = Room(seed=seed, owner=session["_id"], tracker=self.tracker_uuid)
                self.room_id = room.id
                self.log_filename = user_path("logs", f"{self.room_id}.txt")

    def tearDown(self) -> None:
        from pony.orm import db_session, select
        from WebHostLib.models import Command, Room

        with db_session:
            for command in select(command for command in Command if command.room.id == self.room_id):  # type: ignore
                command.delete()
            room: Room = Room.get(id=self.room_id)
            room.seed.delete()
            room.delete()

        try:
            os.unlink(self.log_filename)
        except FileNotFoundError:
            pass

    def test_valid_if_modified_since(self) -> None:
        """
        Verify that we get a 200 response for valid If-Modified-Since
        """
        with self.app.app_context(), self.app.test_request_context():
            response = self.client.get(
                url_for(
                    "get_player_tracker",
                    tracker=self.tracker_uuid,
                    tracked_team=0,
                    tracked_player=1,
                ),
                headers={"If-Modified-Since": "Wed, 21 Oct 2015 07:28:00 GMT"},
            )
            self.assertEqual(response.status_code, 200)

    def test_invalid_if_modified_since(self) -> None:
        """
        Verify that we get a 400 response for invalid If-Modified-Since
        """
        with self.app.app_context(), self.app.test_request_context():
            response = self.client.get(
                url_for(
                    "get_player_tracker",
                    tracker=self.tracker_uuid,
                    tracked_team=1,
                    tracked_player=0,
                ),
                headers={"If-Modified-Since": "Wed, 21 Oct 2015 07:28:00"},  # missing timezone
            )
            self.assertEqual(response.status_code, 400)

    def test_tracker_api(self) -> None:
        """Verify that tracker api gives a reply for the room."""
        with self.app.test_request_context():
            with self.client.open(url_for("api.tracker_data", tracker=self.tracker_uuid)) as response:
                self.assertEqual(response.status_code, 200)
            with self.client.open(url_for("api.static_tracker_data", tracker=self.tracker_uuid)) as response:
                self.assertEqual(response.status_code, 200)
            with self.client.open(url_for("api.tracker_slot_data", tracker=self.tracker_uuid)) as response:
                self.assertEqual(response.status_code, 200)

    def test_logic_api_old_seed_is_unknown(self) -> None:
        with self.app.test_request_context():
            response = self.client.get(url_for("api.tracker_logic", tracker=self.tracker_uuid, team=0))
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertFalse(data["available"])
        for player in data["players"]:
            self.assertTrue(all(loc["in_logic"] is None for loc in player["locations"]))

    def test_logic_api_and_location_page_with_server_results(self) -> None:
        import zlib
        from pony.orm import db_session
        from MultiServer import Context
        from WebHostLib.models import Room
        from ServerLogic import inventory_digest

        with db_session:
            room = Room.get(id=self.room_id)
            data = Context.decompress(room.seed.multidata)
            player = next(iter(data["locations"]))
            from NetUtils import NetworkSlot, SlotType
            data['slot_info'][player] = NetworkSlot('Tester', 'Archipelago', SlotType.player)
            addresses = [100, 101]
            data['locations'][player] = {address: (1, player, 0) for address in addresses}
            data['logic_replay'] = {'version': 1}
            result = {'status': 'ready', 'input_digest': inventory_digest({player: []}, {player: set()}),
                      'locations': {player: {addresses[0]: True, addresses[1]: False}}, 'diagnostics': []}
            room.multisave = pickle.dumps({'logic_results': {0: result}})
            room.seed.multidata = b'\x03' + zlib.compress(pickle.dumps(data))
            room.last_activity = room.last_activity.replace(microsecond=100000)
        with self.app.test_request_context():
            response = self.client.get(url_for("api.tracker_logic", tracker=self.tracker_uuid, team=0))
            self.assertEqual(response.status_code, 200)
            statuses = next(p for p in response.get_json()['players'] if p['player'] == player)['locations']
            self.assertTrue(statuses[0]['in_logic'])
            self.assertTrue(all(loc['in_logic'] is False for loc in statuses[1:]))
            page = self.client.get(url_for('get_generic_game_tracker', tracker=self.tracker_uuid,
                                          tracked_team=0, tracked_player=player))
        self.assertEqual(page.status_code, 200)
        self.assertIn(b'In logic', page.data)
        self.assertIn(b'Out of logic', page.data)
        self.assertNotIn(b'"arguments"', response.data)

        # A save can arrive while its replacement logic is still being evaluated.
        # Keep the known values visible, and invalidate both page/API caches even
        # when the next save has the same whole-second Last-Modified timestamp.
        with db_session:
            room = Room.get(id=self.room_id)
            room.multisave = pickle.dumps({'logic_results': {0: result},
                                          'location_checks': {(0, player): {100}}})
            room.last_activity = room.last_activity.replace(microsecond=200000)
        with self.app.test_request_context():
            updating = self.client.get(url_for('api.tracker_logic', tracker=self.tracker_uuid, team=0)).get_json()
            self.assertEqual(updating['status'], 'updating')
            self.assertTrue(updating['available'])
            self.assertTrue(all(loc['in_logic'] is not None for p in updating['players'] for loc in p['locations']))
            updated_page = self.client.get(
                url_for('get_generic_game_tracker', tracker=self.tracker_uuid, tracked_team=0, tracked_player=player),
                headers={'If-None-Match': page.headers['ETag'],
                         'If-Modified-Since': page.headers['Last-Modified']})
            self.assertEqual(updated_page.status_code, 200)
            self.assertIn(b'data-logic-updating="1"', updated_page.data)
            self.assertIn(b'last verified', updated_page.data)
            self.assertNotEqual(page.headers['ETag'], updated_page.headers['ETag'])

        result = {**result, 'input_digest': inventory_digest({player: []}, {player: {100}}),
                  'locations': {player: {100: True, 101: True}}}
        with db_session:
            room = Room.get(id=self.room_id)
            room.multisave = pickle.dumps({'logic_results': {0: result},
                                          'location_checks': {(0, player): {100}}})
            room.last_activity = room.last_activity.replace(microsecond=300000)
        with self.app.test_request_context():
            ready = self.client.get(url_for('api.tracker_logic', tracker=self.tracker_uuid, team=0)).get_json()
            self.assertEqual(ready['status'], 'ready')
            self.assertTrue(all(loc['in_logic'] for p in ready['players'] for loc in p['locations']))


class TestOwnerSphereProgress(TestBase):
    def make_tracker_data(self):
        from WebHostLib.tracker import TrackerData

        tracker_data = TrackerData.__new__(TrackerData)
        tracker_data._tracker_cache = {}
        tracker_data._multidata = {
            "owners": {1: 4, 2: 4, 3: 7, 4: 8},
            "spheres": [
                {1: {10, 11}, 2: {20}, 3: {30}, 4: {40}},
                {1: {12}, 3: {31, 32}},
            ],
        }
        tracker_data.item_id_to_name = {
            "AlchapelaBot": {
                1004: "Alice Hint Point", 1007: "Bob Hint Point", 1008: "Auto Hint Point",
            },
        }
        tracker_data.get_all_players = Mock(return_value={0: [1, 2, 3, 4]})
        tracker_data.get_player_locations = Mock(side_effect={
            1: {10: None, 11: None, 12: None},
            2: {20: None},
            3: {30: None, 31: None, 32: None},
            4: {40: None},
        }.get)
        checked_locations = {1: {10, 12}, 2: set(), 3: {30, 32}}
        tracker_data.get_player_checked_locations = Mock(
            side_effect=lambda team, player: checked_locations[player])
        return tracker_data

    def test_progress_is_grouped_by_owner_and_sphere(self) -> None:
        tracker_data = self.make_tracker_data()
        self.assertEqual(tracker_data.get_owner_sphere_progress(), {0: [
            {"owner": "Alice", "progress": [33, 100], "cumulative_progress": [33, 50]},
            {"owner": "Bob", "progress": [100, 50], "cumulative_progress": [100, 67]},
        ]})

    def test_cumulative_progress_carries_across_empty_spheres(self) -> None:
        tracker_data = self.make_tracker_data()
        tracker_data._multidata["spheres"] = [{}, *tracker_data._multidata["spheres"], {}]
        self.assertEqual(tracker_data.get_owner_sphere_progress(), {0: [
            {"owner": "Alice", "progress": [None, 33, 100, None],
             "cumulative_progress": [None, 33, 50, 50]},
            {"owner": "Bob", "progress": [None, 100, 50, None],
             "cumulative_progress": [None, 100, 67, 67]},
        ]})

    def test_sphere_table_includes_switch_and_both_percentages(self) -> None:
        from flask import render_template

        tracker_data = self.make_tracker_data()
        with self.app.app_context():
            html = render_template("multitrackerSphereProgressTable.html", sphere_count=2,
                                   sphere_progress=tracker_data.get_owner_sphere_progress())
        self.assertEqual(1, html.count('id="sphere-cumulative"'))
        self.assertIn('role="switch"', html)
        self.assertIn('data-sphere-progress="100"\n                                data-sphere-cumulative="50"',
                      html)
        self.assertNotIn("Auto", html)


class TestLogicFreshness(unittest.TestCase):
    def test_slot_status_precedence_and_connection_independence(self):
        from NetUtils import ClientStatus
        for client_status, unlocked, go_mode, expected in (
                (0, False, False, 'Locked'), (20, False, True, 'Locked'),
                (0, True, False, 'Active'), (5, True, False, 'Active'),
                (10, True, False, 'Active'), (20, True, False, 'Active'),
                (0, True, True, 'Go Mode'), (20, True, True, 'Go Mode'),
                (ClientStatus.CLIENT_GOAL, True, True, 'Goal Completed'),
                (ClientStatus.CLIENT_GOAL, False, False, 'Goal Completed')):
            with self.subTest(expected=expected, client_status=client_status):
                data = self.make_data()
                data.get_room_game_unlocks = Mock(return_value={(0, 1): unlocked})
                data._multisave['client_game_state'] = {(0, 1): client_status}
                data._multisave['logic_results'][0]['completion'] = {1: go_mode}
                self.assertEqual(data.get_player_slot_status(0, 1), expected)

    def test_pending_completion_keeps_verified_go_mode(self):
        data = self.make_data()
        data.get_room_game_unlocks = Mock(return_value={(0, 1): True})
        data._multisave['logic_results'][0]['completion'] = {1: True}
        data._multisave['location_checks'] = {(0, 1): {999}}
        self.assertEqual(data.get_player_slot_status(0, 1), 'Go Mode')
        self.assertEqual(data.get_team_logic(0)['status'], 'updating')

    def make_data(self):
        from WebHostLib.tracker import TrackerData
        from ServerLogic import inventory_digest
        data = TrackerData.__new__(TrackerData)
        data._tracker_cache = {}
        data._multidata = {'logic_replay': {'version': 1}, 'slot_info': {1: None}}
        data._multisave = {'logic_results': {0: {
            'status': 'ready', 'input_digest': inventory_digest({1: []}, {1: set()}),
            'locations': {1: {100: False}}, 'diagnostics': [],
        }}}
        return data

    def test_current_server_results_are_used(self):
        self.assertIs(self.make_data().get_location_logic(0, 1, 100), False)

    def test_new_received_items_keep_verified_results_while_updating(self):
        from NetUtils import NetworkItem
        data = self.make_data()
        data._multisave['received_items'] = {(0, 1, True): [NetworkItem(123, 456, 1, 1)]}
        self.assertIs(data.get_location_logic(0, 1, 100), False)
        self.assertEqual(data.get_team_logic(0)['status'], 'updating')
        self.assertIn('last verified', data.get_team_logic(0)['diagnostics'][0])

    def test_new_checked_locations_keep_verified_results_while_updating(self):
        data = self.make_data()
        data._multisave['location_checks'] = {(0, 1): {999}}
        self.assertIs(data.get_location_logic(0, 1, 100), False)
        self.assertEqual(data.get_team_logic(0)['status'], 'updating')

    def test_no_verified_result_remains_unknown(self):
        data = self.make_data()
        data._multisave['logic_results'] = {}
        self.assertIsNone(data.get_location_logic(0, 1, 100))
        self.assertEqual(data.get_team_logic(0)['status'], 'building')
