import tushare as ts
from datetime import date,timedelta
import pandas as pd
import DBHandler as dh
from collections import  OrderedDict
class TuHandler:
    empty_list = []
    stockList = []
    start = date.today()
    end = date.today()
    hist_cache= {}
    def initHist(self, stockList, start , end):
        '''
        start_str = str(start)
        end_str = str(end)
        for code in stockList :
            print(code, ' hist initialed')
            data =  ts.get_hist_data(code=code, start=start_str, end = end_str, retry_count=10 )
            self.hist_cache.setdefault('code' , data)
            '''
        start_str = str(start)
        end_str = str(end)
        for code in stockList:
            try:
                print(code, ' hist initialed')
                data = pd.read_csv('csv/' + code + '.csv')
                data = data.set_index(['date'])
                if len(data) == 11:
                    self.hist_cache.setdefault(code, data)
                    self.stockList.append(code)
            except:
                self.empty_list.append(code)
                continue
        self.hist_cache.setdefault('sz', ts.get_hist_data(code='sz', start=start_str, end=end_str, retry_count=10))
        self.hist_cache.setdefault('sh', ts.get_hist_data(code='sz', start=start_str, end=end_str, retry_count=10))
        self.stockList.append('sz')
        self.stockList.append('sh')

    def __init__(self,stockList,start,end):

        self.start = start
        self.end = end
        self.initHist(stockList, start, end)
#        self.hist_cache = pd.read_csv('sql_daily.csv')
        print('cache hist', len(self.hist_cache))

    def get_hist_data(self, code, start, end, retry_count = 10):

        if code in self.hist_cache:
            try:
#                print(self.hist_cache[code])
                return self.hist_cache[code].loc[end:start]
            except:
                self.empty_list.append(code)
                raise KeyError (" empty!")

        else:
            try:
                print('retry get hist')
                data = ts.get_hist_data(code=code, start=start, end=end, retry_count=retry_count)
                self.hist_cache.setdefault('', data)
                return data
            except:
                self.empty_list.append(code)
                raise KeyError (" empty!")
    def valid_minus(self, end):
        if end.weekday() in range(1,5):
            return [end-timedelta(days=1), end]
        if end.weekday() ==5:
            return [end-timedelta(days=2), end-timedelta(days=1)]
        if end.weekday() == 6:
            return [end-timedelta(days=3), end-timedelta(days=2)]
        if end.weekday() == 0:
            return [end-timedelta(days=3), end]
        else:
            raise ValueError("weekday out of bound")

    def getRate(self,start, end):
        '''
        start_str = str(start)
        end_str = str(end)
        deposit = pd.DataFrame([])
        while (deposit.empty):
            try:
                deposit = ts.get_deposit_rate()
            except:
                pass
        curr_rate = date(1970, 1, 1)
        diff = 1000
        for de in deposit['date']:
            dedate = date(int(de[0:4]), int(de[5:7]), int(de[8:]))
            if diff > (start - dedate).days and start > dedate:
                diff = (start - dedate).days
                curr_rate = dedate
                #    print(deposit.groupby(['date', 'deposit_type']).sum())
        rate = deposit.groupby(['date', 'deposit_type']).sum().loc[str(curr_rate)].loc['定期存款整存整取(一年)']
        '''
        rate = 1.5
        return rate

    def getSinPremium(self,code, end):
        stockList = self.stockList
        start, end = self.valid_minus(end)
        start_str = str(start)
        end_str = str(end)
        op1 = self.get_hist_data(code = code, start = start_str, end= start_str, retry_count=10)
        op2 = self.get_hist_data(code = code, start = end_str, end = end_str, retry_count=10)
        change = (op2['open'].loc[end_str] - op1['open'].loc[start_str])/op2['open'].loc[end_str]
        rate = float(self.getRate(start, end))
        return change - rate
    def getMarketPremium(self,code,end ):
        expo = 0.0
        start, end = self.valid_minus(end)
        start_str = str(start)
        end_str = str(end)
        if code[0] == '0' or  code[0] =='3':
            op1 = self.get_hist_data(code='sz', start=start_str, end=start_str, retry_count=10)
            op2 = self.get_hist_data(code='sz', start=end_str, end=end_str, retry_count=10)
            expo = (op2['open'].loc[end_str] - op1['open'].loc[start_str])/op2['open'].loc[end_str]
        elif code[0] == '6':
            op1 = self.get_hist_data(code='sh', start=start_str, end=start_str, retry_count=10)
            op2 = self.get_hist_data(code='sh', start=end_str, end=end_str, retry_count=10)
            expo = (op2['open'].loc[end_str] - op1['open'].loc[start_str])/op2['open'].loc[end_str]
        else:
            return "invalid code"
        rate = float(self.getRate(start, end))
        return expo - rate
    def getSMB(self,stockList, start, end):
        stockList = self.stockList
        print('get SMB')
        empty_list = []
        list = []
        start_str = str(start)
        end_str = str(end)
        lenth = len(stockList)
        stock_info = dh.getDBAllData('stock_item', str(start), str(end))
        stock_df = pd.DataFrame(stock_info)
        stif = stock_df.groupby('code').mean()
        for stock in stockList:
            if stock in self.empty_list:
                continue
            try:
                print('smb : ', stock)
                op = self.get_hist_data(code=stock, start=start_str, end=end_str, retry_count=10)
                op = op[['open', 'close']]
                d = (op['open'] - op['close'])/op['open']
                d = pd.DataFrame({'diff': d , 'code': stock})
        #        print(d.reset_index(), stif)
                d = pd.merge(d.reset_index(), stif,left_on='code',right_index=True, how='inner' )
        #        print(d.reset_index(), op.reset_index())
                d = pd.concat([d.reset_index(), op.reset_index()[['open', 'close']]], axis=1)
        #       print("final d ", d)
                list.append(d)
            except :
                continue
        result = pd.concat(list, axis=0)
        result['total'] = result['total']*result['open']
    #    print(result)
        return pd.DataFrame({'SMB ':result.groupby(['date']).apply(lambda x: x.sort_values(by='total').tail(int(lenth/3)).mean()- x.sort_values(by='open').head(int(lenth/3)).mean())['diff']})

    def getHIM(self,stockList, start, end):
        stockList = self.stockList
        print('get HIM')
        list = []
        empty_list = []
        start_str = str(start)
        end_str = str(end)
        lenth = len(stockList)
        stock_info = dh.getDBAllData('stock_item', str(start), str(end))
        stock_df = pd.DataFrame(stock_info)
        stif = stock_df.groupby('code').mean()
        for stock in stockList:
            if stock in self.empty_list:
                continue
            try:
                print('him : ', stock)
                op = self.get_hist_data(code=stock, start=start_str, end=end_str, retry_count=10)
                op = op [['open', 'close']]
                d = (op['open'] - op['close']) / op['open']
                d = pd.DataFrame({'diff': d, 'code': stock})
                d = pd.merge(d.reset_index(), stif, left_on='code', right_index=True, how='inner')
                d = pd.merge(d.reset_index(), op.reset_index(), on='date')
                list.append(d)
            except:
                continue
        result = pd.concat(list, axis=0)
        result['pb'] = 1.0/result['pb']
    #    print(result)
        return pd.DataFrame({'HIM' :result.groupby(['date']).apply(
            lambda x: x.sort_values(by='pb').tail(int(lenth / 3)).mean() - x.sort_values(by='open').head(
                int(lenth / 3)).mean())['diff']})
    def getTurnover(self,code, start, end):
        if code in self.stockList:
            try:
                print('get turnover ', code)
                start_str = str(start)
                end_str = str(end)
                op = self.get_hist_data(code=code, start=start_str, end=end_str,retry_count=10).reset_index()
                df = pd.concat([ op[['turnover', 'date']],pd.DataFrame({'code' : code, }, index=op.index)], axis=1)
                #    print(df['code'])
            except :
                return
            return df
        else:
            return

    def getPremiums(self,code, start, end):
        if code  in self.stockList:
            print('get premiums ', code)
            curr = start
            list = []
            while(curr < end):
                curr = curr+timedelta(days=1)
                #print(curr)
                sp = self.getSinPremium(code, curr)
                wp = self.getMarketPremium(code, curr)
                list.append(OrderedDict({'id' : 0, 'sp' : sp, 'wp': wp,  'date' : str(curr), 'code' :str(code)}))
            df = pd.DataFrame(list)
            return df
        else:
            return
#print(getSinPremium('000001', date(2016,8,31)))
#print(getMarketPremium('000001', date(2016,8,31)))

codes = ['000001',
         '000002',
         '000006',
         '000007',
         '000008',
         '000009',
         '000011',
         '000012',
         '000014',
         '000016',
         '000017',
         '000018',
         '000019',
         '000021',
         '000022',
         '000023',
         '000025',
         '000026',
         '000027',
         '000028',
         '000029',
         '000030',
         '000031',
         '000032',
         '000034',
         '000036']
#print('HIM', getHIM(codes, date(2016, 8, 31), date(2016, 9, 14)))
#print('SMV',getSMB(codes, date(2016, 8, 31), date(2016, 9, 14)))
#print('turnover',getTurnover('000001', date(2016,8,31), date(2016,9,14)))
#print('premiums', getPremiums('000001',date(2016,8,31), date(2016,9,14) ))