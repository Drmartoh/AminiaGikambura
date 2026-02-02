from rest_framework import serializers
from .models import FundingSource, Sponsor, Donation, DonationTier
from projects.serializers import ProjectListSerializer


class FundingSourceSerializer(serializers.ModelSerializer):
    ministry_name = serializers.CharField(source='ministry.name', read_only=True)
    county_name = serializers.CharField(source='county.name', read_only=True)
    
    class Meta:
        model = FundingSource
        fields = ['id', 'name', 'source_type', 'ministry', 'ministry_name',
                  'county', 'county_name', 'description', 'logo', 'contact_email',
                  'contact_phone', 'website', 'created_at']
        read_only_fields = ['id', 'created_at']


class SponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = ['id', 'name', 'organization_type', 'description', 'logo',
                  'contact_email', 'contact_phone', 'website', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']


class DonationSerializer(serializers.ModelSerializer):
    project = ProjectListSerializer(read_only=True)
    sponsor = SponsorSerializer(read_only=True)
    
    class Meta:
        model = Donation
        fields = ['id', 'donor_name', 'donor_email', 'donor_phone', 'is_anonymous',
                  'amount', 'currency', 'payment_method', 'status', 'project',
                  'sponsor', 'transaction_id', 'mpesa_receipt_number', 'payment_reference',
                  'receipt_sent', 'receipt_email', 'notes', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'transaction_id']


class DonationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = ['donor_name', 'donor_email', 'donor_phone', 'is_anonymous',
                  'amount', 'currency', 'payment_method', 'project', 'notes']


class DonationTierSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonationTier
        fields = ['id', 'name', 'amount', 'currency', 'description', 'project', 
                  'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']
