from product_ner.utils.data_process import get_keyword_data, get_keyword_dict, get_data_file_name, get_csv_data, save_csv_data
from product_ner.utils.fact_process import get_fact
from product_ner.algrithom.reg import get_sentence_list
import re
import jieba

INJURY_KEYWORD_PATTERN = "伤害|爆炸|起火|自燃|死亡|身亡|火灾|事故|着火|刺激|故障"
injury_keyword_reg = re.compile(INJURY_KEYWORD_PATTERN)


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
            save_csv_data("./data/" + file_name + ".csv", data_list, ['word', 'label'])
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
            sentence_cut = jieba.cut(sentence)
            for word in sentence_cut:
                label = 1 if injury_keyword_reg.search(word) else 0
                data_list.append({
                    'word': word,
                    'label': label
                })
                # print("word:", word, "label:", label)
    return data_list

