import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017")
mydb = myclient["iiitmkOne"]
table5 = mydb["rawData3"]

table6 = mydb["30topicDB"]

table8 = mydb["80topicNMF"]
table6 = mydb["80topicLDA"]



count = 0
for x in table6.find():
    count+=1
    print(count)
    print(x)
    print("\n")
print("LDA")

count = 0
for x in table8.find():
    count+=1
    print(count)
    print(x)
    print("\n")
print("NMF")