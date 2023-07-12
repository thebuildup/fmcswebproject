"""
Django settings for fmcs project.

Generated by 'django-admin startproject' using Django 4.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-9r(=gp%fjo47(($mq3p1%!@t2%j8ye-y!71k5g!#1o%wi!t+eg"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# DEBUG = False

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "main",
    "leaderboard",
    "users",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "fmcs.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, 'templates')],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "fmcs.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }

# To use Neon with Django, you have to create a Project on Neon and specify the project connection settings in your settings.py in the same way as for standalone Postgres.

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': 'neondb',
    'USER': 'ramanrudakou',
    'PASSWORD': 'zoL2r3Vnpfat',
    'HOST': 'ep-square-art-051666.eu-central-1.aws.neon.tech',
    'PORT': '5432',
  }
}
# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "/static/"

STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"), )
# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

SESSION_SAVE_EVERY_REQUEST = True

LOGIN_REDIRECT_URL = '/'

LOGIN_URL = 'login'

# Rating algorithm settings
RATING_ALGORITHM = os.environ["RATING_ALGORITHM"].lower()

if RATING_ALGORITHM not in {"glicko", "glicko2"}:
    raise ValueError("RATING_ALGORITHM must be 'GLICKO' or 'GLICKO2'")

GLICKO_BASE_RATING = float(os.environ["GLICKO_BASE_RATING"])
GLICKO_BASE_RD = float(os.environ["GLICKO_BASE_RD"])
GLICKO_RATING_PERIOD_DAYS = int(os.environ["GLICKO_RATING_PERIOD_DAYS"])

GLICKO2_BASE_RATING = float(os.environ["GLICKO2_BASE_RATING"])
GLICKO2_BASE_RD = float(os.environ["GLICKO2_BASE_RD"])
GLICKO2_BASE_VOLATILITY = float(os.environ["GLICKO2_BASE_VOLATILITY"])
GLICKO2_SYSTEM_CONSTANT = float(os.environ["GLICKO2_SYSTEM_CONSTANT"])
GLICKO2_RATING_PERIOD_DAYS = int(os.environ["GLICKO2_RATING_PERIOD_DAYS"])

# Other rating settings
NUMBER_OF_RATING_PERIODS_MISSED_TO_BE_INACTIVE = int(
    os.environ["NUMBER_OF_RATING_PERIODS_MISSED_TO_BE_INACTIVE"]
)