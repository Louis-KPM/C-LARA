"""
Django settings for clara_project project.

Generated by 'django-admin startproject' using Django 4.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from django.contrib.messages import constants as messages
from django.apps import apps

import dj_database_url
import os

from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'your-default-secret-key')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.getenv('DJANGO_DEBUG', False))

# Local machine, Heroku, UniSA server
ALLOWED_HOSTS = [
    'localhost',
    'c-lara-758a4f81c1ff.herokuapp.com',
    'c-lara.unisa.edu.au',
    'stmpl-lara2.ml.unisa.edu.au',
    '127.0.0.1',
    '[::1]',
]

CSRF_TRUSTED_ORIGINS = [
    'https://c-lara.unisa.edu.au',
    'https://stmpl-lara2.ml.unisa.edu.au',
    'https://c-lara-758a4f81c1ff.herokuapp.com',
    'https://localhost',
]

# Application definition

INSTALLED_APPS = [
    'clara_app',
    'storages',
    'django_q',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
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
]

MESSAGE_TAGS = {
    messages.ERROR: 'danger'
}

ROOT_URLCONF = 'clara_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "clara_app" / "templates"],
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

WSGI_APPLICATION = 'clara_project.wsgi.application'

CORS_ALLOW_ALL_ORIGINS = True

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

if os.getenv('DB_TYPE') == 'postgres':
    # Version for Heroku deployment
    DATABASES = {
        'default': dj_database_url.config(
            default=os.getenv('DATABASE_URL')
        )
    }
else:
    # Version for sqlite3 configuration, development on local machine
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# if os.getenv('DB_TYPE') == 'postgres':
    # # Version for Heroku deployment
    # AUTH_USER_MODEL = apps.get_model('clara_app', 'User')
# else:
    # # Version for sqlite3 configuration, development on local machine
    # AUTH_USER_MODEL = 'clara_app.User'
    
# Temporarily remove User
#AUTH_USER_MODEL = 'clara_app.User'
AUTH_USER_MODEL = 'auth.User'

AUTHENTICATION_BACKENDS = ['clara_app.backends.CustomUserModelBackend']

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY')

AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

AWS_STORAGE_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')

AWS_S3_REGION_NAME = os.getenv('AWS_REGION') 

AWS_DEFAULT_ACL = None

AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

# Typical S3 URL looks like this: https://c-lara.s3.ap-southeast-2.amazonaws.com/static/profile_pictures/OwnPicture.jpg
#AWS_S3_ENDPOINT_URL = 'https://s3-ap-southeast-2.amazonaws.com'

AWS_S3_ENDPOINT_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com'

AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

AWS_LOCATION = 'static'

#DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
#DEFAULT_FILE_STORAGE = 'clara_project.storage_backends.MyS3Boto3Storage'
#STATICFILES_STORAGE = 'storages.backends.s3boto3.S3ManifestStaticStorage'
STORAGES = {"default": {"BACKEND": "storages.backends.s3boto3.S3Boto3Storage"},
            "staticfiles": {"BACKEND": "storages.backends.s3boto3.S3StaticStorage"}}

MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'

#STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'

# Check the environment variable to determine the correct STATIC_URL
if os.getenv('CLARA_ENVIRONMENT') == 'unisa':
    STATIC_URL = '/static/'
else:
    # Assuming AWS_S3_CUSTOM_DOMAIN and AWS_LOCATION are set for Heroku
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'

STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

Q_CLUSTER = {
    'timeout': 3600,
    'retry': 100000000,  # Don't want tasks retried
    'save_limit': 100,
    'name': 'DjangORM',
    'workers': 10,
    'queue_limit': 10,
    'bulk': 10,
    'orm': 'default'  # Using Django's ORM
}
