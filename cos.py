#! /usrl/bin/python
import nltk
import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

text="The subject of Knowledge Discovery and Data Mining concerns the extraction of useful information from data. Since this is also the essence of many subareas of computer science, as well as the field of statistics, KDD can be said to lie at the intersection of statistics, machine learning, data bases, pattern recognition, information retrieval and artificial intelligence."

word_d = {}
sent_list = []

def process_new_sentence(s):
    sent_list.append(s)
    tokenized = word_tokenize(s)
    for word in tokenized:
        if word not in word_d.keys():
            word_d[word]=0
        word_d[word] += 1

def make_vector(i):
    v = []
    s = sent_list[i]
    tokenized = word_tokenize(s)
    for w in word_d.keys():
        val = 0
        for t in tokenized:
            if t==w:
                val +=1
        v.append(val)
    return v

process_new_sentence("yesterday i saw you study in the house")
process_new_sentence("yesterday i saw you study in the school")
v1=make_vector(0)
v2=make_vector(1)
dotpro=np.dot(v1,v2)
coss=dotpro/(np.linalg.norm(v1)*np.linalg.norm(v2))
print(sent_list[0])
print(make_vector(0))
print(sent_list[1])
print(make_vector(1))
print(dotpro)
print(coss)



