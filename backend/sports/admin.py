from django.contrib import admin
from .models import SportProgram, Team, TeamMember, Match, TrainingSchedule


@admin.register(SportProgram)
class SportProgramAdmin(admin.ModelAdmin):
    list_display = ['name', 'sport_type', 'is_active', 'created_at']
    list_filter = ['is_active', 'sport_type', 'created_at']
    search_fields = ['name', 'sport_type']


class TeamMemberInline(admin.TabularInline):
    model = TeamMember
    extra = 1


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'sport_program', 'coach_name', 'is_active', 'created_at']
    list_filter = ['sport_program', 'is_active', 'created_at']
    search_fields = ['name', 'coach_name']
    inlines = [TeamMemberInline]


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['team', 'member', 'position', 'jersey_number', 'is_active', 'joined_date']
    list_filter = ['position', 'is_active', 'joined_date']
    search_fields = ['team__name', 'member__user__username']


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ['team', 'opponent', 'match_type', 'match_date', 'our_score', 
                    'opponent_score', 'result', 'created_at']
    list_filter = ['match_type', 'result', 'match_date', 'created_at']
    search_fields = ['team__name', 'opponent', 'venue']
    date_hierarchy = 'match_date'


@admin.register(TrainingSchedule)
class TrainingScheduleAdmin(admin.ModelAdmin):
    list_display = ['team', 'title', 'venue', 'start_time', 'end_time', 
                    'is_recurring', 'created_at']
    list_filter = ['is_recurring', 'start_time', 'created_at']
    search_fields = ['team__name', 'title', 'venue']
    date_hierarchy = 'start_time'
