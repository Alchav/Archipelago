import os
import pickle
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


class TestOwnerSphereProgress(TestBase):
    def test_progress_is_grouped_by_owner_and_sphere(self) -> None:
        from WebHostLib.tracker import TrackerData

        tracker_data = TrackerData.__new__(TrackerData)
        tracker_data._tracker_cache = {}
        tracker_data._multidata = {
            "owners": {1: 4, 2: 4, 3: 7, 4: 9},
            "spheres": [
                {1: {10, 11}, 2: {20}, 3: {30}},
                {1: {12}, 3: {31, 32}},
            ],
        }
        tracker_data.item_id_to_name = {
            "AlchapelaBot": {
                1004: "Alice Hint Point", 1007: "Bob Hint Point", 1009: "Nobody Hint Point",
            },
        }
        tracker_data.get_all_players = Mock(return_value={0: [1, 2, 3, 4]})
        tracker_data.get_player_locations = Mock(side_effect={
            1: {10: None, 11: None, 12: None},
            2: {20: None},
            3: {30: None, 31: None, 32: None},
            4: {},
        }.get)
        checked_locations = {1: {10, 12}, 2: set(), 3: {30, 32}}
        tracker_data.get_player_checked_locations = Mock(
            side_effect=lambda team, player: checked_locations[player])

        self.assertEqual(tracker_data.get_owner_sphere_progress(), {0: [
            {"owner": "Alice", "progress": [33, 100]},
            {"owner": "Bob", "progress": [100, 50]},
        ]})
