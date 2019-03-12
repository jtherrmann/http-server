import unittest

from http_server.responses import Response
from http_server.requests import HTTP_VERSION, CRLF


class ResponsesTestCase(unittest.TestCase):

    def test_create_response(self) -> None:
        Response(200, ('text', 'html'), '')

    def test_response_invalid_status_code(self) -> None:
        with self.assertRaises(ValueError):
            Response(50, ('text', 'html'), '')

    def test_response_invalid_content_type(self) -> None:
        with self.assertRaises(ValueError):
            Response(200, ('html', 'text'), '')

    def test_response_get_str(self) -> None:
        message_body = 'here is some text'
        response = Response(200, ('text', 'plain'), message_body)
        expected = (
            HTTP_VERSION + ' 200 OK' + CRLF
            + 'Content-Type: text/plain' + CRLF
            + 'Content-Length: {}'.format(len(message_body)) + CRLF
            + CRLF + message_body
        )
        self.assertEqual(response.get_str(), expected)


if __name__ == '__main__':
    unittest.main()
