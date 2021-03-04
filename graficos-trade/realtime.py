import pandas as pd
import mplfinance as mpf
import matplotlib.animation as animation

class RealTimeAPI():
    def __init__(self):
        self.data_pointer = 0
        self.data_frame = pd.read_csv('SP500_NOV2019_IDay.csv',index_col=0,parse_dates=True)
        self.df_len = len(self.data_frame)

    def fetch_next(self):
        r1 = self.data_pointer
        self.data_pointer += 1
        if self.data_pointer >= self.df_len:
            return None
        return self.data_frame.iloc[r1:self.data_pointer,:]

    def initial_fetch(self):
        if self.data_pointer > 0:
            return
        r1 = self.data_pointer
        self.data_pointer += int(0.2*self.df_len)
        return self.data_frame.iloc[r1:self.data_pointer,:]

rtapi = RealTimeAPI()

resample_map ={'Open' :'first',
               'High' :'max'  ,
               'Low'  :'min'  ,
               'Close':'last' }
resample_period = '15T'

df = rtapi.initial_fetch()
rs = df.resample(resample_period).agg(resample_map).dropna()

# plot
fig, axes = mpf.plot(rs,returnfig=True,figsize=(11,8),type='candle',title='\n\nSP500 bar to bar')
ax = axes[0]

def animate(ival):
    global df
    global rs
    nxt = rtapi.fetch_next()
    if nxt is None:
        print('no more data to plot')
        ani.event_source.interval *= 3
        if ani.event_source.interval > 12000:
            exit()
        return
    df = df.append(nxt)
    rs = df.resample(resample_period).agg(resample_map).dropna()
    ax.clear()
    mpf.plot(rs,ax=ax,type='candle')

ani = animation.FuncAnimation(fig, animate, interval=250)

mpf.show()
