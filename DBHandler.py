#-*-coding=utf-8-*-
import os
import sys
import pymysql
#from gensim import corpora,models,similarities
from collections import OrderedDict
def getDBdata(sFileName,start, end):
    conn = pymysql.connect(
        host = 'localhost',
        port = 3306,
        user = 'root',
        passwd = '123',
        db = 'weibo',
        charset = 'utf8'
    )
    cur = conn.cursor()
    #sFileName = "gu8_item"
    num = cur.execute("select * from "+sFileName+" where time between '"+start+"' and '"+end+"' ")
    print (num)
    #info 0:stock 1:id 2:favor 3:title 4:time 5:forward 6:content 7:user
    infos = cur.fetchmany(num)
    #for i in infos:
    #    print i[6]
    if len(infos) > 0:
        if not os.path.exists('dict'):
            os.mkdir("dict")
        if not os.path.exists('corpus'):
            os.mkdir("corpus")
        contents = OrderedDict()
        all_content = ""
        for info in infos:
            #print (info[0])
            hFile = None
            contents.setdefault(info[0], OrderedDict()).setdefault(info[4], "");
            contents[info[0]][info[4]] += info[6]
        cur.close()
        conn.commit()
        conn.close()
        return contents
def getDBdataList(sFileName, start, end):
    conn = pymysql.connect(
        host = 'localhost',
        port = 3306,
        user = 'root',
        passwd = '123',
        db = 'weibo',
        charset = 'utf8'
    )
    cur = conn.cursor()
    #sFileName = "gu8_item"
    #cur.execute("update "+ sFileName + " set time = date(time) ;")
    num = cur.execute("select * from "+sFileName+" where time between '" +start+ "' and '" + end +"' ;")
    print (num)
    #info 0:stock 1:id 2:favor 3:title 4:time 5:forward 6:content 7:user
    infos = cur.fetchmany(num)
    #for i in infos:
    #    print i[6]
    if len(infos) > 0:
        if not os.path.exists('dict'):
            os.mkdir("dict")
        if not os.path.exists('corpus'):
            os.mkdir("corpus")
        contents = OrderedDict()
        for info in infos:
            #print (info[0])
            contents.setdefault(info[0], OrderedDict()).setdefault(info[4], []);
            contents[info[0]][info[4]].append(info[6])
        cur.close()
        conn.commit()
        conn.close()
        return contents

def getDBAllData(sFileName, start, end):
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='123',
        db='weibo',
        charset='utf8'
    )
    cur = conn.cursor()
    # sFileName = "gu8_item"
    #cur.execute("update " + sFileName + " set time = date(time) ;")
    num = cur.execute("select * from " + sFileName + " ;")
    print(num)
    infos = cur.fetchmany(num)
    contents = []
    for info in infos:
        contents.append({'code':info[0], 'total':info[6], 'pb':info[13]})
    cur.close()
    conn.commit()
    conn.close()
    return contents

def getStockList(sFileName):
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='123',
        db='weibo',
        charset='utf8'
    )
    cur = conn.cursor()
    # sFileName = "gu8_item"
    # cur.execute("update " + sFileName + " set time = date(time) ;")
    num = cur.execute("select code from " + sFileName + " ;")
    print("get stock list:", num)
    infos = cur.fetchmany(num)
    contents = []
    for info in infos:
        contents.append(info[0])
    cur.close()
    conn.commit()
    conn.close()
    return contents
#print(getStockList('stock_item'))
'''
    fileFenci = [ x for x in jieba.cut(' '.join(all_content),cut_all=True)]
    fileFenci2 = [word for word in fileFenci if not word in punctuations]
    texts = [fileFenci2]
    all_tokens = sum(texts, [])
    tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word) == 1)
    texts = [[word for word in text if word not in tokens_once] for text in texts]
    sFileDir, sFileName = os.path.split(sFileName)
    dictFileName = 'dict/'+sFileName+'.dict'
    corpusFileName = 'corpus/'+sFileName+'.mm'
    dictionary = corpora.Dictionary(texts)
    dictionary.save_as_text(dictFileName)
    corpus = ([dictionary.doc2bow(text) for text in texts])
    corpora.MmCorpus.serialize(corpusFileName, corpus)
print 'Build corpus over'
'''
