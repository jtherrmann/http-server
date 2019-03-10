import socket
from typing import Callable, Tuple


# TODO:
# - using port 80 seems to require root, 8080 does not; determine the
#   difference
# - also, it seems that when using 8080, invalid responses aren't allowed,
#   but when using 80, they just get accepted as plaintext?
DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 8080
DEFAULT_ADDR = (DEFAULT_HOST, DEFAULT_PORT)


# Sources:
# - https://docs.python.org/3/library/socket.html#example


# TODO: understand (& comment where appropriate) the purpose of each line


# TODO: configurable logging, e.g for suppressing during tests
def run_server(
        handler: Callable[[str], str],
        address: Tuple[str, int] = DEFAULT_ADDR) -> None:

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

        # Assign the given address to the socket (man 2 bind).
        listener.bind(address)

        # Mark the socket as one that will be used to accept incoming
        # connection requests (man 2 listen).
        #
        # TODO: specify backlog value
        listener.listen()

        while True:

            # Dequeue the first connection request from the listening socket's
            # queue of pending connections. Create and return a new connected
            # socket (not in the listening state) and the address of the peer
            # socket (in this case, a client connecting to our server). The
            # listening socket is unaffected.
            #
            # If the queue is empty, and the listening socket is not marked as
            # nonblocking, then block execution until a connection is present.
            #
            # sources:
            # - man 2 accept
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
    # Create a TCP socket.
    #
    # socket.AF_INET specifies the IPv4 family of protocols.
    #
    # socket.SOCK_STREAM is the socket type and "[p]rovides sequenced,
    # reliable, two-way, connection-based byte streams" (man 2 socket).
    #
    # The protocol can be specified as 0 when only one protocol (in this case,
    # TCP) supports the given socket type within the given protocol family.
    #
    # These are already the default parameter values for socket.socket, but I'm
    # specifying them explicitly in order to learn more about the underlying
    # sockets interface.
    #
    # sources:
    # - man 2 socket
    # - man 7 ip
    return socket.socket(
        family=socket.AF_INET, type=socket.SOCK_STREAM, proto=0
    )
