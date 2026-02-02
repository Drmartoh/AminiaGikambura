from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from .models import SportProgram, Team, TeamMember, Match, TrainingSchedule
from .serializers import (
    SportProgramSerializer, TeamSerializer, TeamMemberSerializer,
    MatchSerializer, TrainingScheduleSerializer
)


class SportProgramViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SportProgram.objects.filter(is_active=True)
    serializer_class = SportProgramSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class TeamViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Team.objects.select_related('sport_program').prefetch_related('team_members').filter(is_active=True)
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['sport_program']


class MatchViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Match.objects.select_related('team__sport_program').all()
    serializer_class = MatchSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['team', 'match_type', 'result']


class TrainingScheduleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TrainingSchedule.objects.select_related('team').all()
    serializer_class = TrainingScheduleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['team']
