# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES_DEV = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'photo2',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': '172.17.0.3',
        'PORT': '5432',
    }
}
