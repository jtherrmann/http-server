from typing import List


# Request grammar

# Adapted from https://tools.ietf.org/html/rfc2616#section-5

# Conventions:
# - Angle brackets (<>) enclose nonterminals.
# - Single quotes ('') enclose literal terminals.
# - Braces ({}) enclose anything that may occur zero or more times.
# - Terminals may also be described using natural language.

# <request>       = <request-line> {any char}
# <request-line>  = <method> ' ' <uri> ' ' <version> '\r\l'
# <method>        = 'GET'
# <uri>           = <uri-part> {<uri-part>}
# <uri-part>      = '/' {'/'} <uri-part-body>
# <uri-part-body> = {any non-whitespace char other than '/'}
# <version>       = 'HTTP/1.1'

# TODO: use in grammar
GET_METHOD = 'GET'
HTTP_VERSION = 'HTTP/1.1'


# TODO: test case for ==
class Request:
    def __init__(self, method: str, uri_ast: List[str], version: str) -> None:
        self.method = method
        self.uri = uri_ast
        self.version = version


def parse(request: str) -> Request:
    pass
