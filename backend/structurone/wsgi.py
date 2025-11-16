"""
WSGI config for StructurOne project.
"""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'structurone.settings')

application = get_wsgi_application()

