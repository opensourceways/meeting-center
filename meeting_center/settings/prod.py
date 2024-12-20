"""
Django settings for community_meetings project.
Generated by 'django-admin startproject' using Django 2.2.5.
For more information on this file, see
For the full list of settings and their values, see
"""
import ssl
import os
import sys
import yaml

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, "apps"))

CONFIG_PATH = os.getenv('CONFIG_PATH')
VAULT_PATH = os.getenv('VAULT_PATH')

# Read Content from path
CONF = yaml.safe_load(open(CONFIG_PATH, 'r'))
VAULT_CONF = yaml.safe_load(open(VAULT_PATH, 'r'))
if not CONF["DEBUG"]:
    MYSQL_TLS_PEM_CONTENT = open(CONF["MYSQL_TLS_PEM_PATH"], 'r')
else:
    MYSQL_TLS_PEM_CONTENT = None

# Delete the file after reading the configuration
if CONF["IS_DELETE_CONFIG"]:
    ALL_CONFIG_PATH_LIST = [CONFIG_PATH, VAULT_PATH, CONF["MYSQL_TLS_PEM_PATH"],
                            CONF["UWSGI_TLS_CRT_PATH"], CONF["UWSGI_TLS_KEY_PATH"]]
    map(lambda x: os.remove(x), ALL_CONFIG_PATH_LIST)

# Quick-start development settings - unsuitable for production

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = VAULT_CONF["SECRET_KEY"]
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = CONF["DEBUG"]

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'meeting.apps.MeetingConfig',
    'rest_framework',
    'corsheaders',
    'django_filters',
]

if DEBUG:
    INSTALLED_APPS.append('drf_yasg')

AUTH_USER_MODEL = "meeting.User"

CORS_ALLOW_METHODS = (
    'GET',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
    'OPTIONS'
)
CORS_ALLOW_HEADERS = (
    'XMLHttpRequest',
    'X_FILENAME',
    'accept-encoding',
    'content-type',
    'Authorization',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'Pragma',
)
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
SESSION_COOKIE_HTTPONLY = True

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'meeting_center.utils.customized.my_middleware.MyMiddleware'
]

ROOT_URLCONF = 'meeting_center.urls'

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'meeting_center.utils.customized.my_exception.my_exception_handler',
    'DEFAULT_THROTTLE_CLASSES': ['meeting_center.utils.customized.my_throttles.MyAnonRateThrottle',
                                 'meeting_center.utils.customized.my_throttles.MyUserRateThrottle'],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '10/s',
        'user': '100/s'
    }
}

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

WSGI_APPLICATION = 'meeting_center.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': VAULT_CONF["DB"]["NAME"],
        'USER': VAULT_CONF["DB"]["USER"],
        'PASSWORD': VAULT_CONF["DB"]["PASSWORD"],
        'HOST': VAULT_CONF["DB"]["HOST"],
        'PORT': VAULT_CONF["DB"]["PORT"],
        'OPTIONS': {
            'ssl': {
                'ssl_version': ssl.PROTOCOL_TLSv1_2,
                'key': MYSQL_TLS_PEM_CONTENT
            },
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': "utf8mb4"
        }
    }
}

# Password validation
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
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# noinspection PyUnresolvedReferences
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'deploy', 'static')

STATIC_URL = '/static/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '[%(asctime)s] [%(filename)s:%(lineno)d] [%(module)s:%(funcName)s] '
                      '[%(levelname)s]- %(message)s'},
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True
        },
        'log': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True
        },
    }
}

# 获取config1
COMMUNITY = CONF["COMMUNITY"]
REFERER_DOMAIN = CONF.get("REFERER_DOMAIN")
COMMUNITY_ETHERPAD = CONF.get("COMMUNITY_ETHERPAD")
ONEID_AUTHORIZATION_URL = CONF.get("ONEID_AUTHORIZATION_URL")
DSAPI_URL = CONF.get("DSAPI_URL")

# 获取config2
MEETING_PLATFORM = VAULT_CONF["MEETING_PLATFORM"]

# https请求超市时间
REQUEST_TIMEOUT = (120, 120)

CONF = None
VAULT_CONF = None
MYSQL_TLS_PEM_CONTENT = None
