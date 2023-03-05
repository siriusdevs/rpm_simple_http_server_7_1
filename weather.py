from requests import get
from config import COLLEGE_LOCATION, YANDEX_API_URL, YANDEX_API_HEADER, OK


def get_weather(api_key: str) -> dict:
    weather_data = {
        'temp': None,
        'feels_like': None,
        'condition': None
    }
    response = get(YANDEX_API_URL, params=COLLEGE_LOCATION, headers={YANDEX_API_HEADER: api_key})
    if response.status_code == OK:
        response_data = response.json()
        if response_data:
            fact = response_data.get('fact')
            try:
                for key in weather_data.keys():
                    weather_data[key] = fact.get(key)
            except Exception as error:
                print(f'YANDEX API get_weather error: {error}')
    else:
        print(f'YANDEX API get_weather failed with status code: {response.status_code}')
    return weather_data
