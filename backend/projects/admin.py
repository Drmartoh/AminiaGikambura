from django.contrib import admin
from .models import County, Ministry, ProjectCategory, Project, ProjectMember, ProjectReport


@admin.register(County)
class CountyAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'created_at']
    search_fields = ['name', 'code']


@admin.register(Ministry)
class MinistryAdmin(admin.ModelAdmin):
    list_display = ['name', 'abbreviation', 'contact_email', 'created_at']
    search_fields = ['name', 'abbreviation']


@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'color', 'created_at']
    prepopulated_fields = {'slug': ('name',)}


class ProjectMemberInline(admin.TabularInline):
    model = ProjectMember
    extra = 1


class ProjectReportInline(admin.TabularInline):
    model = ProjectReport
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'county', 'status', 'budget_amount', 
                    'is_featured', 'is_public', 'created_at']
    list_filter = ['status', 'category', 'county', 'is_featured', 'is_public', 'created_at']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at', 'budget_utilization']
    inlines = [ProjectMemberInline, ProjectReportInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'description', 'objectives', 'category', 
                      'county', 'ministry', 'status', 'featured_image')
        }),
        ('Budget', {
            'fields': ('budget_amount', 'budget_currency', 'allocated_amount', 
                      'spent_amount', 'budget_utilization')
        }),
        ('Timeline', {
            'fields': ('start_date', 'end_date', 'completion_date')
        }),
        ('Settings', {
            'fields': ('is_featured', 'is_public', 'created_by')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(ProjectMember)
class ProjectMemberAdmin(admin.ModelAdmin):
    list_display = ['project', 'member', 'role', 'is_active', 'joined_date']
    list_filter = ['role', 'is_active', 'joined_date']
    search_fields = ['project__title', 'member__user__username']


@admin.register(ProjectReport)
class ProjectReportAdmin(admin.ModelAdmin):
    list_display = ['project', 'title', 'report_date', 'is_public', 'created_at']
    list_filter = ['is_public', 'report_date', 'created_at']
    search_fields = ['project__title', 'title']
