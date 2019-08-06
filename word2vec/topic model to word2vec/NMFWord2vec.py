import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017")
mydb = myclient["iiitmkOne"]

table8 = mydb["80topicNMF"]

from gensim.models import Word2Vec
from nltk import *

data = []
for x in table8.find():
    #print(x['keywords'])
    data.append(x['keywords'])
   # for y in x['keywords']:
    #    data.append(y)
print(data)

#data = ["dadas","dasdas"]
#data = all_keywords
model = Word2Vec(data, min_count=1,size= 100,workers=3, window =3, sg = 1)
model.train(data,total_examples=len(data),epochs=20)
#model.wv.save_word2vec_format('nounsRawData1.bin', binary=True)
vocab = model.wv.vocab

count = 0
while(count==0):
    print("Enter input : \n")
    w = input()
    print(model.wv.most_similar(positive=w))
    print(" 1 : for stop \n 0: for again \n")
    count = int(input())