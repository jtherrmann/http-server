import unittest
from typing import List, Optional, Tuple

from http_server.requests import parse, Request
from http_server.tokens import GET_METHOD, HTTP_VERSION, CRLF


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

    def test_first_missing_space(self) -> None:
        self.assertIsNone(
            parse('{}/ {}{}'.format(GET_METHOD, HTTP_VERSION, CRLF))
        )

    def test_second_missing_space(self) -> None:
        self.assertIsNone(
            parse('{} /{}{}'.format(GET_METHOD, HTTP_VERSION, CRLF))
        )

    def test_missing_crlf(self) -> None:
        self.assertIsNone(parse('{} / {}'.format(GET_METHOD, HTTP_VERSION)))

    def test_leading_space(self) -> None:
        self.assertIsNone(
            parse(' {} / {}{}'.format(GET_METHOD, HTTP_VERSION, CRLF))
        )

    def test_first_extra_space(self) -> None:
        self.assertIsNone(
            parse('{}  / {}{}'.format(GET_METHOD, HTTP_VERSION, CRLF))
        )

    def test_second_extra_space(self) -> None:
        self.assertIsNone(
            parse('{} /  {}{}'.format(GET_METHOD, HTTP_VERSION, CRLF))
        )

    def test_trailing_space(self) -> None:
        self.assertIsNone(
            parse('{} / {} {}'.format(GET_METHOD, HTTP_VERSION, CRLF))
        )

    def test_other_whitespace(self) -> None:
        self.assertIsNone(
            parse('{} /foo/\nbar {}{}'.format(GET_METHOD, HTTP_VERSION, CRLF))
        )
        self.assertIsNotNone(
            parse('{} /foo/bar {}{}'.format(GET_METHOD, HTTP_VERSION, CRLF))
        )

    def test_invalid_method(self) -> None:
        self.assertIsNone(parse('gET / {}{}'.format(HTTP_VERSION, CRLF)))

    def test_invalid_uri(self) -> None:
        self.assertIsNone(parse(self.get_request_str('foo')))
        self.assertIsNotNone(parse(self.get_request_str('/foo')))

    def test_invalid_version(self) -> None:
        self.assertIsNone(parse('{} / HtTP/1.1{}'.format(GET_METHOD, CRLF)))

    def test_missing_method(self) -> None:
        self.assertIsNone(parse('/ {}{}'.format(HTTP_VERSION, CRLF)))

    def test_missing_uri(self) -> None:
        self.assertIsNone(
            parse('{} {}{}'.format(GET_METHOD, HTTP_VERSION, CRLF))
        )

    def test_missing_version(self) -> None:
        self.assertIsNone(parse('{} / {}'.format(GET_METHOD, CRLF)))

    def test_empty_str(self) -> None:
        self.assertIsNone(parse(''))

    def test_only_method(self) -> None:
        self.assertIsNone(parse(GET_METHOD))

    def test_only_method_space(self) -> None:
        self.assertIsNone(parse(GET_METHOD + ' '))

    def test_only_method_space_uri(self) -> None:
        self.assertIsNone(parse(GET_METHOD + ' /'))

    def test_only_method_space_uri_space(self) -> None:
        self.assertIsNone(parse(GET_METHOD + ' / '))

    def test_only_method_space_uri_space_version(self) -> None:
        self.assertIsNone(parse(GET_METHOD + ' / ' + HTTP_VERSION))

    @classmethod
    def get_actual_expected(
            cls,
            uri: str,
            uri_ast: List[str]) -> Tuple[Optional[Request], Request]:
        actual = parse(cls.get_request_str(uri))
        expected = cls.get_request(uri_ast)
        return actual, expected

    @staticmethod
    def get_request_str(uri: str) -> str:
        return '{} {} {}{}'.format(GET_METHOD, uri, HTTP_VERSION, CRLF)

    @staticmethod
    def get_request(uri_ast: List[str]) -> Request:
        return Request(GET_METHOD, uri_ast, HTTP_VERSION)
