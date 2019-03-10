import http_server


if __name__ == '__main__':
    http_server.run_server(lambda request: request)
