import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017")
mydb = myclient["iiitmkOne"]
table = mydb["rawData"] #blob noun phrases

from gensim.models import Word2Vec
from nltk import *

import re

from sklearn import cluster
import matplotlib.pyplot as plt


def clustering(x):
    kmeans = cluster.KMeans(n_clusters=100)
    kmeans.fit(x)
    labels = kmeans.labels_
    centroids = kmeans.cluster_centers_
    #print(len(labels))
    plt.scatter(x[:,0], x[:,1], c=kmeans.labels_, cmap='rainbow') 
    plt.show()
    return labels

def main():
    all_keywords = []
    for x in table.find():
        all_keywords.append(x['nouns'])
    #print(len(all_keywords))
    data = all_keywords
    model = Word2Vec(data, min_count=1,size= 100,workers=3, window =3, sg = 1)
    model.train(data,total_examples=len(data),epochs=10)
    model.wv.save_word2vec_format('nounsRawData1.bin', binary=True)
    vocab = model.wv.vocab
    c_labels = clustering(model[vocab])
    print(vocab)
    print(len(c_labels))
    print("enter to search :\n")
    w = input()
    #print(model.wv.most_similar(positive=w))
    v1 = model.wv[w]
    print(v1)


main()