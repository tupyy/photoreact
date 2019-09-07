# -*- coding: utf-8 -*-

"""
This file contains all the settings that defines the development server.


SECURITY WARNING: don't run with debug turned on in production!
"""
import os

from photogallery.settings.components.database import DATABASES_DEV
from photogallery.settings import utils

DEBUG = True

SECRET_KEY = "my_super_secret_key"

ALLOWED_HOSTS = ['*']

"""
Database dev
"""
DATABASES = DATABASES_DEV

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
    },
}

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_WHITELIST = [
    'http://localhost:7000',
]
CORS_ORIGIN_REGEX_WHITELIST = [
    'http://localhost:7000',
]

"""
Load AWS variables
"""
config_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'config.env')
if os.path.exists(config_file_path):
    utils.load_env(config_file_path)
else:
    print('Config file not found')
