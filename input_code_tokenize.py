from tokenizers import Tokenizer
import json


with open('input_code.json') as inputcode:
    data = json.load(inputcode)
####tokenize

tokenizer = Tokenizer.from_file("kano_input_code_tokenizer.json")

for commit in data:
    hashnum, body = commit
    for input_data in body:
        code, mark = input_data
        code_token = []
        for code_line in code:
            input_tokenize  = tokenizer.encode(code_line)
            code_token.append(input_tokenize.ids)
        for mark_idx in range(len(mark)):
            if mark[mark_idx] == ' ':
                mark[mark_idx] = 1
            elif mark[mark_idx] == '+':
                mark[mark_idx] = 2
            elif mark[mark_idx] == '-':
                mark[mark_idx] = 3
            else:
                raise ValueError('A very specific bad thing happened')
        new_input = [code_token,mark]
    commit[1] = new_input

with open('input_code_tokenize.json','w') as input_code_tokenizer:
    json.dump(data,input_code_tokenizer)