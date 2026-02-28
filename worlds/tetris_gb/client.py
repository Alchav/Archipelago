import logging

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
    "active_garbage_lines": (0xFFD3, 1),
    "input_trap": (0xcc00, 1),
    "line_clears": (0xcc01, 16),
    "game_board": (0xc840, 512)
}

input_traps = {
    "1 Frame of Random Inputs", "1 Second of Random Inputs", "2 Seconds of Random Inputs", "3 Seconds of Random Inputs"
}

lock_traps = {
    "Active Piece Gets Stuck in the Left Wall", "Active Piece Gets Stuck in the Right Wall",
    "Active Piece Locks Instantly"
}


class TetrisClient(BizHawkClient):
    system = ("GB", "SGB")
    game = "Tetris"

    def __init__(self):
        self.garbage_lines_given = None
        self.input_traps_given = None
        self.lock_traps_given = None
        self.clear_rows_given = None
        self.ghost_pieces_given = None
        self.garbage_hole_shuffles_given = 0
        super().__init__()

    async def validate_rom(self, ctx):
        game_name = await read(ctx.bizhawk_ctx, [(0x134, 12, "ROM")])
        if game_name[0] == b"TETRIS\00\00\00\00\00\00":
            ctx.game = self.game
            ctx.items_handling = 0b111
            ctx.want_slot_data = True

            return True
        return False

    async def game_watcher(self, ctx):

        data = await read(ctx.bizhawk_ctx, [(loc_data[0], loc_data[1], "System Bus")
                                            for loc_data in DATA_LOCATIONS.values()])
        data = {data_set_name: data_name for data_set_name, data_name in zip(DATA_LOCATIONS.keys(), data)}

        score = int(data["score"][::-1].hex())

        items_received = [list(items.keys())[item.item - 1] for item in ctx.items_received]

        if ctx.auth and ctx.slot_data:
            if self.garbage_lines_given is None:
                self.garbage_lines_given = items_received.count("Garbage Line")
            if self.ghost_pieces_given is None:
                self.ghost_pieces_given = items_received.count("Active Piece is an Illusion")
            if self.input_traps_given is None:
                self.input_traps_given = len([item for item in items_received if item in input_traps])
            if self.lock_traps_given is None:
                self.lock_traps_given = len([item for item in items_received if item in lock_traps])
            if self.clear_rows_given is None:
                self.clear_rows_given = items_received.count("Clear Random Row")

            if data["patched"][0] == 172:
                hide_next_piece = False
                if "Hide Next Piece" in items_received:
                    hide_next_piece = True
                if "Show Next Piece" in items_received:
                    hide_next_piece = False
                if items_received.count("Toggle Next Piece") % 2:
                    hide_next_piece = True
                speed = min(99, ctx.slot_data["starting_speed"] + items_received.count(
                        "Decrease Speed") - items_received.count("Increase Speed"))
                speed_bcd = list(map(int, f"{speed:02d}"))
                score_multipliers = min(99, items_received.count("Score Multiplier"))
                score_multipliers_bcd = list(map(int, f"{score_multipliers:02d}"))
                data_writes = [
                    (0xc0de, [0x01] if hide_next_piece else [0x00], "System Bus"),
                    (0xc210, [0x80] if hide_next_piece else [0x00], "System Bus"),
                    (0x1fc6, [score_multipliers], "ROM"),
                    (0x1afb, [speed], "ROM"),
                    (0xffa9, [speed], "System Bus"),
                    (0xff9e, speed_bcd, "System Bus"),
                    (0x04b5, [0xC8], "ROM")  # enable proceeding from menu
                ]
                if data["mode"][0] == 0:

                    location_checks = list(range(1, int(score / 50) + 1))
                    if len(ctx.locations_checked) != len(location_checks):
                        await ctx.send_msgs([{"cmd": "LocationChecks", "locations": location_checks}])

                    if speed_bcd[0] == 0:
                        speed_bcd[0] = 0x2F
                    if score_multipliers_bcd[0] == 0:
                        score_multipliers_bcd[0] = 0x2F

                    data_writes += [
                        (0x9950, speed_bcd, "System Bus"),  # main game vram
                        (0x9d50, speed_bcd, "System Bus"),  # pause screen vram
                        (0x98f0, score_multipliers_bcd, "System Bus"),  # main game vram
                        (0x9cf0, score_multipliers_bcd, "System Bus"),  # pause screen vram
                    ]

                    if score >= ctx.slot_data["goal"]:
                        data_writes += [
                            (0xcc13, [1], "System Bus")
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
                    if self.ghost_pieces_given < items_received.count("Active Piece is an Illusion"):
                        success = await guarded_write(ctx.bizhawk_ctx, [(0xCC12, [4], "System Bus")],
                                                      [(0xCC12, [0], "System Bus")])
                        if success:
                            self.ghost_pieces_given = items_received.count("Active Piece is an Illusion")
                    all_input_traps = [item for item in items_received if item in input_traps]
                    if self.input_traps_given < len(all_input_traps):
                        input_trap_value = data["input_trap"][0]
                        while input_trap_value < 255 and self.input_traps_given < len(all_input_traps):
                            next_trap = all_input_traps[self.input_traps_given]
                            self.input_traps_given += 1
                            input_trap_value += (1 if next_trap == "1 Frame of Random Inputs"
                                                 else 60 if next_trap == "1 Second of Random Inputs"
                                                 else 120 if next_trap == "2 Seconds of Random Inputs"
                                                 else 180 if next_trap == "3 Seconds of Random Inputs"
                                                 else 240 if next_trap == "4 Seconds of Random Inputs"
                                                 else None)
                        input_trap_value = min(255, input_trap_value)
                        data_writes.append(
                            (0xCC00, [input_trap_value], "System Bus")
                        )
                    all_lock_traps = [item for item in items_received if item in lock_traps]
                    if self.lock_traps_given < len(all_lock_traps):
                        next_trap = all_lock_traps[self.lock_traps_given]
                        if next_trap == "Instantly Lock Active Piece":
                            success = await guarded_write(ctx.bizhawk_ctx, [(0xCC11, [1], "System Bus"),
                                                                            (0xFF99, [0], "System Bus")],
                                                          [(0xC200, [0], "System Bus")])
                            if success:
                                self.lock_traps_given += 1
                        else:
                            piece_x = (0x17 if next_trap == "Active Piece Gets Stuck in the Left Wall"
                                       else 0x6F if next_trap == "Active Piece Gets Stuck in the Right Wall"
                                       else None)
                            success = await guarded_write(ctx.bizhawk_ctx, [(0xC202, [piece_x], "System Bus"),
                                (0xFF99, [0], "System Bus")], [(0xC200, [0], "System Bus")])
                            if success:
                                self.lock_traps_given += 1
                    clear_rows = items_received.count("Clear Random Row")
                    num_rows_to_clear = min(10 - sum(data["line_clears"]), clear_rows - self.clear_rows_given)
                    if num_rows_to_clear > 0:
                        rows_with_pieces = [
                            r for r in range(0, 16)
                            if any(v != 0x2F for v in data["game_board"][(15-r) * 32 + 2: (15-r) * 32 + 12])
                        ]
                        rows = [i for i in range(0, 16) if not data["line_clears"][i]]
                        rows.sort(key=lambda i: random.randint(0, 99) if i in rows_with_pieces else 100)
                        rows_to_clear = rows[:num_rows_to_clear]
                        data_writes += [(0xCC01 + i, [1], "System Bus") for i in rows_to_clear]
                        self.clear_rows_given += len(rows_to_clear)
                elif data["mode"][0] in range(46, 52) and score >= ctx.slot_data["goal"]:
                    await ctx.send_msgs([{
                        "cmd": "StatusUpdate",
                        "status": ClientStatus.CLIENT_GOAL
                    }])
                    ctx.finished_game = True

                else:
                    self.garbage_lines_given = items_received.count("Garbage Line")
                    self.garbage_hole_shuffles_given = items_received.count("Shuffle Garbage Line Hole")
                    self.lock_traps_given = items_received.count("Instantly Lock Active Piece")
                    self.input_traps_given = len([item for item in items_received if item in input_traps])
                    self.lock_traps_given = len([item for item in items_received if item in lock_traps])
                    data_writes += [
                        (0xC400, shuffle_garbage_line(), "System Bus")
                    ]
                success = await write(ctx.bizhawk_ctx, data_writes)
        elif data["mode"][0] == 37 and data["patched"][0] < 172:
            await write(ctx.bizhawk_ctx, PATCH + [(0xC400, shuffle_garbage_line(), "System Bus")])
            logger.info("Tetris game successfully patched.")
        elif data["patched"][0] < 42:
            logger.info("Reset your game to patch Tetris.")
            await write(ctx.bizhawk_ctx, [(0x014C, [42], "ROM")])
        if data["patched"][0] < 172:
            await write(ctx.bizhawk_ctx,
                        [
                            (0x9800 + (i * 32), [0x1B, 0x0E, 0x1C, 0x0E, 0x1D, 0x2F, 0x1D, 0x18, 0x2F, 0x19, 0x0A, 0x1D,
                                                 0x0C, 0x11, 0x2F, 0x10, 0x0A, 0x16, 0x0E, 0x24], "System Bus")
                            for i in range(0, 18)
                        ])


def shuffle_garbage_line():
    garbage_line = ([0x28] * 9) + [0x2F]
    random.shuffle(garbage_line)
    return garbage_line
