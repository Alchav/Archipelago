import asyncio
from CommonClient import CommonContext, get_base_parser, server_loop, logger, gui_enabled, ClientStatus
import Utils


class IDClientContext(CommonContext):
    game = "Item Dispenser"
    items_handling = 0b111

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.tokens = 0

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(IDClientContext, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    def run_gui(self):
        from kvui import GameManager

        class IDManager(GameManager):
            base_title = "Archipelago Item Dispenser Client"

        self.ui = IDManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")


async def id_loop(ctx):
    try:
        while not ctx.exit_event.is_set():
            try:
                await asyncio.wait_for(ctx.watcher_event.wait(), 0.125)
            except asyncio.TimeoutError:
                pass
            ctx.watcher_event.clear()
            tokens = sum((item.item for item in ctx.items_received))
            if tokens > ctx.tokens:
                await ctx.send_msgs([{"cmd": "LocationChecks",
                                      "locations": list(range(1, tokens + 1))}])
            if len(ctx.checked_locations) == len(ctx.server_locations) and not ctx.finished_game:
                ctx.finished_game = True
                await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])

    except Exception as e:
        breakpoint()




def launch():
    async def main():
        parser = get_base_parser()
        args = parser.parse_args()
        ctx = IDClientContext(args.connect, args.password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")
        client_loop = asyncio.create_task(id_loop(ctx), name="IDLoop")

        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        await ctx.exit_event.wait()
        await ctx.shutdown()

    Utils.init_logging("IDClient", exception_logger="Client")
    import colorama
    colorama.init()
    asyncio.run(main())
    colorama.deinit()