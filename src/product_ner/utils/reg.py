import re

from product_ner.utils.constants import PROD_BRAND_REG_PATTERN, PROD_MODEL_REG_PATTERN, PROD_SPLIT_REG_PATTERN, \
    PROD_MODEL_TEXT_REG_PATTERN, PROD_PRODUCER_REG_PATTERN, PROD_NUMBER_PLATES_REG_PATTERN

prod_brand_reg_obj = re.compile(PROD_BRAND_REG_PATTERN)
prod_number_plates_reg_obj = re.compile(PROD_NUMBER_PLATES_REG_PATTERN)
prod_model_reg_obj = re.compile(PROD_MODEL_REG_PATTERN)
prod_model_text_reg_obj = re.compile(PROD_MODEL_TEXT_REG_PATTERN)
prod_split_reg_obj = re.compile(PROD_SPLIT_REG_PATTERN)
prod_producer_reg_pattern = re.compile(PROD_PRODUCER_REG_PATTERN)


def prod_reg_recognize_brand_func(item, keyword=None):
    has_brand = prod_brand_reg_obj.search(item)
    if has_brand:
        is_number_plates = prod_number_plates_reg_obj.search(item)
        if not is_number_plates:
            return item
    return None


def prod_reg_recognize_keyword_func(item, keyword=None):
    def prod_keyword_reg_func(keyword):
        return re.compile('%s' % keyword)

    prod_keyword_reg_obj = prod_keyword_reg_func(keyword)
    has_keyword = prod_keyword_reg_obj.search(item)
    if has_keyword:
        return item
    return None


def prod_reg_recognize_model_without_text_func(item, keyword=None):
    has_model = prod_model_reg_obj.search(item)

    if has_model:
        return item
    return None


def prod_reg_recognize_model_with_text_func(item, keyword=None):
    has_model = prod_model_reg_obj.search(item)
    has_model_text = prod_model_text_reg_obj.search(item)
    if has_model and has_model_text:
        return item
    return None


def prod_reg_recognize_producer_func(item, keyword=None):
    has_producer = prod_producer_reg_pattern.search(item)
    if has_producer:
        return item
    return None


# 规则列表，每一项有三个元素，function是匹配函数，如果匹配返回匹配的句子，否则返回None
prod_reg_obj_list = [{
    "function": prod_reg_recognize_brand_func,
    "weight": 1,
    "description": "brand"
}, {
    "function": prod_reg_recognize_keyword_func,
    "weight": 1,
    "description": "keyword"
}, {
    "function": prod_reg_recognize_model_without_text_func,
    "weight": 1,
    "description": "model"
}, {
    "function": prod_reg_recognize_model_with_text_func,
    "weight": 1,
    "description": "model text"
}, {
    "function": prod_reg_recognize_producer_func,
    "weight": 1,
    "description": "producer"
}, ]
