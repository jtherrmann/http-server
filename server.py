import socket
from typing import Callable


# Sources:
# - https://docs.python.org/3/library/socket.html#example


# TODO: understand (& comment where appropriate) the purpose of each line


# TODO: configurable logging, e.g for suppressing during tests
def run_server(host: str, port: int, handler: Callable[[str], str]) -> None:

    # TODO: record info from man 2 socket on the params to socket; these are
    # already the default values, but specify them explicitly for educational
    # purposes
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as listener:
        # TODO: document: allow reusing the socket as per
        # https://stackoverflow.com/a/29217540 and
        # help(socket.socket.setsockopt), which says to see the Unix manual;
        # helpful when restarting server during testing
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        listener.bind((host, port))
        listener.listen()

        while True:
            connection, address = listener.accept()
            with connection:
                print('Connection established with {}\n'.format(address))
                # TODO: where does 1024 come from? make it globally
                # configurable (e.g. for tests)?
                request = connection.recv(1024).decode()
                print('Request:\n\n', request, '\n')
                response = handler(request)
                print('Response:\n\n', response)
                connection.sendall(response.encode())


if __name__ == '__main__':
    # TODO:
    # - using port 80 seems to require root, 8080 does not; determine the
    #   difference, maybe make it globally configurable for the purpose of
    #   running tests & such
    # - also, it seems that when using 8080, invalid responses aren't allowed,
    #   but when using 80, they just get accepted as plaintext?
    run_server('127.0.0.1', 8080, lambda s: s)
