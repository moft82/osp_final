#! /usrl/bin/python
import nltk
import numpy as np
import math
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

word_d = {}
sent_list = []

def process_new_sentence(s):
    sent_list.append(s)
    tokenized = word_tokenize(s)
    for word in tokenized:
        if word not in word_d.keys():
            word_d[word]=0
        word_d[word] += 1

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

    process_new_sentence("this is a good day to study what happend to your study plan today you need more study")
process_new_sentence("i need a coffee but coffee is bad for your health")
process_new_sentence("my cat jumped off the car today")
process_new_sentence("let's study together at the cafe")
process_new_sentence("yesterday i saw you study in the house")
process_new_sentence("where were you yesterday i have been looking for you all over")
idf_d = compute_idf()
for i in range(0,len(sent_list)):
    tf_d = compute_tf(sent_list[i])
    for word,tfval in tf_d.items():
        print(word, tfval*idf_d[word])
print(" ")