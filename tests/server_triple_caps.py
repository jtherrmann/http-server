import http_server


if __name__ == '__main__':
    http_server.run_server(
        '127.0.0.1', 8080, lambda request: request.upper() * 3
    )
