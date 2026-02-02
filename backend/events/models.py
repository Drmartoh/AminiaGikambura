from django.db import models
from django.conf import settings
from core.storage import get_storage


class Event(models.Model):
    """
    Events and activities
    """
    EVENT_TYPE_CHOICES = [
        ('workshop', 'Workshop'),
        ('training', 'Training'),
        ('meeting', 'Meeting'),
        ('community_service', 'Community Service'),
        ('sports', 'Sports'),
        ('cultural', 'Cultural'),
        ('fundraising', 'Fundraising'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    event_type = models.CharField(max_length=30, choices=EVENT_TYPE_CHOICES)
    featured_image = models.ImageField(upload_to='events/', storage=get_storage(), blank=True, null=True)
    
    # Location
    venue = models.CharField(max_length=200)
    county = models.ForeignKey('projects.County', on_delete=models.SET_NULL, null=True, blank=True)
    address = models.TextField(blank=True)
    is_online = models.BooleanField(default=False)
    online_link = models.URLField(blank=True)
    
    # Timing
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    registration_deadline = models.DateTimeField(null=True, blank=True)
    
    # Registration
    requires_registration = models.BooleanField(default=False)
    max_participants = models.IntegerField(null=True, blank=True)
    registration_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Association
    project = models.ForeignKey('projects.Project', on_delete=models.SET_NULL, null=True, blank=True, related_name='events')
    
    # Status
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    
    # Metadata
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-start_date']
        indexes = [
            models.Index(fields=['start_date', 'is_published']),
            models.Index(fields=['event_type', 'is_published']),
        ]
    
    def __str__(self):
        return self.title
    
    @property
    def registered_count(self):
        return self.event_registrations.filter(is_confirmed=True).count()
    
    @property
    def is_full(self):
        if self.max_participants:
            return self.registered_count >= self.max_participants
        return False


class EventRegistration(models.Model):
    """
    Event registrations
    """
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event_registrations')
    member = models.ForeignKey('members.MemberProfile', on_delete=models.CASCADE, null=True, blank=True, related_name='event_registrations')
    
    # For non-member registrations
    full_name = models.CharField(max_length=200, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    
    is_confirmed = models.BooleanField(default=False)
    payment_status = models.CharField(max_length=20, default='pending', choices=[
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('free', 'Free'),
    ])
    notes = models.TextField(blank=True)
    registered_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['event', 'member']
        ordering = ['-registered_at']
    
    def __str__(self):
        if self.member:
            return f"{self.member.user.username} - {self.event.title}"
        return f"{self.full_name} - {self.event.title}"


class Announcement(models.Model):
    """
    Announcements and news posts
    """
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    featured_image = models.ImageField(upload_to='announcements/', storage=get_storage(), blank=True, null=True)
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    publish_date = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-publish_date', '-created_at']
    
    def __str__(self):
        return self.title
