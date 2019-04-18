import django_heroku
import dj_database_url

from config.settings.base import *

# Database
# Heroku: Update database configuration from $DATABASE_URL.
DATABASES = {'default': dj_database_url.config(conn_max_age=500)}

django_heroku.settings(locals(), logging=False, staticfiles=False)
