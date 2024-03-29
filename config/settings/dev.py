from .base import *
from .secrets import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "9z8w@2p2&)3i^@76kiawgj6hn*gfrcin4i7+xtds0%glnu7&+l"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

# Email
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

MEDIA_URL = "/media/"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

try:
    from .local import *
except ImportError:
    pass
