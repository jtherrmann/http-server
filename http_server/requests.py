from typing import List  # noqa F401

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


# TODO: tests:
# - missing spaces, missing \r\n, or extra whitespace in request-line
# - invalid method
# - whitespace or / in uri-part-body
# - invalid version


@attrs(frozen=True)
class Request:
    method = attrib()  # type: str
    uri = attrib()  # type: List[str]
    version = attrib()  # type: str


def parse(request: str) -> Request:
    pass
