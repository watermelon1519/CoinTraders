# coding=utf-8
# Author: Winter_pig 2018-06-27

from NetTraders.utils import *
from NetTraders.type import *
from NetTraders.globalParam import *


#网格交易策略
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

    bid, ask, spread = GetTickerPrice(exchange, target)
    mid = adjustFloat(bid + spread)
    numBuy = int(min(MaxNets / 2, (mid - bid) / Step,  account[symbolB]['free'] / bid / Lot))
#    numBuy = int(min(MaxNets / 2,  account[symbolB]['free'] / bid / Lot))
    numSell = int(min(MaxNets / 2, account[symbolA]['free'] / Lot))
    num = max(numBuy, numSell)
    print (exchange.id, 'My Amount', {'numBuy': numBuy, 'numSell': numSell})

    ordersKeep = []
    queue = []
    for i in range(num):
        buyPrice = adjustFloat(mid - (i * Step))
        sellPrice = adjustFloat(mid + (i * Step))
        alreadyBuy = False
        alreadySell = False
        for j in range( len(orders) ):
            if (orders[j]['side'] == ORDER_TYPE_BUY) :
                if (math.fabs( float(orders[j]['price']) - buyPrice) < (Step / 2)) :
                    alreadyBuy = True
                    ordersKeep.append(orders[j]['id'])
            else:
                if (math.fabs(float(orders[j]['price']) - sellPrice) < (Step / 2)) :
                    alreadySell = True
                    ordersKeep.append(orders[j]['id'])

        if ((alreadyBuy == False) and (i < numBuy)) :
            queue.append([buyPrice, ORDER_TYPE_BUY])

        if ((alreadySell == False) and (i < numSell)) :
            queue.append([sellPrice, ORDER_TYPE_SELL])

    for i in range(len(orders)):
        keep = False
        for j in range( len(ordersKeep)):
            if (orders[i]['id'] == ordersKeep[j]) :
                keep = True

        if ( keep==False ):
            try:
                exchange.cancel_order(orders[i]['id'], target)
                LastOrdersLength = LastOrdersLength - 1
            except Exception as e:
                print("cancel_order Error: {}".format(e))


    for i in range( len(queue)):
        if (queue[i][1] == ORDER_TYPE_BUY) :
            try:
                exchange.create_limit_buy_order(target, Lot, queue[i][0])
            except Exception as e:
                print("create_limit_buy_order Error: {}".format(e))
        else:
            try:
                exchange.create_limit_sell_order(target, Lot, queue[i][0])
            except Exception as e:
                print("create_limit_sell_order Error: {}".format(e))

        LastOrdersLength  = LastOrdersLength + 1



if __name__ == '__main__':
    while True:
        onTick()
        time.sleep(LoopInterval)


