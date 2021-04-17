import npyscreen
import pandas as pd
import psutil
import weakref
from curses import KEY_F2, KEY_F4


class PositionsList(npyscreen.MultiLineAction):
    def __init__(self, *args, **keywords):
        super(PositionsList, self).__init__(*args, **keywords)

        max_y, max_x = self.parent.curses_pad.getmaxyx()
        self.X_SCALING_FACTOR = float(max_x) / 104

        self.add_handlers({"^Q": self._quit})
        self.add_handlers({KEY_F2: self._when_change_stock})
        self.add_handlers({KEY_F4: self._when_place_order})

    def _when_change_stock(self, *args, **kwargs):
        self.parent.parentApp.switchForm("SELECTSTOCKFORM")
        form = self.parent.parentApp.getForm("SELECTSTOCKFORM")
        form.display()

    def _when_place_order(self, *args, **kwargs):
        self.parent.parentApp.switchForm("PLACEORDERFORM")
        form = self.parent.parentApp.getForm("PLACEORDERFORM")
        form.display()

    def _quit(self, *args, **kwargs):
        raise KeyboardInterrupt

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
