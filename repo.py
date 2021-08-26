
from git import Repo
repo = Repo.init('/Users/yitongli/pytorch')

print([str(commit.summary) for commit in repo.iter_commits()][1])
print([str(commit.count) for commit in repo.iter_commits()][0])
print([str(commit.size) for commit in repo.iter_commits()][0])
print([str(commit.hexsha) for commit in repo.iter_commits()][0])
[commit.message for commit in repo.iter_commits()][2]

