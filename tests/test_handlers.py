import unittest

from http_server.requests import Request
from http_server.responses import Response
from http_server.tokens import GET_METHOD, HTTP_VERSION


class HandlersTestCase(unittest.TestCase):

    def test_handler(self) -> None:
        # TODO: finish
        def custom_handler(request: Request) -> Response:
            message_body = 'You requested URI {}'.format(request.uri)
            return Response(200, ('text', 'plain'), message_body)

        self.assertEqual(
            custom_handler(
                Request(GET_METHOD, ['hello', 'world'], HTTP_VERSION)
            ),
            Response(
                200, ('text', 'plain'), "You requested URI ['hello', 'world']"
            )
        )


if __name__ == '__main__':
    unittest.main()
