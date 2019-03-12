from typing import Any
from typing import Tuple  # noqa F401

from .tokens import HTTP_VERSION, CRLF


class Response:

    # https://tools.ietf.org/html/rfc2616#section-6.1.1
    _code_phrases = {200: 'OK', 500: 'Internal Server Error'}

    _content_types = (('text', 'html'), ('text', 'plain'))

    def __init__(
            self,
            status_code: int,
            content_type: Tuple[str, str] = None,
            message_body: str = None) -> None:

        if status_code not in self._code_phrases:
            raise ValueError()

        if (content_type is not None
                and content_type not in self._content_types):
            raise ValueError()

        if status_code == 200:
            if content_type is None:
                content_type = ('text', 'plain')

            if message_body is None:
                message_body = ''

        if (status_code == 500
                and (content_type is not None or message_body is not None)):
            raise ValueError()

        self._status_code = status_code
        self._content_type = content_type
        self._message_body = message_body

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Response):
            raise TypeError()

        return other is self or (
            self._status_code == other._status_code
            and self._content_type == other._content_type
            and self._message_body == other._message_body
        )

    def get_str(self) -> str:
        # https://tools.ietf.org/html/rfc2616#section-6
        return (
            self._get_status_line()
            + self._get_content_type() + CRLF
            + self._get_content_length() + CRLF
            + CRLF + self._message_body
        )

    def _get_status_line(self) -> str:
        # https://tools.ietf.org/html/rfc2616#section-6.1
        return '{} {} {}{}'.format(
            HTTP_VERSION, self._status_code, self._get_reason_phrase(), CRLF
        )

    def _get_reason_phrase(self) -> str:
        return self._code_phrases[self._status_code]

    def _get_content_type(self) -> str:
        # https://tools.ietf.org/html/rfc2616#section-14.17
        # https://tools.ietf.org/html/rfc2616#section-3.7
        return 'Content-Type: ' + '/'.join(self._content_type)

    def _get_content_length(self) -> str:
        # https://tools.ietf.org/html/rfc2616#section-14.13
        return 'Content-Length: {}'.format(len(self._message_body.encode()))
