import json
from tokenizers import Tokenizer

with open('clean_py.json') as cleanpy:
    data = json.load(cleanpy)

input_name_all = []
for commit in data:
    *_, input_data = commit
    input_name = ' '.join([diff_data[0] for diff_data in input_data])
    input_name_all.append(input_name)

#tokenizer
from tokenizers import Tokenizer
from tokenizers.models import WordPiece

bert_tokenizer = Tokenizer(WordPiece(unk_token="[UNK]"))
#Then we know that BERT preprocesses texts by removing accents and lowercasing. We also use a unicode normalizer:
from tokenizers import normalizers
from tokenizers.normalizers import Lowercase, NFD, StripAccents

bert_tokenizer.normalizer = normalizers.Sequence([NFD(), Lowercase(), StripAccents()])


#The pre-tokenizer is just splitting on whitespace and punctuation:
from tokenizers.pre_tokenizers import Whitespace

bert_tokenizer.pre_tokenizer = Whitespace()
#And the post-processing uses the template we saw in the previous section:
from tokenizers.processors import TemplateProcessing

bert_tokenizer.post_processor = TemplateProcessing(
    single="[CLS] $A [SEP]",
    pair="[CLS] $A [SEP] $B:1 [SEP]:1",
    special_tokens=[
        ("[CLS]", 1),
        ("[SEP]", 2),
    ],
)
#We can use this tokenizer and train on it on wikitext like in the Quicktour:
from tokenizers.trainers import WordPieceTrainer

trainer = WordPieceTrainer(
    vocab_size=30522, special_tokens=["[UNK]", "[CLS]", "[SEP]", "[PAD]", "[MASK]"]
)


bert_tokenizer.train_from_iterator(input_name_all, trainer)

bert_tokenizer.save("kano_input_name_tokenizer.json")

####tokenize


tokenizer = Tokenizer.from_file("kano_input_name_tokenizer.json")

input_name_token = []
for commit in data:
    *_, input_data = commit
    input_name = ' '.join([diff_data[0] for diff_data in input_data])
    input_tokenize  = tokenizer.encode(input_name)
    input_name_segment = [0] * len(input_tokenize.ids)
    input_name_token.append([commit[0],input_tokenize.ids, input_name_segment])


#tokenizer.decode(input_name_token[1][1])

with open('input_name_tokenizer.json','w') as input_name_tokenizer:
    json.dump(input_name_token,input_name_tokenizer)