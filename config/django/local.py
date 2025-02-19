from .base import *
from config.env import env

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DJANGO_DEBUG", default=True)

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# Commented out as the deffault in `base.py` is currently set to localhost.
# As of now there is no production server or setup so this can be left like that.
# DATABASES = {}

# HTTPS settings
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_SSL_REDIRECT = False