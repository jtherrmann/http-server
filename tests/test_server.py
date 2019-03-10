import os
import subprocess
import time
import unittest
from typing import Iterable

import http_server


class ServerTestCase(unittest.TestCase):

    _script_dir = os.path.join('tests', 'scripts')

    _script = None  # type: str

    _multiple_requests = (
        b'dog dog CAT',
        b'zebra FiSh',
        b'abc abc 123 123',
        b'hello thank you good bye',
        b'asntehuNATOHUECARACntaHAOTehaoneCH',
        b'cool water metal hard rough',
        b'rocks garden water rainbows',
        b'symbols walls trees meadows',
        b'MEMmuetoaeHUEETmeTUEUMTEmTEUM',
        b'live long and prosper'
    )

    # If setUp fails because a process is already listening on the given
    # address (e.g. because a previous test server somehow escaped tearDown or
    # because you manually started a server and forgot to terminate it), you
    # must identify the process and terminate it before you can run the tests
    # successfully. One method is to run the following command as root:
    #
    #   netstat -nlp | grep <host>:<port>
    #
    # where <host> and <port> are the host and port on which the process is
    # listening. The -nlp options tell netstat to show numerical addresses,
    # show only listening sockets, and show the PID to which each socket
    # belongs. The above command should print a line that includes the PID of
    # the rogue process. Kill it with `kill <PID>`.
    #
    # Sources:
    # - https://unix.stackexchange.com/a/106562
    # - man 8 netstat
    # - man 1 kill

    def setUp(self) -> None:
        # Start the test server. Automatically called before each test.

        self._server = subprocess.Popen(
            ('python3', os.path.join(self._script_dir, self._script))
        )
        self._wait()

        # Cause the current test to fail if the server failed to start. Without
        # this check, if the server failed to start because there was already
        # another process listening on the given address, then the current test
        # attempts to connect to the process as if it were the test server, and
        # the test passes or fails depending on the response it receives.
        self.assertEqual(self._server.poll(), None)

    def tearDown(self) -> None:
        # Terminate the test server. Automatically called after each test.

        # SIGTERM vs. SIGKILL: https://major.io/2010/03/18/sigterm-vs-sigkill/

        print('Sending SIGTERM to process {}.'.format(self._server.pid))
        self._server.terminate()
        self._wait()

        while self._server.poll() is None:
            print(
                'Process {} still alive. '
                'Sending SIGKILL.'.format(self._server.pid)
            )
            self._server.kill()
            self._wait()

    @staticmethod
    def _wait() -> None:
        # 300 ms seems to be sufficient everywhere this method is called, but
        # if it ever causes problems, then it should be made configurable,
        # perhaps as a command-line and/or config file option.
        time.sleep(0.3)

    @staticmethod
    def _send_requests(requests: Iterable[bytes]) -> Iterable[bytes]:
        for request in requests:
            with http_server.create_tcp_socket() as client:
                client.connect(http_server.DEFAULT_ADDR)
                client.sendall(request)
                # TODO: see TODO relating to 1024 param in server.py
                yield client.recv(1024)


class ServerEchoTestCase(ServerTestCase):
    # Test a server that, for each request, sends back an identical response.

    _script = 'server_echo.py'

    def test_echo_single(self) -> None:
        requests = (b'Hello, there!',)
        responses = tuple(self._send_requests(requests))
        self.assertEqual(responses, requests)

    def test_echo_multiple(self) -> None:
        requests = self._multiple_requests
        responses = tuple(self._send_requests(requests))
        self.assertEqual(responses, requests)


class ServerTripleCapsTestCase(ServerTestCase):
    # Test a server that, for each request, sends back the concatenation of
    # three copies of the request, converted to upper case.

    _script = 'server_triple_caps.py'

    def test_triple_caps_single(self) -> None:
        requests = (b'Hello, there!',)
        responses = tuple(self._send_requests(requests))
        self.assertEqual(
            responses, (b'HELLO, THERE!HELLO, THERE!HELLO, THERE!',)
        )

    def test_triple_caps_multiple(self) -> None:
        requests = self._multiple_requests
        responses = tuple(self._send_requests(requests))
        self.assertEqual(
            responses, tuple(request.upper() * 3 for request in requests)
        )
