"""
Django settings for administracion_vehicular project.

Generated by 'django-admin startproject' using Django 3.1.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os

import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    "SECRET_KEY", default="*snyad=e3r43¡$b)w+o$g6c-zh+gjuogr7x_=!xybxwt+&m0312"
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = "RENDER" not in os.environ

ALLOWED_HOSTS = []

EXTERNAL_ALLOWED_HOSTS: str = os.getenv("ALLOWED_HOSTS")
if EXTERNAL_ALLOWED_HOSTS:
    ALLOWED_HOSTS.extend(EXTERNAL_ALLOWED_HOSTS.split(","))

CORS_ORIGIN_WHITELIST = ["http://localhost:5173","http://localhost:8001"]


EXTERNAL_CORS_ORIGIN: str = os.getenv("CORS_ORIGIN_WHITELIST")
if EXTERNAL_CORS_ORIGIN:
    CORS_ORIGIN_WHITELIST.extend(EXTERNAL_CORS_ORIGIN.split(","))

CSRF_TRUSTED_ORIGINS = []

EXTERNAL_CSRF_TRUSTED_ORIGINS: str = os.getenv("CSRF_TRUSTED_ORIGINS")
if EXTERNAL_CSRF_TRUSTED_ORIGINS:
    CSRF_TRUSTED_ORIGINS.extend(EXTERNAL_CSRF_TRUSTED_ORIGINS.split(","))

# Media config:
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

if not DEBUG:
    # Allows SSL if the api is running in production
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True

    # AWS credentials:
    # This key are obtained by the EC2 with the IAM role.
    # AWS_ACCESS_KEY_ID = os.getenv('AccessKeyId')
    # AWS_SECRET_ACCESS_KEY = os.getenv('SecretAccessKey')
    AWS_STORAGE_BUCKET_NAME = "iopgpsapi"
    AWS_S3_REGION_NAME = "us-east-1"  # por ejemplo, 'us-west-2'
    AWS_S3_ENDPOINT_URL = "https://s3.amazonaws.com/"

    AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
    AWS_S3_URL_PROTOCOL = "https:"  # o 'http:' si no estás usando SSL

    # Use Amazon S3 for storage for uploaded media files.
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
    MEDIA_URL = f"{AWS_S3_URL_PROTOCOL}//{AWS_S3_CUSTOM_DOMAIN}/media/"

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "whitenoise.runserver_nostatic",
    "django_filters",
    "storages",
    "corsheaders",
    "coreapi",
    "rest_framework",
    "rest_framework.authtoken",
    "advertising",
    "alarms",
    "batteries",
    "devices",
    "licenses",
    "maintenance_manuals",
    "mileage",
    "users",
    "movement_orders",
    "routes",
    "statuses",
    "tires",
    "vehicles",
    "vehicle_insurance",
    "vehicle_registration",
    "work_orders",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "wt_iopgps.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "users/templates")],
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

WSGI_APPLICATION = "wt_iopgps.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
DATABASES = {"default": dj_database_url.config(default="sqlite:///db.sqlite3")}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.getenv("REDIS_LOCATION", "redis://127.0.0.1:6379/1"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators
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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "es-ec"

TIME_ZONE = "America/Guayaquil"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
# This setting tells Django at which URL static files are going to be served to the user.
# Here, they well be accessible at your-domain.onrender.com/static/...
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
# Following settings only make sense on production and may break development environments.
if not DEBUG:  # Tell Django to copy statics to the `staticfiles` directory
    # in your application directory on Render.
    # Turn on WhiteNoise storage backend that takes care of compressing static files
    # and creating unique names for each version so they can safely be cached forever.
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.coreapi.AutoSchema",
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ],
}
