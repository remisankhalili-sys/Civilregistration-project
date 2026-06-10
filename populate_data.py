import os
import sys
import random
import django

# Path settings for accessing the project
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'civil_registry.settings')

