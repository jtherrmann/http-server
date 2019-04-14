from typing import Callable

from .requests import Request, parse
from .responses import Response


# TODO:
# - Return 501 Not Implemented for methods other than GET.
# - Return 505 HTTP Version Not Supported for versions other than HTTP/1.1.

def create_handler(
        handler_func: Callable[[Request], Response]) -> Callable[[bytes], bytes]:  # noqa E501
    def wrapper(request: bytes) -> bytes:
        try:
            parsed_request = parse(request.decode())
            if parsed_request is None:
                # https://tools.ietf.org/html/rfc2616#section-10.4.1
                response = Response(400)
            else:
                response = handler_func(parsed_request)
        except:  # noqa E722
            # TODO: log exception
            # https://tools.ietf.org/html/rfc2616#section-10.5.1
            response = Response(500)
        return response.get_bytes()
    return wrapper
