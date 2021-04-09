from MetaTrader5 import ORDER_TYPE_BUY_LIMIT
import npyscreen
import pandas as pd


class OrdersList(npyscreen.MultiLineAction):
    def __init__(self, *args, **keywords):
        super(OrdersList, self).__init__(*args, **keywords)

        max_y, max_x = self.parent.curses_pad.getmaxyx()
        self.X_SCALING_FACTOR = float(max_x) / 104

    def _quit(self, *args, **kwargs):
        raise KeyboardInterrupt

    def display_value(self, position):
        ORDER_TYPE_BUY = 0
        ORDER_TYPE_BUY_LIMIT = 2

        buys_types = (ORDER_TYPE_BUY, ORDER_TYPE_BUY_LIMIT)
        order_type = "C" if position.type in buys_types else "V"

        return "{0: <8} {5} {4}{1:<5.2f}{4}{2:<5.2f}{4}{3:<5.2f}{4}".format(
            position.symbol,
            position.price_open,
            position.volume_current,
            position.volume_current * position.price_open,
            " " * int(5 * self.X_SCALING_FACTOR),
            order_type,
        )


class OrdersListDisplay(npyscreen.BoxTitle):
    _contained_widget = OrdersList
