from django.db import models
from django.conf import settings
from core.storage import get_storage


class Badge(models.Model):
    """
    Badges that members can earn
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    icon = models.ImageField(upload_to='badges/', storage=get_storage(), blank=True, null=True)
    icon_class = models.CharField(max_length=50, blank=True, help_text="Font Awesome icon class")
    points_required = models.IntegerField(default=0, help_text="Points needed to earn this badge")
    badge_type = models.CharField(max_length=50, choices=[
        ('achievement', 'Achievement'),
        ('participation', 'Participation'),
        ('leadership', 'Leadership'),
        ('volunteer', 'Volunteer'),
        ('special', 'Special'),
    ], default='achievement')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['points_required', 'name']
    
    def __str__(self):
        return self.name


class MemberBadge(models.Model):
    """
    Badges earned by members
    """
    member = models.ForeignKey('members.MemberProfile', on_delete=models.CASCADE, related_name='member_badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, related_name='member_badges')
    earned_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        unique_together = ['member', 'badge']
        ordering = ['-earned_date']
    
    def __str__(self):
        return f"{self.member.user.username} - {self.badge.name}"


class PointsTransaction(models.Model):
    """
    Points transactions for members
    """
    TRANSACTION_TYPE_CHOICES = [
        ('event_attendance', 'Event Attendance'),
        ('project_participation', 'Project Participation'),
        ('volunteer_hours', 'Volunteer Hours'),
        ('achievement', 'Achievement'),
        ('badge_earned', 'Badge Earned'),
        ('admin_adjustment', 'Admin Adjustment'),
        ('penalty', 'Penalty'),
    ]
    
    member = models.ForeignKey('members.MemberProfile', on_delete=models.CASCADE, related_name='points_transactions')
    points = models.IntegerField(help_text="Positive for earning, negative for deduction")
    transaction_type = models.CharField(max_length=30, choices=TRANSACTION_TYPE_CHOICES)
    description = models.TextField()
    
    # Association
    project = models.ForeignKey('projects.Project', on_delete=models.SET_NULL, null=True, blank=True)
    event = models.ForeignKey('events.Event', on_delete=models.SET_NULL, null=True, blank=True)
    
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['member', '-created_at']),
            models.Index(fields=['transaction_type', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.member.user.username} - {self.points} points - {self.transaction_type}"


class Leaderboard(models.Model):
    """
    Monthly leaderboard snapshots
    """
    year = models.IntegerField()
    month = models.IntegerField()
    member = models.ForeignKey('members.MemberProfile', on_delete=models.CASCADE, related_name='leaderboard_entries')
    total_points = models.IntegerField()
    rank = models.IntegerField()
    badges_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['year', 'month', 'member']
        ordering = ['year', 'month', 'rank']
        indexes = [
            models.Index(fields=['year', 'month', 'rank']),
        ]
    
    def __str__(self):
        return f"{self.year}-{self.month:02d} - {self.member.user.username} - Rank {self.rank}"
