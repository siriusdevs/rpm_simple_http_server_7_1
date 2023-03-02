from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from psycopg2 import connect
from dotenv import load_dotenv
from os import getenv
from config import *
from json import loads


load_dotenv()

PG_DBNAME = getenv('PG_DBNAME')
PG_HOST = getenv('PG_HOST')
PG_PORT = getenv('PG_PORT')
PG_USER = getenv('PG_USER')
PG_PASSWORD = getenv('PG_PASSWORD')

class DbUtils:
    @staticmethod
    def get_data(path: str) -> dict:
        global db_cursor
        db_cursor.execute(SELECT_GROUPS.format(group_num=path[1:]))
        students = db_cursor.fetchall()
        return {
            'number': len(students), 
            'students': [record[0] for record in students] if students else 'No students found', 
            'group': '1.11.7.2' if path == page_7_2 else '1.11.7.1'
            }

    @staticmethod
    def is_valid_token(username: str, token: str):
        global db_cursor
        db_cursor.execute(GET_TOKEN.format(username=username))
        data = db_cursor.fetchone()
        if data:
            return data[0] == token
        return False

    @staticmethod
    def change_db(path: str, name: str, request: str) -> bool:
        global db_cursor, db_connection
        try:
            db_cursor.execute(request.format(group_num=path[1:], name=name))
        except Exception as error:
            print(f'change_db error: {error}')
            return False
        else:
            db_connection.commit()
            return bool(db_cursor.rowcount)


def get_template(path: str) -> str:
    if path in PAGES:
        return GROUP_PAGE
    return MAIN_PAGE


class CustomHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'html')
        self.end_headers()
        template = get_template(self.path)
        with open(template, 'r') as f:
            page = f.read()
            if self.path in PAGES:
                page = page.format(**DbUtils.get_data(self.path))
            self.wfile.write(page.encode())


    def respond(self, http_code: int, msg: str):
        print(http_code, msg)
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
                result = 'OK' if DbUtils.change_db(self.path, name, request) else 'FAIL'
                print(1)
                return 200, f'{self.command} {result}'
            print(2)
            return 400, f'No content provided by {self.command}'
        else:                
            print(3)
            return 404, 'Content not found'


    def check_auth(self):
        auth = self.headers.get('Authorization', '').split()
        if len(auth) == 2:
            return DbUtils.is_valid_token(auth[0], auth[1][1:-1])
        return False

    def process_request(self):
        if self.check_auth():
            self.respond(*self.make_changes())
            return
        self.respond(403, 'Auth Fail')

    def do_POST(self):
        self.process_request()

    def do_DELETE(self):
        self.process_request()

if __name__ == '__main__':
    db_connection = connect(dbname=PG_DBNAME, host=PG_HOST, port=PG_PORT, user=PG_USER, password=PG_PASSWORD)
    db_cursor = db_connection.cursor()
    with ThreadingHTTPServer((HOST, PORT), CustomHandler) as server:
        server.serve_forever()
    # server.server_close()
    db_cursor.close()
    db_connection.close()
