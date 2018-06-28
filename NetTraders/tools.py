# coding=utf-8
# Author: Winter_pig 2018-06-27

import json as js

def loadCoinfig(path):
    try:
        configFile = file(path)
        return js.load(configFile)
    except Exception as e:
        print("Load config file Error: {}".format(e))
    else:
       print('nothing')


