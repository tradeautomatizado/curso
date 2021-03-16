import pandas as pd
import mplfinance as mpf
import matplotlib.animation as animation

class GraphicDisplay():
    def __init__(self):
        self._data = None
        self._fetch_data = None
        self._ax = None

    def _animation(self, interval):
        data = self._fetch_data()
        
        self._ax.clear()
        mpf.plot(data,ax=self._ax,type='candle')

    def plot(self, stock_name: str, data: pd.DataFrame, fetch_func):        
        self._data = data
        self._fetch_data = fetch_func
        
        fig, axes = mpf.plot(data,returnfig=True,figsize=(11,8),type='candle',title=stock_name)
        ax = axes[0]        

        self._ax = ax
        
        ani = animation.FuncAnimation(fig, self._animation, interval=250)

        mpf.show()
