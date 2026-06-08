from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class UserProfile(models.Model):
    """
    Extended profile model for registered users.
    Contains civil registry information and consumption management settings.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    # Civil Registry Information
    national_code = models.CharField(max_length=10, unique=True, verbose_name="National Code")
    first_name = models.CharField(max_length=50, verbose_name="First Name")
    last_name = models.CharField(max_length=50, verbose_name="Last Name")
    phone_number = models.CharField(max_length=15, unique=True, verbose_name="Phone Number")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Date of Birth")
    address = models.TextField(blank=True, null=True, verbose_name="Address")
    