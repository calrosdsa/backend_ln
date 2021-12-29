"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 3.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import django_heroku 
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-v3fx)3!ke@52hd!h$pxo9n)qbnns4co_dkuhi7w+vmwh)n(bq%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',
    'channels',
    'rest_framework', # new
    'rest_framework.authtoken', # new
    'django.contrib.sites', # new
    'rest_auth', # new
    'allauth', # new
    'allauth.account', # new
    'allauth.socialaccount', # new
    'rest_auth.registration', # new
    'corsheaders', # new
    #'debug_toolbar',
    'users',
    'profiles',
    'novels',
    'tags',
    'categories',
    'notifications',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware', # IMPORTANT !this will recognize the frontend and NOT deny the access
    'querycount.middleware.QueryCountMiddleware',
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'


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

WSGI_APPLICATION = 'core.wsgi.application'
#ASGI_APPLICATION = 'core.asgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases



# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'Light_Novels',
        'USER':'postgres',
        'PASSWORD':'12ab34cd56ef',
        'HOST':'localhost',
        'PORT':'5432',
    }
}
# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'


STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media') # when we upload images we tell django where to upload the images to

MEDIA_URL = '/media/'


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


## ALL CUSTOM SETTINGS BELOW ##

AUTH_USER_MODEL = 'users.CustomUser' # letting Django know that we are using a custom User Model

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field
REST_AUTH_SERIALIZERS = {
    'TOKEN_SERIALIZER': 'users.serializers.CustomTokenSerializer',
}

# Django All Auth config. Add all of this.
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
AUTHENTICATION_BACKENDS = ("django.contrib.auth.backends.ModelBackend", "allauth.account.auth_backends.AuthenticationBackend",)

SITE_ID = 1 
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_UNIQUE_EMAIL = True

# Rest Framework config. Add all of this.
REST_FRAMEWORK = {'DATETIME_FORMAT': "%m/%d/%Y %H:%M:%S", 
    # Authentication Scheme "%m/%d/%Y %I:%M%P",
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication', #Note DO NOT PUT Session Authentication OR IT WILL ASK FOR CSRF KEY WHICH WE DO NOT WANT
    ], 
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 16,
    #Permission Policies
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny'], # For permissions to protected CRUD operations when users login
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']
    }




# mysite/settings.py
# Channels
#CHANNEL_LAYERS = {
    #'default': {
     #   'BACKEND': 'channels_redis.core.RedisChannelLayer',
    #    'CONFIG': {
   #         "hosts": [('127.0.0.1', 6379)],
  #      },
 #   },
#}
# Specifies localhost port 3000 where the React
# server will be running is safe to receive requests
# from. All all of this.
CORS_ALLOWED_ORIGINS = [    
'http://localhost:3000',
'https://lightnovels.vercel.app',
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'    

django_heroku.settings(locals())