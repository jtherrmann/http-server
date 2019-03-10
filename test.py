import socket
import subprocess
import time
import unittest


class ServerEchoTestCase(unittest.TestCase):

    _script = 'test_run_server_echo.py'

    # setUp starts the server before each test and tearDown terminates it after
    # each test. setUp fails if a process is already listening on the given
    # host and port. If this happens (e.g. because the server somehow escaped
    # tearDown or because you manually started the server and forgot to
    # terminate it), you will have to identify the rogue process and terminate
    # it. One method is to run the following command as root:
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
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as client:
            # TODO: could we get a ConnectionRefusedError if the server is busy
            # with another connection, and thus fail to detect that the server
            # is actually running? should we try this a few times, pausing for
            # ~1 sec. after each attempt?
            with self.assertRaises(ConnectionRefusedError):
                client.connect(('127.0.0.1', 8080))

        self._server = subprocess.Popen(('python3', self._script))
        time.sleep(1)

    def tearDown(self) -> None:
        # SIGTERM vs. SIGKILL: https://major.io/2010/03/18/sigterm-vs-sigkill/

        print('Sending SIGTERM to process {}.'.format(self._server.pid))
        self._server.terminate()
        time.sleep(1)

        while self._server.poll() is None:
            print(
                'Process {} still alive. '
                'Sending SIGKILL.'.format(self._server.pid)
            )
            self._server.kill()
            time.sleep(1)

    def test_run_server_single_echo(self) -> None:
        # TODO: don't re-specify socket params here?
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as client:
            client.connect(('127.0.0.1', 8080))
            client.sendall(b'Hello, there!')
            # TODO: see TODO relating to 1024 param in server.py
            response = client.recv(1024)

        self.assertEqual(response, b'Hello, there!')


if __name__ == '__main__':
    unittest.main()
