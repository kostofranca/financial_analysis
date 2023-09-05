import json
import datetime as dt
from datetime import datetime, timedelta
import time
import os
import operator
from termcolor import colored
from binance.client import Client
from binance.enums import *
from binance.streams import BinanceSocketManager
from pricechange import *
from binanceHelper import *
from pricegroup import *
#from binance.futures import Futures  as Client
import order
import config
import websocket, json
import keyboard
import threading
import datetime 

SOCKET = "wss://stream.binance.com:9443/ws/!ticker@arr"  # spot
# SOCKET = "wss://fstream.binance.com/ws/!ticker@arr"  # futures
#SOCKET = "wss://stream.binancefuture.com/ws/!ticker@arr"    #testnet
show_only_pair = "USDT" #Select nothing for all, only selected currency will be shown,

show_limit = 2      #minimum top query limit
min_perc = 0.005  #min percentage change
price_changes = []
price_groups = {}

TRADED_COIN = []       

previous_price_groups = []
copy_previous_price_groups = []

output_path = "output_pump\\" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + "_output.txt"
list_real_data = []

# def main():
    
def on_open(ws):
    print('opened connection')

def on_close(ws,close_status,close_message):
    print('close connection')
    print(close_status, '  ', close_message)

def on_error(ws,message):
    print(message)

def on_message(ws,message):
    print("on_message")
    global TRADED_COIN
    global output_file_name

    json_message = json.loads(message)
    
    # price_changes listesinin icerisine PriceChange sınıfına ait nesneleri ekliyor.
    for ticker in json_message: # json_message is a list that includes dictionaries.
        symbol = ticker['s']
        if ('BTCUSDT' in symbol and  not 'BUSDT' in symbol):  
            list_real_data.append(ticker)
            price = float(ticker['c']) # Last price
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
                    price_change.isPrinted = False
                    price_change.is_refresh_list = False
                else:
                    price_changes.append(PriceChange(symbol, price, price,  False, event_time, price, False))
            else:
                price_changes.append(PriceChange(symbol, price, price, False, event_time, price, False))

    price_changes.sort(key=operator.attrgetter('price_change_perc'), reverse=True)
        
    for price_change in price_changes:
        
        console_color = 'green'
        temp_price_change  = price_change.price_change_perc
        if  temp_price_change < 0:
            console_color = 'red'

        if (not price_change.isPrinted and abs(temp_price_change) >= min_perc) :

            price_change.isPrinted = True 
            
            if not price_change.symbol in price_groups:
                price_groups[price_change.symbol] = PriceGroup(price_change.symbol,                                                                
                                                            1,                                                                
                                                            abs(temp_price_change),
                                                            temp_price_change,                                                            
                                                            price_change.price,                                                                                                                             
                                                            price_change.event_time,
                                                            False,
                                                            min(price_change.all_prices),
                                                            max(price_change.all_prices))
            else:
                # Eğer anlık fiyat şimdiye kadar gelen fiyatların maksimum değerinin 0.998 katından büyükse yada
                # anlık fiyat şimdiye kadar gelen fiyatların minimum değerinin 1.002 katından küçükse
                # tutulan verinin son fiytı güncelleniyor (burada her veri tutulmasın diye basit bir kural eklenmiş)
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
                        
                        # #  if you dont want to create order, comment line start from here 

                        # if (not TRADED_COIN.count(price_groups[copy_previous_price_groups[s]].symbol) > 0  and not order.getOpenOrder())  and order.isAnyLiquidation():

                        #     if price_groups[copy_previous_price_groups[s]].relative_price_change > 0: 
                        #         order.enterShortOrder(symbol = price_groups[copy_previous_price_groups[s]].symbol
                        #                             ,price =  price_groups[copy_previous_price_groups[s]].last_price   
                        #                             ,type = 'MARKET')
                                    
                        #         explanation = 'Enter Short ' 
                        #         print(explanation, ' ',price_groups[copy_previous_price_groups[s]].symbol)
                                
                                
                        #         TRADED_COIN.append(price_groups[copy_previous_price_groups[s]].symbol)
                        #     else:                                        
                        #         order.enterLongOrder(symbol = price_groups[copy_previous_price_groups[s]].symbol
                        #                             ,price = price_groups[copy_previous_price_groups[s]].last_price   
                        #                             ,type = 'MARKET')     
                                    
                        #         explanation = 'Enter Long '                                  
                        #         print(explanation, ' ',price_groups[copy_previous_price_groups[s]].symbol)


                        #         TRADED_COIN.append(price_groups[copy_previous_price_groups[s]].symbol) 
                        
                        ## aynı coin için işleme girmemek adına yapılmış.
                        # elif  TRADED_COIN.count(price_groups[copy_previous_price_groups[s]].symbol) > 0:
                        #     if not order.getOpenOrder(price_groups[copy_previous_price_groups[s]].symbol):
                        #         TRADED_COIN.remove(price_groups[copy_previous_price_groups[s]].symbol)  

                        # # to here

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
                            with open(output_path, 'a') as file:
                                file.write(str_output)
                                # for zz in range(len(sorted_price_group)):
                                #     file.write(sorted_price_group[zz] + " - ")
                                # file.write("\n")
                            anyPrinted = True                           
                            previous_price_groups.append(max_price_group.symbol) if max_price_group.symbol not in previous_price_groups else previous_price_groups                   
     
        if anyPrinted:
            print("")
    
# Klavye olayını dinleyen fonksiyon
def check_keyboard_event(event):
    if event.name == 'q':  # 'q' tuşuna basıldığında
        ws.close()  # WebSocket bağlantısını kapat
        
def start_websocket():
    ws.run_forever()
    print("run_forever done")

ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message , on_error=on_error)
ws.run_forever()

# Klavye olayını dinlemeye başla
# keyboard.on_press(check_keyboard_event)
    
# WebSocket'i başlatan iş parçacığını başlat
# with open(dosya_adı, "a") as dosya:
#     websocket_thread = threading.Thread(target=start_websocket)
#     websocket_thread.start()
    
        

# keyboard.wait()

  
# if __name__ == '__main__':
#     main()
