from utils.data_process import get_keyword_dict, get_data_file_name, get_keyword_data, get_csv_data, save_csv_data
from utils.fact_process import get_fact
from utils.prod_process import get_prod_info

keyword_data = get_keyword_data()

keyword_dict = get_keyword_dict(keyword_data)

# testing
# keyword_dict = {
#     '冰箱': ['起火']
# }

data_list = []

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
                if row.docId == '58343576c2954ad08d67aad4008f2eb3':
                    print(1)
                if fact_text:
                    prod_info = get_prod_info(fact_text, keyword, incident)
                    # data_list.append({
                    #     "weight": prod_info[0]["weight"],
                    #     "docId": row.docId,
                    #     "product": prod_info[0]["product_text"],
                    # })
                    if prod_info:
                        data_list.append({
                            "weight": prod_info[0]["weight"],
                            "docId": row.docId,
                            "product": prod_info[0]["product_text"],
                            "fact": fact_text
                        })
                        print("docId:", row.docId, "product:", prod_info[:3])
                    # print("docId:", row.docId, "fact:", fact_text)
    data_list.sort(key=lambda k: (k.get('weight', 0)), reverse=True)
    # save_csv_data("./product.csv", data_list, ["weight", "product", "docId"])
    save_csv_data("./product2.csv", data_list, ["weight", "fact", "docId"])


