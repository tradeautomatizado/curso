# encoding: utf-8
import logging
import npyscreen
from services import BrokerAPI
from views import MainForm
from MetaTrader5 import TIMEFRAME_M1


class TradeAppGUI(npyscreen.NPSAppManaged):
    keypress_timeout_default = 5

    def __init__(self):
        super(TradeAppGUI, self).__init__()
        self._logger = logging.getLogger(__name__)

    def onStart(self):
        self.myDatabase = BrokerAPI()
        self.stock = "PETR4"
        self.ask = 0
        self.bid = 0
        self.timeframe = TIMEFRAME_M1
        self.window = MainForm(parentApp=self, name="Trade App [http://www.tradeautomatizado.com.br]")
        self.registerForm("MAIN", self.window)


if __name__ == "__main__":

    # app wide global stop flag
    # global_stop_event = threading.Event()

    App = TradeAppGUI()
    App.run()
