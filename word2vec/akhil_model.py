import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017")
mydb = myclient["iiitmkOne"]
table = mydb["rawData2"] #blob noun phrases

table2 = mydb["CLforMC5"] #blob noun phrases

table3 = mydb["CLforMC1"] #blob noun phrases
table4 = mydb["CLforMC3"] #blob noun phrases


from gensim.models import Word2Vec
#from nltk import *
import nltk
import re

from sklearn import cluster
import matplotlib.pyplot as plt
from nltk.corpus import stopwords

def second():
    all_text = []
    for x in table.find():
        all_text.append(x['data'])
    all_new_text = []
    for x in all_text:
        processed_article = x.lower()
        processed_article = re.sub('[^a-zA-Z]', ' ', processed_article )
        processed_article = re.sub(r'\s+', ' ', processed_article)
        all_new_text.append(processed_article)
    all_words = []
    for x in all_new_text:
        all_words.append(nltk.word_tokenize(x))
    #print(all_words)
    for i in range(len(all_words)):
        all_words[i] = [w for w in all_words[i] if w not in stopwords.words('english')]

    word2vec = Word2Vec(all_words, min_count=3)
    #word2vec.wv.save_word2vec_format('just.bin', binary=True)
    word2vec.save('wordToken2vecMinCount5.model')
def clustering(x):
    kmeans = cluster.KMeans(n_clusters=100)
    kmeans.fit(x)
    labels = kmeans.labels_
    centroids = kmeans.cluster_centers_
    #print(len(labels))
    #plt.scatter(x[:,0], x[:,1], c=kmeans.labels_, cmap='rainbow') 
    #plt.show()
    return labels

def insertdb(words,cluster_labels):
    for x in range(0, len(words)):
        table4.insert_one({"word":words[x],"c_label":str(cluster_labels[x])})

def main():
    #second()
    #model = Word2Vec.load("wordToken2vec.model")
    model = Word2Vec.load("wordToken2vecMinCount3.model")
    #model = Word2Vec.load("wordToken2vecMinCount5.model")
    vocab = model.wv.vocab
    cluster_labels = clustering(model[vocab])
    words = list(model.wv.vocab)
    table4.drop()

    insertdb(words,cluster_labels)
    

main()