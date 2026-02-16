import base64
import logging
import time
import random

from NetUtils import ClientStatus
from worlds._bizhawk.client import BizHawkClient
from worlds._bizhawk import read, write, guarded_write

from .patch import PATCH
from .items import items

logger = logging.getLogger("Client")

DATA_LOCATIONS = {
    "mode": (0xffe1, 1),
    "level": (0xffa9, 1),
    "lines": (0xff9e, 2),
    "score": (0xc0a0, 3),
    "patched": (0x014C, 1),
    "demo": (0xffe4, 1),
    "active_garbage_lines": (0xFFD3, 1)
}


class TetrisClient(BizHawkClient):
    system = ("GB", "SGB")
    game = "Tetris"

    def __init__(self):
        self.patched = None
        self.garbage_lines_given = None
        self.garbage_hole_shuffles_given = 0
        super().__init__()

    async def validate_rom(self, ctx):
        game_name = await read(ctx.bizhawk_ctx, [(0x134, 12, "ROM")])
        if game_name[0] == b"TETRIS\00\00\00\00\00\00":
            ctx.game = self.game
            ctx.items_handling = 0b111
            ctx.want_slot_data = True
            self.patched = None

            return True
        return False

    async def game_watcher(self, ctx):
        if not ctx.slot_data:
            return
        data = await read(ctx.bizhawk_ctx, [(loc_data[0], loc_data[1], "System Bus")
                                            for loc_data in DATA_LOCATIONS.values()])
        data = {data_set_name: data_name for data_set_name, data_name in zip(DATA_LOCATIONS.keys(), data)}

        score = int(data["score"][::-1].hex())

        items_received = [list(items.keys())[item.item - 1] for item in ctx.items_received]
        if data["patched"][0] == 172:
            if ctx.auth:
                data_writes = []
                if data["mode"][0] == 0 and not data["demo"][0]:

                    await ctx.send_msgs([{"cmd": "LocationChecks", "locations": list(range(1, int(score / 100) + 1))}])

                    data_writes += [
                        (0xc0de, [0x01] if "Hide Next Piece" in items_received else [0x00], "System Bus"),
                        (0xc210, [0x80] if "Hide Next Piece" in items_received else [0x00], "System Bus"),
                        (0x1fc6, [items_received.count("Score Multiplier")], "ROM"),
                        (0x1afb, [ctx.slot_data["starting_speed"] + items_received.count("Decrease Speed") - items_received.count("Increase Speed")], "ROM")
                    ]
                    if self.garbage_hole_shuffles_given < items_received.count("Shuffle Garbage Line Hole"):
                        self.garbage_hole_shuffles_given += 1
                        data_writes.append(
                            (0xC400, shuffle_garbage_line(), "System Bus")
                        )
                    if self.garbage_lines_given < items_received.count("Garbage Line"):
                        lines = min(7, (items_received.count("Garbage Line") + data["active_garbage_lines"][0]) - self.garbage_lines_given)
                        if lines > data["active_garbage_lines"][0]:
                            success = await guarded_write(ctx.bizhawk_ctx, [(0xFFD3, [lines], "System Bus")],
                                                          [(0xFFD3, [data["active_garbage_lines"][0]], "System Bus")])
                            if success:
                                self.garbage_lines_given += lines - data["active_garbage_lines"][0]
                                logger.info(f"Sent {items_received.count("Garbage Line") - self.garbage_lines_given} garbage lines, had: {data["active_garbage_lines"][0]}, total now: {lines}")
                else:
                    self.garbage_lines_given = items_received.count("Garbage Line")
                    self.garbage_hole_shuffles_given = items_received.count("Shuffle Garbage Line Hole")

                    data_writes += [
                        (0xC400, shuffle_garbage_line(), "System Bus")
                    ]
                success = await write(ctx.bizhawk_ctx, data_writes)
        elif data["mode"][0] == 7:
            await write(ctx.bizhawk_ctx, PATCH)
            self.patched = True
            logger.info("Tetris game successfully patched.")
        elif data["patched"][0] < 42:
            logger.info("Return to the title screen to patch your Tetris game.")
            await write(ctx.bizhawk_ctx, [(0x014C, [42], "ROM")])

    def on_package(self, ctx, cmd: str, args: dict):
        super().on_package(ctx, cmd, args)
        if cmd == 'ReceivedItems':
            if self.garbage_lines_given is None:
                items_received = [list(items.keys())[item.item - 1] for item in ctx.items_received]
                self.garbage_lines_given = items_received.count("Garbage Line")

def shuffle_garbage_line():
    garbage_line = ([0x28] * 9) + [0x2F]
    random.shuffle(garbage_line)
    return garbage_line