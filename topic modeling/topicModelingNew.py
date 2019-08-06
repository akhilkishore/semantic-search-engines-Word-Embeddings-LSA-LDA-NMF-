import pymongo
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation


myclient = pymongo.MongoClient("mongodb://localhost:27017")
mydb = myclient["iiitmkOne"]
table5 = mydb["rawData3"]

table6 = mydb["80topicLDA"]
table7 = mydb["80topicLSA"]
table8 = mydb["80topicNMF"]

def topicLDA(doc_complete):
    count_vect = CountVectorizer(max_df=0.8, min_df=2, stop_words='english')
    doc_term_matrix = count_vect.fit_transform(doc_complete)

    LDA = LatentDirichletAllocation(n_components=50, random_state=42) #lsqr
    LDA.fit(doc_term_matrix)

    data = []
    for i,topic in enumerate(LDA.components_):
        print(f'Top 10 words for topic #{i}:')
        data.append([count_vect.get_feature_names()[i] for i in topic.argsort()[-25:]])
        print('\n')
    count = 0
    for x in data :
        count += 1 
        #table6.insert_one({"topic":count,"keywords":x})
        print("inserted : ",count)            
    return data    

def topicNMF(doc_complete):
    tfidf_vect = TfidfVectorizer(max_df=0.8, min_df=2, stop_words='english')
    doc_term_matrix = tfidf_vect.fit_transform(doc_complete)
    
    nmf = NMF(n_components=50, random_state=42)
    nmf.fit(doc_term_matrix )

    data =[]
    for i,topic in enumerate(nmf.components_):
        print(f'Top 10 words for topic #{i}:')
        data.append([tfidf_vect.get_feature_names()[i] for i in topic.argsort()[-25:]])
        print('\n')     
    count = 0
    for x in data :
        count += 1 
        table8.insert_one({"topic":count,"keywords":x})
        print("inserted : ",count)            
    return data

def main():
    doc_complete = []

    for x in table5.find():
        text = ""
        doc_complete.append(x['text'])
    print("Total document length is :",len(doc_complete))
    
    data = topicNMF(doc_complete)
    data = topicLDA(doc_complete)


    print("give an input :")
    w = input()
    w = w.split(" ")
    all = []
    for x in w:
        for y in data:
            if x in y:
                all.append(y)
    print(all)

main()

    