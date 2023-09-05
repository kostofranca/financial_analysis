import datetime as dt
from datetime import datetime, timedelta
import time


class PriceChange:
    def __init__(self, 
                symbol, 
                prev_price, 
                price, 
                isPrinted, 
                event_time, 
                all_prices,
                is_refresh_list,
                volume,
                number_of_trades): 
               
        self.symbol = symbol
        self.prev_price = prev_price
        self.price = price
        self.isPrinted = isPrinted
        self.event_time = event_time
        self.all_prices = []
        self.all_prices.append(all_prices)
        self.is_refresh_list = is_refresh_list
        self.volume = volume
        self.number_of_trades = number_of_trades

    def __repr__(self):
        return repr(self.symbol, 
                    self.prev_price, 
                    self.price, 
                    self.isPrinted, 
                    self.event_time, 
                    self.all_prices,
                    self.is_refresh_list,
                    self.volume,
                    self.number_of_trades)
                
    @property
    def price_change(self):

        # geçmiş veriyi silmek için kullanıyor ama buraya nasıl geliyor onu anlamadım
        if len(self.all_prices) >1200:
            self.all_prices = self.all_prices[600:]
            self.is_refresh_list = True

        if abs(self.price - min(self.all_prices)) > abs(self.price - max(self.all_prices)):
            return self.price - min(self.all_prices)
        else:
            return self.price - max(self.all_prices)

    @property
    def price_change_perc(self):
        if (self.all_prices[-1] == 0 or self.price == 0):
            return 0
        else:
            result_price_change = self.price_change
            if result_price_change > 0:
                return result_price_change / min(self.all_prices) * 100
            else:
                return result_price_change / max(self.all_prices) * 100

    def IsPump(self,lim_perc):
        return self.price_change_perc() >= lim_perc

    def IsDump(self,lim_perc):
        if (lim_perc > 0):
            lim_perc = -lim_perc
            
        return self.price_change_perc() <= lim_perc