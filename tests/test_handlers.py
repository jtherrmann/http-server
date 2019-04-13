import unittest

from http_server.handlers import handler
from http_server.requests import parse, Request
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
            wrapped_handler(request_str.encode()), response_str
        )

    def test_handler_code_500(self) -> None:
        def custom_handler(request: Request) -> Response:
            raise Exception()

        request = Request(GET_METHOD, [''], HTTP_VERSION)
        response = Response(500)

        with self.assertRaises(Exception):
            custom_handler(request)

        wrapped_handler = handler(custom_handler)

        request_str = '{} / {}{}'.format(GET_METHOD, HTTP_VERSION, CRLF)
        response_str = response.get_str()

        self.assertEqual(
            wrapped_handler(request_str.encode()), response_str
        )

    def test_handler_code_400(self) -> None:
        response_200 = Response(200, ('text', 'plain'), '')

        @handler
        def custom_handler(request: Request) -> Response:
            return response_200

        good_request_str = '{} / {}{}'.format(GET_METHOD, HTTP_VERSION, CRLF)
        self.assertIsNotNone(parse(good_request_str))
        self.assertEqual(
            response_200.get_str(),
            custom_handler(good_request_str.encode())
        )

        bad_request_str = '{}/ {}{}'.format(GET_METHOD, HTTP_VERSION, CRLF)
        self.assertIsNone(parse(bad_request_str))
        self.assertEqual(
            Response(400).get_str(),
            custom_handler(bad_request_str.encode())
        )
