from django.contrib import admin
from .models import Report, ContactMessage


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['title', 'report_type', 'project', 'report_date', 
                    'is_public', 'created_at']
    list_filter = ['report_type', 'is_public', 'report_date', 'created_at']
    search_fields = ['title', 'description']
    date_hierarchy = 'report_date'


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
