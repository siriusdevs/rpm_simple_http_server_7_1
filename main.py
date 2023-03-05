from http.server import HTTPServer
from http_handler import CustomHandler
from config import HOST, PORT


if __name__ == '__main__':
    with HTTPServer((HOST, PORT), CustomHandler) as server:
        server.serve_forever()
