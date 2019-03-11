import unittest
from typing import List, Tuple

from http_server.requests import parse, Request, GET_METHOD, HTTP_VERSION


class RequestsTestCase(unittest.TestCase):

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
