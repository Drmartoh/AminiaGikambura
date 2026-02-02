from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.db.models import Sum, Count
from django.utils import timezone
from .models import Badge, MemberBadge, PointsTransaction, Leaderboard
from .serializers import (
    BadgeSerializer, MemberBadgeSerializer, PointsTransactionSerializer,
    LeaderboardSerializer
)
from members.models import MemberProfile


class BadgeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Badge.objects.filter(is_active=True)
    serializer_class = BadgeSerializer
    permission_classes = [IsAuthenticated]


class MemberBadgeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MemberBadge.objects.select_related('member__user', 'badge').all()
    serializer_class = MemberBadgeSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_admin_user:
            return self.queryset
        if hasattr(user, 'member_profile'):
            return self.queryset.filter(member=user.member_profile)
        return self.queryset.none()


class PointsTransactionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PointsTransaction.objects.select_related('member__user', 'project', 'event').all()
    serializer_class = PointsTransactionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_admin_user:
            return self.queryset
        if hasattr(user, 'member_profile'):
            return self.queryset.filter(member=user.member_profile)
        return self.queryset.none()
    
    @action(detail=False, methods=['get'])
    def my_points(self, request):
        """Get current user's total points"""
        if not hasattr(request.user, 'member_profile'):
            return Response({'total_points': 0, 'transactions': []})
        
        member = request.user.member_profile
        total_points = PointsTransaction.objects.filter(member=member).aggregate(
            total=Sum('points')
        )['total'] or 0
        
        recent_transactions = PointsTransaction.objects.filter(member=member)[:10]
        serializer = self.get_serializer(recent_transactions, many=True)
        
        return Response({
            'total_points': total_points,
            'recent_transactions': serializer.data
        })


class LeaderboardViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Leaderboard.objects.select_related('member__user').all()
    serializer_class = LeaderboardSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        year = self.request.query_params.get('year', timezone.now().year)
        month = self.request.query_params.get('month', timezone.now().month)
        return self.queryset.filter(year=year, month=month).order_by('rank')[:100]
    
    @action(detail=False, methods=['get'])
    def current(self, request):
        """Get current month's leaderboard"""
        now = timezone.now()
        leaderboard = self.queryset.filter(year=now.year, month=now.month).order_by('rank')[:20]
        serializer = self.get_serializer(leaderboard, many=True)
        return Response(serializer.data)
