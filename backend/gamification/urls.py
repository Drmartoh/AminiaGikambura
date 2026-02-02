from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BadgeViewSet, MemberBadgeViewSet, PointsTransactionViewSet,
    LeaderboardViewSet
)

router = DefaultRouter()
router.register(r'badges', BadgeViewSet, basename='badge')
router.register(r'member-badges', MemberBadgeViewSet, basename='memberbadge')
router.register(r'points', PointsTransactionViewSet, basename='pointstransaction')
router.register(r'leaderboard', LeaderboardViewSet, basename='leaderboard')

urlpatterns = [
    path('', include(router.urls)),
]
