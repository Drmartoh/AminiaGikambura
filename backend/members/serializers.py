from rest_framework import serializers
from core.serializers import UserSerializer
from .models import MemberProfile, Certificate


class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = ['id', 'title', 'description', 'issued_by', 'issue_date', 
                  'certificate_file', 'certificate_url', 'created_at']
        read_only_fields = ['id', 'created_at']


class MemberProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    certificates = CertificateSerializer(many=True, read_only=True)
    skills_list = serializers.SerializerMethodField()
    interests_list = serializers.SerializerMethodField()
    
    class Meta:
        model = MemberProfile
        fields = ['id', 'user', 'profile_picture', 'date_of_birth', 'gender', 
                  'id_number', 'address', 'county', 'skills', 'interests', 
                  'skills_list', 'interests_list', 'bio', 'emergency_contact_name',
                  'emergency_contact_phone', 'joined_date', 'is_active', 'certificates']
        read_only_fields = ['id', 'joined_date']
    
    def get_skills_list(self, obj):
        return [s.strip() for s in obj.skills.split(',')] if obj.skills else []
    
    def get_interests_list(self, obj):
        return [i.strip() for i in obj.interests.split(',')] if obj.interests else []


class MemberProfileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberProfile
        fields = ['date_of_birth', 'gender', 'id_number', 'address', 'county',
                  'skills', 'interests', 'bio', 'emergency_contact_name', 
                  'emergency_contact_phone', 'profile_picture']
