# coding=utf-8
# Author: Winter_pig 2018-06-27


import ccxt
import time
from datetime import datetime
import math

#取消全部委托单
def CancelPendingOrders(exchange,symbol):
    now = datetime.now()
    orders = getOpenOrders(exchange,symbol)
    for order in orders:
        try:
            if ((now - timestamp_datetime(order['timestamp'])).seconds > 10):
                exchange.cancel_order(order['id'], symbol)
            else:
                continue
        except Exception as e:
            print("Cancel Error: {}".format(e))
        else:
            time.sleep(0.5)

#计算下单价格
def GetPrice(exchange,symbol):
    try:
        orderbook = exchange.fetchOrderBook(symbol)
        bid = orderbook['bids'][1][0] if len(orderbook['bids']) > 0 else None
        ask = orderbook['asks'][1][0] if len(orderbook['asks']) > 0 else None
        spread = (orderbook['asks'][0][0]  - orderbook['bids'][0][0])/2 if (bid and ask) else None
        print (exchange.id, 'market price', {'bid': bid, 'ask': ask, 'spread': spread})
        buy_price = bid + spread
        sell_price = ask - spread
        return buy_price, sell_price
    except Exception as e:
        print("GetPrice Error: {}".format(e))
    else:
        return None,None

def GetTickerPrice(exchange,symbol):
    try:
        #orderbook = exchange.fetchOrderBook(symbol)
        #bid = orderbook['bids'][0][0] if len(orderbook['bids']) > 0 else None
        #ask = orderbook['asks'][0][0] if len(orderbook['asks']) > 0 else None
        ticker = exchange.fetch_ticker(symbol)
        bid = ticker['bid']
        ask = ticker['ask']
        spread = (ask  - bid)/2 if (bid and ask) else None
        print (exchange.id, 'market price', {'bid': bid, 'ask': ask, 'spread': spread})
        return bid, ask, spread
    except Exception as e:
        print("GetPrice Error: {}".format(e))
    else:
        return None,None
#timestamp转换成日期
def timestamp_datetime(ts):
     if isinstance(ts, (int, float, str)):
         try:
             ts = int(ts)
         except ValueError:
             raise

         if len(str(ts)) == 13:
             ts = int(ts / 1000)
         if len(str(ts)) != 10:
             raise ValueError
     else:
        raise ValueError()
     return datetime.fromtimestamp(ts)

def getAccount(exchange):
    try:
        account = exchange.fetchBalance()
        return account
    except Exception as e:
        print("getAccount Error: {}".format(e))
    else:
        time.sleep(3)
        return getAccount(exchange)

def getOpenOrders(exchange, symbol):
    try:
        orders = None
        orders = exchange.fetchOpenOrders(symbol)
        return orders
    except Exception as e:
        print("getOpenOrders Error: {}".format(e))
    else:
        time.sleep(3)
        return getOpenOrders(exchange,symbol)

def adjustFloat(v):
    return math.floor(v*100)/100
