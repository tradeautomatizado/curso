import pandas as pd
import numpy as np
import finplot as fplt

# carregar o dataset
df = pd.read_csv("../data/daily/VALE3.csv")
df.date = pd.to_datetime(df.date, format='%Y-%m-%d')
df = df.set_index(['date'])

# filtrar apenas o último ano
df = df['2019-12-30':'2020-12-31']

# criamos 4 eixos
ax1,ax2,ax3,ax4 = fplt.create_plot('VALE3 long term analysis', rows=4, maximize=False)

# configuramos nosso primeiro eixo para usar escala logaritimica
fplt.set_y_scale(ax=ax1, yscale='log')

# plotamos o preço de fechamento
fplt.plot(df.close, color='#000', legend='Preço (Log)', ax=ax1)

# vamos calcular as médias móveis de 21 e 50 períodos
df['ma21'] = df.close.rolling(21).mean()
df['ma50'] = df.close.rolling(50).mean()

# plotamos as médias
fplt.plot(df.ma21, legend='MA21', ax=ax1)
fplt.plot(df.ma50, legend='MA50', ax=ax1)

# volume
df['one'] = 1
fplt.volume_ocv(df[['ma21','ma50','one']], candle_width=1, ax=ax1.overlay(scale=0.02))

# retorno diario
daily_ret = df.close.pct_change()*100
fplt.plot(daily_ret, width=3, color='#000', legend='Daily returns %', ax=ax2)

# histograma do retorno diario
fplt.add_legend('Daily % returns histogram', ax=ax3)
fplt.hist(daily_ret, bins=60, ax=ax3)

# calcular o retornor mensal usando a funcao resample 
months = df['close'].resample('M').last().pct_change().dropna().to_frame() * 100

# plotar um heatmap com o percentual mensal
months.index = mnames = months.index.month_name().to_list()
mnames = mnames[mnames.index('January'):][:12]
mrets = [months.loc[mname].mean() for mname in mnames]
hmap = pd.DataFrame(columns=[2,1,0], data=np.array(mrets).reshape((3,4)).T)
hmap = hmap.reset_index() 
colmap = fplt.ColorMap([0.3, 0.5, 0.7], [[255, 110, 90], [255, 247, 0], [60, 255, 50]]) # traffic light
fplt.heatmap(hmap, rect_size=1, colmap=colmap, colcurve=lambda x: x, ax=ax4)
for j,mrow in enumerate(np.array(mnames).reshape((3,4))):
    for i,month in enumerate(mrow):
        s = month+' %+.2f%%'%hmap.loc[i,2-j]
        fplt.add_text((i, 2.5-j), s, anchor=(0.5,0.5), ax=ax4)

ax4.set_visible(crosshair=False, xaxis=False, yaxis=False) # hide junk for a more pleasing look

fplt.show()
