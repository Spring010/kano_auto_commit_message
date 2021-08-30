
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
logs=repo.git.log("-p","--format=' }\n{'Hash': '%H', 'Commit-m': '%f', 'Summary': '%b',\n 'gitdiff': '")
logs_split = logs.splitlines()
type(logs_split)
# with open("txt.txt", "w") as f:
#     for t in logs_split[:1000]:
#         print(t, file=f)


# ID_mark = [ i for i in range(len(logs_split)) if logs_split[i] == '<<<<<<<ID>>>>>>>' ]
# gitdiff_mark = [ i[0:11] for i in logs_split]
# gitdiff_mark_index = [gitdiff_mark.index('diff --git ',ID_mark[i]) for i in range(len(ID_mark))]
# logs_split_cleaner = logs_split
# for i in gitdiff_mark_index:
#     logs_split_cleaner[i-1] = 'gitdiff:'
#
#
# filter(lambda x: ' A  ' in x, logs_split_cleaner)
logs_split_cleaner = logs_split
for i in logs_split_cleaner[:1000]:
    print(i)




# logs_H=repo.git.log("--pretty=format:(%H,%f,%b)")
# logs_split_H = logs_H.splitlines()
# for i in logs_split_H[:50]:
#     print(i)



