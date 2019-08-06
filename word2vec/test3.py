import pymongo
import re
from textblob import TextBlob
import nltk
from nltk.corpus import stopwords
from rake_nltk import Rake

r = Rake(min_length=2, max_length=2) #rake intiated



myclient = pymongo.MongoClient("mongodb://localhost:27017")
mydb = myclient["iiitmkOne"]
#table = mydb["rawData"] #blob noun phrases
table = mydb["rawData2"] #new scrap
table2 = mydb["CLforMC5"] #cluster labels for min count 5
table3 = mydb["CLforMC1"] #blob noun phrases
table4 = mydb["CLforMC3"] #blob noun phrases
table5 = mydb["rawData3"]

def extract_keywords(text):
    r.extract_keywords_from_text(text)
    keyWords = r.get_ranked_phrases() 
    return keyWords

def extract_noun_phrases(text):
    blob = TextBlob(text)
    nouns = blob.noun_phrases
    temp = []
    for x in nouns:
        if x not in temp:
            temp.append(x)
    return temp

def clean(data):
    processed_article = data.lower()
    processed_article = re.sub('[^a-zA-Z]', ' ', processed_article )
    processed_article = re.sub(r'\s+', ' ', processed_article)

    all_words = nltk.word_tokenize(processed_article)
    all_words2 = []

    for x in all_words:
        if x not in stopwords.words('english'):
            all_words2.append(x)

    keywords = extract_keywords(processed_article)
    nouns = extract_noun_phrases(processed_article)

    return processed_article,all_words2,keywords,nouns

    
def main():
    print('hello')
    for x in table.find():
        print(x['data'])
        data,all_words,keywords,nouns = clean(x['data'])
        table5.insert_one({"url":x['url'],"text":data,"tokens":all_words,"keywords":keywords,"nouns":nouns})  

main()