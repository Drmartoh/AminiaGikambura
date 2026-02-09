import re
from django.db import models
from django.core.exceptions import ValidationError
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
    file = models.FileField(upload_to='gallery/', storage=get_storage(), blank=True, null=True, help_text='Upload an image/video file')
    thumbnail = models.ImageField(upload_to='gallery/thumbnails/', storage=get_storage(), blank=True, null=True)
    url = models.URLField(blank=True, help_text='Or paste a direct image/video URL (e.g. from Facebook, Instagram, or any website). Use either file upload OR link.')
    
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

    def clean(self):
        if not self.file and not self.url:
            raise ValidationError('Provide either an uploaded file or an image/video URL.')

    @property
    def image_url(self):
        """Display URL: from uploaded file or from external link (for images)."""
        if self.file and getattr(self.file, 'url', None):
            return self.file.url
        if self.url and self.media_type == 'image':
            return self.url
        return None

    def get_embed_url(self):
        """Convert YouTube/Vimeo watch URL to embed URL for iframe. Returns None for non-embed videos."""
        if not self.url:
            return None
        url = self.url.strip()
        # YouTube: watch?v=ID, youtu.be/ID, or already embed
        yt_match = re.search(r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([a-zA-Z0-9_-]{11})', url)
        if yt_match:
            return f'https://www.youtube.com/embed/{yt_match.group(1)}'
        # Vimeo: vimeo.com/ID or player.vimeo.com/video/ID
        vimeo_match = re.search(r'vimeo\.com/(?:video/)?(\d+)', url)
        if vimeo_match:
            return f'https://player.vimeo.com/video/{vimeo_match.group(1)}'
        return url
