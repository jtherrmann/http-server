import os
from typing import Callable, Iterator

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
    if path == '':
        path = os.path.curdir
    if os.path.isfile(path):
        with open(path, 'r') as requested_file:
            message_body = requested_file.read()
        # TODO: render html files, javascript, css
        return Response(200, ('text', 'plain'), message_body)
    elif os.path.isdir(path):
        message_body = _get_dir_html(path)
        return Response(200, ('text', 'html'), message_body)
    else:
        return Response(404)


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
    return '    <p><a href="{}">{}</a></p>'.format(filename, filename)
