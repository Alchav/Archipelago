from test.bases import WorldTestBase

from .. import SM64World


class SM64TestBase(WorldTestBase):
    game = SM64World.game
    world: SM64World
