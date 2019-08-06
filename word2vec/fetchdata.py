import pymongo
from nltk.corpus import stopwords


myclient = pymongo.MongoClient("mongodb://localhost:27017")
mydb = myclient["iiitmkOne"]
table = mydb["rawData2"] #new scrap
table2 = mydb["CLforMC5"] #cluster labels for min count 5
table3 = mydb["CLforMC1"] #blob noun phrases
table4 = mydb["CLforMC3"] #blob noun phrases
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
def main():
    print("enter an input :\n")
    q = input()
    q = q.split(" ")
    search_words = []
    for x in q:
        if x not in stopwords.words('english'):
            search_words.append(x)

    list_clusterLabels = getClusterLabels(search_words)

    all_words = getAllWords(list_clusterLabels)

    print(all_words)
main()

