from product_ner.utils.data_process import get_keyword_dict, get_data_file_name, get_keyword_data, get_csv_data, \
    save_csv_data
from product_ner.utils.fact_process import get_fact
from product_ner.utils.prod_process import get_prod_info
import time
from datetime import datetime

# testing
# keyword_dict = {
#     '冰箱': ['起火']
# }


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
            data_list = do_prod_ner(data, keyword, incident)
    data_list.sort(key=lambda k: (k.get('weight', 0)), reverse=True)
    # save_csv_data("./product.csv", data_list, ["weight", "product", "docId"])
    save_csv_data("./product2.csv", data_list, ["weight", "fact", "docId"])


def do_prod_ner(data):
    data_list = []

    for index, row in data.iterrows():

        product = row['product']
        incident = row['criteria']

        if row.label == 0:
            continue
        fact_text = get_fact(row)
        if fact_text:
            prod_list = get_prod_info(fact_text, product, incident)
            if prod_list:
                data_list.append({
                    'product': row['product'],
                    'docId': row['docId'],
                    'court': row['court'],
                    'type': row['type'],
                    'causeOfAction': row['causeOfAction'],
                    'processing': row['processing'],
                    'content': row['content'],
                    'criteria': row['criteria'],
                    'name': row['name'],
                    'litigant': row['litigant'],
                    'publishDate': int(time.mktime(datetime.strptime(row['publishDate'], "%Y-%m-%d").timetuple()) * 1000),
                    'prodList': prod_list
                })
                print("docId:", row.docId, "product:", prod_list[:3])
            # print("docId:", row.docId, "fact:", fact_text)
    data_list.sort(key=lambda k: k['prodList'][0]['weight'], reverse=True)
    return data_list
