from django.db import models
from django.conf import settings
from core.storage import get_storage


class SportProgram(models.Model):
    """
    Sports programs
    """
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    sport_type = models.CharField(max_length=100, help_text="e.g., Football, Basketball, Athletics")
    logo = models.ImageField(upload_to='sports/', storage=get_storage(), blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Team(models.Model):
    """
    Sports teams
    """
    name = models.CharField(max_length=200)
    sport_program = models.ForeignKey(SportProgram, on_delete=models.CASCADE, related_name='teams')
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='teams/', storage=get_storage(), blank=True, null=True)
    coach_name = models.CharField(max_length=200, blank=True)
    coach_phone = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.sport_program.name})"


class TeamMember(models.Model):
    """
    Team members
    """
    POSITION_CHOICES = [
        ('player', 'Player'),
        ('captain', 'Captain'),
        ('vice_captain', 'Vice Captain'),
        ('substitute', 'Substitute'),
    ]
    
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_members')
    member = models.ForeignKey('members.MemberProfile', on_delete=models.CASCADE, related_name='team_memberships')
    position = models.CharField(max_length=20, choices=POSITION_CHOICES, default='player')
    jersey_number = models.IntegerField(null=True, blank=True)
    joined_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['team', 'member']
        ordering = ['jersey_number', 'member__user__first_name']
    
    def __str__(self):
        return f"{self.member.user.username} - {self.team.name}"


class Match(models.Model):
    """
    Sports matches
    """
    MATCH_TYPE_CHOICES = [
        ('friendly', 'Friendly'),
        ('league', 'League'),
        ('tournament', 'Tournament'),
        ('training', 'Training Match'),
    ]
    
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='matches')
    opponent = models.CharField(max_length=200)
    match_type = models.CharField(max_length=20, choices=MATCH_TYPE_CHOICES, default='friendly')
    venue = models.CharField(max_length=200)
    match_date = models.DateTimeField()
    
    # Scores
    our_score = models.IntegerField(null=True, blank=True)
    opponent_score = models.IntegerField(null=True, blank=True)
    
    # Result
    result = models.CharField(max_length=20, blank=True, choices=[
        ('win', 'Win'),
        ('loss', 'Loss'),
        ('draw', 'Draw'),
        ('pending', 'Pending'),
    ])
    
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-match_date']
    
    def __str__(self):
        return f"{self.team.name} vs {self.opponent} - {self.match_date}"


class TrainingSchedule(models.Model):
    """
    Training schedules
    """
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='training_schedules')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    venue = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_recurring = models.BooleanField(default=False)
    recurrence_pattern = models.CharField(max_length=100, blank=True, help_text="e.g., Every Monday, Every 2 weeks")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['start_time']
    
    def __str__(self):
        return f"{self.team.name} - {self.title}"
