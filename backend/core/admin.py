from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, AuditLog, Constituency, Ward, SiteSettings, Official, YouthJob, AboutPage, SectionStyle, SectionSlide


@admin.register(Constituency)
class ConstituencyAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'ward_count']
    ordering = ['order', 'name']

    def ward_count(self, obj):
        return obj.wards.count()
    ward_count.short_description = 'Wards'


@admin.register(Ward)
class WardAdmin(admin.ModelAdmin):
    list_display = ['name', 'constituency', 'order']
    list_filter = ['constituency']
    search_fields = ['name', 'constituency__name']
    ordering = ['constituency', 'order', 'name']


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'updated_at']
    fieldsets = (
        (None, {'fields': ('site_name', 'registration_number', 'logo', 'favicon')}),
        ('Contact', {'fields': ('hotline_1', 'hotline_2', 'hotline_3', 'email', 'address', 'box_number')}),
        ('Social', {'fields': ('facebook_url', 'twitter_url', 'instagram_url', 'youtube_url', 'linkedin_url')}),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'get_full_name_display', 'email', 'phone_number', 'ward_display', 'role', 'is_approved', 'is_active', 'created_at']
    list_filter = ['role', 'is_verified', 'is_approved', 'is_active', 'is_staff', 'created_at']
    search_fields = ['username', 'email', 'phone_number', 'first_name', 'last_name', 'full_names_as_on_id', 'id_or_passport_number']
    list_editable = ['is_approved']
    actions = ['approve_members', 'reject_members']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Member registration', {
            'fields': ('id_or_passport_number', 'full_names_as_on_id', 'ward', 'phone_number')
        }),
        ('Status', {
            'fields': ('role', 'is_verified', 'is_approved', 'last_login_ip')
        }),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('role', 'phone_number', 'email')
        }),
    )

    def get_full_name_display(self, obj):
        return obj.full_names_as_on_id or obj.get_full_name() or '—'
    get_full_name_display.short_description = 'Full name'

    def ward_display(self, obj):
        return obj.ward.name if obj.ward else '—'
    ward_display.short_description = 'Ward'

    @admin.action(description='Approve selected members')
    def approve_members(self, request, queryset):
        updated = queryset.filter(role='member').update(is_approved=True)
        self.message_user(request, f'{updated} member(s) approved.')

    @admin.action(description='Reject / unapprove selected')
    def reject_members(self, request, queryset):
        updated = queryset.update(is_approved=False)
        self.message_user(request, f'{updated} user(s) unapproved.')


@admin.register(Official)
class OfficialAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'order', 'is_published', 'updated_at']
    list_editable = ['order', 'is_published']
    list_filter = ['is_published']
    search_fields = ['name', 'title']


@admin.register(YouthJob)
class YouthJobAdmin(admin.ModelAdmin):
    list_display = ['title', 'organization', 'application_deadline', 'is_published', 'created_at']
    list_filter = ['is_published', 'created_at']
    search_fields = ['title', 'description', 'organization']


@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    list_display = ['updated_at']

    def has_add_permission(self, request):
        return not AboutPage.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


class SectionSlideInline(admin.TabularInline):
    model = SectionSlide
    extra = 0


@admin.register(SectionStyle)
class SectionStyleAdmin(admin.ModelAdmin):
    list_display = ['section_key', 'label', 'background_type', 'is_active', 'updated_at']
    list_filter = ['background_type', 'is_active']
    inlines = [SectionSlideInline]
    fieldsets = (
        (None, {'fields': ('section_key', 'label', 'background_type', 'is_active')}),
        ('Plain', {'fields': ('background_color',), 'classes': ('collapse',)}),
        ('Image', {'fields': ('background_image',), 'classes': ('collapse',)}),
        ('Video', {'fields': ('background_video', 'background_video_url'), 'classes': ('collapse',)}),
        ('Carousel / Slides', {'fields': ('slide_interval_seconds',), 'classes': ('collapse',)}),
    )


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'model_name', 'object_repr', 'timestamp', 'ip_address']
    list_filter = ['action', 'model_name', 'timestamp']
    search_fields = ['user__username', 'model_name', 'object_repr']
    readonly_fields = ['user', 'action', 'model_name', 'object_id', 'object_repr', 'changes', 'ip_address', 'timestamp']
    date_hierarchy = 'timestamp'
