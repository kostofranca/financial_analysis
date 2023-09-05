import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, time

output_path = "output_pump\\20230420_123706_output.txt" 
names = ["Symbol", "Event_Time", "Now_Time", "Ticks", "RPCh", "LP", "MinP", "MaxP", "LTP", "LTPC"]
data_dummy = pd.read_csv(output_path, sep = "\t", header=None)


data = pd.DataFrame()
data["Symbol"] = [i.split(":")[-1] for i in data_dummy.iloc[:,0]]
data["Event_Time"] = [datetime.strptime(i.replace("Event_Time:","").strip(), "%Y-%m-%d %H:%M:%S.%f")  for i in data_dummy.iloc[:,1]]
data["Now_Time"] = [datetime.strptime(i.replace("Now_Time:","").strip(), "%H:%M:%S.%f").time() for i in data_dummy.iloc[:,2]]
data["Ticks"] = [int(i.split(":")[-1]) for i in data_dummy.iloc[:,3]]
data["RPCh"] = [float(i.split(":")[-1]) for i in data_dummy.iloc[:,4]]
data["LP"] = [float(i.split(":")[-1]) for i in data_dummy.iloc[:,5]]
data["MinP"] = [float(i.split(":")[-1]) for i in data_dummy.iloc[:,6]]
data["MaxP"] = [float(i.split(":")[-1]) for i in data_dummy.iloc[:,7]]
data["LTP"] = [float(i.split(":")[-1]) for i in data_dummy.iloc[:,8]]
data["LTPC"] = [float(i.split(":")[-1]) for i in data_dummy.iloc[:,9]]

"""
RPCh: relative_price_change
LP: last_price
MinP: min_price
MaxP: max_price
LTP: last_trade_price
LTPC: change_price_on_last_trade
"""
value_count = data["Symbol"].value_counts()
value_index = value_count.index
counts = value_count.tolist()
for i in range(len(value_count)):
    symbol = value_index[i]
    title = "Symbol: {}, Value Count: {}".format(symbol, counts[i])
    
    series = data[data.Symbol == symbol]
    print(title)
    plt.figure()
    plt.scatter(series.Event_Time, series.RPCh)
    plt.grid(True)
    plt.title(title)



















