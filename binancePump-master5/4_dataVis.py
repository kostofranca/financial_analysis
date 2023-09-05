import pandas as pd
import mplfinance as mpf
import numpy as np

def signalVisualization(df_vis, df_pump_dump):
    
    df_vis_index_string = df_vis.index.astype("string")
    signal   = []
    
    for i in range(len(df_vis)):
        if df_vis_index_string[i] in df_pump_dump.Event_Time.astype("string").tolist():
            signal.append(data_vis.low[i])
        else:signal.append(np.nan)

    return signal

############################################# BURAYI DEGISTIR ##############################################
"""
incelenmek istenile coin adı usdt ile yazılır
    data_historical klasöründe back test için kullanılan veri
    output_pump_dump ve output_buy_sell klasörlerinde bulunan back test ile elde edilen sonuçlar yazdırılır.
"""
coin_name = "EPXUSDT"
data_ = pd.read_pickle("data_historical\\"+"20230607_214659_EPXUSDT_1s")
data_pump_dump = pd.read_pickle("output_pump_dump\\"+"20230607_215230") 
data_buy_sell = pd.read_pickle("output_buy_sell\\"+"20230607_215230") 
#############################################################################################################

# Historical data
data_vis = data_.loc[:, ["event_time", "open", "high", "low", "close", "volume"]]
# Tarih sütununu dizin olarak ayarlayın
data_vis.set_index('event_time', inplace=True)
# Tarih sütununu datetime formatına dönüştürün
data_vis.index = pd.to_datetime(data_vis.index)

# back test result pump dump
data_pump_dump = data_pump_dump[data_pump_dump.Symbol == coin_name]
signal_pump = signalVisualization(data_vis, data_pump_dump[data_pump_dump.color == "green"])
signal_dump = signalVisualization(data_vis, data_pump_dump[data_pump_dump.color == "red"])

ap_pump = mpf.make_addplot(signal_pump,type='scatter',markersize=100,marker='o', color = "green", alpha = 0.5)
ap_dump = mpf.make_addplot(signal_dump,type='scatter',markersize=100,marker='o', color = "red", alpha = 0.5)

# back test result buy sell
data_buy_sell = data_buy_sell[data_buy_sell.Symbol == coin_name]
signal_buy = signalVisualization(data_vis, data_buy_sell[data_buy_sell.order_type == "long"])
signal_sell = signalVisualization(data_vis, data_buy_sell[data_buy_sell.order_type == "short"])

ap_buy = mpf.make_addplot(signal_buy,type='scatter',markersize=200,marker='^', color = "green")
ap_sell = mpf.make_addplot(signal_sell,type='scatter',markersize=200,marker='v', color = "red")

list_ap = [ap_pump, ap_dump, ap_buy, ap_sell]
list_signal = [signal_pump, signal_dump, signal_buy, signal_sell]

ap = []
for i in range(len(list_signal)):
    if len(list_signal[i]) != list_signal[i].count(np.nan):
        ap.append(list_ap[i])

# Grafik çizin (https://plainenglish.io/blog/plot-stock-chart-using-mplfinance-in-python-9286fc69689)
mpf.plot(data_vis, type='candle', style='charles', volume=True, warn_too_much_data=100000, addplot=ap, title = coin_name)


    
    
    
    
    
    
    
    
    
    
    
    
    
    