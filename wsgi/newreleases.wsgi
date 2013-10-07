import os
import sys

sys.path.append('/home/mlapora/pgm')
os.environ['DJANGO_SETTINGS_MODULE'] = 'newreleases.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
