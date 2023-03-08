# server host and port
HOST = '127.0.0.1'
PORT = 8001

# pages
WEATHER = '/weather'
STUDENTS = '/students'
PAGES = (WEATHER, STUDENTS)

# templates paths
TEMPLATES = 'templates/'
MAIN_PAGE = f'{TEMPLATES}index.html'
WEATHER_TEMPLATE = f'{TEMPLATES}weather.html'
STUDENTS_TEMPLATE = f'{TEMPLATES}students.html'

# HTTP codes
OK = 200
NOT_FOUND = 404
FORBIDDEN = 403
BAD_REQUEST = 400

# db requests
SELECTOR = 'SELECT * FROM students'
GET_TOKEN = 'SELECT token FROM token WHERE username=\'{username}\''
INSERT = 'INSERT INTO {table} ({keys}) VALUES ({values})'
DELETE = 'DELETE FROM {table} '
STUDENTS_REQUIRED_ATTRS = ['fname', 'lname', 'group_']


# page str to byte coding
CODING = 'KOI8-R'

# weather consts
COLLEGE_LOCATION = {'lat': 43.403438, 'lon': 39.981544}
SOCHI_LOCATION = {'lat': 43.713351, 'lon': 39.580041}
POLYANA_LOCATION = {'lat': 43.661294, 'lon': 40.268936}
LOCATIONS = {
    'college': COLLEGE_LOCATION,
    'sochi': SOCHI_LOCATION, 
    'polyana': POLYANA_LOCATION
}
YANDEX_API_URL = 'https://api.weather.yandex.ru/v2/informers'

# headers' names
YANDEX_API_HEADER = 'X-Yandex-API-Key'

# debug messsages
WEATHER_MSG = 'YANDEX API get_weather'
