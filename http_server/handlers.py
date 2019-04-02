import os
from typing import Callable

from .requests import Request, parse
from .responses import Response


# TODO:
# - Return 501 Not Implemented for methods other than GET.
# - Return 505 HTTP Version Not Supported for versions other than HTTP/1.1.

def handler(
        handler_func: Callable[[Request], Response]) -> Callable[[bytes], bytes]:  # noqa E501
    def wrapper(request: bytes) -> bytes:
        try:
            parsed_request = parse(request.decode())
            if parsed_request is None:
                response = Response(400)
            else:
                response = handler_func(parsed_request)
        except:  # noqa E722
            # TODO: log exception
            # https://tools.ietf.org/html/rfc2616#section-10.5.1
            response = Response(500)
        return response.get_str().encode()
    return wrapper


# TODO: tests
@handler
def default_handler(request: Request) -> Response:
    path = os.path.join(*request.uri)
    if os.path.isfile(path):
        with open(path, 'r') as requested_file:
            message_body = requested_file.read()
        return Response(200, ('text', 'plain'), message_body)
    else:
        return Response(404)
