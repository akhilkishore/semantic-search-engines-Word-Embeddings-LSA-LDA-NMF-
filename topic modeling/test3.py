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

from nltk.stem.wordnet import WordNetLemmatizer
stop = set(stopwords.words('english'))
exclude = set(string.punctuation)
lemma = WordNetLemmatizer()
def clean(doc):
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized

doc_clean = [clean(doc).split() for doc in doc_complete] 

import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel

dictionary = corpora.Dictionary(doc_clean)

doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]

#id2word = corpora.Dictionary(doc_clean)
#print("id2word created : ",id2word)

# Create Corpus
#texts = doc_clean
#print("text is :", texts)

# Term Document Frequency
#corpus = [id2word.doc2bow(text) for text in doc_clean]
#print("one element of corpus is : ",corpus[0], len(corpus))
#data = [[(id2word[id], freq) for id, freq in cp] for cp in corpus]
#print(len(data))
lda_model = gensim.models.ldamodel.LdaModel(corpus=doc_term_matrix,
                                           id2word=dictionary,
                                           num_topics=20, 
                                           random_state=25,
                                           update_every=1,
                                           chunksize=100,
                                           passes=20,
                                           alpha='auto',
                                           per_word_topics=True)

#lda_model.save("lda_model2")
#lda_model = gensim.models.ldamodel.LdaModel.load("lda_model2")

#print()
#print(len(lda_model.print_topics(num_topics=50, num_words=10)))
data = lda_model.print_topics(num_topics=10, num_words=8)
print("length of data is : ", len(data))

for x in data:
    print(x)
    print("\n")
