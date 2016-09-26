#!/usr/bin/python
#-*-coding=utf-8-*-
import json
import jieba
class emo:
    dict = {}
    emoVal = {}
    emodir = "emo_dict"
    def __init__(self,dictname):
        self.dict = self.loadDict(dictname)
    def loadDict(self,dictname):
        path = "./"+self.emodir+"/"+dictname+".json"
        print ("loading "+ path +"......")
        f = open(path, mode='r')
        try:
            js = json.load(f)
            print (["new dictionary loaded!",js])
            f.close()
            return js
        except Exception :
            print (Exception)
    def update(self,dictname):
        new_dict = self.loadDict(dictname)
        for w in new_dict:
            try:
                dict[w].append(new_dict[w])
            except KeyError:
                dict[w] = (dict[w]+new_dict[w])/2.0
    def getEmo(self, txts, name):
        Eval = 0
        wordsNum = 0
        for w in txts:
            if w in self.dict:
                Eval += self.dict[w]
                wordsNum+=1
        if name in self.emoVal:
            self.emoVal[name]['totalV'] += Eval
            self.emoVal[name]['wnum'] += wordsNum
        else:
            self.emoVal[name] = dict(wnum = wordsNum, totalV = Eval)
        return self.emoVal[name]
    def clear(self):
        self.emoVal = {}

#test
#emo = emo("emodata")
#print emo.dict
#txt = "2011年底泽熙在重庆啤酒的抢反弹广为人知，徐翔事后说：“重庆啤酒不是股票，是彩票。第一次刮出来‘谢谢你’，第二次刮出来还是‘谢谢你’，这时候大家都把它当废纸扔了，但彩票还没刮"
#test_txts = jieba.cut(txt)
#print emo.getEmo(test_txts,"重庆啤酒")

