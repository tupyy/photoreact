# -*- coding: utf-8 -*-

"""
This file contains all the settings that defines the development server.


SECURITY WARNING: don't run with debug turned on in production!
"""
from photogallery.settings.components.database import DATABASES_DEV
DEBUG = True

SECRET_KEY = "my_super_secret_key"

ALLOWED_HOSTS = ['*']

"""
Database dev
"""
DATABASES = DATABASES_DEV

