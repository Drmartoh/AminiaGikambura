from django.db import models
from django.conf import settings
from core.storage import get_storage


class GalleryItem(models.Model):
    """
    Gallery items (photos and videos)
    """
    MEDIA_TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES, default='image')
    file = models.FileField(upload_to='gallery/', storage=get_storage())
    thumbnail = models.ImageField(upload_to='gallery/thumbnails/', storage=get_storage(), blank=True, null=True)
    url = models.URLField(blank=True, help_text="External URL for videos")
    
    # Association
    project = models.ForeignKey('projects.Project', on_delete=models.SET_NULL, null=True, blank=True, related_name='gallery_items')
    event = models.ForeignKey('events.Event', on_delete=models.SET_NULL, null=True, blank=True, related_name='gallery_items')
    
    # Metadata
    year = models.IntegerField(help_text="Year the media was taken")
    tags = models.CharField(max_length=500, blank=True, help_text="Comma-separated tags")
    is_featured = models.BooleanField(default=False)
    is_public = models.BooleanField(default=True)
    
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['year', 'is_public']),
            models.Index(fields=['project', 'is_public']),
            models.Index(fields=['media_type', 'is_public']),
        ]
    
    def __str__(self):
        return self.title
