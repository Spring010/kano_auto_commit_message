import json
from tokenizers import Tokenizer

with open('clean_comment_py.json') as cleanpy:
    data = json.load(cleanpy)

#clean code data
input_code_all = []
for commit in data:
    *_, input_data = commit
    for diff_data in input_data:
        name, *code_body = diff_data
        code_body_all = [code for code in code_body]
    input_code = [commit[0], code_body_all]
    input_code_all.append(input_code)


def new_func(new_ele,new_join,signal):
    for ele in new_ele:
        join_ele = signal.join(ele)
        if new_ele == new_mark:
            join_ele = ''.join(set(join_ele))
        new_join.append(join_ele)
    return new_join

total_code = []
for commit in input_code_all:
    hashnum, code_mark = commit
    new = []
    for every_code in code_mark:
        code, mark = every_code
        mark_final = None
        new_code = []
        new_mark = []
        for codeline, markline in zip(code,mark):
            if markline != mark_final:
                new_code.append([])
                new_mark.append([])
            new_code[-1].append(codeline)
            new_mark[-1].append(markline)
            mark_final = markline
        new_code_clean = []
        new_mark_clean = []
        new_func(new_code, new_code_clean,signal = '\n')
        new_func(new_mark, new_mark_clean,signal = '')
        new.append([new_code_clean, new_mark_clean])
        total_code.append(new_code_clean)
    commit[1] = new

with open('input_code.json','w') as inputcode:
    json.dump(input_code_all,inputcode)

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
    vocab_size=30000, special_tokens=["[UNK]", "[CLS]", "[SEP]", "[PAD]", "[MASK]"]
)


bert_tokenizer.train_from_iterator(total_code, trainer)

bert_tokenizer.save("kano_input_code_tokenizer.json")
