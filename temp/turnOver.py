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
         '000036',
         '000037']


import pandas as pd
import tushare as ts
list = []
for code in codes:
    d = ts.get_hist_data(code, start='2015-01-01', end='2015-12-31')[['turnover']]
    list.append(d)

result = pd.concat(list, axis=0)
print (result.reset_index().groupby('date').apply(lambda x:[x.head(9).mean(), x.tail(9).mean()]))
