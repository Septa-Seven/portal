"""
Django settings for portal project.

Generated by 'django-admin startproject' using Django 3.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import datetime
from pathlib import Path

import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    DEBUG=bool,
)
environ.Env.read_env(str(BASE_DIR / '.env.dev'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

AUTH_USER_MODEL = 'users.User'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG', default=True)

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djangorestframework_camel_case',
    'drf_yasg',
    'rest_framework',
    'rest_framework.authtoken',
    'dj_rest_auth',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'dj_rest_auth.registration',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.vk',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.yandex',
    'django_editorjs_fields',
    'corsheaders',
    'taggit',
    'apps.auth.apps.AuthConfig',
    'apps.teams.apps.TeamsConfig',
    'apps.blog.apps.BlogConfig',
    'apps.matchmaking.apps.MatchmakingConfig',
    'apps.users.apps.UsersConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'portal.urls'

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

WSGI_APPLICATION = 'portal.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
    },
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'dj_rest_auth.jwt_auth.JWTCookieAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_RENDERER_CLASSES': [
        'djangorestframework_camel_case.render.CamelCaseJSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': (
        'djangorestframework_camel_case.parser.CamelCaseMultiPartParser',
        'djangorestframework_camel_case.parser.CamelCaseJSONParser',
    ),
}
if DEBUG:
    REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"].append(
        'djangorestframework_camel_case.render.CamelCaseBrowsableAPIRenderer'
    )

EMAIL_USE_TLS = True
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_PORT = env('EMAIL_PORT')

# Frontend domain to construct letters
DOMAIN = env('DOMAIN')
SITE_NAME = 'Septa'
SITE_ID = 1

BACKEND_DOMAIN = env('BACKEND_DOMAIN')

TEAM_SIZE = env('TEAM_SIZE')
MATCHMAKING_API_KEY = env('MATCHMAKING_API_KEY')
MATCHMAKING_ADDRESS = env('MATCHMAKING_ADDRESS')
MATCHMAKING_HTTP = f'http://{MATCHMAKING_ADDRESS}'
MATCHMAKING_WS = f'ws://{MATCHMAKING_ADDRESS}'


# dj-rest-auth

# Social authentication (allauth)
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_REQUIRED = True
SOCIALACCOUNT_PROVIDERS = {
    'github': {
        'APP': {
            'client_id': env('GITHUB_AUTH_CLIENT_ID'),
            'secret': env('GITHUB_AUTH_SECRET'),
            'key': ''
        }
    },
    'vk': {
        'APP': {
            'client_id': env('VK_AUTH_CLIENT_ID'),
            'secret': env('VK_AUTH_SECRET'),
            'key': '',
        }
    },
    'google': {
        'APP': {
            'client_id': env('GOOGLE_AUTH_CLIENT_ID'),
            'secret': env('GOOGLE_AUTH_SECRET'),
            'key': '',
        }
    },
    'yandex': {
        'APP': {
            'client_id': env('YANDEX_AUTH_CLIENT_ID'),
            'secret': env('YANDEX_AUTH_SECRET'),
            'key': '',
        }
    },
}

# TODO: Email activation

# JWT (enable rest_framework_simplejwt)
REST_USE_JWT = True

# dj-rest-auth uses ACCESS_TOKEN_LIFETIME and REFRESH_TOKEN_LIFETIME
# from SIMPLE_JWT settings if REST_USE_JWT is True
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(
        minutes=env('ACCESS_TOKEN_LIFETIME', default=15)
    ),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(minutes=env('REFRESH_TOKEN_LIFETIME', default=30)),
}


# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Yekaterinburg'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'

MEDIA_URL = BACKEND_DOMAIN + '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# TODO: Prod and dev settings for CORS
CORS_ALLOW_ALL_ORIGINS = True


# AWS specific settings

USE_AWS_S3 = env('USE_AWS_S3', default=False)

if USE_AWS_S3:
    INSTALLED_APPS.append('django_s3_storage')

    # AWS authentication
    AWS_REGION = env('AWS_REGION')
    AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')

    # Media settings
    DEFAULT_FILE_STORAGE = 'django_s3_storage.storage.S3Storage'

    # No auth by default
    AWS_S3_ENDPOINT_URL = env('AWS_S3_ENDPOINT_URL')
    AWS_S3_BUCKET_AUTH = False
    AWS_S3_BUCKET_NAME = env('AWS_S3_BUCKET_NAME')
    AWS_S3_ADDRESSING_STYLE = 'auto'
    AWS_S3_KEY_PREFIX = 'media'

    # Static files settings
    STATICFILES_STORAGE = 'django_s3_storage.storage.StaticS3Storage'

    AWS_S3_ENDPOINT_URL_STATIC = env('AWS_S3_ENDPOINT_URL')
    AWS_S3_BUCKET_NAME_STATIC = env('AWS_S3_BUCKET_NAME')
    AWS_S3_ADDRESSING_STYLE_STATIC = 'auto'
    AWS_S3_KEY_PREFIX_STATIC = 'static'
