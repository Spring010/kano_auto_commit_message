

#Let’s put all those pieces together to build a BERT tokenizer. First, BERT relies on WordPiece, so we instantiate a new Tokenizer with this model:
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
files = [f"data/wikitext-103-raw/wiki.{split}.raw" for split in ["test", "train", "valid"]]
bert_tokenizer.train(files, trainer)

bert_tokenizer.save("data/bert-wiki.json")