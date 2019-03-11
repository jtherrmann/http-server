import unittest
from typing import List, Tuple

from http_server.requests import parse, Request, GET_METHOD, HTTP_VERSION


# TODO: update __main__.py imports


class RequestTestCase(unittest.TestCase):

    def test_construct(self) -> None:
        method = 'foo'
        uri_ast = ['abc', 'hello', 'blah']
        version = 'bar'
        request = Request(method, uri_ast, version)
        self.assertEqual(request.method, method)
        self.assertEqual(request.uri, uri_ast)
        self.assertEqual(request.version, version)


class ParseTestCase(unittest.TestCase):

    def test_parse_uri_0(self) -> None:
        self.assertEqual(*self.get_actual_expected('/', ['']))

    @classmethod
    def get_actual_expected(
            cls, uri: str, uri_ast: List[str]) -> Tuple[Request, Request]:
        actual = parse(cls.get_request_str(uri))
        expected = cls.get_request(uri_ast)
        return actual, expected

    @staticmethod
    def get_request_str(uri: str) -> str:
        return '{} {} {}\r\n'.format(GET_METHOD, uri, HTTP_VERSION)

    @staticmethod
    def get_request(uri_ast: List[str]) -> Request:
        return Request(GET_METHOD, uri_ast, HTTP_VERSION)


if __name__ == '__main__':
    unittest.main()
