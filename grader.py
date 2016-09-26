from Regression import Regression
import pandas as pd
import gc
from collections import OrderedDict
def dump_garbage():
    print("\n garbage")
    gc.collect()
    print("\n garbage object")
    for x in gc.garbage:
        s = str(x)
        if len(s) > 80:
            s = s[:77] + '...'
            #print(type(x), "\b", s)

if __name__ == "__main__":
    # df = dataFetcher("stock_item")
    train_data = pd.read_csv('result.csv')
    # df.get_train_data("gu8_item", date(2016,8,31), date(2016, 9, 14)).groupby(['code', 'date']).sum()
    # print(train_data)
    dic = OrderedDict()
    for i in range(0, len(train_data)):
        print("line: ", i)
        line = train_data.iloc[i]
        #    print(line)
        if line['code'] in dic:
            dic[line['code']][line['date']] = pd.DataFrame({
                'sp': line['sp'],
                'mp': line['wp'],
                'SMB': line['SMB '],
                'HIM': line['HIM'],
                'turnover': line['turnover'],
                'emo': line['emo']}, index=[0])
        else:
            dic[line['code']] = {line['date']: pd.DataFrame({
                'sp': line['sp'],
                'mp': line['wp'],
                'SMB': line['SMB '],
                'HIM': line['HIM'],
                'turnover': line['turnover'],
                'emo': line['emo']}, index=[0])}
    print(dic)
    grade_li = []
    li = []
    stock_count = 0
    grade_count = 0
    buff_count = 0
    re = Regression()
    for code in dic:
        if buff_count > 0:
            buff_count -= 1
            continue
        stock_count += 1
        print('stock counting', stock_count)
        try:
            temp = pd.read_csv('grade/grade' + str(grade_count) + '.csv')
            buff_count += 50
            grade_count += 1
        except:
            li.clear()
            for date in dic[code]:
                df = dic[code][date]
                li.append(df)
            re.LinearR(li)
            new_df = pd.DataFrame({'code': code, 'grade': str(re.mark)}, index=[0])
            dump_garbage()
            grade_li.append(new_df)
            if stock_count >= 50:
                grades = pd.concat(grade_li)
                grade_li.clear()
                grades.to_csv('grade/grade' + str(grade_count) + '.csv')
                grade_count += 1
                print('grade ', grade_count, 'complete')
                stock_count = 0

        #gc.enable()
        #gc.set_debug(gc.DEBUG_LEAK)
    grades = pd.concat(grade_li)
    grades.to_csv('grade/grade' + str(grade_count) + '.csv')
    print("evaluate over")

    gradeFlist = []
    for i in range(0, grade_count):
        df = pd.read_csv('grade/grade' + str(i) + '.csv')
        gradeFlist.append(df)
    grades = pd.concat(gradeFlist)
    grades.to_csv('grade.csv')
    # df = pd.DataFrame({'sp' : 1.0, 'mp' : 1.0 , 'SMB' : 1.0, 'HIM' : 1.0, 'turnover' : 1.0, 'emo' : 1.0}, index= [0])
    # re = Regression(df)

    # def generate_data(self , sp, mp, SMB, HIM, turnover, emo):
