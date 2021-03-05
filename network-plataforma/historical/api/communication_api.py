import logging
import MetaTrader5 as mt5
from historical.core import get_data_by_bar

logger = logging.getLogger(__name__)


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