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
# Random national code generation for test .
 return f"{random.randint(10000000, 99999999)}"

def generate_phone_number():
 # Phone number in +98 format.
    return f"+98{random.randint(9100000000, 9999999999)}"

def populate_users(count=100000):
    print(f"Starting to populate {count} users...")
    
    created_users = 0
    created_profiles = 0
    
    for i in range(count):
        try:
           # Create a user 1 .
            username = f"user_{i}"
            first_name = f"First_{i}"
            last_name = f"Last_{i}"
            email = f"{username}@example.com"
            password = "password123"

            # Check for non-duplicates .
            if User.objects.filter(username=username).exists():
                continue

            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password
            )
            created_users += 1