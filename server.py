import socket
from typing import Callable


# Sources:
# - https://docs.python.org/3/library/socket.html#example


# TODO: understand (& comment where appropriate) the purpose of each line


def run_server(
        host: str, port: int, handler: Callable[[str], str]) -> None:

    # TODO: record info from man 2 socket on the params to socket; these are
    # already the default values, but specify them explicitly for educational
    # purposes
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as listener:
        listener.bind((host, port))
        listener.listen()

        while True:
            connection, address = listener.accept()
            with connection:
                print('Connection established with {}\n'.format(address))
                request = connection.recv(1024).decode()
                print('Request:\n\n', request, '\n')
                response = handler(request)
                print('Response:\n\n', response)
                connection.sendall(response.encode())


if __name__ == '__main__':
    run_server('127.0.0.1', 8080, lambda s: s)
