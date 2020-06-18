from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import requests
import re
from collections import Counter
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def mainpage():
    return render_template('index.htm')

@app.route('/url') # single url
def url():
    return render_template('index.htm')

@app.route('/upload', methods = ['POST']) # with txt file
def upload_file(): 
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
   for i in f.readlines(): #crawling start
      url=i.rstrip("\n")   #url 개행문자제거
      res = requests.get(url)
      soup = BeautifulSoup(res.content, "html.parser")
      html_contents=soup.select('body')
      words=[]
      word=[]
      Dic=Counter()
      w=[]
      f=[]
      
      
      for j in html_contents:
         words=j.get_text().split()
      for j in words:
         word.append(re.sub('[^0-9a-zA-Zㄱ-힗]', '', j)) #number,english, 한글만 남기기
      
      word=[v for v in word if v] # list 빈값제거
      
      for j in word: 
         Dic[j]+=1
         
      for word, freq in Dic.items():
         w.append(word)
         f.append(freq)
      count=len(w)
      dic={
         "url":url,
         # "word":w,
         "count":count
      }
      result.append(dic)
   return render_template('index.htm',res=result, r=1540)      
		
if __name__ == '__main__':
   app.run(debug = True)