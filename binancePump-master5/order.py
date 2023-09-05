
from binance.client import Client as Client
import config
from decimal import Decimal
from binance.helpers import round_step_size

client = Client(config.API_KEY, config.API_SECRET, tld = 'com')


MONEY = 100     
PRECISION = 0

def enterLongOrder(symbol, price, type='LIMIT'):
    
    print('Enter Long Order')
    changeLeverage(symbol=symbol, leverage = 4)
    changeMarginType(symbol=symbol)
    quantity = getQuantity_V2(symbol=symbol, price=price) 

    if type == 'LIMIT':
        client.futures_create_order(symbol = symbol 
                                            ,side = 'BUY'
                                            ,type = 'LIMIT' 
                                            ,price =  price
                                            ,quantity  = quantity
                                            ,timeInForce = 'GTC')
    else:
        result = client.futures_create_order(symbol = symbol 
                                            ,side = 'BUY'
                                            ,type = 'MARKET' 
                                            ,quantity  = quantity)

    quantity, price_func = getCompletedOrderInfo(symbol, result['orderId'])  

    exitLongOrder(symbol=symbol, price=price_func, quantity=quantity)
    return quantity
###################################################################################################################################################

def exitLongOrder(symbol, price, quantity):
    print('EXIT Long Order')
    leverage = 4
    #changeLeverage(symbol=symbol, leverage=leverage)   not required already changed
    changeMarginType(symbol=symbol)

    stopPrice = float(price) * 1.0025
    x = getQuantity_V3(symbol=symbol)
    stopPrice = round_step_size(stopPrice,x)

    """ order_id = 0
    while order_id == 0:
        try: """
    result = client.futures_create_order(symbol = symbol 
                                    ,side = 'SELL'
                                    ,type = 'LIMIT' 
                                    ,price =  stopPrice
                                    ,quantity  =   quantity 
                                    ,timeInForce = 'GTC')
    print(result['orderId'])
    """         order_id = result['orderId']
        except:
            print("try to exit order ") """


###################################################################################################################################################
def enterShortOrder(symbol, price, type='LIMIT'):
    print('Enter Short Order')
    changeLeverage(symbol=symbol, leverage=4)
    changeMarginType(symbol=symbol)
    quantity = getQuantity_V2(symbol=symbol, price=price) 
    if type == 'LIMIT':
        result = client.futures_create_order(symbol = symbol 
                                        ,side = 'SELL'
                                        ,type = 'LIMIT' 
                                        ,price =  price
                                        ,quantity  = quantity
                                        ,timeInForce = 'GTC')
    else:
        result = client.futures_create_order(symbol = symbol 
                                        ,side = 'SELL'
                                        ,type = 'MARKET' 
                                        ,quantity  = quantity)

    quantity, price_func = getCompletedOrderInfo(symbol, result['orderId'])
    
    exitShortOrder(symbol=symbol, price=price_func, quantity= quantity)
    return quantity
###################################################################################################################################################

def exitShortOrder(symbol, price, quantity):
    print('EXIT Short Order')
    leverage = 4
    #changeLeverage(symbol=symbol, leverage=leverage) not required already changed
    changeMarginType(symbol=symbol)
    
    stopPrice = float(price) * 0.9975
    x = getQuantity_V3(symbol=symbol)
    stopPrice = round_step_size(stopPrice,x)

    """ order_id = 0
    while order_id == 0:
        try:
    """
    result = client.futures_create_order(symbol = symbol 
                                    ,side = 'BUY'
                                    ,type = 'LIMIT' 
                                    ,price =  stopPrice
                                    ,quantity  = quantity
                                    ,timeInForce = 'GTC')
    print(result['orderId'])        
    """         order_id = result['orderId']
        except:
            print("try to exit order") """


###################################################################################################################################################

def changeLeverage(symbol, leverage=15):
    client.futures_change_leverage(symbol=symbol, leverage=leverage)

###################################################################################################################################################

def changeMarginType(symbol, marginType='ISOLATED'):  
    try:
        client.futures_change_margin_type(symbol=symbol, marginType=marginType)  # CROSSED
    except Exception as e:
        print("an exception occured - {}".format(e))


###################################################################################################################################################

def getQuantity_V2(symbol, price):  

    info = client.futures_exchange_info()
    info = info['symbols']
    
    for i in range(0,len(info)):   
        if info[i]['pair'] == symbol:
            PRECISION = info[i]['quantityPrecision'] 
            quantity  = (float(MONEY)/float(price))
            return round(quantity, PRECISION) 

def getQuantity_V3(symbol):  
    info = client.futures_exchange_info()
    
    for item in info['symbols']:
        if(item['symbol'] == symbol):
            for f in item['filters']:
                if f['filterType'] == 'PRICE_FILTER':
                
                    return   float(f['tickSize'])

###################################################################################################################################################
  
def getCompletedOrderInfo(symbol, orderId):
    orderInfo = client.futures_account_trades(symbol=symbol, orderId=orderId) 
    totalQuantity = 0.0
    price = 0.0

    if len(orderInfo) > 0:
        for i in range(0,len(orderInfo)):
            totalQuantity = totalQuantity + float(orderInfo[i]['qty']) 
            price = orderInfo[i]['price']

    return totalQuantity, price

###################################################################################################################################################

def getOpenOrder(symbol=''):
    if symbol != '':
        result = client.futures_get_open_orders(symbol = symbol)
        return len(result) > 0
    else:
        result = client.futures_get_open_orders()
        return len(result) > 0


def isAnyLiquidation():
    result = client.futures_liquidation_orders()
    result_time = result[-1]['time']
    result_time = int(result_time)

    now = 1656004367849 # 23 June 2022 20:12:47   https://www.timecalculator.net/milliseconds-to-date

    if now > result_time:
        return True
    else:
        return False

