from django.contrib import admin
from .models import Badge, MemberBadge, PointsTransaction, Leaderboard


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ['name', 'badge_type', 'points_required', 'is_active', 'created_at']
    list_filter = ['badge_type', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(MemberBadge)
class MemberBadgeAdmin(admin.ModelAdmin):
    list_display = ['member', 'badge', 'earned_date']
    list_filter = ['badge', 'earned_date']
    search_fields = ['member__user__username', 'badge__name']
    date_hierarchy = 'earned_date'


@admin.register(PointsTransaction)
class PointsTransactionAdmin(admin.ModelAdmin):
    list_display = ['member', 'points', 'transaction_type', 'project', 'event', 'created_at']
    list_filter = ['transaction_type', 'created_at']
    search_fields = ['member__user__username', 'description']
    date_hierarchy = 'created_at'


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ['year', 'month', 'member', 'total_points', 'rank', 'badges_count', 'created_at']
    list_filter = ['year', 'month', 'created_at']
    search_fields = ['member__user__username']
    ordering = ['year', 'month', 'rank']
