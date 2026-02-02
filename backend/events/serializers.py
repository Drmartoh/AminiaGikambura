from rest_framework import serializers
from .models import Event, EventRegistration, Announcement
from projects.serializers import ProjectListSerializer
from members.serializers import MemberProfileSerializer


class EventSerializer(serializers.ModelSerializer):
    county_name = serializers.CharField(source='county.name', read_only=True)
    project = ProjectListSerializer(read_only=True)
    registered_count = serializers.ReadOnlyField()
    is_full = serializers.ReadOnlyField()
    
    class Meta:
        model = Event
        fields = ['id', 'title', 'slug', 'description', 'event_type', 'featured_image',
                  'venue', 'county', 'county_name', 'address', 'is_online', 'online_link',
                  'start_date', 'end_date', 'registration_deadline', 'requires_registration',
                  'max_participants', 'registration_fee', 'project', 'is_published',
                  'is_featured', 'registered_count', 'is_full', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'registered_count', 'is_full']


class EventRegistrationSerializer(serializers.ModelSerializer):
    event = EventSerializer(read_only=True)
    member = MemberProfileSerializer(read_only=True)
    
    class Meta:
        model = EventRegistration
        fields = ['id', 'event', 'member', 'full_name', 'email', 'phone',
                  'is_confirmed', 'payment_status', 'notes', 'registered_at']
        read_only_fields = ['id', 'registered_at']


class EventRegistrationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventRegistration
        fields = ['event', 'full_name', 'email', 'phone', 'notes']


class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ['id', 'title', 'slug', 'content', 'featured_image', 'is_published',
                  'is_featured', 'publish_date', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
