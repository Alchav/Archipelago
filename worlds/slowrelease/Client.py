
from CommonClient import ClientCommandProcessor, CommonContext, logger, server_loop, gui_enabled, get_base_parser

import asyncio
import random
tracker_loaded = True
from worlds.tracker.TrackerClient import TrackerGameContext

class SlowReleaseCommandProcessor(ClientCommandProcessor):
    def _cmd_time(self, time):
        """Set the time per check."""
        self.ctx.time_per = float(time)
class SlowReleaseContext(TrackerGameContext):
    time_per = 10
    tags = ["SlowRelease", "Tracker"]
    game = ""
    has_game = False
    command_processor = SlowReleaseCommandProcessor
    autoplayer_task = None

    async def autoplayer(self):
        print("Autoplayer")
        inbk = False
        while not self.player_id:
            await asyncio.sleep(1)
        while True:
            if len(self.locations_available) > 0:
                inbk = False
                goal_location = random.choice(self.locations_available)
                logger.info(f"Going for {self.location_names.lookup_in_game(goal_location)}")
                await asyncio.sleep(self.time_per)
                await self.check_locations([goal_location])
                await asyncio.sleep(0.1)
            else:
                if inbk:
                    await asyncio.sleep(1)
                else:
                    logger.info("In BK.")
                    inbk = True
                    await asyncio.sleep(1)
    def make_gui(self):
        ui = super().make_gui()
        ui.base_title = "Slow Release Client"
        return ui
    def on_package(self, cmd, args):
        super().on_package(cmd, args)
        if cmd == "Connected":
            if "Tracker" in self.tags:
                self.tags.remove("Tracker")
                asyncio.create_task(self.send_msgs([{"cmd": "ConnectUpdate", "tags": self.tags}]))

            self.autoplayer_task = asyncio.create_task(self.autoplayer())
    def disconnect(self, *args):
        if self.autoplayer_task:
            self.autoplayer_task.cancel()
        if "Tracker" not in self.tags:
            self.tags.append("Tracker")
        return super().disconnect(*args)
def launch(*args):

    async def main(args):
        ctx = SlowReleaseContext(args.connect, args.password)
        ctx.auth = args.name
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")

        if tracker_loaded:
            ctx.run_generator()
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        await ctx.exit_event.wait()
        await ctx.shutdown()

    import colorama

    parser = get_base_parser(description="Slow Release Archipelago Client, for text interfacing.")
    parser.add_argument('--name', default=None, help="Slot Name to connect as.")
    parser.add_argument("url", nargs="?", help="Archipelago connection url")
    args = parser.parse_args(args)

    # handle if text client is launched using the "archipelago://name:pass@host:port" url from webhost
    if args.url:
        import urllib
        url = urllib.parse.urlparse(args.url)
        if url.scheme == "archipelago":
            args.connect = url.netloc
            if url.username:
                args.name = urllib.parse.unquote(url.username)
            if url.password:
                args.password = urllib.parse.unquote(url.password)
        else:
            parser.error(f"bad url, found {args.url}, expected url in form of archipelago://archipelago.gg:38281")

    # use colorama to display colored text highlighting on windows
    colorama.init()

    asyncio.run(main(args))
    colorama.deinit()

