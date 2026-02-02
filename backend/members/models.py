from django.db import models
from django.conf import settings
from core.storage import get_storage


class MemberProfile(models.Model):
    """
    Extended profile for members
    """
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='member_profile')
    profile_picture = models.ImageField(upload_to='profiles/', storage=get_storage(), blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    id_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True)
    county = models.ForeignKey('projects.County', on_delete=models.SET_NULL, null=True, blank=True)
    skills = models.TextField(help_text="Comma-separated list of skills", blank=True)
    interests = models.TextField(help_text="Comma-separated list of interests", blank=True)
    bio = models.TextField(blank=True)
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_phone = models.CharField(max_length=15, blank=True)
    joined_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-joined_date']
        verbose_name = 'Member Profile'
        verbose_name_plural = 'Member Profiles'
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username}"


class Certificate(models.Model):
    """
    Certificates earned by members
    """
    member = models.ForeignKey(MemberProfile, on_delete=models.CASCADE, related_name='certificates')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    issued_by = models.CharField(max_length=200)
    issue_date = models.DateField()
    certificate_file = models.FileField(upload_to='certificates/', storage=get_storage(), blank=True, null=True)
    certificate_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-issue_date']
    
    def __str__(self):
        return f"{self.member.user.username} - {self.title}"
