# -*- coding: utf-8 -*-

"""
This file contains all the settings used in production.

This file is required and if development.py is present these
values are overridden.
"""
import os

from app.settings.utils.utils import parse_db_variable

DEBUG = False

# TODO change this
ALLOWED_HOSTS = ['*']
SECRET_KEY = os.getenv('SECRET_KEY')

# TODO change origin list
CORS_ORIGIN_WHITELIST = (
    '*',
)

"""
Database Postgres for Heroku
"""
db_variables = parse_db_variable(os.environ.get('DATABASE_URL'))
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': db_variables[4],
        'USER': db_variables[0],
        'PASSWORD': db_variables[1],
        'HOST': db_variables[2],
        'PORT': db_variables[3]
    }
}

#white noise
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'




