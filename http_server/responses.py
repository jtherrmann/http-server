from typing import Tuple  # noqa F401

from .requests import HTTP_VERSION, CRLF


# TODO: move HTTP_VERSION and CRLF to shared module


class Response:

    # https://tools.ietf.org/html/rfc2616#section-6.1.1
    _code_phrases = {200: 'OK'}

    _content_types = (('text', 'html'), ('text', 'plain'))

    def __init__(
            self,
            status_code: int,
            content_type: Tuple[str, str],
            message_body: str) -> None:

        if status_code not in self._code_phrases:
            raise ValueError()

        if content_type not in self._content_types:
            raise ValueError()

        self._status_code = status_code
        self._content_type = content_type
        self._message_body = message_body

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
