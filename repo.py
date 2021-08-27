
from git import Repo
repo = Repo.init('/Users/yitongli/pytorch')

# print([str(commit.summary) for commit in repo.iter_commits()][1])
# print([str(commit.count) for commit in repo.iter_commits()][0])
# print([str(commit.size) for commit in repo.iter_commits()][0])
# print([str(commit.hexsha) for commit in repo.iter_commits()][0])
# print([commit.message for commit in repo.iter_commits()][2])
# repo.git.diff('HEAD~1')

#Reference:https://azzamsa.com/n/gitpython-intro/
#Unwrapped git functionality
logs=repo.git.log("-p","--raw")
logs_split = logs.splitlines()
type(logs_split)
for i in logs_split[500:600]:
    print(i)

logs_H=repo.git.log("--pretty=format:(%H,%f,%b)")
logs_split_H = logs_H.splitlines()
for i in logs_split_H[:50]:
    print(i)

