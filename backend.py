#! /usr/bin/pyhton
import os
import requests
import re
import time
import nltk
import math
import numpy as np
from collections import Counter
from bs4 import BeautifulSoup
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from urllib.request import urlopen, HTTPError, URLError
from elasticsearch import Elasticsearch

def makeWordDic(contents): #list(tokenized)
    global word_d
    for w in contents:
        if w not in word_d.keys():
            word_d[w] = 0
        word_d[w] += 1

def makeVector(contents): #list(tokenized)
    vector=[]
    for w in word_d.keys():
        v = 0
        for t in contents:
            if t == w:
                v += 1
        vector.append(v)
    return vector

def computeCos():
    global datalist
    for i in datalist:
        url = i["url"]
        vector = i["vector"]
        compare = []
        top3 = []
        for j in datalist:
            result = {}
            compare_url = j["url"]
            compare_vector = j["vector"]
            if url == compare_url:
                continue
            else:
                dotpro = np.dot(vector, compare_vector)
                cosine = dotpro / (np.linalg.norm(vector) * np.linalg.norm(compare_vector))
                result["url"] = compare_url
                result["cosine"] = cosine
                compare.append(result)
        compare = sorted(compare, key=(lambda x: x["cosine"]), reverse=True)  
        compare = compare[:3]
        for j in compare:
            top3.append(j["url"])
        i["top3"]=top3
        

def computeTf(contents):
    dic = set()
    word_frequency = {}
    tf_d = {}
    for t in contents:
        if t not in word_frequency.keys():
            word_frequency[t]=0
        word_frequency[t] += 1
        dic.add(t)
    for word, frequency in word_frequency.items():
        tf_d[word]=  float(frequency) / float(len(dic))
    return tf_d

def computeIdf():
    idf_d = {}
    dic = set()
    Dval = float(len(datalist))
    for i in datalist:
        tokenized=i["contents"]
        for t in tokenized:
            dic.add(t)
    for w in dic:
        count = 0.0
        for i in datalist:
            if w in i["contents"]:
                count+=1
        idf_d[w]=math.log10(Dval/count)
    return idf_d

def computeTfidf():
    global datalist
    idf_d=computeIdf()
    for i in datalist:
        result=[]
        tf_d = computeTf(i["contents"])
        top10=[]
        for w, tf in tf_d.items():
            tfidf = {}
            tfidf["word"] = w
            tfidf["value"] = tf*idf_d[w]
            result.append(tfidf)
        result=sorted(result, key=(lambda x: x["value"]), reverse=True)
        result=result[:10]
        for j in result:
            top10.append(j["word"])
        i["top10"]=top10

def crawling(url):
    global datalist
    word=[]
    data_d={}
    startTime = time.time()
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')
    runtime = time.time()-startTime
    html_contents = re.sub('<.+?>', ' ', str(soup.select('body'))).strip().lower()
    html_contents = re.sub('[^0-9a-zA-Zㄱ-힗]', ' ', html_contents)
    for w in word_tokenize(html_contents):                      #eliminate stopwords in cotents
        if w not in stoplist:
           word.append(w)
    word = [v for v in word if v]
    makeWordDic(word)
    data_d["url"] = url
    data_d["execution"] = 'success'
    data_d["runtime"] = runtime
    data_d["word_count"] = len([v for v in html_contents.split() if v]) # delete ' '
    data_d["contents"] = word
    datalist.append(data_d)


word_d = {}
urls = []
runtime = []
word_count = []
datalist = []
faillist = []
urllist=[]
stoplist = list(stopwords.words("english"))
urls=open("upload/123.txt",mode='r',encoding='utf8')

for f in urls.readlines():
    data_d={}
    url = f.rstrip('\n')
    try:
        res = urlopen(url)
    except HTTPError:
        data_d["url"] = url
        data_d["execution"] = "fail(HTTP)"
        faillist.append(data_d)
        urllist.append(url)
    except URLError:
        data_d["url"] = url
        data_d["execution"] = "fail(URL)"
        faillist.append(data_d)
        urllist.append(url)
    except:
        data_d["url"] = url
        data_d["execution"] = "fail"
        faillist.append(data_d)
        urllist.append(url)
    else:
        if url not in urllist:
            crawling(url)
            urllist.append(url)
        else:
            data_d["url"] = url
            data_d["execution"] = "duplicate"
            faillist.append(data_d)

for i in datalist:
    i["vector"]=makeVector(i["contents"])
   
computeCos()
computeTfidf()

for f in datalist:
    print("url : {}".format(f["url"]))
    print("excution : {}".format(f["execution"]))
    print("runtime : {}".format(f["runtime"]))
    print("count : {}".format(f["word_count"]))
    print("top10 : {}".format(f["top10"]))
    print("top3 : {}".format(f["top3"]))
    print("-------------------------------------------------------------------------")
for f in faillist:
    print("url : {}".format(f["url"]))
    print("excution : {}".format(f["execution"]))
