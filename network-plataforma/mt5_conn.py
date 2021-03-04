# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 19:23:09 2021

@author: codekraft
"""

from datetime import datetime
import pandas as pd
import MetaTrader5 as mt5

# connect to MetaTrader 5
if not mt5.initialize():
    print("initialize() failed")
    mt5.shutdown()


def get_data_by_bar(stocks: list, bars: int, timeframe: int) -> pd.DataFrame:
    data = None
    for i, stock in enumerate(stocks):
        rates = mt5.copy_rates_from_pos(stock, timeframe, 0, bars)
        rates_frame = pd.DataFrame(rates)
        rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s')
        rates_frame['stock'] = stock

        if i == 0:
            data = rates_frame
        else:
            data = data.append(rates_frame)
            
    return data      


def get_data_by_date(stocks: list, start_date: datetime, end_date:datetime, timeframe: int) -> pd.DataFrame:
    data = None
    for i, stock in enumerate(stocks):
        rates = mt5.copy_rates_range(stock, timeframe, start_date, end_date)
        rates_frame = pd.DataFrame(rates)
        rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s')
        rates_frame['stock'] = stock

        if i == 0:
            data = rates_frame
        else:
            data = data.append(rates_frame)

    return data