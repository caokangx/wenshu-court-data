import requests
import json
from .proxy import get_backend_address


def upload_doc_to_backend(doc_list):
    response = requests.put(get_backend_address(), data=json.dumps({'docList': doc_list}))