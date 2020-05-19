import re

FACT_START_REG_PATTERN = "(经|一审|法院|原审|本院)*(确认|审理|查明|认定|认证)+(事实|法律|如下|以下)*(,|:|，|：)"
FACT_END_REG_PATTERN = "((上述|以上)事实)|本院认为"
PROD_BRAND_REG_PATTERN = '牌'
PROD_MODEL_REG_PATTERN = '(?![0-9\-\s]+)[0-9a-zA-Z\-\s]{2,}' # 有问题， 72V不能被匹配上
PROD_MODEL_TEXT_REG_PATTERN = '型号'
PROD_PRODUCER_REG_PATTERN = '(公司(生产|提供))的(?!《)'
PROD_NUMBER_PLATES_REG_PATTERN = '([京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼使领A-Z]{1}[A-Z]{1}(([0-9]{5}[DF])|([DF]([A-HJ-NP-Z0-9])[0-9]{4})))|([京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼使领A-Z]{1}[A-Z]{1}[A-HJ-J-NNP-Z0-9]{4}[A-HJ-NP-Z0-9挂学警港澳]{1})'
PROD_SPLIT_REG_PATTERN = '。|，|,|；|;'

fact_start_reg_obj = re.compile(FACT_START_REG_PATTERN)
fact_end_reg_obj = re.compile(FACT_END_REG_PATTERN)



