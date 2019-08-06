import pandas as pd 
from gensim.models import Word2Vec
import pymongo
from nltk import *

import re

from sklearn import cluster
import matplotlib.pyplot as plt

myclient = pymongo.MongoClient("mongodb://localhost:27017")
mydb = myclient["iiitmkOne"]
table = mydb["rawData"] #blob noun phrases
def replace(x):
    regex = re.compile('[^a-zA-Z ]')
    x = regex.sub('', x)
    return x

def get_nounTags():
    data = []
    for x in table.find():
        temp = []
        #data.append(x['nouns'])
        for y in x["nouns"]:
            t = replace(y)
            temp.append(y)
        data.append(temp)
    return data


def clustering(x):
    kmeans = cluster.KMeans(n_clusters=100)
    kmeans.fit(x)
    labels = kmeans.labels_
    centroids = kmeans.cluster_centers_
    #print(len(labels))
    #plt.scatter(x[:,0], x[:,1], c=kmeans.labels_, cmap='rainbow') 
    #plt.show()
    return labels
 
def dbsc(X):
    from sklearn.cluster import DBSCAN
    dbscan = DBSCAN(metric='cosine', eps=0.07, min_samples=50) # you can change these parameters, given just for example 
    cluster_labels = dbscan.fit_predict(X) 
    return cluster_labels


def main():
    #data = get_nounTags()
    data = get_nounTags()
    all_words = []
    for x in data:
        for y in x:
            all_words.append(y)
    model = Word2Vec(data, min_count=1,size= 100,workers=3, window =3, sg = 1)
    model.train(data,total_examples=len(data),epochs=10)

    vocab = model.wv.vocab
    l = list(vocab)
    #c_labels = dbsc(model[vocab])
    c_labels = clustering(model[vocab])

    #print(len(l))
    print("enter to search :\n")
    w = input()
    print(model.wv.most_similar(positive=w))
    #print(all_words)
    #fdist = FreqDist(all_words)
    #common = fdist.most_common(100)
    #print(common0)

main()

#list = ["email address","new posts","' s'","amazing charming places",]