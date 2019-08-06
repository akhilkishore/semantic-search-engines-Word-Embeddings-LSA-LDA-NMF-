from bs4 import BeautifulSoup
import requests
from rake_nltk import Rake
import pymongo
from time import sleep
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
from textblob import TextBlob
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017")
mydb = myclient["iiitmkOne"]
#table = mydb["rawData"] #blob noun phrases
table = mydb["rawData2"] #blob noun phrases


r = Rake(min_length=2, max_length=2) #rake intiated

def scrap_sub_urls(url):
    r = requests.get(url)
    #sleep(3)
    Rdata = r.text
    soup = BeautifulSoup(Rdata, features="lxml")
    list=[]
    #list2=[]
    for a in soup.find_all('a', href=True):
        if a["href"] not in list and url in a["href"]:
            list.append(a["href"])
    stops = [".pdf",".jpg",".jpeg",".png"]
    temp = list
    list = []
    for x in temp:
        flag = 0
        for y in stops:
                if y in x:
                        flag =1
        if flag != 1:
                list.append(x)
    return list

def scrap(url):
    r = requests.get(url)
    sleep(3)
    dataLine = """ """
    Rdata = r.text
    soup = BeautifulSoup(Rdata, features="lxml")
    for i in soup.find_all('p'):
        dataLine +=" "
        dataLine += i.text    
    return dataLine

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

def readFile():
        f = open("urllist.txt", "r")
        data = f.read()
        data = data.split("\n")
        urls = []
        for x in data:
                if x :
                        if "https://" in x:
                                pre = "https://"
                                x = x.replace("https://","")
                        if "http://" in x:
                                pre = "http://"
                                x = x.replace('http://',"")
                        x = x.split("/")
                        x = x[0]
                        urls.append(pre+x)
        return urls

def insertmongo(urlname,data,keywords,noun_phrases):
        x = table.insert_one({"url":urlname,"data":data,"keywords":keywords,"nouns":noun_phrases})

def main():
    #url = "https://www.keralabackwater.com"
        count = 0
        urls = readFile()
        for y in urls:
                sub_urls = scrap_sub_urls(y)
           
                for x in sub_urls:
                        count+=1
                        list = [".pdf",]
                        if y in x:
                                print(x)
                                scrap_page = scrap(x)
                                keywords = extract_keywords(scrap_page) 
                                noun_phrases = extract_noun_phrases(scrap_page)
                                #print(scrap_page)
                                #print(keywords)
                                #print(noun_phrases)
                                #break
                                print(count)
                                insertmongo(x,scrap_page,keywords,noun_phrases)
                      
#readFile()
main()
