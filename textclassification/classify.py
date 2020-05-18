import jieba
import jieba.analyse
import numpy as np
import pickle as pkl
import csv
import torch
import torch.nn as nn
from importlib import import_module
import os

MAX_VOCAB_SIZE = 10000  # 词表长度限制
UNK, PAD = '<UNK>', '的'  # 未知字，padding符号

def build_dataset(config, vocab, document):
    tokenizer = lambda x: x.split()  # 以空格隔开，word-level

    def load_dataset(document, pad_size=32):
        content = document.strip()
        #print(content)
        words_line = []
        token = tokenizer(content)
        seq_len = len(token)
        if pad_size:
            if len(token) < pad_size:
                token.extend([PAD] * (pad_size - len(token)))
            else:
                token = token[:pad_size]
                seq_len = pad_size
        # word to id
        for word in token:
            words_line.append(vocab.get(word, vocab.get(UNK)))
        return words_line
    test = load_dataset(document, config.pad_size)
    return test


def test(config, model, document):
    # test
    model.load_state_dict(torch.load(config.save_path, map_location=torch.device('cpu')))
    model.eval()
    label = evaluate(model, document)
    return label



def evaluate(model, document):
    model.eval()
    with torch.no_grad():
        outputs = model(document)
        predic = torch.max(outputs.data, 0)[1].cpu().numpy()
    return predic



punctuation = '！，；：？"\'（）.、×“”《》[]!,;:?()-_1234567890\\+-x÷/%#@{}【】／'
def removePunctuation(text):
    for c in punctuation:
        text = text.replace(c, "")
    return text


dataset = 'court'  # 数据集
embedding = 'embedding.npz'
model_name = 'DPCNN'  # 'TextRCNN'  # TextCNN, TextRNN, FastText, TextRCNN, TextRNN_Att, DPCNN, Transformer
ues_word = True
x = import_module('models.' + model_name)
config = x.Config(dataset, embedding)
if os.path.exists(config.vocab_path):
    vocab = pkl.load(open(config.vocab_path, 'rb'))
# train
config.n_vocab = len(vocab)
model = x.Model(config).to(config.device)
print(model.parameters)



#文件位置需要改为自己的存放路径
#将文本分词
f = open('test.csv','r') #打开文件
reader = csv.reader(f)
for item in reader:
    if reader.line_num != 1:
        document = item[12] + item[13]
        document_cut = jieba.cut(document)
        result = ' '.join(document_cut).split('。')
        document_clean = ''
        for index, res in enumerate(result):
            res = removePunctuation(res).strip()
            document_clean =  document_clean + res + ' '
        print(document_clean)
        document = build_dataset(config, vocab, document_clean)
        document = torch.tensor(document, dtype=torch.long)
        label = test(config, model, document)
        print(label)






