from dadata import Dadata, DadataAsync
from config import D_KEY, D_SECRET_KEY

token = D_KEY
secret = D_SECRET_KEY


def get_data(source):
    with Dadata(token, secret) as dadata:
        result = dadata.clean(name="address", source=source)
        for k, v in result.items():
            print(k, v)
    try:
        return {'result': result, 'status': True}
    except Exception as e:
        return {'result': None, 'status': False}
