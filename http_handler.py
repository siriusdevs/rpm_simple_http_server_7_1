from http.server import BaseHTTPRequestHandler
from db_utils import DbHandler
from config import *
from json import loads
from views import students, weather, main_page
from weather import get_weather
from dotenv import load_dotenv
from os import getenv


load_dotenv()

YANDEX_KEY = getenv('YANDEX_KEY')


class CustomHandler(BaseHTTPRequestHandler):

    def get_template(self) -> bytes:
        if self.path.startswith(STUDENTS):
            return students(DbHandler.get_data(self.parse_query()))
        elif self.path.startswith(WEATHER):
            return weather(get_weather(YANDEX_KEY))
        return main_page()

    def parse_query(self) -> dict:
        if '?' in self.path:
            query = self.path[self.path.find('?') + 1:].split('&')
            attrs_values = [line.split('=') for line in query]
            return {key: int(value) if value.isdigit() else value for key, value in attrs_values}
        return None

    def do_GET(self):
        self.send_response(OK)
        self.send_header('Content-type', 'html')
        self.end_headers()
        self.wfile.write(self.get_template())

    def respond(self, http_code: int, msg: str):
        self.send_response(http_code)
        self.send_header('Content-type', 'text')
        self.end_headers()
        self.wfile.write(msg.encode())

    def make_changes(self) -> tuple:
        if self.path in PAGES:
            request = INSERT if self.command == 'POST' else DELETE
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length:
                request_data = loads(self.rfile.read(content_length).decode())
                name = request_data.get('name')
                answer_msg = 'OK' if DbHandler.change_db(self.path, name, request) else 'FAIL'
                return OK, f'{self.command} {answer_msg}'
            return BAD_REQUEST, f'No content provided by {self.command}'
        return NOT_FOUND, 'Content not found'

    def check_auth(self):
        auth = self.headers.get('Authorization', '').split()
        if len(auth) == 2:
            return DbHandler.is_valid_token(auth[0], auth[1][1:-1])
        return False

    def process(self):
        if self.check_auth():
            self.respond(*self.make_changes())
            return
        self.respond(FORBIDDEN, 'Auth Fail')

    def do_POST(self):
        self.process()

    def do_DELETE(self):
        self.process()
