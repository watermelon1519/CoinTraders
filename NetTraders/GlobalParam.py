# coding=utf-8
# Author: Winter_pig 2018-06-27

from NetTraders.tools import *
import ccxt

config = loadCoinfig('./NetTraders/config.json')
api = config['API']
password = config['password']
verbose = config['verbose']
symbol = config['symbol']

#网格交易参数
MaxNets = config['Param']['MaxNets']
Step = config['Param']['Step']
Lot = config['Param']['Lot']

LoopInterval = config['LoopInterval']
MinStock = config['MinStock']

exchange = ccxt.bitz(api)
exchange.password = password
exchange.verbose = verbose

target = symbol  #目标交易对

symbollist = symbol.split('/')
symbolA = symbollist[0]
symbolB = symbollist[1]

LastOrdersLength = None

LoopInterval = max(LoopInterval, 1)
Lot = max(MinStock, Lot)