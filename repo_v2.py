from git import Repo
import git
import subprocess


def main():
    repo = Repo.init('/Users/yitongli/pytorch')
    #output
    list = [(str(commit.hexsha), commit.message) for commit in repo.iter_commits()]
    #input
    #gitdiff0 = [(list[i][0], repo.git.diff(list[i][0]+'~1',list[i][0])) for i in range(len(list)-1)]
    rootcommit = subprocess.check_output('git rev-list --max-parents=0 HEAD'.split(), cwd='/Users/yitongli/pytorch')
    rootcommit_set = set(rootcommit)
    gitdiff0=[]
    sumerr=[]
    for i in range(len(list)):
        print(i,len(list))
        try:
           diff_cleaner = (list[i][0], repo.git.diff(list[i][0] + '~1', list[i][0]))
        except git.exc.GitCommandError as err:
            print('diff is none')
            print(err)
            sumerr.append(list[i][0])
        else:
            gitdiff0.append(diff_cleaner)


if __name__ =="__main__":
    main()