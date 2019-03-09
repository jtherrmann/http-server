import socket
import subprocess
import time
import unittest


class ServerTestCase(unittest.TestCase):

    def test_run_server_single_echo(self) -> None:
        proc = subprocess.Popen(('python3', 'test_run_server_echo.py'))
        time.sleep(1)

        # TODO: don't re-specify socket params here?
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as client:
            client.connect(('127.0.0.1', 8080))
            client.sendall(b'Hello, there!')
            # TODO: see TODO relating to 1024 param in server.py
            response = client.recv(1024)

        self.assertEqual(response, b'Hello, there!')

        # TODO: problem: if above assertion fails (or any other exception is
        # raised, probably) before the terminate line below, the proc is never
        # terminated, though somehow we can still run the test program again
        # (is it b/c we allow reusing the same port?); should fix this issue
        # and also, at the start of the test, check that the server is not
        # currently running

        # SIGTERM vs. SIGKILL: https://major.io/2010/03/18/sigterm-vs-sigkill/

        print('Sending SIGTERM to process {}.'.format(proc.pid))
        proc.terminate()
        time.sleep(1)

        while proc.poll() is None:
            print('Process {} still alive. Sending SIGKILL.'.format(proc.pid))
            proc.kill()
            time.sleep(1)


if __name__ == '__main__':
    unittest.main()
