#! /usr/bin/pyhton
import os, requests, re, time, nltk, math
import numpy as np
from collections import Counter
from bs4 import BeautifulSoup
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from urllib.request import urlopen, HTTPError, URLError
from elasticsearch import Elasticsearch

es = Elasticsearch()
app = Flask(__name__)

word_d={} #for COS
stopwordlist = []
contents=[] #for TF-IDF
vectors=[]
result=[]
###########Elasticsearch에 저장되는 것들 ##############
# urllist = []
# counts = []
# runtime = []
###########Elasticsearch에 저장되는 것들 ##############

def makeWordDic(contents):
   global word_d
   tokenized=word_tokenize(contents)
   tokenized=[v for v in tokenized if v]
   result=[]
   stoplist = set(stopwords.words("english"))
   for w in tokenized:
      if w not in stoplist:
         result.append(w)
   for w in result:
      if w not in word_d.keys():
         word_d[w]=0
      word_d[w]+=1

def compute_tf(s):
   bow = set()
    # dictionary for words in the given sentence (document)
   w_d = {}
   tokenized = word_tokenize(s)
   for tok in tokenized:
      if tok not in w_d.keys():
         w_d[tok]=0
      w_d[tok] += 1
      bow.add(tok)
   tf_d = {}
   for word, count in w_d.items():
      tf_d[word]=count/len(bow)
   return tf_d

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

def compute_idf():
   Dval = len(contents)
   idf_d = {}
   for w in word_d.keys():
      cnt = 0
      for s in contents:
            if w in word_tokenize(s):
               cnt += 1
            idf_d[w]=math.log10(Dval/cnt)
   return idf_d

def crawling(url):
   start = time.time() #수행시간 측정
   try:   #url 주소 예외처리
      html = urlopen(url).read().decode('utf-8')
   except HTTPError as e:
      print('page not found')
   except URLError as e:
      print('the server could not be found!')
   else:
      soup = BeautifulSoup(html,'html.parser')
      html_contents=re.sub('<.+?>', ' ', str(soup.select('body'))).strip().lower()
      word=re.sub('[^0-9a-zA-Zㄱ-힗]', ' ', html_contents).split()
      word=[v for v in word if v] # list 빈값제거
      makeWordDic(html_contents)
      contents.append(html_contents)
      counts = len(word) # word count in one crawl
      runtime = time.time() - start
      print(counts)
      print(runtime)


def insertData(url,word_count,runtime): #엘라스틱 서치에 데이터 저장
      body = {
         'url' : url,
         'word_count' : word_count,
         'runtime' : runtime
         #top10 , cos 3
      }
      es.index(index = "websites", doc_type = "title",body=body)


@app.route('/')
def mainpage():
    return render_template('index.htm')

@app.route('/urlsearch',methods = ['POST']) # single url
def urlsearch():
   if(request.method == 'POST'):
          #여기서 url 중복체크#
          crawling(request.form['url'])
   return render_template('index.htm')


@app.route('/upload', methods = ['POST']) # with txt file
def upload_file(): 
   for sw in stopwords.words("english"):
      stopwordlist.append(sw)#

   ################# 파일관련 부분 #################
   directory="upload"
   # es_host='127.0.0.1'
   # es_port='9200'
   if not os.path.exists(directory):
      os.mkdir(directory)
   f=request.files['file']
   savepath = directory +'/'+ secure_filename(f.filename)
   if f.filename.endswith('.txt'):  #is text file?
      f.save(savepath)
   ################# 파일관련 부분 #################

   with open(savepath, mode='r', encoding='utf-8') as f:
      urllist = list(set(f.read().splitlines()))  #url 개행문자제거 #중복된 url 모두 제거 

   for line in urllist: #crawling start
      crawling(line)      #crawling func
   '''
      ##코사인
   for c in contents:
      vectors.append(make_vector(c))
   print(len(vectors))
   dotpro=[]
   cos=[]
   for i in range(0, len(urllist)):
      for j in range(0, len(urllist)): # len(urllist)
         dotpro[i].append(np.dot(vectors[i],vectors[j]))
   for i in range(0, len(urllist)):
      for j in range(0, len(urllist)):
         cos[i].append(dotpro[i][j]/np.linalg.norm(vectors[i])*np.linalg.norm(vectors[j]))
   
   idf_d=compute_idf()
   dic={}
   top10={}
   for i in range(0,len(contents)):
      tf_d = compute_tf(contents[i])
      for word, tf in tf_d.items():
         dic[word]=tf*idf_d[word]
      sortlist=sorted(dic.items(), key=lambda x: x[1], reverse=True)
      top10[i]=sortlist.key[:10]
      ##코사인
   '''    
   return render_template('index.htm',res=result, r=1540)      

if __name__ == '__main__':
   app.run(port = 5001,debug = True)

