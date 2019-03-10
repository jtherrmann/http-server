import server


if __name__ == '__main__':
    server.run_server('127.0.0.1', 8080, lambda request: request)
