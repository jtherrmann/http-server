"""Tools for constructing responses."""


from typing import Any, Union
from typing import Optional, Tuple  # noqa F401

from .media_types import media_types
from .tokens import HTTP_VERSION, CRLF


class Response:

    # https://tools.ietf.org/html/rfc2616#section-6.1.1
    _code_phrases = {
        200: 'OK',
        400: 'Bad Request',
        404: 'Not Found',
        500: 'Internal Server Error'
    }

    def __init__(
            self,
            status_code: int,
            content_type: Tuple[str, str] = None,
            message_body: Union[bytes, str] = None) -> None:

        if status_code not in self._code_phrases:
            raise ValueError()

        if (content_type is not None
                and content_type not in media_types.values()):
            raise ValueError()

        self._status_code = status_code
        self._content_type = content_type
        self._message_body = (
            message_body.encode() if isinstance(message_body, str)
            else message_body
        )  # type: Optional[bytes]

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Response):
            raise TypeError()

        return other is self or (
            self._status_code == other._status_code
            and self._content_type == other._content_type
            and self._message_body == other._message_body
        )

    def get_bytes(self) -> bytes:
        # https://tools.ietf.org/html/rfc2616#section-6
        return (
            self._get_status_line().encode()
            + self._get_content_type().encode()
            + self._get_content_length().encode()
            + self._get_message_body()
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
        if self._content_type is not None:
            return 'Content-Type: {}{}'.format(
                '/'.join(self._content_type), CRLF
            )
        else:
            return ''

    def _get_content_length(self) -> str:
        # https://tools.ietf.org/html/rfc2616#section-14.13
        if self._message_body is not None:
            return 'Content-Length: {}{}'.format(len(self._message_body), CRLF)
        else:
            return ''

    def _get_message_body(self) -> bytes:
        return CRLF.encode() + (self._message_body
                                if self._message_body is not None else b'')
