"""
Django settings for aoj project.

Generated by 'django-admin startproject' using Django 1.10.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '^$a$4*32@y940t@(5)#@l+i%&8+7(!)@ben@0g@_@c646+2_o@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

if DEBUG:
    ALLOWED_HOSTS = ['*']
else:
#     ALLOWED_HOSTS = ['*','.armsofjesus.org']
    ALLOWED_HOSTS = ['127.0.0.1','localhost','.armsofjesus.org']

# ALLOWED_HOSTS = ['127.0.0.1','localhost','.armsofjesus.org']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'carton',
    'solo.apps.SoloAppConfig',
    'ckeditor',
    'ckeditor_uploader',
    'colorful',
    'authtools',
    'crispy_forms',

    'aoj_app',
    'dashboard',
]

CRISPY_TEMPLATE_PACK = 'bootstrap3'
if DEBUG:
    INSTALLED_APPS += ["autotranslate"]
# INSTALLED_APPS += ["autotranslate"]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'aoj_app.middlewares.RequestLogMiddleware',
]

ROOT_URLCONF = 'aoj.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'aoj.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'aoj',
            'USER': 'aoj',
            'PASSWORD': 'i26adMi*',
            'HOST': 'localhost',
            'PORT': '',
        }
    }

    # Password validation
    # https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_USE_TLS = False
    EMAIL_HOST = 'roadster.websitewelcome.com'
    EMAIL_PORT = 25
    EMAIL_HOST_USER = 'armsofjesus@webreign.ca'
    EMAIL_HOST_PASSWORD = 'webreign2020'
    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# MEDIA_URL = '/media/'
MEDIA_URL = '/media/'

CART_PRODUCT_MODEL = 'aoj_app.models.Product'

REDACTOR_OPTIONS = {'lang': 'en', 'plugins': ['video', 'imagemanager', 'source', 'properties', 'alignment']}
REDACTOR_UPLOAD = 'uploads/'

if DEBUG:
    EXACT_X_LOGIN = "WSP-ARMS-I@4AKQAZdA"
    EXACT_TRANSACTION_KEY = "73iaoYJ8HsNcSTg1hFvS"
else:
    EXACT_X_LOGIN = "WSP-ARMS-EZpLiQAGHQ"
    EXACT_TRANSACTION_KEY = "NjPQvH_CSt9sTgpAs3vZ"

    FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0o755
    FILE_UPLOAD_PERMISSIONS = 0o644

    # LOGGING = {
    #     'version': 1,
    #     'disable_existing_loggers': False,
    #     'handlers': {
    #         'file': {
    #             'level': 'INFO',
    #             'class': 'logging.FileHandler',
    #             'filename': '/var/log/aoj.log',
    #         },
    #     },
    #     'loggers': {
    #         '': {
    #             'handlers': ['file'],
    #             'level': 'INFO',
    #             'propagate': True,
    #         },
    #     },
    # }

AUTH_USER_MODEL = 'authtools.User'
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "dashboard:orders"
LOGOUT_REDIRECT_URL = "index"

CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_CONFIGS = {"default": {"toolbar": "full"}}
