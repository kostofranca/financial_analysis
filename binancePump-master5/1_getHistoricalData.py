import pandas as pd
from datetime import datetime
import requests
import json

############################################# BURAYI DEGISTIR ##############################################
"""
İstenilen periyot ile historical veri elde etmek için kullanılıyor
1 saniyede veri alabiliyor
Elde edilen veri kaydediliyor

Veriler data_historical klasörü içerisine o anın tarih ve saat ile kaydediliyor
"""
# Binance API anahtarlarınızı buraya girin
api_key = ""
api_secret = ""

# API isteği için gerekli parametreleri ayarlayın
symbol = "EPXUSDT" # BTC / USDT çifti
interval = "1s" # 1 saniyelik veri aralığı (1m)-(1s)
freq = "1S" # 1 saniyelik veri aralığı (1min)-(1S) (https://pandas.pydata.org/docs/user_guide/timeseries.html#timeseries-offset-aliases)
initial_start_date_string = '2023-06-06 21:50:00.000000'
initial_end_date_string = '2023-06-06 22:00:00.000000'
#############################################################################################################

limit = 1000 # API isteği başına döndürülecek maksimum veri sayısı
date_range = pd.date_range(start = pd.to_datetime(initial_start_date_string), 
                           end = pd.to_datetime(initial_end_date_string), 
                           freq = freq)

list_data_json = []
for i in range(len(date_range) // limit + 1):   
    if i == len(date_range) // limit:
        start_date_string = date_range[i*limit]
        end_date_string = date_range[-1]
    else:
        start_date_string = date_range[i*limit]
        end_date_string = date_range[i*limit + limit - 1]
    print()

    dt_s = datetime.strptime(str(start_date_string), '%Y-%m-%d %H:%M:%S')
    startTime = int(dt_s.timestamp()*1000)
    print("startTime: {} - timestamp: {}".format(dt_s, startTime))
    
    dt_e = datetime.strptime(str(end_date_string), '%Y-%m-%d %H:%M:%S')
    endTime = int(dt_e.timestamp()*1000)
    print("endTime: {} - timestamp: {}".format(dt_e, endTime))

    # API isteği yapın
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}&startTime={startTime}&endTime={endTime}"
    headers = {"X-MBX-APIKEY": api_key}
    response = requests.get(url, headers=headers)
    
    # API yanıtını JSON formatına çevirin
    data_json = json.loads(response.text)
    for j in data_json:
        list_data_json.append(j)
    
data = pd.DataFrame(list_data_json, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time',
                                             'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume',
                                             'taker_buy_quote_asset_volume', 'ignore'])

# check whether desired time range is achieved or not
data["event_time"] = [datetime.fromtimestamp(i/1000) for i in data.timestamp]
data[['open', 'high', 'low', 'close', 'volume']] = data[['open', 'high', 'low', 'close', 'volume']].astype(float)

data.to_pickle("data_historical\\"+datetime.now().strftime("%Y%m%d_%H%M%S") + "_"+symbol+"_"+interval)