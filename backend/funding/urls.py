from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FundingSourceViewSet, SponsorViewSet, DonationViewSet, DonationTierViewSet

router = DefaultRouter()
router.register(r'sources', FundingSourceViewSet, basename='fundingsource')
router.register(r'sponsors', SponsorViewSet, basename='sponsor')
router.register(r'donations', DonationViewSet, basename='donation')
router.register(r'tiers', DonationTierViewSet, basename='donationtier')

urlpatterns = [
    path('', include(router.urls)),
]
