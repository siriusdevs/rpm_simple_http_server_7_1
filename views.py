from config import *


def list_to_view(iterable: list):
    return ''.join([f'<ul>{item}</ul>' for item in iterable]) if iterable else '<p>No data given.</p>'


def weather(weather_data: dict) -> str:
    with open(WEATHER_TEMPLATE, 'r') as template:
        return template.read().format(**weather_data)


def students(students_data: dict) -> str:
    with open(STUDENTS_TEMPLATE, 'r') as template:
        page = template.read()
        return page.format(**students_data)


def main_page() -> str:
    with open(MAIN_PAGE, 'r') as template:
        return template.read()


def error_page(error: str) -> str:
    with open(ERROR_PAGE, 'r') as template:
        return template.read().format(error=error)
