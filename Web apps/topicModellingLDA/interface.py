from flask import Flask, render_template, request
import pymongo

from nltk.corpus import stopwords 
import string
from Jsimilarity import levenshtein_ratio_and_distance

stop_words = set(stopwords.words('english') + list(string.punctuation))

myclient = pymongo.MongoClient("mongodb://localhost:27017")
mydb = myclient["iiitmkOne"]
#table = mydb["rawData2"] #new scrap
#table2 = mydb["CLforMC5"] #cluster labels for min count 5
table6 = mydb["80topicLDA"]
#table3 = mydb["CLforMC1"] #blob noun phrases
#table4 = mydb["CLforMC3"] #blob noun phrases
table5 = mydb["rawData3"]

def getClusterLabels(words):
    list = []
    for x in words:
        for y in table2.find():
            if y['word'] == x:
                list.append(y['c_label'])
    return list

def getAllWords(labels):
    list = []
    for x in labels:
        for y in table2.find():
            if y['c_label'] == x:
                if y['word'] not in list:
                    list.append(y['word'])
    return list
def rankWitTF(words):
    docs = []
    for x in table5.find():
        count = 0
        for y in words:
            c = x['tokens'].count(y)
            count+=c
        docs.append((x['_id'],count))
    return docs

def sort(docList):
      templist = docList
      for y in range(0,1000):
               flag2 = 0
               for x in range(1,len(templist)):
                        if templist[x][1] > templist[x-1][1]:
                           temp = templist[x]
                           templist[x] = templist[x-1]
                           templist[x-1] = temp
                           flag2 = 1
               if flag2 == 0:
                        break
      lastList=[]
      for x in templist:
            if x not in lastList:
                if x[1] != 0:
                    lastList.append(x)
      return lastList

def fetchDB():
    topics = []
    for x in table6.find():
        topics.append(x['keywords'])
    return topics

app = Flask(__name__)

import numpy as np


@app.route('/')
def student():
   return render_template('search.html') # rendering the home page

@app.route('/result',methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        w=request.form.get("sname")
        q = w.split(" ")
        print("data is ",q)
        search_words = []
        for x in q:
            if x not in stopwords.words('english'):
                search_words.append(x)
        data = fetchDB()
        selectedTopics = []
        for x in data:
            for y in search_words:
                if y in x:
                    selectedTopics.append(x)
                    break

        all_words = []
        for x in selectedTopics:
            for y in x:
                if y not in all_words:
                    all_words.append(y)
        


        print("========================================= \n")
        print("length of all candidate words :",len(all_words),"\n")
        print(all_words)
        print("topic wise word list : \n\n")
        temp = []
        for x in selectedTopics:
            if x not in temp:
                temp.append(x)
        print(temp)
        print("========================================= \n")
        
        rankedDocuments = rankWitTF(all_words)
        lastlist = sort(rankedDocuments)
        items = []
        if len(lastlist) > 15:
            n = 15
        else:
            n = len(items)
        for x in range(0,n):
            for y in table5.find():
                if y['_id'] == lastlist[x][0]:
                    text = ""
                    for u in range(0,250):
                        text+=y["text"][u]
                    items.append({"url":y['url'],"text":text})

        return render_template("result.html", users=items,search=w)

if __name__ == '__main__':
    #app.run(debug = True)
    app.run(host='localhost', port=4561)
