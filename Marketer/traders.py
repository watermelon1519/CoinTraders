# coding=utf-8
# Author: Winter_pig 2018-06-27


import ccxt
import time
from datetime import datetime

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

def my_create_limit_order(type, symbol, amount, price):
    if exchange.has['createLimitOrder']:
        if type == 'ORDER_TYPE_BUY' :
            myorder = exchange.create_limit_buy_order(symbol, amount, price)
            return myorder
        if type == 'ORDER_TYPE_SELL':
            myorder = exchange.create_limit_sell_order(symbol, amount, price)
            return myorder
    else:
        return None

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
        orders = exchange.fetchOpenOrders(symbol)
        return orders
    except Exception as e:
        print("getOpenOrders Error: {}".format(e))
    else:
        time.sleep(3)
        return getOpenOrders(exchange,symbol)

def onTick():
    account = getAccount(exchange)
    if( account == None):
        print('account is none')
        return
    orders = getOpenOrders(exchange,target)
    if( orders == None):
        print('orders is none')
        return
    #更新收益
    #if( LastOrdersLength <> None && LastOrdersLength <> len(orders) ):
    #    print("ha")

    LastOrdersLength = len(orders)

    buy_price, sell_price = GetPrice(exchange,target)
    print (exchange.id, 'My price', {'buy_price': buy_price, 'buy_price': sell_price})
    CancelPendingOrders(exchange, target)
    amountBuy = round( account[symbolB]['free'] / buy_price - 0.1 , 2)
    amountSell = round((account[symbolA]['free']), 2);

    print (exchange.id, 'My Amount', {'amountBuy': amountBuy, 'amountSell': amountSell})

    if (amountSell > min_sellAmount) :
        amountSell = max( 0.1 , amountSell )
        try:
            myorder = exchange.create_limit_sell_order(target, amountSell, sell_price)
        except Exception as e:
            print("create_limit_sell_order Error: {}".format(e))
        else:
            time.sleep(0.5)
    if (amountBuy > min_buyAmount) :
        amountBuy = max(0.1, amountBuy)
        try:
            myorder = exchange.create_limit_buy_order(target, amountBuy, buy_price)
        except Exception as e:
            print("create_limit_buy_order Error: {}".format(e))
        else:
            time.sleep(0.5)
    #休眠，进入下一轮循环
    time.sleep(7)




#API的账户密码，后面把他移到外面的json串里去
exchange = ccxt.bitz({
    'apiKey': 'x446e725f166e40a22e37a4d54f7e8553',
    'secret': 'FROYKE93dipQ6C9LwySapZNeyJTn3zKcJ2UvEqeTJK2xrha5M7L8qG0zEN4kFpj3B',
})
exchange.password = '@@@@@'
exchange.verbose = True

symbolA = 'ETH'
symbolB = 'USDT'
target = symbolA + '/' + symbolB
LastOrdersLength = None


#检测一下该站点支持的API
exchange.describe()

#我自己的订单列表
myOrdersDict = {}

min_sellAmount = 0.01
min_buyAmount =0.01

while True:
    onTick()


