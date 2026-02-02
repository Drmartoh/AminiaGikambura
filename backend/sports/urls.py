from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SportProgramViewSet, TeamViewSet, MatchViewSet, TrainingScheduleViewSet

router = DefaultRouter()
router.register(r'programs', SportProgramViewSet, basename='sportprogram')
router.register(r'teams', TeamViewSet, basename='team')
router.register(r'matches', MatchViewSet, basename='match')
router.register(r'training', TrainingScheduleViewSet, basename='trainingschedule')

urlpatterns = [
    path('', include(router.urls)),
]
