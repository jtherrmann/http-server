from http_server import server


if __name__ == '__main__':
    server.run_server(lambda request: request.upper() * 3)
