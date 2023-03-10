from http.server import BaseHTTPRequestHandler
from db_utils import DbHandler
from config import *
from json import loads
from views import students, weather, main_page
from weather import get_weather
from dotenv import load_dotenv
from os import getenv
from typing import Callable


load_dotenv()

YANDEX_KEY = getenv('YANDEX_KEY')


class CustomHandler(BaseHTTPRequestHandler):

    def get_template(self) -> bytes:
        if self.path.startswith(STUDENTS):
            return students(DbHandler.get_data(self.parse_query()))
        elif self.path.startswith(WEATHER):
            return weather(get_weather(self.parse_query()))
        return main_page()

    def parse_query(self) -> dict:
        qm_ind = self.path.find('?')
        if '?' in self.path and qm_ind != len(self.path) - 1:
            query = self.path[qm_ind + 1:].split('&')
            attrs_values = [line.split('=') for line in query]
            return {key: int(value) if value.isdigit() else value for key, value in attrs_values}
        return None

    def do_GET(self):
        self.send_response(OK)
        self.send_header('Content-Type', 'html')
        self.end_headers()
        self.wfile.write(self.get_template())

    def respond(self, http_code: int, msg: str):
        self.send_response(http_code)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(msg.encode())

    def read_content_json(self) -> dict:
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length:
            return loads(self.rfile.read(content_length).decode())
        return {}

    def delete(self):
        if self.path.startswith(STUDENTS):
            query = self.parse_query()
            if not query:
                return BAD_REQUEST, 'DELETE FAILED'
            if DbHandler.delete(query):
                return OK, 'Content has been deleted'
        return NOT_FOUND, 'Content not found'

    def put(self):
        if self.path.startswith(STUDENTS):
            content = self.read_content_json()
            if not content:
                return BAD_REQUEST, f'No content provided by {self.command}'
            for attr in content.keys():
                if attr not in STUDENTS_ALL_ATTRS:
                    return NOT_IMPLEMENTED, f'students do not have attribute: {attr}'
            if all([key in content for key in STUDENTS_REQUIRED_ATTRS]):
                answer = 'OK' if DbHandler.insert(content) else 'FAIL'
                return CREATED, f'{self.command} {answer}'
            return BAD_REQUEST, f'Required keys to add: {STUDENTS_REQUIRED_ATTRS}'
        return NO_CONTENT, 'Content not found'

    def post(self):
        if self.path.startswith(STUDENTS):
            content = self.read_content_json()
            if not content:
                return BAD_REQUEST, f'No content provided by {self.command}'
            for attr in content.keys():
                if attr not in STUDENTS_ALL_ATTRS:
                    return NOT_IMPLEMENTED, f'students do not have attribute: {attr}'
        # TODO if not update -> try insert
        if self.path.startswith(STUDENTS):
            query = self.parse_query()
            if not query:
                return BAD_REQUEST, 'Content not specified'
            for attr in query.keys():
                if attr not in STUDENTS_ALL_ATTRS:
                    return NOT_IMPLEMENTED, f'students do not have attribute: {attr}'
            DbHandler.update(where=query, data=content)
            # TODO update
                

    def check_auth(self):
        auth = self.headers.get('Authorization', '').split()
        if len(auth) == 2:
            return DbHandler.is_valid_token(auth[0], auth[1][1:-1])
        return False

    def process_request(self):
        if self.command == 'GET':
            self.respond(*self.get())
            return
        elif self.command == 'PUT':
            process = self.put
        elif self.command == 'POST':
            process = self.post
        elif self.command == 'DELETE':
            process = self.delete
        else:
            self.respond(NOT_IMPLEMENTED, 'Unknown request method')
            return
        if self.check_auth():
            self.respond(*process())
            return
        self.respond(FORBIDDEN, 'Auth Fail')

    def do_PUT(self):
        self.process_request()

    def do_DELETE(self):
        self.process_request()

    def do_POST(self):
        self.process_request()
