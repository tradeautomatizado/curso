import logging
from dataclasses import dataclass
from datetime import datetime
import pandas as pd
from pandas.plotting import register_matplotlib_converters
import matplotlib.pyplot as plt
import MetaTrader5 as mt5
from decouple import config
from mt5_conn import get_data_by_bar

register_matplotlib_converters()

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

@dataclass
class LogonInfo():
    account: int
    password: str
    server: str

class CommunicationApi():
    """Broker Communction Class."""
    def disconnect(self):
        mt5.shutdown()

    def connect(self, logon_info):
        """it establish communication with broker."""
        # connect to MetaTrader 5
        if not mt5.initialize():
            logger.error("initialize() failed")
            self.disconnect()
            return

        authorized = mt5.login(
            logon_info.account,
            password=logon_info.password,
            server=logon_info.server)

        if not authorized:
            logger.error(mt5.last_error()) 
            self.disconnect()
            return

        logger.debug(mt5.terminal_info())
        logger.debug(mt5.version())

    def get_historical(self, stock):
        N_BARS = 100
        ticks = get_data_by_bar(stock, N_BARS, mt5.TIMEFRAME_D1)
        return ticks

class GraphicDisplay():
    def plot(self, stock_name: str, data: pd.DataFrame):
        plt.plot(data['time'], data['close'], 'r-', label='close')
        
        # display the legends
        plt.legend(loc='upper left')
        
        # add the header
        plt.title(stock_name)
        
        # display the chart
        plt.show()        

logon_info = LogonInfo(
        account=config("account", default=None, cast=int),
        password=config("password", default=None, cast=str),
        server=config("server", None))

api = CommunicationApi()
graph = GraphicDisplay()

api.connect(logon_info)
data = api.get_historical(["PETR4"])

graph.plot(stock_name="PETR4", data=data)
