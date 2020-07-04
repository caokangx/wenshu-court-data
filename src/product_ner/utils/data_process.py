import json

import pandas


def get_keyword_dict(csv_data):
    keyword_dict = {}
    for index, row in csv_data.iterrows():
        line_str = row.values[0]
        key_word_array = line_str.split('：')
        keyword_dict[key_word_array[0]] = key_word_array[1].split('，')
    return keyword_dict


def get_data_file_name(key, value):
    return str(key) + str(value)


def get_keyword_data():
    return pandas.read_csv('../../wenshu-court-data/config/关键词')


def get_csv_data(file_name):
    return pandas.read_csv('../../wenshu-court-data/data/%s.csv' % file_name, usecols=['docId', 'content'])


def save_csv_data(file_path, data_list, columns, index=False):
    df = pandas.DataFrame(data_list, columns=columns)
    df.to_csv(file_path, index=index)


def save_json_data(file_path, data):
    with open(file_path, "w", encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)
