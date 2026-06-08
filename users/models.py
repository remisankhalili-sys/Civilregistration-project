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

      # Consumption Settings (Default Limits)
    # These values can be changed by the admin
    daily_limit = models.IntegerField(default=10, help_text="Daily search limit", verbose_name="Daily Limit")
    monthly_limit = models.IntegerField(default=300, help_text="Monthly search limit", verbose_name="Monthly Limit")

    # Consumption Tracking Dates
    last_reset_daily = models.DateTimeField(default=timezone.now, help_text="Last daily reset time", verbose_name="Last Daily Reset")
    last_reset_monthly = models.DateTimeField(default=timezone.now, help_text="Last monthly reset time", verbose_name="Last Monthly Reset")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

        def __str__(self):
            return f"{self.first_name} {self.last_name} - {self.national_code}"

        def check_daily_limit(self):
            """Checks if the daily limit has been reached."""
            # If more than 24 hours have passed since last reset, reset daily consumption
            if timezone.now() - self.last_reset_daily > timedelta(days=1):
                self.daily_limit = 10 # Default value if admin hasn't changed it
                self.last_reset_daily = timezone.now()
                self.save()


            # Calculate today's searches
            today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
            today_searches = SearchLog.objects.filter(
                user=self.user, 
                timestamp__gte=today_start
            ).count()
            
            return today_searches < self.daily_limit
        
        def check_monthly_limit(self):
            """Checks if the monthly limit has been reached."""
            if timezone.now() - self.last_reset_monthly > timedelta(days=30):
                self.monthly_limit = 300 # Default value
                self.last_reset_monthly = timezone.now()
                self.save()

            # Calculate this month's searches
            month_start = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            month_searches = SearchLog.objects.filter(
                user=self.user,
                timestamp__gte=month_start
            ).count()

            return month_searches < self.monthly_limit
