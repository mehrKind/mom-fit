import os
from datetime import timedelta
from pathlib import Path
from sms_ir import SmsIr

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'mr.kind1382@gmail.com'
EMAIL_HOST_PASSWORD = 'tnamlevyggzpdhqi'
EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# sms_api_key = "Y3UzDGonHtUFZ5jrL7cFSjrPRoJpT6TwhRuZew5kbEJobncm"
sms_api_key = "N0TNmRnjBLQ63tGbKNIP3lfRfhhpt61SahmNuSh6S9e8b9gg"
linenumber = " 30002101007292 "
# sms
sms_ir = SmsIr(
sms_api_key,
linenumber,
)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-$nwt91d0cxs7n0*l3%i*wk0n@=ekllfw2$_otw3mi@(ra)5yvx'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'main',
    'rest_framework',
    'corsheaders',
    'rest_framework_simplejwt',
    'rest_framework.authtoken',
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

CORS_ALLOW_ALL_ORIGINS = True 

CORS_ALLOW_CREDENTIALS = False
ROOT_URLCONF = 'mom_fit.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'mom_fit.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'database/db.sqlite3',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'djongo',
#         'NAME': 'MoMFitDB',
#         'ENFORCE_SCHEMA': False,
#         'CLIENT': {
#             'host': 'mongodb://localhost:27017/MoMFitDB',
#         }
#     }
# }

# todo: databse connection
# connect(
#     db="MoMFitDB",
#     host="mongodb://localhost:27017/MoMFitDB"
# )



# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'assets'),
)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

REST_FRAMEWORK = {
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    # 'PAGE_SIZE': 3,
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication'
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ]
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=365),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=365),
}
SESSION_COOKIE_SAMESITE = 'Lax'  # Use 'Lax' in development unless absolutely necessary
SESSION_COOKIE_SECURE = False    # Keep this False in development (HTTP)

CSRF_COOKIE_SAMESITE = 'Lax'     # Use 'Lax' for development to work with admin panel
CSRF_COOKIE_SECURE = False       # Keep this False in development (HTTP)


# SESSION_COOKIE_AGE = 300  # 5 minutes

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
