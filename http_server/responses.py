from typing import Tuple  # noqa F401


# TODO: move HTTP_VERSION and CRLF to shared module


class Response:

    _status_codes = (200,)
    _content_types = (('text', 'html'), ('text', 'plain'))

    def __init__(
            self,
            status_code: int,
            content_type: Tuple[str, str],
            message_body: str) -> None:

        if status_code not in self._status_codes:
            raise ValueError()

        if content_type not in self._content_types:
            raise ValueError()

        self._status_code = status_code
        self._content_type = content_type
        self._message_body = message_body

    def get_str(self) -> str:
        pass
