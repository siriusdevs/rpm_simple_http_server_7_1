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
INSERT = 'INSERT INTO group_{group_num} VALUES (\'{name}\')'
DELETE = 'DELETE FROM group_{group_num} WHERE name=\'{name}\''

# page str to byte coding
CODING = 'KOI8-R'

# weather consts
COLLEGE_LOCATION = {'lat': 43.403438, 'lon': 39.981544}
YANDEX_API_URL = 'https://api.weather.yandex.ru/v2/informers'

# headers' names
YANDEX_API_HEADER = 'X-Yandex-API-Key'
