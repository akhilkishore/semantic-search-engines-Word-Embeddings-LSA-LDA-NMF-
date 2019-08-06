import pymongo


myclient = pymongo.MongoClient("mongodb://localhost:27017")
mydb = myclient["iiitmkOne"]
table = mydb["rawData"] #blob noun phrases

def func1():
    count = 0
    for x in table.find():
        print(x)
        count+=1
        print(count)
        break

def dropper():
    table.drop()

#dropper()
count = 0
for x in table.find():
    print(x['url'])
    print(x['nouns'])
    count+=1
    print("/n/n")
    print(count)