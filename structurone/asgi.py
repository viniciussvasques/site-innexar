"""
ASGI config for StructurOne project.
"""
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'structurone.settings')

application = get_asgi_application()

