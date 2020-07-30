import pandas
import jieba

from event_extraction import trim_list, mark_constants, label_constants, injury_keyword_reg
from product_ner.utils.data_process import save_json_data


def start_up(file_list):
    for file_name in file_list:
        try:
            data = get_csv_data(file_name)
        except FileNotFoundError:
            print("file: %s.csv doesn't exists." % file_name)
            continue
        data_list = do_event_extraction(data)
        save_json_data("./results/" + file_name + ".json", data_list)
        print(file_name, 'ended')


def get_csv_data(file_name):
    return pandas.read_csv('./data/%s.csv' % file_name, delimiter=' ', header=None)


def do_event_extraction(data, *args):
    data_list = []

    for index, row in data.iterrows():

        sentence = row[1]
        keyword = row[2]

        sentence_list_split_by_kw = sentence.split(keyword)
        sentence_cut_part1 = list(jieba.cut(sentence_list_split_by_kw[0]))
        sentence_cut_part2 = list(jieba.cut(sentence_list_split_by_kw[1]))
        sentence_cut = sentence_cut_part1\
            + [keyword]\
            + sentence_cut_part2
        sentence_cut = trim_list(sentence_cut)

        if not len(sentence_cut):
            continue

        data_item = {
            'words': sentence_cut,
            'marks': [mark_constants['A']] * len(sentence_cut),
            'pos_taggings': [str(n) for n in range(len(sentence_cut))],
            'label': label_constants['TRIGGER']
        }

        keyword_index = len(sentence_cut_part1)
        data_item['marks'][keyword_index] = mark_constants['B']

        data_list.append(data_item)
    return data_list
