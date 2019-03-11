from typing import List  # noqa F401

from attr import attrs, attrib


GET_METHOD = 'GET'

HTTP_VERSION = 'HTTP/1.1'


# Request grammar

# Adapted from https://tools.ietf.org/html/rfc2616#section-5

# Conventions:
# - Angle brackets (<>) enclose nonterminals.
# - Single quotes ('') enclose literal terminals.
# - Braces ({}) enclose anything that may occur zero or more times.
# - Uppercase identifiers refer to terminals defined as global variables
#   (above).
# - Terminals may also be described using natural language.

# <request>       = <request-line> {any char}
# <request-line>  = <method> ' ' <uri> ' ' <version> '\r\n'
# <method>        = GET_METHOD
# <uri>           = <uri-part> {<uri-part>}
# <uri-part>      = '/' {'/'} <uri-part-body>
# <uri-part-body> = {any non-whitespace char other than '/'}
# <version>       = HTTP_VERSION


@attrs(frozen=True)
class Request:
    method = attrib()  # type: str
    uri = attrib()  # type: List[str]
    version = attrib()  # type: str


def parse(request: str) -> Request:
    pass
