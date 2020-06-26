#! /usr/bin/pyhton
import os
import requests
import re
import nltk
import numpy as np
from collections import Counter
from bs4 import BeautifulSoup
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


app = Flask(__name__)

@app.route('/')
def mainpage():
    return render_template('index.htm')

@app.route('/url') # single url
def url():
    return render_template('index.htm')


@app.route('/upload', methods = ['POST']) # with txt file
def upload_file(): 
   word_d={}
   stopwordlist = []
   for sw in stopwords.words("english"):
      stopwordlist.append(sw)

   def makeWordDic(contents):
      tokenized=word_tokenize(contents)
      tokenized=[v for v in tokenized if v]
      result=[]
      for w in tokenized:
         if w not in stopwords:
            result.append(w)
      for w in result:
         if w not in word_d.keys():
            word_d[w]=0
         word_d+=1
   def make_vector(i): #str(html_contents)
      v=[]
      tokenized=word_tokenize(i)
      for w in word_d.keys():
         val=0
         for t in tokenized:
            if t==w:
               val+=1
         v.append(val)
      return v

   directory="upload"
   # es_host='127.0.0.1'
   # es_port='9200'
   if not os.path.exists(directory):
      os.mkdir(directory)
   f=request.files['file']
   savepath = directory +'/'+ secure_filename(f.filename)
   if f.filename.endswith('.txt'):
      f.save(savepath)

   f = open(savepath, mode='r', encoding='utf-8')
   result=[]
   v=0
   vectors=[]
   relist=[]
   contents=[]
   for i in f.readlines(): #crawling start
      relist.append(i)
      url=i.rstrip("\n")   #url 개행문자제거
      res = requests.get(url)
      soup = BeautifulSoup(res.content, "html.parser")
      html_contents=re.sub('<.+?>', ' ', str(soup.select('body'))).strip().lower()
      word=re.sub('[^0-9a-zA-Zㄱ-힗]', ' ', html_contents).split()
      word=[v for v in word if v] # list 빈값제거
      makeWordDic(html_contents)
      counts=len(word) # word count in one crawl
      contents.append(html_contents)
      print(word)

   for c in contents:
      vectors.append(make_vector(c))
   dotpro=[]
   cos=[]
   for i in range(len(relist)):
      for j in range(len(relist)): # len(relist)
            dotpro[i].append(np.dot(vectors[i],vectors[j]))
   for i in range(len(relist)):
      for j in range(len(relist)):
            cos[i].append(dotpro[i][j]/np.linalg.norm(vectors[i])*np.linalg.norm(vectors[j]))
      
   return render_template('index.htm',res=result, r=1540)      
		
if __name__ == '__main__':
   app.run(debug = True)

###########################################################
def compute_tf(s):
    bow = set()
    # dictionary for words in the given sentence (document)
    wordcount_d = {}
    tokenized = word_tokenize(s)
    for tok in tokenized:
        if tok not in wordcount_d.keys():
            wordcount_d[tok]=0
        wordcount_d[tok] += 1
        bow.add(tok)
    tf_d = {}
    for word, count in wordcount_d.items():
        tf_d[word]=count/len(bow)

    return tf_d

def compute_idf():
    Dval = len(sent_list)
    # build set of words
    bow = set()
    for i in range(0,len(sent_list)):
        tokenized = word_tokenize(sent_list[i])
        for tok in tokenized:
            bow.add(tok)
    idf_d = {}
    for t in bow:
        cnt = 0
        for s in sent_list:
            if t in word_tokenize(s):
                cnt += 1
            idf_d[t]=math.log10(Dval/cnt)
    return idf_d

idf_d = compute_idf()
for i in range(0,len(sent_list)):
    tf_d = compute_tf(sent_list[i])
    for word,tfval in tf_d.items():
        print(word, tfval*idf_d[word])
##########################################################################