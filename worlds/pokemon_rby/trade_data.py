from typing import NamedTuple


class TradeData(NamedTuple):
    location: str
    rom_address: str
    source_location: str
    quiz_text: str | None = None


trade_data_rb_common = [
    TradeData(
        "Route 2 Trade House - Marcel Trade",
        "Trade_Marcel",
        "Route 24 - Wild Pokemon - 6",
        "Someone on Route 2<LINE>",
    ),
    TradeData(
        "Cinnabar Lab Fossil Room - Sailor Trade",
        "Trade_Sailor",
        "Pokemon Mansion 1F - Wild Pokemon - 3",
    ),
    TradeData(
        "Vermilion Trade House - Dux Trade",
        "Trade_Dux",
        "Route 3 - Wild Pokemon - 2",
        "A woman in<LINE>Vermilion City<CONT>",
    ),
    TradeData(
        "Route 18 Gate 2F - Marc Trade",
        "Trade_Marc",
        "Route 23/Cerulean Cave Fishing - Super Rod Pokemon - 1",
    ),
    TradeData(
        "Cerulean Trade House - Lola Trade",
        "Trade_Lola",
        "Route 10/Celadon Fishing - Super Rod Pokemon - 1",
        "A man in<LINE>Cerulean City<CONT>",
    ),
    TradeData(
        "Cinnabar Lab Trade Room - Doris Trade",
        "Trade_Doris",
        "Cerulean Cave 1F - Wild Pokemon - 9",
    ),
    TradeData(
        "Cinnabar Lab Trade Room - Crinkles Trade",
        "Trade_Crinkles",
        "Route 12 - Wild Pokemon - 4",
    ),
]

trade_data_red = trade_data_rb_common + [
    TradeData(
        "Route 11 Gate 2F - Terry Trade",
        "Trade_Terry",
        "Safari Zone Center - Wild Pokemon - 5",
    ),
    TradeData(
        "Underground Path Route 5 - Spot Trade",
        "Trade_Spot",
        "Safari Zone East - Wild Pokemon - 1",
        "Someone on Route 5<LINE>",
    ),
]

trade_data_blue = trade_data_rb_common + [
    TradeData(
        "Route 11 Gate 2F - Terry Trade",
        "Trade_Terry",
        "Safari Zone Center - Wild Pokemon - 7",
    ),
    TradeData(
        "Underground Path Route 5 - Spot Trade",
        "Trade_Spot",
        "Safari Zone East - Wild Pokemon - 7",
        "Someone on Route 5<LINE>",
    ),
]

trade_data_yellow = [
    TradeData(
        "Route 11 Gate 2F - Gurio Trade",
        "Trade_Gurio",
        "Cerulean Cave B1F - Wild Pokemon - 9",
        "Someone on Route 11<LINE>",
    ),
    TradeData(
        "Route 2 Trade House - Miles Trade",
        "Trade_Miles",
        "Mt Moon 1F - Wild Pokemon - 10",
        "Someone on Route 2<LINE>",
    ),
    TradeData(
        "Cinnabar Lab Fossil Room - Sticky Trade",
        "Trade_Sticky",
        "Safari Zone North - Wild Pokemon - 6",
        "A scientist in<LINE>Cinnabar Lab<CONT>",
    ),
    TradeData(
        "Route 18 Gate 2F - Spike Trade",
        "Trade_Spike",
        "Safari Zone Center - Wild Pokemon - 9",
        "Someone on Route 18<LINE>",
    ),
    TradeData(
        "Cinnabar Lab Trade Room - Buffy Trade",
        "Trade_Buffy",
        "Route 6 - Surf Pokemon - 9",
        "A scientist in<LINE>Cinnabar Lab<CONT>",
    ),
    TradeData(
        "Cinnabar Lab Trade Room - Cezanne Trade",
        "Trade_Cezanne",
        "Pokemon Mansion 1F - Wild Pokemon - 4",
        "A scientist in<LINE>Cinnabar Lab<CONT>",
    ),
    TradeData(
        "Underground Path Route 5 - Ricky Trade",
        "Trade_Ricky",
        "Pokemon Tower 5F - Wild Pokemon - 7",
        "Someone on Route 5<LINE>",
    ),
]
