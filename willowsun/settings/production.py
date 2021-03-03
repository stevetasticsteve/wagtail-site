import os

from .base import *

DEBUG = False
SECRET_KEY = os.environ.get('SECRET_KEY', '')
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '')


DATABASES = {
    "default": {
        "ENGINE": 'django.db.backends.postgresql_psycopg2',
        "NAME": 'postgres',
        "USER": 'postgres',
        "PASSWORD": os.environ.get('POSTGRES_PASSWORD', ''),
        "HOST": 'localhost',
        "PORT": "5432",
    }
}

try:
    from .local import *
except ImportError:
    pass
