import datetime as dt
from datetime import datetime, timedelta
import time
from termcolor import colored
 
class PriceGroup:
    def __init__(self, 
            symbol, 
            tick_count,
            total_price_change, 
            relative_price_change,
            last_price,
            last_event_time,
            isPrinted,
            min_price,
            max_price,
            volume,
            number_of_trades,
            trade_type = '',
            last_trade_price = 0.0,
            trade_count = 0,
            change_price_on_last_trade = 0): 
                           
        self.symbol = symbol
        self.tick_count = tick_count 
        self.total_price_change = total_price_change
        self.relative_price_change = relative_price_change
        self.last_price = last_price
        self.last_event_time = last_event_time
        self.isPrinted = isPrinted
        self.min_price = min_price
        self.max_price = max_price
        self.volume = volume
        self.number_of_trades = number_of_trades
        self.last_trade_price = last_trade_price
        self.trade_count = trade_count
        self.trade_type = trade_type
        self.change_price_on_last_trade = change_price_on_last_trade

    def __repr__(self):
        return repr(self.symbol, 
                    self.tick_count, 
                    self.total_price_change, 
                    self.relative_price_change,
                    self.last_price, 
                    self.last_event_time, 
                    self.isPrinted,
                    self.min_price,
                    self.max_price,
                    self.volume,
                    self.number_of_trades,
                    self.trade_type,
                    self.last_trade_price,
                    self.trade_count,
                    self.change_price_on_last_trade)

    def __getitem__(self, key):
        return getattr(self,key)    

    def to_string(self, isColored):
        self.isPrinted = True
        now = datetime.now().time() # time object
        retval = "Symbol:{}\t Event_Time:{}\t Now_Time: {}\t Ticks:{}\t RPCh:{}\t  LP:{}\t  MinP:{}\t MaxP: {}\t Vol: {}\t NoT: {}\t LTP: {}\t LTPC: {}\t".format(
                self.symbol,
                self.last_event_time,
                now,
                self.tick_count,
                "{0:2.2f}".format(self.relative_price_change),              
                self.last_price,           
                self.min_price,
                self.max_price,
                self.volume,
                self.number_of_trades,
                self.last_trade_price,
                self.change_price_on_last_trade)
        
        if (not isColored):
            return retval
        else:
            return colored(retval, self.console_color)

    def to_list(self, order_type = "None"):
        now = datetime.now().time() # time object
        # str_result = ""
        # if (not isColored):
        #     str_result = "pump"
        # else:
        #     str_result = "dump"
        
        retval = [ self.symbol,
                self.last_event_time,
                now,
                self.tick_count,
                self.relative_price_change,              
                self.last_price,           
                self.min_price,
                self.max_price,
                self.volume,
                self.number_of_trades,
                self.last_trade_price,
                self.change_price_on_last_trade,
                self.console_color,
                order_type]
        
        return retval
    
    @property
    def console_color(self):
        if self.relative_price_change < 0:
            return 'red'
        else:
            return 'green'

    @property
    def refresh_datas(self):
        self.tick_count         = 1
        self.total_price_change = 0


    def update_last_trade_price(self, last_trade_price = 0.0, trade_type = '',  is_refresh = False):
        if  is_refresh == False:
            self.last_trade_price = last_trade_price
            self.trade_count = self.trade_count + 1
            self.trade_type = trade_type
        else:
            self.last_trade_price = last_trade_price
            self.trade_count = 0
            self.trade_type = ''
        
        return self.trade_count
        
    @property
    def get_trade_count(self):
        if self.trade_count < 1:
            return True, self.trade_count
        else:
            return False, self.trade_count
    
    @property
    def get_price_change_on_last_trade_price(self):
        self.change_price_on_last_trade =((self.last_price - self.last_trade_price) / self.last_trade_price * 100)
        return self.change_price_on_last_trade 

    @property
    def get_trade_type(self):
        return self.trade_type
