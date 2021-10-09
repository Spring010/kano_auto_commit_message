import torch
from io import open
import unicodedata
import string
import re
import random
import torch.nn as nn
from torch import optim
import torch.nn.functional as F
from nltk.translate.bleu_score import corpus_bleu
import json

MAX_LENGTH = 10000


class EncoderRNN(nn.Module):
    def __init__(self, input_size, hidden_size):
        super(EncoderRNN, self).__init__()
        self.hidden_size = hidden_size

        self.embedding = nn.Embedding(input_size, hidden_size)
        self.gru = nn.GRU(hidden_size, hidden_size)

    def forward(self, input, hidden):
        embedded = self.embedding(input).view(1, 1, -1)
        output = embedded
        output, hidden = self.gru(output, hidden)
        return output, hidden

    def initHidden(self):
        return torch.zeros(1, 1, self.hidden_size, device=device)



class AttnDecoderRNN(nn.Module):
    def __init__(self, hidden_size, output_size, dropout_p=0.1, max_length=MAX_LENGTH):
        super(AttnDecoderRNN, self).__init__()
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.dropout_p = dropout_p
        self.max_length = max_length

        self.embedding = nn.Embedding(self.output_size, self.hidden_size)
        self.attn = nn.Linear(self.hidden_size * 2, self.max_length)
        self.attn_combine = nn.Linear(self.hidden_size * 2, self.hidden_size)
        self.dropout = nn.Dropout(self.dropout_p)
        self.gru = nn.GRU(self.hidden_size, self.hidden_size)
        self.out = nn.Linear(self.hidden_size, self.output_size)

    def forward(self, input, hidden, encoder_outputs):
        embedded = self.embedding(input).view(1, 1, -1)
        embedded = self.dropout(embedded)

        attn_weights = F.softmax(
            self.attn(torch.cat((embedded[0], hidden[0]), 1)), dim=1)
        attn_applied = torch.bmm(attn_weights.unsqueeze(0),
                                 encoder_outputs.unsqueeze(0))

        output = torch.cat((embedded[0], attn_applied[0]), 1)
        output = self.attn_combine(output).unsqueeze(0)

        output = F.relu(output)
        output, hidden = self.gru(output, hidden)

        output = F.log_softmax(self.out(output[0]), dim=1)
        return output, hidden, attn_weights

    def initHidden(self):
        return torch.zeros(1, 1, self.hidden_size, device=device)


def train(input_tensor, target_tensor, encoder, decoder, encoder_optimizer, decoder_optimizer, teacher_forcing_ratio=0.5, max_length=MAX_LENGTH):
    encoder_hidden = encoder.initHidden()

    encoder_optimizer.zero_grad()
    decoder_optimizer.zero_grad()

    input_length = input_tensor.size(0)
    target_length = target_tensor.size(0)

    encoder_outputs = torch.zeros(max_length, encoder.hidden_size, device=device)

    loss = 0

    for ei in range(input_length):
        encoder_output, encoder_hidden = encoder(
            input_tensor[ei], encoder_hidden)
        encoder_outputs[ei] = encoder_output[0, 0]

    decoder_input = torch.tensor([[SOS_token]], device=device)

    decoder_hidden = encoder_hidden

    use_teacher_forcing = True if random.random() < teacher_forcing_ratio else False
    loss_fn = torch.nn.NLLLoss()
    output_vocabsize = py_tokenizer.get_vocab_size()
    if use_teacher_forcing:
        # Teacher forcing: Feed the target as the next input
        for di in range(target_length):
            decoder_output, decoder_hidden, decoder_attention = decoder(
                decoder_input, decoder_hidden, encoder_outputs)

            loss += loss_fn(decoder_output, target_tensor[di])
            decoder_input = target_tensor[di]  # Teacher forcing

    else:
        # Without teacher forcing: use its own predictions as the next input
        for di in range(target_length):
            decoder_output, decoder_hidden, decoder_attention = decoder(
                decoder_input, decoder_hidden, encoder_outputs)
            topv, topi = decoder_output.topk(1)
            decoder_input = topi.squeeze().detach()  # detach from history as input

            loss += loss_fn(decoder_output, target_tensor[di])
            if decoder_input.item() == EOS_token:
                break

    loss.backward()

    encoder_optimizer.step()
    decoder_optimizer.step()

    return loss.item() / target_length


def trainIters(encoder, decoder, train_dataset, n_epochs=1, learning_rate=0.01):
    encoder_optimizer = optim.Adagrad(encoder.parameters(), lr=learning_rate)
    decoder_optimizer = optim.Adagrad(decoder.parameters(), lr=learning_rate)
    for epoch in range(n_epochs):
        random.shuffle(train_dataset)
        losses = []
        for index, data in enumerate(train_dataset):
            (input_tensor, input_segment), target_tensor = data
            #(input_tensor, input_segment), target_tensor = train_dataset[0]
            input_tensor = input_tensor.unsqueeze(-1)
            target_tensor = target_tensor.unsqueeze(-1)
            loss = train(input_tensor, target_tensor, encoder,
                         decoder, encoder_optimizer, decoder_optimizer)
            losses.append(loss)
            print(index)
        loss_avg = torch.mean(torch.tensor(losses))
        print('epoch=', epoch, ', loss=', loss_avg)
        print('evaluating train')
        evaluateRandomly(encoder,decoder,train_dataset)
        print('evaluating validation')
        evaluateRandomly(encoder,decoder,validation_dataset)

    return loss_avg

def evaluate(encoder, decoder, input_tensor, max_length=MAX_LENGTH):
    with torch.no_grad():
        input_length = input_tensor.size()[0]
        encoder_hidden = encoder.initHidden()

        encoder_outputs = torch.zeros(max_length, encoder.hidden_size, device=device)

        for ei in range(input_length):
            encoder_output, encoder_hidden = encoder(input_tensor[ei],
                                                     encoder_hidden)
            encoder_outputs[ei] += encoder_output[0, 0]

        decoder_input = torch.tensor([[SOS_token]], device=device)  # SOS

        decoder_hidden = encoder_hidden

        decoded_words = []
        decoder_attentions = torch.zeros(max_length, max_length)

        for di in range(max_length):
            decoder_output, decoder_hidden, decoder_attention = decoder(
                decoder_input, decoder_hidden, encoder_outputs)
            decoder_attentions[di] = decoder_attention.data
            topv, topi = decoder_output.data.topk(1)
            if topi.item() == EOS_token:
                decoded_words.append(EOS_token)
                break
            else:
                decoded_words.append(topi.item())

            decoder_input = topi.squeeze().detach()
        return decoded_words, decoder_attentions[:di + 1]


def evaluateRandomly(encoder, decoder, validation_dataset, n=10):
    output = []
    target = []
    for i in range(n):
        (input_tensor, input_segment), target_tensor = random.choice(validation_dataset)
        #(input_tensor, input_segment), target_tensor = train_dataset[0]
        output_words, attentions = evaluate(encoder, decoder, input_tensor)
        output_words = py_tokenizer.decode(output_words)
        train_words = py_tokenizer.decode(list(target_tensor))
        print(output_words)
        print('--------------')
        print(train_words)
        print('==============')
        output.append(output_words)
        target.append([train_words])
    references = target
    candidates = output
    score = corpus_bleu(references,candidates)
    #output_sentence = ' '.join(output_words)
    print('score: ', score)



device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

inputdata = torch.load('input.pt')
outputdata = torch.load('output.pt')
inputdata = [[d.to(device) for d in data] for data in inputdata]
outputdata = [d.to(device) for d in outputdata]

data = list(zip(inputdata,outputdata))
data = data[:3000]
train_size = int(0.8 * len(data))
validation_size = int(0.5 * (len(data) - train_size))
test_size = len(data) - train_size - validation_size
train_dataset = data[:train_size]
validation_dataset = data[train_size:train_size+validation_size]
test_dataset = data[-test_size:]



from tokenizers import Tokenizer
input_code_tokenizer = Tokenizer.from_file("kano_input_code_tokenizer.json")
py_tokenizer = Tokenizer.from_file("kano_py_tokenizer.json")
SOS_token = py_tokenizer.token_to_id("[CLS]")
EOS_token = py_tokenizer.token_to_id("[SEP]")

# with open('idf.json') as idf:
#     weight_idf = json.load(idf)
# weight_idf = {int(k):v for k,v in weight_idf.items()}
# default_weight = torch.mean(torch.tensor(list(weight_idf.values())))
# output_weight_list = [weight_idf.get(i,default_weight) for i in range(py_tokenizer.get_vocab_size())]
# output_weight = torch.tensor(output_weight_list)
# output_weight = output_weight.to(device)


hidden_size = 1024
encoder1 = EncoderRNN(input_code_tokenizer.get_vocab_size(), hidden_size).to(device)
attn_decoder1 = AttnDecoderRNN(hidden_size, py_tokenizer.get_vocab_size(), dropout_p=0.1).to(device)

loss = trainIters(encoder1, attn_decoder1, train_dataset, n_epochs=100, learning_rate=0.001)

#evaluateRandomly(encoder1, attn_decoder1,validation_dataset)