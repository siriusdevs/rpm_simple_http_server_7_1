from requests import get
from config import COLLEGE_LOCATION, YANDEX_API_URL, YANDEX_API_HEADER, OK, LOCATIONS
from dotenv import load_dotenv
from os import getenv


load_dotenv()
YANDEX_KEY = getenv('YANDEX_KEY')


def get_weather(query: dict) -> dict:
    weather_data = {
        'temp': None,
        'feels_like': None,
        'condition': None,
        'location': 'Sirius College'
    }
    params = LOCATIONS['college']
    if query:
        location = query.get('location')
        if location in LOCATIONS.keys():
            params = LOCATIONS[location]
            weather_data['location'] = location
    response = get(YANDEX_API_URL, params=params, headers={YANDEX_API_HEADER: YANDEX_KEY})
    if response.status_code == OK:
        response_data = response.json()
        if response_data:
            fact = response_data.get('fact')
            try:
                for key in weather_data.keys():
                    if key != 'location':
                        weather_data[key] = fact.get(key)
            except Exception as error:
                print(f'YANDEX API get_weather error: {error}')
    else:
        print(f'YANDEX API get_weather failed with status code: {response.status_code}')
    return weather_data
