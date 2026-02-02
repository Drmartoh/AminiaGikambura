from rest_framework import serializers
from .models import SportProgram, Team, TeamMember, Match, TrainingSchedule
from members.serializers import MemberProfileSerializer


class SportProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = SportProgram
        fields = ['id', 'name', 'description', 'sport_type', 'logo', 
                  'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']


class TeamMemberSerializer(serializers.ModelSerializer):
    member = MemberProfileSerializer(read_only=True)
    
    class Meta:
        model = TeamMember
        fields = ['id', 'member', 'position', 'jersey_number', 'joined_date', 'is_active']
        read_only_fields = ['id', 'joined_date']


class TeamSerializer(serializers.ModelSerializer):
    sport_program = SportProgramSerializer(read_only=True)
    team_members = TeamMemberSerializer(many=True, read_only=True)
    
    class Meta:
        model = Team
        fields = ['id', 'name', 'sport_program', 'description', 'logo', 
                  'coach_name', 'coach_phone', 'is_active', 'created_at', 'team_members']
        read_only_fields = ['id', 'created_at']


class MatchSerializer(serializers.ModelSerializer):
    team = TeamSerializer(read_only=True)
    
    class Meta:
        model = Match
        fields = ['id', 'team', 'opponent', 'match_type', 'venue', 'match_date',
                  'our_score', 'opponent_score', 'result', 'notes', 'created_at']
        read_only_fields = ['id', 'created_at']


class TrainingScheduleSerializer(serializers.ModelSerializer):
    team = TeamSerializer(read_only=True)
    
    class Meta:
        model = TrainingSchedule
        fields = ['id', 'team', 'title', 'description', 'venue', 'start_time',
                  'end_time', 'is_recurring', 'recurrence_pattern', 'created_at']
        read_only_fields = ['id', 'created_at']
