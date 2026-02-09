"""
Storage utility for optional Cloudinary support.
Only imports cloudinary_storage when credentials are set, so migrate/run work
without CLOUDINARY_STORAGE in settings (cloudinary_storage requires it on import).
"""
from django.conf import settings
from django.core.files.storage import FileSystemStorage


def get_storage():
    """Return Cloudinary storage only if credentials are set, else FileSystemStorage."""
    try:
        from decouple import config
        _cn = (config('CLOUDINARY_CLOUD_NAME', default='') or '').strip()
        _key = (config('CLOUDINARY_API_KEY', default='') or '').strip()
        _secret = (config('CLOUDINARY_API_SECRET', default='') or '').strip()
        if _cn and _key and _secret:
            from cloudinary_storage.storage import MediaCloudinaryStorage
            return MediaCloudinaryStorage()
    except Exception:
        pass
    return FileSystemStorage(location=settings.MEDIA_ROOT)
