from django.contrib import admin
from .models import MemberProfile, Certificate


@admin.register(MemberProfile)
class MemberProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'county', 'gender', 'is_active', 'joined_date']
    list_filter = ['is_active', 'gender', 'county', 'joined_date']
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name', 'id_number']
    readonly_fields = ['joined_date']


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ['member', 'title', 'issued_by', 'issue_date']
    list_filter = ['issue_date', 'issued_by']
    search_fields = ['member__user__username', 'title', 'issued_by']
