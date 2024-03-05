from typing import TYPE_CHECKING, Dict, Set
import time
import logging
import sys

from .options import FinalMission, JobUnlockReq


from NetUtils import ClientStatus
import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient
from .items import AbilityItems
from .locations import (MissionGroups, DispatchMissionGroups, bitflags)
from worlds.LauncherComponents import SuffixIdentifier, components

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext
else:
    BizHawkClientContext = object

for component in components:
    if component.script_name == "BizHawkClient":
        component.file_identifier = SuffixIdentifier(*(*component.file_identifier.suffixes, ".apffta"))
        break


class FFTAClient(BizHawkClient):
    game = "Final Fantasy Tactics Advance"
    system = "GBA"
    local_checked_locations: Set[int]
    local_set_events: Dict[str, bool]
    pending_death_link: bool = False
    sending_death_link: bool = False
    death_link: bool = False
    job_unlock: bool = False
    goal_flag: int
    goal_id: int = 0

    def __init__(self) -> None:
        super().__init__()
        self.local_checked_locations = set()
        self.local_set_events = {}

    async def validate_rom(self, ctx: BizHawkClientContext) -> bool:

        try:
            game_name = ((await bizhawk.read(ctx.bizhawk_ctx, [(0x0A0, 10, "ROM")]))[0]).decode("ascii")
            print('Game name for validate rom ' + game_name)
            if game_name != "FFTA_USVER":
                return False
        except UnicodeDecodeError:
            return False
        except bizhawk.RequestFailedError:
            return False  # Should verify on the next pass

        ctx.game = self.game
        print('context is registered for FFTA')
        print(ctx.game)
        ctx.items_handling = 0b001
        ctx.want_slot_data = True
        return True

    """"
    def on_package(self, ctx: BizHawkClientContext, cmd: str, args: dict) -> None:
        if cmd == "Bounced":
            if "tags" in args:
                if "DeathLink" in args["tags"] and args["data"]["source"] != ctx.slot_info[ctx.slot].name:
                    self.on_deathlink(ctx)
    
    async def send_deathlink(self, ctx: BizHawkClientContext):
        self.sending_death_link = True
        ctx.last_death_link = time.time()
        await ctx.send_death("Someone in Ivalice has fallen.")

    def on_deathlink(self, ctx: BizHawkClientContext):
        ctx.last_death_link = time.time()
        self.pending_death_link = True
    
    async def set_auth(self, ctx: "BizHawkClientContext") -> None:
        slot_name_bytes = (await bizhawk.read(ctx.bizhawk_ctx, [(0xAAABD0, 64, "ROM")]))[0]
        ctx.auth = bytes([byte for byte in slot_name_bytes if byte != 0]).decode("utf-8")
    """
        
    async def game_watcher(self, ctx: BizHawkClientContext) -> None:
        if ctx.slot_data is not None:
            if ctx.slot_data["final_mission"] == FinalMission.option_royal_valley:
                self.goal_id = 0x64

            elif ctx.slot_data["final_mission"] == FinalMission.option_decision_time:
                self.goal_id = 0x93

            """
            if "job_unlock_req" in ctx.slot_data:
                if ctx.slot_data["job_unlock_req"] == JobUnlockReq.option_job_items:
                    self.job_unlock = True
                    
            """

            #if ctx.slot_data["job_unlock_req"] == JobUnlockReq.option_job_items:
            #    self.job_unlock = True

        try:
            offset = 41234532
            flag_list = [(0x2001FD0, 50, "System Bus"), (0x2001FD1, 1, "System Bus"),
                         (0x2000110, 2, "System Bus"), (0x200FA18, 2, "System Bus"),
                         (0x2002B08, 0xFC, "System Bus"), (0x2002192, 1, "System Bus"),
                         (0x2000098, 1, "System Bus")]
            read_result = await bizhawk.read(ctx.bizhawk_ctx, flag_list)
            flag_bytes = read_result[0]
            received_items = int.from_bytes(read_result[2], "little")
            mission_items = read_result[4]

            # Remove the archipelago and job unlock mission items
            for byte_i, item in enumerate(mission_items):
                if item == 0x0E or item == 0x45:
                    await bizhawk.write(ctx.bizhawk_ctx, [(0x2002B08 + byte_i, bytes([0x00]), "System Bus")])

            self.goal_flag = read_result[5]

            local_checked_locations = set()
            game_clear = False

            """
            unit_ram = await bizhawk.read(ctx.bizhawk_ctx, [(0x20001a0, 1, "System Bus")])
            #Deathlink
            if ctx.slot_data["death_link"]:
                if not self.death_link:
                    self.death_link = True
                    await ctx.update_death_link(self.death_link)
            if self.pending_death_link:
                await bizhawk.write(ctx.bizhawk_ctx, [(0x200016A, [0x10], "System Bus"), (0x2000159, [0x01], "System Bus"), (0x2000155, [0x20], "System Bus")])
                self.pending_death_link = False
                self.sending_death_link = True
            if "DeathLink" in ctx.tags and ctx.last_death_link + 1 < time.time():
                if unit_ram[0] == 0x00 and not self.sending_death_link:
                    await self.send_deathlink(ctx)
                elif unit_ram[0] != 0x00:
                    self.sending_death_link = False
            """
         
            # Check if goal status is reached
            if self.goal_flag[0] == self.goal_id and self.goal_id != 0:
                game_clear = True

            # Check set flags
            for byte_i, byte in enumerate(flag_bytes):

                for i in range(8):

                    if byte & (1 << i) == bitflags[i]:

                        for mission in MissionGroups:
                            if byte & (1 << i) == mission[2] and byte_i == mission[3]:
                                location_id = mission[0].rom_address
                                if location_id in ctx.server_locations:
                                    local_checked_locations.add(location_id)
                                    # Send location scouts for local job unlock items
                                    if self.job_unlock:
                                        await ctx.send_msgs([{
                                            "cmd": "LocationScouts",
                                            "locations": [location_id]
                                        }])

                                    # Make the mission not repeatable after completing it
                                    #await bizhawk.write(ctx.bizhawk_ctx, [(location_id + 0x1f, [0xC0], "System Bus")])

                                location_id2 = mission[1].rom_address
                                if location_id2 in ctx.server_locations:
                                    local_checked_locations.add(location_id2)

                                    if self.job_unlock:
                                        await ctx.send_msgs([{
                                            "cmd": "LocationScouts",
                                            "locations": [location_id2]
                                        }])

                        for mission in DispatchMissionGroups:
                            if byte & (1 << i) == mission[2] and byte_i == mission[3]:
                                location_id = mission[0].rom_address
                                if location_id in ctx.server_locations:
                                    local_checked_locations.add(location_id)
                                    # Send location scouts for local job unlock items
                                    if self.job_unlock:
                                        await ctx.send_msgs([{
                                            "cmd": "LocationScouts",
                                            "locations": [location_id]
                                        }])

                                location_id2 = mission[1].rom_address
                                if location_id2 in ctx.server_locations:
                                    local_checked_locations.add(location_id2)

                                    if self.job_unlock:
                                        await ctx.send_msgs([{
                                            "cmd": "LocationScouts",
                                            "locations": [location_id2]
                                        }])




            #roulette = 0x12D
            #Roulette trap
            #await bizhawk_write(ctx, [(0x200f58e, roulette.to_bytes(2, "little"), "System Bus")])

            #Death link

            #current_hp = read_result[6]

            #Send death link on game over maybe? every unit dying would be a lot.
            #while int.from_bytes(current_hp, "little") > 0:
                #Marche
                #await bizhawk_write(ctx, [(0x2000159, [0x01], "System Bus"),
                #                          (0x200016A, [0x10], "System Bus"),
                #                          (0x2000155, [0x01], "System Bus")])

                #Montblanc/second unit?
                #await bizhawk_write(ctx, [(0x2000261, [0x01], "System Bus"),
                #                          (0x2000272, [0x10], "System Bus"),
               #                           (0x200025d, [0x01], "System Bus")])


            # Send locations
            if local_checked_locations != self.local_checked_locations:
                self.local_checked_locations = local_checked_locations

                if local_checked_locations is not None:
                    await ctx.send_msgs([{
                        "cmd": "LocationChecks",
                        "locations": list(local_checked_locations)
                    }])

            if not ctx.finished_game and game_clear:
                await ctx.send_msgs([{
                    "cmd": "StatusUpdate",
                    "status": ClientStatus.CLIENT_GOAL
                }])

            guard_list = [(0x200f85c, [0x00], "System Bus"), (0x2019EB9, [0x01], "System Bus")]

            # Check local locations for job unlock items then unlock that job, find a better way to do this later

            if self.job_unlock:
                if len(ctx.locations_info) > 0:
                    # Copy dict to avoid resizing issues during iteration
                    for location in ctx.locations_info.copy():
                        scouted_location = ctx.locations_info[location]
                        if scouted_location.item - 41234532 >= 0x2ac:
                            print(hex(scouted_location.item))
                            await bizhawk.write(ctx.bizhawk_ctx, [
                                (scouted_location.item - 41234532 + 0x8521800, [0x00], "System Bus")])

            job_unlock_item = 0x1bc

            if received_items < len(ctx.items_received):
                next_item = ctx.items_received[received_items]

                not_moving = int.from_bytes(read_result[3], "little") != 0

                # Make sure Marche isn't moving on the world map when receiving an item
                if not_moving:

                    # Checking if next item is a job unlock item
                    if next_item.item - 41234532 >= 0x2ac:
                        await bizhawk.guarded_write(ctx.bizhawk_ctx,
                                                    [(next_item.item - 41234532 + 0x8521800, [0x00], "System Bus"),
                                                     (0x2002c10, [0x00], "System Bus"),
                                                     (0x200fd2b, [0x00], "System Bus"),
                                                     (0x201f46c, job_unlock_item.to_bytes(2, "little"), "System Bus"),
                                                     (0x201f46e, [0x00], "System Bus"),
                                                     (0x2000110, (received_items + 1).to_bytes(2, "little"),
                                                      "System Bus"),
                                                     (0x200f85c, [0x06], "System Bus")], guard_list)

                    #Make case for trap items received
                    #elif next_item.item - 41234532 == 0x11111:

                    elif len(ctx.items_received) - received_items > 1:
                        item_after = ctx.items_received[received_items + 1]

                        if item_after.item - 41234532 >= 0x2ac:
                            await bizhawk.guarded_write(ctx.bizhawk_ctx,
                            [(item_after.item - 41234532 + 0x8521800, [0x00], "System Bus"),
                             (0x2002c10, [0x00], "System Bus"),
                             (0x200fd2b, [0x00], "System Bus"),
                             (0x201f46c, (next_item.item - 41234532).to_bytes(2, "little"),
                              "System Bus"),
                             (0x201f46e, job_unlock_item.to_bytes(2, "little"),
                              "System Bus"),
                             (0x2000110, (received_items + 2).to_bytes(2, "little"),
                              "System Bus"),
                             (0x200f85c, [0x06], "System Bus")], guard_list)

                        else:
                            await bizhawk.guarded_write(ctx.bizhawk_ctx,
                             [(0x2002c10, [0x00], "System Bus"),
                             (0x200fd2b, [0x00], "System Bus"),
                             (0x201f46c, (next_item.item - 41234532).to_bytes(2, "little"),
                              "System Bus"),
                             (0x201f46e, (item_after.item - 41234532).to_bytes(2, "little"),
                              "System Bus"),
                             (0x2000110, (received_items + 2).to_bytes(2, "little"),
                              "System Bus"),
                             (0x200f85c, [0x06], "System Bus")], guard_list)

                    else:
                        await bizhawk.guarded_write(ctx.bizhawk_ctx,
                                                   [(0x2002c10, [0x00], "System Bus"), (0x200fd2b, [0x00], "System Bus"),
                                                    (0x201f46c, (next_item.item - 41234532).to_bytes(2, "little"), "System Bus"),
                                                    (0x201f46e, (0x0000).to_bytes(2, "little"), "System Bus"),
                                                    (0x2000110, (received_items + 1).to_bytes(2, "little"), "System Bus"),
                                                    (0x200f85c, [0x06], "System Bus")], guard_list)

        except bizhawk.RequestFailedError:
            # Exit handler and return to main loop to reconnect
            pass
