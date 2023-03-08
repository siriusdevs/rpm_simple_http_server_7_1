from requests import get
from config import YANDEX_API_URL, YANDEX_API_HEADER, OK, LOCATIONS, WEATHER_MSG
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
    try:
        location = query.get('location')
    except Exception:
        print(f'{WEATHER_MSG} failed to get location from query, defaults to college')
        params = LOCATIONS['college']
    else:
        params = LOCATIONS[location]
        weather_data['location'] = location
    response = get(YANDEX_API_URL, params=params, headers={YANDEX_API_HEADER: YANDEX_KEY})
    if response.status_code != OK:
        print(f'{WEATHER_MSG} failed with status code: {response.status_code}')
        return weather_data
    response_data = response.json()
    if not response_data:
        print(f'{WEATHER_MSG} api did respond with empty content')
        return weather_data
    fact = response_data.get('fact')
    if not fact:
        print(f'{WEATHER_MSG} api did not provide factual weather data')
        return weather_data
    for key in weather_data.keys():
        if key != 'location':
            weather_data[key] = fact.get(key)
    return weather_data
