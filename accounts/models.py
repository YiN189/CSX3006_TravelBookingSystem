# accounts/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom User Model with three roles:
    - customer: Regular user who books hotels/flights
    - partner: Partner admin who manages hotels/flights
    - admin: System admin with full access
    """

    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('partner', 'Partner Admin'),
        ('admin', 'System Admin'),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='customer',
        help_text='User role in the system'
    )

    email = models.EmailField(
        unique=True,
        help_text='Email address (must be unique)'
    )

    phone = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        help_text='Contact phone number'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    def is_customer(self):
        return self.role == 'customer'

    def is_partner(self):
        return self.role == 'partner'

    def is_system_admin(self):
        return self.role == 'admin'


class UserProfile(models.Model):
    """
    Extended profile information for users
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    bio = models.TextField(
        blank=True,
        null=True,
        help_text='User biography'
    )

    profile_picture = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True
    )

    date_of_birth = models.DateField(
        blank=True,
        null=True
    )

    address = models.TextField(
        blank=True,
        null=True
    )

    city = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    country = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    postal_code = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    def __str__(self):
        return f"Profile of {self.user.username}"
    