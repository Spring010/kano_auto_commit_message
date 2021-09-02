from git import Repo
import git
import subprocess
import json

def main():
#if True:
    repo = Repo.init('/Users/yitongli/pytorch')
    repo.git.checkout('master')
    #output
    outputlist = [(str(commit.hexsha), commit.message) for commit in repo.iter_commits()]
    #input
    listhexsha = [str(commit.hexsha) for commit in repo.iter_commits()]
    rootcommit = subprocess.check_output('git rev-list --max-parents=0 HEAD'.split(), cwd='/Users/yitongli/pytorch')
    rootcommit_set = set(rootcommit.decode().strip().split('\n'))
    listhexsha_set = set(listhexsha)
    normhexsha = listhexsha_set.difference(rootcommit_set)
    normhexsha_list = list(normhexsha)
    rootcommit_list = list(rootcommit_set)
    normdiff = [(i, repo.git.diff(i + '~1', i)) for i in normhexsha_list[:1000]]
    rootdiff = []
    for i in rootcommit_list:
        repo.git.checkout(i)
        rootdiff0 = (i, repo.git.log('-p'))
        rootdiff.append(rootdiff0)

    #merge input and output
    mergeio =[]
    for i in outputlist:
        for j in normdiff:
            if i[0] == j[0]:
                io = (i[0],i[1],j[1])
                mergeio.append(io)

    mergeroot =[]
    for i in outputlist:
        for j in rootdiff:
            if i[0] ==j[0]:
                rio = (i[0],i[1],j[1])
                mergeroot.append(rio)

    #save as json
    with open('norm.json','w') as normjson_file:
        json.dump(mergeio,normjson_file)

    with open("root.json","w") as rootjson_file:
        json.dump(mergeroot,rootjson_file)


    #inspection
    with open('norm.json') as normjson_file:
        normdata = json.load(normjson_file)
        for i in normdata[3]:
            print(i)



if __name__ =="__main__":
     main()