"""
Django settings for {{ cookiecutter.django_project_name }} project.

Generated by 'django-admin startproject' using Django 3.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/stable/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/stable/ref/settings/
"""
from pathlib import Path

from django.utils.translation import gettext_lazy as _

from . import env

PROJECT_VERSION = '{{ cookiecutter.project_version }}'

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/stable/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('DJANGO_SECRET_KEY')

SERVER_NAME = env.str('SERVER_NAME')
SERVER_PROTOCOL = env.str('SERVER_PROTOCOL', 'https')
SERVER_PREFIX = f'{SERVER_PROTOCOL}://{SERVER_NAME}'
SITE_NAME = env.str('SITE_NAME', SERVER_NAME)
SITE_ID = 1

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DJANGO_DEBUG', False)
DEBUG_SQL = env.bool('DJANGO_DEBUG_SQL', False)
DEBUG_SQL_LIMIT = env.int('DJANGO_DEBUG_SQL_LIMIT', 5)
DEBUG_TOOLBAR = env.bool('DJANGO_DEBUG_TOOLBAR', False)
LOGGING_PATH = env.get('LOGGING_PATH')
LOGGING_LEVEL = env.str('LOGGING_LEVEL', 'INFO')

ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS')
ADMINS = [(email, email) for email in env.list('DJANGO_ADMINS')]

EMAIL_HOST = env.get('DJANGO_EMAIL_HOST')
EMAIL_HOST_USER = env.get('DJANGO_EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env.get('DJANGO_EMAIL_HOST_PASSWORD')
EMAIL_PORT = env.int('DJANGO_EMAIL_PORT', 0)
EMAIL_USE_TLS = env.bool('DJANGO_EMAIL_USE_TLS', None)
EMAIL_USE_SSL = env.bool('DJANGO_EMAIL_USE_SSL', None)
EMAIL_BACKEND = env.str('DJANGO_EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')
EMAIL_FILE_PATH = env.get('DJANGO_EMAIL_FILE_PATH')

DEFAULT_FROM_EMAIL = env.get('DEFAULT_FROM_EMAIL')


# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
{%- if cookiecutter.worker == 'rq' %}
    'django_rq',
{%- elif cookiecutter.worker == 'celery' %}
    'django_celery_results',
{%- endif %}
    'django_extensions',
    'django_uwsgi',
    '{{ cookiecutter.django_project_name }}.apps.CustomAdminConfig',
    '{{ cookiecutter.django_app_name }}.apps.{{ cookiecutter.django_app_name|replace('_', ' ')|title|replace(' ', '') }}Config',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

ROOT_URLCONF = env.str('DJANGO_ROOT_URLCONF', '{{ cookiecutter.django_project_name }}.urls')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / '{{ cookiecutter.django_project_name }}' / 'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django_settings_export.settings_export',
            ],
        },
    }
]

SETTINGS_EXPORT = [
    'DEBUG',
    'SERVER_NAME',
    'SERVER_PROTOCOL',
    'SERVER_PREFIX',
    'SITE_NAME',
    'PROJECT_VERSION',
]

WSGI_APPLICATION = '{{ cookiecutter.django_project_name }}.wsgi.application'

# Database
# https://docs.djangoproject.com/en/stable/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env.get('DJANGO_DB_NAME'),
        'USER': env.get('DJANGO_DB_USER'),
        'PASSWORD': env.get('DJANGO_DB_PASSWORD'),
        'HOST': env.get('DJANGO_DB_HOST'),
        'ATOMIC_REQUESTS': True,
    }
}

CACHES = {
    'default': {
        'BACKEND': env.str(
            'DJANGO_CACHE_BACKEND',
            'django.core.cache.backends.dummy.DummyCache' if DEBUG else 'django.core.cache.backends.locmem.LocMemCache',
        ),
        'LOCATION': env.get('DJANGO_CACHE_LOCATION'),
        'KEY_PREFIX': env.get('DJANGO_CACHE_KEY_PREFIX'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/stable/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/stable/topics/i18n/

LANGUAGE_CODE = 'en-us'

LANGUAGES = [
    ('en', _('English')),
]

LOCALE_PATHS = [
    '/app/src/locale',
]

TIME_ZONE = '{{ cookiecutter.timezone }}'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/stable/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '/var/app/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_ROOT = '/var/app/media/'

MEDIA_URL = 'media/'

X_FRAME_OPTIONS = 'ORIGIN'

# Default primary key field type
# https://docs.djangoproject.com/en/stable/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

{% if cookiecutter.worker == 'rq' -%}
REDIS_HOST = env.str('REDIS_HOST')
REDIS_PORT = env.int('REDIS_PORT', 6379)
REDIS_DB = env.int('REDIS_DB', 0)
REDIS_PASSWORD = env.get('REDIS_PASSWORD')
REDIS_SOCKET_TIMEOUT = env.int('REDIS_SOCKET_TIMEOUT', 10)

RQ_QUEUES = {
    'default': {
        'HOST': REDIS_HOST,
        'PORT': REDIS_PORT,
        'DB': REDIS_DB,
        'PASSWORD': REDIS_PASSWORD,
        'SOCKET_TIMEOUT': REDIS_SOCKET_TIMEOUT,
        'DEFAULT_TIMEOUT': 24 * 60 * 60,  # 24h - allow long-running tasks
    },
}
{% elif cookiecutter.worker == 'celery' -%}
CELERY_RESULT_BACKEND = 'django-db'
CELERY_BROKER_URL = f'redis://{f'{REDIS_PASSWORD}@' if REDIS_PASSWORD else ''}{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}'
CELERY_BROKER_TRANSPORT_OPTIONS = {
    'max_retries': 1,
    'broker_connection_timeout': REDIS_SOCKET_TIMEOUT,
    'visibility_timeout': 24 * 60 * 60,  # 24h - allow long-running tasks
}
{% endif -%}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s.%(msecs)d] %(name)s (%(levelname)s) %(message)s',
            'datefmt': '%d/%b/%Y %H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'level': LOGGING_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console'],
    },
    'loggers': {
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.db.backends': {
            'level': 'INFO',
            'handlers': ['console'],
            'propagate': False,
        },
        'asyncio': {
            'level': 'WARNING',
            'handlers': ['console'],
            'propagate': False,
        },
        'parso': {
            'level': 'WARNING',
            'handlers': ['console'],
            'propagate': False,
        },
    },
    'filters': {},
}


# Advanced debug settings
SENTRY_DSN = env.get('SENTRY_DSN')
if SENTRY_DSN:
    import logging

    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    from sentry_sdk.integrations.logging import LoggingIntegration
    from sentry_sdk.integrations.logging import ignore_logger

    ignore_logger('django.security.DisallowedHost')
    sentry_sdk.init(
        release=f'{{ cookiecutter.django_project_name }}@{PROJECT_VERSION}',
        dsn=SENTRY_DSN,
        integrations=[
            DjangoIntegration(),
            LoggingIntegration(
                level=logging.INFO,
                event_level=logging.ERROR,
            ),
        ],
        send_default_pii=True,
        auto_session_tracking=False,
    )

if DEBUG_SQL:
    import sys

    try:
        from sqlparse import format as sqlformat
    except ImportError:
        sqlformat = lambda s, reindent=None: s
    from traceback import format_stack

    class WithStacktrace(object):
        def __init__(self, skip=(), limit=5):
            self.skip = [__name__, 'logging']
            self.skip.extend(skip)
            self.limit = limit

        def filter(self, record):
            if not hasattr(record, 'stack_patched'):
                frame = sys._getframe(1)
                while any(skip for skip in self.skip if frame.f_globals.get('__name__', '').startswith(skip)):
                    frame = frame.f_back
                stack = ''.join(f'\33[1;30m{line}\33[0m' for line in format_stack(f=frame, limit=self.limit))
                if hasattr(record, 'duration') and hasattr(record, 'sql') and hasattr(record, 'params'):
                    sql = '\n  '.join(f'\33[33m{line}\33[0m' for line in sqlformat(record.sql or '', reindent=True).strip().splitlines())
                    record.msg = (
                        f'\33[31mduration: \33[{"" if record.duration < 0.1 else "1;"}31m{record.duration:.4f} secs\33[0m, '
                        f'\33[33marguments: \33[1{";33" if record.params else ""}m{record.params}\33[0m'
                        f'\n  {sql}\n \33[1;32m-- stack: \n{stack}\33[0m'
                    )
                    record.args = ()
                else:
                    record.msg += f'\n \33[1;32m-- stack: \n{stack}\33[0m'

                record.stack_patched = True
            return True

    LOGGING['loggers']['django.db.backends']['level'] = 'DEBUG'
    LOGGING['loggers']['django.db.backends']['filters'] = ['add_stack']
    LOGGING['filters']['add_stack'] = {
        '()': WithStacktrace,
        'skip': ('django.db', 'south.', '__main__'),
        'limit': DEBUG_SQL_LIMIT,
    }

if LOGGING_PATH:
    LOGGING['handlers']['logfile'] = {
        'level': 'INFO',
        'class': 'logging.handlers.WatchedFileHandler',
        'encoding': 'utf-8',
        'filename': f'{LOGGING_PATH}/application.log',
        'formatter': 'verbose',
    }
    LOGGING['handlers']['debugfile'] = {
        'level': 'DEBUG',
        'class': 'logging.handlers.WatchedFileHandler',
        'encoding': 'utf-8',
        'filename': f'{LOGGING_PATH}/debug.log',
        'formatter': 'verbose',
    }
    LOGGING['root']['handlers'] = ['logfile', 'debugfile']
    LOGGING['loggers']['django.request']['handlers'] = ['logfile']
    LOGGING['loggers']['django.db.backends']['handlers'] = ['debugfile']

if DEBUG:
    INSTALLED_APPS += [
        'rosetta',
    ]

if DEBUG_TOOLBAR:
    INSTALLED_APPS += [
        'debug_toolbar',
    ]
    MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')
    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': lambda _: DEBUG,
    }
    DEBUG_TOOLBAR_PANELS = [
        'django_uwsgi.panels.UwsgiWorkersPanel',
        'django_uwsgi.panels.UwsgiActionsPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar.panels.signals.SignalsPanel',
        'debug_toolbar.panels.redirects.RedirectsPanel',
        'debug_toolbar.panels.profiling.ProfilingPanel',
    ]
