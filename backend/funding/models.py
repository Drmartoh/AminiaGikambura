from django.db import models
from django.conf import settings
from core.storage import get_storage


class FundingSource(models.Model):
    """
    Funding sources (Ministries, County Government, etc.)
    """
    SOURCE_TYPE_CHOICES = [
        ('ministry', 'Ministry'),
        ('county', 'County Government'),
        ('donor', 'Donor'),
        ('sponsor', 'Sponsor'),
        ('self_funded', 'Self-Funded'),
    ]
    
    name = models.CharField(max_length=200)
    source_type = models.CharField(max_length=20, choices=SOURCE_TYPE_CHOICES)
    ministry = models.ForeignKey('projects.Ministry', on_delete=models.SET_NULL, null=True, blank=True)
    county = models.ForeignKey('projects.County', on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='funding_sources/', storage=get_storage(), blank=True, null=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    website = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Sponsor(models.Model):
    """
    Sponsors and donors
    """
    name = models.CharField(max_length=200)
    organization_type = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='sponsors/', storage=get_storage(), blank=True, null=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    website = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Donation(models.Model):
    """
    Donations received
    """
    PAYMENT_METHOD_CHOICES = [
        ('mpesa', 'M-Pesa'),
        ('bank', 'Bank Transfer'),
        ('paypal', 'PayPal'),
        ('stripe', 'Stripe'),
        ('cash', 'Cash'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Donor information
    donor_name = models.CharField(max_length=200)
    donor_email = models.EmailField()
    donor_phone = models.CharField(max_length=20, blank=True)
    is_anonymous = models.BooleanField(default=False)
    
    # Donation details
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default='KES')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Project association (optional)
    project = models.ForeignKey('projects.Project', on_delete=models.SET_NULL, null=True, blank=True, related_name='donations')
    sponsor = models.ForeignKey(Sponsor, on_delete=models.SET_NULL, null=True, blank=True, related_name='donations')
    
    # Payment details
    transaction_id = models.CharField(max_length=200, blank=True, unique=True, null=True)
    mpesa_receipt_number = models.CharField(max_length=50, blank=True)
    payment_reference = models.CharField(max_length=200, blank=True)
    
    # Receipt
    receipt_sent = models.BooleanField(default=False)
    receipt_email = models.EmailField(blank=True)
    
    # Metadata
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['project', 'status']),
            models.Index(fields=['transaction_id']),
        ]
    
    def __str__(self):
        return f"{self.donor_name} - {self.amount} {self.currency}"


class DonationTier(models.Model):
    """
    Predefined donation tiers for campaigns
    """
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='KES')
    description = models.TextField(blank=True)
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, null=True, blank=True, related_name='donation_tiers')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['amount']
    
    def __str__(self):
        return f"{self.name} - {self.amount} {self.currency}"
