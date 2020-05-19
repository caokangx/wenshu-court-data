# coding=utf-8
from product_ner.algrithom.reg import get_fact_reg


def get_fact(row):
    return get_fact_reg(row)
    # return get_fact_CRF(row)
    # return get_fact_hmm(row)

