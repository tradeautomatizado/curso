
import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])

# Import the backtrader platform
import backtrader as bt


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


if __name__ == '__main__':
    # Cria a engine
    cerebro = bt.Cerebro()

    # Adicionamos nossa estratégia à engine
    cerebro.addstrategy(TestStrategy)

    # Datas are in a subfolder of the samples. Need to find where the script is
    # because it could have been called from anywhere
    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    datapath = os.path.join(modpath, '../data/daily/ABEV3.csv')

    # Create a Data Feed
    data = bt.feeds.GenericCSVData(
        dataname=datapath,
        # data inicial
        fromdate=datetime.datetime(2011, 1, 1),
        # data final
        todate=datetime.datetime(2020, 12, 31),
        # CSV está em ordem descendente de data
        reverse=True,
        # Formato de data
        dtformat=('%Y-%m-%d'),

        datetime=0,
        high=1,
        low=2,
        open=3,
        close=4,
        volume=5,
        openinterest=-1        
    )

    # Adicionamos os dados da ação à nossa engine
    cerebro.adddata(data)

    # Configuramos nosso valor inicial para a estratégia
    cerebro.broker.setcash(100000.0)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.run()

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())