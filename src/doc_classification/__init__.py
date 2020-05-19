import jieba
import jieba.analyse
import numpy as np
import pickle as pkl
import csv
import torch
import torch.nn as nn
from importlib import import_module
import os
import sys

MAX_VOCAB_SIZE = 10000  # 词表长度限制
UNK, PAD = '<UNK>', '的'  # 未知字，padding符号

config = None
vocab = None


def build_dataset(document):
    tokenizer = lambda x: x.split()  # 以空格隔开，word-level

    def load_dataset(document, pad_size=32):
        content = document.strip()
        # print(content)
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

    return load_dataset(document, config.pad_size)


def classify(model, document):
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


# 'TextRCNN'  # TextCNN, TextRNN, FastText, TextRCNN, TextRNN_Att, DPCNN, Transformer
def loading_cnn_model(dataset='../doc_classification/court', embedding='embedding.npz', model_name='DPCNN'):
    # loading config

    x = import_module('.models.' + model_name, package='doc_classification')
    global config
    config = x.Config(dataset, embedding)

    # loading vocab
    if os.path.exists(config.vocab_path):
        global vocab
        vocab = pkl.load(open(config.vocab_path, 'rb'))
    config.n_vocab = len(vocab)

    # loading cnn model
    model = x.Model(config).to(config.device)

    print(model_name, 'loaded:')
    print(model.parameters)

    return model


# input: pandas.DataFrame list
def classify_doc(model, doc_data_frame):

    for i, row in doc_data_frame.iterrows():
        document = row.content
        document_cut = jieba.cut(document)
        result = ' '.join(document_cut).split('。')
        document_clean = ''
        for index, res in enumerate(result):
            res = removePunctuation(res).strip()
            document_clean = document_clean + res + ' '
        document = build_dataset(document_clean)
        document = torch.tensor(document, dtype=torch.long)
        label = classify(model, document)
        row["label"] = label
    return doc_data_frame

