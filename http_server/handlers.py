import os
from typing import Callable, Iterator, Tuple
from typing import Union  # noqa F401

from .media_types import media_types
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


# TODO: tests
@handler
def default_handler(request: Request) -> Response:
    # TODO: consider request's Accept field when setting response's
    # Content-Type
    path = os.path.join(*request.uri)
    if path == '':
        path = os.path.curdir
    if os.path.isfile(path):
        with open(path, 'rb') as requested_file:
            message_body = requested_file.read()  # type: Union[bytes, str]
        content_type = _ext_to_content_type(os.path.splitext(path)[1])
        return Response(200, content_type, message_body)
    elif os.path.isdir(path):
        message_body = _get_dir_html(path)
        return Response(200, ('text', 'html'), message_body)
    else:
        # https://tools.ietf.org/html/rfc2616#section-10.4.5
        return Response(404)


def _ext_to_content_type(ext: str) -> Tuple[str, str]:
    if ext == '.html':
        return media_types['html']
    if ext == '.css':
        return media_types['css']
    if ext == '.js':
        return media_types['javascript']
    if ext == '.png':
        return media_types['png']
    return media_types['plain']


def _get_dir_html(path: str) -> str:
    assert os.path.isdir(path)
    return '\n'.join((
        '<!doctype html>',
        '<html>',
        '  <head>',
        '    <title>{}</title>'.format(path),
        '  </head>',
        '  <body>',
        *_get_dir_html_links(path),
        '  </body>',
        '</html>'
    )) + '\n'


def _get_dir_html_links(path: str) -> Iterator[str]:
    assert os.path.isdir(path)
    yield _get_file_html_link(path, os.path.pardir)
    filenames = os.listdir(path)
    for filename in filenames:
        yield _get_file_html_link(path, filename)


def _get_file_html_link(path: str, filename: str) -> str:
    filepath = os.path.join(path, filename)
    if os.path.isdir(filepath):
        filename += os.path.sep
    return '    <p><a href="/{}">{}</a></p>'.format(filepath, filename)
