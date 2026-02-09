# Optional: Celery app (only if celery is installed; avoids ModuleNotFoundError on PythonAnywhere)
try:
    from .celery import app as celery_app
    __all__ = ('celery_app',)
except ImportError:
    celery_app = None
    __all__ = ()
