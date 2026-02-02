from rest_framework import serializers
from .models import Report, ContactMessage
from projects.serializers import ProjectListSerializer


class ReportSerializer(serializers.ModelSerializer):
    project = ProjectListSerializer(read_only=True)
    
    class Meta:
        model = Report
        fields = ['id', 'title', 'report_type', 'description', 'report_file',
                  'report_url', 'project', 'period_start', 'period_end',
                  'report_date', 'is_public', 'created_at']
        read_only_fields = ['id', 'created_at']


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['id', 'name', 'email', 'phone', 'subject', 'message',
                  'status', 'created_at']
        read_only_fields = ['id', 'status', 'created_at']


class ContactMessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']
