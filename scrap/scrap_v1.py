from tkinter import *
from tkinter import messagebox
from tkinter import scrolledtext
from bs4 import BeautifulSoup
import requests
from rake_nltk import Rake
import pymongo
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 

myclient = pymongo.MongoClient("mongodb://localhost:27017")
mydb = myclient["iiitmkOne"]
table2 = mydb["dbOne"] #intial sscrapn

r = Rake(min_length=2, max_length=2)

window = Tk()
window.configure(background='black')
window.title("Web Scraping")
window.geometry('800x500')

lbl = Label(window, text="Enter URL :",bg="black",fg="white")
url = Entry(window, width = 50)
lbl.grid( column = 10, row = 0 )
url.grid( column = 20, row = 1)
lbl.place(relx=0.5, rely=0.05, anchor=CENTER)
url.place(relx=0.5, rely=0.1, anchor=CENTER)

T = Text(window, height=10, width=55)
T.pack()
T.place(relx=0.5, rely=0.75, anchor=CENTER)

def dataBase(data,obj1,fn1,fn3,fn2):#
    insideRow = {"urls":obj1,"datas":fn1,"keywords":fn2}
    mainRow = {"domain":data,"pages":insideRow}
    table2.insert_one(mainRow) 
    print("\n Success..")

def keyWord(dataLine):
        keyWordslast =[]
        for i in dataLine:
                r.extract_keywords_from_text(i)
                keyWords = """"""
                keyWords = r.get_ranked_phrases() 
                keyWordslast.append(keyWords)
        return keyWordslast

def removeDup(list2):   
    finallist = []
    for i in list2:
        if i not in finallist:
            finallist.append(i)
    return finallist

def prep(data):
        stop = [".jpg",".pdf",".gif",".pdf"]
        r = requests.get(data)
        Rdata = r.text
        soup = BeautifulSoup(Rdata, features="lxml")
        list=[]
        list2=[]
        for a in soup.find_all('a', href=True):
                list.append(a["href"])
        for x in list:
                if data in x:
                        list2.append(x)
                if(len(list2)>19):
                        break
        SublistOfUrls = removeDup(list2)
        print("total sub urls found..",len(SublistOfUrls))
        listOfUrls = []
        for x in SublistOfUrls :
                flag = 0
                for y in stop:
                        if y in x :
                                flag += 1
                if flag == 0:
                        listOfUrls.append(x)           
        print(len(listOfUrls))
        return listOfUrls

def scrap(obj1):
    dataLinefinal = []
    title = []
    for i in obj1:
        dataLine = """ """
        r = requests.get(i)
        Rdata = r.text
        soup = BeautifulSoup(Rdata, features="lxml")
        #title.append(soup.find("title").string) 
        for i in soup.find_all('p'):
                dataLine += i.text    
        dataLinefinal.append(dataLine) 
    return dataLinefinal,title

def main():

    data = url.get()

    obj1 = prep(data) #list of all urls

    fn1,fn3 = scrap(obj1) #dataLine,title

    fn2 = keyWord(fn1)#keywords
    
    print(fn1)
    print("\n")
    print(fn2)

    #dataBase(data,obj1,fn1,fn3,fn2)    

    messagebox.showinfo('info','Success..!')

def display(ta,ua,tta,window2,txt):
   
    txt.insert(INSERT,"Title :\n" + ta + "\n\n")
    txt.insert(INSERT,"Url :\n" + ua + "\n\n")
    txt.insert(INSERT,"Text :\n" + tta + "\n\n\n")


def search():
    data2 = url2.get()
    myquery = {"pages":{"keywords": data2}}#instead of query search search all 
    mysearch = table2.find()

    window2 = Tk()
    window2.configure(background='black')
    window2.title("Web Scraping")
    window2.geometry('800x800')
    txt = scrolledtext.ScrolledText(window2,width=98,height=50) 
    txt.grid(column=0,row=0) 



    for x in mysearch: #loop for printing all result
        loadKeywords = x["pages"]["keywords"]
        loadUrls= x["pages"]["urls"]
        loadDatas = x["pages"]["datas"]

        for y in range(0,len(loadKeywords)):
                sub = loadKeywords[y]
                if data2 in sub:
                        ta = x["domain"]
                        ua = loadUrls[y]
                        tta = loadDatas[y]  
                        display(ta,ua,tta,window2,txt)
  
    window.destroy()

 ### print available keywords
 ### print available keywords
y =[]
keywordsList =[]
keywordsList2 = ""
for x in table2.find({},{ "_id": 0, "domain": 0}):
    z = x["pages"]
    y += z["keywords"]
for x in y:
    for u in x:
        keywordsList.append(u)
keywordsList2 += ", ".join(keywordsList)
T.insert(END, keywordsList2)
###
###

btn = Button(window, text="Scrap", command=main,bg="green")
btn.grid(column=1, row=3)
btn.place(relx=0.5, rely=0.16, anchor=CENTER)

btn2 = Button(window, text="Search", command=search,bg="green")
btn2.grid(column=1, row=6)
btn2.place(relx=0.5, rely=0.41, anchor=CENTER)


window.mainloop()
