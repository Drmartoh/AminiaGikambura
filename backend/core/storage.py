"""
Storage utility for optional Cloudinary support.
Uses Django settings.CLOUDINARY_AVAILABLE so Cloudinary is only used when configured (credentials set).
"""
from django.conf import settings

MediaCloudinaryStorage = None
try:
    from cloudinary_storage.storage import MediaCloudinaryStorage
except ImportError:
    pass

def get_storage():
    """Return Cloudinary storage only if configured in settings, else None (filesystem)."""
    if getattr(settings, 'CLOUDINARY_AVAILABLE', False) and MediaCloudinaryStorage is not None:
        return MediaCloudinaryStorage()
    return None
