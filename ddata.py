from dadata import Dadata, DadataAsync
from config import D_KEY, D_SECRET_KEY
import requests

token = D_KEY
secret = D_SECRET_KEY


def get_data(source):
    with Dadata(token, secret) as dadata:
        result = dadata.suggest(name="address", query=source)
    try:
        return {'result': result, 'status': True}
    except Exception as e:
        return {'result': None, 'status': False}
    
print(get_data('Россия, Новосибирск, Ленинский, Базисная улица, 7'))