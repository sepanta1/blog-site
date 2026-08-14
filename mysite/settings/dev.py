from decouple import config
from django.contrib.messages import constants as messages

from .base import *

DEBUG = True

ALLOWED_HOSTS = ["0.0.0.0", "127.0.0.1"]

# For Django's sites framework
SITE_ID = 2


INSTALLED_APPS += [
    "debug_toolbar",
]
MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware"] + MIDDLEWARE

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": config("DB_NAME"),
#         "USER": config("DB_USER"),
#         "PASSWORD": config("DB_PASSWORD"),
#         "HOST": config("DB_HOST", default="localhost"),
#         "PORT": config("DB_PORT", default="5432"),
#     }
# }


MEDIA_ROOT = BASE_DIR / "media"
STATIC_ROOT = BASE_DIR / "static"

STATICFILES_DIRS = [
    BASE_DIR / "statics",
]

# settings.py

MESSAGE_TAGS = {
    messages.ERROR: "danger",
}
