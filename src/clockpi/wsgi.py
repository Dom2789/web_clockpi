"""
WSGI config for clockpi project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

import os
import sys
import datetime

# Debug output: print to Apache error log
sys.stderr.write(f"[WSGI DEBUG] wsgi.py loaded at {datetime.datetime.now()}\n")

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clockpi.settings')

application = get_wsgi_application()

sys.stderr.write("[WSGI DEBUG] WSGI application successfully created.\n")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clockpi.settings')

# Debug output when application object is created
sys.stderr.write("[WSGI DEBUG] Creating WSGI application...\n")
