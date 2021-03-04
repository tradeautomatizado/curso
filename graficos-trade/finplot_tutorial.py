import pandas as pd
import finplot as fplt

df = pd.read_csv("./stocks/daily/VALE3.csv")
df.date = pd.to_datetime(df.date, format='%Y-%m-%d')
df = df.set_index(['date'])


fplt.candlestick_ochl(df[-100:][['open', 'close', 'high', 'low']])
fplt.show()