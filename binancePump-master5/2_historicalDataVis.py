import pandas as pd
import mplfinance as mpf

############################################# BURAYI DEGISTIR ##############################################
"""
data_historical klasörü içerisinde bulunan veriyi görselleştirir.
data_name değişkenine görselleştirilmek istenen verinin adı yazılır.
"""
data_name = "20230607_214659_EPXUSDT_1s"
#############################################################################################################

data_ = pd.read_pickle("data_historical\\"+data_name)

data_vis = data_.loc[:, ["event_time", "open", "high", "low", "close", "volume"]]
# Tarih sütununu dizin olarak ayarlayın
data_vis.set_index('event_time', inplace=True)
# Tarih sütununu datetime formatına dönüştürün
data_vis.index = pd.to_datetime(data_vis.index)

# Grafik çizin (https://plainenglish.io/blog/plot-stock-chart-using-mplfinance-in-python-9286fc69689)
mpf.plot(data_vis, type='candle', style='charles', volume=True, warn_too_much_data=100000, title = data_name)

# mpf.plot(data_vis, type='renko', renko_params=dict(brick_size='atr', atr_length=50),
#           style='charles', volume=True, warn_too_much_data=100000, title = data_name)

# %% combine data
############################################# BURAYI DEGISTIR ##############################################
"""
# data_historical klasörü içerisinde bulunan veriyi görselleştirir.
# data_name değişkenine görselleştirilmek istenen verinin adı yazılır.
# """
# main_data_name = "2023_04_25_7_00_00__2023_04_25_9_00_00_ETHUSDT_1s"

# datas_name = ["2023_04_25_7_00_00__2023_04_25_9_00_00_ETHUSDT_1d", 
#               "2023_04_25_7_00_00__2023_04_25_9_00_00_ETHUSDT_1h"]
# #############################################################################################################
    
# data_ = pd.read_pickle("data_historical\\"+main_data_name) 
# data_["event_time_dummy"] = data_
# for i in datas_name:
    
#     data_dummy = data_ = pd.read_pickle("data_historical\\"+i) 
#     data_merged = pd.merge(data_, data_dummy, on='event_time', how="outer")