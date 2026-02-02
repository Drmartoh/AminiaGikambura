from django.db import models
from django.conf import settings
from core.storage import get_storage


class County(models.Model):
    """
    Counties in Kenya
    """
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True, blank=True, null=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Counties'
    
    def __str__(self):
        return self.name


class Ministry(models.Model):
    """
    Government Ministries
    """
    name = models.CharField(max_length=200, unique=True)
    abbreviation = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='ministries/', storage=get_storage(), blank=True, null=True)
    website = models.URLField(blank=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Ministries'
    
    def __str__(self):
        return self.name


class ProjectCategory(models.Model):
    """
    Categories for projects
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Font Awesome icon class")
    color = models.CharField(max_length=7, default='#0d4f3c', help_text="Hex color code")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Project Categories'
    
    def __str__(self):
        return self.name


class Project(models.Model):
    """
    CBO Projects
    """
    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
        ('cancelled', 'Cancelled'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    objectives = models.TextField(help_text="Project objectives and goals")
    category = models.ForeignKey(ProjectCategory, on_delete=models.SET_NULL, null=True, related_name='projects')
    county = models.ForeignKey(County, on_delete=models.SET_NULL, null=True, related_name='projects')
    ministry = models.ForeignKey(Ministry, on_delete=models.SET_NULL, null=True, blank=True, related_name='projects')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned')
    
    # Budget
    budget_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    budget_currency = models.CharField(max_length=3, default='KES')
    allocated_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    spent_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Timeline
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    completion_date = models.DateField(null=True, blank=True)
    
    # Media
    featured_image = models.ImageField(upload_to='projects/', storage=get_storage(), blank=True, null=True)
    
    # Metadata
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_projects')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False)
    is_public = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['category', 'status']),
            models.Index(fields=['county', 'status']),
        ]
    
    def __str__(self):
        return self.title
    
    @property
    def budget_utilization(self):
        """Calculate budget utilization percentage"""
        if self.budget_amount > 0:
            return (self.spent_amount / self.budget_amount) * 100
        return 0
    
    @property
    def is_active(self):
        return self.status == 'ongoing'


class ProjectMember(models.Model):
    """
    Many-to-many relationship between Projects and Members
    """
    ROLE_CHOICES = [
        ('leader', 'Project Leader'),
        ('coordinator', 'Coordinator'),
        ('member', 'Member'),
        ('volunteer', 'Volunteer'),
    ]
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_members')
    member = models.ForeignKey('members.MemberProfile', on_delete=models.CASCADE, related_name='member_projects')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    joined_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['project', 'member']
        ordering = ['-joined_date']
    
    def __str__(self):
        return f"{self.member.user.username} - {self.project.title}"


class ProjectReport(models.Model):
    """
    Reports for projects (PDFs, documents)
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_reports')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    report_file = models.FileField(upload_to='project_reports/', storage=get_storage())
    report_url = models.URLField(blank=True)
    report_date = models.DateField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-report_date']
    
    def __str__(self):
        return f"{self.project.title} - {self.title}"
