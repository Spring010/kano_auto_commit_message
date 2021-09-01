from git import Repo
import git
import subprocess

def main():
#if True:
    repo = Repo.init('/Users/yitongli/pytorch')
    #output
    outputlist = [(str(commit.hexsha), commit.message) for commit in repo.iter_commits()]
    #input
    listhexsha = [str(commit.hexsha) for commit in repo.iter_commits()]
    repo.git.checkout('master')
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

if __name__ =="__main__":
    main()