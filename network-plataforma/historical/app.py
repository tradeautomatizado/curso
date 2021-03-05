import logging
from decouple import config
from historical.api import CommunicationApi, LogonInfo
from historical.graph import GraphicDisplay

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

class App():
    def __init__(self, stock_code):
        self._stock_code = stock_code.upper()

    def run(self):
        logon_info = LogonInfo(
                account=config("account", default=None, cast=int),
                password=config("password", default=None, cast=str),
                server=config("server", None))

        api = CommunicationApi()
        graph = GraphicDisplay()

        api.connect(logon_info)
        data = api.get_historical([self._stock_code])

        graph.plot(stock_name=self._stock_code, data=data)
