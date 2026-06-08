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