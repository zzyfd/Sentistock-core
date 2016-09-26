#-*-coding=utf-8-*-
import  jieba
from emotion import emo
from DBHandler import getDBdata
from collections import OrderedDict
#import CNN.eval
source = "gu8_item"
contents = getDBdata(source)
em = emo("mergedResult")
for stock in contents:
    for date in contents[stock]:
        name = "%s %s"%(stock,date)
        emoV = em.getEmo(contents[stock][date],name)
        if emoV['wnum']:
            expo = emoV['totalV']/emoV['wnum']
            print ([stock,date,expo])