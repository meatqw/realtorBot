from dadata import Dadata, DadataAsync
from config import D_KEY, D_SECRET_KEY

token = D_KEY
secret = D_SECRET_KEY


def get_data(source):
    with Dadata(token, secret) as dadata:
        result = dadata.clean(name="address", source=source)
        
    try:
        return {'result': result['result'].replace('г ', ''). replace('р-н ', ''), 'status': True}
    except Exception as e:
        return {'result': None, 'status': False}
