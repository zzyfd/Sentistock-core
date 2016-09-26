#-*-coding=utf-8-*-
from emotion import emo
from collections import OrderedDict
from eval import  getCNNDaata
import pandas as pd
from DBHandler import getStockList
from TuHandler import TuHandler
from datetime import date
class dataFetcher:
    codeList = []
    def __init__(self, listName):
        self.codeList = getStockList(listName)
    def get_emotion(self, source , start, end):
        try:
            return pd.read_csv('emo.csv')
        except:
            pass
        start_str = str(start)
        end_str = str(end)
        posData, negData = getCNNDaata(True, "1472610048" ,source, start_str , end_str)
        em = emo("mergedResult")
        for stock in posData:
            for date in posData[stock]:
                name = "%s %s"%(stock, date)
                emoV = em.getEmo(posData[stock][date], name)
                if emoV['wnum']:
                    expo = emoV['totalV']/emoV['wnum']
                    posData[stock][date] = [posData[stock][date], expo]
                else:
                    posData[stock][date] = [posData[stock][date], 5]
        em.clear()
        for stock in negData:
            for date in negData[stock]:
                name = "%s %s"%(stock, date)
                emoV = em.getEmo(negData[stock][date], name)
                if emoV['wnum']:
                    expo = emoV['totalV']/emoV['wnum']
                    negData[stock][date] = [negData[stock][date], expo]
                else:
                    negData[stock][date] = [negData[stock][date], 5]
        FinalData = OrderedDict()
        for stock in negData:
            for date in negData[stock]:
                FinalData.setdefault(stock, OrderedDict()).setdefault(date, -1)
                expo = 0.0
                try:
                    expo = 0.6*posData[stock][date][1] + 0.4*negData[stock][date][1]
                except KeyError:
                    expo = negData[stock][date][1]
                FinalData[stock][date] = expo
        for stock in posData:
            for date in posData[stock]:
                FinalData.setdefault(stock, OrderedDict()).setdefault(date, -1)
                expo =  FinalData[stock][date]
                if  FinalData[stock][date] == -1:
                    try:
                        expo = 0.6*posData[stock][date][1] + 0.4*negData[stock][date][1]
                    except KeyError:
                        expo = posData[stock][date][1]
                    FinalData[stock][date] = expo
        list = []
        for stock in FinalData:
#            FinalData[stock].setdefault('code', stock)
            for date in FinalData[stock]:
                if date=='code': continue
                d = pd.DataFrame({'emo':FinalData[stock][date], 'code' : stock, 'date' : date}, index=[0])
                list.append(d)
        emo_df = pd.concat(list, axis=0)
        print(emo_df)
        return emo_df
    def get_train_data(self, source = "", start = date.today(), end = date.today()):
        pre_list = []
        turnover_list = []
        tu = TuHandler(self.codeList, start, end)
        self.codeList = tu.stockList
        emo_df  = pd.read_csv('emo.csv')
        SMB_df = pd.read_csv('SMB.csv')
        HIM_df = pd.read_csv('HIM.csv')
        pre_df = pd.read_csv('pre.csv')
        print(pre_df)
        turnover_df = pd.read_csv('turnover.csv')

########emo, SMB, HIM
        '''
        emo_df = self.get_emotion(source, start, end)
        emo_df.to_csv('emo.csv')
        SMB_df = tu.getSMB(self.codeList, start, end)
        SMB_df.to_csv('SMB.csv')
        HIM_df = tu.getHIM(self.codeList, start, end)
        HIM_df.to_csv('HIM.csv')
        '''
########turn, pre
        '''
        for code in self.codeList:
            pre_item = tu.getPremiums(code, start ,end)
            pre_list.append(pre_item)
            turnover_item = tu.getTurnover(code, start, end)
            turnover_list.append(turnover_item)
        pre_df = pd.concat(pre_list)
        pre_df.to_csv('pre.csv')
        turnover_df = pd.concat(turnover_list)
        turnover_df.to_csv('turnover.csv')
        '''
        '''
        result = pd.merge(HIM_df, SMB_df,on= ['date'])
#        print(result, emo_df.reset_index())
        result = pd.merge(emo_df.reset_index(), result, on= ['date'])
        print(result, pre_df)
        result = pd.merge(result, turnover_df, on= ['code', 'date'])
        print(turnover_df.reset_index())
        result = pd.merge(result, pre_df.reset_index(),on= ['code', 'date'])
        result.to_csv('result.csv')
        '''
        result = pd.read_csv('result.csv')
        return result
datafch = dataFetcher('stock_item')
print(datafch.codeList)
print(datafch.get_train_data('gu8_item', date(2016, 8, 31), date(2016, 9, 14)))
#print(datafch.get_emotion('gu8_item', date(2016, 8, 31), date(2016, 8, 31)))
