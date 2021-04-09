from copy import Error
import pandas as pd
import MetaTrader5 as mt5
from datetime import datetime
from MetaTrader5 import AccountInfo


class OrderSendError(Exception):
    pass


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

    def send_order(self, stock_name: str, stock_qty: int, stock_price: float, order_type: int):
        request = {
            "action": mt5.TRADE_ACTION_PENDING,
            "symbol": stock_name,
            "volume": float(stock_qty),
            "type": order_type,
            "price": float(stock_price),
            "magic": 234000,
            "comment": "Trade Automatizado APP Demo",
            "type_time": mt5.ORDER_TIME_DAY,
            "type_filling": mt5.ORDER_FILLING_RETURN,
        }

        result = mt5.order_send(request)

        if not result:
            raise OrderSendError("Order_send failed, retcode={}".format(mt5.last_error()))
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            raise OrderSendError("Order_send failed, retcode={}".format(result.retcode))

        return True

    def buy(self, stock_name: str, stock_qty: int, stock_price: float):
        return self.send_order(stock_name, stock_qty, stock_price, mt5.ORDER_TYPE_BUY_LIMIT)

    def sell(self, stock_name: str, stock_qty: int, stock_price: float):
        return self.send_order(stock_name, stock_qty, stock_price, mt5.ORDER_TYPE_SELL)

    def get_orders(self):
        return mt5.orders_get()
