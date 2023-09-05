import datetime
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

timestamp = 1682193972194 / 1000  # Unix zaman damgası saniye cinsinden olduğu için milisaniyeleri kaldırın
dt = datetime.datetime.fromtimestamp(timestamp)

print(dt.strftime('%Y-%m-%d %H:%M:%S'))

# %% 
data_ = pd.read_pickle("data_historical\\"+"20230427_204624_BELUSDT_1s")
# Historical data
data_vis = data_.loc[:, ["event_time", "open", "high", "low", "close", "volume"]]
plt.hist(data_vis.volume, bins = 120)
plt.plot(data_vis.volume)
