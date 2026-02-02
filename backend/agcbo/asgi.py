"""
ASGI config for agcbo project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agcbo.settings')

application = get_asgi_application()
