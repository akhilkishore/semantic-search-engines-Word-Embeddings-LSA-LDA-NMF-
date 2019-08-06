import pymongo
from nltk.corpus import stopwords 
import string
stop_words = set(stopwords.words('english') + list(string.punctuation))

myclient = pymongo.MongoClient("mongodb://localhost:27017")
mydb = myclient["iiitmkOne"]

table5 = mydb["rawData3"]

for x in table5.find():
    print(x)
    break