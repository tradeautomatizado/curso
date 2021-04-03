import npyscreen
import pandas as pd


class PositionsList(npyscreen.MultiLineAction):
    def __init__(self, *args, **keywords):
        super(PositionsList, self).__init__(*args, **keywords)

        max_y, max_x = self.parent.curses_pad.getmaxyx()
        self.X_SCALING_FACTOR = float(max_x) / 104

        self.add_handlers({"^A": lambda x: x})

    def display_value(self, position):
        return "{0: <8}{4}{1}{4}{2:<10.2f}{4}{3:<10.2f}{4}{5:<10.2f}{6:<10.2f}".format(
            position.symbol,
            pd.to_datetime(position.time, unit="s"),
            position.price_open,
            position.price_current,
            " " * int(5 * self.X_SCALING_FACTOR),
            position.volume,
            position.volume * position.price_current,
        )


class PositionListDisplay(npyscreen.BoxTitle):
    _contained_widget = PositionsList
