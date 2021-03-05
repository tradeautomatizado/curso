import pandas as pd
from pandas.plotting import register_matplotlib_converters
import matplotlib.pyplot as plt

register_matplotlib_converters()


class GraphicDisplay():
    def plot(self, stock_name: str, data: pd.DataFrame):
        plt.plot(data['time'], data['close'], 'r-', label='close')
        
        # display the legends
        plt.legend(loc='upper left')
        
        # add the header
        plt.title(stock_name)
        
        # display the chart
        plt.show()    