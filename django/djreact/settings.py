"""
Django settings for djreact project.

Generated by 'django-admin startproject' using Django 1.9.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


fillPath = lambda x: os.path.join(os.path.dirname(__file__), x)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'y-($z@)bwfp0$_7&ds@tj7%r5e(x)9dyscsawgxd9i=)%1^7ii'

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
    'webpack_loader',
    'bootstrap4',
    'corsheaders', # Because of a bug //CE

    'jquery',

    #'django.contrib.sites', # Took this away in order for the admin site to work //CE
    'django.contrib.admindocs',
    'django.contrib.gis',
    'leaflet',
    'map',
    'accounts',

]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware', # Because of a bug. CorsMiddleware should be placed as high as possible,
    #especially before any middleware that can generate responses such as Django's CommonMiddleware or Whitenoise's WhiteNoiseMiddleware.
    #If it is not before, it will not be able to add the CORS headers to these responses. //CE
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'djreact.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'djreact/templates'), ],
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

WSGI_APPLICATION = 'djreact.wsgi.application'

LEAFLET_CONFIG ={ #Ingrid: Detta fixar med kartan.
    'DEFAULT_CENTER': (59.7177013, 17.3500491),
    'DEFAULT_ZOOM': 9,
    'MAX_ZOOM': 20,
    'MIN_ZOOM': 2,
    # 'SCALE': 'metric', #Ingrid: man kan byta till 'imperial' eller 'both'
    'ATTRIBUTION_PREFIX': 'Toolgate Maps | Leaflet library',
}

# TEMPLATE_DIRS = ( #Så här säger tutorial invisibleroads att det ska se ut -Ingrid
#     fillPath('templates'),
# )


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'postgres5l',

        'USER': 'postgres',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'djreact/static'),
]

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = os.path.join(PROJECT_DIR, '../../../static_root')

try:
    from .local_settings import *  # flake8: noqa
except ImportError:
    pass

# my_project/settings.py
LOGIN_REDIRECT_URL = 'toolgate_maps' #Toolgate Maps will be shown when you login
LOGOUT_REDIRECT_URL = 'home' #Home page will appear when you log out.

AUTH_USER_MODEL = 'accounts.CustomUser'

CORS_ORIGIN_ALLOW_ALL = True #Because of a bug. Configure the middleware's behaviour in your Django settings.
# You must add the hosts that are allowed to do cross-site requests to CORS_ORIGIN_WHITELIST,
#or set CORS_ORIGIN_ALLOW_ALL to True to allow all hosts. //CE
