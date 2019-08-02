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
environ.setdefault('DJANGO_ENV', 'dev_work')
ENV = environ['DJANGO_ENV']

base_settings = [
    'components/logging.py',
    'components/common.py',
    'components/database.py',
    # You can even use glob:
    # 'components/*.py'

    # Select the right env:
    'environments/{0}.py'.format(ENV),

]


# Include settings:
include(*base_settings)
