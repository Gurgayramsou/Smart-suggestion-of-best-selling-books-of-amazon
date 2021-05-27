''' 
This is amazon best selling book gui implementation.
unsupervised machine learning using k-means clustor
gui used: tkinkter
--ramakrishna hegde
'''
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from numpy import random
import re,time,random,webbrowser,googlesearch

#importing datasets of best selling books in amazon
dataset=pd.read_csv('data_set.csv')
data_cp=dataset

#scaling the data in uniform foramat
from sklearn.preprocessing import StandardScaler
sc=StandardScaler()
dataset.iloc[:,2:6]=sc.fit_transform(dataset.iloc[:,2:6])

#encoding the categorical data using onehotencoder of sklearn
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder
from sklearn.compose import ColumnTransformer

def encoder_func(dataset):
    #dependent variable encoding
    le=LabelEncoder()
    dataset['Genre']=le.fit_transform(dataset['Genre'])

    #independent variable encoding
    import category_encoders as ce
    ec=ce.BaseNEncoder(cols=['Name','Author'],return_df=True,base=10)
    return ec.fit_transform(dataset)

#encoding categorical data of dataset
dataset=encoder_func(dataset)

# clustoring similar books using kmeans of clustoring
from sklearn.cluster import KMeans
kmc=KMeans(n_clusters=8)
kmc.fit_transform(dataset)
global labels
labels=kmc.labels_


#----------------------------------------------------------------#
#gui implementations
from tkinter import *
from tkinter import ttk
root=Tk()
root.title('BestBooks')
root.geometry("400x400")
root.configure(bg='ghost white')

#implementing all functions here
#keysearch regx function call
def auto_complete(src1=data_cp["Name"]):
    cp=re.compile('.*'+keyword.get().lower()+'.*')
    books=[]
    for i in src1:
        if len(cp.findall(i.lower()))>0:
            books.append(i)
    #suggested books in a checkbox
    #selected variable holds user selected book name
    global selected 
    selected=StringVar()
    bk_list=ttk.Combobox(root,values=books,width=30,textvariable=selected).place(x=100,y=150) 
    sl_button=Button(root,bg='#B072A7',command=books5,text='select',width=15).place(x=128,y=170)

#top 5 book suggested based on user search
def books5(src=data_cp['Name']):
    count=0
    for book in src:
        if book==selected.get():
            break
        count+=1
    clustor=labels[count]
    count2=5
    sug_list=[]
    rnd_no=[]
    while count2>0:
        rand_no=random.randint(0, 549)
        rnd_no.append(rand_no)
        if labels[rand_no]==clustor:
            sug_list.append(data_cp['Name'][rand_no])
            count2-=1
    inf='top 5 books of your search are here'
    info_books=Label(root,text=inf,pady=3,fg='blue').place(x=0,y=200)
    info_books=Label(root,text='-----------------------------------------------------------------------------------',pady=3,fg='green').place(x=0,y=220)    
    y=220
    for i in range(len(sug_list)):
        y+=20
        b=Label(root,text=str(i+1)+')'+sug_list[i],pady=3).place(x=0,y=y)
    
    #variable by holds the index number of selected book
    global by
    by=StringVar()
    buy=Spinbox(root, font=12, from_=1, to=5,width=5,textvariable=by).place(x=5,y=345)
 
    #user has given with the buying option in book store
    def websrc():
        url=googlesearch.search(sug_list[int(by.get())-1],stop=5)
        for i in url:
            cp=re.compile('.*www.amazon.in+.*')
            if len(cp.findall(i))>0:
                 webbrowser.open(i)
    btnbuy=Button(root,text='Buy',command=websrc,bg='yellow',width=5).place(x=70,y=345)
    


# Headings//
head=Label(root,text='Amazon Best Books')
head.config(font=30,pady=20,border=10,bg='light green')
head.place(x=100,y=0)

#greeting user

invite=Label(root,text="Hi reader! welcome to amazon books.!!",font=15,fg='blue')
invite.place(x=60,y=60)


#label saying user to enter key
search=Label(root,text='-------------------------------------------------------------------------------------------------------').place(x=0,y=85)
search=Label(root,text='please enter some keywords of book here').place(x=0,y=100)

#keyword entry box
global keyword
keyword=StringVar()
enter=Entry(root,width=20,bg='sky blue',relief=SUNKEN,textvariable=keyword).place(x=0,y=125)
searchSub=Button(root,text='search',width=4,bg='pink',command=auto_complete).place(x=110,y=120)



root.mainloop()
       
       







