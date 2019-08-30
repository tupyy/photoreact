"""
This is a django-split-settings main file.
To change settings file:
`DJANGO_ENV=production python manage.py runserver`
"""
from os import environ

from split_settings.tools import include

from .utils import utils

# Managing environment via DJANGO_ENV variable:
<<<<<<< HEAD
environ.setdefault('DJANGO_ENV', 'dev_work')
=======
environ.setdefault('DJANGO_ENV', 'testing')
>>>>>>> fe39c27402e6e020c45285e19429b348478b3d5f
ENV = environ['DJANGO_ENV']

base_settings = [
    'components/logging.py',
    'components/common.py',
    'components/database.py',
    # Select the right env:
    'environments/{0}.py'.format(ENV),

]

# Include settings:
include(*base_settings)
