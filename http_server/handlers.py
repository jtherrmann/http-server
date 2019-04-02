from typing import Callable

from .requests import Request, parse
from .responses import Response


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
