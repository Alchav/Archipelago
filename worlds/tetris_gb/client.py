import base64
import logging
import time

from NetUtils import ClientStatus
from worlds._bizhawk.client import BizHawkClient
from worlds._bizhawk import read, write, guarded_write

from .patch import PATCH

logger = logging.getLogger("Client")

DATA_LOCATIONS = {
    "mode": (0xffe1, 1),
    "level": (0xffa9, 1),
    "lines": (0xff9e, 2),
    "score": (0xc0a0, 3),
    "patched": (0x014C, 1)
}


class TetrisClient(BizHawkClient):
    system = ("GB", "SGB")
    game = "Tetris"

    def __init__(self):
        self.patched = None
        super().__init__()

    async def validate_rom(self, ctx):
        game_name = await read(ctx.bizhawk_ctx, [(0x134, 12, "ROM")])
        if game_name[0] == b"TETRIS\00\00\00\00\00\00":
            ctx.game = self.game
            ctx.items_handling = 0b111
            self.patched = None

            return True
        return False

    async def game_watcher(self, ctx):
        data = await read(ctx.bizhawk_ctx, [(loc_data[0], loc_data[1], "System Bus")
                                            for loc_data in DATA_LOCATIONS.values()])
        data = {data_set_name: data_name for data_set_name, data_name in zip(DATA_LOCATIONS.keys(), data)}

        if not self.patched:
            if data["patched"][0] == 172:
                self.patched = True
            elif data["mode"][0] == 7:
                await write(ctx.bizhawk_ctx, PATCH)
                self.patched = True
                logger.info("Tetris game successfully patched.")
            elif self.patched is None:
                logger.info("Return to the title screen to patch your Tetris game.")
                self.patched = False
        if data["mode"][0] == 0:
            pass