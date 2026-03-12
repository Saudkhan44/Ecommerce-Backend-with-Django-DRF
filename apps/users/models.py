# models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.conf import settings

# ======================================
# CUSTOM USER (prebuilt User + role)
# ======================================
class CustomUser(AbstractUser):
    """
    Extends Django's AbstractUser.
    Fields from SQL users table:
    - id, email, password, first_name, last_name, is_active, created_at (date_joined)
    Additional:
    - role (customer/admin)
    """
    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')

    def __str__(self):
        return self.email

# ======================================
# USER PROFILE
# ======================================
class UserProfile(models.Model):
    """
    Stores additional user info.
    - profile_image: ImageField stored in /media/profiles/
    - phone_number, address
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Profile of {self.user.email}"
