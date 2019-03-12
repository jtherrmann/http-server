import unittest

from http_server.responses import Response


class ResponsesTestCase(unittest.TestCase):

    def test_create_response(self) -> None:
        Response(200, ('text', 'html'), '')

    def test_response_invalid_status_code(self) -> None:
        with self.assertRaises(ValueError):
            Response(50, ('text', 'html'), '')

    def test_response_invalid_content_type(self) -> None:
        with self.assertRaises(ValueError):
            Response(200, ('html', 'text'), '')


if __name__ == '__main__':
    unittest.main()
