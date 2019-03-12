from typing import Callable

from .requests import Request, parse
from .responses import Response


def handler(f: Callable[[Request], Response]) -> Callable[[bytes], bytes]:
    def wrapper(request: bytes) -> bytes:
        parsed_request = parse(request.decode())
        assert parsed_request is not None  # TODO: handle with proper response
        response_str = f(parsed_request).get_str()
        return response_str.encode()
    return wrapper
