from tokenizers import Tokenizer
import json

tokenizer = Tokenizer.from_file("kano_py_tokenizer.json")

with open('clean_py.json') as cleanpy:
    data = json.load(cleanpy)

output_data_all=[]
for data_hash in data:
    _, output_data,*_ = data_hash
    tokenize_data = '\n'.join(output_data)
    output = tokenizer.encode(tokenize_data)
    output_data_all.append([data_hash[0],output.ids])

#tokenizer.decode(output_data_all[1][1])

with open('output_tokenizer.json','w') as output_token:
    json.dump(output_data_all,output_token)
