"""
Django settings for opensourceris project.

Generated by 'django-admin startproject' using Django 1.11.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import warnings

import environ

env = environ.Env()  # set default values and casting
environ.Env.read_env(".env")  # reading .env file

# Mute an irrelevant warning
warnings.filterwarnings("ignore", message="`django-leaflet` is not available.")

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REAL_HOST = env.str('REAL_HOST')
PRODUCT_NAME = "Open Source Ratsinformationssystem"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', default=False)

ALLOWED_HOSTS = [
    REAL_HOST,
    '127.0.0.1',
    'localhost'
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'mainapp',
    'webpack_loader',
    'djgeojson',
    'anymail',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.twitter',
    # Note: The elasticsearch integration is added further below
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'opensourceris.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            'mainapp/templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
            ],
        },
    },
]

WSGI_APPLICATION = 'opensourceris.wsgi.application'

# forcing request.build_absolute_uri to return https
os.environ['HTTPS'] = "on"

ANYMAIL = {
    "MAILJET_API_KEY": env.str('MAILJET_API_KEY'),
    "MAILJET_SECRET_KEY": env.str('MAILJET_SECRET_KEY')
}
EMAIL_BACKEND = "anymail.backends.mailjet.EmailBackend"
DEFAULT_FROM_EMAIL = "info@hoessl.eu"

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Authentication

ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_REQUIRED = True
LOGIN_REDIRECT_URL = "/profile/"
ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https"
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False
# Needed by allauth
SITE_ID = 1

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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


AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'METHOD': 'js_sdk',
        'SCOPE': ['email', 'public_profile'],
        'INIT_PARAMS': {'cookie': True},
        'FIELDS': [
            'id',
            'email',
            'name',
            'first_name',
            'last_name',
            'verified',
            'locale',
            'timezone',
            'link',
            'updated_time',
        ],
        'EXCHANGE_TOKEN': True,
        'LOCALE_FUNC': lambda request: "de",
        'VERIFIED_EMAIL': False,
        'VERSION': 'v2.10',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'de-de'

TIME_ZONE = 'Europe/Berlin'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'mainapp/assets'),
    os.path.join(BASE_DIR, 'elasticsearch_admin/static'),
)


WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': 'bundles/',
        'STATS_FILE': os.path.join(BASE_DIR, 'webpack-stats.json'),
    }
}


# Elastic
USE_ELASTICSEARCH = env.bool('USE_ELASTICSEARCH', True)

if USE_ELASTICSEARCH:
    INSTALLED_APPS.append('elasticsearch_admin')
    INSTALLED_APPS.append('django_elasticsearch_dsl')

ELASTICSEARCH_URL_PRIVATE = env.str('ELASTICSEARCH_URL_PRIVATE')
ELASTICSEARCH_URL_PUBLIC = env.str('ELASTICSEARCH_URL_PUBLIC')

ELASTICSEARCH_DSL = {
    'default': {
        'hosts': ELASTICSEARCH_URL_PRIVATE
    },
}

OPENCAGEDATA_KEY = env.str('OPENCAGEDATA_KEY')

# Settings for Geo-Extraction
# @TODO Clarify if we want to distinguish other cities, and what would be the best way to get a good list
# of relevant city names
GEOEXTRACT_KNOWN_CITIES = ['München', 'Berlin', 'Köln', 'Hamburg', 'Karlsruhe']
GEOEXTRACT_SEARCH_COUNTRY = 'Deutschland'
GEOEXTRACT_DEFAULT_CITY = env.str('GEOEXTRACT_DEFAULT_CITY')
GEO_SEARCH_COUNTRY=env.str('GEO_SEARCH_COUNTRY' , 'Deutschland')

# Configuration regarding the city of choice
SITE_GEO_LIMITS = {'min': {'lat': 47.965, 'lng': 11.286}, 'max': {'lat': 48.296, 'lng': 11.871}}
SITE_GEO_CENTER = {'lat': 48.137, 'lng': 11.575}
SITE_GEO_INIT_ZOOM = 17
