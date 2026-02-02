from rest_framework import serializers
from .models import County, Ministry, ProjectCategory, Project, ProjectMember, ProjectReport
from members.serializers import MemberProfileSerializer


class CountySerializer(serializers.ModelSerializer):
    class Meta:
        model = County
        fields = ['id', 'name', 'code', 'description', 'created_at']
        read_only_fields = ['id', 'created_at']


class MinistrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Ministry
        fields = ['id', 'name', 'abbreviation', 'description', 'logo', 
                  'website', 'contact_email', 'contact_phone', 'created_at']
        read_only_fields = ['id', 'created_at']


class ProjectCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectCategory
        fields = ['id', 'name', 'slug', 'description', 'icon', 'color', 'created_at']
        read_only_fields = ['id', 'created_at']


class ProjectReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectReport
        fields = ['id', 'title', 'description', 'report_file', 'report_url', 
                  'report_date', 'created_at', 'is_public']
        read_only_fields = ['id', 'created_at']


class ProjectMemberSerializer(serializers.ModelSerializer):
    member = MemberProfileSerializer(read_only=True)
    
    class Meta:
        model = ProjectMember
        fields = ['id', 'member', 'role', 'joined_date', 'is_active']
        read_only_fields = ['id', 'joined_date']


class ProjectSerializer(serializers.ModelSerializer):
    category = ProjectCategorySerializer(read_only=True)
    county = CountySerializer(read_only=True)
    ministry = MinistrySerializer(read_only=True)
    project_members = ProjectMemberSerializer(many=True, read_only=True)
    reports = ProjectReportSerializer(many=True, read_only=True)
    budget_utilization = serializers.ReadOnlyField()
    
    class Meta:
        model = Project
        fields = ['id', 'title', 'slug', 'description', 'objectives', 'category',
                  'county', 'ministry', 'status', 'budget_amount', 'budget_currency',
                  'allocated_amount', 'spent_amount', 'budget_utilization',
                  'start_date', 'end_date', 'completion_date', 'featured_image',
                  'created_by', 'created_at', 'updated_at', 'is_featured', 
                  'is_public', 'project_members', 'reports']
        read_only_fields = ['id', 'created_at', 'updated_at', 'budget_utilization']


class ProjectListSerializer(serializers.ModelSerializer):
    category = ProjectCategorySerializer(read_only=True)
    county = CountySerializer(read_only=True)
    
    class Meta:
        model = Project
        fields = ['id', 'title', 'slug', 'description', 'category', 'county', 
                  'status', 'featured_image', 'is_featured', 'created_at']
