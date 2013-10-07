# Django settings for dash project.

#Must run this on mysql db at initial setup:
#alter table nrdb_release change release_id release_id bigint;
import os
import django
import sys
reload(sys)
sys.setdefaultencoding('utf-8') #fixes bug with localization

#================The below must be changed per the environment=================
ENVIRONMENT = "local" #choices are "development","production", or "local"
DEBUG = True 
#==============================================================================

TEMPLATE_DEBUG = DEBUG


DJANGO_ROOT = os.path.dirname(os.path.realpath(django.__file__))
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
sys.path.append('%s/libs' % SITE_ROOT)                  #adds lib directory to python's path
sys.path.append('%s/nrforms' % SITE_ROOT) 

ADMINS = (
    ('Matthew', ''),
)

MANAGERS = ADMINS

#Environments
if ENVIRONMENT == 'development': 
    DATABASE_ENGINE = 'mysql'     # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
    DATABASE_NAME = ''       # Or path to database file if using sqlite3.
    DATABASE_USER = ''            # Not used with sqlite3.
    DATABASE_PASSWORD = ''        # Not used with sqlite3.
    DATABASE_HOST = ''            # Set to empty string for localhost. Not used with sqlite3.
    DATABASE_PORT = ''            # Set to empty string for default. Not used with sqlite3.

    MEDIA_ROOT = '/Users/user/home/work/mercurial/pgm/newreleases/media' #'/Library/Webserver/Documents/static/'
    MEDIA_URL = 'http://localhost/static/'
    ADMIN_MEDIA_PREFIX = '/static/'
    SITE_PREFIX = '/newreleases/'

elif ENVIRONMENT == 'production':
    DATABASE_ENGINE = 'mysql'     # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
    DATABASE_NAME = ''       # Or path to database file if using sqlite3.
    DATABASE_USER = ''            # Not used with sqlite3.
    DATABASE_PASSWORD = ''        # Not used with sqlite3.
    DATABASE_HOST = ''            # Set to empty string for localhost. Not used with sqlite3.
    DATABASE_PORT = ''            # Set to empty string for default. Not used with sqlite3.
    
    MEDIA_ROOT = os.path.join(SITE_ROOT, 'static')
    MEDIA_URL = '/static/'
    ADMIN_MEDIA_PREFIX = '/static/admin-media/'
    SITE_PREFIX = '/newreleases/'


elif ENVIRONMENT == 'local':
    DATABASE_ENGINE = 'mysql'     # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
    DATABASE_NAME = ''      # Or path to database file if using sqlite3.
    DATABASE_USER = ''            # Not used with sqlite3.
    DATABASE_PASSWORD = ''        # Not used with sqlite3.
    DATABASE_HOST = ''            # Set to empty string for localhost. Not used with sqlite3.
    DATABASE_PORT = ''            # Set to empty string for default. Not used with sqlite3.

    MEDIA_ROOT = '/Users/user/home/work/mercurial/pgm/newreleases/media' #'/Library/Webserver/Documents/static/'
    MEDIA_URL = 'http://localhost/static/'
    ADMIN_MEDIA_PREFIX = '/static/'
    SITE_PREFIX = '/'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Los Angeles'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 2

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# MEDIA_ROOT = Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
# MEDIA_URL = URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
# ADMIN_MEDIA_PREFIX = URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
    
# Make this unique, and don't share it with anybody.
SECRET_KEY = ''

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'djangomako.middleware.MakoMiddleware',   #Required to display templates.  This app does not use default django templates.
)

ROOT_URLCONF = 'newreleases.urls'

TEMPLATE_DIRS = (
    os.path.join(SITE_ROOT, 'templates')
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django_evolution',
    'newreleases.nrdb',
)
