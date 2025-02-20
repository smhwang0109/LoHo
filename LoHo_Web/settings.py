"""
Django settings for LoHo_Web project.

Generated by 'django-admin startproject' using Django 2.1.15.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
from decouple import config

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', config('DJANGO_SECRET_KEY'))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool( os.environ.get('DJANGO_DEBUG', True))

ALLOWED_HOSTS = ['localhost', 'lohoweb.herokuapp.com']


# Application definition

INSTALLED_APPS = [

    'bootstrap4',
    'bootstrap_datepicker_plus',

    'ckeditor',
    'ckeditor_uploader',

    # 'cloudinary_storage',

    'django.contrib.humanize', # 숫자 세자리마다 쉼표 찍기
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'accounts',
    'articles',

    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.naver',
    'allauth.socialaccount.providers.kakao',
    'allauth.socialaccount.providers.facebook',

    # 'cloudinary',

]

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'LoHo_Web.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # allauth needs
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'LoHo_Web.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'ko-KR'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

LOGIN_URL = '/accounts/login/'

LOGIN_REDIRECT_URL = '/articles/'

ACCOUNT_LOGOUT_REDIRECT_URL = '/articles/'

ACCOUNT_LOGOUT_ON_GET = True


AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

SITE_ID = 1


SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'METHOD': 'oauth2',
        'SCOPE': ['email', 'public_profile', 'user_friends'],
        'AUTH_PARAMS': {'auth_type':'reauthenticate'},
        'INIT_PARAMS': {'cookie':True},
        'FIELDS':[
            'id',
            'email',
            'name',
            'first_name',
            'last_name',
            'friends',
            'verified',
        ],
        'EXCHANGE_TOKEN':True,
        'LOCALE_FUNC': lambda request: 'ko_KR',
        'VERIFIED_EMAIL': False,
        'VERSION': 'v2.9',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

MEDIA_URL = '/media/' # 업로드하는 과정 처리하는 url
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

CKEDITOR_UPLOAD_PATH = "media/"

BOOTSTRAP4 = {
    'include_jquery': True,
}

import dj_database_url
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

# CLOUDINARY_STORAGE = {
#     'CLOUD_NAME' : config('CLOUNDINARY_CLOUD_NAME'),
#     'API_KEY' : config('CLOUNDINARY_API_KEY'),
#     'API_SECRET' : config('CLOUNDINARY_API_SECRET'),
# }

# DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

IAMPORT_CODE = config('IAMPORT_CODE')
IAMPORT_KEY = config('IAMPORT_KEY')
IAMPORT_SECRET = config('IAMPORT_SECRET')
