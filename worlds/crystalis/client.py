from typing import TYPE_CHECKING, List, Dict, Tuple
from time import time

from NetUtils import ClientStatus, NetworkItem
from Utils import async_start, VersionException, Version, tuplize_version

import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient
from .items import items_data_by_id, items_data
from .regions import regions_data
from .types import CRYSTALIS_BASE_ID, CRYSTALIS_APWORLD_VERSION

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext

LOCATION_FLAGS_ADDR = 0x64A0
ITEM_FLAGS_ADDR = 0x64C0
RECEIVED_INDEX_ADDR = 0x657D
START_OF_CONSUMABLE_INV_ADDR = 0x6440
END_OF_CONSUMABLE_INV_ADDR = 0x6447
GET_ITEM_FLAG_ADDR = 0x6250
MAIN_LOOP_MODE_ADDR = 0x40
GAME_MODE_ADDR = 0x41
CRYSTALIS_ITEM_ID = 0x04
CURRENT_LOCATION_ADDR = 0x6C
HP_ADDR = 0x3C1
SCREEN_LOCK_ADDR = 0x07D7
AP_ROM_LABEL_ADDR = 0x25715
EXPECTED_START: List[bytes] = [bytes([0xD9, 0xD9, 0xD9, 0xD9, 0xD9, 0xD9, 0xD9, 0xD9])]
AP_ROM_LABEL: List[bytes] = [bytes([0x41, 0x52, 0x43, 0x48, 0x49, 0x50, 0x45, 0x4C, 0x41, 0x47, 0x4F])]
ASINA_LOCATION_ID: int = CRYSTALIS_BASE_ID + 57
WHIRLPOOL_LOCATION_ID: int = CRYSTALIS_BASE_ID + 58
ITERATIONS_TO_MATCH: int = 1
GAME_MODE_DEATH: int = 3
GAME_MODE_NORMAL: int = 8
GAME_MODE_DYNA_DEFEATED: int = 0x1E
MAIN_LOOP_GAME: int = 1



class CrystalisClient(BizHawkClient):
    game = "Crystalis"
    system = "NES"
    # intentionally not defining patch_suffix because Archipelago will not be responsible for patching the game
    loc_id_to_addr: Dict[int, Tuple[int, int]] = {}
    unidentified_item_rom_ids: Dict[int, int] = {}
    current_location: int = 0
    asina_hint_collected: bool = False
    iterations_matched: int = 0
    prev_location_flags: bytes = bytes(0)
    pending_death_link: bool = False
    is_dying: bool = False
    last_death_link: float = time()


    def __init__(self):
        super().__init__()
        for region in regions_data.values():
            for location in region.locations:
                byte: int = location.rom_id // 8
                bit: int = location.rom_id % 8
                self.loc_id_to_addr[location.ap_id_offset + CRYSTALIS_BASE_ID] = (byte, bit)

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        from CommonClient import logger
        try:
            rom_start: List[bytes] = (await bizhawk.read(ctx.bizhawk_ctx, [(0x0, 8, "PRG ROM")]))
            if rom_start != EXPECTED_START:
                logger.debug("Expected: " + str(EXPECTED_START))
                logger.debug("Found: " + str(rom_start))
                return False
            ap_label: List[bytes] = \
                (await bizhawk.read(ctx.bizhawk_ctx, [(AP_ROM_LABEL_ADDR, len(AP_ROM_LABEL[0]), "PRG ROM")]))
            if ap_label != AP_ROM_LABEL:
                logger.debug("Expected: " + str(AP_ROM_LABEL))
                logger.debug("Found: " + str(ap_label))
                return False
        except bizhawk.RequestFailedError:
            return False

        ctx.game = self.game
        ctx.items_handling = 0b111
        ctx.want_slot_data = True
        return True

    def on_package(self, ctx: "BizHawkClientContext", cmd: str, args: dict) -> None:
        if cmd == "Connected":
            # slot_data should be set now
            if "version" not in ctx.slot_data:
                err_string = f"Crystalis APWorld version mismatch. Multiworld generated without versioning; " \
                             f"local install using {CRYSTALIS_APWORLD_VERSION.as_simple_string()}"
                raise VersionException(err_string)
            else:
                generator_version: Version = tuplize_version(ctx.slot_data["version"])
                if generator_version.major != CRYSTALIS_APWORLD_VERSION.major:
                    err_string = f"Crystalis APWorld version mismatch. Multiworld generated with " \
                                 f"{ctx.slot_data['version']}; local install using " \
                                 f"{CRYSTALIS_APWORLD_VERSION.as_simple_string()}"
                    raise VersionException(err_string)
            key_item_names: Dict[str, str] = ctx.slot_data["shuffle_data"]["key_item_names"]
            for original_name, new_name in key_item_names.items():
                # want to map the new item's AP ID to the original item's in-game ID.
                self.unidentified_item_rom_ids[items_data[new_name].ap_id_offset + CRYSTALIS_BASE_ID] = \
                    items_data[original_name].rom_id
            async_start(ctx.send_msgs([{"cmd": "Get",
                                  "keys": [f"asina_hint_collected_{ctx.team}_{ctx.slot}"]}]))
            if "death_link" in ctx.slot_data.keys():
                async_start(ctx.update_death_link(ctx.slot_data["death_link"]))
            else:
                async_start(ctx.update_death_link(False))
        elif cmd == "Retrieved":
            if f"asina_hint_collected_{ctx.team}_{ctx.slot}" in args["keys"]:
                self.asina_hint_collected = args["keys"][f"asina_hint_collected_{ctx.team}_{ctx.slot}"]
        elif cmd == "Bounced":
            tags = args.get("tags", [])
            # we can skip checking "DeathLink" in ctx.tags, as otherwise we wouldn't have been sent this
            if "DeathLink" in tags and self.last_death_link != args["data"]["time"]:
                self.pending_death_link = True
                self.last_death_link = max(args["data"]["time"], self.last_death_link)

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        try:
            read_value = await bizhawk.read(ctx.bizhawk_ctx, [(LOCATION_FLAGS_ADDR, 16, "System Bus"),
                                                              (ITEM_FLAGS_ADDR, 16, "System Bus"),
                                                              (RECEIVED_INDEX_ADDR, 2, "System Bus"),
                                                              (GET_ITEM_FLAG_ADDR, 1, "System Bus"),
                                                              (GAME_MODE_ADDR, 1, "System Bus"),
                                                              (MAIN_LOOP_MODE_ADDR, 1, "System Bus"),
                                                              (CURRENT_LOCATION_ADDR, 1, "System Bus"),
                                                              (START_OF_CONSUMABLE_INV_ADDR, 8, "System Bus")])
            if read_value is not None:
                game_mode = read_value[4][0]
                main_loop_mode = read_value[5][0]
                if main_loop_mode == MAIN_LOOP_GAME and game_mode == GAME_MODE_NORMAL:
                    if self.is_dying:
                        # finished this death, reset the variables
                        self.is_dying = False
                        self.pending_death_link = False
                    elif self.pending_death_link:
                        await bizhawk.guarded_write(ctx.bizhawk_ctx,
                                                       [(HP_ADDR, [0], "System Bus")],
                                                       [(MAIN_LOOP_MODE_ADDR, [MAIN_LOOP_GAME], "System Bus")])
                        return # might as well bail now
                    location_flags = read_value[0]
                    if location_flags == self.prev_location_flags:
                        if self.iterations_matched >= ITERATIONS_TO_MATCH:
                            locations_to_send: List[int] = []
                            for location_id in ctx.missing_locations:
                                byte, bit = self.loc_id_to_addr[location_id]
                                if location_flags[byte] & (1 << bit):
                                    locations_to_send.append(location_id)
                                    ctx.locations_checked.add(location_id)

                            if locations_to_send:
                                await ctx.send_msgs([{
                                        "cmd": "LocationChecks",
                                        "locations": list(locations_to_send)
                                    }])
                                return # Bail now to keep this loop short

                            if not self.asina_hint_collected:
                                byte, bit = self.loc_id_to_addr[ASINA_LOCATION_ID]
                                if location_flags[byte] & (1 << bit):
                                    self.asina_hint_collected = True
                                    await ctx.send_msgs([{
                                        "cmd": "LocationScouts",
                                        "locations": [WHIRLPOOL_LOCATION_ID],
                                        "create_as_hint": 2
                                    },
                                    {
                                        "cmd": "Set",
                                        "key": f"asina_hint_collected_{ctx.team}_{ctx.slot}",
                                        "default": True,
                                        "want_reply": False,
                                        "operations": [{"operation": "replace", "value": True}]
                                }])
                        else:
                            self.iterations_matched += 1
                    else:
                        self.iterations_matched = 0
                        self.prev_location_flags = location_flags

                    get_item_flag: bool = read_value[3][0] != 0
                    item_flags: bytes = read_value[1]
                    received_crystalis: bool = item_flags[0] & 16 != 0
                    if not get_item_flag and not received_crystalis and location_flags[0] & 16 != 0:
                        success: bool = await bizhawk.guarded_write(ctx.bizhawk_ctx,
                                                        [(GET_ITEM_FLAG_ADDR, [1, CRYSTALIS_ITEM_ID], "System Bus")],
                                                        [(MAIN_LOOP_MODE_ADDR, [MAIN_LOOP_GAME], "System Bus")])
                        if success:
                            self.received_crystalis = True
                    received_indices: bytes = read_value[2]
                    nonconsumable_index: int = received_indices[0]
                    consumable_index: int = received_indices[1]
                    new_location: int = read_value[6][0]
                    if new_location != self.current_location:
                        self.current_location = new_location
                        async_start(ctx.send_msgs([{
                                    "cmd": "Set",
                                    "key": f"current_location_{ctx.team}_{ctx.slot}",
                                    "default": 0,
                                    "want_reply": False,
                                    "operations": [{"operation": "replace", "value": new_location}]
                                }]), name="send current_location")
                    # if we're not already processing an item and we're not in Mezame Shrine...
                    # Prevent receiving items in Mezame Shrine to make reloading saves for asyncs a bit smoother.
                    if not get_item_flag and self.current_location != 0:
                        if nonconsumable_index + consumable_index < len(ctx.items_received):
                            non_consumables = [item for item in ctx.items_received if
                                               items_data_by_id[item.item].groups != ["Consumable"]]
                            if nonconsumable_index < len(non_consumables):
                                item_to_write: NetworkItem = non_consumables[nonconsumable_index]
                                unique: bool = items_data_by_id[item_to_write.item].unique
                                item_id: int
                                if item_to_write.item in self.unidentified_item_rom_ids.keys():
                                    item_id = self.unidentified_item_rom_ids[item_to_write.item]
                                else:
                                    item_id = items_data_by_id[item_to_write.item].rom_id
                                byte: int = item_id // 8
                                bit: int = item_id % 8
                                item_flag_byte: byte = item_flags[byte] if unique \
                                    else item_flags[byte] & (0xFF ^ (1 << bit))

                                await bizhawk.guarded_write(ctx.bizhawk_ctx,
                                                        [(RECEIVED_INDEX_ADDR, [nonconsumable_index + 1], "System Bus"),
                                                         (GET_ITEM_FLAG_ADDR, [1, item_id], "System Bus"),
                                                         (ITEM_FLAGS_ADDR + byte, [item_flag_byte], "System Bus")],
                                                        [(MAIN_LOOP_MODE_ADDR, [MAIN_LOOP_GAME], "System Bus"),
                                                         (SCREEN_LOCK_ADDR, [0], "System Bus")])
                            else:
                                consumables = [item for item in ctx.items_received if
                                               items_data_by_id[item.item].groups == ["Consumable"]]
                                if consumable_index < len(consumables):
                                    item_to_write: NetworkItem = consumables[consumable_index]
                                    item_id: int = items_data_by_id[item_to_write.item].rom_id
                                    byte: int = item_id // 8
                                    bit: int = item_id % 8
                                    item_flag_byte: byte = item_flags[byte] & (0xFF ^ (1 << bit))
                                    await bizhawk.guarded_write(ctx.bizhawk_ctx,
                                                       [(RECEIVED_INDEX_ADDR + 1, [consumable_index + 1], "System Bus"),
                                                        (GET_ITEM_FLAG_ADDR, [1, item_id], "System Bus"),
                                                        (ITEM_FLAGS_ADDR + byte, [item_flag_byte], "System Bus")],
                                                       [(END_OF_CONSUMABLE_INV_ADDR, [0xFF], "System Bus"),
                                                        (MAIN_LOOP_MODE_ADDR, [MAIN_LOOP_GAME], "System Bus"),
                                                        (SCREEN_LOCK_ADDR, [0], "System Bus")])
                elif game_mode == GAME_MODE_DYNA_DEFEATED and not ctx.finished_game:
                    await ctx.send_msgs([{
                        "cmd": "StatusUpdate",
                        "status": ClientStatus.CLIENT_GOAL
                    }])
                elif game_mode == GAME_MODE_DEATH and main_loop_mode == MAIN_LOOP_GAME:
                    if not self.is_dying and "DeathLink" in ctx.tags:
                        self.is_dying = True
                        # check to see if we should send a death link
                        if not (self.pending_death_link or items_data["Opel Statue"].rom_id in read_value[7]):
                            # this is not a linked death, nor are we being saved by an opel; send a death link
                            async_start(ctx.send_death())
                            self.last_death_link = ctx.last_death_link

        except bizhawk.RequestFailedError:
            # Exit handler and return to main loop to reconnect.
            pass


