"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 4.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-hzdef6(rps5z3=$s0o_qizd74g*osd&rl^dbai!c*74rx4q_e6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['https://websocketking.com',
                 '139.144.176.245', '0.0.0.0', 'localhost', '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'daphne',
    'channels',
    'whitenoise.runserver_nostatic',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'user_app',
    'api_app',
    'dashboard_app',
    'settings_app',
    'community_app',
    'messaging_app',
    'notification_app',
    'imagekit'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'app.urls'

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

WSGI_APPLICATION = 'app.wsgi.application'
ASGI_APPLICATION = 'app.asgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': BASE_DIR / 'db.sqlite3',
#    }
#}

import sys
TESTING = sys.argv[1:2] == ['test']
if TESTING==False:
    DATABASES = {

        'default': {

            'ENGINE': os.environ.get('SQL_ENGINE', 'django.db.backends.sqlite3'),

            'NAME': os.environ.get('SQL_DATABASE', os.path.join(BASE_DIR, 'db.sqlite3')),

            'USER': os.environ.get('SQL_USER'),

            'PASSWORD': os.environ.get('SQL_PASSWORD'),

            'HOST': os.environ.get('SQL_HOST'),

            'PORT': os.environ.get('SQL_PORT'),
        }
    }
else:
    DATABASES = {    
        'default': {
        "ENGINE": "django.db.backends.sqlite3",
        "TEST": {
            "NAME": ":memory:",
        }
    }}

# Redis
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            # "hosts": [("127.0.0.1", 6379), ("139.144.176.245:8000", 6379)],
            "hosts": [("139.144.176.245", 6379)],
        },
    },
}


# Password Hashers
# https://docs.djangoproject.com/en/4.1/topics/auth/passwords/#password-validation
# Using Argon2: running "python -m pip install django[argon2]"
# Using BCrypt: running "python -m pip install django[bcrypt]"
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.ScryptPasswordHasher',
]

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators
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
AUTH_USER_MODEL = 'user_app.CustomUser'


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'de'

TIME_ZONE = 'CET'

USE_I18N = True

# USE_TZ = True

USE_L10N = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = [
    BASE_DIR / "core/static",
    BASE_DIR / "user_app/static"
]
DEFAULT_IMAGE_URL = STATIC_URL + 'default_profile.png'
DEFAULT_BANNER_URL = STATIC_URL + 'default_banner.png'
# Media files (profile-pics)
MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = '/media/'

# Login URL
LOGIN_URL = '/auth/login'
LOGIN_REDIRECT_URL = '/auth/profile-redirect/'

# Logut URL
LOGOUT_REDIRECT_URL = '/landing'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# SMTP Configuration
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = 'smtp.web.de'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'resetpwtest@web.de'
DEFAULT_FROM_EMAIL = 'resetpwtest@web.de'
EMAIL_HOST_PASSWORD = 'ResetPassword$44'
