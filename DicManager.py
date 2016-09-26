import os
from gensim import corpora, models, similarities
def getFileList(dir):
    return [ dir + x for x in os.listdir(dir)]
if not os.path.exists('dict'):
    os.mkdir("dict")
dictLists = getFileList('./dict/')
class LoadDictionary(object):
    def __init__(self, dictionary):
        self.dictionary = dictionary
    def __iter__(self):
        for dictFile in dictLists:
            sFileRaw, sFilePostfix = os.path.splitext(dictFile)
            sFileDir, sFileName = os.path.split(sFileRaw)
            (dictFile, corpusFile) = ( './dict/' + sFileName + '.dict',  './corpus/'+sFileName + '.mm')
            yield self.dictionary.load( './dict/' + sFileName + '.dict',  './corpus/'+sFileName + '.mm');
            #yield self.dictionary.load_from_text(dictFile)
class LoadCorpus(object):
    def __iter__(self):
        for dictFile in dictLists:
            sFileRaw, sFilePostfix = os.path.splitext(dictFile)
            sFileDir, sFileName = os.path.split(sFileRaw)
            (dictFile, corpusFile) = ( './dict/' + sFileName + '.dict',  './corpus/'+sFileName + '.mm')
            yield corpora.MmCorpus(corpusFile)
