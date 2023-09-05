import pandas as pd
pd.__version__  # for the record

df = pd.read_csv('data/SPY_20110701_20120630_Bollinger.csv',index_col=0,parse_dates=True)
df.shape
df.head(3)
df.tail(3)

import mplfinance as mpf
mpf.__version__
mpf.plot(df,volume=True)

# %%
apdict = mpf.make_addplot(df['LowerB'])

mpf.plot(df,volume=True,addplot=apdict)

# %%
apd = mpf.make_addplot(df['LowerB'],type='scatter')

mpf.plot(df,addplot=apd)

# %%
def percentB_belowzero(percentB,price):
    import numpy as np
    signal   = []
    previous = -1.0
    for date,value in percentB.iteritems():
        if value < 0 and previous >= 0:
            signal.append(price[date]*0.99)
        else:
            signal.append(np.nan)
        previous = value
    return signal

tdf = df.loc['05-10-2012':'06-07-2012',]  # Take a smaller data set so it's easier to see the scatter points

signal = percentB_belowzero(tdf['PercentB'], tdf['Close'])

apd = mpf.make_addplot(signal,type='scatter',markersize=200,marker='^')

mpf.plot(tdf,addplot=apd)