import json
import re

with open('clean_py.json') as pyjson:
    data = json.load(pyjson)

data_full = [commit for commit in data if not (commit[1][0].startswith('Merge pull request') or commit[1][0].startswith('Merge branch'))]

#trouble = [i for i in data if i[0] == '456364729ef4c1989b4789453bd2766a69f7a099']

output_comment = []
output_summary = []
patterns = [
    r'\(#\d+\)',
    r'\#\d+',
    r'\# \d+',
    r'\[auto\] Update onnx to [0-9a-z]{7} \- ',
    r'D\d{8}',
]
for commit in data_full:
    hashnum, output,*_ = commit
    comment = output[0]
    for pattern in patterns:
        while True:
            match = re.search(pattern, comment)
            if not match:
                break
            index,rindex = match.span()
            comment = comment[:index]+comment[rindex:]
    summary = output[1:]
    commit_comment = [hashnum,comment ,*_]
    commit_summary = [hashnum,summary,*_]
    output_comment.append(commit_comment)
    output_summary.append(commit_summary)


output_comment = [i for i in output_comment if i[1] != 'Updating submodules']
unwanted = ['Update onnx to onnx/onnx@','Update onnx submodule to onnx/onnx@','Revert ','Merge commit ','Back out ','Backed out changeset ','Automatic update of fbcode/foxi to ','Automated submodule update: ',"' ' ==> ' ' "]
output_comment = [i for i in output_comment if not any(i[1].startswith(p) for p in unwanted)]
output_comment = [i for i in output_comment if not (i[1].startswith("Add '") and "' from commit '" in i[1])]

output_comment = [i for i in output_comment if i[1].replace(' ','').replace('.','')]

with open('clean_comment_py.json','w') as comment_pyjson:
    json.dump(output_comment ,comment_pyjson)

with open('clean_summary_py.json','w') as summary_pyjson:
    json.dump(output_summary ,summary_pyjson)