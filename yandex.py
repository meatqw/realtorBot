import requests
from config import Y_TOKEN


def get_data(source, method):

    geocode = source

    if method == 'region_city':
        request = requests.get(
            f'https://geocode-maps.yandex.ru/1.x/?format=json&apikey={Y_TOKEN}&geocode={geocode}&results=1')

        result = request.json()['response']['GeoObjectCollection']['featureMember'][0]['GeoObject'][
            'metaDataProperty']['GeocoderMetaData']['AddressDetails']['Country']['AdministrativeArea']

        return {'region': result['AdministrativeAreaName'], 'city': result['SubAdministrativeArea']['Locality']['LocalityName']}

    elif method == 'all_data':

        request = requests.get(
            f'https://geocode-maps.yandex.ru/1.x/?format=json&apikey={Y_TOKEN}&geocode={geocode}')
        

        result_area = request.json()['response']['GeoObjectCollection']['featureMember'][1]['GeoObject'][
            'metaDataProperty']['GeocoderMetaData']['AddressDetails']['Country']['AdministrativeArea']

        result_address = request.json()['response']['GeoObjectCollection']['featureMember'][0]['GeoObject'][
            'metaDataProperty']['GeocoderMetaData']['AddressDetails']['Country']['AdministrativeArea']

        return {'area': result_area['SubAdministrativeArea']['Locality']['DependentLocality']['DependentLocalityName'],
                'region': result_address['AdministrativeAreaName'],
                'city': result_address['SubAdministrativeArea']['Locality']['LocalityName'],
                'street': result_address['SubAdministrativeArea']['Locality']['Thoroughfare']['ThoroughfareName'],
                'house': result_address['SubAdministrativeArea']['Locality']['Thoroughfare']['Premise']['PremiseNumber']}


print(get_data('Алтайский край, Барнаул, Индустриальный, Шумакова 45а', 'all_data'))