from config import *


def list_to_view(iterable: list):
    return ''.join([f'<ul>{item}</ul>' for item in iterable]) if iterable else '<p>No data given.</p>'


def weather(weather_data: dict) -> bytes:
    with open(WEATHER_TEMPLATE, 'r') as template:
        return template.read().format(**weather_data).encode(CODING)


def students(students_data: dict):
    with open(STUDENTS_TEMPLATE, 'r') as template:
        page = template.read()
        return page.format(**students_data).encode(CODING)


def main_page():
    with open(MAIN_PAGE, 'r') as template:
        return template.read().encode(CODING)
