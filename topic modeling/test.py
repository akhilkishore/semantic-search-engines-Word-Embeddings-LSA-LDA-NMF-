import pymongo
from nltk.corpus import stopwords 
import string
stop_words = set(stopwords.words('english') + list(string.punctuation))

myclient = pymongo.MongoClient("mongodb://localhost:27017")
mydb = myclient["iiitmkOne"]

table5 = mydb["rawData3"]

doc_complete = []

for x in table5.find():
    doc_complete.append(x['text'])

print("Total document length is :",len(doc_complete))
doc2 = doc_complete
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
stop = set(stopwords.words('english'))
exclude = set(string.punctuation)
lemma = WordNetLemmatizer()
def clean(doc):
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized

doc_clean = [clean(doc).split() for doc in doc_complete] 

print("Total document length is :",len(doc_complete))
print("single document text is :",doc_clean[0])

import gensim
from gensim import corpora

from gensim.models import LsiModel
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from gensim.models.coherencemodel import CoherenceModel
import matplotlib.pyplot as plt
dictionary = corpora.Dictionary(doc_clean)

doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]
def create_gensim_lsa_model(doc_clean,number_of_topics,words, dictionary, doc_term_matrix):
    """
    Input  : clean document, number of topics and number of words associated with each topic
    Purpose: create LSA model using gensim
    Output : return LSA model
    """
    #dictionary,doc_term_matrix=prepare_corpus(doc_clean)
    # generate LSA model
    lsamodel = LsiModel(doc_term_matrix, num_topics=number_of_topics, id2word = dictionary)  # train model
    #print(lsamodel.print_topics(num_topics=50, num_words=50))
    return lsamodel

lsamodel = create_gensim_lsa_model(doc_term_matrix,100,10, dictionary, doc_term_matrix)

data = lsamodel.print_topics(num_topics=50, num_words=10)

for x in data:
    print(x)
    print("\n")


