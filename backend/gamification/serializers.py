from rest_framework import serializers
from .models import Badge, MemberBadge, PointsTransaction, Leaderboard
from members.serializers import MemberProfileSerializer


class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = ['id', 'name', 'slug', 'description', 'icon', 'icon_class',
                  'points_required', 'badge_type', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']


class MemberBadgeSerializer(serializers.ModelSerializer):
    badge = BadgeSerializer(read_only=True)
    member = MemberProfileSerializer(read_only=True)
    
    class Meta:
        model = MemberBadge
        fields = ['id', 'member', 'badge', 'earned_date', 'notes']
        read_only_fields = ['id', 'earned_date']


class PointsTransactionSerializer(serializers.ModelSerializer):
    member = MemberProfileSerializer(read_only=True)
    
    class Meta:
        model = PointsTransaction
        fields = ['id', 'member', 'points', 'transaction_type', 'description',
                  'project', 'event', 'created_at']
        read_only_fields = ['id', 'created_at']


class LeaderboardSerializer(serializers.ModelSerializer):
    member = MemberProfileSerializer(read_only=True)
    
    class Meta:
        model = Leaderboard
        fields = ['id', 'year', 'month', 'member', 'total_points', 'rank',
                  'badges_count', 'created_at']
        read_only_fields = ['id', 'created_at']
