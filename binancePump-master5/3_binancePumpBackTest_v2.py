import pandas as pd
from tqdm import tqdm
import glob
import datetime as dt
from datetime import datetime
import operator
from pricechange import *
from binanceHelper import *
from pricegroup import *
from order import *
############################################# BURAYI DEGISTIR ##############################################
"""
data_historical içerisinde bulunan veriyi okur,
interval = 1s (1 saniye) için data_historical içerisinde bulunan verinin sonunda "_1s" yazan tüm veriyi okur.
Burada birden fazla veri varsa hepsini otomatik olarak okur

Çıktı:
    Dump ve pump olan coinleri output_pump_dump klasörü içerisine o anın tarihi ile kaydeder.
    Dump ve pump olan coinler data_pump_dump degiskeni ile incelenebilir. Console'a print ile yazılmasına gerek yoktur.
    
    Al ve sat emri çıkan coinler output_buy_sell klasörü içerisine o anın tarihi ile kaydeder.
    
"""
interval = "1s"
show_only_pair = "USDT" #Select nothing for all, only selected currency will be shown,
show_limit = 2      #minimum top query limit
min_perc = 0.2  #min percentage change
volume_threshold = 10
#############################################################################################################

# Read Data
folder_name = "data_historical"
list_file_names = glob.glob(folder_name+"/*")

list_data = []
for file in list_file_names:
    if interval in file:
        print(file)
        data = pd.read_pickle(file)
        
        data["s"] = len(data)*[file.split("_")[-2]]
        data['open'] = data['open'].astype(str)
        data.rename(columns={'open': 'c', 'timestamp': 'E'}, inplace=True)
        
        list_data.append(data)

# json formatına çevir
list_json_message = []
for i in tqdm(range(len(data))):
    json_message_l = []
    for j in range(len(list_data)):
        data_dummy = list_data[j]
        json_message_l.append(dict(data_dummy.iloc[i, :]))
    list_json_message.append(json_message_l)

# Backtest
price_changes = []
price_groups = {}

TRADED_COIN = []       

previous_price_groups = []
copy_previous_price_groups = []
list_pump_dump = []
list_buy_sell = []

for json_message in tqdm(list_json_message):
    
    # print("on_message")
    
    # price_changes listesinin icerisine PriceChange sınıfına ait nesneleri ekliyor.
    for ticker in json_message: # json_message is a list that includes dictionaries.
        symbol = ticker['s']  
        
        if ('USDT' in symbol and  not 'BUSDT' in symbol):     
            price = float(ticker['c']) # Last price
            volume = float(ticker['volume']) # volume
            number_of_trades = int(ticker['number_of_trades']) # number_of_trades
            event_time = dt.datetime.fromtimestamp(int(ticker['E'])/1000)
            if len(price_changes) > 0:
                price_change = filter(lambda item: item.symbol == symbol, price_changes)
                price_change = list(price_change)
                if (len(price_change) > 0):
                    price_change = price_change[0]
                    price_change.all_prices.append(price)
                    price_change.event_time = event_time
                    price_change.prev_price = price_change.price
                    price_change.price = price
                    price_change.volume = volume
                    price_change.number_of_trades = number_of_trades
                    price_change.isPrinted = False
                    price_change.is_refresh_list = False
                else:
                    price_changes.append(PriceChange(symbol, price, price,  False, event_time, price, False, volume, number_of_trades))
            else:
                price_changes.append(PriceChange(symbol, price, price, False, event_time, price, False, volume, number_of_trades))

    price_changes.sort(key=operator.attrgetter('price_change_perc'), reverse=True)
        
    for price_change in price_changes:
        
        console_color = 'green'
        temp_price_change  = price_change.price_change_perc
        if  temp_price_change < 0:
            console_color = 'red'

        if (not price_change.isPrinted and abs(temp_price_change) >= min_perc) :

            price_change.isPrinted = True 
            
            # volume filtresi ekle
            if price_change.volume >= volume_threshold:
                if not price_change.symbol in price_groups:
                    price_groups[price_change.symbol] = PriceGroup(price_change.symbol,                                                                
                                                                1,                                                                
                                                                abs(temp_price_change),
                                                                temp_price_change,                                                            
                                                                price_change.price,                                                                                                                             
                                                                price_change.event_time,
                                                                False,
                                                                min(price_change.all_prices),
                                                                max(price_change.all_prices),
                                                                price_change.volume,
                                                                price_change.number_of_trades)
                else:
                    # Eğer anlık fiyat şimdiye kadar gelen fiyatların maksimum değerinin 0.998 katından büyükse yada
                    # anlık fiyat şimdiye kadar gelen fiyatların minimum değerinin 1.002 katından küçükse
                    # tutulan verinin son fiyatı güncelleniyor (burada her veri tutulmasın diye basit bir kural eklenmiş)
                    if ((price_change.price >= (price_groups[price_change.symbol].max_price)*0.998) or 
                        (price_change.price <= (price_groups[price_change.symbol].min_price)*1.002)):
    
                        price_groups[price_change.symbol].tick_count += 1
                        price_groups[price_change.symbol].last_event_time = price_change.event_time
                        price_groups[price_change.symbol].last_price = price_change.price
                        price_groups[price_change.symbol].isPrinted = False
                        price_groups[price_change.symbol].total_price_change = abs(temp_price_change)
                        price_groups[price_change.symbol].relative_price_change = temp_price_change 
                        price_groups[price_change.symbol].min_price = min(price_change.all_prices)      
                        price_groups[price_change.symbol].max_price = max(price_change.all_prices)   
                        price_groups[price_change.symbol].volume = price_change.volume 
                        price_groups[price_change.symbol].number_of_trades = price_change.number_of_trades
    
                    if price_change.is_refresh_list:
                        price_groups[price_change.symbol].refresh_datas

        if abs(temp_price_change) < min_perc:
            break            

    if len(price_groups)>0:
        anyPrinted = False 
        
        sorted_price_group = sorted(price_groups, key=lambda k:price_groups[k]['total_price_change'])
        if (len(sorted_price_group)>0):
            sorted_price_group = list(reversed(sorted_price_group))
            sorted_price_group = sorted_price_group[:3]    
            # print("sorted_price_group: ",sorted_price_group)

            if len(previous_price_groups) > 0:

                copy_previous_price_groups = previous_price_groups.copy()

                for s in range(0,len(copy_previous_price_groups)):

                    if (not copy_previous_price_groups[s] in sorted_price_group) or (price_groups[copy_previous_price_groups[s]].isPrinted):
                        
                        #  if you dont want to create order, comment line start from here 

                        # if (not TRADED_COIN.count(price_groups[copy_previous_price_groups[s]].symbol) > 0  and not order.getOpenOrder())  and order.isAnyLiquidation():
                        if not TRADED_COIN.count(price_groups[copy_previous_price_groups[s]].symbol) > 0:

                            if price_groups[copy_previous_price_groups[s]].relative_price_change > 0: 
                                # order.enterShortOrder(symbol = price_groups[copy_previous_price_groups[s]].symbol
                                #                     ,price =  price_groups[copy_previous_price_groups[s]].last_price   
                                #                     ,type = 'MARKET')
                                    
                                explanation = 'Enter Short ' 
                                # print(explanation, ' ',price_groups[copy_previous_price_groups[s]].symbol)
                                
                                TRADED_COIN.append(price_groups[copy_previous_price_groups[s]].symbol)
                                list_buy_sell.append(price_groups[copy_previous_price_groups[s]].to_list("short"))
                            else:                                        
                                # order.enterLongOrder(symbol = price_groups[copy_previous_price_groups[s]].symbol
                                #                     ,price = price_groups[copy_previous_price_groups[s]].last_price   
                                #                     ,type = 'MARKET')     
                                    
                                explanation = 'Enter Long '                                  
                                # print(explanation, ' ',price_groups[copy_previous_price_groups[s]].symbol)


                                TRADED_COIN.append(price_groups[copy_previous_price_groups[s]].symbol) 
                                list_buy_sell.append(price_groups[copy_previous_price_groups[s]].to_list("long"))
                        # aynı coin için işleme girmemek adına yapılmış.
                        # elif  TRADED_COIN.count(price_groups[copy_previous_price_groups[s]].symbol) > 0:
                        #     if not order.getOpenOrder(price_groups[copy_previous_price_groups[s]].symbol):
                        #         TRADED_COIN.remove(price_groups[copy_previous_price_groups[s]].symbol)  

                        # to here

                        previous_price_groups.remove(copy_previous_price_groups[s])


            for s in range(show_limit):
                header_printed=False
                if (s<len(sorted_price_group)):
                    max_price_group = sorted_price_group[s]
                    max_price_group = price_groups[max_price_group]
                    if not max_price_group.isPrinted :  
                            if not header_printed:
                                msg = "Top Total Price Change"
                                header_printed = True 
                            str_output = max_price_group.to_string(True) + "\n"
                            print(str_output)
                            list_pump_dump.append(max_price_group.to_list())
                            anyPrinted = True                           
                            previous_price_groups.append(max_price_group.symbol) if max_price_group.symbol not in previous_price_groups else previous_price_groups                   


data_pump_dump = pd.DataFrame(list_pump_dump, columns = ["Symbol", "Event_Time", 
                                                         "Now_Time", "Ticks", 
                                                         "RPCh", "LP", "MinP", "MaxP", "volume", "number_of_trades",
                                                         "LTP", "LTPC",
                                                         "color","order_type"])    
data_buy_sell = pd.DataFrame(list_buy_sell, columns = ["Symbol", "Event_Time", 
                                                         "Now_Time", "Ticks", 
                                                         "RPCh", "LP", "MinP", "MaxP", "volume", "number_of_trades",
                                                         "LTP", "LTPC",
                                                         "color","order_type"])       
# save result  
date_now = datetime.now().strftime("%Y%m%d_%H%M%S")
data_pump_dump.to_pickle("output_pump_dump\\"+date_now)  
data_buy_sell.to_pickle("output_buy_sell\\"+date_now)