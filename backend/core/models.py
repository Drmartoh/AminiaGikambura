import re
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class Constituency(models.Model):
    """Kiambu County constituency (for member registration)."""
    name = models.CharField(max_length=100, unique=True)
    order = models.PositiveSmallIntegerField(default=0, help_text='Display order')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = 'Constituencies'

    def __str__(self):
        return self.name


class Ward(models.Model):
    """Kiambu County ward (for member registration)."""
    constituency = models.ForeignKey(Constituency, on_delete=models.CASCADE, related_name='wards')
    name = models.CharField(max_length=100)
    order = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['constituency', 'order', 'name']
        unique_together = [['constituency', 'name']]
        verbose_name_plural = 'Wards'

    def __str__(self):
        return f"{self.name} ({self.constituency.name})"


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    Roles: public, member (CBO members), donor (sponsors), county_official, admin, super_admin.
    Admins are created only by super_admin from the backend; others register via website.
    """
    ROLE_CHOICES = [
        ('public', 'Public User'),
        ('member', 'Member'),
        ('donor', 'Donor / Sponsor'),
        ('county_official', 'County Official'),
        ('admin', 'Admin'),
        ('super_admin', 'Super Admin'),
    ]
    DEPARTMENT_CHOICES = [
        ('administration', 'Administration & Public Service'),
        ('agriculture', 'Agriculture, Livestock & Irrigation'),
        ('education', 'Education, Gender, Culture & Social Services'),
        ('finance', 'Finance, ICT & Economic Planning'),
        ('health', 'Health Services'),
        ('land', 'Land, Housing, Physical Planning & Urban Development'),
        ('roads', 'Roads, Transport & Public Works'),
        ('trade', 'Trade, Industrialization, Tourism and Investment'),
        ('water', 'Water, Environment, Natural Resources and Climate Change'),
        ('youth', 'Youth Affairs, Sports & Communication'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='public')
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    is_verified = models.BooleanField(default=False)  # Used for county officials
    is_approved = models.BooleanField(default=False)  # For member/donor approval
    # Member registration (CBO members)
    id_or_passport_number = models.CharField(max_length=30, blank=True, null=True, verbose_name='ID or Passport number')
    full_names_as_on_id = models.CharField(max_length=200, blank=True, null=True, verbose_name='Full names as on ID/Passport')
    ward = models.ForeignKey('core.Ward', on_delete=models.SET_NULL, null=True, blank=True, related_name='members')
    # Donor: name or company stored in first_name; optional company in company_name
    company_name = models.CharField(max_length=200, blank=True, help_text='Company / organization name (for donors)')
    # County official
    department = models.CharField(max_length=40, choices=DEPARTMENT_CHOICES, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return self.username
    
    @property
    def is_member(self):
        return self.role == 'member' and self.is_approved
    
    @property
    def is_admin_user(self):
        return self.role in ['admin', 'super_admin']


class AuditLog(models.Model):
    """
    Audit log for tracking admin actions
    """
    ACTION_CHOICES = [
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('approve', 'Approve'),
        ('reject', 'Reject'),
        ('verify', 'Verify'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='audit_logs')
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    model_name = models.CharField(max_length=100)
    object_id = models.CharField(max_length=100)
    object_repr = models.CharField(max_length=200)
    changes = models.JSONField(default=dict, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Audit Log'
        verbose_name_plural = 'Audit Logs'
        indexes = [
            models.Index(fields=['-timestamp']),
            models.Index(fields=['user', '-timestamp']),
        ]
    
    def __str__(self):
        return f"{self.user} - {self.action} - {self.model_name} - {self.timestamp}"


class SiteSettings(models.Model):
    """Singleton: logo, hotlines, address, social links (editable in admin)."""
    site_name = models.CharField(max_length=200, default='AGCBO Digital Hub')
    registration_number = models.CharField(max_length=80, blank=True, default='DSD/22/120/02/168788', help_text='CBO Registration No. (displayed in header and key areas)')
    logo = models.ImageField(upload_to='site/', blank=True, null=True, help_text='Organization logo (header)')
    favicon = models.ImageField(upload_to='site/', blank=True, null=True)
    hotline_1 = models.CharField(max_length=25, blank=True, default='+254715574285')
    hotline_2 = models.CharField(max_length=25, blank=True, default='+254728758157')
    hotline_3 = models.CharField(max_length=25, blank=True, default='+254787786299')
    email = models.EmailField(blank=True, default='info@agcbo.org')
    address = models.TextField(blank=True, default="Gikambura (BUJU), Karai Ward, Youth Labour Office, Just Besides MCA's Office Along Gikambura Stadium")
    box_number = models.CharField(max_length=50, blank=True)
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Site settings'
        verbose_name_plural = 'Site settings'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class Official(models.Model):
    """CBO officials (Chairperson, Treasurer, Secretary, etc.) – displayed on Officials page."""
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=120, help_text='e.g. Chairperson, Treasurer, Secretary')
    bio = models.TextField(blank=True, help_text='Short bio or role description (optional)')
    photo = models.ImageField(upload_to='officials/', blank=True, null=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=25, blank=True)
    order = models.PositiveSmallIntegerField(default=0, help_text='Display order (lower first)')
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = 'Officials'

    def __str__(self):
        return f"{self.name} – {self.title}"


class YouthJob(models.Model):
    """Community youth jobs / opportunities – displayed on Youth Jobs page."""
    title = models.CharField(max_length=200)
    description = models.TextField()
    organization = models.CharField(max_length=200, blank=True, help_text='Employer or organization name')
    location = models.CharField(max_length=200, blank=True)
    application_deadline = models.DateField(null=True, blank=True)
    apply_url = models.URLField(blank=True, help_text='Link to apply or more info')
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=25, blank=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Youth jobs / opportunities'

    def __str__(self):
        return self.title


class AboutPage(models.Model):
    """Editable About page content (singleton). When set, public About page uses this."""
    tagline = models.CharField(max_length=300, blank=True, default='Empowering youth, transforming communities')
    vision = models.TextField(blank=True)
    mission = models.TextField(blank=True)
    our_story = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'About page content'
        verbose_name_plural = 'About page content'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class SectionStyle(models.Model):
    """Background style for a site section (header, hero, footer, etc.). Editable from manage panel."""
    BACKGROUND_TYPES = [
        ('plain', 'Plain (solid color)'),
        ('image', 'Single image'),
        ('video', 'Video (upload or URL)'),
        ('carousel', 'Image carousel / slides'),
        ('auto_slides', 'Automatic sliding carousel'),
    ]
    section_key = models.CharField(
        max_length=60, unique=True,
        help_text='e.g. header, hero, about_hero, contact_hero, footer. Used in templates.'
    )
    label = models.CharField(max_length=120, help_text='Display name in admin (e.g. Header, Home Hero)')
    background_type = models.CharField(max_length=20, choices=BACKGROUND_TYPES, default='plain')
    background_color = models.CharField(max_length=20, blank=True, default='#ffffff')
    background_image = models.ImageField(upload_to='sections/', blank=True, null=True)
    background_video = models.FileField(upload_to='sections/video/', blank=True, null=True)
    background_video_url = models.URLField(blank=True, help_text='Or use YouTube/Vimeo URL instead of upload')
    slide_interval_seconds = models.PositiveSmallIntegerField(default=5, help_text='For carousel/auto_slides')
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['section_key']
        verbose_name = 'Section background'
        verbose_name_plural = 'Section backgrounds'

    def __str__(self):
        return f"{self.label} ({self.section_key})"

    def get_video_embed_url(self):
        """Return embed URL for background_video_url (YouTube/Vimeo) or None."""
        url = (self.background_video_url or '').strip()
        if not url:
            return None
        m = re.search(r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([a-zA-Z0-9_-]{11})', url)
        if m:
            return f'https://www.youtube.com/embed/{m.group(1)}?autoplay=1&mute=1&loop=1&controls=0&playsinline=1'
        m = re.search(r'vimeo\.com/(?:video/)?(\d+)', url)
        if m:
            return f'https://player.vimeo.com/video/{m.group(1)}?autoplay=1&muted=1&loop=1'
        return None


class SectionSlide(models.Model):
    """Single slide image for a carousel/auto_slides section."""
    section_style = models.ForeignKey(SectionStyle, on_delete=models.CASCADE, related_name='slides')
    image = models.ImageField(upload_to='sections/slides/')
    order = models.PositiveSmallIntegerField(default=0)
    caption = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ['section_style', 'order']

    def __str__(self):
        return f"Slide {self.order} for {self.section_style.section_key}"
