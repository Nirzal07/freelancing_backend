from ctypes import cast
from .base import *
from decouple import config

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["kaamxa.herokuapp.com", "64.227.173.123"]

DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.postgresql',
        "NAME": config('PGDB'),
       'USER': config('PGNAME'),
       'PASSWORD': config('PGPASSWD'),
       'HOST': config('PGHOST'),
       'PORT': config('PGPORT', cast=int),
   }
}

AUTH_USER_MODEL = 'users.User'


JET_DEFAULT_THEME = 'light-blue'

# cors origins
# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:3000",
#     "https://kaamxa.netlify.app"
# ]

CORS_ALLOW_ALL_ORIGINS= True