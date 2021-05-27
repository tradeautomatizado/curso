
import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])

# Import the backtrader platform
import backtrader as bt
import MetaTrader5 as mt
import pandas as pd
from broker_api import BrokerAPI
import backtrader.analyzers as btanalyzers
import pyfolio as pf

# Nossa estratégia de teste
class TestStrategy(bt.Strategy):

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Buscamos os dados da primeira ação. Como só temos uma (ABEV3), pegamos o indice 0
        self.dataclose = self.datas[0].close

    def next(self):
        # Logamos o preço de fechamento da barra 
        self.log('Close, %.2f' % self.dataclose[0])

        if self.dataclose[0] < self.dataclose[-1]:
            if self.dataclose[-1] < self.dataclose[-2]:
                self.log('ORDEM DE COMPRA CRIADA, %.2f' % self.dataclose[0])
                self.order_target_value(target=3000)

        if self.position.size > 0:
            if self.dataclose[0] > self.dataclose[-1]:
                if self.dataclose[-1] > self.dataclose[-2]:
                    self.log('POSIÇÃO FECHADA, %.2f' % self.dataclose[0])
                    self.close()

if __name__ == '__main__':
    # Cria a engine
    cerebro = bt.Cerebro()

    # Adicionamos nossa estratégia à engine
    cerebro.addstrategy(TestStrategy)
    
    broker = BrokerAPI()
    df_stock = broker.get_stock_by_bars(['PETR4'], 1000, mt.TIMEFRAME_D1)

    df_stock = df_stock.rename(columns={'time':'date', 'real_volume': 'volume'})
    df_stock['date'] = pd.to_datetime(df_stock.date)
    df_stock = df_stock[['date', 'open', 'high', 'low', 'close', 'volume', 'stock']]
    df_stock = df_stock.set_index('date')
    
    data_bt = bt.feeds.PandasData(
        dataname=df_stock
    )

    # Adicionamos os dados da ação à nossa engine
    cerebro.adddata(data_bt)

    # Configuramos nosso valor inicial para a estratégia
    cerebro.broker.setcash(100000.0)

    # Analyzer
    cerebro.addanalyzer(bt.analyzers.PyFolio, _name='pyfolio')

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    results = cerebro.run()

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

    #cerebro.plot(volume=False)

    result = results[0]
    
    pyfoliozer = result.analyzers.getbyname('pyfolio')

    returns, positions, transactions, gross_lev = pyfoliozer.get_pf_items()    

    pf.create_full_tear_sheet(
        returns,
        positions=positions,
        transactions=transactions,
        #live_start_date='2005-05-01'
        )    