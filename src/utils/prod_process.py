import re
from algrithom.reg import get_prod_info_reg


def get_prod_info(fact_text, keyword, incident):
    return get_prod_info_reg(fact_text, keyword, incident)
    # return get_prod_info_crf()
    # return get_prod_info_hmm()

