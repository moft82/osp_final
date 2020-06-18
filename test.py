a={
    'a':1,
    'b':2
}
b={
    'a':3,
    'b':4
}
c={
    'a':5,
    'b':6
}
list1=[]
list1.append(a.copy())
print(list1)
list1.append(b.copy())
print(list1)
list1.append(c.copy())
print(list1)

list2=[]
for i in range(10):
    url=i
    word=i*10
    string=str(i)+"gn"
    dic={
        "url":url,
        "word":word,
        "string":string
    }
    list2.append(dic)
for i in list2:
    print(i["url"])