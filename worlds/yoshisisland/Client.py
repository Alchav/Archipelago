import logging
import asyncio
import typing

from NetUtils import ClientStatus, color
from worlds.AutoSNIClient import SNIClient

if typing.TYPE_CHECKING:
    from SNIClient import SNIContext
else:
    SNIContext = typing.Any

snes_logger = logging.getLogger("SNES")

GAME_YI = "Yoshi's Island"

ROM_START = 0x000000
WRAM_START = 0xF50000
WRAM_SIZE = 0x20000
SRAM_START = 0xE00000

YOSHISISLAND_ROMHASH_START = 0x007FC0
ROMHASH_SIZE = 0x0F

ITEMQUEUE_HIGH = WRAM_START + 0x1465
ITEMQUEUE_LOW = WRAM_START + 0x1466
ITEM_RECEIVED = WRAM_START + 0x1467
GAME_MODE = WRAM_START + 0x0118

VALID_GAME_STATES = [0x0F, 0x10, 0x2C]

class YISNIClient(SNIClient):
    game = "Yoshi's Island"

    async def validate_rom(self, ctx):
        from SNIClient import snes_buffered_write, snes_flush_writes, snes_read

        rom_name = await snes_read(ctx, YOSHISISLAND_ROMHASH_START, ROMHASH_SIZE)
        if rom_name is None or rom_name == bytes([0] * ROMHASH_SIZE) or rom_name[:7] != b"YOSHIAP":
            return False

        ctx.game = self.game
        ctx.items_handling = 0b111  # remote items
        ctx.rom = rom_name
        return True

    async def game_watcher(self, ctx):
        from SNIClient import snes_buffered_write, snes_flush_writes, snes_read


        game_mode = await snes_read(ctx, GAME_MODE, 0x1)
        item_received = await snes_read(ctx, ITEM_RECEIVED,0x1)

        if game_mode is None:
            return
        elif game_mode[0] == 0x1D:
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            ctx.finished_game = True
        elif game_mode[0] not in VALID_GAME_STATES:
            return
        elif item_received[0] > 0x00:
            return
            
        from worlds.yoshisisland.Rom import item_values
        rom = await snes_read(ctx, YOSHISISLAND_ROMHASH_START, ROMHASH_SIZE)
        if rom != ctx.rom:
            ctx.rom = None
            return

        new_checks = []
        from worlds.yoshisisland.Rom import location_table, item_values
        location_ram_data = await snes_read(ctx, WRAM_START + 0x1440, 0x80)
        for loc_id, loc_data in location_table.items():
            if loc_id not in ctx.locations_checked:
                data = location_ram_data[loc_data[0] - 0x1440]
                masked_data = data & (1 << loc_data[1])
                bit_set = (masked_data != 0)
                invert_bit = ((len(loc_data) >= 3) and loc_data[2])
                if bit_set != invert_bit:
                    new_checks.append(loc_id)

        for new_check_id in new_checks:
            ctx.locations_checked.add(new_check_id)
            location = ctx.location_names[new_check_id]
            snes_logger.info(
                f'New Check: {location} ({len(ctx.locations_checked)}/{len(ctx.missing_locations) + len(ctx.checked_locations)})')
            await ctx.send_msgs([{"cmd": 'LocationChecks', "locations": [new_check_id]}])

        recv_count = await snes_read(ctx, ITEMQUEUE_HIGH, 1)
        if recv_count[0] >= 255:
            recv_count = await snes_read(ctx, ITEMQUEUE_LOW, 1)
            high_check = 1
        else:
            high_check = 0
        recv_index = recv_count[0]

        if recv_index < len(ctx.items_received):
            item = ctx.items_received[recv_index]
            recv_index += 1
            logging.info('Received %s from %s (%s) (%d/%d in list)' % (
                color(ctx.item_names[item.item], 'red', 'bold'),
                color(ctx.player_names[item.player], 'yellow'),
                ctx.location_names[item.location], recv_index, len(ctx.items_received)))

            if high_check == 1:
                recv_index -= 10
                snes_buffered_write(ctx, ITEMQUEUE_LOW, bytes([recv_index]))
            else:
                snes_buffered_write(ctx, ITEMQUEUE_HIGH, bytes([recv_index]))
            if item.item in item_values:
                item_count = await snes_read(ctx, WRAM_START + item_values[item.item][0], 0x1)
                increment = item_values[item.item][1]
                new_item_count = item_count[0]
                if increment > 1:
                    new_item_count = increment
                else:
                    new_item_count += increment

                snes_buffered_write(ctx, WRAM_START + item_values[item.item][0], bytes([new_item_count]))
        await snes_flush_writes(ctx)