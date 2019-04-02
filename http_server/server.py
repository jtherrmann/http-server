import socket
from typing import Callable, Tuple


# General sources:
# - https://docs.python.org/3/library/socket.html#example
# - https://blog.stephencleary.com/2009/05/using-socket-as-server-listening-socket.html  # noqa E501
# - Python function `help` for objects of interest. E.g:
#     >>> help(socket.socket)
#     >>> help(socket.socket.listen)


# TODO: socket.socket.listen (called below) has an optional backlog parameter
# that specifies the number of pending connections allowed before the listening
# socket refuses new connections. I have left it unspecified (it defaults to a
# reasonable value), but I should test how the server handles many simultaneous
# incoming connections and consider choosing a custom value for the backlog
# parameter. I should also consider some form of parallelism (probably
# multithreading) to allow handling multiple requests simultaneously. The
# server should return 503 Service Unavailable when it is temporarily
# overloaded.
#
# Sources:
# - man 2 listen
# - https://tools.ietf.org/html/rfc2616#section-10.5.4


# TODO:
# - using port 80 seems to require root, 8080 does not; determine the
#   difference
# - also, it seems that when using 8080, invalid responses aren't allowed,
#   but when using 80, they just get accepted as plaintext?
DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 8080
DEFAULT_ADDR = (DEFAULT_HOST, DEFAULT_PORT)


# HTTP explicitly doesn't specify a minimum or maximum URI length. Various
# sources seem to indicate that the same goes for total request length.
#
# TODO:
# - Confirm requirements (or lack thereof) on total request length.
# - Return 414 (Request-URI Too Long) if URI too long.
#
# sources:
# - https://tools.ietf.org/html/rfc2616#section-3.2.1
# - https://stackoverflow.com/a/2660036
# - https://serverfault.com/a/151092
MAX_REQUEST_LENGTH = 4096


# TODO: more sophisticated logging
def run_server(
        handler: Callable[[bytes], bytes],
        address: Tuple[str, int] = DEFAULT_ADDR,
        verbose: bool = False) -> None:

    with create_tcp_socket() as listener:

        # Normally, calling bind fails if a socket was too recently bound to
        # the given address. Enabling the socket.SO_REUSEADDR option for our
        # listening socket allows us to bind it to a recently used address
        # (e.g. for restarting the server during automated testing). bind still
        # fails if given the address of an actively listening socket.
        #
        # Note that Linux systems allow address reuse only when the option was
        # enabled during the previous bind operation and is enabled during the
        # current bind operation (see NOTES in `man 7 socket`).
        #
        # socket.SOL_SOCKET specifies that we're setting an option at the level
        # of the sockets API (as opposed to e.g. the TCP level).
        #
        # sources:
        # - man 2 setsockopt
        # - man 7 socket
        # - https://docs.python.org/3/library/socket.html#example
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Assign the given address to the socket (man 2 bind).
        listener.bind(address)

        # Mark the socket as one that will be used to accept incoming
        # connection requests (man 2 listen).
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
                if verbose:
                    print('-' * 79)
                    print('Connection established with {}\n'.format(address))

                # Receive up to the given number of bytes on a connected socket
                # (man 2 recv).
                request = connection.recv(MAX_REQUEST_LENGTH)
                if verbose:
                    print('Request:\n\n{}\n'.format(request.decode().strip()))

                response = handler(request)
                if verbose:
                    print(
                        'Response:\n\n{}\n\n'.format(response.decode().strip())
                    )

                # Send data from a connected socket. socket.socket.send, like
                # the underlying system call (see `man 2 send`), returns the
                # number of bytes sent, which may be less than the total if the
                # network is busy. socket.socket.sendall repeatedly sends data
                # until all data has been sent.
                connection.sendall(response)


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
