from git import Repo
import git
import subprocess
import json
#from repo_v3 import main
import re


with open('cleannorm.json') as aanorm:
    aadara = json.load(aanorm)

aadara =[i for i in aadara if i[2]]

#pick up .py
aadara_diffat=[]
for j in aadara:
    # split 'diff --git'
    *_, diff = j
    diffsplit = diff.split('diff --git ')[1:]
    # split @@ under diffsplit
    atatsplit = [i.split('\n@@') for i in diffsplit]
    # pick up .py
    pickuppy = [i[0][-3:] for i in atatsplit]
    #alltail
    if all(i == '.py' for i in pickuppy):
        jj = [*_,diff,atatsplit]
        aadara_diffat.append(jj)


#clean dirty
def clean_item(item, pat):
    return item[item.find(pat)+len(pat):]

for commit in aadara_diffat:
    _, _, _, parsed_diff = commit
    parsed_diff_clean = []
    for file_diff in parsed_diff:
        header, *body = file_diff
        pat = '\n+++ b/'
        header_clean = clean_item(header, pat)
        body_clean = [clean_item(item, ' @@ ') for item in body]
        parsed_diff_clean.append([header_clean,*body_clean])
    commit[3] = parsed_diff_clean


#remove + -,and mark
def replace_all(text, dic):
    for i, j in dic.items():
        text = text.replace(i, j, 1)
    return text

for commit in aadara_diffat:
    _, _, _, parsed_diff_clean =commit
    for file_diff in parsed_diff_clean:
        header, *body_clean = file_diff
        func_final_all = []
        for item in body_clean:
            code_func = item.split('\n')
            code_func_clean = [code for code in code_func if code]
            # replace elements in list-str
            d_replace ={'+': ' ', '-': ' '}
            code_func_clean_nosignal = [replace_all(codeline, d_replace) if codeline[0] in [*d_replace] else codeline for codeline in code_func_clean ]
            signal_two = [codeline[0] for codeline in code_func_clean]
            signal_two_new = signal_two
            sigset_mul = ('+', '-', ' ')
            #replace elements in list
            signal_two_new_clean = [' ' if ele not in sigset_mul else ele for ele in signal_two_new ]
            func_final_cleaner = [code_func_clean_nosignal,  signal_two_new_clean]
            func_final_all.append(func_final_cleaner)
        file_diff[1:] = func_final_all
                # import pdb;pdb.set_trace()
                # pass


with open('clean_py.json','w') as pyjson:
    json.dump(aadara_diffat,pyjson)