import re

FACT_START_REG_PATTERN = "(经|一审|法院|原审|本院)*(确认|审理|查明|认定|认证)+(事实|法律|如下|以下)*(,|:|，|：)"
FACT_END_REG_PATTERN = "((上述|以上)事实)|本院认为"
PROD_BRAND_REG_PATTERN = '牌'
PROD_MODEL_REG_PATTERN = '[a-zA-Z\-\s]'
PROD_SPLIT_REG_PATTERN = '。|，|,|；|;'

fact_start_reg_obj = re.compile(FACT_START_REG_PATTERN)
fact_end_reg_obj = re.compile(FACT_END_REG_PATTERN)

prod_brand_reg_obj = re.compile(PROD_BRAND_REG_PATTERN)
prod_model_reg_obj = re.compile(PROD_MODEL_REG_PATTERN)
prod_split_reg_obj = re.compile(PROD_SPLIT_REG_PATTERN)


def prod_keyword_reg_func(keyword):
    return re.compile('%s' % keyword)
