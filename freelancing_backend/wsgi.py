"""
WSGI config for freelancing_backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application


dev = os.path.isfile("./settings/dev.py")
if dev:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'freelancing_backend.settings.dev')

else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'freelancing_backend.settings.prod')

application = get_wsgi_application()
