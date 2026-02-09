"""
URL configuration for agcbo project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .api_root import api_root
from .media_views import serve_media

# JWT views (optional)
try:
    from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
    JWT_AVAILABLE = True
except ImportError:
    JWT_AVAILABLE = False

urlpatterns = [
    path('admin/', admin.site.urls),
    # Serve uploaded media (logo, images, videos) from MEDIA_ROOT – explicit view so it works in production
    path('media/<path:path>', serve_media),
    path('', include('pages.urls', namespace='pages')),
    path('manage/', include('pages.manage_urls', namespace='manage')),
    path('api/', api_root, name='api-root'),
    path('api/auth/', include('core.urls')),
    path('api/members/', include('members.urls')),
    path('api/projects/', include('projects.urls')),
    path('api/funding/', include('funding.urls')),
    path('api/events/', include('events.urls')),
    path('api/gallery/', include('gallery.urls')),
    path('api/sports/', include('sports.urls')),
    path('api/gamification/', include('gamification.urls')),
    path('api/reports/', include('reports.urls')),
]

# Serve static files in development; in production use Web server / collectstatic + mapping
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
