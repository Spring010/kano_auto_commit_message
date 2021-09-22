import json


with open('input_name_tokenizer.json') as input_name_tokenizer:
    data_name = json.load(input_name_tokenizer)


with open('input_code_tokenize.json') as input_code_tokenizer:
    data_code = json.load(input_code_tokenizer)

clean_data_code = []
for commit in data_code:
    hashnum, body = commit
    body_code = []
    body_mark = []
    for each_code in body:
        code, mark = each_code
        mark_merge = []
        for code_line, mark_line in zip(code,mark):
             mark_mul = [mark_line] * len(code_line)
             mark_merge.append(mark_mul)
        mark_congre = [i for mark in mark_merge for i in mark]
        code_congre = [i for codeline in code for i in codeline]
        body_code.append(code_congre)
        body_mark.append(mark_congre)
    clean_code = [i for body in body_code for i in body]
    clean_mark = [i for body in body_mark for i in body]
    clean_data_code.append([hashnum,clean_code,clean_mark])

new_token = []
new_segment = []
for name,code in zip(data_name,clean_data_code):
    name_hashnum, name_token, name_segment = name
    code_hashnum, code_token, code_segment = code
    if name_hashnum == code_hashnum:
        clean_token = [name_hashnum,name_token,code_token]
        clean_segment = [name_hashnum,name_segment,code_segment]
        new_token.append(clean_token)
        new_segment.append(clean_segment)

with open('input_token_final.json','w') as input_token_final:
    json.dump(new_token,input_token_final)

with open('input_segment_final.json','w') as input_segment_final:
    json.dump(new_segment,input_segment_final)

with open('input_code_final.json','w') as input_code_final:
    json.dump(clean_data_code,input_code_final)