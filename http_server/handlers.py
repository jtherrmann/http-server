from typing import Callable

from .requests import Request, parse
from .responses import Response


def handler(f: Callable[[Request], Response]) -> Callable[[bytes], bytes]:
    def wrapper(request: bytes) -> bytes:
        try:
            parsed_request = parse(request.decode())
            assert parsed_request is not None  # TODO: handle with proper response  # noqa E501
            response_str = f(parsed_request).get_str()
        except:  # noqa E722
            # TODO: log exception
            # https://tools.ietf.org/html/rfc2616#section-10.5.1
            response_str = Response(500).get_str()
        return response_str.encode()
    return wrapper
