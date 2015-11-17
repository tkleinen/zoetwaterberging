"""
WSGI config for berging project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
import sys
import site

ALLDIRS = ['/var/www/vhosts/acaciadata.com/httpdocs/django/lib/python2.7/site-packages']

# Remember original sys.path.
prev_sys_path = list(sys.path) 

# Add each new site-packages directory.
for directory in ALLDIRS:
  site.addsitedir(directory)

# Reorder sys.path so new directories at the front.
new_sys_path = [] 
for item in list(sys.path): 
    if item not in prev_sys_path: 
        new_sys_path.append(item) 
        sys.path.remove(item) 
sys.path[:0] = new_sys_path

# Add the app's directory to the PYTHONPATH
sys.path.append('/var/www/vhosts/zoetwaterberging.nl/httpdocs/berging')
sys.path.append('/var/www/vhosts/zoetwaterberging.nl/httpdocs/berging/berging')

os.environ['DJANGO_SETTINGS_MODULE'] = 'berging.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

