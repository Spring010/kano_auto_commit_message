import json

with open('clean_comment_py.json') as comment_pyjson:
    data = json.load(comment_pyjson)

trydata = []
for i in data:
    _,comment,*_ =i
    trydata.append(comment)

trydata.sort()

for i in trydata:
    print(i)
    #print('-------------------')