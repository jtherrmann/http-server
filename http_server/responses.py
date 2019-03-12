from typing import Tuple  # noqa F401


# TODO: move HTTP_VERSION to this file, import it in requests (w/ TODO to
# include more versions in grammar)


class Response:

    _status_codes = (200,)
    _content_types = (('text', 'html'),)

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
