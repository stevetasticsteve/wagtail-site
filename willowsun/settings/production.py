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

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
   dsn="https://4f6615c480264665a3445c84e9886fdf@o538547.ingest.sentry.io/5656773",
   integrations=[DjangoIntegration()],
   traces_sample_rate=1.0,
   send_default_pii=True,
)

try:
    from .local import *
except ImportError:
    pass
