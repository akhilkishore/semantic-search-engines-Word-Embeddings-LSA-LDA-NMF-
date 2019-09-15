import pymongo


myclient = pymongo.MongoClient("mongodb://localhost:27017")
mydb = myclient["iiitmkOne"]
table = mydb["rawData2"] #blob noun phrases
c = 0
for x in table.find():
	print(x)
	name = str(c)+".txt"
	c+=1
	f = open(name,'a')
	f.write(x['url']+"\n")
	f.write(x['data']+"\n")

