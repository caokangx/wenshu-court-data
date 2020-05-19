import os

BACKEND_SERVICE_ADDRESS_DEV = 'http://127.0.0.1:8081/iprs/prodlist'
BACKEND_SERVICE_ADDRESS_PROD = 'http://127.0.0.1:8081/iprs/prodlist' # TODO


def get_backend_address():
    if os.environ.get('ENV', None):
        return BACKEND_SERVICE_ADDRESS_DEV
    else:
        return BACKEND_SERVICE_ADDRESS_PROD
