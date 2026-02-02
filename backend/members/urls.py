from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MemberProfileViewSet, CertificateViewSet

router = DefaultRouter()
router.register(r'profiles', MemberProfileViewSet, basename='memberprofile')
router.register(r'certificates', CertificateViewSet, basename='certificate')

urlpatterns = [
    path('', include(router.urls)),
]
