import unittest

from http_server.handlers import handler
from http_server.requests import Request
from http_server.responses import Response
from http_server.tokens import GET_METHOD, HTTP_VERSION, CRLF


class HandlersTestCase(unittest.TestCase):

    def test_handler(self) -> None:
        def custom_handler(request: Request) -> Response:
            message_body = 'You requested URI {}'.format(request.uri)
            return Response(200, ('text', 'plain'), message_body)

        request = Request(GET_METHOD, ['hello', 'world'], HTTP_VERSION)
        response = Response(
            200, ('text', 'plain'), "You requested URI ['hello', 'world']"
        )

        self.assertEqual(custom_handler(request), response)

        wrapped_handler = handler(custom_handler)

        request_str = (
            '{} /hello/world {}{}'.format(GET_METHOD, HTTP_VERSION, CRLF)
        )
        response_str = response.get_str()

        self.assertEqual(
            wrapped_handler(request_str.encode()), response_str.encode()
        )


if __name__ == '__main__':
    unittest.main()
