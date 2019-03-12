from typing import List  # noqa F401
from typing import Optional, Tuple

from attr import attrs, attrib


GET_METHOD = 'GET'

HTTP_VERSION = 'HTTP/1.1'

CRLF = '\r\n'


# Request grammar

# Adapted from https://tools.ietf.org/html/rfc2616#section-5

# Conventions:
# - Angle brackets (<>) enclose nonterminals.
# - Single quotes ('') enclose literal terminals.
# - Braces ({}) enclose anything that may occur zero or more times.
# - Uppercase identifiers refer to terminals defined as global constants
#   (above).
# - Terminals may also be described using natural language.

# <request>       = <request-line> {any char}
# <request-line>  = <method> ' ' <uri> ' ' <version> CRLF
# <method>        = GET_METHOD
# <uri>           = <uri-part> {<uri-part>}
# <uri-part>      = '/' {'/'} <uri-part-body>
# <uri-part-body> = {any non-'/' char in range 0x21-0x7E}
# <version>       = HTTP_VERSION


@attrs(frozen=True)
class Request:
    method = attrib()  # type: str
    uri = attrib()  # type: List[str]
    version = attrib()  # type: str


# TODO: refactor to not use global _pos

_pos = 0


def parse(inpt: str) -> Optional[Request]:
    global _pos
    _pos = 0

    request_line = _parse_request_line(inpt)
    if request_line is None:
        return None

    return Request(*request_line)


def _parse_request_line(inpt: str) -> Optional[Tuple[str, List[str], str]]:
    global _pos

    method = _parse_method(inpt)
    if method is None:
        return None

    if inpt[_pos] != ' ':
        return None
    _pos += 1

    uri = _parse_uri(inpt)
    if uri is None:
        return None

    if inpt[_pos] != ' ':
        return None
    _pos += 1

    version = _parse_version(inpt)
    if version is None:
        return None

    if not inpt[_pos:].startswith(CRLF):
        return None
    _pos += len(CRLF)

    return method, uri, version


def _parse_method(inpt: str) -> Optional[str]:
    global _pos

    if not inpt[_pos:].startswith(GET_METHOD):
        return None

    _pos += len(GET_METHOD)
    return GET_METHOD


def _parse_uri(inpt: str) -> Optional[List[str]]:
    parts = []

    while inpt[_pos] == '/':
        uri_part = _parse_uri_part(inpt)
        parts.append(uri_part)

    return parts if parts != [] else None


def _parse_uri_part(inpt: str) -> str:
    global _pos
    assert inpt[_pos] == '/'

    while inpt[_pos] == '/':
        _pos += 1

    return _parse_uri_part_body(inpt)


def _parse_uri_part_body(inpt: str) -> str:
    global _pos
    assert inpt[_pos] != '/'

    part_body = ''
    # TODO: add test for case where _pos == len(inpt)
    while inpt[_pos] != '/' and 0x21 <= ord(inpt[_pos]) <= 0x7E:
        part_body += inpt[_pos]
        _pos += 1

    return part_body


def _parse_version(inpt: str) -> Optional[str]:
    global _pos

    if not inpt[_pos:].startswith(HTTP_VERSION):
        return None

    _pos += len(HTTP_VERSION)
    return HTTP_VERSION
