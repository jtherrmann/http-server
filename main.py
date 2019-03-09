import socket
from typing import Iterator


# Sources:
# - https://docs.python.org/3/library/socket.html#example


def run_server(host: str, port: int) -> Iterator[str]:
    with socket.socket() as listener:
        listener.bind((host, port))
        listener.listen()

        while True:
            connection, address = listener.accept()
            with connection:
                print('Connection established with {}'.format(address))
                yield connection.recv(1024).decode()


if __name__ == '__main__':
    server = run_server('127.0.0.1', 8080)
    while True:
        print(next(server))
