import requests
from config import K_TOKEN

def get_data(source):
    
    content_type = 'city'
    query = source
    request = requests.post(f'https://kladr-api.ru/api.php?query={query}&contentType={content_type}')
    
    print(request.json())
    
    
get_data('Алтайский край Барнаул Центральный район ')