"""
Storage utility for optional Cloudinary support
"""
try:
    from cloudinary_storage.storage import MediaCloudinaryStorage
    CLOUDINARY_AVAILABLE = True
except ImportError:
    CLOUDINARY_AVAILABLE = False
    MediaCloudinaryStorage = None

def get_storage():
    """Get storage class, returns MediaCloudinaryStorage if available, None otherwise"""
    return MediaCloudinaryStorage() if CLOUDINARY_AVAILABLE else None
