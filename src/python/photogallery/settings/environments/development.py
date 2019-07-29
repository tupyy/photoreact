# -*- coding: utf-8 -*-

"""
This file contains all the settings that defines the development server.


SECURITY WARNING: don't run with debug turned on in production!
"""
import os

from photogallery.settings.components.database import DATABASES_DEV
from photogallery.settings.utils import utils

DEBUG = True

SECRET_KEY = "my_super_secret_key"

ALLOWED_HOSTS = ['*']

"""
Database dev
"""
DATABASES = DATABASES_DEV

"""
Load AWS variables
"""
config_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'config.env')
if os.path.exists(config_file_path):
    utils.load_env(config_file_path)
else:
    print('Config file not found')