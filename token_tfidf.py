#import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from tokenizers import Tokenizer
import json

tokenizer = Tokenizer.from_file("kano_py_tokenizer_clean.json")

with open('clean_py.json') as cleanpy:
    data = json.load(cleanpy)

output_data_all=[]
for data_hash in data:
    _, output_data,*_ = data_hash
    tokenize_data = '\n'.join(output_data)
    output = tokenizer.encode(tokenize_data)
    ids = output.ids
    clean_ids = str(ids)[1:-1].replace(',',' ')
    output_data_all.append(clean_ids)

vectorizer = TfidfVectorizer()
vectorizer.fit_transform(output_data_all)
feature_names = vectorizer.get_feature_names()
idf = vectorizer.idf_
feature_names_int = [int(i) for i in feature_names]
dict_idf = dict(zip(feature_names_int, idf))
token_feature = [tokenizer.decode([i]) for i in feature_names_int]
token_idf = dict(zip(token_feature, idf))

token_idf_sort = sorted(token_idf.items(), key = lambda k: token_idf[k[0]])

with open('idf.json','w') as idf:
    json.dump(dict_idf,idf)