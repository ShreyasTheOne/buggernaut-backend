"""
Django settings for buggernaut_backend project.

Generated by 'django-admin startproject' using Django 3.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import yaml

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

base_config_file = open(os.path.join(
    BASE_DIR,
    'configuration/base.yml'
))
base_configuration = yaml.load(base_config_file, Loader=yaml.FullLoader)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = base_configuration["secrets"]["secretKey"]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels',
    'rest_framework',
    'buggernaut',
    'django_filters',
    'tinymce',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_WHITELIST = (
    'http://localhost:3000',
    # 'http://127.0.0.1:3000',
    # 'http://192.168.0.106:3000',
    # 'http://localhost:4000',
    'http://localhost:8000',
    # 'http://internet.channeli.in',
)

SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'
CSRF_COOKIE_NAME = 'buggernaut_csrftoken'
SESSION_COOKIE_NAME = 'buggernaut_sessionid'

ROOT_URLCONF = 'buggernaut_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'buggernaut_backend.wsgi.application'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],

    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication'
    ],
}
# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': base_configuration["services"]["database"]["name"],
        'USER': base_configuration["services"]["database"]["user"],
        'PASSWORD': base_configuration["services"]["database"]["password"],
        'HOST': base_configuration["services"]["database"]["host"],
        'POR': base_configuration["services"]["database"]["port"],
        'OPTIONS': {'charset': 'utf8mb4'},
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTH_USER_MODEL = 'buggernaut.User'

EMAIL_HOST = base_configuration["services"]["mailing"]["email_host"]
EMAIL_PORT = base_configuration["services"]["mailing"]["email_port"]
EMAIL_USE_TLS = True
EMAIL_HOST_USER = base_configuration["services"]["mailing"]["email_host_user"]
EMAIL_HOST_PASSWORD = base_configuration["services"]["mailing"]["email_host_password"]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = base_configuration['i18n']['languageCode']

TIME_ZONE = base_configuration['i18n']['timezone']

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/


STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")
MEDIA_URL = '/media/'

ASGI_APPLICATION = "buggernaut_backend.routing.application"
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}
