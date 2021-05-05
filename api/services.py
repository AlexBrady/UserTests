"""Helper module."""

import typing

from flask import Response

from corelibs.models import Image, Video


def build_file_response(file: typing.Union[Image, Video]):
    response = Response(file.content)
    response.headers['Content-Disposition'] = f'attachment; filename={file.filename}'
    response.content_type = file.mimetype

    return response
