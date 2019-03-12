import unittest

from http_server.responses import Response
from http_server.tokens import HTTP_VERSION, CRLF


class ResponsesTestCase(unittest.TestCase):

    def test_create_response_200(self) -> None:
        Response(200, ('text', 'html'), '')

    def test_response_invalid_status_code(self) -> None:
        with self.assertRaises(ValueError):
            Response(50, ('text', 'html'), '')

    def test_response_invalid_content_type(self) -> None:
        with self.assertRaises(ValueError):
            Response(200, ('html', 'text'), '')

    def test_response_200_get_str(self) -> None:
        message_body = 'here is some text'
        response = Response(200, ('text', 'plain'), message_body)
        expected = (
            HTTP_VERSION + ' 200 OK' + CRLF
            + 'Content-Type: text/plain' + CRLF
            + 'Content-Length: {}'.format(len(message_body)) + CRLF
            + CRLF + message_body
        )
        self.assertEqual(response.get_str(), expected)

    def test_response_200_defaults(self) -> None:
        self.assertEqual(
            Response(200),
            Response(200, ('text', 'plain'), '')
        )
        self.assertEqual(
            Response(200, ('text', 'html')),
            Response(200, ('text', 'html'), '')
        )
        self.assertEqual(
            Response(200, message_body='hello'),
            Response(200, ('text', 'plain'), 'hello')
        )

    # TODO
    # def test_response_500_get_str(self) -> None:

    def test_create_response_500(self) -> None:
        Response(500)

    def test_response_500_content_type(self) -> None:
        Response(200, content_type=('text', 'html'))
        with self.assertRaises(ValueError):
            Response(500, content_type=('text', 'html'))

    def test_response_500_message_body(self) -> None:
        Response(200, message_body='')
        with self.assertRaises(ValueError):
            Response(500, message_body='')


if __name__ == '__main__':
    unittest.main()
