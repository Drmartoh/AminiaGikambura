from django.contrib import admin
from .models import GalleryItem


@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'media_type', 'project', 'event', 'year', 
                    'is_featured', 'is_public', 'created_at']
    list_filter = ['media_type', 'year', 'is_featured', 'is_public', 'created_at']
    search_fields = ['title', 'description', 'tags']
    date_hierarchy = 'created_at'
