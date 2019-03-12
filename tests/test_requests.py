import unittest
from typing import List, Tuple

from http_server.requests import parse, Request, GET_METHOD, HTTP_VERSION, CRLF


class RequestsTestCase(unittest.TestCase):

    def test_parse_uri_0(self) -> None:
        self.assertEqual(*self.get_actual_expected('/', ['']))

    def test_parse_uri_1(self) -> None:
        self.assertEqual(*self.get_actual_expected('/foo', ['foo']))

    def test_parse_uri_2(self) -> None:
        self.assertEqual(*self.get_actual_expected('/foo/bar', ['foo', 'bar']))

    def test_parse_uri_3(self) -> None:
        self.assertEqual(
            *self.get_actual_expected('/foo/bar/baz', ['foo', 'bar', 'baz'])
        )

    def test_parse_uri_0_with_extra_slashes(self) -> None:
        self.assertEqual(*self.get_actual_expected('///////', ['']))

    def test_parse_uri_1_with_extra_slashes(self) -> None:
        self.assertEqual(*self.get_actual_expected('////////foo', ['foo']))

    def test_parse_uri_2_with_extra_slashes(self) -> None:
        self.assertEqual(
            *self.get_actual_expected('////foo///bar', ['foo', 'bar'])
        )

    def test_parse_uri_3_with_extra_slashes(self) -> None:
        self.assertEqual(
            *self.get_actual_expected(
                '////foo///bar//////baz', ['foo', 'bar', 'baz']
            )
        )

    def test_parse_uri_trailing_slash(self) -> None:
        self.assertEqual(
            *self.get_actual_expected('/foo/bar/', ['foo', 'bar', ''])
        )

    def test_parse_uri_extra_trailing_slashes(self) -> None:
        self.assertEqual(
            *self.get_actual_expected('/foo/bar//////', ['foo', 'bar', ''])
        )

    def test_parse_ignores_trailing_chars(self) -> None:
        request_str = (
            self.get_request_str('/foo')
            + '  here is\nsome\r   more \n\n random stuff !!\r!!    \n\n\n   '
        )
        actual = parse(request_str)
        expected = self.get_request(['foo'])
        self.assertEqual(actual, expected)

    @classmethod
    def get_actual_expected(
            cls, uri: str, uri_ast: List[str]) -> Tuple[Request, Request]:
        actual = parse(cls.get_request_str(uri))
        expected = cls.get_request(uri_ast)
        return actual, expected

    @staticmethod
    def get_request_str(uri: str) -> str:
        return '{} {} {}{}'.format(GET_METHOD, uri, HTTP_VERSION, CRLF)

    @staticmethod
    def get_request(uri_ast: List[str]) -> Request:
        return Request(GET_METHOD, uri_ast, HTTP_VERSION)


if __name__ == '__main__':
    unittest.main()
