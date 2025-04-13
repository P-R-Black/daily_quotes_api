"""
WSGI config for daily_quotes project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
import environ
from daily_quotes.settings import base
from django.core.wsgi import get_wsgi_application

env = environ.Env()
environ.Env.read_env()

if base.DEBUG == 'True':
    # os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'daily_quotes.settings')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'daily_quotes.settings.development')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'daily_quotes.settings.production')

application = get_wsgi_application()
