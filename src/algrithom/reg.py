import re
from utils.constants import prod_brand_reg_obj, prod_keyword_reg_func, prod_model_reg_obj, prod_split_reg_obj, \
    fact_start_reg_obj, fact_end_reg_obj


def get_prod_info_reg(fact_text, keyword, incident):
    sentence_list = prod_split_reg_obj.split(fact_text)
    prod_keyword_reg_obj = prod_keyword_reg_func(keyword)

    for item in sentence_list:
        has_brand = prod_brand_reg_obj.search(item)
        has_keyword = prod_keyword_reg_obj.search(item)
        has_model = prod_model_reg_obj.search(item)
        if (has_brand and has_keyword) or (has_brand and has_model) or (has_keyword and has_model):
            return item

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
