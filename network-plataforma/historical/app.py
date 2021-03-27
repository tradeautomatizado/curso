import logging
import pandas as pd
from decouple import config
from historical.api import CommunicationApi, LogonInfo
from historical.graph import GraphicDisplay

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

class App():
    def __init__(self, stock_code):
        self._stock_code = stock_code.upper().strip()
        self._actual_bar = None
        self._data = None,
        self._comm_api = CommunicationApi()


    def _get_last_received_bar(self):
        return pd.to_datetime(self._data.iloc[-1:].time.values[0])        

    def _update_last_received_bar(self):
        self._actual_bar = self._get_last_received_bar()
        
    def _fetch_next(self):
        new_data = self._comm_api.fetch_next([self._stock_code], self._actual_bar)
        new_bar = pd.to_datetime(new_data.iloc[-1:].time.values[0])

        
        if (new_bar != self._actual_bar):                        
            # se é uma barra nova, atualiza a variavel de controle da ultima barra
            self._update_last_received_bar()
        else:
            # se a barra existe, apenas atualiza os preços da ultima barra
            self._data = self._data[:-1]
        
        self._data = self._data.append(new_data)
        return self._data.set_index(['time'])


    def run(self):
        logon_info = LogonInfo(
                account=config("account", default=None, cast=int),
                password=config("password", default=None, cast=str),
                server=config("server", None))

        api = self._comm_api
        graph = GraphicDisplay()

        api.connect(logon_info)
        
        self._data = api.get_historical([self._stock_code])        
        # get last received bar
        self._update_last_received_bar()
        
        df = self._data.set_index(['time'])

        graph.plot(stock_name=self._stock_code, data=df, fetch_func=self._fetch_next)
