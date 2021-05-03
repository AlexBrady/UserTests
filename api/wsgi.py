
"""
WSGI config for this project.

It exposes the WSGI callable as a module-level variable named ``application``.
"""

import os

from api.application import create_app

env = os.environ.get('APP_ENV')

if not env:
    raise Exception('APP_ENV not found.')

application = create_app(env)
