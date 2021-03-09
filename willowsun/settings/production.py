from sentry_sdk.integrations.django import DjangoIntegration
import sentry_sdk
import os

from .base import *


DEBUG = True
SECRET_KEY = os.environ.get('SECRET_KEY', '')
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')
MEDIA_URL = os.path.join('media', os.environ.get('SITE_NAME', '') + '/')

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_HSTS_SECONDS = 3600

DATABASES = {
    "default": {
        "ENGINE": 'django.db.backends.postgresql_psycopg2',
        "NAME": 'postgres',
        "USER": 'postgres',
        "PASSWORD": os.environ.get('POSTGRES_PASSWORD'),
        "HOST": 'db',
        "PORT": "5432",
    }
}


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
