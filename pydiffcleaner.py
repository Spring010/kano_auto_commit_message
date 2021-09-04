from git import Repo
import git
import subprocess
import json
#from repo_v3 import main
import re


with open('cleannorm.json') as aanorm:
    aadara = json.load(aanorm)


diffatall_text=[]
aadara_diffat=[]
for j in aadara:
    # find all 'diff --git'
    findalldiff = [m.start() for m in re.finditer('diff --git', j[2])]
    # find @@ under diff git
    atpall = [j[2].find('@@ ',i) for i in findalldiff]
    #assert
    assert len(findalldiff) == len(atpall)
    # tail[-3:]
    diffatall=[j[2][findalldiff[i]:atpall[i]][-3:] for i in range(len(findalldiff))]
    #alltail
    if all(i == 'py\n' for i in diffatall):
        aadara_diffat.append(j)
        diffatall_text.append(diffatall)



