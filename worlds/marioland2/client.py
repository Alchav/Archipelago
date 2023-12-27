import base64
import logging

from NetUtils import ClientStatus
from worlds._bizhawk.client import BizHawkClient, BizHawkClientContext
from worlds._bizhawk import read, write, guarded_write

from .rom_addresses import rom_addresses

logger = logging.getLogger("Client")


class MarioLand2Client(BizHawkClient):
    system = ("GB", "SGB")
    patch_suffix = ".apsml2"
    game = "Super Mario Land 2"

    def __init__(self):
        super().__init__()
        self.locations_array = []

    async def validate_rom(self, ctx):
        game_name = await read(ctx.bizhawk_ctx, [(0x134, 10, "ROM")])
        game_name = game_name[0].decode("ascii")
        if game_name == "MARIOLAND2":
            ctx.game = self.game
            ctx.items_handling = 0b111
            return True
        return False

    async def set_auth(self, ctx):
        auth_name = await read(ctx.bizhawk_ctx, [(0x77777, 21, "ROM")])
        auth_name = base64.b64encode(auth_name[0]).decode()
        ctx.auth = auth_name

    async def game_watcher(self, ctx: BizHawkClientContext):
        from . import locations, items, START_IDS
        game_loaded_check, level_data, music, auto_scroll_enabled, auto_scroll_levels, current_level, midway_point = \
            await read(ctx.bizhawk_ctx, [(0x0046, 10, "CartRAM"), (0x0848, 42, "CartRAM"), (0x0469, 1, "CartRAM"),
                                         (rom_addresses["Auto_Scroll_Disable"], 1, "ROM"),
                                         (rom_addresses["Auto_Scroll_Levels"], 32, "ROM"),
                                         (0x0269, 1, "CartRAM"),
                                         (0x02A0, 1, "CartRAM")])

        if game_loaded_check != b'\x124Vx\xff\xff\xff\xff\xff\xff':
            return

        current_level = int.from_bytes(current_level)
        midway_point = int.from_bytes(midway_point)
        music = int.from_bytes(music)
        auto_scroll_enabled = int.from_bytes(auto_scroll_enabled)

        level_data = list(level_data)

        items_received = [list(items.keys())[item.item - START_IDS] for item in ctx.items_received]

        progressive_coins = {
            "Space Zone Progression": 3,
            "Tree Zone Progression": 4,
            "Macro Zone Progression": 4,
            "Pumpkin Zone Progression": 4,
            "Mario Zone Progression": 4,
            "Turtle Zone Progression": 3
        }
        for level_item, count in progressive_coins.items():
            if items_received.count(level_item) >= count:
                items_received.append(level_item.split(" ")[1] + " Coin")

        locations_checked = []
        modified_level_data = level_data.copy()
        for ID, (location, data) in enumerate(locations.items(), START_IDS):
            if "clear_condition" in data:
                if items_received.count(data["clear_condition"][0]) >= data["clear_condition"][1]:
                    modified_level_data[data["ram_index"]] |= 0x08 if data["type"] == "bell" else 0x80

            if data["type"] == "level" and level_data[data["ram_index"]] & 0x41:
                locations_checked.append(ID)
            elif data["type"] == "bell" and data["id"] == current_level and midway_point == 0xFF:
                locations_checked.append(ID)

        if ctx.slot_data:
            total_stars = ctx.slot_data["stars"]
        else:
            total_stars = 5

        invincibility_length = int((832.0 / (total_stars + 1))
                                   * (items_received.count("Super Star Duration Increase") + 1))

        if "Easy Mode" in items_received:
            difficulty_mode = 1
        elif "Normal Mode" in items_received:
            difficulty_mode = 0
        elif ctx.slot_data:
            difficulty_mode = ctx.slot_data["mode"] & 1
        else:
            difficulty_mode = 0

        data_writes = [
            (rom_addresses["Space_Physics"], [0x7e] if "Space Physics" in items_received else [0xaf], "ROM"),
            (rom_addresses["Get_Hurt_To_Big_Mario"], [1] if "Mushroom" in items_received else [0], "ROM"),
            (rom_addresses["Get_Mushroom_A"], [0xea, 0x16, 0xa2] if "Mushroom" in items_received else [0, 0, 0], "ROM"),
            (rom_addresses["Get_Mushroom_B"], [0xea, 0x16, 0xa2] if "Mushroom" in items_received else [0, 0, 0], "ROM"),
            (rom_addresses["Get_Mushroom_C"], [00] if "Mushroom" in items_received else [0xd8], "ROM"),
            (rom_addresses["Get_Carrot_A"], [0xea, 0x16, 0xa2] if "Carrot" in items_received else [0, 0, 0], "ROM"),
            (rom_addresses["Get_Carrot_B"], [0xea, 0x16, 0xa2] if "Carrot" in items_received else [0, 0, 0], "ROM"),
            (rom_addresses["Get_Carrot_C"], [00] if "Carrot" in items_received else [0xc8], "ROM"),
            (rom_addresses["Get_Fire_Flower_A"], [0xea, 0x16, 0xa2] if "Fire Flower" in items_received else [0, 0, 0], "ROM"),
            (rom_addresses["Get_Fire_Flower_B"], [0xea, 0x16, 0xa2] if "Fire Flower" in items_received else [0, 0, 0], "ROM"),
            (rom_addresses["Get_Fire_Flower_C"], [00] if "Fire Flower" in items_received else [0xc8], "ROM"),
            (rom_addresses["Invincibility_Star_A"], [(invincibility_length >> 8) + 1], "ROM"),
            (rom_addresses["Invincibility_Star_B"], [invincibility_length & 0xFF], "ROM"),
            (rom_addresses["Enable_Bubble"], [0xcb, 0xd7] if "Hippo Bubble" in items_received else [0, 0], "ROM"),
            (rom_addresses["Enable_Swim"], [0xcb, 0xcf] if "Swim" in items_received else [0, 0], "ROM"),
            (0x02E4, [difficulty_mode], "CartRAM"),
            (0x0848, modified_level_data, "CartRAM")
        ]

        if midway_point == 0xFF and ctx.slot_data and ctx.slot_data["midway_bells"]:
            # after registering the check for the midway bell, clear the value just for safety.
            data_writes.append((0x02A0, [0], "CartRAM"))

        if "Auto Scroll" in items_received:
            if auto_scroll_enabled == 0xaf:  # auto scroll has not yet been enabled
                data_writes.append((rom_addresses["Auto_Scroll_Disable"], [0x7e], "ROM"))
                # if the current level is an auto scroll level, turn on auto scrolling now
                if auto_scroll_levels[current_level] == 1:
                    data_writes.append((0x02C8, [0x01], "CartRAM"))

        await guarded_write(ctx.bizhawk_ctx, data_writes, [(0x0848, level_data, "CartRAM")])

        if not ctx.server or not ctx.server.socket.open or ctx.server.socket.closed:
            return

        if locations_checked and locations_checked != self.locations_array:
            self.locations_array = locations_checked
            await ctx.send_msgs([{"cmd": "LocationChecks", "locations": locations_checked}])

        if music == 0x18:
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            ctx.finished_game = True