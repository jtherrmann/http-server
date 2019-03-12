from typing import Tuple  # noqa F401

from attr import attrs, attrib


# TODO: move HTTP_VERSION to this file, import it in requests (w/ TODO to
# include more versions in grammar)


@attrs(frozen=True)
class Response:
    status_code = attrib()  # type: int
    content_type = attrib()  # type: Tuple[str, str]
    message_body = attrib()  # type: str
