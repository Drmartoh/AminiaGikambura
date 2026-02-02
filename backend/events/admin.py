from django.contrib import admin
from .models import Event, EventRegistration, Announcement


class EventRegistrationInline(admin.TabularInline):
    model = EventRegistration
    extra = 0
    readonly_fields = ['registered_at']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'event_type', 'start_date', 'venue', 
                    'requires_registration', 'is_published', 'is_featured', 'created_at']
    list_filter = ['event_type', 'is_published', 'is_featured', 'requires_registration', 'created_at']
    search_fields = ['title', 'description', 'venue']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at', 'registered_count']
    inlines = [EventRegistrationInline]
    date_hierarchy = 'start_date'


@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ['event', 'member', 'full_name', 'is_confirmed', 
                    'payment_status', 'registered_at']
    list_filter = ['is_confirmed', 'payment_status', 'registered_at']
    search_fields = ['event__title', 'member__user__username', 'full_name', 'email']


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_published', 'is_featured', 'publish_date', 'created_at']
    list_filter = ['is_published', 'is_featured', 'created_at']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'publish_date'
