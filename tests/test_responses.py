import unittest

from http_server.responses import Response
from http_server.tokens import HTTP_VERSION, CRLF


class ResponsesTestCase(unittest.TestCase):

    def test_create_response(self) -> None:
        Response(200, ('text', 'html'), '')

    def test_response_invalid_status_code(self) -> None:
        with self.assertRaises(ValueError):
            Response(50, ('text', 'html'), '')

    def test_response_invalid_content_type(self) -> None:
        with self.assertRaises(ValueError):
            Response(200, ('html', 'text'), '')

    def test_response_get_bytes(self) -> None:
        message_body = 'here is some text'
        response = Response(200, ('text', 'plain'), message_body)
        expected = (
            HTTP_VERSION + ' 200 OK' + CRLF
            + 'Content-Type: text/plain' + CRLF
            + 'Content-Length: {}'.format(len(message_body)) + CRLF
            + CRLF + message_body
        ).encode()
        self.assertEqual(response.get_bytes(), expected)

    def test_response_get_bytes_no_content_type(self) -> None:
        message_body = 'here is some text'
        response = Response(200, message_body=message_body)
        expected = (
            HTTP_VERSION + ' 200 OK' + CRLF
            + 'Content-Length: {}'.format(len(message_body)) + CRLF
            + CRLF + message_body
        ).encode()
        self.assertEqual(response.get_bytes(), expected)

    def test_response_get_bytes_no_message_body(self) -> None:
        response = Response(200, content_type=('text', 'plain'))
        expected = (
            HTTP_VERSION + ' 200 OK' + CRLF
            + 'Content-Type: text/plain' + CRLF
            + CRLF
        ).encode()
        self.assertEqual(response.get_bytes(), expected)

    def test_response_get_bytes_code_only(self) -> None:
        response = Response(200)
        expected = (
            HTTP_VERSION + ' 200 OK' + CRLF
            + CRLF
        ).encode()
        self.assertEqual(response.get_bytes(), expected)

    def test_response_get_bytes_special_unicode_as_bytes(self) -> None:
        response = Response(200, ('text', 'plain'), 'λ'.encode())
        expected = (
            HTTP_VERSION + ' 200 OK' + CRLF
            + 'Content-Type: text/plain' + CRLF
            + 'Content-Length: 2' + CRLF
            + CRLF + 'λ'
        ).encode()
        self.assertEqual(response.get_bytes(), expected)

    def test_response_get_bytes_special_unicode_as_str(self) -> None:
        response = Response(200, ('text', 'plain'), 'λ')
        expected = (
            HTTP_VERSION + ' 200 OK' + CRLF
            + 'Content-Type: text/plain' + CRLF
            + 'Content-Length: 2' + CRLF
            + CRLF + 'λ'
        ).encode()
        self.assertEqual(response.get_bytes(), expected)
