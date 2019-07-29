"""
This is a django-split-settings main file.
To change settings file:
`DJANGO_ENV=production python manage.py runserver`
"""
import os
from os import environ
from split_settings.tools import include

from .utils import utils

# Managing environment via DJANGO_ENV variable:
environ.setdefault('DJANGO_ENV', 'development')
ENV = environ['DJANGO_ENV']

config_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'config.env')
if os.path.exists(config_file_path):
    utils.load_env(config_file_path)
else:
    print('Config file not found')

base_settings = [
    'components/logging.py',
    'components/common.py',
    'components/database.py',
    'components/aws.py',
    # You can even use glob:
    # 'components/*.py'

    # Select the right env:
    'environments/{0}.py'.format(ENV),

]


# Include settings:
include(*base_settings)
