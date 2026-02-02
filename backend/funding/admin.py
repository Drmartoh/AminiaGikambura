from django.contrib import admin
from .models import FundingSource, Sponsor, Donation, DonationTier


@admin.register(FundingSource)
class FundingSourceAdmin(admin.ModelAdmin):
    list_display = ['name', 'source_type', 'ministry', 'county', 'created_at']
    list_filter = ['source_type', 'created_at']
    search_fields = ['name', 'description']


@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = ['name', 'organization_type', 'is_active', 'created_at']
    list_filter = ['is_active', 'organization_type', 'created_at']
    search_fields = ['name', 'organization_type']


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ['donor_name', 'amount', 'currency', 'payment_method', 
                    'status', 'project', 'created_at']
    list_filter = ['status', 'payment_method', 'currency', 'created_at']
    search_fields = ['donor_name', 'donor_email', 'transaction_id', 'mpesa_receipt_number']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'


@admin.register(DonationTier)
class DonationTierAdmin(admin.ModelAdmin):
    list_display = ['name', 'amount', 'currency', 'project', 'is_active', 'created_at']
    list_filter = ['is_active', 'currency', 'created_at']
    search_fields = ['name', 'description']
