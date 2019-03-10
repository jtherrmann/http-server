import socket
import subprocess
import time
import unittest


class ServerEchoTestCase(unittest.TestCase):

    _script = 'test_run_server_echo.py'

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

        # TODO: doc this problem where we check that the server isn't running

        # TODO: problem: if above assertion fails (or any other exception is
        # raised, probably) before the terminate line below, the proc is never
        # terminated, though somehow we can still run the test program again
        # (is it b/c we allow reusing the same port?); should fix this issue
        # and also, at the start of the test, check that the server is not
        # currently running


if __name__ == '__main__':
    unittest.main()
