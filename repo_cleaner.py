from git import Repo
import git
import subprocess
import json
#from repo_v3 import main

#main()
def total_clean(json1,json2):
    with open(json1) as normjson_file:
        normdata = json.load(normjson_file)

    # clean data further
    deleteset = ['Test Plan:', 'Pull Request', 'Reviewed By:', 'Differential Revision:', 'Pulled By:',
                 'fbshipit-source-id:']

    def cleanup(normdata,numm):
        normdata_cleaner=[]
        for i in normdata:
            if numm ==2:
                cleaner0 = [j for j in i[1].split('\n') if j]
            else:
                cleaner0 = i[1]
            cleaner1 = [k for k in cleaner0 if " ".join(k.split()[:numm]) not in deleteset]
            cleaner_final = [i[0],cleaner1,i[2]]
            normdata_cleaner.append(cleaner_final)
        return normdata_cleaner

    normdata1 = cleanup(normdata,2)
    normdata2 = cleanup(normdata1,1)

    #save
    with open(json2,'w') as cleannorm_file:
        json.dump(normdata2,cleannorm_file)

total_clean1 = total_clean('norm.json','cleannorm.json')
total_clean2 = total_clean('root.json','cleanroot.json')