from utils.data_process import get_keyword_dict, get_data_file_name, get_keyword_data, get_csv_data
from utils.fact_process import get_fact
from utils.prod_process import get_prod_info

keyword_data = get_keyword_data()

keyword_dict = get_keyword_dict(keyword_data)

# testing
# keyword_dict = {
#     '冰箱': ['起火']
# }


def startup():
    for keyword, incident_list in keyword_dict.items():

        for incident in incident_list:
            file_name = get_data_file_name(keyword, incident)

            try:
                data = get_csv_data(file_name)
            except FileNotFoundError:
                print("file: %s.csv doesn't exists." % file_name)
                continue
            for index, row in data.iterrows():

                fact_text = get_fact(row)

                prod_info = None
                if fact_text:
                    prod_info = get_prod_info(fact_text, keyword, incident)
                    print("docId:", row.docId, "product:", prod_info)

                # print("docId:", row.docId, "product:", prod_info, "\nfact:", fact_text)

