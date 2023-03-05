from config import GET_TOKEN, SELECTOR
from views import list_to_view
from psycopg2 import connect
from dotenv import load_dotenv
from os import getenv


load_dotenv()

PG_DBNAME = getenv('PG_DBNAME')
PG_HOST = getenv('PG_HOST')
PG_PORT = getenv('PG_PORT')
PG_USER = getenv('PG_USER')
PG_PASSWORD = getenv('PG_PASSWORD')


class DbHandler:

    db_connection = connect(dbname=PG_DBNAME, host=PG_HOST, port=PG_PORT, user=PG_USER, password=PG_PASSWORD)
    db_cursor = db_connection.cursor()

    @classmethod
    def get_data(cls, req_conds: dict = None) -> dict:
        cls.db_cursor.execute(DbHandler.query_request(SELECTOR, req_conds) if req_conds else SELECTOR)
        students = cls.db_cursor.fetchall()
        return {
            'number': len(students),
            'rendered_students': list_to_view(students)
        }

    @classmethod
    def is_valid_token(cls, username: str, req_token: str):
        cls.db_cursor.execute(GET_TOKEN.format(username=username))
        db_token = cls.db_cursor.fetchone()
        if db_token:
            return db_token[0] == req_token
        return False

    @classmethod
    def change_db(cls, path: str, name: str, request: str) -> bool:
        try:
            cls.db_cursor.execute(request.format(group_num=path[1:], name=name))
        except Exception as error:
            print(f'change_db error: {error}')
            return False
        cls.db_connection.commit()
        return bool(cls.db_cursor.rowcount)

    @staticmethod
    def query_request(request: str, req_conds: dict):
        conditions = []
        for attr, value in req_conds.items():
            to_add = f'{attr}={value}' if isinstance(value, (int, float)) else f"{attr}='{value}'"
            conditions.append(to_add)
        return '{0} WHERE {1}'.format(request, ' AND '.join(conditions))
