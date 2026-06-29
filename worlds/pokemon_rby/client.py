import base64
import logging
import time

from NetUtils import ClientStatus
from worlds._bizhawk.client import BizHawkClient
from worlds._bizhawk import read, write, guarded_write

from .locations import (
    Missable,
    build_location_data,
    build_location_name_to_id,
    location_data_blue,
    location_data_red,
    location_data_yellow,
    LocationData
)
from .rom_addresses import (

    wram_addresses_rb,
    wram_addresses_yellow,
)

logger = logging.getLogger("Client")

BANK_EXCHANGE_RATE = 50000000

GAME_NAMES_BY_ROM_HEADER = {
    "POKEMON RED\00\00\00": "Pokemon Red",
    "POKEMON BLUE\00\00": "Pokemon Blue",
    "POKEMON YELLOW": "Pokemon Yellow",
}
SUPPORTED_GAMES = set(GAME_NAMES_BY_ROM_HEADER.values())

DATA_LOCATION_LENGTHS = {
    "ItemIndex": 0x02,
    "Deathlink": 0x01,
    "APItem": 0x01,
    "EventFlag": 0x140,
    "Missable": 0x20,
    "Hidden": 0x0E,
    "Rod": 0x01,
    "DexSanityFlag": 19,
    "GameStatus": 0x01,
    "Money": 3,
    "CurrentMap": 1,
    # First and second Vermilion Gym trash can selection. Second is not used, so should always be 0.
    # First should never be above 0x0F. This is just before Event Flags.
    "CrashCheck1": 2,
    # Unused, should always be 0. This is just before Missables flags.
    "CrashCheck2": 1,
    # Progressive keys, should never be above 10. Just before Dexsanity flags.
    "CrashCheck3": 1,
    # Route 18 Gate script value. Should never be above 3. Just before Hidden items flags.
    "CrashCheck4": 1,
}
RESET_CHECK_LOCATION = (0x0100, 4, "ROM")

TRACKER_EVENT_FLAGS = [
    0x77, # EVENT_BEAT_BROCK
    0xbf, # EVENT_BEAT_MISTY
    0x167, # EVENT_BEAT_LT_SURGE
    0x1a9, # EVENT_BEAT_ERIKA
    0x259, # EVENT_BEAT_KOGA
    0x361, # EVENT_BEAT_SABRINA
    0x299, # EVENT_BEAT_BLAINE
    0x51, # EVENT_BEAT_VIRIDIAN_GYM_GIOVANNI

    0x38, # EVENT_OAK_GOT_PARCEL
    0x525, # EVENT_BEAT_ROUTE22_RIVAL_1ST_BATTLE
    0x117, # EVENT_RESCUED_MR_FUJI
    0x55c, # EVENT_GOT_SS_TICKET
    0x78f, # EVENT_BEAT_SILPH_CO_GIOVANNI
    0x901, # EVENT_BEAT_CHAMPION_RIVAL
]

assert len(TRACKER_EVENT_FLAGS) <= 32

def build_client_location_tables(source_location_data, game):
    location_data, _, _, _ = build_location_data(source_location_data, trainer_data={})
    location_map = {"Rod": {}, "EventFlag": {}, "Missable": {}, "Hidden": {}, "list": {}, "DexSanityFlag": {}}
    location_bytes_bits = {}
    location: LocationData
    for location in location_data:
        if location.ram_address is not None:
            if type(location.ram_address) is list:
                location_map[type(location.ram_address).__name__][
                    (location.ram_address[0].flag[game], location.ram_address[1].flag[game])
                ] = location.address
                location_bytes_bits[location.address] = [
                    {"byte": location.ram_address[0].byte[game], "bit": location.ram_address[0].bit[game]},
                    {"byte": location.ram_address[1].byte[game], "bit": location.ram_address[1].bit[game]},
                ]
            else:
                location_map[type(location.ram_address).__name__][location.ram_address.flag[game]] = location.address
                location_bytes_bits[location.address] = {
                    "byte": location.ram_address.byte[game],
                    "bit": location.ram_address.bit[game],
                }
    return location_map, location_bytes_bits, build_location_name_to_id(location_data)


LOCATION_TABLES = {
    "Pokemon Red": build_client_location_tables(location_data_red, "RB"),
    "Pokemon Blue": build_client_location_tables(location_data_blue, "RB"),
    "Pokemon Yellow": build_client_location_tables(location_data_yellow, "Y"),
}


def build_client_data_locations(wram_addresses):
    data_locations = {
        name: (wram_addresses[name], length, "WRAM")
        for name, length in DATA_LOCATION_LENGTHS.items()
    }
    data_locations["ResetCheck"] = RESET_CHECK_LOCATION
    return data_locations


WRAM_TABLES = {
    "Pokemon Red": build_client_data_locations(wram_addresses_rb),
    "Pokemon Blue": build_client_data_locations(wram_addresses_rb),
    "Pokemon Yellow": build_client_data_locations(wram_addresses_yellow),
}


class PokemonRBYClient(BizHawkClient):
    system = ("GB", "GBC", "SGB")
    patch_suffix = (".apred", ".apblue", ".apyellow")
    game = "Pokemon RBY"

    def __init__(self):
        super().__init__()
        self.auto_hints = set()
        self.locations_array = None
        self.tracker_bitfield = 0
        self.disconnect_pending = False
        self.set_deathlink = False
        self.banking_command = None
        self.game_state = False
        self.last_death_link = 0
        self.current_map = 0
        self.ap_game = None
        self.location_map = {"Rod": {}, "EventFlag": {}, "Missable": {}, "Hidden": {}, "list": {}, "DexSanityFlag": {}}
        self.location_bytes_bits = {}
        self.location_name_to_id = {}
        self.data_locations = {"ResetCheck": RESET_CHECK_LOCATION}

    async def validate_rom(self, ctx):
        game_name = await read(ctx.bizhawk_ctx, [(0x134, 14, "ROM")])
        game_name = game_name[0].decode("ascii")
        ap_game = GAME_NAMES_BY_ROM_HEADER.get(game_name)
        if ap_game:
            ctx.game = ap_game
            ctx.items_handling = 0b001
            ctx.command_processor.commands["bank"] = cmd_bank
            seed_name = await read(ctx.bizhawk_ctx, [(0xFFDB, 21, "ROM")])
            ctx.seed_name = seed_name[0].split(b"\0")[0].decode("ascii")
            self.set_deathlink = False
            self.banking_command = None
            self.locations_array = None
            self.disconnect_pending = False
            self.game_state = False
            self.auto_hints.clear()
            self.tracker_bitfield = 0
            self.current_map = 0
            self.ap_game = ap_game
            self.location_map, self.location_bytes_bits, self.location_name_to_id = LOCATION_TABLES[ap_game]
            self.data_locations = WRAM_TABLES[ap_game]
            return True
        return False

    async def set_auth(self, ctx):
        auth_name = await read(ctx.bizhawk_ctx, [(0xFFC6, 21, "ROM")])
        if auth_name[0] == bytes([0] * 21):
            # rom was patched before rom names implemented, use player name
            auth_name = await read(ctx.bizhawk_ctx, [(0xFFF0, 16, "ROM")])
            auth_name = auth_name[0].decode("ascii").split("\x00")[0]
        else:
            auth_name = base64.b64encode(auth_name[0]).decode()
        ctx.auth = auth_name

    async def game_watcher(self, ctx):
        if not ctx.server or not ctx.server.socket.open or ctx.server.socket.closed:
            return

        data = await read(
            ctx.bizhawk_ctx,
            [(address, length, domain) for address, length, domain in self.data_locations.values()],
        )
        data = {
            data_set_name: data_name
            for data_set_name, data_name in zip(self.data_locations.keys(), data)
        }

        if self.set_deathlink:
            self.set_deathlink = False
            await ctx.update_death_link(True)

        if self.disconnect_pending:
            self.disconnect_pending = False
            await ctx.disconnect()

        if data["GameStatus"][0] == 0 or data["ResetCheck"] == b'\xff\xff\xff\x7f':
            # Do not handle anything before game save is loaded
            self.game_state = False
            return
        elif (data["GameStatus"][0] not in (0x2A, 0xAC)
              or data["CrashCheck1"][0] & 0xF0 or data["CrashCheck1"][1] & 0xFF
              or data["CrashCheck2"][0]
              or data["CrashCheck3"][0] > 10
              or data["CrashCheck4"][0] > 3):
            # Should mean game crashed
            logger.warning("%s may have crashed. Disconnecting from server.", self.ap_game or "Pokemon RBY")
            self.game_state = False
            await ctx.disconnect()
            return
        self.game_state = True

        # SEND ITEMS TO CLIENT

        if data["APItem"][0] == 0:
            item_index = int.from_bytes(data["ItemIndex"], "little")
            if len(ctx.items_received) > item_index:
                item_code = ctx.items_received[item_index].item
                if item_code > 255:
                    item_code -= 256
                await write(ctx.bizhawk_ctx, [(self.data_locations["APItem"][0],
                                               [item_code], self.data_locations["APItem"][2])])

        # LOCATION CHECKS

        locations = set()

        for flag_type, loc_map in self.location_map.items():
            for flag, loc_id in loc_map.items():
                if flag_type == "list":
                    if (data["EventFlag"][self.location_bytes_bits[loc_id][0]["byte"]] & 1 <<
                            self.location_bytes_bits[loc_id][0]["bit"]
                            and data["Missable"][self.location_bytes_bits[loc_id][1]["byte"]] & 1 <<
                            self.location_bytes_bits[loc_id][1]["bit"]):
                        locations.add(loc_id)
                elif data[flag_type][self.location_bytes_bits[loc_id]["byte"]] & 1 << self.location_bytes_bits[loc_id]["bit"]:
                    locations.add(loc_id)

        if locations != self.locations_array:
            if locations:
                self.locations_array = locations
                await ctx.send_msgs([{"cmd": "LocationChecks", "locations": list(locations)}])

        # AUTO HINTS

        hints = []
        if data["EventFlag"][280] & 16:
            hints.append("Cerulean Bicycle Shop")
        if data["EventFlag"][280] & 32:
            hints.append("Route 2 Gate - Oak's Aide")
        if data["EventFlag"][280] & 64:
            hints.append("Route 11 Gate 2F - Oak's Aide")
        if data["EventFlag"][280] & 128:
            hints.append("Route 15 Gate 2F - Oak's Aide")
        if data["EventFlag"][281] & 1:
            hints += ["Celadon Prize Corner - Item Prize 1", "Celadon Prize Corner - Item Prize 2",
                      "Celadon Prize Corner - Item Prize 3"]
        fossil_choice_a = self.location_name_to_id.get("Fossil - Choice A")
        fossil_choice_b = self.location_name_to_id.get("Fossil - Choice B")
        if fossil_choice_a in ctx.checked_locations and fossil_choice_b not in ctx.checked_locations:
            hints.append("Fossil - Choice B")
        elif fossil_choice_b in ctx.checked_locations and fossil_choice_a not in ctx.checked_locations:
            hints.append("Fossil - Choice A")
        hints = [
            loc_id for loc in hints
            if (loc_id := self.location_name_to_id.get(loc)) is not None
            and loc_id not in self.auto_hints
            and loc_id in ctx.missing_locations
            and loc_id not in ctx.locations_checked
        ]
        if hints:
            await ctx.send_msgs([{"cmd": "LocationScouts", "locations": hints, "create_as_hint": 2}])
        self.auto_hints.update(hints)

        # DEATHLINK

        if "DeathLink" in ctx.tags:
            if data["Deathlink"][0] == 3:
                await ctx.send_death(ctx.player_names[ctx.slot] + " is out of usable Pokémon! "
                                     + ctx.player_names[ctx.slot] + " blacked out!")
                await write(ctx.bizhawk_ctx, [(self.data_locations["Deathlink"][0], [0], self.data_locations["Deathlink"][2])])
                self.last_death_link = ctx.last_death_link
            elif ctx.last_death_link > self.last_death_link:
                self.last_death_link = ctx.last_death_link
                await write(ctx.bizhawk_ctx, [(self.data_locations["Deathlink"][0], [1], self.data_locations["Deathlink"][2])])

        # BANK

        if self.banking_command:
            original_money = data["Money"]
            # Money is stored as binary-coded decimal.
            money = int(original_money.hex())
            if self.banking_command > money:
                logger.warning(f"You do not have ${self.banking_command} to deposit!")
            elif (-self.banking_command * BANK_EXCHANGE_RATE) > (ctx.stored_data[f"EnergyLink{ctx.team}"] or 0):
                logger.warning("Not enough money in the EnergyLink storage!")
            else:
                if self.banking_command + money > 999999:
                    self.banking_command = 999999 - money
                money = str(money - self.banking_command).zfill(6)
                money = [int(money[:2], 16), int(money[2:4], 16), int(money[4:], 16)]
                money_address, _, money_domain = self.data_locations["Money"]
                money_written = await guarded_write(
                    ctx.bizhawk_ctx,
                    [(money_address, money, money_domain)],
                    [(money_address, original_money, money_domain)],
                )
                if money_written:
                    if self.banking_command >= 0:
                        deposit = self.banking_command - int(self.banking_command / 4)
                        tax = self.banking_command - deposit
                        logger.info(f"Deposited ${deposit}, and charged a tax of ${tax}.")
                        self.banking_command = deposit
                    else:
                        logger.info(f"Withdrew ${-self.banking_command}.")
                    await ctx.send_msgs([{
                        "cmd": "Set", "key": f"EnergyLink{ctx.team}", "operations":
                            [{"operation": "add", "value": self.banking_command * BANK_EXCHANGE_RATE},
                             {"operation": "max", "value": 0}],
                    }])
            self.banking_command = None

        if data["CurrentMap"][0] != self.current_map:
            await ctx.send_msgs([{"cmd": "Bounce", "slots": [ctx.slot], "data": {"currentMap": data["CurrentMap"][0]}}])
            self.current_map = data["CurrentMap"][0]

        # TRACKER
        tracker_bitfield = 0
        for i, flag in enumerate(TRACKER_EVENT_FLAGS):
            if data["EventFlag"][flag // 8] & (1 << (flag % 8)):
                tracker_bitfield |= 1 << i

        if tracker_bitfield != self.tracker_bitfield:
            await ctx.send_msgs([{
                "cmd": "Set",
                "key": f"pokemon_rb_events_{ctx.team}_{ctx.slot}",
                "default": 0,
                "want_reply": False,
                "operations": [{"operation": "or", "value": tracker_bitfield}],
            }])
            self.tracker_bitfield = tracker_bitfield

        # VICTORY

        if data["EventFlag"][280] & 1 and not ctx.finished_game:
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            ctx.finished_game = True

    def on_package(self, ctx, cmd, args):
        if cmd == 'Connected':
            if 'death_link' in args['slot_data'] and args['slot_data']['death_link']:
                self.set_deathlink = True
                self.last_death_link = time.time()
            ctx.set_notify(f"EnergyLink{ctx.team}")
        elif cmd == 'RoomInfo':
            if ctx.seed_name and ctx.seed_name != args["seed_name"]:
                # CommonClient's on_package displays an error to the user in this case, but connection is not cancelled.
                self.game_state = False
                self.disconnect_pending = True
        super().on_package(ctx, cmd, args)


def cmd_bank(self, cmd: str = "", amount: str = ""):
    """Deposit or withdraw money with the server's EnergyLink storage.
    /bank - check server balance.
    /bank deposit # - deposit money. One quarter of the amount will be lost to taxation.
    /bank withdraw # - withdraw money."""
    if self.ctx.game not in SUPPORTED_GAMES:
        logger.warning("This command can only be used while playing Pokemon Red, Blue, or Yellow")
        return
    if (not self.ctx.server) or self.ctx.server.socket.closed or not self.ctx.client_handler.game_state:
        logger.info(f"Must be connected to server and in game.")
        return
    elif not cmd:
        logger.info(f"Money available: {int((self.ctx.stored_data[f'EnergyLink{self.ctx.team}'] or 0) / BANK_EXCHANGE_RATE)}")
        return
    elif not amount:
        logger.warning("You must specify an amount.")
    elif cmd == "withdraw":
        self.ctx.client_handler.banking_command = -int(amount)
    elif cmd == "deposit":
        if int(amount) < 4:
            logger.warning("You must deposit at least $4, for tax purposes.")
            return
        self.ctx.client_handler.banking_command = int(amount)
    else:
        logger.warning(f"Invalid bank command {cmd}")
        return
