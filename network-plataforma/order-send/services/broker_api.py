import pandas as pd
import MetaTrader5 as mt5
from datetime import datetime
from MetaTrader5 import AccountInfo


class BrokerAPI:
    def __init__(self) -> None:
        # connect to MetaTrader 5
        if not mt5.initialize():
            print("initialize() failed")
            mt5.shutdown()
            return

        # request connection status and parameters
        print(mt5.terminal_info())
        # get data on MetaTrader 5 version
        print(mt5.version())

    def list_opened_positions(self):
        positions = list(mt5.positions_get())
        positions.reverse()

        return positions

    def account_info(self) -> AccountInfo:
        ai = mt5.account_info()
        return ai

    def get_ask_bid(self, symbol):
        data = mt5.symbol_info(symbol)
        return data.ask, data.bid

    def get_stock_by_bars(self, stocks: list, bars: int, timeframe: int) -> pd.DataFrame:
        data = None
        for i, stock in enumerate(stocks):
            rates = mt5.copy_rates_from_pos(stock, timeframe, 0, bars)
            rates_frame = pd.DataFrame(rates)
            rates_frame["time"] = pd.to_datetime(rates_frame["time"], unit="s")
            rates_frame["stock"] = stock

            if i == 0:
                data = rates_frame
            else:
                data = data.append(rates_frame)

        return data

    def get_stock_by_date(
        self, stocks: list, start_date: datetime, end_date: datetime, timeframe: int
    ) -> pd.DataFrame:
        data = None
        for i, stock in enumerate(stocks):
            # rates = mt5.copy_rates_from_pos(stock, timeframe, 0, bars)
            rates = mt5.copy_rates_range(stock, timeframe, start_date, end_date)
            rates_frame = pd.DataFrame(rates)
            rates_frame["time"] = pd.to_datetime(rates_frame["time"], unit="s")
            rates_frame["stock"] = stock

            if i == 0:
                data = rates_frame
            else:
                data = data.append(rates_frame)

        return data

