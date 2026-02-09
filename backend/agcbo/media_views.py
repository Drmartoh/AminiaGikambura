"""
Serve uploaded media files (images, videos, logos, etc.) in development and production.
Uses Django's static.serve so /media/* requests are served from MEDIA_ROOT.
"""
import os
from django.views.static import serve
from django.conf import settings
from django.http import Http404


def serve_media(request, path):
    """
    Serve files from MEDIA_ROOT. path is the part after /media/ (e.g. site/logo.jpg).
    Uses a resolved absolute MEDIA_ROOT so it works regardless of working directory.
    """
    document_root = os.path.abspath(os.path.realpath(str(settings.MEDIA_ROOT)))
    path = path.strip('/')
    if '..' in path or path.startswith('/'):
        raise Http404("Invalid path")
    return serve(request, path, document_root=document_root)
