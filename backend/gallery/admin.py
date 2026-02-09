from django.contrib import admin
from django.utils.html import format_html
from .models import GalleryItem


@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ['thumbnail_preview', 'title', 'media_type', 'project', 'event', 'year',
                    'is_featured', 'is_public', 'created_at']
    list_filter = ['media_type', 'year', 'is_featured', 'is_public', 'created_at']
    search_fields = ['title', 'description', 'tags']
    date_hierarchy = 'created_at'
    list_editable = ['is_featured', 'is_public']
    readonly_fields = ['thumbnail_preview_large']

    def thumbnail_preview(self, obj):
        url = obj.image_url if hasattr(obj, 'image_url') else (obj.file.url if obj.file and hasattr(obj.file, 'url') else obj.url)
        if url:
            return format_html('<img src="{}" width="60" height="60" style="object-fit:cover;border-radius:6px;" />', url)
        return '—'
    thumbnail_preview.short_description = 'Preview'

    def thumbnail_preview_large(self, obj):
        url = obj.image_url if hasattr(obj, 'image_url') else (obj.file.url if obj.file and hasattr(obj.file, 'url') else obj.url)
        if url:
            return format_html('<img src="{}" style="max-width:400px;height:auto;border-radius:8px;" />', url)
        return '—'
    thumbnail_preview_large.short_description = 'Preview'

    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'media_type', 'thumbnail_preview_large'),
            'description': 'Add an image by uploading a file OR by pasting a direct image URL (e.g. from Facebook, Instagram, or any website).'
        }),
        ('Image / video source (use one)', {
            'fields': ('file', 'url'),
            'description': 'Images: upload a file or paste a direct image URL. Videos: set Media type to "Video" and paste a YouTube or Vimeo link (e.g. https://www.youtube.com/watch?v=...) — the video will be embedded and play on the site.'
        }),
        ('Association', {'fields': ('project', 'event')}),
        ('Meta', {'fields': ('year', 'tags', 'is_featured', 'is_public')}),
    )
