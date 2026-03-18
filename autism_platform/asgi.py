"""
ASGI config for Autism Learning Platform.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "autism_platform.settings")

application = get_asgi_application()
