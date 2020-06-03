from product_ner.utils.constants import fact_start_reg_obj, fact_end_reg_obj

from product_ner.utils.reg import prod_reg_obj_list, prod_split_reg_obj


#  对每个句子进行规则匹配，不同的规则自己定义，规则之间有权重（有正，有负），最后取总和最高者
def get_prod_info_reg(fact_text, keyword, incident):
    sentence_list = prod_split_reg_obj.split(fact_text)
    sentence_list = strip_list(sentence_list)

    match_info_list = []

    for sentence in sentence_list:
        match_info = {
            "weight": 0,
            "match_reg_list": [],
            "context": ""
        }
        for recognize_obj in prod_reg_obj_list:
            recognize_func = recognize_obj["function"]
            recognize_weight = recognize_obj["weight"]
            product_info = recognize_func(sentence, keyword)
            if product_info:
                match_info["weight"] += recognize_weight
                match_info["match_reg_list"].append(recognize_obj["description"])
                match_info["context"] = sentence

        if len(match_info["match_reg_list"]) > 0:
            match_info_list.append(match_info)

    if len(match_info_list) > 0:
        match_info_list.sort(key=lambda k: (k.get('weight', 0)), reverse=True)
        return match_info_list

    return None



def get_fact_start_pos_reg(row):
    content = row.content if row.content else ""
    docId = row.docId if row.docId else ""

    match_len = 0
    fact_start_dict = {
        'start': -1,
        'end': -1,
        'text': ''
    }

    for match in fact_start_reg_obj.finditer(content):
        if len(match.group()) > match_len:
            fact_start_dict['end'] = match.end()
            fact_start_dict['start'] = match.start()
            match_len = len(match.group())
    if match_len > 0:
        fact_start_dict['text'] = content[fact_start_dict['start']:fact_start_dict['end']]
    else:
        fact_start_dict['text'] = 'fact: No fact found'
    # print('docId:', docId, ' text:', fact_start_dict['text'])
    return fact_start_dict


def get_fact_end_pos_reg(fact_start_dict, row):
    content = row.content if row.content else ""

    fact_end_dict = {
        'start': -1,
        'end': -1,
        'text': ''
    }

    start_index = fact_start_dict['end']
    match = fact_end_reg_obj.search(content, pos=start_index)

    if match and len(match.group()) > 0:
        fact_end_dict['end'] = match.end()
        fact_end_dict['start'] = match.start()
        fact_end_dict['text'] = match.group()
    return fact_end_dict


def get_fact_reg(row):
    start_dict = get_fact_start_pos_reg(row)
    end_dict = get_fact_end_pos_reg(start_dict, row)

    content = row.content
    start_index = start_dict['start']
    end_index = end_dict['start']

    if end_index > start_index >= 0:
        fact = content[start_index: end_index]
    else:
        fact = None
    return fact


def strip_list(str_list):
    return [x.strip() for x in str_list]

