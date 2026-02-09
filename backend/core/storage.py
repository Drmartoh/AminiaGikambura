"""
Storage utility for optional Cloudinary support.
Checks credentials directly so Cloudinary is only used when properly configured,
even if settings.CLOUDINARY_AVAILABLE is wrong (e.g. old settings on server).
"""
from django.conf import settings
from django.core.files.storage import FileSystemStorage

MediaCloudinaryStorage = None
try:
    from cloudinary_storage.storage import MediaCloudinaryStorage
except ImportError:
    pass

def get_storage():
    """Return Cloudinary storage only if credentials are set, else FileSystemStorage."""
    if MediaCloudinaryStorage is None:
        return FileSystemStorage(location=settings.MEDIA_ROOT)
    try:
        from decouple import config
        _cn = config('CLOUDINARY_CLOUD_NAME', default='')
        _key = config('CLOUDINARY_API_KEY', default='')
        _secret = config('CLOUDINARY_API_SECRET', default='')
        if _cn.strip() and _key.strip() and _secret.strip():
            return MediaCloudinaryStorage()
    except Exception:
        pass
    return FileSystemStorage(location=settings.MEDIA_ROOT)
