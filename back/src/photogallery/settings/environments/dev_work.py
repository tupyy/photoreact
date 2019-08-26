import os

from src.photogallery.settings.components.database import DATABASES_DEV_WORK
from src.photogallery.settings import utils

DEBUG = True

SECRET_KEY = "my_super_secret_key"

ALLOWED_HOSTS = ['*']

"""
Database dev
"""
DATABASES = DATABASES_DEV_WORK

"""
Load AWS variables
"""
config_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'config.env')
if os.path.exists(config_file_path):
    utils.load_env(config_file_path)
else:
    print('Config file not found at: {}'.format(config_file_path))