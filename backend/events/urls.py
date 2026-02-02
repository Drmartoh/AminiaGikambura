from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, EventRegistrationViewSet, AnnouncementViewSet

router = DefaultRouter()
router.register(r'', EventViewSet, basename='event')
router.register(r'registrations', EventRegistrationViewSet, basename='eventregistration')
router.register(r'announcements', AnnouncementViewSet, basename='announcement')

urlpatterns = [
    path('', include(router.urls)),
]
