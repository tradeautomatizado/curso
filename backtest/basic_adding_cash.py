import backtrader as bt

# inicializa nossa engine de backtest
cerebro = bt.Cerebro()

# vamos configurar o valor inicial para ser usado no backtest
cerebro.broker.setcash(50000.0)

print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

# executa nosso backtest
cerebro.run()

print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
