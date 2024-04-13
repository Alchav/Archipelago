import asyncio
from CommonClient import CommonContext, ClientCommandProcessor, get_base_parser, server_loop, logger, gui_enabled
import Utils

class BingoCommandProcessor(ClientCommandProcessor):
    def _cmd_cards(self):
        if self.ctx.cards:
            for i, card in enumerate(self.ctx.cards, 1):
                logger.info(f"Bingo Card {i}")
                for row in range(5):
                    row_string = " ".join([str(card[x][row]).zfill(2) for x in range(0, 5)])
                    if row_string[6:8] == "00":
                        row_string = row_string[:6] + "XX" + row_string[8:]
                    logger.info(row_string)

class BingoClientContext(CommonContext):
    command_processor = BingoCommandProcessor
    game = "Bingo"
    items_handling = 0b111

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.cards = None
        self.send_locations = False

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(BingoClientContext, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    def on_package(self, cmd: str, args: dict):
        super().on_package(cmd, args)
        if cmd == 'Connected':
            self.cards = args['slot_data']["cards"]




    def run_gui(self):
        from kvui import GameManager
        from kivy.uix.tabbedpanel import TabbedPanelItem
        from kivy.clock import Clock
        from kivy.uix.gridlayout import GridLayout
        from kivy.uix.label import Label

        class BingoCard(GridLayout):
            def __init__(self, card_data, **kwargs):
                super(BingoCard, self).__init__(**kwargs)
                self.cols = 5  # Number of columns in the bingo card

                # Add labels to represent each cell in the card
                for column in card_data:
                    for number in column:
                        self.add_widget(Label(text=str(number)))

        class BingoManager(GameManager):
            base_title = "Archipelago Bingo Client"
            def build(self):
                container = super().build()

                panel = TabbedPanelItem(text="Bingo Cards")
                # self.bingo_panel = panel.content = BingoCard()
                for card_data in [[[1,2,3,4,5],[1,2,3,4,5],[1,2,3,4,5],[1,2,3,4,5],[1,2,3,4,5]], [[1,2,3,4,5],[1,2,3,4,5],[1,2,3,4,5],[1,2,3,4,5],[1,2,3,4,5]],[[1,2,3,4,5],[1,2,3,4,5],[1,2,3,4,5],[1,2,3,4,5],[1,2,3,4,5]], [[1,2,3,4,5],[1,2,3,4,5],[1,2,3,4,5],[1,2,3,4,5],[1,2,3,4,5]],[[1,2,3,4,5],[1,2,3,4,5],[1,2,3,4,5],[1,2,3,4,5],[1,2,3,4,5]], [[1,2,3,4,5],[1,2,3,4,5],[1,2,3,4,5],[1,2,3,4,5],[1,2,3,4,5]]]:
                    bingo_card = BingoCard(card_data, size_hint=(None, 1))
                    panel.add_widget(bingo_card)
                self.tabs.add_widget(panel)

                # Clock.schedule_interval(self.build_bingo_cards, 0.5)

                return container

        self.ui = BingoManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")
    pass

async def bingo_loop(ctx):
    from . import Bingo, start_ids
    while not ctx.exit_event.is_set():
        try:
            await asyncio.wait_for(ctx.watcher_event.wait(), 0.125)
        except asyncio.TimeoutError:
            pass
        ctx.watcher_event.clear()
        if not ctx.cards:
            continue
        checked_locations = []
        items_received = [item.item - start_ids for item in ctx.items_received]
        # for i, card in enumerate(self.stored_data["cards"]):
        for location in Bingo.location_name_to_id.keys():
            card = int(location.split(" ")[2]) - 1
            n = int(location.split(" ")[5]) - 1
            line_type = location.split(" ")[4]
            if line_type == "Horizontal":
                coords = [(i, n) for i in range(5)]
                # location.access_rule = lambda state: state.has_all([f"Bingo Call {bingo_letter(self.cards[card][r][n])}-{self.cards[card][r][n]}" for r in range(1, 6)], self.player)
            elif line_type == "Vertical":
                coords = [(n, i) for i in range(5)]
                # location.access_rule = lambda state: state.has_all([f"Bingo Call {bingo_letter(self.cards[card][n][r])}-{self.cards[card][n][r]}" for r in range(1, 6)], self.player)
            elif line_type == "Diagonal":
                if n == 0:
                    coords = [(i, i) for i in range(5)]
                else:
                    coords = [(i, 4-i) for i in range(5)]
            needed_calls = [ctx.cards[card][coord[0]][coord[1]] for coord in coords if ctx.cards[card][coord[0]][coord[1]] != 0]
            if all(item in items_received for item in needed_calls):
                checked_locations.append(Bingo.location_name_to_id[location])

        if len(checked_locations) != len(ctx.checked_locations):
            await ctx.send_msgs([{"cmd": "LocationChecks", "locations": list(checked_locations)}])


def launch():
    async def main():
        parser = get_base_parser()
        args = parser.parse_args()
        ctx = BingoClientContext(args.connect, args.password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")
        b_loop = asyncio.create_task(bingo_loop(ctx), name="BingoLoop")

        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        await ctx.exit_event.wait()
        await ctx.shutdown()

    Utils.init_logging("BizHawkClient", exception_logger="Client")
    import colorama
    colorama.init()
    asyncio.run(main())
    colorama.deinit()