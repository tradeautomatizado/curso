from os import close
import npyscreen
import drawille
import math
from random import random
from .positions import PositionListDisplay
from .account import AccountInfoDisplay
from .form_widgets_positions import FormWidgetsPositions
from .orders import OrdersListDisplay
from curses import KEY_F2, KEY_F4


class WindowForm(npyscreen.FormBaseNew):
    """
    Frameless Form
    """

    def create(self, *args, **kwargs):
        super(WindowForm, self).create(*args, **kwargs)

    def while_waiting(self):
        pass


class MultiLineWidget(npyscreen.BoxTitle):
    """
        A framed widget containing multiline text
    """

    _contained_widget = npyscreen.MultiLineEdit


class MainForm(WindowForm):
    def _draw_chart(self, canvas, data_points):
        """
            :param y: The next height to draw
            :param canvas: The canvas on which to draw
            :param chart_type: cpu/memory
        """

        for x in range(0, self.CHART_WIDTH):
            for y in range(self.CHART_HEIGHT, self.CHART_HEIGHT - data_points[x], -1):
                canvas.set(x, y)

        return canvas.frame(0, 0, self.CHART_WIDTH, self.CHART_HEIGHT)

    def _draw_account_info_wdiget(self, fd):
        self.basic_stats = self.add(
            AccountInfoDisplay,
            name="Informações da conta",
            relx=fd.account.REL_X,
            rely=fd.account.REL_Y,
            max_height=fd.account.HEIGHT,
            max_width=fd.account.WIDTH,
        )
        self.basic_stats.entry_widget.editable = False

    def _draw_stock_graph_widget(self, fd):
        self.stock_chart = self.add(
            MultiLineWidget,
            name=f"Carregando...",
            relx=fd.stock_graph.REL_X,
            rely=fd.stock_graph.REL_Y,
            max_height=fd.stock_graph.HEIGHT,
            max_width=fd.stock_graph.WIDTH,
        )
        self.stock_chart.value = ""
        self.stock_chart.entry_widget.editable = False

    def _draw_ordens_widget(self, fd):
        self.orders = self.add(
            OrdersListDisplay,
            name="Ordens",
            relx=fd.ordens.REL_X,
            rely=fd.ordens.REL_Y,
            max_height=fd.ordens.HEIGHT,
            max_width=fd.ordens.WIDTH,
        )
        self.orders.value = ""
        self.orders.entry_widget.scroll_exit = False

    def _draw_positions_widgets(self, fd):
        self.positions = self.add(
            PositionListDisplay,
            name="Posições abertas ( papel - data - preço compra - preço atual - volume - total )",
            relx=fd.posicoes.REL_X,
            rely=fd.posicoes.REL_Y,
            max_height=fd.posicoes.HEIGHT,
            max_width=fd.posicoes.WIDTH - 1,
        )

        self.positions.entry_widget.values = ""
        self.positions.entry_widget.scroll_exit = False

    def _when_change_stock(self, *args, **kwargs):
        self.parentApp.switchForm("SELECTSTOCKFORM")
        form = self.parentApp.getForm("SELECTSTOCKFORM")
        form.display()

    def _when_place_order(self, *args, **kwargs):
        self.parentApp.switchForm("PLACEORDERFORM")
        form = self.parentApp.getForm("PLACEORDERFORM")
        form.display()

    def _quit(self, *args, **kwargs):
        raise KeyboardInterrupt

    def create(self):
        self.add_handlers({"^Q": self._quit})
        self.add_handlers({KEY_F2: self._when_change_stock})
        self.add_handlers({KEY_F4: self._when_place_order})

        max_y, max_x = self.curses_pad.getmaxyx()
        fd = FormWidgetsPositions(max_x, max_y)

        self.CHART_HEIGHT = int(math.floor((fd.ordens.HEIGHT - 2) * 4))
        self.CHART_WIDTH = int(math.floor((fd.ordens.WIDTH - 2) * 2))

        stock_data = self.parentApp.broker.get_stock_by_bars(
            [self.parentApp.stock], self.CHART_WIDTH, self.parentApp.timeframe
        )

        p = stock_data.close
        scale = 100 / ((p.max() - p.min()) * 100)
        pdiff = p - p.min()
        prices = list((pdiff * scale * self.CHART_HEIGHT).dropna().apply(math.ceil))

        self.cpu_array = prices

        self._draw_account_info_wdiget(fd)
        self._draw_stock_graph_widget(fd)
        self._draw_ordens_widget(fd)
        self._draw_positions_widgets(fd)

        ACTIONS_WIDGET_REL_X = fd.LEFT_OFFSET
        ACTIONS_WIDGET_REL_Y = fd.posicoes.REL_Y + fd.posicoes.HEIGHT
        self.actions = self.add(npyscreen.FixedText, relx=ACTIONS_WIDGET_REL_X, rely=ACTIONS_WIDGET_REL_Y)
        self.actions.value = "^Q:Sair\t\tF2:Trocar papel"
        self.actions.display()
        self.actions.editable = True

    def _get_stock_graph_title(self):
        return f"{self.parentApp.stock} - [Ask: {self.parentApp.ask:.2f} - Bid: {self.parentApp.bid:.2f}]"

    def afterEditing(self):
        return

        # self.parentApp.setNextForm(None)

    def _update_stock_graph(self, data):
        p = data
        scale = 100 / ((p.max() - p.min()) * 100)
        pdiff = p - p.min()
        prices = list((pdiff * scale * self.CHART_HEIGHT).dropna().apply(math.ceil))

        stock_graph_canvas = drawille.Canvas()
        self.stock_chart.value = self._draw_chart(stock_graph_canvas, prices)
        self.stock_chart.name = self._get_stock_graph_title()

        self.stock_chart.update(clear=True)

    def update(self):
        """
        Update the form in background, this used to be called inside the ThreadJob
        and but now is getting called automatically in while_waiting
        """
        try:
            self.basic_stats.value = self.parentApp.broker.account_info()
            self.positions.entry_widget.values = self.parentApp.broker.list_opened_positions()
            self.orders.entry_widget.values = self.parentApp.broker.get_orders()

            self.parentApp.ask, self.parentApp.bid = self.parentApp.broker.get_ask_bid(self.parentApp.stock)

            stock_data = self.parentApp.broker.get_stock_by_bars(
                [self.parentApp.stock], self.CHART_WIDTH, self.parentApp.timeframe
            )
            self._update_stock_graph(stock_data.close)

            # Lazy update to GUI
            self.basic_stats.update(clear=True)
            self.positions.update(clear=True)
            self.orders.update(clear=True)

            # self.DISPLAY()
        # catch the fucking KeyError caused to c
        # cumbersome point of reading the stats data structures
        except KeyError:
            self._logger.info("Some of the stats reading failed", exc_info=True)

    def while_waiting(self):
        super().while_waiting()
        self.update()

