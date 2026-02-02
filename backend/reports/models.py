from django.db import models
from django.conf import settings
from core.storage import get_storage


class Report(models.Model):
    """
    Reports for various purposes
    """
    REPORT_TYPE_CHOICES = [
        ('member_participation', 'Member Participation'),
        ('project_progress', 'Project Progress'),
        ('funding_allocation', 'Funding Allocation'),
        ('financial', 'Financial'),
        ('annual', 'Annual'),
        ('quarterly', 'Quarterly'),
        ('monthly', 'Monthly'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=200)
    report_type = models.CharField(max_length=30, choices=REPORT_TYPE_CHOICES)
    description = models.TextField(blank=True)
    report_file = models.FileField(upload_to='reports/', storage=get_storage())
    report_url = models.URLField(blank=True)
    
    # Association
    project = models.ForeignKey('projects.Project', on_delete=models.SET_NULL, null=True, blank=True, related_name='reports')
    
    # Period
    period_start = models.DateField(null=True, blank=True)
    period_end = models.DateField(null=True, blank=True)
    report_date = models.DateField()
    
    # Metadata
    is_public = models.BooleanField(default=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-report_date']
        indexes = [
            models.Index(fields=['report_type', '-report_date']),
            models.Index(fields=['project', '-report_date']),
        ]
    
    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    """
    Contact messages from public website
    """
    STATUS_CHOICES = [
        ('new', 'New'),
        ('read', 'Read'),
        ('replied', 'Replied'),
        ('archived', 'Archived'),
    ]
    
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    replied_at = models.DateTimeField(null=True, blank=True)
    reply_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.subject}"
