import os
import sys
import random
import django

# Path settings for accessing the project
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'civil_registry.settings')

# Setting up Django
django.setup()

from django.contrib.auth.models import User
from users.models import UserProfile, AdminConsumptionLimit
from datetime import date

def generate_national_code():