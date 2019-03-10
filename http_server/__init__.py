import socket
from typing import Callable


# Sources:
# - https://docs.python.org/3/library/socket.html#example


# TODO: understand (& comment where appropriate) the purpose of each line


# TODO:
# - using port 80 seems to require root, 8080 does not; determine the
#   difference, maybe make it globally configurable for the purpose of
#   running tests & such
# - also, it seems that when using 8080, invalid responses aren't allowed,
#   but when using 80, they just get accepted as plaintext?


# TODO: configurable logging, e.g for suppressing during tests
def run_server(host: str, port: int, handler: Callable[[str], str]) -> None:

    # TODO: record info from man 2 socket on the params to socket; these are
    # already the default values, but specify them explicitly for educational
    # purposes
    with create_tcp_socket() as listener:
        # TODO: document: allow reusing the socket as per
        # https://stackoverflow.com/a/29217540 and
        # help(socket.socket.setsockopt), which says to see the Unix manual;
        # helpful when restarting server during testing
        #
        # note that without this line, socket.bind (called on the next line)
        # raises an exception displayed as "OSError: [Errno 98] Address already
        # in use" if we try to run the server too soon after it was last
        # terminated; this is the same error that prints if we try to run the
        # server while another instance of the server is actually running, in
        # which case having set this option still does not allow us to bind two
        # different sockets to the same address; this line only allows us to
        # reuse the address immediately after terminating the previous server's
        # process
        #
        # Error codes:
        # http://www-numi.fnal.gov/offline_software/srt_public_context/WebDocs/Errors/unix_system_errors.html
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


def create_tcp_socket() -> socket.socket:
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
