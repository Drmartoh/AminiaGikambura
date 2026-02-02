from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReportViewSet, ContactMessageViewSet

router = DefaultRouter()
router.register(r'', ReportViewSet, basename='report')
router.register(r'contact', ContactMessageViewSet, basename='contactmessage')

urlpatterns = [
    path('', include(router.urls)),
]
