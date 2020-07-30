from product_ner.utils.data_process import get_keyword_data, get_keyword_dict, get_data_file_name, get_csv_data, \
    save_csv_data, save_json_data
from product_ner.utils.fact_process import get_fact
from product_ner.algrithom.reg import get_sentence_list
from .utils import removePunctuation
import re
import jieba

INJURY_KEYWORD_PATTERN = "伤害|爆炸|起火|自燃|死亡|身亡|火灾|事故|着火|刺激|故障|烧毁|引燃|毁损|损坏|失火|燃烧|受损|受伤|泄漏|辐射|原因|导致"
injury_keyword_reg = re.compile(INJURY_KEYWORD_PATTERN)
label_constants = {
    'NONE': 'None',
    'TRIGGER': 'TRIGGER'
}
mark_constants = {
    'A': 'A',
    'B': 'B'
}


def startup():
    keyword_data = get_keyword_data()
    keyword_dict = get_keyword_dict(keyword_data)
    for keyword, incident_list in keyword_dict.items():

        for incident in incident_list:
            file_name = get_data_file_name(keyword, incident)

            try:
                data = get_csv_data(file_name)
            except FileNotFoundError:
                print("file: %s.csv doesn't exists." % file_name)
                continue
            data_list = do_event_extraction(data, keyword, incident)
            save_json_data("./data/" + file_name + ".json", data_list)
            print(file_name, 'ended')


def do_event_extraction(data, *args):
    data_list = []

    for index, row in data.iterrows():

        # product = row['product']
        # incident = row['criteria']

        fact_text = get_fact(row)
        if not fact_text:
            fact_text = row['content']

        sentence_list = get_sentence_list(fact_text)

        for sentence in sentence_list:
            if not len(sentence):
                continue
            sentence_cut = list(jieba.cut(sentence))
            sentence_cut = trim_list(sentence_cut)
            if not len(sentence_cut):
                continue

            injury_flag = False
            data = {
                'words': sentence_cut,
                'marks': [mark_constants['A']] * len(sentence_cut),
                'pos_taggings': [str(n) for n in range(len(sentence_cut))],
                'label': label_constants['NONE']
            }
            for index, word in enumerate(sentence_cut):
                if injury_keyword_reg.search(word):
                    data['marks'][index] = mark_constants['B']
                    data['label'] = label_constants['TRIGGER']
                    injury_flag = True
                    break
            if not injury_flag:
                data['marks'][0] = mark_constants['B']

            data_list.append(data)
    return data_list


def trim_list(li):
    for index in range((len(li) - 1), -1, -1):
        item = removePunctuation(li[index])
        if not_empty(item):
            li[index] = item.strip()
        else:
            li.pop(index)
    return list(li)


def not_empty(s):
    return s and s.strip()
